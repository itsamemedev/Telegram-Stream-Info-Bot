"""nc.persona — AZRAEL-Persona-Heuristiken (rein).

Extrahiert aus bot_v37.py: Intensitäts-Hinweis fürs LLM-Prompt, Emotions-
Klassifikation für Reaktionen, Lernparameter-Anpassung."""

import json
from datetime import datetime, timezone

def _persona_intensity_hint(level):
    """Ton-Modus für die AZRAEL-Persona (cfg.intensity). Verändert NUR den Tonfall,
       nicht die Safety-Rails/Identität. 0=sanft, 1=normal (unverändert), 2=streng."""
    try:
        level = int(level)
    except Exception:
        level = 1
    if level <= 0:
        return (" Ton-Modus SANFT: besonders ruhig, geduldig und sehr freundlich; deeskaliere "
                "maximal, kein Sarkasmus, gib viel Nachsicht.")
    if level >= 2:
        return (" Ton-Modus STRENG: direkter und knapper, klare Ansage bei Regelverstößen — "
                "aber weiterhin respektvoll, jugendfrei und ohne jede Beleidigung.")
    return ""

def _azrael_emotion(text):
    """Leichte Emotions-Heuristik aus dem Reaktionstext — treibt den reaktiven Avatar."""
    t = (text or "").lower()
    if any(w in t for w in ("haha", "lol", "genial", "wow", "stark", "nice", "feier", "hype", "!!!", "🔥", "😂")):
        return "hype"
    if any(w in t for w in ("unfair", "wütend", "schlimm", "inakzeptabel", "frech", "respektlos", "aufhören", "stopp")):
        return "angry"
    if any(w in t for w in ("schade", "traurig", "leider", "mitgefühl", "tut mir leid")):
        return "sad"
    if any(w in t for w in ("wirklich?", "fraglich", "zweifel", "sicher?", "hmm", "angeblich", "skeptisch")):
        return "skeptical"
    if any(w in t for w in ("willkommen", "freut mich", "schön", "danke", "super", "toll")):
        return "happy"
    return "neutral"

def _learn_param(conn, key, value, confidence, samples, category):
    """Upsert eines gelernten Parameters (backend-agnostisch)."""
    payload = json.dumps(value, ensure_ascii=False)
    now = datetime.now(timezone.utc).isoformat()
    cur = conn.execute(
        "UPDATE learned_params SET v=?, confidence=?, samples=?, category=?, updated_at=? "
        "WHERE k=?", (payload, float(confidence), int(samples), category, now, key))
    if getattr(cur, "rowcount", 0) in (0, -1):
        if not conn.execute("SELECT 1 FROM learned_params WHERE k=?", (key,)).fetchone():
            conn.execute("INSERT INTO learned_params (k, v, confidence, samples, category, updated_at) "
                         "VALUES (?,?,?,?,?,?)",
                         (key, payload, float(confidence), int(samples), category, now))
