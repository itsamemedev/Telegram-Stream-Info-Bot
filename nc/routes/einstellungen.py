"""nc.routes.einstellungen — v4.2-W145: die Einstellungen im Deck.

    GET  /api/einstellungen                 alle Schluessel, Quelle, Schutz — ohne Geheimnisse
    POST /api/einstellungen                 {"name", "wert"}  setzen (Datenbank > .env)
    POST /api/einstellungen/zuruecksetzen   {"name"}          wieder .env bzw. Vorgabe
    POST /api/einstellungen/uebernehmen     {}                .env einmal in die Datenbank

Die Regeln (was geschuetzt ist, was geheim ist, wie geladen wird) stehen in
nc/einstellungen.py. Hier steht nur, was eine Route zusaetzlich braucht:

  * Schreiben nur als JSON. Ein Formular einer fremden Seite kann den Typ
    application/json nicht ohne CORS-Vorabfrage senden, und die beantwortet
    das Deck nicht — so kommt kein Klick auf einer fremden Seite bis hierher.
    Das Deck laeuft ohne Token auf 127.0.0.1 (W84), und genau dort ist das
    der Riegel.
  * Fehlertexte nach aussen gesaeubert (nc/fehlertext.py), Gruende uebersetzt.
"""

import logging

from flask import Blueprint, jsonify, request

from nc import einstellungen as _nc_einst
from nc import fehlertext as _nc_fehlertext
from nc import i18n as _nc_i18n

bp = Blueprint("einstellungen", __name__)
log = logging.getLogger("TikTokBot")

# Eine abgelehnte Aenderung steht im Log (warning): wer versucht, einen
# geschuetzten Schluessel aus dem Deck zu setzen, soll dort zu finden sein.


def _t(s):
    return _nc_i18n.t(s)


def _json():
    """Der Rumpf — oder None, wenn es kein JSON-Objekt ist.

    Der Riegel ist get_json OHNE force: Flask liest den Rumpf nur bei
    Content-Type application/json. Eine eigene is_json-Pruefung davor war
    wirkungslos doppelt — die Mutationsprobe hat sie entfernt, und nichts
    fiel (W105: zwei Riegel, von denen einer wirkt, sind einer und eine
    falsche Gewissheit). force=True waere das Loch."""
    d = request.get_json(silent=True)
    return d if isinstance(d, dict) else None


def _nur_json():
    return jsonify(ok=False, error=_t("Nur als JSON (application/json) — "
                                       "so kommt kein Formular einer fremden Seite durch.")), 415


@bp.route("/api/einstellungen")
def api_einstellungen():
    try:
        u = _nc_einst.uebersicht()
    except Exception as e:
        return jsonify(ok=False, error=_nc_fehlertext.nach_aussen(e, "api_einstellungen")), 503
    for e in u["eintraege"]:
        if e["schutz"]:
            e["schutz"] = _t(e["schutz"])
    return jsonify(ok=True, **u)


@bp.route("/api/einstellungen", methods=["POST"])
def api_einstellungen_setzen():
    d = _json()
    if d is None:
        return _nur_json()
    name, wert = str(d.get("name") or "").strip(), d.get("wert")
    try:
        _nc_einst.setzen(name, wert, von="deck")
    except _nc_einst.Abgelehnt as e:
        log.warning("Deck: Einstellung %s setzen abgelehnt — %s", name or "?", e)
        return jsonify(ok=False, error=_t(e.grund)), 400
    except Exception as e:
        return jsonify(ok=False, error=_nc_fehlertext.nach_aussen(e, "api_einstellungen_setzen")), 503
    return jsonify(ok=True, name=name, neustart=True,
                   hinweis=_t("Gespeichert. Viele Werte liest der Bot nur beim Start — "
                              "sicher wirkt die Änderung nach einem Neustart."))


@bp.route("/api/einstellungen/zuruecksetzen", methods=["POST"])
def api_einstellungen_zuruecksetzen():
    d = _json()
    if d is None:
        return _nur_json()
    name = str(d.get("name") or "").strip()
    try:
        _nc_einst.zuruecksetzen(name)
    except _nc_einst.Abgelehnt as e:
        log.warning("Deck: Einstellung %s zuruecksetzen abgelehnt — %s", name or "?", e)
        return jsonify(ok=False, error=_t(e.grund)), 400
    except Exception as e:
        return jsonify(ok=False, error=_nc_fehlertext.nach_aussen(e, "api_einstellungen_zuruecksetzen")), 503
    return jsonify(ok=True, name=name, neustart=True)


@bp.route("/api/einstellungen/uebernehmen", methods=["POST"])
def api_einstellungen_uebernehmen():
    if _json() is None:
        return _nur_json()
    try:
        aus = _nc_einst.uebernehmen(von="deck")
    except Exception as e:
        return jsonify(ok=False, error=_nc_fehlertext.nach_aussen(e, "api_einstellungen_uebernehmen")), 503
    return jsonify(ok=True, neustart=bool(aus["uebernommen"]), **aus)
