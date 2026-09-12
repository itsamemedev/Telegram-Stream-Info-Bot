"""nc.ffmpeg_filters — v4.0-W27: reine Overlay-Filtergraph-Bauer (aus bot.py).

Die zwei Overlay-Ketten des Restreams als reine String-Bauer herausgelöst — in
W22 scheiterte der naive Schnitt (verschachtelte defs), jetzt AST-exakt und
bitgenau geprüft. Keine Bot-Kopplung: alles, was vorher aus Modul-Globals kam
(Overlay-Dateipfade, Font, Canvas-Maße, FPS), wird hereingereicht.

* drawtext_chain(files, font)                         -> vf-Kette (Vollbild-Bänder)
* studio_chain(files, font, canvas_w, canvas_h, fps,  -> (filtergraph-Teile, vlabel)
                avatar_idx=None)
"""


def avatar_kette(avatar_idx, alpha_idx, hoehe, label):
    """v4.2-W32: der Avatar als Filter-Teilkette. -> (teile, label)

    Zwei Faelle, EINE Stelle: das alte Standbild ist ein Input und wird nur
    skaliert; die Animation sind ZWEI Inputs, weil VP9 keine Transparenz
    tragen kann (ffmpegs libvpx-vp9 verwirft den Alphakanal wortlos). Die
    Bewegung steckt also im WebM, die Deckung in einem einzelnen Graustufen-
    bild — alphamerge fuegt beides pro Frame wieder zusammen. Ohne diesen
    Schritt liegt ein undurchsichtiger Kasten im Sendebild.
    """
    if alpha_idx is None:
        return [f"[{avatar_idx}:v]scale=-1:{hoehe}[{label}]"], label
    return ([f"[{avatar_idx}:v]scale=-1:{hoehe}[{label}f]",
             f"[{alpha_idx}:v]scale=-1:{hoehe}[{label}d]",
             f"[{label}f][{label}d]alphamerge[{label}]"], label)


def drawtext_chain(files, font):
    """Alle Overlays als drawtext-Kette (auf [0:v]). Cyberpunk/Terminal-Look, MOBILE-
       tauglich: zwei VOLLBREITE Hintergrund-Bänder (oben/unten) — die bleiben sichtbar,
       auch wenn der Handy-Player die Seiten wegschneidet — plus Text mit Sicherheitsrand
       vom Bildrand + kleinerer Schrift. textfile+reload=1, leere Datei = nichts gezeichnet."""
    f = files
    INK = "0x05090f"                    # fast-schwarzes Band (Terminal-Optik)
    CY = "0x00e5ff"

    def esc(p):                         # ':' und '\' im Pfad fürs Filtergraph entschärfen
        return p.replace("\\", "\\\\").replace(":", "\\:")

    def dt(path, **kw):
        kw.setdefault("borderw", 2)
        kw.setdefault("bordercolor", "black@0.85")
        opts = ":".join(f"{k}={v}" for k, v in kw.items())
        return (f"drawtext=fontfile='{esc(font)}':textfile='{esc(path)}':"
                f"reload=1:{opts}")
    M = "(w*0.08)"                       # linker Sicherheitsrand (~8 % vom Bildrand weg)
    # Hintergrund-Bänder: full-width → Kanten-Crop auf Mobile schadet nicht.
    bands = [
        f"drawbox=x=0:y=0:w=iw:h=120:color={INK}@0.62:t=fill",            # Top-Band
        f"drawbox=x=0:y=118:w=iw:h=3:color={CY}@0.55:t=fill",             # Neon-Linie unter Top
        f"drawbox=x=0:y=ih-156:w=iw:h=156:color={INK}@0.62:t=fill",       # Bottom-Band
        f"drawbox=x=0:y=ih-156:w=iw:h=3:color={CY}@0.45:t=fill",          # Neon-Linie über Bottom
    ]
    texts = [
        dt(f["title"],  fontcolor=CY,         fontsize=21, x=M, y=12),                 # Titel — cyan
        dt(f["source"], fontcolor="0x00ff9c", fontsize=15, x=M, y=44),                 # Quelle — grün
        dt(f["goal"],   fontcolor="0xffb000", fontsize=16, x=M, y=72),                 # Spendenziel — amber
        dt(f["follow"], fontcolor="0x00ff9c", fontsize=17, x=M, y="h-th-98"),          # Follower — grün
        dt(f["react"],  fontcolor="0xe7fff4", fontsize=21, x=M, y="h-th-30"),          # Reaktion — weiß
        # B73-Fix: box=1 zeichnete auch bei LEERER Textdatei einen Blob
        # (boxborderw-großes Quadrat) mitten ins Bild — "grafischer Abfall".
        # Kräftige Kontur statt Box: unsichtbar sobald die Datei leer ist.
        dt(f["alert"],  fontcolor="0xff2e88", fontsize=27, x="(w-tw)/2", y="h*0.34",
           borderw=4, bordercolor="0x05090f@0.9",
           alpha="0.55+0.45*sin(2*PI*t*1.6)"),                                         # Alert — pulsiert
    ]
    return ",".join(bands + texts)


