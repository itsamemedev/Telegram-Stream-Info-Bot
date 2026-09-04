"""nc.routes.selbsttest — /api/selftest als Flask-Blueprint.

v4.2-W5, letzte Teillieferung von Vorschlag 2: damit steht keine System-Route
mehr im Monolithen.

Der Selbsttest ist die laengste der acht (226 Zeilen) und die einzige, die
quer durch alle Domaenen liest — Dauerlaeufer, Restream-Ziele, Moderation,
Abwehr. Genau deshalb kam sie zuletzt: erst musste der Zustand, den sie
abfragt, ueberall sonst aufgeloest sein.

Er kostet **keinen** neuen nc.ctx-Slot:

* Der Restream-Manager kommt aus dem Register nc/restreamstate.py (W18).
* Sperrliste und Angriffe kommen ueber die HAKEN, die nc/routes/abwehr.py
  seit W25 ohnehin haelt — dieselben zwei Funktionen, die das Abwehr-Panel
  benutzt. Ein zweiter Weg zu denselben Daten waere eine zweite Wahrheit.
* Alles Uebrige sind .env-Werte und geteilte Zustands-Dicts aus ctx.cfg.

`_st_befund` ist mitgewandert: 23 Aufrufe, alle in dieser einen Funktion.
Im Monolithen stand er daneben, hier gehoert er hin.
"""
import os
import shutil
import time

from flask import Blueprint, jsonify

from nc import ctx as _ctx
from nc import fehlertext as _nc_fehlertext
from nc import restream_targets as _nc_rst
from nc import restreamstate as _nc_rsstate
from nc.routes import abwehr as _nc_routes_abwehr

bp = Blueprint("selbsttest", __name__)


def _c():
    """Laufzeitkontext. Aufruf statt Modul-Konstante — er wird erst beim
       Bot-Start gefuellt."""
    return _ctx.get()


class _LazyLog:
    def __getattr__(self, name):
        return getattr(_c().log, name)


log = _LazyLog()


def _fehler_text(e, wo=""):
    """v4.1-W30: der Wortlaut ins Log, nach aussen die gesaeuberte Fassung."""
    return _nc_fehlertext.nach_aussen(e, wo)


def _mgr():
    """Der Restream-Manager aus dem Register — oder None vor dem Start.

    Die Aufrufer pruefen auf None. Ein AttributeError haette hier die GANZE
    Selbsttest-Antwort gekippt, also auch die 20 Befunde, die nichts mit
    Restream zu tun haben.
    """
    return _nc_rsstate.MGR["obj"]


def _haken(name):
    """Sperrliste bzw. Angriffe ueber den Haken, den der Bot in
       nc/routes/abwehr.py eintraegt.

    Gibt {} zurueck, wenn der Haken fehlt (Bot laeuft nicht). Der Aufrufer
    unterscheidet das von einem leeren Ergebnis — bei einer Sicherheitsanzeige
    ist "gar nicht nachgesehen" etwas anderes als "nichts gefunden", genau
    wie in nc/routes/abwehr._nicht_bereit().
    """
    fn = _nc_routes_abwehr.HAKEN[name]["fn"]
    if fn is None:
        return {}
    try:
        return fn() or {}
    except Exception as e:
        log.warning("selbsttest: Haken %s: %s", name, e)
        return {}


def _st_befund(liste, schwere, bereich, befund, fix=None):
    """schwere: 'rot' (sendet nicht / Datenverlust) | 'gelb' (eingeschraenkt)."""
    liste.append({"schwere": schwere, "bereich": bereich,
                  "befund": befund, "fix": fix})


