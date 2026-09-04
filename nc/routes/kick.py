"""nc.routes.kick — die Routen unter /api/kick als Flask-Blueprint.

Welle 3 der Zerlegung (siehe docs/MODULARISIERUNG.md), erzeugt mit
tools/bp_extract.py. Pfade stehen woertlich in den Dekoratoren (kein
url_prefix); app-weite Hooks bleiben auf der App; was der Monolith weiterhin
stellen muss, kommt ueber nc.ctx statt ueber einen Import aus bot.py.

v4.1-W9: Die Gruppe kostete vor der Welle elf nc.ctx-Eintraege und war damit
die teuerste offene Gruppe ueberhaupt. Geloest wurden Slug, Broadcaster-ID,
Sendeprotokoll und Token-Tausch (nc/kickapi.py), die Rueckruf-Adressen
(nc/oauthredirect.py, W8) und der Zugriff auf den laufenden Moderator
(nc/channels.py). Uebrig bleiben run_async und log — beide gab es schon.
Neue Kontext-Eintraege: null.

Der Moderator kommt aus dem Register nc.channels.KICK_MOD, NICHT aus
globals(): im Monolithen stand dort globals().get("_KICK_MOD"), und in einem
Blueprint waere globals() dessen eigener Namensraum — der Wert waere fuer
immer None und /api/kick/sendcheck meldete "Kick-Moderator laeuft nicht",
waehrend er laeuft. Dieselbe stille Fehlanzeige wie bei _MAIN_LOOP in W116.
"""

import time as _time_mod

from flask import Blueprint, jsonify, request

from nc import channels as _nc_channels
from nc import fehlertext as _nc_fehlertext
from nc import i18n as _nc_i18n
from nc import kick_oauth as _nc_kickoauth
from nc.cfgstore import get as _cfg_get
from nc.cfgstore import set_ as _cfg_set
from nc.kickapi import SEND_LAST as _KICK_SEND_LAST
from nc.kickapi import broadcaster_id as _kick_broadcaster_id
from nc.kickapi import oauth_exchange as _kick_oauth_exchange
from nc.kickapi import slug as _kick_slug
from nc.oauthpage import kick as _oauth_page
from nc.oauthredirect import redirect_public as _redirect_public
from nc.oauthredirect import redirect_source as _redirect_source
from nc.oauthredirect import redirect_uri as _redirect_uri
from nc.util import _loop_not_ready

from nc import ctx as _ctx

bp = Blueprint("kick", __name__)


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


def _kick_redirect_uri():
    # v4.0-W23: app_config schlaegt .env schlaegt Fallback. Damit laesst sich die
    # Redirect-URI LIVE im Dashboard setzen — ohne .env/systemd-Neustart, der die
    # haeufigste Ursache fuer "steht immer noch auf localhost:8050" ist (Variable
    # nicht in der EnvironmentFile oder Bot nicht neu gestartet).
    return _redirect_uri("kick")


@bp.route("/api/kick/oauth/start")
def api_kick_oauth_start():
    # v4.2-W1: das Boolean statt der beiden Werte. Das Secret stand nur fuer
    # diese drei Ja/Nein-Fragen im Kontext und war damit fuer JEDES der 35
    # Blueprints erreichbar — Angriffsflaeche ohne Gegenwert.
    if not _c().cfg["HAT_KICK_CREDS"]:
        return jsonify(ok=False, error=_t("KICK_CLIENT_ID/SECRET fehlen — Kick-Developer-App "
                                          "unter kick.com/settings/developer anlegen")), 400
    redirect = _kick_redirect_uri()
    verifier, challenge = _nc_kickoauth.gen_pkce()
    state = _nc_kickoauth.gen_state()
    _cfg_set("kick.oauth_pending", {"verifier": verifier, "state": state,
                                    "ts": _time_mod.time(), "redirect": redirect})
    url = _nc_kickoauth.build_authorize_url(
        _c().cfg["KICK_CLIENT_ID"], redirect, _nc_kickoauth.DEFAULT_SCOPES, state, challenge)
    return jsonify(ok=True, auth_url=url, redirect_uri=redirect)


