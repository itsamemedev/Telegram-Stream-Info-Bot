"""nc.mariadbumzug — eine bestehende SQLite-Datenbank nach MariaDB umziehen (v4.2-W143).

Der Betreiber am 05.11.: „wenn die Datenbank auf sqlite steht diese in Mariadb
integrieren soll und dann nur noch über Mariadb laufen soll dazu muss das in
der env geändert werden."

**Der Befund, gegen den dieses Modul gebaut ist.** Der Installer kann MariaDB
einrichten — Server, Datenbank, Nutzer — und setzt danach `DB_BACKEND=mariadb`
in die `.env`. Die DATEN zieht er nicht um. Wer eine laufende SQLite-
Installation erneut durch den Installer schickt und MariaDB waehlt, startet den
Bot gegen eine leere Datenbank: Trackings, Aufnahme-Eintraege, Ledger,
Community — alles scheinbar weg, ohne eine einzige Fehlermeldung, weil eine
leere Datenbank kein Fehler ist. Dazu verwies `bot.init_db()` seit Jahren auf
ein `sqlite2mariadb.py`, das es nie gab.

**Der Weg.** Die Bausteine gab es schon, sie waren nur nie verbunden:
`nc/dbexport.py` exportiert NUR Daten (dialektrichtig escaped, siehe dort zum
Backslash), `nc/schema.anlegen()` baut das Schema im Zieldialekt. Hier kommt
dazu, was ein Umzug gegen Produktion braucht:

  1. Vorher pruefen, und bei jedem Zweifel abbrechen, BEVOR geschrieben wird:
     Quelle lesbar und `integrity_check` = ok, Ziel erreichbar und LEER, der
     Bot schreibt nicht mehr in die Quelle.
  2. Nachher zaehlen: jede Tabelle im Ziel muss genau so viele Zeilen haben
     wie in der Quelle. Ein Import, der „ok" sagt und Zeilen verloren hat, ist
     die Lage aus W95 („angewandt: 7 von 9"), eine Ebene weiter.
  3. Erst dann die `.env` umstellen — mit Sicherungskopie. Die SQLite-Datei
     wird nie angefasst: der Rueckweg ist `DB_BACKEND=sqlite`.

Kein Logger-Aufruf ohne Grund, kein Netz ausser der MariaDB-Verbindung, kein
Import aus bot.py.
"""

import logging
import os
import sqlite3
import time

from nc import dbexport as _dbexport
from nc import envdatei as _envdatei
from nc import dbwrap as _dbwrap
from nc import schema as _schema
from nc import schemastand as _schemastand

log = logging.getLogger("TikTokBot")

# Wie frisch eine Aenderung an der SQLite-Datei sein darf, bevor wir annehmen,
# dass der Bot noch hineinschreibt. Der Bot schreibt alle paar Sekunden
# (Pruefschleife, Lagezeilen, Heartbeat); 30 s Ruhe heisst „gestoppt".
RUHE_S = 30

# Schluessel, die der Umzug in der .env setzt — in dieser Reihenfolge.
ENV_SCHLUESSEL = ("DB_BACKEND", "MARIADB_HOST", "MARIADB_PORT", "MARIADB_DB",
                  "MARIADB_USER", "MARIADB_PASSWORD")


class UmzugAbgebrochen(Exception):
    """Ein Grund, nicht weiterzumachen — mit Abhilfe im Text."""


# ── Pruefungen ───────────────────────────────────────────────────────────────

