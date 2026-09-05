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
# v4.2-W8: der Windows-Installer. Er stand bis hierher nicht einmal in dieser
# Liste — der Prüfer meldete deshalb 100 % Abdeckung für ein Werkzeug, das er
# gar nicht ansah. Batch hat eine eigene Aufrufform (`call :senke "text"`) und
# braucht deshalb einen eigenen Ausdruck; dieselbe Datei tools.en.tsv trägt
# beide Installer.
QUELLEN_BAT = ("tools/install.bat",)

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

# v4.2-W14: motd.sh hat EIGENE Senken (sect/row/gauge) und umschliesst den Rest
# ausdruecklich mit t(). Die Senken von installer.sh gibt es dort nicht — und
# genau deshalb sammelte der Pruefer bisher NICHTS aus motd.sh und meldete
# trotzdem 100 % Abdeckung. Eine Zahl, die nur zaehlt, was sie ohnehin kennt.
_MOTD_SENKEN = re.compile(r'(?:^|\s)(?:sect|row|gauge)\s+"([^"\\$`]{2,})"', re.M)
# lage_setz traegt den Text der Gesamtampel. Er wird erst beim Zeichnen
# uebersetzt ($(t "$LAGE_TEXT")), muss aber hier eingesammelt werden —
# sonst fehlt genau die Zeile im Katalog, die als erste ins Auge faellt.
_LAGE = re.compile(r'(?:^|\s)lage_setz\s+(?:err|warn)\s+"([^"\\$`]{2,})"', re.M)
# Ausdrueckliche Umschliessung, in beiden Schreibweisen: t "…" und $(t "…").
_T_AUFRUF = re.compile(r'\$\(t\s+"([^"\\$`]{2,})"\)|(?:^|\s)t\s+"([^"\\$`]{2,})"', re.M)

# Die Senken von tools/install.bat. Erfasst wird das ERSTE Argument — ausser
# bei :wert_gut, wo der Wert vorne steht und der feste Text hinten.
# Kein %: was einen Wert traegt, kann kein Schluessel sein (der Wert steht erst
# zur Laufzeit fest). Genau dafuer gibt es die *_wert-Senken.
_BAT_SENKEN = re.compile(
    r'\bcall :(?:kopf|info|info_wert|gut|gut_wert|warn|fehler|fehler_wert|'
    r'erklaere|merken|merken_wert|zeile|zeile2|zeile_wert|zeile_wert2|'
    r'zeile2_wert|punkt|t)\s+"([^"%]{3,})"')
_BAT_WERT_GUT = re.compile(r'\bcall :wert_gut\s+"[^"]*"\s+"([^"%]{3,})"')
_BAT_FRAGEN = re.compile(
    r'\bcall :(?:frage_ja|frage_text|frage_geheimnis)\s+(?:[JN]\s+)?"([^"%]{3,})"')


def sammeln():
    raus = set()
    for rel in QUELLEN:
        pfad = os.path.join(ROOT, rel)
        if not os.path.exists(pfad):
            continue
        text = io.open(pfad, encoding="utf-8").read()
        raus |= set(_SENKEN.findall(text))
        raus |= set(_FRAGEN.findall(text))
        raus |= set(_MOTD_SENKEN.findall(text))
        raus |= set(_LAGE.findall(text))
        for a, b in _T_AUFRUF.findall(text):
            wert = a or b
            # "$LAGE_TEXT" ist eine Variable, kein Schluessel — ihre Werte
            # stehen an den lage_setz-Aufrufstellen und werden dort erfasst.
            if wert and not wert.startswith("$"):
                raus.add(wert)
    for rel in QUELLEN_BAT:
        pfad = os.path.join(ROOT, rel)
        if not os.path.exists(pfad):
            continue
        text = io.open(pfad, encoding="utf-8").read()
        raus |= set(_BAT_SENKEN.findall(text))
        raus |= set(_BAT_WERT_GUT.findall(text))
        raus |= set(_BAT_FRAGEN.findall(text))
    return raus


# Deutsche Marker — dieselbe Idee wie in tools/i18n_extract.py.
_DEUTSCH = re.compile(
    r"[ÄÖÜäöüß]|\b(?:der|die|das|den|dem|ein|eine|und|oder|nicht|kein|keine|"
    r"wird|wurde|werden|ist|sind|war|hat|haben|kann|koennen|muss|muessen|soll|"
    r"noch|schon|nur|auch|mehr|alle|jede|jeder|beim|vom|zum|zur|fuer|mit|ohne|"
    r"nach|vor|ueber|unter|seit|Fehler|Datei|Grund|Stand|Wert|Seite|gefunden|"
    r"laeuft|fehlt|fehlen|unbekannt|gestoppt|aktiv|inaktiv|"
    # v4.2-W14: Beschriftungen der MOTD, die keinen der Marker oben tragen.
    # Sie standen im englischen Lauf sichtbar deutsch da, waehrend der Melder
    # schwieg — ein Marker-Satz, den man nicht nachzieht, wird blind.
    r"Kerne|Netz|Platte|Werkzeuge|Aufnahmen|Erkennung|Sicherung|Vorschau)\b")
# Was wie deutscher Text aussieht und keiner ist.
_KEIN_TEXT = ("NIGHTCRAWLER", "CROWDSEC", "DASHBOARD")


