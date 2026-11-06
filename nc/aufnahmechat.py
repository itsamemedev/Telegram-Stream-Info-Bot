"""nc.aufnahmechat — der TikTok-Chat gehoert auch in die Aufnahme (rein, bot-frei).

v4.2-W158. Gemeldet am 06.11.: „In den Aufnahmen fehlt der Chat. In den
Restreams ist alles korrekt. Nur in den Aufnahmen hast du das nie
beruecksichtigt."

Der Befund hatte zwei Haelften:

* Die Aufnahme ist eine Kopie des TikTok-Stroms (`-c copy` bzw. yt-dlp) — der
  Chat ist dort gar nicht enthalten. Im Restream steht er nur, weil der Sender
  ihn per drawtext ins Bild brennt. Fuer die Aufnahme gab es keinen Weg dorthin:
  `on_comment` schrieb in einen Puffer im Speicher, ohne Zeitstempel und ohne
  Bezug zu einer Datei.
* Ein Chat-Listener lief ueberhaupt nur fuer Nutzer mit Live-React-Worker (bis
  LIVE_REACT_MAX_USERS) oder mit Restream. Im Log vom 06.11. wurden @tbwpueppi
  und @tatjana335 aufgenommen, ohne dass ihr Chat je empfangen wurde.

Hier steht die reine Logik: der Mitschnitt je laufender Aufnahme (im Speicher,
nie auf der Platte im Event-Loop — CLAUDE.md, W97), die Untertitel im
ASS-Format und die beiden ffmpeg-Befehle. Wann was laeuft, entscheidet bot.py.

Zwei Arten, den Chat in die Datei zu bringen (AUFNAHME_CHAT):
  einbrennen   ins Bild, wie im Restream — sichtbar in jedem Player, auch in
               Telegram. Kostet einen Durchlauf mit libx264. Vorgabe.
  untertitel   als abschaltbare Untertitelspur — ohne Neukodieren, aber
               Telegram zeigt eingebettete Untertitel nicht an.
  aus          wie bisher.
"""

import collections
import time

from nc.ffbuild import ff_cmd

MODI = ("einbrennen", "untertitel", "aus")
VORGABE = "einbrennen"
ANZEIGE_S = 8.0           # so lange steht eine Nachricht im Bild
ZEILEN = 6                # so viele Nachrichten gleichzeitig, die neueste unten
MAX_EINTRAEGE = 50000     # je Aufnahme — ein Deckel gegen Speicherwachstum
MAX_SITZUNGEN = 64
DOPPELT_S = 3.0           # zwei Listener auf demselben Chat: gleiche Zeile entfaellt
MAX_TEXT = 140

# video_pfad -> {"user", "t0", "eintraege": [(t_rel, wer, text)], "proc"}
SITZUNGEN = collections.OrderedDict()
_ZULETZT = {}             # user -> deque[(wer, text, t)] fuer die Doppel-Erkennung


def modus(wert) -> str:
    w = (wert or "").strip().lower()
    return w if w in MODI else VORGABE


def _schluessel(user):
    return (user or "").lstrip("@").lower()


def beginnen(user, video_pfad, t0, proc=None) -> None:
    """Eine Aufnahme hat begonnen. `t0` ist die Wanduhr beim Start des
    Aufnahmeprozesses — die Nullzeit der Datei."""
    SITZUNGEN[video_pfad] = {"user": _schluessel(user), "t0": float(t0),
                             "eintraege": [], "proc": proc}
    while len(SITZUNGEN) > MAX_SITZUNGEN:
        SITZUNGEN.popitem(last=False)


def _lebt(s) -> bool:
    p = s.get("proc")
    return p is None or getattr(p, "returncode", None) is None


def laeuft(user) -> bool:
    """Laeuft fuer diesen Nutzer gerade eine Aufnahme mit Chat-Mitschnitt?"""
    k = _schluessel(user)
    return any(s["user"] == k and _lebt(s) for s in SITZUNGEN.values())


