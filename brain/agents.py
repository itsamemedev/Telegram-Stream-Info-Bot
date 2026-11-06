# brain/agents.py — M7: Multi-Agent-Framework
#
# ROLLENTEILUNG: Regeln (M2) sind Reflexe — eine Bedingung, eine Aktion,
# jede Runde. Agenten sind Spezialisten mit eigenem Takt und mehrstufiger
# Logik (beobachten → bewerten → befinden). Beide loggen ins selbe
# Entscheidungssystem; Agenten-Befunde landen als Events im Memory und
# als Entitäten (kind='agent') in der StateMachine.
#
# ABGRENZUNG zu den AZRAEL-Personas in bot_v36: Die 5 Chat-Personas
# (Kick/Discord/TikTok) bleiben, wo sie sind — sie sind Kommunikation.
# Brain-Agenten sind Betrieb. Gleicher Namensraum (AZRAEL-Flotte),
# getrennte Zuständigkeit.
#
# JEDER Agent: einzeln aktivierbar/deaktivierbar (Laufzeit-Toggle,
# persistiert in brain.db → überlebt Neustart), Fehler-isoliert,
# mit Laufstatistik. Ein toter Agent kann NIE den Tick töten.

from __future__ import annotations

import logging
import os
import threading
import time
from typing import Callable, Optional

from nc.envnum import env_float, env_int  # v4.0-W78/W81: leer-gesetzte .env robust

log = logging.getLogger("brain.agents")

_SCHEMA = """
CREATE TABLE IF NOT EXISTS agent_config(
    name TEXT PRIMARY KEY,
    enabled INTEGER DEFAULT 1);
"""


class Agent:
    """Basisklasse. Konkrete Agenten überschreiben run(ctx) und geben
    eine Liste von Befunden zurück: [{level, text, ...}]. level:
    info|warn|crit — crit geht zusätzlich an notify."""

    name = "agent"
    interval_s = 300.0

    def run(self, ctx: dict) -> list[dict]:      # pragma: no cover
        raise NotImplementedError


class AgentManager:
    def __init__(self, brain, notify: Optional[Callable[[str], None]] = None):
        self._brain = brain
        self._notify = notify
        self._agents: dict[str, Agent] = {}
        self._enabled: dict[str, bool] = {}
        self._last_run: dict[str, float] = {}
        self._stats: dict[str, dict] = {}
        self._lock = threading.RLock()
        with brain._db_lock, brain._conn() as c:
            c.executescript(_SCHEMA)

    # ------------------------------------------------------------- API

    def register(self, agent: Agent) -> None:
        with self._lock:
            self._agents[agent.name] = agent
            self._enabled[agent.name] = self._load_enabled(agent.name)
            self._stats.setdefault(agent.name, {
                "runs": 0, "errors": 0, "findings": 0,
                "last_error": "", "last_ms": 0.0})
        self._brain.state.set(
            "agent", agent.name,
            "idle" if self._enabled[agent.name] else "disabled",
            interval_s=agent.interval_s)

    def enable(self, name: str, on: bool = True) -> bool:
        with self._lock:
            if name not in self._agents:
                return False
            self._enabled[name] = on
        with self._brain._db_lock, self._brain._conn() as c:
            c.execute("INSERT INTO agent_config VALUES(?,?) "
                      "ON CONFLICT(name) DO UPDATE SET enabled=excluded.enabled",
                      (name, 1 if on else 0))
        self._brain.state.set("agent", name, "idle" if on else "disabled")
        return True

    def run_due(self, ctx: dict) -> list[dict]:
        """Vom Bridge-Tick gerufen: alle fälligen, aktiven Agenten laufen
        lassen. Rückgabe: alle Befunde dieser Runde."""
        now = time.time()
        out: list[dict] = []
        with self._lock:
            due = [a for a in self._agents.values()
                   if self._enabled.get(a.name)
                   and now - self._last_run.get(a.name, 0) >= a.interval_s]
        for agent in due:
            out.extend(self.run_one(agent.name, ctx))
        return out

    def run_one(self, name: str, ctx: dict) -> list[dict]:
        with self._lock:
            agent = self._agents.get(name)
            if not agent:
                return []
            self._last_run[name] = time.time()
            st = self._stats[name]
        t0 = time.time()
        try:
            findings = agent.run(ctx) or []
        except Exception as e:
            with self._lock:
                st["errors"] += 1
                st["last_error"] = f"{type(e).__name__}: {e}"
            self._brain.state.set("agent", name, "error",
                                  error=st["last_error"])
            log.exception("Agent %s fehlgeschlagen (isoliert)", name)
            return []
        ms = round((time.time() - t0) * 1000, 1)
        with self._lock:
            st["runs"] += 1
            st["findings"] += len(findings)
            st["last_ms"] = ms
        # IMP-3: idempotent — erzeugt nur beim Wechsel error→idle (Erholung)
        # eine Transition, sonst reines attrs-Update ohne DB-Zeile.
        self._brain.state.set("agent", name, "idle", last_ms=ms,
                              last_findings=len(findings))
        for f in findings:
            f.setdefault("agent", name)
            self._brain.memory.record_event("agent_finding", name, **f)
            if f.get("level") == "crit" and self._notify:
                try:
                    self._notify(f"🤖 [{name}] {f.get('text', '')}")
                except Exception:
                    pass
        return findings

    def status(self) -> list[dict]:
        with self._lock:
            return [{
                "name": a.name, "enabled": self._enabled.get(a.name, False),
                "interval_s": a.interval_s,
                "last_run": self._last_run.get(a.name, 0),
                **self._stats.get(a.name, {}),
            } for a in self._agents.values()]

    def _load_enabled(self, name: str) -> bool:
        with self._brain._db_lock, self._brain._conn() as c:
            row = c.execute("SELECT enabled FROM agent_config WHERE name=?",
                            (name,)).fetchone()
        if row is not None:
            return bool(row[0])
        import os
        return os.getenv(f"BRAIN_AGENT_{name.upper()}", "1") in ("1", "true")


# ======================================================================
# Konkrete Agenten — arbeiten ausschließlich auf Brain-Daten (Zero-Call-
# Site). Nur RecoveryAgent bekommt optional bot-DB-Zugriff für seine
# env-gated Aktion.
# ======================================================================

class HealthAgent(Agent):
    """Selbstüberwachung des Brains + Grundsystem. Erkennt: stehender
    Tick (Loop-Starvation/Deadlock-Indiz), nicht schreibbare brain.db,
    Regel-Fehlerhäufungen."""
    name = "health"
    interval_s = 120.0

    def __init__(self, brain):
        self._brain = brain
        self._last_tick_seen = time.time()

    def run(self, ctx: dict) -> list[dict]:
        out = []
        b = self._brain
        # Tick-Frische: ctx["ts"] stammt aus dem laufenden Tick — wenn
        # run() überhaupt läuft, lebt der Tick. Interessant ist die Lücke
        # SEIT dem letzten Lauf (Starvation durch blockierte Threads).
        gap = time.time() - self._last_tick_seen
        self._last_tick_seen = time.time()
        if gap > self.interval_s * 3:
            out.append({"level": "warn",
                        "text": f"Agent-Takt hing {gap:.0f}s — Thread-"
                                f"Starvation prüfen (Flask/DB-Lock?)"})
        try:
            with b._db_lock, b._conn() as c:
                c.execute("SELECT 1")
        except Exception as e:
            out.append({"level": "crit",
                        "text": f"brain.db nicht erreichbar: {e}"})
        for r in b.rules.rules_status():
            if r["errors"] >= 5 and r["enabled"]:
                out.append({"level": "warn",
                            "text": f"Regel {r['name']} hat {r['errors']} "
                                    f"Fehler — Bedingung/Aktion prüfen "
                                    f"({r['last_error']})",
                            "rule": r["name"]})
        return out


