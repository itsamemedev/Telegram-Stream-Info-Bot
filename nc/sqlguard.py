"""nc.sqlguard — v4.0-W14: harte Read-only-Pruefung fuer die KI-Abfrage.

Warum: der bisherige Schutz war eine WORTLISTE mit Leerzeichen-Padding
(" delete " usw.). Das laesst sich trivial umgehen, weil SQLite

    WITH x AS (SELECT 1) DELETE FROM recordings

erlaubt UND Trennzeichen nicht nur Leerzeichen sind. Bewiesen umgangen mit
TABS und mit /**/-Kommentaren -> echte Datenloeschung. Die Frage kommt vom
Nutzer und wird von einem LLM in SQL uebersetzt, ist also beeinflussbar.

Dieses Modul normalisiert zuerst (Kommentare raus, ALLE Whitespaces zu
Leerzeichen) und prueft dann mit Wortgrenzen. Die eigentliche Garantie
liefert zusaetzlich eine read-only Datenbankverbindung im Bot.
"""

import re

# Alles, was Daten oder Schema aendert bzw. aus der Sandbox ausbricht.
FORBIDDEN = ("insert", "update", "delete", "drop", "alter", "create", "attach",
             "detach", "pragma", "replace", "vacuum", "into", "reindex",
             "analyze", "begin", "commit", "rollback", "savepoint", "trigger",
             "grant", "revoke", "load_extension", "writefile", "readfile",
             # v4.0-W118 (SEC): die Liste war auf SQLite gemuenzt. Unter
             # DB_BACKEND=mariadb sind ganz andere Dinge gefaehrlich, und ein
             # reines SELECT reicht dort fuer Dateizugriff und Lahmlegen:
             #   SELECT LOAD_FILE('/etc/passwd')      -> Datei lesen
             #   SELECT ... INTO OUTFILE '/var/www/x' -> Datei schreiben
             #   SELECT SLEEP(600) / BENCHMARK(...)   -> Verbindung blockieren
             #   SELECT ... FROM mysql.user           -> Passwort-Hashes
             # "into" stand schon drin, der Rest nicht. Wortgrenzen sorgen
             # dafuer, dass z.B. OFFSET nicht an "set" haengenbleibt.
             "load_file", "outfile", "dumpfile", "benchmark", "sleep",
             "information_schema", "mysql", "performance_schema", "sys_exec",
             "handler", "lock", "unlock", "prepare", "execute", "call", "set",
             "show", "describe", "use", "kill", "shutdown")

_LINE_COMMENT = re.compile(r"--[^\n]*")
_BLOCK_COMMENT = re.compile(r"/\*.*?\*/", re.S)
_WS = re.compile(r"\s+")


def normalize(sql):
    """Kommentare entfernen, jede Whitespace-Folge (auch \\t, \\r, \\f, \\v) zu
       EINEM Leerzeichen. Ohne das greifen Wortpruefungen nicht zuverlaessig."""
    if not sql or not isinstance(sql, str):
        return ""
    s = _BLOCK_COMMENT.sub(" ", sql)
    s = _LINE_COMMENT.sub(" ", s)
    return _WS.sub(" ", s).strip()


def check_readonly(sql, tables=()):
    """(normalisiertes_sql, None) wenn die Abfrage sicher lesend ist,
       sonst (None, grund). tables = erlaubte Tabellen (leer = nicht pruefen)."""
    s = normalize(sql).rstrip(";").strip()
    if not s:
        return None, "leeres SQL"
    if ";" in s:                       # keine gestapelten Statements
        return None, "mehrere Statements sind nicht erlaubt"
    low = s.lower()
    if not (low.startswith("select") or low.startswith("with")):
        return None, "nur SELECT erlaubt"
    for word in FORBIDDEN:
        if re.search(r"\b" + word + r"\b", low):
            return None, f"unzulaessiges Schluesselwort: {word}"
    if tables and not any(re.search(r"\b" + re.escape(t) + r"\b", low) for t in tables):
        return None, "keine bekannte Tabelle referenziert"
    return s, None


