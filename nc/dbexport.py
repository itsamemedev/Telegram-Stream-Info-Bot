"""nc.dbexport — Datenbank als portables SQL exportieren und importieren.

Zweck: der Umstieg SQLite -> MariaDB (und zurueck) ohne Handarbeit.

WARUM NICHT `sqlite3 .dump` / `mysqldump`?
Beide erzeugen dialekt-spezifische DDL. `.dump` schreibt
"INTEGER PRIMARY KEY AUTOINCREMENT" und "BEGIN TRANSACTION" — MariaDB frisst
das nicht. mysqldump schreibt Backticks und ENGINE=InnoDB — SQLite frisst das
nicht. Ein DDL-Uebersetzer waere eine eigene Baustelle mit vielen Sonderfaellen.

DER WEG HIER: **nur Daten exportieren, das Schema baut das Ziel selbst.**
bot._init_db() legt alle 42 Tabellen bereits in beiden Dialekten korrekt an
(_schema_pk(), txt_idx/txt_big/tbl_opts). Also: Bot einmal gegen das neue
Backend starten -> Schema steht -> dieses SQL einspielen. Das ist robust, weil
die Schema-Wahrheit an genau EINER Stelle bleibt.

DER DIALEKT-FALLSTRICK (echt, nicht theoretisch):
MySQL/MariaDB behandeln den Backslash in String-Literalen als Escape-Zeichen,
SQLite NICHT. 'C:\\pfad' ist in SQLite der Text C:\\pfad, in MariaDB wird daraus
C:pfad — Dateipfade und Regexe waeren still zerstoert. Deshalb kennt der Export
seinen ZIEL-Dialekt und escaped entsprechend; der Header haelt ihn fest und der
Import prueft ihn.
"""
import datetime
import logging

from nc.dbwrap import db_conn

log = logging.getLogger("TikTokBot")

HEADER_MARK = "-- NIGHTCRAWLER-DB-EXPORT"
DIALECTS = ("sqlite", "mariadb")

# Tabellen, die beim Umzug nichts verloren haben (Laufzeit-/Cache-Daten).
# Werden per default uebersprungen; skip_tables=() holt sie doch mit.
DEFAULT_SKIP = ("sqlite_sequence", "sqlite_stat1")


def _tables(conn):
    """Tabellennamen — backend-agnostisch."""
    cur = conn.cursor()
    try:
        cur.execute("SELECT name FROM sqlite_master WHERE type='table' "
                    "ORDER BY name")
        return [r[0] for r in cur.fetchall()]
    except Exception:
        pass
    cur.execute("SHOW TABLES")
    return [r[0] if not isinstance(r, dict) else list(r.values())[0]
            for r in cur.fetchall()]


def _columns(conn, table):
    cur = conn.cursor()
    try:
        cur.execute("PRAGMA table_info(%s)" % table)
        rows = cur.fetchall()
        if rows:
            return [r["name"] for r in rows]
    except Exception:
        pass
    cur.execute("SELECT * FROM %s LIMIT 0" % table)
    return [d[0] for d in cur.description]


def _lit(v, dialect):
    """Ein Python-Wert -> SQL-Literal fuer den ZIEL-Dialekt."""
    if v is None:
        return "NULL"
    if isinstance(v, bool):
        return "1" if v else "0"
    if isinstance(v, int):
        return str(v)
    if isinstance(v, float):
        # inf/nan sind in keinem der beiden Dialekte darstellbar
        if v != v or v in (float("inf"), float("-inf")):
            return "NULL"
        return repr(v)
    if isinstance(v, (bytes, bytearray)):
        # X'..' versteht SQLite wie MariaDB
        return "X'%s'" % bytes(v).hex()
    if isinstance(v, (datetime.datetime, datetime.date)):
        v = v.isoformat(sep=" ")
    s = str(v)
    s = s.replace("'", "''")
    if dialect == "mariadb":
        # DER Fallstrick: Backslash ist in MySQL ein Escape, in SQLite nicht.
        s = s.replace("\\", "\\\\")
    return "'%s'" % s


