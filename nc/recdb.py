"""nc.recdb — die Aufnahmen-Datenbankzugriffe, aus bot.py herausgelöst.

Warum gebündelt und warum GENAU diese dreizehn: sie sind der Datenzugriff der
Aufnahmen-Domäne (recordings, recording_attempts, recording_notes, bookmarks,
recording_annotations, recording_inspect_cache, manual_recordings) und wurden
ausschliesslich von den /api/recordings-Routen benutzt. Sie zuerst zu lösen ist
die Vorarbeit für den Blueprint dieser Routen: dessen Fremdbezüge fallen damit
von 23 auf neun. Siehe docs/MODULARISIERUNG.md, Welle 1 → Welle 2.

Verbatim übernommen — Verhalten bitgenau identisch zum Monolithen, inklusive
der `except Exception: return []`-Pfade. Die sind hier Absicht und kein
Versehen: das Dashboard soll bei einer klemmenden Tabelle eine leere Liste
zeigen statt einen 500er, und der Fehler steht ohnehin im DB-Log.

`db_conn` kommt direkt aus nc.dbwrap (die Module kennen sich bereits),
`compute_recording_fingerprint` aus nc.archive. Einzig `log_event` lebt im Bot
und wird per configure() injiziert — ohne Injection bleiben die beiden
Papierkorb-Funktionen still, statt mit NameError zu sterben.
"""

import os
from datetime import datetime, timezone
from typing import Optional

from nc.dbwrap import db_conn
from nc.archive import compute_recording_fingerprint
from nc import inspectcache as _nc_inspectcache

# Vom Bot injiziert. Default ist ein No-Op und keine Ausnahme: der Datenzugriff
# darf nie daran scheitern, dass das Ereignisprotokoll nicht verdrahtet ist.
_log_event = lambda *a, **k: None


def configure(*, log_event=None):
    """Vom Bot einmal beim Start gerufen."""
    global _log_event
    if log_event is not None:
        _log_event = log_event


def get_recent_recording_attempts(limit=50):
    try:
        with db_conn() as conn:
            return conn.execute(
                "SELECT id, tracking_id, username, recorder, started_at, "
                "ended_at, duration_secs, returncode, file_path, file_size, "
                "outcome, stderr_tail, error "
                "FROM recording_attempts ORDER BY id DESC LIMIT ?", (limit,)
            ).fetchall()
    except Exception:
        return []

def get_all_recordings(limit=50, include_deleted=False):
    with db_conn() as conn:
        if include_deleted:
            return conn.execute(
                "SELECT * FROM recordings ORDER BY id DESC LIMIT ?",
                (limit,)).fetchall()
        # X-Series: Soft-Delete-Filter (deleted_at IS NULL)
        return conn.execute(
            "SELECT * FROM recordings WHERE deleted_at IS NULL "
            "ORDER BY id DESC LIMIT ?",
            (limit,)).fetchall()

def get_recording_by_id(recording_id: int):
    with db_conn() as conn:
        return conn.execute("SELECT * FROM recordings WHERE id=?", (recording_id,)).fetchone()

def get_recording_note(recording_id: int) -> Optional[str]:
    try:
        with db_conn() as conn:
            row = conn.execute(
                "SELECT note FROM recording_notes WHERE recording_id=?",
                (recording_id,)).fetchone()
        return row["note"] if row else None
    except Exception:
        return None

def get_bookmarked_recordings(limit: int = 50) -> list:
    try:
        with db_conn() as conn:
            return conn.execute(
                "SELECT r.id, r.username, r.filepath, r.file_size, r.duration_secs, "
                "  r.created_at, b.created_at AS bookmarked_at "
                "FROM bookmarks b JOIN recordings r ON r.id = b.recording_id "
                "WHERE r.deleted_at IS NULL "
                "ORDER BY b.created_at DESC LIMIT ?",
                (limit,)).fetchall()
    except Exception:
        return []

def get_annotations_for_recording(recording_id: int) -> list:
    try:
        with db_conn() as conn:
            return conn.execute(
                "SELECT id, timestamp_secs, label, created_at "
                "FROM recording_annotations WHERE recording_id=? "
                "ORDER BY timestamp_secs ASC",
                (recording_id,)).fetchall()
    except Exception:
        return []

