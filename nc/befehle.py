"""nc.befehle — v4.2-W109: EIN Verzeichnis aller Befehle, Telegram und Discord.

Gemeldet: „Telegram und Discord sind immer noch nicht vereinheitlicht." Der
Bestand vor dieser Welle:

* Telegram registrierte 29 Befehle aus einer Tupel-Liste in `run_bot()`.
* Discord hatte 15 davon als Zwischenbefehle UNTER ANDEREM NAMEN
  (`/sys_pause` fuer `/pause`, `/sys_res` fuer `/sysres`, …) und zwei weitere
  als eigene Kopie: `/sys_report` (der Rumpf woertlich wie `/report`, laut
  eigenem Docstring „identisch") und `/sys_unpause`, das es auf Telegram gar
  nicht gab.
* Sieben Telegram-Befehle fehlten auf Discord ganz.
* Die Hilfe auf Discord war ein handgeschriebener Absatz, der von 45
  Befehlen 27 nannte — die `sys_*`-Befehle kein einziges Mal.
* `/untrack` stand auf Discord jedem Servermitglied offen und loeschte ein
  Tracking der ganzen Gruppe, gleich wer es angelegt hatte. Auf Telegram
  darf das nur ein freigeschalteter Nutzer.

Hier steht deshalb jeder Befehl genau einmal: Name, Rubrik, auf welchen
Plattformen, wie er auf Discord ausgefuehrt wird und wer ihn benutzen darf.
Beide Seiten registrieren daraus, beide Hilfen werden daraus gebaut, und der
Vertrag haelt fest, dass es keinen Befehl gibt, der hier fehlt.

**Discord-Ausfuehrung** (`discord`):

* ``"tg"`` — der Telegram-Handler laeuft unveraendert ueber den Shim in
  discordbot.py (`_run_tg_handler`). Eine Logik, null Kopien: ein Fix am
  Telegram-Handler wirkt auf Discord mit. Das ist der Weg fuer jeden
  Betreiberbefehl.
* ``"nativ"`` — Discord hat eine eigene Umsetzung (Community-Funktionen,
  Rollen, Gilden-Bezug). Die Beschreibung steht dann am Dekorator.
* ``None`` — nur Telegram.

**Rechte** (`recht`) regeln Discord. Auf Telegram antwortet der Bot
ohnehin nur freigeschalteten Nutzern (`_is_authorized` in jedem Handler) —
dort ist jeder Befehl ein Betreiberbefehl. Auf Discord heisst
``"betreiber"`` Admin (`_is_admin`), ``"jeder"`` jedes Servermitglied, und
das gibt es nur fuer Community-, Lese- und KI-Befehle. Ein Befehl, der auf
beiden Plattformen existiert und etwas VERAENDERT, ist auf beiden
Betreiberbefehl — die eine Ausnahme ist `/track` auf Discord (Quota je
Mitglied, so gebaut seit B63) und `/untrack`, das dort seit W109 nur der
Betreiber oder der Anleger darf.

Bewusst nur auf Telegram: `/start` (der Telegram-Einstieg; Discord hat
`/help`) und `/update`. Ein Update spielt Code vom Repo auf den Server — der
Knopf gehoert an die kleinste Tuer, die es gibt, und das ist die
Telegram-Freischaltliste, nicht eine Discord-Rolle, die ein Moderator
vergeben kann.
"""

from collections import OrderedDict, namedtuple

TG = "telegram"
DC = "discord"


def _t(text):
    """Markiert Benutzertext fuer tools/i18n_extract.py. Uebersetzt wird beim
    Gebrauch (nc.i18n.t), nicht hier: die Sprache steht erst je Anfrage fest."""
    return text


# name, rubrik, text, plattformen, discord, recht, args, tg_handler
#   args: None = keine Argumente; sonst ein Nutzungshinweis ("@user")
Befehl = namedtuple("Befehl", "name rubrik text plattformen discord recht "
                              "args tg_handler")

RUBRIKEN = OrderedDict([
    ("analyse", _t("Analyse")),
    ("tracking", _t("Tracking")),
    ("aufnahme", _t("Aufnahmen")),
    ("ki", _t("KI und Brain")),
    ("system", _t("System")),
    ("community", _t("Community")),
    ("moderation", _t("Moderation")),
    ("server", _t("Server")),
])

_BEIDE = frozenset((TG, DC))
_NUR_TG = frozenset((TG,))
_NUR_DC = frozenset((DC,))


def _b(name, rubrik, text, handler, args=None, recht="betreiber",
       discord="tg", plattformen=_BEIDE):
    return Befehl(name, rubrik, text, plattformen, discord, recht, args, handler)


def _dc(name, rubrik, recht="jeder"):
    """Nur Discord, eigene Umsetzung — Beschreibung steht am Dekorator."""
    return Befehl(name, rubrik, None, _NUR_DC, "nativ", recht, None, None)


