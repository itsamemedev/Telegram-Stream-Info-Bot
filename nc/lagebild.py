"""nc.lagebild — v4.2-W112: was die lebende Übersicht zeigt, an EINER Stelle.

Die Übersicht trug bis hierher eine „3D-Kommandozentrale": fünf Kennzahlen
auf einem drehbaren Ring — dieselben fünf Zahlen, die in den Kacheln direkt
darüber stehen. Sie sah lebendig aus und sagte nichts, was nicht schon dastand.
Das Gegenteil von dem, was eine Leitstelle braucht.

Das Lagebild zeigt stattdessen, WAS GERADE PASSIERT: welche Nutzer live sind,
an welchem eine Aufnahme haengt, welcher Restream gesund, langsam oder
gestoert ist — und was die vierzehn Waechter (brain/agents.py) tun. Ein
Waechter, der eben gelaufen ist, steht an seinem Arbeitsort: der
Platten-Waechter an der Platte, der Aufnahme-Waechter an einer laufenden
Aufnahme, der Restream-Waechter an einem Restream, bevorzugt an einem, der
Hilfe braucht.

**Warum die Zuordnung hier steht und nicht im JavaScript:** sie ist die
eigentliche Aussage der Animation. Im Browser waere sie ungeprueft; hier
haelt ein Vertrag fest, dass ein gestoerter Restream nicht gruen gezeichnet
wird und ein abgeschalteter Waechter nicht patrouilliert. Das JS bewegt nur
noch, was dieses Modul entschieden hat.

**Unterscheiden, ob nichts da ist oder nichts geladen wurde** (CLAUDE.md,
W99): `quellen` sagt je Quelle, ob sie gelesen werden konnte. Ein Brain, das
nicht antwortet, ist kein Lagebild ohne Waechter.
"""

# Wie lange ein Waechter nach seinem Lauf als „taetig" gilt. Die Laeufe selbst
# dauern Millisekunden; ohne Nachlauf saehe ein 8-s-Poll sie fast nie. 20 s
# sind zwei Polls Luft und kurz genug, dass „steht an der Platte" noch
# „hat gerade nach der Platte gesehen" heisst.
import logging

log = logging.getLogger("TikTokBot")

TAETIG_S = 20.0

# Ab hier sendet ein Restream nicht mehr, obwohl der Prozess lebt (W113:
# ohne_fortschritt_s). Darunter ist ein Haenger eine Delle, darueber eine
# Stoerung.
LANGSAM_AB_S = 15.0
GESTOERT_AB_S = 60.0

# Ab so vielen verpassten Takten gilt ein Waechter als ueberfaellig.
UEBERFAELLIG_TAKTE = 3

# So viele Ziele zeichnet die Übersicht hoechstens. Mehr passt nicht lesbar
# auf einen Ring; die Zahl dahinter steht als „+N".
MAX_ZIELE = 24

# Waechter -> Arbeitsort. „ziel:…" heisst: bei einem Nutzer in diesem Zustand.
# Die Namen sind die `name`-Attribute aus brain/agents.py. Ein Waechter, der
# hier fehlt, arbeitet am Kern — er erscheint, statt zu verschwinden.
# Nachgesehen an den Docstrings der Klassen, nicht am Namen: `sentinel` ist der
# CrowdSec-Waechter (Abwehr, nicht Live), `uptime` prueft die eigenen
# Chat-Verbindungen, `recovery` sucht festgefahrene Aufnahmen.
ORT = {
    "health": "kern",
    "swap": "kern",
    "disk": "platte",
    "proxy": "tunnel",
    "sentinel": "abwehr",
    "toxicity": "chat",
    "uptime": "chat",
    "analytics": "archiv",
    "learning": "archiv",
    "scout": "ziel:live",
    "recording": "ziel:aufnahme",
    "recovery": "ziel:aufnahme",
    "restream_sentinel": "ziel:restream",
    "datenbank": "datenbank",        # v4.2-W146: der vierzehnte
    # v4.2-W148: der fuenfzehnte und sechzehnte — nur registriert, wenn der
    # Dienst eingerichtet ist; die Station steht trotzdem immer.
    "prometheus": "beobachtung",
    "grafana": "beobachtung",
}

STATIONEN = ("kern", "datenbank", "platte", "tunnel", "abwehr", "chat", "archiv",
             "beobachtung")


