"""nc.shield — SENTINEL-SHIELD: deterministische Anti-Doxxing/Anti-Hate-Schicht.

Extrahiert aus bot_v37.py (V37-W-SHIELD). Reine Regex-Logik, greift VOR jeder
KI-Klassifikation auf Kick UND Discord, kostet 0 KI-Budget. Erkennt Leetspeak/
Punkt-Tarnung. bot_v37.py importiert _sentinel_screen/_shield_normalize zurück.
"""

import os
import re
import unicodedata

# SENTINEL-SHIELD: deterministische Anti-Doxxing/Anti-Hate-Schicht VOR jeder
# KI-Klassifikation — greift auf Kick UND Discord, kostet 0 KI-Budget und
# funktioniert auch, wenn das LLM down ist. Erkennt Leetspeak/Punkt-Tarnung.
_SHIELD_LEET = str.maketrans({"0": "o", "1": "i", "3": "e", "4": "a", "5": "s",
                              "7": "t", "@": "a", "$": "s", "!": "i", "+": "t"})

# V37-SHIELD-HARDEN: Homoglyphen — Zeichen, die lateinisch AUSSEHEN, aber aus
# anderen Alphabeten stammen (kyrillisch/griechisch). Umgehungstrick: "ѕсhеiѕе"
# sieht aus wie "scheise", ist aber unsichtbar anders. Auf Latein zurueckbilden.
_SHIELD_HOMOGLYPH = str.maketrans({
    # kyrillisch → lateinisch
    "\u0430": "a", "\u0435": "e", "\u043e": "o", "\u0440": "p", "\u0441": "c",
    "\u0443": "y", "\u0445": "x", "\u0456": "i", "\u0458": "j", "\u04bb": "h",
    "\u0455": "s", "\u0405": "s", "\u0491": "g",
    "\u0410": "a", "\u0415": "e", "\u041e": "o", "\u0420": "p", "\u0421": "c",
    "\u0422": "t", "\u0423": "y", "\u0425": "x", "\u041c": "m", "\u041d": "h",
    "\u041a": "k", "\u0412": "b",
    # griechisch → lateinisch
    "\u03b1": "a", "\u03bf": "o", "\u03c1": "p", "\u03c5": "u", "\u03bd": "v",
    "\u0391": "a", "\u0392": "b", "\u0395": "e", "\u0396": "z", "\u0397": "h",
    "\u0399": "i", "\u039a": "k", "\u039c": "m", "\u039d": "n", "\u039f": "o",
    "\u03a1": "p", "\u03a4": "t", "\u03a5": "y", "\u03a7": "x",
    # sonstige haeufige Lookalikes
    "\u0131": "i", "\u0261": "g",
})

# Zero-Width- und unsichtbare Trennzeichen, die zwischen Buchstaben gestreut
# werden ("s\u200bcheiße"), plus diverse Whitespace-Varianten.
_SHIELD_INVISIBLE = re.compile(
    r"[\u200b\u200c\u200d\u2060\ufeff\u00ad\u180e\u2000-\u200a\u202f\u205f\u3000]")


def _shield_normalize(t):
    t = (t or "").lower()
    # 1. Unicode-Kanonik: kombinierte Akzente zerlegen und Diakritika droppen
    #    (héllö → hello), faengt Akzent-Tarnung ab.
    t = unicodedata.normalize("NFKD", t)
    t = "".join(c for c in t if not unicodedata.combining(c))
    # 2. Homoglyphen auf Latein, dann Leetspeak
    t = t.translate(_SHIELD_HOMOGLYPH).translate(_SHIELD_LEET)
    # 3. unsichtbare Zeichen raus (die zwischen Buchstaben versteckt werden)
    t = _SHIELD_INVISIBLE.sub("", t)
    # 4a. Zeichen-Tarnung mit Satzzeichen (f.i.c.k, s-c-h-e-i-ß-e): Trenner
    #     ZWISCHEN Buchstaben entfernen. Kein Leerzeichen hier — das wuerde
    #     echte Wortgrenzen zerstoeren (und ungewollt Wörter verschmelzen).
    for _ in range(2):
        t = re.sub(r"(?<=[a-zäöüß])[.\-_*~|/\\]+(?=[a-zäöüß])", "", t)
    # 4b. Leerzeichen-Tarnung NUR wenn viele Einzelbuchstaben vereinzelt stehen
    #     ("s c h e i ß e") — an Sequenzen von >=4 einzelnen Buchstaben erkennbar.
    #     So bleiben normale Saetze ("gut gemacht leute") unangetastet.
    def _despace(m):
        return m.group(0).replace(" ", "")
    t = re.sub(r"(?:[a-zäöüß] ){3,}[a-zäöüß]\b", _despace, t)
    # 5. Wiederholungen kappen: fickkkk → fickk
    t = re.sub(r"(.)\1{2,}", r"\1\1", t)
    return t

