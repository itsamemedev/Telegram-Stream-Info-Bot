"""nc.whispercfg — v4.1-W19: welches Whisper-Modell laeuft, und laeuft es ueberhaupt.

════════════════════════════════════════════════════════════════════════
WARUM DIESES MODUL
════════════════════════════════════════════════════════════════════════
`/api/azrael/whisper_model` schaltet das Spracherkennungs-Modell zur Laufzeit
um. Im Monolithen tat es das mit

    global _whisper_model, WHISPER_MODEL_NAME

also durch NEUBINDUNG zweier Modul-Globals. In einem Blueprint waere `global`
der Namensraum DES BLUEPRINTS: der Name im Bot bliebe unveraendert, die Route
meldete Erfolg, und der naechste Transkript-Lauf benutzte weiter das alte
Modell. Eine stille Fehlanzeige — dieselbe Falle wie bei `_MAIN_LOOP` (W116)
und `_RESTREAM_ACTIVE` (W18).

Deshalb ein **Register**: der Bot und die Route greifen auf DASSELBE Dict zu,
und wer den Namen neu bindet, aendert ihn fuer beide.

`obj` ist das geladene Modell (teuer, wird lazy geladen). Ein Modellwechsel
setzt es auf None — der naechste Transkript-Lauf laedt neu. Genau deshalb
gehoeren Name und Objekt in EIN Register: wer nur den Namen aendert und das
Objekt stehen laesst, benutzt weiter das alte Modell und sieht den neuen Namen
im Dashboard. Das waere schlimmer als gar kein Umschalten.
"""

import contextlib
import logging
import os
import re
import threading
import time

# Register: Name UND geladenes Objekt. Beide werden neu gebunden.
# v5.2-W193: "zuletzt" = monotonic der letzten Anforderung (fuer das Entladen).
MODELL = {"name": "base", "obj": None, "zuletzt": 0.0, "entladen": 0, "laufend": 0}
_GEBRAUCH_SPERRE = threading.Lock()


@contextlib.contextmanager
def gebrauch():
    """Um jede Transkription legen (im Thread). Solange eine laeuft, wird nicht
    entladen: eine lange Archiv-Transkription hielte ihr Modell fest, und der
    naechste Live-Satz luede ein ZWEITES — doppelter Speicher statt weniger."""
    with _GEBRAUCH_SPERRE:
        MODELL["laufend"] += 1
    try:
        yield
    finally:
        with _GEBRAUCH_SPERRE:
            MODELL["laufend"] -= 1
        MODELL["zuletzt"] = time.monotonic()


def benutzt(jetzt) -> None:
    """Bei jeder Anforderung des Modells aufrufen."""
    MODELL["zuletzt"] = float(jetzt)


def leerlauf_s() -> float:
    """WHISPER_ENTLADEN_MIN (Vorgabe 15; 0 = nie) in Sekunden. Als Funktion gelesen.

    v5.2-W193: das Modell blieb nach dem ersten Satz fuer immer geladen —
    `medium` belegt rund 1,5 GB, und der Sprung am 11.11. (W180) auf 4,5 GB RSS
    war genau so ein Modell, das danach nie wieder ging."""
    roh = os.getenv("WHISPER_ENTLADEN_MIN", "15").strip()
    return max(0.0, float(roh)) * 60 if roh.replace(".", "", 1).isdigit() else 900.0


def entladen_wenn_leer(jetzt, leerlauf) -> bool:
    """Modell verwerfen, wenn es `leerlauf` s nicht angefordert wurde. -> True = verworfen.

    Sicher auch waehrend einer laufenden Transkription: die haelt ihr Modell
    selbst als lokale Variable, freigegeben wird es erst nach ihrem Ende."""
    if MODELL["obj"] is None or leerlauf <= 0 or MODELL["laufend"] > 0:
        return False
    if float(jetzt) - MODELL["zuletzt"] < leerlauf:
        return False
    MODELL["obj"] = None
    MODELL["entladen"] += 1
    return True

