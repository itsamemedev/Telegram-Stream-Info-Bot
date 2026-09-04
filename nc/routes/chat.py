"""nc.routes.chat — die Routen unter /api/chat als Flask-Blueprint.

Welle 3 der Zerlegung (siehe docs/MODULARISIERUNG.md), erzeugt mit
tools/bp_extract.py. Pfade stehen woertlich in den Dekoratoren (kein
url_prefix); app-weite Hooks bleiben auf der App; was der Monolith weiterhin
stellen muss, kommt ueber nc.ctx statt ueber einen Import aus bot.py.

v4.1-W15: Alle drei Sendewege sind GETEILTER Zustand aus nc/channels.py —
KICK_MOD (der laufende Moderator, seit W9 im Register), TWITCH_SEND und
YT_SEND (die Sende-Hooks, die die Listener-Loops setzen). Der direkte Import
trifft dieselben Objekte: eine Kopie hiesse, dass diese Routen "nicht
verbunden" melden, waehrend der Bot sendet. Aus dem Kontext kommt nur
run_async, das es ohnehin schon gab. Neue Kontext-Eintraege: null.
"""

import os

from flask import Blueprint, jsonify, request

from nc import channels as _nc_channels
from nc import fehlertext as _nc_fehlertext
from nc import i18n as _nc_i18n
from nc.channels import TWITCH_SEND as _TWITCH_SEND
from nc.channels import YT_SEND as _YT_SEND

from nc import ctx as _ctx

bp = Blueprint("chat", __name__)


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


@bp.route("/api/chat/send_status")
def api_chat_send_status():
    """v4.0-W41: beantwortet direkt „auf welchen Plattformen kann der Bot GERADE
       in den Chat schreiben?". Genau die Frage hinter „Nachricht nur auf Kick"."""
    kick_ready = _nc_channels.KICK_MOD["obj"] is not None
    tw_ready = bool(_TWITCH_SEND.get("fn"))
    yt_ready = bool(_YT_SEND.get("fn"))
    tw_chan = (os.getenv("TWITCH_CHANNEL", "") or "").strip()
    yt_chan = (os.getenv("YOUTUBE_CHANNEL", "") or "").strip()

    def _hint(ready, chan, plat):
        if ready:
            return ""
        if not chan:
            return f"{plat}_CHANNEL ist in der .env leer — dort setzen (dann startet der Listener)"
        return "Kanal gesetzt, aber Chat nicht verbunden — OAuth/Token prüfen"
    plats = {
        "kick": {"can_send": kick_ready,
                 "hint": "" if kick_ready else "Kick-Mod/App-Token nicht bereit"},
        "twitch": {"can_send": tw_ready, "channel_set": bool(tw_chan),
                   "hint": _hint(tw_ready, tw_chan, "TWITCH")},
        "youtube": {"can_send": yt_ready, "channel_set": bool(yt_chan),
                    "hint": _hint(yt_ready, yt_chan, "YOUTUBE")},
    }
    ready = [p for p, v in plats.items() if v["can_send"]]
    return jsonify(ok=True, ready=ready, count=len(ready), platforms=plats)


@bp.route("/api/chat/send", methods=["POST"])
def api_chat_send():
    """V37-W-CTRL: Nachricht in den EIGENEN Kanal-Chat (kick|twitch) —
    der Mobile-Operator muss dafür nicht mehr die Plattform-App öffnen.
    YouTube ist lesend (Senden bräuchte OAuth) → 501."""
    d = request.get_json(silent=True) or {}
    platform = (d.get("platform") or "kick").strip().lower()
    text = (d.get("text") or "").strip()[:450]
    if not text:
        return jsonify(ok=False, error=_t("text fehlt")), 400
    if platform == "kick":
        if not _nc_channels.KICK_MOD["obj"]:
            return jsonify(ok=False, error=_t("Kick-Mod nicht verbunden")), 503
        ok, err = _c().run_async(_nc_channels.KICK_MOD["obj"].send_message(_nc_i18n.t(text)), timeout=15)
        return jsonify(ok=bool(ok), error=err)
    if platform == "twitch":
        fn = _TWITCH_SEND.get("fn")
        if not fn:
            return jsonify(ok=False, error=_t("Twitch nicht verbunden oder "
                                              "kein TWITCH_CHAT_TOKEN (nur-lesend)")), 503
        try:
            _c().run_async(fn(text), timeout=10)
            return jsonify(ok=True)
        except Exception as e:
            return jsonify(ok=False, error=_fehler_text(e, "api_chat_send")), 500
    if platform == "youtube":
        fn = _YT_SEND.get("fn")
        if not fn:
            return jsonify(ok=False, error=_t("YouTube nicht sendefähig "
                                              "(kein aktiver Live-Chat oder OAuth nicht "
                                              "konfiguriert — docs/SETUP_YT_OAUTH.md)")), 503
        try:
            _c().run_async(fn(text), timeout=15)
            return jsonify(ok=True)
        except Exception as e:
            return jsonify(ok=False, error=_fehler_text(e, "api_chat_send")), 500
    if platform in ("all", "broadcast"):
        # V37-W-CTRL: eine Ansage in ALLE sendefähigen eigenen Chats
        # (Kick + Twitch-mit-Token). Eine Aktion für "gleich gehts los".
        # B143: zusaetzlich strukturierte results{plattform:{ok,error}}, damit
        # das Dashboard pro Plattform Erfolg/Grund toasten kann (sent/failed
        # bleiben fuer den Discord-Announce-Aufrufer erhalten).
        done, fails, results = [], [], {}
        if _nc_channels.KICK_MOD["obj"]:
            ok, err = _c().run_async(_nc_channels.KICK_MOD["obj"].send_message(_nc_i18n.t(text)), timeout=15)
            results["kick"] = {"ok": bool(ok), "error": err}
            (done if ok else fails).append("kick" + (f" ({err})" if err else ""))
        else:
            results["kick"] = {"ok": False, "error": _t("Kick nicht verbunden")}
        fn = _TWITCH_SEND.get("fn")
        if fn:
            try:
                _c().run_async(fn(text), timeout=10); done.append("twitch")
                results["twitch"] = {"ok": True, "error": None}
            except Exception as e:
                fails.append(f"twitch ({e})")
                results["twitch"] = {"ok": False, "error": _fehler_text(e, "chat-twitch")}
        else:
            results["twitch"] = {"ok": False, "error": _t("Twitch nicht verbunden (IRC/chat:edit)")}
        ytf = _YT_SEND.get("fn")
        if ytf:
            try:
                _c().run_async(ytf(text), timeout=15); done.append("youtube")
                results["youtube"] = {"ok": True, "error": None}
            except Exception as e:
                fails.append(f"youtube ({e})")
                results["youtube"] = {"ok": False, "error": _fehler_text(e, "chat-youtube")}
        else:
            results["youtube"] = {"ok": False, "error": _t("YouTube nicht verbunden (OAuth)")}
        return jsonify(ok=bool(done), sent=done, failed=fails, results=results)
    return jsonify(ok=False, error=_t("platform muss kick|twitch|youtube|all sein")), 400