# Doxxing: private Daten Dritter im Chat. Bewusst DE-fokussiert.
_SHIELD_DOXX = [
    (re.compile(r"(?:\+49|0049|(?<!\d)0)[\s\-/]?1\d{2}[\s\-/]?\d{6,8}(?!\d)"), "Mobilnummer"),
    (re.compile(r"\bDE\s?(?:\d\s?){20}\b", re.I), "IBAN"),
    (re.compile(r"\b[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}\b", re.I), "E-Mail-Adresse"),
    (re.compile(r"\b[a-zäöüß]+(?:straße|strasse|str\.|weg|allee|gasse|ring|platz)\s*\d{1,4}\b.{0,40}?\b\d{5}\b", re.I | re.S), "Wohnadresse"),
    (re.compile(r"\b\d{5}\b\s+[A-ZÄÖÜ][a-zäöüß]+.{0,30}?(?:straße|strasse|str\.|weg|allee|gasse)", re.I), "Wohnadresse"),
    (re.compile(r"\b\d{1,2}\.\d{4,6},?\s*\d{1,2}\.\d{4,6}\b"), "Geo-Koordinaten"),
    (re.compile(r"(?:wohnt in|adresse ist|heißt in echt|heisst in echt|sein richtiger name|ihr richtiger name|klarname)", re.I), "Doxxing-Ansage"),
]
# Hate/Drohung: Volksverhetzung, Slurs (Kern — Rest via banned_words.json),
# Suizid-Aufforderung, Gewaltandrohung.
_SHIELD_HATE = [
    (re.compile(r"\b(?:heil hitler|sieg heil|hh88|untermensch(?:en)?|judensau|ins gas|vergas(?:en|t)|holocaust.{0,15}(?:geil|super|verdient))\b", re.I), "Volksverhetzung"),
    # 1488 nur als Code, nicht als Betrag/Menge (…1488 euro, preis 1488, 1488€)
    (re.compile(r"(?<!preis )(?<!kostet )(?<![\d,.])1488(?![\d,.])(?!\s*(?:€|euro|eur|dollar|usd|chf|k\b))", re.I), "Volksverhetzung"),
    (re.compile(r"\b(?:kys|kill\s*yourself|bring dich um|geh sterben|häng dich auf|haeng dich auf)\b", re.I), "Suizid-Aufforderung"),
    (re.compile(r"\b(?:ich (?:weiß|weiss) wo du wohnst|ich finde (?:dich|deine familie)|ich stech(?:e)? dich ab|ich bring(?:e)? dich um|ich schlag(?:e)? dich krankenhausreif)\b", re.I), "Drohung"),
]

def _sentinel_screen(text):
    """→ (kategorie, detail) bei Hard-Verstoß, sonst None. Kategorien:
    'DOXXING' | 'HATE' | 'DROHUNG'. Wird VOR Banned-Words/KI geprüft."""
    if os.getenv("SENTINEL_SHIELD", "1") not in ("1", "true"):
        return None
    raw = (text or "").strip()
    if len(raw) < 3:
        return None
    norm = _shield_normalize(raw)
    for rx, what in _SHIELD_DOXX:
        if rx.search(raw) or rx.search(norm):
            return ("DOXXING", what)
    for rx, what in _SHIELD_HATE:
        if rx.search(raw) or rx.search(norm):
            return ("HATE" if what == "Volksverhetzung" else "DROHUNG", what)
    return None