# v4.2-W54 — die Masse des Studio-Panels an EINER Stelle.
#
# Vorher rechnete studio_chain sie sich selbst aus, und der Chat-Umbruch stand
# als feste Zeichenzahl in bot.py (RESTREAM_CHAT_WIDTH=62, im Kommentar als
# "Mono" bezeichnet). Die Schrift ist aber PROPORTIONAL: 62 Zeichen DejaVu
# Bold sind bei Schriftgroesse 22 rund 780 px, das Panel hat 632. Jede
# zweite Chat-Zeile lief rechts aus dem Bild — auf dem Bildschirmfoto des
# Betreibers endet sie mitten im Wort.
#
# Beide Rechnungen lesen jetzt aus derselben Quelle, damit sie nicht wieder
# auseinanderlaufen koennen.

# Mittlere Zeichenbreite als Vielfaches der Schriftgroesse. Gemessen an
# DejaVuSans-Bold: deutscher Chat-Text liegt bei 0.56, gemischt mit
# Grossbuchstaben und Ziffern bei 0.69. 0.66 liegt bewusst am oberen Ende —
# eine etwas kuerzere Zeile ist harmlos, eine abgeschnittene nicht.
ZEICHENBREITE = 0.66

# Chat-Schrift im Panel. v4.2-W54: 22 -> 20. Bei 22 passten 47 Zeichen und
# elf Zeilen; bei 20 sind es 52 und zwoelf — auf einem Chat-Panel zaehlt
# Inhalt mehr als Schriftgroesse, und der Text traegt jetzt eine Kontur,
# die ihn auch klein noch lesbar haelt.
CHAT_FS = 20
CHAT_ABSTAND = 9


def studio_masse(canvas_w, canvas_h):
    """Alle Masse des Studio-Layouts. -> dict

    v4.2-W54. Der Chat behaelt seine volle Hoehe, AUCH wenn der Avatar
    darunter liegt: seit W54 wird er nach dem Avatar gezeichnet und steht
    damit vorn. Ihn wegen des Avatars zu kuerzen, waere die falsche
    Reihenfolge zweimal bezahlt — erst verdeckt, dann verkuerzt.
    """
    W = max(1280, canvas_w); W -= W % 2
    H = max(720, canvas_h);  H -= H % 2
    vreg = int(W * 0.46); vreg -= vreg % 2
    px = vreg + 34
    rand = 26
    ziel_y = H - 208
    chat_y = 172
    return {"W": W, "H": H, "vreg": vreg, "px": px, "rand": rand,
            "panel_b": W - px - rand,        # nutzbare Textbreite im Panel
            "chat_y": chat_y, "ziel_y": ziel_y,
            "chat_h": max(0, ziel_y - 12 - chat_y)}


def chat_umbruch_w(canvas_w, fontsize, panel_b=None):
    """Wieviele Zeichen passen in eine Panel-Zeile? -> int

    v4.2-W54. Ersetzt die feste 62 aus bot.py. Untergrenze 24: schmaler wird
    der Chat unlesbar, und ein absurd schmales Panel soll die Zeilen nicht auf
    ein Zeichen zusammenquetschen.
    """
    if panel_b is None:
        panel_b = studio_masse(canvas_w, 720)["panel_b"]
    return max(24, int(panel_b / (max(8, fontsize) * ZEICHENBREITE)))


