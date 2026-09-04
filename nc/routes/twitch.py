"""nc.routes.twitch — die Routen unter /api/twitch als Flask-Blueprint.

Welle 3 der Zerlegung (siehe docs/MODULARISIERUNG.md), erzeugt mit
tools/bp_extract.py. Pfade stehen woertlich in den Dekoratoren (kein
url_prefix); app-weite Hooks bleiben auf der App; was der Monolith weiterhin
stellen muss, kommt ueber nc.ctx statt ueber einen Import aus bot.py.

v4.1-W8: Diese Gruppe kostete vor der Welle DREI nc.ctx-Slots, allein fuer
die Rueckruf-Aufloesung. Seit sie in nc/oauthredirect.py liegt, importiert
das Blueprint sie direkt; aus dem Kontext kommt nur noch run_async, das es
ohnehin schon gab. Neue Kontext-Eintraege: null.
"""

import os
from flask import Blueprint, jsonify, redirect, request

from nc import fehlertext as _nc_fehlertext

from nc import i18n as _nc_i18n

import nc.twitchoauth as _twoauth
from nc.cfgstore import set_ as _cfg_set
from nc.oauthpage import twitch as _twitch_oauth_page
from nc.oauthredirect import redirect_public as _redirect_public
from nc.oauthredirect import redirect_source as _redirect_source
from nc.oauthredirect import redirect_uri as _redirect_uri

from nc import ctx as _ctx

bp = Blueprint("twitch", __name__)


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


@bp.route("/api/twitch/oauth/status")
def api_twitch_oauth_status():
    """V37-TWOAUTH: Was ist konfiguriert, ist der Flow abgeschlossen?"""
    try:
        st = _twoauth.status()
        # Die Redirect-URI melden, die der Nutzer in der Twitch-App eintragen
        # MUSS. Twitch erlaubt nur HTTPS oder http://localhost — eine IP mit
        # https wird abgelehnt. Default localhost:3000 (per SSH-Tunnel), oder
        # der erzwungene TWITCH_REDIRECT_URI (echte Domain mit HTTPS).
        # Wie bei Kick/YouTube: ohne Vorgabe die Adresse, unter der das
        # Dashboard gerade laeuft (hinter dem Proxy also die echte Domain).
        eff = _redirect_uri("twitch")
        st["redirect_uri"] = eff
        st["redirect_source"] = _redirect_source("twitch")
        st["redirect_forced"] = st["redirect_source"] != "fallback"
        st["redirect_public"] = _redirect_public(eff)
        st["needs_tunnel"] = not st["redirect_public"]
        return jsonify(ok=True, **st)
    except Exception as e:
        return jsonify(ok=False, error=_fehler_text(e, "api_twitch_oauth_status")), 500


@bp.route("/api/twitch/oauth/redirect", methods=["POST"])
def api_twitch_oauth_redirect():
    """Redirect-URI live setzen (app_config), ohne .env/Neustart — wie bei Kick
       und YouTube. Muss danach 1:1 in der Twitch-App unter 'OAuth Redirect
       URLs' stehen. Leerer Wert loescht die Ueberschreibung."""
    data = request.get_json(silent=True) or {}
    uri = str(data.get("uri", "") or "").strip()
    if uri:
        low = uri.lower()
        if not (low.startswith("http://") or low.startswith("https://")):
            return jsonify(ok=False, error=_t("URI muss mit http:// oder https:// beginnen")), 400
        if not low.endswith("/api/twitch/oauth/callback"):
            return jsonify(ok=False, error=_t("URI muss auf /api/twitch/oauth/callback enden "
                                              "(exakt dieser Pfad ist die Rueckruf-Route)")), 400
        if low.startswith("http://") and "localhost" not in low and "127.0.0.1" not in low:
            return jsonify(ok=False, error=_t("Twitch akzeptiert http:// nur fuer localhost — "
                                              "sonst https:// verwenden")), 400
    _cfg_set("twitch.redirect_uri", uri)
    eff = _redirect_uri("twitch")
    return jsonify(ok=True, redirect_uri=eff,
                   redirect_source=_redirect_source("twitch"),
                   redirect_public=_redirect_public(eff))


@bp.route("/api/twitch/oauth/start")
def api_twitch_oauth_start():
    """Schritt 1: leitet zum Twitch-Zustimmungsdialog um. CSRF-state in der
       Session-freien Umgebung: wir merken ihn im Modul (Single-User-Dashboard)."""
    import secrets
    cid = (os.getenv("TWITCH_CLIENT_ID", "") or "").strip()
    if not cid:
        return jsonify(ok=False, error=_t("TWITCH_CLIENT_ID fehlt in der .env")), 400
    if not (os.getenv("TWITCH_CLIENT_SECRET", "") or "").strip():
        return jsonify(ok=False, error=_t("TWITCH_CLIENT_SECRET fehlt in der .env")), 400
    # V37-TWOAUTH-FIX2: Twitch verlangt bei Redirect-URIs HTTPS — mit EINER
    # Ausnahme: http://localhost:PORT ist erlaubt. Eine IP mit https geht NICHT
    # (kein Zertifikat fuer nackte IPs). Deshalb ist der Default localhost:3000,
    # das der Nutzer per SSH-Tunnel auf den Bot legt (docs/SETUP_TWITCH_OAUTH.md).
    # Wer eine echte Domain + HTTPS hat, setzt TWITCH_REDIRECT_URI darauf —
    # oder laesst es: hinter dem Proxy liefert nc.oauthredirect genau diese
    # Domain, ohne dass irgendwo eine Adresse doppelt gepflegt werden muss.
    redirect_uri = _redirect_uri("twitch")
    url = _twoauth.authorize_url(secrets.token_urlsafe(16), redirect_uri=redirect_uri)
    if not url:
        return jsonify(ok=False, error=_t("Authorize-URL nicht baubar")), 400
    return redirect(url)


@bp.route("/api/twitch/oauth/callback")
def api_twitch_oauth_callback():
    """Schritt 2: Twitch schickt ?code hierher. Gegen Refresh-Token tauschen.

    Der Redirect zeigt zwar auf localhost:3000 (so in der App eingetragen), aber
    der Nutzer kann den ?code-Teil der URL auch von Hand hierher kopieren, falls
    das Dashboard nicht unter localhost:3000 laeuft. Beide Wege landen hier.
    """
    import aiohttp
    err = request.args.get("error")
    if err:
        return _twitch_oauth_page(False, f"Twitch lehnte ab: {err} "
                                  f"({request.args.get('error_description', '')})")
    code = (request.args.get("code") or "").strip()
    state = (request.args.get("state") or "").strip()
    if not code:
        return _twitch_oauth_page(False, "Kein ?code in der URL"), 400
    ok, msg = _c().run_async(
        _twoauth.exchange_code(code, state, aiohttp), timeout=25)
    return _twitch_oauth_page(ok, msg)
