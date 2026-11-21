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


# ── v5.11.4 (OPS-2): mysqldump ohne Passwort in der Zeile ───────────────────
# Bis dahin lief `mysqldump … -p<Passwort>`. Das Passwort stand damit fuer
# jeden Nutzer des Rechners in `ps`, und scheiterte der Dump, trug
# str(CalledProcessError) die ganze argv — samt Passwort — in
# _SYS_BACKUP_STATE["error"], also nach /api/backup/status im Deck, ins
# error.log und in den Discord-Fehlerkanal. Dazu fehlte `-P`: ein MariaDB auf
# einem anderen Port als 3306 scheiterte bei JEDER Sicherung.
#
# MYSQL_PWD statt --defaults-extra-file: der Wert geht unveraendert durch,
# ohne die Quoting-Regeln der Optionsdatei (ein `"` oder `\` im Passwort
# waere dort ein Fehlerbild fuer sich), und es bleibt keine Datei liegen.
# /proc/<pid>/environ liest nur derselbe Nutzer oder root — argv jeder.

class DumpFehler(RuntimeError):
    """mysqldump scheiterte. Die Meldung traegt Exitcode und geschwaerztes
    stderr, nie die Kommandozeile."""


def schwaerzen(text, geheim):
    """Ersetzt `geheim` in `text` durch *** — fuer jede Meldung, die nach
    aussen geht. Ein leeres Geheimnis schwaerzt nichts (sonst stuende
    zwischen jedem Zeichen ein ***)."""
    t = str(text if text is not None else "")
    return t.replace(geheim, "***") if geheim else t


def mysqldump(programm, ziel, db, host, port, user, passwort, timeout=600, lauf=None):
    """Schreibt den Dump von `db` in die offene Datei `ziel`. Wirft DumpFehler
    mit einer Meldung, die nach aussen darf. `lauf` ist fuer Vertraege."""
    import subprocess
    lauf = lauf or subprocess.run
    argv = [programm, "-h", str(host), "-P", str(int(port)), "-u", str(user), str(db)]
    env = dict(os.environ)
    env.pop("MYSQL_PWD", None)      # kein geerbtes Passwort eines anderen Kontos
    if passwort:
        env["MYSQL_PWD"] = passwort
    try:
        r = lauf(argv, stdout=ziel, stderr=subprocess.PIPE, env=env, timeout=timeout)
    except subprocess.TimeoutExpired:
        # str(TimeoutExpired) nennt die argv; `from None`, damit auch der
        # Traceback sie nicht mitschleppt.
        raise DumpFehler("mysqldump nach %d s abgebrochen (Zeitlimit)" % timeout) from None
    if r.returncode != 0:
        roh = r.stderr or b""
        if isinstance(roh, bytes):
            roh = roh.decode("utf-8", "replace")
        # stderr nennt bei 1045 nur „using password: YES" — geschwaerzt wird
        # trotzdem, weil hier niemand garantiert, was ein Client ausgibt.
        text = schwaerzen(roh.strip(), passwort)[-300:] or "keine Meldung auf stderr"
        raise DumpFehler("mysqldump endete mit Exitcode %d: %s" % (r.returncode, text))
