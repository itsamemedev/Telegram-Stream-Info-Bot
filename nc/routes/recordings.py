"""nc.routes.recordings — die Aufnahmen-Routen als Flask-Blueprint.

Welle 2 der Zerlegung (v4.0-W106, siehe docs/MODULARISIERUNG.md): 34 Routen und
fuenf Helfer, die ausschliesslich diese Routen benutzen, verbatim aus bot.py
geloest. Der Monolith registriert das Blueprint nur noch.

Warum Blueprints hier verhaltensneutral sind: die Pfade stehen woertlich in den
Dekoratoren (kein url_prefix), und im ganzen Projekt gibt es KEIN einziges
url_for() — das Dashboard spricht /api/... als Zeichenkette an. Damit ist die
einzige Aenderung der Endpunkt-NAME (api_recordings_list ->
recordings.api_recordings_list), und den liest niemand.

Was bewusst NICHT mitgewandert ist:
  * Die app-weiten Hooks (before_request/after_request/errorhandler) bleiben auf
    der App. Als Blueprint-Hook wuerden sie nur noch fuer dieses Blueprint
    gelten — eine stille Verhaltensaenderung, genau die Sorte, die niemand
    bemerkt.
  * trigger_manual_recording und stop_manual_recording bleiben im Bot: das
    erste haengt am Recorder-Kern (_spawn, build_recording_cmd), und beide
    teilen sich das Dict _MANUAL_RECORDINGS. Geteilten veraenderlichen Zustand
    ueber zwei Module zu verteilen waere ein Rueckschritt, kein Fortschritt.

Alles, was der Monolith weiterhin bereitstellen muss, kommt ueber nc.ctx —
nicht ueber einen Import aus bot.py. Die Architektur-Grenze haelt.
"""

import asyncio
import json
import os
import shutil
import signal as _signal_mod
from datetime import datetime, timedelta, timezone
from typing import Optional

from flask import Blueprint, jsonify, request

from nc import ctx as _ctx
from nc import recdb
from nc import inspectcache as _nc_inspectcache
from nc import ffbuild as _nc_ffbuild
from nc.dbwrap import db_conn
from nc.archive import compute_recording_fingerprint, _retention_match
from nc.ffdiag import _rec_quality
from nc.notes import add_annotation, set_recording_note, toggle_bookmark
from nc.recdiag import disconnect_analysis as _rd_analysis, url_refresh_stats as _rd_refresh
from nc.scoring import compute_quality_score

bp = Blueprint("recordings", __name__)


def _c():
    """Kurzform fuer den Laufzeitkontext. Bewusst ein Aufruf und keine
       Modul-Konstante: der Kontext wird erst beim Bot-Start gefuellt, ein
       Import-Zeit-Zugriff waere immer None."""
    return _ctx.get()


class _LazyLog:
    """Leitet log.info/warning/error an den Bot-Logger weiter, ohne ihn beim
       Import einzufrieren. Damit bleiben die verschobenen Rumpfe woertlich."""

    def __getattr__(self, name):
        return getattr(_c().log, name)


log = _LazyLog()


def _arg_int(*a, **kw):
    return _c().arg_int(*a, **kw)


def log_event(*a, **kw):
    return _c().log_event(*a, **kw)


async def ffprobe_inspect(filepath: str) -> Optional[dict]:
    """ffprobe -show_format -show_streams JSON-Output. None bei Fehler."""
    if not filepath or not os.path.isfile(filepath):
        return None
    if not shutil.which("ffprobe"):
        return None
    cmd = [
        "ffprobe", "-v", "error",
        "-print_format", "json",
        "-show_format", "-show_streams",
        filepath,
    ]
    proc = None
    try:
        proc = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.DEVNULL)
        out, _ = await asyncio.wait_for(proc.communicate(), timeout=20)
        if proc.returncode != 0:
            return None
        return json.loads(out.decode("utf-8", errors="replace"))
    except asyncio.TimeoutError:
        if proc:
            try: proc.kill()
            except Exception: pass
            try: await asyncio.wait_for(proc.wait(), timeout=2)
            except Exception: pass
        return None
    except Exception as e:
        log.debug(f"ffprobe_inspect({filepath}): {e}")
        return None


def store_inspect(recording_id: int, data: dict, file_hash: Optional[str] = None):
    try:
        with db_conn() as conn:
            conn.execute(
                "DELETE FROM recording_inspect_cache WHERE recording_id=?",
                (recording_id,))
            conn.execute(
                "INSERT INTO recording_inspect_cache "
                "(recording_id, inspect_json, file_hash, inspected_at) "
                "VALUES (?,?,?,?)",
                (recording_id,
                 _nc_inspectcache.serialize(data),   # v4.0-W54: json.dumps + 200KB-Deckel
                 file_hash,
                 datetime.now(timezone.utc).isoformat()))
            conn.commit()
    except Exception as e:
        log.warning(f"store_inspect: {e}")


