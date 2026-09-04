"""nc.routes.systemlage — /api/system und die beiden Diagnose-Routen daneben.

v4.1-W32, erste Teillieferung von Vorschlag 2 (der harte Rest des Monolithen).

Warum diese Gruppe zuletzt drankommt: die acht System-Routen greifen zusammen
auf 112 verschiedene Namen aus bot.py zu — mehr als jede andere Gruppe, die
bisher gewandert ist. Der Weg dahin ist derselbe wie in W117: erst die Daten-
und Zustandsschicht aufloesen, dann kosten die Routen nichts. Diese Welle
loest die Sondenschicht auf (nc/systemprobe.py, nc/cookies.load_dict,
nc/logsafe.url_ohne_zugang) und nimmt die drei Routen mit, die danach ohne
einen einzigen neuen ctx-Slot auskommen.

Die uebrigen fuenf — preflight, resilience, check_timing, config_snapshot und
selftest — haengen noch am Discord-Client, am Restream-Manager und am
Watchdog-Zustand. Sie folgen, wenn deren Zustand aufgeloest ist, nicht vorher.
"""
import os
import threading
import time
from datetime import datetime, timezone

from flask import Blueprint, jsonify, request

from nc import ctx as _ctx
from nc import discordlimits as _nc_dclimits
from nc import fehlertext as _nc_fehlertext
from nc import i18n as _nc_i18n
from nc import piper_voices as _nc_piper
from nc import proxyutil as _nc_proxyutil
from nc import discordstate as _nc_discordstate
from nc import restream_targets as _nc_rst
from nc import restreamstate as _nc_rsstate
from nc import version as _nc_version
from nc import whispercfg as _nc_whisper
from nc import logsafe as _nc_logsafe
from nc import systemprobe as _nc_probe
from nc.confdrift import config_drift as _cfg_drift
from nc.cookies import load_dict as _load_cookies_dict
from nc.dbwrap import db_conn

bp = Blueprint("systemlage", __name__)


def _c():
    """Laufzeitkontext. Aufruf statt Modul-Konstante — der Kontext wird erst
       beim Bot-Start gefuellt."""
    return _ctx.get()


class _LazyLog:
    def __getattr__(self, name):
        return getattr(_c().log, name)


log = _LazyLog()


def _t(s):
    """v4.1-W20: an der Quelle uebersetzen. Diese Urteile erreichen das DOM in
       einem JSON-Feld — der Browser-Uebersetzer sieht ganze Textknoten, ein
       Wert in einer JSON-Antwort ist keiner. Im Monolithen war das gesamte
       Panel deshalb dauerhaft deutsch, auch im englischen Deck."""
    return _nc_i18n.t(s)


def _fehler_text(e, wo):
    """v4.1-W30: kein roher Ausnahmetext nach aussen."""
    return _nc_fehlertext.nach_aussen(e, wo)


@bp.route("/api/system")
def api_system():
    """F15: Reichere Stack-Infos (Recorder, Modell-Liste, Redis-Version,
       AI-Counter) für die Dashboard-Detailzeile."""
    cookies = _load_cookies_dict()
    important = ["sessionid_ss", "sessionid", "ttwid", "tt_chain_token"]
    have = [c for c in important if c in cookies]
    ai_model = _c().cfg["AI_MODEL"]
    models = _c().check_ai_models_sync()
    redis_ver = _nc_probe.redis_version()
    return jsonify(
        recorder       = _nc_probe.active_recorder(),
        recorder_pref  = _nc_probe.recorder_pref(),
        ai_backend     = ("brain" if os.getenv("AI_PROVIDER","").strip().lower()=="brain"
                          else "freeai"),
        ai_model       = ai_model,
        ai_models      = models if models is not None else [],
        ai_alive       = models is not None,
        ai_has_model   = bool(models) and (
            ai_model in models or
            any(m.startswith(ai_model + ":") for m in models)
        ),
        redis_url      = _nc_logsafe.url_ohne_zugang(_nc_probe.redis_url()),   # v4.0-W118 (SEC)
        redis_alive    = redis_ver is not None,
        redis_version  = redis_ver,
        cookies_total  = len(cookies),
        cookies_critical_have = len(have),
        cookies_critical_need = len(important),
        ai_calls_total = _nc_probe.ai_calls_total(),
    )


