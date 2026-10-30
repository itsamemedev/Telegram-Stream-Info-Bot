"""nc.sendebruecke — v4.2-W130: die Verbindung zur Plattform überlebt den Quellwechsel.

════════════════════════════════════════════════════════════════════════
DER BEFUND
════════════════════════════════════════════════════════════════════════
Bis hierher war ein Restream EIN ffmpeg: TikTok rein, Kick/Twitch/YouTube
raus. Damit hing die Sendeverbindung an der Quelle. Jede Störung der Quelle
beendete den Prozess, und mit ihm die RTMP-Verbindung:

* TikToks signierte Pull-Adressen laufen rund alle sechs Minuten ab
  (`_looks_like_source_expired`, B138). Der Manager holte dann sofort eine
  frische Adresse — aber in einem NEUEN Prozess, also mit neuer Verbindung.
* Ein CDN-Hänger hielt die Ausgabe bis `-rw_timeout` (30 s) an, der
  Stillstands-Wächter griff nach 75 s. So lange bekam die Plattform nichts.
* Jeder Neustart lief durch Auflösung, Preflight, YouTube-Key-Abfrage (bis
  10 s) und Overlay-Start, bevor wieder ein Bild ankam.

Für die Plattform ist eine geschlossene Verbindung ein beendeter Stream. Die
Zuschauer sehen den Lade-Kreisel, die Player müssen neu laden, und je nach
Plattform beginnt eine neue Sendung. Gemessen mit echtem ffmpeg gegen einen
lokalen RTMP-Empfänger: zwei Quell-Abschnitte im heutigen Aufbau ergeben zwei
Verbindungen — der Empfänger endet mit dem ersten.

════════════════════════════════════════════════════════════════════════
DER AUFBAU
════════════════════════════════════════════════════════════════════════
Ab hier sind es zwei Rollen:

    Zubringer (TikTok → MPEG-TS)  ─┐
                                   ├─ Weiche ─→ Sender (TS → Plattformen)
    Füller    (Pausenbild → TS)   ─┘

Der SENDER hält die Verbindung und lebt so lange wie der Restream. Die
ZUBRINGER kommen und gehen: läuft die Adresse ab oder hängt das CDN, schaltet
die Weiche nach `luecke_s` Sekunden auf den Füller und holt im Hintergrund
eine frische Adresse. Die Plattform bekommt in der Zeit ein Pausenbild mit
Stille, aber keinen Abbruch.

Die WEICHE ist der Teil, der das erst möglich macht. Zwei Zubringer haben
voneinander unabhängige Zeitstempel; ohne Eingriff springt der Strom beim
Wechsel rückwärts. Gemessen (ffmpeg 6.1, drei Abschnitte 6+4+6 s):

    ohne Umschreiben     26,0 s Ausgabe für 16 s Inhalt — der Sender
                         „korrigiert" den Sprung und schiebt 10 s Leerlauf ein
    mit Umschreiben      16,8 s — der Strom folgt der Uhr

`TsUmschreiber` setzt PTS, DTS und PCR jedes Abschnitts so, dass er an die
Wanduhr anschliesst und nie rückwärts läuft, und nummeriert die
Continuity-Counter durch. Umgeschaltet wird nur an einem Video-Keyframe
(random_access_indicator), sonst zeigt der Sender bis zum nächsten Keyframe
Pixelsalat (W108: der lässt sich nicht wegfiltern, nur vermeiden).

Bewusst NICHT hier: ffmpeg-Kommandos (nc/restreamcmd.py) und das Auflösen der
Quelle (Bot, über `quelle`). Dieses Modul kennt nur Bytes, Prozesse und die
Uhr — und ist damit ohne Netz und ohne Bot prüfbar.
"""

import logging
import os
import subprocess
import threading
import time

from nc import tonspur as _tonspur

log = logging.getLogger("nc.sendebruecke")

TS = 188
_SYNC = 0x47
_UMLAUF = 1 << 33                 # PTS/DTS/PCR-Basis sind 33 Bit breit, Takt 90 kHz
_TAKT = 90000

# Elementarstrom-Typen aus der PMT (ISO/IEC 13818-1, Tabelle 2-34).
H264 = 0x1B
HEVC = 0x24
AAC_ADTS = 0x0F

# Strom-IDs ohne optionalen PES-Kopf — dort steht kein Zeitstempel.
_OHNE_KOPF = {0xBC, 0xBE, 0xBF, 0xF0, 0xF1, 0xFF, 0xF2, 0xF8}

