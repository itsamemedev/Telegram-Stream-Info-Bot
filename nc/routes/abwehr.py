"""nc.routes.abwehr — was den Server angreift und wer gesperrt ist.

Welle 3 der Zerlegung (siehe docs/MODULARISIERUNG.md). Pfade stehen woertlich
in den Dekoratoren (kein url_prefix); was der Monolith weiterhin stellen muss,
kommt ueber nc.ctx statt ueber einen Import aus bot.py.

v4.1-W25: Vier Routen — Ueberblick, CrowdSec-Diagnose, Sperrliste und die
Angriffsversuche. Sie ZEIGEN nur; keine davon sperrt oder entsperrt etwas.

**Null neue Kontext-Eintraege.** Vorweg geloest:

* **nc/defensecfg.py** — Serverstandort und die vier LAPI-Angaben. Der
  Bouncer-Schluessel kommt nur aus `bouncer_key()`; die Routen benutzen
  ausschliesslich `bouncer_gesetzt()` (bool).
* **nc/geocache.py** — der Adress-Cache mit EINEM Schreibweg.
* **nc/geoip.py** — die Stapelabfrage bei ip-api.

Was nur der laufende Server kann — cscli aufrufen, das Journal lesen —
kommt als Haken herein.
"""

from flask import Blueprint, jsonify

from nc import crowdsec as _nc_crowdsec
from nc import fehlertext as _nc_fehlertext
from nc import defensecfg as _nc_dcfg
from nc import geoip as _nc_geoip
from nc import i18n as _nc_i18n

from nc import ctx as _ctx

bp = Blueprint("abwehr", __name__)


def _fehler_text(e, wo=""):
    """v4.1-W30: der Wortlaut geht ins Log, nach aussen die gesaeuberte
       Fassung — ohne Pfade, ohne Zugangsdaten, gekuerzt. Siehe
       nc/fehlertext.py, dort steht auch, warum nicht einfach "interner
       Fehler"."""
    return _nc_fehlertext.nach_aussen(e, wo)


def _c():
    """Laufzeitkontext. Aufruf statt Modul-Konstante — der Kontext wird erst
       beim Bot-Start gefuellt."""
    return _ctx.get()


def _t(s):
    """v4.1-W25: an der Quelle uebersetzen. Diese Texte erreichen das DOM
       meist verkettet ("Fehler: " + error) — ein Katalogeintrag fuer den
       blossen Text traefe dort nie."""
    return _nc_i18n.t(s)


def _geo(ips):
    """Adressen aufloesen und den letzten Fehlgrund festhalten. Ohne den
       konnte das Panel "nichts gefunden" nicht von "ip-api antwortet nicht"
       unterscheiden (B138)."""
    return _nc_geoip.lookup(ips, fehler_setzen=_nc_dcfg.geo_fehler_setzen)


# Was nur der laufende Server kann: cscli aufrufen (braucht Root, ausser mit
# Bouncer-Schluessel) und das Journal nach fehlgeschlagenen Anmeldungen
# durchsehen. Der Bot traegt beim Start ein, die Routen rufen auf. Sichtbare
# Kopplung statt eines Kontext-Slots — dieselbe Begruendung wie in
# nc/restreamstate.py und nc/routes/wartung.py.
HAKEN = {"sperrliste": {"fn": None},   # () -> dict (jails, total_banned, ...)
         "angriffe": {"fn": None}}     # (limit) -> dict (attacks, total, ...)


def _haken(name):
    """Der eingetragene Haken. None, wenn der Bot ihn nie gesetzt hat — die
       Aufrufer pruefen das und sagen es, statt Leere als Ergebnis zu melden."""
    return HAKEN[name]["fn"]


def _nicht_bereit():
    """Antwort, wenn der Bot die Haken nie eingetragen hat. Ohne sie meldete
       die Ansicht 0 Sperren und 0 Angriffe — also 'alles ruhig', obwohl in
       Wahrheit gar nicht nachgesehen wurde. Das ist bei einer
       SICHERHEITSANZEIGE die gefaehrlichste aller Antworten."""
    return jsonify(ok=False, status="nicht_bereit",
                   error=_t("Abwehr nicht bereit — Bot laeuft nicht"),
                   hint=_t("Diese Ansicht braucht den laufenden Bot: sie fragt "
                           "CrowdSec ab und liest das Journal."),
                   jails=[], total_banned=0, attacks=[], total=0), 503


