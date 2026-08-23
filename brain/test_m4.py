# brain/test_m4.py — M4-Integrationstest
# Prüft: Fakten-Ableitung aus Memory, Refresh-Idempotenz (Upsert),
# Prune von Karteileichen, MIN_SESSIONS-Rauschfilter, Empfehlung mit
# Begründung, who_streams_at, Graph-Export.
# Ausführung: python3 -m brain.test_m4

import os
import tempfile
import time

os.environ["BRAIN_DB"] = os.path.join(tempfile.mkdtemp(), "brain_m4.db")

from brain import get_brain                                  # noqa: E402

HOUR = 3600


def _seed_sessions(b, user, hours_utc, dur_s=1800, recorded=1):
    """Sessions direkt in die M3-Tabelle legen — deterministische
    Startzeiten (State-Transitions würden 'jetzt' stempeln)."""
    now = time.time()
    with b._db_lock, b._conn() as c:
        for i, h in enumerate(hours_utc):
            day_start = now - (i + 1) * 86400
            t = time.gmtime(day_start)
            base = day_start - t.tm_hour * HOUR - t.tm_min * 60 - t.tm_sec
            start = base + h * HOUR
            c.execute(
                "INSERT INTO stream_sessions(username, started, ended, "
                "duration_s, recorded, abandoned) VALUES(?,?,?,?,?,0)",
                (user, start, start + dur_s, dur_s, recorded))


def main():
    b = get_brain()

    # gamma: 6 Sessions, immer 20 Uhr UTC, lang, immer aufgenommen
    _seed_sessions(b, "gamma", [20] * 6, dur_s=2 * HOUR, recorded=1)
    # delta: 4 Sessions, 8 Uhr UTC, kurz, nie aufgenommen
    _seed_sessions(b, "delta", [8] * 4, dur_s=600, recorded=0)
    # epsilon: nur 2 Sessions → unter MIN_SESSIONS, KEINE Fakten
    _seed_sessions(b, "epsilon", [12] * 2)

    n = b.knowledge.refresh(b.memory)
    assert n > 0

    # --- Ableitung korrekt --------------------------------------------
    f = {x["p"]: x for x in b.knowledge.query(s="gamma")}
    assert f["peak_hour_utc"]["o"] == "20"
    assert f["duration_class"]["o"] == "long"
    assert float(f["record_ratio"]["o"]) == 1.0
    assert "Sessions in Stunde 20" in f["peak_hour_utc"]["reason"]  # WARUM
    f = {x["p"]: x for x in b.knowledge.query(s="delta")}
    assert f["duration_class"]["o"] == "short"
    assert float(f["record_ratio"]["o"]) == 0.0
    assert b.knowledge.query(s="epsilon") == []       # Rauschfilter greift

    # --- Idempotenz: zweiter Refresh dupliziert nichts ------------------
    before = b.knowledge.stats()["triples"]
    b.knowledge.refresh(b.memory)
    assert b.knowledge.stats()["triples"] == before

    # --- who_streams_at ---------------------------------------------------
    who = b.knowledge.who_streams_at(20)
    assert who and who[0]["user"] == "gamma"

    # --- Empfehlung: um 20 UTC muss gamma vor delta liegen ----------------
    recs = b.knowledge.recommend(hour_utc=20)
    assert recs[0]["user"] == "gamma", recs
    assert recs[0]["components"]["hour_match"] > 0.9
    assert "aktive Stunde 20" in recs[0]["reason"]     # erklärbar
    # um 8 UTC dreht sich hour_match — delta holt auf
    recs8 = b.knowledge.recommend(hour_utc=8)
    d8 = next(r for r in recs8 if r["user"] == "delta")
    d20 = next(r for r in recs if r["user"] == "delta")
    assert d8["score"] > d20["score"]

    # --- Prune: gamma-Sessions "veralten" → Fakten verschwinden ------------
    with b._db_lock, b._conn() as c:
        c.execute("UPDATE stream_sessions SET started=started-90*86400 "
                  "WHERE username='gamma'")
    b.knowledge.refresh(b.memory)
    assert b.knowledge.query(s="gamma") == []          # Karteileiche weg
    assert b.knowledge.query(s="delta")                # delta bleibt

    # --- manuelle Fakten überleben refresh ----------------------------------
    b.knowledge.assert_fact("delta", "category", "IRL", source="operator")
    b.knowledge.refresh(b.memory)
    assert b.knowledge.query(s="delta", p="category")

    # --- Graph-Export ---------------------------------------------------------
    g = b.knowledge.graph_export()
    assert g["nodes"] and g["edges"]
    assert any(e["label"] == "category" for e in g["edges"])

    print("test_m4 OK — Ableitung/Idempotenz/Prune/Empfehlung/Erklärung grün")


if __name__ == "__main__":
    main()
