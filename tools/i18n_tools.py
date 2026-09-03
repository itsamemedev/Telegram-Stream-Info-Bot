#!/usr/bin/env python3
"""i18n_tools — Abdeckung des Shell-Katalogs pruefen (v4.1-W17).

Das Gegenstueck zu tools/i18n_extract.py, nur fuer die SHELL-Werkzeuge. Es
sammelt die Texte, die durch die uebersetzenden Senken von installer.sh und
motd.sh laufen, und vergleicht sie mit locales/tools.<lang>.tsv.

    python3 tools/i18n_tools.py --liste          was gefunden wurde
    python3 tools/i18n_tools.py --check en       Abdeckung melden

WARUM --check NICHT scheitert, wenn etwas fehlt: der deutsche Text ist der
Schluessel, eine fehlende Zeile bleibt deutsch. Das ist eine Luecke, kein
Fehler — anders als beim Bot-Katalog, wo ein VERWAISTER Eintrag auf einen
umbenannten String hindeutet. Verwaiste Eintraege sind hier deshalb der
harte Befund, fehlende nur eine Zahl.
"""

import io
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
QUELLEN = ("tools/installer.sh", "tools/motd.sh")

# Die Senken, die in v4.1-W17 durch t() laufen. Erfasst werden nur Literale
# OHNE Variablen: alles mit $ oder ` ist zur Laufzeit zusammengesetzt und
# taugt nicht als Katalogschluessel.
# Nicht am Zeilenanfang verankert: die Senken stehen oft hinter && oder ||
# ("... && gut "..." || warn "..."" ueber zwei Zeilen). Ein Anker auf ^ hat
# genau die uebersehen — und sie tauchten dann als "verwaist" auf, obwohl sie
# im Quelltext stehen.
_SENKEN = re.compile(
    r'(?:^|&&|\|\||;|\{)\s*(?:info|gut|warn|fehler|erklaere|merke)\s+"([^"\\$`]{4,})"', re.M)
_FRAGEN = re.compile(r'(?:frage_ja|frage_text)\s+\w*\s*"([^"\\$`]{4,})"')


def sammeln():
    raus = set()
    for rel in QUELLEN:
        pfad = os.path.join(ROOT, rel)
        if not os.path.exists(pfad):
            continue
        text = io.open(pfad, encoding="utf-8").read()
        raus |= set(_SENKEN.findall(text))
        raus |= set(_FRAGEN.findall(text))
    return raus


def katalog(sprache):
    pfad = os.path.join(ROOT, "locales", "tools.%s.tsv" % sprache)
    aus = {}
    if not os.path.exists(pfad):
        return aus
    for zeile in io.open(pfad, encoding="utf-8"):
        if not zeile.strip() or zeile.lstrip().startswith("#"):
            continue
        teile = zeile.rstrip("\n").split("\t")
        if len(teile) >= 2 and teile[0] and teile[1]:
            aus[teile[0]] = teile[1]
    return aus


def main():
    args = sys.argv[1:]
    gefunden = sammeln()
    if "--liste" in args:
        for s in sorted(gefunden):
            print(s)
        print("\n%d uebersetzbare Zeichenketten in %d Dateien"
              % (len(gefunden), len(QUELLEN)))
        return 0
    sprache = "en"
    if "--check" in args:
        i = args.index("--check")
        if i + 1 < len(args):
            sprache = args[i + 1]
    kat = katalog(sprache)
    fehlt = sorted(gefunden - set(kat))
    verwaist = sorted(set(kat) - gefunden)
    quote = (100.0 * (len(gefunden) - len(fehlt)) / len(gefunden)) if gefunden else 100.0
    print("gefunden: %d Zeichenketten in %d Shell-Werkzeugen"
          % (len(gefunden), len(QUELLEN)))
    print("Katalog %s: %d Eintraege | fehlend: %d | verwaist: %d | Abdeckung: %.0f%%"
          % (sprache, len(kat), len(fehlt), len(verwaist), quote))
    for v in verwaist[:20]:
        print("  verwaist: %s" % v[:100])
    if verwaist:
        # Ein Eintrag ohne Quelle heisst: der deutsche Text wurde geaendert und
        # der Katalog nicht nachgezogen. Ab jetzt bleibt diese Zeile fuer immer
        # deutsch, ohne dass es jemand merkt — DAS ist der Fehler.
        print("FEHLER: verwaiste Eintraege — deutscher Text geaendert?")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
