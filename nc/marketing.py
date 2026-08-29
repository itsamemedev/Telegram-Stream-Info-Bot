"""nc.marketing — B162: Cross-Promo-Agent fuer die eigenen Kanaele + Website.

════════════════════════════════════════════════════════════════════════
WAS DER AGENT TUT — UND WAS BEWUSST NICHT
════════════════════════════════════════════════════════════════════════
Er bewirbt die EIGENEN Kanaele (Kick/Twitch/YouTube) und die Website auf den
Flaechen, die der Betreiber selbst besitzt: dem eigenen Discord (Webhook) und
Telegram. Er postet NICHT in fremde Communities, schreibt keine Nutzer an und
braucht keine neuen Plattform-Keys — genau deshalb ist er ohne Ban-Risiko
einschaltbar. Reichweite ausserhalb der eigenen Audience (X, Reddit …) ist eine
eigene, groessere Baustelle mit eigenen Zugangsdaten und bleibt hier aussen vor.

════════════════════════════════════════════════════════════════════════
WARUM BOT-FREI
════════════════════════════════════════════════════════════════════════
Wie nc.restream_guard/nc.restream_testpush steckt die Entscheidung — DARF und
SOLL jetzt gepostet werden? — in reinen Funktionen ohne Netz, ohne DB, ohne
asyncio. Der Bot liefert nur die Fakten (Uhrzeit, letzter Post, live?) und fuehrt
das Posten aus. So ist die Anti-Spam-Logik vollstaendig testbar und kann nicht
durch einen Seiteneffekt im Monolithen kippen — ein Marketing-Agent, der aus
Versehen im Minutentakt sendet, ist schlimmer als keiner.

DIE REGELN GEGEN SPAM (in should_post, Reihenfolge = zuerst greift zuerst):
1. AUS ist AUS. Ohne enabled passiert nichts.
2. MANUELL-ZUERST. Ohne auto=True postet der Hintergrund-Loop NIE von selbst;
   der Betreiber sendet dann nur ueber den Knopf.
3. RUHEZEITEN. Innerhalb quiet_start..quiet_end wird nicht gepostet.
4. MINDESTABSTAND (min_gap_hours). Harte Untergrenze zwischen zwei Posts —
   faengt auch eine fehlkonfigurierte Cadence ab.
5. CADENCE. Regulaerer Abstand fuer den naechsten Auto-Post.
Ein manueller Post ueber den Knopf umgeht 3–5 bewusst (der Mensch hat entschieden),
aktualisiert aber den Zeitstempel — der naechste Auto-Post haelt wieder Abstand.
"""

import asyncio
import os
import time as _time_mod
from dataclasses import dataclass, field

from nc import freeai as _nc_freeai
from nc.cfgstore import get as _cfg_get, set_ as _cfg_set
from nc.envnum import env_int as _env_int

DISCORD = "discord"
TELEGRAM = "telegram"
TARGETS = (DISCORD, TELEGRAM)


@dataclass
class MarketingConfig:
    enabled: bool = False
    auto: bool = False                 # Hintergrund-Loop postet selbststaendig? (Default: nur manuell)
    targets: tuple = ()                # Teilmenge von TARGETS
    cadence_hours: float = 6.0         # regulaerer Auto-Abstand
    min_gap_hours: float = 3.0         # harte Anti-Spam-Untergrenze
    quiet_start: int = 23              # Ruhezeit-Beginn (Stunde 0-23)
    quiet_end: int = 8                 # Ruhezeit-Ende; start==end → keine Ruhezeit
    only_when_live: bool = False       # nur posten, wenn ein eigener Restream laeuft
    channels: dict = field(default_factory=dict)   # {"Kick": url, "Twitch": url, ...}
    website: str = ""
    invite: str = ""                   # Discord-Invite-URL


@dataclass
class MarketingState:
    last_post_ts: float = 0.0
    count: int = 0


def _in_quiet(hour: int, qs: int, qe: int) -> bool:
    """Ruhezeitfenster inklusive Mitternachts-Ueberlauf (23..8)."""
    qs %= 24
    qe %= 24
    if qs == qe:
        return False
    if qs < qe:
        return qs <= hour < qe
    return hour >= qs or hour < qe


