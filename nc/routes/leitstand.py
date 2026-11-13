"""nc.routes.leitstand — v5.10-W207: GET /api/leitstand für die Übersicht.

Ein Aufruf für alle neun Tab-Tafeln: die Übersicht fragt alle acht Sekunden,
und neun Einzelrouten hiessen neun Datenbank- und Brain-Zugriffe je Takt und
je offenem Tab. Welche Lage eine Tafel hat, entscheidet nc/leitstand.py.

Jede Quelle ist einzeln abgesichert und hat ihre eigene Gültigkeit: die
Lieferkette ändert sich im Sekundentakt, die Einstellungen kaum. Eine Quelle,
die nicht antwortet, kostet nur ihre Tafel — sie steht als „unbekannt" da,
nie als „ok" (W99) — und geht gedrosselt ins Log (nc.meldetakt).

Die Rohdaten kommen aus denselben Funktionen, die die Tabs selbst lesen
(Lagebild, Restream-Gesundheit, Tageszählung, Trefferquote, KI-Wahl, MCP):
eine zweite Abfrage für dieselbe Zahl zählt früher oder später anders.
"""

import logging
import os
import threading
import time

from flask import Blueprint, jsonify

from nc import brainstate as _nc_brainstate
from nc import community as _nc_community
from nc import discordstate as _nc_discordstate
from nc import einstellungen as _nc_einst
from nc import eventquery as _nc_eventquery
from nc import highlights as _nc_highlights
from nc import kiwahl as _nc_kiwahl
from nc import lagebild as _nc_lagebild
from nc import leitstand as _nc_leitstand
from nc import mcpdienste as _nc_mcp
from nc import meldetakt as _takt
from nc import stats as _nc_stats
from nc import systemprobe as _nc_probe
from nc.dbwrap import db_conn
from nc.routes import lagebild as _rlagebild
from nc.routes import restream as _rrestream

bp = Blueprint("leitstand", __name__)
log = logging.getLogger("TikTokBot")


def _ausfall(quelle, e):
    laut, weg = _takt.melden("leitstand", quelle + ":" + type(e).__name__, time.time())
    if laut:
        log.warning("Leitstand: Quelle %s nicht lesbar (%s: %s) — ihre Tafel steht "
                    "als unbekannt.%s", quelle, type(e).__name__, e, _takt.zusatz(weg))


# ─── die Quellen ─────────────────────────────────────────────────────────

def _zaehler():
    # Dieselben Zaehler wie die Kopfkacheln (/api/stats, schlanker Weg):
    # „Live jetzt" oben und auf der Live-Wand sollen dieselbe Zahl zeigen.
    with db_conn() as conn:
        t = conn.execute("SELECT COUNT(*) FROM trackings").fetchone()[0]
        live = conn.execute("SELECT COUNT(*) FROM trackings WHERE last_live=1").fetchone()[0]
    return {"trackings": int(t or 0), "live": int(live or 0)}


def _system():
    snap = _nc_probe.cpu_load_snapshot()
    pct, st = _nc_probe.disk_pct()
    gesamt, frei = snap.get("mem_total_gb") or 0, snap.get("mem_available_gb") or 0
    return {"last": {k: snap.get(k) for k in ("avg", "per_core", "state") if k in snap},
            "kerne": os.cpu_count() or 1,
            "speicher_prozent": round(100.0 * (gesamt - frei) / gesamt, 1) if gesamt else None,
            "swap_pct": snap.get("swap_pct"),
            # disk_pct liefert (0, None), wenn es nicht messen konnte — dann
            # ist die Platte unbekannt, nicht leer.
            "platte_prozent": pct if st is not None else None,
            "platte_frei_gb": round(st.free / 1024 ** 3, 1) if st is not None else None,
            "fresser": [{"name": x.get("comm"), "cpu": x.get("cpu"), "rss_mb": x.get("rss_mb")}
                        for x in (snap.get("top") or [])[:3]]}