@bp.route("/api/selftest")
def api_selftest():
    """Aggregierte Selbstdiagnose. Ueber den SSH-Tunnel:
       curl -s localhost:8050/api/selftest | python3 -m json.tool"""
    c = _c().cfg
    b = []
    try:
        # ── gestoerte Dauerschleifen ────────────────────────────────────
        # Das Wertvollste hier: _LOOP_FEHLER weiss, WELCHE Schleife klemmt.
        # Faellt _backup_loop aus, laufen Backups nicht — das sah man bisher
        # nirgends, weil die Schleifen auf log.debug abfingen.
        for name, st in sorted(c["_LOOP_FEHLER"].items()):
            alter = time.monotonic() - st[0]
            _st_befund(b, "rot", "Schleife",
                       f"{name} ist gestoert (letzte Meldung vor {int(alter)}s, "
                       f"{st[1]} weitere unterdrueckt)",
                       f"journalctl -u tiktok-bot | grep 'Schleife {name}'")

        # ── Restream: sendet ueberhaupt etwas? ──────────────────────────
        _m = _mgr()
        laeuft = sorted((getattr(_m, "_procs", None) or {}).keys())
        ziele = [n for n, _u in _nc_rst.active_targets()]   # v4.0-W77
        if not laeuft:
            _st_befund(b, "gelb", "Restream", "kein Restream aktiv",
                       "Normal, wenn gerade keine Quelle live ist.")

        # ── Encoder-Rueckstand: CPU-gebunden oder nicht? ────────────────
        # Die entscheidende Zahl bei "der Restream laggt". ffmpeg meldet
        # speed=1.0x, wenn es Echtzeit schafft. Faellt der Wert darunter,
        # kommt der Encoder NICHT hinterher — dann ist es wirklich CPU.
        # Bleibt er bei ~1.0x und es ruckelt trotzdem, ist es Puffer oder
        # Netz, und mehr CPU aendert nichts. Ohne diese Unterscheidung dreht
        # man an den falschen Schrauben.
        for rid, info in sorted((getattr(_mgr(), "_procs", None) or {}).items()):
            h = info.get("health") or {}
            sp = h.get("speed")
            langsam = h.get("slow_ticks", 0)
            try:
                spf = float(str(sp).rstrip("x")) if sp else None
            except (TypeError, ValueError):
                spf = None
            if spf is not None and spf < 0.95:
                _st_befund(b, "rot", "Encoder",
                           f"Restream #{rid}: ffmpeg schafft nur {sp} Echtzeit "
                           f"({langsam} langsame Takte) — CPU-gebunden, das Bild "
                           f"laeuft dem Encoder davon",
                           "FFMPEG_THREADS_LIVE erhoehen (Default 3, bei tee laeuft "
                           "nur EIN Encoder) oder RESTREAM_BITRATE_K senken")
            elif langsam >= 3:
                _st_befund(b, "gelb", "Encoder",
                           f"Restream #{rid}: {langsam} langsame Takte, aktuell {sp}",
                           "Grenzwertig — bei Lastspitzen reisst es ab.")
            if info.get("transcode"):
                _st_befund(b, "gelb", "Encoder",
                           f"Restream #{rid} laeuft im Transcode (kostet CPU). "
                           f"Ziele: {', '.join(ziele) or '?'}",
                           "Nur EIN Ziel? Dann ist Transcode vermeidbar. Mehrere "
                           "Ziele erzwingen ihn (RESTREAM_MULTI_ALLOW_COPY=0).")

        # ── Kick: welcher Ausgang ist tot? ──────────────────────────────
        for zielname, tf in ((_mgr().tee_fehler() if _mgr() else {}) or {}).items():   # v4.0-W116
            alter = time.time() - (tf.get("ts") or 0)
            if alter < 3600:
                _st_befund(b, "rot", "Restream",
                           f"ffmpeg meldet Ziel '{zielname}' abgelehnt "
                           f"(vor {int(alter)}s): {(tf.get('msg') or '')[:160]}",
                           "journalctl -u tiktok-bot | grep 'Kick-Ziel:' "
                           "— zeigt Ingest und Key-Herkunft (db schlaegt .env)")

        # ── YouTube ─────────────────────────────────────────────────────
        yt_grund = c["_YT_INGEST_CACHE"].get("reason") or ""
        # Bodenwahrheit zuerst: steht YouTube wirklich in der Zielliste? Alles
        # andere ist Absicht, das hier ist Wirkung. multistream_targets()
        # verlangt enabled UND ingest UND key — faellt eines aus, fehlt das
        # Ziel im tee, ohne dass irgendwo "YouTube" auftaucht.
        if c["YOUTUBE_ENABLED"] and c["HAT_YOUTUBE_KEY"] and "youtube" not in ziele:
            fehlt = []
            if not c["YOUTUBE_INGEST_URL"]:
                fehlt.append("YOUTUBE_INGEST_URL ist leer")
            if not _nc_rst._CFG.get("youtube_enabled"):
                fehlt.append("youtube_enabled im Restream-Modul steht auf False")
            if not _nc_rst._CFG.get("youtube_key"):
                fehlt.append("youtube_key im Restream-Modul ist leer "
                             "(wurde von _youtube_restream_autoconfig geleert?)")
            _st_befund(b, "rot", "YouTube",
                       "YOUTUBE_ENABLED=1 und YOUTUBE_STREAM_KEY gesetzt, aber "
                       "YouTube ist KEIN Sendeziel. " + ("; ".join(fehlt) or
                       "Grund unklar — .env nach dem Setzen neu geladen? "
                       "Modul-Konstanten werden nur beim Start gelesen."),
                       "sudo systemctl restart tiktok-bot   # .env wirkt erst "
                       "nach Neustart")
        if c["YOUTUBE_ENABLED"] and not c["HAT_YOUTUBE_KEY"]:
            if not c["_YT_INGEST_CACHE"].get("key"):
                _st_befund(b, "rot", "YouTube",
                           f"kein Stream-Key aufgeloest: {yt_grund or 'noch nicht versucht'}",
                           "In YouTube Studio einen Live-Stream anlegen, dann: "
                           "curl -s localhost:8050/api/restream/deck")
            elif not c["_YT_INGEST_CACHE"].get("bound"):
                _st_befund(b, "gelb", "YouTube",
                           "sendet auf den persistenten Key — kein aktiver oder "
                           "geplanter Broadcast gefunden. Bild erscheint erst, "
                           "wenn YouTube den Broadcast selbst startet.",
                           "In YouTube Studio den Stream starten.")
        elif not c["YOUTUBE_ENABLED"]:
            _st_befund(b, "gelb", "YouTube", "YOUTUBE_ENABLED=0",
                       "In der .env auf 1 setzen und Dienst neu starten.")

        # ── Ingest-Adressen auf offensichtlich Falsches pruefen ─────────
        # Aus dem echten error.log: rtmp://live.twitch.tv/app/<key> — das ist
        # Twitchs WEBserver, kein RTMP-Ingest. ffmpeg meldet darauf nur
        # "Input/output error"; dass die Adresse selbst falsch ist, sieht man
        # der Meldung nicht an. Solche Adressen sind statisch pruefbar.
        if c["TWITCH_ENABLED"] and c["TWITCH_INGEST_URL"]:
            _t = c["TWITCH_INGEST_URL"].lower()
            if "contribute.live-video.net" not in _t:
                _st_befund(b, "rot", "Twitch",
                           f"TWITCH_INGEST_URL zeigt auf '{c['TWITCH_INGEST_URL']}' — "
                           "Twitch nimmt RTMP nur auf *.contribute.live-video.net "
                           "an. Jede andere Adresse endet in 'Input/output error'.",
                           "TWITCH_INGEST_URL=rtmp://ingest.global-contribute."
                           "live-video.net/app  (dann Dienst neu starten)")
        if c["KICK_INGEST_URL"] and not c["KICK_INGEST_URL"].lower().startswith(("rtmp://", "rtmps://")):
            _st_befund(b, "rot", "Kick",
                       f"KICK_INGEST_URL ist keine RTMP-Adresse: {c['KICK_INGEST_URL']}",
                       "Im Kick-Dashboard die Ingest-URL kopieren (rtmps://…).")

        # ── Quell-URL-Ablauf: Telemetrie, kein Fehler ───────────────────
        for rid, n in sorted((getattr(_mgr(), "_srcexpired", None) or {}).items()):
            if n >= 3:
                _st_befund(b, "gelb", "Quelle",
                           f"Restream #{rid}: TikTok-Quell-URL lief {n}x ab und "
                           "wurde jedesmal erneuert — der Stream laeuft, es "
                           "kostet nur je ~2s Unterbrechung",
                           "Normal. Nur wenn es im Minutentakt passiert, lohnt "
                           "ein Blick auf RECORD_PROXY.")

        # ── AZRAEL: antwortet er auf Ansprache? ─────────────────────────
        # AZRAEL_CHAT_REPLY steht per Default auf 0 — dann gibt der Gate
        # _azrael_chat_should_reply() sofort False zurueck und AZRAEL
        # schweigt auf Kick, Twitch UND YouTube. Von aussen sieht das aus
        # wie ein kaputter Bot, ist aber eine nie gesetzte Variable.
        if not c["AZRAEL_CHAT_REPLY"]:
            _st_befund(b, "gelb", "AZRAEL",
                       "antwortet NICHT auf Ansprache im Stream-Chat "
                       "(AZRAEL_CHAT_REPLY=0) — betrifft Kick, Twitch und "
                       "YouTube gleichzeitig",
                       "AZRAEL_CHAT_REPLY=1 in die .env, dann Dienst neu starten")

        # ── AZRAEL: kommt er ueberhaupt ins Publikum? ───────────────────
        # Lange unbemerkt: die Reaktionen liefen in Stimme, Overlay, Dashboard
        # und Discord, aber in keinen Stream-Chat. Wenn kein Kanal sendefaehig
        # ist, soll das hier stehen und nicht erst auffallen, wenn jemand die
        # Chats vergleicht.
        if c["AZRAEL_REACT_TO_CHAT"]:
            _kanaele = []
            if c["_KICK_MOD"]:
                _kanaele.append("kick")
            if c["_TWITCH_SEND"].get("fn"):
                _kanaele.append("twitch")
            if c["_YT_SEND"].get("fn"):
                _kanaele.append("youtube")
            if not _kanaele:
                _st_befund(b, "rot", "AZRAEL",
                           "kein Stream-Chat sendefaehig — Reaktionen erscheinen "
                           "nur in Overlay/Stimme/Discord, nicht im Chat",
                           "Kick: KICK_CLIENT_ID/SECRET · Twitch: OAuth im "
                           "Dashboard verbinden · YouTube: aktiver Live-Chat")
            elif len(_kanaele) < 3:
                _st_befund(b, "gelb", "AZRAEL",
                           f"sendet nur nach: {', '.join(_kanaele)}",
                           "Die fehlenden Kanaele sind nicht verbunden.")

        # ── Abwehr ──────────────────────────────────────────────────────
        try:
            f2b = _haken("sperrliste")
            if not f2b.get("ok"):
                _st_befund(b, "gelb", "Abwehr",
                           f"CrowdSec: {f2b.get('hint') or f2b.get('error')}",
                           f2b.get("fix"))
            atk = _haken("angriffe")
            if not atk.get("ok"):
                _st_befund(b, "gelb", "Abwehr",
                           f"Auth-Log: {atk.get('hint') or atk.get('error')}",
                           atk.get("fix"))
        except Exception as e:
            _st_befund(b, "gelb", "Abwehr",
                       f"Abwehr-Pruefung selbst gescheitert: "
                       f"{_fehler_text(e, 'api_selftest')}")

        # ── Herzschlaege: schweigt ein Kern-Loop? ───────────────────────
        now = time.monotonic()
        for name, last in sorted((c["_HEARTBEATS"] or {}).items()):
            still = now - last
            if still > 900:
                _st_befund(b, "rot", "Herzschlag",
                           f"{name} meldet sich seit {int(still)}s nicht mehr",
                           "journalctl -u tiktok-bot -n 200 --no-pager")

        # ── Platte ──────────────────────────────────────────────────────
        try:
            # shutil, nicht _sh: '_sh' ist nur ein lokaler Alias innerhalb von
            # _alert_monitor_loop und hier nicht sichtbar.
            du = shutil.disk_usage(_c().recordings_dir if os.path.isdir(_c().recordings_dir) else "/")
            pct = 100 * (du.total - du.free) / du.total if du.total else 0
            if pct >= 90:
                _st_befund(b, "rot", "Platte", f"zu {pct:.0f}% voll",
                           "curl -X POST localhost:8050/api/system/cleanup")
            elif pct >= 80:
                _st_befund(b, "gelb", "Platte", f"zu {pct:.0f}% voll")
        except Exception:
            pass

        rot = sum(1 for x in b if x["schwere"] == "rot")
        return jsonify(
            ok=True,
            urteil=("kaputt" if rot else ("eingeschraenkt" if b else "gesund")),
            befunde=b, anzahl_rot=rot, anzahl_gelb=len(b) - rot,
            kontext={
                "restreams_aktiv": laeuft,
                "restream_ziele": ziele,
                "youtube": {"aktiviert": bool(c["YOUTUBE_ENABLED"]),
                            "key_quelle": ("env" if c["HAT_YOUTUBE_KEY"]
                                           else (c["_YT_INGEST_CACHE"].get("source") or "")),
                            "broadcast": c["_YT_INGEST_CACHE"].get("broadcast", ""),
                            "grund": yt_grund},
                "db_backend": c["DB_BACKEND"],
                "schleifen_gestoert": sorted(c["_LOOP_FEHLER"].keys()),
            })
    except Exception as e:
        log.error("api_selftest: %s", e, exc_info=True)
        return jsonify(ok=False, error=_fehler_text(e, "api_selftest")), 500
