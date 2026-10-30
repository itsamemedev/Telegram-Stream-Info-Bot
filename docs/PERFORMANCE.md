# Performance & Stabilität — Betreiber-Notiz

Härtungs-Sprint ab v4.2-W117. Sechs Pakete, eines je Welle, jedes einzeln
auslieferbar und rückrollbar. Diese Datei wächst mit jedem Paket.

## Plan

| Paket | Inhalt | Erwartete Wirkung |
|---|---|---|
| **A — Event-Loop-Schutz** | Loop-Lag in ms messen, blockierende Stelle benennen, Log-Schleuse gegen Nachzügler, DB-Zugriffe der heißen Pfade neben den Loop, Sperre gegen neue | Stockungen unter 3 s werden sichtbar **und** lokalisierbar; die bekannten Plattenlast-Stockungen in Restream/Intel fallen weg |
| **B — Nebenläufigkeit & Gegendruck** | Semaphoren und Grenzen prüfen (Auflösung, Aufnahmen, Restreams, TikTokLive-Clients), Prozessstarts drosseln, harte Deckel mit Meldung statt stiller Überlast | Kein Einbruch unter Last, sondern sichtbares Abregeln |
| **C — Caches, Polling, heiße Pfade** | Live-Status-Cache und Nachschläge, adaptives Polling ohne Rückkopplung, Status-Aggregation für Deck/Befehle ohne Vollscan | Kürzere Zeit live → Aufnahme, weniger Last je Abfrage |
| **D — Prozess- & Ressourcen-Lebenszyklus** | Kindprozesse lückenlos verfolgen und abräumen, fd-/Zombie-Schutz, Deckel auf langlebige Dicts | Kein Wachstum über Tage |
| E — Start, Stopp, Neustart | Unabhängige Initialisierung parallel, sauberes Herunterfahren ohne Waisen-ffmpeg, „degradiert aber lebendig" vs. „tot" | Schnellerer, deterministischer `systemctl restart` |
| F — Leichte Beobachtbarkeit | Aktive Aufnahmen/Restreams/Clients, Cache-Trefferquote, Resolver-Latenz, fds, Kindprozesse, RSS — billig, ohne Log-Flut | Ein Blick auf `/healthz` statt SSH |

## Paket A — Event-Loop-Schutz (W117)

### Was sich geändert hat

Der Bot misst jetzt in 100-ms-Schritten, wie lange der Event-Loop steht.
Bisher gab es dafür nur zwei grobe Schwellen (3 s Warnung, 30 s Stack-Dump).
Alles darunter — der „zähe" Bot — war unsichtbar.

Steht der Loop länger als 250 ms, liest ein eigener Thread die Zeile, an der
er steht, und meldet sie im Log:

    Event-Loop 840 ms gestanden an bot.py:_monitor:15008 > nc/dbwrap.py:db_conn:370

Vor dem `<-` stehen die zwei innersten Stellen im eigenen Code (dort wird es
behoben), dahinter — falls vorhanden — die innerste Stelle überhaupt, woran es
hängt (`logging/__init__.py:handle`, `threading.py:wait`). Ein `sqlite3`- oder
`time.sleep`-Aufruf hat keinen eigenen Python-Rahmen; dann endet die Zeile
beim eigenen Code. Dieselbe Stelle meldet sich höchstens alle 15 Minuten, eine
neue sofort. Ab einer Sekunde Stillstand auf ERROR, darunter auf WARNING.

Die Datenbankzugriffe in Restream-Steuerung, Auto-Scheduler, Live-Chat,
Director, Discord-Clip und Liveboard laufen jetzt in einem Thread; die
Transkript-Indizierung rechnete ihre Einbettungen bisher auf dem Loop.

### Neue Schalter

| Variable | Vorgabe | Wirkung |
|---|---|---|
| `LOOP_TAKT_MS` | 100 | Schrittweite der Messung |
| `LOOP_BUDGET_MS` | 100 | Ab hier zählt ein Schritt als „über Budget" (nur Zählung) |
| `LOOP_SPAEHER_MS` | 250 | Ab hier wird die blockierende Stelle erfasst; `0` = aus |

Die Messung kostet rund 0,4 % eines Kerns. Abschalten ist nicht nötig.

### Wo man hinsieht

`/healthz` (ohne Anmeldung):

    "loop_lag": {"aktiv": true, "p50_ms": 0.3, "p99_ms": 4.1, "max_ms": 38.0,
                 "ueber_budget": 0, "stockungen": 0, "fenster_s": 300, ...},
    "log_synchron": 0