BEFEHLE = (
    # ── auf beiden Plattformen, EINE Logik (Telegram-Handler) ──────────────
    _b("tiktok", "analyse", _t("Profil-Analyse eines TikTok-Accounts"), "tiktok", "‹name›"),
    _b("live", "analyse", _t("Live-Status sofort pruefen"), "live", "@user"),
    _b("track_exact", "tracking", _t("Exakten Usernamen tracken (ohne Korrektur)"),
       "track_exact", "‹name›"),
    _b("pause", "tracking", _t("Tracking pausieren"), "pause_tracking", "@user"),
    _b("resume", "tracking", _t("Tracking fortsetzen"), "resume_tracking", "@user"),
    _b("unpause", "tracking", _t("Auto-pausierte Quelle wieder aktivieren"),
       "unpause_cmd", "@user"),
    _b("bulkadd", "tracking", _t("Mehrere User auf einmal tracken"), "bulkadd", "a b c"),
    _b("stoprec", "aufnahme", _t("Laufende Aufnahme sauber beenden"), "stoprec", "@user"),
    _b("cleanup", "aufnahme", _t("Alte Aufnahmen aufraeumen"), "cleanup"),
    _b("quota", "aufnahme", _t("Speicher-Quota"), "quota"),
    _b("teststream", "aufnahme", _t("Recorder-Selbsttest"), "teststream", "@user"),
    _b("topusers", "aufnahme", _t("Top-Streamer nach Aufnahmen"), "topusers"),
    _b("summary", "aufnahme", _t("Tageszusammenfassung"), "summary_cmd"),
    _b("aireset", "ki", _t("KI-Kontext zuruecksetzen"), "aireset"),
    _b("brain", "ki", _t("Brain-Lage: Regeln, Agenten, Empfehlungen"), "brain_cmd"),
    _b("report", "ki", _t("Azrael-Sentinel-Wochenreport"), "report_cmd"),
    _b("cookies", "system", _t("Cookie-Status — mit 'holen' selbst beziehen"),
       "cookies_cmd", "[holen]"),
    _b("sysres", "system", _t("System-Ressourcen"), "sysres"),
    _b("logs", "system", _t("Letzte Fehler aus dem Log"), "logs_cmd"),
    _b("diag", "system", _t("Vollstaendige Diagnose"), "diag"),
    _b("einnahmen", "system", _t("Einnahmen und Spenden"), "einnahmen_cmd"),
    _b("about", "system", _t("Ueber diesen Bot"), "about"),

    # ── auf beiden Plattformen, Discord mit eigener Umsetzung ─────────────
    # Lesen und KI: auf Discord fuer die Community offen.
    _b("tracklist", "tracking", _t("Getrackte Accounts anzeigen"), "tracklist",
       recht="jeder", discord="nativ"),
    # /track ist auf Discord offen, aber je Mitglied per Quota begrenzt (B63).
    _b("track", "tracking", _t("TikTok-User tracken"), "track", "‹name›",
       recht="jeder", discord="nativ"),
    # /untrack: Betreiber — oder wer das Tracking angelegt hat (added_by).
    _b("untrack", "tracking", _t("TikTok-User nicht mehr tracken"), "untrack",
       "‹name›", discord="nativ"),
    _b("recstatus", "aufnahme", _t("Laufende Aufnahmen"), "recstatus",
       recht="jeder", discord="nativ"),
    _b("stats", "aufnahme", _t("Statistik"), "stats", recht="jeder",
       discord="nativ"),
    _b("ai", "ki", _t("AZRAEL fragen"), "ai", "‹frage›", recht="jeder",
       discord="nativ"),
    _b("help", "system", _t("Alle Befehle anzeigen"), "hilfe_cmd",
       recht="jeder", discord="nativ"),

    # ── nur Telegram ───────────────────────────────────────────────────────
    _b("start", "system", _t("Einstieg und Kurzuebersicht"), "start",
       discord=None, plattformen=_NUR_TG),
    _b("update", "system", _t("Update vom Repo einspielen"), "update_cmd",
       discord=None, plattformen=_NUR_TG),

    # ── nur Discord (Community, Server, Moderation) ───────────────────────
    _dc("status", "analyse"), _dc("streaminfo", "analyse"),
    _dc("livenow", "tracking"), _dc("restream_status", "tracking"),
    _dc("follow", "tracking"), _dc("unfollow", "tracking"),
    _dc("topstreamers", "aufnahme"), _dc("clips", "aufnahme"),
    _dc("clip", "aufnahme"), _dc("clipoftheweek", "aufnahme"),
    _dc("ask", "ki"),
    _dc("botstats", "system", "betreiber"), _dc("post_test", "system", "betreiber"),
    _dc("rank", "community"), _dc("leaderboard", "community"),
    _dc("daily", "community"), _dc("profile", "community"),
    _dc("event", "community", "betreiber"), _dc("events", "community"),
    _dc("warn", "moderation", "betreiber"), _dc("warnings", "moderation"),
    _dc("clearwarns", "moderation", "betreiber"), _dc("purge", "moderation", "betreiber"),
    _dc("kick", "moderation", "betreiber"), _dc("ban", "moderation", "betreiber"),
    _dc("timeout", "moderation", "betreiber"),
    _dc("setup_community", "server", "betreiber"), _dc("setup_targets", "server", "betreiber"),
    _dc("create_channel", "server", "betreiber"), _dc("create_voice", "server", "betreiber"),
    _dc("create_category", "server", "betreiber"), _dc("create_role", "server", "betreiber"),
    _dc("create_group", "server", "betreiber"), _dc("assign_role", "server", "betreiber"),
    _dc("remove_role", "server", "betreiber"), _dc("set_channel_perms", "server", "betreiber"),
)

