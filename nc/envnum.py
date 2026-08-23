"""nc.envnum — v4.0-W32: reine Zahl-/Env-Parser, aus bot_v37 gebündelt.

Drei Helfer, die vorher im Monolithen lagen und dieselbe Aufgabe an mehreren
Stellen lösten — jetzt zentral, rein und bitgenau geprüft:

* env_int(name, default)                 — int aus os.getenv, Fallback + WARN.
* env_int_range(name, default, lo, hi)   — dito, auf [lo, hi] geklemmt.
* clamp_int(raw, default, lo, hi)        — der reine Kern: einen bereits gelesenen
                                           Rohwert robust nach int wandeln + klemmen.
                                           (Basis für den Flask-Query-Parser _arg_int
                                           und überall dort, wo `int(x)` sonst 500t.)

env_int/env_int_range lesen os.getenv direkt (verbatim übernommen); clamp_int ist
reine Eingabe→Ausgabe-Logik ohne jede Kopplung.
"""

import os


def env_int(name: str, default: int) -> int:
    """F24-B14: int(os.getenv(...)) crasht hart bei Tippfehlern in .env.
       Mit dieser Hilfsfunktion wird auf den Default gefallen + gewarnt."""
    raw = os.getenv(name)
    if raw is None or not raw.strip():
        return default
    try:
        return int(raw.strip())
    except (ValueError, TypeError):
        # Logger ist hier evtl. noch nicht initialisiert → print
        print(f"[boot] WARN: env {name}={raw!r} nicht als int parsebar → benutze {default}",
              flush=True)
        return default


def env_int_range(name: str, default: int, lo: int, hi: int) -> int:
    """B38: Wie env_int, aber clamped auf [lo, hi]. Bei out-of-range wird
       gewarnt und der nächstgelegene gültige Wert returnt. Wichtig für
       hour-Werte (0-23) und Prozent-Thresholds (1-100) — sonst crasht der
       DAILY_SUMMARY_HOUR=25-Fall im datetime.replace(hour=25) hart in einem
       1h-Retry-Loop. Bessere UX: clampen + WARN-Log."""
    v = env_int(name, default)
    if v < lo:
        print(f"[boot] WARN: env {name}={v} unter Minimum {lo} → benutze {lo}",
              flush=True)
        return lo
    if v > hi:
        print(f"[boot] WARN: env {name}={v} über Maximum {hi} → benutze {hi}",
              flush=True)
        return hi
    return v


def clamp_int(raw, default: int, lo=None, hi=None) -> int:
    """Reiner Kern: einen bereits gelesenen Rohwert (z. B. Query-Parameter) robust
       nach int wandeln — ungültig/None/leer → default — und optional auf [lo, hi]
       klemmen. Wirft nie: ersetzt `int(request.args.get(x, N))`, das bei 'abc'
       einen Flask-500 auslöste."""
    if raw is None or raw == "":
        v = default
    else:
        try:
            v = int(raw)
        except (TypeError, ValueError):
            v = default
    if lo is not None:
        v = max(lo, v)
    if hi is not None:
        v = min(hi, v)
    return v


def env_float(name: str, default: float) -> float:
    """v4.0-W78: float-Pendant zu env_int. WICHTIG: float(os.getenv(name, "d"))
       nutzt den Default NUR bei ungesetzter Variable — ist sie in der .env
       gesetzt-aber-LEER (name=), liefert getenv "" und float("") wirft
       ValueError('could not convert string to float: ''). Genau daran ist die
       Brain-Bridge beim Import gestorben. Hier: leer/None/unparsebar → default,
       wirft nie."""
    raw = os.getenv(name)
    if raw is None or not raw.strip():
        return default
    try:
        return float(raw.strip())
    except (ValueError, TypeError):
        print(f"[boot] WARN: env {name}={raw!r} nicht als float parsebar → benutze {default}",
              flush=True)
        return default


def clamp_float(raw, default: float, lo=None, hi=None) -> float:
    """Reiner Kern (analog clamp_int): Rohwert robust nach float — leer/None/
       ungültig → default — optional auf [lo, hi] geklemmt. Wirft nie; ersetzt
       float(request.args.get(x, N)), das bei '' oder 'abc' 500t."""
    if raw is None or (isinstance(raw, str) and not raw.strip()):
        v = default
    else:
        try:
            v = float(raw)
        except (TypeError, ValueError):
            v = default
    if lo is not None:
        v = max(lo, v)
    if hi is not None:
        v = min(hi, v)
    return v
