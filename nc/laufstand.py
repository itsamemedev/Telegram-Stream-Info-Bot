"""nc.laufstand — laeuft der Code, der auf der Platte liegt? (v4.2-W104)

**Der Anlass.** Der Betreiber hat am 01.10. korrigiert: „auf dem Server laeuft
die repo dank der update Funktion". Davor stand in `CLAUDE.md` und im Kopf von
`nc/auslieferung.py` als Tatsache, ausgeliefert werde per ZIP und das Repo sei
„nicht der Deploy-Weg" — und genau dieser Satz hat eine Welle lang falsch
beraten, mich eingeschlossen.

Der eigentliche Befund steckt eine Ebene tiefer. `nc.updater` schreibt die
Dateien und **startet nichts neu** — ein laufender Python-Prozess behaelt
seinen Bytecode, also liegt nach einem Update der neue Stand auf der Platte
und es laeuft weiter der alte.

Der Neustart selbst ist gut gebaut und bleibt, wie er ist: das Deck zeigt den
Knopf „Dienst neu starten", sobald `restart_needed` gesetzt ist, und
`/api/update/restart` fuehrt `UPDATE_RESTART_CMD` aus — oder nennt, wenn die
Variable bewusst leer ist, den Befehl zum Selbst-Absetzen. Das Opt-in ist eine
Sicherheitsentscheidung und keine Luecke.

Die Luecke ist die ZEIT DANACH. Der Hinweis erscheint EINMAL, als Toast und
Knopf direkt nach dem Lauf. Wer den Tab schliesst, per Telegram aktualisiert
oder einfach abgelenkt wird, hat danach keine Stelle mehr, die den Zustand
nennt: `/healthz` und `/api/version` lasen `AUSLIEFERUNG.json` beziehungsweise
`git` und kannten den Update-Weg gar nicht, melden also unveraendert den Stand
von vorher. Der Bestand auf der Platte und der laufende Prozess driften
auseinander, und nichts misst das.

Das Fehlerbild ist damit genau das teuerste, das dieses Projekt kennt: es
faellt nichts, es meldet sich nichts, es wird nur nichts. Im Log steht das
alte Verhalten, im Deck die alte Fassung, und die naheliegende Deutung — „das
Update hat nicht funktioniert" — ist falsch.

**Was dieses Modul tut.** Es vergleicht den Stand, mit dem der Prozess
GESTARTET ist, gegen den Stand, der JETZT auf der Platte liegt. Weichen beide
ab, ist der laufende Code veraltet, und der Betreiber braucht einen Neustart.

**Was es ausdruecklich NICHT tut: Fehlalarm.** Ist der Stand auf der Platte
unbekannt — kein Update-Weg benutzt, kein `.nc_update.json`, ein Checkout ohne
`git` —, dann lautet die Antwort „weiss ich nicht" und nicht „veraltet". Eine
Meldung, die auf jeder Entwicklungsmaschine rot ist, erzieht dazu, sie auch
auf dem Server zu uebersehen; dieselbe Begruendung steht seit W85 im Kopf von
`nc/auslieferung.py`, und sie gilt hier genauso.

Reine Rechnung ueber zwei Zeichenketten: so ist die Entscheidung ohne Update,
ohne Netz und ohne Neustart pruefbar.
"""

# Die Lagen, die herauskommen koennen. Ausdruecklich benannt und nicht als
# Wahrheitswert: „ich weiss es nicht" ist etwas anderes als „alles in
# Ordnung", und ein Boolean kann das nicht sagen (Lehre aus W102,
# nc/resolvergrund.LAGE_OK).
AKTUELL = "aktuell"            # Prozess und Platte tragen denselben Stand
VERALTET = "veraltet"          # auf der Platte liegt ein NEUERER Stand
UNBEKANNT = "unbekannt"        # einer der beiden Staende ist nicht ermittelbar

# Der Dienstname steht im Bestand schon zweimal so (nc/dbrestore.py,
# nc/telegramfehler.py) und ebenso im `hint` von /api/update/restart. Er
# gehoert hierher, damit die Abhilfe einen Befehl NENNEN kann — ausgefuehrt
# wird hier nichts, das bleibt beim Opt-in von UPDATE_RESTART_CMD.
DIENST_VORGABE = "tiktok-bot"


def befehl(dienst=None) -> str:
    """Der Neustart-Befehl, den der Betreiber kopieren kann."""
    return "sudo systemctl restart %s" % (dienst or DIENST_VORGABE)


def vergleich(start_sha, platte_sha, dienst=None) -> dict:
    """{lage, start, platte, text, abhilfe} — ohne Uhr, ohne Dateizugriff.

    `start_sha` ist der Stand, mit dem der Prozess gestartet ist (beim Start
    EINMAL gemerkt — danach aendert ihn nichts mehr, das ist der Punkt).
    `platte_sha` ist der Stand, der jetzt auf der Platte liegt.
    """
    start = (start_sha or "").strip()
    platte = (platte_sha or "").strip()
    if not start or not platte:
        lage = UNBEKANNT
    elif start == platte:
        lage = AKTUELL
    else:
        lage = VERALTET
    aus = {"lage": lage, "start": start[:12], "platte": platte[:12],
           "text": "", "abhilfe": ""}
    if lage == VERALTET:
        aus["text"] = ("Auf der Platte liegt ein NEUERER Stand (%s) als der, "
                       "mit dem dieser Prozess gestartet ist (%s). Ein "
                       "laufender Python-Prozess behaelt seinen Bytecode — das "
                       "Update ist also eingespielt und wirkt NICHT."
                       % (platte[:12], start[:12]))
        aus["abhilfe"] = befehl(dienst)
    elif lage == UNBEKANNT:
        # Kein Fehler und keine Warnung: so sieht eine Entwicklungsmaschine
        # aus, und so sieht ein Bestand aus, der nie ueber den Update-Weg
        # kam. Gesagt wird es trotzdem, damit niemand die Null fuer ein
        # „alles gut" nimmt (Lehre aus W97, log_wartend = -1 statt 0).
        aus["text"] = ("Der Stand auf der Platte ist nicht ermittelbar — kein "
                       "Update-Weg benutzt und kein git. Dann laesst sich "
                       "nicht sagen, ob der laufende Code der aktuelle ist.")
    return aus


def veraltet(start_sha, platte_sha) -> bool:
    """Kurzform fuer die eine Frage, die einen Alarm rechtfertigt."""
    return vergleich(start_sha, platte_sha)["lage"] == VERALTET
