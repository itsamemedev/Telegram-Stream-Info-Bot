"""nc.claude — v4.0-W64: Anthropic-Claude-Provider (ersetzt Ollama/keyless als
primären LLM-Pfad, sobald ein API-Key gesetzt ist).

Reine, testbare Bausteine: _split_messages (system → Top-Level-Feld, nur
user/assistant in messages, wie die Messages-API es verlangt), build_payload,
parse_response. chat_sync macht den HTTP-Call über einen injizierbaren opener
(Default: urllib) und mappt Fehler auf stabile Kürzel. Der API-Key wird vom
Aufrufer übergeben (kommt aus app_config/Dashboard oder ENV) — dieses Modul
speichert nie einen Key.
"""

import json
import urllib.request
import urllib.error

API_URL = "https://api.anthropic.com/v1/messages"
API_VERSION = "2023-06-01"
DEFAULT_MODEL = "claude-haiku-4-5-20251001"
DEFAULT_MAX_TOKENS = 1024

# v4.0-W73: bekannt ABGESCHALTETE Modelle → aktuelles Äquivalent gleicher Klasse.
# Ein auf ein retired Modell gepinnter Wert (env ANTHROPIC_MODEL / gespeichert)
# liefert von der API ein 404 not_found_error — z. B. claude-3-5-haiku-latest
# (Haiku 3.5, retired 2026-02-19). Statt still zu scheitern wird beim Auflösen
# angehoben. Die Zielstrings sind die aktuellen (identisch zur Dashboard-Auswahl).
CURRENT_HAIKU = DEFAULT_MODEL                 # Haiku 4.5
CURRENT_SONNET = "claude-sonnet-5"
CURRENT_OPUS = "claude-opus-4-8"

# Vollständig retired 4.0/4.1-Erstausgaben (exakte IDs — NICHT per Präfix, sonst
# träfe man die aktiven 4-5/4-6/4-7/4-8).
_RETIRED_EXACT = {
    "claude-sonnet-4-0", "claude-sonnet-4", "claude-sonnet-4-20250514",
    "claude-opus-4-0", "claude-opus-4", "claude-opus-4-20250514",
    "claude-opus-4-1", "claude-opus-4-1-20250805",
}
# Ganze retired Generationen (1/2/instant/3/3.5/3.7) — Präfix ist sicher, weil
# in diesen Familien nichts mehr aktiv ist.
_RETIRED_PREFIX = (
    "claude-1", "claude-2", "claude-instant",
    "claude-3-haiku", "claude-3-5-haiku",
    "claude-3-opus", "claude-3-5-opus",
    "claude-3-sonnet", "claude-3-5-sonnet", "claude-3-7-sonnet",
)


def _retired_family(model):
    """Klasse (haiku/sonnet/opus) eines bekannt abgeschalteten Modells, sonst None."""
    m = (model or "").strip().lower()
    if not m:
        return None
    if m in _RETIRED_EXACT:
        return "opus" if "opus" in m else "sonnet"   # haiku ist nicht im Exakt-Set
    for p in _RETIRED_PREFIX:
        if m.startswith(p):
            return "haiku" if "haiku" in p else ("opus" if "opus" in p else "sonnet")
    return None


def is_retired(model):
    """True, wenn das Modell bekannt abgeschaltet ist (würde 404 liefern)."""
    return _retired_family(model) is not None


def resolve_model(model):
    """Retired-Modell → aktuelles Äquivalent gleicher Klasse; sonst unverändert.
       Leerer Wert → DEFAULT_MODEL. Rein und deterministisch."""
    fam = _retired_family(model)
    if fam == "haiku":
        return CURRENT_HAIKU
    if fam == "sonnet":
        return CURRENT_SONNET
    if fam == "opus":
        return CURRENT_OPUS
    return (model or "").strip() or DEFAULT_MODEL


def _split_messages(messages):
    """Anthropic trennt System-Prompt vom Verlauf: system ist ein Top-Level-Feld,
       messages enthält nur user/assistant. Mehrere System-Nachrichten werden
       zusammengeführt."""
    system = []
    conv = []
    for m in (messages or []):
        role = (m.get("role") or "").strip()
        content = m.get("content", "")
        if role == "system":
            if str(content).strip():
                system.append(str(content).strip())
        elif role in ("user", "assistant"):
            conv.append({"role": role, "content": str(content)})
    return ("\n\n".join(system) or None), conv


def build_payload(messages, model=None, max_tokens=None):
    """Request-Body für /v1/messages."""
    system, conv = _split_messages(messages)
    body = {"model": model or DEFAULT_MODEL,
            "max_tokens": int(max_tokens or DEFAULT_MAX_TOKENS),
            "messages": conv}
    if system:
        body["system"] = system
    return body


def parse_response(data):
    """Antworttext aus content[]-Blöcken zusammensetzen (nur type=='text')."""
    parts = []
    for block in ((data or {}).get("content") or []):
        if isinstance(block, dict) and block.get("type") == "text":
            parts.append(block.get("text", ""))
    return "".join(parts).strip()


def parse_usage(data):
    """v4.0-W92: (input_tokens, output_tokens) aus der API-Antwort ziehen.
       Fehlt der usage-Block, (0, 0)."""
    u = (data or {}).get("usage") or {}
    try:
        return (int(u.get("input_tokens") or 0), int(u.get("output_tokens") or 0))
    except (TypeError, ValueError):
        return (0, 0)


def _error_kind(code):
    if code == 401 or code == 403:
        return "auth"
    if code == 429:
        return "rate"
    if code == 400:
        return "bad_request"
    return f"http_{code}"


