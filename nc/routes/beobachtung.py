"""nc.routes.beobachtung — was der Bot ueber sich und die Streams berichtet.

Welle 3 der Zerlegung (siehe docs/MODULARISIERUNG.md). Pfade stehen woertlich
in den Dekoratoren (kein url_prefix); was der Monolith weiterhin stellen muss,
kommt ueber nc.ctx statt ueber einen Import aus bot.py.

v4.1-W23: Vier kleine Gruppen in EINEM Blueprint — /metrics,
/api/backoff-watch, /api/stream und /api/profile. Einzeln rechtfertigt keine
davon eine eigene Datei; zusammen haben sie eine klare Klammer: **sie
beobachten, sie steuern nichts.** Kein Aufruf hier startet, stoppt oder
loescht etwas.

**Null neue Kontext-Eintraege.** Der geteilte Zustand liegt in
nc/brainstate.py (Waechter-Zaehler), nc/channels.py (Zuschauer-Stichproben),
nc/restreamstate.py und nc/azraelstate.py. Was nur der laufende Bot kann —
den Redis-Cache lesen und schreiben, TikTok-Live-Infos holen, eine
Stream-URL aufloesen — kommt als Haken aus nc/restreamstate.py.
"""

import json
import os
import time
from datetime import datetime, timedelta, timezone
from typing import Optional


from flask import Blueprint, jsonify, request

from nc import azraelstate as _nc_azrael
from nc import fehlertext as _nc_fehlertext
from nc import brainstate as _nc_brainstate
from nc import channels as _nc_channels
from nc import i18n as _nc_i18n
from nc import restreamstate as _nc_rsstate
from nc import tiktokheaders as _nc_tthdr
from nc import trackingdb as _nc_trackingdb
from nc.dbwrap import db_conn
from nc.envnum import env_int as _env_int
from nc.textutil import clean_username
from nc.trackingdb import get_all_active_trackings

from nc import ctx as _ctx

bp = Blueprint("beobachtung", __name__)


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


def _t(s):
    """v4.1-W23: an der Quelle uebersetzen. Diese Texte erreichen das DOM
       meist verkettet ("Fehler: " + error) — ein Katalogeintrag fuer den
       blossen Text traefe dort nie."""
    return _nc_i18n.t(s)



def save_profile_snapshot(username: str, payload: dict) -> Optional[int]:
    """Persistiert einen Profile-Snapshot. follower_count etc. werden in
       eigene Spalten extrahiert für schnelle Diff-Queries."""
    try:
        with db_conn() as conn:
            cur = conn.execute(
                "INSERT INTO profile_snapshots "
                "(username, payload, follower_count, heart_count, video_count, captured_at) "
                "VALUES (?,?,?,?,?,?)",
                (username,
                 json.dumps(payload, ensure_ascii=False)[:50000],
                 payload.get("follower_count"),
                 payload.get("heart_count"),
                 payload.get("video_count"),
                 datetime.now(timezone.utc).isoformat()))
            conn.commit()
            return cur.lastrowid
    except Exception as e:
        _c().log.warning(f"save_profile_snapshot @{username}: {e}")
        return None


def get_profile_snapshots(username: str, limit: int = 50) -> list:
    try:
        with db_conn() as conn:
            return conn.execute(
                "SELECT id, follower_count, heart_count, video_count, captured_at "
                "FROM profile_snapshots WHERE username=? "
                "ORDER BY captured_at DESC LIMIT ?",
                (username, limit)).fetchall()
    except Exception:
        return []


