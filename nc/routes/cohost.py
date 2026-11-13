"""nc.routes.cohost — die Routen unter /api/cohost als Flask-Blueprint.

Welle 3 der Zerlegung (siehe docs/MODULARISIERUNG.md), erzeugt mit
tools/bp_extract.py. Pfade stehen woertlich in den Dekoratoren (kein
url_prefix); app-weite Hooks bleiben auf der App; was der Monolith weiterhin
stellen muss, kommt ueber nc.ctx statt ueber einen Import aus bot.py.

v4.1-W15: Dieses Blueprint braucht den Kontext GAR NICHT. Entscheidung,
Zustand und Konfigurations-Leser des Co-Hosts liegen vollstaendig in
nc/cohost.py; der Monolith haelt nur noch Aliase fuer seine drei Lesestellen.

STATE ist geteilt, nicht kopiert: der Co-Host-Pfad im Bot schreibt die Bremse
fort (decide), diese Route liest sie (snapshot). Zwei Kopien, und das
Dashboard zeigte eine Bremse, die nie zieht.
"""

import time as _time_mod

from flask import Blueprint, jsonify, request

from nc import cohost as _nc_cohost
from nc import fehlertext as _nc_fehlertext
from nc import cfgstore as _nc_cfgstore
from nc.cohost import STATE as _COHOST
from nc.cohost import config as _cohost_cfg

bp = Blueprint("cohost", __name__)


def _fehler_text(e, wo=""):
    """v4.1-W30: der Wortlaut geht ins Log, nach aussen die gesaeuberte
       Fassung — ohne Pfade, ohne Zugangsdaten, gekuerzt. Siehe
       nc/fehlertext.py, dort steht auch, warum nicht einfach "interner
       Fehler"."""
    return _nc_fehlertext.nach_aussen(e, wo)


@bp.route("/api/cohost")
def api_cohost():
    """v4.0-W24: Status des proaktiven Co-Hosts — an/aus, Bremse, letzte Impulse."""
    try:
        cfg = _cohost_cfg()
        snap = _nc_cohost.snapshot(_COHOST, _time_mod.monotonic())
        return jsonify(ok=True, enabled=cfg["enabled"], min_gap_s=cfg["min_gap_s"],
                       per_15min=cfg["per_15min"], kinds=cfg["kinds"], **snap)
    except Exception as e:
        return jsonify(ok=False, error=_fehler_text(e, "api_cohost")), 500


@bp.route("/api/cohost/config", methods=["POST"])
def api_cohost_config():
    """v4.0-W24: Co-Host live schalten/justieren (app_config, kein Neustart)."""
    d = request.get_json(silent=True) or {}
    # v5.8-W199: streng gelesen und in einem Schritt angewandt. get(…, None)
    # setzte bei gesperrter Datenbank jedes nicht genannte Feld (auch die
    # Abklingzeiten je Art) still auf die Vorgabe zurück (nc/cfgstore.aendern).
    try:
        _nc_cfgstore.aendern("azrael.cohost", lambda alt: _cohost_anwenden(dict(alt), d),
                             fehlt={}, art=dict)
    except Exception as e:
        return jsonify(ok=False, error=_nc_fehlertext.nach_aussen(e, "api_cohost_config")), 503
    cfg = _cohost_cfg()
    return jsonify(ok=True, enabled=cfg["enabled"], min_gap_s=cfg["min_gap_s"],
                   per_15min=cfg["per_15min"], kinds=cfg["kinds"])


def _cohost_anwenden(saved, d):
    """Die Felder aus `d` auf den gespeicherten Stand legen. Ungültige Werte
    bleiben wie bisher unbeachtet (das Deck sendet Zahlen aus Schiebern)."""
    if "enabled" in d:
        saved["enabled"] = bool(d["enabled"])
    if "min_gap_s" in d:
        try:
            saved["min_gap_s"] = max(10.0, float(d["min_gap_s"]))
        except (TypeError, ValueError):
            pass
    if "per_15min" in d:
        try:
            saved["per_15min"] = max(1, int(d["per_15min"]))
        except (TypeError, ValueError):
            pass
    if isinstance(d.get("kinds"), dict):
        kd = dict(saved.get("kinds") or {})
        for name, kc in d["kinds"].items():
            if name in ("highlight", "quiet") and isinstance(kc, dict):
                cur = dict(kd.get(name) or {})
                if "on" in kc:
                    cur["on"] = bool(kc["on"])
                if "cooldown_s" in kc:
                    try:
                        cur["cooldown_s"] = max(30.0, float(kc["cooldown_s"]))
                    except (TypeError, ValueError):
                        pass
                kd[name] = cur
        saved["kinds"] = kd
    return saved
