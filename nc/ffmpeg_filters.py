"""nc.ffmpeg_filters — v4.0-W27: reine Overlay-Filtergraph-Bauer (aus bot_v37).

Die zwei Overlay-Ketten des Restreams als reine String-Bauer herausgelöst — in
W22 scheiterte der naive Schnitt (verschachtelte defs), jetzt AST-exakt und
bitgenau geprüft. Keine Bot-Kopplung: alles, was vorher aus Modul-Globals kam
(Overlay-Dateipfade, Font, Canvas-Maße, FPS), wird hereingereicht.

* drawtext_chain(files, font)                         -> vf-Kette (Vollbild-Bänder)
* studio_chain(files, font, canvas_w, canvas_h, fps,  -> (filtergraph-Teile, vlabel)
                avatar_idx=None)
"""


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


def studio_chain(files, font, canvas_w, canvas_h, fps, avatar_idx=None):
    """F92: STUDIO-LAYOUT als filter_complex-Kette. Komponiert eine 16:9-Leinwand:
       Quell-Video links (aspect-fit, funktioniert für Hochkant-TikTok UND 16:9),
       rechts ein Info-Panel mit LIVE-CHAT (TikTok+Kick), Titel, Quelle, Ziel,
       Follower, AZRAEL-Reaktion; unten ein Branding-Footer. Alle Texte kommen aus
       reload-baren Dateien (expansion=none → kein %-Unfall durch Chat-Inhalte).
       Rückgabe: (liste von filtergraph-Teilen, finales Video-Label)."""
    f = files
    W, H = max(1280, canvas_w), max(720, canvas_h)
    W -= W % 2
    H -= H % 2
    fps = max(15, min(60, fps))
    VREG = int(W * 0.46)
    VREG -= VREG % 2            # Video-Region links (inkl. Rand)
    PX = VREG + 34                                     # Panel-Text linke Kante
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
        dt(f["chat"],    fontcolor="0xd9f6ea", fontsize=22, x=PX, y=172,
           line_spacing=11, borderw=0),
        dt(f["goal"],    fontcolor=AMB, fontsize=19, x=PX, y=H - 208),
        dt(f["follow"],  fontcolor=GRN, fontsize=19, x=PX, y=H - 174),
        # V37-OVFIX: react von der brand-Zeile nach OBEN ankern (y=H-th-58) statt
        # fix bei H-132. Bei 3 Zeilen wuchs der Block sonst nach unten in die
        # brand-Zeile (H-37). th ist die tatsaechliche Texthoehe → egal ob 1 oder
        # 3 Zeilen, der Block sitzt immer sauber ueber dem Marken-Schriftzug.
        dt(f["react"],   fontcolor="0xf2fffa", fontsize=22, x=PX, y=f"{H}-th-58"),
        dt(f["brand"],   fontcolor=GRN, fontsize=17, x="(w-tw)/2", y=H - 37, borderw=0),
        # Alert pulsiert ÜBER dem Video (Kontur statt Box — kein Leer-Blob, s. B73)
        dt(f["alert"],   fontcolor=MAG, fontsize=28, x=f"({VREG}-tw)/2", y=f"{H}*0.30",
           borderw=4, bordercolor=f"{INK}@0.9", alpha="0.55+0.45*sin(2*PI*t*1.6)"),
    ]
    parts.append("[sb]" + ",".join(deco + texts) + "[vdeco]")
    vlabel = "vdeco"
    if avatar_idx is not None:
        # Avatar oben rechts INS PANEL — nach der Deko, sonst übermalt drawbox ihn
        parts.append(f"[{avatar_idx}:v]scale=-1:92[sav]")
        parts.append("[vdeco][sav]overlay=x=W-w-26:y=22[vstudio]")
        vlabel = "vstudio"
    return parts, vlabel
