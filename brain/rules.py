# brain/rules.py — M1: Deterministische Rules Engine
#
# WARUM: bot_v36 hat 33 Loops, die jeweils "wenn X dann Y" prüfen
# (Disk voll → Alarm, Recorder stalled → Kill, Cookie alt → Refresh).
# Diese Logik bleibt WO SIE IST (Rückwärtskompatibilität), aber NEUE
# Automatik-Regeln kommen hierher: deklarativ, zentral, mit Cooldown,
# Prioritäten, Ein/Aus-Schalter und einem Entscheidungslog, das die
# Frage "WARUM wurde das getan?" beantwortet — Kernanforderung v37.
#
# WARUM hier NIEMALS ein LLM: Reconnects, Recording, CPU, RAM, Netzwerk,
# Health Checks, Watchdogs, Retries sind deterministisch entscheidbar.
# Ein LLM würde nur Latenz, RAM und Unvorhersagbarkeit hinzufügen.
# Diese Engine hat keinerlei Import-Pfad Richtung LLM — by design.

from __future__ import annotations

import threading
import time
import traceback
from dataclasses import dataclass, field
from typing import Any, Callable, Optional


@dataclass
class Rule:
    """Eine Regel: name + condition + action.

    condition(ctx) -> truthy  → action(ctx) wird ausgeführt.
    Gibt condition ein Dict/String zurück, landet es als 'reason' im
    Entscheidungslog — so erklärt jede Regel selbst ihr WARUM.

    cooldown_s: Mindestabstand zwischen zwei Ausführungen. Verhindert,
    dass eine Dauerbedingung (Disk seit 1h voll) die Aktion (Telegram-
    Alarm!) im Sekundentakt feuert. 0 = jede Runde erlaubt.

    priority: kleinere Zahl = früher geprüft. Wichtig, wenn Aktionen
    denselben Engpass betreffen (erst Recording stoppen, dann aufräumen).
    """
    name: str
    condition: Callable[[dict], Any]
    action: Callable[[dict], Any]
    cooldown_s: float = 0.0
    priority: int = 100
    enabled: bool = True
    tags: tuple = ()
    # Laufzeitstatistik (Dashboard: welche Regeln arbeiten wirklich?)
    hits: int = 0
    errors: int = 0
    last_fired: float = 0.0
    last_error: str = ""
    _created: float = field(default_factory=time.time)


