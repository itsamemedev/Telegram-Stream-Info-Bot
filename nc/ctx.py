"""nc.ctx — der Laufzeitkontext, den herausgelöste Route-Module brauchen.

Warum es das gibt: die Blueprints in nc/routes/ brauchen eine Handvoll Helfer,
die im Monolithen leben und dort auch bleiben — weil sie am Bot-Loop, am
Recorder-Kern oder an geteiltem Zustand hängen. Sie einzeln durch zwanzig
configure()-Parameter zu reichen erzeugt genau die Signatur-Drift, an der die
Restream-Verträge schon dreimal gekippt sind. Ein Objekt, einmal gefüllt, ist
die kleinere Angriffsfläche.

**Es ist KEIN Sammelbecken.** Was nur eine Route braucht, gehört in ihr
Blueprint, nicht hierher. `__slots__` ist die Bremse: ein neues Feld ist eine
bewusste Entscheidung und fällt im Diff auf. Wer hier etwas einträgt, muss
zeigen können, dass es mehr als ein Blueprint benutzt.

Die Architektur-Grenze bleibt: kein Import aus bot.py. Der Bot füllt den
Kontext einmal beim Start, danach wird nur gelesen.
"""


class Ctx:
    """Reiner Namensraum. Kein Verhalten, damit nichts hier drin versteckt wird."""

    __slots__ = (
        # --- Querschnitt: von mehreren Blueprints gebraucht ---
        "log",                      # der Logger des Bots
        "log_event",                # Ereignisprotokoll (event_log + Webhooks)
        "arg_int",                  # geprüfter Query-Parameter
        "run_async",                # Coroutine auf dem Bot-Loop, blockierend
        "cfg",                      # Konfigurationswerte, siehe unten
        # --- Aufnahme-Domäne ---
        "recordings_dir",
        "ffmpeg_threads_bg",
        "ffmpeg_nice_bg",
        "proc_is_recorder",         # PID gehört zu einem Recorder?
        "scraper_session",          # geteilte HTTP-Session des Scrapers
        "trigger_manual_recording",  # haengt am Recorder-Kern, bleibt im Bot
        "stop_manual_recording",    # teilt _MANUAL_RECORDINGS mit trigger_
        "get_tags_for_tracking",
        # --- Archiv-Domäne (W107) ---
        "intel_ensure_schema",
        "intel_index_one",
        "intel_semantic",
        "intel_ps",                 # laufende Index-Prozesse, geteilter Zustand
        # --- Auswertung und Webhooks (W108) ---
        "latest_popularity",
        "post_json_threaded",       # feuert Webhooks im eigenen Thread ab
        # --- Systemzustand (W110) ---
        # Bewusst ein GETTER, kein Wert: _BOT_START_TIME ist beim Import noch
        # None und wird erst in main() gesetzt. Ein beim Start uebergebener Wert
        # waere fuer immer None, und die Uptime staende ewig auf 0.
        "get_bot_start_time",
        "get_cookie_health",
        "get_storage_stats",
        # Ebenfalls ein GETTER (W116): _MAIN_LOOP wird erst in run_bot() gesetzt.
        # Im Monolithen stand dafuer globals().get("_MAIN_LOOP") — in einem
        # Blueprint waere das still None, weil globals() dort der Modul-
        # Namensraum des Blueprints ist. Genau die Sorte stiller Fehlanzeige,
        # vor der CLAUDE.md warnt: der Healthcheck haette "event_loop: false"
        # gemeldet, obwohl der Loop laeuft.
        "get_main_loop",
        # --- KI-Pfade (W112). Bleiben im Bot: llm_chat_sync geht ueber
        # brain/freeai und haengt am Provider-Zustand, _check_ai_models_sync
        # an dessen Modell-Cache.
        "llm_chat_sync",
        "check_ai_models_sync",
    )


# Warum cfg ein Dict ist und keine zwoelf weiteren Slots: die Blueprints
# brauchen .env-abgeleitete Werte (ARCHIVE_DIR, AI_TIMEOUT, …). Als Einzelfelder
# waere nc/ctx.py nach drei Wellen ein Konfigurations-Abladeplatz — genau das
# Sammelbecken, das dieses Modul verhindern soll. Ein Dict haelt die Grenze
# zwischen "Helfer, die der Monolith stellt" (Slots, einzeln begruendet) und
# "Werte, die aus der .env kommen" (cfg) sichtbar.
#
# Die Werte werden beim Start uebergeben, nicht gelesen: der Bot friert sie
# ohnehin schon beim Import ein, und ein zweiter Lesepfad waere eine stille
# Verhaltensaenderung gegenueber dem Monolithen.
_CTX = None


def configure(**kw):
    """Vom Bot genau einmal beim Start gerufen.

    Unbekannte Namen fliegen sofort auf (AttributeError durch __slots__) statt
    still ins Leere zu laufen — ein vertippter Schlüssel wäre sonst ein Helfer,
    der zur Laufzeit None ist und erst beim ersten Aufruf knallt.
    """
    global _CTX
    c = Ctx()
    for k, v in kw.items():
        setattr(c, k, v)
    _CTX = c
    return c


def get():
    """Der gefüllte Kontext.

    Wirft laut, wenn configure() fehlt. Ein stiller None-Kontext waere genau
    der Fehler aus CLAUDE.md — eine Ebene hoeher: die Route liefe, taete aber
    nichts, und niemand saehe warum.
    """
    if _CTX is None:
        raise RuntimeError(
            "nc.ctx ist nicht konfiguriert — nc.ctx.configure(...) fehlt im Startpfad "
            "von bot.py")
    return _CTX


def is_configured():
    """Fuer Tests und Diagnose — fragt, ohne zu werfen."""
    return _CTX is not None