- `p99_ms` dauerhaft über 100: der Loop ist regelmäßig belegt — im Log nach
  „Event-Loop … gestanden an" suchen.
- `stockungen` steigt: es gab Stillstände über 250 ms; die Stellen stehen in
  `/api/debug/threads` → `loop_bremser`, sortiert nach Gesamtdauer.
- `aktiv: false`: es läuft **keine** Messung (Bot startet noch, oder der Takt
  ist gestorben) — nicht mit „kein Lag" verwechseln.
- `log_synchron` > 0: ein Log-Handler schreibt an der Schleuse vorbei und kann
  den Loop wieder an der Platte festhalten. Welcher, steht in
  `/api/debug/threads` und im error.log.

### Verhalten unter Last

Unter einer Log-Flut mit drei mitloggenden Threads und einer Platte, die je
Zeile 20 ms braucht, stand der Loop ohne Schleuse 560 ms, mit Schleuse 1,8 ms
(Vertrag `_test_v42_w117_log_flut_haelt_den_loop_nicht`). Unter Plattenlast
blockieren SQLite-Zugriffe in den umgestellten Pfaden jetzt nur noch ihren
eigenen Thread, nicht mehr den ganzen Bot.

### Was bewusst geblieben ist

48 blockierende Aufrufe direkt in `async def` stehen noch im Bestand,
überwiegend in Telegram- und Discord-Befehlen, die selten laufen. Sie einzeln
umzubauen wäre Risiko ohne Nutzen. `tools/loopblocker.py --sperre` verhindert,
dass es mehr werden; was davon wirklich stört, zeigt der Späher im Betrieb.

## Paket B — Nebenläufigkeit & Gegendruck (W118)

### Was sich geändert hat

- **Dateideskriptoren:** Der Dienst lief bisher mit 1024 — die Unit setzte kein
  `LimitNOFILE`. Der Bot hebt das Soft-Limit beim Start selbst an (bis zum
  Hard-Limit, höchstens 65536). Im Log beim Start:

      fd-Grenze angehoben: 1024 -> 65536

  Steht stattdessen „fd-Grenze bleibt bei …", erlaubt das Hard-Limit nicht
  mehr — dann `LimitNOFILE=65536` unter `[Service]` in die Unit eintragen,
  `systemctl daemon-reload`, Neustart. Neue Installationen haben die Zeile.
- **Deckel für parallele Aufnahmen** (`MAX_PARALLEL_AUFNAHMEN`). Vorgabe 0 =
  automatisch: vier je Kern, mindestens acht, auf der 8-Kern-Box also 32.
- **fd-Sperre:** Ab 85 % belegter Dateideskriptoren startet kein neuer
  ffmpeg mehr, weder für Aufnahmen noch für Restreams — sonst verliert der Bot
  gleich danach Datenbank und Netz.
- **Live-Check-Schlange:** Läuft sie über, steht das jetzt im Log, statt dass
  ein Nutzer still später geprüft wird.

### Neue Schalter

| Variable | Vorgabe | Wirkung |
|---|---|---|
| `MAX_PARALLEL_AUFNAHMEN` | 0 (= 4 je Kern, mind. 8) | Höchstzahl gleichzeitiger Aufnahmen |

`RESTREAM_MAX_CONCURRENT` (Vorgabe 2) und `WORKER_COUNT` (Vorgabe 4) bleiben,
wie sie sind.

### Wo man hinsieht

`/healthz` → `gegendruck`:

    "gegendruck": {"aufnahmen": 3, "aufnahmen_deckel": 32,
                   "fd": {"offen": 212, "grenze": 65536, "anteil": 0.003},
                   "abgewiesen": {}, "pruef_schlange": 0,
                   "pruef_schlange_max": 200, "pruef_verworfen": 0}

- `fd.grenze` 1024: die Anhebung hat nicht gegriffen (siehe oben).
- `fd.anteil` steigt über Tage ohne mehr Aufnahmen: ein Leck — Paket D.
- `abgewiesen` nicht leer: `aufnahme:deckel` heißt, der Deckel hat gegriffen;
  `aufnahme:fd` oder `restream:fd` heißt, die Deskriptoren werden knapp.
  Das error.log nennt dazu Nutzer und Abhilfe (einmal je 15 Minuten je Grund).
- `pruef_verworfen` > 0: die Worker kommen nicht nach — `WORKER_COUNT`
  erhöhen oder nach „Event-Loop … gestanden" suchen (Paket A).

### Verhalten unter Last