def _ki():
    lage = dict(_nc_kiwahl.deck_lage())
    lage["bruecke_ok"] = bool(_nc_brainstate.BRIDGE.get("ok"))
    try:
        from brain import get_brain
        lage["llm"] = dict(get_brain().llm.stats().get("slot") or {})
    except Exception as e:
        # Die Plaetze sind ein Teil der Tafel, nicht die Tafel: ohne sie steht
        # die KI-Wahl trotzdem da. Laut, gedrosselt.
        _ausfall("ki-plaetze", e)
        lage["llm"] = {}
    return lage


def _community():
    out = {"discord_verbunden": False,
           # Ob ein Discord-Bot eingerichtet ist — als Ja/Nein, nie der Wert.
           "discord_konfiguriert": bool(os.getenv("DISCORD_BOT_TOKEN", "").strip()),
           "server": None, "mitglieder": None}
    c = _nc_discordstate.CLIENT["obj"]
    if c is not None and c.is_ready():
        out["discord_verbunden"] = True
        if c.guilds:
            out["server"] = c.guilds[0].name
            out["mitglieder"] = c.guilds[0].member_count
    st = _nc_community.seen_stats()
    raten = _nc_highlights.chat_raten()
    out.update(bekannt=st.get("known"), stammgaeste=st.get("regulars"),
               chat_rate=raten["rate"], chat_basis=raten["basis"])
    return out


def _insights():
    q = _nc_stats.trefferquote()
    return {"quote": q["catch_rate"], "versuche": q["total_attempts"],
            "erfolgreich": q["successful"], "tage": _nc_stats.aufnahmen_je_tag(14)}


def _einstellungen():
    u = _nc_einst.uebersicht()
    return {"zahl": dict(u.get("zahl") or {}), "geschuetzt": u.get("geschuetzt"),
            "neustart": list(u.get("neustart") or []), "backend": u.get("backend")}


def _ereignisse():
    sql, params = _nc_eventquery.build_query(_nc_leitstand.MAX_EREIGNISSE, None, None)
    with db_conn() as conn:
        rows = conn.execute(sql, params).fetchall()
    return [{"ts": r["ts"], "kind": r["kind"], "severity": r["severity"],
             "summary": r["summary"]} for r in rows]


# (Name, Funktion, Gueltigkeit in s). Die Ereignisse und die Lieferkette
# altern schnell; Einstellungen, MCP und die 14-Tage-Zaehlung kaum.
QUELLEN = (
    ("lagebild", _rlagebild.daten, 6),
    ("restream", _rrestream.gesundheit, 6),
    ("zaehler", _zaehler, 8),
    ("ereignisse", _ereignisse, 5),
    ("system", _system, 8),
    ("ki", _ki, 10),
    ("community", _community, 20),
    ("insights", _insights, 120),
    ("einstellungen", _einstellungen, 60),
    ("mcp", _nc_mcp.lage, 60),
)

# Eine gescheiterte Quelle wird nicht bei jedem Abruf neu gefragt, aber
# auch nicht lange: nach so vielen Sekunden der naechste Versuch.
FEHLER_RUHE_S = 5.0

_CACHE = {}           # name -> (gueltig_bis, daten, gelesen)
_SPERRE = threading.Lock()


def _lesen(name, fn, ttl):
    with _SPERRE:
        hat = _CACHE.get(name)
    if hat and hat[0] > time.monotonic():
        return hat[1], hat[2]
    try:
        daten, gelesen = fn(), True
    except Exception as e:
        daten, gelesen = None, False
        _ausfall(name, e)
    # Die Uhr beim SCHREIBEN (W103): eine zaehe Quelle waere sonst schon
    # abgelaufen, wenn sie eingetragen wird.
    frist = ttl if gelesen else min(ttl, FEHLER_RUHE_S)
    with _SPERRE:
        _CACHE[name] = (time.monotonic() + frist, daten, gelesen)
    return daten, gelesen


@bp.route("/api/leitstand")
def api_leitstand():
    roh, gelesen = {}, {}
    for name, fn, ttl in QUELLEN:
        daten, ok = _lesen(name, fn, ttl)
        gelesen[name] = ok
        if ok:
            roh[name] = daten
    return jsonify(_nc_leitstand.bauen(roh, gelesen, time.time(),
                                       ort_von_name=_nc_lagebild.ORT))
