"""nc.routes.insights — die Routen unter /api/insights als Flask-Blueprint.

Welle 3 der Zerlegung (siehe docs/MODULARISIERUNG.md), erzeugt mit
tools/bp_extract.py. Pfade stehen woertlich in den Dekoratoren (kein
url_prefix); app-weite Hooks bleiben auf der App; was der Monolith weiterhin
stellen muss, kommt ueber nc.ctx statt ueber einen Import aus bot.py.
"""

from flask import Blueprint, jsonify

from nc import fehlertext as _nc_fehlertext
from nc.textmore import _parse_iso
from nc.dbwrap import db_conn

from nc import ctx as _ctx

bp = Blueprint("insights", __name__)


def _fehler_text(e, wo=""):
    """v4.1-W30: der Wortlaut geht ins Log, nach aussen die gesaeuberte
       Fassung — ohne Pfade, ohne Zugangsdaten, gekuerzt. Siehe
       nc/fehlertext.py, dort steht auch, warum nicht einfach "interner
       Fehler"."""
    return _nc_fehlertext.nach_aussen(e, wo)


def _c():
    """Laufzeitkontext. Aufruf statt Modul-Konstante — der Kontext wird erst
       beim Bot-Start gefuellt."""
    return _ctx.get()


class _LazyLog:
    def __getattr__(self, name):
        return getattr(_c().log, name)


log = _LazyLog()


@bp.route("/api/insights/best-times/<username>")
def api_insights_best_times(username):
    """Beste Stunden/Wochentage um diesen Streamer live zu erwischen — aus den
       Startzeiten erfolgreicher Aufnahmeversuche (Live-Evidenz)."""
    try:
        with db_conn() as conn:
            rows = conn.execute(
                "SELECT started_at FROM recording_attempts "
                "WHERE username=? AND started_at IS NOT NULL", (username,)).fetchall()
        by_hour = [0] * 24
        by_dow = [0] * 7        # 0=Montag … 6=Sonntag
        total = 0
        for r in rows:
            dt = _parse_iso(r["started_at"])
            if not dt:
                continue
            by_hour[dt.hour] += 1
            by_dow[dt.weekday()] += 1
            total += 1
        top_hours = sorted(range(24), key=lambda h: by_hour[h], reverse=True)
        top_hours = [{"hour": h, "count": by_hour[h]} for h in top_hours if by_hour[h] > 0][:5]
        dow_names = ["Mo", "Di", "Mi", "Do", "Fr", "Sa", "So"]
        top_dows = sorted(range(7), key=lambda d: by_dow[d], reverse=True)
        top_dows = [{"day": dow_names[d], "count": by_dow[d]} for d in top_dows if by_dow[d] > 0][:3]
        rec = None
        if top_hours and top_dows:
            rec = f"{top_dows[0]['day']} gegen {top_hours[0]['hour']:02d}:00 Uhr"
        return jsonify(ok=True, username=username, samples=total,
                       top_hours=top_hours, top_days=top_dows, recommendation=rec)
    except Exception as e:
        return jsonify(ok=False, error=_fehler_text(e, "api_insights_best_times")), 500


@bp.route("/api/insights/reliability")
def api_insights_reliability():
    """Aufnahme-Zuverlässigkeit pro Streamer (ok-Quote), schlechteste zuerst."""
    try:
        with db_conn() as conn:
            rows = conn.execute(
                "SELECT username, COUNT(*) AS total, "
                "SUM(CASE WHEN outcome='ok' THEN 1 ELSE 0 END) AS ok "
                "FROM recording_attempts GROUP BY username "
                "HAVING COUNT(*) >= 1").fetchall()
        out = []
        for r in rows:
            total = int(r["total"] or 0)
            ok = int(r["ok"] or 0)
            rate = round(100.0 * ok / total, 1) if total else 0.0
            out.append({"username": r["username"], "attempts": total,
                        "successful": ok, "success_rate": rate})
        out.sort(key=lambda x: (x["success_rate"], -x["attempts"]))
        return jsonify(ok=True, streamers=out, count=len(out))
    except Exception as e:
        return jsonify(ok=False, error=_fehler_text(e, "api_insights_reliability")), 500


@bp.route("/api/insights/session-stats")
def api_insights_session_stats():
    """Live-Session-Dauer-Statistik pro Streamer aus aufgenommenen Dateien."""
    try:
        with db_conn() as conn:
            rows = conn.execute(
                "SELECT username, COUNT(*) AS n, "
                "AVG(duration_secs) AS avg_s, MAX(duration_secs) AS max_s, "
                "SUM(duration_secs) AS sum_s "
                "FROM recordings WHERE deleted_at IS NULL AND duration_secs IS NOT NULL "
                "GROUP BY username").fetchall()
        out = []
        for r in rows:
            out.append({
                "username": r["username"],
                "recordings": int(r["n"] or 0),
                "avg_minutes": round((r["avg_s"] or 0) / 60.0, 1),
                "max_minutes": round((r["max_s"] or 0) / 60.0, 1),
                "total_hours": round((r["sum_s"] or 0) / 3600.0, 1),
            })
        out.sort(key=lambda x: x["total_hours"], reverse=True)
        return jsonify(ok=True, streamers=out, count=len(out))
    except Exception as e:
        return jsonify(ok=False, error=_fehler_text(e, "api_insights_session_stats")), 500