def build_recording_manifest(recording_id: int) -> Optional[dict]:
    """Vollständiges JSON-Manifest für eine Aufnahme: alle Metadaten,
       Inspect-Cache, Annotations, Notes, Bookmark-State, Hash, Tags
       der ursprünglichen Tracking-Quelle."""
    rec = recdb.get_recording_by_id(recording_id)
    if not rec: return None
    rec_dict = dict(rec) if hasattr(rec, 'keys') else None
    if rec_dict is None:
        try:
            rec_dict = {k: rec[k] for k in rec.keys()}
        except Exception:
            return None
    out = {
        "recording_id": rec_dict["id"],
        "username": rec_dict.get("username"),
        "filepath": rec_dict.get("filepath"),
        "filename": os.path.basename(rec_dict.get("filepath") or ""),
        "file_size": rec_dict.get("file_size"),
        "duration_secs": rec_dict.get("duration_secs"),
        "quality_score": rec_dict.get("quality_score"),
        "fingerprint": rec_dict.get("fingerprint"),
        "tracking_id": rec_dict.get("tracking_id"),
        "created_at": rec_dict.get("created_at"),
        "deleted_at": rec_dict.get("deleted_at"),
        "note": recdb.get_recording_note(recording_id),
        "annotations": [],
        "bookmark": False,
        "inspect": recdb.get_or_compute_inspect_sync(recording_id),
        "tags": [],
        "exists_on_disk": rec_dict.get("filepath") and os.path.exists(rec_dict["filepath"]),
    }
    # Annotations
    ann_rows = recdb.get_annotations_for_recording(recording_id)
    out["annotations"] = [{"id": a["id"], "ts": a["timestamp_secs"],
                            "label": a["label"]} for a in ann_rows]
    # Bookmark
    try:
        with db_conn() as conn:
            bm = conn.execute(
                "SELECT 1 FROM bookmarks WHERE recording_id=?",
                (recording_id,)).fetchone()
            out["bookmark"] = bool(bm)
    except Exception: pass
    # Tags vom ursprünglichen Tracking (wenn vorhanden)
    if out["tracking_id"]:
        out["tags"] = _c().get_tags_for_tracking(out["tracking_id"])
    return out


async def compute_waveform_peaks(filepath: str, num_samples: int = 200) -> Optional[list]:
    """Reduziert Audio auf num_samples Peaks für die Waveform-Visualisierung.
       Nutzt ffmpeg -af aresample → astats. Limit: max 200 Samples damit
       das JSON nicht zu groß wird."""
    num_samples = max(1, int(num_samples))   # v4.0-W34: Schutz gegen Division durch 0
    if not filepath or not os.path.isfile(filepath):
        return None
    if not shutil.which("ffmpeg"):
        return None
    num_samples = max(20, min(int(num_samples), 500))

    # Hol Duration via ffprobe für die Sample-Window-Berechnung
    inspect = await ffprobe_inspect(filepath)
    if not inspect:
        return None
    try:
        duration = float((inspect.get("format") or {}).get("duration") or 0)
    except Exception:
        duration = 0
    if duration <= 0:
        return None

    # Sample-Rate für die astats: damit wir num_samples Frames bekommen.
    # Wir benutzen astats=length=duration/num_samples
    bucket_secs = duration / num_samples
    # ffmpeg-cmd: extract RMS per bucket
    cmd = _nc_ffbuild.ff_cmd([
        "ffmpeg", "-v", "error", "-i", filepath,
        "-vn", "-af", f"asetnsamples=n={max(1, int(48000*bucket_secs))}:p=0,astats=metadata=1:reset=1,ametadata=print:key=lavfi.astats.Overall.RMS_level:file=-",
        "-f", "null", "-",
    ], threads=_c().ffmpeg_threads_bg, nice=_c().ffmpeg_nice_bg)   # V37-CPU: reine Analyse, Hintergrund
    proc = None
    try:
        proc = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.DEVNULL)
        out, _ = await asyncio.wait_for(proc.communicate(), timeout=60)
        text = out.decode("utf-8", errors="ignore")
        peaks = []
        for line in text.splitlines():
            if "RMS_level" in line:
                try:
                    val = float(line.split("=")[-1])
                    # dB → linear 0-1 (dB ≤ 0, normaler Wert: -60 to 0)
                    if val < -60: val = -60
                    linear = (val + 60) / 60.0
                    peaks.append(round(linear, 3))
                except Exception: pass
        if not peaks: return None
        # Cap auf num_samples
        if len(peaks) > num_samples:
            step = len(peaks) / num_samples
            sampled = []
            for i in range(num_samples):
                sampled.append(peaks[int(i * step)])
            peaks = sampled
        return peaks
    except asyncio.TimeoutError:
        if proc:
            try: proc.kill()
            except Exception: pass
            try: await asyncio.wait_for(proc.wait(), timeout=2)
            except Exception: pass
        return None
    except Exception as e:
        log.debug(f"compute_waveform_peaks: {e}")
        return None


