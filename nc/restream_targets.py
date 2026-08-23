"""nc.restream_targets — SYMMETRISCHE Multistream-Ziel-Auflösung + ffmpeg-Ausgabebau.

v4.0-W77: „Kein Haupt-Restream mehr." Kick, Twitch und YouTube sind GLEICH
berechtigt. Es gibt kein Primär-Ziel: jede Plattform sendet, sobald ihre
Ingest-URL + Stream-Key gesetzt sind (global via configure() aus der Env ODER
pro Restream via Override), und jedes tee-Ziel trägt onfail=ignore — fällt eine
Plattform weg, laufen die anderen unbeirrt weiter. Die B123-Verify-Loop erkennt
echtes Sterben je Ziel separat und startet gezielt neu.

Vorher war Kick das fest verdrahtete Basis-Ziel (immer ffmpeg-Ausgang) und
Twitch/YouTube opt-in-Extras (per Default AUS). Diese Asymmetrie ist entfernt.

Rein/ohne Bot-Abhängigkeit — konfiguriert via configure(), das bot.py mit
den Env-Werten füttert. Reihenfolge (kick, twitch, youtube) ist nur stabil, NICHT
privilegierend.
"""

_ORDER = ("kick", "twitch", "youtube")

_CFG = {
    "kick_ingest": "", "kick_key": "", "kick_enabled": True,
    "twitch_ingest": "", "twitch_key": "", "twitch_enabled": True,
    "youtube_ingest": "", "youtube_key": "", "youtube_enabled": True,
}


def configure(**kw):
    """bot.py reicht die Env-Konfiguration rein. Unbekannte Keys ignoriert.
       Legacy-Keys (kick_hard) werden stillschweigend geschluckt — es gibt kein
       hartes Primär-Ziel mehr, alle Ziele sind weich (onfail=ignore)."""
    for k, v in kw.items():
        if k in _CFG:
            _CFG[k] = v
    # Legacy: kick_hard existiert nicht mehr; bewusst ignoriert.


def _norm(ingest, key):
    return ingest.rstrip("/") + "/" + key


def _platform_target(name, overrides=None):
    """(name, url) für EINE Plattform, wenn aktiv+konfiguriert — sonst None.
       overrides: {name: (ingest, key)} pro Restream (schlägt die Env-Globals)."""
    if not _CFG.get(f"{name}_enabled", True):
        return None
    ing = key = ""
    if overrides and name in overrides:
        ing, key = (overrides[name] or ("", ""))
        ing, key = (ing or "").strip(), (key or "").strip()
    if not (ing and key):
        ing, key = _CFG.get(f"{name}_ingest", ""), _CFG.get(f"{name}_key", "")
    if ing and key:
        return (name, _norm(ing, key))
    return None


def active_targets(overrides=None):
    """Alle gleichberechtigten Ziele als [(name, url), …] — jede aktive,
       konfigurierte Plattform. Keine ist „primär". Leer = nichts konfiguriert."""
    out = []
    for name in _ORDER:
        t = _platform_target(name, overrides)
        if t:
            out.append(t)
    return out


def _slot(url, soft=True):
    of = ":onfail=ignore" if soft else ""
    return f"[f=flv{of}:flvflags=no_duration_filesize]{url}"


def build_output_args(targets):
    """ffmpeg-Ausgabe für eine FLACHE Zielliste [(name, url), …] — alle gleich.

    - 0 Ziele → [] (Aufrufer muss vorher prüfen; ohne Ziel kein Sinn).
    - 1 Ziel  → schlichtes -f flv (bewährter Single-Pfad, identisch zu früher).
    - >1 Ziel → tee-Muxer, JEDES Ziel mit onfail=ignore (echte Gleichbehandlung:
      fällt eine Plattform, senden die anderen weiter; der geteilte TikTok-Input
      reißt nicht ab).

    URLs bleiben ROH (kein Backslash-Escaping der ':' ) — der Bot startet ffmpeg
    über exec (keine Shell); der tee-Muxer parst rtmps://host:443/app/key korrekt.
    """
    urls = [u for _n, u in targets]
    if not urls:
        return []
    if len(urls) == 1:
        return ["-f", "flv", "-flvflags", "no_duration_filesize", urls[0]]
    outs = [_slot(u, soft=True) for u in urls]
    return ["-flags", "+global_header", "-f", "tee", "|".join(outs)]


def single_output_args(target):
    """Ausgabe-Argumente für GENAU EIN Ziel (unabhängiger Relay-Prozess)."""
    return ["-f", "flv", "-flvflags", "no_duration_filesize", target]


# ──────────────────────────────────────────────────────────────────────────
# Rückwärtskompatible Helfer — bestehende Aufrufer/Contracts weiter bedienen.
# ──────────────────────────────────────────────────────────────────────────
def multistream_targets(overrides=None):
    """Legacy: „Zusatz"-Ziele = alle aktiven AUSSER kick. Es gibt zwar kein
       Primär-Ziel mehr, aber ein paar Aufrufer (Status/Labels) fragen weiter
       nach den Nicht-Kick-Zielen. Liefert Twitch/YouTube, sobald konfiguriert."""
    return [(n, u) for n, u in active_targets(overrides) if n != "kick"]