def _split_statements(sql):
    """SQL-Text in Statements zerlegen.

    Naiv auf ';' zu splitten zerreisst jeden Wert, der ein Semikolon enthaelt
    (Chat-Nachrichten, HTML-Entities, Regexe) — deshalb wird hier zeichenweise
    geparst und der String-Zustand mitgefuehrt.
    """
    out, buf = [], []
    in_str = False
    esc_backslash = False    # nur relevant, wenn der Dump MariaDB-escaped ist
    i, n = 0, len(sql)
    while i < n:
        ch = sql[i]
        if in_str:
            buf.append(ch)
            if esc_backslash:
                esc_backslash = False
            elif ch == "\\":
                esc_backslash = True
            elif ch == "'":
                if i + 1 < n and sql[i + 1] == "'":   # '' = escaptes Quote
                    buf.append("'")
                    i += 2
                    continue
                in_str = False
            i += 1
            continue
        if ch == "'":
            in_str = True
            buf.append(ch)
        elif ch == "-" and sql.startswith("--", i):
            j = sql.find("\n", i)
            i = n if j < 0 else j + 1
            continue
        elif ch == ";":
            st = "".join(buf).strip()
            if st:
                out.append(st)
            buf = []
        else:
            buf.append(ch)
        i += 1
    st = "".join(buf).strip()
    if st:
        out.append(st)
    return out


def db_export_sql(dialect="mariadb", skip_tables=DEFAULT_SKIP,
                  batch=200, truncate=True):
    """Generator: liefert den SQL-Export zeilenweise (streamt, kein RAM-Berg).

    dialect: fuer welches ZIEL-Backend die Literale escaped werden.
    truncate: DELETE FROM vor jedem Insert-Block (Wiedereinspielen ohne Dubletten).
    """
    if dialect not in DIALECTS:
        raise ValueError("dialect muss sqlite oder mariadb sein, nicht %r" % dialect)
    skip = set(skip_tables or ())
    now = datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds")

    with db_conn() as conn:
        tables = [t for t in _tables(conn) if t not in skip]
        total = 0
        counts = {}
        for t in tables:
            cur = conn.cursor()
            try:
                cur.execute("SELECT COUNT(*) FROM %s" % t)
                r = cur.fetchone()
                c = (list(r.values())[0] if isinstance(r, dict) else r[0]) or 0
            except Exception:
                c = 0
            counts[t] = c
            total += c

        yield HEADER_MARK + "\n"
        yield "-- Erzeugt:      %s\n" % now
        yield "-- Ziel-Dialekt: %s\n" % dialect
        yield "-- Tabellen:     %d\n" % len(tables)
        yield "-- Zeilen:       %d\n" % total
        yield "--\n"
        yield "-- NUR DATEN. Das Schema legt der Bot selbst an (_init_db kennt\n"
        yield "-- beide Dialekte). Vorgehen beim Umstieg:\n"
        yield "--   1) .env auf das neue Backend stellen (DB_BACKEND=mariadb + MARIADB_*)\n"
        yield "--   2) Bot einmal starten -> Schema wird angelegt -> wieder stoppen\n"
        yield "--   3) Diesen Export einspielen (Dashboard -> Wartung -> Import)\n"
        yield "--\n"
        if dialect == "mariadb":
            yield "SET FOREIGN_KEY_CHECKS=0;\n"
            yield "SET sql_mode='';\n"
        else:
            yield "PRAGMA foreign_keys=OFF;\n"
        yield "\n"

        for t in tables:
            cols = _columns(conn, t)
            if not cols:
                continue
            yield "-- ---- %s (%d Zeilen) ----\n" % (t, counts.get(t, 0))
            if truncate:
                yield "DELETE FROM %s;\n" % t
            if not counts.get(t):
                yield "\n"
                continue
            collist = ", ".join(cols)
            cur = conn.cursor()
            cur.execute("SELECT %s FROM %s" % (collist, t))
            rows, buf = 0, []
            while True:
                chunk = cur.fetchmany(batch)
                if not chunk:
                    break
                for row in chunk:
                    vals = [row[c] if isinstance(row, dict) else row[i]
                            for i, c in enumerate(cols)]
                    buf.append("(%s)" % ", ".join(_lit(v, dialect) for v in vals))
                    rows += 1
                yield "INSERT INTO %s (%s) VALUES\n%s;\n" % (
                    t, collist, ",\n".join(buf))
                buf = []
            yield "\n"

        if dialect == "mariadb":
            yield "SET FOREIGN_KEY_CHECKS=1;\n"
        else:
            yield "PRAGMA foreign_keys=ON;\n"
        yield "-- Export vollstaendig: %d Tabellen, %d Zeilen\n" % (len(tables), total)