class RecoveryAgent(Agent):
    """Erkennt festgefahrene Zustände, die die bewährten Loops NICHT
    aufgelöst haben (Reaper sollte tote PIDs in ≤60s räumen — wenn ein
    recorder nach Minuten noch pid_dead ist, klemmt etwas).

    Aktion (nur mit BRAIN_ACT_RECOVERY=1): Stale-Recording-Flag in der
    bot-DB löschen — exakt die idempotente Reaper-Operation
    (recording=0, pid=NULL). Konfliktarm: wirkt nur auf Zeilen, deren
    PID nachweislich tot UND seit >stuck_s unverändert ist."""
    name = "recovery"
    interval_s = 180.0
    stuck_s = 600.0

    def __init__(self, brain, db_conn: Optional[Callable] = None,
                 act_check: Optional[Callable[[str], bool]] = None):
        self._brain = brain
        self._db_conn = db_conn
        self._act = act_check or (lambda n: False)

    def run(self, ctx: dict) -> list[dict]:
        out = []
        now = time.time()
        for e in self._brain.state.query("recorder", "pid_dead"):
            stuck = now - e["since"]
            if stuck < self.stuck_s:
                continue
            if self._act("recovery") and self._db_conn:
                try:
                    with self._db_conn() as conn:
                        conn.execute(
                            "UPDATE trackings SET recording=0, pid=NULL "
                            "WHERE username=? AND recording=1", (e["key"],))
                        conn.commit()
                    out.append({"level": "warn", "user": e["key"],
                                "action": "cleared_stale_recording",
                                "text": f"{e['key']}: recording-Flag nach "
                                        f"{stuck:.0f}s pid_dead gelöscht "
                                        f"(Reaper kam nicht)"})
                    continue
                except Exception as ex:
                    out.append({"level": "crit", "user": e["key"],
                                "text": f"Recovery-Aktion fehlgeschlagen: "
                                        f"{ex}"})
                    continue
            out.append({"level": "crit", "user": e["key"],
                        "text": f"{e['key']} seit {stuck:.0f}s pid_dead — "
                                f"Reaper klemmt? (Auto-Fix: "
                                f"BRAIN_ACT_RECOVERY=1)"})
        for e in self._brain.state.query("restream", "error"):
            if now - e["since"] > self.stuck_s:
                out.append({"level": "warn",
                            "text": f"Restream {e['attrs'].get('label') or e['key']} "
                                    f"seit {(now - e['since']) / 60:.0f}min "
                                    f"im Fehlerzustand"})
        out.extend(self._restart_dead_restreams(ctx, now))
        out.extend(self._pause_dead_sources(ctx, now))
        return out

    # ---- V37-W-PLUS: Stufe 2 — toten Restream selbst neu starten ----------
    # Gate: BRAIN_ACT_RESTREAM_RESTART=1 (Default 0 — erst dem Warum-Log
    # vertrauen, dann scharf schalten). Max. 2 Versuche pro rid und Stunde
    # (persistiert in brain.db), danach kritisches Finding statt Endlos-
    # Restart-Schleife. Der eigentliche Neustart läuft über den vom Bot
    # gereichten Hook (V37-P7c) threadsicher auf der Bot-Eventloop.
    # ---- V37-B91e: Stufe 3 — chronisch tote Quelle auto-pausieren ---------
    # Gate: BRAIN_ACT_PAUSE_DEAD_SOURCE=1 (Default 0). Eine Quelle, die beim
    # Preflight X-mal in Folge komplett tot war (Schwelle wie die Alarm-
    # Regel, aber +50% Sicherheitsabstand), wird über den Bot-Hook pausiert
    # statt nur gemeldet — spart dauerhaft Poll-Ressourcen für offline/
    # gelöschte Accounts. Nur EINMAL pro Quelle (persistiert), damit ein
    # manuelles Reaktivieren nicht sofort wieder pausiert wird.
    def _pause_dead_sources(self, ctx, now):
        findings = []
        if os.getenv("BRAIN_ACT_PAUSE_DEAD_SOURCE", "0") not in ("1", "true"):
            return findings
        pause = (ctx or {}).get("pause_source")
        streak_cb = (ctx or {}).get("dead_streak")
        if not (callable(pause) and callable(streak_cb)):
            return findings
        thresh = env_int("BRAIN_DEAD_STREAK_ALERT", 8)
        thresh = int(thresh * 1.5)      # Auto-Aktion konservativer als Alarm
        b = self._brain
        with b._db_lock, b._conn() as c:
            c.execute("CREATE TABLE IF NOT EXISTS paused_sources("
                      "who TEXT PRIMARY KEY, ts REAL)")
        try:
            streaks = streak_cb() or {}
        except Exception:
            return findings
        # V37-B91f: Auto-Reaktivierung — pausierte Quellen nach Karenzzeit
        # eine zweite Chance geben. Kommt der Account zurück, läuft er wieder;
        # bleibt er tot, greift Stufe 3 beim nächsten Preflight erneut.
        unpause = (ctx or {}).get("unpause_source")
        retry_h = env_float("BRAIN_DEAD_RETRY_HOURS", 12)
        if callable(unpause) and retry_h > 0:
            with b._db_lock, b._conn() as c:
                stale = c.execute(
                    "SELECT who FROM paused_sources WHERE ts < ?",
                    (now - retry_h * 3600,)).fetchall()
            for (w,) in stale:
                try:
                    if unpause(w):
                        findings.append({"level": "info",
                                         "text": f"{w} nach {retry_h:.0f}h "
                                                 f"reaktiviert (zweite Chance)"})
                        try:
                            b.memory.record_metric("sources_reactivated", 1, now)
                        except Exception:
                            pass
                except Exception:
                    pass
                with b._db_lock, b._conn() as c:
                    c.execute("DELETE FROM paused_sources WHERE who=?", (w,))

        for who, n in streaks.items():
            if n < thresh or ":" in str(who):   # Restream-Quellen überspringen
                continue
            with b._db_lock, b._conn() as c:
                seen = c.execute("SELECT 1 FROM paused_sources WHERE who=?",
                                 (who,)).fetchone()
            if seen:
                continue
            try:
                ok = bool(pause(who))
            except Exception as ex:
                findings.append({"level": "warn",
                                 "text": f"Pause-Hook für {who} warf: {ex}"})
                continue
            if ok:
                with b._db_lock, b._conn() as c:
                    c.execute("INSERT OR REPLACE INTO paused_sources(who,ts) "
                              "VALUES(?,?)", (who, now))
                findings.append({"level": "info",
                                 "text": f"{who} nach {n}× Preflight-tot "
                                         f"automatisch pausiert (Stufe 3)"})
                try:
                    b.memory.record_metric("sources_auto_paused", 1, now)
                except Exception:
                    pass
        return findings

    def _restart_dead_restreams(self, ctx, now):
        findings = []
        if os.getenv("BRAIN_ACT_RESTREAM_RESTART", "0") not in ("1", "true"):
            return findings
        cb = (ctx or {}).get("restream_restart")
        if not callable(cb):
            return findings
        after = env_float("BRAIN_RESTART_AFTER_S", 180)
        b = self._brain
        with b._db_lock, b._conn() as c:
            c.execute("CREATE TABLE IF NOT EXISTS restart_attempts("
                      "rid TEXT, ts REAL)")
        for e in b.state.query("restream"):
            if e["state"] not in ("pid_dead", "error"):
                continue
            if now - e.get("since", now) < after:
                continue      # Manager-eigene Retries zuerst machen lassen
            rid_key = str(e["key"])
            with b._db_lock, b._conn() as c:
                c.execute("DELETE FROM restart_attempts WHERE ts < ?",
                          (now - 3600,))
                n = c.execute("SELECT COUNT(*) FROM restart_attempts "
                              "WHERE rid=?", (rid_key,)).fetchone()[0]
                if n >= 2:
                    findings.append({"level": "crit",
                                     "text": f"{rid_key} nach 2 Neustart-"
                                             f"Versuchen weiter tot — "
                                             f"manueller Eingriff nötig"})
                    continue
                c.execute("INSERT INTO restart_attempts(rid, ts) VALUES(?,?)",
                          (rid_key, now))
            try:
                rid = int(rid_key.split(":", 1)[-1])
                ok = bool(cb(rid))
            except Exception as ex:
                ok = False
                findings.append({"level": "warn",
                                 "text": f"Restart-Hook für {rid_key} "
                                         f"warf: {ex}"})
            if ok:
                findings.append({"level": "info",
                                 "text": f"{rid_key} war {e['state']} "
                                         f"({int(now - e.get('since', now))}s)"
                                         f" — Neustart ausgelöst"})
        return findings


