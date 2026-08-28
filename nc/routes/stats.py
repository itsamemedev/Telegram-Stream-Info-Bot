"""nc.routes.stats — die Routen unter /api/stats,/api/ai-log,/api/moderation als Flask-Blueprint.

Welle 3 der Zerlegung (siehe docs/MODULARISIERUNG.md), erzeugt mit
tools/bp_extract.py. Pfade stehen woertlich in den Dekoratoren (kein
url_prefix); app-weite Hooks bleiben auf der App; was der Monolith weiterhin
stellen muss, kommt ueber nc.ctx statt ueber einen Import aus bot.py.
"""

from datetime import datetime, timedelta, timezone
import json
import re
from flask import Blueprint, jsonify
from nc.dbwrap import db_conn
from nc.stats import get_stats, get_tiktok_status_distribution

from nc import ctx as _ctx

bp = Blueprint("stats", __name__)


def _c():
    """Laufzeitkontext. Aufruf statt Modul-Konstante — der Kontext wird erst
       beim Bot-Start gefuellt."""
    return _ctx.get()


class _LazyLog:
    def __getattr__(self, name):
        return getattr(_c().log, name)


log = _LazyLog()


_FAILURE_PATTERNS = [
    ("403/Forbidden",       re.compile(r"\b403\b|forbidden", re.I)),
    ("Connection-Timeout",  re.compile(r"connection.*timed out|timed out", re.I)),
    ("HTTP-404 (stream)",   re.compile(r"http.{0,3}error.{0,3}404|not found", re.I)),
    ("DNS/Network",         re.compile(r"name resolution|dns|unable to find", re.I)),
    ("Broken-Pipe",         re.compile(r"broken pipe|epipe", re.I)),
    ("Codec-Error",         re.compile(r"invalid data found|codec.*not.*found", re.I)),
    ("Moov-Missing",        re.compile(r"moov atom not found", re.I)),
    ("Bitstream-Error",     re.compile(r"non-monotonous dts|aac.*adts", re.I)),
    ("TLS-Handshake",       re.compile(r"ssl|tls|certificate", re.I)),
    ("Rate-Limit (429)",    re.compile(r"\b429\b|too many requests", re.I)),
]


def get_recent_ai_log(limit=50):
    try:
        with db_conn() as conn:
            return conn.execute(
                "SELECT id, chat_id, user_id, prompt, response, model, duration_ms, "
                "error, file_kind, file_size, created_at "
                "FROM ai_log ORDER BY id DESC LIMIT ?", (limit,)
            ).fetchall()
    except Exception as e:
        log.warning(f"get_recent_ai_log failed: {e}")
        return []


def cluster_failures(hours: int = 24) -> dict:
    """Liest stderr_tail der letzten N Stunden, gruppiert nach Pattern."""
    hours = max(1, min(int(hours or 24), 168))
    since = (datetime.now(timezone.utc) - timedelta(hours=hours)).isoformat()
    counts = {label: 0 for label, _ in _FAILURE_PATTERNS}
    counts["Unknown"] = 0
    total_failures = 0
    examples = {}    # pattern -> example stderr-snippet
    try:
        with db_conn() as conn:
            rows = conn.execute(
                "SELECT username, stderr_tail FROM recording_attempts "
                "WHERE started_at >= ? "
                "  AND outcome NOT IN ('ok', 'stall_killed_partial', 'running') "
                "ORDER BY id DESC LIMIT 500",
                (since,)).fetchall()
    except Exception as e:
        return {"hours": hours, "total": 0, "error": str(e), "patterns": []}
    for r in rows:
        tail = r["stderr_tail"] or ""
        total_failures += 1
        matched = False
        for label, regex in _FAILURE_PATTERNS:
            if regex.search(tail):
                counts[label] += 1
                if label not in examples:
                    examples[label] = (r["username"], tail[-150:].strip())
                matched = True
                break
        if not matched and tail.strip():
            counts["Unknown"] += 1
    patterns = []
    for label, _ in _FAILURE_PATTERNS + [("Unknown", None)]:
        if counts.get(label, 0) > 0:
            example = examples.get(label)
            patterns.append({
                "label": label,
                "count": counts[label],
                "pct": round(100.0 * counts[label] / total_failures, 1) if total_failures else 0,
                "example_user": example[0] if example else None,
                "example_snippet": example[1] if example else None,
            })
    patterns.sort(key=lambda x: -x["count"])
    return {"hours": hours, "total": total_failures, "patterns": patterns}


