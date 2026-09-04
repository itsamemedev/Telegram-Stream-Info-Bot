"""nc.routes.trackings — die Routen unter /api/trackings als Flask-Blueprint.

Welle 3 der Zerlegung (siehe docs/MODULARISIERUNG.md), erzeugt mit
tools/bp_extract.py. Pfade stehen woertlich in den Dekoratoren (kein
url_prefix); app-weite Hooks bleiben auf der App; was der Monolith weiterhin
stellen muss, kommt ueber nc.ctx statt ueber einen Import aus bot.py.
"""

from datetime import datetime, timezone
import json
import re
from flask import Blueprint, jsonify, request

from nc import fehlertext as _nc_fehlertext

from nc import i18n as _nc_i18n
from nc.dbwrap import db_conn
import io
import csv as _csv
from nc.envnum import env_int as _env_int
# v4.0-W117: alle Tracking-Zugriffe kommen direkt aus nc.trackingdb. Der
# Extraktor hatte die Bot-Delegationen mit hierher gezogen — eine
# Weiterleitung auf eine Weiterleitung, die nur auseinanderlaufen kann.
from nc.trackingdb import (bulk_add_trackings, get_all_active_trackings,
                          set_tracking_paused, add_tracking_tag,
                          remove_tracking_tag, get_tags_for_tracking,
                          set_tracking_priority, get_tracking_priority)
from nc.notes import set_tracking_notes

from nc import ctx as _ctx

bp = Blueprint("trackings", __name__)


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



def _c():
    """Laufzeitkontext. Aufruf statt Modul-Konstante — der Kontext wird erst
       beim Bot-Start gefuellt."""
    return _ctx.get()


class _LazyLog:
    def __getattr__(self, name):
        return getattr(_c().log, name)


log = _LazyLog()


def quick_restart_tracking(tracking_id: int) -> dict:
    """Setzt den State eines Trackings zurück: cleared backoff,
       early-disconnect, stream-dead, queued sofort für Recheck."""
    info = {"tracking_id": tracking_id, "actions": []}
    try:
        with db_conn() as conn:
            row = conn.execute(
                "SELECT username FROM trackings WHERE id=?",
                (tracking_id,)).fetchone()
        if not row:
            return {"ok": False, "error": _t("Tracking nicht gefunden")}
        username = row["username"]
        info["username"] = username
    except Exception as e:
        return {"ok": False, "error": _fehler_text(e, "trackings")}
    if _c().cfg["_STREAM_DEAD_STREAK"].pop(tracking_id, None):
        info["actions"].append("cleared stream_dead_streak")
    if _c().cfg["_STREAM_DEAD_BACKOFF_UNTIL"].pop(tracking_id, None):
        info["actions"].append("cleared stream_dead_backoff")
    if _c().cfg["_EARLY_DISCONNECT_RETRY"].pop(tracking_id, None):
        info["actions"].append("cleared early_disconnect_retries")
    if _c().cfg["_PENDING_OFFLINE_COUNT"].pop(tracking_id, None):
        _c().cfg["_PENDING_OFFLINE_SINCE"].pop(tracking_id, None)
        info["actions"].append("cleared pending_offline")
    if _c().cfg["_RATE_LIMIT_BACKOFF"].pop(username, None):
        info["actions"].append("cleared rate_limit_backoff")
    if _c().cfg["_RATE_LIMIT_PENALTY"].pop(username, None):
        info["actions"].append("cleared rate_limit_penalty")
    _c().cfg["_LIVE_STATUS_CACHE"].pop(username, None)
    info["actions"].append("flushed live_status_cache")
    _c().cfg["_NEXT_CHECK_AT"][tracking_id] = 0
    info["actions"].append("queued immediate recheck")
    _c().log_event("tracking.restart", "info",
              f"Quick-Restart Tracking #{tracking_id} @{username}",
              {"tracking_id": tracking_id, "username": username,
               "actions": info["actions"]})
    return {"ok": True, **info}


