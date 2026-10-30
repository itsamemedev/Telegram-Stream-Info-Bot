"""nc.kennzahlen — v4.2-W122: Leistungssignale als Schnappschuss, billig zu lesen.

Die Pakete A bis E haben Signale gebaut — Loop-Lag, Gegendruck, Cache,
Kindprozesse, Speicher, Betriebslage — und sie stehen in /healthz. Was
fehlte:

**Ein Weg fuer Prometheus.** `/metrics` (beobachtung.py) kannte keines
davon und zaehlte stattdessen bei JEDEM Abruf in der Datenbank. Ein
Scraper alle 15 s ist damit eine Last, die mit der Datenbank waechst.

**Eine Geschichte.** /healthz sagt, wie es JETZT ist. Ob der Loop-Lag
seit gestern steigt, ob die fds ueber die Woche klettern — das stand
nirgends, solange niemand einen Monitoring-Stack betreibt. Eine Zeile
alle 15 Minuten im Journal ist der billigste Verlauf, den es gibt.

Deshalb ein **Schnappschuss**: der Bot erhebt alle paar Sekunden aus dem,
was er ohnehin im Speicher hat (keine Datenbank), und legt das Ergebnis
hier ab. Leser nehmen den fertigen Wert — eine Zuweisung, keine Sperre.
Das Alter des Schnappschusses geht mit, damit ein stehengebliebener
Erheber nicht wie ein gesunder Bot aussieht.

Bot-frei, stdlib-only. Ausgegeben werden nur Zahlen: keine Namen, keine
Pfade, keine Kommandozeilen.
"""
from __future__ import annotations

import os
import re
import threading
import time
from typing import Optional

# Ein Tupel (stand_monotonic, daten), als Ganzes ersetzt: das Lesen aus
# einem Flask-Thread sieht immer ein zusammengehoeriges Paar.
_STAND = [(0.0, {})]

_SEITE = os.sysconf("SC_PAGE_SIZE") if hasattr(os, "sysconf") else 4096


def veroeffentlichen(daten: dict, jetzt: Optional[float] = None) -> None:
    _STAND[0] = (time.monotonic() if jetzt is None else jetzt, dict(daten))


def stand(jetzt: Optional[float] = None) -> tuple:
    """-> (alter_s oder None, daten). None heisst: noch nie erhoben."""
    ts, daten = _STAND[0]
    jetzt = time.monotonic() if jetzt is None else jetzt
    # Ein Ausgang: "nie erhoben" ist ein Zustand, kein Fehlschlag — und er
    # muss als None sichtbar bleiben, nicht als Alter 0.
    return (round(jetzt - ts, 1) if ts else None), (daten if ts else {})


def prozess() -> dict:
    """RSS und Threads — ein Lesezugriff auf /proc/self/statm, sonst -1.

    statm statt status: eine Zeile mit Zahlen statt ~50 Zeilen Text zu
    zerlegen. Gemessen wird der residente Speicher, also das, was der
    OOM-Killer zaehlt."""
    rss_mb = -1.0
    if os.path.isfile("/proc/self/statm"):
        with open("/proc/self/statm") as f:
            teile = f.read().split()
        if len(teile) >= 2 and teile[1].isdigit():
            rss_mb = round(int(teile[1]) * _SEITE / 1048576.0, 1)
    return {"rss_mb": rss_mb, "threads": threading.active_count()}


_NAME = re.compile(r"[^a-zA-Z0-9_]")


def _flach(praefix: str, wert, aus: list) -> None:
    if isinstance(wert, bool):
        aus.append((praefix, 1 if wert else 0))
    elif isinstance(wert, (int, float)):
        aus.append((praefix, wert))
    elif isinstance(wert, dict):
        for k, v in wert.items():
            _flach(praefix + "_" + _NAME.sub("_", str(k)), v, aus)
    # Text, Listen und None werden nicht ausgegeben: Text kann Namen und
    # Pfade tragen, und eine Liste hat keine eindeutige Zahl.


def prometheus(daten: dict, praefix: str = "nightcrawler",
               alter_s: Optional[float] = None) -> str:
    """Alle Zahlen-Blaetter als Gauges im Prometheus-Textformat."""
    paare: list = []
    for k, v in daten.items():
        _flach(praefix + "_" + _NAME.sub("_", str(k)), v, paare)
    zeilen = ["# TYPE %s gauge\n%s %s\n" % (n, n, ("%g" % w) if isinstance(w, float) else w)
              for n, w in paare]
    zeilen.append("# HELP %s_kennzahlen_alter_sekunden Alter des Schnappschusses; "
                  "-1 = nie erhoben\n# TYPE %s_kennzahlen_alter_sekunden gauge\n"
                  "%s_kennzahlen_alter_sekunden %s\n"
                  % (praefix, praefix, praefix, -1 if alter_s is None else alter_s))
    return "".join(zeilen)


def zeile(d: dict) -> str:
    """Die Lagezeile fuer das Journal — eine Zeile, die man greppen und
       ueber Tage vergleichen kann. Fehlende Werte als '?', nie als 0."""
    def g(*pfad):
        w = d
        for p in pfad:
            w = w.get(p) if isinstance(w, dict) else None
        return "?" if w is None else w
    quote = g("livecache", "trefferquote")
    quote = "?" if quote == "?" else "%.0f %%" % (100.0 * quote)
    return ("Lage: Loop p99 %s ms (max %s) · Aufnahmen %s/%s · Restreams %s · "
            "Chats %s · fd %s/%s · RSS %s MB · Threads %s · Cache %s · "
            "Kinder %s · Log wartend %s"
            % (g("loop_lag", "p99_ms"), g("loop_lag", "max_ms"),
               g("gegendruck", "aufnahmen"), g("gegendruck", "aufnahmen_deckel"),
               g("betrieb", "restreams"), g("betrieb", "chat_clients"),
               g("gegendruck", "fd", "offen"), g("gegendruck", "fd", "grenze"),
               g("prozess", "rss_mb"), g("prozess", "threads"), quote,
               g("kinder", "laufend"), g("log", "wartend")))
