"""nc.modheuristics — B165: plattformunabhängige Chat-Moderations-Heuristik.

════════════════════════════════════════════════════════════════════════
WARUM DIESES MODUL
════════════════════════════════════════════════════════════════════════
Die schnelle Spam-Heuristik (CAPS/Link/Mention/Flood/Repeat) und die
Eskalations-Leiter steckten bislang INNEN in bot_v37.KickModerator — also fest
an Kick gebunden. Genau deshalb moderiert der volle KI-Moderator nur auf Kick:
die Logik war nicht wiederverwendbar. Hier liegt sie jetzt als REINE Funktionen
ohne Bot-Zustand, ohne Netz, ohne Plattformbezug. Der Kick-Moderator ruft sie
auf; ein späterer Twitch-/YouTube-Moderator kann exakt dieselben Regeln nutzen,
statt sie zu duplizieren.

Was BEWUSST im Bot bleibt: _detect_foreign_ad (hängt an der Streamer-eigenen
Allowlist/Invite-Liste) und der gesamte Zustand (Nachrichtenverlauf pro User,
Infraktionszähler). Dieses Modul entscheidet nur anhand übergebener Werte —
so ist das Moderationsverhalten vollständig testbar und bitgenau reproduzierbar.
"""

import re

_LINK_RE = re.compile(r"https?://|www\.", re.I)


def caps_ratio(text: str):
    """(Großbuchstaben-Anteil, Buchstabenzahl). Nur Buchstaben zählen."""
    letters = [ch for ch in (text or "") if ch.isalpha()]
    if not letters:
        return 0.0, 0
    up = sum(1 for ch in letters if ch.isupper())
    return up / max(1, len(letters)), len(letters)


def is_caps_spam(text: str, *, max_ratio: float = 0.7, min_letters: int = 10) -> bool:
    """CAPS-Spam erst ab min_letters Buchstaben UND Anteil >= max_ratio
       (identisch zur bisherigen Inline-Prüfung im KickModerator)."""
    ratio, n = caps_ratio(text)
    return n >= min_letters and ratio >= float(max_ratio)


def count_links(text: str) -> int:
    return len(_LINK_RE.findall(text or ""))


def count_mentions(text: str) -> int:
    return (text or "").count("@")


def stateless_reason(text: str, *, max_caps_ratio: float = 0.7, max_links: int = 2,
                     max_mentions: int = 5, min_caps_letters: int = 10):
    """Zustandslose Spam-Gründe in EXAKT der bisherigen Reihenfolge:
       CAPS → Link → Mention. Gibt den Grund-String zurück, sonst None.
       (Fremdwerbung wird davor separat im Bot geprüft — Allowlist-abhängig.)"""
    if is_caps_spam(text, max_ratio=max_caps_ratio, min_letters=min_caps_letters):
        return "CAPS-Spam"
    if count_links(text) > int(max_links):
        return "Link-Spam"
    if count_mentions(text) > int(max_mentions):
        return "Mention-Spam"
    return None


def flood_reason(recent_lowers, current_lower, *, flood_max: int = 5, repeat_min: int = 3):
    """recent_lowers = die jüngsten Nachrichten (lowercase) im Flood-Zeitfenster,
       inklusive der aktuellen. Reihenfolge wie bisher: erst Flood, dann Repeat.
         Flood       : mehr als flood_max Nachrichten im Fenster
         Repeat-Spam : dieselbe Nachricht >= repeat_min mal
       Der Zeitfenster-/Verlaufszustand bleibt beim Aufrufer (plattformabhängig)."""
    if len(recent_lowers) > int(flood_max):
        return "Flood"
    if sum(1 for m in recent_lowers if m == current_lower) >= int(repeat_min):
        return "Repeat-Spam"
    return None


def escalation_minutes(infraction_n: int, *, cap: int, first: int = 1, second: int = 5) -> int:
    """Eskalierende Timeout-Dauer, gedeckelt durch cap. Leiter [first, second, cap]:
       1. Verstoß → first, 2. → second, ab 3. → cap. infraction_n ist 1-basiert.
       (Identisch zur bisherigen KickModerator-Leiter [1, 5, cap].)"""
    ladder = [first, second, cap]
    return min(cap, ladder[min(int(infraction_n), len(ladder)) - 1])

def prune_history(hist, now, window_s, max_users=5000):
    """v4.0-W14 (Audit): haelt die Flood-Historie klein. Die Listen wurden zwar
       nach Zeit gekuerzt, der SCHLUESSEL pro Chatter blieb aber fuer immer im
       Dict — in einem 24/7-Prozess ein stetig wachsendes Speicherleck.
       Entfernt leere Eintraege und deckelt notfalls die Anzahl der Nutzer
       (aeltester Eintrag zuerst). Gibt die Anzahl entfernter Schluessel zurueck."""
    if not isinstance(hist, dict) or not hist:
        return 0
    removed = 0
    for key in [k for k, v in hist.items() if not v]:
        hist.pop(key, None)
        removed += 1
    if len(hist) > max_users:
        def _newest(item):
            v = item[1]
            try:
                return max(t for (t, _m) in v)
            except (ValueError, TypeError):
                return 0
        for key, _v in sorted(hist.items(), key=_newest)[:len(hist) - max_users]:
            hist.pop(key, None)
            removed += 1
    return removed