def _dashboard_track_group() -> int:
    """Standardgruppe für Trackings ohne explizite group_id.
       Reihenfolge: DASHBOARD_TRACK_GROUP_ID → DAILY_SUMMARY_CHAT_ID →
       die meistgenutzte group_id aus trackings (dort läuft der Betrieb
       nachweislich) → DISCORD_TRACK_GROUP_ID → DISCORD_GUILD_ID →
       ALLOWED_CHAT_IDS, falls es genau einen gibt. 0 = nicht auflösbar,
       der Aufrufer meldet das mit Klartext statt still zu schlucken.
       Als Funktion gelesen, nicht als Modul-Konstante: .env ist zum
       Import-Zeitpunkt teils noch nicht geladen."""
    gid = _env_int("DASHBOARD_TRACK_GROUP_ID", 0)
    if gid:
        return gid
    if _c().cfg["DAILY_SUMMARY_CHAT_ID"]:
        return _c().cfg["DAILY_SUMMARY_CHAT_ID"]
    try:
        with db_conn() as conn:
            row = conn.execute(
                "SELECT group_id, COUNT(*) AS n FROM trackings "
                "GROUP BY group_id ORDER BY n DESC LIMIT 1").fetchone()
        if row and row["group_id"]:
            return int(row["group_id"])
    except Exception as e:
        log.warning("Standardgruppe fürs Dashboard: DB-Abfrage fehlgeschlagen: %s", e)
    for cand in (_c().cfg["DISCORD_TRACK_GROUP_ID"], _c().cfg["DISCORD_GUILD_ID"]):
        if cand:
            return int(cand)
    if len(_c().cfg["ALLOWED_CHAT_IDS"]) == 1:
        return int(next(iter(_c().cfg["ALLOWED_CHAT_IDS"])))
    return 0


@bp.route("/api/trackings/groups")
def api_trackings_groups():
    """Bekannte Zielgruppen samt Belegung + die aufgelöste Standardgruppe.
       Damit kann das Dashboard eine Auswahl anbieten, statt den Betreiber
       eine Chat-ID tippen zu lassen, die er nirgends ablesen kann."""
    default_gid = _dashboard_track_group()

    def _src(gid: int) -> str:
        return "discord" if (_c().cfg["DISCORD_GUILD_ID"] and gid == _c().cfg["DISCORD_GUILD_ID"]) else "telegram"

    groups = []
    try:
        with db_conn() as conn:
            rows = conn.execute(
                "SELECT group_id, COUNT(*) AS n FROM trackings "
                "GROUP BY group_id ORDER BY n DESC").fetchall()
        for r in rows:
            gid = int(r["group_id"] or 0)
            groups.append({"group_id": gid, "count": r["n"], "source": _src(gid),
                           "default": gid == default_gid})
    except Exception as e:
        return jsonify(ok=False, error=_fehler_text(e, "api_trackings_groups")), 500
    # Die Standardgruppe steht auch dann zur Wahl, wenn dort noch nichts läuft
    # (frische Installation — sonst böte das Dashboard genau nichts an).
    if default_gid and not any(g["group_id"] == default_gid for g in groups):
        groups.insert(0, {"group_id": default_gid, "count": 0,
                          "source": _src(default_gid), "default": True})
    return jsonify(ok=True, groups=groups, default_group_id=default_gid)


