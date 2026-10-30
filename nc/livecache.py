"""nc.livecache — der Kurzzeit-Cache der Live-Erkennung (v4.2-W103).

**Der Anlass.** Der Betreiber hat am 01.10. das Log mitgeschnitten, und darin
stehen die Zeilen PAARWEISE:

    10:55:53,944  live-ohne-URL @laurahasisfrau1601225: …
    10:55:53,961  live-ohne-URL @laurahasisfrau1601225: …     (17 ms spaeter)
    10:56:18,477  live-ohne-URL @laurahasisfrau1601225: …
    10:56:18,555  live-ohne-URL @laurahasisfrau1601225: …     (78 ms)

Zwei vollstaendige Aufloesungen fuer DENSELBEN Nutzer, Millisekunden
auseinander, rund siebzig Mal in achtzehn Minuten. Genau dagegen gibt es
diesen Cache — sein Kommentar in `bot.py` nennt als Zweck woertlich
„Multi-Chat-Dedup", und derselbe Nutzer in zwei Chats ist der Normalfall.

**Warum er nicht griff.** Er wurde EINMAL geprueft, und zwar VOR der
Semaphore:

    cached = _LIVE_STATUS_CACHE.get(username)
    if cached and cached[0] > now and not force_fresh:
        return cached[1], cached[2]
    ...
    async with sem:                      # _RESOLVE_CONCURRENCY = 2
        ...volle Aufloesung...
        _LIVE_STATUS_CACHE[username] = (now + TTL, status, info)

Treffen zwei Aufrufer ein, bevor einer von ihnen geschrieben hat, passieren
BEIDE die Pruefung. Die Semaphore faengt das nicht: sie ist zwei gross, also
laufen genau zwei gleichzeitig durch — sie serialisiert alles ausser dem
Fall, der hier auftritt. Ergebnis: doppelte Last auf einem Dienst, der uns
ohnehin rate-limitet, doppelte Logzeile, und der Dedup, der im Kommentar
steht, existierte nie.

**Der zweite Fehler steckt im Zeitstempel.** `now` wird VOR der Aufloesung
genommen und danach fuer `now + TTL` benutzt. Die TTL ist 15 s; eine
Aufloesung ueber Webcast-API plus HTML-Weg braucht Sekunden, und seit W102
kommt im haeufigsten Fall ein yt-dlp-Lauf mit bis zu 20 s Timeout dazu. Der
Eintrag ist dann beim Schreiben **schon abgelaufen** — der Cache ist genau
dann wirkungslos, wenn er am meisten gebraucht wird. Gemessen in Vertrag (3):
bei einer Aufloesung von 20 s und TTL 15 s bleibt eine Restgueltigkeit von
**minus fuenf Sekunden**.

Reine Rechnung, kein Netz, keine Uhr aus dem Modul: die Zeit kommt als
Parameter, damit beides ohne Live-Stream pruefbar ist. Das Woerterbuch wird
in place fortgeschrieben — dasselbe Objekt, das `bot.py` und
`/api/debug/state` lesen.
"""

# Nur DEFINITIVE Antworten gehoeren in den Cache. "unknown" heisst „ich konnte
# es nicht ermitteln"; wer das zwischenspeichert, verlaengert einen Aussetzer
# um die TTL, statt es gleich noch einmal zu versuchen.
DEFINITIV = ("live", "offline")


def frisch(eintrag, jetzt) -> bool:
    """Gilt dieser Cache-Eintrag noch? Fehlender Eintrag -> False."""
    return bool(eintrag) and eintrag[0] > jetzt


