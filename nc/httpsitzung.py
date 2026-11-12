"""nc.httpsitzung — v5.2-W193: eine geteilte aiohttp-Sitzung fuer kurze API-Aufrufe (bot-frei).

`nc/kickapi.py` oeffnete fuer jeden Aufruf eine eigene `ClientSession` —
`send_message` sogar zwei (eine fuer den Token, eine fuer die Nachricht). Jede
Sitzung baut ihre Verbindung neu auf, also je AZRAEL-Antwort im Kick-Chat
zweimal TCP und TLS zu api.kick.com/id.kick.com, statt eine offene Verbindung
weiterzunutzen.

Die Sitzung gehoert dem laufenden Event-Loop (eine aiohttp-Sitzung darf nicht
ueber Loops wandern) und wird neu angelegt, wenn sie geschlossen ist. Wer eine
eigene Sitzung uebergibt, behaelt sie — der Aufrufer schliesst die geteilte
nie. HTTP_SITZUNG_TEILEN=0 schaltet ab (dann je Aufruf eine eigene wie bisher).
"""

import asyncio
import os

_SITZUNG = {}                    # id(loop) -> (loop, sitzung)


def teilen() -> bool:
    return os.getenv("HTTP_SITZUNG_TEILEN", "1").strip().lower() not in (
        "0", "false", "nein", "no", "aus", "off")


def sitzung():
    """(sitzung, eigen) fuer den laufenden Loop. eigen=True: der Aufrufer
    schliesst sie selbst (Teilen aus)."""
    import aiohttp
    if not teilen():
        return aiohttp.ClientSession(), True
    loop = asyncio.get_running_loop()
    eintrag = _SITZUNG.get(id(loop))
    if eintrag is None or eintrag[0] is not loop or eintrag[1].closed:
        # Gleiche id, anderer Loop (nach einem Neustart des Loops) oder zu:
        # neu anlegen. Alte Eintraege toter Loops raeumen wir mit ab.
        for k in [k for k, (lp, _s) in _SITZUNG.items() if lp.is_closed()]:
            _SITZUNG.pop(k, None)
        eintrag = (loop, aiohttp.ClientSession())
        _SITZUNG[id(loop)] = eintrag
    return eintrag[1], False


async def schliessen():
    """Beim Herunterfahren: die Sitzung des laufenden Loops schliessen."""
    eintrag = _SITZUNG.pop(id(asyncio.get_running_loop()), None)
    if eintrag is not None and not eintrag[1].closed:
        await eintrag[1].close()