@bp.route("/api/system/preflight_history")
def api_system_preflight_history():
    try:
        with db_conn() as conn:
            rows = conn.execute("SELECT overall, fails, warns, created_at FROM preflight_history "
                                "ORDER BY id DESC LIMIT 40").fetchall()
        items = [{"overall": r["overall"], "fails": r["fails"], "warns": r["warns"],
                  "at": (r["created_at"] or "")[5:16].replace("T", " ")} for r in rows]
        return jsonify(ok=True, items=list(reversed(items)))
    except Exception as e:
        return jsonify(ok=False, error=_fehler_text(e, "api_system_preflight_history")), 500


@bp.route("/api/system/config_drift")
def api_config_drift():
    """V37-DRIFT: Welche .env-Werte weichen vom Code-Default ab?

    ?all=1 zeigt auch die harmlosen. Ohne Parameter nur die Watchlist —
    Einstellungen, bei denen eine Abweichung Verhalten oder Last spuerbar
    aendert.

    v4.1-W32: der Quelltext, der durchsucht wird, kommt aus cfg["BOT_DATEI"].
    Im Monolithen stand hier __file__ — in einem Blueprint zeigt das auf
    DIESE Datei, und die Antwort waere still eine leere Drift-Liste gewesen.
    Genau die Sorte stiller Fehlanzeige, vor der CLAUDE.md warnt.
    """
    try:
        rep = _cfg_drift(_c().cfg["BOT_DATEI"],
                         only_watchlist=(request.args.get("all") != "1"))
        rep["ok"] = True
        return jsonify(rep)
    except Exception as e:
        log.warning("api_config_drift: %s", e)
        return jsonify(ok=False, error=_fehler_text(e, "api_config_drift")), 500


@bp.route("/api/system/config_snapshot")
def api_system_config_snapshot():
    """Sanitisierter Config-Überblick (ohne Secrets) — für Support/Doku.

    v4.2-W1: die Geheimnisse erreichen dieses Modul GAR NICHT. Der Bot legt
    nur `HAT_…`-Booleans in den Kontext; im Monolithen stand hier
    `has(DASHBOARD_TOKEN)` mit dem Wert in Reichweite. Für eine Antwort, die
    ohnehin nur true/false ist, war das unnötige Angriffsfläche.
    """
    c = _c().cfg
    snap = {
        # v4.2: nicht mehr globals().get("BOT_VERSION", "?") — in einem
        # Blueprint ist das der falsche Namensraum und haette dauerhaft "?"
        # gemeldet. Dieselbe Falle wie bei /api/version (siehe W33).
        "version": _nc_version.VERSION,
        "build": c.get("BUILD_STAMP") or _nc_version.build_stamp(),
        "restream": {"kick_creds": c["HAT_KICK_CREDS"],
                     "kick_channel": c["KICK_CHANNEL_URL"] or None,
                     "restream_enabled": c["RESTREAM_ENABLED"]},
        "egress": {"tunnel_configured": c["HAT_RECORD_PROXY"],
                   "proxy_pool": c["PROXY_POOL_GROESSE"]},
        "ai": {"model": c["AI_MODEL"],
               "backend": ("brain" if os.getenv("AI_PROVIDER","").strip().lower()=="brain"
                           else "freeai"),
               "budget_per_min": c["AZRAEL_MAX_CALLS_MIN"]},
        "automation": {k: c["_AUTOMATION"].get(k) for k in c["_AUTOMATION"]},
        "discord": {"bot_token_set": c["HAT_DISCORD_BOT_TOKEN"],
                    "guild": c["HAT_DISCORD_GUILD"],
                    "webhook_set": c["HAT_DISCORD_WEBHOOK"],
                    "upload_limit_mb": _nc_dclimits.aktuell_mb(),
                    "upload_limit_label": _nc_dclimits.aktuell_label()},
        "security": {"dashboard_auth": c["HAT_DASHBOARD_TOKEN"],
                     "rate_limit_per_min": c["DASHBOARD_RATE_LIMIT_PER_MIN"]},
        "voice": {"piper": _nc_piper.available(), "whisper": _nc_whisper.verfuegbar()},
    }
    return jsonify(ok=True, snapshot=snap)


