#!/usr/bin/env python3
"""tools/dbkopf.py — v4.2-W94: eine SQLite-Datei retten, deren Kopf zerstoert ist.

════════════════════════════════════════════════════════════════════════
DER ANLASS
════════════════════════════════════════════════════════════════════════
Am 18.09. lag statt der Datenbank dies im Arbeitsverzeichnis:

    Datei: /home/ubuntu/tiktok-bot/tiktok_bot.db
    Groesse: 401408 Bytes (0.4 MB)
    Erste Bytes: 17 03 03 00 2d 0c fc ba 34 d6 d6 33 52 fb 55 0a
    Das ist am Anfang wie ein TLS-Record (Application Data).

W92 hat den Start korrekt abgebrochen und korrekt gewarnt, die Datei nicht
zu loeschen. Nur half die Diagnose dann nicht weiter: sie sagte
"STRUKTURIERTE Daten, aufgeben waere verfrueht" — und nannte keinen Weg.
Das ist derselbe Fehler wie ein blankes "HTTP 403", eine Ebene tiefer:
richtig und nutzlos.

Die entscheidende Zahl stand im Log und wurde von niemandem gelesen:
**401408 = 4096 x 98**, also exakt 98 SQLite-Seiten. Die Datei wurde nicht
ERSETZT, sondern nur am ANFANG ueberschrieben — der TLS-Record ist 5 Bytes
Kopf plus 0x2d = 45 Bytes Nutzlast, zusammen 50 Bytes. Kaputt ist damit der
100-Byte-Dateikopf; die 98 Seiten dahinter sind unberuehrt.

Genau dafuer ist dieses Werkzeug da.

════════════════════════════════════════════════════════════════════════
WARUM BRUTE FORCE UND NICHT RECHNEN
════════════════════════════════════════════════════════════════════════
Im zerstoerten Kopf steht auch die Seitengroesse (Byte 16-17) und die
Seitenzahl (Byte 28-31). Beides ist weg, beides braucht SQLite.

Die Seitenzahl folgt aus Dateigroesse / Seitengroesse. Die Seitengroesse
selbst ist nicht zu berechnen — sie ist eine von acht erlaubten Zweierpotenzen
(512 bis 65536). Also werden alle acht durchprobiert.

Geraten wird dabei nichts: **`PRAGMA integrity_check` entscheidet.** Nur die
richtige Seitengroesse liefert exakt "ok". Eine falsche liefert entweder
einen Fehler oder einen Bericht voller "Page N: never used" — gemessen: bei
8192 statt 4096 kamen 308 von 2000 Zeilen heraus, und integrity_check meldete
die Fragmentierung. Waere "keine Ausnahme" das Kriterium, haette das Werkzeug
diese Datei als gerettet ausgegeben und 85 % der Daten still verloren. Das
Kriterium ist deshalb die wortgleiche Antwort "ok" und nichts sonst.

════════════════════════════════════════════════════════════════════════
WAS ES NICHT TUT
════════════════════════════════════════════════════════════════════════
Es schreibt **nie** in die Eingabedatei. Sie wird ausschliesslich mit "rb"
geoeffnet. Das Ergebnis geht in eine neue Datei, und die muss der Betreiber
selbst benennen — W91 hat gezeigt, wohin ein Werkzeug fuehrt, das im
Zweifelsfall selbst entscheidet, was weg darf.

Es ersetzt auch **keine Sicherung**. Der tagesaktuelle SQL-Dump aus dem
Systemarchiv ist der bessere Weg, wenn er vorhanden und aktuell ist; dieses
Werkzeug ist fuer den Fall, dass er fehlt oder aelter ist als die Arbeit
eines ganzen Tages.
"""
from __future__ import annotations

import argparse
import os
import sqlite3
import tempfile

# Die acht von SQLite erlaubten Seitengroessen. Absteigend nicht noetig —
# integrity_check trennt sie sauber, die Reihenfolge ist nur Kosmetik.
SEITENGROESSEN = (512, 1024, 2048, 4096, 8192, 16384, 32768, 65536)

MAGIE = b"SQLite format 3\x00"

# Exitcodes, getrennt wie bei den Sperren aus W83: 1 heisst "nicht zu retten",
# 2 heisst "ich konnte nicht nachsehen". Beides als 1 zu melden waere genau
# die Vermischung, die dort schon einmal einen Fortschritt vorgetaeuscht hat.
OK, NICHT_ZU_RETTEN, NICHT_LESBAR = 0, 1, 2


