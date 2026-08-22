"""nc.confdrift — welche .env-Werte weichen vom Code-Default ab?

WARUM DAS EXISTIERT (drei echte Faelle, alle in einer Session):
  - RESTREAM_OVERLAY_HTML_SIZE: .env hatte eine feste Groesse, der Code-Default
    war "auto". Das Overlay wurde in falscher Aufloesung gerendert; die Suche
    danach hat mehrere Runden gekostet.
  - RESTREAM_MULTI_MODE: .env "independent", Code-Default "tee". Ergebnis: jedes
    Bild wurde ZWEIMAL encodiert — die halbe Encoder-CPU verschenkt.
  - LIVE_REACT_ENABLED: Code-Default 0, .env 1. Wer nur den Code liest, sagt das
    Falsche.

Das Muster: os.getenv("X", "default") kollabiert zur Laufzeit. Steht in der .env
etwas anderes, ist der Default unsichtbar — und niemand merkt, dass eine
Einstellung die Absicht des Codes aushebelt.

Der Trick hier: die Quelldatei zur Laufzeit selbst lesen und die Defaults per AST
zurueckgewinnen. Damit bleibt die Pruefung automatisch aktuell — es gibt keine
zweite Liste, die man pflegen (und vergessen) koennte.
"""
import ast
import logging
import os

log = logging.getLogger("TikTokBot")

# Schluessel, bei denen eine Abweichung das VERHALTEN oder die LAST spuerbar
# aendert. Drift ist hier nicht automatisch falsch — aber sie gehoert gesehen.
WATCHLIST = {
    "RESTREAM_MULTI_MODE": "tee = EIN Encode fuer alle Ziele; independent = ein "
                           "voller Encode + Pull PRO Ziel (doppelte CPU)",
    "RESTREAM_OVERLAY_MODE": "html = echtes Overlay; drawtext = Notnagel",
    "RESTREAM_OVERLAY_HTML_SIZE": "auto = Quellaufloesung uebernehmen; feste "
                                  "Werte koennen das Bild verzerren",
    "LIVE_REACT_ENABLED": "schaltet AZRAELs Live-Reaktion",
    "AI_TIMEOUT": "0 wird im Code zu 3600s — eine Stunde",
    "WHISPER_MAX_CONCURRENT": "jede Instanz kostet WHISPER_CPU_THREADS Kerne",
    "WHISPER_CPU_THREADS": "multipliziert sich mit WHISPER_MAX_CONCURRENT",
    "FFMPEG_THREADS_LIVE": "Threads fuers Sendebild",
    "FFMPEG_THREADS_BG": "Threads fuer Nachbearbeitung",
    "DB_BACKEND": "sqlite oder mariadb",
    "RESTREAM_BITRATE_K": "hoeher = mehr CPU",
    "RESTREAM_RELAY_BITRATE_K": "hoeher = mehr CPU",
    "CHECK_INTERVAL": "Basis-Pollintervall",
    "AI_PROVIDER": "brain = lokales llama.cpp (CPU!)",
}

# Diese Werte MUESSEN gesetzt werden — Drift ist dort normal und kein Hinweis.
IGNORE = {
    "TELEGRAM_TOKEN", "TELEGRAM_CHAT_ID", "KICK_CLIENT_ID", "KICK_CLIENT_SECRET",
    "KICK_CHANNEL_URL", "KICK_STREAM_KEY", "TWITCH_CLIENT_ID", "TWITCH_STREAM_KEY",
    "TWITCH_EVENTSUB_TOKEN", "YOUTUBE_STREAM_KEY", "MARIADB_PASSWORD",
    "MARIADB_USER", "MARIADB_HOST", "MARIADB_DB", "TIKTOK_SIGN_API_KEY",
    "DISCORD_TOKEN", "DISCORD_WEBHOOK", "OPENAI_API_KEY", "RECORD_PROXY",
    "PROXY_LIST", "COOKIE_FILE", "RECORDINGS_DIR", "ARCHIVE_DIR", "DB_PATH",
    "REDIS_URL", "BRAIN_LLAMACPP_URL",
}


