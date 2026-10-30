"""nc.kindprozess — v4.2-W120: ein Kindprozess endet auf JEDEM Weg.

════════════════════════════════════════════════════════════════════════
DER BESTAND
════════════════════════════════════════════════════════════════════════
22 Stellen starten Kindprozesse per `asyncio.create_subprocess_exec`. Die
Abraeum-Hilfe `_reap_proc` (W75) gibt es seit Langem — benutzt wird sie an
drei. Der Rest hat sein eigenes Muster, und es hat zwei Loecher:

**Kein Zeitlimit.** `_shrink_for_discord`, `clip_moment` und
`_restream_tts_enqueue_wav` warteten mit nacktem `await proc.communicate()`.
Ein ffmpeg, der an einer kaputten Datei haengt, haengt dort fuer immer —
und mit ihm der Task, der ihn gestartet hat, samt Pipes und fds.

**Der Abbruch.** Jede Stelle faengt `asyncio.TimeoutError` und raeumt ab.
Keine einzige raeumt ab, wenn der AUFRUFENDE Task abgebrochen wird: ein
`CancelledError` ist seit Python 3.8 kein `Exception` mehr, rauscht an
`except Exception` vorbei, und der Prozess laeuft weiter — ohne dass ihn
noch jemand kennt. Abgebrochen wird oefter, als man denkt: beim
Herunterfahren jeder Task, im Restream-Wechsel der Quellen-Watcher, im
Single-Flight aus W119 der fuehrende Lauf. Ein yt-dlp laeuft dann seine
20 s zu Ende, ein Neukodieren einer Aufnahme seine Viertelstunde.

════════════════════════════════════════════════════════════════════════
DIE REGEL
════════════════════════════════════════════════════════════════════════
`ausfuehren(cmd, zeitlimit, art)` ist der Weg: das Zeitlimit ist Pflicht,
und das Abraeumen steht im `finally` — es laeuft bei Erfolg (dann ist
nichts zu tun), Zeitablauf, Ausnahme und Abbruch gleichermassen. Danach
fliegt, was geflogen waere: `asyncio.TimeoutError`, die Ausnahme, der
`CancelledError`. Der Aufrufer behaelt seine Fehlerbehandlung; sie wird nur
nicht mehr gebraucht, um aufzuraeumen.

Abgeraeumt wird mit SIGTERM, dann SIGKILL, und beide Male mit `wait()`:
ffmpeg schreibt auf SIGTERM noch sein moov-Atom (eine haelftig fertige
Datei bleibt abspielbar), und ohne `wait()` bleibt der Exit-Status liegen.

Jeder laufende Prozess steht im Register (`LAUFEND`), damit /healthz sagen
kann, wie viele es sind und wie alt der aelteste ist — und damit das
Herunterfahren sie alle findet (`alle_beenden`).

Bot-frei, stdlib-only.
"""
from __future__ import annotations

import asyncio
import threading
import time
from typing import Optional, Sequence, Tuple

PIPE = asyncio.subprocess.PIPE
DEVNULL = asyncio.subprocess.DEVNULL

_SPERRE = threading.Lock()
# pid -> (art, start_monotonic, proc)
LAUFEND: dict = {}
ZAEHLER = {"gestartet": 0, "zeitlimit": 0, "abgebrochen": 0, "getoetet": 0}


def _zaehle(art: str) -> None:
    with _SPERRE:
        ZAEHLER[art] += 1


