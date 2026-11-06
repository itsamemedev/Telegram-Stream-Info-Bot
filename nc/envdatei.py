"""nc.envdatei — die .env lesen und gezielt aendern, ohne sie auszufuehren (rein).

v4.2-W144. Bis hierher gab es zwei Schreiber: den Umzug nach MariaDB (W143)
und keinen fuer Prometheus/Grafana — die schrieben gar nichts in die .env,
und wo Grafana lauscht und mit welchem Passwort, stand nirgends. Ein zweiter
Schreiber daneben waere die dritte Fassung derselben Regeln (W100: zwei
Listen fuer denselben Zweck laufen auseinander). Hier steht sie EINMAL:

  * gelesen wie python-dotenv: die LETZTE unkommentierte Zeile gewinnt;
  * ersetzt wird genau diese Zeile, fehlt der Schluessel, kommt er ans Ende;
  * vorher eine Sicherung `.env.<kennung>-<zeit>` mit denselben Rechten und
    demselben Besitzer — die Datei traegt Geheimnisse, und ein Werkzeug, das
    als root laeuft, darf sie dem Bot-Nutzer nicht wegnehmen;
  * geschrieben wird atomar (os.replace): kein Abbruch hinterlaesst eine
    halbe .env.

Kommandozeile, fuer die Shell-Werkzeuge — die Werte kommen ueber die
Standardeingabe, damit kein Passwort in der Prozessliste steht:

    printf 'GRAFANA_URL=http://127.0.0.1:3000\\n' | python3 -m nc.envdatei /pfad/.env grafana
"""

import codecs
import os
import re
import shutil
import sys
import time


class EnvdateiFehler(Exception):
    """Die .env laesst sich nicht so schreiben, dass der Bot sie danach liest."""


def lesen(pfad):
    """{schluessel: wert} — gelesen, nicht ausgefuehrt; die letzte Zeile gewinnt."""
    werte = {}
    if not os.path.isfile(pfad):
        return werte
    with open(pfad, encoding="utf-8") as fh:
        for z in fh:
            z = z.strip()
            if not z or z.startswith("#") or "=" not in z:
                continue
            k, v = z.split("=", 1)
            k = k.strip()
            if k.startswith("export "):
                k = k[len("export "):].strip()
            werte[k] = wert_lesen(v)
    return werte


_EINFACH = re.compile(r"'((?:\\'|[^'])*)'")
_DOPPELT = re.compile(r'"((?:\\"|[^"])*)"')
_ESC_EINFACH = re.compile(r"\\[\\']")
_ESC_DOPPELT = re.compile(r"\\[\\'\"abfnrtv]")


def _entschaerfen(muster, s):
    return muster.sub(lambda m: codecs.decode(m.group(0), "unicode-escape"), s)


def wert_lesen(roh: str) -> str:
    """Ein Wert, wie python-dotenv ihn liest (v4.2-W148, Codex #193/#194).

    Bis hierher schnitt `split(" #")` auch INNERHALB von Anfuehrungszeichen
    ab: aus `PROMPT="answer #1"` wurde `answer` — und `uebernehmen()` schrieb
    das gekuerzte in die Datenbank, wo es die richtige .env bei jedem Start
    ueberstimmte. Die Regeln sind abgeschrieben, nicht erfunden
    (dotenv/parser.py): in '…' gelten \\' und \\\\, in "…" zusaetzlich
    \\n, \\t und Verwandte; ungequotet ist ` #` ein Kommentar. Die erste
    Fassung kannte in '…' kein Escape und las `'It\\'s'` als `It\\`."""
    v = roh.strip()
    m = _EINFACH.match(v)
    if m:
        return _entschaerfen(_ESC_EINFACH, m.group(1))
    m = _DOPPELT.match(v)
    if m:
        return _entschaerfen(_ESC_DOPPELT, m.group(1))
    if v[:1] in ('"', "'"):
        # Kein schliessendes Zeichen: wie bisher, nur das oeffnende weg.
        return v[1:].strip()
    return v.split(" #", 1)[0].strip()


_KOMMENTAR = re.compile(r"\s#")


def wert_schreiben(wert) -> str:
    """Ein Wert so, dass python-dotenv ihn GENAU so zurueckliest (v4.2-W149).

    Bis hierher stand der Wert roh hinter dem `=`. Ein Passwort `abc #12`
    kam als `abc` zurueck (ungequotet ist ` #` ein Kommentar), eines mit
    `${X}` wurde von load_dotenv() interpoliert (die Vorgabe ist
    interpolate=True), eines mit fuehrendem `'` verlor sein Zeichen. Der Bot
    las damit etwas anderes, als geschrieben wurde — und weil `main()` nur
    schreibt, was sich laut `lesen()` unterscheidet, stand dieselbe falsche
    Zeile beim naechsten Lauf als "unveraendert" da.

    Einfache Anfuehrungszeichen: dotenv kennt darin nur zwei Escapes, \\ und
    \'. Alle anderen Werte bleiben ungequotet — so sieht
    die .env aus wie von Hand gepflegt. `${` laesst sich gar nicht schreiben:
    python-dotenv 1.2 interpoliert auch in '…' und kennt dafuer kein Escape
    (nachgemessen) — setzen() lehnt solche Werte ab."""
    v = str(wert)
    # Ungequotet liest dotenv alles bis zum Zeilenende, schneidet aber ein
    # " #" samt Rest ab, entfernt Rand-Leerzeichen und deutet ein fuehrendes
    # Anfuehrungszeichen. Nur dann wird gequotet.
    if v == v.strip() and not _KOMMENTAR.search(v) and v[:1] not in ("'", '"'):
        return v
    return "'" + v.replace("\\", "\\\\").replace("'", "\\'") + "'"