def holen(cache, username, jetzt, force_fresh=False):
    """(status, info) aus dem Cache, oder None wenn nichts Gueltiges da ist.

    `None` und `("offline", None)` sind verschieden: das erste heisst „kein
    Treffer", das zweite ist ein gueltiger Treffer mit leerer Nutzlast. Ein
    Aufrufer, der auf Wahrheitswert prueft, wuerde beides verwechseln —
    deshalb gibt diese Funktion das Tupel oder `None`, nie ein leeres Tupel.

    **Zweimal aufrufen.** Einmal vor der Semaphore (der billige Weg, spart den
    Platz in der Warteschlange) und einmal INNERHALB (der richtige: dort ist
    der Schreiber des ersten Aufrufers fertig). Ohne den zweiten Aufruf
    loesen zwei gleichzeitige Aufrufer beide voll auf — siehe Modultext.
    """
    # EIN Ausgang. Ein vorzeitiges `return None` waere ein stummer
    # Misserfolgs-Rueckweg (tools/blindstellen.py zaehlt genau das) — und
    # „kein Treffer" ist hier kein Misserfolg, sondern der Normalfall. Melden
    # tut der Aufrufer, dieses Modul loggt nicht.
    treffer = None
    if not force_fresh:
        eintrag = cache.get(username)
        if frisch(eintrag, jetzt):
            treffer = (eintrag[1], eintrag[2])
    return treffer


def setzen(cache, username, status, info, jetzt, ttl) -> bool:
    """Eintragen, wenn die Antwort definitiv ist. Rueckgabe: eingetragen?

    `jetzt` muss der Zeitpunkt des SCHREIBENS sein, nicht der des Beginns der
    Aufloesung. Wer den alten Zeitstempel weiterbenutzt, verschenkt die
    Dauer der Aufloesung — und bei einer Aufloesung, die laenger als die TTL
    braucht, schreibt er einen Eintrag, der bereits abgelaufen ist.
    """
    if status not in DEFINITIV:
        return False
    cache[username] = (jetzt + ttl, status, info)
    return True


def aufraeumen(cache, jetzt, ab_groesse=50):
    """Abgelaufene Eintraege entfernen. Rueckgabe: Anzahl der entfernten.

    Opportunistisch beim Schreiben aufgerufen; unter `ab_groesse` lohnt der
    Durchlauf nicht.
    """
    alt = []
    if len(cache) > ab_groesse:
        alt = [k for k, v in cache.items() if not frisch(v, jetzt)]
        for k in alt:
            cache.pop(k, None)
    return len(alt)


# ═════════════════════════════════════════════════════════════════════════
# v4.2-W119: EIN Lauf je Nutzer, und Zahlen dazu
# ═════════════════════════════════════════════════════════════════════════
#
# Die zweite Pruefung aus W103 faengt den Aufrufer, der NACH dem Schreiben
# des ersten ankommt. Den, der WAEHREND der Aufloesung ankommt, faengt sie
# nicht: die Semaphore ist `RESOLVE_CONCURRENCY` (2) gross, beide stehen
# gleichzeitig darin, beide sehen einen leeren Cache. Bei 20 s yt-dlp ist
# "waehrend" kein Zufall, sondern das breite Fenster.
#
# `einflug` laesst je Schluessel genau EINEN Lauf zu; wer waehrenddessen
# kommt, wartet auf dessen Ergebnis statt einen eigenen zu starten. Scheitert
# der Lauf (Ausnahme oder Abbruch), bekommen die Wartenden `ersatz` — nie die
# Ausnahme des anderen: ein Worker, dem ein fremder `CancelledError` in die
# Schleife faellt, beendet sich, und dann prueft niemand mehr.

import asyncio as _asyncio
import threading as _threading

# Zaehler fuer /healthz. Unter der Sperre, weil /healthz im Flask-Thread liest.
_SPERRE = _threading.Lock()
ZAEHLER = {"treffer": 0, "fehlschlag": 0, "geteilt": 0, "laeufe": 0,
           "dauer_summe": 0.0, "dauer_max": 0.0, "schreibvorgaenge": 0}

