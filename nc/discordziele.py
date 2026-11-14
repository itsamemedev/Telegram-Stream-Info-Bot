"""nc.discordziele — die Nutzer-Bereiche auf Discord und der gemeinsame Clip-Kanal (rein).

v4.2-W153 legte je getracktem Nutzer einen Bereich an (Kategorie `🎯 name`
mit Clips-, Chat- und Voice-Kanal) und loeschte ihn beim Entfernen wieder.

v4.2-W168, entschieden vom Betreiber am 07.11.: das wurde unterbunden — alle
Clips in EINEN Kanal (`clip_kanal()`), die alten Bereiche umgezogen und
geloescht.

v5.11-W209, der Betreiber am 14.11.: „irgendwie sind die getrackten Nutzer
samt Aufnahmen, Channel und Hype-Channel verschwunden. Das sollte doch der
/setup-Befehl regeln. Aber dieser erstellt nur ein paar Standard-Channel."
Fuer Telegram war W168 schon mit W175 zurueckgenommen (wieder ein Thema je
Nutzer); in Discord zog ein Automat alle zehn Minuten jeden 🎯-Bereich in den
gemeinsamen Kanal und loeschte ihn. Jetzt wieder: je getracktem Nutzer ein
Bereich mit `-aufnahmen`, `-chat` und `-hype`; ganze Aufnahmen und Hype-Clips
gehen dorthin, `#clips` ist nur noch Rueckfall. **Geloescht wird nichts mehr
automatisch** — ein Bereich, dessen Nutzer nicht mehr getrackt wird, bleibt
stehen und wird gemeldet („verwaist"). Die Loeschregel aus W161
(`loeschbar()`) bleibt als Herkunftsbeweis fuer diese Meldung.

Hier stehen die Entscheidungen, bot-frei und pruefbar; das Anlegen und
Einsortieren selbst macht discordbot.py.
"""

import logging
import re
import time

from nc import meldetakt as _takt
from nc.discordrang import slug as _slug

log = logging.getLogger("TikTokBot")

PRAEFIX = "🎯 "

# v5.11-W209: die drei Kanaele eines Bereichs — Aufnahmen (ganze Aufnahme in
# Teilen), Chat (Community zum Streamer) und Hype (Highlight-Clips).
ARTEN = ("aufnahmen", "chat", "hype")
THEMEN = {
    "aufnahmen": "🎬 Ganze Aufnahmen von @{nutzer}",
    "chat": "💬 Alles rund um @{nutzer}",
    "hype": "🔥 Hype-Momente und Highlights von @{nutzer} · ⭐ = Vote für Clip-of-the-Week",
}

# Discord erlaubt 500 Kanaele je Server, Kategorien eingerechnet. Die Reserve
# haelt Platz fuer Kanaele, die der Betreiber von Hand anlegt — ein Server,
# den der Bot bis auf den letzten Platz fuellt, laesst niemanden mehr etwas
# anlegen.
LIMIT_KANAELE = 500
RESERVE = 25


def bereich_name(username) -> str:
    """„@Anna_K" -> „🎯 anna-k" (Kategorie des Nutzers)."""
    return PRAEFIX + _slug(username)


def kanal_name(username, art) -> str:
    """„@Anna_K", „hype" -> „anna-k-hype"."""
    if art not in ARTEN:
        raise ValueError("unbekannte Kanalart: %r" % (art,))
    return "%s-%s" % (_slug(username), art)


def eigene_kanaele(slug) -> set:
    """Die Kanaele, die der Bot in einem Bereich anlegt — seit W209 die drei
    aus ARTEN, dazu die aus W153 (`-clips`, Voice), damit ein alter Bereich
    weiter als „vom Bot" erkannt wird. Discord schreibt Textkanaele klein und
    ohne Leerzeichen; der Slug ist das schon."""
    return ({"%s-%s" % (slug, a) for a in ARTEN}
            | {"%s-clips" % slug, "%s 🔊" % slug})


