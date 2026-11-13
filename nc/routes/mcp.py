"""nc.routes.mcp — v5.6-W198: MCP-Server im Deck verwalten.

    GET    /api/mcp/server             {"ok", "server": [...], "lage": {...}}
    POST   /api/mcp/server             anlegen  {name, url, token?, aktiv?, notiz?}
    POST   /api/mcp/server/<sid>       ändern   (token weggelassen = unverändert, "" = löschen)
    DELETE /api/mcp/server/<sid>       löschen
    POST   /api/mcp/server/<sid>/test  Verbindungstest — ok=true heißt: die Route lief;
                                       ob der Server erreichbar war, steht in test.ok
    GET    /api/mcp/export[?mit_token=1]  Datei mcp_server.json für einen MCP-Client

Die Regeln (Eingaben, Token, Protokoll, Frist, Deckel) stehen in
nc/mcpdienste.py. Hier steht nur, was eine Route zusätzlich braucht:

  * Anlegen und Ändern nur als JSON. Ein Formular einer fremden Seite kann
    application/json nicht ohne CORS-Vorabfrage senden, und die beantwortet
    das Deck nicht. Anmeldung und Herkunftsprüfung (nc/herkunft.py) gelten
    wie für jede andere /api-Route — hier steht bewusst keine Ausnahme.
  * Gründe in der Sprache der Anfrage: das Modul liefert die deutsche
    Vorlage mit Werten, übersetzt wird hier und erst dann gefüllt.
  * Fehlertexte nach außen gesäubert (nc/fehlertext.py).
"""

import json
import logging

from flask import Blueprint, Response, jsonify, request

from nc import fehlertext as _nc_fehlertext
from nc import i18n as _nc_i18n
from nc import mcpdienste as _nc_mcp

bp = Blueprint("mcp", __name__)
log = logging.getLogger("TikTokBot")

# Innenfelder eines Testergebnisses: daraus entsteht der übersetzte Grund,
# hinaus gehen sie nicht.
_INNEN = ("grund_vorlage", "grund_werte")


def _t(s, **kw):
    return _nc_i18n.t(s, **kw)


def _json():
    """Der Rumpf — oder None, wenn es kein JSON-Objekt ist. get_json OHNE
    force: Flask liest den Rumpf nur bei Content-Type application/json."""
    d = request.get_json(silent=True)
    return d if isinstance(d, dict) else None


def _nur_json():
    return jsonify(ok=False, error=_t("Nur als JSON (application/json) — "
                                       "so kommt kein Formular einer fremden Seite durch.")), 415


def _unbekannt():
    return jsonify(ok=False, error=_t(_nc_mcp.UNBEKANNT)), 404


def _test_aussen(test):
    """Ein Testergebnis für die Antwort: Grund übersetzt, Innenfelder weg."""
    if not isinstance(test, dict):
        return test
    aus = {k: v for k, v in test.items() if k not in _INNEN}
    vorlage = test.get("grund_vorlage")
    if vorlage:
        aus["grund"] = _t(vorlage, **(test.get("grund_werte") or {}))
    return aus


def _server_aussen(s):
    aus = dict(s)
    aus["letzter_test"] = _test_aussen(s.get("letzter_test"))
    return aus


def _lage_aussen(lage):
    w = dict(lage["webui"])
    if w.get("abhilfe"):
        w["abhilfe"] = _t(w["abhilfe"])
    return dict(lage, webui=w)


@bp.route("/api/mcp/server")
def api_mcp_server_liste():
    try:
        server = _nc_mcp.liste()
        lage = _nc_mcp.lage(server=server)
    except Exception as e:
        return jsonify(ok=False, error=_nc_fehlertext.nach_aussen(e, "api_mcp_server_liste")), 503
    return jsonify(ok=True, server=[_server_aussen(s) for s in server], lage=_lage_aussen(lage))


def _speichern(sid, wo):
    d = _json()
    if d is None:
        return _nur_json()
    try:
        erfolg, aus = _nc_mcp.speichern(d, sid)
    except Exception as e:
        # Auch BestandUnbekannt: wer nicht lesen kann, was gespeichert ist,
        # schreibt nicht — 503, nicht 400. Der Betreiber soll es erneut
        # versuchen, nicht seine Eingabe ändern.
        return jsonify(ok=False, error=_nc_fehlertext.nach_aussen(e, wo)), 503
    if not erfolg:
        return jsonify(ok=False, error=_t(aus)), (404 if aus == _nc_mcp.UNBEKANNT else 400)
    return jsonify(ok=True, server=_server_aussen(aus))


@bp.route("/api/mcp/server", methods=["POST"])
def api_mcp_server_anlegen():
    return _speichern(None, "api_mcp_server_anlegen")


@bp.route("/api/mcp/server/<sid>", methods=["POST"])
def api_mcp_server_aendern(sid):
    return _speichern(sid, "api_mcp_server_aendern")


@bp.route("/api/mcp/server/<sid>", methods=["DELETE"])
def api_mcp_server_loeschen(sid):
    try:
        weg = _nc_mcp.loeschen(sid)
    except Exception as e:
        return jsonify(ok=False, error=_nc_fehlertext.nach_aussen(e, "api_mcp_server_loeschen")), 503
    if not weg:
        return _unbekannt()
    return jsonify(ok=True)


@bp.route("/api/mcp/server/<sid>/test", methods=["POST"])
def api_mcp_server_test(sid):
    # Kein JSON-Zwang: der Test liest keinen Rumpf, und die Herkunftsprüfung
    # der App weist einen POST einer fremden Seite ohnehin ab.
    try:
        test = _nc_mcp.testen(sid)
    except _nc_mcp.Unbekannt:
        log.info("MCP-Test: unbekannte Kennung %r aus dem Deck.", str(sid)[:16])
        return _unbekannt()
    except Exception as e:
        return jsonify(ok=False, error=_nc_fehlertext.nach_aussen(e, "api_mcp_server_test")), 503
    return jsonify(ok=True, test=_test_aussen(test))


@bp.route("/api/mcp/export")
def api_mcp_export():
    mit_token = (request.args.get("mit_token") or "").strip().lower() in ("1", "true", "ja", "yes")
    try:
        daten = _nc_mcp.export(mit_token=mit_token)
    except Exception as e:
        return jsonify(ok=False, error=_nc_fehlertext.nach_aussen(e, "api_mcp_export")), 503
    if mit_token:
        n = sum(1 for e in daten["mcpServers"].values() if "headers" in e)
        # Die einzige Stelle, an der ein Token den Server verlässt — im Log
        # zu finden, wenn später jemand fragt, wann.
        log.warning("MCP-Export MIT Token aus dem Deck (%d von %d Servern mit Token).",
                    n, len(daten["mcpServers"]))
    antwort = Response(json.dumps(daten, ensure_ascii=False, indent=2) + "\n",
                       mimetype="application/json")
    antwort.headers["Content-Disposition"] = 'attachment; filename="mcp_server.json"'
    # Eine Datei mit Zugangsdaten gehört in keinen Browser- oder Proxy-Zwischenspeicher.
    antwort.headers["Cache-Control"] = "no-store"
    return antwort