# v5.6-W197: ein LIMIT am ENDE der Abfrage — nur das begrenzt die aeussere
# Ergebnismenge. Erwartet das normalisierte SQL aus check_readonly (keine
# Kommentare, kein Semikolon, Whitespace zu einem Leerzeichen).
_LIMIT_ENDE = re.compile(r"\blimit (\d+)(?: ?(,|offset) ?(\d+))?$", re.I)

# Wie lange die KI-Abfrage rechnen darf, bevor die Datenbank sie abbricht.
FRIST_S = 15


def with_limit(sql, limit=200):
    """Hoechstens `limit` Zeilen fuer die AEUSSERE Abfrage.

    v5.6-W197: bis hierher genuegte das Wort „limit" IRGENDWO, damit gar
    nichts angehaengt wurde. `SELECT * FROM chat_messages WHERE id IN (SELECT
    id FROM chat_messages LIMIT 5)` holte damit die ganze Tabelle — das LIMIT
    der Unterabfrage begrenzt die aeussere Menge nicht. Und ein `LIMIT 1000000`
    am Ende ging unveraendert durch. Jetzt zaehlt nur ein LIMIT am Ende, und
    sein Wert wird auf `limit` gedeckelt."""
    n = int(limit)
    s = sql.rstrip()
    m = _LIMIT_ENDE.search(s)
    if not m:
        return f"{s} LIMIT {n}"
    a, trenn, b = m.group(1), (m.group(2) or "").lower(), m.group(3)
    if trenn == ",":                    # LIMIT versatz, anzahl (MySQL/SQLite)
        neu = f"LIMIT {a}, {min(int(b), n)}"
    elif trenn == "offset":
        neu = f"LIMIT {min(int(a), n)} OFFSET {b}"
    else:
        neu = f"LIMIT {min(int(a), n)}"
    return s[:m.start()] + neu


def abbruch_nach(frist_s, uhr=None):
    """Fortschritts-Handler fuer sqlite3.Connection.set_progress_handler:
    liefert ab der Frist 1, und SQLite bricht mit „interrupted" ab.

    v5.6-W197: die KI-Abfrage hatte keine Frist. Eine rekursive CTE ohne
    Abbruch oder ein Kreuzprodukt zweier grosser Tabellen lief, bis jemand den
    Dienst neu startete — und hielt dabei einen Lese-Schnappschuss, an dem der
    WAL-Checkpoint nicht vorbeikommt: `-wal` waechst, solange sie laeuft."""
    import time as _time
    uhr = uhr or _time.monotonic
    ende = uhr() + float(frist_s)

    def _handler():
        return 1 if uhr() > ende else 0
    return _handler


def mariadb_mit_frist(sql, frist_s=FRIST_S):
    """Dieselbe Frist unter MariaDB — je Anweisung, nicht je Sitzung.

    `SET SESSION max_statement_time` bliebe an der Verbindung haengen, und die
    geht zurueck in den Pool: die naechste Wartungsabfrage auf derselben
    Verbindung wuerde nach 15 s abgebrochen. `SET STATEMENT ... FOR` gilt nur
    fuer diese eine Abfrage (MariaDB ab 10.1.2)."""
    return "SET STATEMENT max_statement_time=%d FOR %s" % (int(frist_s), sql)


def frist_unbekannt(e) -> bool:
    """Kennt der Server `SET STATEMENT max_statement_time` nicht (MySQL statt
    MariaDB)? Dann laeuft die Abfrage ohne Frist, und der Aufrufer sagt das."""
    t = str(e)
    return ("near 'STATEMENT max_statement_time" in t
            or "Unknown system variable 'max_statement_time'" in t)


def frist_ueberschritten(e) -> bool:
    """Hat die Datenbank die Abfrage wegen der Frist abgebrochen?
    SQLite: „interrupted" (Fortschritts-Handler). MariaDB: Fehler 1969
    „Query execution was interrupted (max_statement_time exceeded)"."""
    t = str(e).lower()
    return t == "interrupted" or "max_statement_time exceeded" in t