# Ein Bild bei 30 fps in 90-kHz-Ticks. Abstand, um den ein neuer Abschnitt
# mindestens hinter dem letzten liegt, damit der Sender nie zwei Bilder mit
# demselben Zeitstempel bekommt.
_BILD = 3000


# ══════════════════════════════════════════════════════════════════════════
# Zeitstempel im Paket
# ══════════════════════════════════════════════════════════════════════════

def _ts_lesen(b, i):
    """33-Bit-PTS/DTS aus den fünf Bytes ab i (mit Markerbits)."""
    return (((b[i] >> 1) & 0x07) << 30 | b[i + 1] << 22
            | ((b[i + 2] >> 1) & 0x7F) << 15 | b[i + 3] << 7 | (b[i + 4] >> 1))


def _ts_schreiben(b, i, wert):
    # Das obere Halbbyte (0010/0011/0001) sagt, ob PTS oder DTS — es bleibt.
    b[i] = (b[i] & 0xF0) | (((wert >> 30) & 0x07) << 1) | 1
    b[i + 1] = (wert >> 22) & 0xFF
    b[i + 2] = (((wert >> 15) & 0x7F) << 1) | 1
    b[i + 3] = (wert >> 7) & 0xFF
    b[i + 4] = ((wert & 0x7F) << 1) | 1


def _pcr_lesen(b, i):
    return b[i] << 25 | b[i + 1] << 17 | b[i + 2] << 9 | b[i + 3] << 1 | (b[i + 4] >> 7)


def _pcr_schreiben(b, i, basis):
    # Erweiterung (27-MHz-Rest) und die sechs reservierten Bits bleiben.
    b[i] = (basis >> 25) & 0xFF
    b[i + 1] = (basis >> 17) & 0xFF
    b[i + 2] = (basis >> 9) & 0xFF
    b[i + 3] = (basis >> 1) & 0xFF
    b[i + 4] = ((basis & 1) << 7) | (b[i + 4] & 0x7F)


def pid(p):
    return ((p[1] & 0x1F) << 8) | p[2]


def _af_laenge(p):
    """Länge des Anpassungsfelds inkl. Längenbyte, 0 ohne Feld."""
    return (p[4] + 1) if (p[3] & 0x20) else 0


def ist_keyframe(p):
    """random_access_indicator gesetzt — ffmpegs TS-Muxer setzt ihn auf
    jedem Keyframe, und zwar JEDES Stroms: auch auf Tonpaketen, die alle
    Keyframes sind. Die Weiche fragt deshalb zusaetzlich nach der Bild-PID
    (`video_pid`). Gemessen: ohne die Frage schaltete sie an einem Tonpaket
    um, der Sender bekam das Bild ab mitten im GOP und meldete „QP out of
    range / decode_slice_header error" bis zum naechsten Keyframe."""
    return bool((p[3] & 0x20) and p[4] > 0 and (p[5] & 0x40))


def pes_zeit(p):
    """(pts, dts) eines Pakets mit PES-Anfang, sonst (None, None)."""
    if not (p[1] & 0x40) or not (p[3] & 0x10):
        return None, None
    o = 4 + _af_laenge(p)
    if o + 14 > TS or p[o:o + 3] != b"\x00\x00\x01" or p[o + 3] in _OHNE_KOPF:
        return None, None
    flags = p[o + 7] >> 6
    pts = _ts_lesen(p, o + 9) if flags & 2 else None
    dts = _ts_lesen(p, o + 14) if flags == 3 and o + 19 <= TS else None
    return pts, dts