async def inspect_stream_url(username: str, session=None) -> dict:
    """Probiert resolve_tiktok_live_stream und prüft die HLS-URL via HTTP HEAD.
       Liefert: ttfb, headers, resolved-format etc."""
    # Erst hier importiert, nicht auf Modulebene: nc/* muss ohne den vollen
    # Laufzeitstack importierbar bleiben — der CI-Job "Verträge & Module"
    # installiert nur orjson und flask und ist an genau diesem Import
    # gescheitert (W23). Lokal fiel es nicht auf, weil aiohttp hier liegt.
    import aiohttp

    username = clean_username(username)
    if not username:
        return {"ok": False, "error": _t("ungültiger username")}
    started = time.monotonic()
    own_session = False
    if session is None:
        session = aiohttp.ClientSession()
        own_session = True
    try:
        info = await _nc_rsstate.haken("resolve_live")(username, session, mode="auto")
        resolve_ms = int((time.monotonic() - started) * 1000)
        if not info:
            return {"ok": False, "error": _t("Aufloeser lieferte nichts"),
                    "resolve_ms": resolve_ms}
        url = info.get("hls_url") or info.get("flv_url")
        if not url:
            return {"ok": False, "error": _t("keine abspielbare URL im Ergebnis"),
                    "resolve_ms": resolve_ms,
                    "resolved": {"via": info.get("via")}}
        # HEAD request für TTFB
        head_started = time.monotonic()
        head_info = None
        try:
            async with session.get(url, headers=_nc_tthdr.HEADERS,
                                    timeout=aiohttp.ClientTimeout(total=10),
                                    allow_redirects=True) as resp:
                head_info = {
                    "status": resp.status,
                    "content_type": resp.headers.get("Content-Type"),
                    "content_length": resp.headers.get("Content-Length"),
                    "ttfb_ms": int((time.monotonic() - head_started) * 1000),
                }
                if resp.status == 200 and ".m3u8" in url.lower():
                    # m3u8-Playlist anschauen
                    text = await resp.text()
                    head_info["m3u8_lines"] = text.count("\n")
                    head_info["m3u8_segments"] = text.count(".ts")
        except Exception as e:
            head_info = {"error": _fehler_text(e, "inspect_stream_url")}
        return {
            "ok": True,
            "username": username,
            "resolve_ms": resolve_ms,
            "via": info.get("via"),
            "hls_url": info.get("hls_url"),
            "flv_url": info.get("flv_url"),
            "url_test": head_info,
        }
    finally:
        if own_session:
            try: await session.close()
            except Exception: pass


def _viewer_stats(since_ts=None):
    pts = [(t, c) for (t, c) in _nc_channels.VIEWER_SAMPLES if not since_ts or t >= since_ts]
    if not pts:
        return {"now": None, "peak": None, "avg": None, "points": []}
    vals = [c for _, c in pts]
    return {"now": vals[-1], "peak": max(vals),
            "avg": round(sum(vals) / len(vals)),
            "points": [{"t": int(t), "v": c} for t, c in pts[-120:]]}


