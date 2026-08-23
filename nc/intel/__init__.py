"""nc.intel — Flaggschiff-Intelligenz für NIGHTCRAWLER v4.0.

Bewusst als eigenes Subpaket ausgelagert (Monolith-Abtrag): die drei großen
v4.0-Funktionen leben hier als self-contained, testbare Module — bot.py
bekommt nur dünne Adapter (Whisper-/Embed-/LLM-Funktion reinreichen, Routen).

- transcripts : gemeinsames Substrat — Transkript-Segmente je Aufnahme (Store).
- library     : Feature A — semantisches Stream-Archiv („Frag dein Archiv").
- reel        : Feature B — KI-Auto-Highlight-Reel.
- copilot     : Feature C — Live-Regie-Copilot.

Alle Module sind DB-/Backend-agnostisch: sie bekommen eine DBAPI-Connection und
die schweren Abhängigkeiten (Whisper, Embedding, LLM) injiziert — dadurch ohne
den ganzen Bot unit-testbar.
"""

__all__ = ["transcripts", "library", "reel", "copilot"]