@bp.route("/api/system/check_timing")
def api_check_timing():
    """B127-PERF: Messwerte statt Bauchgefuehl fuer drei Stellschrauben.

    * Polling: Dauer der Live-Checks gegen das eingestellte Intervall.
    * Whisper: Echtzeitfaktor (RTF). >1 heisst, die Transkription ist
      langsamer als das Audio spielt — dann hilft nur ein kleineres Modell.
    * Restream: laeuft gerade ein Ziel im Transcode (2-4 Kerne) statt copy?
    """
    c = _c().cfg
    _rs = {}
    try:
        # v4.2-W1: der Manager liegt seit W18 als Register in nc/rsstate.py.
        # Vor dem Start ist er None — dann bleibt die Zielliste leer, statt
        # dass die ganze Antwort an einem AttributeError stirbt.
        _mgr = _nc_rsstate.MGR["obj"]
        if _mgr is not None:
            for rid, st in _mgr.status().items():
                _rs[rid] = {"transcode": st.get("transcode"),
                            "uptime_s": st.get("uptime_s"),
                            "speed": (st.get("health") or {}).get("speed"),
                            "slow_ticks": (st.get("health") or {}).get("slow_ticks", 0)}
    except Exception:
        pass
    _mess = c["_CHECK_TIMING"]
    _w = c["_WHISPER_STATE"]
    return jsonify(
        ok=True,
        polling={"messungen": _mess["n"], "mittel_ms": round(_mess["avg_ms"]),
                 "spitze_ms": round(_mess["max_ms"]),
                 "ueber_intervall": _mess["over_interval"],
                 "anteil_prozent": (round(100 * _mess["over_interval"] / _mess["n"])
                                    if _mess["n"] else 0),
                 "intervalle": c["ADAPTIVE_INTERVALS"],
                 "urteil": (_t("noch zu wenige Messungen") if _mess["n"] < 50 else
                            _t("Checks überholen sich — Intervall erhöhen")
                            if _mess["over_interval"] > _mess["n"] * 0.2
                            else _t("unauffällig"))},
        whisper={"modell": _nc_whisper.MODELL["name"], "compute": c["WHISPER_COMPUTE"],
                 "threads": c["WHISPER_THREADS"], "chunk_s": c["WHISPER_CHUNK_SECS"],
                 "laeufe": _w.get("runs", 0),
                 "rtf_letzter": _w.get("last_rtf"),
                 "rtf_mittel": _w.get("rtf_avg"),
                 "laeufe_ueber_echtzeit": _w.get("slow_runs", 0),
                 "gedrosselt": _w.get("throttled", False),
                 "urteil": (_t("noch keine Messung") if not _w.get("rtf_avg")
                            else _t("langsamer als Echtzeit — kleineres Modell")
                            if _w["rtf_avg"] > 1.0 else _t("unauffällig"))},
        restream={"ziele": _rs,
                  "transcode_default": c["RESTREAM_TRANSCODE"],
                  "hinweis": _t("Transcode kostet 2-4 Kerne (x264 veryfast). "
                                "copy=false überall ist der günstige Zustand.")},
        retention={"checks_tage": c["CHECKS_RETENTION_DAYS"],
                   "checks_max": c["CHECKS_MAX_ROWS"],
                   "eventlog_tage": c["EVENTLOG_RETENTION_DAYS"],
                   "ailog_tage": c["AI_LOG_RETENTION_DAYS"],
                   "snapshots_ausduennen_ab_tage": c["SNAPSHOT_THIN_AFTER_DAYS"],
                   "overlay_tage_ohne_spenden": c["OVERLAY_RETENTION_DAYS"]})


