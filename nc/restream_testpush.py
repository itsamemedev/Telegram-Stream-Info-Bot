"""nc.restream_testpush — B161: sichere Test-Pushes auf Restream-Ingests.

════════════════════════════════════════════════════════════════════════
WOZU DIESES MODUL EXISTIERT
════════════════════════════════════════════════════════════════════════
Ein Test-Push schickt ein synthetisches ffmpeg-Testbild (testsrc) an einen
RTMP(S)-Ingest, um VOR dem echten Sendestart zu prüfen: nimmt die Plattform
den Key an, oder kommt 403/refused zurück? Das beantwortet die Frage, die
START_HIER bisher nur raten ließ ("stimmt der Kick-Key noch?") — ohne einen
echten Stream aufzusetzen.

Der gefährliche Teil ist NICHT das Testbild, sondern WOHIN es geht. Der
produktive Kick-Kanal (kick.com/<slug>) ist öffentlich. Ein Testbild auf den
LIVE-Ingest-Key erscheint dort für jeden Zuschauer. Deshalb ist die
Voreinstellung dieses Moduls IMMER ein eigener Test-Ingest/-Key (ein zweiter,
unbeworbener Slot oder ein lokaler mediamtx/nginx-rtmp-Loopback). Der Live-Key
ist nur mit ausdrücklicher Doppel-Freigabe erreichbar und selbst dann nie,
während der Kanal live ist.

════════════════════════════════════════════════════════════════════════
WARUM BOT-FREI
════════════════════════════════════════════════════════════════════════
Wie nc.restream_guard steckt die heikle Entscheidung — DARF gepusht werden? —
in reinen Funktionen ohne DB, ohne asyncio, ohne ffmpeg. So ist die
Sicherheitslogik vollständig testbar (test_restream.py) und kann nicht durch
einen Seiteneffekt im Monolithen kippen. Der Bot liefert nur die Fakten
(läuft ein Restream? ist der Kanal live?) und führt den Subprozess aus; die
Freigabe fällt hier.
"""

from dataclasses import dataclass

# Ziel-Auswahl
TARGET_TEST = "test"          # eigener Test-Ingest/-Key (Voreinstellung, sicher)
TARGET_LIVE = "live"          # produktiver Kick-Ingest/-Key (nur mit Doppel-Freigabe)

# Kanal-Live-Zustand (bewusst dreiwertig, wie restream_guard: UNKNOWN ist NICHT OFFLINE)
CH_LIVE = "live"
CH_OFFLINE = "offline"
CH_UNKNOWN = "unknown"


@dataclass
class TestPushConfig:
    """Alle Fakten für eine Test-Push-Entscheidung. Der Bot baut das Objekt zur
       Laufzeit frisch aus der .env (Modul-Konstanten würden die .env einfrieren)."""
    test_ingest: str = ""         # RESTREAM_TEST_INGEST
    test_key: str = ""            # RESTREAM_TEST_KEY
    live_ingest: str = ""         # aufgelöst wie start(): DB-Zeile zuerst, sonst KICK_INGEST_URL
    live_key: str = ""            # aufgelöst wie start(): DB-Zeile zuerst, sonst KICK_STREAM_KEY
    live_key_source: str = ""     # "db" | "env" | "" — nur zur Anzeige/Diagnose
    allow_live: bool = False      # RESTREAM_TEST_ALLOW_LIVE
    duration_s: int = 8           # RESTREAM_TEST_DURATION_S
    fps: int = 30                 # RESTREAM_TEST_FPS


@dataclass
class ResolvedTarget:
    ok: bool
    source: str = ""              # "test" | "live" | ""
    ingest: str = ""
    key: str = ""
    is_live_key: bool = False     # True, wenn der Key dem produktiven Live-Key ENTSPRICHT
    error: str = ""


