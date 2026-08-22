# brain/test_m7.py — M7-Integrationstest
# Prüft: Registry+Status, Toggle persistiert über Brain-Neustart,
# Fehler-Isolation (kaputter Agent tötet nichts), HealthAgent-Befunde,
# RecoveryAgent beobachtet vs. handelt (env-Gate) auf echter bot-DB,
# ScoutAgent aus Seeds, LearningAgent Prognose→Ergebnis→Brier.
# Ausführung: python3 -m brain.test_m7

import contextlib
import os
import sqlite3
import tempfile
import time

TMP = tempfile.mkdtemp()
os.environ["BRAIN_DB"] = os.path.join(TMP, "brain_m7.db")

import brain as brain_mod                                    # noqa: E402
from brain import (Agent, get_brain,                         # noqa: E402
                   HealthAgent, LearningAgent, RecoveryAgent, ScoutAgent)

BOT_DB = os.path.join(TMP, "bot.db")


@contextlib.contextmanager
def db_conn():
    conn = sqlite3.connect(BOT_DB)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()


def main():
    c = sqlite3.connect(BOT_DB)
    c.execute("CREATE TABLE trackings(id INTEGER PRIMARY KEY, username "
              "TEXT, recording INT, pid INT, last_live INT, paused INT)")
    c.execute("INSERT INTO trackings(username, recording, pid) "
              "VALUES('stuck', 1, 999999)")
    c.commit()
    c.close()

    b = get_brain()
    notes = []
    b.agents._notify = notes.append

    # --- Registry, Status, kaputter Agent isoliert -----------------------
    class Broken(Agent):
        name = "broken"
        interval_s = 0.0

        def run(self, ctx):
            raise RuntimeError("kaputt")

    b.agents.register(HealthAgent(b))
    b.agents.register(Broken())
    findings = b.agents.run_due({"trigger": "test"})
    assert isinstance(findings, list)                    # kein Crash
    st = {a["name"]: a for a in b.agents.status()}
    assert st["broken"]["errors"] == 1
    assert "kaputt" in st["broken"]["last_error"]
    assert st["health"]["runs"] == 1
    assert b.state.get("agent", "broken")["state"] == "error"

    # --- Toggle persistiert über Neustart ----------------------------------
    assert b.agents.enable("broken", False)
    assert b.state.get("agent", "broken")["state"] == "disabled"
    b2 = brain_mod.Brain(db_path=os.environ["BRAIN_DB"])
    b2.agents.register(Broken())
    assert not b2.agents._enabled["broken"]              # aus brain.db geladen

    # --- RecoveryAgent: beobachten (Gate zu) --------------------------------
    b.state.set("recorder", "stuck", "pid_dead", pid=999999)
    # since künstlich altern lassen (>stuck_s)
    with b.state._lock:
        b.state._entities[("recorder", "stuck")].since -= 700
    gate = {"recovery": False}
    rec = RecoveryAgent(b, db_conn=db_conn,
                        act_check=lambda n: gate.get(n, False))
    b.agents.register(rec)
    f = b.agents.run_one("recovery", {})
    assert any(x["level"] == "crit" and "Reaper klemmt" in x["text"]
               for x in f), f
    assert any("[recovery]" in n for n in notes)         # crit → notify
    with db_conn() as conn:                              # NICHT angefasst
        assert conn.execute("SELECT recording FROM trackings "
                            "WHERE username='stuck'").fetchone()[0] == 1

    # --- RecoveryAgent: handeln (Gate offen) ----------------------------------
    gate["recovery"] = True
    f = b.agents.run_one("recovery", {})
    assert any(x.get("action") == "cleared_stale_recording" for x in f), f
    with db_conn() as conn:
        row = conn.execute("SELECT recording, pid FROM trackings "
                           "WHERE username='stuck'").fetchone()
        assert row[0] == 0 and row[1] is None            # Reaper-Operation

    # --- ScoutAgent aus geseedeten Sessions -------------------------------------
    now = time.time()
    cur_h = time.gmtime().tm_hour
    with b._db_lock, b._conn() as cc:
        for d in range(1, 9):
            t = time.gmtime(now - d * 86400)
            mid = (now - d * 86400) - t.tm_hour * 3600 - t.tm_min * 60 - t.tm_sec
            s = mid + cur_h * 3600
            cc.execute("INSERT INTO stream_sessions(username, started, "
                       "ended, duration_s, recorded, abandoned) "
                       "VALUES('hotuser',?,?,3600,1,0)", (s, s + 3600))
    b.agents.register(ScoutAgent(b))
    f = b.agents.run_one("scout", {})
    assert any(x["user"] == "hotuser" for x in f), f
    assert b.memory.events(kind="agent_finding")         # Befunde im Memory

    # --- LearningAgent: Prognose → Ergebnis → Brier -------------------------------
    la = LearningAgent(b)
    b.agents.register(la)
    b.agents.run_one("learning", {})                     # schreibt Prognosen
    preds = [e for e in b.memory.events(kind="prediction", limit=50)
             if e["data"]["user"] == "hotuser"]
    assert preds and preds[0]["data"]["prob"] > 0
    # Vorstunden-Prognose faken + hotuser war "live" (Session existiert
    # in den letzten 2h? seeden):
    prev_h = time.gmtime(now - 3600).tm_hour
    b.memory.record_event("prediction", "hotuser", user="hotuser",
                          hour_utc=prev_h, prob=0.8)
    with b._db_lock, b._conn() as cc:
        cc.execute("INSERT INTO stream_sessions(username, started, ended, "
                   "duration_s, recorded, abandoned) "
                   "VALUES('hotuser',?,?,600,1,0)", (now - 1800, now - 1200))
    f = b.agents.run_one("learning", {})
    assert any("Brier" in x.get("text", "") for x in f), f
    briers = b.memory.metric_series("prediction_brier", hours=1)
    assert briers and briers[-1]["avg"] <= 0.25          # 0.8 vs 1.0 → 0.04er-Nähe

    # --- B153: ProxyHealthAgent Schwellen (Regressionsschutz) ---
    from brain.agents import ProxyHealthAgent
    _snaps = []
    pa = ProxyHealthAgent(b, tiktok_status=lambda: _snaps[-1])

    def _prun(by_code):
        _snaps.append({"by_code": by_code, "record_proxy": True, "pool_size": 0})
        return pa.run({})

    def _lvl(r):
        return r[0]["level"] if r else "still"
    assert _lvl(_prun({200: 100, 403: 5})) == "still"      # erste Runde: nur Basis
    assert _lvl(_prun({200: 200, 403: 6})) == "still"      # gesund
    assert _lvl(_prun({200: 205, 403: 60})) == "crit"      # 403-Sturm >50%
    assert _lvl(_prun({200: 225, 403: 75})) == "warn"      # Erfolg ~57%
    assert _lvl(_prun({200: 230, 403: 78})) == "still"     # <15 Samples -> keine Aussage
    assert b.memory.metric_series("tiktok_fetch_success_pct", hours=1), \
        "ProxyHealthAgent: Erfolgsrate-Metrik fehlt"

    print("test_m7 OK — Registry/Toggle-Persistenz/Isolation/Recovery-Gate/"
          "Scout/Learning-Brier/Proxy-Wächter grün")


if __name__ == "__main__":
    main()