@bp.route("/api/profile/<username>")
def api_profile(username):
    """Operator-Hover-Popup: alle Tracking-Stats + Recording-History pro Username.
       Aggregiert über ALLE Chats (ein User kann in mehreren Gruppen getrackt sein).
       Returns 404 wenn der Username gar nicht in der DB ist."""
    username = clean_username(username)
    if not username:
        return jsonify(ok=False, error=_t("ungültiger username")), 400
    with db_conn() as conn:
        # Tracking-Rows (kann mehrere Chats geben)
        trackings = conn.execute(
            "SELECT id, group_id, created_at, last_live, recording, "
            "  COALESCE(paused, 0) AS paused, "
            "  COALESCE(notes, '') AS notes "
            "FROM trackings WHERE username=?",
            (username,)).fetchall()
        if not trackings:
            return jsonify(ok=False, error=_t("Nutzer wird nicht getrackt")), 404
        # Recording-Attempts aggregieren
        attempts = conn.execute(
            "SELECT COUNT(*) AS total, "
            "  SUM(CASE WHEN outcome IN ('ok', 'stall_killed_partial') THEN 1 ELSE 0 END) AS success, "
            "  SUM(CASE WHEN file_size IS NOT NULL THEN file_size ELSE 0 END) AS total_bytes, "
            "  MAX(started_at) AS last_attempt "
            "FROM recording_attempts WHERE username=?",
            (username,)).fetchone()
        # Outcome-Breakdown (top 5)
        outcomes = conn.execute(
            "SELECT outcome, COUNT(*) AS c FROM recording_attempts "
            "WHERE username=? AND outcome IS NOT NULL "
            "GROUP BY outcome ORDER BY c DESC LIMIT 5",
            (username,)).fetchall()
        # Letzte 5 erfolgreichen Aufnahmen mit Größe + Datum.
        # WICHTIG: recordings-Tabelle hat KEINE file_size-Spalte (siehe
        # init_db). file_size steht in recording_attempts. Wir filtern auf
        # erfolgreiche Attempts mit Daten (file_size IS NOT NULL und > 0).
        recent_recs = conn.execute(
            "SELECT started_at, file_path, file_size FROM recording_attempts "
            "WHERE username=? AND outcome IN ('ok', 'stall_killed_partial') "
            "  AND file_size IS NOT NULL AND file_size > 0 "
            "ORDER BY started_at DESC LIMIT 5",
            (username,)).fetchall()
    # B60: Optional das LIVE TikTok-Profil dazuladen (Avatar, Follower, Bio,
    # verified) wenn ?tiktok=1. Wird vom Dashboard-Profil-Popup genutzt.
    # Graceful: schlägt der Fetch fehl (Netz/Rate-Limit/Scraper nicht bereit),
    # liefern wir trotzdem die lokalen Stats + tiktok:{error}. Cache via Redis
    # (PROFILE_CACHE_TTL, wie der /tiktok Telegram-Command) entlastet TikTok.
    tiktok_profile = None
    if request.args.get("tiktok") == "1":
        try:
            async def _fetch_tk():
                cache_key = f"profile:{username}"
                data = await _nc_rsstate.haken("redis_get")(cache_key)
                if data is None and _c().scraper_session() is not None:
                    data = await _c().scraper_session().fetch_profile(username)
                    if data and data.get("ok"):
                        await _nc_rsstate.haken("redis_set")(cache_key, data, ttl=_env_int("PROFILE_CACHE_TTL", 60))
                return data
            tk = _c().run_async(_fetch_tk(), timeout=20)
            if tk and tk.get("ok"):
                tiktok_profile = {
                    "nickname":        tk.get("nickname"),
                    "signature":       tk.get("signature"),
                    "avatar":          tk.get("avatar"),
                    "verified":        bool(tk.get("verified")),
                    "private":         bool(tk.get("private")),
                    "follower_count":  tk.get("follower_count"),
                    "following_count": tk.get("following_count"),
                    "heart_count":     tk.get("heart_count"),
                    "video_count":     tk.get("video_count"),
                }
                try: save_profile_snapshot(username, tk)
                except Exception: pass
            elif tk:
                tiktok_profile = {"error": tk.get("error") or "fetch failed"}
            else:
                tiktok_profile = {"error": _t("Scraper nicht bereit")}
        except Exception as e:
            tiktok_profile = {"error": _fehler_text(e, "profil")}

    return jsonify({
        "ok": True,
        "username": username,
        "profile_url": f"https://www.tiktok.com/@{username}",
        "tiktok": tiktok_profile,
        "trackings": [{
            "id": t["id"], "group_id": t["group_id"],
            "created_at": t["created_at"][:19] if t["created_at"] else "",
            "last_live": bool(t["last_live"]),
            "recording": bool(t["recording"]),
            "paused": bool(t["paused"]),
            "notes": t["notes"] or "",
        } for t in trackings],
        "stats": {
            "rec_count": attempts["total"] or 0,
            "success_count": attempts["success"] or 0,
            "success_rate": round(100.0 * (attempts["success"] or 0) / max(1, attempts["total"] or 0), 1),
            "total_bytes": attempts["total_bytes"] or 0,
            "last_attempt": (attempts["last_attempt"] or "")[:19],
        },
        "outcomes": [{"outcome": o["outcome"], "count": o["c"]} for o in outcomes],
        "recent_recordings": [{
            "created_at": (r["started_at"] or "")[:19],
            "filename": os.path.basename(r["file_path"]) if r["file_path"] else "",
            "size_mb": round((r["file_size"] or 0) / 1024 / 1024, 1),
        } for r in recent_recs],
    })


@bp.route("/api/backoff-watch")
def api_backoff_watch():
    """Liste aller Trackings im aktiven B45-Backoff mit Restzeit + Streak."""
    now = time.monotonic()
    watching = []
    # Build username lookup für Trackings die backed off sind
    if _nc_brainstate.DEAD_BACKOFF_UNTIL:
        tids = list(_nc_brainstate.DEAD_BACKOFF_UNTIL.keys())
        with db_conn() as conn:
            # Portabel: einzelne SELECTs (n ist klein, max 10-20)
            for tid in tids:
                until = _nc_brainstate.DEAD_BACKOFF_UNTIL.get(tid, 0)
                remaining = int(max(0, until - now))
                if remaining <= 0:
                    continue
                streak = _nc_brainstate.DEAD_STREAK.get(tid, 0)
                row = conn.execute(
                    "SELECT username, group_id, COALESCE(notes, '') AS notes "
                    "FROM trackings WHERE id=?", (tid,)).fetchone()
                if row:
                    watching.append({
                        "tracking_id": tid,
                        "username": row["username"],
                        "group_id": row["group_id"],
                        "notes": row["notes"] or "",
                        "streak": streak,
                        "remaining_secs": remaining,
                    })
    # Sort by remaining-time ascending (whose backoff ends soonest first)
    watching.sort(key=lambda x: x["remaining_secs"])
    # Plus Anzahl Trackings im "early-disconnect"-Retry-Mode
    early_retries = []
    if _nc_brainstate.EARLY_DISCONNECT:
        tids = list(_nc_brainstate.EARLY_DISCONNECT.keys())
        with db_conn() as conn:
            for tid in tids:
                count = _nc_brainstate.EARLY_DISCONNECT.get(tid, 0)
                if count <= 0:
                    continue
                row = conn.execute(
                    "SELECT username FROM trackings WHERE id=?", (tid,)).fetchone()
                if row:
                    early_retries.append({
                        "tracking_id": tid,
                        "username": row["username"],
                        "retry_count": count,
                    })
    return jsonify({
        "stream_dead_backoff": watching,
        "early_disconnect_retry": early_retries,
        "threshold": _env_int("STREAM_DEAD_STREAK_THRESHOLD", 3),
    })


