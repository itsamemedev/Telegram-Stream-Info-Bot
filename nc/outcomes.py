"""nc.outcomes — v4.1-W26: warum Aufnahmen scheitern, nach Ursache gebuendelt.

Aus dem Monolithen geloest. `_OUTCOME_META` wandert mit: die Zuordnung
Ausgang -> Klartext und Farbe gehoert zur Auswertung, nicht ins Deck. Stuenden
beide getrennt, muesste man sie doppelt pflegen — und ein neuer Ausgang taucht
dann in der Liste auf, aber ohne Namen.
"""

from datetime import datetime, timedelta, timezone

from nc.dbwrap import db_conn


_OUTCOME_META = {
    "ok":                    ("OK",                 "good"),
    "stall_killed_partial":  ("OK (Stall, partial)","warn"),
    "early_disconnect":      ("Early Disconnect",   "bad"),
    "stall_killed":          ("Stall (kill, 0B)",   "bad"),
    "codec_header_fail":     ("Codec/Input-Fehler", "bad"),   # B59
    "hevc_unsupported":      ("HEVC – ffmpeg-Update nötig", "bad"),  # B64
    "stream_dead":           ("Stream Dead (404)",  "bad"),   # B43
    "resolve_failed":        ("Resolve Failed",     "bad"),
    "start_failed":          ("Start Failed",       "bad"),
    "fail":                  ("Fail (sonstig)",     "bad"),
    "running":               ("Running",            "muted"),
}


def get_outcome_breakdown(hours: int = 24) -> dict:
    """Returns {total, since_iso, by_outcome:[{key,label,status,count,pct}],
                top_failing_users:[{username, fail_count}], early_disconnect_users:[...]}.
       hours: Zeitfenster (max 168 = 7 Tage)."""
    hours = max(1, min(int(hours or 24), 168))
    since = (datetime.now(timezone.utc) - timedelta(hours=hours)).isoformat()

    with db_conn() as conn:
        rows = conn.execute(
            "SELECT outcome, COUNT(*) AS c FROM recording_attempts "
            "WHERE started_at >= ? GROUP BY outcome ORDER BY c DESC",
            (since,)).fetchall()
        total = sum(r["c"] for r in rows)
        # F57: Top User mit Failures (alles außer ok/partial)
        top_fail = conn.execute(
            "SELECT username, COUNT(*) AS c FROM recording_attempts "
            "WHERE started_at >= ? "
            "AND outcome NOT IN ('ok', 'stall_killed_partial', 'running') "
            "GROUP BY username ORDER BY c DESC LIMIT 5",
            (since,)).fetchall()
        # F57: Top User mit early_disconnect (das ist der TikTok-Pain-Point)
        top_ed = conn.execute(
            "SELECT username, COUNT(*) AS c FROM recording_attempts "
            "WHERE started_at >= ? AND outcome = 'early_disconnect' "
            "GROUP BY username ORDER BY c DESC LIMIT 5",
            (since,)).fetchall()

    by_outcome = []
    for r in rows:
        key = r["outcome"] or "unknown"
        label, status = _OUTCOME_META.get(key, (key, "muted"))
        pct = round(r["c"] / total * 100, 1) if total else 0
        by_outcome.append({"key": key, "label": label, "status": status,
                           "count": r["c"], "pct": pct})

    return {
        "total":      total,
        "hours":      hours,
        "since":      since,
        "by_outcome": by_outcome,
        "top_failing_users": [{"username": r["username"], "fail_count": r["c"]}
                              for r in top_fail],
        "early_disconnect_users": [{"username": r["username"], "count": r["c"]}
                                    for r in top_ed],
    }
