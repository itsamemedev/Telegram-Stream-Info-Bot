"""nc.restream_stability — v4.0-W113: Wiederanlauf-Regeln fuer den Restream-Relay.

════════════════════════════════════════════════════════════════════════
WARUM DIESES MODUL BOT-FREI IST
════════════════════════════════════════════════════════════════════════
Die Wiederanlauf-Logik lag verstreut in RestreamManager._monitor: Zaehler,
Backoff, Ablauf-Sonderfall und Codec-Fallback in einer Methode, die ohne
laufendes ffmpeg, laufende DB und laufenden Event-Loop gar nicht erst
anlaeuft — also nie geprueft wurde. Falsch gebaut erzeugt genau diese
Logik entweder eine Neustart-Schleife (schlimmer als der Ausfall) oder
einen Restream, der nach fuenf Huepfern fuer den Rest der Nacht wegbleibt.
Deshalb steht sie hier als reine Funktionen: stdlib-only, kein Import aus
bot_v37, vollstaendig testbar.

════════════════════════════════════════════════════════════════════════
DIE FUENF BEFUNDE, DIE HIER BEHOBEN WERDEN
════════════════════════════════════════════════════════════════════════
1. DAS RECONNECT-BUDGET WURDE NIE ZURUECKGEGEBEN.
   MAX_RECONNECTS=5, und `attempts` wanderte von Reconnect zu Reconnect
   weiter — zurueckgesetzt wurde es nur beim Start von Hand. Ein Restream,
   der acht Stunden laeuft und dabei fuenfmal kurz stolpert, galt danach
   als "aufgegeben nach 5 Reconnects", obwohl jeder einzelne Lauf
   stundenlang sauber war. Danach half nur noch die Verify-Schleife —
   mit 120s-Takt und bis zu 900s Backoff statt 8s. Das ist das Bild
   "der Restream kommt nicht mehr von allein zurueck".
   Fuer die UNABHAENGIGEN Relays wurde genau das in W87 schon repariert
   (`if _ran > 120: attempt = 0`); der Hauptpfad blieb aussen vor.
   -> budget_after_run()

2. BACKOFF OHNE STREUUNG.
   `min(60, 8*(attempts+1))` ist fuer jeden Restream identisch. Faellt das
   Netz kurz aus, sterben alle gleichzeitig und kommen auf die Sekunde
   gleichzeitig zurueck — gegen dieselbe TikTok-Aufloesung und dieselbe
   Ingest. Das ist der direkte Weg ins 429, und ein 429 sieht fuer den
   Bot aus wie "Quelle unknown".
   -> reconnect_delay() mit Streuung, echt exponentiell statt linear.

3. DER ABLAUF-PFAD HATTE KEINE UNTERGRENZE.
   Abgelaufene TikTok-Quell-URL -> 2s Pause, neuer Versuch, KEIN
   Fehlversuch. Das ist richtig, solange ffmpeg vorher Minuten lief (der
   Normalfall: TikToks Signaturen halten ~6 Minuten). Stirbt der Prozess
   aber nach einer halben Sekunde und die Meldung sieht nur AUS wie ein
   Ablauf — ein 404 kommt auch von einer dauerhaft toten Edge — dreht
   sich die Schleife alle 2s: Resolve plus ffmpeg-Spawn, endlos, ohne
   dass ein Zaehler jemals greift. `_srcexpired` zaehlte das mit, tat
   aber nichts damit.
   -> expired_delay(): schnell bleiben, solange es der Normalfall ist;
      bremsen, sobald es einer Schleife aehnelt.

4. DER CODEC-FALLBACK SPRANG AUF NETZFEHLER AN.
   Die Heuristik matcht unter anderem "failed to" und "unable to" —
   beides steht wortwoertlich in "Failed to resolve hostname" und
   "Unable to open resource". Ein kurzer Netzhaenger in den ersten 25
   Sekunden schaltete den Restream damit fuer die GANZE Sitzung auf
   transcode (_force_transcode ist persistent). Auf dem GPU-losen Server
   ist der Encode-Rueckstand laut der eigenen Warnung des Bots "die
   typische Disconnect-Ursache" — der vermeintliche Fix erzeugte also
   genau das Problem, gegen das er antrat.
   -> is_codec_failure() prueft ZUERST auf Netz/Quelle und verneint dort.

5. EIN HAENGENDER FFMPEG WURDE NIE BEMERKT.
   Stirbt der Prozess, greift _monitor. Bleibt er am Leben, ohne noch ein
   Bild zu schreiben — RTMP-Ausgang blockiert, Input steht, tee-Slave mit
   onfail=ignore weggebrochen — passiert NICHTS: -progress verstummt oder
   wiederholt denselben Frame-Stand, health friert auf dem letzten Wert
   ein, und das Panel zeigt weiter "live". Das ist der Ausfall, den der
   Betreiber als "der Stream ist einfach weg und im Log steht nichts"
   erlebt.
   -> stall_verdict(): Fortschritt heisst Bild ODER Bytes, nicht
      "es kam ein progress-Block an".

════════════════════════════════════════════════════════════════════════
DIE REGELN, DIE EINE NEUSTART-SCHLEIFE VERHINDERN
════════════════════════════════════════════════════════════════════════
* Budget zurueckgeben nur nach einem Lauf, der NACHWEISLICH Bild
  geliefert hat. Ein Lauf, den der Stillstands-Waechter abgeschossen hat,
  war lang, aber nicht gesund — er darf das Budget nicht auffuellen,
  sonst haemmert ein toter Ingest ewig im 8s-Takt.
* Karenz vor der Stillstands-Bewertung: RTMP-Handshake, Probe und der
  erste Keyframe brauchen Zeit; vorher gibt es legitim keinen Fortschritt.
* Blind heisst nicht tot: liefert der progress-Leser gar nichts (Reader-
  Task gestorben), wird NICHT abgeschossen — Unwissen ist kein Beweis.
  Diese Regel steht bewusst hier und nicht nur im Aufrufer.
"""

