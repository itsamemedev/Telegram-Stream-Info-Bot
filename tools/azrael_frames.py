#!/usr/bin/env python3
"""tools/azrael_frames.py — die Animationsschleifen des AZRAEL-Avatars bauen.

WARUM VORGERENDERT UND NICHT ZUR LAUFZEIT:
Pillow ist KEINE Laufzeit-Abhaengigkeit des Bots (steht nicht in
requirements.txt und wird nirgends importiert). Ein Avatar, der sich zur
Laufzeit selbst zeichnet, haette also erst ein Bildpaket in den Serverbestand
gezogen — fuer eine Figur, die sich immer gleich bewegt. Stattdessen laufen
die Frames EINMAL hier durch und liegen fertig im Repo; der Live-Pfad liest
nur noch Dateien.

WARUM AUS EINEM EINZIGEN BILD:
Die Vorlage ist ein Standbild. Bewegung entsteht durch Teil-Ebenen, die
gegeneinander verschoben werden — Kiefer faellt, Schwertarm dreht um den
Unterarm, Aura pulsiert, Augen glimmen. Die Ebenen tragen ABSICHTLICH einen
grosszuegigen dunklen Rand: beim Verschieben deckt eine Ebene damit ihre
eigene alte Lage zu. Ohne diesen Rand steht die Klinge doppelt im Bild.

DIE RIG-PUNKTE sind am Original (1024x1024) ausgemessen, nicht geschaetzt:
Lippenlinie y=495, Mundmitte x=521, Augen (455,321) und (612,318),
Unterarm-Drehpunkt (800,795). Wer die Vorlage austauscht, muss sie neu messen.

WARUM WEBM + EINE ALPHA-DATEI STATT EINER PNG-SEQUENZ:
46 Einzel-PNGs sind 11 MB — das gehoert nicht in ein Repo. VP9 packt dieselben
Frames auf 53 KB, kann aber KEINE Transparenz (ffmpegs libvpx-vp9 verwirft den
Alphakanal wortlos, ffprobe zeigt danach yuv420p statt yuva420p). APNG kann
Alpha, ist mit 14,6 MB aber noch schlimmer. Ausweg: die Alpha ist bei allen 46
Frames BITGLEICH (die Vignette haengt nicht von der Pose ab), also einmal als
11-KB-Graustufenbild daneben. Der Filtergraph fuegt beides mit alphamerge
wieder zusammen. Ergebnis 122 KB statt 11 MB.

Aufruf:  python tools/azrael_frames.py <vorlage.png>
"""

import math
import os
import shutil
import subprocess
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# v4.2-W62: die Namen der Schleifen kommen aus nc.avatarloop, nicht aus einer
# zweiten Liste hier. Der Feeder in bot.py sucht die Dateien nach genau diesen
# Namen — zwei Listen waeren zwei Wahrheiten, und die Abweichung faellt erst
# im Sendebild auf (fehlende Schleife = stiller Rueckfall auf Ruhe).
from nc.avatarloop import AFK, RUHE, SPRICH, ZUSTAENDE, blinzeln     # noqa: E402

# Pillow wird ERST in den zeichnenden Funktionen geholt, nicht hier oben.
# Grund: die Bewegungsrechnung (bewegung()) soll in der CI pruefbar sein, und
# dort ist Pillow nicht installiert — es steht bewusst weder in
# requirements.txt noch in requirements-smoke.txt. Ein Import auf Modulebene
# haette jeden Vertrag ueber die Rig-Winkel unmoeglich gemacht.
Image = ImageChops = ImageDraw = ImageFilter = None


def _pil():
    """Pillow nachladen und die vier Namen global setzen. Einmal pro Lauf."""
    global Image, ImageChops, ImageDraw, ImageFilter
    if Image is None:
        try:
            from PIL import Image as _I, ImageChops as _C
            from PIL import ImageDraw as _D, ImageFilter as _F
        except ImportError as e:
            raise SystemExit("Pillow noetig: python -m pip install Pillow "
                             "(nur hier, nicht auf dem Server)") from e
        Image, ImageChops, ImageDraw, ImageFilter = _I, _C, _D, _F

