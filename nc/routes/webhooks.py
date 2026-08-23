"""nc.routes.webhooks — die Routen unter /api/webhooks als Flask-Blueprint.

Welle 3 der Zerlegung (siehe docs/MODULARISIERUNG.md), erzeugt mit
tools/bp_extract.py. Pfade stehen woertlich in den Dekoratoren (kein
url_prefix); app-weite Hooks bleiben auf der App; was der Monolith weiterhin
stellen muss, kommt ueber nc.ctx statt ueber einen Import aus bot.py.
"""

from datetime import datetime, timezone
from flask import Blueprint, jsonify, request
from nc.dbwrap import db_conn

from nc import ctx as _ctx

bp = Blueprint("webhooks", __name__)


def _c():
    """Laufzeitkontext. Aufruf statt Modul-Konstante — der Kontext wird erst
       beim Bot-Start gefuellt."""
    return _ctx.get()


class _LazyLog:
    def __getattr__(self, name):
        return getattr(_c().log, name)


log = _LazyLog()


@bp.route("/api/webhooks", methods=["GET", "POST"])
def api_webhooks():
    """GET: alle Webhooks. POST: neuen Webhook anlegen
       {url, events?: 'kindA,kindB' | '*', enabled?}."""
    if request.method == "POST":
        payload = request.get_json(silent=True) or {}
        url = (payload.get("url") or "").strip()
        events = (payload.get("events") or "*").strip()[:255]
        enabled = 0 if payload.get("enabled") is False else 1
        if not (url.startswith("http://") or url.startswith("https://")):
            return jsonify(ok=False, error="url muss mit http:// oder https:// beginnen."), 400
        if len(url) > 2000:
            return jsonify(ok=False, error="url zu lang."), 400
        try:
            with db_conn() as conn:
                cur = conn.execute(
                    "INSERT INTO webhooks (url, events, enabled, created_at) "
                    "VALUES (?,?,?,?)",
                    (url, events, enabled, datetime.now(timezone.utc).isoformat()))
                conn.commit()
                new_id = cur.lastrowid
            return jsonify(ok=True, id=new_id, url=url, events=events,
                           enabled=bool(enabled))
        except Exception as e:
            return jsonify(ok=False, error=str(e)), 500
    # GET
    try:
        with db_conn() as conn:
            rows = conn.execute(
                "SELECT id, url, events, enabled, created_at, last_status, "
                "last_fired_at, fail_count FROM webhooks ORDER BY id DESC").fetchall()
        return jsonify(ok=True, webhooks=[
            {"id": r["id"], "url": r["url"], "events": r["events"],
             "enabled": bool(r["enabled"]), "last_status": r["last_status"],
             "last_fired_at": (r["last_fired_at"] or "")[:19] if r["last_fired_at"] else None,
             "fail_count": int(r["fail_count"] or 0)} for r in rows])
    except Exception as e:
        return jsonify(ok=False, error=str(e)), 500


@bp.route("/api/webhooks/<int:wid>", methods=["DELETE"])
def api_webhook_delete(wid):
    """Webhook löschen."""
    try:
        with db_conn() as conn:
            row = conn.execute("SELECT 1 FROM webhooks WHERE id=?", (wid,)).fetchone()
            if not row:
                return jsonify(ok=False, error="Webhook nicht gefunden."), 404
            conn.execute("DELETE FROM webhooks WHERE id=?", (wid,))
            conn.commit()
        return jsonify(ok=True, deleted=wid)
    except Exception as e:
        return jsonify(ok=False, error=str(e)), 500


@bp.route("/api/webhooks/<int:wid>/toggle", methods=["POST"])
def api_webhook_toggle(wid):
    """Webhook aktivieren/deaktivieren (toggle)."""
    try:
        with db_conn() as conn:
            row = conn.execute("SELECT enabled FROM webhooks WHERE id=?", (wid,)).fetchone()
            if not row:
                return jsonify(ok=False, error="Webhook nicht gefunden."), 404
            new_val = 0 if (row["enabled"] or 0) else 1
            conn.execute("UPDATE webhooks SET enabled=? WHERE id=?", (new_val, wid))
            conn.commit()
        return jsonify(ok=True, id=wid, enabled=bool(new_val))
    except Exception as e:
        return jsonify(ok=False, error=str(e)), 500


@bp.route("/api/webhooks/<int:wid>/test", methods=["POST"])
def api_webhook_test(wid):
    """Feuert einen Test-Payload an diesen Webhook (asynchron im Thread).
       Das tatsächliche Ergebnis erscheint danach in last_status (GET /api/webhooks)."""
    try:
        with db_conn() as conn:
            row = conn.execute("SELECT id, url FROM webhooks WHERE id=?", (wid,)).fetchone()
        if not row:
            return jsonify(ok=False, error="Webhook nicht gefunden."), 404
        body = {"event": "webhook.test", "severity": "info",
                "summary": "Test-Webhook vom TikTok-Bot Dashboard",
                "payload": {"test": True}, "ts": datetime.now(timezone.utc).isoformat(),
                "source": "tiktok-bot"}
        _c().post_json_threaded(row["url"], body, wid)
        return jsonify(ok=True, id=wid, dispatched=True,
                       note="Test gesendet — Ergebnis in 'last_status' nach kurzer Zeit.")
    except Exception as e:
        return jsonify(ok=False, error=str(e)), 500