def restream_lage(st: dict) -> str:
    """Ein Eintrag aus RestreamManager.status() -> gesund | langsam | gestoert.

    „live" allein ist der Prozess-Zustand (B123) und sagt nichts darueber, ob
    etwas ankommt. Gestoert ist ein Restream, der nicht mehr sendet, im
    Backoff steht oder dessen Ziele ALLE tot sind; langsam einer, der unter
    Echtzeit faellt, kurz haengt oder einzelne Ziele verloren hat.
    """
    st = st or {}
    ohne = st.get("ohne_fortschritt_s") or 0
    tot = st.get("targets_dead") or []
    ziele = st.get("targets") or {}
    if not st.get("live") or (st.get("backoff_s") or 0) > 0 \
            or ohne >= GESTOERT_AB_S or (ziele and len(tot) >= len(ziele)):
        return "gestoert"
    if tot or _lahm(st) or any(_lahm(r, relay=True)
                               for r in (st.get("relays") or {}).values()):
        return "langsam"
    return "gesund"


def _lahm(st, relay=False):
    """Unter Echtzeit, haengend — oder, bei einem unabhaengigen Relay
    (RESTREAM_MULTI_MODE=independent), gar nicht mehr da. Ein Relay, das
    steht, ist eine ausgefallene Plattform, waehrend der Hauptstrom weiter
    sendet: kein Totalausfall, aber auch nicht gesund (Codex-Befund auf
    PR #154 — vorher las diese Funktion nur den Hauptprozess)."""
    st = st or {}
    gesundheit = st.get("health") or {}
    return bool((relay and not st.get("pid"))
                or (st.get("ohne_fortschritt_s") or 0) >= LANGSAM_AB_S
                or gesundheit.get("slow_ticks", 0) >= 5
                or gesundheit.get("slow_warned"))


_RANG = {"gestoert": 0, "langsam": 1, "gesund": 2}


def _ziele(trackings, restreams):
    """Nur, wer gerade etwas tut: live, in Aufnahme oder im Restream. Die
    ruhenden Trackings sind eine Zahl, kein Punkt auf dem Ring."""
    rs = {}
    for r in restreams or ():
        u = (r.get("user") or "").lstrip("@").lower()
        if not u:
            continue
        lage = restream_lage(r)
        # Mehrere Restreams desselben Nutzers: der schlechteste zaehlt. Ein
        # gesunder zweiter darf einen gestoerten ersten nicht gruen faerben.
        if u not in rs or _RANG[lage] < _RANG[rs[u]]:
            rs[u] = lage
    out = {}
    for t in trackings or ():
        u = (t.get("username") or "").lstrip("@").lower()
        if not u:
            continue
        pausiert = bool(t.get("paused"))
        # Ein pausiertes Tracking fasst der Worker nicht mehr an — sein
        # last_live ist der Stand vom Moment der Pause und bliebe ewig „live"
        # (Codex-Befund auf PR #154). Dort zaehlt nur, was unabhaengig
        # bestaetigt ist: eine laufende Aufnahme oder ein Restream.
        live = bool(t.get("last_live")) and not pausiert
        rec = bool(t.get("recording"))
        if live or rec or u in rs:
            out[u] = {"name": u, "live": live or rec or u in rs,
                      "aufnahme": rec, "restream": rs.get(u),
                      "pausiert": pausiert}
    # Ein Restream ohne Tracking (manuell gestartet) ist trotzdem ein Ziel.
    for u, lage in rs.items():
        out.setdefault(u, {"name": u, "live": True, "aufnahme": False,
                           "restream": lage, "pausiert": False})
    # Feste Reihenfolge: Stoerungen zuerst, dann nach Name. Ohne sie springen
    # die Punkte bei jedem Poll auf dem Ring umher.
    return sorted(out.values(), key=lambda z: (
        _RANG.get(z["restream"], 3), not z["aufnahme"], z["name"]))