def unumschlossen(rel):
    """Deutscher Ausgabetext, der an KEINER Senke haengt. -> [(zeile, text)]

    Das ist die ehrliche Haelfte der Abdeckung. Die Quote oben sagt nur, wie
    viel von dem uebersetzt ist, was der Sammler FINDET — sie kann 100 %
    melden, waehrend eine ganze Datei deutsch bleibt. Genau das war bis
    v4.2-W14 der Fall: motd.sh band lib/i18n.sh ein und rief t() nie auf.
    """
    pfad = os.path.join(ROOT, rel)
    if not os.path.exists(pfad):
        return []
    raus = []
    for nr, zeile in enumerate(io.open(pfad, encoding="utf-8"), 1):
        roh = zeile.strip()
        if roh.startswith("#") or not roh:
            continue
        # Was ist Ausgabe? Drei Merkmale, und alle drei sind noetig:
        #   * printf/echo — der offensichtliche Fall;
        #   * lage_setz — die Gesamtampel, die ihren Text erst spaeter zeichnet;
        #   * ein FARBCODE im Literal. Eine Zeichenkette mit ${FNT} darin ist
        #     per Bauart Anzeige, egal ob sie in eine Variable geht.
        # Die ersten beiden allein reichten nicht: `EQ="  ${FNT}Kerne  ${R}"`
        # hat kein printf, und der englische Lauf zeigte prompt "Kerne".
        _farbe = re.search(r'"\s*[^"]*\$\{(?:FNT|TXT|WRN|ERR|OK|DIM|BR|B)\}', roh)
        if not (re.search(r"\b(?:printf|echo|lage_setz)\b", roh) or _farbe):
            continue
        # Umschliessungen ZUERST herausschneiden. Sonst zieht der Melder die
        # innere Zeichenkette aus $(t "…") heraus und meldet ausgerechnet das
        # als unumschlossen — ein Melder mit Fehlalarm wird nicht gelesen,
        # und dann faellt der echte Befund mit durch.
        ohne_t = re.sub(r'\$\(t\s+"[^"]*"\)', "\x00", roh)
        ohne_t = re.sub(r'(?:^|\s)t\s+"[^"]*"', "\x00", ohne_t)
        # Und die Senken mit ihrem ersten Argument: die laufen ohnehin durch
        # t(). Ohne das meldet jede Zeile, die zufaellig ein `echo` als
        # Vorgabewert traegt, ihren Fragetext als unumschlossen.
        ohne_t = re.sub(
            r'(?:^|\s)(?:info|gut|warn|fehler|erklaere|merke|merken|sect|row|gauge|'
            r'frage_ja|frage_text|frage_geheimnis)\s+\w*\s*"[^"]*"', "\x00", ohne_t)
        ohne_t = re.sub(r'lage_setz\s+(?:err|warn)\s+"[^"]*"', "\x00", ohne_t)
        for lit in re.findall(r'"([^"]{4,})"', ohne_t):
            klar = re.sub(r"\$\{[^}]*\}|\$\([^)]*\)|\$\w+|%[-0-9.]*[a-zA-Z]|\\[nt]",
                          " ", lit)
            klar = " ".join(klar.split())
            if len(klar) < 4 or klar in _KEIN_TEXT:
                continue
            if _DEUTSCH.search(klar):
                raus.append((nr, klar[:70]))
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
              % (len(gefunden), len(QUELLEN) + len(QUELLEN_BAT)))
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
    print("gefunden: %d Zeichenketten in %d Werkzeugen"
          % (len(gefunden), len(QUELLEN) + len(QUELLEN_BAT)))
    print("Katalog %s: %d Eintraege | fehlend: %d | verwaist: %d | Abdeckung: %.0f%%"
          % (sprache, len(kat), len(fehlt), len(verwaist), quote))
    # v4.2-W14: die EHRLICHE Haelfte. Die Quote oben sagt nur, wie viel von
    # dem uebersetzt ist, was der Sammler findet — sie kann 100 % melden,
    # waehrend eine ganze Datei deutsch bleibt. Genau das war bis hierher der
    # Fall: motd.sh band lib/i18n.sh ein und rief t() nie auf.
    offen = []
    for rel in QUELLEN + QUELLEN_BAT:
        for nr, txt in unumschlossen(rel):
            offen.append("%s:%d: %s" % (rel, nr, txt))
    print("unumschlossene deutsche Ausgabe: %d" % len(offen))
    for o in offen[:20]:
        print("  %s" % o)
    for v in verwaist[:20]:
        print("  verwaist: %s" % v[:100])
    if verwaist:
        # Ein Eintrag ohne Quelle heisst: der deutsche Text wurde geaendert und
        # der Katalog nicht nachgezogen. Ab jetzt bleibt diese Zeile fuer immer
        # deutsch, ohne dass es jemand merkt — DAS ist der Fehler.
        print("FEHLER: verwaiste Eintraege — deutscher Text geaendert?")
        return 1
    if offen:
        # Hartes Tor, und zwar bei NULL. Eine Ausnahmeliste "vier bekannte
        # Faelle" verrottet: nach dem fuenften liest niemand mehr hin.
        print("FEHLER: deutsche Ausgabe an keiner Senke — sie bleibt fuer "
              "immer deutsch, ohne dass die Abdeckung es zeigt")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
