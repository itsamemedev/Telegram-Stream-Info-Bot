"""nc.routes.brain — die Routen unter /api/brain als Flask-Blueprint.

Welle 3 der Zerlegung (siehe docs/MODULARISIERUNG.md). Pfade stehen woertlich
in den Dekoratoren (kein url_prefix); was der Monolith weiterhin stellen muss,
kommt ueber nc.ctx statt ueber einen Import aus bot.py.

v4.1-W21: Sechs Routen, **null neue Kontext-Eintraege**. Roh waeren es
siebzehn gewesen — bei 24 von vertraglich 25 belegten Plaetzen unmoeglich.
Vorweg geloest nach nc/brainstate.py: die Ringpuffer der Knoten-Historie, das
Uebergangs-Gedaechtnis, der Bruecken-Zustand, die Sende-Bremse des
Dashboard-Chats, der Waechter-Zustand des Check-Loops — und zwei Register.

Warum zwei davon Register sein MUESSEN und nicht Aliase sein koennen:

* **STALLS** war eine ganze Zahl (`_LOOP_STALL_COUNT += 1`). Eine Zahl laesst
  sich nicht teilen; ein Alias waere eine Kopie, die fuer immer auf 0 steht,
  und /api/brain/health meldete "keine Stalls", waehrend der Loop klemmt.
* **PROXY** entsteht im Monolithen erst weit unten in der Datei. Dort stand
  dafuer `globals().get("PROXY_ROUTER")` — hier waere globals() der
  Namensraum DIESER Datei, und das Panel meldete den Proxy fuer immer als
  "idle".

Die .env-Werte werden bei JEDEM Aufruf gelesen statt als Modul-Konstante
eingefroren (CLAUDE.md: .env laedt teils erst nach den ersten Imports).
Benutzertexte laufen durch t(...) — an der Quelle, nicht im Browser.
"""

import os
import time
from datetime import datetime, timedelta, timezone

from flask import Blueprint, jsonify, request

from nc import brainstate as _nc_brainstate
from nc import fehlertext as _nc_fehlertext
from nc import i18n as _nc_i18n
from nc.dbwrap import db_conn
from nc.stats import get_tiktok_status_distribution

from nc import ctx as _ctx

bp = Blueprint("brain", __name__)


def _fehler_text(e, wo=""):
    """v4.1-W30: der Wortlaut geht ins Log, nach aussen die gesaeuberte
       Fassung — ohne Pfade, ohne Zugangsdaten, gekuerzt. Siehe
       nc/fehlertext.py, dort steht auch, warum nicht einfach "interner
       Fehler"."""
    return _nc_fehlertext.nach_aussen(e, wo)


def _c():
    """Laufzeitkontext. Aufruf statt Modul-Konstante — der Kontext wird erst
       beim Bot-Start gefuellt."""
    return _ctx.get()


def _t(s):
    """v4.1-W21: an der Quelle uebersetzen. Diese Texte erreichen das DOM
       meist verkettet ("Fehler: " + error) — ein Katalogeintrag fuer den
       blossen Text traefe dort nie."""
    return _nc_i18n.t(s)


def _uptime_s() -> int:
    """v4.0-W88: Prozess-Uptime in Sekunden (0 vor dem Start)."""
    try:
        start = _c().get_bot_start_time()
        if start is None:
            return 0
        return int((datetime.now(timezone.utc) - start).total_seconds())
    except Exception:
        return 0



@bp.route("/api/brain/health")
def api_brain_health():
    """v4.0-W81: Start-Status der Brain-Bridge — existiert IMMER (unabhängig
       davon, ob die Bridge selbst hochkam), damit das Dashboard bei gescheiterter
       Bridge den echten Grund zeigen kann statt nur „GESTÖRT"."""
    return jsonify(ok=bool(_nc_brainstate.BRIDGE.get("ok")),
                   phase=_nc_brainstate.BRIDGE.get("phase"),
                   error=_nc_brainstate.BRIDGE.get("error"),
                   version=os.getenv("BUILD_STAMP", "2026.08 · v4.1"),                       # v4.0-W88
                   uptime_s=_uptime_s(),                      # v4.0-W88
                   loop_stalls=_nc_brainstate.STALLS["n"])             # v4.0-W88


