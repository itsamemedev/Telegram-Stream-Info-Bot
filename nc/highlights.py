"""nc.highlights — v4.0-W22: Highlight-Radar.

Die Idee: Wenn im Stream etwas Starkes passiert, EXPLODIERT der Chat. Diese
Reaktion ist ein besserer Momentmarker als jede Bild- oder Tonanalyse — und sie
ist praktisch gratis, weil ohnehin jede Chat-Nachricht durch EINE Stelle laeuft.

Der Radar fuehrt ein gleitendes Fenster der Nachrichtenrate (ueber ALLE drei
Plattformen zusammen), vergleicht die aktuelle Rate mit dem ruhigen Grundrauschen
und meldet einen Ausschlag, wenn die Rate deutlich darueber liegt. Zusaetzlich
zaehlt er Begeisterungs-Signale (Lachen, Emotes, Ausrufe) — Tempo ALLEIN kann
auch Streit sein.

Rein und testbar: der Zustand wird hereingereicht, keine Uhr, keine Globals.
"""

import math
import re

#: Begeisterung, absichtlich sprachneutral gehalten (Kick/Twitch/YouTube gemischt).
HYPE = re.compile(
    r"(?:\b(?:lol|lmao|omg|wtf|wow|krass|hammer|geil|nice|insane|clip(?:it)?|"
    r"was war das|digga|alter|hype|pog|poggers|kekw|lul|xd)\b|"
    r"[😂🤣😱🔥💀👏🎉😭]|"
    r"(?:ha){2,}|!{3,}|\?{3,})", re.I)


def new_state():
    return {"events": [], "base": [], "last_hit": 0.0, "hits": []}


def observe(state, now, text="", window_s=20.0, base_s=600.0):
    """Eine Chat-Nachricht einsortieren. Gibt (rate, base_rate, hype_anteil)
       zurueck — alles bezogen auf das aktuelle Fenster."""
    hype = bool(HYPE.search(text or ""))
    state["events"].append((now, hype))
    state["events"] = [(t, h) for (t, h) in state["events"] if now - t <= window_s]
    state["base"].append(now)
    state["base"] = [t for t in state["base"] if now - t <= base_s]

    n = len(state["events"])
    rate = n / max(window_s, 1.0) * 60.0                      # Nachrichten/Minute
    base_rate = len(state["base"]) / max(base_s, 1.0) * 60.0
    hype_share = (sum(1 for (_t, h) in state["events"] if h) / n) if n else 0.0
    return rate, base_rate, hype_share


def score(rate, base_rate, hype_share):
    """0..100. Ausschlag gegenueber dem Grundrauschen, veredelt mit Begeisterung.
       Ohne Grundrauschen (Stream gerade gestartet) bleibt der Wert klein."""
    if base_rate <= 0.5 or rate <= 0:
        return 0
    ratio = rate / base_rate
    if ratio <= 1.0:
        return 0
    spike = min(1.0, math.log(ratio, 4))                      # 4x Rate ≈ voll
    return int(round(100 * (0.75 * spike + 0.25 * min(1.0, hype_share * 2))))


def check(state, now, text="", *, min_score=55, min_msgs=8, cooldown_s=90.0,
          window_s=20.0, base_s=600.0):
    """(treffer|None, info). treffer = Highlight-Moment. Der Cooldown verhindert,
       dass ein einziger langer Jubel zu zwanzig Eintraegen wird."""
    rate, base_rate, hype_share = observe(state, now, text, window_s, base_s)
    info = {"rate": round(rate, 1), "base": round(base_rate, 1),
            "hype": round(hype_share, 2), "msgs": len(state["events"])}
    if len(state["events"]) < min_msgs:
        return None, info
    sc = score(rate, base_rate, hype_share)
    info["score"] = sc
    if sc < min_score:
        return None, info
    if state.get("last_hit") and (now - state["last_hit"]) < cooldown_s:
        info["skipped"] = "cooldown"
        return None, info
    state["last_hit"] = now
    hit = {"ts": now, "score": sc, "rate": info["rate"], "base": info["base"],
           "hype": info["hype"], "msgs": info["msgs"]}
    state["hits"] = (state.get("hits") or [])[-49:] + [hit]
    return hit, info


# ---- Der laufende Zustand ---------------------------------------------------

# REGISTER und NICHT Alias: bot.py erzeugt den Zustand mit new_state() und
# BINDET den Namen damit neu. Ein Alias zeigte danach fuer immer auf das
# leere Anfangs-Dict, und das Radar-Panel meldete dauerhaft null Treffer,
# ohne Fehler und ohne Logzeile (v4.1-W26 — dieselbe Ueberlegung wie bei
# MGR in nc/restreamstate.py und STALLS in nc/brainstate.py).
STATE = {"obj": None}


def zustand():
    """Der laufende Radar-Zustand, oder ein leeres Dict. Nie None — die
       Auskunfts-Route liest hier im Sekundentakt und soll nicht bei jedem
       Zugriff pruefen muessen."""
    return STATE["obj"] if STATE["obj"] is not None else {}
