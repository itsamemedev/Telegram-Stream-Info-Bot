# brain_bridge.py — M2: Integration brain/ ↔ bot_v36
#
# ARCHITEKTUR-ENTSCHEIDUNG: bot_v36 importiert die Bridge, NIE umgekehrt.
# Alle bot-Referenzen (db_conn, Flask-App, Notify) werden per init_bridge()
# ÜBERGEBEN → kein Zirkularimport in den 28k-Zeilen-Monolithen, brain/
# bleibt standalone testbar.
#
# ZERO-CALL-SITE-PRINZIP: Kein Recorder-/Restream-Code wird angefasst.
# Der Systemzustand liegt bereits in der DB (trackings.recording/pid,
# restreams.status/pid) — die Bridge SPIEGELT ihn per Poll in die
# StateMachine. Vorteil: 0 Risiko für die Aufnahme-Pipeline. Nachteil:
# Latenz = Tick-Intervall (10s) — für Beobachtungsregeln völlig ok.
# Event-genaue Meldungen direkt aus dem Recorder kommen in M5.
#
# M2-REGELN BEOBACHTEN NUR: Aktionen (Kill, Cleanup, Restart) bleiben
# bei den bewährten Loops (reaper, disk_guard, watchdog). Zwei Akteure
# am selben Prozess = Race Conditions. Die Regeln liefern das ZENTRALE
# Entscheidungs-/Alarmlog; Aktions-Übernahme erfolgt in M5 pro Regel
# einzeln, nachdem das Log Vertrauen geschaffen hat.

from __future__ import annotations

import logging
import os
import shutil
import time
from typing import Callable, Optional

from brain import get_brain
from nc.envnum import clamp_float, env_float, env_int  # v4.0-W78: leer-gesetzte .env-Werte robust

log = logging.getLogger("brain.bridge")

# ---------------------------------------------------------------- Konfig
# Alle Schwellen env-steuerbar; Defaults konservativ für ns3068954 (8 Cores).
# v4.0-W78: env_float statt float(os.getenv(...)) — eine in der .env GESETZTE,
# aber LEERE Variable (name=) lieferte sonst "" und float("") warf beim IMPORT
# 'could not convert string to float: ''. Genau daran ist die ganze Brain-Bridge
# gestorben (TICK ✗, 0 Regeln, /api/brain/* 404). Jetzt: leer → Default.
DISK_WARN_PCT   = env_float("BRAIN_DISK_WARN_PCT", 85)
DISK_CRIT_PCT   = env_float("BRAIN_DISK_CRIT_PCT", 92)
LOAD_WARN_RATIO = env_float("BRAIN_LOAD_WARN_RATIO", 1.5)
RAM_WARN_PCT    = env_float("BRAIN_RAM_WARN_PCT", 10)   # frei < 10%
COOKIE_MAX_D    = env_float("BRAIN_COOKIE_MAX_AGE_D", 7)
REC_PARALLEL_WARN = env_int("BRAIN_REC_PARALLEL_WARN", 6)
BRAIN_DB_MAX_MB = env_float("BRAIN_DB_MAX_MB", 200)
TICK_S          = env_float("BRAIN_TICK_S", 10)
# M3: Metriken nicht pro Tick (10s → 8.6k Zeilen/Tag/Metrik) sondern
# im 60s-Raster — reicht für Trends/Prognosen, hält brain.db klein.
METRIC_EVERY_S  = env_float("BRAIN_METRIC_EVERY_S", 60)
_last_metric_ts = 0.0
# M4: Graph-Neuableitung aus Memory. 15min ist bewusst träge — die
# Faktenbasis (Sessions über 30 Tage) ändert sich langsam; häufiger
# rechnen wäre nur CPU-Verschwendung.
KG_REFRESH_S    = env_float("BRAIN_KG_REFRESH_S", 900)
_last_kg_ts     = 0.0
# M5: Planungslauf (Hints neu berechnen). 5min: Wahrscheinlichkeiten
# ändern sich mit der Tagesstunde, nicht sekündlich.
SCHED_EVERY_S   = env_float("BRAIN_SCHED_EVERY_S", 300)
_last_sched_ts  = 0.0


def _act_enabled(rule_name: str) -> bool:
    """M5-Aktions-Gate: Regel darf nur HANDELN (statt nur melden), wenn
    der Operator sie einzeln freischaltet: BRAIN_ACT_<RULE>=1.
    Default IMMER aus — Autonomie wird pro Regel verdient, nachdem das
    Entscheidungslog gezeigt hat, dass die Regel richtig liegt."""
    return os.getenv(f"BRAIN_ACT_{rule_name.upper()}", "0") in ("1", "true")

_ctx: dict = {}          # von init_bridge gesetzt: db_conn, notify, pfade


# ---------------------------------------------------------------- Telemetrie
# WARUM stdlib statt psutil: bot_v36 vermeidet psutil bewusst (F19) —
# gleiche Linie hier. /proc + shutil reichen für alle M2-Regeln.

def _telemetry() -> dict:
    t: dict = {"ts": time.time()}
    try:
        cores = os.cpu_count() or 1
        la1, la5, la15 = os.getloadavg()
        t["load"] = {"1": la1, "5": la5, "15": la15,
                     "cores": cores, "ratio15": la15 / cores}
    except Exception:
        pass
    try:
        mem = {}
        with open("/proc/meminfo") as f:
            for line in f:
                k, v = line.split(":", 1)
                mem[k] = int(v.strip().split()[0])       # kB
        total = mem.get("MemTotal", 0)
        avail = mem.get("MemAvailable", 0)
        if total:
            t["ram"] = {"total_mb": total // 1024, "avail_mb": avail // 1024,
                        "avail_pct": round(avail / total * 100, 1)}
    except Exception:
        pass
    try:
        rec_dir = _ctx.get("recordings_dir") or "recordings"
        # recordings-Dir kann auf anderem Mount liegen als / → beide messen,
        # die Regel nimmt das Maximum (der vollste Mount ist das Problem).
        paths = {"/": "/"}
        if os.path.isdir(rec_dir):
            paths["recordings"] = rec_dir
        disks = {}
        for name, p in paths.items():
            du = shutil.disk_usage(p)
            disks[name] = {"used_pct": round(du.used / du.total * 100, 1),
                           "free_gb": round(du.free / 2**30, 1)}
        t["disk"] = disks
        t["disk_max_pct"] = max(d["used_pct"] for d in disks.values())
    except Exception:
        pass
    return t


