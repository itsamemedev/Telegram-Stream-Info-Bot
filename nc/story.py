"""nc.story — StoryMemory: leichtgewichtiges Erzähl-Gedächtnis pro Live-Session.

Extrahiert aus bot.py. Sammelt Beats/Running-Gags/Stammzuschauer heuristisch
(kein LLM in der Hot-Loop) und liefert dem Director eine Kontext-Essenz. Die
Deque-Länge (STORY_MAX_BEATS) wird per configure() injiziert.
"""

import collections as _collections
import time as _time_mod

STORY_MAX_BEATS = 40


def configure(max_beats=None):
    """bot.py reicht STORY_MAX_BEATS rein (identisches Verhalten)."""
    global STORY_MAX_BEATS
    if max_beats is not None:
        STORY_MAX_BEATS = int(max_beats)


class StoryMemory:
    """Leichtgewichtiges Erzähl-Gedächtnis pro Live-Session. Kein LLM in der
       Hot-Loop — sammelt Beats heuristisch; das LLM bekommt die Essenz als
       Kontext. Wird vom Director gespeist."""

    def __init__(self, username):
        self.user = username
        self.beats = _collections.deque(maxlen=STORY_MAX_BEATS)   # markante Momente
        self.gags = _collections.Counter()                        # wiederkehrende Phrasen
        self.regulars_seen = set()
        self.started = _time_mod.time()

    def note_moment(self, text, kind="moment"):
        t = (text or "").strip()
        if t:
            self.beats.append({"ts": _time_mod.time(), "kind": kind, "text": t[:120]})

    def note_regular(self, name):
        if name:
            self.regulars_seen.add(name[:24])

    def note_phrase(self, phrase):
        p = (phrase or "").strip().lower()
        if 4 <= len(p) <= 40:
            self.gags[p] += 1

    def recap(self):
        """Kurze Kontext-Notiz für die nächste Reaktion (der 'rote Faden')."""
        if not self.beats and not self.regulars_seen:
            return ""
        bits = []
        if self.beats:
            recent = list(self.beats)[-3:]
            bits.append("Bisher im Stream passiert: " + " → ".join(b["text"] for b in recent))
        top_gag = self.gags.most_common(1)
        if top_gag and top_gag[0][1] >= 3:
            bits.append(f"Running Gag/Thema: '{top_gag[0][0]}' (kam {top_gag[0][1]}× vor)")
        if len(self.regulars_seen) >= 2:
            bits.append("Stammzuschauer heute: " + ", ".join(list(self.regulars_seen)[:4]))
        return "STORY-GEDÄCHTNIS — " + " | ".join(bits) if bits else ""

    def snapshot(self):
        return {"beats": len(self.beats), "regulars": len(self.regulars_seen),
                "top_gag": (self.gags.most_common(1)[0] if self.gags else None),
                "recap": self.recap()[:300]}
