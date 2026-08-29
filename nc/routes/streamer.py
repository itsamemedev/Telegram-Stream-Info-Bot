"""nc.routes.streamer — die Routen unter /api/streamer,/api/streamers als Flask-Blueprint.

Welle 3 der Zerlegung (siehe docs/MODULARISIERUNG.md), erzeugt mit
tools/bp_extract.py. Pfade stehen woertlich in den Dekoratoren (kein
url_prefix); app-weite Hooks bleiben auf der App; was der Monolith weiterhin
stellen muss, kommt ueber nc.ctx statt ueber einen Import aus bot.py.
"""

from datetime import datetime, timedelta, timezone
import os
from flask import Blueprint, jsonify, request
from nc.dbwrap import db_conn
from nc import tiktokcheck as _nc_tiktokcheck
from nc import trackingdb as _nc_trackingdb
from nc.trackingdb import get_all_active_trackings
from nc.util import _loop_not_ready
from nc.stats import _streamer_health

from nc import ctx as _ctx

bp = Blueprint("streamer", __name__)


def _c():
    """Laufzeitkontext. Aufruf statt Modul-Konstante — der Kontext wird erst
       beim Bot-Start gefuellt."""
    return _ctx.get()


class _LazyLog:
    def __getattr__(self, name):
        return getattr(_c().log, name)


log = _LazyLog()


@bp.route("/api/streamers/wall")
def api_streamers_wall():
    """F92: Angereicherte Streamer-Kacheln für die Monitor-Wall: Live-/Rec-
       Status + Aufnahmen-Gesamt + letzte Aufnahme + Avatar (best-effort aus
       Redis-Cache, kein TikTok-Call). Live-Kacheln zuerst."""
    try:
        rows = get_all_active_trackings(include_paused=True)
    except Exception as e:
        return jsonify(ok=False, error=str(e)), 500
    counts, lasts = {}, {}
    try:
        with db_conn() as conn:
            for r in conn.execute("SELECT username, COUNT(*) AS n, MAX(created_at) AS last "
                                  "FROM recordings GROUP BY username").fetchall():
                counts[r["username"]] = r["n"]
                lasts[r["username"]] = (r["last"] or "")[:16].replace("T", " ")
    except Exception:
        pass
    tiles = []
    for t in rows:
        u = t["username"]
        tiles.append({
            "username": u,
            "live": bool(t["last_live"]), "recording": bool(t["recording"]),
            "paused": bool(t["paused"]) if "paused" in t.keys() else False,
            "source": ("discord" if (_c().cfg["DISCORD_GUILD_ID"] and t["group_id"] == _c().cfg["DISCORD_GUILD_ID"]) else "telegram"),
            "recs": counts.get(u, 0), "last_rec": lasts.get(u, ""),
        })
    tiles.sort(key=lambda x: (not x["live"], not x["recording"], -x["recs"], x["username"].lower()))
    return jsonify(ok=True, tiles=tiles, live=sum(1 for t in tiles if t["live"]), total=len(tiles))


@bp.route("/api/streamer/detail")
def api_streamer_detail():
    raw = (request.args.get("user") or "").lstrip("@").strip()
    if not raw:
        return jsonify(ok=False, error="user fehlt"), 400
    # WARUM case-insensitiv: clean_username macht KEIN lower(), die trackings
    # speichern den Handle also so, wie er getippt wurde ("@RabiLive"). Diese
    # Route hat stur .lower() angewendet — bei jedem Handle mit Großbuchstaben
    # traf keine einzige Abfrage: die Streamer-Karte zeigte OFFLINE, 0
    # Aufnahmen, keine Kapitel, obwohl der Streamer gerade sendete. Genau das
    # sah im Dashboard aus wie "der hinzugefügte Streamer zählt nirgends".
    user = _nc_trackingdb.resolve_tracked_user(raw)
    live_key = _nc_trackingdb.ci_key(_c().cfg["_LIVE_SESSION_START"], user)
    tier_key = _nc_trackingdb.ci_key(_c().cfg["_ACTIVE_TIER"], user)
    out = {"ok": True, "user": user,
           "tier": _c().cfg["_ACTIVE_TIER"].get(tier_key) if tier_key else None,
           "live": bool(live_key), "recordings": [], "chapters": [], "rec_total": 0}
    try:
        with db_conn() as conn:
            recs = conn.execute("SELECT filepath, created_at FROM recordings "
                                "WHERE LOWER(username)=LOWER(?) "
                                "ORDER BY id DESC LIMIT 10", (user,)).fetchall()
            out["recordings"] = [{"file": os.path.basename(r["filepath"] or ""),
                                  "at": (r["created_at"] or "")[:16].replace("T", " ")} for r in recs]
            out["rec_total"] = conn.execute("SELECT COUNT(*) AS c FROM recordings "
                                            "WHERE LOWER(username)=LOWER(?)",
                                            (user,)).fetchone()["c"]
            chaps = conn.execute("SELECT offset_secs, title, reason, created_at FROM stream_chapters "
                                 "WHERE LOWER(username)=LOWER(?) "
                                 "ORDER BY id DESC LIMIT 8", (user,)).fetchall()
            out["chapters"] = [{"offset": c["offset_secs"] or 0,
                                "title": c["title"] or c["reason"] or "Moment",
                                "at": (c["created_at"] or "")[:16].replace("T", " ")} for c in chaps]
    except Exception as e:
        out["db_error"] = str(e)
    return jsonify(out)