def _pid_alive(pid) -> bool:
    if not pid:
        return False
    try:
        os.kill(int(pid), 0)
        return True
    except (ProcessLookupError, ValueError, TypeError):
        return False
    except PermissionError:
        return True     # existiert, gehört anderem User


# ---------------------------------------------------------------- DB-Sync

def _sync_db_state() -> None:
    """trackings + restreams → StateMachine spiegeln.

    WARUM remove() für Verschwundenes: sonst sammeln sich 'gone'-Geister
    an und snapshot() wird über Wochen immer größer (24/7!)."""
    db_conn = _ctx.get("db_conn")
    if not db_conn:
        return
    brain = get_brain()
    try:
        with db_conn() as conn:
            recs = conn.execute(
                "SELECT username, recording, pid, last_live, paused "
                "FROM trackings").fetchall()
            rests = conn.execute(
                "SELECT id, label, status, pid, source_username, started_at "
                "FROM restreams WHERE enabled=1").fetchall()
    except Exception as e:
        # IMP-6: WARNING mit Drossel statt debug — ein dauerhaft kaputter
        # Sync (z.B. Schema-Drift nach Bot-Update) hieße "Brain für immer
        # leer" und wäre auf debug-Level nie aufgefallen.
        now = time.time()
        if now - _ctx.get("_sync_warn_ts", 0) > 600:
            _ctx["_sync_warn_ts"] = now
            log.warning("Brain-DB-Sync fehlgeschlagen (Schema-Drift?): %s", e)
        return

    seen_rec, seen_stream, seen_rest = set(), set(), set()
    for r in recs:
        u = r["username"]
        seen_stream.add(u)
        brain.state.set("stream", u,
                        "online" if r["last_live"] else "offline",
                        paused=bool(r["paused"]))
        if r["recording"]:
            seen_rec.add(u)
            alive = _pid_alive(r["pid"])
            brain.state.set("recorder", u,
                            "running" if alive else "pid_dead",
                            pid=r["pid"])
    for rs in rests:
        key = f"restream:{rs['id']}"
        seen_rest.add(key)
        st = rs["status"] or "idle"
        # BH3-Fix (Literal seit M2 falsch): Der Restream-Manager schreibt
        # "live" als Laufstatus, nicht "running" — die pid_dead-Promotion
        # war daher UNERREICHBAR und restream_unhealthy konnte tote
        # Prozesse nie melden. Nur MIT gesetztem PID prüfen: "starting"
        # hat legitim noch keinen (Resolve-Phase) → wäre sonst Fehlalarm
        # bei jedem Start.
        if st in ("live", "running") and rs["pid"] and not _pid_alive(rs["pid"]):
            st = "pid_dead"
        brain.state.set("restream", key, st,
                        label=rs["label"], source=rs["source_username"],
                        pid=rs["pid"], started_at=rs["started_at"])

    # Aufräumen: Entitäten, die die DB nicht mehr führt. BH-1: Restreams
    # fehlten hier — gelöschte/disabled Restreams blieben als Geister im
    # State und hielten restream_unhealthy/RecoveryAgent dauerhaft am Feuern.
    for e in brain.state.query("recorder"):
        if e["key"] not in seen_rec:
            brain.state.remove("recorder", e["key"])
    for e in brain.state.query("stream"):
        if e["key"] not in seen_stream:
            brain.state.remove("stream", e["key"])
    for e in brain.state.query("restream"):
        if e["key"] not in seen_rest:
            brain.state.remove("restream", e["key"])


# ---------------------------------------------------------------- Notify
# Aktionen der M2-Regeln = Melden. _notify puffert dedupe-frei dank
# Rule-Cooldowns; Kanal liefert bot_v36 (Telegram) oder Fallback-Log.

def _notify(text: str) -> str:
    fn: Optional[Callable] = _ctx.get("notify")
    if fn:
        try:
            fn(text)
            return "notified"
        except Exception as e:
            log.warning("Brain-Notify fehlgeschlagen: %s", e)
            return f"notify_failed: {e}"
    log.warning("BRAIN: %s", text)
    return "logged"


# ---------------------------------------------------------------- Regeln

