"""nc.prueflage — wann wurde ein Tracking zuletzt geprüft, und mit welchem Ergebnis.

v4.2-W138. Der Betreiber am 05.11.: „bin ich mir nicht sicher ob überhaupt alle
User vernünftig abgefragt werden und korrekt online/offline angezeigt werden."

Die Frage war berechtigt, und sie war im Deck nicht zu beantworten. Der
Online-Punkt hängt an `trackings.last_live`, und das ändert sich nur bei einer
*sicheren* Antwort (live oder offline). Meldet der Resolver „unbekannt" — im
Audit W134 Befund 9 der Fall für die Mehrheit der Nutzer —, bleibt der alte
Wert stehen. Ein Nutzer, der vor drei Stunden offline ging und seitdem nur
„unbekannt" lieferte, stand weiter als LIVE da, ohne jeden Hinweis. Und ein
Tracking, das nie geprüft wurde, sah genauso aus wie eines, das gerade
„offline" geliefert hat.

Dieses Modul merkt sich je Tracking den letzten Prüfzeitpunkt, das Ergebnis
und den Zeitpunkt der letzten *sicheren* Antwort. Gemerkt wird im Prozess,
nicht in der Datenbank: nach einem Neustart ist „seit dem Start nicht
geprüft" genau die richtige Auskunft.
"""

import threading
import time

# Ab wann eine fehlende sichere Antwort zur Auskunft „unbekannt" wird. Ein
# einzelnes „unknown" zwischen zwei guten Antworten ist Alltag (ein Timeout)
# und soll den Punkt nicht flackern lassen; zehn Minuten ohne sichere Antwort
# sind es nicht mehr.
UNSICHER_AB_S = 600

# Ab wann ein aktives Tracking als „überfällig" gilt. Der längste reguläre
# Abstand ist idle mit 180 s, unter Last gedehnt bis etwa das Vierfache
# (nc/livefolge.last_dehnung) — 15 Minuten ohne Prüfung heißt, der Nutzer
# fällt durch die Abfrage, nicht, dass er bloß spät dran ist.
UEBERFAELLIG_AB_S = 900

SICHER = ("live", "offline")

_STAND = {}                 # tid -> {"status", "at", "sicher_at"}
_LOCK = threading.Lock()    # geschrieben vom Loop, gelesen von Flask-Threads


def merken(tid, status, jetzt=None):
    jetzt = time.time() if jetzt is None else jetzt
    with _LOCK:
        alt = _STAND.get(tid) or {}
        _STAND[tid] = {
            "status": status,
            "at": jetzt,
            "sicher_at": jetzt if status in SICHER else alt.get("sicher_at"),
        }


def vergessen(tid):
    with _LOCK:
        _STAND.pop(tid, None)


def lage(tid, last_live, paused=False, recording=False, jetzt=None):
    """Was das Deck für dieses Tracking zeigen soll.

    zustand: rec | live | offline | pause | unbekannt | ausstehend
    Dazu die Sekunden seit der letzten Prüfung und seit der letzten sicheren
    Antwort (None, wenn es keine gab) und `ueberfaellig`.
    """
    jetzt = time.time() if jetzt is None else jetzt
    with _LOCK:
        st = dict(_STAND.get(tid) or {})
    vor = (jetzt - st["at"]) if st.get("at") else None
    sicher_vor = (jetzt - st["sicher_at"]) if st.get("sicher_at") else None
    aus = {
        "zustand": None,
        "letztes": st.get("status"),
        "geprueft_vor_s": int(vor) if vor is not None else None,
        "sicher_vor_s": int(sicher_vor) if sicher_vor is not None else None,
        "ueberfaellig": bool(not paused and vor is not None
                             and vor > UEBERFAELLIG_AB_S),
    }
    if paused:
        aus["zustand"] = "pause"
    elif recording:
        # Eine laufende Aufnahme ist der stärkste Beleg — sie schlägt jede
        # Resolver-Antwort.
        aus["zustand"] = "rec"
    elif not st:
        aus["zustand"] = "ausstehend"
    elif st.get("status") not in SICHER and (
            sicher_vor is None or sicher_vor > UNSICHER_AB_S):
        aus["zustand"] = "unbekannt"
    else:
        aus["zustand"] = "live" if last_live else "offline"
    return aus
