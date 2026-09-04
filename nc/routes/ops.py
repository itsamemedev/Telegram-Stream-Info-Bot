"""nc.routes.ops — die Routen unter /api/ops,/api/tunnel,/api/update als Flask-Blueprint.

Welle 3 der Zerlegung (siehe docs/MODULARISIERUNG.md), erzeugt mit
tools/bp_extract.py. Pfade stehen woertlich in den Dekoratoren (kein
url_prefix); app-weite Hooks bleiben auf der App; was der Monolith weiterhin
stellen muss, kommt ueber nc.ctx statt ueber einen Import aus bot.py.
"""

from datetime import datetime, timedelta, timezone
import os
import re
import shutil
import subprocess
from flask import Blueprint, jsonify, request
from nc.dbwrap import db_conn
from flask import current_app
import time as _time_mod
from nc import i18n as _nc_i18n
from nc import restrend as _nc_restrend
from nc import fehlertext as _nc_fehlertext
from nc import ffver as _nc_ffver
from nc import updater as _nc_updater
from nc.proxyutil import _tunnel_mask
from nc import proxyutil as _nc_proxyutil

from nc import ctx as _ctx

bp = Blueprint("ops", __name__)


def _fehler_text(e, wo=""):
    """v4.1-W30: der Wortlaut geht ins Log, nach aussen die gesaeuberte
       Fassung — ohne Pfade, ohne Zugangsdaten, gekuerzt. Siehe
       nc/fehlertext.py, dort steht auch, warum nicht einfach "interner
       Fehler"."""
    return _nc_fehlertext.nach_aussen(e, wo)

def _t(s):
    """v4.1-W20: an der Quelle uebersetzen. Diese Texte erreichen das DOM
       meist verkettet ("Fehler: " + error) — ein Katalogeintrag fuer den
       blossen Text traefe dort nie."""
    return _nc_i18n.t(s)



def _c():
    """Laufzeitkontext. Aufruf statt Modul-Konstante — der Kontext wird erst
       beim Bot-Start gefuellt."""
    return _ctx.get()


class _LazyLog:
    def __getattr__(self, name):
        return getattr(_c().log, name)


log = _LazyLog()


_FFMPEG_VER_CACHE = {"v": None}


def _ffmpeg_version_str():
    """ffmpeg-Version (gecached). Leerer String wenn nicht ermittelbar."""
    if _FFMPEG_VER_CACHE["v"] is not None:
        return _FFMPEG_VER_CACHE["v"]
    ver = ""
    try:
        import subprocess as _sp
        out = _sp.run(["ffmpeg", "-version"], capture_output=True, text=True, timeout=4)
        # v4.0-W61: Parsen der Versionszeile nach nc/ffver.py (bitgenau geprüft).
        ver = _nc_ffver.parse_version(out.stdout)
    except Exception:
        ver = ""
    _FFMPEG_VER_CACHE["v"] = ver
    return ver


@bp.route("/api/ops/logtail")
def api_ops_logtail():
    """v37: letzte N Zeilen des Logs — Betriebseinblick ohne SSH."""
    level = (request.args.get("level") or "debug").lower()
    fname = "error.log" if level == "error" else "debug.log"
    try:
        n = _c().arg_int("n", 90, 10, 300)
    except Exception:
        n = 90
    path = os.path.join(_c().cfg["LOG_DIR"], fname)
    lines = []
    try:
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8", errors="replace") as f:
                lines = f.readlines()[-n:]
    except Exception as e:
        return jsonify(ok=False, error=_fehler_text(e, "api_ops_logtail")), 500
    return jsonify(ok=True, file=fname, lines=[ln.rstrip("\n") for ln in lines])


@bp.route("/api/tunnel/status")
def api_tunnel_status():
    eff = _nc_proxyutil.tunnel_effective()
    return jsonify(ok=True,
                   configured=_tunnel_mask(_nc_proxyutil.record_proxy() or None),
                   override=_tunnel_mask(_nc_proxyutil.tunnel_state().get("override")),
                   forced_off=bool(_nc_proxyutil.tunnel_state().get("forced_off")),
                   active=bool(eff),
                   effective=_tunnel_mask(eff),
                   pool_size=len(_nc_proxyutil.proxy_pool()),
                   last_test=_nc_proxyutil.tunnel_state().get("last_test"))


