#!/usr/bin/env python3
"""i18n_extract — die uebersetzbaren Zeichenketten einsammeln und den Katalog pflegen.

    python3 tools/i18n_extract.py                 # Bericht: was ist da, was fehlt
    python3 tools/i18n_extract.py --write en      # locales/en.json ergaenzen (nie ueberschreiben)
    python3 tools/i18n_extract.py --check en      # Vertrag: fehlende + verwaiste Eintraege

Warum die deutsche Zeichenkette der Schluessel ist, steht in nc/i18n.py. Hier
steht die andere Haelfte: **wie man merkt, dass der Katalog auseinanderlaeuft.**
Ohne diese Pruefung waere der Preis des Verfahrens unsichtbar — ein geaenderter
deutscher Satz faellt still auf Deutsch zurueck, und niemand sieht es.

`--write` ergaenzt nur; eine bestehende Uebersetzung wird NIE angefasst. Sonst
wuerde ein Lauf des Werkzeugs geleistete Arbeit ueberschreiben.
"""

import argparse
import ast
import io
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOCALES = os.path.join(ROOT, "locales")

HTML_DATEIEN = ["templates/dashboard.html", "templates/brain.html",
                "templates/overlay.html", "website/lafap_index.html",
                "website/impressum.html", "website/datenschutz.html"]
PY_DATEIEN = ["bot.py"]

# Ein Text ist uebersetzbar, wenn er ueberhaupt Sprache enthaelt. Reine Zahlen,
# Symbole, CSS-Werte und Platzhalter fliegen raus.
_WORT = re.compile(r"[A-Za-zÄÖÜäöüß]{3}")
# Deutsche Marker: Umlaute oder Funktionswoerter. Englische Fachbegriffe wie
# "Restream" oder "Dashboard" sind in beiden Sprachen gleich und brauchen
# keinen Eintrag — sie werden hier bewusst NICHT eingesammelt.
_DEUTSCH = re.compile(
    r"[ÄÖÜäöüß]|\b(?:der|die|das|den|dem|des|ein|eine|einen|einem|und|oder|nicht|"
    r"kein|keine|keinen|wird|wurde|werden|ist|sind|war|waren|hat|haben|kann|"
    r"koennen|muss|muessen|soll|bitte|noch|schon|nur|auch|mehr|alle|jede|jeder|"
    r"beim|vom|zum|zur|fuer|mit|ohne|nach|vor|ueber|unter|seit|Fehler|Datei|"
    r"Ziel|Quelle|Zeit|Datum|Name|Anzahl|Grund|Stand|Wert|Seite|Sprache|"
    r"gespeichert|geladen|gestartet|gestoppt|laeuft|fehlt|fehlen|unbekannt)\b")

_SKIP_ATTR_WERTE = re.compile(r"^[\d\s.,:%#/+-]*$")


# Ein Schluessel muss im DOM als GANZER Textknoten auftauchen koennen, sonst
# trifft er nie. Diese Muster erkennen die Bruchstuecke, die entstehen, wenn das
# Dashboard sein HTML per String-Verkettung baut.
_MARKUP = re.compile(r'[<>]|\w+\s*=\s*["\']|\$\{|`')
_BRUCHSTUECK_ANFANG = re.compile(r'^[)\],;:%.\u2014\u2013+*/|=&#-]')
_BRUCHSTUECK_ENDE = re.compile(r'[(\[{=]$|\b(?:und|oder|der|die|das|von|mit|im|in|am|auf|zu|bei)$')


