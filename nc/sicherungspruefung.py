"""nc.sicherungspruefung — ist die Sicherung, die gerade entstand, brauchbar? (rein)

v4.2-W142. `_system_backup()` meldete `ok: True`, sobald ein Archiv auf der
Platte lag. Was darin stand, prueft niemand — und zwei Faelle lieferten damit
eine Sicherung, die beim Wiederherstellen nichts enthaelt:

  * ohne `mysqldump` schrieb der Bot eine Platzhalterzeile
    („mysqldump nicht installiert — kein Dump möglich") an die Stelle des
    Dumps und packte DIE ein. Die Sicherung meldete Erfolg, ohne Datenbank.
  * ein abgebrochener Dump (Platte voll, Prozess beendet) endet mitten in
    einer INSERT-Zeile. `sqlite3 neu.db < dump.sql` laeuft dann bis zur
    Bruchstelle und hoert auf — eine halbe Datenbank, ohne Fehlermeldung
    beim Sichern.

Eine Sicherung, die beim Wiederherstellen nichts taugt, faellt genau dann
auf, wenn man sie braucht (dieselbe Lage wie W92: der Rettungsweg fehlt im
Ernstfall). Geprueft wird deshalb jetzt beim Sichern, nicht beim Einspielen.

Bewusst KEIN Probe-Import: ein `executescript` des ganzen Dumps kostet bei
einer Datenbank im Gigabyte-Bereich so viel Speicher und Zeit wie der Bot
selbst. Der Abschluss-Marker ist der billige, sichere Teil — iterdump()
schreibt `COMMIT;` als letzte Zeile, mysqldump `-- Dump completed`.
"""

import logging
import os
import tarfile

log = logging.getLogger("TikTokBot")

ENDE_MARKER = {"sqlite": "COMMIT;", "mariadb": "-- Dump completed"}
_SCHWANZ = 4096


def dump_vollstaendig(pfad, backend="sqlite"):
    """(ok, grund). Liest nur das Ende der Datei."""
    marker = ENDE_MARKER["mariadb" if backend == "mariadb" else "sqlite"]
    grund = ""
    if not pfad or not os.path.isfile(pfad):
        grund = "Dump fehlt"
    elif os.path.getsize(pfad) == 0:
        grund = "Dump ist leer"
    else:
        with open(pfad, "rb") as fh:
            fh.seek(max(0, os.path.getsize(pfad) - _SCHWANZ))
            schwanz = fh.read().decode("utf-8", "ignore")
        if marker not in schwanz:
            erste = schwanz.strip().splitlines()[-1][:120] if schwanz.strip() else ""
            grund = ("Dump endet ohne %r — abgebrochen oder Platzhalter (letzte Zeile: %r)"
                     % (marker, erste))
    return (not grund), grund


def archiv_lesbar(pfad):
    """(ok, grund, eintraege). Oeffnet das Archiv neu und liest das Verzeichnis
    — ein beim Schreiben abgeschnittenes tar.gz scheitert genau hier."""
    try:
        with tarfile.open(pfad, "r:gz") as tar:
            namen = tar.getnames()
    except (OSError, tarfile.TarError, EOFError) as e:
        # Der Aufrufer meldet das Gesamturteil auf error; die Zeile hier
        # nennt die Datei, falls die Pruefung woanders verwendet wird.
        log.warning("Sicherung %s nicht lesbar: %s: %s", pfad, type(e).__name__, e)
        return False, "Archiv nicht lesbar: %s: %s" % (type(e).__name__, e), 0
    if not any(n.startswith("db/") for n in namen):
        return False, "Archiv enthält keinen Datenbank-Dump (db/…)", len(namen)
    return True, "", len(namen)


def pruefen(archiv, dump, backend="sqlite"):
    """{"ok": bool, "gruende": [...], "eintraege": n} — alle Befunde, nicht nur der erste."""
    gruende = []
    ok_d, g = dump_vollstaendig(dump, backend)
    if not ok_d:
        gruende.append(g)
    ok_a, g, n = archiv_lesbar(archiv)
    if not ok_a:
        gruende.append(g)
    return {"ok": not gruende, "gruende": gruende, "eintraege": n}