def _find_orphans():
    """Sucht verwaiste Dateien im _c().recordings_dir: Split-Part-Reste, .repaired,
       sowie Dateien ohne DB-Eintrag."""
    orphans = []
    if not os.path.isdir(_c().recordings_dir):
        return orphans
    try:
        with db_conn() as conn:
            known = set(r["filepath"] for r in
                        conn.execute("SELECT filepath FROM recordings").fetchall())
    except Exception:
        known = set()
    for name in os.listdir(_c().recordings_dir):
        full = os.path.join(_c().recordings_dir, name)
        if not os.path.isfile(full):
            continue
        reason = None
        if "_part" in name or name.endswith(".repaired.mp4") or "_re_" in name:
            reason = "split-rest"
        elif full not in known and name.endswith((".mp4", ".flv", ".ts", ".part")):
            reason = "kein-db-eintrag"
        if reason:
            try:
                orphans.append({"name": name, "path": full,
                                "mb": round(os.path.getsize(full) / 1048576.0, 2),
                                "reason": reason})
            except OSError:
                pass
    return orphans


@bp.route("/api/recordings/<int:tracking_id>/stop", methods=["POST"])
def api_recording_stop(tracking_id):
    """POST. Sendet SIGTERM an die laufende ffmpeg/yt-dlp-Aufnahme dieses
       Trackings. File wird grazil finalisiert (moov-atom geschrieben).
       Returns {ok, pid, username} oder 404 wenn nichts läuft."""
    with db_conn() as conn:
        row = conn.execute(
            "SELECT username, pid, output_file FROM trackings "
            "WHERE id=? AND recording=1", (tracking_id,)).fetchone()
    if not row:
        return jsonify(ok=False,
                       error="kein aktives Recording für dieses Tracking"), 404
    pid = row["pid"]
    if not pid:
        # Edge: recording=1 aber kein pid (Race oder Inkonsistenz).
        # Der Reaper räumt das beim nächsten Lauf weg.
        return jsonify(ok=False, error="recording flag gesetzt aber kein PID — "
                       "Reaper räumt beim nächsten Tick auf"), 409
    # F59-Bug-Fix B36: PID-Reuse-Schutz. Wenn der ffmpeg-Prozess vor Stunden
    # gecrasht ist und der Kernel die PID inzwischen recycled hat, würden
    # wir hier eine fremde Anwendung töten. _proc_is_recorder liest
    # /proc/{pid}/comm und verifiziert dass es noch ffmpeg/yt-dlp ist.
    if not _c().proc_is_recorder(pid):
        return jsonify(ok=False, error=f"PID {pid} ist nicht (mehr) unser "
                       "Recorder-Prozess — wahrscheinlich schon beendet. "
                       "Reaper räumt beim nächsten Tick (5s) auf"), 409
    try:
        # F59: SIGTERM = grazil. ffmpeg flusht buffers + schreibt moov-atom.
        os.kill(pid, _signal_mod.SIGTERM)
        log.info(f"F59: SIGTERM an PID {pid} (@{row['username']}) — "
                 f"Aufnahme wird grazil gestoppt.")
    except ProcessLookupError:
        # Process schon weg — der natürliche Exit kommt jeden Moment.
        # Nichts mehr zu tun.
        return jsonify(ok=True, username=row["username"], pid=pid,
                       note="process bereits beendet, cleanup läuft"), 200
    except PermissionError as e:
        return jsonify(ok=False, error=f"keine Permission den Prozess zu stoppen: {e}"), 500
    except Exception as e:
        return jsonify(ok=False, error=f"kill fehlgeschlagen: {e}"), 500
    return jsonify(ok=True, username=row["username"], pid=pid,
                   message="SIGTERM gesendet — file wird grazil finalisiert")


@bp.route("/api/recordings/list")
def api_recordings_list():
    # v4.0-W95: limit per Query übersteuerbar (Default 50, geklemmt 1..1000, über
    # den gehärteten _arg_int → nie 500). Die Aufnahmen-Timeline holt damit mehr
    # als 50 Sessions, statt ältere still abzuschneiden.
    rows = recdb.get_all_recordings(limit=_arg_int("limit", 50, 1, 1000))
    out = []
    for r in rows:
        # F38-Bugfix: TOCTOU — die Datei kann zwischen os.path.exists() und
        # os.path.getsize() verschwinden (Cleanup-Skript, manuelles rm,
        # Disk-Unmount). getsize() würde dann FileNotFoundError werfen und
        # die ganze Route mit 500 abbrechen. Einmal try/except — wenn Größe
        # nicht ermittelbar, 0 ausgeben.
        # BUG-FIX: file_size aus DB bevorzugen (X-Series-Spalte), nur als
        # Fallback von Disk lesen. Vorher gab die Route NUR size_mb zurück,
        # aber das neue Dashboard liest r.file_size + r.duration_secs →
        # Größen- und Dauer-Spalte blieben leer ("—").
        db_size = None
        try:
            db_size = r["file_size"]
        except Exception:
            db_size = None
        size_bytes = db_size
        if not size_bytes:
            try:
                size_bytes = os.path.getsize(r["filepath"])
            except (OSError, TypeError):
                size_bytes = 0
        dur = None
        try:
            dur = r["duration_secs"]
        except Exception:
            dur = None
        out.append({
            "id": r["id"], "username": r["username"],
            "filename": os.path.basename(r["filepath"]) if r["filepath"] else "",
            "created_at": r["created_at"][:19] if r["created_at"] else "",
            "size_mb": round((size_bytes or 0) / 1024 / 1024, 2),
            "file_size": size_bytes or 0,
            "duration_secs": dur,
        })
    return jsonify(out)


