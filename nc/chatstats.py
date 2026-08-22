"""nc.chatstats — v4.0-W45: reine Chat-Health-Aggregation, aus bot_v37 gelöst.

Verdichtet die rohen Verbindungs-Zähler je Chat-Listener zu den Kennzahlen, an
denen man Disconnect-Muster erkennt (Uptime-Quote, Median-/kürzeste/längste
Session, Flaps, letzte Trenngründe). Rein: das _CHAT_STATS-dict und die beiden
Zeitwerte (monoton + Wanduhr) kommen herein, ein Summary-dict geht raus —
bitgenau gegen den Monolithen geprüft.
"""


def summarize(stats, now_mono, now_wall):
    """{username -> Kennzahlen} fürs Dashboard. now_mono für die laufende
       Session (monotone Uhr), now_wall für Alter/Gründe (Wanduhr)."""
    out = {}
    for u, s in stats.items():
        ses = s["sessions"]
        live = bool(s["connected_since"])
        cur = (now_mono - s["connected_since"]) if live else 0.0
        span = max(1.0, now_wall - s["first_seen"])
        out[u] = {
            "connected": live,
            "current_session_s": round(cur),
            "connects": s["connects"], "failed": s["failed"],
            "disconnects": s["disconnects"], "flaps": s["flaps"],
            "median_session_s": round(sorted(ses)[len(ses) // 2]) if ses else 0,
            "shortest_s": round(min(ses)) if ses else 0,
            "longest_s": round(max(ses)) if ses else 0,
            # Uptime-Quote: der ehrlichste Einzelwert. 100% = nie getrennt.
            "uptime_pct": round(min(100.0, (s["total_uptime"] + cur) * 100.0 / span), 1),
            "backoff_s": s["backoff_s"],
            "last_reasons": [{"ago_s": round(now_wall - t), "why": w}
                             for t, w in reversed(s["reasons"])],
        }
    return out