def loeschbar(kategoriename, kanalnamen) -> bool:
    """Darf der Abgleich diese Kategorie samt Kanaelen loeschen?

    v4.2-W161: das Praefix allein ist kein Beweis der Herkunft. `🎯 ` ist ein
    gewoehnliches Emoji; eine Kategorie „🎯 Ziele", die jemand von Hand
    angelegt hat, waere als „nicht mehr getrackt" mitsamt ihren Kanaelen und
    deren Verlauf geloescht worden — nicht rueckholbar. Geloescht wird jetzt
    nur, was nach Name UND Inhalt von uns stammt: unsere Kategorie, darin
    nichts als die Kanaele, die wir selbst anlegen. Ein fremder Kanal darin
    (von Hand dazugelegt) sperrt das Loeschen ebenso."""
    if not (kategoriename or "").startswith(PRAEFIX):
        return False
    slug = kategoriename[len(PRAEFIX):]
    return set(kanalnamen or ()) <= eigene_kanaele(slug)


# ══════════════════════════════════════════════════════════════════════════
# v4.2-W168: EIN Clip-Kanal statt eines Bereichs je Nutzer
# ══════════════════════════════════════════════════════════════════════════
#
# Entschieden vom Betreiber am 07.11.: „das sollte unterbunden werden …
# alle anderen Channel loeschen" — gewaehlt: „Ein Clip-Kanal, Rest loeschen".
# Je getracktem Nutzer eine Kategorie mit drei Kanaelen (W153) wuchs mit jedem
# Tracking und streute die Clips ueber den ganzen Server. Ab jetzt gehen alle
# Clips in EINEN Kanal; die Bereiche werden umgezogen (Clips umkopiert) und
# danach geloescht — weiterhin nur, was nachweislich vom Bot stammt
# (`loeschbar`, W161).

CLIP_KANAL_VORGABE = "clips"


def clip_kanal(env=None) -> str:
    """Name des gemeinsamen Clip-Kanals (DISCORD_CLIP_CHANNEL, Vorgabe „clips").
    Discord schreibt Textkanaele klein und ohne Leerzeichen — der Name wird
    deshalb genauso geformt, sonst faende die Suche den angelegten Kanal nie."""
    import os
    import re
    roh = (env.get("DISCORD_CLIP_CHANNEL") if env is not None
           else os.getenv("DISCORD_CLIP_CHANNEL", "clips")) or ""
    roh = roh.strip()
    name = re.sub(r"[^a-z0-9_-]+", "-", roh.lower()).strip("-")
    return name or CLIP_KANAL_VORGABE


_MARKE = "\n-# ↪ umgezogen · "


def umzugsmarke(quell_id) -> str:
    """Die Zeile, an der eine umgezogene Kopie ihre Quelle erkennt (Review
    #210). `-#` ist Discords Kleintext — sichtbar, aber unauffaellig."""
    return "%s%d" % (_MARKE, int(quell_id))


def umzugsmarke_lesen(text):
    """Quell-ID aus einer Kopie — oder 0, wenn der Text keine Marke traegt."""
    _, gefunden, rest = (text or "").rpartition(_MARKE)
    return int(rest) if gefunden and rest.isdigit() else 0


def clip_kanal_des_bereichs(kategoriename) -> str:
    """Der Clip-Kanal eines alten Nutzer-Bereichs („🎯 anna" -> „anna-clips")."""
    return "%s-clips" % (kategoriename or "")[len(PRAEFIX):]


async def clip_kanal_holen(gilden, bevorzugt=0, name=None, anlegen=True):
    """Den gemeinsamen Clip-Kanal finden — und, wenn er fehlt, anlegen.

    Gesucht wird zuerst in der Guild `bevorzugt` (DISCORD_GUILD_ID), dann in
    jeder anderen. Angelegt wird in der ersten Guild der Reihe; ein fehlendes
    Recht wirft (discord.Forbidden) und der Aufrufer meldet es — bis W168
    endete ein fehlender Kanal auf log.debug, und ein Clip verschwand still.
    -> Kanal oder None (keine Guild, oder anlegen=False und nichts gefunden).
    Bot-frei: arbeitet mit dem, was discord.py an Guild-Objekten liefert."""
    name = name or clip_kanal()
    reihe = sorted(gilden or (), key=lambda g: getattr(g, "id", 0) != bevorzugt)
    treffer = next((ch for g in reihe for ch in getattr(g, "text_channels", ())
                    if ch.name == name), None)
    if treffer is None and anlegen and reihe:
        treffer = await reihe[0].create_text_channel(
            name, topic="Highlights aller getrackten Streamer · ⭐ = Vote für Clip-of-the-Week")
    return treffer



# ══════════════════════════════════════════════════════════════════════════
# v5.11-W209: wieder ein Bereich je getracktem Nutzer
# ══════════════════════════════════════════════════════════════════════════

