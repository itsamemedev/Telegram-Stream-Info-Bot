# brain/memory.py — M3: Langzeitgedächtnis
#
# WARUM abgeleitet statt gemeldet: Sessions entstehen automatisch aus
# State-Transitions (stream online→offline), die M1 ohnehin persistiert.
# Kein einziger neuer Meldepunkt in bot_v36 nötig — Zero-Call-Site wie M2.
#
# WAS gespeichert wird (v37-Anforderung "nicht nur Chatverlauf"):
#   events          generische Ereignisse (Fehler, Uploads, Marker)
#   stream_sessions Live-Sessions mit Dauer + recorded-Flag
#   metrics         Zeitreihen (CPU, RAM, Disk, Parallelität)
#   decisions       hat M1 bereits (Entscheidungen + Begründung)
#
# WARUM eigene Tabellen in brain.db statt bot-DB: gleiche Isolation wie
# M1 — brain.db kaputt ⇒ Bot läuft unverändert. Die bot-DB kennt zudem
# den MariaDB-Translation-Layer; brain.db ist bewusst SQLite-only (WAL),
# weil sie nur lokale Betriebsdaten hält, keine Nutzdaten.

from __future__ import annotations

import json
import logging
import threading
import time
from typing import Callable, Optional

log = logging.getLogger("brain.memory")

_SCHEMA = """
CREATE TABLE IF NOT EXISTS events(
    ts REAL, kind TEXT, key TEXT, data TEXT);
CREATE INDEX IF NOT EXISTS idx_ev_ts ON events(ts);
CREATE INDEX IF NOT EXISTS idx_ev_kind ON events(kind, ts);
CREATE TABLE IF NOT EXISTS stream_sessions(
    id INTEGER PRIMARY KEY,
    username TEXT, started REAL, ended REAL,
    duration_s REAL, recorded INTEGER DEFAULT 0,
    abandoned INTEGER DEFAULT 0);
CREATE INDEX IF NOT EXISTS idx_sess_user ON stream_sessions(username, started);
CREATE TABLE IF NOT EXISTS metrics(
    ts REAL, name TEXT, value REAL);
CREATE INDEX IF NOT EXISTS idx_met ON metrics(name, ts);
"""


