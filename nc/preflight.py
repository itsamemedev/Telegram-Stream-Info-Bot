"""nc.preflight — Stream-URL-Preflight (CDN-404-Schutz, V37-B91).

Extrahiert aus bot.py. Prüft eine Stream-URL vor dem ffmpeg-Spawn auf 404
und testet _hd/_uhd/_sd-Suffix-Fallbacks (TikTok-CDN-Quirk). Nutzt die Zähler
_PREFLIGHT_STATS/_PREFLIGHT_DEAD_STREAK, die die Bridge als Metriken spiegelt.

`log` und `RECORD_PROXY` werden von bot.py via configure() injiziert, damit
das Modul keine Rückabhängigkeit auf den Monolithen hat.

════════════════════════════════════════════════════════════════════════
DREI AUSGÄNGE, UND WARUM SIE SICH NICHT VERTRETEN — v4.2-W89
════════════════════════════════════════════════════════════════════════
`_preflight_url` gibt drei Dinge zurück, und die Unterscheidung ist der ganze
Wert des Moduls:

    eine URL != u   Eine Variante lebt. Aufnehmen, und zwar von dort.
    u selbst        Wir wissen NICHTS. Fail-open: ffmpeg soll es versuchen.
    None            Alle Varianten haben sauber mit 404 geantwortet. Tot.

Bis W89 liefen der zweite und der dritte Fall durcheinander, und zwar in
beide Richtungen:

**`return u` mitten in der Kandidatenschleife.** Ein Timeout auf der zweiten
Variante beendete die Suche und gab das Original zurück — obwohl genau dieses
Original zwei Zeilen vorher schon mit 404 geantwortet hatte. Die dritte
Variante, die vielleicht gelebt hätte, wurde nie probiert. ffmpeg startete ins
Leere, ohne Zähler und ohne Logzeile; im Dashboard sah es aus, als hänge
TikTok.

**Und `None` bei einer Störung, die keine ist.** `None` heißt „tot", und
„tot" füttert `_PREFLIGHT_DEAD_STREAK`. Die Bridge hängt daran die
Brain-Regel `source_chronically_dead`, die ab acht Treffern in Folge das
Untracken vorschlägt. Ein Netzhänger auf DIESEM Server durfte also einen
lebenden Account zum Entfernen empfehlen — der teuerste mögliche Ausgang
einer Messung, die nur schiefgegangen ist.

Seit W89 zählt der Störfall auf `_PREFLIGHT_STATS["gestoert"]`, lässt die
Tot-Strähne ausdrücklich unberührt und meldet gedrosselt über
`nc.meldetakt` — erste Meldung sofort, ein Wechsel des Grundes sofort (aus
einem Timeout ein 403 zu machen ist die eigentliche Nachricht), sonst
höchstens alle 15 Minuten. Der Erfolgspfad setzt die Drossel zurück, sonst
bliebe ein wiederkehrender Ausfall bis zu 15 Minuten unsichtbar.

════════════════════════════════════════════════════════════════════════
DIE VARIANTENLISTE
════════════════════════════════════════════════════════════════════════
`_varianten` baut die Kandidaten und sortiert die, die beim letzten Mal
geholfen hat, nach vorn — ein Treffer beim ersten Versuch spart im
404-Sturm drei GETs je Aufnahme.

Bis W89 stand dort `x.replace(pref, "")`, und das entfernt `_hd` an JEDER
Stelle der URL: im Hostnamen (`cdn_hd.example`), in einem Abfrageparameter
(`?sess_hd=1`). Die so gebaute Zeichenkette stand dann in keiner
Kandidatenliste, und weil die Zuweisung an `pv in out` haengt, lief die
Bevorzugung einfach **ins Leere** — eine falsche URL konnte dadurch nie nach
vorn geraten, das hat `pv in out` verhindert. Der Schaden war also keine
falsche Abfrage, sondern eine ausgefallene Abkuerzung: bei jeder Quelle, deren
URL das Suffix zweimal traegt, kostete jede Aufnahme wieder die zusaetzliche
404-Runde, die der Merker gerade sparen soll. Ersetzt wird deshalb gezielt vor
`.flv`, `/index.m3u8` und `.m3u8`, genau wie beim Bauen der Liste.

`_varianten` steht auf Modulebene und nicht mehr als innere Funktion: so ist
die Sortierung ohne Netz, ohne Attrappe und ohne Ereignisschleife prüfbar.
"""