Gehen mehr Nutzer gleichzeitig live, als der Deckel erlaubt, starten die
ersten bis zum Deckel; die übrigen werden beim nächsten Live-Check (alle 30 s
für einen Live-Nutzer) erneut gefragt und starten, sobald eine Aufnahme endet.
Kein Lock bleibt hängen, kein Nutzer wird gesperrt. Was abgewiesen wurde, steht
im Log — nichts verschwindet still.

## Paket C — Caches, Polling, heiße Pfade (W119)

### Was sich geändert hat

- **Live-Erkennung:** Fragen mehrere Stellen gleichzeitig nach demselben Nutzer
  (zwei Chats, Restream-Scheduler, Deck), löst der Bot ihn nur noch **einmal**
  auf; alle anderen bekommen dasselbe Ergebnis. Weniger Anfragen bei TikTok,
  weniger 429, weniger doppelte Logzeilen.
- **Cache-Aufräumen** läuft jetzt verlässlich alle 64 Schreibvorgänge.
- **Polling unter Last:** Ist die Live-Check-Schlange mehr als halb voll,
  werden Nutzer, die offline sind oder nicht ermittelt werden konnten, seltener
  geprüft — bei voller Schlange halb so oft. Live-Nutzer und gerade offline
  gegangene werden **nie** gedehnt; VIP-Prioritäten gelten weiter.
- **Deck-Puls:** Egal wie viele Tabs offen sind, `/api/pulse` rechnet höchstens
  einmal je 2 Sekunden.

Keine neuen Schalter.

### Wo man hinsieht

`/healthz` → `livecache`:

    "livecache": {"treffer": 812, "fehlschlag": 1430, "trefferquote": 0.362,
                  "geteilt": 57, "laeufe": 1430, "dauer_mittel_ms": 1840,
                  "dauer_max_ms": 20112, "eintraege": 41, "laufend": 1}

- `geteilt`: so viele doppelte Auflösungen wurden eingespart.
- `dauer_mittel_ms` über ein paar Sekunden: die Auflösung geht oft über den
  langsamen Weg (yt-dlp); dann lohnt ein Blick auf die Resolver-Meldungen im
  Log (Cookies, Tunnel).
- `dauer_max_ms` um 20 000: yt-dlp läuft in seinen Timeout.
- `laufend` dauerhaft hoch: Auflösungen hängen — Tunnel/Proxy prüfen.

Liefert der Puls `"veraltet": true`, hing beim Bauen etwas (meist SQLite unter
Plattenlast); das Deck zeigt dann die Zahlen von vor wenigen Sekunden statt gar
keine.

## Paket D — Prozess- & Ressourcen-Lebenszyklus (W120)

### Was sich geändert hat

- **Hilfsprozesse** (yt-dlp-Erkennung, Clips, Discord-Verkleinern, TTS,
  Zerlegen und Reparieren von Aufnahmen, Tonspur-Prüfung) haben jetzt alle ein
  Zeitlimit und werden beendet, wenn die Aufgabe abgebrochen wird. Vorher
  konnte ein yt-dlp oder ein Neukodieren nach einem Abbruch unbemerkt
  weiterlaufen, und drei ffmpeg-Aufrufe konnten für immer hängen.
- **Speicher:** Einige interne Tabellen wuchsen mit jedem `/check` und jedem
  Clip für Nutzer, die nicht getrackt sind, und wurden nie geleert. Sie werden
  jetzt alle 10 Minuten beschnitten.

Keine neuen Schalter. Aufnahme- und Restream-Prozesse selbst hatten ihre
Abräumwege schon (W75/W83); die bleiben, wie sie sind.

### Wo man hinsieht

`/healthz`:

    "kinder": {"laufend": 1, "je_art": {"yt-dlp": 1}, "aeltester_s": 4,
               "gestartet": 3120, "zeitlimit": 17, "abgebrochen": 2,
               "getoetet": 0},
    "speicher": {"live_status_cache": 38, "rate_backoff": 2, ...}

- `kinder.aeltester_s` weit über den Zeitlimits (yt-dlp 20 s, Clip wenige
  Minuten): etwas hängt im Kernel (meist die Platte); ein Neustart räumt auf.
- `kinder.getoetet` steigt: Prozesse ignorieren SIGTERM — bei ffmpeg ein
  Hinweis auf eine hängende Ein-/Ausgabe.
- `kinder.zeitlimit` steigt schnell, vor allem bei `yt-dlp`: TikTok oder der
  Tunnel antworten langsam (siehe auch `livecache.dauer_max_ms`).
- `speicher`: bleibt über Tage ungefähr bei der Zahl der getrackten Nutzer.
  Steigt ein Wert stetig, ist es ein Leck — Wert und Name ins Ticket.