def _ist_uebersetzbar(text, deutsch_noetig=True, bezeichner_moeglich=True):
    """deutsch_noetig=False fuer Stellen, die per Definition Benutzertext sind.

    Der Deutsch-Marker ist eine Heuristik gegen Bezeichner und CSS-Werte. Bei
    einer Slash-Befehl-Beschreibung braucht es sie nicht: dort steht IMMER Text
    fuer Menschen, auch wenn er zufaellig ohne Umlaut auskommt ("Status",
    "Tracklist"). Ohne diese Ausnahme fielen 22 der 46 Beschreibungen aus dem
    Katalog — und die Befehlsliste im Discord waere halb deutsch geblieben.

    bezeichner_moeglich=False fuer Stellen, an denen ein einzelnes Wort KEIN
    Bezeichner sein kann, weil es zwischen zwei Tags steht (v4.1-W18). Ein
    `<th>Datei</th>` ist im DOM ein vollstaendiger Textknoten und niemals eine
    CSS-Klasse; die Bezeichner-Heuristik hat dort nichts zu entscheiden.
    """
    t = (text or "").strip()
    if len(t) < 3 or not _WORT.search(t):
        return False
    if t.startswith("{{") or t.startswith("${") or t.startswith("&"):
        return False
    # Reine Bezeichner (CSS-Klassen, IDs, Dateinamen, URLs) sind kein Text —
    # ausser an Stellen, die per Definition Benutzertext sind. "Restream-Status"
    # sieht fuer diese Pruefung aus wie ein Bezeichner und ist doch die
    # Beschreibung eines Slash-Befehls.
    if deutsch_noetig and bezeichner_moeglich and re.fullmatch(r"[\w./#:-]+", t):
        return False
    if t.startswith("http://") or t.startswith("https://"):
        return False
    # v4.1-W6: Bruchstuecke aussortieren. Der Uebersetzer im Browser vergleicht
    # GANZE Textknoten; ein Stueck wie ") — bitte durchsehen" oder
    # '<span class="btn" onclick="x(' steht dort nie fuer sich. Ein Eintrag
    # dafuer waere tot und wuerde den Katalog nur aufblaehen — schlimmer noch,
    # er wuerde als "uebersetzt" zaehlen, obwohl die Stelle deutsch bleibt.
    if _MARKUP.search(t):
        return False
    if _BRUCHSTUECK_ANFANG.match(t) or _BRUCHSTUECK_ENDE.search(t):
        return False
    if "\n" in t:
        return False
    return bool(_DEUTSCH.search(t)) if deutsch_noetig else True


def _js_textstuecke(literal):
    """Aus einem JS-Literal die Stuecke holen, die spaeter als TEXT im DOM stehen.

    Der Uebersetzer im Browser sieht Textknoten, keine Quelltext-Literale. Ein
    Literal wie `<div class="empty">Noch keine Aufnahmen.</div>` erscheint dort
    als der blosse Satz — das rohe Literal als Schluessel zu nehmen waere ein
    Eintrag, der NIE trifft. Deshalb: Markup abziehen, an ${...} trennen (was
    dort steht, sind Daten und wechselt zur Laufzeit), und nur die festen
    Stuecke behalten.

    Bruchstuecke wie "Fuer @" fliegen raus: sie stehen im DOM nie allein,
    sondern verschmelzen mit dem eingesetzten Wert zu einem Textknoten. Ein
    Eintrag dafuer waere ebenfalls tot — solche Saetze brauchen ein T() an der
    Quelle und kommen in einer eigenen Welle.
    """
    if not literal:
        return []
    # ${...} und Markup entfernen; beides ist im DOM kein uebersetzbarer Text.
    ohne_var = re.sub(r"\$\{[^}]*\}", "\x00", literal)
    ohne_tags = re.sub(r"<[^>]{0,200}>", "\x01", ohne_var)
    # v4.1-W18: Ein Stueck zwischen zwei TAGS ist im DOM ein vollstaendiger
    # Textknoten und darf deshalb auch ein einzelnes Wort sein. Genau daran
    # fielen bisher die Tabellenkoepfe aus dem Katalog — 'Datei', 'Datum',
    # 'Grund', 'Groesse', 'Geloescht' stehen als <th>…</th> voellig fuer sich,
    # zaehlten aber als "weniger als zwei Woerter" und flogen mit den echten
    # Bruchstuecken zusammen raus. Ergebnis: der Kopf einer Tabelle blieb
    # deutsch, waehrend ihr Inhalt uebersetzt war.
    raus = []
    # \x00 = ${...}, \x01 = Tag. Der Unterschied entscheidet, ob ein Stueck im
    # DOM allein steht: an einem Tag endet ein Textknoten, an einem Platzhalter
    # verschmilzt er mit dem eingesetzten Wert.
    teile = re.split(r"([\x00\x01])", ohne_tags)
    stuecke = teile[::2]
    grenzen = teile[1::2]
    for i, stueck in enumerate(stuecke):
        links = grenzen[i - 1] if i > 0 else None
        rechts = grenzen[i] if i < len(grenzen) else None
        stueck = stueck.replace("&nbsp;", " ").replace("&amp;", "&").strip()
        # Ein Knoten steht fuer sich, wenn ihn auf beiden Seiten ein Tag oder
        # das Literalende begrenzt UND mindestens eine Seite wirklich ein Tag
        # ist. Die zweite Bedingung ist der Punkt: ein blankes Literal wie
        # 'läuft' kann genauso gut ein Vergleichswert sein (`x === 'läuft'`)
        # oder ein Objektschluessel. Dafuer einen Eintrag anzulegen waere ein
        # TOTER Eintrag — er zaehlte als uebersetzt, waehrend die Stelle
        # deutsch bleibt, und verdeckte damit genau das, was die Pruefung
        # sichtbar machen soll. Ein Tag daneben ist dagegen ein Beleg: so
        # schreibt niemand einen Vergleich.
        allein = (links in (None, "\x01") and rechts in (None, "\x01")
                  and "\x01" in (links, rechts))
        if not _ist_uebersetzbar(stueck, bezeichner_moeglich=not allein):
            continue
        # Sonst: mindestens zwei Woerter ODER ein abgeschlossener Satz — alles
        # andere ist ein Bruchstueck um einen Platzhalter herum und stuende im
        # DOM nie fuer sich.
        if not allein and len(stueck.split()) < 2 and not stueck.endswith((".", "!", "?", ":")):
            continue
        raus.append(stueck)
    return raus