def kopf_bauen(roh: bytes, seitengroesse: int) -> bytes:
    """Die ersten 100 Bytes neu setzen. -> vollstaendiger Dateiinhalt

    Nur der Kopf wird ersetzt; ab Byte 100 bleibt alles, wie es ist. Die
    Werte sind die, die SQLite selbst fuer eine gewoehnliche Datei schreibt —
    kein Raten, sondern das dokumentierte Format.
    """
    aus = bytearray(roh)
    seiten = len(roh) // seitengroesse
    aus[0:16] = MAGIE
    aus[16:18] = seitengroesse.to_bytes(2, "big")
    aus[18:20] = bytes([1, 1])           # Schreib-/Leseformat: Journal (nicht WAL)
    aus[20:21] = bytes([0])              # reservierter Platz am Seitenende
    aus[21:24] = bytes([64, 32, 32])     # Nutzlast-Grenzen, in SQLite fest
    aus[24:28] = (1).to_bytes(4, "big")  # Aenderungszaehler
    aus[28:32] = seiten.to_bytes(4, "big")
    aus[32:40] = bytes(8)                # Freiliste: leer annehmen
    aus[40:44] = (1).to_bytes(4, "big")  # Schema-Zaehler
    aus[44:48] = (4).to_bytes(4, "big")  # Schemaformat 4
    aus[48:52] = bytes(4)                # Standard-Cache
    # Byte 92-95 ("version-valid-for") auf 0. SQLite glaubt die Seitenzahl aus
    # Byte 28-31 nur, wenn dieses Feld zum Aenderungszaehler passt, und nimmt
    # sonst die Dateigroesse.
    #
    # EHRLICH GESAGT traegt die Zeile nichts: die Seitenzahl oben ist bereits
    # richtig gerechnet, also stimmen beide Wege ueberein. Die Mutationsprobe
    # hat das nachgewiesen — sie zu entfernen aendert nichts, und kein
    # Vertrag kann das fangen. Sie bleibt trotzdem, weil sie den zweiten Weg
    # FESTLEGT statt ihn dem Restmuell in der kaputten Datei zu ueberlassen;
    # sie als "das ist der Mechanismus" zu kommentieren waere aber genau die
    # Sorte Behauptung, die dieses Projekt sich abgewoehnt hat.
    aus[92:96] = bytes(4)
    return bytes(aus)


def _pruefe(inhalt: bytes, arbeitsverzeichnis: str):
    """Ergibt dieser Inhalt eine HEILE Datenbank? -> (ok, befund, tabellen)

    `ok` ist nur dann wahr, wenn integrity_check woertlich "ok" sagt. Siehe
    Kopfkommentar: "keine Ausnahme" als Kriterium haette eine halb gelesene
    Datei als Rettung ausgegeben.
    """
    pfad = os.path.join(arbeitsverzeichnis, "probe.db")
    with open(pfad, "wb") as f:
        f.write(inhalt)
    try:
        con = sqlite3.connect(pfad)
    except sqlite3.DatabaseError as e:
        return False, str(e), []
    try:
        try:
            befund = con.execute("PRAGMA integrity_check").fetchone()[0]
        except sqlite3.DatabaseError as e:
            return False, str(e), []
        if befund != "ok":
            return False, str(befund).splitlines()[0], []
        tabellen = []
        for (name,) in con.execute(
                "SELECT name FROM sqlite_master WHERE type='table' "
                "AND name NOT LIKE 'sqlite_%' ORDER BY name").fetchall():
            try:
                n = con.execute('SELECT count(*) FROM "%s"' % name).fetchone()[0]
            except sqlite3.DatabaseError as e:
                # Eine einzelne unlesbare Tabelle macht den Fund nicht
                # wertlos — sie gehoert aber genannt, nicht verschwiegen.
                n = "unlesbar (%s)" % e
            tabellen.append((name, n))
        return True, "ok", tabellen
    finally:
        con.close()
        try:
            os.remove(pfad)
        except OSError:
            pass                          # Aufraeumpfad, Fehlschlag folgenlos


