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

import contextvars
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
    """AZRAEL_LLM zur Laufzeit -> lokal / auto / cloud.

    v5.9-W201: die Wahl im Deck (deck_wahl) geht vor — sie gilt fuer Deck,
    Telegram und AZRAEL zugleich. Ohne sie bleibt alles wie in W196."""
    deck = deck_wahl()
    if deck:
        return {LOKAL: LOKAL, FREE: CLOUD, AUTO: AUTO}[deck]
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


# ─────────────────────────────────────────────────────────────────────────
# v5.9-W201: EINE Wahl fuer Deck, Telegram und AZRAEL — und wer geantwortet hat.
#
# Der Betreiber: „Azrael nutzt in Telegram eine free AI. Und im gesamten
# Dashboard sollte man zwischen lokaler und free AI unterscheiden koennen."
# Nachgesehen: es gab DREI Schalter (AI_PROVIDER fuer Chat und Deck,
# REACTION_AI_PROVIDER fuer die Reaktions-Engine, AZRAEL_LLM fuer die
# Persona), alle nur in der .env, und Telegram fragte AZRAEL_LLM gar nicht.
# Keine Antwort sagte, woher sie kam — der Fuss in Telegram nannte das
# EINGESTELLTE Modell, nicht das, das geantwortet hatte.
#
# Jetzt: ki.wahl in app_config, im Deck umschaltbar, mit Vorrang vor allen
# drei. lokal = nur das lokale Modell (kein Claude, kein stiller Wechsel in
# die Cloud), free = nur die freie Cloud-KI (nc.freeai, kein Claude), auto =
# die bisherige Kette. Leer = nicht gesetzt: dann gelten die .env-Schalter
# wie bisher — ein Update aendert nichts, bevor der Betreiber waehlt.
# ─────────────────────────────────────────────────────────────────────────

DECK_SCHLUESSEL = "ki.wahl"
FREE = "free"
DECK_WERTE = (LOKAL, FREE, AUTO)
_ANZEIGE = {LOKAL: "lokal", FREE: "free", AUTO: "auto", "": "aufgehoben (es gilt die .env)"}
# Die Wahl wird bei jeder KI-Anfrage gelesen; die Reaktions-Engine fragt im
# Sekundenbereich. Fuenf Sekunden Puffer sind fuer einen Klick im Deck
# unmerklich und sparen die Datenbank.
DECK_CACHE_S = 5.0
_DECK = {"t": -1e9, "wert": ""}


def deck_wahl(jetzt=None) -> str:
    """Die im Deck gesetzte Wahl ("lokal" | "free" | "auto") oder "" (nicht gesetzt).

    Nachsichtig gelesen: bei einem Datenbankfehler "" — dann gelten die
    .env-Schalter. Das ist hier die sichere Seite: eine gesperrte Datenbank
    soll AZRAEL nicht stumm schalten."""
    jetzt = time.monotonic() if jetzt is None else jetzt
    if jetzt - _DECK["t"] < DECK_CACHE_S:
        return _DECK["wert"]
    from nc import cfgstore
    roh = str(cfgstore.get(DECK_SCHLUESSEL, "") or "").strip().lower()
    wert = roh if roh in DECK_WERTE else ""
    _DECK.update(t=jetzt, wert=wert)
    return wert


def deck_setzen(wert) -> str:
    """Die Wahl im Deck setzen. "" hebt sie auf (dann gilt die .env). Wirft ValueError."""
    w = str(wert or "").strip().lower()
    if w not in DECK_WERTE + ("",):
        raise ValueError("KI-Wahl muss lokal, free, auto oder leer sein")
    from nc import cfgstore
    cfgstore.set_(DECK_SCHLUESSEL, w)
    _DECK.update(t=time.monotonic(), wert=w)
    # Ins Log nur ein fester Text je Wahl, nie der Wert aus der Anfrage —
    # auch geprueft bleibt er fuer die Datenflussanalyse Fremdeingabe.
    log.info("KI-Wahl im Deck: %s.", _ANZEIGE[w])
    return w


def brain_kette(wahl=None):
    """Die Backends fuer brain.llm.chat zur Wahl: lokal -> ["llamacpp"],
    free -> ["freeai"], sonst None (die konfigurierte Kette)."""
    w = deck_wahl() if wahl is None else wahl
    return {LOKAL: ["llamacpp"], FREE: ["freeai"]}.get(w)


# Wer hat geantwortet? Je Aufruf (ContextVar folgt dem awaitenden Task bzw.
# dem Thread der Flask-Anfrage — zwei gleichzeitige Anfragen ueberschreiben
# sich nicht), dazu Zaehler seit dem Start fuer das Deck.
HERKUNFT = ("lokal", "free", "claude")
_ALIAS_HERKUNFT = {"lokal": "lokal", "llamacpp": "lokal", "brain": "lokal",
                   "free": "free", "freeai": "free", "cloud": "free",
                   "claude": "claude", "anthropic": "claude"}
_HERKUNFT = contextvars.ContextVar("ki_herkunft", default="")
HERKUNFT_ZAEHLER = {"lokal": 0, "free": 0, "claude": 0}


def herkunft_von(wert) -> str:
    """Backend- oder Wegname -> "lokal" | "free" | "claude" | ""."""
    return _ALIAS_HERKUNFT.get(str(wert or "").strip().lower(), "")


def herkunft_setzen(wert) -> str:
    """Nach einer Antwort: wer war es? Zaehlt mit. -> die normalisierte Herkunft."""
    h = herkunft_von(wert)
    _HERKUNFT.set(h)
    if h:
        HERKUNFT_ZAEHLER[h] += 1
    return h


def herkunft_loeschen():
    """Vor einer Anfrage: kein Rest aus der vorigen im selben Faden."""
    _HERKUNFT.set("")


def herkunft() -> str:
    return _HERKUNFT.get()


def etikett(herkunft_wert, modell="") -> str:
    """„lokal · qwen3-14b" — fuer den Telegram-Fuss und die Ablage."""
    h = herkunft_von(herkunft_wert)
    name = {"lokal": "lokal", "free": "free", "claude": "Claude"}.get(h, "?")
    m = str(modell or "").strip()
    return "%s · %s" % (name, m) if m else name


def beschriftung(herkunft_wert, angefragt="") -> str:
    """Das Etikett einer Antwort fuer Fuss, Chat und KI-Log — mit dem Modell,
    das WIRKLICH geantwortet hat: lokal das geladene Modell, free das
    angefragte, Claude ohne Namen (der steht im Deck unter KI-Schluessel).
    Unbekannte Herkunft (Fehler): das angefragte Modell wie bisher."""
    h = herkunft_von(herkunft_wert)
    if h == "lokal":
        return etikett(h, lokales_modell() or "llama.cpp")
    if h == "free":
        return etikett(h, angefragt)
    if h == "claude":
        return etikett(h)
    return str(angefragt or "")


def deck_lage() -> dict:
    """Fuer den Umschalter im Deck: Wahl, was sie bewirkt, lokaler Server, Zaehler."""
    wahl = deck_wahl()
    oben = lokal_stand()
    return {"wahl": wahl, "azrael": azrael_wahl(),
            "chat": wahl or normal(os.getenv("AI_PROVIDER", "auto")),
            "lokal_oben": oben, "lokal_installiert": lokal_installiert(),
            "lokal_modell": lokales_modell() if oben else None,
            "zaehler": dict(HERKUNFT_ZAEHLER)}