def _html_strings(pfad):
    """Textknoten, uebersetzbare Attribute und deutschsprachige JS-Literale."""
    roh = io.open(os.path.join(ROOT, pfad), encoding="utf-8").read()
    # v4.1-W10 (CodeQL py/bad-tag-filter): `</script>` ist nicht die einzige
    # Schreibweise, die ein Browser als Ende akzeptiert — `</script >` und
    # `</SCRIPT\n>` sind es auch. Der alte Ausdruck haette dort weitergesucht
    # und den Rest der Datei als Skript verschluckt; im Extraktor heisst das:
    # alle folgenden Textknoten fehlen im Katalog, ohne dass es auffaellt.
    ohne_js = re.sub(r"<script\b.*?</script\s*>|<style\b.*?</style\s*>|<!--.*?-->", "",
                     roh, flags=re.S | re.I)
    raus = set()
    for t in re.findall(r">([^<>]+)<", ohne_js):
        if _ist_uebersetzbar(t):
            raus.add(t.strip())
    for a in re.findall(r'(?:placeholder|title|aria-label|alt)="([^"]{3,})"', ohne_js):
        if _ist_uebersetzbar(a) and not _SKIP_ATTR_WERTE.match(a):
            raus.add(a.strip())
    js = "\n".join(re.findall(r"<script\b[^>]*>(.*?)</script\s*>", roh,
                              flags=re.S | re.I))
    for a, b, c in re.findall(r"'([^'\\\n]{4,})'|\"([^\"\\\n]{4,})\"|`([^`\\\n]{4,})`", js):
        for stueck in _js_textstuecke(a or b or c):
            raus.add(stueck)
    return raus


# Wohin ein Text fliesst, entscheidet, ob er uebersetzt gehoert. Diese Aufrufe
# gehen an einen MENSCHEN — Telegram-Antworten, Discord-Nachrichten, die
# Beschreibungen der Slash-Befehle. Alles andere in bot.py ist Log und Diagnose
# fuer den Betreiber und hat im Katalog nichts verloren: 660 log.*-Aufrufe
# wuerden ihn um Hunderte Eintraege aufblaehen, die nie jemand liest und die
# faelschlich als "noch zu uebersetzen" zaehlen.
_SENKEN = {"reply_text", "send_message", "_safe_send", "send", "answer", "reply",
           "send_video", "send_photo", "send_document", "edit_text",
           "edit_message_text", "respond"}
# Schluesselwoerter, unter denen Text an dieselben Senken geht.
_SENKE_KW = {"text", "content", "caption", "description"}


def _py_strings(pfad):
    """Die Zeichenketten aus bot.py, die einen BENUTZER erreichen.

    Nicht jedes deutsche Literal gehoert in den Katalog. bot.py hat rund 870
    deutschsprachige Literale, davon sind die allermeisten Logzeilen: sie
    erreichen nie jemanden ausser dem Betreiber im Journal, und CLAUDE.md sagt
    ausdruecklich, dass die auf Deutsch bleiben. Ein Katalog, der sie
    einsammelt, zaehlt Hunderte Eintraege als "noch zu uebersetzen", die
    niemand je sehen wird — und verdeckt damit, was wirklich fehlt.

    Eingesammelt wird deshalb, was in eine Senke fliesst (siehe _SENKEN) oder
    als description= an einem Slash-Befehl haengt. Docstrings sind ohnehin
    ausgeschlossen; der AST unterscheidet sie zuverlaessig, ein Regex nicht.
    """
    quelle = io.open(os.path.join(ROOT, pfad), encoding="utf-8").read()
    baum = ast.parse(quelle)
    raus = set()

    def _aus_knoten(n, deutsch_noetig=True):
        if isinstance(n, ast.Constant) and isinstance(n.value, str):
            if _ist_uebersetzbar(n.value, deutsch_noetig):
                raus.add(n.value.strip())
        elif isinstance(n, ast.JoinedStr):
            for x in n.values:
                if isinstance(x, ast.Constant) and isinstance(x.value, str):
                    st = x.value.strip()
                    if _ist_uebersetzbar(st, deutsch_noetig) and len(st.split()) >= 3:
                        raus.add(st)
        elif isinstance(n, ast.BinOp):
            # "Text " + var + " Rest": beide Seiten pruefen.
            _aus_knoten(n.left, deutsch_noetig)
            _aus_knoten(n.right, deutsch_noetig)
        elif isinstance(n, ast.Call):
            # Bereits umschlossenes _nc_i18n.t("..."): das Argument ist der Text.
            for a in n.args[:1]:
                _aus_knoten(a, deutsch_noetig)

    for n in ast.walk(baum):
        if not isinstance(n, ast.Call):
            continue
        f = n.func
        name = f.attr if isinstance(f, ast.Attribute) else (f.id if isinstance(f, ast.Name) else None)
        treffer = name in _SENKEN
        for arg in (n.args if treffer else []):
            _aus_knoten(arg)
        for kw in n.keywords:
            if kw.arg in _SENKE_KW and (treffer or kw.arg == "description"):
                _aus_knoten(kw.value, deutsch_noetig=(kw.arg != "description"))
    return raus


