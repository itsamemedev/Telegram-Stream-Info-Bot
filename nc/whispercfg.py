"""nc.whispercfg — v4.1-W19: welches Whisper-Modell laeuft, und laeuft es ueberhaupt.

════════════════════════════════════════════════════════════════════════
WARUM DIESES MODUL
════════════════════════════════════════════════════════════════════════
`/api/azrael/whisper_model` schaltet das Spracherkennungs-Modell zur Laufzeit
um. Im Monolithen tat es das mit

    global _whisper_model, WHISPER_MODEL_NAME

also durch NEUBINDUNG zweier Modul-Globals. In einem Blueprint waere `global`
der Namensraum DES BLUEPRINTS: der Name im Bot bliebe unveraendert, die Route
meldete Erfolg, und der naechste Transkript-Lauf benutzte weiter das alte
Modell. Eine stille Fehlanzeige — dieselbe Falle wie bei `_MAIN_LOOP` (W116)
und `_RESTREAM_ACTIVE` (W18).

Deshalb ein **Register**: der Bot und die Route greifen auf DASSELBE Dict zu,
und wer den Namen neu bindet, aendert ihn fuer beide.

`obj` ist das geladene Modell (teuer, wird lazy geladen). Ein Modellwechsel
setzt es auf None — der naechste Transkript-Lauf laedt neu. Genau deshalb
gehoeren Name und Objekt in EIN Register: wer nur den Namen aendert und das
Objekt stehen laesst, benutzt weiter das alte Modell und sieht den neuen Namen
im Dashboard. Das waere schlimmer als gar kein Umschalten.
"""

# Register: Name UND geladenes Objekt. Beide werden neu gebunden.
MODELL = {"name": "base", "obj": None}

# Die Auswahl im Dashboard. Kein Zwang — ein eigener Name wird akzeptiert,
# faster-whisper laedt auch Modelle, die hier nicht stehen.
PRESETS = ["tiny", "base", "small", "medium", "large-v3",
           "tiny.en", "base.en", "small.en", "medium.en"]


def name() -> str:
    return MODELL["name"]


def geladen() -> bool:
    return MODELL["obj"] is not None


def waehle(neuer_name: str):
    """Modell umschalten: Name setzen, geladenes Objekt verwerfen.

    Beides in einem Zug — siehe Modul-Kopf. Gibt den gesetzten Namen zurueck.
    """
    MODELL["name"] = str(neuer_name or "").strip() or MODELL["name"]
    MODELL["obj"] = None
    return MODELL["name"]


def verfuegbar() -> bool:
    """Ist faster-whisper installiert? Nur der Import, kein Modell-Laden —
       die Frage im Dashboard lautet 'kann der Server das ueberhaupt', nicht
       'ist es schon warm'."""
    try:
        import importlib.util
        return importlib.util.find_spec("faster_whisper") is not None
    except Exception:
        return False
