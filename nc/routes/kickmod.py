"""nc.routes.kickmod — die Routen unter /api/kickmod als Flask-Blueprint.

Welle 3 der Zerlegung (siehe docs/MODULARISIERUNG.md). Pfade stehen woertlich
in den Dekoratoren (kein url_prefix); was der Monolith weiterhin stellen muss,
kommt ueber nc.ctx statt ueber einen Import aus bot.py.

v4.1-W18: Neun Routen, null neue Kontext-Eintraege — nach zwei Aufloesungen
vorweg, in genau der Reihenfolge aus W117:

* Die Dateiarbeit (Bannwortliste, Lern-Warteschlange, LDNOOBW-Basisliste)
  liegt seit dieser Welle in nc/badwords.py. Sie waere sonst fuer sich allein
  fuenf Kontext-Eintraege gewesen.
* Der primaere Restream ist ein Register in nc/channels.py. Im Monolithen
  stand dafuer `globals()["_RESTREAM_ACTIVE"] = …`; in einem Blueprint waere
  globals() der Namensraum DIESER Datei — das SENTINEL-Panel meldete TikTok
  fuer immer als "nicht verbunden", waehrend der Listener laeuft.

Die sieben .env-Werte (KICK_CLIENT_ID, KICKMOD_AUTOSTART, …) werden hier bei
JEDEM Aufruf gelesen statt als Modul-Konstante eingefroren. Das ist nicht nur
billiger als ein Kontext-Eintrag, es ist auch die Regel aus CLAUDE.md:
`.env` wird teils erst nach den ersten Imports geladen, eine Modul-Konstante
haette dann den Default statt des eingetragenen Werts.

Aus dem Kontext kommt einzig run_async, das es ohnehin schon gab.
"""

import os

from flask import Blueprint, jsonify, request

from nc import badwords as _nc_badwords
from nc import channels as _nc_channels
from nc import discordstate as _nc_discordstate
from nc import i18n as _nc_i18n
from nc.dbwrap import db_conn
from nc.textmore import _merge_banned_words
from nc.util import _loop_not_ready

from nc import ctx as _ctx

bp = Blueprint("kickmod", __name__)

_WAHR = ("1", "true", "yes", "on", "y")


def _c():
    """Laufzeitkontext. Aufruf statt Modul-Konstante — der Kontext wird erst
       beim Bot-Start gefuellt."""
    return _ctx.get()


def _t(s):
    """v4.1-W19: an der Quelle uebersetzen. Diese Texte erreichen das DOM
       meist verkettet ("Fehler: " + error) — ein Katalogeintrag fuer den
       blossen Text traefe dort nie."""
    return _nc_i18n.t(s)


def _mod():
    """Der laufende Kick-Moderator aus dem Register (v4.1-W9)."""
    return _nc_channels.KICK_MOD["obj"]


def _flag(name, default="1"):
    return (os.getenv(name, default) or "").strip().lower() in _WAHR


def _txt(name):
    return (os.getenv(name, "") or "").strip()


@bp.route("/api/kickmod/status")
def api_kickmod_status():
    rows = []
    try:
        with db_conn() as conn:
            rows = conn.execute("SELECT ts, kind, actor, content, meta FROM kick_mod_log "
                                "ORDER BY id DESC LIMIT 50").fetchall()
    except Exception:
        pass
    mod = _mod()
    stats = getattr(mod, "stats", {}) or {}
    try:
        chatroom = int(os.getenv("KICK_CHATROOM_ID", "0") or 0)
    except (TypeError, ValueError):
        chatroom = 0
    dc = _nc_discordstate.CLIENT["obj"]
    return jsonify(ok=True, running=bool(getattr(mod, "running", False)),
                   api_configured=bool(_txt("KICK_CLIENT_ID") and _txt("KICK_CLIENT_SECRET")),
                   chat_configured=bool(chatroom),
                   autostart=_flag("KICKMOD_AUTOSTART"),
                   # F93: Multi-Channel-Sicht für das SENTINEL-Panel
                   channels={
                       "kick": {"enabled": bool(chatroom),
                                "connected": bool(stats.get("connected"))},
                       "discord": {"enabled": bool(_txt("DISCORD_BOT_TOKEN") and _flag("DISCORD_AI_MOD")),
                                   "connected": bool(dc and getattr(dc, "user", None))},
                       "tiktok": {"enabled": _flag("LIVE_REACT_CHAT"),
                                  "connected": bool(_nc_channels.restream_active().get("user"))},
                       "twitch": {"enabled": bool(_txt("TWITCH_CHANNEL")),
                                  "connected": _nc_channels.WCHAT_STATUS["twitch"]["connected"]},
                       "youtube": {"enabled": bool(_txt("YOUTUBE_CHANNEL")),
                                   "connected": _nc_channels.WCHAT_STATUS["youtube"]["connected"]}},
                   cfg=getattr(mod, "cfg", {}) or {}, stats=stats,
                   log=[{"ts": (r["ts"] or "")[:19], "kind": r["kind"], "actor": r["actor"],
                         "content": r["content"]} for r in rows])