@bp.route("/api/tunnel/toggle", methods=["POST"])
def api_tunnel_toggle():
    d = request.get_json(silent=True) or {}
    _nc_proxyutil.tunnel_state()["forced_off"] = bool(d.get("off"))
    log.info("v37 Tunnel: forced_off=%s (Dashboard)", _nc_proxyutil.tunnel_state()["forced_off"])
    return jsonify(ok=True, forced_off=_nc_proxyutil.tunnel_state()["forced_off"], effective=_tunnel_mask(_nc_proxyutil.tunnel_effective()))


@bp.route("/api/tunnel/set", methods=["POST"])
def api_tunnel_set():
    d = request.get_json(silent=True) or {}
    p = (d.get("proxy") or "").strip()
    if p and not re.match(r"^(socks5h?|https?)://", p):
        return jsonify(ok=False, error=_t("Format: socks5://host:port oder http://host:port")), 400
    _nc_proxyutil.tunnel_state()["override"] = p or None
    log.info("v37 Tunnel: override=%s (Dashboard)", _tunnel_mask(_nc_proxyutil.tunnel_state()["override"]))
    return jsonify(ok=True, override=_tunnel_mask(_nc_proxyutil.tunnel_state()["override"]), effective=_tunnel_mask(_nc_proxyutil.tunnel_effective()))


@bp.route("/api/tunnel/test", methods=["POST"])
def api_tunnel_test():
    """Testet Erreichbarkeit von TikTok über den aktuell effektiven Proxy
       (oder direkt, wenn keiner). Nutzt curl (auf dem Server vorhanden)."""
    eff = _nc_proxyutil.tunnel_effective()
    import subprocess
    cmd = ["curl", "--max-time", "10", "-sS", "-o", "/dev/null",
           "-w", "%{http_code} %{time_total}", "-A", "Mozilla/5.0",
           "https://www.tiktok.com/"]
    if eff:
        cmd = cmd[:1] + ["-x", eff] + cmd[1:]
    t0 = _time_mod.time()
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=14)
        out = (r.stdout or "").strip()
        code = out.split(" ")[0] if out else "0"
        ok = code.startswith(("2", "3"))
        res = {"ok": ok, "http_code": code, "via": _tunnel_mask(eff) or "direkt",
               "ms": int((_time_mod.time() - t0) * 1000),
               "err": (r.stderr or "").strip()[:200] if not ok else None,
               "at": datetime.now(timezone.utc).strftime("%H:%M:%S")}
    except Exception as e:
        res = {"ok": False, "http_code": "0", "via": _tunnel_mask(eff) or "direkt",
               "ms": int((_time_mod.time() - t0) * 1000), "err": _fehler_text(e, "ops-probe"),
               "at": datetime.now(timezone.utc).strftime("%H:%M:%S")}
    _nc_proxyutil.tunnel_state()["last_test"] = res
    return jsonify(res)


@bp.route("/api/ops/resource_history")
def api_ops_resource_history():
    """v4.0-W40: Langzeit-Verlauf von RSS/fds für den Trend-Chart im Dashboard.
       Zeigt schleichendes Wachstum, das die Momentwerte nicht verraten."""
    hist = list(_c().cfg["_RES_HISTORY"])
    fd_series = [p["fds"] for p in hist]
    rss_series = [p["rss_mb"] for p in hist]
    return jsonify(
        ok=True,
        sample_min=_c().cfg["WATCHDOG_RES_SAMPLE_MIN"],
        points=hist,
        fd_trend=_nc_restrend.rising_trend(fd_series, min_points=12,
                                           min_rel_growth=0.30, min_abs_growth=40.0),
        rss_trend=_nc_restrend.rising_trend(rss_series, min_points=12,
                                            min_rel_growth=0.30, min_abs_growth=150.0))


