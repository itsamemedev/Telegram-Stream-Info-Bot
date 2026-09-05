"""nc.botctx — der Vertrag zwischen dem Monolithen und dem Discord-Teil.

Warum es das gibt: `discordbot.py` ist aus `bot.py` herausgelöst und darf
nicht zurückimportieren — sonst steht ein Zirkelimport da, und die
Architektur-Grenze aus CLAUDE.md ("nc/* und brain/* importieren nie aus
bot.py") wäre für den ersten bot-seitigen Ableger sofort aufgeweicht.
Statt dessen füllt der Bot beim Start EINEN Kontext und reicht ihn hinein.

Warum nicht `nc.ctx`: der dort ist der Kontext der Flask-Blueprints und steht
vertraglich bei 25 Feldern. Der Discord-Teil braucht andere Dinge (Telegram-
Handler, den Moderator, die Fehler-Deque) und würde die Bremse dort sprengen,
ohne dass eine einzige Route etwas davon hätte. Zwei Kontexte, zwei Grenzen.

**Die Aufteilung ist Absicht, kein Zufall:**

* Aufrufbares und LEBENDER Zustand sind Felder — sie haben eine Signatur bzw.
  eine Identität, die im Diff auffallen muss, wenn sie sich ändert.
* Konfiguration ist EIN Wörterbuch (`schalter`). Sie kommt komplett aus `.env`,
  wird nur gelesen, und sie in 36 Einzelfelder zu zerlegen hätte den Kontext
  auf 57 Felder aufgebläht — genau das Sammelbecken, vor dem `nc/ctx.py`
  warnt. Die Schlüsselmenge steht als `SCHALTER` fest und wird geprüft; ein
  Tippfehler fällt damit BEIM START auf, nicht nachts um drei in einem
  Slash-Command als `KeyError`.
* Die Telegram-Befehle, die Discord mitbenutzt, sind ebenfalls ein Wörterbuch
  (`befehle`). Sie sind KEINE Discord-Funktionen: `/sys_diag` in Discord ruft
  denselben `diag`-Handler wie `/diag` in Telegram. Genau deshalb dürfen sie
  nicht mitwandern — sie sind die geteilte Befehlsschicht.

`.env` wird an genau EINER Stelle gelesen, nämlich in `bot.py`. Zwei Dateien
mit eigenem `os.getenv("DISCORD_…")` wären zwei Orte, an denen ein Default
auseinanderlaufen kann — und `tools/gen_env_example.py` müsste beide kennen.
"""

from dataclasses import dataclass

# Telegram-Handler, die die Discord-Slash-Commands (sys_*) mitbenutzen.
# Sie leben weiter in bot.py; hier steht nur, welche der Discord-Teil erwartet.
BEFEHLE = (
    "pause_tracking", "resume_tracking", "stoprec", "cleanup", "quota",
    "sysres", "topusers", "summary_cmd", "logs_cmd", "diag", "aireset",
    "teststream", "bulkadd", "live", "cookies_cmd",
)

# Konfigurationswerte aus .env, die der Discord-Teil liest. Nur-lesend.
SCHALTER = (
    # geteilt mit dem Rest des Bots
    "ALLOWED_CHAT_IDS", "ALLOWED_USER_IDS", "AZRAEL_MAX_CALLS_MIN",
    "CLIP_DIR", "CLIP_HIGHLIGHT_STARS", "CLIP_HIGHLIGHT_TO_TG",
    "DB_BACKEND", "DB_PATH", "DISCORD_BOT_TOKEN", "DISCORD_GUILD_ID",
    "DISCORD_MODLOG_CHANNEL", "DISCORD_TRACK_GROUP_ID", "DISCORD_WEBHOOK_URL",
    "KICK_CHANNEL_URL", "MAX_TRACKINGS_PER_CHAT",
    # nur der Discord-Teil liest sie
    "CLIP_CMD_COOLDOWN_S", "COMMUNITY_HIGHLIGHT_SHARE_ENABLED",
    "DISCORD_ADMIN_ROLE", "DISCORD_AI_MOD", "DISCORD_AUTOMOD",
    "DISCORD_AUTOMOD_ACTION", "DISCORD_AZRAEL_REPLY", "DISCORD_CLIP_OF_WEEK",
    "DISCORD_DAILY_STREAK_XP", "DISCORD_DAILY_XP", "DISCORD_ERROR_CHANNEL",
    "DISCORD_ERROR_PUSH", "DISCORD_EVENTS_CHANNEL", "DISCORD_LEVELING",
    "DISCORD_LEVELUP_CHANNEL", "DISCORD_LIVEBOARD", "DISCORD_TARGET_CAP",
    "DISCORD_VOICE_AI", "DISCORD_WARN_TIMEOUT_MIN", "DISCORD_WEEKLY_DIGEST",
    "DISCORD_XP_LIVE_BOOST",
)


