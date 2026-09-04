"""test_smoke — laedt bot.py WIRKLICH und ruft jede GET-Route auf.

Warum das noetig war: die uebrigen Suiten lesen bot.py nur als TEXT
(Regex/AST). Ob die Datei ueberhaupt importierbar ist, ob die Modul-Ebene ohne
NameError durchlaeuft, ob alle 268 Routen registriert werden und ob sie beim
Aufruf nicht in einen 500er laufen — das hat vorher NICHTS geprueft. Genau
solche Fehler (z.B. jsonify(ok=…, **rep) mit doppeltem Keyword) sind statisch
unsichtbar und knallen erst zur Laufzeit.

Fremdpakete (TikTokLive, python-telegram-bot) werden gestubbt: geprueft werden
soll die MODUL-LOGIK, nicht ob die Libs installiert sind.

Erwartet werden zwei 503er auf /api/channels/status und /api/kick/channel —
die brauchen einen laufenden Event-Loop, den es im Testharnisch nicht gibt.
Der Code liefert dort planmaessig {"transient": true}; das IST das korrekte
Verhalten und wird hier festgehalten.
"""
import os
import sys
import tempfile
import time
import types

ROOT = os.path.dirname(os.path.abspath(__file__))
EXPECT_TRANSIENT = {"/api/channels/status", "/api/kick/channel"}
PASS = 0


def ok(msg):
    global PASS
    PASS += 1
    print("  \u2713 " + msg)


class _AnyMeta(type):
    """Auch KLASSEN-Attribute muessen gehen: ContextTypes.DEFAULT_TYPE etc."""

    def __getattr__(cls, n):
        return _Any


class _Any(metaclass=_AnyMeta):
    def __init__(self, *a, **k):
        pass

    def __getattr__(self, n):
        return _Any()

    def __call__(self, *a, **k):
        return _Any()

    def __iter__(self):
        return iter(())


def _stub(name):
    m = types.ModuleType(name)
    m.__path__ = []
    sys.modules[name] = m
    return m


def _install_stubs():
    for n in ["TikTokLive", "TikTokLive.client", "TikTokLive.client.errors",
              "TikTokLive.events", "TikTokLive.client.web",
              "TikTokLive.client.web.web_settings", "TikTokLive.proto"]:
        _stub(n)
    sys.modules["TikTokLive"].TikTokLiveClient = _Any
    sys.modules["TikTokLive.client.web.web_settings"].WebDefaults = _Any()
    for e in ["CommentEvent", "GiftEvent", "ConnectEvent", "DisconnectEvent",
              "FollowEvent", "ShareEvent", "LikeEvent", "JoinEvent",
              "LiveEndEvent", "RoomUserSeqEvent", "SubscribeEvent"]:
        setattr(sys.modules["TikTokLive.events"], e, type(e, (), {}))
    for e in ["UserOfflineError", "UserNotFoundError", "AgeRestrictedError",
              "SignAPIError", "WebcastBlocked200Error", "InitialCursorMissing",
              "SignatureRateLimitError"]:
        setattr(sys.modules["TikTokLive.client.errors"], e,
                type(e, (Exception,), {}))

    for n in ["telegram", "telegram.ext", "telegram.constants", "telegram.error",
              "telegram.request"]:
        _stub(n)
    for c in ["Update", "InlineKeyboardButton", "InlineKeyboardMarkup", "Bot",
              "InputFile", "InputMediaPhoto", "InputMediaVideo", "BotCommand",
              "ReplyKeyboardMarkup", "KeyboardButton"]:
        setattr(sys.modules["telegram"], c,
                type(c, (), {"__init__": lambda self, *a, **k: None}))
    for c in ["Application", "ApplicationBuilder", "CommandHandler",
              "MessageHandler", "filters", "ContextTypes", "CallbackQueryHandler",
              "ConversationHandler", "JobQueue", "AIORateLimiter",
              # v4.1-W7: setzt die Sprache des Absenders, bevor ein Handler laeuft
              "TypeHandler"]:
        setattr(sys.modules["telegram.ext"], c, _Any)
    sys.modules["telegram.constants"].ParseMode = type(
        "ParseMode", (), {"HTML": "HTML", "MARKDOWN": "Markdown",
                          "MARKDOWN_V2": "MarkdownV2"})
    sys.modules["telegram.constants"].ChatAction = type(
        "ChatAction", (), {"TYPING": "typing", "UPLOAD_VIDEO": "upload_video"})
    for e in ["TelegramError", "BadRequest", "TimedOut", "NetworkError",
              "RetryAfter", "Forbidden", "Conflict", "InvalidToken"]:
        setattr(sys.modules["telegram.error"], e, type(e, (Exception,), {}))
    sys.modules["telegram.request"].HTTPXRequest = _Any