@bp.route("/api/insights/growth/<username>")
def api_insights_growth(username):
    """Follower-/Heart-Wachstum aus profile_snapshots (Delta + Tagesrate)."""
    try:
        with db_conn() as conn:
            rows = conn.execute(
                "SELECT follower_count, heart_count, captured_at FROM profile_snapshots "
                "WHERE username=? ORDER BY captured_at ASC", (username,)).fetchall()
        if len(rows) < 2:
            return jsonify(ok=True, username=username, snapshots=len(rows),
                           note="Zu wenige Snapshots für Wachstums-Analyse.")
        first, last = rows[0], rows[-1]
        d_follow = (last["follower_count"] or 0) - (first["follower_count"] or 0)
        d_heart = (last["heart_count"] or 0) - (first["heart_count"] or 0)
        t0, t1 = _parse_iso(first["captured_at"]), _parse_iso(last["captured_at"])
        days = max((t1 - t0).total_seconds() / 86400.0, 0.01) if (t0 and t1) else 1.0
        return jsonify(ok=True, username=username, snapshots=len(rows),
                       follower_delta=d_follow, heart_delta=d_heart,
                       days_span=round(days, 1),
                       followers_per_day=round(d_follow / days, 1),
                       current_followers=last["follower_count"])
    except Exception as e:
        return jsonify(ok=False, error=_fehler_text(e, "api_insights_growth")), 500


@bp.route("/api/insights/catch-rate")
def api_insights_catch_rate():
    """Anteil erkannter Lives die erfolgreich aufgenommen wurden (gesamt)."""
    try:
        with db_conn() as conn:
            row = conn.execute(
                "SELECT COUNT(*) AS total, "
                "SUM(CASE WHEN outcome='ok' THEN 1 ELSE 0 END) AS ok "
                "FROM recording_attempts").fetchone()
        total = int(row["total"] or 0)
        ok = int(row["ok"] or 0)
        rate = round(100.0 * ok / total, 1) if total else 0.0
        return jsonify(ok=True, total_attempts=total, successful=ok,
                       catch_rate=rate)
    except Exception as e:
        return jsonify(ok=False, error=_fehler_text(e, "api_insights_catch_rate")), 500


@bp.route("/api/insights/activity-clock")
def api_insights_activity_clock():
    """Globale Live-Aktivität nach Tagesstunde (über alle Streamer) — für
       Kapazitätsplanung: wann laufen die meisten Aufnahmen gleichzeitig."""
    try:
        with db_conn() as conn:
            rows = conn.execute(
                "SELECT started_at FROM recording_attempts "
                "WHERE started_at IS NOT NULL").fetchall()
        by_hour = [0] * 24
        for r in rows:
            dt = _parse_iso(r["started_at"])
            if dt:
                by_hour[dt.hour] += 1
        peak = max(range(24), key=lambda h: by_hour[h]) if any(by_hour) else None
        return jsonify(ok=True, by_hour=by_hour, peak_hour=peak,
                       total=sum(by_hour))
    except Exception as e:
        return jsonify(ok=False, error=_fehler_text(e, "api_insights_activity_clock")), 500


@bp.route("/api/insights/leaderboard")
def api_insights_leaderboard():
    """Komposit-Ranking der Streamer: Aktivität (Versuche) × Zuverlässigkeit
       (ok-Quote) × Popularität (Follower). Score 0-100, höchste zuerst."""
    try:
        with db_conn() as conn:
            rows = conn.execute(
                "SELECT username, COUNT(*) AS total, "
                "SUM(CASE WHEN outcome='ok' THEN 1 ELSE 0 END) AS ok "
                "FROM recording_attempts GROUP BY username").fetchall()
            data = []
            max_act = 1
            max_pop = 1
            for r in rows:
                total = int(r["total"] or 0)
                ok = int(r["ok"] or 0)
                pop = _c().latest_popularity(conn, r["username"])
                max_act = max(max_act, total)
                max_pop = max(max_pop, pop)
                data.append({"username": r["username"], "attempts": total,
                             "ok": ok, "followers": pop})
        out = []
        for d in data:
            rel = (d["ok"] / d["attempts"]) if d["attempts"] else 0.0
            act = d["attempts"] / max_act
            pop = d["followers"] / max_pop
            score = round(100.0 * (0.4 * act + 0.35 * rel + 0.25 * pop), 1)
            out.append({**d, "reliability": round(rel * 100, 1), "score": score})
        out.sort(key=lambda x: x["score"], reverse=True)
        return jsonify(ok=True, leaderboard=out[:50], count=len(out))
    except Exception as e:
        return jsonify(ok=False, error=_fehler_text(e, "api_insights_leaderboard")), 500


@bp.route("/api/insights/storage-by-streamer")
def api_insights_storage_by_streamer():
    """Belegter Speicher pro Streamer (GB), größte zuerst."""
    try:
        with db_conn() as conn:
            rows = conn.execute(
                "SELECT username, COUNT(*) AS n, SUM(file_size) AS bytes "
                "FROM recordings WHERE deleted_at IS NULL "
                "GROUP BY username").fetchall()
        out = [{"username": r["username"], "recordings": int(r["n"] or 0),
                "gb": round((r["bytes"] or 0) / 1024 / 1024 / 1024, 2)}
               for r in rows]
        out.sort(key=lambda x: x["gb"], reverse=True)
        total_gb = round(sum(x["gb"] for x in out), 2)
        return jsonify(ok=True, streamers=out, total_gb=total_gb, count=len(out))
    except Exception as e:
        return jsonify(ok=False, error=_fehler_text(e, "api_insights_storage_by_streamer")), 500
