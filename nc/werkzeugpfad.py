"""nc.werkzeugpfad — v5.4-W195: welches yt-dlp/streamlink der Bot benutzt, und wie alt (bot-frei).

DER BEFUND (Betreiber, 12.11.)
  Der Dienst lief mit `/usr/bin/yt-dlp` aus dem apt-Paket, Fassung 2026.03.17
  — acht Monate alt. TikTok aendert seine Seiten in Wochen; jedes Live hiess
  „The channel is not currently live". Dabei hatten Installer und update.sh
  geschrieben: „Ein yt-dlp im venv zaehlt: der Bot ruft sie von dort, weil
  .venv/bin im PATH des Dienstes vorn steht." Die Unit setzt keinen PATH, und
  bot.py hat ihn nie angefasst — ein Kommentar ueber die Umgebung, von niemandem
  nachgesehen (dieselbe Klasse wie `concat_cmd`, CLAUDE.md W44).

  Dazu: die venv hiess beim Betreiber `venv/`, nicht `.venv/`. Ein fester Name
  waere also auch dann falsch gewesen, wenn ihn jemand gesetzt haette.

DIE REGEL
  * Der Bot stellt das Verzeichnis SEINES Interpreters (sys.executable) vor den
    PATH — das ist die venv, wie immer sie heisst. Nur wenn dort yt-dlp oder
    streamlink liegt; sonst aendert sich nichts.
  * Er sagt, welches yt-dlp er benutzt, wie alt es ist und ob es einen Browser
    nachahmen kann (curl_cffi). Ohne das liefert TikTok die Sperrseite.
"""

import calendar
import datetime
import os
import re
import shutil
import subprocess
import sys

WERKZEUGE = ("yt-dlp", "streamlink")
_DATUM = re.compile(r"^(\d{4})\.(\d{1,2})\.(\d{1,2})")
ALT_TAGE = 45          # ab hier ist ein yt-dlp fuer TikTok zu alt
_LAGE = {"pfad": "", "fassung": "", "alter_tage": None, "nachahmen": None,
         "vorangestellt": "", "grund": "noch nicht geprueft"}


def voranstellen(env=None, exe=None) -> str:
    """Das bin-Verzeichnis des laufenden Interpreters vor PATH setzen.

    -> das vorangestellte Verzeichnis, oder '' wenn nichts zu tun war
    (keines der Werkzeuge liegt dort, oder es steht schon vorn)."""
    env = os.environ if env is None else env
    ordner = os.path.dirname(os.path.abspath(exe or sys.executable))
    if not any(os.access(os.path.join(ordner, w), os.X_OK) for w in WERKZEUGE):
        return ""
    teile = [t for t in env.get("PATH", "").split(os.pathsep) if t]
    if teile and os.path.abspath(teile[0]) == ordner:
        return ""
    env["PATH"] = os.pathsep.join([ordner] + [t for t in teile
                                              if os.path.abspath(t) != ordner])
    _LAGE["vorangestellt"] = ordner
    return ordner


def alter_tage(fassung, heute=None):
    """yt-dlp-Fassungen sind Daten (JJJJ.MM.TT[.n]). -> Tage oder None."""
    m = _DATUM.match(str(fassung or ""))
    if not m:
        return None                   # keine Datumsfassung (Eigenbau, nightly-Hash)
    j, mo, t = (int(x) for x in m.groups())
    if not (1 <= mo <= 12 and 1 <= t <= calendar.monthrange(j, mo)[1]):
        return None
    return ((heute or datetime.date.today()) - datetime.date(j, mo, t)).days


def nachahmen_aus(ausgabe):
    """Ausgabe von `yt-dlp --list-impersonate-targets` -> bool oder None.

    Die Tabelle steht unter einer Zeile aus Bindestrichen; jede Zeile darunter,
    die NICHT „(unavailable)" traegt, ist ein nutzbares Ziel."""
    zeilen = (ausgabe or "").splitlines()
    for i, z in enumerate(zeilen):
        if z.strip() and set(z.strip()) == {"-"}:
            ziele = [r for r in zeilen[i + 1:] if r.strip()]
            return any("unavailable" not in r for r in ziele) if ziele else False
    return None


def pruefen(lauf=None, heute=None) -> dict:
    """Fassung, Alter und Nachahm-Faehigkeit des yt-dlp im PATH. Blockiert
    (zwei kurze Kindprozesse) — aus dem Event-Loop nur per to_thread."""
    lauf = lauf or _lauf
    pfad = shutil.which("yt-dlp") or ""
    _LAGE.update(pfad=pfad, fassung="", alter_tage=None, nachahmen=None)
    if not pfad:
        _LAGE["grund"] = "kein yt-dlp im PATH"
        return dict(_LAGE)
    rc, out = lauf([pfad, "--version"])
    _LAGE["fassung"] = out.strip().splitlines()[0] if rc == 0 and out.strip() else ""
    _LAGE["alter_tage"] = alter_tage(_LAGE["fassung"], heute)
    rc, out = lauf([pfad, "--list-impersonate-targets"])
    _LAGE["nachahmen"] = nachahmen_aus(out) if rc == 0 else None
    _LAGE["grund"] = befund(_LAGE)
    return dict(_LAGE)


def _lauf(cmd):
    """Ein Timeout oder ein verschwundenes Programm geht DURCH — die Schleife
    meldet es mit _loop_fehler auf error. Als rc=1 verpackt stand davon im
    Befund nur noch „nennt keine Fassung", und der eigentliche Grund war weg."""
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
    return r.returncode, (r.stdout or "") + (r.stderr or "")


def befund(lage) -> str:
    """'' wenn alles passt, sonst der Satz MIT Abhilfe."""
    teile = []
    if not lage.get("fassung"):
        teile.append("yt-dlp unter %s nennt keine Fassung" % (lage.get("pfad") or "?"))
    elif lage.get("alter_tage") is not None and lage["alter_tage"] > ALT_TAGE:
        teile.append("yt-dlp %s (%s) ist %d Tage alt — TikTok aendert sich schneller"
                     % (lage["fassung"], lage.get("pfad"), lage["alter_tage"]))
    if lage.get("nachahmen") is False:
        teile.append("yt-dlp kann keinen Browser nachahmen (curl_cffi fehlt) — TikTok "
                     "antwortet dann mit der Sperrseite")
    if not teile:
        return ""
    return ("; ".join(teile) + ". Abhilfe: bash tools/update.sh --python-deps "
            "(bringt yt-dlp mit curl_cffi und streamlink in die venv des Bots).")


def lage() -> dict:
    """Fuer /healthz — misst nicht (die Messung macht die Schleife)."""
    return dict(_LAGE)