class ScoutAgent(Agent):
    """Vorausschau: kombiniert Scheduler-Prognose + Graph-Ranking zu
    einer Beobachtungsliste 'wen jetzt eng pollen'. Reines Vorschlags-
    organ — die Hints (M5) bleiben die maschinenlesbare Wahrheit."""
    name = "scout"
    interval_s = 600.0

    def __init__(self, brain):
        self._brain = brain

    def run(self, ctx: dict) -> list[dict]:
        b = self._brain
        up = b.scheduler.upcoming(b.memory, horizon_h=2, threshold=0.25)
        out = []
        for u in up[:5]:
            out.append({"level": "info", "user": u["user"],
                        "text": f"{u['user']} vermutlich in {u['in_hours']}h "
                                f"live (P={u['prob']}) — {u['basis']}"})
        return out


class AnalyticsAgent(Agent):
    """Tagesbild: verdichtet Sessions/Entscheidungen/Metriken der letzten
    24h zu einem Event — Grundlage für Dashboard-Digest und Telegram-
    Tageszusammenfassung."""
    name = "analytics"
    interval_s = 3600.0

    def __init__(self, brain):
        self._brain = brain

    def run(self, ctx: dict) -> list[dict]:
        b = self._brain
        day = time.time() - 86400
        with b._db_lock, b._conn() as c:
            sessions, rec = c.execute(
                "SELECT COUNT(*), COALESCE(SUM(recorded),0) FROM "
                "stream_sessions WHERE started>? AND abandoned=0",
                (day,)).fetchone()
            decisions = c.execute(
                "SELECT COUNT(*) FROM decisions WHERE ts>?",
                (day,)).fetchone()[0]
        return [{"level": "info", "sessions_24h": sessions,
                 "recorded_24h": rec, "decisions_24h": decisions,
                 "text": f"24h: {sessions} Sessions, {rec} aufgenommen, "
                         f"{decisions} Entscheidungen"}]


class LearningAgent(Agent):
    """'Aus Erfahrungen lernen' — messbar gemacht: schreibt stündlich die
    aktuellen Go-Live-Prognosen weg und vergleicht die Prognosen der
    VORSTUNDE mit dem, was wirklich passiert ist. Ergebnis: Brier-Score
    (0=perfekt, 0.25=Münzwurf-Niveau) als Metrik 'prediction_brier'.

    WARUM das zentral ist: Erst diese Rückkopplung sagt, ob die simple
    Histogramm-Prognose (M5) reicht oder ob mehr Modell nötig ist —
    Entscheidung per Daten statt per Bauchgefühl."""
    name = "learning"
    interval_s = 3600.0

    def __init__(self, brain):
        self._brain = brain

    def run(self, ctx: dict) -> list[dict]:
        b = self._brain
        now = time.time()
        prev_hour = time.gmtime(now - 3600).tm_hour
        # 1) Prognosen der Vorstunde bewerten
        preds = [e for e in b.memory.events(kind="prediction", limit=500)
                 if e["data"].get("hour_utc") == prev_hour
                 and now - e["ts"] < 7200]
        out = []
        if preds:
            errs = []
            for p in preds:
                user, prob = p["data"]["user"], float(p["data"]["prob"])
                with b._db_lock, b._conn() as c:
                    actual = c.execute(
                        "SELECT 1 FROM stream_sessions WHERE username=? "
                        "AND started>? AND abandoned=0 LIMIT 1",
                        (user, now - 2 * 3600)).fetchone()
                errs.append((prob - (1.0 if actual else 0.0)) ** 2)
            brier = sum(errs) / len(errs)
            b.memory.record_metric("prediction_brier", brier)
            out.append({"level": "info", "brier": round(brier, 4),
                        "n": len(errs),
                        "text": f"Prognosegüte Stunde {prev_hour} UTC: "
                                f"Brier {brier:.3f} über {len(errs)} User"})
        # 2) Prognosen für die aktuelle Stunde festschreiben
        cur_hour = time.gmtime(now).tm_hour
        for u in b.scheduler._users(b.memory, 30):
            p = b.scheduler.go_live_prob(b.memory, u, cur_hour)
            b.memory.record_event("prediction", u, user=u,
                                  hour_utc=cur_hour, prob=p["prob"])
        return out


# ======================================================================
# M8: AZRAEL-Sentinel-Flotte — Sicherheits- und Betriebs-Wächter.
# Reine Beobachter: sie greifen NICHT ein, sondern melden Befunde (die als
# agent_finding im Memory landen; crit zusaetzlich an notify). Externe Daten
# kommen ausschliesslich ueber injizierte Accessoren (wie RecoveryAgent seine
# bot-DB bekommt) — brain/ bleibt frei von Bot-Interna.
# ======================================================================

