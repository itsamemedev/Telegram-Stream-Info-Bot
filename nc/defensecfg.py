"""nc.defensecfg — v4.1-W25: die Einstellungen der Abwehr-Ansicht.

Die vier Routen unter `/api/defense` lesen sechs .env-Werte des Monolithen:
den Standort des Servers für die Weltkarte und die vier Angaben zur
CrowdSec-LAPI. Als nc.ctx-Einträge wären das sechs der 25 vertraglichen
Plätze — bei 24 belegten unmöglich. Dieselbe Auflösung wie in
nc/restreamcfg.py (W22) und nc/backupcfg.py (W24).

**Gelesen wird bei JEDEM Aufruf, nie als Modul-Konstante** (CLAUDE.md).

════════════════════════════════════════════════════════════════════════
DER BOUNCER-SCHLÜSSEL IST EIN GEHEIMNIS
════════════════════════════════════════════════════════════════════════
`CROWDSEC_BOUNCER_KEY` ist ein API-Schlüssel für die lokale CrowdSec-LAPI.
Deshalb dieselbe Trennung wie bei den Stream-Keys (W22) und den
S3-Zugangsdaten (W24):

* `bouncer_key()` gibt ihn heraus und ist **nur für den LAPI-Aufruf**.
* Für Anzeige und Diagnose gibt es `bouncer_gesetzt()` — ein bool.
  Die Routen benutzen ausschliesslich das.

Ob der Schlüssel fehlt, ist eine Betriebsfrage und kein Geheimnis: ohne ihn
läuft die Abfrage über `cscli` und braucht Root. Genau deshalb darf die
Anzeige „ist einer da?" beantworten — sie erklärt dem Betreiber, warum der
sudo-Weg genommen wird.
"""

import os


def _zahl(wert, default):
    try:
        return int((wert or "").strip() or default)
    except (TypeError, ValueError):
        return default


def _komma(wert, default):
    """Fliesskomma aus .env. Eine leere Variable faellt auf den Vorgabewert
       zurueck statt zu werfen — eine gesetzte, leere .env-Zeile ist der
       häufigste Fall (v4.0-W82)."""
    try:
        return float((wert or "").strip().replace(",", ".") or default)
    except (TypeError, ValueError):
        return default


# ---- Standort des Servers (für die Weltkarte) -------------------------------

def server_lat() -> float:
    """Vorgabe: OVH Gravelines, FR — dort steht die Kiste."""
    return _komma(os.getenv("DEFENSE_SERVER_LAT", "50.69"), 50.69)


def server_lon() -> float:
    return _komma(os.getenv("DEFENSE_SERVER_LON", "2.13"), 2.13)


# ---- CrowdSec-LAPI ----------------------------------------------------------

def lapi_host() -> str:
    return (os.getenv("CROWDSEC_LAPI_HOST", "127.0.0.1") or "127.0.0.1").strip()


def lapi_port() -> int:
    return _zahl(os.getenv("CROWDSEC_LAPI_PORT", "8083"), 8083)


def lapi_url() -> str:
    """Vollständige Adresse, wenn gesetzt — sonst leer, dann bauen Host und
       Port sie zusammen (nc.crowdsec.decisions_url)."""
    return (os.getenv("CROWDSEC_LAPI_URL", "") or "").strip()


def bouncer_key() -> str:
    """Der Bouncer-Schlüssel. EINZIGE Funktion hier, die ihn herausgibt —
       siehe Modul-Kopf. Nur für den LAPI-Aufruf, nie für eine Antwort."""
    return (os.getenv("CROWDSEC_BOUNCER_KEY", "") or "").strip()


def bouncer_gesetzt() -> bool:
    """Für Anzeige und Diagnose: ist ein Schlüssel hinterlegt? Ohne ihn läuft
       die Abfrage über cscli und braucht Root — das erklärt dem Betreiber,
       warum der sudo-Weg genommen wird."""
    return bool(bouncer_key())


# ---- Letzter Fehler der Geo-Auflösung ---------------------------------------

# REGISTER, kein Alias: das ist eine Zeichenkette, und eine Zeichenkette ist
# unteilbar — der Monolith BINDET den Namen neu (`global _DEFENSE_GEO_ERR`),
# ein Alias zeigte danach für immer auf den alten leeren Wert. Dieselbe
# Überlegung wie bei STALLS in nc/brainstate.py (W21).
GEO_ERR = {"text": ""}


def geo_fehler() -> str:
    """Warum ist die Weltkarte leer? Fiel ip-api aus (Rate-Limit 45/min oder
       ausgehender Port 80 zu), blieben TOP-LÄNDER und Karte leer und niemand
       erfuhr warum (B138)."""
    return GEO_ERR["text"]


def geo_fehler_setzen(text: str):
    GEO_ERR["text"] = (text or "")[:160]