def setzen(pfad, werte, kennung="aenderung", jetzt=None):
    """Schluessel setzen, alles andere unveraendert. -> Pfad der Sicherung.

    Ein Wert mit Zeilenumbruch wird abgelehnt: er schriebe eine zweite,
    fremde Zeile in die Datei — bei einem Wert aus einem Formular waere das
    eine Einschleusung beliebiger Variablen."""
    for k, v in werte.items():
        if not k or not all(c.isalnum() or c == "_" for c in k):
            raise EnvdateiFehler("Kein gueltiger Variablenname: %r" % k)
        if "\n" in str(v) or "\r" in str(v):
            raise EnvdateiFehler("Wert fuer %s enthaelt einen Zeilenumbruch." % k)
        if "${" in str(v):
            raise EnvdateiFehler("Wert fuer %s enthaelt '${' — load_dotenv() wuerde ihn "
                                 "als Variable auswerten, ein Escape gibt es nicht." % k)
    stempel = time.strftime("%Y%m%d-%H%M%S", time.localtime(jetzt))
    sicherung = "%s.%s-%s" % (pfad, kennung, stempel)
    alt = os.stat(pfad)
    shutil.copy2(pfad, sicherung)
    _eigentum(sicherung, alt)
    with open(pfad, encoding="utf-8") as fh:
        zeilen = fh.read().splitlines()
    for schluessel, wert in werte.items():
        neu = "%s=%s" % (schluessel, wert_schreiben(wert))
        treffer = [i for i, z in enumerate(zeilen)
                   if z.lstrip().startswith(schluessel + "=")
                   or z.lstrip().startswith(schluessel + " =")]
        if treffer:
            zeilen[treffer[-1]] = neu
        else:
            zeilen.append(neu)
    tmp = pfad + ".tmp-" + kennung
    with open(tmp, "w", encoding="utf-8") as fh:
        fh.write("\n".join(zeilen) + "\n")
    shutil.copymode(pfad, tmp)
    _eigentum(tmp, alt)
    os.replace(tmp, pfad)
    return sicherung


def _eigentum(pfad, alt):
    """Besitzer und Gruppe der alten .env uebernehmen.

    Die Werkzeuge laufen als root; os.replace legte die neue .env sonst als
    root an — mit 600 kann der Bot-Nutzer sie dann nicht mehr lesen, und der
    Dienst startet nicht. Ohne Recht dazu gehoert die Datei schon dem Aufrufer."""
    if hasattr(os, "chown") and (alt.st_uid, alt.st_gid) != (os.stat(pfad).st_uid,
                                                            os.stat(pfad).st_gid):
        try:
            os.chown(pfad, alt.st_uid, alt.st_gid)
        except PermissionError as e:
            raise EnvdateiFehler(
                "Besitz der .env laesst sich nicht uebernehmen (%s) — als root oder als "
                "Besitzer der .env ausfuehren." % e) from e


def main(argv=None, stdin=None):
    """python3 -m nc.envdatei PFAD KENNUNG  — KEY=WERT-Zeilen auf stdin.

    Exitcodes: 0 gesetzt oder unveraendert, 1 nicht schreibbar, 2 Aufruf."""
    argv = sys.argv[1:] if argv is None else argv
    stdin = sys.stdin if stdin is None else stdin
    rc = 0
    if len(argv) != 2:
        print("Aufruf: python3 -m nc.envdatei PFAD KENNUNG  (KEY=WERT auf stdin)", file=sys.stderr)
        rc = 2
    elif not os.path.isfile(argv[0]):
        print("Keine .env unter %s." % argv[0], file=sys.stderr)
        rc = 2
    else:
        pfad, kennung = argv
        werte = {}
        for z in stdin.read().splitlines():
            if z.strip() and "=" in z:
                k, v = z.split("=", 1)
                werte[k.strip()] = v
        alt = lesen(pfad)
        werte = {k: v for k, v in werte.items() if alt.get(k) != v}
        if not werte:
            print("unveraendert")
        else:
            try:
                sicherung = setzen(pfad, werte, kennung)
                # Nur Namen, nie Werte — hier gehen Passwoerter durch.
                print("gesetzt: %s (Sicherung: %s)"
                      % (", ".join(sorted(werte)), os.path.basename(sicherung)))
            except EnvdateiFehler as e:
                print("FEHLER: %s" % e, file=sys.stderr)
                rc = 1
    return rc


if __name__ == "__main__":
    sys.exit(main())