@bp.route("/api/brain/graph")
def api_brain_graph():
    """B155: Wissensgraph (Creator + abgeleitete Fakten) fuer die Brain-Visualisierung.
       Waechst automatisch mit dem KG-Refresh (BRAIN_KG_REFRESH_S)."""
    try:
        limit = _c().arg_int("limit", 300, 20, 600)
    except ValueError:
        limit = 300
    out = {"ok": True, "nodes": [], "edges": [], "triples": 0, "creators": 0}
    try:
        from brain import get_brain
        kg = get_brain().knowledge
        g = kg.graph_export(limit=limit)
        out["nodes"] = g.get("nodes", [])
        out["edges"] = g.get("edges", [])
        out["triples"] = kg.stats().get("triples", 0)
        out["creators"] = sum(1 for n in out["nodes"] if n.get("kind") == "subject")
    except Exception as e:
        out = {"ok": False, "error": _fehler_text(e, "brain-graph"), "nodes": [], "edges": [],
               "triples": 0, "creators": 0}
    return jsonify(out)


@bp.route("/api/brain/creator")
def api_brain_creator():
    """B157: gelernte Fakten eines Creators (Subjekt) fuer den Wissensgraph-Inspektor."""
    cid = (request.args.get("id") or "").strip()
    if not cid:
        return jsonify(ok=False, error=_t("id fehlt"), facts=[])
    try:
        from brain import get_brain
        facts = [{"p": t["p"], "o": t["o"], "weight": round(float(t.get("weight") or 0), 2)}
                 for t in get_brain().knowledge.query(s=cid, limit=60)]
    except Exception as e:
        return jsonify(ok=False, error=_fehler_text(e, "api_brain_creator"), id=cid, facts=[])
    return jsonify(ok=True, id=cid, facts=facts, count=len(facts))


@bp.route("/api/brain/alarms")
def api_brain_alarms():
    """B158: Verlauf der Sentinel-Befunde (agent_finding-Events) fuer die Alarm-Zeitleiste."""
    lvl = (request.args.get("level") or "").strip()
    try:
        limit = _c().arg_int("limit", 120, 10, 300)
    except ValueError:
        limit = 120
    out = []
    try:
        from brain import get_brain
        for e in get_brain().memory.events(kind="agent_finding", limit=limit):
            d = e.get("data") or {}
            lv = d.get("level", "info")
            if lvl and lv != lvl:
                continue
            out.append({"ts": e.get("ts"), "agent": e.get("key", ""),
                        "level": lv, "text": str(d.get("text", ""))[:200]})
    except Exception as ex:
        return jsonify(ok=False, error=str(ex)[:120], alarms=[])
    return jsonify(ok=True, alarms=out, count=len(out))


@bp.route("/api/brain/growth")
def api_brain_growth():
    """V37-BRAINVIZ: Wachstumskurve — echte Zeitreihe, wie das Brain lernt.
    ?days=30 begrenzt. Liefert Serien für Wissen/Vektoren/Nutzer."""
    try:
        days = _c().arg_int("days", 30, 1, 365)
    except ValueError:
        days = 30
    out = {"ok": True, "points": [], "current": {}}
    try:
        with db_conn() as conn:
            cur = conn.cursor()
            try:
                cur.execute(
                    "SELECT ts, triples, vectors, users, sessions FROM brain_growth "
                    "WHERE ts >= datetime('now', ?) ORDER BY ts", ("-%d days" % days,))
            except Exception:
                cur.execute(
                    "SELECT ts, triples, vectors, users, sessions FROM brain_growth "
                    "WHERE ts >= (NOW() - INTERVAL %d DAY) ORDER BY ts" % days)
            for r in cur.fetchall():
                out["points"].append({
                    "ts": r["ts"], "triples": r["triples"], "vectors": r["vectors"],
                    "users": r["users"], "sessions": r["sessions"]})
        # aktueller Live-Stand (auch wenn noch kein Snapshot existiert)
        try:
            from brain import get_brain
            b = get_brain()
            out["current"] = {
                "triples": b.knowledge.stats().get("triples", 0),
                "vectors": b.semantic.stats().get("vectors", 0),
                "users": b.semantic.stats().get("users", 0),
                "predicates": b.knowledge.stats().get("predicates", {})}
        except Exception:
            pass
        return jsonify(out)
    except Exception as e:
        return jsonify(ok=False, error=_fehler_text(e, "api_brain_growth")), 500


