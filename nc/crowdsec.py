"""nc.crowdsec — v4.0-W18: CrowdSec-Sperrliste über die LAPI statt über cscli.

Warum: bisher las der Bot die Sperren mit `cscli`. Das braucht Root (die
LAPI-Zugangsdaten gehoeren root) und damit eine sudoers-Regel — die haeufigste
Fehlerquelle beim Einrichten. CrowdSec kennt dafuer einen eigenen Zugang:
einen BOUNCER-Schluessel (`cscli bouncers add azrael-dashboard`). Damit fragt
man die LAPI ueber HTTP ab — ohne Root, ohne sudo, mit einem Schluessel, den
man jederzeit widerrufen kann.

Die Rueckgabeform ist absichtlich IDENTISCH zur cscli-Auswertung
(jails/total_banned), damit Dashboard und Weltkarte unveraendert laufen.
"""

DECISIONS_PATH = "/v1/decisions"


def base_url(url=None, host="127.0.0.1", port=8083):
    """Normalisierte LAPI-Basis-URL (ohne Schraegstrich am Ende)."""
    u = (url or "").strip()
    if not u:
        u = f"http://{host}:{int(port)}"
    if "://" not in u:
        u = "http://" + u
    return u.rstrip("/")


def decisions_url(url=None, host="127.0.0.1", port=8083):
    return base_url(url, host, port) + DECISIONS_PATH


def headers(api_key):
    """Der Bouncer-Schluessel geht als X-Api-Key mit — so erwartet es die LAPI."""
    return {"X-Api-Key": (api_key or "").strip(),
            "Accept": "application/json",
            "User-Agent": "azrael-sentinel-bouncer/1.0"}


def parse_decisions(data):
    """LAPI-Antwort → gleiche Form wie die cscli-Auswertung:
       (jails, total_banned). Die LAPI liefert eine flache Liste oder null."""
    jails, total = {}, 0
    for dec in (data or []):
        if not isinstance(dec, dict):
            continue
        ip = (dec.get("value") or "").strip()
        if not ip:
            continue
        origin = (dec.get("origin") or "crowdsec").strip() or "crowdsec"
        e = jails.setdefault(origin, {"jail": origin, "ips": [], "banned_now": 0,
                                      "banned_total": None, "scenarios": {}})
        if ip not in e["ips"]:
            e["ips"].append(ip)
            e["banned_now"] += 1
            total += 1
        sc = (dec.get("scenario") or "").split("/")[-1]
        if sc:
            e["scenarios"][sc] = e["scenarios"].get(sc, 0) + 1
    return list(jails.values()), total


def explain_status(http_status):
    """(status, hint, fix) zu einem HTTP-Code — damit im Dashboard steht, WAS zu
       tun ist, statt einer nackten Zahl."""
    if http_status in (401, 403):
        return ("kein_zugang",
                "Der CrowdSec-Zugang wurde abgelehnt — Schluessel falsch oder widerrufen.",
                "sudo cscli bouncers add azrael-dashboard  → Schluessel in CROWDSEC_BOUNCER_KEY")
    if http_status == 404:
        return ("lapi_pfad",
                "LAPI erreichbar, aber /v1/decisions nicht gefunden — falscher Port/Dienst?",
                "sudo cscli lapi status")
    return (f"http_{http_status}",
            f"CrowdSec-LAPI antwortete mit HTTP {http_status}.",
            "sudo systemctl status crowdsec && sudo cscli lapi status")
