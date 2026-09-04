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