class TsUmschreiber:
    """Macht aus Abschnitten verschiedener Zubringer EINEN fortlaufenden Strom.

    `abschnitt(wand)` beginnt einen neuen Abschnitt. Sein Versatz wird am
    ersten Zeitstempel festgelegt, den er bringt: der Abschnitt beginnt bei
    der Wanduhr `wand` (90 kHz seit Senderstart), aber nie vor dem letzten
    ausgegebenen Zeitstempel plus ein Bild. Der Versatz gilt für ALLE PIDs
    des Abschnitts — sonst liefen Bild und Ton auseinander.
    """

    def __init__(self):
        self.cc = {}
        self.je_pid = {}         # letzter ausgegebener Zeitstempel je PID
        self.verwerfen = set()   # PIDs, deren laufendes PES verworfen wird
        self.letzt = None        # höchster ausgegebener Zeitstempel (90 kHz)
        self.delta = None
        self._wand = 0

    def abschnitt(self, wand):
        self.delta = None
        self._wand = int(wand) % _UMLAUF

    def _versatz(self, ein):
        if self.delta is None:
            ziel = self._wand
            if self.letzt is not None and _vor(ziel, (self.letzt + _BILD) % _UMLAUF):
                ziel = (self.letzt + _BILD) % _UMLAUF
            self.delta = (ziel - ein) % _UMLAUF
        return (ein + self.delta) % _UMLAUF

    def _merke(self, wert):
        if self.letzt is None or _vor(self.letzt, wert):
            self.letzt = wert

    def paket(self, p):
        """Das umgeschriebene Paket — oder None, wenn es weg muss.

        Weg muss ein PES, das hinter den letzten seines Stroms zurückfiele.
        Gemessen, nicht vermutet: ein frischer Zubringer liefert seinen ersten
        Ton ein paar Millisekunden VOR dem Keyframe, an dem umgeschaltet wird
        (AAC-Vorlauf, -0,023 s). Durchgereicht meldete der AAC-Encoder des
        Senders „Queue input is backward in time", der FLV-Muxer bog die
        Zeitstempel zurecht, und die Plattform bekam an jeder Umschaltung
        hunderte Tonpakete in einer Sekunde (629 statt 43)."""
        b = bytearray(p)
        k = pid(b)
        # PES zuerst: ist der Versatz noch offen, soll ihn der Zeitstempel des
        # Keyframes festlegen, nicht die PCR davor (die liegt mit muxdelay 0
        # zwar fast gleich, aber eben nicht genau).
        pts, dts = pes_zeit(b)
        if pts is not None:
            o = 4 + _af_laenge(b) + 9
            neu = self._versatz(dts if dts is not None else pts)
            vorher = self.je_pid.get(k)
            if vorher is not None and not _vor(vorher, neu):
                self.verwerfen.add(k)
                return None
            self.verwerfen.discard(k)
            self.je_pid[k] = neu
            if dts is not None:
                neu_pts = (pts + self.delta) % _UMLAUF
                _ts_schreiben(b, o, neu_pts)
                _ts_schreiben(b, o + 5, neu)
                self._merke(neu_pts)
            else:
                _ts_schreiben(b, o, neu)
                self._merke(neu)
        elif k in self.verwerfen and (b[3] & 0x10):
            return None             # Fortsetzung eines verworfenen PES
        if (b[3] & 0x20) and b[4] >= 7 and (b[5] & 0x10):
            _pcr_schreiben(b, 6, self._versatz(_pcr_lesen(b, 6)))
        if b[3] & 0x10:
            # Continuity-Counter je PID durchzählen. Ein Sprung beim Wechsel
            # ist für den Demuxer ein Paketverlust und kostet ein Bild.
            n = (self.cc.get(k, -1) + 1) & 0x0F
            self.cc[k] = n
            b[3] = (b[3] & 0xF0) | n
        return bytes(b)


def _vor(a, b):
    """a liegt zeitlich vor b — mit Umlauf der 33 Bit."""
    return 0 < (b - a) % _UMLAUF < _UMLAUF // 2


# ══════════════════════════════════════════════════════════════════════════
# PAT/PMT: was bringt ein Zubringer mit?
# ══════════════════════════════════════════════════════════════════════════

def _abschnitt_daten(p):
    if not (p[1] & 0x40):
        return None
    o = 4 + _af_laenge(p)
    if o >= TS:
        return None
    o += 1 + p[o]                 # pointer_field
    return p[o:] if o < TS else None


def pat_pmt_pid(p):
    """PMT-PID aus einem PAT-Paket (erstes Programm), sonst None."""
    d = _abschnitt_daten(p)
    if not d or len(d) < 12 or d[0] != 0x00:
        return None
    laenge = ((d[1] & 0x0F) << 8) | d[2]
    i, ende = 8, min(3 + laenge - 4, len(d))
    while i + 4 <= ende:
        prog = (d[i] << 8) | d[i + 1]
        if prog != 0:
            return ((d[i + 2] & 0x1F) << 8) | d[i + 3]
        i += 4
    return None


def pmt_stroeme(p):
    """{pid: stream_type} aus einem PMT-Paket, sonst None."""
    d = _abschnitt_daten(p)
    if not d or len(d) < 12 or d[0] != 0x02:
        return None
    laenge = ((d[1] & 0x0F) << 8) | d[2]
    ende = min(3 + laenge - 4, len(d))
    i = 12 + (((d[10] & 0x0F) << 8) | d[11])
    out = {}
    while i + 5 <= ende:
        out[((d[i + 1] & 0x1F) << 8) | d[i + 2]] = d[i]
        i += 5 + (((d[i + 3] & 0x0F) << 8) | d[i + 4])
    return out