ZIEL = os.path.join("assets", "azrael")
HOEHE = 360                 # Kantenlaenge der fertigen Frames
FPS = 10                    # Takt der Schleifen
RUHE_S = 3.0                # Laenge der Ruheschleife
SPRECH_S = 1.6              # Laenge der Sprechschleife
# v4.2-W62. Doppelt so lang wie die Ruheschleife, und das ist der Punkt: eine
# AFK-Figur soll nicht schneller wiederkehren als die aktive. Sechs Sekunden
# teilen sich sauber in 3.0, 2.0, 1.5, 1.2 und 1.0 — genug Perioden fuer eine
# Bewegung, die sich nicht offensichtlich wiederholt, ohne die Naht zu brechen.
AFK_S = 6.0                 # Laenge der AFK-Schleife
# Ueber ZUSTAENDE aufgebaut und nicht von Hand aufgezaehlt: kommt spaeter ein
# vierter Zustand dazu, faellt hier ein KeyError beim Import — statt dass der
# Generator still zwei Schleifen schreibt und die dritte im Betrieb fehlt.
_LAENGE = {RUHE: RUHE_S, SPRICH: SPRECH_S, AFK: AFK_S}
SCHLEIFEN = tuple((z, _LAENGE[z]) for z in ZUSTAENDE)

# --- am Original ausgemessen -------------------------------------------------
LIPPE = 495
MUND_X, MUND_B = 521, 104
AUGEN = ((455, 321), (612, 318))
ARM_DREHPUNKT = (800, 795)
ARM_BOX = (672, 118, 1030, 830)      # Klinge + Faust samt dunklem Rand
KIEFER_BOX = (432, 486, 608, 600)
ZUSCHNITT = (70, 0, 985, 940)        # Totraum weg, beide Pauldrons drin

# v4.2-W53 — drei weitere Rig-Punkte, am selben Original ausgemessen.
#
# Bis hierher bewegte sich am Avatar der Kiefer, die Aura, die Augen und der
# Arm ALS EIN STUECK. Der Kopf stand still, und Faust und Klinge waren
# aneinandergenagelt: ARM_BOX deckt beide ab und dreht sie um denselben
# Punkt. Eine Figur, deren Kopf sich drei Minuten lang nicht ruehrt, liest
# sich als Standbild mit zuckendem Mund.
#
# KOPF_BOX ist bewusst KEIN Umriss der Kapuze, sondern eine Ellipse ueber
# Gesicht und Innenkapuze. Die aeussere Kapuze faellt ueber die Schultern —
# dreht man sie mit, reisst sie dort auf. Die Maske laeuft deshalb oberhalb
# des Halses weich aus (_kopf_maske), und der Drehpunkt liegt genau in diesem
# ausgelaufenen Rand: dort bewirkt die Drehung fast nichts, und die Naht
# bleibt unsichtbar.
KOPF_BOX = (300, 10, 740, 570)
KOPF_DREHPUNKT = (521, 561)          # Halsansatz, unter dem Kinn
KOPF_SAUM = 545                      # ab hier blendet die Kopfmaske aus

# Der Griff sitzt IN der Faust: dreht die Klinge um ihn, wischt sie durch
# das Bild, waehrend die Faust sie haelt. Drehte sie um den Unterarm (wie
# bisher), wanderte die Faust mit und die Bewegung sah aus wie ein
# Achselzucken.
KLINGE_BOX = (755, 78, 1000, 588)
KLINGE_DREHPUNKT = (800, 640)        # Griffmitte, in der Faust

# Das Handgelenk liegt UNTERHALB der Faust — der Unterarm kommt von unten.
HAND_BOX = (692, 580, 867, 762)
HAND_DREHPUNKT = (780, 770)


