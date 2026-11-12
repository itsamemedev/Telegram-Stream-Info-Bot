"""nc.ytdlpdienst — v5.2-W193: yt-dlp-Aufrufe ueber dauerhafte Arbeitsprozesse (bot-frei).

DER BEFUND
  `_resolve_via_ytdlp` startete fuer jeden Nachschlag ein neues yt-dlp —
  Interpreter hochfahren, yt_dlp samt rund 1800 Extraktoren importieren.
  Gemessen: 0,24 s CPU je Start, bevor eine einzige Anfrage an TikTok geht.
  Bei 40 Live-Nutzern und 60 s Ruhezeit je Nutzer (W102) sind das bis zu
  0,17 Kerne nur fuer das Anlaufen.

DIE REGEL
  Ein Arbeiter (nc/ytdlparbeiter.py) laedt yt_dlp einmal und nimmt danach
  Aufrufe ueber stdin entgegen — mit denselben Argumenten und derselben
  Antwort wie die Kommandozeile, also aendert sich an der Auswertung nichts.
  Vier Riegel:
    * Zeitueberschreitung: der Arbeiter wird beendet wie vorher der
      Einzelaufruf (asyncio.TimeoutError geht durch). Abschiessbar bleibt er,
      weil er ein eigener Prozess ist und kein Thread im Bot.
    * Belegt, nicht startbar, gestorben: der alte Einzelaufruf laeuft
      (`ersatz`). Der Arbeiter ist eine Ersparnis, keine Voraussetzung.
    * Fassung: nur wenn die yt_dlp-Fassung des Arbeiters dieselbe ist wie die
      des Programms im PATH. Sonst haette ein `yt-dlp -U` keine Wirkung, und
      ein von TikTok gebrochener Extraktor bliebe gebrochen, waehrend der
      Betreiber das Update fuer eingespielt haelt.
    * Abnutzung: nach YTDLP_ARBEITER_LAEUFE Aufrufen (Vorgabe 200) neu, damit
      ein Leck in yt-dlp nicht ueber Tage waechst.
  YTDLP_ARBEITER=0 schaltet ab (Vorgabe 2 — so viele, wie der Resolver
  gleichzeitig zulaesst).
"""

import asyncio
import json
import logging
import os
import sys
import time

log = logging.getLogger("TikTokBot")
_SKRIPT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ytdlparbeiter.py")
# -I: isoliert — kein PYTHONPATH, kein Arbeitsverzeichnis im Suchpfad. Ein
# yt_dlp.py, das jemand in den Aufnahmeordner legt, wird so nie geladen.
PY_ARGS = ["-I"]
_ZEILE_MAX = 64 * 1024 * 1024        # ein Live-JSON ist gross; Vorgabe 64 KiB reicht nicht
LAGE = {"aufrufe": 0, "ersatz": 0, "zeitlimit": 0, "gestartet": 0, "grund": ""}
_ARBEITER = []                        # [_Arbeiter]
_FASSUNG = {}                         # (binpfad, mtime) -> Fassung des Programms
_STARTEND = {"n": 0}                  # Starts im Gange — sonst startet ein Wettlauf zu viele


def anzahl() -> int:
    """YTDLP_ARBEITER: so viele Arbeiter hoechstens (0 = aus). Als Funktion gelesen."""
    roh = os.getenv("YTDLP_ARBEITER", "2").strip()
    return max(0, min(8, int(roh))) if roh.isdigit() else 2


def laeufe_max() -> int:
    roh = os.getenv("YTDLP_ARBEITER_LAEUFE", "200").strip()
    return max(1, int(roh)) if roh.isdigit() else 200


_GEMELDET = set()


def _grund_melden(text):
    """Warum der Einzelaufruf lief: in /healthz (lage) und EINMAL je neuem
    Grund ins Log (INFO — der Einzelaufruf arbeitet ja; es kostet nur CPU).
    "belegt" ist Alltag bei zwei gleichzeitigen Aufrufen und bleibt still."""
    LAGE["grund"] = text
    if "belegt" in text or text in _GEMELDET:
        return
    _GEMELDET.add(text)
    log.info("%s: %s — Einzelaufruf wie vor v5.2-W193.", __name__, text)


class _Arbeiter:
    def __init__(self, proc, fassung):
        self.proc = proc
        self.fassung = fassung
        self.laeufe = 0
        self.belegt = False

    def lebt(self):
        return self.proc.returncode is None


async def _beenden(a):
    if a in _ARBEITER:
        _ARBEITER.remove(a)
    if a.proc.returncode is None:
        a.proc.kill()
        await a.proc.wait()


async def _fassung_programm(binpfad, ausfuehren):
    """`yt-dlp --version` des Programms im PATH — einmal je Datei und Stand."""
    schluessel = (binpfad, os.path.getmtime(binpfad))
    if schluessel not in _FASSUNG:
        rc, out, _err = await ausfuehren([binpfad, "--version"], 20)
        _FASSUNG[schluessel] = (out or b"").decode("utf-8", "ignore").strip() if rc == 0 else ""
    return _FASSUNG[schluessel]


