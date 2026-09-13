"""nc.discordrang — v4.2-W71: Rang-Rechnung des Discord-Teils, bot-frei.

Diese vier Dinge steckten als Closures rund 330 Zeilen tief in
`_discord_run_once` — der mit 1730 Zeilen groessten Funktion des ganzen
Bestands. Sie sind reine Rechnung: kein `discord`, kein Netz, kein Zustand.
Dort drin waren sie weder einzeln aufrufbar noch pruefbar, und die
XP-Schwelle stand zusaetzlich zweimal woertlich im Code daneben
(`100 * (lvl + 1) * (lvl + 1)` in /rank und in /profile).

Bot-frei heisst hier auch discord-frei: dieses Modul importiert die
Bibliothek nicht. Das Anlegen der Rollen bleibt in discordbot.py, weil es ein
Guild-Objekt braucht — hier steht nur, WELCHE Raenge es gibt und ab wann.
"""

import re

# (ab Level, Name, Farbe). Reihenfolge aufsteigend — `rang_fuer_level` laeuft
# sie durch und behaelt den letzten Treffer, damit ein Level ueber der
# hoechsten Stufe nicht durchfaellt.
RANG_STUFEN = (
    (1,  "GHOST",      0x5a6472),
    (3,  "RUNNER",     0x00e5ff),
    (7,  "NETRUNNER",  0x00ff9c),
    (15, "ICEBREAKER", 0xffb000),
    (25, "LEGENDE",    0xff2e88),
)


def xp_fuer_level(lvl: int) -> int:
    """XP-Schwelle fuer Level `lvl`. -> 100 * lvl^2

    Level 1 = 100, 2 = 400, 3 = 900. Stand vor W71 zweimal woertlich im
    Anzeigecode; wer die Kurve aendern wollte, musste drei Stellen finden.
    """
    return 100 * lvl * lvl


def xp_zu_level(xp: int) -> int:
    """Wie viele Level sind mit `xp` erreicht? -> int

    Bewusst die Schleife von frueher und keine Wurzel-Formel. Beim Umzug
    einer laufenden Rechnung ist Gleichheit wichtiger als Eleganz: eine
    geschlossene Form kann an den Rundungsraendern um eins danebenliegen,
    und das faellt erst auf, wenn jemandem ein Level fehlt.
    """
    lvl = 0
    while xp >= xp_fuer_level(lvl + 1):
        lvl += 1
    return lvl


def rang_fuer_level(lvl: int):
    """Der hoechste erreichte Rangname, oder None unterhalb der ersten Stufe."""
    name = None
    for noetig, rname, _farbe in RANG_STUFEN:
        if lvl >= noetig:
            name = rname
    return name


def slug(username: str) -> str:
    """TikTok-Name -> Discord-tauglicher Kanal-/Rollenbestandteil.

    Discord erlaubt in Kanalnamen keine Grossbuchstaben und keine
    Sonderzeichen; 90 Zeichen sind der Riegel gegen den Namenslaengen-Fehler
    beim Anlegen. Leerer Rest wird zu "user", damit nie ein Kanal "#-clips"
    entsteht.
    """
    s = re.sub(r"[^a-z0-9]+", "-", (username or "").lstrip("@").lower()).strip("-")
    return (s or "user")[:90]


# Funktionale Rollen mit Rechten und Farben, zusaetzlich zu den Rang-Rollen.
# (Name, Farbe, hoist=getrennt anzeigen, {Permission: True})
#
# v4.2-W72: ebenfalls reine Daten und deshalb hier statt in der Closure. Die
# Rechte stehen als einfache Wahrheitswerte da und nicht als
# discord.Permissions — dieses Modul kennt die Bibliothek nicht, und
# discordbot.py baut daraus das, was Discord sehen will.
TEAM_ROLLEN = (
    ("\U0001f451 Owner",     0xff2e88, True,  {"administrator": True}),
    ("\U0001f6e1 Moderator", 0xffb000, True,  {"kick_members": True, "ban_members": True,
                                       "manage_messages": True, "moderate_members": True,
                                       "manage_nicknames": True, "mute_members": True,
                                       "deafen_members": True, "move_members": True}),
    ("\U0001f3ac Streamer",  0x00ff9c, True,  {"priority_speaker": True, "stream": True}),
    ("\u2b50 VIP",        0x00e5ff, True,  {}),
    ("\U0001f916 Bot",        0x8892a0, False, {}),
    ("\U0001f464 Member",     0x5a6472, False, {}),
)