@bp.route("/api/stats")
def api_stats(lean: bool = False):
    """lean=True (aus /api/pulse): nur die drei billigen, indizierten Zaehler.
       Die teuren Gesamt-Aggregate ueber tiktok_checks bleiben weg — der
       Header zeigt sie ohnehin nicht (siehe Kommentar an get_stats)."""
    if lean:
        with db_conn() as conn:
            active_t = conn.execute("SELECT COUNT(*) FROM trackings").fetchone()[0]
            live_now = conn.execute("SELECT COUNT(*) FROM trackings WHERE last_live=1").fetchone()[0]
            creators = conn.execute(
                "SELECT COUNT(DISTINCT username) FROM trackings").fetchone()[0]
            rec_count = conn.execute(
                "SELECT COUNT(*) FROM recordings WHERE deleted_at IS NULL").fetchone()[0]
        return jsonify(active_trackings=active_t, live_now=live_now,
                       creators=creators, recordings_count=rec_count, lean=True)
    total, unique_users, top = get_stats()
    with db_conn() as conn:
        active_t = conn.execute("SELECT COUNT(*) FROM trackings").fetchone()[0]
        live_now = conn.execute("SELECT COUNT(*) FROM trackings WHERE last_live=1").fetchone()[0]
        # Die Kachel "Creator" zeigte bisher unique_users — das sind DISTINCT
        # telegram_user_id aus tiktok_checks, also die Menschen, die mal /check
        # getippt haben. Ein neu getrackter Streamer änderte daran nichts, die
        # Zahl stand tage- bis wochenlang still. "Creator" sind die getrackten
        # Handles; unique_users bleibt für die Checks-Kachel erhalten.
        creators = conn.execute(
            "SELECT COUNT(DISTINCT username) FROM trackings").fetchone()[0]
        # BUG-FIX (Konsistenz): soft-deleted (X19 Trash) ausschließen. Vorher
        # zählte stats ALLE recordings, während get_all_recordings / overview /
        # captures-Liste gelöschte ausschließen → Header-Count wich nach dem
        # In-den-Papierkorb-Verschieben von der sichtbaren Liste ab.
        rec_count = conn.execute(
            "SELECT COUNT(*) FROM recordings WHERE deleted_at IS NULL").fetchone()[0]
    return jsonify(total_checks=total, unique_users=unique_users, creators=creators,
                   top=[{"username": r["username"], "count": r["cnt"]} for r in top],
                   active_trackings=active_t, live_now=live_now, recordings_count=rec_count)


@bp.route("/api/ai-log/<int:entry_id>")
def api_ai_log_detail(entry_id):
    """Volle prompt + response für einen AI-Log-Eintrag. Wird vom Modal
       gefetched wenn der Operator auf eine Zeile klickt."""
    with db_conn() as conn:
        row = conn.execute(
            "SELECT id, created_at, chat_id, user_id, prompt, response, "
            "  model, duration_ms, error, file_kind, file_size "
            "FROM ai_log WHERE id=?",
            (entry_id,)).fetchone()
    if not row:
        return jsonify(ok=False, error="entry not found"), 404
    # B50: Cap bei 50KB pro Feld damit eine kaputte AI-Antwort den Browser
    # nicht crasht. 50KB ist mehr als genug für normale Chats.
    return jsonify({
        "ok": True,
        "id": row["id"],
        "created_at": row["created_at"],
        "chat_id": row["chat_id"],
        "user_id": row["user_id"],
        "prompt": (row["prompt"] or "")[:50000],
        "response": (row["response"] or "")[:50000],
        "model": row["model"],
        "duration_ms": row["duration_ms"],
        "error": row["error"],
        "file_kind": row["file_kind"],
        "file_size": row["file_size"],
    })


