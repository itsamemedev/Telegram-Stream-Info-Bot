"""nc.freeai — keyless Free-API-LLM-Client (V37, Stand 2026-07).

Der EINZIGE Cloud-AI-Pfad des Bots: OpenAI-kompatible Endpunkte, bevorzugt
ohne API-Key.

WAS SICH GEGENUEBER DER ALTEN FASSUNG GEAENDERT HAT (B120):
1. PRO-BASE-MODELL. Vorher ging EIN globaler Modellname ("openai") an ALLE
   Basen. Nur Pollinations kennt diesen Alias — jede Rotation auf eine
   zweite Base lief sofort in HTTP 400/404 "unknown model". Die Rotation
   war damit faktisch tot: fiel Base 1 aus, fiel alles aus. Jede Base hat
   jetzt ihre eigene Modell-Liste; der Aufrufer-Modellname gilt nur noch
   als *Wunsch* und geht nur an Basen, die ihn kennen.
2. POLLINATIONS-MIGRATION. text.pollinations.ai/openai ist der Altpfad;
   aktueller Endpunkt ist gen.pollinations.ai/v1/chat/completions, der fuer
   die meisten Modelle einen Key erwartet (POLLINATIONS_API_KEY). Anonym
   bleibt der offene Pfad + Referrer nutzbar.
3. REFERRER-AUTH. Pollinations identifiziert keylose Aufrufer ueber
   Referer/referrer. Ohne den Header landen Server-Requests im striktesten
   Anonym-Bucket. FREEAI_REFERRER setzt ihn (Default "nightcrawler").
4. FEHLER-KLASSIFIKATION. 402 (Payment Required) laeuft als 'auth', nicht
   als generisches 'http' — sonst zeigt das Dashboard "HTTP-Fehler" statt
   "Base verlangt jetzt einen Key".
5. DIAGNOSE. last_errors()/diagnose() merken pro Base den letzten echten
   Fehler inkl. Body-Anfang. Ohne das ist ein Ausfall der Kette blind.

Vertrag unveraendert: (text, error_kind) mit
error_kind in {None,'auth','rate_limit','http','timeout','net','empty'}.
"""

import json
import os
import threading
import time as _time_mod
import urllib.error
import urllib.request
from typing import AsyncIterator, List, Optional, Tuple

# ---- Basen-Katalog ----------------------------------------------------------
# 'models'   = was diese Base WIRKLICH kennt (erstes Element = Default).
# 'referrer' = Base wertet Referer/referrer zur App-Identifikation aus.
# Reihenfolge = Startreihenfolge; danach sortiert die gemessene Latenz.

_CATALOG = [
    {   # keyless, offener Altpfad
        "url": "https://text.pollinations.ai/openai",
        "key": "",
        "models": ["openai", "openai-fast", "mistral"],
        "referrer": True,
    },
    {   # aktueller Pollinations-Gateway (Key optional, aber empfohlen)
        "url": "https://gen.pollinations.ai/v1/chat/completions",
        "key": "",                       # aus POLLINATIONS_API_KEY
        "models": ["openai", "openai-fast", "gemini", "mistral"],
        "referrer": True,
    },
    {   # anonym 30 RPM, mit kostenlosem Token 120 RPM (token.llm7.io)
        "url": "https://api.llm7.io/v1",
        "key": "",                       # aus LLM7_TOKEN
        # B140: gpt-4o-mini-2024-07-18 entfernt — llm7.io lieferte dafuer
        # dauerhaft HTTP 400 "model_unavailable" und legte damit (als
        # models[0]-Default) den ganzen freeai-Pfad lahm. Neuer Default: nano.
        "models": ["gpt-4.1-nano-2025-04-14", "deepseek-r1-0528",
                   "qwen2.5-coder-32b-instruct"],
    },
    {   # OVH AI Endpoints, anonym ~2 RPM/Modell, EU-gehostet — gleiche
        # Region wie der Bot-Host, daher als letzte Reserve latenzarm.
        "url": "https://oai.endpoints.kepler.ai.cloud.ovh.net/v1",
        "key": "",
        "models": ["Meta-Llama-3_3-70B-Instruct",
                   "Mistral-Small-3.2-24B-Instruct-2506"],
    },
]