def bewegung(t, zust):
    """Alle Rig-Groessen fuer den Zeitpunkt t. -> dict, keine Bilder.

    `zust` ist einer aus nc.avatarloop.ZUSTAENDE. Bis v4.2-W62 stand hier ein
    Boolescher `spricht` — mit dem dritten Zustand geht das nicht mehr, und
    ein `spricht=False, afk=True` waeren zwei Flaggen fuer eine Entscheidung,
    die genau einen Wert hat.

    v4.2-W53. Getrennt vom Zeichnen, damit die Bewegung ohne Pillow pruefbar
    ist: Pillow steht bewusst in keiner requirements-Datei, ein Vertrag ueber
    die Winkel waere sonst in der CI nicht lauffaehig.

    **JEDE Periode muss ihre Schleifenlaenge ganzzahlig teilen.** Das Ergebnis
    ist eine Schleife: nach RUHE_S bzw. SPRECH_S springt der Feeder zurueck
    auf t=0. Eine Schwingung, die dort nicht gerade eine ganze Zahl von
    Durchlaeufen hinter sich hat, steht am Nahtpunkt auf einem anderen Wert
    als am Anfang — und das Glied zuckt einmal pro Runde.

    Genau das tat der Bestand in der Sprechschleife: Arm auf 1.15 s, Aura und
    Augen auf 1.4 s, bei 1.6 s Schleifenlaenge. Das sind 1.39 bzw. 1.14
    Durchlaeufe — der Arm sprang alle 1,6 Sekunden. Solange sich sonst nichts
    bewegte, ging das unter; mit einem mitschwingenden Kopf faellt es auf.
    Ein Vertrag rechnet die Teilbarkeit jetzt nach.

    **Unterschiedlich aussehen muessen die Glieder trotzdem** — sonst wirkt
    die Figur wie ein Mechanismus, der einen Takt abarbeitet. Das leisten
    hier die PHASEN, nicht krumme Perioden: gleiche (oder harmonische)
    Periode, verschobener Nulldurchgang. Kopf, Arm und Hand erreichen ihren
    Umkehrpunkt dadurch nie gemeinsam, und die Schleife bleibt trotzdem dicht.

    Warum der Kopf so wenig bekommt (1.4 Grad in Ruhe, 2.6 beim Sprechen):
    er ist das groesste Glied. Ein Grad am Hals sind an der Kapuzenspitze
    schon zehn Pixel — bei 350x360 ist das deutlich sichtbar. Was am Arm
    lebendig aussieht, sieht am Kopf aus wie ein Wackelkopf.
    """
    def w(amplitude, periode, phase=0.0):
        return amplitude * math.sin(2 * math.pi * t / periode + phase)

    if zust == AFK:
        # Einmal gerechnet, zweimal gebraucht: die Glut geht aus UND das Lid
        # faellt. Zwei getrennte Aufrufe waeren zwei Wahrheiten ueber
        # denselben Lidschlag.
        _bl = blinzeln(t, AFK_S / 2)
        # Schleife AFK_S = 6.0 s -> erlaubt sind 6.0, 3.0, 2.0, 1.5, 1.2, 1.0 …
        #
        # AFK IST EINE HALTUNG, KEIN LANGSAMERES ZAPPELN. Der erste Entwurf
        # nahm nur die Ruhewerte und halbierte sie — das Ergebnis war von der
        # Ruheschleife nicht zu unterscheiden, weil die Amplituden dort ohnehin
        # bei ein bis zwei Grad liegen. Der Unterschied muss im FESTEN VERSATZ
        # stecken: Kinn auf die Brust, Klingenspitze gesenkt. Daran erkennt
        # man die Abwesenheit auf den ersten Blick, auch im Standbild.
        #
        # Still stehen darf sie trotzdem nicht. Ein bewegungsloser Avatar ist
        # im Sendebild von einem abgestuerzten Restream nicht zu unterscheiden
        # — genau die Verwechslung, die dieses Projekt sonst ueberall vermeidet.
        return {
            "kopf_grad":   w(1.1, AFK_S),
            # +5 = Kinn nach unten (positives kopf_hoch versetzt die Ebene
            # nach unten, siehe frame()). Das Atmen darueber ist langsam und
            # klein: es soll auffallen, DASS sie noch lebt, nicht wie.
            "kopf_hoch":   5.0 + w(2.0, AFK_S / 2, 1.9),
            "arm_grad":    w(0.8, AFK_S, 2.6),
            # Klinge gesenkt. Der Griff bleibt in der Faust (der Drehpunkt
            # liegt dort), es faellt also nur die Spitze — kein Wegrutschen
            # der ganzen Waffe.
            "klinge_grad": -4.0 + w(1.2, AFK_S, 0.7),
            "hand_grad":   w(0.7, AFK_S, 4.2),
            "mund_auf":    0.0,
            # Aura heruntergefahren, aber nicht aus: die Figur glimmt weiter.
            "aura":        0.08 + w(0.05, AFK_S),
            # Halb geschlossene Augen, dazu alle drei Sekunden ein Blinzeln.
            # 34 - 30 heisst: im Zufallen bleibt ein Rest von vier, das Auge
            # wird dunkel statt schwarz. Ein hart auf 0 fallender Wert liest
            # sich als Bildfehler, nicht als Lid.
            "augen":       34.0 + w(12.0, AFK_S / 2) - _bl,
            # Das Lid ist der eigentliche Lidschlag. Die Glut wegzunehmen
            # genuegt NICHT: die Vorlage hat schon leuchtende Augen, und das
            # Leuchten kommt per screen OBEN DRAUF. Gemessen faellt der
            # Augenkasten dabei bloss von 63 auf 55 — 13 Prozent, das liest
            # kein Zuschauer als Blinzeln. Erst das Abdunkeln in frame()
            # macht daraus ein zufallendes Auge.
            "lid":         _bl / 30.0,
        }
    if zust == SPRICH:
        # Schleife SPRECH_S = 1.6 s -> erlaubt sind 1.6, 0.8, 0.4, 0.32, 0.2 …
        return {
            "kopf_grad":   w(2.6, 1.6),          # dreht ueber den ganzen Satz
            "kopf_hoch":   w(3.4, 0.8, 0.5),     # nickt in die Betonung
            "arm_grad":    w(2.4, 0.8, 1.1),
            "klinge_grad": w(3.2, 0.8, 0.7),
            "hand_grad":   w(1.8, 1.6, 2.0),
            "mund_auf":    13.0 - 13.0 * math.cos(2 * math.pi * t / 0.40),
            "aura":        0.30 + w(0.22, 1.6),
            "augen":       120.0 + w(70.0, 0.8),
            "lid":         0.0,        # beim Sprechen blinzelt niemand
        }
    # Schleife RUHE_S = 3.0 s -> erlaubt sind 3.0, 1.5, 1.0, 0.75, 0.6 …
    return {
        "kopf_grad":   w(1.4, RUHE_S),
        "kopf_hoch":   w(2.6, RUHE_S, 1.9),
        "arm_grad":    w(1.0, RUHE_S, 2.6),
        "klinge_grad": w(1.8, RUHE_S / 2, 0.7),
        "hand_grad":   w(0.9, RUHE_S, 4.2),
        "mund_auf":    0.0,
        "aura":        0.14 + w(0.10, RUHE_S),
        "augen":       70.0 + w(26.0, RUHE_S / 2),
        "lid":         0.0,
    }