@bp.route("/api/recordings/daily")
def api_recordings_daily():
    """v4.0-W72: Aufnahmen je Tag über ein Fenster (Default 14 Tage), direkt aus
       der DB aggregiert. Das W69-3D-Balkendiagramm baute sein 14-Tage-Histogramm
       vorher client-seitig aus /api/recordings/list — das aber nur die letzten 50
       Zeilen liefert, sodass ältere Tage auf einem 24/7-System still auf 0 fielen
       (und das UTC-Datum gegen die DB-Zeit off-by-one bucketen konnte). Hier wird
       je Kalendertag serverseitig gezählt: exakt und backend-agnostisch (dieselbe
       parametrisierte Datumsfenster-Technik wie _public_stats)."""
    days = _arg_int("days", 14, 1, 90)
    out = []
    total = 0
    try:
        with db_conn() as conn:
            for i in range(days - 1, -1, -1):
                d0 = (datetime.now(timezone.utc) - timedelta(days=i)).date()
                lo = datetime(d0.year, d0.month, d0.day,
                              tzinfo=timezone.utc).isoformat()
                hi = (datetime(d0.year, d0.month, d0.day, tzinfo=timezone.utc)
                      + timedelta(days=1)).isoformat()
                n = conn.execute(
                    "SELECT COUNT(*) AS n FROM recordings "
                    "WHERE deleted_at IS NULL AND created_at >= ? AND created_at < ?",
                    (lo, hi)).fetchone()["n"]
                n = int(n or 0)
                total += n
                out.append({"day": d0.isoformat(), "count": n})
    except Exception as e:
        return jsonify(ok=False, error=str(e), days=[]), 500
    return jsonify(ok=True, days=out, total=total,
                   peak=max((d["count"] for d in out), default=0))


@bp.route("/api/recordings/<int:rid>/inspect")
def api_recording_inspect(rid):
    rec = recdb.get_recording_by_id(rid)
    if not rec:
        return jsonify(ok=False, error="recording not found"), 404
    # Cache first
    cached = recdb.get_or_compute_inspect_sync(rid)
    force = request.args.get("force") == "1"
    if cached and not force:
        return jsonify(ok=True, cached=True, inspect=cached)
    fp = rec["filepath"]
    if not fp or not os.path.exists(fp):
        return jsonify(ok=False, error="file not on disk",
                       inspect=cached), 404
    try:
        data = _c().run_async(ffprobe_inspect(fp), timeout=30)
    except Exception as e:
        return jsonify(ok=False, error=f"ffprobe failed: {e}",
                       inspect=cached), 503
    if not data:
        return jsonify(ok=False, error="ffprobe returned nothing",
                       inspect=cached), 502
    fhash = compute_recording_fingerprint(fp)
    store_inspect(rid, data, fhash)
    return jsonify(ok=True, cached=False, inspect=data)


@bp.route("/api/recordings/<int:rid>/quality")
def api_recording_quality(rid):
    rec = recdb.get_recording_by_id(rid)
    if not rec:
        return jsonify(ok=False, error="recording not found"), 404
    inspect = recdb.get_or_compute_inspect_sync(rid)
    fp = rec["filepath"]
    if not inspect and fp and os.path.exists(fp):
        try:
            inspect = _c().run_async(ffprobe_inspect(fp), timeout=30)
            if inspect:
                store_inspect(rid, inspect, compute_recording_fingerprint(fp))
        except Exception:
            inspect = None
    file_size = rec["file_size"] or (os.path.getsize(fp) if fp and os.path.exists(fp) else 0)
    duration = rec["duration_secs"] or 0
    result = compute_quality_score(inspect or {}, file_size, duration)
    # Persist
    try:
        with db_conn() as conn:
            conn.execute("UPDATE recordings SET quality_score=? WHERE id=?",
                         (result["score"], rid))
            conn.commit()
    except Exception: pass
    return jsonify(ok=True, **result)


@bp.route("/api/recordings/<int:rid>/notes", methods=["GET", "POST", "DELETE"])
def api_recording_notes(rid):
    if request.method == "GET":
        return jsonify(ok=True, note=recdb.get_recording_note(rid) or "")
    if request.method == "DELETE":
        ok = set_recording_note(rid, "")
        return jsonify(ok=ok)
    data = request.get_json(silent=True) or {}
    note = data.get("note", "")
    ok = set_recording_note(rid, note)
    if not ok:
        return jsonify(ok=False, error="recording not found"), 404
    return jsonify(ok=True, note=note.strip()[:5000])


@bp.route("/api/recordings/<int:rid>/bookmark", methods=["POST"])
def api_recording_bookmark(rid):
    return jsonify(ok=True, **toggle_bookmark(rid))


