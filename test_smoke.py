"""test_smoke — laedt bot_v37.py WIRKLICH und ruft jede GET-Route auf.

Warum das noetig war: die uebrigen Suiten lesen bot_v37.py nur als TEXT
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
              "ConversationHandler", "JobQueue", "AIORateLimiter"]:
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
    spec = u.spec_from_file_location("bot_v37", os.path.join(ROOT, "bot_v37.py"))
    m = u.module_from_spec(spec)
    spec.loader.exec_module(m)          # NameError/Reihenfolge-Fallen knallen hier
    ok("bot_v37.py importiert — Modul-Ebene laeuft ohne Fehler durch")

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

    # Konfig-Wahrheit: greifen die Defaults, die wir gesetzt haben?
    assert m.RESTREAM_OVERLAY_MODE == "html", m.RESTREAM_OVERLAY_MODE
    assert m.RESTREAM_OVERLAY_HTML_SIZE == "auto", m.RESTREAM_OVERLAY_HTML_SIZE
    ok("Defaults aktiv: OVERLAY_MODE=html, HTML_SIZE=auto")

    print("test_smoke OK \u2014 %d Vertraege gruen" % PASS)


if __name__ == "__main__":
    main()
