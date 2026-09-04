"""nc.routes.systemlage — /api/system und die beiden Diagnose-Routen daneben.

v4.1-W32, erste Teillieferung von Vorschlag 2 (der harte Rest des Monolithen).

Warum diese Gruppe zuletzt drankommt: die acht System-Routen greifen zusammen
auf 112 verschiedene Namen aus bot.py zu — mehr als jede andere Gruppe, die
bisher gewandert ist. Der Weg dahin ist derselbe wie in W117: erst die Daten-
und Zustandsschicht aufloesen, dann kosten die Routen nichts. Diese Welle
loest die Sondenschicht auf (nc/systemprobe.py, nc/cookies.load_dict,
nc/logsafe.url_ohne_zugang) und nimmt die drei Routen mit, die danach ohne
einen einzigen neuen ctx-Slot auskommen.

Die uebrigen fuenf — preflight, resilience, check_timing, config_snapshot und
selftest — haengen noch am Discord-Client, am Restream-Manager und am
Watchdog-Zustand. Sie folgen, wenn deren Zustand aufgeloest ist, nicht vorher.
"""
import os

from flask import Blueprint, jsonify, request

from nc import ctx as _ctx
from nc import fehlertext as _nc_fehlertext
from nc import logsafe as _nc_logsafe
from nc import systemprobe as _nc_probe
from nc.confdrift import config_drift as _cfg_drift
from nc.cookies import load_dict as _load_cookies_dict
from nc.dbwrap import db_conn

bp = Blueprint("systemlage", __name__)


def _c():
    """Laufzeitkontext. Aufruf statt Modul-Konstante — der Kontext wird erst
       beim Bot-Start gefuellt."""
    return _ctx.get()


class _LazyLog:
    def __getattr__(self, name):
        return getattr(_c().log, name)


log = _LazyLog()


def _fehler_text(e, wo):
    """v4.1-W30: kein roher Ausnahmetext nach aussen."""
    return _nc_fehlertext.nach_aussen(e, wo)


@bp.route("/api/system")
def api_system():
    """F15: Reichere Stack-Infos (Recorder, Modell-Liste, Redis-Version,
       AI-Counter) für die Dashboard-Detailzeile."""
    cookies = _load_cookies_dict()
    important = ["sessionid_ss", "sessionid", "ttwid", "tt_chain_token"]
    have = [c for c in important if c in cookies]
    ai_model = _c().cfg["AI_MODEL"]
    models = _c().check_ai_models_sync()
    redis_ver = _nc_probe.redis_version()
    return jsonify(
        recorder       = _nc_probe.active_recorder(),
        recorder_pref  = _nc_probe.recorder_pref(),
        ai_backend     = ("brain" if os.getenv("AI_PROVIDER","").strip().lower()=="brain"
                          else "freeai"),
        ai_model       = ai_model,
        ai_models      = models if models is not None else [],
        ai_alive       = models is not None,
        ai_has_model   = bool(models) and (
            ai_model in models or
            any(m.startswith(ai_model + ":") for m in models)
        ),
        redis_url      = _nc_logsafe.url_ohne_zugang(_nc_probe.redis_url()),   # v4.0-W118 (SEC)
        redis_alive    = redis_ver is not None,
        redis_version  = redis_ver,
        cookies_total  = len(cookies),
        cookies_critical_have = len(have),
        cookies_critical_need = len(important),
        ai_calls_total = _nc_probe.ai_calls_total(),
    )


@bp.route("/api/system/preflight_history")
def api_system_preflight_history():
    try:
        with db_conn() as conn:
            rows = conn.execute("SELECT overall, fails, warns, created_at FROM preflight_history "
                                "ORDER BY id DESC LIMIT 40").fetchall()
        items = [{"overall": r["overall"], "fails": r["fails"], "warns": r["warns"],
                  "at": (r["created_at"] or "")[5:16].replace("T", " ")} for r in rows]
        return jsonify(ok=True, items=list(reversed(items)))
    except Exception as e:
        return jsonify(ok=False, error=_fehler_text(e, "api_system_preflight_history")), 500


@bp.route("/api/system/config_drift")
def api_config_drift():
    """V37-DRIFT: Welche .env-Werte weichen vom Code-Default ab?

    ?all=1 zeigt auch die harmlosen. Ohne Parameter nur die Watchlist —
    Einstellungen, bei denen eine Abweichung Verhalten oder Last spuerbar
    aendert.

    v4.1-W32: der Quelltext, der durchsucht wird, kommt aus cfg["BOT_DATEI"].
    Im Monolithen stand hier __file__ — in einem Blueprint zeigt das auf
    DIESE Datei, und die Antwort waere still eine leere Drift-Liste gewesen.
    Genau die Sorte stiller Fehlanzeige, vor der CLAUDE.md warnt.
    """
    try:
        rep = _cfg_drift(_c().cfg["BOT_DATEI"],
                         only_watchlist=(request.args.get("all") != "1"))
        rep["ok"] = True
        return jsonify(rep)
    except Exception as e:
        log.warning("api_config_drift: %s", e)
        return jsonify(ok=False, error=_fehler_text(e, "api_config_drift")), 500