def plan(getrackt, kategorien) -> dict:
    """Was der Abgleich tun soll — und was er nur melden darf.

    getrackt     Nutzernamen (beliebige Schreibweise, Dubletten erlaubt)
    kategorien   {Kategoriename: [Kanalnamen]} des Servers

    -> {"anlegen": [nutzer], "ergaenzen": {nutzer: [fehlende Kanaele]},
        "verwaist": [Kategoriename]}

    Angelegt wird je Slug einmal (zwei Schreibweisen desselben Nutzers sind
    ein Bereich). Ergaenzt wird nur, was fehlt — ein Kanal, den der
    Betreiber in den Bereich gelegt hat, bleibt unberuehrt. Verwaist ist ein
    Bereich des Bots, dessen Nutzer nicht mehr getrackt wird: er wird NUR
    gemeldet. Geloescht wird nichts (W209: „verschwunden" war die Beschwerde)."""
    kategorien = kategorien or {}
    soll = {}
    for u in getrackt or ():
        u = str(u or "").strip().lstrip("@")
        if u:
            soll.setdefault(_slug(u), u)
    anlegen, ergaenzen = [], {}
    for s, u in sorted(soll.items()):
        name = PRAEFIX + s
        if name not in kategorien:
            anlegen.append(u)
            continue
        fehlt = [kanal_name(u, a) for a in ARTEN if kanal_name(u, a) not in set(kategorien[name])]
        if fehlt:
            ergaenzen[u] = fehlt
    verwaist = sorted(n for n, kanaele in kategorien.items()
                      if n.startswith(PRAEFIX) and n[len(PRAEFIX):] not in soll
                      and loeschbar(n, kanaele))
    return {"anlegen": anlegen, "ergaenzen": ergaenzen, "verwaist": verwaist}


def platz(vorhanden) -> int:
    """Wie viele Kanaele (Kategorien eingerechnet) der Bot noch anlegen darf."""
    return max(0, LIMIT_KANAELE - RESERVE - int(vorhanden or 0))


_ART_TEXT = re.compile(r"(🎬 Aufnahme|✂ Highlight|🔥|Highlight|Hype)?[^@\n]*@([A-Za-z0-9_.]+)")


def einsortieren(text):
    """Text einer Nachricht in #clips -> (Kanalart, Nutzer) oder (None, None).

    Erkannt wird, was der Bot selbst dort gepostet hat: ganze Aufnahmen
    („🎬 Aufnahme @name · …", nc.discordaufnahme.beschriftung) gehen nach
    `-aufnahmen`, alles andere mit einem @Namen (Highlight-Clips, Hype,
    Zusammenschnitte) nach `-hype`. Discord-Markdown-Escapes (`anna\\_k`)
    werden vorher aufgeloest. Ohne @Namen bleibt die Nachricht, wo sie ist —
    raten waere schlimmer als liegen lassen."""
    roh = re.sub(r"\\(.)", r"\1", str(text or ""))
    roh = roh.split(_MARKE, 1)[0]
    t = _ART_TEXT.search(roh)
    nutzer = t.group(2).rstrip(".") if t else ""
    if not nutzer:
        # Kein Befund, kein Fehler: eine Nachricht ohne @Namen (von Hand
        # gepostet, Umfrage, Ankuendigung) bleibt, wo sie ist.
        return None, None
    art = "aufnahmen" if "🎬 Aufnahme" in roh.split("@", 1)[0] else "hype"
    return art, nutzer


def bereiche_an(env=None) -> bool:
    """DISCORD_BEREICHE (Vorgabe an): Aufnahmen und Hype-Clips in den Bereich
    des Nutzers. 0 = alles in den gemeinsamen Clip-Kanal (wie W168)."""
    import os
    roh = (env.get("DISCORD_BEREICHE") if env is not None
           else os.getenv("DISCORD_BEREICHE", "1")) or "1"
    return roh.strip().lower() not in ("0", "false", "nein", "no", "off", "aus")


def gilde_waehlen(gilden, bevorzugt=0):
    """Die Guild fuer Bereiche: DISCORD_GUILD_ID, sonst die erste."""
    gilden = list(gilden or ())
    return next((g for g in gilden if getattr(g, "id", 0) == bevorzugt),
                gilden[0] if gilden else None)


class KeinPlatz(Exception):
    """Der Server hat keinen Platz mehr fuer einen weiteren Bereich."""


