"""nc.auslieferung — v4.2-W85: welcher Stand läuft hier eigentlich?

════════════════════════════════════════════════════════════════════════
WARUM DIESES MODUL
════════════════════════════════════════════════════════════════════════
Ausgeliefert wird per ZIP über den Bestand; das Repo trägt Historie, CI und
Issues, es ist nicht der Deploy-Weg. `tools/deploy.sh` macht das ordentlich —
Staging, Prüfung, dann umschwenken. Was fehlt, ist die Gegenprobe hinterher:

    Entspricht das, was gerade läuft, überhaupt einem Commit?

Heute lässt sich das nicht beantworten. Ein Handgriff direkt auf dem Server —
eine Zeile in `bot.py` geändert, um eine Störung zu überbrücken — ist danach
unsichtbar. Beim nächsten Deploy wird er wortlos überschrieben, und der
Fehler, den er behoben hat, ist zurück. Das ist die einzige echte Lücke des
ZIP-Wegs, und sie kostet eine Datei.

`tools/build_release.py` schreibt beim Packen eine `AUSLIEFERUNG.json` ins
Archiv: Commit, Zweig, ob der Arbeitsbaum beim Bauen sauber war, Zeitpunkt,
Version. Dieses Modul liest sie und beantwortet die Frage über `/healthz` und
`/api/version` — dort, wo der Betreiber ohnehin nachsieht.

**Was es NICHT tut.** Es prüft keine Dateien nach und misst keine Abweichung
zum Repo. Ein Hash über den Bestand klänge gründlicher, wäre aber bei jeder
`.pyc`, jeder Logdatei und jedem lokalen Eingriff rot — und eine Meldung, die
immer rot ist, liest niemand. Gefragt ist die Herkunft, nicht die Unversehrtheit.

**Warum es ohne die Datei nicht meckert.** Wer aus dem Repo heraus startet,
hat keine `AUSLIEFERUNG.json`, und das ist völlig in Ordnung. Dann wird
ersatzweise `git` gefragt; geht auch das nicht, lautet die Antwort schlicht
„unbekannt". Ein Fehlalarm auf der Entwicklungsmaschine erzieht dazu, die
Meldung auch auf dem Server zu überlesen.
"""

import json
import logging
import os
import subprocess

log = logging.getLogger("TikTokBot")

DATEI = "AUSLIEFERUNG.json"

_ZWISCHENSPEICHER = {}


def _wurzel() -> str:
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


UNBEKANNT = {"commit": "", "zweig": "", "sauber": None, "gebaut_am": "",
             "version": "", "quelle": "unbekannt"}


def _git(wurzel, *args) -> str:
    """git aufrufen. -> Ausgabe oder "" (auch, wenn es kein git gibt).

    timeout ist Pflicht: ein git, das auf ein Netzlaufwerk oder eine
    Sperrdatei wartet, wuerde sonst den Start blockieren — und zwar an einer
    Stelle, an der niemand git vermutet.

    Die leere Zeichenkette ist hier KEIN Misserfolg, sondern die Antwort
    "dieser Baum sagt dazu nichts". Deshalb steht sie in einem Ausgang und
    nicht in einem eigenen Fehlerzweig; wer sie bekommt, entscheidet selbst,
    ob das ein Problem ist — auf dem Server ist es der Normalfall.
    """
    aus = ""
    try:
        r = subprocess.run(("git",) + args, cwd=wurzel, capture_output=True,
                           text=True, timeout=5)
        aus = r.stdout.strip() if r.returncode == 0 else ""
    except (OSError, subprocess.SubprocessError) as e:
        # Auf debug, und nur hier: kein git zu haben ist auf dem Server der
        # NORMALFALL — dort kommt die Herkunft aus der Stempeldatei. Eine
        # Meldung bei jedem Start waere ein Dauer-Fehlalarm, und der erzieht
        # dazu, auch die echten zu ueberlesen. Dass die Herkunft am Ende
        # unbekannt bleibt, meldet stand()/text() laut genug.
        log.debug("git %s nicht ausfuehrbar (%s: %s)", args[0],
                  type(e).__name__, e)
    return aus


