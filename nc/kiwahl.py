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

Seit v5.1-W181 ist „lokal" ik_llama.cpp mit Qwen3-14B-Uncensored, eingerichtet
von ``tools/ikllama.sh`` als ``llama-server.service`` auf demselben Port wie
vorher. Fuer diese Datei aendert das nichts: sie spricht nur HTTP mit dem
Server, und ik_llama.cpp hat dieselbe Schnittstelle (``/health``,
``/v1/chat/completions``).

Was lokal NICHT kann und deshalb weiter in die Cloud geht: Bilder (Vision).
llama-server kann das nur mit einem multimodalen Modell plus ``--mmproj``,
und der Chat-Pfad hier reicht Bilder nicht im OpenAI-Format durch.
"""

import logging
import os
import shutil
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


# v5.1-W181: wo ein lokaler Server liegen kann. ik_llama.cpp landet NICHT im
# PATH (/opt/ik_llama.cpp/build/bin), und der Selbsttest fragte bis hierher nur
# shutil.which("llama-server") — ein installierter, aber gestorbener Server
# galt damit als „nicht installiert", und die Zeile blieb gruen.
UNIT_ORTE = ("/etc/systemd/system", "/lib/systemd/system", "/usr/lib/systemd/system")
UNIT_NAMEN = ("llama-server.service", "llamacpp.service")
PROGRAMME = ("/opt/ik_llama.cpp/build/bin/llama-server",)


def lokal_installiert(wurzel="") -> bool:
    """Ist auf dieser Maschine ein lokaler LLM-Server eingerichtet?

    Ja, wenn `llama-server` im PATH liegt, eine der Units existiert oder das
    Programm von ``tools/ikllama.sh`` da ist. `wurzel` ist fuer die Vertraege.
    Liest nur das Dateisystem — kein HTTP, keine Probe."""
    if not wurzel and shutil.which("llama-server"):
        return True
    for ort in UNIT_ORTE:
        for name in UNIT_NAMEN:
            if os.path.isfile(wurzel + ort + "/" + name):
                return True
    return any(os.path.isfile(wurzel + p) for p in PROGRAMME)


def lokales_modell():
    """Name des lokal geladenen Modells laut letzter Probe, sonst None.

    v5.1-W181. Liest nur den Zwischenstand (brain/llm.py: zuletzt_modell) —
    Anzeigen duerfen fragen, ohne zu messen."""
    try:
        from brain import get_brain
        return get_brain().llm.zuletzt_modell()
    except Exception as e:
        laut, weg = _takt.melden("kiwahl", type(e).__name__, time.time())
        if laut:
            log.warning("KI-Wahl: Modellname des lokalen Servers nicht lesbar "
                        "(%s: %s) — die Anzeige nennt das Cloud-Modell.%s",
                        type(e).__name__, e, _takt.zusatz(weg))
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


# ─────────────────────────────────────────────────────────────────────────
# v5.5-W196: AZRAEL an das lokale Modell binden.
#
# Gemessen beim Betreiber (Qwen3-14B Q4 auf der CPU, -t 4): 7,8 Token/s beim
# Einlesen, 3,4 Token/s beim Erzeugen. AZRAELs Zeitlimits waren 25 s
# (Gespraech) und 75 s (Reaktion) — das schafft das Modell mit einer Persona
# von mehreren hundert Token nie, und dann antwortete still die Cloud, mit
# anderem Modell und anderem Ton. Dazu ging ein gesetzter Anthropic-Schluessel
# VOR das lokale Modell. Wer mit der Persona spricht, wusste nie, mit wem.
#
# AZRAEL_LLM:
#   lokal  nur das lokale Modell. Kein Claude, kein stiller Wechsel in die
#          Cloud; antwortet es nicht, sagt AZRAEL nichts — und das Log sagt warum.
#   auto   wie die uebrige KI (AI_PROVIDER-Regel: Claude, lokal, Cloud).
#   cloud  lokal auslassen.
# Vorgabe: lokal, WENN ein lokaler Server eingerichtet ist (lokal_installiert),
# sonst auto — eine Vorgabe „lokal" ohne Server schaltete AZRAEL stumm, und
# genau so eine Vorgabe hat in W110 ein Feature lautlos abgeschaltet.
# ─────────────────────────────────────────────────────────────────────────

VORRAENGE = ("gespraech", "reaktion", "nebenbei")
_ZEIT_ENV = ("AZRAEL_LOKAL_ZEIT_GESPRAECH", "AZRAEL_LOKAL_ZEIT_REAKTION",
             "AZRAEL_LOKAL_ZEIT_NEBENBEI")

# Zwecke, die niemand angefordert hat: AZRAEL redet von sich aus. Bei Stau
# fallen sie weg, statt ein Gespraech warten zu lassen.
_NEBENBEI = ("dead-air", "director", "hype", "proaktiv", "proactive", "recap-auto")


def azrael_wahl() -> str:
    """AZRAEL_LLM zur Laufzeit -> lokal / auto / cloud."""
    roh = os.getenv("AZRAEL_LLM", "").strip()
    if not roh:
        return LOKAL if lokal_installiert() else AUTO
    return normal(roh)


def vorrang(zweck) -> str:
    """Zweck eines AZRAEL-Aufrufs -> gespraech / reaktion / nebenbei.

    Die Live-Reaktion nennt sich selbst ``reaktion``; was von sich aus
    redet, steht in _NEBENBEI; alles andere hat jemand angesprochen."""
    z = str(zweck or "").strip().lower()
    if z in VORRAENGE:
        return z
    if any(w in z for w in _NEBENBEI):
        return "nebenbei"
    return "gespraech"


def zeitlimit(vorr) -> float:
    """Wie lange AZRAEL auf das lokale Modell wartet (Rechnen + Warten auf den
    Platz), je Vorrang. Einstellbar mit AZRAEL_LOKAL_ZEIT_<VORRANG> (Sekunden).

    Die Vorgaben folgen der Messung: mit Prompt-Cache bleibt je Nachricht der
    wechselnde Teil (rund 150 Token = 20 s) plus ein, zwei Saetze (rund 40
    Token = 12 s). Ein Gespraech darf auf einen belegten Platz warten, eine
    Reaktion kuerzer — sie ist sonst veraltet —, Eigeninitiative gar nicht."""
    vorgabe = {"gespraech": 180, "reaktion": 90, "nebenbei": 60}.get(vorr, 90)
    name, roh = "", ""
    for kandidat in _ZEIT_ENV:          # woertlich, damit .env.example sie kennt (W99)
        if kandidat.endswith("_" + str(vorr).upper()):
            name, roh = kandidat, os.getenv(kandidat, "").strip()
            break
    try:
        return max(10.0, float(roh)) if roh else float(vorgabe)
    except ValueError:
        # Ein Tippfehler in der .env darf nicht still die Vorgabe ergeben —
        # sonst wundert sich der Betreiber, warum seine Einstellung nicht wirkt.
        laut, weg = _takt.melden("kiwahl", name, time.time())
        if laut:
            log.warning("KI-Wahl: %s=%r ist keine Zahl — es gilt die Vorgabe %d s.%s",
                        name, roh, vorgabe, _takt.zusatz(weg))
        return float(vorgabe)


def wartezeit(vorr) -> float:
    """Wie lange auf einen belegten Platz gewartet wird — die Haelfte des
    Zeitlimits fuer Gespraeche, ein Drittel fuer Reaktionen, nie fuer
    Eigeninitiative (die faellt bei Stau weg)."""
    anteil = {"gespraech": 0.5, "reaktion": 0.33}.get(vorr, 0.0)
    return zeitlimit(vorr) * anteil


# Wer hat AZRAEL geantwortet? Fuer /healthz und das Deck.
AZRAEL_WEG = {"lokal": 0, "cloud": 0, "claude": 0, "verworfen": 0,
              "letzter_grund": "", "letzter_weg": ""}


def weg_zaehlen(weg, grund=""):
    AZRAEL_WEG[weg] = AZRAEL_WEG.get(weg, 0) + 1
    AZRAEL_WEG["letzter_weg"] = weg
    if grund:
        AZRAEL_WEG["letzter_grund"] = str(grund)[:200]


def azrael_lage() -> dict:
    """Fuer /healthz: Wahl, Zaehler, und ob AZRAEL wirklich bei der Wahl bleibt."""
    d = dict(AZRAEL_WEG)
    d["wahl"] = azrael_wahl()
    gesamt = sum(AZRAEL_WEG.get(k, 0) for k in ("lokal", "cloud", "claude"))
    d["lokal_anteil"] = round(AZRAEL_WEG["lokal"] / gesamt, 3) if gesamt else None
    return d


def gesamtzeit(vorr) -> float:
    """Obergrenze fuer einen ganzen lokalen AZRAEL-Aufruf: Warten auf den
    Platz + Rechnen + 10 s Puffer. Aeussere wait_for-Grenzen der Aufrufer
    muessen mindestens so lang sein, sonst schneiden sie die Antwort ab,
    die das Modell gerade fertig hat."""
    return zeitlimit(vorr) + wartezeit(vorr) + 10.0


def llm_zeiten() -> dict:
    """Fuer /healthz: was die letzte lokale Antwort gekostet hat, wie viel des
    Prompts aus dem Cache kam, Budget und Platz. Liest nur Zaehler — misst nicht
    (W105: /healthz misst nicht)."""
    try:
        from brain import get_brain
        st = get_brain().llm.stats()
    except Exception as e:
        laut, weg = _takt.melden("kiwahl", type(e).__name__, time.time())
        if laut:
            log.warning("KI-Wahl: Zahlen des lokalen Modells nicht lesbar (%s: %s).%s",
                        type(e).__name__, e, _takt.zusatz(weg))
        return {"lesbar": False, "grund": type(e).__name__}
    return {"lesbar": True, "letzte": st.get("letzte_zeiten") or {},
            "cache_anteil": st.get("cache_anteil"), "slot": st.get("slot"),
            "budget": st.get("budget"), "reserve": st.get("reserve"),
            "abgewiesen": {"budget": st.get("budget_denied", 0),
                           "reserve": st.get("reserve_denied", 0),
                           "belegt": st.get("busy_denied", 0)}}
