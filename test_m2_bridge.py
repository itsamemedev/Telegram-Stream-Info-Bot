# test_m2_bridge.py — M2-Integrationstest
# Simuliert bot_v36-Umgebung: echte SQLite-DB im trackings/restreams-
# Schema, Flask-Testclient, toter/lebender PID, Cookie-Alter.
# Ausführung: python3 test_m2_bridge.py  (im Projektroot neben brain/)

import contextlib
import os
import sqlite3
import tempfile
import time

TMP = tempfile.mkdtemp()
os.environ["BRAIN_DB"] = os.path.join(TMP, "brain.db")
os.environ["BRAIN_TICK_S"] = "999"          # kein Auto-Tick im Test
os.environ["BRAIN_COOKIE_MAX_AGE_D"] = "7"
os.environ["BRAIN_REC_PARALLEL_WARN"] = "2"

import brain_bridge                                          # noqa: E402
from brain import get_brain                                  # noqa: E402

BOT_DB = os.path.join(TMP, "bot.db")


def _mk_bot_db():
    c = sqlite3.connect(BOT_DB)
    c.executescript("""
    CREATE TABLE trackings(id INTEGER PRIMARY KEY, group_id INT,
        username TEXT, added_by INT, created_at TEXT, last_live INT,
        recording INT, output_file TEXT, pid INT, paused INT DEFAULT 0);
    CREATE TABLE restreams(id INTEGER PRIMARY KEY, created_at TEXT,
        label TEXT, source_username TEXT, ingest_url TEXT, stream_key TEXT,
        transcode INT, enabled INT DEFAULT 1, status TEXT DEFAULT 'idle',
        pid INT, started_at TEXT, last_error TEXT);
    CREATE TABLE recordings(id INTEGER PRIMARY KEY, username TEXT,
        filepath TEXT, created_at TEXT);
    """)
    my_pid = os.getpid()                     # lebt garantiert
    c.executemany(
        "INSERT INTO trackings(group_id, username, last_live, recording, pid)"
        " VALUES(1,?,?,?,?)",
        [("alpha", 1, 1, my_pid),            # läuft sauber
         ("delta", 1, 1, my_pid),            # zweiter lebender Recorder
         ("bravo", 1, 1, 999999),            # PID tot → recorder_pid_dead
         ("charlie", 0, 0, None)])           # offline, keine Aufnahme
    c.execute("INSERT INTO restreams(created_at, label, status, pid) "
              "VALUES('x','KICK-Main','error',NULL)")
    c.executemany("INSERT INTO recordings(username, filepath, created_at) "
                  "VALUES(?, 'f', 'x')", [("alpha",)] * 5)
    c.commit()
    c.close()


@contextlib.contextmanager
def db_conn():
    conn = sqlite3.connect(BOT_DB)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()


