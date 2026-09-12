#!/usr/bin/env python3
"""tools/stillecheck.py — v4.2-W65: der Hauptfeind, gezaehlt und eingesperrt.

CLAUDE.md sagt es seit Langem in einem Satz:

    „Stille except-Bloecke sind der Hauptfeind. Der Bot faengt grossflaechig
     ab und loggt auf warning/debug. Wenn etwas 'nicht mehr geht', suche
     zuerst das except, das den Grund frisst."

Gemessen wurde das nie. Beim Nachzaehlen: **1747 except-Bloecke, davon 1292
ohne jede Meldung**. Jede einzelne Welle dieser Reihe kam aus dieser Klasse:

    W51  der Recorder startete blind — die fehlende Stream-URL fiel in ein except
    W55  AZRAELs Ohr war taub, das Log sagte nur „audio=False"
    W60  die Drossel warf das Panel weg, ohne es zu erwaehnen
    W63  eine manuelle Aufnahme lief unsichtbar weiter
    W64  die Rechnung des KI-Anbieters ging als Antwort in den Chat

Alle 1292 auf einmal zu beheben waere ein Quartal und ein riesiger Diff. Dieses
Werkzeug macht stattdessen zwei Dinge, die sofort wirken:

  1. ES ZAEHLT UND SORTIERT. Nicht jedes stille except ist falsch — CLAUDE.md
     nennt die Ausnahmen selbst: Aufraeumpfade, deren Fehlschlag bedeutungslos
     ist (proc.terminate() auf einen toten Prozess, os.remove() auf eine
     geloeschte Datei), und der Fehlerkanal selbst, wo Loggen eine Rekursion
     erzeugt. Die trennt der Klassierer ab, damit die Zahl etwas bedeutet.

  2. ES SPERRT DEN ZUWACHS. `--sperre` vergleicht gegen eine eingefrorene
     Grundlinie je Datei und faellt, sobald irgendwo ein stiller Block
     dazukommt. Der Bestand darf bleiben; er darf nur nicht wachsen. Das ist
     der Unterschied zwischen einer Schuld, die man abtraegt, und einer, die
     sich verzinst.

Aufrufe:

    python3 tools/stillecheck.py                  Bericht
    python3 tools/stillecheck.py --sperre         gegen die Grundlinie (CI)
    python3 tools/stillecheck.py --neu-grundlinie Grundlinie neu einfrieren
    python3 tools/stillecheck.py --datei bot.py   nur eine Datei, mit Zeilen
"""

import argparse
import ast
import glob
import io
import json
import os
import sys

WURZEL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GRUNDLINIE = os.path.join(WURZEL, ".claude", "stille_grundlinie.json")

# Namen, die eine Meldung bedeuten. `_loop_fehler` ist der Weg fuer
# Dauerlaeufer (erste Meldung sofort auf error, danach gedrosselt), die
# uebrigen sind die im Bestand ueblichen Kanaele.
MELDER = ("log.", "_loop_fehler", "_react_warn", "_warn", "logger.",
          "melden", "logging.", "print(", "_telemetry", "log_event",
          "_modlog", "_record_error", "traceback.print")

# Aufrufe, deren Fehlschlag bedeutungslos ist — CLAUDE.md nennt genau diese
# Art: „proc.terminate() auf einen toten Prozess, os.remove() auf eine
# bereits geloeschte Datei".
AUFRAEUMEN = ("terminate", "kill", "unlink", "remove", "rmtree", "close",
              "shutdown", "cancel", "flush", "discard", "pop", "clear",
              "killpg", "wait", "disconnect", "stop")

# Dateien, in denen Stille die einzig richtige Antwort ist: der Fehlerkanal
# selbst. Ein log-Aufruf im Logging-Pfad erzeugt eine Rekursion.
FEHLERKANAL = ("nc/logsafe.py", "nc/fehlertext.py", "nc/ffdiag.py")

# KEINE FEHLER, SONDERN ABLAUFSTEUERUNG. Ein Abbruch ist kein Ausfall: er
# wurde angeordnet. Ihn zu melden erzeugt bei jedem geordneten Herunterfahren
# eine Warnung je Dauerlaeufer — und eine Warnung, die bei jedem sauberen
# Stopp kommt, erzieht dazu, Warnungen zu ueberlesen. Genau das nennt auch
# der W59-Audit als legitime Stille.
#
# Der erste Entwurf zaehlte sie mit und lieferte damit eine Zielliste, die zu
# drei Vierteln aus `except asyncio.CancelledError: raise` bestand. Eine
# Aufgabenliste voller Nicht-Aufgaben ist schlimmer als keine.
ABLAUFSTEUERUNG = ("CancelledError", "KeyboardInterrupt", "GeneratorExit",
                   "SystemExit", "StopIteration", "StopAsyncIteration")


