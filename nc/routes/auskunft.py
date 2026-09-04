"""nc.routes.auskunft — die kleinen Fragen, die das Deck stellt.

Welle 3 der Zerlegung (siehe docs/MODULARISIERUNG.md). Pfade stehen woertlich
in den Dekoratoren (kein url_prefix); was der Monolith weiterhin stellen muss,
kommt ueber nc.ctx statt ueber einen Import aus bot.py.

v4.1-W26: Die lange Reihe kleiner Routen, die einzeln keinen eigenen Blueprint
rechtfertigen. Die Klammer ist streng: **sie ANTWORTEN nur.** Keine Route hier
startet, stoppt, loescht oder speichert etwas — /api/annotations (DELETE) und
/api/highlights/config (POST) sind deshalb ausdruecklich NICHT dabei,
obwohl sie benachbart liegen. Ein Vertrag haelt das fest: kaeme hier je ein
schreibender Pfad herein, waere die Klammer eine Behauptung statt einer Regel.

**Null neue Kontext-Eintraege.** Vorweg geloest:

* **nc/suche.py** — die bestandsweite Suche (60 Zeilen Fachlogik).
* **nc/outcomes.py** — warum Aufnahmen scheitern, mitsamt der Zuordnung
  Ausgang -> Klartext und Farbe.
* **nc/bandbreite.py** — wie schnell die laufenden Aufnahmen wachsen.
* **nc/storage.py** — die Vorhersage "wann ist die Platte voll" steht jetzt
  neben "wie viel Platz ist da". Das gehoert zusammen.
"""

import json
import os
import time
from datetime import datetime, timedelta, timezone

from flask import Blueprint, jsonify, request

from nc import bandbreite as _nc_band
from nc import cfgnorm as _nc_cfgnorm
from nc import community as _community
from nc import freeai as _nc_freeai
from nc import highlights as _nc_highlights
from nc import i18n as _nc_i18n
from nc import loyalty as _loyalty
from nc import outcomes as _nc_outcomes
from nc import stats as _nc_stats
from nc import storage as _nc_storage
from nc import suche as _nc_suche
from nc import version as _nc_version
from nc.cfgstore import get as _cfg_get
from nc.dbwrap import db_conn
from nc.envnum import env_int as _env_int
from nc.recdb import (get_all_checks, get_bookmarked_recordings,
                      get_recent_recording_attempts)
from nc.trackingdb import get_all_tags_with_counts
from nc.stats import (get_activity_pulse, get_lives_heatmap, get_per_user_stats,
                      get_recordings_heatmap)
from nc.textutil import clean_username

# /api/pulse buendelt vier bestehende Antworten zu einer. Es ruft die Routen
# der anderen Blueprints direkt auf — das ist kein Umweg, sondern der Zweck
# dieser Route: EIN Aufruf statt vier, damit das Deck im Sekundentakt nicht
# vier Verbindungen aufmacht.
from nc.routes import health as _nc_routes_health
from nc.routes import restream as _nc_routes_restream
from nc.routes import stats as _nc_routes_stats

from nc import ctx as _ctx

bp = Blueprint("auskunft", __name__)


def _c():
    """Laufzeitkontext. Aufruf statt Modul-Konstante — der Kontext wird erst
       beim Bot-Start gefuellt."""
    return _ctx.get()


def _t(s):
    """v4.1-W26: an der Quelle uebersetzen. Diese Texte erreichen das DOM
       meist verkettet ("Fehler: " + error) — ein Katalogeintrag fuer den
       blossen Text traefe dort nie."""
    return _nc_i18n.t(s)


def _tagesbericht_chat() -> int:
    """Ziel-Chat der Tageszusammenfassung. 0 heisst aus. Als Funktion und
       nicht als Konstante: .env wird teils erst nach den ersten Imports
       geladen (CLAUDE.md)."""
    return _env_int("DAILY_SUMMARY_CHAT_ID", 0)


def _tagesbericht_stunde() -> int:
    """Volle Stunde in LOKALER Serverzeit. Ausserhalb 0-23 faellt sie auf 9
       zurueck — eine kaputte .env darf die Auskunft nicht kippen."""
    h = _env_int("DAILY_SUMMARY_HOUR", 9)
    return h if 0 <= h <= 23 else 9


