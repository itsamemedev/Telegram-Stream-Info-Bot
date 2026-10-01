#!/usr/bin/env python3
"""v4.0-W100: erzeugt .env.example aus dem Code — vollständig & immer aktuell.

Warum generiert statt handgepflegt: der Bot liest ~470 Umgebungsvariablen. Eine
handgeschriebene Vorlage veraltet sofort und übersieht Variablen — genau die
Lücke, an der leere .env-Zeilen den Brain gekillt haben (W81/W82). Dieses Skript
scannt bot.py, brain/, brain_bridge.py und nc/ nach env-Zugriffen, zieht Name
+ Default und schreibt sie gruppiert heraus. Erneut ausführbar:

    python tools/gen_env_example.py        # schreibt .env.example
    python tools/gen_env_example.py --check # nur prüfen, ob aktuell (Exit 1 wenn nicht)
"""
import ast
import glob
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, ".env.example")

# env_int/env_float/env_int_range/clamp_*("NAME", default …) → numerischer Default
_NUM = re.compile(r'env_(?:int|float)(?:_range)?\(\s*["\']([A-Z][A-Z0-9_]+)["\']\s*,\s*([0-9.]+)')
# v4.2-W54: dieselbe Form, aber mit BERECHNETER Vorgabe statt einer Zahl —
# z.B. _env_int("RESTREAM_CHAT_WIDTH", _nc_ff.chat_umbruch_w(...)). _NUM
# verlangt eine Ziffer und liess solche Variablen lautlos aus der Vorlage
# fallen; genau so verschwanden RESTREAM_CHAT_LINES und RESTREAM_CHAT_WIDTH,
# als ihre Vorgabe aus der Panel-Geometrie kam. Eine Variable, die es gibt,
# gehoert in die Vorlage — auch wenn ihre Vorgabe erst zur Laufzeit feststeht.
_BERECHNET = re.compile(
    r'env_(?:int|float)(?:_range)?\(\s*["\']([A-Z][A-Z0-9_]+)["\']\s*,\s*(?![0-9.\'"])')
# os.getenv("NAME"[, "default"]) → String-Default (oder leer)
_STR = re.compile(r'os\.getenv\(\s*["\']([A-Z][A-Z0-9_]+)["\']\s*(?:,\s*["\']((?:[^"\'\\]|\\.)*)["\'])?')

# Namen, die Geheimnisse/Zugangsdaten sind → NIE mit Wert vorbelegen
_SECRET = re.compile(r'(TOKEN|KEY|SECRET|PASSWORD|_PIN|WEBHOOK|CLIENT_SECRET|ACCESS)')
# ohne die kann der Bot nicht sinnvoll starten
_REQUIRED = {"BOT_TOKEN", "TELEGRAM_TOKEN", "TELEGRAM_CHAT_ID"}


def _ohne_kommentar(zeile: str) -> str:
    """Kommentar abschneiden, aber nur ein '#' AUSSERHALB von Anfuehrungszeichen.

    Vorher: zeile.split("#", 1)[0]. Damit haette ein Default, der selbst ein
    '#' enthaelt — eine Farbe wie os.getenv("UI_ACCENT", "#e8c86a") — die Zeile
    mittendrin zerschnitten, das Muster nicht mehr gepasst und die Variable
    waere lautlos aus .env.example gefallen. Genau die Luecke, gegen die dieses
    Skript ueberhaupt geschrieben wurde. Heute trifft es keine Lesestelle
    (nachgezaehlt: null) — es ist eine Falle fuer die naechste.
    """
    quote = ""
    for i, c in enumerate(zeile):
        if quote:
            if c == "\\":
                continue
            if c == quote:
                quote = ""
        elif c in "\"'":
            quote = c
        elif c == "#":
            return zeile[:i]
    return zeile