def extract_defaults(source_path):
    """Alle Env-Keys + ihre Code-Defaults per AST aus der Quelle ziehen.

    Erfasst os.getenv("X", "d"), _env_int("X", n) und _env_int_range("X", n, ...).
    Regex waere hier zu grob: Defaults koennen Ausdruecke sein (z.B. berechnete
    Werte), die wir dann sauber als "dynamisch" markieren statt falsch zu raten.
    """
    try:
        with open(source_path, encoding="utf-8") as _sf:
            tree = ast.parse(_sf.read())
    except Exception as e:
        log.debug("confdrift: %s nicht lesbar: %s", source_path, e)
        return {}
    out = {}
    for n in ast.walk(tree):
        if not isinstance(n, ast.Call):
            continue
        fname = None
        if isinstance(n.func, ast.Attribute) and n.func.attr == "getenv":
            fname = "getenv"
        elif isinstance(n.func, ast.Name) and n.func.id in ("_env_int",
                                                            "_env_int_range"):
            fname = n.func.id
        if not fname or not n.args:
            continue
        key = n.args[0]
        if not (isinstance(key, ast.Constant) and isinstance(key.value, str)):
            continue
        if len(n.args) < 2:
            out.setdefault(key.value, None)          # kein Default = ""/None
            continue
        d = n.args[1]
        if isinstance(d, ast.Constant):
            out.setdefault(key.value, d.value)
        else:
            out.setdefault(key.value, "<dynamisch>")
    return out


def _norm(v):
    """Vergleichbar machen: "1" == 1, "TRUE" == "true"."""
    if v is None:
        return ""
    s = str(v).strip()
    return s.lower()


def config_drift(source_path, env=None, only_watchlist=False):
    """Vergleicht die gesetzte Umgebung mit den Code-Defaults.

    Gibt Eintraege zurueck, bei denen beides voneinander abweicht — plus die
    Info, ob der Schluessel auf der Watchlist steht (= Abweichung aendert
    Verhalten oder Last spuerbar).
    """
    env = env if env is not None else os.environ
    defaults = extract_defaults(source_path)
    rows = []
    for key, dflt in sorted(defaults.items()):
        if key in IGNORE or key not in env:
            continue
        if dflt == "<dynamisch>":
            continue                     # Default nicht statisch bestimmbar
        cur = env.get(key)
        if _norm(cur) == _norm(dflt):
            continue
        watched = key in WATCHLIST
        if only_watchlist and not watched:
            continue
        rows.append({
            "key": key,
            "code_default": "" if dflt is None else str(dflt),
            "env_value": str(cur),
            "watched": watched,
            "why": WATCHLIST.get(key, ""),
        })
    rows.sort(key=lambda r: (not r["watched"], r["key"]))
    return {
        "total_env_keys": len(defaults),
        "drift_count": len(rows),
        "watched_drift": sum(1 for r in rows if r["watched"]),
        "entries": rows,
    }


def log_watchlist_drift(source_path, env=None):
    """Beim Start EINMAL die verhaltensrelevanten Abweichungen loggen.

    Absichtlich nur die Watchlist: eine Wand aus 57 harmlosen Abweichungen liest
    niemand, und was niemand liest, warnt nicht.
    """
    try:
        rep = config_drift(source_path, env=env, only_watchlist=True)
    except Exception as e:
        log.debug("confdrift: %s", e)
        return 0
    for r in rep["entries"]:
        log.info("CONFIG-DRIFT: %s = %r (Code-Default: %r) — %s",
                 r["key"], r["env_value"], r["code_default"], r["why"])
    if rep["entries"]:
        log.info("CONFIG-DRIFT: %d verhaltensrelevante Abweichung(en). Das ist "
                 "nicht automatisch falsch — aber es ist der Grund, warum eine "
                 "Einstellung anders wirkt als der Code vermuten laesst.",
                 len(rep["entries"]))
    return len(rep["entries"])
