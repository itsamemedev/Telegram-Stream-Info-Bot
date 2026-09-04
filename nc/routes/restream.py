"""nc.routes.restream — die Routen unter /api/restream als Flask-Blueprint.

Welle 3 der Zerlegung (siehe docs/MODULARISIERUNG.md). Pfade stehen woertlich
in den Dekoratoren (kein url_prefix); was der Monolith weiterhin stellen muss,
kommt ueber nc.ctx statt ueber einen Import aus bot.py.

v4.1-W22: Die letzte grosse Gruppe im Monolithen — sechzehn Routen, und
**null neue Kontext-Eintraege**. Roh waeren es achtunddreissig gewesen, bei
24 von vertraglich 25 belegten Plaetzen. Vorweg geloest:

* **nc/restreamcfg.py** — die drei Sendeziele, die Parameter der Sendepruefung,
  der Stall-Zeitgeber und die beiden oeffentlichen Links. Jeder .env-Name steht
  dort WOERTLICH in einem os.getenv(...), damit tools/gen_env_example.py ihn
  findet und ein grep ihn trifft.
* **nc/restreamstate.py** — die sieben Zustands-Container als Aliase, dazu
  Manager und Waechter als Register (sie entstehen im Monolithen erst weit
  unten, ein Alias waere fuer immer None).

STREAM-KEYS: dieser Blueprint gibt **keinen** Schluessel heraus. Fuer Anzeige
und Diagnose gibt es `key_gesetzt(name)` — ein bool. Wer hier einen Key in
eine Antwort schreibt, verschenkt den Kanal.

Die drei Haken (Discord-Meldung, geteilte aiohttp-Session, Live-Absicherung
des Test-Pushes) kommen aus nc/restreamstate.py, nicht aus dem Kontext —
begruendet dort.
"""

import asyncio
import os
import time
from datetime import datetime, timezone

from flask import Blueprint, jsonify, request

from nc import channels as _nc_channels
from nc import fehlertext as _nc_fehlertext
from nc import i18n as _nc_i18n
from nc import kickapi as _nc_kickapi
from nc import restream_targets as _nc_rst
from nc import restream_util as _nc_rutil
from nc import restreamcfg as _nc_rscfg
from nc import restreamstate as _nc_rsstate
from nc import restream_testpush as _nc_testpush
from nc import trackingdb as _nc_trackingdb
from nc.channels import RESTREAM_CHAT as _RESTREAM_CHAT
from nc.dbwrap import db_conn
from nc.envnum import env_int as _env_int
from nc.stats import _collect_session_stats
from nc.textutil import clean_username
from nc.util import _loop_not_ready

from nc import ctx as _ctx

bp = Blueprint("restream", __name__)


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
    """v4.1-W22: an der Quelle uebersetzen. Diese Texte erreichen das DOM
       meist verkettet ("Fehler: " + error) — ein Katalogeintrag fuer den
       blossen Text traefe dort nie."""
    return _nc_i18n.t(s)



async def _kick_channel_live():
    """B161: Ist der produktive Kick-Kanal gerade live? True/False/None(=unklar).
       public keyless API kick.com/api/v2/channels/<slug> — None bei jedem Zweifel,
       damit UNKNOWN nie als OFFLINE fehlgedeutet wird (Regel aus restream_guard)."""
    slug = _nc_kickapi.slug()
    if not slug:
        return None
    try:
        import aiohttp
        session = await _nc_rsstate.haken("ai_session")()
        async with session.get(f"https://kick.com/api/v2/channels/{slug}",
                               timeout=aiohttp.ClientTimeout(total=8),
                               headers={"User-Agent": "Mozilla/5.0"}) as r:
            if r.status != 200:
                return None
            j = await r.json(content_type=None)
        ls = j.get("livestream")
        return bool(ls and ls.get("is_live", True))
    except Exception:
        return None