def sammeln():
    gefunden = {}
    for p in HTML_DATEIEN:
        if os.path.exists(os.path.join(ROOT, p)):
            for s in _html_strings(p):
                gefunden.setdefault(s, set()).add(p)
    for p in PY_DATEIEN:
        if os.path.exists(os.path.join(ROOT, p)):
            for s in _py_strings(p):
                gefunden.setdefault(s, set()).add(p)
    return gefunden


def _laden(sprache):
    pfad = os.path.join(LOCALES, "%s.json" % sprache)
    if not os.path.exists(pfad):
        return {"sprache": sprache, "strings": {}}
    with io.open(pfad, encoding="utf-8") as f:
        return json.load(f)


def _speichern(sprache, daten):
    os.makedirs(LOCALES, exist_ok=True)
    daten["strings"] = dict(sorted(daten.get("strings", {}).items()))
    with io.open(os.path.join(LOCALES, "%s.json" % sprache), "w", encoding="utf-8") as f:
        json.dump(daten, f, ensure_ascii=False, indent=2, sort_keys=False)
        f.write("\n")


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--write", metavar="SPRACHE", help="fehlende Schluessel ergaenzen (leer)")
    ap.add_argument("--check", metavar="SPRACHE", help="Vertrag: fehlend + verwaist melden")
    ap.add_argument("--liste", metavar="SPRACHE", help="fehlende Schluessel ausgeben, einer je Zeile")
    a = ap.parse_args()

    gefunden = sammeln()
    print("gefunden: %d uebersetzbare Zeichenketten in %d Dateien"
          % (len(gefunden), len(HTML_DATEIEN) + len(PY_DATEIEN)))

    sprache = a.write or a.check or a.liste
    if not sprache:
        je_datei = {}
        for _text, dateien in gefunden.items():
            for d in dateien:
                je_datei[d] = je_datei.get(d, 0) + 1
        for d, n in sorted(je_datei.items(), key=lambda x: -x[1]):
            print("   %-34s %4d" % (d, n))
        return 0

    daten = _laden(sprache)
    vorhanden = daten.get("strings", {})
    fehlend = sorted(s for s in gefunden if s not in vorhanden)
    verwaist = sorted(k for k in vorhanden if k not in gefunden)

    if a.liste:
        for s in fehlend:
            print(json.dumps(s, ensure_ascii=False))
        return 0

    print("Katalog %s: %d Eintraege | fehlend: %d | verwaist: %d"
          % (sprache, len(vorhanden), len(fehlend), len(verwaist)))

    if a.check:
        if verwaist:
            print("\nVERWAIST — im Quelltext nicht mehr gefunden (Text geaendert?):")
            for k in verwaist[:20]:
                print("   %s" % k[:100])
            if len(verwaist) > 20:
                print("   ... und %d weitere" % (len(verwaist) - 20))
        if fehlend:
            print("\nFEHLEND — ohne Uebersetzung, faellt auf Deutsch zurueck:")
            for k in fehlend[:20]:
                print("   %s" % k[:100])
            if len(fehlend) > 20:
                print("   ... und %d weitere" % (len(fehlend) - 20))
        return 1 if (fehlend or verwaist) else 0

    for s in fehlend:
        vorhanden[s] = ""
    daten["strings"] = vorhanden
    daten.setdefault("sprache", sprache)
    _speichern(sprache, daten)
    print("geschrieben: locales/%s.json (%d neue leere Eintraege)" % (sprache, len(fehlend)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
