"""nc.discordaufnahme — die GANZE Aufnahme nach Discord, in hochladbaren Teilen.

v4.2-W175. Gewuenscht vom Betreiber am 11.11.: nicht nur Highlights und
Memes, sondern jede fertige Aufnahme in den Clip-Kanal (DISCORD_CLIP_CHANNEL,
Vorgabe #clips) — auch fuer Nutzer, die nur per Discord-/track verfolgt
werden. W168 hatte genau diesen Nutzern Telegram genommen und im Log
behauptet, ihre Aufnahme gehe „nur nach Discord"; tatsaechlich ging sie
nirgendwohin, solange kein Highlight-Clip entstand.

Discord nimmt je Datei nur, was das Guild-Limit erlaubt (10 MB ohne Boost,
50/100 MB mit — nc/discordlimits). Geteilt wird mit derselben Logik wie fuer
Telegram (nc/videoteil): erst ohne Neukodieren an Keyframes, bei zu groben
Teilen noch einmal mit halbem Ziel, und erst dann neu kodiert — das laeuft
in nc/videoteil.neu_kodieren durch die Encode-Warteschlange (W174), eine
Aufnahme nebenan zerfaellt also nicht.

Die Sendefunktion reicht der Bot herein (`senden(pfad, text)`), damit dieses
Modul kein discord.py braucht und ohne Discord pruefbar bleibt.
"""

import asyncio
import logging
import os

from nc import i18n as _i18n
from nc import videoteil as _videoteil

log = logging.getLogger("TikTokBot")

SCHALTER = "DISCORD_AUFNAHME_UPLOAD"
_MB = 1024 * 1024
PAUSE_S = 2.0              # Discord drosselt ab 5 Nachrichten je 5 s und Kanal
ABBRUCH_IN_FOLGE = 3       # so viele Teile in Folge gescheitert -> Rest lassen


def an(env=None) -> bool:
    """Schalter, als Funktion gelesen (.env kommt spaeter). Vorgabe: an."""
    wert = (env if env is not None else os.getenv("DISCORD_AUFNAHME_UPLOAD", "1")) or "1"
    return str(wert).strip().lower() not in ("0", "false", "no", "off", "aus", "nein")


def _md(text) -> str:
    """Discord-Markdown entschaerfen — ein Handle wie `__anna__` wuerde sonst
    unterstrichen statt angezeigt."""
    aus = str(text or "")
    for z in ("\\", "*", "_", "~", "|", "`", ">"):
        aus = aus.replace(z, "\\" + z)
    return aus


def beschriftung(nutzer, i, n, mb, beginn=None) -> str:
    datum = beginn.strftime("%d.%m.%Y %H:%M") if beginn else "?"
    if n <= 1:
        return _i18n.t("🎬 Aufnahme @{nutzer} · {datum} · {mb} MB",
                       nutzer=_md(nutzer), datum=datum, mb="%.1f" % mb)
    return _i18n.t("🎬 Aufnahme @{nutzer} · {datum} · Teil {i}/{n} · {mb} MB",
                   nutzer=_md(nutzer), datum=datum, i=i, n=n, mb="%.1f" % mb)