def _testpush_cfg():
    """.env FRISCH lesen (Modul-Konstanten würden sie einfrieren — s. Skill)."""
    li, lk, ls = _nc_rsstate.haken("testpush_live")()
    return _nc_testpush.TestPushConfig(
        test_ingest=os.getenv("RESTREAM_TEST_INGEST", "").strip(),
        test_key=os.getenv("RESTREAM_TEST_KEY", "").strip(),
        live_ingest=li, live_key=lk, live_key_source=ls,
        allow_live=os.getenv("RESTREAM_TEST_ALLOW_LIVE", "0").strip().lower() in ("1", "true", "yes", "on"),
        duration_s=_env_int("RESTREAM_TEST_DURATION_S", 8),
        fps=_env_int("RESTREAM_TEST_FPS", 30))


async def _testpush_exec(cmd, duration_s):
    """Führt den ffmpeg-Testbild-Push aus, sammelt rc+stderr. Hartes Timeout,
       Prozess wird bei Überschreitung sicher getötet (kein Zombie/Leak)."""
    proc = await asyncio.create_subprocess_exec(
        *cmd, stdout=asyncio.subprocess.DEVNULL, stderr=asyncio.subprocess.PIPE)
    try:
        _, stderr = await asyncio.wait_for(proc.communicate(), timeout=duration_s + 15)
    except asyncio.TimeoutError:
        try:
            proc.kill()
        except Exception:
            pass
        try:
            await proc.wait()
        except Exception:
            pass
        return {"rc": -1, "stderr": "timed out"}
    return {"rc": proc.returncode, "stderr": (stderr or b"").decode("utf-8", "replace")}


@bp.route("/api/restream/report", methods=["POST"])
def api_restream_report():
    """1-Klick-Sende-Report: Session-Bilanz → Discord (+ Rückgabe für die Anzeige)."""
    d = request.get_json(silent=True) or {}
    # Wie in /api/stream/timeline: Schreibweise aus den trackings auflösen,
    # sonst zählt der Report für "@RabiLive" nichts (Aufnahmen, Dauer, Momente).
    user = _nc_trackingdb.resolve_tracked_user(
        (d.get("user") or _nc_channels.restream_active().get("user") or "").lstrip("@").strip())
    if not user:
        return jsonify(ok=False, error=_t("kein aktiver Stream — Streamer angeben")), 400
    _sk = _nc_trackingdb.ci_key(_nc_rsstate.SESSION_START, user)
    start = _nc_rsstate.SESSION_START.get(_sk) if _sk else None
    stats = _collect_session_stats(user, start)
    dur = stats.get("dur_min")
    lines = [f"📊 **Sende-Report @{user}**",
             (f"⏱ Dauer: {dur // 60}h {dur % 60}min" if isinstance(dur, int) else "⏱ Dauer: —"),
             f"📼 Aufnahmen: {stats.get('recs', 0)} · {stats.get('size_mb', 0)} MB",
             f"🔥 Hype-Momente: {stats.get('moments', 0)}"]
    text = "\n".join(lines)
    sent_dc = False
    try:
        # v4.0-W105 (Tiefenbughunt): _spawn() scheitert hier immer — diese Route
        # laeuft im Flask-Thread ohne eigenen Loop. Die Meldung ging deshalb nie
        # raus, und der Grund stand nur auf log.debug, also im Fehlerlog nie.
        _nc_rsstate.haken("spawn")(_nc_rsstate.haken("notify")(text, "report"), name="report-dc")
        sent_dc = True
    except Exception as e:
        _c().log.error("Sende-Report an Discord fehlgeschlagen: %s", e, exc_info=e)
    return jsonify(ok=True, text=text, sent_discord=sent_dc)


@bp.route("/api/restream/health")
def api_restream_health():
    """B160: Live-Encode-Health je aktivem Restream (bitrate/fps/speed/drop aus ffmpeg-progress)."""
    out = []
    try:
        procs = getattr(_nc_rsstate.mgr(), "_procs", {}) or {}
        active = _nc_rsstate.ACTIVE_ALL or {}
        for rid, info in list(procs.items()):
            h = (info or {}).get("health") or {}
            meta = active.get(rid) or {}
            started = (info or {}).get("started")
            up = int(time.monotonic() - started) if started else None
            tt = (info or {}).get("tee_targets")
            out.append({
                "rid": rid, "user": meta.get("user", ""), "label": meta.get("label", ""),
                "bitrate": h.get("bitrate"), "fps": h.get("fps"), "speed": h.get("speed"),
                "drop": h.get("drop", 0), "dup": h.get("dup", 0), "size_mb": h.get("size_mb"),
                "out_time": h.get("out_time"),
                "slow": bool(h.get("slow_ticks", 0) >= 5 or h.get("slow_warned")),
                "uptime_s": up, "ntargets": (len(tt) if hasattr(tt, "__len__") else 0),
            })
    except Exception as e:
        return jsonify(ok=False, error=_fehler_text(e, "api_restream_health"), streams=[])
    return jsonify(ok=True, streams=out, count=len(out))


