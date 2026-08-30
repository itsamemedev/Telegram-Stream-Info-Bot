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
YT_SEND = {"fn": None, "token": "", "token_exp": 0.0,
           "live_chat_id": "", "lcid_exp": 0.0}


# ---- Studio-Chat-Puffer (V37 Welle 3): shared Container + Renderer ----------
import collections as _collections
from nc.textutil import clean_username

RESTREAM_CHAT = _collections.deque(maxlen=160)   # shared: Bot schreibt, Renderer liest
_CHAT_LINES = 14
_CHAT_WIDTH = 62


def configure_chat(lines=None, width=None):
    global _CHAT_LINES, _CHAT_WIDTH
    if lines is not None: _CHAT_LINES = int(lines)
    if width is not None: _CHAT_WIDTH = int(width)


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
    dot = "\u00b7"
    out = []
    _items = list(RESTREAM_CHAT)
    if source_user:
        _su = clean_username(source_user)
        _items = [m for m in _items
                  if m.get("src") in ("kick", "twitch", "youtube")
                  or (m.get("origin") or "") == _su]
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
    return "\n".join(out[-maxlines:])


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
