"""nc.audio_cue — v4.0-W11: Signalton vor AZRAELs Stimme + Ducking im Restream-Mix.

Zwei Dinge, beide rein und testbar:

1. tone_pcm(): erzeugt einen SAUBEREN kurzen Ton als s16le-PCM (gleiches Format
   wie die TTS-Häppchen: 44100 Hz, stereo). Sinus mit weichen Ein-/Ausblenden —
   ohne Fades knackt es hörbar, weil die Welle hart bei ungleich null abbricht.

2. mix_chain(): baut die ffmpeg-Filterkette, die AZRAELs Stimme in den Stream
   mischt und dabei den ÜBRIGEN Ton absenkt (Ducking), solange AZRAEL redet.
   Umgesetzt mit sidechaincompress: die Stimme steuert als Sidechain die
   Absenkung des Quell-Tons. Die Stärke wird aus dem gewünschten Faktor
   berechnet (0.9 = 10 % leiser).
"""

import math
import struct

SR = 44100
CH = 2


def tone_pcm(freq=880.0, ms=120, volume=0.25, fade_ms=15, sr=SR, ch=CH):
    """Sauberer Signalton als s16le-PCM-Bytes (interleaved, `ch` Kanäle).
       volume 0..1 relativ zur Vollaussteuerung; fade_ms blendet ein und aus,
       damit es an den Rändern nicht knackt."""
    n = max(1, int(sr * (max(1, int(ms)) / 1000.0)))
    fade = min(int(sr * (max(0, int(fade_ms)) / 1000.0)), n // 2)
    vol = max(0.0, min(1.0, float(volume)))
    out = bytearray()
    two_pi_f = 2.0 * math.pi * float(freq)
    for i in range(n):
        env = 1.0
        if fade:
            if i < fade:
                env = i / fade
            elif i >= n - fade:
                env = (n - 1 - i) / fade
        s = math.sin(two_pi_f * (i / sr)) * vol * env
        v = int(max(-1.0, min(1.0, s)) * 32767)
        out += struct.pack("<h", v) * ch
    return bytes(out)


def silence_pcm(ms=60, sr=SR, ch=CH):
    """Kurze Pause zwischen Ton und Stimme (PCM-Stille)."""
    return bytes(int(sr * (max(0, int(ms)) / 1000.0)) * ch * 2)


def cue_pcm(freq=880.0, ms=120, volume=0.25, fade_ms=15, gap_ms=60, sr=SR, ch=CH):
    """Kompletter Vorspann: Ton + kurze Pause — direkt vor die Stimme zu setzen."""
    return tone_pcm(freq, ms, volume, fade_ms, sr, ch) + silence_pcm(gap_ms, sr, ch)


def duck_ratio(factor, over_db=16.6):
    """sidechaincompress-ratio fuer eine gewuenschte Absenkung.
       factor 0.9 = auf 90 % (also 10 % leiser). Rueckgabe 1.0 = keine Absenkung.
       `over_db` = wie weit die Stimme ueber der Schwelle liegt; 16.6 ist an
       einer ffmpeg-Messung kalibriert (0.9 ergibt damit ~10 % Absenkung)."""
    try:
        f = float(factor)
    except (TypeError, ValueError):
        return 1.0
    if f >= 1.0 or f <= 0.0:
        return 1.0
    reduction_db = -20.0 * math.log10(f)          # 0.9 -> ~0.92 dB
    frac = min(0.95, reduction_db / float(over_db))
    return round(min(20.0, max(1.0, 1.0 / (1.0 - frac))), 3)


def mix_chain(tts_idx, gain="1.8", duck_factor=1.0, src="0:a", out="a"):
    """Filterglieder (Liste) fuer den Stimm-Mix. Ohne Ducking exakt die bisherige
       Kette (Quell-Ton voll via normalize=0, Stimme angehoben, alimiter gegen
       Clipping). Mit Ducking wird der Quell-Ton waehrend der Stimme abgesenkt."""
    r = duck_ratio(duck_factor)
    if r <= 1.0:
        return [f"[{tts_idx}:a]volume={gain}[vtts]",
                f"[{src}][vtts]amix=inputs=2:duration=first:dropout_transition=0:"
                f"normalize=0,alimiter=limit=0.97[{out}]"]
    return [f"[{tts_idx}:a]volume={gain},asplit=2[vtts][vsc]",
            f"[{src}][vsc]sidechaincompress=threshold=0.03:ratio={r}:"
            f"attack=20:release=350:detection=rms[vduck]",
            f"[vduck][vtts]amix=inputs=2:duration=first:dropout_transition=0:"
            f"normalize=0,alimiter=limit=0.97[{out}]"]