@bp.route("/api/restream/testpush", methods=["GET"])
def api_testpush_status():
    """B161: Status fürs Panel — Test-Ziel konfiguriert? Guards frei? Kanal live?"""
    cfg = _testpush_cfg()
    tgt = _nc_testpush.resolve_target(cfg, _nc_testpush.TARGET_TEST)
    ch = _nc_testpush.CH_UNKNOWN
    try:
        live = _c().run_async(_kick_channel_live(), timeout=10)
        ch = (_nc_testpush.CH_LIVE if live
              else _nc_testpush.CH_OFFLINE if live is False
              else _nc_testpush.CH_UNKNOWN)
    except Exception:
        ch = _nc_testpush.CH_UNKNOWN
    return jsonify(ok=True,
                   test_configured=bool(cfg.test_ingest and cfg.test_key),
                   test_ingest_host=(_nc_rutil.url_host(cfg.test_ingest) or ""),
                   test_key_fp=(_nc_testpush.fingerprint(cfg.test_key) if cfg.test_key else None),
                   live_key_source=cfg.live_key_source,
                   live_ingest_host=(_nc_rutil.url_host(cfg.live_ingest) or ""),
                   allow_live=cfg.allow_live,
                   restream_active=len(_nc_rsstate.ACTIVE_ALL),
                   channel=ch, duration_s=cfg.duration_s, fps=cfg.fps,
                   default_ready=bool(tgt.ok))


@bp.route("/api/restream/testpush", methods=["POST"])
def api_testpush_run():
    """B161: sendet ein kurzes ffmpeg-Testbild an einen Ingest, um den Key zu
       prüfen. Body: {target?: 'test'|'live', confirm?: bool}. Standard = Test-Slot.
       Der Live-Key ist mehrfach gesichert (allow_live + Kanal-Offline + confirm)."""
    payload = request.get_json(silent=True) or {}
    prefer = (_nc_testpush.TARGET_LIVE
              if str(payload.get("target", "")).lower() == "live"
              else _nc_testpush.TARGET_TEST)
    confirm = bool(payload.get("confirm", False))
    cfg = _testpush_cfg()
    tgt = _nc_testpush.resolve_target(cfg, prefer)
    # Kanal-Live nur abfragen, wenn der Live-Key betroffen sein KÖNNTE — spart
    # bei jedem harmlosen Test-Slot-Push einen HTTP-Aufruf.
    channel = _nc_testpush.CH_OFFLINE
    if tgt.ok and tgt.is_live_key:
        try:
            live = _c().run_async(_kick_channel_live(), timeout=10)
            channel = (_nc_testpush.CH_LIVE if live
                       else _nc_testpush.CH_OFFLINE if live is False
                       else _nc_testpush.CH_UNKNOWN)
        except Exception:
            channel = _nc_testpush.CH_UNKNOWN
    dec = _nc_testpush.guard(cfg, tgt, active_all_nonempty=bool(_nc_rsstate.ACTIVE_ALL),
                             channel=channel, confirm=confirm)
    if not dec.allowed:
        return jsonify(ok=False, allowed=False, reason=dec.reason, error=dec.message,
                       target=tgt.source, is_live_key=tgt.is_live_key,
                       channel=channel), dec.http
    cmd = _nc_testpush.build_cmd(tgt.ingest, tgt.key, _nc_rutil.normalize_ingest,
                                 duration_s=cfg.duration_s, fps=cfg.fps)
    fp = _nc_testpush.fingerprint(tgt.key)
    _c().log.info("Test-Push: Ziel=%s host=%s key(len=%d,fp=%05d) dur=%ds live_key=%s",
             tgt.source, _nc_rutil.url_host(tgt.ingest) or "?", fp["len"], fp["fp"],
             cfg.duration_s, tgt.is_live_key)
    try:
        res = _c().run_async(_testpush_exec(cmd, cfg.duration_s),
                                    timeout=cfg.duration_s + 25)
    except Exception as e:
        if _loop_not_ready(e):
            return jsonify(ok=False, error=_t("Event-Loop startet noch — kurz erneut versuchen.")), 503
        return jsonify(ok=False, error=f"Test-Push-Ausführung: {e}"), 500
    result = _nc_testpush.classify_result(res.get("rc"), res.get("stderr", ""))
    return jsonify(ok=(result["state"] == "ok"), allowed=True,
                   target=tgt.source, is_live_key=tgt.is_live_key,
                   ingest_host=_nc_rutil.url_host(tgt.ingest) or "", key_fp=fp,
                   channel=channel, duration_s=cfg.duration_s, result=result)