def should_post(cfg: MarketingConfig, state: MarketingState, now_ts: float,
                now_hour: int, *, any_live: bool):
    """Reine Auto-Post-Entscheidung. Gibt (bool, grund) zurueck.
       grund ist ein Maschinen-Code fuer Tests/Anzeige."""
    if not cfg.enabled:
        return False, "disabled"
    if not cfg.auto:
        return False, "manual_only"
    if not cfg.targets:
        return False, "no_targets"
    if cfg.only_when_live and not any_live:
        return False, "not_live"
    if _in_quiet(now_hour, cfg.quiet_start, cfg.quiet_end):
        return False, "quiet_hours"
    last = state.last_post_ts or 0.0
    if last:
        gap = now_ts - last
        if gap < cfg.min_gap_hours * 3600:
            return False, "min_gap"
        if gap < cfg.cadence_hours * 3600:
            return False, "cadence"
    return True, "due"


def next_due_ts(cfg: MarketingConfig, state: MarketingState):
    """Wann der naechste Auto-Post frueheestens faellig ist (None = sofort)."""
    if not state.last_post_ts:
        return None
    return state.last_post_ts + max(cfg.cadence_hours, cfg.min_gap_hours) * 3600


def variants():
    """Rotierende Aufhaenger, damit der Post nicht jedes Mal identisch ist."""
    return [
        "Wir sind auf allen Kanaelen unterwegs — schau vorbei!",
        "Verpass keinen Stream — folg uns ueberall:",
        "Alle Kanaele auf einen Blick — sei dabei:",
        "Neu hier? So findest du uns:",
    ]


def _channel_lines(cfg: MarketingConfig):
    return [(n, u) for n, u in cfg.channels.items() if u]


def compose(cfg: MarketingConfig, *, variant: int = 0, flavor: str = None) -> dict:
    """Baut den Promo-Text je Ziel. Rein — kein Netz.
       flavor = optionale, vom Bot ergaenzte KI-Zeile (kann None sein).
       Discord bekommt Markdown, Telegram bewusst Klartext (Telegram
       verlinkt URLs von selbst; kein parse_mode = keine Entity-Fehler)."""
    vs = variants()
    head = vs[variant % len(vs)] if vs else "Folg uns!"
    chans = _channel_lines(cfg)
    fl = (flavor or "").strip()

    d = [f"**📢 {head}**"]
    if fl:
        d.append(fl)
    d.append("")
    for name, url in chans:
        d.append(f"• **{name}**: {url}")
    if cfg.website:
        d.append(f"• 🌐 **Website**: {cfg.website}")
    if cfg.invite:
        d.append(f"• 💬 **Discord**: {cfg.invite}")

    t = [f"📢 {head}"]
    if fl:
        t.append(fl)
    t.append("")
    for name, url in chans:
        t.append(f"• {name}: {url}")
    if cfg.website:
        t.append(f"• 🌐 Website: {cfg.website}")
    if cfg.invite:
        t.append(f"• 💬 Discord: {cfg.invite}")

    return {"discord": "\n".join(d), "telegram": "\n".join(t)}


def has_content(cfg: MarketingConfig) -> bool:
    """Gibt es ueberhaupt etwas zu bewerben? (mind. ein Kanal ODER Website)."""
    return bool(_channel_lines(cfg) or cfg.website or cfg.invite)


# ---------------------------------------------------------------------------
# v4.1-W4: die Bot-Seite des Marketings, aus dem Monolithen geloest.
#
# Bis hierher lag hier nur die bot-freie Anti-Spam- und Textlogik; Config-Bau,
# Zustand und das Senden selbst blieben in bot.py — und damit auch die fuenf
# /api/marketing-Routen, die daran haengen. Erst der Kern, dann die Routen (die
# Reihenfolge aus W117): so kostet nc/routes/marketing.py null nc.ctx-Slots.
#
# Die Koerper sind woertlich uebernommen. Ersetzt wurden nur die Namen, die im
# Monolithen Modul-Globals waren; sie kommen jetzt aus _conf.
# ---------------------------------------------------------------------------


