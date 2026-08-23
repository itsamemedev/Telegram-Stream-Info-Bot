"""nc.replygate — v4.0-W20: Bremse fuer AZRAELs Chat-Antworten.

Seit B170 geht JEDE Antwort an alle drei Chats (Kick/Twitch/YouTube). Aus einer
Frage werden also drei Zeilen. Bei mehreren Fragern zugleich — oder wenn jemand
AZRAEL absichtlich anstupst — flutet der Bot den Chat und riskiert obendrein
Plattform-Ratelimits. Bisher gab es KEINE Bremse.

Vier Regeln, in dieser Reihenfolge:
  1. gleiche Antwort kurz hintereinander  -> unterdruecken (Dopplung)
  2. Mindestabstand zwischen zwei Antworten (global)
  3. Cooldown je Nutzer (ein Vielfrager blockiert nicht den ganzen Chat)
  4. Obergrenze Antworten pro Minute

Rein und testbar: der Zustand wird als dict hereingereicht, nichts global.
"""

import hashlib
import re

_WS = re.compile(r"\s+")


def default_config():
    return {"min_gap_s": 8.0, "user_cooldown_s": 60.0,
            "per_min": 6, "dup_window_s": 120.0}


def _fingerprint(text):
    """Erkennungsmerkmal einer Antwort. Whitespace wird vereinheitlicht, sonst
       gilt „Text  A" als andere Antwort als „Text A" und die Dopplungssperre
       liefe ins Leere."""
    norm = _WS.sub(" ", (text or "").strip().lower())
    return hashlib.sha1(norm.encode("utf-8")).hexdigest()[:16]


def allow(state, user, text, now, cfg=None):
    """(True, "") wenn geantwortet werden darf, sonst (False, grund).
       state wird NUR bei Erlaubnis fortgeschrieben — abgelehnte Antworten
       duerfen die Bremse nicht weiter anziehen."""
    c = dict(default_config())
    c.update({k: v for k, v in (cfg or {}).items() if v is not None})
    last_ts = state.get("last_ts") or 0.0
    recent = [t for t in (state.get("recent") or []) if now - t < 60.0]
    users = {u: t for u, t in (state.get("users") or {}).items()
             if now - t < max(float(c["user_cooldown_s"]), 60.0)}
    dups = {f: t for f, t in (state.get("dups") or {}).items()
            if now - t < float(c["dup_window_s"])}

    fp = _fingerprint(text)
    if fp in dups:
        return False, "gleiche Antwort gerade erst gesendet"
    if last_ts and (now - last_ts) < float(c["min_gap_s"]):
        return False, f"Mindestabstand {c['min_gap_s']:g}s"
    ukey = (user or "").strip().lower()
    if ukey and ukey in users and (now - users[ukey]) < float(c["user_cooldown_s"]):
        return False, f"Cooldown fuer {user}"
    if len(recent) >= int(c["per_min"]):
        return False, f"Obergrenze {c['per_min']}/min"

    recent.append(now)
    if ukey:
        users[ukey] = now
    dups[fp] = now
    state["last_ts"] = now
    state["recent"] = recent
    state["users"] = users
    state["dups"] = dups
    return True, ""
