"""nc.routes.discord — die Routen unter /api/discord als Flask-Blueprint.

Welle 3 der Zerlegung (siehe docs/MODULARISIERUNG.md), erzeugt mit
tools/bp_extract.py. Pfade stehen woertlich in den Dekoratoren (kein
url_prefix); app-weite Hooks bleiben auf der App; was der Monolith weiterhin
stellen muss, kommt ueber nc.ctx statt ueber einen Import aus bot.py.

v4.1-W16: Die Gruppe kostete vor der Welle acht nc.ctx-Eintraege. Geloest
wurden Wochenstand, Invite und der Verbindungszustand (nc/discordstate.py);
die drei .env-Werte kommen ueber ctx.cfg, das ein Dict ist und keinen Slot
kostet. Aus dem Kontext kommt nur run_async, das es ohnehin schon gab. Neue
Kontext-Eintraege: null.

CLIENT und SESSION sind GETEILTER Zustand: der Supervisor im Bot schreibt sie
fort (Reconnects, Fehlergrund, Verbindungszeitpunkt), diese Routen lesen sie.
Eine zweite Kopie, und das Panel meldete "nie verbunden", waehrend der Bot
seit Stunden im Server sitzt. Der CLIENT steht dabei in einem REGISTER und
nicht als Alias, weil der Bot den Namen neu bindet — ein Alias zeigte nach dem
ersten Reconnect auf den alten Client.
"""

from datetime import datetime, timedelta, timezone

from flask import Blueprint, jsonify, request

from nc import discordstate as _nc_discordstate
from nc.cfgstore import get as _cfg_get
from nc.dbwrap import db_conn
from nc.discordstate import SESSION as _DISCORD_SESSION
from nc.discordstate import invite as _discord_invite
from nc.discordstate import state_get as _disc_state_get
from nc.util import _loop_not_ready

from nc import ctx as _ctx

bp = Blueprint("discord", __name__)


def _c():
    """Laufzeitkontext. Aufruf statt Modul-Konstante — der Kontext wird erst
       beim Bot-Start gefuellt."""
    return _ctx.get()


@bp.route("/api/discord/overview")
def api_discord_overview():
    """F81: Discord-Status + Community-Daten fürs Dashboard. Liest NUR
       sync-sichere Client-Attribute (is_ready/user/guilds/member_count sind
       gecachte Properties, kein await) + DB-Tabellen. Bewusst KEIN
       run_coroutine_threadsafe → kann den Bot-Loop nicht blockieren."""
    out = {"ok": True, "connected": False, "bot": None, "guild": None,
           "members": None, "trackings_discord": 0, "xp_top": [],
           "warns": [], "clips_7d": 0, "digest_week": None, "cotw_week": None}
    # B120: Session-Telemetrie mitliefern, damit das Dashboard einen
    # stillen Gateway-Abriss anzeigen kann statt nur "connected: false".
    out["session"] = dict(_DISCORD_SESSION)
    c = _nc_discordstate.CLIENT["obj"]
    guild = None
    try:
        if c is not None and c.is_ready():
            out["connected"] = True
            out["bot"] = str(c.user)
            if c.guilds:
                guild = c.guilds[0]
                out["guild"] = guild.name
                out["members"] = guild.member_count
    except Exception:
        pass

    def _dname(uid):
        # User-ID → Anzeigename aus dem Guild-Cache (sync); Fallback: nackte ID
        try:
            if guild is not None:
                m = guild.get_member(int(uid))
                if m:
                    return m.display_name
        except Exception:
            pass
        return str(uid)

    try:
        with db_conn() as conn:
            if _c().cfg["DISCORD_GUILD_ID"]:
                r = conn.execute("SELECT COUNT(*) AS c FROM trackings WHERE group_id=?",
                                 (_c().cfg["DISCORD_GUILD_ID"],)).fetchone()
                out["trackings_discord"] = r["c"] if r else 0
            # B65: Auf die konfigurierte Guild filtern — sonst mischen sich bei
            # Guild-Wechsel (alte Test-Server) fremde XP/Warns in die Anzeige.
            # (?=0 OR …) = Filter aus, wenn keine Guild konfiguriert.
            out["xp_top"] = [{"name": _dname(r["user_id"]), "xp": r["xp"], "level": r["level"]}
                             for r in conn.execute(
                                 "SELECT user_id, xp, level FROM discord_xp "
                                 "WHERE (?=0 OR guild_id=?) "
                                 "ORDER BY xp DESC LIMIT 10",
                                 (_c().cfg["DISCORD_GUILD_ID"], _c().cfg["DISCORD_GUILD_ID"])).fetchall()]
            out["warns"] = [{"name": _dname(r["user_id"]), "reason": r["reason"] or "",
                             "moderator": r["moderator"] or "",
                             "at": (r["created_at"] or "")[:16].replace("T", " ")}
                            for r in conn.execute(
                                "SELECT user_id, moderator, reason, created_at FROM discord_warns "
                                "WHERE (?=0 OR guild_id=?) "
                                "ORDER BY id DESC LIMIT 10",
                                (_c().cfg["DISCORD_GUILD_ID"], _c().cfg["DISCORD_GUILD_ID"])).fetchall()]
            since = (datetime.now(timezone.utc) - timedelta(days=7)).isoformat()
            r = conn.execute("SELECT COUNT(*) AS c FROM discord_clips WHERE created_at >= ?",
                             (since,)).fetchone()
            out["clips_7d"] = r["c"] if r else 0
    except Exception as e:
        out["db_error"] = str(e)
    try:
        out["digest_week"] = _disc_state_get("digest_week")
        out["cotw_week"] = _disc_state_get("cotw_week")
    except Exception:
        pass
    return jsonify(out)


