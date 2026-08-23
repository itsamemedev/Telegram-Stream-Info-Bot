# Changelog

Alle nennenswerten Änderungen an NIGHTCRAWLER. Format angelehnt an
[Keep a Changelog](https://keepachangelog.com/de/1.1.0/).

Die maßgebliche Quelle ist [`nc/version.py`](nc/version.py) — Dashboard-Footer,
`/api/version` und das „Was ist neu"-Panel lesen von dort. Die ausführliche
Historie aller Entwicklungswellen steht in [`README_V37.md`](README_V37.md).

---

## [Unveröffentlicht]

### Hinzugefügt — Selbst-Update aus dem Repo (W115)

Der Bestand lässt sich jetzt aus dem GitHub-Repo aktualisieren, ohne den Umweg
über ein ZIP von Hand. Die Entscheidungslogik liegt bot-frei und geprüft in
[`nc/updater.py`](nc/updater.py).

- **Übersicht, ganz vorn:** die Karte „Software-Stand" zeigt Version, lokalen
  Stand, Repo-Stand und Datum. Ablauf in vier Schritten, jeder einzeln
  auslösbar: prüfen → Trockenlauf → einspielen → neu starten.
- **Trockenlauf zuerst.** Er rechnet Datei für Datei durch, was sich ändern
  würde, und schreibt nichts. Erst danach steht die Rückfrage vor dem
  Einspielen.
- **Betriebsdaten sind unantastbar.** `.env`, Datenbanken, Logs, Aufnahmen,
  Archiv, Backups und die vom News-Agenten geschriebene `website/news.json`
  werden nie angefasst. Ohne diese Liste hätte ein Update die `.env` mit der
  `.env.example` überschrieben — 352 Variablen weg.
- **Nur hinzufügen und ersetzen, nie löschen.** Eine lokale Datei, die im
  Archiv fehlt, bleibt liegen; sonst räumt ein Update eigene Skripte weg, und
  das fällt erst Wochen später auf.
- **Nichts wird geschrieben, bevor das Backup steht.** Jede ersetzte Datei
  wandert vorher nach `backups/nc_update_<zeit>.zip`; scheitert das Backup,
  bricht das Update ab. `Zurückrollen` stellt genau diesen Stand wieder her.
- **Zip-Slip abgeriegelt.** Archivnamen mit `../` oder absolutem Pfad werden
  verworfen, zusätzlich prüft der Schreibpfad die Wurzel ein zweites Mal.
- **Im Hintergrund, mit Fortschritt.** Der Download dauert je nach Leitung bis
  zu einer Minute — im Flask-Request wäre der Browser in den Timeout gelaufen,
  während das Update in Wahrheit sauber durchläuft.
- **Telegram:** `/update`, `/update pruefen`, `/update jetzt`,
  `/update zurueck` — eingespielt wird nur nach ausdrücklichem „jetzt".
- **Website:** Abschnitt „Quellcode & Download" mit ZIP-Link, GitHub-Link und
  `git clone`. Neue Variablen: `UPDATE_ENABLED`, `UPDATE_REPO`,
  `UPDATE_BRANCH`, `UPDATE_RESTART_CMD`, `UPDATE_KEEP_BACKUPS`.

### Behoben — Übersicht blieb beim ersten Aufruf leer (W115)

Die Tab-Wiederherstellung beim Start klickt den Übersichts-Tab, läuft aber in
einem früheren Script-Block als `VIEW_LOADERS['overview']=loadOverview`. Zum
Zeitpunkt des Klicks war der Eintrag noch `undefined`, der Loader wurde
übersprungen — und der 8s-Intervall-Refresh deckt nur `system` ab. Kennzahlen,
Kommandozentrale und Trefferquote blieben deshalb leer, bis der Betreiber von
Hand auf einen anderen Tab und zurück ging. Jetzt stößt die Registrierung den
Loader selbst an, wenn die Übersicht vorn liegt.

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

### Sicherheit — Tiefen-Audit (W118)

Vollständiger Durchgang über Code-Ausführung, Deserialisierung, SQL, Pfade,
Web-Auth, XSS, SSRF, OAuth, Secrets und Abhängigkeiten. Sieben Befunde behoben,
jeder mit eigenem Vertrag in `test_restream.py`.

- **XSS im Dashboard (hoch, im Browser bewiesen).** 20 Stellen bauten
  `onclick="f('${esc(x)}')"`. `esc()` liefert für `'` das Zeichen `&#39;` — der
  HTML-Parser dekodiert Attributwerte aber, **bevor** die JS-Engine sie sieht.
  Aus `&#39;` wird wieder `'`, der String ist zu, der Rest läuft als Code.
  Nachgestellt: Eingabe `x');window.__xss=1;showProfile('y` ergab das Attribut
  `showProfile('x');window.__xss=1;showProfile('y')` — fremder Code lief in der
  Sitzung des Betreibers, also der Sitzung mit dem Dashboard-Cookie. Neu:
  `escJs()` mit `\xNN`-Sequenzen, die kein HTML-Sonderzeichen enthalten, die
  HTML-Dekodierung unverändert überstehen und erst von der JS-Engine
  **innerhalb** des Strings aufgelöst werden. Sechs Angriffsmuster
  gegengeprüft, Werte kommen unverändert am Handler an.
- **KI-SQL unter MariaDB (mittel).** `_safe_select` hatte die read-only
  Verbindung nur für SQLite (`mode=ro`); MariaDB fiel auf eine normale
  Schreibverbindung zurück. Der Wortfilter war ebenfalls auf SQLite gemünzt —
  `LOAD_FILE`, `OUTFILE`, `SLEEP`, `BENCHMARK`, `mysql.user`,
  `information_schema` fehlten, allesamt mit einem reinen `SELECT` erreichbar.
  Jetzt: Filter erweitert **und** `START TRANSACTION READ ONLY` mit `ROLLBACK`,
  damit eine Filterlücke allein nicht mehr reicht.
- **OAuth-`state` übersprungen (mittel).** `if state and _state["csrf"] and …`
  ließ die CSRF-Prüfung weg, sobald der Rückruf gar keinen `state` mitbrachte —
  und genau das bestimmt der Aufrufer. Twitch und YouTube: `state` wird jetzt
  erzwungen, sobald einer ausgegeben wurde.
- **Open Redirect (niedrig-mittel).** `nxt.startswith("/")` ließ `//example.com`
  durch — protokoll-relativ, vom Browser als `https://example.com` aufgelöst.
  Neu: `_sicheres_ziel()` weist `//host` und `/\host` ab.
- **Zwei schwache `esc`-Schatten (niedrig).** Lokale Maskierer ohne `'` in
  Funktionen, die fremde Creator-Daten rendern, verdeckten das globale,
  stärkere `esc`. Entfernt — es gibt jetzt genau einen.
- **`REDIS_URL` mit Passwort in `/api/system` (niedrig).** Neu:
  `_url_ohne_zugang()` maskiert Zugangsdaten, Host und Port bleiben lesbar.
- **PIN-Cookie ohne Ablauf (niedrig).** Der Wert war ein statischer HMAC über
  das PIN: einmal ausgestellt, für immer gültig, widerrufbar nur durch
  PIN-Wechsel. Jetzt trägt er seinen Ausstellungszeitpunkt (vom HMAC gedeckt,
  also nicht verschiebbar) und läuft nach `DASHBOARD_PIN_MAX_AGE_S` ab.
  **Der Betreiber muss sich einmalig neu anmelden.**

Geprüft und für unbedenklich befunden: keine `eval`/`exec`/`pickle`/`yaml.load`,
Pfad-Traversal überall über `realpath` + `commonpath` abgesichert, keine
eingehenden Webhooks ohne Signatur (der Bot pollt), API-Antworten ohne
Klartext-Geheimnisse, Token-Speicher mit `0600`, Rate-Limiting und
Brute-Force-Sperre vorhanden, Auth-Vergleiche zeitkonstant.

### Geändert — Anker-Hygiene und Cache-Stempel (W117)

- **Testfenster schneiden jetzt an der echten Grenze.** Die Verträge in
  `test_restream.py` verankern sich an wörtlichem Quelltext — daran führt bei
  einem 1,5-MB-Monolithen kein Weg vorbei. Das Problem waren nie die Textanker,
  sondern die **Fenster** der Form `src[i:i + 2200]` mit einem N, das jemand
  vor Monaten geschätzt hat: wächst die Zielfunktion darüber hinaus, meldet der
  Test etwas als fehlend, das zwei Zeilen weiter unten steht. Gemessen: von 31
  auflösbaren Fenstern hatten **13 weniger als 200 Zeichen Reserve** bis zur
  zuletzt geprüften Nadel. Neue Helfer `_fn(src, name)`, `_meth(src, Klasse,
  name)` und `_ab(src, marke)` schneiden per AST; 12 Fenster sind umgestellt
  (das dreizehnte prüft bewusst einen 160-Zeichen-Ausschnitt mit `not in` und
  bleibt).
- **Ein Wächter hält das so.** `test_v40_w117_ankerhygiene` misst bei jedem
  Lauf, wie viel Luft zwischen der zuletzt geprüften Nadel und dem Fensterrand
  liegt, und schlägt unter 150 Zeichen an — mit Zeilennummer und dem Hinweis,
  auf welchen Helfer umzustellen ist. Aus einem irreführenden „Vertrag
  gebrochen" wird damit eine Meldung, die sagt, was wirklich los ist.
- **`raum.css` und `raum.js` tragen einen Cache-Stempel.** Beide werden von
  allen drei öffentlichen Seiten geladen; ohne Stempel hält ein Browser mit
  warmem Cache nach einem Deploy die alte Fassung — die Seite bleibt dann still
  flach statt kaputt, und *weil* nichts bricht, fällt es niemandem auf. Der
  Stempel ist ein Inhalts-Hash (`?v=<sha256[:10]>`), keine Nummer zum
  Hochzählen: gleicher Inhalt, gleicher Stempel, Cache bleibt gültig. Gesetzt
  von [`tools/stempel_assets.py`](tools/stempel_assets.py), geprüft im
  Vertrag — dasselbe Muster wie bei `.env.example`.

### Behoben — Drei Zustände, die die Sicht verstellt haben (W116)

- **`_tee_fail` wurde nie geleert.** Geschrieben in `_read_stderr`, gelesen an
  fünf Stellen (Deck, Verify-Loop, Sentinel-Alarm, `status()`, Selbsttest) —
  geleert an keiner. Eine einmalige Ablehnung von YouTube stand bis zum
  Bot-Neustart im Panel **und im Sentinel-Alarm**, auch wenn das Ziel seit
  Stunden wieder sendet: Dauerfehlalarm, und bei der Fehlersuche jagt man einem
  Zustand von vorgestern hinterher. Jetzt zwei Wege raus, beide nötig:
  `tee_fehler()` filtert nach `RESTREAM_TEE_FAIL_TTL_S` (Vorgabe 15 min) und
  entsorgt Verfallenes gleich, und die Verify-Schleife löscht einen Eintrag,
  sobald die Plattform selbst bestätigt, dass sie wieder sendet. Alle fünf
  Lesestellen gehen über die Methode — Direktzugriff ist vertraglich verboten,
  sonst umgeht einer den Verfall.
- **Chat-Trennungen eskalierten nie.** Kick-WebSocket, Twitch-EventSub und
  Twitch-Chat meldeten auf `log.warning`; in einem ERROR-Log steht davon nichts.
  Die Verbindung konnte die ganze Nacht flattern, ohne dass irgendwo etwas
  stand — dasselbe Muster wie beim Discord-Gateway-Tod. „Jede Trennung auf
  error" wäre aber genauso blind, also entscheidet der Verlauf:
  [`nc/flapguard.py`](nc/flapguard.py) meldet erst, wenn vier Trennungen in eine
  Viertelstunde fallen, drosselt Wiederholungen und meldet die Erholung einmal.
  Alle drei Kanäle halten dafür jetzt fest, seit wann ihre Verbindung steht.
- **Der Aufnahme-Wächter maß nur das Dateiwachstum.** Das fängt den toten
  Stream, nicht den halbtoten: fällt die Videospur weg und der Ton läuft weiter,
  wächst die Datei im Kilobyte-Takt und der Wächter sieht Fortschritt — am Ende
  liegt eine Stunde Standbild auf der Platte. Neue zweite Spur über die
  **Rate** (`nc.recdiag.RateSpur`). Sie **meldet nur und bricht nicht ab**: eine
  wirklich statische Szene drückt die Bitrate völlig legitim um mehr als 85 %
  nach unten, und abgebrochenes Material ist unwiederbringlich weg. Der
  bewährte Nullwachstums-Kill bleibt unangetastet.

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
