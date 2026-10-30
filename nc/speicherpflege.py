"""nc.speicherpflege — v4.2-W120: langlebige Woerterbuecher, die nur wachsen.

Der Bot haelt rund fuenfzig Woerterbuecher auf Modul-Ebene. Die meisten
sind durch die Zahl der getrackten Nutzer begrenzt und damit harmlos. Eine
Handvoll wird aber mit Namen gefuellt, die NICHT getrackt sind — `/check`
fuer einen beliebigen Nutzer, die Quelle eines Restreams, ein Clip — und
nie geleert:

    _YTDLP_NACHSCHLAG_ZULETZT   Ruhezeit 60 s, Eintrag bleibt ewig
    _CLIP_LAST / _HYPE_CLIP_LAST  Cooldown 75 / 180 s, Eintrag bleibt ewig
    _ABO_PROBE_DONE              Drossel 6 h, Eintrag bleibt ewig
    _RATE_LIMIT_BACKOFF/_PENALTY  geleert nur, wenn `_NEXT_CHECK_AT` doppelt
                                  so gross ist wie die Tracking-Zahl — also
                                  nach vielen Untracks, nicht nach /check

Jeder Eintrag ist klein, das Wachstum langsam. Genau deshalb faellt es in
keinem Test auf und erst nach Wochen Laufzeit im RSS — und dann sieht man
nicht mehr, woher. Die Abhilfe ist nicht, die Maps umzubauen, sondern sie
nach ihrer eigenen Bedeutung zu beschneiden: ein Zeitstempel, dessen
Ruhezeit lange vorbei ist, sagt nichts mehr.

Rein rechnend, ohne Uhr: `jetzt` kommt herein. Die Woerterbuecher werden
in place beschnitten — dieselben Objekte, die der Bot liest.
"""
from __future__ import annotations


def alte_stempel_weg(d: dict, jetzt: float, aelter_als: float) -> int:
    """Eintraege mit Zeitstempel (monotonic) aelter als `aelter_als` s
       entfernen. -> wie viele. `list()` als Schnappschuss: Flask-Threads
       schreiben in manche dieser Maps nebenlaeufig (F46-B30)."""
    weg = [k for k, v in list(d.items())
           if isinstance(v, (int, float)) and jetzt - float(v) > aelter_als]
    for k in weg:
        d.pop(k, None)
    return len(weg)


def abgelaufene_weg(d: dict, jetzt: float, nachlauf: float = 0.0) -> list:
    """Eintraege mit einem Ablauf-Zeitpunkt (`bis`), der laenger als
       `nachlauf` s vorbei ist, entfernen. -> die entfernten Schluessel —
       der Aufrufer raeumt damit verbundene Maps mit ab."""
    weg = [k for k, v in list(d.items())
           if isinstance(v, (int, float)) and float(v) + nachlauf < jetzt]
    for k in weg:
        d.pop(k, None)
    return weg


def groessen(maps: dict) -> dict:
    """{name: len} fuer /healthz — nur Zahlen, keine Schluessel (das sind
       Nutzernamen)."""
    return {name: len(m) for name, m in maps.items()}
