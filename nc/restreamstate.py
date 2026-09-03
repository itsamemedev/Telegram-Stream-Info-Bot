"""nc.restreamstate — v4.1-W22: der Laufzeitzustand rund um den Restream.

════════════════════════════════════════════════════════════════════════
WARUM DIESES MODUL
════════════════════════════════════════════════════════════════════════
Die sechzehn Routen unter `/api/restream` lesen sieben Zustands-Container und
den Restream-Manager. Als nc.ctx-Einträge wären das acht der 25 vertraglichen
Plätze — bei 24 belegten unmöglich. Der Kontext ist auch der falsche Ort:
das ist **geteilter Zustand**, den Bot und Oberfläche gemeinsam sehen müssen,
keine Fähigkeit, die nur der Monolith hat (wie schon in nc/azraelstate.py und
nc/brainstate.py).

Alle sieben Container sind **Aliase**: bot.py verändert sie nur an Ort und
Stelle und bindet keinen der Namen je neu. Ein Vertrag hält das fest — kippt
es, zeigt der Alias auf eine tote Kopie und das Deck meldet einen
eingefrorenen Stand, ohne Fehler und ohne Logzeile.

**MGR ist ein Register**, und zwar aus demselben Grund wie PROXY in W21: der
RestreamManager entsteht im Monolithen erst weit unten in der Datei, lange
nach dem Import dieses Moduls. Ein Alias wäre für immer None, und jede
Steuerroute meldete "kein Manager", während er läuft.
"""

# ---- Geteilter Zustand (Aliase) --------------------------------------------

# rid -> {"user","label",...}: ALLE laufenden Restreams. Der primäre liegt
# daneben in nc/channels.RESTREAM_ACTIVE (W18) — dort steht nur der zuletzt
# gestartete, hier stehen alle. Beide werden gebraucht: das Overlay zeigt den
# primären, das Deck zeigt alle.
ACTIVE_ALL = {}


# Sendebild-Layout zur Laufzeit ("studio" | "burnin"). Ein Dict statt einer
# Zeichenkette, damit es teilbar ist — ein nackter String wäre eine Kopie.
LAYOUT = {"mode": "studio"}

# Diagnose des TikTok-Chat-Listeners. Macht "Panel leer" erklärbar: verbunden?
# wie viele Ereignisse? letzter Fehler? welcher Egress?
CHAT_DIAG = {"user": None, "phase": "idle", "since": 0.0, "events": 0,
             "last_error": "", "egress": "", "register": "", "cooldown_until": 0.0}

# username -> Regie-Instanz der laufenden Live-Reaction.
DIRECTORS = {}

# username -> Startzeit der laufenden Aufnahme-Session.
SESSION_START = {}

# Cache der YouTube-Ingest-Adresse (B138). Die YouTube Data API hat ein
# TAGES-Kontingent; ohne Cache wäre es vor Mittag verbrannt (dieselbe
# Überlegung wie bei YT_API_CACHE in nc/channels.py).
#
# ACHTUNG: "key" ist ein echter Sendeschlüssel — nie loggen, nie in eine
# API-Antwort. `reason`/`source`/`broadcast`/`bound` sind die Diagnose-Felder,
# die stattdessen ins Dashboard gehören. `last_logged` verhindert, dass
# derselbe Fehlgrund bei jedem Restream-Start erneut ins Log wandert.
YT_INGEST_CACHE = {"addr": "", "key": "", "ts": 0.0, "reason": "", "source": "",
                   "broadcast": "", "bound": "", "last_logged": ""}


# ---- Register --------------------------------------------------------------

# Der RestreamManager. Register und NICHT Alias: er entsteht im Monolithen
# erst weit unten, lange nach dem Import dieses Moduls — ein Alias wäre für
# immer None. Siehe Modul-Kopf.
MGR = {"obj": None}

# Der Restream-Wächter (nc.guard.RestreamGuard). Ebenfalls ein Register und
# kein Alias: es ist eine INSTANZ, kein Container — ein Modul-Global im
# Blueprint wäre eine zweite, leere Instanz mit eigenem Gedächtnis, und
# "warum hat er neu gestartet?" wäre nicht mehr beantwortbar.
GUARD = {"obj": None}


# ---- Haken in den Monolithen ------------------------------------------------
# Was der Bot kann und ein Modul nicht: eine Nachricht nach Discord schicken,
# eine geteilte aiohttp-Session herausgeben, einen Test-Push gegen den echten
# Live-Zustand absichern. Der Bot trägt beim Start ein, die Routen rufen auf.
#
# Wie in nc/azraelstate.py: das ist Kopplung, sie steht hier sichtbar statt
# versteckt im Kontext, dessen 25 Plätze eine andere Frage beantworten.
NOTIFY = {"fn": None}        # async (text, source=None) -> None
AI_SESSION = {"fn": None}    # () -> aiohttp.ClientSession | None
TESTPUSH_LIVE = {"fn": None}  # () -> (darf: bool, grund: str)
SPAWN = {"fn": None}         # (coro, name=...) -> None, feuert auf dem Bot-Loop


def haken(name):
    """Einen registrierten Haken holen, oder None."""
    return {"notify": NOTIFY, "ai_session": AI_SESSION,
            "testpush_live": TESTPUSH_LIVE, "spawn": SPAWN}[name]["fn"]


def guard():
    """Der laufende Wächter, oder None."""
    return GUARD["obj"]


def mgr():
    """Der laufende Manager, oder None. Aufruf statt Direktzugriff, damit ein
       fehlender Manager an EINER Stelle behandelt wird."""
    return MGR["obj"]


def laufende():
    """Die rids der laufenden Relays. Leer, wenn kein Manager da ist —
       nie eine Ausnahme: die Steuerrouten fragen das im Sekundentakt ab."""
    m = MGR["obj"]
    try:
        return sorted((getattr(m, "_procs", {}) or {}).keys()) if m else []
    except Exception:
        return []


def layout_mode() -> str:
    """Das geltende Sendebild-Layout. Unbekanntes fällt auf 'studio' zurück —
       ein erfundener Modus würde den Filtergraph von ffmpeg brechen."""
    m = (LAYOUT.get("mode") or "studio").lower()
    return m if m in ("studio", "burnin") else "studio"
