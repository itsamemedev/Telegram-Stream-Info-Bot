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
    praefix = pfad + "_dcpart"
    teile, fehler = await _videoteil.kopier_teilen(pfad, praefix, grenze_mb)
    if teile and _videoteil.zu_gross(teile, grenze_mb):
        # Lange GOPs: der Segment-Muxer schneidet nur an Keyframes. Einmal mit
        # halbem Ziel — haeufig reicht das, und es kostet kein Neukodieren.
        _videoteil.wegwerfen(teile)
        teile, fehler = await _videoteil.kopier_teilen(pfad, praefix, max(1, grenze_mb // 2))
    if teile and _videoteil.zu_gross(teile, grenze_mb):
        _videoteil.wegwerfen(teile)
        teile, fehler = None, "Teile ohne Neukodieren zu gross"
    if not teile:
        log.warning("Discord-Aufnahme %s: Teilen ohne Neukodieren gescheitert (%s) — "
                    "kodiere neu.", os.path.basename(pfad), fehler)
        teile, fehler = await _videoteil.neu_kodieren(pfad, praefix, grenze_mb)
    if not teile:
        return None, "Teilen gescheitert: %s" % (fehler or "?")
    return teile, None


async def hochladen(pfad, grenze_mb, senden, nutzer, beginn=None, ergebnis=None,
                    pause_s=PAUSE_S):
    """Die Aufnahme in Teilen <= grenze_mb hochladen.

    -> ergebnis {"gesendet": n, "fehler": n, "teile": n, "grund": text}.
    Wirft nicht (bis auf CancelledError): ein Fehler wird gezaehlt und im
    Grund benannt, der Aufrufer meldet ihn laut."""
    ergebnis = {} if ergebnis is None else ergebnis
    ergebnis.setdefault("gesendet", 0)
    ergebnis.setdefault("fehler", 0)
    try:
        groesse = os.path.getsize(pfad)
    except OSError as e:
        log.error("Discord-Aufnahme: %s nicht lesbar: %s", pfad, e)
        ergebnis["fehler"] += 1
        ergebnis["grund"] = "Datei nicht lesbar: %s" % e
        return ergebnis
    eigene = False
    if groesse <= grenze_mb * _MB:
        teile = [pfad]
    else:
        ok, info = _videoteil.platz_reicht(pfad)
        if not ok:
            ergebnis["fehler"] += 1
            ergebnis["grund"] = "zu wenig Platz zum Teilen: %s" % info
            return ergebnis
        teile, grund = await teilen(pfad, grenze_mb)
        if not teile:
            ergebnis["fehler"] += 1
            ergebnis["grund"] = grund
            return ergebnis
        eigene = True
    n = len(teile)
    ergebnis["teile"] = n
    in_folge = 0
    try:
        for i, teil in enumerate(teile, 1):
            mb = os.path.getsize(teil) / _MB
            if mb > grenze_mb:
                # Auch nach dem Neukodieren zu gross: Discord antwortete mit
                # 413. Gezaehlt, damit die Aufnahme nicht als angekommen gilt.
                ergebnis["fehler"] += 1
                ergebnis["grund"] = "Teil %d/%d bleibt %.1f MB > %d MB" % (i, n, mb, grenze_mb)
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
                in_folge += 1
                if in_folge >= ABBRUCH_IN_FOLGE:
                    # Fehlendes Recht oder geloeschter Kanal: jeder weitere Teil
                    # scheitert genauso, und bei 100 Teilen waeren das 100 Fehler.
                    ergebnis["fehler"] += n - i
                    ergebnis["grund"] += " — Rest (%d Teile) nicht versucht" % (n - i)
                    break
            if i < n:
                await asyncio.sleep(pause_s)
    finally:
        if eigene:
            _videoteil.wegwerfen(teile)
    return ergebnis