def _ziel_fuer(art, ziele, name):
    if art == "aufnahme":
        kandidaten = [z for z in ziele if z["aufnahme"]]
    elif art == "restream":
        # Bevorzugt dorthin, wo es brennt: _ziele sortiert Stoerungen vorn.
        kandidaten = [z for z in ziele if z["restream"]]
    else:
        kandidaten = [z for z in ziele if z["live"]]
    # Kein Kandidat ist eine Antwort („niemand nimmt auf"), kein Fehler.
    # Sonst: beim Restream der erste (dort brennt es), bei den anderen eine
    # feste, aber verteilte Wahl — zwei Waechter mit „ziel:live" sollen nicht
    # beide immer am selben Nutzer kleben. hash() ist je Prozess gesalzen,
    # deshalb die Buchstabensumme.
    stelle = 0 if art == "restream" else sum(map(ord, name)) % max(1, len(kandidaten))
    return kandidaten[stelle]["name"] if kandidaten else None


def _agent(a, zustand, ziele, jetzt):
    name = a.get("name") or "?"
    ort = ORT.get(name, "kern")
    vor = (jetzt - a["last_run"]) if a.get("last_run") else None
    if not a.get("enabled"):
        lage = "aus"
    elif (zustand or {}).get("state") == "error":
        lage = "fehler"
    elif vor is not None and vor < TAETIG_S:
        lage = "taetig"
    else:
        lage = "ruht"
    ziel = None
    if ort.startswith("ziel:"):
        ziel = _ziel_fuer(ort[5:], ziele, name)
        # Kein passendes Ziel: dann sieht der Waechter am Kern nach. Nie ein
        # Ziel erfinden — ein Aufnahme-Waechter an einem Nutzer, der nicht
        # aufnimmt, waere genau die Falschanzeige, die das Bild entwertet.
        ort = "ziel" if ziel else "kern"
    # v4.2-W116: der Takt jedes Waechters, damit die Uebersicht in Echtzeit
    # zeigen kann, woran er gerade ist — nicht nur die 20 s nach einem Lauf.
    # Bis hierher bewegten sich bei Takten von 120 bis 600 s im Schnitt drei
    # von dreizehn; die anderen sahen aus, als taeten sie nichts.
    takt = float(a.get("interval_s") or 0) or None
    faellig = None
    if lage != "aus" and takt:
        faellig = 0.0 if vor is None else max(0.0, takt - vor)
    # Ueberfaellig: ein aktiver Waechter, der dreimal seinen Takt verpasst
    # hat. Dann laeuft der Bridge-Tick nicht, der ihn ausloest — die eine
    # Stoerung, die man an keinem einzelnen Waechter sonst sieht.
    ueber = bool(lage in ("ruht", "taetig") and takt and vor is not None
                 and vor > UEBERFAELLIG_TAKTE * takt)
    return {"name": name, "lage": lage, "ort": ort, "ziel": ziel,
            "vor_s": None if vor is None else round(max(0.0, vor), 1),
            "takt_s": takt, "faellig_in_s": None if faellig is None else round(faellig, 1),
            "ueberfaellig": ueber,
            "laeufe": int(a.get("runs") or 0),
            "befunde": int(a.get("findings") or 0),
            "dauer_ms": a.get("last_ms"),
            "fehler": int(a.get("errors") or 0)}


# ═════════════════════════════════════════════════════════════════════════
# v5.1-W186: die Betriebsteile seit v5.0 — Schlangen, Browser, Verbindungen
# ═════════════════════════════════════════════════════════════════════════
#
# Bis v5.0 zeigte das Lagebild Nutzer, Restreams und Waechter. Seither sind
# Teile dazugekommen, die eigene Stoerbilder haben und im Deck nirgends
# zusammen stehen: die Encode-Warteschlange (W174), die Upload-Schlange
# (W175), der Discord-Versand ganzer Aufnahmen (W175), der dauerhafte
# Overlay-Browser (W170), die Tunnelwache (W105), der Kick-Chat ueber
# Centrifugo (W171) und das Spendenziel (W173). Am 11.11. stand die
# Encode-Schlange mit drei wartenden Kodierungen und die Upload-Schlange mit
# einer aufgeschobenen Aufnahme — beides nur im Log.
#
# Wie oben: WAS eine Lage ist, entscheidet diese Datei; das JS waehlt nur
# Farbe und Text zu `lage` und `grund`. Der Bot meldet seine Rohdaten ueber
# `dienst_quelle()` an (nc/ importiert nie aus bot.py); eine Quelle, die
# nicht antwortet oder nie angemeldet wurde, ist „unbekannt" — nie „ok"
# (W99: nichts geladen ist nicht dasselbe wie nichts da).

