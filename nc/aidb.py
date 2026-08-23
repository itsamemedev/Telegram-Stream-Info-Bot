"""nc.aidb — der Datenzugriff der KI-Domaene, aus bot_v37 geloest.

v4.0-W112, Vorarbeit fuer das /api/ai-Blueprint: beides ist reiner
DB-Zugriff (Tabellen ai_log und ai_messages) und waere im Laufzeitkontext zu
zwei Eintraegen geworden, obwohl kein zweites Blueprint sie braucht. Gebaut
wie nc/recdb.py.

Abgrenzung: die CONVERSATIONS-Tabelle selbst wird weiterhin von nc.notes
bedient (_conv_list liegt dort seit laenger). Hier liegen die NACHRICHTEN
einer Konversation und das Aufruf-Protokoll.

Verbatim uebernommen — inklusive der Kappungen auf 8.000/16.000 Zeichen, die
die Tabelle schlank halten, und des best-effort-except: ein fehlgeschlagener
Protokolleintrag darf einen KI-Aufruf nie scheitern lassen.
"""

import logging
from datetime import datetime, timezone

from nc.dbwrap import db_conn
from nc import convmap as _nc_convmap

_log = logging.getLogger("TikTokBot")


def add_log_entry(chat_id, user_id, prompt, response, model, duration_ms,
                     error=None, file_kind=None, file_size=None):
    """F16: ein AI-Call wird ins persistente Log geschrieben.
       F49: gibt die DB-id zurück (für /api/ai/ask response) oder None bei Fehler."""
    try:
        with db_conn() as conn:
            cur = conn.execute(
                "INSERT INTO ai_log (chat_id, user_id, prompt, response, model, "
                "duration_ms, error, file_kind, file_size, created_at) "
                "VALUES (?,?,?,?,?,?,?,?,?,?)",
                (int(chat_id), int(user_id),
                 (prompt or "")[:8000],     # cap to keep DB lean
                 (response or "")[:16000] if response else None,
                 model, duration_ms, error, file_kind, file_size,
                 datetime.now(timezone.utc).isoformat()))
            conn.commit()
            return cur.lastrowid
    except Exception as e:
        _log.warning(f"add_ai_log_entry failed: {e}")
        return None


def conv_messages(conv_id):
    """Alle Messages einer Conversation, chronologisch.
       v4.0-W55b: das Row→Dict-Mapping lebt in nc/convmap.py (bitgenau geprüft)."""
    with db_conn() as conn:
        rows = conn.execute(
            "SELECT id, role, content, created_at, model, duration_ms, error "
            "FROM ai_messages WHERE conversation_id = ? ORDER BY id ASC",
            (conv_id,)).fetchall()
    return _nc_convmap.messages(rows)
