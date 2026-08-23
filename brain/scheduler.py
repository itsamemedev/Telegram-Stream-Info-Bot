# brain/scheduler.py — M5: Autonomer Scheduler + Prognosen
#
# AUFGABE: Aus Gelerntem (M3-Sessions, M3-Metriken, M4-Fakten) autonome
# Planungsentscheidungen ableiten: Wann prüfen? Wen priorisieren? Wann
# wird die CPU eng? — jede Entscheidung mit Begründung.
#
# ABGRENZUNG zu bot_v36._schedule_next_check: Das bestehende adaptive
# Polling bleibt unangetastet (Rückwärtskompatibilität). Der Scheduler
# schreibt EMPFEHLUNGEN in eine eigene Tabelle (sched_hints). bot_v36
# KANN sie konsumieren (1-Zeilen-Hook, optional), muss aber nicht —
# gleiche Beobachten-vor-Handeln-Philosophie wie die M2-Regeln.
#
# WARUM simple Statistik statt ML-Modell: 8 CPU-Cores, 24/7-Betrieb.
# Ein Stunden-Histogramm über 30 Tage schlägt für "geht Streamer X um
# 20 Uhr live?" jedes Modell, das man erst trainieren müsste — und es
# ist zu 100% erklärbar. ML lohnt erst, wenn diese Baseline nachweislich
# zu schlecht ist (Entscheidungslog liefert dafür die Daten).

from __future__ import annotations

import logging
import threading
import time
from typing import Callable, Optional

log = logging.getLogger("brain.scheduler")

_SCHEMA = """
CREATE TABLE IF NOT EXISTS sched_hints(
    username TEXT PRIMARY KEY,
    interval_s INTEGER,
    priority REAL,
    prob_now REAL,
    reason TEXT,
    ts REAL);
"""

# Poll-Intervall-Spanne für Empfehlungen. Defaults spiegeln die Praxis
# des bestehenden adaptiven Pollings: heiß = 60s, kalt = 15min.
MIN_INTERVAL_S = 60
MAX_INTERVAL_S = 900

# Glättungskern über Nachbarstunden: eine 20:00-Session macht auch
# 19:00/21:00 etwas wahrscheinlicher (Streamer sind nicht atomuhrgenau).
_KERNEL = (0.25, 0.5, 0.25)