def geoeffnet_von(sqlite_pfad, proc="/proc"):
    """PIDs anderer Prozesse, die die Datei oder ihr WAL offen halten — oder
    None, wenn das System es nicht verraet (kein /proc, z. B. macOS).

    Die ehrliche Frage ist „schreibt der Bot noch?", und die beantwortet nur
    ein offenes Handle. Die Aenderungszeit taugt dafuer nicht: beim sauberen
    Stopp schreibt SQLite die Datei beim Schliessen noch einmal (Checkpoint),
    und eine Zeitregel verweigerte den Umzug genau dann, wenn er sicher ist —
    gemessen beim Bau dieses Moduls."""
    if not os.path.isdir(proc):
        log.info("Kein %s — ob der Bot die Datenbank offen haelt, entscheidet die "
                 "Aenderungszeit (%d s Ruhe).", proc, RUHE_S)
        return None
    ziele = {os.path.realpath(p) for p in (sqlite_pfad, sqlite_pfad + "-wal")}
    eigene = str(os.getpid())
    pids, unlesbar = [], 0
    for pid in os.listdir(proc):
        if not pid.isdigit() or pid == eigene:
            continue
        try:
            links = _fd_ziele(os.path.join(proc, pid, "fd"))
        except OSError as e:
            # PermissionError: fremder Nutzer oder ptrace-Sperre — im
            # Container darf selbst root /proc/1/fd auflisten, aber kein
            # Handle darin lesen (gemessen beim Bau; os.access sagt dort ja).
            # FileNotFoundError: der Prozess endete — er haelt nichts mehr.
            if isinstance(e, PermissionError):
                unlesbar += 1
            log.debug("Handles von PID %s nicht lesbar: %s", pid, e)
            continue
        if ziele.intersection(links):
            pids.append(int(pid))
    # Ohne Leserecht auf fremde Prozesse hiesse „keiner gefunden" nur „keiner,
    # den ich sehen darf" — und der Umzug liefe, waehrend der Bot schreibt.
    if not pids and unlesbar:
        log.info("%d Prozesse ohne Leserecht auf ihre Handles — ob der Bot die "
                 "Datenbank offen haelt, entscheidet die Aenderungszeit (%d s Ruhe). "
                 "Als root ausgefuehrt waere die Antwort sicher.", unlesbar, RUHE_S)
        return None
    return pids


def _fd_ziele(fd_dir):
    """Die Ziele der offenen Handles eines Prozesses. Wirft OSError."""
    with os.scandir(fd_dir) as it:
        return [os.readlink(e.path) for e in it if e.is_symlink()]


def in_benutzung(sqlite_pfad, ruhe_s=RUHE_S, jetzt=None, proc="/proc"):
    """Haelt ein anderer Prozess die Datenbank offen? Ohne /proc ersatzweise:
    wurde sie in den letzten `ruhe_s` Sekunden geschrieben?"""
    pids = geoeffnet_von(sqlite_pfad, proc)
    if pids is not None:
        return bool(pids)
    jetzt = time.time() if jetzt is None else jetzt
    juengst = max((os.path.getmtime(p) for p in (sqlite_pfad, sqlite_pfad + "-wal")
                   if os.path.exists(p)), default=0.0)
    return bool(juengst) and (jetzt - juengst) < ruhe_s


def quelle_zaehlen(sqlite_pfad, auslassen=()):
    """{tabelle: zeilen} der Quelle — nach `integrity_check`.

    Direkt mit sqlite3 und NUR lesend (`mode=ro`): die Pruefung darf die
    Quelle nicht veraendern, auch nicht um ein WAL."""
    if not os.path.isfile(sqlite_pfad):
        raise UmzugAbgebrochen(
            "SQLite-Datei nicht gefunden: %s — DB_PATH in der .env pruefen." % sqlite_pfad)
    con = sqlite3.connect("file:%s?mode=ro" % sqlite_pfad, uri=True)
    try:
        try:
            befund = con.execute("PRAGMA integrity_check").fetchone()[0]
        except sqlite3.DatabaseError as e:
            # Kein SQLite-Kopf (W92): sqlite3 wirft, bevor integrity_check
            # etwas sagen kann. Ein roher Traceback hier hiesse dem Betreiber
            # nichts — die Diagnose nennt Groesse, Kopf-Bytes und den Weg.
            raise UmzugAbgebrochen(
                "Die SQLite-Datei ist nicht lesbar (%s) — kein Umzug. %s"
                % (e, _dbwrap.datei_diagnose(sqlite_pfad))) from e
        if befund != "ok":
            raise UmzugAbgebrochen(
                "SQLite meldet integrity_check = %r — eine beschaedigte Quelle zieht "
                "nicht um. Erst retten: tools/dbwiederher.py bzw. tools/dbkopf.py." % befund)
        namen = [r[0] for r in con.execute(
            "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")]
        weg = set(_dbexport.DEFAULT_SKIP) | set(auslassen or ())
        return {n: con.execute('SELECT COUNT(*) FROM "%s"' % n).fetchone()[0]
                for n in namen if n not in weg}
    finally:
        con.close()


