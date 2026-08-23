"""nc.routes.archive — die Archiv-Routen als Flask-Blueprint.

Welle 3 der Zerlegung (v4.0-W107, siehe docs/MODULARISIERUNG.md): elf Routen und
sieben Helfer, die ausschliesslich diese Routen benutzen, verbatim aus bot_v37
geloest. Ausgewaehlt wurde die Gruppe nicht nach Gefuehl, sondern nach der
Kennzahl aus tools/bp_analyse.py: 582 Zeilen fuer 16 neue Kontext-Eintraege ist
das beste Verhaeltnis unter den grossen Gruppen. /api/ai bringt zwar mehr
Zeilen, wuerde aber 24 Konfigurationswerte in den Kontext ziehen.

Wie bei nc.routes.recordings: die Pfade stehen woertlich in den Dekoratoren
(kein url_prefix), die app-weiten Hooks bleiben auf der App, und alles, was der
Monolith weiterhin stellen muss, kommt ueber nc.ctx statt ueber einen Import
aus bot_v37.

Konfiguration kommt als _c().cfg["NAME"] und nicht per eigenem Env-Lesepfad:
der Bot friert diese Werte beim Import ein, ein zweiter Lesepfad waere eine
stille Verhaltensaenderung gegenueber dem Monolithen.
"""

import os
import shutil

from flask import Blueprint, jsonify, request

from nc import ctx as _ctx
from nc import recdb
from nc import envnum as _nc_envnum
from nc.dbwrap import db_conn
from nc.archive import (get_archive_entries_paged, run_archive_file_check,
                        _scan_for_duplicates, add_archive_entry,
                        get_archive_entry, delete_archive_entry,
                        _kind_from_filename)
from nc.textmore import _safe_archive_filename
from nc.intel import library as _intel_lib
from nc import archivename as _nc_archivename
from nc.sqlutil import _archive_where_clause

bp = Blueprint("archive", __name__)


def _c():
    """Kurzform fuer den Laufzeitkontext — Aufruf statt Modul-Konstante, weil
       der Kontext erst beim Bot-Start gefuellt wird."""
    return _ctx.get()


class _LazyLog:
    """Haelt die verschobenen Rumpfe woertlich: log.info(...) funktioniert
       weiter, ohne den Logger beim Import einzufrieren."""

    def __getattr__(self, name):
        return getattr(_c().log, name)


log = _LazyLog()


def _arg_int(*a, **kw):
    return _c().arg_int(*a, **kw)


def archive_writeable() -> bool:
    """True wenn ARCHIVE_DIR konfiguriert UND existiert/anlegbar UND beschreibbar."""
    if not _c().cfg["ARCHIVE_DIR"]:
        return False
    try:
        os.makedirs(_c().cfg["ARCHIVE_DIR"], exist_ok=True)
        return os.access(_c().cfg["ARCHIVE_DIR"], os.W_OK)
    except Exception:
        return False


def _archive_open_unique(filename: str) -> tuple:
    """F32: Atomares Anlegen einer neuen Datei unter ARCHIVE_DIR. Liefert
       (file_descriptor, full_path). Bei Kollision wird _2, _3, ... vor
       die Extension gehängt — anders als _archive_unique_path() ist das
       atomisch (O_CREAT | O_EXCL): zwei parallele Uploads können nicht
       denselben Pfad wählen und einander überschreiben."""
    flags = os.O_CREAT | os.O_EXCL | os.O_WRONLY
    # v4.0-W62: Namensfolge + Retry nach nc/archivename.py (opener injiziert,
    # bewiesen). Der atomare os.open (O_CREAT|O_EXCL) bleibt hier.
    return _nc_archivename.open_unique(
        _c().cfg["ARCHIVE_DIR"], filename, lambda full: os.open(full, flags, 0o644))


