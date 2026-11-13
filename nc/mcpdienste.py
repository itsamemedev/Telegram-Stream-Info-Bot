"""nc.mcpdienste — v5.6-W198: MCP-Server im Deck führen, prüfen und ausgeben (bot-frei).

════════════════════════════════════════════════════════════════════════
DER ANLASS
════════════════════════════════════════════════════════════════════════
Der Betreiber: „Ich hätte gern den Tab im Dashboard, um MCPs verwalten zu
können." Seit v5.6-W197 zeigt llama-server (ik_llama.cpp) mit
`--webui llamacpp` die Chat-Oberfläche mit dem Reiter „MCP". Die speichert
ihre Server aber im BROWSER — das Deck kann sie dort nicht setzen, und was
dort steht, kennt der Server nicht.

Was das Deck kann: die Liste an EINER Stelle auf dem Server führen
(app_config, Schlüssel "mcp.server" — kein Schemawechsel), jeden Eintrag
ECHT prüfen (MCP Streamable HTTP: initialize, notifications/initialized,
tools/list) und als Datei ausgeben, die sich in einen Client übernehmen
lässt. lage() sagt dazu, ob llama-server überhaupt mit dieser Oberfläche
und dem CORS-Proxy läuft — und wenn nicht, was in die .env gehört.

════════════════════════════════════════════════════════════════════════
WAS HIER GILT
════════════════════════════════════════════════════════════════════════
* DER TOKEN VERLÄSST DEN SERVER NIE — nicht in liste(), nicht im Log, nicht
  in einem Grund. Auch dann nicht, wenn ein Fremdserver ihn in seiner
  Fehlerseite zurückspiegelt: das ganze Ergebnis läuft durch _schwaerzen.
  Einzige Ausnahme ist export(mit_token=True), ausdrücklich verlangt.
* KEINER UMLEITUNG FOLGEN. urllib folgt einem 301/302 und nimmt den
  Authorization-Kopf an das neue Ziel mit — ein Server, der auf einen
  fremden Rechner umleitet, bekäme den Token. http.client folgt nie; eine
  Umleitung ist ein Befund mit Abhilfe. Nebenbei kennt http.client keine
  Proxy-Variablen der Umgebung: ein MCP-Server auf 127.0.0.1 wird direkt
  gefragt und nicht über einen Proxy, der ihn nicht erreicht.
* STRENG LESEN, BEVOR GESCHRIEBEN WIRD. cfgstore.get() liefert bei einem
  Datenbankfehler die Vorgabe. Mit [] als Vorgabe hätte das Anlegen eines
  Servers während einer gesperrten Datenbank alle anderen gelöscht —
  dieselbe Klasse wie _find_orphans in W91 („ich weiß nicht, was in der
  Datenbank steht" heißt nicht „es steht nichts darin"). cfgstore.lesen()
  wirft statt zu raten, und die Route antwortet 503.
* EINE FRIST FÜR DEN GANZEN TEST, nicht je Socket-Operation. Ein
  Socket-Zeitlimit gilt je recv(); ein Server, der alle neun Sekunden ein
  SSE-Keepalive schickt, hielte eine Deck-Anfrage sonst beliebig lange fest.
* DER RUMPF IST GEDECKELT (MAX_RUMPF). Ein fremder Server darf den Bot nicht
  mit Speicher füllen — auch nicht mit einem SSE-Strom, der nie endet, oder
  mit einer einzigen Zeile ohne Umbruch.
"""

import http.client
import json
import logging
import os
import re
import secrets
import socket
import ssl
import threading
import time
import unicodedata
from datetime import datetime, timezone
from urllib.parse import quote, urlsplit

from nc import cfgstore as _cfgstore
from nc import fehlertext as _fehlertext
from nc import version as _version

log = logging.getLogger("TikTokBot")

SCHLUESSEL = "mcp.server"
UNIT_PFAD = "/etc/systemd/system/llama-server.service"
LLAMA_VORGABE = "http://127.0.0.1:8080"
# Die Fassung, die wir anbieten. Der Server antwortet mit der, die er
# spricht; die geht danach als MCP-Protocol-Version-Kopf mit (Pflicht seit
# 2025-06-18 für jede Anfrage nach initialize).
PROTOKOLL = "2025-06-18"
MAX_RUMPF = 2 * 1024 * 1024
MAX_SEITEN = 5
MAX_SERVER = 50
MAX_WERKZEUGE = 200
GESCHWAERZT = "<geschwärzt>"
_PROTO = re.compile(r"[0-9A-Za-z.-]{1,40}")
# Mcp-Session-Id: laut Spezifikation nur sichtbare ASCII-Zeichen. Alles
# andere wäre ein Kopfzeilen-Einschub in die nächste Anfrage.
_SITZUNG = re.compile(r"[\x21-\x7e]{1,200}")
_SPERRE = threading.Lock()


def _t(s):
    """Markiert Benutzertext für tools/i18n_extract.py (MARKIERT). Übersetzt
    wird in der Route (nc/routes/mcp.py): die Sprache steht erst je Anfrage
    fest, und ein Grund mit Platzhaltern wird dort NACH der Übersetzung
    gefüllt — sonst wäre er als Katalogschlüssel wertlos."""
    return s


