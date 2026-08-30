"""nc.i18n — v4.1-W6: Mehrsprachigkeit fuer Dashboard, Website und Bot.

Der Ansatz: **die deutsche Zeichenkette IST der Schluessel.** Kein Katalog aus
kuenstlichen IDs, keine 2.000 Einzelaenderungen im Bestand.

Warum so und nicht mit Schluesseln wie `dashboard.panel.recordings.title`:
Der Bestand hat rund 2.000 uebersetzbare Zeichenketten, verteilt ueber
templates/dashboard.html (12.000 Zeilen), bot.py und die Website. Jede davon
gegen einen Schluessel zu tauschen waere ein Umbau an 2.000 Stellen — nicht
rueckrollbar, nicht einzeln pruefbar und mit sicherem Verlust einzelner
Strings. Mit der Quellzeichenkette als Schluessel bleibt der Bestand
unveraendert lesbar: wer Deutsch liest, sieht weiterhin Deutsch im Quelltext,
und ein fehlender Eintrag faellt auf Deutsch zurueck statt auf einen nackten
Schluesselnamen.

Der Preis ist bekannt und bewusst getragen: aendert sich der deutsche Text,
faellt seine Uebersetzung zurueck auf Deutsch statt zu verschwinden. Deshalb
gibt es tools/i18n_extract.py --check: es meldet Katalogeintraege, die im
Quelltext nicht mehr vorkommen (verwaiste Uebersetzungen) und Fundstellen ohne
Eintrag (fehlende Uebersetzungen).

Architektur-Grenze wie ueberall in nc/: kein Import aus bot.py, stdlib-only.
"""

import contextvars
import json
import os
import re
import threading

# Die Quellsprache. Der Bestand ist auf Deutsch geschrieben, deshalb braucht
# Deutsch keinen Katalog — der Schluessel IST schon der deutsche Text.
QUELLSPRACHE = "de"

# Was ausgeliefert wird. Reihenfolge = Reihenfolge im Umschalter.
SPRACHEN = ("de", "en")

# Anzeigenamen, jeweils in der eigenen Sprache — so findet sich auch jemand
# zurecht, der die aktuelle Oberflaechensprache nicht liest.
SPRACHNAMEN = {"de": "Deutsch", "en": "English"}

_kataloge = {}
_lock = threading.Lock()
_verzeichnis = None
_standard = QUELLSPRACHE

# v4.1-W7: die Sprache DES GERADE BEDIENTEN BENUTZERS.
#
# Warum eine ContextVar und kein Modul-Global: Telegram und Discord bearbeiten
# mehrere Anfragen gleichzeitig, jede in ihrer eigenen asyncio-Task. Ein
# Modul-Global waere ein geteilter Zustand zwischen ihnen — der Deutsche bekaeme
# die Antwort auf Englisch, weil eine Millisekunde vorher ein Englaender etwas
# gefragt hat. Eine ContextVar wird je Task getrennt gefuehrt und vererbt sich
# an alles, was innerhalb der Task awaited wird.
#
# Warum ueberhaupt implizit statt als Parameter: der Bot hat 208 Sendestellen.
# Eine Sprache durch alle durchzureichen waere ein Umbau an 208 Stellen, bei dem
# garantiert welche vergessen werden — und eine vergessene Stelle antwortet
# stumm in der falschen Sprache, ohne dass irgendetwas auffaellt.
_aktuelle = contextvars.ContextVar("nc_i18n_sprache", default=None)


def sprache_setzen(sprache):
    """Die Sprache fuer diese Anfrage setzen. Unbekanntes setzt nichts."""
    norm = normalisieren(sprache)
    if norm:
        _aktuelle.set(norm)
    return norm


def aktuelle_sprache():
    """Die Sprache dieser Anfrage, sonst der Standard."""
    return _aktuelle.get() or _standard


def configure(*, verzeichnis=None, standard=None):
    """Vom Bot einmal beim Start gerufen.

    `verzeichnis` ist der Ordner mit den <sprache>.json-Katalogen; ohne Angabe
    liegt er neben diesem Modul (locales/ im Projekt). `standard` ist die
    Sprache fuer alles, was keine eigene Angabe mitbringt — Hintergrund-Jobs,
    Logzeilen, ein Aufruf ohne Request-Kontext.
    """
    global _verzeichnis, _standard
    if verzeichnis is not None:
        _verzeichnis = verzeichnis
    if standard is not None:
        _standard = standard if standard in SPRACHEN else QUELLSPRACHE
    with _lock:
        _kataloge.clear()


def _pfad():
    if _verzeichnis:
        return _verzeichnis
    return os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "locales")