_MODEL = "openai"           # Wunschmodell des Bots (nur wenn Base es kennt)
_TIMEOUT = 60.0
_SESSION_GET = None          # async () -> aiohttp.ClientSession (gepoolt)
_REFERRER = os.getenv("FREEAI_REFERRER", "nightcrawler").strip() or "nightcrawler"
_WARN = lambda topic, msg: None          # noqa: E731
_TELEMETRY = lambda **kw: None           # noqa: E731

_COOLDOWN_S = 90.0           # 429-Sperre pro Base
_state_lock = threading.Lock()
_base_block = {}             # url -> monotonic-ts, bis wann gesperrt
_base_lat = {}               # url -> EMA-Latenz in ms
_base_err = {}               # url -> {"kind","detail","ts"}  (Diagnose)
_LAT_ALPHA = 0.3             # EMA-Gewicht neuer Messungen


def _default_bases() -> List[dict]:
    """Katalog + Keys aus der Umgebung. Keys sind IMMER optional."""
    poll_key = (os.getenv("POLLINATIONS_API_KEY", "")
                or os.getenv("POLLINATIONS_TOKEN", "")).strip()
    llm7_key = (os.getenv("LLM7_TOKEN", "")
                or os.getenv("LLM7_API_KEY", "")).strip()
    out = []
    for entry in _CATALOG:
        b = dict(entry)
        b["models"] = list(entry["models"])
        if "pollinations.ai" in b["url"] and poll_key:
            b["key"] = poll_key
        if "llm7.io" in b["url"] and llm7_key:
            b["key"] = llm7_key
        out.append(b)
    return out


_BASES: List[dict] = _default_bases()


def configure(bases=None, model=None, timeout=None, session_getter=None,
              warn_cb=None, telemetry_cb=None, cooldown_s=None,
              referrer=None):
    """Vom Bot einmalig beim Start aufgerufen (Reihenfolge egal, alles optional).

    bases: Liste von "url", "url|key" ODER dicts {url,key,models}.
           Leer/None = eingebauter Katalog (empfohlen)."""
    global _BASES, _MODEL, _TIMEOUT, _SESSION_GET, _WARN, _TELEMETRY
    global _COOLDOWN_S, _REFERRER
    if bases:
        parsed = []
        known = {c["url"].rstrip("/"): c for c in _CATALOG}
        for b in bases:
            if isinstance(b, dict):
                u = (b.get("url") or "").strip()
                k = (b.get("key") or "").strip()
                models = b.get("models")
            else:
                u, _, k = str(b).partition("|")
                u, k, models = u.strip(), k.strip(), None
            if not u:
                continue
            u = u.rstrip("/")
            # B120: bekannte Basen erben Modell-Liste + Referrer-Flag aus dem
            # Katalog, damit eine schlichte URL-Liste in FREEAI_BASES nicht
            # die Modell-Aufloesung verliert.
            cat = known.get(u, {})
            parsed.append({"url": u, "key": k or cat.get("key", ""),
                           "models": list(models or cat.get("models") or []),
                           "referrer": bool(cat.get("referrer", False))})
        if parsed:
            _BASES = parsed
    if model:
        _MODEL = str(model).strip()
    if timeout is not None:
        _TIMEOUT = float(timeout)
    if session_getter is not None:
        _SESSION_GET = session_getter
    if warn_cb is not None:
        _WARN = warn_cb
    if telemetry_cb is not None:
        _TELEMETRY = telemetry_cb
    if cooldown_s is not None:
        _COOLDOWN_S = float(cooldown_s)
    if referrer:
        _REFERRER = str(referrer).strip()


