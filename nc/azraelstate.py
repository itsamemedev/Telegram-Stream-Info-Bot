"""nc.azraelstate — v4.1-W19: AZRAELs Laufzeitzustand, geteilt statt injiziert.

════════════════════════════════════════════════════════════════════════
WARUM DIESES MODUL
════════════════════════════════════════════════════════════════════════
Die achtzehn Routen unter `/api/azrael` lesen und schreiben acht
Zustands-Container des Bots. Als nc.ctx-Eintraege waeren das acht der 25
vertraglich erlaubten Plaetze — bei 24 belegten schlicht nicht vorhanden.

Der Kontext ist auch der falsche Ort dafuer. `nc.ctx` ist eine
Injektionsstelle fuer FAEHIGKEITEN, die nur der Monolith hat (den Bot-Loop
antreiben, eine Aufnahme starten). Diese acht sind etwas anderes: **geteilter
Zustand**, den Bot und Oberflaeche gemeinsam sehen muessen. Genau wie
WCHAT_STATUS und RESTREAM_CHAT in nc/channels.py.

Alle acht sind **Aliase**, nicht Register: bot.py bindet keinen dieser Namen
je neu, es veraendert sie nur an Ort und Stelle (`.update`, `[k] = v`,
`.append`, `.pop`). Ein Alias trifft damit immer dasselbe Objekt. Waere auch
nur einer davon neu gebunden worden, zeigte der Alias danach auf eine tote
Kopie — die Oberflaeche zeigte einen eingefrorenen Stand, ohne Fehler. Deshalb
haelt ein Vertrag fest, dass hier nichts neu gebunden wird.

Die drei HAKEN am Ende sind die Gegenrichtung und die ehrliche Kehrseite: sie
sind Kopplung, nur an einer sichtbaren Stelle statt im Kontext. Sie bleiben
absichtlich wenige und benannt — dasselbe Muster wie TWITCH_SEND/YT_SEND.
"""

import collections
import os

# ---- Geteilter Zustand (Aliase) --------------------------------------------

# Overlay-Konfiguration: Titel, Spendenziel, Stimme. Der Bot fuellt sie beim
# Start aus .env (OVERLAY.update(...)), Dashboard und Overlay-Routen aendern
# sie zur Laufzeit. Absichtlich leer angelegt: die .env-Aufloesung bleibt im
# Bot, wo sie steht — ein configure() waere hier nur eine zweite Baustelle.
OVERLAY = {}

# Was der Betreiber AZRAEL als Stream-Kontext mitgibt ("worum geht es gerade").
CONTEXT = {"text": "", "ts": 0.0}

# Die zuletzt erzeugte Live-Reaktion — das Overlay pollt sie und zeigt sie an.
REACTION = {"ts": 0.0, "statement": "", "text": "", "active": False,
            "audio": "", "source": "", "emotion": "neutral"}

# V7: globales Aufruf-Budget. Zeitstempel der letzten KI-Aufrufe; alles aelter
# als 60 s faellt vorne raus. maxlen ist die zweite Bremse — ohne sie wuechse
# die Deque bei einem klemmenden Abraeumer unbegrenzt.
CALL_TS = collections.deque(maxlen=300)

# Reaction-Engine zur Laufzeit angehalten? Ein Dict statt eines bool, damit es
# ueberhaupt teilbar ist — ein nackter bool waere eine Kopie.
LIVE_PAUSED = {"v": False}

# username -> [{"ts","text"}]: was Whisper gerade hoert, juengstes zuletzt.
TRANSCRIPT = {}

# username -> {"stop": Event, "task": Task} der laufenden Live-React-Worker.
WORKERS = {}

# Die Rollen, in denen AZRAEL auftritt. Fest, aber hier statt im Monolithen:
# /api/azrael/agents liefert sie unveraendert ans Dashboard.
AGENTS = {}

# v4.1-W20: ISO-Zeitstempel des aktuellen Stream-Starts. Die Spendensumme im
# Overlay zaehlt erst ab hier — die Historie bleibt vollstaendig in der DB.
# Alias wie die uebrigen: bot.py setzt nur `["start"] = …`, bindet nie neu.
OVERLAY_SESSION = {"start": None}


# ---- Haken in den Monolithen ------------------------------------------------
# Was der Bot kann und ein Modul nicht: eine Coroutine auf dem Bot-Loop
# ausfuehren, die an ai_chat, am Overlay-Ton und am Restream-Mischer haengt.
# Der Bot traegt beim Start ein, die Routen rufen auf.
#
# Das ist Kopplung — sie steht hier, damit man sie SIEHT, statt sie im Kontext
# zu verstecken, dessen 25 Plaetze eine andere Frage beantworten. Drei Haken,
# jeder benannt, jeder mit genau einem Aufrufer.
SAY = {"fn": None}          # async (text, rate=None, source_user=None) -> URL|None
CHAT = {"fn": None}         # async (purpose, content, ...) -> (text, err)
LIVE_STATE = {"fn": None}   # () -> str: was NIGHTCRAWLER gerade tut
PUSH = {"fn": None}         # (kind, name, amount, message, platform) -> None


def haken(name):
    """Einen registrierten Haken holen, oder None. Aufruf statt Direktzugriff,
       damit ein fehlender Haken an EINER Stelle behandelt wird."""
    return {"say": SAY, "chat": CHAT, "live_state": LIVE_STATE,
            "push": PUSH}[name]["fn"]


def flag(name, default="0") -> bool:
    """.env-Schalter bei jedem Aufruf lesen, nie als Modul-Konstante einfrieren
       (CLAUDE.md: .env laedt teils erst nach den ersten Imports)."""
    return (os.getenv(name, default) or "").strip().lower() in (
        "1", "true", "yes", "on", "y")


# ---- Pro-Streamer-Persona (auf Platte) --------------------------------------
# username -> eigener AZRAEL-Persona-Text. Gehoert hierher und nicht in ein
# eigenes Modul: es IST AZRAEL-Zustand, nur eben persistent. Geschrieben wird
# ueber eine Zwischendatei und os.replace — wie bei nc/badwords.py, aus
# demselben Grund: eine halb geschriebene Datei laedt beim naechsten Start als
# leer, und AZRAEL spraeche ploetzlich fuer alle Streamer gleich.

_PFAD = {"recordings_dir": "."}


def configure(*, recordings_dir):
    _PFAD["recordings_dir"] = str(recordings_dir or ".")


def personas_path() -> str:
    return os.path.join(_PFAD["recordings_dir"], "streamer_personas.json")


def personas_load():
    import json
    try:
        with open(personas_path(), "r", encoding="utf-8") as f:
            d = json.load(f)
        return d if isinstance(d, dict) else {}
    except (FileNotFoundError, json.JSONDecodeError, OSError, ValueError):
        return {}


def personas_save(d):
    import json
    try:
        os.makedirs(_PFAD["recordings_dir"], exist_ok=True)
        tmp = personas_path() + ".tmp"
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(dict(d), f, ensure_ascii=False, indent=2)
        os.replace(tmp, personas_path())
        return True
    except OSError:
        return False
