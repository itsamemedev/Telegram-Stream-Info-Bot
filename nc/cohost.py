"""nc.cohost — v4.0-W24: AZRAEL als proaktiver Live-Co-Host (bot-frei, rein).

Bisher ergriff AZRAEL nur bei FUNKSTILLE selbst das Wort (F91). Der Sprung:
AZRAEL reagiert jetzt auch auf HIGHLIGHT-Momente — wenn der Chat (W22-Radar)
explodiert, wirft er von sich aus einen kurzen Live-Kommentar rein, ueber ALLE
Plattformen. Damit wird aus dem Antwort-Bot ein echter Co-Host, der das
Geschehen begleitet, statt nur auf Ansprache zu warten.

Der heikle Teil ist NICHT das Reden, sondern das MASS: zwei Ausloeser (Highlight
+ Funkstille) duerfen sich nicht ins Gehege kommen und keine Flut erzeugen.
Dieses Modul ist die EINE Entscheidungsstelle: pro Ausloeser eine Sperrzeit,
darueber ein globaler Mindestabstand und eine harte Obergrenze je 15 min. Der
Zustand wird hereingereicht und NUR bei Erlaubnis fortgeschrieben — abgelehnte
Impulse ziehen die Bremse nicht weiter an. Der Bot erzeugt die Zeile und sendet;
hier faellt nur die Ja/Nein-Entscheidung und der Prompt-Anstoss.
"""

WINDOW_S = 900.0     # 15-min-Fenster fuer die globale Obergrenze


def new_state():
    return {"last_any": None, "by_kind": {}, "window": []}


def default_config():
    return {
        "enabled": False,          # Opt-in — proaktives Reden ist eine Ansage
        "min_gap_s": 45.0,         # globaler Mindestabstand zwischen zwei Impulsen
        "per_15min": 8,            # harte Obergrenze je 15 min (alle Ausloeser)
        "kinds": {
            "highlight": {"on": True, "cooldown_s": 120.0},
            "quiet":     {"on": True, "cooldown_s": 300.0},
        },
    }


def _cfg(cfg):
    c = default_config()
    if isinstance(cfg, dict):
        for k in ("enabled", "min_gap_s", "per_15min"):
            if k in cfg:
                try:
                    c[k] = type(c[k])(cfg[k])
                except (TypeError, ValueError):
                    pass
        kinds = cfg.get("kinds")
        if isinstance(kinds, dict):
            for name, kc in kinds.items():
                base = c["kinds"].get(name, {"on": True, "cooldown_s": 180.0})
                if isinstance(kc, dict):
                    if "on" in kc:
                        base = {**base, "on": bool(kc["on"])}
                    if "cooldown_s" in kc:
                        try:
                            base = {**base, "cooldown_s": float(kc["cooldown_s"])}
                        except (TypeError, ValueError):
                            pass
                c["kinds"][name] = base
    return c


def _prune(state, now):
    cut = now - WINDOW_S
    win = state.setdefault("window", [])
    if win and win[0] < cut:
        state["window"] = win = [t for t in win if t >= cut]
    return win


def decide(state, kind, now, cfg=None):
    """(True, "") wenn AZRAEL jetzt proaktiv reden darf, sonst (False, grund).

    Reihenfolge: global aus? → Ausloeser aus? → globaler Mindestabstand →
    Ausloeser-Sperrzeit → 15-min-Obergrenze. Zustand nur bei Erlaubnis fort-
    geschrieben.
    """
    c = _cfg(cfg)
    if not c["enabled"]:
        return False, "aus"
    kc = c["kinds"].get(kind)
    if not kc or not kc.get("on", True):
        return False, "ausloeser_aus"
    win = _prune(state, now)
    last_any = state.get("last_any")
    if last_any is not None and (now - last_any) < c["min_gap_s"]:
        return False, "min_gap"
    last_kind = (state.get("by_kind") or {}).get(kind)
    if last_kind is not None and (now - last_kind) < kc["cooldown_s"]:
        return False, "cooldown"
    if c["per_15min"] > 0 and len(win) >= c["per_15min"]:
        return False, "per_15min"
    win.append(now)
    state["last_any"] = now
    state.setdefault("by_kind", {})[kind] = now
    return True, ""


def prompt_seed(kind, info=None):
    """Der Anstoss (deutsch), den der Bot AZRAELs react()/chat() als 'Aussage'
       gibt. Rein datengetrieben, damit testbar. Nie ein '@user' — proaktive
       Zeilen richten sich an die Runde, nicht an eine Person."""
    info = info or {}
    if kind == "highlight":
        rate = info.get("rate"); base = info.get("base")
        hype = info.get("hype")
        wie = "viel Gelächter und Hype" if hype else "der Chat geht steil"
        zahl = (f" ({rate} Nachrichten/min statt sonst {base})"
                if rate and base else "")
        return ("Im Stream passiert gerade etwas Starkes — der Chat explodiert"
                f"{zahl}, {wie}. Reagiere als Live-Co-Host mit EINEM kurzen, "
                "mitreißenden Satz auf den Moment, ohne einen einzelnen Zuschauer "
                "anzusprechen und ohne Links.")
    if kind == "quiet":
        return ("Der Chat ist gerade still, im Stream passiert aber etwas. Wirf "
                "als Live-Co-Host EINE kurze, lockere Bemerkung oder Frage an die "
                "Runde, die wieder Leben reinbringt — keine Links, sprich niemanden "
                "direkt an.")
    return ("Sag als Live-Co-Host EINEN kurzen, passenden Satz zum aktuellen "
            "Stream-Geschehen.")


def snapshot(state, now):
    win = [t for t in state.get("window", []) if t >= now - WINDOW_S]
    return {"in_window": len(win),
            "by_kind": dict(state.get("by_kind") or {}),
            "last_any": state.get("last_any")}