def get_archive_aggregate_stats(*, kind='all', query=None, date_from=None, date_to=None):
    """F38: Aggregierte Stats ÜBER ALLE gefilterten Rows (nicht nur Seite)."""
    where_sql, params = _archive_where_clause(kind=kind, query=query, date_from=date_from, date_to=date_to)
    try:
        with db_conn() as conn:
            row = conn.execute(
                f"SELECT COUNT(*), COALESCE(SUM(COALESCE(size_bytes,0)), 0) "
                f"FROM archive {where_sql}", params).fetchone()
            return {"count": row[0] if row else 0,
                    "total_size_bytes": row[1] if row else 0}
    except Exception as e:
        log.warning(f"get_archive_aggregate_stats failed: {e}")
        return {"count": 0, "total_size_bytes": 0}


def get_archive_kind_breakdown():
    """F38: Anzahl pro Kind (video/audio/image/other). Für die Type-Filter-Tabs."""
    breakdown = {'all': 0, 'video': 0, 'audio': 0, 'image': 0, 'other': 0}
    try:
        with db_conn() as conn:
            rows = conn.execute("SELECT filename FROM archive").fetchall()
            for r in rows:
                breakdown['all'] += 1
                breakdown[_kind_from_filename(r["filename"])] = \
                    breakdown.get(_kind_from_filename(r["filename"]), 0) + 1
    except Exception as e:
        log.warning(f"get_archive_kind_breakdown failed: {e}")
    return breakdown


def get_archive_missing_ids():
    """F38: Schnell-Check — nur die IDs der fehlenden Einträge (für Indikator-
       Badges in der Liste). Geht die ganze Tabelle durch; bei 100k Files
       Sekundenbereich, aber wir cachen das im Frontend pro Refresh-Cycle."""
    missing = set()
    try:
        with db_conn() as conn:
            rows = conn.execute("SELECT id, filepath FROM archive").fetchall()
        for r in rows:
            fp = r["filepath"]
            if not fp or not os.path.exists(fp):
                missing.add(r["id"])
    except Exception as e:
        log.warning(f"get_archive_missing_ids failed: {e}")
    return missing


def bulk_delete_archive_entries(ids):
    """F38: Bulk-Delete für Multi-Select-UI. Geht über delete_archive_entry()
       — damit Path-Safety, File-Cleanup und DB-Row-Cleanup pro Eintrag laufen,
       und ein einzelnes Fehlschlagen den Batch nicht abbricht.
       F39-Bug-Hunt-Fix H2: IDs werden dedupliziert. Vorher hat der Client mit
       ids=[1,1,1] drei Mal versucht ID 1 zu löschen — erster Versuch ok, die
       zwei folgenden 'not found' → deleted=1/failed=2 obwohl logisch nichts
       fehlschlug.
    """
    if not ids:
        return {"ok": True, "deleted": 0, "failed": 0, "errors": []}
    seen = set()
    deduped = []
    for eid in ids:
        # Konvertierungsversuch früh, damit Dedup über int-Werte arbeitet
        # (sonst zählen "1" und 1 als zwei verschiedene Einträge)
        try:
            eid_int = int(eid)
        except (TypeError, ValueError):
            # Bad-ID dennoch ans Log weitergeben — wir liefern den Fehler später
            deduped.append(eid)
            continue
        if eid_int not in seen:
            seen.add(eid_int)
            deduped.append(eid_int)

    deleted = 0
    failed = 0
    errors = []
    for eid in deduped:
        if not isinstance(eid, int):
            failed += 1
            errors.append({"id": str(eid), "error": "ungültige ID"})
            continue
        ok, err = delete_archive_entry(eid)
        if ok:
            deleted += 1
        else:
            failed += 1
            errors.append({"id": eid, "error": err or "unbekannt"})
    return {"ok": failed == 0, "deleted": deleted, "failed": failed, "errors": errors}


