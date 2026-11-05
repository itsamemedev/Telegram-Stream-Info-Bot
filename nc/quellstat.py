"""nc.quellstat — woher kam die Stream-Adresse, und wie oft kam keine (rein).

v4.2-W141. Der Betreiber am 05.11.: „7 User live keiner wird restreamt weil
angeblich keine flv oder hls streams empfangen werden können."

Der Satz enthaelt ein „angeblich", und das war berechtigt: die Antwort stand
nur in gedrosselten Logzeilen (`live-ohne-URL`, W103), und eine Drossel
zeigt naturgemaess nicht, wie OFT etwas passiert. Ob 7 von 7 Nutzern ohne
Adresse sind oder 1 von 7, und welcher Weg sie in den anderen Faellen
brachte, war nicht abzulesen. Das ist dieselbe Lage wie die 71 % aus W51 —
damals von Hand aus dem Log gezaehlt.

Hier wird je Ausgang gezaehlt, ueber ein gleitendes Fenster von einer
Stunde. Die Ausgaenge sind die des URL-Nachschlags:

    api      die Webcast-API trug die Adresse selbst
    html     der HTML-Weg lieferte sie nach
    ytdlp    yt-dlp lieferte sie nach
    keiner   „live", aber kein Weg fand eine Adresse

Kein Netz, keine Datenbank, kein Logger: `/healthz` liest es, und
`/healthz` misst nicht (Regel aus W97/W105).
"""

import collections
import threading
import time

FENSTER_S = 3600
AUSGAENGE = ("api", "html", "ytdlp", "keiner")
# Obergrenze je Ausgang: bei 200 Trackings und einem Poll alle 30 s sind das
# 24 000 Ereignisse je Stunde — die Schlange darf nicht unbegrenzt wachsen
# (dieselbe Haltung wie die Log-Schleuse aus W97: begrenzt statt OOM).
HOECHSTENS = 50000

_ZEITEN = {a: collections.deque(maxlen=HOECHSTENS) for a in AUSGAENGE}
_LOCK = threading.Lock()


def zaehlen(ausgang, jetzt=None):
    """Einen Ausgang zaehlen. Unbekannte Namen sind ein Programmierfehler."""
    if ausgang not in _ZEITEN:
        raise ValueError("unbekannter Ausgang %r" % (ausgang,))
    with _LOCK:
        _ZEITEN[ausgang].append(time.monotonic() if jetzt is None else jetzt)


def lage(jetzt=None):
    """{"api": n, …, "gesamt": n, "ohne_url_anteil": 0..1 oder None}.

    Der Anteil ist None, solange nichts gezaehlt ist — eine 0 laese sich wie
    „alles in Ordnung" (dieselbe Regel wie log_wartend = −1 in W97)."""
    jetzt = time.monotonic() if jetzt is None else jetzt
    grenze = jetzt - FENSTER_S
    aus = {}
    with _LOCK:
        for a, zeiten in _ZEITEN.items():
            while zeiten and zeiten[0] < grenze:
                zeiten.popleft()
            aus[a] = len(zeiten)
    gesamt = sum(aus.values())
    aus["gesamt"] = gesamt
    aus["ohne_url_anteil"] = round(aus["keiner"] / gesamt, 3) if gesamt else None
    return aus


def zuruecksetzen():
    with _LOCK:
        for zeiten in _ZEITEN.values():
            zeiten.clear()
