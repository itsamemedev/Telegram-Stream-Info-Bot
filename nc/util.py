"""nc.util — kleine reine Logik-Helfer (keine Bot-Abhängigkeiten).

Extrahiert aus bot.py: LLM-Fehlermeldungen, Vision-Modell-Heuristik,
Telegram-callback_data-Kappung, Topic-Key-Bau. Alle stdlib-only.
"""


def _ai_err_msg(kind, model):
    return {
        "model_missing": f"Modell '{model}' nicht installiert",
        "timeout":       "Ollama Timeout (keine Daten)",
        "unreachable":   "Ollama nicht erreichbar (Service läuft nicht?)",
        "http":          "Ollama HTTP-Fehler",
        "other":         "Unerwarteter Fehler",
    }.get(kind, "Keine Antwort vom LLM")


def _looks_like_vision_model(model_name: str) -> bool:
    """Heuristik: ist das ein Vision-fähiges Modell?"""
    n = (model_name or "").lower()
    return any(tag in n for tag in ("vision", "llava", "bakllava", "moondream", "minicpm-v"))


def _safe_callback_data(prefix: str, payload: str, max_total: int = 60) -> str:
    """Telegram callback_data ist auf 64 Bytes begrenzt. Wir kappen mit Reserve."""
    raw = f"{prefix}{payload}"
    return raw if len(raw.encode("utf-8")) <= max_total else raw.encode("utf-8")[:max_total].decode("utf-8", errors="ignore")


def _topic_key(chat_id, username) -> str:
    return f"{chat_id}:{str(username).lower()}"


def _webhook_event_match(events_csv, kind):
    """True wenn ein Webhook (events_csv) auf diesen event-kind hört.
       Leer/'*'/'all' = alle Events. Sonst exakter Match auf Komma-Liste."""
    if not events_csv:
        return True
    ev = events_csv.strip().lower()
    if ev in ("*", "all", ""):
        return True
    wanted = {x.strip().lower() for x in ev.split(",") if x.strip()}
    return (kind or "").lower() in wanted


def _loop_not_ready(e) -> bool:
    """B86: True wenn der Fehler das transiente 'Loop faehrt noch hoch'-Signal ist.
       Routes geben dann 503 statt 500 zurueck (kein Serverfehler-Push).

       v4.1-W4 aus bot.py geloest: siebzehn Routen im Monolithen und ab jetzt
       jedes Blueprint fragen dasselbe. Ein reines Praedikat ohne Bot-Bezug
       gehoert nicht in nc.ctx — dort ist der Platz knapp und begruendungs-
       pflichtig, hier kostet es nichts."""
    return isinstance(e, RuntimeError) and "event loop not ready" in str(e)


def datei_in(basis, name, endung=None):
    """Absoluter Pfad zu `name` UNTERHALB von `basis` — oder None.

    v4.1-W10 (CodeQL py/path-injection). Die Ausliefer-Routen prüften bisher
    mit `"/" in fn or "\\\\" in fn`. Das ist inhaltlich dicht, aber es ist eine
    Prüfung auf VERBOTENES statt eine Zusage über das Ergebnis: wer sie später
    lockert (ein Unterordner, ein Windows-Laufwerksbuchstabe, ein URL-dekodiertes
    Zeichen), verschiebt die Sicherheit, ohne sie anzufassen. Hier wird
    stattdessen der fertige Pfad aufgelöst und nachgewiesen, dass er in `basis`
    liegt — was auch Symlinks und `..` in jeder Schreibweise abdeckt.

    `endung` (z.B. ".mp4") wird zusätzlich erzwungen, damit eine Route für
    Videos keine Datenbank ausliefert.
    """
    import os
    if not name or not isinstance(name, str):
        return None
    if endung and not name.lower().endswith(endung.lower()):
        return None
    wurzel = os.path.realpath(os.path.abspath(basis))
    ziel = os.path.realpath(os.path.join(wurzel, name))
    # commonpath statt startswith: "/daten/clips2" faengt auch mit
    # "/daten/clips" an, liegt aber NICHT darin.
    try:
        if os.path.commonpath([wurzel, ziel]) != wurzel:
            return None
    except ValueError:
        return None                      # verschiedene Laufwerke (Windows)
    if ziel == wurzel:
        return None
    return ziel