@bp.route("/api/defense/overview")
def api_defense_overview():
    sperrliste, angriffe = _haken("sperrliste"), _haken("angriffe")
    if not (sperrliste and angriffe):
        return _nicht_bereit()
    try:
        f2b = sperrliste()
        atk = angriffe(limit=250)
        top_ips = [a["ip"] for a in atk.get("attacks", [])[:60]]
        geo = _geo(top_ips) if top_ips else {}
        by_country = {}
        for a in atk.get("attacks", []):
            g = geo.get(a["ip"])
            if g and g.get("country"):
                by_country[g["country"]] = by_country.get(g["country"], 0) + a["count"]
        top_countries = sorted(by_country.items(), key=lambda x: x[1], reverse=True)[:8]
        # B138: status + fix mitliefern. Ohne sie kann das Panel "nichts
        # gefunden" nicht von "darf nicht nachsehen" unterscheiden.
        return jsonify(ok=True, banned=f2b.get("total_banned", 0), f2b_ok=f2b.get("ok"),
                       f2b_status=f2b.get("status"),
                       f2b_hint=(None if f2b.get("ok") else f2b.get("hint")),
                       f2b_fix=(None if f2b.get("ok") else f2b.get("fix")),
                       attacks_total=atk.get("total", 0), unique_ips=atk.get("unique_ips", 0),
                       attacks_ok=atk.get("ok"), attacks_status=atk.get("status"),
                       attacks_source=atk.get("source"),
                       attacks_hint=(None if atk.get("ok") else atk.get("hint")),
                       attacks_fix=(None if atk.get("ok") else atk.get("fix")),
                       geo_error=(_nc_dcfg.geo_fehler() or None),
                       top_countries=[{"country": c, "hits": n} for c, n in top_countries],
                       server={"lat": _nc_dcfg.server_lat(), "lon": _nc_dcfg.server_lon()})
    except Exception as e:
        return jsonify(ok=False, error=_fehler_text(e, "api_defense_overview")), 500


@bp.route("/api/defense/crowdsec")
def api_defense_crowdsec():
    """v4.0-W23: Verbindungs-Diagnose zu CrowdSec — genau der Weg, den der Bot
       geht (LAPI via Bouncer-Schluessel, sonst cscli). Zeigt Modus, die exakt
       abgefragte LAPI-URL, ob ein Schluessel gesetzt ist, sowie ok/hint/fix.
       Der 'Verbindung testen'-Knopf im Dashboard ruft genau das auf."""
    sperrliste = _haken("sperrliste")
    if not sperrliste:
        return _nicht_bereit()
    try:
        st = dict(sperrliste() or {})
        st.setdefault("ok", False)
        st["mode"] = "lapi" if _nc_dcfg.bouncer_gesetzt() else "cscli"
        st["lapi_url"] = _nc_crowdsec.base_url(_nc_dcfg.lapi_url(), _nc_dcfg.lapi_host(),
                                               _nc_dcfg.lapi_port())
        st["bouncer_key_set"] = bool(_nc_dcfg.bouncer_gesetzt())
        return jsonify(st)
    except Exception as e:
        return jsonify(ok=False, error=_fehler_text(e, "api_defense_crowdsec")), 500


@bp.route("/api/defense/fail2ban")
def api_defense_fail2ban():
    sperrliste = _haken("sperrliste")
    if not sperrliste:
        return _nicht_bereit()
    try:
        f2b = sperrliste()
        all_ips = []
        for j in f2b.get("jails", []):
            all_ips += j.get("ips", [])
        geo = _geo(all_ips[:100]) if all_ips else {}
        for j in f2b.get("jails", []):
            j["ip_geo"] = [dict(ip=ip, **(geo.get(ip) or {})) for ip in j.get("ips", [])]
        return jsonify(**f2b)
    except Exception as e:
        return jsonify(ok=False, error=_fehler_text(e, "api_defense_fail2ban")), 500


@bp.route("/api/defense/attacks")
def api_defense_attacks():
    angriffe = _haken("angriffe")
    if not angriffe:
        return _nicht_bereit()
    try:
        atk = angriffe(limit=300)
        ips = [a["ip"] for a in atk.get("attacks", [])]
        geo = _geo(ips[:100]) if ips else {}
        for a in atk.get("attacks", []):
            g = geo.get(a["ip"])
            if g:
                a.update(lat=g.get("lat"), lon=g.get("lon"), country=g.get("country"),
                         cc=g.get("cc"), city=g.get("city"))
        atk["server"] = {"lat": _nc_dcfg.server_lat(), "lon": _nc_dcfg.server_lon()}
        return jsonify(**atk)
    except Exception as e:
        return jsonify(ok=False, error=_fehler_text(e, "api_defense_attacks")), 500