# ══════════════════════════════════════════════════════════════════════
# v4.2-W99: env-Namen, die NICHT woertlich im Aufruf stehen
# ══════════════════════════════════════════════════════════════════════
# Die drei Muster oben verlangen einen String IM Aufruf. Wer die Namen aus
# einer Liste liest, ist damit unsichtbar:
#
#     for coin, label, env in _COINS:          # nc/crypto.py
#         a = os.getenv(env, "")
#
# Gemessen am 30.09.: acht Variablen fehlten so in der Vorlage, darunter
# ALLE SECHS Krypto-Spendenadressen (DONATION_<COIN>_ADDRESS). Der Betreiber
# baute seine .env aus dieser Vorlage neu und verlor damit saemtliche
# Wallet-Adressen — die oeffentliche Seite versteckte den Block danach still.
#
# Es ist der dritte Fall derselben Klasse: `_BERECHNET` kam, weil eine
# gerechnete Vorgabe die Variable fallen liess, `_ohne_kommentar`, weil ein
# '#' im Default die Zeile zerschnitt. Diesmal wird deshalb nicht nur der
# Fall behoben, sondern die KLASSE gesperrt — `dynamische_luecken()` findet
# jede Lesestelle, die keiner der Wege erreicht, und `--check` faellt darauf.
#
# Eine Lesestelle, die den Namen als PARAMETER bekommt, ist keine Luecke:
# dort steht das Literal beim Aufrufer und die Muster oben sehen es
# (nc/envnum, nc/cfgnorm, nc/dashauth und die Routen-Helfer, 15 Stellen).

# Praefix-Familien: der Name entsteht erst zur Laufzeit
# (BRAIN_ACT_<REGEL>, BRAIN_AGENT_<NAME>). Die lassen sich nicht aufzaehlen,
# nur dokumentieren — beide stehen als Muster in der Vorlage. Der Eintrag
# hier ist die bewusste Ausnahme, nicht ein vergessener Fall.
# (datei, praefix) -> (Platzhalter, Vorgabe, Begruendung). Aus DIESEM Dict
# schreibt render() auch den Muster-Abschnitt der Vorlage: Ausnahme und
# Dokumentation sind damit dieselbe Tatsache und koennen nicht auseinander
# laufen. Beim ersten Anlauf von W99 taten sie genau das — BRAIN_ACT_ war
# (durch zwei konkrete Regeln) sichtbar, BRAIN_AGENT_ gar nicht, und der
# Betreiber konnte von den Agent-Schaltern nichts wissen.
DYNAMISCH_ERLAUBT = {
    ("brain_bridge.py", "BRAIN_ACT_"): (
        "<REGEL>", "0",
        "Aktions-Gate je Brain-Regel. Default AUS — Autonomie wird pro Regel "
        "verdient, nachdem das Entscheidungslog sie bestaetigt hat."),
    ("brain/agents.py", "BRAIN_AGENT_"): (
        "<AGENT>", "1",
        "Ein Sentinel-Agent einzeln abschalten. Der Wert in der Tabelle "
        "agent_config schlaegt diese Variable."),
}

_ENVNAME = re.compile(r"^[A-Z][A-Z0-9_]{2,}$")

# Gesammelt waehrend collect(); von main() geprueft.
LUECKEN = []


def _parameter_namen(fn):
    a = fn.args
    raus = {x.arg for gruppe in (a.posonlyargs, a.args, a.kwonlyargs)
            for x in gruppe}
    if a.vararg:
        raus.add(a.vararg.arg)
    if a.kwarg:
        raus.add(a.kwarg.arg)
    return raus


def _texte_aus(knoten):
    """Alle env-taugliche Zeichenketten in einem Literal-Baum. Auch aus
       Tupeln in Listen — `_COINS` traegt (coin, label, ENV) je Zeile."""
    raus = []
    for n in ast.walk(knoten):
        if isinstance(n, ast.Constant) and isinstance(n.value, str) \
                and _ENVNAME.match(n.value):
            raus.append(n.value)
    return raus