@bp.route("/api/ops/metrics")
def api_ops_metrics():
    """Zeitreihen der letzten 14 Tage: Aufnahmen, KI-Calls, Clips pro Tag."""
    days = 14
    today = datetime.now(timezone.utc).date()
    date_list = [(today - timedelta(days=i)).isoformat() for i in range(days - 1, -1, -1)]
    start = date_list[0]

    def series(table):
        # table stammt aus fixer Whitelist unten → kein Injection-Vektor
        agg = {}
        try:
            with db_conn() as conn:
                for r in conn.execute("SELECT substr(created_at,1,10) AS d, COUNT(*) AS n FROM " + table +
                                      " WHERE created_at >= ? GROUP BY d", (start,)).fetchall():
                    agg[r["d"]] = r["n"]
        except Exception:
            pass
        return [agg.get(dt, 0) for dt in date_list]

    ai_err = {}
    try:
        with db_conn() as conn:
            for r in conn.execute("SELECT substr(created_at,1,10) AS d, COUNT(*) AS n FROM ai_interactions "
                                  "WHERE created_at >= ? AND ok=0 GROUP BY d", (start,)).fetchall():
                ai_err[r["d"]] = r["n"]
    except Exception:
        pass
    return jsonify(ok=True, dates=[d[5:] for d in date_list],
                   recordings=series("recordings"),
                   ai_calls=series("ai_interactions"),
                   ai_errors=[ai_err.get(dt, 0) for dt in date_list],
                   clips=series("discord_clips"))


@bp.route("/api/ops/errors")
def api_ops_errors():
    """Zuverlässigkeit: normalisiert die letzten error.log-Zeilen zu Signaturen
       (User/URLs/Zahlen raus → gleiche Fehler gruppiert), zählt Häufigkeit und
       Trend (letzte Stunde / 24h). Rein lesend."""
    import collections as _collections
    path = os.path.join(_c().cfg["LOG_DIR"], "error.log")
    lines = []
    try:
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8", errors="replace") as f:
                lines = f.readlines()[-1000:]
    except Exception as e:
        return jsonify(ok=False, error=_fehler_text(e, "api_ops_errors")), 500
    now = datetime.now(timezone.utc)
    sig_count = _collections.Counter()
    sig_last, sig_sample = {}, {}
    last_hour = last_24h = 0
    for raw in lines:
        ln = raw.rstrip("\n")
        if not ln.strip():
            continue
        ts = None
        m = re.match(r'(\d{4}-\d{2}-\d{2}[ T]\d{2}:\d{2}:\d{2})', ln)
        if m:
            try:
                ts = datetime.fromisoformat(m.group(1).replace(" ", "T")).replace(tzinfo=timezone.utc)
            except Exception:
                ts = None
        mm = re.search(r'\b(ERROR|WARNING|CRITICAL)\b\s*(.*)$', ln)
        msg = (mm.group(2) if mm else ln).strip()
        sig = re.sub(r'@\w+', '@X', msg)
        sig = re.sub(r'https?://\S+', 'URL', sig)
        sig = re.sub(r'0x[0-9a-fA-F]+', '0xN', sig)
        sig = re.sub(r'\b\d+\b', '#', sig)
        sig = re.sub(r'\s+', ' ', sig).strip()[:90]
        if not sig:
            continue
        sig_count[sig] += 1
        if ts:
            sig_last[sig] = ts.isoformat()[11:19]
        sig_sample.setdefault(sig, msg[:140])
        if ts:
            age = (now - ts).total_seconds()
            if age <= 3600:
                last_hour += 1
            if age <= 86400:
                last_24h += 1
    top = [{"sig": s, "count": c, "last": sig_last.get(s, ""), "sample": sig_sample.get(s, "")}
           for s, c in sig_count.most_common(12)]
    return jsonify(ok=True, scanned=len(lines), last_hour=last_hour, last_24h=last_24h,
                   distinct=len(sig_count), categories=top)


@bp.route("/api/ops/audit")
def api_ops_audit():
    try:
        with db_conn() as conn:
            rows = conn.execute("SELECT method, path, ip, status, created_at FROM audit_log "
                                "ORDER BY id DESC LIMIT 40").fetchall()
        items = [{"method": r["method"], "path": r["path"], "ip": r["ip"], "status": r["status"],
                  "at": (r["created_at"] or "")[5:19].replace("T", " ")} for r in rows]
        return jsonify(ok=True, items=items)
    except Exception as e:
        return jsonify(ok=False, error=_fehler_text(e, "api_ops_audit")), 500