def bases_status() -> List[dict]:
    """Fuer Dashboards/Diagnose: Basen + Sperr-Status + letzter Fehler."""
    now = _time_mod.monotonic()
    with _state_lock:
        return [{"url": b["url"], "keyed": bool(b.get("key")),
                 "models": list(b.get("models") or []),
                 "blocked_s": max(0, round(_base_block.get(b["url"], 0) - now)),
                 "avg_ms": round(_base_lat[b["url"]]) if b["url"] in _base_lat else None,
                 "last_error": _base_err.get(b["url"])}
                for b in _BASES]


def last_errors() -> dict:
    """Letzter Fehler pro Base — das WARUM, wenn die Kette schweigt."""
    with _state_lock:
        return dict(_base_err)


def _record_latency(url: str, ms: float):
    with _state_lock:
        old = _base_lat.get(url)
        _base_lat[url] = ms if old is None else (old * (1 - _LAT_ALPHA) + ms * _LAT_ALPHA)
        _base_err.pop(url, None)          # Erfolg loescht den Altfehler


def _record_error(url: str, kind: str, detail: str = ""):
    with _state_lock:
        _base_err[url] = {"kind": kind, "detail": str(detail)[:200],
                          "ts": _time_mod.time()}


def _eligible_bases() -> List[dict]:
    """Basen ohne 429-Cooldown, sortiert nach EMA-Latenz (schnellste zuerst).
    Ungemessene Basen bekommen Latenz 0 → sie werden früh probiert und damit
    gemessen (sonst käme eine zweite Base nie an die Reihe). Sind ALLE
    gesperrt, trotzdem alle zurückgeben (lieber ein Versuch als sicheres
    Scheitern)."""
    now = _time_mod.monotonic()
    with _state_lock:
        free = [b for b in _BASES if _base_block.get(b["url"], 0) <= now]
        pool = free or list(_BASES)
        return sorted(pool, key=lambda b: _base_lat.get(b["url"], 0.0))


def _block_base(url: str):
    with _state_lock:
        _base_block[url] = _time_mod.monotonic() + _COOLDOWN_S


def _convert_messages(messages) -> list:
    """Ollama-Style Vision ('images': [base64,…] am Message-Dict) → OpenAI-
    Vision-Format (content-Array mit image_url/data-URL). Text-only Messages
    passieren unverändert — so bleiben ALLE alten Bot-Callsites kompatibel."""
    out = []
    for m in messages:
        imgs = m.get("images") if isinstance(m, dict) else None
        if not imgs:
            out.append(m)
            continue
        content = [{"type": "text", "text": m.get("content") or ""}]
        for b64 in imgs:
            b64 = str(b64)
            url = b64 if b64.startswith("data:") else "data:image/jpeg;base64," + b64
            content.append({"type": "image_url", "image_url": {"url": url}})
        out.append({"role": m.get("role", "user"), "content": content})
    return out


def _model_for(base: dict, wanted: Optional[str]) -> Optional[str]:
    """B120-Kernfix: Modellname PRO BASE aufloesen.

    Der Wunschname gilt nur, wenn die Base ihn kennt — sonst nimmt die Base
    ihr eigenes Default-Modell. Kennt eine Base gar keine Modelle (custom
    Base aus FREEAI_BASES), wird der Wunschname durchgereicht."""
    models = base.get("models") or []
    if not models:
        return wanted or _MODEL or None
    w = (wanted or _MODEL or "").strip()
    return w if (w and w in models) else models[0]