@bp.route("/api/brain")
def api_brain():
    """Real-time state aller Subsysteme + aktive Prozessliste + Historie."""
    now = time.monotonic()

    nodes = {}

    # CORE: immer aktiv (wir antworten ja)
    nodes["core"] = {"status": "active", "activity": 50, "label": "BOT CORE"}

    # WORKER: aktive Live-Checks. Wenn _nc_brainstate.NEXT_CHECK_AT viele Trackings hat → aktiv
    try:
        # _nc_brainstate.NEXT_CHECK_AT ist ein Modul-Level-Global, immer vorhanden — der
        # frühere "X" in globals()-Check war Dead Code (Hinweis aus Header).
        pending = len(_nc_brainstate.NEXT_CHECK_AT)
        nodes["worker"] = {
            "status": "active" if pending > 0 else "idle",
            "activity": min(100, pending * 5),
            "label": "WORKER",
            "detail": f"{pending} trackings",
        }
    except Exception:
        nodes["worker"] = {"status": "idle", "activity": 0, "label": "WORKER"}

    # RECORDER: aktive Recording-Prozesse
    try:
        with db_conn() as conn:
            row = conn.execute(
                "SELECT COUNT(*) AS c FROM trackings WHERE recording = 1").fetchone()
        active_recs = row["c"] or 0
        if active_recs > 0:
            status = "working"
            activity = min(100, 30 + active_recs * 20)
        else:
            status = "idle"
            activity = 0
        nodes["recorder"] = {
            "status": status, "activity": activity, "label": "RECORDER",
            "detail": f"{active_recs} active",
        }
    except Exception:
        nodes["recorder"] = {"status": "idle", "activity": 0, "label": "RECORDER"}

    # TIKTOK API: ableitbar aus letzten Worker-Cycles + backoff-state
    try:
        # BUG-FIX: list()-Snapshot — der Async-Worker kann _nc_brainstate.DEAD_BACKOFF_UNTIL
        # parallel mutieren ('dictionary changed size during iteration').
        in_backoff = len([t for t, until in list(_nc_brainstate.DEAD_BACKOFF_UNTIL.items())
                          if until > now])
        if in_backoff > 0:
            nodes["tiktok"] = {
                "status": "error" if in_backoff > 5 else "active",
                "activity": 40, "label": "TIKTOK",
                "detail": f"{in_backoff} in backoff",
            }
        else:
            nodes["tiktok"] = {"status": "active", "activity": 30, "label": "TIKTOK"}
    except Exception:
        nodes["tiktok"] = {"status": "idle", "activity": 0, "label": "TIKTOK"}

    # DATABASE: praktisch immer aktiv (wir lesen ja gerade)
    nodes["database"] = {"status": "active", "activity": 20, "label": "DATABASE"}

    # TELEGRAM: ableitbar aus letzter Aktivität (count messages in last 5min)
    try:
        cutoff = (datetime.now(timezone.utc) - timedelta(minutes=5)).isoformat()
        with db_conn() as conn:
            row = conn.execute(
                "SELECT COUNT(*) AS c FROM ai_log WHERE created_at >= ?",
                (cutoff,)).fetchone()
        recent = row["c"] or 0
        nodes["telegram"] = {
            "status": "active" if recent > 0 else "idle",
            "activity": min(100, recent * 10),
            "label": "TELEGRAM",
            "detail": f"{recent} msgs/5min",
        }
    except Exception:
        nodes["telegram"] = {"status": "idle", "activity": 0, "label": "TELEGRAM"}

    # AI/OLLAMA: aus letzter Rate
    try:
        with _nc_brainstate.AI_LOCK:
            ai_count = len(_nc_brainstate.AI_RATE)
        nodes["ai"] = {
            "status": "working" if ai_count > 0 else "idle",
            "activity": min(100, ai_count * 15),
            "label": "AI",
            "detail": f"{ai_count} calls/min",
        }
    except Exception:
        nodes["ai"] = {"status": "idle", "activity": 0, "label": "AI"}

    # ARCHIVE: storage stats
    try:
        with db_conn() as conn:
            row = conn.execute(
                "SELECT COUNT(*) AS c FROM recording_attempts "
                "WHERE outcome IN ('ok','stall_killed_partial')").fetchone()
        rec_count = row["c"] or 0
        nodes["archive"] = {
            "status": "active" if rec_count > 0 else "idle",
            "activity": 25,
            "label": "ARCHIVE",
            "detail": f"{rec_count} files",
        }
    except Exception:
        nodes["archive"] = {"status": "idle", "activity": 0, "label": "ARCHIVE"}

    # Active processes feed (was läuft GERADE)
    processes = []
    try:
        # B2-Fix: ALLES innerhalb des with db_conn()-Blocks halten. Vorher wurde
        # `conn.execute(...)` auf Z. 8433 außerhalb des with-Blocks aufgerufen.
        # SQLite ließ das durch (Connection wird nicht geschlossen beim exit),
        # MariaDB nicht: __exit__ → close() → Conn zurück in den Pool → der
        # nächste Aufruf liest aus einer fremden Connection oder crashed.
        with db_conn() as conn:
            recs = conn.execute(
                "SELECT username, output_file, pid FROM trackings WHERE recording = 1 LIMIT 8"
            ).fetchall()
            for r in recs:
                processes.append({
                    "type": "recording",
                    "label": f"Recording @{r['username']}",
                    "detail": os.path.basename(r['output_file'] or '') or '—',
                    "pid": r['pid'] or 0,
                })
            in_backoff = list(_nc_brainstate.DEAD_BACKOFF_UNTIL.items())[:5]
            for tid, until in in_backoff:
                remaining = max(0, int(until - now))
                row = conn.execute(
                    "SELECT username FROM trackings WHERE id = ?", (tid,)).fetchone()
                if row and remaining > 0:
                    processes.append({
                        "type": "backoff",
                        "label": f"Backoff @{row['username']}",
                        "detail": f"{remaining}s remaining",
                        "pid": 0,
                    })
    except Exception:
        pass

    # PROXY: bei festem (os.getenv("RECORD_PROXY", "") or "").strip() trägt der feste Proxy 100% des TikTok-
    # Verkehrs — der rotierende Pool schläft dann (healthy=0, sähe „idle" aus).
    # Gesundheit daher aus der Fetch-Erfolgsrate (Status-Counter), sonst Pool.
    try:
        if (os.getenv("RECORD_PROXY", "") or "").strip():
            dist = get_tiktok_status_distribution()
            total = dist.get("total", 0) or 0
            by = {d["code"]: d for d in dist.get("by_code", [])}
            ok = 100.0 * by.get(200, {}).get("count", 0) / total if total else None
            if total < 15 or ok is None:
                nodes["proxy"] = {"status": "active", "activity": 40,
                                  "label": "PROXY", "detail": "fester Proxy · aufwärmend"}
            else:
                st = "active" if ok >= 60 else ("working" if ok >= 25 else "error")
                nodes["proxy"] = {"status": st, "activity": max(6, min(100, int(ok))),
                                  "label": "PROXY",
                                  "detail": f"fester Proxy · {ok:.0f}% 200 ({total} Fetches)"}
        else:
            pr = _nc_brainstate.PROXY["obj"].stats()
            healthy = pr.get("healthy", 0)
            nodes["proxy"] = {
                "status": "active" if healthy > 0 else ("error" if pr.get("total", 0) > 0 else "idle"),
                "activity": min(100, healthy * 8),
                "label": "PROXY",
                "detail": f"{healthy}/{pr.get('total',0)} healthy · {pr.get('strategy','')}",
            }
    except Exception:
        nodes["proxy"] = {"status": "idle", "activity": 0, "label": "PROXY"}

    # Historie + Stream aktualisieren (vor dem Anreichern lesen)
    _nc_brainstate.record(nodes)

    # Pro-Knoten Historie (Sparkline) + Anomalie-Flag anhängen
    for key, n in nodes.items():
        hist = _nc_brainstate.history_for(key)
        n["history"] = hist
        # Anomalie: aktueller Wert weicht stark vom jüngsten Mittel ab, oder error
        anomaly = (n.get("status") == "error")
        if len(hist) >= 6:
            recent = hist[-6:-1] or [0]
            avg = sum(recent) / len(recent)
            if avg > 0 and n.get("activity", 0) > avg * 2.2:
                anomaly = True
        n["anomaly"] = anomaly

    # Kognitive Gesamt-Last (gewichteter Mittelwert der Activity) + Brain-State
    acts = [n.get("activity", 0) for n in nodes.values()]
    cognitive_load = round(sum(acts) / len(acts)) if acts else 0
    error_nodes = [n.get("label") for n in nodes.values() if n.get("status") == "error"]
    working_nodes = sum(1 for n in nodes.values() if n.get("status") == "working")
    if error_nodes:
        brain_state = "STRESSED"
    elif cognitive_load > 60 or working_nodes >= 2:
        brain_state = "FOCUSED"
    elif cognitive_load > 20:
        brain_state = "ACTIVE"
    else:
        brain_state = "IDLE"

    return jsonify({
        "nodes": nodes,
        "processes": processes,
        "cognitive_load": cognitive_load,
        "brain_state": brain_state,
        "error_nodes": error_nodes,
        "stream": _nc_brainstate.stream_recent(20),
        "timestamp": datetime.now(timezone.utc).isoformat(),
    })
