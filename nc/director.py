"""nc.director — LiveDirector: Regie-Instanz pro Live-User.

Extrahiert aus bot_v37.py. Hält Kurzzeit-Gedächtnis, misst Stream-Momentum und
entscheidet WANN/mit welcher Energie AZRAEL reagiert — reine schnelle Heuristik,
kein LLM in der Hot-Loop. Die DIRECTOR_*-Schwellen + AZRAEL_THANK_TRACKED_GIFTS
werden per configure() injiziert (identisches Verhalten wie im Monolithen).
"""

import collections as _collections
import os
import time as _time_mod

DIRECTOR_MIN_GAP_S = 8
DIRECTOR_MAX_GAP_S = 45
DIRECTOR_MEM_TURNS = 8
DIRECTOR_CHATTERS = 40


def configure(min_gap_s=None, max_gap_s=None, mem_turns=None, chatters=None):
    global DIRECTOR_MIN_GAP_S, DIRECTOR_MAX_GAP_S, DIRECTOR_MEM_TURNS, DIRECTOR_CHATTERS
    if min_gap_s is not None: DIRECTOR_MIN_GAP_S = int(min_gap_s)
    if max_gap_s is not None: DIRECTOR_MAX_GAP_S = int(max_gap_s)
    if mem_turns is not None: DIRECTOR_MEM_TURNS = int(mem_turns)
    if chatters is not None: DIRECTOR_CHATTERS = int(chatters)


