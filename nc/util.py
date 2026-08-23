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
