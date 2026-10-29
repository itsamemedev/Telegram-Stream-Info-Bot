"""nc.kiwahl — v4.2-W110: EINE Antwort auf „lokal oder Cloud?".

Der Betreiber hat llama.cpp installiert (`llama-server.service`) und erwartet,
dass es benutzt wird. Nachgesehen, wann es das wurde:

* Der zentrale Chat (`llm_chat`, `llm_chat_sync`) fragte das Brain NUR bei
  `AI_PROVIDER=brain`. Ohne die Zeile ging jede Anfrage an die keyless Cloud,
  waehrend der lokale Server lief und wartete.
* Die Reaktions-Engine stand per Vorgabe auf `REACTION_AI_PROVIDER=pollinations`
  — lokal nie.
* Die Modellliste rief `get_brain().llm.models()`. Die Methode gab es nicht;
  der AttributeError wurde still gefangen, und im Deck standen nur
  Cloud-Modelle.
* Dieselbe Abfrage „AI_PROVIDER == brain" stand siebenmal
  verstreut (Bot, vier Routen, Konfig-Drift) — jede Anzeige rechnete selbst
  und behauptete „freeai", wenn die Zeile fehlte.

`brain/llm.py` selbst war richtig gebaut: lokal zuerst, die Cloud als Reserve,
Stundenbudget, ein Inferenz-Slot. Gefehlt hat nur, dass jemand es fragt.

**Die Regel:** ``AI_PROVIDER`` ist ``auto`` (Vorgabe), ``lokal`` oder
``cloud``. ``auto`` heisst: lokal, wenn `llama-server` antwortet, sonst Cloud.
``lokal`` (auch die alten Werte ``brain``/``llamacpp``) fragt lokal auch dann
zuerst, wenn die letzte Probe tot war — ``brain/llm.py`` faellt dann selbst auf
die Cloud zurueck. ``cloud`` (auch ``freeai``/``pollinations``) laesst lokal aus.
Fuer die Reaktions-Engine gilt dieselbe Regel mit ``REACTION_AI_PROVIDER``.

Was lokal NICHT kann und deshalb weiter in die Cloud geht: Bilder (Vision).
llama-server kann das nur mit einem multimodalen Modell plus ``--mmproj``,
und der Chat-Pfad hier reicht Bilder nicht im OpenAI-Format durch.
"""

import logging
import os
import time

from nc import meldetakt as _takt

log = logging.getLogger("TikTokBot")

LOKAL = "lokal"
CLOUD = "cloud"
AUTO = "auto"

_ALIAS = {
    "": AUTO, "auto": AUTO,
    "lokal": LOKAL, "local": LOKAL, "brain": LOKAL, "llamacpp": LOKAL,
    "llama.cpp": LOKAL,
    "cloud": CLOUD, "freeai": CLOUD, "pollinations": CLOUD, "keyless": CLOUD,
}


def normal(wert) -> str:
    """Einen Provider-Wert auf auto/lokal/cloud abbilden.

    Unbekannte Werte werden zu ``auto`` — nicht zu ``cloud``: wer sich
    vertippt, soll nicht still auf den lokalen Server verzichten, den er
    gerade installiert hat. (Ein Groq- oder OpenRouter-Wert der
    Reaktions-Engine landet damit ebenfalls bei auto; die Cloud-Kette dahinter
    ist dieselbe.)
    """
    return _ALIAS.get(str(wert or "").strip().lower(), AUTO)


def provider() -> str:
    """AI_PROVIDER, zur Laufzeit gelesen (CLAUDE.md: keine Modul-Konstante)."""
    return normal(os.getenv("AI_PROVIDER", "auto"))


def lokal_zuerst(wahl, lokal_oben) -> bool:
    """Soll der lokale Server zuerst gefragt werden?

    `lokal_oben` ist True/False/None (None = nie gemessen). Bei ``auto`` und
    unbekanntem Zustand wird gefragt: die erste Anfrage IST dann die Probe,
    und brain/llm.py faellt bei totem Server in Sekunden auf die Cloud.
    """
    w = normal(wahl)
    if w == CLOUD:
        return False
    if w == LOKAL:
        return True
    return lokal_oben is not False


def lokal_stand(messen=False):
    """Antwortet llama-server? -> True / False / None (unbekannt).

    `messen=False` liest nur den Zwischenstand der letzten Probe (15 s alt
    hoechstens) und kostet nichts — so duerfen Anzeigen und /healthz fragen,
    ohne selbst eine 3-s-Probe auszuloesen (W105: /healthz misst nicht).
    """
    try:
        from brain import get_brain
        llm = get_brain().llm
        if messen:
            return bool((llm.health().get("llamacpp") or {}).get("up"))
        return llm.zuletzt_oben()
    except Exception as e:
        # Kein stilles None: „unbekannt" heisst bei auto „lokal versuchen",
        # und wer nicht sieht, dass das Brain gar nicht startet, sucht den
        # Fehler am llama-server.
        laut, weg = _takt.melden("kiwahl", type(e).__name__, time.time())
        if laut:
            log.warning("KI-Wahl: Brain nicht erreichbar (%s: %s) — der lokale "
                        "Weg bleibt ungeprueft.%s", type(e).__name__, e,
                        _takt.zusatz(weg))
        return None


def backend(wahl=None, lokal_oben="lesen") -> str:
    """Was die Anzeigen nennen: ``brain`` (lokal), ``freeai`` (Cloud) oder
    ``auto`` (lokal bevorzugt, Zustand noch nicht gemessen)."""
    w = normal(wahl if wahl is not None else os.getenv("AI_PROVIDER", "auto"))
    oben = lokal_stand() if lokal_oben == "lesen" else lokal_oben
    if w == CLOUD:
        return "freeai"
    if w == LOKAL or oben is True:
        return "brain"
    return "freeai" if oben is False else "auto"
