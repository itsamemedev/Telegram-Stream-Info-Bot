"""nc.routes.health — die Routen unter /api/health-score,/api/system-resources als Flask-Blueprint.

Welle 3 der Zerlegung (siehe docs/MODULARISIERUNG.md), erzeugt mit
tools/bp_extract.py. Pfade stehen woertlich in den Dekoratoren (kein
url_prefix); app-weite Hooks bleiben auf der App; was der Monolith weiterhin
stellen muss, kommt ueber nc.ctx statt ueber einen Import aus bot.py.
"""

from datetime import datetime, timedelta, timezone
import os
import shutil
from flask import Blueprint, jsonify
from nc.dbwrap import db_conn
import glob

from nc import ctx as _ctx

bp = Blueprint("health", __name__)


def _c():
    """Laufzeitkontext. Aufruf statt Modul-Konstante — der Kontext wird erst
       beim Bot-Start gefuellt."""
    return _ctx.get()


class _LazyLog:
    def __getattr__(self, name):
        return getattr(_c().log, name)


log = _LazyLog()


@bp.route("/api/health-score")
def api_health_score():
    """Computed health score (0-100) für KPI-Widget. Plus Component-Breakdown
       damit Operator sieht WAS das Problem ist."""
    components = {}

    # Component 1: success_rate_24h
    try:
        with db_conn() as conn:
            row = conn.execute(
                "SELECT COUNT(*) AS total, "
                "  SUM(CASE WHEN outcome IN ('ok', 'stall_killed_partial') "
                "    THEN 1 ELSE 0 END) AS ok_count "
                "FROM recording_attempts "
                "WHERE started_at >= ?",
                ((datetime.now(timezone.utc) - timedelta(hours=24)).isoformat(),)
            ).fetchone()
        total = row["total"] or 0
        ok_count = row["ok_count"] or 0
        if total == 0:
            sr_score = 100   # keine Aufnahmen → keine Probleme
            sr_note = "Keine Aufnahmen in 24h"
        else:
            sr_score = int(100.0 * ok_count / total)
            sr_note = f"{ok_count}/{total} OK ({sr_score}%)"
        components["success_rate"] = {"score": sr_score, "weight": 50, "note": sr_note}
    except Exception as e:
        components["success_rate"] = {"score": 50, "weight": 50, "note": f"error: {e}"}

    # Component 2: cookie_health
    try:
        ck = _c().get_cookie_health()
        if ck.get("status") == "ok":
            cs, cnote = 100, "OK"
        elif ck.get("status") == "warning":
            cs, cnote = 60, "warning"
        elif ck.get("status") == "missing":
            cs, cnote = 0, "fehlen"
        else:
            cs, cnote = 30, ck.get("status", "?")
        components["cookies"] = {"score": cs, "weight": 20, "note": cnote}
    except Exception as e:
        components["cookies"] = {"score": 50, "weight": 20, "note": f"error: {e}"}

    # Component 3: disk_usage (umgekehrt: 100% used → 0 score)
    try:
        st = _c().get_storage_stats()
        pct = (st.get("disk") or {}).get("used_percent")
        if pct is None:
            ds, dnote = 70, "?"
        else:
            # Linear: 0% → 100, 80% → 50, 95% → 10, 100% → 0
            ds = max(0, int(100 - max(0, pct - 30) * 1.5))
            dnote = f"{pct:.0f}% belegt"
        components["disk"] = {"score": ds, "weight": 20, "note": dnote}
    except Exception as e:
        components["disk"] = {"score": 70, "weight": 20, "note": f"error: {e}"}

    # Component 4: bot_alive (trivial 100 — Endpoint antwortet ja)
    components["bot"] = {"score": 100, "weight": 10, "note": "responsive"}

    # Weighted sum
    score = 0
    total_w = 0
    for c in components.values():
        score += c["score"] * c["weight"]
        total_w += c["weight"]
    overall = int(score / total_w) if total_w else 0
    # Label für Operator
    if   overall >= 85: label = "OK"
    elif overall >= 60: label = "DEGRADED"
    elif overall >= 30: label = "WARNING"
    else:               label = "CRITICAL"
    return jsonify({
        "score": overall,
        "label": label,
        "components": components,
    })


