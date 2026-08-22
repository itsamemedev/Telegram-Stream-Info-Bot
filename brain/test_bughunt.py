# brain/test_bughunt.py — Regressionstests der Tiefengrund-Bughunt-Runde
# BH-1 Restream-Geister · BH-2 Tick-Heartbeat · BH-4 evaluate-Race ·
# BH-5 Connection-Close · BH-6 VACUUM über den neuen Contextmanager
# Ausführung: python3 -m brain.test_bughunt

import contextlib
import os
import sqlite3
import tempfile
import threading

TMP = tempfile.mkdtemp()
os.environ["BRAIN_DB"] = os.path.join(TMP, "bh.db")
os.environ["BRAIN_TICK_S"] = "999"

import brain_bridge                                          # noqa: E402
from brain import get_brain                                  # noqa: E402

BOT = os.path.join(TMP, "bot.db")


@contextlib.contextmanager
def db_conn():
    conn = sqlite3.connect(BOT)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()


def main():
    c = sqlite3.connect(BOT)
    c.executescript("""
    CREATE TABLE trackings(id INTEGER PRIMARY KEY, username TEXT,
        recording INT, pid INT, last_live INT, paused INT DEFAULT 0);
    CREATE TABLE restreams(id INTEGER PRIMARY KEY, label TEXT,
        source_username TEXT, enabled INT DEFAULT 1, status TEXT,
        pid INT, started_at TEXT);
    CREATE TABLE recordings(id INTEGER PRIMARY KEY, username TEXT);""")
    c.execute("INSERT INTO restreams(label,status) VALUES('KICK','error')")
    c.commit()
    c.close()
    brain_bridge._ctx.update(db_conn=db_conn)
    b = get_brain()

    # --- BH-1: Restream-Geister werden aufgeräumt ------------------------
    brain_bridge._sync_db_state()
    assert b.state.get("restream", "restream:1")["state"] == "error"
    with sqlite3.connect(BOT) as cc:
        cc.execute("DELETE FROM restreams")
    brain_bridge._sync_db_state()
    assert b.state.get("restream", "restream:1") is None, "BH-1 Regression"

    # --- BH-2: Bridge-Tick setzt Heartbeat → tick_alive -------------------
    assert not b.overview()["tick_alive"]          # noch kein Tick
    brain_bridge._bridge_tick()
    assert b.overview()["tick_alive"], "BH-2 Regression"

    # --- BH-4: paralleles evaluate feuert Cooldown-Regel genau 1x ---------
    hits = []
    b.rules.register("bh4", lambda ctx: "immer",
                     lambda ctx: hits.append(1) or "ok", cooldown_s=3600)
    barrier = threading.Barrier(8)

    def worker():
        barrier.wait()
        b.rules.evaluate({"trigger": "race"})

    ts = [threading.Thread(target=worker) for _ in range(8)]
    [t.start() for t in ts]
    [t.join() for t in ts]
    assert len(hits) == 1, f"BH-4 Regression: {len(hits)}x gefeuert"

    # --- BH-5: Connections werden geschlossen (fd-Zählung stabil) ---------
    def open_fds():
        return len(os.listdir("/proc/self/fd"))
    base = open_fds()
    for _ in range(120):
        b.memory.record_metric("bh5", 1.0)
        b.state.set("stream", "bh5user", "online")
        b.state.set("stream", "bh5user", "offline")
    grown = open_fds() - base
    assert grown <= 3, f"BH-5 Regression: fd-Wachstum {grown}"

    # --- BH-6: VACUUM läuft über den neuen Contextmanager -----------------
    b.memory.gc(1)
    with b._db_lock, b._conn() as conn:
        conn.execute("VACUUM")
    # Exception-Pfad: rollback + close, kein hängender Lock
    try:
        with b._db_lock, b._conn() as conn:
            conn.execute("SELECT * FROM gibtsnicht")
        raise AssertionError("hätte werfen müssen")
    except sqlite3.OperationalError:
        pass
    with b._db_lock, b._conn() as conn:            # DB weiter benutzbar
        conn.execute("SELECT 1")

    # --- BH-8: tick() führt Retention aus (unabhängig vom Tick-Treiber) ---
    with b._db_lock, b._conn() as conn:
        conn.execute("INSERT INTO metrics VALUES(?, 'bh8', 1.0)",
                     (__import__('time').time() - 100 * 86400,))
    b._last_gc = 0.0                                  # GC sofort fällig
    b.tick()
    with b._db_lock, b._conn() as conn:
        n = conn.execute("SELECT COUNT(*) FROM metrics "
                         "WHERE name='bh8'").fetchone()[0]
    assert n == 0, "BH-8 Regression: Retention lief nicht im tick()"

    # --- BH-11: doppeltes init_bridge crasht nicht und behält Routen ------
    from flask import Flask
    app = Flask("bh11")
    brain_bridge._ctx.pop("_initialized", None)
    brain_bridge.init_bridge(db_conn=db_conn, flask_app=app,
                             start_tick=False)
    brain_bridge.init_bridge(db_conn=db_conn, flask_app=app,
                             start_tick=False)       # zweiter Aufruf
    assert app.test_client().get("/api/brain/overview").status_code == 200

    # --- IMP-3: Agenten-Läufe fluten die Transition-Historie nicht --------
    from brain import HealthAgent
    b.agents.register(HealthAgent(b))
    with b._db_lock, b._conn() as conn:
        before = conn.execute("SELECT COUNT(*) FROM transitions "
                              "WHERE kind='agent'").fetchone()[0]
    for _ in range(5):
        b.agents.run_one("health", {})
    with b._db_lock, b._conn() as conn:
        after = conn.execute("SELECT COUNT(*) FROM transitions "
                             "WHERE kind='agent'").fetchone()[0]
    assert after - before <= 1, \
        f"IMP-3 Regression: {after - before} Agent-Transitions für 5 Läufe"

    # --- IMP-4: LLM-health gecacht (Probes nicht pro Aufruf) ---------------
    probes = []
    orig = type(b.llm)._probe
    type(b.llm)._probe = lambda self, be: probes.append(be) or \
        {"up": False, "error": "test"}
    try:
        b.llm._health_cache = None
        b.llm.health(); b.llm.health(); b.llm.health()
        # V37: nur noch llamacpp-Backend → 1 Probe für 3 health()-Calls (Cache!)
        assert len(probes) == 1, f"IMP-4 Regression: {len(probes)} Probes"
    finally:
        type(b.llm)._probe = orig

    print("test_bughunt OK — BH-1/2/4/5/6/8/11/13 + IMP-3/4 abgesichert")


if __name__ == "__main__":
    main()