def _register_rules() -> None:
    b = get_brain()
    R = b.rules.register

    # --- Quellen-Gesundheit (V37-B91d) ------------------------------
    # Feuert, wenn eine Quelle X-mal in Folge beim Preflight komplett tot
    # war (alle URL-Varianten 404). Das ist ein starker Hinweis, dass der
    # Account offline ist / nicht mehr existiert / dauerhaft Battle-Stage —
    # Kandidat zum Untracken. Cooldown lang, damit es nicht nervt.
    _DEAD_STREAK_MIN = env_int("BRAIN_DEAD_STREAK_ALERT", 8)

    def _dead_source_reason(c):
        cb = _ctx.get("preflight_dead_streak")
        if not callable(cb):
            return None
        streaks = cb() or {}
        hot = [(w, n) for w, n in streaks.items() if n >= _DEAD_STREAK_MIN]
        if not hot:
            return None
        hot.sort(key=lambda x: -x[1])
        w, n = hot[0]
        return f"{w}: {n}× in Folge tot (alle URL-Varianten 404)"

    R("source_chronically_dead",
      _dead_source_reason,
      lambda c: _notify("💀 Quelle chronisch tot — " + _dead_source_reason(c)
                        + ". Vermutlich offline/gelöscht — Untracken erwägen."),
      cooldown_s=21600, priority=15, tags=("source", "preflight"))

    # --- Ressourcen -------------------------------------------------
    R("disk_critical",
      lambda c: (f"Disk {c['disk_max_pct']}% ≥ {DISK_CRIT_PCT}% "
                 f"({c.get('disk')})"
                 if c.get("disk_max_pct", 0) >= DISK_CRIT_PCT else None),
      lambda c: _notify(f"🔴 DISK KRITISCH: {c['disk_max_pct']}% belegt — "
                        f"disk_guard sollte eingreifen, prüfen!"),
      cooldown_s=1800, priority=5, tags=("resource", "disk"))

    R("disk_warn",
      lambda c: (f"Disk {c['disk_max_pct']}% ≥ {DISK_WARN_PCT}%"
                 if DISK_WARN_PCT <= c.get("disk_max_pct", 0) < DISK_CRIT_PCT
                 else None),
      lambda c: _notify(f"🟡 Disk-Warnung: {c['disk_max_pct']}% belegt"),
      cooldown_s=7200, priority=20, tags=("resource", "disk"))

    R("cpu_load_high",
      lambda c: (f"load15={c['load']['15']:.1f} bei {c['load']['cores']} "
                 f"Cores (ratio {c['load']['ratio15']:.2f} ≥ {LOAD_WARN_RATIO})"
                 if c.get("load", {}).get("ratio15", 0) >= LOAD_WARN_RATIO
                 else None),
      lambda c: _notify(f"🟡 CPU-Dauerlast: load15 {c['load']['15']:.1f} "
                        f"auf {c['load']['cores']} Cores"),
      cooldown_s=1800, priority=10, tags=("resource", "cpu"))

    R("ram_low",
      lambda c: (f"RAM frei {c['ram']['avail_pct']}% < {RAM_WARN_PCT}%"
                 if c.get("ram", {}).get("avail_pct", 100) < RAM_WARN_PCT
                 else None),
      lambda c: _notify(f"🔴 RAM knapp: {c['ram']['avail_mb']}MB frei "
                        f"({c['ram']['avail_pct']}%)"),
      cooldown_s=1800, priority=8, tags=("resource", "ram"))

    # --- Recording/Restream-Gesundheit -------------------------------
    def cond_pid_dead(c):
        dead = [e["key"] for e in c["state"]["entities"]
                if e["kind"] == "recorder" and e["state"] == "pid_dead"]
        return {"pid_dead": dead,
                "hinweis": "recording=1 aber Prozess weg — Reaper "
                           "sollte in ≤60s aufräumen"} if dead else None

    R("recorder_pid_dead", cond_pid_dead,
      lambda c: _notify("🟡 Recorder-PID tot (Reaper beobachten): "
                        + ", ".join(e["key"] for e in c["state"]["entities"]
                                    if e["kind"] == "recorder"
                                    and e["state"] == "pid_dead")),
      cooldown_s=300, priority=15, tags=("watchdog", "recorder"))

    def cond_restream_err(c):
        bad = [e for e in c["state"]["entities"]
               if e["kind"] == "restream"
               and e["state"] in ("error", "pid_dead")]
        return {"restreams": [(e["key"], e["state"],
                               e["attrs"].get("label")) for e in bad]} \
            if bad else None

    R("restream_unhealthy", cond_restream_err,
      lambda c: _notify("🔴 Restream unhealthy: " + ", ".join(
          f"{e['attrs'].get('label') or e['key']}={e['state']}"
          for e in c["state"]["entities"]
          if e["kind"] == "restream" and e["state"] in ("error", "pid_dead"))),
      cooldown_s=600, priority=7, tags=("watchdog", "restream"))

    def cond_many_recs(c):
        n = len([e for e in c["state"]["entities"]
                 if e["kind"] == "recorder" and e["state"] == "running"])
        return (f"{n} parallele Recordings ≥ {REC_PARALLEL_WARN} "
                f"(CPU-Budget 8 Cores)") if n >= REC_PARALLEL_WARN else None

    R("recordings_parallel_high", cond_many_recs,
      lambda c: _notify("🟡 Viele parallele Recordings — CPU/Disk im Auge "
                        "behalten"),
      cooldown_s=1800, priority=25, tags=("resource", "recorder"))

    # --- Infrastruktur ------------------------------------------------
    def cond_cookie(c):
        f = _ctx.get("cookie_file")
        if not f or not os.path.exists(f):
            return None     # Fehlen meldet bot_v36 beim Start selbst (F37)
        age_d = (time.time() - os.path.getmtime(f)) / 86400
        return (f"Cookie-Datei {age_d:.1f}d alt ≥ {COOKIE_MAX_D}d — "
                f"TikTok-Auth-Risiko") if age_d >= COOKIE_MAX_D else None

    R("cookie_stale", cond_cookie,
      lambda c: _notify("🟡 TikTok-Cookies veraltet — Refresh prüfen"),
      cooldown_s=43200, priority=30, tags=("infra", "cookies"))

    def cond_brain_db(c):
        try:
            mb = os.path.getsize(get_brain()._db_path) / 2**20
        except OSError:
            return None
        return (f"brain.db {mb:.0f}MB > {BRAIN_DB_MAX_MB}MB — Retention "
                f"prüfen (BRAIN_RETAIN_DAYS)") if mb > BRAIN_DB_MAX_MB else None

    def _act_brain_db(c):
        # M5: erste echte Aktion — Selbstwartung. Konfliktfrei per
        # Definition: betrifft NUR brain.db, keinen bot_v36-Prozess.
        if not _act_enabled("brain_db_big"):
            return _notify("🟡 brain.db wächst — Retention greift nicht? "
                           "(Auto-Fix: BRAIN_ACT_BRAIN_DB_BIG=1)")
        b = get_brain()
        b.memory.gc(env_int("BRAIN_RETAIN_DAYS", 14))
        try:
            with b._db_lock, b._conn() as conn:
                conn.execute("VACUUM")
            mb = os.path.getsize(b._db_path) / 2**20
            return _notify(f"🔧 brain.db Selbstwartung: GC+VACUUM "
                           f"ausgeführt, jetzt {mb:.0f}MB")
        except Exception as e:
            return _notify(f"🔴 brain.db Selbstwartung fehlgeschlagen: {e}")

    R("brain_db_big", cond_brain_db, _act_brain_db,
      cooldown_s=86400, priority=90, tags=("infra", "brain", "selfheal"))

    def cond_all_offline(c):
        streams = [e for e in c["state"]["entities"] if e["kind"] == "stream"]
        # Nur sinnvoll, wenn überhaupt Trackings existieren und ALLE seit
        # >30min offline sind UND vorher mind. 1 online war (Historie).
        if not streams or any(e["state"] == "online" for e in streams):
            return None
        recent_online = any(
            h["kind"] == "stream" and h["old"] == "online"
            and time.time() - h["ts"] < 7200
            for h in c.get("history", []))
        oldest = min(time.time() - e["since"] for e in streams)
        if recent_online and oldest > 1800:
            return (f"Alle {len(streams)} Streams seit >30min offline, "
                    f"vor <2h war noch was online — Detection-Ausfall? "
                    f"(Cookies/Proxy/WAF)")
        return None

    R("all_streams_dark", cond_all_offline,
      lambda c: _notify("🔴 Alle Streams plötzlich offline — Live-Detection "
                        "prüfen (Cookies/Proxy)"),
      cooldown_s=3600, priority=12, tags=("watchdog", "detection"))