def _candidate_models(base: dict, wanted: Optional[str]) -> List[Optional[str]]:
    """B140: Reihenfolge der Modelle, die chat() bei EINER Base durchprobiert.

    Vorher schickte chat() pro Base genau EINEN Request (models[0] bzw. das
    gewuenschte Modell) und rotierte bei HTTP 400 sofort zur naechsten Base —
    die uebrigen Modelle derselben Base blieben ungenutzt. Ein einziges totes
    Modell (z.B. abgeschaltetes gpt-4o-mini) legte damit die ganze Base und
    im Zweifel AZRAEL lahm. Jetzt sind die restlichen Modelle legitime
    Rueckfaelle. Gewuenschtes (bekanntes) Modell zuerst, dann der Rest."""
    models = list(base.get("models") or [])
    if not models:
        return [wanted]        # custom Base ohne Katalog: _model_for entscheidet
    w = (wanted or _MODEL or "").strip()
    if w and w in models:
        return [w] + [m for m in models if m != w]
    return models


def _payload(base: dict, messages, model, stream=False) -> dict:
    body = {"model": _model_for(base, model),
            "messages": _convert_messages(messages),
            "stream": stream}
    if base.get("referrer"):
        body["referrer"] = _REFERRER      # Pollinations akzeptiert es im Body
    return body


def _headers(base: dict) -> dict:
    h = {"Content-Type": "application/json",
         "User-Agent": "NIGHTCRAWLER/37 (+nc.freeai)"}
    if base.get("key"):
        h["Authorization"] = "Bearer " + base["key"]
    if base.get("referrer"):
        h["Referer"] = (_REFERRER if "://" in _REFERRER
                        else f"https://{_REFERRER}.local/")
    return h


def _endpoint(base: dict) -> str:
    """Basen-URL -> Chat-Completions-Endpunkt (idempotent)."""
    u = base["url"].rstrip("/")
    if u.endswith(("/openai", "/completions")):
        return u
    return u + "/chat/completions"


def _extract_text(data) -> str:
    try:
        ch = (data.get("choices") or [{}])[0]
        c = (ch.get("message") or {}).get("content")
        if isinstance(c, list):          # Block-Format mancher Basen
            return "".join(p.get("text", "") for p in c if isinstance(p, dict))
        return c or ch.get("text") or ""
    except (AttributeError, IndexError, TypeError):
        return ""


def _classify_status(status: int) -> Optional[str]:
    if status in (401, 402, 403):
        # 402 = Gateway verlangt Guthaben/Key. Als 'auth' fuehren, nicht als
        # generisches 'http': der Unterschied entscheidet, ob der Operator
        # einen Key setzt oder das Netz debuggt.
        return "auth"
    if status == 429:
        return "rate_limit"
    if status >= 400:
        return "http"
    return None


# ---- async (Haupt-Pfad, nutzt die gepoolte aiohttp-Session des Bots) --------

