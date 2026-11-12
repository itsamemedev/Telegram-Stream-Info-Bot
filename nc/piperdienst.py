"""nc.piperdienst — v5.2-W193: Sprachausgabe ueber einen dauerhaften Piper-Prozess (bot-frei).

DER BEFUND
  `_piper_say` startete je Satz `piper` neu. piper-tts ist selbst ein
  Python-Programm: gemessen 0,5–0,6 s CPU fuer Interpreter, piper und
  onnxruntime, BEVOR die Stimme (rund 60 MB .onnx) geladen ist — und die wird
  bei jedem Satz neu geladen. AZRAEL spricht im Live-Betrieb mehrmals je
  Minute, und jede dieser Spitzen faellt auf dieselben Kerne wie der Transcode.

DIE REGEL
  Ein Arbeiter (nc/piperarbeiter.py) laedt piper einmal und haelt die Stimme.
  Belegt, nicht startbar oder gestorben -> None, und der Bot nimmt den alten
  Einzelaufruf. Zeitueberschreitung -> Arbeiter beendet, Ergebnis False.
  PIPER_ARBEITER=0 schaltet ab.
"""

import asyncio
import json
import logging
import os
import sys

log = logging.getLogger("TikTokBot")
_SKRIPT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "piperarbeiter.py")
PY_ARGS = ["-I"]                  # isoliert, wie nc/ytdlpdienst.py
LAGE = {"saetze": 0, "ersatz": 0, "zeitlimit": 0, "gestartet": 0, "grund": ""}
_ZUSTAND = {"proc": None, "belegt": False, "startend": False}


def an() -> bool:
    """PIPER_ARBEITER (Vorgabe 1). Als Funktion gelesen."""
    return os.getenv("PIPER_ARBEITER", "1").strip().lower() not in (
        "0", "false", "nein", "no", "aus", "off")


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


async def _beenden():
    p, _ZUSTAND["proc"] = _ZUSTAND["proc"], None
    if p is not None and p.returncode is None:
        p.kill()
        await p.wait()


async def _starten():
    proc = await asyncio.create_subprocess_exec(
        sys.executable, *PY_ARGS, _SKRIPT, stdin=asyncio.subprocess.PIPE,
        stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.DEVNULL)
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
    LAGE["gestartet"] += 1
    _ZUSTAND["proc"] = proc
    return proc


async def sprechen(modell, text, aus, laenge, zeitlimit=30.0):
    """WAV schreiben. -> True (geschrieben), False (gescheitert) oder None
    (kein Arbeiter nutzbar — der Aufrufer nimmt den Einzelaufruf)."""
    if not an():
        return None
    if _ZUSTAND["belegt"] or _ZUSTAND["startend"]:
        LAGE["ersatz"] += 1
        _grund_melden("Arbeiter belegt")
        return None
    _ZUSTAND["belegt"] = True
    try:
        proc = _ZUSTAND["proc"]
        if proc is None or proc.returncode is not None:
            _ZUSTAND["startend"] = True
            try:
                proc = await _starten()
            finally:
                _ZUSTAND["startend"] = False
            if proc is None:
                LAGE["ersatz"] += 1
                return None
        try:
            proc.stdin.write((json.dumps({"modell": modell, "text": text, "aus": aus,
                                          "laenge": laenge}) + "\n").encode())
            await proc.stdin.drain()
            zeile = await asyncio.wait_for(proc.stdout.readline(), zeitlimit)
        except asyncio.TimeoutError:
            LAGE["zeitlimit"] += 1
            _grund_melden("Synthese ueber %.0f s — Arbeiter beendet" % zeitlimit)
            await _beenden()
            return False
        except OSError as e:
            await _beenden()
            _grund_melden("Arbeiter ausgefallen: %s" % e)
            LAGE["ersatz"] += 1
            return None
        if not zeile:
            await _beenden()
            _grund_melden("Arbeiter beendet sich mitten im Satz")
            LAGE["ersatz"] += 1
            return None
        antwort = json.loads(zeile)
        if not antwort.get("ok"):
            _grund_melden(str(antwort.get("fehler") or "?")[:200])
            return False
        LAGE["saetze"] += 1
        return True
    except asyncio.CancelledError:
        await _beenden()               # nicht halb in einem Satz liegen lassen
        raise
    finally:
        _ZUSTAND["belegt"] = False


async def beenden():
    """Beim Herunterfahren."""
    await _beenden()


def lage() -> dict:
    p = _ZUSTAND["proc"]
    return dict(LAGE, laeuft=bool(p is not None and p.returncode is None), an=an())
