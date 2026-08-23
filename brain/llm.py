# brain/llm.py — M6: Eigene LLM-Runtime (llama.cpp; V37: ollama-frei)
#
# ARCHITEKTUR-ENTSCHEIDUNG (ehrlich begründet): Die "eigene Runtime"
# ist llama.cpp (llama-server, GGUF INT4) statt einer Python-Eigenbau-
# Inferenz (tokenizer.py/attention.py/kv_cache.py). WARUM:
#   - llama.cpp liefert GQA, Sliding-Window-Attention, Streaming-KV-Cache
#     und INT4/INT3-Quantisierung produktionsreif und CPU-optimiert (AVX2).
#   - Eine Pure-Python-Attention wäre auf 8 Cores 10-50x langsamer und
#     monatelange Arbeit ohne Mehrwert — Verstoß gegen die v37-Kernregel
#     "niemals nur für mehr KI optimieren".
#   - Ollama fällt trotzdem weg: llama-server ist EIN statisches Binary
#     + EIN GGUF-File, kein Go-Daemon, kein Model-Registry-Overhead.
#
# BUDGET-PRINZIP: Das LLM ist Tier 4 — die LETZTE Instanz. Hartes
# Stundenbudget + Concurrency 1 (CPU-Box: zwei parallele Inferenzen
# würden Recording-ffmpeg die Kerne stehlen). Budget erschöpft ⇒ der
# Router bekommt Unhandled und antwortet ehrlich "kein Tier konnte".
#
# WARUM stdlib-urllib statt aiohttp: brain/ ist thread-basiert (M1) und
# dependency-frei. Blocking-HTTP ist bei Concurrency 1 kein Nachteil.

from __future__ import annotations

import json
import logging
import os
import threading
import time
import urllib.error
import urllib.request
from typing import Optional

from nc.envnum import env_float, env_int  # v4.0-W78/W81: leer-gesetzte .env robust

log = logging.getLogger("brain.llm")

# B-M6-1: Konfig als Laufzeit-Lookup statt Modul-Konstante. WARUM:
# bot_v36 lädt .env teils NACH den ersten Imports — Konstanten würden
# die Defaults einfrieren, bevor die echten Werte existieren (gleiche
# Bug-Klasse wie BRAIN_DB in M1, dort bereits gefixt).
def _backend_conf() -> str:
    return os.getenv("BRAIN_LLM_BACKEND", "auto")   # auto|llamacpp|off (V37: ollama entfernt)


def _llamacpp_url() -> str:
    return os.getenv("BRAIN_LLAMACPP_URL", "http://127.0.0.1:8080").rstrip("/")


def _max_calls_h() -> int:
    return env_int("BRAIN_LLM_MAX_CALLS_H", 30)


def _timeout_s() -> float:
    # V37-LLMBUDGET: CPU-Inferenz ohne GPU braucht Zeit — 60s war zu knapp und
    # riss Requests mitten in der Antwort ab. Auf 300s angehoben (deckt lange
    # Antworten auf 8 Cores). Über BRAIN_LLM_TIMEOUT_S weiter frei einstellbar.
    return env_float("BRAIN_LLM_TIMEOUT_S", 300)


def _max_tokens() -> int:
    # V37-LLMBUDGET: 512 schnitt längere Antworten ab. Auf 1024 verdoppelt —
    # genug für ausführliche Antworten, ohne den CPU-Aufwand zu sprengen.
    return env_int("BRAIN_LLM_MAX_TOKENS", 1024)


class BudgetExhausted(Exception):
    """Stundenbudget verbraucht — Aufrufer (Router-Tier) reicht als
    Unhandled weiter statt zu warten: Warten würde den Router-Pfad
    blockieren, und Tier-4-Antworten sind nie zeitkritisch genug dafür."""