def _modulweite_literale(baum):
    """name -> Literal-Knoten fuer Zuweisungen auf Modul-Ebene."""
    raus = {}
    for st in baum.body:
        if isinstance(st, ast.Assign) and isinstance(st.value, (ast.Tuple, ast.List, ast.Set)):
            for ziel in st.targets:
                if isinstance(ziel, ast.Name):
                    raus[ziel.id] = st.value
    return raus


def _schleifen_quelle(knoten, name, literale):
    """Woraus laeuft `name` in dieser Schleife/Comprehension? -> Literal oder None."""
    if isinstance(knoten, (ast.For, ast.AsyncFor)):
        ziele = [knoten.target]
        quelle = knoten.iter
    elif isinstance(knoten, ast.comprehension):
        ziele = [knoten.target]
        quelle = knoten.iter
    else:
        return None
    gebunden = set()
    for z in ziele:
        gebunden |= {n.id for n in ast.walk(z) if isinstance(n, ast.Name)}
    if name not in gebunden:
        return None
    if isinstance(quelle, (ast.Tuple, ast.List, ast.Set)):
        return quelle
    if isinstance(quelle, ast.Name):
        return literale.get(quelle.id)
    return None


def dynamische_namen(pfad, quelltext):
    """(namen, luecken) fuer eine Datei.

    `namen` sind env-Namen, die nur ueber eine Liste erreichbar sind —
    aufgeloest aus der Schleife, ueber die die Lesestelle laeuft.
    `luecken` sind Lesestellen, die weder Parameter noch aufloesbar sind:
    sie muessen in DYNAMISCH_ERLAUBT stehen, sonst faellt die Sperre.
    """
    try:
        baum = ast.parse(quelltext)
    except SyntaxError:
        return set(), []
    for n in ast.walk(baum):
        for k in ast.iter_child_nodes(n):
            k._eltern = n
    literale = _modulweite_literale(baum)
    namen, luecken = set(), []
    for n in ast.walk(baum):
        if not isinstance(n, ast.Call) or not n.args:
            continue
        f = n.func
        if not (isinstance(f, ast.Attribute) and f.attr == "getenv"):
            continue
        erst = n.args[0]
        if isinstance(erst, ast.Constant):
            continue                        # woertlich — die Muster oben sehen es

        # (1) Praefix-Familie: f"BRAIN_ACT_{...}"
        if isinstance(erst, ast.JoinedStr):
            teile = [t.value for t in erst.values
                     if isinstance(t, ast.Constant) and isinstance(t.value, str)]
            praefix = teile[0] if teile else ""
            if (pfad, praefix) in DYNAMISCH_ERLAUBT:
                continue
            luecken.append((n.lineno, "f-String %r" % praefix))
            continue

        if not isinstance(erst, ast.Name):
            luecken.append((n.lineno, type(erst).__name__))
            continue

        # (2) Parameter: das Literal steht beim Aufrufer
        o, fn = n, None
        while hasattr(o, "_eltern"):
            o = o._eltern
            if isinstance(o, (ast.FunctionDef, ast.AsyncFunctionDef)):
                fn = o
                break
        if fn is not None and erst.id in _parameter_namen(fn):
            continue

        # (3) Schleifenvariable: die Liste aufloesen
        o, gefunden = n, None
        while hasattr(o, "_eltern"):
            o = o._eltern
            gefunden = _schleifen_quelle(o, erst.id, literale)
            if gefunden is not None:
                break
            for kind in ast.iter_child_nodes(o):
                if isinstance(kind, ast.comprehension):
                    gefunden = _schleifen_quelle(kind, erst.id, literale)
                    if gefunden is not None:
                        break
            if gefunden is not None:
                break
        if gefunden is not None:
            namen |= set(_texte_aus(gefunden))
            continue

        luecken.append((n.lineno, "Name %r nicht aufloesbar" % erst.id))
    return namen, luecken