def _ki_modell() -> str:
    return (os.getenv("AI_MODEL", "openai") or "openai").strip()


def _rec_dir() -> str:
    """Das Aufnahme-Verzeichnis. Als Funktion und nicht als Konstante: .env
       wird teils erst nach den ersten Imports geladen (CLAUDE.md)."""
    return (os.getenv("RECORDINGS_DIR", "recordings") or "recordings").strip()


# Was nur der laufende Bot kann. Der Bot traegt beim Start ein, die Routen
# rufen auf. Sichtbare Kopplung statt eines Kontext-Slots — dieselbe
# Begruendung wie in nc/routes/wartung.py und nc/routes/abwehr.py.
HAKEN = {"tagesbericht": {"fn": None},     # () -> str, baut die Tageszusammenfassung
         "ist_aufnehmer": {"fn": None},    # (pid) -> bool, prueft einen Prozess
         "oeffentlich": {"fn": None},      # () -> dict, die oeffentliche Statistik
         "netzdurchsatz": {"fn": None}}    # () -> kbit/s


def _haken(name):
    """Der eingetragene Haken, oder None. Die Aufrufer pruefen das."""
    return HAKEN[name]["fn"]


def _nicht_bereit(was):
    """Antwort, wenn der Bot den Haken nie eingetragen hat. Ausdruecklich
       NICHT ein leeres Ergebnis: eine leere Liste sieht aus wie "nichts
       gefunden", und der Betreiber sucht dann an der falschen Stelle."""
    return jsonify(ok=False, status="nicht_bereit",
                   error=_t("%s braucht den laufenden Bot") % was), 503


# Bruecke, weil sich die Signatur geaendert hat: nc/storage.py nimmt das
# Aufnahme-Verzeichnis entgegen, statt eine Modul-Konstante zu lesen.

def _nc_storage_forecast():
    return _nc_storage.forecast(_rec_dir())


@bp.route("/api/pulse")
def api_pulse():
    """V37: gebündelter Header/Sendbar-Puls — ersetzt 4 separate 5s-Poller
       (stats, bandwidth/live, health-score, restream/deck) durch EINEN
       Request. Ruft die bestehenden View-Funktionen intern auf, sodass die
       Datenstruktur 1:1 identisch bleibt (kein Frontend-Format-Drift)."""
    def _j(fn):
        try:
            r = fn()
            return r.get_json(silent=True) if hasattr(r, "get_json") else None
        except Exception:
            return None
    return jsonify(ok=True,
                   stats=_j(lambda: _nc_routes_stats.api_stats(lean=True)),
                   bandwidth=_j(api_bandwidth_live),
                   health=_j(_nc_routes_health.api_health_score),
                   deck=_j(_nc_routes_restream.api_restream_deck))


@bp.route("/api/checks")
def api_checks():
    rows = get_all_checks(limit=50)
    res = []
    for c in rows:
        d = json.loads(c["data"]) if c["data"] else {}
        res.append({"id": c["id"], "created_at": c["created_at"][:19] if c["created_at"] else "",
                    "username": c["username"],
                    "follower_count": d.get("follower_count"),
                    "heart_count": d.get("heart_count"),
                    "video_count": d.get("video_count"),
                    "verified": d.get("verified")})
    return jsonify(res)


@bp.route("/api/top")
def api_top():
    _, _, top = _nc_stats.get_stats()
    return jsonify([{"username": r["username"], "count": r["cnt"]} for r in top])


@bp.route("/api/active-recordings")
def api_active_recordings():
    # READ ONLY – Aufräumen passiert im Reaper, nicht im HTTP-Handler.
    # F59: id mitliefern damit der STOP-Button im Dashboard den richtigen
    # Endpoint /api/recordings/<tracking_id>/stop ansprechen kann.
    with db_conn() as conn:
        rows = conn.execute(
            "SELECT id, username, output_file, created_at, pid FROM trackings WHERE recording=1"
        ).fetchall()
    # Einmal holen statt je Zeile: ohne laufenden Bot gibt es keine
    # PID-Pruefung, und dann ist "alive" ehrlicherweise false statt geraten.
    _ist_aufnehmer = _haken("ist_aufnehmer")
    return jsonify([{
        "tracking_id": r["id"],
        "username": r["username"],
        "output_file": os.path.basename(r["output_file"]) if r["output_file"] else "",
        "started_at": r["created_at"][:19] if r["created_at"] else "",
        # B36: PID-Reuse-Schutz. Ohne den Check würde "alive=true" zurück-
        # gegeben werden auch wenn die PID inzwischen einem fremden Prozess
        # gehört → User sieht grünen Dot obwohl Aufnahme tot ist.
        "alive": bool(_ist_aufnehmer and _ist_aufnehmer(r["pid"])),
    } for r in rows])


