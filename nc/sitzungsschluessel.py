"""nc.sitzungsschluessel — v5.2-W190: ein Zufallsschluessel fuer Sitzungs-Cookies (bot-frei).

DAS FEHLERBILD
  Das PIN-Cookie war `<zeit>.<HMAC(PIN, "nc-dashboard-pin|<zeit>")>`. Der
  Schluessel war die PIN selbst, und Zeit wie Nachricht stehen im Klartext im
  Cookie. Wer EIN solches Cookie sieht (Browser-Sicherung, Screenshot der
  Entwicklerwerkzeuge, ein geteiltes HAR), probiert offline alle PINs durch:
  eine sechsstellige PIN sind eine Million HMACs, gemessen unter zwei Sekunden.
  Danach kennt er die PIN und stellt sich Cookies mit beliebigem Zeitstempel
  selbst aus — die Ablaufzeit aus v4.0-W118 ist damit wertlos, und die
  Fehlversuchssperre sieht ihn nie.

DIE REGEL
  Der HMAC-Schluessel ist ein Zufallswert des Servers, an die PIN gebunden
  (PIN-Wechsel macht weiter jedes Cookie ungueltig). Ohne den Serverwert
  verraet ein Cookie nichts ueber die PIN. Der Wert liegt in einer Datei mit
  Rechten 0600, damit Sitzungen einen Neustart ueberleben; laesst sie sich
  nicht anlegen, gilt ein Wert nur fuer diesen Prozess — und das wird gesagt,
  weil der Betreiber sonst nach jedem Neustart grundlos neu anmelden muss.
"""

import hashlib
import hmac
import os
import re
import secrets

DATEINAME = ".nc_sitzung.key"     # *.key: weder im Git, noch im Archiv, noch im Update
_LAENGE = 32
_HEX = re.compile(rb"[0-9a-fA-F]+")
_CACHE = {}                       # pfad -> (bytes, dauerhaft)
# Warum der Schluessel nicht dauerhaft ist — der Bot nennt es im Fehlerlog.
# Bot-frei heisst: hier wird nicht geloggt, aber nichts verschluckt.
LAGE = {"grund": ""}


def _grund_melden(e):
    LAGE["grund"] = "%s: %s" % (type(e).__name__, e)


def _lesen(pfad):
    """-> bytes oder None (Datei fehlt oder taugt nicht). OSError geht durch."""
    if not os.path.exists(pfad):
        return None
    with open(pfad, "rb") as f:
        roh = f.read(4096).strip()
    if len(roh) < 2 * _LAENGE or len(roh) % 2 or not _HEX.fullmatch(roh):
        return None
    return bytes.fromhex(roh.decode("ascii"))


def _anlegen(pfad):
    """Legt die Datei exklusiv an (0600). -> bytes; wirft OSError."""
    wert = secrets.token_bytes(_LAENGE)
    fd = os.open(pfad, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    with os.fdopen(fd, "wb") as f:
        f.write(wert.hex().encode("ascii") + b"\n")
    return wert


def _laden_oder_anlegen(pfad):
    wert = _lesen(pfad)
    if wert is not None:
        return wert
    if os.path.exists(pfad):
        # Kaputt oder zu kurz: zur Seite legen. Bestehende Cookies verfallen,
        # das ist der sichere Ausgang.
        os.replace(pfad, pfad + ".kaputt")
    try:
        return _anlegen(pfad)
    except FileExistsError as e:
        # Ein paralleler Start hat sie gerade angelegt — dessen Wert gilt.
        _grund_melden(e)
        return _lesen(pfad)


def laden(pfad):
    """-> (schluessel: bytes, dauerhaft: bool). Einmal je Pfad und Prozess.
    Bei dauerhaft=False steht der Grund in LAGE["grund"]."""
    if pfad in _CACHE:
        return _CACHE[pfad]
    try:
        wert = _laden_oder_anlegen(pfad)
    except OSError as e:
        _grund_melden(e)
        wert = None
    dauerhaft = wert is not None
    if wert is None:
        wert = secrets.token_bytes(_LAENGE)
    _CACHE[pfad] = (wert, dauerhaft)
    return _CACHE[pfad]


def pin_schluessel(pin, server):
    """HMAC-Schluessel fuer das PIN-Cookie: gebunden an PIN UND Serverwert."""
    return hmac.new(server, b"nc-pin-schluessel|" + (pin or "").encode("utf-8"),
                    hashlib.sha256).digest()
