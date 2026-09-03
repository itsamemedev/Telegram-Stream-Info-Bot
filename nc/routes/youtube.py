"""nc.routes.youtube — die Routen unter /api/youtube als Flask-Blueprint.

Welle 3 der Zerlegung (siehe docs/MODULARISIERUNG.md), erzeugt mit
tools/bp_extract.py. Pfade stehen woertlich in den Dekoratoren (kein
url_prefix); app-weite Hooks bleiben auf der App; was der Monolith weiterhin
stellen muss, kommt ueber nc.ctx statt ueber einen Import aus bot.py.

v4.1-W8: Die Gruppe kostete vor der Welle acht nc.ctx-Eintraege — drei fuer
die Rueckruf-Aufloesung, drei fuer YT-Cache/Sende-Bremse, dazu die
Normalisierung. Alle sechs liegen jetzt in nc/oauthredirect.py bzw.
nc/channels.py und werden direkt importiert. Aus dem Kontext kommt nur noch
run_async, das es ohnehin schon gab. Neue Kontext-Eintraege: null.

YT_SEND, YT_SENDRATE und YT_API_CACHE sind GETEILTER Zustand: der Bot schreibt
hinein (Token-Erneuerung, Sende-Bremse), diese Routen lesen und verwerfen ihn.
Der direkte Import trifft dasselbe Objekt — eine zweite Kopie waere ein
Zustandsriss, bei dem der Trennen-Knopf den Bot-Cache nicht mehr leert.
"""

import os
import time as _time_mod

from flask import Blueprint, jsonify, redirect, request

import nc.ytoauth as _ytoauth
from nc import i18n as _nc_i18n
from nc import sendrate as _nc_sendrate
from nc.channels import YT_API_CACHE as _YT_API_CACHE
from nc.channels import YT_SEND as _YT_SEND
from nc.channels import YT_SENDRATE as _YT_SENDRATE
from nc.channels import yt_sendrate_cfg as _yt_sendrate_cfg
from nc.cfgstore import set_ as _cfg_set
from nc.oauthpage import twitch as _oauth_page
from nc.oauthredirect import redirect_public as _redirect_public
from nc.oauthredirect import redirect_source as _redirect_source
from nc.oauthredirect import redirect_uri as _redirect_uri
from nc.util import _loop_not_ready

from nc import ctx as _ctx

bp = Blueprint("youtube", __name__)

def _t(s):
    """v4.1-W20: an der Quelle uebersetzen. Diese Texte erreichen das DOM
       meist verkettet ("Fehler: " + error) — ein Katalogeintrag fuer den
       blossen Text traefe dort nie."""
    return _nc_i18n.t(s)



def _c():
    """Laufzeitkontext. Aufruf statt Modul-Konstante — der Kontext wird erst
       beim Bot-Start gefuellt."""
    return _ctx.get()


@bp.route("/api/youtube/oauth/status")
def api_youtube_oauth_status():
    try:
        st = _ytoauth.status()
        # Google erlaubt als Redirect nur HTTPS oder http://localhost:PORT —
        # eine nackte IP wird abgelehnt (kein Zertifikat moeglich). Hinter dem
        # nginx-Proxy ist genau die Adresse richtig, unter der das Dashboard
        # gerade geoeffnet ist; frueher stand hier stur localhost:3000, und
        # Google brach mit redirect_uri_mismatch ab (siehe _public_base_url).
        eff = _redirect_uri("youtube")
        src = _redirect_source("youtube")
        st["redirect_uri"] = eff
        st["redirect_source"] = src
        st["redirect_forced"] = src != "fallback"
        st["redirect_public"] = _redirect_public(eff)
        # Ein Tunnel ist nur noetig, solange die Adresse auf localhost zeigt.
        st["needs_tunnel"] = not st["redirect_public"]
        return jsonify(ok=True, **st)
    except Exception as e:
        return jsonify(ok=False, error=str(e)), 500


@bp.route("/api/youtube/oauth/redirect", methods=["POST"])
def api_youtube_oauth_redirect():
    """Redirect-URI live setzen (app_config), ohne .env/Neustart — wie bei Kick.
       Muss danach 1:1 in der Google-Cloud-Console unter 'Autorisierte
       Weiterleitungs-URIs' stehen. Leerer Wert loescht die Ueberschreibung."""
    data = request.get_json(silent=True) or {}
    uri = str(data.get("uri", "") or "").strip()
    if uri:
        low = uri.lower()
        if not (low.startswith("http://") or low.startswith("https://")):
            return jsonify(ok=False, error=_t("URI muss mit http:// oder https:// beginnen")), 400
        if not low.endswith("/api/youtube/oauth/callback"):
            return jsonify(ok=False, error=_t("URI muss auf /api/youtube/oauth/callback enden "
                                              "(exakt dieser Pfad ist die Rueckruf-Route)")), 400
        if low.startswith("http://") and "localhost" not in low and "127.0.0.1" not in low:
            return jsonify(ok=False, error=_t("Google akzeptiert http:// nur fuer localhost — "
                                              "sonst https:// verwenden")), 400
    _cfg_set("youtube.redirect_uri", uri)
    eff = _redirect_uri("youtube")
    return jsonify(ok=True, redirect_uri=eff,
                   redirect_source=_redirect_source("youtube"),
                   redirect_public=_redirect_public(eff))