def main():
    _mk_bot_db()
    # Alte Cookie-Datei simulieren (10 Tage)
    cookie = os.path.join(TMP, "tiktok_cookies.txt")
    open(cookie, "w").write("# netscape")
    os.utime(cookie, (time.time() - 10 * 86400,) * 2)

    alerts = []
    try:
        from flask import Flask
        app = Flask(__name__)
    except ImportError:
        app = None                            # Flask-Teil dann übersprungen

    brain_bridge.init_bridge(
        db_conn=db_conn, flask_app=app, notify=alerts.append,
        cookie_file=cookie, recordings_dir=TMP, start_tick=False)

    brain_bridge._bridge_tick()               # eine manuelle Runde
    b = get_brain()

    # --- State korrekt gespiegelt -------------------------------------
    assert b.state.get("recorder", "alpha")["state"] == "running"
    assert b.state.get("recorder", "bravo")["state"] == "pid_dead"
    assert b.state.get("stream", "charlie")["state"] == "offline"
    assert b.state.get("restream", "restream:1")["state"] == "error"

    # --- Regeln gefeuert (beobachtend) --------------------------------
    fired = {d["rule"] for d in b.rules.decisions(50)}
    assert "recorder_pid_dead" in fired, fired
    assert "restream_unhealthy" in fired, fired
    assert "cookie_stale" in fired, fired
    assert "recordings_parallel_high" in fired, fired   # 2 ≥ Warn=2
    assert len(alerts) >= 4, alerts
    assert any("bravo" in a for a in alerts)

    # --- Cooldown: zweite Runde feuert nicht erneut --------------------
    n = len(alerts)
    brain_bridge._bridge_tick()
    assert len(alerts) == n, "Cooldown verletzt"

    # --- DB-Tier des Routers -------------------------------------------
    res = b.router.route("streamer_stats", {"user": "alpha"})
    assert res["ok"] and res["result"]["recordings"] == 5 \
        and res["result"]["live"]
    res = b.router.route("system_stats", {})
    assert res["ok"] and "telemetry" in res["result"]

    # --- Aufräumen nach Recording-Ende ---------------------------------
    with sqlite3.connect(BOT_DB) as c:
        c.execute("UPDATE trackings SET recording=0, pid=NULL "
                  "WHERE username='bravo'")
    brain_bridge._bridge_tick()
    assert b.state.get("recorder", "bravo") is None, "Geist nicht entfernt"

    # --- Flask-Routen ----------------------------------------------------
    if app:
        tc = app.test_client()
        j = tc.get("/api/brain/overview").get_json()
        assert j["rules"] and j["state"]["counts"]
        j = tc.get("/api/brain/why?limit=10").get_json()
        assert j and j[0]["rule"]
        assert tc.post("/api/brain/rules/disk_warn/toggle?on=0"
                       ).get_json()["ok"]
        assert tc.post("/api/brain/rules/nixda/toggle").status_code == 404
        j = tc.post("/api/brain/route",
                    json={"topic": "streamer_stats",
                          "payload": {"user": "alpha"}}).get_json()
        assert j["ok"] and j["tier"] == "db"

        # --- Wochenreport: der Abrufweg des Betreibers -------------------
        # WARUM als Vertrag: brain/report.weekly() haengt an genau drei
        # Aufrufern (Telegram /report, Discord /sys_report, dieser Route)
        # und der Button "REPORT 7T" in templates/brain.html zeigt auf
        # diese Route. Ohne Vertrag laesst sich _register_routes um den
        # Report kuerzen, ohne dass irgendetwas rot wird — der Button
        # lieferte dann still 404, und genau solche stillen Ausfaelle
        # sind hier schon monatelang unbemerkt geblieben.
        # Geprueft wird der Inhalt, nicht die blosse Existenz: eine Route,
        # die 200 mit leerem Rumpf liefert, waere kein Report.
        _now = time.time()
        with b._db_lock, b._conn() as _c:
            _c.execute(
                "INSERT INTO stream_sessions(username, started, ended, "
                "duration_s, recorded) VALUES(?,?,?,?,1)",
                ("reportcanary", _now - 7200, _now - 3600, 3600))
            _c.execute("INSERT INTO metrics(name, value, ts) "
                       "VALUES('cpu', 0.5, ?)", (_now - 60,))
        rv = tc.get("/api/brain/report/weekly")
        assert rv.status_code == 200, rv.status_code
        # Markdown, nicht JSON — der Browser soll den Text zeigen.
        assert "text/markdown" in rv.headers.get("Content-Type", ""), \
            rv.headers.get("Content-Type")
        md = rv.get_data(as_text=True)
        assert md.startswith("# NIGHTCRAWLER Wochenreport"), md[:80]
        # Die gesetzte Session muss aggregiert wieder herauskommen:
        # 3600s duration_s ⇒ "1h00m" aus _fmt_dur.
        assert "@reportcanary" in md, md
        assert "1h00m" in md, md
        assert "## System" in md and "Ø 50%" in md, md

    print("test_m2 OK — Sync/Regeln/Cooldown/Router-DB/Flask/Report/Cleanup grün"
          + ("" if app else " (Flask übersprungen)"))


if __name__ == "__main__":
    main()
