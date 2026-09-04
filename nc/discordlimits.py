"""nc.discordlimits — v4.0-W80: Discord-Upload-Limit level-genau bestimmen.

Aus dem Monolithen extrahiert (reine Logik, kein discord-Import, voll testbar).

WARUM: Discord senkte 2024 das Free-Limit auf 10 MB; Server-Boosts heben es an
(Level 2 = 50 MB, Level 3 = 100 MB; Level 1 je nach Discord-Policy). Das GUILD
kennt sein echtes Limit über `guild.filesize_limit` (Bytes) — es folgt dem
Boost-Level UND Discords Richtlinien-Änderungen automatisch. Deshalb ist das
Guild-Limit die WAHRHEIT; die Env-Variable DISCORD_UPLOAD_LIMIT_MB ist nur ein
optionaler Betreiber-Deckel (z. B. für langsame Leitungen), der NUR greift, wenn
explizit gesetzt — ein Default darf einen bezahlten Boost nicht aushebeln.

Der alte Code rechnete `min(env_default=10, guild)` → auf einem geboosteten
Server wurde alles auf 10 MB heruntergerechnet, der Boost verpuffte.
"""

FREE_DEFAULT_MB = 10   # Discord-Free-Limit (Stand: seit Ende 2024)
FLOOR_MB = 8           # nie unter diesen Wert komprimieren (Qualität)


def guild_limit_mb(filesize_limit_bytes) -> int:
    """`guild.filesize_limit` (Bytes) → ganze MB. 0 wenn unbekannt/ungültig."""
    try:
        mb = int(filesize_limit_bytes) // (1024 * 1024)
        return mb if mb > 0 else 0
    except (TypeError, ValueError):
        return 0


def effective_upload_mb(filesize_limit_bytes, env_override_mb=None,
                        floor_mb: int = FLOOR_MB) -> int:
    """Der EFFEKTIVE harte Upload-Deckel in MB.

    - filesize_limit_bytes: das echte Guild-Limit (kennt Boost-Level + Policy).
    - env_override_mb: DISCORD_UPLOAD_LIMIT_MB NUR wenn der Betreiber es explizit
      gesetzt hat (sonst None) — deckelt dann nach unten, hebt aber nie an.
    Guild-Limit ist autoritativ; fehlt es, greift der konservative Free-Default.
    Ergebnis nie unter floor_mb.
    """
    guild_mb = guild_limit_mb(filesize_limit_bytes)
    base = guild_mb if guild_mb > 0 else FREE_DEFAULT_MB
    if env_override_mb is not None:
        try:
            ov = int(env_override_mb)
            if ov > 0:
                base = min(base, ov)   # expliziter Betreiber-Deckel (nur senken)
        except (TypeError, ValueError):
            pass
    return max(floor_mb, base)


def gate_mb(effective_mb: int, margin_mb: int = 1, floor_mb: int = FLOOR_MB) -> int:
    """Schwelle, ab der VOR dem Upload komprimiert wird — knapp unter dem harten
    Deckel, weil Discord auch 25.1 MB bei einem 25er-Cap ablehnt (Container-/
    Multipart-Overhead zählt mit). Nie unter floor_mb."""
    return max(floor_mb, int(effective_mb) - max(0, int(margin_mb)))


def describe(filesize_limit_bytes, env_override_mb=None) -> str:
    """Kurzlabel fürs Dashboard, z. B. '50 MB (Server-Level)' oder
    '10 MB (Free)' bzw. '10 MB (Betreiber-Limit)'."""
    guild_mb = guild_limit_mb(filesize_limit_bytes)
    eff = effective_upload_mb(filesize_limit_bytes, env_override_mb)
    if env_override_mb is not None:
        try:
            if int(env_override_mb) > 0 and int(env_override_mb) <= (guild_mb or FREE_DEFAULT_MB):
                return f"{eff} MB (Betreiber-Limit)"
        except (TypeError, ValueError):
            pass
    if guild_mb > FREE_DEFAULT_MB:
        return f"{eff} MB (Server-Level)"
    return f"{eff} MB (Free)"


# ─────────────────────────────────────────────────────────────────────────────
# v4.2-W1: das AKTUELLE Limit — die Seite, die den laufenden Client kennt.
#
# Bis hierher war dieses Modul reine Rechnung: Bytes rein, MB raus. Wer das
# Ergebnis wollte, musste im Bot `_discord_guild_filesize_bytes()` rufen, und
# genau das hing `/api/system/config_snapshot` am Monolithen fest.
#
# Der verbundene Client liegt seit v4.1-W16 als Register in nc/discordstate.py,
# die Guild-ID und der Betreiber-Deckel kommen per configure(). Damit kann das
# Limit von hier aus beantwortet werden, ohne dass jemand aus bot.py importiert.
from nc import discordstate as _discordstate

_KONF = {"guild_id": 0, "override_mb": None}


def configure(guild_id=None, override_mb=None):
    """Vom Bot einmal beim Start gerufen."""
    if guild_id is not None:
        _KONF["guild_id"] = guild_id
    _KONF["override_mb"] = override_mb


def guild_filesize_bytes():
    """v4.0-W80: filesize_limit des verbundenen Guilds (Bytes) — kennt das
       Boost-Level. 0, wenn (noch) kein Client/Guild verbunden ist."""
    try:
        cli = _discordstate.CLIENT["obj"]
        if cli and getattr(cli, "guilds", None):
            gid = _KONF["guild_id"] or 0
            gs = list(cli.guilds)
            g = next((x for x in gs if getattr(x, "id", 0) == gid), None) or (gs[0] if gs else None)
            if g is not None:
                return int(getattr(g, "filesize_limit", 0) or 0)
    except Exception:
        pass
    return 0


def aktuell_mb():
    """Das Limit, das JETZT gilt — Guild-Wahrheit gedeckelt vom Betreiber."""
    return effective_upload_mb(guild_filesize_bytes(), _KONF["override_mb"])


def aktuell_label():
    """Kurzlabel fürs Dashboard, z. B. '50 MB (Server-Level)'."""
    return describe(guild_filesize_bytes(), _KONF["override_mb"])
