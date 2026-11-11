"""nc.zeitglaetter — v4.2-W179: Zeitstempel-Spruenge der TikTok-Quelle glaetten.

════════════════════════════════════════════════════════════════════════
DER BEFUND (Betreiber-Server, ffmpeg 6.1.1, Aufnahme -c copy nach mp4)
════════════════════════════════════════════════════════════════════════
    [mp4 @ …] pts has no value
    [vost#0:0/copy @ …] Non-monotonic DTS; previous: 4448, current: 4358; changing to 4449
    [vist#0:0/h264 @ …] timestamp discontinuity (stream id=0): -11989666, new offset= …
    [aost#0:1/copy @ …] Non-monotonic DTS; previous: 8648703, current: 8648543; changing to …

Gemeldet dazu: Aufnahmen mit Pixelsalat und/oder fehlendem Ton. Nachgestellt
mit echtem ffmpeg 6.1 (Testquelle 25 fps, B-Frames, Spruenge um ±12 s wie
beim CDN-Reconnect), Aufnahmebefehl unveraendert aus nc.reccmd:

    Fall                 heute                          geglaettet
    HLS ohne Sprung      0 Dekodierfehler               0
    HLS  -12 s           129 Fehler (PTS-Reihenfolge)   0
    HLS  +12 s           199 Fehler                     0
    HLS, PES ohne PTS    96 Fehler, „pts has no value"  0
    FLV  -12 s           8 s Bild UND Ton auf 12 ms     16 s, 0 Fehler
                         zusammengeschoben („changing
                         to …"): Standbild, Ton weg
    FLV  +12 s           12 s Standbild und Stille      16 s, 0 Fehler

Im RESTREAM dasselbe eine Schicht weiter: der Zubringer der Sendebruecke
kopiert das Bild, und `TsUmschreiber` legt seinen Versatz einmal je Abschnitt
fest — ein Sprung mitten im Abschnitt ging unveraendert an den Sender. Gemessen
(FLV -12 s, 22 s Lauf, lokaler RTMP-Empfaenger): der Sender korrigierte acht
„timestamp discontinuity" und lieferte dem Ziel nur 10,4 s Ausgabe — rund 11 s
bekam die Plattform nichts, und genau dann trennt Kick die Verbindung
(„nicht entgegengenommen"). Geglaettet: 20,4 s, keine Korrektur. Ein Sprung
VORWAERTS laesst den Zubringer unter -re schlafen; das faengt die Bruecke wie
jeden Haenger mit dem Pausenbild ab (vorher wie nachher 6,9 s).

Zwei Ursachen. (1) `+igndts` (B60) wirft bei HLS die DTS weg; zusammen mit
der Diskontinuitaets-Korrektur des HLS-Demuxers bekommen B-Frames danach
eine falsche Dekodierreihenfolge — das ist der Pixelsalat. +genpts allein
fuellt fehlende PTS genauso. (2) Der FLV-Demuxer kennt keine Diskontinuitaet:
ffmpeg reicht einen Sprung unveraendert an den mp4-Muxer, und der „repariert"
jeden rueckwaerts laufenden Zeitstempel auf vorher+1 — bis die Quelle wieder
aufgeholt hat.

DIE ANTWORT: der Bitstream-Filter `setts` je Strom. Er schreibt die Zeit
fort als vorheriger Ausgang + Schritt der Quelle. Ein Schritt, der
rueckwaerts laeuft oder ueber SPRUNG_S liegt, ist kein Inhalt, sondern ein
Sprung, und zaehlt als ein Paket. Bild und Ton verlieren dabei denselben
Sprung, bleiben also beieinander. Echter Inhalt kommt nie weg — nur die Zeit,
in der keiner kam.
"""
import functools
import logging
import subprocess

log = logging.getLogger("nc.zeitglaetter")

# Groesster Schritt zwischen zwei Paketen eines Stroms, der noch als Inhalt
# gilt. TikToks Spruenge liegen bei ±12 s (Log oben); ein normaler Schritt
# bei 40 ms (Bild) bzw. 23 ms (Ton). Darunter bleibt jede echte Luecke als
# Luecke stehen.
SPRUNG_S = 5.0


def ausdruck(sprung_s=SPRUNG_S) -> str:
    """Der setts-Ausdruck fuer DTS (PTS = derselbe + PTS-DTS-Abstand).

    Kommata sind fuer den Filtergraph-Parser maskiert: `-bsf` trennt Filter
    an Kommata, eine unmaskierte Klammer zerlegte den Ausdruck."""
    schritt = "DTS-PREV_INDTS"
    return ("if(eq(PREV_OUTDTS\\,NOPTS)\\,DTS\\,PREV_OUTDTS+if(gt({s}\\,0)*lte({s}\\,{g}/TB)"
            "\\,{s}\\,max(DURATION\\,1)))").format(s=schritt, g=float(sprung_s))


def filter_text(sprung_s=SPRUNG_S) -> str:
    """`setts=dts=…:pts=…` — fuer eine -bsf-Kette."""
    d = ausdruck(sprung_s)
    return "setts=dts=%s:pts=%s+PTS-DTS" % (d, d)


@functools.lru_cache(maxsize=4)
def verfuegbar(ffmpeg="ffmpeg") -> bool:
    """Kennt dieses ffmpeg den Filter? setts gibt es seit 4.4.

    Ein unbekannter Bitstream-Filter laesst ffmpeg gar nicht erst anfangen —
    das wuerde JEDE Aufnahme brechen, nicht nur die mit Spruengen. Deshalb
    einmal nachsehen und laut sagen, wenn er fehlt."""
    try:
        r = subprocess.run([ffmpeg, "-hide_banner", "-bsfs"], capture_output=True,
                           text=True, timeout=10)
        da = "setts" in r.stdout.split()
    except (OSError, subprocess.SubprocessError) as e:
        log.warning("Zeitstempel-Glaettung: ffmpeg nicht befragbar (%s) — Aufnahmen "
                    "laufen ohne; Spruenge der Quelle gehen dann ungefiltert in die Datei.", e)
        return False
    if not da:
        log.warning("Zeitstempel-Glaettung: dieses ffmpeg kennt den Filter 'setts' nicht "
                    "(erst ab 4.4) — Aufnahmen laufen ohne. Folge bei CDN-Reconnects: "
                    "Standbild, fehlender Ton. Abhilfe: ffmpeg aktualisieren.")
    return da


def bsf_args(ton_vorher=None, ffmpeg="ffmpeg") -> list:
    """-bsf-Argumente fuer Bild und Ton einer copy-Ausgabe.

    `ton_vorher`: ein Ton-Filter, der schon vorgesehen ist (aac_adtstoasc
    bei HLS). Zwei `-bsf:a` hintereinander ueberschreiben sich — der zweite
    gewinnt still. Deshalb eine Kette."""
    if not verfuegbar(ffmpeg):
        return ["-bsf:a", ton_vorher] if ton_vorher else []
    f = filter_text()
    ton = (ton_vorher + "," + f) if ton_vorher else f
    return ["-bsf:v", f, "-bsf:a", ton]
