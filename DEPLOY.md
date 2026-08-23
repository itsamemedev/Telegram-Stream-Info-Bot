# NIGHTCRAWLER v37 — Build B120

Dieses Archiv ist der **komplette Projektstand**, identisch aufgebaut wie das
Original. Entpacken, ueber das Bestandsverzeichnis legen, neu starten.

## 1. Sichern (nicht ueberspringen)

    cd ~/tiktok-bot
    tar czf ../nightcrawler_backup_$(date +%F_%H%M).tgz .

## 2. Einspielen

    sudo systemctl stop tiktok-bot
    unzip -o NIGHTCRAWLER_v37_B120.zip -d ~/tiktok-bot
    sudo systemctl start tiktok-bot

`.env`, `tiktok_cookies.txt`, `recordings/` und die Datenbank sind NICHT im
Archiv und bleiben unangetastet. `.env.example` ist nur die Vorlage.

## 3. Was neu dazukommt

    nc/ledger.py              Einnahmen-Journal (Finanzamt)
    nc/ytoauth.py             YouTube-OAuth-Flow (Pendant zu nc/twitchoauth.py)
    tools/ncpatch.py          Patch-/Validierungswerkzeug
    skills/nightcrawler/      Arbeitsanweisung fuer kuenftige Sessions
    DEPLOY.md                 diese Datei

Geaendert: bot_v37.py, brain_bridge.py, nc/freeai.py, nc/logfilters.py,
brain/llm.py. Alles andere unveraendert aus dem Original.

## 4. Beim Start mitlesen

    journalctl -u tiktok-bot -f | grep -Ei 'discord|brain|freeai|Normalisierung'

Erwartet:
  Discord verbunden als <bot> — 60 Slash-Commands aktiv.
  Brain-LLM: llama.cpp OK   ODER   KEIN Backend erreichbar
  ggf. Startup-Cleanup: N Usernames normalisiert

Bleibt Discord still, steht der Grund jetzt als ERROR mit Traceback im Log —
vorher war das ein WARNING und damit in einem Fehlerlog unsichtbar.

## 5. Pruefschritte

**KI-Basen**

    cd ~/tiktok-bot && python3 -c "import nc.freeai as f; print(f.diagnose())"

Zeigt pro Base: frei/gesperrt, Latenz, keyless/KEY, letzter Fehler.
Melden alle Pollinations-Basen "auth", brauchst du einen Key von
enter.pollinations.ai -> `POLLINATIONS_API_KEY` in die `.env`.
Optional `LLM7_TOKEN` von token.llm7.io (hebt 30 auf 120 Anfragen/min).

**Befehle**

    Telegram:  /brain          Statuszeile mit aktivem Backend
               /brain teste    echte Antwort statt "keine Antwort"
               /ai hallo
               /einnahmen
    Discord:   /status  /ai  /tracklist

**YouTube**

    curl -s localhost:8050/api/channels/status | jq .youtube

`"source":"api"` = Data API aktiv, exakte Zuschauer + Abonnenten.
`"source":"scrape"` = nicht verbunden, keyloser Fallback laeuft.

Verbinden geht jetzt im Dashboard: Panel **„YouTube verbinden"** direkt unter
dem Twitch-Panel. Es braucht nur YOUTUBE_CLIENT_ID + YOUTUBE_CLIENT_SECRET in
der .env; den Refresh-Token holt der Flow selbst (SETUP_YT_OAUTH.md).
Wie bei Twitch einmal `ssh -L 3000:localhost:8050 ...` tunneln und die Seite
ueber http://localhost:3000 oeffnen — Google erlaubt keine nackten IPs.

**Discord-Zustand**

    curl -s localhost:8050/api/discord/overview | jq .session

Enthaelt Versuche, Reconnects, letzten Grund und Zeitpunkt.

**Finanzamt**

    /einnahmen buchen 2026-02-15 twitch 412.50 0 TW-2026-01
    /einnahmen 2026
    curl -s "localhost:8050/api/finanzamt/entries?year=2026" | jq .summary
    Browser: localhost:8050/api/finanzamt/export.csv?year=2026

Datum = Tag der **Gutschrift auf dem Konto**, nicht der Stream-Tag.
Buchungen sind append-only; eine Korrektur ist eine Gegenbuchung
(`kind=correction` + `storno_of`), kein Ueberschreiben.