@bp.route("/api/kick/oauth/callback")
def api_kick_oauth_callback():
    if request.args.get("error"):
        return _oauth_page(False, f"Kick lehnte ab: {request.args.get('error')}")
    code = request.args.get("code", "")
    state = request.args.get("state", "")
    pending = _cfg_get("kick.oauth_pending", None) or {}
    if not code or not pending:
        return _oauth_page(False, "Kein Code oder kein laufender Flow.")
    if state != pending.get("state"):
        return _oauth_page(False, "State stimmt nicht — Abbruch aus Sicherheitsgründen.")
    try:
        res = _c().run_async(_kick_oauth_exchange(code, pending), timeout=30)
    except Exception as e:
        if _loop_not_ready(e):
            return _oauth_page(False, "Event-Loop startet noch — kurz erneut versuchen.")
        return _oauth_page(False, f"Token-Tausch fehlgeschlagen: {_fehler_text(e, 'api_kick_oauth_callback')}")
    _cfg_set("kick.oauth_pending", {})
    if not res.get("ok"):
        return _oauth_page(False, res.get("error") or "Token-Tausch fehlgeschlagen.")
    scope = res.get("scope", "")
    extra = "" if "channel:write" in scope else " (Achtung: channel:write NICHT gewährt — Titel/Kategorie bleiben gesperrt)"
    return _oauth_page(True, f"Kick verbunden. Scopes: {scope}{extra}")


@bp.route("/api/kick/oauth/status")
def api_kick_oauth_status():
    tok = _cfg_get("kick.user_token", None) or {}
    connected = bool(tok.get("access_token"))
    now = _time_mod.time()
    return jsonify(ok=True, connected=connected, scope=tok.get("scope", ""),
                   has_channel_write=_nc_kickoauth.has_scope(tok, "channel:write"),
                   # W17: ohne diese beiden antwortet Kick auf Chat/Timeouts mit 401
                   has_chat_write=_nc_kickoauth.has_scope(tok, "chat:write"),
                   has_moderation=_nc_kickoauth.has_scope(tok, "moderation:ban"),
                   expired=(_nc_kickoauth.is_expired(tok, now) if connected else None),
                   expires_in=(int(tok.get("expires_at", 0) - now) if tok.get("expires_at") else None),
                   client_configured=_c().cfg["HAT_KICK_CREDS"],   # v4.2-W1
                   redirect_uri=_kick_redirect_uri(),
                   # v4.0-W23: woher kommt die Redirect-URI + ist sie extern
                   # erreichbar? Das Panel warnt, wenn noch der localhost-Fallback
                   # aktiv ist (Kick erreicht den nie → OAuth scheitert).
                   redirect_source=_redirect_source("kick"),
                   redirect_public=_redirect_public(_kick_redirect_uri()))


@bp.route("/api/kick/oauth/redirect", methods=["POST"])
def api_kick_oauth_redirect():
    """v4.0-W23: Redirect-URI LIVE setzen (app_config), ohne .env/Neustart.
       Muss danach 1:1 in der Kick-Developer-App eingetragen sein. Leerer Wert
       loescht die Ueberschreibung → es gilt wieder .env bzw. der Fallback."""
    data = request.get_json(silent=True) or {}
    uri = str(data.get("uri", "") or "").strip()
    if uri:
        low = uri.lower()
        if not (low.startswith("http://") or low.startswith("https://")):
            return jsonify(ok=False, error=_t("URI muss mit http:// oder https:// beginnen")), 400
        if not low.endswith("/api/kick/oauth/callback"):
            return jsonify(ok=False, error=_t("URI muss auf /api/kick/oauth/callback enden "
                                              "(exakt dieser Pfad ist die Rueckruf-Route)")), 400
    _cfg_set("kick.redirect_uri", uri)
    eff = _kick_redirect_uri()
    return jsonify(ok=True, redirect_uri=eff, redirect_source=_redirect_source("kick"),
                   redirect_public=_redirect_public(eff),
                   note=("" if _redirect_public(eff)
                         else "Achtung: localhost ist von Kick aus nicht erreichbar."))


@bp.route("/api/kick/oauth/disconnect", methods=["POST"])
def api_kick_oauth_disconnect():
    _cfg_set("kick.user_token", {})
    _cfg_set("kick.oauth_pending", {})
    return jsonify(ok=True)


