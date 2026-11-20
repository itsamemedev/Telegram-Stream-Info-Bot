"""nc.channels — geteilter Zustand der Eigene-Kanal-Chat-Listener.

Erster Modularisierungsschritt für die W-CHAT-Schicht: der Status-Container und
die Send-Hooks liegen hier zentral, damit Deck-API, Chat-Send, Broadcast und die
Listener-Loops dieselbe Quelle nutzen. Die Loops selbst bleiben (vorerst) in
bot.py; sie schreiben in diese Register. Kein Verhalten ändert sich.
"""

# Live-Status pro Plattform (von den Listener-Loops gepflegt, von Deck/Dashboard
# gelesen). reconnects/since dienen der Stabilitäts-Metrik.
WCHAT_STATUS = {
    "twitch":  {"connected": False, "mode": "aus", "last_msg": 0.0,
                "error": "", "reconnects": 0, "since": 0.0},
    "youtube": {"connected": False, "mode": "aus", "last_msg": 0.0,
                "error": "", "reconnects": 0, "since": 0.0},
}

# Send-Hooks: von den Loops gesetzt (sendefähige Verbindung), von Chat-Send/
# Broadcast aufgerufen. None = nicht sendefähig.
TWITCH_SEND = {"fn": None}

# v4.1-W9: Register für den laufenden Kick-Moderator. Die KickModerator-Klasse
# bleibt im Monolithen (Welle 4), aber drei Blueprints müssen die INSTANZ
# erreichen: /api/kick, /api/kickmod und /api/chat.
#
# Warum ein Register und kein nc.ctx-Slot: der Kontext ist keine Sammelstelle,
# und ein Dict neben TWITCH_SEND/YT_SEND ist dasselbe Muster wie dort — der Bot
# trägt ein, die Leser lesen.
#
# Warum überhaupt: im Monolithen stand dafür `globals().get("_KICK_MOD")`. In
# einem Blueprint ist globals() der Namensraum DES BLUEPRINTS — der Ausdruck
# wäre dort für immer None, und /api/kick/sendcheck meldete "Kick-Moderator
# läuft nicht", während er läuft. Genau die stille Fehlanzeige aus W116
# (_MAIN_LOOP) und aus CLAUDE.md.
KICK_MOD = {"obj": None}

# v4.1-W18: Register für den PRIMÄREN Restream (zuletzt gestartet) —
# {"user","label","rid"} oder leer. Der Quell-Streamer, dessen Bild gerade
# gesendet wird; das Overlay, die Chat-Weiche und das SENTINEL-Panel hängen
# daran.
#
# Register und NICHT Alias, obwohl es ein Dict ist: bot.py bindet den Namen bei
# jeder Primär-Nachfolge komplett NEU (früher `globals()["_RESTREAM_ACTIVE"] =
# {...}`). Ein Alias zeigte danach auf das alte, tote Dict — die Blueprints
# meldeten den zuvor gesendeten User, während längst ein anderer läuft. Genau
# die Falle aus CLAUDE.md ("Guards als Objekt-Attribut").
RESTREAM_ACTIVE = {"obj": {}}

# v4.1-W20: laufende AZRAEL-Stimmkanäle je Restream — rid -> {thread, stop,
# fifo, queue}. Alias und nicht Register: bot.py trägt ein und nimmt heraus,
# bindet den Namen aber nie neu. /api/audio/testtone legt den Signalton in
# genau diese Warteschlangen, damit er im LIVE-Mix hörbar ist statt nur lokal.
RESTREAM_TTS = {}


def restream_active():
    """Der primäre Restream als Dict — nie None, damit .get() immer trägt."""
    return RESTREAM_ACTIVE["obj"] or {}
YT_SEND = {"fn": None, "token": "", "token_exp": 0.0,
           "live_chat_id": "", "lcid_exp": 0.0}


# ---- Studio-Chat-Puffer (V37 Welle 3): shared Container + Renderer ----------
import collections as _collections
import threading as _threading
from nc.textutil import clean_username

RESTREAM_CHAT = _collections.deque(maxlen=160)   # shared: Bot schreibt, Renderer liest
# BH-10: wer den Ring VERAENDERT, nimmt diese Sperre — chat_anhaengen() im
# Chat-Arbeiter (Thread "chatpush") und chat_ausduennen() im Restream-Start
# (Event-Loop). Vorher iterierte der Start per Listen-Abstraktion ueber den
# Ring, waehrend der Arbeiter anhaengte: entweder „deque mutated during
# iteration" (still gefangen, Filter lief nicht) oder die Nachrichten
# zwischen Abzug und clear()/extend() waren weg. Lesen per list(RING) ist
# ohne Sperre sicher — die Kopie entsteht in C, ohne Thread-Wechsel.
CHAT_SPERRE = _threading.Lock()

# Die eigenen Kanaele: ihre Zeilen laufen in JEDEM Kasten mit (V37-P6), auch
# ihre Ereignisse (src="event", kanal=...). TikTok gehoert nicht dazu — das
# ist die Quelle des jeweiligen Restreams.
EIGENE_KANAELE = ("kick", "twitch", "youtube")