def resolve_target(cfg: TestPushConfig, prefer: str = TARGET_TEST) -> ResolvedTarget:
    """Wählt Ingest+Key. Voreinstellung Test-Slot. Der Live-Slot wird nur
       geliefert, wenn ausdrücklich verlangt UND freigegeben.

       WICHTIG: is_live_key wird über einen KEY-VERGLEICH bestimmt, nicht über
       das Label. Ist ein Test-Key versehentlich identisch mit dem Live-Key
       (Fehlkonfiguration), gilt er als Live-Key und fällt unter dessen
       Schutzregeln — sonst wäre die Isolation nur nominell."""
    live_key = (cfg.live_key or "").strip()

    def _is_live(k: str) -> bool:
        return bool(live_key) and (k or "").strip() == live_key

    if prefer == TARGET_LIVE:
        if not cfg.allow_live:
            return ResolvedTarget(False, error="live_gesperrt")
        if not (cfg.live_ingest and live_key):
            return ResolvedTarget(False, error="live_unkonfiguriert")
        return ResolvedTarget(True, TARGET_LIVE, cfg.live_ingest.strip(),
                              live_key, True, "")

    # Standardpfad: eigener Test-Slot
    tk = (cfg.test_key or "").strip()
    ti = (cfg.test_ingest or "").strip()
    if ti and tk:
        return ResolvedTarget(True, TARGET_TEST, ti, tk, _is_live(tk), "")

    # Kein Test-Slot gesetzt. NICHT still auf den Live-Key ausweichen — das wäre
    # genau die versehentliche Live-Sendung, die dieses Modul verhindert.
    return ResolvedTarget(False, error="kein_test_ziel")


@dataclass
class GuardDecision:
    allowed: bool
    reason: str                   # Maschinen-Code (für Tests/Logik)
    http: int = 200               # passender HTTP-Status für die Route
    message: str = ""             # deutscher Klartext für die Oberfläche


def guard(cfg: TestPushConfig, tgt: ResolvedTarget, *,
          active_all_nonempty: bool, channel: str, confirm: bool) -> GuardDecision:
    """Die Sicherheitsentscheidung. Reihenfolge = Schwere absteigend.

       active_all_nonempty : läuft gerade IRGENDEIN vom Bot gestarteter Restream?
                             (ein Kick-Key = ein Slot → Kollision, egal welches Ziel)
       channel             : CH_LIVE / CH_OFFLINE / CH_UNKNOWN des produktiven Kanals
       confirm             : hat der Bediener ausdrücklich bestätigt?
    """
    if not tgt.ok:
        msg = {
            "live_gesperrt": "Live-Key ist gesperrt. RESTREAM_TEST_ALLOW_LIVE=1 setzen, um ihn freizugeben.",
            "live_unkonfiguriert": "Kein Live-Ingest/-Key auflösbar (weder DB-Ziel noch .env).",
            "kein_test_ziel": "Kein Test-Ziel gesetzt. RESTREAM_TEST_INGEST und RESTREAM_TEST_KEY in der .env eintragen.",
        }.get(tgt.error, "Test-Ziel nicht auflösbar.")
        return GuardDecision(False, tgt.error, 400, msg)

    # 1. Laufender Restream — der Slot ist belegt, ein Test-Push würde kollidieren.
    if active_all_nonempty:
        return GuardDecision(False, "restream_active", 409,
                             "Es läuft bereits ein Restream. Test-Push würde mit dem Sende-Slot kollidieren — erst stoppen.")

    # Test-Slot (eigener Key, KEIN Live-Key): sicher isoliert. Nur Bestätigung nötig.
    if not tgt.is_live_key:
        if not confirm:
            return GuardDecision(False, "confirm_required", 428,
                                 "Test-Push senden? Zur Bestätigung confirm=true mitschicken.")
        return GuardDecision(True, "ok_test", 200, "")

    # Ab hier: der Key IST der produktive Live-Key. Schärfste Stufe.
    if not cfg.allow_live:
        return GuardDecision(False, "live_forbidden", 403,
                             "Das ist der LIVE-Kanal-Key. Gesperrt — RESTREAM_TEST_ALLOW_LIVE=1 nötig.")

    # 2. Kanal ist nachweislich live → niemals ein Testbild darüberlegen.
    if channel == CH_LIVE:
        return GuardDecision(False, "channel_live", 423,
                             "Der Kanal ist gerade LIVE. Test-Push auf den Live-Key würde das öffentliche Bild stören — abgelehnt.")

    # 3. Kanal-Status unklar → nicht beweisbar sicher, also nicht senden.
    if channel != CH_OFFLINE:
        return GuardDecision(False, "channel_unknown", 425,
                             "Live-Status des Kanals unklar (Kick-API nicht erreichbar). Test auf den Live-Key nur bei bestätigtem Offline.")

    # 4. Auch bei freiem, offlinem Live-Kanal: ausdrückliche Bestätigung Pflicht.
    if not confirm:
        return GuardDecision(False, "confirm_required_live", 428,
                             "ACHTUNG: Test-Push auf den LIVE-Kanal-Key. Nur mit ausdrücklicher Bestätigung (confirm=true).")

    return GuardDecision(True, "ok_live", 200, "")