@bp.route("/api/recordings/<int:rid>/annotations", methods=["GET", "POST"])
def api_recording_annotations(rid):
    if request.method == "GET":
        rows = recdb.get_annotations_for_recording(rid)
        return jsonify(ok=True, annotations=[{
            "id": a["id"], "ts": a["timestamp_secs"],
            "label": a["label"], "created_at": a["created_at"],
        } for a in rows])
    data = request.get_json(silent=True) or {}
    ts = data.get("timestamp_secs", 0)
    label = data.get("label", "")
    aid = add_annotation(rid, ts, label)
    if aid is None:
        return jsonify(ok=False, error="invalid annotation or recording not found"), 400
    return jsonify(ok=True, id=aid)


@bp.route("/api/recordings/<int:rid>/manifest")
def api_recording_manifest(rid):
    m = build_recording_manifest(rid)
    if not m:
        return jsonify(ok=False, error="recording not found"), 404
    return jsonify(ok=True, manifest=m)


@bp.route("/api/recordings/<int:rid>/waveform")
def api_recording_waveform(rid):
    rec = recdb.get_recording_by_id(rid)
    if not rec:
        return jsonify(ok=False, error="recording not found"), 404
    fp = rec["filepath"]
    if not fp or not os.path.exists(fp):
        return jsonify(ok=False, error="file not on disk"), 404
    samples = _arg_int("samples", 160, 20, 400)
    try:
        peaks = _c().run_async(compute_waveform_peaks(fp, samples), timeout=70)
    except Exception as e:
        return jsonify(ok=False, error=f"waveform failed: {e}"), 503
    if peaks is None:
        return jsonify(ok=False, error="could not compute waveform"), 502
    return jsonify(ok=True, peaks=peaks, count=len(peaks))


@bp.route("/api/recordings/<int:rid>/fingerprint", methods=["POST"])
def api_recording_fingerprint(rid):
    h = recdb.update_recording_fingerprint(rid)
    if not h:
        return jsonify(ok=False, error="could not compute (file missing?)"), 404
    dupes = recdb.find_recordings_by_fingerprint(h)
    return jsonify(ok=True, fingerprint=h, duplicates=[{
        "id": d["id"], "username": d["username"],
        "filename": os.path.basename(d["filepath"] or ""),
        "size_mb": round((d["file_size"] or 0)/1024/1024, 1),
    } for d in dupes if d["id"] != rid])


@bp.route("/api/recordings/manual/start", methods=["POST"])
def api_manual_start():
    data = request.get_json(silent=True) or {}
    username = (data.get("username") or "").strip()
    duration = data.get("duration_secs", 300)
    if not username:
        return jsonify(ok=False, error="username required"), 400
    try:
        result = _c().run_async(
            _c().trigger_manual_recording(username, duration, session=_c().scraper_session()),
            timeout=60)
    except Exception as e:
        return jsonify(ok=False, error=f"start failed: {e}"), 503
    code = 200 if result.get("ok") else 400
    return jsonify(result), code


@bp.route("/api/recordings/manual/list")
def api_manual_list():
    only_active = request.args.get("active") == "1"
    rows = recdb.get_manual_recordings(50, only_active)
    return jsonify(ok=True, recordings=[{
        "id": r["id"], "username": r["username"],
        "max_duration_secs": r["max_duration_secs"],
        "started_at": r["started_at"], "ended_at": r["ended_at"],
        "status": r["status"],
        "filename": os.path.basename(r["output_file"] or ""),
        "size_mb": round((r["file_size"] or 0)/1024/1024, 1) if r["file_size"] else None,
    } for r in rows])


@bp.route("/api/recordings/manual/<int:mid>/stop", methods=["POST"])
def api_manual_stop(mid):
    return jsonify(_c().stop_manual_recording(mid))


@bp.route("/api/recordings/<int:rid>/trash", methods=["POST"])
def api_recording_trash(rid):
    return jsonify(ok=recdb.soft_delete_recording(rid))


@bp.route("/api/recordings/<int:rid>/restore", methods=["POST"])
def api_recording_restore(rid):
    return jsonify(ok=recdb.restore_recording(rid))


@bp.route("/api/recordings/trash")
def api_trash_list():
    rows = recdb.get_trash_recordings(100)
    return jsonify(ok=True, trash=[{
        "id": r["id"], "username": r["username"],
        "filename": os.path.basename(r["filepath"] or ""),
        "size_mb": round((r["file_size"] or 0)/1024/1024, 1),
        "created_at": r["created_at"], "deleted_at": r["deleted_at"],
    } for r in rows])


