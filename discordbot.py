"""discordbot.py — der Discord-Teil, aus dem Monolithen herausgelöst (v4.2-W15).

Warum diese Datei bot-seitig liegt und nicht unter nc/: sie importiert
`discord.py` und baut Slash-Commands. `nc/*` ist bewusst bot-frei und
bibliotheksartig — ein Modul, das ein Gateway aufmacht, gehört dort nicht hin.
Die Grenze, die gilt, ist die andere Richtung: **hier steht kein einziges
`from bot import`.** Alles, was der Monolith beisteuert, kommt durch genau
einen Kanal, `starte(ctx)` mit einem `nc.botctx.BotKontext`.

Warum die Namen unten als Modul-Globale gefüllt werden statt als `ctx.spawn`
im Rumpf: der verschobene Code ist damit ZEICHENGLEICH mit dem, was vorher in
`bot.py` stand. Ein Umschreiben von 1.900 Zeilen auf Attributzugriffe hätte
jede Zeile zu einer möglichen Regression gemacht — bei einem Teil, für den es
hier keinen Gateway und keinen Test gibt, der ihn wirklich ausführt. So ist
der Diff nachprüfbar: verschoben, nicht umgeschrieben.

Warum `bot.py` diese Datei ERST IN main() importiert: die Schalter unten
stehen in `bot.py` als Modul-Konstanten und werden über den Kontext gereicht.
Ein Import am Kopf von `bot.py` würde `starte()` zwar nicht auslösen, aber die
Reihenfolge stillschweigend festschreiben. Der späte Import macht sichtbar,
dass hier nichts läuft, bevor der Bot steht — dieselbe Falle wie bei den
Modul-Konstanten, die `.env` einfrieren (CLAUDE.md).

Es gibt keinen Discord-Gateway in der Entwicklungsumgebung. Prüfbar ist
deshalb die Form: der Importgraph, dass kein Name direkt aus `bot.py` gelesen
wird, und dass `starte()` jeden Platzhalter belegt. Ob ein Slash-Command
antwortet, zeigt erst der Server.
"""

import asyncio
import logging
import os
import re
import time as _time_mod
import types
from datetime import datetime, timedelta, timezone

import nc.community as _community
from nc import azraelstate as _nc_azrael
from nc import badwords as _nc_badwords
from nc import brainstate as _nc_brainstate
from nc import channels as _nc_channels
from nc import discordstate as _nc_discordstate
from nc import i18n as _nc_i18n
from nc import modheuristics as _nc_mod
from nc import trackingdb as _nc_trackingdb
from nc.dbwrap import db_async, db_conn
from nc.logfilters import _DiscordErrorHandler
from nc.shield import _sentinel_screen

# B79-Fix: discord.py wertet Parameter-Annotationen (z.B. `member: discord.Member`)
# zur Command-Registrierung ueber callback.__globals__ aus. Steht der Import nur
# lokal in einer Funktion, ist er dort nicht sichtbar -> NameError beim
# Registrieren, und der GESAMTE Discord-Bot faellt aus.
try:
    import discord as discord   # noqa: F401 — modulweite Sichtbarkeit fuer Annotationen
except Exception:
    discord = None

# Aliase auf nc-Register. Direkt statt ueber den Kontext, weil sie ohnehin
# bot-frei sind und der Bot sie nie neu bindet — ein Kontextfeld waere hier
# nur eine zweite Signatur, an der etwas driften kann.
_load_banned_words_file = _nc_badwords.load_banned
_NEXT_CHECK_AT = _nc_brainstate.NEXT_CHECK_AT
_AI_CALL_TS = _nc_azrael.CALL_TS
_restream_active = _nc_channels.restream_active


# ══════════════════════════════════════════════════════════════════════════
# Vom Bot gefuellt — siehe starte(). Vor dem Aufruf ist hier alles None bzw.
# leer; das ist Absicht: ein Zugriff vor starte() soll krachen und nicht
# stillschweigend einen Default benutzen.
# ══════════════════════════════════════════════════════════════════════════
log = None
_spawn = None
_loop_fehler = None
_modlog = None
_auto_on = None
_cfg_get = None
_cfg_set = None
_discord_notify = None
_discord_post_user = None
_disc_state_get = None
_disc_state_set = None
_whisper_transcribe = None
add_tracking = None
azrael_chat = None
clip_moment = None
_einladung_merken = None
_KICK_MOD = None
_DC_ERR_QUEUE = None
_BOOT_TS = None

# Telegram-Handler, die die sys_*-Slash-Commands mitbenutzen.
pause_tracking = None
resume_tracking = None
stoprec = None
cleanup = None
quota = None
sysres = None
topusers = None
summary_cmd = None
logs_cmd = None
diag = None
aireset = None
teststream = None
bulkadd = None
live = None
cookies_cmd = None

# Konfiguration aus .env — gelesen wird sie ausschliesslich in bot.py.
ALLOWED_CHAT_IDS = None
ALLOWED_USER_IDS = None
AZRAEL_MAX_CALLS_MIN = None
CLIP_DIR = None
CLIP_HIGHLIGHT_STARS = None
CLIP_HIGHLIGHT_TO_TG = None
DB_BACKEND = None
DB_PATH = None
DISCORD_BOT_TOKEN = None
DISCORD_GUILD_ID = None
DISCORD_MODLOG_CHANNEL = None
DISCORD_TRACK_GROUP_ID = None
DISCORD_WEBHOOK_URL = None
KICK_CHANNEL_URL = None
MAX_TRACKINGS_PER_CHAT = None
CLIP_CMD_COOLDOWN_S = None
COMMUNITY_HIGHLIGHT_SHARE_ENABLED = None
DISCORD_ADMIN_ROLE = None
DISCORD_AI_MOD = None
DISCORD_AUTOMOD = None
DISCORD_AUTOMOD_ACTION = None
DISCORD_AZRAEL_REPLY = None
DISCORD_CLIP_OF_WEEK = None
DISCORD_DAILY_STREAK_XP = None
DISCORD_DAILY_XP = None
DISCORD_ERROR_CHANNEL = None
DISCORD_ERROR_PUSH = None
DISCORD_EVENTS_CHANNEL = None
DISCORD_LEVELING = None
DISCORD_LEVELUP_CHANNEL = None
DISCORD_LIVEBOARD = None
DISCORD_TARGET_CAP = None
DISCORD_VOICE_AI = None
DISCORD_WARN_TIMEOUT_MIN = None
DISCORD_WEEKLY_DIGEST = None
DISCORD_XP_LIVE_BOOST = None


def _uebernehmen(ctx):
    """Belegt die Platzhalter oben aus dem Kontext. Genau einmal, beim Start."""
    global log, _spawn, _loop_fehler, _modlog, _auto_on, _cfg_get, _cfg_set, _discord_notify, _discord_post_user, _disc_state_get, _disc_state_set, _whisper_transcribe, add_tracking, azrael_chat, clip_moment, _einladung_merken, _KICK_MOD, _DC_ERR_QUEUE, _BOOT_TS
    global pause_tracking, resume_tracking, stoprec, cleanup, quota, sysres, topusers, summary_cmd, logs_cmd, diag, aireset, teststream, bulkadd, live, cookies_cmd
    global ALLOWED_CHAT_IDS, ALLOWED_USER_IDS, AZRAEL_MAX_CALLS_MIN, CLIP_DIR, CLIP_HIGHLIGHT_STARS, CLIP_HIGHLIGHT_TO_TG, DB_BACKEND, DB_PATH, DISCORD_BOT_TOKEN, DISCORD_GUILD_ID, DISCORD_MODLOG_CHANNEL, DISCORD_TRACK_GROUP_ID, DISCORD_WEBHOOK_URL, KICK_CHANNEL_URL, MAX_TRACKINGS_PER_CHAT, CLIP_CMD_COOLDOWN_S, COMMUNITY_HIGHLIGHT_SHARE_ENABLED, DISCORD_ADMIN_ROLE, DISCORD_AI_MOD, DISCORD_AUTOMOD, DISCORD_AUTOMOD_ACTION, DISCORD_AZRAEL_REPLY, DISCORD_CLIP_OF_WEEK, DISCORD_DAILY_STREAK_XP, DISCORD_DAILY_XP, DISCORD_ERROR_CHANNEL, DISCORD_ERROR_PUSH, DISCORD_EVENTS_CHANNEL, DISCORD_LEVELING, DISCORD_LEVELUP_CHANNEL, DISCORD_LIVEBOARD, DISCORD_TARGET_CAP, DISCORD_VOICE_AI, DISCORD_WARN_TIMEOUT_MIN, DISCORD_WEEKLY_DIGEST, DISCORD_XP_LIVE_BOOST
    log = ctx.log
    _spawn = ctx.spawn
    _loop_fehler = ctx.loop_fehler
    _modlog = ctx.modlog
    _auto_on = ctx.auto_on
    _cfg_get = ctx.cfg_get
    _cfg_set = ctx.cfg_set
    _discord_notify = ctx.discord_notify
    _discord_post_user = ctx.discord_post_user
    _disc_state_get = ctx.disc_state_get
    _disc_state_set = ctx.disc_state_set
    _whisper_transcribe = ctx.whisper_transcribe
    add_tracking = ctx.add_tracking
    azrael_chat = ctx.azrael_chat
    clip_moment = ctx.clip_moment
    _einladung_merken = ctx.einladung_merken
    _KICK_MOD = ctx.kick_mod
    _DC_ERR_QUEUE = ctx.fehler_schlange
    _BOOT_TS = ctx.boot_ts
    pause_tracking = ctx.befehle["pause_tracking"]
    resume_tracking = ctx.befehle["resume_tracking"]
    stoprec = ctx.befehle["stoprec"]
    cleanup = ctx.befehle["cleanup"]
    quota = ctx.befehle["quota"]
    sysres = ctx.befehle["sysres"]
    topusers = ctx.befehle["topusers"]
    summary_cmd = ctx.befehle["summary_cmd"]
    logs_cmd = ctx.befehle["logs_cmd"]
    diag = ctx.befehle["diag"]
    aireset = ctx.befehle["aireset"]
    teststream = ctx.befehle["teststream"]
    bulkadd = ctx.befehle["bulkadd"]
    live = ctx.befehle["live"]
    cookies_cmd = ctx.befehle["cookies_cmd"]
    ALLOWED_CHAT_IDS = ctx.schalter["ALLOWED_CHAT_IDS"]
    ALLOWED_USER_IDS = ctx.schalter["ALLOWED_USER_IDS"]
    AZRAEL_MAX_CALLS_MIN = ctx.schalter["AZRAEL_MAX_CALLS_MIN"]
    CLIP_DIR = ctx.schalter["CLIP_DIR"]
    CLIP_HIGHLIGHT_STARS = ctx.schalter["CLIP_HIGHLIGHT_STARS"]
    CLIP_HIGHLIGHT_TO_TG = ctx.schalter["CLIP_HIGHLIGHT_TO_TG"]
    DB_BACKEND = ctx.schalter["DB_BACKEND"]
    DB_PATH = ctx.schalter["DB_PATH"]
    DISCORD_BOT_TOKEN = ctx.schalter["DISCORD_BOT_TOKEN"]
    DISCORD_GUILD_ID = ctx.schalter["DISCORD_GUILD_ID"]
    DISCORD_MODLOG_CHANNEL = ctx.schalter["DISCORD_MODLOG_CHANNEL"]
    DISCORD_TRACK_GROUP_ID = ctx.schalter["DISCORD_TRACK_GROUP_ID"]
    DISCORD_WEBHOOK_URL = ctx.schalter["DISCORD_WEBHOOK_URL"]
    KICK_CHANNEL_URL = ctx.schalter["KICK_CHANNEL_URL"]
    MAX_TRACKINGS_PER_CHAT = ctx.schalter["MAX_TRACKINGS_PER_CHAT"]
    CLIP_CMD_COOLDOWN_S = ctx.schalter["CLIP_CMD_COOLDOWN_S"]
    COMMUNITY_HIGHLIGHT_SHARE_ENABLED = ctx.schalter["COMMUNITY_HIGHLIGHT_SHARE_ENABLED"]
    DISCORD_ADMIN_ROLE = ctx.schalter["DISCORD_ADMIN_ROLE"]
    DISCORD_AI_MOD = ctx.schalter["DISCORD_AI_MOD"]
    DISCORD_AUTOMOD = ctx.schalter["DISCORD_AUTOMOD"]
    DISCORD_AUTOMOD_ACTION = ctx.schalter["DISCORD_AUTOMOD_ACTION"]
    DISCORD_AZRAEL_REPLY = ctx.schalter["DISCORD_AZRAEL_REPLY"]
    DISCORD_CLIP_OF_WEEK = ctx.schalter["DISCORD_CLIP_OF_WEEK"]
    DISCORD_DAILY_STREAK_XP = ctx.schalter["DISCORD_DAILY_STREAK_XP"]
    DISCORD_DAILY_XP = ctx.schalter["DISCORD_DAILY_XP"]
    DISCORD_ERROR_CHANNEL = ctx.schalter["DISCORD_ERROR_CHANNEL"]
    DISCORD_ERROR_PUSH = ctx.schalter["DISCORD_ERROR_PUSH"]
    DISCORD_EVENTS_CHANNEL = ctx.schalter["DISCORD_EVENTS_CHANNEL"]
    DISCORD_LEVELING = ctx.schalter["DISCORD_LEVELING"]
    DISCORD_LEVELUP_CHANNEL = ctx.schalter["DISCORD_LEVELUP_CHANNEL"]
    DISCORD_LIVEBOARD = ctx.schalter["DISCORD_LIVEBOARD"]
    DISCORD_TARGET_CAP = ctx.schalter["DISCORD_TARGET_CAP"]
    DISCORD_VOICE_AI = ctx.schalter["DISCORD_VOICE_AI"]
    DISCORD_WARN_TIMEOUT_MIN = ctx.schalter["DISCORD_WARN_TIMEOUT_MIN"]
    DISCORD_WEEKLY_DIGEST = ctx.schalter["DISCORD_WEEKLY_DIGEST"]
    DISCORD_XP_LIVE_BOOST = ctx.schalter["DISCORD_XP_LIVE_BOOST"]


async def starte(ctx):
    """Der EINE Einstieg. Uebernimmt den Kontext und haelt die Session am Leben."""
    _uebernehmen(ctx)
    await _discord_start()


# B120: Hintergrund-Loops einmalig ueber ALLE Sessions hinweg. Der alte
# Guard hing als Attribut am client-Objekt; nach einem Reconnect gibt es
# ein NEUES client-Objekt, der Guard war leer und jede Session startete
# _liveboard_loop/_weekly_digest_loop/... erneut. Bei n Reconnects liefen
# n parallele Endlosschleifen gegen dieselben Channels.
_DISCORD_BGTASKS_STARTED = False
# v4.1-W16: dasselbe Dict wie in nc/discordstate.py — der Supervisor hier
# schreibt es fort, die Route liest es. Eine zweite Kopie, und das Panel
# meldete "nie verbunden", waehrend der Bot seit Stunden im Server sitzt.
_DISCORD_SESSION = _nc_discordstate.SESSION