# ---------------------------------------------------------------- Router-Handler (Tier: db)

def _register_db_handlers() -> None:
    from brain import Unhandled
    b = get_brain()
    db_conn = _ctx.get("db_conn")

    def streamer_stats(task):
        user = task.payload.get("user")
        if not user or not db_conn:
            raise Unhandled("kein user/db")
        with db_conn() as conn:
            row = conn.execute(
                "SELECT COUNT(*) AS n FROM recordings WHERE username=?",
                (user,)).fetchone()
            live = conn.execute(
                "SELECT last_live, paused FROM trackings WHERE username=? "
                "LIMIT 1", (user,)).fetchone()
        return {"user": user, "recordings": row["n"] if row else 0,
                "live": bool(live and live["last_live"]),
                "paused": bool(live and live["paused"])}

    def system_stats(task):
        return {"telemetry": _telemetry(),
                "state_counts": get_brain().state.snapshot()["counts"]}

    def streamer_profile(task):
        user = task.payload.get("user")
        if not user:
            raise Unhandled("kein user")
        prof = get_brain().memory.streamer_profile(
            user, days=int(task.payload.get("days", 30)))
        if not prof.get("sessions"):
            raise Unhandled("keine Sessions im Memory")   # → nächster Tier
        return prof

    b.router.register("db", "streamer_stats", streamer_stats)
    b.router.register("db", "system_stats", system_stats)
    # M3: Profile liegen VOR der bot-DB im 'rules'-Tier? Nein — es sind
    # Faktenabfragen, also Tier 'db'. Memory zuerst probieren wäre falsch
    # herum: streamer_stats (bot-DB) und streamer_profile (Memory) sind
    # verschiedene Topics, keine Kaskade nötig.
    b.router.register("db", "streamer_profile", streamer_profile)

    # --- M4: Tier 'knowledge' wird aktiv ------------------------------
    def kg_recommend(task):
        recs = get_brain().knowledge.recommend(
            hour_utc=task.payload.get("hour_utc"),
            top=int(task.payload.get("top", 10)))
        if not recs:
            raise Unhandled("Graph leer — noch keine abgeleiteten Fakten")
        return recs

    def kg_facts(task):
        facts = get_brain().knowledge.query(
            s=task.payload.get("s"), p=task.payload.get("p"),
            o=task.payload.get("o"))
        if not facts:
            raise Unhandled("keine passenden Fakten")
        return facts

    def kg_who_at(task):
        h = task.payload.get("hour_utc")
        if h is None:
            raise Unhandled("hour_utc fehlt")
        who = get_brain().knowledge.who_streams_at(int(h))
        if not who:
            raise Unhandled(f"niemand für Stunde {h} bekannt")
        return who

    b.router.register("knowledge", "recommendation", kg_recommend)
    b.router.register("knowledge", "streamer_facts", kg_facts)
    b.router.register("knowledge", "who_streams_at", kg_who_at)

    # --- M5: Prognose-Topics (gelernt → Tier knowledge) ----------------
    def go_live(task):
        user = task.payload.get("user")
        if not user:
            raise Unhandled("user fehlt")
        h = task.payload.get("hour_utc")
        h = int(h) if h is not None else time.gmtime().tm_hour
        p = get_brain().scheduler.go_live_prob(get_brain().memory, user, h)
        if p["basis"] == "keine Sessions":
            raise Unhandled(f"keine Historie für {user}")
        return p

    def cpu_fc(task):
        fc = get_brain().scheduler.cpu_forecast(
            get_brain().memory,
            horizon_h=int(task.payload.get("horizon_h", 6)))
        if all(x["load_ratio_avg"] is None for x in fc):
            raise Unhandled("keine Metrik-Historie")
        return fc

    b.router.register("knowledge", "go_live_prediction", go_live)
    b.router.register("knowledge", "cpu_forecast", cpu_fc)

    # --- M6: Tier 'llm' wird aktiv — die LETZTE Instanz ------------------
    from brain import BudgetExhausted

    def _llm_guarded(messages, max_tokens=None):
        """Budget/Busy → Unhandled: der Router soll ehrlich 'kein Tier
        konnte' melden statt auf einen Slot zu warten."""
        try:
            res = get_brain().llm.chat(messages, max_tokens=max_tokens)
        except BudgetExhausted as e:
            raise Unhandled(str(e)) from None
        if not res["ok"]:
            raise Unhandled(f"LLM nicht erreichbar: {res['error']}")
        return res

    def llm_ask(task):
        # B120: Schluessel-Toleranz. bot.brain_cmd schickte
        # {"question": ...}, dieser Handler las nur "prompt" -> er warf
        # IMMER Unhandled, der Router meldete "kein Tier konnte den Task
        # loesen" und /brain antwortete strukturell "keine Antwort".
        # Die Flask-Route (/api/brain/ask) nutzt "prompt", deshalb lief
        # die Dashboard-KI weiter und der Bruch blieb unbemerkt.
        # Beide Namen werden jetzt akzeptiert.
        payload = task.payload or {}
        prompt = (payload.get("prompt") or payload.get("question")
                  or payload.get("q") or payload.get("text"))
        if not prompt:
            raise Unhandled("kein prompt")
        sysmsg = ("Du bist AZRAEL, das Brain von NIGHTCRAWLER (TikTok-"
                  "Live-Recording/Restream-System). Antworte knapp, "
                  "deutsch, technisch präzise.")
        return _llm_guarded([{"role": "system", "content": sysmsg},
                             {"role": "user", "content": prompt}])

    def llm_explain(task):
        # Showcase des v37-'Warum?': Entscheidungslog → natürliche Sprache.
        # Tiers 1-3 können Fakten liefern, aber keine Prosa — legitimer
        # Tier-4-Fall.
        decisions = get_brain().why(limit=int(task.payload.get("limit", 8)))
        if not decisions:
            raise Unhandled("keine Entscheidungen im Log")
        lines = "\n".join(
            f"- {time.strftime('%H:%M', time.gmtime(d['ts']))} UTC "
            f"[{d['rule']}] Grund: {d['reason']} → {d['result']}"
            for d in decisions)
        return _llm_guarded(
            [{"role": "system",
              "content": "Fasse Systementscheidungen für den Operator "
                         "zusammen. Deutsch, max. 5 Sätze, keine Floskeln."},
             {"role": "user",
              "content": f"Letzte Entscheidungen des Systems:\n{lines}\n\n"
                         f"Was ist passiert und muss ich etwas tun?"}],
            max_tokens=300)

    b.router.register("llm", "ask", llm_ask)
    b.router.register("llm", "explain_decisions", llm_explain)
    # Catch-all NUR wenn explizit erlaubt: unbekannte Topics dürfen
    # nicht standardmäßig Budget verbrennen.
    if os.getenv("BRAIN_LLM_CATCHALL", "0") in ("1", "true"):
        b.router.register("llm", "*", llm_ask)