def build_cmd(ingest: str, key: str, normalize_ingest, *,
              duration_s: int = 8, fps: int = 30) -> list:
    """ffmpeg-Argv für einen kurzen Testbild-Push (testsrc2 + Sinuston → FLV).

       normalize_ingest: der Bot reicht sein _normalize_ingest hier hinein, damit
       das Ziel BITGENAU so gebaut wird wie im echten Restream (IVS/Kick brauchen
       :443 + /app; ein abweichender Ziel-String testet den falschen Endpunkt).
       Kein Quell-Pull, keine Cookies — reines synthetisches Signal."""
    fps = max(1, min(60, int(fps)))
    dur = max(1, min(30, int(duration_s)))       # hart gedeckelt: ein Test, kein Stream
    target = normalize_ingest(ingest) + "/" + key
    gop = fps * 2
    return [
        "ffmpeg", "-hide_banner", "-loglevel", "error",
        "-re", "-f", "lavfi", "-i", f"testsrc2=size=1280x720:rate={fps}",
        "-f", "lavfi", "-i", "sine=frequency=440:sample_rate=44100",
        "-c:v", "libx264", "-preset", "veryfast", "-tune", "zerolatency",
        "-pix_fmt", "yuv420p", "-g", str(gop), "-keyint_min", str(gop),
        "-b:v", "2500k", "-maxrate", "2500k", "-bufsize", "5000k",
        "-c:a", "aac", "-b:a", "128k", "-ar", "44100",
        "-t", str(dur), "-f", "flv", target,
    ]


def classify_result(rc, stderr: str) -> dict:
    """ffmpeg-Ende → {state, detail}. state ∈ ok|forbidden|refused|timeout|error.

       Spiegelt die Fehlerbilder, die der echte Restream an der Kick-Ingest sieht
       (403 = Key falsch/abgelaufen; refused = Host/Port zu; End-of-file = TLS/App-
       Pfad falsch). So ist das Test-Ergebnis 1:1 auf den Produktivpfad übertragbar."""
    s = (stderr or "").lower()
    if rc == 0:
        return {"state": "ok", "detail": "Ingest hat den Push angenommen."}
    if "403" in s or "forbidden" in s:
        return {"state": "forbidden", "detail": "403/Forbidden — Stream-Key falsch oder abgelaufen."}
    if "connection refused" in s or "refused" in s or "connection reset" in s:
        return {"state": "refused", "detail": "Verbindung abgelehnt — Ingest-Host/Port prüfen."}
    if "timed out" in s or "timeout" in s:
        return {"state": "timeout", "detail": "Zeitüberschreitung — Ingest antwortet nicht."}
    if "end of file" in s or "i/o error" in s or "input/output error" in s or "server error" in s:
        return {"state": "error", "detail": "TLS/Handshake fehlgeschlagen — Ingest-URL (Port 443 / /app-Pfad) prüfen."}
    tail = (stderr or "").strip().splitlines()[-1:] or [""]
    return {"state": "error", "detail": f"ffmpeg rc={rc}: {tail[0][:160]}"}


def fingerprint(key: str) -> dict:
    """Key NIE im Klartext (wie start() in bot.py): Länge + Quersumme reichen,
       um den benutzten Key gegen den im Kick-Dashboard zu vergleichen."""
    k = (key or "").encode("utf-8")
    return {"len": len(k), "fp": sum(k) % 65536}
