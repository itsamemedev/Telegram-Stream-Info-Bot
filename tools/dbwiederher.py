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
import sqlite3
import tarfile
import tempfile

OK, NICHT_BRAUCHBAR, NICHT_LESBAR = 0, 1, 2

# Vokabular, das nur ein `.iterdump()`-Dump hat. `CREATE TABLE` allein taugt
# NICHT als Erkennungsmerkmal — es steht auch in jeder SQLite-Datei, weil das
# Schema woertlich in sqlite_master liegt (W94).
DUMP_MARKEN = ("BEGIN TRANSACTION", "CREATE TABLE", "INSERT INTO")


def dump_aus_archiv(pfad: str, ziel_verz: str):
    """Holt db/tiktok_bot_*.sql aus einem nightcrawler_sys_*.tar.gz.
       -> Pfad der ausgepackten .sql, oder None."""
    with tarfile.open(pfad, "r:gz") as tar:
        # Positiv auswaehlen, nicht negativ filtern. `_system_backup()` legt
        # den Dump als `db/tiktok_bot_<stempel>.sql` ab, daneben liegt
        # `db/brain_<stempel>.sql`. Ein Filter "alles ausser brain" sah
        # richtig aus und war es nur durch Zufall: sortiert steht `brain` vor
        # `tiktok_bot`, also haette der Zugriff auf das letzte Element ohnehin
        # das Richtige erwischt — bis eine dritte Datei dazukommt, die
        # alphabetisch dahinter liegt. Die Mutationsprobe hat genau das
        # aufgedeckt: den Filter zu entfernen aenderte nichts.
        kandidaten = [m for m in tar.getmembers()
                      if m.isfile() and m.name.startswith("db/")
                      and m.name.endswith(".sql")
                      and os.path.basename(m.name).startswith("tiktok_bot_")]
        if not kandidaten:
            return None
        # Bei mehreren: der juengste Stempel steht im Namen, also der groesste.
        m = sorted(kandidaten, key=lambda x: x.name)[-1]
        # Bewusst einzeln und mit flachem Namen: ein Archiv mit "../" im Pfad
        # duerfte sonst ausserhalb des Zielverzeichnisses schreiben.
        quelle = tar.extractfile(m)
        if quelle is None:
            return None
        ziel = os.path.join(ziel_verz, os.path.basename(m.name))
        with open(ziel, "wb") as f:
            f.write(quelle.read())
        return ziel


def einspielen(sql_pfad: str, ziel_db: str):
    """Baut aus dem Dump eine NEUE Datenbank. -> (ok, befund, tabellen)"""
    with open(sql_pfad, encoding="utf-8", errors="replace") as f:
        sql = f.read()
    fehlend = [m for m in DUMP_MARKEN if m not in sql]
    if fehlend:
        return False, ("Das sieht nicht nach einem Systemarchiv-Dump aus "
                       "(es fehlt: %s)." % ", ".join(fehlend)), []
    con = sqlite3.connect(ziel_db)
    try:
        con.executescript(sql)
        con.commit()
        # Der Vollstaendigkeit halber, nicht als Sicherung: eine Datenbank,
        # die SQLite gerade selbst aus SQL gebaut hat, ist strukturell heil —
        # die Mutationsprobe hat bestaetigt, dass dieser Zweig mit einem
        # gueltigen Dump nicht erreichbar ist. Was hier WIRKLICH traegt, ist
        # executescript(): ein kaputter Dump faellt dort. Der Befund wandert
        # trotzdem in die Ausgabe, damit der Betreiber ihn sieht, statt ihm
        # vertrauen zu muessen.
        befund = con.execute("PRAGMA integrity_check").fetchone()[0]
        if befund != "ok":
            return False, str(befund).splitlines()[0], []
        tabellen = []
        for (name,) in con.execute(
                "SELECT name FROM sqlite_master WHERE type='table' "
                "AND name NOT LIKE 'sqlite_%' ORDER BY name").fetchall():
            n = con.execute('SELECT count(*) FROM "%s"' % name).fetchone()[0]
            tabellen.append((name, n))
        return True, "ok", tabellen
    except sqlite3.DatabaseError as e:
        return False, str(e), []
    finally:
        con.close()


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

    with tempfile.TemporaryDirectory(prefix="dbwh-") as tmp:
        sql = a.quelle
        if a.quelle.endswith((".tar.gz", ".tgz")):
            print("Archiv:  %s" % a.quelle)
            try:
                sql = dump_aus_archiv(a.quelle, tmp)
            except (tarfile.TarError, OSError) as e:
                print("Das Archiv ist nicht zu lesen: %s" % e)
                return NICHT_LESBAR
            if not sql:
                print("Im Archiv liegt kein db/tiktok_bot_*.sql.")
                print("Nachsehen, was drin ist:  tar -tzf %s | head" % a.quelle)
                return NICHT_BRAUCHBAR
        print("Dump:    %s (%d Bytes)" % (os.path.basename(sql),
                                          os.path.getsize(sql)))

        ok, befund, tabellen = einspielen(sql, a.ziel)

    if not ok:
        print("\nNICHT eingespielt: %s" % befund)
        # Die halb gebaute Datei ist wertlos und wuerde beim naechsten Lauf
        # als "gibt es schon" im Weg stehen.
        try:
            os.remove(a.ziel)
        except OSError:
            pass                       # Aufraeumpfad, Fehlschlag folgenlos
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
