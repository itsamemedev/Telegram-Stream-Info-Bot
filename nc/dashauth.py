"""nc.dashauth — v4.1-W30: ist das Dashboard erreichbar, ohne dass jemand fragt?

════════════════════════════════════════════════════════════════════════
WARUM DIESES MODUL
════════════════════════════════════════════════════════════════════════
Die Schranke im Monolithen (`_auth_guard`) macht **gar nichts**, wenn weder
`DASHBOARD_TOKEN` noch `DASHBOARD_PIN` gesetzt ist:

    if not DASHBOARD_TOKEN and not DASHBOARD_PIN:
        return None          # jede Adresse, jeder Pfad, frei

Das ist so gewollt, solange `WEB_HOST` auf `127.0.0.1` steht — dann kommt
ohnehin nur der SSH-Tunnel durch. Steht dort etwas anderes, ist das Deck
offen im Netz: Cookies lesen, Aufnahmen löschen, Konfiguration
zurückspielen, Log mitlesen.

Die Warnung dafür gab es schon. Sie hatte drei Mängel, und zwei davon sind
genau die Fallen, die CLAUDE.md selbst benennt:

1. **Sie lief auf `log.warning`.** „Ein `log.warning` erscheint in einem
   ERROR-Log **nie**" — so blieb der Discord-Gateway-Tod monatelang
   unsichtbar. Für einen Sicherheitszustand ist das die falsche Stufe.
2. **Sie kam nur beim Start.** Wer den Bot neu startet und das Bootlog nicht
   liest, sieht sie nie wieder.
3. **Sie fragte nur nach dem Token, nicht nach dem PIN.** Ein PIN-geschütztes
   Deck ohne Token löste sie fälschlich aus — und ein Fehlalarm erzieht den
   Betreiber dazu, die Meldung zu überlesen. Das ist schlimmer als keine
   Meldung.

Dieses Modul beantwortet die Frage an EINER Stelle, mit denselben Regeln,
die die Schranke selbst benutzt.
"""

import os

# Adressen, bei denen nur der lokale Rechner (bzw. ein SSH-Tunnel) durchkommt.
LOOPBACK = ("127.0.0.1", "localhost", "::1")


def _wert(name) -> str:
    """Als Funktion gelesen, nicht als Konstante: .env wird teils erst nach
       den ersten Imports geladen (CLAUDE.md)."""
    return (os.getenv(name, "") or "").strip()


def host() -> str:
    return _wert("WEB_HOST") or "127.0.0.1"


def nur_lokal() -> bool:
    """Hört das Deck ausschliesslich auf dem eigenen Rechner?"""
    return host() in LOOPBACK


def geschuetzt() -> bool:
    """Greift die Schranke überhaupt? Genau die Bedingung aus `_auth_guard`:
       ein Token ODER ein PIN reicht. Beide fehlen heisst: frei für alle."""
    return bool(_wert("DASHBOARD_TOKEN") or _wert("DASHBOARD_PIN"))


def offen_im_netz() -> bool:
    """Der gefährliche Fall: erreichbar von aussen UND ohne jede Schranke."""
    return not nur_lokal() and not geschuetzt()


def lage():
    """-> (offen: bool, text: str). Der Text nennt den Zustand und die Abhilfe.

    Er ist bewusst lang: er landet im Fehlerlog, und dort hat der Betreiber
    keinen Kontext. Eine Zeile „Dashboard ungeschützt" ohne die zwei Wege
    heraus würde ihn nur beunruhigen, nicht handlungsfähig machen.
    """
    if not offen_im_netz():
        return False, ""
    return True, (
        "SICHERHEIT: Das Dashboard hört auf %s und hat WEDER Token NOCH PIN — "
        "die Schranke ist damit vollständig aus. Jeder, der den Port erreicht, "
        "kann Aufnahmen löschen, die Konfiguration zurückspielen und das Log "
        "mitlesen. Zwei Wege heraus: (a) DASHBOARD_PIN=<Geheimnis> oder "
        "DASHBOARD_TOKEN=<langes Geheimnis> in die .env; (b) den Port per "
        "Firewall auf die eigene Adresse beschränken "
        "(ufw allow from <DEINE-IP> to any port <PORT>). "
        "Oder WEB_HOST=127.0.0.1 setzen und über einen SSH-Tunnel zugreifen."
        % host())