@bp.route("/api/streamer/compare")
def api_streamer_compare():
    """Vergleicht zwei Streamer Seite an Seite. ?a=user1&b=user2"""
    a = (request.args.get("a") or "").lstrip("@")
    b = (request.args.get("b") or "").lstrip("@")
    if not a or not b:
        return jsonify(ok=False, error="a und b erforderlich"), 400
    try:
        with db_conn() as conn:
            def stats(u):
                h = _streamer_health(u, conn)
                rec = conn.execute(
                    "SELECT COUNT(*) AS n, COALESCE(SUM(file_size),0)/1048576.0 AS mb, "
                    "COALESCE(SUM(duration_secs),0) AS dur FROM recordings WHERE username=?",
                    (u,)).fetchone()
                h.update({"recordings": int(rec["n"] or 0), "total_mb": round(rec["mb"] or 0),
                          "total_minutes": round((rec["dur"] or 0) / 60.0)})
                return h
            return jsonify(ok=True, a={"username": a, **stats(a)},
                           b={"username": b, **stats(b)})
    except Exception as e:
        return jsonify(ok=False, error=str(e)), 500


@bp.route("/api/streamer/priority/<username>", methods=["GET", "POST"])
def api_streamer_priority(username):
    """Liest/setzt die Prioritätsstufe (0=normal,1=high,2=vip) eines Streamers.
       Beeinflusst Polling/Retry. POST body: {"level":2}"""
    username = username.lstrip("@")
    try:
        with db_conn() as conn:
            tr = conn.execute("SELECT id FROM trackings WHERE username=? LIMIT 1",
                              (username,)).fetchone()
            if not tr:
                return jsonify(ok=False, error="streamer not tracked"), 404
            tid = tr["id"]
            if request.method == "POST":
                data = request.get_json(silent=True) or {}
                level = int(data.get("level", 0))
                if level not in (0, 1, 2):
                    return jsonify(ok=False, error="level muss 0,1,2 sein"), 400
                now = datetime.now(timezone.utc).isoformat()
                cur = conn.execute("UPDATE tracking_priority SET priority_level=?, updated_at=? "
                                   "WHERE tracking_id=?", (level, now, tid))
                if getattr(cur, "rowcount", 0) in (0, -1):
                    if not conn.execute("SELECT 1 FROM tracking_priority WHERE tracking_id=?",
                                        (tid,)).fetchone():
                        conn.execute("INSERT INTO tracking_priority (tracking_id, priority_level, updated_at) "
                                     "VALUES (?,?,?)", (tid, level, now))
                conn.commit()
                return jsonify(ok=True, username=username, level=level)
            row = conn.execute("SELECT priority_level FROM tracking_priority WHERE tracking_id=?",
                               (tid,)).fetchone()
            return jsonify(ok=True, username=username,
                           level=int(row["priority_level"]) if row else 0)
    except Exception as e:
        return jsonify(ok=False, error=str(e)), 500


@bp.route("/api/streamer/journal/<username>")
def api_streamer_journal(username):
    """Aktivitäts-Journal eines Streamers: jüngste Versuche + Aufnahmen,
       chronologisch gemischt."""
    username = username.lstrip("@")
    try:
        items = []
        with db_conn() as conn:
            for r in conn.execute(
                    "SELECT started_at AS at, outcome, duration_secs FROM recording_attempts "
                    "WHERE username=? ORDER BY started_at DESC LIMIT 40", (username,)).fetchall():
                items.append({"at": r["at"], "type": "attempt", "outcome": r["outcome"],
                              "duration_secs": r["duration_secs"]})
            for r in conn.execute(
                    "SELECT created_at AS at, file_size, duration_secs FROM recordings "
                    "WHERE username=? ORDER BY created_at DESC LIMIT 40", (username,)).fetchall():
                items.append({"at": r["at"], "type": "recording",
                              "mb": round((r["file_size"] or 0) / 1048576.0, 1),
                              "duration_secs": r["duration_secs"]})
        items.sort(key=lambda x: x["at"] or "", reverse=True)
        return jsonify(ok=True, username=username, count=len(items), journal=items[:60])
    except Exception as e:
        return jsonify(ok=False, error=str(e)), 500


@bp.route("/api/streamer/watchlist")
def api_streamer_watchlist():
    """Alle getrackten Streamer mit Prioritätsstufe + Health-Score."""
    try:
        out = []
        with db_conn() as conn:
            rows = conn.execute(
                "SELECT t.username, t.paused, COALESCE(p.priority_level,0) AS lvl "
                "FROM trackings t LEFT JOIN tracking_priority p ON p.tracking_id=t.id "
                "ORDER BY lvl DESC, t.username ASC").fetchall()
            for r in rows:
                h = _streamer_health(r["username"], conn)
                out.append({"username": r["username"], "paused": bool(r["paused"]),
                            "priority": int(r["lvl"]), "health": h["score"],
                            "grade": h["grade"], "ok_rate": h["ok_rate"]})
        return jsonify(ok=True, count=len(out), watchlist=out)
    except Exception as e:
        return jsonify(ok=False, error=str(e)), 500