async def _starten(binpfad, ausfuehren):
    """Einen Arbeiter starten. -> _Arbeiter oder None (Grund in LAGE)."""
    proc = await asyncio.create_subprocess_exec(
        sys.executable, *PY_ARGS, _SKRIPT, stdin=asyncio.subprocess.PIPE,
        stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.DEVNULL,
        limit=_ZEILE_MAX)
    try:
        kopf = json.loads(await asyncio.wait_for(proc.stdout.readline(), 30) or b"{}")
    except (asyncio.TimeoutError, ValueError) as e:
        _grund_melden("Arbeiter antwortet beim Start nicht (%s)" % type(e).__name__)
        kopf = {"bereit": False, "grund": LAGE["grund"]}
    if not kopf.get("bereit"):
        proc.kill()
        await proc.wait()
        _grund_melden("Arbeiter startet nicht: %s" % (kopf.get("grund") or "keine Antwort"))
        return None
    soll = await _fassung_programm(binpfad, ausfuehren)
    if soll != kopf.get("version"):
        proc.kill()
        await proc.wait()
        _grund_melden("yt_dlp im Bot (%s) ist nicht das yt-dlp im PATH (%s) — Einzelaufruf, "
               "damit ein Update des Programms wirkt" % (kopf.get("version"), soll or "?"))
        return None
    LAGE["gestartet"] += 1
    a = _Arbeiter(proc, soll)
    _ARBEITER.append(a)
    return a


async def _freier(binpfad, ausfuehren):
    for a in list(_ARBEITER):
        if not a.lebt():
            await _beenden(a)
    for a in _ARBEITER:
        if not a.belegt:
            return a
    if len(_ARBEITER) + _STARTEND["n"] >= anzahl():
        _grund_melden("alle Arbeiter belegt")
        return None
    _STARTEND["n"] += 1
    try:
        a = await _starten(binpfad, ausfuehren)
    finally:
        _STARTEND["n"] -= 1
    if a is not None:
        a.belegt = True                 # gehoert diesem Aufrufer, bevor ein anderer ihn sieht
    return a


async def ausfuehren(cmd, zeitlimit, ausfuehren_einzeln):
    """Wie nc.kindprozess.ausfuehren(cmd, zeitlimit) -> (rc, out, err).

    `ausfuehren_einzeln(cmd, zeitlimit)` ist der bisherige Weg; er laeuft,
    wenn kein Arbeiter frei oder nutzbar ist. asyncio.TimeoutError geht durch."""
    LAGE["aufrufe"] += 1
    a = await _freier(cmd[0], ausfuehren_einzeln) if anzahl() > 0 else None
    if a is None:
        LAGE["ersatz"] += 1
        return await ausfuehren_einzeln(cmd, zeitlimit)
    a.belegt = True
    try:
        a.proc.stdin.write((json.dumps({"argv": list(cmd[1:])}) + "\n").encode())
        await a.proc.stdin.drain()
        zeile = await asyncio.wait_for(a.proc.stdout.readline(), zeitlimit)
        antwort = json.loads(zeile) if zeile else None
    except asyncio.TimeoutError:
        LAGE["zeitlimit"] += 1
        await _beenden(a)
        raise
    except (OSError, ValueError, asyncio.LimitOverrunError) as e:
        # Arbeiter gestorben oder Antwort kaputt: einmal den alten Weg.
        await _beenden(a)
        _grund_melden("Arbeiter ausgefallen: %s: %s" % (type(e).__name__, e))
        LAGE["ersatz"] += 1
        return await ausfuehren_einzeln(cmd, zeitlimit)
    except BaseException:
        await _beenden(a)              # Abbruch (CancelledError): nicht halb belegt lassen
        raise
    finally:
        a.belegt = False
    if antwort is None:
        await _beenden(a)
        _grund_melden("Arbeiter beendet sich mitten im Aufruf")
        LAGE["ersatz"] += 1
        return await ausfuehren_einzeln(cmd, zeitlimit)
    a.laeufe += 1
    if a.laeufe >= laeufe_max():
        await _beenden(a)
    return (int(antwort.get("rc", 1)), str(antwort.get("out", "")).encode(),
            str(antwort.get("err", "")).encode())


async def alle_beenden():
    """Beim Herunterfahren. -> wie viele."""
    n = len(_ARBEITER)
    for a in list(_ARBEITER):
        await _beenden(a)
    return n


def lage() -> dict:
    """Fuer /healthz."""
    return dict(LAGE, arbeiter=len(_ARBEITER), belegt=sum(1 for a in _ARBEITER if a.belegt),
                vorgabe=anzahl(), stand=time.time())