@bp.route("/api/restream/deck")
def api_restream_deck():
    """F85: Signalfluss-Status für das ON-AIR-Deck: aktiver Restream
       (Quelle/Label) + öffentlicher Kick-Link. Bewusst minimal & sync-sicher."""
    ra = dict(_nc_channels.restream_active())
    # V37-W-CTRL: Status aller drei Eigene-Kanal-Plattformen fürs Deck.
    _tw_chan = (os.getenv("TWITCH_CHANNEL", "") or "").strip().lstrip("#")
    _yt = (os.getenv("YOUTUBE_CHANNEL", "") or "").strip()
    _now = time.time()
    def _age(p):
        lm = _nc_channels.WCHAT_STATUS[p]["last_msg"]
        return round(_now - lm) if lm else None
    def _up(p):
        sc = _nc_channels.WCHAT_STATUS[p].get("since") or 0
        return round(_now - sc) if (sc and _nc_channels.WCHAT_STATUS[p]["connected"]) else None
    # v4.0-W24c: YouTube-Chip war ohne YOUTUBE_CHANNEL nicht klickbar — die
    # Deck-URL war dann None, das Frontend haengt den onclick aber an p.url.
    # Jetzt eine brauchbare URL auch ohne Handle: laeuft gerade ein Broadcast,
    # direkt auf die Live-Watch-Seite; sonst, wenn YouTube ueberhaupt in Betrieb
    # ist (Key/OAuth/enabled), ins Studio-Live-Dashboard des Creators.
    def _yt_deck_url():
        if _yt:
            return (_yt if _yt.startswith("http")
                    else f"https://youtube.com/{_yt if _yt.startswith('@') else '@' + _yt}/live")
        bc = (_nc_rsstate.YT_INGEST_CACHE.get("broadcast") or "").strip()
        if bc:
            return f"https://www.youtube.com/watch?v={bc}"
        if (_nc_rscfg.ziel("youtube")["key"] or _nc_rscfg.aktiv("youtube") or _nc_rsstate.YT_INGEST_CACHE.get("key")
                or _nc_rscfg.yt_oauth_configured()):
            return "https://studio.youtube.com/"
        return None
    _yt_url = _yt_deck_url()
    platforms = {
        "kick": {
            "configured": bool(_nc_rscfg.kick_channel_url() or _env_int("KICK_CHATROOM_ID", 0)),
            "connected": bool(_nc_channels.KICK_MOD["obj"] and _nc_channels.KICK_MOD["obj"].stats.get("connected")),
            "mode": "send", "url": _nc_rscfg.kick_channel_url() or None,
            # v4.0-W10: letzter Sendeversuch (Klartext) statt stummem Scheitern
            "error": ("" if _nc_kickapi.SEND_LAST.get("ok") is not False
                      else _nc_kickapi.SEND_LAST.get("error", "")),
            "send_ok": _nc_kickapi.SEND_LAST.get("ok"),
            "send_age_s": (round(_now - _nc_kickapi.SEND_LAST["ts"])
                           if _nc_kickapi.SEND_LAST.get("ts") else None)},
        "twitch": {
            "configured": bool(_tw_chan),
            "connected": _nc_channels.WCHAT_STATUS["twitch"]["connected"],
            "mode": _nc_channels.WCHAT_STATUS["twitch"]["mode"],
            "last_msg_s": _age("twitch"),
            "reconnects": _nc_channels.WCHAT_STATUS["twitch"]["reconnects"],
            "uptime_s": _up("twitch"),
            "error": _nc_channels.WCHAT_STATUS["twitch"].get("error") or "",
            "url": f"https://twitch.tv/{_tw_chan}" if _tw_chan else None},
        "youtube": {
            "configured": bool(_yt or _nc_rscfg.ziel("youtube")["key"] or _nc_rscfg.aktiv("youtube")
                               or _nc_rsstate.YT_INGEST_CACHE.get("key") or _nc_rscfg.yt_oauth_configured()),
            "connected": _nc_channels.WCHAT_STATUS["youtube"]["connected"],
            "mode": _nc_channels.WCHAT_STATUS["youtube"]["mode"],
            "last_msg_s": _age("youtube"),
            "reconnects": _nc_channels.WCHAT_STATUS["youtube"]["reconnects"],
            "uptime_s": _up("youtube"),
            "error": _nc_channels.WCHAT_STATUS["youtube"].get("error") or "",
            "url": _yt_url},
    }
    # V37: Restream-Ziel-Status pro Plattform (wohin wird tatsächlich
    # ausgespielt) — nicht zu verwechseln mit dem Chat-Listener-Status oben.
    _extra = [n for n, _ in _nc_rst.multistream_targets()]
    _any_live = bool(_nc_rsstate.ACTIVE_ALL)
    _tf = _nc_rsstate.mgr().tee_fehler()          # v4.0-W116: nur noch geltende
    def _terr(_n):
        _e = _tf.get(_n)
        return {"msg": str(_e.get("msg", ""))[:200],
                "age_s": int(time.time() - _e.get("ts", time.time()))} if _e else None
    def _ihost(_u):
        try:
            return _nc_rutil.url_host(_u) or ""
        except Exception:
            return ""
    _kick_db = False
    try:
        with db_conn() as _kc:
            _kr = _kc.execute("SELECT 1 FROM restreams WHERE COALESCE(stream_key,'')<>'' "
                              "OR COALESCE(ingest_url,'')<>'' LIMIT 1").fetchone()
            _kick_db = bool(_kr)
    except Exception:
        _kick_db = False
    restream = {
        "kick": {"is_target": True, "configured": bool(_nc_rscfg.ziel("kick")["key"] or _nc_rscfg.ingest("kick")),
                 "live": _any_live, "primary": True,
                 "key_source": ("db" if _kick_db else ("env" if _nc_rscfg.ziel("kick")["key"] else "")),
                 "ingest_host": _ihost(_nc_rscfg.ingest("kick")), "last_error": _terr("kick")},
        "twitch": {"is_target": ("twitch" in _extra), "configured": bool(_nc_rscfg.ziel("twitch")["key"]),
                   "enabled": _nc_rscfg.aktiv("twitch"), "live": (_any_live and "twitch" in _extra),
                   "primary": False,
                   "key_source": ("env" if _nc_rscfg.ziel("twitch")["key"] else ""),
                   "ingest_host": _ihost(_nc_rscfg.ingest("twitch")), "last_error": _terr("twitch")},
        "youtube": {"is_target": ("youtube" in _extra),
                    "configured": bool(_nc_rscfg.ziel("youtube")["key"] or _nc_rsstate.YT_INGEST_CACHE.get("key")),
                    "enabled": _nc_rscfg.aktiv("youtube"), "live": (_any_live and "youtube" in _extra),
                    "key_source": ("env" if _nc_rscfg.ziel("youtube")["key"]
                                   else (_nc_rsstate.YT_INGEST_CACHE.get("source") or "")),
                    # B138: Welcher Broadcast wurde getroffen? Ohne das laesst
                    # sich "sendet auf den falschen Key" nur am schwarzen
                    # Player in Studio erkennen — nie im Dashboard.
                    "broadcast": _nc_rsstate.YT_INGEST_CACHE.get("broadcast", ""),
                    "reason": ("" if ("youtube" in _extra)
                               else (_nc_rsstate.YT_INGEST_CACHE.get("reason")
                                     or ("YOUTUBE_ENABLED=0 (in .env aktivieren)"
                                         if not _nc_rscfg.aktiv("youtube") else "Stream-Key wird aufgelöst…"))),
                    "primary": False,
                    "ingest_host": _ihost(_nc_rscfg.ingest("youtube")), "last_error": _terr("youtube")},
    }
    # Chat-Status + Restream-Status zusammenführen (Frontend nutzt beides)
    for k in ("kick", "twitch", "youtube"):
        platforms[k]["restream"] = restream[k]
    return jsonify(ok=True,
                   active=(ra if ra.get("user") else None),
                   all=[{k: v for k, v in (i or {}).items() if k != "ovdir"}
                        for i in _nc_rsstate.ACTIVE_ALL.values()],   # V37-P5c (BH3: ohne interne Pfade)
                   platforms=platforms,
                   restream=restream,
                   kick_url=_nc_rscfg.kick_channel_url() or None)