# ── Gründe, die eine Eingabe ablehnen (statisch, ohne Platzhalter) ──────────
KEIN_OBJEKT = _t("Erwartet ein JSON-Objekt.")
UNBEKANNT = _t("Unbekannter MCP-Server.")
ZU_VIELE = _t("Höchstens 50 MCP-Server — erst einen löschen.")
NAME_FEHLT = _t("Der Name fehlt.")
NAME_TEXT = _t("Der Name muss Text sein.")
NAME_LANG = _t("Der Name ist zu lang (höchstens 60 Zeichen).")
NAME_ZEICHEN = _t("Der Name enthält Steuerzeichen.")
NAME_VERGEBEN = _t("Diesen Namen trägt schon ein anderer MCP-Server.")
URL_FEHLT = _t("Die Adresse fehlt.")
URL_TEXT = _t("Die Adresse muss Text sein.")
URL_LANG = _t("Die Adresse ist zu lang (höchstens 500 Zeichen).")
URL_ZEICHEN = _t("Die Adresse enthält Leer- oder Steuerzeichen.")
URL_SCHEMA = _t("Nur http:// und https:// — der Verbindungstest spricht MCP über HTTP.")
URL_HOST = _t("Die Adresse nennt keinen Rechner.")
URL_PORT = _t("Ungültiger Port in der Adresse.")
URL_PUNYCODE = _t("Rechnername mit Sonderzeichen — bitte als Punycode (xn--…) eintragen.")
URL_ZUGANG = _t("Zugangsdaten gehören nicht in die Adresse (user:pass@) — dort stünden sie "
                "in jeder Liste und jedem Export. Den Token ins Feld „Token“ eintragen.")
TOKEN_TEXT = _t("Der Token muss Text sein.")
TOKEN_LANG = _t("Der Token ist zu lang (höchstens 4096 Zeichen).")
TOKEN_ZEICHEN = _t("Der Token enthält Leer- oder Steuerzeichen.")
AKTIV_WERT = _t("„aktiv“ muss true oder false sein.")
NOTIZ_TEXT = _t("Die Notiz muss Text sein.")
NOTIZ_LANG = _t("Die Notiz ist zu lang (höchstens 200 Zeichen).")
NOTIZ_ZEICHEN = _t("Die Notiz enthält Steuerzeichen.")

# ── Gründe eines gescheiterten Verbindungstests — jeder MIT Abhilfe ─────────
# „HTTP 403" allein hat schon einmal wochenlang niemandem geholfen
# (nc/resolvergrund.py). Platzhalter füllt die Route nach der Übersetzung.
ZEIT = _t("Zeitüberschreitung nach {s} s — der Server antwortet nicht. Läuft er, und ist die "
          "Adresse von diesem Rechner aus erreichbar (Firewall, Tunnel)?")
VERWEIGERT = _t("Verbindung verweigert ({ziel}) — dort lauscht kein Server. Läuft der "
                "MCP-Server, und stimmt der Port?")
NAME_UNAUFLOESBAR = _t("Rechnername nicht auflösbar ({ziel}) — Tippfehler in der Adresse, oder "
                       "dieser Rechner kennt den Namen nicht (DNS).")
TLS_ZERTIFIKAT = _t("TLS-Zertifikat nicht vertrauenswürdig ({ziel}) — abgelaufen, selbst signiert "
                    "oder für einen anderen Namen. Zertifikat erneuern oder die Adresse so "
                    "eintragen, wie sie im Zertifikat steht.")
TLS = _t("TLS-Fehler ({ziel}) — spricht der Server wirklich https? Sonst die Adresse mit "
         "http:// eintragen.")
NETZ = _t("Netzwerkfehler ({ziel}): {art} — ist der Rechner von hier aus erreichbar "
          "(Route, Firewall, Tunnel)?")
KEIN_HTTP = _t("Die Antwort ist kein gültiges HTTP ({art}) — lauscht dort ein Webserver? "
               "Spricht er https, die Adresse mit https:// eintragen.")
UMLEITUNG = _t("HTTP {code}: Umleitung nach {ziel} — die Zieladresse direkt eintragen. Einer "
               "Umleitung wird nicht gefolgt, damit der Token nicht an einen anderen Server geht.")
ANMELDUNG = _t("HTTP {code}: Der Server lehnt die Anmeldung ab — den Token prüfen (im Feld "
               "„Token“, ohne „Bearer “ davor).")
ANMELDUNG_OHNE = _t("HTTP {code}: Der Server verlangt eine Anmeldung, für diesen Eintrag ist aber "
                    "kein Token gesetzt — Token eintragen.")
KEIN_ENDPUNKT = _t("HTTP {code}: Kein Streamable-HTTP-Endpunkt unter dieser Adresse — oft endet sie "
                   "auf /mcp. Reine SSE-Server (alt) werden nicht unterstützt.")
SERVERFEHLER = _t("HTTP {code}: Fehler im MCP-Server — dessen Log ansehen. Antwort: {auszug}")
ABGELEHNT = _t("HTTP {code}: Der Server lehnt die Anfrage ab. Antwort: {auszug}")
KEIN_MCP = _t("Antwort mit Inhaltstyp „{typ}“ statt JSON oder SSE — ist das ein MCP-Endpunkt? "
              "Oft endet die Adresse auf /mcp.")
KEIN_JSON = _t("Die Antwort auf „{methode}“ ist kein gültiges JSON ({fehler}) — spricht der "
               "Server MCP? Die Adresse muss auf den MCP-Endpunkt zeigen.")
OHNE_ERGEBNIS = _t("Die Antwort auf „{methode}“ trägt kein Ergebnis-Objekt — der Server hält "
                   "sich nicht an JSON-RPC.")
OHNE_ANTWORT = _t("Der Server hat auf „{methode}“ nicht geantwortet (der Strom endete ohne "
                  "Antwort) — Log des MCP-Servers ansehen.")
RPC_FEHLER = _t("Der Server meldet bei „{methode}“ den Fehler {code}: {meldung}")
ZU_GROSS = _t("Antwort größer als {mb} MB — abgebrochen, damit ein fremder Server den Bot nicht "
              "mit Speicher füllt.")
SITZUNG_UNGUELTIG = _t("Ungültige Mcp-Session-Id vom Server — er hält sich nicht an das Protokoll.")
WERKZEUGLISTE = _t("tools/list lieferte keine Werkzeugliste — der Server hält sich nicht an MCP.")