DIENSTE = ("encode", "upload", "discord_aufnahme", "overlay", "tunnel",
           "kick_chat", "spendenziel")

# Ab so langem Warten gilt eine Kodierung als Stau, nicht als Reihenfolge:
# ein Chat-Einbrennen dauert Minuten (11.11.: 539 s), der Zusammenschnitt
# danach wartet zu Recht. Eine Viertelstunde ist mehr als ein Durchgang.
ENCODE_STAU_S = 900

LAGEN = ("ok", "aktiv", "warn", "fehler", "aus", "unbekannt")

_QUELLEN = {}


def dienst_quelle(name, fn):
    """Der Bot meldet je Dienst eine Funktion an, die Rohdaten liefert."""
    if name not in DIENSTE:
        raise ValueError("unbekannter Dienst: %s" % name)
    _QUELLEN[name] = fn


def dienste_lesen(melden):
    """-> (roh, gelesen): Rohdaten je Dienst und je Dienst, ob lesbar.

    Jede Quelle einzeln abgesichert: eine Ausnahme kostet nur ihren Dienst,
    steht in `gelesen` als False und geht an `melden(name, exc)` — die Route
    meldet gedrosselt (nc.meldetakt), dieses Modul kennt keine Drossel."""
    roh, gelesen = {}, {}
    for name in DIENSTE:
        fn = _QUELLEN.get(name)
        if fn is None:
            gelesen[name] = False
            continue
        try:
            roh[name] = fn()
            gelesen[name] = True
        except Exception as e:
            gelesen[name] = False
            melden(name, e)
    return roh, gelesen


def _eintrag(name, lage, grund, **werte):
    return {"name": name, "lage": lage, "grund": grund, "werte": werte}


def _encode(r):
    laeuft, wartet = r.get("laeuft") or [], r.get("wartet") or []
    laengste = max((int(w.get("s") or 0) for w in wartet), default=0)
    w = dict(laeuft=len(laeuft), wartet=len(wartet), laengste_s=laengste,
             parallel=r.get("parallel"), arten=sorted({e.get("art", "?") for e in laeuft}))
    if wartet and laengste >= ENCODE_STAU_S:
        return "warn", "stau", w
    if laeuft or wartet:
        return "aktiv", "laeuft", w
    return "ok", "leer", w


def _upload(r):
    w = dict(wartend=int(r.get("wartend") or 0), faellig=int(r.get("faellig") or 0),
             fehlversuche=int(r.get("fehlversuche") or 0), discord=int(r.get("discord") or 0),
             fenster=r.get("fenster"))
    if w["fehlversuche"]:
        return "warn", "fehlversuch", w
    if not w["wartend"]:
        return "ok", "leer", w
    if r.get("fenster_offen"):
        return "aktiv", "sendet", w
    return "ok", "fenster_zu", w


def _discord_aufnahme(r):
    w = dict(verbunden=bool(r.get("verbunden")))
    if not r.get("an"):
        return "aus", "abgeschaltet", w
    if not r.get("verbunden"):
        # Angeschaltet, aber ohne Discord-Verbindung geht jede fertige
        # Aufnahme nur in die Schlange — das ist eine Stoerung, keine Ruhe.
        return "warn", "nicht_verbunden", w
    return "ok", "bereit", w


def _overlay(r):
    soll, dauer, lebend = (int(r.get(k) or 0) for k in ("restreams", "dauer", "lebend"))
    w = dict(restreams=soll, dauer=dauer, lebend=lebend, modus=r.get("modus"))
    if r.get("modus") != "html":
        return "aus", "anderer_modus", w
    if not soll:
        return "ok", "bereit", w
    if lebend < dauer:
        # Ein toter Dauer-Chromium heisst: das Overlay friert ein (der Writer
        # wiederholt das letzte Bild), waehrend der Restream weiterlaeuft.
        return "fehler", "browser_tot", w
    if dauer < soll:
        # Einzelschuss je Bild: das Overlay steht, kostet aber rund 0,9
        # CPU-s je Bild (W170) — der Grund, warum der Transcode lahmt.
        return "warn", "einzelschuss", w
    return "aktiv", "laeuft", w