class SentinelAgent(Agent):
    """CrowdSec-Waechter. Liest per injiziertem Accessor einen Snapshot der
    aktiven Bans und meldet: (a) Angriffs-Spitzen — deutlicher Anstieg der
    Bans seit der letzten Runde; (b) CrowdSec selbst nicht erreichbar (Abwehr
    blind). Greift nicht in CrowdSec ein."""
    name = "sentinel"
    interval_s = 120.0
    surge_min = 8              # ab so vielen NEUEN Bans/Runde: Spitze

    def __init__(self, brain, crowdsec: Optional[Callable] = None):
        self._brain = brain
        self._cs = crowdsec
        self._last_total: Optional[int] = None
        self._down = False

    def run(self, ctx: dict) -> list[dict]:
        if not self._cs:
            return []
        try:
            snap = self._cs() or {}
        except Exception as e:
            return [{"level": "warn", "text": f"CrowdSec-Snapshot fehlgeschlagen: {e}"}]
        out: list[dict] = []
        if not snap.get("running", True):
            if not self._down:                    # nur beim Wechsel warnen
                self._down = True
                out.append({"level": "crit",
                            "text": "CrowdSec antwortet nicht — Abwehr blind. "
                                    + (snap.get("hint") or "cscli lapi status prüfen")})
            return out
        if self._down:
            self._down = False
            out.append({"level": "info", "text": "CrowdSec wieder erreichbar."})
        total = int(snap.get("bans", 0) or 0)
        top = snap.get("top_country") or ""
        if self._last_total is not None:
            delta = total - self._last_total
            if delta >= self.surge_min:
                lvl = "crit" if delta >= self.surge_min * 3 else "warn"
                out.append({"level": lvl, "bans_new": delta, "bans_total": total,
                            "top_country": top,
                            "text": f"CrowdSec: {delta} neue Bans seit letzter Runde "
                                    f"(gesamt {total})"
                                    f"{f', Top {top}' if top else ''} "
                                    f"— moegliche Angriffs-Spitze"})
        self._last_total = total
        return out


class DiskAgent(Agent):
    """Speicher-Reichweite. Misst freien Platz auf dem Aufnahme-Volume und
    schaetzt aus dem Verbrauch seit der letzten Runde die Reichweite (Stunden
    bis voll). Warnt frueh, damit ein 24/7-Recorder nie an die Wand faehrt."""
    name = "disk"
    interval_s = 300.0
    warn_free_gb = 15.0
    crit_free_gb = 5.0

    def __init__(self, brain, recordings_dir: str = "recordings"):
        self._brain = brain
        self._dir = recordings_dir
        self._last = None                          # (ts, free_bytes)

    def run(self, ctx: dict) -> list[dict]:
        import os
        import shutil
        path = self._dir if os.path.isdir(self._dir) else "."
        try:
            du = shutil.disk_usage(path)
        except Exception as e:
            return [{"level": "warn", "text": f"Disk-Messung fehlgeschlagen: {e}"}]
        free_gb = du.free / 1e9
        now = time.time()
        runway = None
        if self._last:
            dt = now - self._last[0]
            drained = self._last[1] - du.free      # Bytes seit letzter Runde
            if dt > 0 and drained > 0:
                runway = du.free / (drained / dt) / 3600.0   # Stunden bis voll
        self._last = (now, du.free)
        self._brain.memory.record_metric("disk_free_gb", round(free_gb, 2))
        tail = f", Reichweite ~{runway:.1f}h" if runway else ""
        if free_gb <= self.crit_free_gb:
            return [{"level": "crit", "free_gb": round(free_gb, 1),
                     "runway_h": round(runway, 1) if runway else None,
                     "text": f"Aufnahme-Speicher fast voll: {free_gb:.1f} GB frei{tail}"}]
        if free_gb <= self.warn_free_gb:
            return [{"level": "warn", "free_gb": round(free_gb, 1),
                     "runway_h": round(runway, 1) if runway else None,
                     "text": f"Aufnahme-Speicher wird knapp: {free_gb:.1f} GB frei{tail}"}]
        if runway and runway < 12:
            return [{"level": "warn", "runway_h": round(runway, 1),
                     "free_gb": round(free_gb, 1),
                     "text": f"Speicher-Reichweite nur ~{runway:.1f}h bei aktuellem "
                             f"Verbrauch ({free_gb:.0f} GB frei)"}]
        return []


class DatabaseAgent(Agent):
    """Datenbank-Waechter (v4.2-W146, der vierzehnte). Seit W143 kann die
    Datenbank MariaDB sein, seit W145 traegt sie die Einstellungen des Decks —
    ohne sie weiss der Bot weder, wen er verfolgt, noch wie er eingestellt
    ist. /healthz fragt `SELECT 1` und sagt ja oder nein; dieser Waechter
    misst, was VORHER schiefgeht: Latenz, Zuwachs, eine -wal-Datei ohne
    Checkpoint (SQLite), ein Schema neuer als der Code, Einstellungen, die
    beim Start nicht geladen wurden. Die Messung liefert nc/dbgesundheit.py
    ueber das injizierte `db_health` — kein Zugriff auf bot.py."""

    name = "datenbank"
    interval_s = 300.0
    warn_latenz_ms = 500.0       # SELECT 1 langsamer: jede Deck-Abfrage wartet mit
    crit_latenz_ms = 3000.0
    warn_wal_mb = 256.0          # -wal ohne Checkpoint waechst unbegrenzt
    crit_wal_mb = 1024.0
    warn_zuwachs_mb_h = 200.0    # so viel je Stunde ist kein Betrieb mehr, sondern ein Leck

    def __init__(self, brain, db_health: Optional[Callable] = None):
        self._brain = brain
        self._mess = db_health
        self._last = None            # (ts, groesse_b) der Vorrunde
        self._ohne_gesagt = False

    def run(self, ctx: dict) -> list[dict]:
        if not self._mess:
            # Einmal sagen, dass dieser Waechter nichts misst — sonst saehe ein
            # nicht verdrahteter Waechter im Deck aus wie eine gesunde Datenbank.
            if not self._ohne_gesagt:
                log.info("Datenbank-Waechter ohne Messung (db_health nicht uebergeben) — "
                         "er bleibt still.")
            self._ohne_gesagt = True
            return []
        try:
            m = self._mess() or {}
        except Exception as e:
            log.warning("Datenbank-Messung fehlgeschlagen: %s: %s", type(e).__name__, e)
            return [{"level": "warn", "text": f"Datenbank-Messung fehlgeschlagen: {type(e).__name__}: {e}"}]
        be = "MariaDB" if m.get("backend") == "mariadb" else "SQLite"
        if not m.get("ok"):
            return [{"level": "crit", "backend": m.get("backend"),
                     "text": f"{be} antwortet nicht: {m.get('fehler') or 'unbekannt'} — "
                             "Trackings, Aufnahmen und Einstellungen sind nicht lesbar."}]
        out = []
        lat = m.get("latenz_ms")
        groesse, wal = m.get("groesse_b"), m.get("wal_b")
        werte = {"db_latency_ms": lat}
        if groesse is not None:
            werte["db_size_mb"] = round(groesse / 1e6, 2)
        if wal is not None:
            werte["db_wal_mb"] = round(wal / 1e6, 2)
        # Ohne try: scheitert das Ablegen, meldet AgentManager.run_one das laut
        # als Waechter-Fehler (state "error") — besser als eine stille Luecke.
        for k, v in werte.items():
            if v is not None:
                self._brain.memory.record_metric(k, v)
        if lat is not None and lat >= self.warn_latenz_ms:
            out.append({"level": "crit" if lat >= self.crit_latenz_ms else "warn",
                        "latenz_ms": lat,
                        "text": f"{be} langsam: SELECT 1 braucht {lat:.0f} ms — gesperrt oder "
                                "ueberlastet; jede Abfrage des Decks wartet mit."})
        if wal is not None and wal / 1e6 >= self.warn_wal_mb:
            out.append({"level": "crit" if wal / 1e6 >= self.crit_wal_mb else "warn",
                        "wal_mb": round(wal / 1e6, 1),
                        "text": f"SQLite-Journal (-wal) {wal / 1e6:.0f} MB — der Checkpoint laeuft "
                                "nicht, ein Leser haelt eine Transaktion offen. Neustart raeumt es; "
                                "auf Dauer: bash tools/update.sh --mariadb."})
        now = time.time()
        if groesse is not None and self._last and now > self._last[0]:
            zuwachs = (groesse - self._last[1]) / 1e6 / ((now - self._last[0]) / 3600.0)
            if zuwachs >= self.warn_zuwachs_mb_h:
                out.append({"level": "warn", "zuwachs_mb_h": round(zuwachs, 1),
                            "text": f"Datenbank waechst um {zuwachs:.0f} MB je Stunde — "
                                    "welche Tabelle? Deck → System → Datenbank."})
        if groesse is not None:
            self._last = (now, groesse)
        st, erw = m.get("schema_stand"), m.get("schema_erwartet")
        if st is not None and erw is not None and st > erw:
            out.append({"level": "crit", "schema_stand": st, "schema_erwartet": erw,
                        "text": f"Schema-Stand {st} ist neuer als der Code ({erw}) — Rollback? "
                                "Zahlen koennen falsch sein."})
        if m.get("einst_fehler"):
            out.append({"level": "warn",
                        "text": "Einstellungen beim Start nicht aus der Datenbank geladen ("
                                f"{m['einst_fehler']}) — es gilt die .env, im Deck gesetzte "
                                "Werte wirken nicht."})
        return out


