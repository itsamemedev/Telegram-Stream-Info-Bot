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

try:
    from PIL import Image, ImageChops, ImageDraw, ImageFilter
except ImportError as e:
    raise SystemExit("Pillow noetig: python -m pip install Pillow "
                     "(nur hier, nicht auf dem Server)") from e

ZIEL = os.path.join("assets", "azrael")
HOEHE = 360                 # Kantenlaenge der fertigen Frames
FPS = 10                    # Takt der Schleifen
RUHE_S = 3.0                # Laenge der Ruheschleife
SPRECH_S = 1.6              # Laenge der Sprechschleife

# --- am Original ausgemessen -------------------------------------------------
LIPPE = 495
MUND_X, MUND_B = 521, 104
AUGEN = ((455, 321), (612, 318))
ARM_DREHPUNKT = (800, 795)
ARM_BOX = (672, 118, 1030, 830)      # Klinge + Faust samt dunklem Rand
KIEFER_BOX = (432, 486, 608, 600)
ZUSCHNITT = (70, 0, 985, 940)        # Totraum weg, beide Pauldrons drin


def _ellipse(groesse, box, weich, wert=255):
    m = Image.new("L", groesse, 0)
    ImageDraw.Draw(m).ellipse(box, fill=wert)
    return m.filter(ImageFilter.GaussianBlur(weich)) if weich else m


def _masken(groesse):
    """Kiefer- und Armmaske. Der Kiefer wird oberhalb der Lippenlinie
    abgeschnitten — sonst wandert die Nase mit und das Gesicht verschmiert
    (genau daran ist der erste Entwurf gescheitert)."""
    kiefer = _ellipse(groesse, KIEFER_BOX, 7)
    deckel = Image.new("L", groesse, 0)
    ImageDraw.Draw(deckel).rectangle((0, 0, groesse[0], LIPPE - 3), fill=255)
    kiefer = ImageChops.subtract(kiefer, deckel.filter(ImageFilter.GaussianBlur(4)))
    return kiefer, _ellipse(groesse, ARM_BOX, 22)


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


def _alpha(bild):
    """Freistellen geht bei dieser Vorlage nicht: der Glow reicht bis an die
    Kante, und die Figur ist selbst fast schwarz — ein Luminanz-Key frisst
    Kapuze und Ruestung. Deshalb Superellipsen-Vignette, und erst ganz aussen
    nimmt eine sanfte Dunkel-Maske die schwarzen Ecken weg."""
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
    return maske.filter(ImageFilter.GaussianBlur(5))


def frame(basis, bloom, kiefer_maske, arm_maske, t, spricht):
    """Ein Einzelbild. t laeuft in Sekunden durch die jeweilige Schleife."""
    G = basis.size
    bild = basis.copy()

    # Schwertarm: dreht um den Unterarm. Beim Sprechen betont, sonst ein Wiegen.
    grad = (2.4 * math.sin(2 * math.pi * t / 1.15)) if spricht \
        else (0.8 * math.sin(2 * math.pi * t / RUHE_S))
    bild = Image.composite(
        basis.rotate(grad, resample=Image.BICUBIC, center=ARM_DREHPUNKT),
        bild, arm_maske)

    # Mund: Silbentakt. Kiefer faellt mit, und in die Hoehle kommt Glut —
    # ohne die liest ein blosses Absenken des Kinns als Rutsch, nicht als Mund.
    auf = 26 * (0.5 - 0.5 * math.cos(2 * math.pi * t / 0.40)) if spricht else 0.0
    if auf >= 1.0:
        versatz = int(round(auf * 0.55))
        if versatz:
            bild = Image.composite(ImageChops.offset(bild, 0, versatz), bild,
                                   ImageChops.offset(kiefer_maske, 0, versatz))
        hoehle = _ellipse(G, (MUND_X - MUND_B // 2, LIPPE - 3,
                              MUND_X + MUND_B // 2, LIPPE + auf), 3)
        bild = Image.composite(Image.new("RGB", G, (10, 2, 3)), bild, hoehle)
        glut = _ellipse(G, (MUND_X - MUND_B // 3, LIPPE + auf * 0.35,
                            MUND_X + MUND_B // 3, LIPPE + auf), 5,
                        int(150 * min(1, auf / 18)))
        bild = ImageChops.screen(bild, Image.merge(
            "RGB", (glut, glut.point(lambda v: v // 7), glut.point(lambda v: v // 6))))

    # Aura: Schleier dazuschalten, Staerke atmet.
    staerke = (0.30 + 0.22 * math.sin(2 * math.pi * t / 1.4)) if spricht \
        else (0.14 + 0.10 * math.sin(2 * math.pi * t / RUHE_S))
    bild = ImageChops.screen(bild, bloom.point(lambda v: int(v * staerke)))

    # Augen: glimmen mit, beim Sprechen heller.
    aug = Image.new("L", G, 0)
    d = ImageDraw.Draw(aug)
    hell = int((120 + 70 * math.sin(2 * math.pi * t / 1.4)) if spricht
               else (70 + 26 * math.sin(2 * math.pi * t / (RUHE_S / 1.5))))
    for cx, cy in AUGEN:
        d.ellipse((cx - 26, cy - 11, cx + 26, cy + 11), fill=hell)
    aug = aug.filter(ImageFilter.GaussianBlur(9))
    return ImageChops.screen(bild, Image.merge(
        "RGB", (aug, aug.point(lambda v: v // 5), aug.point(lambda v: v // 4))))


def main():
    quelle = sys.argv[1] if len(sys.argv) > 1 else "azrael_vorlage.png"
    if not os.path.isfile(quelle):
        raise SystemExit(f"Vorlage fehlt: {quelle}")
    basis = Image.open(quelle).convert("RGB")
    kiefer_maske, arm_maske = _masken(basis.size)
    bloom = _bloom(basis)

    zuschnitt = ZUSCHNITT
    breite = int(HOEHE * (zuschnitt[2] - zuschnitt[0]) / (zuschnitt[3] - zuschnitt[1]))
    alpha = _alpha(basis.crop(zuschnitt).resize((breite, HOEHE), Image.LANCZOS))

    if not shutil.which("ffmpeg"):
        raise SystemExit("ffmpeg noetig, um die Schleifen zu packen")

    os.makedirs(ZIEL, exist_ok=True)
    alpha.save(os.path.join(ZIEL, "alpha.png"), optimize=True)
    gesamt = os.path.getsize(os.path.join(ZIEL, "alpha.png"))

    for name, dauer, spricht in (("ruhe", RUHE_S, False), ("sprich", SPRECH_S, True)):
        anzahl = int(round(dauer * FPS))
        with tempfile.TemporaryDirectory() as tmp:
            for i in range(anzahl):
                f = frame(basis, bloom, kiefer_maske, arm_maske, i / FPS, spricht)
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
    print(f"gesamt {gesamt / 1024:.0f} KB in {ZIEL}/ (alpha.png + zwei Schleifen)")


if __name__ == "__main__":
    main()
