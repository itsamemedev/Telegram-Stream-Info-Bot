"""nc.eventlog — v4.1-W29: das Ereignisprotokoll schreiben, ohne zu blockieren.

════════════════════════════════════════════════════════════════════════
WARUM DIESES MODUL
════════════════════════════════════════════════════════════════════════
`log_event` schrieb direkt in die Datenbank — synchron, aus jedem Pfad.
Steht der Aufruf in einer async-Funktion, blockiert er unter Plattenlast den
GANZEN Event-Loop: keine Live-Prüfungen, kein Telegram, Discord trennt mit
"heartbeat blocked". Genau das stand in den Stack-Abzügen des Wächters vom
2026-09-03 (`on_comment` → `log_event`).

Die Funktion hat über dreissig Aufrufer, synchrone wie asynchrone. Sie alle
auf `await` umzustellen hiesse, dreissig Stellen anzufassen und die
Zusicherung zu brechen, die im Docstring steht: „Caller darf das aus jedem
Pfad aufrufen ohne Risiko".

Deshalb der andere Weg: **eine Warteschlange und EIN Schreiber-Thread.**
Der Aufrufer legt ab und geht weiter — synchron wie asynchron, ohne eine
einzige geänderte Aufrufstelle.

════════════════════════════════════════════════════════════════════════
DREI ENTSCHEIDUNGEN, DIE ERKLÄRT GEHÖREN
════════════════════════════════════════════════════════════════════════
**Die Schlange ist BEGRENZT.** Ein unbegrenzter Puffer vor einer hängenden
Platte ist ein Speicherleck mit Anlauf — dieselbe Sorte wie der Adress-Cache
in W25, nur schneller. Läuft sie voll, fallen NEUE Einträge raus und werden
GEZÄHLT. Ein stiller Verlust wäre bei einem Prüfprotokoll das Schlimmste:
es sähe aus, als wäre nichts passiert.

**EIN Schreiber, keine Nebenläufigkeit.** Das Protokoll ist eine Chronik;
zwei Threads würden die Reihenfolge zerwürfeln. Ein Thread hält sie exakt.

**Gebündelt geschrieben.** Bis zu `BUENDEL` Einträge gehen in EINE
Transaktion. Bei einem Chat-Ansturm ist das der Unterschied zwischen
zweihundert Schreibvorgängen und zweien — und die Platte war das Problem.
"""

import logging
import queue
import threading
import time

from nc.dbwrap import db_conn

log = logging.getLogger("TikTokBot")

# Platz für rund eine Minute Ansturm. Darüber ist etwas grundsätzlich kaputt,
# und dann ist Zählen ehrlicher als Puffern.
KAPAZITAET = 2000
BUENDEL = 50           # höchstens so viele Einträge in EINER Transaktion
_LEERLAUF = 0.25       # Wartezeit, wenn nichts anliegt

_SCHLANGE = queue.Queue(maxsize=KAPAZITAET)
_ZAEHLER = {"geschrieben": 0, "verworfen": 0, "fehler": 0}
_LAEUFT = {"an": False}          # modul-global, nicht als Objekt-Attribut
_START_SPERRE = threading.Lock()
_VERWORFEN_GEMELDET = {"ts": 0.0, "stand": 0}
_FEHLER_GEMELDET = {"ts": 0.0}


