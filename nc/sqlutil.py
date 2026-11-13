"""nc.sqlutil — SQL-Text-Helfer für Brain-NL→SQL + Archiv (rein).

Extrahiert aus bot.py: Übersetzungs-Mapping natürlicher Begriffe,
regelbasierter SQL-Bau, sichere ORDER-BY-Klauseln."""



def _translate_sql(sql: str, mit_parametern: bool = True) -> str:
    """Convert SQLite '?' placeholders to MariaDB '%s'. Schont Strings.

    v4.2-W150: pymysql formatiert den GANZEN Text mit `query % args` — auch
    das Innere von Zeichenketten. Ein `%` in einem Literal (`'100% welt'`)
    blieb hier bisher stehen und warf "not enough arguments for format
    string"; der Umzug nach MariaDB scheiterte damit an jedem Datensatz, der
    ein Prozentzeichen traegt. Mit Parametern wird deshalb JEDES `%`
    verdoppelt. Ohne Parameter formatiert pymysql gar nicht (der Aufrufer
    reicht dann None durch) — dann darf auch nichts verdoppelt werden, sonst
    stuende `%%` woertlich in der Datenbank."""
    out = []
    in_string = False
    str_char = None
    i = 0
    while i < len(sql):
        c = sql[i]
        if in_string:
            if c == '\\' and i + 1 < len(sql):
                nxt = sql[i + 1]
                out.append(c)
                out.append('%%' if (nxt == '%' and mit_parametern) else nxt)
                i += 2; continue
            if c == str_char:
                in_string = False
            out.append('%%' if (c == '%' and mit_parametern) else c)
        elif c in ("'", '"'):
            in_string = True
            str_char = c
            out.append(c)
        elif c == '?':
            out.append('%s')
        elif c == '%':
            # PyMySQL behandelt '%' als format-char — escape zu '%%'
            out.append('%%' if mit_parametern else '%')
        else:
            out.append(c)
        i += 1
    return ''.join(out)

def zeitfenster_literal(heute=False, jetzt=None) -> str:
    """Untergrenze eines Zeitfensters als ISO-Literal — fuer BEIDE Backends.

    v5.6-W197: hier stand `datetime('now','-7 days')` und `date('now')`. Das
    ist SQLite; unter MariaDB (dem Betrieb seit 11/2026) gibt es keine
    Funktion `datetime`, und vier der sechs Regel-Abfragen endeten in
    „FUNCTION datetime does not exist". Die Zeitspalten sind in beiden
    Backends ISO-8601-Zeichenketten (MariaDB: VARCHAR(64), nc/schema.py) — ein
    Vergleich mit einem ISO-Literal ist also dort wie hier derselbe
    Zeichenkettenvergleich, ohne Dialekt."""
    from datetime import datetime, timedelta, timezone
    jetzt = jetzt or datetime.now(timezone.utc)
    if heute:
        return "'" + jetzt.strftime("%Y-%m-%d") + "'"
    return "'" + (jetzt - timedelta(days=7)).strftime("%Y-%m-%dT%H:%M:%S") + "'"


def _rule_based_sql(q, jetzt=None):
    """Fallback NL→SQL für häufige Fragen, falls keine LLM verfügbar ist."""
    ql = (q or "").lower()
    win = zeitfenster_literal("today" in ql or "heute" in ql, jetzt)
    if ("fail" in ql or "scheiter" in ql or "fehl" in ql) and ("most" in ql or "meist" in ql or "häufig" in ql):
        return ("SELECT username, COUNT(*) AS fehlversuche FROM recording_attempts "
                "WHERE outcome NOT IN ('ok','stall_killed_partial','running','cancelled') "
                f"AND started_at >= {win} GROUP BY username ORDER BY fehlversuche DESC LIMIT 10")
    if ("recording" in ql or "aufnahme" in ql) and ("how many" in ql or "wie viele" in ql or "count" in ql or "anzahl" in ql):
        return f"SELECT COUNT(*) AS aufnahmen FROM recordings WHERE created_at >= {win}"
    if "storage" in ql or "speicher" in ql or "größt" in ql or "largest" in ql or "biggest" in ql:
        return ("SELECT username, ROUND(SUM(file_size)/1048576.0,1) AS mb, COUNT(*) AS n "
                "FROM recordings GROUP BY username ORDER BY mb DESC LIMIT 10")
    if "success" in ql or "erfolg" in ql:
        return ("SELECT ROUND(100.0*SUM(CASE WHEN outcome IN ('ok','stall_killed_partial') THEN 1 ELSE 0 END)/"
                "NULLIF(SUM(CASE WHEN outcome NOT IN ('running','cancelled') THEN 1 ELSE 0 END),0),1) AS erfolgsquote_prozent "
                f"FROM recording_attempts WHERE started_at >= {win}")
    if "active" in ql or "aktiv" in ql or "live" in ql:
        return "SELECT username, last_live FROM trackings WHERE paused=0 ORDER BY last_live DESC LIMIT 15"
    if "longest" in ql or "längst" in ql:
        return ("SELECT username, ROUND(MAX(duration_secs)/60.0,1) AS minuten FROM recordings "
                "GROUP BY username ORDER BY minuten DESC LIMIT 10")
    return None

