"""nc.routes.scheduler — die Routen unter /api/scheduler als Flask-Blueprint.

Welle 3 der Zerlegung (siehe docs/MODULARISIERUNG.md), erzeugt mit
tools/bp_extract.py. Pfade stehen woertlich in den Dekoratoren (kein
url_prefix); app-weite Hooks bleiben auf der App; was der Monolith weiterhin
stellen muss, kommt ueber nc.ctx statt ueber einen Import aus bot.py.
"""

from datetime import datetime, timezone
import re
from flask import Blueprint, jsonify, request
from nc import i18n as _nc_i18n
from nc import envnum as _nc_envnum
from nc import fehlertext as _nc_fehlertext
from nc.dbwrap import db_conn

from nc import ctx as _ctx

bp = Blueprint("scheduler", __name__)


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


@bp.route("/api/scheduler/list")
def api_scheduler_list():
    try:
        with db_conn() as conn:
            rows = conn.execute("SELECT id, kind, at_hhmm, payload, enabled, last_run_date "
                                "FROM scheduled_tasks ORDER BY at_hhmm").fetchall()
        items = [{"id": r["id"], "kind": r["kind"], "at": r["at_hhmm"], "payload": r["payload"] or "",
                  "enabled": bool(r["enabled"]), "last": r["last_run_date"] or "—"} for r in rows]
        return jsonify(ok=True, items=items)
    except Exception as e:
        return jsonify(ok=False, error=_fehler_text(e, "api_scheduler_list")), 500


@bp.route("/api/scheduler/add", methods=["POST"])
def api_scheduler_add():
    d = request.get_json(silent=True) or {}
    kind = (d.get("kind") or "").strip()
    at = (d.get("at") or "").strip()
    payload = (d.get("payload") or "").strip()[:1000]
    if kind not in ("announce", "push"):
        return jsonify(ok=False, error=_t("kind muss 'announce' oder 'push' sein")), 400
    if not re.match(r'^([01]\d|2[0-3]):[0-5]\d$', at):
        return jsonify(ok=False, error=_t("Zeit im Format HH:MM (24h)")), 400
    if not payload:
        return jsonify(ok=False, error=_t("leerer Text")), 400
    try:
        with db_conn() as conn:
            conn.execute("INSERT INTO scheduled_tasks (kind, at_hhmm, payload, enabled, created_at) "
                         "VALUES (?,?,?,1,?)", (kind, at, payload, datetime.now(timezone.utc).isoformat()))
        return jsonify(ok=True)
    except Exception as e:
        return jsonify(ok=False, error=_fehler_text(e, "api_scheduler_add")), 500


@bp.route("/api/scheduler/delete", methods=["POST"])
def api_scheduler_delete():
    d = request.get_json(silent=True) or {}
    # v4.0-W34-FIX: id sauber validieren — vorher crashte int(None) bei fehlender
    # id in einen 500 mit Python-Interna; jetzt klarer 400 (wie die übrigen Routen).
    tid = _nc_envnum.clamp_int(d.get("id"), None)
    if tid is None:
        return jsonify(ok=False, error=_t("id (Zahl) fehlt oder ungültig")), 400
    try:
        with db_conn() as conn:
            conn.execute("DELETE FROM scheduled_tasks WHERE id=?", (tid,))
        return jsonify(ok=True)
    except Exception as e:
        return jsonify(ok=False, error=_fehler_text(e, "api_scheduler_delete")), 500


@bp.route("/api/scheduler/toggle", methods=["POST"])
def api_scheduler_toggle():
    d = request.get_json(silent=True) or {}
    # v4.0-W34-FIX: id sauber validieren (vorher 500 bei fehlender id).
    tid = _nc_envnum.clamp_int(d.get("id"), None)
    if tid is None:
        return jsonify(ok=False, error=_t("id (Zahl) fehlt oder ungültig")), 400
    try:
        with db_conn() as conn:
            conn.execute("UPDATE scheduled_tasks SET enabled=? WHERE id=?",
                         (1 if d.get("enabled") else 0, tid))
        return jsonify(ok=True)
    except Exception as e:
        return jsonify(ok=False, error=_fehler_text(e, "api_scheduler_toggle")), 500