@bp.route("/api/ops/healthcheck")
def api_ops_healthcheck():
    """Detaillierter Health-Check für externes Monitoring (Uptime-Kuma etc).
       Liefert pro Komponente ok/nok + Gesamtstatus ok|degraded|down."""
    checks = {}
    # DB
    try:
        with db_conn() as conn:
            conn.execute("SELECT 1").fetchone()
        checks["database"] = True
    except Exception:
        checks["database"] = False
    # Disk
    disk_ok = True
    disk_pct = None
    try:
        usage = shutil.disk_usage(_c().recordings_dir if os.path.isdir(_c().recordings_dir) else ".")
        disk_pct = round(100.0 * usage.used / usage.total, 1)
        disk_ok = disk_pct < 95.0
    except Exception:
        disk_ok = False
    checks["disk"] = disk_ok
    # Cookies
    try:
        ch = _c().get_cookie_health()
        checks["cookies"] = bool(ch.get("critical_present"))
    except Exception:
        checks["cookies"] = False
    # ffmpeg vorhanden
    try:
        checks["ffmpeg"] = shutil.which("ffmpeg") is not None
    except Exception:
        checks["ffmpeg"] = False
    # Event-Loop des Bots
    try:
        # War globals().get("_MAIN_LOOP") im Monolithen. Im Blueprint waere das
        # ein stilles None — globals() ist hier der Modul-Namensraum. Getter,
        # weil _MAIN_LOOP erst in run_bot() gesetzt wird (W116).
        loop = _c().get_main_loop()
        checks["event_loop"] = bool(loop and loop.is_running())
    except Exception:
        checks["event_loop"] = False
    critical = ["database", "disk"]
    if all(checks.get(c) for c in critical) and all(checks.values()):
        status = "ok"
    elif all(checks.get(c) for c in critical):
        status = "degraded"
    else:
        status = "down"
    code = 200 if status != "down" else 503
    return jsonify(ok=(status != "down"), status=status, checks=checks,
                   disk_used_pct=disk_pct), code


@bp.route("/api/ops/db-stats")
def api_ops_db_stats():
    """Zeilen-Anzahl pro Tabelle + DB-Größe (SQLite). Für Kapazitäts-Monitoring."""
    tables = ["trackings", "recordings", "tiktok_checks", "recording_attempts",
              "event_log", "bookmarks", "tracking_tags", "recording_notes",
              "recording_annotations", "archive", "profile_snapshots",
              "ai_conversations", "ai_messages", "manual_recordings",
              "webhooks", "tracking_collections", "app_config"]
    counts = {}
    try:
        with db_conn() as conn:
            for t in tables:
                try:
                    counts[t] = conn.execute(f"SELECT COUNT(*) AS n FROM {t}").fetchone()["n"]
                except Exception:
                    counts[t] = None
    except Exception as e:
        return jsonify(ok=False, error=_fehler_text(e, "api_ops_db_stats")), 500
    db_size = None
    try:
        if _c().cfg["DB_BACKEND"] != "mariadb" and os.path.exists(_c().cfg["DB_PATH"]):
            db_size = os.path.getsize(_c().cfg["DB_PATH"])
    except Exception:
        pass
    return jsonify(ok=True, backend=_c().cfg["DB_BACKEND"], table_rows=counts,
                   db_size_mb=round(db_size / 1024 / 1024, 2) if db_size else None)


