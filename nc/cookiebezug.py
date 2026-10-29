"""nc.cookiebezug — v4.2-W107: der automatische Cookie-Bezug als Standardweg.

Der Betreiber: „Cookies automatisch beziehen soll Standard sein." Im Code
stand das seit W10 so — `COOKIE_AUTO_FETCH` ist per Vorgabe an. Nachgesehen,
WANN der Bezug wirklich lief, und die Antwort war: fast nie.

1. Er hing im Telegram-Cookie-Alarm (`_cookie_alarm_loop`). Der wird nur
   gestartet, wenn `DISK_ALARM_CHAT_ID` oder `DAILY_SUMMARY_CHAT_ID` gesetzt
   ist — und beendet sich sonst mit einer Zeile auf `warning`. Ohne
   Alarm-Chat lief der „Standard" also NIE. Eine Abhaengigkeit, die nirgends
   steht und die niemand vermutet: Cookies holen hat mit Telegram nichts zu
   tun.
2. Auch mit Chat lief er nur bei rotem Health-Check, im Takt des
   Platten-Alarms (Vorgabe eine Stunde), und frühestens 60 s nach dem Start.
   Eine frische Installation ohne Cookie-Datei wartete damit bis zum ersten
   Alarm-Tick.
3. Ein 403 der Aufnahme oder der Stream-Aufloesung — genau das Symptom, das
   abgelaufene Anti-Bot-Tokens erzeugen — stiess nichts an.
4. Der Deck-Knopf rief `nc/cookieholen.aktualisiere` direkt und ging am
   Buchhalter vorbei: nach einem erfolgreichen Klick stand im Deck weiter
   „Auto-Bezug: noch nie gelaufen".

Hier steht deshalb der eine Zeitplan mit seinem Zustand, und jeder Weg —
Schleife, 403, Deck-Knopf, Telegram — geht durch `holen()`. Die Schleife
selbst bleibt bot-seitig (sie braucht `_hb` und `_loop_fehler`), fragt aber
nur `faellig()`.

**Was der Bezug kann, und was nicht** — die Grenze steht in
nc/cookieholen.py und gilt hier unveraendert: ein Gast-Aufruf erneuert die
rotierenden Anti-Bot-Tokens (ttwid, msToken, tt_chain_token, …). Einen Login
(`sessionid`) erzeugt er NIE. Deshalb loest ein roter Health-Check nur dann
einen Bezug aus, wenn ein Gast-Aufruf ihn ueberhaupt heilen kann
(`gast_hilft`) — sonst stuende auf einer Installation ohne Login alle halbe
Stunde ein Aufruf bei TikTok, der garantiert nichts aendert.
"""

import time
from typing import Optional, Tuple

from nc import cookieholen as _holen

# Nach einem Fehlschlag nicht das volle Intervall warten: ein nicht
# erreichbares TikTok um 03:00 hiesse sonst „naechster Versuch 09:00".
NEU_VERSUCH_S = 30 * 60
# Mindestabstand fuer ANGESTOSSENE Bezuege (403, Health). Kurz genug, dass
# ein 403-Schwall binnen Minuten frische Tokens bekommt, lang genug, dass 40
# Trackings im 403 nicht 40 Aufrufe bei TikTok ausloesen — genau die Sorte
# Selbstbeschuss, die eine IP auf die Sperrliste bringt.
ANSTOSS_ABSTAND_S = 15 * 60

# Die Anti-Bot-Namen, die ein Gast-Aufruf liefern kann — aus nc/cookieholen,
# nicht abgeschrieben. Zwei Listen fuer denselben Zweck sind hier schon
# dreimal auseinandergelaufen (CLAUDE.md, W100).
GAST_NAMEN = frozenset(_holen.ANTIBOT)

# Resolver-Gruende, hinter denen abgelaufene Anti-Bot-Tokens stecken koennen.
# Bewusst nicht "netz" oder "html_kein_tag": dort hilft kein Cookie.
RESOLVER_ANSTOSS = frozenset({"http_403", "status_code", "kein_json"})

_KONF = {"datei": None, "aktiv": True, "intervall_h": 6.0, "timeout": 15,
         "nach_erfolg": None, "log": None}

# Der eine Zustand. Wanduhr (time.time), nicht monotonic: das Deck zeigt
# „zuletzt" und „naechster Lauf" als Uhrzeit.
STAND = {"last_try": 0.0, "last_ok": None, "last_error": None, "count": 0,
         "last_report": None, "last_anlass": None, "anstoss": None}


def configure(datei, aktiv=True, intervall_h=6.0, timeout=15,
              nach_erfolg=None, log=None):
    """Vom Bot einmal beim Start. `nach_erfolg` leert den Cookie-Cache des
    Recorders — sonst liest er nach einem Bezug noch 5 s den alten Stand."""
    _KONF.update(datei=datei, aktiv=bool(aktiv),
                 intervall_h=max(0.25, float(intervall_h or 6.0)),
                 timeout=int(timeout or 15), nach_erfolg=nach_erfolg, log=log)