@bp.route("/api/kickmod/config", methods=["POST"])
def api_kickmod_config():
    mod = _mod()
    if mod is None:
        return jsonify(ok=False, error=_t("Kick-Moderator läuft nicht")), 503
    d = request.get_json(silent=True) or {}
    if "auto_reply" in d:    mod.cfg["auto_reply"] = bool(d["auto_reply"])
    if "auto_moderate" in d: mod.cfg["auto_moderate"] = bool(d["auto_moderate"])
    if "sensitivity" in d:
        try: mod.cfg["sensitivity"] = max(0.0, min(1.0, float(d["sensitivity"])))
        except (TypeError, ValueError): pass
    if "engage_min" in d:
        try: mod.cfg["engage_min"] = max(0, min(120, int(d["engage_min"])))
        except (TypeError, ValueError): pass
    if "persona" in d:  mod.cfg["persona"] = (d["persona"] or "")[:200]
    if "persona_full" in d:  mod.cfg["persona_full"] = (d["persona_full"] or "")[:4000]
    if "reaction_prompt" in d: mod.cfg["reaction_prompt"] = (d["reaction_prompt"] or "")[:4000]
    if "learn_badwords" in d: mod.cfg["learn_badwords"] = bool(d["learn_badwords"])
    if "learn_autoadd" in d: mod.cfg["learn_autoadd"] = bool(d["learn_autoadd"])
    # AUSBAU: Spam-Heuristik + Eskalation + Persona-Ton
    if "spam_filter" in d: mod.cfg["spam_filter"] = bool(d["spam_filter"])
    if "escalate" in d: mod.cfg["escalate"] = bool(d["escalate"])
    if "intensity" in d:
        try: mod.cfg["intensity"] = max(0, min(2, int(d["intensity"])))
        except (TypeError, ValueError): pass
    if "flood_max" in d:
        try: mod.cfg["flood_max"] = max(2, min(50, int(d["flood_max"])))
        except (TypeError, ValueError): pass
    if "max_links" in d:
        try: mod.cfg["max_links"] = max(0, min(20, int(d["max_links"])))
        except (TypeError, ValueError): pass
    if "max_caps_ratio" in d:
        try: mod.cfg["max_caps_ratio"] = max(0.3, min(1.0, float(d["max_caps_ratio"])))
        except (TypeError, ValueError): pass
    if "auto_timeout_max_min" in d:
        try: mod.cfg["auto_timeout_max_min"] = max(1, min(1440, int(d["auto_timeout_max_min"])))
        except (TypeError, ValueError): pass
    if "greeting" in d: mod.cfg["greeting"] = (d["greeting"] or "")[:300]
    if "banned_words" in d:
        bw = d["banned_words"]
        if isinstance(bw, str):
            bw = [w.strip() for w in bw.split(",") if w.strip()]
        if isinstance(bw, list):
            mod.cfg["banned_words"] = [str(w)[:40] for w in bw][:_nc_badwords.CAP]
            _nc_badwords.save_banned(mod.cfg["banned_words"])
    return jsonify(ok=True, cfg=mod.cfg)


@bp.route("/api/kickmod/import_badwords", methods=["POST"])
def api_kickmod_import_badwords():
    """Lädt eine freie deutsche Schimpfwort-Basisliste (LDNOOBW) EINMAL und merged sie
       in banned_words (dedupliziert, gekappt, lokal gecached). Bei Netzfehler Fallback.
       Die Liste ist im Dashboard-Feld danach reviewbar/kürzbar."""
    mod = _mod()
    if mod is None:
        return jsonify(ok=False, error=_t("Kick-Moderator läuft nicht")), 503
    words, source = _nc_badwords.fetch_ldnoobw_de()
    before = list(mod.cfg.get("banned_words") or [])
    merged = _merge_banned_words(before, words)
    added = len(merged) - len(before)
    mod.cfg["banned_words"] = merged
    _nc_badwords.save_banned(merged)
    return jsonify(ok=True, source=source, added=added, total=len(merged), banned_words=merged)


