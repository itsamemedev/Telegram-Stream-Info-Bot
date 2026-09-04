"""nc.routes.evolution — die Routen unter /api/evolution als Flask-Blueprint.

Welle 3 der Zerlegung (siehe docs/MODULARISIERUNG.md), erzeugt mit
tools/bp_extract.py. Pfade stehen woertlich in den Dekoratoren (kein
url_prefix); app-weite Hooks bleiben auf der App.

Das erste Blueprint OHNE nc.ctx: der Evolution-Core liegt seit v4.1-W3
vollstaendig in nc/evolution.py, deshalb importiert dieses Modul ihn direkt
statt sich Helfer durch den Kontext reichen zu lassen. Genau das ist die
Reihenfolge aus W117 — erst den Kern loesen, dann die Routen; der Kontext
waechst dabei um null Eintraege.
"""

import glob
import json
import os

from flask import Blueprint, jsonify, request

from nc import i18n as _nc_i18n
from nc import evolution as _nc_evolution
from nc import fehlertext as _nc_fehlertext
from nc.dbwrap import db_conn

bp = Blueprint("evolution", __name__)


def _fehler_text(e, wo=""):
    """v4.1-W30: der Wortlaut geht ins Log, nach aussen die gesaeuberte
       Fassung — ohne Pfade, ohne Zugangsdaten, gekuerzt. Siehe
       nc/fehlertext.py, dort steht auch, warum nicht einfach "interner
       Fehler"."""
    return _nc_fehlertext.nach_aussen(e, wo)

def _t(s):
    """v4.1-W20: an der Quelle uebersetzen. Diese Texte erreichen das DOM
       meist verkettet ("Fehler: " + error) — ein Katalogeintrag fuer den
       blossen Text traefe dort nie."""
    return _nc_i18n.t(s)



@bp.route("/api/evolution/status")
def api_evolution_status():
    """Zustand des Evolution Core: Version, letzter Zyklus, Wissens-/Vorschlags-
       Zähler, 'Wissens-Level' (für die Gehirn-Anzeige)."""
    try:
        with db_conn() as conn:
            last = conn.execute("SELECT version, ts, summary, insights, proposals, files, trigger "
                               "FROM evolution_log ORDER BY id DESC LIMIT 1").fetchone()
            cycles = conn.execute("SELECT COUNT(*) AS n FROM evolution_log").fetchone()["n"]
            nlearned = conn.execute("SELECT COUNT(*) AS n, AVG(confidence) AS c, "
                                   "SUM(samples) AS s FROM learned_params").fetchone()
            open_props = conn.execute("SELECT COUNT(*) AS n FROM evolution_proposals "
                                     "WHERE status='proposed'").fetchone()["n"]
        knew = int(nlearned["n"] or 0)
        avg_conf = round((nlearned["c"] or 0) * 100, 0)
        samples = int(nlearned["s"] or 0)
        # Wissens-Level 0-100: skaliert mit Anzahl Parameter, Konfidenz und Samples
        knowledge = min(100, round(0.35 * min(100, knew * 6)
                                   + 0.35 * (avg_conf or 0)
                                   + 0.30 * min(100, samples / 2.0)))
        _evo = _nc_evolution.conf()
        return jsonify(
            ok=True, enabled=_evo["enabled"], version=_nc_evolution.next_version() - 1,
            next_version=_nc_evolution.next_version(), cycles=int(cycles or 0),
            interval_hours=_evo["interval_hours"], use_llm=_evo["use_llm"],
            learned_params=knew, avg_confidence=avg_conf, total_samples=samples,
            knowledge_level=knowledge, open_proposals=int(open_props or 0),
            build_dir=_nc_evolution.build_dir(),
            last_cycle=(dict(version=last["version"], ts=(last["ts"] or "")[:19],
                             summary=last["summary"], insights=last["insights"],
                             proposals=last["proposals"], files=last["files"],
                             trigger=last["trigger"]) if last else None))
    except Exception as e:
        return jsonify(ok=False, error=_fehler_text(e, "api_evolution_status")), 500


@bp.route("/api/evolution/run", methods=["POST"])
def api_evolution_run():
    """Startet sofort einen Lern-Zyklus (manuell). Läuft im Flask-Thread."""
    try:
        res = _nc_evolution.cycle("manual")
        return jsonify(res)
    except Exception as e:
        return jsonify(ok=False, error=_fehler_text(e, "api_evolution_run")), 500


