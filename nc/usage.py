"""nc.usage — LLM-Token- und Kostenzähler (v4.0-W92).

Akkumuliert Input/Output-Tokens (gesamt, je Modellfamilie, laufender Monat) und
schätzt die Kosten in EUR. Persistiert nach einer JSON-Datei, überlebt also
Neustarts. Thread-sicher (wird aus dem Claude-Call heraus aufgerufen, der in
einem Worker-Thread läuft).

WICHTIG: Die Preise sind SCHÄTZWERTE. Anbieterpreise ändern sich; deshalb sind
sie per configure()/env übersteuerbar und die Kosten werden auf der Website als
„geschätzt" ausgewiesen. Lieber transparent schätzen als exakt tun und irren.
"""
import json
import os
import threading
import time
from datetime import datetime, timezone

_LOCK = threading.RLock()
_USD_EUR = 0.92                      # gleiche Konvention wie nc.donations
_PATH = None
_LAST_PERSIST = 0.0
_PERSIST_EVERY_S = 10.0              # I/O drosseln — Zustand lebt im Speicher

# USD pro 1 Mio. Token (Input, Output) je Claude-Familie — SCHÄTZWERTE.
_RATES = {
    # v4.0-W97: EINE Rate für alles — „wie Claude". Das primäre Claude-Modell
    # ist haiku (claude-haiku-4-5); dessen Preis gilt jetzt für JEDES Token,
    # egal welcher Provider. USD pro 1 Mio Token (Input, Output).
    "claude":  (1.00, 5.00),
}


def _blank_bucket():
    return {"tokens_in": 0, "tokens_out": 0, "cost_eur": 0.0, "calls": 0}


_STATE = {
    "tokens_in": 0, "tokens_out": 0, "cost_eur": 0.0, "calls": 0,
    "by_provider": {},              # provider -> bucket (claude/freeai/brain/…)
    "month_key": "",
    "month": _blank_bucket(),
    "updated_at": 0.0,
}

# v4.0-W96: früher trennte _PAID_PROVIDERS bezahlt/gratis und setzte gratis auf
# 0 €. Das Transparenz-Panel soll aber den API-Gegenwert ALLER Tokens zeigen —
# die Trennung ist entfallen (_cost_eur bepreist jetzt jeden Provider).


def _family(model):
    m = (model or "").lower()
    if "haiku" in m:
        return "haiku"
    if "opus" in m:
        return "opus"
    if "sonnet" in m:
        return "sonnet"
    return "_default"


