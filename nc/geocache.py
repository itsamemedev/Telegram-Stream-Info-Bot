"""nc.geocache — v4.1-W25: die IP-Geodaten, mit EINEM Schreibweg.

════════════════════════════════════════════════════════════════════════
WARUM DIESES MODUL — UND EIN BEFUND
════════════════════════════════════════════════════════════════════════
Im Monolithen lagen Cache, Sperre und Obergrenze offen, dazu ein Helfer
`_proxy_geo_cache_put`, der die Obergrenze durchsetzt. Zwei Aufrufer
benutzten ihn — und **einer nicht**: die Geo-Auflösung der Abwehr-Karte
schrieb `_PROXY_GEO_CACHE[ip] = g` direkt unter der Sperre und ging damit an
der Verdrängung vorbei.

Folge: bei einer Angriffswelle mit vielen verschiedenen Adressen wuchs der
Cache unbegrenzt. Kein Fehler, keine Logzeile — nur Speicher, der nicht mehr
zurückkommt. Genau die Sorte Befund, die man nur beim Verschieben findet.

Deshalb hat dieses Modul **einen** Schreibweg: `put()`. Wer eintragen will,
kommt an der Obergrenze nicht vorbei, weil es keinen zweiten Weg gibt. Der
Cache selbst ist absichtlich nicht Teil der öffentlichen Fläche.

FIFO-Verdrängung ist hier richtig: die Geolage einer Adresse ist stabil, ein
verdrängter Eintrag wird beim nächsten Mal einfach neu geholt.
"""

import threading

# Obergrenze. Bei 5000 Einträgen à rund 200 Byte sind das etwa ein Megabyte —
# die Grenze schützt vor der Angriffswelle, nicht vor dem Normalbetrieb.
MAX = 5000

_CACHE = {}          # ip -> {lat, lon, country, cc, city, isp}
_LOCK = threading.Lock()


def get(ip):
    """Der Eintrag zu einer Adresse, oder None."""
    with _LOCK:
        return _CACHE.get(ip)


def put(ip, geo):
    """Eintragen. EINZIGER Schreibweg — siehe Modul-Kopf.

    Ein vorhandener Eintrag wandert ans Ende (Pythons dict hält die
    Einfügereihenfolge), damit die Verdrängung den ältesten trifft und nicht
    den zuletzt benutzten.
    """
    if not ip:
        return
    with _LOCK:
        if ip in _CACHE:
            _CACHE.pop(ip)
        _CACHE[ip] = geo
        while len(_CACHE) > MAX:
            _CACHE.pop(next(iter(_CACHE)), None)


def groesse() -> int:
    """Wie viele Adressen liegen im Cache? Für die Diagnose."""
    with _LOCK:
        return len(_CACHE)


def leeren():
    """Nur für Tests und den Betreiber — im Betrieb verdrängt put() selbst."""
    with _LOCK:
        _CACHE.clear()


# ── v5.8-W199: die Anreicherung der Proxy-Liste, aus bot.py geloest ──────────
#
# Woertlich uebernommen (F79, B57), mit einer Korrektur: die Ruhezeit gegen
# ip-api.com wurde nur bei ERFOLG gestempelt. War der Dienst gestoert, lief
# jede Pool-Auffrischung erneut in den 10-Sekunden-Timeout — dieselbe Klasse
# wie der yt-dlp-Nachschlag in W102 („der Zeitstempel steht VOR dem Aufruf").

import json as _json            # noqa: E402
import logging as _logging      # noqa: E402
import time as _time            # noqa: E402

_log = _logging.getLogger("TikTokBot")
RUHE_S = 5.0                    # hoechstens ein Stapel alle 5 s (45 Anfragen/min erlaubt)
_LETZTER_ABRUF = [0.0]          # monotone Uhr der letzten ip-api-Anfrage
API_URL = "http://ip-api.com/batch"


def _abrufen(ips, timeout=10):
    """Die Stapelanfrage an ip-api.com. Eigene Funktion, damit ein Vertrag sie
    ersetzen kann, ohne ins Netz zu gehen."""
    import urllib.request
    body = _json.dumps([{"query": ip, "fields": "status,lat,lon,country,city,isp,query"}
                        for ip in ips]).encode()
    req = urllib.request.Request(API_URL, data=body,
                                 headers={"Content-Type": "application/json",
                                          "User-Agent": "TKT-OPS/1.0"})
    with urllib.request.urlopen(req, timeout=timeout) as resp:      # noqa: S310 (feste URL)
        return _json.loads(resp.read().decode("utf-8", errors="ignore"))


def anreichern(proxies):
    """Fuegt jedem Proxy-Dict {lat, lon, country, city, isp} hinzu.
       Cache hits = sofort, Cache misses = ein Batch-Call zu ip-api.com.
       Falls ip-api down: kein crash, fehlt halt das geo-Feld."""
    # Phase 1: cache hits direkt anwenden, misses sammeln
    unknown = []
    for p in proxies:
        ip = (p.get("url", "").split(":") or [""])[0]
        if not ip:
            continue
        cached = get(ip)
        if cached:
            p.update(cached)
        else:
            unknown.append((p, ip))

    if not unknown:
        return proxies

    # Phase 2: rate-limit gegen ip-api.com (45 req/min — wir machen max 1 batch
    # alle 5s damit pool-refresh-storms uns nicht bannen)
    now = _time.monotonic()
    if now - _LETZTER_ABRUF[0] < RUHE_S:
        _log.info("GeoIP rate-limit: skip enrichment (%d unknown remain)", len(unknown))
        return proxies
    # v5.8-W199: VOR dem Aufruf stempeln — auch ein Fehlschlag haelt die Ruhe ein.
    _LETZTER_ABRUF[0] = now

    # Phase 3: batch fetch (max 100 IPs pro request laut ip-api docs)
    batch_ips = [ip for _, ip in unknown[:100]]
    try:
        results = _abrufen(batch_ips)
        # Index by IP (results are in request order but safer to map by query field)
        ip_to_geo = {}
        for r in results:
            if isinstance(r, dict) and r.get("status") == "success":
                ip_to_geo[r.get("query", "")] = {
                    "lat": r.get("lat"),
                    "lon": r.get("lon"),
                    "country": r.get("country", ""),
                    "city": r.get("city", ""),
                    "isp": (r.get("isp", "") or "")[:50],
                }
        # Apply + cache
        for proxy_dict, ip in unknown:
            geo = ip_to_geo.get(ip)
            if geo:
                proxy_dict.update(geo)
                put(ip, geo)   # B57: bounded cache write
        _log.info("GeoIP enriched %d/%d proxies", len(ip_to_geo), len(batch_ips))
    except Exception as e:
        _log.warning("GeoIP batch fetch failed: %s", e)
    return proxies