@bp.route("/api/trackings/bulk", methods=["POST"])
def api_trackings_bulk():
    """Bulk-add Trackings für einen Chat. Akzeptiert:
       POST { "group_id": <int>, "usernames": ["@user1", "user2", ...] }
       ODER  { "group_id": <int>, "text": "@u1 @u2\nu3 u4" }   (text auto-split)
       Returns: { ok: true, group_id: <int>, added: [...], duplicates: [...],
                  invalid: [...] }

       group_id ist OPTIONAL: fehlt sie (oder ist 0), übernimmt
       _dashboard_track_group() die Auflösung. Vorher war sie Pflicht — das
       Dashboard-Feld blieb leer und der Streamer wurde nie angelegt.

       Limit: max 200 Usernames pro Call (sonst Telegram-Rate-Limit-Probleme
       beim späteren Polling und langes Block des Flask-Workers)."""
    payload = request.get_json(silent=True) or {}
    raw_gid = payload.get("group_id")
    if raw_gid in (None, "", 0, "0"):
        group_id = _dashboard_track_group()
    else:
        try:
            group_id = int(raw_gid)
        except (TypeError, ValueError):
            return jsonify(ok=False, error=_t("group_id muss eine Zahl sein")), 400
    if not group_id:
        return jsonify(ok=False, error=_t("keine Zielgruppe auflösbar — "
                                          "DASHBOARD_TRACK_GROUP_ID (oder DAILY_SUMMARY_CHAT_ID) "
                                          "in .env setzen oder group_id mitgeben")), 400

    # Usernames-Liste aus 'usernames' ODER 'text' bauen
    names = payload.get("usernames")
    if not names:
        text = payload.get("text", "")
        if not isinstance(text, str):
            return jsonify(ok=False, error=_t("text muss ein String sein")), 400
        # F56-Bug-Fix B39: text-Input cappen. Flask MAX_CONTENT_LENGTH ist auf
        # ARCHIVE_MAX_UPLOAD_MB+16 hochgesetzt (für Archive-Uploads — ~2GB
        # default). Ohne hier zu cappen könnte ein User 2GB Text reinpasten →
        # der regex-split würde den Flask-Worker für ein paar Sekunden blocken.
        # 50KB ist mehr als genug für 200 Usernames inkl. Whitespace/Trenner.
        if len(text) > 50_000:
            return jsonify(ok=False,
                           error=_t("text zu groß (max 50KB für Bulk-Add)")), 413
        # F56: Split nach Whitespace, Komma, Newline, Semikolon
        names = [n for n in re.split(r'[\s,;\n]+', text) if n]
    if not isinstance(names, list) or not names:
        return jsonify(ok=False, error=_t("keine usernames angegeben")), 400
    if len(names) > 200:
        return jsonify(ok=False, error=_t("max 200 usernames pro bulk-call")), 400

    # added_by=0 als Dashboard-Marker (analog zu F49)
    result = bulk_add_trackings(group_id, names, added_by=0)

    # F56: Sofort recheck für alle neuen (kein Warten auf nächsten Polling-Tick)
    if result["added"]:
        try:
            with db_conn() as conn:
                rows = conn.execute(
                    "SELECT id FROM trackings WHERE group_id=? AND username IN ("
                    + ",".join("?" * len(result["added"])) + ")",
                    [group_id] + result["added"]
                ).fetchall()
                for r in rows:
                    _c().cfg["_NEXT_CHECK_AT"][r["id"]] = 0
        except Exception as e:
            log.warning(f"bulk_add: sofort-recheck setup failed: {e}")

    return jsonify(ok=True, group_id=group_id, **result,
                   summary={"added": len(result["added"]),
                            "duplicates": len(result["duplicates"]),
                            "invalid": len(result["invalid"]),
                            "quota_exceeded": len(result.get("quota_exceeded", []))})


@bp.route("/api/trackings")
def api_trackings():
    """F53: include_paused=True damit Dashboard alle Trackings sieht
       (mit Pause-Badge). Worker nutzt include_paused=False.
       B54: liefert auch auto_disabled_at + auto_disabled_reason damit das
       Dashboard zwischen 'manuell pausiert' und 'circuit-breaker hit' unterscheidet."""
    rows = get_all_active_trackings(include_paused=True)
    # B63: Quelle mitliefern — Trackings können aus Telegram-Gruppen ODER vom
    # Discord-Server stammen. Ohne Badge sieht der Operator nicht, woher ein
    # Eintrag kommt (und warum er ggf. doppelt existiert). Bei geteilter Liste
    # (DISCORD_TRACK_GROUP_ID=Telegram-ID) ist die Heimat Telegram → kein DC-Badge.
    return jsonify([{
        "id": t["id"], "username": t["username"], "group_id": t["group_id"],
        "source": ("discord" if (_c().cfg["DISCORD_GUILD_ID"] and t["group_id"] == _c().cfg["DISCORD_GUILD_ID"]) else "telegram"),
        "last_live": bool(t["last_live"]), "recording": bool(t["recording"]),
        "paused": bool(t["paused"]) if "paused" in t.keys() else False,    # F53
        "notes": (t["notes"] if "notes" in t.keys() else None) or "",      # F60
        "auto_disabled_at": (t["auto_disabled_at"]
            if "auto_disabled_at" in t.keys() else None) or "",            # B54
        "auto_disabled_reason": (t["auto_disabled_reason"]
            if "auto_disabled_reason" in t.keys() else None) or "",        # B54
        "created_at": t["created_at"][:19] if t["created_at"] else ""
    } for t in rows])


