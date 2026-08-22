"""nc.eventquery — v4.0-W51: der Event-Log-Query-Bauer, aus bot_v37 gelöst.

Baut die SELECT-Abfrage fürs Event-Log mit optionalen, PARAMETRISIERTEN Filtern
(kind/severity) — der WHERE-Teil entsteht dynamisch, aber jeder Wert geht als
Platzhalter rein (injektionssicher). Rein: Filter rein, (sql, params) raus; die
Ausführung bleibt beim Aufrufer (db_conn). Bitgenau gegen den Monolithen geprüft.
"""

from typing import Optional


def build_query(limit: int = 100, kind: Optional[str] = None,
                severity: Optional[str] = None):
    """Liefert (sql, params) für Events neueste-zuerst, optional nach
       kind/severity gefiltert. LIMIT steht immer als letzter Parameter."""
    where = []
    params = []
    if kind:
        where.append("kind = ?")
        params.append(kind)
    if severity:
        where.append("severity = ?")
        params.append(severity)
    wsql = ("WHERE " + " AND ".join(where)) if where else ""
    sql = (f"SELECT id, ts, kind, severity, summary, payload FROM event_log "
           f"{wsql} ORDER BY id DESC LIMIT ?")
    return sql, params + [limit]