def notieren(user, wer, text, jetzt=None) -> int:
    """Eine Chatnachricht. -> Zahl der Aufnahmen, in die sie ging."""
    jetzt = time.time() if jetzt is None else float(jetzt)
    k = _schluessel(user)
    text = " ".join(str(text or "").split())[:MAX_TEXT]
    wer = " ".join(str(wer or "?").split())[:40]
    letzte = _ZULETZT.setdefault(k, collections.deque(maxlen=50))
    # Leer oder Doppel (zwei Listener auf demselben Chat): nichts zu notieren.
    neu = bool(text) and not any(w == wer and t == text and jetzt - z < DOPPELT_S
                                 for w, t, z in letzte)
    n = 0
    if neu:
        letzte.append((wer, text, jetzt))
        for s in SITZUNGEN.values():
            if s["user"] == k and _lebt(s) and jetzt >= s["t0"] \
                    and len(s["eintraege"]) < MAX_EINTRAEGE:
                s["eintraege"].append((jetzt - s["t0"], wer, text))
                n += 1
    return n


def beenden(video_pfad) -> list:
    """Die Aufnahme ist fertig. -> [(t_rel, wer, text)], die Sitzung ist weg."""
    s = SITZUNGEN.pop(video_pfad, None)
    return list(s["eintraege"]) if s else []


# ── Untertitel ─────────────────────────────────────────────────────────────

def _ass_text(s):
    # Steuerzeichen von ASS entschaerfen: {…} waere ein Override-Block,
    # ein Backslash eine Steuersequenz. Nutzertext darf nie Formatierung sein.
    return (s.replace("\\", "⧵").replace("{", "(").replace("}", ")"))


