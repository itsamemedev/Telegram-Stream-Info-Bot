"""nc.loyalty — Belohnungssystem: Punkte + Raenge fuer Stammzuschauer.

Warum getrennt vom Discord-XP:
Das vorhandene discord_xp belohnt Discord-CHAT. Dieses Modul belohnt Stream-
TREUE — wer regelmaessig zuschaut und im Live-Chat aktiv ist, sammelt Punkte,
auch ohne je etwas im Discord zu schreiben. Genau die Stammzuschauer, die die
Wiedererkennung (nc.community) erkennt, werden hier belohnt.

Punkte MUESSEN persistent sein — ein Belohnungssystem, das beim Neustart alles
vergisst, ist wertlos. Deshalb schreibt dieses Modul in eine DB-Tabelle
(loyalty_points), nicht in den RAM. Der Aufrufer injiziert die DB-Funktionen
per configure(), damit das Modul testbar bleibt und nicht selbst DB-Details
kennt.

Punktequellen (der Aufrufer entscheidet, wann er award() ruft):
- Chat-Nachricht im Live (mit Cooldown gegen Spam-Farming)
- Wiederkehr nach Pause (die Wiedererkennung feuert das)
- optional: Anwesenheit pro Stream-Minute (falls der Aufrufer das trackt)

Raenge sind Schwellen auf der Gesamtpunktzahl — konfigurierbar.
"""
import time

# Standard-Raenge: (Mindestpunkte, Name). Aufsteigend.
DEFAULT_RANKS = [
    (0, "Neuling"),
    (100, "Stammgast"),
    (500, "Bekanntes Gesicht"),
    (1500, "Veteran"),
    (5000, "Legende"),
]

_CFG = {
    "enabled": False,
    "chat_points": 1,          # Punkte pro gewerteter Chat-Nachricht
    "chat_cooldown_s": 60,     # fruehestens alle 60s Punkte fuers Chatten
    "return_points": 25,       # Bonus fuer Wiederkehr nach Pause
    "ranks": DEFAULT_RANKS,
}
_chat_cool = {}     # key -> last award ts (Anti-Farming)

# DB-Injektion (vom Aufrufer gesetzt)
_db = {"get": None, "add": None, "top": None}


def configure(db_get=None, db_add=None, db_top=None, **kw):
    """db_get(key)->int, db_add(key, delta, name)->neue_summe, db_top(n)->[(key,name,pts)]."""
    if db_get:
        _db["get"] = db_get
    if db_add:
        _db["add"] = db_add
    if db_top:
        _db["top"] = db_top
    for k, v in kw.items():
        if k in _CFG:
            _CFG[k] = v


def _key(who, platform):
    return f"{platform}:{(who or '').strip().lower()}"


def rank_for(points):
    """Welcher Rang gilt bei dieser Punktzahl? Gibt (name, naechste_schwelle_oder_None)."""
    ranks = _CFG["ranks"]
    name = ranks[0][1]
    nxt = None
    for i, (thr, rname) in enumerate(ranks):
        if points >= thr:
            name = rname
            nxt = ranks[i + 1][0] if i + 1 < len(ranks) else None
        else:
            break
    return name, nxt


def award_chat(who, platform, now=None):
    """Punkte fuer eine Live-Chat-Nachricht, mit Cooldown gegen Farming.
       Gibt None zurueck (kein Aufhebens) oder (neue_summe, rang, aufgestiegen?)
       nur wenn ein Rangaufstieg passierte — damit der Aufrufer den feiern kann."""
    if not (_CFG["enabled"] and _db["add"]):
        return None
    who = (who or "").strip()
    if not who:
        return None
    now = now or time.time()
    k = _key(who, platform)
    if now - _chat_cool.get(k, 0) < _CFG["chat_cooldown_s"]:
        return None
    _chat_cool[k] = now
    return _award(k, who, _CFG["chat_points"])


def award_return(who, platform):
    """Bonus fuer Wiederkehr nach Pause (die Wiedererkennung ruft das)."""
    if not (_CFG["enabled"] and _db["add"]):
        return None
    return _award(_key(who, platform), who, _CFG["return_points"])


def _award(key, name, delta):
    before = _db["get"](key) if _db["get"] else 0
    after = _db["add"](key, delta, name)
    old_rank, _ = rank_for(before)
    new_rank, nxt = rank_for(after)
    if new_rank != old_rank:
        return {"points": after, "rank": new_rank, "leveled_up": True,
                "next_at": nxt, "name": name}
    return {"points": after, "rank": new_rank, "leveled_up": False,
            "next_at": nxt, "name": name}


def leaderboard(n=10):
    """Top-N Stammzuschauer nach Punkten, mit Rang."""
    if not _db["top"]:
        return []
    out = []
    for key, name, pts in _db["top"](n):
        rank, nxt = rank_for(pts)
        out.append({"name": name or key.split(":", 1)[-1], "points": pts,
                    "rank": rank, "next_at": nxt})
    return out


def status():
    return {"enabled": _CFG["enabled"],
            "ranks": [{"at": t, "name": nm} for t, nm in _CFG["ranks"]],
            "chat_points": _CFG["chat_points"],
            "return_points": _CFG["return_points"]}


def enabled() -> bool:
    """v4.1-W26: der Schalter liegt jetzt beim Modul, nicht im Monolithen.

    Als Funktion und nicht als Konstante: .env wird teils erst nach den ersten
    Imports geladen (CLAUDE.md), und der Betreiber schaltet das im Betrieb um.
    Vorgabe ist AUS — ein Punktesystem, das ungefragt anfaengt zu zaehlen,
    will niemand.
    """
    import os
    return (os.getenv("LOYALTY_ENABLED", "0") or "0").strip().lower() in (
        "1", "true", "yes", "on", "y")