@bp.route("/api/system/preflight")
def api_system_preflight():
    """Professioneller Ops-Check: verifiziert jedes kritische Subsystem und
       liefert eine farbcodierte Scorecard (ok/warn/fail) + Gesamturteil.
       Ausschließlich lesend — verändert nichts."""
    import shutil as _sh
    c = _c().cfg
    checks = []

    def add(cat, name, status, detail):
        checks.append({"cat": cat, "name": name, "status": status, "detail": detail})

    # ── Core ──
    try:
        with db_conn() as conn:
            conn.execute("SELECT 1").fetchone()
        add("Core", "Datenbank", "ok", "erreichbar")
    except Exception as e:
        add("Core", "Datenbank", "fail", _fehler_text(e, "api_system_preflight")[:80])
    try:
        # v4.2-W4: kein globals()-Test mehr. Im Monolithen war das eine
        # Absicherung gegen eine noch nicht gesetzte Konstante; in einem
        # Blueprint ist globals() der Namensraum DIESER Datei, der Test
        # waere dauerhaft False und der Pfad still "/" — gemessen wuerde
        # dann die Systemplatte statt des Aufnahme-Verzeichnisses.
        du = _sh.disk_usage(_c().recordings_dir)
        free_pct = 100 * du.free / du.total
        free_gb = du.free / (1024 ** 3)
        st = "ok" if free_pct >= 15 else ("warn" if free_pct >= 5 else "fail")
        add("Core", "Speicherplatz", st, f"{free_gb:.0f} GB frei ({free_pct:.0f}%)")
    except Exception as e:
        add("Core", "Speicherplatz", "warn", _fehler_text(e, "api_system_preflight")[:60])
    try:
        ok_w = os.access(c["LOG_DIR"], os.W_OK)
        add("Core", "Log-Verzeichnis", "ok" if ok_w else "warn",
            c["LOG_DIR"] if ok_w else "nicht beschreibbar")
    except Exception:
        add("Core", "Log-Verzeichnis", "warn", "unbekannt")

    # ── Recording ──
    for b, crit in (("ffmpeg", True), ("ffprobe", True), ("yt-dlp", False), ("streamlink", False)):
        p = _sh.which(b)
        if p:
            add("Aufnahme", b, "ok", "installiert")
        else:
            add("Aufnahme", b, "fail" if crit else "warn",
                "FEHLT (kritisch)" if crit else "fehlt (Fallback-Tier)")
    eff = _nc_proxyutil.tunnel_effective()
    lt = _nc_proxyutil.tunnel_state().get("last_test")
    if eff:
        if lt and lt.get("ok"):
            add("Aufnahme", "Egress-Tunnel", "ok", f"aktiv · letzter Test HTTP {lt.get('http_code')}")
        else:
            add("Aufnahme", "Egress-Tunnel", "ok", "aktiv (noch nicht getestet)")
    else:
        add("Aufnahme", "Egress-Tunnel", "warn", "direkt (kein Tunnel)")

    # ── Restream ──
    add("Restream", "Kick-Zugang", "ok" if c["HAT_KICK_CREDS"] else "warn",
        "Client-Creds gesetzt" if c["HAT_KICK_CREDS"] else "keine Kick-Creds")
    add("Restream", "Kick-Kanal", "ok" if c["KICK_CHANNEL_URL"] else "warn",
        c["KICK_CHANNEL_URL"] or "keine Kanal-URL")
    add("Restream", "Multi-Kick-Failover",
        "ok" if c["HAT_KICK_BACKUP"] else "warn",
        "Backup-Ingest scharf" if c["HAT_KICK_BACKUP"]
        else "kein Backup-Ingest (optional)")

    # ── KI ──
    add("KI", "Modell", "ok" if c["AI_MODEL"] else "warn", c["AI_MODEL"] or "kein Modell")
    ai_ok = _nc_probe.ai_alive(timeout=3)
    add("KI", "LLM-Endpoint", "ok" if ai_ok else "warn",
        "Brain-Runtime/freeai erreichbar" if ai_ok
        else "kein LLM erreichbar (Brain + freeai-Basen down)")

    # ── Community ──
    dc_ok = bool(_nc_discordstate.CLIENT["obj"] and getattr(_nc_discordstate.CLIENT["obj"], "user", None))
    # B120: Ohne Reconnect-Zaehler und letzten Grund war "nicht verbunden"
    # nicht von "nie konfiguriert" zu unterscheiden — der stille Gateway-
    # Tod blieb monatelang unsichtbar.
    if dc_ok:
        _dc_detail = f"online als {_nc_discordstate.CLIENT['obj'].user}"
        if _nc_discordstate.SESSION.get("reconnects"):
            _dc_detail += f" · {_nc_discordstate.SESSION['reconnects']} Reconnects"
    elif not c["HAT_DISCORD_BOT_TOKEN"]:
        _dc_detail = "kein DISCORD_BOT_TOKEN gesetzt"
    else:
        _dc_detail = "nicht verbunden"
        if _nc_discordstate.SESSION.get("last_error"):
            _dc_detail += f" · letzter Grund: {_nc_discordstate.SESSION['last_error'][:120]}"
        if _nc_discordstate.SESSION.get("last_disconnect"):
            _dc_detail += (f" · seit {int((time.time() - _nc_discordstate.SESSION['last_disconnect']) // 60)} min")
    add("Community", "Discord-Bot",
        "ok" if dc_ok else ("warn" if not c["HAT_DISCORD_BOT_TOKEN"] else "err"),
        _dc_detail)
    add("Community", "Webhook", "ok" if c["HAT_DISCORD_WEBHOOK"] else "warn",
        "konfiguriert" if c["HAT_DISCORD_WEBHOOK"] else "kein Webhook (Broadcast/Alerts aus)")

    # ── Voice ──
    add("Voice", "Piper TTS", "ok" if _nc_piper.available() else "warn",
        "verfügbar" if _nc_piper.available() else "nicht installiert (optional)")
    add("Voice", "faster-whisper", "ok" if _nc_whisper.verfuegbar() else "warn",
        "verfügbar" if _nc_whisper.verfuegbar() else "nicht installiert (Oracle/Transkript aus)")

    # ── Sicherheit ──
    add("Sicherheit", "Dashboard-Auth", "ok" if c["HAT_DASHBOARD_TOKEN"] else "warn",
        "Token aktiv (extern erzwungen, Loopback frei)" if c["HAT_DASHBOARD_TOKEN"]
        else "kein Token (nur lokal betreiben!)")
    add("Sicherheit", "Rate-Limiting", "ok",
        f"{c['DASHBOARD_RATE_LIMIT_PER_MIN']}/min · {c['DASHBOARD_RATE_LIMIT_WRITE_PER_MIN']}/min schreibend (localhost frei)")
    add("Sicherheit", "Security-Header", "ok", "nosniff · X-Frame · Referrer-Policy")

    fails = sum(1 for c in checks if c["status"] == "fail")
    warns = sum(1 for c in checks if c["status"] == "warn")
    overall = "fail" if fails else ("warn" if warns else "ok")
    def _hist():
        try:
            with db_conn() as conn:
                conn.execute("INSERT INTO preflight_history (overall, fails, warns, created_at) "
                             "VALUES (?,?,?,?)",
                             (overall, fails, warns, datetime.now(timezone.utc).isoformat()))
                conn.execute("DELETE FROM preflight_history WHERE id NOT IN "
                             "(SELECT id FROM (SELECT id FROM preflight_history ORDER BY id DESC LIMIT 500) _k)")
        except Exception:
            pass
    # B74-Fix: _spawn(asyncio.to_thread(...)) braucht einen LAUFENDEN Event-Loop —
    # diese Route läuft aber im Flask-Thread (kein Loop) → RuntimeError bei JEDEM
    # Preflight-Poll. _hist ist reine synchrone DB-Arbeit → Daemon-Thread reicht.
    threading.Thread(target=_hist, name="pf-hist", daemon=True).start()
    return jsonify(ok=True, overall=overall, fails=fails, warns=warns,
                   total=len(checks), checks=checks)


