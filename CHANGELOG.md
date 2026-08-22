# Changelog

Alle nennenswerten Änderungen an NIGHTCRAWLER. Format angelehnt an
[Keep a Changelog](https://keepachangelog.com/de/1.1.0/).

Die maßgebliche Quelle ist [`nc/version.py`](nc/version.py) — Dashboard-Footer,
`/api/version` und das „Was ist neu"-Panel lesen von dort. Die ausführliche
Historie aller Entwicklungswellen steht in [`README_V37.md`](README_V37.md).

---

## [4.0] — 2026-08 · „Restream Control Room"

### Multi-Plattform-Moderation & offener Kern

#### Hinzugefügt
- **Moderator überall** — KI-Moderation auf Kick, Twitch und YouTube über eine
  geteilte Heuristik (`nc/modheuristics.py`).
- **AZRAEL in allen drei Chats** — adressiert an genau einen User im Restream.
- **Kick User-OAuth** — Stream-Titel und Kategorie direkt aus dem Dashboard setzen.
- **News- und Marketing-Agent** — eigene Kanäle und Website automatisch bewerben.
- **Sicherer Restream-Test-Push** — Ziel prüfen ohne Broadcast-Risiko
  (`nc/restream_testpush.py`).
- **Sentinel-Flotte** — zwölf Wächter-Agenten mit Telegram-Alarmen, einzeln
  abschaltbar: `health`, `recovery`, `scout`, `analytics`, `learning`,
  `sentinel` (CrowdSec), `disk`, `restream_sentinel`, `toxicity`, `uptime`,
  `recording`.
- **Stream-Archiv-Indexer** (opt-in via `ARCHIVE_INDEX_ENABLED=1`) mit
  Transkripten und Reels (`nc/intel/`).
- **Loop-Stall-Watchdog** — schreibt bei eingefrorenem Event-Loop automatisch
  einen Voll-Stack-Dump ins Log.
- **PWA** — Dashboard als installierbare Android-App (Manifest, Service Worker,
  Icons). API-Antworten werden bewusst **nie** gecacht.
- **Loyalty-System** — Punkte und Ränge für Stream-Treue, persistent in der DB.
- **Community-Discovery-Loop** — Wiedererkennung von Stammzuschauern, Live-Ping
  nach Discord, Highlight-Share.
- **`/api/selftest`** — fasst zusammen, was vorher fünf verschiedene Log-Greps
  waren, jeder Befund mit dem behebenden Befehl.
- **`tools/deploy.sh`** — prüft den neuen Build in einem Nebenverzeichnis
  komplett durch, schwenkt erst bei grünem Ergebnis um, rollt bei Fehlschlag
  automatisch zurück.

#### Geändert
- **Modularer Kern** — Schema, Moderations-Heuristik, Selbstanalyse und
  Stimmwahl in eigene Module gelöst (`nc/schema.py`, `nc/modheuristics.py`,
  `nc/piper_voices.py`).
- **SENTINEL-SHIELD gehärtet** — Normalisierung von Unicode-Homoglyphen,
  Zero-Width-Zeichen, Diakritika (NFKD) und Trennzeichen-Tarnung vor der
  Prüfung. Mindestlänge von 4 auf 3 gesenkt. Weiterhin null False Positives
  über die Grenzfall-Suite.
- **Restream-Deckel** `RESTREAM_MAX_CONCURRENT` (Default 2) — vorher war der
  Multi-Modus unbegrenzt und hätte die CPU des GPU-losen Servers überrannt.
- **AZRAEL reagiert nur auf den restreamten User** (`AZRAEL_REACT_ONLY_LIVE`,
  Default 1) — Reaktionen auf nicht gesendete Streams waren im Sendebild
  verwirrend.
- **Overlay** — Sprechblase 300 → 440 px breit, Schrift 13 → 15 px, Höhe wächst
  mit dem Text; `AZRAEL_OVERLAY_MAXLEN` 240 → 400. Donation-Box nach oben links.
- **Llama.cpp-Budget** — `BRAIN_LLM_TIMEOUT_S` 60 → 300 s,
  `BRAIN_LLM_MAX_TOKENS` 512 → 1024, Kontextfenster 4096 → 8192.
  `REACTION_AI_TIMEOUT` bleibt bewusst kurz (75 s).
- **Discord = Telegram** — 15 `/sys_*`-Kommandos führen die
  Original-Telegram-Handler über einen Update/Context-Shim aus. Null Duplikate.
- **`requirements.txt`** existiert erstmals explizit — die 17 Fremdpakete standen
  vorher nur implizit im Code.

#### Behoben
- **Cookie-Log-Spam** — `_load_cookies_dict` warnte bei Permission-denied bei
  jedem der 21 Aufrufer erneut. Warnung auf max. alle 60 s gedrosselt.
- **Race Condition** — zwei Schleifen iterierten über
  `_RESTREAM_ACTIVE_ALL.items()` ohne `list()`, während ein paralleler Task
  `.pop()` aufrief → `RuntimeError`.
- **File-Handle-Leaks** — `/proc/meminfo`, `/proc/loadavg` und `nc/confdrift.py`
  lasen mit nacktem `open()`; im Health-Loop summiert sich das gegen das
  fd-Limit.
- **Discord-Upload-Limit** — Default auf die realen 10 MB korrigiert, echtes
  `guild.filesize_limit` zur Laufzeit, 413 → Schrumpfen + Retry.
- **404-Serien beim Recorder** — Preflight-GET vor dem Spawn,
  `_hd`/`_uhd`/`_sd`-Suffix-Fallback für einen CDN-Quirk; alles 404 → kein Spawn.
- **Live-React-Watchdog-Fehlalarme** — Heartbeat jetzt pro Loop-Iteration statt
  nur nach Reaktionen; Reaktions-KI-Calls hart auf `REACTION_AI_TIMEOUT` begrenzt.
- **Multi-Ziel-Restream** — `tee` ohne `onfail=ignore` riss den ganzen Fan-out
  ab; Copy-Modus war mit Multi-Target inkompatibel. Transcode wird jetzt
  automatisch erzwungen, sobald ein Zusatzziel aktiv ist.
- **`COLLATE NOCASE`** war SQLite-only und crashte jede Archiv-Liste unter
  MariaDB → `LOWER(...)`.
- **Connection-Leak in `api_brain`** — `conn.execute(...)` wurde nach `__exit__`
  aufgerufen; unter MariaDB ein Use-after-free für den nächsten Pool-Nutzer.
- **`disk.used_percent`** fehlte in `get_storage_stats()` — Health-Score-Disk
  hing permanent bei 70/100.

#### Entfernt
- **Nexus** vollständig — NeuralCore-Klasse, Loop, vier Routen, Env-Konfig,
  Dashboard-Panel und CSS. AZRAEL Sentinel ist das eigenständige System.
- **Obsidian-Integration** restlos — Definitionsblock, Aufrufe, zwei Routen,
  Panel, Env-Block. Die umgebende Logik (Schimpfwort-Lernen) bleibt.
- Tote Funktion `sparkline()` aus dem Dashboard.

---

## [3.7] — 2026-07 · „Kontrollraum-Fundament"

#### Hinzugefügt
- **Dreistufiger Recorder-Fallback**, adaptives Polling, Anti-Flap-Hysterese.
- **Multi-Plattform-Restream** (Kick / Twitch / YouTube).
- **Wissensgraph-Gehirn** mit Live-Visualisierung (`brain/` M1–M8).
- **Abo-Stream-Erkennung** mit eigenen Benachrichtigungen.
- **Einnahmen-Journal** (`nc/ledger.py`) — append-only mit Hash-Kette,
  CSV-Export fürs Finanzamt.
- **YouTube-OAuth-Flow** (`nc/ytoauth.py`) als Pendant zu `nc/twitchoauth.py`.
- **`tools/ncpatch.py`** — Patch- und Prüfwerkzeug samt Navigationskarte.
- **Restream-Aufsicht** — Soll-Zustand `restreams.desired`, Wiederanlauf nach
  Neustart, Ziel-Verifikation gegen die Plattform-APIs, vier Regeln gegen
  Neustart-Schleifen in `nc/restream_guard.py`.

---

[4.0]: https://github.com/itsamemedev/Telegram-Stream-Info-Bot/releases/tag/v4.0
[3.7]: https://github.com/itsamemedev/Telegram-Stream-Info-Bot/releases/tag/v3.7