## 6. Restream-Aufsicht (B123)

Zwei getrennte Probleme, zwei Mechanismen.

**a) Wiederanlauf nach Neustart/Absturz**
Neue Spalten `restreams.desired` + `desired_since`: der SOLL-Zustand.
start() setzt ihn, nur ein ausdrueckliches stop() loescht ihn — ein
Absturz fasst ihn nicht an. Beim Start nimmt `_restream_resume_after_restart`
alles wieder auf, was laufen sollte. Vorher hing das allein an
auto_restream=1; von Hand gestartete Restreams waren nach einem Neustart weg.

**b) "online" war nur "Prozess existiert"**
Bei Multistream tragen Twitch und YouTube im tee-Muxer `onfail=ignore`
(damit ein klemmendes Twitch nicht Kick mitreisst). Genau deshalb laeuft
ffmpeg weiter, wenn sie wegbrechen — das Panel zeigte drei gruene Ziele,
waehrend auf zwei Plattformen nichts ankam.

`_restream_verify_loop` fragt jetzt alle RESTREAM_VERIFY_S die
PLATTFORMEN selbst (Kick keyless, Twitch Helix, YouTube Data API) und
baut den Restream neu auf, wenn ein Ziel nachweislich tot ist. Bei tee
laesst sich kein einzelnes Ziel neu verbinden, deshalb der ganze Prozess.

Vier Regeln gegen Neustart-Schleifen (in nc/restream_guard.py, isoliert
getestet):
  1. Anlaufkarenz 90s — RTMP braucht bis zu einer Minute, bis die
     Plattform live meldet. YouTube ist am langsamsten.
  2. Hysterese: 3 Fehlanzeigen in Folge, nicht eine.
  3. UNKNOWN != OFFLINE. Ein API-Timeout oder Quota-Fehler ist KEIN
     Beweis fuer einen toten Stream und zaehlt nicht mit.
  4. Backoff 60s, verdoppelnd bis 15 min.
  Zusaetzlich: ist die QUELLE offline, sind leere Ziele der Normalfall.

Pruefen:

    curl -s localhost:8050/api/restream/verify | jq

Zeigt pro Ziel die letzte Plattform-Antwort, Fehlanzeigen in Folge und ob
das Ziel seit dem Start je bestaetigt war. `targets_dead` ist die Antwort
auf "laeuft es wirklich?" — `live` bleibt der reine Prozess-Zustand.

Abschalten: RESTREAM_VERIFY=0.

## 7. Performance (B122)

Gemessen an einer realistisch gefuellten tiktok_checks-Tabelle:

| tiktok_checks | get_stats() gesamt |
|---|---|
| 50.000 Zeilen | 10 ms |
| 250.000 | 54 ms |
| 1.000.000 | 241 ms |
| 3.000.000 | 635 ms |

Diese drei Full-Scans hingen ueber api_stats() am 5-Sekunden-Puls des
Dashboards — 17.280 Aufrufe pro Tag und offenem Tab. Der Header zeigt davon
nichts; er liest nur live_now und active_trackings.

    /api/pulse   1164 ms  ->  0,2 ms
    CPU/Tag       335 Min ->  0,1 Min

Drei Aenderungen:
  * /api/pulse ruft api_stats(lean=True) — nur die drei billigen,
    indizierten Zaehler auf kleinen Tabellen.
  * get_stats() bekommt einen TTL-Cache (STATS_CACHE_TTL, Default 120s)
    fuer die Statistik-Ansicht.
  * tiktok_checks hatte als einzige Log-Tabelle KEINE Aufraeumung.
    Jetzt Kappung nach CHECKS_RETENTION_DAYS (30) und dem harten Deckel
    CHECKS_MAX_ROWS (200.000), plus Index auf created_at.
    Wirkung: 403 MB -> 27 MB, Statistik-Ansicht 1164 ms -> 42 ms.

Beim ERSTEN Start nach dem Update raeumt die Retention einmalig gross auf.
Danach einmal verdichten, damit der Plattenplatz auch zurueckkommt:

    sqlite3 <deine>.db "VACUUM;"

Abschalten geht ueber die .env (CHECKS_RETENTION_DAYS=0, CHECKS_MAX_ROWS=0).

## 7b. Was NICHT geaendert wurde und warum