@bp.route("/api/ai-log")
def api_ai_log():
    """F16: letzte AI-Calls für Dashboard-Stream."""
    rows = get_recent_ai_log(limit=50)
    return jsonify([{
        "id": r["id"],
        "created_at": r["created_at"][:19] if r["created_at"] else "",
        "chat_id": r["chat_id"],
        "user_id": r["user_id"],
        "prompt": (r["prompt"] or "")[:200],
        "response_preview": (r["response"] or "")[:200] if r["response"] else None,
        "model": r["model"],
        "duration_ms": r["duration_ms"],
        "error": r["error"],
        "file_kind": r["file_kind"],
        "file_size": r["file_size"],
    } for r in rows])


@bp.route("/api/stats/tiktok-status")
def api_tiktok_status():
    return jsonify(ok=True, **get_tiktok_status_distribution())


@bp.route("/api/stats/failures-by-pattern")
def api_failures_by_pattern():
    hours = _c().arg_int("hours", 24, 1, 168)
    return jsonify(ok=True, **cluster_failures(hours))


@bp.route("/api/moderation/feed")
def api_moderation_feed():
    """v4.0: plattformUEBERGREIFENDER Moderations-Feed (Kick/Twitch/YouTube) aus
       kick_mod_log. Macht „Moderator ueberall" sichtbar — welche Aktion, welche
       Plattform, welcher User, welcher Grund. Admin-Dashboard (kein oeffentl. Leak)."""
    try:
        hours = _c().arg_int("hours", 24, 1, 168)
    except (TypeError, ValueError):
        hours = 24
    try:
        limit = _c().arg_int("limit", 40, 1, 200)
    except (TypeError, ValueError):
        limit = 40
    cut = (datetime.now(timezone.utc) - timedelta(hours=hours)).isoformat()

    def _platform(actor):
        a = (actor or "").lower()
        if "twitch" in a:
            return "twitch"
        if "youtube" in a or "yt" in a:
            return "youtube"
        return "kick"

    items, counts = [], {"kick": 0, "twitch": 0, "youtube": 0}
    try:
        with db_conn() as c:
            rows = c.execute(
                "SELECT ts, kind, actor, content, meta FROM kick_mod_log "
                "WHERE ts >= ? AND kind IN ('timeout','ban','flag','delete','warn') "
                "ORDER BY ts DESC LIMIT ?", (cut, limit)).fetchall()
        for r in rows:
            try:
                meta = json.loads(r["meta"] or "{}")
            except Exception:
                meta = {}
            plat = _platform(r["actor"])
            counts[plat] = counts.get(plat, 0) + 1
            items.append({
                "ts": r["ts"], "platform": plat, "kind": r["kind"],
                "user": meta.get("user", ""), "cat": meta.get("cat", ""),
                "detail": meta.get("detail", ""),
                "note": meta.get("note", ""),
                "content": (r["content"] or "")[:160],
            })
    except Exception as e:
        return jsonify(ok=False, error=str(e)[:160]), 200
    return jsonify(ok=True, hours=hours, count=len(items), counts=counts, items=items)


@bp.route("/api/stats/timeline")
def api_stats_timeline():
    """Aktivitäts-Zeitreihe der letzten N Tage (?days=14): Versuche, Erfolge,
       Aufnahmen, MB — für ein Dashboard-Chart."""
    days = _c().arg_int("days", 14, 1, 90)
    try:
        out = []
        with db_conn() as conn:
            for i in range(days - 1, -1, -1):
                day = (datetime.now(timezone.utc) - timedelta(days=i)).date().isoformat()
                a = conn.execute(
                    "SELECT COUNT(*) AS att, "
                    "SUM(CASE WHEN outcome IN ('ok','stall_killed_partial') THEN 1 ELSE 0 END) AS ok "
                    "FROM recording_attempts WHERE date(started_at)=?", (day,)).fetchone()
                rec = conn.execute(
                    "SELECT COUNT(*) AS n, COALESCE(SUM(file_size),0)/1048576.0 AS mb "
                    "FROM recordings WHERE date(created_at)=?", (day,)).fetchone()
                out.append({"date": day, "attempts": int(a["att"] or 0),
                            "successes": int(a["ok"] or 0),
                            "recordings": int(rec["n"] or 0), "mb": round(rec["mb"] or 0)})
        return jsonify(ok=True, days=days, timeline=out)
    except Exception as e:
        return jsonify(ok=False, error=str(e)), 500
