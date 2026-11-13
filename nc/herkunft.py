"""nc.herkunft — v4.2-W178: schreibende Deck-Anfragen nur von der eigenen Seite (bot-frei).

DAS FEHLERBILD
  Das Deck laesst Anfragen vom Rechner selbst ohne Token durch — so ist der
  SSH-Tunnel gedacht (`_auth_guard`, `_ist_lokal`). Der Browser des Betreibers
  ist aber nicht nur im Deck: jede andere Seite, die er im selben Browser
  offen hat, darf ein Formular an http://localhost:3000/api/... abschicken.
  Der Browser schickt es, die Anfrage kommt ueber den Tunnel als 127.0.0.1
  an, und 44 POST-Routen lesen Formulare (request.form/values). Ein
  verstecktes <form> genuegte fuer /api/donations/reset, /api/db/import,
  /api/restream/<id>/delete oder /api/update/restart. Mit Token oder PIN gilt
  dasselbe: das Cookie geht bei einem Formular-POST der obersten Ebene mit
  (SameSite=Lax schuetzt nur Unteranfragen).

DIE REGEL
  Fuer POST/PUT/PATCH/DELETE:
    * `Sec-Fetch-Site` gesetzt (jeder Browser seit 2020/2023): nur
      "same-origin" und "none" (vom Nutzer selbst, Adresszeile/Lesezeichen).
      "same-site" ist NICHT genug — ein anderer Port auf demselben Rechner
      ist dieselbe Site.
    * sonst `Origin` gesetzt: Host (und, wo beide einen nennen, Port) muss
      dem Host der Anfrage entsprechen. `X-Forwarded-Host` zaehlt nur von
      einem vertrauten Proxy (TRUSTED_PROXIES, nc/clientip) — sonst setzt ihn
      die fremde Seite nicht, aber ein Skript, das ohnehin kein Browser ist.
    * keine von beiden: durchlassen. curl, tools/, Skripte und alte Clients
      schicken keine; ein Browser, der eine fremde Seite ausfuehrt, schickt
      bei einem POST immer mindestens Origin.
  Das Deck selbst ruft per fetch() auf derselben Adresse — dort steht
  "same-origin", und nichts aendert sich.

AUSNAHMEN
  Pfade, die fremde Server aufrufen (OAuth-Rueckrufe). Eingehende Webhooks
  gibt es im Bestand derzeit keine; wer einen baut, traegt ihn in AUSNAHMEN
  ein und prueft dort seine Signatur.
"""

import re
from urllib.parse import urlsplit

SCHREIBEND = frozenset(("POST", "PUT", "PATCH", "DELETE"))
ERLAUBTE_SEITE = frozenset(("same-origin", "none"))
# Die Antwort „darf durch". Benannt, weil None hier kein Misserfolg ist,
# sondern der Normalfall jeder Deck-Anfrage (tools/blindstellen.py).
ERLAUBT = None


def _t(text):
    """Markiert Benutzertext fuer tools/i18n_extract.py (uebersetzt wird beim Gebrauch)."""
    return text


# Die Antwort an das Deck. Hier statt in bot.py: dort sammelt der Extraktor nur
# Texte, die an Telegram/Discord gehen — eine JSON-Fehlerantwort waere in der
# englischen Oberflaeche still deutsch geblieben.
ABGEWIESEN = _t("Abgewiesen: Die Anfrage kam nicht vom Deck selbst (fremde Seite im Browser).")
# v5.6-W197: "/api/yt/oauth/callback" stand hier und in _AUTH_EXEMPT_EXACT,
# ohne dass es die Route je gab. Eine Ausnahme fuer einen leeren Pfad ist eine
# Luecke auf Vorrat: wer dort spaeter etwas anlegt, haette es ohne Anmeldung
# und ohne Herkunftspruefung.
AUSNAHMEN = ("/api/kick/oauth/callback", "/api/twitch/oauth/callback",
             "/api/youtube/oauth/callback")


# Ein regulaerer Ausdruck statt urlsplit().port: der wirft bei einem Port
# ausser Bereich ValueError, und ein fremder Kopf darf hier nichts werfen.
_HOST_RE = re.compile(r"^(?:[a-z][a-z0-9+.-]*://)?(?:[^@/]*@)?(\[[^\]/]*\]|[^:/?#\[\]]*)"
                      r"(?::(\d{1,5}))?(?:[/?#]|$)")


def _host_port(wert, schema=""):
    """('host', 'port' oder '') aus 'host:port', '[v6]:port' oder einer URL."""
    m = _HOST_RE.match((wert or "").strip().lower())
    host = (m.group(1) if m else "").strip(".")
    port = (m.group(2) or "") if m else ""
    if host and not port and schema:
        port = {"http": "80", "https": "443"}.get(schema, "")
    return host, port


def _passt(origin, hosts) -> bool:
    """Stimmt Origin mit einem der erlaubten Hosts ueberein?"""
    o_schema = urlsplit((origin or "").strip().lower()).scheme
    if o_schema not in ("http", "https"):
        return False                    # auch "null" (Sandbox, file://)
    o_host, o_port = _host_port(origin, o_schema)
    if not o_host:
        return False
    for h in hosts:
        h_host, h_port = _host_port(h)
        if not h_host or h_host != o_host:
            continue
        # Port nur vergleichen, wo der Host einen nennt: nginx reicht
        # "Host $host" ohne Port durch, der Browser nennt ihn im Origin.
        if h_port and h_port != o_port:
            continue
        return True
    return False


def entscheiden(methode, pfad, koepfe, remote="", vertraut=()):
    """ERLAUBT (None) = darf durch, sonst der Grund (Text fuers Log und die Antwort).

    koepfe: Mapping der Kopfzeilen (request.headers — Gross/Klein egal)."""
    if (methode or "").upper() not in SCHREIBEND:
        return ERLAUBT
    if (pfad or "") in AUSNAHMEN:
        return ERLAUBT
    seite = (koepfe.get("Sec-Fetch-Site") or "").strip().lower()
    if seite:
        if seite in ERLAUBTE_SEITE:
            return ERLAUBT
        return "Sec-Fetch-Site=%s" % seite[:40]
    origin = (koepfe.get("Origin") or "").strip()
    if not origin:
        return ERLAUBT                      # kein Browser — curl, tools/, Skripte
    hosts = [koepfe.get("Host") or ""]
    if (remote or "").strip() in vertraut:
        xfh = (koepfe.get("X-Forwarded-Host") or "").split(",")[-1].strip()
        if xfh:
            hosts.append(xfh)
    if _passt(origin, hosts):
        return ERLAUBT
    return "Origin %s passt nicht zu Host %s" % (origin[:80], (hosts[0] or "?")[:80])