def _dateien():
    """Alle ausgelieferten .py — ohne Tests und ohne Werkzeuge."""
    aus = ["bot.py", "discordbot.py", "brain_bridge.py", "telegramversand.py"]
    aus += sorted(glob.glob("nc/**/*.py", recursive=True))
    aus += sorted(glob.glob("brain/**/*.py", recursive=True))
    return [p for p in aus
            if os.path.isfile(os.path.join(WURZEL, p))
            and not os.path.basename(p).startswith("test_")]


def _punktname(knoten) -> str:
    """Aufruf-Ziel als gepunkteter Name: log.warning -> "log.warning".

    UEBER DEN SYNTAXBAUM, nicht ueber ast.dump. Der erste Entwurf suchte
    `"log." in ast.dump(...)` — und dump rendert einen Attributzugriff als
    Attribute(value=Name(id='log'), attr='warning'). Die Zeichenkette "log."
    kommt darin NIE vor. Das Werkzeug meldete deshalb 121 Melder statt 455
    und haette den Bestand um den Faktor vier zu schwarz gezeichnet. Ein
    Messgeraet, das falsch misst, ist schlimmer als keines.
    """
    teile = []
    while isinstance(knoten, ast.Attribute):
        teile.append(knoten.attr)
        knoten = knoten.value
    if isinstance(knoten, ast.Name):
        teile.append(knoten.id)
    return ".".join(reversed(teile))


def _ist_ablaufsteuerung(handler) -> bool:
    """Faengt der Block NUR Abbruch-Signale? -> bool"""
    typ = handler.type
    if typ is None:
        return False                     # bare except faengt auch echte Fehler
    kandidaten = typ.elts if isinstance(typ, ast.Tuple) else [typ]
    namen = [_punktname(k) for k in kandidaten]
    return bool(namen) and all(
        any(a in (n or "") for a in ABLAUFSTEUERUNG) for n in namen)


_ABGELEITETE_MELDER = None


def _melder_sammeln():
    """Funktionen, die SELBST melden — aus dem Bestand gelesen, nicht geraten.

    Der zweite Entwurf hatte eine handgeschriebene MELDER-Liste, und die war
    unvollstaendig: `_verbindung_verloren(...)` steht in vier Twitch- und
    YouTube-Dauerlaeufern, meldet dort sauber mit Verlaufsbewertung — und
    galt trotzdem als Stille. Die Zielliste enthielt damit vier Faelle, an
    denen nichts zu tun war.

    Eine geratene Liste veraltet ausserdem mit dem naechsten Helfer. Deshalb
    wird sie hier abgeleitet: jede Top-Level-Funktion, deren eigener Rumpf
    einen bekannten Kanal ruft, ist selbst ein Kanal. Eine Ebene genuegt —
    tiefer wird es unscharf, und Unschaerfe in einem Messgeraet ist genau das,
    was hier zweimal danebengelegen hat.
    """
    global _ABGELEITETE_MELDER
    if _ABGELEITETE_MELDER is not None:
        return _ABGELEITETE_MELDER
    gefunden = set()
    for pfad in _dateien():
        try:
            baum = ast.parse(io.open(os.path.join(WURZEL, pfad),
                                     encoding="utf-8").read())
        except (OSError, SyntaxError):
            continue
        for n in ast.walk(baum):
            if not isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)):
                continue
            for k in ast.walk(n):
                if not isinstance(k, ast.Call):
                    continue
                ziel = _punktname(k.func).lower()
                if any(m.strip("(.").lower() in ziel for m in MELDER):
                    gefunden.add(n.name.lower())
                    break
    _ABGELEITETE_MELDER = gefunden
    return gefunden


def _meldet(handler) -> bool:
    abgeleitet = _melder_sammeln()
    for n in ast.walk(handler):
        if isinstance(n, ast.Raise):
            return True                  # weiterwerfen ist auch eine Antwort
        if not isinstance(n, ast.Call):
            continue
        name = _punktname(n.func).lower()
        if any(m.strip("(.").lower() in name for m in MELDER):
            return True
        if name.split(".")[-1] in abgeleitet:
            return True
    return False


def _nur_aufraeumen(versuch) -> bool:
    """Steht im try-Block ausschliesslich Aufraeumarbeit?"""
    rufe = [n for n in ast.walk(versuch) if isinstance(n, ast.Call)]
    if not rufe:
        return False
    namen = []
    for r in rufe:
        f = r.func
        namen.append(f.attr if isinstance(f, ast.Attribute)
                     else (f.id if isinstance(f, ast.Name) else ""))
    return all(any(a in (n or "") for a in AUFRAEUMEN) for n in namen)


