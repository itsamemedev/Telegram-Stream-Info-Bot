"""nc.discordziele — die Nutzer-Bereiche auf Discord und der gemeinsame Clip-Kanal (rein).

v4.2-W153 legte je getracktem Nutzer einen Bereich an (Kategorie `🎯 name`
mit Clips-, Chat- und Voice-Kanal) und loeschte ihn beim Entfernen wieder.

v4.2-W168, entschieden vom Betreiber am 07.11.: das wird unterbunden. Alle
Clips gehen in EINEN Kanal (`clip_kanal()`), die alten Bereiche werden
umgezogen (Clips umkopiert) und danach geloescht. Angelegt wird kein Bereich
mehr. Die Loeschregel aus W161 gilt unveraendert: geloescht wird nur, was
nach Name UND Inhalt vom Bot stammt (`loeschbar()`) — eine von Hand angelegte
`🎯 `-Kategorie bleibt tabu, ihr Verlauf ist nicht rueckholbar.

Hier steht die Entscheidung, bot-frei und pruefbar; das Umziehen und Loeschen
selbst macht discordbot.py.
"""

PRAEFIX = "🎯 "


def eigene_kanaele(slug) -> set:
    """Die Kanaele, die discordbot._provision_user_channels (bis W168) in einem
    Bereich anlegte. Discord schreibt Textkanaele klein und ohne Leerzeichen; der Slug
    ist das schon."""
    return {"%s-clips" % slug, "%s-chat" % slug, "%s 🔊" % slug}


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