class RulesEngine:
    """Zentrale, LLM-freie Entscheidungsschicht (Tier 1 des Routers)."""

    # Entscheidungslog-Größe im RAM. Persistenz → M3 (Memory) via Sink.
    LOG_MAX = 1000

    def __init__(self):
        self._lock = threading.RLock()
        self._rules: dict[str, Rule] = {}
        self._log: list[dict] = []
        # BH-4: evaluate() kann konkurrent laufen (Bridge-Tick-Thread UND
        # Flask via router-Topic 'evaluate'). Cooldown-Check und last_fired-
        # Update waren nicht atomar → Doppel-Feuern derselben Regel möglich
        # (doppelte Telegram-Alarme). RLock statt Lock, weil eine Regel-
        # Aktion ihrerseits router.route('evaluate') anstoßen darf, ohne
        # sich selbst zu deadlocken.
        self._eval_lock = threading.RLock()
        # Optionaler Sink (M3 hängt hier die SQLite-Persistenz ein).
        self._sink: Optional[Callable[[dict], None]] = None

    # ------------------------------------------------------------- API

    def register(self, name: str, condition: Callable, action: Callable,
                 cooldown_s: float = 0.0, priority: int = 100,
                 tags: tuple = (), enabled: bool = True) -> Rule:
        """Regel registrieren. Gleicher Name überschreibt (Redeploy-Fall:
        Modul registriert seine Regeln beim Import neu)."""
        rule = Rule(name=name, condition=condition, action=action,
                    cooldown_s=cooldown_s, priority=priority,
                    tags=tuple(tags), enabled=enabled)
        with self._lock:
            self._rules[name] = rule
        return rule

    def enable(self, name: str, on: bool = True) -> bool:
        with self._lock:
            r = self._rules.get(name)
            if not r:
                return False
            r.enabled = on
            return True

    def evaluate(self, ctx: dict) -> list[dict]:
        """Eine Bewertungsrunde über alle Regeln.

        ctx enthält mindestens den State-Snapshot ('state') plus alles,
        was der Aufrufer mitgibt (Telemetrie, Event). Rückgabe: Liste
        der in dieser Runde gefeuerten Entscheidungen.

        WARUM Fehler pro Regel isoliert: Eine kaputte Regel (Tippfehler
        in condition) darf niemals die restlichen 40 Regeln oder gar den
        aufrufenden Loop töten — 24/7-Anforderung.
        """
        with self._lock:
            rules = sorted((r for r in self._rules.values() if r.enabled),
                           key=lambda r: r.priority)
        fired: list[dict] = []
        with self._eval_lock:                      # BH-4: Runden serialisiert
            now = time.time()
            for rule in rules:
                try:
                    reason = rule.condition(ctx)
                except Exception as e:
                    self._note_error(rule, e)
                    continue
                if not reason:
                    continue
                if rule.cooldown_s and (now - rule.last_fired) < rule.cooldown_s:
                    continue    # Bedingung wahr, aber Cooldown → bewusst still
                try:
                    result = rule.action(ctx)
                except Exception as e:
                    self._note_error(rule, e)
                    continue
                rule.hits += 1
                rule.last_fired = now
                entry = self._log_decision(rule, reason, result, ctx)
                fired.append(entry)
        return fired

    def rules_status(self) -> list[dict]:
        """Für Dashboard: alle Regeln + Statistik."""
        with self._lock:
            return [{
                "name": r.name, "enabled": r.enabled, "priority": r.priority,
                "cooldown_s": r.cooldown_s, "tags": list(r.tags),
                "hits": r.hits, "errors": r.errors,
                "last_fired": r.last_fired, "last_error": r.last_error,
            } for r in sorted(self._rules.values(), key=lambda r: r.priority)]

    def decisions(self, limit: int = 100) -> list[dict]:
        with self._lock:
            return self._log[-limit:]

    def set_sink(self, fn: Callable[[dict], None]) -> None:
        """M3 hängt hier Persistenz ein (jede Entscheidung → SQLite)."""
        self._sink = fn

    # -------------------------------------------------------- intern

    def _log_decision(self, rule: Rule, reason: Any, result: Any,
                      ctx: dict) -> dict:
        entry = {
            "ts": time.time(),
            "rule": rule.name,
            "tags": list(rule.tags),
            # 'reason' = das WARUM. String/Dict der condition, sonst True.
            "reason": reason if isinstance(reason, (str, dict)) else True,
            "result": result if isinstance(result, (str, dict, int, float,
                                                    bool)) else str(result),
            "trigger": ctx.get("trigger", "tick"),
        }
        with self._lock:
            self._log.append(entry)
            if len(self._log) > self.LOG_MAX:
                del self._log[: len(self._log) - self.LOG_MAX]
        if self._sink:
            try:
                self._sink(entry)
            except Exception:
                pass    # Persistenz-Ausfall darf Entscheidungen nicht stoppen
        return entry

    def _note_error(self, rule: Rule, e: Exception) -> None:
        with self._lock:
            rule.errors += 1
            rule.last_error = f"{type(e).__name__}: {e}"
        # Traceback nur einmalig pro Fehlerstelle interessant → Debug-Ebene
        # übernimmt der Facade-Logger; hier bewusst kein print/log-Import.
        _ = traceback.format_exc()


def _selftest() -> None:
    eng = RulesEngine()
    hits: list[str] = []

    eng.register(
        "disk_warn",
        condition=lambda c: (f"disk {c['disk_pct']}% > 90%"
                             if c.get("disk_pct", 0) > 90 else None),
        action=lambda c: hits.append("warned") or "alert_sent",
        cooldown_s=60, priority=10, tags=("resource",))
    eng.register(
        "broken_rule",
        condition=lambda c: c["missing_key"],   # wirft KeyError
        action=lambda c: None, priority=5)

    fired = eng.evaluate({"disk_pct": 95})
    assert len(fired) == 1 and fired[0]["rule"] == "disk_warn"
    assert "95%" in fired[0]["reason"]                 # WARUM erklärt
    fired = eng.evaluate({"disk_pct": 96})             # Cooldown greift
    assert fired == []
    st = {r["name"]: r for r in eng.rules_status()}
    assert st["broken_rule"]["errors"] == 2            # isoliert, 2 Runden
    assert st["disk_warn"]["hits"] == 1
    assert eng.enable("disk_warn", False) and not eng.evaluate({"disk_pct": 99})
    print("rules.py selftest OK")


if __name__ == "__main__":
    _selftest()