def chat_sync(messages, api_key, model=None, timeout=None, max_tokens=None, opener=None,
              on_usage=None):
    """Blockierender Claude-Chat → (text, err_kind|None). opener(req, timeout) ist
       für Tests injizierbar; Default ist urllib. Ohne Key → (None, 'no_key').
       v4.0-W92: on_usage(model, input_tokens, output_tokens) wird bei Erfolg
       best-effort aufgerufen (Token-Zählung) — Default None = altes Verhalten."""
    if not api_key:
        return (None, "no_key")
    body = build_payload(messages, model, max_tokens)
    req = urllib.request.Request(
        API_URL, data=json.dumps(body).encode("utf-8"),
        headers={"content-type": "application/json",
                 "x-api-key": api_key,
                 "anthropic-version": API_VERSION},
        method="POST")
    _open = opener or (lambda r, t: urllib.request.urlopen(r, timeout=t))
    try:
        with _open(req, timeout or 60) as r:
            data = json.loads(r.read().decode("utf-8"))
        text = parse_response(data)
        if on_usage:
            try:
                _tin, _tout = parse_usage(data)
                on_usage(body.get("model"), _tin, _tout)
            except Exception:
                pass
        return (text, None) if text else (None, "empty")
    except urllib.error.HTTPError as e:
        return (None, _error_kind(e.code))
    except Exception:
        return (None, "unreachable")


def probe(api_key, model=None, opener=None):
    """v4.0-W70: Diagnose-Call für den Dashboard-Test → (ok, kind, detail).
       detail nennt die ECHTE Ursache: HTTP-Status + Anthropics Fehlertext, oder
       den konkreten Netzfehler (Timeout/DNS/refused/TLS) — damit der Betreiber
       nicht im Dunkeln steht, wenn der Test scheitert."""
    if not api_key:
        return (False, "no_key", "Kein Key gesetzt.")
    body = build_payload([{"role": "user", "content": "ping"}], model, 8)
    req = urllib.request.Request(
        API_URL, data=json.dumps(body).encode("utf-8"),
        headers={"content-type": "application/json", "x-api-key": api_key,
                 "anthropic-version": API_VERSION}, method="POST")
    _open = opener or (lambda r, t: urllib.request.urlopen(r, timeout=t))
    try:
        with _open(req, 20) as r:
            data = json.loads(r.read().decode("utf-8"))
        return (True, "ok", "Verbindung ok — Claude antwortet.") if parse_response(data) \
            else (False, "empty", "Verbunden, aber leere Antwort.")
    except urllib.error.HTTPError as e:
        raw = ""
        try:
            raw = e.read().decode("utf-8", "replace")[:400]
        except Exception:
            pass
        amsg = ""
        try:
            amsg = (json.loads(raw).get("error", {}) or {}).get("message", "")
        except Exception:
            amsg = raw
        return (False, _error_kind(e.code), "HTTP %s: %s" % (e.code, amsg or getattr(e, "reason", "") or "abgelehnt"))
    except urllib.error.URLError as e:
        return (False, "unreachable", "Netzwerk nicht erreichbar: %s" % getattr(e, "reason", e))
    except Exception as e:
        return (False, "unreachable", "%s: %s" % (type(e).__name__, e))


def test_key(api_key, model=None, opener=None):
    """Key mit einem minimalen Call prüfen → (ok: bool, detail: str)."""
    ok_, _kind, detail = probe(api_key, model=model, opener=opener)
    return (ok_, "ok" if ok_ else detail)


# ── v4.0-W111: Schluessel- und Modellwahl, aus bot.py geloest ───────────
#
# Warum hierher: das sind Anthropic-Belange, und nc.claude IST der
# Anthropic-Provider. Im Laufzeitkontext haetten sie drei Slots belegt, ohne
# dass ein zweites Blueprint sie braucht. Sie lasen nur deshalb wie Bot-Code,
# weil sie ueber _cfg_get an die app_config gingen — die liegt seit W111
# ebenfalls in nc (nc.cfgstore).

import logging as _logging                                    # noqa: E402
import os as _os                                              # noqa: E402

from nc import cfgstore as _cfgstore                          # noqa: E402

_log = _logging.getLogger("TikTokBot")
_MODEL_WARNED = set()


def api_key():
    """Anthropic-API-Key — Dashboard-Eingabe (app_config) hat Vorrang, sonst
       ENV ANTHROPIC_API_KEY. Leer bedeutet Claude aus, der Fallback greift."""
    try:
        k = _cfgstore.get("ai.anthropic_key", None)
        if isinstance(k, str) and k.strip():
            return k.strip()
    except Exception:
        pass
    return _os.getenv("ANTHROPIC_API_KEY", "").strip()


def model_raw(override=None):
    """Der KONFIGURIERTE Modellwert (override → app_config → env → Default),
       noch OHNE Retired-Aufloesung — fuer die Status-Anzeige."""
    if override and str(override).startswith("claude"):
        return override
    try:
        m = _cfgstore.get("ai.anthropic_model", None)
        if isinstance(m, str) and m.strip():
            return m.strip()
    except Exception:
        pass
    return _os.getenv("ANTHROPIC_MODEL", "").strip() or DEFAULT_MODEL


def model(override=None):
    """Das EFFEKTIVE Modell — ein bekannt abgeschalteter Pin wird automatisch
       auf das aktuelle Aequivalent gleicher Klasse angehoben, damit der
       LLM-Pfad nicht still bricht. Die Anhebung wird EINMAL je Wert
       protokolliert."""
    raw = model_raw(override)
    eff = resolve_model(raw)
    if eff != raw and raw not in _MODEL_WARNED:
        _MODEL_WARNED.add(raw)
        _log.warning("Anthropic-Modell '%s' ist abgeschaltet — automatisch auf "
                     "'%s' angehoben. Bitte ANTHROPIC_MODEL/.env aktualisieren.",
                     raw, eff)
    return eff