import logging
import time as _time_mod

from nc import meldetakt as _meldetakt

log = logging.getLogger("nc.preflight")
RECORD_PROXY = ""


def configure(logger=None, record_proxy=None):
    """bot.py reicht seinen Logger + Proxy rein (identisches Verhalten)."""
    global log, RECORD_PROXY
    if logger is not None:
        log = logger
    if record_proxy is not None:
        RECORD_PROXY = record_proxy


_PREFLIGHT_CACHE = {}
# V37-B91c: Preflight-Telemetrie — die Bridge spiegelt diese Zähler als
# Metriken (preflight_ok/fallback/dead), damit im Dashboard/Report sichtbar
# wird, wie oft der CDN-404-Quirk zuschlägt und der Fallback rettet.
# v4.2-W89: "gestoert" als vierter Wert — Faelle, in denen der Preflight
# NICHTS gemessen hat (Netzfehler/Timeout auf jede Variante) und deshalb
# fail-open mit dem Original weitergibt. Vorher liefen diese Faelle teils als
# "dead" mit: das ist die gefaehrlichste Verwechslung des Moduls, weil "dead"
# die Untrack-Empfehlung der Brain-Regel `source_chronically_dead` fuettert.
# Ein Netzhaenger auf DIESEM Server darf keinen lebenden Account zum
# Entfernen vorschlagen.
_PREFLIGHT_STATS = {"ok": 0, "fallback": 0, "dead": 0, "gestoert": 0}
# V37-B91d: aufeinanderfolgende Tot-Treffer pro Quelle (who → streak). Jeder
# Erfolg (ok/fallback) setzt zurück; die Bridge exponiert das an eine
# Brain-Regel, die chronisch tote Quellen zum Untracken vorschlägt.
_PREFLIGHT_DEAD_STREAK = {}

# Die Suffixe, die das TikTok-CDN an denselben Stream haengt. Reihenfolge ist
# die Wahrscheinlichkeit, in der sie auftreten.
SUFFIXE = ("_hd", "_uhd", "_sd", "_ld")

# Wo ein Suffix stehen darf: unmittelbar vor der Endung. Als Liste, weil an
# zwei Stellen ueber dieselben drei Formen gelaufen wird (bauen und
# bevorzugen) — zwei handgeschriebene Tripel laufen auseinander.
_ENDUNGEN = (".flv", "/index.m3u8", ".m3u8")


def _ohne(x, sfx):
    """`x` ohne das Suffix `sfx` vor einer der drei Endungen.

    -> die geaenderte URL, oder `x` selbst, wenn das Suffix dort nicht steht.
    Gezielt und nicht `x.replace(sfx, "")`: siehe DIE VARIANTENLISTE oben.
    """
    for endung in _ENDUNGEN:
        v = x.replace(sfx + endung, endung)
        if v != x:
            return v
    return x


def _varianten(x, who="?"):
    """Die Kandidatenliste fuer `x`, bevorzugte zuerst. -> list[str]

    Steht auf Modulebene, damit die Sortierung ohne Netz pruefbar ist.
    """
    out, seen = [x], {x}
    for sfx in SUFFIXE:
        for endung in _ENDUNGEN:
            v = x.replace(sfx + endung, endung)
            if v not in seen:
                seen.add(v); out.append(v)
    # Die Variante, die beim letzten Mal geholfen hat, nach vorn.
    pref = _PREFLIGHT_CACHE.get(who)
    if pref:
        pv = _ohne(x, pref)
        if pv != x and pv in out and out.index(pv) > 0:
            out.remove(pv); out.insert(0, pv)
    return out