def ziel_zaehlen(tabellen):
    """{tabelle: zeilen} im aktuell konfigurierten Ziel; fehlende Tabelle = None."""
    with _dbwrap.db_conn() as conn:
        # Erst fragen, welche Tabellen es gibt — statt jeden Fehler beim
        # Zaehlen als „fehlt" zu lesen. Ein verweigertes SELECT (1142) haette
        # sonst wie ein leeres Ziel ausgesehen.
        if _dbwrap.DB_BACKEND == "mariadb":
            rows = conn.execute("SELECT TABLE_NAME AS n FROM information_schema.TABLES "
                                "WHERE TABLE_SCHEMA = DATABASE()").fetchall()
        else:
            rows = conn.execute("SELECT name AS n FROM sqlite_master "
                                "WHERE type='table'").fetchall()
        da = {r["n"] for r in rows}
        return {t: (conn.execute("SELECT COUNT(*) AS n FROM %s" % t).fetchone()["n"]
                    if t in da else None) for t in tabellen}


def vergleichen(quelle, ziel):
    """[(tabelle, quelle_n, ziel_n)] fuer jede Abweichung — leer heisst gleich."""
    return [(t, n, ziel.get(t)) for t, n in sorted(quelle.items()) if ziel.get(t) != n]


# ── Der Umzug ────────────────────────────────────────────────────────────────

def umziehen(*, sqlite_pfad, ziel_backend="mariadb", mariadb=None, log,
             ausgabe=print, auslassen=(), trotzdem_aktiv=False, trocken=False):
    """Quelle → Ziel. Rueckgabe: Bericht {"tabellen", "zeilen", "trocken"}.

    `ziel_backend="sqlite"` ist fuer die Vertraege da (Umzug in eine zweite
    SQLite-Datei, `mariadb={"db_path": …}`) — dieselbe Kette ohne Server.
    Wirft UmzugAbgebrochen mit Abhilfe; bis zum Import ist dann nichts
    geschrieben, und die .env fasst diese Funktion nie an.
    """
    mariadb = dict(mariadb or {})
    if not trotzdem_aktiv and in_benutzung(sqlite_pfad):
        raise UmzugAbgebrochen(
            "Ein anderer Prozess haelt die SQLite-Datei offen — der Bot laeuft noch. "
            "Erst den Dienst stoppen (systemctl stop <dienst>), sonst fehlt im Ziel, "
            "was er nach dem Export schreibt.")
    quelle = quelle_zaehlen(sqlite_pfad, auslassen)
    gesamt = sum(quelle.values())
    ausgabe("Quelle: %d Tabellen, %d Zeilen (%s)" % (len(quelle), gesamt, sqlite_pfad))

    # 1) Ziel konfigurieren und pruefen, BEVOR irgendetwas geschrieben wird.
    _ziel_konfigurieren(ziel_backend, mariadb)
    try:
        vorher = ziel_zaehlen(quelle)
    except Exception as e:
        raise UmzugAbgebrochen(_verbindungsrat(e, mariadb)) from e
    belegt = {t: n for t, n in vorher.items() if n}
    if belegt:
        raise UmzugAbgebrochen(
            "Das Ziel ist nicht leer (%s) — ein Umzug ueberschreibt nichts. Leere "
            "Datenbank anlegen oder die vorhandene bewusst sichern und leeren."
            % ", ".join("%s=%d" % kv for kv in sorted(belegt.items())[:5]))
    if trocken:
        ausgabe("Trockenlauf: Ziel erreichbar und leer — es wurde nichts geschrieben.")
        return {"tabellen": len(quelle), "zeilen": gesamt, "trocken": True}

    # 2) Export aus der Quelle, im Dialekt des ZIELS escaped.
    _dbwrap.configure_db(db_path=sqlite_pfad, backend="sqlite")
    sql = "\n".join(_dbexport.db_export_sql(dialect=ziel_backend,
                                            skip_tables=tuple(_dbexport.DEFAULT_SKIP)
                                            + tuple(auslassen or ())))

    # 3) Schema im Ziel, dann die Daten.
    _ziel_konfigurieren(ziel_backend, mariadb)
    with _dbwrap.db_conn() as conn:
        p = _schema.anlegen(conn, backend=ziel_backend,
                            mariadb_db=mariadb.get("db", ""), log=log)
        _schemastand.lege_an(conn, pk=p["pk"], txt_idx=p["txt_idx"],
                             txt_long=p["txt_long"], tbl_opts=p["tbl_opts"])
    fehlt = [t for t, n in ziel_zaehlen(quelle).items() if n is None]
    if fehlt:
        raise UmzugAbgebrochen(
            "Diese Tabellen der Quelle kennt das Schema nicht: %s — Altbestand einer "
            "frueheren Fassung. Mit --auslassen %s bewusst weglassen oder vorher "
            "sichern." % (", ".join(fehlt), ",".join(fehlt)))
    bericht = _dbexport.db_import_sql(sql, expect_dialect=ziel_backend)
    if not bericht.get("ok"):
        raise UmzugAbgebrochen(
            "Import gescheitert (%d von %d Anweisungen): %s — die .env bleibt auf "
            "SQLite, der Bot laeuft unveraendert weiter."
            % (bericht.get("applied", 0), bericht.get("statements", 0),
               "; ".join(str(x) for x in (bericht.get("errors") or [])[:3])))

    # 4) Nachzaehlen. Erst wenn jede Tabelle stimmt, ist der Umzug einer.
    abw = vergleichen(quelle, ziel_zaehlen(quelle))
    if abw:
        raise UmzugAbgebrochen(
            "Zeilenzahl weicht ab: %s — die .env bleibt auf SQLite."
            % ", ".join("%s %s→%s" % a for a in abw[:5]))
    ausgabe("Ziel: alle %d Tabellen mit gleicher Zeilenzahl (%d Zeilen)." % (len(quelle), gesamt))
    return {"tabellen": len(quelle), "zeilen": gesamt, "trocken": False}


