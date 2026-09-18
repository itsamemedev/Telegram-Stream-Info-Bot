"""nc.telegramfehler — v4.2-W93: warum das Telegram-Polling klemmt.

════════════════════════════════════════════════════════════════════════
DER ANLASS
════════════════════════════════════════════════════════════════════════
Im Log vom 18.09. steht sechsmal hintereinander dasselbe, jedes Mal ueber
zwoelf Zeilen Traceback durch fremde Bibliotheksrahmen:

    ERROR | telegram.ext.Updater | default_error_callback:371 |
    Exception happened while polling for updates.
    Traceback (most recent call last):
      ... elf Rahmen aus telegram/ext/_utils/networkloop.py,
          _updater.py, _extbot.py, _bot.py, _baserequest.py ...
    telegram.error.Conflict: Conflict: terminated by other getUpdates
    request; make sure that only one bot instance is running

Das ist die Umkehrung des Befunds aus v4.2-W92: dort war die Meldung zu
KURZ, hier ist sie zu LANG — und beide sagen dem Betreiber dasselbe,
naemlich nichts. Kein Rahmen des Tracebacks steht in unserem Code, es gibt
nichts darin nachzusehen. Was fehlt, ist die eine Zeile: was ist die
Folge, und was ist zu tun.

════════════════════════════════════════════════════════════════════════
WARUM DAS NICHT NUR LAERM IST
════════════════════════════════════════════════════════════════════════
Ein `Conflict` hat zwei vollkommen verschiedene Bedeutungen, und im Log
sehen sie identisch aus:

  (a) **Neustart-Ueberlappung.** Die alte Instanz haengt noch in ihrem
      Long-Poll, die neue faengt schon an. Telegram gibt der neuen den
      409, bis die alte die Verbindung loslaesst — binnen etwa einer
      Minute. Genau das ist am 18.09. passiert: 07:23:42 bis 07:24:21
      Konflikt, ab 07:24:39 wieder HTTP 200. Voellig harmlos.

  (b) **Zwei laufende Instanzen.** Ein vergessener Handstart neben dem
      systemd-Dienst, eine zweite Box mit demselben BOT_TOKEN. Dann hoert
      es nie auf, und die Folge ist die gefaehrliche: die Updates gehen an
      die ANDERE Instanz. Dieser Bot nimmt weiter auf, sendet weiter und
      moderiert weiter — er bekommt nur keinen einzigen Telegram-Befehl
      mehr. Nichts stuerzt ab, nichts meldet sich; es geht bloss nichts.

Fall (b) ist damit dieselbe Klasse wie die stillen `return`s aus W81: ein
Ausfall ohne Absturz. Der Unterschied zu (a) ist nicht der Fehlertext —
der ist wortgleich — sondern die DAUER. Genau die misst dieses Modul.

════════════════════════════════════════════════════════════════════════
DIE REGEL
════════════════════════════════════════════════════════════════════════
  - Konflikt innerhalb der Gnadenfrist -> "konflikt_anlauf", Warnung, und
    dazu der Satz, dass ein Neustart genau so aussieht. Niemand soll
    nachts nach einer Ueberlappung suchen.
  - Konflikt darueber hinaus -> "konflikt_dauerhaft", Fehler, mit der
    Dauer und der Abhilfe. Weil der Grund-Schluessel wechselt, laesst
    nc.meldetakt die Eskalation SOFORT durch statt sie in die
    15-Minuten-Drossel zu stecken — der Wechsel ist die Nachricht.

Das Modul ist **bot-frei und uhrfrei**: es importiert `telegram` nicht (es
klassiert ueber den Klassennamen), loggt nicht selbst und liest keine
Zeit, sondern bekommt `jetzt` hereingereicht. Dieselbe Linie wie
nc.meldetakt und nc.resolvergrund — ohne Bot, ohne Netz und ohne Schlaf
pruefbar.
"""
from __future__ import annotations

from typing import Tuple

# So lange gilt ein Konflikt als Neustart-Ueberlappung. Gemessen am Fall vom
# 18.09.: 07:23:42 erster Konflikt, 07:24:39 wieder HTTP 200 — 57 s. 90 s
# lassen Luft fuer eine zaeher sterbende alte Instanz, ohne den Fall (b) eine
# geschlagene Viertelstunde lang als harmlos auszugeben.
GNADENFRIST_S = 90.0