# ---------------------------------------------------------------- Flask

def _register_routes(app) -> None:
    """VOR dem Flask-Thread-Start aufrufen (Routen nach Serve = Fehler).
    Auth: erbt die app-weiten before_request-Guards von bot_v36."""
    from flask import jsonify, request
    b = get_brain()

    @app.route("/api/brain/overview")
    def brain_overview():
        return jsonify(b.overview())

    @app.route("/api/brain/why")
    def brain_why():
        return jsonify(b.why(limit=int(request.args.get("limit", 50))))

    @app.route("/api/brain/rules")
    def brain_rules():
        return jsonify(b.rules.rules_status())

    @app.route("/api/brain/rules/<name>/toggle", methods=["POST"])
    def brain_rule_toggle(name):
        on = request.args.get("on", "1") not in ("0", "false")
        ok = b.rules.enable(name, on)
        return jsonify({"ok": ok, "rule": name, "enabled": on}), \
            200 if ok else 404

    @app.route("/api/brain/route", methods=["POST"])
    def brain_route():
        j = request.get_json(silent=True) or {}
        topic = j.get("topic")
        if not topic:
            return jsonify({"ok": False, "error": "topic fehlt"}), 400
        return jsonify(b.router.route(topic, j.get("payload")))

    # --- M3: Memory-Sichten ------------------------------------------
    @app.route("/api/brain/memory/profile")
    def brain_mem_profile():
        user = request.args.get("user", "")
        if not user:
            return jsonify({"ok": False, "error": "user fehlt"}), 400
        return jsonify(b.memory.streamer_profile(
            user, days=int(request.args.get("days", 30))))

    @app.route("/api/brain/memory/metrics")
    def brain_mem_metrics():
        name = request.args.get("name")
        if not name:
            return jsonify({"names": b.memory.metric_names()})
        return jsonify(b.memory.metric_series(
            name, hours=clamp_float(request.args.get("hours"), 24, 0.1, 8760),
            buckets=int(request.args.get("buckets", 120))))

    @app.route("/api/brain/memory/sessions")
    def brain_mem_sessions():
        return jsonify(b.memory.sessions(
            user=request.args.get("user"),
            limit=int(request.args.get("limit", 50))))

    # --- M4: Knowledge-Graph-Sichten -----------------------------------
    @app.route("/api/brain/knowledge/facts")
    def brain_kg_facts():
        return jsonify(b.knowledge.query(
            s=request.args.get("s"), p=request.args.get("p"),
            o=request.args.get("o"),
            limit=int(request.args.get("limit", 200))))

    @app.route("/api/brain/knowledge/recommend")
    def brain_kg_recommend():
        h = request.args.get("hour_utc")
        return jsonify(b.knowledge.recommend(
            hour_utc=int(h) if h is not None else None,
            top=int(request.args.get("top", 10))))

    @app.route("/api/brain/knowledge/graph")
    def brain_kg_graph():
        return jsonify(b.knowledge.graph_export(
            limit=int(request.args.get("limit", 500))))

    @app.route("/api/brain/knowledge/refresh", methods=["POST"])
    def brain_kg_refresh():
        n = b.knowledge.refresh(b.memory)
        return jsonify({"ok": True, "facts": n,
                        "stats": b.knowledge.stats()})

    # --- M5: Scheduler-Sichten ------------------------------------------
    @app.route("/api/brain/schedule/hints")
    def brain_sched_hints():
        return jsonify(b.scheduler.hints(user=request.args.get("user")))

    @app.route("/api/brain/schedule/upcoming")
    def brain_sched_upcoming():
        return jsonify(b.scheduler.upcoming(
            b.memory,
            horizon_h=int(request.args.get("hours", 6)),
            threshold=clamp_float(request.args.get("threshold"), 0.15, 0, 1)))

    @app.route("/api/brain/schedule/cpu")
    def brain_sched_cpu():
        return jsonify(b.scheduler.cpu_forecast(
            b.memory, horizon_h=int(request.args.get("hours", 6))))

    @app.route("/api/brain/schedule/plan", methods=["POST"])
    def brain_sched_plan():
        return jsonify(b.scheduler.plan(b.memory))

    # --- M6: LLM-Runtime-Sichten -----------------------------------------
    @app.route("/api/brain/llm/health")
    def brain_llm_health():
        return jsonify(b.llm.health())

    @app.route("/api/brain/llm/stats")
    def brain_llm_stats():
        return jsonify(b.llm.stats())

    @app.route("/api/brain/llm/ask", methods=["POST"])
    def brain_llm_ask():
        j = request.get_json(silent=True) or {}
        prompt = j.get("prompt")
        if not prompt:
            return jsonify({"ok": False, "error": "prompt fehlt"}), 400
        # Über den Router, nicht direkt: Budget/Trace/Log inklusive.
        return jsonify(b.router.route("ask", {"prompt": prompt}))

    @app.route("/api/brain/llm/explain", methods=["POST"])
    def brain_llm_explain():
        return jsonify(b.router.route("explain_decisions", {}))

    # --- M7: Agenten-Sichten ----------------------------------------------
    @app.route("/api/brain/agents")
    def brain_agents():
        return jsonify(b.agents.status())

    @app.route("/api/brain/agents/<name>/toggle", methods=["POST"])
    def brain_agent_toggle(name):
        on = request.args.get("on", "1") not in ("0", "false")
        ok = b.agents.enable(name, on)
        return jsonify({"ok": ok, "agent": name, "enabled": on}), \
            200 if ok else 404

    @app.route("/api/brain/agents/<name>/run", methods=["POST"])
    def brain_agent_run(name):
        findings = b.agents.run_one(name, {"trigger": "manual"})
        return jsonify({"ok": True, "agent": name, "findings": findings})

    @app.route("/api/brain/agents/findings")
    def brain_agent_findings():
        return jsonify(b.memory.events(
            kind="agent_finding",
            limit=int(request.args.get("limit", 50))))

    @app.route("/api/brain/report/weekly")
    def brain_report_weekly():
        from brain import report as _report
        md = _report.weekly(get_brain())
        return md, 200, {"Content-Type": "text/markdown; charset=utf-8"}

    @app.route("/api/brain/semantic/search")
    def brain_sem_search():
        q = (request.args.get("q") or "").strip()
        if not q:
            return jsonify(ok=False, error="q fehlt"), 400
        return jsonify(get_brain().semantic.search(
            q, k=int(request.args.get("k", 5)),
            username=request.args.get("user")))

    @app.route("/api/brain/semantic/stats")
    def brain_sem_stats():
        return jsonify(get_brain().semantic.stats())

    # --- M8: Brain-Dashboard-Seite --------------------------------------
    @app.route("/brain")
    def brain_page():
        """Eigenständige Seite, zusätzlich als Tab 06 im Haupt-Dashboard
        eingebettet (iframe). Suchreihenfolge folgt der Flask-Konvention
        des Bots (templates/): 1) BRAIN_DASHBOARD_HTML (env),
        2) templates/brain.html, 3) brain_dashboard.html (Fallback).
        Bewusst raw ausgeliefert statt render_template: die Seite enthält
        kein Jinja, und raw kann nicht an Jinja-Tokens in JS scheitern."""
        candidates = [os.getenv("BRAIN_DASHBOARD_HTML", ""),
                      os.path.join("templates", "brain.html"),
                      "brain_dashboard.html"]
        for path in candidates:
            if not path:
                continue
            try:
                with open(path, encoding="utf-8") as f:
                    return f.read(), 200, {"Content-Type":
                                           "text/html; charset=utf-8"}
            except OSError:
                continue
        return ("templates/brain.html fehlt — Datei dorthin legen oder "
                "BRAIN_DASHBOARD_HTML setzen."), 404


