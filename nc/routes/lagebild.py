"""nc.routes.lagebild — v4.2-W112: GET /api/lagebild fuer die lebende Übersicht.

Ein Aufruf statt vier: die Übersicht fragt alle acht Sekunden, und vier
Einzelrouten hiessen vier Datenbank- und Brain-Zugriffe je Takt und je
offenem Tab. Die Entscheidung, was gezeichnet wird, steht in nc/lagebild.py.

Jede Quelle ist einzeln abgesichert und meldet ihren Ausfall in `quellen` —
ein Brain, das nicht antwortet, darf die Ziele nicht mitreissen, und ein
leerer Waechter-Ring muss sich von einem nicht geladenen unterscheiden
lassen (W99). Der Ausfall geht ausserdem gedrosselt ins Log: eine Anzeige,
die still „aus" zeigt, ist dieselbe Blindheit wie ein stiller except.
"""

import logging
import time

from flask import Blueprint, jsonify

from nc import lagebild as _nc_lagebild
from nc import meldetakt as _takt
from nc import restreamstate as _nc_rsstate
from nc.trackingdb import get_all_active_trackings

bp = Blueprint("lagebild", __name__)
log = logging.getLogger("TikTokBot")


def _ausfall(quelle, e):
    laut, weg = _takt.melden("lagebild", quelle + ":" + type(e).__name__,
                             time.time())
    if laut:
        log.warning("Lagebild: Quelle %s nicht lesbar (%s: %s) — die "
                    "Übersicht zeigt sie als nicht geladen.%s",
                    quelle, type(e).__name__, e, _takt.zusatz(weg))


def _trackings():
    return [{"username": t["username"], "last_live": t["last_live"],
             "recording": t["recording"],
             "paused": t["paused"] if "paused" in t.keys() else 0}
            for t in get_all_active_trackings(include_paused=True)]


def _restreams():
    m = _nc_rsstate.mgr()
    # Kein Manager ist keine Stoerung (Restream abgeschaltet) — eine leere
    # Liste, die `quellen` als gelesen fuehrt.
    stand = (m.status() if m is not None else None) or {}
    aktiv = _nc_rsstate.ACTIVE_ALL or {}
    out = []
    for rid, st in stand.items():
        e = dict(st or {})
        e["user"] = (aktiv.get(rid) or {}).get("user", "")
        out.append(e)
    return out


def _agenten():
    from brain import get_brain
    b = get_brain()
    zustand = {e["key"]: e for e in b.state.query("agent")}
    return b.agents.status(), zustand


@bp.route("/api/lagebild")
def api_lagebild():
    quellen = {}
    trackings, restreams, agenten, zustand = [], [], [], {}
    try:
        trackings = _trackings()
        quellen["trackings"] = True
    except Exception as e:
        quellen["trackings"] = False
        _ausfall("trackings", e)
    try:
        restreams = _restreams()
        quellen["restream"] = True
    except Exception as e:
        quellen["restream"] = False
        _ausfall("restream", e)
    try:
        agenten, zustand = _agenten()
        quellen["brain"] = True
    except Exception as e:
        quellen["brain"] = False
        _ausfall("brain", e)
    return jsonify(_nc_lagebild.bauen(trackings, restreams, agenten, zustand,
                                      time.time(), quellen=quellen))