from __future__ import annotations

import random
from dataclasses import dataclass

# ── Ergebnis der Stillstands-Bewertung ────────────────────────────────────
STALL_OK = "ok"              # laeuft, Fortschritt gesehen
STALL_GRACE = "grace"        # noch in der Anlaufkarenz — nicht bewerten
STALL_BLIND = "blind"        # keine Messwerte (Reader tot) — nicht bewerten
STALL_DEAD = "stalled"       # Prozess lebt, liefert aber nichts mehr


@dataclass(frozen=True)
class ReconnectPolicy:
    """Alle Stellschrauben an einem Ort. Werte sind bewusst konservativ:
       lieber einmal zu spaet neu aufbauen als eine Neustart-Schleife."""
    max_reconnects: int = 5
    # Ein Lauf gilt als gesund, wenn er so lange durchhielt. 180s liegt klar
    # ueber der TikTok-Signaturdauer-Untergrenze und ueber jedem Handshake.
    stable_run_s: float = 180.0
    base_delay_s: float = 8.0
    max_delay_s: float = 60.0
    jitter: float = 0.25              # +/-25 % Streuung
    # Ablauf-Pfad: so lange gilt ein Lauf als "sofort gestorben".
    expired_short_run_s: float = 20.0
    expired_delays_s: tuple = (2.0, 2.0, 5.0, 15.0, 30.0, 60.0)
    # Stillstands-Waechter.
    stall_grace_s: float = 60.0       # Karenz nach Prozessstart
    stall_timeout_s: float = 75.0     # so lange ohne Bild/Bytes = tot
    stall_check_s: float = 15.0       # Prueftakt des Waechters


@dataclass(frozen=True)
class StallVerdict:
    state: str
    reason: str = ""

    @property
    def stalled(self) -> bool:
        return self.state == STALL_DEAD


