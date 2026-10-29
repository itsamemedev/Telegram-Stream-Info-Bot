"""nc.routes.schriften — v4.2-W111: die Schriften des Decks kommen vom Deck.

Bis hierher luden `templates/dashboard.html` und `templates/overlay.html`
Orbitron und JetBrains Mono von fonts.googleapis.com. Die oeffentliche Seite
macht das seit W88 nicht mehr (website/FONTS.md: jede Anfrage traegt die IP
des Besuchers zu Google, ohne Einwilligung) — das Deck und das Overlay hatten
es weiter, und das Overlay sogar bei JEDEM Chromium-Screenshot des
HTML-Overlays fuer den Restream, also im Sekundentakt vom Server aus. Auf einem
Server ohne freien Weg nach draussen kamen die Schriften dann gar nicht, und
das Sendebild lief in der Ersatzschrift.

Die Dateien liegen schon im Bestand (`website/fonts/`, OFL, 100 KB). Hier
werden sie ausgeliefert — dieselben Dateien, keine zweite Kopie, damit eine
neu gebaute Schrift an beiden Stellen gleichzeitig ankommt.

**Kein Pfad aus der Anfrage.** Der Name wird gegen eine feste Liste
nachgeschlagen; was nicht darin steht, ist 404. Ein Riegel mit
`safe_join` waere dicht, aber CodeQL sieht ihn nicht (CLAUDE.md, W98) — und
eine Liste von sechs Dateien braucht keinen Riegel, sondern ein Woerterbuch.

Ohne Token erreichbar (wie `/overlay`): die OBS-Browserquelle laeuft oft auf
einem anderen Rechner und kann keinen Token mitschicken. Die Dateien sind
oeffentlich lizenziert und verraten nichts.
"""

import os

from flask import Blueprint, Response, abort, send_from_directory

bp = Blueprint("schriften", __name__)

_VERZ = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__)))), "website", "fonts")

# Name in der URL -> Datei. Die Familie und das Gewicht stehen daneben, damit
# das CSS unten aus DERSELBEN Liste entsteht und nicht von Hand mitlaeuft.
SCHNITTE = {
    "orbitron-500.woff2": ("Orbitron", 500),
    "orbitron-700.woff2": ("Orbitron", 700),
    "orbitron-900.woff2": ("Orbitron", 900),
    "jetbrainsmono-400.woff2": ("JetBrains Mono", 400),
    "jetbrainsmono-500.woff2": ("JetBrains Mono", 500),
    "jetbrainsmono-700.woff2": ("JetBrains Mono", 700),
}

# Die Dateien aendern sich nur mit einem Update; ein Tag Cache spart die
# Anfrage bei jedem Seitenaufruf, ohne eine neue Fassung wochenlang zu
# verstecken.
_CACHE = "public, max-age=86400"


def css() -> str:
    """Die @font-face-Regeln. `font-display: swap`: Text erscheint sofort in
    der Ersatzschrift und wechselt, sobald die Datei da ist — ein Deck, das
    auf eine Schrift wartet, zeigt im Zweifel nichts."""
    teile = []
    for datei, (familie, gewicht) in SCHNITTE.items():
        teile.append(
            "@font-face{font-family:'%s';font-style:normal;font-weight:%d;"
            "font-display:swap;src:url('/fonts/%s') format('woff2')}"
            % (familie, gewicht, datei))
    return "\n".join(teile) + "\n"


@bp.route("/fonts/schriften.css")
def schriften_css():
    antwort = Response(css(), mimetype="text/css")
    antwort.headers["Cache-Control"] = _CACHE
    return antwort


@bp.route("/fonts/<name>")
def schrift(name):
    # Der Dateiname, der an send_from_directory geht, stammt aus SCHNITTE —
    # nie aus der Anfrage. `name` dient nur zum Vergleich.
    for datei in SCHNITTE:
        if datei == name:
            antwort = send_from_directory(_VERZ, datei, mimetype="font/woff2")
            antwort.headers["Cache-Control"] = _CACHE
            return antwort
    abort(404)