Connection-Pooling fuer SQLite wurde geprueft und verworfen: db_conn()
oeffnet zwar bei jedem Aufruf neu, der Overhead betraegt aber gemessen
0,095 ms und der warme Page-Cache braechte nur 14 %. Gegen das Risiko
thread-geteilter SQLite-Connections in einem Prozess mit Recording-,
Restream- und Flask-Threads ist das kein guter Tausch.

Die ffmpeg-Pfade (x264-Presets, Thread-Deckel, Whisper-Drossel) waren in
frueheren Builds bereits begrenzt und wurden nicht angefasst.

## 8. Tiefensuche B124 — gefundene und behobene Fehler

**1. Shutdown loeschte den Soll-Zustand (schwer, selbst eingebaut in B123)**
`_shutdown` ruft `stop_all()`, und jedes `stop()` setzte `desired=0`. Nach
einem geordneten `systemctl restart` kam damit KEIN Restream zurueck — die
B123-Funktion haette nur nach einem harten Absturz gewirkt.
Fix: `stop_all(_keep_desired=True)` im Shutdown-Pfad.

**2. Quellen-Failover schaltete Restreams dauerhaft ab (schwer, B123)**
`_switch_to_next_live()` stoppte ohne `_keep_desired`. Jedes Mal, wenn eine
TikTok-Quelle offline ging, war der Restream dauerhaft deaktiviert.
Fix: Soll-Zustand bleibt; wird wirklich auf ein anderes Ziel umgeschaltet,
wandert er mit.

**3. Verify-Schleife ignorierte RESTREAM_SINGLE (schwer, B123)**
Bei mehreren desired=1-Zielen haette sie jedes gestartet. Im Single-Modus
gibt es aber genau EINEN Kick-Ingest — zwei ffmpeg-Encoder auf denselben
Stream-Key, und die Plattform trennt beide. Der Waechter haette den Ausfall
selbst erzeugt. Fix: Slot-Sperre.

**4. Fuenf Discord-Loops ohne Task-Referenz (schwer, Altbestand)**
`client.loop.create_task(...)` ohne Referenz. asyncio haelt nur eine SCHWACHE
Referenz — ein Task, der in `await asyncio.sleep()` haengt, kann vom GC
eingesammelt werden. Genau das tun alle fuenf (Liveboard, Wochen-Digest,
Clip der Woche, Error-Feed, Event-Countdown). Verschwindet einer, gibt es
KEINE Exception und KEINE Logzeile.
Fix: ueber `_spawn()` — haelt die Referenz und loggt Abstuerze.

**5. 32 ungeschuetzte DOM-Zugriffe auf nicht existierende Elemente (Altbestand)**
8 JS-Funktionen (loadSurveil, loadCaptures, loadVault, aiShowEmpty,
aiOpenConv, loadEvolution, renderTargetGrid, renderCaptures) schreiben auf
IDs, die in KEINEM Template stehen — Ueberbleibsel entfernter Ansichten. Das
Dashboard hat nur noch 5 Views. Jeder Aufruf warf "Cannot set properties of
null" und brach die Funktion ab.
Fix: Waechter mit fruehem `return` am Funktionsanfang.

**6. Irrefuehrender toter Code (kosmetisch)**
`if False:` / `and False` im Discord-Clip-Upload las sich wie ein Fehler.
Die echte Kompression laeuft weiter unten guild-genau. Zweig entfernt.

GEPRUEFT UND SAUBER: SQL-Injection (alle f-String-Queries whitelisted),
Arity und Keywords ueber 69 modeuluebergreifende Aufrufe, fehlende `await`,
veraenderliche Default-Argumente, Dict-Mutation waehrend Iteration,
Namensnutzung vor Definition auf Modulebene, 135 onclick-Ziele, 116
API-Aufrufe gegen 280 Routen.

## 8b. Nachtrag B124 — Auswertung des Produktionslogs vom 24.07.

Der Log ist von 4047 auf 23 Zeilen geschrumpft. Werkzeug-Rauschen,
"channel is not currently live" und die Telegram-Fehler sind weg.
Uebrig blieb EIN Ereignis (@tatjana335), doppelt geloggt. Daraus zwei Fixe:

**7. ffmpeg hämmerte 60 Sekunden gegen ein 404**
`-reconnect_on_http_error 4xx,5xx` schloss 404 und 403 ein. Beide sind bei
TikTok TERMINAL: die CDN-Pull-URL traegt ein `expire=<ts>` — nach Ablauf
oder Edge-Wechsel existiert sie nicht mehr, dieselbe URL erneut anzufragen
kann per Definition nie gelingen. Beobachtet: fuenf Reconnects ueber 60s,
danach Abbruch ohne eine Sekunde Material. Die einzige Rettung waere gewesen,
die Stream-URL NEU AUFZULOESEN — und genau das tut der Bot beim naechsten
Versuch, sobald ffmpeg schnell aufgibt.
Die eigene Diagnose-Empfehlung im Code sagte das laengst ("bei 404 schnell
aufhoeren statt zu haemmern"), nur die ffmpeg-Argumente folgten ihr nicht.
Jetzt: nur noch die wirklich voruebergehenden Codes 408,429,500,502,503,504.

Gegen echtes ffmpeg 6.1.1 geprueft: die Codeliste wird akzeptiert.
`-reconnect_delay_total_max` wurde bewusst NICHT ergaenzt — dieselbe Probe
zeigte "Unrecognized option", das haette JEDE Aufnahme gebrochen.

**8. Derselbe stderr wurde zweimal in voller Laenge geloggt**
handle_recording_finished und log_recording_failure gaben beide den
kompletten Block aus — zwei mal ~800 Zeichen fuer EIN Ereignis, die Haelfte
des verbliebenen Logvolumens. Jetzt: Diagnose-Zeile mit gekapptem Tail
(600 Zeichen), Kurzform daneben (400). Vollstaendig steht der stderr
weiterhin in recording_attempts.stderr_tail.

Zusaetzlich: 404/stream_dead laeuft jetzt als WARNING statt ERROR. Der
Verlust bleibt sichtbar, aber ein rotierender CDN-Edge ist kein Bot-Defekt
und gehoert nicht ins Fehlerlog.

## 8c. B125 — Datenzerstoerer in clean_username behoben

**9. "@www.tiktok.comrabi1978" ist ein ECHTER Handle, kein URL-Muell**

22 Zeichen, nur Buchstaben, Ziffern und Punkte — TikTok erlaubt Punkte im
Handle, also voellig gueltig. Der Name ist offenkundig genau so gewaehlt,
um automatische URL-Erkennung auszutricksen. Das ist gelungen:

  * `clean_username()` schnitt bei JEDEM Vorkommen von "tiktok.com" alles
    davor weg -> aus dem echten Handle wurde "rabi1978".
  * Die in B120 ergaenzte Start-Migration haette das in der DB
    festgeschrieben und, falls "rabi1978" ebenfalls getrackt wird, das
    Original ALS DUPLIKAT GELOESCHT.

Behoben:
  * `clean_username()` interpretiert nur noch, wenn es interpretieren DARF:
    Schema oder "/" vorhanden -> URL. Sonst "@" vorhanden -> alles bis zum
    letzten "@" weg (fuehrendes @ / verschluckter Slash). Sonst LITERAL.
    Ein Handle enthaelt per Definition weder "/" noch "@" — deshalb kann
    "www.tiktok.comrabi1978" gar keine URL sein und bleibt unangetastet.
    12 Faelle getestet, inkl. "tiktok.company" und "www.tiktok.com.official".
  * Die Migration ist ersetzt durch einen reinen BERICHT. Gemeldet wird nur,
    was ein Handle NIE sein kann (/ : ? Leerzeichen oder @ im Namen).
    Geaendert oder geloescht wird NICHTS.
  * NEU `/track_exact <name>` — uebernimmt den Namen buchstabengetreu, ganz
    ohne URL-Erkennung, mit Gueltigkeitspruefung gegen die TikTok-Regeln.
  * `/track` sagt jetzt, WENN es die Eingabe als URL gelesen hat, und
    verweist auf /track_exact. Vorher merkte man die Umdeutung erst am
    ausbleibenden Mitschnitt.
  * NEU `nc.textutil.is_valid_tiktok_username()` — 2-24 Zeichen, nur
    a-z A-Z 0-9 _ . , kein Punkt am Ende.

Falls die alte Migration schon gelaufen ist, pruefe:

    sqlite3 <deine>.db "SELECT id, username FROM trackings ORDER BY id;"

Fehlt der Handle, einmal neu anlegen:  /track_exact www.tiktok.comrabi1978

## 8d. B127 — Performance, zweite Runde

**Punkt 1 (Chromium-Overlay) entfaellt**: laeuft bei dir bereits als
RESTREAM_OVERLAY_MODE=text. Der teure html-Pfad wird gar nicht betreten.

**10. Vier weitere Log-Tabellen ohne Aufraeumung**
B122 kappte nur tiktok_checks. Ebenfalls unbegrenzt wachsend waren
event_log, ai_log, profile_snapshots und overlay_events.

Besonders: AI_LOG_RETENTION_DAYS=30 war definiert und dokumentiert, aber
NIRGENDS angewendet — es gab kein einziges DELETE FROM ai_log. Eine
Einstellung, die Aufraeumen suggerierte und nichts tat.

Behandlung je Tabelle, nicht pauschal:
  * event_log        -> loeschen aelter als 60 Tage
  * ai_log           -> loeschen aelter als AI_LOG_RETENTION_DAYS (wirkt jetzt)
  * profile_snapshots-> AUSDUENNEN statt loeschen: jenseits 30 Tagen bleibt
                        pro User und Kalendertag der juengste Snapshot.
                        Gemessen an 2880 Testzeilen: -65 %, Kurvenform
                        erhalten (genau 1 Wert je Tag), letzte 30 Tage
                        unangetastet.
  * overlay_events   -> aelter als 180 Tage, ABER kind='donation' NIE.
                        Diese Zeilen speisen das Spendenziel und die
                        Gegenprobe der Finanzamt-Auswertung. Im Test:
                        300 von 300 Spenden unberuehrt.

**11. Messung statt Blindjustage fuer Whisper, Polling und Transcode**
Fuer diese drei fehlten die Zahlen — auf deiner Maschine, nicht in meiner
Sandbox. Statt Defaults zu raten wird jetzt gemessen:

  * Whisper: Echtzeitfaktor (RTF = Rechenzeit / Audiolaenge) je Lauf,
    gleitender Mittelwert. RTF > 1 heisst, die Transkription ist langsamer
    als das Audio spielt -> Backlog staut sich. Warnung nach 5, 25 und 100
    solchen Laeufen mit konkretem Hinweis (WHISPER_MODEL=tiny).
  * Polling: Dauer jedes Live-Checks gegen SEIN Intervall. Ueberschreiten
    mehr als 20 % der Checks ihr Intervall (ab 50 Messungen), gibt es eine
    einmalige Warnung. Anlass: der Kommentar an _INFLIGHT_GUARD_SECS raeumt
    Worst-Case ~90s ein, das Live-Intervall steht auf 20s.
  * Restream: transcode-Status je Ziel plus speed/slow_ticks sichtbar.

Alles zusammen:

    curl -s localhost:8050/api/system/check_timing | jq

Jeder Block hat ein Feld "urteil" — "unauffaellig", "noch zu wenige
Messungen" oder ein konkreter Hinweis. Erst wenn dort ueber Tage etwas
anderes als "unauffaellig" steht, lohnt es, an den Werten zu drehen.

## 8e. B128 — Website und Dashboard

### Website (website/lafap_index.html)

**12. Sieben Platzhalter-Links waren live**
DEIN-INVITE und DEIN-KANAL zeigten ins Leere. Jetzt die echten Kanaele
aus deiner .env (Kick, YouTube, Twitch, Discord).

**13. Google Fonts wurde extern geladen**
Dabei uebertraegt der Browser jedes Besuchers dessen IP an Google, ohne
Einwilligung — fuer eine deutsche Seite mit Impressum und Datenschutz-
hinweis ein vermeidbares Risiko (LG Muenchen I, 20.01.2022, 3 O 17493/20).
Jetzt lokale @font-face-Einbindung mit preload. Externe Requests: 9 -> 7,
und die verbliebenen 7 sind ausschliesslich deine eigenen Social-Links.
Die Schriftdateien musst du einmalig ablegen — Anleitung in
website/FONTS.md. Bis dahin greift font-display:swap, die Seite bleibt
benutzbar, sieht nur weniger nach Terminal aus.

**14. Kein <h1>** (4x h2, 0x h1). Der Akronym-Block ist inhaltlich die
Hauptueberschrift und wird jetzt auch so ausgezeichnet; role="img" bleibt,
damit die Buchstabengrafik als Einheit vorgelesen wird.

**15. Kein <main>-Landmark** — ergaenzt.

**16. Kein og:image** — beim Teilen in Discord/WhatsApp/Telegram erschien
eine graue Karte. og:image + twitter:card (1200x630) ergaenzt; die Datei
og-card.png musst du noch anlegen (siehe FONTS.md).

### Dashboard (templates/dashboard.html)

**17. 27 Icon-Knoepfe ohne Beschriftung** — ein Screenreader las nur
"Schaltflaeche", Sprachsteuerung funktionierte nicht. Jetzt aria-label
UND title (letzteres hilft auch sehenden Nutzern als Tooltip).
aria-Attribute gesamt: 37 -> 64.

**18. Touch-Ziele unter 44px** — Apple und Google nennen beide 44px als
Minimum. Gebunden an @media(pointer:coarse) statt an eine Bildschirm-
breite: die Desktop-Dichte bleibt, ein Touch-Laptop profitiert trotzdem.
Auf einem Dashboard, das vom Handy bedient wird, kann ein Fehlgriff
heissen: falschen Restream gestoppt.

**19. Kein Sprunglink, kein sichtbarer Fokusring, kein main-Landmark**
Sprunglink "Zum Hauptinhalt springen" (nur bei Tastaturfokus sichtbar),
:focus-visible-Outline und <main id="hauptinhalt"> ergaenzt.

**20. Einziges <img> ohne alt** — alt="" gesetzt (Avatar ist dekorativ,
der Name steht daneben; leeres alt laesst Screenreader es ueberspringen).

## 9. Rollback

    sudo systemctl stop tiktok-bot
    cd ~/tiktok-bot && tar xzf ../nightcrawler_backup_<stamp>.tgz
    sudo systemctl start tiktok-bot

## 10. Was in diesem Build steckt

| Bereich | Ursache | Behoben |
|---|---|---|
| Discord tot | `client.start()` ohne Supervisor, Exception als WARNING geschluckt | Reconnect 5s->300s, Abbruch nach 5 erfolglosen Starts, Konfigfehler klar benannt |
| Discord-Loops | Guard hing am client-Objekt | modul-globaler Guard |
| `/brain` | Payload-Key `question` vs. Handler `prompt` | beide akzeptiert, Router-Trace statt "keine Antwort" |
| `/brain` | Kette nur `['llamacpp']` | `['llamacpp','freeai']`, Cloud-Reserve |
| `/ai` | ein globales Modell an alle Basen -> Rotation tot | Modell pro Base, 4 Basen, Key+Referrer, 402 als `auth` |
| Logspam | Offline-Kanal als ERROR, Client-Abbrueche als ERROR | beides DEBUG, stdout gekappt |
| Phantom-User | Altzeilen vor dem B76c-Fix | Startup-Normalisierung |
| Spenden | TikTok nur in einer Ansicht ausgeblendet | `REVENUE_PLATFORMS`-Gate, TikTok laeuft als `gift` |
| YouTube | Scrape, gerundete Abonnenten | Data API v3, exakte Werte, 60s Quota-Cache |
| YouTube verbinden | fehlte — Refresh-Token nur von Hand ueber die .env | Dashboard-Panel wie bei Twitch, Ein-Klick-Flow, selbst erneuernd |
| Finanzamt | fehlte | `nc/ledger.py`, append-only, Hash-Kette, CSV |
| Restream nach Neustart | nur auto_restream=1, sonst weg | persistierter Soll-Zustand, Wiederanlauf beim Start |
| Restream "online" trotz offline | status() meldete nur "Prozess lebt" | Plattform-Pruefung alle 120s + Neuaufbau |
| CPU-Last | 3 Full-Scans ueber eine unbegrenzt wachsende Tabelle im 5s-Takt | lean-Puls + TTL-Cache + Retention: 1164 ms -> 0,2 ms |

## 11. Grenze

Meine Testumgebung erreicht nur eine Domain-Allowlist — Pollinations, llm7.io,
OVH und die YouTube-API waren nicht erreichbar. Logik, Fehlerklassifikation und
Rotationspfade sind geprueft, die tatsaechliche Erreichbarkeit der Dienste nicht.
Deshalb Schritt 5 zuerst.

Das Einnahmen-Journal ist eine strukturierte Vorarbeit fuer dein Steuerbuero,
keine Steuerberatung. Zahlen gegen Kontoauszuege und Plattform-Abrechnungen
pruefen.