async def beenden(proc, term_s: float = 5.0, kill_s: float = 3.0) -> str:
    """SIGTERM -> wait -> SIGKILL -> wait. -> "lief_nicht" | "term" | "kill"

    Wirft nie: ein Prozess, der beim Abraeumen schon weg ist, ist das Ziel,
    kein Fehler. Gewartet wird begrenzt — ein Abraeumen, das selbst haengt,
    haelt sonst den Aufrufer, den es befreien soll."""
    if proc is None or proc.returncode is not None:
        return "lief_nicht"
    try:
        proc.terminate()
    except ProcessLookupError:
        return "lief_nicht"
    try:
        await asyncio.wait_for(proc.wait(), timeout=term_s)
        return "term"
    except asyncio.TimeoutError:
        pass                 # SIGTERM ignoriert -> naechste Stufe, kein Fehler
    try:
        proc.kill()
    except ProcessLookupError:
        return "term"
    _zaehle("getoetet")
    try:
        await asyncio.wait_for(proc.wait(), timeout=kill_s)
    except asyncio.TimeoutError:
        # Nach SIGKILL heisst das: der Prozess steckt im Kernel (D-Zustand,
        # meist eine haengende Platte). Dagegen hilft nichts mehr von hier;
        # der Kindprozess-Waechter des Loops holt ihn ab, sobald er endet.
        pass
    return "kill"


async def ausfuehren(cmd: Sequence[str], zeitlimit: float, art: str = "?",
                     stdout=PIPE, stderr=PIPE, eingabe: Optional[bytes] = None
                     ) -> Tuple[int, bytes, bytes]:
    """`cmd` starten, hoechstens `zeitlimit` s warten. -> (rc, out, err)

    Wirft `asyncio.TimeoutError` nach Ablauf (der Prozess ist dann schon
    beendet), `OSError` wenn er nicht startet, und reicht jeden Abbruch
    durch — immer erst NACHDEM der Prozess abgeraeumt ist."""
    if not zeitlimit or zeitlimit <= 0:
        raise ValueError("ausfuehren ohne Zeitlimit — genau das soll es nicht geben")
    proc = await asyncio.create_subprocess_exec(
        *cmd, stdout=stdout, stderr=stderr,
        stdin=PIPE if eingabe is not None else DEVNULL)
    with _SPERRE:
        LAUFEND[proc.pid] = (str(art), time.monotonic(), proc)
        ZAEHLER["gestartet"] += 1
    try:
        out, err = await asyncio.wait_for(proc.communicate(eingabe), timeout=zeitlimit)
        return proc.returncode, out or b"", err or b""
    except asyncio.TimeoutError:
        _zaehle("zeitlimit")
        raise
    except asyncio.CancelledError:
        _zaehle("abgebrochen")
        raise
    finally:
        # Abschirmen: wird der Task WAEHREND des Abraeumens noch einmal
        # abgebrochen, darf das Abraeumen nicht mitsterben.
        if proc.returncode is None:
            await asyncio.shield(beenden(proc))
        with _SPERRE:
            LAUFEND.pop(proc.pid, None)


async def alle_beenden(term_s: float = 5.0) -> int:
    """Alle registrierten Prozesse beenden (Herunterfahren). -> wie viele."""
    with _SPERRE:
        procs = [e[2] for e in LAUFEND.values()]
    erg = await asyncio.gather(*[beenden(p, term_s=term_s) for p in procs],
                               return_exceptions=True)
    return sum(1 for e in erg if e in ("term", "kill"))


def lage(jetzt: Optional[float] = None) -> dict:
    """Fuer /healthz: Zahl je Art, Alter des aeltesten, Zaehler. Keine
       Kommandozeilen — darin stehen Stream-Adressen mit Token."""
    jetzt = time.monotonic() if jetzt is None else jetzt
    with _SPERRE:
        eintraege = list(LAUFEND.values())
        z = dict(ZAEHLER)
    je_art: dict = {}
    for art, _start, _p in eintraege:
        je_art[art] = je_art.get(art, 0) + 1
    aeltester = max((jetzt - s for _a, s, _p in eintraege), default=0.0)
    return {"laufend": len(eintraege), "je_art": je_art,
            "aeltester_s": round(aeltester, 0), **z}


def zuruecksetzen() -> None:
    """Nur fuer die Vertraege."""
    with _SPERRE:
        LAUFEND.clear()
        for k in ZAEHLER:
            ZAEHLER[k] = 0