def rename_archive_entry(eid: int, new_name: str):
    """Liefert (ok: bool, payload_or_error). Bei ok=True ist payload ein dict
       mit den neuen Feldern. Bei ok=False ist payload ein Fehler-String."""
    if not _c().cfg["ARCHIVE_DIR"]:
        return False, "ARCHIVE_DIR nicht konfiguriert"
    if not new_name or not new_name.strip():
        return False, "neuer Name ist leer"

    row = get_archive_entry(eid)
    if not row:
        return False, "Eintrag nicht gefunden"

    old_filename = row["filename"]
    old_filepath = row["filepath"]
    old_ext = os.path.splitext(old_filename)[1].lower() if old_filename else ""

    # Sanitization gleich wie beim Upload — gleiche Zeichensatz-Regeln.
    candidate = _safe_archive_filename(new_name.strip())

    # Extension-Lock: wenn der User keine Extension angegeben hat (oder eine
    # andere), erzwingen wir die alte. Verhindert dass der Browser den Download
    # als .mov anbietet, obwohl das File intern .mp4 ist.
    cand_base, cand_ext = os.path.splitext(candidate)
    if not cand_ext:
        # User hat nur den Namen-Stem angegeben → alte Extension dranhängen
        candidate = cand_base + old_ext
    elif cand_ext.lower() != old_ext:
        return False, (f"Extension darf nicht geändert werden "
                       f"(alt: {old_ext or 'keine'}, neu: {cand_ext}). "
                       f"Lass die Extension weg, dann wird '{old_ext}' beibehalten.")

    # Erneute Sanity-Prüfung nach evtl. zusammengefügter Extension
    if not candidate or candidate in (".", "..", old_ext):
        return False, "neuer Name nach Sanitization leer"

    if candidate == old_filename:
        return False, "neuer Name ist identisch mit altem Namen"

    # Pfad-Safety: alter Pfad muss innerhalb ARCHIVE_DIR liegen
    real_archive = os.path.realpath(_c().cfg["ARCHIVE_DIR"])
    if old_filepath:
        try:
            real_old = os.path.realpath(old_filepath)
            if os.path.commonpath([real_archive, real_old]) != real_archive:
                log.warning(f"rename blocked: old path outside archive: {old_filepath}")
                return False, "Pfad-Safety-Check fehlgeschlagen (alter Pfad)"
        except (ValueError, OSError) as e:
            return False, f"alter Pfad ungültig: {e}"

    # Ziel-Pfad bestimmen — bei Kollision _2/_3/... anhängen.
    # F39-Bug-Hunt-Fix: Vorher haben wir NUR os.path.exists() geprüft. Wenn
    # ein DB-Eintrag aber einen Pfad referenzierte dessen Datei gelöscht
    # war (file-check zeigt 'fehlt'), bestand der Pfad auf Disk nicht — wir
    # hätten dorthin umbenannt — der DB-UPDATE wäre dann am UNIQUE-Constraint
    # auf filepath gescheitert (Rollback hat zwar funktioniert, aber das
    # ist unnötiger File-Bounce). Jetzt prüfen wir beides.
    base, ext = os.path.splitext(candidate)
    target_filename = candidate
    target_path = os.path.join(_c().cfg["ARCHIVE_DIR"], target_filename)

    def _target_in_use(path):
        if os.path.exists(path):
            return True
        # DB-Check: filepath ist UNIQUE. Wenn ein anderer Eintrag diesen Pfad
        # belegt (auch wenn das File auf Disk fehlt), kollidieren wir beim
        # UPDATE.
        try:
            with db_conn() as conn:
                row = conn.execute(
                    "SELECT id FROM archive WHERE filepath = ? AND id != ?",
                    (path, eid)).fetchone()
                return row is not None
        except Exception as e:
            log.warning(f"rename db-collision check failed: {e}")
            # Im Zweifel kollidieren-lassen — sicherer als überschreiben.
            return True

    for n in range(2, 10000):
        # Pfad-Safety: Ziel muss in ARCHIVE_DIR sein. Defensive Wahl auch
        # wenn _safe_archive_filename '..' eigentlich rausstripped.
        try:
            real_target = os.path.realpath(target_path)
            if os.path.commonpath([real_archive, real_target]) != real_archive:
                return False, "Pfad-Safety-Check fehlgeschlagen (neuer Pfad)"
        except (ValueError, OSError) as e:
            return False, f"neuer Pfad ungültig: {e}"
        if not _target_in_use(target_path):
            break
        target_filename = f"{base}_{n}{ext}"
        target_path = os.path.join(_c().cfg["ARCHIVE_DIR"], target_filename)
    else:
        return False, "zu viele Namenskollisionen"

    # Eigentlicher Rename auf Disk — nur wenn alte Datei existiert.
    old_existed = bool(old_filepath) and os.path.exists(old_filepath)
    if old_existed:
        try:
            os.rename(old_filepath, target_path)
        except OSError as e:
            log.error(f"rename failed for #{eid}: {e}")
            return False, f"rename auf Disk fehlgeschlagen: {e}"
    else:
        log.info(f"rename #{eid}: alte Datei fehlte, nur DB-Eintrag wird aktualisiert")

    # DB-Eintrag aktualisieren
    try:
        with db_conn() as conn:
            conn.execute(
                "UPDATE archive SET filename=?, filepath=? WHERE id=?",
                (target_filename, target_path, eid))
            conn.commit()
    except _c().cfg["DB_INTEGRITY_ERRORS"] as e:
        # UNIQUE constraint auf filepath — Race mit parallelem Rename auf
        # denselben Zielnamen. File auf Disk wieder zurückbenennen, damit
        # wir keine Datei-/DB-Inkonsistenz produzieren.
        if old_existed:
            try: os.rename(target_path, old_filepath)
            except Exception: pass
        return False, f"DB-Konflikt: {e}"
    except Exception as e:
        # Selber Rollback-Versuch — DB-Update fehlgeschlagen, File aber schon
        # umbenannt. Zurückrollen.
        if old_existed:
            try: os.rename(target_path, old_filepath)
            except Exception: pass
        log.error(f"rename db update failed for #{eid}: {e}")
        return False, f"DB-Update fehlgeschlagen: {e}"

    log.info(f"archive: '#{eid}' renamed '{old_filename}' → '{target_filename}'")
    return True, {
        "id":          eid,
        "filename":    target_filename,
        "filepath":    target_path,
        "old_filename": old_filename,
        "renamed_on_disk": old_existed,
    }


