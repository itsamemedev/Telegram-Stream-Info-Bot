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


def with_limit(sql, limit=200):
    """Erzwingt ein LIMIT, falls keines gesetzt ist."""
    return sql if re.search(r"\blimit\b", sql, re.I) else f"{sql} LIMIT {int(limit)}"