@bp.route("/api/trackings/<int:tracking_id>/notes", methods=["POST"])
def api_tracking_notes(tracking_id):
    """POST {"notes": "..."} — speichert/löscht Notiz. Max 200 Zeichen."""
    payload = request.get_json(silent=True) or {}
    notes = payload.get("notes", "")
    if not isinstance(notes, str):
        return jsonify(ok=False, error=_t("notes muss ein String sein")), 400
    ok = set_tracking_notes(tracking_id, notes)
    if not ok:
        return jsonify(ok=False, error=_t("Tracking nicht gefunden")), 404
    return jsonify(ok=True, tracking_id=tracking_id,
                   notes=notes.strip()[:200])


@bp.route("/api/trackings/export")
def api_trackings_export():
    """GET → text/csv. Alle Trackings inkl. Status, Notes, Chat-IDs.
       Format ist gut für Import in andere Bots oder als Backup."""
    rows = get_all_active_trackings(include_paused=True)
    buf = io.StringIO()
    writer = _csv.writer(buf, quoting=_csv.QUOTE_MINIMAL)
    # Header — Reihenfolge ist die für Re-Import-freundlichste
    writer.writerow(["id", "username", "group_id", "added_by", "created_at",
                     "last_live", "recording", "paused", "notes"])
    for t in rows:
        writer.writerow([
            t["id"],
            t["username"],
            t["group_id"],
            t["added_by"] if "added_by" in t.keys() else "",
            t["created_at"] or "",
            1 if t["last_live"] else 0,
            1 if t["recording"] else 0,
            1 if ("paused" in t.keys() and t["paused"]) else 0,
            (t["notes"] if "notes" in t.keys() else None) or "",
        ])
    csv_text = buf.getvalue()
    # F62: Filename mit Datum damit man bei mehreren Backups durchblickt
    fname = f"trackings_{datetime.now(timezone.utc).strftime('%Y-%m-%d')}.csv"
    return (csv_text, 200, {
        "Content-Type": "text/csv; charset=utf-8",
        "Content-Disposition": f'attachment; filename="{fname}"',
    })


@bp.route("/api/trackings/<int:tracking_id>/pause", methods=["POST"])
def api_tracking_pause(tracking_id):
    """Pausiert ein Tracking — Worker überspringt es bis Resume."""
    ok = set_tracking_paused(tracking_id, True)
    if not ok:
        return jsonify(ok=False, error=_t("Tracking nicht gefunden")), 404
    # F53: Falls gerade aufgenommen wird — laufende Aufnahme NICHT stoppen,
    # nur weitere verhindern. Wer aktiv stoppen will nutzt /cleanup.
    return jsonify(ok=True, paused=True, tracking_id=tracking_id)


@bp.route("/api/trackings/<int:tracking_id>/resume", methods=["POST"])
def api_tracking_resume(tracking_id):
    """Setzt das Tracking wieder aktiv — Worker pollt wieder."""
    ok = set_tracking_paused(tracking_id, False)
    if not ok:
        return jsonify(ok=False, error=_t("Tracking nicht gefunden")), 404
    # F53: Sofort recheck damit man nicht bis zum nächsten regulären Tick wartet
    try:
        _c().cfg["_NEXT_CHECK_AT"][tracking_id] = 0
    except Exception: pass
    return jsonify(ok=True, paused=False, tracking_id=tracking_id)


@bp.route("/api/trackings/<int:tracking_id>/recheck", methods=["POST"])
def api_tracking_recheck(tracking_id):
    """POST. Sofort-Check eines Trackings + Cache-Invalidation."""
    # 1. Tracking existiert?
    with db_conn() as conn:
        row = conn.execute(
            "SELECT username FROM trackings WHERE id=?",
            (tracking_id,)).fetchone()
    if not row:
        return jsonify(ok=False, error=_t("Tracking nicht gefunden")), 404
    username = row["username"]

    # 2. Live-Status-Cache flushen damit der Recheck wirklich frisch ist
    try:
        _c().cfg["_LIVE_STATUS_CACHE"].pop(username, None)
    except Exception:
        pass

    # 3. Rate-Limit-Backoff für diesen User zurücksetzen (er soll JETZT geprüft
    # werden, nicht warten). Vorsicht: falls TikTok wirklich rate-limited, gibt
    # es trotzdem 429 — aber dann setzt sich der Backoff bei der nächsten
    # Antwort eh wieder.
    try:
        _c().cfg["_RATE_LIMIT_BACKOFF"].pop(username, None)
    except Exception:
        pass

    # 4. Schedule sofort für nächsten Loop-Tick (LOOP_TICK = 5s)
    try:
        _c().cfg["_NEXT_CHECK_AT"][tracking_id] = 0
    except Exception:
        pass

    return jsonify(ok=True, message=f"recheck queued für @{username}",
                   username=username, tracking_id=tracking_id)