class Scheduler:
    def __init__(self, conn_factory: Callable, db_lock: threading.Lock):
        self._conn = conn_factory
        self._lock = db_lock
        with self._lock, self._conn() as c:
            c.executescript(_SCHEMA)

    # -------------------------------------------------- Go-Live-Prognose

    def go_live_prob(self, memory, user: str, hour_utc: int,
                     days: int = 30) -> dict:
        """P(Streamer geht in Stunde h live) = Anteil beobachteter Tage
        mit Session-Start in h, kernel-geglättet über Nachbarstunden.

        WARUM 'Tage mit Session' statt Session-Zählung: 5 Flap-Sessions
        an EINEM Abend dürfen nicht wie 5 verlässliche Abende zählen."""
        since = time.time() - days * 86400
        with memory._lock, memory._conn() as c:
            rows = c.execute(
                "SELECT started FROM stream_sessions WHERE username=? "
                "AND started>? AND abandoned=0", (user, since)).fetchall()
        if not rows:
            return {"user": user, "hour_utc": hour_utc, "prob": 0.0,
                    "basis": "keine Sessions"}
        day_hours: dict[int, set[int]] = {}
        first = min(r[0] for r in rows)
        for (ts,) in rows:
            t = time.gmtime(ts)
            day_hours.setdefault(t.tm_hour, set()).add(t.tm_yday)
        observed_days = max((time.time() - first) / 86400, 1.0)
        raw = [len(day_hours.get(h, ())) / observed_days for h in range(24)]
        prob = sum(_KERNEL[i] * raw[(hour_utc - 1 + i) % 24]
                   for i in range(3))
        prob = min(prob, 1.0)
        return {"user": user, "hour_utc": hour_utc,
                "prob": round(prob, 3),
                "basis": (f"{len(rows)} Sessions / {observed_days:.0f} "
                          f"beobachtete Tage, Stunde {hour_utc}±1 UTC")}

    def upcoming(self, memory, horizon_h: int = 6, threshold: float = 0.15,
                 days: int = 30) -> list[dict]:
        """Wer geht in den nächsten N Stunden wahrscheinlich live?
        Sortiert nach (Stunde, Wahrscheinlichkeit) — der Sende-Timeline-
        Blick fürs Dashboard."""
        users = self._users(memory, days)
        now_h = time.gmtime().tm_hour
        out = []
        for u in users:
            for dh in range(horizon_h):
                h = (now_h + dh) % 24
                p = self.go_live_prob(memory, u, h, days)
                if p["prob"] >= threshold:
                    out.append({"user": u, "in_hours": dh, "hour_utc": h,
                                "prob": p["prob"], "basis": p["basis"]})
                    break        # erste relevante Stunde reicht pro User
        return sorted(out, key=lambda x: (x["in_hours"], -x["prob"]))

    # ---------------------------------------------------- CPU-Forecast

    def cpu_forecast(self, memory, horizon_h: int = 6,
                     days: int = 7) -> list[dict]:
        """Saisonale Stunden-Prognose: Ø load_ratio15 je Tagesstunde über
        die letzten `days` Tage. warn=True, wo Prognose ≥ 0.85 — dort
        keine zusätzlichen Transcode-Restreams einplanen."""
        since = time.time() - days * 86400
        with memory._lock, memory._conn() as c:
            rows = c.execute(
                "SELECT CAST(strftime('%H', ts, 'unixepoch') AS INT) AS h, "
                "AVG(value), MAX(value), COUNT(*) FROM metrics "
                "WHERE name='load_ratio15' AND ts>? GROUP BY h",
                (since,)).fetchall()
        seasonal = {r[0]: {"avg": r[1], "max": r[2], "n": r[3]}
                    for r in rows}
        now_h = time.gmtime().tm_hour
        out = []
        for dh in range(horizon_h):
            h = (now_h + dh) % 24
            s = seasonal.get(h)
            if s:
                out.append({"in_hours": dh, "hour_utc": h,
                            "load_ratio_avg": round(s["avg"], 3),
                            "load_ratio_max": round(s["max"], 3),
                            "samples": s["n"],
                            "warn": s["avg"] >= 0.85,
                            "basis": f"Ø aus {s['n']} Messungen, {days}d"})
            else:
                out.append({"in_hours": dh, "hour_utc": h,
                            "load_ratio_avg": None, "warn": False,
                            "basis": "keine Metrik-Historie"})
        return out

    # ----------------------------------------------- Prioritätsplanung

    def plan(self, memory, days: int = 30) -> list[dict]:
        """Für jeden bekannten Streamer ein Poll-Intervall empfehlen und
        als Hint persistieren. Linear zwischen MIN (P≥0.5) und MAX (P=0).

        Das IST die autonome Entscheidung — geloggt, begründet, abrufbar.
        Ob bot_v36 sie befolgt, entscheidet der optionale Hook (unten
        dokumentiert), nicht der Scheduler."""
        now_h = time.gmtime().tm_hour
        hints = []
        for u in self._users(memory, days):
            p = self.go_live_prob(memory, u, now_h, days)
            prob = p["prob"]
            frac = min(prob / 0.5, 1.0)
            interval = int(MAX_INTERVAL_S - frac
                           * (MAX_INTERVAL_S - MIN_INTERVAL_S))
            reason = (f"P(live, Stunde {now_h} UTC)={prob} → "
                      f"{'heiß' if frac >= 1 else 'warm' if prob > 0.15 else 'kalt'}; "
                      f"{p['basis']}")
            hints.append({"username": u, "interval_s": interval,
                          "priority": round(prob, 3), "prob_now": prob,
                          "reason": reason})
        with self._lock, self._conn() as c:
            c.execute("DELETE FROM sched_hints")
            c.executemany(
                "INSERT INTO sched_hints VALUES(?,?,?,?,?,?)",
                [(h["username"], h["interval_s"], h["priority"],
                  h["prob_now"], h["reason"], time.time()) for h in hints])
        return sorted(hints, key=lambda x: -x["priority"])

    def hints(self, user: Optional[str] = None) -> list[dict]:
        q = "SELECT username, interval_s, priority, prob_now, reason, ts " \
            "FROM sched_hints "
        args: tuple = ()
        if user:
            q += "WHERE username=? "
            args = (user,)
        q += "ORDER BY priority DESC"
        with self._lock, self._conn() as c:
            rows = c.execute(q, args).fetchall()
        return [{"username": r[0], "interval_s": r[1], "priority": r[2],
                 "prob_now": r[3], "reason": r[4], "ts": r[5]}
                for r in rows]

    # -------------------------------------------------------- intern

    @staticmethod
    def _users(memory, days: int) -> list[str]:
        since = time.time() - days * 86400
        with memory._lock, memory._conn() as c:
            return [r[0] for r in c.execute(
                "SELECT DISTINCT username FROM stream_sessions "
                "WHERE started>? AND abandoned=0", (since,)).fetchall()]
