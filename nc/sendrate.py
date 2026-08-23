"""nc.sendrate — v4.0-W23: ausgehende Sende-Bremse je Plattform (bot-frei, rein).

Warum: AZRAELs *Antworten* laufen seit W20 durch die replygate-Bremse — aber
Dankeschoens (Sub/Superchat), Command-Antworten und Mod-Verwarnungen NICHT.
Bei einem Ansturm gehen dann viele YouTube-liveChat-Inserts kurz hintereinander
raus; YouTube wertet das als Spam und sperrt Chat oder Konto. Diese Bremse sitzt
am EINEN echten Sendepunkt (_youtube_send) und gilt damit fuer JEDE Zeile,
egal welches Feature sie ausgeloest hat.

Modell: Mindestabstand zwischen zwei Zeilen + harte Obergrenze pro 60-s-Fenster.
Ueberschuss wird VERWORFEN, nicht gestaut — eine verworfene Chatzeile ist
harmloser als eine Kontosperre. Der Zustand wird hereingereicht (kein globaler
State); er wird NUR bei Erlaubnis fortgeschrieben, damit abgelehnte Zeilen die
Bremse nicht weiter anziehen.
"""


def new_state():
    """Frischer Bremszustand. 'window' = Zeitstempel der letzten erlaubten Sends
       (fuer die Minuten-Obergrenze), plus Zaehler fuer die Anzeige."""
    return {"last_ts": None, "window": [], "sent": 0, "dropped": 0}


def default_config():
    return {"min_gap_s": 3.0, "per_min": 12}


def _cfg(cfg):
    c = default_config()
    if isinstance(cfg, dict):
        for k in c:
            try:
                c[k] = type(c[k])(cfg[k])
            except (KeyError, TypeError, ValueError):
                pass
    return c


def _prune(state, now):
    cutoff = now - 60.0
    win = state.setdefault("window", [])
    if win and win[0] < cutoff:
        state["window"] = win = [t for t in win if t >= cutoff]
    return win


def allow(state, now, cfg=None):
    """(True, "") wenn die Zeile raus darf, sonst (False, grund).

    Reihenfolge: erst Mindestabstand, dann Minuten-Obergrenze. Der Zustand
    (last_ts/window/sent) wird NUR bei Erlaubnis fortgeschrieben; ein Drop
    erhoeht nur den 'dropped'-Zaehler.
    """
    c = _cfg(cfg)
    win = _prune(state, now)
    last = state.get("last_ts")
    if last is not None and c["min_gap_s"] > 0 and (now - last) < c["min_gap_s"]:
        state["dropped"] = state.get("dropped", 0) + 1
        return False, "min_gap"
    if c["per_min"] > 0 and len(win) >= c["per_min"]:
        state["dropped"] = state.get("dropped", 0) + 1
        return False, "per_min"
    win.append(now)
    state["last_ts"] = now
    state["sent"] = state.get("sent", 0) + 1
    return True, ""


def snapshot(state, now):
    """Lesbarer Zustand fuers Dashboard, ohne den Zustand zu veraendern."""
    cutoff = now - 60.0
    last_min = sum(1 for t in state.get("window", []) if t >= cutoff)
    return {"last_min": last_min,
            "sent": int(state.get("sent", 0)),
            "dropped": int(state.get("dropped", 0))}
