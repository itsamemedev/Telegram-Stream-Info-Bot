# brain/test_m5.py — M5-Integrationstest
# Prüft: Go-Live-Wahrscheinlichkeit (inkl. Flap-Schutz: 5 Sessions an
# EINEM Tag ≠ 5 verlässliche Tage), Kernel-Glättung, Hint-Planung mit
# Begründung, CPU-Saisonforecast, upcoming(), Aktions-Gate env-gated.
# Ausführung: python3 -m brain.test_m5

import os
import tempfile
import time

os.environ["BRAIN_DB"] = os.path.join(tempfile.mkdtemp(), "brain_m5.db")

from brain import get_brain                                  # noqa: E402
from brain.scheduler import MAX_INTERVAL_S, MIN_INTERVAL_S   # noqa: E402

HOUR = 3600


def _day_at(days_ago: int, hour_utc: int) -> float:
    now = time.time()
    t = time.gmtime(now)
    midnight = now - t.tm_hour * HOUR - t.tm_min * 60 - t.tm_sec
    return midnight - days_ago * 86400 + hour_utc * HOUR


def _seed(b, user, starts, dur=1800):
    with b._db_lock, b._conn() as c:
        c.executemany(
            "INSERT INTO stream_sessions(username, started, ended, "
            "duration_s, recorded, abandoned) VALUES(?,?,?,?,1,0)",
            [(user, s, s + dur, dur) for s in starts])


def main():
    b = get_brain()
    sch, mem = b.scheduler, b.memory

    # zuverlaessig: 10 der letzten 20 Tage um 20 UTC live
    _seed(b, "zuverlaessig", [_day_at(d, 20) for d in range(1, 21, 2)])
    # flapper: 5 Sessions, aber alle am SELBEN Tag um 10 UTC
    base = _day_at(3, 10)
    _seed(b, "flapper", [base + i * 120 for i in range(5)], dur=60)

    # --- Wahrscheinlichkeits-Mathematik ---------------------------------
    p = sch.go_live_prob(mem, "zuverlaessig", 20)
    assert 0.2 <= p["prob"] <= 0.6, p        # ~10/20 Tage · Kernel 0.5-Mitte
    p_off = sch.go_live_prob(mem, "zuverlaessig", 8)
    assert p_off["prob"] < 0.05, p_off       # 8 UTC praktisch nie
    p_n = sch.go_live_prob(mem, "zuverlaessig", 21)
    assert p_n["prob"] > 0.05, p_n           # Kernel: Nachbarstunde > 0
    # Flap-Schutz: 5 Sessions an 1 Tag → P bleibt klein
    p_f = sch.go_live_prob(mem, "flapper", 10)
    assert p_f["prob"] <= 0.2, p_f
    assert "Sessions" in p["basis"]          # Begründung vorhanden
    assert sch.go_live_prob(mem, "niemand", 20)["prob"] == 0.0

    # --- Hint-Planung ------------------------------------------------------
    hints = sch.plan(mem)
    hu = {h["username"]: h for h in hints}
    assert set(hu) == {"zuverlaessig", "flapper"}
    for h in hints:
        assert MIN_INTERVAL_S <= h["interval_s"] <= MAX_INTERVAL_S
        assert "P(live" in h["reason"]       # jede Empfehlung begründet
    # Persistiert + sortiert nach Priorität
    stored = sch.hints()
    assert stored and stored[0]["priority"] >= stored[-1]["priority"]
    assert sch.hints(user="flapper")[0]["username"] == "flapper"

    # Höhere P jetzt ⇒ kürzeres Intervall (Monotonie über die Formel):
    now_h = time.gmtime().tm_hour
    pz = sch.go_live_prob(mem, "zuverlaessig", now_h)["prob"]
    pf = sch.go_live_prob(mem, "flapper", now_h)["prob"]
    if pz != pf:
        hi, lo = (("zuverlaessig", "flapper") if pz > pf
                  else ("flapper", "zuverlaessig"))
        assert hu[hi]["interval_s"] <= hu[lo]["interval_s"]

    # --- CPU-Forecast --------------------------------------------------------
    for d in range(3):
        for h in range(24):
            ts = _day_at(d + 1, h) + 1800
            val = 0.9 if h == 20 else 0.3     # abends eng, sonst locker
            mem.record_metric("load_ratio15", val, ts=ts)
    fc = sch.cpu_forecast(mem, horizon_h=24)
    by_h = {x["hour_utc"]: x for x in fc}
    assert by_h[20]["warn"] and by_h[20]["load_ratio_avg"] >= 0.85
    assert not by_h[(20 + 6) % 24]["warn"]
    assert by_h[20]["samples"] >= 3

    # --- upcoming ---------------------------------------------------------------
    up = sch.upcoming(mem, horizon_h=24, threshold=0.1)
    assert any(u["user"] == "zuverlaessig" and u["hour_utc"] in (19, 20, 21)
               for u in up), up
    assert up == sorted(up, key=lambda x: (x["in_hours"], -x["prob"]))

    # --- Aktions-Gate (env, einzeln, default aus) ---------------------------------
    import brain_bridge
    assert not brain_bridge._act_enabled("brain_db_big")
    os.environ["BRAIN_ACT_BRAIN_DB_BIG"] = "1"
    assert brain_bridge._act_enabled("brain_db_big")
    os.environ["BRAIN_ACT_BRAIN_DB_BIG"] = "0"
    assert not brain_bridge._act_enabled("brain_db_big")

    print("test_m5 OK — Prognose/Flap-Schutz/Hints/Forecast/Gate grün")


if __name__ == "__main__":
    main()
