"""nc.routes.collections — die Routen unter /api/collections als Flask-Blueprint.

Welle 3 der Zerlegung (siehe docs/MODULARISIERUNG.md), erzeugt mit
tools/bp_extract.py. Pfade stehen woertlich in den Dekoratoren (kein
url_prefix); app-weite Hooks bleiben auf der App; was der Monolith weiterhin
stellen muss, kommt ueber nc.ctx statt ueber einen Import aus bot.py.
"""

from datetime import datetime, timezone
from flask import Blueprint, jsonify, request
from nc.dbwrap import db_conn

from nc import ctx as _ctx

bp = Blueprint("collections", __name__)


def _c():
    """Laufzeitkontext. Aufruf statt Modul-Konstante — der Kontext wird erst
       beim Bot-Start gefuellt."""
    return _ctx.get()


class _LazyLog:
    def __getattr__(self, name):
        return getattr(_c().log, name)


log = _LazyLog()


@bp.route("/api/collections", methods=["GET", "POST"])
def api_collections():
    """GET: alle Collections + Mitglieder-Anzahl. POST: neue Collection anlegen."""
    if request.method == "POST":
        payload = request.get_json(silent=True) or {}
        name = (payload.get("name") or "").strip()[:64]
        color = (payload.get("color") or "").strip()[:16] or None
        if not name:
            return jsonify(ok=False, error="name erforderlich."), 400
        try:
            with db_conn() as conn:
                cur = conn.execute(
                    "INSERT INTO tracking_collections (name, color, created_at) "
                    "VALUES (?,?,?)",
                    (name, color, datetime.now(timezone.utc).isoformat()))
                conn.commit()
                new_id = cur.lastrowid
            return jsonify(ok=True, id=new_id, name=name, color=color)
        except Exception as e:
            return jsonify(ok=False, error=str(e)), 500
    # GET
    try:
        with db_conn() as conn:
            rows = conn.execute(
                "SELECT c.id, c.name, c.color, c.created_at, "
                "(SELECT COUNT(*) FROM trackings t WHERE t.collection_id=c.id) AS members "
                "FROM tracking_collections c ORDER BY c.name").fetchall()
        return jsonify(ok=True, collections=[
            {"id": r["id"], "name": r["name"], "color": r["color"],
             "members": int(r["members"] or 0),
             "created_at": (r["created_at"] or "")[:19]} for r in rows])
    except Exception as e:
        return jsonify(ok=False, error=str(e)), 500


@bp.route("/api/collections/<int:cid>", methods=["POST", "DELETE"])
def api_collection_modify(cid):
    """POST: umbenennen/Farbe ändern. DELETE: Collection löschen (Mitglieder
       werden nur entkoppelt, nicht gelöscht)."""
    try:
        with db_conn() as conn:
            row = conn.execute("SELECT 1 FROM tracking_collections WHERE id=?",
                              (cid,)).fetchone()
            if not row:
                return jsonify(ok=False, error="Collection nicht gefunden."), 404
            if request.method == "DELETE":
                conn.execute("UPDATE trackings SET collection_id=NULL WHERE collection_id=?",
                             (cid,))
                conn.execute("DELETE FROM tracking_collections WHERE id=?", (cid,))
                conn.commit()
                return jsonify(ok=True, deleted=cid)
            payload = request.get_json(silent=True) or {}
            name = (payload.get("name") or "").strip()[:64]
            color = (payload.get("color") or "").strip()[:16]
            sets, params = [], []
            if name:
                sets.append("name=?"); params.append(name)
            if color:
                sets.append("color=?"); params.append(color)
            if not sets:
                return jsonify(ok=False, error="Nichts zu ändern."), 400
            params.append(cid)
            conn.execute(f"UPDATE tracking_collections SET {', '.join(sets)} WHERE id=?",
                         tuple(params))
            conn.commit()
        return jsonify(ok=True, id=cid)
    except Exception as e:
        return jsonify(ok=False, error=str(e)), 500


@bp.route("/api/collections/<int:cid>/trackings")
def api_collection_trackings(cid):
    """Alle Trackings einer Collection."""
    try:
        with db_conn() as conn:
            c = conn.execute("SELECT name FROM tracking_collections WHERE id=?",
                            (cid,)).fetchone()
            if not c:
                return jsonify(ok=False, error="Collection nicht gefunden."), 404
            rows = conn.execute(
                "SELECT id, username, last_live, recording, paused FROM trackings "
                "WHERE collection_id=? ORDER BY username", (cid,)).fetchall()
        return jsonify(ok=True, collection=c["name"], trackings=[
            {"id": r["id"], "username": r["username"],
             "live": bool(r["last_live"]), "recording": bool(r["recording"]),
             "paused": bool(r["paused"])} for r in rows])
    except Exception as e:
        return jsonify(ok=False, error=str(e)), 500