def _schreiber():
    """Der eine Schreiber. Läuft, bis der Prozess endet."""
    while True:
        try:
            erster = _SCHLANGE.get(timeout=_LEERLAUF)
        except queue.Empty:
            continue
        buendel = [erster]
        while len(buendel) < BUENDEL:
            try:
                buendel.append(_SCHLANGE.get_nowait())
            except queue.Empty:
                break
        try:
            with db_conn() as conn:
                conn.executemany(
                    "INSERT INTO event_log (ts, kind, severity, summary, payload) "
                    "VALUES (?,?,?,?,?)", buendel)
                conn.commit()
            _ZAEHLER["geschrieben"] += len(buendel)
        except Exception as e:
            # Nicht still: ein dauerhaft scheiterndes Protokoll heisst, dass
            # die Chronik Lücken hat, und das merkt sonst niemand. Gedrosselt,
            # damit eine kaputte Platte nicht das Log flutet.
            _ZAEHLER["fehler"] += len(buendel)
            # Gedrosselt ueber die ZEIT, nicht ueber den Zaehler. Ein
            # `% 100 == 1` haette hier nie ausgeloest: der Zaehler waechst in
            # Buendeln von bis zu 50, und 50 oder 100 treffen die 1 nicht —
            # der Schreibfehler waere still geblieben, ausgerechnet der, der
            # die Chronik loechert.
            _jetzt = time.monotonic()
            if _jetzt - _FEHLER_GEMELDET["ts"] >= 60:
                log.error("Ereignisprotokoll: %d Einträge nicht geschrieben "
                          "(zuletzt: %s)", _ZAEHLER["fehler"], e)
                _FEHLER_GEMELDET["ts"] = _jetzt
        finally:
            for _ in buendel:
                _SCHLANGE.task_done()


def _sicherstellen():
    """Den Schreiber starten, falls er noch nicht läuft.

    Der Wächter ist MODUL-GLOBAL und kein Objekt-Attribut: ein
    `getattr(obj, "_läuft")` bricht, sobald das Objekt neu erzeugt wird, und
    dann laufen zwei Schreiber (CLAUDE.md).
    """
    if _LAEUFT["an"]:
        return
    with _START_SPERRE:
        if _LAEUFT["an"]:
            return
        t = threading.Thread(target=_schreiber, name="eventlog", daemon=True)
        t.start()
        _LAEUFT["an"] = True


def schreibe(ts, kind, severity, summary, payload):
    """Einen Eintrag einreihen. Blockiert NIE — auch nicht, wenn die Platte hängt.

    Die Werte kommen fertig zugeschnitten herein: das Kürzen gehört zum
    Aufrufer, damit hier keine zweite Wahrheit über die Feldlängen entsteht.
    """
    _sicherstellen()
    try:
        _SCHLANGE.put_nowait((ts, kind, severity, summary, payload))
    except queue.Full:
        _ZAEHLER["verworfen"] += 1
        _melde_verworfen()


def _melde_verworfen():
    """Verworfene Einträge melden — höchstens alle 60 Sekunden, dafür mit Zahl.

    Ein Prüfprotokoll, das still Einträge verliert, ist schlimmer als keines:
    die Lücke sieht aus wie Ruhe.
    """
    jetzt = time.monotonic()
    if jetzt - _VERWORFEN_GEMELDET["ts"] < 60:
        return
    neu = _ZAEHLER["verworfen"] - _VERWORFEN_GEMELDET["stand"]
    log.error("Ereignisprotokoll überlastet: %d Einträge verworfen "
              "(insgesamt %d). Die Datenbank kommt nicht hinterher.",
              neu, _ZAEHLER["verworfen"])
    _VERWORFEN_GEMELDET["ts"] = jetzt
    _VERWORFEN_GEMELDET["stand"] = _ZAEHLER["verworfen"]


def stand():
    """Für die Diagnose: was liegt an, was ist durch, was ging verloren."""
    return {"warteschlange": _SCHLANGE.qsize(), "kapazitaet": KAPAZITAET,
            **_ZAEHLER}


def leeren(timeout=5.0):
    """Auf das Schreiben des Rests warten — für den geordneten Herunterfahren.

    Ohne diesen Aufruf verliert ein Neustart, was noch in der Schlange liegt:
    der Schreiber ist ein Daemon und stirbt mit dem Prozess. Bei einem harten
    Abbruch (SIGKILL) hilft auch das nicht — dann sind die letzten Sekunden
    Chronik weg, und das ist der bewusst in Kauf genommene Preis dafür, dass
    kein Aufrufer je wartet.
    """
    ende = time.monotonic() + timeout
    while not _SCHLANGE.empty() and time.monotonic() < ende:
        time.sleep(0.05)
    return _SCHLANGE.empty()