@bp.route("/api/summary/preview")
def api_summary_preview():
    """Liefert den Daily-Summary-Text (HTML) ohne ihn zu posten — für
       Dashboard-Vorschau. Beinhaltet 24h-Aktivität, Top-User, Storage,
       Cookies."""
    bericht = _haken("tagesbericht")
    if not bericht:
        return _nicht_bereit(_t("Die Tageszusammenfassung"))
    try:
        text = bericht()
        return jsonify(ok=True, text=text,
                       configured=bool(_tagesbericht_chat()),
                       chat_id=_tagesbericht_chat(),
                       hour=_tagesbericht_stunde())
    except Exception as e:
        _c().log.warning(f"summary preview failed: {e}")
        return jsonify(ok=False, error=str(e)), 500


@bp.route("/api/outcomes")
def api_outcomes():
    """Recording-Outcome-Verteilung über Zeitfenster. Query-Param 'hours'
       (default 24, max 168). Hilft bei der Frage 'wieso scheitern Aufnahmen
       gerade häufig?' — zeigt Anteil pro Outcome + die User mit den meisten
       Fehlern + dedizierte Liste für early_disconnect (TikTok-CDN-Pain)."""
    try:
        hours = _c().arg_int("hours", 24)
    except (TypeError, ValueError):
        hours = 24
    return jsonify(_nc_outcomes.get_outcome_breakdown(hours))


@bp.route("/api/userstats")
def api_userstats():
    """Aggregat-Stats pro User. Query-Params:
         limit (default 20, max 200)
         sort  (rec_count|total_bytes|success_rate|last_recording)"""
    try:
        limit = _c().arg_int("limit", 20, 1, 200)
    except (TypeError, ValueError):
        limit = 20
    sort_by = request.args.get("sort", "rec_count")
    rows = get_per_user_stats(limit=limit, sort_by=sort_by)
    return jsonify(rows)


@bp.route("/api/trend-7d")
def api_trend_7d():
    """Pro Tag der letzten 7 Tage: total, ok, success-rate. Für Sparkline."""
    days = []
    cutoff = datetime.now(timezone.utc) - timedelta(days=7)
    with db_conn() as conn:
        # Portabel über SQLite und MariaDB: pro Tag SUBSTR(started_at, 1, 10)
        rows = conn.execute(
            "SELECT SUBSTR(started_at, 1, 10) AS day, "
            "  COUNT(*) AS total, "
            "  SUM(CASE WHEN outcome IN ('ok', 'stall_killed_partial') "
            "    THEN 1 ELSE 0 END) AS ok_count "
            "FROM recording_attempts "
            "WHERE started_at >= ? "
            "GROUP BY SUBSTR(started_at, 1, 10) "
            "ORDER BY day ASC",
            (cutoff.isoformat(),)).fetchall()
    by_day = {r["day"]: (r["total"] or 0, r["ok_count"] or 0) for r in rows}
    # Ensure 7 days even if some have no data (so the bar chart has consistent layout)
    for i in range(7):
        d = (datetime.now(timezone.utc) - timedelta(days=6 - i)).strftime("%Y-%m-%d")
        total, ok = by_day.get(d, (0, 0))
        days.append({
            "day": d,
            "weekday": (datetime.now(timezone.utc) - timedelta(days=6 - i)).strftime("%a"),
            "total": total,
            "ok": ok,
            "rate": int(100.0 * ok / total) if total else None,
        })
    return jsonify({"days": days})


@bp.route("/api/freeai/status")
def api_freeai_status():
    """V37: Status der keyless Cloud-Basen (Rotation/Cooldown) fürs Dashboard."""
    try:
        return jsonify(ok=True, bases=_nc_freeai.bases_status(),
                       model=_ki_modell(),
                       provider=("brain" if os.getenv("AI_PROVIDER","").strip().lower()=="brain"
                                 else "freeai"))
    except Exception as e:
        return jsonify(ok=False, error=str(e)[:200])