# So lange ohne Konflikt heisst: die Straehne ist vorbei, der naechste
# Konflikt faengt eine neue an. PTBs Wiederholungsabstand waechst bei
# anhaltendem Fehler nur in den Bereich einer halben Minute (am 18.09.
# gemessen: 6, 6, 6, 9, 12 s) — 300 s liegen weit darueber. Ohne diese
# Grenze wuerde eine Stunde spaeter ein einzelner, neuer Konflikt sofort als
# "haelt seit einer Stunde an" gemeldet, und das waere schlicht falsch.
STRAEHNE_ENDE_S = 300.0

# Zustand der laufenden Konflikt-Straehne. Ein Dict und keine Modul-Globals:
# wer zuruecksetzt, muss fuer ALLE Leser zuruecksetzen (dieselbe Falle wie
# bei _RESTREAM_ACTIVE, W18, und nc.meldetakt.ZUSTAND).
STRAEHNE: dict = {"seit": None, "zuletzt": None}

# Grund-Schluessel -> Klartext. Bewusst mit Abhilfe und bewusst mit der
# FOLGE: "Conflict" allein sagt nicht, dass Telegram-Befehle ausfallen.
GRUND = {
    "konflikt_anlauf":
        "Eine zweite getUpdates-Abfrage hat den Long-Poll uebernommen. Bei "
        "einem Neustart ist das der Normalfall — die alte Instanz haelt ihre "
        "Verbindung noch bis zu einer Minute. Hoert es binnen der Gnadenfrist "
        "auf, war es genau das und nichts ist zu tun.",
    "konflikt_dauerhaft":
        "Der Konflikt haelt laenger an, als eine Neustart-Ueberlappung dauern "
        "kann: es laeuft WIRKLICH eine zweite Instanz mit demselben "
        "BOT_TOKEN. Folge: DIESER Bot bekommt keine Telegram-Befehle mehr — "
        "die Updates gehen an die andere Instanz. Aufnahme, Restream und "
        "Moderation laufen unbeeindruckt weiter, deshalb faellt es sonst "
        "nirgends auf. Abhilfe: auf ALLEN Maschinen (auch der Test-Box) "
        "nachsehen — pgrep -af 'python3.*bot.py' — und die zweite beenden: "
        "sudo systemctl stop tiktok-bot bzw. kill <PID>.",
    "konflikt_webhook":
        "Fuer diesen Token ist ein Webhook eingetragen, und Telegram laesst "
        "getUpdates und Webhook nicht nebeneinander zu. Folge: keine "
        "Telegram-Befehle. Abhilfe: curl -s "
        "'https://api.telegram.org/bot<TOKEN>/deleteWebhook' — danach "
        "greift das Polling beim naechsten Versuch von selbst.",
    "token_ungueltig":
        "Telegram lehnt das BOT_TOKEN ab. Das heilt nicht von selbst: die "
        "Telegram-Befehle bleiben aus, bis der Token stimmt. Abhilfe: "
        "BOT_TOKEN in der .env gegen den Wert aus dem BotFather pruefen "
        "(/mybots -> API Token), auf Leerzeichen und Zeilenumbrueche achten.",
    "verboten":
        "Telegram antwortet mit 403. Meist ist der Bot aus dem Chat geworfen "
        "oder blockiert worden. Abhilfe: den Bot der Gruppe erneut "
        "hinzufuegen bzw. den Chat wieder oeffnen.",
    "zu_schnell":
        "Telegram drosselt (429, Flood-Limit) und nennt eine Wartezeit. PTB "
        "haelt sie selbst ein. Haelt es an, fragt der Bot zu haeufig ab — "
        "dann gehoert das Poll-Intervall hoch.",
    "zeitueberschreitung":
        "Telegram hat nicht rechtzeitig geantwortet. Einzeln harmlos (der "
        "Long-Poll laeuft in seine eigene Frist), dauerhaft ein Netz- oder "
        "Proxy-Problem. PTB versucht es selbst weiter.",
    "netz":
        "Telegram ist nicht erreichbar (DNS, Route, Proxy oder TLS). PTB "
        "versucht es selbst weiter; bleibt es dabei, hilft nur ein Blick auf "
        "das Netz der Box: curl -s https://api.telegram.org/ >/dev/null && "
        "echo erreichbar.",
}