def export_summary(skip_tables=DEFAULT_SKIP):
    """Zeilen pro Tabelle — fuers Dashboard, ohne den Export zu bauen."""
    skip = set(skip_tables or ())
    out = {}
    with db_conn() as conn:
        for t in _tables(conn):
            if t in skip:
                continue
            try:
                cur = conn.cursor()
                cur.execute("SELECT COUNT(*) FROM %s" % t)
                r = cur.fetchone()
                out[t] = (list(r.values())[0] if isinstance(r, dict) else r[0]) or 0
            except Exception:
                out[t] = -1
    return out


def parse_header(sql_text):
    """Dialekt + Kennzahlen aus dem Export-Header lesen. {} wenn kein Header."""
    head = sql_text[:2000]
    if HEADER_MARK not in head:
        return {}
    info = {}
    for line in head.splitlines():
        if not line.startswith("--"):
            continue
        if "Ziel-Dialekt:" in line:
            info["dialect"] = line.split(":", 1)[1].strip()
        elif "Zeilen:" in line:
            try:
                info["rows"] = int(line.split(":", 1)[1].strip())
            except ValueError:
                pass
        elif "Tabellen:" in line:
            try:
                info["tables"] = int(line.split(":", 1)[1].strip())
            except ValueError:
                pass
        elif "Erzeugt:" in line:
            info["created"] = line.split(":", 1)[1].strip()
    return info


def db_import_sql(sql_text, expect_dialect=None, dry_run=False):
    """Spielt einen Export ein. Gibt einen Bericht zurueck.

    expect_dialect: aktuelles Backend. Passt der Header nicht dazu, wird
    abgebrochen — ein mariadb-escapter Dump in SQLite wuerde Backslashes
    verdoppeln und Pfade still zerstoeren.
    dry_run: nur zaehlen und pruefen, nichts schreiben.
    """
    info = parse_header(sql_text)
    rep = {"ok": False, "header": info, "statements": 0, "applied": 0,
           "errors": [], "dry_run": bool(dry_run)}

    if expect_dialect and info.get("dialect") and info["dialect"] != expect_dialect:
        rep["errors"].append(
            "Dump ist fuer '%s' escaped, dieses Backend ist '%s'. Backslashes in "
            "Pfaden wuerden dabei still kaputtgehen. Exportiere neu mit "
            "dialect=%s." % (info["dialect"], expect_dialect, expect_dialect))
        return rep

    stmts = _split_statements(sql_text)
    rep["statements"] = len(stmts)
    if not stmts:
        rep["errors"].append("Keine Statements gefunden — leere oder kaputte Datei?")
        return rep
    if dry_run:
        rep["ok"] = True
        return rep

    with db_conn() as conn:
        cur = conn.cursor()
        for st in stmts:
            try:
                cur.execute(st)
                rep["applied"] += 1
            except Exception as e:
                # PRAGMA/SET des jeweils anderen Dialekts sind harmlos
                if st.upper().startswith(("PRAGMA", "SET ")):
                    continue
                rep["errors"].append("%s: %s" % (st[:70].replace("\n", " "), e))
                if len(rep["errors"]) > 25:
                    rep["errors"].append("… weitere Fehler unterdrueckt, Abbruch.")
                    raise
    rep["ok"] = not rep["errors"]
    log.info("DB-Import: %d/%d Statements, %d Fehler",
             rep["applied"], rep["statements"], len(rep["errors"]))
    return rep