NACH_NAME = OrderedDict((b.name, b) for b in BEFEHLE)


def fuer(plattform):
    """Alle Befehle einer Plattform, in Verzeichnis-Reihenfolge."""
    return [b for b in BEFEHLE if plattform in b.plattformen]


def telegram_handler():
    """(name, handlername) fuer jeden Telegram-Befehl."""
    return [(b.name, b.tg_handler) for b in fuer(TG)]


def discord_ueber_tg():
    """Discord-Befehle, die den Telegram-Handler ueber den Shim ausfuehren."""
    return [b for b in fuer(DC) if b.discord == "tg"]


def discord_nativ():
    return [b for b in fuer(DC) if b.discord == "nativ"]


def beschreibung(b, uebersetzen=lambda s: s):
    """Kurztext mit Nutzungshinweis — auf 100 Zeichen, die Discord erlaubt."""
    txt = uebersetzen(b.text or b.name)
    if b.args:
        txt = "%s · %s" % (txt, b.args)
    return txt[:100]


def hilfe_text(plattform, uebersetzen=lambda s: s, ist_betreiber=True):
    """Die Befehlsliste einer Plattform, nach Rubriken.

    Eine Hilfe, die von Hand gepflegt wird, veraltet mit dem naechsten Befehl
    — die Discord-Hilfe nannte 27 von 45. Diese wird gebaut, also kann sie
    nichts weglassen. Wer kein Betreiber ist, sieht nur, was er benutzen darf:
    eine Liste voller „Nur Admins."-Antworten ist keine Hilfe.
    """
    zeilen = []
    for schluessel, titel in RUBRIKEN.items():
        namen = ["/" + b.name for b in fuer(plattform) if b.rubrik == schluessel
                 and (ist_betreiber or b.recht == "jeder")]
        if namen:
            zeilen.append("%s: %s" % (uebersetzen(titel), " ".join(namen)))
    return "\n".join(zeilen)


def pruefen():
    """Innere Stimmigkeit. -> Liste von Befunden (leer = in Ordnung)."""
    befunde = []
    # Aus BEFEHLE gezaehlt, nicht gegen NACH_NAME: das entsteht einmal beim
    # Import und saehe ein spaeter dazugekommenes Doppel nie.
    namen = [b.name for b in BEFEHLE]
    for doppelt in sorted({n for n in namen if namen.count(n) > 1}):
        befunde.append("%s: doppelter Name im Verzeichnis" % doppelt)
    for b in BEFEHLE:
        if b.rubrik not in RUBRIKEN:
            befunde.append("%s: unbekannte Rubrik %r" % (b.name, b.rubrik))
        if b.recht not in ("betreiber", "jeder"):
            befunde.append("%s: unbekanntes Recht %r" % (b.name, b.recht))
        if TG in b.plattformen and not b.tg_handler:
            befunde.append("%s: Telegram ohne Handler" % b.name)
        if DC in b.plattformen and b.discord not in ("tg", "nativ"):
            befunde.append("%s: Discord ohne Ausfuehrungsweg" % b.name)
        if b.discord == "tg" and b.recht != "betreiber":
            # Der Shim prueft _is_admin und meldet sich dann als erster
            # freigeschalteter Telegram-Nutzer an — ein offener Shim-Befehl
            # gaebe jedem Discord-Mitglied die Telegram-Rechte des Betreibers.
            befunde.append("%s: Shim-Befehl muss Betreiberbefehl sein" % b.name)
        if b.name.startswith("sys_"):
            befunde.append("%s: sys_-Praefix — der Name ist auf beiden "
                           "Plattformen derselbe" % b.name)
        if len(b.name) > 32 or not b.name.replace("_", "").isalnum() \
                or b.name != b.name.lower():
            befunde.append("%s: kein gueltiger Befehlsname (Telegram und "
                           "Discord: a-z, 0-9, _, hoechstens 32)" % b.name)
    return befunde
