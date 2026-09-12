"""nc.avatarloop — v4.2-W62: welche Avatar-Schleife gehoert gerade ins Bild?

Der Bestand kannte zwei Zustaende, und die Entscheidung dazwischen stand als
eine Zeile mitten im Writer-Thread des Frame-Feeders:

    jetzt = _azrael_spricht()

Damit gab es genau zwei Bilder von AZRAEL: er redet, oder er steht in seiner
Drei-Sekunden-Schleife. Der Betreiber hat den fehlenden dritten benannt: „Der
Avatar braucht idle/afk Animationen." Eine Figur, die stundenlang dieselben
drei Sekunden abspielt, waehrend im Chat nichts passiert, liest sich als
eingefrorenes Standbild — und ein eingefrorener Avatar sieht genauso aus wie
ein abgestuerzter Restream.

WARUM ALS EIGENES MODUL und nicht als zweite Zeile im Writer: der Writer
laeuft in einem Thread, dessen Ausgabe eine FIFO ist. Was dort entschieden
wird, laesst sich nicht pruefen, ohne ffmpeg zu starten. Hier steht dieselbe
Entscheidung als reine Funktion — kein Zustand, keine Uhr, kein Import aus
bot.py. Dieselbe Bauart wie nc/livefolge.py (W51) und nc/audiotap.py (W55),
und aus demselben Grund: die schwierige Haelfte ist die Entscheidung, nicht
das Abspielen.
"""

import math

# Die drei Zustaende. Sie sind zugleich die DATEINAMEN der Schleifen
# (ruhe.webm, sprich.webm, afk.webm) und die Schluessel im Frame-Feeder —
# genau eine Schreibweise, damit ein Tippfehler nicht still auf die
# Ruheschleife zurueckfaellt.
RUHE = "ruhe"
SPRICH = "sprich"
AFK = "afk"
ZUSTAENDE = (RUHE, SPRICH, AFK)

# Nach so vielen Sekunden ohne Chat und ohne AZRAEL geht die Figur in die
# AFK-Schleife. 90 s ist bewusst lang: in einem lebhaften Stream soll sie nie
# greifen, sonst wechselt der Avatar staendig die Haltung und das ist
# unruhiger als eine Schleife, die sich wiederholt.
AFK_NACH_S = 90.0


def ruhe_seit(jetzt, *stempel):
    """Sekunden seit der juengsten Aktivitaet. -> float, nie negativ.

    `stempel` sind Zeitpunkte derselben Uhr wie `jetzt` — die letzte
    Chat-Nachricht, AZRAELs letzte Reaktion, und der Start des Feeders.

    DER FEEDER-START MUSS MIT HINEIN. Ohne ihn stuende die Figur beim
    Stream-Beginn sofort in AFK, weil noch niemand etwas geschrieben hat: das
    Sendebild ginge mit einem schlafenden Avatar auf Sendung. Ein leeres
    `stempel` (nichts bekannt) gilt deshalb als „gerade eben", nicht als „seit
    jeher nichts".

    Nie negativ: die Stempel kommen aus zwei Quellen, und eine Uhr, die um
    Millisekunden vorlaeuft, wuerde sonst eine negative Ruhezeit liefern —
    harmlos hier, aber ein negativer Wert in einem Vergleich ist die Art
    Kleinigkeit, die spaeter jemand eine Stunde kostet.
    """
    echte = [s for s in stempel if s]
    if not echte:
        return 0.0
    return max(0.0, float(jetzt) - max(echte))


def zustand(spricht, ruhe_s, afk_nach_s=AFK_NACH_S):
    """Welche Schleife jetzt? -> "sprich" | "ruhe" | "afk"

    Sprechen gewinnt immer: sagt AZRAEL gerade etwas, ist er per Definition
    nicht abwesend, egal wie lange der Chat davor still war.

    `afk_nach_s <= 0` schaltet den dritten Zustand ab — dann verhaelt sich
    alles wie vor W62. Das ist der Rueckweg fuer den Fall, dass die
    AFK-Haltung im Betrieb nicht gefaellt: eine Zahl in der .env, kein
    Codeeingriff.
    """
    if spricht:
        return SPRICH
    if afk_nach_s > 0 and float(ruhe_s) >= float(afk_nach_s):
        return AFK
    return RUHE


def schleife(zust, vorrat):
    """Die Frames fuer `zust`, mit Rueckfall auf Ruhe. -> (frames, echter_zustand)

    `vorrat` ist {zustand: frames}. Fehlt eine Schleife — und die
    AFK-Schleife FEHLT in jedem Bestand, der den Bildergenerator seit W62
    nicht neu laufen liess —, dann spielt die Ruheschleife weiter, statt dass
    der Avatar verschwindet. Zurueck kommt auch, was tatsaechlich gespielt
    wird: nur so kann der Aufrufer melden, dass eine Schleife fehlt, statt
    stumm etwas anderes zu zeigen.
    """
    f = (vorrat or {}).get(zust)
    if f:
        return f, zust
    return (vorrat or {}).get(RUHE), RUHE


def blinzeln(t, periode, staerke=30.0, schaerfe=24):
    """Ein kurzes Zufallen der Augen. -> Abzug auf die Augenhelligkeit.

    Bewusst OHNE Modulo gerechnet. Der Naht-Vertrag aus W53 vergleicht
    bewegung(t) mit bewegung(t + Schleifenlaenge) auf 1e-9 genau; `t % p`
    liefert dort je nach Gleitkomma-Rest minimal andere Werte und der Vertrag
    kippt an einer Stelle, an der die Bewegung in Ordnung ist. Eine hohe
    Potenz des angehobenen Kosinus ist dagegen exakt periodisch und dabei
    genauso spitz: bei `schaerfe`=24 dauert das Zufallen rund ein Zehntel der
    Periode.

    Phase so gelegt, dass das Auge bei t=0 OFFEN ist — sonst begaenne jede
    Schleife mit einem geschlossenen Auge, und beim Umschalten von Ruhe auf
    AFK blinzelte die Figur genau im Moment des Wechsels.
    """
    return staerke * (0.5 - 0.5 * math.cos(2 * math.pi * t / periode)) ** schaerfe
