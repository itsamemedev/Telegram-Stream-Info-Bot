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

import os
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
            werte[k.strip()] = v.split(" #", 1)[0].strip().strip('"').strip("'")
    return werte


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
    stempel = time.strftime("%Y%m%d-%H%M%S", time.localtime(jetzt))
    sicherung = "%s.%s-%s" % (pfad, kennung, stempel)
    alt = os.stat(pfad)
    shutil.copy2(pfad, sicherung)
    _eigentum(sicherung, alt)
    with open(pfad, encoding="utf-8") as fh:
        zeilen = fh.read().splitlines()
    for schluessel, wert in werte.items():
        neu = "%s=%s" % (schluessel, wert)
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