# ── Abhilfe der llama-server-Lage (statisch) ────────────────────────────────
WEBUI_KEINE_UNIT = _t("Kein llama-server-Dienst gefunden — das lokale LLM mit "
                      "„sudo bash tools/ikllama.sh“ einrichten (LLM_WEBUI=llamacpp ist die Vorgabe).")
WEBUI_UNLESBAR = _t("Die Unit von llama-server ist nicht lesbar (Rechte) — ob die Oberfläche "
                    "läuft, lässt sich von hier nicht sagen.")
WEBUI_OHNE_START = _t("Die Unit von llama-server hat keine ExecStart-Zeile — mit "
                      "„sudo bash tools/ikllama.sh“ neu schreiben lassen.")
WEBUI_FEHLT = _t("Die Oberfläche mit dem Reiter „MCP“ läuft nicht: LLM_WEBUI=llamacpp in die "
                 ".env, dann „sudo bash tools/ikllama.sh“.")
WEBUI_PROXY_AUS = _t("Für MCP-Server ohne CORS-Freigabe: LLM_WEBUI_MCP_PROXY=1 in die .env, dann "
                     "„sudo bash tools/ikllama.sh“. Der Proxy lässt llama-server fremde Adressen "
                     "abrufen — nur bei Bedarf einschalten.")


class Abgelehnt(ValueError):
    """Eine Eingabe, die nicht gespeichert wird — `grund` steht für das Deck."""

    def __init__(self, grund):
        super().__init__(grund)
        self.grund = grund


class BestandUnbekannt(RuntimeError):
    """Der gespeicherte Bestand ist unlesbar. Dann wird NICHT geschrieben."""


class Unbekannt(LookupError):
    """Keine MCP-Server-Kennung dieses Namens."""


class _Abbruch(Exception):
    """Ein Prüfschritt ist gescheitert: Vorlage, Werte für die Platzhalter, HTTP-Status."""

    def __init__(self, vorlage, http=None, **werte):
        super().__init__(vorlage)
        self.vorlage = vorlage
        self.http = http
        self.werte = werte


def _jetzt():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


# ── Bestand ─────────────────────────────────────────────────────────────────

def _laden():
    """Der gespeicherte Bestand als Liste von dicts (mit Token). Wirft bei
    einem Datenbankfehler — nie eine leere Liste aus Verlegenheit."""
    roh = _cfgstore.lesen(SCHLUESSEL, [])
    if not isinstance(roh, list):
        raise BestandUnbekannt("app_config[%s] ist keine Liste, sondern %s"
                               % (SCHLUESSEL, type(roh).__name__))
    gut = [dict(s) for s in roh
           if isinstance(s, dict) and isinstance(s.get("id"), str)
           and isinstance(s.get("name"), str) and isinstance(s.get("url"), str)]
    if len(gut) != len(roh):
        log.warning("MCP-Server: %d unlesbare Einträge in app_config[%s] übersprungen — "
                    "der nächste Schreibvorgang verwirft sie.", len(roh) - len(gut), SCHLUESSEL)
    return gut


def _schreiben(bestand):
    _cfgstore.set_(SCHLUESSEL, bestand)


def _oeffentlich(s):
    """Der Eintrag für Antworten — als Erlaubnisliste, nicht als „alles außer
    token": ein Feld, das später dazukommt, geht so nicht ungeprüft hinaus."""
    aus = {k: s.get(k) for k in ("id", "name", "url", "notiz", "geaendert", "letzter_test")}
    aus["aktiv"] = bool(s.get("aktiv", True))
    aus["notiz"] = aus["notiz"] or ""
    aus["token_gesetzt"] = bool(s.get("token"))
    return aus


def liste():
    """Alle Server ohne Token, stattdessen `token_gesetzt`. Wirft bei Datenbankfehler."""
    return [_oeffentlich(s) for s in _laden()]


def _eintrag(sid):
    for s in _laden():
        if s["id"] == sid:
            return s
    raise Unbekannt(str(sid)[:16])


# ── Eingaben prüfen ─────────────────────────────────────────────────────────

def _hat_steuerzeichen(s, erlaubt="") -> bool:
    # Kategorie C* statt nur Cc: auch Format-Zeichen (Cf) wie die Bidi-Umkehr
    # U+202E — ein Name, der sich im Deck anders liest, als er heißt.
    return any(unicodedata.category(c)[0] == "C" and c not in erlaubt for c in s)


def _name(wert):
    if wert is None:
        raise Abgelehnt(NAME_FEHLT)
    if not isinstance(wert, str):
        raise Abgelehnt(NAME_TEXT)
    n = wert.strip()
    if not n:
        raise Abgelehnt(NAME_FEHLT)
    if len(n) > 60:
        raise Abgelehnt(NAME_LANG)
    if _hat_steuerzeichen(n):
        raise Abgelehnt(NAME_ZEICHEN)
    return n


def _url(wert):
    if wert is None:
        raise Abgelehnt(URL_FEHLT)
    if not isinstance(wert, str):
        raise Abgelehnt(URL_TEXT)
    u = wert.strip()
    if not u:
        raise Abgelehnt(URL_FEHLT)
    if len(u) > 500:
        raise Abgelehnt(URL_LANG)
    if any(c.isspace() for c in u) or _hat_steuerzeichen(u):
        raise Abgelehnt(URL_ZEICHEN)
    teile = urlsplit(u)
    # Erlaubnisliste statt „irgendein Schema": file://, javascript: oder
    # gopher:// haben in einem Verbindungstest und in einem Export für einen
    # fremden Client nichts zu suchen.
    if teile.scheme not in ("http", "https"):
        raise Abgelehnt(URL_SCHEMA)
    # Zugangsdaten im Host-Teil stünden in liste(), im Log und im Export —
    # genau dort, wo der Token nie hin darf.
    if "@" in teile.netloc:
        raise Abgelehnt(URL_ZUGANG)
    if not teile.hostname:
        raise Abgelehnt(URL_HOST)
    if not teile.hostname.isascii():
        raise Abgelehnt(URL_PUNYCODE)
    # .port wirft erst beim Lesen (ausserhalb 0–65535, keine Zahl) — hier,
    # nicht spaeter im Verbindungstest, wo es nach einem Fehler des Bots
    # aussaehe. Port 0 laesst sich nicht verbinden.
    try:
        port = teile.port
    except ValueError:
        raise Abgelehnt(URL_PORT) from None
    if port == 0:
        raise Abgelehnt(URL_PORT)
    return u


