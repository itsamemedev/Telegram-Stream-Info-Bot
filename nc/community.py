"""nc.community — Community-Ausbau: Discovery-Loop.

Drei zusammenspielende Bausteine, jeder einzeln abschaltbar:

1. RETURNING (Stammzuschauer-Wiedererkennung): merkt sich, wer schon einmal im
   Chat war, und meldet beim Wiederkommen "X ist zurueck". Baut Bindung — die
   Leute fuehlen sich erkannt.

2. HIGHLIGHT-SHARE: wenn ein Clip die Highlight-Schwelle reisst, liefert dieses
   Modul den fertigen, teilbaren Discord-Post (Titel + Aufruf + Platz fuer Link).
   Der eigentliche Reichweiten-Motor — jeder geteilte Clip bringt neue Zuschauer.

3. LIVE-PING: baut die "geht live"-Ankuendigung fuer Discord mit Rollen-Ping,
   damit die bestehende Community mitkriegt, dass gestreamt wird.

Dieses Modul baut nur die INHALTE/Logik (was gemeldet wird, wer neu/bekannt ist)
— das tatsaechliche Senden an Discord macht der Aufrufer mit seinem vorhandenen
Webhook. So bleibt das Modul testbar ohne Netzwerk.
"""
import time

# --- 1. Wiedererkennung ---------------------------------------------------

# who(lower)+platform -> {"first": ts, "last": ts, "count": n}
_SEEN = {}
_RECENT_GREET = {}      # Cooldown gegen Doppelbegruessung pro Session
_CFG = {
    "returning_enabled": False,
    "returning_min_gap_s": 3600,     # erst nach dieser Pause gilt jemand als "zurueck"
    "returning_greet_cooldown_s": 21600,   # pro Person hoechstens alle 6h begruessen
    "returning_min_visits": 2,       # ab dem wievielten Besuch begruesst wird
    "live_role_id": "",              # Discord-Rollen-ID fuer den Live-Ping
    "highlight_channel": "",         # optionaler eigener Webhook fuer Highlights
}


def configure(**kw):
    for k, v in kw.items():
        if k in _CFG:
            _CFG[k] = v


def note_chatter(who, platform, now=None):
    """Einen Chatter registrieren. Gibt eine Begruessung zurueck, wenn die Person
       ein wiederkehrender Stammgast ist (nach Pause zurueck) — sonst None.

       Bewusst konservativ: erst ab N Besuchen, nach echter Pause, mit Cooldown.
       So wird nicht jeder Erstbesucher und nicht jede Nachricht bejubelt."""
    if not _CFG["returning_enabled"]:
        return None
    who = (who or "").strip()
    if not who:
        return None
    now = now or time.time()
    key = f"{platform}:{who.lower()}"
    rec = _SEEN.get(key)
    greet = None
    if rec is None:
        _SEEN[key] = {"first": now, "last": now, "count": 1}
    else:
        gap = now - rec["last"]
        rec["last"] = now
        # nur als neuer "Besuch" zaehlen, wenn echte Pause dazwischen lag
        if gap >= _CFG["returning_min_gap_s"]:
            rec["count"] += 1
            if (rec["count"] >= _CFG["returning_min_visits"]
                    and now - _RECENT_GREET.get(key, 0) >= _CFG["returning_greet_cooldown_s"]):
                _RECENT_GREET[key] = now
                greet = _returning_line(who, rec["count"])
    # Speicher deckeln
    if len(_SEEN) > 5000:
        oldest = sorted(_SEEN.items(), key=lambda kv: kv[1]["last"])[:2000]
        for k, _ in oldest:
            _SEEN.pop(k, None)
            _RECENT_GREET.pop(k, None)
    return greet


def _returning_line(who, visits):
    if visits >= 10:
        return f"\U0001F525 {who} ist wieder da \u2014 echter Stammgast! (Besuch #{visits})"
    if visits >= 5:
        return f"\u2728 Willkommen zur\u00fcck, {who}! Sch\u00f6n dass du wieder dabei bist."
    return f"\U0001F44B {who} ist zur\u00fcck \u2014 willkommen wieder!"


def seen_stats():
    """Fuers Dashboard: wie viele Leute kennt der Bot, wie viele Stammgaeste?"""
    total = len(_SEEN)
    regulars = sum(1 for r in _SEEN.values() if r["count"] >= _CFG["returning_min_visits"])
    return {"known": total, "regulars": regulars}


# --- 2. Highlight-Share ---------------------------------------------------

def highlight_post(username, clip_url=None, stars=None):
    """Der teilbare Discord-Post fuer einen Highlight-Clip. clip_url optional —
       ohne wird ein Platzhalter gesetzt, den der Aufrufer fuellt."""
    star_txt = f" ({stars}\u2b50)" if stars else ""
    body = [f"\U0001F3AC **Neuer Highlight-Clip von @{username}**{star_txt}"]
    if clip_url:
        body.append(clip_url)
    body.append("\u25B6 Teilt den Clip gerne \u2014 jede geteilte Sekunde bringt "
                "neue Leute in den Stream! \U0001F680")
    return "\n".join(body)


# --- 3. Live-Ping ---------------------------------------------------------

def live_ping(streamer, platforms=None, title=None):
    """Die 'geht live'-Ankuendigung fuer Discord, mit optionalem Rollen-Ping."""
    role = _CFG["live_role_id"]
    ping = f"<@&{role}> " if role else ""
    plats = ""
    if platforms:
        plats = " \u2014 jetzt auf " + ", ".join(platforms)
    line = f"{ping}\U0001F534 **{streamer} ist LIVE!**{plats}"
    if title:
        line += f"\n> {title}"
    line += "\n\U0001F449 Kommt vorbei und sagt Hallo!"
    return line


# v4.1-W26: die drei Schalter liegen jetzt beim Modul. Als Funktionen und
# nicht als Konstanten: .env wird teils erst nach den ersten Imports geladen
# (CLAUDE.md). Vorgabe ist ueberall AUS — jede dieser Funktionen schreibt in
# einen fremden Kanal, und das faengt nicht ungefragt an.

def _flag(name) -> bool:
    import os
    return (os.getenv(name, "0") or "0").strip().lower() in (
        "1", "true", "yes", "on", "y")


def returning_enabled() -> bool:
    return _flag("COMMUNITY_RETURNING_ENABLED")


def live_ping_enabled() -> bool:
    return _flag("COMMUNITY_LIVE_PING_ENABLED")


def highlight_share_enabled() -> bool:
    return _flag("COMMUNITY_HIGHLIGHT_SHARE_ENABLED")