@bp.route("/api/system/resilience")
def api_system_resilience():
    """F103: Bündelt Watchdog, Disk-Guard, Sign-Key-Health, Multistream & KI-
       Tiefe (Story-Gedächtnis) für ein Dashboard-Resilienz-Panel."""
    c = _c().cfg
    pct, st = _nc_probe.disk_pct()
    stories = {u: s.snapshot() for u, s in list(c["_STORY_MEMORIES"].items())}
    return jsonify(
        ok=True,
        watchdog={"enabled": c["WATCHDOG_ENABLED"], "last_scan": c["_WATCHDOG_STATE"]["last_scan"],
                  "stalls": [k for k, v in c["_WATCHDOG_STATE"]["stalls"].items() if v],
                  "heartbeats": {k: round(time.monotonic() - v, 1) for k, v in c["_HEARTBEATS"].items()}},
        disk={"pct": pct, "autoclean": c["DISK_AUTOCLEAN"], "threshold": c["DISK_AUTOCLEAN_PCT"],
              "target": c["DISK_AUTOCLEAN_TARGET"], "last_freed_mb": c["_DISK_GUARD_STATE"]["freed_mb"],
              "last_deleted": c["_DISK_GUARD_STATE"]["deleted"], "active": c["_DISK_GUARD_STATE"]["active"],
              "free_gb": round(st.free / 1024**3, 1) if st else None},
        sign={"ok": c["_SIGN_HEALTH"]["ok"], "key_set": c["_SIGN_HEALTH"]["key_set"],
              "detail": c["_SIGN_HEALTH"]["detail"], "checked": c["_SIGN_HEALTH"]["checked"],
              "cooldown_min": max(0, int((c["_SIGN_COOLDOWN"]["until"] - time.time()) // 60))},
        multistream={"kick": True,
                     "youtube": {"enabled": c["YOUTUBE_ENABLED"], "configured": c["HAT_YOUTUBE_KEY"]},
                     "twitch": {"enabled": c["TWITCH_ENABLED"], "configured": c["HAT_TWITCH_KEY"]},
                     "active_extra": [n for n, _ in _nc_rst.multistream_targets()]},
        ai={"story_memory": c["STORY_MEMORY"], "hype_clip": c["HYPE_CLIP_AUTO"],
            "directors": len(c["_LIVE_DIRECTORS"]), "stories": stories},
        # V37-B98: CPU-Konkurrenz sichtbar machen. Ohne GPU teilen sich
        # Encoder, Whisper und llama.cpp dieselben Kerne — wer wie viel
        # bekommt, entscheidet, ob das Sendebild ruckelt.
        cpu={"cores": os.cpu_count(),
             # V37-CPU: die harten Zahlen. Load > Kerne = Ueberbuchung; Load
             # zaehlt auch Prozesse im I/O-Wait, deshalb steht Swap daneben —
             # ein vollgelaufener Swap treibt die Load hoch, ohne dass eine
             # CPU rechnet.
             "load": _nc_probe.cpu_load_snapshot(),
             "ffmpeg_threads": {"live": c["FFMPEG_THREADS_LIVE"],
                                "relay": c["FFMPEG_THREADS_RELAY"],
                                "record": c["FFMPEG_THREADS_RECORD"],
                                "background": _c().ffmpeg_threads_bg,
                                "nice_bg": _c().ffmpeg_nice_bg,
                                "nice_record": c["FFMPEG_NICE_RECORD"]},
             "restream_live": len(c["_RESTREAM_ACTIVE_ALL"]),
             "whisper": {"throttled": c["_WHISPER_STATE"]["throttled"],
                         "throttle_enabled": c["WHISPER_THROTTLE_LIVE"],
                         "max_conc": c["WHISPER_MAX_CONC"],
                         "threads_each": c["WHISPER_THREADS"],
                         "runs": c["_WHISPER_STATE"]["runs"],
                         "throttled_runs": c["_WHISPER_STATE"]["throttled_runs"],
                         "dropped_segments": sum(c["_LIVE_REACT_DROPPED"].values())},
             "encoder": {"preset": c["RESTREAM_X264_PRESET"],
                         "relay_preset": c["RESTREAM_RELAY_PRESET"],
                         "mode": c["RESTREAM_MULTI_MODE"]},
             "brain_llm": os.getenv("AI_PROVIDER", "").strip().lower() == "brain"})