@bp.route("/api/youtube/oauth/start")
def api_youtube_oauth_start():
    import secrets
    if not (os.getenv("YOUTUBE_CLIENT_ID", "") or "").strip():
        return jsonify(ok=False, error=_t("YOUTUBE_CLIENT_ID fehlt in der .env")), 400
    if not (os.getenv("YOUTUBE_CLIENT_SECRET", "") or "").strip():
        return jsonify(ok=False, error=_t("YOUTUBE_CLIENT_SECRET fehlt in der .env")), 400
    redirect_uri = _redirect_uri("youtube")
    # 'select_account consent' ausdruecklich mitgeben statt auf den Modul-
    # Default zu bauen: das ist die Kontoauswahl, ohne die man mit mehreren
    # Google-Konten immer beim zuletzt benutzten landet.
    url = _ytoauth.authorize_url(secrets.token_urlsafe(16), redirect_uri=redirect_uri,
                                 prompt="select_account consent")
    if not url:
        return jsonify(ok=False, error=_t("Authorize-URL nicht baubar")), 400
    return redirect(url)


@bp.route("/api/youtube/oauth/callback")
def api_youtube_oauth_callback():
    import aiohttp
    err = request.args.get("error")
    if err:
        return _oauth_page(False, f"Google lehnte ab: {err} "
                                  f"({request.args.get('error_description', '')})")
    code = (request.args.get("code") or "").strip()
    state = (request.args.get("state") or "").strip()
    if not code:
        return _oauth_page(False, "Kein ?code in der URL"), 400
    ok, msg = _c().run_async(
        _ytoauth.exchange_code(code, state, aiohttp), timeout=25)
    if ok:
        # Token-Cache invalidieren, damit der naechste Aufruf sofort den
        # frischen Zugang nutzt statt auf den alten Ablauf zu warten.
        _YT_SEND["token"], _YT_SEND["token_exp"] = "", 0
        _YT_API_CACHE.update(ts=0.0, data=None)
    return _oauth_page(ok, msg)


@bp.route("/api/youtube/oauth/forget", methods=["POST"])
def api_youtube_oauth_forget():
    """Verbindung loesen (z.B. vor dem Wechsel auf einen anderen Kanal)."""
    try:
        _ytoauth.forget()
        _YT_SEND["token"], _YT_SEND["token_exp"] = "", 0
        _YT_API_CACHE.update(ts=0.0, data=None)
        return jsonify(ok=True)
    except Exception as e:
        return jsonify(ok=False, error=str(e)), 500


@bp.route("/api/youtube/oauth/logout", methods=["POST"])
def api_youtube_oauth_logout():
    """Vom Google-Konto abmelden: Zugriff BEI GOOGLE widerrufen und lokal
       loeschen. Unterschied zu /forget: danach ist auch die Freigabe im
       Google-Konto weg, der naechste Verbindungsversuch fragt wieder nach
       Konto und Zustimmung. Das ist der Weg, um auf ein anderes Google-Konto
       zu wechseln, ohne myaccount.google.com von Hand aufzurufen."""
    import aiohttp
    # Stammt der Token aus der .env, ueberlebt er das Abmelden: beim naechsten
    # Start liest ytoauth ihn dort wieder ein — dann steht "verbunden (.env)"
    # im Panel, waehrend der Zugriff bei Google laengst widerrufen ist. Das
    # sagen wir, statt es den Betreiber suchen zu lassen.
    _aus_env = (os.getenv("YOUTUBE_REFRESH_TOKEN", "") or "").strip()
    try:
        ok, msg = _c().run_async(_ytoauth.revoke(aiohttp), timeout=25)
    except RuntimeError as e:
        if _loop_not_ready(e):
            # Ohne Loop kein Netz-Aufruf — wenigstens lokal sauber trennen,
            # damit der Knopf nicht wirkungslos aussieht.
            _ytoauth.forget()
            ok, msg = False, ("Bot-Loop startet noch — lokal getrennt, der "
                              "Widerruf bei Google muss wiederholt werden.")
        else:
            return jsonify(ok=False, error=str(e)), 500
    except Exception as e:
        return jsonify(ok=False, error=str(e)), 500
    _YT_SEND["token"], _YT_SEND["token_exp"] = "", 0
    _YT_API_CACHE.update(ts=0.0, data=None)
    if _aus_env:
        msg += (" Achtung: YOUTUBE_REFRESH_TOKEN steht noch in der .env — der "
                "Wert ist jetzt tot, wird beim naechsten Start aber wieder "
                "gelesen. Zeile dort entfernen.")
    return jsonify(ok=ok, message=msg)


@bp.route("/api/youtube/sendrate")
def api_youtube_sendrate():
    """v4.0-W23: Zustand der YT-Sende-Bremse (verworfen/gesendet, letzte Minute)."""
    try:
        cfg = _yt_sendrate_cfg()
        snap = _nc_sendrate.snapshot(_YT_SENDRATE, _time_mod.monotonic())
        return jsonify(ok=True, cfg=cfg, **snap)
    except Exception as e:
        return jsonify(ok=False, error=str(e)), 500
