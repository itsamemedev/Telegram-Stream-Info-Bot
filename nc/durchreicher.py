"""nc.durchreicher — der Restream-Weg, wenn TikTok keine ziehbare Adresse herausgibt.

v4.2-W148. Der Betreiber am 05.11.: „Für die restreams werden angeblich keine
links gepullt die Gültigkeit haben … dann sollte vllt auf andere Formate
geprüft werden." Die Kette fragt seit W141 FLV, HLS, CMAF/DASH und
yt-dlp-Formate ab — und scheitert trotzdem, wenn TikTok der Server-IP zwar
„live" sagt, aber keine Adresse herausgibt, die ein fremdes ffmpeg ziehen
darf (signiert, sofort abgelaufen oder 403 für die IP). Gemessen hat das die
Quellprobe: in diesem Fall reicht `yt-dlp -o -` den Stream oft trotzdem
durch, weil yt-dlp die Signatur selbst bildet und die Segmente selbst holt.

Genau dieser Weg wird hier zum Restream-Zubringer. Die Sendebrücke (W130)
startet je Quelle EINEN Prozess, der MPEG-TS auf stdout schreibt. Dieser
Prozess ist hier ein kleines Programm, das zwei verkettet:

    yt-dlp -o - https://www.tiktok.com/@nutzer/live   (ersatzweise streamlink --stdout)
        └── stdout ──▶ ffmpeg -i pipe:0 … -f mpegts pipe:1   (der übliche Zubringer)

und beim Beenden BEIDE beendet. Für die Brücke bleibt es ein Prozess:
Stopp, Neustart und Umschalten funktionieren unverändert.

Nur Standardbibliothek und ohne Import aus nc/: das Modul läuft auch als
eigenes Programm (`python3 nc/durchreicher.py …`), ohne den Bot zu laden.

Zugangsdaten des Proxys stehen NIE in einer Befehlszeile (sie wären in der
Prozessliste lesbar): RECORD_PROXY geht als HTTPS_PROXY/HTTP_PROXY in die
Umgebung des Ziehers; yt-dlp und streamlink lesen sie dort.
"""

import os
import re
import shutil
import signal
import subprocess
import sys

SCHEMA = "durchreich://tiktok/"
_NUTZER = re.compile(r"^[A-Za-z0-9._]{1,64}$")
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36")


def adresse(nutzer: str) -> str:
    """Die Pseudo-Adresse, die der Restream statt einer URL weiterreicht."""
    if not _NUTZER.match(nutzer or ""):
        raise ValueError("kein gültiger TikTok-Name: %r" % nutzer)
    return SCHEMA + nutzer


def ist(url) -> bool:
    return isinstance(url, str) and url.startswith(SCHEMA)


def nutzer_aus(url: str) -> str:
    n = url[len(SCHEMA):] if ist(url) else ""
    if not _NUTZER.match(n):
        raise ValueError("keine Durchreicher-Adresse: %r" % url)
    return n


def werkzeug(which=shutil.which):
    """(name, pfad) des Ziehers — yt-dlp bevorzugt, dann streamlink — oder None."""
    for name in ("yt-dlp", "yt_dlp", "streamlink"):
        p = which(name)
        if p:
            return ("streamlink" if name == "streamlink" else "yt-dlp"), p
    return None


def zieher_cmd(name: str, exe: str, nutzer: str, cookies=None) -> list:
    """Der Befehl, der den Stream nach stdout zieht. Ohne Proxy-Angabe — die
    steht in der Umgebung (siehe Modul-Docstring)."""
    seite = "https://www.tiktok.com/@%s/live" % nutzer
    if name == "streamlink":
        return [exe, "--stdout", "--loglevel", "error", "--http-header",
                "User-Agent=" + UA, seite, "best"]
    cmd = [exe, "-q", "--no-warnings", "--no-part", "--hls-use-mpegts",
           "-o", "-", "--user-agent", UA, "--referer", "https://www.tiktok.com/"]
    if cookies and os.path.isfile(cookies):
        cmd += ["--cookies", cookies]
    return cmd + [seite]


def zieher_umgebung(env=None) -> dict:
    """Die Umgebung des Ziehers: RECORD_PROXY als HTTPS_PROXY/HTTP_PROXY."""
    env = dict(os.environ if env is None else env)
    proxy = (env.get("RECORD_PROXY") or "").strip()
    if proxy:
        if "://" not in proxy:
            proxy = "http://" + proxy
        env["HTTPS_PROXY"] = env["HTTP_PROXY"] = env["https_proxy"] = env["http_proxy"] = proxy
    return env


def zubringer_cmd(nutzer: str, ffmpeg_cmd: list, cookies=None, python=None) -> list:
    """Der Befehl fuer die Sendebruecke: dieses Programm, das Zieher und
    ffmpeg verkettet. `ffmpeg_cmd` liest von pipe:0."""
    return [python or sys.executable, os.path.abspath(__file__), nutzer,
            cookies or "-", "--"] + list(ffmpeg_cmd)


# ── Das Programm selbst ─────────────────────────────────────────────────────

def _beende(p):
    if p is not None and p.poll() is None:
        try:
            p.terminate()
            p.wait(timeout=3)
        except subprocess.TimeoutExpired:
            p.kill()
        except OSError:
            pass      # schon weg — das war das Ziel


def main(argv=None, popen=subprocess.Popen, which=shutil.which) -> int:
    """durchreicher.py NUTZER COOKIES|- -- FFMPEG …  -> Exitcode des ffmpeg.

    Exitcodes: 2 Aufruf, 3 kein Zieher installiert, sonst der des ffmpeg."""
    argv = sys.argv[1:] if argv is None else argv
    if "--" not in argv or argv.index("--") != 2:
        sys.stderr.write("Aufruf: durchreicher.py NUTZER COOKIES|- -- FFMPEG …\n")
        return 2
    nutzer, cookies, ff = argv[0], argv[1], argv[3:]
    if not _NUTZER.match(nutzer) or not ff:
        sys.stderr.write("Durchreicher: ungültiger Aufruf (%r)\n" % nutzer)
        return 2
    wz = werkzeug(which)
    if not wz:
        sys.stderr.write("Durchreicher: weder yt-dlp noch streamlink installiert — "
                         "sudo bash tools/update.sh\n")
        return 3
    zieher = popen(zieher_cmd(wz[0], wz[1], nutzer, None if cookies == "-" else cookies),
                   stdout=subprocess.PIPE, stderr=sys.stderr, stdin=subprocess.DEVNULL,
                   env=zieher_umgebung())
    try:
        wandler = popen(ff, stdin=zieher.stdout, stdout=sys.stdout, stderr=sys.stderr)
    except OSError as e:
        # stderr ist hier der Kanal: die Bruecke liest ihn ins Bot-Log.
        print("Durchreicher: ffmpeg startet nicht (%s)" % e, file=sys.stderr)
        _beende(zieher)
        return 2
    # Unser Ende der Leitung schliessen: endet ffmpeg, bekommt der Zieher
    # SIGPIPE und haelt nicht ewig einen toten Stream offen.
    if zieher.stdout is not None:
        zieher.stdout.close()

    def _halt(_sig, _frame):
        _beende(wandler)
        _beende(zieher)
        sys.exit(0)

    signal.signal(signal.SIGTERM, _halt)
    signal.signal(signal.SIGINT, _halt)
    rc = wandler.wait()
    _beende(zieher)
    return rc


if __name__ == "__main__":
    sys.exit(main())