@bp.route("/api/public/stats")
def api_public_stats():
    """Live-Abruf derselben sicheren Metriken (Dashboard/Debug)."""
    oeff = _haken("oeffentlich")
    if not oeff:
        return _nicht_bereit(_t("Die oeffentliche Statistik"))
    return jsonify(ok=True, **oeff())


@bp.route("/api/version")
def api_version():
    """v4.0: zentrale Versions-/Changelog-Auskunft für Footer + „Was ist neu"-Panel."""
    data = _nc_version.current()
    return jsonify(ok=True, build=globals().get("BUILD_STAMP", ""),
                   summary=_nc_version.summary_line(),
                   changelog=_nc_version.changelog(), **data)


@bp.route("/api/recording-attempts")
def api_recording_attempts():
    """F19: letzte Aufnahme-Versuche für Dashboard-Stream."""
    rows = get_recent_recording_attempts(limit=50)
    return jsonify([{
        "id": r["id"],
        "username": r["username"],
        "recorder": r["recorder"],
        "started_at": (r["started_at"] or "")[:19].replace("T", " "),
        "ended_at": (r["ended_at"] or "")[:19].replace("T", " ") if r["ended_at"] else None,
        "duration_secs": r["duration_secs"],
        "returncode": r["returncode"],
        "file_size": r["file_size"],
        "outcome": r["outcome"],
        "stderr_tail": (r["stderr_tail"] or "")[-400:] if r["stderr_tail"] else None,
        "error": r["error"],
    } for r in rows])


@bp.route("/api/search")
def api_search():
    q = (request.args.get("q") or "").strip()
    limit = _c().arg_int("limit", 30, 1, 100)
    if len(q) < 2:
        return jsonify(query=q, results={}, total=0,
                       note="query too short (min 2 chars)")
    return jsonify(_nc_suche.universal_search(q, limit))


@bp.route("/api/bookmarks", methods=["GET"])
def api_bookmarks_list():
    rows = get_bookmarked_recordings(100)
    return jsonify(ok=True, bookmarks=[{
        "id": r["id"], "username": r["username"],
        "filename": os.path.basename(r["filepath"] or ""),
        "size_mb": round((r["file_size"] or 0)/1024/1024, 1),
        "duration_secs": r["duration_secs"],
        "created_at": r["created_at"],
        "bookmarked_at": r["bookmarked_at"],
    } for r in rows])


@bp.route("/api/tags")
def api_tags_list():
    return jsonify(ok=True, tags=get_all_tags_with_counts())


@bp.route("/api/forecast/storage")
def api_forecast_storage():
    return jsonify(ok=True, **_nc_storage_forecast())


@bp.route("/api/bandwidth/live")
def api_bandwidth_live():
    streams = _nc_band.messen()
    total_kbps = round(sum(s["rate_kbps"] for s in streams), 1)
    _durchsatz = _haken("netzdurchsatz")
    net_kbps = _durchsatz() if _durchsatz else None
    return jsonify(ok=True, streams=streams, total_kbps=total_kbps,
                   net_kbps=net_kbps, count=len(streams))


@bp.route("/api/heatmap/recordings")
def api_heatmap_recordings():
    return jsonify(ok=True, **get_recordings_heatmap())


@bp.route("/api/heatmap/lives/<username>")
def api_heatmap_lives(username):
    username = clean_username(username)
    if not username:
        return jsonify(ok=False, error=_t("ungültiger Benutzername")), 400
    return jsonify(ok=True, username=username, **get_lives_heatmap(username))


@bp.route("/api/activity-pulse")
def api_activity_pulse():
    minutes = _c().arg_int("minutes", 60, 5, 1440)
    return jsonify(ok=True, minutes=minutes, pulse=get_activity_pulse(minutes))


@bp.route("/api/loyalty/leaderboard")
def api_loyalty_leaderboard():
    """V37-LOYALTY: Top-Stammzuschauer nach Punkten, mit Rang."""
    try:
        n = _c().arg_int("n", 10, 1, 50)
    except ValueError:
        n = 10
    try:
        return jsonify(ok=True, enabled=_loyalty.enabled(),
                       leaderboard=_loyalty.leaderboard(n),
                       ranks=_loyalty.status()["ranks"])
    except Exception as e:
        return jsonify(ok=False, error=str(e)), 500