@bp.route("/api/archive/duplicates")
def api_archive_duplicates():
    """Scannt nach Duplikaten. Query-Param 'root' kann anderen Pfad geben
       (default: MANUAL_ARCHIVE_DIR env-var, fallback ARCHIVE_DIR, fallback ./archive)."""
    scan_root = (request.args.get("root") or _c().cfg["_MANUAL_ARCHIVE_DIR"] or
                 os.getenv("ARCHIVE_DIR", "").strip() or "archive")
    scan_root = os.path.abspath(scan_root)
    dup_groups, stats = _scan_for_duplicates(scan_root)
    return jsonify({
        "ok": True,
        "scan_root": scan_root,
        "duplicate_groups": dup_groups,
        "stats": stats,
    })


@bp.route("/api/archive/duplicates/delete", methods=["POST"])
def api_archive_duplicates_delete():
    """Löscht eine spezifische Duplikat-Datei. Sicherheits-Check: muss unter
       dem Scan-Root liegen (kein beliebiges Filesystem-Delete via Dashboard).
       Body: {"path": "...", "scan_root": "..."}"""
    payload = request.get_json(silent=True) or {}
    target = payload.get("path", "")
    scan_root = payload.get("scan_root", "")
    if not target or not scan_root:
        return jsonify(ok=False, error="path + scan_root required"), 400
    abs_target = os.path.abspath(target)
    abs_root = os.path.abspath(scan_root)
    # SECURITY: target MUSS unter scan_root liegen
    if not abs_target.startswith(abs_root + os.sep):
        return jsonify(ok=False,
                       error="path not within scan_root (security check failed)"), 403
    if not os.path.isfile(abs_target):
        return jsonify(ok=False, error="file not found"), 404
    try:
        size = os.path.getsize(abs_target)
        os.remove(abs_target)
        log.info(f"manual-archive duplicate deleted: {abs_target} ({size}B)")
        return jsonify(ok=True, deleted=abs_target, freed_bytes=size)
    except OSError as e:
        return jsonify(ok=False, error=str(e)), 500


