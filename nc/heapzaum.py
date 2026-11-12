"""nc.heapzaum — v5.2-W191: glibc-Heap deckeln und freien Speicher zurueckgeben (bot-frei).

DAS FEHLERBILD
  Der Bot laeuft mit 21+ Threads (Pruef-Worker, waitress, Whisper, der
  to_thread-Pool). glibc legt fuer nebenlaeufige Threads eigene Arenen an —
  bis zu 8 je Kern, hier also bis zu 64 — und gibt Speicher, der in einer
  Arena frei wird, kaum je an das System zurueck. Das Bild im Betrieb: der
  RSS steigt nach jeder Spitze (Whisper-Lauf, grosse JSON-Antwort, ein
  Modellwechsel wie am 11.11., W180) und faellt danach nicht mehr. Auf einer
  Box, auf der daneben ein 14B-LLM und mehrere ffmpeg laufen, ist das Platz,
  der dem Kernel beim naechsten OOM-Entscheid fehlt.

DIE REGEL
  * deckeln(): `mallopt(M_ARENA_MAX, n)` — so frueh wie moeglich, bevor die
    Threads ihre Arenen anlegen. Wirkt nur auf glibc; anderswo (musl, macOS)
    wird nichts getan und das als Lage gesagt, nicht verschwiegen.
  * zurueckgeben(): `malloc_trim(0)` — gibt freie Seiten aller Arenen zurueck.
    Gemessen wird der RSS davor und danach, damit /healthz sagt, ob es etwas
    bringt (und niemand eine Wirkung behauptet, die er nicht gesehen hat).

  Beides ist harmlos fuer die Korrektheit: mallopt aendert nur, WO alloziert
  wird, malloc_trim nur, was das System zurueckbekommt.
"""

import ctypes
import ctypes.util
import logging
import os
import sys
import time

log = logging.getLogger("TikTokBot")
M_ARENA_MAX = -8                 # glibc malloc.h
LAGE = {"libc": None, "arenen": None, "grund": "", "trims": 0,
        "frei_mb_summe": 0.0, "letzter_mb": 0.0, "letzter_ts": 0.0}
_LIBC = {"h": None, "geprueft": False}


def _grund(text):
    """Warum nichts getan wird — in /healthz und EINMAL ins Log (INFO: auf
    macOS/musl ist das der Normalfall, kein Alarm; W85)."""
    LAGE["grund"] = text
    log.info("Heap-Pflege: %s — Arenen bleiben auf der Vorgabe, kein malloc_trim.", text)


def _libc():
    """glibc-Handle mit mallopt und malloc_trim — oder None (Grund in LAGE)."""
    if _LIBC["geprueft"]:
        return _LIBC["h"]
    _LIBC["geprueft"] = True
    if not sys.platform.startswith("linux"):
        _grund("kein Linux (%s)" % sys.platform)
        return None
    name = ctypes.util.find_library("c") or "libc.so.6"
    try:
        h = ctypes.CDLL(name, use_errno=True)
        h.mallopt.argtypes = (ctypes.c_int, ctypes.c_int)
        h.malloc_trim.argtypes = (ctypes.c_size_t,)
    except (OSError, AttributeError) as e:
        # musl hat weder mallopt noch malloc_trim — dann gibt es nichts zu tun.
        _grund("keine glibc (%s: %s)" % (type(e).__name__, e))
        return None
    _LIBC["h"] = h
    LAGE["libc"] = name
    return h


def arenen_wunsch() -> int:
    """SPEICHER_ARENEN: 0 = glibc-Vorgabe lassen; Vorgabe 2. Als Funktion gelesen."""
    roh = os.getenv("SPEICHER_ARENEN", "2").strip()
    return max(0, min(64, int(roh))) if roh.isdigit() else 2


def deckeln(n=None) -> bool:
    """Arenen auf n begrenzen. -> True, wenn gesetzt."""
    n = arenen_wunsch() if n is None else int(n)
    if n <= 0:
        LAGE["grund"] = "SPEICHER_ARENEN=0 (glibc-Vorgabe)"
        return False
    h = _libc()
    if h is None:
        return False
    if h.mallopt(M_ARENA_MAX, n) != 1:
        _grund("mallopt(M_ARENA_MAX, %d) abgelehnt" % n)
        return False
    LAGE["arenen"] = n
    return True


def rss_mb() -> float:
    """Resident Set Size dieses Prozesses in MB (/proc), sonst -1."""
    if not os.path.exists("/proc/self/statm"):
        return -1.0
    with open("/proc/self/statm") as f:
        teile = f.read().split()
    return int(teile[1]) * os.sysconf("SC_PAGE_SIZE") / 1048576.0


def zurueckgeben() -> dict:
    """malloc_trim(0) mit RSS-Messung. -> {"ok", "vorher_mb", "nachher_mb", "frei_mb"}

    Laeuft synchron und kann bei grossem Heap einige Millisekunden dauern —
    aus dem Event-Loop nur ueber asyncio.to_thread aufrufen (W97)."""
    h = _libc()
    if h is None:
        return {"ok": False, "grund": LAGE["grund"]}
    vorher = rss_mb()
    h.malloc_trim(0)
    nachher = rss_mb()
    frei = max(0.0, vorher - nachher) if vorher >= 0 and nachher >= 0 else 0.0
    LAGE["trims"] += 1
    LAGE["frei_mb_summe"] = round(LAGE["frei_mb_summe"] + frei, 1)
    LAGE["letzter_mb"] = round(frei, 1)
    LAGE["letzter_ts"] = time.time()
    return {"ok": True, "vorher_mb": round(vorher, 1), "nachher_mb": round(nachher, 1),
            "frei_mb": round(frei, 1)}


def takt_min() -> float:
    """SPEICHER_TRIM_MIN: Abstand der Rueckgabe in Minuten (0 = aus), Vorgabe 10."""
    roh = os.getenv("SPEICHER_TRIM_MIN", "10").strip()
    try:
        return max(0.0, float(roh))
    except ValueError:
        _grund("SPEICHER_TRIM_MIN=%r ist keine Zahl — Vorgabe 10" % roh[:20])
        return 10.0


def lage() -> dict:
    """Fuer /healthz."""
    return dict(LAGE)