# ── 1) Reconnect-Budget ───────────────────────────────────────────────────
def budget_after_run(attempts: int, ran_s: float, policy: ReconnectPolicy,
                     *, progressed: bool = True) -> int:
    """Wie viele Fehlversuche stehen nach diesem Lauf zu Buche?

    `progressed=False` ist der Fall "lang gelaufen, aber nichts gesendet"
    (vom Stillstands-Waechter abgeschossen). Der Lauf war dann zwar lang,
    aber eben NICHT gesund — er darf das Budget nicht auffuellen, sonst
    baut der Bot gegen einen toten Ingest ewig im 8s-Takt neu auf.
    """
    if progressed and ran_s >= policy.stable_run_s:
        return 0
    return max(0, int(attempts))


def budget_exhausted(attempts: int, policy: ReconnectPolicy) -> bool:
    return int(attempts) >= policy.max_reconnects


# ── 2) Backoff ────────────────────────────────────────────────────────────
def reconnect_delay(attempts: int, policy: ReconnectPolicy,
                    rnd: random.Random | None = None) -> float:
    """Exponentiell mit Deckel und Streuung.

    Exponentiell statt linear, weil ein Fehler, der drei Versuche
    ueberlebt, meist auch den vierten ueberlebt; Streuung, damit mehrere
    gleichzeitig gestorbene Restreams nicht im Gleichschritt gegen
    dieselbe Ingest und dieselbe TikTok-Aufloesung zurueckkommen.
    """
    n = max(0, int(attempts))
    raw = policy.base_delay_s * (2 ** min(n, 8))
    raw = min(policy.max_delay_s, raw)
    if policy.jitter <= 0:
        return round(raw, 2)
    r = rnd or random
    lo = raw * (1.0 - policy.jitter)
    hi = raw * (1.0 + policy.jitter)
    # Deckel gilt auch nach der Streuung; Untergrenze 1s, damit die Pause
    # nie so kurz wird, dass der sterbende Prozess seine Ports noch haelt.
    return round(max(1.0, min(policy.max_delay_s, r.uniform(lo, hi))), 2)


# ── 3) Ablauf der Quell-URL ───────────────────────────────────────────────
def expired_streak(prev_streak: int, ran_s: float,
                   policy: ReconnectPolicy) -> int:
    """Zaehlt NUR die Ablaeufe, die verdaechtig schnell aufeinander folgen.

    Ein Ablauf nach mehreren Minuten ist TikToks Normalfall und setzt den
    Zaehler zurueck — dieser Pfad soll schnell bleiben. Ein Ablauf nach
    Sekunden ist keiner: dort steht in Wahrheit eine tote Edge oder ein
    Block hinter dem 404.
    """
    if ran_s >= policy.expired_short_run_s:
        return 0
    return max(0, int(prev_streak)) + 1


def expired_delay(streak: int, policy: ReconnectPolicy) -> float:
    """Pause vor dem naechsten Versuch mit frisch aufgeloester URL."""
    tbl = policy.expired_delays_s or (2.0,)
    i = min(max(0, int(streak)), len(tbl) - 1)
    return float(tbl[i])


def expired_is_spinning(streak: int, policy: ReconnectPolicy) -> bool:
    """Ab hier ist es keine Signatur-Rotation mehr, sondern eine Schleife —
       der Aufrufer soll den Versuch als echten Fehlversuch buchen, damit
       MAX_RECONNECTS und danach der Guard uebernehmen."""
    return int(streak) >= len(policy.expired_delays_s or (2.0,))


# ── 4) Codec-Fallback ─────────────────────────────────────────────────────
# Die Marker des Monolithen, aufgeteilt nach Beweiskraft. Diese Trennung IST
# der Fix: die alte Liste warf beides in einen Topf, und die schwachen Muster
# stehen woertlich in Netzfehlern.
#
# STARK — dafuer gibt es keine harmlose Lesart. Ein solcher Befund bleibt ein
# Codec-Befund, auch wenn in derselben stderr-Kachel Netz-Rauschen steht.
_CODEC_STRONG = ("no such codec", "does not support", "incompatible",
                 "non-monotonous", "invalid data", "could not find")