@bp.route("/api/ops/disk-breakdown")
def api_ops_disk_breakdown():
    """Speicherbelegung pro Verzeichnis (recordings/archive/logs) + DB + frei."""
    def _dir_bytes(path):
        total = 0
        if not path or not os.path.isdir(path):
            return 0
        try:
            for root, _dirs, files in os.walk(path):
                for f in files:
                    try:
                        total += os.path.getsize(os.path.join(root, f))
                    except OSError:
                        pass
        except Exception:
            pass
        return total
    out = {}
    try:
        out["recordings_mb"] = round(_dir_bytes(_c().recordings_dir) / 1024 / 1024, 1)
        arch = _c().cfg.get("ARCHIVE_DIR")
        out["archive_mb"] = round(_dir_bytes(arch) / 1024 / 1024, 1) if arch else 0
        logs_dir = os.path.join(os.path.dirname(os.path.abspath(_c().cfg["DB_PATH"])), "logs")
        if not os.path.isdir(logs_dir):
            logs_dir = "logs"
        out["logs_mb"] = round(_dir_bytes(logs_dir) / 1024 / 1024, 1)
        db_mb = 0
        if _c().cfg["DB_BACKEND"] != "mariadb" and os.path.exists(_c().cfg["DB_PATH"]):
            db_mb = os.path.getsize(_c().cfg["DB_PATH"]) / 1024 / 1024
        out["db_mb"] = round(db_mb, 2)
        usage = shutil.disk_usage(_c().recordings_dir if os.path.isdir(_c().recordings_dir) else ".")
        out["free_gb"] = round(usage.free / 1024 / 1024 / 1024, 1)
        out["total_gb"] = round(usage.total / 1024 / 1024 / 1024, 1)
        out["used_pct"] = round(100.0 * usage.used / usage.total, 1)
    except Exception as e:
        return jsonify(ok=False, error=_fehler_text(e, "api_ops_disk_breakdown")), 500
    return jsonify(ok=True, **out)


@bp.route("/api/ops/version")
def api_ops_version():
    """Bot-Version, Uptime, Feature-Anzahl, Python/ffmpeg-Versionen, Schalter."""
    import sys as _sys
    start = _c().get_bot_start_time()
    uptime_s = None
    if start:
        try:
            uptime_s = int((datetime.now(timezone.utc) - start).total_seconds())
        except Exception:
            uptime_s = None
    try:
        # current_app statt dashboard_app: im Request ist beides dieselbe App,
        # aber nur current_app ueberlebt den Umzug in ein Blueprint (W116).
        route_count = len(list(current_app.url_map.iter_rules()))
    except Exception:
        route_count = None
    return jsonify(ok=True,
                   version=_c().cfg.get("BOT_VERSION", "3.7"),
                   build=_c().cfg.get("BUILD_STAMP", ""),
                   uptime_seconds=uptime_s,
                   api_routes=route_count,
                   python=_sys.version.split()[0],
                   ffmpeg=_ffmpeg_version_str(),
                   db_backend=_c().cfg["DB_BACKEND"],
                   prefer_h264=_c().cfg["PREFER_H264"])


@bp.route("/api/update/check")
def api_update_check():
    """Billige Pruefung — ein GitHub-API-Aufruf, kein Download."""
    try:
        res = _nc_updater.check()
    except Exception as e:
        log.error("Update-Pruefung fehlgeschlagen: %s", e, exc_info=True)
        return jsonify(ok=False, error=f"Update-Pruefung: {e}"), 500
    res["job"] = _nc_updater.job_state()
    res["backups"] = _nc_updater.list_backups()[:5]
    res["local_version"] = _c().cfg.get("BOT_VERSION", "")
    res["build"] = _c().cfg.get("BUILD_STAMP", "")
    return jsonify(**res)


@bp.route("/api/update/status")
def api_update_status():
    """Fortschritt des laufenden bzw. Ergebnis des letzten Laufs."""
    return jsonify(ok=True, job=_nc_updater.job_state(),
                   settings=_nc_updater.settings())


@bp.route("/api/update/start", methods=["POST"])
def api_update_start():
    """Update anstossen. dry_run=true rechnet nur durch und schreibt nichts."""
    body = request.get_json(silent=True) or {}
    dry = bool(body.get("dry_run"))
    if not dry and not _c().cfg["UPDATE_ENABLED"]:
        return jsonify(ok=False,
                       error=_t("Update-Schreiben ist abgeschaltet (UPDATE_ENABLED=0).")), 403
    res = _nc_updater.start_update(dry_run=dry)
    return (jsonify(**res), 200 if res.get("ok") else 409)


@bp.route("/api/update/backups")
def api_update_backups():
    return jsonify(ok=True, backups=_nc_updater.list_backups())