@bp.route("/api/discord/webhook_test", methods=["POST"])
def api_discord_webhook_test():
    """Testet den Discord-Webhook mit einer Testnachricht."""
    if not _c().cfg["DISCORD_WEBHOOK_URL"]:
        return jsonify(ok=False, error="Kein DISCORD_WEBHOOK_URL konfiguriert"), 400

    async def _send():
        import aiohttp
        to = aiohttp.ClientTimeout(total=10)
        async with aiohttp.ClientSession(timeout=to) as sx:
            async with sx.post(_c().cfg["DISCORD_WEBHOOK_URL"],
                               json={"content": "✅ Webhook-Test von NIGHTCRAWLER — Verbindung ok."}) as r:
                return r.status
    try:
        status = _c().run_async(_send(), timeout=15)
        return jsonify(ok=(status in (200, 204)), status=status)
    except RuntimeError as e:
        if _loop_not_ready(e):
            return jsonify(ok=False, error="Bot-Loop startet noch", transient=True), 503
        return jsonify(ok=False, error=str(e)), 500
    except Exception as e:
        return jsonify(ok=False, error=str(e)), 500


@bp.route("/api/discord/invite")
def api_discord_invite():
    """v4.0-W35: liefert den dauerhaften Community-Invite für die Website. Quelle
       ist der einmalig erzeugte (oder in .env gesetzte) Link — nie ein neuer."""
    url = _discord_invite()
    return jsonify(ok=bool(url), invite=url,
                   source=("app_config" if (_cfg_get("discord.invite_url", "") or "").strip()
                           else ("env" if url else "none")))


@bp.route("/api/discord/clips_week")
def api_discord_clips_week():
    wk = (datetime.now(timezone.utc) - timedelta(days=7)).isoformat()
    try:
        with db_conn() as conn:
            rows = conn.execute("SELECT username, stars_pushed, created_at FROM discord_clips "
                                "WHERE guild_id=? AND created_at>=? "
                                "ORDER BY stars_pushed DESC, id DESC LIMIT 12",
                                (_c().cfg["DISCORD_GUILD_ID"], wk)).fetchall()
        clips = [{"username": r["username"] or "?", "highlighted": bool(r["stars_pushed"]),
                  "at": (r["created_at"] or "")[:16].replace("T", " ")} for r in rows]
        return jsonify(ok=True, clips=clips,
                       highlighted=sum(1 for c in clips if c["highlighted"]),
                       total=len(clips), threshold=_c().cfg["CLIP_HIGHLIGHT_STARS"])
    except Exception as e:
        return jsonify(ok=False, error=str(e)), 500