def _schluessel(name) -> str:
    """Vergleichsform eines TikTok-Namens. Ohne Gross-/Kleinschreibung:
    TikTok unterscheidet sie nicht, und der Name kommt je nach Weg aus der
    Datenbank („Name"), aus dem Listener („name") oder aus der Adresse des
    Kastens."""
    return clean_username(name or "").lower()


def gehoert_in_kasten(m, source_user) -> bool:
    """Gehoert dieser Ring-Eintrag in den Chat-Kasten des Restreams von
    `source_user`? EINE Regel fuer beide Renderer — chat_eintraege()
    (Chromium-Kasten) und _chat_block() (drawtext) — und fuer das
    Ausduennen beim Restream-Start.

    BH-7: die beiden Renderer hatten zwei Lesarten. chat_eintraege()
    verglich ohne, _chat_block() MIT Gross-/Kleinschreibung; stand der Name
    in der Datenbank als „Name" und kam aus dem Listener als „name", war der
    gebrannte Studio-Kasten leer, waehrend der Chromium-Kasten lief.

    Ohne source_user: alles (es gibt nichts, wonach zu filtern waere)."""
    if not source_user:
        return True
    if m.get("src") in EIGENE_KANAELE or m.get("kanal") in EIGENE_KANAELE:
        return True
    su = _schluessel(source_user)
    return bool(su) and _schluessel(m.get("origin")) == su


def quelle_aktiv(origin, quellen) -> bool:
    """Stammt `origin` aus einer der laufenden Restream-Quellen? Dieselbe
    Vergleichsform wie gehoert_in_kasten() — der Einlass in den Ring darf
    nicht strenger sein als der Kasten, sonst kommt eine Zeile, die der
    Kasten zeigen wuerde, gar nicht erst an."""
    o = _schluessel(origin)
    return bool(o) and o in {_schluessel(q) for q in quellen}


def chat_anhaengen(eintrag):
    """Einen Eintrag an den Ring haengen — unter CHAT_SPERRE (BH-10)."""
    with CHAT_SPERRE:
        RESTREAM_CHAT.append(eintrag)


def letzte_zeit() -> float:
    """Zeitstempel der juengsten Ring-Zeile, 0.0 ohne. Ueber eine Kopie statt
    `ring[-1]["ts"] if ring else 0.0`: zwischen Pruefung und Zugriff kann
    chat_ausduennen() die letzte Zeile entfernen — ein IndexError im
    Avatar-Takt, und der stand bis BH-9 in einem stillen except."""
    kopie = list(RESTREAM_CHAT)
    return kopie[-1]["ts"] if kopie else 0.0


def chat_ausduennen(quellen) -> int:
    """TikTok-Eintraege, die in KEINEN Kasten der laufenden Quellen gehoeren,
    aus dem Ring werfen. -> Zahl der entfernten.

    Fuer das Sendebild waere das nicht mehr noetig — beide Renderer filtern
    seit V37-P6 je Quelle. Gebraucht wird es fuer den Studio-Monitor im Deck
    (/api/restream/chatfeed), der den Ring ungefiltert zeigt: ohne das
    stuenden dort nach einem Quellenwechsel die Chats des vorigen Nutzers.

    BH-10: atomar gegen chat_anhaengen(), und OHNE leeren Zwischenstand.
    Ein clear() mit anschliessendem extend() liess den Ring fuer einen
    Augenblick leer — wer genau dann las (Overlay-Schreiber, Avatar-Takt),
    sah keinen Chat. `del ring[i]` von hinten nimmt nur die fremden heraus;
    jeder Zwischenstand ist eine Teilmenge in der richtigen Reihenfolge."""
    # Ein Name, der sich leer bereinigt („@"), ist keine Quelle: auf ihn passte
    # keine TikTok-Zeile, und der Ring verloere den Chat der laufenden.
    quellen = [q for q in quellen if _schluessel(q)]
    weg = []
    if quellen:
        with CHAT_SPERRE:
            weg = [i for i, m in enumerate(RESTREAM_CHAT)
                   if not any(gehoert_in_kasten(m, q) for q in quellen)]
            for i in reversed(weg):
                del RESTREAM_CHAT[i]
    return len(weg)
# v4.1-W23: Zuschauer-Stichproben (ts, count) der letzten ~12 h bei 60-s-Takt.
# /metrics und der Verlaufs-Graph lesen sie, der Status-Loop schreibt sie.
# maxlen ist die Bremse: ohne sie waere das ein Leck, das erst nach Tagen
# auffaellt — dieselbe Ueberlegung wie bei den Ringpuffern in nc/brainstate.py.
VIEWER_SAMPLES = _collections.deque(maxlen=720)
_CHAT_LINES = 14
_CHAT_WIDTH = 62


def configure_chat(lines=None, width=None):
    global _CHAT_LINES, _CHAT_WIDTH
    if lines is not None: _CHAT_LINES = int(lines)
    if width is not None: _CHAT_WIDTH = int(width)