@bp.route("/api/recordings/overview")
def api_recordings_overview():
    try:
        with db_conn() as conn:
            total = conn.execute(
                "SELECT COUNT(*) AS c FROM recordings WHERE deleted_at IS NULL"
            ).fetchone()["c"]
            trashed = conn.execute(
                "SELECT COUNT(*) AS c FROM recordings WHERE deleted_at IS NOT NULL"
            ).fetchone()["c"]
            total_bytes = conn.execute(
                "SELECT SUM(COALESCE(file_size,0)) AS s FROM recordings "
                "WHERE deleted_at IS NULL"
            ).fetchone()["s"] or 0
            bookmarked = conn.execute(
                "SELECT COUNT(*) AS c FROM bookmarks").fetchone()["c"]
            with_notes = conn.execute(
                "SELECT COUNT(*) AS c FROM recording_notes").fetchone()["c"]
            annotated = conn.execute(
                "SELECT COUNT(DISTINCT recording_id) AS c FROM recording_annotations"
            ).fetchone()["c"]
            avg_quality = conn.execute(
                "SELECT AVG(quality_score) AS a FROM recordings "
                "WHERE quality_score IS NOT NULL AND deleted_at IS NULL"
            ).fetchone()["a"]
        return jsonify(ok=True,
                       total=total, trashed=trashed,
                       total_gb=round(total_bytes/1024**3, 2),
                       bookmarked=bookmarked, with_notes=with_notes,
                       annotated=annotated,
                       avg_quality=round(avg_quality, 1) if avg_quality else None)
    except Exception as e:
        return jsonify(ok=False, error=str(e)), 500


@bp.route("/api/recordings/dedup-scan", methods=["POST"])
def api_dedup_scan():
    """Berechnet Fingerprints für alle recordings ohne fingerprint und
       gruppiert Duplikate. Limit: 200 files pro Scan (sonst zu langsam)."""
    try:
        with db_conn() as conn:
            rows = conn.execute(
                "SELECT id, filepath FROM recordings "
                "WHERE deleted_at IS NULL AND fingerprint IS NULL "
                "ORDER BY id DESC LIMIT 200").fetchall()
        computed = 0
        for r in rows:
            if r["filepath"] and os.path.exists(r["filepath"]):
                if recdb.update_recording_fingerprint(r["id"]):
                    computed += 1
        # Jetzt Duplikat-Gruppen finden
        with db_conn() as conn:
            dup_rows = conn.execute(
                "SELECT fingerprint, COUNT(*) AS c FROM recordings "
                "WHERE fingerprint IS NOT NULL AND deleted_at IS NULL "
                "GROUP BY fingerprint HAVING COUNT(*) > 1").fetchall()
        groups = []
        for d in dup_rows:
            members = recdb.find_recordings_by_fingerprint(d["fingerprint"])
            groups.append({
                "fingerprint": d["fingerprint"][:16] + "…",
                "count": d["c"],
                "members": [{"id": m["id"], "username": m["username"],
                             "filename": os.path.basename(m["filepath"] or ""),
                             "size_mb": round((m["file_size"] or 0)/1024/1024, 1)}
                            for m in members],
            })
        return jsonify(ok=True, computed=computed, duplicate_groups=groups,
                       group_count=len(groups))
    except Exception as e:
        return jsonify(ok=False, error=str(e)), 500


@bp.route("/api/recordings/<int:rid>/star", methods=["POST"])
def api_recording_star(rid):
    """Markiert/entmarkiert eine Aufnahme als Favorit (toggle oder explizit)."""
    payload = request.get_json(silent=True) or {}
    try:
        with db_conn() as conn:
            row = conn.execute("SELECT starred FROM recordings WHERE id=?", (rid,)).fetchone()
            if not row:
                return jsonify(ok=False, error="Aufnahme nicht gefunden."), 404
            if "starred" in payload:
                new_val = 1 if payload.get("starred") else 0
            else:
                new_val = 0 if (row["starred"] or 0) else 1
            conn.execute("UPDATE recordings SET starred=? WHERE id=?", (new_val, rid))
            conn.commit()
        return jsonify(ok=True, id=rid, starred=bool(new_val))
    except Exception as e:
        return jsonify(ok=False, error=str(e)), 500


@bp.route("/api/recordings/starred")
def api_recordings_starred():
    """Liste aller markierten (starred) Aufnahmen."""
    try:
        with db_conn() as conn:
            rows = conn.execute(
                "SELECT id, username, filepath, file_size, duration_secs, rating, "
                "label, created_at FROM recordings "
                "WHERE starred=1 AND deleted_at IS NULL "
                "ORDER BY created_at DESC LIMIT 200").fetchall()
        out = [{"id": r["id"], "username": r["username"],
                "filename": os.path.basename(r["filepath"] or ""),
                "size_mb": round((r["file_size"] or 0) / 1024 / 1024, 1),
                "duration_secs": r["duration_secs"], "rating": r["rating"],
                "label": r["label"], "created_at": (r["created_at"] or "")[:19]}
               for r in rows]
        return jsonify(ok=True, recordings=out, count=len(out))
    except Exception as e:
        return jsonify(ok=False, error=str(e)), 500


@bp.route("/api/recordings/<int:rid>/rating", methods=["POST"])
def api_recording_rating(rid):
    """Setzt eine 1-5-Bewertung (0/None = löschen)."""
    payload = request.get_json(silent=True) or {}
    raw = payload.get("rating", None)
    if raw in (None, 0, "0", ""):
        rating = None
    else:
        try:
            rating = int(raw)
        except (TypeError, ValueError):
            return jsonify(ok=False, error="rating muss 1-5 sein."), 400
        if not (1 <= rating <= 5):
            return jsonify(ok=False, error="rating muss 1-5 sein."), 400
    try:
        with db_conn() as conn:
            r = conn.execute("SELECT 1 FROM recordings WHERE id=?", (rid,)).fetchone()
            if not r:
                return jsonify(ok=False, error="Aufnahme nicht gefunden."), 404
            conn.execute("UPDATE recordings SET rating=? WHERE id=?", (rating, rid))
            conn.commit()
        return jsonify(ok=True, id=rid, rating=rating)
    except Exception as e:
        return jsonify(ok=False, error=str(e)), 500


