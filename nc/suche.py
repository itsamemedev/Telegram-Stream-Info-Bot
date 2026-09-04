"""nc.suche — v4.1-W26: die bestandsweite Suche.

Aus dem Monolithen geloest: sie liest nur die Datenbank und haengt an keinem
Bot-Zustand. Die Route unter /api/search war ihr einziger Aufrufer, und ein
Blueprint mit einer eingebauten 60-Zeilen-Suche waere ein Blueprint mit
Fachlogik gewesen.
"""

import logging
import os

from nc.dbwrap import db_conn

log = logging.getLogger("TikTokBot")


def universal_search(query: str, limit: int = 30) -> dict:
    """Sucht über trackings, recordings, archive, profile_snapshots.
       Returns kategorisierte Treffer."""
    q = (query or "").strip().lower()
    if not q or len(q) < 2:
        return {"query": q, "results": {}}
    like = f"%{q}%"
    results = {"trackings": [], "recordings": [], "archive": [], "tags": []}
    try:
        with db_conn() as conn:
            # Trackings — username + notes
            rows = conn.execute(
                "SELECT id, username, group_id, COALESCE(notes, '') AS notes, "
                "  last_live, recording, COALESCE(paused, 0) AS paused "
                "FROM trackings WHERE LOWER(username) LIKE ? "
                "  OR LOWER(COALESCE(notes, '')) LIKE ? LIMIT ?",
                (like, like, limit)).fetchall()
            results["trackings"] = [{
                "id": r["id"], "username": r["username"],
                "group_id": r["group_id"], "notes": r["notes"],
                "live": bool(r["last_live"]), "recording": bool(r["recording"]),
                "paused": bool(r["paused"]),
            } for r in rows]
            # Recordings — username + file basename
            rows = conn.execute(
                "SELECT id, username, filepath, file_size, created_at "
                "FROM recordings WHERE deleted_at IS NULL "
                "  AND (LOWER(username) LIKE ? OR LOWER(filepath) LIKE ?) "
                "ORDER BY id DESC LIMIT ?",
                (like, like, limit)).fetchall()
            results["recordings"] = [{
                "id": r["id"], "username": r["username"],
                "filename": os.path.basename(r["filepath"] or ""),
                "size_mb": round((r["file_size"] or 0)/1024/1024, 1),
                "created_at": r["created_at"],
            } for r in rows]
            # Archive — filename, title, notes
            rows = conn.execute(
                "SELECT id, filename, title, COALESCE(notes, '') AS notes, "
                "  size_bytes, created_at "
                "FROM archive "
                "WHERE LOWER(filename) LIKE ? OR LOWER(COALESCE(title, '')) LIKE ? "
                "  OR LOWER(COALESCE(notes, '')) LIKE ? LIMIT ?",
                (like, like, like, limit)).fetchall()
            results["archive"] = [{
                "id": r["id"], "filename": r["filename"],
                "title": r["title"], "notes": r["notes"],
                "size_mb": round((r["size_bytes"] or 0)/1024/1024, 1),
                "created_at": r["created_at"],
            } for r in rows]
            # Tags
            rows = conn.execute(
                "SELECT tag, COUNT(*) AS c FROM tracking_tags "
                "WHERE LOWER(tag) LIKE ? GROUP BY tag LIMIT ?",
                (like, limit)).fetchall()
            results["tags"] = [{"tag": r["tag"], "count": r["c"]} for r in rows]
    except Exception as e:
        log.warning(f"universal_search: {e}")
    return {"query": q, "results": results,
            "total": sum(len(v) for v in results.values())}