class LLMRuntime:
    def __init__(self):
        # Concurrency 1: EIN Inferenz-Slot. threading.Lock statt Semaphore,
        # non-blocking acquire → zweiter Aufrufer bekommt sofort busy.
        self._slot = threading.Lock()
        self._calls: list[float] = []
        self._durs: list[float] = []      # V37: letzte Latenzen (ms)      # Timestamps fürs Stundenbudget
        self._stats = {"ok": 0, "errors": 0, "budget_denied": 0,
                       "busy_denied": 0, "by_backend": {}}
        # B-M6-2: RLock, nicht Lock — stats() ruft unter gehaltenem Lock
        # budget() auf, das denselben Lock nimmt. Nicht-reentrant = Deadlock.
        self._stats_lock = threading.RLock()

    # ------------------------------------------------------------- API

    def chat(self, messages: list[dict], timeout: Optional[float] = None,
             max_tokens: Optional[int] = None) -> dict:
        """Eine Chat-Vervollständigung über die Backend-Kette.

        Rückgabe: {ok, text|error, backend, ms}. Wirft BudgetExhausted
        bei verbrauchtem Budget (bewusst Exception statt ok=False: der
        Unterschied 'LLM kaputt' vs. 'LLM gedeckelt' muss im Router-Trace
        unterscheidbar sein)."""
        self._check_budget()
        if not self._slot.acquire(blocking=False):
            with self._stats_lock:
                self._stats["busy_denied"] += 1
            raise BudgetExhausted("Inferenz-Slot belegt (Concurrency 1)")
        try:
            t0 = time.time()
            last_err = "kein Backend konfiguriert"
            for backend in self._chain():
                try:
                    text = self._call(backend, messages,
                                      timeout or _timeout_s(),
                                      max_tokens or _max_tokens())
                    ms = round((time.time() - t0) * 1000, 1)
                    with self._stats_lock:
                        self._stats["ok"] += 1
                        bb = self._stats["by_backend"]
                        bb[backend] = bb.get(backend, 0) + 1
                        self._calls.append(time.time())
                        # V37: Latenz-Historie für stats()/Metrik/Dashboard
                        self._durs.append(ms)
                        if len(self._durs) > 50:
                            del self._durs[:25]
                    return {"ok": True, "text": text,
                            "backend": backend, "ms": ms}
                except Exception as e:
                    last_err = f"{backend}: {type(e).__name__}: {e}"
                    log.debug("LLM-Backend %s fehlgeschlagen: %s",
                              backend, e)
            with self._stats_lock:
                self._stats["errors"] += 1
            return {"ok": False, "error": last_err, "backend": None,
                    "ms": round((time.time() - t0) * 1000, 1)}
        finally:
            self._slot.release()

    _HEALTH_TTL = 15.0

    def health(self) -> dict:
        """Backends anpingen (für Dashboard). Zählt NICHT ins Budget.
        IMP-4: 15s-Cache — bei toten Backends kosten die Probes 2×3s
        Timeout; ungecached blockierte das bei jedem 10s-Dashboard-Poll
        einen Flask-Worker. Budget wird immer frisch berechnet."""
        now = time.time()
        cache = getattr(self, "_health_cache", None)
        if cache and now - cache[0] < self._HEALTH_TTL:
            out = dict(cache[1])
        else:
            out = {"llamacpp": self._probe("llamacpp")}
            # B120: Cloud-Reserve im Health sichtbar machen. Ohne den
            # Eintrag meldete das Dashboard 'offline', obwohl freeai
            # antwortet — der Operator suchte dann am falschen Ende.
            if "freeai" in self._chain():
                try:
                    from nc import freeai as _freeai
                    out["freeai"] = {"up": bool(_freeai.alive_sync(3.0)),
                                     "bases": _freeai.bases_status()}
                except Exception as e:
                    out["freeai"] = {"up": False, "error": type(e).__name__}
            self._health_cache = (now, dict(out))
        out["backend_conf"] = _backend_conf()
        out["budget"] = self.budget()
        with self._stats_lock:                     # V37: Latenz für die Pill
            out["avg_ms"] = (round(sum(self._durs) / len(self._durs), 1)
                             if self._durs else None)
        return out

    def budget(self) -> dict:
        cutoff = time.time() - 3600
        with self._stats_lock:
            self._calls = [t for t in self._calls if t > cutoff]
            used = len(self._calls)
        return {"used_h": used, "max_h": _max_calls_h(),
                "remaining": max(_max_calls_h() - used, 0)}

    def stats(self) -> dict:
        with self._stats_lock:
            return dict(self._stats, budget=self.budget(),
                        avg_ms=(round(sum(self._durs) / len(self._durs), 1)
                                if self._durs else None),
                        last_ms=(self._durs[-1] if self._durs else None))

    # -------------------------------------------------------- Backends

    def _chain(self) -> list[str]:
        """B120: Kette statt Sackgasse.

        Vorher lieferte _chain() AUSSCHLIESSLICH ['llamacpp']. Lief der
        llama-server nicht (Standardfall auf der 8-Kern-Box, wenn kein
        GGUF geladen ist), gab chat() ok=False zurueck, der Router-Tier
        'llm' warf Unhandled — und /brain antwortete strukturell IMMER
        'keine Antwort'. Beim Ollama-Ausbau wurde der Cloud-Fallback
        vergessen; nc.freeai existiert, war hier aber nie verdrahtet.

        Reihenfolge bleibt lokal-zuerst: llama.cpp kostet nichts und
        verlaesst die Box nicht. 'freeai' greift nur, wenn lokal nichts
        antwortet. BRAIN_LLM_BACKEND=llamacpp erzwingt rein lokal."""
        conf = _backend_conf()
        if conf == "off":
            return []
        if conf == "llamacpp":
            return ["llamacpp"]          # bewusst ohne Cloud-Ausweg
        if conf == "freeai":
            return ["freeai"]
        return ["llamacpp", "freeai"]    # auto (Default) + unbekannte Werte

    def _call(self, backend: str, messages, timeout, max_tokens) -> str:
        if backend == "freeai":
            # Cloud-Reserve. Import LOKAL, damit brain/ dependency-frei
            # bleibt und ohne nc/ weiter importierbar ist (M1-Vertrag).
            from nc import freeai as _freeai
            txt, err = _freeai.chat_sync(messages, timeout=timeout)
            if not txt:
                raise RuntimeError(f"freeai: {err or 'leer'}")
            return txt
        if backend == "llamacpp":
            # llama-server spricht die OpenAI-kompatible API — Vorteil:
            # jeder andere OpenAI-kompatible lokale Server (vllm, etc.)
            # funktioniert ohne Codeänderung über BRAIN_LLAMACPP_URL.
            body = {"messages": messages, "max_tokens": max_tokens,
                    "temperature": 0.3, "stream": False}
            j = self._post(f"{_llamacpp_url()}/v1/chat/completions",
                           body, timeout)
            return j["choices"][0]["message"]["content"]
        raise ValueError(f"unbekanntes Backend: {backend}")

    def _probe(self, backend: str) -> dict:
        url = f"{_llamacpp_url()}/health"
        t0 = time.time()
        try:
            req = urllib.request.Request(url, method="GET")
            with urllib.request.urlopen(req, timeout=3) as r:
                r.read(256)
            return {"up": True,
                    "ms": round((time.time() - t0) * 1000, 1)}
        except Exception as e:
            return {"up": False, "error": f"{type(e).__name__}"}

    @staticmethod
    def _post(url: str, body: dict, timeout: float) -> dict:
        data = json.dumps(body).encode()
        req = urllib.request.Request(
            url, data=data, method="POST",
            headers={"Content-Type": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return json.loads(r.read().decode())
        except urllib.error.HTTPError as e:
            # B120: Body anhaengen. 'HTTPError: 400' allein sagt nicht,
            # ob das Modell fehlt oder der Prompt zu lang war.
            try:
                detail = e.read().decode("utf-8", "ignore")[:200]
            except Exception:
                detail = ""
            raise RuntimeError(f"HTTP {e.code}: {detail}") from None

    # ---------------------------------------------------------- Budget

    def _check_budget(self) -> None:
        b = self.budget()
        if b["remaining"] <= 0:
            with self._stats_lock:
                self._stats["budget_denied"] += 1
            raise BudgetExhausted(
                f"LLM-Stundenbudget verbraucht ({b['used_h']}/{b['max_h']})")
