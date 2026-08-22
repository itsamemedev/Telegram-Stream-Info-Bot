# brain/__init__.py — M1: Brain-Facade
#
# Einziger Import-Punkt für bot_v36:
#
#     from brain import get_brain
#     brain = get_brain()
#     brain.state.set("recorder", username, "running", pid=pid)
#     brain.rules.register("cpu_guard", cond, act, cooldown_s=300)
#     res = brain.router.route("should_record", {"user": u})
#     brain.start_tick(interval_s=10)   # optional: periodische Regelrunde
#
# WARUM eigene brain.db statt Tabellen in der bot-DB:
# M1 muss mit 0 Risiko integrierbar sein. Die bot-DB hat Migrationen,
# MariaDB-Translation-Layer und 258 Routen, die darauf zugreifen — jede
# Schema-Änderung dort ist ein Risiko. brain.db ist isoliert; geht sie
# kaputt, läuft der Bot unverändert weiter. Zusammenführung ist später
# möglich, M1 priorisiert Rückwärtskompatibilität.
#
# WARUM Persistenz überhaupt in M1 (statt erst M3): Transitions und
# Entscheidungen sind der Audit-Trail ("warum wurde entschieden?").
# Ohne Persistenz wäre nach jedem Neustart alles weg — für ein 24/7-
# System mit systemd-Restarts unbrauchbar. M3 baut darauf auf.

from __future__ import annotations

import contextlib
import json
import logging
import os
import sqlite3
import threading
import time
from typing import Optional

from nc.envnum import env_int  # v4.0-W81: leer-gesetzte .env-Ints robust (float war W78)

from .semantic import SemanticMemory
from .agents import (Agent, AgentManager, AnalyticsAgent, DiskAgent,
                     HealthAgent, LearningAgent, ProxyHealthAgent, RecoveryAgent,
                     RecordingAgent, RestreamSentinelAgent, ScoutAgent,
                     SentinelAgent, SwapAgent, ToxicityAgent, UptimeAgent)
from .knowledge import KnowledgeGraph
from .llm import BudgetExhausted, LLMRuntime
from .memory import Memory
from .scheduler import Scheduler
from .rules import RulesEngine
from .router import TaskRouter, Unhandled
from .state import StateMachine

# Öffentliche API des Pakets. WARUM __all__: pyflakes wertet Re-Exports
# sonst als 'imported but unused' — und die Bridge importiert Unhandled/
# BudgetExhausted bewusst von hier statt aus den Submodulen (ein Import-
# punkt, siehe M1-Vertrag).
__all__ = ["Agent", "AgentManager", "AnalyticsAgent", "Brain",
           "DiskAgent",
           "BudgetExhausted",
           "HealthAgent", "KnowledgeGraph", "LearningAgent", "ProxyHealthAgent",
           "RecordingAgent", "RecoveryAgent", "RestreamSentinelAgent", "ScoutAgent",
           "SentinelAgent", "SwapAgent", "ToxicityAgent", "UptimeAgent", "get_brain",
           "LLMRuntime", "Memory", "RulesEngine", "Scheduler",
           "StateMachine", "TaskRouter", "Unhandled"]

log = logging.getLogger("brain")

# WARUM Funktion statt Konstante: bot_v36 lädt .env teils NACH ersten
# Imports. Eine Import-Zeit-Konstante würde den Env-Wert einfrieren,
# bevor er existiert → falsche DB-Datei. Lookup daher pro Brain-Init.
def _brain_db_path() -> str:
    return os.getenv("BRAIN_DB", "brain.db")

_SCHEMA = """
CREATE TABLE IF NOT EXISTS transitions(
    ts REAL, kind TEXT, key TEXT, old TEXT, new TEXT, attrs TEXT);
CREATE INDEX IF NOT EXISTS idx_trans_ts ON transitions(ts);
CREATE TABLE IF NOT EXISTS decisions(
    ts REAL, rule TEXT, reason TEXT, result TEXT, trigger TEXT, tags TEXT);
CREATE INDEX IF NOT EXISTS idx_dec_ts ON decisions(ts);
"""

# Aufbewahrung in Tagen; 0 = unbegrenzt. Klein halten: brain.db soll
# nie zum Disk-Problem werden, das ihre eigenen Regeln melden müssten.
RETAIN_DAYS = env_int("BRAIN_RETAIN_DAYS", 14)