def _token(wert):
    """None und "" heißen löschen. Ein vorangestelltes „Bearer " wird
    abgenommen — sonst ginge „Bearer Bearer …" hinaus und der Server sagte 401."""
    if wert is None:
        wert = ""
    if not isinstance(wert, str):
        raise Abgelehnt(TOKEN_TEXT)
    t = wert.strip()
    if t[:7].lower() == "bearer ":
        t = t[7:].strip()
    if len(t) > 4096:
        raise Abgelehnt(TOKEN_LANG)
    # Ein Zeilenumbruch im Token wäre eine zusätzliche Kopfzeile in der
    # Anfrage (Header-Einschub); http.client lehnt das erst beim Senden ab.
    if any(c.isspace() for c in t) or _hat_steuerzeichen(t):
        raise Abgelehnt(TOKEN_ZEICHEN)
    return t


def _schalter(wert):
    if isinstance(wert, bool):
        return wert
    if isinstance(wert, int) and wert in (0, 1):
        return bool(wert)
    if isinstance(wert, str) and wert.strip().lower() in ("true", "1", "ja", "false", "0", "nein"):
        return wert.strip().lower() in ("true", "1", "ja")
    raise Abgelehnt(AKTIV_WERT)


def _notiz(wert):
    if wert is None:
        wert = ""
    if not isinstance(wert, str):
        raise Abgelehnt(NOTIZ_TEXT)
    n = wert.strip()
    if len(n) > 200:
        raise Abgelehnt(NOTIZ_LANG)
    if _hat_steuerzeichen(n, erlaubt="\n\t"):
        raise Abgelehnt(NOTIZ_ZEICHEN)
    return n


def _anwenden(alt, daten, neu_anlegen, bestand):
    """Die Felder aus `daten` auf eine Kopie von `alt` legen. Wirft Abgelehnt."""
    neu = dict(alt)
    if neu_anlegen or "name" in daten:
        neu["name"] = _name(daten.get("name"))
        andere = {s["name"].casefold() for s in bestand if s["id"] != alt["id"]}
        # Der Name ist der Schlüssel im Export ({"mcpServers": {name: …}}):
        # zwei gleiche Namen hießen, dass einer davon dort still verschwindet.
        if neu["name"].casefold() in andere:
            raise Abgelehnt(NAME_VERGEBEN)
    if neu_anlegen or "url" in daten:
        neu["url"] = _url(daten.get("url"))
    if "token" in daten:
        neu["token"] = _token(daten.get("token"))
    if "aktiv" in daten:
        neu["aktiv"] = _schalter(daten.get("aktiv"))
    if "notiz" in daten:
        neu["notiz"] = _notiz(daten.get("notiz"))
    # Ein Test gegen eine andere Adresse oder mit einem anderen Token sagt
    # über diesen Eintrag nichts mehr — stehen gelassen, läse er sich wie ein
    # Befund über die neue Lage.
    if neu.get("url") != alt.get("url") or neu.get("token", "") != alt.get("token", ""):
        neu["letzter_test"] = None
    return neu


def _neue_id(bestand):
    vergeben = {s["id"] for s in bestand}
    sid = secrets.token_hex(4)
    while sid in vergeben:
        sid = secrets.token_hex(4)
    return sid


def speichern(daten, sid=None):
    """Anlegen (sid None) oder ändern. -> (True, öffentlicher Eintrag) | (False, Grund).

    Beim Ändern gilt: ein weggelassenes Feld bleibt, wie es ist — auch der
    Token; `"token": ""` löscht ihn. Ein Datenbankfehler wirft (die Route
    antwortet 503), statt als Ablehnung auszusehen."""
    if not isinstance(daten, dict):
        log.warning("MCP-Server: Eingabe abgelehnt — kein JSON-Objekt (%s).", type(daten).__name__)
        return False, KEIN_OBJEKT
    with _SPERRE:
        bestand = _laden()
        if sid is None:
            if len(bestand) >= MAX_SERVER:
                log.warning("MCP-Server: %d Einträge, kein weiterer angelegt.", len(bestand))
                return False, ZU_VIELE
            alt = {"id": _neue_id(bestand), "name": "", "url": "", "token": "",
                   "aktiv": True, "notiz": "", "letzter_test": None}
        else:
            alt = next((s for s in bestand if s["id"] == sid), None)
            if alt is None:
                log.info("MCP-Server %r: unbekannte Kennung — nichts geändert.", str(sid)[:16])
                return False, UNBEKANNT
        try:
            neu = _anwenden(alt, daten, sid is None, bestand)
        except Abgelehnt as e:
            log.warning("MCP-Server %r: Eingabe abgelehnt — %s",
                        str(daten.get("name") or alt["name"])[:60], e.grund)
            return False, e.grund
        neu["geaendert"] = _jetzt()
        if sid is None:
            bestand.append(neu)
        else:
            bestand = [neu if s["id"] == sid else s for s in bestand]
        _schreiben(bestand)
    log.info("MCP-Server %r %s (%s).", neu["name"], "angelegt" if sid is None else "geändert",
             urlsplit(neu["url"]).netloc)
    return True, _oeffentlich(neu)