# Welche Stufe gehoert zu welchem Grund. Ein Dauerkonflikt und ein falscher
# Token sind Ausfaelle des Dienstes und gehoeren auf `error` — alles andere
# heilt sich und waere auf `error` nur Rauschen, das die echten Faelle
# zudeckt. Genau daran ist der Discord-Gateway-Tod monatelang vorbeigelaufen,
# nur in die andere Richtung (CLAUDE.md).
FEHLERSTUFE = ("konflikt_dauerhaft", "konflikt_webhook", "token_ungueltig")


def text(grund: str) -> str:
    """Klartext zu einem Grund-Schluessel. Unbekannt -> der Schluessel selbst,
       damit eine neue Kategorie im Log auftaucht statt zu verschwinden."""
    return GRUND.get(grund, grund or "unbekannt")


def ist_fehler(grund: str) -> bool:
    """Gehoert dieser Grund auf `error` (statt auf `warning`)?"""
    return grund in FEHLERSTUFE


def _klassenname(exc) -> str:
    return type(exc).__name__ if exc is not None else ""


def grund(exc, jetzt: float) -> Tuple[str, float]:
    """Was ist da schiefgegangen? -> (grund_schluessel, dauer_s)

    `dauer_s` ist nur beim Konflikt von Belang: die Laenge der laufenden
    Straehne in Sekunden. Sonst 0.0.

    Klassiert wird ueber den KLASSENNAMEN, nicht ueber isinstance: dieses
    Modul soll ohne installiertes python-telegram-bot importierbar und
    pruefbar bleiben (nc/ ist bot-frei, und die Suite laeuft ohne das
    Paket). Der Klassenname ist dafuer stabil genug — er ist Teil der
    oeffentlichen API von telegram.error.
    """
    name = _klassenname(exc)
    meldung = str(exc or "")
    if name == "Conflict":
        # Zwei Konflikte mit voellig verschiedener Abhilfe, und nur der Text
        # unterscheidet sie. Telegram schreibt beim Webhook-Fall woertlich
        # "can't use getUpdates method while webhook is active".
        if "webhook" in meldung.lower():
            return "konflikt_webhook", 0.0
        return _konflikt_straehne(jetzt)
    if name == "InvalidToken":
        return "token_ungueltig", 0.0
    if name == "Forbidden":
        return "verboten", 0.0
    if name == "RetryAfter":
        return "zu_schnell", 0.0
    if name == "TimedOut":
        return "zeitueberschreitung", 0.0
    if name == "NetworkError":
        return "netz", 0.0
    # Unbekanntes bekommt den Klassennamen IN den Schluessel. Ein Sammeltopf
    # "unbekannt" wuerde zwei verschiedene neue Fehlerbilder zu einem
    # verschmelzen — und dann schluckt die Drossel das zweite, weil sich der
    # Grund fuer sie nicht geaendert hat.
    return ("unbekannt:%s" % (name or "?"), 0.0)


def _konflikt_straehne(jetzt: float) -> Tuple[str, float]:
    """Laeuft der Konflikt noch im Anlauf oder schon dauerhaft?"""
    jetzt = float(jetzt)
    seit, zuletzt = STRAEHNE["seit"], STRAEHNE["zuletzt"]
    if seit is None or zuletzt is None or (jetzt - zuletzt) > STRAEHNE_ENDE_S:
        # Neue Straehne — entweder die erste oder eine nach langer Ruhe.
        STRAEHNE["seit"] = jetzt
        STRAEHNE["zuletzt"] = jetzt
        return "konflikt_anlauf", 0.0
    STRAEHNE["zuletzt"] = jetzt
    dauer = jetzt - float(seit)
    if dauer > GNADENFRIST_S:
        return "konflikt_dauerhaft", dauer
    return "konflikt_anlauf", dauer


def zuruecksetzen() -> None:
    """Die Konflikt-Straehne vergessen. Nach einem sauberen Start oder in der
       Pruefung — ohne das traegt ein Testlauf den Zustand in den naechsten."""
    STRAEHNE["seit"] = None
    STRAEHNE["zuletzt"] = None


def dauer_text(dauer_s: float) -> str:
    """Die Dauer als Klartext fuer die Meldung. Ohne Nachkommastellen: es geht
       um 'seit zwei Minuten', nicht um 127,4 Sekunden."""
    s = int(max(0.0, float(dauer_s or 0.0)))
    if s < 120:
        return "%d s" % s
    if s < 7200:
        return "%d min" % (s // 60)
    return "%d h" % (s // 3600)
