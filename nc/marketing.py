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

from dataclasses import dataclass, field

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