@bp.route("/api/archive")
def api_archive():
    """F38: Paginierte + gefilterte Archive-Liste.
       Query-Params (alle optional):
         page       (int, 1-based, default 1)
         per_page   (int, 1..200, default 25)
         sort       (date|name|filename|size, default 'date')
         dir        (asc|desc, default 'desc')
         kind       (all|video|audio|image, default 'all')
         q          (Such-String, Liste/title/notes/source_url)
         check      (1 = pro Eintrag os.path.exists() prüfen — teurer aber genau)
    """
    if not _c().cfg["ARCHIVE_DIR"]:
        return jsonify({
            "enabled": False, "configured": False,
            "archive_dir": "", "writable": False,
            "max_upload_mb": _c().cfg["ARCHIVE_MAX_UPLOAD_MB"],
            "stats": None, "entries": [],
            "page": 1, "per_page": 25,
            "total": 0, "total_filtered": 0,
            "kind_breakdown": {"all": 0, "video": 0, "audio": 0, "image": 0, "other": 0},
            "missing_count": 0,
        })

    # Query-Params parsen mit defensiven Defaults — bei Garbage-Input nicht
    # crashen, sondern auf "alles anzeigen, Seite 1" fallen.
    try:
        page = _arg_int("page", 1, 1)
    except (TypeError, ValueError): page = 1
    try:
        per_page = _arg_int("per_page", 25, 1, 200)
    except (TypeError, ValueError): per_page = 25
    sort = (request.args.get("sort") or "date").lower()
    if sort not in ("date", "name", "filename", "size"): sort = "date"
    direction = (request.args.get("dir") or "desc").lower()
    if direction not in ("asc", "desc"): direction = "desc"
    kind = (request.args.get("kind") or "all").lower()
    # F39-Bug-Hunt-Fix H1: 'other' war in der Validierung erlaubt, aber
    # _ARCHIVE_KIND_MAP enthält kein 'other' → kein Filter angewandt →
    # ?kind=other zeigte stillschweigend ALLE Einträge an. Wir akzeptieren
    # 'other' nicht mehr (Frontend hat eh keinen Tab dafür); URL-Hacker
    # bekommen ein sauberes Fallback auf 'all'.
    if kind not in ("all", "video", "audio", "image"): kind = "all"
    query = (request.args.get("q") or "").strip() or None
    date_from = (request.args.get("from") or "").strip() or None   # v37: Datums-Range
    date_to = (request.args.get("to") or "").strip() or None
    check_files = request.args.get("check") in ("1", "true", "yes")

    writable = archive_writeable()
    rows, total_filtered, total_all = get_archive_entries_paged(
        page=page, per_page=per_page, sort=sort, direction=direction,
        kind=kind, query=query, date_from=date_from, date_to=date_to)
    agg = get_archive_aggregate_stats(kind=kind, query=query, date_from=date_from, date_to=date_to)
    breakdown = get_archive_kind_breakdown()

    # Datei-Existenz pro Seite — billig (max 200 stat()-Calls). Wird IMMER
    # gemacht damit das ✗-Badge in der Liste pro Eintrag korrekt ist.
    page_missing_count = 0
    entries_out = []
    for r in rows:
        fp = r["filepath"]
        exists = bool(fp) and os.path.exists(fp)
        if not exists: page_missing_count += 1
        entries_out.append({
            "id": r["id"],
            "filename": r["filename"],
            "title": r["title"] or "",
            "notes": r["notes"] or "",
            "size_bytes": r["size_bytes"] or 0,
            "mime_type": r["mime_type"],
            "source_url": r["source_url"],
            "created_at": (r["created_at"] or "")[:19].replace("T", " "),
            "kind": _kind_from_filename(r["filename"]),
            "exists": exists,
        })

    # Gesamtzahl fehlender Files — nur wenn explizit angefordert (kostet
    # einen Full-Table-Scan mit os.path.exists() pro Row, bei 50k Files
    # nicht-trivial). Default: nur die Seite checken (s.o.).
    total_missing = None
    if check_files:
        total_missing = len(get_archive_missing_ids())

    disk = None
    try:
        s = shutil.disk_usage(_c().cfg["ARCHIVE_DIR"] if os.path.isdir(_c().cfg["ARCHIVE_DIR"]) else "/")
        disk = {
            "total_gb": round(s.total / 1024**3, 2),
            "free_gb":  round(s.free  / 1024**3, 2),
            "used_gb":  round((s.total - s.free) / 1024**3, 2),
            "percent":  round((s.total - s.free) / s.total * 100, 1),
        }
    except Exception: pass

    total_pages = max(1, (total_filtered + per_page - 1) // per_page) if total_filtered else 1

    return jsonify({
        "enabled": True,
        "configured": True,
        "archive_dir": _c().cfg["ARCHIVE_DIR"],
        "writable": writable,
        "max_upload_mb": _c().cfg["ARCHIVE_MAX_UPLOAD_MB"],
        "allowed_extensions": sorted(_c().cfg["ARCHIVE_ALLOWED_EXTS"]),
        "stats": {
            "count": agg["count"],                      # nach Filter
            "total_size_bytes": agg["total_size_bytes"],# nach Filter
            "total_all": total_all,                     # ungefiltert
            "disk": disk,
        },
        "entries": entries_out,
        "page": page,
        "per_page": per_page,
        "total_filtered": total_filtered,
        "total_pages": total_pages,
        "sort": sort, "dir": direction, "kind": kind, "q": query or "",
        "kind_breakdown": breakdown,
        "page_missing_count": page_missing_count,
        "total_missing": total_missing,    # None wenn ?check=0
    })


@bp.route("/api/archive/check")
def api_archive_check():
    if not _c().cfg["ARCHIVE_DIR"]:
        return jsonify({"ok": False, "error": "ARCHIVE_DIR nicht konfiguriert"}), 400
    result = run_archive_file_check()
    return jsonify({"ok": True, **result})


@bp.route("/api/archive/bulk-delete", methods=["POST"])
def api_archive_bulk_delete():
    if not _c().cfg["ARCHIVE_DIR"]:
        return jsonify({"ok": False, "error": "ARCHIVE_DIR nicht konfiguriert"}), 400
    payload = request.get_json(silent=True) or {}
    ids = payload.get("ids") or []
    if not isinstance(ids, list):
        return jsonify({"ok": False, "error": "ids muss Liste sein"}), 400
    if len(ids) > 500:
        return jsonify({"ok": False, "error": "max 500 IDs pro Request"}), 400
    result = bulk_delete_archive_entries(ids)
    log.info(f"archive bulk-delete: requested={len(ids)} "
             f"deleted={result['deleted']} failed={result['failed']}")
    code = 200 if result["ok"] else 207   # 207 Multi-Status bei Teilerfolg
    return jsonify(result), code


@bp.route("/api/archive/<int:eid>/rename", methods=["POST"])
def api_archive_rename(eid):
    if not _c().cfg["ARCHIVE_DIR"]:
        return jsonify({"ok": False, "error": "ARCHIVE_DIR nicht konfiguriert"}), 400
    # Auch hier accept-or-fail: nur wenn ARCHIVE_DIR beschreibbar ist macht
    # Rename Sinn (sonst kann os.rename fehlschlagen — wir wollen das
    # frühzeitig melden).
    if not archive_writeable():
        return jsonify({"ok": False,
                        "error": f"ARCHIVE_DIR '{_c().cfg["ARCHIVE_DIR"]}' nicht schreibbar"}), 500

    payload = request.get_json(silent=True) or {}
    new_name = payload.get("new_name") or payload.get("filename") or ""
    if not isinstance(new_name, str):
        return jsonify({"ok": False, "error": "new_name muss String sein"}), 400
    if len(new_name) > 255:
        return jsonify({"ok": False, "error": "neuer Name zu lang (max 255 Zeichen)"}), 400

    ok, result = rename_archive_entry(eid, new_name)
    if ok:
        return jsonify({"ok": True, **result})
    # Eigene Status-Codes je nach Fehlerart — hilft beim Debuggen im Frontend
    err = str(result)
    if "nicht gefunden" in err:
        code = 404
    elif "Pfad-Safety" in err or "Extension" in err or "leer" in err or "identisch" in err:
        code = 400
    elif "Kollision" in err:
        code = 409
    else:
        code = 500
    return jsonify({"ok": False, "error": err}), code


@bp.route("/api/archive/upload", methods=["POST"])
def api_archive_upload():
    if not _c().cfg["ARCHIVE_DIR"]:
        return jsonify({"ok": False, "error": "ARCHIVE_DIR nicht konfiguriert"}), 400
    if not archive_writeable():
        return jsonify({"ok": False,
                        "error": f"ARCHIVE_DIR '{_c().cfg["ARCHIVE_DIR"]}' nicht schreibbar"}), 500

    f = request.files.get("file")
    if not f or not f.filename:
        return jsonify({"ok": False, "error": "keine Datei im Upload"}), 400

    title  = (request.form.get("title")      or "").strip()[:200]
    notes  = (request.form.get("notes")      or "").strip()[:2000]
    source = (request.form.get("source_url") or "").strip()[:500]

    fname = _safe_archive_filename(f.filename)
    ext = fname.rsplit(".", 1)[-1].lower() if "." in fname else ""
    if ext not in _c().cfg["ARCHIVE_ALLOWED_EXTS"]:
        return jsonify({"ok": False,
                        "error": f"Datei-Typ '.{ext}' nicht erlaubt. "
                                 f"Erlaubt: {', '.join(sorted(_c().cfg["ARCHIVE_ALLOWED_EXTS"]))}"}), 400

    # BUG-FIX (Disk-Check): Vorher wurde `free < ARCHIVE_MAX_UPLOAD_MB/4` geprüft
    # (= 25 GB bei 100-GB-Default). Folge: selbst eine 5-MB-Datei ließ sich nicht
    # hochladen wenn < 25 GB frei waren — komplett kaputt auf normalen Disks.
    # Jetzt: echte Upload-Größe (Content-Length) + 100 MB Puffer prüfen. Fällt
    # auf einen kleinen Mindest-Puffer zurück wenn Content-Length fehlt.
    try:
        free = shutil.disk_usage(_c().cfg["ARCHIVE_DIR"]).free
        incoming = request.content_length or 0           # Gesamt-Body inkl. Multipart-Overhead
        buffer_bytes = 100 * 1024 * 1024                  # 100 MB Sicherheitspuffer
        needed = (incoming if incoming > 0 else 1024 * 1024) + buffer_bytes
        if free < needed:
            return jsonify({"ok": False,
                            "error": f"nur {free/1024**3:.2f} GB frei, Upload braucht "
                                     f"~{needed/1024**3:.2f} GB — bitte aufräumen"}), 507
    except Exception: pass

    # F32: Atomare Filename-Allokation. Zwei parallele Uploads mit gleichem
    # ursprünglichem Namen können sich nicht mehr gegenseitig überschreiben.
    try:
        fd, target = _archive_open_unique(fname)
    except Exception as e:
        log.error(f"archive open failed: {e}")
        return jsonify({"ok": False, "error": f"file allocation failed: {e}"}), 500
    try:
        # Stream Werkzeug-FileStorage in den exclusively geöffneten fd
        with os.fdopen(fd, "wb") as out:
            f.stream.seek(0)
            while True:
                chunk = f.stream.read(1024 * 1024)   # 1 MB chunks
                if not chunk: break
                out.write(chunk)
        size = os.path.getsize(target)
    except Exception as e:
        try:
            if os.path.exists(target): os.remove(target)
        except Exception: pass
        log.error(f"archive upload save failed: {e}")
        return jsonify({"ok": False, "error": f"save failed: {e}"}), 500

    # Nach-Hoc-Limit-Check (falls multipart-Stream durchkam)
    if size > _c().cfg["ARCHIVE_MAX_UPLOAD_MB"] * 1024 * 1024:
        try: os.remove(target)
        except Exception: pass
        return jsonify({"ok": False,
                        "error": f"Datei zu groß ({size/1024**2:.0f} MB > "
                                 f"{_c().cfg["ARCHIVE_MAX_UPLOAD_MB"]} MB)"}), 413

    eid = add_archive_entry(
        filename=os.path.basename(target),
        filepath=target,
        title=title or None,
        notes=notes or None,
        size=size,
        mime=f.mimetype or None,
        source_url=source or None,
    )
    log.info(f"archive: '{os.path.basename(target)}' ({size/1024**2:.1f} MB) abgelegt → id={eid}")
    return jsonify({"ok": True, "id": eid,
                    "filename": os.path.basename(target), "size": size})


@bp.route("/api/archive/<int:eid>", methods=["DELETE"])
def api_archive_delete(eid):
    ok, err = delete_archive_entry(eid)
    if ok:
        return jsonify({"ok": True})
    code = 404 if "not found" in err else 500
    return jsonify({"ok": False, "error": err}), code


@bp.route("/api/archive/search")
def api_archive_search():
    """Bedeutungs-Suche über alle transkribierten Aufnahmen."""
    q = (request.args.get("q") or "").strip()
    if not q:
        return jsonify(ok=False, error="Parameter q fehlt", hits=[])
    be = _c().intel_semantic()
    if be is None:
        return jsonify(ok=False, error="Semantik-Backend (Brain) nicht verfügbar", hits=[])
    _c().intel_ensure_schema()
    k = _arg_int("k", 8, 1, 30)
    user = (request.args.get("user") or "").strip() or None
    try:
        with db_conn() as c:
            res = _intel_lib.search(c, be, q, k=k, username=user, paramstyle=_c().intel_ps)
        return jsonify(res)
    except Exception as e:
        return jsonify(ok=False, error=str(e)[:200], hits=[])


@bp.route("/api/archive/status")
def api_archive_status():
    _c().intel_ensure_schema()
    be = _c().intel_semantic()
    try:
        with db_conn() as c:
            cov = _intel_lib.coverage(c, be, _c().intel_ps)
        cov["ok"] = True
        cov["backend_ready"] = be is not None
        cov["indexer_enabled"] = _nc_envnum.env_int("ARCHIVE_INDEX_ENABLED", 0) == 1
        return jsonify(cov)
    except Exception as e:
        return jsonify(ok=False, error=str(e)[:200])


@bp.route("/api/archive/index/<int:rid>", methods=["POST"])
def api_archive_index_one(rid):
    """Eine bestimmte Aufnahme manuell (neu) transkribieren + indizieren."""
    rec = next((r for r in recdb.get_all_recordings(limit=1000) if r["id"] == rid), None)
    if not rec or not rec.get("filepath"):
        return jsonify(ok=False, error="Aufnahme/Datei nicht gefunden"), 404
    try:
        n = _c().run_async(
            _c().intel_index_one(rid, rec["filepath"], username=rec.get("username", "")),
            timeout=900)
        return jsonify(ok=True, recording_id=rid, segments=n)
    except Exception as e:
        return jsonify(ok=False, error=str(e)[:200]), 500
