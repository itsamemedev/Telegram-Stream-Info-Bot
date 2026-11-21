"""nc.discordrang — v4.2-W71: Rang-Rechnung des Discord-Teils, bot-frei.

Diese vier Dinge steckten als Closures rund 330 Zeilen tief in
`_discord_run_once` — der mit 1730 Zeilen groessten Funktion des ganzen
Bestands. Sie sind reine Rechnung: kein `discord`, kein Netz, kein Zustand.
Dort drin waren sie weder einzeln aufrufbar noch pruefbar, und die
XP-Schwelle stand zusaetzlich zweimal woertlich im Code daneben
(`100 * (lvl + 1) * (lvl + 1)` in /rank und in /profile).

Seit DC-1 steht hier auch die Rangfolge der Server-Befehle (unten).

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


# ── DC-1: Rangfolge, bevor der Bot mit SEINEN Rechten handelt ────────────
#
# Die Server-Befehle (/assign_role, /kick, /ban, /set_channel_perms …)
# fragten nur `_is_admin` — „Server verwalten" ODER eine Rolle mit dem
# NAMEN aus DISCORD_ADMIN_ROLE — und handelten danach mit den Rechten des
# Bots. Ein Mitglied mit nur „Server verwalten" gab sich so
# `/assign_role @selbst 👑 Owner` (administrator=True, siehe TEAM_ROLLEN),
# bannte Hoehergestellte und oeffnete #mod-log per /set_channel_perms. Der
# Bot war damit ein Aufzug an Discords eigener Rangfolge vorbei.
#
# Die Regeln hier sind Discords eigene, nur gegen den AUFRUFER statt gegen
# den Bot gerechnet: eine Rolle oder ein Mitglied laesst sich nur verwalten,
# wenn es UNTER der eigenen hoechsten Rolle steht; der Eigentuemer steht
# ueber allem. Wer keine Rangfolge erkennen laesst, darf nichts — ein
# fehlendes `top_role` ist kein Freibrief.

# Rechte, die eine Rolle zum Werkzeug gegen den Server machen. Vergeben darf
# sie nur, wer selbst Administrator ist: sonst reicht „Server verwalten",
# um sich „Rollen verwalten" zu geben, und von dort jede Rolle darunter.
MACHT_RECHTE = ("administrator", "manage_guild", "manage_roles",
                "manage_channels", "ban_members", "kick_members")


def _position(rolle) -> int:
    # Discord fuehrt die Position als int. Alles andere (fehlende Rolle,
    # Attrappe ohne Feld) zaehlt als „ganz unten" — nie als Freibrief.
    p = getattr(rolle, "position", None)
    return p if isinstance(p, int) and not isinstance(p, bool) else -1


def ist_eigentuemer(mitglied, guild) -> bool:
    oid = getattr(guild, "owner_id", None)
    return oid is not None and getattr(mitglied, "id", None) == oid


def macht_rechte(rolle) -> list:
    """Welche der MACHT_RECHTE traegt diese Rolle? -> Liste der Namen."""
    p = getattr(rolle, "permissions", None)
    return [n for n in MACHT_RECHTE if getattr(p, n, False) is True]


def rang_einwand(aufrufer, guild, rolle=None, ziel=None, selbst_ok=False) -> str:
    """'frei' = erlaubt, sonst ein Kurzgrund ('rolle_hoeher', 'rolle_macht',
    'ziel_hoeher'), den discordbot.py in einen Satz fuer den Nutzer uebersetzt.
    Ein ausdruecklicher Status statt '': ein leerer Text liest sich an der
    Aufrufstelle wie „nichts gefunden" und an der falschen wie „erlaubt".

    selbst_ok: das Ziel darf der Aufrufer selbst sein. Fuer Rollen-Vergabe
    richtig (die Rolle steht ja schon unter ihm, und „Macht" ist eigens
    gesperrt), fuer Kick/Bann/Timeout nicht.
    """
    if ist_eigentuemer(aufrufer, guild):
        return "frei"
    oben = _position(getattr(aufrufer, "top_role", None))
    if rolle is not None:
        if _position(rolle) >= oben:
            return "rolle_hoeher"
        darf = getattr(getattr(aufrufer, "guild_permissions", None), "administrator", False)
        if macht_rechte(rolle) and darf is not True:
            return "rolle_macht"
    if ziel is not None:
        selbst = getattr(ziel, "id", None) == getattr(aufrufer, "id", None)
        if not (selbst and selbst_ok):
            if ist_eigentuemer(ziel, guild) or _position(getattr(ziel, "top_role", None)) >= oben:
                return "ziel_hoeher"
    return "frei"


def kanal_einwand(kanal, aufrufer, guild) -> str:
    """'frei' = erlaubt, 'kanal_unsichtbar' sonst. Rechte eines Kanals setzt nur,
    wer ihn selbst sehen darf — sonst oeffnet „Server verwalten" #mod-log."""
    if ist_eigentuemer(aufrufer, guild):
        return "frei"
    # Bewusst ungefangen: wirft permissions_for, faengt das der Befehl als
    # Fehler ab, und es geschieht nichts — „weiss nicht" ist hier „nein".
    sicht = getattr(kanal.permissions_for(aufrufer), "view_channel", False)
    return "frei" if sicht is True else "kanal_unsichtbar"


def admin_rolle(alle, kennung):
    """Die Rolle zu DISCORD_ADMIN_ROLE: Ziffern = Rollen-ID, sonst der Name.

    Beim Namen zaehlt nur die HOECHSTE gleichnamige Rolle. Der reine
    Namensvergleich machte jeden mit „Rollen verwalten" zum Bot-Admin: eine
    Rolle gleichen Namens anlegen, sich geben, fertig. Discord legt neue
    Rollen ganz unten an, und hochschieben laesst sich eine Rolle nur bis
    unter die eigene hoechste — die echte Admin-Rolle ueberholt also nur,
    wer sie sich in Discord ohnehin selbst geben koennte. Eindeutig ist
    allein die ID; der Name bleibt fuer bestehende .env-Eintraege.
    """
    k = str(kennung or "").strip()
    rollen = list(alle or ()) if k else []     # nichts konfiguriert -> keine Rolle
    if k.isdigit():
        return next((r for r in rollen if getattr(r, "id", None) == int(k)), None)
    gleich = [r for r in rollen if getattr(r, "name", None) == k]
    return max(gleich, key=_position) if gleich else None


def admin_rolle_traegt(eigene, alle, kennung) -> bool:
    """Traegt das Mitglied (Rollen `eigene`) die Admin-Rolle aus `alle`?"""
    r = admin_rolle(alle, kennung)
    if r is None:
        return False
    rid = getattr(r, "id", None)
    return any(x is r or (rid is not None and getattr(x, "id", None) == rid)
               for x in (eigene or ()))