# SCHWACH — trifft haeufiger daneben als ins Ziel, sobald das Netz wackelt:
# "Failed to resolve hostname", "Unable to open resource", und "Could not
# write header (incorrect codec parameters ?)" ist laut B59 die Folge eines
# flaky Inputs, nicht eines falschen Codecs.
_CODEC_WEAK = ("codec", "unable to", "failed to", "could not write header")

# Netz- und Quellenmuster. Sie entkraeften die SCHWACHEN Marker.
_NET_MARKERS = ("resolve hostname", "name or service not known",
                "temporary failure in name resolution",
                "connection refused", "connection reset", "connection timed out",
                "network is unreachable", "no route to host",
                "operation timed out", "timed out",
                "i/o error", "input/output error", "end of file",
                "server returned 4", "server returned 5",
                "http error 4", "http error 5",
                "403 forbidden", "404 not found",
                "will reconnect", "stream ends prematurely",
                "error in the pull function", "unable to open resource",
                "handshake", "broken pipe")


def looks_like_network_failure(text: str) -> bool:
    t = (text or "").lower()
    return any(s in t for s in _NET_MARKERS)


def is_codec_failure(text: str) -> bool:
    """Ist der fruehe Abbruch WIRKLICH ein Codec-Problem?

    Nur dann lohnt der Umstieg copy -> transcode. Sieht die Zeile nur nach
    Netz oder Quelle aus, ist transcode das falsche Mittel: es kostet auf
    dem GPU-losen Server CPU, die dem Sendebild fehlt, und die Umstellung
    haelt die ganze Sitzung (_force_transcode wird nie geleert). Ein
    Encode-Rueckstand ist laut der eigenen Warnung des Bots "die typische
    Disconnect-Ursache" — der Fallback wuerde dann den Ausfall erzeugen,
    gegen den er antritt.
    """
    t = (text or "").lower()
    if not t:
        return False
    if any(s in t for s in _CODEC_STRONG):
        return True
    if looks_like_network_failure(t):
        return False
    return any(s in t for s in _CODEC_WEAK)


# ── 5) Stillstands-Waechter ───────────────────────────────────────────────
def stall_verdict(ran_s: float, since_advance_s: float | None,
                  policy: ReconnectPolicy, *, reader_alive: bool = True
                  ) -> StallVerdict:
    """Lebt der Prozess noch WIRKLICH — also kommt Bild oder kommen Bytes?

    `since_advance_s` ist die Zeit seit dem letzten Zuwachs an frame ODER
    total_size, NICHT die Zeit seit dem letzten progress-Block: ffmpeg
    schreibt seine Schnappschuesse auch dann weiter, wenn der Ausgang
    blockiert und beide Zaehler stehenbleiben. Genau dieser Fall ist der
    stille Ausfall.

    `reader_alive=False` (der progress-Leser ist gestorben) fuehrt NIE zu
    einem Abschuss: dann fehlen die Messwerte, und Unwissen ist kein
    Beweis fuer einen toten Stream — dieselbe Regel wie UNKNOWN in
    nc.restream_guard.
    """
    if ran_s < policy.stall_grace_s:
        return StallVerdict(STALL_GRACE,
                            f"Anlaufkarenz ({ran_s:.0f}s < {policy.stall_grace_s:.0f}s)")
    if not reader_alive or since_advance_s is None:
        return StallVerdict(STALL_BLIND, "keine Fortschrittsdaten (progress-Leser tot)")
    if since_advance_s >= policy.stall_timeout_s:
        return StallVerdict(
            STALL_DEAD,
            f"seit {since_advance_s:.0f}s kein Bild und keine Bytes "
            f"(Grenze {policy.stall_timeout_s:.0f}s)")
    return StallVerdict(STALL_OK)
