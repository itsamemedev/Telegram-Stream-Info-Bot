# brain/state.py — M1: Zentrale State Machine
#
# WARUM eigenes Modul statt globaler Dicts in bot_v36:
# bot_v36 hält Zustand in ~20 verstreuten Globals (Recordings, Restreams,
# Proxy-Pool, Agenten). Keine Komponente kann fragen "was läuft GERADE alles?"
# ohne 20 Stellen zu kennen. Die StateMachine ist EIN thread-sicherer
# Snapshot-Punkt. Sie ERSETZT die Globals nicht (Rückwärtskompatibilität!),
# sie spiegelt sie: Komponenten melden Zustandswechsel per set()/transition().
#
# WARUM threading.RLock statt asyncio.Lock: bot_v36 mischt asyncio-Loops
# (Recorder, Watchdogs) mit Flask-Threads (Dashboard). Ein asyncio.Lock wäre
# aus Flask-Threads nicht benutzbar. RLock funktioniert aus beiden Welten,
# und alle Operationen hier sind Mikrosekunden-kurz (kein I/O unter Lock).

from __future__ import annotations

import threading
import time
from collections import deque
from typing import Callable, Optional

# Entitätstypen, die das System kennt. Bewusst Strings statt Enum:
# bot_v36 soll neue Typen melden können ohne brain/ zu ändern.
KNOWN_KINDS = ("stream", "recorder", "restream", "upload", "agent",
               "process", "error", "proxy", "resource")


class Entity:
    """Ein beobachtetes Ding (Stream, Recorder, Agent, ...) mit Zustand.

    WARUM attrs-Dict statt fester Felder: Ein Recorder hat pid+datei,
    ein Stream hat viewer+kategorie, ein Agent hat persona. Ein starres
    Schema würde bei jedem neuen Executor eine brain/-Änderung erzwingen.
    """

    __slots__ = ("kind", "key", "state", "attrs", "since", "updated")

    def __init__(self, kind: str, key: str, state: str,
                 attrs: Optional[dict] = None):
        self.kind = kind
        self.key = key
        self.state = state
        self.attrs = dict(attrs or {})
        self.since = time.time()      # Beginn des AKTUELLEN Zustands
        self.updated = self.since

    def as_dict(self) -> dict:
        return {
            "kind": self.kind, "key": self.key, "state": self.state,
            "attrs": dict(self.attrs),
            "since": self.since, "updated": self.updated,
            "age_s": round(time.time() - self.since, 1),
        }


class StateMachine:
    """Thread-sicherer Zustandsspiegel des Gesamtsystems.

    Beantwortet jederzeit: welche Streams online, welche Recorder laufen,
    welche Prozesse/Uploads/Agenten aktiv, welche Fehler offen.
    """

    # Ringpuffer-Größe der Transition-Historie. 500 reicht für Dashboard
    # und Regel-Debugging; Langzeit-Persistenz übernimmt M3 (Memory).
    HISTORY = 500

    def __init__(self):
        self._lock = threading.RLock()
        self._entities: dict[tuple[str, str], Entity] = {}
        self._history: deque = deque(maxlen=self.HISTORY)
        # Listener werden bei jeder Transition gerufen (z.B. Rules Engine
        # im Event-Modus, Memory-Sink). Fehler in Listenern dürfen NIEMALS
        # die meldende Komponente (Recorder!) crashen → try/except.
        self._listeners: list[Callable[[dict], None]] = []

    # ------------------------------------------------------------- API

    def set(self, kind: str, key: str, state: str, **attrs) -> None:
        """Zustand setzen/aktualisieren. Idempotent: gleicher Zustand
        aktualisiert nur attrs+updated, erzeugt KEINE Transition
        (sonst würde ein 10s-Poll-Loop die Historie fluten)."""
        ev = None
        with self._lock:
            ent = self._entities.get((kind, key))
            now = time.time()
            if ent is None:
                ent = Entity(kind, key, state, attrs)
                self._entities[(kind, key)] = ent
                ev = self._mk_event(ent, old=None)
            elif ent.state != state:
                old = ent.state
                ent.state = state
                ent.since = now
                ent.attrs.update(attrs)
                ent.updated = now
                ev = self._mk_event(ent, old=old)
            else:
                ent.attrs.update(attrs)
                ent.updated = now
        if ev:
            self._emit(ev)

    def remove(self, kind: str, key: str) -> None:
        """Entität entfernen (Stream offline+vergessen, Agent deaktiviert).
        Erzeugt eine finale 'gone'-Transition für die Historie."""
        ev = None
        with self._lock:
            ent = self._entities.pop((kind, key), None)
            if ent:
                old = ent.state
                ent.state = "gone"
                ev = self._mk_event(ent, old=old)
        if ev:
            self._emit(ev)

    def get(self, kind: str, key: str) -> Optional[dict]:
        with self._lock:
            ent = self._entities.get((kind, key))
            return ent.as_dict() if ent else None

    def query(self, kind: Optional[str] = None,
              state: Optional[str] = None) -> list[dict]:
        """Filterbare Sicht: query('recorder', 'running') etc."""
        with self._lock:
            out = []
            for ent in self._entities.values():
                if kind and ent.kind != kind:
                    continue
                if state and ent.state != state:
                    continue
                out.append(ent.as_dict())
            return out

    def snapshot(self) -> dict:
        """Kompletter Systemzustand als ein Dict — für Dashboard,
        Regeln und (später) LLM-Kontext."""
        with self._lock:
            counts: dict[str, dict[str, int]] = {}
            for ent in self._entities.values():
                counts.setdefault(ent.kind, {}).setdefault(ent.state, 0)
                counts[ent.kind][ent.state] += 1
            return {
                "ts": time.time(),
                "counts": counts,
                "entities": [e.as_dict() for e in self._entities.values()],
            }

    def history(self, limit: int = 100) -> list[dict]:
        with self._lock:
            return list(self._history)[-limit:]

    def on_transition(self, fn: Callable[[dict], None]) -> None:
        with self._lock:
            self._listeners.append(fn)

    # -------------------------------------------------------- intern

    def _mk_event(self, ent: Entity, old: Optional[str]) -> dict:
        ev = {"ts": time.time(), "kind": ent.kind, "key": ent.key,
              "old": old, "new": ent.state, "attrs": dict(ent.attrs)}
        self._history.append(ev)
        return ev

    def _emit(self, ev: dict) -> None:
        # Listener außerhalb des Locks rufen: verhindert Deadlock, wenn
        # ein Listener selbst state.set() aufruft (Rules-Aktionen tun das).
        for fn in list(self._listeners):
            try:
                fn(ev)
            except Exception:
                # Bewusst still: State-Meldung darf nie am Listener sterben.
                # Logging übernimmt der Brain-Facade-Layer (hat den Logger).
                pass


def _selftest() -> None:
    sm = StateMachine()
    events: list[dict] = []
    sm.on_transition(events.append)

    sm.set("recorder", "userA", "running", pid=1234)
    sm.set("recorder", "userA", "running", pid=1234)   # idempotent
    sm.set("recorder", "userA", "stalled")
    sm.set("stream", "userB", "online", viewers=500)
    assert len(events) == 3, events                     # kein Event für Dup
    assert sm.get("recorder", "userA")["state"] == "stalled"
    assert len(sm.query("recorder")) == 1
    assert sm.snapshot()["counts"]["stream"]["online"] == 1
    sm.remove("stream", "userB")
    assert sm.get("stream", "userB") is None
    assert sm.history()[-1]["new"] == "gone"
    print("state.py selftest OK")


if __name__ == "__main__":
    _selftest()