def katalog(sprache):
    """Der geladene Katalog einer Sprache. Fehlt er, ist er leer — dann faellt
       jede Uebersetzung auf den deutschen Quelltext zurueck, statt dass die
       Oberflaeche mit Schluesselnamen zerfaellt."""
    sprache = sprache or _standard
    # v4.1-W10 (CodeQL py/path-injection): NUR bekannte Sprachen. Der Name
    # wandert unten in einen Dateipfad, und katalog() ist aus der Route
    # /api/i18n/katalog?lang=… erreichbar. Ohne diese Schranke liest
    # lang=../../irgendwas eine beliebige JSON-Datei vom Server. Unbekanntes
    # faellt auf den leeren Katalog — also auf Deutsch, die immer gueltige
    # Antwort — statt zu werfen.
    if sprache not in SPRACHEN:
        return {}
    if sprache == QUELLSPRACHE:
        return {}
    with _lock:
        if sprache in _kataloge:
            return _kataloge[sprache]
    daten = {}
    try:
        with open(os.path.join(_pfad(), "%s.json" % sprache), encoding="utf-8") as f:
            roh = json.load(f)
        # Format: {"strings": {"deutsch": "english", ...}}. Ein flaches Dict
        # wird ebenfalls angenommen, damit ein von Hand gebauter Katalog laeuft.
        daten = roh.get("strings", roh) if isinstance(roh, dict) else {}
        daten = {k: v for k, v in daten.items() if isinstance(v, str) and v}
    except FileNotFoundError:
        pass
    except Exception:
        # Ein kaputter Katalog darf die Oberflaeche nicht mitnehmen. Deutsch
        # ist immer eine gueltige Antwort.
        daten = {}
    with _lock:
        _kataloge[sprache] = daten
    return daten


def t(text, sprache=None, **kw):
    """Uebersetzt eine deutsche Zeichenkette. Unbekanntes bleibt Deutsch.

    Platzhalter werden NACH der Uebersetzung eingesetzt (str.format), damit ein
    Katalogeintrag die Reihenfolge aendern darf — im Englischen steht das Objekt
    oft woanders als im Deutschen.
    """
    if not text or not isinstance(text, str):
        # v4.1-W7: t() sitzt an 208 Sendestellen, und manche bekommen keinen
        # Text, sondern None oder ein Embed. Ein TypeError dort waere eine
        # Antwort, die gar nicht erst rausgeht — der Uebersetzer darf nie
        # gefaehrlicher sein als das, was er uebersetzt.
        return text
    # Ohne ausdrueckliche Angabe gilt die Sprache dieser Anfrage — so muss sie
    # nicht durch 208 Sendestellen gereicht werden.
    if sprache is None:
        sprache = aktuelle_sprache()
    aus = katalog(sprache).get(text, text)
    if kw:
        try:
            aus = aus.format(**kw)
        except (KeyError, IndexError, ValueError):
            # Ein Katalogeintrag mit falschem Platzhalter darf keine Route
            # sprengen — lieber der deutsche Satz als ein 500er.
            try:
                aus = text.format(**kw)
            except Exception:
                aus = text
    return aus


_QUALITAET = re.compile(r"^\s*([A-Za-z-]{2,8})(?:\s*;\s*q\s*=\s*([0-9.]+))?\s*$")


def aus_accept_language(kopfzeile):
    """Die beste unterstuetzte Sprache aus einem Accept-Language-Header.

    Gibt None zurueck, wenn nichts passt — dann entscheidet der Aufrufer, und
    das ist richtig so: der Header ist ein Wunsch, keine Einstellung.
    """
    if not kopfzeile:
        return None
    kandidaten = []
    for teil in str(kopfzeile).split(","):
        m = _QUALITAET.match(teil)
        if not m:
            continue
        tag = m.group(1).lower()
        try:
            q = float(m.group(2)) if m.group(2) else 1.0
        except ValueError:
            q = 1.0
        kandidaten.append((q, tag))
    for _q, tag in sorted(kandidaten, key=lambda x: -x[0]):
        if tag in SPRACHEN:
            return tag
        kurz = tag.split("-")[0]
        if kurz in SPRACHEN:
            return kurz
    return None


def normalisieren(sprache):
    """Beliebige Eingabe auf eine unterstuetzte Sprache bringen, sonst None.

    Nimmt auch 'de-DE' oder 'EN' — genau die Formen, die aus Browsern und aus
    Telegrams language_code kommen.
    """
    if not sprache:
        return None
    s = str(sprache).strip().lower().replace("_", "-")
    if s in SPRACHEN:
        return s
    kurz = s.split("-")[0]
    return kurz if kurz in SPRACHEN else None


def standard():
    """Die eingestellte Standardsprache. Als Funktion, nicht als Konstante:
       .env wird teils erst nach den ersten Importen geladen."""
    return _standard
