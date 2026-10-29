"""nc.lastvorsorge — v4.2-W108: die Drossel greift VOR dem Pixelsalat, nicht danach.

Gemeldet: „Pixelsalat, wenn mehrere getrackte Nutzer live sind und
aufgenommen und restreamt werden." Bevor hier etwas gebaut wurde, sind drei
Ursachen gegen echtes ffmpeg (6.1) nachgemessen worden — zwei sind es nicht:

1. *Abriss mitten im FLV-Strom* (`-reconnect_streamed`, ein Live-CDN schickt
   beim Wiederverbinden einen frischen Strom samt Kopf): ffmpeg meldet
   „Packet mismatch", resynchronisiert aber sauber — 0 Dekodierfehler im
   Ziel, copy wie transcode.
2. *B-Frames unter `+genpts+igndts`* (Aufnahme und Restream bei HLS): die
   dekodierten Bilder sind bitgleich zur Quelle, die Zeitstempel steigen
   streng in 40-ms-Schritten. Kein Befund.
3. *Fehlende Video-Pakete mitten im GOP* — das, was ein Live-CDN einem
   Client antut, der zu langsam liest: **69 von 502 Bildern Salat** (bestes
   Gegenstueck in der Quelle 20,8 dB statt > 59 dB), bis zum naechsten
   Keyframe. ffmpeg warnt dabei nicht einmal. Und KEIN Decoder-Schalter hilft:
   `-fflags +discardcorrupt`, `-flags -output_corrupt` und beide zusammen —
   jedes Mal dieselben 69 Bilder.

Damit ist die Kette: mehr Nutzer live → mehr parallele Transcodes (dazu die
Aufnahmen, Whisper, die Audio-Taps) → ein Transcode faellt unter Echtzeit →
er liest die Quelle zu langsam → das CDN verwirft Pakete → Salat. Der Salat
laesst sich hinterher nicht wegfiltern. Man kann nur verhindern, dass der
Transcode unter Echtzeit faellt.

Die vorhandene Drossel (W43–W61) regelt erst nach einem GEMESSENEN Rückstand
ab. Dann ist der Salat schon gesendet. Dieses Modul waehlt deshalb beim
Start eine Stufe, die in die freie Rechenzeit passt.

Die Kosten je Stufe sind nicht geschaetzt, sondern die Messung aus W61
(nc/restreamcmd.py, Kommentar ueber `drossel_fps`): Stufe 3 (Bildrate)
−19,9 %, Bildrate + Avatar aus −33,9 % — gemessen MIT verkleinerter
Leinwand, die nach derselben Messung nichts beitraegt (−18,7 gegen −19,9 %).
Deshalb tragen die heutigen Stufen 4 und 5 dieselbe Zahl. Stufe 1 und 2 (Preset, Bitrate) sind
nie gemessen worden — sie stehen deshalb mit 1,0 in der Tabelle. Eine
erfundene Ersparnis haette hier genau den Fall durchgelassen, gegen den das
Modul antritt.
"""

from typing import Optional, Tuple

# Relative Encode-Last je Drossel-Stufe (Stufe 0 = 1,0). Quelle: W61-Messung,
# drei Laeufe je Fall, Median. Ungemessenes steht auf 1,0 — siehe Modulkopf.
KOSTEN = {0: 1.0, 1: 1.0, 2: 1.0, 3: 0.80, 4: 0.66, 5: 0.66}

# Bis zu welchem Anteil der Kerne geplant wird. Nicht 1,0: das Load-Mittel
# misst Warteschlange, nicht Reserve, und ein Transcode auf exakt voller
# Maschine faellt beim ersten Ausreisser unter Echtzeit — genau der Fall,
# der den Salat erzeugt.
ZIEL_ANTEIL = 0.85

# So lange zaehlt ein frisch gestarteter Transcode zusaetzlich zum
# Load-Mittel. Das 1-Minuten-Mittel braucht etwa so lange, bis es einen neuen
# Dauerverbraucher zeigt; ohne den Aufschlag saehen zwei kurz nacheinander
# gestartete Restreams beide eine leere Maschine.
JUNG_S = 90


def freie_kerne(load1: float, kerne: int, junge_transcodes: int,
                threads_je: int) -> float:
    """Planbare Kerne nach Abzug der Last — und der Last, die gleich kommt."""
    belegt = max(0.0, float(load1)) + max(0, junge_transcodes) * max(1, threads_je)
    return max(1, int(kerne or 1)) * ZIEL_ANTEIL - belegt


def startstufe(load1: float, kerne: int, junge_transcodes: int,
               threads_je: int, stufe_jetzt: int = 0,
               stufe_max: int = 5) -> Tuple[int, Optional[str]]:
    """Mit welcher Drossel-Stufe soll ein Transcode STARTEN? -> (Stufe, Grund)

    Grund ist None, wenn nichts zu tun ist — dann ist auch nichts zu melden.
    Nie unter `stufe_jetzt`: was die Drossel schon erreicht hat, nimmt die
    Vorsorge nicht zurueck (die Drossel regelt bewusst nie hoch, siehe
    _drossel_zuruecksetzen im Bot).
    """
    bedarf = max(1, int(threads_je or 1))
    frei = freie_kerne(load1, kerne, junge_transcodes, bedarf)
    if frei >= bedarf * KOSTEN.get(stufe_jetzt, 1.0):
        return stufe_jetzt, None
    faktor = max(0.0, frei) / bedarf
    # Kein eigener Riegel gegen „unter stufe_jetzt": er waere wirkungslos.
    # Wer hier ankommt, passt mit KOSTEN[stufe_jetzt] nicht, und weil die
    # Kosten mit der Stufe nie steigen (der Vertrag haelt das fest), passt
    # auch keine kleinere Stufe.
    for s in range(stufe_max + 1):
        if KOSTEN.get(s, KOSTEN[max(KOSTEN)]) <= faktor:
            return s, ("frei %.1f von %d Kernen (Load %.1f, %d Transcode(s) "
                       "gerade gestartet), dieser braucht %d — Stufe %d "
                       "kostet gemessen %d %%"
                       % (max(0.0, frei), kerne, load1, junge_transcodes,
                          bedarf, s, round(KOSTEN.get(s, 1.0) * 100)))
    return stufe_max, ("frei %.1f von %d Kernen (Load %.1f, %d Transcode(s) "
                       "gerade gestartet) — selbst die hoechste Stufe passt "
                       "nicht. Abhilfe: weniger gleichzeitige Restreams "
                       "(RESTREAM_MAX_CONCURRENT), weniger Ziele, oder mehr "
                       "Kerne. Sonst faellt der Transcode unter Echtzeit, das "
                       "CDN verwirft Pakete, und das Bild zerfaellt."
                       % (max(0.0, frei), kerne, load1, junge_transcodes))


def jung(gestartet_mono, jetzt_mono) -> bool:
    return gestartet_mono is not None and (jetzt_mono - gestartet_mono) < JUNG_S