@bp.route("/api/streamer/dormant")
def api_streamer_dormant():
    """Streamer ohne Aktivität seit N Tagen (?days=14) — Drop-Kandidaten."""
    # BUG-FIX: int() auf ungültigem Query-Parameter (z.B. "days=abc") wirft
    # ValueError → unkontrollierter 500. Außerdem: extrem große Werte (days=999999)
    # erzeugen einen datetime vor Unix-Epoch → SQLite gibt falsche Ergebnisse.
    try:
        days = _c().arg_int("days", 14, 1, 3650)
    except (ValueError, TypeError):
        return jsonify(ok=False, error="days muss eine ganze Zahl sein (1–3650)"), 400
    try:
        cut = (datetime.now(timezone.utc) - timedelta(days=days)).isoformat()
        with db_conn() as conn:
            rows = conn.execute(
                "SELECT t.username, MAX(a.started_at) AS last FROM trackings t "
                "LEFT JOIN recording_attempts a ON a.username=t.username "
                "WHERE t.paused=0 GROUP BY t.username HAVING last IS NULL OR last < ? "
                "ORDER BY last ASC", (cut,)).fetchall()
        out = [{"username": r["username"], "last_activity": r["last"]} for r in rows]
        return jsonify(ok=True, count=len(out), days=days, dormant=out)
    except Exception as e:
        return jsonify(ok=False, error=str(e)), 500


@bp.route("/api/streamer/exists/<username>")
def api_streamer_exists(username):
    """Konservativer Existenz-Check eines TikTok-Accounts. deletable=True nur,
    wenn TikTok den Account eindeutig als nicht (mehr) vorhanden meldet."""
    uname = (username or "").lstrip("@").strip()
    if not uname:
        return jsonify(ok=False, error="kein Name"), 400
    try:
        status, http_status, detail = _c().run_async(
            _nc_tiktokcheck.account_exists(uname), timeout=25)
    except Exception as e:
        if _loop_not_ready(e):
            return jsonify(ok=False, error="Bot startet noch — gleich erneut"), 503
        return jsonify(ok=False, error=str(e)), 500
    return jsonify(ok=True, username=uname, status=status,
                   http_status=http_status, detail=detail,
                   deletable=(status == "gone"))


@bp.route("/api/streamer/delete/<username>", methods=["POST"])
def api_streamer_delete(username):
    """Entfernt ALLE Trackings eines Streamers (über alle Gruppen) inkl. der
    in-memory-States (remove_tracking cleant die). Gedacht für Accounts, die es
    auf TikTok nicht mehr gibt — die UI ruft das erst nach Bestätigung auf."""
    uname = (username or "").lstrip("@").strip()
    if not uname:
        return jsonify(ok=False, error="kein Name"), 400
    try:
        with db_conn() as conn:
            rows = conn.execute(
                "SELECT DISTINCT group_id FROM trackings WHERE username=?",
                (uname,)).fetchall()
        groups = [r["group_id"] for r in rows]
        if not groups:
            return jsonify(ok=False, error="kein Tracking für diesen Namen"), 404
        for gid in groups:
            _nc_trackingdb.remove_tracking(gid, uname)
        log.info("Streamer @%s via Dashboard gelöscht (%d Tracking(s)).",
                 uname, len(groups))
        return jsonify(ok=True, username=uname, deleted=len(groups))
    except Exception as e:
        return jsonify(ok=False, error=str(e)), 500


@bp.route("/api/streamer/digest/<username>")
def api_streamer_digest(username):
    """Konsolidiertes Streamer-Profil in EINEM Call: Health, Volumen,
       Top-Zeiten, dominanter Fehler — für die Per-Streamer-Ansicht."""
    username = username.lstrip("@")
    try:
        with db_conn() as conn:
            health = _streamer_health(username, conn)
            rec = conn.execute(
                "SELECT COUNT(*) AS n, COALESCE(SUM(file_size),0)/1048576.0 AS mb, "
                "COALESCE(SUM(duration_secs),0) AS dur, MAX(created_at) AS last "
                "FROM recordings WHERE username=?", (username,)).fetchone()
            domfail = conn.execute(
                "SELECT outcome, COUNT(*) AS n FROM recording_attempts WHERE username=? "
                "AND outcome NOT IN ('ok','stall_killed_partial','running','cancelled') "
                "GROUP BY outcome ORDER BY n DESC LIMIT 1", (username,)).fetchone()
        return jsonify(ok=True, username=username, health=health,
                       recordings={"count": int(rec["n"] or 0),
                                   "total_mb": round(rec["mb"] or 0),
                                   "total_minutes": round((rec["dur"] or 0) / 60.0),
                                   "last": rec["last"]},
                       dominant_failure=(domfail["outcome"] if domfail else None))
    except Exception as e:
        return jsonify(ok=False, error=str(e)), 500
