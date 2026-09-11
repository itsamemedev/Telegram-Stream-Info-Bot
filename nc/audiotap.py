"""nc.audiotap — warum der Audio-Tap der Live-Reaktion gestorben ist (v4.2-W46).

Befund vom 10.09.: im Log von 101 Minuten stehen 57 Starts des Audio-Taps und
57 Zeilen "Audio-Tap beendet -> Worker-Neustart", jede exakt eine Sekunde nach
ihrem Start. Warum, stand nirgends — der Prozess lief mit

    stderr=asyncio.subprocess.DEVNULL

Der Grund wurde also 57 Mal erzeugt und 57 Mal weggeworfen. In denselben 101
Minuten hat AZRAEL kein einziges Mal auf den gesendeten TikTok-Stream reagiert
("triggere AZRAEL-Reaktion": 0 Treffer). Der Recorder hat fuer genau diesen
Fall eine ganze Diagnosekette (nc.aufnahmekategorie, 403/Stall/Codec); der Tap
hatte nichts.

Dieses Modul rechnet, und zwar nur: keine Uhr, kein Prozess, keine Datei.
Es entscheidet zweierlei —

  1. In welche Kategorie faellt der Tod? Das rechnet NICHT dieses Modul
     selbst, sondern nc.aufnahmekategorie. Dieselbe Frage zweimal zu
     beantworten hiesse, zwei Wahrheiten zu haben, von denen eine veraltet.
     Hier steht nur die Abbildung der Tap-Groessen auf deren Parameter und
     die Abhilfe im Klartext.

  2. Soll dieser Tod ausfuehrlich gemeldet werden? Der Tap stirbt im
     Acht-Sekunden-Takt; 225 gleichlautende Warnungen sind ihr eigenes
     Rauschen und erziehen dazu, die Meldung zu ueberlesen. Die Regel ist
     dieselbe wie bei _loop_fehler in bot.py (CLAUDE.md): der erste Fall
     sofort, danach hoechstens alle 15 Minuten — mit der Zahl der
     unterdrueckten Faelle. Eine NEUE Kategorie meldet immer sofort: dass
     sich das Fehlerbild geaendert hat, ist die eigentliche Nachricht.
"""
from __future__ import annotations

from nc.aufnahmekategorie import kategorisiere

# Abstand zwischen zwei ausfuehrlichen Meldungen derselben Kategorie.
MELDE_ABSTAND_S = 900

# Was der Betreiber TUN kann — je Kategorie ein Satz, kein Lehrbuch.
# Bewusst hier und nicht in nc.aufnahmekategorie: dort geht es um die
# Aufnahme, und dieselbe Kategorie heisst beim Tap etwas anderes. Ein 403
# beim Recorder kostet eine Aufnahme, beim Tap kostet er AZRAELs Gehoer.
ABHILFE = {
    "forbidden_403":
        "TikTok blockt die Datacenter-IP. RECORD_PROXY (Residential/Mobile) "
        "setzen oder den Proxy-Pool fuellen lassen — derselbe Riegel wie bei "
        "der Aufnahme.",
    "stream_dead":
        "Die signierte Quell-URL ist abgelaufen (sie haelt rund 30 Minuten). "
        "Der Worker holt sie beim Neustart neu; passiert das im Minutentakt, "
        "war sie schon beim Aufloesen alt.",
    "offline_or_protected":
        "Der Stream ist beendet oder nicht oeffentlich. Kein Fehler des Bots "
        "— der Worker sollte dann aber gar nicht erst starten.",
    "timeout":
        "Die Quelle antwortet nicht rechtzeitig. Netz oder Proxy pruefen; "
        "haeufig derselbe Grund wie bei abbrechenden Aufnahmen.",
    "hevc_unsupported":
        "HEVC im FLV-Container — ffmpeg unter 7.x kann das nicht demuxen, "
        "auch wenn nur der Ton gebraucht wird. Neueres ffmpeg noetig.",
    "no_plugin":
        "ffmpeg kennt das Quellformat nicht. Aufloesung liefert vermutlich "
        "eine URL, die kein HLS/FLV ist.",
    "empty_output":
        "ffmpeg beendete sich ohne Fehler und ohne ein einziges Segment. "
        "Meist eine Quelle, die sofort EOF liefert.",
    "early_disconnect":
        "Die Quelle hat die Verbindung binnen Sekunden zugemacht. Typisch "
        "nach zu vielen Zugriffen von derselben IP.",
    "codec_header_fail":
        "ffmpeg konnte die Ausgabe nicht anlegen — Schreibrecht und Platz "
        "im Temp-Verzeichnis pruefen.",
    "stall_killed":
        "Der Tap lief, lieferte aber nichts mehr.",
    "fail":
        "Kein bekanntes Muster im stderr. Der Wortlaut unten ist alles, was "
        "ffmpeg gesagt hat.",
}


def diagnose(stderr_text, returncode, laufzeit_s, segmente) -> dict:
    """Warum ist der Tap gestorben, und was kann der Betreiber tun?

    `segmente` ist die Zahl der geschriebenen WAV-Dateien. Sie tritt an die
    Stelle von `file_exists` beim Recorder — und das ist kein Behelf: die
    Frage ist beide Male dieselbe, naemlich ob ueberhaupt etwas ankam.
    `stall_killed` ist beim Tap immer False; es gibt keinen Waechter, der ihn
    absichtlich abschiesst.
    """
    text = (stderr_text or "").strip() or "empty stderr"
    try:
        rc = int(returncode) if returncode is not None else 1
    except (TypeError, ValueError):
        rc = 1
    try:
        dauer = float(laufzeit_s or 0.0)
    except (TypeError, ValueError):
        dauer = 0.0
    kat = kategorisiere(text, False, rc, bool(segmente), dauer)
    return {
        "kategorie": kat,
        "abhilfe": ABHILFE.get(kat, ABHILFE["fail"]),
        "laufzeit_s": round(dauer, 1),
        "segmente": int(segmente or 0),
        "returncode": rc,
    }


def melden(zuletzt, jetzt, kategorie, letzte_kategorie,
           abstand_s=None) -> bool:
    """Ausfuehrlich melden — oder diesmal nur mitzaehlen?

    Sofort bei der ersten Meldung ueberhaupt und bei jedem WECHSEL der
    Kategorie. Sonst hoechstens alle MELDE_ABSTAND_S.

    Der Wechsel ist der wichtige Teil: laeuft ein 403-Sturm und wird daraus
    ein Codec-Fehler, dann ist das eine neue Lage und keine Wiederholung.
    Wer nur nach der Zeit drosselt, sieht den Wechsel erst eine Viertelstunde
    spaeter — und sucht bis dahin den falschen Fehler.
    """
    if zuletzt is None or letzte_kategorie != kategorie:
        return True
    grenze = MELDE_ABSTAND_S if abstand_s is None else abstand_s
    try:
        return (jetzt - zuletzt) >= float(grenze)
    except (TypeError, ValueError):
        # Im Zweifel melden: eine Meldung zu viel ist besser als der
        # Zustand von vor W46, in dem gar nichts zu sehen war.
        return True
