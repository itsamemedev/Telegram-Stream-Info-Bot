"""nc.webserver — v4.2-W84: womit das Dashboard wirklich ausgeliefert wird,
und auf welche Adresse es sich binden darf.

════════════════════════════════════════════════════════════════════════
WARUM DIESES MODUL
════════════════════════════════════════════════════════════════════════
Zwei Entscheidungen standen bisher mitten in `run_flask()` im Monolithen und
waren dort nicht prüfbar — beide betreffen die Aussenhaut des Dienstes.

**Erstens: der Server.** `dashboard_app.run(...)` ist der
ENTWICKLUNGSSERVER von Werkzeug. Er trägt 364 Routen, optional TLS und
optional `0.0.0.0`. Werkzeug sagt selbst, dass er nicht für den Betrieb
gedacht ist, und der Grund ist nicht Stilfrage:

  * `threaded=True` heisst *ein Thread je Anfrage, unbegrenzt*. Wer den Port
    erreicht, kann Threads erzeugen, bis die Box steht — dieselbe Anfrage,
    die das Rate-Limit zählt, hat den Thread längst.
  * Kein Backlog-Management, kein sauberes Herunterfahren, keine Begrenzung
    von Kopfzeilen oder Rumpfgrösse.

`waitress` ist reines Python, ein einziges Paket ohne C-Anteil, läuft auf
Server und Windows gleichermassen und hat einen festen Thread-Pool. Keine
Route ändert sich, es ist dieselbe WSGI-App.

**Waitress kann kein TLS.** Steht `DASHBOARD_TLS_CERT`, bleibt es beim
Werkzeug-Server — der Twitch-OAuth-Rückruf braucht eine erreichbare
HTTPS-URL, und die abzuschalten wäre schlimmer als der Dev-Server. Wer
beides will, stellt einen Reverse-Proxy davor. Das Modul sagt genau das,
statt still das eine oder andere zu tun.

**Zweitens: die Bindung.** `_auth_guard` macht **gar nichts**, wenn weder
`DASHBOARD_TOKEN` noch `DASHBOARD_PIN` gesetzt ist:

    if not DASHBOARD_TOKEN and not DASHBOARD_PIN:
        return None          # jede Adresse, jeder Pfad, frei

Bei `WEB_HOST=127.0.0.1` ist das richtig — durch den SSH-Tunnel kommt
ohnehin nur der Betreiber. Bei jeder anderen Adresse ist es ein offenes
Bedienpult im Netz: Cookies lesen, Aufnahmen löschen, Konfiguration
zurückspielen, Log mitlesen.

Bisher wurde dieser Zustand nur GEMELDET (`nc/dashauth.py`, v4.1-W30), und
zwar laut und auf ERROR. Das war der richtige erste Schritt und der falsche
letzte: eine Meldung hilft nur dem, der das Log liest. Seit v4.2-W84 fällt
die Bindung stattdessen auf Loopback zurück — der gefährliche Zustand ist
dann nicht mehr erreichbar, statt beschrieben zu werden.

**Warum Rückfall statt Abbruch.** Der Bot ist nicht das Dashboard. Er nimmt
auf, sendet weiter und moderiert; ihn wegen einer Dashboard-Einstellung
sterben zu lassen, träfe genau die Arbeit, die niemand angefasst hat. Das
Deck läuft weiter, nur eben über den Tunnel.

**Und warum ein Schalter.** Wer bewusst offen binden will — hinter einer
Firewall-Regel, in einem privaten Netz —, setzt `DASHBOARD_OFFEN_ERLAUBEN=1`
und bekommt das alte Verhalten samt Warnung. Eine Sperre ohne Ausweg wird
umgangen, und ein Umgehungsweg, den der Bestand nicht kennt, ist schlimmer
als ein dokumentierter.
"""

import os

# Adressen, bei denen nur der lokale Rechner (bzw. ein SSH-Tunnel) durchkommt.
# Bewusst dieselbe Liste wie in nc/dashauth.py — wer sie hier erweitert, muss
# sie dort mit erweitern, sonst weichen Meldung und Verhalten voneinander ab.
LOOPBACK = ("127.0.0.1", "localhost", "::1")

RUECKFALL = "127.0.0.1"

# Fester Pool statt "ein Thread je Anfrage". Acht Kerne, ein Dashboard mit
# einer Handvoll Poll-Anfragen je 30 s — 8 Threads sind reichlich und deckeln
# zugleich, was eine Flut anrichten kann.
THREADS_VORGABE = 8


def _an(roh) -> bool:
    return (roh or "").strip().lower() in ("1", "true", "yes", "ja", "on")