@bp.route("/api/restream/verify")
def api_restream_verify():
    """B123: Was sagen die PLATTFORMEN — nicht was sagt ffmpeg.

    Zeigt pro Restream je Ziel: letzte Antwort der Plattform, Zahl der
    Fehlanzeigen in Folge, ob das Ziel seit dem Start je bestaetigt war.
    Damit ist im Panel unterscheidbar: 'laeuft' vs. 'kommt an'."""
    try:
        return jsonify(ok=True,
                       enabled=_nc_rscfg.verify(),
                       interval_s=_nc_rscfg.verify_takt(),
                       grace_s=_nc_rscfg.verify_karenz(),
                       misses_before_action=_nc_rscfg.verify_misses(),
                       active_platforms=sorted(_nc_rscfg.active_platforms()),
                       # v4.0-W115: das Panel braucht die Grenze, gegen die es
                       # ohne_fortschritt_s einfaerbt — sonst muesste es den
                       # Default doppelt kennen und liefe bei geaenderter .env
                       # auseinander.
                       stall_timeout_s=_nc_rscfg.stall_timeout(),
                       guard=_nc_rsstate.guard().snapshot(),
                       status=_nc_rsstate.mgr().status())
    except Exception as e:
        return jsonify(ok=False, error=_fehler_text(e, "api_restream_verify")), 500