def loeschen(sid) -> bool:
    """Den Eintrag entfernen. False = unbekannte Kennung. Wirft bei Datenbankfehler."""
    with _SPERRE:
        bestand = _laden()
        rest = [s for s in bestand if s["id"] != sid]
        if len(rest) == len(bestand):
            log.info("MCP-Server %r: unbekannte Kennung — nichts gelöscht.", str(sid)[:16])
            return False
        _schreiben(rest)
    weg = next(s for s in bestand if s["id"] == sid)
    log.info("MCP-Server %r gelöscht.", weg["name"])
    return True


def export(mit_token=False):
    """{"mcpServers": {name: {"url": …, "headers": {"Authorization": "Bearer …"}}}}.

    Nur aktive Einträge. `headers` nur mit mit_token=True und gesetztem Token —
    die einzige Stelle, an der ein Token den Server verlässt, und nur, weil
    der Betreiber sie ausdrücklich verlangt."""
    server = {}
    for s in _laden():
        if not s.get("aktiv", True):
            continue
        e = {"url": s["url"]}
        if mit_token and s.get("token"):
            e["headers"] = {"Authorization": "Bearer " + s["token"]}
        server[s["name"]] = e
    return {"mcpServers": server}


# ── Verbindungstest: MCP Streamable HTTP ────────────────────────────────────

def _kurz(wert, n):
    """Fremder Text für Anzeige und Ablage: ohne Steuerzeichen, eine Zeile, gekürzt."""
    return (" ".join("".join(c for c in wert if unicodedata.category(c)[0] != "C"
                             or c.isspace()).split())[:n]
            if isinstance(wert, str) else "")


def _schwaerzen(obj, token):
    """Den Token aus allem entfernen, was ein Fremdserver geliefert hat.

    Ein Server, der die Anfrage in seiner Fehlerseite oder einer
    Werkzeugbeschreibung zurückspiegelt, trüge ihn sonst ins Deck und in
    die Ablage."""
    if not token:
        return obj
    if isinstance(obj, str):
        return obj.replace(token, GESCHWAERZT)
    if isinstance(obj, list):
        return [_schwaerzen(x, token) for x in obj]
    if isinstance(obj, dict):
        return {k: _schwaerzen(v, token) for k, v in obj.items()}
    return obj


def _antworten_in(obj, nr):
    """Die Antworten auf Anfrage `nr` in einer Nachricht (oder einem Stapel).
    Benachrichtigungen und Anfragen des Servers (ping, logging) gehören nicht
    dazu — ein SSE-Strom darf sie vor der Antwort schicken."""
    stapel = obj if isinstance(obj, list) else [obj]
    return [m for m in stapel
            if isinstance(m, dict) and m.get("id") in (nr, str(nr))
            and ("result" in m or "error" in m)]


class _Sitzung:
    """Eine Prüfung gegen einen Server: Frist, Sitzungskennung, Kopfzeilen."""

    def __init__(self, url, token, zeitlimit):
        teile = urlsplit(url)
        self.https = teile.scheme == "https"
        self.host = teile.hostname
        self.port = teile.port
        self.ziel = teile.netloc
        pfad = (teile.path or "/") + ("?" + teile.query if teile.query else "")
        # Prozentkodiert: http.client schreibt die Anfragezeile als ASCII; ein
        # Umlaut im Pfad wäre sonst ein UnicodeEncodeError statt eines Tests.
        self.pfad = quote(pfad, safe="/?&=%:@!$'()*+,;~-._")
        self.token = token
        self.zeitlimit = zeitlimit
        self.frist = time.monotonic() + zeitlimit
        self.sitzung = None
        self.protokoll = None
        self.status = None
        self.nr = 0

    def rest(self):
        """Verbleibende Zeit bis zur Frist — vor JEDEM Lesevorgang neu gesetzt."""
        r = self.frist - time.monotonic()
        if r <= 0:
            raise _Abbruch(ZEIT, s="%g" % self.zeitlimit)
        return r

    def koepfe(self, mit_inhalt):
        k = {"Accept": "application/json, text/event-stream",
             "User-Agent": "NIGHTCRAWLER/%s (MCP-Test)" % _version.VERSION}
        if mit_inhalt:
            k["Content-Type"] = "application/json"
        if self.token:
            k["Authorization"] = "Bearer " + self.token
        if self.sitzung:
            k["Mcp-Session-Id"] = self.sitzung
        if self.protokoll:
            k["MCP-Protocol-Version"] = self.protokoll
        return k

    def verbindung(self, zeit):
        if self.https:
            return http.client.HTTPSConnection(self.host, self.port, timeout=zeit,
                                               context=ssl.create_default_context())
        return http.client.HTTPConnection(self.host, self.port, timeout=zeit)

    def _post(self, conn, nachricht):
        """-> (sock, resp). Der Socket wird VOR getresponse() gegriffen: bei
        „Connection: close" gibt http.client ihn dort an die Antwort ab, und
        conn.sock ist danach None — die Frist liesse sich nicht mehr setzen."""
        self.status = None
        conn.request("POST", self.pfad, body=json.dumps(nachricht).encode("utf-8"),
                     headers=self.koepfe(True))
        sock = conn.sock
        sock.settimeout(self.rest())
        resp = conn.getresponse()
        self.status = resp.status
        return sock, resp

    def anfrage(self, methode, params):
        """Eine JSON-RPC-Anfrage. -> das result-Objekt (dict). Wirft _Abbruch."""
        self.nr += 1
        nr = self.nr
        conn = self.verbindung(self.rest())
        resp = None
        try:
            sock, resp = self._post(conn, {"jsonrpc": "2.0", "id": nr, "method": methode,
                                           "params": params})
            _status_pruefen(self, resp, sock)
            if methode == "initialize":
                self._sitzung_merken(resp)
            art = (resp.getheader("Content-Type") or "").split(";")[0].strip().lower()
            if resp.status == 202:
                raise _Abbruch(OHNE_ANTWORT, methode=methode)
            if art == "text/event-stream":
                antwort = _aus_sse(self, resp, sock, nr, methode)
            elif art == "application/json":
                antwort = _aus_json(self, resp, sock, nr, methode)
            else:
                raise _Abbruch(KEIN_MCP, typ=art[:60] or "?")
        finally:
            if resp is not None:
                resp.close()
            conn.close()
        if "error" in antwort:
            f = antwort["error"] if isinstance(antwort["error"], dict) else {}
            raise _Abbruch(RPC_FEHLER, methode=methode, code=_kurz(str(f.get("code", "?")), 12),
                           meldung=_kurz(f.get("message"), 160) or "?")
        ergebnis = antwort.get("result")
        if not isinstance(ergebnis, dict):
            raise _Abbruch(OHNE_ERGEBNIS, methode=methode)
        return ergebnis

    def benachrichtigen(self, methode):
        """Eine Benachrichtigung (ohne id). Erwartet 202; jedes 2xx genügt."""
        conn = self.verbindung(self.rest())
        resp = None
        try:
            sock, resp = self._post(conn, {"jsonrpc": "2.0", "method": methode})
            _status_pruefen(self, resp, sock)
        finally:
            if resp is not None:
                resp.close()
            conn.close()

    def _sitzung_merken(self, resp):
        sid = resp.getheader("Mcp-Session-Id")
        if sid is None:
            return
        if not _SITZUNG.fullmatch(sid):
            raise _Abbruch(SITZUNG_UNGUELTIG)
        self.sitzung = sid


