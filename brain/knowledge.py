# brain/knowledge.py — M4: Knowledge Graph
#
# WARUM Triple-Store (Subjekt–Prädikat–Objekt) in SQLite statt einer
# Graph-DB: Der Graph hat hunderte Knoten (Streamer, Stunden, Kategorien),
# nicht Millionen. SQLite mit (s,p,o)-Index beantwortet jede Wildcard-
# Abfrage in <1ms, braucht 0 neue Dependencies und 0 zusätzliche RAM-
# Prozesse — 24/7-CPU-Budget-Regel von v37.
#
# WOHER die Fakten kommen: refresh() leitet sie aus M3 ab (stream_sessions).
# KEINE Meldepunkte in bot_v36 — Zero-Call-Site wie M2/M3. Jeder abgeleitete
# Fakt trägt source + reason → "Warum wurde diese Entscheidung getroffen?"
# ist pro Fakt UND pro Empfehlung beantwortbar.
#
# ABGRENZUNG zur Rules Engine: Regeln reagieren auf JETZT (Disk voll).
# Der Graph beantwortet Zusammenhangs-Fragen über GELERNTES (wer streamt
# wann, wer ist zuverlässig live) — Tier 3 des Routers, vor dem LLM.

from __future__ import annotations

import logging
import threading
import time
from typing import Callable, Optional

log = logging.getLogger("brain.knowledge")

_SCHEMA = """
CREATE TABLE IF NOT EXISTS triples(
    s TEXT, p TEXT, o TEXT,
    weight REAL DEFAULT 1.0,
    ts REAL, source TEXT, reason TEXT,
    PRIMARY KEY (s, p, o));
CREATE INDEX IF NOT EXISTS idx_tri_p ON triples(p, o);
CREATE INDEX IF NOT EXISTS idx_tri_o ON triples(o);
"""

# Mindestsessions, bevor Fakten abgeleitet werden. Unter 3 Sessions ist
# jedes "typisch um 20 Uhr" statistisches Rauschen — lieber kein Fakt
# als ein falscher (der Graph füttert später Aufnahme-Prioritäten!).
MIN_SESSIONS = 3

# Fakten, die refresh() verwaltet. Manuell/extern gesetzte Fakten mit
# anderen Prädikaten werden bei der Neuableitung NICHT angefasst.
_DERIVED_PREDICATES = ("peak_hour_utc", "active_hour", "duration_class",
                       "sessions_per_week", "record_ratio")