async def chat(messages: List[dict], model=None, timeout=None
               ) -> Tuple[Optional[str], Optional[str]]:
    """Keyless-Chat mit Basen-Rotation. Vertrag: (text, error_kind)."""
    import aiohttp
    to = _TIMEOUT if (timeout is None or timeout <= 0) else float(timeout)
    last_err = "net"
    t0 = _time_mod.monotonic()
    for base in _eligible_bases():
        url = _endpoint(base)
        # B140: Modelle DIESER Base der Reihe nach durchprobieren. Ein
        # 400/model_unavailable auf dem ersten Modell verbrennt die Base nicht
        # mehr — die uebrigen Modelle sind legitime Rueckfaelle. auth/429/Netz
        # bleiben Base-Ebene (anderes Modell hilft nicht) und brechen die
        # Modellschleife, damit die aeussere Schleife zur naechsten Base geht.
        for _m in _candidate_models(base, model):
            try:
                if _SESSION_GET is None:
                    raise RuntimeError("freeai: session_getter nicht konfiguriert")
                session = await _SESSION_GET()
                async with session.post(
                        url, json=_payload(base, messages, _m),
                        headers=_headers(base),
                        timeout=aiohttp.ClientTimeout(total=to)) as resp:
                    kind = _classify_status(resp.status)
                    if kind == "rate_limit":
                        _block_base(base["url"])
                        _record_error(base["url"], kind, "HTTP 429")
                        _WARN("freeai429", f"freeai: 429 bei {base['url']} — Base "
                                           f"{int(_COOLDOWN_S)}s gesperrt, rotiere.")
                        last_err = kind
                        break                       # Base-Ebene → naechste Base
                    if kind == "auth":
                        # Key/Guthaben-Problem der Base — anderes Modell hilft nicht.
                        _record_error(base["url"], kind, f"HTTP {resp.status}")
                        _WARN("freeaihttp",
                              f"freeai: HTTP {resp.status} (auth) bei {url}")
                        last_err = kind
                        break                       # Base-Ebene → naechste Base
                    if kind:
                        # B120/B140: 400 & Co. sind i.d.R. MODELL-spezifisch
                        # (model_unavailable/unknown model). Body mitloggen, dann
                        # das NAECHSTE Modell derselben Base versuchen.
                        try:
                            _body = (await resp.text())[:200]
                        except Exception:
                            _body = ""
                        _record_error(base["url"], kind,
                                      f"HTTP {resp.status} (model={_m}): {_body}")
                        _WARN("freeaihttp",
                              f"freeai: HTTP {resp.status} bei {url} "
                              f"(model={_m}) {_body}")
                        last_err = kind
                        continue                    # naechstes Modell derselben Base
                    data = await resp.json(content_type=None)
                    txt = _extract_text(data)
                    ms = round((_time_mod.monotonic() - t0) * 1000)
                    if txt:
                        _record_latency(base["url"], ms)
                        _TELEMETRY(purpose="freeai", ok=True, ms=ms,
                                   prompt_len=sum(len(str(mm.get("content") or "")) for mm in messages),
                                   answer_len=len(txt))
                        return (txt, None)
                    _record_error(base["url"], "empty", str(data)[:200])
                    last_err = "empty"
                    continue                        # leere Antwort → naechstes Modell
            except Exception as e:
                last_err = "timeout" if "imeout" in type(e).__name__ else "net"
                _record_error(base["url"], last_err, f"{type(e).__name__}: {e}")
                _WARN("freeainet", f"freeai: {type(e).__name__} bei {base['url']}")
                break                               # Netz/Timeout = Base-Ebene → naechste Base
    _TELEMETRY(purpose="freeai", ok=False, ms=round((_time_mod.monotonic() - t0) * 1000),
               prompt_len=0, answer_len=0, err=last_err)
    return (None, last_err)


async def chat_stream(messages: List[dict], model=None, timeout=None
                      ) -> AsyncIterator[str]:
    """SSE-Streaming (OpenAI-Format). Yields Text-Deltas; bricht bei Fehler ab
    (Aufrufer kann auf chat() zurückfallen, wenn nichts kam)."""
    import aiohttp
    to = _TIMEOUT if (timeout is None or timeout <= 0) else float(timeout)
    for base in _eligible_bases():
        url = _endpoint(base)
        try:
            if _SESSION_GET is None:
                return
            session = await _SESSION_GET()
            async with session.post(
                    url, json=_payload(base, messages, model, stream=True),
                    headers=_headers(base),
                    timeout=aiohttp.ClientTimeout(total=to, sock_read=to)) as resp:
                if _classify_status(resp.status) == "rate_limit":
                    _block_base(base["url"])
                    continue
                if resp.status >= 400:
                    _record_error(base["url"],
                                  _classify_status(resp.status) or "http",
                                  f"HTTP {resp.status} (stream)")
                    continue
                got = False
                async for raw in resp.content:
                    line = raw.decode("utf-8", "ignore").strip()
                    if not line.startswith("data:"):
                        continue
                    body = line[5:].strip()
                    if body == "[DONE]":
                        return
                    try:
                        delta = ((json.loads(body).get("choices") or [{}])[0]
                                 .get("delta") or {}).get("content") or ""
                    except Exception:
                        delta = ""
                    if delta:
                        got = True
                        yield delta
                if got:
                    return          # Stream lief — nicht weiterrotieren
        except Exception as e:
            _record_error(base["url"], "net", f"{type(e).__name__}: {e}")
            continue
    return