def _ellipse(groesse, box, weich, wert=255):
    m = Image.new("L", groesse, 0)
    ImageDraw.Draw(m).ellipse(box, fill=wert)
    return m.filter(ImageFilter.GaussianBlur(weich)) if weich else m


def _masken(groesse):
    """Alle Ebenenmasken — und zwar UEBERSCHNEIDUNGSFREI. -> dict

    Der Kiefer wird oberhalb der Lippenlinie abgeschnitten, sonst wandert die
    Nase mit und das Gesicht verschmiert (daran ist der erste Entwurf
    gescheitert).

    v4.2-W53, und hier steckt die Lehre der Welle: **jedes Pixel darf zu
    genau EINER beweglichen Ebene gehoeren.** Der erste Entwurf hatte
    Klinge und Hand als Teilmengen des Arms und drehte nacheinander — Arm
    dreht die Klinge mit, danach dreht die Klinge nochmal. Wo die beiden
    Masken nicht deckungsgleich sind (und das sind sie nie), blieb die
    einfach gedrehte Klinge neben der doppelt gedrehten stehen: die Spitze
    stand zweimal im Bild. Das ist genau das Gespenst, vor dem der Kopf
    dieser Datei warnt, nur ueber zwei Ebenen statt ueber eine.

    Deshalb Vorrang statt Verschachtelung: Hand vor Klinge vor Kopf vor Arm.
    Was eine hoehere Ebene beansprucht, wird der niedrigeren abgezogen. Die
    Nahtkanten liegen dadurch dort, wo beide Seiten sich ohnehin fast gleich
    bewegen (Faust/Griff), und beide Masken sind weich — die Naht faellt
    nicht auf.

    Die Drehwinkel der unteren Ebenen wandern dafuer in die oberen: die
    Klinge dreht um Arm + Klinge, die Hand um Arm + Hand. Nur so wiegt der
    Arm sie noch mit, obwohl er sie nicht mehr selbst zeichnet.
    """
    kiefer = _ellipse(groesse, KIEFER_BOX, 7)
    deckel = Image.new("L", groesse, 0)
    ImageDraw.Draw(deckel).rectangle((0, 0, groesse[0], LIPPE - 3), fill=255)
    kiefer = ImageChops.subtract(kiefer, deckel.filter(ImageFilter.GaussianBlur(4)))

    hand = _ellipse(groesse, HAND_BOX, 16)
    klinge = ImageChops.subtract(_ellipse(groesse, KLINGE_BOX, 20), hand)
    kopf = ImageChops.subtract(_kopf_maske(groesse),
                               ImageChops.lighter(hand, klinge))
    belegt = ImageChops.lighter(ImageChops.lighter(hand, klinge), kopf)
    arm = ImageChops.subtract(_ellipse(groesse, ARM_BOX, 22), belegt)
    return {"kiefer": kiefer, "arm": arm, "kopf": kopf,
            "klinge": klinge, "hand": hand}