def chat_zeilen(chat_h, fontsize, zeilenabstand):
    """Wieviele Chat-Zeilen passen ueber die Ziel-Leiste? -> int

    v4.2-W54. Eine Zeile Luft bleibt frei: drawtext misst die Zeilenhoehe
    etwas grosszuegiger als fontsize+line_spacing, und die Kontur (borderw=3)
    traegt unten noch drei Pixel auf. Ohne diese Reserve steht die letzte
    Chat-Zeile auf der Fortschrittsleiste.
    """
    schritt = max(1, fontsize + zeilenabstand)
    return max(3, int(chat_h / schritt) - 1)


def studio_chain(files, font, canvas_w, canvas_h, fps, avatar_idx=None,
                 avatar_alpha_idx=None, avatar_h=170):
    """F92: STUDIO-LAYOUT als filter_complex-Kette. Komponiert eine 16:9-Leinwand:
       Quell-Video links (aspect-fit, funktioniert für Hochkant-TikTok UND 16:9),
       rechts ein Info-Panel mit LIVE-CHAT (TikTok+Kick), Titel, Quelle, Ziel,
       Follower, AZRAEL-Reaktion; unten ein Branding-Footer. Alle Texte kommen aus
       reload-baren Dateien (expansion=none → kein %-Unfall durch Chat-Inhalte).
       Rückgabe: (liste von filtergraph-Teilen, finales Video-Label)."""
    f = files
    M = studio_masse(canvas_w, canvas_h)               # v4.2-W54: eine Quelle
    W, H, VREG, PX = M["W"], M["H"], M["vreg"], M["px"]
    fps = max(15, min(60, fps))
    INK, CY, GRN, AMB, MAG = "0x05070d", "0x00e5ff", "0x00ff9c", "0xffb000", "0xff2e88"

    def esc(p):
        return p.replace("\\", "\\\\").replace(":", "\\:")

    def dt(path, **kw):
        kw.setdefault("borderw", 2)
        kw.setdefault("bordercolor", "black@0.85")
        opts = ":".join(f"{k}={v}" for k, v in kw.items())
        return (f"drawtext=fontfile='{esc(font)}':textfile='{esc(path)}':"
                f"reload=1:expansion=none:{opts}")

    parts = [
        f"color=c={INK}:s={W}x{H}:r={fps}[cnv]",
        # Video aspect-fit in die linke Region — Hochkant bleibt Hochkant.
        (f"[0:v]scale={VREG - 56}:{H}:force_original_aspect_ratio=decrease:"
         f"force_divisible_by=2,setsar=1[vsrc]"),
        # shortest=1: Leinwand ist endlos — Ausgabe endet mit dem Quell-Video.
        f"[cnv][vsrc]overlay=x='({VREG}-w)/2':y='(H-h)/2':shortest=1[sb]",
    ]
    deco = [
        # Panel-Grund + Neon-Trennlinie + Header-Linie + Footer-Band
        f"drawbox=x={VREG}:y=0:w={W - VREG}:h={H}:color=0x070b12@0.94:t=fill",
        f"drawbox=x={VREG}:y=0:w=3:h={H}:color={CY}@0.55:t=fill",
        f"drawbox=x={PX - 14}:y=118:w={W - PX - 26}:h=2:color={CY}@0.35:t=fill",
        f"drawbox=x=0:y={H - 52}:w={W}:h=52:color=0x04060a@0.88:t=fill",
        f"drawbox=x=0:y={H - 52}:w={W}:h=2:color={GRN}@0.4:t=fill",
    ]
    texts = [
        dt(f["title"],   fontcolor=CY,  fontsize=30, x=PX, y=34),  # Panel-Breite: W-PX-40 px
        dt(f["source"],  fontcolor=GRN, fontsize=19, x=PX, y=82),
        dt(f["caption"], fontcolor="0x5d8a78", fontsize=15, x=PX, y=136, borderw=0),
        # v4.2-W54: borderw=0 war hier der eigentliche Grund, warum der Chat
        # unter dem Avatar verschwand. Er liegt jetzt VORN (siehe unten), und
        # eine Kontur traegt ihn ueber jede Textur — ohne sie waere heller
        # Text auf dem roten Gesicht nicht zu lesen, Reihenfolge hin oder her.
        dt(f["chat"],    fontcolor="0xd9f6ea", fontsize=CHAT_FS, x=PX,
           y=M["chat_y"], line_spacing=CHAT_ABSTAND,
           borderw=3, bordercolor="0x03060a@0.92"),
        dt(f["goal"],    fontcolor=AMB, fontsize=19, x=PX, y=H - 208),
        dt(f["follow"],  fontcolor=GRN, fontsize=19, x=PX, y=H - 174),
        # V37-OVFIX: react von der brand-Zeile nach OBEN ankern (y=H-th-58) statt
        # fix bei H-132. Bei 3 Zeilen wuchs der Block sonst nach unten in die
        # brand-Zeile (H-37). th ist die tatsaechliche Texthoehe → egal ob 1 oder
        # 3 Zeilen, der Block sitzt immer sauber ueber dem Marken-Schriftzug.
        dt(f["react"],   fontcolor="0xf2fffa", fontsize=22, x=PX, y=f"{H}-th-58",
           borderw=3, bordercolor="0x03060a@0.92"),
        dt(f["brand"],   fontcolor=GRN, fontsize=17, x="(w-tw)/2", y=H - 37, borderw=0),
        # Alert pulsiert ÜBER dem Video (Kontur statt Box — kein Leer-Blob, s. B73)
        dt(f["alert"],   fontcolor=MAG, fontsize=28, x=f"({VREG}-tw)/2", y=f"{H}*0.30",
           borderw=4, bordercolor=f"{INK}@0.9", alpha="0.55+0.45*sin(2*PI*t*1.6)"),
    ]
    # v4.2-W54 — DIE REIHENFOLGE IST DER GANZE PUNKT DIESER WELLE.
    #
    # Vorher stand hier deco UND Texte in EINER Kette, und der Avatar kam
    # danach. Er lag damit ueber allem, auch ueber dem Chat: auf dem
    # Bildschirmfoto des Betreibers verdeckt er die halbe rechte Spalte, und
    # von "S E L I N A  schrecklich, ..." ist nur der Anfang zu lesen.
    #
    # Er MUSS nach der Deko kommen (die drawboxen sind fast deckend und
    # wuerden ihn sonst uebermalen) und VOR den Texten. Also drei Ketten
    # statt einer.
    parts.append("[sb]" + ",".join(deco) + "[vdeco]")
    vlabel = "vdeco"
    if avatar_idx is not None:
        # v4.2-W30: unten rechts im Panel statt oben — nach der Deko, sonst
        # übermalt drawbox ihn. y=H-148 sitzt sicher ÜBER dem Footer-Band
        # (H-52) und rechts NEBEN goal/follow/react (die bei PX links im
        # Panel stehen, react bei AZRAEL_OVERLAY_WRAP_W=38 Zeichen bleibt
        # deutlich schmaler als die Panel-Breite). +6*sin(...) = sanftes
        # Schweben, dieselbe Bewegung wie beim HTML-Avatar (azFloat) und der
        # Nicht-Studio-Kette oben in restreamcmd.py, nur kleinere Amplitude
        # (Panel ist enger als das freie Sendebild).
        # v4.2-W31: 92 -> 170 px. Bei 92 war vom Gesicht nichts mehr zu
        # erkennen (8 % Bildhoehe, im Sendebild ein roter Fleck). Seit W32
        # kommt die Hoehe von aussen (RESTREAM_AVATAR_H) — der Avatar ist der
        # optische Moderator, wie gross er sein soll ist Geschmack und gehoert
        # nicht in den Quelltext. y rechnet MIT h statt gegen eine feste
        # Pixelzahl, sonst rutscht er bei jeder Groessenaenderung aus dem
        # Panel. 72 = 52 px Footer-Band + 20 px Luft darueber.
        teile, lab = avatar_kette(avatar_idx, avatar_alpha_idx, avatar_h, "sav")
        parts.extend(teile)
        # eof_action=repeat + shortest=0: die Schleife ist endlich, das
        # Sendebild nicht. Ohne beides endet der Stream mit dem Avatar.
        parts.append(f"[vdeco][{lab}]overlay=x=W-w-{M['rand']}:"
                     f"y=H-72-h+6*sin(2*PI*t/6):"
                     f"eof_action=repeat:shortest=0[vav]")
        vlabel = "vav"
    # ... und JETZT die Texte, ueber den Avatar.
    parts.append(f"[{vlabel}]" + ",".join(texts) + "[vstudio]")
    return parts, "vstudio"