def intervall_s() -> float:
    return _KONF["intervall_h"] * 3600.0


def gast_hilft(gesundheit) -> bool:
    """Kann ein Gast-Aufruf diesen Health-Zustand verbessern?

    Ja bei: keiner Datei, unlesbarer Datei, oder einem fehlenden bzw.
    abgelaufenen Anti-Bot-Token. Nein bei einem fehlenden Login — den holt
    kein Gast-Aufruf, und ihn trotzdem anzustossen hiesse, alle 15 Minuten
    TikTok zu fragen, ohne dass sich je etwas aendert.
    """
    g = gesundheit or {}
    if not g.get("exists", True) or g.get("status") == "parse_error":
        return True
    fehlt = set(g.get("critical_missing") or ())
    abgelaufen = {(e or {}).get("name") for e in (g.get("expired") or ())
                  if isinstance(e, dict)}
    return bool((fehlt | abgelaufen) & GAST_NAMEN)


def anstossen(anlass: str) -> None:
    """Ein Ereignis meldet: frische Tokens koennten helfen. Billig und
    thread-sicher genug (eine Zuweisung) — die Schleife holt es ab und
    entscheidet ueber `faellig`, ob wirklich gefragt wird."""
    STAND["anstoss"] = anlass


def faellig(jetzt: float, gesundheit=None) -> Tuple[bool, str]:
    """Soll die Schleife JETZT beziehen? -> (ja, Anlass)

    Der Anlass ist kein Schmuck: er steht in der Logzeile und im Deck. Ein
    Automat, bei dem niemand sieht, WARUM er laeuft, ist von einem kaputten
    nicht zu unterscheiden.
    """
    if not _KONF["aktiv"]:
        return False, "aus"
    seit = jetzt - STAND["last_try"] if STAND["last_try"] else None
    if seit is None:
        return True, "start"
    if gesundheit is not None and gast_hilft(gesundheit) \
            and seit >= ANSTOSS_ABSTAND_S:
        return True, "gesundheit"
    if STAND["anstoss"] and seit >= ANSTOSS_ABSTAND_S:
        return True, STAND["anstoss"]
    if STAND["last_error"] and seit >= min(NEU_VERSUCH_S, intervall_s()):
        return True, "neuer_versuch"
    if seit >= intervall_s():
        return True, "plan"
    return False, "wartet"


def naechster_lauf(jetzt: float) -> Optional[float]:
    """Wann die Schleife ohne Anstoss das naechste Mal bezieht (Wanduhr).

    None heisst „nie" (abgeschaltet) — eine Antwort, kein Fehler."""
    warte = min(NEU_VERSUCH_S, intervall_s()) if STAND["last_error"] \
        else intervall_s()
    lauf = STAND["last_try"] + warte if STAND["last_try"] else jetzt
    return lauf if _KONF["aktiv"] else None


def holen(quelle="gast", browser=None, anlass="hand", proxy=None,
          urls=None, domains=None) -> dict:
    """Der eine Bezugsweg fuer Schleife, Deck und Telegram. Wirft nie.

    Die Drossel steht NICHT hier, sondern in `faellig`: ein Knopfdruck des
    Betreibers ist ein ausdruecklicher Wunsch und wird nicht wegrationiert.
    """
    STAND["last_try"] = time.time()
    STAND["last_anlass"] = anlass
    STAND["anstoss"] = None
    bericht = _holen.aktualisiere(
        _KONF["datei"], quelle=quelle, browser=browser,
        timeout=_KONF["timeout"], proxy=proxy, log=_KONF["log"],
        urls=urls, domains=domains)
    bericht["anlass"] = anlass
    if bericht.get("ok"):
        STAND["last_ok"] = STAND["last_try"]
        STAND["last_error"] = None
        STAND["count"] += len(bericht.get("added") or []) + \
            len(bericht.get("replaced") or [])
        if callable(_KONF["nach_erfolg"]):
            _KONF["nach_erfolg"]()
    else:
        STAND["last_error"] = bericht.get("error") or "unbekannt"
    STAND["last_report"] = bericht
    return bericht


def _iso(ts):
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(ts)) if ts else None


def info(jetzt: float = None) -> dict:
    """Was das Deck und /healthz zeigen. Die Schluessel der W10-Fassung
    (`enabled`, `interval_h`, `last_ok`, `fetched_total`, `last_error`)
    bleiben — das Deck liest sie."""
    jetzt = time.time() if jetzt is None else jetzt
    return {"enabled": _KONF["aktiv"],
            "interval_h": _KONF["intervall_h"],
            "last_ok": _iso(STAND["last_ok"]),
            "last_try": _iso(STAND["last_try"]),
            "next_run": _iso(naechster_lauf(jetzt)),
            "last_anlass": STAND["last_anlass"],
            "pending": STAND["anstoss"],
            "fetched_total": STAND["count"],
            "last_error": STAND["last_error"]}
