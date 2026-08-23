"""nc.cfgnorm — v4.0-W33: reine Config-Normalisierer, aus bot_v37 gebündelt.

Sechs Funktionen mit demselben Muster lagen verstreut im Monolithen: ein
gespeichertes app_config-dict (`saved`) wird mit .env-Fallbacks und Defaults zu
einem sauberen Config-dict normalisiert. Das Lesen aus der DB (_cfg_get) bleibt
im Bot; hier liegt nur die reine dict→dict-Normalisierung (Defaults, Clamps,
Typ-Coercion) — bitgenau gegen den Monolithen geprüft.

Die feinen Cast-Unterschiede sind bewusst 1:1 übernommen (z. B. highlights castet
den .env-Wert über int(float(...)), die Bremsen über float(...)).
"""

import os


def normalize_quiet_hours(saved):
    """{enabled, start, end} — Stunden modulo 24."""
    saved = saved or {}
    return {
        "enabled": bool(saved.get("enabled", False)),
        "start": int(saved.get("start", 23)) % 24,
        "end": int(saved.get("end", 7)) % 24,
    }


def normalize_highlights(saved):
    """Empfindlichkeit des Highlight-Radars (saved > .env > Default)."""
    saved = saved or {}

    def _i(key, env, default):
        try:
            return int(saved[key])
        except (KeyError, TypeError, ValueError):
            try:
                return int(float(os.getenv(env, default)))
            except (TypeError, ValueError):
                return int(default)
    _on = saved.get("enabled")
    if _on is None:
        _on = os.getenv("HIGHLIGHTS_ENABLED", "1").strip().lower() in (
            "1", "true", "yes", "on", "y")
    return {"enabled": bool(_on),
            "min_score": _i("min_score", "HIGHLIGHT_MIN_SCORE", 55),
            "min_msgs": _i("min_msgs", "HIGHLIGHT_MIN_MSGS", 8),
            "cooldown_s": _i("cooldown_s", "HIGHLIGHT_COOLDOWN_S", 90)}


def normalize_sendrate(saved):
    """YT-Sende-Bremse (saved > .env > Default)."""
    saved = saved or {}

    def _f(key, env, default):
        try:
            return float(saved[key])
        except (KeyError, TypeError, ValueError):
            try:
                return float(os.getenv(env, default))
            except (TypeError, ValueError):
                return float(default)
    return {"min_gap_s": _f("min_gap_s", "YT_SEND_MIN_GAP_S", 3),
            "per_min": int(_f("per_min", "YT_SEND_PER_MIN", 12))}


def normalize_gate(saved):
    """AZRAEL-Reply-Bremse (saved > .env > Default)."""
    saved = saved or {}

    def _f(key, env, default):
        try:
            return float(saved[key])
        except (KeyError, TypeError, ValueError):
            try:
                return float(os.getenv(env, default))
            except (TypeError, ValueError):
                return float(default)
    return {"min_gap_s": _f("min_gap_s", "AZRAEL_REPLY_MIN_GAP_S", 8),
            "user_cooldown_s": _f("user_cooldown_s", "AZRAEL_REPLY_USER_COOLDOWN_S", 60),
            "per_min": int(_f("per_min", "AZRAEL_REPLY_PER_MIN", 6)),
            "dup_window_s": _f("dup_window_s", "AZRAEL_REPLY_DUP_WINDOW_S", 120)}


def normalize_audio(saved, tone_def, freq_def, ms_def, vol_def, gap_def, duck_def):
    """Ton-/Ducking-Einstellungen. Anders als die Bremsen KEIN os.getenv im
       Fallback — die Defaults sind bereits aufgelöste Modul-Konstanten, die der
       Bot hereinreicht."""
    saved = saved or {}

    def _f(key, env_default):
        try:
            return float(saved[key])
        except (KeyError, TypeError, ValueError):
            return float(env_default)

    def _i(key, env_default):
        try:
            return int(saved[key])
        except (KeyError, TypeError, ValueError):
            return int(env_default)
    return {
        "tone": bool(saved.get("tone", tone_def)),
        "freq": _f("freq", freq_def),
        "ms": _i("ms", ms_def),
        "vol": _f("vol", vol_def),
        "gap_ms": _i("gap_ms", gap_def),
        "duck": _f("duck", duck_def),
    }


def normalize_cohost(saved, base_cfg):
    """Proaktiver Co-Host (saved > .env > Default). base_cfg ist ein frisches
       Default-dict (nc.cohost.default_config), das hier gefüllt/gemerged wird."""
    saved = saved or {}
    cfg = base_cfg
    if isinstance(saved.get("enabled"), bool):
        cfg["enabled"] = saved["enabled"]
    else:
        cfg["enabled"] = os.getenv("AZRAEL_COHOST", "0").strip().lower() in (
            "1", "true", "yes", "on", "y")

    def _f(key, env, default):
        try:
            return float(saved[key])
        except (KeyError, TypeError, ValueError):
            try:
                return float(os.getenv(env, default))
            except (TypeError, ValueError):
                return float(default)
    cfg["min_gap_s"] = _f("min_gap_s", "AZRAEL_COHOST_MIN_GAP_S", cfg["min_gap_s"])
    cfg["per_15min"] = int(_f("per_15min", "AZRAEL_COHOST_PER_15MIN", cfg["per_15min"]))
    sk = saved.get("kinds")
    if isinstance(sk, dict):
        cfg["kinds"] = {**cfg["kinds"], **{k: {**cfg["kinds"].get(k, {}), **v}
                                           for k, v in sk.items() if isinstance(v, dict)}}
    return cfg