@bp.route("/api/kick/sendcheck", methods=["GET", "POST"])
def api_kick_sendcheck():
    """v4.0-W10: Warum schweigt AZRAEL auf Kick? GET = Diagnose ohne zu senden
       (Zugangsdaten da? Broadcaster-ID aufloesbar? letzter Sendeversuch/Fehler).
       POST = schickt EINE kurze Testzeile und meldet den echten Grund im Klartext."""
    creds = _c().cfg["HAT_KICK_CREDS"]   # v4.2-W1
    out = {
        "ok": True,
        "creds_configured": creds,
        "broadcaster_id_env": _c().cfg["KICK_BROADCASTER_ID"] or 0,
        "channel": _kick_slug() or "",
        # v4.1-W9: aus dem geteilten Register statt globals(). In einem
        # Blueprint waere globals() dessen eigener Namensraum — der Eintrag
        # waere fuer immer None und die Diagnose meldete "laeuft nicht",
        # waehrend der Moderator laeuft.
        "moderator_running": bool(_nc_channels.KICK_MOD["obj"]),
        "last": dict(_KICK_SEND_LAST),
    }
    if not creds:
        out["hinweis"] = ("KICK_CLIENT_ID/KICK_CLIENT_SECRET fehlen — ohne sie kann "
                          "der Bot auf Kick nicht schreiben (Lesen geht ohne).")
        return jsonify(out)
    if request.method == "GET":
        try:
            out["broadcaster_id_resolved"] = _c().run_async(
                _kick_broadcaster_id(), timeout=15)
        except Exception as e:
            out["broadcaster_id_resolved"] = 0
            out["hinweis"] = "Broadcaster-ID nicht aufloesbar: " + _fehler_text(e, "kick-broadcaster")
        return jsonify(out)
    mod = _nc_channels.KICK_MOD["obj"]
    if mod is None:
        out.update(ok=False, error=_t("Kick-Moderator laeuft nicht (KICK_CHATROOM_ID?)"))
        return jsonify(out)
    txt = (request.get_json(silent=True) or {}).get("text") or "Azrael Sentinel · Sendetest"
    try:
        sent, err = _c().run_async(mod.send_message(_nc_i18n.t(str(txt)[:120])), timeout=30)
    except Exception as e:
        out.update(ok=False, error=_fehler_text(e, "kick"))
        return jsonify(out)
    out.update(sent=bool(sent), error=(err or ""), last=dict(_KICK_SEND_LAST))
    return jsonify(out)


@bp.route("/api/kick/channel")
def api_kick_channel():
    """Kanal-Status: live, Zuschauer, Titel, Follower."""
    try:
        info, err = _c().run_async(
            _nc_channels.KICK_MOD["obj"].channel_info(), timeout=20)
        if err:
            return jsonify(ok=False, error=err), 502
        return jsonify(ok=True, channel=info)
    except RuntimeError as e:
        # B86-Fix: 'event loop not ready' ist KEIN Serverfehler — es ist das
        # normale Startup-Fenster (Dashboard lädt, asyncio-Loop fährt noch hoch)
        # ODER Kick ist nicht konfiguriert. Vorher fiel das in den generischen
        # 500-Zweig → Dashboard zeigte "Server-Fehler 500" als Push, aber nichts
        # stand im Log (still gefangen). Jetzt 503 (transient) — das Frontend
        # toastet 503 NICHT als Serverfehler.
        return jsonify(ok=False, error=_fehler_text(e, "api_kick_channel"), transient=True), 503
    except Exception as e:
        log.warning("api_kick_channel: %s", e)   # B85: jetzt auch geloggt
        return jsonify(ok=False, error=_fehler_text(e, "api_kick_channel")), 500


@bp.route("/api/kick/channel", methods=["POST"])
def api_kick_channel_set():
    """Stream-Titel / Kategorie setzen (PATCH /channels)."""
    d = request.get_json(silent=True) or {}
    title = d.get("title")
    cat = d.get("category_id")
    if title is None and not cat:
        return jsonify(ok=False, error=_t("title oder category_id nötig")), 400
    try:
        ok, err = _c().run_async(
            _nc_channels.KICK_MOD["obj"].update_channel(
                title=title, category_id=cat), timeout=20)
        return jsonify(ok=ok, error=err), (200 if ok else 502)
    except RuntimeError as e:
        if _loop_not_ready(e):
            return jsonify(ok=False, error=_t("Bot-Loop startet noch"), transient=True), 503
        return jsonify(ok=False, error=_fehler_text(e, "api_kick_channel_set")), 500
    except Exception as e:
        return jsonify(ok=False, error=_fehler_text(e, "api_kick_channel_set")), 500
