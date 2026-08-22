"""nc.notes — Notizen, Lesezeichen, Annotationen.

Extrahiert aus bot_v37.py. Reine DB-Schreibpfade ohne Bot-Globals."""

import logging
from datetime import datetime, timezone

from typing import Optional

from nc.dbwrap import db_conn

log = logging.getLogger("TikTokBot")


def set_recording_note(recording_id: int, note: str) -> bool:
    note = (note or "").strip()[:5000]
    now = datetime.now(timezone.utc).isoformat()
    try:
        with db_conn() as conn:
            # Existiert recording?
            exists = conn.execute(
                "SELECT 1 FROM recordings WHERE id=?",
                (recording_id,)).fetchone()
            if not exists: return False
            if not note:
                conn.execute(
                    "DELETE FROM recording_notes WHERE recording_id=?",
                    (recording_id,))
            else:
                conn.execute(
                    "DELETE FROM recording_notes WHERE recording_id=?",
                    (recording_id,))
                conn.execute(
                    "INSERT INTO recording_notes "
                    "(recording_id, note, created_at, updated_at) "
                    "VALUES (?,?,?,?)",
                    (recording_id, note, now, now))
            conn.commit()
            return True
    except Exception as e:
        log.warning(f"set_recording_note: {e}")
        return False


def toggle_bookmark(recording_id: int) -> dict:
    """Toggle: wenn bookmark existiert → entfernen, sonst → erstellen.
       Returns {bookmarked: bool}."""
    try:
        with db_conn() as conn:
            existing = conn.execute(
                "SELECT 1 FROM bookmarks WHERE recording_id=?",
                (recording_id,)).fetchone()
            if existing:
                conn.execute("DELETE FROM bookmarks WHERE recording_id=?",
                             (recording_id,))
                conn.commit()
                return {"bookmarked": False}
            # Existiert recording?
            rec = conn.execute(
                "SELECT 1 FROM recordings WHERE id=?",
                (recording_id,)).fetchone()
            if not rec:
                return {"bookmarked": False, "error": "recording not found"}
            conn.execute(
                "INSERT INTO bookmarks (recording_id, created_at) VALUES (?,?)",
                (recording_id, datetime.now(timezone.utc).isoformat()))
            conn.commit()
            return {"bookmarked": True}
    except Exception as e:
        log.warning(f"toggle_bookmark: {e}")
        return {"bookmarked": False, "error": str(e)}


def add_annotation(recording_id: int, timestamp_secs: int,
                    label: str) -> Optional[int]:
    timestamp_secs = max(0, int(timestamp_secs))
    label = (label or "").strip()[:200]
    if not label: return None
    try:
        with db_conn() as conn:
            # Existiert recording?
            exists = conn.execute(
                "SELECT 1 FROM recordings WHERE id=?",
                (recording_id,)).fetchone()
            if not exists: return None
            cur = conn.execute(
                "INSERT INTO recording_annotations "
                "(recording_id, timestamp_secs, label, created_at) "
                "VALUES (?,?,?,?)",
                (recording_id, timestamp_secs, label,
                 datetime.now(timezone.utc).isoformat()))
            conn.commit()
            return cur.lastrowid
    except Exception as e:
        log.warning(f"add_annotation: {e}")
        return None


def delete_annotation(annotation_id: int) -> bool:
    try:
        with db_conn() as conn:
            cur = conn.execute(
                "DELETE FROM recording_annotations WHERE id=?",
                (annotation_id,))
            conn.commit()
            return cur.rowcount > 0
    except Exception:
        return False


def _conv_list(limit=50, include_archived=False):
    """Liste aller Conversations, neueste zuerst."""
    with db_conn() as conn:
        if include_archived:
            rows = conn.execute(
                "SELECT id, title, created_at, updated_at, archived, message_count "
                "FROM ai_conversations ORDER BY updated_at DESC LIMIT ?",
                (limit,)).fetchall()
        else:
            rows = conn.execute(
                "SELECT id, title, created_at, updated_at, archived, message_count "
                "FROM ai_conversations WHERE COALESCE(archived, 0) = 0 "
                "ORDER BY updated_at DESC LIMIT ?",
                (limit,)).fetchall()
    return [{
        "id": r["id"],
        "title": r["title"] or f"Konversation #{r['id']}",
        "created_at": r["created_at"],
        "updated_at": r["updated_at"],
        "message_count": r["message_count"] or 0,
    } for r in rows]


def set_tracking_notes(tracking_id: int, notes: Optional[str]) -> bool:
    """F60: Speichert Operator-Notizen für ein Tracking. Returns True wenn
       Row existiert (analog zu set_tracking_paused, gleicher B33-Fix).
       notes=None oder leerer String löscht die Notiz."""
    # F60: Cleanup + Cap
    clean = (notes or "").strip()
    if len(clean) > 200:
        clean = clean[:200]
    if not clean:
        clean = None
    with db_conn() as conn:
        exists = conn.execute(
            "SELECT 1 FROM trackings WHERE id=? LIMIT 1",
            (tracking_id,)).fetchone()
        if not exists:
            return False
        conn.execute("UPDATE trackings SET notes=? WHERE id=?",
                     (clean, tracking_id))
        conn.commit()
        return True