# Die Auswahl im Dashboard. Kein Zwang — ein eigener Name wird akzeptiert,
# faster-whisper laedt auch Modelle, die hier nicht stehen.
PRESETS = ["tiny", "base", "small", "medium", "large-v3",
           "tiny.en", "base.en", "small.en", "medium.en"]


def name() -> str:
    return MODELL["name"]


def geladen() -> bool:
    return MODELL["obj"] is not None


def waehle(neuer_name: str):
    """Modell umschalten: Name setzen, geladenes Objekt verwerfen.

    Beides in einem Zug — siehe Modul-Kopf. Gibt den gesetzten Namen zurueck.
    """
    MODELL["name"] = str(neuer_name or "").strip() or MODELL["name"]
    MODELL["obj"] = None
    return MODELL["name"]


def verfuegbar() -> bool:
    """Ist faster-whisper installiert? Nur der Import, kein Modell-Laden —
       die Frage im Dashboard lautet 'kann der Server das ueberhaupt', nicht
       'ist es schon warm'.

       v4.2-W1: bot.py hielt bis hierher eine ZWEITE Fassung
       (`_faster_whisper_available`) — dieselben drei Zeilen, aber ohne das
       try. Ein kaputter Paket-Baum haette dort eine Ausnahme geworfen statt
       "nein" zu sagen. Der Bot benutzt jetzt diese hier.
       """
    try:
        import importlib.util
        return importlib.util.find_spec("faster_whisper") is not None
    except Exception:
        return False


# ═════════════════════════════════════════════════════════════════════════
# v5.1-W180: Speicherbedarf — ein Modellwechsel, den die Box nicht traegt
# ═════════════════════════════════════════════════════════════════════════
#
# Gemessen am 11.11. (Produktionslog): um 18:08:20 wurde im Deck von `base`
# auf `medium` umgeschaltet. 14 s spaeter meldete der Watchdog RSS 3321 MB,
# eine Viertelstunde danach 4535 MB — vorher 973 MB. Das Laden von `base`
# am selben Nachmittag hatte den Prozess von 391 auf 890 MB gehoben. Dazu
# lief `medium` mit RTF 2,74, also fast dreimal langsamer als das Audio:
# jeder Transkriptionslauf hielt den Fork-Riegel entsprechend lange, und
# die Live-Pruefung verhungerte daran (W183, nc/forkriegel.py).
#
# Die Route schaltete bis hier blind um. Jetzt wird vorher gefragt, ob der
# freie Speicher das neue Modell traegt — und wenn nicht, mit Zahlen und
# Abhilfe abgelehnt. Die Werte sind der RSS-Zuwachs im Betrieb (CPU, int8,
# Gewichte plus Arbeitsspeicher eines Laufs), nicht die Dateigroesse: die
# ist bei `medium` 1,5 GB, im Prozess wurden es ueber 3 GB.
BEDARF_MB = {
    "tiny": 300,
    "base": 500,
    "small": 1200,
    "medium": 3000,
    "large": 6000,
    "turbo": 3500,
}
RESERVE_MB = 512     # Rest fuer Aufnahmen, Restreams und den Bot selbst


def bedarf_mb(modell):
    """Geschaetzter RSS-Zuwachs eines Modells in MB — None, wenn unbekannt.

    `.en`-Varianten und `distil-`-Fassungen gehoeren zur Groessenklasse ihres
    Grundmodells; `large-v2`/`large-v3` sind `large`. Ein eigener Name, den
    die Tabelle nicht kennt, ist keine Ablehnung wert — nur nicht pruefbar."""
    n = str(modell or "").strip().lower()
    for vorsilbe in ("faster-distil-whisper-", "faster-whisper-", "distil-"):
        if n.startswith(vorsilbe):
            n = n[len(vorsilbe):]
    n = n.split(".")[0]
    if n.startswith("large-v3-turbo") or n == "turbo":
        return BEDARF_MB["turbo"]
    if n.startswith("large"):
        return BEDARF_MB["large"]
    return BEDARF_MB.get(n)


