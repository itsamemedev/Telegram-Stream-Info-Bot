"""nc.badwords — v4.1-W18: Bannwortliste und Lern-Warteschlange als Datei.

════════════════════════════════════════════════════════════════════════
WARUM DIESES MODUL
════════════════════════════════════════════════════════════════════════
Die neun Routen unter `/api/kickmod` sind zur Haelfte Dateiarbeit: Liste
lesen, Liste schreiben, Basisliste holen, gelernte Kandidaten annehmen oder
verwerfen. Genau diese Haelfte haette als Blueprint fuenf Eintraege in
nc/ctx.py gekostet — bei 24 von 25 belegten Plaetzen ist das der ganze Rest.

Dieselbe Reihenfolge wie in W117: erst die Datenschicht aufloesen, dann sind
die Routen umsonst. Hier steht deshalb alles, was mit den beiden JSON-Dateien
unter RECORDINGS_DIR zu tun hat — ohne Flask, ohne Bot, ohne Netzzwang.

Zwei Dinge, die absichtlich so sind:

* **Geschrieben wird ueber eine Zwischendatei und `os.replace`.** Ein Absturz
  mitten im Schreiben darf die Bannwortliste nicht halbieren: danach
  moderiert der Bot still schwaecher, und niemand sieht es.
* **Gelernte Woerter werden NIE automatisch gebannt.** Was die KI als toxisch
  flaggt, ist ein Kandidat. Eine Fehleinschaetzung des Modells wuerde sonst
  Unschuldige sperren — die Uebernahme ist eine bewusste Handlung im
  Dashboard.

Der Ablageort kommt per `configure(...)`, nicht als Modul-Konstante: `.env`
ist beim Import teils noch nicht geladen (CLAUDE.md, "Modul-Konstanten
frieren .env ein").
"""

import json
import os

# LDNOOBW ist eine freie Basisliste. Substring-Treffer sind fuer Deutsch
# gewollt (faengt Komposita: "arsch" -> "Arschloch"). Sie ueber-filtert
# teils — deshalb ist sie im Dashboard reviewbar und die Ollama-Moderation
# deckt Kontext und Verschleierung zusaetzlich ab.
LDNOOBW_DE_URL = ("https://raw.githubusercontent.com/LDNOOBW/"
                  "List-of-Dirty-Naughty-Obscene-and-Otherwise-Bad-Words/master/de")
CAP = 300

FALLBACK_DE = [
    "analritter", "arsch", "arschficker", "arschlecker", "arschloch", "bimbo", "bratze",
    "bumsen", "bonze", "dödel", "fick", "ficken", "flittchen", "fotze", "fratze",
    "hackfresse", "hure", "hurensohn", "ische", "kackbratze", "kacke", "kacken",
    "kackwurst", "kampflesbe", "kanake", "kimme", "lümmel", "milf", "möpse",
    "morgenlatte", "möse", "mufti", "muschi", "nackt", "neger", "nigger", "nippel",
    "nutte", "onanieren", "orgasmus", "penis", "pimmel", "pimpern", "pinkeln", "pissen",
    "pisser", "popel", "poppen", "porno", "reudig", "rosette", "schabracke", "schlampe",
    "scheiße", "scheisser", "schiesser", "schnackeln", "schwanzlutscher", "schwuchtel",
    "tittchen", "titten", "vögeln", "vollpfosten", "wichse", "wichsen", "wichser",
]

_CONF = {"recordings_dir": "."}


def configure(*, recordings_dir):
    """Ablageort setzen. Der Bot ruft das beim Start, die Tests direkt."""
    _CONF["recordings_dir"] = str(recordings_dir or ".")


def banned_path() -> str:
    return os.path.join(_CONF["recordings_dir"], "banned_words.json")


def learned_path() -> str:
    return os.path.join(_CONF["recordings_dir"], "learned_badwords.json")


def _lade(pfad, kappen=False):
    try:
        with open(pfad, "r", encoding="utf-8") as f:
            d = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError, OSError, ValueError):
        return []
    if not isinstance(d, list):
        return []
    if not kappen:
        return d
    return [str(w)[:40] for w in d if str(w).strip()][:CAP]


def _schreibe(pfad, daten):
    """Atomar: erst daneben, dann ueber. Ein Abbruch mitten im Schreiben
       darf keine halbe Bannwortliste hinterlassen."""
    try:
        os.makedirs(_CONF["recordings_dir"], exist_ok=True)
        tmp = pfad + ".tmp"
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(list(daten), f, ensure_ascii=False)
        os.replace(tmp, pfad)
        return True
    except OSError:
        return False


def load_banned():
    return _lade(banned_path(), kappen=True)


def save_banned(words):
    return _schreibe(banned_path(), words)


def load_learned():
    return _lade(learned_path())


def save_learned(items):
    return _schreibe(learned_path(), items)


def fetch_ldnoobw_de(opener=None):
    """Die deutsche Basisliste holen. -> (woerter, quelle).

    `opener` ist nur fuer die Tests da: ohne Einspeisung wird wirklich
    geladen, und ein Netzfehler landet im eingebauten Fallback. Ein leeres
    Ergebnis zaehlt als Fehlschlag — eine geleerte Liste waere ein still
    entwaffneter Moderator.
    """
    try:
        if opener is None:
            import urllib.request

            req = urllib.request.Request(
                LDNOOBW_DE_URL, headers={"User-Agent": "nightcrawler-bot/1.0"})
            with urllib.request.urlopen(req, timeout=12) as r:
                roh = r.read().decode("utf-8", "replace")
        else:
            roh = opener(LDNOOBW_DE_URL)
        words = [ln.strip() for ln in roh.splitlines()
                 if ln.strip() and not ln.lstrip().startswith("#")]
        if words:
            return words, "online"
    except Exception:
        pass
    return list(FALLBACK_DE), "fallback"