class KnowledgeGraph:
    def __init__(self, conn_factory: Callable, db_lock: threading.Lock):
        self._conn = conn_factory
        self._lock = db_lock
        self._last_refresh = 0.0
        with self._lock, self._conn() as c:
            c.executescript(_SCHEMA)

    # ---------------------------------------------------------- Fakten

    def assert_fact(self, s: str, p: str, o: str, weight: float = 1.0,
                    source: str = "manual", reason: str = "") -> None:
        """Upsert: gleiche (s,p,o) aktualisiert Gewicht/Zeit statt zu
        duplizieren — refresh() darf beliebig oft laufen (idempotent)."""
        with self._lock, self._conn() as c:
            c.execute(
                "INSERT INTO triples VALUES(?,?,?,?,?,?,?) "
                "ON CONFLICT(s,p,o) DO UPDATE SET weight=excluded.weight, "
                "ts=excluded.ts, source=excluded.source, "
                "reason=excluded.reason",
                (s, p, str(o), weight, time.time(), source, reason))

    def retract(self, s: Optional[str] = None, p: Optional[str] = None,
                o: Optional[str] = None) -> int:
        conds, args = self._where(s, p, o)
        with self._lock, self._conn() as c:
            cur = c.execute(f"DELETE FROM triples {conds}", args)
            return cur.rowcount

    def query(self, s: Optional[str] = None, p: Optional[str] = None,
              o: Optional[str] = None, limit: int = 200) -> list[dict]:
        """Wildcard-Abfrage: jedes None ist frei. query(p='peak_hour_utc')
        → alle Streamer mit bekannter Peak-Stunde."""
        conds, args = self._where(s, p, o)
        with self._lock, self._conn() as c:
            rows = c.execute(
                f"SELECT s,p,o,weight,ts,source,reason FROM triples {conds} "
                f"ORDER BY weight DESC LIMIT ?", args + (limit,)).fetchall()
        return [{"s": r[0], "p": r[1], "o": r[2], "weight": r[3],
                 "ts": r[4], "source": r[5], "reason": r[6]} for r in rows]

    def graph_export(self, limit: int = 500) -> dict:
        """Knoten+Kanten fürs Dashboard (M8-Visualisierung)."""
        facts = self.query(limit=limit)
        nodes: dict[str, dict] = {}
        for f in facts:
            nodes.setdefault(f["s"], {"id": f["s"], "kind": "subject"})
            nodes.setdefault(f["o"], {"id": f["o"], "kind": "value"})
        return {"nodes": list(nodes.values()),
                "edges": [{"from": f["s"], "to": f["o"], "label": f["p"],
                           "weight": f["weight"]} for f in facts]}

    # -------------------------------------------------- Ableitung (M3→M4)

    def refresh(self, memory, min_sessions: int = MIN_SESSIONS,
                days: int = 30) -> int:
        """Fakten aus Memory-Sessions neu ableiten. Idempotent (Upsert).
        Rückgabe: Anzahl aktualisierter Fakten. Veraltete abgeleitete
        Fakten (Streamer ohne Sessions mehr) werden entfernt, damit der
        Graph nicht mit Karteileichen wächst."""
        users = self._session_users(memory, days)
        n = 0
        fresh: set[tuple] = set()
        for user in users:
            prof = memory.streamer_profile(user, days=days)
            if prof.get("sessions", 0) < min_sessions:
                continue
            n += self._derive_user(user, prof, days, fresh)
        self._prune_stale_derived(fresh)
        self._last_refresh = time.time()
        log.info("KG-Refresh: %d Fakten aus %d Streamern", n, len(users))
        return n

    def _derive_user(self, user: str, prof: dict, days: int,
                     fresh: set) -> int:
        n = 0
        hist = prof["hours_histogram_utc"]
        total = sum(hist) or 1
        src = f"memory:{days}d"

        def put(p, o, w, reason):
            nonlocal n
            self.assert_fact(user, p, o, w, source=src, reason=reason)
            fresh.add((user, p, str(o)))
            n += 1

        peak = prof["peak_hour_utc"]
        share = hist[peak] / total
        put("peak_hour_utc", peak, round(share, 3),
            f"{hist[peak]}/{total} Sessions in Stunde {peak} UTC")
        # Top-3 aktive Stunden (statt aller 24: Graph klein halten)
        for h in sorted(range(24), key=lambda x: hist[x], reverse=True)[:3]:
            if hist[h]:
                put("active_hour", h, round(hist[h] / total, 3),
                    f"{hist[h]} Sessions in Stunde {h} UTC")
        avg_min = prof["avg_duration_s"] / 60
        cls = "short" if avg_min < 15 else "medium" if avg_min < 60 else "long"
        put("duration_class", cls, 1.0, f"Ø {avg_min:.0f}min")
        put("sessions_per_week",
            round(prof["sessions"] / max(days / 7, 1), 2), 1.0,
            f"{prof['sessions']} Sessions in {days}d")
        put("record_ratio",
            round(prof["recorded"] / max(prof["sessions"], 1), 2), 1.0,
            f"{prof['recorded']}/{prof['sessions']} Sessions aufgenommen")
        return n

    def _prune_stale_derived(self, fresh: set) -> None:
        with self._lock, self._conn() as c:
            marks = ",".join("?" * len(_DERIVED_PREDICATES))
            rows = c.execute(
                f"SELECT s,p,o FROM triples WHERE p IN ({marks})",
                _DERIVED_PREDICATES).fetchall()
            stale = [r for r in rows if (r[0], r[1], str(r[2])) not in fresh]
            for r in stale:
                c.execute("DELETE FROM triples WHERE s=? AND p=? AND o=?", r)
            if stale:
                log.info("KG-Prune: %d veraltete Fakten entfernt", len(stale))

    # ---------------------------------------------------- Inferenz/Empfehlung

    def who_streams_at(self, hour_utc: int) -> list[dict]:
        out = []
        for f in self.query(p="active_hour", o=str(hour_utc)):
            out.append({"user": f["s"], "share": f["weight"],
                        "reason": f["reason"]})
        return sorted(out, key=lambda x: -x["share"])

    def recommend(self, hour_utc: Optional[int] = None,
                  top: int = 10) -> list[dict]:
        """Ranking 'welchen Streamer jetzt priorisieren?' — vollständig
        erklärbar: jede Komponente steht in components + reason.

        Score = 0.4·Aktivität + 0.3·Dauer + 0.3·Stunden-Nähe.
        Gewichte bewusst simpel und hier dokumentiert statt 'gelernt' —
        nachvollziehbar > clever, bis M5 echte Prognosen liefert."""
        hour = hour_utc if hour_utc is not None else time.gmtime().tm_hour
        users = {f["s"] for f in self.query(p="sessions_per_week")}
        ranked = []
        for u in users:
            facts = {f["p"]: f for f in self.query(s=u)}
            spw = float(facts.get("sessions_per_week", {}).get("o", 0))
            act = min(spw / 7.0, 1.0)                    # 1×/Tag = voll
            dur = {"short": 0.3, "medium": 0.7,
                   "long": 1.0}.get(facts.get("duration_class",
                                              {}).get("o"), 0.5)
            hour_match, hour_why = 0.0, "keine Stunden-Daten"
            best = None
            for f in self.query(s=u, p="active_hour"):
                d = min(abs(int(f["o"]) - hour), 24 - abs(int(f["o"]) - hour))
                m = max(0.0, 1.0 - d / 4.0) * f["weight"]   # ±4h Fenster
                if m > hour_match:
                    hour_match, best = m, f
            if best:
                hour_why = (f"aktive Stunde {best['o']} UTC "
                            f"(Anteil {best['weight']}) vs. jetzt {hour} UTC")
            score = 0.4 * act + 0.3 * dur + 0.3 * hour_match
            ranked.append({
                "user": u, "score": round(score, 3),
                "components": {"activity": round(act, 3),
                               "duration": dur,
                               "hour_match": round(hour_match, 3)},
                "reason": (f"{spw}/Woche aktiv; Dauerklasse "
                           f"{facts.get('duration_class', {}).get('o', '?')}; "
                           f"{hour_why}"),
            })
        return sorted(ranked, key=lambda x: -x["score"])[:top]

    def stats(self) -> dict:
        with self._lock, self._conn() as c:
            n = c.execute("SELECT COUNT(*) FROM triples").fetchone()[0]
            preds = c.execute(
                "SELECT p, COUNT(*) FROM triples GROUP BY p").fetchall()
        return {"triples": n, "predicates": dict(preds),
                "last_refresh": self._last_refresh}

    # -------------------------------------------------------- intern

    @staticmethod
    def _session_users(memory, days: int) -> list[str]:
        since = time.time() - days * 86400
        with memory._lock, memory._conn() as c:
            rows = c.execute(
                "SELECT DISTINCT username FROM stream_sessions "
                "WHERE started>? AND abandoned=0", (since,)).fetchall()
        return [r[0] for r in rows]

    @staticmethod
    def _where(s, p, o) -> tuple[str, tuple]:
        conds, args = [], []
        for col, val in (("s", s), ("p", p), ("o", o)):
            if val is not None:
                conds.append(f"{col}=?")
                args.append(str(val))
        return ("WHERE " + " AND ".join(conds)) if conds else "", tuple(args)