def rette(pfad: str):
    """Die Seitengroesse finden, bei der die Datei heil ist.
       -> (seitengroesse, inhalt, tabellen) oder (None, None, [])"""
    with open(pfad, "rb") as f:
        roh = f.read()
    if len(roh) < 512:
        return None, None, []
    with tempfile.TemporaryDirectory(prefix="dbkopf-") as tmp:
        for sg in SEITENGROESSEN:
            # Eine Datei, deren Groesse kein Vielfaches der Seitengroesse
            # ist, kann diese Seitengroesse nicht haben. Das ist ein billiger
            # Vorfilter, KEINE Sicherung: die Entscheidung faellt unten an
            # integrity_check, und die Mutationsprobe hat bestaetigt, dass
            # das Weglassen dieser Zeile am Ergebnis nichts aendert. Sie
            # bleibt, weil sie sieben nutzlose Schreibvorgaenge je Durchlauf
            # spart — auf einer 108-MB-Datei ist das der Unterschied zwischen
            # Sekunden und Minuten.
            if len(roh) % sg:
                continue
            inhalt = kopf_bauen(roh, sg)
            ok, _befund, tabellen = _pruefe(inhalt, tmp)
            if ok:
                return sg, inhalt, tabellen
    return None, None, []


def main() -> int:
    p = argparse.ArgumentParser(
        description="Rettet eine SQLite-Datei, deren 100-Byte-Kopf "
                    "ueberschrieben wurde. Die Eingabedatei wird nie "
                    "veraendert.")
    p.add_argument("datei", help="die beschaedigte Datenbankdatei")
    p.add_argument("-o", "--ziel", help="wohin die Rettung geschrieben wird "
                                        "(ohne dies wird nur geprueft)")
    a = p.parse_args()

    if not os.path.isfile(a.datei):
        print("dbkopf: %s gibt es nicht." % a.datei)
        return NICHT_LESBAR
    try:
        groesse = os.path.getsize(a.datei)
        with open(a.datei, "rb") as f:
            erste = f.read(16)
    except OSError as e:
        print("dbkopf: %s ist nicht zu lesen: %s" % (a.datei, e))
        return NICHT_LESBAR

    print("Datei:   %s (%d Bytes)" % (a.datei, groesse))
    print("Anfang:  %s" % " ".join("%02x" % b for b in erste))
    if erste.startswith(MAGIE):
        print("\nDer Kopf ist INTAKT — diese Datei hat einen anderen Schaden.")
        print("Dieses Werkzeug hilft nur bei zerstoertem Kopf; hier ist")
        print("  sqlite3 %s '.recover' > gerettet.sql" % os.path.basename(a.datei))
        print("der richtige Weg.")
        return NICHT_ZU_RETTEN

    passend = [sg for sg in SEITENGROESSEN if groesse % sg == 0]
    print("Seitenraster: %s" % (", ".join(str(s) for s in passend) or "keines"))
    if not passend:
        print("\nDie Groesse ist durch keine erlaubte Seitengroesse teilbar.")
        print("Damit ist die Datei keine (angeschnittene) SQLite-Datenbank —")
        print("sie wurde ersetzt, nicht nur am Anfang ueberschrieben.")
        return NICHT_ZU_RETTEN

    sg, inhalt, tabellen = rette(a.datei)
    if sg is None:
        print("\nKeine Seitengroesse ergibt eine heile Datenbank.")
        print("Die Daten dahinter sind entweder auch beschaedigt oder es war")
        print("nie eine SQLite-Datei. Naechster Weg: der SQL-Dump aus dem")
        print("Systemarchiv (LOCAL_BACKUP_DIR/system bzw. S3 unter system/).")
        return NICHT_ZU_RETTEN

    print("\nGERETTET mit Seitengroesse %d (%d Seiten), integrity_check: ok"
          % (sg, len(inhalt) // sg))
    for name, n in tabellen:
        print("   %-28s %s" % (name, n))
    if not a.ziel:
        print("\nNur geprueft. Zum Schreiben:")
        print("   python3 tools/dbkopf.py %s -o gerettet.db" % a.datei)
        return OK
    if os.path.exists(a.ziel):
        # Nicht ueberschreiben: das Ziel koennte die Sicherung sein, aus der
        # gerade wiederhergestellt wurde. W91 ist genau daran entlanggelaufen.
        print("\n%s gibt es schon — ich ueberschreibe nichts." % a.ziel)
        return NICHT_LESBAR
    with open(a.ziel, "wb") as f:
        f.write(inhalt)
    print("\nGeschrieben: %s" % a.ziel)
    print("Pruefen und erst DANN einsetzen:")
    print("   sqlite3 %s 'PRAGMA integrity_check; SELECT count(*) FROM trackings;'"
          % a.ziel)
    return OK


if __name__ == "__main__":
    raise SystemExit(main())