class SwapAgent(Agent):
    """v4.0-W86: hält den Swap sauber. Auf einem 24/7-Recorder wandern mit der
    Zeit inaktive Seiten in den Swap und bleiben dort liegen, auch wenn wieder
    RAM frei ist — das bremst spürbar. Dieser Wächter misst die Swap-Belegung
    und leert sie regelmäßig (swapoff -a && swapon -a, zieht die Seiten zurück
    ins RAM).

    SICHERHEIT (kritisch): swapoff -a zieht ALLE Swap-Seiten ins RAM. Passt das
    nicht ins freie RAM, kommt der OOM-Killer — im Zweifel stirbt der Bot. Darum
    wird NUR geleert, wenn MemAvailable groesser ist als die Swap-Belegung plus
    ein Sicherheitspuffer. Sonst: nur warnen, nichts anfassen.

    Braucht Rechte (swapoff/swapon = root). Standard-Kommando nutzt `sudo -n`
    (passwortloses sudo noetig); per SWAP_CLEAR_CMD frei setzbar. Fehlen die
    Rechte, wird das sauber gemeldet statt zu crashen."""
    name = "swap"

    def __init__(self, brain):
        self._brain = brain
        self.interval_s = float(env_int("SWAP_AGENT_INTERVAL_S", 900))   # 15 min
        self._min_mb = env_int("SWAP_CLEAR_MIN_MB", 64)       # darunter lohnt's nicht
        self._margin_mb = env_int("SWAP_CLEAR_MARGIN_MB", 512)  # RAM-Sicherheitspuffer
        self._cmd = os.getenv("SWAP_CLEAR_CMD",
                              "sudo -n swapoff -a && sudo -n swapon -a").strip()

    @staticmethod
    def _meminfo():
        """SwapTotal/SwapFree/MemAvailable in MB aus /proc/meminfo."""
        vals = {}
        try:
            with open("/proc/meminfo") as f:
                for ln in f:
                    k, _, rest = ln.partition(":")
                    if k in ("SwapTotal", "SwapFree", "MemAvailable"):
                        vals[k] = int(rest.strip().split()[0]) / 1024.0   # kB → MB
        except Exception:
            return None
        return vals

    def run(self, ctx: dict) -> list[dict]:
        import subprocess
        mi = self._meminfo()
        if not mi or mi.get("SwapTotal", 0) <= 0:
            return []                                   # kein Swap konfiguriert
        used = mi["SwapTotal"] - mi.get("SwapFree", mi["SwapTotal"])
        avail = mi.get("MemAvailable", 0)
        self._brain.memory.record_metric("swap_used_mb", round(used, 1))
        if used < self._min_mb:
            return []                                   # praktisch leer, nichts zu tun
        # OOM-Schutz: nur leeren, wenn die Seiten sicher ins RAM passen.
        if avail < used + self._margin_mb:
            return [{"level": "warn", "swap_used_mb": round(used),
                     "text": f"Swap bei {used:.0f} MB, aber nur {avail:.0f} MB RAM "
                             f"frei — Leeren uebersprungen (OOM-Schutz, Puffer "
                             f"{self._margin_mb} MB)"}]
        try:
            r = subprocess.run(self._cmd, shell=True, capture_output=True,
                               text=True, timeout=120)
        except Exception as e:
            return [{"level": "warn", "text": f"Swap-Leeren nicht ausgefuehrt: {e}"}]
        if r.returncode != 0:
            err = (r.stderr or r.stdout or "").strip()[:160]
            return [{"level": "warn", "swap_used_mb": round(used),
                     "text": f"Swap-Leeren fehlgeschlagen (Rechte? sudo NOPASSWD "
                             f"fuer swapoff/swapon noetig): {err}"}]
        mi2 = self._meminfo() or {}
        used2 = mi2.get("SwapTotal", 0) - mi2.get("SwapFree", 0)
        self._brain.memory.record_metric("swap_used_mb", round(used2, 1))
        return [{"level": "info", "swap_before_mb": round(used),
                 "swap_after_mb": round(used2),
                 "text": f"Swap geleert: {used:.0f} MB → {used2:.0f} MB "
                         f"(RAM frei war {avail:.0f} MB)"}]