# ---------------------------------------------------------------- Tick

def _record_metrics(telemetry: dict) -> None:
    """M3: Betriebsmetriken ins Memory — Datengrundlage für CPU-Prognose
    (M5) und Dashboard-Charts (M8)."""
    global _last_metric_ts
    now = time.time()
    if now - _last_metric_ts < METRIC_EVERY_S:
        return
    _last_metric_ts = now
    b = get_brain()
    counts = b.state.snapshot()["counts"]
    rest_counts = counts.get("restream", {})
    vals = {
        "recorders_running": counts.get("recorder", {}).get("running", 0),
        "streams_online": counts.get("stream", {}).get("online", 0),
        # BH3-Fix: Laufstatus der Restreams heißt "live" — der alte Zugriff
        # auf "running" lieferte konstant 0 in die Zeitreihe.
        "restreams_running": (rest_counts.get("live", 0)
                              + rest_counts.get("running", 0)
                              + rest_counts.get("starting", 0)),
    }
    # V37: Listener-Reconnects (kumulativ seit Bot-Start) als Zeitreihe —
    # ein chronisch instabiler Kanal fällt so auch im Wochenreport auf.
    try:
        wcb = _ctx.get("wchat_status")
        if callable(wcb):
            st = wcb() or {}
            rc = sum(int((v or {}).get("reconnects", 0)) for v in st.values())
            vals["listener_reconnects"] = rc
    except Exception:
        pass
    # V37-B91c: Preflight-Zähler (CDN-404-Quirk-Telemetrie) als Zeitreihen.
    try:
        pcb = _ctx.get("preflight_stats")
        if callable(pcb):
            ps = pcb() or {}
            for k in ("ok", "fallback", "dead"):
                if k in ps:
                    vals[f"preflight_{k}"] = int(ps[k])
    except Exception:
        pass
    # V37: LLM-Latenz als Zeitreihe (nur wenn schon Calls liefen) — macht
    # den llama.cpp-Umstieg im Metrik-Panel messbar (vorher/nachher).
    try:
        _ams = b.llm.stats().get("avg_ms")
        if _ams:
            vals["llm_avg_ms"] = _ams
    except Exception:
        pass
    if "load" in telemetry:
        vals["load_ratio15"] = telemetry["load"]["ratio15"]
        vals["load1"] = telemetry["load"]["1"]
    if "ram" in telemetry:
        vals["ram_avail_pct"] = telemetry["ram"]["avail_pct"]
    if "disk_max_pct" in telemetry:
        vals["disk_max_pct"] = telemetry["disk_max_pct"]
    b.memory.record_metrics(vals, ts=now)