@bp.route("/api/system-resources")
def api_system_resources():
    """F19: Disk/Memory/Uptime aus stdlib (kein psutil als Dep)."""
    out = {"recordings_dir": _c().recordings_dir}
    # Disk-Usage des Recordings-Verzeichnisses
    try:
        st = shutil.disk_usage(_c().recordings_dir if os.path.isdir(_c().recordings_dir) else ".")
        out["disk_total_gb"]  = round(st.total / 1024**3, 1)
        out["disk_used_gb"]   = round((st.total - st.free) / 1024**3, 1)
        out["disk_free_gb"]   = round(st.free / 1024**3, 1)
        out["disk_percent"]   = round((st.total - st.free) / st.total * 100, 1)
    except Exception:
        out["disk_total_gb"] = out["disk_used_gb"] = out["disk_free_gb"] = out["disk_percent"] = None

    # Memory aus /proc/meminfo (Linux)
    out["mem_total_gb"] = out["mem_avail_gb"] = out["mem_percent"] = None
    try:
        meminfo = {}
        with open("/proc/meminfo") as f:
            for line in f:
                k, _, v = line.partition(":")
                meminfo[k.strip()] = v.strip()
        total_kb = int(meminfo["MemTotal"].split()[0])
        avail_kb = int(meminfo["MemAvailable"].split()[0])
        out["mem_total_gb"]  = round(total_kb / 1024**2, 1)
        out["mem_avail_gb"]  = round(avail_kb / 1024**2, 1)
        out["mem_percent"]   = round((total_kb - avail_kb) / total_kb * 100, 1)
    except Exception: pass

    # v37 Welle 1: CPU-Last aus /proc/loadavg (kein psutil nötig)
    out["cores"] = os.cpu_count() or 1
    out["load1"] = out["load5"] = out["load15"] = out["load_percent"] = None
    try:
        with open("/proc/loadavg") as _lf:   # Tiefenbughunt: with statt open()-Leak
            la = _lf.read().split()
        out["load1"], out["load5"], out["load15"] = float(la[0]), float(la[1]), float(la[2])
        out["load_percent"] = round(100 * out["load1"] / max(1, out["cores"]), 1)
    except Exception:
        pass

    # Load average
    try:
        out["load_1"], out["load_5"], out["load_15"] = os.getloadavg()
    except Exception:
        out["load_1"] = out["load_5"] = out["load_15"] = None

    # Bot-Uptime
    _start = _c().get_bot_start_time()      # spaet lesen, siehe nc/ctx.py
    if _start:
        out["uptime_secs"] = int((datetime.now(timezone.utc) - _start).total_seconds())
    else:
        out["uptime_secs"] = 0

    # Recordings-Disk-Footprint
    rec_size = 0; rec_files = 0
    try:
        for f in glob.glob(os.path.join(_c().recordings_dir, "*.mp4")):
            try:
                rec_size += os.path.getsize(f); rec_files += 1
            except OSError: pass
    except Exception: pass
    out["recordings_size_mb"] = round(rec_size / 1024**2, 1)
    out["recordings_count"] = rec_files

    # F54: Bot-Prozess-spezifische Stats — RSS, FDs, Threads.
    # Lesbar aus /proc/self/* ohne psutil-Dependency. Direkt relevant für
    # "warum stirbt ffmpeg mit rc=-9?" — wenn der Bot über RSS=2GB ist,
    # ist OOM-Killer wahrscheinlich. Wenn FDs ungewöhnlich hoch (1000+),
    # leaken wir Sockets/Files irgendwo.
    out["bot_rss_mb"] = None
    out["bot_threads"] = None
    out["bot_open_fds"] = None
    try:
        with open("/proc/self/status") as f:
            for line in f:
                if line.startswith("VmRSS:"):
                    out["bot_rss_mb"] = round(int(line.split()[1]) / 1024, 1)
                elif line.startswith("Threads:"):
                    out["bot_threads"] = int(line.split()[1])
    except Exception: pass
    try:
        out["bot_open_fds"] = len(os.listdir("/proc/self/fd"))
    except Exception: pass

    # F54: ffmpeg/yt-dlp Prozess-Count — zeigt ob Recordings tatsächlich laufen
    # (vs DB sagt recording=1 aber Prozess weg → der R1-Reaper greift hier).
    out["ffmpeg_procs"] = None
    out["ytdlp_procs"] = None
    try:
        ff = yt = 0
        for pid_dir in os.listdir("/proc"):
            if not pid_dir.isdigit(): continue
            try:
                with open(f"/proc/{pid_dir}/comm") as f:
                    comm = f.read().strip()
                if comm == "ffmpeg": ff += 1
                elif comm in ("yt-dlp", "yt_dlp"): yt += 1
            except (OSError, IOError):
                continue
        out["ffmpeg_procs"] = ff
        out["ytdlp_procs"]  = yt
    except Exception: pass

    return jsonify(out)
