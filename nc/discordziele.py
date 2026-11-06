"""nc.discordziele — welche User-Bereiche auf Discord anzulegen und zu loeschen sind (rein).

v4.2-W153. Gemeldet: „discord, wo alle getrackten User einen Channel bekommen
sollten und die, die nicht mehr getrackt sind, die Channel sollten gelöscht
werden." Bis hierher gab es dafuer nur `/setup_targets` — von Hand, nur
anlegend, gedeckelt auf DISCORD_TARGET_CAP und nur fuer NICHT pausierte
Trackings. Ein neu getrackter User bekam seinen Bereich erst, wenn jemand den
Befehl tippte; ein entfernter behielt ihn fuer immer.

Hier steht die Entscheidung, bot-frei und pruefbar; das Anlegen und Loeschen
selbst macht discordbot.py. Drei Regeln tragen die Sicherheit:

1. **Geloescht wird nur, was wir erkennbar selbst angelegt haben** — eine
   Kategorie mit dem Praefix `🎯 `, die nur unsere Kanaele traegt
   (`loeschbar()`, v4.2-W161). Alles andere auf dem Server ist tabu.
2. **Ohne Bestand kein Loeschen.** Eine leere Tracking-Liste heisst
   wahrscheinlicher „Datenbank nicht da" (frisch umgezogen, falsch
   konfiguriert — W143 hat genau so eine leere MariaDB gezeigt) als „der
   Betreiber hat alle entfernt". Dasselbe Prinzip wie BestandUnbekannt (W91).
3. **Kein Massenloeschen im Automaten.** Wuerde ein Lauf mehr als die Haelfte
   der Bereiche (und mehr als drei) loeschen, loescht er nichts und meldet
   es; `/setup_targets` darf es dann ausdruecklich. Geloeschte Kanaele nehmen
   ihren Verlauf mit — das ist nicht rueckholbar.

Pausierte Trackings zaehlen als getrackt: pausieren heisst „gerade nicht
aufnehmen", nicht „Kanal weg".
"""

from nc import discordrang as _rang

PRAEFIX = "🎯 "
# Eine Kategorie plus Clips-, Chat- und Voice-Kanal.
KANAELE_JE_USER = 4
# Discord-Grenze: 500 Kanaele je Server, Kategorien eingeschlossen.
SERVER_GRENZE = 500
MASSEN_ANTEIL = 0.5
MASSEN_MINDEST = 3


def kategorie(username) -> str:
    return PRAEFIX + _rang.slug(username)


def eigene_kanaele(slug) -> set:
    """Die Kanaele, die discordbot._provision_user_channels in einem Bereich
    anlegt. Discord schreibt Textkanaele klein und ohne Leerzeichen; der Slug
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


def plan(getrackt, vorhanden, belegt, erzwingen=False) -> dict:
    """-> {"anlegen": [username], "loeschen": [kategoriename],
            "zurueckgestellt": [username], "grund": str}

    getrackt:  Benutzernamen aller Trackings (auch pausierte)
    vorhanden: Namen ALLER Kategorien auf dem Server
    belegt:    Zahl der Kanaele auf dem Server (Kategorien eingeschlossen)
    erzwingen: True nur aus /setup_targets — hebt den Massen-Riegel auf,
               nie den Riegel „ohne Bestand kein Loeschen"
    """
    soll = {}
    for u in getrackt or ():
        if u:
            soll.setdefault(kategorie(u), u)          # gleiche Slugs: einer genuegt
    unsere = {k for k in (vorhanden or ()) if k.startswith(PRAEFIX)}
    loeschen = sorted(unsere - set(soll))
    grund = ""
    if not soll:
        loeschen, grund = [], "keine Trackings gelesen — es wird nichts geloescht"
    elif not erzwingen and len(loeschen) > MASSEN_MINDEST \
            and len(loeschen) > MASSEN_ANTEIL * max(1, len(unsere)):
        grund = ("%d von %d Bereichen waeren zu loeschen — zu viele fuer den Automaten; "
                 "/setup_targets loescht sie ausdruecklich" % (len(loeschen), len(unsere)))
        loeschen = []
    fehlt = [soll[k] for k in sorted(soll) if k not in unsere]
    frei = SERVER_GRENZE - int(belegt) + KANAELE_JE_USER * len(loeschen)
    passt = max(0, frei // KANAELE_JE_USER)
    return {"anlegen": fehlt[:passt], "loeschen": loeschen,
            "zurueckgestellt": fehlt[passt:], "grund": grund}