def _register_agents() -> None:
    """M7: AZRAEL-Betriebsflotte. Recovery bekommt bot-DB + Aktions-Gate;
    der Rest arbeitet rein auf Brain-Daten."""
    from brain import (AnalyticsAgent, DiskAgent, HealthAgent, LearningAgent,
                       ProxyHealthAgent,
                       RecordingAgent, RecoveryAgent, RestreamSentinelAgent,
                       ScoutAgent, SentinelAgent, SwapAgent, ToxicityAgent, UptimeAgent)
    b = get_brain()
    b.agents._notify = _ctx.get("agent_notify") or _notify
    b.agents.register(HealthAgent(b))
    b.agents.register(RecoveryAgent(b, db_conn=_ctx.get("db_conn"),
                                    act_check=_act_enabled))
    b.agents.register(ScoutAgent(b))
    b.agents.register(AnalyticsAgent(b))
    b.agents.register(LearningAgent(b))
    # M8: AZRAEL-Sentinel-Flotte (reine Waechter, injizierte Accessoren)
    b.agents.register(SentinelAgent(b, crowdsec=_ctx.get("crowdsec")))
    b.agents.register(DiskAgent(b, recordings_dir=_ctx.get("recordings_dir",
                                                           "recordings")))
    b.agents.register(RestreamSentinelAgent(
        b, restream_health=_ctx.get("restream_health")))
    b.agents.register(ToxicityAgent(b, moderation=_ctx.get("moderation")))
    b.agents.register(UptimeAgent(b, wchat_status=_ctx.get("wchat_status")))
    b.agents.register(RecordingAgent(
        b, recording_health=_ctx.get("recording_health")))
    b.agents.register(ProxyHealthAgent(
        b, tiktok_status=_ctx.get("tiktok_status")))
    # v4.0-W86: Swap-Wächter (13.) — hält den Swap sauber, mit OOM-Schutz.
    b.agents.register(SwapAgent(b))


_last_sem_ts = 0.0
_briefing_day = [""]


def _daily_briefing():
    """V37: Einmal pro Tag (erster Tick nach Mitternacht UTC) eine kompakte
    Lagemeldung ins Decision-Log — Dashboard-Warum-Feed und /brain zeigen
    sie. Bewusst als 'Regel-Feuerung' verbucht: gleiche Pipeline, GC,
    Sichtbarkeit — kein neuer Kanal."""
    import datetime as _dt
    today = _dt.datetime.now(_dt.timezone.utc).strftime("%Y-%m-%d")
    if _briefing_day[0] == today:
        return
    _briefing_day[0] = today
    b = get_brain()
    try:
        since = time.time() - 86400
        with b._db_lock, b._conn() as c:
            n_sess, dur = c.execute(
                "SELECT COUNT(*), COALESCE(SUM(duration_s),0) FROM stream_sessions "
                "WHERE started >= ? AND ended IS NOT NULL", (since,)).fetchone()
            n_dec = c.execute("SELECT COUNT(*) FROM decisions WHERE ts >= ?",
                              (since,)).fetchone()[0]
        counts = {}
        for e in b.state.query("restream"):
            counts[e["state"]] = counts.get(e["state"], 0) + 1
        up = []
        try:
            up = b.scheduler.upcoming(b.memory, horizon_h=8, threshold=0.3)[:2]
        except Exception:
            pass
        nxt = ", ".join(f"@{u['user']} ~{u['in_hours']}h ({u['prob']:.0%})"
                        for u in up) or "keine Prognose ≥30%"
        b.rules._log_decision(
            type("R", (), {"name": "daily_briefing", "priority": 99,
                           "tags": ("briefing",)})(),
            f"Tagesbriefing {today}",
            f"24h: {n_sess} Sessions ({int(dur) // 3600}h beobachtet) · "
            f"{n_dec} Entscheidungen · Restreams: "
            f"{', '.join(f'{k}={v}' for k, v in counts.items()) or 'keine'} · "
            f"Als Nächstes live: {nxt}",
            {"trigger": "briefing"})
    except Exception as e:
        log.debug("Tagesbriefing übersprungen: %s", e)


def _ingest_stream_memories():
    """V37-W-PLUS: neue stream_memories-Zeilen (Whisper-Zusammenfassungen
    des Bots) ins semantische Gedächtnis. Cursor-basiert, max. 20 pro
    Runde (Embedding = CPU-Arbeit), fail-open ohne Tabelle/Backend."""
    db = _ctx.get("db_conn")
    if not db:
        return
    b = get_brain()
    try:
        last = b.semantic.cursor("stream_memories")
        with db() as conn:
            rows = conn.execute(
                "SELECT id, username, summary FROM stream_memories "
                "WHERE id > ? ORDER BY id LIMIT 20", (last,)).fetchall()
        for r in rows:
            if b.semantic.index_text("stream_memory", r["username"],
                                     r["summary"] or "", ref=str(r["id"])):
                last = r["id"]
            else:
                break              # Backend down → nächste Runde erneut
        if rows:
            b.semantic.cursor("stream_memories", last)
    except Exception as e:
        log.debug("Semantik-Ingest übersprungen: %s", e)


_last_shield_ts = 0.0


def _ingest_shield_blocks():
    """V37: SENTINEL-SHIELD-Blocks aus kick_mod_log als Brain-Metriken
    spiegeln (shield_blocks gesamt + je Kategorie). Cursor-basiert, damit
    jede Abwehr genau einmal in die Zeitreihe zählt. So taucht der Schutz
    im Metrik-Panel UND im Wochenreport auf, nicht nur im 24h-Fenster."""
    db = _ctx.get("db_conn")
    if not db:
        return
    b = get_brain()
    try:
        last = b.semantic.cursor("shield_log")   # dieselbe Cursor-Tabelle
        cats = {"DOXXING": 0, "HATE": 0, "DROHUNG": 0}
        total, maxid = 0, last
        with db() as conn:
            rows = conn.execute(
                "SELECT id, meta FROM kick_mod_log WHERE actor='sentinel-shield' "
                "AND id > ? ORDER BY id LIMIT 200", (last,)).fetchall()
        import json as _json
        for r in rows:
            total += 1
            maxid = r["id"]
            try:
                m = _json.loads(r["meta"] or "{}")
            except Exception:
                m = {}
            c = (m.get("cat") or "").upper()
            if c in cats:
                cats[c] += 1
        if total:
            now = time.time()
            b.memory.record_metric("shield_blocks", total, now)
            for c, n in cats.items():
                if n:
                    b.memory.record_metric(f"shield_{c.lower()}", n, now)
            b.semantic.cursor("shield_log", maxid)
    except Exception as e:
        log.debug("Shield-Ingest übersprungen: %s", e)