class RestreamSentinelAgent(Agent):
    """Restream-Waechter. Erkennt Ziele, die STILL scheitern — der ffmpeg-
    Prozess lebt, aber ein tee-Slave (Kick/Twitch/YouTube) wird von der
    Plattform abgelehnt. RecoveryAgent sieht nur tote Prozesse, nicht tote
    Slaves; genau diese Luecke deckt dieser Agent. Meldet zusaetzlich doppelt
    belegte Ziele — ein Ingest-Key nimmt nur EINEN Publisher an, egal auf
    welcher Plattform. Injizierter Accessor liefert den Zustand."""
    name = "restream_sentinel"
    interval_s = 120.0
    stale_s = 180.0            # tee-Fehler juenger als das = frisch/relevant

    def __init__(self, brain, restream_health: Optional[Callable] = None):
        self._brain = brain
        self._rh = restream_health

    def run(self, ctx: dict) -> list[dict]:
        if not self._rh:
            return []
        try:
            h = self._rh() or {}
        except Exception as e:
            return [{"level": "warn", "text": f"Restream-Status fehlgeschlagen: {e}"}]
        out: list[dict] = []
        now = time.time()
        tee_fail = h.get("tee_fail") or {}
        fresh = [name for name, info in tee_fail.items()
                 if name != "unbekannt"
                 and now - (info.get("ts") or 0) < self.stale_s]
        if fresh:
            out.append({"level": "warn", "targets": fresh,
                        "text": f"Restream-Ziel(e) still abgelehnt: {', '.join(fresh)} "
                                f"— Prozess laeuft, Plattform verweigert "
                                f"(Key/Doppel-Live/IP?)"})
        out.extend(self._collisions(h))
        return out

    @staticmethod
    def _collisions(h: dict) -> list[dict]:
        """Ziel-Doppelbelegungen als Befund.

        Frueher hiess das pauschal "Kick-Key-Kollision" und verglich ein Feld,
        das seit der symmetrischen Zielaufloesung bei JEDEM Restream gleich
        ist (die erste konfigurierte Plattform). Wer eine Quelle auf drei
        Plattformen ausspielt, bekam die Meldung im Zwei-Minuten-Takt, ohne
        zu erfahren, WELCHE zwei Zeilen gemeint sind — und der Rat "eigene
        Keys je Channel" passte nicht mehr zur Konfiguration ueber die .env.
        Jetzt benennt der Befund Plattform, Restream-Nummern und Quellen und
        unterscheidet die zwei Faelle, die verschiedene Abhilfen haben."""
        out: list[dict] = []
        for col in (h.get("key_collisions") or []):
            # Rueckwaertskompatibel: aeltere Bruecken liefern nur [rid, rid].
            if not isinstance(col, dict):
                col = {"platform": "?", "rids": list(col), "sources": [],
                       "same_source": False}
            rids = col.get("rids") or []
            if len(rids) < 2:
                continue
            plat = col.get("platform") or "?"
            nummern = ", ".join("#" + str(x) for x in rids)
            quellen = [q for q in (col.get("sources") or []) if q]
            wer = (" (" + ", ".join("@" + q for q in dict.fromkeys(quellen)) + ")"
                   if quellen else "")
            if col.get("same_source"):
                text = (f"Restreams {nummern}{wer} senden dieselbe Quelle doppelt "
                        f"auf denselben {plat}-Key — ein Key nimmt nur EINEN "
                        f"Publisher an, der zweite scheitert. Es ist eine Zeile "
                        f"zu viel: eine davon abschalten.")
            else:
                text = (f"Restreams {nummern}{wer} senden auf denselben "
                        f"{plat}-Key — nur einer kommt an. Entweder RESTREAM_SINGLE=1 "
                        f"(ein Kanal, ein Stream) oder je Restream eigene "
                        f"Ingest/Key-Werte hinterlegen.")
            out.append({"level": "warn", "collision": rids, "platform": plat,
                        "sources": quellen, "text": text})
        return out


class ToxicityAgent(Agent):
    """Chat-Toxizitaets-Trend. Liest per injiziertem Accessor eine Verdichtung
    des Moderations-Logs (Aktionen letzte Stunde vs. Vorstunde + mittlerer
    toxic-Score) und meldet, wenn die Toxizitaet auffaellig STEIGT — nicht die
    Einzelaktion (die macht die Moderation schon), sondern die Welle.

    Welche Plattformen einfliessen, entscheidet der Lieferant des
    Schnappschusses (nc/modstats.py), nicht dieser Agent: TikTok gehoert nicht
    dazu, dort hat der Bot keine Moderationsbefugnis. Steht in der
    Verdichtung ein `platforms`-Zaehler, nennt die Meldung ihn mit — sonst
    weiss der Betreiber zwar, DASS es kracht, aber nicht WO."""
    name = "toxicity"
    interval_s = 600.0
    spike_factor = 2.0         # Aktionen ≥ 2× Vorstunde = Welle
    spike_min = 6              # und mind. so viele absolut
    hot_toxic = 0.75           # mittlerer toxic-Score, ab dem es "heiss" ist

    def __init__(self, brain, moderation: Optional[Callable] = None):
        self._brain = brain
        self._mod = moderation

    def run(self, ctx: dict) -> list[dict]:
        if not self._mod:
            return []
        try:
            s = self._mod() or {}
        except Exception as e:
            return [{"level": "warn", "text": f"Moderations-Snapshot fehlgeschlagen: {e}"}]
        now_n = int(s.get("actions_1h", 0) or 0)
        prev_n = int(s.get("actions_prev_1h", 0) or 0)
        avg = s.get("avg_toxic_1h")
        self._brain.memory.record_metric("moderation_actions_1h", now_n)
        out: list[dict] = []
        je = s.get("platforms") or {}
        wo = ""
        if je:
            wo = " [" + ", ".join(f"{k} {v}" for k, v in
                                  sorted(je.items(), key=lambda x: -x[1])) + "]"
        rising = now_n >= self.spike_min and now_n >= self.spike_factor * max(prev_n, 1)
        if rising:
            lvl = "crit" if now_n >= self.spike_min * 3 else "warn"
            tail = f", Ø-Toxizität {avg}" if avg is not None else ""
            out.append({"level": lvl, "actions_1h": now_n, "actions_prev_1h": prev_n,
                        "avg_toxic": avg, "platforms": je,
                        "text": f"Chat-Toxizität steigt: {now_n} Moderations-Aktionen "
                                f"letzte Stunde (Vorstunde {prev_n}){tail}{wo} "
                                f"— moegliche Welle/Raid"})
        elif avg is not None and avg >= self.hot_toxic and now_n >= self.spike_min:
            out.append({"level": "warn", "avg_toxic": avg, "actions_1h": now_n,
                        "platforms": je,
                        "text": f"Chat laeuft heiss: Ø-Toxizität {avg} ueber "
                                f"{now_n} Aktionen/Stunde{wo}"})
        return out


