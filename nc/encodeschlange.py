"""nc.encodeschlange — v4.2-W174: Hintergrund-Kodierungen nacheinander, nicht gleichzeitig.

Gemeldet am 11.11.: „Dann gibt's wieder Aufnahmen mit Pixelsalat und/oder
fehlendem Ton. Wenn er die Videos nicht alle gleichzeitig encoden kann, sollte
er eine Warteschlange einpflegen, dass er die Dinger nach und nach abarbeitet."

Die Kette steht seit W108 in nc/lastvorsorge.py: liest ein Live-Prozess seine
Quelle zu langsam, verwirft das CDN Pakete, und das Bild zerfaellt bis zum
naechsten Keyframe; der Ton reisst mit. Die Aufnahme selbst ist `-c copy` und
kostet fast nichts — langsam wird sie, wenn um sie herum libx264-Durchgaenge
die Kerne belegen. Davon gab es bis hier sechs, und jeder startete sofort,
egal wie viele schon liefen:

    Clip-Schnitt            je Hype-Moment, mehrere pro Stream
    Meme-Zusammenschnitt    nach jedem Stream
    Chat einbrennen         die ganze Aufnahme, Minuten bis Stunden
    Discord verkleinern     Clips und Link-Videos ueber dem Limit
    Link-Video (W169)       ueber dasselbe Verkleinern
    Zerlegen-Rueckfall      Neu-Kodierung, wenn ein Teil zu gross bleibt

`nice` (W44) laesst sie hinter Aufnahme und Restream zuruecktreten — aber nur
anteilig: sechs Prozesse auf nice 12 bekommen zusammen trotzdem einen
spuerbaren Teil der Maschine, und ihr Speicher- und Platten-Durchsatz kennt
gar keine Prioritaet.

Hier gilt deshalb:

* hoechstens ENCODE_PARALLEL (Vorgabe 1) Kodierungen gleichzeitig;
* eine Kodierung beginnt erst, wenn das Load-Mittel unter ENCODE_LAST_ANTEIL
  (Vorgabe 0,7) der Kerne liegt — Aufnahme und Restream haben Vorrang;
* nach ENCODE_WARTEN_MAX_S (Vorgabe 1800) laeuft sie trotzdem, damit eine
  dauerhaft volle Maschine nicht jeden Clip fuer immer zurueckhaelt (ein
  verhungerter Job ist dieselbe stille Lage wie ein verlorener);
* was wartet und was laeuft, steht in lage() — fuer /healthz und das Deck.

Nichts geht verloren: ein Job wartet, statt abgewiesen zu werden.

Bot-frei. Ein Tor fuer Threads und den Event-Loop zugleich (das Einbrennen
laeuft in einem Arbeiter-Thread, Clips im Loop).
"""

import asyncio
import contextlib
import itertools
import logging
import os
import threading
import time

log = logging.getLogger("TikTokBot")

_SPERRE = threading.Lock()
_ZUSTAND = {"laeuft": {}, "wartet": {}, "erledigt": 0, "zwangsstart": 0}
_ID = itertools.count(1)
PRUEF_S = 2.0          # so oft schaut ein Wartender nach


def parallel() -> int:
    try:
        return max(1, int(os.getenv("ENCODE_PARALLEL", "1") or 1))
    except ValueError:
        log.error("ENCODE_PARALLEL=%r ist keine Zahl — es gilt 1.", os.getenv("ENCODE_PARALLEL"))
        return 1


def _zahl(name, vorgabe):
    try:
        return float(os.getenv(name, str(vorgabe)) or vorgabe)
    except ValueError:
        log.error("%s=%r ist keine Zahl — es gilt %s.", name, os.getenv(name), vorgabe)
        return float(vorgabe)