async def _discord_start():
    """B120-Supervisor: haelt den Discord-Client dauerhaft am Leben.

    VORHER stand hier ein einziges `await client.start(TOKEN)` in einem
    try/except, das die Exception nur als WARNING loggte. Riss die
    Gateway-Verbindung endgueltig ab (ConnectionClosed mit nicht
    wiederaufnehmbarem Code, GatewayNotFound, DNS-Aussetzer beim
    Reconnect, abgelaufene Session), endete die Coroutine — und Discord
    blieb bis zum KOMPLETTEN Bot-Neustart tot, waehrend Recording,
    Restream und Telegram munter weiterliefen. Genau dieses Bild:
    "Discord-Funktionen gehen nicht mehr", ohne eine einzige Zeile im
    Fehlerlog (WARNING taucht in einem ERROR-Log nicht auf).

    Jetzt: Exponentielles Backoff 5s -> 300s, unbegrenzte Versuche.
    Konfigurationsfehler (kein Token, Token ungueltig, privilegierte
    Intents nicht aktiviert, discord.py fehlt) werden davon
    ausgenommen — die heilt kein Retry, die brauchen den Operator.
    """
    delay = 5
    never_connected = 0      # Fehlversuche, die on_ready NIE erreicht haben
    while True:
        _DISCORD_SESSION["attempt"] += 1
        _reached_ready = False
        try:
            fatal = await _discord_run_once()
            if fatal:
                return                      # Konfigfehler: Retry sinnlos
            reason = "Gateway-Verbindung beendet"
        except asyncio.CancelledError:
            raise                           # Shutdown: nicht abfangen
        except Exception as e:
            reason = f"{type(e).__name__}: {e}"
            log.error("Discord-Session abgebrochen (%s) — Neuversuch in %ss",
                      reason, delay, exc_info=True)
        else:
            log.warning("Discord-Session beendet (%s) — Neuversuch in %ss",
                        reason, delay)
        _reached_ready = bool(_DISCORD_SESSION.get("connected_since"))
        _DISCORD_SESSION.update(last_error=reason,
                                last_disconnect=_time_mod.time(),
                                connected_since=None)
        _DISCORD_SESSION["reconnects"] += 1
        _nc_discordstate.CLIENT["obj"] = None
        # Kam die Session nie bis on_ready, ist der Fehler deterministisch
        # (kaputte Command-Registrierung, Netzsperre, falsche Guild-ID).
        # Endlos dagegen zu laufen verschleiert das Problem nur, deshalb
        # nach 5 solchen Versuchen laut aufgeben statt leise weiterloopen.
        if _reached_ready:
            never_connected = 0
            delay = 5                       # nach echter Session neu starten
        else:
            never_connected += 1
            if never_connected >= 5:
                log.error("Discord: 5 Startversuche ohne eine einzige "
                          "erfolgreiche Verbindung — aufgegeben. Letzter "
                          "Grund: %s. Nach Behebung Bot neu starten.", reason)
                return
        await asyncio.sleep(delay)
        delay = min(delay * 2, 300)


async def _ensure_discord_invite(client):
    """v4.0-W35: erzeugt GENAU EINMAL einen nie ablaufenden Discord-Invite und
       legt ihn in app_config ab. Danach wird nie wieder ein neuer erzeugt —
       weder bei Reconnect noch bei Neustart (der gespeicherte Wert bleibt).

       max_age=0 → läuft nie ab, max_uses=0 → unbegrenzt, unique=False → falls
       Discord schon einen passenden Invite hat, wird DER wiederverwendet statt
       ein Duplikat anzulegen. Steht bereits einer in .env oder app_config,
       passiert nichts."""
    try:
        if (_cfg_get("discord.invite_url", "") or "").strip():
            return                                   # schon einmal erzeugt → fertig
        if (os.getenv("DISCORD_INVITE_URL", "") or "").strip():
            return                                   # .env-Wert hat Vorrang, nichts erzeugen
        guild = None
        if DISCORD_GUILD_ID:
            guild = client.get_guild(DISCORD_GUILD_ID)
        if guild is None:
            guild = client.guilds[0] if client.guilds else None
        if guild is None:
            log.info("Discord-Invite: Bot in keiner Guild — übersprungen.")
            return
        me = guild.me
        chan = None
        sysc = getattr(guild, "system_channel", None)
        if sysc is not None and sysc.permissions_for(me).create_instant_invite:
            chan = sysc
        else:
            for c in guild.text_channels:
                try:
                    if c.permissions_for(me).create_instant_invite:
                        chan = c
                        break
                except Exception:
                    continue
        if chan is None:
            log.warning("Discord-Invite: KEIN Kanal, in dem der Bot 'Einladung erstellen' darf — "
                        "bitte dem Bot die Berechtigung geben, dann erzeugt er den Invite selbst.")
            return
        invite = await chan.create_invite(
            max_age=0, max_uses=0, unique=False,
            reason="LAFAP: dauerhafter Community-Invite (einmalig)")
        url = invite.url
        _cfg_set("discord.invite_url", url)
        # ANKER GEWANDERT (v4.2-W15, nicht der Vertrag): hier stand
        # `global DISCORD_INVITE_URL` + Zuweisung. In dieser Datei haette das
        # nur die Kopie hier gesetzt — DIE Variable, die der Announcer liest,
        # liegt in bot.py. Der Setzer kommt deshalb durch den Kontext und
        # traegt die "nur wenn noch leer"-Bedingung mit.
        _einladung_merken(url)
        log.info("Discord-Invite EINMALIG erzeugt (nie ablaufend, in app_config gespeichert): %s | "
                 "Für die .env kannst du eintragen: DISCORD_INVITE_URL=%s", url, url)
    except Exception as e:
        log.warning("Discord-Invite konnte nicht erzeugt werden: %s", e)