def video_pid(stroeme):
    """Die PID des Bildstroms (H.264 oder HEVC), sonst None."""
    for k, typ in sorted((stroeme or {}).items()):
        if typ in (H264, HEVC):
            return k
    return None


def pmt_urteil(stroeme):
    """Passt dieser Zubringer hinter den Sender?

    'ok'        H.264 und AAC — wie der Füller.
    'neukodieren'  das Bild ist kein H.264 (TikTok liefert teils HEVC). Der
                Sender hat seinen Decoder am ersten Strom eingerichtet; ein
                anderer Codec unter derselben PID wäre Datensalat.
    'tonlos'    kein Ton. Der Sender braucht Ton, sonst wartet sein Muxer auf
                Audio und die Ausgabe steht (W106, eine Schicht weiter).
    """
    typen = set((stroeme or {}).values())
    if H264 not in typen:
        return "neukodieren"
    if AAC_ADTS not in typen:
        return "tonlos"
    return "ok"


# ══════════════════════════════════════════════════════════════════════════
# Die Brücke
# ══════════════════════════════════════════════════════════════════════════

FUELLER = "fueller"
QUELLE = "quelle"


class Bruecke:
    """Hält den Sender gefüttert, egal was die Quelle tut.

    schreib_fd     Schreibende der Pipe, deren Leseende der Sender als stdin hat.
    fueller_cmd    ffmpeg-Kommando des Pausenbilds (läuft durchgehend).
    zubringer_cmd  f(url, tonlos, neukodieren) -> ffmpeg-Kommando.
    quelle         f() -> (url, fehler). fehler 'offline' heisst: nachweislich
                   nicht live; alles andere: unklar, später noch einmal.
    erste_url      die bereits aufgelöste Adresse des Starts.
    luecke_s       so lange darf die Quelle schweigen, bevor der Füller kommt.
    offline_s      so lange hält der Füller eine Quelle, die offline ist. Danach
                   endet die Brücke, der Sender bekommt EOF und endet mit 0 —
                   das ist für den Manager „Quelle beendet", und der Platz
                   wird frei. Ein Streamer, der nur kurz neu verbindet, kommt
                   damit ohne Abbruch zurück.
    redigieren     f(text) -> text: stderr der Zubringer kann Adressen tragen.
    """

    def __init__(self, schreib_fd, fueller_cmd, zubringer_cmd, quelle,
                 erste_url=None, luecke_s=3.0, offline_s=120.0, redigieren=None,
                 name="", uhr=time.monotonic, popen=subprocess.Popen,
                 neustart_min_s=1.0, neustart_max_s=30.0, unklar_s=600.0,
                 start_warten_s=20.0, anlauf_s=20.0):
        self._fd = schreib_fd
        self._fueller_cmd = fueller_cmd
        self._zubringer_cmd = zubringer_cmd
        self._quelle = quelle
        self._erste_url = erste_url
        self.luecke_s = float(luecke_s)
        self.offline_s = float(offline_s)
        self._redigieren = redigieren or (lambda s: s)
        self.name = name
        self._uhr = uhr
        self._popen = popen
        self._neustart_min = float(neustart_min_s)
        self._neustart_max = float(neustart_max_s)
        self.unklar_s = float(unklar_s)
        self.start_warten_s = float(start_warten_s)
        self.anlauf_s = float(anlauf_s)
        self._fueller_frei = False

        self._sperre = threading.Lock()
        self._startsperre = threading.Lock()
        self._halt = threading.Event()
        self._um = TsUmschreiber()
        self._t0 = uhr()
        self._quelle_zuletzt = self._t0   # zuletzt Quelle auf Sendung
        self.aktiv = FUELLER         # wer gerade durchkommt
        self._wunsch = FUELLER       # wohin beim nächsten Keyframe geschaltet wird
        self._zuletzt = {FUELLER: None, QUELLE: None}
        self._pmt_pid = {}
        self._urteil = {}
        self._vpid = {}
        self._zub = None             # laufender Zubringer-Prozess
        self._fue = None
        self._tonlos = False
        self._neukodieren = False
        self._url = erste_url
        self._ersetzt = False
        # Zustand der Wache — hier gesetzt, nicht erst in _wache, damit jeder
        # Schritt auch einzeln (im Vertrag) einen definierten Anfang hat.
        self._naechste = erste_url
        self._pause = self._neustart_min
        self._offline_seit = None
        self._gestartet = None
        self._threads = []
        self._stderr_leser = {}
        self.wechsel = 0
        self.fueller_s = 0.0
        self._fueller_seit = uhr()
        self.grund = "Start"
        self.ende = None             # gesetzt, wenn die Brücke aufgibt
        self.stderr = {FUELLER: [], QUELLE: []}

    # ---- Lage für Dashboard und Health ------------------------------------
    def lage(self):
        with self._sperre:
            f = self.fueller_s + ((self._uhr() - self._fueller_seit)
                                  if self.aktiv == FUELLER else 0.0)
            return {"aktiv": self.aktiv, "wechsel": self.wechsel,
                    "fueller_s": round(f, 1), "grund": self.grund,
                    "tonlos": self._tonlos, "neukodieren": self._neukodieren,
                    "ende": self.ende}

    # ---- Weiche -----------------------------------------------------------
    def _wand(self):
        return int((self._uhr() - self._t0) * _TAKT)

    def _umschalten(self, wer, grund):
        # unter self._sperre
        if wer == QUELLE:
            self._fueller_frei = True
        if self.aktiv == FUELLER and wer != FUELLER:
            self.fueller_s += self._uhr() - self._fueller_seit
        if wer == FUELLER:
            self._fueller_seit = self._uhr()
        self.aktiv = wer
        self.wechsel += 1
        self.grund = grund
        self._um.abschnitt(self._wand())
        log.info("Sendebrücke %s: %s (%s)", self.name,
                 "Pausenbild" if wer == FUELLER else "Quelle", grund)

    def daten(self, wer, paket) -> bool:
        """Ein TS-Paket von `wer`. Gibt zurück, ob es durchging."""
        with self._sperre:
            self._zuletzt[wer] = self._uhr()
            k = pid(paket)
            if k == 0:
                pp = pat_pmt_pid(paket)
                if pp is not None:
                    self._pmt_pid[wer] = pp
            elif k == self._pmt_pid.get(wer):
                st = pmt_stroeme(paket)
                if st is not None:
                    self._urteil[wer] = pmt_urteil(st)
                    self._vpid[wer] = video_pid(st)
            if wer == FUELLER and not self._fueller_frei:
                # Wer zuerst beim Sender ankommt, legt dessen Bildgroesse fest:
                # der Encoder ist danach eingerichtet, und ffmpeg skaliert alles
                # Spaetere still auf diese Groesse. Gemessen: kam das Pausenbild
                # zuerst, lief eine 1080x1920-Quelle die ganze Sitzung als
                # 720x1280 hinaus. Also bekommt die Quelle den Vortritt — das
                # Pausenbild erst, wenn sie einmal lief oder zu lange ausbleibt.
                # Verzerrt wird dabei nichts Sichtbares: das Pausenbild ist eine
                # einfarbige Flaeche.
                if self._uhr() - self._t0 < self.start_warten_s:
                    return False
                self._fueller_frei = True
            if wer != self.aktiv:
                # Umschalten nur an einem Keyframe dessen, der übernehmen soll,
                # und nur, wenn seine PMT gelesen und für passend befunden ist.
                if (wer == self._wunsch and self._urteil.get(wer) == "ok"
                        and k == self._vpid.get(wer) and ist_keyframe(paket)):
                    self._umschalten(wer, self._wunsch_grund)
                else:
                    return False
            if self._fd is None:
                return False
            if wer == QUELLE:
                self._quelle_zuletzt = self._zuletzt[wer]
            raus = self._um.paket(paket)
            if raus is None:
                return False
            # In der Sperre schreiben. Ausserhalb koennten zwei Leser um eine
            # Umschaltung herum ihre Pakete vertauschen — die Continuity-
            # Counter stimmten dann nicht mehr, und der Demuxer des Senders
            # verwirft ein Paket. Ein langsamer Sender blockiert so nur die
            # Zubringer, und die laufen mit -re ohnehin im Takt.
            try:
                os.write(self._fd, raus)
            except OSError as e:
                # Laut genug: das Ende des Senders meldet der Manager mit
                # seinem stderr. Hier nur der Zusammenhang, auf info.
                log.info("Sendebrücke %s: Sender nimmt nichts mehr an (%s)",
                         self.name, e)
                self._abbruch("Sender nimmt nichts mehr an (%s)" % e)
                return False
        return True

    def _wuensche(self, wer, grund):
        with self._sperre:
            self._wunsch = wer
            self._wunsch_grund = grund

    _wunsch_grund = "Start"

    # ---- Prozesse ---------------------------------------------------------
    def _lies(self, wer, proc):
        rest = b""
        lesen = getattr(proc.stdout, "read1", proc.stdout.read)
        try:
            while not self._halt.is_set():
                d = lesen(65536)
                if not d:
                    break
                d = rest + d
                # Am Sync-Byte ausrichten. ffmpeg schreibt ganze Pakete, die
                # Pipe zerteilt sie aber beliebig — ein Rest wird angesetzt.
                s = d.find(bytes([_SYNC]))
                if s > 0:
                    d = d[s:]
                n = len(d) // TS * TS
                rest = d[n:]
                for i in range(0, n, TS):
                    if d[i] == _SYNC:
                        self.daten(wer, d[i:i + TS])
        except (OSError, ValueError) as e:
            if not self._halt.is_set():
                log.warning("Sendebrücke %s: Lesen von %s abgebrochen: %s",
                            self.name, wer, e)

    def _stderr(self, wer, proc):
        senke = self.stderr[wer]
        try:
            for z in iter(proc.stderr.readline, b""):
                senke.append(self._redigieren(z.decode("utf-8", "ignore")).rstrip())
                del senke[:-20]
        except (OSError, ValueError) as e:
            # Normal endet die Schleife an b"" (EOF). Eine Ausnahme heisst,
            # die Pipe ist unter dem Leser weggebrochen — dann fehlen die
            # letzten Zeilen, nach denen _nach_ende urteilt.
            log.info("Sendebrücke %s: stderr von %s nicht zu Ende gelesen: %s",
                     self.name, wer, e)

    def _starte(self, wer, cmd, halt_pruefen=False):
        """halt_pruefen: Prüfen und Starten unter der Sperre, die auch stop()
        nimmt (die Startsperre, nicht die Datensperre). Review #169: stop() während einer laufenden Auflösung räumte
        auf, die Auflösung lieferte danach noch eine Adresse, und der so
        gestartete Zubringer blieb als Waise stehen. Unter der Sperre sieht
        entweder stop() den neuen Prozess, oder _starte sieht den Halt."""
        if halt_pruefen:
            with self._startsperre:
                if self._halt.is_set():
                    log.info("Sendebrücke %s: gestoppt, während die Quelle "
                             "aufgelöst wurde — kein Zubringer mehr.", self.name)
                    return None
                p = self._popen(cmd, stdin=subprocess.DEVNULL,
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                self._zub = p
        else:
            p = self._popen(cmd, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)
        for ziel in (self._lies, self._stderr):
            t = threading.Thread(target=ziel, args=(wer, p), daemon=True,
                                 name="bruecke-%s-%s" % (self.name, wer))
            t.start()
            self._threads.append(t)
        self._stderr_leser[id(p)] = t
        return p

    @staticmethod
    def _beende(p):
        if p is None or p.poll() is not None:
            return
        try:
            p.terminate()
            p.wait(timeout=3)
        except subprocess.TimeoutExpired:
            p.kill()
        except OSError:
            return     # schon weg — das war das Ziel

    def start(self):
        self._fue = self._starte(FUELLER, self._fueller_cmd)
        t = threading.Thread(target=self._wache, daemon=True,
                             name="bruecke-%s-wache" % self.name)
        t.start()
        self._threads.append(t)

    def stop(self):
        with self._startsperre:
            # Unter der Startsperre: ein _starte(halt_pruefen=True) laeuft
            # entweder davor (dann steht sein Prozess hier in _zub) oder danach
            # (dann sieht es den Halt). Bewusst NICHT self._sperre: die haelt
            # daten() waehrend os.write, und ein Sender, der nicht liest,
            # liesse stop() dann ewig warten.
            self._halt.set()
            zub = self._zub
        self._beende(zub)
        self._beende(self._fue)
        self._schliessen()

    def _schliessen(self):
        with self._sperre:
            fd, self._fd = self._fd, None
        if fd is not None:
            try:
                os.close(fd)
            except OSError:
                return     # schon zu: der Sender hat seine Seite geschlossen

    def _abbruch(self, grund, laut=False):
        """laut=False: die Ursache meldet ein anderer — der Manager das Ende
        des Senders, die Offline-Lage ist Alltag. Zweimal dieselbe Störung
        im ERROR-Log ist eine zu viel. Gemeldet wird in jedem Fall, einmal.
        Gibt None zurück, damit _adresse mit `return self._abbruch(...)`
        enden kann."""
        if self.ende is None:
            self.ende = grund
            (log.error if laut else log.info)("Sendebrücke %s endet: %s",
                                              self.name, grund)
        self._halt.set()

    # ---- Wache: Zubringer starten, Lücken erkennen -------------------------
    def _wache(self):
        """Der Takt der Bruecke: Zubringer ueberwachen, ersetzen, starten.

        Drei Schritte mit eigenem Namen, weil jeder seine eigene Frage
        beantwortet: was lehrt das Ende eines Zubringers (_nach_ende), lebt
        der laufende noch wirklich (_pruefe_laufenden), und woher kommt die
        naechste Adresse (_adresse)."""
        while not self._halt.is_set():
            zub = self._zub
            if zub is not None and zub.poll() is not None:
                self._nach_ende(zub)
                self._halt.wait(self._pause)
                continue
            if zub is not None:
                if not self._pruefe_laufenden(zub):
                    self._halt.wait(0.25)
                continue
            url = self._adresse()
            if url is None:
                if self.ende is not None:
                    break
                continue
            self._gestartet = self._uhr()
            self._url = url
            del self.stderr[QUELLE][:]
            # Wunsch und Zeitmarke VOR dem Start: der Leser-Thread kann den
            # ersten Keyframe schon verarbeitet haben, bevor _starte
            # zurueckkehrt — danach gesetzt, verfiele er, und die Quelle
            # kaeme erst mit dem naechsten GOP (Vertrag W130 hat es gefangen).
            self._zuletzt[QUELLE] = None
            self._wuensche(QUELLE, "Zubringer gestartet")
            try:
                self._zub = self._starte(QUELLE, self._zubringer_cmd(
                    url, self._tonlos, self._neukodieren), halt_pruefen=True)
            except OSError as e:
                # Review #169: ein Popen-Fehler (Prozess-/fd-Grenze) beendete
                # bisher die Wache. Das Pausenbild lief weiter, der Sender sah
                # gesund aus, und nichts versuchte die Quelle je wieder. Jetzt
                # wie ein gescheiterter Lauf: laut, mit Pause, neuer Versuch;
                # die Grenze unklar_s beendet die Brücke, wenn es so bleibt.
                log.warning("Sendebrücke %s: Zubringer startet nicht (%s) — "
                            "neuer Versuch in %.0f s.", self.name, e, self._pause)
                self._halt.wait(self._pause)
                self._pause = min(self._neustart_max, self._pause * 2)
        self._schliessen()

    def _nach_ende(self, zub):
        """Ein Zubringer ist beendet. Setzt self._naechste und self._pause."""
        lief = self._uhr() - (self._gestartet or self._uhr())
        # Erst fertig lesen, dann urteilen: der Prozess kann beendet
        # sein, bevor sein letzter stderr-Satz hier angekommen ist.
        # Der Vertrag hat genau diesen Wettlauf gefangen — die
        # tonlose Quelle wurde dann als tote Edge behandelt.
        _t = self._stderr_leser.pop(id(zub), None)
        if _t is not None:
            _t.join(timeout=2.0)
        urteil = self._urteil.get(QUELLE)
        if urteil is None and _tonspur.ist_tonlos_fehler(
                "\n".join(self.stderr[QUELLE])):
            # Ohne Ton stirbt der Zubringer am -map, BEVOR er eine PMT
            # schreibt — die Weiche sieht dann nie „tonlos". Gemessen:
            # ohne diese Zeile drehte eine tonlose Quelle endlos
            # Neustarts, und das Pausenbild blieb stehen.
            urteil = "tonlos"
        ersetzt, self._ersetzt = self._ersetzt, False
        self._zub = None
        self._fallback("Zubringer beendet (rc=%s)" % zub.returncode)
        with self._sperre:
            self._urteil.pop(QUELLE, None)
            self._pmt_pid.pop(QUELLE, None)
            self._vpid.pop(QUELLE, None)
        if urteil == "neukodieren" and not self._neukodieren:
            self._neukodieren = True
            log.warning("Sendebrücke %s: Quelle ist kein H.264 — "
                        "Zubringer kodiert ab jetzt neu.", self.name)
            self._naechste, self._pause = self._url, self._neustart_min
        elif urteil == "tonlos" and not self._tonlos:
            self._tonlos = True
            log.warning("Sendebrücke %s: Quelle ohne Ton — Zubringer "
                        "legt ab jetzt Stille an.", self.name)
            self._naechste, self._pause = self._url, self._neustart_min
        elif ersetzt and self._zuletzt.get(QUELLE) is not None:
            # Ein Hänger, nachdem die Quelle geliefert hatte: dieselbe
            # Adresse ist sehr wahrscheinlich noch gültig, und eine
            # Auflösung je Hänger fordert TikToks 429 heraus. Hat sie
            # nie geliefert (Anlaufzeit verstrichen), taugt die
            # Adresse nichts — dann der Zweig unten.
            self._naechste, self._pause = self._url, self._neustart_min
        else:
            # Kurze Läufe in Folge: eine tote Edge, kein Ablauf. Dann
            # nicht im Sekundentakt nachlegen.
            self._pause = (self._neustart_min if lief > 60
                           else min(self._neustart_max, self._pause * 2))
            self._naechste = None

    def _pruefe_laufenden(self, zub) -> bool:
        """False: alles in Ordnung, weiter warten. True: er wurde beendet."""
        urteil = self._urteil.get(QUELLE)
        if (urteil == "neukodieren" and not self._neukodieren) or (
                urteil == "tonlos" and not self._tonlos):
            # Unpassend: beenden, _nach_ende stellt um.
            self._beende(zub)
            return True
        jetzt = self._uhr()
        zl = self._zuletzt.get(QUELLE)
        # Vor dem ersten Byte gilt die Anlaufzeit, nicht die Luecke:
        # ffmpeg probt die Quelle (-analyzeduration bis 10 s), und
        # ein Zubringer, der nach luecke_s abgeschossen wird, kaeme
        # bei einer zaehen HLS-Quelle nie ueber das Proben hinaus.
        grenze = self.luecke_s if zl is not None else self.anlauf_s
        seit = zl or self._gestartet or jetzt
        if jetzt - seit <= grenze:
            return False
        # Schweigt sie, kommt der Füller — und der Zubringer wird
        # ERSETZT, nicht abgewartet. Gemessen: ein Zubringer, der
        # nach einem Hänger weiterliest, holt mit -re die
        # verpasste Zeit im Schwall nach, und der Strom läuft
        # danach um die Länge des Hängers vor der Uhr (26,1 s
        # Wanduhr, 30,5 s Ausgabe). Ein frischer Zubringer setzt
        # an der Live-Kante an.
        if self.aktiv == QUELLE:
            self._fallback("Quelle schweigt seit %.0f s" % (jetzt - seit))
        self._ersetzt = True
        self._beende(zub)
        return True

    def _adresse(self):
        """Die Adresse fuer den naechsten Zubringer, oder None (dann ist
        gewartet worden, oder die Bruecke hat aufgegeben: self.ende)."""
        if self._naechste is not None:
            url, self._naechste = self._naechste, None
            return url
        jetzt = self._uhr()
        try:
            url, fehler = self._quelle()
        except Exception as e:     # Auflösung selbst gestorben
            log.warning("Sendebrücke %s: Auflösung der Quelle ist abgestürzt "
                        "(%s: %s).", self.name, type(e).__name__, e)
            url, fehler = None, "%s: %s" % (type(e).__name__, e)
        if url:
            self._offline_seit = None
            # Eine NEUE Adresse kann ein anderer Strom sein: der Streamer
            # hat neu gestartet, TikTok liefert eine andere Stufe. Die
            # Erfahrungen der alten Adresse gelten dafuer nicht — sonst
            # bliebe eine Sitzung nach einem einzigen tonlosen Anlauf fuer
            # immer stumm, auch wenn die Quelle laengst wieder Ton hat.
            self._tonlos = self._neukodieren = False
            return url
        ohne = jetzt - self._quelle_zuletzt
        if fehler != "offline" and ohne >= self.unklar_s:
            # Ohne Grenze stuende das Pausenbild ewig, waehrend
            # TikTok uns blockt — fuer den Zuschauer dasselbe wie
            # ein toter Stream, nur ohne dass jemand es erfaehrt.
            return self._abbruch("seit %.0f s keine abspielbare Quelle "
                                 "(zuletzt: %s)" % (ohne, fehler), laut=True)
        if fehler == "offline":
            self._offline_seit = self._offline_seit or jetzt
            if jetzt - self._offline_seit >= self.offline_s:
                return self._abbruch("Quelle seit %.0f s offline"
                                     % (jetzt - self._offline_seit))
        else:
            self._offline_seit = None
            log.warning("Sendebrücke %s: Quelle nicht auflösbar (%s) "
                        "— Pausenbild bleibt, neuer Versuch in %.0f s.",
                        self.name, fehler, self._pause)
        self._halt.wait(self._pause)
        self._pause = min(self._neustart_max, self._pause * 2)
        return None

    def _fallback(self, grund):
        with self._sperre:
            self._wunsch = FUELLER
            self._wunsch_grund = grund
            if self.aktiv != FUELLER:
                # Der Füller läuft durchgehend, sein nächster Keyframe kommt
                # spätestens nach seinem GOP. Bis dahin schweigt die Weiche.
                self.aktiv = "wechsel"