class UptimeAgent(Agent):
    """Chat-Verbindungs-Waechter. Prueft je Plattform (Kick/Twitch/YouTube), ob
    der eigene Chat-Listener verbunden ist, und meldet Trennungen sowie
    Reconnect-Flattern (viele Reconnects in kurzer Zeit = instabile Leitung).
    Plattformen, die bewusst AUS sind, werden ignoriert."""
    name = "uptime"
    interval_s = 180.0
    churn_min = 3              # Reconnects/Runde, ab denen es 'flattert'

    def __init__(self, brain, wchat_status: Optional[Callable] = None):
        self._brain = brain
        self._ws = wchat_status
        self._last_rc: dict = {}

    def run(self, ctx: dict) -> list[dict]:
        if not self._ws:
            return []
        try:
            st = self._ws() or {}
        except Exception as e:
            return [{"level": "warn", "text": f"Uptime-Status fehlgeschlagen: {e}"}]
        out: list[dict] = []
        for plat in ("kick", "twitch", "youtube"):
            p = st.get(plat) or {}
            if not p:
                continue
            mode = str(p.get("mode", "") or "").lower()
            if mode in ("aus", "off", "disabled", "-"):
                continue                            # bewusst aus → nicht melden
            reconnects = int(p.get("reconnects", 0) or 0)
            churn = reconnects - self._last_rc.get(plat, reconnects)
            self._last_rc[plat] = reconnects
            if not p.get("connected"):
                out.append({"level": "warn", "platform": plat,
                            "text": f"{plat.capitalize()}-Chat getrennt "
                                    f"(Modus {mode or '?'}, {reconnects} Reconnects gesamt)"})
            elif churn >= self.churn_min:
                out.append({"level": "warn", "platform": plat, "churn": churn,
                            "text": f"{plat.capitalize()}-Chat flattert: {churn} "
                                    f"Reconnects seit letzter Runde"})
        return out


class RecordingAgent(Agent):
    """Aufnahme-Waechter. Erkennt Streamer, die als recording=1 markiert sind,
    deren Ausgabedatei aber ueber mehrere Runden NICHT waechst — dann laeuft
    die Aufnahme stumm/eingefroren (Prozess da, 0 Bytes/keine Zunahme). Der
    Reaper raeumt tote PIDs; genau die Luecke 'lebende PID, tote Datei' deckt
    er nicht. Injizierter Accessor liefert je aktivem Mitschnitt Groesse+alive."""
    name = "recording"
    interval_s = 120.0
    stall_rounds = 2           # so viele Runden ohne Wachstum = Stall

    def __init__(self, brain, recording_health: Optional[Callable] = None):
        self._brain = brain
        self._rh = recording_health
        self._last: dict = {}      # user -> (bytes, stall_count)

    def run(self, ctx: dict) -> list[dict]:
        if not self._rh:
            return []
        try:
            snap = self._rh() or {}
        except Exception as e:
            return [{"level": "warn", "text": f"Aufnahme-Status fehlgeschlagen: {e}"}]
        out: list[dict] = []
        seen = set()
        for user, info in snap.items():
            seen.add(user)
            b = info.get("bytes")
            alive = info.get("alive", True)
            prev = self._last.get(user)
            if b is None:
                if alive:
                    out.append({"level": "warn", "user": user,
                                "text": f"Aufnahme @{user}: recording=1, aber keine "
                                        f"Ausgabedatei gefunden"})
                self._last[user] = (0, 0)
                continue
            stall = prev[1] + 1 if (prev is not None and b <= prev[0]) else 0
            self._last[user] = (b, stall)
            if stall >= self.stall_rounds and alive:
                mb = b / 1e6
                out.append({"level": "warn", "user": user, "mb": round(mb, 1),
                            "stall_rounds": stall,
                            "text": f"Aufnahme @{user} eingefroren: {mb:.1f} MB, kein "
                                    f"Wachstum seit {stall} Runden (Prozess laeuft) "
                                    f"— stummer/kaputter Mitschnitt?"})
        for u in list(self._last):        # aufgeraeumte User vergessen
            if u not in seen:
                del self._last[u]
        return out


class ProxyHealthAgent(Agent):
    """Proxy-/Fetch-Waechter. Der einzige Weg zu TikTok fuehrt ueber einen
    Proxy (fester RECORD_PROXY oder rotierender Pool) — faellt der aus, gehen
    ALLE Live-Erkennungen blind, ohne dass ein anderer Waechter das abdeckt.
    Dieser misst die HTTP-Status-Verteilung der Webcast-Fetches (mode-agnostisch:
    was TikTok zurueckgibt, egal welcher Proxy) und schlaegt an, wenn die
    Erfolgsrate (HTTP 200) einbricht oder 403-Blocks die Runde dominieren.
    Delta gegen die Vorrunde — nur der JUENGSTE Zustand zaehlt."""

    name = "proxy"
    interval_s = 300.0
    min_samples = 15           # unter so wenig Fetches keine Aussage (still)
    warn_success = 0.60        # <60% HTTP-200 in der Runde = warn
    crit_success = 0.25        # <25% = crit
    warn_block = 0.25          # >25% HTTP-403 (Server-IP/Proxy-Block) = warn
    crit_block = 0.50          # >50% = crit

    def __init__(self, brain, tiktok_status: Optional[Callable] = None):
        self._brain = brain
        self._ts = tiktok_status
        self._last = None            # dict {code: cum_count} der Vorrunde

    def run(self, ctx: dict) -> list[dict]:
        if not self._ts:
            return []
        try:
            snap = self._ts() or {}
        except Exception as e:
            return [{"level": "warn", "text": f"Proxy-/Fetch-Status fehlgeschlagen: {e}"}]
        by_code = snap.get("by_code") or {}
        prev = self._last
        self._last = dict(by_code)
        if prev is None:
            return []                # erste Runde: nur Basis setzen
        total = ok = blocked = 0
        for code, cnt in by_code.items():
            d = cnt - prev.get(code, 0)
            if d <= 0:
                continue
            total += d
            if code == 200:
                ok += d
            elif code == 403:
                blocked += d
        if total < self.min_samples:
            return []                # zu wenig Verkehr fuer eine Aussage
        success = ok / total
        block_rate = blocked / total
        try:
            self._brain.memory.record_metric(
                "tiktok_fetch_success_pct", round(success * 100, 1))
        except Exception:
            pass
        mode = "fester Proxy" if snap.get("record_proxy") else f"Pool ({snap.get('pool_size', 0)})"
        base = (f"TikTok-Fetch-Erfolg {success * 100:.0f}% ueber {total} Fetches "
                f"({mode}), 403-Block {block_rate * 100:.0f}%")
        if success <= self.crit_success or block_rate >= self.crit_block:
            return [{"level": "crit", "success_pct": round(success * 100, 1),
                     "block_pct": round(block_rate * 100, 1), "samples": total,
                     "text": base + " — Proxy/Fetch-Pfad ueberwiegend tot. "
                                    "RECORD_PROXY/Pool + Polen-Tunnel pruefen."}]
        if success <= self.warn_success or block_rate >= self.warn_block:
            return [{"level": "warn", "success_pct": round(success * 100, 1),
                     "block_pct": round(block_rate * 100, 1), "samples": total,
                     "text": base + " — Fetch-Erfolg gesunken, Proxy koennte degradieren."}]
        return []