async def _discord_run_once():
    """EINE Discord-Session. Rueckgabe True = nicht neu versuchen."""
    if not DISCORD_BOT_TOKEN:
        log.info("Discord deaktiviert (kein DISCORD_BOT_TOKEN gesetzt).")
        return True
    try:
        import discord
        from discord import app_commands
    except Exception:
        log.warning("Discord aktiviert, aber discord.py fehlt — 'pip install discord.py'. Discord übersprungen.")
        return True

    # B129: Selbstpruefung VOR dem Login. Die beiden folgenden Intents sind
    # PRIVILEGIERT — sie muessen im Developer Portal ausdruecklich
    # eingeschaltet sein (Applications -> Bot -> Privileged Gateway Intents).
    # Sind sie es nicht, verweigert Discord den Login komplett und KEIN
    # einziger Slash-Command funktioniert. Das ist mit Abstand die haeufigste
    # Ursache fuer "der Bot reagiert auf gar nichts", und der Fehler war
    # bisher nur als generische Exception sichtbar.
    log.info("Discord: fordere privilegierte Intents an (message_content, "
             "members). Falls der Login mit PrivilegedIntentsRequired "
             "scheitert, sind sie im Developer Portal nicht aktiviert.")
    intents = discord.Intents.default()
    intents.message_content = True
    intents.members = True
    try:
        intents.moderation = True
    except Exception:
        pass

    client = discord.Client(intents=intents)
    tree = app_commands.CommandTree(client)

    # v4.1-W7: die Sprache dieses Discord-Benutzers fuer diese Anfrage merken.
    #
    # interaction_check laeuft vor JEDEM Slash-Befehl — das ist der einzige
    # Punkt, an dem man alle 46 erwischt, ohne 46 Dekoratoren anzufassen.
    # discord.py liefert die Sprache als Locale-Objekt ("de", "en-US", …);
    # str() darauf ergibt das Kuerzel, das nc.i18n normalisiert.
    #
    # Der Rueckgabewert MUSS True sein: interaction_check ist eigentlich eine
    # Berechtigungspruefung. Gaebe diese Funktion False oder wuerfe sie, waere
    # jeder Slash-Befehl im Discord tot — die Spracherkennung haette den Bot
    # abgeschaltet. Deshalb faengt sie alles und antwortet immer True.
    async def _disc_sprache_setzen(inter):
        try:
            _nc_i18n.sprache_setzen(str(getattr(inter, "locale", "") or ""))
        except Exception as e:
            log.debug("Spracherkennung (Discord): %s", e)
        return True

    tree.interaction_check = _disc_sprache_setzen

    _nc_discordstate.CLIENT["obj"] = client
    # F96: ERROR-Logs aller Logger (bot, TikTokBot, Flask) in die Discord-Queue.
    # Am ROOT-Logger, damit auch Flask-Exceptions (log_exception) mitkommen.
    if DISCORD_ERROR_PUSH and not getattr(logging.getLogger(), "_nc_errhandler", False):
        _eh = _DiscordErrorHandler(level=logging.ERROR)
        _eh.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(name)s:%(lineno)d %(message)s",
                                           "%d.%m %H:%M:%S"))
        logging.getLogger().addHandler(_eh)
        logging.getLogger()._nc_errhandler = True

    def _is_admin(inter) -> bool:
        """Guild-Admin/Manage-Guild ODER konfigurierte DISCORD_ADMIN_ROLE."""
        try:
            perms = getattr(inter.user, "guild_permissions", None)
            if perms and (perms.administrator or perms.manage_guild):
                return True
            if DISCORD_ADMIN_ROLE and getattr(inter.user, "roles", None):
                return any(r.name == DISCORD_ADMIN_ROLE for r in inter.user.roles)
        except Exception:
            pass
        return False

    async def _guard(inter) -> bool:
        if _is_admin(inter):
            return True
        await inter.response.send_message(_nc_i18n.t("⛔ Nur Admins (oder konfigurierte Admin-Rolle)."), ephemeral=True)
        return False

    # ───────── INFO / Telegram-Parität ─────────
    @tree.command(name="status", description=_nc_i18n.t("Azrael Sentinel Status: Trackings, Live, Restream"))
    async def _c_status(inter):
        try:
            with db_conn() as conn:
                at = conn.execute("SELECT COUNT(*) FROM trackings").fetchone()[0]
                ln = conn.execute("SELECT COUNT(*) FROM trackings WHERE last_live=1").fetchone()[0]
                rc = conn.execute("SELECT COUNT(*) FROM recordings WHERE deleted_at IS NULL").fetchone()[0]
            act = _restream_active()
            rs = ("@" + str(act["user"])) if act.get("user") else "— inaktiv"
            await inter.response.send_message(
                _nc_i18n.t(f"**Azrael Sentinel**\n• Trackings: `{at}`   • Live: `{ln}`   • Recordings: `{rc}`\n• Restream: `{rs}`"))
        except Exception as e:
            await inter.response.send_message(_nc_i18n.t(f"Fehler: {e}"), ephemeral=True)

    @tree.command(name="tracklist", description=_nc_i18n.t("Getrackte TikTok-User dieses Servers"))
    async def _c_tracklist(inter):
        gid = DISCORD_TRACK_GROUP_ID or (inter.guild_id or 0)   # B63: Schalter wurde ignoriert
        try:
            with db_conn() as conn:
                rows = conn.execute("SELECT username, last_live FROM trackings WHERE group_id=? "
                                    "ORDER BY username", (gid,)).fetchall()
            if not rows:
                await inter.response.send_message(_nc_i18n.t("Keine Trackings auf diesem Server. `/track <user>`"), ephemeral=True)
                return
            lines = [("🔴 " if r["last_live"] else "⚪ ") + "@" + r["username"] for r in rows]
            await inter.response.send_message(_nc_i18n.t("**Trackings**\n" + "\n".join(lines[:50])))
        except Exception as e:
            await inter.response.send_message(_nc_i18n.t(f"Fehler: {e}"), ephemeral=True)

    @tree.command(name="track", description=_nc_i18n.t("TikTok-User tracken"))
    @app_commands.describe(username="TikTok-Username (ohne @)")
    async def _c_track(inter, username: str):
        gid = DISCORD_TRACK_GROUP_ID or (inter.guild_id or 0)   # B63: Schalter wurde ignoriert
        u = username.strip().lstrip("@")
        if not u:
            await inter.response.send_message(_nc_i18n.t("Username fehlt."), ephemeral=True)
            return
        try:
            ok = await asyncio.to_thread(add_tracking, gid, u, inter.user.id)
            if ok:
                with db_conn() as conn:
                    row = conn.execute("SELECT id FROM trackings WHERE group_id=? AND username=?",
                                       (gid, u)).fetchone()
                if row:
                    _NEXT_CHECK_AT[row["id"]] = 0   # sofort prüfen statt aufs Intervall warten
                await inter.response.send_message(_nc_i18n.t(f"✅ Tracke @{u} — erster Check läuft."))
            else:
                # B63: Ehrliches Feedback — 'schon getrackt' stimmte nur bei Duplikat
                # in DIESER Gruppe. Quota-Ablehnung sah identisch aus → User glaubte
                # das Tracking existiert, obwohl nie eins angelegt wurde.
                with db_conn() as conn:
                    here = conn.execute("SELECT 1 FROM trackings WHERE group_id=? AND username=?",
                                        (gid, u)).fetchone()
                if here:
                    await inter.response.send_message(_nc_i18n.t(f"ℹ @{u} ist hier schon getrackt."))
                else:
                    await inter.response.send_message(
                        f"⛔ @{u} NICHT angelegt — Tracking-Limit erreicht "
                        f"(MAX_TRACKINGS_PER_CHAT={MAX_TRACKINGS_PER_CHAT}).", ephemeral=True)
        except Exception as e:
            await inter.response.send_message(_nc_i18n.t(f"Fehler: {e}"), ephemeral=True)

    @tree.command(name="untrack", description=_nc_i18n.t("TikTok-User nicht mehr tracken"))
    @app_commands.describe(username="TikTok-Username (ohne @)")
    async def _c_untrack(inter, username: str):
        gid = DISCORD_TRACK_GROUP_ID or (inter.guild_id or 0)   # B63: Schalter wurde ignoriert
        u = username.strip().lstrip("@")
        try:
            await asyncio.to_thread(_nc_trackingdb.remove_tracking, gid, u)
            await inter.response.send_message(_nc_i18n.t(f"🗑 @{u} wird nicht mehr getrackt"))
        except Exception as e:
            await inter.response.send_message(_nc_i18n.t(f"Fehler: {e}"), ephemeral=True)

    @tree.command(name="ai", description=_nc_i18n.t("AZRAEL / KI fragen (Text oder Sprachnachricht)"))
    @app_commands.describe(prompt="Deine Frage")
    async def _c_ai(inter, prompt: str):
        await inter.response.defer()
        try:
            content, err = await azrael_chat("Discord /ai", prompt, timeout=30)   # F90: eine KI-Identität
            if err == "budget":
                await inter.followup.send(_nc_i18n.t("⏳ AZRAEL ist gerade ausgelastet — gleich nochmal."))
            elif err or not content:
                await inter.followup.send(_nc_i18n.t(f"KI nicht verfügbar ({err or 'leer'})."))
            else:
                await inter.followup.send(_nc_i18n.t(content[:1900]))
        except Exception as e:
            await inter.followup.send(_nc_i18n.t(f"Fehler: {e}"))

    @tree.command(name="restream_status", description=_nc_i18n.t("Restream-Status"))
    async def _c_restream_status(inter):
        act = _restream_active()
        await inter.response.send_message(_nc_i18n.t("Restream: " + (("@" + str(act["user"])) if act.get("user") else "— inaktiv")))

    # ───────── SERVER-VERWALTUNG (Admin) ─────────
    @tree.command(name="create_channel", description=_nc_i18n.t("Text-Channel anlegen (optional in Kategorie)"))
    @app_commands.describe(name="Channel-Name", category="optional: Kategorie-Name (wird angelegt falls neu)")
    async def _c_create_channel(inter, name: str, category: str = None):
        if not await _guard(inter):
            return
        try:
            cat = None
            if category:
                cat = discord.utils.get(inter.guild.categories, name=category) or \
                    await inter.guild.create_category(category)
            ch = await inter.guild.create_text_channel(name, category=cat)
            await inter.response.send_message(f"✅ Channel {ch.mention} angelegt"
                                              + (f" in **{cat.name}**" if cat else ""))
        except Exception as e:
            await inter.response.send_message(_nc_i18n.t(f"Fehler: {e}"), ephemeral=True)

    @tree.command(name="create_voice", description=_nc_i18n.t("Voice-Channel anlegen"))
    @app_commands.describe(name="Name", category="optional: Kategorie")
    async def _c_create_voice(inter, name: str, category: str = None):
        if not await _guard(inter):
            return
        try:
            cat = None
            if category:
                cat = discord.utils.get(inter.guild.categories, name=category) or \
                    await inter.guild.create_category(category)
            ch = await inter.guild.create_voice_channel(name, category=cat)
            await inter.response.send_message(_nc_i18n.t(f"✅ Voice-Channel **{ch.name}** angelegt"))
        except Exception as e:
            await inter.response.send_message(_nc_i18n.t(f"Fehler: {e}"), ephemeral=True)

    @tree.command(name="create_category", description=_nc_i18n.t("Kategorie anlegen"))
    @app_commands.describe(name="Kategorie-Name")
    async def _c_create_category(inter, name: str):
        if not await _guard(inter):
            return
        try:
            cat = await inter.guild.create_category(name)
            await inter.response.send_message(_nc_i18n.t(f"✅ Kategorie **{cat.name}** angelegt"))
        except Exception as e:
            await inter.response.send_message(_nc_i18n.t(f"Fehler: {e}"), ephemeral=True)

    @tree.command(name="create_role", description=_nc_i18n.t("Rolle / Nutzergruppe anlegen"))
    @app_commands.describe(name="Rollenname", color="optional: Hex (z.B. 00ff9c)", mentionable="erwähnbar?")
    async def _c_create_role(inter, name: str, color: str = None, mentionable: bool = True):
        if not await _guard(inter):
            return
        try:
            kwargs = {"name": name, "mentionable": mentionable}
            if color:
                try:
                    kwargs["colour"] = discord.Colour(int(color.lstrip("#"), 16))
                except Exception:
                    pass
            role = await inter.guild.create_role(**kwargs)
            await inter.response.send_message(_nc_i18n.t(f"✅ Rolle {role.mention} angelegt"))
        except Exception as e:
            await inter.response.send_message(_nc_i18n.t(f"Fehler: {e}"), ephemeral=True)

    @tree.command(name="create_group", description=_nc_i18n.t("Nutzergruppe (= Rolle) anlegen"))
    @app_commands.describe(name="Gruppenname")
    async def _c_create_group(inter, name: str):
        if not await _guard(inter):
            return
        try:
            role = await inter.guild.create_role(name=name, mentionable=True)
            await inter.response.send_message(_nc_i18n.t(f"✅ Gruppe {role.mention} angelegt"))
        except Exception as e:
            await inter.response.send_message(_nc_i18n.t(f"Fehler: {e}"), ephemeral=True)

    @tree.command(name="assign_role", description=_nc_i18n.t("Rolle/Gruppe einem Mitglied geben"))
    @app_commands.describe(member="Mitglied", role="Rolle/Gruppe")
    async def _c_assign_role(inter, member: discord.Member, role: discord.Role):
        if not await _guard(inter):
            return
        try:
            await member.add_roles(role)
            await inter.response.send_message(_nc_i18n.t(f"✅ {member.mention} → {role.mention}"))
        except Exception as e:
            await inter.response.send_message(_nc_i18n.t(f"Fehler: {e}"), ephemeral=True)

    @tree.command(name="remove_role", description=_nc_i18n.t("Rolle/Gruppe entfernen"))
    @app_commands.describe(member="Mitglied", role="Rolle/Gruppe")
    async def _c_remove_role(inter, member: discord.Member, role: discord.Role):
        if not await _guard(inter):
            return
        try:
            await member.remove_roles(role)
            await inter.response.send_message(_nc_i18n.t(f"✅ {role.mention} von {member.mention} entfernt"))
        except Exception as e:
            await inter.response.send_message(_nc_i18n.t(f"Fehler: {e}"), ephemeral=True)

    @tree.command(name="set_channel_perms", description=_nc_i18n.t("Rechte einer Rolle für einen Channel setzen"))
    @app_commands.describe(channel="Channel", role="Rolle", view="ansehen", send="schreiben")
    async def _c_set_perms(inter, channel: discord.TextChannel, role: discord.Role,
                           view: bool = True, send: bool = True):
        if not await _guard(inter):
            return
        try:
            await channel.set_permissions(role, view_channel=view, send_messages=send)
            await inter.response.send_message(
                _nc_i18n.t(f"✅ {role.mention} in {channel.mention}: ansehen={view}, schreiben={send}"))
        except Exception as e:
            await inter.response.send_message(_nc_i18n.t(f"Fehler: {e}"), ephemeral=True)

    @tree.command(name="kick", description=_nc_i18n.t("Mitglied kicken"))
    @app_commands.describe(member="Mitglied", reason="Grund (optional)")
    async def _c_kick(inter, member: discord.Member, reason: str = None):
        if not await _guard(inter):
            return
        try:
            await member.kick(reason=reason)
            await inter.response.send_message(_nc_i18n.t(f"👢 {member} gekickt" + (f" — {reason}" if reason else "")))
        except Exception as e:
            await inter.response.send_message(_nc_i18n.t(f"Fehler: {e}"), ephemeral=True)

    @tree.command(name="ban", description=_nc_i18n.t("Mitglied bannen"))
    @app_commands.describe(member="Mitglied", reason="Grund (optional)")
    async def _c_ban(inter, member: discord.Member, reason: str = None):
        if not await _guard(inter):
            return
        try:
            await member.ban(reason=reason, delete_message_days=0)
            await inter.response.send_message(_nc_i18n.t(f"🔨 {member} gebannt" + (f" — {reason}" if reason else "")))
        except Exception as e:
            await inter.response.send_message(_nc_i18n.t(f"Fehler: {e}"), ephemeral=True)

    @tree.command(name="timeout", description=_nc_i18n.t("Mitglied stummschalten (Minuten)"))
    @app_commands.describe(member="Mitglied", minutes="Minuten", reason="Grund (optional)")
    async def _c_timeout(inter, member: discord.Member, minutes: int, reason: str = None):
        if not await _guard(inter):
            return
        try:
            import datetime as _dt
            until = _dt.datetime.now(_dt.timezone.utc) + _dt.timedelta(minutes=max(1, minutes))
            await member.timeout(until, reason=reason)
            await inter.response.send_message(_nc_i18n.t(f"🔇 {member} für {minutes} min stummgeschaltet"))
        except Exception as e:
            await inter.response.send_message(_nc_i18n.t(f"Fehler: {e}"), ephemeral=True)

    @tree.command(name="purge", description=_nc_i18n.t("Letzte N Nachrichten im Channel löschen (max 100)"))
    @app_commands.describe(count="Anzahl")
    async def _c_purge(inter, count: int):
        if not await _guard(inter):
            return
        try:
            await inter.response.defer(ephemeral=True)
            deleted = await inter.channel.purge(limit=max(1, min(100, count)))
            await inter.followup.send(_nc_i18n.t(f"🧹 {len(deleted)} Nachrichten gelöscht"), ephemeral=True)
        except Exception as e:
            try:
                await inter.followup.send(_nc_i18n.t(f"Fehler: {e}"), ephemeral=True)
            except Exception:
                pass

    # ───────── COMMUNITY-SETUP: Ranking, Channels, Rechte, Target-Channels ─────────
    # Rang-Tiers: (min_level, Rollenname, Farbe). Reihenfolge niedrig→hoch (Cyberpunk).
    RANK_TIERS = [
        (1,  "GHOST",      0x5a6472),
        (3,  "RUNNER",     0x00e5ff),
        (7,  "NETRUNNER",  0x00ff9c),
        (15, "ICEBREAKER", 0xffb000),
        (25, "LEGENDE",    0xff2e88),
    ]

    def _xp_to_level(xp):
        """Level N benötigt 100*N^2 XP (Lvl1=100, 2=400, 3=900 …)."""
        lvl = 0
        while xp >= 100 * (lvl + 1) * (lvl + 1):
            lvl += 1
        return lvl

    def _rank_for_level(lvl):
        name = None
        for need, rname, _c in RANK_TIERS:
            if lvl >= need:
                name = rname
        return name

    def _disc_slug(username):
        s = re.sub(r"[^a-z0-9]+", "-", (username or "").lstrip("@").lower()).strip("-")
        return (s or "user")[:90]

    async def _ensure_rank_roles(guild):
        """Legt fehlende Rang-Rollen an (hoist=sichtbar getrennt). Gibt {name: role}."""
        roles = {}
        for _need, rname, color in RANK_TIERS:
            r = discord.utils.get(guild.roles, name=rname)
            if r is None:
                try:
                    r = await guild.create_role(name=rname, colour=discord.Colour(color),
                                                hoist=True, mentionable=False,
                                                reason="Azrael Sentinel Community-Setup")
                except Exception as e:
                    log.warning("Discord: Rolle %s nicht erstellt: %s", rname, e); continue
            roles[rname] = r
        return roles

    # Funktionale Rollen mit Rechten + Farben (zusätzlich zu den Rang-Rollen).
    # (Name, Farbe, hoist=getrennt anzeigen, {Permission: True})
    TEAM_ROLES = [
        ("👑 Owner",     0xff2e88, True,  {"administrator": True}),
        ("🛡 Moderator", 0xffb000, True,  {"kick_members": True, "ban_members": True,
                                           "manage_messages": True, "moderate_members": True,
                                           "manage_nicknames": True, "mute_members": True,
                                           "deafen_members": True, "move_members": True}),
        ("🎬 Streamer",  0x00ff9c, True,  {"priority_speaker": True, "stream": True}),
        ("⭐ VIP",        0x00e5ff, True,  {}),
        ("🤖 Bot",        0x8892a0, False, {}),
        ("👤 Member",     0x5a6472, False, {}),
    ]

    async def _ensure_team_roles(guild):
        """Legt funktionale Rollen mit Rechten+Farbe an (idempotent). Gibt {name: role}."""
        out = {}
        for name, color, hoist, perms in TEAM_ROLES:
            r = discord.utils.get(guild.roles, name=name)
            if r is None:
                try:
                    p = discord.Permissions(**perms) if perms else discord.Permissions.none()
                    r = await guild.create_role(name=name, colour=discord.Colour(color),
                                                hoist=hoist, mentionable=False, permissions=p,
                                                reason="Azrael Sentinel Community-Setup")
                except Exception as e:
                    log.warning("Discord: Team-Rolle %s nicht erstellt: %s", name, e); continue
            out[name] = r
        return out

    async def _provision_base_channels(guild):
        created = []
        ev = guild.default_role
        ro = discord.PermissionOverwrite(send_messages=False, view_channel=True)
        info = discord.utils.get(guild.categories, name="📋 INFO")
        if info is None:
            info = await guild.create_category("📋 INFO"); created.append("📋 INFO")
        for nm in ("willkommen", "regeln", "ankündigungen"):
            if discord.utils.get(guild.text_channels, name=nm) is None:
                await guild.create_text_channel(nm, category=info, overwrites={ev: ro}); created.append(nm)
        comm = discord.utils.get(guild.categories, name="💬 COMMUNITY")
        if comm is None:
            comm = await guild.create_category("💬 COMMUNITY"); created.append("💬 COMMUNITY")
        for nm in ("general", "live-feed", "clips-feed", "ki-moderator"):
            if discord.utils.get(guild.text_channels, name=nm) is None:
                await guild.create_text_channel(nm, category=comm); created.append(nm)
        if discord.utils.get(guild.voice_channels, name="🔊 Lounge") is None:
            await guild.create_voice_channel("🔊 Lounge", category=comm); created.append("🔊 Lounge")
        # mod-log: nur Owner/Moderator sichtbar (Auto-Moderation-Flags)
        if discord.utils.get(guild.text_channels, name=DISCORD_MODLOG_CHANNEL) is None:
            ovw = {guild.default_role: discord.PermissionOverwrite(view_channel=False)}
            for rn in ("👑 Owner", "🛡 Moderator"):
                rr = discord.utils.get(guild.roles, name=rn)
                if rr: ovw[rr] = discord.PermissionOverwrite(view_channel=True)
            await guild.create_text_channel(DISCORD_MODLOG_CHANNEL, category=comm, overwrites=ovw)
            created.append(DISCORD_MODLOG_CHANNEL)
        return created

    async def _provision_user_channels(guild, usernames):
        made = []
        for u in usernames:
            slug = _disc_slug(u)
            catname = f"🎯 {slug}"
            if discord.utils.get(guild.categories, name=catname):
                continue   # idempotent: schon vorhanden
            try:
                cat = await guild.create_category(catname)
                await guild.create_text_channel(f"{slug}-clips", category=cat,
                                                 topic=f"Highlight-Clips von @{u}")
                await guild.create_text_channel(f"{slug}-chat", category=cat)
                await guild.create_voice_channel(f"{slug} 🔊", category=cat)
                made.append(slug)
            except Exception as e:
                log.warning("Discord: User-Channels für %s fehlgeschlagen: %s", u, e)
        return made

    def _tracked_usernames(limit):
        out = []
        try:
            with db_conn() as conn:
                rows = conn.execute("SELECT DISTINCT username FROM trackings "
                                    "WHERE COALESCE(paused,0)=0 ORDER BY username "
                                    f"LIMIT {int(limit)}").fetchall()
            out = [r["username"] for r in rows if r["username"]]
        except Exception as e:
            log.warning("Discord: Tracked-User-Query fehlgeschlagen: %s", e)
        return out

    @tree.command(name="setup_community", description=_nc_i18n.t("Community-Server einrichten: Ränge, Channels, Rechte"))
    async def _c_setup_community(inter):
        if not await _guard(inter):
            return
        await inter.response.defer(ephemeral=True)
        try:
            roles = await _ensure_rank_roles(inter.guild)
            team = await _ensure_team_roles(inter.guild)
            chans = await _provision_base_channels(inter.guild)
            await inter.followup.send(
                f"✅ Community eingerichtet.\n• Team-Rollen: {', '.join(team.keys()) or '—'}\n"
                f"• Rang-Rollen: {', '.join(roles.keys()) or '—'}\n"
                f"• Channels: {', '.join(chans) or 'alle bereits vorhanden'}\n"
                f"Nächster Schritt: `/setup_targets` legt pro getracktem User eigene Channels an.",
                ephemeral=True)
        except Exception as e:
            await inter.followup.send(_nc_i18n.t(f"Fehler: {e}"), ephemeral=True)

    @tree.command(name="setup_targets", description=_nc_i18n.t("Pro getracktem User: Clips-, Chat- und Voice-Channel anlegen"))
    async def _c_setup_targets(inter):
        if not await _guard(inter):
            return
        await inter.response.defer(ephemeral=True)
        try:
            users = _tracked_usernames(DISCORD_TARGET_CAP)
            if not users:
                await inter.followup.send(_nc_i18n.t("Keine getrackten User gefunden."), ephemeral=True); return
            made = await _provision_user_channels(inter.guild, users)
            await inter.followup.send(
                f"✅ {len(made)} neue User-Bereiche angelegt (von {len(users)} getrackten · Cap {DISCORD_TARGET_CAP}).\n"
                + (", ".join(made) if made else "alle bereits vorhanden."),
                ephemeral=True)
        except Exception as e:
            await inter.followup.send(_nc_i18n.t(f"Fehler: {e}"), ephemeral=True)

    @tree.command(name="rank", description=_nc_i18n.t("Dein Level und Rang anzeigen"))
    async def _c_rank(inter):
        try:
            with db_conn() as conn:
                row = conn.execute("SELECT xp FROM discord_xp WHERE guild_id=? AND user_id=?",
                                   (inter.guild_id, inter.user.id)).fetchone()
            xp = row["xp"] if row else 0
            lvl = _xp_to_level(xp); need = 100 * (lvl + 1) * (lvl + 1)
            await inter.response.send_message(
                f"🏅 **{inter.user.display_name}** · Level **{lvl}** · Rang **{_rank_for_level(lvl) or '—'}**\n"
                f"XP: {xp} / {need} (nächstes Level)", ephemeral=True)
        except Exception as e:
            await inter.response.send_message(_nc_i18n.t(f"Fehler: {e}"), ephemeral=True)

    @tree.command(name="leaderboard", description=_nc_i18n.t("Top-10 der Community nach XP"))
    async def _c_leaderboard(inter):
        try:
            with db_conn() as conn:
                rows = conn.execute("SELECT user_id, xp FROM discord_xp WHERE guild_id=? "
                                    "ORDER BY xp DESC LIMIT 10", (inter.guild_id,)).fetchall()
            if not rows:
                await inter.response.send_message(_nc_i18n.t("Noch keine XP-Daten."), ephemeral=True); return
            lines = []
            for i, r in enumerate(rows, 1):
                m = inter.guild.get_member(r["user_id"])
                nm = m.display_name if m else f"User {r['user_id']}"
                lines.append(f"`{i:2}.` **{nm}** — Lvl {_xp_to_level(r['xp'])} ({r['xp']} XP)")
            await inter.response.send_message(_nc_i18n.t("🏆 **Leaderboard**\n" + "\n".join(lines)))
        except Exception as e:
            await inter.response.send_message(_nc_i18n.t(f"Fehler: {e}"), ephemeral=True)

    # ───────── F102: COMMUNITY — Daily-Streak, Profil, AZRAEL-Q&A, Events ─────────
    @tree.command(name="daily", description=_nc_i18n.t("Tägliche XP-Belohnung abholen (Streak-Bonus!)"))
    async def _c_daily(inter):
        try:
            today = datetime.now(timezone.utc).date()
            # v4.1-W29: Erst LESEN, dann antworten, dann schreiben.
            #
            # Vorher lag das `await inter.response.send_message(...)` im
            # Fruehausstieg INNERHALB des offenen db_conn()-Blocks. Das
            # blockiert den Loop nicht (das await gibt ihn frei) — es haelt
            # aber die Verbindung offen, waehrend auf Discord gewartet wird.
            # Bei einem langsamen Discord bekommt in der Zeit jeder andere
            # Schreiber "database is locked".
            row = await db_async(lambda c: c.execute(
                "SELECT last_claim, streak, best_streak, total_claims "
                "FROM discord_daily WHERE guild_id=? AND user_id=?",
                (inter.guild_id, inter.user.id)).fetchone())
            last = None
            if row and row["last_claim"]:
                try:
                    last = datetime.fromisoformat(row["last_claim"]).date()
                except Exception:
                    last = None
            if last == today:
                await inter.response.send_message(
                    _nc_i18n.t("⏳ Heute schon abgeholt — komm morgen wieder für deinen Streak-Bonus!"),
                    ephemeral=True)
                return

            def _buchen(conn):
                # Streak: gestern geclaimt → +1, sonst Reset auf 1
                streak = (row["streak"] + 1) if (row and last == today - timedelta(days=1)) else 1
                best = max(streak, row["best_streak"] if row else 0)
                total = (row["total_claims"] if row else 0) + 1
                bonus = min(DISCORD_DAILY_STREAK_XP * (streak - 1), DISCORD_DAILY_STREAK_XP * 14)
                gain = DISCORD_DAILY_XP + bonus
                conn.execute(
                    "INSERT INTO discord_daily (guild_id,user_id,last_claim,streak,best_streak,total_claims) "
                    "VALUES (?,?,?,?,?,?) ON CONFLICT(guild_id,user_id) DO UPDATE SET "
                    "last_claim=excluded.last_claim, streak=excluded.streak, "
                    "best_streak=excluded.best_streak, total_claims=excluded.total_claims",
                    (inter.guild_id, inter.user.id, today.isoformat(), streak, best, total))
                xprow = conn.execute("SELECT xp, level FROM discord_xp WHERE guild_id=? AND user_id=?",
                                     (inter.guild_id, inter.user.id)).fetchone()
                oldlvl = xprow["level"] if xprow else 0
                newxp = (xprow["xp"] if xprow else 0) + gain
                newlvl = _xp_to_level(newxp)
                nowiso = datetime.now(timezone.utc).isoformat()
                if xprow:
                    conn.execute("UPDATE discord_xp SET xp=?, level=?, last_ts=? WHERE guild_id=? AND user_id=?",
                                 (newxp, newlvl, nowiso, inter.guild_id, inter.user.id))
                else:
                    conn.execute("INSERT INTO discord_xp (guild_id,user_id,xp,level,last_ts) VALUES (?,?,?,?,?)",
                                 (inter.guild_id, inter.user.id, newxp, newlvl, nowiso))
                conn.commit()
                return streak, best, total, gain, bonus, oldlvl, newlvl

            streak, best, total, gain, bonus, oldlvl, newlvl = await db_async(_buchen)
            fire = "🔥" * min(streak, 7)
            await inter.response.send_message(
                f"🎁 **+{gain} XP** abgeholt!  {fire}\n"
                f"Streak: **{streak} Tage** (Bonus +{bonus}) · Bestwert {best} · insgesamt {total}× abgeholt",
                ephemeral=True)
            if newlvl > oldlvl:
                try:
                    await _on_level_up(inter, newlvl)
                except Exception:
                    pass
        except Exception as e:
            await inter.response.send_message(_nc_i18n.t(f"Fehler: {e}"), ephemeral=True)

    @tree.command(name="profile", description=_nc_i18n.t("Dein Community-Profil: Level, Rang, Streak, Rang-Platz"))
    async def _c_profile(inter, member: discord.Member = None):
        try:
            target = member or inter.user
            with db_conn() as conn:
                xr = conn.execute("SELECT xp, level FROM discord_xp WHERE guild_id=? AND user_id=?",
                                  (inter.guild_id, target.id)).fetchone()
                dr = conn.execute("SELECT streak, best_streak, total_claims FROM discord_daily "
                                  "WHERE guild_id=? AND user_id=?", (inter.guild_id, target.id)).fetchone()
                xp = xr["xp"] if xr else 0
                place = conn.execute("SELECT COUNT(*)+1 AS p FROM discord_xp WHERE guild_id=? AND xp>?",
                                     (inter.guild_id, xp)).fetchone()["p"]
                total_members = conn.execute("SELECT COUNT(*) AS c FROM discord_xp WHERE guild_id=?",
                                             (inter.guild_id,)).fetchone()["c"]
            lvl = _xp_to_level(xp); need = 100 * (lvl + 1) * (lvl + 1); prev = 100 * lvl * lvl
            pct = int(100 * (xp - prev) / max(1, need - prev))
            bar = "█" * (pct // 10) + "░" * (10 - pct // 10)
            emb = discord.Embed(title=f"🦇 {target.display_name}", color=0x00ff9c)
            emb.add_field(name="Level", value=f"**{lvl}** · {_rank_for_level(lvl) or 'GHOST'}", inline=True)
            emb.add_field(name="Rang-Platz", value=f"#{place} / {total_members}", inline=True)
            emb.add_field(name="XP", value=f"{xp}", inline=True)
            emb.add_field(name="Fortschritt", value=f"`{bar}` {pct}%  ({xp}/{need})", inline=False)
            if dr:
                emb.add_field(name="Daily-Streak", value=f"🔥 {dr['streak']} Tage (Best: {dr['best_streak']})", inline=True)
            if target.display_avatar:
                emb.set_thumbnail(url=target.display_avatar.url)
            await inter.response.send_message(embed=emb)
        except Exception as e:
            await inter.response.send_message(_nc_i18n.t(f"Fehler: {e}"), ephemeral=True)

    @tree.command(name="ask", description=_nc_i18n.t("AZRAEL etwas fragen — der KI-Community-Assistent"))
    async def _c_ask(inter, frage: str):
        await inter.response.defer()
        try:
            # Live-Kontext mitgeben, damit AZRAEL community-bewusst antwortet
            ctx = ""
            try:
                with db_conn() as conn:
                    live = [r["username"] for r in conn.execute(
                        "SELECT username FROM trackings WHERE last_live=1 LIMIT 5").fetchall()]
                if live:
                    ctx = "Gerade live: " + ", ".join("@" + u for u in live) + ". "
            except Exception:
                pass
            txt, err = await azrael_chat(
                "Discord-Community-Frage",
                f"{inter.user.display_name} fragt: {frage}",
                extra_system=(ctx + "Du bist AZRAEL, der KI-Community-Assistent dieses "
                              "TikTok-Restream-Servers. Antworte hilfreich, freundlich, kurz "
                              "(max 4 Sätze), auf Deutsch. Kennst du etwas nicht, sag es ehrlich."))
            if err or not txt:
                await inter.followup.send(_nc_i18n.t(f"⚠ AZRAEL konnte nicht antworten ({err or 'leer'})."))
                return
            emb = discord.Embed(description=txt[:3900], color=0x00e5ff)
            emb.set_author(name="🦇 AZRAEL")
            emb.set_footer(text=f"gefragt von {inter.user.display_name}")
            await inter.followup.send(embed=emb)
        except Exception as e:
            await inter.followup.send(_nc_i18n.t(f"Fehler: {e}"))

    @tree.command(name="event", description=_nc_i18n.t("Community-Event ankündigen (Admin) — mit Countdown"))
    async def _c_event(inter, titel: str, wann: str, beschreibung: str = ""):
        if not await _guard(inter):
            return
        try:
            # 'wann' flexibel parsen: ISO, 'YYYY-MM-DD HH:MM' oder '+2h' / '+30m'
            when = None
            w = wann.strip()
            mrel = re.match(r"^\+(\d+)\s*([mhd])$", w, re.I)
            if mrel:
                n = int(mrel.group(1)); unit = mrel.group(2).lower()
                delta = timedelta(minutes=n) if unit == "m" else (
                    timedelta(hours=n) if unit == "h" else timedelta(days=n))
                when = datetime.now(timezone.utc) + delta
            else:
                for fmt in ("%Y-%m-%dT%H:%M", "%Y-%m-%d %H:%M", "%Y-%m-%d %H:%M:%S"):
                    try:
                        when = datetime.strptime(w, fmt).replace(tzinfo=timezone.utc); break
                    except ValueError:
                        continue
            if when is None:
                await inter.response.send_message(
                    _nc_i18n.t("⚠ Zeit nicht verstanden. Formate: `2026-07-10 20:00`, `+2h`, `+30m`, `+1d`."),
                    ephemeral=True)
                return
            with db_conn() as conn:
                conn.execute("INSERT INTO community_events (guild_id,title,description,starts_at,"
                             "created_by,created_at) VALUES (?,?,?,?,?,?)",
                             (inter.guild_id, titel[:120], beschreibung[:500], when.isoformat(),
                              inter.user.id, datetime.now(timezone.utc).isoformat()))
            ts = int(when.timestamp())
            emb = discord.Embed(title=f"📅 {titel}", description=beschreibung or None, color=0xffb000)
            emb.add_field(name="Wann", value=f"<t:{ts}:F>  ·  <t:{ts}:R>", inline=False)
            emb.set_footer(text=f"angekündigt von {inter.user.display_name}")
            ev_ch = discord.utils.get(inter.guild.text_channels, name=DISCORD_EVENTS_CHANNEL)
            if ev_ch:
                await ev_ch.send(content="@here 📢 Neues Event!", embed=emb)
                await inter.response.send_message(_nc_i18n.t(f"✅ Event in #{DISCORD_EVENTS_CHANNEL} angekündigt."), ephemeral=True)
            else:
                await inter.response.send_message(embed=emb)
        except Exception as e:
            await inter.response.send_message(_nc_i18n.t(f"Fehler: {e}"), ephemeral=True)

    @tree.command(name="events", description=_nc_i18n.t("Kommende Community-Events anzeigen"))
    async def _c_events(inter):
        try:
            with db_conn() as conn:
                rows = conn.execute("SELECT title, description, starts_at FROM community_events "
                                    "WHERE guild_id=? AND done=0 ORDER BY starts_at LIMIT 10",
                                    (inter.guild_id,)).fetchall()
            if not rows:
                await inter.response.send_message(_nc_i18n.t("📭 Keine kommenden Events. Admins: `/event`."), ephemeral=True)
                return
            emb = discord.Embed(title="📅 Kommende Events", color=0xffb000)
            for r in rows:
                try:
                    ts = int(datetime.fromisoformat(r["starts_at"]).timestamp())
                    when = f"<t:{ts}:R> · <t:{ts}:f>"
                except Exception:
                    when = r["starts_at"]
                emb.add_field(name=r["title"], value=(r["description"] or "") + f"\n{when}", inline=False)
            await inter.response.send_message(embed=emb)
        except Exception as e:
            await inter.response.send_message(_nc_i18n.t(f"Fehler: {e}"), ephemeral=True)

    # ───────── BOT-STEUERUNG: recstatus (track/untrack/tracklist/ai existieren bereits oben) ─────────
    @tree.command(name="recstatus", description=_nc_i18n.t("Aktuell laufende Aufnahmen"))
    async def _c_recstatus(inter):
        try:
            with db_conn() as conn:
                rows = conn.execute("SELECT username, output_file FROM trackings WHERE recording=1 "
                                    "ORDER BY username").fetchall()
            if not rows:
                await inter.response.send_message(_nc_i18n.t("⚫ Keine aktiven Aufnahmen."), ephemeral=True); return
            lines = [f"🔴 @{r['username']}" + (f" — `{os.path.basename(r['output_file'])}`" if r["output_file"] else "") for r in rows]
            await inter.response.send_message(_nc_i18n.t(f"**Aktive Aufnahmen ({len(rows)})**\n" + "\n".join(lines[:40])))
        except Exception as e:
            await inter.response.send_message(_nc_i18n.t(f"Fehler: {e}"), ephemeral=True)

    @tree.command(name="livenow", description=_nc_i18n.t("Welche getrackten User sind gerade live"))
    async def _c_livenow(inter):
        try:
            with db_conn() as conn:
                rows = conn.execute("SELECT username, recording FROM trackings WHERE last_live=1 "
                                    "ORDER BY username").fetchall()
            if not rows:
                await inter.response.send_message(_nc_i18n.t("⚫ Gerade niemand live."), ephemeral=True); return
            lines = [("🔴 REC " if r["recording"] else "🟢 LIVE ") + f"@{r['username']}" for r in rows]
            await inter.response.send_message(_nc_i18n.t(f"**Live jetzt ({len(rows)})**\n" + "\n".join(lines[:40])))
        except Exception as e:
            await inter.response.send_message(_nc_i18n.t(f"Fehler: {e}"), ephemeral=True)

    @tree.command(name="clips", description=_nc_i18n.t("Letzte Highlight-Clips eines Users"))
    @app_commands.describe(username="TikTok-Username")
    async def _c_clips(inter, username: str):
        try:
            slug = _disc_slug(username)
            if not os.path.isdir(CLIP_DIR):
                await inter.response.send_message(_nc_i18n.t("Keine Clips vorhanden."), ephemeral=True); return
            files = [f for f in os.listdir(CLIP_DIR) if f.endswith(".mp4") and slug in f.lower()]
            files.sort(key=lambda f: os.path.getmtime(os.path.join(CLIP_DIR, f)), reverse=True)
            if not files:
                await inter.response.send_message(_nc_i18n.t(f"Keine Clips für @{username.lstrip('@')}."), ephemeral=True); return
            lines = [f"• `{f}` ({os.path.getsize(os.path.join(CLIP_DIR, f)) // 1048576} MB)" for f in files[:10]]
            await inter.response.send_message(_nc_i18n.t(f"**Clips @{username.lstrip('@')} ({len(files)})**\n" + "\n".join(lines)))
        except Exception as e:
            await inter.response.send_message(_nc_i18n.t(f"Fehler: {e}"), ephemeral=True)

    @tree.command(name="post_test", description=_nc_i18n.t("Test: Nachricht in den Channel eines getrackten Users posten"))
    @app_commands.describe(username="TikTok-Username")
    async def _c_post_test(inter, username: str):
        if not await _guard(inter):
            return
        await inter.response.defer(ephemeral=True)
        try:
            u = username.lstrip("@")
            await _discord_post_user(u, f"✅ Test-Post für **@{u}** — der Upload-Channel funktioniert.", feed=None)
            await inter.followup.send(
                _nc_i18n.t(f"Test-Nachricht an `#{_disc_slug(u)}-clips` gesendet (falls Channel existiert — sonst erst `/setup_targets`)."),
                ephemeral=True)
        except Exception as e:
            await inter.followup.send(_nc_i18n.t(f"Fehler: {e}"), ephemeral=True)

    @tree.command(name="help", description=_nc_i18n.t("Alle Bot-Befehle anzeigen"))
    async def _c_help(inter):
        await inter.response.send_message(
            "**🦇 Azrael Sentinel — Befehle**\n"
            "**Tracking:** `/track` `/untrack` `/tracklist` `/livenow` `/recstatus` `/clips` `/stats` `/topstreamers` `/streaminfo`\n"
            "**Clips:** `/clip` — Highlight vom laufenden Stream schneiden · ⭐ voten fürs Clip-of-the-Week\n"
            "**Streamer folgen:** `/follow` `/unfollow` — Live-Ping nur für deine Streamer\n"
            "**KI:** `/ai <frage>` · `/ask <frage>` — AZRAEL, der KI-Community-Assistent\n"
            "**Community:** `/rank` `/profile` `/leaderboard` `/daily` (Streak-XP!) `/clipoftheweek`\n"
            "**Events:** `/event` (Admin) · `/events` — Ankündigungen mit Countdown\n"
            "**Moderation (Admin):** `/warn` `/warnings` `/clearwarns` `/purge`\n"
            "**Setup (Admin):** `/setup_community` `/setup_targets` `/post_test`\n"
            "**Server (Admin):** `/create_channel` `/create_voice` `/create_category` `/create_role`",
            ephemeral=True)

    @tree.command(name="follow", description=_nc_i18n.t("Bei Live-Gang eines Streamers gepingt werden"))
    @app_commands.describe(username="TikTok-Username")
    async def _c_follow(inter, username: str):
        u = username.lstrip("@")
        rname = f"🔔 {_disc_slug(u)}"
        try:
            role = discord.utils.get(inter.guild.roles, name=rname)
            if role is None:
                role = await inter.guild.create_role(name=rname, mentionable=True,
                                                     colour=discord.Colour(0x00e5ff), reason="Streamer-Notify")
            await inter.user.add_roles(role, reason="follow")
            await inter.response.send_message(_nc_i18n.t(f"🔔 Du wirst gepingt wenn **@{u}** live geht."), ephemeral=True)
        except Exception as e:
            await inter.response.send_message(_nc_i18n.t(f"Fehler: {e}"), ephemeral=True)

    @tree.command(name="unfollow", description=_nc_i18n.t("Live-Pings für einen Streamer abbestellen"))
    @app_commands.describe(username="TikTok-Username")
    async def _c_unfollow(inter, username: str):
        try:
            role = discord.utils.get(inter.guild.roles, name=f"🔔 {_disc_slug(username.lstrip('@'))}")
            if role and role in inter.user.roles:
                await inter.user.remove_roles(role, reason="unfollow")
            await inter.response.send_message(_nc_i18n.t(f"🔕 Keine Live-Pings mehr für **@{username.lstrip('@')}**."), ephemeral=True)
        except Exception as e:
            await inter.response.send_message(_nc_i18n.t(f"Fehler: {e}"), ephemeral=True)

    @tree.command(name="stats", description=_nc_i18n.t("Statistik zu einem getrackten Streamer"))
    @app_commands.describe(username="TikTok-Username")
    async def _c_stats(inter, username: str):
        try:
            u = username.lstrip("@")
            with db_conn() as conn:
                rc = conn.execute("SELECT COUNT(*) AS n, MAX(created_at) AS last FROM recordings WHERE username=?", (u,)).fetchone()
                snap = conn.execute("SELECT follower_count, heart_count, video_count FROM profile_snapshots "
                                    "WHERE username=? ORDER BY captured_at DESC LIMIT 1", (u,)).fetchone()
                live = conn.execute("SELECT last_live, recording FROM trackings WHERE username=? LIMIT 1", (u,)).fetchone()
            n = rc["n"] if rc else 0
            last = (rc["last"] or "")[:10] if rc and rc["last"] else "—"
            status = "🔴 REC" if (live and live["recording"]) else ("🟢 LIVE" if (live and live["last_live"]) else "⚫ offline")
            lines = [f"📊 **@{u}** · {status}", f"🎬 Aufnahmen: **{n}**" + (f" (letzte {last})" if n else "")]
            if snap:
                if snap["follower_count"] is not None: lines.append(f"👥 Follower: **{snap['follower_count']:,}**")
                if snap["heart_count"] is not None: lines.append(f"❤️ Herzen: **{snap['heart_count']:,}**")
                if snap["video_count"] is not None: lines.append(f"🎥 Videos: **{snap['video_count']:,}**")
            await inter.response.send_message(_nc_i18n.t("\n".join(lines)))
        except Exception as e:
            await inter.response.send_message(_nc_i18n.t(f"Fehler: {e}"), ephemeral=True)

    @tree.command(name="warn", description=_nc_i18n.t("Mitglied verwarnen (eskaliert ab 3 Verwarnungen zu Timeout)"))
    @app_commands.describe(member="Mitglied", reason="Grund")
    async def _c_warn(inter, member: discord.Member, reason: str = "kein Grund"):
        if not await _guard(inter):
            return
        try:
            with db_conn() as conn:
                conn.execute("INSERT INTO discord_warns (guild_id, user_id, moderator, reason, created_at) "
                             "VALUES (?,?,?,?,?)",
                             (inter.guild_id, member.id, str(inter.user), reason, datetime.now(timezone.utc).isoformat()))
                n = conn.execute("SELECT COUNT(*) AS c FROM discord_warns WHERE guild_id=? AND user_id=?",
                                 (inter.guild_id, member.id)).fetchone()["c"]
            msg = f"⚠️ {member.mention} verwarnt ({n}. Verwarnung) — {reason}"
            if n >= 3:
                try:
                    until = datetime.now(timezone.utc) + timedelta(minutes=DISCORD_WARN_TIMEOUT_MIN)
                    await member.timeout(until, reason=f"{n} Verwarnungen")
                    msg += f"\n⏳ Timeout {DISCORD_WARN_TIMEOUT_MIN}min (ab 3. Verwarnung)."
                except Exception:
                    pass
            await inter.response.send_message(_nc_i18n.t(msg))
        except Exception as e:
            await inter.response.send_message(_nc_i18n.t(f"Fehler: {e}"), ephemeral=True)

    @tree.command(name="warnings", description=_nc_i18n.t("Verwarnungen eines Mitglieds anzeigen"))
    @app_commands.describe(member="Mitglied")
    async def _c_warnings(inter, member: discord.Member):
        try:
            with db_conn() as conn:
                rows = conn.execute("SELECT reason, moderator, created_at FROM discord_warns "
                                    "WHERE guild_id=? AND user_id=? ORDER BY id DESC LIMIT 15",
                                    (inter.guild_id, member.id)).fetchall()
            if not rows:
                await inter.response.send_message(_nc_i18n.t(f"{member.display_name} hat keine Verwarnungen."), ephemeral=True); return
            lines = [f"• {(r['created_at'] or '')[:10]} — {r['reason']} _(von {r['moderator']})_" for r in rows]
            await inter.response.send_message(_nc_i18n.t(f"⚠️ **{member.display_name}** ({len(rows)})\n" + "\n".join(lines)), ephemeral=True)
        except Exception as e:
            await inter.response.send_message(_nc_i18n.t(f"Fehler: {e}"), ephemeral=True)

    @tree.command(name="clearwarns", description=_nc_i18n.t("Alle Verwarnungen eines Mitglieds löschen"))
    @app_commands.describe(member="Mitglied")
    async def _c_clearwarns(inter, member: discord.Member):
        if not await _guard(inter):
            return
        try:
            with db_conn() as conn:
                conn.execute("DELETE FROM discord_warns WHERE guild_id=? AND user_id=?", (inter.guild_id, member.id))
            await inter.response.send_message(_nc_i18n.t(f"🧹 Verwarnungen von {member.mention} gelöscht."))
        except Exception as e:
            await inter.response.send_message(_nc_i18n.t(f"Fehler: {e}"), ephemeral=True)

    @tree.command(name="topstreamers", description=_nc_i18n.t("Rangliste der Streamer nach Aufnahmen"))
    async def _c_topstreamers(inter):
        try:
            with db_conn() as conn:
                rows = conn.execute("SELECT username, COUNT(*) AS n FROM recordings "
                                    "GROUP BY username ORDER BY n DESC LIMIT 10").fetchall()
            if not rows:
                await inter.response.send_message(_nc_i18n.t("Noch keine Aufnahmen."), ephemeral=True); return
            medals = ["🥇", "🥈", "🥉"] + ["🔹"] * 7
            lines = [f"{medals[i]} **@{r['username']}** — {r['n']} Aufnahmen" for i, r in enumerate(rows)]
            await inter.response.send_message(_nc_i18n.t("🏆 **Top-Streamer**\n" + "\n".join(lines)))
        except Exception as e:
            await inter.response.send_message(_nc_i18n.t(f"Fehler: {e}"), ephemeral=True)

    @tree.command(name="clipoftheweek", description=_nc_i18n.t("Aktuell führender Clip-of-the-Week (⭐-Voting)"))
    async def _c_cotw(inter):
        await inter.response.defer()
        try:
            leader = await _clip_week_leader()
            if not leader or leader[1] <= 0:
                await inter.followup.send(_nc_i18n.t("Noch keine Votes diese Woche. ⭐ die Clips zum Abstimmen!")); return
            msg, votes, username = leader
            await inter.followup.send(_nc_i18n.t(f"🏆 **Führend:** @{username} mit **{votes}** ⭐\n{msg.jump_url}"))
        except Exception as e:
            await inter.followup.send(_nc_i18n.t(f"Fehler: {e}"))

    _disc_clip_last = {}    # F84: user_id -> monotonic (Cooldown für /clip)

    @tree.command(name="clip", description=_nc_i18n.t("Highlight-Clip der letzten Sekunden vom laufenden Stream"))
    @app_commands.describe(username="Streamer (leer = der einzige der gerade aufgenommen wird)")
    async def _c_clip(inter, username: str = ""):
        now = _time_mod.monotonic()
        wait = CLIP_CMD_COOLDOWN_S - (now - _disc_clip_last.get(inter.user.id, 0))
        if wait > 0:
            await inter.response.send_message(_nc_i18n.t(f"⏳ Cooldown — versuch's in {int(wait)}s nochmal."), ephemeral=True)
            return
        u = username.strip().lstrip("@")
        try:
            if not u:
                with db_conn() as conn:
                    rows = conn.execute("SELECT username FROM trackings WHERE last_live=1 AND recording=1 "
                                        "GROUP BY username").fetchall()
                names = [r["username"] for r in rows]
                if not names:
                    await inter.response.send_message(_nc_i18n.t("Gerade läuft keine Aufnahme."), ephemeral=True); return
                if len(names) > 1:
                    await inter.response.send_message(
                        "Mehrere Aufnahmen laufen — gib den Streamer an: " +
                        ", ".join(f"`{n}`" for n in names[:10]), ephemeral=True); return
                u = names[0]
            await inter.response.defer()
            _disc_clip_last[inter.user.id] = now
            out = await clip_moment(u, reason=f"/clip von {inter.user.display_name}",
                                    caption=f"Clip by {inter.user.display_name}")
            if out:
                await inter.followup.send(_nc_i18n.t(f"✂ Clip von **@{u}** erstellt — landet gleich in **#{u}-clips**. ⭐ nicht vergessen!"))
            else:
                await inter.followup.send(f"Kein Clip möglich für @{u} — keine laufende Aufnahme, "
                                          f"Aufnahme zu frisch oder Clip-Cooldown des Streamers aktiv.")
        except Exception as e:
            try:
                await inter.followup.send(_nc_i18n.t(f"Fehler: {e}"))
            except Exception:
                await inter.response.send_message(_nc_i18n.t(f"Fehler: {e}"), ephemeral=True)

    @tree.command(name="botstats", description=_nc_i18n.t("Bot-Health: Uptime, Trackings, Aufnahmen, DB (Admin)"))
    async def _c_botstats(inter):
        if not await _guard(inter):
            return
        try:
            up = int(_time_mod.time() - _BOOT_TS)
            d, rem = divmod(up, 86400); h, rem = divmod(rem, 3600); m = rem // 60
            today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
            with db_conn() as conn:
                tr = conn.execute("SELECT COUNT(*) AS c FROM trackings").fetchone()["c"]
                lv = conn.execute("SELECT COUNT(*) AS c FROM trackings WHERE last_live=1").fetchone()["c"]
                rc = conn.execute("SELECT COUNT(*) AS c FROM recordings WHERE created_at >= ?",
                                  (today,)).fetchone()["c"]
            try:
                dbsz = round(os.path.getsize(DB_PATH) / (1024 * 1024), 1) if DB_BACKEND != "mariadb" else None
            except Exception:
                dbsz = None
            emb = discord.Embed(title="🦇 Azrael Sentinel Botstats", colour=discord.Colour(0x00FF9C))
            emb.add_field(name="Uptime", value=f"{d}d {h}h {m}m", inline=True)
            emb.add_field(name="Trackings", value=f"{tr} ({lv} live)", inline=True)
            emb.add_field(name="Aufnahmen heute", value=str(rc), inline=True)
            if dbsz is not None:
                emb.add_field(name="DB-Größe", value=f"{dbsz} MB", inline=True)
            emb.add_field(name="Discord-Latenz", value=f"{int(client.latency * 1000)} ms", inline=True)
            _ra = _restream_active()
            emb.add_field(name="Restream", value=(f"📡 @{_ra['user']}" if _ra.get("user") else "—"), inline=True)
            emb.timestamp = datetime.now(timezone.utc)
            await inter.response.send_message(embed=emb, ephemeral=True)
        except Exception as e:
            await inter.response.send_message(_nc_i18n.t(f"Fehler: {e}"), ephemeral=True)

    @tree.command(name="sys_unpause", description=_nc_i18n.t("Auto-pausierte Quelle wieder aktivieren (Admin)"))
    @app_commands.describe(username="TikTok-Username der pausierten Quelle")
    async def _c_sys_unpause(inter, username: str):
        if not _is_admin(inter):
            await inter.response.send_message(_nc_i18n.t("Nur Admins."), ephemeral=True); return
        await inter.response.defer(thinking=True)
        u = username.strip().lstrip("@")
        try:
            with db_conn() as conn:
                cur = conn.execute("UPDATE trackings SET paused=0 WHERE "
                                   "username=? AND paused=1", (u,))
                conn.commit(); n = cur.rowcount
            try:
                from brain import get_brain as _gb
                _b = _gb()
                with _b._db_lock, _b._conn() as _c:
                    _c.execute("DELETE FROM paused_sources WHERE who=? OR who=?",
                               (u, "@" + u))
            except Exception:
                pass
            await inter.followup.send(f"✅ @{u} reaktiviert." if n else
                                      f"@{u} war nicht pausiert.")
        except Exception as e:
            await inter.followup.send(_nc_i18n.t(f"❌ Fehler: {e}"))

    @tree.command(name="sys_report", description=_nc_i18n.t("Azrael Sentinel Wochenreport (Brain, Markdown)"))
    async def _c_sys_report(inter):
        if not _is_admin(inter):
            await inter.response.send_message(_nc_i18n.t("Nur Admins."), ephemeral=True); return
        await inter.response.defer(thinking=True)
        try:
            from brain import get_brain
            from brain import report as _brain_report
            md = await asyncio.to_thread(_brain_report.weekly, get_brain())
        except Exception as e:
            await inter.followup.send(_nc_i18n.t(f"❌ Report fehlgeschlagen: {e}")); return
        for i in range(0, len(md), 1900):
            await inter.followup.send(_nc_i18n.t(md[i:i + 1900]))

    # ===================== V37-W-PAR: Telegram-Parität ======================
    # Die restlichen TG-Kommandos laufen über einen Shim, der die ORIGINAL-
    # Handler (pause_tracking, sysres, …) unverändert ausführt: ein Fake-
    # Update/Context sammelt jede reply_text-Ausgabe ein und schickt sie als
    # Interaction-Followup. Eine Logik, null Code-Duplikate — Fixes an den
    # TG-Handlern wirken automatisch auch in Discord.
    class _ParMsg:
        def __init__(self, sink):
            self._sink = sink
            self.text = ""
            self.message_id = 0
            self.chat = types.SimpleNamespace(id=_par_chat_id())
        async def reply_text(self, text, **kw):
            await self._sink(str(text)); return self
        reply_html = reply_markdown = reply_markdown_v2 = reply_text
        async def reply_document(self, document=None, filename=None, caption=None, **kw):
            await self._sink(f"[Datei: {filename or 'dokument'}] {caption or ''}".strip())
            return self
        async def edit_text(self, text, **kw):
            await self._sink(str(text)); return self

    def _par_chat_id():
        return next(iter(ALLOWED_CHAT_IDS), next(iter(ALLOWED_USER_IDS), 0))

    class _ParBot:
        def __init__(self, sink): self._sink = sink
        async def send_message(self, chat_id=None, text="", **kw):
            await self._sink(str(text))
        async def send_document(self, chat_id=None, document=None, filename=None,
                                caption=None, **kw):
            await self._sink(f"[Datei: {filename or 'dokument'}] {caption or ''}".strip())
        async def send_chat_action(self, *a, **kw): pass

    async def _run_tg_handler(inter, fn, args_str=""):
        if not _is_admin(inter):
            await inter.response.send_message(_nc_i18n.t("Nur Admins."), ephemeral=True); return
        await inter.response.defer(thinking=True)
        chunks = []
        async def _sink(t):
            chunks.append(t)
        msg = _ParMsg(_sink)
        uid = next(iter(ALLOWED_USER_IDS), 0)
        upd = types.SimpleNamespace(
            effective_user=types.SimpleNamespace(id=uid, first_name="discord",
                                                 username="discord"),
            effective_chat=types.SimpleNamespace(id=_par_chat_id()),
            effective_message=msg, message=msg, callback_query=None)
        ctx = types.SimpleNamespace(args=(args_str or "").split(),
                                    bot=_ParBot(_sink),
                                    user_data={}, chat_data={}, bot_data={})
        try:
            await fn(upd, ctx)
        except Exception as e:
            chunks.append(f"❌ Handler-Fehler: {type(e).__name__}: {e}")
        out = "\n\n".join(c for c in chunks if c) or "✅ Ausgeführt (keine Ausgabe)."
        out = re.sub(r"</?(?:b|i|code|pre|u|s)>", "**", out)     # grobes HTML→MD
        for i in range(0, len(out), 1900):
            await inter.followup.send(_nc_i18n.t(out[i:i + 1900]))

    _PAR_CMDS = (
        ("sys_pause",    "Tracking pausieren (TG: /pause @user)",        pause_tracking,  True),
        ("sys_resume",   "Tracking fortsetzen (TG: /resume @user)",      resume_tracking, True),
        ("sys_stoprec",  "Aufnahme grazil stoppen (TG: /stoprec @user)", stoprec,         True),
        ("sys_cleanup",  "Alte Aufnahmen aufräumen (TG: /cleanup)",      cleanup,         True),
        ("sys_quota",    "Speicher-Quota (TG: /quota)",                  quota,           False),
        ("sys_res",      "System-Ressourcen (TG: /sysres)",              sysres,          False),
        ("sys_topusers", "Top-Streamer-Statistik (TG: /topusers)",       topusers,        False),
        ("sys_summary",  "Tageszusammenfassung (TG: /summary)",          summary_cmd,     False),
        ("sys_logs",     "Letzte Fehler-Logs (TG: /logs)",               logs_cmd,        True),
        ("sys_diag",     "Vollständige Diagnose (TG: /diag)",            diag,            False),
        ("sys_aireset",  "KI-Kontext zurücksetzen (TG: /aireset)",       aireset,         True),
        ("sys_teststream", "Recorder-Selbsttest (TG: /teststream)",      teststream,      True),
        ("sys_bulkadd",  "Mehrere User tracken (TG: /bulkadd a b c)",    bulkadd,         True),
        ("sys_live",     "Live-Check erzwingen (TG: /live @user)",       live,            True),
        ("sys_cookies",  "Cookie-Status (TG: /cookies)",                 cookies_cmd,     True),
    )
    for _pname, _pdesc, _pfn, _pargs in _PAR_CMDS:
        def _mk(fn=_pfn, wants_args=_pargs):
            if wants_args:
                async def _h(inter, args: str = ""):
                    await _run_tg_handler(inter, fn, args)
            else:
                async def _h(inter):
                    await _run_tg_handler(inter, fn)
            return _h
        tree.command(name=_pname, description=_pdesc[:100])(_mk())
    # =================== ENDE V37-W-PAR ======================================

    @tree.command(name="streaminfo", description=_nc_i18n.t("Kompakt-Karte eines Streamers: Aktivität, Aufnahmen, Follower-Trend"))
    @app_commands.describe(username="TikTok-Username")
    async def _c_streaminfo(inter, username: str):
        u = username.strip().lstrip("@")
        try:
            with db_conn() as conn:
                agg = conn.execute("SELECT COUNT(*) AS n, MAX(created_at) AS last, "
                                   "AVG(duration_secs) AS avgd FROM recordings WHERE username=?",
                                   (u,)).fetchone()
                month_ago = (datetime.now(timezone.utc) - timedelta(days=30)).isoformat()
                snaps = conn.execute("SELECT follower_count, captured_at FROM profile_snapshots "
                                     "WHERE username=? AND captured_at >= ? ORDER BY captured_at",
                                     (u, month_ago)).fetchall()
                is_live = conn.execute("SELECT COUNT(*) AS c FROM trackings WHERE username=? AND last_live=1",
                                       (u,)).fetchone()["c"] > 0
            emb = discord.Embed(title=f"📊 @{u}",
                                url=f"https://www.tiktok.com/@{u}",
                                colour=discord.Colour(0xFF2E88 if is_live else 0x00E5FF))
            emb.add_field(name="Status", value=("🔴 LIVE" if is_live else "⚫ offline"), inline=True)
            emb.add_field(name="Aufnahmen", value=str(agg["n"] if agg else 0), inline=True)
            if agg and agg["avgd"]:
                emb.add_field(name="Ø Dauer", value=f"{int(agg['avgd'] // 60)} min", inline=True)
            if agg and agg["last"]:
                emb.add_field(name="Zuletzt gesehen", value=str(agg["last"])[:16].replace("T", " "), inline=True)
            if len(snaps) >= 2 and snaps[0]["follower_count"] and snaps[-1]["follower_count"]:
                diff = int(snaps[-1]["follower_count"]) - int(snaps[0]["follower_count"])
                emb.add_field(name="Follower 30d",
                              value=f"{snaps[-1]['follower_count']:,} ({'+' if diff >= 0 else ''}{diff:,})".replace(",", "."),
                              inline=True)
            emb.set_footer(text="Azrael Sentinel")
            emb.timestamp = datetime.now(timezone.utc)
            await inter.response.send_message(embed=emb)
        except Exception as e:
            await inter.response.send_message(_nc_i18n.t(f"Fehler: {e}"), ephemeral=True)

    # ───────── XP/Leveling via on_message ─────────
    _xp_cool = {}   # user_id -> monotonic (Anti-Spam: max 1× XP / 60s)

    async def _on_level_up(message, newlvl):
        try:
            rkname = _rank_for_level(newlvl)
            if rkname:
                roles = await _ensure_rank_roles(message.guild)
                role = roles.get(rkname)
                if role and role not in getattr(message.author, "roles", []):
                    old = [discord.utils.get(message.guild.roles, name=n) for _, n, _c in RANK_TIERS]
                    old = [r for r in old if r and r != role and r in message.author.roles]
                    try:
                        if old: await message.author.remove_roles(*old, reason="Rang-Upgrade")
                        await message.author.add_roles(role, reason=f"Level {newlvl}")
                    except Exception:
                        pass
            txt = f"🎉 {message.author.mention} ist jetzt **Level {newlvl}**" + (f" — Rang **{rkname}**!" if rkname else "!")
            ch = discord.utils.get(message.guild.text_channels, name=DISCORD_LEVELUP_CHANNEL) if DISCORD_LEVELUP_CHANNEL else None
            await (ch or message.channel).send(_nc_i18n.t(txt))
        except Exception as e:
            log.debug("Discord Level-Up: %s", e)

    async def _handle_voice_ai(message, att):
        """Sprachnachricht → ffmpeg→16k-WAV → Whisper → ai_chat → Antwort."""
        import tempfile
        tmp_in = os.path.join(tempfile.gettempdir(), f"disc_voice_{message.id}_{_disc_slug(att.filename)}")
        tmp_wav = tmp_in + ".wav"
        try:
            await att.save(tmp_in)
            proc = await asyncio.create_subprocess_exec(
                "ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", tmp_in,
                "-ar", "16000", "-ac", "1", tmp_wav,
                stdout=asyncio.subprocess.DEVNULL, stderr=asyncio.subprocess.DEVNULL)
            await proc.wait()
            if not os.path.exists(tmp_wav) or os.path.getsize(tmp_wav) < 100:
                return
            async with message.channel.typing():
                text = await _whisper_transcribe(tmp_wav)
                if not text:
                    await message.reply(_nc_i18n.t("🎤 Konnte die Sprachnachricht nicht transkribieren."), mention_author=False)
                    return
                txt, err = await azrael_chat("Telegram Voice", text, timeout=30)   # F90: eine KI-Identität
            await message.reply(_nc_i18n.t(f"🎤 **Du:** {text[:300]}\n\n🤖 {(txt or err or '—')[:1700]}"), mention_author=False)
        except Exception as e:
            log.debug("Discord Voice-AI: %s", e)
        finally:
            for f in (tmp_in, tmp_wav):
                try:
                    if os.path.exists(f): os.remove(f)
                except OSError:
                    pass

    @client.event
    async def on_raw_reaction_add(payload):
        """F84: Community-kuratierte Highlights — erreicht ein Clip
           CLIP_HIGHLIGHT_STARS echte ⭐, wird er EINMAL automatisch an die
           Telegram-Gruppen gepusht, die den Streamer tracken."""
        try:
            if not _auto_on("highlight_tg", CLIP_HIGHLIGHT_TO_TG) or str(payload.emoji) != "⭐":
                return
            if client.user and payload.user_id == client.user.id:
                return
            # v4.1-W29: NEBEN dem Loop. Laeuft bei JEDER Discord-Reaktion.
            row = await db_async(lambda c: c.execute(
                "SELECT id, username, filepath, stars_pushed FROM discord_clips "
                "WHERE message_id=?", (payload.message_id,)).fetchone())
            if not row or row["stars_pushed"] or not row["filepath"]:
                return
            ch = client.get_channel(payload.channel_id)
            if not ch:
                return
            msg = await ch.fetch_message(payload.message_id)
            votes = 0
            for rc in msg.reactions:
                if str(rc.emoji) == "⭐":
                    votes = max(0, rc.count - (1 if rc.me else 0))
                    break
            if votes < max(1, CLIP_HIGHLIGHT_STARS):
                return
            fp = row["filepath"]
            if not (os.path.exists(fp) and os.path.getsize(fp) < 48 * 1024 * 1024):
                return
            await db_async(lambda c: c.execute(
                "UPDATE discord_clips SET stars_pushed=1 WHERE id=?", (row["id"],)))
            app = globals().get("bot_app")
            if not app:
                return
            gids = await db_async(lambda c: [r["group_id"] for r in c.execute(
                "SELECT DISTINCT group_id FROM trackings WHERE username=?",
                (row["username"],)).fetchall()])
            cap = f"⭐ Community-Highlight: @{row['username']} — {votes}× gevotet im Discord"
            for gid in gids:
                if DISCORD_GUILD_ID and gid == DISCORD_GUILD_ID:
                    continue    # Discord-eigene Liste → kein Telegram-Ziel
                try:
                    with open(fp, "rb") as f:
                        await app.bot.send_video(chat_id=gid, video=f, caption=cap,
                                                 read_timeout=120, write_timeout=120)
                except Exception as e:
                    log.debug("highlight→TG %s: %s", gid, e)
            log.info("⭐ Highlight-Clip @%s (%d Votes) → Telegram gepusht.", row["username"], votes)
            # V37-COMMUNITY: denselben Highlight als teilbaren Discord-Post — der
            # Reichweiten-Motor. Aufruf zum Teilen + Sterne-Zahl. Der Clip liegt
            # schon im Discord (dort wurde er ja gevotet), daher kein Re-Upload —
            # nur die Ansage, die zum Teilen anregt.
            if COMMUNITY_HIGHLIGHT_SHARE_ENABLED and DISCORD_WEBHOOK_URL:
                try:
                    _post = _community.highlight_post(row["username"], stars=votes)
                    await _discord_notify(_post)
                except Exception as _e:
                    log.debug("community highlight-share: %s", _e)
        except Exception as e:
            log.debug("raw-reaction: %s", e)

    async def _award_xp(message):
        uid = message.author.id
        now = _time_mod.monotonic()
        if now - _xp_cool.get(uid, 0) < 60:
            return
        _xp_cool[uid] = now
        gain = 15 + int(now) % 11               # 15–25 XP
        # F84: Doppelte XP solange irgendein getrackter Stream live ist —
        # zieht Leute genau dann in den Chat. Live-Status 30s gecacht
        # (kein DB-Hit pro Message).
        if DISCORD_XP_LIVE_BOOST > 1:
            try:
                c = getattr(_award_xp, "_live_cache", None)
                if not c or now - c[0] > 30:
                    # v4.1-W29: NEBEN dem Loop. Diese Funktion laeuft bei
                    # JEDER Discord-Nachricht; der 30-s-Cache daempft die
                    # Zahl der Abfragen, nicht ihre Blockade.
                    n = await db_async(lambda cn: cn.execute(
                        "SELECT COUNT(*) AS c FROM trackings WHERE last_live=1").fetchone()["c"])
                    c = (now, n > 0)
                    _award_xp._live_cache = c
                if c[1]:
                    gain *= DISCORD_XP_LIVE_BOOST
            except Exception:
                pass
        try:
            # v4.1-W29: NEBEN dem Loop. Lesen und Schreiben bleiben in EINER
            # Transaktion — sonst koennten zwei Nachrichten desselben Nutzers
            # denselben Stand lesen und einer der beiden XP-Gewinne ginge
            # verloren. Der 60-s-Cooldown oben macht das unwahrscheinlich,
            # aber nicht unmoeglich.
            def _buchen(conn):
                row = conn.execute("SELECT xp, level FROM discord_xp WHERE guild_id=? AND user_id=?",
                                   (message.guild.id, uid)).fetchone()
                oldlvl = row["level"] if row else 0
                newxp = (row["xp"] if row else 0) + gain
                newlvl = _xp_to_level(newxp)
                nowiso = datetime.now(timezone.utc).isoformat()
                if row:
                    conn.execute("UPDATE discord_xp SET xp=?, level=?, last_ts=? WHERE guild_id=? AND user_id=?",
                                 (newxp, newlvl, nowiso, message.guild.id, uid))
                else:
                    conn.execute("INSERT INTO discord_xp (guild_id, user_id, xp, level, last_ts) VALUES (?,?,?,?,?)",
                                 (message.guild.id, uid, newxp, newlvl, nowiso))
                conn.commit()
                return oldlvl, newlvl

            oldlvl, newlvl = await db_async(_buchen)
            if newlvl > oldlvl:
                await _on_level_up(message, newlvl)
        except Exception as e:
            log.debug("Discord XP-Update: %s", e)

    async def _discord_automod(message):
        # Owner/Moderator nicht moderieren
        if {r.name for r in getattr(message.author, "roles", [])} & {"👑 Owner", "🛡 Moderator"}:
            return
        reason = _disc_automod_check(message.content, message.author.id)
        if not reason:
            return
        try:
            mlog = discord.utils.get(message.guild.text_channels, name=DISCORD_MODLOG_CHANNEL)
            if mlog:
                await mlog.send(f"⚠️ **{reason}** · {message.author.mention} in {message.channel.mention}: "
                                f"`{(message.content or '')[:180]}`")
        except Exception:
            pass
        # V37-W-SHIELD: Doxxing/Volksverhetzung/Drohung wird IMMER entfernt
        # + eskalierender Timeout — unabhängig von DISCORD_AUTOMOD_ACTION.
        if reason.startswith("🛑"):
            try:
                await message.delete()
            except Exception:
                pass
            try:
                mins = _KICK_MOD._escalation_minutes(f"dc:{message.author.id}")
                await message.author.timeout(timedelta(minutes=mins),
                                             reason=f"SENTINEL: {reason}")
            except Exception:
                pass
            _modlog("timeout", "sentinel-shield", (message.content or "")[:200],
                    {"user": str(message.author), "reason": reason,
                     "platform": "discord"})
            return True
        if DISCORD_AUTOMOD_ACTION == "delete":
            try:
                await message.delete()
                w = await message.channel.send(_nc_i18n.t(f"{message.author.mention} Nachricht entfernt — {reason}."))
                await w.delete(delay=6)
                return True
            except Exception:
                pass
        return False

    # ───────── F93: AZRAEL SENTINEL — KI-Moderation im Discord ─────────
    # Dieselbe eine KI-Identität, die den Kick-Chat bewacht, klassifiziert jetzt
    # auch Discord-Nachrichten (Toxizität via Ollama). CPU-Schutz: Semaphore(2)
    # ohne Warteschlange, min. 3s Abstand, globales KI-Budget wird respektiert.
    _dc_ai_sema = asyncio.Semaphore(2)
    _dc_ai_last = {"ts": 0.0}

    async def _discord_ai_automod(message) -> bool:
        c = (message.content or "").strip()
        if len(c) < 12 or c.startswith(("/", "!")):
            return False
        if {r.name for r in getattr(message.author, "roles", [])} & {"👑 Owner", "🛡 Moderator"}:
            return False
        now = _time_mod.monotonic()
        if now - _dc_ai_last["ts"] < 3.0:               # max ~1 Klassifikation / 3s
            return False
        if len(_AI_CALL_TS) >= max(1, AZRAEL_MAX_CALLS_MIN):   # globales KI-Budget voll
            return False
        if _dc_ai_sema.locked():
            return False                                 # kein freier Slot → skip statt Stau
        _dc_ai_last["ts"] = now
        _KICK_MOD.stats["dc_seen"] = _KICK_MOD.stats.get("dc_seen", 0) + 1
        async with _dc_ai_sema:
            cls = await _KICK_MOD._classify(c)
        if not cls or cls["toxic"] < float(_KICK_MOD.cfg.get("sensitivity", 0.85)):
            return False
        # Verstoß: löschen + eskalierender Timeout + Mod-Log (Discord + Dashboard)
        mins = _KICK_MOD._escalation_minutes(f"dc:{message.author.id}")
        acted = []
        try:
            await message.delete(); acted.append("gelöscht")
        except Exception:
            pass
        try:
            await message.author.timeout(timedelta(minutes=mins),
                                         reason=f"AZRAEL: Toxizität {cls['toxic']:.2f}")
            acted.append(f"Timeout {mins}min")
        except Exception:
            pass
        _KICK_MOD.stats["dc_moderated"] = _KICK_MOD.stats.get("dc_moderated", 0) + 1
        _modlog("timeout", "ai-discord", c[:200],
                {"user": str(message.author), "toxic": round(cls["toxic"], 2), "min": mins,
                 "platform": "discord"})
        try:
            mlog = discord.utils.get(message.guild.text_channels, name=DISCORD_MODLOG_CHANNEL)
            if mlog:
                await mlog.send(f"🦇 **AZRAEL KI-Mod** ({', '.join(acted) or 'nur geflaggt'}) · "
                                f"{message.author.mention} · Toxizität `{cls['toxic']:.2f}`\n"
                                f"`{c[:180]}`")
        except Exception:
            pass
        try:
            await _KICK_MOD._learn_from(c)               # neue Schimpfwörter → Review-Queue
        except Exception:
            pass
        return True

    _dc_reply_last = {"ts": 0.0}

    async def _discord_azrael_reply(message):
        """AZRAEL antwortet, wenn er im Discord direkt erwähnt wird — dieselbe
           eine KI-Identität wie im Kick-Chat/Overlay. 10s-Cooldown gegen Fluten."""
        now = _time_mod.monotonic()
        if now - _dc_reply_last["ts"] < 10:
            return
        _dc_reply_last["ts"] = now
        q = re.sub(r"<@!?\d+>", "", message.content or "").strip()[:600]
        if not q:
            return
        try:
            async with message.channel.typing():
                txt, err = await azrael_chat(
                    "Discord-Chat",
                    f"{message.author.display_name} schreibt im Discord: {q}",
                    extra_system="Antworte kurz (max 3 Sätze), locker, deutsch.")
            if txt and not err:
                await message.reply(_nc_i18n.t(txt[:1900]), mention_author=False)
                _KICK_MOD.last_spoken = {"text": txt[:200], "ts": _time_mod.monotonic()}
        except Exception as e:
            log.debug("discord azrael reply: %s", e)

    async def _update_liveboard():
        guild = client.guilds[0] if client.guilds else None
        if not guild:
            return
        ch = discord.utils.get(guild.text_channels, name="live-feed")
        if not ch:
            return
        with db_conn() as conn:
            rows = conn.execute("SELECT username, recording FROM trackings WHERE last_live=1 ORDER BY username").fetchall()
        desc = "\n".join((("🔴 " if r["recording"] else "🟢 ") + f"@{r['username']}") for r in rows) if rows else "Gerade niemand live."
        # F84: Restream-Status direkt im Board — Community sieht sofort ob Kick läuft
        _ra = _restream_active()
        if _ra.get("user"):
            desc += f"\n\n📡 **Kick-Restream läuft** — Quelle: @{_ra['user']}"
            if KICK_CHANNEL_URL:
                desc += f"\n{KICK_CHANNEL_URL}"
        emb = discord.Embed(title="🔴 LIVE JETZT", colour=discord.Colour(0x00ff9c), description=desc[:4000])
        emb.set_footer(text=f"{len(rows)} live · aktualisiert")
        emb.timestamp = datetime.now(timezone.utc)
        mid = _disc_state_get("liveboard_msg")
        msg = None
        if mid:
            try: msg = await ch.fetch_message(int(mid))
            except Exception: msg = None
        if msg:
            await msg.edit(embed=emb)
        else:
            m = await ch.send(embed=emb)
            try: await m.pin()
            except Exception: pass
            _disc_state_set("liveboard_msg", m.id)

    async def _liveboard_loop():
        await client.wait_until_ready()
        while not client.is_closed():
            try:
                if DISCORD_LIVEBOARD:
                    await _update_liveboard()
            except Exception as e:
                _loop_fehler("_liveboard_loop", e)
            await asyncio.sleep(60)

    async def _post_weekly_digest():
        guild = client.guilds[0] if client.guilds else None
        if not guild:
            return
        ch = discord.utils.get(guild.text_channels, name="live-feed") or discord.utils.get(guild.text_channels, name="general")
        if not ch:
            return
        since = (datetime.now(timezone.utc) - timedelta(days=7)).isoformat()
        with db_conn() as conn:
            recs = conn.execute("SELECT COUNT(*) AS n FROM recordings WHERE created_at >= ?", (since,)).fetchone()
            top = conn.execute("SELECT username, COUNT(*) AS n FROM recordings WHERE created_at >= ? "
                               "GROUP BY username ORDER BY n DESC LIMIT 5", (since,)).fetchall()
        emb = discord.Embed(title="📅 Wochenrückblick", colour=discord.Colour(0x00e5ff))
        emb.add_field(name="Aufnahmen diese Woche", value=str(recs["n"] if recs else 0), inline=False)
        if top:
            emb.add_field(name="Top-Streamer", value="\n".join(f"**@{r['username']}** — {r['n']}" for r in top), inline=False)
        emb.timestamp = datetime.now(timezone.utc)
        await ch.send(embed=emb)

    async def _weekly_digest_loop():
        await client.wait_until_ready()
        while not client.is_closed():
            try:
                now = datetime.now(timezone.utc)
                wk = now.strftime("%Y-W%W")
                if DISCORD_WEEKLY_DIGEST and now.weekday() == 6 and now.hour >= 18 and _disc_state_get("digest_week") != wk:
                    await _post_weekly_digest()
                    _disc_state_set("digest_week", wk)
            except Exception as e:
                _loop_fehler("_weekly_digest_loop", e)
            await asyncio.sleep(1800)   # alle 30min prüfen

    async def _clip_week_leader():
        """Clip der letzten 7 Tage mit den meisten ⭐-Votes → (msg, votes, username) oder None."""
        guild = client.guilds[0] if client.guilds else None
        if not guild:
            return None
        since = (datetime.now(timezone.utc) - timedelta(days=7)).isoformat()
        with db_conn() as conn:
            rows = conn.execute("SELECT channel_id, message_id, username FROM discord_clips "
                                "WHERE created_at >= ? ORDER BY id DESC LIMIT 100", (since,)).fetchall()
        best = None
        for r in rows:
            ch = guild.get_channel(int(r["channel_id"]))
            if not ch:
                continue
            try:
                msg = await ch.fetch_message(int(r["message_id"]))
            except Exception:
                continue
            votes = 0
            for rc in msg.reactions:
                if str(rc.emoji) == "⭐":
                    # B64: Bot-Seed nur abziehen wenn die Bot-Reaction wirklich
                    # existiert (add_reaction kann fehlgeschlagen sein → sonst
                    # zählt jeder Clip 1 Vote zu wenig).
                    votes = max(0, rc.count - (1 if rc.me else 0))
                    break
            if best is None or votes > best[1]:
                best = (msg, votes, r["username"])
        return best

    async def _post_clip_of_week():
        leader = await _clip_week_leader()
        if not leader or leader[1] <= 0:
            return
        msg, votes, username = leader
        guild = client.guilds[0] if client.guilds else None
        ch = discord.utils.get(guild.text_channels, name="clips-feed") or discord.utils.get(guild.text_channels, name="live-feed")
        if not ch:
            return
        emb = discord.Embed(title="🏆 Clip of the Week",
                            description=f"**@{username}** · {votes} ⭐\n[▶ zum Clip]({msg.jump_url})",
                            colour=discord.Colour(0xffb000))
        emb.timestamp = datetime.now(timezone.utc)
        w = await ch.send(embed=emb)
        try:
            await w.pin()
        except Exception:
            pass

    async def _clipoftheweek_loop():
        await client.wait_until_ready()
        while not client.is_closed():
            try:
                now = datetime.now(timezone.utc)
                wk = now.strftime("%Y-CW%W")
                if DISCORD_CLIP_OF_WEEK and now.weekday() == 6 and now.hour >= 19 and _disc_state_get("cotw_week") != wk:
                    await _post_clip_of_week()
                    _disc_state_set("cotw_week", wk)
            except Exception as e:
                _loop_fehler("_clipoftheweek_loop", e)
            await asyncio.sleep(1800)

    @client.event
    async def on_message(message):
        if message.author.bot:
            return
        # B138: Direktnachrichten haben KEINE guild. Der frühere Guard
        # "or not message.guild" brach hier ab — damit ignorierte der Bot
        # jede Discord-DM vollständig, auch eine ausdrückliche @Erwähnung.
        # Moderation bleibt serverseitig (in einer DM gibt es nichts zu
        # moderieren, und Löschen/Timeout wäre dort gar nicht möglich),
        # die Ansprache läuft jetzt in beiden Fällen.
        _in_gilde = message.guild is not None
        if _in_gilde:
            # Auto-Moderation (Heuristik/Banned-Words) — bei Löschung Rest überspringen
            if DISCORD_AUTOMOD and await _discord_automod(message):
                return
            # F93: AZRAEL KI-Moderation (Ollama-Toxizität, budget-geschützt)
            if DISCORD_AI_MOD and await _discord_ai_automod(message):
                return
        # F93: AZRAEL antwortet bei direkter @Mention (eine KI, alle Kanäle).
        # B138: in einer DM ist jede Nachricht eine Ansprache — dort ist eine
        # @Erwähnung unüblich und wäre eine sinnlose Hürde.
        _angesprochen = (
            (not _in_gilde)
            or (client.user and client.user in message.mentions
                and not message.mention_everyone))
        if DISCORD_AZRAEL_REPLY and _angesprochen:
            _spawn(_discord_azrael_reply(message), name="dc-azrael-reply")
        # Sprachnachricht → Whisper → KI-Antwort
        if DISCORD_VOICE_AI and message.attachments:
            for att in message.attachments:
                fn = (att.filename or "").lower()
                if (att.content_type or "").startswith("audio") or fn.endswith((".ogg", ".oga", ".mp3", ".m4a", ".wav", ".webm")):
                    await _handle_voice_ai(message, att)
                    break
        # XP/Level-Ranking
        if DISCORD_LEVELING:
            await _award_xp(message)

    @client.event
    async def on_member_join(member):
        try:
            role = discord.utils.get(member.guild.roles, name="👤 Member")
            if role:
                try: await member.add_roles(role, reason="Auto-Role beim Beitritt")
                except Exception: pass
            ch = discord.utils.get(member.guild.text_channels, name="willkommen")
            if ch:
                try:
                    # F84: Willkommens-Embed statt nackter Zeile
                    emb = discord.Embed(
                        title=f"👋 Willkommen, {member.display_name}!",
                        description=("Schön dass du da bist! So legst du los:\n\n"
                                     "📜 Wirf einen Blick in **#regeln**\n"
                                     "🔔 `/follow <streamer>` — Ping nur bei DEINEN Streamern\n"
                                     "✂ `/clip` — Highlight vom laufenden Stream schneiden\n"
                                     "🤖 `/ai <frage>` — frag die Bot-KI (auch per Sprachnachricht)\n"
                                     "⭐ Clips voten — der beste wird **Clip of the Week**\n\n"
                                     "Alle Befehle: `/help`"),
                        colour=discord.Colour(0x00E5FF))
                    try:
                        emb.set_thumbnail(url=member.display_avatar.url)
                    except Exception:
                        pass
                    emb.set_footer(text="Azrael Sentinel Community")
                    await ch.send(content=member.mention, embed=emb)
                except Exception:
                    try:
                        await ch.send(_nc_i18n.t(f"👋 Willkommen {member.mention} in der Community!"))
                    except Exception:
                        pass
        except Exception as e:
            log.debug("Discord on_member_join: %s", e)

    @client.event
    async def on_ready():
        try:
            if DISCORD_GUILD_ID:
                g = discord.Object(id=DISCORD_GUILD_ID)
                tree.copy_global_to(guild=g)
                await tree.sync(guild=g)
            else:
                await tree.sync()
            log.info("Discord verbunden als %s — %d Slash-Commands aktiv.",
                     client.user, len(tree.get_commands()))
        except Exception as e:
            log.warning("Discord Slash-Sync fehlgeschlagen: %s", e)
        # Hintergrund-Loops einmalig starten (on_ready feuert bei jedem
        # Reconnect erneut — und B120 erzeugt bei jeder Session ein NEUES
        # client-Objekt, weshalb ein Attribut am client als Guard nicht
        # mehr reicht).
        global _DISCORD_BGTASKS_STARTED
        _DISCORD_SESSION["connected_since"] = _time_mod.time()
        if not _DISCORD_BGTASKS_STARTED:
            _DISCORD_BGTASKS_STARTED = True
            # BUGFIX (Tiefensuche): diese fuenf Loops liefen ueber
            # client.loop.create_task(...) OHNE dass jemand die Task-Objekte
            # festhielt. asyncio haelt auf laufende Tasks nur eine SCHWACHE
            # Referenz — ein Task, der gerade in `await asyncio.sleep(...)`
            # haengt, kann vom Garbage Collector eingesammelt werden. Genau
            # das tun alle fuenf: sie schlafen 20-60s zwischen den Durchlaeufen.
            #
            # Verschwindet ein Loop so, gibt es KEINE Exception und KEINE
            # Logzeile — Liveboard, Wochen-Digest, Clip der Woche, Error-Feed
            # oder Event-Countdown hoeren einfach auf zu arbeiten, waehrend der
            # Discord-Bot ansonsten normal weiterlaeuft. Das ist ununterscheid-
            # bar von "die Discord-Funktionen gehen nicht mehr".
            #
            # _spawn() haelt die Referenz in _background_tasks und loggt
            # Abstuerze — dieselbe Behandlung wie alle anderen Loops des Bots.
            if DISCORD_LIVEBOARD:
                _spawn(_liveboard_loop(), name="discord-liveboard")
            if DISCORD_WEEKLY_DIGEST:
                _spawn(_weekly_digest_loop(), name="discord-digest")
            if DISCORD_CLIP_OF_WEEK:
                _spawn(_clipoftheweek_loop(), name="discord-clipoftheweek")
            if DISCORD_ERROR_PUSH:
                _spawn(_error_channel_loop(), name="discord-errorfeed")
            _spawn(_community_events_loop(), name="discord-community-events")
            # v4.0-W35: nie ablaufenden Community-Invite EINMALIG erzeugen (nur
            # wenn noch keiner in .env/app_config steht) — für Website + Announcer.
            _spawn(_ensure_discord_invite(client), name="discord-invite-once")

    # B120: Ausnahmen NICHT mehr schlucken — der Supervisor oben muss sie
    # sehen, sonst gibt es keinen Reconnect. Nur die vier Faelle, die ein
    # Retry nachweislich nicht heilt, werden hier final abgefangen.
    try:
        await client.start(DISCORD_BOT_TOKEN)
    except discord.PrivilegedIntentsRequired:
        log.error(
            "Discord: PRIVILEGIERTE INTENTS NICHT AKTIVIERT. Der Bot fordert "
            "message_content und members an. Beides muss im Developer Portal "
            "unter Applications -> %s -> Bot -> Privileged Gateway Intents "
            "eingeschaltet sein. Ohne das verweigert Discord den Login und "
            "KEIN Slash-Command funktioniert.",
            "<deine App>")
        return True
    except discord.LoginFailure as e:
        log.error("Discord: Token abgelehnt (%s). DISCORD_BOT_TOKEN pruefen — "
                  "ein neu generierter Token macht den alten sofort ungueltig.", e)
        return True
    except asyncio.CancelledError:
        raise
    finally:
        _nc_discordstate.CLIENT["obj"] = None
        try:
            if not client.is_closed():
                await client.close()
        except Exception:
            pass
    return False


_DC_ERR_CH_CACHE = {}       # guild_id -> Channel (oder False = anlegen fehlgeschlagen)


async def _ensure_error_channel(guild):
    """#error-log finden oder anlegen — default_role unsichtbar, Owner/Moderator
       (+ DISCORD_ADMIN_ROLE) und der Bot selbst sichtbar."""
    try:
        import discord
    except Exception:
        return None
    cached = _DC_ERR_CH_CACHE.get(guild.id)
    if cached is not None:
        return cached or None
    ch = discord.utils.get(guild.text_channels, name=DISCORD_ERROR_CHANNEL)
    if ch is None:
        try:
            ovw = {guild.default_role: discord.PermissionOverwrite(view_channel=False),
                   guild.me: discord.PermissionOverwrite(view_channel=True, send_messages=True)}
            roles = ["👑 Owner", "🛡 Moderator"]
            if DISCORD_ADMIN_ROLE:
                roles.append(DISCORD_ADMIN_ROLE)
            for rn in roles:
                rr = discord.utils.get(guild.roles, name=rn)
                if rr:
                    ovw[rr] = discord.PermissionOverwrite(view_channel=True)
            ch = await guild.create_text_channel(
                DISCORD_ERROR_CHANNEL, overwrites=ovw,
                topic="🦇 NIGHTCRAWLER Fehler-Feed — nur Admins. Automatisch befüllt.",
                reason="NIGHTCRAWLER Error-Channel (F96)")
            log.info("Discord: Admin-Error-Channel #%s angelegt.", DISCORD_ERROR_CHANNEL)
        except Exception as e:
            log.warning("Discord: Error-Channel nicht anlegbar: %s", e)
            _DC_ERR_CH_CACHE[guild.id] = False
            return None
    _DC_ERR_CH_CACHE[guild.id] = ch
    return ch


async def _community_events_loop():
    """F102: Erinnert 10 Min vor Event-Start (@here) und markiert vergangene
       Events als erledigt. Läuft alle 60s, best-effort."""
    await asyncio.sleep(30)
    import discord
    while True:
        try:
            if _nc_discordstate.CLIENT["obj"] and getattr(_nc_discordstate.CLIENT["obj"], "user", None):
                now = datetime.now(timezone.utc)
                # v4.1-W29: ERST lesen, DANN senden, DANN schreiben.
                #
                # Vorher stand `await ch.send(...)` INNERHALB des
                # `with db_conn()`-Blocks. Das blockierte zwar nicht den Loop
                # (das await gibt ihn frei) — es hielt aber die Verbindung und
                # damit den Schreib-Lock offen, waehrend auf Discord gewartet
                # wurde. Bei einem langsamen Discord bekommt in der Zeit JEDER
                # andere Schreiber "database is locked", und die Ursache steht
                # in einer Schleife, die nur alle 60 Sekunden laeuft.
                rows = await db_async(lambda c: c.execute(
                    "SELECT id, guild_id, title, description, starts_at, announced "
                    "FROM community_events WHERE done=0").fetchall())
                erledigt, angekuendigt = [], []
                for r in rows:
                    try:
                        when = datetime.fromisoformat(r["starts_at"])
                    except Exception:
                        continue
                    mins = (when - now).total_seconds() / 60.0
                    guild = _nc_discordstate.CLIENT["obj"].get_guild(r["guild_id"])
                    ch = discord.utils.get(guild.text_channels, name=DISCORD_EVENTS_CHANNEL) if guild else None
                    # 10-Min-Vorwarnung (einmalig via announced=1)
                    if ch and not r["announced"] and 0 < mins <= 10:
                        ts = int(when.timestamp())
                        await ch.send(f"@here ⏰ **{r['title']}** startet <t:{ts}:R>!"
                                      + (f"\n{r['description']}" if r["description"] else ""))
                        angekuendigt.append(r["id"])
                    # Start erreicht → Go + erledigt
                    elif ch and mins <= 0:
                        # v4.1-W29: t() um den FESTEN Teil, nicht um den
                        # f-String. Vorher lautete der Schluessel
                        # "@here 🔴 **Filmabend** geht JETZT los!" — mit dem
                        # Titel drin, und traf im Katalog nie.
                        await ch.send("@here 🔴 **%s** %s"
                                      % (r["title"], _nc_i18n.t("geht JETZT los!")))
                        erledigt.append(r["id"])
                    elif mins < -120:      # alte Leichen aufräumen
                        erledigt.append(r["id"])

                if angekuendigt or erledigt:
                    # Die Listen kommen als ARGUMENT herein, nicht ueber die
                    # Closure: die Funktion steht in einer while-Schleife, und
                    # eine eingefangene Schleifenvariable ist die Sorte Fehler,
                    # die erst bei der zweiten Runde zuschlaegt (ruff B023).
                    def _fortschreiben(conn, an, erl):
                        for rid in an:
                            conn.execute("UPDATE community_events SET announced=1 WHERE id=?", (rid,))
                        for rid in erl:
                            conn.execute("UPDATE community_events SET done=1 WHERE id=?", (rid,))
                        conn.commit()
                    await db_async(_fortschreiben, angekuendigt, erledigt)
        except Exception as e:
            _loop_fehler("_community_events_loop", e)
        await asyncio.sleep(60)


async def _error_channel_loop():
    """Flusht die Error-Queue alle 20s gebündelt in #error-log."""
    last_sent = {}
    await asyncio.sleep(20)
    while True:
        try:
            if _DC_ERR_QUEUE and _nc_discordstate.CLIENT["obj"] and getattr(_nc_discordstate.CLIENT["obj"], "user", None):
                batch = []
                while _DC_ERR_QUEUE and len(batch) < 8:
                    batch.append(_DC_ERR_QUEUE.popleft())
                now = _time_mod.time()
                out = []
                for b in batch:
                    key = b["msg"][:160]                      # Dedup: gleiche Meldung max 1×/10min
                    if now - last_sent.get(key, 0) > 600:
                        last_sent[key] = now
                        out.append(b)
                if len(last_sent) > 500:                       # Dedup-Map nicht wachsen lassen
                    last_sent = {k: v for k, v in last_sent.items() if now - v < 600}
                if out:
                    txt = "\n".join(f"```{b['msg']}```" for b in out)[:1990]
                    for g in _nc_discordstate.CLIENT["obj"].guilds:
                        ch = await _ensure_error_channel(g)
                        if ch:
                            try:
                                await ch.send(_nc_i18n.t(txt))
                            except Exception:
                                pass
        except Exception as e:
            _loop_fehler("_error_channel_loop", e)
        await asyncio.sleep(20)


_disc_automod_hist = {}
_disc_banned_cache = {"words": None}


def _disc_automod_check(content, user_id):
    """Heuristik-Spam + Banned-Words. Gibt Grund-String zurück wenn Verstoß, sonst None."""
    c = (content or "").strip()
    if not c:
        return None
    hard = _sentinel_screen(c)                      # V37-W-SHIELD
    if hard:
        return f"🛑 {hard[0]}: {hard[1]}"
    letters = [ch for ch in c if ch.isalpha()]
    if len(letters) >= 10:
        up = sum(1 for ch in letters if ch.isupper())
        if up / max(1, len(letters)) >= 0.85:
            return "CAPS-Spam"
    if len(re.findall(r"https?://|www\.", c, re.I)) > 3:
        return "Link-Spam"
    if c.count("@") > 6:
        return "Mention-Spam"
    if _disc_banned_cache["words"] is None:
        try:
            _disc_banned_cache["words"] = set(w.lower() for w in _load_banned_words_file())
        except Exception:
            _disc_banned_cache["words"] = set()
    bw = _disc_banned_cache["words"]
    if bw and (set(re.findall(r"[a-zA-ZäöüÄÖÜß]+", c.lower())) & bw):
        return "Verbotenes Wort"
    now = _time_mod.monotonic()
    h = _disc_automod_hist.setdefault(user_id, [])
    h.append((now, c.lower()))
    _disc_automod_hist[user_id] = [(t, m) for (t, m) in h if now - t <= 8]
    _nc_mod.prune_history(_disc_automod_hist, now, 8)   # W14: kein Dauerwachstum
    recent = _disc_automod_hist.get(user_id, [])
    if len(recent) > 6:
        return "Flood"
    if sum(1 for (_t, m) in recent if m == c.lower()) >= 4:
        return "Repeat-Spam"
    return None