@bp.route("/api/stream/timeline")
def api_stream_timeline():
    """Kapitel-Marker (Auto-Director) der laufenden/letzten Session für die Timeline."""
    # Groß-/Kleinschreibung: trackings speichern den Handle wie getippt
    # (clean_username macht kein lower()). Ein hart kleingeschriebener Name
    # traf hier weder die Kapitel noch die laufende Session — die Timeline
    # blieb leer und meldete "nicht live", während gesendet wurde.
    user = _nc_trackingdb.resolve_tracked_user(
        (request.args.get("user") or _nc_channels.restream_active().get("user") or "").lstrip("@").strip())
    if not user:
        return jsonify(ok=True, user=None, chapters=[], duration_secs=0, live=False)
    since = (datetime.now(timezone.utc) - timedelta(hours=12)).isoformat()
    try:
        with db_conn() as conn:
            rows = conn.execute("SELECT offset_secs, reason, title, created_at FROM stream_chapters "
                                "WHERE LOWER(username)=LOWER(?) AND created_at >= ? "
                                "ORDER BY offset_secs ASC LIMIT 40",
                                (user, since)).fetchall()
    except Exception as e:
        return jsonify(ok=False, error=_fehler_text(e, "api_stream_timeline")), 500
    chapters = [{"offset": int(r["offset_secs"] or 0), "reason": r["reason"] or "",
                 "title": r["title"] or "", "at": (r["created_at"] or "")[11:19]} for r in rows]
    _sk = _nc_trackingdb.ci_key(_nc_rsstate.SESSION_START, user)
    start = _nc_rsstate.SESSION_START.get(_sk) if _sk else None
    dur = int(time.time() - start) if start else (max([c["offset"] for c in chapters], default=0) + 60)
    return jsonify(ok=True, user=user, live=bool(start), chapters=chapters,
                   duration_secs=max(dur, 1),
                   viewers=_viewer_stats(start))     # V37: Kick-Zuschauer-Kontext


@bp.route("/api/stream/transcript")
def api_stream_transcript():
    """Live-Transkript: was AZRAEL gerade vom Stream hört (letzte Zeilen)."""
    user = (request.args.get("user") or _nc_channels.restream_active().get("user") or "").lstrip("@").lower()
    if not user:
        return jsonify(ok=True, user=None, lines=[])
    buf = list(_nc_azrael.TRANSCRIPT.get(user) or [])[-30:]
    lines = [{"text": x.get("text", ""), "at": (str(x.get("ts", ""))[11:19] if x.get("ts") else "")}
             for x in buf if x.get("text")]
    return jsonify(ok=True, user=user, lines=lines)