class _BeobachtungsAgent(Agent):
    """Gemeinsamer Teil der beiden Beobachtungs-Waechter (v4.2-W148).

    Die Messung (`lage`) und die Steuerung (`steuern`) kommen injiziert aus
    nc/beobachtungsdienst.py — hier steht nur die Bewertung und, hinter dem
    Aktions-Gate, die Selbstheilung: liegt der Dienst zweimal in Folge
    nicht erreichbar, wird er neu gestartet, hoechstens einmal je
    `heil_ruhe_s`. Zwei Runden statt einer: ein Neustart von Hand oder
    durch observability.sh dauert ein paar Sekunden, und genau da soll der
    Waechter nicht zusaetzlich zugreifen."""

    dienst = "?"
    titel = "?"
    heil_ruhe_s = 1800.0

    def __init__(self, brain, lage: Optional[Callable] = None,
                 steuern: Optional[Callable] = None,
                 act_check: Optional[Callable] = None):
        self._brain = brain
        self._lage = lage
        self._steuern = steuern
        self._act = act_check or (lambda n: False)
        self._aus_in_folge = 0
        self._letzte_heilung = 0.0
        self.letzte_lage: dict = {}

    def _ohne_messung(self) -> list[dict]:
        # Einmal sagen, dass dieser Waechter nichts misst — wie beim
        # Datenbank-Waechter: sonst saehe er im Deck aus wie ein gesunder Dienst.
        if not getattr(self, "_ohne_gesagt", False):
            log.info("%s-Waechter ohne Messung (lage nicht uebergeben) — er bleibt still.", self.titel)
            self._ohne_gesagt = True
        return []

    def _messen(self):
        try:
            m = self._lage() or {}
        except Exception as e:
            log.warning("%s-Messung fehlgeschlagen: %s: %s", self.titel, type(e).__name__, e)
            return None, [{"level": "warn",
                           "text": f"{self.titel}-Messung fehlgeschlagen: {type(e).__name__}: {e}"}]
        self.letzte_lage = m
        return m, []

    def _heilen(self, aktion: str) -> list[dict]:
        """Hinter dem Gate BRAIN_ACT_<DIENST>; Ergebnis als Befund, damit es
        im Entscheidungslog steht — auch wenn es scheitert."""
        self._aus_in_folge += 1
        jetzt = time.time()
        # Kein Fehlerpfad, sondern drei Gruende, NICHT einzugreifen: erste
        # Runde, kein Gate/keine Steuerung, Ruhezeit. Der Ausfall selbst steht
        # schon als crit-Befund in run().
        darf = (self._aus_in_folge >= 2 and self._steuern is not None and self._act(self.dienst)
                and jetzt - self._letzte_heilung >= self.heil_ruhe_s)
        befund = []
        if darf:
            self._letzte_heilung = jetzt
            r = self._steuern(self.dienst, aktion) or {}
            if r.get("ok"):
                befund.append({"level": "warn", "aktion": aktion,
                               "text": f"{self.titel} war nicht erreichbar — neu gestartet ({r.get('befehl')})."})
            else:
                befund.append({"level": "crit", "aktion": aktion,
                               "text": f"{self.titel}: Neustart gescheitert — {r.get('text') or 'unbekannt'}"})
        return befund


class PrometheusAgent(_BeobachtungsAgent):
    """Prometheus-Waechter (v4.2-W148, der fuenfzehnte). Registriert nur,
    wenn PROMETHEUS_URL gesetzt ist. Faellt Prometheus aus, kommt kein
    einziger seiner Alarme mehr — der Ausfall, der sich selbst verschweigt.
    Daneben: erreicht er den Bot (up), scheitern Abrufziele oder Regeln,
    hat der letzte Reload die Konfiguration angenommen, und welche Alarme
    feuern gerade."""

    name = "prometheus"
    dienst = "prometheus"
    titel = "Prometheus"
    interval_s = 120.0

    def run(self, ctx: dict) -> list[dict]:
        if not self._lage:
            return self._ohne_messung()
        m, out = self._messen()
        if m is None:
            return out
        if not m.get("erreichbar"):
            return [{"level": "crit",
                     "text": f"Prometheus antwortet nicht ({m.get('fehler') or 'unbekannt'}) — "
                             "kein Alarm kommt mehr durch. journalctl -u nightcrawler-prometheus -n 40"}
                    ] + self._heilen("neu_starten")
        self._aus_in_folge = 0
        if m.get("serien") is not None:
            self._brain.memory.record_metric("prometheus_series", m["serien"])
        if m.get("liest_bot") is False:
            out.append({"level": "crit",
                        "text": "Prometheus erreicht den Bot nicht (up=0) — stimmt DASHBOARD_PORT, "
                                "laeuft das Deck? bash tools/observability.sh --check"})
        if m.get("config_ok") is False:
            out.append({"level": "crit",
                        "text": "Prometheus hat die letzte Konfiguration abgelehnt und laeuft mit "
                                "der alten weiter — promtool check config /etc/nightcrawler/observability/prometheus.yml"})
        for z in m.get("ziele_aus") or []:
            out.append({"level": "warn",
                        "text": f"Abrufziel {z.get('job')} nicht erreichbar: {z.get('fehler') or '—'}"})
        for r in m.get("regeln_aus") or []:
            out.append({"level": "warn",
                        "text": f"Alarmregel {r.get('regel')} scheitert: {r.get('fehler') or '—'}"})
        for a in m.get("alarme") or []:
            out.append({"level": "crit" if a.get("schwere") == "critical" else "warn",
                        "alarm": a.get("name"),
                        "text": f"Alarm {a.get('name')}: {a.get('text') or 'feuert'}"})
        return out


class GrafanaAgent(_BeobachtungsAgent):
    """Grafana-Waechter (v4.2-W148, der sechzehnte). Registriert nur, wenn
    GRAFANA_URL gesetzt ist. Prueft, was zwischen „der Dienst laeuft" und
    „man sieht etwas" liegt: Datenbank, das Passwort aus der .env, die
    Datenquelle zu Prometheus und das NIGHTCRAWLER-Dashboard."""

    name = "grafana"
    dienst = "grafana"
    titel = "Grafana"
    interval_s = 300.0

    def run(self, ctx: dict) -> list[dict]:
        if not self._lage:
            return self._ohne_messung()
        m, out = self._messen()
        if m is None:
            return out
        if not m.get("erreichbar"):
            return [{"level": "crit",
                     "text": f"Grafana antwortet nicht ({m.get('fehler') or 'unbekannt'}) — "
                             "journalctl -u grafana-server -n 40"}] + self._heilen("neu_starten")
        self._aus_in_folge = 0
        if m.get("db_ok") is False:
            out.append({"level": "crit", "text": "Grafana meldet seine Datenbank als defekt (/api/health)."})
        if m.get("anmeldung_ok") is False:
            out.append({"level": "warn",
                        "text": "Grafana lehnt GRAFANA_ADMIN_PASSWORD aus der .env ab — "
                                "sudo bash tools/observability.sh setzt es neu."})
        if m.get("quelle_ok") is False:
            out.append({"level": "warn",
                        "text": "Grafana erreicht seine Datenquelle Prometheus nicht — die Diagramme bleiben leer."})
        if m.get("dashboard_da") is False:
            out.append({"level": "warn",
                        "text": "Das NIGHTCRAWLER-Dashboard fehlt in Grafana — sudo bash tools/observability.sh legt es an."})
        return out