@bp.route("/api/restream/list")
def api_restream_list():
    try:
        with db_conn() as conn:
            rows = conn.execute("SELECT * FROM restreams ORDER BY id DESC").fetchall()
        live = _nc_rsstate.mgr().status()
        en, why = _nc_rscfg.enabled()
        def _auto(r):
            try: return bool(r["auto_restream"])
            except (IndexError, KeyError): return False
        return jsonify(ok=True, enabled=en, reason=why,
                       configured=bool(_nc_rscfg.ingest("kick") or any(r["ingest_url"] for r in rows)),
                       targets=[{
                           "id": r["id"], "label": r["label"], "source_username": r["source_username"],
                           "ingest_url": r["ingest_url"] or _nc_rscfg.ingest("kick"),
                           "has_key": bool(r["stream_key"] or _nc_rscfg.ziel("kick")["key"]),
                           "transcode": bool(r["transcode"]), "enabled": bool(r["enabled"]),
                           "auto_restream": _auto(r),
                           "status": r["status"], "last_error": r["last_error"],
                           "uptime_s": live.get(r["id"], {}).get("uptime_s"),
                           "attempts": live.get(r["id"], {}).get("attempts"),
                           "active_transcode": live.get(r["id"], {}).get("transcode"),
                           "health": live.get(r["id"], {}).get("health")} for r in rows])
    except Exception as e:
        return jsonify(ok=False, error=_fehler_text(e, "api_restream_list")), 500


