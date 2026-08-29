"""nc.routes.i18n — Sprachkatalog und Sprachwahl als Flask-Blueprint.

v4.1-W6. Ohne nc.ctx: der Katalog liegt in nc/i18n.py, die Sprachwahl steckt in
Request und Cookie — der Monolith muss dafuer nichts stellen.

Die Oberflaeche uebersetzt im Browser, nicht auf dem Server. Warum: das
Dashboard ist eine JS-Oberflaeche, die den grossen Teil ihrer Texte selbst
erzeugt (Tabellenzeilen, Meldungen, Panels). Serverseitiges Rendern haette nur
das feste Geruest getroffen und den Rest auf Deutsch stehen lassen — sichtbar
zweisprachig, also schlimmer als gar nicht.
"""

from flask import Blueprint, jsonify, make_response, request

from nc import i18n as _nc_i18n

bp = Blueprint("i18n", __name__)

# Ein Jahr. Die Sprachwahl ist eine Vorliebe, keine Sitzung — sie soll einen
# Neustart des Browsers ueberleben.
_COOKIE = "nc_lang"
_COOKIE_MAX_AGE = 365 * 24 * 3600


def aktive_sprache():
    """Die Sprache dieses Requests.

    Reihenfolge, absichtlich in dieser: ausdrueckliche Wahl (?lang=) schlaegt
    gespeicherte Wahl (Cookie) schlaegt Browser-Wunsch (Accept-Language)
    schlaegt Standard. Eine gesetzte Wahl darf der Browser nie ueberstimmen —
    sonst springt die Oberflaeche beim naechsten Geraet wieder zurueck.
    """
    aus_query = _nc_i18n.normalisieren(request.args.get("lang"))
    if aus_query:
        return aus_query
    aus_cookie = _nc_i18n.normalisieren(request.cookies.get(_COOKIE))
    if aus_cookie:
        return aus_cookie
    aus_browser = _nc_i18n.aus_accept_language(request.headers.get("Accept-Language"))
    if aus_browser:
        return aus_browser
    return _nc_i18n.standard()


@bp.route("/api/i18n/sprachen")
def api_i18n_sprachen():
    """Welche Sprachen es gibt und welche gerade gilt — fuer den Umschalter."""
    return jsonify(ok=True,
                   aktiv=aktive_sprache(),
                   standard=_nc_i18n.standard(),
                   quelle=_nc_i18n.QUELLSPRACHE,
                   sprachen=[{"code": c, "name": _nc_i18n.SPRACHNAMEN.get(c, c)}
                             for c in _nc_i18n.SPRACHEN])


@bp.route("/api/i18n/katalog")
def api_i18n_katalog():
    """Der Katalog der aktiven (oder per ?lang= gewuenschten) Sprache.

    Fuer Deutsch ist er leer — die Quellsprache braucht keine Uebersetzung, und
    ein leerer Katalog laesst den Uebersetzer im Browser sofort aufhoeren.
    """
    sprache = aktive_sprache()
    return jsonify(ok=True, sprache=sprache,
                   quelle=_nc_i18n.QUELLSPRACHE,
                   strings=_nc_i18n.katalog(sprache))


@bp.route("/api/i18n/waehlen", methods=["POST"])
def api_i18n_waehlen():
    """Sprache setzen und im Cookie merken.

    Bewusst ein POST mit Cookie und nicht nur localStorage: die Wahl muss auch
    dort gelten, wo der Server die Seite ausliefert — sonst blitzt beim Laden
    erst Deutsch auf und springt dann um.
    """
    daten = request.get_json(silent=True) or {}
    gewuenscht = _nc_i18n.normalisieren(daten.get("sprache") or request.args.get("lang"))
    if not gewuenscht:
        return jsonify(ok=False, error="unbekannte Sprache",
                       sprachen=list(_nc_i18n.SPRACHEN)), 400
    antwort = make_response(jsonify(ok=True, sprache=gewuenscht))
    antwort.set_cookie(_COOKIE, gewuenscht, max_age=_COOKIE_MAX_AGE,
                       samesite="Lax", httponly=False)
    return antwort
