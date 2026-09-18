#!/usr/bin/env python3
"""tools/dbwiederher.py — v4.2-W95: die Datenbank aus einem Systemarchiv zurueckholen.

════════════════════════════════════════════════════════════════════════
DER ANLASS
════════════════════════════════════════════════════════════════════════
Der Betreiber am 18.09., nachdem die Datenbank ueberschrieben war:

    "Über die Backup Funktion im dashboard lassen sich keine SQL Dateien
     importieren da sämtliche Tabellen schon existieren."

Das stimmt, und es sind ZWEI Formate, die niemand gegeneinander gehalten
hat:

  nc/dbexport.py        Kopfzeile `-- NIGHTCRAWLER-DB-EXPORT`, **nur Daten**.
  (Deck: Export/Import) Gebaut fuer den Umzug SQLite <-> MariaDB; das Schema
                        legt das Ziel selbst an. Steht so im Modulkopf.

  _system_backup()      `sqlite3 .iterdump()`, also **Schema UND Daten**,
  (Archiv, taeglich 04:00) beginnend mit BEGIN TRANSACTION; CREATE TABLE ...

Die Sicherung schreibt also genau das Format, das der Importer nicht lesen
kann. Nachgestellt ergab das:

    ok: False | Statements: 9 | angewandt: 7
      CREATE TABLE recordings ...: table recordings already exists

Die CREATE fallen, **die INSERT laufen durch**. Der Import bricht nicht ab,
er spielt TEILWEISE ein und mischt alte Zeilen in den laufenden Bestand.
Auf einer gesunden Datenbank waere das ein Datenschaden.

════════════════════════════════════════════════════════════════════════
WARUM EIN EIGENES WERKZEUG UND NICHT "DEN IMPORTER REPARIEREN"
════════════════════════════════════════════════════════════════════════
Zwei Gruende, und beide sind Lage, nicht Geschmack:

  * **Das Deck laeuft nicht.** Ist die Datenbank unlesbar, bricht der Start
    mit Exitcode 3 ab (W92) — es gibt kein Dashboard, in das man etwas
    hochladen koennte. Ein Wiederherstellungsweg, der den laufenden Bot
    voraussetzt, ist genau dann weg, wenn man ihn braucht.
  * **In eine belegte Datenbank laesst sich das nicht sauber einspielen.**
    Der Bot haelt die Datei offen, die Tabellen stehen, und ein Dump mit
    Schema gehoert in eine LEERE Datei. Alles andere ist Mischen.

Deshalb: neu bauen, pruefen, und der Betreiber tauscht selbst. Dieses
Werkzeug entscheidet nie, was weg darf — W91 hat gezeigt, wohin das fuehrt.
"""
from __future__ import annotations

import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# v4.2-W96: EINE Implementierung, nicht zwei. Bis hierher stand der Kern
# doppelt — hier und (neu) hinter den Deck-Routen. Zwei Fassungen derselben
# Rettung sind genau die Lage, in der eine davon die WAL-Falle kennt und die
# andere nicht. nc/ ist bot-frei, also laesst sich das Modul auch hier
# benutzen, ohne den Bot zu ziehen.
from nc import dbrestore as _rest        # noqa: E402

OK, NICHT_BRAUCHBAR, NICHT_LESBAR = 0, 1, 2


def main() -> int:
    p = argparse.ArgumentParser(
        description="Baut aus einem Systemarchiv (oder einem SQL-Dump) eine "
                    "neue Datenbankdatei. Die laufende Datenbank wird nie "
                    "angefasst.")
    p.add_argument("quelle", help="nightcrawler_sys_*.tar.gz oder *.sql")
    p.add_argument("-o", "--ziel", default="wiederhergestellt.db",
                   help="die neue Datei (Vorgabe: wiederhergestellt.db)")
    a = p.parse_args()

    if not os.path.isfile(a.quelle):
        print("dbwiederher: %s gibt es nicht." % a.quelle)
        return NICHT_LESBAR
    if os.path.exists(a.ziel):
        # Niemals ueberschreiben: das Ziel koennte die laufende Datenbank oder
        # ein frueherer Rettungsversuch sein.
        print("dbwiederher: %s gibt es schon — ich ueberschreibe nichts."
              % a.ziel)
        print("Waehle einen anderen Namen mit -o.")
        return NICHT_LESBAR

    if a.quelle.endswith((".tar.gz", ".tgz")):
        print("Archiv:  %s" % a.quelle)
    ok, befund, tabellen = _rest.vorbereiten(a.quelle, a.ziel)
    if not ok:
        print("\nNICHT eingespielt: %s" % befund)
        return NICHT_BRAUCHBAR

    gesamt = sum(n for _n, n in tabellen)
    print("\nEINGESPIELT: %s — %d Tabellen, %d Zeilen, integrity_check: ok"
          % (a.ziel, len(tabellen), gesamt))
    for name, n in sorted(tabellen, key=lambda x: -x[1])[:15]:
        if n:
            print("   %-28s %d" % (name, n))
    leer = [n for n, c in tabellen if not c]
    if leer:
        print("   (%d Tabellen leer: %s%s)"
              % (len(leer), ", ".join(leer[:6]),
                 " …" if len(leer) > 6 else ""))
    print("\nErst die Zahlen pruefen. Sehen sie plausibel aus, dann tauschen:")
    print("   sudo systemctl stop tiktok-bot")
    print("   mv tiktok_bot.db tiktok_bot.db.kaputt")
    print("   cp %s tiktok_bot.db" % a.ziel)
    print("   sudo systemctl start tiktok-bot")
    return OK


if __name__ == "__main__":
    raise SystemExit(main())
