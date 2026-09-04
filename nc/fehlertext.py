"""nc.fehlertext — v4.1-W30: was eine Fehlermeldung nach aussen tragen darf.

════════════════════════════════════════════════════════════════════════
WARUM DIESES MODUL
════════════════════════════════════════════════════════════════════════
Über zweihundert Stellen antworten mit `jsonify(ok=False, error=str(e))`.
CodeQL meldet das als `py/stack-trace-exposure`, und bei jeder Verschiebung
in einen Blueprint erneut als „neu" — fünfmal habe ich in einer PR
vorgerechnet, dass die Bilanz stimmt. Das ist die Antwort auf die Meldung,
nicht auf die Sache.

**Ob es ein echtes Problem ist, hängt am Betrieb.** Die Schranke des
Dashboards macht gar nichts, wenn weder `DASHBOARD_TOKEN` noch
`DASHBOARD_PIN` gesetzt ist (siehe nc/dashauth.py). Steht `WEB_HOST` dann
nicht auf dem Loopback, geht jede dieser Meldungen an jeden, der den Port
erreicht — mitsamt Dateipfaden, Datenbank-Interna und gelegentlich dem
Wortlaut einer Anfrage an eine fremde API.

Der Betreiber ist zugleich der einzige gewollte Leser. Ihm den Grund
wegzunehmen wäre eine Verschlechterung: „interner Fehler" ist in einem
Ein-Personen-Betrieb keine Sicherheit, sondern eine Sackgasse.

Deshalb kein Entweder-Oder, sondern:

* **Der Wortlaut geht ins Log**, wo er hingehört — vollständig, mit Typ.
* **Nach aussen geht eine gekürzte, gesäuberte Fassung**: Pfade und
  Zugangsdaten raus, Länge begrenzt.

Damit bleibt die Meldung für den Betreiber brauchbar, und das, was sie
verräterisch machte, ist weg.
"""

import logging
import os
import re

log = logging.getLogger("TikTokBot")

# So viel Text ist genug, um zu verstehen was los ist. Alles darüber ist
# meist ein Stacktrace oder eine zurückgegebene HTML-Seite.
MAX = 200

# Absolute Pfade verraten die Verzeichnisstruktur des Servers und tauchen in
# fast jedem Datei- und ffmpeg-Fehler auf.
_PFAD = re.compile(r"(/(?:home|root|mnt|srv|var|etc|opt|tmp)/[^\s'\"]+)")

# Was nach Zugangsdaten aussieht. Bewusst grob: lieber ein zu viel
# geschwaerztes Wort als ein durchgerutschter Schluessel. Die Namen decken
# sich mit denen, die nc/logsafe.py fuer die Kommandozeilen redigiert.
_GEHEIM = re.compile(
    r"(?i)\b(token|key|secret|password|passwd|pin|cookie|authorization|bearer|sig)"
    r"\s*[=:]\s*[^\s,;'\"&]+")

# Stream-Keys und lange Zufallsketten, auch ohne Namen davor.
_LANGES_GEHEIMNIS = re.compile(r"\b[A-Za-z0-9_-]{32,}\b")


def saeubern(text: str) -> str:
    """Pfade, Zugangsdaten und lange Zufallsketten schwärzen, dann kürzen."""
    t = (text or "").strip().replace("\n", " ")
    t = _GEHEIM.sub(lambda m: m.group(1) + "=<geschwärzt>", t)
    t = _PFAD.sub(lambda m: "<" + os.path.basename(m.group(1)) + ">", t)
    t = _LANGES_GEHEIMNIS.sub("<geschwärzt>", t)
    if len(t) > MAX:
        t = t[:MAX - 1] + "…"
    return t


def nach_aussen(e, wo: str = "") -> str:
    """Der Text für eine API-Antwort. Der Wortlaut geht ins Log.

    `wo` benennt die Stelle (Route, Funktion) und steht nur im Log — nach
    aussen sagt sie nichts, was der Aufrufer nicht ohnehin weiss.
    """
    art = type(e).__name__
    roh = str(e)
    log.warning("Fehler in %s: %s: %s", wo or "?", art, roh)
    sauber = saeubern(roh)
    # Der Typ bleibt drin: er ist die Hälfte der Diagnose ("OperationalError"
    # sagt Datenbank, "TimeoutError" sagt Netz) und verrät nichts über den
    # Bestand.
    return "%s: %s" % (art, sauber) if sauber else art
