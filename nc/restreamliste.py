"""nc.restreamliste — v5.9-W204: getrackte Nutzer landen in der Restream-Auto-Liste.

════════════════════════════════════════════════════════════════════════
DER ANLASS
════════════════════════════════════════════════════════════════════════
Der Betreiber: „Die User aus Discord und Telegram werden nicht mehr in die
Liste eingetragen, welche User im Kick-, YouTube- und Twitch-Stream landen."

Nachgesehen: die Liste ist die Tabelle `restreams`, und sie wurde
ausschliesslich im Deck befuellt (`/api/restream/create`). Wer per Telegram
oder Discord einen TikTok-Account trackte, landete in `trackings` — und von
dort fuehrte kein Weg in die Auto-Liste. Der Auto-Restream (Single-Modus:
das erste Ziel der Liste, dessen Quelle live ist) kannte diese Nutzer nicht.

Jetzt gleicht `abgleichen()` die beiden Tabellen ab:

* Ein getrackter Nutzer ohne Zeile bekommt eine — `auto_restream=1`, Ingest
  und Key LEER (dann gelten die Ziele aus der .env, wie bei jeder Zeile ohne
  eigene Keys), `herkunft='tracking'`. Manuelle Zeilen (herkunft leer) haben
  kleinere Kennungen und bleiben damit vorn in der Reihenfolge.
* Wird ein Nutzer nirgends mehr getrackt, ruht seine Zeile
  (`auto_restream=0`, `herkunft='tracking-ruht'`) — geloescht wird nichts:
  eine laufende Sendung oder ein Soll-Zustand haengt womoeglich daran.
  Kommt er zurueck, wird sie wieder scharf.
* Was der Betreiber im Deck entscheidet, gilt: eine Zeile, deren Auto-Schalter
  er abgestellt hat, bleibt aus (nur 'tracking-ruht' wird wieder scharf), und
  wer eine Zeile aus dem Tracking loescht, steht auf der Ausschlussliste
  (`restream.tracking_ausschluss` in app_config) — sonst kaeme sie beim
  naechsten Abgleich zurueck, und Loeschen haette keine Wirkung.

Pausierte Trackings zaehlen nicht: wer pausiert, will diesen Nutzer gerade
nicht verfolgen. Abschaltbar mit RESTREAM_TRACKINGS=0.

Bot-frei; die Verbindung kommt vom Aufrufer.
"""

import logging
import os

from nc.textutil import clean_username

log = logging.getLogger(__name__)


def _schluessel(u) -> str:
    """Vergleichsform eines TikTok-Namens. TikTok unterscheidet keine Gross- und
    Kleinschreibung, clean_username behaelt sie — ohne das galten „Dora" (im
    Deck angelegt) und „dora" (per Telegram getrackt) als zwei Nutzer, und ein
    Ausschluss „@Emil" griff nicht fuer „emil"."""
    return clean_username(u or "").lower()


HERKUNFT = "tracking"
HERKUNFT_RUHT = "tracking-ruht"
AUSSCHLUSS_SCHLUESSEL = "restream.tracking_ausschluss"


def an() -> bool:
    """RESTREAM_TRACKINGS (Vorgabe an). Zur Laufzeit gelesen (.env kommt spaeter)."""
    return os.getenv("RESTREAM_TRACKINGS", "1").strip().lower() not in ("0", "false", "nein", "no", "off", "aus")


def _transcode_vorgabe(zeilen) -> int:
    """Wie die juengste MANUELLE Zeile — der Betreiber hat dort entschieden,
    ob umkodiert wird (das Studio-Sendebild braucht es). Ohne manuelle Zeile: 1,
    denn ohne Umkodieren gibt es kein Overlay."""
    manuell = [z for z in zeilen if not (z.get("herkunft") or "")]
    if not manuell:
        return 1
    return 1 if int(max(manuell, key=lambda z: int(z["id"]))["transcode"] or 0) else 0


def abgleichen(conn, jetzt_iso, ausgeschlossen=()) -> dict:
    """trackings -> restreams. -> {"neu": [...], "ruht": [...], "wieder": [...]}.

    Schreibt nur, was sich aendert; der Aufrufer committet."""
    ausgeschlossen = {_schluessel(u) for u in (ausgeschlossen or ()) if u}
    getrackt = {}                              # Vergleichsform -> Schreibweise
    for r in conn.execute("SELECT DISTINCT username FROM trackings "
                          "WHERE COALESCE(paused, 0) = 0").fetchall():
        u = clean_username(r["username"] or "")
        if u:
            getrackt.setdefault(u.lower(), u)
    zeilen = [dict(r) for r in conn.execute(
        "SELECT id, source_username, auto_restream, transcode, herkunft "
        "FROM restreams").fetchall()]
    vorhanden = {}
    for z in zeilen:
        u = _schluessel(z["source_username"])
        if u and u not in vorhanden:
            vorhanden[u] = z
    neu, ruht, wieder = [], [], []
    transcode = _transcode_vorgabe(zeilen)
    for s in sorted(set(getrackt) - set(vorhanden) - ausgeschlossen):
        u = getrackt[s]
        conn.execute(
            "INSERT INTO restreams (created_at, label, source_username, ingest_url, "
            "stream_key, transcode, enabled, auto_restream, status, herkunft) "
            "VALUES (?,?,?,?,?,?,1,1,'idle',?)",
            (jetzt_iso, u[:120], u, "", "", transcode, HERKUNFT))
        neu.append(u)
    for u, z in vorhanden.items():
        h = z.get("herkunft") or ""
        if h == HERKUNFT and u not in getrackt and int(z["auto_restream"] or 0):
            conn.execute("UPDATE restreams SET auto_restream=0, herkunft=? WHERE id=?",
                         (HERKUNFT_RUHT, z["id"]))
            ruht.append(u)
        elif h == HERKUNFT_RUHT and u in getrackt and u not in ausgeschlossen:
            conn.execute("UPDATE restreams SET auto_restream=1, herkunft=? WHERE id=?",
                         (HERKUNFT, z["id"]))
            wieder.append(u)
    return {"neu": neu, "ruht": ruht, "wieder": wieder}


def ausschliessen(liste, username):
    """Fuer cfgstore.aendern(): `username` auf die Ausschlussliste (ohne Doppel)."""
    u = _schluessel(username)
    aus = [x for x in (liste if isinstance(liste, list) else []) if isinstance(x, str)]
    if u and u not in {_schluessel(x) for x in aus}:
        aus.append(u)
    return aus


def zulassen(liste, username):
    """Fuer cfgstore.aendern(): `username` wieder von der Ausschlussliste nehmen."""
    u = _schluessel(username)
    return [x for x in (liste if isinstance(liste, list) else [])
            if isinstance(x, str) and _schluessel(x) != u]