def main():
    os.chdir(tempfile.mkdtemp())
    sys.path.insert(0, ROOT)
    os.environ.update(TELEGRAM_TOKEN="x", TELEGRAM_CHAT_ID="1",
                      DASHBOARD_PORT="0", LIVE_REACT_ENABLED="0",
                      DB_BACKEND="sqlite")
    _install_stubs()

    import importlib.util as u
    spec = u.spec_from_file_location("bot", os.path.join(ROOT, "bot.py"))
    m = u.module_from_spec(spec)
    spec.loader.exec_module(m)          # NameError/Reihenfolge-Fallen knallen hier
    ok("bot.py importiert — Modul-Ebene laeuft ohne Fehler durch")

    # v4.1-W31: discord.py ist im Code OPTIONAL (`except Exception: discord =
    # None`). Fehlt das Paket, laeuft dieser Test bis zum Ende gruen — und hat
    # dabei die gesamte Slash-Command-Registrierung nie angefasst. Genau dort
    # sass B79: eine Annotation `member: discord.Member` wird von discord.py
    # ueber callback.__globals__ aufgeloest, ein fehlender Modul-Import liess
    # den ganzen Discord-Bot beim Registrieren crashen. Ein Rauchtest, der das
    # stillschweigend ueberspringt, ist ein Rauchtest ohne Rauch.
    assert m.discord is not None, (
        "discord.py ist nicht installiert — dieser Test wuerde die "
        "Discord-Pfade ueberspringen und trotzdem gruen melden. "
        "pip install -r requirements-smoke.txt")
    ok("discord.py geladen — die Slash-Command-Pfade sind wirklich mit drin")

    rules = list(m.dashboard_app.url_map.iter_rules())
    assert len(rules) > 200, "nur %d Routen registriert?" % len(rules)
    ok("Flask: %d Routen registriert" % len(rules))

    m.init_db()
    ok("init_db(): Schema angelegt (alle 42 Tabellen, SQLite-Dialekt)")

    client = m.dashboard_app.test_client()
    crashes, called, skipped, transient = [], 0, 0, []
    for r in sorted(rules, key=lambda x: str(x.rule)):
        if "GET" not in r.methods:
            continue
        path = str(r.rule)
        if r.arguments or path.startswith("/static"):
            skipped += 1
            continue
        called += 1
        try:
            resp = client.get(path)
        except Exception as e:
            crashes.append((path, "EXC", "%s: %s" % (type(e).__name__, e)))
            continue
        if resp.status_code < 500:
            continue
        body = resp.get_data(as_text=True)[:140].replace("\n", " ")
        if resp.status_code == 503 and path in EXPECT_TRANSIENT:
            assert '"transient": true' in body or '"transient":true' in body, \
                "%s: 503 ohne transient-Flag" % path
            transient.append(path)
            continue
        crashes.append((path, resp.status_code, body))

    if crashes:
        print("\n  HTTP 5xx / Exception:")
        for p, c, b in crashes:
            print("    [%s] %s\n        %s" % (c, p, b))
        raise AssertionError("%d Route(n) mit 5xx" % len(crashes))

    ok("Route-Smoke: %d GET-Routen aufgerufen, 0 unerwartete 5xx "
       "(%d mit Parametern uebersprungen)" % (called, skipped))
    assert set(transient) == EXPECT_TRANSIENT, \
        "erwartete transient-503er: %s, bekommen: %s" % (EXPECT_TRANSIENT, transient)
    ok("die 2 erwarteten 503er liefern korrekt transient=true (kein Event-Loop)")

    # Die in dieser Session gebauten Routen muessen da sein
    paths = {str(r.rule) for r in rules}
    for want in ("/api/db/export", "/api/db/import", "/api/db/summary",
                 "/api/channels/status", "/api/system/resilience"):
        assert want in paths, "Route fehlt: %s" % want
    ok("neue Routen registriert (db/export, db/import, db/summary, channels/status)")

    # v4.0-W105 (Tiefenbughunt): das Audit-Log MUSS jeden Schreibzugriff
    # protokollieren. Vorher tat es das nie: after_request feuerte den Eintrag
    # per _spawn(asyncio.to_thread(...)) ab, was asyncio.create_task() nutzt und
    # damit einen laufenden Loop IM Flask-Thread verlangt — den es dort nie
    # gibt. Der RuntimeError landete im umgebenden `except: pass`, die Coroutine
    # blieb unerwartet liegen, und audit_log blieb bei jedem POST/PUT/DELETE
    # leer. Genau das haelt dieser Vertrag fest: ein Verhaltenstest, kein
    # Quelltext-Anker, weil nur das Verhalten zaehlt.
    def _audit_rows():
        with m.db_conn() as _c:
            return _c.execute("SELECT COUNT(*) AS n FROM audit_log").fetchone()["n"]

    _before = _audit_rows()
    client.post("/api/automation/toggle", json={"enabled": True})
    client.delete("/api/annotations/999999")
    for _ in range(50):                      # der Schreibvorgang laeuft nebenlaeufig
        if _audit_rows() >= _before + 2:
            break
        time.sleep(0.1)
    _after = _audit_rows()
    assert _after >= _before + 2, (
        "Audit-Log schreibt nicht: %d Eintraege nach 2 Schreibzugriffen "
        "(erwartet >= %d). Regression von v4.0-W105." % (_after, _before + 2))
    ok("Audit-Log protokolliert Schreibzugriffe (W105: kein create_task im Flask-Thread)")

    # v4.0-W117: die Tracking-Zugriffe liegen in nc/trackingdb.py, das
    # Aufraeumen des Recorder-Zustands beim Entpausen macht ein Rueckruf im Bot
    # (B54). Faellt der Rueckruf weg, laeuft alles weiter — und das Tracking
    # pausiert sich beim naechsten stall_killed-Streak sofort wieder. Statisch
    # unsichtbar, deshalb hier als Rundlauf.
    from nc import trackingdb as _TD
    _r = m.bulk_add_trackings(1, ["alice", "bob", "alice"], added_by=7)
    assert _r["added"] == ["alice", "bob"] and _r["duplicates"] == ["alice"], _r
    _tid = [x["id"] for x in m.get_all_active_trackings(include_paused=True)
            if x["username"] == "alice"][0]
    for _d in (m._STREAM_DEAD_STREAK, m._STREAM_DEAD_BACKOFF_UNTIL,
               m._PENDING_OFFLINE_COUNT, m._PENDING_OFFLINE_SINCE,
               m._EARLY_DISCONNECT_RETRY):
        _d[_tid] = 1
    assert m.set_tracking_paused(_tid, True) is True
    assert len(m.get_all_active_trackings()) == 1, "pausiertes Tracking noch aktiv"
    assert m.set_tracking_paused(_tid, False) is True
    assert len(m.get_all_active_trackings()) == 2, "entpaustes Tracking fehlt"
    for _n in ("_STREAM_DEAD_STREAK", "_STREAM_DEAD_BACKOFF_UNTIL",
               "_PENDING_OFFLINE_COUNT", "_PENDING_OFFLINE_SINCE",
               "_EARLY_DISCONNECT_RETRY"):
        assert _tid not in getattr(m, _n), \
            "%s beim Resume nicht geraeumt — on_resume-Rueckruf nicht verdrahtet (B54)" % _n
    assert m.set_tracking_paused(999999, True) is False, "unbekannte id muss False geben"
    assert _TD.add_tracking_tag(_tid, "vip") is True
    assert _TD.add_tracking_tag(_tid, "vip") is False, "Dublette muss False geben"
    assert _TD.get_tags_for_tracking(_tid) == ["vip"]
    assert _TD.set_tracking_priority(_tid, 2) is True
    assert m.get_priority_poll_interval(_tid, 60) == 10, "VIP-Intervall greift nicht"
    ok("W117: Tracking-Zugriffe delegiert, Resume raeumt den Worker-Zustand auf")

    # v4.0-W117: der TikTok-Status-Zaehler wird als REFERENZ nach nc/stats.py
    # gereicht. Bei einer Kopie zaehlte der Scraper ins Leere und die Verteilung
    # staende ewig auf 0 — auch das sieht man nur im Lauf.
    m.record_tiktok_status(200)
    m.record_tiktok_status(200)
    m.record_tiktok_status(404)
    _dist = m.get_tiktok_status_distribution()
    assert _dist["total"] == 3 and _dist["by_code"][0] == {"code": 200, "count": 2,
                                                          "pct": 66.7}, _dist
    ok("W117: Status-Zaehler als Referenz geteilt (Scraper zaehlt, Auswertung sieht es)")

    # Konfig-Wahrheit: greifen die Defaults, die wir gesetzt haben?
    assert m.RESTREAM_OVERLAY_MODE == "html", m.RESTREAM_OVERLAY_MODE
    assert m.RESTREAM_OVERLAY_HTML_SIZE == "auto", m.RESTREAM_OVERLAY_HTML_SIZE
    ok("Defaults aktiv: OVERLAY_MODE=html, HTML_SIZE=auto")

    print("test_smoke OK \u2014 %d Vertraege gruen" % PASS)


if __name__ == "__main__":
    main()