class _Conf(dict):
    """Wirft laut statt einen nackten KeyError zu liefern.

    Ein fehlender Startwert ist ein Verdrahtungsfehler im Bot, kein Datenfehler
    der Route — und er soll den Namen nennen, der fehlt, statt im naechsten
    except-Block zu verschwinden.
    """

    def __missing__(self, key):
        raise RuntimeError(
            "%s ist nicht konfiguriert (%r fehlt) — configure(...) fehlt im "
            "Startpfad von bot.py" % (__name__, key))


_conf = _Conf()


class _LazyLog:
    """Der Logger des Bots, erst beim Zugriff geholt — beim Import ist er None."""

    def __getattr__(self, name):
        return getattr(_conf["log"], name)


log = _LazyLog()


def configure(*, log, get_bot_app, safe_send, get_ai_session, discord_invite,
              discord_webhook_url, allowed_user_ids, kick_channel_url):
    """Vom Bot genau einmal beim Start gerufen.

    get_bot_app ist bewusst ein GETTER: die Telegram-Application entsteht erst
    in run_bot(). Im Monolithen stand dafuer globals().get("bot_app") — in
    einem nc/-Modul waere globals() der MODUL-Namensraum und der Wert fuer
    immer None, also genau die stille Fehlanzeige aus W116. (Dass der Name im
    Bot ueberhaupt gebunden wird, ist der Fix aus W4a.)
    """
    _conf.update(log=log, get_bot_app=get_bot_app, safe_send=safe_send,
                 get_ai_session=get_ai_session, discord_invite=discord_invite,
                 discord_webhook_url=discord_webhook_url,
                 allowed_user_ids=allowed_user_ids,
                 kick_channel_url=kick_channel_url)


def enabled() -> bool:
    return bool(_cfg_get("marketing.enabled",
                         os.getenv("MARKETING_ENABLED", "0").strip().lower() in ("1", "true", "yes", "on")))


def default_targets():
    t = []
    if _conf["discord_webhook_url"]:
        t.append("discord")
    if os.getenv("MARKETING_TG_CHAT_ID", "").strip() or _conf["allowed_user_ids"]:
        t.append("telegram")
    return t


def config() -> "MarketingConfig":
    """Config FRISCH bauen: app_config-Overrides ueber .env-Defaults, Kanal-URLs
       aus den bestehenden Env-Variablen (Modul-Konstanten wuerden .env einfrieren)."""
    stored = _cfg_get("marketing.config", {}) or {}
    channels = {}
    if _conf["kick_channel_url"]:
        channels["Kick"] = _conf["kick_channel_url"]
    _tw = (os.getenv("TWITCH_CHANNEL", "") or "").strip().lstrip("#")
    if _tw:
        channels["Twitch"] = _tw if _tw.startswith("http") else f"https://twitch.tv/{_tw}"
    _yt = (os.getenv("YOUTUBE_CHANNEL", "") or "").strip()
    if _yt:
        channels["YouTube"] = _yt if _yt.startswith("http") else f"https://youtube.com/@{_yt.lstrip('@')}"

    def _b(v, dflt):
        return bool(v) if isinstance(v, bool) else dflt
    return MarketingConfig(
        enabled=enabled(),
        auto=_b(stored.get("auto"), os.getenv("MARKETING_AUTO", "0").strip().lower() in ("1", "true", "yes", "on")),
        targets=tuple(stored.get("targets") or default_targets()),
        cadence_hours=float(stored.get("cadence_hours") or _env_int("MARKETING_CADENCE_HOURS", 6)),
        min_gap_hours=float(stored.get("min_gap_hours") or _env_int("MARKETING_MIN_GAP_HOURS", 3)),
        quiet_start=int(stored.get("quiet_start", _env_int("MARKETING_QUIET_START", 23))),
        quiet_end=int(stored.get("quiet_end", _env_int("MARKETING_QUIET_END", 8))),
        only_when_live=_b(stored.get("only_when_live"),
                          os.getenv("MARKETING_ONLY_WHEN_LIVE", "0").strip().lower() in ("1", "true", "yes", "on")),
        channels=channels,
        website=(os.getenv("MARKETING_WEBSITE_URL", "https://lafap.de").strip()),
        invite=_conf["discord_invite"](),
    )


