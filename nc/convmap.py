"""nc.convmap — v4.0-W55b: das Row→Dict-Mapping der AI-Conversation-Messages.

Aus _conv_messages herausgelöst: nimmt die DB-Zeilen (sqlite3.Row, chronologisch)
und formt sie in die stabile Message-Struktur fürs Frontend. Rein — Zeilen rein,
Liste aus dicts raus; das SELECT bleibt beim Aufrufer. Bitgenau gegen den
Monolithen geprüft.
"""

_FIELDS = ("id", "role", "content", "created_at", "model", "duration_ms", "error")


def messages(rows):
    """Message-Zeilen einer Conversation → Liste stabiler dicts (gleiche
       Reihenfolge wie die Eingabe, also chronologisch wie das SELECT)."""
    return [{f: r[f] for f in _FIELDS} for r in rows]