class Brain:
    def __init__(self, db_path: Optional[str] = None):
        db_path = db_path or _brain_db_path()
        self.state = StateMachine()
        self.rules = RulesEngine()
        self.router = TaskRouter()
        self._db_path = db_path
        self._db_lock = threading.Lock()
        self._tick_thread: Optional[threading.Thread] = None
        self._stop = threading.Event()
        # BH-2: Heartbeat des letzten Ticks — egal ob Brain.start_tick
        # oder der Bridge-Tick ihn treibt. overview() wertet das aus,
        # sonst zeigt das Dashboard TICK TOT trotz laufender Bridge.
        self.last_tick_ts: float = 0.0
        # BH-8: GC-Zeitpunkt gehört zum Tick selbst, nicht zum (optionalen)
        # start_tick-Thread. Die Bridge fährt ihren eigenen Tick — vorher
        # lief die Retention in Produktion daher NIE und brain.db wuchs
        # unbegrenzt, bis die 200MB-Warnregel den Operator alarmierte.
        self._last_gc: float = 0.0
        self._init_db()
        # Persistenz-Sinks einhängen: jede Transition/Entscheidung → SQLite
        self.state.on_transition(self._persist_transition)
        self.rules.set_sink(self._persist_decision)
        # M3: Memory teilt Connection-Factory+Lock des Brains (EIN
        # Schreibpfad auf brain.db). Der Session-Hook MUSS nach dem
        # Transition-Persistenz-Hook registriert sein: _close_session
        # liest die transitions-Tabelle (recorded-Flag) — das online-
        # Event muss also bereits geschrieben sein, wenn Memory dran ist.
        self.memory = Memory(self._conn, self._db_lock)
        self.state.on_transition(self.memory.observe_transition)
        # M4: Knowledge Graph — gleicher Schreibpfad (Factory+Lock).
        self.knowledge = KnowledgeGraph(self._conn, self._db_lock)
        # M5: Scheduler — Prognosen + Prioritätsplanung, Hints in brain.db.
        self.scheduler = Scheduler(self._conn, self._db_lock)
        # M6: LLM-Runtime (Tier 4). Lazy — verbindet erst beim 1. Call.
        self.llm = LLMRuntime()
        # M7: Agent-Manager. Konkrete Agenten registriert die Bridge
        # (RecoveryAgent braucht bot-DB-Zugriff und das Aktions-Gate).
        self.agents = AgentManager(self)
        # V37-W-PLUS: semantisches Gedächtnis (Embeddings, Cosine-Suche)
        self.semantic = SemanticMemory(self._conn, self._db_lock)
        # Router-Tier 'rules' standardmäßig auf die Engine legen:
        # ein Task 'evaluate' triggert eine Regelrunde mit Task-Payload.
        self.router.register("rules", "evaluate", self._route_evaluate)

    # ------------------------------------------------------------- Tick

    def start_tick(self, interval_s: float = 10.0) -> None:
        """Periodische Regelrunde in eigenem Daemon-Thread.

        WARUM Thread statt asyncio-Task: Das Brain muss auch weiterlaufen,
        wenn der asyncio-Loop von bot_v36 hängt (genau DAS soll eine
        Watchdog-Regel ja erkennen können). Daemon=True: blockiert kein
        Shutdown."""
        if self._tick_thread and self._tick_thread.is_alive():
            return
        self._stop.clear()

        def _run():
            log.info("Brain-Tick gestartet (%.0fs)", interval_s)
            while not self._stop.wait(interval_s):
                try:
                    self.tick()   # BH-8: tick() übernimmt auch die Retention
                except Exception:
                    log.exception("Brain-Tick-Fehler (isoliert)")

        self._tick_thread = threading.Thread(
            target=_run, name="brain-tick", daemon=True)
        self._tick_thread.start()

    def stop_tick(self) -> None:
        self._stop.set()

    def tick(self, extra_ctx: Optional[dict] = None) -> list[dict]:
        """Eine Bewertungsrunde: State-Snapshot + optionale Telemetrie."""
        self.last_tick_ts = time.time()
        # BH-8: Retention stündlich, unabhängig davon, welcher Thread tickt.
        if RETAIN_DAYS and self.last_tick_ts - self._last_gc > 3600:
            self._last_gc = self.last_tick_ts
            try:
                self._gc()
            except Exception:
                log.exception("brain.db-Retention fehlgeschlagen (isoliert)")
        ctx = {"state": self.state.snapshot(), "trigger": "tick",
               "ts": self.last_tick_ts}
        if extra_ctx:
            ctx.update(extra_ctx)
        return self.rules.evaluate(ctx)

    # -------------------------------------------------- Dashboard-Sicht

    def overview(self) -> dict:
        """Ein Call für den künftigen 'AI Brain'-Tab (M8)."""
        return {
            "state": self.state.snapshot(),
            "rules": self.rules.rules_status(),
            "decisions": self.rules.decisions(50),
            "router": {"stats": self.router.stats(),
                       "log": self.router.log(50)},
            # BH-2: lebendig = eigener Thread ODER frischer Heartbeat
            # (Bridge-Tick). 60s Toleranz deckt BRAIN_TICK_S bis 20s ab.
            "tick_alive": bool(
                (self._tick_thread and self._tick_thread.is_alive())
                or (time.time() - self.last_tick_ts < 60)),
        }

    def why(self, limit: int = 20) -> list[dict]:
        """Letzte Entscheidungen inkl. Begründung aus der DB (persistent,
        überlebt Neustarts — anders als rules.decisions())."""
        with self._db_lock, self._conn() as c:
            rows = c.execute(
                "SELECT ts, rule, reason, result, trigger, tags "
                "FROM decisions ORDER BY ts DESC LIMIT ?", (limit,)
            ).fetchall()
        return [{"ts": r[0], "rule": r[1], "reason": _unjson(r[2]),
                 "result": _unjson(r[3]), "trigger": r[4],
                 "tags": _unjson(r[5])} for r in rows]

    # -------------------------------------------------------- intern

    @contextlib.contextmanager
    def _conn(self):
        # check_same_thread=False + eigener Lock: Zugriffe kommen aus
        # Tick-Thread, Flask-Threads UND asyncio-Kontext.
        # BH-5: Contextmanager mit explizitem close(). Vorher wurde die
        # Connection nur per CPython-Refcounting geschlossen — Exceptions
        # mit gehaltenen Tracebacks können Frames (und damit fds) pinnen,
        # und auf alternativen Runtimes (PyPy) leckt es sicher. commit bei
        # Erfolg, rollback bei Exception, close IMMER.
        conn = sqlite3.connect(self._db_path, timeout=10,
                               check_same_thread=False)
        try:
            conn.execute("PRAGMA journal_mode=WAL")
            conn.execute("PRAGMA synchronous=NORMAL")  # IMP-9
            yield conn
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    def _init_db(self) -> None:
        with self._db_lock, self._conn() as c:
            c.executescript(_SCHEMA)

    def _persist_transition(self, ev: dict) -> None:
        try:
            with self._db_lock, self._conn() as c:
                c.execute(
                    "INSERT INTO transitions VALUES(?,?,?,?,?,?)",
                    (ev["ts"], ev["kind"], ev["key"], ev["old"], ev["new"],
                     json.dumps(ev["attrs"], default=str)))
        except Exception:
            log.debug("Transition-Persistenz fehlgeschlagen", exc_info=True)

    def _persist_decision(self, entry: dict) -> None:
        try:
            with self._db_lock, self._conn() as c:
                c.execute(
                    "INSERT INTO decisions VALUES(?,?,?,?,?,?)",
                    (entry["ts"], entry["rule"],
                     json.dumps(entry["reason"], default=str),
                     json.dumps(entry["result"], default=str),
                     entry["trigger"],
                     json.dumps(entry["tags"], default=str)))
        except Exception:
            log.debug("Decision-Persistenz fehlgeschlagen", exc_info=True)

    def _route_evaluate(self, task) -> list[dict]:
        fired = self.tick(extra_ctx=dict(task.payload,
                                         trigger=f"task:{task.topic}"))
        if not fired:
            raise Unhandled("keine Regel hat gefeuert")
        return fired

    def _gc(self) -> None:
        cutoff = time.time() - RETAIN_DAYS * 86400
        try:
            with self._db_lock, self._conn() as c:
                c.execute("DELETE FROM transitions WHERE ts < ?", (cutoff,))
                c.execute("DELETE FROM decisions WHERE ts < ?", (cutoff,))
        except Exception:
            log.debug("brain.db GC fehlgeschlagen", exc_info=True)
        self.memory.gc(RETAIN_DAYS)     # M3: events/metrics/sessions


def _unjson(s):
    try:
        return json.loads(s)
    except Exception:
        return s


# Singleton: bot_v36 und alle Module teilen EIN Brain.
_BRAIN: Optional[Brain] = None
_BRAIN_LOCK = threading.Lock()


def get_brain() -> Brain:
    global _BRAIN
    with _BRAIN_LOCK:
        if _BRAIN is None:
            _BRAIN = Brain()
        return _BRAIN
