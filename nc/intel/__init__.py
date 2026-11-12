"""nc.intel — Flaggschiff-Intelligenz für NIGHTCRAWLER v4.0.

Bewusst als eigenes Subpaket ausgelagert (Monolith-Abtrag): die drei großen
v4.0-Funktionen leben hier als self-contained, testbare Module — bot.py
bekommt nur dünne Adapter (Whisper-/Embed-/LLM-Funktion reinreichen, Routen).

- transcripts : gemeinsames Substrat — Transkript-Segmente je Aufnahme (Store).
- library     : Feature A — semantisches Stream-Archiv („Frag dein Archiv").

v5.6-W197: `reel` (Auto-Highlight-Reel) ist entfernt — der „duenne Adapter im
Bot", den es brauchte, wurde nie gebaut, das Modul lief nur in seinem eigenen
Test. `copilot` stand in __all__, ohne dass es die Datei je gab: ein
`from nc.intel import *` waere daran mit AttributeError gestorben.

Alle Module sind DB-/Backend-agnostisch: sie bekommen eine DBAPI-Connection und
die schweren Abhängigkeiten (Whisper, Embedding, LLM) injiziert — dadurch ohne
den ganzen Bot unit-testbar.
"""

__all__ = ["transcripts", "library"]
