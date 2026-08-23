# brain/test_m1.py — M1-Integrationstest
# Simuliert einen realen NIGHTCRAWLER-Ablauf: Recorder stallt,
# Regel erkennt es über den State, Aktion feuert, Entscheidung
# überlebt einen Brain-"Neustart" (Persistenz-Check).
# Ausführung: python3 -m brain.test_m1  (aus dem Projektroot)

import os
import tempfile
import time

os.environ["BRAIN_DB"] = os.path.join(tempfile.mkdtemp(), "brain_test.db")

import brain as brain_mod                                    # noqa: E402
from brain import Unhandled, get_brain                       # noqa: E402


def main():
    b = get_brain()

    # --- Szenario: Recorder-Stall-Watchdog als Regel -----------------
    killed = []

    def cond_stalled(ctx):
        st = ctx["state"]
        stalled = [e for e in st["entities"]
                   if e["kind"] == "recorder" and e["state"] == "stalled"]
        if stalled:
            return {"stalled": [e["key"] for e in stalled],
                    "grund": "Recorder ohne Fortschritt gemeldet"}
        return None

    def act_kill(ctx):
        st = ctx["state"]
        for e in st["entities"]:
            if e["kind"] == "recorder" and e["state"] == "stalled":
                killed.append(e["key"])
                b.state.set("recorder", e["key"], "killed",
                            by="rule:recorder_stall_kill")
        return {"killed": list(killed)}

    b.rules.register("recorder_stall_kill", cond_stalled, act_kill,
                     cooldown_s=0, priority=10, tags=("watchdog",))

    # Recorder läuft → stallt
    b.state.set("recorder", "streamer_x", "running", pid=4711)
    fired = b.tick()
    assert fired == [], "darf bei running nicht feuern"

    b.state.set("recorder", "streamer_x", "stalled")
    fired = b.tick()
    assert len(fired) == 1 and killed == ["streamer_x"]
    assert fired[0]["reason"]["grund"].startswith("Recorder ohne")
    assert b.state.get("recorder", "streamer_x")["state"] == "killed"

    # --- Router-Kaskade: rules passt nicht → db antwortet ------------
    def rules_h(task):
        raise Unhandled("keine Regel für Statistik-Fragen")

    b.router.register("rules", "streamer_stats", rules_h)
    b.router.register("db", "streamer_stats",
                      lambda t: {"user": t.payload["user"], "recs": 42})
    res = b.router.route("streamer_stats", {"user": "streamer_x"})
    assert res["ok"] and res["tier"] == "db" and res["result"]["recs"] == 42

    # --- Persistenz: neues Brain-Objekt liest alte Entscheidungen ----
    time.sleep(0.05)
    b2 = brain_mod.Brain(db_path=os.environ["BRAIN_DB"])
    why = b2.why(limit=5)
    assert why and why[0]["rule"] == "recorder_stall_kill"
    assert why[0]["reason"]["stalled"] == ["streamer_x"]

    # --- Tick-Thread startet und stoppt sauber ------------------------
    b.start_tick(interval_s=0.1)
    time.sleep(0.3)
    assert b.overview()["tick_alive"]
    b.stop_tick()

    print("test_m1 OK — State/Rules/Router/Persistenz/Tick grün")


if __name__ == "__main__":
    main()