def pruefe_datei(pfad):
    """-> (still, laut, aufraeumen, [zeilennummern der stillen])"""
    try:
        quelle = io.open(os.path.join(WURZEL, pfad), encoding="utf-8").read()
        baum = ast.parse(quelle)
    except (OSError, SyntaxError):
        return 0, 0, 0, []
    still, laut, aufr, zeilen = 0, 0, 0, []
    kanal = any(pfad.endswith(k) for k in FEHLERKANAL)
    for n in ast.walk(baum):
        if not isinstance(n, ast.Try):
            continue
        sauber = _nur_aufraeumen(n)
        for h in n.handlers:
            if _meldet(h):
                laut += 1
            elif sauber or kanal or _ist_ablaufsteuerung(h):
                aufr += 1
            else:
                still += 1
                zeilen.append(h.lineno)
    return still, laut, aufr, zeilen


def bericht():
    """-> (stand, gesamt) — stand ist {datei: stille Bloecke}"""
    stand, gesamt = {}, {"still": 0, "laut": 0, "aufraeumen": 0}
    for pfad in _dateien():
        s, l, a, _ = pruefe_datei(pfad)
        if s:
            stand[pfad] = s
        gesamt["still"] += s
        gesamt["laut"] += l
        gesamt["aufraeumen"] += a
    return stand, gesamt


def _lade_grundlinie():
    try:
        return json.load(io.open(GRUNDLINIE, encoding="utf-8"))
    except (OSError, ValueError):
        return None


def main():
    p = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    p.add_argument("--sperre", action="store_true",
                   help="gegen die Grundlinie pruefen (Rueckgabe 1 bei Zuwachs)")
    p.add_argument("--neu-grundlinie", action="store_true",
                   help="Grundlinie auf den aktuellen Stand einfrieren")
    p.add_argument("--datei", help="nur diese Datei, mit Zeilennummern")
    a = p.parse_args()

    if a.datei:
        s, l, auf, zeilen = pruefe_datei(a.datei)
        print(f"{a.datei}: {s} still, {l} melden, {auf} legitim still")
        for z in zeilen:
            print(f"  {a.datei}:{z}")
        return 0

    stand, gesamt = bericht()
    if a.neu_grundlinie:
        os.makedirs(os.path.dirname(GRUNDLINIE), exist_ok=True)
        io.open(GRUNDLINIE, "w", encoding="utf-8").write(
            json.dumps({"stille_bloecke": dict(sorted(stand.items())),
                        "summe": gesamt["still"]},
                       ensure_ascii=False, indent=2) + "\n")
        print(f"Grundlinie eingefroren: {gesamt['still']} stille Bloecke "
              f"in {len(stand)} Dateien -> {os.path.relpath(GRUNDLINIE, WURZEL)}")
        return 0

    if a.sperre:
        basis = _lade_grundlinie()
        if basis is None:
            print("stille: KEINE GRUNDLINIE — einmal --neu-grundlinie laufen "
                  "lassen und die Datei mit einchecken.")
            return 1
        alt = basis.get("stille_bloecke", {})
        gewachsen = [(d, alt.get(d, 0), n) for d, n in sorted(stand.items())
                     if n > alt.get(d, 0)]
        if gewachsen:
            print("stille: NEUE stille except-Bloecke — jeder frisst einen "
                  "Grund, den spaeter jemand sucht.")
            for d, war, ist in gewachsen:
                print(f"  {d}: {war} -> {ist}")
            print("\n  Abhilfe: melden statt schlucken. In Dauerlaeufern mit")
            print("  _loop_fehler(name, exc) — erste Meldung sofort auf error,")
            print("  danach hoechstens alle 15 Minuten eine.")
            print("  Ist die Stille richtig (Aufraeumpfad, Fehlerkanal), dann")
            print("  erkennt der Klassierer sie meist selbst; sonst gehoert die")
            print("  Begruendung als Kommentar daneben und die Grundlinie neu.")
            return 1
        gesunken = sum(alt.values()) - gesamt["still"]
        print(f"stille: OK — {gesamt['still']} stille Bloecke, keine neuen"
              + (f" (–{gesunken} seit der Grundlinie)" if gesunken > 0 else ""))
        return 0

    ges = gesamt["still"] + gesamt["laut"] + gesamt["aufraeumen"]
    print(f"except-Bloecke: {ges}")
    print(f"  melden           {gesamt['laut']:5d}")
    print(f"  legitim still    {gesamt['aufraeumen']:5d}  "
          f"(Aufraeumpfade, Fehlerkanal, Abbruch-Signale)")
    print(f"  STILL            {gesamt['still']:5d}  "
          f"({100 * gesamt['still'] / max(1, ges):.0f} %)")
    print("\nDie 15 Dateien mit den meisten stillen Bloecken:")
    for d, n in sorted(stand.items(), key=lambda x: -x[1])[:15]:
        print(f"  {n:5d}  {d}")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except BrokenPipeError:
        # `stillecheck.py | head` — kein Fehler, sondern ein Leser, der genug
        # gesehen hat. Ohne das steht bei jedem gekuerzten Aufruf ein
        # Traceback unter dem Bericht.
        os._exit(0)