@bp.route("/api/restream/create", methods=["POST"])
def api_restream_create():
    d = request.get_json(silent=True) or {}
    # B76-Fix: User fügen gern die komplette TikTok-URL ein — lstrip("@") ließ
    # "https://www.tiktok.com/@rabi1978" durch, der Chat-Listener scheiterte dann
    # an einem Phantom-User ("www.tiktok.comrabi1978"). clean_username extrahiert
    # das echte Handle aus URL/@-Formen.
    src = clean_username(d.get("source_username") or "")
    if not src:
        return jsonify(ok=False, error=_t("source_username fehlt")), 400
    try:
        with db_conn() as conn:
            conn.execute(
                "INSERT INTO restreams (created_at, label, source_username, ingest_url, stream_key, "
                "transcode, enabled, auto_restream, status) VALUES (?,?,?,?,?,?,1,?,'idle')",
                (datetime.now(timezone.utc).isoformat(), (d.get("label") or src)[:120], src,
                 (d.get("ingest_url") or "").strip(), (d.get("stream_key") or "").strip(),
                 1 if d.get("transcode") else 0, 1 if d.get("auto_restream") else 0))
            conn.commit()
        return jsonify(ok=True)
    except Exception as e:
        return jsonify(ok=False, error=_fehler_text(e, "api_restream_create")), 500


@bp.route("/api/restream/<int:rid>/edit", methods=["POST"])
def api_restream_edit(rid):
    """Ziel-Parameter ändern (Label, Ingest, Key, Transcode, Auto). Nicht im Live-Betrieb."""
    d = request.get_json(silent=True) or {}
    fields, vals = [], []
    if "label" in d:        fields.append("label=?");        vals.append((d["label"] or "")[:120])
    if "ingest_url" in d:   fields.append("ingest_url=?");   vals.append((d["ingest_url"] or "").strip())
    if "stream_key" in d:   fields.append("stream_key=?");   vals.append((d["stream_key"] or "").strip())
    if "transcode" in d:    fields.append("transcode=?");    vals.append(1 if d["transcode"] else 0)
    if "auto_restream" in d:fields.append("auto_restream=?");vals.append(1 if d["auto_restream"] else 0)
    if not fields:
        return jsonify(ok=False, error=_t("nichts zu ändern")), 400
    try:
        with db_conn() as conn:
            vals.append(rid)
            conn.execute(f"UPDATE restreams SET {', '.join(fields)} WHERE id=?", vals)
            conn.commit()
        return jsonify(ok=True)
    except Exception as e:
        return jsonify(ok=False, error=_fehler_text(e, "api_restream_edit")), 500


@bp.route("/api/restream/<int:rid>/delete", methods=["POST"])
def api_restream_delete(rid):
    try:
        _c().run_async(_nc_rsstate.mgr().stop(rid), timeout=15)
    except Exception:
        pass
    try:
        with db_conn() as conn:
            conn.execute("DELETE FROM restreams WHERE id=?", (rid,))
            conn.commit()
        return jsonify(ok=True)
    except RuntimeError as e:
        if _loop_not_ready(e):
            return jsonify(ok=False, error=_t("Bot-Loop startet noch"), transient=True), 503
        return jsonify(ok=False, error=_fehler_text(e, "api_restream_delete")), 500
    except Exception as e:
        return jsonify(ok=False, error=_fehler_text(e, "api_restream_delete")), 500


@bp.route("/api/restream/<int:rid>/start", methods=["POST"])
def api_restream_start(rid):
    en, why = _nc_rscfg.enabled()
    if not en:
        return jsonify(ok=False, error=f"Restream deaktiviert: {why}"), 409
    try:
        with db_conn() as conn:
            conn.execute("UPDATE restreams SET enabled=1 WHERE id=?", (rid,))
            conn.commit()
        res = _c().run_async(_nc_rsstate.mgr().start(rid), timeout=40)
        return jsonify(res), (200 if res.get("ok") else 502)
    except RuntimeError:
        return jsonify(ok=False, error=_t("Event-Loop nicht bereit")), 503
    except Exception as e:
        return jsonify(ok=False, error=_fehler_text(e, "api_restream_start")), 500


@bp.route("/api/restream/<int:rid>/stop", methods=["POST"])
def api_restream_stop(rid):
    try:
        res = _c().run_async(_nc_rsstate.mgr().stop(rid), timeout=15)
        return jsonify(res)
    except RuntimeError as e:
        if _loop_not_ready(e):
            return jsonify(ok=False, error=_t("Bot-Loop startet noch"), transient=True), 503
        return jsonify(ok=False, error=_fehler_text(e, "api_restream_stop")), 500
    except Exception as e:
        return jsonify(ok=False, error=_fehler_text(e, "api_restream_stop")), 500


