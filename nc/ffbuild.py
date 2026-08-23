"""nc.ffbuild — v4.0-W44: der ffmpeg-Kommandobauer, aus bot.py herausgelöst.

Ein kleiner, aber überall genutzter Baustein (Restream, Recording, Clips): setzt
den Thread-Deckel und die optionale nice-Stufe. Verbatim übernommen — Verhalten
bitgenau identisch zum Monolithen, inklusive der Assertion, die einen falsch
positionierten -threads-Einschub früh auffliegen lässt. Einzige Aussenwirkung ist
shutil.which("nice") (wie im Original); ansonsten reine Listen-Logik.
"""

import shutil


def ff_cmd(cmd, threads=None, nice=None):
    """Baut einen ffmpeg-Befehl mit Thread-Deckel und optionaler nice-Stufe.

    -threads steht direkt hinter "ffmpeg" (globale Codec-Option; gilt fuer De-
    UND Encoder). Nachgemessen: "-threads 2" ergibt 4 OS-Threads (2 Encode +
    Main + Filter) statt ~1.5x Kerne.

    nice wird als Prefix gesetzt statt per preexec_fn — das funktioniert auch
    ueber asyncio.create_subprocess_exec und ist im ps sichtbar.
    """
    out = list(cmd)
    if threads and threads > 0 and "-threads" not in out:
        assert out and out[0] == "ffmpeg", "_ff_cmd erwartet ffmpeg an Position 0"
        out[1:1] = ["-threads", str(int(threads))]
    if nice and nice > 0 and shutil.which("nice"):
        out[0:0] = ["nice", "-n", str(int(nice))]
    return out