def _ziel_konfigurieren(backend, mariadb):
    if backend == "mariadb":
        _dbwrap.set_pool(None)       # frischer Pool mit den neuen Zugangsdaten
        _dbwrap.configure_db(backend="mariadb", mariadb={
            k: mariadb[k] for k in ("host", "port", "user", "password", "db") if k in mariadb})
    else:
        _dbwrap.configure_db(backend="sqlite", db_path=mariadb["db_path"])


def _verbindungsrat(e, mariadb):
    """Ein Satz mit Abhilfe statt eines pymysql-Tracebacks (Lehre aus W92/W93)."""
    t = "%s: %s" % (type(e).__name__, e)
    if "No module named" in t and "pymysql" in t:
        return "PyMySQL fehlt — bash tools/update.sh --optional (oder pip install PyMySQL)."
    if "1045" in t:
        return ("MariaDB lehnt Nutzer/Passwort ab (1045) — MARIADB_USER/MARIADB_PASSWORD "
                "pruefen; tools/update.sh legt den Nutzer auf Wunsch an.")
    if "1049" in t:
        return ("Die Datenbank %r gibt es im Server nicht (1049) — anlegen lassen: "
                "bash tools/update.sh." % mariadb.get("db"))
    if "2003" in t or "Connection refused" in t:
        return ("MariaDB nicht erreichbar auf %s:%s (2003) — laeuft der Dienst? "
                "systemctl status mariadb" % (mariadb.get("host"), mariadb.get("port")))
    return "MariaDB nicht nutzbar: %s" % t


# ── .env ─────────────────────────────────────────────────────────────────────

def env_setzen(pfad, werte, jetzt=None):
    """Die MariaDB-Schluessel in die .env — Sicherung `.env.vor-mariadb-<zeit>`.

    Die Regeln (letzte Zeile gewinnt, atomar, Rechte und Besitzer der alten
    Datei) stehen seit W144 in nc/envdatei.py, fuer alle Schreiber gleich."""
    try:
        return _envdatei.setzen(pfad, {k: werte[k] for k in ENV_SCHLUESSEL if k in werte},
                                "vor-mariadb", jetzt)
    except _envdatei.EnvdateiFehler as e:
        raise UmzugAbgebrochen(str(e)) from e