def collect():
    files = ["bot.py", "brain_bridge.py"] + \
        sorted(glob.glob(os.path.join(ROOT, "brain", "*.py"))) + \
        sorted(glob.glob(os.path.join(ROOT, "nc", "*.py"))) + \
        sorted(glob.glob(os.path.join(ROOT, "nc", "routes", "*.py")))
    # v4.0-W117: nc/routes/ gehoert dazu. Ohne das verschwindet jede Variable
    # aus der Beispieldatei, sobald ihre einzige Lesestelle in ein Blueprint
    # wandert (zuerst passiert bei DASHBOARD_TRACK_GROUP_ID) — der Betreiber
    # haette einen Schalter verloren, den es weiterhin gibt.
    seen = {}
    for f in files:
        p = f if os.path.isabs(f) else os.path.join(ROOT, f)
        try:
            with open(p, encoding="utf-8") as _fh:
                txt = _fh.read()
        except OSError:
            continue
        # v4.1-W22: die kommentarfreien Zeilen wieder ZUSAMMENSETZEN und erst
        # dann suchen. Vorher lief die Suche je Zeile — ein umbrochener Aufruf
        #
        #     os.getenv(
        #         "TWITCH_INGEST_URL",
        #         "rtmp://ingest.global-contribute...").strip()
        #
        # passte auf keine einzelne Zeile und fiel still aus der Vorlage. Genau
        # die Luecke, gegen die dieses Skript geschrieben wurde; sie kostete
        # beim ersten Anlauf von W22 prompt eine Variable. Kommentare werden
        # weiterhin ZEILENWEISE entfernt — sonst verschluckte ein '#' in einem
        # Default den Rest der Datei.
        ohne = "\n".join(_ohne_kommentar(z) for z in txt.splitlines())
        for m in _NUM.finditer(ohne):
            seen.setdefault(m.group(1), m.group(2))
        for m in _BERECHNET.finditer(ohne):
            # Leerer Wert: der Default steht nicht als Zahl im Quelltext,
            # sondern wird gerechnet. Leer ist hier korrekt und sicher — die
            # Zeile ist ohnehin auskommentiert, und ein leerer Wert laesst
            # laut Kopf der Vorlage den Default greifen.
            seen.setdefault(m.group(1), "")
        for m in _STR.finditer(ohne):
            seen.setdefault(m.group(1), (m.group(2) or ""))
        # v4.2-W99: die Namen, die nur ueber eine Liste erreichbar sind.
        # Gegen den ROHEN Text geparst, nicht gegen `ohne` — das Entfernen
        # der Kommentare erhaelt die Zeilennummern nicht zwingend, und die
        # Sperre nennt eine Zeile.
        rel = os.path.relpath(p, ROOT).replace(os.sep, "/")
        namen, luecken = dynamische_namen(rel, txt)
        for name in namen:
            seen.setdefault(name, "")
        for zeile, was in luecken:
            LUECKEN.append((rel, zeile, was))
    return seen


def _umbruch(text, breite):
    """Kommentar auf `breite` Zeichen umbrechen — eine Vorlage, die man in
       einem 80-Spalten-Terminal liest, soll dort auch lesbar sein."""
    worte, zeilen, jetzt = text.split(), [], ""
    for w in worte:
        if jetzt and len(jetzt) + 1 + len(w) > breite:
            zeilen.append(jetzt)
            jetzt = "# " + w
        else:
            jetzt = (jetzt + " " + w) if jetzt else w
    if jetzt:
        zeilen.append(jetzt)
    return zeilen