@bp.route("/api/update/rollback", methods=["POST"])
def api_update_rollback():
    """Ein Backup zurueckspielen. Ohne Namen das neueste."""
    body = request.get_json(silent=True) or {}
    name = (body.get("backup") or "").strip()
    if not name:
        bl = _nc_updater.list_backups()
        if not bl:
            return jsonify(ok=False, error=_t("Kein Backup vorhanden.")), 404
        name = bl[0]["name"]
    try:
        res = _nc_updater.rollback(name)
    except Exception as e:
        log.error("Rollback fehlgeschlagen: %s", e, exc_info=True)
        return jsonify(ok=False, error=f"Rollback: {e}"), 500
    if res.get("ok"):
        _c().log_event("update_rollback", "warning", f"Backup {name} zurueckgespielt")
    return (jsonify(**res), 200 if res.get("ok") else 500)


@bp.route("/api/update/restart", methods=["POST"])
def api_update_restart():
    """Dienst neu starten — nur wenn UPDATE_RESTART_CMD gesetzt ist.

    Bewusst opt-in: ein Neustart-Kommando, das der Bot selbst kennt, ist ein
    Fernsteuer-Knopf auf das System. Ohne gesetzte Variable nennt die Antwort
    nur das Kommando, das der Operator selbst absetzt."""
    if not _c().cfg["UPDATE_RESTART_CMD"]:
        return jsonify(ok=False, needs_manual=True,
                       hint="sudo systemctl restart tiktok-bot",
                       error=_t("Kein Neustart-Kommando hinterlegt "
                                "(UPDATE_RESTART_CMD). Bitte von Hand neu starten.")), 409
    try:
        # Verzoegert und abgekoppelt: der Neustart killt genau den Prozess, der
        # diese Antwort noch senden muss. Ohne das Fenster sieht der Operator
        # einen Netzwerkfehler statt einer Bestaetigung.
        subprocess.Popen(["sh", "-c", f"sleep 2; {_c().cfg['UPDATE_RESTART_CMD']}"],
                         start_new_session=True,
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception as e:
        log.error("Neustart nicht ausgeloest: %s", e, exc_info=True)
        return jsonify(ok=False, error=f"Neustart nicht ausgeloest: {e}"), 500
    _c().log_event("update_restart", "warning", f"Neustart ausgeloest: {_c().cfg['UPDATE_RESTART_CMD']}")
    return jsonify(ok=True, cmd=_c().cfg["UPDATE_RESTART_CMD"],
                   summary="Neustart in 2 Sekunden — das Dashboard ist kurz weg.")


@bp.route("/api/ops/log-tail")
def api_ops_log_tail():
    """Letzte N Zeilen des debug- oder error-Logs (which=debug|error, lines=N)."""
    # v4.1-W10 (CodeQL py/path-injection): der Dateiname kommt aus einer
    # TABELLE, nicht aus dem Parameter. Die Positivliste von vorher war
    # inhaltlich schon dicht, aber sie schrieb den geprueften Text weiter in
    # den Pfad — fuer Leser wie fuer Pruefwerkzeug bleibt so offen, ob wirklich
    # jeder Weg durch die Pruefung fuehrt. Jetzt kann dort nur noch stehen, was
    # hier steht.
    _DATEIEN = {"debug": "debug.log", "error": "error.log"}
    which = (request.args.get("which") or "debug").lower()
    if which not in _DATEIEN:
        which = "debug"
    try:
        lines = _c().arg_int("lines", 100, 1, 1000)
    except (TypeError, ValueError):
        lines = 100
    logs_dir = os.path.join(os.path.dirname(os.path.abspath(_c().cfg["DB_PATH"])), "logs")
    if not os.path.isdir(logs_dir):
        logs_dir = "logs"
    path = os.path.join(logs_dir, _DATEIEN[which])
    if not os.path.exists(path):
        return jsonify(ok=True, file=path, lines=[], count=0,
                       note="Log-Datei nicht gefunden.")
    try:
        # Effizientes Tail: Datei in Blöcken vom Ende lesen
        with open(path, "rb") as f:
            f.seek(0, os.SEEK_END)
            size = f.tell()
            block = 8192
            data = b""
            while size > 0 and data.count(b"\n") <= lines:
                step = min(block, size)
                size -= step
                f.seek(size)
                data = f.read(step) + data
        text_lines = data.decode("utf-8", errors="replace").splitlines()[-lines:]
        return jsonify(ok=True, file=path, count=len(text_lines), lines=text_lines)
    except Exception as e:
        return jsonify(ok=False, error=_fehler_text(e, "api_ops_log_tail")), 500