# Alle so viele Schreibvorgaenge wird aufgeraeumt. Bis W119 hing das an
# `hash(username) & 63 == 0` — das ist je NUTZER fest, nicht je Schreiben:
# bei 40 Nutzern traf es mit rund 50 % keinen einzigen, und dann wurde nie
# aufgeraeumt. Der Kommentar daneben sagte "alle 100 Writes".
AUFRAEUM_TAKT = 64


def zaehle(art: str, n: int = 1) -> None:
    with _SPERRE:
        ZAEHLER[art] += n


def aufraeumen_faellig() -> bool:
    """Einen Schreibvorgang zaehlen. -> True bei jedem AUFRAEUM_TAKT-ten."""
    with _SPERRE:
        ZAEHLER["schreibvorgaenge"] += 1
        return ZAEHLER["schreibvorgaenge"] % AUFRAEUM_TAKT == 0


def dauer(sekunden: float) -> None:
    with _SPERRE:
        ZAEHLER["laeufe"] += 1
        ZAEHLER["dauer_summe"] += sekunden
        if sekunden > ZAEHLER["dauer_max"]:
            ZAEHLER["dauer_max"] = sekunden


async def einflug(laufend: dict, schluessel, erzeuger, ersatz):
    """`erzeuger()` hoechstens einmal gleichzeitig je `schluessel` ausfuehren.

    `laufend` ist das Register der laufenden Futures (vom Aufrufer gehalten,
    damit es inspizierbar bleibt). Der fuehrende Aufrufer bekommt Ergebnis
    oder Ausnahme wie gewohnt; Mitlaeufer bekommen das Ergebnis — oder
    `ersatz`, wenn der fuehrende Lauf scheiterte.
    """
    fut = laufend.get(schluessel)
    if fut is not None:
        zaehle("geteilt")
        # asyncio.wait statt await fut: es wirft nie die Ausnahme des Laufs
        # und bricht ihn nicht ab, wenn DIESER Aufrufer abgebrochen wird —
        # dann fliegt hier nur unser eigener CancelledError, wie es sein soll.
        # Ohne try/except: der Fehlschlag des fuehrenden Laufs ist dort
        # gemeldet, hier ist er die Antwort `ersatz`.
        await _asyncio.wait({fut})
        if fut.cancelled() or fut.exception() is not None:
            return ersatz
        return fut.result()
    fut = _asyncio.get_running_loop().create_future()
    # Liest niemand mehr mit, darf eine gesetzte Ausnahme nicht als
    # "Future exception was never retrieved" ins Log fallen.
    fut.add_done_callback(lambda f: f.cancelled() or f.exception())
    laufend[schluessel] = fut
    try:
        erg = await erzeuger()
    except _asyncio.CancelledError:
        fut.cancel()
        raise
    except BaseException as e:
        fut.set_exception(e)
        raise
    else:
        fut.set_result(erg)
        return erg
    finally:
        if laufend.get(schluessel) is fut:
            del laufend[schluessel]


def statistik(groesse: int = -1, laufend: int = -1) -> dict:
    """Fuer /healthz: Trefferquote und Aufloesungsdauer. Keine Namen."""
    with _SPERRE:
        z = dict(ZAEHLER)
    abfragen = z["treffer"] + z["fehlschlag"]
    return {
        "treffer": z["treffer"], "fehlschlag": z["fehlschlag"],
        "trefferquote": round(z["treffer"] / abfragen, 3) if abfragen else None,
        "geteilt": z["geteilt"], "laeufe": z["laeufe"],
        "dauer_mittel_ms": (round(1000.0 * z["dauer_summe"] / z["laeufe"], 0)
                            if z["laeufe"] else None),
        "dauer_max_ms": round(1000.0 * z["dauer_max"], 0),
        "eintraege": int(groesse), "laufend": int(laufend),
    }


def zaehler_zuruecksetzen() -> None:
    """Nur fuer die Vertraege."""
    with _SPERRE:
        for k in ZAEHLER:
            ZAEHLER[k] = 0.0 if isinstance(ZAEHLER[k], float) else 0