async def teilen(pfad, grenze_mb):
    """-> (teile, None) oder (None, grund). Teile liegen neben der Aufnahme
    mit eigenem Praefix — der Telegram-Versand teilt dieselbe Datei unter
    `_part` und sammelt danach per Glob `<praefix>_*.mp4` ein; ein Praefix
    `_part_dc` laege in genau diesem Glob, und Telegram bekaeme die
    Discord-Teile mitgesendet. `_dcpart` erkennt die Waisen-Suche trotzdem
    als Split-Rest (sie sucht „_part“ im Namen)."""
    # v5.12: die Grenze steht im Praefix. Mehrere Server laden gleichzeitig,
    # und Server verschiedener Boost-Stufen brauchen verschieden grosse Teile —
    # unter EINEM Praefix haette der zweite Split die Teile des ersten
    # ueberschrieben. nc/videoteil._REST kennt die Form `_dcpart<N>_000.mp4`.
    praefix = "%s_dcpart%d" % (pfad, int(grenze_mb))
    teile, fehler = await _videoteil.kopier_teilen(pfad, praefix, grenze_mb)
    if teile and _videoteil.zu_gross(teile, grenze_mb):
        # Lange GOPs: der Segment-Muxer schneidet nur an Keyframes. Einmal mit
        # halbem Ziel — haeufig reicht das, und es kostet kein Neukodieren.
        # v5.12.1: Loeschen im Thread — 86 Teile auf voller Platte hielten
        # den Event-Loop bis 6,1 s an (Log 27.11., loop_bremser).
        await asyncio.to_thread(_videoteil.wegwerfen, teile)
        teile, fehler = await _videoteil.kopier_teilen(pfad, praefix, max(1, grenze_mb // 2))
    if teile and _videoteil.zu_gross(teile, grenze_mb):
        await asyncio.to_thread(_videoteil.wegwerfen, teile)
        teile, fehler = None, "Teile ohne Neukodieren zu gross"
    if not teile:
        log.warning("Discord-Aufnahme %s: Teilen ohne Neukodieren gescheitert (%s) — "
                    "kodiere neu.", os.path.basename(pfad), fehler)
        teile, fehler = await _neu_kodiert(pfad, praefix, grenze_mb)
    if not teile:
        return None, "Teilen gescheitert: %s" % (fehler or "?")
    return teile, None


async def _neu_kodiert(pfad, praefix, grenze_mb):
    """Neu kodieren wie der Telegram-Weg (B70+): erst die Zeitstempel
    geradeziehen, dann auf der geradegezogenen Kopie kodieren.

    v5.12.1: der Discord-Weg kodierte das Original direkt. Streams mit „pts
    has no value" / „Non-monotonic DTS" bringen den Segment-Muxer zum Absturz
    — am 27.11. nach drei Minuten Kodieren „Conversion failed!", und die
    Warteschlange wiederholte es zweimal. Der Name traegt den Praefix (und
    damit die Grenze): Telegram legt fuer dieselbe Aufnahme gleichzeitig
    `<aufnahme>.remux.mp4` an, ein gemeinsamer Name haette sich ueberschrieben."""
    remux = praefix + ".remux.mp4"
    try:
        ok, fehler = await _videoteil.zeitstempel_richten(pfad, remux)
        if not ok:
            log.warning("Discord-Aufnahme %s: Re-Mux (genpts) scheiterte (%s) — kodiere "
                        "das Original.", os.path.basename(pfad), fehler or "?")
        return await _videoteil.neu_kodieren(remux if ok else pfad, praefix, grenze_mb)
    finally:
        await asyncio.to_thread(_videoteil.wegwerfen, [remux])


async def hochladen(pfad, grenze_mb, senden, nutzer, beginn=None, ergebnis=None,
                    pause_s=PAUSE_S):
    """Die Aufnahme in Teilen <= grenze_mb an EIN Ziel hochladen.

    -> ergebnis {"gesendet": n, "fehler": n, "teile": n, "grund": text}.
    Wirft nicht (bis auf CancelledError): ein Fehler wird gezaehlt und im
    Grund benannt, der Aufrufer meldet ihn laut. Seit v5.12 ein Sonderfall von
    an_alle (ein Ziel)."""
    ergebnis = {} if ergebnis is None else ergebnis
    await an_alle(pfad, [(grenze_mb, senden, ergebnis)], nutzer, beginn, pause_s)
    return ergebnis


async def an_alle(pfad, ziele, nutzer, beginn=None, pause_s=PAUSE_S):
    """Die Aufnahme an MEHRERE Server gleichzeitig. ziele = [(grenze_mb, senden, ergebnis)].

    v5.12, gewuenscht vom Betreiber: die Uploads starten ueberall zugleich,
    jeder Server in Teilen nach SEINER Grenze (Boost-Stufe, nc/discordlimits).
    Server mit derselben Grenze teilen sich EINEN Split — die Teile liegen
    einmal auf der Platte, und ffmpeg laeuft nicht je Server. Jedes `ergebnis`
    wird gefuellt wie bei hochladen; wirft nicht (bis auf CancelledError)."""
    nach_grenze = {}
    for grenze, senden, ergebnis in ziele:
        ergebnis.setdefault("gesendet", 0)
        ergebnis.setdefault("fehler", 0)
        nach_grenze.setdefault(int(grenze), []).append((senden, ergebnis))
    await asyncio.gather(*(_gruppe(pfad, grenze, empfaenger, nutzer, beginn, pause_s)
                           for grenze, empfaenger in nach_grenze.items()))


def _alle_fehler(empfaenger, grund, art):
    for _senden, ergebnis in empfaenger:
        ergebnis["fehler"] += 1
        ergebnis["grund"] = grund
        ergebnis["art"] = art


# v5.12.1: woran es lag — bis hierher sagte JEDE gescheiterte Aufnahme
# „Fehlt dem Bot das Recht, in #… Dateien zu posten?", auch wenn ffmpeg
# schon beim Teilen gescheitert war und Discord nie gefragt wurde (Log
# 26./27.11.: „0 von 0 Teilen gesendet. Fehlt dem Bot das Recht …"). Ein
# falscher Rat schickt den Betreiber in die Server-Einstellungen, waehrend
# der Fehler in der Datei liegt.
_ABHILFE = {
    "datei": "Die Aufnahme ist nicht lesbar — liegt sie noch dort, und darf der Bot sie lesen?",
    "platz": "Zu wenig Platz zum Teilen neben der Aufnahme — Platte aufraeumen "
             "(Deck › Aufnahmen › Reste) oder RECORDINGS_DIR auf eine groessere Platte.",
    "teilen": "ffmpeg konnte die Aufnahme nicht in hochladbare Teile zerlegen (Grund oben); "
              "Discord wurde nicht gefragt.",
    "groesse": "Ein Teil blieb auch nach dem Neukodieren ueber der Grenze des Servers; "
               "Discord wurde fuer diesen Teil nicht gefragt.",
    "rechte": "Fehlt dem Bot das Recht, in #{kanal} Dateien zu posten (Dateien anhaengen, "
              "Nachrichten senden)?",
    "senden": "Discord hat den Upload abgelehnt (Grund oben) — Netz oder Discord-Stoerung; "
              "die Warteschlange versucht es erneut.",
    "kanal": "Fuer den Nutzer gibt es keinen Aufnahme-Kanal, und der Bot konnte keinen "
             "anlegen — Recht „Kanaele verwalten\" pruefen.",
}

# Woran ein Sendefehler als fehlendes Recht zu erkennen ist: discord.Forbidden
# (HTTP 403), Discord-Code 50013 „Missing Permissions" oder 50001 „Missing Access".
_RECHTE = ("forbidden", "missing permissions", "missing access", "50013", "50001", "403")


def abhilfe(ergebnis, kanal="?") -> str:
    """Der Rat zu einem gescheiterten Upload, nach der Art des Fehlers."""
    vorlage = _ABHILFE.get((ergebnis or {}).get("art") or "")
    if vorlage is None:
        return "Grund siehe oben."
    return vorlage.replace("{kanal}", str(kanal))


async def _gruppe(pfad, grenze_mb, empfaenger, nutzer, beginn, pause_s):
    """Ein Split fuer alle Server dieser Grenze, dann alle gleichzeitig senden."""
    try:
        groesse = os.path.getsize(pfad)
    except OSError as e:
        log.error("Discord-Aufnahme: %s nicht lesbar: %s", pfad, e)
        _alle_fehler(empfaenger, "Datei nicht lesbar: %s" % e, "datei")
        return
    eigene = False
    if groesse <= grenze_mb * _MB:
        teile = [pfad]
    else:
        ok, info = _videoteil.platz_reicht(pfad)
        if not ok:
            _alle_fehler(empfaenger, "zu wenig Platz zum Teilen: %s" % info, "platz")
            return
        teile, grund = await teilen(pfad, grenze_mb)
        if not teile:
            _alle_fehler(empfaenger, grund, "teilen")
            return
        eigene = True
    try:
        await asyncio.gather(*(_senden_alle(teile, grenze_mb, senden, ergebnis, nutzer,
                                            beginn, pause_s)
                               for senden, ergebnis in empfaenger))
    finally:
        # Erst wenn ALLE Server dieser Grenze fertig sind (oder abgebrochen).
        if eigene:
            await asyncio.to_thread(_videoteil.wegwerfen, teile)


async def _senden_alle(teile, grenze_mb, senden, ergebnis, nutzer, beginn, pause_s):
    """Die Teile nacheinander an EINEN Server (Pause gegen die Kanal-Drossel)."""
    n = len(teile)
    ergebnis["teile"] = n
    in_folge = 0
    for i, teil in enumerate(teile, 1):
        mb = os.path.getsize(teil) / _MB
        if mb > grenze_mb:
            # Auch nach dem Neukodieren zu gross: Discord antwortete mit
            # 413. Gezaehlt, damit die Aufnahme nicht als angekommen gilt.
            ergebnis["fehler"] += 1
            ergebnis["grund"] = "Teil %d/%d bleibt %.1f MB > %d MB" % (i, n, mb, grenze_mb)
            ergebnis["art"] = "groesse"
            continue
        try:
            await senden(teil, beschriftung(nutzer, i, n, mb, beginn))
            ergebnis["gesendet"] += 1
            in_folge = 0
        except asyncio.CancelledError:
            raise
        except Exception as e:
            # Je Teil eine Zeile; die Zusammenfassung meldet der Aufrufer
            # gedrosselt auf error (bot._aufnahme_nach_discord).
            log.warning("Discord-Aufnahme @%s Teil %d/%d gescheitert: %s", nutzer, i, n, e)
            ergebnis["fehler"] += 1
            ergebnis["grund"] = "Teil %d/%d: %s: %s" % (i, n, type(e).__name__, e)
            text = ("%s %s" % (type(e).__name__, e)).lower()
            ergebnis["art"] = "rechte" if any(w in text for w in _RECHTE) else "senden"
            in_folge += 1
            if in_folge >= ABBRUCH_IN_FOLGE:
                # Fehlendes Recht oder geloeschter Kanal: jeder weitere Teil
                # scheitert genauso, und bei 100 Teilen waeren das 100 Fehler.
                ergebnis["fehler"] += n - i
                ergebnis["grund"] += " — Rest (%d Teile) nicht versucht" % (n - i)
                break
        if i < n:
            await asyncio.sleep(pause_s)
