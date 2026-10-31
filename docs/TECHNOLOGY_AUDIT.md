# Technologie-Audit — Leitdokument

> Ausgangsstand: v4.4.1, Commit `4fa5426`, Branch `main`, 31.10.2026.
> Dieses Dokument ist die priorisierte Befundliste. Die Einzelberichte
> entstehen Welle für Welle; was noch nicht gemessen ist, steht hier als
> offen und nicht als Behauptung.

| Bericht | Stand |
|---|---|
| [`DEPENDENCY_AUDIT.md`](DEPENDENCY_AUDIT.md) | **W134** — vollständig |
| [`SECURITY_AUDIT.md`](SECURITY_AUDIT.md) | **W134** — statisch vollständig, Server offen |
| `PERFORMANCE_AUDIT.md` | geplant W135 — Messung mit py-spy/tracemalloc, Vorher-Nachher |
| `ARCHITECTURE_REVIEW.md` | geplant W136 |
| `TESTING_REPORT.md` | geplant W136 |
| `INNOVATION_ROADMAP.md` | geplant W137 — Prototypen isoliert, mit Messung |
| `RELEASE_READINESS.md` | geplant zum Release-Kandidaten |

## Ausgangszustand (Phase 1)

- Arbeitsbaum sauber, `main` bei `4fa5426` (Merge von PR #173).
- Prüfkette aus CLAUDE.md vollständig grün; Verträge: 612 + 389 + 19.
- **Zusätzlich auf Python 3.14.6** (Produktionsfassung laut Server-Log)
  gefahren: alle drei Suiten grün. Die CI kannte 3.14 bis W134 nicht.
- Architekturgrenze: `nc/`, `brain/`, `discordbot.py` importieren nicht aus
  `bot.py`; `brain/` ist stdlib-only (außer einer Testdatei). Gemessen per
  Syntaxbaum, nicht angenommen.

## Priorisierte Befunde

Bewertung: Nutzen / Risiko der Änderung / Aufwand, jeweils hoch–mittel–niedrig.
„Belegt" heißt: gemessen oder im Log nachgewiesen.

| # | Befund | Beleg | Nutzen | Risiko | Aufwand | Status |
|---|---|---|---|---|---|---|
| 1 | Untergrenzen erlaubten 69 bekannte Schwachstellen | pip-audit | hoch | niedrig | niedrig | **behoben W134** |
| 2 | CI testete nicht die Produktions-Python 3.14 | Server-Log, lokaler Lauf | hoch | niedrig | niedrig | **behoben W134** |
| 3 | Dependabot war die leere Vorlage, lief nie | `.github/dependabot.yml` | mittel | niedrig | niedrig | **behoben W134** |
| 4 | TikTokLive-Lizenz falsch angegeben (MIT statt AGPL-3.0 mit Zusatz ab 7.0) | Rad-Metadaten | mittel | — | niedrig | **behoben W134** |
| 5 | `asyncio.iscoroutinefunction` veraltet seit 3.14, weg in 3.16 | DeprecationWarning auf 3.14 | niedrig | niedrig | niedrig | **behoben W134** |
| 6 | Kein Lockfile — Produktionsfassungen unbekannt | Repo, Logs | hoch | niedrig | niedrig, braucht den Server | **offen, Betreiber** |
| 7 | RSS stieg in 3,5 h von 230 MB auf 1,46 GB | Kennzahlen-Zeilen vom 31.10. | hoch | mittel | mittel | offen, W135 — erst nach W133 neu messen |
| 8 | Restliche synchrone DB-Zugriffe auf dem Event-Loop (`get_tracking_priority`, `_live_users`, `cfgstore.get`, `_set_status`) | `_loop_stockung_melden` | mittel | **mittel** — Reihenfolge der Schreibvorgänge | mittel | offen, W135 |
| 9 | Resolver meldet `status_code` für die Mehrheit der Nutzer | 386 Warnungen in 3,5 h | hoch | mittel | hoch | offen — eigene Welle mit Messung gegen TikTok |
| 10 | KI-Kette antwortet nicht (Pollinations `auth`, Anthropic-Guthaben leer, llama-server nicht erreichbar) | Log | hoch | — | Betrieb | **offen, Betreiber** |
| 11 | `AI_TIMEOUT=0` heißt 3600 s und hielt den Abbau fest | Stall-Dump | mittel | — | Betrieb | abgefangen W133; Wert in `.env` prüfen |
| 12 | `brain.db` war beschädigt, Ursache unbekannt | Backup-Log | mittel | — | mittel | offen — nach der Rettung beobachten |
| 13 | PySocks ohne Release seit 2019 | PyPI | niedrig | niedrig | niedrig | später |
| 14 | TikTokLive 7.x ungeprüft, signiert über Drittanbieter | PyPI, Lizenz | mittel | **hoch** | mittel | Prototyp isoliert, W137 |

## Bewusst verworfen

- **Migration auf die offizielle TikTok-API** — laut Auftrag ausgeschlossen.
- **Ersatz von python-telegram-bot oder discord.py** — kein messbarer Gewinn,
  sehr hoher Umbau an über 200 Sendestellen.
- **Eine Lockfile aus den neuesten PyPI-Fassungen** — wäre eine Behauptung
  über eine Umgebung, die niemand gefahren hat.
- **Obere Grenze `TikTokLive < 7` in `requirements.txt`** — der bekannte
  Bruch lag innerhalb der 6er-Reihe; was schützt, ist das Lockfile. Dependabot
  schlägt die Hauptversion trotzdem nicht automatisch vor.

## Wellenplan

| Welle | Inhalt |
|---|---|
| W134 | Bestandsaufnahme, Dependency- und Security-Audit, Befunde 1–5 |
| W135 | Performance: Speicherwachstum messen (tracemalloc-Schnappschüsse, nach W133), Loop-Stockungen mit Vorher-Nachher |
| W136 | Architektur- und Testbericht; Lücken in der Überdeckung gezielt schließen |
| W137 | Prototypen isoliert: TikTokLive 7.x gegen 6.x, Hardware-Encoding, Streaming-Scheduler — nur mit Messung |
| danach | Release-Kandidat mit Prüfsummen und Rollback-Beschreibung, **ohne** Veröffentlichung |
