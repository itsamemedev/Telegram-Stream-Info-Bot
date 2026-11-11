"""nc.dbwartung — v4.2-W176: wann ist das woechentliche VACUUM faellig?

`_db_vacuum_loop` schlief vor dem ERSTEN Lauf sieben Tage. Der Dienst wird
bei jedem Update neu gestartet (nc/laufstand.py meldet, wenn nicht), und ein
Neustart setzte die Uhr wieder auf null — das VACUUM lief damit praktisch
nie. Dazu startete die Schleife nur mit DAILY_SUMMARY_CHAT_ID, obwohl sie
keinen Chat braucht. Ohne VACUUM waechst die Datei nach Monaten von Inserts
und Deletes unbegrenzt, und das sieht man erst an der Platte.

Jetzt steht der letzte Lauf in einer kleinen Datei neben der Datenbank, und
die Schleife fragt nach Faelligkeit statt nach Laufzeit. Die Datei liegt
bewusst NICHT in der Datenbank: VACUUM ist reine SQLite-Wartung, und eine
eigene Tabelle dafuer muesste unter MariaDB mitgefuehrt werden, wo sie nie
gelesen wird.

Bot-frei und ohne Uhr im Inneren — `jetzt` kommt herein, damit der Vertrag
eine Woche ohne Warten pruefen kann.
"""
from __future__ import annotations

import json
import logging
import os

log = logging.getLogger("TikTokBot")

ABSTAND_S = 7 * 24 * 3600
DATEINAME = ".db_wartung.json"


def stand_datei(db_path: str) -> str:
    """Neben der Datenbank, nicht im Arbeitsverzeichnis: wer DB_PATH auf
    eine andere Platte legt, will dort auch ihren Zustand haben."""
    return os.path.join(os.path.dirname(os.path.abspath(db_path)), DATEINAME)


def letzter_lauf(pfad: str):
    """-> Zeitstempel (time.time()) des letzten gelungenen Laufs, oder None.

    None heisst „unbekannt" und damit „faellig". Eine unlesbare Datei wird
    gemeldet und genauso behandelt — ein VACUUM zu viel kostet eine Minute,
    eines zu wenig waechst unbemerkt."""
    wert = None
    if os.path.exists(pfad):
        try:
            with open(pfad, encoding="utf-8") as f:
                wert = float(json.load(f)["letzter"])
        except (OSError, ValueError, KeyError, TypeError) as e:
            log.warning("DB-Wartung: Stand %s unlesbar (%s) — gilt als faellig.", pfad, e)
    return wert


def faellig_in(letzter, jetzt: float, abstand_s: float = ABSTAND_S) -> float:
    """Sekunden bis zum naechsten Lauf; 0 = jetzt faellig."""
    # Ein Ausdruck statt `return 0.0` im eigenen Zweig: die 0 ist hier kein
    # Misserfolg, sondern „jetzt faellig" (dieselbe Abwaegung wie in
    # nc/schemastand.lies fuer tools/blindstellen.py).
    return (0.0 if letzter is None
            else max(0.0, float(letzter) + abstand_s - float(jetzt)))


def merken(pfad: str, jetzt: float) -> None:
    """Atomar schreiben — ein halb geschriebener Stand waere beim naechsten
    Lesen unlesbar und loeste ein unnoetiges VACUUM aus."""
    tmp = pfad + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump({"letzter": float(jetzt)}, f)
    os.replace(tmp, pfad)