_SPERRE = {"obj": None}


def _sperre():
    """Eine Sperre fuer alles Anlegen: zwei Clips desselben neuen Nutzers zur
    selben Zeit legten sonst zwei Kategorien „🎯 anna" an."""
    import asyncio
    if _SPERRE["obj"] is None:
        _SPERRE["obj"] = asyncio.Lock()
    return _SPERRE["obj"]


async def bereich_kanal_holen(gilde, username, art, anlegen=True):
    """Den Kanal `art` im Bereich des Nutzers finden — und, wenn er fehlt,
    samt Kategorie anlegen. -> Kanal, oder None (anlegen=False und nicht da).

    Wirft KeinPlatz, wenn der Server voll ist, und discord.Forbidden, wenn
    das Recht fehlt — der Aufrufer faellt dann auf #clips zurueck und sagt es
    laut. Bot-frei: arbeitet mit dem, was discord.py an Objekten liefert."""
    kname, bname = kanal_name(username, art), bereich_name(username)

    def _suchen():
        cat = next((c for c in getattr(gilde, "categories", ()) if c.name == bname), None)
        ch = next((c for c in (getattr(cat, "text_channels", ()) if cat else ())
                   if c.name == kname), None)
        return cat, ch
    cat, ch = _suchen()
    if ch is not None or not anlegen:
        return ch
    async with _sperre():
        cat, ch = _suchen()                  # ein anderer war schneller
        if ch is not None:
            return ch
        noetig = 1 if cat is not None else 1 + 1
        if platz(len(getattr(gilde, "channels", ()))) < noetig:
            raise KeinPlatz("%d Kanaele belegt, Grenze %d (Reserve %d)" % (
                len(getattr(gilde, "channels", ())), LIMIT_KANAELE, RESERVE))
        if cat is None:
            cat = await gilde.create_category(bname, reason="v5.11-W209: Bereich je getracktem Nutzer")
        nutzer = str(username or "").lstrip("@")
        return await cat.create_text_channel(kname, topic=THEMEN[art].format(nutzer=nutzer))


async def ziel_kanal(gilden, bevorzugt, username, art):
    """Wohin ein Clip oder eine Aufnahme geht. -> (Kanal oder None, Rueckfallgrund).

    Erst der Bereich des Nutzers (DISCORD_BEREICHE an), sonst — oder wenn
    der Bereich nicht angelegt werden kann — der gemeinsame Clip-Kanal. Der
    Grund ist leer, wenn es der Bereich wurde; sonst sagt er, warum nicht,
    damit der Aufrufer es melden kann (ein stiller Rueckfall war die Klasse
    Fehler, die W209 behoben hat: es sah aus, als waere alles verschwunden)."""
    gilde = gilde_waehlen(gilden, bevorzugt)
    grund = ""
    if bereiche_an() and gilde is not None and username:
        try:
            ch = await bereich_kanal_holen(gilde, username, art)
            if ch is not None:
                return ch, ""
        except Exception as e:                      # KeinPlatz, discord.Forbidden, HTTPException
            grund = ("kein Platz fuer den Bereich (%s)" % e if isinstance(e, KeinPlatz)
                     else "%s: %s" % (type(e).__name__, e))
            _rueckfall_melden(username, art, grund)
    elif not bereiche_an():
        grund = "DISCORD_BEREICHE=0"
    ch = await clip_kanal_holen(gilden, bevorzugt)
    return ch, grund or ("kein Server" if gilde is None else "kein Nutzername")


def _rueckfall_melden(username, art, grund):
    """Ging etwas nach #clips statt in den Bereich: laut und gedrosselt — ein
    stiller Rueckfall sah aus wie „alles verschwunden" (W209). Der Schluessel
    ist der Grund, nicht der Nutzer: bei 40 Trackings und fehlendem Recht
    waere es sonst eine Zeile je Clip (W97)."""
    laut, weg = _takt.melden("discord-bereich-rueckfall", str(grund)[:60], time.monotonic())
    if laut:
        log.error("Discord: %s @%s nicht im Bereich des Nutzers, sondern in #%s: %s. Abhilfe: "
                  "dem Bot „Kanaele verwalten\" geben oder /setup_community ausfuehren.%s",
                  "Aufnahme" if art == "aufnahmen" else "Clip", str(username or "").lstrip("@"),
                  clip_kanal(), grund, _takt.zusatz(weg))