@bp.route("/api/kickmod/learned")
def api_kickmod_learned():
    """Gelernte Schimpfwort-Kandidaten (Review-Queue)."""
    items = _nc_badwords.load_learned()
    return jsonify(ok=True, count=len(items), learned=items)


@bp.route("/api/kickmod/learned/promote", methods=["POST"])
def api_kickmod_learned_promote():
    """Übernimmt gelernte Kandidaten in die aktive banned_words-Liste (Auswahl via
       'words', sonst alle) und entfernt sie aus der Queue."""
    mod = _mod()
    if mod is None:
        return jsonify(ok=False, error=_t("Kick-Moderator läuft nicht")), 503
    d = request.get_json(silent=True) or {}
    words = d.get("words")
    items = _nc_badwords.load_learned()
    pick = {str(w).lower() for w in words} if isinstance(words, list) and words else None
    promote = [it for it in items if (pick is None or str(it.get("word", "")).lower() in pick)]
    if promote:
        bw = list(mod.cfg.get("banned_words") or [])
        bw += [it["word"] for it in promote if it.get("word")]
        mod.cfg["banned_words"] = _merge_banned_words(bw, [])
        _nc_badwords.save_banned(mod.cfg["banned_words"])
        rest = [it for it in items if str(it.get("word", "")).lower() not in pick] if pick else []
        _nc_badwords.save_learned(rest)
    return jsonify(ok=True, promoted=len(promote), banned_words=mod.cfg.get("banned_words") or [],
                   total=len(mod.cfg.get("banned_words") or []),
                   remaining=len(_nc_badwords.load_learned()))


@bp.route("/api/kickmod/learned/clear", methods=["POST"])
def api_kickmod_learned_clear():
    _nc_badwords.save_learned([])
    return jsonify(ok=True)


@bp.route("/api/kickmod/start", methods=["POST"])
def api_kickmod_start():
    mod = _mod()
    if mod is None:
        return jsonify(ok=False, error=_t("Kick-Moderator läuft nicht")), 503
    try:
        res = _c().run_async(mod.start(), timeout=15)
        return jsonify(res), (200 if res.get("ok") else 502)
    except RuntimeError:
        return jsonify(ok=False, error=_t("Event-Loop nicht bereit")), 503
    except Exception as e:
        return jsonify(ok=False, error=str(e)), 500


@bp.route("/api/kickmod/stop", methods=["POST"])
def api_kickmod_stop():
    mod = _mod()
    if mod is None:
        return jsonify(ok=False, error=_t("Kick-Moderator läuft nicht")), 503
    try:
        res = _c().run_async(mod.stop(), timeout=15)
        return jsonify(res)
    except RuntimeError as e:
        if _loop_not_ready(e):
            return jsonify(ok=False, error=_t("Bot-Loop startet noch"), transient=True), 503
        return jsonify(ok=False, error=str(e)), 500
    except Exception as e:
        return jsonify(ok=False, error=str(e)), 500


@bp.route("/api/kickmod/say", methods=["POST"])
def api_kickmod_say():
    """Manuelle Nachricht über den Bot senden (Operator-Test)."""
    mod = _mod()
    if mod is None:
        return jsonify(ok=False, error=_t("Kick-Moderator läuft nicht")), 503
    d = request.get_json(silent=True) or {}
    msg = (d.get("message") or "").strip()
    if not msg:
        return jsonify(ok=False, error=_t("leere Nachricht")), 400
    try:
        ok, err = _c().run_async(mod.send_message(_nc_i18n.t(msg)), timeout=20)
        return jsonify(ok=ok, error=err), (200 if ok else 502)
    except RuntimeError as e:
        if _loop_not_ready(e):
            return jsonify(ok=False, error=_t("Bot-Loop startet noch"), transient=True), 503
        return jsonify(ok=False, error=str(e)), 500
    except Exception as e:
        return jsonify(ok=False, error=str(e)), 500
