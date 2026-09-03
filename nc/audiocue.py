"""nc.audiocue — v4.1-W20: Signalton- und Ducking-Konfiguration.

Sechs .env-Vorgaben und ein Normalisierer. Im Monolithen war das eine Funktion
plus sechs Modul-Konstanten; fuer die zwei Routen unter /api/audio waeren das
zwei nc.ctx-Eintraege gewesen (bei 24 von vertraglich 25 belegten Plaetzen).

Die Vorgaben kommen per configure(), nicht als Modul-Konstante: `.env` wird
teils erst nach den ersten Imports geladen (CLAUDE.md). Die eigentliche
Normalisierung liegt unveraendert in nc/cfgnorm.py — hier steht nur, WOHER die
Vorgaben kommen und wer den gespeicherten Wert liest.
"""

from nc import cfgnorm as _cfgnorm
from nc import cfgstore as _cfgstore

_VORGABEN = {"tone": True, "freq": 880.0, "ms": 120, "vol": 0.25,
             "gap_ms": 60, "duck": 0.9}


def configure(*, tone=None, freq=None, ms=None, vol=None, gap_ms=None, duck=None):
    for name, wert in (("tone", tone), ("freq", freq), ("ms", ms),
                       ("vol", vol), ("gap_ms", gap_ms), ("duck", duck)):
        if wert is not None:
            _VORGABEN[name] = wert


def config():
    """Die geltende Ton-Konfiguration: gespeicherter Wert vor .env-Vorgabe."""
    return _cfgnorm.normalize_audio(
        _cfgstore.get("audio.cue", None),
        _VORGABEN["tone"], _VORGABEN["freq"], _VORGABEN["ms"],
        _VORGABEN["vol"], _VORGABEN["gap_ms"], _VORGABEN["duck"])