def frei_mb(meminfo_text=None):
    """MemAvailable aus /proc/meminfo in MB — None, wenn nicht lesbar.

    None heisst „unbekannt" (kein Linux, kein procfs) und ist KEINE Null:
    eine Null wuerde jeden Wechsel ablehnen."""
    if meminfo_text is None:
        try:
            with open("/proc/meminfo", encoding="ascii", errors="replace") as f:
                meminfo_text = f.read()
        except OSError as e:
            # Nicht stumm: ohne diese Zahl prueft der Modellwechsel nicht vor,
            # und genau das soll im Log stehen, wenn danach der RSS springt.
            logging.getLogger("TikTokBot").warning(
                "Whisper: /proc/meminfo nicht lesbar (%s) — Speicherbedarf wird "
                "vor dem Modellwechsel nicht geprueft.", e)
            return None
    m = re.search(r"^MemAvailable:\s*(\d+)", str(meminfo_text), re.M)
    return int(m.group(1)) // 1024 if m else None


def wechsel_pruefen(neu, frei=None):
    """Traegt der Speicher den Wechsel auf `neu`? -> (erlaubt, grund)

    `frei` ist MemAvailable in MB (None = unbekannt). Gezaehlt wird der VOLLE
    Bedarf des neuen Modells, nicht die Differenz zum alten: das alte Objekt
    haengt an laufenden Transkriptionen und wird erst nach dem Laden des
    neuen frei — eine Differenz rechnete mit Speicher, der im entscheidenden
    Moment noch belegt ist.

    `grund` ist bei Erlaubnis ein Hinweis (oder ""), bei Ablehnung der
    Klartext mit Zahlen und Abhilfe."""
    bedarf = bedarf_mb(neu)
    if bedarf is None:
        return True, "Speicherbedarf von '%s' unbekannt — nicht vorab geprueft." % neu
    if frei is None:
        return True, "freier Speicher nicht lesbar — nicht vorab geprueft."
    if bedarf + RESERVE_MB <= frei:
        return True, ""
    rat = [m for m in ("small", "base", "tiny")
           if BEDARF_MB[m] + RESERVE_MB <= frei and BEDARF_MB[m] < bedarf]
    return False, (
        "Whisper-Modell '%s' braucht im Betrieb rund %d MB, frei sind %d MB "
        "(dazu %d MB Reserve fuer Aufnahmen und Restreams) — der Wechsel triebe "
        "den Bot in den OOM-Killer. Abhilfe: %s; erzwingen mit force=true."
        % (neu, bedarf, frei, RESERVE_MB,
           ("ein kleineres Modell (%s)" % ", ".join(rat)) if rat
           else "mehr RAM oder weniger gleichzeitige Restreams"))


def rss_hinweis():
    """Zusatz fuer die RSS-Meldung des Watchdogs: haelt Whisper den Speicher?

    Die Meldung vom 11.11. lautete nur „RSS 3321 MB (>1800) — Speicher-
    Wachstum, OOM-Killer-Gefahr" und klang nach einem Leck. Es war das eben
    geladene `medium`. Ein geladenes Modell ab 1 GB Bedarf wird deshalb
    genannt — mit dem Schalter, der es zuruecknimmt."""
    bedarf = bedarf_mb(MODELL["name"]) if MODELL["obj"] is not None else None
    gross = bool(bedarf and bedarf >= 1000)
    return (" Davon belegt das geladene Whisper-Modell '%s' rund %d MB — Abhilfe: "
            "im Deck (AZRAEL › Whisper) auf base/small zurueck oder WHISPER_MODEL in "
            "der .env." % (MODELL["name"], bedarf)) if gross else ""