def render(seen):
    from collections import defaultdict
    groups = defaultdict(list)
    for name in sorted(seen):
        groups[name.split("_", 1)[0]].append(name)

    out = []
    out.append("# ==========================================================================")
    out.append("# NIGHTCRAWLER v37 · .env.example  —  AUTO-GENERIERT")
    out.append("# Erzeugt von tools/gen_env_example.py aus dem Quellcode.")
    out.append("# NICHT von Hand pflegen — neu generieren: python tools/gen_env_example.py")
    out.append("#")
    out.append("# Kopiere nach .env und passe an. Zeilen sind AUSKOMMENTIERT = Default aktiv.")
    out.append("# Leere Werte (NAME=) sind seit W81/W82 sicher — der Default greift, kein Crash.")
    out.append("# Mit [PFLICHT] markierte Variablen musst du setzen.")
    out.append("# ==========================================================================")
    out.append("")
    # v4.2-W99: die Praefix-Familien. Ihre Namen entstehen erst zur Laufzeit,
    # aufzaehlen laesst sich das nicht — verschweigen aber auch nicht: der
    # Betreiber wuesste sonst nicht, dass es diese Schalter gibt.
    if DYNAMISCH_ERLAUBT:
        out.append("# ── MUSTER (Name entsteht zur Laufzeit) ───────────")
        for (_datei, praefix), (platz, vorgabe, grund) in sorted(
                DYNAMISCH_ERLAUBT.items(), key=lambda kv: kv[0][1]):
            for zeile in _umbruch("# " + grund, 74):
                out.append(zeile)
            out.append("# %s%s=%s" % (praefix, platz, vorgabe))
            out.append("")
    for pre in sorted(groups):
        out.append("# ── %s ─────────────────────────────────────────────" % pre)
        for name in groups[pre]:
            val = seen[name]
            secret = bool(_SECRET.search(name))
            req = name in _REQUIRED
            if secret or req:
                # Der Hinweis gehoert in eine EIGENE Zeile. "NAME=   # Hinweis"
                # sieht wie ein Kommentar aus, ist aber keiner: python-dotenv
                # liest bei einem unquotierten Wert den Rest der Zeile als WERT.
                # Aus `cp .env.example .env` wurden so rund 40 Variablen mit dem
                # Inhalt "# (Geheimnis — hier eintragen)" — der Bot hielt damit
                # Discord, Twitch, YouTube und Anthropic fuer konfiguriert und
                # meldete "Token abgelehnt" statt "kein Token".
                out.append("# [PFLICHT] setzen" if req else "# (Geheimnis — hier eintragen)")
                out.append("%s=" % name)
            else:
                # Default informativ, auskommentiert (Bot nutzt ohnehin den Default)
                shown = str(val).replace("\n", " ")
                out.append("# %s=%s" % (name, shown))
        out.append("")
    return "\n".join(out).rstrip() + "\n"


def main():
    seen = collect()
    # v4.2-W99: eine Lesestelle, die kein Weg erreicht, bricht ab — statt
    # eine Variable lautlos aus der Vorlage fallen zu lassen. Das ist der
    # Unterschied zu den beiden Vorgaengern derselben Klasse: dort wurde je
    # der Einzelfall behoben, hier wird gemeldet, wenn ein neuer entsteht.
    if LUECKEN:
        print("env-LUECKE — diese Lesestellen erreicht kein Muster, die "
              "Variablen fehlen damit in der Vorlage:")
        for pfad, zeile, was in LUECKEN:
            print("  %s:%d  %s" % (pfad, zeile, was))
        print()
        print("  Abhilfe: entweder den Namen woertlich in den Aufruf schreiben,")
        print("  oder die Liste so, dass dynamische_namen() sie aufloest (ein")
        print("  Tupel/eine Liste auf Modul-Ebene), oder — wenn der Name erst")
        print("  zur Laufzeit entsteht — als Praefix-Familie in")
        print("  DYNAMISCH_ERLAUBT eintragen UND als Muster in die Vorlage.")
        sys.exit(2)
    content = render(seen)
    if "--check" in sys.argv:
        if os.path.exists(OUT):
            with open(OUT, encoding="utf-8") as _fh:
                cur = _fh.read()
        else:
            cur = ""
        if cur != content:
            print("VERALTET — bitte `python tools/gen_env_example.py` ausführen. "
                  "(%d Variablen erkannt)" % len(seen))
            sys.exit(1)
        print(".env.example aktuell (%d Variablen)" % len(seen))
        return
    with open(OUT, "w", encoding="utf-8") as _fh:
        _fh.write(content)
    print("geschrieben: .env.example  (%d Variablen, %d Gruppen)" %
          (len(seen), len({n.split('_', 1)[0] for n in seen})))


if __name__ == "__main__":
    main()