@bp.route("/api/discord/community")
def api_discord_community():
    """Reichhaltige Community-Statistik: Level-Verteilung, XP, Clips, Warns —
       gefiltert auf die eigene Guild."""
    gid = _c().cfg["DISCORD_GUILD_ID"]
    out = {"ok": True, "levels": [], "xp_total": 0, "members_ranked": 0,
           "clips_week": 0, "clips_total": 0, "warns_week": 0, "warns_total": 0,
           "top_clippers": [], "top_members": []}
    try:
        wk = (datetime.now(timezone.utc) - timedelta(days=7)).isoformat()
        with db_conn() as conn:
            rows = conn.execute("SELECT level, COUNT(*) AS n FROM discord_xp WHERE guild_id=? "
                                "GROUP BY level ORDER BY level", (gid,)).fetchall()
            out["levels"] = [{"level": r["level"], "n": r["n"]} for r in rows]
            out["members_ranked"] = sum(r["n"] for r in rows)
            out["xp_total"] = conn.execute("SELECT COALESCE(SUM(xp),0) AS t FROM discord_xp "
                                           "WHERE guild_id=?", (gid,)).fetchone()["t"] or 0
            out["top_members"] = [{"user_id": str(r["user_id"]), "xp": r["xp"], "level": r["level"]}
                                  for r in conn.execute("SELECT user_id, xp, level FROM discord_xp "
                                  "WHERE guild_id=? ORDER BY xp DESC LIMIT 10", (gid,)).fetchall()]
            out["clips_week"] = conn.execute("SELECT COUNT(*) AS c FROM discord_clips "
                                "WHERE guild_id=? AND created_at>=?", (gid, wk)).fetchone()["c"]
            out["clips_total"] = conn.execute("SELECT COUNT(*) AS c FROM discord_clips "
                                "WHERE guild_id=?", (gid,)).fetchone()["c"]
            out["top_clippers"] = [{"username": r["username"], "n": r["n"]}
                                   for r in conn.execute("SELECT username, COUNT(*) AS n FROM discord_clips "
                                   "WHERE guild_id=? AND username IS NOT NULL GROUP BY username "
                                   "ORDER BY n DESC LIMIT 6", (gid,)).fetchall()]
            out["top_clippers_week"] = [{"username": r["username"], "n": r["n"]}
                                        for r in conn.execute("SELECT username, COUNT(*) AS n FROM discord_clips "
                                        "WHERE guild_id=? AND username IS NOT NULL AND created_at>=? GROUP BY username "
                                        "ORDER BY n DESC LIMIT 6", (gid, wk)).fetchall()]
            out["warns_week"] = conn.execute("SELECT COUNT(*) AS c FROM discord_warns "
                                "WHERE guild_id=? AND created_at>=?", (gid, wk)).fetchone()["c"]
            out["warns_total"] = conn.execute("SELECT COUNT(*) AS c FROM discord_warns "
                                "WHERE guild_id=?", (gid,)).fetchone()["c"]
            # F102: Daily-Streaks + kommende Events
            try:
                out["daily_active"] = conn.execute(
                    "SELECT COUNT(*) AS c FROM discord_daily WHERE guild_id=? AND streak>0",
                    (gid,)).fetchone()["c"]
                out["top_streaks"] = [{"user_id": str(r["user_id"]), "streak": r["streak"],
                                       "best": r["best_streak"]}
                    for r in conn.execute("SELECT user_id, streak, best_streak FROM discord_daily "
                    "WHERE guild_id=? ORDER BY streak DESC LIMIT 6", (gid,)).fetchall()]
                out["events"] = [{"title": r["title"], "starts_at": r["starts_at"],
                                  "desc": r["description"]}
                    for r in conn.execute("SELECT title, starts_at, description FROM community_events "
                    "WHERE guild_id=? AND done=0 ORDER BY starts_at LIMIT 8", (gid,)).fetchall()]
            except Exception:
                pass
    except Exception as e:
        out["db_error"] = str(e)
    return jsonify(out)


@bp.route("/api/discord/announce", methods=["POST"])
def api_discord_announce():
    """v37 Feature: Community-Broadcast — Ankündigung aus dem Dashboard an den
       Discord-Webhook posten."""
    if not _c().cfg["DISCORD_WEBHOOK_URL"]:
        return jsonify(ok=False, error="Kein DISCORD_WEBHOOK_URL in der .env konfiguriert"), 400
    d = request.get_json(silent=True) or {}
    text = (d.get("text") or "").strip()[:3000]   # v37: Längen-Cap
    if not text:
        return jsonify(ok=False, error="leere Nachricht"), 400

    async def _send():
        import aiohttp
        content = ("📢 **Ankündigung**\n" + text)[:1900]
        to = aiohttp.ClientTimeout(total=10)
        async with aiohttp.ClientSession(timeout=to) as sx:
            async with sx.post(_c().cfg["DISCORD_WEBHOOK_URL"], json={"content": content}) as r:
                return r.status
    try:
        status = _c().run_async(_send(), timeout=15)
        return jsonify(ok=(status in (200, 204)), status=status)
    except RuntimeError as e:
        if _loop_not_ready(e):
            return jsonify(ok=False, error="Bot-Loop startet noch", transient=True), 503
        return jsonify(ok=False, error=str(e)), 500
    except Exception as e:
        return jsonify(ok=False, error=str(e)), 500