def state() -> "MarketingState":
    s = _cfg_get("marketing.state", {}) or {}
    return MarketingState(
        last_post_ts=float(s.get("last_post_ts", 0) or 0),
        count=int(s.get("count", 0) or 0))


def state_save(ts, count):
    _cfg_set("marketing.state", {"last_post_ts": ts, "count": int(count)})


async def ai_flavor(cfg) -> "str | None":
    """Optionale KI-Zeile (ein Satz) via freeai. Best-effort — None bei Fehler,
       dann greift die statische Vorlage. self-gated auf MARKETING_AI_FLAVOR."""
    if os.getenv("MARKETING_AI_FLAVOR", "1").strip().lower() not in ("1", "true", "yes", "on"):
        return None
    try:
        names = ", ".join(cfg.channels.keys()) or "unseren Kanaelen"
        msgs = [{"role": "system", "content": "Du bist ein knapper Social-Media-Texter. "
                 "Antworte mit GENAU EINEM kurzen deutschen Satz, ohne Hashtags, ohne Emojis."},
                {"role": "user", "content": f"Schreibe einen einladenden Ein-Satz-Aufruf, "
                 f"unseren Livestream auf {names} und unsere Website zu besuchen."}]
        out = await asyncio.wait_for(_nc_freeai.chat(msgs, timeout=8), timeout=10)
        out = (out or "").strip().replace("\n", " ")
        return out[:200] or None
    except Exception:
        return None


async def post_discord(text: str) -> dict:
    if not _conf["discord_webhook_url"]:
        return {"ok": False, "error": "kein DISCORD_WEBHOOK_URL"}
    try:
        import aiohttp
        session = await _conf["get_ai_session"]()
        async with session.post(_conf["discord_webhook_url"], json={"content": text[:1900]},
                                timeout=aiohttp.ClientTimeout(total=10)) as r:
            return {"ok": r.status in (200, 204), "status": r.status}
    except Exception as e:
        return {"ok": False, "error": str(e)[:160]}


async def post_telegram(text: str) -> dict:
    try:
        chat_id = os.getenv("MARKETING_TG_CHAT_ID", "").strip()
        chat_id = int(chat_id) if chat_id.lstrip("-").isdigit() else (sorted(_conf["allowed_user_ids"])[0] if _conf["allowed_user_ids"] else 0)
    except Exception:
        chat_id = sorted(_conf["allowed_user_ids"])[0] if _conf["allowed_user_ids"] else 0
    if not chat_id:
        return {"ok": False, "error": "kein Telegram-Ziel (MARKETING_TG_CHAT_ID)"}
    _app = _conf["get_bot_app"]()
    if _app is None:
        return {"ok": False, "error": "Bot nicht bereit"}
    await _conf["safe_send"](_app.bot, chat_id, text[:4000])   # _safe_send wirft nie
    return {"ok": True, "chat_id": chat_id}


async def publish(manual: bool = False) -> dict:
    """Komponiert (optional mit KI-Zeile) und postet an alle aktiven Ziele.
       Aktualisiert immer den Zeitstempel — auch der manuelle Post haelt danach Abstand."""
    cfg = config()
    if not has_content(cfg):
        return {"ok": False, "error": "Nichts zu bewerben (keine Kanal-URL/Website gesetzt)"}
    if not cfg.targets:
        return {"ok": False, "error": "Keine Ziele aktiv (Discord-Webhook/Telegram-Chat konfigurieren)"}
    st = state()
    flavor = await ai_flavor(cfg)
    msg = compose(cfg, variant=st.count, flavor=flavor)
    sent = {}
    if "discord" in cfg.targets:
        sent["discord"] = await post_discord(msg["discord"])
    if "telegram" in cfg.targets:
        sent["telegram"] = await post_telegram(msg["telegram"])
    ok = any(v.get("ok") for v in sent.values()) if sent else False
    if ok:
        state_save(_time_mod.time(), st.count + 1)
        log.info("Marketing-Post gesendet (manual=%s, count=%d, Ziele=%s)",
                 manual, st.count + 1, ",".join(k for k, v in sent.items() if v.get("ok")))
    return {"ok": ok, "manual": manual, "sent": sent, "count": st.count + (1 if ok else 0)}