class LiveDirector:
    """Pro Live-User eine Regie-Instanz: hält Kurzzeit-Gedächtnis, misst das
       Momentum des Streams und entscheidet, WANN und mit WELCHER Energie
       AZRAEL reagiert. Kein LLM in der Hot-Loop — reine, schnelle Heuristik;
       das LLM formuliert nur die Reaktion, die Regie liefert den Kontext."""

    def __init__(self, username):
        self.user = username
        self.said = _collections.deque(maxlen=DIRECTOR_MEM_TURNS)   # eigene letzte Aussagen
        self.chatters = _collections.OrderedDict()   # name -> {"n": msgs, "first": ts, "greeted": bool}
        self.beats = _collections.deque(maxlen=60)    # (ts, kind) Ereignis-Takt fürs Momentum
        self.highlights = []                          # markante Momente (fürs Gedächtnis/Recap)
        self.energy = 0.3                             # 0..1 gleitend
        self.mood = "chill"                           # chill|hype|drama|quiet|hostile
        self.last_react = 0.0
        self.last_speaker = ""
        self.started = _time_mod.time()
        self.react_count = 0

    # ---- Wahrnehmung -------------------------------------------------------
    def observe_chat(self, lines):
        """Chat-Zeilen 'name: text' bzw. Event-Strings verarbeiten → Chatter
           merken, Momentum-Beats setzen, neue/Gift-Ereignisse zurückgeben."""
        now = _time_mod.time()
        newcomers, gifts, questions = [], [], []
        for raw in lines:
            raw = (raw or "").strip()
            if not raw:
                continue
            low = raw.lower()
            if "geschenk" in low or "gift" in low or "🎁" in raw or "sendet" in low:
                self.beats.append((now, "gift")); gifts.append(raw[:80]); continue
            if raw.startswith("➕") or "folgt jetzt" in low:
                self.beats.append((now, "follow")); continue
            name, _, text = raw.partition(":")
            name = name.strip()[:24]; text = text.strip()
            if not text:
                text = name; name = ""
            if name:
                self.last_speaker = name
                c = self.chatters.get(name)
                if c is None:
                    self.chatters[name] = {"n": 1, "first": now, "greeted": False}
                    newcomers.append(name)
                    while len(self.chatters) > DIRECTOR_CHATTERS:
                        self.chatters.popitem(last=False)
                else:
                    c["n"] += 1
            self.beats.append((now, "chat"))
            if "?" in text and len(text) > 6:
                questions.append((name, text[:120]))
        return {"newcomers": newcomers, "gifts": gifts, "questions": questions}

    def observe_speech(self, text):
        if text and text.strip():
            self.beats.append((_time_mod.time(), "speech"))

    # ---- Momentum + Energie -----------------------------------------------
    def _recompute(self):
        now = _time_mod.time()
        w = [(t, k) for (t, k) in self.beats if now - t <= 20]   # 20s-Fenster
        rate = len(w) / 20.0                                     # Ereignisse/Sek
        gifts = sum(1 for _, k in w if k == "gift")
        chats = sum(1 for _, k in w if k == "chat")
        # Energie gleitend nachziehen (nie ruckartig)
        target = min(1.0, rate / 1.5 + gifts * 0.25)
        self.energy += (target - self.energy) * 0.4
        # Stimmung ableiten
        if gifts >= 2 or self.energy > 0.75:
            self.mood = "hype"
        elif rate < 0.08 and now - self.started > 45:
            self.mood = "quiet"
        elif chats >= 6 and self.energy > 0.5:
            self.mood = "drama"
        else:
            self.mood = "chill"
        return rate, gifts

    def gap_now(self):
        """Adaptives Reaktions-Fenster: viel los → kurz, tote Hose → lang."""
        self._recompute()
        span = DIRECTOR_MAX_GAP_S - DIRECTOR_MIN_GAP_S
        return DIRECTOR_MIN_GAP_S + span * (1.0 - self.energy)

    def should_react(self, has_input, gift_priority):
        if gift_priority:
            return True
        if not has_input:
            return False
        return (_time_mod.time() - self.last_react) >= self.gap_now()

    # ---- Regie-Anweisung fürs LLM -----------------------------------------
    def direction(self, obs):
        """Baut die Regie-Notiz, die als System-Kontext an AZRAEL geht: Stimmung,
           Energie, wen ansprechen, was zurückrufen, was NICHT wiederholen."""
        mood_line = {
            "hype":  "Der Stream KOCHT — hohe Energie, Gifts fliegen. Sei laut, mitreißend, feiernd, kurze schnelle Sätze.",
            "drama": "Im Chat brodelt's — viel Bewegung, evtl. Streit. Bring Klarheit und Haltung, moderiere die Energie.",
            "quiet": "Gerade ist es ruhig/leer. Halte die Stimmung locker am Leben, stell eine Frage in den Chat, ohne zu nerven.",
            "chill": "Entspannte Grundstimmung. Locker, nahbar, unterhaltsam.",
        }.get(self.mood, "")
        bits = [f"REGIE — Stimmung: {self.mood} (Energie {self.energy:.0%}). {mood_line}"]
        gr = [n for n in obs.get("newcomers", []) if not self.chatters.get(n, {}).get("greeted")]
        if gr:
            for n in gr[:3]:
                if n in self.chatters:
                    self.chatters[n]["greeted"] = True
            bits.append("Begrüße neu dazugekommene Zuschauer namentlich: " + ", ".join(gr[:3]) + ".")
        if obs.get("gifts"):
            # V37-P4a: Diese Regie läuft NUR im Live-React-Worker getrackter
            # TikTok-Streams — die Geschenke hier gehen an den GETRACKTEN
            # Streamer, nicht an unseren Kanal. AZRAEL hat sich dafür bedankt,
            # als wären es eigene Donations → peinlich und irreführend.
            # Default jetzt: als Stream-Moment kommentieren. Altverhalten per
            # AZRAEL_THANK_TRACKED_GIFTS=1 reaktivierbar.
            if os.getenv("AZRAEL_THANK_TRACKED_GIFTS", "0") in ("1", "true"):
                bits.append("Bedanke dich konkret & herzlich für Geschenke: " + " | ".join(obs["gifts"][:3]) + ".")
            else:
                bits.append("Im Quell-Stream wurden Geschenke gesendet (an den STREAMER, "
                            "nicht an dich): " + " | ".join(obs["gifts"][:3])
                            + ". Kommentiere das als Moment des Streams — bedanke dich "
                              "NICHT dafür, es sind nicht deine Geschenke.")
        if obs.get("questions"):
            qs = "; ".join((f"{n}: {q}" if n else q) for n, q in obs["questions"][:2])
            bits.append("Greife diese Chat-Frage(n) direkt auf und antworte darauf: " + qs)
        # Stamm-Chatter erkennen (mehr als 4 Nachrichten) → Bindung
        regulars = [n for n, c in self.chatters.items() if c["n"] >= 5][:3]
        if regulars and self.mood in ("chill", "hype"):
            bits.append("Aktive Stammzuschauer gerade: " + ", ".join(regulars) + " — beziehe dich ruhig mal auf sie.")
        if self.said:
            bits.append("Das hast du zuletzt schon gesagt — NICHT wiederholen, bring etwas Neues: "
                        + " / ".join(list(self.said)[-3:]))
        return "\n".join(bits)

    def record(self, text):
        """AZRAELs eigene Reaktion ins Gedächtnis + Highlight-Log."""
        self.last_react = _time_mod.time()
        self.react_count += 1
        t = (text or "").strip()
        if t:
            self.said.append(t[:160])
            if any(k in t.lower() for k in ("wow", "unfassbar", "krass", "!!!", "endlich", "hammer")):
                self.highlights.append({"ts": self.last_react, "text": t[:140]})
                self.highlights = self.highlights[-12:]

    def voice_style(self):
        """Regie-Tags für die Stimme (Tempo/Energie) je nach Stimmung."""
        return {
            "hype":  {"rate": 1.12, "tag": "energisch, schnell, begeistert"},
            "drama": {"rate": 1.0,  "tag": "bestimmt, klar, präsent"},
            "quiet": {"rate": 0.94, "tag": "ruhig, warm, einladend"},
            "chill": {"rate": 1.0,  "tag": "locker, freundlich"},
        }.get(self.mood, {"rate": 1.0, "tag": "natürlich"})

    def snapshot(self):
        return {"user": self.user, "mood": self.mood, "energy": round(self.energy, 2),
                "reacts": self.react_count, "chatters": len(self.chatters),
                "regulars": [n for n, c in self.chatters.items() if c["n"] >= 5][:5],
                "highlights": self.highlights[-5:],
                "uptime": int(_time_mod.time() - self.started)}


# Regie-Instanzen pro Live-User (fürs Dashboard sichtbar)
