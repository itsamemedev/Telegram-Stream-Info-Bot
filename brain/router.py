# brain/router.py — M1: Task Router (Tier-Kaskade)
#
# Kernprinzip v37: Das LLM ist die LETZTE Instanz, nicht die erste.
#
#   Task → Tier RULES  (deterministisch, µs)
#        → Tier DB     (Faktenabfrage, ms)
#        → Tier KNOWLEDGE (Graph-Inferenz, ms — M4)
#        → Tier LLM    (nur wenn nichts anderes kann — M6)
#
# WARUM Handler-Registrierung statt Hardcoding: Der Router kennt bot_v36
# nicht. bot_v36 (bzw. M2-Shim) registriert Handler wie
#   router.register("db", "stream_stats", handler_fn)
# Dadurch bleibt brain/ ohne einen einzigen Import aus bot_v36 →
# separat testbar, keine Zirkularimporte im 28k-Zeilen-Monolithen.
#
# Jede Routing-Entscheidung wird geloggt: welcher Tier hat geantwortet,
# warum die vorherigen Tiers nicht konnten → Dashboard-Erklärbarkeit.

from __future__ import annotations

import threading
import time
from typing import Any, Callable, Optional

# Reihenfolge ist Vertrag: billig → teuer. LLM immer zuletzt.
TIERS = ("rules", "db", "knowledge", "llm")


class Unhandled(Exception):
    """Handler signalisiert: 'ich bin zwar zuständig registriert, kann
    DIESEN konkreten Task aber nicht lösen' → Router probiert nächsten
    Tier. Bewusst eine Exception statt None-Rückgabe: None kann eine
    legitime Antwort sein ('Streamer hat keine Kategorie')."""


class Task:
    __slots__ = ("topic", "payload", "created", "id")
    _seq = 0
    _seq_lock = threading.Lock()

    def __init__(self, topic: str, payload: Optional[dict] = None):
        self.topic = topic
        self.payload = dict(payload or {})
        self.created = time.time()
        with Task._seq_lock:
            Task._seq += 1
            self.id = Task._seq


class TaskRouter:
    LOG_MAX = 500

    def __init__(self):
        self._lock = threading.RLock()
        # {tier: {topic: handler}} — '*' als topic = Catch-all des Tiers
        self._handlers: dict[str, dict[str, Callable]] = {t: {} for t in TIERS}
        self._log: list[dict] = []
        self._stats = {t: {"handled": 0, "passed": 0, "errors": 0}
                       for t in TIERS}

    # ------------------------------------------------------------- API

    def register(self, tier: str, topic: str,
                 handler: Callable[[Task], Any]) -> None:
        if tier not in TIERS:
            raise ValueError(f"unbekannter Tier: {tier!r}, erlaubt: {TIERS}")
        with self._lock:
            self._handlers[tier][topic] = handler

    def route(self, topic: str, payload: Optional[dict] = None) -> dict:
        """Task durch die Kaskade schicken.

        Rückgabe immer ein Dict:
          {ok, tier, result | error, trace}
        trace = pro Tier, warum weitergereicht wurde → das WARUM fürs
        Dashboard ("Regel konnte nicht → DB hat geantwortet").
        """
        task = Task(topic, payload)
        trace: list[dict] = []
        for tier in TIERS:
            handler = self._pick(tier, topic)
            if handler is None:
                trace.append({"tier": tier, "skip": "kein Handler"})
                continue
            t0 = time.time()
            try:
                result = handler(task)
            except Unhandled as u:
                self._bump(tier, "passed")
                trace.append({"tier": tier,
                              "skip": str(u) or "Handler passt"})
                continue
            except Exception as e:
                # Tier-Fehler = weiterreichen, nicht abbrechen: ein DB-
                # Timeout darf eine Knowledge-Antwort nicht verhindern.
                self._bump(tier, "errors")
                trace.append({"tier": tier,
                              "error": f"{type(e).__name__}: {e}"})
                continue
            self._bump(tier, "handled")
            entry = self._log_route(task, tier, trace, ok=True,
                                    ms=(time.time() - t0) * 1000)
            return {"ok": True, "tier": tier, "result": result,
                    "trace": trace, "task_id": task.id,
                    "ms": entry["ms"]}
        self._log_route(task, None, trace, ok=False, ms=0.0)
        return {"ok": False, "tier": None, "trace": trace,
                "task_id": task.id,
                "error": "kein Tier konnte den Task lösen"}

    def stats(self) -> dict:
        with self._lock:
            return {t: dict(v) for t, v in self._stats.items()}

    def log(self, limit: int = 100) -> list[dict]:
        with self._lock:
            return self._log[-limit:]

    # -------------------------------------------------------- intern

    def _pick(self, tier: str, topic: str) -> Optional[Callable]:
        with self._lock:
            h = self._handlers[tier]
            return h.get(topic) or h.get("*")

    def _bump(self, tier: str, key: str) -> None:
        with self._lock:
            self._stats[tier][key] += 1

    def _log_route(self, task: Task, tier: Optional[str],
                   trace: list, ok: bool, ms: float) -> dict:
        entry = {"ts": time.time(), "task_id": task.id, "topic": task.topic,
                 "tier": tier, "ok": ok, "ms": round(ms, 2),
                 "trace": list(trace)}
        with self._lock:
            self._log.append(entry)
            if len(self._log) > self.LOG_MAX:
                del self._log[: len(self._log) - self.LOG_MAX]
        return entry


def _selftest() -> None:
    r = TaskRouter()

    # Tier 'rules' kann nur bekannte Streamer, sonst weiterreichen
    def rules_h(task: Task):
        if task.payload.get("user") != "known":
            raise Unhandled("Regelwerk kennt User nicht")
        return {"decision": "record"}

    r.register("rules", "should_record", rules_h)
    r.register("db", "should_record", lambda t: {"decision": "skip",
                                                 "src": "history"})
    # LLM-Tier absichtlich NICHT registriert → M6

    res = r.route("should_record", {"user": "known"})
    assert res["ok"] and res["tier"] == "rules"

    res = r.route("should_record", {"user": "stranger"})
    assert res["ok"] and res["tier"] == "db"
    assert any("kennt User nicht" in str(t.get("skip", ""))
               for t in res["trace"])                 # WARUM nachvollziehbar

    res = r.route("unbekanntes_topic")
    assert not res["ok"] and len(res["trace"]) == 4   # alle 4 Tiers probiert

    s = r.stats()
    assert s["rules"]["handled"] == 1 and s["rules"]["passed"] == 1
    assert s["db"]["handled"] == 1
    print("router.py selftest OK")


if __name__ == "__main__":
    _selftest()