@bp.route("/api/evolution/learned")
def api_evolution_learned():
    """Alle gelernten Parameter mit Konfidenz + Samples."""
    try:
        with db_conn() as conn:
            rows = conn.execute("SELECT k, v, confidence, samples, category, updated_at "
                               "FROM learned_params ORDER BY category, k").fetchall()
        out = []
        for r in rows:
            try:
                val = json.loads(r["v"])
            except Exception:
                val = r["v"]
            out.append({"key": r["k"], "value": val,
                        "confidence": round((r["confidence"] or 0) * 100, 0),
                        "samples": r["samples"], "category": r["category"],
                        "updated_at": (r["updated_at"] or "")[:19]})
        return jsonify(ok=True, params=out, count=len(out))
    except Exception as e:
        return jsonify(ok=False, error=_fehler_text(e, "api_evolution_learned")), 500


@bp.route("/api/evolution/proposals")
def api_evolution_proposals():
    """Vorschläge (default nur offene). ?all=1 für alle."""
    show_all = request.args.get("all") in ("1", "true", "yes")
    try:
        with db_conn() as conn:
            q = ("SELECT id, version, ts, category, title, rationale, confidence, impact, status "
                 "FROM evolution_proposals ")
            if not show_all:
                q += "WHERE status='proposed' "
            q += "ORDER BY confidence DESC, id DESC LIMIT 100"
            rows = conn.execute(q).fetchall()
        return jsonify(ok=True, proposals=[
            {"id": r["id"], "version": r["version"], "ts": (r["ts"] or "")[:19],
             "category": r["category"], "title": r["title"], "rationale": r["rationale"],
             "confidence": round((r["confidence"] or 0) * 100, 0),
             "impact": r["impact"], "status": r["status"]} for r in rows])
    except Exception as e:
        return jsonify(ok=False, error=_fehler_text(e, "api_evolution_proposals")), 500


@bp.route("/api/evolution/proposals/<int:pid>/dismiss", methods=["POST"])
def api_evolution_dismiss(pid):
    """Markiert einen Vorschlag als erledigt/verworfen."""
    payload = request.get_json(silent=True) or {}
    new_status = "applied" if payload.get("applied") else "dismissed"
    try:
        with db_conn() as conn:
            row = conn.execute("SELECT 1 FROM evolution_proposals WHERE id=?", (pid,)).fetchone()
            if not row:
                return jsonify(ok=False, error=_t("Vorschlag nicht gefunden.")), 404
            conn.execute("UPDATE evolution_proposals SET status=? WHERE id=?", (new_status, pid))
            conn.commit()
        return jsonify(ok=True, id=pid, status=new_status)
    except Exception as e:
        return jsonify(ok=False, error=_fehler_text(e, "api_evolution_dismiss")), 500


@bp.route("/api/evolution/history")
def api_evolution_history():
    """Liste der Lern-Zyklen (neueste zuerst)."""
    try:
        with db_conn() as conn:
            rows = conn.execute("SELECT version, ts, summary, insights, proposals, files, trigger "
                               "FROM evolution_log ORDER BY id DESC LIMIT 40").fetchall()
        return jsonify(ok=True, history=[
            {"version": r["version"], "ts": (r["ts"] or "")[:19], "summary": r["summary"],
             "insights": r["insights"], "proposals": r["proposals"], "files": r["files"],
             "trigger": r["trigger"]} for r in rows])
    except Exception as e:
        return jsonify(ok=False, error=_fehler_text(e, "api_evolution_history")), 500


@bp.route("/api/evolution/changelog")
def api_evolution_changelog():
    """Inhalt der generierten CHANGELOG.md (für die Dashboard-Anzeige)."""
    path = os.path.join(_nc_evolution.build_dir(), "CHANGELOG.md")
    if not os.path.exists(path):
        return jsonify(ok=True, exists=False, content="",
                       note="Noch kein Zyklus gelaufen — Changelog wird beim ersten erzeugt.")
    try:
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()[:40000]
        return jsonify(ok=True, exists=True, path=path, content=content)
    except Exception as e:
        return jsonify(ok=False, error=_fehler_text(e, "api_evolution_changelog")), 500


@bp.route("/api/evolution/snapshots")
def api_evolution_snapshots():
    """Listet verfügbare bot.py-Snapshots im build/-Ordner (Self-Reproduction Manifest)."""
    bdir = _nc_evolution.build_dir()
    manifest_path = os.path.join(bdir, "snapshots.json")
    snapshots = []
    if os.path.exists(manifest_path):
        try:
            with open(manifest_path, "r", encoding="utf-8") as f:
                snapshots = json.load(f)
        except Exception:
            pass
    # Fallback: build/-Ordner nach bot_v*.py scannen
    if not snapshots:
        for p in sorted(glob.glob(os.path.join(bdir, "bot_v*.py")), reverse=True)[:10]:
            snapshots.append({
                "file": os.path.basename(p),
                "size_kb": round(os.path.getsize(p) / 1024, 1),
                "ts": "",
            })
    return jsonify(ok=True, snapshots=snapshots, build_dir=bdir)