def _bridge_tick() -> None:
    global _last_kg_ts, _last_sched_ts, _last_sem_ts
    _sync_db_state()
    b = get_brain()
    ctx = _telemetry()
    _record_metrics(ctx)
    if time.time() - _last_sem_ts > 300:
        _last_sem_ts = time.time()
        _ingest_stream_memories()
    global _last_shield_ts
    if time.time() - _last_shield_ts > 120:
        _last_shield_ts = time.time()
        _ingest_shield_blocks()
    _daily_briefing()
    ctx["history"] = b.state.history(200)
    b.tick(extra_ctx=ctx)
    if time.time() - _last_kg_ts >= KG_REFRESH_S:
        _last_kg_ts = time.time()
        try:
            b.knowledge.refresh(b.memory)
        except Exception:
            log.exception("KG-Refresh-Fehler (isoliert)")
    if time.time() - _last_sched_ts >= SCHED_EVERY_S:
        _last_sched_ts = time.time()
        try:
            hints = b.scheduler.plan(b.memory)
            if hints:
                log.debug("Scheduler: %d Hints, Top: %s (%ss)",
                          len(hints), hints[0]["username"],
                          hints[0]["interval_s"])
        except Exception:
            log.exception("Scheduler-Plan-Fehler (isoliert)")
    try:
        ctx["restream_restart"] = _ctx.get("restream_restart")   # V37-W-PLUS
        ctx["pause_source"] = _ctx.get("pause_source")           # V37-B91e
        ctx["dead_streak"] = _ctx.get("preflight_dead_streak")   # V37-B91e
        ctx["unpause_source"] = _ctx.get("unpause_source")       # V37-B91f
        b.agents.run_due(ctx)
    except Exception:
        log.exception("Agent-Runde-Fehler (isoliert)")


def start_bridge_tick(interval_s: float = TICK_S) -> None:
    """Eigener Daemon-Thread (NICHT Brain.start_tick: der Bridge-Tick
    macht zusätzlich DB-Sync + Telemetrie vor der Regelrunde)."""
    import threading
    if _ctx.get("_tick_thread") and _ctx["_tick_thread"].is_alive():
        return                      # BH-11b: kein zweiter Tick-Thread

    def _run():
        log.info("Brain-Bridge-Tick gestartet (%.0fs)", interval_s)
        while True:
            try:
                _bridge_tick()
            except Exception:
                log.exception("Bridge-Tick-Fehler (isoliert)")
            time.sleep(interval_s)

    t = threading.Thread(target=_run, name="brain-bridge", daemon=True)
    _ctx["_tick_thread"] = t
    t.start()


# ---------------------------------------------------------------- Init

def init_bridge(db_conn: Callable, flask_app=None,
                notify: Optional[Callable[[str], None]] = None,
                cookie_file: str = "tiktok_cookies.txt",
                recordings_dir: str = "recordings",
                restream_restart: Optional[Callable] = None,
                wchat_status: Optional[Callable] = None,
                preflight_stats: Optional[Callable] = None,
                preflight_dead_streak: Optional[Callable] = None,
                pause_source: Optional[Callable] = None,
                unpause_source: Optional[Callable] = None,
                crowdsec: Optional[Callable] = None,
                restream_health: Optional[Callable] = None,
                moderation: Optional[Callable] = None,
                recording_health: Optional[Callable] = None,
                tiktok_status: Optional[Callable] = None,
                agent_notify: Optional[Callable] = None,
                start_tick: bool = True) -> None:
    """Einziger Aufruf aus bot_v36.main(), VOR dem Flask-Thread-Start.

    db_conn        : bot_v36.db_conn (Context-Manager-Factory)
    flask_app      : dashboard_app → registriert /api/brain/*
    notify         : Callable(text) für Alarme (z.B. Telegram-Wrapper);
                     None = log.warning-Fallback
    """
    _ctx.update(db_conn=db_conn, notify=notify,
                cookie_file=cookie_file, recordings_dir=recordings_dir,
                restream_restart=restream_restart, wchat_status=wchat_status,
                preflight_stats=preflight_stats,
                preflight_dead_streak=preflight_dead_streak,
                pause_source=pause_source, unpause_source=unpause_source,
                crowdsec=crowdsec, restream_health=restream_health,
                moderation=moderation, recording_health=recording_health,
                tiktok_status=tiktok_status, agent_notify=agent_notify)
    # BH-11: Idempotenz-Guard. Ein zweiter Aufruf (Restart-Pfad, Tests)
    # würde Flask-Routen doppelt registrieren → AssertionError → der Shim
    # fängt sie → Bot liefe still OHNE Brain weiter. Zweiter Aufruf
    # aktualisiert daher nur den Kontext (db_conn/notify) und kehrt zurück;
    # Regeln/Handler/Agenten sind ohnehin Upsert-fähig.
    if _ctx.get("_initialized"):
        _register_rules()          # Upsert: neue Schwellen aus Env ziehen
        log.info("Brain-Bridge bereits initialisiert — Kontext aktualisiert")
        return
    _ctx["_initialized"] = True
    _register_rules()
    _register_db_handlers()
    _register_agents()
    if flask_app is not None:
        _register_routes(flask_app)
    if start_tick:
        start_bridge_tick()
    # V37: einmaliges Backend-Log — nach dem llama.cpp-Umstieg soll im
    # Journal sofort sichtbar sein, welches LLM-Backend wirklich antwortet.
    def _log_llm_backend():
        try:
            h = get_brain().llm.health()
            if h.get("backend_conf") == "off":
                log.info("Brain-LLM: konfiguriert AUS")
            elif (h.get("llamacpp") or {}).get("up"):
                log.info("Brain-LLM: llama.cpp OK (%s)",
                         os.getenv("BRAIN_LLAMACPP_URL", "http://127.0.0.1:8080"))
            # V37: Ollama-Fallback entfernt — llama.cpp down = Cloud (freeai) übernimmt.
            else:
                log.warning("Brain-LLM: KEIN Backend erreichbar — Tier 4 aus")
        except Exception:
            pass
    import threading as _th
    _th.Thread(target=_log_llm_backend, name="llm-backend-log",
               daemon=True).start()
    log.info("Brain-Bridge initialisiert: %d Regeln, Tick=%ss",
             len(get_brain().rules.rules_status()), TICK_S)