@bp.route("/api/community/stats")
def api_community_stats():
    """V37-COMMUNITY: Wiedererkennungs-Stats + welche Loop-Teile aktiv sind."""
    try:
        st = _community.seen_stats()
        return jsonify(ok=True, known=st["known"], regulars=st["regulars"],
                       returning=_community.returning_enabled(),
                       live_ping=_community.live_ping_enabled(),
                       highlight_share=_community.highlight_share_enabled())
    except Exception as e:
        return jsonify(ok=False, error=str(e)), 500


@bp.route("/api/shield/stats")
def api_shield_stats():
    """V37-W-CTRL: Was SENTINEL-SHIELD in 24h abgewehrt hat — Doxxing/Hate/
    Drohungen aus dem Moderations-Log, für das AZRAEL-Panel."""
    since = (datetime.now(timezone.utc) - timedelta(days=1)).isoformat()
    by_cat, recent, total = {}, [], 0
    try:
        with db_conn() as conn:
            rows = conn.execute(
                "SELECT ts, actor, content, meta FROM kick_mod_log "
                "WHERE actor='sentinel-shield' AND ts>=? ORDER BY ts DESC LIMIT 200",
                (since,)).fetchall()
        for r in rows:
            total += 1
            try:
                m = json.loads(r["meta"] or "{}")
            except Exception:
                m = {}
            cat = m.get("cat") or (m.get("reason", "").split(":")[0].replace("🛑", "").strip()) or "?"
            by_cat[cat] = by_cat.get(cat, 0) + 1
            if len(recent) < 12:
                recent.append({"ts": r["ts"], "cat": cat,
                               "what": m.get("what", ""),
                               "text": (r["content"] or "")[:80]})
    except Exception as e:
        return jsonify(ok=False, error=str(e))
    return jsonify(ok=True, total_24h=total, by_cat=by_cat, recent=recent)


@bp.route("/api/highlights")
def api_highlights():
    """v4.0-W22: erkannte Highlight-Momente + aktuelle Chat-Lage."""
    cfg = _nc_cfgnorm.normalize_highlights(_cfg_get("highlights", None))
    hits = list(_nc_highlights.zustand().get("hits") or [])[-40:]
    return jsonify(ok=True, enabled=cfg["enabled"], min_score=cfg["min_score"],
                   now=time.time(),
                   rate=round(len(_nc_highlights.zustand().get("events") or []) / 20.0 * 60.0, 1),
                   base=round(len(_nc_highlights.zustand().get("base") or []) / 600.0 * 60.0, 1),
                   count=len(hits), items=list(reversed(hits)))


@bp.route("/api/data/export")
def api_data_export():
    """Exportiert Daten als CSV oder JSON. ?kind=recordings|streamers|attempts&format=csv|json"""
    kind = (request.args.get("kind") or "recordings").lower()
    fmt = (request.args.get("format") or "json").lower()
    queries = {
        "recordings": ("SELECT id, username, created_at, file_size, duration_secs, rating, label "
                       "FROM recordings ORDER BY created_at DESC LIMIT 5000"),
        "streamers": ("SELECT id, username, created_at, last_live, paused FROM trackings "
                      "ORDER BY username LIMIT 5000"),
        "attempts": ("SELECT id, username, started_at, outcome, duration_secs, file_size "
                     "FROM recording_attempts ORDER BY started_at DESC LIMIT 5000"),
    }
    if kind not in queries:
        return jsonify(ok=False, error=_t("kind muss recordings, streamers oder attempts sein")), 400
    try:
        with db_conn() as conn:
            rows = [dict(r) for r in conn.execute(queries[kind]).fetchall()]
        if fmt == "csv":
            import csv as _csv
            import io as _io
            buf = _io.StringIO()
            if rows:
                w = _csv.DictWriter(buf, fieldnames=list(rows[0].keys()))
                w.writeheader()
                w.writerows(rows)
            from flask import Response
            return Response(buf.getvalue(), mimetype="text/csv",
                            headers={"Content-Disposition": f"attachment; filename={kind}.csv"})
        return jsonify(ok=True, kind=kind, count=len(rows), rows=rows)
    except Exception as e:
        return jsonify(ok=False, error=str(e)), 500
