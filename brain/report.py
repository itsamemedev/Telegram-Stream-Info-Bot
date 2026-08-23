# brain/report.py — V37-W-PLUS: Wochenreport als Markdown.
# Aggregiert Memory (Sessions/Metriken), Wissensgraph, Regel-Feuerungen und
# Agenten-Läufe der letzten 7 Tage. Reine Leseoperationen auf brain.db.

from __future__ import annotations

import time
from datetime import datetime, timezone


def _fmt_dur(s: float) -> str:
    s = int(s or 0)
    if s >= 3600:
        return f"{s // 3600}h{(s % 3600) // 60:02d}m"
    return f"{s // 60}m"


def weekly(brain, days: int = 7) -> str:
    """Markdown-Report. Fehlertolerant: jede Sektion isoliert."""
    since = time.time() - days * 86400
    now = datetime.now(timezone.utc).strftime("%d.%m.%Y %H:%M UTC")
    out = [f"# NIGHTCRAWLER Wochenreport\n\n*Erstellt {now} · Zeitraum: letzte {days} Tage*\n"]

    # --- Sessions pro Streamer ------------------------------------------
    try:
        with brain._db_lock, brain._conn() as c:
            rows = c.execute(
                "SELECT username, COUNT(*) n, SUM(duration_s) dur, "
                "SUM(recorded) rec FROM stream_sessions "
                "WHERE started >= ? AND ended IS NOT NULL "
                "GROUP BY username ORDER BY dur DESC LIMIT 15",
                (since,)).fetchall()
        out.append("## Streams\n")
        if rows:
            out.append("| Streamer | Sessions | Sendezeit | Aufgezeichnet |")
            out.append("|---|---|---|---|")
            for u, n, dur, rec in rows:
                out.append(f"| @{u} | {n} | {_fmt_dur(dur)} | {rec}/{n} |")
            total_n = sum(r[1] for r in rows)
            total_d = sum(r[2] or 0 for r in rows)
            out.append(f"\n**Gesamt:** {total_n} Sessions · {_fmt_dur(total_d)} "
                       f"beobachtete Livezeit.\n")
        else:
            out.append("*Keine abgeschlossenen Sessions im Zeitraum.*\n")
    except Exception as e:
        out.append(f"*Sessions nicht lesbar: {e}*\n")

    # --- Systemlast -------------------------------------------------------
    try:
        with brain._db_lock, brain._conn() as c:
            cpu = c.execute("SELECT AVG(value), MAX(value) FROM metrics "
                            "WHERE name='cpu' AND ts >= ?", (since,)).fetchone()
            dsk = c.execute("SELECT MAX(value) FROM metrics "
                            "WHERE name='disk_pct' AND ts >= ?", (since,)).fetchone()
            rst = c.execute("SELECT MAX(value) FROM metrics "
                            "WHERE name='restreams_running' AND ts >= ?",
                            (since,)).fetchone()
        out.append("## System\n")
        if cpu and cpu[0] is not None:
            out.append(f"- CPU: Ø {cpu[0]:.0%} · Peak {cpu[1]:.0%}")
        if dsk and dsk[0] is not None:
            out.append(f"- Disk-Peak: {dsk[0]:.0f}%")
        if rst and rst[0] is not None:
            out.append(f"- Max. parallele Restreams: {int(rst[0])}")
        try:
            with brain._db_lock, brain._conn() as c:
                rc = c.execute("SELECT MAX(value)-MIN(value) FROM metrics "
                               "WHERE name='listener_reconnects' AND ts >= ?",
                               (since,)).fetchone()[0]
            if rc:
                out.append(f"- Chat-Listener-Reconnects: {int(rc)} "
                           f"{'⚠ (instabil)' if rc > 20 else ''}".rstrip())
        except Exception:
            pass
        try:
            with brain._db_lock, brain._conn() as c:
                paused = c.execute("SELECT COALESCE(SUM(value),0) FROM metrics "
                                   "WHERE name='sources_auto_paused' AND ts>=?",
                                   (since,)).fetchone()[0]
                react = c.execute("SELECT COALESCE(SUM(value),0) FROM metrics "
                                  "WHERE name='sources_reactivated' AND ts>=?",
                                  (since,)).fetchone()[0]
            if paused or react:
                out.append(f"- Tote Quellen: {int(paused)} auto-pausiert, "
                           f"{int(react)} reaktiviert (zweite Chance)")
        except Exception:
            pass
        out.append("")
    except Exception as e:
        out.append(f"*Metriken nicht lesbar: {e}*\n")

    # --- Recorder-Preflight (CDN-404-Quirk) -------------------------------
    try:
        with brain._db_lock, brain._conn() as c:
            def _delta(name):
                r = c.execute("SELECT MAX(value)-MIN(value) FROM metrics "
                              "WHERE name=? AND ts >= ?", (name, since)).fetchone()[0]
                return int(r) if r else 0
            fb, dead = _delta("preflight_fallback"), _delta("preflight_dead")
        if fb or dead:
            out.append("## Recorder-Preflight\n")
            if fb:
                out.append(f"- **{fb}×** tote HD-URL erkannt und auf "
                           f"funktionierende Variante umgeschwenkt (spart je "
                           f"~30–60s ffmpeg-Reconnect)")
            if dead:
                out.append(f"- {dead}× Quelle komplett tot → kein Spawn "
                           f"(Battle-Stage/offline)")
            out.append("")
    except Exception:
        pass

    # --- Regel-Feuerungen (Warum-Log) ------------------------------------
    try:
        with brain._db_lock, brain._conn() as c:
            rows = c.execute(
                "SELECT rule, COUNT(*) FROM decisions WHERE ts >= ? "
                "GROUP BY rule ORDER BY 2 DESC LIMIT 12", (since,)).fetchall()
        out.append("## Entscheidungen (Rules Engine)\n")
        if rows:
            for rule, n in rows:
                out.append(f"- `{rule}` — {n}×")
        else:
            out.append("*Keine Regel-Feuerungen — ruhige Woche.*")
        out.append("")
    except Exception as e:
        out.append(f"*Decisions nicht lesbar: {e}*\n")

    # --- SENTINEL-SHIELD --------------------------------------------------
    try:
        with brain._db_lock, brain._conn() as c:
            total = c.execute("SELECT COALESCE(SUM(value),0) FROM metrics "
                              "WHERE name='shield_blocks' AND ts >= ?",
                              (since,)).fetchone()[0]
            cats = {}
            for cat in ("doxxing", "hate", "drohung"):
                v = c.execute("SELECT COALESCE(SUM(value),0) FROM metrics "
                              "WHERE name=? AND ts >= ?",
                              (f"shield_{cat}", since)).fetchone()[0]
                if v:
                    cats[cat] = int(v)
        if total:
            out.append("## SENTINEL-SHIELD\n")
            out.append(f"- **{int(total)}** Angriffe abgewehrt "
                       f"(Doxxing/Hate/Drohung, vor KI)")
            if cats:
                out.append("- Aufschlüsselung: " + " · ".join(
                    f"{k.capitalize()} {v}" for k, v in cats.items()))
            out.append("")
    except Exception:
        pass

    # --- Prognose-Güte + Agenten ------------------------------------------
    try:
        with brain._db_lock, brain._conn() as c:
            br = c.execute("SELECT AVG(value), COUNT(*) FROM metrics "
                           "WHERE name='prediction_brier' AND ts >= ?",
                           (since,)).fetchone()
        if br and br[0] is not None:
            out.append(f"## Lernen\n- Brier-Score Ø {br[0]:.3f} "
                       f"({int(br[1])} Messungen; 0 = perfekt, 0.25 = Raten)\n")
    except Exception:
        pass
    try:
        ag = brain.agents.status()
        out.append("## AZRAEL-Agenten\n")
        for a in ag:
            out.append(f"- **{a['name']}**: {a['runs']} Läufe · "
                       f"{a['findings']} Findings · {a['errors']} Fehler")
        out.append("")
    except Exception:
        pass

    # --- Empfehlungen aus dem Wissensgraph --------------------------------
    try:
        recs = brain.knowledge.recommend(limit=3)
        if recs:
            out.append("## Empfehlungen\n")
            for r in recs:
                out.append(f"- **@{r['username']}** (Score {r['score']:.2f}): "
                           f"{r['why']}")
            out.append("")
    except Exception:
        pass

    return "\n".join(out) + "\n"