def chat_eintraege(anzahl=None, source_user=None):
    """Die juengsten Chat-Eintraege fuer EIN Sendebild, als Daten.

    v5.9-W205: fuer den Chat-Kasten, den Chromium zeichnet (Emoji farbig).
    Derselbe Filter wie _chat_block: Kick, Twitch und YouTube sind der eigene
    Kanal und laufen ueberall mit, TikTok nur aus der Quelle dieses Restreams
    (V37-P6) — sonst stuenden fremde Chats im Sendebild."""
    items = [m for m in list(RESTREAM_CHAT) if gehoert_in_kasten(m, source_user)]
    n = int(anzahl or _CHAT_LINES)
    return [{"src": m.get("src") or "", "who": m.get("who") or "", "text": m.get("text") or ""}
            for m in items[-n:]]


def _chat_block(maxlines=None, width=None, source_user=None):
    # V37-P6: source_user filtert den globalen Ring auf EINE Restream-Quelle
    # (Kick-Zeilen laufen überall mit — eigener Kanal). Nötig, seit P5b
    # mehrere TikTok-Quellen parallel in den Ring dürfen: ohne Filter
    # stünden fremde Quell-Chats im Studio-Panel des jeweils anderen Streams.
    """Baut den Panel-Text: pro Nachricht Icon + Name + Text, wortumbrochen mit
       hängendem Einzug — die JÜNGSTEN Zeilen unten, gekappt auf maxlines."""
    maxlines = maxlines or _CHAT_LINES
    width = width or _CHAT_WIDTH
    icon = {"tiktok": "\u25b8", "kick": "\u25cf", "event": "\u25c6"}
    indent_marke = "    "     # v4.2-W54: kennzeichnet eine Fortsetzungszeile
    dot = "\u00b7"
    out = []
    # BH-7: dieselbe Regel wie chat_eintraege() — vorher hier MIT Gross-/
    # Kleinschreibung, dort ohne; „Name" aus der Datenbank gegen „name" aus
    # dem Listener liess nur diesen Kasten leer.
    _items = [m for m in list(RESTREAM_CHAT) if gehoert_in_kasten(m, source_user)]
    for m in _items[-maxlines:]:
        head = f"{icon.get(m['src'], dot)} {m['who']}  "
        body = m["text"]
        avail = max(16, width - len(head))
        first, rest = body[:avail], body[avail:]
        # sauberer Wortbruch statt harter Kante
        if rest and " " in first:
            cut = first.rfind(" ")
            rest = first[cut + 1:] + rest
            first = first[:cut]
        out.append(head + first)
        indent = "    "
        while rest:
            avail2 = max(16, width - len(indent))
            seg, rest = rest[:avail2], rest[avail2:]
            if rest and " " in seg:
                cut = seg.rfind(" ")
                rest = seg[cut + 1:] + rest
                seg = seg[:cut]
            out.append(indent + seg)
            if len(out) > maxlines * 3:      # Notbremse gegen Endlos-Wraps
                break
    # v4.2-W54: der Schnitt auf maxlines darf nicht mitten in einer Nachricht
    # landen. Vorher stand oben im Panel regelmaessig eine nackte
    # Fortsetzungszeile ("    gleiche Frisur") ohne Namen davor — im
    # Sendebild sieht das aus wie ein Textfehler, nicht wie ein Umbruch.
    # Also vorne so lange Fortsetzungszeilen wegwerfen, bis die erste Zeile
    # wieder eine mit Absender ist.
    rest_zeilen = out[-maxlines:]
    while rest_zeilen and rest_zeilen[0].startswith(indent_marke):
        rest_zeilen.pop(0)
    return "\n".join(rest_zeilen)


# ---- YouTube: Kontingent-Cache und Sende-Bremse (v4.1-W8) -------------------
# Beide lagen als Modul-Globals in bot.py und waeren beim Herausloesen von
# /api/youtube zu drei nc.ctx-Eintraegen geworden — obwohl sie reiner geteilter
# Zustand sind, genau wie YT_SEND daneben. Der Kontext steht bei 24 von
# vertraglich 25 Slots; die Reihenfolge aus W117 lautet deshalb: erst den
# Zustand loesen, dann die Routen.

# B120: eigener Cache fuer den API-Kanalstatus. Die YouTube Data API hat
# ein TAGES-Kontingent (10.000 Einheiten); der Control-Tab pollt alle 20s.
# Ohne diesen Cache waere das Kontingent vor Mittag verbrannt und die API
# antwortet bis Mitternacht nur noch mit 403 quotaExceeded.
YT_API_CACHE = {"ts": 0.0, "data": None}

from nc import sendrate as _sendrate           # noqa: E402 — Blockgrenze, siehe oben
from nc import cfgnorm as _cfgnorm             # noqa: E402
from nc.cfgstore import get as _cfg_get        # noqa: E402

YT_SENDRATE = _sendrate.new_state()    # v4.0-W23: Zustand der YT-Sende-Bremse


def yt_sendrate_cfg():
    # v4.0-W33: Normalisierung nach nc/cfgnorm.py (bitgenau geprüft).
    return _cfgnorm.normalize_sendrate(_cfg_get("youtube.sendrate", None))