@bp.route("/api/trackings/tags-map")
def api_trackings_tags_map():
    """BUG-FIX (Perf): Liefert ALLE Tag-Zuordnungen in EINER Query als
       {tracking_id: [tags]}. Vorher hat das Dashboard pro Grid-Zeile einen
       eigenen /tags-Call gemacht → bei 50 Trackings 50 Requests, und das
       alle 8s beim Auto-Refresh + bei jedem Filter-Tastendruck."""
    out = {}
    try:
        with db_conn() as conn:
            rows = conn.execute(
                "SELECT tracking_id, tag FROM tracking_tags ORDER BY tracking_id, tag"
            ).fetchall()
        for r in rows:
            out.setdefault(str(r["tracking_id"]), []).append(r["tag"])
    except Exception as e:
        return jsonify(ok=False, error=_fehler_text(e, "api_trackings_tags_map")), 500
    return jsonify(ok=True, map=out)


@bp.route("/api/trackings/<int:tid>/tags", methods=["GET", "POST", "DELETE"])
def api_tracking_tags(tid):
    if request.method == "GET":
        return jsonify(ok=True, tags=get_tags_for_tracking(tid))
    data = request.get_json(silent=True) or {}
    tag = data.get("tag", "")
    if request.method == "POST":
        ok = add_tracking_tag(tid, tag)
        return jsonify(ok=ok, tags=get_tags_for_tracking(tid))
    # DELETE
    ok = remove_tracking_tag(tid, tag)
    return jsonify(ok=ok, tags=get_tags_for_tracking(tid))


@bp.route("/api/trackings/<int:tid>/priority", methods=["GET", "POST"])
def api_tracking_priority(tid):
    if request.method == "GET":
        return jsonify(ok=True, **get_tracking_priority(tid))
    data = request.get_json(silent=True) or {}
    level = data.get("level", 0)
    custom = data.get("custom_interval")
    ok = set_tracking_priority(tid, level, custom)
    if not ok:
        return jsonify(ok=False, error=_t("Tracking nicht gefunden")), 404
    return jsonify(ok=True, **get_tracking_priority(tid))


@bp.route("/api/trackings/<int:tid>/quick-restart", methods=["POST"])
def api_tracking_quick_restart(tid):
    # quick_restart_tracking ist sync (manipuliert nur in-memory dicts + DB),
    # daher kein async-Bridge nötig.
    result = quick_restart_tracking(tid)
    code = 200 if result.get("ok") else 404
    return jsonify(result), code


@bp.route("/api/trackings/watchlist-export")
def api_watchlist_export():
    try:
        with db_conn() as conn:
            rows = conn.execute(
                "SELECT id, username, group_id, COALESCE(notes,'') AS notes, "
                "  last_live, recording, COALESCE(paused,0) AS paused, created_at "
                "FROM trackings ORDER BY username ASC").fetchall()
        out = []
        for r in rows:
            out.append({
                "username": r["username"],
                "notes": r["notes"],
                "paused": bool(r["paused"]),
                "tags": get_tags_for_tracking(r["id"]),
                "priority": get_tracking_priority(r["id"]),
                "created_at": r["created_at"],
            })
        from flask import Response
        payload = json.dumps({"exported_at": datetime.now(timezone.utc).isoformat(),
                              "count": len(out), "watchlist": out},
                             ensure_ascii=False, indent=2)
        return Response(payload, mimetype="application/json",
                        headers={"Content-Disposition":
                                 "attachment; filename=watchlist.json"})
    except Exception as e:
        return jsonify(ok=False, error=_fehler_text(e, "api_watchlist_export")), 500