# ---- sync (für Flask-Routen/Threads ohne Event-Loop) -------------------------

def chat_sync(messages: List[dict], model=None, timeout=None
              ) -> Tuple[Optional[str], Optional[str]]:
    """Blockierender Chat über urllib (keine aiohttp-Session nötig)."""
    to = _TIMEOUT if (timeout is None or timeout <= 0) else float(timeout)
    last_err = "net"
    for base in _eligible_bases():
        url = _endpoint(base)
        req = urllib.request.Request(
            url, data=json.dumps(_payload(base, messages, model)).encode(),
            headers=_headers(base), method="POST")
        try:
            _t0 = _time_mod.monotonic()
            with urllib.request.urlopen(req, timeout=to) as resp:
                data = json.loads(resp.read().decode("utf-8", "ignore"))
                txt = _extract_text(data)
                if txt:
                    _record_latency(base["url"], (_time_mod.monotonic() - _t0) * 1000)
                    return (txt, None)
                _record_error(base["url"], "empty", str(data)[:200])
                last_err = "empty"
        except urllib.error.HTTPError as e:
            kind = _classify_status(e.code) or "http"
            try:
                _detail = e.read().decode("utf-8", "ignore")[:200]
            except Exception:
                _detail = ""
            _record_error(base["url"], kind, f"HTTP {e.code}: {_detail}")
            if kind == "rate_limit":
                _block_base(base["url"])
            last_err = kind
            continue
        except Exception as e:
            last_err = "timeout" if "imeout" in type(e).__name__ else "net"
            _record_error(base["url"], last_err, f"{type(e).__name__}: {e}")
            continue
    return (None, last_err)


def alive_sync(timeout: float = 3.0) -> bool:
    """Schneller Health-Ping: ist mindestens eine Base erreichbar?"""
    r, err = chat_sync([{"role": "user", "content": "ping"}], timeout=timeout)
    return err not in ("net", "timeout") if err else bool(r)


def list_models_sync(timeout: float = 6.0) -> List[str]:
    """Modell-Liste der ersten erreichbaren Base (Pollinations: GET /models)."""
    for base in _eligible_bases():
        root = (base["url"].rsplit("/openai", 1)[0]
                .rsplit("/chat/completions", 1)[0].rstrip("/"))
        for path in ("/models", "/v1/models"):
            try:
                _rq = urllib.request.Request(root + path, headers=_headers(base))
                with urllib.request.urlopen(_rq, timeout=timeout) as resp:
                    data = json.loads(resp.read().decode("utf-8", "ignore"))
                if isinstance(data, list):
                    out = [str(m.get("name") or m.get("id") or m) if isinstance(m, dict)
                           else str(m) for m in data]
                    if out:
                        return out
                if isinstance(data, dict) and isinstance(data.get("data"), list):
                    out = [str(m.get("id") or "") for m in data["data"] if m.get("id")]
                    if out:
                        return out
            except Exception:
                continue
    # B120: Katalog-Fallback — das Dashboard darf nie eine leere Modell-
    # Auswahl zeigen, nur weil /models gerade nicht antwortet.
    seen, out = set(), []
    for b in _BASES:
        for m in b.get("models") or []:
            if m not in seen:
                seen.add(m)
                out.append(m)
    return out


def diagnose() -> str:
    """Einzeiler fuer /diag und das Dashboard: Zustand aller Basen."""
    parts = []
    for b in bases_status():
        state = f"gesperrt {b['blocked_s']}s" if b["blocked_s"] else "frei"
        seg = (b["url"].split("//")[-1][:40] + " ["
               + state + (f", {b['avg_ms']}ms" if b["avg_ms"] else "")
               + (", KEY" if b["keyed"] else ", keyless"))
        if b["last_error"]:
            seg += f", Fehler: {b['last_error']['kind']}"
        parts.append(seg + "]")
    return " | ".join(parts) or "keine Basen konfiguriert"