@bp.route("/api/restream/start_all", methods=["POST"])
def api_restream_start_all():
    """Startet alle aktivierten Ziele, deren Quelle gerade live ist."""
    en, why = _nc_rscfg.enabled()
    if not en:
        return jsonify(ok=False, error=f"Restream deaktiviert: {why}"), 409
    started, skipped = 0, 0
    try:
        with db_conn() as conn:
            rows = conn.execute("SELECT id FROM restreams WHERE enabled=1").fetchall()
        for r in rows:
            try:
                res = _c().run_async(_nc_rsstate.mgr().start(r["id"]), timeout=40)
                if res.get("ok"): started += 1
                else: skipped += 1
            except Exception:
                skipped += 1
        return jsonify(ok=True, started=started, skipped=skipped)
    except RuntimeError as e:
        if _loop_not_ready(e):
            return jsonify(ok=False, error=_t("Bot-Loop startet noch"), transient=True), 503
        return jsonify(ok=False, error=_fehler_text(e, "api_restream_start_all")), 500
    except Exception as e:
        return jsonify(ok=False, error=_fehler_text(e, "api_restream_start_all")), 500


@bp.route("/api/restream/stop_all", methods=["POST"])
def api_restream_stop_all():
    try:
        _c().run_async(_nc_rsstate.mgr().stop_all(), timeout=30)
        return jsonify(ok=True)
    except RuntimeError as e:
        if _loop_not_ready(e):
            return jsonify(ok=False, error=_t("Bot-Loop startet noch"), transient=True), 503
        return jsonify(ok=False, error=_fehler_text(e, "api_restream_stop_all")), 500
    except Exception as e:
        return jsonify(ok=False, error=_fehler_text(e, "api_restream_stop_all")), 500


@bp.route("/api/restream/chatfeed")
def api_restream_chatfeed():
    """Live-Chat-Feed (TikTok + Kick), wie er ins Sendebild gebrannt wird —
       fürs Studio-Monitor-Panel im Dashboard."""
    items = [{"ts": round(m["ts"], 1), "src": m["src"], "who": m["who"], "text": m["text"]}
             for m in list(_RESTREAM_CHAT)[-40:]]
    brand = "  \u00b7  ".join(
        u.replace("https://", "").replace("http://", "").rstrip("/")
        for u in (_nc_rscfg.kick_channel_url(), _nc_rscfg.discord_invite()) if (u or "").strip())
    # F100: Regie-Zustand des aktiven Streams (Stimmung/Energie/Stammchatter)
    _active_u = clean_username(_nc_channels.restream_active().get("user") or "")
    _dir = _nc_rsstate.DIRECTORS.get(_nc_channels.restream_active().get("user") or "") or \
        (next((d for u, d in _nc_rsstate.DIRECTORS.items() if clean_username(u) == _active_u), None) if _active_u else None)
    director = _dir.snapshot() if _dir is not None else None
    return jsonify(ok=True, items=items, layout=_nc_rsstate.layout_mode(), brand=brand,
                   director=director,
                   diag=dict(_nc_rsstate.CHAT_DIAG),
                   sources={"tiktok": _nc_rscfg.chat_src_ok("tiktok"), "kick": _nc_rscfg.chat_src_ok("kick")},
                   overlay_enabled=_nc_rscfg.overlay(),
                   active=_nc_channels.restream_active().get("user"))


@bp.route("/api/restream/layout", methods=["POST"])
def api_restream_layout():
    """Layout zur Laufzeit umschalten (studio|burnin). Greift beim NÄCHSTEN
       Relay-Start — ein laufender ffmpeg behält seinen Filtergraph."""
    d = request.get_json(silent=True) or {}
    mode = (d.get("mode") or "").strip().lower()
    if mode not in ("studio", "burnin"):
        return jsonify(ok=False, error=_t("mode muss studio|burnin sein")), 400
    _nc_rsstate.LAYOUT["mode"] = mode
    _c().log_event("restream.layout", "info", f"Sendebild-Layout → {mode}", {"mode": mode})
    running = bool(getattr(_nc_rsstate.mgr(), "_procs", {}))
    return jsonify(ok=True, mode=mode,
                   note=("greift beim nächsten Relay-Start — laufenden Restream neu starten"
                         if running else "aktiv beim nächsten Relay-Start"))