@bp.route("/api/recordings/<int:rid>/label", methods=["POST"])
def api_recording_label(rid):
    """Setzt/löscht ein freies Label (z.B. 'Highlight', 'Drama', 'Musik')."""
    payload = request.get_json(silent=True) or {}
    label = (payload.get("label") or "").strip()[:64] or None
    try:
        with db_conn() as conn:
            r = conn.execute("SELECT 1 FROM recordings WHERE id=?", (rid,)).fetchone()
            if not r:
                return jsonify(ok=False, error="Aufnahme nicht gefunden."), 404
            conn.execute("UPDATE recordings SET label=? WHERE id=?", (label, rid))
            conn.commit()
        return jsonify(ok=True, id=rid, label=label)
    except Exception as e:
        return jsonify(ok=False, error=str(e)), 500


@bp.route("/api/recordings/by-label/<label>")
def api_recordings_by_label(label):
    """Aufnahmen mit einem bestimmten Label."""
    try:
        with db_conn() as conn:
            rows = conn.execute(
                "SELECT id, username, filepath, file_size, created_at FROM recordings "
                "WHERE label=? AND deleted_at IS NULL ORDER BY created_at DESC LIMIT 200",
                (label,)).fetchall()
        out = [{"id": r["id"], "username": r["username"],
                "filename": os.path.basename(r["filepath"] or ""),
                "size_mb": round((r["file_size"] or 0) / 1024 / 1024, 1),
                "created_at": (r["created_at"] or "")[:19]} for r in rows]
        return jsonify(ok=True, label=label, recordings=out, count=len(out))
    except Exception as e:
        return jsonify(ok=False, error=str(e)), 500


@bp.route("/api/recordings/labels")
def api_recordings_labels():
    """Alle vergebenen Labels + Anzahl."""
    try:
        with db_conn() as conn:
            rows = conn.execute(
                "SELECT label, COUNT(*) AS n FROM recordings "
                "WHERE label IS NOT NULL AND label <> '' AND deleted_at IS NULL "
                "GROUP BY label ORDER BY n DESC").fetchall()
        return jsonify(ok=True, labels=[{"label": r["label"], "count": int(r["n"])}
                                        for r in rows])
    except Exception as e:
        return jsonify(ok=False, error=str(e)), 500


@bp.route("/api/recordings/disconnects")
def api_recording_disconnects():
    """V37-DISC: Warum enden Aufnahmen? Aggregiert recording_attempts.

    ?days=7 &user=<name>. Zeigt Outcome-Verteilung, die echten ffmpeg-stderr-
    Ursachen (403/404/Timeout/...), Dauer-Verteilung und die Problem-User.
    """
    try:
        days = _arg_int("days", 7, 1, 90)
    except ValueError:
        days = 7
    user = (request.args.get("user") or "").strip().lstrip("@").lower() or None
    try:
        rep = _rd_analysis(days=days, username=user)
        rep["url_refresh"] = _rd_refresh(days=days)
        rep["ok"] = True
        return jsonify(rep)
    except Exception as e:
        log.warning("api_recording_disconnects: %s", e)
        return jsonify(ok=False, error=str(e)), 500


@bp.route("/api/rec/quality/<int:rec_id>")
def api_rec_quality(rec_id):
    """Qualitäts-Score einer Aufnahme."""
    try:
        with db_conn() as conn:
            row = conn.execute("SELECT * FROM recordings WHERE id=?", (rec_id,)).fetchone()
        if not row:
            return jsonify(ok=False, error="recording not found"), 404
        return jsonify(ok=True, id=rec_id, username=row["username"], **_rec_quality(dict(row)))
    except Exception as e:
        return jsonify(ok=False, error=str(e)), 500


@bp.route("/api/rec/classify/<int:rec_id>")
def api_rec_classify(rec_id):
    """Klassifiziert eine Aufnahme: quick / standard / marathon (+Qualität)."""
    try:
        with db_conn() as conn:
            row = conn.execute("SELECT * FROM recordings WHERE id=?", (rec_id,)).fetchone()
        if not row:
            return jsonify(ok=False, error="recording not found"), 404
        d = dict(row)
        dur = d.get("duration_secs") or 0
        cat = ("quick" if dur < 300 else "standard" if dur < 3600 else "marathon")
        return jsonify(ok=True, id=rec_id, username=d["username"], category=cat,
                       duration_secs=dur, quality=_rec_quality(d))
    except Exception as e:
        return jsonify(ok=False, error=str(e)), 500