# ── v4.0-W16: Rollen-Erkennung, damit die Auto-Moderation NICHT das eigene
# Team trifft. Bisher wurden Twitch-/Kick-Badges gar nicht ausgewertet: ein
# Moderator (oder der Broadcaster selbst) mit einem Link oder GROSSSCHRIFT
# kassierte einen Timeout vom eigenen Bot. YouTube war bereits ausgenommen.

#: Rollen, die standardmaessig von der Auto-Moderation ausgenommen sind.
DEFAULT_EXEMPT = ("broadcaster", "moderator", "staff", "admin")


def twitch_roles(tags):
    """Rollen aus den IRC-Tags (CAP twitch.tv/tags). tags = dict."""
    roles = set()
    if not isinstance(tags, dict):
        return roles
    if str(tags.get("mod", "")).strip() == "1":
        roles.add("moderator")
    badges = (tags.get("badges") or "")
    for chunk in badges.split(","):
        name = chunk.split("/", 1)[0].strip().lower()
        if not name:
            continue
        if name in ("broadcaster", "moderator", "vip", "staff", "admin",
                    "global_mod", "subscriber", "founder", "partner"):
            roles.add("global_mod" if name == "global_mod" else name)
    if (tags.get("user-type") or "").strip().lower() in ("mod", "staff", "admin", "global_mod"):
        roles.add("moderator")
    return roles


def kick_roles(sender_obj):
    """Rollen aus dem Kick-Chat-Payload (sender.identity.badges)."""
    roles = set()
    if not isinstance(sender_obj, dict):
        return roles
    identity = sender_obj.get("identity") or {}
    for badge in (identity.get("badges") or []):
        if isinstance(badge, dict):
            t = (badge.get("type") or badge.get("text") or "").strip().lower()
        else:
            t = str(badge).strip().lower()
        if not t:
            continue
        if t in ("broadcaster", "owner", "host"):
            roles.add("broadcaster")
        elif t in ("moderator", "mod"):
            roles.add("moderator")
        elif t in ("vip", "og", "founder"):
            roles.add(t)
        elif "sub" in t:
            roles.add("subscriber")
        elif t in ("staff", "admin", "verified"):
            roles.add(t)
    return roles


def is_exempt(roles, exempt=DEFAULT_EXEMPT):
    """True, wenn eine der Rollen von der Auto-Moderation ausgenommen ist."""
    if not roles:
        return False
    ex = {str(r).strip().lower() for r in (exempt or ()) if str(r).strip()}
    return bool({str(r).strip().lower() for r in roles} & ex)


def resolve_exempt(cfg, env_value=None):
    """v4.0-W62d: Die Ausnahme-Rollen bestimmen (Config-Auflösung, aus bot_v37
       gelöst). Reihenfolge: cfg['exempt_roles'] (nur wenn cfg ein dict ist), sonst
       env_value, sonst DEFAULT_EXEMPT. Ein String wird an Komma/Whitespace
       gesplittet. os.getenv bleibt beim Aufrufer (env_value wird injiziert)."""
    cfgv = cfg.get("exempt_roles") if isinstance(cfg, dict) else None
    if not cfgv:
        cfgv = env_value or None
    if isinstance(cfgv, str):
        cfgv = [x.strip() for x in cfgv.replace(",", " ").split() if x.strip()]
    return cfgv or DEFAULT_EXEMPT

def escalation_step(infraction_n, *, cap, first=1, second=5, warn_first=True):
    """v4.0-W19: Was passiert beim n-ten Verstoss? ("warn", 0) oder ("timeout", min).

    Bisher gab es beim ERSTEN Verstoss sofort einen Timeout. Eine oeffentliche
    Verwarnung davor ist fairer und beendet die meisten Faelle schon — erst der
    Wiederholungstaeter wird stummgeschaltet. Mit warn_first=False bleibt das
    alte Verhalten exakt erhalten.
    """
    n = max(1, int(infraction_n))
    if warn_first and n == 1:
        return ("warn", 0)
    # Nach der Verwarnung faengt die Timeout-Leiter bei ihrer ersten Stufe an.
    step = n - 1 if warn_first else n
    return ("timeout", escalation_minutes(step, cap=cap, first=first, second=second))


def prune_infractions(infractions, now, ttl_s=3600, max_users=5000):
    """v4.0-W19: gleiche Leck-Klasse wie prune_history — die Verstoss-Zaehler
       verjaehren zwar inhaltlich, der SCHLUESSEL pro Nutzer blieb aber fuer
       immer im Dict. Entfernt abgelaufene Eintraege und deckelt notfalls."""
    if not isinstance(infractions, dict) or not infractions:
        return 0
    removed = 0
    for key in [k for k, v in infractions.items()
                if not isinstance(v, dict) or (now - (v.get("ts") or 0)) > ttl_s]:
        infractions.pop(key, None)
        removed += 1
    if len(infractions) > max_users:
        oldest = sorted(infractions.items(), key=lambda kv: (kv[1] or {}).get("ts", 0))
        for key, _v in oldest[:len(infractions) - max_users]:
            infractions.pop(key, None)
            removed += 1
    return removed
