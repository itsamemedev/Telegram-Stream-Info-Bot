"""nc.creatoragg — v4.0-W63: Aktivitäts-Zusammenfassung je getracktem Creator.

Rein: nimmt die recording_attempts-Zeilen des Fensters (username, started_at,
outcome) plus die Liste ALLER getrackten Usernamen und liefert je User eine
kompakte Bilanz — auch für inaktive (sessions=0). started_at ist ISO-8601, daher
sortieren Strings lexikalisch korrekt nach Zeit; der Tag ist einfach das
Datums-Präfix. Keine DB, kein I/O — der Aufrufer fragt ab und cacht. Testbar.
"""

from collections import defaultdict


def summarize(rows, tracked):
    """rows: iterierbar über dicts/Rows mit username, started_at (ISO), outcome.
       tracked: alle getrackten Usernamen (auch die ohne Aktivität im Fenster).
       → Liste je User: {username, sessions, active_days, last_seen, outcomes},
       sortiert nach Aktivität (meiste sessions zuerst), dann Name."""
    users = {}

    def _slot(u):
        return users.setdefault(u, {"username": u, "sessions": 0,
                                    "_days": set(), "last_seen": "",
                                    "_oc": defaultdict(int)})

    for r in rows:
        u = (_get(r, "username") or "").strip()
        if not u:
            continue
        st = str(_get(r, "started_at") or "")
        d = _slot(u)
        d["sessions"] += 1
        if st > d["last_seen"]:
            d["last_seen"] = st          # ISO-Strings sortieren zeitlich korrekt
        if st:
            d["_days"].add(st[:10])      # YYYY-MM-DD
        oc = (str(_get(r, "outcome") or "").strip() or "?")
        d["_oc"][oc] += 1

    for u in tracked:
        u = (u or "").strip()
        if u:
            _slot(u)                     # inaktive User mit sessions=0 aufnehmen

    out = []
    for u, d in users.items():
        out.append({
            "username": u,
            "sessions": d["sessions"],
            "active_days": len(d["_days"]),
            "last_seen": d["last_seen"],
            "outcomes": dict(d["_oc"]),
        })
    out.sort(key=lambda x: (-x["sessions"], x["username"].lower()))
    return out


def _get(row, key):
    """Feldzugriff für dict ODER sqlite3.Row."""
    try:
        return row[key]
    except Exception:
        return None