def _kopf_maske(groesse):
    """Gesicht und Innenkapuze — aber NICHT die Kapuze auf den Schultern.

    v4.2-W53. Die aeussere Kapuze faellt ueber beide Pauldrons und liegt dort
    auf. Nimmt man sie mit in die Drehung, schert sie gegen die stillstehende
    Schulter und reisst sichtbar auf. Die Maske laeuft deshalb ab KOPF_SAUM
    weich aus, und KOPF_DREHPUNKT liegt genau in diesem Auslauf: an der Naht
    ist die Maske schon fast Null, die Drehung bewirkt dort also fast nichts.

    Kein harter Schnitt, sondern ein weicher: eine Kante an dieser Stelle
    saehe aus wie ein abgetrennter Kopf, der ueber dem Rumpf schwebt.
    """
    kopf = _ellipse(groesse, KOPF_BOX, 26)
    boden = Image.new("L", groesse, 0)
    ImageDraw.Draw(boden).rectangle((0, KOPF_SAUM, groesse[0], groesse[1]), fill=255)
    return ImageChops.subtract(kopf, boden.filter(ImageFilter.GaussianBlur(30)))


def _bloom(bild):
    """Nur die ohnehin roten Stellen, stark unscharf — als Schleier zum
    Dazuschalten. Ein globaler Rot-Gain faerbt stattdessen die ganze Figur
    rosa und frisst den schwarzen Panzer."""
    r, g, b = bild.split()
    rot = ImageChops.subtract(r, ImageChops.lighter(g, b))
    return Image.merge("RGB", (rot,
                               rot.point(lambda v: v // 6),
                               rot.point(lambda v: v // 5))
                       ).filter(ImageFilter.GaussianBlur(14))


KOPF_AUSBLENDUNG = 0.26     # oberste 26 % der Hoehe weich auf 0 ziehen


def _alpha(bild):
    """Freistellen geht bei dieser Vorlage nicht: der Glow reicht bis an die
    Kante, und die Figur ist selbst fast schwarz — ein Luminanz-Key frisst
    Kapuze und Ruestung. Deshalb Superellipsen-Vignette, und erst ganz aussen
    nimmt eine sanfte Dunkel-Maske die schwarzen Ecken weg.

    v4.2-W33 — KOPF NICHT ABSCHNEIDEN: in der Vorlage beruehrt die Kapuze
    bereits die obere Bildkante, und die Vignette war dort noch voll deckend
    (Alpha 255 in der obersten Zeile). Im Sendebild stand der Kopf damit glatt
    abgeschnitten. Nach oben gibt es keine Pixel zum Nachwachsen, also blendet
    die Kapuze aus, statt zu enden — was zur Figur passt, die ohnehin aus dem
    Dunkel kommt. Unten passiert das von selbst, weil der Ellipsenmittelpunkt
    bei 0.47 liegt und der untere Rand damit weiter weg ist als der obere.
    """
    W, H = bild.size
    lum = bild.convert("L")
    maske = Image.new("L", (W, H))
    px = maske.load()
    lp = lum.load()
    for y in range(H):
        dy = (y - H * 0.47) / (H * 0.57)
        for x in range(W):
            dx = (x - W / 2.0) / (W * 0.53)
            r = (abs(dx) ** 2.8 + abs(dy) ** 2.8) ** (1 / 2.8)
            k = min(1.0, max(0.0, (1.02 - r) / 0.19))
            k = k * k * (3 - 2 * k)
            if r > 0.80:
                d = min(1.0, max(0.0, (lp[x, y] - 6.0) / 34.0)) ** 0.6
                m = min(1.0, (r - 0.80) / 0.22)
                k *= (1 - m) + m * d
            px[x, y] = int(k * 255)
    aus = int(H * KOPF_AUSBLENDUNG)
    for y in range(aus):
        t = y / aus
        f = t * t * (3 - 2 * t)          # smoothstep, kein linearer Keil
        for x in range(W):
            px[x, y] = int(px[x, y] * f)
    return maske.filter(ImageFilter.GaussianBlur(5))


def frame(basis, bloom, masken, t, zust):
    """Ein Einzelbild. t laeuft in Sekunden durch die jeweilige Schleife.

    **Jede Ebene wird aus BASIS gedreht, nie aus dem halbfertigen Bild.**
    Dreht man das Zwischenergebnis weiter, traegt die zweite Drehung die
    erste huckepack und die Ebene steht doppelt im Bild — siehe _masken().
    Aus demselben Grund wandern die Winkel der unteren Ebenen in die oberen:
    die Klinge dreht um Arm+Klinge, die Hand um Arm+Hand.

    Reihenfolge von hinten nach vorn: Arm, Kopf, Klinge, Hand. Die Faust
    haelt den Griff, sie gewinnt also im Ueberlappungsband. Mund, Aura und
    Augen kommen danach: der Kiefer setzt auf dem schon bewegten Kopf auf,
    und das Leuchten darf von keiner Drehung erfasst werden, sonst wandert
    es aus den Augenhoehlen heraus.
    """
    _pil()
    G = basis.size
    b = bewegung(t, zust)
    bild = basis.copy()

    def ebene(grad, punkt, maske, quelle=None):
        """Eine Ebene aus basis drehen und einsetzen. Unter einem Zehntelgrad
        lohnt das Resampling nicht und kostet nur Schaerfe."""
        if abs(grad) < 0.1:
            return
        return Image.composite(
            (quelle or basis).rotate(grad, resample=Image.BICUBIC, center=punkt),
            bild, maske)

    for grad, punkt, maske in (
            (b["arm_grad"], ARM_DREHPUNKT, masken["arm"]),
            (b["arm_grad"] + b["klinge_grad"], KLINGE_DREHPUNKT, masken["klinge"]),
            (b["arm_grad"] + b["hand_grad"], HAND_DREHPUNKT, masken["hand"])):
        bild = ebene(grad, punkt, maske) or bild

    # Kopf: Neigung um den Hals, dazu ein Heben und Senken. Maske und Inhalt
    # werden GEMEINSAM versetzt — versetzte man nur den Inhalt, schoebe sich
    # der Kopf unter einer feststehenden Maske durch und wuerde oben
    # abgeschnitten.
    kopf_grad, hoch = b["kopf_grad"], int(round(b["kopf_hoch"]))
    kopf_maske = masken["kopf"]
    kiefer_maske = masken["kiefer"]
    if abs(kopf_grad) >= 0.1:
        quelle = basis.rotate(kopf_grad, resample=Image.BICUBIC, center=KOPF_DREHPUNKT)
        # Der Kiefer sitzt IM Kopf: seine Maske muss dieselbe Drehung
        # mitmachen, sonst faellt der Mund neben das Kinn.
        kiefer_maske = kiefer_maske.rotate(kopf_grad, resample=Image.BICUBIC,
                                           center=KOPF_DREHPUNKT)
    else:
        quelle = basis
    if hoch:
        quelle = ImageChops.offset(quelle, 0, hoch)
        kopf_maske = ImageChops.offset(kopf_maske, 0, hoch)
        kiefer_maske = ImageChops.offset(kiefer_maske, 0, hoch)
    if abs(kopf_grad) >= 0.1 or hoch:
        bild = Image.composite(quelle, bild, kopf_maske)

    # Mund: Silbentakt. Kiefer faellt mit, und in die Hoehle kommt Glut —
    # ohne die liest ein blosses Absenken des Kinns als Rutsch, nicht als
    # Mund. Die Lippenlinie wandert mit dem Kopf, sonst haengt der offene
    # Mund in der Luft, sobald der Kopf gerade oben oder unten steht.
    auf = b["mund_auf"]
    lippe = LIPPE + hoch
    if auf >= 1.0:
        versatz = int(round(auf * 0.55))
        if versatz:
            bild = Image.composite(ImageChops.offset(bild, 0, versatz), bild,
                                   ImageChops.offset(kiefer_maske, 0, versatz))
        hoehle = _ellipse(G, (MUND_X - MUND_B // 2, lippe - 3,
                              MUND_X + MUND_B // 2, lippe + auf), 3)
        bild = Image.composite(Image.new("RGB", G, (10, 2, 3)), bild, hoehle)
        glut = _ellipse(G, (MUND_X - MUND_B // 3, lippe + auf * 0.35,
                            MUND_X + MUND_B // 3, lippe + auf), 5,
                        int(150 * min(1, auf / 18)))
        bild = ImageChops.screen(bild, Image.merge(
            "RGB", (glut, glut.point(lambda v: v // 7), glut.point(lambda v: v // 6))))

    # Aura: Schleier dazuschalten, Staerke atmet.
    bild = ImageChops.screen(bild, bloom.point(lambda v: int(v * b["aura"])))

    # Augen: glimmen mit, beim Sprechen heller. Sie sitzen im Kopf und machen
    # dessen Bewegung mit — ohne das leuchtet es neben den Hoehlen, sobald
    # der Kopf sich neigt.
    aug = Image.new("L", G, 0)
    d = ImageDraw.Draw(aug)
    hell = int(b["augen"])
    for cx, cy in AUGEN:
        d.ellipse((cx - 26, cy - 11, cx + 26, cy + 11), fill=hell)
    if abs(kopf_grad) >= 0.1:
        aug = aug.rotate(kopf_grad, resample=Image.BICUBIC, center=KOPF_DREHPUNKT)
    if hoch:
        aug = ImageChops.offset(aug, 0, hoch)
    aug = aug.filter(ImageFilter.GaussianBlur(9))
    bild = ImageChops.screen(bild, Image.merge(
        "RGB", (aug, aug.point(lambda v: v // 5), aug.point(lambda v: v // 4))))

    # v4.2-W62: DAS LID. Es kommt ZULETZT, nach der Glut — davor gesetzt
    # leuchtete das Auge durch das geschlossene Lid hindurch wieder auf.
    #
    # Der Kasten ist absichtlich groesser als der Glut-Kasten (34x16 gegen
    # 26x11): abgedunkelt werden muss die Augenhoehle der VORLAGE, und die
    # ist breiter als der Fleck, den die Glut daraufsetzt. Weichgezeichnet,
    # damit kein Rechteck im Gesicht steht.
    lid = b.get("lid", 0.0)
    if lid > 0.02:
        zu = Image.new("L", G, 0)
        dz = ImageDraw.Draw(zu)
        for cx, cy in AUGEN:
            dz.ellipse((cx - 34, cy - 16, cx + 34, cy + 16),
                       fill=int(255 * min(1.0, lid)))
        # Dieselbe Kopfbewegung wie die Glut — sonst faellt das Lid neben das
        # Auge, sobald der Kopf sich neigt.
        if abs(kopf_grad) >= 0.1:
            zu = zu.rotate(kopf_grad, resample=Image.BICUBIC, center=KOPF_DREHPUNKT)
        if hoch:
            zu = ImageChops.offset(zu, 0, hoch)
        zu = zu.filter(ImageFilter.GaussianBlur(7))
        # multiply mit dem INVERTIERTEN Lid: ausserhalb der Ellipse ist die
        # Maske 0, invertiert 255, und multiply damit die Identitaet — das
        # uebrige Bild bleibt unangetastet, ohne zweite Maske.
        offen = ImageChops.invert(zu)
        bild = ImageChops.multiply(bild, Image.merge("RGB", (offen, offen, offen)))
    return bild


def main():
    _pil()
    quelle = sys.argv[1] if len(sys.argv) > 1 else "azrael_vorlage.png"
    if not os.path.isfile(quelle):
        raise SystemExit(f"Vorlage fehlt: {quelle}")
    basis = Image.open(quelle).convert("RGB")
    masken = _masken(basis.size)
    bloom = _bloom(basis)

    zuschnitt = ZUSCHNITT
    breite = int(HOEHE * (zuschnitt[2] - zuschnitt[0]) / (zuschnitt[3] - zuschnitt[1]))
    alpha = _alpha(basis.crop(zuschnitt).resize((breite, HOEHE), Image.LANCZOS))

    if not shutil.which("ffmpeg"):
        raise SystemExit("ffmpeg noetig, um die Schleifen zu packen")

    os.makedirs(ZIEL, exist_ok=True)
    alpha.save(os.path.join(ZIEL, "alpha.png"), optimize=True)
    gesamt = os.path.getsize(os.path.join(ZIEL, "alpha.png"))

    for name, dauer in SCHLEIFEN:
        anzahl = int(round(dauer * FPS))
        with tempfile.TemporaryDirectory() as tmp:
            for i in range(anzahl):
                f = frame(basis, bloom, masken, i / FPS, name)
                f.crop(zuschnitt).resize((breite, HOEHE), Image.LANCZOS).save(
                    os.path.join(tmp, f"{i:03d}.png"))
            ziel = os.path.join(ZIEL, f"{name}.webm")
            subprocess.run(
                ["ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
                 "-framerate", str(FPS), "-i", os.path.join(tmp, "%03d.png"),
                 # VP9 traegt hier NUR die Farbe; die Transparenz liegt in
                 # alpha.png und kommt im Filtergraph per alphamerge zurueck.
                 "-c:v", "libvpx-vp9", "-pix_fmt", "yuv420p",
                 "-crf", "28", "-b:v", "0", "-an", ziel], check=True)
        gesamt += os.path.getsize(ziel)
        print(f"{name}.webm: {anzahl} Frames a {breite}x{HOEHE} @ {FPS} fps")
    print(f"gesamt {gesamt / 1024:.0f} KB in {ZIEL}/ "
          f"(alpha.png + {len(SCHLEIFEN)} Schleifen: "
          f"{', '.join(n for n, _ in SCHLEIFEN)})")


if __name__ == "__main__":
    main()
