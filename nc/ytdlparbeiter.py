"""nc.ytdlparbeiter — v5.2-W193: ein dauerhafter yt-dlp-Prozess (eigenes Programm).

Wird NICHT importiert, sondern von nc/ytdlpdienst.py als eigener Prozess
gestartet (`python -I nc/ytdlparbeiter.py`). Er laedt yt_dlp EINMAL und fuehrt
danach je Zeile auf stdin einen Aufruf aus — mit genau den Argumenten, die
sonst auf der Kommandozeile stuenden, und mit genau dem, was die
Kommandozeile geliefert haette: Rueckgabecode, stdout, stderr.

Warum ein eigener Prozess und nicht yt_dlp im Bot: ein yt-dlp, das haengt,
muss abschiessbar bleiben. Im Bot liefe es in einem Thread, und einen Thread
beendet man nicht. Hier beendet der Dienst den Prozess bei Zeitueberschreitung
genauso wie vorher den Einzelaufruf.

Protokoll (eine JSON-Zeile je Richtung):
    Start:    -> {"bereit": true, "version": "2026.10.26"}
    Anfrage:  <- {"argv": ["--no-warnings", ..., "https://..."]}
    Antwort:  -> {"rc": 0, "out": "...", "err": "..."}
Endet bei EOF auf stdin — stirbt der Bot, endet der Arbeiter mit ihm.
"""

import contextlib
import io
import json
import sys


def _fehler_melden(puffer, text):
    """Der Fehlerkanal dieses Programms ist die Antwort an den Bot (stderr im
    Protokoll) — dort landet er wie beim Einzelaufruf in err."""
    puffer.write(text)


def _antwort_melden(ausgabe, daten):
    """Eine Protokollzeile an den Bot — auch fuer jeden Fehler die Meldung."""
    ausgabe.write(json.dumps(daten) + "\n")
    ausgabe.flush()


def _ein_lauf(yt_dlp, argv):
    """Ein yt-dlp-Aufruf wie auf der Kommandozeile. -> (rc, out, err)"""
    aus, fehl = io.StringIO(), io.StringIO()
    rc = 0
    try:
        with contextlib.redirect_stdout(aus), contextlib.redirect_stderr(fehl):
            yt_dlp.main(list(argv))
    except SystemExit as e:
        # yt_dlp.main endet immer mit sys.exit — das ist der Rueckgabecode.
        code = e.code
        rc = code if isinstance(code, int) else (0 if code is None else 1)
    except BaseException as e:            # noqa: B036 — jeder Fehler ist eine Antwort
        rc = 1
        _fehler_melden(fehl, "ytdlparbeiter: %s: %s" % (type(e).__name__, e))
    return rc, aus.getvalue(), fehl.getvalue()


def main():
    ausgabe = sys.__stdout__
    try:
        import yt_dlp
    except ImportError as e:
        _antwort_melden(ausgabe, {"bereit": False, "grund": str(e)})
        return 3
    _antwort_melden(ausgabe, {"bereit": True, "version": yt_dlp.version.__version__})
    for zeile in sys.stdin:
        try:
            argv = json.loads(zeile)["argv"]
        except (ValueError, KeyError, TypeError) as e:
            _antwort_melden(ausgabe, {"rc": 2, "out": "",
                                      "err": "ytdlparbeiter: Anfrage unlesbar (%s)" % e})
            continue
        rc, out, err = _ein_lauf(yt_dlp, argv)
        _antwort_melden(ausgabe, {"rc": rc, "out": out, "err": err})
    return 0


if __name__ == "__main__":
    sys.exit(main())
