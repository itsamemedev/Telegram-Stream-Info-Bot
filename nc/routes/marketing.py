"""nc.routes.marketing — die Routen unter /api/marketing als Flask-Blueprint.

Welle 3 der Zerlegung (siehe docs/MODULARISIERUNG.md), erzeugt mit
tools/bp_extract.py. Pfade stehen woertlich in den Dekoratoren (kein
url_prefix); app-weite Hooks bleiben auf der App; was der Monolith weiterhin
stellen muss, kommt ueber nc.ctx statt ueber einen Import aus bot.py.
"""

import os
from flask import Blueprint, jsonify, request
from nc import fehlertext as _nc_fehlertext
from nc import i18n as _nc_i18n
from nc import marketing as _nc_marketing
from nc.util import _loop_not_ready
from nc.cfgstore import get as _cfg_get, set_ as _cfg_set

from nc import ctx as _ctx

bp = Blueprint("marketing", __name__)

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


@bp.route("/api/marketing/status")
def api_marketing_status():
    cfg = _nc_marketing.config()
    st = _nc_marketing.state()
    return jsonify(ok=True,
                   enabled=cfg.enabled, auto=cfg.auto, targets=list(cfg.targets),
                   cadence_hours=cfg.cadence_hours, min_gap_hours=cfg.min_gap_hours,
                   quiet_start=cfg.quiet_start, quiet_end=cfg.quiet_end,
                   only_when_live=cfg.only_when_live,
                   channels=[{"name": n, "url": u} for n, u in cfg.channels.items()],
                   website=cfg.website, invite_set=bool(cfg.invite),
                   discord_ready=bool(_c().cfg["DISCORD_WEBHOOK_URL"]),
                   telegram_ready=bool(os.getenv("MARKETING_TG_CHAT_ID", "").strip() or _c().cfg["ALLOWED_USER_IDS"]),
                   has_content=_nc_marketing.has_content(cfg),
                   last_post_ts=st.last_post_ts, count=st.count,
                   next_due_ts=_nc_marketing.next_due_ts(cfg, st))


@bp.route("/api/marketing/toggle", methods=["POST"])
def api_marketing_toggle():
    payload = request.get_json(silent=True) or {}
    enabled = bool(payload.get("enabled"))
    _cfg_set("marketing.enabled", enabled)
    return jsonify(ok=True, enabled=enabled)


@bp.route("/api/marketing/config", methods=["POST"])
def api_marketing_config():
    payload = request.get_json(silent=True) or {}
    stored = _cfg_get("marketing.config", {}) or {}
    for k in ("auto", "only_when_live"):
        if k in payload:
            stored[k] = bool(payload[k])
    if "targets" in payload and isinstance(payload["targets"], list):
        stored["targets"] = [t for t in payload["targets"] if t in _nc_marketing.TARGETS]
    for k in ("cadence_hours", "min_gap_hours"):
        if k in payload:
            try:
                stored[k] = max(0.5, float(payload[k]))
            except (TypeError, ValueError):
                return jsonify(ok=False, error=f"{k} muss eine Zahl sein"), 400
    for k in ("quiet_start", "quiet_end"):
        if k in payload:
            try:
                stored[k] = int(payload[k]) % 24
            except (TypeError, ValueError):
                return jsonify(ok=False, error=f"{k} muss 0-23 sein"), 400
    _cfg_set("marketing.config", stored)
    return jsonify(ok=True, config=stored)


@bp.route("/api/marketing/preview")
def api_marketing_preview():
    """Schnelle Vorschau OHNE KI-Zeile (die wird erst beim echten Senden ergaenzt)
       und OHNE zu posten."""
    cfg = _nc_marketing.config()
    st = _nc_marketing.state()
    msg = _nc_marketing.compose(cfg, variant=st.count, flavor=None)
    return jsonify(ok=True, preview=msg, has_content=_nc_marketing.has_content(cfg))


@bp.route("/api/marketing/send-now", methods=["POST"])
def api_marketing_send_now():
    """Manueller Sofort-Post (umgeht Cadence/Ruhezeit bewusst — der Mensch entscheidet)."""
    try:
        res = _c().run_async(_nc_marketing.publish(manual=True), timeout=40)
    except Exception as e:
        if _loop_not_ready(e):
            return jsonify(ok=False, error=_t("Event-Loop startet noch — kurz erneut versuchen.")), 503
        return jsonify(ok=False, error=f"Marketing-Post: {_fehler_text(e, 'api_marketing_post')}"), 500
    return jsonify(**res)
