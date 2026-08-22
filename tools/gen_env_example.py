#!/usr/bin/env python3
"""v4.0-W100: erzeugt .env.example aus dem Code — vollständig & immer aktuell.

Warum generiert statt handgepflegt: der Bot liest ~470 Umgebungsvariablen. Eine
handgeschriebene Vorlage veraltet sofort und übersieht Variablen — genau die
Lücke, an der leere .env-Zeilen den Brain gekillt haben (W81/W82). Dieses Skript
scannt bot_v37.py, brain/, brain_bridge.py und nc/ nach env-Zugriffen, zieht Name
+ Default und schreibt sie gruppiert heraus. Erneut ausführbar:

    python tools/gen_env_example.py        # schreibt .env.example
    python tools/gen_env_example.py --check # nur prüfen, ob aktuell (Exit 1 wenn nicht)
"""
import glob
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, ".env.example")

# env_int/env_float/env_int_range/clamp_*("NAME", default …) → numerischer Default
_NUM = re.compile(r'env_(?:int|float)(?:_range)?\(\s*["\']([A-Z][A-Z0-9_]+)["\']\s*,\s*([0-9.]+)')
# os.getenv("NAME"[, "default"]) → String-Default (oder leer)
_STR = re.compile(r'os\.getenv\(\s*["\']([A-Z][A-Z0-9_]+)["\']\s*(?:,\s*["\']((?:[^"\'\\]|\\.)*)["\'])?')

# Namen, die Geheimnisse/Zugangsdaten sind → NIE mit Wert vorbelegen
_SECRET = re.compile(r'(TOKEN|KEY|SECRET|PASSWORD|_PIN|WEBHOOK|CLIENT_SECRET|ACCESS)')
# ohne die kann der Bot nicht sinnvoll starten
_REQUIRED = {"BOT_TOKEN", "TELEGRAM_TOKEN", "TELEGRAM_CHAT_ID"}


def collect():
    files = ["bot_v37.py", "brain_bridge.py"] + \
        sorted(glob.glob(os.path.join(ROOT, "brain", "*.py"))) + \
        sorted(glob.glob(os.path.join(ROOT, "nc", "*.py")))
    seen = {}
    for f in files:
        p = f if os.path.isabs(f) else os.path.join(ROOT, f)
        try:
            txt = open(p, encoding="utf-8").read()
        except OSError:
            continue
        for line in txt.splitlines():
            s = line.split("#", 1)[0]
            for m in _NUM.finditer(s):
                seen.setdefault(m.group(1), m.group(2))
            for m in _STR.finditer(s):
                seen.setdefault(m.group(1), (m.group(2) or ""))
    return seen


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
    for pre in sorted(groups):
        out.append("# ── %s ─────────────────────────────────────────────" % pre)
        for name in groups[pre]:
            val = seen[name]
            secret = bool(_SECRET.search(name))
            req = name in _REQUIRED
            tag = ""
            if req:
                tag = "   # [PFLICHT] setzen"
            elif secret:
                tag = "   # (Geheimnis — hier eintragen)"
            if secret or req:
                out.append("%s=%s" % (name, tag))
            else:
                # Default informativ, auskommentiert (Bot nutzt ohnehin den Default)
                shown = str(val).replace("\n", " ")
                out.append("# %s=%s" % (name, shown))
        out.append("")
    return "\n".join(out).rstrip() + "\n"


def main():
    seen = collect()
    content = render(seen)
    if "--check" in sys.argv:
        cur = open(OUT, encoding="utf-8").read() if os.path.exists(OUT) else ""
        if cur != content:
            print("VERALTET — bitte `python tools/gen_env_example.py` ausführen. "
                  "(%d Variablen erkannt)" % len(seen))
            sys.exit(1)
        print(".env.example aktuell (%d Variablen)" % len(seen))
        return
    open(OUT, "w", encoding="utf-8").write(content)
    print("geschrieben: .env.example  (%d Variablen, %d Gruppen)" %
          (len(seen), len({n.split('_', 1)[0] for n in seen})))


if __name__ == "__main__":
    main()