_TUNNEL = {"ok": ("ok", "ok"), "direkt": ("aus", "kein_proxy"),
           "aus": ("aus", "abgeschaltet"), "fehler": ("fehler", "fehler")}


def _tunnel(r):
    lage, grund = _TUNNEL.get(r.get("lage"), ("unbekannt", "noch_nicht_geprueft"))
    return lage, grund, {}


def _kick_chat(r):
    w = dict(nachrichten=int(r.get("gesehen") or 0))
    if not r.get("konfiguriert"):
        return "aus", "nicht_konfiguriert", w
    if not r.get("laeuft"):
        return "aus", "abgeschaltet", w
    if not r.get("verbunden"):
        return "warn", "nicht_verbunden", w
    return "ok", "verbunden", w


def _spendenziel(r):
    ziel = float(r.get("ziel_eur") or 0)
    w = dict(ziel_eur=round(ziel, 2), aktuell_eur=round(float(r.get("aktuell_eur") or 0), 2),
             prozent=float(r.get("prozent") or 0), zeitraum=r.get("zeitraum"))
    if ziel <= 0:
        return "aus", "kein_ziel", w
    if w["prozent"] >= 100:
        return "ok", "erreicht", w
    return "ok", "laeuft", w


_BEWERTER = {"encode": _encode, "upload": _upload, "discord_aufnahme": _discord_aufnahme,
             "overlay": _overlay, "tunnel": _tunnel, "kick_chat": _kick_chat,
             "spendenziel": _spendenziel}


def dienste(roh, gelesen=None) -> list:
    """Rohdaten je Dienst -> Liste in fester Reihenfolge (DIENSTE).

    Ein Dienst ohne Rohdaten oder mit `gelesen[name] is False` ist
    „unbekannt" — nie „ok". Eine Ausnahme beim Bewerten (Rohdaten in
    unerwarteter Form) ebenso, und zwar mit eigenem Grund: sie ist ein
    Programmfehler, kein Betriebszustand."""
    roh, gelesen = roh or {}, gelesen or {}
    out = []
    for name in DIENSTE:
        r = roh.get(name)
        if gelesen.get(name) is False or not isinstance(r, dict):
            out.append(_eintrag(name, "unbekannt", "nicht_geladen"))
            continue
        try:
            lage, grund, werte = _BEWERTER[name](r)
        except (TypeError, ValueError, AttributeError) as e:
            # Rohdaten in unerwarteter Form: ein Programmfehler zwischen Bot
            # und diesem Modul — laut, denn die Zeile zeigt dann „unbekannt".
            log.error("Lagebild: Rohdaten fuer %s unlesbar (%s: %s) — der Dienst "
                      "steht als unbekannt.", name, type(e).__name__, e)
            out.append(_eintrag(name, "unbekannt", "rohdaten_unlesbar"))
            continue
        out.append(_eintrag(name, lage, grund, **werte))
    return out


def bauen(trackings, restreams, agenten, agentenzustand, jetzt,
          quellen=None, dienste_roh=None, dienste_gelesen=None) -> dict:
    """Das Lagebild aus den Rohdaten. Rein — kein Netz, keine Datenbank.

    trackings       Zeilen wie /api/trackings (username, last_live, recording, paused)
    restreams       Eintraege aus RestreamManager.status() mit "user" daneben
    agenten         AgentManager.status()
    agentenzustand  {name: brain.state-Eintrag} (fuer „error")
    jetzt           time.time()
    """
    ziele = _ziele(trackings, restreams)
    agentenzustand = agentenzustand or {}
    ags = [_agent(a, agentenzustand.get(a.get("name")), ziele, jetzt)
           for a in (agenten or ())]
    return {
        "ok": True,
        "getrackt": len(list(trackings or ())),
        "ziele": ziele[:MAX_ZIELE],
        "weitere": max(0, len(ziele) - MAX_ZIELE),
        "agenten": ags,
        "stationen": list(STATIONEN),
        "quellen": dict(quellen or {}),
        # v5.1-W186: die Betriebsteile seit v5.0 (siehe dienste()).
        "dienste": dienste(dienste_roh, dienste_gelesen),
        # Serverzeit: die Uebersicht zaehlt die Countdowns zwischen zwei
        # Abrufen selbst herunter und braucht dafuer den Bezugspunkt.
        "jetzt": round(jetzt, 1),
    }