def _ermittle(wurzel) -> dict:
    """Die Herkunft bestimmen. -> immer ein vollstaendiges Woerterbuch.

    EIN Ausgang, kein `return None` in einem Zweig. Die Reihenfolge ist
    Absicht: erst die ausgelieferte Datei, dann git. Auf dem Server gibt es
    kein .git — dort ist die Datei die einzige Wahrheit. Auf der
    Entwicklungsmaschine gibt es beides, und dann ist git das Aktuellere: die
    Datei stammt vom letzten `build_release`, der Arbeitsbaum ist weiter.

    Dass die Datei FEHLT, ist der Normalfall (Start aus dem Repo) und bleibt
    still. Dass sie da, aber kaputt ist, nicht: sonst wuerde daraus "Herkunft
    unbekannt", und der Betreiber glaubte, er habe von Hand ausgeliefert,
    waehrend in Wahrheit das Archiv beschaedigt ist.
    """
    aus = dict(UNBEKANNT)
    pfad = os.path.join(wurzel, DATEI)

    if os.path.isfile(pfad):
        d = None
        try:
            with open(pfad, encoding="utf-8") as fh:
                d = json.load(fh)
        except (OSError, ValueError) as e:
            log.error("%s ist vorhanden, aber nicht lesbar (%s: %s) — die "
                      "Herkunft dieses Bestands laesst sich damit nicht "
                      "belegen. Neu ausliefern mit tools/build_release.py.",
                      DATEI, type(e).__name__, e)
        if isinstance(d, dict) and d.get("commit"):
            aus = {"commit": d.get("commit", ""), "zweig": d.get("zweig", ""),
                   "sauber": d.get("sauber"), "gebaut_am": d.get("gebaut_am", ""),
                   "version": d.get("version", ""), "quelle": "archiv"}
        elif d is not None:
            log.error("%s enthaelt keinen Commit — der Stempel wurde aus "
                      "einem Baum ohne git erzeugt. Die Herkunft dieses "
                      "Bestands ist damit unbelegt.", DATEI)

    if aus["quelle"] == "unbekannt" and os.path.isdir(os.path.join(wurzel, ".git")):
        commit = _git(wurzel, "rev-parse", "HEAD")
        if commit:
            aus = {"commit": commit,
                   "zweig": _git(wurzel, "rev-parse", "--abbrev-ref", "HEAD") or "?",
                   "sauber": _git(wurzel, "status", "--porcelain") == "",
                   "gebaut_am": "", "version": "", "quelle": "git"}

    return aus


def stand(wurzel=None, frisch=False) -> dict:
    """-> {commit, kurz, zweig, sauber, gebaut_am, version, quelle}

    `quelle` ist "archiv", "git" oder "unbekannt". Wird zwischengespeichert:
    der Wert aendert sich im Lauf eines Prozesses nicht, und /healthz wird von
    Monitoring-Diensten im Minutentakt abgefragt — ein git-Aufruf je Abfrage
    waere Unfug.
    """
    wurzel = wurzel or _wurzel()
    if frisch or wurzel not in _ZWISCHENSPEICHER:
        d = _ermittle(wurzel)
        d["kurz"] = (d.get("commit") or "")[:12]
        _ZWISCHENSPEICHER[wurzel] = d
    return _ZWISCHENSPEICHER[wurzel]


def text(wurzel=None) -> str:
    """Eine Zeile fuer das Log. Nennt den Zustand, nicht nur die Zahl."""
    d = stand(wurzel)
    if d["quelle"] == "unbekannt":
        return ("Auslieferung: unbekannt — weder %s im Bestand noch ein "
                "git-Arbeitsbaum. Wer einen Stand zuordnen will, liefert mit "
                "tools/build_release.py aus." % DATEI)
    teile = ["Auslieferung: %s" % (d["kurz"] or "?")]
    if d.get("zweig"):
        teile.append("Zweig %s" % d["zweig"])
    if d.get("version"):
        teile.append("v%s" % d["version"])
    if d.get("gebaut_am"):
        teile.append("gebaut %s" % d["gebaut_am"])
    teile.append("Quelle %s" % d["quelle"])
    if d.get("sauber") is False:
        # Zwei verschiedene Aussagen, nicht eine: aus dem Archiv heisst es,
        # der Baum war BEIM BAUEN schmutzig — dann entspricht das Archiv
        # keinem Commit. Aus git heisst es, der Baum ist es JETZT, und das ist
        # auf der Entwicklungsmaschine der Normalzustand. Beides in denselben
        # Satz zu giessen waere auf einer der beiden Seiten schlicht falsch.
        teile.append("ARBEITSBAUM WAR BEIM BAUEN NICHT SAUBER — dieser Stand "
                     "entspricht keinem Commit"
                     if d["quelle"] == "archiv"
                     else "Arbeitsbaum nicht sauber (unfestgeschriebene "
                          "Aenderungen)")
    return " · ".join(teile)


def schreibe(wurzel, version: str, gebaut_am: str) -> dict:
    """Die Datei fuers Archiv erzeugen. -> der geschriebene Inhalt.

    Wird von tools/build_release.py aufgerufen, nie zur Laufzeit. Liegt
    trotzdem hier, damit Schreiber und Leser dieselbe Form benutzen — zwei
    Stellen, die ein Format teilen, laufen sonst auseinander.
    """
    d = _ermittle(wurzel)
    inhalt = {
        "commit": d.get("commit", ""),
        "zweig": d.get("zweig", ""),
        "sauber": d.get("sauber"),
        "gebaut_am": gebaut_am,
        "version": version,
    }
    with open(os.path.join(wurzel, DATEI), "w", encoding="utf-8") as fh:
        json.dump(inhalt, fh, ensure_ascii=False, indent=2)
        fh.write("\n")
    return inhalt
