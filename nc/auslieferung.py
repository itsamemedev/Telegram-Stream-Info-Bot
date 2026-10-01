"""nc.auslieferung — v4.2-W85: welcher Stand läuft hier eigentlich?

════════════════════════════════════════════════════════════════════════
WARUM DIESES MODUL
════════════════════════════════════════════════════════════════════════
Es gibt **zwei** Wege, wie Code auf den Server kommt, und dieses Modul kannte
bis v4.2-W104 nur einen. Der eine ist die ZIP über den Bestand
(`tools/deploy.sh` — Staging, Prüfung, umschwenken). Der andere ist die
**Update-Funktion** (`nc/updater.py`, bedient aus dem Deck und per Telegram),
die den Repo-Stand holt und Datei für Datei einspielt; der Betreiber benutzt
sie, und genau das hat hier gefehlt. Der Satz „das Repo ist nicht der
Deploy-Weg" stand jahrelang im Kopf dieser Datei und war falsch.

Was in beiden Fällen fehlt, ist die Gegenprobe hinterher:

    Entspricht das, was gerade läuft, überhaupt einem Commit?

Heute lässt sich das nicht beantworten. Ein Handgriff direkt auf dem Server —
eine Zeile in `bot.py` geändert, um eine Störung zu überbrücken — ist danach
unsichtbar. Beim nächsten Deploy wird er wortlos überschrieben, und der
Fehler, den er behoben hat, ist zurück. Das ist die einzige echte Lücke des
ZIP-Wegs, und sie kostet eine Datei.

Der Update-Weg hat eine zweite, teurere Lücke: er schreibt die Dateien und
startet **nichts** neu. Ein laufender Python-Prozess behält seinen Bytecode,
also liegt danach der neue Stand auf der Platte und es läuft weiter der alte —
ohne dass irgendetwas das sagt. Deshalb liest dieses Modul seit v4.2-W104 auch
`.nc_update.json`, und `nc/laufstand.py` vergleicht den Stand beim Start gegen
den Stand jetzt.

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
# v4.2-W104: was die Update-Funktion hinterlaesst (nc.updater.STATE_FILE).
# Bewusst als Literal und nicht per Import: dieses Modul laeuft in
# /healthz und darf nicht an nc.updater haengen, das Netz anfasst.
UPDATE_DATEI = ".nc_update.json"

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
    Absicht: erst der Update-Stand, dann die ausgelieferte Datei, dann git.

    **Warum der Update-Stand VORNE steht (v4.2-W104).** Wer die
    Update-Funktion benutzt, hat danach einen neueren Stand auf der Platte als
    den, den `AUSLIEFERUNG.json` vom letzten ZIP-Deploy nennt — der Stempel
    des Archivs ist dann veraltet, und ihn zu bevorzugen hiesse, dem
    Betreiber eine Fassung zu melden, die seit Wochen nicht mehr auf der
    Platte liegt. Die Datei des Archivs faellt dabei nicht weg: sie bleibt die
    Antwort, solange kein Update gelaufen ist.

    Auf dem Server gibt es kein .git — dort sind die beiden Dateien die
    einzige Wahrheit. Auf der Entwicklungsmaschine gibt es git, und dann ist
    git das Aktuellere: die Datei stammt vom letzten `build_release`, der
    Arbeitsbaum ist weiter.

    Dass die Datei FEHLT, ist der Normalfall (Start aus dem Repo) und bleibt
    still. Dass sie da, aber kaputt ist, nicht: sonst wuerde daraus "Herkunft
    unbekannt", und der Betreiber glaubte, er habe von Hand ausgeliefert,
    waehrend in Wahrheit das Archiv beschaedigt ist.
    """
    aus = dict(UNBEKANNT)

    # v4.2-W104: der Stand, den die Update-Funktion eingespielt hat. Er ist
    # das Jüngste, was auf der Platte liegt, wenn er existiert.
    upd = os.path.join(wurzel, UPDATE_DATEI)
    if os.path.isfile(upd):
        u = None
        try:
            with open(upd, encoding="utf-8") as fh:
                u = json.load(fh)
        except (OSError, ValueError) as e:
            # Nicht still: ist diese Datei kaputt, meldet der Bot den Stand
            # des ARCHIVS weiter, obwohl per Update längst etwas anderes
            # draufliegt — eine falsche Auskunft statt keiner.
            log.error("%s ist vorhanden, aber nicht lesbar (%s: %s) — der per "
                      "Update eingespielte Stand laesst sich damit nicht "
                      "belegen; gemeldet wird der Stand des Archivs.",
                      UPDATE_DATEI, type(e).__name__, e)
        if isinstance(u, dict) and u.get("sha"):
            aus = {"commit": u.get("sha", ""), "zweig": u.get("branch", ""),
                   "sauber": True, "gebaut_am": u.get("date", ""),
                   "version": "", "quelle": "update"}

    pfad = os.path.join(wurzel, DATEI)

    if aus["quelle"] == "unbekannt" and os.path.isfile(pfad):
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

    `quelle` ist "update", "archiv", "git" oder "unbekannt". Wird
    zwischengespeichert, weil /healthz von Monitoring-Diensten im Minutentakt
    abgefragt wird — ein git-Aufruf je Abfrage waere Unfug.

    **v4.2-W104: was hier zwischengespeichert wird, ist die PLATTE.** Der
    alte Kommentar sagte "der Wert aendert sich im Lauf eines Prozesses
    nicht". Fuer den ZIP-Weg stimmt das; mit der Update-Funktion nicht — sie
    schreibt `.nc_update.json` waehrend der Prozess laeuft. Je nachdem, ob die
    erste Abfrage vor oder nach einem Update kam, beschreibt der Wert also den
    laufenden Prozess ODER den Bestand auf der Platte.

    Aufgeloest wird das nicht hier, sondern daneben: `nc/laufstand.py`
    vergleicht den beim Start gemerkten Stand gegen den jetzigen und sagt, ob
    beide noch zusammenpassen. Diese Funktion beantwortet "was liegt da", der
    Laufstand "laeuft es auch".
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