async def _preflight_url(u, who="?"):
    """Lebt diese Stream-URL? -> URL (ggf. eine andere), `u` oder None.

    Die drei Ausgaenge und warum sie sich nicht vertreten: siehe
    Modul-Docstring.
    """
    if not u:
        return u
    try:
        import aiohttp as _ah
        tmo = _ah.ClientTimeout(total=6)
        _pxy = RECORD_PROXY or None
        # Der letzte Netzfehler, falls einer auftrat. Kein Wahrheitswert: der
        # Ausnahmetyp ist der GRUND, den nc.meldetakt braucht.
        gestoert = None
        async with _ah.ClientSession(timeout=tmo) as _s:
            for cand in _varianten(u, who):
                try:
                    async with _s.get(cand, proxy=_pxy,
                                      headers={"Range": "bytes=0-1023",
                                               "User-Agent": "Mozilla/5.0"},
                                      allow_redirects=True) as r:
                        if r.status == 404:
                            continue
                        if cand != u:
                            for _sfx in SUFFIXE:
                                if _sfx in u and _sfx not in cand:
                                    _PREFLIGHT_CACHE[who] = _sfx
                                    if len(_PREFLIGHT_CACHE) > 300:
                                        _PREFLIGHT_CACHE.pop(next(iter(_PREFLIGHT_CACHE)))
                                    break
                            log.info("%s: B91-Preflight — %s 404, Fallback greift",
                                     who, u.split("?")[0].rsplit("/", 1)[-1])
                            _PREFLIGHT_STATS["fallback"] += 1
                        else:
                            if who in _PREFLIGHT_CACHE:
                                _PREFLIGHT_CACHE.pop(who, None)
                            _PREFLIGHT_STATS["ok"] += 1
                        _PREFLIGHT_DEAD_STREAK.pop(who, None)   # V37-B91d
                        # Der Erfolgspfad setzt die Drossel zurueck (W81).
                        _meldetakt.zuruecksetzen("preflight")
                        return cand
                except Exception as e:
                    # v4.2-W89: WEITERSUCHEN, nicht abbrechen. Hier stand
                    # `return u` — siehe DREI AUSGAENGE im Modul-Docstring.
                    gestoert = e
                    continue

        if gestoert is not None:
            # Wir haben NICHTS gemessen. Fail-open, und die Tot-Straehne
            # bleibt ausdruecklich unberuehrt — sie empfiehlt das Untracken.
            grund = type(gestoert).__name__
            laut, unterdrueckt = _meldetakt.melden(
                "preflight", grund, _time_mod.monotonic())
            if laut:
                log.warning(
                    "B91-Preflight: keine URL-Variante erreichbar (%s: %s) — "
                    "gebe das Original weiter, ffmpeg entscheidet. Die Quelle "
                    "gilt damit NICHT als tot. Wenn das anhaelt, ist der Weg "
                    "nach aussen gestoert: RECORD_PROXY pruefen (gesetzt: %s), "
                    "sonst DNS/Firewall auf diesem Rechner.%s",
                    grund, str(gestoert)[:120], "ja" if RECORD_PROXY else "nein",
                    _meldetakt.zusatz(unterdrueckt))
            _PREFLIGHT_STATS["gestoert"] += 1
            return u

        log.warning("%s: B91-Preflight — alle URL-Varianten 404 (tot/Battle-Stage)", who)
        _PREFLIGHT_STATS["dead"] += 1
        _PREFLIGHT_DEAD_STREAK[who] = _PREFLIGHT_DEAD_STREAK.get(who, 0) + 1  # V37-B91d
        if len(_PREFLIGHT_DEAD_STREAK) > 300:
            _PREFLIGHT_DEAD_STREAK.pop(next(iter(_PREFLIGHT_DEAD_STREAK)))
        return None
    except Exception as e:
        # v4.2-W89: nicht mehr still. Hier landet, was die Schleife gar nicht
        # erst erreicht — ein fehlendes aiohttp, ein kaputter Proxy-Wert, ein
        # Programmierfehler in _varianten. Der Aufruf kehrte ordentlich
        # zurueck, nur wusste niemand, dass der Preflight nie lief.
        laut, unterdrueckt = _meldetakt.melden(
            "preflight-aufbau", type(e).__name__, _time_mod.monotonic())
        if laut:
            log.error("B91-Preflight liess sich nicht aufbauen (%s: %s) — die "
                      "404-Vorpruefung faellt damit komplett aus, die "
                      "Aufnahme laeuft ungeprueft weiter.%s",
                      type(e).__name__, str(e)[:160],
                      _meldetakt.zusatz(unterdrueckt))
        return u