# Die drei Variablen unten werden ABSICHTLICH woertlich mit os.getenv gelesen,
# nicht ueber einen Helfer mit Namensparameter. Zwei Gruende, und beide haben
# schon zugeschlagen:
#
#   * tools/gen_env_example.py findet nur das woertliche os.getenv("NAME").
#     Ein Helfer `_wert(name)` macht die Variable fuer den Generator
#     unsichtbar — sie stuende dann in keiner .env-Vorlage, und der Betreiber
#     erfaehrt von ihr nur, wenn er den Quelltext liest.
#   * Gelesen wird trotzdem IN einer Funktion, nie als Modul-Konstante:
#     .env wird teils erst nach den ersten Imports geladen (CLAUDE.md, W67).


def threads() -> int:
    """Grösse des Thread-Pools. -> int >= 1"""
    roh = (os.getenv("DASHBOARD_THREADS", "") or "").strip()
    if roh.isdigit() and int(roh) >= 1:
        return int(roh)
    return THREADS_VORGABE


def ist_loopback(host) -> bool:
    return (host or "").strip() in LOOPBACK


def bindung(host, geschuetzt: bool):
    """Auf welche Adresse darf sich das Deck binden?

    -> (effektiver_host, meldung).  meldung ist "" im unauffaelligen Fall,
       sonst der Text fuer das Fehlerlog — mit dem Grund UND der Abhilfe.
    """
    host = (host or "").strip() or RUECKFALL
    if ist_loopback(host) or geschuetzt:
        return host, ""

    if _an(os.getenv("DASHBOARD_OFFEN_ERLAUBEN", "")):
        return host, (
            "SICHERHEIT: Das Dashboard hört auf %s und hat WEDER Token NOCH "
            "PIN. Das ist per DASHBOARD_OFFEN_ERLAUBEN=1 ausdrücklich so "
            "gewollt — jeder, der den Port erreicht, kann Aufnahmen löschen, "
            "die Konfiguration zurückspielen und das Log mitlesen. Der Port "
            "gehört hinter eine Firewall-Regel: "
            "ufw allow from <DEINE-IP> to any port <PORT>" % host)

    return RUECKFALL, (
        "SICHERHEIT: WEB_HOST=%s, aber WEDER DASHBOARD_TOKEN NOCH "
        "DASHBOARD_PIN gesetzt — die Schranke wäre damit vollständig aus. "
        "Das Deck bindet deshalb auf %s statt offen ins Netz; der Bot läuft "
        "normal weiter (Aufnahme, Restream, Moderation sind nicht betroffen). "
        "Drei Wege zurück auf %s: (a) DASHBOARD_PIN=<Geheimnis> in die .env, "
        "(b) DASHBOARD_TOKEN=<langes Geheimnis>, (c) "
        "DASHBOARD_OFFEN_ERLAUBEN=1, wenn der Port wirklich ungeschützt "
        "offen stehen soll. Bis dahin: ssh -L %s:%s:<PORT> <user>@<host>"
        % (host, RUECKFALL, host, "<PORT>", RUECKFALL))


def waehle(tls: bool):
    """Welcher Server traegt das Dashboard? -> (name, meldung)

    name ist "waitress" oder "werkzeug"; meldung erklaert bei "werkzeug",
    WARUM es der Entwicklungsserver geblieben ist. Nie still — sonst steht
    monatelang der Dev-Server im Betrieb und niemand weiss es.
    """
    if tls:
        return "werkzeug", (
            "Dashboard-TLS ist aktiv, und waitress kann kein TLS. Das Deck "
            "läuft deshalb auf dem Werkzeug-Entwicklungsserver — der ist für "
            "den Dauerbetrieb nicht gedacht (ein Thread je Anfrage, "
            "unbegrenzt). Saubere Lösung: waitress ohne TLS laufen lassen und "
            "einen Reverse-Proxy (nginx/Caddy) davorstellen, der das "
            "Zertifikat hält.")
    if _an(os.getenv("DASHBOARD_WERKZEUG", "")):
        return "werkzeug", (
            "DASHBOARD_WERKZEUG=1 — das Deck läuft auf dem "
            "Werkzeug-Entwicklungsserver statt auf waitress. Das ist ein "
            "Notausgang für den Störungsfall, keine Betriebsart.")
    # find_spec statt `try: import waitress`: der Import waere hier ein
    # try/except, das im Erfolgsfall nichts sagt — genau die Form, die
    # tools/stillecheck.py zaehlt, und sie waere hier auch inhaltlich falsch.
    # Gefragt ist "ist das Paket da?", nicht "laedt es gerade".
    import importlib.util
    if importlib.util.find_spec("waitress") is None:
        return "werkzeug", (
            "waitress ist nicht installiert — das Deck läuft auf dem "
            "Werkzeug-Entwicklungsserver (ein Thread je Anfrage, unbegrenzt; "
            "kein sauberes Herunterfahren). Abhilfe: "
            "python3 -m pip install -r requirements.txt")
    return "waitress", ""
