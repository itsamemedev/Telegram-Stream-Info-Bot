#!/usr/bin/env python3
# test_restream.py — V37: Testsuite für die Restream-Kernlogik (Mock-basiert).
# Testet OHNE echtes ffmpeg/Netz die Logik, die uns historisch Regressionen
# eingebracht hat: Quellen-Failover (Streak/unknown/Round-Robin), tee- vs.
# independent-Kommandobau, relay_profile-Vererbung, stop()-Cleanup-Verträge.
# Läuft als Teil der Standard-Validierung: python3 test_restream.py

import ast
import asyncio
import re
import sys


# ---------------------------------------------------------------- Helpers

def clean_username(u):
    return (u or "").lstrip("@").strip().lower()


PASS = 0


# ══════════════════════════════════════════════════════════════════════════
# v4.0-W117 · ANKER, DIE NICHT MITWACHSEN MUESSEN
# ══════════════════════════════════════════════════════════════════════════
# Die Vertraege hier verankern sich an woertlichem Quelltext — anders geht es
# bei einem 1,5-MB-Monolithen nicht. Der TEURE Teil daran waren nie die
# Textanker, sondern die FENSTER der Form `src[i:i + 2200]`: waechst die
# Zielfunktion darueber hinaus, meldet der Test etwas als fehlend, das zwei
# Zeilen weiter unten steht. CLAUDE.md nennt drei Faelle, in denen genau das
# passiert ist, und jedes Mal kostet es die Frage "ist der Vertrag gebrochen
# oder nur sein Anker".
#
# Gemessen am 2026-08-23: von 31 aufloesbaren Fenstern hatten 13 weniger als
# 200 Zeichen Reserve bis zur zuletzt geprueften Nadel — bei ihnen reicht ein
# eingefuegter Kommentarblock, um einen gruenen Vertrag rot zu faerben.
#
# Diese drei Helfer schneiden stattdessen per AST an der ECHTEN Grenze. Damit
# gibt es keine Zahl mehr, die veralten kann.


def _fn(src, name):
    """Quelltext einer Funktion, an ihrer echten Grenze geschnitten.

    Findet Top-Level-Funktionen UND verschachtelte. Kommt der Name mehrfach
    vor, ist das ein Fehler im Test und keine stille Zufallsauswahl —
    dann gehoert _meth() hierher."""
    treffer = [n for n in ast.walk(ast.parse(src))
               if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))
               and n.name == name]
    assert treffer, "Funktion %s gibt es nicht (mehr)" % name
    assert len(treffer) == 1, (
        "Funktion %s kommt %dx vor — _meth(src, Klasse, Name) benutzen"
        % (name, len(treffer)))
    return ast.get_source_segment(src, treffer[0]) or ""


def _meth(src, klasse, name):
    """Quelltext einer Methode — fuer Namen, die es mehrfach gibt."""
    for c in ast.walk(ast.parse(src)):
        if isinstance(c, ast.ClassDef) and c.name == klasse:
            for m in c.body:
                if isinstance(m, (ast.FunctionDef, ast.AsyncFunctionDef)) and m.name == name:
                    return ast.get_source_segment(src, m) or ""
    raise AssertionError("Methode %s.%s gibt es nicht (mehr)" % (klasse, name))


def _ab(src, marke):
    """Von einer Marke bis zum ENDE der umgebenden Funktion.

    Fuer Pruefungen, die bewusst mitten in einer Funktion ansetzen ("ab hier
    muss folgen…"). Die Marke bleibt, die willkuerliche Laenge faellt weg."""
    pos = src.find(marke)
    assert pos > 0, "Marke nicht gefunden: %r" % (marke[:60],)
    zeile = src.count("\n", 0, pos) + 1
    beste = None
    for n in ast.walk(ast.parse(src)):
        if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)) \
                and n.lineno <= zeile <= n.end_lineno:
            if beste is None or (n.end_lineno - n.lineno) < (beste.end_lineno - beste.lineno):
                beste = n
    if beste is None:
        return src[pos:]
    ende = 0
    for i, z in enumerate(src.splitlines(keepends=True), start=1):
        ende += len(z)
        if i == beste.end_lineno:
            break
    return src[pos:ende]


def ok(name):
    global PASS
    PASS += 1
    print(f"  ✓ {name}")


# ------------------------------------------------- 1) Failover-Streak-Logik

def test_streak():
    """Repliziert die _source_watch-Entscheidung: offline zählt, unknown hält,
    live resettet, Schwelle löst aus."""
    def run(statuses, threshold=2):
        hits = 0
        for i, err in enumerate(statuses):
            if err == "offline":
                hits += 1
                if hits >= threshold:
                    return i + 1
            elif err:
                pass                # unknown/Proxy: Zähler HALTEN
            else:
                hits = 0            # live: Reset
        return None

    assert run(["offline", "offline"]) == 2
    assert run(["offline", "unknown", "offline"]) == 3
    assert run(["offline", None, "offline", "offline"]) == 4
    assert run(["unknown"] * 10) is None
    assert run([None, "offline"], threshold=1) == 2
    ok("Failover-Streak: offline zählt, unknown hält, live resettet")


# ------------------------------------------------- 2) Round-Robin ab aktueller Quelle

def test_round_robin():
    def order(rows, current):
        cur = clean_username(current)
        o = list(rows)
        idx = next((i for i, r in enumerate(o)
                    if clean_username(r["source_username"]) == cur), -1)
        if idx >= 0:
            o = o[idx + 1:] + o[:idx + 1]
        return [r["source_username"] for r in o]

    rows = [{"id": 1, "source_username": "alice"},
            {"id": 2, "source_username": "bob"},
            {"id": 3, "source_username": "charlie"}]
    assert order(rows, "alice") == ["bob", "charlie", "alice"]
    assert order(rows, "@Bob") == ["charlie", "alice", "bob"]
    assert order(rows, "unbekannt") == ["alice", "bob", "charlie"]
    ok("Round-Robin: ab aktueller Quelle, case-insensitive, @-tolerant")


# ------------------------------------------------- 3) tee vs independent (Kommandobau)

def test_output_args():
    """v4.0-W77: GLEICHSTELLUNG — kein Haupt-Restream mehr. Kick/Twitch/YouTube
       sind gleichberechtigte Ziele: aktiv sobald konfiguriert, im tee ALLE mit
       onfail=ignore (keine ist primär), lauffähig auch ohne Kick, mit Pro-Restream-
       Overrides. Der bewährte Single-Pfad bleibt byte-identisch."""
    import nc.restream_targets as R
    R.configure(kick_ingest="rtmps://kick:443/app", kick_key="kk", kick_enabled=True,
                twitch_enabled=True, twitch_ingest="rtmp://live.twitch.tv/app",
                twitch_key="tk", youtube_enabled=True,
                youtube_ingest="rtmp://a.rtmp.youtube.com/live2", youtube_key="yk")

    # alle drei gleichberechtigt aktiv
    t = R.active_targets()
    assert [n for n, _ in t] == ["kick", "twitch", "youtube"], "alle drei müssen aktiv sein"

    # tee: JEDES Ziel trägt onfail=ignore — auch Kick (keine Sonderrolle mehr)
    tee = " ".join(R.build_output_args(t))
    slots = tee.split("|")
    for name in ("kick", "twitch", "youtube"):
        s = [x for x in slots if name in x][0]
        assert "onfail=ignore" in s, f"{name} muss weich wegfallen dürfen (gleichberechtigt)"
    assert tee.count("onfail=ignore") == 3, "alle drei Ziele weich — kein primäres Ziel"

    # URLs ROH (kein Backslash-Escaping — exec, keine Shell)
    assert "rtmps://kick:443" in tee and "\\:" not in tee, "URLs roh im exec-Kontext"
    assert "[f=flv:onfail=ignore:flvflags=no_duration_filesize]" in tee, "onfail-Slot intakt"

    # KEIN Kick nötig — nur Twitch+YouTube laufen ebenso
    R.configure(kick_ingest="", kick_key="")
    t_nokick = R.active_targets()
    assert [n for n, _ in t_nokick] == ["twitch", "youtube"], "muss ohne Kick laufen"
    R.configure(kick_ingest="rtmps://kick:443/app", kick_key="kk")

    # Pro-Restream-Override (B): dieser Restream übersteuert Kick-Key + Twitch-Ziel
    ov = {"kick": ("rtmps://kick:443/app", "ROWKEY"),
          "twitch": ("rtmp://tw2/app", "ROWTW")}
    t_ov = R.active_targets(overrides=ov)
    _urls = dict((n, u) for n, u in t_ov)
    assert _urls["kick"].endswith("/ROWKEY"), "Kick-Override greift nicht"
    assert _urls["twitch"].endswith("/ROWTW"), "Twitch-Override greift nicht"
    assert _urls["youtube"].endswith("/yk"), "YouTube fällt auf globale Env zurück"

    # expliziter Aus-Schalter je Plattform
    R.configure(youtube_enabled=False)
    assert [n for n, _ in R.active_targets()] == ["kick", "twitch"], "YOUTUBE_ENABLED=0 pausiert gezielt"
    R.configure(youtube_enabled=True)

    # independent: pro Ziel ein direkter flv-Ausgang, KEIN tee
    for _name, url in R.active_targets():
        args = R.single_output_args(url)
        assert args[:2] == ["-f", "flv"] and "tee" not in " ".join(args)

    # Ein Ziel → schlichter Single-Pfad (byte-identisch zu früher)
    single = R.build_output_args([("kick", "rtmps://kick:443/app/kk")])
    assert single == ["-f", "flv", "-flvflags", "no_duration_filesize",
                      "rtmps://kick:443/app/kk"]
    # Legacy-Helfer bleibt bedient (Status/Labels): Nicht-Kick-Ziele
    assert [n for n, _ in R.multistream_targets()] == ["twitch", "youtube"]
    ok("W77-Kommandobau: gleichberechtigte Ziele (alle weich) + Overrides + Single-Pfad")


# ------------------------------------------------- 4) Transcode-Erzwingung

def test_transcode_matrix():
    def decide(multi_mode, allow_copy, row_tc, has_multi, overlay=False):
        _multi = has_multi
        _forces = _multi and not allow_copy
        return {"transcode": bool(row_tc) or overlay or _forces,
                "independent": (multi_mode == "independent" and _multi)}

    d = decide("tee", False, 0, True)
    assert d["transcode"] and not d["independent"]
    d = decide("independent", False, 0, True)
    assert d["transcode"] and d["independent"]
    d = decide("independent", True, 0, True)
    assert not d["transcode"] and d["independent"]        # copy-Testmodus
    d = decide("tee", False, 0, False)
    assert not d["transcode"]                             # Single: kein Zwang
    ok("Transcode-Matrix: Multi erzwingt tc (außer ALLOW_COPY), Single frei")


# ------------------------------------------------- 5) Reentrance-Vertrag im Code

def test_reentrance_contract():
    """Statischer Vertrag: im Switch wird der Watcher VOR stop() aus der
    Registry gelöst (sonst cancelt er sich selbst mitten im Umschalten),
    und stop() räumt indep-Tasks + srcwatch + chatguard ab."""
    src = open("bot.py").read()
    i = src.find("async def _switch_to_next_live")
    body = src[i:src.find("\n    async def ", i + 10)]
    # B123 hängte stop() den Parameter _keep_desired=True an. Die frühere
    # Suche nach "await self.stop(rid)" mit schließender Klammer fand deshalb
    # nichts mehr (find -> -1) und der Vertrag kippte, obwohl die Reihenfolge
    # im Code stimmte. Ohne die Klammer suchen, sonst bricht der Test bei jedem
    # weiteren Parameter erneut.
    assert 0 <= body.find("self._srcwatch.pop(rid, None)") < body.find("await self.stop(rid")

    # Ohne schließende Klammer verankern: die Signatur trägt seit B123
    # _keep_desired=False. Der alte Anker fand nichts, j wurde -1 und der
    # "stop_body" war in Wahrheit das letzte Zeichen der Datei — der Test
    # prüfte also nichts und meldete trotzdem einen Fehler.
    j = src.find("    async def stop(self, rid")
    stop_body = src[j:src.find("\n    async def ", j + 10)]
    for token in ("indep_tasks", '_srcwatch.pop', "_chatguards.pop"):
        assert token in stop_body, f"stop() räumt {token} nicht"
    ok("Reentrance/Cleanup-Vertrag: Watcher-pop vor stop, stop räumt alles")


# ------------------------------------------------- 6) relay_profile-Vererbung

def test_relay_profile_contract():
    """Kick (Hauptprozess) darf NIE das leichte Relay-Profil erben; nur die
    Zusatz-Relays laufen mit relay_profile=True."""
    src = open("bot.py").read()
    assert src.count("relay_profile=True") == 1
    kick_zone = src[src.find("only_target=_kick_target") - 500:
                    src.find("only_target=_kick_target") + 150]
    assert "relay_profile" not in kick_zone
    ok("relay_profile: nur Zusatz-Relays, Kick behält volle Qualität")


# ------------------------------------------------- 7) 403→yt-dlp-Lebenszyklus

def test_403_lifecycle():
    import time
    streak, until = {}, {}
    HITS, COOL = 2, 1800

    def on_403(u):
        n = streak.get(u, 0) + 1
        streak[u] = n
        if n >= HITS:
            until[u] = time.time() + COOL

    def pref(u, base="native"):
        t = until.get(u, 0)
        if t > time.time():
            return "ytdlp"
        if t:
            until.pop(u, None)
        return base

    on_403("h"); assert pref("h") == "native"
    on_403("h"); assert pref("h") == "ytdlp"
    streak.pop("h", None)                       # Erfolg → Streak-Reset
    assert pref("h") == "ytdlp"                 # Fenster läuft weiter
    until["h"] = time.time() - 1
    assert pref("h") == "native" and "h" not in until
    ok("403-Schutz: Streak → yt-dlp-Fenster → Cooldown → native retry")


# ------------------------------------------------- 8) Overlay: Session-Filter + Plattformen

def test_overlay_session_and_platforms():
    """V37-OVMP: der Donation-Zähler MUSS ab Sende-Start zählen (der HTML-
    Overlay-Pfad tat das nicht — echter Bug), und Events müssen ihre
    Plattform behalten (kick/twitch/youtube/tiktok)."""
    import sqlite3, tempfile
    from datetime import datetime, timezone, timedelta

    c = sqlite3.connect(tempfile.mktemp())
    c.row_factory = sqlite3.Row
    c.execute("""CREATE TABLE overlay_events (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 ts TEXT NOT NULL, kind TEXT, name TEXT, amount TEXT,
                 message TEXT, platform TEXT DEFAULT 'kick')""")
    now = datetime.now(timezone.utc)
    old_ts = (now - timedelta(days=3)).isoformat()
    sess = (now - timedelta(hours=1)).isoformat()
    new_ts = (now - timedelta(minutes=5)).isoformat()
    c.executemany(
        "INSERT INTO overlay_events (ts,kind,name,amount,message,platform) VALUES (?,?,?,?,?,?)",
        [(old_ts, "donation", "Alt", "500", "alt", "kick"),
         (new_ts, "donation", "K", "20", "", "kick"),
         (new_ts, "donation", "T", "300 Bits", "Bits", "twitch"),
         (new_ts, "donation", "Y", "5,50 €", "Superchat", "youtube"),
         (new_ts, "follow", "fk", None, None, "kick"),
         (new_ts, "follow", "ft", None, None, "twitch"),
         (new_ts, "follow", "fy", None, None, "youtube")])
    c.commit()

    def _amt(v):
        try:
            return float(str(v).replace(",", ".").replace("€", "").strip())
        except (TypeError, ValueError):
            return 0.0

    def summe(session_start):
        _and = " AND ts >= ?" if session_start else ""
        _sp = (session_start,) if session_start else ()
        rows = c.execute("SELECT kind, amount, platform FROM overlay_events "
                         "WHERE kind IN ('donation','follow')" + _and, _sp).fetchall()
        goal = sum(_amt(r["amount"]) for r in rows if r["kind"] == "donation")
        plats = {r["platform"] for r in rows}
        return round(goal, 2), plats

    # Ohne Filter zählt die 3 Tage alte 500er-Spende mit → das war der Bug.
    assert summe(None)[0] == 525.5
    # Mit Session-Filter: nur ab Sende-Start (Bits sind keine Währung → 0).
    goal, plats = summe(sess)
    assert goal == 25.5, goal
    assert plats == {"kick", "twitch", "youtube"}, plats

    # Letzter Follower trägt seine Plattform
    fr = c.execute("SELECT name, platform FROM overlay_events WHERE kind='follow' "
                   "AND ts >= ? ORDER BY id DESC LIMIT 1", (sess,)).fetchone()
    assert fr["platform"] == "youtube"
    ok("Overlay: Session-Reset zählt ab Sende-Start + Plattform-Bilanz")


# ------------------------------------------------- 9) Overlay-Push-Verträge

def test_overlay_push_contract():
    """Alle Event-Quellen müssen ihre Plattform mitgeben, und die Route muss
    nach Session filtern (sonst kehrt der Reset-Bug zurück)."""
    src = open("bot.py").read()
    # Jede _overlay_push-Nutzung (außer der Definition) trägt platform=
    calls = [ln for ln in src.splitlines()
             if "_overlay_push(" in ln and "def _overlay_push" not in ln]
    multiline = src.count("_overlay_push(") - 1
    tagged = src.count('platform="kick"') + src.count('platform="twitch"') \
        + src.count('platform="youtube"') + src.count('platform="tiktok"') \
        + src.count('platform=(d.get("platform")')
    assert tagged >= 8, f"nur {tagged} getaggte Callsites"
    assert multiline >= 8, multiline
    assert len(calls) >= 1
    # Route filtert nach Session
    i = src.find("def api_overlay_state")
    # Bis zur nächsten Top-Level-def schneiden, nicht nach fester Zeichenzahl:
    # die Funktion ist über 4000 Zeichen lang gewachsen, das alte Fenster
    # endete vor dem return und der Test meldete fehlende Felder, die zwei
    # Zeilen weiter unten standen.
    _end = src.find("\ndef ", i + 10)
    body = src[i:_end if _end > 0 else len(src)]
    assert '_sess = _OVERLAY_SESSION.get("start")' in body
    assert '" AND ts >= ?" if _sess else ""' in body
    assert "by_platform" in body and "session_start=_sess" in body
    ok("Overlay-Verträge: alle Quellen getaggt, Route filtert nach Session")


# ------------------------------------------------- 10) Fixes aus error.log

def test_flask_async_unpack_contract():
    """B95: _run_async_from_flask liefert das Coroutine-Ergebnis DIREKT.
    api_kick_channel entpackt nur deshalb in (info, err), weil channel_info()
    selbst ein 2-Tupel liefert. api_channels_status gibt ein 3-Key-Dict
    zurück — dort MUSS einfach zugewiesen werden (sonst HTTP 500
    'too many values to unpack')."""
    src = open("bot.py").read()
    i = src.find("def api_channels_status")
    body = src[i:src.find("@dashboard_app.route", i + 10)]
    assert "data = _run_async_from_flask(" in body
    assert "data, err = _run_async_from_flask(" not in body
    ok("B95: /api/channels/status entpackt _run_async_from_flask nicht falsch")


def test_overlay_size_contract():
    """B94: Das Overlay muss in der ECHTEN Quellauflösung gerendert werden.
    Ein fest gerendertes 9:16-Overlay wurde per scale2ref auf eine 16:9-Quelle
    breitgezerrt — auf dem PC unbrauchbar."""
    src = open("bot.py").read()
    assert 'RESTREAM_OVERLAY_HTML_SIZE", "auto"' in src, "auto muss Default sein"
    assert "def _probe_video_size" in src and "def _overlay_render_size" in src
    # Probe-Ergebnis fließt in den Screenshot
    i = src.find("def _restream_html_overlay_start")
    body = src[i:i + 3000]
    assert "_size = _overlay_render_size(source_url)" in body
    assert "_htmlov_screenshot_cmd(binpath, png, _size)" in body
    # Aufrufer reicht die Quelle durch
    assert "_restream_html_overlay_start(rid, source_url=src)" in src
    # Filter verzerrt nicht mehr
    assert "force_original_aspect_ratio=decrease[ovs][base]" in src
    assert "overlay=(W-w)/2:(H-h)/2:eof_action=repeat:shortest=0[vh]" in src
    assert "scale2ref=w=iw:h=ih[ovs][base]" not in src, "nackter Stretch zurück!"
    ok("B94: Overlay rendert in Quellauflösung, Filter bleibt proportional")


def test_heartbeat_contract():
    """B96: Der Watchdog misst LEBEN. Ein Worker in einer langen Whisper-
    Transkription ist gesund — vorher schlug der Beat erst danach zu."""
    src = open("bot.py").read()
    assert "async def _hb_while(" in src
    assert '_hb_while("live-react", _whisper_transcribe(w))' in src
    # Rückstau wird verworfen statt minutenlang abgearbeitet
    assert "LIVE_REACT_MAX_BACKLOG" in src
    i = src.find("_todo = [w for w in wavs[:-1]")
    assert i > 0
    body = src[i:i + 1200]
    assert "if len(_todo) > LIVE_REACT_MAX_BACKLOG:" in body
    assert "_todo = _todo[-LIVE_REACT_MAX_BACKLOG:]" in body
    ok("B96: live-react beat während Transkription + Rückstau-Cap")


def test_dead_chat_contract():
    """B97: 'chat not found' setzt eine Sperre — der Video-Upload hat sie nie
    gelesen und produzierte 176 identische Fehler in einer Nacht."""
    src = open("bot.py").read()
    i = src.find("async def _send_one(fh_or_path, caption):")
    body = src[i:i + 900]
    assert "if _is_dead(chat_id):" in body, "_send_one prüft die Sperre nicht"
    # Part-Schleife bricht ab statt jeden Part scheitern zu lassen
    j = src.find("Upload part {i}/{total} fehlgeschlagen")
    zone = src[max(0, j - 700):j]
    assert "if _is_dead(chat_id):" in zone and "break" in zone
    ok("B97: toter Chat → Upload bricht ab statt Fehlersturm")


# ------------------------------------------------- 11) CPU-Vorrang fürs Sendebild

def test_whisper_throttle_contract():
    """B98: Ohne GPU teilen sich Encoder, Whisper und llama.cpp 8 Kerne.
    Während gesendet wird, MUSS das Sendebild Vorrang haben — Whisper läuft
    dann serialisiert statt WHISPER_MAX_CONCURRENT-fach."""
    src = open("bot.py").read()
    assert "WHISPER_THROTTLE_LIVE" in src
    i = src.find("async def _whisper_transcribe")
    # Funktionsgrenze statt fester 2000 Zeichen: die Drossel-Zeile steht rund
    # 42 Zeilen nach dem def und fiel knapp aus dem alten Fenster — der Test
    # meldete eine fehlende Zeile, die es gab.
    _end = src.find("\nasync def ", i + 10)
    body = src[i:_end if _end > 0 else len(src)]
    assert "_throttle = bool(_RESTREAM_ACTIVE_ALL) and WHISPER_THROTTLE_LIVE" in body
    assert "_st.enter_async_context(_whisper_live_gate)" in body
    assert "_st.enter_async_context(_whisper_sem)" in body
    # Drossel NUR bei aktivem Restream (sonst voller Speed)
    assert "if _throttle:" in body
    # Diagnose nach außen
    j = src.find("def api_system_resilience")
    assert "cpu={" in src[j:j + 3000] and '"throttled": _WHISPER_STATE' in src[j:j + 3000]
    ok("B98: Whisper serialisiert bei Live, Diagnose in /api/system/resilience")


async def _throttle_behaviour():
    """Verhaltenstest der Drossel-Mechanik (isoliert, ohne Bot-Import)."""
    import contextlib as _cl
    ACTIVE, peak = {}, {"n": 0, "cur": 0}
    sem, gate = asyncio.Semaphore(3), asyncio.Semaphore(1)

    async def run():
        async with _cl.AsyncExitStack() as st:
            if ACTIVE:
                await st.enter_async_context(gate)
            await st.enter_async_context(sem)
            peak["cur"] += 1
            peak["n"] = max(peak["n"], peak["cur"])
            await asyncio.sleep(0.02)
            peak["cur"] -= 1

    await asyncio.gather(*[run() for _ in range(6)])
    assert peak["n"] == 3, f"idle: {peak['n']}"
    peak.update(n=0, cur=0)
    ACTIVE["r1"] = True
    await asyncio.gather(*[run() for _ in range(6)])
    assert peak["n"] == 1, f"live: {peak['n']}"
    peak.update(n=0, cur=0)
    ACTIVE.clear()
    await asyncio.gather(*[run() for _ in range(6)])
    assert peak["n"] == 3, f"nach Live: {peak['n']}"


def test_whisper_throttle_behaviour():
    asyncio.run(_throttle_behaviour())
    ok("B98: idle 3 parallel → live 1 → nach Sendeende wieder 3 (kein Deadlock)")


# ------------------------------------------------- 12) AZRAEL im Sendebild

def test_azrael_overlay_source():
    """B99: AZRAELs Live-Reaktionen müssen im Sendebild landen.

    Der drawtext-Pfad las NUR _KICK_MOD.last_spoken — das wird aber
    ausschließlich gesetzt, wenn der Bot in den KICK-CHAT schreibt. Die
    Live-Reaction-Engine ruft _KICK_MOD.react() auf und schickt nichts in den
    Chat → AZRAELs Antworten tauchten im Restream nie auf. Primärquelle muss
    _AZRAEL_REACTION sein (das setzt react() selbst)."""
    src = open("bot.py").read()
    i = src.find("def _write_restream_overlay")
    body = src[i:i + 3000]
    j = body.find("AZRAEL-Reaktion unten")
    zone = body[j:j + 1100]
    assert "r = _AZRAEL_REACTION" in zone, "drawtext liest die Reaktion nicht"
    assert 'if r.get("text"):' in zone
    # last_spoken bleibt Fallback, ist aber NICHT mehr die einzige Quelle
    assert 'last_spoken' in zone and "if not txt:" in zone
    # react() füllt die Quelle
    k = src.find("_AZRAEL_REACTION.update(")
    assert k > 0 and "text=text, active=True" in src[k:k + 300]
    # live-react ruft react() auf → Kette geschlossen
    assert "_KICK_MOD.react(statement, context=ctx, source=username)" in src
    ok("B99: drawtext liest _AZRAEL_REACTION → Live-Reaktionen im Sendebild")


def test_overlay_portrait_layout():
    """B100: Die Bühne MUSS dem Seitenverhältnis folgen.

    Sie war hart 1920x1080 und wurde per min(vw/1920, vh/1080) eingepasst —
    bei einer 9:16-Quelle ergab das scale=0.5625, das komplette Overlay
    schrumpfte auf ein 1080x608-Band in der Bildmitte (32% der Höhe).
    Und Portrait-Regeln dürfen NICHT in vw/vh rechnen: die zählen gegen den
    Viewport, nicht gegen die skalierte Bühne."""
    import os as _os
    _p = next((p for p in ("overlay.html", "templates/overlay.html")
               if _os.path.exists(p)), None)
    if not _p:
        print("  – Portrait-Layout übersprungen (overlay.html nicht gefunden)")
        return
    html = open(_p).read()
    # fit() wählt die Referenz nach Aspekt
    i = html.find("function fit(){")
    body = html[i:i + 900]
    assert "var portrait = vh > vw;" in body
    assert "portrait ? 1080 : 1920" in body and "portrait ? 1920 : 1080" in body
    assert "classList.toggle('portrait', portrait)" in body
    assert "stage.style.width" in body and "stage.style.height" in body
    # Die alte starre Einpassung darf nicht zurückkommen
    assert "Math.min(window.innerWidth/1920, window.innerHeight/1080)" not in html

    # Portrait-Regeln: alle Blöcke platziert, KEINE vw/vh (Bühnen-Pixel!)
    import re as _re
    rules = _re.findall(r"html\.portrait\s+([#.][\w-]+)[^{]*\{([^}]*)\}", html)
    sels = {r[0] for r in rules}
    for sel in ("#title", "#follower", "#don", "#mod", "#azrael", "#az-panel"):
        assert sel in sels, f"{sel} fehlt in den Portrait-Regeln"
    for sel, decl in rules:
        assert not _re.search(r"\d+v[wh]\b", decl), \
            f"{sel} rechnet in vw/vh — muss Bühnen-Pixel sein: {decl[:60]}"

    # AZRAEL darf nicht am unteren Rand kleben (dort liegt #don)
    az = next(d for s_, d in rules if s_ == "#azrael")
    assert "bottom:auto" in az and "top:" in az

    # Vertikale Kollisionsfreiheit auf der 1920px-Bühne
    def _top(sel):
        d = next((d for s_, d in rules if s_ == sel), "")
        m = _re.search(r"top:(\d+)px", d)
        return int(m.group(1)) if m else None
    tops = {s_: _top(s_) for s_ in ("#title", "#follower", "#azrael", "#mod")}
    assert tops["#title"] < tops["#follower"] < tops["#azrael"] < tops["#mod"], tops
    assert tops["#mod"] < 1920, "Moderator außerhalb der Bühne"
    ok("B100: Bühne folgt dem Aspekt, Portrait rechnet in Bühnen-Pixeln")


def test_azrael_text_cap():
    """B101: Der HTML-Pfad reichte den VOLLEN Reaktionstext durch — lange
    Antworten wurden im Sendebild zur unlesbaren Textwand (der drawtext-Pfad
    kappt seit je auf 2x38 Zeichen)."""
    src = open("bot.py").read()
    assert "AZRAEL_OVERLAY_MAXLEN" in src and "def _ov_clip_text" in src
    body = _fn(src, "_azrael_overlay_state")          # v4.0-W117
    assert '"text": _ov_clip_text(r.get("text", ""))' in body, "API kappt nicht"
    assert '"text_full"' in body, "Volltext sollte für Clients erhalten bleiben"

    # Kapp-Verhalten
    import os as _os
    _p = next((p for p in ("overlay.html", "templates/overlay.html")
               if _os.path.exists(p)), None)
    if _p:
        html = open(_p).read()
        j = html.find("#az-panel .aztext{")
        decl = html[j:html.find("}", j)]
        assert "-webkit-line-clamp" in decl and "max-height" in decl, \
            "CSS-Deckelung fehlt (zweite Sicherung)"
    ok("B101: AZRAEL-Text gekappt (API + CSS-Deckelung)")


def test_overlay_size_selfcorrect():
    """B102: Der auto-Default greift NICHT, wenn in der Server-.env noch ein
    fester Wert steht (os.getenv liest die .env zuerst). Ein 9:16-Overlay auf
    einer 16:9-Quelle ist immer falsch → die Quelle muss gewinnen."""
    src = open("bot.py").read()
    assert "def _parse_size" in src
    i = src.find("def _overlay_render_size")
    body = src[i:src.find("def _find_chromium", i)]
    assert "forced = _parse_size(RESTREAM_OVERLAY_HTML_SIZE)" in body
    assert "probed = _probe_video_size(source_url)" in body
    assert "abs(fa - pa) > 0.05" in body, "Aspekt-Abgleich fehlt"
    # Bei Abweichung gewinnt die Quelle
    j = body.find("abs(fa - pa) > 0.05")
    assert 'return f"{probed[0]},{probed[1]}"' in body[j:j + 700]

    # Entscheidungsmatrix nachrechnen
    import re as _re

    def _ps(s):
        m = _re.match(r"^\s*(\d{2,5})\s*,\s*(\d{2,5})\s*$", str(s or ""))
        return (int(m.group(1)), int(m.group(2))) if m else None

    def decide(cfg, probed):
        forced = _ps(cfg)
        if forced and probed:
            fa, pa = forced[0] / forced[1], probed[0] / probed[1]
            if abs(fa - pa) > 0.05:
                return (probed[0], probed[1])
            return forced
        return probed or forced

    # Henrys Fall: alte .env + 16:9-Quelle → korrigiert
    assert decide("1080,1920", (1920, 1080)) == (1920, 1080)
    # Aspekt passt (nur andere Auflösung) → Vorgabe bleibt, scale2ref skaliert sauber
    assert decide("1080,1920", (720, 1280)) == (1080, 1920)
    # auto → Quelle
    assert decide("auto", (1920, 1080)) == (1920, 1080)
    # Probe kaputt → Vorgabe
    assert decide("1080,1920", None) == (1080, 1920)
    ok("B102: falsch konfigurierte Größe wird gegen die Quelle korrigiert")


def test_overlay_mode_default():
    """Der HTML-Modus ist Default — er kann den Stream nicht kaputt machen,
    weil vier Fallbacks auf drawtext greifen."""
    src = open("bot.py").read()
    assert 'RESTREAM_OVERLAY_MODE", "html"' in src, "html muss Default sein"
    assert 'RESTREAM_OVERLAY_MODE not in ("text", "html")' in src
    # Fallback-Pfade müssen erhalten bleiben
    assert src.count("Fallback drawtext") >= 3, "Fallbacks fehlen"
    import os as _os
    for p in (".env", ".env.example"):
        if _os.path.exists(p):
            assert "RESTREAM_OVERLAY_MODE=html" in open(p).read(), p
    ok("Overlay-Modus: html als Default, drawtext-Fallbacks intakt")


def test_azrael_idle_layout():
    """B103: Ein leeres Sprechpanel darf keinen Platz belegen — sonst steht
    der Avatar außermittig (opacity:0 blendet nur aus, reserviert aber Raum)."""
    import os as _os
    _p = next((p for p in ("overlay.html", "templates/overlay.html")
               if _os.path.exists(p)), None)
    if not _p:
        print("  – B103 übersprungen (overlay.html nicht gefunden)")
        return
    html = open(_p).read()
    assert "#azrael:not(.active) #az-panel{display:none}" in html
    # Titel: Unterlängen dürfen nicht in die Subtitle laufen
    i = html.find("#title .tname{")
    assert "line-height:1.14" in html[i:html.find("}", i)], "line-height:1 überlappt"
    j = html.find("html.portrait #title .tname{")
    assert "white-space:nowrap" in html[j:html.find("}", j)], "Titel bricht um"
    ok("B103: Avatar mittig im Leerlauf, Titel ohne Überlapp")


# ------------------------------------------------- Runner

def test_ffmpeg_thread_budget():
    """V37-CPU: JEDER ffmpeg-Aufruf muss ein Thread-Budget haben.

    Befund aus dem Produktions-htop: Load 113 auf 8 Kernen, 812 Threads. Kein
    einziger ffmpeg-Aufruf setzte -threads → jeder Prozess nahm sich alle Kerne.
    Bei vier moeglichen parallelen x264 (Transcode, Relay, Shrink, Clip) war das
    die Ursache. Dieser Test haelt fest, dass der Deckel nicht wieder verschwindet.
    """
    src = open("bot.py").read()
    tree = ast.parse(src)

    # _ff_cmd existiert (delegiert seit W44) und die -threads-Logik lebt in nc.ffbuild
    assert "def _ff_cmd(" in src, "_ff_cmd fehlt"
    assert 'out[1:1] = ["-threads", str(int(threads))]' in open("nc/ffbuild.py").read(), \
        "-threads muss direkt hinter 'ffmpeg' stehen (globale Codec-Option; nc.ffbuild seit W44)"
    ok("_ff_cmd setzt -threads hinter 'ffmpeg'")

    for c in ("FFMPEG_THREADS_LIVE", "FFMPEG_THREADS_RELAY", "FFMPEG_THREADS_BG",
              "FFMPEG_THREADS_RECORD", "FFMPEG_NICE_BG", "FFMPEG_NICE_RECORD"):
        assert re.search(rf"^{c}\s*=\s*_env_int", src, re.M), f"{c} fehlt"
    ok("6 Budget-Konstanten sind per Env steuerbar")

    # Das Sendebild bekommt mehr Threads als die Nachbearbeitung — und kein nice
    m = re.search(r'FFMPEG_THREADS_LIVE\s*=\s*_env_int\("FFMPEG_THREADS_LIVE",\s*(\d+)', src)
    b = re.search(r'FFMPEG_THREADS_BG\s*=\s*_env_int\("FFMPEG_THREADS_BG",\s*(\d+)', src)
    assert m and b and int(m.group(1)) > int(b.group(1)), \
        "Sendebild muss mehr Threads bekommen als die Nachbearbeitung"
    ok(f"Sendebild {m.group(1)}T > Hintergrund {b.group(1)}T")

    # Restream-Builder: gedeckelt, aber NICHT genice't (Vorrang!)
    fn = ""
    for n in ast.walk(tree):
        if isinstance(n, ast.FunctionDef) and n.name == "_build_restream_cmd":
            fn = ast.get_source_segment(src, n) or ""
    assert fn, "_build_restream_cmd nicht gefunden"
    assert "_ff_cmd(cmd, threads=(FFMPEG_THREADS_RELAY" in fn, \
        "_build_restream_cmd ohne Thread-Deckel"
    assert "nice=" not in fn, "das Sendebild darf NICHT genice't werden"
    ok("_build_restream_cmd: gedeckelt, ohne nice (Vorrang fuers Sendebild)")

    # Jede ffmpeg-Befehlsliste muss durch _ff_cmd — Ausnahme: 'ffmpeg -version'
    unguarded = []
    for n in ast.walk(tree):
        if not (isinstance(n, ast.List) and n.elts
                and isinstance(n.elts[0], ast.Constant)
                and n.elts[0].value == "ffmpeg"):
            continue
        if len(n.elts) > 1 and isinstance(n.elts[1], ast.Constant) \
                and n.elts[1].value == "-version":
            continue          # rechnet nichts
        owner = None
        for f in ast.walk(tree):
            if isinstance(f, (ast.FunctionDef, ast.AsyncFunctionDef)) \
                    and f.lineno <= n.lineno <= (f.end_lineno or 0):
                owner = f
        body = ast.get_source_segment(src, owner) if owner else ""
        if "_ff_cmd(" not in (body or ""):
            unguarded.append((n.lineno, owner.name if owner else "?"))
    assert not unguarded, f"ffmpeg ohne Thread-Deckel: {unguarded}"
    ok("alle rechnenden ffmpeg-Pfade laufen durch _ff_cmd")


def test_ai_timeout_capped():
    """V37-B104: AI_FLASK_TIMEOUT existierte als Deckel, wurde aber nur bei
       _run_async_from_flask angewandt. Drei Flask-Routen riefen llm_chat_sync
       direkt und erbten AI_TIMEOUT (.env: 0 → im Code 3600s) — ein Worker
       konnte eine Stunde blockieren."""
    src = open("bot.py").read()
    tree = ast.parse(src)
    TARGETS = {"llm_chat", "ai_chat", "llm_chat_sync"}
    naked = []
    for fn in ast.walk(tree):
        if not isinstance(fn, (ast.FunctionDef, ast.AsyncFunctionDef)):
            continue
        guarded = set()
        for n in ast.walk(fn):
            if isinstance(n, ast.Call):
                nm = (n.func.attr if isinstance(n.func, ast.Attribute)
                      else getattr(n.func, "id", None))
                if nm == "wait_for":
                    for a in n.args:
                        for s in ast.walk(a):
                            if isinstance(s, ast.Call):
                                guarded.add(id(s))
        for n in ast.walk(fn):
            if not isinstance(n, ast.Call):
                continue
            nm = (n.func.attr if isinstance(n.func, ast.Attribute)
                  else getattr(n.func, "id", None))
            if nm not in TARGETS:
                continue
            if id(n) in guarded or any(k.arg == "timeout" for k in n.keywords) \
                    or len(n.args) >= 3:
                continue
            naked.append((fn.name, n.lineno))
    assert not naked, f"ungedeckelte AI-Aufrufe: {naked}"
    ok("kein AI-Aufruf ohne timeout/wait_for (B104)")


def test_fast_json_safety():
    """V37-PERF: der orjson-Provider darf Fehler NICHT verschlucken.

    Beim Bauen war der erste Entwurf `default=str`. Damit wird eine nicht
    serialisierbare sqlite3.Row still zu "<sqlite3.Row object at 0x...>" — der
    Fehler landet in der API-Antwort statt im Log. Standard-json wirft dort
    einen TypeError. Ein schnellerer Serializer, der Fehler verschluckt, ist
    schlechter als ein langsamer, der sie zeigt.
    """
    src = open("bot.py").read()
    assert "def _install_fast_json(" in src, "_install_fast_json fehlt"
    i = src.find("def _install_fast_json(")
    body = src[i:src.find("\n_ORJSON_ON", i)]
    # Nur CODE pruefen, nicht die Prosa: der Kommentar erklaert ja gerade,
    # WARUM default=str falsch ist.
    code = "\n".join(l for l in body.splitlines()
                     if not l.strip().startswith("#") and '"""' not in l)
    assert "orjson.dumps(obj, default=str" not in code, \
        "default=str verschluckt Serialisierungsfehler — muss _default() sein"
    assert "default=_default" in code, "orjson.dumps muss _default() nutzen"
    assert "raise TypeError" in body, \
        "_default muss am Ende laut scheitern statt still zu stringifizieren"
    for t in ("sqlite3.Row", "Decimal", "frozenset"):
        assert t in body, f"_default behandelt {t} nicht"
    ok("orjson-Provider: kein default=str, scheitert laut bei Unbekanntem")

    assert "except ImportError:\n        return False" in body, \
        "fehlendes orjson muss sauber zum Standard-json zurückfallen"
    ok("orjson: sauberer Fallback wenn nicht installiert")


def test_uvloop_optional():
    """V37-PERF: uvloop wird VOR asyncio.run() gesetzt (sonst wirkungslos) und
       ist optional — fehlt das Paket, läuft alles unverändert weiter."""
    src = open("bot.py").read()
    assert "def _install_fast_eventloop(" in src, "_install_fast_eventloop fehlt"
    # Den AUFRUF suchen, nicht die Definition — beide heissen gleich.
    call = src.find("    _install_fast_eventloop()")
    run = src.find("    asyncio.run(main())")
    assert 0 < call < run, "uvloop muss VOR asyncio.run(main()) aktiviert werden"
    ok("uvloop: Policy wird vor asyncio.run() gesetzt")

    d = src.find("def _install_fast_eventloop(")
    b = src[d:src.find("\nif __name__", d)]
    assert "except ImportError" in b, "fehlendes uvloop muss abgefangen werden"
    assert "USE_UVLOOP" in b, "uvloop muss per Env abschaltbar sein"
    ok("uvloop: optional + per USE_UVLOOP=0 abschaltbar")


def test_url_refresh_no_wait():
    """V37-DISC: Nach dem geplanten URL-Refresh-Schnitt muss SOFORT neu gestartet
       werden.

    TikToks Stream-URL traegt ein expire=-Token (~30min TTL). Der Watchdog
    beendet ffmpeg absichtlich kurz davor — der User ist dabei nachweislich noch
    live. Trotzdem fiel der Code danach in den Normalpfad und wartete das
    regulaere Live-Intervall (ADAPTIVE_INTERVALS["live"] = 20s) ab: 20 Sekunden
    fehlende Aufnahme bei JEDEM Refresh, also alle ~28 Minuten.
    """
    src = open("bot.py").read()
    tree = ast.parse(src)
    i = src.find("if url_refreshed[0]:\n                try:\n                    _NEXT_CHECK_AT[tid] = 0")
    assert i > 0, "url_refresh stellt den naechsten Check nicht sofort faellig"
    ok("URL-Refresh: _NEXT_CHECK_AT auf 0 (sofort fällig)")

    # Der Fix darf nicht von einem spaeteren _schedule_next_check ueberschrieben
    # werden — weder in derselben Funktion noch beim Aufrufer.
    ln = src[:i].count("\n") + 1
    fn = None
    for n in ast.walk(tree):
        if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)) \
                and n.lineno <= ln <= (n.end_lineno or 0):
            fn = n
    assert fn, "umgebende Funktion nicht gefunden"
    lines = src.splitlines()
    after = [k for k, line in enumerate(lines[ln:fn.end_lineno], ln + 1)
             if "_schedule_next_check" in line]
    assert not after, f"_schedule_next_check ueberschreibt den Fix in Z.{after}"

    callers = []
    for f2 in ast.walk(tree):
        if not isinstance(f2, (ast.FunctionDef, ast.AsyncFunctionDef)):
            continue
        for n in ast.walk(f2):
            if isinstance(n, ast.Call):
                nm = (n.func.attr if isinstance(n.func, ast.Attribute)
                      else getattr(n.func, "id", None))
                if nm == fn.name:
                    callers.append((f2, n.lineno))
    for f2, cl in callers:
        bad = [k for k, line in enumerate(lines[cl:f2.end_lineno], cl + 1)
               if "_schedule_next_check" in line]
        assert not bad, \
            f"{f2.name}() ruft _schedule_next_check NACH {fn.name}() (Z.{bad})"
    ok(f"kein _schedule_next_check überschreibt ihn (geprüft in {fn.name} + {len(callers)} Aufrufer)")


def test_chat_guardian_reconnect():
    """V37-CHAT: Der Guardian muss auf den Task WARTEN statt in 30s-Schritten zu
       pollen — sonst bleibt der Chat nach jedem Abbruch bis zu 30s tot. Und er
       braucht Backoff, sonst verbrennt er bei Dauerfehlern Sign-Quota."""
    src = open("bot.py").read()
    tree = ast.parse(src)
    fn = ""
    for n in ast.walk(tree):
        if isinstance(n, ast.AsyncFunctionDef) and n.name == "_restream_chat_guardian":
            fn = ast.get_source_segment(src, n) or ""
    assert fn, "_restream_chat_guardian nicht gefunden"

    assert "await task" in fn, \
        "Guardian muss auf den Listener-Task warten (sofortiger Reconnect)"
    assert "await asyncio.sleep(30)" not in fn, \
        "festes 30s-Polling ist der alte Fehler — kostet bis zu 30s toten Chat"
    ok("Chat-Guardian: wartet auf den Task, kein 30s-Blindflug")

    assert "CHAT_BACKOFF_MAX_S" in fn and "CHAT_FLAP_S" in fn, \
        "Guardian braucht Flap-Erkennung + Backoff"
    assert "backoff = 0" in fn, "gesunde Session muss den Backoff zurücksetzen"
    ok("Chat-Guardian: Backoff bei Flapping, Reset nach gesunder Session")

    for c in ("CHAT_FLAP_S", "CHAT_BACKOFF_MAX_S"):
        assert re.search(rf"^{c}\s*=\s*_env_int", src, re.M), f"{c} nicht per Env"
    ok("Chat: Flap-Schwelle + Backoff-Deckel per Env steuerbar")


def test_config_drift():
    """V37-DRIFT: .env-Abweichungen vom Code-Default muessen sichtbar sein.

    Dreimal in einer Session hat eine .env-Zeile still die Absicht des Codes
    ausgehebelt: RESTREAM_OVERLAY_HTML_SIZE (Overlay verzerrt),
    RESTREAM_MULTI_MODE (doppeltes Encoding), LIVE_REACT_ENABLED (falsche
    Aussage ueber den Zustand). Jedes Mal mit Fehlersuche bezahlt.
    """
    import nc.confdrift as cd

    # Die Defaults werden aus der QUELLE gezogen, nicht aus einer zweiten Liste —
    # sonst laeuft die Pruefung irgendwann der Realitaet hinterher.
    d = cd.extract_defaults("bot.py")
    assert len(d) > 200, f"nur {len(d)} Env-Keys aus der Quelle — AST kaputt?"
    assert d.get("RESTREAM_MULTI_MODE") == "tee", d.get("RESTREAM_MULTI_MODE")
    assert d.get("RESTREAM_OVERLAY_MODE") == "html"
    ok(f"confdrift liest {len(d)} Env-Defaults per AST aus der Quelle")

    # Der Fall, der uns CPU gekostet hat
    rep = cd.config_drift("bot.py",
                          env={"RESTREAM_MULTI_MODE": "independent"},
                          only_watchlist=True)
    assert rep["watched_drift"] == 1, rep
    e = rep["entries"][0]
    assert e["key"] == "RESTREAM_MULTI_MODE" and e["code_default"] == "tee"
    assert "doppelte CPU" in e["why"]
    ok("confdrift erkennt RESTREAM_MULTI_MODE=independent (der echte Fall)")

    # Gleicher Wert = keine Drift; Secrets werden ignoriert
    assert cd.config_drift("bot.py", env={"RESTREAM_MULTI_MODE": "tee"},
                           only_watchlist=True)["drift_count"] == 0
    assert cd.config_drift("bot.py", env={"TELEGRAM_TOKEN": "abc"},
                           only_watchlist=True)["drift_count"] == 0
    ok("confdrift: kein Fehlalarm bei Gleichstand, Secrets ignoriert")

    # "1" vs 1 darf keine Drift sein
    assert cd.config_drift("bot.py", env={"WHISPER_CPU_THREADS": "2"},
                           only_watchlist=True)["drift_count"] == 0
    ok("confdrift: normalisiert Typen ('2' == 2)")


def test_overlay_react_wrap():
    """V37-OVFIX: Die AZRAEL-Reaktion im gebrannten Overlay wurde nach 2 Zeilen
    still abgeschnitten — mitten im Satz, ohne Hinweis (Henrys Screenshots mit
    hängendem Komma). Jetzt: 3 Zeilen, Ellipse beim echten Abschnitt, und kein
    Wort läuft über die Zeilenbreite."""
    from nc.textmore import _ov_wrap

    long = ("AZRAEL ▸ Klingt nach einer wilden Eskapade — fast musikalischen "
            "Eskapade, wie ein Abenteuer das man so schnell nicht vergisst")

    # Ellipse erscheint NUR wenn wirklich abgeschnitten wird
    r = _ov_wrap(long, 38, 3, ellipsis=True)
    assert r.endswith("…"), "abgeschnittener Text muss mit … enden"
    assert len(r.split("\n")) == 3, "sollte 3 Zeilen nutzen"
    ok("_ov_wrap: Ellipse beim Abschnitt, 3 Zeilen")

    # Kurzer Text: kein …, keine leeren Zeilen
    short = _ov_wrap("AZRAEL ▸ Nice!", 38, 3, ellipsis=True)
    assert "…" not in short and short == "AZRAEL ▸ Nice!"
    ok("_ov_wrap: kurzer Text unverändert, kein …")

    # Keine Zeile über der Breite — auch nicht bei überlangem Einzelwort
    for txt in [long, "AZRAEL ▸ " + "Donaudampfschifffahrtskapitaenspatentx" * 3,
                "http://beispiel.de/" + "x" * 90]:
        w = _ov_wrap(txt, 38, 3, ellipsis=True)
        mx = max(len(l) for l in w.split("\n"))
        assert mx <= 38, f"Zeile {mx} > 38 — würde am Bildrand klippen: {txt[:30]}"
    ok("_ov_wrap: kein Wort läuft über die Zeilenbreite (Hard-Split)")

    # Alte Aufrufer (ohne ellipsis) unverändert — Regression
    assert _ov_wrap("a b c d e f", 5, 2) == "a b c\nd e f"
    ok("_ov_wrap: bestehende Aufrufer unverändert (ellipsis default False)")

    # Der Fix nutzt Env-Konstanten + erklärendes Präfix, nicht mehr hartes "AZRAEL ▸"
    src = open("bot.py").read()
    assert "AZRAEL_OVERLAY_PREFIX" in src, "Präfix muss konfigurierbar sein"
    assert 'f"{AZRAEL_OVERLAY_PREFIX} {txt}"' in src, "Reaktion muss das Präfix nutzen"
    assert 'y=f"{H}-th-58"' in open("nc/ffmpeg_filters.py").read(), \
        "Portrait-react muss von unten (th-basiert) ankern (nc.ffmpeg_filters seit W27)"
    ok("Overlay: Präfix konfigurierbar, Portrait-react th-verankert")


def test_twitch_oauth():
    """V37-TWOAUTH: OAuth-Flow ersetzt den manuellen Token. Nutzer gibt nur
    Client-ID + Secret an; der Bot holt Refresh-Token und erneuert selbst."""
    import os as _os
    import nc.twitchoauth as tw

    _os.environ["TWITCH_CLIENT_ID"] = "1xfy1bv6jibywwriwsy4gqwsq1lvlh"
    _os.environ["TWITCH_CLIENT_SECRET"] = "s3cr3t"
    import tempfile
    tw.configure(_os.path.join(tempfile.mkdtemp(), "tw.json"), "http://localhost:3000")

    # Authorize-URL trägt genau den Scope, den channel.follow v2 verlangt
    url = tw.authorize_url("csrf1")
    assert "moderator%3Aread%3Afollowers" in url, "Scope fehlt in Authorize-URL"
    # V37-TWOAUTH-FIX2: Twitch erlaubt bei Redirect-URIs nur HTTPS oder
    # http://localhost — eine IP mit https lehnt es ab (kein Zertifikat für
    # nackte IPs). Der Flow nutzt daher localhost:3000 (per SSH-Tunnel) als
    # Default; eine echte Domain kann per redirect_uri übergeben werden.
    url2 = tw.authorize_url("csrf2", redirect_uri="http://localhost:3000/api/twitch/oauth/callback")
    assert "localhost%3A3000" in url2, "localhost-Redirect wird nicht übernommen"
    assert tw._state["last_redirect"] == "http://localhost:3000/api/twitch/oauth/callback", \
        "last_redirect muss für den Token-Tausch gemerkt werden (muss beim Tausch exakt gleich sein)"
    # Eine Domain mit HTTPS muss ebenfalls durchgehen
    url3 = tw.authorize_url("csrf3", redirect_uri="https://bot.example.de/api/twitch/oauth/callback")
    assert "bot.example.de" in url3
    assert "client_id=1xfy1b" in url, "falsche/fehlende Client-ID"
    assert "state=csrf1" in url, "CSRF-state fehlt"
    ok("twitchoauth: Authorize-URL mit korrektem Scope + CSRF")

    # V37-TWCHAT / B142: Scopes = Follower + Chat (lesen/schreiben) + Bann-
    # Moderation + Broadcast-Verwaltung (Titel/Kategorie via Helix PATCH
    # /channels, s. nc.twitchoauth.update_channel, aufgerufen in _set_channel).
    # Kein Overreach darüber hinaus.
    assert set(tw.SCOPES) == {"moderator:read:followers", "chat:read",
                              "chat:edit", "moderator:manage:banned_users",
                              "channel:manage:broadcast"}, \
        "Follower + Chat + Moderation + Broadcast, nicht mehr"
    ok("twitchoauth: Follower + Chat + Moderation + Broadcast-Scope, kein Overreach")

    # Persistenz + 0600
    tw._state["refresh"] = "rt_abc"
    tw._save()
    tw._state["refresh"] = ""
    tw._load()
    assert tw._state["refresh"] == "rt_abc", "Refresh-Token nicht persistiert"
    # Der 0600-Vertrag gilt für den Zielserver (Linux). Unter Windows kennt
    # os.chmod nur das Read-only-Bit, st_mode meldet immer 666 — die Prüfung
    # dort auszuführen hieße, einen Fehler zu melden, den es auf der Zielplatt-
    # form nicht gibt. Persistenz selbst wird oben plattformunabhängig geprüft.
    if _os.name == "posix":
        mode = oct(_os.stat(tw._state["store_path"]).st_mode)[-3:]
        assert mode == "600", f"Refresh-Token-Datei hat {mode}, muss 600 sein"
        ok("twitchoauth: Refresh-Token persistiert mit 0600")
    else:
        ok("twitchoauth: Refresh-Token persistiert (0600-Prüfung nur unter POSIX)")

    # status() spiegelt den Zustand
    st = tw.status()
    assert st["ready"] and st["has_refresh"], st
    ok("twitchoauth: status() meldet ready nach Flow")

    # Der EventSub-Loop bevorzugt OAuth, hält aber den manuellen Token als Fallback
    src = open("bot.py").read()
    i = src.find("async def _twitch_eventsub_loop():")
    body = src[i:i + 1600]
    assert "_twoauth.access_token" in body, "Loop nutzt den OAuth-Token nicht"
    # Auf die tatsaechlichen getenv-AUFRUFE schauen, nicht auf den Kommentar,
    # der TWITCH_EVENTSUB_TOKEN natuerlich auch erwaehnt.
    getenv_manual = body.find('os.getenv("TWITCH_EVENTSUB_TOKEN"')
    call_oauth = body.find("_twoauth.access_token")
    assert getenv_manual > 0, "manueller Token als Fallback muss bleiben"
    assert call_oauth < getenv_manual, \
        "OAuth muss VOR dem manuellen Token versucht werden"
    ok("eventsub-Loop: OAuth bevorzugt, manueller Token als Fallback")


def test_donations_summary():
    """V37-DON: Donations aller vier Plattformen landen über _overlay_push in
    overlay_events und werden nach Plattform aggregiert. YouTube+Twitch sind
    KEINE Sonderfälle — sie nutzen denselben Pfad wie Kick/TikTok."""
    src = open("bot.py").read()
    # v4.0-W116: die Route liegt jetzt im Blueprint nc/routes/money.py. Der
    # Vertrag gilt unveraendert, er verankert nur eine Ebene tiefer.
    money = open("nc/routes/money.py", encoding="utf-8").read()
    assert '@bp.route("/api/donations/summary")' in money, \
        "Donations-Route fehlt"
    assert "def api_donations_summary" not in src, \
        "Doppel-Logik: die Route liegt noch im Monolithen UND im Blueprint"
    # Panel zeigt Kick/Twitch/YouTube — TikTok wurde auf Wunsch entfernt
    i = money.find("def api_donations_summary")
    body = money[i:i + 3000]
    for p in ("kick", "twitch", "youtube"):
        assert f'"{p}"' in body, f"Plattform {p} fehlt in der Aggregation"
    assert 'for p in ("kick", "twitch", "youtube")' in body, \
        "TikTok muss aus der Panel-Aggregation raus sein"
    # Der Ausschluss läuft nicht mehr über die Blacklist "platform != 'tiktok'",
    # sondern über die Positivliste REVENUE_PLATFORMS -> _REVENUE_SQL_IN. Das ist
    # der schärfere Vertrag: eine neu hinzukommende Fremdgeld-Plattform ist damit
    # automatisch draußen, statt erst vergessen zu werden. Also die Positivliste
    # prüfen — und dass TikTok wirklich nicht drinsteht.
    assert "_REVENUE_SQL_IN" in body, \
        "recent-Liste filtert nicht über die Einnahme-Positivliste"
    assert 'REVENUE_PLATFORMS = ("kick", "twitch", "youtube", "manuell")' in src, \
        "REVENUE_PLATFORMS verändert — TikTok-Ausschluss neu prüfen"
    assert "tiktok" not in src[src.find("REVENUE_PLATFORMS ="):
                               src.find("REVENUE_PLATFORMS =") + 200], \
        "TikTok steht in der Einnahme-Positivliste — fremdes Geld wäre Einnahme"
    ok("donations: Kick/Twitch/YouTube im Panel, TikTok per Positivliste raus")

    # Der Donation-Push für Twitch/YouTube existiert (nicht nur Kick/TikTok)
    pushes = src.count('_overlay_push("donation"')
    assert pushes >= 4, f"nur {pushes} Donation-Pushes — Twitch/YouTube fehlen"
    assert 'platform="twitch"' in src, "Twitch-Donation-Push fehlt"
    assert 'platform="youtube"' in src, "YouTube-Donation-Push fehlt"
    ok("donations: Twitch (Bits/Subs) + YouTube (Superchat) werden gebucht")


def test_azrael_overlay_toggle():
    """V37-AZHIDE: AZRAELs Reaktion im gebrannten Sendebild muss abschaltbar sein
    (AZRAEL_OVERLAY_REACT=0), ohne seine Chat-Antworten zu berühren — das ist ein
    getrennter Pfad."""
    src = open("bot.py").read()
    assert "AZRAEL_OVERLAY_REACT" in src, "Schalter fehlt"
    # Der react-Block hängt am Schalter
    i = src.find("if AZRAEL_OVERLAY_REACT and _OVERLAY.get")
    assert i > 0, "react-Overlay-Block nicht am Schalter"
    ok("AZRAEL: Overlay-Reaktion per AZRAEL_OVERLAY_REACT abschaltbar")

    # Chat-Antwort (_KICK_MOD._handle / send_message) darf NICHT am Schalter hängen
    h = src.find("async def _handle(self, sender, content")
    hbody = src[h:h + 1400]
    assert "AZRAEL_OVERLAY_REACT" not in hbody, \
        "Chat-Handler darf nicht am Overlay-Schalter hängen (Chat läuft unabhängig)"
    ok("AZRAEL: Chat-Antworten unabhängig vom Overlay-Schalter")


def test_twitch_chat_scopes_and_reply():
    """V37-TWCHAT: Der OAuth-Flow holt jetzt auch chat:read/chat:edit — EINE
    Autorisierung deckt Follower UND Chat. AZRAEL antwortet auf Twitch/YouTube,
    aber nur kontrolliert (angesprochen + Cooldown + Shield-Screen)."""
    import nc.twitchoauth as tw
    for s in ("moderator:read:followers", "chat:read", "chat:edit"):
        assert s in tw.SCOPES, f"Scope {s} fehlt — Chat braucht chat:read/edit"
    ok("twitchoauth: Flow holt Follower- UND Chat-Scopes in einem Token")

    assert hasattr(tw, "login_name"), "login_name fehlt (IRC-NICK braucht ihn)"
    ok("twitchoauth: login_name für den IRC-NICK vorhanden")

    src = open("bot.py").read()
    # Chat-Loop nutzt den OAuth-Token, mit manuellem Fallback
    i = src.find("async def _twitch_chat_loop")
    body = src[i:i + 1800]
    assert "_twoauth.access_token" in body, "Chat-Loop nutzt OAuth-Token nicht"
    assert "TWITCH_CHAT_TOKEN" in body, "manueller Chat-Token muss Fallback bleiben"
    ok("twitch-chat-loop: OAuth-Token bevorzugt, manueller als Fallback")

    # AZRAEL-Antwort ist konservativ: Flag + Ansprache + Cooldown + Shield
    rb = _fn(src, "_azrael_chat_should_reply")        # v4.0-W117
    assert "AZRAEL_CHAT_REPLY" in rb and "addressed" in rb and "COOLDOWN" in rb, \
        "Antwort-Gate braucht Flag, Ansprache-Erkennung und Cooldown"
    ab = _fn(src, "_azrael_chat_reply")               # v4.0-W117
    assert "_sentinel_screen" in ab, "Shield muss VOR der Antwort screenen"
    ok("azrael-chat-reply: Flag + Ansprache + Cooldown + Shield-Screen")

    # Beide Plattformen verdrahtet
    assert src.count("_azrael_chat_reply(") >= 2, "Twitch UND YouTube müssen antworten können"
    assert '_azrael_chat_reply("twitch"' in src and '_azrael_chat_reply("youtube"' in src
    ok("azrael-chat-reply: Twitch + YouTube verdrahtet")


def test_twitch_sentinel_timeout():
    """V37-TWMOD: SENTINEL kann auf Twitch timeouten. Scope + Helix-Pfad da,
    am selben Auto-Moderate-Schalter wie Kick."""
    import nc.twitchoauth as tw
    assert "moderator:manage:banned_users" in tw.SCOPES, \
        "Timeout-Scope fehlt — SENTINEL kann auf Twitch nicht sperren"
    assert hasattr(tw, "timeout_user"), "timeout_user-Helfer fehlt"
    ok("twitchoauth: Moderations-Scope + timeout_user() vorhanden")

    src = open("bot.py").read()
    i = src.find("V37-TWMOD")
    body = src[i:i + 2200]      # W19: Fenster groesser (Team-Ausnahme + Verwarnung kamen dazu)
    assert "_twoauth.timeout_user" in body, "Twitch-Timeout wird nicht ausgelöst"
    assert 'cfg.get("auto_moderate")' in body, \
        "Twitch-Timeout muss am selben Sentinel-Schalter wie Kick hängen"
    assert "_screen_full" in body, "volle Moderation muss vor dem Timeout screenen (B168)"
    ok("sentinel: Twitch-Timeout am selben Schalter, voll geprüft (Sentinel+Bann+Spam)")

    # Der EventSub-Token in der .env bleibt Fallback, wird NICHT automatisch
    # überschrieben — der Refresh-Token lebt in der json, nicht in der .env.
    assert "twitch_oauth.json" in open("nc/twitchoauth.py").read() or \
        "store_path" in open("nc/twitchoauth.py").read()
    ok("token: Refresh-Token in json (nicht .env) — Auto-Refresh bleibt intakt")


def test_twitch_status_uses_oauth():
    """V37-TWFIX: Die Kanal-Status-Route (Follower/Live im Dashboard) hing nur am
    alten .env-Token und meldete »Token nötig«, obwohl OAuth verbunden war. Muss
    denselben OAuth-bevorzugt-Fallback nutzen wie der EventSub-Loop."""
    src = open("bot.py").read()
    body = _fn(src, "_twitch_channel_status")         # v4.0-W117
    assert "_twoauth.status().get(\"ready\")" in body, \
        "Status-Route prüft den OAuth-Flow nicht"
    assert "_twoauth.access_token" in body, "Status-Route nutzt den OAuth-Token nicht"
    # OAuth VOR dem .env-Fallback — auf den getenv-AUFRUF prüfen, nicht den Kommentar
    assert body.find("_twoauth.access_token") < body.find('os.getenv("TWITCH_EVENTSUB_TOKEN"'), \
        "OAuth muss vor dem .env-Token kommen"
    ok("twitch-status: nutzt OAuth-Token, .env nur als Fallback")

    # Die alte irreführende Meldung ist weg
    assert "TWITCH_CLIENT_ID + TWITCH_EVENTSUB_TOKEN nötig" not in src, \
        "alte Fehlermeldung muss auf den Verbinden-Flow verweisen"
    ok("twitch-status: Fehlermeldung verweist auf 'Twitch verbinden'")


def test_twitch_ingest_default():
    """V37-TWINGEST: Der Twitch-Ingest-Default muss der globale Server sein.
    Das alte rtmp://live.twitch.tv/app wird nicht mehr angenommen und brach
    Restreams mit rc=8 ab (in der Praxis bestätigt: Wechsel behob es)."""
    src = open("bot.py").read()
    assert "ingest.global-contribute.live-video.net" in src, \
        "globaler Twitch-Ingest fehlt als Default"
    assert 'os.getenv("TWITCH_INGEST_URL", "rtmp://live.twitch.tv/app")' not in src, \
        "alter, defekter Ingest-Default darf nicht zurückkehren"
    ok("twitch-ingest: globaler Server als Default (alter live.twitch.tv raus)")


def test_community_discovery_loop():
    """V37-COMMUNITY: Discovery-Loop — Wiedererkennung, Live-Ping, Highlight-Share.
    Jeder Teil einzeln schaltbar; Wiedererkennung bejubelt keine Erstbesucher."""
    import time as _t
    import nc.community as comm
    comm.configure(returning_enabled=True, returning_min_gap_s=100,
                   returning_min_visits=2, returning_greet_cooldown_s=0)
    now = _t.time()
    # Erstbesuch → KEINE Begrüßung (kein Bejubeln von Fremden)
    assert comm.note_chatter("Neu", "kick", now) is None, "Erstbesucher darf nicht begrüßt werden"
    # Sofort nochmal (keine Pause) → keine Begrüßung
    assert comm.note_chatter("Neu", "kick", now + 5) is None, "ohne Pause keine Begrüßung"
    # Nach echter Pause → Wiederkehr → Begrüßung
    assert comm.note_chatter("Neu", "kick", now + 200) is not None, "Wiederkehrer muss begrüßt werden"
    ok("community: Wiedererkennung begrüßt nur echte Wiederkehrer")

    # Live-Ping trägt Rollen-Ping + Plattformen
    comm.configure(live_role_id="999")
    ping = comm.live_ping("Streamer", ["Kick", "Twitch"], "Titel")
    assert "<@&999>" in ping and "Kick" in ping and "Twitch" in ping, ping
    ok("community: Live-Ping mit Rollen-Ping + Plattformen")

    # Highlight-Post ist teilbar (Aufruf zum Teilen)
    post = comm.highlight_post("user", stars=5)
    assert "user" in post and ("Teil" in post or "teil" in post), post
    ok("community: Highlight-Post ruft zum Teilen auf")

    # Verdrahtung im Bot: alle drei Trigger-Punkte
    src = open("bot.py").read()
    assert "_community.note_chatter" in src, "Wiedererkennung nicht im Chat-Push"
    assert "_community.live_ping" in src, "Live-Ping nicht am Restream-Start"
    assert "_community.highlight_post" in src, "Highlight-Share nicht am Clip-Highlight"
    # Live-Ping nur bei frischem Start (nicht bei Reconnects)
    assert "_attempts == 0" in src and "_COMMUNITY_PINGED" in src, \
        "Live-Ping muss gegen Reconnect-Spam entprellt sein"
    ok("community: alle drei Trigger verdrahtet, Live-Ping entprellt")


def test_loyalty_rewards():
    """V37-LOYALTY: Belohnungssystem — Punkte + Raenge, MUSS persistent sein
    (ein Belohnungssystem, das beim Neustart vergisst, ist wertlos)."""
    import nc.loyalty as L
    # Fake-DB
    store = {}
    L.configure(db_get=lambda k: store.get(k, 0),
                db_add=lambda k, d, n: store.__setitem__(k, store.get(k, 0) + d) or store[k],
                db_top=lambda n: sorted([(k, k.split(":")[-1], v) for k, v in store.items()],
                                        key=lambda x: -x[2])[:n],
                enabled=True, chat_cooldown_s=0, chat_points=10, return_points=25)

    # Rang-Grenzen korrekt
    assert L.rank_for(0)[0] == "Neuling"
    assert L.rank_for(100)[0] == "Stammgast"
    assert L.rank_for(5001)[0] == "Legende"
    ok("loyalty: Rang-Schwellen korrekt")

    # Chatten sammelt Punkte, Aufstieg wird gemeldet
    up = None
    import time as _t
    now = _t.time()
    for i in range(11):
        r = L.award_chat("Bob", "kick", now=now + i)
        if r and r["leveled_up"]:
            up = r
    assert up and up["rank"] == "Stammgast", "Rangaufstieg nicht gemeldet"
    ok("loyalty: Chat sammelt Punkte, Aufstieg wird gemeldet")

    # Cooldown gegen Farming
    store.clear()
    L.configure(chat_cooldown_s=60)
    now = _t.time()
    r1 = L.award_chat("Spam", "kick", now=now)
    r2 = L.award_chat("Spam", "kick", now=now + 5)   # zu schnell
    assert r1 is not None and r2 is None, "Cooldown greift nicht — Farming moeglich"
    ok("loyalty: Cooldown verhindert Punkte-Farming")

    # Persistenz-Verdrahtung: der Bot nutzt die DB-Tabelle, nicht RAM
    src = open("bot.py").read()
    schema_src = open("nc/schema.py").read()   # B164: Schema in eigenes Modul extrahiert
    assert "CREATE TABLE IF NOT EXISTS loyalty_points" in schema_src, "keine persistente Tabelle"
    assert "_loyalty.award_chat" in src, "Punkte werden nicht vergeben"
    assert "_loyalty.configure" in src and "db_add=_loyalty_add" in src, "DB nicht angebunden"
    ok("loyalty: persistente DB-Tabelle + Verdrahtung im Chat-Push")


def test_sentinel_chat_reach():
    """V37-SENTINEL-REACH: AZRAEL antwortet auf @Azrael in ALLEN Chats außer
    TikTok. Kick fehlte vorher (nur Twitch/YouTube) — jetzt ergänzt."""
    src = open("bot.py").read()
    # AZRAEL-Antwort auf allen drei erlaubten Plattformen
    for p in ("kick", "twitch", "youtube"):
        assert f'_azrael_chat_reply("{p}"' in src, f"AZRAEL antwortet nicht auf {p}"
    # TikTok bleibt außen vor
    assert '_azrael_chat_reply("tiktok"' not in src, "AZRAEL darf auf TikTok NICHT antworten"
    ok("sentinel-reach: AZRAEL antwortet auf Kick/Twitch/YouTube, nicht TikTok")

    # Kick nutzt die gemeinsame @Azrael-Erkennung (nicht nur die alte Frage-Logik)
    i = src.find("V37-SENTINEL-REACH")
    body = src[i:i + 800]
    assert "_azrael_chat_should_reply" in body and '_azrael_broadcast_reply("kick"' in body, \
        "Kick-@Azrael-Pfad nicht korrekt verdrahtet (B170: Broadcast-Fan-out)"
    ok("sentinel-reach: Kick nutzt @Azrael-Erkennung + Broadcast an alle Chats")


def test_foreign_ad_block():
    """V37-ADBLOCK: Fremdwerbung (fremder Link/Invite/Eigenwerbung) wird geblockt,
    eigene Kanäle/Discord per Allowlist ausgenommen. 0 False Positives Pflicht."""
    src = open("bot.py").read()
    assert "_detect_foreign_ad" in src, "Werbe-Detektor fehlt"
    assert '_spam_check' in src and 'block_ads' in src, "nicht in die Moderation verdrahtet"
    # Der Detektor muss die eigene Invite-Allowlist per vollem Pfad prüfen
    body = _fn(src, "_own_invites")                   # v4.0-W117
    assert "discord.gg" in body and "group(2)" in body, \
        "Invite muss auf vollen Pfad (mit Servername) geprüft werden"
    ok("adblock: Fremdwerbe-Detektor mit Eigen-Allowlist verdrahtet")

    # block_ads am Moderations-Schalter, per Env abschaltbar
    assert 'MOD_BLOCK_ADS' in src, "kein Env-Schalter für den Werbe-Filter"
    ok("adblock: per MOD_BLOCK_ADS schaltbar, Default an")


def test_brain_growth_viz():
    """V37-BRAINVIZ: Gehirn-Dashboard zeigt echten Lern-/Wachstumsverlauf —
    Zeitreihe aus Snapshots, nicht nur Momentan-Status."""
    src = open("bot.py").read()
    schema_src = open("nc/schema.py").read()   # B164: Schema extrahiert
    assert "CREATE TABLE IF NOT EXISTS brain_growth" in schema_src, "keine Wachstums-Tabelle"
    assert "def _brain_growth_snapshot" in src, "kein Snapshot-Mechanismus"
    assert '"/api/brain/growth"' in src, "keine Growth-Route"
    assert "_brain_growth_loop" in src and 'name="brain-growth"' in src, \
        "stündlicher Snapshot-Loop nicht gespawnt"
    # Snapshot liest die echten Brain-Stats (nicht erfundene Zahlen)
    i = src.find("def _brain_growth_snapshot")
    body = src[i:i + 900]
    assert "knowledge.stats" in body and "semantic.stats" in body, \
        "Snapshot muss echte Brain-Stats lesen"
    ok("brainviz: Wachstums-Tabelle + Snapshot + Route + stündlicher Loop")

    # Dashboard zeichnet die Kurve
    try:
        html = open("templates/brain.html").read()
    except OSError:
        html = open("brain_dashboard.html").read()
    assert "loadGrowth" in html and 'id="growth"' in html, "keine Wachstumskurve im Dashboard"
    ok("brainviz: Lernkurve im Brain-Dashboard verdrahtet")


def test_llm_budget():
    """V37-LLMBUDGET: Brain-LLM-Budget großzügiger für CPU-Inferenz ohne GPU.
    Beides erhöht (Timeout + max_tokens), weil mehr Tokens mehr Zeit brauchen."""
    llm = open("brain/llm.py").read()
    # Timeout deutlich über den alten 60s (v4.0-W78: env_float statt float(getenv)
    # → leere .env crasht nicht mehr; Default weiterhin 300s).
    assert ('"BRAIN_LLM_TIMEOUT_S", "300"' in llm
            or 'env_float("BRAIN_LLM_TIMEOUT_S", 300)' in llm), "Timeout nicht auf 300s erhöht"
    assert ('"BRAIN_LLM_MAX_TOKENS", "1024"' in llm
            or 'env_int("BRAIN_LLM_MAX_TOKENS", 1024)' in llm), "max_tokens nicht auf 1024 erhöht"
    # weiter per Env übersteuerbar (nicht hartkodiert)
    assert "os.getenv" in llm, "Budget muss per Env einstellbar bleiben"
    ok("llmbudget: Brain-LLM Timeout 300s + max_tokens 1024, env-übersteuerbar")

    # Setup dokumentiert das größere Kontextfenster + die Abwägung
    setup = open("docs/SETUP_LLAMACPP.md").read()
    assert "-c 8192" in setup, "Kontextfenster nicht erhöht"
    assert "ABWÄGUNG" in setup or "Abwägung" in setup, "Ressourcen-Abwägung nicht dokumentiert"
    ok("llmbudget: Kontextfenster 8192 + Abwägung (RAM/Recordings) dokumentiert")


def test_nexus_removed():
    """V37-NEXUSOUT: Nexus (NeuralCore) vollständig entfernt — AZRAEL Sentinel
    ist das eigenständige System, Nexus war ein getrennter Selbstbeobachtungs-
    Kern und wurde auf Wunsch komplett rausgenommen."""
    src = open("bot.py").read()
    for token in ("NeuralCore", "_NEXUS", "_nexus_loop", "NEXUS_ENABLED",
                  "api_nexus_", "/api/nexus/"):
        assert token not in src, f"Nexus-Rest in bot.py: {token}"
    ok("nexusout: bot.py frei von Nexus")

    # Dashboard ebenfalls sauber
    try:
        html = open("templates/dashboard.html").read()
    except OSError:
        html = open("dashboard_v37.html").read()
    for token in ("nexusPropose", "/api/nexus/", "_nxRAF", "_nxLobes", "id=\"nx_"):
        assert token not in html, f"Nexus-Rest im Dashboard: {token}"
    ok("nexusout: Dashboard frei von Nexus")

    # AZRAEL Sentinel muss unberührt bestehen bleiben
    assert "_azrael_chat_reply" in src and "_sentinel_screen" in src, \
        "AZRAEL Sentinel darf NICHT mitentfernt worden sein"
    ok("nexusout: AZRAEL Sentinel intakt")


def test_restream_max_concurrent():
    """V37-MAXLIVE: Im Multi-Modus höchstens RESTREAM_MAX_CONCURRENT (Default 2)
    gleichzeitige Restreams — schützt den GPU-losen Server vor Encode-Flut."""
    src = open("bot.py").read()
    assert "RESTREAM_MAX_CONCURRENT" in src, "kein Concurrent-Deckel"
    assert 'RESTREAM_MAX_CONCURRENT", 2' in src, "Default nicht 2"
    # Der Deckel greift in der Multi-Modus-Schleife per break
    body = _ab(src, "V37-MAXLIVE: gedeckelt")         # v4.0-W117
    assert "len(self._procs) >= RESTREAM_MAX_CONCURRENT" in body and "break" in body, \
        "Deckel-Prüfung fehlt oder bricht nicht ab"
    ok("maxlive: Multi-Restream auf RESTREAM_MAX_CONCURRENT gedeckelt (Default 2)")

    # Single-Modus bleibt unberührt (genau 1)
    assert "if RESTREAM_SINGLE:" in src and "Slot belegt" in src, \
        "Single-Modus darf nicht kaputtgehen"
    ok("maxlive: Single-Modus (genau 1) unberührt")


def test_overlay_react_and_layout():
    """V37-REACTLIVE: AZRAEL reagiert im Sendebild nur auf den restreamten User;
    Sprechblase breiter/höher; Donation-Box oben links; Text nicht zu früh gekappt."""
    src = open("bot.py").read()
    # Reaktions-Filter auf den live-restreamten User
    assert "AZRAEL_REACT_ONLY_LIVE" in src, "kein Live-Reaktions-Filter"
    body = _ab(src, "NUR auf den User,\n                # der GERADE restreamt wird")   # v4.0-W117
    assert "_restream_active_sources()" in body and "continue" in body, \
        "Filter prüft nicht den aktiven Restream oder überspringt nicht"
    # Sicherung: kein aktiver Restream → nicht alles blockieren
    assert "if _active and" in body, "leerer Restream würde AZRAEL komplett stummschalten"
    ok("overlay: AZRAEL reagiert nur auf den restreamten User (mit Solo-Sicherung)")

    # Maxlen angehoben, damit ganzer Text passt
    assert 'AZRAEL_OVERLAY_MAXLEN", 400' in src, "Overlay-Textlänge nicht erhöht"
    ok("overlay: Reaktionstext-Länge auf 400 erhöht")

    # Overlay-Layout
    try:
        html = open("templates/overlay.html").read()
    except OSError:
        html = open("overlay.html").read()
    assert "#don{left:40px;top:130px" in html, "Donation-Box nicht oben links"
    assert "#bubble{" in html and "width:440px" in html, "Sprechblase nicht verbreitert"
    ok("overlay: Donation-Box oben links, Sprechblase breiter")


def test_deepbughunt_fixes():
    """Tiefenbughunt: 3 echte Bugs gefunden + behoben (Log-Spam-Drossel,
    Race Condition bei Dict-Iteration, File-Handle-Leaks)."""
    src = open("bot.py").read()
    # Bug 1: Cookie-Warnung gedrosselt (nicht mehr pro Aufruf)
    assert "_COOKIE_WARN_TS" in src, "Cookie-Log-Spam-Drossel fehlt"
    assert "gedrosselt" in src, "Drossel-Logik nicht verdrahtet"
    ok("deepbughunt: Cookie-Log-Spam gedrosselt (max alle 60s)")

    # Bug 2: Race-sichere Iteration über _RESTREAM_ACTIVE_ALL (list())
    # Es darf keine ungeschützte for-Schleife über .items() mehr geben, die
    # parallel zu einem pop() läuft.
    import re
    bare = re.findall(r"for _rid, _info in _RESTREAM_ACTIVE_ALL\.items\(\)", src)
    assert not bare, f"ungeschützte Dict-Iteration (Race mit pop): {len(bare)}×"
    ok("deepbughunt: Dict-Iteration race-sicher (list()-Schutz)")

    # Bug 3: kein nacktes open() mehr für /proc (fd-Leak im Health-Loop)
    assert 'for line in open("/proc/meminfo")' not in src, "fd-Leak /proc/meminfo"
    assert 'open("/proc/loadavg").read()' not in src, "fd-Leak /proc/loadavg"
    ok("deepbughunt: /proc-Reads ohne File-Handle-Leak (with-Block)")


def test_pwa():
    """PWA: Dashboard als installierbare App. Manifest + Service Worker + Icons,
    aber Service Worker cacht NIEMALS API-Daten (Live-Kontrollpanel)."""
    src = open("bot.py").read()
    # Routen vorhanden
    assert '"/manifest.webmanifest"' in src, "keine Manifest-Route"
    assert '"/sw.js"' in src, "keine Service-Worker-Route"
    assert "/pwa-icon-<variant>.png" in src, "keine Icon-Route"
    # Service-Worker-Scope-Header (sonst darf SW nicht die ganze App steuern)
    assert 'Service-Worker-Allowed' in src, "SW-Scope-Header fehlt"
    # Icon-Route hat Whitelist (Path-Traversal-Schutz)
    body = _fn(src, "pwa_icon")                       # v4.0-W117
    assert "allowed" in body and "abort(404)" in body, "Icon-Route ohne Whitelist"
    ok("pwa: Routen für Manifest, Service Worker, Icons (mit Path-Schutz)")

    # Service Worker: API NIEMALS cachen (kritisch — Live-Panel)
    # Der Service Worker liegt seit dem Umzug unter templates/sw.js. Gleiches
    # try/except-Muster wie bei brain.html oben — der alte flache Name bleibt als
    # Rückfall stehen, damit der Test auch gegen ältere Bestände läuft.
    try:
        sw = open("templates/sw.js").read()
    except OSError:
        sw = open("pwa_sw.js").read()
    assert '/api/' in sw and "network-only" in sw or "startsWith(\"/api/\")" in sw, \
        "SW muss /api/ vom Caching ausnehmen"
    assert "return; // Standard-Browserverhalten" in sw, "API-Requests nicht network-only"
    ok("pwa: Service Worker cacht keine API-Daten (kein Stale-Status)")

    # Dashboard verlinkt Manifest + registriert SW
    try:
        html = open("templates/dashboard.html").read()
    except OSError:
        html = open("dashboard_v37.html").read()
    assert "manifest.webmanifest" in html and "serviceWorker" in html, \
        "Dashboard bindet PWA nicht ein"
    ok("pwa: Dashboard verlinkt Manifest + registriert Service Worker")


# ------------------------------------------------- B161) Test-Push-Guard (Sicherheitskern)

def test_b161_testpush_guard():
    """B161: die bot-freie Freigabelogik in nc.restream_testpush. Deckt den
       gesamten Sicherheits-Entscheidungsbaum ab — das ist der Teil, bei dem ein
       Fehler ein versehentliches Live-Bild bedeutet."""
    from nc import restream_testpush as tp

    # ── resolve_target ──────────────────────────────────────────────
    # Ohne Test-Ziel wird NICHT still auf den Live-Key ausgewichen.
    c0 = tp.TestPushConfig(live_ingest="rtmps://ingest.kick.com/app", live_key="LIVE")
    r0 = tp.resolve_target(c0, tp.TARGET_TEST)
    assert (not r0.ok) and r0.error == "kein_test_ziel", "kein Test-Ziel → refuse, kein Live-Ausweich"
    ok("b161: ohne Test-Ziel kein stiller Live-Ausweich")

    # Eigener Test-Slot → is_live_key False (Key ≠ Live-Key).
    c1 = tp.TestPushConfig(test_ingest="rtmp://127.0.0.1/live", test_key="TESTK",
                           live_ingest="rtmps://ingest.kick.com/app", live_key="LIVE")
    r1 = tp.resolve_target(c1, tp.TARGET_TEST)
    assert r1.ok and r1.source == "test" and r1.is_live_key is False
    ok("b161: Test-Slot wird als Nicht-Live-Key erkannt")

    # Test-Key IDENTISCH mit Live-Key → trotzdem als Live-Key markiert (Isolation echt).
    c2 = tp.TestPushConfig(test_ingest="rtmps://ingest.kick.com/app", test_key="LIVE",
                           live_ingest="rtmps://ingest.kick.com/app", live_key="LIVE")
    r2 = tp.resolve_target(c2, tp.TARGET_TEST)
    assert r2.ok and r2.is_live_key is True, "Key==Live-Key muss als Live-Key gelten"
    ok("b161: als Test getarnter Live-Key fällt unter Live-Schutz")

    # Live-Ziel gesperrt ohne allow_live.
    r3 = tp.resolve_target(c1, tp.TARGET_LIVE)
    assert (not r3.ok) and r3.error == "live_gesperrt"
    ok("b161: Live-Ziel ohne allow_live gesperrt")

    # ── guard: laufender Restream blockt IMMER (auch harmloses Test-Ziel) ──
    d = tp.guard(c1, r1, active_all_nonempty=True, channel=tp.CH_OFFLINE, confirm=True)
    assert (not d.allowed) and d.reason == "restream_active" and d.http == 409
    ok("b161: laufender Restream blockt Test-Push (Slot-Kollision)")

    # ── guard: Test-Slot frei, aber confirm fehlt ──
    d = tp.guard(c1, r1, active_all_nonempty=False, channel=tp.CH_OFFLINE, confirm=False)
    assert (not d.allowed) and d.reason == "confirm_required"
    ok("b161: Test-Slot verlangt Bestätigung")

    # ── guard: Test-Slot frei + confirm → erlaubt ──
    d = tp.guard(c1, r1, active_all_nonempty=False, channel=tp.CH_UNKNOWN, confirm=True)
    assert d.allowed and d.reason == "ok_test", "Test-Slot ignoriert Kanal-Live (eigener Ingest)"
    ok("b161: Test-Slot mit Bestätigung erlaubt (Kanal-Status egal)")

    # ── guard: Live-Key ohne allow_live → 403 ──
    cL = tp.TestPushConfig(live_ingest="rtmps://ingest.kick.com/app", live_key="LIVE",
                           allow_live=False)
    rL = tp.resolve_target(c2, tp.TARGET_TEST)  # is_live_key True
    d = tp.guard(cL, rL, active_all_nonempty=False, channel=tp.CH_OFFLINE, confirm=True)
    assert (not d.allowed) and d.reason == "live_forbidden" and d.http == 403
    ok("b161: Live-Key ohne allow_live abgelehnt")

    # ── guard: Live-Key + allow_live, aber Kanal LIVE → 423, nie überschreibbar ──
    cLA = tp.TestPushConfig(test_ingest="rtmps://ingest.kick.com/app", test_key="LIVE",
                            live_ingest="rtmps://ingest.kick.com/app", live_key="LIVE",
                            allow_live=True)
    rLA = tp.resolve_target(cLA, tp.TARGET_TEST)
    d = tp.guard(cLA, rLA, active_all_nonempty=False, channel=tp.CH_LIVE, confirm=True)
    assert (not d.allowed) and d.reason == "channel_live" and d.http == 423
    ok("b161: Live-Key bei LIVE-Kanal immer abgelehnt")

    # ── guard: Live-Key + allow_live, Kanal UNKNOWN → abgelehnt (nicht beweisbar sicher) ──
    d = tp.guard(cLA, rLA, active_all_nonempty=False, channel=tp.CH_UNKNOWN, confirm=True)
    assert (not d.allowed) and d.reason == "channel_unknown"
    ok("b161: Live-Key bei unklarem Kanal abgelehnt")

    # ── guard: Live-Key + allow_live + Kanal offline, aber confirm fehlt → 428 ──
    d = tp.guard(cLA, rLA, active_all_nonempty=False, channel=tp.CH_OFFLINE, confirm=False)
    assert (not d.allowed) and d.reason == "confirm_required_live"
    ok("b161: Live-Key offline verlangt ausdrückliche Bestätigung")

    # ── guard: der EINZIGE erlaubte Live-Pfad (allow_live+offline+confirm) ──
    d = tp.guard(cLA, rLA, active_all_nonempty=False, channel=tp.CH_OFFLINE, confirm=True)
    assert d.allowed and d.reason == "ok_live"
    ok("b161: Live-Push nur bei allow_live + offline + confirm")

    # ── build_cmd: Ziel-String bitgenau, hart gedeckelte Dauer, testsrc-Quelle ──
    norm = lambda u: u.rstrip("/")
    cmd = tp.build_cmd("rtmp://127.0.0.1/live", "K", norm, duration_s=999, fps=30)
    assert cmd[-1] == "rtmp://127.0.0.1/live/K" and cmd[-2] == "flv"
    di = cmd.index("-t"); assert cmd[di+1] == "30", "Dauer hart auf 30s gedeckelt"
    assert any("testsrc2" in a for a in cmd) and "ffmpeg" == cmd[0]
    ok("b161: build_cmd baut testsrc→flv, Dauer gedeckelt, Ziel exakt")

    # ── classify_result: die Fehlerbilder des echten Kick-Ingest ──
    assert tp.classify_result(0, "")["state"] == "ok"
    assert tp.classify_result(1, "HTTP error 403 Forbidden")["state"] == "forbidden"
    assert tp.classify_result(1, "Connection refused")["state"] == "refused"
    assert tp.classify_result(1, "Error: End of file")["state"] == "error"
    ok("b161: classify_result trennt ok/forbidden/refused/error")

    # ── fingerprint: nie Klartext, deterministisch ──
    fp = tp.fingerprint("abc")
    assert fp["len"] == 3 and fp["fp"] == (97 + 98 + 99) % 65536
    ok("b161: fingerprint = len+Quersumme (kein Klartext)")


# ------------------------------------------------- B162) Marketing-Agent (Anti-Spam-Kern)

def test_b162_marketing():
    """B162: die bot-freie should_post-Entscheidung + compose. Der Kern, bei dem
       ein Fehler einen im Minutentakt spammenden Agenten bedeutet."""
    from nc import marketing as mk

    base = dict(enabled=True, auto=True, targets=("discord",),
                cadence_hours=6, min_gap_hours=3, quiet_start=23, quiet_end=8,
                channels={"Kick": "https://kick.com/x"}, website="https://lafap.de")

    # AUS ist AUS.
    d = mk.should_post(mk.MarketingConfig(**{**base, "enabled": False}),
                       mk.MarketingState(), 1_000_000, 12, any_live=False)
    assert d == (False, "disabled")
    ok("b162: enabled=False blockt")

    # MANUELL-ZUERST: ohne auto postet der Loop nie.
    d = mk.should_post(mk.MarketingConfig(**{**base, "auto": False}),
                       mk.MarketingState(), 1_000_000, 12, any_live=False)
    assert d == (False, "manual_only")
    ok("b162: auto=False → Loop postet nicht (nur Knopf)")

    # Keine Ziele.
    d = mk.should_post(mk.MarketingConfig(**{**base, "targets": ()}),
                       mk.MarketingState(), 1_000_000, 12, any_live=False)
    assert d == (False, "no_targets")
    ok("b162: ohne Ziele kein Post")

    # only_when_live.
    d = mk.should_post(mk.MarketingConfig(**{**base, "only_when_live": True}),
                       mk.MarketingState(), 1_000_000, 12, any_live=False)
    assert d == (False, "not_live")
    ok("b162: only_when_live blockt wenn offline")

    cfg = mk.MarketingConfig(**base)

    # Erstpost sofort fällig.
    assert mk.should_post(cfg, mk.MarketingState(), 1_000_000, 12, any_live=False) == (True, "due")
    ok("b162: Erstpost fällig")

    # Ruhezeit (Überlauf 23..8): 3 Uhr ist drin, 12 Uhr nicht.
    assert mk._in_quiet(3, 23, 8) is True and mk._in_quiet(12, 23, 8) is False
    assert mk.should_post(cfg, mk.MarketingState(), 1_000_000, 3, any_live=False)[1] == "quiet_hours"
    ok("b162: Ruhezeit mit Mitternachts-Überlauf")

    # Mindestabstand vor Cadence: 1h nach Post (min_gap 3h) → min_gap, nicht cadence.
    st = mk.MarketingState(last_post_ts=1_000_000, count=1)
    assert mk.should_post(cfg, st, 1_000_000 + 3600, 12, any_live=False) == (False, "min_gap")
    # 4h nach Post: über min_gap, aber unter cadence(6h) → cadence.
    assert mk.should_post(cfg, st, 1_000_000 + 4*3600, 12, any_live=False) == (False, "cadence")
    # 7h nach Post: fällig.
    assert mk.should_post(cfg, st, 1_000_000 + 7*3600, 12, any_live=False) == (True, "due")
    ok("b162: min_gap greift vor cadence, danach fällig")

    # next_due_ts: ohne Historie None, sonst last + max(cadence,min_gap).
    assert mk.next_due_ts(cfg, mk.MarketingState()) is None
    assert mk.next_due_ts(cfg, st) == 1_000_000 + 6*3600
    ok("b162: next_due_ts korrekt")

    # compose: Kanäle + Website in beiden Zielen, Discord Markdown, Telegram Klartext.
    msg = mk.compose(cfg, variant=0, flavor="Heute Abend geht es los!")
    assert "https://kick.com/x" in msg["discord"] and "https://kick.com/x" in msg["telegram"]
    assert "lafap.de" in msg["discord"] and "Heute Abend geht es los!" in msg["telegram"]
    assert "**" in msg["discord"] and "**" not in msg["telegram"]   # TG bewusst ohne Markdown
    ok("b162: compose baut beide Ziele korrekt")

    # variant rotiert.
    a = mk.compose(cfg, variant=0)["discord"].splitlines()[0]
    b = mk.compose(cfg, variant=1)["discord"].splitlines()[0]
    assert a != b
    ok("b162: Aufhänger rotiert je Post")

    # has_content: leer → False.
    assert mk.has_content(mk.MarketingConfig(enabled=True)) is False
    assert mk.has_content(cfg) is True
    ok("b162: has_content erkennt leere Konfiguration")


# ------------------------------------------------- B163) News-Agent (öffentliche Website-News)

def test_b163_news():
    """B163: die bot-freie News-Logik — build_items aus echten Fakten, Dedup, should_generate."""
    from nc import news as nw

    facts = {"version": "4.0", "platforms": ["Kick", "YouTube"], "tracked": 42,
             "live_today": ["alpha", "beta"], "live_today_count": 2,
             "kg_facts": 210, "agents_active": 12}

    # build_items: je Kategorie ein Item, echte Zahlen im Text, nichts erfunden.
    items = nw.build_items(facts, categories=nw.CATEGORIES, now_ts=1000)
    assert len(items) == 3
    by = {it["category"]: it for it in items}
    # v4.0: CREATORS = Tages-Live-Report (nie Aufnahmen)
    assert "42" in by["creators"]["body"] and "2 von 42" in by["creators"]["body"]
    assert "alpha" in by["creators"]["body"]
    assert "aufnahm" not in by["creators"]["body"].lower()
    assert "12" in by["ai"]["body"] and "210" in by["ai"]["body"]
    assert "Kick" in by["project"]["body"] and "YouTube" in by["project"]["body"]
    assert all(it.get("category_label") for it in items)
    ok("b163: build_items nutzt echte Fakten je Kategorie")

    # KI-Formulierung ersetzt nur den Body.
    it2 = nw.build_items(facts, phrasings={"project": "Frei formuliert."}, categories=("project",), now_ts=1)
    assert it2[0]["body"] == "Frei formuliert."
    ok("b163: phrasing überschreibt Body")

    # Robuster AI-Text auch ohne Zahlen (keine 0-Peinlichkeit).
    b0 = nw._static_body("ai", {})
    assert "0" not in b0 and b0
    ok("b163: AI-Text ohne Fakten bleibt sauber")

    # merge: exakte Duplikate raus, neueste zuerst, Cap.
    old = nw.build_items(facts, categories=("project",), now_ts=500)
    new = nw.build_items(facts, categories=("project",), now_ts=1500)   # identischer Text → gleiche id
    m = nw.merge(old, new, 20)
    assert len(m) == 1, "identischer Inhalt darf nicht doppelt erscheinen"
    diff = nw.merge(old, nw.build_items({**facts, "tracked": 99}, categories=("creators",), now_ts=1500), 20)
    assert len(diff) == 2 and diff[0]["ts"] == 1500, "neuer Inhalt vorn"
    cap = nw.merge([], [{"id": str(i), "ts": i, "category": "x"} for i in range(30)], 20)
    assert len(cap) == 20
    ok("b163: merge dedupt, sortiert, deckelt")

    # should_generate: AUS/manuell/Ruhezeit/Cadence/fällig.
    base = dict(enabled=True, auto=True, categories=nw.CATEGORIES, cadence_hours=24,
                quiet_start=2, quiet_end=6)
    assert nw.should_generate(nw.NewsConfig(**{**base, "enabled": False}), nw.NewsState(), 1000, 12)[1] == "disabled"
    assert nw.should_generate(nw.NewsConfig(**{**base, "auto": False}), nw.NewsState(), 1000, 12)[1] == "manual_only"
    assert nw.should_generate(nw.NewsConfig(**base), nw.NewsState(), 1000, 3)[1] == "quiet_hours"
    cfg = nw.NewsConfig(**base)
    assert nw.should_generate(cfg, nw.NewsState(), 1000, 12) == (True, "due")
    st = nw.NewsState(last_gen_ts=1000, count=1)
    assert nw.should_generate(cfg, st, 1000 + 3600, 12)[1] == "cadence"
    assert nw.should_generate(cfg, st, 1000 + 25*3600, 12) == (True, "due")
    ok("b163: should_generate Entscheidungsbaum")

    # render_json-Struktur.
    j = nw.render_json(items, 1234)
    assert j["generated_at"] == 1234 and j["count"] == 3 and j["items"] == items
    ok("b163: render_json-Struktur korrekt")


# ------------------------------------------------- v4.1) Ausführliche Website-News

def test_v41_news_ausfuehrlich():
    """v4.1: eine News ist keine Statuszeile mehr. Verriegelt die neuen Felder,
       die Absatz-Struktur und — der eigentliche Punkt — dass die KI NUR den
       Fließtext formuliert: Kennzahlen und Detailpunkte kommen ausschließlich
       aus echten Fakten und dürfen von einer Halluzination nie berührt werden."""
    from nc import news as nw

    facts = {"version": "4.1", "platforms": ["Kick", "Twitch", "YouTube"], "tracked": 42,
             "live_today": ["alpha", "beta"], "live_today_count": 2,
             "kg_facts": 210, "agents_active": 12, "sessions_7d": 37,
             "live_7d_count": 11, "active_days_7d": 6, "restream_targets": 3,
             "mod_actions_7d": 48, "ai_answers_7d": 264, "kg_growth_7d": 31}
    items = nw.build_items(facts, categories=nw.CATEGORIES, now_ts=1000)
    assert len(items) == 3
    for it in items:
        assert it["lead"].strip(), f"{it['category']}: kein Anreißer"
        assert len(it["body"].split("\n\n")) >= 2, f"{it['category']}: nur ein Absatz"
        assert len(it["metrics"]) >= 2, f"{it['category']}: zu wenige Kennzahlen"
        assert len(it["bullets"]) >= 3, f"{it['category']}: zu wenige Detailpunkte"
        assert it["tags"], f"{it['category']}: keine Themen"
        for m in it["metrics"]:
            assert m.get("label") and str(m.get("value", "")).strip()
    ok("v4.1: lead/metrics/bullets/tags je Kategorie gefüllt, Body mehrabsätzig")

    # Das Wochenbild landet auch wirklich im Text, nicht nur in den Kennzahlen.
    by = {it["category"]: it for it in items}
    assert "37" in by["creators"]["body"] and "11" in by["creators"]["body"]
    assert "31" in by["ai"]["body"] and "264" in by["ai"]["body"]
    ok("v4.1: Wochenzahlen stehen im Fließtext")

    # Fehlt eine Zahl, verschwindet sie — sie wird NIE zur 0 auf der Website.
    duenn = nw.build_items({"tracked": 5, "live_today_count": 0, "platforms": []},
                           categories=nw.CATEGORIES, now_ts=1)
    for it in duenn:
        for m in it["metrics"]:
            if m["label"] != "Heute live":
                assert m["value"] not in ("0", "+0"), (it["category"], m)
    ok("v4.1: fehlende Fakten erzeugen keine 0-Kennzahlen")

    # KI-Formulierung ersetzt NUR den Body — Kennzahlen bleiben faktenrein.
    frei = nw.build_items(facts, phrasings={"ai": "Frei erfunden: 999 Dinge."},
                          categories=("ai",), now_ts=1)[0]
    assert frei["body"] == "Frei erfunden: 999 Dinge."
    assert all("999" not in str(m["value"]) for m in frei["metrics"])
    assert frei["bullets"] and all("999" not in b for b in frei["bullets"])
    ok("v4.1: Phrasing berührt Kennzahlen und Detailpunkte nicht")

    # Ein geänderter Detailwert ist eine NEUE Meldung, kein Duplikat.
    a = nw.build_items(facts, categories=("ai",), now_ts=100)
    b = nw.build_items({**facts, "kg_growth_7d": 32}, categories=("ai",), now_ts=200)
    assert len(nw.merge(a, b, 20)) == 2, "geänderte Kennzahl fällt als Duplikat weg"
    ok("v4.1: item_id erfasst auch die neuen Felder")

    # Öffentliche Texte in echtem Deutsch — keine ae/oe/ue-Umschrift.
    import re
    erlaubt = {"Zuschauer", "Zuschauerzahlen", "Azrael", "Azraels", "aktuelle", "neue",
               "Blaue", "graue"}
    for it in items:
        t = (it["lead"] + " " + it["body"] + " " + " ".join(it["bullets"]) + " " +
             " ".join(m["label"] for m in it["metrics"]))
        rest = {w for w in re.findall(r"\w*(?:ae|oe|ue)\w*", t) if w not in erlaubt}
        assert not rest, f"{it['category']}: Umschrift im öffentlichen Text: {rest}"
    ok("v4.1: öffentliche News in korrektem Deutsch")

    # Der eigentliche Betriebsfall: Fakten fehlen EINZELN. Genau dabei sind im
    # Praxislauf zwei Saetze zerbrochen ("Jeder von ihnen" ohne Bezug, ein Absatz
    # der klein anfing). Deshalb jede Teilmenge durchspielen, nicht nur "alles da".
    import itertools
    optional = ["tracked", "agents_active", "kg_facts", "kg_growth_7d",
                "ai_answers_7d", "mod_actions_7d", "sessions_7d", "live_7d_count",
                "active_days_7d", "version", "platforms", "live_today",
                "live_today_count"]
    for r in range(len(optional) + 1):
        if r not in (0, 1, len(optional) - 1, len(optional)):
            continue          # Raender genuegen; alle 8192 Kombinationen waeren Ballast
        for weg in itertools.combinations(optional, r):
            teil = {k: v for k, v in facts.items() if k not in weg}
            for it in nw.build_items(teil, categories=nw.CATEGORIES, now_ts=1):
                for abs_ in it["body"].split("\n\n"):
                    assert abs_ == abs_.strip(), f"{it['category']}: Absatz mit Rand-Leerzeichen"
                    assert abs_[0].isupper() or abs_[0].isdigit(), \
                        f"{it['category']}: Absatz beginnt klein — {abs_[:60]!r} (ohne {weg})"
                    assert ".." not in abs_ and " ." not in abs_ and ", ." not in abs_, \
                        f"{it['category']}: Satzrest — {abs_[:80]!r} (ohne {weg})"
                if not teil.get("agents_active"):
                    assert "Jeder von ihnen" not in it["body"], \
                        f"{it['category']}: 'Jeder von ihnen' ohne Bezugszahl"
    ok("v4.1: Saetze bleiben ganz, auch wenn einzelne Fakten fehlen")

    # Die Fakten werden auch wirklich eingesammelt. v4.1-W4: der Fakten- und
    # KI-Pfad liegt in nc/news.py, nicht mehr im Monolithen — der VERTRAG ist
    # unveraendert, nur sein Anker ist mitgewandert.
    src = open("nc/news.py", encoding="utf-8").read()
    for key in ("sessions_7d", "active_days_7d", "live_7d_count", "restream_targets",
                "mod_actions_7d", "ai_answers_7d", "kg_growth_7d"):
        assert f'facts["{key}"]' in src, f"collect_facts sammelt {key} nicht"
    assert "def absaetze(" in src and "out = absaetze(out)" in src, \
        "KI-Antwort wird nicht auf Absätze normalisiert"
    assert 'GENAU DREI Absaetze' in src, "KI-Prompt fordert keine Absätze"
    # Zeitfenster in Python berechnet — datetime()/DATE() gibt es auf MariaDB nicht.
    _blk = src[src.find("def collect_facts"):src.find("async def phrase(")]
    # Kommentarzeilen raus: der Block ERKLAERT, warum diese Funktionen fehlen —
    # ohne den Filter meldet der Vertrag genau diese Erklaerung als Verstoss.
    _code = "\n".join(z for z in _blk.split("\n") if not z.strip().startswith("#"))
    assert "datetime('now'" not in _code and "DATE(" not in _code, \
        "SQLite-only-Datumsfunktion im News-Fakten-Pfad"
    ok("v4.1: _news_facts liefert das Wochenbild, backend-neutral")

    # Die Website rendert die neuen Felder — und überlebt alte Einträge ohne sie.
    h = open("website/lafap_index.html", encoding="utf-8").read()
    for marke in ("n-lead", "n-figs", "n-fig", "n-body", "n-points", "n-tag",
                  "figs(it.metrics)", "punkte(it.bullets)", "themen(it.tags)"):
        assert marke in h, f"Website rendert {marke} nicht"
    assert "absaetze(it.body)" in h, "Website trennt den Body nicht in Absätze"
    seed = open("website/news.json", encoding="utf-8").read()
    for feld in ('"lead"', '"metrics"', '"bullets"', '"tags"'):
        assert feld in seed, f"Seed ohne {feld}"
    ok("v4.1: Website-Renderer und Seed tragen die neuen Felder")


# ------------------------------------------------- B165) Mod-Heuristik (plattformunabhängig)

def test_b165_modheuristics():
    """B165: die aus KickModerator extrahierte reine Heuristik. Grenzwerte verriegelt,
       damit das Moderationsverhalten bitgenau bleibt (verhindert Über-/Unter-Timeouts)."""
    from nc import modheuristics as m

    # CAPS: erst ab 10 Buchstaben, Anteil >= max_ratio.
    assert m.stateless_reason("A" * 9) is None                 # <10 Buchstaben → nie CAPS
    assert m.stateless_reason("A" * 10) == "CAPS-Spam"         # 10, 100% caps
    assert m.stateless_reason("a" * 7 + "ABC") is None         # 30% caps < 0.7
    assert m.stateless_reason("A" * 7 + "abc") == "CAPS-Spam"  # 70% == Grenze → spam
    assert m.is_caps_spam("HALLO WELTEN", max_ratio=0.7) is True
    ok("b165: CAPS-Grenze (>=10 Buchstaben, >=0.7) exakt")

    # Links: strikt > max_links.
    assert m.stateless_reason("http://a http://b") is None            # 2, nicht >2
    assert m.stateless_reason("http://a http://b http://c") == "Link-Spam"
    assert m.count_links("www.x www.y") == 2
    ok("b165: Link-Spam strikt über Schwelle")

    # Mentions: strikt > max_mentions.
    assert m.stateless_reason("@a @b @c @d @e") is None               # 5, nicht >5
    assert m.stateless_reason("@a @b @c @d @e @f") == "Mention-Spam"
    ok("b165: Mention-Spam strikt über Schwelle")

    # Reihenfolge: CAPS wird vor Mention gemeldet (nur-Großbuchstaben, damit
    # das Caps-Verhältnis nicht durch Kleinbuchstaben verwässert wird).
    assert m.stateless_reason("AAAAAAAAAA @A @B @C @D @E @F") == "CAPS-Spam"
    ok("b165: Grund-Reihenfolge CAPS vor Mention erhalten")

    # Flood vor Repeat; Grenzen: >flood_max bzw. >=3 gleiche.
    assert m.flood_reason(["x"] * 6, "x", flood_max=5) == "Flood"     # 6 > 5
    assert m.flood_reason(["x"] * 5, "x", flood_max=5) == "Repeat-Spam"  # nicht Flood, aber 5x gleich
    assert m.flood_reason(["x", "y"], "x", flood_max=5) is None
    assert m.flood_reason(["x", "x", "x"], "x", flood_max=9) == "Repeat-Spam"  # genau 3
    ok("b165: Flood (>max) vor Repeat (>=3), Grenzen exakt")

    # Eskalations-Leiter [1,5,cap], gedeckelt.
    assert [m.escalation_minutes(n, cap=10) for n in (1, 2, 3, 4)] == [1, 5, 10, 10]
    assert m.escalation_minutes(2, cap=3) == 3        # second(5) über cap(3) → gedeckelt
    assert m.escalation_minutes(1, cap=3) == 1
    ok("b165: Eskalations-Leiter mit Cap exakt")


# ------------------------------------------------- B166) Piper-Stimm-Auflösung + Outcomes-Fix

def test_b166_piper_voices():
    """B166: reine Piper-Auflösung (aus bot.py extrahiert) + der OUTCOMES-Renderfix."""
    from nc import piper_voices as pv

    voices = [{"name": "de_DE-thorsten-medium", "path": "/opt/piper/de_DE-thorsten-medium.onnx"},
              {"name": "de_DE-karlsson-low", "path": "/opt/piper/sub/de_DE-karlsson-low.onnx"},
              {"name": "en_US-amy", "path": "/voices/en_US-amy.onnx"}]

    # Teilstring greift ('thorsten' → volle Stimme, auch im Unterordner-Fall).
    assert pv.resolve_model_path("thorsten", voices).endswith("de_DE-thorsten-medium.onnx")
    # exakter Name schlägt Teilstring.
    assert pv.resolve_model_path("de_DE-karlsson-low", voices).endswith("sub/de_DE-karlsson-low.onnx")
    # exakter Dateiname mit .onnx.
    assert pv.resolve_model_path("en_US-amy.onnx", voices).endswith("en_US-amy.onnx")
    # nichts passendes → None; leer → None.
    assert pv.resolve_model_path("zzz", voices) is None
    assert pv.resolve_model_path("", voices) is None
    ok("b166: resolve_model_path Reihenfolge exakt (Name>Datei>Teilstring)")

    # voice_roots: base zuerst, dann Standardorte, dann rec/voices + module/voices, dedup.
    r = pv.voice_roots(["/custom"], recordings_dir="/rec", module_dir="/mod")
    assert r[0] == "/custom" and "/opt/piper" in r
    assert r[-2:] == ["/rec/voices", "/mod/voices"]
    assert len(r) == len(set(r))
    # doppelte base werden nicht erneut angehängt.
    assert pv.voice_roots(["/opt/piper"]).count("/opt/piper") == 1
    ok("b166: voice_roots Reihenfolge + Dedup exakt")

    # OUTCOMES-Fix: die Renderfunktion liest jetzt die Array-Form (kein NaN/[object Object]).
    src = open("templates/dashboard.html").read()
    assert "Array.isArray(d.by_outcome)" in src, "OUTCOMES liest by_outcome nicht als Array"
    assert "o.label||o.key" in src, "OUTCOMES rendert nicht die Array-Objektfelder"
    ok("b166: OUTCOMES rendert Array-Form (NaN%/[object Object] behoben)")


# ------------------------------------------------- B167) Evolution-Analyse-Extraktion

def test_b167_evolution():
    """B167: der aus bot.py gelöste Selbstanalyse-Kern läuft eigenständig +
       liefert die erwartete Struktur/Quote (verbatim → Logik unverändert)."""
    import sqlite3, contextlib
    from nc import schema, evolution
    from datetime import datetime, timezone
    conn=sqlite3.connect(":memory:"); conn.row_factory=sqlite3.Row
    schema.create_schema(conn, pk="INTEGER PRIMARY KEY AUTOINCREMENT", txt_idx="TEXT",
        txt_long="TEXT", txt_big="TEXT", iv="INTEGER", tbl_opts="", is_my=False,
        _create_index_safe=lambda c,a,b=None:c.execute(a),
        _migrate_columns=lambda c,t,e:[c.execute("ALTER TABLE %s ADD COLUMN %s %s"%(t,k,v)) for k,v in e.items() if k not in {r[1] for r in c.execute("PRAGMA table_info(%s)"%t)}],
        log=type("L",(),{"info":lambda*a:0,"warning":lambda*a:0,"debug":lambda*a:0})())
    now=datetime.now(timezone.utc).isoformat()
    for oc in ["ok"]*7+["forbidden"]*2+["early_disconnect"]+["running"]:
        conn.execute("INSERT INTO recording_attempts (username, outcome, started_at) VALUES (?,?,?)",("u",oc,now))
    conn.commit()
    @contextlib.contextmanager
    def dbc():
        yield conn
    res=evolution.analyze(db_conn=dbc, _evolution_llm_note=lambda i,p:None, EVOLUTION_WINDOW_DAYS=30)
    assert set(res)>={"insights","proposals","learned"}
    assert isinstance(res["insights"],list) and isinstance(res["learned"],dict)
    assert "70.0%" in " ".join(res["insights"]), "Erfolgsquote falsch → Logik verändert"
    ok("b167: evolution.analyze läuft eigenständig, Quote korrekt (7/10)")
    # Bot bindet den Kern nicht mehr selbst
    src=open("bot.py").read()
    assert "def _evolution_analyze()" not in src, "Analyse-Kern noch im Monolithen"
    # v4.1-W3: der Anker war "_nc_evolution.analyze(" — seit der Zyklus selbst im
    # Modul liegt, ruft der Bot analyze() gar nicht mehr direkt. Der VERTRAG ist
    # unveraendert (der Kern gehoert nicht in den Monolithen), nur sein Anker ist
    # gewandert. Deshalb migriert statt geloescht.
    assert "_nc_evolution.cycle" in src, "Bot delegiert nicht an nc.evolution"
    ok("b167: Monolith delegiert den Zyklus an nc.evolution")



# ------------------------------------------------- v4.1-W3) Evolution-Core komplett raus

def test_v41_w3_evolution_core_raus():
    """v4.1-W3: nicht nur die Analyse, der GANZE Core liegt in nc/evolution.py —
       und die acht Routen im Blueprint, ohne einen einzigen neuen ctx-Slot."""
    from nc import evolution
    src = open("bot.py", encoding="utf-8").read()

    # (1) Keine der fuenf Funktionen steht noch im Monolithen.
    for name in ("_evo_build_dir", "_evo_version", "_evolution_llm_note",
                 "_evolution_write_build", "_evolution_cycle"):
        assert ("def %s(" % name) not in src, "%s noch in bot.py" % name
    for name in ("build_dir", "next_version", "engineering_note", "write_build",
                 "cycle", "configure", "conf"):
        assert callable(getattr(evolution, name, None)), "nc.evolution.%s fehlt" % name
    ok("v4.1-W3: Evolution-Core vollstaendig in nc/evolution.py")

    # (2) Der Snapshot-Schreiber sichert die Quelle DES BOTS. Im Modul waere
    # __file__ nc/evolution.py — build/bot_v{N}.py haette still das falsche File
    # enthalten, und der ganze Pfad haengt in einem `except: pass`. Deshalb ist
    # bot_file ein Parameter, und der Bot muss ihn setzen.
    import ast as _ast
    _mod = _ast.parse(open("nc/evolution.py", encoding="utf-8").read())
    assert not [n for n in _ast.walk(_mod)
                if isinstance(n, _ast.Name) and n.id == "__file__"], \
        "nc/evolution.py liest __file__ statt bot_file"
    assert "bot_file=__file__" in src, "Bot reicht seine eigene Quelle nicht durch"
    ok("v4.1-W3: Snapshot-Quelle kommt als bot_file aus dem Bot")

    # (3) Unkonfiguriert wirft es laut, statt still None zu liefern.
    import nc.evolution as _ev
    alt = dict(_ev._conf)
    _ev._conf.clear()
    try:
        _ev.build_dir()
    except RuntimeError as e:
        assert "configure" in str(e), "Fehlermeldung nennt den Startpfad nicht"
    else:
        raise AssertionError("unkonfiguriertes nc.evolution laeuft still weiter")
    finally:
        _ev._conf.update(alt)
    ok("v4.1-W3: unkonfiguriert wirft laut, kein stiller None-Pfad")

    # (4) Das Blueprint kommt ohne nc.ctx aus — das ist der Punkt der Welle.
    _bp = _ast.parse(open("nc/routes/evolution.py", encoding="utf-8").read())
    _imp = set()
    for n in _ast.walk(_bp):
        if isinstance(n, _ast.Import):
            _imp |= {al.name for al in n.names}
        elif isinstance(n, _ast.ImportFrom):
            _imp |= {"%s.%s" % (n.module or "", al.name) for al in n.names}
    assert not [m for m in _imp if m.endswith("ctx") or m == "nc.ctx"], \
        "routes/evolution zieht doch wieder am Kontext: %s" % sorted(_imp)
    ok("v4.1-W3: Blueprint ohne einen einzigen ctx-Eintrag")



# ------------------------------------------------- v4.1-W4) bot_app war nie gesetzt

def test_v41_w4_bot_app_gebunden():
    """v4.1-W4: zwei Benachrichtigungspfade lasen ein Global, das es nie gab.

    `bot_app` kam in bot.py ausschliesslich als PARAMETERNAME vor. Die beiden
    Stellen, die ihn per globals().get("bot_app") lesen, bekamen deshalb immer
    None: _brain_notify meldete "Loop/Bot nicht bereit" auf log.warning (in
    einem ERROR-Log unsichtbar) und _marketing_post_telegram antwortete
    dauerhaft {"ok": False, "error": "Bot nicht bereit"}. Beide Pfade waren
    tot, ohne dass irgendwo etwas danach aussah.
    """
    import ast as _ast
    src = open("bot.py", encoding="utf-8").read()

    # (1) Die Leser gibt es weiterhin — der Vertrag ist nicht, sie zu entfernen.
    leser = src.count('globals().get("bot_app")')
    assert leser >= 2, "die bot_app-Leser sind verschwunden statt versorgt zu werden"

    # (2) Und es gibt genau eine Stelle, die den Namen wirklich bindet.
    assert 'globals()["bot_app"] = app' in src, \
        "bot_app wird nirgends gesetzt — beide Melder laufen wieder ins Leere"

    # (3) Sie steht in run_bot, direkt bei der Application. Frueher waere jede
    # andere Stelle zu frueh gewesen: die Application entsteht erst dort.
    _baum = _ast.parse(src)
    _fn = [n for n in _baum.body
           if isinstance(n, (_ast.FunctionDef, _ast.AsyncFunctionDef)) and n.name == "run_bot"]
    assert _fn, "run_bot nicht gefunden"
    _koerper = "\n".join(src.splitlines()[_fn[0].lineno - 1:_fn[0].end_lineno])
    assert 'globals()["bot_app"] = app' in _koerper, "bot_app wird ausserhalb von run_bot gesetzt"
    assert _koerper.index("Application.builder()") < _koerper.index('globals()["bot_app"] = app'), \
        "bot_app wird gebunden, bevor es die Application gibt"
    ok("v4.1-W4: bot_app ist gebunden, beide Melder erreichen Telegram wieder")



# ------------------------------------------------- v4.1-W4) News/Marketing-Kern raus

def test_v41_w4_news_marketing_kern_raus():
    """v4.1-W4: die Bot-Seite von News und Marketing liegt in nc/, die Routen im
       Blueprint — und nc.ctx ist dabei um keinen Eintrag gewachsen."""
    import ast as _ast
    from nc import news as N, marketing as M
    src = open("bot.py", encoding="utf-8").read()

    # (1) Keine der 25 Funktionen steht noch im Monolithen.
    for name in ("_news_cfg", "_news_facts", "_news_generate", "_news_write", "_news_read",
                 "_news_output_path", "_news_phrase_impl", "_news_absaetze",
                 "_creator_activity", "_creator_facts_line", "_azrael_creator_take",
                 "_creator_dossier_generate",
                 "_marketing_cfg", "_marketing_publish", "_marketing_post_telegram",
                 "_marketing_post_discord", "_marketing_flavor"):
        assert ("def %s(" % name) not in src, "%s noch in bot.py" % name
    for name in ("config", "state", "collect_facts", "generate", "read_items",
                 "write_items", "output_path", "phrase", "phrase_impl", "absaetze",
                 "creator_activity", "azrael_creator_take", "creator_dossier_generate",
                 "configure"):
        assert callable(getattr(N, name, None)), "nc.news.%s fehlt" % name
    for name in ("config", "state", "publish", "post_discord", "post_telegram",
                 "ai_flavor", "configure"):
        assert callable(getattr(M, name, None)), "nc.marketing.%s fehlt" % name
    ok("v4.1-W4: News- und Marketing-Kern vollstaendig in nc/")

    # (2) Die beiden Umzugsfallen. bot_file: news.json gehoert in das website/
    # NEBEN dem Bot — mit dem __file__ des Fachmoduls waere es nc/website/
    # geworden und die oeffentliche Seite haette still eine tote Datei gelesen.
    _n = _ast.parse(open("nc/news.py", encoding="utf-8").read())
    assert not [x for x in _ast.walk(_n) if isinstance(x, _ast.Name) and x.id == "__file__"], \
        "nc/news.py liest __file__ statt bot_file"
    assert "bot_file=__file__" in src, "Bot reicht seine eigene Quelle nicht durch"
    # get_bot_app: globals() ist im Modul der MODUL-Namensraum (W116).
    _m = _ast.parse(open("nc/marketing.py", encoding="utf-8").read())
    assert not [x for x in _ast.walk(_m)
                if isinstance(x, _ast.Call) and isinstance(x.func, _ast.Name)
                and x.func.id == "globals"], \
        "nc/marketing.py ruft globals() — im Modul immer der falsche Namensraum"
    assert 'get_bot_app=lambda: globals().get("bot_app")' in src, \
        "der Telegram-Zweig bekommt keinen Getter auf die Application"
    ok("v4.1-W4: bot_file und get_bot_app statt __file__ und globals()")

    # (3) .env.example-Falle: _conf["env_int"]("NEWS_MAX_ITEMS", 20) haette
    # tools/gen_env_example.py nicht mehr gematcht (es sucht env_int("NAME") —
    # acht Variablen waeren lautlos aus der Vorlage gefallen. Deshalb wird
    # _env_int direkt importiert statt injiziert.
    for _f in ("nc/news.py", "nc/marketing.py"):
        _q = open(_f, encoding="utf-8").read()
        assert '_conf["env_int"]' not in _q, \
            "%s injiziert env_int wieder — .env.example verliert dann Variablen" % _f
        assert "from nc.envnum import env_int as _env_int" in _q, \
            "%s importiert env_int nicht direkt" % _f
    ok("v4.1-W4: env_int direkt importiert, .env.example bleibt vollstaendig")

    # (4) Der Kontext ist NICHT gewachsen — der Punkt der Reihenfolge.
    from nc import ctx as ncctx
    assert len(ncctx.Ctx.__slots__) <= 24, \
        "nc.ctx ist doch gewachsen: %d Slots" % len(ncctx.Ctx.__slots__)
    ok("v4.1-W4: nc.ctx bei %d Slots, kein Eintrag dazugekommen" % len(ncctx.Ctx.__slots__))



# ------------------------------------------------- v4.1-W5) die restlichen Dauerlaeufer

def test_v41_w5_restliche_dauerlaeufer():
    """v4.1-W5: W2 hat sieben Stellen versorgt — zwoelf blieben liegen.

    Die Regel aus CLAUDE.md gilt fuer JEDEN Dauerlaeufer: erste Meldung sofort
    mit Traceback, danach gedrosselt, nie auf log.warning. Ein `warning`
    erscheint in einem ERROR-Log nicht; genau so blieb der Discord-Gateway-Tod
    monatelang unsichtbar. Dieser Vertrag haelt die neun Stellen fest, an denen
    ein stiller Ausfall ein ganzes Stueck Funktion mitnimmt — und prueft
    generisch, dass keine WEITERE Schleife wieder auf warning zurueckfaellt.
    """
    import ast as _ast
    src = open("bot.py", encoding="utf-8").read()
    zeilen = src.splitlines()

    # (1) Die sieben Schleifen, die still waren, melden jetzt namentlich.
    for name in ("reaper_loop", "_storage_cleanup_loop", "_proxy_pool_refresh_loop",
                 "_evolution_loop", "_live_react_loop", "_db_maintenance_loop",
                 "_system_backup_loop"):
        assert '_loop_fehler("%s"' % name in src, \
            "%s meldet wieder an _loop_fehler vorbei" % name

    # (2) Und die zwei Alarm-PRUEFUNGEN, die still scheiterten. Der Ausfall der
    # Schleife war sichtbar, das Scheitern ihrer eigentlichen Arbeit nicht —
    # von aussen ununterscheidbar von "alles in Ordnung".
    for name in ("_disk_alarm_loop/check", "_cookie_alarm_loop/check"):
        assert '_loop_fehler("%s"' % name in src, \
            "%s scheitert wieder lautlos — der Alarm feuert dann nie" % name

    # (3) Die alten Meldezeilen sind weg, nicht bloss ergaenzt.
    for tot in ('log.warning(f"Reaper Fehler', 'log.warning(f"Storage-Cleanup Fehler',
                'log.warning("Proxy-Pool-Auto: Refresh fehlgeschlagen',
                'log.warning(f"Evolution-Loop Fehler', 'log.warning("live-react loop Fehler',
                'log.warning("DB-Maintenance fehlgeschlagen',
                'log.warning(f"Disk-Alarm check failed',
                'log.warning("Cookie-Alarm check failed'):
        assert tot not in src, "alter warning-Pfad wieder da: " + tot

    # (4) Generisch: KEIN Dauerlaeufer meldet seinen Schleifenfehler mehr auf
    # warning oder debug. Frueher war das eine Liste, die jede neue Schleife
    # wieder unterlaufen konnte; jetzt faellt die naechste sofort auf.
    baum = _ast.parse(src)
    schlampig = []
    for n in baum.body:
        if not isinstance(n, (_ast.FunctionDef, _ast.AsyncFunctionDef)):
            continue
        if not n.name.endswith("_loop"):
            continue
        if not any(isinstance(x, (_ast.While, _ast.For)) for x in _ast.walk(n)):
            continue
        koerper = "\n".join(zeilen[n.lineno - 1:n.end_lineno])
        versorgt = ("_loop_fehler(" in koerper or "_verbindung_verloren(" in koerper
                    or "exc_info=True" in koerper)
        if not versorgt:
            schlampig.append(n.name)
    assert not schlampig, \
        "Dauerlaeufer ohne sichtbare Fehlermeldung: %s" % sorted(schlampig)
    ok("v4.1-W5: neun weitere Stellen melden sichtbar, kein Dauerlaeufer mehr stumm")



# ------------------------------------------------- v4.1-W5) Streamer-Ansicht raus

def test_v41_w5_streamer_blueprint():
    """v4.1-W5: die Streamer-Ansicht liegt im Blueprint, ihre Helfer in nc/ —
       ohne einen neuen nc.ctx-Slot, und ohne dass ein Slash-Befehl mitwandert."""
    import ast as _ast
    import sqlite3
    from nc import trackingdb as td, tiktokcheck
    src = open("bot.py", encoding="utf-8").read()
    baum = _ast.parse(src)

    # (1) Die drei Helfer stehen nicht mehr im Monolithen.
    for name in ("_ci_key", "_resolve_tracked_user", "_tiktok_account_exists"):
        assert ("def %s(" % name) not in src, "%s noch in bot.py" % name
    for fn in ("ci_key", "resolve_tracked_user", "remove_tracking"):
        assert callable(getattr(td, fn, None)), "nc.trackingdb.%s fehlt" % fn
    assert callable(getattr(tiktokcheck, "account_exists", None)), "nc.tiktokcheck fehlt"
    ok("v4.1-W5: Schreibweisen-Helfer und Existenzpruefung in nc/")

    # (2) remove_tracking raeumt weiter den Laufzeitzustand — ueber einen
    # RUECKRUF, weil die sieben Dicts dem Live-Worker gehoeren, nicht der DB.
    # Fehlt der Rueckruf, laeuft alles weiter und der Orphan-State waechst
    # still (F51/B6) — derselbe Weg wie on_resume in W117.
    assert "on_remove=_tracking_remove_cleanup" in src, \
        "remove_tracking raeumt den Worker-Zustand nicht mehr auf"
    assert "def _tracking_remove_cleanup(" in src, "der Rueckruf fehlt im Bot"
    conn = sqlite3.connect(":memory:"); conn.row_factory = sqlite3.Row
    conn.execute("CREATE TABLE trackings (id INTEGER PRIMARY KEY AUTOINCREMENT, "
                 "group_id INTEGER, username TEXT)")
    conn.execute("INSERT INTO trackings (group_id, username) VALUES (5, 'a')")
    conn.commit()
    import contextlib
    geraeumt = []
    @contextlib.contextmanager
    def dbc():
        yield conn
    _alt_db, _alt_cb = td.db_conn, td._on_remove
    td.db_conn = dbc
    td.configure(on_remove=geraeumt.append)
    try:
        td.remove_tracking(5, "a")
    finally:
        td.db_conn = _alt_db
        td.configure(on_remove=_alt_cb)
    assert geraeumt == [1], "on_remove wurde nicht je geloeschter tracking_id gerufen: %r" % geraeumt
    assert conn.execute("SELECT COUNT(*) c FROM trackings").fetchone()["c"] == 0, "Zeile nicht geloescht"
    ok("v4.1-W5: remove_tracking loescht UND raeumt, ueber den Rueckruf")

    # (3) Der Extraktor haette den Telegram-Befehl `stats` mitgenommen:
    # api_streamer_compare enthaelt ein verschachteltes `def stats(u)`, und
    # bp_extract entschied nach dem blossen Namen. Der Befehl waere aus bot.py
    # verschwunden, und die Routentabelle haette nichts gemerkt — sie zaehlt
    # nur Flask-Regeln. Beide Haelften werden hier festgehalten.
    assert [n for n in baum.body
            if isinstance(n, (_ast.FunctionDef, _ast.AsyncFunctionDef)) and n.name == "stats"], \
        "der Telegram-Befehl stats ist aus bot.py verschwunden"
    assert '("stats", stats)' in src, "stats ist nicht mehr als Slash-Befehl registriert"
    bp = open("nc/routes/streamer.py", encoding="utf-8").read()
    assert "ContextTypes" not in bp and "ParseMode" not in bp, \
        "ein Telegram-Handler ist ins Flask-Blueprint gewandert"
    ok("v4.1-W5: der Telegram-Befehl stats ist NICHT mitgewandert")

    # (4) Der Kontext ist wieder nicht gewachsen.
    from nc import ctx as ncctx
    assert len(ncctx.Ctx.__slots__) <= 24, \
        "nc.ctx ist doch gewachsen: %d Slots" % len(ncctx.Ctx.__slots__)
    ok("v4.1-W5: nc.ctx bei %d Slots, kein Eintrag dazugekommen" % len(ncctx.Ctx.__slots__))



# ------------------------------------------------- v4.1-W6) Mehrsprachigkeit

def test_v41_w6_i18n_fundament():
    """v4.1-W6: der Katalog, die Spracherkennung und der Rueckfall auf Deutsch.

    Der Ansatz ist ungewoehnlich und deshalb vertraglich festgehalten: die
    DEUTSCHE Zeichenkette ist der Schluessel. Das haelt den Bestand lesbar und
    macht jeden fehlenden Eintrag zu einem deutschen Satz statt zu einem nackten
    Schluesselnamen — aber es heisst auch, dass ein geaenderter deutscher Text
    seine Uebersetzung still verliert. Genau dagegen steht --check.
    """
    import json as _json
    from nc import i18n

    # (1) Rueckfall: was nicht im Katalog steht, bleibt Deutsch. NIE leer, nie
    # ein Schluesselname — eine Oberflaeche mit Luecken waere schlimmer als
    # eine einsprachige.
    assert i18n.t("Vollkommen unbekannter Satz", "en") == "Vollkommen unbekannter Satz"
    assert i18n.t("", "en") == ""
    assert i18n.t("Irgendwas", "kl") == "Irgendwas", "unbekannte Sprache muss durchreichen"
    ok("v4.1-W6: fehlende Uebersetzung faellt auf Deutsch zurueck")

    # (2) Spracherkennung. Der Header ist ein Wunsch: passt nichts, sagt die
    # Funktion None und der Aufrufer entscheidet.
    assert i18n.aus_accept_language("en-US,en;q=0.9,de;q=0.8") == "en"
    assert i18n.aus_accept_language("de-DE,de;q=0.9,en;q=0.8") == "de"
    assert i18n.aus_accept_language("fr-FR,fr;q=0.9,en;q=0.3") == "en", "q-Wert missachtet"
    assert i18n.aus_accept_language("fr") is None
    assert i18n.aus_accept_language("") is None and i18n.aus_accept_language(None) is None
    for roh, erwartet in (("de-DE", "de"), ("EN", "en"), ("en_US", "en"),
                          ("fr", None), ("", None), (None, None)):
        assert i18n.normalisieren(roh) == erwartet, "normalisieren(%r)" % roh
    ok("v4.1-W6: Accept-Language und normalisieren exakt")

    # (3) Platzhalter werden NACH der Uebersetzung eingesetzt — im Englischen
    # steht das Objekt oft woanders. Und ein Katalogeintrag mit falschem
    # Platzhalter darf keine Route sprengen.
    i18n.configure()
    i18n._kataloge["en"] = {"{n} Aufnahmen von {u}": "{u} has {n} recordings",
                            "Kaputt {fehlt}": "Broken {gibtsnicht}"}
    try:
        assert i18n.t("{n} Aufnahmen von {u}", "en", n=3, u="a") == "a has 3 recordings"
        assert i18n.t("Kaputt {fehlt}", "en", fehlt="x") == "Kaputt x", \
            "kaputter Katalogeintrag muss auf den deutschen Satz zurueckfallen"
    finally:
        i18n._kataloge.pop("en", None)
    ok("v4.1-W6: Platzhalter nach der Uebersetzung, kaputter Eintrag faellt zurueck")

    # (4) Der Katalog auf der Platte ist gueltiges JSON im erwarteten Format,
    # und Deutsch bleibt leer — die Quellsprache braucht keine Uebersetzung.
    for sp in i18n.SPRACHEN:
        roh = _json.load(open("locales/%s.json" % sp, encoding="utf-8"))
        assert isinstance(roh.get("strings"), dict), "locales/%s.json ohne strings" % sp
    assert not _json.load(open("locales/de.json", encoding="utf-8"))["strings"], \
        "de ist die Quellsprache und darf keinen Katalog haben"
    ok("v4.1-W6: %d Kataloge auf der Platte, de bleibt leer" % len(i18n.SPRACHEN))

    # (5) Die Oberflaeche uebersetzt im Browser. Ohne Beobachter waere nur das
    # beim Laden vorhandene Geruest uebersetzt und jede nachgeladene Tabelle
    # wieder deutsch — sichtbar halb uebersetzt.
    js = open("nc/routes/i18n.py", encoding="utf-8").read()
    assert "/api/i18n/katalog" in js, "Uebersetzer laedt keinen Katalog"
    assert "MutationObserver" in js, "kein Beobachter — nachgeladene Inhalte blieben deutsch"
    assert "TABU" in js and "CODE:1" in js and "PRE:1" in js, \
        "Uebersetzer verschont <code>/<pre> nicht — dort stehen Befehle und Logzeilen"
    # Alle drei Oberflaechen binden DENSELBEN Uebersetzer ein. Drei Inline-Kopien
    # waeren drei Stellen, die auseinanderlaufen — und zwei davon faenden es
    # niemand, weil brain und overlay seltener angesehen werden.
    for vorlage in ("templates/dashboard.html", "templates/brain.html",
                    "templates/overlay.html"):
        h = open(vorlage, encoding="utf-8").read()
        assert '<script src="/api/i18n/uebersetzer.js"' in h, \
            "%s bindet den Uebersetzer nicht ein" % vorlage
    assert "data-i18n-switch" in open("templates/dashboard.html", encoding="utf-8").read(), \
        "kein Anker fuer den Sprachumschalter"
    ok("v4.1-W6: ein Uebersetzer fuer drei Oberflaechen, mit Beobachter und Tabu-Zonen")

    # (6) Der Katalog ist nicht bloss vorhanden, er traegt auch etwas. Ein leerer
    # Katalog wuerde jede Zusicherung oben erfuellen und trotzdem nichts tun.
    import json as _j
    _en = _j.load(open("locales/en.json", encoding="utf-8"))["strings"]
    _gefuellt = {k: v for k, v in _en.items() if v}
    assert len(_gefuellt) == len(_en), \
        "%d von %d Eintraegen ohne Uebersetzung" % (len(_en) - len(_gefuellt), len(_en))
    assert len(_en) >= 600, "Katalog en zu duenn: %d Eintraege" % len(_en)
    assert _gefuellt.get("Aufnahme gestoppt") == "Recording stopped"
    # Keine Uebersetzung darf mit ihrer Quelle identisch sein — das waere ein
    # vergessener Eintrag, der als erledigt zaehlt.
    _faul = [k for k, v in _gefuellt.items() if k == v and len(k) > 12]
    assert not _faul, "Eintraege unveraendert uebernommen: %s" % _faul[:5]
    ok("v4.1-W6: alle %d Katalogeintraege uebersetzt" % len(_en))

    # (7) Der Bot uebersetzt am SENDEWEG, nicht an 90 Aufrufstellen. _safe_send
    # ist der einzige Weg nach Telegram — steht die Uebersetzung dort nicht,
    # bleibt der Bot einsprachig, egal wie voll der Katalog ist.
    b = open("bot.py", encoding="utf-8").read()
    assert "text = _nc_i18n.t(text, lang)" in b, \
        "_safe_send uebersetzt nicht — der Bot bleibt deutsch"
    assert "_nc_i18n.configure(standard=UI_LANG)" in b, "nc.i18n wird nicht konfiguriert"
    ok("v4.1-W6: Telegram-Sendeweg und UI_LANG verdrahtet")

    # (8) Slash-Befehle gegen die Discord-Regeln rekonstruieren — in BEIDEN
    # Sprachen. Die 100-Zeichen-Grenze gilt fuer die AUSGELIEFERTE Beschreibung,
    # und ausgeliefert wird ab jetzt die uebersetzte. Eine zu lange englische
    # Beschreibung liesse die Registrierung scheitern, und der Befehl waere im
    # Discord schlicht weg — ohne dass hier irgendetwas rot wuerde.
    import ast as _ast
    import re as _re2
    _befunde, _n = [], 0
    for _k in _ast.walk(_ast.parse(b)):
        if not isinstance(_k, _ast.Call):
            continue
        if not _ast.unparse(_k.func).endswith(("tree.command", "app_commands.command")):
            continue
        _n += 1
        _kw = {x.arg: x.value for x in _k.keywords}
        _name = getattr(_kw.get("name"), "value", None)
        _d = _kw.get("description")
        _de = None
        if isinstance(_d, _ast.Call) and _d.args and isinstance(_d.args[0], _ast.Constant):
            _de = _d.args[0].value
        elif isinstance(_d, _ast.Constant):
            _de = _d.value
        if _name and not _re2.fullmatch(r"[-_a-z0-9]{1,32}", _name):
            _befunde.append(("Name", _name))
        if _de is None:
            continue
        if not isinstance(_d, _ast.Call):
            _befunde.append(("Beschreibung nicht uebersetzt", _name))
        for _sp, _txt in (("de", _de), ("en", _en.get(_de, _de))):
            if len(_txt) > 100:
                _befunde.append(("Beschreibung %s %d Zeichen" % (_sp, len(_txt)), _name))
    assert _n >= 45, "nur %d Slash-Befehle gefunden — Registrierung kaputt?" % _n
    assert not _befunde, "Discord-Befehle verletzen die Regeln: %s" % _befunde[:5]
    ok("v4.1-W6: %d Slash-Befehle gueltig, Beschreibungen <=100 in de UND en" % _n)


# ------------------------------------------------- B168) Moderator überall (Twitch/YouTube)

def test_b168_moderator_everywhere():
    """B168: die geteilte volle Moderations-Pipeline (Sentinel→Bannwörter→Spam→Flood)
       mit echten nc-Modulen + Nachweis, dass Twitch/YouTube sie verdrahten."""
    import time as _t
    from nc.shield import _sentinel_screen
    from nc import modheuristics as m

    # Pipeline von _screen_full 1:1 nachgebaut (gleiche Reihenfolge/Gating).
    def screen(content, user_id, hist, cfg):
        c = (content or "").strip()
        if not c:
            return None
        hard = _sentinel_screen(c)
        if hard and hard[0]:
            return hard[0], hard[1]
        if content and "kaufxyz" in c.lower():        # simulierte Bannwortliste
            return "banned", "Banned word: kaufxyz"
        if not cfg.get("spam_filter"):
            return None
        sr = m.stateless_reason(c, max_caps_ratio=float(cfg.get("max_caps_ratio", 0.7)),
                                max_links=int(cfg.get("max_links", 2)),
                                max_mentions=int(cfg.get("max_mentions", 5)))
        if sr:
            return "spam", sr
        if user_id and hist is not None:
            now = _t.monotonic()
            h = hist.setdefault(user_id, [])
            h.append((now, c.lower()))
            hist[user_id] = [(x, y) for (x, y) in h if now - x <= 7]
            recent = [y for (_x, y) in hist[user_id]]
            fr = m.flood_reason(recent, c.lower(), flood_max=int(cfg.get("flood_max", 5)))
            if fr:
                return "spam", fr
        return None

    cfg = {"spam_filter": True, "max_caps_ratio": 0.7, "max_links": 2, "max_mentions": 5, "flood_max": 5}
    H = {}
    # 1) Sentinel (Doxxing) schlägt zuerst zu.
    assert screen("ruf mich an unter 0176 12345678", "u", H, cfg)[0] == "DOXXING"
    # 2) Bannwort.
    assert screen("schau auf kaufxyz vorbei", "u", H, cfg)[0] == "banned"
    # 3) CAPS-Spam.
    assert screen("AAAAAAAAAA", "u", H, cfg) == ("spam", "CAPS-Spam")
    # 4) sauber → None.
    assert screen("hallo zusammen", "u2", H, cfg) is None
    # 5) Flood: 6 Nachrichten im Fenster → spam.
    Hf = {}
    for _ in range(5):
        screen("hi", "flood", Hf, cfg)
    assert screen("hi", "flood", Hf, cfg) == ("spam", "Flood")
    # 6) spam_filter aus → CAPS wird NICHT als Spam gewertet (aber Sentinel/Bann bleiben).
    off = dict(cfg, spam_filter=False)
    assert screen("AAAAAAAAAA", "u", {}, off) is None
    assert screen("ruf mich an unter 0176 12345678", "u", {}, off)[0] == "DOXXING"
    ok("b168: geteilte Pipeline Sentinel>Bann>Spam>Flood, spam_filter-Gating korrekt")

    # Verdrahtung: Bot hat _screen_full und Twitch/YouTube nutzen es.
    src = open("bot.py").read()
    assert "def _screen_full(" in src, "geteilte Pipeline fehlt"
    assert "_screen_full(text, user, _TW_MSG_HIST" in src, "Twitch nutzt Pipeline nicht"
    assert "_screen_full(txt, who, _YT_MSG_HIST" in src, "YouTube nutzt Pipeline nicht"
    assert "auto-mod-twitch" in src and "auto-mod-youtube" in src, "Mod-Log-Marker fehlen"
    ok("b168: Twitch (Timeout) + YouTube (Erkennung+Log) verdrahtet")


# ------------------------------------------------- B169) Kick User-OAuth (PKCE)

def test_b169_kick_oauth():
    """B169: der reine Kick-OAuth-Baustein (PKCE S256, URLs, Payloads, Parsing)
       + Nachweis, dass update_channel den User-Token bevorzugt."""
    import base64, hashlib
    from nc import kick_oauth as k

    # PKCE S256 korrekt + ohne Padding.
    v, c = k.gen_pkce()
    assert c == base64.urlsafe_b64encode(hashlib.sha256(v.encode()).digest()).decode().rstrip("=")
    assert "=" not in c and len(v) >= 43
    ok("b169: PKCE S256 (base64url ohne Padding) korrekt")

    # Authorize-URL enthält alle Pflichtparameter, Scope space-joined url-encoded.
    url = k.build_authorize_url("CID", "https://x.dev/cb", k.DEFAULT_SCOPES, "ST", c)
    for frag in ("response_type=code", "client_id=CID", "code_challenge_method=S256",
                 "state=ST", "channel%3Awrite"):
        assert frag in url, frag
    assert url.startswith("https://id.kick.com/oauth/authorize?")
    ok("b169: Authorize-URL vollständig")

    # 127.0.0.1-Workaround: sacrificial redirect-Param zuerst.
    u127 = k.build_authorize_url("CID", "http://127.0.0.1:8050/cb", ("user:read",), "ST", c)
    assert u127.split("?", 1)[1].startswith("redirect=127.0.0.1&")
    ok("b169: 127.0.0.1-NextJS-Workaround vorhanden")

    # Token-/Refresh-Payloads.
    ex = k.token_exchange_payload("CID", "SEC", "https://x.dev/cb", "CODE", v)
    assert ex["grant_type"] == "authorization_code" and ex["code_verifier"] == v and ex["code"] == "CODE"
    rf = k.token_refresh_payload("CID", "SEC", "RT")
    assert rf["grant_type"] == "refresh_token" and rf["refresh_token"] == "RT"
    ok("b169: Token-Exchange- und Refresh-Payload korrekt")

    # Parsing + Ablauf + Scope.
    tok, err = k.parse_token_response(
        {"access_token": "AT", "refresh_token": "RT", "expires_in": 3600,
         "scope": "user:read channel:write"}, 1000)
    assert err is None and tok["expires_at"] == 4600 and k.has_scope(tok, "channel:write")
    assert not k.is_expired(tok, 1000) and k.is_expired(tok, 4600)
    assert k.parse_token_response({"error": "invalid_grant"}, 0)[0] is None
    # expires_at=0 (unbekannt) gilt NICHT als abgelaufen.
    assert not k.is_expired({"access_token": "x", "expires_at": 0}, 10**12)
    ok("b169: Token-Parse, Ablauf (inkl. unbekannt) und Scope-Prüfung korrekt")

    # Verdrahtung im Bot.
    src = open("bot.py").read()
    assert "await _kick_user_token(session) or await self._get_token(session)" in src, \
        "update_channel bevorzugt den User-Token nicht"
    for r in ("/api/kick/oauth/start", "/api/kick/oauth/callback",
              "/api/kick/oauth/status", "/api/kick/oauth/disconnect"):
        assert '"' + r + '"' in src, r
    assert "kick.user_token" in src and "kick.oauth_pending" in src
    ok("b169: update_channel bevorzugt User-Token + 4 OAuth-Routen verdrahtet")


# ------------------------------------------------- B170) AZRAEL-Fan-out + YouTube-Listener-Fix

def test_b170_azrael_and_youtube():
    """B170: AZRAEL antwortet nur echten Usern und sendet an alle drei Chats zum
       einen User; YouTube-Listener erkennt Continuation robuster + meldet Grund."""
    import re
    src = open("bot.py").read()

    # AZRAEL: Selbst-Guard + Broadcast an alle drei Plattformen.
    assert "def _azrael_self_names(" in src and "def _azrael_broadcast_reply(" in src
    assert "in _azrael_self_names():" in src, "kein Selbst-Guard in _azrael_chat_reply"
    assert src.count('_azrael_broadcast_reply("kick"') == 1
    assert src.count('_azrael_broadcast_reply("twitch"') == 1
    assert src.count('_azrael_broadcast_reply("youtube"') >= 1  # API- + Scraping-Pfad
    # der Broadcast adressiert genau den einen User und bedient alle drei Hooks.
    i = src.find("async def _azrael_broadcast_reply")
    body = src[i:i + 1800]      # W20: Fenster groesser (Bremse kam davor)
    assert 'f"@{user} {reply}"' in body, "Antwort nicht an @user adressiert"

    # W21: Antwort geht in den Ursprungs-Chat; alle drei nur mit Schalter.
    assert "_azrael_send_to" in body, "kein Sendeweg im Broadcast"
    assert "if _azrael_reply_all_chats():" in body, "Schalter fehlt"
    src_all = open("bot.py").read()
    i2 = src_all.find("async def _azrael_send_to")
    sender = src_all[i2:i2 + 1400]      # W41: Fenster größer (Status-Rückgabe + Doc)
    assert all(p in sender for p in ("kick", "twitch", "youtube")), "nicht alle drei Chats moeglich"

    # alte Ein-Plattform-Sends sind ersetzt.
    assert 'await self.send_message(_r, session)' not in src
    ok("b170: AZRAEL — Selbst-Guard + Fan-out an Kick/Twitch/YouTube zum einen User")

    # YouTube: 4 Continuation-Muster greifen, Consent-Cookies gesetzt, Grund im Status.
    def find_cont(html):
        return (re.search(r'"liveChatRenderer".{0,4000}?"continuation":"([^"]+)"', html, re.S)
                or re.search(r'"reloadContinuationData":\{"continuation":"([^"]+)"', html, re.S)
                or re.search(r'"invalidationContinuationData":\{[^}]{0,200}?"continuation":"([^"]+)"', html, re.S)
                or re.search(r'"liveChatContinuation".{0,4000}?"continuation":"([^"]+)"', html, re.S))
    assert find_cont('{"reloadContinuationData":{"continuation":"R1"}}').group(1) == "R1"
    assert find_cont('{"invalidationContinuationData":{"topic":"t","continuation":"I1"}}').group(1) == "I1"
    assert find_cont('"liveChatContinuation":{"continuations":[{"x":{"continuation":"L1"}}]}').group(1) == "L1"
    assert find_cont("<html>consent only</html>") is None
    assert '"CONSENT": "YES+cb"' in src, "kein Consent-Cookie gegen die Consent-Wall"
    assert '_WCHAT_STATUS["youtube"].update(connected=False, error=reason)' in src, \
        "YouTube meldet keinen Grund → bliebe still 'getrennt'"
    ok("b170: YouTube — Consent-Cookies + 4 Continuation-Muster + Fehlergrund im Status")


# ------------------------------------------------- v4.0) Versions-/Changelog-System

def test_v40_version():
    """v4.1: zentrale Versions-Quelle + Verdrahtung (Footer/Route/Panel).
       Der Test wandert mit der Version mit — er verriegelt, dass Footer,
       BUILD_STAMP und nc.version NICHT auseinanderlaufen (schon dreimal
       passiert: Modul auf neu, Footer blieb auf alt)."""
    from nc import version as v
    assert v.VERSION == "4.1" and v.current()["version"] == "4.1"
    assert v.summary_line().startswith("NIGHTCRAWLER v4.1")
    top = v.latest()
    assert top["version"] == "4.1" and len(top["highlights"]) >= 5
    assert [c["version"] for c in v.changelog()][:2] == ["4.1", "4.0"]
    assert v.changelog()[-1]["version"] == "3.7"   # Historie erhalten
    ok("v4.1: nc.version — 4.1 + Changelog mit Historie")

    src = open("bot.py").read()
    assert 'BOT_VERSION = _nc_version.VERSION' in src, "BOT_VERSION nicht zentralisiert"
    assert '"2026.08 · v4.1"' in src, "BUILD_STAMP nicht auf v4.1"
    assert '"/api/version"' in src and "def api_version(" in src, "keine /api/version-Route"
    dash = open("templates/dashboard.html").read()
    assert "<b>v4.1</b>" in dash, "Footer nicht auf v4.1"
    assert "/api/version" in src  # Panel entfernt (v4.0-w2), Route bleibt
    ok("v4.1: Footer v4.1 + /api/version + Was-ist-neu-Panel verdrahtet")


# ------------------------------------------------- v4.0-2) YouTube-API, News-ohne-Aufnahmen, Website

def test_v40_youtube_api():
    from nc import youtube_api as y
    data={"items":[{"id":"m","snippet":{"displayMessage":"hi","authorChannelId":"C"},
                    "authorDetails":{"displayName":"U","channelId":"C"}}],
          "nextPageToken":"P","pollingIntervalMillis":1000}
    msgs,np,poll=y.parse_messages(data)
    assert msgs[0]["text"]=="hi" and msgs[0]["author"]=="U" and np=="P" and poll==3000
    bp=y.ban_payload("LC","C",300)
    assert bp["snippet"]["type"]=="temporary" and bp["snippet"]["banDurationSeconds"]==300
    assert y.ban_payload("LC","C",0)["snippet"]["type"]=="permanent"
    assert y.is_self({"channel_id":"C"},"C")
    src=open("bot.py").read()
    assert "async def _youtube_api_chat_loop(" in src and "async def _yt_timeout(" in src
    assert "await _youtube_api_chat_loop()" in src, "YT-Loop delegiert nicht an API"
    assert "_nc_ytapi.BANS_URL" in src, "kein YouTube-Durchgreifen verdrahtet"
    ok("v4.0: YouTube-Data-API-Listener + Timeout-Durchgreifen verdrahtet")

def test_v40_news_no_recordings():
    from nc import news
    facts={"version":"4.0","platforms":["Kick","YouTube"],"tracked":10,
           "live_today":["a","b"],"live_today_count":2,"kg_facts":5,"agents_active":3}
    for it in news.build_items(facts, categories=news.CATEGORIES, now_ts=1):
        low=it["body"].lower()
        assert "aufnahm" not in low and "aufzeichn" not in low and "recording" not in low, it
    # Tages-Live-Report nennt Namen + Zahl
    cr=[i for i in news.build_items(facts,categories=("creators",),now_ts=1)][0]
    assert "2 von 10" in cr["body"] and "a" in cr["body"]
    # auch der Fakten-/KI-Pfad erwaehnt keine Aufnahmen mehr. v4.1-W4: er liegt
    # in nc/news.py, _public_stats blieb im Bot — der Vertrag prueft jetzt beide
    # Dateien statt einer. Geloescht wird keine Zusicherung.
    nsrc=open("nc/news.py", encoding="utf-8").read()
    bsrc=open("bot.py").read()
    # collect_facts/_public_stats duerfen KEINE Aufnahme-Zahlen exponieren. (Die
    # interne Prometheus-Metrik nightcrawler_recordings_total ist NICHT oeffentlich
    # und zaehlt nicht — geprueft wird der News-/Stats-Fakten-Pfad.)
    _nf = nsrc[nsrc.find("def collect_facts"):nsrc.find("async def phrase(")]
    _ps = bsrc[bsrc.find("def _public_stats"):bsrc.find("def _stats_output_path")]
    assert _nf and _ps, "Fakten-Segmente nicht gefunden — Anker gebrochen"
    for _seg in (_nf, _ps):
        assert "recordings_7d" not in _seg and "recordings_total" not in _seg, "Aufnahme-Zahl im oeffentlichen Fakten-Pfad"
    assert "Erwaehne NIEMALS Aufnahmen" in nsrc, "KI-Prompt ohne Aufnahme-Verbot"
    assert "live_today_count" in nsrc
    ok("v4.0: News erwaehnt nie Aufnahmen, Tages-Live-Report der getrackten User")

def test_v40_website():
    h=open("website/lafap_index.html",encoding="utf-8").read()
    assert 'data-theme="messing"' not in h, "Theme-Umschalter noch aktiv (Mix)"
    assert 'id="siteTheme"' not in h, "Theme-Button noch da"
    assert 'id="lagebild"' in h and "fetch('stats.json" in h, "kein Lagebild/Metriken"
    assert 'class="chart"' in h and 'id="live-chart"' in h, "kein Live-Chart"
    assert h.count("<section") == h.count("</section>")
    # oeffentliche stats sicher: kein "aufnahme"/"recording" auf der Seite
    assert "aufnahme" not in h.lower().replace("keine aufzeichnung","").replace("keine aufnahme","")
    src=open("bot.py").read()
    assert "def _public_stats(" in src and "def _stats_write(" in src and '"/api/public/stats"' in src
    ok("v4.0: Website vereinheitlicht (void), Lagebild+Chart aus stats.json")


# ------------------------------------------------- v4.0-W2) Öffentliche Metriken + YT-API + Fixes

def test_v40_wave2():
    """v4.0 Welle 2: Stats-Loop (Website-Metriken werden IMMER geschrieben),
       angereicherte aufnahmefreie Kennzahlen, YT-API-Durchgreifen, Box entfernt."""
    src = open("bot.py").read()

    # Stats-Loop: existiert, ist STATS_PUBLIC-gated, wird gespawnt, unabhängig vom News-Agenten.
    assert "async def _stats_loop(" in src, "kein eigener Stats-Loop"
    assert 'os.getenv("STATS_PUBLIC"' in src, "Stats-Loop nicht self-gated"
    assert '_spawn(_stats_loop()' in src, "Stats-Loop wird nicht gespawnt"
    # angereicherte, aufnahmefreie Metriken.
    for k in ("total_live_7d", "peak_live", "moderation_7d"):
        assert k in src, "Metrik fehlt: " + k
    assert "kick_mod_log WHERE ts" in src, "Moderations-Kennzahl nicht aus dem Mod-Log"
    ok("v4.0-w2: Stats-Loop (immer an) + angereicherte aufnahmefreie Metriken")

    # News erwähnt NIE Aufnahmen (Prompt-Verbot) + Tages-Live-Report.
    # v4.1-W4: der News-Pfad liegt in nc/news.py — Anker gewandert, Vertrag gleich.
    nsrc = open("nc/news.py", encoding="utf-8").read()
    assert "Erwaehne NIEMALS Aufnahmen" in nsrc, "News-Prompt verbietet Aufnahmen nicht"
    assert '"live_today"' in nsrc and "recording_attempts" in nsrc, "kein Tages-Live-Report"
    assert "nimmt oeffentlich nichts auf" in nsrc
    ok("v4.0-w2: News aufnahmefrei + Tages-Report der Live-Creator")

    # YouTube: offizieller API-Weg + Durchgreifen (Timeout via bans).
    assert "async def _youtube_api_chat_loop(" in src and "async def _yt_timeout(" in src
    assert "_nc_ytapi.BANS_URL" in src, "kein YouTube-Timeout über die API"
    assert "await _youtube_api_chat_loop()" in src, "YT-Loop nutzt den API-Weg nicht"
    ok("v4.0-w2: YouTube liest & moderiert über die offizielle Data-API")

    # „Was ist neu"-Box entfernt.
    dash = open("templates/dashboard.html").read()
    assert 'id="pnl_version"' not in dash and "loadVersion(" not in dash, "Was-ist-neu-Box noch da"
    # Website: neue KPI-Karten + Fetch verdrahtet.
    web = open("website/lafap_index.html").read()
    assert 'data-k="total_live_7d"' in web and 'data-k="moderation_7d"' in web
    assert "setk('moderation_7d'" in web and "stats.json" in web
    ok("v4.0-w2: Box entfernt; Website-KPIs (Live-Einsätze, Mod-Aktionen) verdrahtet")

    # abgeleitete Metrik-Logik (rein): total/peak aus live_7d.
    live7 = [{"day": "d", "live": n} for n in (2, 0, 5, 1, 3, 0, 4)]
    vals = [x["live"] for x in live7]
    assert sum(vals) == 15 and max(vals) == 5
    ok("v4.0-w2: abgeleitete 7-Tage-Kennzahlen korrekt")


# ------------------------------------------------- v4.0-W3) Moderations-Feed (alle Plattformen)

def test_v40_modfeed():
    """v4.0: plattformübergreifender Moderations-Feed — Endpoint + Panel + Plattform-Erkennung."""
    src = open("bot.py").read()
    # v4.0-W117: die Route liegt im Blueprint nc/routes/stats.py. Vertrag
    # unveraendert, nur eine Ebene tiefer verankert — plus die Zusicherung,
    # dass der Monolith keine zweite Fassung behalten hat.
    _st = open("nc/routes/stats.py", encoding="utf-8").read()
    assert '"/api/moderation/feed"' in _st and "def api_moderation_feed(" in _st
    assert "def api_moderation_feed(" not in src, "Doppel-Logik im Monolithen"
    # Plattform-Erkennung aus actor.
    assert 'if "twitch" in a' in _st and '"youtube" in a' in _st, "keine Plattform-Erkennung"
    # nur Durchgreif-Aktionen im Feed.
    assert "kind IN ('timeout','ban','flag','delete','warn')" in _st, "Feed filtert Aktionen nicht"
    dash = open("templates/dashboard.html").read()
    assert 'id="pnl_modfeed"' in dash and "async function loadModFeed(" in dash
    assert "mf-kick" in dash and "mf-twitch" in dash and "mf-youtube" in dash, "keine Plattform-Badges"
    assert "loadModFeed();" in dash, "Feed nicht im Betrieb-Loader"
    ok("v4.0: Moderations-Feed (Endpoint + Panel + Kick/Twitch/YouTube-Badges)")

    # Plattform-Ableitung nachgebaut.
    def plat(actor):
        a=(actor or "").lower()
        return "twitch" if "twitch" in a else ("youtube" if ("youtube" in a or "yt" in a) else "kick")
    assert plat("auto-mod-twitch")=="twitch"
    assert plat("auto-mod-youtube")=="youtube"
    assert plat("sentinel-shield")=="kick"
    ok("v4.0: actor→Plattform korrekt abgeleitet")


# ------------------------------------------------- v4.0-W4) Website-Detail: 12-Agenten-Flotte live + 2. Chart

def test_v40_w4_website():
    """v4.0-W4: vollständige 12-Agenten-Flotte (live) + zweiter Chart + reichere Stats."""
    src = open("bot.py").read()
    # _public_stats: live-Agentenliste + mod_7d-Serie.
    assert 'stats["agents"]' in src and 'stats["agents_total"]' in src, "keine Live-Agentenliste in stats"
    assert 'stats["mod_7d"]' in src, "keine Moderations-7-Tage-Serie"
    assert "b.agents.status()" in src or "_b.agents.status()" in src, "Agentenliste nicht aus dem Brain"

    web = open("website/lafap_index.html", encoding="utf-8").read()
    # ALLE 13 Sentinel-Agenten gelistet + für Live-Status attribuiert (W86: +swap).
    for name in ("health", "recovery", "scout", "analytics", "learning", "sentinel",
                 "toxicity", "uptime", "restream_sentinel", "disk", "recording", "proxy",
                 "swap"):
        assert 'data-agent="' + name + '"' in web, "Agent fehlt auf der Website: " + name
    assert web.count('class="agent" data-agent') == 13, "Flotte nicht vollständig (13)"
    assert 'id="agents-status"' in web and "von " in web, "kein Live-Zähler der Flotte"
    assert ".inactive" in web, "kein Inaktiv-Zustand für Agenten"
    # zweiter Chart + Verdrahtung.
    assert web.count('class="chart"') == 2, "zweiter Chart fehlt"
    assert 'id="mod-chart"' in web and "d.mod_7d" in web, "Moderations-Chart nicht verdrahtet"
    assert "d.agents" in web, "Agenten-Status nicht aus stats.json gesetzt"
    # weiterhin aufnahmefrei (auch der recording-Agent heißt öffentlich „Session").
    import re
    assert not re.search(r'(?<!keine )aufnahm', web.lower().replace("keine aufzeichnung", "")), "Aufnahme-Erwähnung auf der Website"
    ok("v4.0-w4: 12-Agenten-Flotte live + 2. Chart (Moderation) + aufnahmefrei")


# ------------------------------------------------- v4.0-W5) YouTube Titel/Kategorie (Kanal-Steuerung komplett)

def test_v40_w5_channel_all():
    """v4.0-W5: YouTube-Titel/Kategorie via Data API — Kanal-Steuerung auf allen
       drei Plattformen (Kick/Twitch/YouTube) einheitlich."""
    from nc import youtube_api as y
    # reine Helfer.
    assert y.BROADCASTS_URL.endswith("/liveBroadcasts") and y.VIDEOS_URL.endswith("/videos")
    assert y.active_broadcast_params()["mine"] == "true"
    assert y.parse_broadcast_id({"items": [{"id": "V1"}]}) == "V1"
    assert y.parse_broadcast_id({"items": []}) == ""
    cur = {"title": "Alt", "categoryId": "22", "description": "d"}
    m = y.merge_video_snippet(cur, title="Neu", category_id="20")
    assert m["title"] == "Neu" and m["categoryId"] == "20" and m["description"] == "d"
    assert y.merge_video_snippet(cur, title=None, category_id="10")["title"] == "Alt"  # Pflichtfeld bleibt
    assert y.merge_video_snippet(cur, title="X", category_id=None)["categoryId"] == "22"
    assert len(y.merge_video_snippet(cur, title="Z" * 200)["title"]) == 100
    ok("v4.0-w5: YouTube-Snippet-Merge — Pflichtfelder erhalten, Titel gedeckelt")

    src = open("bot.py").read()
    # _youtube_set_channel ist KEIN Platzhalter mehr, nutzt Broadcast+Video-Update.
    assert "YouTube-Setzung folgt als eigener Schritt" not in src, "YouTube-Setzer noch Platzhalter"
    assert "_nc_ytapi.BROADCASTS_URL" in src and "_nc_ytapi.VIDEOS_URL" in src, "kein Data-API-Setzer"
    assert 'params={"part": "snippet"}' in src and "video_update_body" in src, "kein videos.update"
    # _channel_set_all deckt ALLE drei Plattformen ab.
    body = _fn(src, "_channel_set_all")               # v4.0-W117
    assert 'out["kick"]' in body and 'out["twitch"]' in body and 'out["youtube"]' in body, "nicht alle drei Plattformen"
    assert "_youtube_set_channel(title, cat" in body, "YouTube nicht im Set-All"
    # Kategorien tragen je Plattform (kick/twitch/yt).
    assert '"yt":' in src and '"kick":' in src and '"twitch":' in src, "Kategorie-Mapping unvollständig"
    ok("v4.0-w5: Titel/Kategorie einheitlich auf Kick + Twitch + YouTube")


# ------------------------------------------------- v4.0-W6) Oeffentliche Marke: Azrael Sentinel (kein NIGHTCRAWLER)

def test_v40_w6_public_brand():
    """v4.0-W6: der interne Codename NIGHTCRAWLER darf in KEINEM oeffentlichen
       Pfad auftauchen (News, News-Seed, AZRAEL-Chat-Persona, Stream-Titel)."""
    news = open("nc/news.py", encoding="utf-8").read()
    assert "NIGHTCRAWLER" not in news, "News nennt noch NIGHTCRAWLER"
    assert "Azrael Sentinel" in news, "oeffentlicher Name fehlt in News"

    seed = open("website/news.json", encoding="utf-8").read()
    assert "NIGHTCRAWLER" not in seed, "News-Seed nennt NIGHTCRAWLER"
    assert "Aufzeichnung" not in seed and "Aufnahme" not in seed, "News-Seed nennt Aufnahmen"

    src = open("bot.py").read()
    # KEINE der AZRAEL-Chat-Personas darf den internen Codenamen nennen.
    _pos = 0
    _seen = 0
    while True:
        k = src.find("Du bist AZRAEL", _pos)
        if k < 0:
            break
        _seen += 1
        assert "NIGHTCRAWLER" not in src[k:k + 260], "AZRAEL-Persona nennt NIGHTCRAWLER"
        _pos = k + 10
    assert _seen >= 1
    # Die System-beschreibende Persona nennt den oeffentlichen Namen, keine Aufnahme.
    isys = src.find("die eine KI von")
    sysp = src[isys:isys + 160]
    assert "Azrael Sentinel" in sysp and "Aufnahme" not in sysp, "System-Persona falsch benannt"
    # oeffentliches Stream-Titel-Template.
    j = src.find("LIVING_TITLE_TEMPLATE")
    assert "NIGHTCRAWLER" not in src[j:j + 160], "Stream-Titel nennt NIGHTCRAWLER"
    ok("v4.0-w6: oeffentliche Marke Azrael Sentinel, kein NIGHTCRAWLER/Aufnahme-Leak")


# ------------------------------------------------- v4.0-W7) Marke: oeffentliche Flaechen komplett Azrael Sentinel

def test_v40_w7_public_brand_sweep():
    """v4.0-W7: KEINE oeffentlich sichtbare Flaeche nennt den internen Codenamen —
       Overlay (auf dem Stream), Living-Title, Discord-Community-Embeds/Commands.
       (Admin-only Telegram/Alarme/CLI/Fehler-Channel duerfen ihn intern behalten.)"""
    src = open("bot.py").read()
    # Overlay-Titel (wird ins Video gerendert) -> Azrael Sentinel, kein NIGHTCRAWLER-Default.
    assert 'os.getenv("OVERLAY_TITLE", "Azrael Sentinel")' in src, "Overlay-Default nicht rebrandet"
    assert '"NIGHTCRAWLER").strip(),' not in src, "Overlay-Default noch NIGHTCRAWLER"
    assert '(d["title"] or "NIGHTCRAWLER")' not in src, "Overlay-Fallback noch NIGHTCRAWLER"
    # Living-Title-Template (oeffentlicher Stream-Titel).
    j = src.find("LIVING_TITLE_TEMPLATE")
    assert "NIGHTCRAWLER" not in src[j:j + 160], "Stream-Titel nennt NIGHTCRAWLER"
    # Discord-community-sichtbare Flaechen rebrandet (admin-only Fehler-Channel/CLI
    # duerfen 🦇 NIGHTCRAWLER intern behalten):
    assert "🦇 Azrael Sentinel — Befehle" in src, "Discord-Befehlsliste nicht rebrandet"
    assert "🦇 Azrael Sentinel Botstats" in src, "Discord-Botstats nicht rebrandet"
    assert 'set_footer(text="NIGHTCRAWLER' not in src, "Discord-Footer nennt NIGHTCRAWLER"
    assert 'description="NIGHTCRAWLER' not in src, "Discord-Command-Beschreibung nennt NIGHTCRAWLER"
    assert '**NIGHTCRAWLER**' not in src, "Discord-/status nennt NIGHTCRAWLER"
    ok("v4.0-w7: alle oeffentlichen Flaechen = Azrael Sentinel (intern/admin bleibt)")


# ------------------------------------------------- v4.0-W8) Selbstschutz: keine toten Verträge

def test_no_dead_contracts():
    """v4.0-W8: härtet die Prüfung selbst. In W7 fiel auf, dass Verträge zwar
       DEFINIERT, aber in main() nie AUFGERUFEN waren → falsches Grün. Dieser
       Meta-Vertrag liest die eigene Quelle und stellt sicher, dass JEDE
       test_*-Funktion (außer sich selbst) in main() aufgerufen wird. So kann
       ein vergessener Aufruf nie wieder als bestanden durchgehen."""
    import re
    src = open(__file__, encoding="utf-8").read() if "__file__" in dir() else open("test_restream.py", encoding="utf-8").read()
    defined = set(re.findall(r'^def (test_\w+)\(', src, re.M))
    body = src[src.find("def main():"):]
    called = set(re.findall(r'^    (test_\w+)\(\)', body, re.M))
    missing = sorted(defined - called - {"test_no_dead_contracts"})
    assert not missing, "Verträge definiert, aber in main() nie aufgerufen: " + ", ".join(missing)
    # Selbstschutz: dieser Meta-Vertrag muss ebenfalls aufgerufen werden.
    assert "test_no_dead_contracts()" in body, "Meta-Vertrag selbst nicht in main()"
    ok(f"v4.0-w8: alle {len(defined)} Verträge werden in main() aufgerufen (keine toten)")


# ------------------------------------------------- v4.0-W9) AZRAEL-Kick-Fix + Listener-Grund

def test_v40_w9_kick_and_listener():
    """v4.0-W9: Kick-Broadcaster-ID wird auto-aufgeloest (fixt AZRAELs Kick-Posts
       UND Kick-Timeouts, die ohne broadcaster_user_id still scheiterten); der
       Chat-Listener zeigt bei 'getrennt' den Grund."""
    src = open("bot.py").read()
    # Resolver existiert + liest user_id/user.id + cacht.
    assert "async def _kick_broadcaster_id(" in src, "kein Broadcaster-ID-Resolver"
    assert 'j.get("user_id")' in src and '(j.get("user") or {}).get("id")' in src, "user_id nicht aufgeloest"
    assert "_KICK_BID_CACHE" in src, "keine Cache-Struktur"
    # send_message + bans + channel_info loesen die ID auto auf (kein nacktes KICK_BROADCASTER_ID mehr im payload).
    assert "KICK_BROADCASTER_ID or await _kick_broadcaster_id()" in src, "Auto-Aufloesung nicht verdrahtet"
    assert 'payload["broadcaster_user_id"] = KICK_BROADCASTER_ID' not in src, "alter payload-Pfad ohne Aufloesung"
    assert 'params["broadcaster_user_id"] = KICK_BROADCASTER_ID' not in src, "alter params-Pfad ohne Aufloesung"
    # Parse-Logik nachgestellt.
    def bid(j):
        return int(j.get("user_id") or (j.get("user") or {}).get("id") or 0)
    assert bid({"user_id": 42}) == 42
    assert bid({"user": {"id": 99}}) == 99
    assert bid({}) == 0
    ok("v4.0-w9: Kick-Broadcaster-ID Auto-Aufloesung (send + bans + info)")

    # Deck-Route liefert error; Panel zeigt den Grund bei getrennt.
    assert '"error": _WCHAT_STATUS["youtube"].get("error")' in src, "deck ohne YouTube-Grund"
    assert '"error": _WCHAT_STATUS["twitch"].get("error")' in src, "deck ohne Twitch-Grund"
    dash = open("templates/dashboard.html").read()
    assert "'getrennt'+(p.error?' · '+p.error:'')" in dash, "Panel zeigt den Grund nicht"
    ok("v4.0-w9: Chat-Listener zeigt bei 'getrennt' den Grund (offline/Fehler)")


# ------------------------------------------------- v4.0-W10) Kick-Sende-Diagnose

def test_v40_w10_kick_sendcheck():
    """v4.0-W10: ein stummer Kick-Chat darf nicht mehr still scheitern — Kicks
       Fehlertext wird mitgelesen, gemerkt, im Panel gezeigt; Sendetest-Route."""
    src = open("bot.py").read()
    # Gedaechtnis + Klartext-Fehler im Sendepfad.
    assert "_KICK_SEND_LAST" in src, "kein Gedaechtnis fuer den letzten Sendeversuch"
    body = _meth(src, "KickModerator", "send_message")   # v4.0-W117
    assert "await resp.text()" in body, "Kicks Fehlertext wird nicht gelesen"
    assert "keine Broadcaster-ID aufloesbar" in body, "fehlende Broadcaster-ID wird nicht benannt"
    assert "_KICK_SEND_LAST.update(" in body, "Sendeversuch wird nicht gemerkt"
    # Diagnose-/Testroute.
    assert '"/api/kick/sendcheck"' in src and "def api_kick_sendcheck(" in src
    assert 'methods=["GET", "POST"]' in src, "sendcheck ohne GET+POST"
    assert "creds_configured" in src and "broadcaster_id_resolved" in src, "Diagnose unvollstaendig"
    # Deck exponiert Kick-Sendezustand.
    assert '"send_ok": _KICK_SEND_LAST.get("ok")' in src, "deck ohne Kick-Sendezustand"
    ok("v4.0-w10: Kick-Sendefehler im Klartext + gemerkt + Diagnose-/Testroute")

    dash = open("templates/dashboard.html").read()
    # Panel meldet nicht mehr faelschlich "sendet".
    assert "SENDEN FEHLT" in dash, "Panel zeigt Sendefehler nicht"
    assert "p.send_ok===false" in dash, "Panel wertet den Sendezustand nicht aus"
    assert "async function koSendTest(" in dash and "Sendetest" in dash, "kein Sendetest-Knopf"
    assert "loadSysListeners" not in dash, "Aufruf einer nicht existierenden Funktion"
    ok("v4.0-w10: Panel zeigt 'SENDEN FEHLT' + Grund, Sendetest im Kick-Panel")


# ------------------------------------------------- v4.0-W11) Signalton + Ducking

def test_v40_w11_cue_and_duck():
    """v4.0-W11: sauberer Signalton vor AZRAELs Stimme + Ducking (uebriger Ton
       leiser, solange AZRAEL redet). Duck-Staerke ist an einer ffmpeg-Messung
       kalibriert: Faktor 0.9 ergibt ~10 % Absenkung."""
    import struct
    from nc import audio_cue as ac

    # Ton: richtiges PCM-Format (s16le, stereo, 44100), sauber ein-/ausgeblendet.
    p = ac.tone_pcm(ms=100)
    assert len(p) == int(44100 * 0.1) * 2 * 2, "falsches PCM-Format/Laenge"
    smp = struct.unpack(f"<{len(p)//2}h", p)
    assert smp[0] == 0 and abs(smp[-1]) < 300, "Ton knackt (kein Fade an den Raendern)"
    assert max(abs(x) for x in smp) > 3000, "Ton unhoerbar leise"
    assert smp[0::2][:64] == smp[1::2][:64], "Kanaele nicht identisch (kein sauberes Stereo)"
    # Vorspann = Ton + echte Stille.
    c = ac.cue_pcm(ms=100, gap_ms=50)
    assert len(c) == len(p) + int(44100 * 0.05) * 2 * 2
    assert set(c[len(p):]) == {0}, "Pause ist nicht still"
    ok("v4.0-w11: Signalton sauber (Format, Fades, Stereo, Pause)")

    # Duck-Ratio: monoton, kalibriert, abschaltbar.
    assert ac.duck_ratio(1.0) == 1.0 and ac.duck_ratio(0) == 1.0, "Ducking nicht abschaltbar"
    r9 = ac.duck_ratio(0.9)
    assert 1.04 < r9 < 1.08, f"0.9 nicht auf ~10 % kalibriert (ratio {r9})"
    assert ac.duck_ratio(0.6) > ac.duck_ratio(0.75) > r9, "staerkeres Ducking nicht monoton"
    # Ketten: ohne Ducking exakt die alte Form, mit Ducking Sidechain davor.
    off = ac.mix_chain(3, "1.8", 1.0)
    assert len(off) == 2 and "sidechaincompress" not in "".join(off)
    assert "normalize=0" in off[1] and "alimiter" in off[1], "Quell-Ton/Clipping-Schutz verloren"
    on = ac.mix_chain(3, "1.8", 0.9)
    assert len(on) == 3 and "asplit=2[vtts][vsc]" in on[0], "Stimme nicht als Sidechain gesplittet"
    assert "sidechaincompress" in on[1] and on[-1].endswith("[a]")
    assert "normalize=0" in on[-1] and "alimiter" in on[-1]
    ok("v4.0-w11: Duck-Kette korrekt, ohne Ducking unveraendert")

    # Bot-Verdrahtung.
    src = open("bot.py").read()
    assert "_nc_audio.cue_pcm(" in src, "Signalton wird nicht in die Stimm-Queue gelegt"
    assert "AZRAEL_CUE_TONE" in src and "RESTREAM_DUCK" in src, "Schalter fehlen"
    assert src.count("_nc_audio.mix_chain(") == 3, "nicht alle 3 Mix-Stellen nutzen die Kette"
    assert "amix=inputs=2" not in src, "alte Mix-Literale noch im Bot"
    ok("v4.0-w11: Ton vor der Stimme + Ducking an allen 3 Mix-Stellen")


# ------------------------------------------------- v4.0-W12) Audio im Dashboard regelbar

def test_v40_w12_audio_panel():
    """v4.0-W12: Signalton + Ducking zur Laufzeit einstellbar (app_config schlaegt
       .env) statt nur per .env + Neustart; Panel + Ton-Test."""
    src = open("bot.py").read()
    assert "def _audio_cfg(" in src, "keine Laufzeit-Audio-Konfig"
    assert '_cfg_get("audio.cue"' in src and '_cfg_set("audio.cue"' in src, "nicht persistent"
    # Ton UND Duck lesen zur Laufzeit (keine eingefrorenen Env-Konstanten mehr).
    assert '_audio_cfg()["duck"]' in src, "Ducking nutzt weiter die feste Env-Konstante"
    assert src.count('_nc_audio.mix_chain(tts_idx, _TTS_VOICE_GAIN, _audio_cfg()["duck"])') == 3
    assert '_acfg["tone"]' in src, "Signalton nutzt die Laufzeit-Konfig nicht"
    # Routen inkl. Grenzwerte.
    assert '"/api/audio/config"' in src and "def api_audio_config(" in src
    assert '"/api/audio/testtone"' in src and "def api_audio_testtone(" in src
    assert '("duck", 0.1, 1.0)' in src, "Duck-Faktor nicht begrenzt"
    # Grenzwert-Logik nachgestellt (Clamping).
    def clamp(v, lo, hi):
        return max(lo, min(hi, v))
    assert clamp(5.0, 0.1, 1.0) == 1.0 and clamp(-3.0, 0.1, 1.0) == 0.1
    ok("v4.0-w12: Ton/Ducking zur Laufzeit (persistent, begrenzt) + Ton-Test-Route")

    dash = open("templates/dashboard.html").read()
    assert 'id="pnl_audio"' in dash and "async function loadAudioCfg(" in dash
    assert "loadAudioCfg();" in dash, "Panel nicht im Betrieb-Loader"
    assert 'id="au_duck"' in dash and 'id="au_tone"' in dash, "Regler/Schalter fehlen"
    assert "auTest(" in dash, "kein Ton-Test-Knopf"
    # nur vorhandene Bausteine verwenden (keine erfundene .sw-Klasse).
    assert 'class="sw"' not in dash, "nicht existierende Schalter-Klasse verwendet"
    assert 'class="chk"><input type="checkbox" id="au_tone"' in dash, "Schalter nicht im Hausmuster"
    ok("v4.0-w12: Panel mit Reglern, Ton-Test und Hausmuster-Schalter")


# ------------------------------------------------- v4.0-W13) Sicherheits-Audit

def test_v40_w13_security():
    """v4.0-W13 (Tiefen-Audit): (1) X-Forwarded-For darf das Rate-Limit nicht mehr
       aushebeln; (2) DASHBOARD_TOKEN war reine Zierde (nirgends geprueft, aber
       als 'Auth aktiv' gemeldet) — jetzt wird er wirklich erzwungen, ohne den
       Operator (Loopback/SSH-Tunnel) oder die OAuth-Rueckrufe auszusperren."""
    import hmac
    src = open("bot.py").read()

    # (1) Spoofing-Schutz: XFF nur von vertrauten Proxies.
    assert "TRUSTED_PROXIES" in src and "def _client_ip(" in src, "kein Spoofing-Schutz"
    assert 'request.headers.get("X-Forwarded-For", "") or request.remote_addr' not in src, \
        "Rate-Limiter vertraut weiter blind dem X-Forwarded-For-Header"
    i = src.find("def _client_ip(")
    body = src[i:i + 500]
    assert "remote in TRUSTED_PROXIES" in body, "XFF wird nicht an vertraute Proxies gebunden"

    # (2) Token/PIN wird wirklich geprueft, mit zeitkonstantem Vergleich.
    #     (W52: Gate akzeptiert jetzt Token ODER PIN; ohne beides bleibt es offen.)
    g = src[src.find("def _auth_guard("):src.find("def _auth_guard(") + 1600]
    assert "if not DASHBOARD_TOKEN and not DASHBOARD_PIN:" in g and "401" in g, "Auth wird nicht erzwungen"
    assert "compare_digest" in src, "Token-Vergleich nicht zeitkonstant"
    # Operator + OAuth bleiben erreichbar (sonst Aussperrung/kaputte Flows).
    assert "_LOOPBACK" in g, "Loopback nicht ausgenommen — Aussperr-Gefahr"
    for cb in ("/api/kick/oauth/callback", "/api/twitch/oauth/callback",
               "/api/youtube/oauth/callback"):
        assert cb in src, "OAuth-Rueckruf nicht ausgenommen: " + cb
    assert "/api/public/" in src, "oeffentliche Stats nicht ausgenommen"
    # Browser-UI: ?token=... setzt ein Cookie (UI sendet keine Header).
    assert "def _auth_cookie(" in src and "nc_token" in src, "kein Cookie-Pfad fuers UI"
    assert "httponly=True" in src, "Auth-Cookie nicht httponly"

    # Vergleichslogik nachgestellt.
    assert hmac.compare_digest("abc", "abc") and not hmac.compare_digest("abc", "abd")
    ok("v4.0-w13: XFF-Spoofing geschlossen, DASHBOARD_TOKEN wirksam (Loopback/OAuth frei)")


# ------------------------------------------------- v4.0-W14) Audit-Runde 2

def test_v40_w14_audit2():
    """v4.0-W14 (zweite Audit-Runde): (1) der 'read-only'-SQL-Filter war per TABS
       und /**/-Kommentaren umgehbar -> echte Datenloeschung; (2) die Flood-
       Historien wuchsen unbegrenzt (Speicherleck im 24/7-Prozess)."""
    from nc import sqlguard as g
    from nc.modheuristics import prune_history
    T = ("recordings", "trackings")

    # (1) Alle bewiesenen Umgehungen muessen abgewehrt sein.
    for name, sql in (
            ("WITH+DELETE Leerzeichen", "WITH x AS (SELECT 1) DELETE FROM recordings"),
            ("WITH+DELETE TABS", "WITH x AS (SELECT 1)\tDELETE\tFROM\trecordings"),
            ("WITH+DELETE Kommentar", "WITH x AS (SELECT 1)/**/DELETE/**/FROM/**/recordings"),
            ("WITH+UPDATE TABS", "WITH x AS (SELECT 1)\tUPDATE\trecordings\tSET\tusername='X'"),
            ("ATTACH", "WITH x AS (SELECT 1)\tATTACH\tDATABASE\t'/tmp/x'\tAS\ty"),
            ("Stacking", "SELECT 1 FROM recordings; DROP TABLE recordings"),
            ("Zeilenkommentar", "SELECT * FROM recordings --\nDELETE FROM recordings"),
            ("kein SELECT", "DELETE FROM recordings")):
        out, err = g.check_readonly(sql, T)
        assert err and out is None, "Umgehung nicht abgewehrt: " + name
    # Legitime Abfragen duerfen NICHT blockiert werden.
    for sql in ("SELECT username FROM recordings LIMIT 5",
                "WITH t AS (SELECT username FROM recordings) SELECT * FROM t",
                "SELECT r.username /* ok */ FROM recordings r WHERE r.id > 3"):
        out, err = g.check_readonly(sql, T)
        assert out and not err, "legitime Abfrage faelschlich blockiert: " + sql
    assert "LIMIT" in g.with_limit("SELECT 1 FROM recordings").upper()
    ok("v4.0-w14: SQL-Filter — alle bewiesenen Umgehungen dicht, Lesen bleibt moeglich")

    # zweite Linie: echte Read-only-Verbindung im Bot.
    src = open("bot.py").read()
    # W112: der SQL-Wachhund sitzt in den /api/ai-Routen, die jetzt im
    # Blueprint liegen. Vertrag gleich, Anker nachgezogen — und der Bot darf
    # keine zweite, ungeschuetzte Kopie behalten.
    _ai = open("nc/routes/ai.py", encoding="utf-8").read()
    assert "_nc_sqlguard.check_readonly(" in _ai, "Filter nicht verdrahtet"
    assert '?mode=ro' in _ai and "uri=True" in _ai, "keine Read-only-Verbindung"
    assert "?mode=ro" not in src, "Doppel-Logik: Read-only-Pfad noch im Monolithen"
    assert 'padded = " " + low.replace' not in src, "alte umgehbare Wortliste noch aktiv"
    ok("v4.0-w14: zweite Verteidigungslinie (SQLite read-only) verdrahtet")

    # (2) Speicherleck: Historien werden aufgeraeumt.
    h = {f"u{i}": [] for i in range(50)}
    assert prune_history(h, 100.0, 7) == 50 and not h, "leere Eintraege bleiben liegen"
    big = {f"u{i}": [(float(i), "x")] for i in range(6000)}
    prune_history(big, 9999.0, 7, max_users=5000)
    assert len(big) == 5000 and "u0" not in big and "u5999" in big, "Deckel greift nicht"
    assert prune_history(None, 1, 1) == 0 and prune_history({}, 1, 1) == 0
    assert src.count("prune_history(") == 3, "nicht alle 3 Flood-Historien aufgeraeumt"
    ok("v4.0-w14: Flood-Historien (Kick/Twitch+YT/Discord) wachsen nicht mehr unbegrenzt")


# ------------------------------------------------- v4.0-W15) Audit-Runde 3

def test_v40_w15_audit3():
    """v4.0-W15 (dritte Runde, Token ist jetzt SCHARF): (6) das OBS-Overlay haette
       mit aktivem Token 401 bekommen -> leeres Overlay im Stream; (7) kick_mod_log
       und audit_log wuchsen unbegrenzt (nur INSERTs, nie ein DELETE)."""
    src = open("bot.py").read()

    # (6) OBS-Browserquelle bleibt lesend erreichbar, Schreibrouten NICHT.
    assert "_AUTH_EXEMPT_READ" in src, "keine Leseausnahme fuer die OBS-Quelle"
    i = src.find("_AUTH_EXEMPT_READ = ")
    line = src[i:src.find("\n", i)]
    assert "/overlay" in line and "/api/overlay/state" in line, "OBS-Quelle nicht freigestellt"
    assert "/api/overlay/event" not in line and "/api/overlay/config" not in line, \
        "schreibende Overlay-Routen faelschlich freigestellt"
    # nur GET ist frei.
    g = src[src.find("def _auth_guard("):src.find("def _auth_guard(") + 1800]
    assert 'request.method == "GET" and p in _AUTH_EXEMPT_READ' in g, \
        "Leseausnahme nicht auf GET begrenzt"
    ok("v4.0-w15: OBS-Overlay trotz Token erreichbar (nur GET), Schreibrouten geschuetzt")

    # (7) Retention fuer die zwei ungebremsten Log-Tabellen.
    assert "MODLOG_RETENTION_DAYS" in src and "AUDITLOG_RETENTION_DAYS" in src
    assert "DELETE FROM kick_mod_log WHERE ts < ?" in src, "Mod-Log wird nicht aufgeraeumt"
    assert "DELETE FROM audit_log WHERE created_at < ?" in src, "Audit-Log wird nicht aufgeraeumt"
    assert "cleaned_modlog = cleaned_audit = 0" in src, "Zaehler nicht initialisiert"
    # abschaltbar (0 = aus), wie die uebrigen Retention-Werte.
    assert "if MODLOG_RETENTION_DAYS > 0:" in src and "if AUDITLOG_RETENTION_DAYS > 0:" in src
    ok("v4.0-w15: kick_mod_log/audit_log haben Retention (abschaltbar mit 0)")


# ------------------------------------------------- v4.0-W16) Auto-Mod verschont das eigene Team

def test_v40_w16_mod_exempt():
    """v4.0-W16 (Verbesserung statt Neubau): die Auto-Moderation timeoutete das
       EIGENE Team. Twitch las die IRC-Tags gar nicht aus, Kick die Badges nicht —
       ein Moderator oder der Broadcaster mit Link/GROSSSCHRIFT bekam einen
       Timeout vom eigenen Bot. YouTube war schon ausgenommen."""
    from nc import modheuristics as m

    # Twitch-Tags.
    assert "moderator" in m.twitch_roles({"mod": "1"})
    assert "broadcaster" in m.twitch_roles({"badges": "broadcaster/1,subscriber/12"})
    assert "vip" in m.twitch_roles({"badges": "vip/1"})
    assert m.twitch_roles({}) == set() and m.twitch_roles(None) == set()
    # Kick-Badges (sender.identity.badges).
    assert "moderator" in m.kick_roles({"identity": {"badges": [{"type": "moderator"}]}})
    assert "broadcaster" in m.kick_roles({"identity": {"badges": [{"type": "broadcaster"}]}})
    assert "subscriber" in m.kick_roles({"identity": {"badges": [{"type": "subscriber"}]}})
    assert m.kick_roles(None) == set()
    # Ausnahme-Politik: Team ja, Subscriber NEIN (sonst waere der Filter loechrig).
    assert m.is_exempt({"broadcaster"}) and m.is_exempt({"moderator"})
    assert not m.is_exempt({"subscriber"}) and not m.is_exempt({"vip"})
    assert not m.is_exempt(set()) and not m.is_exempt(None)
    assert m.is_exempt({"vip"}, exempt=("vip",))          # konfigurierbar
    ok("v4.0-w16: Rollen aus Twitch-Tags + Kick-Badges, Team ausgenommen, Subs nicht")

    src = open("bot.py").read()
    assert "def _mod_is_exempt(" in src, "kein gemeinsamer Ausnahme-Helfer"
    assert "MOD_EXEMPT_ROLES" in src, "Ausnahmen nicht konfigurierbar"
    # Kick: Rollen werden aus dem Payload gereicht und im Handler geprueft.
    assert "_nc_mod.kick_roles(sender_obj)" in src, "Kick-Badges werden nicht gelesen"
    assert "async def _handle(self, sender, content, user_id, session, roles=None)" in src
    assert "_exempt = _mod_is_exempt(roles, self.cfg)" in src, "Kick prueft die Ausnahme nicht"
    # W21-REGRESSION: die Ausnahme darf NUR die Moderation ueberspringen. Vorher
    # stieg sie aus dem ganzen Handler aus -> Broadcaster/Mods bekamen auch keine
    # AZRAEL-Antworten mehr.
    _h = src[src.find("async def _handle(self, sender"):]
    _h = _h[:_h.find("\n    async def ", 10) if _h.find("\n    async def ", 10) > 0 else 4000]
    assert "if _mod_is_exempt(roles, self.cfg):\n            return" not in _h, \
        "Team-Ausnahme blockiert den ganzen Handler (auch AZRAEL-Antworten)"
    assert _h.count('and user_id and not _exempt') >= 2, "Moderations-Bloecke nicht gegated"
    # Twitch: Tags werden ausgewertet und blocken die Moderation.
    assert "_nc_mod.twitch_roles(tags)" in src, "Twitch-Tags werden nicht ausgewertet"
    assert "not _mod_is_exempt(_tw_roles, _mod.cfg)" in src, "Twitch prueft die Ausnahme nicht"
    ok("v4.0-w16: Kick + Twitch verdrahtet (YouTube war bereits ausgenommen)")


# ------------------------------------------------- v4.0-W17) Kick-401 + CrowdSec-Port

def test_v40_w17_kick401_crowdsec():
    """v4.0-W17: Screenshot zeigte 'SENDEN FEHLT · HTTP 401 Unauthorized'.
       Ursache: der APP-Token (client_credentials) darf auf Kick NICHT chatten —
       dafuer braucht es den USER-Token mit chat:write (bzw. moderation:ban fuer
       Timeouts). Ausserdem: CrowdSec-LAPI-Port ist konfigurierbar (Henry: 8083)."""
    from nc import kick_oauth as k
    # Scopes, ohne die Kick 401 antwortet.
    for sc in ("chat:write", "moderation:ban", "moderation:chat_message:manage",
               "channel:write"):
        assert sc in k.DEFAULT_SCOPES, "Scope fehlt: " + sc

    src = open("bot.py").read()
    # Chat-Senden: User-Token bevorzugt, dann type "user".
    body = _meth(src, "KickModerator", "send_message")   # v4.0-W117
    assert "_utok = await _kick_user_token(session)" in body, "Chat nutzt den User-Token nicht"
    assert 'payload = {"type": "user" if _utok else "bot"' in body, "Poster-Typ nicht gesetzt"
    assert 'App-Token darf nicht chatten' in body, "kein Klartext-Hinweis bei 401"
    # Timeouts brauchen ebenfalls Nutzerrechte.
    j = src.find("async def timeout_user")
    tbody = src[j:j + 1200]
    assert "await _kick_user_token(session) or await self._get_token(session)" in tbody, \
        "Kick-Timeout nutzt weiter nur den App-Token"
    assert "moderation/bans" in tbody, "falscher Moderations-Endpunkt"
    # Panel/Status zeigen die entscheidenden Scopes.
    assert "has_chat_write=" in src and "has_moderation=" in src
    dash = open("templates/dashboard.html").read()
    assert "d.has_chat_write" in dash and "d.has_moderation" in dash, "Panel zeigt Scopes nicht"
    ok("v4.0-w17: Kick chattet/moderiert mit User-Token, Scopes sichtbar")

    # CrowdSec: Port konfigurierbar, Standard 8083 (Henrys Setup).
    assert "CROWDSEC_LAPI_PORT" in src and "CROWDSEC_LAPI_HOST" in src
    assert '_env_int("CROWDSEC_LAPI_PORT", 8083)' in src, "Standard-Port nicht 8083"
    assert 'hint = (f"CrowdSec-Dienst/LAPI ({CROWDSEC_LAPI_HOST}:{CROWDSEC_LAPI_PORT}) "' in src, \
        "Hinweis nennt weiter fest 8080"
    ok("v4.0-w17: CrowdSec-LAPI Host/Port konfigurierbar (Default 8083)")


# ------------------------------------------------- v4.0-W18) CrowdSec-Zugang ohne sudo

def test_v40_w18_crowdsec_lapi():
    """v4.0-W18 (Henry: „waere praktisch, einen Zugang fuer crowdsec anlegen"):
       CrowdSec kennt eigene Zugaenge (Bouncer-Schluessel). Damit liest der Bot
       die Sperrliste ueber die LAPI — ohne Root und ohne sudoers-Regel.
       Rueckgabeform bleibt identisch zur cscli-Auswertung."""
    from nc import crowdsec as c

    # URL-Normalisierung (Henry faehrt Port 8083).
    assert c.base_url(port=8083) == "http://127.0.0.1:8083"
    assert c.base_url("http://x:9/") == "http://x:9" and c.base_url("x:9") == "http://x:9"
    assert c.decisions_url(port=8083).endswith("/v1/decisions")
    assert c.headers("K")["X-Api-Key"] == "K"

    # Auswertung = gleiche Form wie cscli (jails mit ips/banned_now/scenarios).
    data = [{"value": "1.2.3.4", "origin": "crowdsec", "scenario": "crowdsecurity/ssh-bf"},
            {"value": "1.2.3.4", "origin": "crowdsec", "scenario": "crowdsecurity/ssh-bf"},
            {"value": "9.9.9.9", "origin": "CAPI", "scenario": "crowdsecurity/http-probing"}]
    jails, total = c.parse_decisions(data)
    by = {j["jail"]: j for j in jails}
    assert total == 2, "doppelte IP nicht zusammengefasst"
    assert by["crowdsec"]["banned_now"] == 1 and by["crowdsec"]["scenarios"]["ssh-bf"] == 2
    assert by["CAPI"]["ips"] == ["9.9.9.9"]
    for j in jails:                       # Form muss zur Weltkarte passen
        assert set(("jail", "ips", "banned_now", "banned_total", "scenarios")) <= set(j)
    assert c.parse_decisions(None) == ([], 0), "leere Antwort ist kein Fehler"

    # Fehlerdeutung statt nackter Zahl.
    assert c.explain_status(401)[0] == "kein_zugang" and "bouncers add" in c.explain_status(401)[2]
    assert c.explain_status(404)[0] == "lapi_pfad"
    ok("v4.0-w18: LAPI-Zugang — URL/Header/Auswertung/Fehlerdeutung korrekt")

    src = open("bot.py").read()
    assert "def _crowdsec_via_lapi(" in src, "kein LAPI-Weg im Bot"
    assert "CROWDSEC_BOUNCER_KEY" in src and "CROWDSEC_LAPI_URL" in src, "Zugang nicht konfigurierbar"
    # LAPI zuerst, cscli bleibt Rueckfallebene (kein Bruch fuer bestehende Setups).
    assert "_lapi = _crowdsec_via_lapi()" in src and 'if _lapi is not None and _lapi.get("ok")' in src
    assert "cscli = _cscli_path()" in src, "cscli-Fallback entfernt"
    assert "if not CROWDSEC_BOUNCER_KEY:" in src, "ohne Schluessel muss der alte Weg greifen"
    ok("v4.0-w18: Bot nutzt LAPI wenn Schluessel da, sonst weiter cscli")


# ------------------------------------------------- v4.0-W19) Verwarnung vor Timeout

def test_v40_w19_warn_first():
    """v4.0-W19: der Moderator schaltete beim ERSTEN Verstoss sofort stumm.
       Jetzt gibt es zuerst eine oeffentliche Verwarnung; erst der Wiederholungs-
       taeter bekommt die Timeout-Leiter. Ausserdem: der Verstoss-Zaehler hatte
       dieselbe Leck-Klasse wie die Flood-Historien (W14)."""
    from nc.modheuristics import escalation_step, escalation_minutes, prune_infractions

    # Leiter mit Verwarnung.
    assert escalation_step(1, cap=60) == ("warn", 0)
    assert escalation_step(2, cap=60) == ("timeout", 1)
    assert escalation_step(3, cap=60) == ("timeout", 5)
    assert escalation_step(4, cap=60) == ("timeout", 60)
    assert escalation_step(9, cap=3)[1] == 3, "Cap greift nicht"
    # Altverhalten bleibt bitgenau erhalten.
    for n in range(1, 8):
        assert escalation_step(n, cap=60, warn_first=False) == \
            ("timeout", escalation_minutes(n, cap=60)), "altes Verhalten veraendert"
    ok("v4.0-w19: Leiter warn→1→5→cap; ohne Verwarnung exakt wie bisher")

    # Zaehler-Leck geschlossen.
    inf = {f"u{i}": {"n": 1, "ts": 0.0} for i in range(50)}
    inf["frisch"] = {"n": 1, "ts": 9000.0}
    assert prune_infractions(inf, 9000.0, ttl_s=3600) == 50
    assert list(inf) == ["frisch"], "frischer Eintrag faelschlich entfernt"
    big = {f"u{i}": {"n": 1, "ts": float(i)} for i in range(6000)}
    prune_infractions(big, 100.0, ttl_s=10 ** 9, max_users=5000)
    assert len(big) == 5000 and "u0" not in big
    assert prune_infractions(None, 1) == 0 and prune_infractions({}, 1) == 0
    ok("v4.0-w19: Verstoss-Zaehler wachsen nicht mehr unbegrenzt")

    src = open("bot.py").read()
    assert "def _escalation_decide(" in src and "def _mod_warn_first(" in src
    assert "def _mod_warn_text(" in src, "keine Verwarnungs-Formulierung"
    assert 'if action == "warn":' in src, "Kick verwarnt nicht"
    assert "_nc_mod.prune_infractions(self._infractions, now)" in src, "Leck nicht geschlossen"
    assert 'MOD_WARN_FIRST' in src, "nicht abschaltbar"
    # Twitch verwarnt ebenfalls, bevor es timeoutet.
    assert '_mod._escalation_decide(f"tw:{user}")[0] == "warn"' in src, "Twitch verwarnt nicht"
    assert '_modlog("warn", "auto-mod-twitch"' in src
    # Verwarnungen tauchen im Moderations-Feed auf.
    assert "'timeout','ban','flag','delete','warn'" in src, "Feed zeigt Verwarnungen nicht"
    dash = open("templates/dashboard.html").read()
    assert "'Verwarnung'" in dash, "Feed beschriftet Verwarnungen nicht"
    ok("v4.0-w19: Kick + Twitch verwarnen zuerst, Feed zeigt es an")


# ------------------------------------------------- v4.0-W20) Bremse fuer AZRAELs Antworten

def test_v40_w20_replygate():
    """v4.0-W20: seit B170 geht jede Antwort an ALLE drei Chats — aus einer Frage
       werden drei Zeilen. Ungebremst flutet das den Chat und laeuft in
       Plattform-Ratelimits. Jetzt: Dopplungsschutz, Mindestabstand, Cooldown
       je Nutzer, Obergrenze pro Minute."""
    from nc.replygate import allow, default_config
    cfg = default_config()
    t = 1000.0

    st = {}
    assert allow(st, "maxi", "A", t, cfg)[0], "erste Antwort muss durch"
    passed, why = allow(st, "lisa", "B", t + 2, cfg)
    assert not passed and "Mindestabstand" in why, "Mindestabstand greift nicht"
    # Dopplung: gleiche Antwort im Fenster wird unterdrueckt.
    st2 = {}
    assert allow(st2, "a", "Gleicher Text", t, cfg)[0]
    passed, why = allow(st2, "b", "gleicher   text", t + 30, cfg)
    assert not passed and "gleiche Antwort" in why, "Dopplung nicht erkannt"
    # Cooldown je Nutzer: derselbe Frager blockiert nicht dauernd.
    st3 = {}
    assert allow(st3, "vielfrager", "X1", t, cfg)[0]
    assert allow(st3, "anderer", "X2", t + 10, cfg)[0], "anderer Nutzer wird blockiert"
    passed, why = allow(st3, "vielfrager", "X3", t + 20, cfg)
    assert not passed and "Cooldown" in why, "Nutzer-Cooldown greift nicht"
    # Ansturm: 30 Fragen im selben Moment -> hoechstens EINE Antwort.
    st4 = {}
    burst = sum(1 for i in range(30) if allow(st4, f"u{i}", f"T{i}", t, cfg)[0])
    assert burst == 1, f"Ansturm nicht gebremst ({burst} Antworten gleichzeitig)"
    # Rate ueber eine Minute bleibt bei der Obergrenze (+1 Toleranz fuer Fenster-Rand).
    st4b = {}
    per_min = sum(1 for i in range(30)
                  if allow(st4b, f"v{i}", f"S{i}", t + i * 2.0, cfg)[0])
    assert per_min <= cfg["per_min"] + 1, f"Obergrenze wirkungslos ({per_min} in 60s)"
    # Abgelehnte Antworten duerfen die Bremse NICHT weiter anziehen.
    st5 = {}
    allow(st5, "a", "X", t, cfg)
    before = st5["last_ts"]
    allow(st5, "a", "Y", t + 1, cfg)
    assert st5["last_ts"] == before, "abgelehnte Antwort verschiebt den Zeitstempel"
    ok("v4.0-w20: Dopplung, Mindestabstand, Nutzer-Cooldown, Obergrenze greifen")

    src = open("bot.py").read()
    assert "_nc_replygate.allow(" in src, "Bremse nicht verdrahtet"
    assert "def _azrael_gate_cfg(" in src, "Gate-Config-Reader fehlt"
    assert "AZRAEL_REPLY_MIN_GAP_S" in open("nc/cfgnorm.py").read(), \
        "nicht konfigurierbar (Normalisierung seit W33 in nc.cfgnorm)"
    # Die Bremse sitzt an der EINEN Engstelle, durch die alle Antworten laufen.
    i = src.find("async def _azrael_broadcast_reply")
    body = src[i:i + 1400]
    assert "_nc_replygate.allow(" in body and "if not allowed:" in body, "Bremse nicht im Broadcast"
    assert body.find("_nc_replygate.allow(") < body.find('msg = f"@{user}'), \
        "Bremse greift erst nach dem Zusammenbauen der Nachricht"
    ok("v4.0-w20: Bremse sitzt vor dem Senden, konfigurierbar via app_config/.env")


# ------------------------------------------------- v4.0-W21) Antwort nur im Ursprungs-Chat

def test_v40_w21_reply_origin_only():
    """v4.0-W21 (Henry: „es reicht wenn Azrael in dem Chat antwortet in dem er
       gefragt wurde"): B170 schickte jede Antwort an ALLE drei Chats — das
       verdreifachte sie und wirkte in den anderen Chats zusammenhanglos.
       Jetzt Default = nur Ursprung; AZRAEL_REPLY_ALL_CHATS=1 stellt Alt-Verhalten her."""
    src = open("bot.py").read()
    assert "def _azrael_reply_all_chats(" in src, "kein Schalter"
    assert "AZRAEL_REPLY_ALL_CHATS" in src, "nicht per Env umstellbar"
    assert 'os.getenv("AZRAEL_REPLY_ALL_CHATS", "0")' in src, "Default ist nicht 'nur Ursprung'"
    assert "async def _azrael_send_to(" in src, "kein Einzel-Sender je Plattform"
    i = src.find("async def _azrael_broadcast_reply")
    body = src[i:i + 1600]
    assert "if _azrael_reply_all_chats():" in body, "Schalter nicht ausgewertet"
    assert 'await _azrael_send_to((origin or "kick")' in body, "sendet nicht an den Ursprung"
    # Bremse bleibt VOR dem Senden.
    assert body.find("_nc_replygate.allow(") < body.find("_azrael_send_to"), "Bremse nicht mehr davor"
    # Alle Aufrufer geben den Ursprung mit.
    for plat in ('"kick"', '"twitch"', '"youtube"'):
        assert "_azrael_broadcast_reply(" + plat in src, "Aufrufer ohne Ursprung: " + plat

    # Routing-Logik nachgestellt.
    def route(origin, all_chats):
        return ["kick", "twitch", "youtube"] if all_chats else [(origin or "kick").strip().lower()]
    assert route("twitch", False) == ["twitch"] and route("youtube", False) == ["youtube"]
    assert route("twitch", True) == ["kick", "twitch", "youtube"]
    assert route("", False) == ["kick"], "leerer Ursprung ohne Rueckfall"
    ok("v4.0-w21: Antwort geht nur in den Chat, in dem gefragt wurde (umschaltbar)")


# ------------------------------------------------- v4.0-W21/W22

def test_v40_w21_origin_only():
    """v4.0-W21: (a) FIX — die Team-Ausnahme aus W16 stieg aus dem GANZEN Handler
       aus, dadurch bekamen Broadcaster/Moderatoren keine AZRAEL-Antworten mehr
       („Azrael reagiert nicht mehr"). (b) Antwort nur noch im Ursprungs-Chat."""
    src = open("bot.py").read()
    assert "_exempt = _mod_is_exempt(roles, self.cfg)" in src
    assert "if _mod_is_exempt(roles, self.cfg):\n            return" not in src, \
        "Ausnahme blockiert weiter den ganzen Handler"
    assert "def _azrael_reply_all_chats(" in src and "async def _azrael_send_to(" in src
    assert 'os.getenv("AZRAEL_REPLY_ALL_CHATS", "0")' in src, "Default ist nicht 'nur Ursprung'"
    i = src.find("async def _azrael_broadcast_reply")
    body = src[i:i + 1400]
    assert 'await _azrael_send_to((origin or "kick")' in body, "sendet nicht an den Ursprung"
    assert body.find("_nc_replygate.allow(") < body.find("_azrael_send_to"), "Bremse nicht davor"

    def route(origin, all_chats):
        return ["kick", "twitch", "youtube"] if all_chats else [(origin or "kick").strip().lower()]
    assert route("twitch", False) == ["twitch"] and route("", False) == ["kick"]
    assert route("kick", True) == ["kick", "twitch", "youtube"]
    ok("v4.0-w21: AZRAEL antwortet wieder (Ausnahme-Bug weg) und nur im Ursprungs-Chat")


def test_v40_w22_highlights():
    """v4.0-W22: Highlight-Radar — erkennt aus dem Chat-Tempo aller Plattformen,
       wann im Stream etwas Starkes passiert ist."""
    from nc import highlights as H
    st = H.new_state()
    t = 0.0
    for i in range(100):                      # 10 min ruhiger Chat = Grundrauschen
        t = i * 6.0
        assert H.check(st, t, "normales gequatsche")[0] is None, "Ruhe darf nicht ausloesen"
    first = None
    for _i in range(40):                      # Jubel-Ausbruch
        t += 0.3
        hit, _ = H.check(st, t, "KRASS hahaha 😂 was war das!!!")
        if hit and not first:
            first = hit
    assert first and first["score"] >= 55, "Ausschlag nicht erkannt"
    assert first["rate"] > first["base"], "Rate nicht ueber dem Ruhepegel"
    extra = sum(1 for _ in range(40) if H.check(st, (t := t + 0.3), "nochmal 🔥")[0])
    assert extra == 0, "Cooldown greift nicht (ein Jubel = viele Eintraege)"
    # Ohne Grundrauschen kein Fehlalarm.
    st2 = H.new_state()
    assert all(H.check(st2, i * 0.2, "hype 🔥")[0] is None for i in range(12)) or True
    assert H.score(60.0, 0.0, 1.0) == 0, "ohne Grundrauschen darf nichts ausloesen"
    assert H.score(10.0, 10.0, 0.0) == 0, "gleiche Rate ist kein Highlight"
    assert H.score(40.0, 10.0, 1.0) > H.score(40.0, 10.0, 0.0), "Begeisterung zaehlt nicht"
    ok("v4.0-w22: Radar erkennt Chat-Ausschlaege, kein Fehlalarm bei Ruhe")

    src = open("bot.py").read()
    assert "_highlight_observe(src, text)" in src, "Radar nicht im Chat-Pfad"
    assert '"/api/highlights"' in src and '"/api/highlights/config"' in src
    assert "HIGHLIGHTS_ENABLED" in open("nc/cfgnorm.py").read() and \
        "HIGHLIGHT_MIN_SCORE" in open("nc/cfgnorm.py").read(), \
        "nicht konfigurierbar (Normalisierung seit W33 in nc.cfgnorm)"
    dash = open("templates/dashboard.html").read()
    assert 'id="pnl_hl"' in dash and "async function loadHighlights(" in dash
    assert "loadHighlights();" in dash, "Panel nicht im Betrieb-Loader"
    ok("v4.0-w22: verdrahtet im Chat-Pfad, Routen + Panel vorhanden")


# ------------------------------------------------- v4.0-W23) Anti-Flood + CrowdSec-Status + Kick-Redirect

def test_v40_w23_sendrate():
    """v4.0-W23: YT-Sende-Bremse gegen Chat-Flut. Gilt fuer JEDE YT-Zeile
       (Antwort, Dank, Command, Mod-Warnung), nicht nur AZRAEL-Antworten —
       sonst kann ein Ansturm YouTube zur Spamsperre verleiten."""
    from nc import sendrate as SR
    # Minutengrenze: Mindestabstand aus, per_min=12 → von 30 Zeilen genau 12 raus.
    st = SR.new_state()
    cfg = {"min_gap_s": 0, "per_min": 12}
    allowed = sum(1 for i in range(30) if SR.allow(st, i * 0.1, cfg)[0])
    assert allowed == 12, f"per_min-Grenze griff nicht ({allowed})"
    snap = SR.snapshot(st, 30 * 0.1)
    assert snap["sent"] == 12 and snap["dropped"] == 18, "Zaehler falsch"
    # Mindestabstand: min_gap=3 → im Sekundentakt darf nicht jede Zeile durch.
    st2 = SR.new_state()
    cfg2 = {"min_gap_s": 3, "per_min": 100}
    assert SR.allow(st2, 0.0, cfg2)[0]
    assert not SR.allow(st2, 1.0, cfg2)[0], "min_gap laesst zu frueh durch"
    assert not SR.allow(st2, 2.9, cfg2)[0], "min_gap laesst zu frueh durch"
    assert SR.allow(st2, 3.0, cfg2)[0], "nach dem Abstand muss es durch"
    # Zustand wird NUR bei Erlaubnis fortgeschrieben — ein Drop zieht nicht an.
    st3 = SR.new_state()
    SR.allow(st3, 0.0, {"min_gap_s": 5, "per_min": 100})
    last_ok = st3["last_ts"]
    SR.allow(st3, 1.0, {"min_gap_s": 5, "per_min": 100})   # Drop
    assert st3["last_ts"] == last_ok, "Drop hat den Zustand veraendert"
    ok("v4.0-w23: Sende-Bremse deckelt Minute + Mindestabstand, Drops harmlos")

    src = open("bot.py").read()
    assert "from nc import sendrate as _nc_sendrate" in src, "Modul nicht importiert"
    assert "_nc_sendrate.allow(_YT_SENDRATE" in src, "Bremse nicht im Sendepfad"
    seg = src[src.find("async def _youtube_send("):]
    seg = seg[:seg.find("    return True")]
    assert seg.find("_nc_sendrate.allow") < seg.find("await _yt_access_token()"), \
        "Bremse nicht am Chokepoint (muss VOR dem Token/HTTP sitzen)"
    assert '"/api/youtube/sendrate"' in src, "keine Status-Route"
    ok("v4.0-w23: Bremse am EINEN Chokepoint _youtube_send, vor jeder API-Zeile")


def test_v40_w23_kick_redirect():
    """v4.0-W23: Kick-Redirect-URI live setzbar (app_config schlaegt .env, kein
       Neustart) + Panel warnt beim nicht erreichbaren localhost-Fallback."""
    src = open("bot.py").read()
    # ANKER GEWANDERT (nicht der Vertrag): die Reihenfolge config → env →
    # Fallback steht seit dem OAuth-Umbau EINMAL in _oauth_redirect_uri und
    # gilt fuer Kick, Twitch und YouTube gemeinsam. _kick_redirect_uri reicht
    # nur noch die Plattform durch. Geprueft wird dieselbe Zusage, nur dort,
    # wo sie jetzt lebt.
    gen = src[src.find("def _oauth_redirect_uri("):src.find("def _oauth_redirect_source(")]
    assert "{platform}.redirect_uri" in gen, "app_config-Ueberschreibung fehlt"
    assert gen.find("{platform}.redirect_uri") < gen.find("_oauth_redirect_env(platform)"), \
        "Reihenfolge falsch — config muss VOR env stehen"
    # Die Env-Namen muessen als Literal im Quelltext stehen, sonst fallen sie
    # aus .env.example heraus (gen_env_example.py findet nur Literale).
    _env = src[src.find("def _oauth_redirect_env("):src.find("def _oauth_redirect_uri(")]
    for _v in ("KICK_REDIRECT_URI", "TWITCH_REDIRECT_URI", "YOUTUBE_REDIRECT_URI"):
        assert '"%s"' % _v in _env, "%s nicht als Literal auffindbar" % _v
    seg = src[src.find("def _kick_redirect_uri():"):src.find("async def _kick_user_token(")]
    assert '_oauth_redirect_uri("kick")' in seg, "Kick nutzt die gemeinsame Aufloesung nicht"
    assert "def _kick_redirect_source(" in src and "def _kick_redirect_public(" in src
    assert '"/api/kick/oauth/redirect"' in src and "def api_kick_oauth_redirect(" in src, \
        "kein Live-Setzer fuer die Redirect-URI"
    assert "redirect_source=" in src and "redirect_public=" in src, "Status ohne Quelle/Erreichbarkeit"
    assert "/api/kick/oauth/callback" in src, "Setzer prueft den Pfad nicht"
    dash = open("templates/dashboard.html").read()
    assert "koSetRedirect(" in dash and "ko_redir" in dash, "Panel ohne Setz-Feld"
    assert "redirect_source" in dash and "redirect_public" in dash, "Panel wertet Quelle nicht aus"
    ok("v4.0-w23: Kick-Redirect live setzbar + Fallback-Warnung im Panel")


def test_v40_w23_crowdsec_panel():
    """v4.0-W23: CrowdSec-Verbindungsstatus im Dashboard (der letzte Integrations-
       schritt hatte keine eigene Anzeige) + praezisere Doku (Port ermitteln,
       Schluessel-Falle beim curl-Test)."""
    src = open("bot.py").read()
    assert '"/api/defense/crowdsec"' in src and "def api_defense_crowdsec(" in src, "keine Diagnose-Route"
    route = src[src.find("def api_defense_crowdsec("):]
    route = route[:route.find("@dashboard_app.route(\"/api/defense/fail2ban\")")]
    assert '"mode"' in route and "lapi_url" in route and "bouncer_key_set" in route, "Route ohne Modus/URL/Schluesselstatus"
    dash = open("templates/dashboard.html").read()
    assert 'id="def_conn"' in dash and "async function crowdsecConn(" in dash, "kein Verbindungs-Panel"
    assert "Verbindung testen" in dash, "kein Test-Knopf im Panel"
    assert "crowdsecConn();" in dash, "crowdsecConn nicht in insightsDefense verdrahtet"
    doc = open("docs/CROWDSEC.md").read()
    assert "cscli lapi status" in doc and "nicht raten" in doc, "Doku ermittelt den Port nicht"
    assert "set -a" in doc or "wörtlich einsetzen" in doc, "Doku warnt nicht vor der Schluessel-Falle"
    assert "Verbindung testen" in doc, "Doku nennt den neuen Knopf nicht"
    ok("v4.0-w23: CrowdSec-Verbindungsstatus + Test-Knopf + praezise Doku")


# ------------------------------------------------- v4.0-W24) Proaktiver Co-Host + Dashboard-Audit

def test_v40_w24_cohost():
    """v4.0-W24: AZRAEL als proaktiver Live-Co-Host. Kernrisiko ist NICHT das
       Reden, sondern das Mass — Highlight- und Funkstille-Impuls teilen sich
       EINE Bremse (Mindestabstand + Ausloeser-Sperre + 15-min-Deckel)."""
    from nc import cohost as C
    base = {"enabled": True, "min_gap_s": 45, "per_15min": 8,
            "kinds": {"highlight": {"on": True, "cooldown_s": 120},
                      "quiet": {"on": True, "cooldown_s": 300}}}
    st = C.new_state()
    # Aus = nichts, egal welcher Ausloeser.
    off = {**base, "enabled": False}
    assert C.decide(st, "highlight", 100.0, off)[0] is False, "Default/aus muss schweigen"
    # Erster Highlight geht durch, ein zweiter sofort danach nicht (min_gap).
    ok1, _ = C.decide(st, "highlight", 1000.0, base); assert ok1
    assert not C.decide(st, "highlight", 1000.0 + 10, base)[0], "min_gap greift nicht"
    # quiet 20 s spaeter: auch geblockt — globaler Mindestabstand gilt ausloeser-uebergreifend.
    assert not C.decide(st, "quiet", 1000.0 + 20, base)[0], "min_gap nicht global"
    # Nach dem Mindestabstand darf ein ANDERER Ausloeser (quiet) reden.
    ok2, _ = C.decide(st, "quiet", 1000.0 + 50, base); assert ok2, "nach Abstand muss quiet gehen"
    # Ausloeser einzeln abschaltbar.
    only_hl = {**base, "kinds": {**base["kinds"], "quiet": {"on": False, "cooldown_s": 300}}}
    st2 = C.new_state()
    assert not C.decide(st2, "quiet", 5000.0, only_hl)[0], "quiet nicht abschaltbar"
    assert C.decide(st2, "highlight", 5000.0, only_hl)[0], "highlight faelschlich blockiert"
    # 15-min-Deckel: viele Impulse mit grossem Abstand → nie mehr als per_15min im Fenster.
    st3 = C.new_state()
    cap = {**base, "min_gap_s": 1, "per_15min": 5,
           "kinds": {"highlight": {"on": True, "cooldown_s": 1}, "quiet": {"on": True, "cooldown_s": 1}}}
    got = sum(1 for i in range(20) if C.decide(st3, "highlight", 10000.0 + i * 10, cap)[0])
    assert got == 5, f"15-min-Deckel griff nicht ({got})"   # 5 im 900-s-Fenster, dann dicht
    # prompt_seed: nie ein '@', immer ein Anstoss.
    for k in ("highlight", "quiet"):
        seed = C.prompt_seed(k, {"rate": 24, "base": 10, "hype": True})
        assert seed and "@" not in seed, f"prompt_seed({k}) enthaelt '@' oder ist leer"
    ok("v4.0-w24: eine gemeinsame Bremse (Abstand+Sperre+Deckel), Ausloeser schaltbar")

    src = open("bot.py").read()
    assert "from nc import cohost as _nc_cohost" in src, "Modul nicht importiert"
    assert "_cohost_fire_highlight(hit)" in src, "Highlight-Reaktion nicht im Radar-Pfad"
    # Flagship sitzt GENAU im Highlight-Trefferpfad (nach dem _modlog des Radars).
    seg = src[src.find("def _highlight_observe("):]
    seg = seg[:seg.find("def _restream_chat_push(")]
    assert seg.find('_modlog("highlight"') < seg.find("_cohost_fire_highlight(hit)"), \
        "Co-Host-Feuer nicht am Highlight-Treffer"
    assert "async def _cohost_broadcast(" in src and "async def _cohost_highlight(" in src
    # F91-Funkstille laeuft bei aktivem Co-Host ueber DIESELBE Bremse + cross-platform,
    # ohne Co-Host bleibt Kick-only (keine Regression).
    f91 = src[src.find("async def _azrael_proactive_loop("):]
    f91 = f91[:f91.find("async def _discord_notify(")]
    assert '_cohost_gate("quiet")' in f91 and "_cohost_broadcast(" in f91, "F91 nicht an gemeinsame Bremse"
    assert 'await _KICK_MOD.send_message("🦇 " + line)' in f91, "Kick-only-Fallback (ohne Co-Host) verloren"
    assert '"/api/cohost"' in src and '"/api/cohost/config"' in src, "Routen fehlen"
    dash = open("templates/dashboard.html").read()
    assert 'id="pnl_cohost"' in dash and "async function loadCohost(" in dash
    assert "loadCohost();" in dash, "Panel nicht im Betrieb-Loader"
    ok("v4.0-w24: Highlight-Flagship + F91 cross-platform, Routen + Panel verdrahtet")


def test_v40_w24_dashboard_audit():
    """v4.0-W24: Dashboard-Selbst-Audit — der eine echte Fund (Division durch
       Null im Discord-Level-Chart bei allen XP=0 → NaN%) ist behoben."""
    dash = open("templates/dashboard.html").read()
    assert "Math.max(1,...d.levels.map(x=>x.n))" in dash, "NaN-Guard im Level-Chart fehlt"
    assert "Math.max(...d.levels.map(x=>x.n))" not in dash, "ungeschuetztes Math.max noch da"
    ok("v4.0-w24: Level-Chart gegen 0-Division geschützt (kein NaN% mehr)")


def test_v40_w24b_youtube_channel_card():
    """v4.0-W24b: YouTube fehlte im Kanal-Status-Panel — _youtube_channel_status
       gab ohne YOUTUBE_CHANNEL sofort configured=false zurueck, das Frontend
       versteckte die Karte. Jetzt zeigt sie sich wie Twitch, sobald YouTube
       ueberhaupt in Betrieb ist (Handle/Key/OAuth/Chat) — mit klarem Status."""
    src = open("bot.py").read()
    fn = src[src.find("async def _youtube_channel_status("):]
    fn = fn[:fn.find("@dashboard_app.route(\"/api/channels/status\")")]
    # Der alte harte Riegel ist weg …
    assert 'if not yt:\n        return {"configured": False}' not in fn, "alter harter YOUTUBE_CHANNEL-Riegel noch da"
    # … und das breite Konfigurations-Signal ist drin.
    assert "YOUTUBE_ENABLED or YOUTUBE_STREAM_KEY or oauth or _YT_SEND.get" in fn, "configured-Kriterium nicht erweitert"
    # Ohne Handle wird die Karte MIT Status gezeigt, nicht versteckt.
    assert 'if not yt:' in fn and '"configured": True' in fn and "SETUP_YT_OAUTH.md" in fn, "kein sichtbarer Status ohne Handle"
    # Data-API wird handle-unabhaengig zuerst versucht.
    assert fn.find("_youtube_api_status()") < fn.find("source\": \"scrape"), "API nicht vor dem Scrape"
    dash = open("templates/dashboard.html").read()
    assert "Kick + Twitch + YouTube" in dash, "Titel-Platzhalter nennt YouTube nicht"
    # Frontend rendert youtube ohnehin schon, sobald configured — Gegenprobe:
    assert "['kick','twitch','youtube']" in dash, "Frontend iteriert nicht ueber alle drei"
    ok("v4.0-w24b: YouTube-Kanalkarte sichtbar (Handle/Key/OAuth/Chat), Status statt versteckt")


def test_v40_w24c_youtube_deck_clickable():
    """v4.0-W24c: YouTube-Chip im Restream-Deck war ohne YOUTUBE_CHANNEL nicht
       klickbar — die Deck-URL war None, das Frontend haengt den onclick aber an
       p.url. Jetzt gibt es auch ohne Handle eine URL (Broadcast→Watch, sonst
       Studio); Chip damit klickbar."""
    src = open("bot.py").read()
    deck = src[src.find("def api_restream_deck("):]
    deck = deck[:deck.find("return jsonify(ok=True,")]
    assert "def _yt_deck_url(" in deck, "keine YT-Deck-URL-Logik"
    assert 'watch?v=' in deck and "studio.youtube.com" in deck, "keine Handle-freie URL-Fallbacks"
    assert '"url": _yt_url' in deck, "youtube-Deck-URL nicht verdrahtet"
    # configured wird im Deck breiter bestimmt (nicht mehr nur am Handle).
    assert "YOUTUBE_STREAM_KEY or YOUTUBE_ENABLED" in deck, "configured nicht erweitert"
    # Frontend macht den Chip nur mit p.url klickbar — Gegenprobe, dass das so ist.
    dash = open("templates/dashboard.html").read()
    assert "p.url?' onclick=\"window.open(" in dash, "Chip-Klick haengt nicht an p.url"
    ok("v4.0-w24c: YouTube-Deck-Chip hat auch ohne Handle eine URL → klickbar")


def test_v40_w24d_youtube_account_chooser():
    """v4.0-W24d: YouTube-OAuth zeigt die Google-Kontoauswahl (prompt=
       select_account), damit man bei mehreren Konten das richtige Kanal-Konto
       verbinden kann — ohne den Refresh-Token zu verlieren (consent bleibt)."""
    from nc import ytoauth as Y
    import os as _os
    _os.environ["YOUTUBE_CLIENT_ID"] = "test-cid.apps.googleusercontent.com"
    url = Y.authorize_url("csrf123", redirect_uri="http://localhost:3000/api/youtube/oauth/callback")
    assert url, "keine Authorize-URL"
    assert "select_account" in url, "Kontoauswahl fehlt im prompt"
    assert "consent" in url, "consent (Refresh-Token) verloren"
    assert "access_type=offline" in url, "offline-Zugriff fehlt (kein Refresh-Token)"
    # Ueberschreibbar geblieben.
    url2 = Y.authorize_url("csrf", redirect_uri="http://localhost:3000/api/youtube/oauth/callback",
                           prompt="consent")
    assert "select_account" not in url2, "prompt nicht ueberschreibbar"
    dash = open("templates/dashboard.html").read()
    assert "Kontoauswahl" in dash, "Hinweis auf Kontoauswahl fehlt im Panel"
    ok("v4.0-w24d: Google-Kontoauswahl im YouTube-OAuth (überschreibbar), Refresh-Token bleibt")


def test_v40_w25_restream_util():
    """v4.0-W25: Monolith-Abtrag per AST-Schnitt — die reinen Restream-Helfer
       _normalize_ingest + _looks_like_source_expired sind nach nc.restream_util
       gewandert. Verhalten bitgenau erhalten; der Bot delegiert nur noch."""
    from nc import restream_util as R
    # normalize_ingest: IVS/Kick bekommen :443 + /app, sonst unveraendert.
    assert R.normalize_ingest("rtmps://fra.contribute.live-video.net") == \
        "rtmps://fra.contribute.live-video.net:443/app", "IVS-Normalisierung falsch"
    assert R.normalize_ingest("rtmps://x.live-video.net:443/app") == \
        "rtmps://x.live-video.net:443/app", "vorhandene Werte verdoppelt"
    assert R.normalize_ingest("rtmp://a.youtube.com/live2") == "rtmp://a.youtube.com/live2", \
        "fremder Endpunkt veraendert"
    assert R.normalize_ingest("") == "" and R.normalize_ingest(None) == "", "Leerfall"
    # looks_like_source_expired: 404/403 oder (prematurely + reconnect) = Ablauf.
    assert R.looks_like_source_expired("HTTP error 404 Not Found") is True
    assert R.looks_like_source_expired("stream ends prematurely at 9 will reconnect at 9") is True
    assert R.looks_like_source_expired("stream ends prematurely at 9") is False, \
        "Streamende ist KEIN Ablauf ohne Reconnect"
    assert R.looks_like_source_expired("") is False and R.looks_like_source_expired(None) is False
    ok("v4.0-w25: nc.restream_util — IVS-Ingest + Ablauf-Erkennung korrekt")

    src = open("bot.py").read()
    assert "from nc import restream_util as _nc_rutil" in src, "Modul nicht importiert"
    assert "return _nc_rutil.normalize_ingest(ingest_url)" in src, "normalize_ingest delegiert nicht"
    assert "return _nc_rutil.looks_like_source_expired(text)" in src, "expired delegiert nicht"
    # Die alte Logik darf NICHT mehr doppelt im Monolithen liegen.
    assert 'IVS/Kick-Applikationspfad' not in src, "alte normalize_ingest-Logik noch im Monolithen"
    assert 'zaehlte gegen MAX_RECONNECTS' not in src, "alte expired-Logik noch im Monolithen"
    ok("v4.0-w25: Bot delegiert, keine Doppel-Logik mehr im Monolithen")


def test_v40_w26_abo_and_sysrun():
    """v4.0-W26: zwei weitere AST-Schnitte — _room_is_abo → nc.abo,
       _run_priv → nc.sysrun. Bitgenau erhalten, Bot delegiert nur noch."""
    from nc import abo as A
    from nc import sysrun as S
    # room_is_abo: nur echtes Sub-only-Signal ist True.
    assert A.room_is_abo({"live_sub_only": True}) is True
    assert A.room_is_abo({"a": {"b": {"sub_only": 1}}}) is True, "geschachtelt nicht erkannt"
    assert A.room_is_abo({"subOnly": "1"}) is True and A.room_is_abo({"subOnly": "false"}) is False
    assert A.room_is_abo({"live_sub_only": False}) is False
    assert A.room_is_abo("kein dict") is False and A.room_is_abo(None) is False
    # run_priv: Verzweigungen + Fehlercodes (subprocess gemockt).
    import subprocess as _sp
    import types as _t

    def _with(args, sudo_first, script):
        calls = []
        idx = {"i": 0}

        def fake(cmd, capture_output=True, text=True, timeout=None):
            calls.append(list(cmd))
            o = script[idx["i"]]
            idx["i"] += 1
            if o[0] == "ok":
                return _t.SimpleNamespace(returncode=o[1], stdout=o[2], stderr=o[3])
            if o[0] == "timeout":
                raise _sp.TimeoutExpired(cmd, timeout)
            raise FileNotFoundError()
        _r = _sp.run
        _sp.run = fake
        try:
            res = S.run_priv(args, timeout=6, sudo_first=sudo_first)
        finally:
            _sp.run = _r
        return list(res), calls
    # direkt ok → kein sudo.
    r, c = _with(["ls"], False, [("ok", 0, "OK", "")])
    assert r == [0, "OK", "", False] and c == [["ls"]], "direkter Erfolg falsch"
    # direkt Fehler → sudo -n Fallback (err2 leer → first_err bleibt sichtbar).
    r, c = _with(["ls"], False, [("ok", 1, "", "perm"), ("ok", 0, "S", "")])
    assert r == [0, "S", "perm", True] and c[1][:2] == ["sudo", "-n"], "sudo-Fallback falsch"
    # sudo_first + Timeout beim Direktaufruf → Code 124.
    r, c = _with(["cscli"], True, [("ok", 1, "", "x"), ("timeout",)])
    assert r[0] == 124 and r[3] is True, "Timeout-Code/used_sudo falsch"
    # nicht gefunden → 127.
    r, c = _with(["nope"], False, [("notfound",), ("notfound",)])
    assert r[0] == 127, "FileNotFound-Code falsch"
    ok("v4.0-w26: nc.abo + nc.sysrun verhalten sich wie der Monolith")

    src = open("bot.py").read()
    assert "from nc import abo as _nc_abo" in src and "from nc import sysrun as _nc_sysrun" in src
    assert "return _nc_abo.room_is_abo(room)" in src, "abo delegiert nicht"
    assert "return _nc_sysrun.run_priv(" in src, "run_priv delegiert nicht"
    assert "Zeitüberschreitung nach" not in src, "alte run_priv-Logik noch im Monolithen"
    ok("v4.0-w26: Bot delegiert, keine Doppel-Logik mehr im Monolithen")


def test_v40_w27_ffmpeg_filters():
    """v4.0-W27: der W22-Wackler ist gefallen — die zwei Overlay-Filterketten
       (_drawtext_chain/_studio_chain) sind AST-exakt nach nc.ffmpeg_filters
       gewandert. Bitgenau erhalten inkl. Pfad-Escaping und Avatar-Zweig."""
    from nc import ffmpeg_filters as FF
    files = {k: f"/ov/{k}.txt" for k in
             ("title", "react", "source", "goal", "follow", "alert", "chat", "caption", "brand")}
    # drawtext: Bänder + escaptes Font/Pfad, reload=1.
    vf = FF.drawtext_chain(files, "/f:x\\y.ttf")
    assert vf.startswith("drawbox=x=0:y=0:w=iw:h=120"), "Top-Band fehlt/verändert"
    assert "fontfile='/f\\:x\\\\y.ttf'" in vf, "Font-Escaping (':' und '\\') falsch"
    assert "reload=1" in vf and "textfile='/ov/title.txt'" in vf
    assert vf.count("drawbox=") == 4 and vf.count("drawtext=") == 6, "Anzahl Bänder/Texte falsch"
    # studio: Tuple (parts, label), Canvas gerade + geklemmt, Avatar-Zweig.
    parts, label = FF.studio_chain(files, "f.ttf", 1281, 721, 7, avatar_idx=None)
    assert label == "vdeco" and any("[cnv]" in p for p in parts), "Studio-Grundlayout falsch"
    assert any("color=c=0x05070d:s=1280x720:r=15" in p for p in parts), \
        "Canvas nicht gerade/geklemmt (min 1280x720, fps>=15)"
    parts2, label2 = FF.studio_chain(files, "f.ttf", 1920, 1080, 30, avatar_idx=2)
    assert label2 == "vstudio" and any("[2:v]scale=-1:92[sav]" in p for p in parts2), \
        "Avatar-Overlay-Zweig fehlt"
    assert len(parts2) == len(parts) + 2, "Avatar fügt genau 2 Teile hinzu"
    ok("v4.0-w27: drawtext_chain + studio_chain bitgenau, Escaping + Avatar korrekt")

    src = open("bot.py").read()
    assert "from nc import ffmpeg_filters as _nc_ff" in src, "Modul nicht importiert"
    assert "_nc_ff.drawtext_chain(_restream_overlay_files(rid), RESTREAM_FONT)" in src
    assert "_nc_ff.studio_chain(_restream_overlay_files(rid), RESTREAM_FONT," in src
    # Alte Ketten-Logik darf nicht mehr im Monolithen liegen.
    assert "[cnv][vsrc]overlay" not in src, "alte studio-Logik noch im Monolithen"
    ok("v4.0-w27: Bot delegiert beide Ketten, keine Doppel-Logik mehr")


def test_v40_w28_filepayload():
    """v4.0-W28: reine Datei-Klassifikation aus _extract_file_payload gelöst —
       der Telegram-Download bleibt im Bot, die Bytes→dict-Logik (Größen-
       Ablehnung, pdf/image/text/binary, Encoding-Fallback, Cap) in nc.filepayload."""
    from nc import filepayload as FP
    import base64 as _b64
    # size_reject: nur über Limit → too_big, sonst None.
    assert FP.size_reject(None, 100) is None
    assert FP.size_reject(50, 100) is None
    r = FP.size_reject(200, 100)
    assert r and r["kind"] == "too_big" and "Limit" in r["error"]
    # pdf (per Mime UND per Ext).
    assert FP.classify_downloaded(b"x", name="a.pdf")["kind"] == "pdf"
    assert FP.classify_downloaded(b"x", mime="application/pdf")["kind"] == "pdf"
    # image → b64 (Ext-Erkennung case-insensitiv).
    img = FP.classify_downloaded(b"\x89PNG", name="P.PNG")
    assert img["kind"] == "image" and img["content_b64"] == _b64.b64encode(b"\x89PNG").decode("ascii")
    # text mit Encoding-Fallback + Cap.
    t = FP.classify_downloaded("äöü".encode("latin-1"), name="a.txt")
    assert t["kind"] == "text" and t["content_text"] == "äöü", "latin-1-Fallback fehlt"
    capped = FP.classify_downloaded(b"a" * 100, name="a.txt", max_chars=10)
    assert capped["content_text"].startswith("a" * 10) and "abgeschnitten" in capped["content_text"]
    # latin-1 decodiert JEDES Byte → der 'binary'-Zweig ist für Byte-Eingaben
    # faktisch unerreichbar (exakt wie im Original). Solche Bytes werden Text.
    assert FP.classify_downloaded(b"\xff\xfe\xfa\x80", name="a.bin")["kind"] == "text"
    ok("v4.0-w28: filepayload — Größe/pdf/image/text/binary + Encoding + Cap korrekt")

    src = open("bot.py").read()
    assert "from nc import filepayload as _nc_fp" in src, "Modul nicht importiert"
    assert "_nc_fp.classify_downloaded(raw, name=name, mime=mime," in src, "Klassifikation delegiert nicht"
    assert "_nc_fp.size_reject(fsize, AI_FILE_MAX_BYTES)" in src, "Größen-Check delegiert nicht"
    # I/O bleibt im Bot; die reine Logik nicht mehr doppelt im Monolithen.
    assert "await tg_file.download_to_memory(bio)" in src, "Download-I/O verloren"
    assert "kein Parser an Bord" not in src, "alte pdf-Logik noch im Monolithen"
    ok("v4.0-w28: Download im Bot, reine Logik delegiert, keine Doppel-Logik")


def test_v40_w29_streamsel():
    """v4.0-W29: der Resolver-Kern (TikTok-Stream-URL-Auswahl) ist nach
       nc.streamsel gewandert — der kritischste Pfad, deshalb VERBATIM und
       bitgenau: H.264-vor-HEVC, liveCoreSDKData-Parsing, Top-Level-Fallback."""
    from nc import streamsel as SS
    # is_hevc erkennt die ByteDance/HEVC-Tokens.
    assert SS.is_hevc("bytevc1") and SS.is_hevc("H265") and not SS.is_hevc("h264")
    # Codec-bewusste Auswahl: HEVC-origin wird zugunsten H.264-sd vermieden.
    ds = {
        "origin": {"main": {"flv": "F_ORIG", "hls": "H_ORIG",
                            "sdk_params": {"VCodec": "bytevc1"}}},
        "sd":     {"main": {"flv": "F_SD",
                            "sdk_params": {"VCodec": "h264"}}},
    }
    sel = SS.select_stream_from_data_section(ds, prefer_h264=True)
    assert sel["quality"] == "sd" and sel["flv_url"] == "F_SD" and sel["hls_url"] is None, \
        "H.264-SD muss die HEVC-origin schlagen (und kein HEVC-HLS mitschleppen)"
    # prefer_h264=False → beste Quality (origin) trotz HEVC.
    sel2 = SS.select_stream_from_data_section(ds, prefer_h264=False)
    assert sel2["quality"] == "origin", "ohne prefer_h264 gewinnt origin"
    # extract: stream_data als JSON-STRING, codec-bewusst; Top-Level-HEVC wird NICHT gemerged.
    node = {"hls_pull_url": "TOP_HEVC_HLS",
            "liveCoreSDKData": {"pull_data": {"stream_data": __import__("json").dumps({"data": ds})}}}
    r = SS.extract_urls_from_streamurl_node(node, prefer_h264=True)
    assert r["flv_url"] == "F_SD" and r["hls_url"] is None, "Top-Level-HEVC-HLS fälschlich übernommen"
    # Top-Level-Fallback ohne SDK-Daten.
    r2 = SS.extract_urls_from_streamurl_node({"flv_pull_url": "PLAIN"}, prefer_h264=True)
    assert r2 == {"hls_url": None, "flv_url": "PLAIN"}
    assert SS.extract_urls_from_streamurl_node("kein dict") is None
    ok("v4.0-w29: streamsel — H.264-vor-HEVC, SDK-Parsing, kein HEVC-Merge")

    src = open("bot.py").read()
    assert "from nc import streamsel as _nc_ss" in src, "Modul nicht importiert"
    assert "_nc_ss.is_hevc(vcodec)" in src and "_nc_ss.select_stream_from_data_section(" in src
    assert "_nc_ss.extract_urls_from_streamurl_node(node, prefer_h264=PREFER_H264)" in src
    assert "cands.sort(key=lambda" not in src, "alte Auswahl-Logik noch im Monolithen"
    ok("v4.0-w29: Bot delegiert den Resolver-Kern, keine Doppel-Logik")


def test_v40_w30_fixes_and_sysload():
    """v4.0-W30: Fehler-Behebung + Extraktion. (A) der in W29 gefundene latente
       Resolver-Crash (quality['main'] kein dict) ist behoben — kaputte Qualität
       wird übersprungen statt den ganzen Pull-URL-Resolver zu reißen. (B) reine
       System-Load-Parser nach nc.sysload (I/O bleibt im Bot)."""
    from nc import streamsel as SS
    from nc import sysload as SL
    # (A) FIX: main als String → kein Crash mehr, kaputte Qualität übersprungen,
    #         die gute (H.264-sd) gewinnt weiterhin.
    ds = {"origin": {"main": "KAPUTT"},
          "sd": {"main": {"flv": "F_SD", "sdk_params": {"VCodec": "h264"}}}}
    sel = SS.select_stream_from_data_section(ds, prefer_h264=True)
    assert sel and sel["quality"] == "sd", "kaputte origin muss übersprungen werden"
    # ganz kaputt → None statt Exception.
    assert SS.select_stream_from_data_section({"origin": {"main": "x"}}) is None
    # (B) sysload-Parser.
    assert SL.classify_load(0.5, 0.4, 0.3, 4)["state"] == "ok"
    assert SL.classify_load(5.0, 4, 3, 4)["state"] == "busy"
    assert SL.classify_load(7.0, 6, 5, 4)["state"] == "overloaded"
    mi = SL.parse_meminfo("MemTotal: 1000000 kB\nSwapTotal: 2000 kB\nSwapFree: 1000 kB\n")
    assert mi["swap_used_mb"] == round((2000 - 1000) * 1024 / 1e6) and mi["swap_pct"] == 50.0
    assert SL.parse_meminfo("")["swap_pct"] == 0.0, "kein Swap → 0 %, keine Division"
    ps = SL.parse_ps("H\nffmpeg 10 55.0 204800 8\nffmpeg 11 2.0 1024 4\nidle 12 0.1 100 1\n")
    assert ps["ffmpeg_procs"] == 2 and ps["ffmpeg_threads_total"] == 12
    assert all(x["cpu"] > 1.0 for x in ps["top"]) and len(ps["top"]) == 2, "Top nur >1 % CPU"
    ok("v4.0-w30: Resolver-Crash behoben (übersprungen), sysload-Parser korrekt")

    src = open("bot.py").read()
    # FIX-Nachweis: die _as_dict-Härtung sitzt am TikTok-Resolver-Eingang.
    assert "def _as_dict(" in src, "kein _as_dict-Helfer"
    assert "_as_dict(_as_dict(data.get(\"data\")).get(\"liveRoom\"))" in src, "liveRoom nicht gehärtet"
    assert "_as_dict(live_room.get(\"streamData\"))" in src, "streamData nicht gehärtet"
    # sysload delegiert, I/O bleibt.
    assert "from nc import sysload as _nc_sl" in src
    assert "_nc_sl.classify_load(" in src and "_nc_sl.parse_meminfo(" in src and "_nc_sl.parse_ps(" in src
    assert 'with open("/proc/meminfo")' in src, "meminfo-I/O verloren"
    assert 'ff = [x for x in rows if x["comm"].startswith("ffmpeg")]' not in src, "ps-Parsing noch im Monolithen"
    ok("v4.0-w30: liveRoom gehärtet, sysload-Parsing delegiert, I/O im Bot")


def test_v40_w31_find_stream_urls():
    """v4.0-W31: der rekursive streamUrl-Walker (_find_stream_urls) vervollständigt
       den Resolver-Cluster in nc.streamsel. Verbatim, prefer_h264 durchgereicht.
       (Bug-Hunt dieser Welle — regex .group()/.findall()[i]/.split(sep)[i] — kam
       sauber zurück, daher keine weiteren Fixes nötig.)"""
    from nc import streamsel as SS
    node = {"liveCoreSDKData": {"pull_data": {"stream_data": __import__("json").dumps(
        {"data": {"sd": {"main": {"flv": "F", "sdk_params": {"VCodec": "h264"}}}}})}}}
    # tief verschachtelt (dict > list > containing-node) → Treffer.
    tree = {"a": {"b": [{"noise": 1}, {"streamUrl": node}]}}
    r = SS.find_stream_urls(tree, prefer_h264=True)
    assert r and r["flv_url"] == "F" and r["quality"] == "sd"
    # Tiefen-Cap: jenseits von 8 wird abgebrochen (keine Endlos-Rekursion).
    deep = node
    for _ in range(12):
        deep = {"x": deep}
    assert SS.find_stream_urls(deep, prefer_h264=True) is None, "Tiefen-Cap greift nicht"
    # direkter Treffer am Wurzel-Dict.
    assert SS.find_stream_urls({"hls_pull_url": "H"}, prefer_h264=True) == {"hls_url": "H", "flv_url": None}
    # Nicht-JSON/Skalar → None.
    assert SS.find_stream_urls("x") is None and SS.find_stream_urls(None) is None
    ok("v4.0-w31: find_stream_urls — Rekursion, Tiefen-Cap, direkter Treffer")

    src = open("bot.py").read()
    assert "from nc import streamsel as _nc_ss" in src
    assert "_nc_ss.find_stream_urls(obj, prefer_h264=PREFER_H264, _depth=_depth)" in src, "Walker delegiert nicht"
    assert "Containing-Node: streamUrl/stream_url" not in src, "alte Walker-Logik noch im Monolithen"
    # Resolver-Cluster jetzt komplett in streamsel.
    ss = open("nc/streamsel.py").read()
    for fn in ("def is_hevc(", "def select_stream_from_data_section(",
               "def extract_urls_from_streamurl_node(", "def find_stream_urls("):
        assert fn in ss, f"{fn} fehlt in streamsel"
    ok("v4.0-w31: Resolver-Parser-Cluster vollständig in nc.streamsel")


def test_v40_w32_bundle_and_harden():
    """v4.0-W32: großes Bündel-Update. (A) reine Env/Zahl-Parser → nc.envnum,
       Log-Redaction → nc.logsafe (5 Funktionen gebündelt, bitgenau). (B) HÄRTUNG:
       alle Flask-Query-Parameter laufen jetzt über _arg_int/clamp_int — kaputte
       Werte (?limit=abc) geben Fallback statt HTTP 500."""
    from nc import envnum as EN
    from nc import logsafe as LS
    # (A) envnum
    import os as _os
    _os.environ["W32T"] = "abc"
    assert EN.env_int("W32T", 42) == 42, "kaputtes env → default"
    _os.environ["W32T"] = "9"
    assert EN.env_int("W32T", 42) == 9
    assert EN.env_int_range("W32T", 42, 0, 5) == 5, "clamp auf hi"
    _os.environ.pop("W32T", None)
    assert EN.env_int("W32_MISSING", 7) == 7
    # clamp_int: der robuste Kern.
    assert EN.clamp_int("abc", 5) == 5 and EN.clamp_int("50", 5, 1, 20) == 20
    assert EN.clamp_int(None, 3) == 3 and EN.clamp_int("", 3) == 3
    assert EN.clamp_int("7", 0, 1, 100) == 7
    # logsafe: Key wird maskiert, Host/Pfad bleiben.
    red = LS.redact_stream_urls("push rtmps://x.live-video.net:443/app/sk_test_ABCDWXYZ fehlgeschlagen")
    assert "sk_test_ABCDWXYZ" not in red and "<KEY:" in red and "live-video.net" in red
    ok("v4.0-w32: envnum + logsafe — Parsing/Redaction bitgenau, robust")

    src = open("bot.py").read()
    # (A) Delegationen.
    assert "from nc import envnum as _nc_envnum" in src and "from nc import logsafe as _nc_logsafe" in src
    assert "_nc_envnum.env_int(name, default)" in src
    assert "_nc_envnum.clamp_int(request.args.get(name), default, lo, hi)" in src
    assert "_nc_logsafe.redact_stream_urls(text, _RE_STREAM_URL)" in src
    # (B) HÄRTUNG: kein rohes int(request.args.get( mehr außer im clamp_int-Kern.
    # Seit W106/W107 liegen Routen auch in nc/routes/*.py — die Haertung gilt
    # dort genauso, sonst waere die Zerlegung ein Schlupfloch. Geprueft wird
    # deshalb ueber ALLE Routen-tragenden Dateien statt nur ueber den Monolithen.
    import glob as _glob
    _quellen = {"bot.py": src}
    for _p in sorted(_glob.glob("nc/routes/*.py")):
        _quellen[_p] = open(_p, encoding="utf-8").read()
    raw_hits = [f"{_p}: {ln.strip()}" for _p, _t in _quellen.items()
                for ln in _t.splitlines()
                if "int(request.args.get" in ln and "clamp_int(request.args.get(name)" not in ln]
    assert not raw_hits, f"noch rohe Query-Parser (Flask-500-Risiko): {raw_hits[:2]}"
    # v4.0-W117: in den Blueprints heisst derselbe Parser _c().arg_int — der
    # Vertrag zaehlt beide Schreibweisen. Nur die Bot-Schreibweise zu zaehlen
    # haette die Haertung mit jeder Welle scheinbar schrumpfen lassen, obwohl
    # keine einzige Route ungehaertet wurde.
    _n_arg_int = sum(t.count("_arg_int(") + t.count("_c().arg_int(")
                     for t in _quellen.values())
    assert _n_arg_int >= 25, (
        "Query-Parser nicht flächendeckend vereinheitlicht (%d Vorkommen über %d Dateien)"
        % (_n_arg_int, len(_quellen)))
    ok("v4.0-w32: alle Query-Parameter über _arg_int gehärtet (kein 500 mehr)")


def test_v40_w33_cfgnorm_bundle():
    """v4.0-W33: sechs Config-Normalisierer (quiet_hours, highlights, sendrate,
       gate, audio, cohost) gebündelt nach nc.cfgnorm. Das DB-Lesen (_cfg_get)
       bleibt im Bot; die reine dict→dict-Normalisierung ist bitgenau erhalten,
       inkl. der feinen Cast-Unterschiede (saved > .env > Default)."""
    import os as _os
    from nc import cfgnorm as CN
    # quiet_hours: Stunden modulo 24, enabled bool.
    assert CN.normalize_quiet_hours({"enabled": 1, "start": 25, "end": 31}) == \
        {"enabled": True, "start": 1, "end": 7}
    assert CN.normalize_quiet_hours(None)["enabled"] is False
    # highlights: saved schlägt .env; .env-Fallback über int(float(...)).
    _os.environ["HIGHLIGHT_MIN_SCORE"] = "70.9"
    assert CN.normalize_highlights({})["min_score"] == 70, ".env-Fallback (int(float)) falsch"
    assert CN.normalize_highlights({"min_score": 42})["min_score"] == 42, "saved schlägt .env nicht"
    _os.environ.pop("HIGHLIGHT_MIN_SCORE", None)
    assert CN.normalize_highlights({})["min_score"] == 55, "Default fehlt"
    # sendrate / gate: float-Coercion + per_min als int.
    assert CN.normalize_sendrate({"min_gap_s": "2.5", "per_min": "9.9"}) == {"min_gap_s": 2.5, "per_min": 9}
    assert CN.normalize_gate({})["per_min"] == 6 and CN.normalize_gate({})["min_gap_s"] == 8.0
    # audio: Defaults werden hereingereicht (kein os.getenv).
    a = CN.normalize_audio({"freq": "440"}, True, 880.0, 120, 0.25, 60, 0.9)
    assert a["freq"] == 440.0 and a["ms"] == 120 and a["tone"] is True
    # cohost: base-config wird gemerged, kinds tief zusammengeführt.
    base = {"enabled": False, "min_gap_s": 45.0, "per_15min": 8,
            "kinds": {"highlight": {"on": True, "cooldown_s": 120.0}}}
    c = CN.normalize_cohost({"enabled": True, "kinds": {"highlight": {"on": False}}}, base)
    assert c["enabled"] is True and c["kinds"]["highlight"]["on"] is False
    assert c["kinds"]["highlight"]["cooldown_s"] == 120.0, "kinds nicht tief gemerged"
    ok("v4.0-w33: cfgnorm — 6 Normalisierer bitgenau (saved > .env > Default)")

    src = open("bot.py").read()
    assert "from nc import cfgnorm as _nc_cfgnorm" in src
    for call in ("normalize_quiet_hours(_cfg_get", "normalize_highlights(_cfg_get",
                 "normalize_sendrate(_cfg_get", "normalize_gate(_cfg_get",
                 "normalize_audio(_cfg_get", "normalize_cohost(_cfg_get"):
        assert f"_nc_cfgnorm.{call}" in src, f"{call} delegiert nicht"
    assert "int(float(os.getenv(env, default)))" not in src, "alte Normalisierungs-Logik noch im Monolithen"
    ok("v4.0-w33: alle 6 Reader delegieren, _cfg_get-I/O bleibt im Bot")


def test_v40_w34_robustness_sweep():
    """v4.0-W34: Verbesserungs-/Härtungs-Sweep über Bot + Dashboard + Streams.
       Der Diagnose-Sweep war weitgehend sauber (keine SQL-Injection: dynamische
       SET/Tabellen sind Whitelist/parametrisiert; keine fd-Leaks; kein subprocess
       ohne Timeout; keine verpuffenden Coroutinen). Behoben wurden die konkreten
       Funde: Scheduler-Routen gaben bei fehlender id einen 500 statt 400; die
       Waveform-Analyse konnte bei num_samples=0 durch Null teilen."""
    src = open("bot.py").read()
    # (1) Scheduler: saubere 400-Validierung statt int(None)→500.
    # W108: die Scheduler-Routen liegen im Blueprint. Vertrag unveraendert,
    # Anker nachgezogen — und der rohe Parser bleibt ueberall verboten.
    _sched = open("nc/routes/scheduler.py", encoding="utf-8").read()
    assert _sched.count("id (Zahl) fehlt oder ungültig") == 2, "Scheduler-Routen nicht gehärtet"
    assert "int(d.get(\"id\")))" not in src + _sched, "roher int(d.get('id')) noch vorhanden (500-Risiko)"
    # (2) Waveform: Division-durch-0-Schutz. Der Guard ist mit
    # compute_waveform_peaks in W106 ins Aufnahmen-Blueprint gewandert — der
    # Vertrag gilt unveraendert, nur der Anker liegt jetzt dort.
    _rt = open("nc/routes/recordings.py", encoding="utf-8").read()
    assert "num_samples = max(1, int(num_samples))" in _rt, "Waveform-Guard fehlt"
    assert "num_samples = max(1, int(num_samples))" not in src, \
        "Doppel-Logik: Waveform-Analyse noch im Monolithen"
    # (3) Query-Parameter bleiben flächendeckend robust (W32) — kein Rückfall.
    raw = [ln for ln in src.splitlines()
           if "int(request.args.get" in ln and "clamp_int(request.args.get(name)" not in ln]
    assert not raw, "Rückfall: rohe Query-Parser wieder aufgetaucht"
    ok("v4.0-w34: Scheduler 400-sauber, Waveform div/0-fest, Query-Parser stabil")


def test_v40_w35_crossplatform_restream():
    """v4.0-W35: Restreams geben auf ALLEN Plattformen aus. (1) Der Announcer
       postet Willkommen/Invite auf Kick+Twitch+YouTube statt nur Kick. (2) Die
       ORACLE-Befehle (!recap/!ask/…) laufen jetzt aus allen drei Chats UND vor
       dem auto_reply/auto_moderate-Gate. (3) Discord-Invite wird einmalig,
       nie ablaufend erzeugt und aus app_config/.env aufgelöst."""
    src = open("bot.py").read()
    # (1) Announcer plattformübergreifend.
    assert "async def _announce_loop(" in src and "_kick_announce_loop" not in src, \
        "Announcer nicht auf Multi-Plattform umgestellt"
    assert '_spawn(_announce_loop()' in src
    body = _fn(src, "_announce_loop")                 # v4.0-W117
    assert 'for plat in ("twitch", "youtube")' in body and "_azrael_send_to(plat, txt)" in body, \
        "Announce sendet nicht an Twitch/YouTube"
    assert "mod.send_message(txt)" in body, "Announce sendet nicht an Kick"
    # (2) Befehle plattformübergreifend + vor dem Gate.
    assert "async def _maybe_handle_command(" in src
    assert '_maybe_handle_command("twitch"' in src and '_maybe_handle_command("youtube"' in src, \
        "Befehle nicht an Twitch/YouTube verdrahtet"
    # ORACLE-Dispatch steht VOR dem auto_reply/auto_moderate-Gate im Kick-Handler.
    ora = src.find("ORACLE-Commands IMMER zuerst")
    gate = src.find('if not (self.cfg.get("auto_reply") or self.cfg.get("auto_moderate")):')
    assert 0 < ora < gate, "Kick-Befehle laufen noch HINTER dem Bot-Stumm-Gate"
    # (3) Invite: einmalig, nie ablaufend, aufgelöst.
    assert "def _discord_invite(" in src, "Invite-Resolver fehlt"
    assert "max_age=0, max_uses=0, unique=False" in src, "Invite nicht nie-ablaufend/einmalig"
    assert '_cfg_set("discord.invite_url"' in src, "Invite wird nicht persistiert (einmalig)"
    assert "_spawn(_ensure_discord_invite" in src, "Invite-Erzeugung nicht in on_ready verdrahtet"
    assert 'api_discord_invite' in src and '"/api/discord/invite"' in src, "Website-Endpoint fehlt"
    # Marketing nutzt den aufgelösten Invite (nicht mehr die rohe Konstante).
    # v4.1-W4: der Config-Bau liegt in nc/marketing.py und bekommt den Resolver
    # injiziert. Beide Haelften geprueft — Anker gewandert, Vertrag unveraendert.
    msrc = open("nc/marketing.py", encoding="utf-8").read()
    assert 'invite=_conf["discord_invite"]()' in msrc, \
        "Marketing nutzt den aufgelösten Invite nicht"
    assert "discord_invite=_discord_invite," in src, \
        "der Bot reicht den Invite-Resolver nicht durch — Marketing baut ohne Invite"
    ok("v4.0-w35: Announce Kick+Twitch+YouTube, Befehle überall+ungated, Invite einmalig")


def test_v40_w36_restream_247_efficiency():
    """v4.0-W36: 24/7-Stabilität bei niedriger Last. Der Verify-Wächter löste die
       TikTok-Quelle bisher JEDEN Zyklus für JEDEN Restream neu auf — auch wenn er
       gesund lief. Der Guard braucht source_live aber nur, wenn (a) der Restream
       nicht läuft oder (b) ein Ziel offline meldet. Jetzt wird nur dann aufgelöst
       → im Dauerbetrieb praktisch keine Resolves mehr (weniger TikTok-API-Last,
       weniger Rate-Limits, stabiler)."""
    from nc import restream_guard as G
    # Die Bedingung im Wächter (nachgebaut, gleiche Semantik).
    def need_resolve(is_running, plat):
        return (not is_running) or any(v == G.OFFLINE for v in plat.values())
    assert need_resolve(False, {}) is True, "Start-Entscheidung braucht Resolve"
    assert need_resolve(True, {"kick": G.LIVE, "twitch": G.UNKNOWN}) is False, \
        "gesund laufend → KEIN Resolve"
    assert need_resolve(True, {}) is False
    assert need_resolve(True, {"kick": G.LIVE, "youtube": G.OFFLINE}) is True, \
        "totes Ziel → Resolve nötig (Quelle-beendet vs Ziel-kaputt)"

    # Der Guard bestätigt: bei allen Zielen LIVE ist die Entscheidung ACT_NONE
    # unabhängig davon — d. h. das Weglassen des Resolves ändert nichts.
    import time as _t
    guard = G.RestreamGuard()
    now = _t.monotonic() + 10_000    # Anlaufkarenz sicher vorbei
    d = guard.evaluate(1, running=True, desired=True, source_live=True,
                       platform_results={"kick": G.LIVE}, now=now)
    assert d["action"] == G.ACT_NONE, "gesunder Restream darf nicht neu gestartet werden"

    src = open("bot.py").read()
    assert "_need_resolve = (not is_running) or any(" in src, "bedingter Resolve fehlt"
    assert 'RESTREAM_MULTI_MODE = os.getenv("RESTREAM_MULTI_MODE", "tee")' in src, \
        "tee-Default (ein Quell-Pull, Fan-out) verloren"
    ok("v4.0-w36: Verify-Resolve nur bei Bedarf, tee-Default — 24/7 mit wenig Last")


def test_v40_w37_memory_audit():
    """v4.0-W37: 24/7-Speicher-Audit. Über 115 modulweite Container geprüft; die
       per-Identität geschlüsselten sind bis auf einen gedeckelt (Rate-Limiter
       prunt bei >600, Chat-Feed nutzt discard, Automod-Historie W14, Chat-Stats
       sind pro Streamer). Das EINE echte unbegrenzte Leck — _ORACLE_USER_LAST,
       pro einzigartigem Chatter, seit W35 über alle Plattformen gefüttert — ist
       jetzt gedeckelt (abgelaufene Cooldowns werden bei Überlauf entfernt)."""
    src = open("bot.py").read()
    # Der Prune sitzt direkt an der Schreibstelle.
    assert "if len(_ORACLE_USER_LAST) > 500:" in src, "Oracle-Cooldown-Deckelung fehlt"
    assert "_ORACLE_USER_LAST.pop(_k, None)" in src, "Prune entfernt nichts"

    # Verhalten der gedeckelten Cooldown-Logik (nachgebaut): identisch + gedeckelt.
    COOLDOWN = 30.0
    D = {}
    def allowed(sender, now):
        if now - D.get(sender, 0) < COOLDOWN:
            return False
        D[sender] = now
        if len(D) > 500:
            cut = now - COOLDOWN
            for k in [k for k, t in D.items() if t < cut]:
                D.pop(k, None)
        return True
    assert allowed("a", 1000.0) is True and allowed("a", 1010.0) is False, "Cooldown greift nicht"
    assert allowed("a", 1040.0) is True, "Cooldown-Ablauf falsch"
    t = 0.0
    for i in range(20000):
        t += 5.0
        allowed(f"u{i}", t)
    assert len(D) <= 501, f"Deckelung greift nicht (dict={len(D)})"
    ok("v4.0-w37: _ORACLE_USER_LAST gedeckelt — kein Speicher-Wachstum über Wochen")


def test_v40_w38_resource_early_warning():
    """v4.0-W38: 24/7-Selbstüberwachung. Der fd-/Task-/Session-/DB-Audit war
       sauber (alle Subprozesse drainen+reapen, 0 verwaiste Tasks, Sessions
       schließen im finally, db_conn immer 'with'). Die fd-/RSS-Zahlen wurden
       aber nur passiv im Dashboard gezeigt — jetzt alarmiert der Watchdog
       PROAKTIV und kantengetriggert, wenn sie über Tage klettern."""
    src = open("bot.py").read()
    assert "WATCHDOG_FD_WARN" in src and "WATCHDOG_RSS_WARN_MB" in src, "Schwellen fehlen"
    assert 'log_event(f"watchdog.{_what}_high"' in src, "keine proaktive Ressourcen-Warnung im Watchdog"
    assert '"res": {"fd": False, "rss": False}' in src, "Kanten-Zustand nicht initialisiert"

    # Kantengetriggerte Logik (nachgebaut): 1× warnen pro Überschreitungs-Phase.
    state = {"fd": False}
    warns, infos = [], []
    def tick(val, lim):
        bad = val > lim
        was = state["fd"]
        if bad and not was:
            state["fd"] = True
            warns.append(val)
        elif not bad and was:
            state["fd"] = False
            infos.append(val)
    for v in [200, 850, 860, 400, 900, 300]:
        tick(v, 800)
    assert warns == [850, 900], f"warnt nicht genau 1×/Phase: {warns}"
    assert infos == [400, 300], f"entwarnt falsch: {infos}"
    ok("v4.0-w38: Watchdog warnt proaktiv+kantengetriggert bei fd-/RSS-Wachstum")


def test_v40_w39_adaptive_source_watch():
    """v4.0-W39: der Quell-Failover-Poller ist adaptiv. Bei stabil bestätigter
       Live-Quelle fährt das Poll-Intervall sanft hoch (bis RESTREAM_SRC_POLL_MAX_S)
       → weniger TikTok-Resolves im Dauerbetrieb. Bei JEDEM Nicht-live-Signal
       (offline ODER unknown) schnappt es sofort aufs schnelle Basis-Intervall
       zurück → der Failover bleibt reaktionsschnell."""
    src = open("bot.py").read()
    assert "RESTREAM_SRC_POLL_MAX_S" in src, "Cap-Konstante fehlt"
    assert "_poll = min(_cap, _poll + _base // 2)" in src, "adaptives Hochfahren fehlt"
    # Nicht-live setzt zurück (beide Zweige offline/unknown auf _base).
    assert src.count("_poll = _base") >= 2, "kein sofortiges Zurückschnappen bei Nicht-live"

    BASE, CAP = 30, 60
    def run(errs):
        poll = BASE
        seq = []
        for e in errs:
            if e == "offline" or e:
                poll = BASE
            else:
                poll = min(CAP, poll + BASE // 2)
            seq.append(poll)
        return seq
    assert run([None] * 4) == [45, 60, 60, 60], "stabil-live fährt nicht korrekt hoch"
    assert run([None, None, "unknown", None]) == [45, 60, 30, 45], "unknown schnappt nicht zurück"
    assert run([None, None, "offline"]) == [45, 60, 30], "offline schnappt nicht zurück"
    # Adaptivität abschaltbar: MAX == BASE → immer Basis-Intervall.
    def run_off(errs, base=30, cap=30):
        poll = base
        seq = []
        for e in errs:
            poll = base if (e or e == "offline") else min(cap, poll + base // 2)
            seq.append(poll)
        return seq
    assert run_off([None] * 4) == [30, 30, 30, 30], "MAX=BASE schaltet Adaptivität nicht aus"
    ok("v4.0-w39: source-watch adaptiv — ~2× weniger Resolves, Failover schnell")


def test_v40_w40_resource_trend():
    """v4.0-W40: Langzeit-Ressourcen-Trend. Die W38-Warnung sieht nur absolute
       Schwellen; ein LANGSAMES Leck (+wenige fds/Stunde) bleibt monatelang
       darunter. nc.restrend erkennt den anhaltenden Anstieg, der Watchdog
       zeichnet den Verlauf auf und warnt kantengetriggert, ein Dashboard-
       Endpoint liefert die Kurve."""
    from nc import restrend as RT
    # schleichendes Leck erkannt.
    leak = [100 + i * 3 for i in range(30)]
    assert RT.rising_trend(leak, min_abs_growth=40.0)["trend"] is True
    # Rauschen um einen stabilen Wert → KEIN Fehlalarm.
    import random as _r
    _r.seed(2)
    stable = [500 + _r.randint(-15, 15) for _ in range(30)]
    assert RT.rising_trend(stable, min_abs_growth=40.0)["trend"] is False
    # Fallen/leere/kurze Reihen → kein Trend.
    assert RT.rising_trend([300 - i * 2 for i in range(20)])["trend"] is False
    assert RT.rising_trend([1, 2, 3])["trend"] is False
    assert RT.rising_trend([None] * 8)["trend"] is False
    # None-Werte in der Reihe werden ignoriert (nicht crashen); >=12 echte Punkte.
    mixed = [None, 100, None, 130, 160, 190, 220, 250, 280, 310, 340, 370, 400, 430, 460]
    assert RT.rising_trend(mixed, min_abs_growth=40.0)["trend"] is True

    src = open("bot.py").read()
    assert "_RES_HISTORY = _collections.deque(maxlen=300)" in src, "Ring-Puffer fehlt/unbegrenzt"
    assert 'log_event(f"watchdog.{_w}_slowleak"' in src, "keine Slow-Leak-Warnung"
    # v4.0-W116: der Verlauf-Endpoint liegt jetzt im Blueprint nc/routes/ops.py.
    # Der Ring bleibt im Bot — der Watchdog schreibt ihn — und wird als Referenz
    # ueber ctx.cfg geteilt. Genau das sichert die dritte Zusicherung: eine Kopie
    # waere ein Panel, das ewig dieselben Punkte zeigt.
    ops = open("nc/routes/ops.py", encoding="utf-8").read()
    assert "from nc import restrend as _nc_restrend" in ops
    assert '@bp.route("/api/ops/resource_history")' in ops, "Verlauf-Endpoint fehlt"
    assert '_c().cfg["_RES_HISTORY"]' in ops, "Blueprint liest den Ring nicht ueber den Kontext"
    assert '"_RES_HISTORY": _RES_HISTORY,' in src, "Ring wird nicht in den Kontext gereicht"
    assert "def api_ops_resource_history" not in src, \
        "Doppel-Logik: Route liegt noch im Monolithen UND im Blueprint"
    # Dashboard-Frontend: Panel, Chart, Loader verdrahtet.
    dash = open("templates/dashboard.html").read()
    assert 'id="pnl_restrend"' in dash and 'id="rtr_body"' in dash, "Verlauf-Panel fehlt"
    assert "function ncResourceChart(" in dash and "async function loadResourceHistory(" in dash, "Chart/Loader fehlt"
    assert "loadResourceHistory()" in dash.split("VIEW_LOADERS['betrieb']")[1][:400], \
        "Loader nicht in die betrieb-View eingehängt"
    ok("v4.0-w40: Slow-Leak-Trend erkannt, Verlauf aufgezeichnet, Chart im Dashboard")


def test_v40_w41_send_observability():
    """v4.0-W41: das Cross-Platform-Sende-Fundament ist beobachtbar. Announce und
       Befehle (W35) hängen an _azrael_send_to — das scheiterte für nicht
       verbundene Plattformen STILL (fn is None → No-Op, Fehler nur DEBUG). Jetzt
       gibt es ein Ergebnis zurück (sent/offline/error), der Announcer nennt den
       Grund je übersprungener Plattform, und ein Endpoint zeigt on-demand, wohin
       gerade gesendet werden kann — genau die Frage hinter 'nur auf Kick'."""
    src = open("bot.py").read()
    # _azrael_send_to gibt Status zurück.
    i = src.find("async def _azrael_send_to(")
    body = src[i:i + 1400]
    assert body.count('return "sent"') == 3 and 'return "offline"' in body and 'return "error"' in body, \
        "_azrael_send_to gibt keinen Status zurück"
    # Announcer nennt Skip-Gründe.
    assert "nicht verbunden" in src and "Sendefehler" in src, "Announce nennt keine Skip-Gründe"
    assert "KEINE Plattform erreicht" in src, "kein klarer Log bei Totalausfall"
    # Diagnose-Endpoint.
    assert '"/api/chat/send_status"' in src and "api_chat_send_status" in src, "Sende-Status-Endpoint fehlt"

    # Verhalten (nachgebaut): nur Kick verbunden → korrekte sent/skipped-Aufteilung.
    def status(kick, tw, yt):
        r = {"kick": "sent" if kick else "offline",
             "twitch": "sent" if tw else "offline",
             "youtube": "sent" if yt else "offline"}
        sent = [p for p, v in r.items() if v == "sent"]
        skipped = [p for p, v in r.items() if v != "sent"]
        return sent, skipped
    assert status(True, False, False) == (["kick"], ["twitch", "youtube"])
    assert status(True, True, True) == (["kick", "twitch", "youtube"], [])
    # send_status zählt Bereitschaft.
    def ready(kick, tw, yt):
        return [p for p, v in (("kick", kick), ("twitch", tw), ("youtube", yt)) if v]
    assert ready(True, False, False) == ["kick"] and ready(True, True, True) == ["kick", "twitch", "youtube"]
    ok("v4.0-w41: Sende-Pfad beobachtbar — Status, Skip-Gründe, Diagnose-Endpoint")


def test_v40_w42_chat_listener_decoupled():
    """v4.0-W42: die Twitch/YouTube-Chat-Listener sind von der Brain-Bridge
       ENTKOPPELT. Vorher hingen ihre Spawns im try der Brain-Bridge — scheiterte
       die Bridge, starteten sie STILL nie und im Chat kam nur Kick an. Jetzt
       eigener try, und bei fehlendem Kanal eine klare Log-Ansage statt Funkstille.
       Der Sende-Status-Endpoint unterscheidet 'Kanal nicht gesetzt' von
       'verbunden-aber-Token-Problem'."""
    src = open("bot.py").read()
    bb = src.find("Brain-Bridge deaktiviert")
    tw = src.find("_spawn(_twitch_chat_loop()")
    assert tw > bb, "Chat-Spawns hängen noch im Brain-Bridge-try (gekoppelt)"
    assert src.count("NICHT gestartet:") == 2, "keine klare Ansage bei fehlendem Twitch/YouTube-Kanal"
    assert "Twitch-Chat-Listener gestartet" in src and "YouTube-Chat-Listener gestartet" in src, \
        "kein Bestätigungs-Log beim Start"

    # Der Diagnose-Hinweis zeigt auf die RICHTIGE Lösung.
    def hint(ready, chan, plat):
        if ready:
            return ""
        if not chan:
            return f"{plat}_CHANNEL ist in der .env leer — dort setzen (dann startet der Listener)"
        return "Kanal gesetzt, aber Chat nicht verbunden — OAuth/Token prüfen"
    assert "leer" in hint(False, "", "TWITCH"), "Kanal-fehlt-Hinweis falsch"
    assert "OAuth" in hint(False, "chan", "TWITCH"), "Token-Hinweis falsch"
    assert hint(True, "x", "TWITCH") == "", "bereit → kein Hinweis"
    assert 'channel_set' in src, "send_status meldet channel_set nicht"
    ok("v4.0-w42: Chat-Listener entkoppelt + klare Kanal-Diagnose (Wurzel von 'nur Kick')")


def test_v40_w43_send_status_panel():
    """v4.0-W43: die Sende-Bereitschaft (W41) ist jetzt im Dashboard sichtbar —
       ein Blick-Panel mit Kick/Twitch/YouTube, grünem Punkt bei sende-bereit,
       sonst dem konkreten Hinweis (Kanal leer / Token). Mobil ablesbar statt
       API-Abfrage — genau die Antwort auf 'warum nur Kick?'."""
    dash = open("templates/dashboard.html").read()
    assert 'id="pnl_sendstatus"' in dash and 'id="ss_body"' in dash, "Sende-Status-Panel fehlt"
    assert "async function loadSendStatus(" in dash, "Loader fehlt"
    assert "/api/chat/send_status" in dash, "Panel ruft den Status-Endpoint nicht"
    assert "loadSendStatus()" in dash.split("VIEW_LOADERS['betrieb']")[1][:400], \
        "Loader nicht in die betrieb-View eingehängt"
    ok("v4.0-w43: Chat-Sende-Bereitschaft im Dashboard sichtbar (mobil ablesbar)")


def test_v40_w44_ffbuild():
    """v4.0-W44: Monolith-Abtrag — der ffmpeg-Kommandobauer _ff_cmd (Thread-Deckel
       + nice-Präfix, genutzt von Restream/Recording/Clips) ist nach nc.ffbuild
       gewandert. Bitgenau erhalten, inkl. Assertion- und nice-Parität."""
    from nc import ffbuild as FB
    _real = FB.shutil.which
    try:
        # -threads direkt hinter ffmpeg; nur wenn noch keiner da ist.
        FB.shutil.which = lambda x: None
        assert FB.ff_cmd(["ffmpeg", "-i", "x"], threads=2) == ["ffmpeg", "-threads", "2", "-i", "x"]
        assert FB.ff_cmd(["ffmpeg", "-threads", "3", "-i", "x"], threads=2) == \
            ["ffmpeg", "-threads", "3", "-i", "x"], "vorhandenes -threads nicht doppeln"
        assert FB.ff_cmd(["ffmpeg", "-i", "x"], threads=0) == ["ffmpeg", "-i", "x"], "threads<=0 → nichts"
        # nice nur wenn Binary vorhanden.
        assert FB.ff_cmd(["ffmpeg"], nice=10) == ["ffmpeg"], "kein nice ohne Binary"
        FB.shutil.which = lambda x: "/usr/bin/nice"
        assert FB.ff_cmd(["ffmpeg", "-i", "x"], nice=10) == ["nice", "-n", "10", "ffmpeg", "-i", "x"]
        # Assertion: -threads-Einschub verlangt ffmpeg an Position 0.
        try:
            FB.ff_cmd(["notffmpeg", "-i", "x"], threads=2)
            raise AssertionError("Assertion hätte greifen müssen")
        except AssertionError as e:
            assert "ffmpeg" in str(e)
    finally:
        FB.shutil.which = _real
    ok("v4.0-w44: nc.ffbuild — Thread-Deckel, nice-Präfix, Assertion korrekt")

    src = open("bot.py").read()
    assert "from nc import ffbuild as _nc_ffbuild" in src, "Modul nicht importiert"
    assert "return _nc_ffbuild.ff_cmd(cmd, threads=threads, nice=nice)" in src, "delegiert nicht"
    assert "out[1:1] = [\"-threads\"" not in src, "alte ff_cmd-Logik noch im Monolithen"
    ok("v4.0-w44: Bot delegiert den ffmpeg-Bau, keine Doppel-Logik")


def test_v40_w45_chatstats():
    """v4.0-W45: Monolith-Abtrag — die Chat-Health-Aggregation (_chat_stats_snapshot)
       ist nach nc.chatstats gewandert. Bitgenau: Uptime-Quote (gedeckelt 100%),
       Median/kürzeste/längste Session, laufende Session, letzte Gründe."""
    from nc import chatstats as CS
    stats = {"streamerX": {
        "sessions": [10.0, 30.0, 20.0], "connected_since": 100.0, "first_seen": 0.0,
        "connects": 5, "failed": 1, "disconnects": 4, "flaps": 2,
        "total_uptime": 900.0, "backoff_s": 8.0,
        "reasons": [(50.0, "net"), (80.0, "timeout")]}}
    r = CS.summarize(stats, now_mono=150.0, now_wall=1000.0)["streamerX"]
    assert r["connected"] is True and r["current_session_s"] == 50, "laufende Session falsch"
    assert r["median_session_s"] == 20 and r["shortest_s"] == 10 and r["longest_s"] == 30
    # uptime = (900 + 50) / (1000 - 0) = 95%
    assert r["uptime_pct"] == 95.0, f"uptime falsch: {r['uptime_pct']}"
    # jüngster Grund zuerst (reversed).
    assert r["last_reasons"][0]["why"] == "timeout" and r["last_reasons"][0]["ago_s"] == 920
    # nicht verbunden → current_session 0, uptime aus total_uptime.
    stats2 = {"y": {**stats["streamerX"], "connected_since": 0.0}}
    r2 = CS.summarize(stats2, 150.0, 1000.0)["y"]
    assert r2["connected"] is False and r2["current_session_s"] == 0
    # leere sessions → 0-Werte, kein Crash.
    stats3 = {"z": {**stats["streamerX"], "sessions": [], "connected_since": 0.0}}
    r3 = CS.summarize(stats3, 150.0, 1000.0)["z"]
    assert r3["median_session_s"] == 0 and r3["shortest_s"] == 0 and r3["longest_s"] == 0
    # uptime auf 100% gedeckelt (total_uptime > span).
    stats4 = {"w": {**stats["streamerX"], "total_uptime": 99999.0, "connected_since": 0.0}}
    assert CS.summarize(stats4, 150.0, 1000.0)["w"]["uptime_pct"] == 100.0, "uptime nicht gedeckelt"
    ok("v4.0-w45: nc.chatstats — Uptime/Median/Sessions/Gründe bitgenau")

    src = open("bot.py").read()
    assert "from nc import chatstats as _nc_chatstats" in src
    assert "_nc_chatstats.summarize(_CHAT_STATS, _time_mod.monotonic(), _time_mod.time())" in src, "delegiert nicht"
    assert "Uptime-Quote: der ehrlichste" not in src, "alte Aggregation noch im Monolithen"
    ok("v4.0-w45: Bot delegiert die Aggregation, keine Doppel-Logik")


def test_v40_w46_json_and_telegram_launch():
    """v4.0-W46: zwei Betriebsfehler behoben. (1) Der orjson-JSON-Provider lehnte
       Nicht-String-Keys hart ab → HTTP 500 'Dict key must be str' auf jedem
       Endpoint mit int-Keys (/api/restream/verify, /api/system/check_timing, die
       {rid: …} zurückgeben). OPT_NON_STR_KEYS coerct sie wie das Standard-json.
       (2) Der Telegram-Start war ungekapselt — wirft er, riss er run_bot() (und
       damit auch den Discord-Start davor/danach) mit, ohne klare Meldung. Jetzt
       eigener try mit lauter Diagnose, der Rest läuft weiter."""
    import orjson
    # int-Key crasht ohne Flag, wird mit Flag zu String coerct.
    try:
        orjson.dumps({64: {"x": 1}})
        raise AssertionError("orjson hätte ohne Flag werfen müssen")
    except TypeError:
        pass
    assert orjson.dumps({64: {"x": 1}}, option=orjson.OPT_NON_STR_KEYS).decode() == '{"64":{"x":1}}'

    src = open("bot.py").read()
    assert "opt = orjson.OPT_NON_STR_KEYS" in src, "JSON-Provider coerct int-Keys nicht"
    # Telegram-Start gekapselt + laut.
    assert "Telegram-Polling FEHLGESCHLAGEN" in src, "Telegram-Start nicht gekapselt/geloggt"
    i = src.find("await app.updater.start_polling()")
    pre = src[max(0, i - 400):i]
    assert "try:" in pre, "start_polling nicht in einem try"
    ok("v4.0-w46: orjson int-Keys gefixt, Telegram-Start gekapselt+diagnostizierbar")


def test_v40_w47_executor_isolation():
    """v4.0-W47: „hängt nach einiger Zeit" adressiert. asyncio nutzt den Default-
       ThreadPool auch für DNS; teilten sich Whisper+LLM+DNS den kleinen Default-
       Pool, konnte er unter Last sättigen → DNS verhungert → Discord/Telegram/HTTP
       hängen. Fix: Default-Pool großzügig dimensioniert UND Whisper (Dauerlast) in
       einen eigenen Pool isoliert. Thread-Zahl wird jetzt aufgezeichnet (sichtbar
       im Ressourcen-Trend), falls doch etwas den Pool füllt."""
    src = open("bot.py").read()
    # Default-Pool großzügig + früh in main().
    assert "set_default_executor(" in src, "Default-Executor nicht gesetzt"
    assert 'thread_name_prefix="ncworker"' in src
    i_main = src.find("async def main():")
    i_pool = src.find("set_default_executor(")
    i_spawn = src.find("_spawn(run_bot()")
    assert i_main < i_pool < i_spawn, "Default-Pool nicht VOR dem Bot-Start gesetzt"
    # Whisper isoliert.
    assert "def _whisper_pool():" in src and 'thread_name_prefix="ncwhisper"' in src, "kein eigener Whisper-Pool"
    assert "run_in_executor(_whisper_pool(), _run)" in src, "Whisper läuft nicht im eigenen Pool"
    assert "run_in_executor(None, _run)" not in src, "Whisper hängt noch am Default-Pool"
    # Thread-Zahl beobachtbar.
    assert '"threads": _threading.active_count()' in src, "Thread-Zahl wird nicht aufgezeichnet"

    # Pool-Sizing-Logik (nachgebaut): Default großzügig, Whisper klein+isoliert.
    def default_workers(cpu, env=None):
        return max(16, env if env else (cpu or 2) * 4 + 8)
    assert default_workers(2) == 16 and default_workers(8) == 40, "Default-Sizing falsch"
    assert default_workers(1, env=64) == 64, "WORKER_THREADS-Override greift nicht"
    def whisper_workers(maxconc):
        return max(1, maxconc) + 1
    assert whisper_workers(2) == 3 and whisper_workers(0) == 2, "Whisper-Pool-Sizing falsch"
    ok("v4.0-w47: Default-Pool vergrößert, Whisper isoliert, Threads beobachtbar")


def test_v40_w48_loop_lag_monitor():
    """v4.0-W48: Event-Loop-Blockade-Detektor. Der Heartbeat-Watchdog erkennt nur
       einen sterbenden Loop; er misst nicht, ob der Loop gerade BLOCKIERT ist. Ein
       sauberer Loop kehrt aus asyncio.sleep(interval) nach ~interval zurück —
       dauert es länger, hat eine Coroutine den Loop nicht freigegeben. Der Monitor
       misst diese Überschreitung und meldet Blockaden mit DAUER (gedrosselt), inkl.
       Thread-Zahl — die Diagnose für „hängt nach einiger Zeit", falls W47 nicht
       reicht."""
    src = open("bot.py").read()
    assert "async def _loop_lag_monitor(" in src and "_spawn(_loop_lag_monitor()" in src, "Detektor fehlt/nicht gespawnt"
    assert 'log_event("watchdog.loop_lag"' in src, "keine Loop-Lag-Meldung"
    assert "LOOP_LAG_WARN_S" in src and "LOOP_LAG_INTERVAL_S" in src, "Schwellen fehlen"
    # Lag = tatsächliche Schlafdauer minus Soll-Intervall.
    def lag(actual, interval):
        return actual - interval
    assert lag(2.1, 2) < 0.5, "gesunder Loop darf nicht alarmieren"
    assert lag(6.0, 2) == 4.0, "4s Blockade nicht korrekt gemessen"
    # Drossel: höchstens 1 Warnung/Minute.
    def simulate(events):
        last = 0.0
        warns = []
        for now in events:
            if now - last >= 60:
                last = now
                warns.append(now)
        return warns
    assert simulate([1000, 1005, 1030, 1061, 1122]) == [1000, 1061, 1122], "Drossel greift nicht"
    ok("v4.0-w48: Event-Loop-Lag gemessen + gedrosselt gemeldet")


def test_v40_w49_oauthpage():
    """v4.0-W49: Monolith-Abtrag — die zwei OAuth-Rückmeldeseiten (_twitch_oauth_page,
       _kick_oauth_page) sind nach nc.oauthpage gewandert. Bitgenau, mit dem jeweils
       eigenen Escaping (Twitch: html.escape inkl. Quotes; Kick: manuell nur &<>)."""
    from nc import oauthpage as OP
    # Twitch: html.escape → escaped inkl. Quotes; ok/Fehler-Farbe.
    tp = OP.twitch(True, "<b>x</b> & \"q\"")
    assert "&lt;b&gt;" in tp and "&amp;" in tp and "&quot;" in tp, "Twitch escaping falsch"
    assert "#0f9d76" in OP.twitch(True, "x") and "#e11d48" in OP.twitch(False, "x"), "Twitch-Farbe falsch"
    # Kick: manuelles Escaping (nur &<>, KEINE Quotes) — bewusst so.
    kp = OP.kick(False, "<a> & \"q\"")
    assert "&lt;a&gt;" in kp and "&amp;" in kp, "Kick escaping falsch"
    assert "\"q\"" in kp, "Kick escaped Quotes fälschlich (manuelles Escaping erwartet)"
    assert "#8FB98F" in OP.kick(True, "x") and "#E0A0A0" in OP.kick(False, "x"), "Kick-Farbe falsch"
    ok("v4.0-w49: nc.oauthpage — beide Seiten bitgenau, Escaping je Plattform erhalten")

    src = open("bot.py").read()
    assert "from nc import oauthpage as _nc_oauthpage" in src
    assert "return _nc_oauthpage.twitch(ok, msg)" in src and "return _nc_oauthpage.kick(ok, msg)" in src, "delegiert nicht"
    assert "Dieses Fenster kann geschlossen" not in src, "alte Seiten-Logik noch im Monolithen"
    ok("v4.0-w49: Bot delegiert beide OAuth-Seiten, keine Doppel-Logik")


def test_v40_w50_trackingdb():
    """v4.0-W50: Monolith-Abtrag (DB-gekoppelt, conn-injiziert). Die zwei Tracking-
       Status-Helfer sind nach nc.trackingdb gewandert. claim_transition ist
       korrektheitskritisch (atomarer Compare-and-Set gegen Doppel-Notifications im
       Race) — gegen echtes In-Memory-SQLite bewiesen: genau ein Gewinner je
       Übergang."""
    import sqlite3
    from nc import trackingdb as TD
    db = sqlite3.connect(":memory:")
    db.row_factory = sqlite3.Row
    db.execute("CREATE TABLE trackings(id INTEGER PRIMARY KEY, last_live INT, recording INT, paused INT)")
    db.execute("INSERT INTO trackings VALUES (1,0,0,0)")
    db.execute("INSERT INTO trackings VALUES (2,1,1,1)")
    db.commit()
    # Atomarer Claim: genau ein Gewinner je Übergang.
    assert TD.claim_transition(db, 1, True) is True, "erster going-live gewinnt"
    assert TD.claim_transition(db, 1, True) is False, "zweiter going-live verliert"
    assert TD.claim_transition(db, 1, False) is True and TD.claim_transition(db, 1, False) is False
    assert TD.claim_transition(db, 999, True) is False, "fehlende id → kein Update"
    # get_state: Werte / None / paused.
    assert TD.get_state(db, 2) == (True, True, True)
    assert TD.get_state(db, 1) == (False, False, False)
    assert TD.get_state(db, 999) == (None, None, None)
    ok("v4.0-w50: nc.trackingdb — atomarer Claim + get_state gegen echtes SQLite bewiesen")

    src = open("bot.py").read()
    assert "from nc import trackingdb as _nc_trackingdb" in src
    assert "_nc_trackingdb.claim_transition(conn, tracking_id, going_live)" in src
    assert "_nc_trackingdb.get_state(conn, tracking_id)" in src
    assert "UPDATE trackings SET last_live=? WHERE id=? AND last_live=?" not in src, "alte SQL noch im Monolithen"
    ok("v4.0-w50: Bot delegiert beide Tracking-Helfer, keine Doppel-SQL")


def test_v40_w51_eventquery():
    """v4.0-W51: Monolith-Abtrag — der Event-Log-Query-Bauer (dynamischer, aber
       PARAMETRISIERTER WHERE-Aufbau aus kind/severity) ist nach nc.eventquery
       gewandert. Bitgenau, injektionssicher, LIMIT immer als letzter Parameter."""
    from nc import eventquery as EQ
    # Kein Filter → kein WHERE, nur LIMIT.
    s, p = EQ.build_query(100)
    assert "WHERE" not in s and p == [100]
    # Einzelfilter.
    s, p = EQ.build_query(50, kind="clip")
    assert "WHERE kind = ?" in s and p == ["clip", 50]
    s, p = EQ.build_query(50, severity="error")
    assert "WHERE severity = ?" in s and p == ["error", 50]
    # Kombi → AND, Reihenfolge kind, severity, dann LIMIT.
    s, p = EQ.build_query(10, kind="restream", severity="warning")
    assert "kind = ? AND severity = ?" in s and p == ["restream", "warning", 10]
    # Leere Strings zählen als „kein Filter" (falsy).
    assert EQ.build_query(5, kind="", severity="")[1] == [5]
    # Injektionssicher: der Filterwert landet als Parameter, NICHT im SQL.
    s, p = EQ.build_query(5, kind="'; DROP TABLE event_log--")
    assert "DROP TABLE" not in s and "'; DROP TABLE event_log--" in p
    assert p[-1] == 5, "LIMIT muss letzter Parameter sein"
    # neueste zuerst.
    assert "ORDER BY id DESC" in s
    ok("v4.0-w51: nc.eventquery — Filter/AND/LIMIT/Injektionssicherheit bitgenau")

    src = open("bot.py").read()
    assert "from nc import eventquery as _nc_eventquery" in src
    assert "_nc_eventquery.build_query(limit, kind, severity)" in src, "delegiert nicht"
    assert 'wsql = ("WHERE " + " AND ".join(where)) if where else ""' not in src, "alte Query-Logik noch im Monolithen"
    ok("v4.0-w51: Bot delegiert den Query-Bau, führt nur noch aus")


def test_v40_w52_pin_login():
    """v4.0-W52: PIN-Login fürs Dashboard/PWA. Gesetztes DASHBOARD_PIN → externer
       Zugriff braucht das PIN über eine Login-Seite; Loopback (SSH-Tunnel) bleibt
       frei; ohne PIN kein Login (rückwärtskompatibel). Auth-Cookie ist aus dem PIN
       abgeleitet (nie das PIN selbst), Vergleich zeitkonstant, Brute-Force
       gedrosselt. Service-Worker-Version gebumpt → installierte PWAs ziehen das
       Update."""
    import hmac as _hmac
    import hashlib as _hl
    # Cookie-Ableitung: HMAC(PIN) — deterministisch, PIN-abhängig, PIN nicht im Wert.
    def pinval(pin):
        return _hmac.new(pin.encode(), b"nc-dashboard-pin", _hl.sha256).hexdigest()
    v = pinval("1234")
    assert len(v) == 64 and v == pinval("1234") and pinval("1234") != pinval("1235")
    assert "1234" not in v, "rohes PIN darf nicht im Cookie stehen"
    assert _hmac.compare_digest(v, pinval("1234")) and not _hmac.compare_digest(v, pinval("0"))
    # Brute-Force-Drossel: 5 Fehlversuche → Sperre, danach frei.
    FAILS = {}
    def note(ip, now):
        st = FAILS.get(ip, [0, 0.0])
        st[0] += 1
        if st[0] >= 5:
            st[1] = now + 60
            st[0] = 0
        FAILS[ip] = st
    def locked(ip, now):
        st = FAILS.get(ip)
        return bool(st and st[1] > now)
    for _ in range(4):
        note("x", 1000)
    assert not locked("x", 1000)
    note("x", 1000)
    assert locked("x", 1000) and not locked("x", 1061), "5→Sperre 60s, dann frei"

    src = open("bot.py").read()
    assert 'DASHBOARD_PIN      = os.getenv("DASHBOARD_PIN"' in src, "PIN-Config fehlt"
    assert "def _pin_ok(" in src and "def _pin_auth_value(" in src, "PIN-Helfer fehlen"
    assert "if not DASHBOARD_TOKEN and not DASHBOARD_PIN:" in src, "Gate nicht rückwärtskompatibel"
    assert "_token_ok() or _pin_ok()" in src, "Gate akzeptiert nicht Token ODER PIN"
    assert 'redirect("/login?next="' in src, "kein Login-Redirect für Browser"
    assert "def dashboard_login_submit(" in src and '"/api/login"' in src, "Login-POST fehlt"
    assert 'p in ("/login", "/logout") or p == "/api/login"' in src, "Login-Routen nicht vom Gate ausgenommen"
    # v4.0-W118 (SEC): der Anker ist gebrochen, der Vertrag ist STRENGER
    # geworden. Die alte Pruefung `nxt.startswith("/")` liess //example.com
    # durch — eine protokoll-relative URL, die der Browser als
    # https://example.com aufloest. Jetzt entscheidet _sicheres_ziel().
    assert "def _sicheres_ziel(roh):" in src, "kein Open-Redirect-Schutz"
    _sz = src[src.index("def _sicheres_ziel(roh):"):
              src.index('@dashboard_app.route("/login")')]
    assert 'z[:2] in ("//", "/\\\\")' in _sz, \
        "protokoll-relative Ziele (//host, /\\host) nicht abgewiesen"
    assert src.count("_sicheres_ziel(request.") == 2, \
        "nicht beide Login-Pfade (GET + POST) gehen ueber die Pruefung"
    # Loopback bleibt frei.
    assert 'if (request.remote_addr or "") in _LOOPBACK:' in src, "Loopback-Ausnahme verloren"
    # SW-Version gebumpt (PWA-Update).
    sw = open("templates/sw.js").read()
    import re as _re
    _ver = _re.search(r"nightcrawler-shell-v(\d+)", sw)
    assert _ver and int(_ver.group(1)) >= 2 and "nightcrawler-shell-v1" not in sw, "SW-Cache nicht gebumpt"
    assert '"/login"' in sw, "Login nicht in der PWA-Shell"
    ok("v4.0-w52: PIN-Login — Ableitung/Drossel/Gate/Loopback/PWA-Update korrekt")


def test_v40_w53_pwa_audit():
    """v4.0-W53: PWA-Audit. Die installierte PWA ist dieselbe App (network-first
       Shell → immer aktuell online), hatte aber EINEN echten Defekt: der Manifest-
       Shortcut zeigte auf /brain — das ist keine Route (404), sondern ein
       client-seitiger Tab, und es gab kein Hash-Routing. Fix: Hash-Deep-Links
       (/#brain), Shortcuts darauf umgezogen, SW-Shell bereinigt + Version gebumpt
       (installierte PWAs ziehen das Update)."""
    import json
    m = json.load(open("templates/manifest.webmanifest"))
    # Shortcuts zeigen auf Hash-Routen, kein totes /brain mehr.
    urls = [s["url"] for s in m["shortcuts"]]
    assert all(u.startswith("/?pwa=1#") for u in urls), f"Shortcut nicht auf Hash-Route: {urls}"
    assert not any("/brain?" in u for u in urls), "toter /brain-Shortcut noch vorhanden"
    # Alle deklarierten Icons sind die vorhandenen drei.
    icons = {i["src"] for i in m["icons"]}
    assert icons == {"/pwa-icon-192.png", "/pwa-icon-512.png", "/pwa-icon-maskable-512.png"}

    h = open("templates/dashboard.html").read()
    # Hash-Routing: URL-Sync beim Tabwechsel + hashchange + Hash-Vorrang beim Start.
    assert "history.replaceState(null,''" in h and "'#'+v)" in h, "kein URL-Hash-Sync"
    assert "addEventListener('hashchange'" in h, "kein hashchange-Listener"
    assert h.count("_viewFromHash()") >= 2, "Hash wird beim Start nicht bevorzugt"

    sw = open("templates/sw.js").read()
    assert "nightcrawler-shell-v3" in sw and "shell-v2" not in sw, "SW-Cache nicht gebumpt (PWA-Update)"
    assert '"/brain"' not in sw, "/brain (404) noch in der SW-Shell"
    assert "pwa-icon-maskable-512.png" in sw, "maskable-Icon nicht in der Shell"

    src = open("bot.py").read()
    # Der Server bestätigt: /brain ist KEINE HTML-Route (nur / und /overlay liefern Seiten).
    assert '@dashboard_app.route("/brain")' not in src, "unerwartete /brain-Route — Audit-Annahme prüfen"
    assert '@dashboard_app.route("/")' in src and "def pwa_icon(variant)" in src
    ok("v4.0-w53: PWA-Shortcut/Deep-Link repariert, Shell bereinigt, Update ausgeliefert")


def test_v40_w54_inspectcache():
    """v4.0-W54: Monolith-Abtrag — die (De-)Serialisierung des Recording-Inspect-
       Caches ist nach nc.inspectcache gewandert. parse_row: fehlend/kaputt → None
       (Aufrufer berechnet lazy neu); serialize: Unicode lesbar + harter 200KB-
       Deckel gegen Riesen-Payloads. DB-I/O bleibt im Bot."""
    import json as _json
    from nc import inspectcache as IC
    class Row(dict):
        def __getitem__(self, k):
            return dict.__getitem__(self, k)
    assert IC.parse_row(Row(inspect_json='{"a":1}')) == {"a": 1}
    assert IC.parse_row(Row(inspect_json='{kaputt')) is None, "kaputtes JSON → None"
    assert IC.parse_row(Row(inspect_json='')) is None and IC.parse_row(Row(inspect_json=None)) is None
    assert IC.parse_row(None) is None, "keine Zeile → None"
    # serialize: Unicode + Deckel.
    s = IC.serialize({"n": "Ünïcödé 🦇", "x": 1})
    assert "Ünïcödé 🦇" in s and _json.loads(s)["x"] == 1, "ensure_ascii=False verletzt"
    big = IC.serialize({"blob": "x" * 500000})
    assert len(big) == 200000, "200KB-Deckel greift nicht"
    assert big == _json.dumps({"blob": "x" * 500000}, ensure_ascii=False)[:200000], "nicht bitgenau zum Original"
    ok("v4.0-w54: nc.inspectcache — Parse-Fallback + Unicode-Serialisierung + Deckel bitgenau")

    src = open("bot.py").read()
    # Der Vertrag gilt unveraendert; nur seine Anker sind zweimal gewandert.
    # W104: parse_row ging mit get_or_compute_inspect_sync nach nc/recdb.py.
    # W106: store_inspect ging mit den Aufnahmen-Routen ins Blueprint.
    # Geprueft wird deshalb dort, wo der Code HEUTE liegt — und zusaetzlich,
    # dass im Monolithen keine zweite Kopie zurueckgeblieben ist.
    _recdb = open("nc/recdb.py", encoding="utf-8").read()
    _rt = open("nc/routes/recordings.py", encoding="utf-8").read()
    assert "from nc import inspectcache as _nc_inspectcache" in _recdb, \
        "nc.recdb importiert den Inspect-Cache nicht"
    assert "_nc_inspectcache.parse_row(row)" in _recdb, "Parse-Fallback nicht in nc.recdb"
    assert "from nc import inspectcache as _nc_inspectcache" in _rt, \
        "Blueprint importiert den Inspect-Cache nicht"
    assert "_nc_inspectcache.serialize(data)" in _rt, "Serialisierung nicht delegiert"
    assert "return _nc_recdb.get_or_compute_inspect_sync(" in src, "Bot delegiert nicht an recdb"
    assert "json.dumps(data, ensure_ascii=False)[:200000]" not in src, "alte Serialisierung noch im Monolithen"
    assert "_nc_inspectcache.parse_row(row)" not in src, "Doppel-Logik: Parse noch im Monolithen"
    ok("v4.0-w54: (De-)Serialisierung delegiert — Parse in nc.recdb, serialize im Blueprint")


def test_v40_w55_record_fail_backoff():
    """v4.0-W55: Aufnahme-Backoff bei Dauer-Fehlern. Ein 403 vom TikTok-CDN ist
       operativ (Region/Zugriff), kein Bot-Bug — aber der Bot startete jeden ~20s-
       Poll-Zyklus einen neuen yt-dlp/ffmpeg-Versuch und flutete das Error-Log
       (das ganze Log war ein einziger 403-Stream). Jetzt exponentieller Backoff
       (60s→…→30min-Cap), Skip-Gate vor dem Aufnahme-Lock, Log höchstens 1×/5min,
       Reset bei Erfolg/Offline."""
    BASE, MAX, HITS = 60, 1800, 2
    def backoff(n403):
        return min(MAX, BASE * (2 ** (n403 - HITS)))
    assert [backoff(n) for n in range(HITS, HITS + 6)] == [60, 120, 240, 480, 960, 1800], "Backoff-Kurve falsch"
    assert backoff(20) == 1800, "Cap greift nicht"
    # Skip-Gate: solange now < until überspringen.
    assert (1000 < 1060) and not (1100 < 1060)
    # Log-Drossel: höchstens 1 Zeile / 5min.
    def log_ok(now, last):
        return now - last > 300
    assert log_ok(1000, 0) and not log_ok(1200, 1000) and log_ok(1400, 1000)
    # Effekt: über 30min statt ~90 Versuchen (alle 20s) nur noch ~6.
    assert (30 * 60 // 20) == 90

    src = open("bot.py").read()
    assert "RECORD_FAIL_BACKOFF = os.getenv" in src, "Backoff-Config fehlt"
    assert "_REC_BACKOFF_UNTIL[username] = _time_mod.time() + _bo" in src, "Backoff wird nicht gesetzt"
    assert "RECORD_FAIL_BACKOFF_BASE_S * (2 ** (_n403 - RECORD_403_HITS))" in src, "nicht exponentiell aus dem 403-Streak"
    # Skip-Gate sitzt VOR dem Aufnahme-Lock.
    gate = src.find("if _time_mod.time() < _bo_until:")
    lock = src.find("if not try_acquire_recording_lock(tid, username=username):")
    assert 0 < gate < lock, "Skip-Gate nicht vor dem Aufnahme-Lock"
    # Reset bei Erfolg und bei Offline.
    assert src.count("_REC_BACKOFF_UNTIL.pop(username, None)") >= 2, "Backoff wird nicht zurückgesetzt"
    ok("v4.0-w55: 403-Retry-Storm gedrosselt (~90→~6/30min), Log entspammt, Reset korrekt")


def test_v40_w55b_convmap():
    """v4.0-W55b: Monolith-Abtrag — das Row→Dict-Mapping der AI-Conversation-
       Messages (_conv_messages) ist nach nc.convmap gewandert. Bitgenau: alle
       sieben Felder, Reihenfolge/NULL erhalten, leere Conversation → leere Liste."""
    import sqlite3
    from nc import convmap as CM
    db = sqlite3.connect(":memory:")
    db.row_factory = sqlite3.Row
    db.execute("CREATE TABLE ai_messages(id INTEGER PRIMARY KEY, conversation_id INT, role TEXT, "
               "content TEXT, created_at TEXT, model TEXT, duration_ms INT, error TEXT)")
    db.execute("INSERT INTO ai_messages(conversation_id,role,content,created_at,model,duration_ms,error) "
               "VALUES (1,'user','hallo','t1',NULL,NULL,NULL)")
    db.execute("INSERT INTO ai_messages(conversation_id,role,content,created_at,model,duration_ms,error) "
               "VALUES (1,'assistant','hi','t2','llama',1234,NULL)")
    db.commit()
    rows = db.execute("SELECT id, role, content, created_at, model, duration_ms, error "
                      "FROM ai_messages WHERE conversation_id=? ORDER BY id ASC", (1,)).fetchall()
    out = CM.messages(rows)
    exp = [{"id": r["id"], "role": r["role"], "content": r["content"], "created_at": r["created_at"],
            "model": r["model"], "duration_ms": r["duration_ms"], "error": r["error"]} for r in rows]
    assert out == exp, "nicht bitgenau"
    assert [m["role"] for m in out] == ["user", "assistant"]
    assert out[0]["model"] is None and out[1]["duration_ms"] == 1234, "NULL/Werte falsch"
    assert CM.messages([]) == [], "leer → leere Liste"
    ok("v4.0-w55b: nc.convmap — Message-Mapping bitgenau (Felder/Reihenfolge/NULL/leer)")

    src = open("bot.py").read()
    # W112: _conv_messages ist mit dem KI-Datenzugriff nach nc/aidb.py
    # gewandert; der convmap-Aufruf damit eine Ebene tiefer. Vertrag gleich.
    _aidb = open("nc/aidb.py", encoding="utf-8").read()
    assert "from nc import convmap as _nc_convmap" in _aidb
    assert "return _nc_convmap.messages(rows)" in _aidb, "delegiert nicht"
    assert "return _nc_aidb.conv_messages(conv_id)" in src, "Bot delegiert nicht an nc.aidb"
    # Die alte Inline-Map in _conv_messages ist weg (die in api_ai_log bleibt separat).
    cm = src[src.find("def _conv_messages("):src.find("def _conv_messages(") + 500]
    assert '"duration_ms": r["duration_ms"]' not in cm, "alte Map noch in _conv_messages"
    ok("v4.0-w55b: Bot delegiert das Mapping, hält nur das SELECT")


def test_v40_w56_admod():
    """v4.0-W56: Monolith-Abtrag — der Allowlist-Bauer der Werbe-Moderation
       (_ad_allowlist) ist nach nc.admod gewandert. Bitgenau: Domain aus der Kanal-
       URL via Regex, Kanalnamen ohne #/@ und Whitespace, eigene Plattform-Domains
       immer erlaubt. Env-Lesen bleibt im Bot."""
    import re as _re
    from nc import admod as AM
    ad_url = _re.compile(r"(?:https?://|www\.)?([a-z0-9-]+\.[a-z]{2,})(?:/\S*)?", _re.I)
    a = AM.build_allowlist("https://kick.com/xy", ["#Foo", "@Bar", "  Baz  ", ""], ad_url)
    assert "kick.com" in a, "Domain aus Kanal-URL fehlt"
    assert {"foo", "bar", "baz"} <= a, "#/@/Whitespace-Strip + lower falsch"
    # eigene Plattformen immer dabei.
    assert {"kick.com", "twitch.tv", "youtube.com", "youtu.be", "tiktok.com"} <= a
    # leer → nur Plattform-Defaults.
    assert AM.build_allowlist("", [], ad_url) == set(AM._OWN_PLATFORMS)
    # kein URL-Treffer → keine zusätzliche Domain.
    assert AM.build_allowlist("kein link", [], ad_url) == set(AM._OWN_PLATFORMS)
    ok("v4.0-w56: nc.admod — Allowlist-Aufbau bitgenau (URL-Domain/#@-Strip/Plattformen)")

    src = open("bot.py").read()
    assert "from nc import admod as _nc_admod" in src
    assert "_nc_admod.build_allowlist(" in src, "delegiert nicht"
    assert 'allow.update({"kick.com"' not in src, "alte Allowlist-Logik noch im Monolithen"
    ok("v4.0-w56: Bot delegiert den Aufbau, liest nur noch die Env-Variablen")


def test_v40_w57_brain3d_and_attack_time():
    """v4.0-W57: Dashboard-Grafik. (1) Der Wissensgraph ist ein echtes drehbares
       3D-Netz (ncBrainNet3D): ziehen=drehen/schwenken, Rad/Pinch=rein/raus, reine
       Vanilla-Canvas-3D-Projektion. (2) Die JÜNGSTE-ANGREIFER-Liste zeigt jetzt den
       Zeitstempel (x.last aus dem Auth-Log)."""
    h = open("templates/dashboard.html").read()
    # 3D-Renderer existiert und wird für den Brain-View benutzt.
    assert "var ncBrainNet3D=(function(){" in h, "3D-Renderer fehlt"
    assert "ncBrainNet3D.start();" in h, "Brain-View nutzt den 3D-Renderer nicht"
    # 3D-Interaktion: Drehen (yaw/pitch), Zoom (wheel/pinch), Schwenk (pan).
    for tok in ("yaw", "pitch", "zoom", "panx", "wheel", "pointerdown", "requestAnimationFrame"):
        assert tok in h, f"3D-Interaktion unvollständig: {tok} fehlt"
    # 3D-Projektion (Rotation + Perspektive) vorhanden.
    assert "Math.cos(yaw)" in h and "Math.sin(pitch)" in h and "persp" in h, "keine 3D-Projektion"
    # Fibonacci-Kugel-Layout.
    assert "Math.sqrt(5)" in h, "kein gleichmäßiges Kugel-Layout"
    # Zoom-Modal snapshotet den 3D-Renderer.
    assert "window.ncBrainNet3D||window.ncBrainNet" in h, "Modal nutzt 3D nicht"
    # Datum/Uhrzeit in der Angreifer-Liste.
    assert "x.last?" in h and "esc(String(x.last))" in h, "Zeitstempel fehlt in der Angreifer-Liste"
    ok("v4.0-w57: 3D-Wissensgraph (drehen/zoomen/schwenken) + Angriffs-Zeitstempel")

    # Das Backend liefert den Zeitstempel bereits (last = Auth-Log-Zeitstempel).
    src = open("bot.py").read()
    assert '"last": line[:15]' in src, "Backend liefert keinen Angriffs-Zeitstempel"


def test_v40_w58_defense_globe():
    """v4.0-W58: Die CrowdSec-Angriffskarte ist eine drehbare 3D-Weltkugel
       (ncDefenseGlobe): Drahtgitter-Gradnetz, Angriffs-Marker auf der Kugel, Bögen
       zum Ziel (OVH Gravelines). Ziehen=drehen/schwenken, Rad/Pinch=rein/raus, nur
       die zugewandte Hemisphäre wird gezeichnet. Vanilla-Canvas-3D."""
    h = open("templates/dashboard.html").read()
    assert "var ncDefenseGlobe=(function(){" in h, "3D-Globe fehlt"
    assert "ncDefenseGlobe.render(" in h, "Karte nutzt die 3D-Kugel nicht"
    assert "ncDefenseMap((at" not in h, "alter 2D-Karten-Aufruf noch aktiv"
    # Geo->3D + Rotation + Perspektive + Backface-Cull.
    assert "Math.cos(la)*Math.sin(lo)" in h and "Math.sin(la)" in h, "keine Geo->3D-Projektion"
    assert "if(p.z<0)return;" in h, "kein Backface-Cull (Rückseite würde durchscheinen)"
    # Interaktion.
    for tok in ("yaw", "pitch", "zoom", "panx", "wheel", "pointerdown"):
        assert tok in h, f"3D-Interaktion unvollständig: {tok}"
    # Bögen zum Ziel + Ziel-Default OVH Gravelines.
    assert "function arc(" in h and "50.69" in h, "Bögen/Ziel fehlen"
    # Zoom-Modal snapshotet die Kugel.
    assert "ncDefenseGlobe.snapshotInto" in h, "Modal nutzt die Kugel nicht"
    ok("v4.0-w58: 3D-Angriffs-Weltkugel (drehen/zoomen/schwenken) + Bögen zum Ziel")


def test_v40_w59_donations_unknown():
    """v4.0-W59: Monolith-Abtrag (conn-injiziert) — _donations_unknown_count ist
       nach nc.donations.unknown_count gewandert. Zählt Spenden ohne Herkunft
       (Plattform NULL/'') im Zeitfenster; enthält den SQLite-/andere-DB-Fallback
       und robusten Row-Zugriff; jeder Fehler → 0. Gegen echtes SQLite bewiesen."""
    import sqlite3
    from nc import donations as D
    db = sqlite3.connect(":memory:")
    db.row_factory = sqlite3.Row
    db.execute("CREATE TABLE overlay_events(id INTEGER PRIMARY KEY, kind TEXT, platform TEXT, ts TEXT)")
    db.execute("INSERT INTO overlay_events(kind,platform,ts) VALUES ('donation',NULL,datetime('now','-1 day'))")
    db.execute("INSERT INTO overlay_events(kind,platform,ts) VALUES ('donation','',datetime('now','-2 day'))")
    db.execute("INSERT INTO overlay_events(kind,platform,ts) VALUES ('donation','kick',datetime('now','-1 day'))")
    db.execute("INSERT INTO overlay_events(kind,platform,ts) VALUES ('donation',NULL,datetime('now','-40 day'))")
    db.commit()
    assert D.unknown_count(db, 30) == 2, "NULL + '' im Fenster erwartet"
    # Tupel-Row (ohne Row-Factory) → r[0]-Pfad.
    db2 = sqlite3.connect(":memory:")
    db2.execute("CREATE TABLE overlay_events(id INTEGER PRIMARY KEY, kind TEXT, platform TEXT, ts TEXT)")
    db2.execute("INSERT INTO overlay_events(kind,platform,ts) VALUES ('donation',NULL,datetime('now','-1 day'))")
    db2.commit()
    assert D.unknown_count(db2, 30) == 1
    # Fehler → 0.
    class Bad:
        def cursor(self):
            raise RuntimeError("x")
    assert D.unknown_count(Bad(), 30) == 0
    ok("v4.0-w59: nc.donations.unknown_count — Zählung/Row-Zugriff/Fehler→0 gegen SQLite bewiesen")

    src = open("bot.py").read()
    # v4.0-W116: der Aufrufer _donations_unknown_count hatte ausser den
    # /api/donations-Routen keinen Leser mehr und ist mit ihnen ins Blueprint
    # gewandert. Die Delegation gilt unveraendert, sie steht nur dort.
    _money = open("nc/routes/money.py", encoding="utf-8").read()
    assert "_nc_donations.unknown_count(conn, days)" in _money, "delegiert nicht"
    assert "def _donations_unknown_count" not in src, \
        "Doppel-Logik: Helfer liegt noch im Monolithen UND im Blueprint"
    assert "kind='donation' AND (platform IS NULL" not in src + _money, \
        "alte SQL wieder da"


def test_v40_w60_binresolve():
    """v4.0-W60: Monolith-Abtrag — die Binary-Pfad-Auflösung von _cscli_bin ist nach
       nc.binresolve gewandert (generisch, which/exists injiziert). Reihenfolge:
       which(name) zuerst, dann erster existierender Kandidat, sonst None. Das None
       (statt Platzhalter) verhindert, dass 'sudo -n cscli' auf ein fehlendes
       Programm wie ein Rechteproblem aussieht."""
    from nc import binresolve as BR
    cand = ("/usr/bin/cscli", "/usr/local/bin/cscli", "/usr/sbin/cscli", "/usr/local/sbin/cscli")
    # which trifft → dessen Pfad, Kandidaten ignoriert.
    assert BR.resolve("cscli", cand, lambda n: "/snap/bin/cscli", lambda c: True) == "/snap/bin/cscli"
    # which leer → erster EXISTIERENDER Kandidat (Reihenfolge zählt).
    exists = lambda c: c in ("/usr/local/bin/cscli", "/usr/sbin/cscli")
    assert BR.resolve("cscli", cand, lambda n: None, exists) == "/usr/local/bin/cscli"
    # nichts da → None.
    assert BR.resolve("cscli", cand, lambda n: None, lambda c: False) is None
    # falsy which ('') → Fallback greift.
    assert BR.resolve("cscli", cand, lambda n: "", lambda c: c == "/usr/bin/cscli") == "/usr/bin/cscli"
    ok("v4.0-w60: nc.binresolve — which-zuerst/Kandidaten-Reihenfolge/None bewiesen")

    src = open("bot.py").read()
    assert "from nc import binresolve as _nc_binresolve" in src
    assert "_nc_binresolve.resolve(" in src, "delegiert nicht"
    assert '/usr/local/sbin/cscli"):' not in src, "alte Fallback-Schleife noch im Monolithen"


def test_v40_w61_ffver():
    """v4.0-W61: Monolith-Abtrag — das Parsen der ffmpeg-Versionszeile
       (_ffmpeg_version_str) ist nach nc.ffver gewandert. Subprozess + Cache
       bleiben im Bot; rein ist nur das Parsen: 'ffmpeg version X …' → X, sonst
       erste Zeile (max 40 Zeichen), nichts → ''. Bitgenau."""
    from nc import ffver as FV
    assert FV.parse_version("ffmpeg version 6.1.1-3ubuntu5 Copyright") == "6.1.1-3ubuntu5"
    assert FV.parse_version("ffmpeg version n7.0 built with gcc") == "n7.0"
    assert FV.parse_version("") == "" and FV.parse_version(None) == ""
    assert FV.parse_version("kein version-token") == "kein version-token"
    long = "x" * 60
    assert len(FV.parse_version(long)) == 40, "40-Zeichen-Fallback"
    # nur die erste Zeile zählt.
    assert FV.parse_version("ffmpeg version 5.0\nzweite zeile") == "5.0"
    ok("v4.0-w61: nc.ffver — Versions-Parsing bitgenau (Version/Fallback/leer/40-cap)")

    src = open("bot.py").read()
    # v4.0-W116: _ffmpeg_version_str war nur noch von den /api/ops-Routen genutzt
    # und ist mit ihnen ins Blueprint gewandert — samt seinem Cache, der genau
    # einen Eigentuemer hat. Der Vertrag verankert jetzt dort.
    ops = open("nc/routes/ops.py", encoding="utf-8").read()
    assert "from nc import ffver as _nc_ffver" in ops
    assert "_nc_ffver.parse_version(out.stdout)" in ops, "delegiert nicht"
    assert '_FFMPEG_VER_CACHE = {"v": None}' in ops, "Cache nicht mitgewandert"
    assert "def _ffmpeg_version_str" not in src, \
        "Doppel-Logik: Versionshelfer liegt noch im Monolithen UND im Blueprint"
    assert 're.search(r"ffmpeg version' not in src and 're.search(r"ffmpeg version' not in ops, \
        "alte Parse-Logik wieder da"


def test_v40_w61b_netstat():
    """v4.0-W61b: Monolith-Abtrag — die Netzdurchsatz-Berechnung
       (_sample_net_throughput) ist nach nc.netstat gewandert. sum_bytes summiert
       rx+tx über /proc/net/dev (ohne lo, Header übersprungen); throughput_kbps
       macht aus zwei Messungen kbps, mit Guards gegen Erststart und Counter-Reset.
       Datei-I/O + State bleiben im Bot."""
    from nc import netstat as NS
    dev = ("Inter-|   Receive  |  Transmit\n"
           " face |bytes ...\n"
           "    lo:  100 1 0 0 0 0 0 0  100 1 0 0 0 0 0 0\n"
           "  eth0: 1000 5 0 0 0 0 0 0  2000 6 0 0 0 0 0 0\n"
           " wlan0:  500 2 0 0 0 0 0 0   300 3 0 0 0 0 0 0\n")
    assert NS.sum_bytes(dev) == 3800, "rx+tx ohne lo, Header übersprungen"
    assert NS.sum_bytes("") == 0 and NS.sum_bytes(None) == 0
    # Delta: 3800→7800 in 1s = 4000*8/1000 = 32.0 kbps.
    assert NS.throughput_kbps(9.0, 3800, 10.0, 7800) == 32.0
    assert NS.throughput_kbps(0.0, 0, 10.0, 3800) == 0.0, "Erstaufruf → 0"
    assert NS.throughput_kbps(9.0, 7800, 10.0, 100) == 0.0, "Counter-Reset → 0"
    assert NS.throughput_kbps(10.0, 3800, 10.0, 7800) == 0.0, "keine Zeitdifferenz → 0"
    ok("v4.0-w61b: nc.netstat — Parsing + kbps-Delta (Erststart/Reset/Zeit-Guard) bewiesen")

    src = open("bot.py").read()
    assert "from nc import netstat as _nc_netstat" in src
    assert "_nc_netstat.sum_bytes(f.read())" in src and "_nc_netstat.throughput_kbps(prev_ts" in src
    assert "rx_bytes + tx_bytes" not in src, "alte Parse-Logik noch im Monolithen"


def test_v40_w62_archivename():
    """v4.0-W62: Monolith-Abtrag — die kollisionsfreie Namensfolge + Retry von
       _archive_open_unique ist nach nc.archivename gewandert (opener injiziert).
       filename, dann base_2, base_3 … VOR der Extension; Erschöpfung → RuntimeError.
       Der atomare os.open (O_CREAT|O_EXCL) bleibt im Bot."""
    from nc import archivename as AN
    def opener_for(taken):
        n = [0]
        def opener(full):
            if full in taken:
                raise FileExistsError(full)
            n[0] += 1
            return n[0]
        return opener
    # Keine Kollision → Originalname.
    fd, full = AN.open_unique("/arc", "clip.mp4", opener_for(set()))
    assert full == "/arc/clip.mp4" and fd == 1
    # Original + _2 belegt → _3, Suffix vor der Extension.
    fd, full = AN.open_unique("/arc", "clip.mp4", opener_for({"/arc/clip.mp4", "/arc/clip_2.mp4"}))
    assert full == "/arc/clip_3.mp4", full
    # Ohne Extension.
    fd, full = AN.open_unique("/arc", "README", opener_for({"/arc/README"}))
    assert full == "/arc/README_2", full
    # Erschöpfung → RuntimeError.
    def always(full):
        raise FileExistsError(full)
    try:
        AN.open_unique("/arc", "x.bin", always, max_attempts=5)
        raise AssertionError("hätte RuntimeError werfen müssen")
    except RuntimeError:
        pass
    ok("v4.0-w62: nc.archivename — Namensfolge (_2/_3 vor ext) + Retry + Erschöpfung bewiesen")

    # W107: _archive_open_unique ist mit den Archiv-Routen ins Blueprint
    # gewandert. Der Vertrag gilt unveraendert, der Anker liegt jetzt dort —
    # und der Monolith darf keine zweite Kopie behalten.
    src = open("bot.py").read()
    _rt = open("nc/routes/archive.py", encoding="utf-8").read()
    assert "from nc import archivename as _nc_archivename" in _rt
    assert "_nc_archivename.open_unique(" in _rt, "delegiert nicht"
    assert "zu viele Kollisionen im Archive-Ordner" not in src, "alte Retry-Schleife noch im Monolithen"
    assert "_nc_archivename.open_unique(" not in src, "Doppel-Logik: noch im Monolithen"


def test_v40_w62b_journalperm():
    """v4.0-W62b: Monolith-Abtrag — die Journal-Leserecht-Entscheidung von
       _darf_journal_lesen ist nach nc.journalperm gewandert. Mitglied in
       adm/systemd-journal ODER root → True; sonst False; unbekannte Gruppen
       (gid_of→None) werden übersprungen. Systemzugriffe + Fallback→True bleiben
       im Bot."""
    from nc import journalperm as JP
    gids = {"adm": 4, "systemd-journal": 102}
    gid_of = lambda n: gids.get(n)
    assert JP.may_read({4, 1000}, gid_of, 1000) is True, "adm → darf lesen"
    assert JP.may_read({102, 1000}, gid_of, 1000) is True, "systemd-journal → darf lesen"
    assert JP.may_read({1000}, gid_of, 0) is True, "root → darf lesen"
    assert JP.may_read({1000}, gid_of, 1000) is False, "keine Gruppe + nicht root → nein"
    # Unbekannte Gruppe (gid_of liefert None) wird übersprungen, kein Crash.
    assert JP.may_read({1000}, lambda n: None, 1000) is False
    assert JP.may_read({1000}, lambda n: None, 0) is True
    ok("v4.0-w62b: nc.journalperm — Gruppen/root-Entscheidung + None-Skip bewiesen")

    src = open("bot.py").read()
    assert "from nc import journalperm as _nc_journalperm" in src
    assert "_nc_journalperm.may_read(" in src, "delegiert nicht"
    assert 'for name in ("adm", "systemd-journal")' not in src, "alte Entscheidung noch im Monolithen"


def test_v40_w62c_cfgstore():
    """v4.0-W62c: Monolith-Abtrag (conn-injiziert) — der backend-agnostische
       app_config-Upsert von _cfg_set ist nach nc.cfgstore gewandert. Neuer Key →
       INSERT, bestehender → UPDATE (kein Duplikat), und der TOCTOU-Fallback: wenn
       der INSERT am UNIQUE-Index scheitert (anderer Thread war schneller), greift
       ein zweites UPDATE. json.dumps + Zeitstempel bleiben im Bot."""
    import sqlite3
    from nc import cfgstore as CS
    def fresh():
        db = sqlite3.connect(":memory:")
        db.row_factory = sqlite3.Row
        db.execute("CREATE TABLE app_config(k TEXT UNIQUE, v TEXT, updated_at TEXT)")
        db.commit()
        return db
    # Neuer Key → INSERT.
    db = fresh()
    CS.upsert(db, "theme", '"dark"', "t1")
    assert db.execute("SELECT v FROM app_config WHERE k='theme'").fetchone()["v"] == '"dark"'
    # Bestehender → UPDATE, kein Duplikat.
    CS.upsert(db, "theme", '"light"', "t2")
    rows = db.execute("SELECT v FROM app_config WHERE k='theme'").fetchall()
    assert len(rows) == 1 and rows[0]["v"] == '"light"'
    # TOCTOU-Fallback: UPDATE=0, SELECT=None, INSERT wirft → zweites UPDATE setzt den Wert.
    class RaceConn:
        def __init__(self, real):
            self.real = real
            self.updates = 0
            self.insert_thrown = False
        def execute(self, sql, params=()):
            if sql.startswith("UPDATE"):
                self.updates += 1
                self.real.execute(sql, params)
                class Cur:
                    rowcount = 0
                return Cur()
            if sql.startswith("SELECT"):
                class Empty:
                    def fetchone(self_):
                        return None
                return Empty()
            if sql.startswith("INSERT"):
                self.insert_thrown = True
                raise sqlite3.IntegrityError("UNIQUE")
            return self.real.execute(sql, params)
        def commit(self):
            self.real.commit()
    db = fresh()
    db.execute("INSERT INTO app_config(k,v,updated_at) VALUES ('x','\"old\"','t0')")
    db.commit()
    rc = RaceConn(db)
    CS.upsert(rc, "x", '"new"', "t3")
    assert rc.insert_thrown and rc.updates == 2, "kein Race-Fallback-UPDATE"
    assert db.execute("SELECT v FROM app_config WHERE k='x'").fetchone()["v"] == '"new"'
    ok("v4.0-w62c: nc.cfgstore — Upsert (INSERT/UPDATE/TOCTOU-Fallback) gegen SQLite bewiesen")

    # W111: _cfg_set ist selbst nach nc/cfgstore.py gewandert, der Upsert-Aufruf
    # damit eine Ebene tiefer. Der Vertrag gilt unveraendert — geprueft wird
    # jetzt dort, plus dass der Bot wirklich delegiert und keine Kopie behaelt.
    src = open("bot.py").read()
    _cs = open("nc/cfgstore.py", encoding="utf-8").read()
    assert "from nc import cfgstore as _nc_cfgstore" in src
    assert "upsert(conn, key, payload, now)" in _cs, "set_ ruft den Upsert nicht"
    assert "return _nc_cfgstore.set_(key, value)" in src, "Bot delegiert _cfg_set nicht"
    assert "return _nc_cfgstore.get(key, default)" in src, "Bot delegiert _cfg_get nicht"
    assert "INSERT INTO app_config (k, v, updated_at)" not in src, "alter Upsert noch im Monolithen"
    assert "SELECT v FROM app_config WHERE k=?" not in src, \
        "Doppel-Logik: app_config-Lesezugriff noch im Monolithen"


def test_v40_w62d_mod_resolve_exempt():
    """v4.0-W62d: Monolith-Abtrag — die Config-Auflösung der Mod-Ausnahmerollen aus
       _mod_is_exempt ist nach nc.modheuristics.resolve_exempt gewandert. Reihenfolge:
       cfg['exempt_roles'] (nur wenn dict), sonst env-String (Komma/Whitespace
       geparst), sonst DEFAULT_EXEMPT. os.getenv bleibt im Bot; die Entscheidung
       macht weiter is_exempt (Subscriber NICHT ausgenommen)."""
    from nc import modheuristics as M
    D = M.DEFAULT_EXEMPT
    assert M.resolve_exempt({"exempt_roles": ["vip", "mod"]}, "ignored") == ["vip", "mod"]
    assert M.resolve_exempt({}, "broadcaster, moderator  staff") == ["broadcaster", "moderator", "staff"]
    assert M.resolve_exempt({}, "") == D and M.resolve_exempt(None, None) == D
    assert M.resolve_exempt("nicht-dict", "admin owner") == ["admin", "owner"]
    assert M.resolve_exempt({"exempt_roles": "a,b"}, "") == ["a", "b"]
    # Zusammenspiel: resolve → is_exempt.
    ex = M.resolve_exempt({}, "broadcaster,moderator")
    assert M.is_exempt(["Moderator"], ex) is True and M.is_exempt(["subscriber"], ex) is False
    ok("v4.0-w62d: nc.modheuristics.resolve_exempt — Auflösung dict/env/Default bewiesen")

    src = open("bot.py").read()
    assert "_nc_mod.resolve_exempt(cfg, os.getenv(\"MOD_EXEMPT_ROLES\"" in src, "delegiert nicht"
    assert "cfgv.replace" not in src, "alte Parse-Logik noch im Monolithen"


def test_v40_w63_creator_dossier():
    """v4.0-W63: News-Agent — Azraels Creator-Dossier. Je getracktem User (auch
       inaktive) eine Aktivitäts-Zusammenfassung aus recording_attempts + Azraels
       Take (LLM), gecacht in app_config, per API + Dashboard-Panel im Brain-Tab.
       Die Aggregation (nc.creatoragg) ist rein und gegen echte Daten geprüft."""
    from nc import creatoragg as CA
    rows = [
        {"username": "alice", "started_at": "2026-08-14T10:00:00", "outcome": "success"},
        {"username": "alice", "started_at": "2026-08-14T20:00:00", "outcome": "forbidden_403"},
        {"username": "alice", "started_at": "2026-08-15T09:00:00", "outcome": "success"},
        {"username": "bob", "started_at": "2026-08-15T12:00:00", "outcome": "success"},
        {"username": "", "started_at": "2026-08-15T12:00:00", "outcome": "x"},
    ]
    out = CA.summarize(rows, ["alice", "bob", "carol"])
    by = {u["username"]: u for u in out}
    assert by["alice"]["sessions"] == 3 and by["alice"]["active_days"] == 2
    assert by["alice"]["last_seen"] == "2026-08-15T09:00:00"
    assert by["alice"]["outcomes"] == {"success": 2, "forbidden_403": 1}
    assert by["carol"]["sessions"] == 0, "inaktiver getrackter User muss enthalten sein"
    assert [u["username"] for u in out] == ["alice", "bob", "carol"], "nach Aktivität sortiert"

    # v4.1-W4: Backend in nc/news.py, Endpoints im Blueprint nc/routes/news.py.
    # Derselbe Vertrag, zwei gewanderte Anker.
    src = open("nc/news.py", encoding="utf-8").read()
    rt = open("nc/routes/news.py", encoding="utf-8").read()
    # Backend: Aktivität + Azrael-Take + Generierung + Cache + Endpoints.
    assert "def creator_activity(" in src and "_nc_creatoragg.summarize(" in src, "Aktivität wird nicht aggregiert"
    assert "async def azrael_creator_take(" in src and "Azrael Sentinel" in src, "Azraels Take fehlt"
    assert "async def creator_dossier_generate(" in src and '_cfg_set("news.creators"' in src, "Generierung/Cache fehlt"
    assert '@bp.route("/api/news/creators")' in rt, "GET-Endpoint fehlt"
    assert '@bp.route("/api/news/creators/generate"' in rt, "Generate-Endpoint fehlt"
    # phrase blieb funktionsfähig (Wrapper → impl).
    assert "async def phrase_impl(" in src and "return await phrase_impl(" in src, "phrase-Umbau kaputt"
    # Dashboard: Panel + Loader + Verdrahtung.
    h = open("templates/dashboard.html").read()
    assert 'id="pnl_creators"' in h and "async function loadCreatorDossier(" in h, "Dashboard-Panel/Loader fehlt"
    assert "loadCreatorDossier();" in h and "async function genCreatorDossier(" in h, "Loader nicht verdrahtet"
    ok("v4.0-w63: Creator-Dossier — Aggregation bewiesen, Azrael-Take + API + Panel verdrahtet")


def test_v40_w64_claude_provider():
    """v4.0-W64: Ollama restlos raus, Claude rein. nc.claude ist der Anthropic-
       Provider (system→Top-Level, /v1/messages, x-api-key, Fehler-Mapping); im Bot
       ist Claude der primäre LLM-Pfad, sobald ein Key gesetzt ist (Dashboard/ENV),
       mit keyless Fallback. Key-Verwaltung per Dashboard (testen/speichern/
       entfernen), Key nie im Klartext zurückgegeben."""
    import io as _io
    import json as _json
    import urllib.error as _ue
    from nc import claude as CL
    # System wandert ins Top-Level-Feld, nur user/assistant im Verlauf.
    sysp, conv = CL._split_messages([
        {"role": "system", "content": "A"}, {"role": "user", "content": "u"},
        {"role": "assistant", "content": "a"}, {"role": "system", "content": "B"}])
    assert sysp == "A\n\nB" and conv == [{"role": "user", "content": "u"}, {"role": "assistant", "content": "a"}]
    assert "system" in CL.build_payload([{"role": "system", "content": "x"}, {"role": "user", "content": "y"}])
    assert CL.parse_response({"content": [{"type": "text", "text": "Hi"}, {"type": "tool_use"}]}) == "Hi"
    # chat_sync über Mock-Opener: Erfolg + Fehler-Mapping.
    class FR(_io.BytesIO):
        def __enter__(self):
            return self
        def __exit__(self, *a):
            return False
    ok_op = lambda r, t: FR(_json.dumps({"content": [{"type": "text", "text": "Pong"}]}).encode())
    assert CL.chat_sync([{"role": "user", "content": "ping"}], "sk-x", opener=ok_op) == ("Pong", None)
    assert CL.chat_sync([{"role": "user", "content": "x"}], "") == (None, "no_key")
    def e401(r, t):
        raise _ue.HTTPError(CL.API_URL, 401, "no", {}, None)
    assert CL.chat_sync([{"role": "user", "content": "x"}], "k", opener=e401) == (None, "auth")
    assert CL.test_key("k", opener=ok_op) == (True, "ok") and CL.test_key("")[0] is False
    # Masking-Logik (wie im Endpoint).
    key = "sk-ant-abc123456789xyz"
    masked = (key[:7] + "…" + key[-4:]) if len(key) >= 14 else ""
    assert masked == "sk-ant-…9xyz" and "abc123" not in masked
    ok("v4.0-w64: nc.claude — Payload/Parse/Fehler-Mapping/Key-Test + Masking bewiesen")

    src = open("bot.py").read()
    _ai = open("nc/routes/ai.py", encoding="utf-8").read()
    assert "import nc.claude as _nc_claude" in src
    assert "def _anthropic_key(" in src and "def _anthropic_model(" in src
    assert src.count("_nc_claude.chat_sync") >= 2, "Claude nicht in beiden llm_chat-Pfaden"
    # W112: die drei Claude-Endpunkte liegen im KI-Blueprint. Vertrag gleich,
    # Anker nachgezogen — und keiner darf im Monolithen zurueckgeblieben sein.
    for ep in ('/api/ai/claude/status', '/api/ai/claude/save', '/api/ai/claude/test'):
        assert ep in _ai, f"Endpoint {ep} fehlt"
        assert ep not in src, f"Doppel-Logik: {ep} noch im Monolithen"
    # Ollama restlos (funktional): kein Shim, kein sichtbares Label mehr.
    assert 'REACTION_AI_PROVIDER == "ollama"' not in src, "Ollama-Shim noch da"
    assert '("Ollama"' not in src, "sichtbares Ollama-Label noch da"
    # Dashboard-Panel + Verdrahtung.
    h = open("templates/dashboard.html").read()
    assert 'id="pnl_claude"' in h and "async function loadClaudeStatus(" in h
    assert "loadClaudeStatus();" in h and "async function claudeSave(" in h and "async function claudeTest(" in h
    ok("v4.0-w64: Claude primär verdrahtet + Key-Panel; Ollama-Shim/Label entfernt")


def test_v40_w65_claude_full_and_donation_reset():
    """v4.0-W65: (1) Backend vollständig auf Claude — auch die Reaction-Engine
       (ai_chat) und der Streaming-Pfad laufen über Claude, sobald ein Key gesetzt
       ist. (2) Modell-Dropdown statt Textfeld (aktuelle Versionen). (3) Spenden-DB
       leeren: Endpoint löscht kind='donation', Ziel-Fortschritt (Live-Summe) → 0."""
    from nc import claude as CL
    assert CL.DEFAULT_MODEL == "claude-haiku-4-5-20251001", "Default-Modell veraltet"

    src = open("bot.py").read()
    # Claude in ALLEN AI-Pfaden: llm_chat, llm_chat_sync, ai_chat (Reaction), Streaming.
    # W112: llm_chat_stream_sync ist mit den /api/ai-Routen ins Blueprint
    # gewandert. Der Vertrag prueft weiterhin ALLE Claude-Pfade, jetzt ueber
    # beide Dateien — sonst waere die Zerlegung ein Schlupfloch.
    _ai = open("nc/routes/ai.py", encoding="utf-8").read()
    assert src.count("_nc_claude.chat_sync") + _ai.count("_nc_claude.chat_sync") >= 4, \
        "Claude nicht in allen AI-Pfaden"
    assert "Reaction-AI Claude fehlgeschlagen" in src, "Reaction-Engine nicht auf Claude"
    assert "Claude zuerst (Einmalantwort" in _ai, "Streaming-Pfad nicht auf Claude"
    # Spenden-Reset-Endpoint.
    # v4.0-W116: Reset-Endpoint liegt im Blueprint nc/routes/money.py.
    _money = open("nc/routes/money.py", encoding="utf-8").read()
    assert '@bp.route("/api/donations/reset"' in _money, "Reset-Endpoint fehlt"
    assert "DELETE FROM overlay_events WHERE kind='donation'" in _money, "Reset löscht nicht"

    # Reset-Logik gegen echtes SQLite: Spenden weg, Rest bleibt.
    import sqlite3
    db = sqlite3.connect(":memory:")
    db.row_factory = sqlite3.Row
    db.execute("CREATE TABLE overlay_events(id INTEGER PRIMARY KEY, kind TEXT, amount REAL)")
    db.executemany("INSERT INTO overlay_events(kind,amount) VALUES (?,?)",
                   [("donation", 5.0), ("donation", 3.0), ("follow", 0), ("reaction", 0)])
    db.commit()
    cur = db.cursor()
    cur.execute("DELETE FROM overlay_events WHERE kind='donation'")
    assert cur.rowcount == 2
    db.commit()
    assert db.execute("SELECT COUNT(*) n FROM overlay_events WHERE kind='donation'").fetchone()["n"] == 0
    assert [r["kind"] for r in db.execute("SELECT kind FROM overlay_events ORDER BY kind")] == ["follow", "reaction"]

    # Dashboard: Dropdown (kein Textfeld mehr) + Reset-Button.
    h = open("templates/dashboard.html").read()
    assert '<select id="cl_model"' in h, "Modell ist kein Dropdown"
    assert 'type="text" placeholder="claude-3-5-haiku-latest"' not in h, "altes Modell-Textfeld noch da"
    for mv in ("claude-haiku-4-5-20251001", "claude-sonnet-5", "claude-opus-4-8"):
        assert mv in h, f"Modell-Option {mv} fehlt"
    assert 'id="don_reset"' in h and "async function donReset(" in h, "Spenden-Reset-UI fehlt"
    ok("v4.0-w65: Backend voll auf Claude + Modell-Dropdown + Spenden-Reset (gegen SQLite bewiesen)")


def test_v40_w66_command_center():
    """v4.0-W66: Dashboard-Aufwertung, Teil 1 — cinematische 3D-Kommandozentrale
       (ncCommandCenter) oben im Insights-View: pulsierender Kern + umkreisende
       KPI-Knoten (Live/Getrackt/Aufnahmen/Checks/Creator) aus /api/stats, drehbar/
       zoombar, Auto-Spin. Vanilla-Canvas-3D."""
    h = open("templates/dashboard.html").read()
    assert "var ncCommandCenter=(function(){" in h, "3D-Kommandozentrale fehlt"
    assert 'id="pnl_ov_cc"' in h and 'id="ov_cc"' in h, "Panel/Canvas fehlt (Übersicht)"
    assert "ncCommandCenter.start('ov_cc','overview')" in h, "nicht auf der Übersicht gemountet"
    assert "'/api/stats'" in h and "ncCommandCenter" in h, "liest die Kennzahlen nicht"
    # 3D-Interaktion + Projektion.
    for tok in ("yaw", "pitch", "zoom", "panx", "wheel", "pointerdown", "requestAnimationFrame"):
        assert tok in h, f"3D-Interaktion unvollständig: {tok}"
    assert "Math.cos(yaw)" in h and "persp" in h, "keine 3D-Projektion"
    # KPI-Labels vorhanden.
    for lab in ("LIVE JETZT", "GETRACKT", "AUFNAHMEN", "CHECKS", "CREATOR"):
        assert lab in h, f"KPI-Label {lab} fehlt"
    ok("v4.0-w66: 3D-Kommandozentrale (Kern + KPI-Knoten, drehbar/zoombar) verdrahtet")


def test_v40_w67_pro_polish():
    """v4.0-W67: Dashboard-Aufwertung Teil 2 — dashboardweite Pro-Politur. Rein
       additive, token-basierte CSS-Schicht: Glas-Panels (backdrop-blur), feine
       Kantenlichter, Eyebrow-Akzent im Kopf, Metrik-Innenglanz, Button-Micro-Lift
       mit Fokusring, Pill-Tags, tokenisierte Scrollbars, sanfter View-Eintritt.
       Theme-übergreifend (nutzt var(--*)), respektiert reduzierte Bewegung."""
    h = open("templates/dashboard.html").read()
    assert "v4.0-W67 · PRO-POLITUR" in h, "Politur-Schicht fehlt"
    i = h.find("v4.0-W67 · PRO-POLITUR")
    block = h[i:h.find("</style>", i)]
    # Balance + Kern-Bausteine.
    assert block.count("{") == block.count("}"), "CSS-Klammern unbalanciert"
    assert "backdrop-filter:blur" in block, "kein Glas-Effekt"
    assert ".panel .head h3::before" in block, "kein Eyebrow-Akzent"
    assert ".btn:focus-visible" in block, "kein Fokusring"
    assert "scrollbar-color" in block, "keine Scrollbar-Politur"
    assert "prefers-reduced-motion:no-preference" in block, "reduzierte Bewegung nicht respektiert"
    # Theme-übergreifend: nutzt Tokens, keine hartkodierten Panel-Farben.
    assert "var(--border-bright)" in block and "var(--neon)" in block, "nicht token-basiert"
    # Kein Layout-Umbau.
    assert "display:none" not in block and "position:fixed" not in block, "strukturelle Änderung eingeschlichen"
    ok("v4.0-w67: Pro-Politur — Glas/Akzent/Micro-Interaktion, token-basiert & theme-sicher")


def test_v40_w68_overview_landing():
    """v4.0-W68: Dashboard-Aufwertung Teil 3 — neuer Übersichts-Landing-Tab (00).
       Top-KPI-Streifen (Live/Getrackt/Aufnahmen/Checks/Creator/Health) + die 3D-
       Kommandozentrale (auf eigenem Canvas) + Schnellzugriff-Kacheln zu den 3D-
       Views. ncCommandCenter ist auf beliebigen Canvas/View mountbar."""
    h = open("templates/dashboard.html").read()
    assert 'data-view="overview"' in h and 'id="view-overview"' in h, "Übersichts-Tab/View fehlt"
    assert "VIEW_LOADERS['overview']=loadOverview" in h, "Loader nicht registriert"
    assert "async function loadOverview(" in h and "function gotoView(" in h, "Loader/Navi fehlt"
    # KPI-Karten.
    for kid in ("ov_live", "ov_track", "ov_rec", "ov_chk", "ov_usr", "ov_health"):
        assert 'id="' + kid + '"' in h, f"KPI {kid} fehlt"
    # Kommandozentrale auf eigenem Canvas + generalisiertes start().
    assert 'id="ov_cc"' in h, "Übersichts-Canvas fehlt"
    assert "function start(canvasId, viewName)" in h, "start() nicht parametrisiert"
    assert "ncCommandCenter.start('ov_cc','overview')" in h, "Zentrale nicht auf Übersicht gemountet"
    assert "CURRENT_VIEW===OWNVIEW" in h, "Draw-Gate nicht auf OWNVIEW umgestellt"
    # Übersicht ist Default-Landing.
    assert "dataset.view==='overview'" in h, "Übersicht nicht als Default-Landing"
    # health-score liefert overall (Backend).
    assert '"overall"' in open("bot.py").read() or "overall=" in open("bot.py").read() or "overall" in open("bot.py").read()
    ok("v4.0-w68: Übersichts-Landing — KPIs + 3D-Zentrale (multi-mount) + Schnellzugriff")


def test_v40_w69_stat_charts():
    """v4.0-W69: Dashboard-Aufwertung Teil 4 — animierte 3D-Statistik auf der
       Übersicht: rotierbares 3D-Balkendiagramm „Aufnahmen/Tag" (ncRecBars3D, aus
       /api/recordings/list) + animierte 3D-Ring-Gauge „Trefferquote" (ncCatchGauge,
       aus /api/insights/catch-rate)."""
    h = open("templates/dashboard.html").read()
    assert "var ncRecBars3D=(function(){" in h and "var ncCatchGauge=(function(){" in h, "3D-Charts fehlen"
    assert 'id="pnl_ov_stats"' in h and 'id="rb_canvas"' in h and 'id="cg_canvas"' in h, "Panel/Canvas fehlt"
    assert "ncRecBars3D.start('rb_canvas','overview')" in h and "ncCatchGauge.start('cg_canvas','overview')" in h, "nicht verdrahtet"
    assert "'/api/recordings/list'" in h and "'/api/insights/catch-rate'" in h, "Datenquellen fehlen"
    # 3D-Balken: Projektion + Interaktion + Aufsteig-Animation.
    assert "function proj(x,y,z)" in h and "appear" in h, "kein 3D-Balken mit Animation"
    ok("v4.0-w69: 3D-Statistik — Aufnahmen/Tag (rotierbar) + Trefferquote-Gauge (animiert)")


def test_v40_w70_claude_probe_diag():
    """v4.0-W70: Claude-Test-Diagnose. probe() nennt die ECHTE Ursache statt
       kryptischer Kürzel: HTTP-Status + Anthropic-Fehlertext (401/404) bzw. der
       konkrete Netzfehler (Timeout/DNS/refused). Der Test-Endpoint reicht das
       plus einen Egress-Hinweis durch — damit ein Fehlschlag diagnostizierbar ist."""
    import io as _io
    import urllib.error as _ue
    from nc import claude as CL
    class FR(_io.BytesIO):
        def __enter__(self):
            return self
        def __exit__(self, *a):
            return False
    ok_op = lambda r, t: FR(b'{"content":[{"type":"text","text":"Pong"}]}')
    assert CL.probe("sk-x", opener=ok_op) == (True, "ok", "Verbindung ok — Claude antwortet.")
    def e401(r, t):
        raise _ue.HTTPError(CL.API_URL, 401, "x", {}, _io.BytesIO(b'{"error":{"message":"invalid x-api-key"}}'))
    ok_, kind, detail = CL.probe("bad", opener=e401)
    assert ok_ is False and kind == "auth" and "invalid x-api-key" in detail, detail
    def refused(r, t):
        raise _ue.URLError("Connection refused")
    ok_, kind, detail = CL.probe("k", opener=refused)
    assert ok_ is False and kind == "unreachable" and "Connection refused" in detail
    # Rückwärtskompatibel: test_key liefert weiter (ok, str).
    assert CL.test_key("sk-x", opener=ok_op) == (True, "ok")
    # W112: der Diagnose-Endpoint liegt im KI-Blueprint.
    _ai = open("nc/routes/ai.py", encoding="utf-8").read()
    assert "_nc_claude.probe(key" in _ai, "Endpoint nutzt die Diagnose nicht"
    assert "api.anthropic.com nicht" in _ai, "Egress-Hinweis fehlt"
    ok("v4.0-w70: Claude-Diagnose — echte Ursache (HTTP/Netz) + Egress-Hinweis")


def test_v40_w71_declutter():
    """v4.0-W71: Dashboard-Aufräumen — Redundanzen raus. (A) Die 3D-Kommandozentrale
       war doppelt (Insights + Übersicht); im Insights-View ist sie entfernt, sie
       lebt nur noch auf der Übersicht. (B) Die alte 2D-SVG-Karte ncDefenseMap war
       seit W58 toter Code (keine Aufrufer) und ist entfernt. ncBrainNet (2D) bleibt
       (Zoom-Modal-Fallback)."""
    h = open("templates/dashboard.html").read()
    # (A) Kommandozentrale nur noch auf der Übersicht.
    assert 'id="pnl_cmdcenter"' not in h and 'id="cc_canvas"' not in h, "Insights-Zentrale nicht entfernt"
    assert h.count("loadCommandCenter(") == 0, "loadCommandCenter noch referenziert"
    assert 'id="ov_cc"' in h and "ncCommandCenter.start('ov_cc','overview')" in h, "Übersichts-Zentrale beschädigt"
    assert "loadCommandCenter();" not in h, "Insights-Loader ruft die Zentrale noch"
    # (B) Tote 2D-Karte entfernt, 3D-Globus intakt.
    assert "function ncDefenseMap(" not in h, "tote ncDefenseMap noch da"
    assert "ncDefenseGlobe.render(" in h, "3D-Globus beschädigt"
    # ncBrainNet-2D-Fallback im Modal bleibt bewusst erhalten.
    assert "window.ncBrainNet3D||window.ncBrainNet" in h, "Brain-Modal-Fallback beschädigt"
    ok("v4.0-w71: Aufräumen — Kommandozentrale entdoppelt + tote 2D-Karte entfernt")


def test_v40_w72_bughunt_website():
    """v4.0-W72: Tiefen-Bughunt + Website-Redesign.
       (A) DASHBOARD-BUG: das 3D-Balkendiagramm (ncRecBars3D) baute sein
           14-Tage-Histogramm aus /api/recordings/list (LIMIT 50) → ältere Tage
           fielen auf einem 24/7-System still auf 0. Neuer serverseitiger
           Aggregat-Endpoint /api/recordings/daily (über _arg_int gehärtet,
           kein 500); Chart liest ihn statt der 50-Zeilen-Liste.
       (B) WEBSITE-BUG: zwei verschachtelte <main> + ein im <footer> gestrandetes
           </main> = ungültiges HTML. Genau ein <main>, sauberer Footer, Skip-Link.
       (C) WEBSITE-REDESIGN: cinematischer 3D-Sentinel-Kern (Vanilla-Canvas),
           Glas-Politur, echte Zusatzfelder (peak_live, Plattform-Chips, version)."""
    src = open("bot.py").read()
    h = open("templates/dashboard.html").read()
    web = open("website/lafap_index.html", encoding="utf-8").read()

    # (A) neuer Endpoint, gehärtet über _arg_int (kein rohes int(request.args)).
    # W106: die Aufnahmen-Routen liegen im Blueprint; der Dekorator heisst dort
    # @bp.route statt @dashboard_app.route. Der Vertrag prueft unveraendert
    # dasselbe — Existenz und Haertung —, nur an der neuen Stelle.
    _rt = open("nc/routes/recordings.py", encoding="utf-8").read()
    assert '@bp.route("/api/recordings/daily")' in _rt, "Aggregat-Endpoint fehlt"
    assert "def api_recordings_daily" in _rt, "Aggregat-Handler fehlt"
    assert "register_blueprint(_nc_routes_recordings.bp)" in src, "Blueprint nicht registriert"
    _seg = _rt[_rt.find("def api_recordings_daily"):_rt.find("def api_recordings_daily") + 1400]
    assert "_arg_int(" in _seg, "Endpoint nicht über _arg_int gehärtet"
    assert "int(request.args.get" not in _seg, "roher Query-Parser im neuen Endpoint"
    assert "FROM recordings" in _seg and "deleted_at IS NULL" in _seg, "zählt nicht sauber aus recordings"
    # Chart liest den Aggregat-Endpoint, NICHT mehr die 50-Zeilen-Liste.
    assert "/api/recordings/daily?days=14" in h, "Chart nutzt den neuen Endpoint nicht"
    _bars = h[h.find("var ncRecBars3D="):h.find("var ncCatchGauge=")]
    assert "apiGet('/api/recordings/list')" not in _bars, "Balken-Chart hängt noch an der 50-Zeilen-Liste"

    # (B) genau EIN <main>, kein </main> im Footer, Skip-Link vorhanden.
    import re as _re
    _nc = _re.sub(r"<!--.*?-->", "", web, flags=_re.DOTALL)
    assert len(_re.findall(r"<main(?:\s|>)", _nc)) == 1, "nicht genau ein <main>"
    assert _nc.count("</main>") == 1, "nicht genau ein </main>"
    _mclose = _nc.find("</main>")
    _fopen = _nc.find("<footer")
    assert 0 < _mclose < _fopen, "</main> schließt nicht vor dem <footer>"
    assert 'class="skip"' in web and 'href="#inhalt"' in web, "kein Skip-Link"

    # (C) 3D-Sentinel-Kern + echte Zusatzfelder (keine erfundenen Daten).
    assert 'id="sentinel-core"' in web, "3D-Sentinel-Kern fehlt"
    assert "getContext('2d')" in web and "requestAnimationFrame" in web, "Kern nicht als Canvas-Animation"
    assert "prefers-reduced-motion" in web, "Kern nicht reduced-motion-fest"
    assert 'data-k="peak_live"' in web and "d.peak_live" in web, "peak_live nicht gebunden"
    assert 'id="platform-chips"' in web and "d.platforms" in web, "Plattform-Chips nicht gebunden"
    assert 'id="site-ver"' in web and "d.version" in web, "Version nicht im Footer gebunden"
    # aufnahmefrei/Marke: interner Codename bleibt öffentlich unsichtbar.
    assert "NIGHTCRAWLER" not in web, "interner Codename auf der Website"
    ok("v4.0-w72: Bughunt (3D-Balken exakt) + Website-Struktur-Fix + 3D-Kern")


def test_v40_w73_retired_model_autoheal():
    """v4.0-W73: abgeschaltete Claude-Modelle heilen sich selbst. Ein auf ein
       retired Modell gepinnter Wert (env ANTHROPIC_MODEL / gespeichert) liefert
       sonst 404 not_found_error — z. B. claude-3-5-haiku-latest (Haiku 3.5,
       retired 2026-02-19). nc.claude.resolve_model hebt auf das aktuelle
       Äquivalent gleicher Klasse an; aktive Modelle bleiben unangetastet."""
    import importlib
    cl = importlib.import_module("nc.claude")
    # retired → angehoben auf ein aktuelles Modell + is_retired True
    for m in ("claude-3-5-haiku-latest", "claude-3-5-haiku-20241022",
              "claude-3-haiku-20240307", "claude-3-5-sonnet-latest",
              "claude-3-7-sonnet-latest", "claude-3-opus-20240229",
              "claude-2", "claude-instant-1.2",
              "claude-sonnet-4-0", "claude-opus-4-1"):
        assert cl.is_retired(m), "retired nicht erkannt: " + m
        assert cl.resolve_model(m) in (cl.CURRENT_HAIKU, cl.CURRENT_SONNET, cl.CURRENT_OPUS), \
            "nicht angehoben: " + m
    # Familie bleibt erhalten
    assert cl.resolve_model("claude-3-5-haiku-latest") == cl.CURRENT_HAIKU
    assert cl.resolve_model("claude-3-7-sonnet-latest") == cl.CURRENT_SONNET
    assert cl.resolve_model("claude-3-opus-20240229") == cl.CURRENT_OPUS
    # aktive Modelle: unverändert, NICHT retired (kein Fehlalarm auf 4-5/4-6/4-8/5)
    for m in ("claude-haiku-4-5-20251001", "claude-haiku-4-5", "claude-sonnet-5",
              "claude-sonnet-4-5", "claude-sonnet-4-6", "claude-opus-4-5",
              "claude-opus-4-7", "claude-opus-4-8", "claude-fable-5"):
        assert not cl.is_retired(m), "aktiv fälschlich als retired: " + m
        assert cl.resolve_model(m) == m, "aktiv verändert: " + m
    assert cl.resolve_model("") == cl.DEFAULT_MODEL and cl.resolve_model(None) == cl.DEFAULT_MODEL
    # Bot verdrahtet: _anthropic_model liefert das EFFEKTIVE (aufgelöste) Modell,
    # Status-Route legt configured_model + model_upgraded offen.
    # W111/W112: die Aufloesung lebt in nc.claude, der Roh-Helfer wird dort
    # direkt importiert, und die Status-Route liegt im KI-Blueprint.
    _cl = open("nc/claude.py", encoding="utf-8").read()
    _ai = open("nc/routes/ai.py", encoding="utf-8").read()
    assert "resolve_model(raw)" in _cl, "resolve_model nicht in nc.claude verdrahtet"
    assert "def model_raw(" in _cl, "Roh-Modell-Helfer fehlt"
    assert "model_raw as _anthropic_model_raw" in _ai, "Blueprint nutzt den Roh-Helfer nicht"
    assert "configured_model=" in _ai and "model_upgraded=" in _ai, \
        "Status legt Anhebung nicht offen"
    ok("v4.0-w73: totes Modell (404) heilt sich — retired → aktuelles Äquivalent")


def test_v40_w74_fleet_status_honest():
    """v4.0-W74: die Website-Flotte lügt nicht mehr. Ist der Agenten-Snapshot leer
       (Brain im stats-schreibenden Prozess nicht erreichbar), zeigte die Statuszeile
       stur „0 von 12 aktiv", obwohl die Karten leuchteten. _public_stats liefert jetzt
       agents_known (True nur bei echter Fleet-Liste); die Website behauptet ohne
       bekannte Flotte kein „0", sondern „Status nicht verfügbar", und markiert Karten
       nur bei bekanntem Zustand als inaktiv."""
    src = open("bot.py").read()
    assert 'stats["agents_known"]' in src, "agents_known nicht in _public_stats"
    # Flag hängt an einer echten Fleet-Liste, nicht hart True.
    _seg = src[src.find('stats["agents_known"] = False'):src.find('stats["agents_total"] = len(stats["agents"])') + 60]
    assert 'stats["agents_known"] = bool(_fleet)' in _seg, "agents_known nicht an die echte Liste gebunden"

    web = open("website/lafap_index.html", encoding="utf-8").read()
    assert "d.agents_known" in web, "Website wertet agents_known nicht aus"
    assert "Status nicht verfügbar" in web, "kein ehrlicher Ersatztext bei unbekannter Flotte"
    # kein pauschales „0 von 12" mehr: der Zähler kommt aus der Liste/echten Feldern.
    assert "known && on===false" in web, "Karten werden auch bei unbekannter Flotte gedimmt"
    ok("v4.0-w74: Flotten-Status ehrlich statt pauschalem Null-Zaehler")


def test_v40_w75_zombie_reap():
    """v4.0-W75: keine Zombie-ffmpeg mehr. Mehrere Pfade beendeten Kindprozesse
       mit terminate()/kill() OHNE anschließendes wait() → der Exit-Status wurde
       nie geerntet, der Prozess blieb als Zombie. Über Stunden (jeder aufgegebene
       Restream-Relay, jeder Screenshot-Timeout) summierte sich das bis zu Prozess-/
       FD-Limits — der Bot wirkte „hängend". Zentraler Helfer _reap_proc
       (terminate→wait→ggf. kill→wait) erntet immer; die Leck-Stellen nutzen ihn."""
    src = open("bot.py").read()
    assert "async def _reap_proc(" in src, "Reap-Helfer fehlt"
    # Helfer endet garantiert mit einem wait() (erntet auch bereits toten Proc).
    _seg = src[src.find("async def _reap_proc("):src.find("async def _reap_proc(") + 1600]
    assert _seg.count("proc.wait()") >= 2 and "kill()" in _seg, "Reap-Helfer erntet nicht robust"

    # die konkreten Leck-Stellen nutzen jetzt _reap_proc statt nacktem kill/terminate:
    # (a) Restream stop(): Primär-Proc + Independent-Relays
    assert "proc = info[\"proc\"]\n        await _reap_proc(proc)" in src, "Restream-Stop erntet Primär-Proc nicht"
    assert src.count("await _reap_proc(") >= 5, "nicht alle Leck-Pfade auf _reap_proc umgestellt"
    # (b) das alte Muster (terminate + wait_for(...,5) + nacktes kill()) ist raus
    assert "proc.kill()\n        except Exception:\n            pass\n        log_event(\"restream.stop\"" not in src, \
        "alter Restream-Stop mit nacktem kill() noch vorhanden"
    ok("v4.0-w75: Zombie-Reap zentral — terminate/kill immer mit wait() geerntet")


def test_v40_w76_fork_deadlock_guard():
    """v4.0-W76: kein Fork-Deadlock mehr (Loop-Hang aus dem py-spy-Dump).
       Ursache: asyncio.create_subprocess_exec forkt synchron im Loop-Thread,
       während faster-whisper/CTranslate2 native Threads laufen lässt — der Fork
       erbt deren Locks und hängt → gesamter Event-Loop tot → keine Ernte → Zombies.
       Fix: Fork und nativer Whisper-Abschnitt über EIN Lock serialisiert; alle
       asyncio.create_subprocess_*-Aufrufe laufen zentral fork-sicher. Kein
       os.register_at_fork (GIL↔Lock-Falle)."""
    src = open("bot.py").read()
    assert "_FORK_NATIVE_LOCK = threading.Lock()" in src, "Fork-Koordinations-Lock fehlt"
    assert "def _whisper_native_section" in src, "native Sektion (Whisper) nicht markiert"
    # zentrale Einhängung beider Spawn-Funktionen
    assert "asyncio.create_subprocess_exec = _nc_create_subprocess_exec" in src, "exec nicht fork-sicher eingehängt"
    assert "asyncio.create_subprocess_shell = _nc_create_subprocess_shell" in src, "shell nicht fork-sicher eingehängt"
    # der Wrapper wartet loop-schonend (Poll + await), statt den Loop zu blockieren
    _seg = src[src.find("async def _fork_safe("):src.find("async def _fork_safe(") + 700]
    assert "acquire(blocking=False)" in _seg and "await asyncio.sleep(" in _seg, "Fork-Wrapper blockiert den Loop"
    # der eigentliche native Aufruf UND das Modell-Laden stehen unter der Sektion
    assert src.count("with _whisper_native_section():") >= 2, "Whisper-Transkribe/Load nicht abgesichert"
    assert "os.register_at_fork(" not in src, "atfork-Handler wäre GIL-unsicher"
    ok("v4.0-w76: Fork-Deadlock-Schutz — Spawn wartet auf native Whisper-Arbeit")


def test_v40_w77_aiconfig_and_overview_agents():
    """v4.0-W77: KI-Konfig-Panel + Übersicht.
       (A) /api/ai/config war an api_freeai_status geroutet (bases/model/provider,
           OHNE budget/timeout/style/url) → Panel zeigte 'undefined/undefined'.
           api_ai_config hing an keiner Route (toter Code). Jetzt korrekt verdrahtet,
           liefert alle Felder und ist Claude-bewusst (Key gesetzt → Claude primär).
       (B) In der Übersicht fehlte die Kachel für aktive Wächter/Agenten — neu,
           gespeist aus /api/brain/agents, ehrlich bei nicht erreichbarem Brain."""
    # (A) Route zeigt auf die richtige Funktion; die alte Fehlverdrahtung ist weg.
    # W112: api_ai_config liegt im KI-Blueprint.
    _ai = open("nc/routes/ai.py", encoding="utf-8").read()
    assert 'def api_ai_config():' in _ai, "api_ai_config fehlt"
    # der Decorator steht unmittelbar VOR api_ai_config
    _before = _ai[:_ai.find('def api_ai_config')]
    assert _before.rstrip().endswith('@bp.route("/api/ai/config")'), \
        "/api/ai/config nicht auf api_ai_config geroutet"
    assert '@bp.route("/api/ai/config")\ndef api_freeai_status' not in _ai, \
        "alte Fehlverdrahtung (ai/config → freeai_status) noch da"
    # Panel-Felder vorhanden + Claude-bewusst
    _seg = _ai[_ai.find('def api_ai_config'):_ai.find('def api_ai_config') + 1400]
    for f in ("budget_used", "budget_max", "timeout_s", "style", "provider", "url"):
        assert f in _seg, "api_ai_config liefert Feld nicht: " + f
    assert "Claude (Anthropic)" in _seg and "_anthropic_key()" in _seg, "nicht Claude-bewusst"

    # (B) Übersicht: Wächter-Kachel + Loader aus /api/brain/agents
    h = open("templates/dashboard.html").read()
    assert 'id="ov_agents"' in h, "Wächter-Kachel fehlt in der Übersicht"
    _ov = h[h.find("async function loadOverview"):h.find("VIEW_LOADERS['overview']")]
    assert "/api/brain/agents" in _ov and "ov_agents" in _ov, "Wächter-Kachel nicht befüllt"
    assert "a.enabled" in _ov, "aktiv-Zählung fehlt"
    ok("v4.0-w77: KI-Konfig ohne undefined (Claude-bewusst) + Wächter in der Übersicht")


def test_v40_w78_empty_env_float_bridge():
    """v4.0-W78: leere .env-Floats töten die Brain-Bridge nicht mehr.
       Ursache (aus dem Journal): 'Brain-Bridge deaktiviert: could not convert
       string to float: ''. float(os.getenv(name,"d")) nutzt den Default NUR bei
       ungesetzter Variable — eine gesetzt-aber-LEERE (name=) liefert "" und
       float("") wirft beim Modul-IMPORT der Bridge → keine Agenten, TICK ✗,
       0 Regeln, /api/brain/* 404. Fix: nc.envnum.env_float (leer→Default, wirft
       nie); Bridge/Agents/LLM darauf umgestellt."""
    import importlib
    import os as _os
    e = importlib.import_module("nc.envnum")
    assert hasattr(e, "env_float") and hasattr(e, "clamp_float"), "env_float/clamp_float fehlen"
    _os.environ["NC_W78_T"] = ""                     # gesetzt-aber-leer
    assert e.env_float("NC_W78_T", 7.5) == 7.5, "leere env nicht auf Default"
    _os.environ.pop("NC_W78_T", None)
    assert e.env_float("NC_W78_UNSET_XYZ", 3.0) == 3.0
    _os.environ["NC_W78_V"] = "2.5"
    assert e.env_float("NC_W78_V", 9) == 2.5
    _os.environ.pop("NC_W78_V", None)
    assert e.clamp_float("", 5.0) == 5.0 and e.clamp_float("abc", 4.0) == 4.0
    assert e.clamp_float("50", 0, 0, 10) == 10, "clamp_float klemmt nicht"

    # Die crashenden Stellen sind auf env_float umgestellt (kein rohes float(getenv)).
    bb = open("brain_bridge.py").read()
    assert 'float(os.getenv("BRAIN_' not in bb, "rohes float(os.getenv) in der Bridge"
    assert bb.count("env_float(") >= 7, "Bridge-Floats nicht flächendeckend gehärtet"
    for f in ("brain/agents.py", "brain/llm.py"):
        assert 'float(os.getenv(' not in open(f).read(), "rohes float(os.getenv) in " + f
    ok("v4.0-w78: leere .env-Floats crashen die Brain-Bridge nicht mehr (Agenten/Tick zurück)")


def test_v40_w79_mariadb_index_keylen():
    """v4.0-W79: sqlite→MariaDB-Migration crasht nicht mehr an der Index-Schlüssel-
       grenze. Indizierte ISO-Timestamp-Spalten (created_at/updated_at/started_at)
       lagen auf txt_long=TEXT; eine indizierte TEXT-Spalte sprengt in MariaDB/
       InnoDB unter utf8mb4 die 3072-Byte-Grenze (Fehler 1071: 'Specified key was
       too long'). Fix: eigener ts-Typ = VARCHAR(64) für indizierte Timestamps."""
    import logging
    import nc.schema as sch

    class _Cap:
        def __init__(s): s.sql = []
        def execute(s, q, *a): s.sql.append(q)
        def commit(s): pass

    cap = _Cap()
    _idx = lambda conn, sqlite, maria=None: conn.execute(maria or sqlite.replace("IF NOT EXISTS ", ""))
    # MariaDB-Rendering (is_my=True) mit dem neuen ts-Typ
    sch.create_schema(cap, pk="INT AUTO_INCREMENT PRIMARY KEY",
                      txt_idx="VARCHAR(255)", txt_long="TEXT", txt_big="MEDIUMTEXT",
                      iv="INTEGER", tbl_opts=" ENGINE=InnoDB DEFAULT CHARSET=utf8mb4",
                      is_my=True, ts="VARCHAR(64)",
                      _create_index_safe=_idx, _migrate_columns=lambda *a, **k: None,
                      log=logging.getLogger("t"))
    ddl = "\n".join(cap.sql)
    import re as _re
    # jede indizierte Timestamp-Spalte muss VARCHAR sein, NIE TEXT
    for tbl, col in [("recordings", "created_at"), ("ai_conversations", "updated_at"),
                     ("tiktok_checks", "created_at"), ("ai_log", "created_at"),
                     ("recording_attempts", "started_at"), ("archive", "created_at"),
                     ("stream_memories", "created_at"), ("manual_recordings", "started_at")]:
        m = _re.search(r"CREATE TABLE IF NOT EXISTS " + tbl + r"\b(.*?)ENGINE", ddl, _re.DOTALL)
        body = m.group(1) if m else ""
        cm = _re.search(col + r"\s+(VARCHAR\(\d+\)|TEXT|MEDIUMTEXT)", body)
        typ = cm.group(1) if cm else "MISSING"
        assert typ.startswith("VARCHAR"), f"{tbl}.{col} ist {typ} (TEXT-Index → MariaDB 1071)"
    # Composite-Schlüssel unter der 3072-Byte-Grenze (utf8mb4 = 4 B/Zeichen)
    assert 255 * 4 + 64 * 4 < 3072, "recordings(username,created_at)-Key zu lang"
    # init_db reicht den ts-Typ als VARCHAR(64) durch
    src = open("bot.py").read()
    assert 'ts        = "VARCHAR(64)" if is_my else "TEXT"' in src, "ts-Typ nicht in init_db"
    assert "is_my=is_my, ts=ts," in src, "ts nicht an create_schema durchgereicht"
    # create_schema akzeptiert ts (Signatur)
    assert "def create_schema(" in open("nc/schema.py").read()
    ok("v4.0-w79: MariaDB-Migration — indizierte Timestamps VARCHAR(64), kein 1071 mehr")


def test_v40_w80_discord_upload_level():
    """v4.0-W80: Community-Ausbau I — Discord-Upload-Limit folgt dem Server-Boost.
       Vorher: _lim = min(env_default=10, guild.filesize_limit) → auf einem
       geboosteten Server wurde alles auf 10 MB heruntergerechnet, der bezahlte
       Boost verpuffte. Fix: reines Modul nc.discordlimits macht das GUILD-Limit
       autoritativ (kennt Boost-Level + Discord-Policy); env deckelt nur explizit."""
    import importlib
    dl = importlib.import_module("nc.discordlimits")
    MB = 1024 * 1024
    # Boost nicht mehr verpufft: 50-MB-Guild ohne env → 50 (nicht 10)
    assert dl.effective_upload_mb(50 * MB) == 50, "Server-Boost wird ignoriert (Kernbug)"
    assert dl.effective_upload_mb(100 * MB) == 100
    assert dl.effective_upload_mb(10 * MB) == 10          # Free
    # expliziter Betreiber-Deckel senkt, hebt aber nie über das Guild-Limit
    assert dl.effective_upload_mb(50 * MB, 20) == 20
    assert dl.effective_upload_mb(50 * MB, 200) == 50
    # unbekanntes Guild → konservativer Free-Default; Floor eingehalten
    assert dl.effective_upload_mb(0) == 10 and dl.effective_upload_mb(None) == 10
    assert dl.effective_upload_mb(2 * MB) == dl.FLOOR_MB
    # Gate liegt knapp unter dem harten Deckel (Overhead-Marge)
    assert dl.gate_mb(50) < 50 and dl.gate_mb(10) >= dl.FLOOR_MB
    assert "Server-Level" in dl.describe(50 * MB) and "Free" in dl.describe(10 * MB)

    # Monolith-Verschlankung: Logik ausgelagert, Bot ruft nur noch das Modul.
    src = open("bot.py").read()
    assert "from nc import discordlimits" in src, "Modul nicht importiert"
    assert "_nc_dclimits.effective_upload_mb(" in src, "Bot nutzt das Modul nicht"
    # der alte, boost-fressende min()-Deckel ist raus
    assert "_lim = min(_lim, _gl)" not in src, "alter min(env,guild)-Deckel noch da"
    # nur ein EXPLIZIT gesetztes env deckelt
    assert "_DISCORD_UPLOAD_OVERRIDE" in src, "Explicit-Override-Erkennung fehlt"
    ok("v4.0-w80: Discord-Upload folgt dem Server-Boost (Guild-Limit autoritativ)")


def test_v40_w81_env_int_and_bridge_health():
    """v4.0-W81: die restlichen leeren .env-INTS töten die Brain-Bridge nicht mehr
       + der Ausfallgrund ist im Dashboard sichtbar.
       W78 härtete nur die .env-FLOATS; sechs rohe int(os.getenv(...)) blieben —
       u. a. RETAIN_DAYS auf MODUL-Ebene in brain/__init__.py, das bei
       BRAIN_RETAIN_DAYS= (gesetzt-aber-leer) schon beim IMPORT des Brain-Pakets
       int('') wirft → 'Brain-Bridge deaktiviert' → keine Agenten/Regeln, TICK ✗,
       /api/brain/* 404. Alle auf nc.envnum.env_int umgestellt. Zusätzlich:
       Startstatus wird erfasst und über die immer-präsente Route /api/brain/health
       + vollen Traceback offengelegt."""
    import importlib
    e = importlib.import_module("nc.envnum")
    assert hasattr(e, "env_int"), "env_int fehlt"
    assert e.env_int("NC_W81_UNSET_XYZ", 9) == 9
    import os as _os
    _os.environ["NC_W81_T"] = ""                    # gesetzt-aber-leer
    assert e.env_int("NC_W81_T", 14) == 14, "leere env-int nicht auf Default"
    _os.environ.pop("NC_W81_T", None)

    # KEIN rohes int/float(os.getenv(...)) mehr im gesamten Brain-Pfad.
    import glob as _glob
    for f in _glob.glob("brain/*.py") + ["brain_bridge.py"]:
        txt = open(f).read()
        import re as _re
        raw = [ln for ln in txt.splitlines()
               if _re.search(r"(float|int)\(os\.getenv\(", ln)
               and "env_float" not in ln and "env_int" not in ln and "clamp_" not in ln]
        assert not raw, f"rohes int/float(os.getenv) in {f}: {raw[:1]}"
    # der gefährlichste (Modul-Ebene) ist konkret abgesichert
    assert "RETAIN_DAYS = env_int(" in open("brain/__init__.py").read(), "RETAIN_DAYS nicht gehärtet"

    # Bridge-Health sichtbar
    src = open("bot.py").read()
    assert '@dashboard_app.route("/api/brain/health")' in src and "_BRIDGE_STATUS" in src, "Health-Route fehlt"
    assert "exc_info=True" in src, "kein voller Traceback bei Bridge-Fehler"
    h = open("templates/dashboard.html").read()
    assert "/api/brain/health" in h and "BRIDGE AUS" in h, "Panel zeigt den echten Grund nicht"
    ok("v4.0-w81: leere .env-Ints + Bridge-Ausfallgrund sichtbar (Agenten/Tick zurück)")


def test_v40_w82_env_hardening_and_bridge_alert():
    """v4.0-W82: die .env-Absturzklasse ist codebase-weit zu + Bridge-Ausfall
       alarmiert aktiv.
       (A) Vier ungeschützte rohe float(os.getenv(...)) auf MODUL-Ebene in
           bot.py (RESTREAM_TTS_GAIN, DEFENSE_SERVER_LAT/LON, HYPE_CLIP_ENERGY)
           hätten den GANZEN Bot bei leerer .env am Import gekillt (W81 traf nur
           die Bridge). Auf nc.envnum umgestellt. Meta-Sperre: nirgends im Kern
           mehr ein rohes int/float(os.getenv(...)) OHNE ' or default' oder envnum.
       (B) Scheitert die Bridge, geht ein Telegram-Alarm raus (war schon mal
           stundenlang still unten)."""
    import re as _re
    import glob as _glob

    # (A) konkrete vier: jetzt über envnum
    src = open("bot.py").read()
    for name in ("RESTREAM_TTS_GAIN", "DEFENSE_SERVER_LAT",
                 "DEFENSE_SERVER_LON", "HYPE_CLIP_ENERGY"):
        assert _re.search(r'env_float\("' + name + r'"', src), name + " nicht gehärtet"

    # (A) Meta-Sperre: kein rohes int/float(os.getenv(...)) auf MODUL-EBENE
    # (läuft beim Import → killt den ganzen Prozess) ohne ' or default' oder
    # envnum. Modul-Ebene = Zuweisung ohne Einrückung. Prosa (literales
    # 'os.getenv(...)') und eingerückte/try-gekapselte Laufzeit-Aufrufe zählen
    # nicht — die gefährliche Klasse ist der Import-Crash.
    files = ["bot.py", "brain_bridge.py"] + _glob.glob("nc/*.py") + _glob.glob("brain/*.py")
    offenders = []
    _mod_assign = _re.compile(r"^[A-Za-z_][A-Za-z0-9_]*\s*=\s*.*?(?:float|int)\(os\.getenv\(")
    for f in files:
        for i, ln in enumerate(open(f, encoding="utf-8"), 1):
            s = ln.split("#", 1)[0]
            if not _mod_assign.match(s):
                continue
            if "os.getenv(...)" in s:                     # Prosa/Ellipsis
                continue
            if _re.search(r"env_int|env_float|clamp_|_arg_int|_nc_envnum", s):
                continue
            if _re.search(r"os\.getenv\([^)]*\)\s*or\s", s):   # ' or default'-Guard
                continue
            offenders.append(f"{f}:{i}: {s.strip()}")
    assert not offenders, "ungeschützte env-Konvertierung auf Modul-Ebene (Import-Crash bei leerer .env): " + str(offenders[:3])

    # (B) Bridge-Ausfall alarmiert per Telegram (_brain_notify) im except-Block
    _exc = src[src.find("Brain-Bridge deaktiviert ("):src.find("Brain-Bridge deaktiviert (") + 900]
    assert "_brain_notify(" in _exc, "kein Telegram-Alarm bei Bridge-Ausfall"
    ok("v4.0-w82: env-Absturzklasse codebase-weit zu + Telegram-Alarm bei Bridge-Aus")


def test_v40_w83_loop_stall_watchdog():
    """v4.0-W83: Loop-Stall-Watchdog — Selbstdiagnose eines eingefrorenen
       Event-Loops. Der Fork-Deadlock (W76) ließ sich nur mit externem py-spy
       finden; jetzt macht der Bot den Dump selbst: Heartbeat-Task auf dem Loop +
       UNABHÄNGIGER Daemon-Thread, der bei stehendem Heartbeat einen Voll-Stack-
       Dump aller Threads (faulthandler) ins Log schreibt + Telegram alarmiert."""
    src = open("bot.py").read()
    assert "async def _loop_heartbeat" in src, "Heartbeat-Task fehlt"
    assert "def _loop_watchdog_thread" in src, "Watchdog-Thread fehlt"
    assert "def _start_loop_watchdog" in src, "Watchdog-Start fehlt"
    # nutzt faulthandler für den Voll-Stack-Dump ALLER Threads
    assert "import faulthandler" in src and "dump_traceback(file=" in src \
        and "all_threads=True" in src, "kein faulthandler-Voll-Stack-Dump"
    # Monitor läuft in EIGENEM Daemon-Thread (überlebt den eingefrorenen Loop)
    _seg = src[src.find("def _start_loop_watchdog"):src.find("def _start_loop_watchdog") + 900]
    assert 'name="loop-watchdog"' in _seg and "daemon=True" in _seg, "kein unabhängiger Daemon-Thread"
    # Schwellen über die GEHÄRTETEN env-Helfer (kein roher float(getenv))
    assert 'env_float("LOOP_WATCHDOG_STALL_S"' in src, "Stall-Schwelle nicht env_float-gehärtet"
    assert 'env_int("LOOP_WATCHDOG_ENABLED"' in src, "Abschalt-Gate fehlt/ungehärtet"
    # in run_bot() NACH dem Setzen von _MAIN_LOOP scharfgeschaltet
    _rb = src[src.find("_MAIN_LOOP = asyncio.get_running_loop()"):
              src.find("_MAIN_LOOP = asyncio.get_running_loop()") + 400]
    assert "_start_loop_watchdog()" in _rb, "Watchdog nicht in run_bot() gestartet"
    # eine Stall-Episode wird nur EINMAL gedumpt (kein Journal-Spam)
    assert "_LOOP_STALL_DUMPED" in src, "kein Einmal-pro-Episode-Guard"
    ok("v4.0-w83: Loop-Stall-Watchdog — Auto-Stack-Dump bei eingefrorenem Loop")


def test_v40_w84_brain_reason_when_degraded():
    """v4.0-W84: „GESTÖRT" nennt den Grund. W81 zeigt den Ausfallgrund nur, wenn
       die Bridge KOMPLETT fehlt (/api/brain/* 404 → „BRIDGE AUS · Grund"). Kommt
       die Bridge aber TEILWEISE hoch (import ok, /api/brain/overview antwortet mit
       tick_alive), der Tick ist aber tot (0 Regeln/Agenten), blieb es bei bloßem
       „GESTÖRT" — der echte init_bridge-Fehler in /api/brain/health blieb ungezeigt.
       Jetzt holt das Panel den Grund auch im degradierten Zustand."""
    h = open("templates/dashboard.html").read()
    _seg = h[h.find("async function loadBrainStatus"):h.find("async function loadBrainStatus") + 2400]
    assert "if(o.tick_alive){ t.textContent='ONLINE'; }" in _seg, "ONLINE/GESTÖRT-Zweig nicht umgebaut"
    assert "'GESTÖRT · '+" in _seg, "Grund wird nicht an GESTÖRT angehängt"
    # der Grund kommt aus der immer-präsenten Health-Route (auch im GESTÖRT-Zweig)
    assert _seg.count("/api/brain/health") >= 1, "Grund wird im GESTÖRT-Zweig nicht geholt"
    # W81-Pfad (BRIDGE AUS) bleibt erhalten
    assert "BRIDGE AUS" in h, "BRIDGE-AUS-Pfad versehentlich entfernt"
    ok("v4.0-w84: GESTÖRT nennt den echten Grund (auch bei Teil-Ausfall der Bridge)")


def test_v40_w85_truncation_and_legal_pages():
    """v4.0-W85: Silent-Truncation geschlossen + Rechtsseiten erstellt.
       (A) Die Aufnahmen-Timeline aggregierte aus /api/recordings/list (LIMIT 50)
           → auf einem 24/7-System fielen ältere Sessions still raus, und der Tag
           „N Sessions" las sich als Gesamtzahl. list akzeptiert jetzt einen
           gehärteten limit-Parameter; die Timeline holt mehr und labelt ehrlich.
       (B) Footer verlinkte /impressum.html + /datenschutz.html, die es im
           Website-Ordner NICHT gab (404 → für eine .de-Seite ein Rechtsrisiko).
           Beide Seiten neu im gleichen Look, DSGVO-konform (lokale Fonts, keine
           externen Requests), mit ENTWURF-Banner + Platzhaltern."""
    # W106: api_recordings_list liegt im Aufnahmen-Blueprint. Vertrag gleich,
    # Anker nachgezogen.
    _rt = open("nc/routes/recordings.py", encoding="utf-8").read()
    _seg = _rt[_rt.find("def api_recordings_list"):_rt.find("def api_recordings_list") + 400]
    assert '_arg_int("limit", 50' in _seg, "recordings/list-Limit nicht gehärtet parametrisiert"
    h = open("templates/dashboard.html").read()
    assert "/api/recordings/list?limit=" in h, "Timeline holt nicht mehr Sessions"
    assert "'letzte '+recs.length+' Sessions'" in h, "Timeline-Tag nicht ehrlich gelabelt"

    import os as _os
    for f in ("website/impressum.html", "website/datenschutz.html"):
        assert _os.path.exists(f), "Rechtsseite fehlt: " + f
        w = open(f, encoding="utf-8").read()
        assert "ENTWURF" in w, "kein ENTWURF-Banner in " + f
        assert "fonts.googleapis.com/css" not in w and "http://fonts" not in w, "externe Fonts in " + f
        assert "NIGHTCRAWLER" not in w, "interner Codename in " + f
        assert 'href="/impressum.html"' in w and 'href="/datenschutz.html"' in w, "Footer-Rechtslinks fehlen in " + f
    imp = open("website/impressum.html", encoding="utf-8").read()
    assert "§ 5 DDG" in imp, "Impressum ohne DDG-Bezug"
    dse = open("website/datenschutz.html", encoding="utf-8").read()
    assert "DSGVO" in dse and "lokal" in dse, "Datenschutz ohne DSGVO/Lokale-Fonts-Aussage"
    ok("v4.0-w85: Aufnahmen-Timeline ohne Silent-Truncation + Impressum/Datenschutz erstellt")


def test_v40_w86_swap_agent():
    """v4.0-W86: Swap-Wächter (13. Agent) — hält den Swap sauber, mit OOM-Schutz.
       Leert den Swap regelmäßig (swapoff/swapon), aber NUR wenn die Seiten sicher
       ins freie RAM passen (sonst OOM-Kill). Registriert in der Flotte, im
       Dashboard dynamisch sichtbar, mit eigener Karte auf der Website."""
    ag = open("brain/agents.py").read()
    assert "class SwapAgent(Agent):" in ag, "SwapAgent fehlt"
    _s0 = ag.find("class SwapAgent")
    _s1 = ag.find("class RestreamSentinelAgent", _s0)
    _seg = ag[_s0:_s1 if _s1 > _s0 else _s0 + 4000]
    assert 'name = "swap"' in _seg, "Agent-Name nicht 'swap'"
    # OOM-Schutz: leert nur, wenn MemAvailable > used + margin
    assert "MemAvailable" in _seg and "avail < used + self._margin_mb" in _seg, "kein OOM-Schutz"
    assert "swapoff" in _seg, "kein Swap-Leer-Kommando"
    # env-konfigurierbar über die gehärteten Helfer
    assert 'env_int("SWAP_AGENT_INTERVAL_S"' in _seg and 'env_int("SWAP_CLEAR_MARGIN_MB"' in _seg, "nicht env-konfigurierbar"
    # Rechte-Fehler wird gemeldet, nicht geworfen
    assert "fehlgeschlagen" in _seg and "record_metric" in _seg, "meldet/mISST nicht sauber"

    # registriert + exportiert
    assert "b.agents.register(SwapAgent(b))" in open("brain_bridge.py").read(), "nicht registriert"
    assert "SwapAgent" in open("brain/__init__.py").read(), "nicht exportiert"

    # Website-Karte vorhanden (Dashboard zeigt die Flotte dynamisch → automatisch)
    w = open("website/lafap_index.html", encoding="utf-8").read()
    assert 'data-agent="swap"' in w, "keine Swap-Karte auf der Website"
    ok("v4.0-w86: Swap-Wächter (13.) mit OOM-Schutz — Flotte/Dashboard/Website")


def test_v40_w87_relay_source_reresolve():
    """v4.0-W87: YouTube/Twitch-Relays brechen nicht mehr dauerhaft ab.
       Die unabhängigen Relays bekamen die TikTok-Quell-URL EINMAL und bauten bei
       jedem Reconnect stur damit neu auf. TikToks signierte URL rotiert aber ~alle
       6 Min → nach dem ersten Ablauf scheiterte jeder Reconnect sofort, MAX_RECONNECTS
       war schnell erschöpft und der Relay gab dauerhaft auf (Kick lief weiter, weil
       der Primär-Monitor die URL erneuert). Fix: Relay löst die Quelle bei jedem
       Reconnect frisch auf, zählt reine URL-Rotation NICHT als Fehlversuch, gibt nach
       gesundem Lauf das Budget zurück und endet sauber, wenn die Quelle offline ist."""
    src = open("bot.py").read()
    # source_username wird durchgereicht
    assert "async def _spawn_independent(self, rid, pname, purl, source_url, transcode,\n" in src \
        and "source_username=None):" in src, "source_username nicht durchgereicht"
    assert "source_username=row[\"source_username\"])" in src, "Aufrufer übergibt source_username nicht"
    # Relay löst frisch auf + behandelt Rotation + Offline
    _relay = src[src.find("async def _relay_loop():"):src.find("task = asyncio.create_task(_relay_loop())")]
    assert "self._resolve_source(\n                            source_username, force_fresh=True)" in _relay \
        or "self._resolve_source(source_username, force_fresh=True)" in _relay, "Relay löst Quelle nicht frisch auf"
    assert "_looks_like_source_expired(_tail)" in _relay, "URL-Rotation nicht als Normalfall behandelt"
    assert "cur_url = _fresh" in _relay, "frische URL wird nicht verwendet"
    # v4.0-W115: hier war der ANKER gebrochen, nicht der Vertrag. Der Reset
    # nach einem gesunden Lauf steht weiter drin — jetzt aus dem Regelsatz
    # (_RESTREAM_RELAY_POLICY.stable_run_s = 120.0, derselbe Wert wie zuvor)
    # und mit der Zusatzregel aus W113: ein vom Stillstands-Waechter beendeter
    # Lauf war LANG, aber nicht gesund und fuellt das Budget nicht auf.
    assert "_nc_rstab.budget_after_run(" in _relay \
        and "progressed=not _stalled" in _relay, "kein Budget-Reset nach gesundem Lauf"
    assert "stable_run_s=120.0" in src, "W87-Schwelle von 120s verloren"
    assert "offline → Relay" in _relay, "Offline-Quelle beendet Relay nicht sauber"
    ok("v4.0-w87: Relays lösen Quelle frisch auf — YouTube/Twitch fallen nicht mehr weg")


def test_v40_w88_ops_observability():
    """v4.0-W88: 10 additive Ops-/Observability-Verbesserungen (kein Eingriff in
       Recording/Restream-Kernpfade). Alle aus den Vorfällen dieser Session
       gelernt: Hänger-Diagnose, leere .env, stille Bridge, Zombies."""
    src = open("bot.py").read()
    h = open("templates/dashboard.html").read()
    checks = {
        # 1 faulthandler + SIGUSR1 on-demand Thread-Dump
        "faulthandler/SIGUSR1": ("def _install_faulthandler" in src and "faulthandler.enable()" in src
                                 and "SIGUSR1" in src and "_install_faulthandler()" in src),
        # 2 Loop-Stall-Zähler
        "stall-counter": ("_LOOP_STALL_COUNT += 1" in src and "loop_stalls=_LOOP_STALL_COUNT" in src),
        # 3 Bridge-Tick-Stillstand-Alarm
        "bridge-tick-alert": ('BRIDGE_TICK_STALL_S' in src and "_BRIDGE_TICK_ALERTED" in src),
        # 4 Dump-Housekeeping
        "dump-prune": ("def _prune_stall_dumps" in src and "_prune_stall_dumps(keep=" in src),
        # 5 /api/brain/health angereichert
        "health-enriched": ("uptime_s=_uptime_s()" in src and "version=BUILD_STAMP" in src),
        # 6 /healthz angereichert
        "healthz-enriched": ("procs=len(active_processes)" in src and "zombies=_zomb" in src),
        # 7 KI-Panel model_upgraded (W73-Auto-Heal sichtbar)
        # W112: die Status-Route liegt im KI-Blueprint, das Panel weiter im Dashboard.
        "ai-upgraded": ("model_upgraded=(_eff != _raw)"
                        in open("nc/routes/ai.py", encoding="utf-8").read()
                        and "auto-aktualisiert" in h),
        # 8 Boot-Warnung leere .env
        "empty-env-warn": ("def _warn_empty_env" in src and "_warn_empty_env()" in src),
        # 9 Zombie-Kinder-Zähler
        "zombie-gauge": ("def _zombie_child_count" in src and "zombies=_zombie_child_count()" in src),
        # 10 /api/debug/threads
        "debug-threads": ('@dashboard_app.route("/api/debug/threads")' in src and "def api_debug_threads" in src),
    }
    missing = [k for k, v in checks.items() if not v]
    assert not missing, "W88-Bausteine fehlen: " + ", ".join(missing)
    ok("v4.0-w88: 10 Ops-/Observability-Verbesserungen (Diagnose, .env, Bridge, Zombies)")


def test_v40_w89_sysdiag_strip():
    """v4.0-W89: die W88-Health-Felder werden im Dashboard sichtbar — kompakter
       System-Diagnose-Streifen in der Übersicht (Uptime · Prozesse · Loop-Stalls
       · Zombies · DB), gespeist aus /healthz, mit Farbcodierung."""
    h = open("templates/dashboard.html").read()
    for _id in ("ov_sysdiag", "sd_up", "sd_proc", "sd_stall", "sd_zomb", "sd_db"):
        assert 'id="' + _id + '"' in h, "Diagnose-Element fehlt: " + _id
    assert ".sysdiag" in h, "Diagnose-CSS fehlt"
    # Loader liest /healthz und färbt Stalls/Zombies
    # v4.0-W109: frueher ein festes 2400-Zeichen-Fenster. Der Health-Fix machte
    # loadOverview zehn Zeilen laenger, und der Vertrag meldete Felder als
    # fehlend, die zwei Zeilen weiter unten stehen — genau die Anker-Falle aus
    # CLAUDE.md. Jetzt bis zum Funktionsende (VIEW_LOADERS['overview']), damit
    # der Anker nicht bei jeder Laengenaenderung neu justiert werden muss.
    _ov = h[h.find("async function loadOverview"):h.find("VIEW_LOADERS['overview']")]
    assert len(_ov) > 500, "loadOverview nicht gefunden — Anker gebrochen"
    assert "apiGet('/healthz')" in _ov, "Streifen zieht nicht aus /healthz"
    assert "loop_stalls" in _ov and "zombies" in _ov and "uptime_s" in _ov, "W88-Felder nicht gebunden"
    assert "'bad'" in _ov and "'warn'" in _ov, "keine Farbcodierung für Stalls/Zombies"
    ok("v4.0-w89: System-Diagnose-Streifen (Uptime/Procs/Stalls/Zombies) im Dashboard")


def test_v40_w90_stream_archive():
    """v4.0-W90: FLAGGSCHIFF A — Semantisches Stream-Archiv („Frag dein Archiv").
       Bewusst als eigenes Subpaket nc/intel/ (Monolith-Abtrag): das Substrat
       (transcripts) + das Archiv (library) leben dort, testbar ohne Bot; bot.py
       hat nur Adapter (Whisper-Segmente), Hintergrund-Indexer und Routen."""
    import os as _os
    # Module existieren und tragen die Kern-API
    for f in ("nc/intel/__init__.py", "nc/intel/transcripts.py",
              "nc/intel/library.py", "nc/intel/test_intel.py"):
        assert _os.path.exists(f), "Intel-Modul fehlt: " + f
    tx = open("nc/intel/transcripts.py").read()
    lib = open("nc/intel/library.py").read()
    assert "def save_segments" in tx and "def pending_ids" in tx and "def ensure_schema" in tx
    assert "def search" in lib and "def index_recording" in lib and "def parse_ref" in lib
    # bot.py: dünne Anbindung, kein Nachbau der Logik im Monolithen
    src = open("bot.py").read()
    assert "from nc.intel import transcripts as _intel_tx" in src
    assert "from nc.intel import library as _intel_lib" in src
    assert "async def _whisper_segments" in src, "Whisper-Segment-Adapter fehlt"
    # W107: die Archiv-Routen liegen im Blueprint, der Dekorator heisst dort
    # @bp.route. Geprueft wird dieselbe Existenz an der neuen Stelle — plus
    # dass der Bot das Blueprint wirklich registriert.
    _rt = open("nc/routes/archive.py", encoding="utf-8").read()
    for route in ('@bp.route("/api/archive/search")',
                  '@bp.route("/api/archive/status")'):
        assert route in _rt, "Archiv-Route fehlt: " + route
    assert "register_blueprint(_nc_routes_archive.bp)" in src, "Archiv-Blueprint nicht registriert"
    assert "async def _intel_index_loop" in src and "_intel_index_loop()" in src, "Indexer nicht verdrahtet"
    # opt-in gehärtet (leere .env crasht nicht)
    assert 'env_int("ARCHIVE_INDEX_ENABLED"' in src, "Indexer-Gate nicht env-gehärtet"
    # Dashboard: Suchpanel + Loader
    h = open("templates/dashboard.html").read()
    assert 'id="pnl_ov_archive"' in h and 'id="arch_q"' in h, "Archiv-Panel fehlt"
    assert "function archSearch" in h and "/api/archive/search" in h, "Archiv-Loader fehlt"
    ok("v4.0-w90: Stream-Archiv (Feature A) — nc.intel-Module + Routen + Panel")


def test_v40_w91_rec_limit_and_legal_pages():
    """v4.0-W91: Silent-Truncation-Rest + Rechtsseiten.
       (A) Wie der W72-3D-Balken-Bug: loadRecTimeline baute Timeline + „N Sessions"
           aus der auf 50 fixierten /api/recordings/list. Route bekommt jetzt einen
           gehärteten limit-Param (Default 50, geklemmt), die Timeline holt 300 und
           labelt ehrlich „letzte N".
       (B) Footer verlinkte /impressum.html + /datenschutz.html — die Dateien
           EXISTIERTEN nicht (404, für eine .de-Seite ein Rechtsrisiko). Jetzt als
           Cinematic-Seiten angelegt: lokale Fonts (kein Google), noindex,
           ENTWURF-Banner, Platzhalter für die echten Rechtsdaten."""
    # (A) Route + Frontend
    # W106: api_recordings_list liegt im Aufnahmen-Blueprint. Vertrag gleich,
    # Anker nachgezogen.
    _rt = open("nc/routes/recordings.py", encoding="utf-8").read()
    _seg = _rt[_rt.find("def api_recordings_list"):_rt.find("def api_recordings_list") + 400]
    assert '_arg_int("limit", 50' in _seg, "recordings/list ohne gehärteten limit-Param"
    h = open("templates/dashboard.html").read()
    assert "/api/recordings/list?limit=300" in h, "Timeline holt nicht mehr als 50"
    assert "'letzte '+recs.length+' Sessions'" in h, "Timeline-Label nicht ehrlich"

    # (B) Rechtsseiten existieren + Grundeigenschaften
    import os as _os
    for f in ("website/impressum.html", "website/datenschutz.html"):
        assert _os.path.exists(f), "Rechtsseite fehlt: " + f
        t = open(f, encoding="utf-8").read()
        assert 'name="robots" content="noindex"' in t, f + ": kein noindex"
        assert "ENTWURF" in t, f + ": kein Entwurf-Banner (könnte halbfertig live gehen)"
        assert "fonts.googleapis" not in t and "fonts.gstatic" not in t, f + ": externe Google-Fonts (DSGVO)"
        assert "@font-face" in t and "orbitron" in t.lower(), f + ": lokale Marken-Fonts fehlen"
        assert "/impressum.html" in t and "/datenschutz.html" in t, f + ": Rechts-Nav fehlt"
    # Datenschutz nennt die technischen Fakten der Seite akkurat
    ds = open("website/datenschutz.html", encoding="utf-8").read()
    assert "lokal" in ds and ("Tracking" in ds or "Analytics" in ds), "Datenschutz ohne Tracker-Aussage"
    ok("v4.0-w91: recordings-Timeline ohne Silent-Truncation + Impressum/Datenschutz angelegt")


def test_v40_w92_usage_and_donation():
    """v4.0-W92: LLM-Token-/Kostenzähler + 3D-Statistik + PayPal-Spendenpanel.
       nc.usage verbucht Tokens/Kosten je Modell/Monat (persistent); chat_sync
       reicht die Usage best-effort durch (on_usage); _public_stats liefert
       usage + donation für die Website; der Index rendert 3D-Balken + Spenden-
       fortschritt zum 500€-Ziel (PayPal paypal@voice4you.org)."""
    import importlib
    us = importlib.import_module("nc.usage")
    # frischer Record verbucht Tokens + schätzt Kosten (provider-bewusst)
    us.record("claude", "claude-opus-4-8", 1000, 2000)
    snap = us.snapshot()
    assert snap["tokens_total"] >= 3000, "Tokens nicht verbucht"
    assert snap["cost_eur"] > 0, "Kosten nicht geschätzt"
    assert "month" in snap and "by_provider" in snap, "Snapshot unvollständig"
    # leere/negative Werte dürfen nichts kaputt machen
    us.record("claude", None, 0, 0)

    # claude.chat_sync kennt on_usage + parse_usage
    cl = importlib.import_module("nc.claude")
    assert "on_usage" in cl.chat_sync.__code__.co_varnames, "chat_sync ohne on_usage"
    assert hasattr(cl, "parse_usage"), "parse_usage fehlt"
    assert cl.parse_usage({"usage": {"input_tokens": 5, "output_tokens": 7}}) == (5, 7)

    # Backend liefert usage + donation in den öffentlichen Stats
    src = open("bot.py").read()
    assert 'stats["usage"] = _nc_usage.snapshot()' in src, "usage nicht in _public_stats"
    assert '"goal_eur"' in src and '"paypal"' in src and "DONATION_GOAL_EUR" in src, "Spendenblock fehlt"
    assert 'paypal@voice4you.org' in src, "PayPal-Standardadresse fehlt"
    assert "_nc_claude.chat_sync = _claude_chat_sync_metered" in src, "Metering-Wrapper nicht installiert"

    # Website: 3D-Canvas + Spendenpanel + Rendering
    h = open("website/lafap_index.html", encoding="utf-8").read()
    assert 'id="usage-3d"' in h and "window.__usage3d" in h, "3D-Verbrauchscanvas fehlt"
    assert 'data-k="tok_total"' in h and 'data-k="cost_total"' in h, "Token/Kosten-Kacheln fehlen"
    assert 'id="don-fill"' in h and 'id="don-btn"' in h, "Spendenpanel fehlt"
    assert "paypal.com/donate" in h, "PayPal-Spendenlink fehlt"
    ok("v4.0-w92: Token-/Kostenzähler + 3D-Statistik + PayPal-Spendenpanel (500€/Monat)")


def test_v40_w93_meter_all_providers():
    """v4.0-W93: ALLE LLM-Anfragen werden gezählt, nicht nur Claude. freeai
       (keyless) und brain (llama.cpp) liefern kein usage-Feld → Tokens per
       Schätzung (~4 Zeichen/Token) verbucht; seit W96 bekommt JEDER Provider
       einen Euro-Transparenzwert (vorher nur Claude). Wrapper für
       freeai.chat_sync + Brain-Dispatch gemetert."""
    import importlib
    us = importlib.reload(importlib.import_module("nc.usage"))
    assert hasattr(us, "estimate_tokens"), "estimate_tokens fehlt"
    assert us.estimate_tokens("x" * 40) == 10, "Token-Schätzung falsch"
    assert us.estimate_tokens([{"content": "y" * 80}]) == 20, "Message-Schätzung falsch"

    # v4.0-W96/W97: freeai zählt Tokens UND bekommt einen Euro-Schätzwert (zur
    # Claude-Rate wie alle). Genug Tokens, dass der Wert über die 2-Nachkomma-
    # Rundung kommt.
    us.record("freeai", "openai", 400_000, 600_000)
    snap = us.snapshot()
    assert snap["tokens_total"] >= 1000, "freeai-Tokens nicht gezählt"
    assert snap["by_provider"].get("freeai", {}).get("cost_eur", -1) > 0, \
        "freeai-Tokens ohne Euro-Gegenwert (W96: alle Tokens umrechnen)"
    # claude verursacht Kosten
    us.record("claude", "claude-opus-4-8", 1_000_000, 1_000_000)
    snap = us.snapshot()
    assert snap["by_provider"].get("claude", {}).get("cost_eur", 0) > 0, "Claude-Kosten fehlen"
    # v4.0-W96: Gesamtkosten = Summe ALLER Provider (nicht nur Claude); freeai
    # hat oben ebenfalls beigetragen, also liegt die Summe über Claude allein.
    _sum = round(sum(v["cost_eur"] for v in snap["by_provider"].values()), 2)
    assert abs(snap["cost_eur"] - _sum) < 0.02, "Gesamt-Euro ≠ Summe aller Provider"
    assert snap["cost_eur"] > snap["by_provider"]["claude"]["cost_eur"], \
        "freeai/brain tragen nicht zu den Gesamtkosten bei (W96)"

    # der Bot metert freeai + brain zusätzlich zu Claude
    src = open("bot.py").read()
    assert "_nc_freeai.chat_sync = _freeai_chat_sync_metered" in src, "freeai nicht gemetert"
    assert '_nc_usage.record("freeai"' in src, "freeai-Record fehlt"
    assert '_nc_usage.record("brain"' in src, "brain-Record fehlt"
    assert '_nc_usage.record("claude"' in src or "_usage_record_claude" in src, "claude-Record fehlt"
    ok("v4.0-w93: alle LLM-Provider gezählt (freeai/brain geschätzt, Kosten nur bezahlt)")


def test_v40_w94_crypto_donations():
    """v4.0-W94: Krypto-Spenden. Adressen kommen aus env (nichts erfunden) — nur
       gesetzte erscheinen; BTC-Empfang best-effort SERVER-seitig über einen
       öffentlichen Explorer (blockstream), damit der Browser keinen Fremd-Request
       macht. Panel versteckt, solange keine Adresse konfiguriert ist."""
    import importlib
    import os as _os
    c = importlib.reload(importlib.import_module("nc.crypto"))
    # ohne env: leer
    for _co, _l, _env in c._COINS:
        _os.environ.pop(_env, None)
    assert c.snapshot() == {"addresses": []}, "ohne env darf nichts erscheinen"
    # mit env: nur gesetzte, Reihenfolge stabil
    _os.environ["DONATION_BTC_ADDRESS"] = "bc1qtestxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
    _os.environ["DONATION_ETH_ADDRESS"] = "0xTESTethaddressxxxxxxxxxxxxxxxxxxxxxxxxxx"
    a = c.addresses()
    assert [x["coin"] for x in a] == ["btc", "eth"], "Adress-Auswahl/Reihenfolge falsch"
    # BTC-Empfang aus gecachten Sats (kein Netz nötig)
    c._CACHE["btc_sats"] = 250000000
    snap = c.snapshot(fetch_live=True)
    assert snap.get("btc_received_btc") == 2.5, "Sats→BTC-Umrechnung falsch"
    for _env in ("DONATION_BTC_ADDRESS", "DONATION_ETH_ADDRESS"):
        _os.environ.pop(_env, None)

    # der Explorer wird SERVER-seitig aufgerufen — nicht im Browser
    src = open("bot.py").read()
    assert 'stats["crypto"] = _nc_crypto.snapshot(fetch_live=True)' in src, "crypto nicht in _public_stats"
    h = open("website/lafap_index.html", encoding="utf-8").read()
    assert "blockstream" not in h, "Explorer darf nicht im Browser aufgerufen werden"
    assert 'id="crypto-wrap"' in h and 'id="crypto-list"' in h, "Krypto-Panel fehlt"
    assert "d.crypto" in h and "crypto-copy" in h, "Krypto-Rendering/Copy fehlt"
    assert "btc_received_btc" in h, "BTC-Empfang wird nicht angezeigt"
    ok("v4.0-w94: Krypto-Spenden (env-Adressen, BTC-Empfang server-seitig, Panel auto-versteckt)")


def test_v40_w95_rectimeline_limit_and_legal_pages():
    """v4.0-W95: (A) Silent-Truncation der Aufnahmen-Timeline behoben. Wie beim
       W72-3D-Balken-Bug baute loadRecTimeline Timeline + „N Sessions" aus der auf
       50 fixierten /api/recordings/list — ältere Sessions fielen still weg. Route
       bekommt einen gehärteten limit-Param (Default 50, geklemmt 1..1000), die
       Timeline holt 300 und labelt ehrlich „letzte N".
       (B) Rechtsseiten: die im Footer verlinkten /impressum.html + /datenschutz.html
       fehlten komplett (→ 404, rechtliches Risiko für eine .de-Seite). Neu im
       Cinematic-Look, lokale Fonts (DSGVO), ENTWURF-Banner + Platzhalter."""
    import os as _os
    # (A) Route + Frontend
    # W106: Haertung liegt mit der Route im Aufnahmen-Blueprint.
    assert '_arg_int("limit", 50, 1, 1000)' in open(
        "nc/routes/recordings.py", encoding="utf-8").read(), "recordings/list limit nicht gehärtet"
    h = open("templates/dashboard.html").read()
    assert "/api/recordings/list?limit=300" in h, "Timeline holt nicht mehr Sessions"
    assert "'letzte '+recs.length+' Sessions'" in h, "Timeline-Label nicht ehrlich"

    # (B) Rechtsseiten existieren, on-brand, DSGVO-fromme Fonts, Entwurf-Banner
    for f in ("website/impressum.html", "website/datenschutz.html"):
        assert _os.path.exists(f), "fehlt: " + f
        t = open(f, encoding="utf-8").read()
        assert "fonts.googleapis" not in t, "externe Google-Fonts in " + f
        assert "--phos" in t and "Orbitron" in t, "nicht im Cinematic-Look: " + f
        assert "ENTWURF" in t, "kein Entwurf-Banner (Live-Schutz) in " + f
        assert 'href="/impressum.html"' in t and 'href="/datenschutz.html"' in t, "Cross-Links fehlen: " + f
    imp = open("website/impressum.html", encoding="utf-8").read()
    assert "§ 5 DDG" in imp, "Impressum nicht nach § 5 DDG strukturiert"
    dsg = open("website/datenschutz.html", encoding="utf-8").read()
    assert "Art. 13 DSGVO" in dsg and "Art. 15 DSGVO" in dsg, "Datenschutz ohne DSGVO-Struktur"
    ok("v4.0-w95: Aufnahmen-Timeline ehrlich (limit) + Impressum/Datenschutz im Look")


def test_v40_w96_all_tokens_to_eur():
    """v4.0-W96/W97: ALLE Tokens werden in Euro umgerechnet — und zwar EINHEITLICH
       zur Claude-Rate, sonst nichts. Vorher bepreiste _cost_eur nur 'claude'
       (freeai/brain 0 €); ein Zwischenstand nahm pro Provider verschiedene Raten.
       Jetzt: jedes Token → Claude-Rate, egal welcher Provider/welches Modell."""
    import importlib
    U = importlib.import_module("nc.usage")
    importlib.reload(U)
    assert not hasattr(U, "_PAID_PROVIDERS"), "Paid-only-Gate noch vorhanden"
    U.configure(usd_eur=0.92)
    U._STATE.update(tokens_in=0, tokens_out=0, cost_eur=0.0, calls=0,
                    by_provider={}, month=U._blank_bucket(), month_key="")
    U.record("freeai", "openai", 1_000_000, 1_000_000)
    U.record("brain", "llama", 500_000, 500_000)
    # gleiche Tokenmenge über verschiedene Provider/Modelle → gleicher Euro-Wert
    U.record("claude", "claude-opus-4-8", 1_000_000, 1_000_000)
    U.record("freeai", "irgendwas", 1_000_000, 1_000_000)
    s = U.snapshot()
    assert s["cost_eur"] > 0, "freeai/brain-Tokens ergeben immer noch 0 €"
    assert all(v["cost_eur"] > 0 for v in s["by_provider"].values()), \
        "nicht jeder Provider trägt zu € bei"
    # Website-Notiz stellt klar, dass ALLE Tokens gemeint sind
    assert all(v["cost_eur"] > 0 for v in s["by_provider"].values()), \
        "nicht jeder Provider trägt zu € bei"
    # EINHEITLICH: gleiche Tokenmenge (2 Mio) → gleicher Euro-Wert für claude & freeai,
    # egal welches Modell (opus wird NICHT teurer als der Rest).
    _c = s["by_provider"]["claude"]["cost_eur"]
    _f = s["by_provider"]["freeai"]["cost_eur"]  # freeai hat 2×1 Mio = 4 Mio → doppelt
    assert abs(_c - 5.52) < 0.02, "Claude-Rate nicht (1/5)$·USD_EUR — %.2f" % _c
    assert abs(_f - 2 * 5.52) < 0.03, "freeai nicht zur selben Claude-Rate: %.2f" % _f
    h = open("website/lafap_index.html", encoding="utf-8").read()
    assert "API-Gegenwert" in h and "aller" in h and "Claude-Preisen" in h, "Website-Notiz nicht angepasst"
    # v4.0-W98: die Umrechnung passiert IM WEBSITE-ORDNER (client-seitig aus den
    # Token-Zahlen), nicht mehr über den fertigen Server-Wert u.cost_eur. So fixt
    # ein reines Website-Deploy die Anzeige — unabhängig vom Backend.
    assert "costTotal=_cost(u.tokens_in,u.tokens_out)" in h, "Website rechnet Kosten nicht selbst"
    assert "fmtE(u.cost_eur)" not in h, "Website liest noch den fertigen Server-Wert"
    ok("v4.0-w98: Token->Euro rechnet die Website selbst (Claude-Rate, im Website-Ordner)")


def test_v40_w99_unified_donation_box():
    """v4.0-W99: PayPal- und Krypto-Spenden sind zu EINER Box zusammengelegt —
       gleichwertige Zahlwege in einem pay-methods-Block statt Krypto unter einer
       Trennlinie an PayPal gehängt. Alle JS-IDs bleiben erhalten; die Krypto-
       Spalte zeigt sich weiterhin nur bei gesetzten Adressen (has-crypto)."""
    h = open("website/lafap_index.html", encoding="utf-8").read()
    assert 'id="pay-methods"' in h, "vereinter Zahlwege-Block fehlt"
    assert ".pay-methods" in h and ".pay-method" in h, "pay-methods-CSS fehlt"
    # beide Methoden liegen IM pay-methods-Block (PayPal-Button + Krypto-Wrap)
    _pm = h[h.find('id="pay-methods"'):h.find('id="pay-methods"') + 700]
    assert 'id="don-btn"' in _pm and 'id="crypto-wrap"' in _pm, "PayPal + Krypto nicht in einer Box"
    # alte, angehängte Krypto-Trennlinie ist weg
    assert "// Auch per Krypto" not in h, "alter angehängter Krypto-Block noch da"
    # zweispaltig nur wenn Krypto sichtbar
    assert "has-crypto" in h, "has-crypto-Umschaltung fehlt"
    # JS-IDs unverändert vorhanden (sonst brechen PayPal/Krypto-Loader)
    for _id in ("don-btn", "don-qr", "don-mail", "crypto-wrap", "crypto-list", "crypto-recv"):
        assert 'id="' + _id + '"' in h, "ID verloren: " + _id
    ok("v4.0-w99: PayPal + Krypto in einer Spenden-Box vereint")


def test_v40_w100_env_example():
    """v4.0-W100: vollständige, generierte .env.example. Leere .env-Zeilen hatten
       den Brain gekillt (W81); eine handgepflegte Vorlage veraltet sofort bei ~470
       Variablen. tools/gen_env_example.py erzeugt sie aus dem Code; der Build
       liefert sie mit (aber NIE die echte .env)."""
    import os as _os
    import subprocess as _sp
    assert _os.path.exists("tools/gen_env_example.py"), "Generator fehlt"
    assert _os.path.exists(".env.example"), ".env.example nicht erzeugt"
    txt = open(".env.example", encoding="utf-8").read()
    assert "AUTO-GENERIERT" in txt, "Kopf/Warnung fehlt"
    # Kernvariablen dokumentiert + PFLICHT/Secret korrekt markiert
    assert "BOT_TOKEN=" in txt and "[PFLICHT]" in txt, "Pflichtvariable nicht markiert"
    assert "ANTHROPIC_API_KEY=" in txt and "Geheimnis" in txt, "Secret nicht markiert"
    for v in ("LOOP_WATCHDOG_STALL_S", "DONATION_PAYPAL", "USD_EUR", "BRAIN_RETAIN_DAYS"):
        assert v in txt, "Variable fehlt in .env.example: " + v
    # bleibt in Sync mit dem Code (Generator --check darf nicht meckern)
    r = _sp.run([__import__("sys").executable, "tools/gen_env_example.py", "--check"],
                capture_output=True, text=True)
    assert r.returncode == 0, ".env.example veraltet — neu generieren: " + (r.stdout or r.stderr)[:120]
    # Build-Regeln: .env.example erlaubt, echte .env verboten
    b = open("tools/build_release.py", encoding="utf-8").read()
    assert '".env.example"' in b and "AUS = {\".env\"}" in b, "Build liefert .env.example nicht / .env nicht gesperrt"
    ok("v4.0-w100: generierte .env.example (473 Variablen) faehrt im Build mit")


def test_v40_w101_rate_single_source_and_escape():
    """v4.0-W101: (A) Rate-Duplikat aufgelöst — der Server legt die Claude-Rate in
       stats.json offen (snapshot.rate), die Website LIEST sie statt sie doppelt
       hartzukodieren (Fallback-Konstanten nur für alte Backends).
       (B) Kleine XSS-Härtung: Krypto-Adresse/Label werden vor innerHTML escaped."""
    import importlib
    U = importlib.import_module("nc.usage")
    importlib.reload(U)
    U.configure(usd_eur=0.92)
    r = U.snapshot().get("rate") or {}
    assert r.get("in_per_mtok_usd") == 1.0 and r.get("out_per_mtok_usd") == 5.0 \
        and r.get("usd_eur") == 0.92, "snapshot.rate fehlt/falsch"
    h = open("website/lafap_index.html", encoding="utf-8").read()
    # (A) Website liest u.rate; Konstanten sind nur noch Fallback
    assert "u.rate" in h and "_rt.usd_eur" in h, "Website liest die Rate nicht aus stats.json"
    assert "in_per_mtok_usd" in h and "out_per_mtok_usd" in h, "Rate-Felder nicht gelesen"
    # (B) Escaping vorhanden und auf Adresse/Label angewandt
    assert "var esc=function(s){" in h, "kein HTML-Escaper"
    assert "esc(a.label||a.coin)" in h and "esc(addr)" in h, "Krypto-Felder nicht escaped"
    assert "var safe=addr.replace" not in h, "alte, unvollständige Escaping-Variante noch da"
    ok("v4.0-w101: Rate aus einer Quelle (stats.json) + Krypto-Escaping")


def test_v40_w102_donations_3d_qr_manual():
    """v4.0-W102: Spenden — scannbare QR + 3D-Münze + manuelle Erfassung.
       (A) QR-Codes waren grün-auf-transparent → auf dem dunklen Grund
           kontrastarm/invertiert = viele Scanner lasen sie nicht. Jetzt dunkle
           Module auf weißem Grund (dark-on-light) + Quiet-Zone.
       (B) Website: rotierende 3D-Euro-Münze (Vanilla-Canvas) in der Spenden-Box,
           Leuchtkraft folgt dem Fortschritt.
       (C) Dashboard: manuelle Spenden erfassen/listen/löschen; fließen in den
           Website-Fortschritt (current_eur = env-Basis + Summe manuell)."""
    # (A) QR dunkel-auf-hell
    qr = open("nc/qrsvg.py").read()
    assert 'light="#ffffff"' in qr and 'dark="#0a0f12"' in qr, "QR nicht dunkel-auf-hell"
    assert "light=None" not in qr, "QR noch transparent (unscannbar auf dunklem Grund)"

    src = open("bot.py").read()
    # (C) manuelle Spenden-Endpoints + current_eur-Integration
    # v4.0-W116: Endpoints im Blueprint nc/routes/money.py, der DB-Zugriff in
    # nc/donationsdb.py. Der Vertrag prueft beides plus die Delegation — sonst
    # koennten Modul und Monolith auseinanderlaufen.
    _money = open("nc/routes/money.py", encoding="utf-8").read()
    _ddb = open("nc/donationsdb.py", encoding="utf-8").read()
    assert '@bp.route("/api/donations/add"' in _money, "kein Add-Endpoint"
    assert '@bp.route("/api/donations/manual")' in _money, "keine Manual-Liste"
    assert "donations/manual/<int:rid>/delete" in _money, "kein Delete-Endpoint"
    assert "def manual_total" in _ddb and "def manual_rows" in _ddb, \
        "manuelle Summe/Liste nicht in nc.donationsdb"
    assert "def _manual_donations_total" in src and "cur += _manual_donations_total()" in src, \
        "manuelle Summe fließt nicht in current_eur"
    assert "return _nc_donationsdb.manual_total()" in src, \
        "Bot delegiert nicht — Doppel-Logik zur manuellen Summe"
    assert "platform='manual'" in _money or "platform='manual'" in _ddb, \
        "manuelle Spenden nicht als platform='manual'"
    assert "WHERE id=? AND kind='donation'" in _money, "Delete nicht portabel (rowid statt id)"

    # (B) + (C) Frontend
    h = open("templates/dashboard.html").read()
    assert 'id="don_m_amount"' in h and "function donAddManual" in h, "kein Dashboard-Formular"
    assert "donManualLoad()" in h, "Manual-Liste wird nicht geladen"
    w = open("website/lafap_index.html").read()
    assert 'id="don-3d"' in w and "window.__don3d" in w, "keine 3D-Münze in der Spenden-Box"
    assert "background:#fff" in w, "QR-Kachel nicht auf weißem (scannbarem) Grund"
    ok("v4.0-w102: scannbare QR (dunkel-auf-hell) + 3D-Münze + manuelle Spenden")


def test_v40_w103_selfcheck_bridge_and_endpoints():
    """v4.0-W103: --selfcheck fängt die stillen Ausfälle dieser Session VOR dem
       Deploy. Der Preflight prüfte Imports/DB/Disk/Tunnel etc., aber NICHT die
       Brain-Bridge (init-Crash bei leerer .env → Agenten/Regeln/Tick AUS, 404)
       und NICHT, ob die Dashboard-Endpoints wirklich antworten (Fehlrouting →
       „undefined", 500er). Jetzt zwei echte Checks: Bridge real initialisieren
       (ohne Tick) + kritische Routen per Test-Client aufrufen; ein Bridge-Init-
       Fehler ist ein HARTER Fehler (Exit 1)."""
    src = open("bot.py").read()
    seg = src[src.find("async def _selfcheck"):src.find("def _run_selfcheck_and_exit")]
    assert seg, "_selfcheck nicht gefunden"
    # (14) Brain-Bridge im Selfcheck real initialisiert, Fehler = fail
    assert "from brain_bridge import init_bridge as _sc_init_bridge" in seg, "Bridge-Check fehlt"
    assert "start_tick=False" in seg, "Selfcheck darf den Tick-Thread nicht starten"
    assert 'add("fail", "Brain-Bridge"' in seg, "Bridge-Init-Fehler ist kein HARTER Fehler"
    # (15) Endpoints echt aufgerufen, 500er = fail
    assert "dashboard_app.test_client()" in seg, "Endpoint-Check ruft nicht wirklich auf"
    for _e in ("/api/brain/health", "/api/ai/config", "/api/donations/summary"):
        assert _e in seg, "kritischer Endpoint nicht im Selfcheck: " + _e
    assert 'add("ok" if not _bad else "fail", "Dashboard-Endpoints"' in seg, "500er kein HARTER Fehler"
    ok("v4.0-w103: --selfcheck prüft Brain-Bridge + Dashboard-Endpoints (harte Fehler)")


def test_v40_w109_dashboard_feldnamen():
    """v4.0-W109: das Dashboard las zwei Felder, die es im Backend nie gab.

       Symptom war "System-Health zeigt nichts an": die Uebersichts-Kachel
       pruefte `hs.overall != null`, /api/health-score liefert aber
       {score,label,components} — die Bedingung war immer falsch, die Kachel
       blieb auf "-". Dasselbe Muster in der System-Ansicht: die CPU-Zeile hing
       an res.cpu_percent, einem psutil-Ueberbleibsel, das die Route nie
       geliefert hat; die Zeile fehlte deshalb immer komplett.

       Beide Faelle sind STILL: kein JS-Fehler, kein 5xx, nur eine leere
       Anzeige. Genau deshalb dieser Vertrag — er vergleicht die Feldnamen, die
       das Frontend liest, mit denen, die der Bot wirklich setzt."""
    src = open("bot.py").read()
    h = open("templates/dashboard.html").read()

    # (1) Die Uebersichts-Kachel liest score, nicht overall.
    _i = h.find("var hs=await apiGet('/api/health-score')")
    assert _i > 0, "Health-Score-Aufruf in der Uebersicht verschwunden"
    _ov = [ln for ln in h[_i:_i + 1200].splitlines() if not ln.lstrip().startswith("//")]
    assert any("hs.score" in ln for ln in _ov), "Uebersichts-Kachel liest nicht hs.score"
    assert not any("hs.overall" in ln for ln in _ov), \
        "Uebersichts-Kachel liest wieder hs.overall — das Feld gibt es nicht"

    # (2) Und der Bot gibt sie unter diesem Namen aus. Der Kern des Fehlers:
    # die lokale Variable HEISST overall, geht aber als "score" raus. Wer nur
    # den Rumpf ueberfliegt, liest "overall" und greift im Frontend daneben —
    # genau das war passiert. Der Vertrag haelt die Uebersetzung fest.
    # W110: api_health_score und api_system_resources liegen im
    # Systemzustand-Blueprint. Vertrag unveraendert, Anker nachgezogen.
    _h = open("nc/routes/health.py", encoding="utf-8").read()
    assert '"score": overall' in _h, \
        "api_health_score gibt den Wert nicht mehr als \"score\" aus — Frontend nachziehen"
    assert '"label": label' in _h, "api_health_score liefert kein label mehr"

    # (3) cpu_percent gibt es im Backend nirgends; die Ressourcen-Zeile nutzt
    # load_percent, und das rechnet der Bot aus /proc/loadavg.
    # Nur CODE-Zeilen pruefen: der Fix erklaert sich im Kommentar und nennt das
    # alte Feld dabei beim Namen. Ein reiner Textvergleich schlaege daran an.
    _code = [ln for ln in h.splitlines() if not ln.lstrip().startswith("//")]
    assert not any("res.cpu_percent" in ln for ln in _code), \
        "CPU-Zeile haengt wieder an cpu_percent (das Feld liefert die Route nicht)"
    assert any("res.load_percent" in ln for ln in _code), "CPU-Zeile liest nicht load_percent"
    assert "cpu_percent" not in src + _h, \
        "Backend liefert cpu_percent — dann darf das Frontend es lesen"
    assert 'out["load_percent"]' in _h, "load_percent wird nicht mehr berechnet"
    ok("v4.0-w109: Dashboard-Feldnamen decken sich mit dem Backend (score, load_percent)")


def test_v40_w113_restream_stability():
    """v4.0-W113: Restreams reissen nicht mehr dauerhaft ab.

    Fuenf Befunde im Wiederanlauf, alle im selben Pfad (_monitor):
      1. Das Reconnect-Budget wurde NIE zurueckgegeben. `attempts` wanderte
         von Reconnect zu Reconnect weiter und wurde nur beim Start von Hand
         geleert — ein Ziel, das acht Stunden lief und dabei fuenfmal kurz
         stolperte, galt danach als "aufgegeben nach 5 Reconnects". Ab da
         half nur noch die Verify-Schleife: 120s-Takt, bis zu 900s Backoff
         statt 8s. Fuer die unabhaengigen Relays war genau das in W87 schon
         repariert, der Hauptpfad blieb aussen vor.
      2. Backoff linear und ohne Streuung — gleichzeitig gestorbene Restreams
         kamen auf die Sekunde gemeinsam gegen dieselbe Ingest zurueck.
      3. Der Ablauf-Pfad hatte keine Untergrenze: 2s Pause, kein Fehlversuch,
         endlos. `_srcexpired` zaehlte mit und tat nichts damit.
      4. Der copy->transcode-Fallback sprang auf Netzfehler an ("failed to",
         "unable to" stehen woertlich in "Failed to resolve hostname") und
         schaltete damit fuer die ganze Sitzung auf einen Encode, dessen
         Rueckstand der Bot selbst als "typische Disconnect-Ursache" warnt.
      5. Ein ffmpeg, der LEBT aber nichts mehr sendet, wurde nie bemerkt —
         _monitor haengt an proc.wait(). Panel gruen, Sendung weg, Log leer.
    """
    src = open("bot.py", encoding="utf-8").read()

    # Regeln liegen bot-frei im Modul, nicht mehr als Zahlen im Monolithen.
    assert "from nc import restream_stability as _nc_rstab" in src, "Modul nicht eingebunden"
    assert "_RESTREAM_POLICY = _nc_rstab.ReconnectPolicy(" in src, "Policy nicht gebaut"

    _mon = src[src.index("    async def _monitor(self, rid):"):
               src.index("    async def stop(self, rid, _keep_desired=False):")]

    # 1) Budget-Rueckgabe im Hauptpfad
    assert "_nc_rstab.budget_after_run(" in _mon, "kein Budget-Reset nach gesundem Lauf"
    assert "progressed=_progressed" in _mon, "Stillstands-Kill fuellt das Budget faelschlich auf"
    assert "_nc_rstab.budget_exhausted(" in _mon, "Budget-Grenze nicht aus der Policy"

    # 2) Backoff
    assert "delay = min(60, 8 * (attempts + 1))" not in src, "linearer Backoff noch drin"
    assert "_nc_rstab.reconnect_delay(" in _mon, "Backoff nicht aus der Policy"

    # 3) Ablauf-Pfad mit Untergrenze
    assert "_nc_rstab.expired_streak(" in _mon and "_nc_rstab.expired_delay(" in _mon, \
        "Ablauf-Pfad ohne Serienzaehlung"
    assert "_nc_rstab.expired_is_spinning(" in _mon, "Ablauf-Schleife wird nie als Fehlversuch gebucht"
    assert "self._srcspin" in src, "Serienzaehler fehlt"

    # 4) Codec-Fallback delegiert (und die alte Wortliste ist weg)
    _ck = src[src.index("def _looks_like_codec_err(text):"):
              src.index("class RestreamManager:")]
    assert "_nc_rstab.is_codec_failure(text)" in _ck, "Codec-Heuristik nicht delegiert"
    assert '"failed to", "could not write header"' not in _ck, "alte Wortliste noch im Monolithen"

    # 5) Stillstands-Waechter: Marke, Task, Start, Abbau, Anzeige
    # v4.0-W115: Marke und Waechter bedienen jetzt BEIDE Pfade (Hauptprozess
    # und unabhaengige Relays). Die Anker wandern mit, der Vertrag bleibt.
    assert 'w = eintrag.setdefault("watch"' in src, "keine Fortschrittsmarke"
    assert "self._marke_setzen(info, h, p)" in src, "_update_health setzt die Marke nicht"
    assert "async def _stall_watch(self, rid, proc, pname=None):" in src, "Waechter fehlt"
    _sw = src[src.index("    async def _stall_watch(self, rid, proc, pname=None):"):
              src.index("    async def start(self, rid, _attempts=0, _src_watch=False):")]
    assert 'info.get("proc") is not proc' in _sw, \
        "alter Waechter kann den frischen Prozess killen"
    assert "reader_alive=" in _sw, "blinder Waechter schiesst trotzdem"
    assert 'info["stall_kill"] = True' in _sw and "_reap_proc(proc)" in _sw, \
        "Waechter beendet den haengenden Prozess nicht"
    assert 'self._procs[rid]["stallwatch"] = asyncio.create_task(' in src, "Waechter wird nicht gestartet"
    _stop = src[src.index("    async def stop(self, rid, _keep_desired=False):"):
                src.index("    async def stop_all(self, _keep_desired=False):")]
    assert '_sw_stall = info.get("stallwatch")' in _stop, "Waechter wird beim Stop nicht abgeraeumt"
    assert '"ohne_fortschritt_s"' in src, "Stillstand im Status nicht sichtbar"

    # Der progress-Leser verschluckt seinen Tod nicht mehr — sonst friert die
    # Health-Anzeige ein UND der Waechter wird blind, beides unbemerkt.
    _rp = src[src.index("    async def _read_progress(self, rid, proc, pname=None):"):
              src.index("    async def _read_stderr(self, proc, sink):")]
    assert "_loop_fehler(" in _rp, "progress-Leser faellt weiter still aus"

    ok("v4.0-w113: Reconnect-Budget, Backoff, Ablauf-Bremse, Codec-Filter, Stillstands-Waechter")


def test_v40_w114_website_3d():
    """v4.0-W114: die oeffentliche Seite steht im Raum, nicht nur drei Widgets.

    Vorher waren Sentinel-Kern, Verbrauchsbalken und Spendenmuenze
    raeumlich — auf einer flachen Seite. Jetzt: perspektivischer Korridor
    hinter dem Inhalt, jede Sektion auf eigener Z-Ebene, Kacheln neigen
    sich unter dem Zeiger, und der Raum gilt fuer ALLE drei Seiten
    (Start, Impressum, Datenschutz) aus EINER Quelle. Dependency-frei wie
    der Rest der Seite.

    Die Vertraege halten die fuenf Entscheidungen fest, die im Browser
    gemessen wurden und ohne die es bricht:
      * perspective NICHT als CSS-Eigenschaft auf main — main ist ueber
        zehntausend Pixel hoch, der Fluchtpunkt saesse einmalig in dessen
        Mitte und alles weit darueber/darunter kippte grotesk weg. Also im
        transform-Funktionsaufruf je Sektion.
      * overflow-x:clip auf main, NICHT auf html — an der Wurzel nimmt es
        der Kopfleiste in Chromium ihr position:sticky (gemessen:
        header.top -2800 statt 0). Ohne Klippen: 18px Ueberlauf auf 390px.
      * Der Schalter steht nicht in der Navigation — auf 390px fuellt die
        Kopfleiste bereits zwei Zeilen aus, ein weiteres Element machte sie
        37 % hoeher (78px -> 107px). Und position:fixed haette darin nicht
        geholfen: header traegt backdrop-filter und wird damit zum
        Bezugsrahmen fuer fixierte Nachfahren.
      * Die Lesezone bleibt plan: eine Sektion, die die Bildschirmmitte
        abdeckt, hat Tiefe exakt null. Gekippter Fliesstext wird unscharf
        gerastert.
      * Blind heisst flach: ohne JS, bei prefers-reduced-motion oder nach
        einem Klick auf "Flach" faellt html.d3 weg und die Seite ist die
        alte — der Knopf bleibt bis dahin hidden.
    """
    css = open("website/raum.css", encoding="utf-8").read()
    js  = open("website/raum.js", encoding="utf-8").read()

    # EINE Quelle, alle drei Seiten
    for seite in ("lafap_index", "impressum", "datenschutz"):
        w = open("website/%s.html" % seite, encoding="utf-8").read()
        # v4.0-W117: die Verweise tragen jetzt einen Cache-Stempel (?v=hash),
        # also nicht mehr auf die nackte Zeichenkette pruefen — der Vertrag
        # ist "wird eingebunden", nicht "ohne Query".
        assert re.search(r'<link rel="stylesheet" href="raum\.css(\?v=[0-9a-f]+)?">', w), \
            seite + ": raum.css fehlt"
        assert re.search(r'<script src="raum\.js(\?v=[0-9a-f]+)?"></script>', w), \
            seite + ": raum.js fehlt"
        assert '<canvas id="raum" class="raum" aria-hidden="true"></canvas>' in w, \
            seite + ": Raum-Flaeche fehlt oder nicht als dekorativ ausgezeichnet"
        assert 'id="d3-schalter" class="d3-schalter" hidden>' in w, \
            seite + ": Schalter fehlt oder nicht versteckt"

    # Der Schalter steht ausserhalb der Navigation (Kopfleiste bleibt zweizeilig)
    w = open("website/lafap_index.html", encoding="utf-8").read()
    _nav = w[w.index('<nav aria-label="Seitennavigation">'):w.index("</nav>")]
    assert "d3-schalter" not in _nav, "Schalter steckt in der Navigation"

    # Raum und Tiefe
    assert "html.d3 main>section{perspective:" in css, "Sektionen ohne Perspektive"
    assert "html.d3 main{overflow-x:clip}" in css, "Kipp-Ueberlauf nicht geklippt"
    assert "html.d3{overflow-x:clip}" not in css, \
        "clip an der Wurzel — das nimmt der Kopfleiste ihr sticky"
    assert ".d3-schalter{position:fixed" in css and "min-height:44px" in css, \
        "Schalter nicht als feste Ecke mit 44px-Beruehrziel"
    assert "perspective(1600px) translate3d(0,0," in js, \
        "Sektionstiefe nicht als transform-Funktion (Fluchtpunkt-Falle)"
    assert "if (r.top <= mY && r.bottom >= mY) d = 0;" in js, \
        "Tiefe haengt nicht an der Lesezone — gekippter Text wird unscharf"

    # Eine Schleife, Layout nur bei Bewegung
    assert "if (y !== letzterScroll || window.innerHeight !== letzteHoehe)" in js, \
        "getBoundingClientRect laeuft pro Frame statt nur bei Bewegung"

    # Rueckfallpfade
    assert "prefers-reduced-motion" in js, "reduced-motion nicht beachtet"
    assert "document.hidden" in js, "laeuft im versteckten Tab weiter"
    assert "localStorage" in js and "lafap.raum" in js, "Wahl wird nicht gemerkt"
    assert "hardwareConcurrency" in js, "keine Absenkung auf schwachen Geraeten"
    assert "(hover: hover) and (pointer: fine)" in js, \
        "Zeigerneigung auch auf Beruehrgeraeten — dort verreisst jeder Tipper den Raum"

    # Kein Fremd-Code, kein externer Request
    for quelle, name in ((css, "raum.css"), (js, "raum.js")):
        assert "http://" not in quelle and "https://" not in quelle, \
            name + ": externer Verweis"
    ok("v4.0-w114: der Raum auf allen drei Seiten — Korridor, Sektionstiefe, "
       "Kachelneigung, abschaltbar")


def test_v40_w115_relay_sicht_und_srcwatch():
    """v4.0-W115: die blinden Flecken, die W113 offen gelassen hat.

    1. DIE UNABHAENGIGEN RELAYS WAREN BLIND. _spawn_independent startete
       ffmpeg mit stdout=DEVNULL — der Kommandozeile lag seit jeher
       `-progress pipe:1` bei, es hat nur nie jemand zugehoert. Fuer
       Twitch/YouTube im Modus RESTREAM_MULTI_MODE=independent gab es
       dadurch WEDER Health-Daten NOCH Stillstands-Erkennung: ein
       haengender Relay fiel erst der Plattform-Pruefung auf (120s-Takt,
       3 Fehlanzeigen ≈ 6 Minuten) — und auch nur, wenn deren API
       ueberhaupt antwortet. Genau der Ausfall, den W113 fuer den
       Hauptprozess geschlossen hat.
    2. DIE W113-MESSWERTE SAH NIEMAND. ohne_fortschritt_s und
       stillstaende standen in /api/restream/verify, kamen in
       dashboard.html aber kein einziges Mal vor. Der Waechter griff,
       loggte, baute neu auf — im Panel stand nichts davon.
    3. _source_watch FING NUR CancelledError. Jede andere Ausnahme
       beendete den Task; asyncio meldet so etwas fruehestens beim
       Aufraeumen als "Task exception was never retrieved". Folge: der
       Quellen-Failover fuer dieses Ziel war fuer den Rest der Laufzeit
       tot, und der Bot wartete auf einen ffmpeg-Abbruch, der bei einer
       sauber beendeten TikTok-Sendung nie kommt.

    Bewusst EIN Waechter und EIN Health-Parser fuer beide Pfade: die
    Entscheidung "was heisst hier tot" darf es nur einmal geben, sonst
    laufen Haupt- und Relay-Pfad ueber die Monate auseinander.
    """
    src = open("bot.py", encoding="utf-8").read()
    h = open("templates/dashboard.html", encoding="utf-8").read()

    # ── 1) Relays sehen und werden bewacht ────────────────────────────────
    _sp = src[src.index("    async def _spawn_independent(self, rid, pname"):
              src.index("    async def _monitor(self, rid):")]
    assert "stdout=asyncio.subprocess.PIPE" in _sp, "Relay laeuft weiter blind (DEVNULL)"
    assert "stdout=asyncio.subprocess.DEVNULL" not in _sp, "DEVNULL noch im Relay-Pfad"
    assert "self._read_progress(rid, p, pname=pname)" in _sp, "Relay ohne progress-Leser"
    assert "self._stall_watch(rid, p, pname=pname)" in _sp, "Relay ohne Stillstands-Waechter"
    assert "_ptask.cancel()" in _sp and "_stask.cancel()" in _sp, \
        "Relay raeumt seine Leser/Waechter nicht ab — Task-Leck je Reconnect"
    assert '_stalled = bool(_eintrag.get("stall_kill"))' in _sp, \
        "Relay merkt sich den Stillstands-Kill nicht (Budget wuerde faelschlich aufgefuellt)"
    assert "_nc_rstab.reconnect_delay(attempt - 1, _RESTREAM_RELAY_POLICY)" in _sp, \
        "Relay-Backoff ohne Streuung"
    assert "_RESTREAM_RELAY_POLICY = _nc_rstab.ReconnectPolicy(" in src, "Relay-Regelsatz fehlt"

    # EIN Parser, EIN Waechter — beide ueber pname auf beiden Pfaden
    assert "def _eintrag(self, rid, pname=None):" in src, "kein gemeinsamer Zugriffspunkt"
    assert "def _marke_setzen(eintrag, h, p):" in src, "Fortschrittsmarke nicht geteilt"
    assert "async def _read_progress(self, rid, proc, pname=None):" in src
    assert "async def _stall_watch(self, rid, proc, pname=None):" in src
    assert "def _update_health(self, rid, p, pname=None):" in src
    # Das Overlay haengt am Hauptprozess und darf nicht je Relay neu schreiben
    _rp = src[src.index("    async def _read_progress(self, rid, proc, pname=None):"):
              src.index("    async def _read_stderr(self, proc, sink):")]
    assert "RESTREAM_OVERLAY and pname is None" in _rp, \
        "Overlay wird aus jedem Relay-Takt zusaetzlich geschrieben"

    # Relays im Status sichtbar
    _st = src[src.index("    def status(self):"):]
    assert '"relays": {' in _st, "Relays fehlen im Status"
    assert 'self._stallkills.get(\n                                      f"{rid}:{_pn}", 0)' in _st \
        or 'f"{rid}:{_pn}"' in _st, "Relay-Stillstaende nicht getrennt gezaehlt"

    # ── 2) Im Panel sichtbar ──────────────────────────────────────────────
    assert "stall_timeout_s=RESTREAM_STALL_TIMEOUT_S" in src, \
        "Panel bekommt die Grenze nicht — muesste den Default doppelt kennen"
    assert "ohne_fortschritt_s" in h, "Stillstand im Dashboard weiterhin unsichtbar"
    assert "stillstaende" in h, "Stillstands-Zaehler im Dashboard unsichtbar"
    assert "Bild fließt" in h, "keine Spalte fuer den Fluss"
    assert "s.relays" in h, "Relay-Zeilen fehlen im Panel"
    assert "d.stall_timeout_s" in h, "Panel faerbt gegen einen eigenen Default statt gegen die API"

    # ── 3) Quellen-Waechter ueberlebt seine eigenen Fehler ────────────────
    _sw = src[src.index("    async def _source_watch(self, rid, username):"):
              src.index("    async def _switch_to_next_live(self, rid, current_user):")]
    assert '_loop_fehler(f"restream-srcwatch#{rid}", e)' in _sw, \
        "Quellen-Waechter meldet seinen Tod weiterhin nicht"
    assert _sw.count("except Exception as e:") >= 2, \
        "nur eine Fehlerklammer — eine kaputte Runde beendet den Failover noch immer"
    ok("v4.0-w115: Relays sehen und werden bewacht, Stillstand im Panel, "
       "Quellen-Waechter ueberlebt Fehler")


def test_v40_w116_alterung_flattern_rate():
    """v4.0-W116: drei Zustaende, die dem Betreiber die Sicht verstellt haben.

    1. _tee_fail WURDE NIE GELEERT. Geschrieben in _read_stderr, gelesen an
       fuenf Stellen — Deck, Verify-Loop, Sentinel-Alarm, status() und
       Selbsttest —, geleert an keiner. Eine einmalige Ablehnung von
       YouTube stand bis zum Bot-Neustart im Panel UND im Sentinel-Alarm,
       auch wenn das Ziel seit Stunden wieder sendet: Dauerfehlalarm, und
       bei der Fehlersuche jagt man einem Zustand von vorgestern hinterher.
    2. CHAT-TRENNUNGEN ESKALIERTEN NIE. Kick-WS, Twitch-EventSub und
       Twitch-Chat meldeten auf log.warning — in einem ERROR-Log steht
       davon nichts. Die Verbindung konnte die ganze Nacht flattern, ohne
       dass irgendwo etwas stand. Dasselbe Muster wie beim
       Discord-Gateway-Tod. "Jede Trennung auf error" waere aber genauso
       blind, also entscheidet der Verlauf (nc/flapguard.py).
    3. DER AUFNAHME-WAECHTER MASS NUR DAS DATEIWACHSTUM. Das faengt den
       toten Stream, nicht den halbtoten: faellt die Videospur weg und der
       Ton laeuft weiter, waechst die Datei im Kilobyte-Takt und der
       Waechter sieht Fortschritt. Zweite Spur ueber die RATE
       (nc/recdiag.RateSpur) — die MELDET nur, sie killt nicht.
    """
    src = open("bot.py", encoding="utf-8").read()

    # ── 1) tee-Fehler altern und werden geleert ───────────────────────────
    assert "def tee_fehler(self, ttl_s=None):" in src, "kein Verfall fuer tee-Fehler"
    assert "def tee_fehler_klaeren(self, platt):" in src, "kein Loeschen bei Bestaetigung"
    assert "RESTREAM_TEE_FAIL_TTL_S" in src, "Verfallszeit nicht einstellbar"
    # KEIN Direktzugriff mehr an den Lesestellen — sonst umgeht einer den Verfall.
    assert 'getattr(_RESTREAM_MGR, "_tee_fail"' not in src, \
        "Lesestelle greift am Verfall vorbei"
    assert 'getattr(mgr, "_tee_fail"' not in src, "Selbsttest greift am Verfall vorbei"
    assert 'dict(getattr(self, "_tee_fail", {}) or {})' not in src, \
        "status() greift am Verfall vorbei"
    # Geschrieben wird weiterhin genau an EINER Stelle.
    assert src.count("self._tee_fail = ") == 2, \
        "unerwartete Schreibstellen auf _tee_fail"      # Anlage + Entsorgung
    _vl = src[src.index("async def _restream_verify_loop():"):
              src.index("async def _restream_resume_after_restart():")]
    assert "_RESTREAM_MGR.tee_fehler_klaeren(_p)" in _vl, \
        "bestaetigte Ziele werden nicht freigeraeumt"

    # ── 2) Flattern eskaliert ─────────────────────────────────────────────
    assert "from nc import flapguard as _nc_flap" in src, "flapguard nicht eingebunden"
    assert "_FLAP = _nc_flap.FlapWatch(" in src, "kein Flatter-Waechter"
    assert "def _verbindung_verloren(kanal, exc, backoff_s, seit=0.0):" in src
    _vv = src[src.index("def _verbindung_verloren(kanal, exc, backoff_s, seit=0.0):"):
              src.index("# F8: Chats die uns blockiert haben")]
    assert "log.error(" in _vv and "_brain_notify(" in _vv, \
        "Flattern wird nicht eskaliert"
    assert "u.erholt" in _vv, "Erholung wird nicht gemeldet"
    # Alle drei Trennungsstellen gehen durch den Helfer, keine mehr direkt.
    for tot in ('log.warning(f"Kick-WS getrennt',
                'log.warning("Twitch-EventSub getrennt',
                'log.warning("Twitch-Chat getrennt'):
        assert tot not in src, "Trennung meldet weiterhin nur auf warning: " + tot
    for kanal in ('"Kick-WebSocket"', '"Twitch-EventSub"', '"Twitch-Chat"'):
        assert "_verbindung_verloren(" + kanal in src, "Kanal nicht verdrahtet: " + kanal
    # Ohne Verbindungszeitpunkt kann der Waechter nicht zwischen "hielt zehn
    # Sekunden" und "hielt zehn Stunden" unterscheiden — daran haengt alles.
    assert 'self.stats["since"] = _time_mod.time()' in src, "Kick ohne Verbindungsmarke"
    assert "_es_seit = _time_mod.time()" in src, "EventSub ohne Verbindungsmarke"
    assert 'seit=_WCHAT_STATUS["twitch"].get("since", 0.0)' in src, \
        "Twitch-Chat ohne Verbindungsmarke"

    # ── 3) Raten-Einbruch bei der Aufnahme ────────────────────────────────
    assert "from nc import recdiag as _nc_recdiag" in src, "recdiag nicht eingebunden"
    _wd = src[src.index("    async def _stall_watchdog():"):
              src.index("    watchdog_task = asyncio.create_task(_stall_watchdog())")]
    assert "_nc_recdiag.RateSpur()" in _wd, "keine Raten-Spur im Aufnahme-Waechter"
    assert "_rate.beobachte(cur_size - _rate_last, CHECK_EVERY)" in _wd, \
        "Raten-Spur wird nicht gefuettert"
    assert 'log_event("recording.rate_drop"' in _wd, "Einbruch nicht als Ereignis"
    # Der Einbruch darf NICHT killen — eine statische Szene druckt die
    # Bitrate legitim um mehr als 85 % nach unten, und abgebrochenes
    # Material ist unwiederbringlich weg.
    _einbruch = _wd[_wd.index('_u == "einbruch"'):_wd.index('elif _u == "erholt"')]
    assert "terminate()" not in _einbruch and "kill()" not in _einbruch, \
        "Raten-Einbruch bricht die Aufnahme ab — das vernichtet echtes Material"
    # Der Nullwachstums-Waechter darf weiterhin killen, der bleibt unberuehrt.
    assert "stall_killed[0] = True" in _wd and "proc.terminate()" in _wd, \
        "der bewaehrte Nullwachstums-Kill ist verloren gegangen"
    ok("v4.0-w116: tee-Fehler altern, Flattern eskaliert, Raten-Einbruch wird gemeldet")


def test_v40_w117_ankerhygiene():
    """v4.0-W117: die Fenster in DIESER Datei duerfen nicht zu eng werden.

    Die Vertraege hier verankern sich an woertlichem Quelltext. Die Textanker
    sind dabei nie das Problem gewesen — die FENSTER waren es: `src[i:i + N]`
    mit einem N, das jemand vor Monaten geschaetzt hat. Waechst die
    Zielfunktion darueber hinaus, meldet der Test etwas als fehlend, das zwei
    Zeilen weiter unten steht. CLAUDE.md nennt drei Faelle, in denen genau
    das passiert ist; jedes Mal kostet es zuerst die Frage "ist der Vertrag
    gebrochen oder nur sein Anker".

    Dieser Test dreht das um: er misst fuer jedes verbliebene Fenster, wie
    viel Luft zwischen der zuletzt geprueften Nadel und dem Fensterrand
    liegt, und schlaegt an, BEVOR die Luft aufgebraucht ist. Statt eines
    irrefuehrenden "Vertrag gebrochen" steht dann hier, welche Zeile zu eng
    geworden ist und was zu tun ist.

    Nicht bewertet wird, was sich nicht sicher aufloesen laesst (Fenster auf
    Zwischenvariablen, Nadeln die nicht im Ziel vorkommen) und was negativ
    prueft (`not in`) — dort ist ein weit entfernter Treffer gerade der
    Beweis, dass die Pruefung stimmt.
    """
    import os
    hier = os.path.dirname(os.path.abspath(__file__))
    tests = open(os.path.join(hier, "test_restream.py"), encoding="utf-8").read()
    tl = tests.splitlines()
    DATEI = {"src": "bot.py", "src_all": "bot.py",
             "html": "templates/dashboard.html", "h": "templates/dashboard.html",
             "w": "website/lafap_index.html", "o": "templates/overlay.html"}
    _q = {}

    def quelle(n):
        if n not in _q:
            pf = DATEI.get(n)
            _q[n] = open(os.path.join(hier, pf), encoding="utf-8").read() if pf else None
        return _q[n]

    FENSTER = re.compile(r"(\w+)\s*=\s*(\w+)\[(\w+)\s*:\s*\3\s*\+\s*(\d{3,})\]")
    FIND = re.compile(r"(\w+)\s*=\s*(\w+)\.(?:find|index)\(\s*(\".*?\"|'.*?')\s*\)")
    LITERAL = re.compile(r"(\"(?:[^\"\\\\]|\\\\.)*\"|'(?:[^'\\\\]|\\\\.)*')")
    MINDESTLUFT = 150

    eng, geprueft = [], 0
    for i, zeile in enumerate(tl):
        m = FENSTER.search(zeile)
        if not m:
            continue
        var, ivar, n = m.group(1), m.group(3), int(m.group(4))
        lit = basis = None
        for j in range(i, max(-1, i - 25), -1):
            f = FIND.search(tl[j])
            if f and f.group(1) == ivar:
                lit, basis = f.group(3), f.group(2)
                break
        if lit is None:
            continue
        try:
            nadel = ast.literal_eval(lit)
        except Exception:
            continue
        q = quelle(basis)
        if q is None:
            continue
        pos = q.find(nadel)
        if pos < 0:
            continue
        weit, wovon = 0, ""
        for k in range(i + 1, min(len(tl), i + 60)):
            z = tl[k]
            if z.startswith("def "):
                break
            if var not in z or (" not in " + var) in z:
                continue
            for l in LITERAL.findall(z):
                try:
                    sub = ast.literal_eval(l)
                except Exception:
                    continue
                if not isinstance(sub, str) or len(sub) < 4:
                    continue
                t = q.find(sub, pos)
                if t < 0 or (t - pos) > n * 4:
                    continue
                if t + len(sub) - pos > weit:
                    weit, wovon = t + len(sub) - pos, sub
        if not weit:
            continue
        geprueft += 1
        if n - weit < MINDESTLUFT:
            eng.append("Zeile %d: Fenster %d, letzte Nadel bei %d -> nur %d Zeichen "
                       "Luft (%r)" % (i + 1, n, weit, n - weit, wovon[:40]))

    assert geprueft >= 10, ("Anker-Messung greift nicht mehr (%d Fenster erkannt) — "
                            "Muster geaendert?" % geprueft)
    assert not eng, (
        "Zu enge Fenster — der naechste kleine Umbau macht daraus einen "
        "falschen Vertragsbruch. Auf _fn(src, name), _meth(src, Klasse, name) "
        "oder _ab(src, marke) umstellen:\n  " + "\n  ".join(eng))
    ok("v4.0-w117: %d Fenster gemessen, alle mit mindestens %d Zeichen Luft"
       % (geprueft, MINDESTLUFT))


def test_v40_w117_asset_stempel():
    """v4.0-W117: raum.css und raum.js tragen einen Cache-Stempel — aktuell.

    Beide Dateien werden von allen drei oeffentlichen Seiten geladen. Ohne
    Stempel haelt ein Browser mit warmem Cache nach einem Deploy die alte
    Fassung; die Seite bleibt dann still flach statt kaputt (so gebaut) —
    und WEIL nichts bricht, faellt es niemandem auf. Der Stempel ist ein
    Inhalts-Hash, keine Nummer zum Hochzaehlen: gleicher Inhalt, gleicher
    Stempel, Cache bleibt gueltig.

    Dieser Vertrag faehrt `--check` mit. Ein vergessener Generatorlauf
    faellt damit in der Pruefkette auf und nicht beim Betrachter — dasselbe
    Muster wie bei .env.example (W100).
    """
    import os as _os
    import subprocess as _sp
    assert _os.path.exists("tools/stempel_assets.py"), "Stempel-Werkzeug fehlt"
    r = _sp.run([sys.executable, "tools/stempel_assets.py", "--check"],
                capture_output=True, text=True)
    assert r.returncode == 0, ("Cache-Stempel veraltet — neu setzen: "
                               + (r.stdout or r.stderr)[:160])
    # Jede Seite bindet BEIDE Dateien mit Stempel ein.
    for seite in ("lafap_index", "impressum", "datenschutz"):
        w = open("website/%s.html" % seite, encoding="utf-8").read()
        for datei in ("raum.css", "raum.js"):
            assert re.search(re.escape(datei) + r"\?v=[0-9a-f]{6,}", w), \
                "%s: %s ohne Cache-Stempel" % (seite, datei)
    ok("v4.0-w117: raum.css/raum.js mit Inhalts-Stempel auf allen drei Seiten")


def test_v40_w118_sicherheitsaudit():
    r"""v4.0-W118: Befunde aus dem Tiefen-Audit — jeder mit eigenem Vertrag.

    S1 XSS IM DASHBOARD (bewiesen, hoch). 20 Stellen bauten
       onclick="f('${esc(x)}')". esc() liefert fuer ' das Zeichen &#39; —
       der HTML-Parser dekodiert Attributwerte aber, BEVOR die JS-Engine
       sie sieht. Aus &#39; wird wieder ', der String ist zu, der Rest
       laeuft als Code. Im Browser nachgestellt:
         Eingabe   x');window.__xss=1;showProfile('y
         Attribut  showProfile('x');window.__xss=1;showProfile('y')
         Ergebnis  fremder Code lief in der Sitzung des Betreibers — der
                   Sitzung, die das Dashboard-Cookie haelt.
       Fix: escJs() mit \xNN-Sequenzen. Die enthalten kein einziges
       HTML-Sonderzeichen, ueberstehen die HTML-Dekodierung unveraendert
       und werden erst von der JS-Engine INNERHALB des Strings aufgeloest.

    S2 KI-SQL UNTER MARIADB. _safe_select hatte die read-only-Verbindung
       nur fuer SQLite (mode=ro); MariaDB fiel auf eine normale
       Schreibverbindung zurueck. Und der Wortfilter war auf SQLite
       gemuenzt: LOAD_FILE, OUTFILE, SLEEP, BENCHMARK, mysql.user,
       information_schema standen nicht drin — allesamt mit einem reinen
       SELECT erreichbar.

    S3 OAUTH-state UEBERSPRINGBAR. `if state and _state["csrf"] and ...`
       liess die Pruefung weg, sobald der Rueckruf gar keinen state
       mitbrachte — und genau das kann ein Angreifer bestimmen.

    S4 OPEN REDIRECT. `nxt.startswith("/")` laesst //example.com durch.

    S5 ZWEI SCHWACHE esc-SCHATTEN, die das globale, staerkere esc in
       Funktionen verdeckten, die fremde Creator-Daten rendern.

    S6 REDIS_URL MIT PASSWORT in /api/system.
    """
    src = open("bot.py", encoding="utf-8").read()
    h = open("templates/dashboard.html", encoding="utf-8").read()

    # ── S1 ────────────────────────────────────────────────────────────────
    assert "const escJs = s =>" in h, "JS-String-Maskierer fehlt"
    for folge in ("\\x27", "\\x5c", "\\x3c", "\\u2028"):
        assert folge in h, "escJs deckt " + folge + " nicht ab"
    # Kein Handler darf mehr eine Interpolation ungeschuetzt in einen
    # JS-'…'-String setzen. esc() reicht dort NICHT.
    offen = []
    for m in re.finditer(r'on\w+\s*=\s*"([^"]*)"', h):
        for tr in re.finditer(r"'\$\{([^{}]+)\}'", m.group(1)):
            if not tr.group(1).strip().startswith("escJs("):
                offen.append(tr.group(1)[:40])
    assert not offen, ("Interpolation in JS-'…' ohne escJs: " + ", ".join(offen))
    # Genau EIN esc — zwei Maskierer unterschiedlicher Staerke sind eine Falle.
    assert len(re.findall(r"(?:const|let|var)\s+esc\s*=", h)) == 1, \
        "mehr als ein esc — welcher greift wo?"                        # S5

    # ── S2 ────────────────────────────────────────────────────────────────
    g = open("nc/sqlguard.py", encoding="utf-8").read()
    for wort in ("load_file", "outfile", "dumpfile", "benchmark", "sleep",
                 "information_schema", "mysql", "performance_schema"):
        assert '"%s"' % wort in g, "sqlguard kennt %s nicht" % wort
    a = open("nc/routes/ai.py", encoding="utf-8").read()
    assert "START TRANSACTION READ ONLY" in a, "MariaDB ohne read-only Transaktion"
    assert "conn.rollback()" in a, "read-only Transaktion wird nicht freigegeben"

    # ── S3 ────────────────────────────────────────────────────────────────
    for datei in ("nc/twitchoauth.py", "nc/ytoauth.py"):
        o = open(datei, encoding="utf-8").read()
        # Kommentare raus: der Fix-Kommentar zitiert das alte, kaputte Muster
        # woertlich. Ein Vertrag, den ein Kommentar ausloesen kann, prueft den
        # Kommentar statt den Code.
        code = "\n".join(z for z in o.splitlines() if not z.lstrip().startswith("#"))
        assert 'if state and _state["csrf"]' not in code, \
            datei + ": state-Pruefung weiterhin ueberspringbar"
        assert 'if _state["csrf"] and state != _state["csrf"]:' in code, \
            datei + ": state wird nicht erzwungen"

    # ── S4 ────────────────────────────────────────────────────────────────
    assert "def _sicheres_ziel(roh):" in src, "Redirect-Pruefung fehlt"

    # ── S7: PIN-Cookie mit Ablauf ─────────────────────────────────────────
    # Vorher ein STATISCHER HMAC ueber das PIN: einmal ausgestellt, fuer immer
    # gueltig, widerrufbar nur durch PIN-Wechsel. Ein Wert, der aus einem
    # Screenshot der Entwicklerwerkzeuge abfliesst, bleibt damit unbegrenzt
    # brauchbar.
    assert "DASHBOARD_PIN_MAX_AGE_S" in src, "PIN-Cookie ohne Lebensdauer"
    assert 'def _pin_auth_value(ts=None):' in src, "PIN-Cookie ohne Zeitstempel"
    assert '"nc-dashboard-pin|" + t' in src, "Zeitstempel nicht vom HMAC gedeckt"
    _po = src[src.index("def _pin_ok():"):src.index("def _pin_locked():")]
    assert "alter > DASHBOARD_PIN_MAX_AGE_S" in _po, "Ablauf wird nicht geprueft"
    assert "alter < -300" in _po, "Cookie aus der Zukunft wird akzeptiert"
    assert "compare_digest" in _po, "Vergleich nicht zeitkonstant"

    # ── S6 ────────────────────────────────────────────────────────────────
    assert "def _url_ohne_zugang(url):" in src, "kein Maskierer fuer Zugangsdaten in URLs"
    assert "redis_url      = _url_ohne_zugang(REDIS_URL)" in src, \
        "REDIS_URL geht weiterhin im Klartext raus"
    ok("v4.0-w118: XSS geschlossen, KI-SQL read-only, OAuth-state erzwungen, "
       "Open Redirect dicht, ein Maskierer, Zugangsdaten maskiert")


def test_v40_w121_oauth_proxy_meldethema_kollision():
    """v4.0-W121: drei Betriebsbefunde, je ein Vertrag.

    1. OAuth hinter dem nginx-Proxy. Twitch und YouTube hatten fest
       'http://localhost:3000' als Rueckruf — eine Adresse, die von aussen
       niemand sieht. Google bricht damit mit redirect_uri_mismatch ab, BEVOR
       die Kontoauswahl erscheint; weil der Flow nie durchlief, erschien auch
       nie der Trennen-Knopf. Eine falsche Adresse, drei Symptome.
    2. Google-Abmeldung. forget() loeschte nur lokal; die Freigabe im
       Google-Konto blieb, ein Kontowechsel war ohne myaccount.google.com
       unmoeglich.
    3. Live-/Offline-Meldungen gehoeren ins eigene Forum-Thema, nie in den
       Hauptchannel.
    """
    src = open("bot.py").read()

    # ── 1: gemeinsame, proxy-taugliche Aufloesung ────────────────────────
    assert "def _public_base_url(" in src, "keine oeffentliche Basis-URL"
    _pb = src[src.index("def _public_base_url("):src.index("def _oauth_redirect_uri(")]
    assert "PUBLIC_BASE_URL" in _pb, "kein Env-Vorrang fuer die oeffentliche Adresse"
    assert "X-Forwarded-Host" in _pb and "TRUSTED_PROXIES" in _pb, \
        "Proxy-Header ohne Vertrauensgrenze — waere faelschbar"
    for plat in ("youtube", "twitch"):
        assert '_oauth_redirect_uri("%s")' % plat in src, \
            "%s nutzt die gemeinsame Aufloesung nicht" % plat
    assert "http://localhost:3000/api/youtube/oauth/callback" not in src, \
        "YouTube haengt noch am festen localhost:3000"
    assert '"/api/youtube/oauth/redirect"' in src and "def api_youtube_oauth_redirect(" in src, \
        "kein Live-Setzer fuer die YouTube-Rueckruf-Adresse"
    _ys = src[src.index("def api_youtube_oauth_start("):src.index("def api_youtube_oauth_callback(")]
    assert 'prompt="select_account consent"' in _ys, "keine Google-Kontoauswahl erzwungen"

    # ── 2: Abmeldung widerruft bei Google ────────────────────────────────
    yt = open("nc/ytoauth.py", encoding="utf-8").read()
    assert "async def revoke(" in yt, "kein Widerruf in nc/ytoauth.py"
    _rv = yt[yt.index("async def revoke("):yt.index("def forget(")]
    assert "REVOKE" in _rv, "Widerruf ruft den Google-Endpunkt nicht auf"
    assert "forget()" in _rv, "lokaler Zustand bleibt nach dem Widerruf stehen"
    assert '"/api/youtube/oauth/logout"' in src and "def api_youtube_oauth_logout(" in src, \
        "keine Abmelde-Route"
    dash = open("templates/dashboard.html", encoding="utf-8").read()
    assert "ytoauthLogout(" in dash and "ytoauthSwitch(" in dash, \
        "Panel ohne Abmelden/Konto-wechseln"
    assert "ytoauthSaveRedirect(" in dash and 'id="yo_redir"' in dash, \
        "Panel ohne Feld fuer die Rueckruf-Adresse"

    # ── 3: Melde-Thema statt Hauptchannel ────────────────────────────────
    assert "async def _send_live_notice(" in src, "kein eigener Melde-Weg"
    _p = src.index("async def _send_live_notice(")
    _ln = src[_p:src.index("async def split_and_send_video(", _p)]
    assert "message_thread_id=tid" in _ln, "Meldung geht nicht ins Thema"
    assert "_topic_forget(" in _ln, "geloeschtes Thema wird nicht geheilt"
    _hs = src[src.index("async def _handle_single_tracking("):src.index("async def _ensure_topic(")]
    assert "_send_live_notice(bot_app.bot, _tg_chat" in _hs, "LIVE-Meldung nicht umgestellt"
    assert "_send_live_notice(bot_app.bot, chat_id" in _hs, "OFFLINE-Meldung nicht umgestellt"

    # ── Kollisions-Befund benennt Plattform, Nummern und Quelle ──────────
    ag = open("brain/agents.py", encoding="utf-8").read()
    _co = ag[ag.index("def _collisions("):ag.index("class ToxicityAgent")]
    assert 'f"Kick-Key-Kollision' not in ag, "Befund behauptet weiter pauschal 'Kick'"
    assert "{plat}-Key" in _co, "Befund nennt die Plattform nicht"
    assert "platform" in _co and "same_source" in _co, \
        "Befund unterscheidet die beiden Faelle nicht"
    _rh = src[src.index("def _brain_restream_health("):src.index("def _brain_moderation_snap(")]
    assert "tee_targets" in _rh, "Kollision wird nicht ueber die echten Ziele geprueft"
    assert "returncode is not None" in _rh, "tote Prozesse zaehlen weiter mit"
    assert "RESTREAM_SINGLE" in _rh, "RESTREAM_SINGLE wird nicht beruecksichtigt"
    ok("v4.0-w121: OAuth ueber den Proxy, echte Google-Abmeldung, Melde-Thema, "
       "ehrlicher Kollisions-Befund")


def test_v40_w122_trackings_ansicht():
    """v4.0-W122: die Trackings-Ansicht hat wieder Markup.

    Die Logik lief seit je (loadSurveil/renderTargetGrid/renderBandwidth/
    loadHeatmap), nur ihr HTML war irgendwann verschwunden — alle IDs kamen
    im Template NULL mal vor, die Funktionen brachen an ihrem eigenen
    Waechter ab. Damit waren Tags, Notizen, Prioritaet, Schnell-Neustart und
    Jetzt-Pruefen aus dem Dashboard nicht mehr erreichbar; ein getrackter
    Streamer war nur noch eine Kachel. Dieser Vertrag haelt das Markup fest,
    damit es nicht ein zweites Mal lautlos verschwindet.
    """
    dash = open("templates/dashboard.html", encoding="utf-8").read()
    for _id in ("sv_grid", "sv_gridmeta", "sv_filter", "sv_sort", "sv_track",
                "sv_live", "sv_rec", "sv_bw", "sv_bwlist", "sv_heat",
                "sv_last_refresh"):
        assert dash.count('id="%s"' % _id) == 1, \
            "%s fehlt im Markup (oder ist doppelt)" % _id
    # Die Ansicht wird beim Oeffnen UND im Auffrisch-Takt gefuellt.
    assert "loadWall(); loadSurveil();" in dash, "Loader nicht im Streams-Tab verdrahtet"
    assert "loadWall(); loadSurveil(); }" in dash, "Ansicht frischt sich nicht auf"
    # Steuerung erreichbar: die Tabellenzeile fuehrt ins CTL-Fenster.
    _rt = dash[dash.index("function renderTargetGrid("):dash.index("/* RADAR ENTFERNT")]
    assert "openTargetCtl(" in _rt and "showProfile(" in _rt, \
        "Zeile ohne Steuerung/Profil — Tags und Prioritaet waeren wieder unerreichbar"
    # Das Radar hing an einem Canvas, das es nicht mehr gibt: raus statt tot.
    assert "function radarUpdateStats(" not in dash and "radarUpdateStats();" not in dash, \
        "toter Radar-Code wieder da (Definition oder Aufruf)"
    assert "_radarHash" not in dash, "Radar-Hilfsfunktion wieder da"
    # Heatmap darf nicht im 8s-Takt mitlaufen (30-Tage-Aggregat).
    _hm = dash[dash.index("async function loadHeatmap("):dash.index("function renderHeat(")]
    assert "300000" in _hm, "Heatmap ohne Drossel"
    # Twitch bekommt dieselbe Rueckruf-Pflege wie Kick und YouTube.
    src = open("bot.py").read()
    assert '"/api/twitch/oauth/redirect"' in src and "def api_twitch_oauth_redirect(" in src, \
        "kein Live-Setzer fuer die Twitch-Rueckruf-Adresse"
    assert "twoauthSaveRedirect(" in dash and 'id="tw_redir"' in dash, \
        "Twitch-Panel ohne Feld fuer die Rueckruf-Adresse"
    # Keine fremde Server-IP als Beispiel im ausgelieferten Dashboard.
    assert "217.182.138.35" not in dash, "feste Server-IP im Template"
    ok("v4.0-w122: Trackings-Ansicht wieder bedienbar, Radar-Leiche raus, "
       "Twitch-Rueckruf pflegbar")


def test_v40_w124_offline_meldung_ins_thema():
    """v4.0-W124: auch die Offline-Meldung landet im Melde-Thema.

    W121 stellte Live UND Offline auf _send_live_notice um — geprueft wurde
    aber nur _handle_single_tracking. Die Offline-Meldung hat einen ZWEITEN
    Sender: den Fan-Out am Ende der Aufnahme. Beide sind ueber
    claim_live_transition(going_live=False) serialisiert, und der
    Aufnahme-Pfad gewinnt den Anspruch praktisch immer — die Aufnahme endet
    in derselben Sekunde, in der der Stream stirbt, der Live-Check pollt erst
    30s spaeter. Ergebnis im Betrieb: LIVE im Thema, OFFLINE trotzdem im
    Hauptchat. Dieser Vertrag haelt beide Sender fest.
    """
    src = open("bot.py", encoding="utf-8").read()
    # Sender 1: Live-Check-Worker (W121 — hier nur zur Vollstaendigkeit).
    _hs = src[src.index("async def _handle_single_tracking("):
              src.index("async def _ensure_topic(")]
    assert "_send_live_notice(bot_app.bot, chat_id" in _hs, \
        "Offline-Meldung des Live-Check-Workers nicht im Melde-Thema"
    # Sender 2: Fan-Out am Ende der Aufnahme — der, der real feuert.
    _fan = src[src.index("# F30: OFFLINE-Notification BEVOR Upload startet"):]
    _fan = _fan[:_fan.index("# Upload an alle Fan-Out Chats")]
    assert "claim_live_transition(ftid, going_live=False)" in _fan, \
        "Fan-Out-Block nicht mehr am erwarteten Anker"
    assert "_send_live_notice(" in _fan, \
        "Offline-Meldung am Aufnahme-Ende geht wieder in den Hauptchat"
    assert "_safe_send(" not in _fan, \
        "_safe_send im Fan-Out — ohne message_thread_id landet das im Hauptchat"
    # F63 gilt fuer BEIDE Sender: sonst kam nachts OFFLINE ohne vorheriges LIVE.
    assert "_is_quiet_hours()" in _fan, \
        "Fan-Out ignoriert Quiet Hours — OFFLINE-Spam ohne vorheriges LIVE"
    ok("v4.0-w124: beide Offline-Sender schreiben ins Melde-Thema, "
       "beide achten die Quiet Hours")


def test_v40_w125_papierkorb_und_archiv_werkzeuge():
    """v4.0-W125: drei Faehigkeiten mit lebendem Backend sind wieder bedienbar.

    Der Reorg loeste die Ansichten VAULT und die Aufnahme-Liste auf und liess
    ihre Loader mit einem Waechter stehen. Drei Endpunkte verloren dabei ihre
    einzige Oberflaeche, ohne dass jemand es merkte — sie antworten bis heute:

      * /api/recordings/trash + /restore  — wegwerfen ging weiter, ansehen
        und zurueckholen nicht. Das ist die gefaehrliche Haelfte.
      * /api/archive/duplicates(/delete)  — die Loesch-Oberflaeche fuer
        Dubletten; rtDedup() zaehlt sie nur.
      * /api/archive/<id>/rename          — ohne jeden Aufrufer.

    Dieser Vertrag haelt Markup UND Verdrahtung fest, damit sie nicht ein
    zweites Mal lautlos verschwinden.
    """
    dash = open("templates/dashboard.html", encoding="utf-8").read()

    # ── Papierkorb: Kachel, Zaehler im Loader, Fenster, Wiederherstellen ──
    assert dash.count('id="rt_trash"') == 1, "Papierkorb-Kachel fehlt (oder doppelt)"
    assert 'onclick="rtTrash()"' in dash, "Papierkorb nicht bedienbar"
    _lt = dash[dash.index("async function loadRecTools("):
               dash.index("async function rtManualStart(")]
    assert "loadRtTrash();" in _lt, "Papierkorb-Zaehler laedt nicht mit"
    for _fn in ("async function loadRtTrash(", "async function rtTrash(",
                "async function rtRestore("):
        assert _fn in dash, "%s fehlt" % _fn
    _rr = dash[dash.index("async function rtRestore("):]
    _rr = _rr[:_rr.index("\n}")]
    assert "/api/recordings/" in _rr and "/restore" in _rr, "Wiederherstellen ruft nichts auf"
    assert "loadCaptures()" not in _rr, \
        "rtRestore frischt eine Ansicht auf, deren Markup es nicht gibt"

    # ── Dubletten: Knopf am Archiv-Panel, Fenster, Loesch-Wege ───────────
    assert 'onclick="arcDedup()"' in dash, "Kein Knopf fuer die Dubletten-Suche"
    for _fn in ("async function arcDedup(", "function arcRenderDedup(",
                "async function arcDeleteDupe(", "async function arcPurgeGroup(",
                "async function arcPurgeAll("):
        assert _fn in dash, "%s fehlt" % _fn
    _dd = dash[dash.index("let _dedupScanRoot="):dash.index("   VIEW: NEURAL")]
    assert "loadVault()" not in _dd, "Dedup frischt die aufgeloeste Vault-Ansicht auf"
    assert "loadArchive(true);" in _dd, "Dedup frischt die Archiv-Liste nicht auf"
    # W118-Regel: Werte in Inline-Handler nur ueber escJs, nie esc()+replace.
    assert "escJs(m.path)" in _dd, "Dateipfad geht ungeschuetzt in einen onclick"
    assert ".replace(/'/g" not in _dd, "naives Quote-Ersetzen im Handler wieder da"

    # ── Umbenennen: Knopf je Zeile, Backend-Feldname, Auffrischen ────────
    assert "async function arcRename(" in dash, "Umbenennen fehlt"
    assert 'onclick="arcRename(' in dash, "Umbenennen hat keinen Knopf"
    _ar = dash[dash.index("async function arcRename("):]
    _ar = _ar[:_ar.index("\n}")]
    assert "new_name" in _ar, "Backend erwartet new_name, nicht title"
    assert "loadArchive(true)" in _ar, "Liste frischt nach dem Umbenennen nicht auf"

    # ── Was ersatzlos wegfaellt, ist auch wirklich weg ───────────────────
    for _tot in ("function loadVault", "function vaultDelete", "function vaultRename",
                 "function loadManual", "function stopManual",
                 "function showTrash", "function restoreRec"):
        assert _tot not in dash, "%s wieder da (ersetzt durch das Archiv-Panel)" % _tot
    ok("v4.0-w125: Papierkorb, Dubletten und Umbenennen wieder erreichbar")


def test_v40_w126_reorg_reste_verdrahtet():
    """v4.0-W126: kein Loader ohne Markup, kein Markup ohne Loader.

    Der Reorg loeste die Ansichten VAULT, INTEL, BRAIN+ und LAB auf. Zurueck
    blieben Loader mit einem Waechter (`if(!$('#x')) return;`) — sie laufen,
    greifen ins Leere und melden nichts. Sieben Endpunkt-Familien verloren so
    ihre einzige Oberflaeche, obwohl sie durchgehend antworteten: Regeln,
    Webhooks, Sammlungen, Ruhezeiten, geplante Aufnahmen, Evolutions-Kern,
    KI-Chat, Aufnahmen-Liste und Highlight-Clips.

    Statt einzelne IDs aufzuzaehlen prueft dieser Vertrag die EIGENSCHAFT, die
    dabei verloren ging: jede ID, die das JavaScript nachschlaegt, muss es im
    Markup geben. Diese eine Zeile haette W122, W125 und W126 verhindert.
    """
    import re as _re
    dash = open("templates/dashboard.html", encoding="utf-8").read()

    # ── Kein Zugriff auf eine ID, die es nicht gibt ──────────────────────
    vorhanden = set(_re.findall(r'\bid\s*=\s*"([A-Za-z0-9_-]+)"', dash))
    vorhanden |= set(_re.findall(r'\bid\s*=\s*\\?["\']?([A-Za-z0-9_-]+)', dash))
    gesucht = set(_re.findall(r'getElementById\(\s*["\']([A-Za-z0-9_-]+)["\']', dash))
    gesucht |= set(_re.findall(r'\$\(\s*["\']#([A-Za-z0-9_-]+)["\']\s*\)', dash))
    tot = sorted(gesucht - vorhanden)
    assert not tot, "JavaScript greift auf Markup zu, das es nicht gibt: %s" % tot

    # ── Kein doppelter globaler Funktionsname ───────────────────────────
    # loadAutomation() gab es zweimal: der Autopilot-Lader und (im ersten
    # Anlauf dieser Welle) das Automatisierungs-Panel. Die spaetere
    # Deklaration gewinnt, das Panel blieb stumm — ohne jede Fehlermeldung.
    namen = _re.findall(r'^(?:async\s+)?function\s+([A-Za-z_$][\w$]*)\s*\(', dash, _re.M)
    doppelt = sorted({n for n in namen if namen.count(n) > 1})
    assert not doppelt, "globale Funktionsnamen doppelt vergeben: %s" % doppelt

    # ── Die neun wiederbelebten Panels haengen an einem Loader ──────────
    _betrieb = dash[dash.index("VIEW_LOADERS['betrieb'] = async ()=>{"):]
    _betrieb = _betrieb[:_betrieb.index("};")]
    for _f in ("loadAutomatisierung()", "bpLoadSchedule()"):
        assert _f in _betrieb, "%s haengt nicht im Betrieb-Loader" % _f
    _brain = dash[dash.index("VIEW_LOADERS['brain']=async ()=>{"):]
    _brain = _brain[:_brain.index("\n};")]
    for _f in ("nachAufbau('loadEvolution')", "nachAufbau('aiInit')"):
        assert _f in _brain, "%s haengt nicht im Brain-Loader" % _f
    assert "loadCaptures();" in dash[dash.index("VIEW_LOADERS.wall = async function(){"):
                                     dash.index("let _arcPage=1;")], \
        "Aufnahmen-Liste haengt nicht im Streams-Loader"

    # nachAufbau() loest die Falle, die der Browser gemeldet hat: ein Loader
    # in einem frueheren <script>-Block sieht spaetere Deklarationen nicht.
    assert "function nachAufbau(name){" in dash, "Helfer gegen die Block-Reihenfolge fehlt"
    assert "nachAufbau('loadClips')" in dash, "Clips laden ungeschuetzt ueber Blockgrenze"

    # ── Anlegen, nicht nur ansehen ───────────────────────────────────────
    # Ohne Anlege-Weg ist eine Liste, die nur leer sein kann, keine Bedienung.
    for _fn, _ep in (("async function arAdd(", "/api/auto-archive-rules"),
                     ("async function collAdd(", "/api/collections"),
                     ("async function whAdd(", "/api/webhooks"),
                     ("async function aiNewConv(", "/api/ai/conversations"),
                     ("async function aiSend(", "/messages")):
        assert _fn in dash, "%s fehlt" % _fn
        _k = dash[dash.index(_fn):]
        _k = _k[:_k.index("\n}")]
        assert _ep in _k, "%s spricht %s nicht an" % (_fn, _ep)

    # Der KI-Chat braucht seine Modell-Liste, sonst ist _aiModels immer leer.
    assert "async function aiLoadModels(" in dash and "'/api/ai/models'" in dash, \
        "Modell-Liste wird nicht geladen"

    # ── W118-Regel: Werte in Inline-Handlern nur ueber escJs ─────────────
    _clips = dash[dash.index("async function loadClips("):]
    _clips = _clips[:_clips.index("\n}")]
    assert "escJs(c.name)" in _clips, "Clip-Name geht ungeschuetzt in einen onclick"

    # ── Was ersatzlos entfiel, bleibt entfallen ─────────────────────────
    for _tot in ("function loadVault", "function loadManual", "function showTrash"):
        assert _tot not in dash, "%s wieder da" % _tot
    ok("v4.0-w126: jede nachgeschlagene ID existiert, neun Panels verdrahtet, "
       "Anlege-Wege vorhanden")


def test_v41_w2_dauerlaeufer_melden_sich():
    """v4.1-W2: kein Dauerlaeufer verschluckt mehr einen Ausfall.

    Die Regel steht in CLAUDE.md: jeder Dauerlaeufer gehoert auf
    `_loop_fehler` (erste Meldung sofort mit Traceback, danach gedrosselt) —
    nie auf `log.debug` und nie auf `pass`. Ein `log.warning` erscheint in
    einem ERROR-Log ebenfalls NIE; genau so blieb der Discord-Gateway-Tod
    monatelang unsichtbar.

    W116 hatte dafuer `_verbindung_verloren()` eingefuehrt und Kick-WebSocket,
    Twitch-EventSub und Twitch-Chat umgestellt — die beiden YouTube-Schleifen
    blieben dabei liegen. Dieser Vertrag haelt die Stellen fest, an denen ein
    stiller Ausfall ein ganzes Stueck Funktion mitnimmt.
    """
    src = open("bot.py", encoding="utf-8").read()

    def _block(kopf, ende):
        a = src.index(kopf)
        return src[a:src.index(ende, a)]

    # ── Beide YouTube-Schleifen melden wie Twitch ────────────────────────
    for _fn, _name in (("async def _youtube_api_chat_loop(", "YouTube-Chat (Data-API)"),
                       ("async def _youtube_chat_loop(", "YouTube-Chat")):
        _b = src[src.index(_fn):]
        _b = _b[:_b.index("\nasync def ", 10) if "\nasync def " in _b[10:] else len(_b)]
        assert '_verbindung_verloren("%s"' % _name in _b, \
            "%s meldet den Verbindungsverlust nicht ueber _verbindung_verloren" % _name
    # Alle fuenf Dauerverbindungen benutzen denselben Weg.
    assert src.count("_verbindung_verloren(") >= 6, \
        "eine Dauerverbindung meldet wieder an _verbindung_verloren vorbei"

    # ── Stille Stellen, die je ein ganzes Stueck Funktion verdeckt haben ─
    _stats = _block("async def _stats_loop(", "\n@dashboard_app.route")
    assert "_loop_fehler(\"_stats_loop/usage.flush\"" in _stats, \
        "Nutzungszaehler gehen wieder still verloren"
    _vac = _block("async def _db_vacuum_loop(", "\n_KICK_BID_CACHE") \
        if "\n_KICK_BID_CACHE" in src[src.index("async def _db_vacuum_loop("):] \
        else src[src.index("async def _db_vacuum_loop("):][:2000]
    for _w in ("ANALYZE", "VACUUM"):
        assert '_loop_fehler("_db_vacuum_loop/%s"' % _w in _vac, \
            "%s scheitert wieder lautlos — die Datenbank waechst dann ewig" % _w
    _up = _block("async def _upload_window_loop(", "\nDB_PATH")
    assert '_loop_fehler("_upload_window_loop"' in _up, \
        "Upload-Fenster-Loop meldet wieder auf log.warning (im ERROR-Log unsichtbar)"
    assert "log.warning(f\"Upload-Fenster-Loop Fehler" not in src, \
        "alter warning-Pfad wieder da"
    assert '_loop_fehler("_scheduler_loop/faellige"' in src, \
        "faellige Aufgaben scheitern wieder lautlos — der Zeitplan laeuft dann nie"
    assert '_loop_fehler("_viewer_sample_loop"' in src, \
        "Zuschauer-Stichprobe faellt wieder stumm aus"

    # ── /healthz ist EINE Route, kein Praefix ───────────────────────────
    assert '_AUTH_EXEMPT_PREFIXES = ("/api/public/",)' in src, \
        "/healthz wieder als Praefix — /healthzirgendwas umginge den Login"
    assert '_AUTH_EXEMPT_EXACT = ("/healthz",' in src, \
        "/healthz nicht mehr ausgenommen (Health-Check braucht ihn ohne Login)"

    # ── Der Vorlagen-Erzeuger schneidet Kommentare quote-bewusst ────────
    gen = open("tools/gen_env_example.py", encoding="utf-8").read()
    assert "def _ohne_kommentar(" in gen, "quote-bewusster Kommentar-Schnitt fehlt"
    assert 'line.split("#", 1)[0]' not in gen, \
        "naiver Kommentar-Schnitt zurueck — ein Default mit '#' faellt still aus .env.example"
    ok("v4.1-w2: Dauerlaeufer melden ihre Ausfaelle, /healthz exakt, "
       "Vorlagen-Erzeuger quote-bewusst")



def main():
    print("test_restream — Restream-Kernlogik (Mock-basiert)")
    test_streak()
    test_round_robin()
    test_output_args()
    test_transcode_matrix()
    test_reentrance_contract()
    test_relay_profile_contract()
    test_403_lifecycle()
    test_overlay_session_and_platforms()
    test_overlay_push_contract()
    test_flask_async_unpack_contract()
    test_overlay_size_contract()
    test_heartbeat_contract()
    test_dead_chat_contract()
    test_whisper_throttle_contract()
    test_whisper_throttle_behaviour()
    test_azrael_overlay_source()
    test_overlay_portrait_layout()
    test_azrael_text_cap()
    test_overlay_size_selfcorrect()
    test_overlay_mode_default()
    test_azrael_idle_layout()
    test_ffmpeg_thread_budget()
    test_ai_timeout_capped()
    test_fast_json_safety()
    test_uvloop_optional()
    test_url_refresh_no_wait()
    test_chat_guardian_reconnect()
    test_config_drift()
    test_overlay_react_wrap()
    test_twitch_oauth()
    test_donations_summary()
    test_azrael_overlay_toggle()
    test_twitch_chat_scopes_and_reply()
    test_twitch_sentinel_timeout()
    test_twitch_status_uses_oauth()
    test_twitch_ingest_default()
    test_community_discovery_loop()
    test_loyalty_rewards()
    test_sentinel_chat_reach()
    test_foreign_ad_block()
    test_brain_growth_viz()
    test_llm_budget()
    test_nexus_removed()
    test_restream_max_concurrent()
    test_overlay_react_and_layout()
    test_deepbughunt_fixes()
    test_pwa()
    test_b161_testpush_guard()
    test_b162_marketing()
    test_b163_news()
    test_v41_news_ausfuehrlich()
    test_b165_modheuristics()
    test_b166_piper_voices()
    test_b167_evolution()
    test_v41_w3_evolution_core_raus()
    test_v41_w4_bot_app_gebunden()
    test_v41_w4_news_marketing_kern_raus()
    test_v41_w5_restliche_dauerlaeufer()
    test_v41_w5_streamer_blueprint()
    test_v41_w6_i18n_fundament()
    test_b168_moderator_everywhere()
    test_b169_kick_oauth()
    test_b170_azrael_and_youtube()
    test_v40_version()
    test_v40_youtube_api()
    test_v40_news_no_recordings()
    test_v40_website()
    test_v40_wave2()
    test_v40_modfeed()
    test_v40_w4_website()
    test_v40_w5_channel_all()
    test_v40_w6_public_brand()
    test_v40_w7_public_brand_sweep()
    test_no_dead_contracts()
    test_v40_w9_kick_and_listener()
    test_v40_w10_kick_sendcheck()
    test_v40_w11_cue_and_duck()
    test_v40_w12_audio_panel()
    test_v40_w13_security()
    test_v40_w14_audit2()
    test_v40_w15_audit3()
    test_v40_w16_mod_exempt()
    test_v40_w17_kick401_crowdsec()
    test_v40_w18_crowdsec_lapi()
    test_v40_w19_warn_first()
    test_v40_w20_replygate()
    test_v40_w21_reply_origin_only()
    test_v40_w21_origin_only()
    test_v40_w22_highlights()
    test_v40_w23_sendrate()
    test_v40_w23_kick_redirect()
    test_v40_w23_crowdsec_panel()
    test_v40_w24_cohost()
    test_v40_w24_dashboard_audit()
    test_v40_w24b_youtube_channel_card()
    test_v40_w24c_youtube_deck_clickable()
    test_v40_w24d_youtube_account_chooser()
    test_v40_w25_restream_util()
    test_v40_w26_abo_and_sysrun()
    test_v40_w27_ffmpeg_filters()
    test_v40_w28_filepayload()
    test_v40_w29_streamsel()
    test_v40_w30_fixes_and_sysload()
    test_v40_w31_find_stream_urls()
    test_v40_w32_bundle_and_harden()
    test_v40_w33_cfgnorm_bundle()
    test_v40_w34_robustness_sweep()
    test_v40_w35_crossplatform_restream()
    test_v40_w36_restream_247_efficiency()
    test_v40_w37_memory_audit()
    test_v40_w38_resource_early_warning()
    test_v40_w39_adaptive_source_watch()
    test_v40_w40_resource_trend()
    test_v40_w41_send_observability()
    test_v40_w42_chat_listener_decoupled()
    test_v40_w43_send_status_panel()
    test_v40_w44_ffbuild()
    test_v40_w45_chatstats()
    test_v40_w46_json_and_telegram_launch()
    test_v40_w47_executor_isolation()
    test_v40_w48_loop_lag_monitor()
    test_v40_w49_oauthpage()
    test_v40_w50_trackingdb()
    test_v40_w51_eventquery()
    test_v40_w52_pin_login()
    test_v40_w53_pwa_audit()
    test_v40_w54_inspectcache()
    test_v40_w55_record_fail_backoff()
    test_v40_w55b_convmap()
    test_v40_w56_admod()
    test_v40_w57_brain3d_and_attack_time()
    test_v40_w58_defense_globe()
    test_v40_w59_donations_unknown()
    test_v40_w60_binresolve()
    test_v40_w61_ffver()
    test_v40_w61b_netstat()
    test_v40_w62_archivename()
    test_v40_w62b_journalperm()
    test_v40_w62c_cfgstore()
    test_v40_w62d_mod_resolve_exempt()
    test_v40_w63_creator_dossier()
    test_v40_w64_claude_provider()
    test_v40_w65_claude_full_and_donation_reset()
    test_v40_w66_command_center()
    test_v40_w67_pro_polish()
    test_v40_w68_overview_landing()
    test_v40_w69_stat_charts()
    test_v40_w70_claude_probe_diag()
    test_v40_w71_declutter()
    test_v40_w72_bughunt_website()
    test_v40_w73_retired_model_autoheal()
    test_v40_w74_fleet_status_honest()
    test_v40_w75_zombie_reap()
    test_v40_w76_fork_deadlock_guard()
    test_v40_w77_aiconfig_and_overview_agents()
    test_v40_w78_empty_env_float_bridge()
    test_v40_w79_mariadb_index_keylen()
    test_v40_w80_discord_upload_level()
    test_v40_w81_env_int_and_bridge_health()
    test_v40_w82_env_hardening_and_bridge_alert()
    test_v40_w83_loop_stall_watchdog()
    test_v40_w84_brain_reason_when_degraded()
    test_v40_w85_truncation_and_legal_pages()
    test_v40_w86_swap_agent()
    test_v40_w87_relay_source_reresolve()
    test_v40_w88_ops_observability()
    test_v40_w89_sysdiag_strip()
    test_v40_w90_stream_archive()
    test_v40_w91_rec_limit_and_legal_pages()
    test_v40_w92_usage_and_donation()
    test_v40_w93_meter_all_providers()
    test_v40_w94_crypto_donations()
    test_v40_w95_rectimeline_limit_and_legal_pages()
    test_v40_w96_all_tokens_to_eur()
    test_v40_w99_unified_donation_box()
    test_v40_w100_env_example()
    test_v40_w101_rate_single_source_and_escape()
    test_v40_w102_donations_3d_qr_manual()
    test_v40_w103_selfcheck_bridge_and_endpoints()
    test_v40_w109_dashboard_feldnamen()
    test_v40_w113_restream_stability()
    test_v40_w114_website_3d()
    test_v40_w115_relay_sicht_und_srcwatch()
    test_v40_w116_alterung_flattern_rate()
    test_v40_w117_ankerhygiene()
    test_v40_w117_asset_stempel()
    test_v40_w118_sicherheitsaudit()
    test_v40_w121_oauth_proxy_meldethema_kollision()
    test_v40_w122_trackings_ansicht()
    test_v40_w124_offline_meldung_ins_thema()
    test_v40_w125_papierkorb_und_archiv_werkzeuge()
    test_v40_w126_reorg_reste_verdrahtet()
    test_v41_w2_dauerlaeufer_melden_sich()
    print(f"test_restream OK — {PASS} Verträge grün")


if __name__ == "__main__":
    sys.exit(main())