@bp.route("/metrics")
def api_prometheus_metrics():
    """v37 Observability: Prometheus-kompatibler Endpoint. An Grafana/Prometheus/
       Uptime-Kuma hängbar. Rein lesend, ohne Auth (nur Betriebs-Kennzahlen)."""
    import shutil as _sh
    now = datetime.now(timezone.utc)
    since_24 = (now - timedelta(hours=24)).isoformat()
    _start = _c().get_bot_start_time()
    up = int((datetime.now(timezone.utc) - _start).total_seconds()) if _start else 0
    db_ok = 1
    rec_24 = rec_total = ai_24 = 0
    try:
        with db_conn() as conn:
            conn.execute("SELECT 1").fetchone()
            rec_24 = conn.execute("SELECT COUNT(*) AS c FROM recordings WHERE created_at>=?", (since_24,)).fetchone()["c"]
            rec_total = conn.execute("SELECT COUNT(*) AS c FROM recordings").fetchone()["c"]
            try:
                ai_24 = conn.execute("SELECT COUNT(*) AS c FROM ai_interactions WHERE created_at>=?", (since_24,)).fetchone()["c"]
            except Exception:
                ai_24 = 0
    except Exception:
        db_ok = 0
    live = len(_nc_rsstate.SESSION_START or {})
    restream = 1 if _nc_channels.restream_active().get("user") else 0
    try:
        tracked = len(get_all_active_trackings(include_paused=True))
    except Exception:
        tracked = 0
    try:
        disk_free = _sh.disk_usage((os.getenv("RECORDINGS_DIR", "recordings") or "recordings").strip() if "RECORDINGS_DIR" in globals() else "/").free
    except Exception:
        disk_free = 0
    ai_budget = len(_nc_azrael.CALL_TS)

    def metric(name, val, help_txt, typ="gauge"):
        return f"# HELP {name} {help_txt}\n# TYPE {name} {typ}\n{name} {val}\n"

    body = "".join([
        metric("nightcrawler_up", 1, "Bot-Prozess läuft"),
        metric("nightcrawler_uptime_seconds", up, "Uptime in Sekunden", "counter"),
        metric("nightcrawler_db_ok", db_ok, "Datenbank erreichbar (1/0)"),
        metric("nightcrawler_recordings_24h", rec_24, "Aufnahmen letzte 24h"),
        metric("nightcrawler_recordings_total", rec_total, "Aufnahmen gesamt", "counter"),
        metric("nightcrawler_ai_calls_24h", ai_24, "KI-Aufrufe letzte 24h"),
        metric("nightcrawler_ai_budget_used", ai_budget, "KI-Calls in der aktuellen Minute"),
        metric("nightcrawler_live_streams", live, "Aktuell live & in Aufnahme"),
        metric("nightcrawler_restream_active", restream, "Kick-Restream aktiv (1/0)"),
        metric("nightcrawler_tracked_streamers", tracked, "Getrackte Streamer gesamt"),
        metric("nightcrawler_disk_free_bytes", disk_free, "Freier Speicher am Aufnahme-Pfad"),
    ])
    return (body, 200, {"Content-Type": "text/plain; version=0.0.4; charset=utf-8"})


@bp.route("/api/profile/snapshots/<username>")
def api_profile_snapshots(username):
    username = clean_username(username)
    if not username:
        return jsonify(ok=False, error=_t("ungültiger username")), 400
    rows = get_profile_snapshots(username, 100)
    return jsonify(ok=True, username=username, snapshots=[{
        "id": r["id"], "follower_count": r["follower_count"],
        "heart_count": r["heart_count"], "video_count": r["video_count"],
        "captured_at": r["captured_at"],
    } for r in rows])


@bp.route("/api/stream/inspect/<username>")
def api_stream_inspect(username):
    try:
        result = _c().run_async(
            inspect_stream_url(username, session=_c().scraper_session()),
            timeout=45)
    except Exception as e:
        return jsonify(ok=False, error=f"inspect failed: {e}"), 503
    code = 200 if result.get("ok") else 502
    return jsonify(result), code


@bp.route("/api/profile/lookup-bulk", methods=["POST"])
def api_profile_lookup_bulk():
    data = request.get_json(silent=True) or {}
    usernames = data.get("usernames") or []
    if not isinstance(usernames, list) or not usernames:
        return jsonify(ok=False, error=_t("usernames[] erforderlich")), 400
    usernames = [clean_username(u) for u in usernames[:20]]
    usernames = [u for u in usernames if u]
    async def _lookup_all():
        import aiohttp          # siehe inspect_stream_url: nicht auf Modulebene

        results = {}
        session = _c().scraper_session()
        own = False
        if session is None:
            session = aiohttp.ClientSession(); own = True
        try:
            for u in usernames:
                try:
                    info = await _nc_rsstate.haken("live_info")(u, session=session)
                    detail = info.get("info") or {}
                    results[u] = {
                        "is_live": info.get("is_live"),
                        "title": detail.get("title"),
                        "viewers": detail.get("viewer_count") or detail.get("viewers"),
                    }
                except Exception as e:
                    results[u] = {"error": _fehler_text(e, "bulk-live")}
        finally:
            if own:
                try: await session.close()
                except Exception: pass
        return results
    try:
        results = _c().run_async(_lookup_all(), timeout=60)
    except Exception as e:
        return jsonify(ok=False, error=f"lookup failed: {e}"), 503
    return jsonify(ok=True, results=results)
