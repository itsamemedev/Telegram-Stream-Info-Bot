"""nc.pruefschlange — v5.1-W183: eine Live-Pruefung je Tracking, mit Frist.

════════════════════════════════════════════════════════════════════════
DER BEFUND (Produktionslog 11.11.)
════════════════════════════════════════════════════════════════════════
„Live-Check-Schlange voll: … verworfen (4809 bisher)" in 18 Minuten, dazu
„WATCHDOG: Loop 'live-worker-0' seit 450s ohne Lebenszeichen". Zwei
Ursachen, die sich gegenseitig hochschaukeln:

1. Der In-Flight-Riegel in `_pruef_runde` war eine ZEIT (90 s), keine
   Tatsache. Wartete ein Eintrag laenger als 90 s in der Schlange — oder
   hing ein Worker laenger —, wurde dasselbe Tracking ein zweites, drittes,
   viertes Mal eingereiht. Ein Stau erzeugte so Doppel, die Doppel
   verlaengerten den Stau, und die volle Schlange warf jede Sekunde den
   aeltesten Eintrag weg.
2. Eine einzelne Pruefung hatte keine Frist. Stand ein Worker (hier: im
   Fork-Poll hinter Whisper, nc/forkriegel.py), stand er beliebig lange,
   und sein Lebenszeichen stand mit ihm.

Jetzt: ein Tracking ist hoechstens EINMAL vorgemerkt — von der Einreihung
bis zum Ende der Pruefung (`vormerken`/`erledigt`). Und jede Pruefung laeuft
mit Frist; waehrend sie laeuft, gibt der Worker in Scheiben Lebenszeichen,
damit ein langsamer Lauf nicht als toter Worker gemeldet wird — und ein
Lauf ueber der Frist wird abgebrochen und laut gemeldet, statt den Worker
fuer immer zu binden.

Bot-frei. Die Vormerkung ist modul-global (CLAUDE.md: Guards nie als
Objekt-Attribut) und nur aus dem Event-Loop benutzt — kein Lock noetig.
"""

import asyncio

_VORGEMERKT = set()


def vormerken(tid) -> bool:
    """-> True, wenn `tid` jetzt vorgemerkt wurde; False, wenn es schon
    in der Schlange steht oder gerade geprueft wird (dann nicht einreihen)."""
    if tid in _VORGEMERKT:
        return False
    _VORGEMERKT.add(tid)
    return True


def erledigt(tid) -> None:
    """Pruefung zu Ende (oder Eintrag aus der Schlange verworfen)."""
    _VORGEMERKT.discard(tid)


def vorgemerkt() -> int:
    return len(_VORGEMERKT)


def zuruecksetzen() -> None:
    _VORGEMERKT.clear()


async def mit_frist(aufgabe, frist_s, scheibe_s, lebenszeichen):
    """`aufgabe` (Coroutine) mit Frist ausfuehren, Lebenszeichen je Scheibe.

    -> True, wenn sie fertig wurde; False, wenn die Frist ablief (dann ist
    sie abgebrochen). Eine Ausnahme der Aufgabe geht unveraendert durch.

    Warum nicht einfach `asyncio.wait_for`: das bricht ab, gibt aber
    zwischendurch kein Lebenszeichen. Ein Worker in einer langsamen, aber
    gesunden Pruefung (yt-dlp-Nachschlag bis 20 s, W102) waere fuer den
    Watchdog tot; ein Lebenszeichen nur VOR der Pruefung (wie bis W182)
    sagt nichts ueber die Pruefung selbst."""
    task = asyncio.ensure_future(aufgabe)
    loop = asyncio.get_running_loop()
    ende = loop.time() + max(0.0, float(frist_s))
    try:
        while True:
            rest = ende - loop.time()
            if rest <= 0:
                break
            fertig, _ = await asyncio.wait({task}, timeout=min(scheibe_s, rest))
            if fertig:
                task.result()          # wirft die Ausnahme der Aufgabe weiter
                return True
            lebenszeichen()
    except asyncio.CancelledError:
        task.cancel()
        raise
    task.cancel()
    # Auf das Ende des Abbruchs warten, ohne dessen Ausnahme zu werfen: was
    # die Aufgabe beim Abbrechen noch wirft, ist Folge des Abbruchs, nicht ihr
    # Befund — der Aufrufer meldet die Frist. Abgeholt wird sie trotzdem,
    # sonst schreibt asyncio „exception was never retrieved" ins Log.
    await asyncio.wait({task})
    if not task.cancelled():
        task.exception()
    return False
