"""nc.piperarbeiter — v5.2-W193: ein dauerhafter Piper-Prozess (eigenes Programm).

Wird von nc/piperdienst.py als eigener Prozess gestartet (`python -I
nc/piperarbeiter.py`), nie importiert. Er laedt piper und onnxruntime EINMAL,
haelt geladene Stimmen (hoechstens drei) und schreibt je Anfrage eine WAV —
dieselbe Datei, die `piper -m <modell> -f <aus> --length-scale <x>` schriebe.

Warum ein eigener Prozess: onnxruntime rechnet mit eigenen Threads und eigenem
Speicher; im Bot teilten sie sich den GIL und den Heap mit allem anderen, und
eine haengende Synthese liesse sich nicht beenden. So beendet der Dienst den
Prozess bei Zeitueberschreitung wie vorher den Einzelaufruf.

Protokoll (eine JSON-Zeile je Richtung):
    Start:    -> {"bereit": true, "version": "1.4.2"}
    Anfrage:  <- {"modell": "/pfad/x.onnx", "text": "...", "aus": "/pfad/y.wav", "laenge": 1.0}
    Antwort:  -> {"ok": true} | {"ok": false, "fehler": "..."}
Endet bei EOF auf stdin.
"""

import json
import sys
import wave

_STIMMEN_MAX = 3


def _antwort_melden(ausgabe, daten):
    """Eine Protokollzeile an den Bot — auch fuer jeden Fehler die Meldung."""
    ausgabe.write(json.dumps(daten) + "\n")
    ausgabe.flush()


def _sprechen(piper, stimmen, anfrage):
    modell = anfrage["modell"]
    stimme = stimmen.pop(modell, None) or piper.PiperVoice.load(modell)
    stimmen[modell] = stimme                       # zuletzt benutzt ans Ende
    while len(stimmen) > _STIMMEN_MAX:
        stimmen.pop(next(iter(stimmen)))
    konfig = piper.SynthesisConfig(length_scale=float(anfrage.get("laenge") or 1.0))
    # Nicht `with wave.open(...)`: scheitert die Synthese, bevor das Format
    # gesetzt ist, wirft das Schliessen "# channels not specified" — und
    # VERDECKT den eigentlichen Grund (gefunden vom W193-Vertrag).
    wav = wave.open(anfrage["aus"], "wb")
    try:
        stimme.synthesize_wav(anfrage["text"], wav, syn_config=konfig)
    finally:
        try:
            wav.close()
        except wave.Error:
            pass        # Aufraeumen: der Grund kommt aus synthesize_wav


def main():
    ausgabe = sys.__stdout__
    try:
        import importlib.metadata as _md
        import piper
        # ab piper-tts 1.3; aeltere haben beides nicht -> AttributeError -> Einzelaufruf
        _api = (piper.PiperVoice.synthesize_wav, piper.SynthesisConfig)
        del _api
        fassung = _md.version("piper-tts")
    except (ImportError, AttributeError) as e:
        _antwort_melden(ausgabe, {"bereit": False, "grund": "%s: %s" % (type(e).__name__, e)})
        return 3
    _antwort_melden(ausgabe, {"bereit": True, "version": fassung})
    stimmen = {}
    for zeile in sys.stdin:
        try:
            _sprechen(piper, stimmen, json.loads(zeile))
        except Exception as e:                       # jeder Fehler ist eine Antwort
            _antwort_melden(ausgabe, {"ok": False, "fehler": "%s: %s" % (type(e).__name__, e)})
            continue
        _antwort_melden(ausgabe, {"ok": True})
    return 0


if __name__ == "__main__":
    sys.exit(main())