def estimate_tokens(text):
    """Grobe Token-Schätzung für Provider ohne usage-Feld (~4 Zeichen/Token).
       Nimmt str, Message-Liste oder beliebiges Objekt entgegen."""
    if text is None:
        return 0
    if isinstance(text, (list, tuple)):
        s = 0
        for m in text:
            if isinstance(m, dict):
                c = m.get("content", "")
                s += len(c) if isinstance(c, str) else len(str(c))
            else:
                s += len(str(m))
        n = s
    elif isinstance(text, str):
        n = len(text)
    else:
        n = len(str(text))
    return max(0, n // 4)


def _month_key(ts=None):
    d = datetime.fromtimestamp(ts, timezone.utc) if ts else datetime.now(timezone.utc)
    return "%04d-%02d" % (d.year, d.month)


def _cost_eur(provider, family, tin, tout):
    # v4.0-W97: ALLE Tokens werden wie Claude berechnet — eine Rate, sonst nichts.
    # (W96 hatte pro Provider verschiedene Raten genommen; das war zu viel.)
    ri, ro = _RATES.get("claude", (1.00, 5.00))
    usd = (tin / 1_000_000.0) * ri + (tout / 1_000_000.0) * ro
    return round(usd * _USD_EUR, 6)


def configure(path=None, usd_eur=None, rates=None):
    """Persistenzpfad setzen, Zustand laden, Preise/Kurs übersteuern.
       Idempotent — mehrfach aufrufbar."""
    global _PATH, _USD_EUR
    with _LOCK:
        if usd_eur is not None:
            try:
                _USD_EUR = float(usd_eur)
            except (TypeError, ValueError):
                pass
        if isinstance(rates, dict):
            for k, v in rates.items():
                try:
                    _RATES[k] = (float(v[0]), float(v[1]))
                except Exception:
                    pass
        if path:
            _PATH = path
            _load()


def _load():
    if not _PATH or not os.path.exists(_PATH):
        return
    try:
        with open(_PATH, "r", encoding="utf-8") as fh:
            data = json.load(fh)
        if isinstance(data, dict) and "tokens_in" in data:
            _STATE.update(data)
            _STATE.setdefault("by_provider", {})
            _STATE.setdefault("month", _blank_bucket())
    except Exception:
        pass                        # kaputte Datei → mit leerem Zustand weiter


def _persist(force=False):
    global _LAST_PERSIST
    if not _PATH:
        return
    now = time.time()
    if not force and (now - _LAST_PERSIST) < _PERSIST_EVERY_S:
        return
    _LAST_PERSIST = now
    try:
        os.makedirs(os.path.dirname(_PATH) or ".", exist_ok=True)
        tmp = _PATH + ".tmp"
        with open(tmp, "w", encoding="utf-8") as fh:
            json.dump(_STATE, fh)
        os.replace(tmp, _PATH)      # atomar
    except Exception:
        pass


def record(provider, model, tokens_in, tokens_out):
    """Einen LLM-Call verbuchen (provider = 'claude'|'freeai'|'brain'|…).
       Tokens werden IMMER gezählt; Kosten nur für bezahlte Provider.
       Wirft NIE — Telemetrie darf den Call nie stören."""
    try:
        tin = int(tokens_in or 0)
        tout = int(tokens_out or 0)
    except (TypeError, ValueError):
        return
    if tin <= 0 and tout <= 0:
        return
    prov = (provider or "?").strip().lower() or "?"
    cost = _cost_eur(prov, _family(model), tin, tout)
    with _LOCK:
        mk = _month_key()
        if _STATE.get("month_key") != mk:      # Monatswechsel → Monatsbucket neu
            _STATE["month_key"] = mk
            _STATE["month"] = _blank_bucket()
        for bucket in (_STATE, _STATE["month"]):
            bucket["tokens_in"] += tin
            bucket["tokens_out"] += tout
            bucket["cost_eur"] = round(bucket["cost_eur"] + cost, 6)
            bucket["calls"] += 1
        bp = _STATE["by_provider"].setdefault(prov, _blank_bucket())
        bp["tokens_in"] += tin
        bp["tokens_out"] += tout
        bp["cost_eur"] = round(bp["cost_eur"] + cost, 6)
        bp["calls"] += 1
        _STATE["updated_at"] = time.time()
        _persist()


def snapshot():
    """Öffentlicher Zustand (Kopie). tokens_total + gerundete EUR fürs Frontend."""
    with _LOCK:
        tin = int(_STATE["tokens_in"])
        tout = int(_STATE["tokens_out"])
        m = _STATE.get("month") or _blank_bucket()
        return {
            "tokens_in": tin,
            "tokens_out": tout,
            "tokens_total": tin + tout,
            "cost_eur": round(float(_STATE["cost_eur"]), 2),
            "calls": int(_STATE["calls"]),
            "month": {
                "tokens_total": int(m["tokens_in"]) + int(m["tokens_out"]),
                "cost_eur": round(float(m["cost_eur"]), 2),
                "calls": int(m["calls"]),
            },
            "by_provider": {k: {"tokens_total": int(v["tokens_in"]) + int(v["tokens_out"]),
                                "cost_eur": round(float(v["cost_eur"]), 2),
                                "calls": int(v["calls"])}
                            for k, v in _STATE.get("by_provider", {}).items()},
            # v4.0-W101: Rate offenlegen, damit die Website sie LIEST statt sie
            # doppelt hartzukodieren (eine Quelle der Wahrheit).
            "rate": {
                "in_per_mtok_usd": _RATES.get("claude", (1.00, 5.00))[0],
                "out_per_mtok_usd": _RATES.get("claude", (1.00, 5.00))[1],
                "usd_eur": round(float(_USD_EUR), 4),
            },
            "updated_at": float(_STATE.get("updated_at") or 0.0),
        }


def flush():
    """Erzwungenes Schreiben (z. B. aus der stats-Schleife)."""
    with _LOCK:
        _persist(force=True)
