"""tools/ueberdeckung.py — v4.2-W86: welcher Code wird überhaupt ausgeführt?

════════════════════════════════════════════════════════════════════════
WARUM DIESES WERKZEUG
════════════════════════════════════════════════════════════════════════
Dieses Projekt misst viel und sperrt viel: stille `except`-Blöcke (1085),
stumme `return`-Ausgänge (478), Riesenfunktionen über vier Stufen,
`.env`-Lesungen vor `load_dotenv`, feste Fenster in den Verträgen,
Fremdpakete ohne Untergrenze. Eine Zahl fehlte, und es ist ausgerechnet die,
die den 322 Verträgen erst ihren Maßstab gibt:

    Welcher Teil von nc/ und brain/ wird beim Prüflauf überhaupt ausgeführt?

Ohne sie sagt „322 Verträge grün" nichts darüber, wie viel Bestand dabei
angefasst wurde. Die Antwort ist **47,4 %** — und das ist kein Vorwurf,
sondern eine Arbeitsliste: die untersten Einträge der Tabelle sind die
Module, in denen ein Fehler heute unbemerkt durchginge. `nc/scraper.py` und
`nc/director.py` stehen auf null.

════════════════════════════════════════════════════════════════════════
WARUM DIE SPERRE AUF „FEHLEND", NICHT AUF PROZENT
════════════════════════════════════════════════════════════════════════
Ein Prozentsatz springt auch dann, wenn gar nichts schlechter wurde: wer 200
Zeilen gut geprüften Code hinzufügt, hebt ihn, wer 200 Zeilen gut geprüften
Code entfernt, senkt ihn. Gesperrt wird deshalb die **Anzahl der nicht
ausgeführten Anweisungen**, genau wie bei `stillecheck` und `blindstellen`:
der Bestand darf bleiben, er darf nur nicht *wachsen*. Neuer Code ohne
Vertrag fällt damit auf, ohne dass ein Umbau die Sperre grundlos kippt.

════════════════════════════════════════════════════════════════════════
WARUM DAS ÜBERHAUPT STABIL IST
════════════════════════════════════════════════════════════════════════
Eine Überdeckungsmessung hängt normalerweise an der Umgebung — welche Pakete
installiert sind, entscheidet, welche Zweige laufen. Hier nicht: `nc/` und
`brain/` sind stdlib-only, und die Suiten stubben, was sie brauchen.
Nachgemessen gegen die CI-Minimalumgebung (`orjson flask waitress`) und gegen
eine volle Installation:

    CI-Minimal 3.13:   19495 Anweisungen, 10248 fehlend, 47,4 %
    voller venv 3.13:  19495 Anweisungen, 10248 fehlend, 47,4 %
    CI-Minimal 3.12:   19495 Anweisungen, 10248 fehlend, 47,4 %

Byte-identisch über beide Fassungen und beide Umgebungen. Deshalb ist die
Sperre hier tragfähig, wo sie es in einem Projekt mit vielen optionalen
Abhängigkeiten nicht wäre.

`bot.py` und `discordbot.py` sind bewusst NICHT dabei. Sie laufen nur im
Rauchtest, und der misst etwas anderes — dass der Prozess hochkommt und 364
Routen antworten, nicht welche Zweige dabei fallen. Eine Zahl, die beides
vermischt, wäre in keine Richtung mehr lesbar.
"""

import argparse
import io
import json
import os
import subprocess
import sys

WURZEL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GRUNDLINIE = os.path.join(WURZEL, ".claude", "ueberdeckung_grundlinie.json")

# Genau die Suiten, die der CI-Job `Vertraege & Module` faehrt. Wer hier etwas
# ergaenzt, hebt die Ueberdeckung und muss die Grundlinie neu setzen — das ist
# in Ordnung, aber es soll eine Entscheidung sein, keine Nebenwirkung.
SUITEN = (
    ("test_nc_modules.py", {}),
    ("test_restream.py", {}),
    ("test_m2_bridge.py", {}),
    (os.path.join("nc", "intel", "test_intel.py"), {"PYTHONPATH": WURZEL}),
)

GEMESSEN = "nc,brain"
# Der vendorierte QR-Encoder ist Fremdcode mit eigener Lizenz (wie ueberall
# sonst ausgenommen). Die test_*.py unter brain/ und nc/intel/ sind Tests, kein
# Produktionscode — mitgezaehlt druecken sie die Zahl um rund vier Punkte und
# stehen dann als "0 % gedeckt" ganz oben in der Arbeitsliste, wo sie nichts
# zu suchen haben.
AUSGENOMMEN = "nc/_vendor/*,*/test_*.py"


def _lauf(argv, umgebung=None):
    env = dict(os.environ, PYTHONUTF8="1")
    env.update(umgebung or {})
    return subprocess.run([sys.executable] + argv, cwd=WURZEL, env=env,
                          capture_output=True, text=True)