def _archive_sort_clause(sort: str, direction: str) -> str:
    """Whitelist-basierter ORDER-BY-Builder. KEINE Userinput-Interpolation
       — die Werte werden ausschließlich gegen feste Maps geprüft.
       F39-Bug-Hunt-Fix H4: Tiebreaker folgt jetzt der Sortier-Richtung statt
       hart 'id DESC' zu sein. Bei 'name ASC' mit Ties war vorher der neueste
       Eintrag oben, bei 'name DESC' aber auch — verwirrend.
       B3-Fix: COLLATE NOCASE ist SQLite-only — MariaDB crasht damit. Statt
       Backend-spezifischer SQL nutzen wir LOWER(...) wenn case-insensitive
       sortiert werden soll — funktioniert auf beiden Backends identisch.
    """
    sort_map = {
        'date':     'created_at',
        'name':     'LOWER(COALESCE(NULLIF(title, ""), filename))',
        'filename': 'LOWER(filename)',
        'size':     'COALESCE(size_bytes, 0)',
    }
    col = sort_map.get(sort, 'created_at')
    dir_kw = 'ASC' if direction == 'asc' else 'DESC'
    return f"ORDER BY {col} {dir_kw}, id {dir_kw}"


_ARCHIVE_KIND_MAP = {
    'video': {'mp4', 'webm', 'mov', 'mkv', 'avi', 'm4v', 'ts', 'flv', 'mpg', 'mpeg'},
    'audio': {'mp3', 'wav', 'ogg', 'm4a', 'aac', 'flac', 'opus'},
    'image': {'jpg', 'jpeg', 'png', 'webp', 'gif', 'avif'},
}


def _archive_where_clause(kind: str = 'all', query=None, date_from=None, date_to=None):
    """F39 (DRY-Fix für F38-Bug-Hunt H3): liefert (where_sql, params).
       Wird sowohl von get_archive_entries_paged als auch von
       get_archive_aggregate_stats benutzt. Vorher dupliziert — Drift-Risiko
       wenn wir die Filter-Semantik mal anpassen (z.B. neue Spalte).
       v37: + Datums-Range (date_from/date_to, created_at ist ISO-Text).
    """
    where = []
    params = []
    if query:
        q = f"%{query.lower()}%"
        where.append("(LOWER(filename) LIKE ? OR LOWER(COALESCE(title, '')) LIKE ? "
                     "OR LOWER(COALESCE(notes, '')) LIKE ? OR LOWER(COALESCE(source_url, '')) LIKE ?)")
        params.extend([q, q, q, q])
    # Kind-Filter via Extension-Liste in (...).
    # LIKE '%.ext' statt einer dedizierten Extension-Spalte — bei ein paar
    # Dutzend Extensions schnell genug, und wir müssen die DB nicht migrieren.
    if kind in _ARCHIVE_KIND_MAP:
        exts = _ARCHIVE_KIND_MAP[kind]
        ext_clauses = " OR ".join(["LOWER(filename) LIKE ?"] * len(exts))
        where.append(f"({ext_clauses})")
        params.extend([f"%.{e}" for e in sorted(exts)])
    # v37: Datums-Range — created_at ist ISO ('YYYY-MM-DDTHH:MM:SS'), also reicht
    # der String-Vergleich. date_to schließt den kompletten Endtag ein.
    if date_from:
        where.append("created_at >= ?")
        params.append(str(date_from)[:10])
    if date_to:
        where.append("created_at <= ?")
        params.append(str(date_to)[:10] + "T23:59:59")
    where_sql = ("WHERE " + " AND ".join(where)) if where else ""
    return where_sql, params