class Memory:
    """Persistentes Gedächtnis. Bekommt Connection-Factory + Lock vom
    Brain — EIN Schreibpfad auf brain.db, keine zweite Lock-Hierarchie."""

    def __init__(self, conn_factory: Callable, db_lock: threading.Lock):
        self._conn = conn_factory
        self._lock = db_lock
        self._init_schema()
        self._recover_open_sessions()

    # ------------------------------------------------------ Schreiben

    def record_event(self, kind: str, key: str = "", **data) -> None:
        try:
            with self._lock, self._conn() as c:
                c.execute("INSERT INTO events VALUES(?,?,?,?)",
                          (time.time(), kind, key,
                           json.dumps(data, default=str)))
        except Exception:
            log.debug("event-Persistenz fehlgeschlagen", exc_info=True)

    def record_metric(self, name: str, value: float,
                      ts: Optional[float] = None) -> None:
        try:
            with self._lock, self._conn() as c:
                c.execute("INSERT INTO metrics VALUES(?,?,?)",
                          (ts or time.time(), name, float(value)))
        except Exception:
            log.debug("metric-Persistenz fehlgeschlagen", exc_info=True)

    def record_metrics(self, values: dict, ts: Optional[float] = None) -> None:
        ts = ts or time.time()
        rows = [(ts, k, float(v)) for k, v in values.items()
                if isinstance(v, (int, float))]
        if not rows:
            return
        try:
            with self._lock, self._conn() as c:
                c.executemany("INSERT INTO metrics VALUES(?,?,?)", rows)
        except Exception:
            log.debug("metrics-Persistenz fehlgeschlagen", exc_info=True)

    # --------------------------------------- Session-Ableitung (Hook)

    def observe_transition(self, ev: dict) -> None:
        """Wird vom Brain als State-Listener registriert. Leitet Sessions
        aus stream-Transitions ab. Fehler hier dürfen NIE nach oben —
        der Listener-Pfad läuft im Kontext der meldenden Komponente."""
        try:
            if ev["kind"] != "stream":
                return
            user, new, old = ev["key"], ev["new"], ev["old"]
            if new == "online" and old != "online":
                self._open_session(user, ev["ts"])
            elif old == "online" and new in ("offline", "gone"):
                self._close_session(user, ev["ts"])
        except Exception:
            log.debug("observe_transition-Fehler", exc_info=True)

    def _open_session(self, user: str, ts: float) -> None:
        with self._lock, self._conn() as c:
            # Doppel-online (Detection-Flap): alte offene Session erst als
            # abandoned schließen, sonst zählt eine Session doppelt.
            c.execute(
                "UPDATE stream_sessions SET ended=?, duration_s=?-started, "
                "abandoned=1 WHERE username=? AND ended IS NULL",
                (ts, ts, user))
            c.execute(
                "INSERT INTO stream_sessions(username, started) VALUES(?,?)",
                (user, ts))

    def _close_session(self, user: str, ts: float) -> None:
        with self._lock, self._conn() as c:
            row = c.execute(
                "SELECT id, started FROM stream_sessions "
                "WHERE username=? AND ended IS NULL "
                "ORDER BY started DESC LIMIT 1", (user,)).fetchone()
            if not row:
                return          # online-Event verpasst (Neustart) → still
            sid, started = row
            # recorded-Flag aus der persistierten Recorder-Historie:
            # lief WÄHREND [started, ended] ein Recorder für diesen User?
            # ±1s Slop nur für Listener-Reihenfolge (Transition-Persist
            # und Session-Hook teilen sich denselben Zeitstempel). Ein
            # größeres Fenster würde bei schnellen Offline/Online-Flaps
            # die Aufnahme fälschlich auf Nachbar-Sessions abfärben.
            rec = c.execute(
                "SELECT 1 FROM transitions WHERE kind='recorder' AND key=? "
                "AND new='running' AND ts BETWEEN ? AND ? LIMIT 1",
                (user, started - 1, ts + 1)).fetchone()
            c.execute(
                "UPDATE stream_sessions SET ended=?, duration_s=?, "
                "recorded=? WHERE id=?",
                (ts, ts - started, 1 if rec else 0, sid))

    def _recover_open_sessions(self) -> None:
        """Nach Bot-Neustart: Sessions ohne Ende, älter als 24h, sind
        Crash-Waisen → als abandoned schließen, damit Profile/Statistik
        nicht durch 'unendliche' Sessions verzerrt werden."""
        cutoff = time.time() - 86400
        try:
            with self._lock, self._conn() as c:
                c.execute(
                    "UPDATE stream_sessions SET ended=started, duration_s=0, "
                    "abandoned=1 WHERE ended IS NULL AND started < ?",
                    (cutoff,))
        except Exception:
            log.debug("Session-Recovery fehlgeschlagen", exc_info=True)

    # -------------------------------------------------------- Abfragen

    def streamer_profile(self, user: str, days: int = 30) -> dict:
        """Aggregierte Sicht auf einen Streamer — Datenbasis für M4/M5.
        hours-Histogramm in UTC; Umrechnung macht das Dashboard (Client
        kennt seine Zone, der Server soll zonenfrei bleiben)."""
        since = time.time() - days * 86400
        with self._lock, self._conn() as c:
            rows = c.execute(
                "SELECT started, duration_s, recorded FROM stream_sessions "
                "WHERE username=? AND started>? AND abandoned=0 "
                "AND ended IS NOT NULL", (user, since)).fetchall()
        if not rows:
            return {"user": user, "days": days, "sessions": 0}
        durs = sorted(r[1] for r in rows)
        hours = [0] * 24
        for r in rows:
            hours[int(time.gmtime(r[0]).tm_hour)] += 1
        peak = max(range(24), key=lambda h: hours[h])
        return {
            "user": user, "days": days, "sessions": len(rows),
            "recorded": sum(r[2] for r in rows),
            "avg_duration_s": round(sum(durs) / len(durs), 1),
            "median_duration_s": round(durs[len(durs) // 2], 1),
            "hours_histogram_utc": hours,
            "peak_hour_utc": peak,
        }

    def metric_series(self, name: str, hours: float = 24,
                      buckets: int = 120) -> list[dict]:
        """Downsampled-Zeitreihe fürs Dashboard: hours-Fenster auf max.
        `buckets` Punkte reduziert (AVG/MIN/MAX pro Bucket). WARUM im SQL:
        14 Tage à 60s-Auflösung sind 20k Zeilen pro Metrik — die schickt
        man nicht roh an ein Mobile-Dashboard."""
        since = time.time() - hours * 3600
        step = max((hours * 3600) / max(buckets, 1), 1)
        with self._lock, self._conn() as c:
            rows = c.execute(
                "SELECT CAST((ts-?)/? AS INT) AS b, AVG(value), "
                "MIN(value), MAX(value), MAX(ts) "
                "FROM metrics WHERE name=? AND ts>? GROUP BY b ORDER BY b",
                (since, step, name, since)).fetchall()
        return [{"ts": r[4], "avg": round(r[1], 3),
                 "min": round(r[2], 3), "max": round(r[3], 3)}
                for r in rows]

    def metric_names(self) -> list[str]:
        with self._lock, self._conn() as c:
            return [r[0] for r in c.execute(
                "SELECT DISTINCT name FROM metrics").fetchall()]

    def events(self, kind: Optional[str] = None, limit: int = 100) -> list[dict]:
        q = "SELECT ts, kind, key, data FROM events "
        args: tuple = ()
        if kind:
            q += "WHERE kind=? "
            args = (kind,)
        q += "ORDER BY ts DESC LIMIT ?"
        with self._lock, self._conn() as c:
            rows = c.execute(q, args + (limit,)).fetchall()
        out = []
        for r in rows:
            try:
                data = json.loads(r[3])
            except Exception:
                data = r[3]
            out.append({"ts": r[0], "kind": r[1], "key": r[2], "data": data})
        return out

    def sessions(self, user: Optional[str] = None,
                 limit: int = 50) -> list[dict]:
        q = ("SELECT username, started, ended, duration_s, recorded, "
             "abandoned FROM stream_sessions ")
        args: tuple = ()
        if user:
            q += "WHERE username=? "
            args = (user,)
        q += "ORDER BY started DESC LIMIT ?"
        with self._lock, self._conn() as c:
            rows = c.execute(q, args + (limit,)).fetchall()
        return [{"user": r[0], "started": r[1], "ended": r[2],
                 "duration_s": r[3], "recorded": bool(r[4]),
                 "abandoned": bool(r[5])} for r in rows]

    # ------------------------------------------------------- Wartung

    def gc(self, retain_days: int) -> None:
        if not retain_days:
            return
        cutoff = time.time() - retain_days * 86400
        try:
            with self._lock, self._conn() as c:
                c.execute("DELETE FROM events WHERE ts<?", (cutoff,))
                c.execute("DELETE FROM metrics WHERE ts<?", (cutoff,))
                # Sessions 6x länger behalten: sie sind winzig (1 Zeile pro
                # Live-Gang) und die wertvollste Datenquelle für M5-Prognosen.
                c.execute("DELETE FROM stream_sessions WHERE started<?",
                          (time.time() - retain_days * 6 * 86400,))
        except Exception:
            log.debug("memory GC fehlgeschlagen", exc_info=True)

    def _init_schema(self) -> None:
        with self._lock, self._conn() as c:
            c.executescript(_SCHEMA)