@dataclass(frozen=True, slots=True)
class BotKontext:
    """Was der Discord-Teil vom Monolithen braucht — und sonst nichts.

    `frozen=True` ist kein Schmuck: der Kontext wird einmal beim Start gebaut
    und danach nur gelesen. Ein späteres Umbiegen eines Feldes wäre genau die
    Sorte Fernwirkung, die im Monolithen schon zweimal parallele
    Endlosschleifen erzeugt hat (Guard als Objekt-Attribut, B120).
    `slots=True` verhindert, dass jemand still ein 22. Feld anhängt.
    """

    log: object                 # der Logger des Bots

    # --- Infrastruktur ---
    spawn: object               # _spawn: Task auf dem Bot-Loop, benannt
    loop_fehler: object         # _loop_fehler: gedrosselte Dauerläufer-Meldung
    modlog: object              # _modlog: Moderations-Protokoll
    auto_on: object             # _auto_on: Schalter aus app_config/.env
    cfg_get: object             # _cfg_get / _cfg_set: app_config
    cfg_set: object

    # --- Fachliches, das im Monolithen bleibt ---
    discord_notify: object      # _discord_notify: Webhook-Meldung
    discord_post_user: object   # _discord_post_user: Beitrag im User-Channel
    disc_state_get: object      # Wochenstände der Digests
    disc_state_set: object
    whisper_transcribe: object  # Sprachnachricht → Text
    add_tracking: object
    azrael_chat: object
    clip_moment: object

    # Warum ein SETZER und kein Wert: `_ensure_discord_invite` erzeugt den
    # Invite genau einmal und schreibt ihn nach DISCORD_INVITE_URL. Diese
    # Variable liest der Announcer in bot.py. Ein `global` im ausgelagerten
    # Modul hätte nur die dortige Kopie gesetzt — der Announcer hätte weiter
    # die alte, leere URL verschickt.
    einladung_merken: object

    # --- Lebender Zustand: dieselben Objekte, keine Kopien ---
    kick_mod: object            # _KICK_MOD, der Moderator (Statistik + Lernen)
    fehler_schlange: object     # _DC_ERR_QUEUE, vom Logging-Handler gefüllt
    boot_ts: float              # _BOOT_TS

    befehle: dict               # siehe BEFEHLE
    schalter: dict              # siehe SCHALTER

    def __post_init__(self):
        """Fehlende Schlüssel sofort melden, nicht erst beim ersten Aufruf.

        Ohne das wäre ein vergessener Eintrag ein `KeyError` mitten in einem
        Slash-Command oder — schlimmer — ein `None`, das erst beim Aufruf als
        `NoneType is not callable` auffällt. Beides im laufenden Betrieb,
        beides mit stiller `except`-Behandlung drumherum.
        """
        for name, erwartet, ist in (("befehle", BEFEHLE, self.befehle),
                                    ("schalter", SCHALTER, self.schalter)):
            fehlt = [k for k in erwartet if k not in ist]
            zuviel = [k for k in ist if k not in erwartet]
            if fehlt or zuviel:
                raise ValueError(
                    f"BotKontext.{name}: fehlt={fehlt} unbekannt={zuviel}")
        for k in BEFEHLE:
            if not callable(self.befehle[k]):
                raise ValueError(f"BotKontext.befehle[{k!r}] ist nicht aufrufbar")