def _zeit(t):
    t = max(0.0, t)
    h = int(t // 3600)
    m = int(t % 3600 // 60)
    s = t % 60
    return "%d:%02d:%05.2f" % (h, m, s)


def ass(eintraege, breite=720, hoehe=1280, anzeige_s=ANZEIGE_S, zeilen=ZEILEN) -> str:
    """Die Chat-Untertitel als ASS-Datei (Text).

    Jede Nachricht startet ein Ereignis, das die letzten `zeilen` noch
    sichtbaren Nachrichten zeigt — die neueste unten, wie im Chat. Ein
    Ereignis endet mit der naechsten Nachricht oder nach `anzeige_s`.
    Das Panel sitzt unten links auf einem halbdurchsichtigen Kasten, wie
    das Chat-Panel im Restream."""
    b, h = max(160, int(breite)), max(160, int(hoehe))
    groesse = max(12, round(min(b, h) * 0.034))
    rand = max(8, round(b * 0.03))
    kopf = ("[Script Info]\nScriptType: v4.00+\nPlayResX: %d\nPlayResY: %d\n"
            "WrapStyle: 0\nScaledBorderAndShadow: yes\n\n"
            "[V4+ Styles]\nFormat: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, "
            "OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, "
            "Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, "
            "MarginV, Encoding\n"
            "Style: Chat,DejaVu Sans,%d,&H00F0F6EA,&H00FFFFFF,&H90000000,&H90000000,"
            "0,0,0,0,100,100,0,0,3,%d,0,1,%d,%d,%d,1\n\n"
            "[Events]\nFormat: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, "
            "Effect, Text\n") % (b, h, groesse, max(2, groesse // 4), rand,
                                 round(b * 0.25), round(h * 0.12))
    zeilen_out = []
    e = sorted(eintraege, key=lambda x: x[0])
    for i, (t, _w, _x) in enumerate(e):
        ende = t + anzeige_s
        if i + 1 < len(e):
            ende = min(ende, e[i + 1][0])
        if ende <= t:
            continue
        sicht = [x for x in e[max(0, i - zeilen + 1):i + 1] if t - x[0] < anzeige_s]
        text = "\\N".join("{\\c&H9CFF00&}%s{\\c&HEAF6F0&}: %s" % (_ass_text(w), _ass_text(x))
                          for _t, w, x in sicht)
        zeilen_out.append("Dialogue: 0,%s,%s,Chat,,0,0,0,,%s" % (_zeit(t), _zeit(ende), text))
    return kopf + "\n".join(zeilen_out) + ("\n" if zeilen_out else "")


# ── ffmpeg ─────────────────────────────────────────────────────────────────

def _filterpfad(p):
    # Im Filtergraph sind ':' und '\'' Trenner bzw. Quotes; Windows-Pfade
    # bringen Backslashes mit. Der Pfad stammt vom Bot, nicht vom Nutzer.
    return p.replace("\\", "/").replace(":", "\\:").replace("'", "\\'")


# Nachbearbeitung laeuft mit der niedrigsten Prioritaet: Aufnahmen und
# Restreams gehen vor, und die Box war am 06.11. ohnehin am CPU-Limit.
NICE = 19


def einbrennen_cmd(video, ass_pfad, ziel, preset="veryfast", crf=23, threads=2) -> list:
    """Chat ins Bild brennen. Ton bleibt eine Kopie, das Bild wird neu kodiert."""
    return ff_cmd(["ffmpeg", "-hide_banner", "-loglevel", "error", "-nostats", "-y",
                   "-i", video, "-map", "0:v:0", "-map", "0:a?",
                   "-vf", "subtitles='%s'" % _filterpfad(ass_pfad),
                   "-c:v", "libx264", "-preset", preset, "-crf", str(int(crf)),
                   "-pix_fmt", "yuv420p",
                   "-c:a", "copy", "-movflags", "+faststart", ziel],
                  threads=max(1, int(threads)), nice=NICE)


def untertitel_cmd(video, ass_pfad, ziel) -> list:
    """Chat als Untertitelspur — ohne Neukodieren."""
    return ff_cmd(["ffmpeg", "-hide_banner", "-loglevel", "error", "-nostats", "-y",
                   "-i", video, "-i", ass_pfad, "-map", "0:v:0", "-map", "0:a?", "-map", "1:0",
                   "-c:v", "copy", "-c:a", "copy", "-c:s", "mov_text",
                   "-metadata:s:s:0", "language=deu", "-metadata:s:s:0", "title=Chat",
                   "-movflags", "+faststart", ziel], threads=1, nice=NICE)


# ══════════════════════════════════════════════════════════════════════════
# v4.2-W159: Chat im Clip, Clips einer Aufnahme, der Zusammenschnitt
# ══════════════════════════════════════════════════════════════════════════
#
# Gemeldet: „der Hype-Director schneidet gar keine Memes zusammen … die
# Dateien muss er vor dem Upload in Discord oder Telegram wieder
# zusammensetzen, dass er Video mit Chat uploaded." Einen Zusammenschnitt gab
# es im Code nicht, und die Clips trugen keinen Chat.

CLIPS = collections.OrderedDict()     # video_pfad -> [(clip_pfad, grund)]
MAX_CLIPS = 40


def ausschnitt(video_pfad, von, bis) -> list:
    """Der Chat der laufenden Aufnahme zwischen `von` und `bis` (Sekunden der
    Datei), auf den Clip verschoben: t=0 ist der Clipanfang."""
    s = SITZUNGEN.get(video_pfad) or {"eintraege": ()}    # keine Sitzung: kein Chat
    return [(t - von, w, x) for t, w, x in s["eintraege"] if von <= t <= bis]


def clip_merken(video_pfad, clip_pfad, grund="") -> None:
    liste = CLIPS.setdefault(video_pfad, [])
    if len(liste) < MAX_CLIPS:
        liste.append((clip_pfad, grund or ""))
    while len(CLIPS) > MAX_SITZUNGEN:
        CLIPS.popitem(last=False)


def clips_nehmen(video_pfad) -> list:
    """Die Clips einer fertigen Aufnahme, in Entstehungsreihenfolge."""
    return list(CLIPS.pop(video_pfad, []))


def concat_liste(pfade) -> str:
    """Inhalt einer concat-Liste mit ABSOLUTEN Pfaden.

    Ein relativer Eintrag wird gegen das Verzeichnis der LISTE aufgeloest,
    nicht gegen das Arbeitsverzeichnis — genau daran ist das Zusammenfuegen
    der Sitzungen gescheitert („recordings/recordings/…", CLAUDE.md W44)."""
    import os
    return "".join("file '%s'\n" % os.path.abspath(p).replace("'", "'\\''") for p in pfade)


def zusammenschnitt_cmd(liste_pfad, ziel, neu=False, threads=1) -> list:
    """Clips hintereinander. Erst als Kopie — die Clips einer Aufnahme tragen
    dasselbe Format —, bei `neu` neu kodiert, falls die Kopie scheitert."""
    cmd = ["ffmpeg", "-hide_banner", "-loglevel", "error", "-nostats", "-y",
           "-f", "concat", "-safe", "0", "-i", liste_pfad]
    if neu:
        cmd += ["-c:v", "libx264", "-preset", "veryfast", "-crf", "23",
                "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "160k"]
    else:
        cmd += ["-c", "copy"]
    cmd += ["-movflags", "+faststart", ziel]
    return ff_cmd(cmd, threads=max(1, int(threads)), nice=NICE)
