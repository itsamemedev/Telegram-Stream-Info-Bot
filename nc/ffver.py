"""nc.ffver — v4.0-W61: Parsen der ffmpeg-Versionszeile, aus bot.py gelöst.

Rein: die stdout von 'ffmpeg -version' rein, die Versionsnummer raus. Der
Subprozess-Aufruf und der Cache bleiben beim Aufrufer. 'ffmpeg version X …' → X;
sonst die erste Zeile (max. 40 Zeichen); nichts → ''. Bitgenau zum Monolithen.
"""

import re

_VER = re.compile(r"ffmpeg version (\S+)")


def parse_version(stdout):
    """Versionsnummer aus der ffmpeg -version-Ausgabe."""
    first = (stdout or "").splitlines()[0] if stdout else ""
    m = _VER.search(first)
    return m.group(1) if m else first[:40]