def get_or_compute_inspect_sync(recording_id: int) -> Optional[dict]:
    """Sync wrapper: Cache lookup, sonst gibt None zurück (Frontend kann
       dann via POST eine Inspection triggern). Wir bauen den Cache lazy
       beim Recording-Save oder explizitem User-Request."""
    try:
        with db_conn() as conn:
            row = conn.execute(
                "SELECT inspect_json, inspected_at FROM recording_inspect_cache "
                "WHERE recording_id=?", (recording_id,)).fetchone()
        # v4.0-W54: Parse-mit-Fallback nach nc/inspectcache.py extrahiert.
        return _nc_inspectcache.parse_row(row)
    except Exception:
        return None

def update_recording_fingerprint(recording_id: int) -> Optional[str]:
    rec = get_recording_by_id(recording_id)
    if not rec or not rec["filepath"]: return None
    fp = rec["filepath"]
    if not os.path.exists(fp): return None
    h = compute_recording_fingerprint(fp)
    if not h: return None
    try:
        with db_conn() as conn:
            conn.execute(
                "UPDATE recordings SET fingerprint=? WHERE id=?",
                (h, recording_id))
            conn.commit()
    except Exception: pass
    return h

def find_recordings_by_fingerprint(h: str) -> list:
    if not h or len(h) < 16: return []
    try:
        with db_conn() as conn:
            return conn.execute(
                "SELECT id, username, filepath, file_size, created_at "
                "FROM recordings WHERE fingerprint=? AND deleted_at IS NULL "
                "ORDER BY id ASC", (h,)).fetchall()
    except Exception:
        return []

def get_manual_recordings(limit: int = 50, only_active: bool = False) -> list:
    where = "WHERE status='running'" if only_active else ""
    try:
        with db_conn() as conn:
            return conn.execute(
                f"SELECT id, username, max_duration_secs, started_at, ended_at, "
                f"  recorder_pid, output_file, status, file_size, triggered_by "
                f"FROM manual_recordings {where} ORDER BY id DESC LIMIT ?",
                (limit,)).fetchall()
    except Exception:
        return []

def soft_delete_recording(recording_id: int) -> bool:
    try:
        with db_conn() as conn:
            cur = conn.execute(
                "UPDATE recordings SET deleted_at=? WHERE id=? AND deleted_at IS NULL",
                (datetime.now(timezone.utc).isoformat(), recording_id))
            conn.commit()
            ok = cur.rowcount > 0
        if ok:
            _log_event("recording.trashed", "info",
                      f"Recording #{recording_id} in den Papierkorb verschoben",
                      {"recording_id": recording_id})
        return ok
    except Exception:
        return False

def restore_recording(recording_id: int) -> bool:
    try:
        with db_conn() as conn:
            cur = conn.execute(
                "UPDATE recordings SET deleted_at=NULL "
                "WHERE id=? AND deleted_at IS NOT NULL",
                (recording_id,))
            conn.commit()
            ok = cur.rowcount > 0
        if ok:
            _log_event("recording.restored", "info",
                      f"Recording #{recording_id} aus Papierkorb wiederhergestellt",
                      {"recording_id": recording_id})
        return ok
    except Exception:
        return False

def get_trash_recordings(limit: int = 50) -> list:
    try:
        with db_conn() as conn:
            return conn.execute(
                "SELECT id, username, filepath, file_size, duration_secs, "
                "  created_at, deleted_at FROM recordings "
                "WHERE deleted_at IS NOT NULL ORDER BY deleted_at DESC LIMIT ?",
                (limit,)).fetchall()
    except Exception:
        return []


def get_all_checks(limit=100, offset=0):
    """v4.1-W26: aus bot.py geloest. Reiner Datenzugriff auf die
       TikTok-Pruefungen — die Route unter /api/checks war der einzige
       Aufrufer, und ein Blueprint mit eigenem SELECT ist ein Blueprint mit
       Datenschicht."""
    with db_conn() as conn:
        return conn.execute("SELECT * FROM tiktok_checks ORDER BY id DESC LIMIT ? OFFSET ?",
                            (limit, offset)).fetchall()
