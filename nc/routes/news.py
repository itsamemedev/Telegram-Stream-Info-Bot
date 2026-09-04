"""nc.routes.news — die Routen unter /api/news als Flask-Blueprint.

Welle 3 der Zerlegung (siehe docs/MODULARISIERUNG.md), erzeugt mit
tools/bp_extract.py. Pfade stehen woertlich in den Dekoratoren (kein
url_prefix); app-weite Hooks bleiben auf der App; was der Monolith weiterhin
stellen muss, kommt ueber nc.ctx statt ueber einen Import aus bot.py.
"""

import asyncio
from flask import Blueprint, jsonify, request
import time as _time_mod
from nc import fehlertext as _nc_fehlertext
from nc import i18n as _nc_i18n
from nc import news as _nc_news
from nc.util import _loop_not_ready
from nc.cfgstore import get as _cfg_get, set_ as _cfg_set

from nc import ctx as _ctx

bp = Blueprint("news", __name__)

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


@bp.route("/api/news/status")
def api_news_status():
    cfg = _nc_news.config()
    st = _nc_news.state()
    current = _nc_news.read_items()
    return jsonify(ok=True,
                   enabled=cfg.enabled, auto=cfg.auto, categories=list(cfg.categories),
                   cadence_hours=cfg.cadence_hours, quiet_start=cfg.quiet_start,
                   quiet_end=cfg.quiet_end, max_items=cfg.max_items,
                   output_path=_nc_news.output_path(), current_items=len(current),
                   last_gen_ts=st.last_gen_ts, count=st.count)


@bp.route("/api/news/creators")
def api_news_creators():
    """v4.0-W63: Azraels Creator-Dossier — je getracktem User Aktivitäts-
       Zusammenfassung + Azraels Take (aus dem Cache, sofort)."""
    data = _cfg_get("news.creators", {}) or {}
    items = data.get("items", []) if isinstance(data, dict) else []
    return jsonify(ok=True, items=items,
                   generated_ts=data.get("generated_ts") if isinstance(data, dict) else None,
                   days=data.get("days", 7) if isinstance(data, dict) else 7)


@bp.route("/api/news/creators/generate", methods=["POST"])
def api_news_creators_generate():
    """Neu-Bewertung anstoßen (läuft im Hintergrund; kann KI-Zeit kosten)."""
    payload = request.get_json(silent=True) or {}
    try:
        days = max(1, min(60, int(payload.get("days", 7))))
    except (TypeError, ValueError):
        days = 7
    loop = _c().get_main_loop()
    if loop and loop.is_running():
        asyncio.run_coroutine_threadsafe(_nc_news.creator_dossier_generate(days), loop)
        return jsonify(ok=True, started=True, days=days)
    return jsonify(ok=False, error=_t("Event-Loop nicht bereit")), 503


@bp.route("/api/news/toggle", methods=["POST"])
def api_news_toggle():
    payload = request.get_json(silent=True) or {}
    enabled = bool(payload.get("enabled"))
    _cfg_set("news.enabled", enabled)
    return jsonify(ok=True, enabled=enabled)


@bp.route("/api/news/config", methods=["POST"])
def api_news_config():
    payload = request.get_json(silent=True) or {}
    stored = _cfg_get("news.config", {}) or {}
    if "auto" in payload:
        stored["auto"] = bool(payload["auto"])
    if "categories" in payload and isinstance(payload["categories"], list):
        stored["categories"] = [c for c in payload["categories"] if c in _nc_news.CATEGORIES]
    if "cadence_hours" in payload:
        try:
            stored["cadence_hours"] = max(0.5, float(payload["cadence_hours"]))
        except (TypeError, ValueError):
            return jsonify(ok=False, error=_t("cadence_hours muss eine Zahl sein")), 400
    if "max_items" in payload:
        try:
            stored["max_items"] = max(1, min(100, int(payload["max_items"])))
        except (TypeError, ValueError):
            return jsonify(ok=False, error=_t("max_items muss eine Zahl sein")), 400
    for k in ("quiet_start", "quiet_end"):
        if k in payload:
            try:
                stored[k] = int(payload[k]) % 24
            except (TypeError, ValueError):
                return jsonify(ok=False, error=f"{k} muss 0-23 sein"), 400
    _cfg_set("news.config", stored)
    return jsonify(ok=True, config=stored)


@bp.route("/api/news/preview")
def api_news_preview():
    """Schnelle Vorschau OHNE KI-Formulierung (statische Fakten-Texte), ohne zu schreiben."""
    cfg = _nc_news.config()
    facts = _nc_news.collect_facts()
    items = _nc_news.build_items(facts, phrasings={}, categories=cfg.categories, now_ts=_time_mod.time())
    return jsonify(ok=True, items=items, facts=facts)


@bp.route("/api/news/items")
def api_news_items():
    return jsonify(ok=True, items=_nc_news.read_items())


@bp.route("/api/news/generate-now", methods=["POST"])
def api_news_generate_now():
    try:
        res = _c().run_async(_nc_news.generate(manual=True), timeout=60)
    except Exception as e:
        if _loop_not_ready(e):
            return jsonify(ok=False, error=_t("Event-Loop startet noch — kurz erneut versuchen.")), 503
        return jsonify(ok=False, error=f"News-Generierung: {_fehler_text(e, 'api_news_generate')}"), 500
    return jsonify(**res)