def last_frei(load1=None, kerne=None) -> bool:
    """Ist die Maschine frei genug fuer eine Hintergrund-Kodierung?"""
    if load1 is None:
        try:
            load1 = os.getloadavg()[0]
        except OSError:
            return True        # kein Load-Mittel (z. B. Windows): nur die Zahl begrenzt
    kerne = kerne or os.cpu_count() or 1
    return load1 < kerne * _zahl("ENCODE_LAST_ANTEIL", 0.7)


def _darf_starten(seit, jetzt):
    """(darf, zwang) — zwang heisst: nur wegen Wartezeit-Obergrenze."""
    if len(_ZUSTAND["laeuft"]) >= parallel():
        return False, False
    if last_frei():
        return True, False
    if jetzt - seit >= _zahl("ENCODE_WARTEN_MAX_S", 1800):
        return True, True
    return False, False


def _anmelden(art, wer):
    jid = next(_ID)
    with _SPERRE:
        _ZUSTAND["wartet"][jid] = {"art": art, "wer": wer, "seit": time.time()}
        vor = len(_ZUSTAND["wartet"]) - 1 + len(_ZUSTAND["laeuft"])
    if vor:
        log.info("Kodierung %s%s wartet — %d vor ihr (Aufnahme und Restream haben Vorrang).",
                 art, (" @" + wer) if wer else "", vor)
    return jid, time.monotonic()


def _versuchen(jid, seit):
    """Unter der Sperre: Platz nehmen, wenn er frei ist. True = laeuft jetzt.

    Reihenfolge: nur der aelteste Wartende darf nehmen. Ohne das gewinnt bei
    jedem freien Platz zufaellig, wer gerade nachsieht, und ein Job kann
    beliebig oft ueberholt werden."""
    with _SPERRE:
        if min(_ZUSTAND["wartet"]) != jid:
            return False
        darf, zwang = _darf_starten(seit, time.monotonic())
        if not darf:
            return False
        eintrag = _ZUSTAND["wartet"].pop(jid)
        eintrag["start"] = time.time()
        _ZUSTAND["laeuft"][jid] = eintrag
        if zwang:
            _ZUSTAND["zwangsstart"] += 1
    if zwang:
        log.warning("Kodierung %s startet trotz hoher Last — sie wartete schon %.0f min. "
                    "Abhilfe: weniger gleichzeitige Restreams/Aufnahmen oder "
                    "ENCODE_WARTEN_MAX_S hoeher.", eintrag["art"],
                    (time.monotonic() - seit) / 60)
    return True


def _abmelden(jid):
    with _SPERRE:
        _ZUSTAND["wartet"].pop(jid, None)
        if _ZUSTAND["laeuft"].pop(jid, None) is not None:
            _ZUSTAND["erledigt"] += 1


@contextlib.contextmanager
def platz_sync(art, wer=""):
    """Fuer Arbeiter-Threads: blockiert, bis die Kodierung dran ist."""
    jid, seit = _anmelden(art, wer)
    try:
        while not _versuchen(jid, seit):
            time.sleep(PRUEF_S)
        yield
    finally:
        _abmelden(jid)


@contextlib.asynccontextmanager
async def platz(art, wer=""):
    """Fuer den Event-Loop: wartet, ohne den Loop zu halten."""
    jid, seit = _anmelden(art, wer)
    try:
        while not _versuchen(jid, seit):
            await asyncio.sleep(PRUEF_S)
        yield
    finally:
        # Auch bei Abbruch (CancelledError) — sonst bliebe ein Platz fuer immer belegt.
        _abmelden(jid)


def lage() -> dict:
    """Momentaufnahme fuer /healthz und das Deck."""
    jetzt = time.time()
    with _SPERRE:
        def _liste(d, feld):
            return [{"art": e["art"], "wer": e["wer"], "s": round(jetzt - e[feld])}
                    for e in d.values()]
        return {"laeuft": _liste(_ZUSTAND["laeuft"], "start"),
                "wartet": _liste(_ZUSTAND["wartet"], "seit"),
                "erledigt": _ZUSTAND["erledigt"], "zwangsstart": _ZUSTAND["zwangsstart"],
                "parallel": parallel()}