@bp.route("/api/rec/timeline/<username>")
def api_rec_timeline(username):
    """Chronologische Aufnahme-Timeline eines Streamers (für Gantt/Liste)."""
    username = username.lstrip("@")
    try:
        with db_conn() as conn:
            rows = conn.execute(
                "SELECT id, created_at, file_size, duration_secs, rating, label "
                "FROM recordings WHERE username=? ORDER BY created_at DESC LIMIT 100",
                (username,)).fetchall()
        items = [{"id": r["id"], "at": r["created_at"],
                  "mb": round((r["file_size"] or 0) / 1048576.0, 1),
                  "duration_secs": r["duration_secs"] or 0,
                  "rating": r["rating"], "label": r["label"]} for r in rows]
        return jsonify(ok=True, username=username, count=len(items), timeline=items)
    except Exception as e:
        return jsonify(ok=False, error=str(e)), 500


@bp.route("/api/rec/retention/preview", methods=["POST"])
def api_rec_retention_preview():
    """Vorschau: welche Aufnahmen eine Retention-Regel löschen würde."""
    rules = request.get_json(silent=True) or {}
    try:
        matched = _retention_match(rules)
        total_mb = round(sum((m.get("file_size") or 0) for m in matched) / 1048576.0, 1)
        return jsonify(ok=True, rules=rules, would_delete=len(matched),
                       reclaim_mb=total_mb, sample=matched[:50])
    except Exception as e:
        return jsonify(ok=False, error=str(e)), 500


@bp.route("/api/rec/retention/apply", methods=["POST"])
def api_rec_retention_apply():
    """Wendet eine Retention-Regel an. Erfordert confirm=true. Löscht Dateien
       von der Platte + DB-Einträge. Mit Trockenlauf-Schutz."""
    data = request.get_json(silent=True) or {}
    if not data.get("confirm"):
        return jsonify(ok=False, error="confirm=true erforderlich (Sicherheitsabfrage)"), 400
    rules = data.get("rules") or {}
    try:
        matched = _retention_match(rules)
        deleted, freed = 0, 0
        with db_conn() as conn:
            for m in matched:
                fp = m.get("filepath")
                try:
                    if fp and os.path.exists(fp):
                        freed += os.path.getsize(fp)
                        os.remove(fp)
                except OSError:
                    pass
                conn.execute("DELETE FROM recordings WHERE id=?", (m["id"],))
                deleted += 1
            conn.commit()
        try:
            log_event("retention_apply", "warn",
                      f"Retention löschte {deleted} Aufnahmen ({round(freed/1048576.0)} MB)")
        except Exception:
            pass
        return jsonify(ok=True, deleted=deleted, freed_mb=round(freed / 1048576.0, 1))
    except Exception as e:
        return jsonify(ok=False, error=str(e)), 500


@bp.route("/api/rec/compress-candidates")
def api_rec_compress_candidates():
    """Findet große Aufnahmen mit hoher Bitrate, die sich gut komprimieren
       ließen (geschätzte Ersparnis bei Re-Encode auf ~2 Mbps)."""
    try:
        with db_conn() as conn:
            rows = conn.execute(
                "SELECT id, username, file_size, duration_secs FROM recordings "
                "WHERE file_size > ? AND duration_secs > 0 ORDER BY file_size DESC LIMIT 50",
                (200 * 1048576,)).fetchall()
        out = []
        for r in rows:
            size_mb = (r["file_size"] or 0) / 1048576.0
            dur = r["duration_secs"] or 1
            mbps = (size_mb * 8) / dur
            if mbps <= 2.2:
                continue
            est_mb = (2.0 * dur) / 8.0 + 0.128 * dur / 8.0
            out.append({"id": r["id"], "username": r["username"],
                        "current_mb": round(size_mb, 1), "current_mbps": round(mbps, 2),
                        "est_mb_after": round(est_mb, 1),
                        "est_savings_mb": round(size_mb - est_mb, 1)})
        total_save = round(sum(o["est_savings_mb"] for o in out), 1)
        return jsonify(ok=True, count=len(out), est_total_savings_mb=total_save, candidates=out)
    except Exception as e:
        return jsonify(ok=False, error=str(e)), 500


@bp.route("/api/rec/orphans")
def api_rec_orphans():
    """Listet verwaiste/temporäre Dateien (Split-Reste etc.)."""
    try:
        o = _find_orphans()
        return jsonify(ok=True, count=len(o),
                       total_mb=round(sum(x["mb"] for x in o), 1), orphans=o)
    except Exception as e:
        return jsonify(ok=False, error=str(e)), 500


@bp.route("/api/rec/orphans/clean", methods=["POST"])
def api_rec_orphans_clean():
    """Löscht verwaiste Dateien. confirm=true erforderlich."""
    data = request.get_json(silent=True) or {}
    if not data.get("confirm"):
        return jsonify(ok=False, error="confirm=true erforderlich"), 400
    try:
        o = _find_orphans()
        freed, deleted = 0, 0
        for x in o:
            try:
                freed += os.path.getsize(x["path"])
                os.remove(x["path"])
                deleted += 1
            except OSError:
                pass
        return jsonify(ok=True, deleted=deleted, freed_mb=round(freed / 1048576.0, 1))
    except Exception as e:
        return jsonify(ok=False, error=str(e)), 500