def messen():
    """Alle Suiten unter coverage fahren. -> (anweisungen, fehlend, prozent)

    Wirft RuntimeError, wenn eine Suite faellt oder coverage fehlt — eine
    Ueberdeckungszahl aus einem abgebrochenen Lauf ist schlimmer als keine:
    sie faellt, und zwar aus dem falschen Grund.
    """
    if _lauf(["-m", "coverage", "--version"]).returncode != 0:
        raise RuntimeError(
            "coverage ist nicht installiert.\n"
            "  python3 -m pip install coverage")

    _lauf(["-m", "coverage", "erase"])
    for suite, umgebung in SUITEN:
        if not os.path.isfile(os.path.join(WURZEL, suite)):
            raise RuntimeError("Suite fehlt: %s" % suite)
        r = _lauf(["-m", "coverage", "run", "-a", "--source=" + GEMESSEN,
                   "--omit=" + AUSGENOMMEN, suite], umgebung)
        if r.returncode != 0:
            raise RuntimeError(
                "%s ist gefallen — die Ueberdeckung daraus waere wertlos.\n%s"
                % (suite, (r.stdout or "")[-1500:] + (r.stderr or "")[-800:]))

    r = _lauf(["-m", "coverage", "json", "-o", "-", "--omit=" + AUSGENOMMEN])
    if r.returncode != 0:
        raise RuntimeError("coverage json fehlgeschlagen:\n" + (r.stderr or ""))
    d = json.loads(r.stdout)
    g = d["totals"]
    return g["num_statements"], g["missing_lines"], d["files"]


def _lade():
    try:
        return json.load(io.open(GRUNDLINIE, encoding="utf-8"))
    except (OSError, ValueError):
        return None


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    p.add_argument("--sperre", action="store_true",
                   help="faellt, wenn mehr Anweisungen ungeprueft sind als in "
                        "der Grundlinie")
    p.add_argument("--neu-grundlinie", action="store_true")
    a = p.parse_args(argv)

    anweisungen, fehlend, dateien = messen()
    prozent = 100.0 * (anweisungen - fehlend) / max(1, anweisungen)

    if a.neu_grundlinie:
        os.makedirs(os.path.dirname(GRUNDLINIE), exist_ok=True)
        io.open(GRUNDLINIE, "w", encoding="utf-8").write(json.dumps(
            {"anweisungen": anweisungen, "fehlend": fehlend,
             "prozent": round(prozent, 1)},
            ensure_ascii=False, indent=2) + "\n")
        print("Grundlinie eingefroren: %d Anweisungen, %d ungeprueft (%.1f %%)"
              % (anweisungen, fehlend, prozent))
        return 0

    if a.sperre:
        basis = _lade()
        if basis is None:
            print("ueberdeckung: KEINE GRUNDLINIE — einmal --neu-grundlinie "
                  "laufen lassen und die Datei mit einchecken.")
            return 1
        war = basis.get("fehlend", 0)
        if fehlend > war:
            print("ueberdeckung: MEHR UNGEPRUEFTER CODE — %d -> %d "
                  "ungepruefte Anweisungen (+%d)."
                  % (war, fehlend, fehlend - war))
            print("\n  Es ist Code dazugekommen, den kein Vertrag anfasst. "
                  "Das ist nicht verboten, aber es soll eine Entscheidung "
                  "sein: entweder ein Vertrag dazu, oder die Grundlinie neu "
                  "und die Begruendung in den Commit.")
            print("  Welche Datei es ist, zeigt der Lauf ohne --sperre.")
            return 1
        gewonnen = war - fehlend
        print("ueberdeckung: OK — %d von %d Anweisungen ungeprueft (%.1f %% "
              "gedeckt)%s" % (fehlend, anweisungen, prozent,
                              ", %d weniger als in der Grundlinie" % gewonnen
                              if gewonnen > 0 else ", keine neuen"))
        return 0

    print("Ueberdeckung von nc/ und brain/ durch die Vertragssuiten:")
    print("  %d Anweisungen, %d ungeprueft -> %.1f %% gedeckt"
          % (anweisungen, fehlend, prozent))
    roh = []
    for name, d in dateien.items():
        g = d["summary"]
        if g["num_statements"] >= 40:
            roh.append((g["percent_covered"], g["missing_lines"],
                        g["num_statements"], name))
    roh.sort()
    print("\nDie 20 groessten blinden Flecken (ab 40 Anweisungen):")
    print("  %6s %7s  %s" % ("Deckung", "fehlend", "Datei"))
    for pz, fehlt, ges, name in roh[:20]:
        print("  %5.0f %% %7d  %s (%d)" % (pz, fehlt, name, ges))
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except RuntimeError as e:
        print(str(e), file=sys.stderr)
        sys.exit(2)
    except BrokenPipeError:
        os._exit(0)
