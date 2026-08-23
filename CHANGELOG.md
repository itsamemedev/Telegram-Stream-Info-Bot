# Changelog

Alle nennenswerten Änderungen an NIGHTCRAWLER. Format angelehnt an
[Keep a Changelog](https://keepachangelog.com/de/1.1.0/).

Die maßgebliche Quelle ist [`nc/version.py`](nc/version.py) — Dashboard-Footer,
`/api/version` und das „Was ist neu"-Panel lesen von dort. Die ausführliche
Historie aller Entwicklungswellen steht in [`README_V37.md`](README_V37.md).

---

## [Unveröffentlicht]

### Behoben — Restream-Stabilität (W113)

Fünf Befunde im Wiederanlauf-Pfad des Restreams, alle in
`RestreamManager._monitor`. Die Entscheidungslogik liegt jetzt bot-frei und
geprüft in [`nc/restream_stability.py`](nc/restream_stability.py).

- **Reconnect-Budget kam nie zurück.** `attempts` wanderte von Reconnect zu
  Reconnect weiter und wurde nur beim Start von Hand geleert. Ein Ziel, das
  acht Stunden lief und dabei fünfmal kurz stolperte, galt danach als
  „aufgegeben nach 5 Reconnects" — ab da half nur noch die Verify-Schleife mit
  120s-Takt und bis zu 900s Backoff statt 8s. Jetzt gibt ein Lauf ab
  `RESTREAM_STABLE_RUN_S` (180s) das Budget zurück. Für die unabhängigen
  Relays war genau das in W87 schon repariert; der Hauptpfad blieb aussen vor.
- **Backoff linear und ohne Streuung.** Gleichzeitig gestorbene Restreams
  kehrten auf die Sekunde gemeinsam gegen dieselbe Ingest und dieselbe
  TikTok-Auflösung zurück — der direkte Weg ins 429. Jetzt exponentiell,
  gedeckelt und mit ±25 % Streuung.
- **Der Ablauf-Pfad hatte keine Untergrenze.** Eine abgelaufene TikTok-Quell-URL
  führte zu 2s Pause und einem Neuversuch ohne Fehlversuch — endlos. Solange
  der Lauf Minuten hielt, ist das richtig (TikToks Signaturen rotieren ~alle
  sechs Minuten); starb der Prozess nach Sekunden, drehte sich Resolve plus
  ffmpeg-Spawn im 2s-Takt weiter. Jetzt bremst eine Serienzählung, und ab der
  letzten Stufe zählt der Versuch als echter Fehlversuch.
- **Der copy→transcode-Fallback sprang auf Netzfehler an.** Die Heuristik
  enthielt `"failed to"` und `"unable to"` — beides steht wörtlich in
  „Failed to resolve hostname" und „Unable to open resource". Ein kurzer
  Netzhänger in den ersten 25 Sekunden schaltete den Restream damit für die
  ganze Sitzung auf transcode, dessen Encode-Rückstand der Bot selbst als
  „die typische Disconnect-Ursache" warnt. Starke Codec-Marker gelten weiter
  unabhängig vom Netz-Rauschen, die schwachen nur ohne Netzbefund.

### Hinzugefügt

- **Stillstands-Wächter für den Restream.** `_monitor` hängt an `proc.wait()`
  und sieht deshalb nur den *toten* ffmpeg — nicht den, der lebt und nichts
  mehr sendet (RTMP-Ausgang blockiert, Input steht, tee-Slave mit
  `onfail=ignore` weggebrochen). Bisher fror die Health-Anzeige ein und das
  Panel zeigte weiter „live". Der Wächter belegt Fortschritt an Bild **oder**
  Bytes, nie am blossen Eintreffen eines `-progress`-Blocks, und beendet einen
  stehenden Prozess, damit `_monitor` neu aufbaut. Ein so beendeter Lauf füllt
  das Reconnect-Budget nicht auf. Blind heisst nicht tot: fehlen die Messwerte,
  wird nicht abgeschossen. Neue Felder in `/api/restream/*`:
  `ohne_fortschritt_s`, `stillstaende`.
- **Der progress-Leser verschluckt seinen Tod nicht mehr** (`_loop_fehler`
  statt blankem `pass`). Stirbt er, friert die gesamte Health-Anzeige ein und
  der Wächter wird blind — beides war vorher nirgends sichtbar.
- Neue Stellschrauben: `RESTREAM_STABLE_RUN_S`, `RESTREAM_MAX_RECONNECTS`,
  `RESTREAM_BACKOFF_BASE_S`, `RESTREAM_BACKOFF_MAX_S`,
  `RESTREAM_STALL_TIMEOUT_S` (0 = Wächter aus), `RESTREAM_STALL_GRACE_S`,
  `RESTREAM_STALL_CHECK_S`.

### Behoben — Blinde Flecken im Restream-Pfad (W115)

Drei Stellen, die W113 offen gelassen hat.

- **Die unabhängigen Relays waren blind.** `_spawn_independent` startete ffmpeg
  mit `stdout=DEVNULL` — die Kommandozeile trägt seit jeher `-progress pipe:1`,
  es hat nur nie jemand zugehört. Für Twitch/YouTube im Modus
  `RESTREAM_MULTI_MODE=independent` gab es dadurch **weder Health-Daten noch
  Stillstands-Erkennung**: ein hängender Relay fiel erst der Plattform-Prüfung
  auf (120s-Takt, 3 Fehlanzeigen ≈ 6 Minuten) — und auch nur, wenn deren API
  antwortet. Jetzt bedienen **derselbe** Health-Parser und **derselbe**
  Stillstands-Wächter beide Pfade (`pname`-Parameter). Der Relay bringt nur
  einen eigenen, härter getakteten Regelsatz mit (`_RESTREAM_RELAY_POLICY`:
  Grundtakt 3s statt 8s, Deckel 30s statt 60s, gesunder Lauf ab 120s — der
  W87-Wert, unverändert). Sein Backoff streut jetzt ebenfalls.
- **Die W113-Messwerte sah niemand.** `ohne_fortschritt_s` und `stillstaende`
  standen in `/api/restream/verify`, kamen in `dashboard.html` aber kein
  einziges Mal vor. Neu: Spalte **„Bild fließt"** in der Zielprüfung,
  farbcodiert gegen `stall_timeout_s` (das die API jetzt mitliefert, statt dass
  das Panel den Default doppelt kennt), plus eine eigene Zeile je Relay mit
  Laufzeit, Fluss, pid und speed.
- **`_source_watch` fing nur `CancelledError`.** Jede andere Ausnahme beendete
  den Task; asyncio meldet so etwas frühestens beim Aufräumen als „Task
  exception was never retrieved". Folge: der Quellen-Failover für dieses Ziel
  war für den Rest der Laufzeit tot, und der Bot wartete auf einen
  ffmpeg-Abbruch, der bei einer sauber beendeten TikTok-Sendung nie kommt.
  Jetzt überlebt eine einzelne gescheiterte Runde — sichtbar über
  `_loop_fehler`, der Wächter läuft weiter.

### Hinzugefügt — Die Website steht im Raum (W114)

Die öffentliche Seite hatte drei räumliche Widgets (Sentinel-Kern,
Verbrauchsbalken, Spendenmünze) auf einer flachen Fläche. Jetzt trägt die
Seite selbst die Tiefe — auf **allen drei Seiten** (Start, Impressum,
Datenschutz) aus einer Quelle: [`website/raum.css`](website/raum.css) und
[`website/raum.js`](website/raum.js). Dependency-frei wie der Rest der
Seite: Vanilla-Canvas, kein Fremd-Code, kein externer Request.

- **Perspektivischer Korridor** hinter dem Inhalt — Boden, Decke, Ringe und
  ein driftendes Knotenfeld, gekoppelt an Scrollstand und Zeiger.
- **Jede Sektion auf eigener Z-Ebene.** Sie kippt und liegt hinten, während
  sie in den Blick kommt, und steht **exakt plan, sobald sie die Lesezone
  abdeckt** — dauerhaft gekippter Fließtext wird unscharf gerastert.
- **Kacheln als Körper**: Stream-Knöpfe, Karten, Kennzahlen und Agenten
  neigen sich unter dem Zeiger, das Akronym ist als Extrusion ausgestellt.
- **Schalter „Flach" / „3D"** unten rechts, in `localStorage` gemerkt.
  Vorgabe an; bei `prefers-reduced-motion` aus, aber umschaltbar — die
  ausdrückliche Wahl schlägt die Systemvorgabe. Ohne JS bleibt der Knopf
  versteckt und die Seite exakt die alte.
- Weniger Punkte auf schmalen Schirmen und schwachen Geräten, Pause im
  versteckten Tab, Zeigerparallaxe nur bei echtem Zeiger.

Drei Fallen, die im Browser gemessen und deshalb im Code festgehalten sind:
`perspective` steht **im transform-Funktionsaufruf je Sektion**, nicht als
CSS-Eigenschaft auf `main` (das Element ist über zehntausend Pixel hoch — der
Fluchtpunkt säße einmalig in dessen Mitte); `overflow-x:clip` sitzt auf
`main`, **nicht auf `html`** (an der Wurzel nimmt es der Kopfleiste in
Chromium ihr `position:sticky`); und der Schalter steht **außerhalb der
Navigation** (auf 390px füllt die Kopfleiste bereits zwei Zeilen — ein
weiteres Element machte sie 37 % höher).

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
