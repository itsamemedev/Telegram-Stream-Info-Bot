"""nc.geoip — v4.1-W25: IP-Adressen geolokalisieren (ip-api.com, Stapelabfrage).

Aus dem Monolithen geloest, weil die Abwehr-Ansicht sie braucht und ein Modul
sie besser haelt: der Cache liegt in nc/geocache.py und hat dort genau EINEN
Schreibweg.

**Das war hier ein echter Befund, kein Aufraeumen.** Vorher schrieb diese
Funktion `_PROXY_GEO_CACHE[ip] = g` direkt unter der Sperre und ging damit an
`_proxy_geo_cache_put` und dessen Obergrenze von 5000 Eintraegen vorbei. Bei
einer Angriffswelle mit vielen verschiedenen Adressen wuchs der Cache
unbegrenzt — kein Fehler, keine Logzeile, nur Speicher, der nicht
zurueckkommt. Jetzt gibt es keinen zweiten Schreibweg mehr, an dem man
vorbeikommen koennte.

Private und lokale Adressen werden uebersprungen: ip-api kennt sie nicht, und
sie kosten nur Kontingent (45 Anfragen pro Minute).
"""

import ipaddress
import json
import logging
import urllib.request

from nc import geocache as _cache

log = logging.getLogger("TikTokBot")


def ist_privat(ip) -> bool:
    """Private, lokale, Link-Local- und reservierte Adressen. Der Textvergleich
       im Rueckfall faengt den Fall ab, dass ip_address() eine kaputte Eingabe
       ablehnt — dann lieber ueberspringen als ip-api damit belasten."""
    try:
        a = ipaddress.ip_address(ip)
        return a.is_private or a.is_loopback or a.is_link_local or a.is_reserved
    except Exception:
        return str(ip).startswith(("10.", "192.168.", "127.", "169.254.",
                                   "172.1", "172.2", "172.3"))


def lookup(ips, fehler_setzen=None):
    """Geolokalisiert Adressen für die Abwehr-Karte. -> {ip: {lat, lon,
       country, cc, city}}. Private und lokale Adressen fallen still raus.

       `fehler_setzen` ist optional und nimmt den letzten Fehlgrund entgegen
       (nc.defensecfg.geo_fehler_setzen). Ohne ihn laeuft die Auflösung
       genauso, sie kann dem Deck nur nicht erklären, warum die Karte leer
       blieb — und genau das war B138."""
    if fehler_setzen:
        fehler_setzen("")
    out, unknown = {}, []
    for ip in {i for i in ips if i}:
        if ist_privat(ip):
            continue
        c = _cache.get(ip)
        if c and c.get("lat") is not None:
            out[ip] = c
        else:
            unknown.append(ip)
    if unknown:
        pub = unknown[:100]
        try:
            body = json.dumps([{"query": ip,
                                "fields": "status,lat,lon,country,countryCode,city,query"}
                               for ip in pub]).encode()
            req = urllib.request.Request("http://ip-api.com/batch", data=body,
                                         headers={"Content-Type": "application/json",
                                                  "User-Agent": "nc-defense/1"})
            with urllib.request.urlopen(req, timeout=8) as r:
                arr = json.loads(r.read().decode())
            for item in arr or []:
                if item.get("status") == "success":
                    ip = item.get("query")
                    g = {"lat": item.get("lat"), "lon": item.get("lon"),
                         "country": item.get("country"), "cc": item.get("countryCode"),
                         "city": item.get("city")}
                    # EIN Schreibweg — put() setzt die Obergrenze durch.
                    # Vorher stand hier ein Direktzugriff, der daran vorbeiging
                    # (siehe Modul-Kopf).
                    _cache.put(ip, g)
                    out[ip] = g
        except Exception as e:
            # B138: war log.debug — in einem ERROR-Log unsichtbar. Fiel ip-api
            # aus (Rate-Limit 45/min oder ausgehender Port 80 zu), blieben
            # TOP-LÄNDER und Weltkarte leer und niemand erfuhr warum.
            if fehler_setzen:
                fehler_setzen(str(e))
            log.warning("Abwehr: Geo-Auflösung (ip-api) fehlgeschlagen: %s", e)
    return out