def _lesen(s, resp, sock, gelesen, zeile):
    """Ein Stück des Rumpfs, unter Frist und Deckel. -> bytes (leer = Ende)."""
    if resp.isclosed():
        # v5.7-W198: der Rumpf ist ganz gelesen. Bei „Connection: close"
        # (HTTP/1.0, viele einfache MCP-Server) hat http.client den Socket
        # dabei geschlossen — ein settimeout darauf warf OSError (EBADF), und
        # jeder solche Server erschien als „Netzwerkfehler", obwohl er korrekt
        # geantwortet hatte. Gefunden im Ende-zu-Ende-Lauf, nicht im Vertrag:
        # dessen Attrappe hielt die Verbindung offen.
        return resp.read(0)
    sock.settimeout(s.rest())
    stueck = resp.readline(MAX_RUMPF + 1 - gelesen) if zeile else resp.read1(65536)
    if gelesen + len(stueck) > MAX_RUMPF:
        raise _Abbruch(ZU_GROSS, mb=MAX_RUMPF // (1024 * 1024))
    return stueck


def _aus_json(s, resp, sock, nr, methode):
    # Kein zweiter Riegel über Content-Length: der Deckel in _lesen greift auch
    # ohne Längenangabe, und eine Vorprüfung, deren Wegfall kein Vertrag
    # bemerkt, wäre eine falsche Gewissheit (W105).
    teile, n = [], 0
    while True:
        stueck = _lesen(s, resp, sock, n, zeile=False)
        if not stueck:
            break
        n += len(stueck)
        teile.append(stueck)
    try:
        obj = json.loads(b"".join(teile).decode("utf-8"))
    except ValueError as e:
        raise _Abbruch(KEIN_JSON, methode=methode, fehler=_kurz(str(e), 80)) from None
    treffer = _antworten_in(obj, nr)
    if not treffer:
        raise _Abbruch(OHNE_ANTWORT, methode=methode)
    return treffer[0]


def _ereignis(daten, nr, methode):
    try:
        obj = json.loads("\n".join(daten))
    except ValueError as e:
        raise _Abbruch(KEIN_JSON, methode=methode, fehler=_kurz(str(e), 80)) from None
    return _antworten_in(obj, nr)


def _aus_sse(s, resp, sock, nr, methode):
    """Die Antwort aus einem SSE-Strom: `data:`-Zeilen bis zur Leerzeile sind
    ein Ereignis; das erste mit passender id ist die Antwort. Kommentare
    (`: ping`) und andere Ereignisse zählen gegen Frist und Deckel."""
    daten, n = [], 0
    while True:
        roh = _lesen(s, resp, sock, n, zeile=True)
        n += len(roh)
        z = roh.decode("utf-8", "replace").rstrip("\r\n")
        if roh and z.startswith("data:"):
            daten.append(z[6:] if z.startswith("data: ") else z[5:])
            continue
        if z or (roh and not daten):
            continue                   # event:/id:/Kommentar, oder Leerzeile ohne Ereignis
        # Leerzeile nach einem Ereignis — oder das Ende des Stroms (manche
        # Server schliessen direkt nach der letzten data:-Zeile).
        treffer = _ereignis(daten, nr, methode) if daten else []
        if treffer:
            return treffer[0]
        if not roh:
            raise _Abbruch(OHNE_ANTWORT, methode=methode)
        daten = []


def _ziel(ort):
    """Das Umleitungsziel für die Anzeige: Rechner und Pfad, ohne Abfrage."""
    t = urlsplit(ort or "")
    return _kurz((t.hostname or "") + (t.path or ""), 120) or "?"


def _auszug(s, resp, sock):
    """Die ersten Zeichen einer Fehlerantwort — für den Betreiber, gedeckelt."""
    sock.settimeout(s.rest())
    return _kurz(resp.read1(600).decode("utf-8", "replace"), 160) or "-"


def _status_pruefen(s, resp, sock):
    code = resp.status
    if 200 <= code < 300:
        return
    if 300 <= code < 400:
        raise _Abbruch(UMLEITUNG, http=code, code=code, ziel=_ziel(resp.getheader("Location")))
    if code in (401, 403):
        raise _Abbruch(ANMELDUNG if s.token else ANMELDUNG_OHNE, http=code, code=code)
    if code in (404, 405):
        raise _Abbruch(KEIN_ENDPUNKT, http=code, code=code)
    raise _Abbruch(SERVERFEHLER if code >= 500 else ABGELEHNT, http=code, code=code,
                   auszug=_auszug(s, resp, sock))


def _werkzeuge(s):
    """-> (werkzeuge, vollstaendig). Höchstens MAX_SEITEN Seiten, MAX_WERKZEUGE Einträge.

    `vollstaendig` False heißt: es gibt mehr, als hier steht. Eine Liste, die
    still abschneidet, sähe aus wie der ganze Bestand des Servers."""
    aus, abgeschnitten, cursor = [], False, None
    for _seite in range(MAX_SEITEN):
        erg = s.anfrage("tools/list", {"cursor": cursor} if cursor else {})
        werkzeuge = erg.get("tools")
        if not isinstance(werkzeuge, list):
            raise _Abbruch(WERKZEUGLISTE)
        for w in werkzeuge:
            if not (isinstance(w, dict) and isinstance(w.get("name"), str)):
                continue
            if len(aus) >= MAX_WERKZEUGE:
                abgeschnitten = True
                break
            aus.append({"name": _kurz(w["name"], 128),
                        "beschreibung": _kurz(w.get("description"), 300)})
        cursor = erg.get("nextCursor")
        if not (isinstance(cursor, str) and cursor) or abgeschnitten:
            return aus, not abgeschnitten
    return aus, False


def _sitzung_beenden(s):
    """Die Sitzung beim Server abmelden (Spezifikation: SHOULD). Sonst sammelt
    ein zustandsbehafteter Server je Test eine Sitzung, bis er sie vergisst."""
    rest = s.frist - time.monotonic()
    if not s.sitzung or rest <= 0.2:
        return
    conn = s.verbindung(min(2.0, rest))
    try:
        conn.request("DELETE", s.pfad, headers=s.koepfe(False))
        conn.getresponse().close()
    except (OSError, http.client.HTTPException) as e:
        # Aufräumen: der Test ist entschieden. 405 ist laut Spezifikation
        # erlaubt, ein Server ohne DELETE oder mit vergessener Sitzung ist
        # kein Befund — deshalb nur debug.
        log.debug("MCP: Sitzung bei %s nicht beendet — %s", s.ziel, type(e).__name__)
    finally:
        conn.close()


def _pruefen(s):
    """initialize → notifications/initialized → tools/list. -> Ergebnis (ok)."""
    init = s.anfrage("initialize", {
        "protocolVersion": PROTOKOLL, "capabilities": {},
        "clientInfo": {"name": "nightcrawler", "version": _version.VERSION}})
    proto = init.get("protocolVersion")
    proto = proto if isinstance(proto, str) and _PROTO.fullmatch(proto) else None
    s.protokoll = proto or PROTOKOLL
    info = init.get("serverInfo") if isinstance(init.get("serverInfo"), dict) else {}
    server = {"name": _kurz(info.get("name"), 100), "version": _kurz(info.get("version"), 60)}
    s.benachrichtigen("notifications/initialized")
    faehig = init.get("capabilities") if isinstance(init.get("capabilities"), dict) else {}
    # Ohne angekündigte Werkzeuge kein tools/list: die Spezifikation verlangt
    # die Ankündigung, und ein reiner Ressourcen-Server ist kein Fehler.
    werkzeuge, vollstaendig = _werkzeuge(s) if "tools" in faehig else ([], True)
    _sitzung_beenden(s)
    return {"ok": True, "protokoll": proto, "server": server, "werkzeuge": werkzeuge,
            "vollstaendig": vollstaendig, "grund": "", "http": s.status}


def _netzfehler(e, s):
    """Eine Netz-Ausnahme als Befund mit Abhilfe. Reihenfolge zählt: die
    SSL-Fehler sind OSError, RemoteDisconnected ist beides."""
    if isinstance(e, TimeoutError):
        return _Abbruch(ZEIT, s="%g" % s.zeitlimit)
    if isinstance(e, ConnectionRefusedError):
        return _Abbruch(VERWEIGERT, ziel=s.ziel)
    if isinstance(e, socket.gaierror):
        return _Abbruch(NAME_UNAUFLOESBAR, ziel=s.host)
    if isinstance(e, ssl.SSLCertVerificationError):
        return _Abbruch(TLS_ZERTIFIKAT, ziel=s.ziel)
    if isinstance(e, ssl.SSLError):
        return _Abbruch(TLS, ziel=s.ziel)
    if isinstance(e, http.client.HTTPException):
        return _Abbruch(KEIN_HTTP, art=type(e).__name__)
    return _Abbruch(NETZ, ziel=s.ziel, art=type(e).__name__)


def _fehlschlag(e, s, name):
    """Das Ergebnis eines gescheiterten Tests — und seine Zeile im Log.

    Die Werte laufen durch _schwaerzen UND fehlertext.saeubern: ein
    Antwort-Auszug ist fremder Text und darf weder den Token noch einen
    Serverpfad ins Deck tragen."""
    werte = {k: _fehlertext.saeubern(_schwaerzen(str(v), s.token)) for k, v in e.werte.items()}
    grund = e.vorlage.format(**werte)
    log.warning("MCP-Test %r (%s): %s", name, s.ziel, grund)
    return {"ok": False, "protokoll": None, "server": None, "werkzeuge": [],
            "vollstaendig": False, "grund": grund, "grund_vorlage": e.vorlage,
            "grund_werte": werte, "http": e.http if e.http is not None else s.status}


def _ablegen(eintrag, ergebnis):
    """Das Ergebnis als letzter_test ablegen — nur, wenn der Eintrag noch
    derselbe ist. Wer während des Tests Adresse oder Token geändert hat, hat
    damit den alten Befund schon verworfen (_anwenden)."""
    try:
        with _SPERRE:
            bestand = _laden()
            for s in bestand:
                if (s["id"] == eintrag["id"] and s["url"] == eintrag["url"]
                        and s.get("token", "") == eintrag.get("token", "")):
                    s["letzter_test"] = ergebnis
                    _schreiben(bestand)
                    break
            else:
                log.info("MCP-Test %r: Eintrag während des Tests geändert oder gelöscht — "
                         "Ergebnis nicht abgelegt.", eintrag["name"])
    except Exception as e:
        log.warning("MCP-Test %r: Ergebnis nicht gespeichert — %s: %s", eintrag["name"],
                    type(e).__name__, _fehlertext.saeubern(str(e)))


def testen(sid, zeitlimit=10.0):
    """Verbindungstest nach MCP Streamable HTTP. -> Ergebnis-dict, auch als
    letzter_test abgelegt. Wirft Unbekannt bei fremder Kennung.

    {"ok", "zeit", "dauer_ms", "protokoll", "server": {"name", "version"} | None,
     "werkzeuge": [{"name", "beschreibung"}], "vollstaendig", "grund", "http"}
    Bei einem Fehlschlag zusätzlich grund_vorlage/grund_werte — daraus baut
    die Route den Grund in der Sprache der Anfrage."""
    eintrag = _eintrag(sid)
    zeitlimit = min(max(float(zeitlimit), 0.5), 60.0)
    s = _Sitzung(eintrag["url"], eintrag.get("token") or "", zeitlimit)
    t0 = time.monotonic()
    try:
        ergebnis = _schwaerzen(_pruefen(s), s.token)
    except _Abbruch as e:
        ergebnis = _fehlschlag(e, s, eintrag["name"])
    except (OSError, http.client.HTTPException) as e:
        ergebnis = _fehlschlag(_netzfehler(e, s), s, eintrag["name"])
    ergebnis["zeit"] = _jetzt()
    ergebnis["dauer_ms"] = int((time.monotonic() - t0) * 1000)
    if ergebnis["ok"]:
        log.info("MCP-Test %r (%s): erreichbar, Protokoll %s, %d Werkzeuge, %d ms.",
                 eintrag["name"], s.ziel, ergebnis["protokoll"], len(ergebnis["werkzeuge"]),
                 ergebnis["dauer_ms"])
    _ablegen(eintrag, ergebnis)
    return ergebnis


# ── Lage: läuft llama-server mit der Oberfläche, die MCP kennt? ─────────────

def llama_adresse():
    """BRAIN_LLAMACPP_URL — als Funktion gelesen, nie als Modul-Konstante: die
    .env lädt der Bot erst nach den ersten Importen (CLAUDE.md, W67)."""
    return (os.getenv("BRAIN_LLAMACPP_URL") or "").strip().rstrip("/") or LLAMA_VORGABE


def _execstart(text):
    """Die Wörter der LETZTEN ExecStart=-Zeile — und nur dieser.

    Die mitgelieferte Vorlage (llama-server.service) nennt `--webui llamacpp`
    im KOMMENTAR, ohne den Schalter zu setzen. Wer den Dateitext absucht,
    meldet eine Oberfläche, die nicht läuft — die Falle aus W102–W104 (eine
    Begründung als Befund gelesen)."""
    woerter = []
    for z in text.replace("\\\n", " ").splitlines():
        z = z.strip()
        if z.startswith("ExecStart="):
            woerter = z[len("ExecStart="):].split()
    return woerter


def webui(unit_pfad=None):
    """{"gefunden", "webui": "llamacpp"|"auto"|"none"|None, "mcp_proxy", "adresse", "abhilfe"}.

    "abhilfe" ist leer, wenn Oberfläche und Proxy laufen."""
    pfad = unit_pfad or UNIT_PFAD
    aus = {"gefunden": False, "webui": None, "mcp_proxy": False,
           "adresse": llama_adresse(), "abhilfe": WEBUI_KEINE_UNIT}
    if not os.path.isfile(pfad):
        return aus
    try:
        with open(pfad, encoding="utf-8", errors="replace") as f:
            text = f.read(256 * 1024)
    except OSError as e:
        log.warning("MCP-Lage: %s nicht lesbar — %s: %s", pfad, type(e).__name__, e)
        aus["abhilfe"] = WEBUI_UNLESBAR
        return aus
    aus["gefunden"] = True
    woerter = _execstart(text)
    if not woerter:
        aus["abhilfe"] = WEBUI_OHNE_START
        return aus
    # Ohne Schalter zeigt ik_llama.cpp seine Vorgabe `auto` — die alte
    # Oberfläche ohne MCP-Reiter (W197).
    wert = "auto"
    for i, w in enumerate(woerter):
        if w == "--webui" and i + 1 < len(woerter):
            wert = woerter[i + 1]
        elif w.startswith("--webui="):
            wert = w.split("=", 1)[1]
    aus["webui"] = _kurz(wert, 20)
    aus["mcp_proxy"] = any(w in ("--webui-mcp-proxy", "--ui-mcp-proxy") for w in woerter)
    if aus["webui"] != "llamacpp":
        aus["abhilfe"] = WEBUI_FEHLT
    elif not aus["mcp_proxy"]:
        aus["abhilfe"] = WEBUI_PROXY_AUS
    else:
        aus["abhilfe"] = ""
    return aus


def lage(server=None, unit_pfad=None):
    """{"anzahl", "aktiv", "webui": webui()}. `server` spart den zweiten
    Datenbankzugriff, wenn der Aufrufer liste() schon hat."""
    if server is None:
        server = liste()
    return {"anzahl": len(server), "aktiv": sum(1 for s in server if s.get("aktiv", True)),
            "webui": webui(unit_pfad)}