@bp.route("/api/trackings/<int:tid>/collection", methods=["POST"])
def api_tracking_collection(tid):
    """Ordnet ein Tracking einer Collection zu (collection_id=null → entkoppeln)."""
    payload = request.get_json(silent=True) or {}
    cid = payload.get("collection_id", None)
    try:
        with db_conn() as conn:
            tr = conn.execute("SELECT 1 FROM trackings WHERE id=?", (tid,)).fetchone()
            if not tr:
                return jsonify(ok=False, error=_t("Tracking nicht gefunden.")), 404
            if cid in (None, 0, "", "null"):
                conn.execute("UPDATE trackings SET collection_id=NULL WHERE id=?", (tid,))
                conn.commit()
                return jsonify(ok=True, tracking_id=tid, collection_id=None)
            try:
                cid = int(cid)
            except (TypeError, ValueError):
                return jsonify(ok=False, error=_t("collection_id ungültig.")), 400
            exists = conn.execute("SELECT 1 FROM tracking_collections WHERE id=?",
                                 (cid,)).fetchone()
            if not exists:
                return jsonify(ok=False, error=_t("Collection existiert nicht.")), 400
            conn.execute("UPDATE trackings SET collection_id=? WHERE id=?", (cid, tid))
            conn.commit()
        return jsonify(ok=True, tracking_id=tid, collection_id=cid)
    except Exception as e:
        return jsonify(ok=False, error=_fehler_text(e, "api_tracking_collection")), 500


@bp.route("/api/trackings/<int:tid>/max-duration", methods=["POST"])
def api_tracking_max_duration(tid):
    """Setzt das Aufnahmedauer-Override (Sekunden) für einen Streamer.
       0/null → Override entfernen (globaler Default greift wieder)."""
    payload = request.get_json(silent=True) or {}
    raw = payload.get("seconds", payload.get("max_duration", None))
    try:
        with db_conn() as conn:
            tr = conn.execute("SELECT 1 FROM trackings WHERE id=?", (tid,)).fetchone()
            if not tr:
                return jsonify(ok=False, error=_t("Tracking nicht gefunden.")), 404
            if raw in (None, 0, "0", "", "null"):
                conn.execute("UPDATE trackings SET max_duration_override=NULL WHERE id=?",
                             (tid,))
                conn.commit()
                return jsonify(ok=True, tracking_id=tid, seconds=None)
            try:
                secs = int(raw)
            except (TypeError, ValueError):
                return jsonify(ok=False, error=_t("seconds muss eine Zahl sein.")), 400
            secs = max(30, min(secs, 86400))     # 30s … 24h Sicherheits-Clamp
            conn.execute("UPDATE trackings SET max_duration_override=? WHERE id=?",
                         (secs, tid))
            conn.commit()
        return jsonify(ok=True, tracking_id=tid, seconds=secs)
    except Exception as e:
        return jsonify(ok=False, error=_fehler_text(e, "api_tracking_max_duration")), 500


@bp.route("/api/trackings/<int:tid>/settings")
def api_tracking_settings(tid):
    """Kombinierte Per-Streamer-Einstellungen (Override, Collection, Tags-Anzahl,
       Notizen-Anzahl, Status) in einem Aufruf."""
    try:
        with db_conn() as conn:
            tr = conn.execute(
                "SELECT id, username, last_live, recording, paused, collection_id, "
                "max_duration_override FROM trackings WHERE id=?", (tid,)).fetchone()
            if not tr:
                return jsonify(ok=False, error=_t("Tracking nicht gefunden.")), 404
            coll_name = None
            if tr["collection_id"]:
                c = conn.execute("SELECT name FROM tracking_collections WHERE id=?",
                                (tr["collection_id"],)).fetchone()
                coll_name = c["name"] if c else None
            try:
                ntags = conn.execute("SELECT COUNT(*) AS n FROM tracking_tags "
                                     "WHERE tracking_id=?", (tid,)).fetchone()["n"]
            except Exception:
                ntags = 0
            try:
                nnotes = conn.execute("SELECT COUNT(*) AS n FROM recording_notes "
                                      "WHERE tracking_id=?", (tid,)).fetchone()["n"]
            except Exception:
                nnotes = 0
        return jsonify(ok=True, tracking_id=tid, username=tr["username"],
                       live=bool(tr["last_live"]), recording=bool(tr["recording"]),
                       paused=bool(tr["paused"]),
                       collection_id=tr["collection_id"], collection=coll_name,
                       max_duration_override=tr["max_duration_override"],
                       effective_duration=(tr["max_duration_override"] or _c().cfg["MAX_RECORD_SECS"]),
                       tag_count=int(ntags or 0), note_count=int(nnotes or 0))
    except Exception as e:
        return jsonify(ok=False, error=_fehler_text(e, "api_tracking_settings")), 500
