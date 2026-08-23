## PWA: Dashboard als installierbare Android-App

Das Dashboard ist jetzt eine **Progressive Web App** — auf dem Handy per
"Zum Startbildschirm hinzufügen" installierbar, startet dann wie eine echte App
(Vollbild, eigenes Icon, kein Browser-Rahmen). Kein Play-Store, kein APK.

Bausteine:
- **manifest.webmanifest** — macht die App installierbar (Name, Icons, standalone-
  Modus, Theme-Farbe passend zum Dashboard). Route `/manifest.webmanifest`.
- **sw.js** (Service Worker) — Offline-Shell + schneller Start. Route `/sw.js`
  mit `Service-Worker-Allowed: /`, damit er die ganze App steuert.
- **App-Icons** (192/512/maskable) im Cyberpunk-Terminal-Stil (Phosphor-Orb mit
  Scan-Linien + HUD-Eckwinkel). Routen `/pwa-icon-*.png` mit Whitelist gegen
  Path-Traversal.

**Kritische Design-Entscheidung:** Der Service Worker cacht NIEMALS `/api/`-
Antworten — das ist ein Live-Kontrollpanel, gecachte API-Daten würden veralteten
Bot-Status zeigen (z.B. "live" obwohl offline). Nur die statische Shell wird
gecacht; bei Verbindungsverlust erscheint eine saubere Offline-Meldung statt des
Browser-Dinos. Die SW-Registrierung ist gekapselt und blockiert das Dashboard
nie, falls sie fehlschlägt.

**Installation auf dem Handy:** Dashboard im Chrome öffnen (über trevlix.dev,
nicht die lokale IP — PWA braucht HTTPS) → Menü → "Zum Startbildschirm
hinzufügen". Beide Dashboards (Haupt + Gehirn) sind eingebunden.

Deploy: die vier PWA-Dateien liegen in `templates/` neben dashboard.html —
`manifest.webmanifest`, `sw.js`, `pwa-icon-192.png`, `pwa-icon-512.png`,
`pwa-icon-maskable-512.png`.

## Tiefenbughunt: 3 echte Bugs gefunden & behoben

Tiefe Code-Analyse (nicht Test-Durchlauf) auf Race Conditions, Leaks,
ungefangene Fehler. Ergebnis: die Codebasis ist defensiver als erwartet — die
meisten Verdachtsfälle waren bereits abgesichert. Drei ECHTE Bugs gefunden:

1. **Cookie-Log-Spam (Klasse: Log-Flut).** `_load_cookies_dict` loggte bei
   Permission-denied bei JEDEM der 21 Aufrufer erneut — im Live-Log mehrere
   Warnungen/Sekunde (genau so beobachtet). Der Erfolgs-Cache griff nicht, weil
   die Datei nie gelesen wurde. Fix: Warnung gedrosselt (max alle 60s), Fehler
   selbst wird nicht verschluckt. Getestet: 50 Aufrufe → ≤2 statt 50 Warnungen.

2. **Race Condition (Klasse: dict changed during iteration).** Zwei Schleifen
   iterierten über `_RESTREAM_ACTIVE_ALL.items()` OHNE `list()`, während ein
   paralleler Task `.pop()` aufruft (Restream-Stop) → `RuntimeError`. Die
   anderen Iterationen im File nutzten bereits `list()`; hier fehlte es. Fix:
   `list()`-Schutz ergänzt.

3. **File-Handle-Leaks (Klasse: Ressourcen-Leck).** `/proc/meminfo` und
   `/proc/loadavg` wurden mit nacktem `open()` ohne `with`/`close()` gelesen —
   im Health-Loop summiert sich das gegen das fd-Limit. Plus `nc/confdrift.py`.
   Fix: alle drei auf `with`-Block.

BEWUSST NICHT "gefixt" (waren keine Bugs — verifiziert statt geraten):
`except Exception` um `asyncio.sleep` fängt KEIN CancelledError (erbt von
BaseException seit 3.8) → Shutdown sauber. Divisionen hatten durchweg
Leer-Guards. `win_done`-Division hatte bereits `if win_done else`. Kein
Aktionismus an funktionierendem Code.

## V37-REACTLIVE: Overlay-Feinschliff (Reaktion, Sprechblase, Donation-Box)

Drei Overlay-Änderungen aus dem Sende-Feedback:

1. **AZRAEL reagiert nur auf den restreamten User.** Vorher reagierten die
   Live-React-Worker auf ALLE getrackten Live-User (bis zu LIVE_REACT_MAX_USERS).
   Auf dem Sendebild sieht/hört man aber nur den restreamten Stream — Reaktionen
   auf andere waren verwirrend. Jetzt filtert der Worker gegen
   `_restream_active_sources()`: nur der gerade gesendete User erzeugt eine
   Sendebild-/Sprech-Reaktion. Schalter `AZRAEL_REACT_ONLY_LIVE` (Default 1).
   Sicherung: läuft KEIN Restream, wird nicht alles stummgeschaltet (Solo-Betrieb
   bleibt hörbar). Chat-Antworten sind unberührt.

2. **Sprechblase breiter + höher.** Von 300px auf 440px Breite, Schrift 13→15px,
   Höhe wächst mit dem Text (kein Abschneiden mehr). Zusätzlich die
   Server-Textgrenze `AZRAEL_OVERLAY_MAXLEN` von 240 auf 400 erhöht — sonst hätte
   die breitere Blase nichts gebracht, weil der Text schon vorher gekappt wurde.

3. **Donation-Box nach oben links** (unter den Titel, `top:130px`) — vorher unten
   links.

## V37-MAXLIVE: Max. gleichzeitige Restreams gedeckelt

Neuer Deckel `RESTREAM_MAX_CONCURRENT` (Default 2): Im Multi-Modus
(`RESTREAM_SINGLE=0`) werden höchstens so viele gleichzeitig live Nutzer
restreamt. Vorher war Multi unbegrenzt — bei vielen Live-Usern hätte pro User
ein ffmpeg-Encode gestartet und die CPU des GPU-losen Servers überrannt.

Der Deckel greift in `auto_start_due`: sobald `len(self._procs)` das Limit
erreicht, `break` — keine weiteren Starts. Single-Modus (genau 1 Restream)
bleibt unberührt. Getestet: 5 Live-User → nur 2 gestartet (Deckel 2), 3 bei
Deckel 3.

Voraussetzung für >1: eigene Ingest-Ziele/Keys pro Restream — zwei Restreams
auf denselben Kick-Slot würden sich gegenseitig stören.

## V37-NEXUSOUT: Nexus vollständig entfernt

Auf Wunsch komplett raus — AZRAEL Sentinel ist das eigenständige System, Nexus
war ein davon getrennter KI-Selbstbeobachtungs-Kern (NeuralCore: Lobes-Zustand,
Denkzyklen, Vorschlagsgenerator). Nichts übertragen.

Entfernt: NeuralCore-Klasse, `_NEXUS`-Instanz, `_nexus_loop`, alle vier Routen
(state/think/ask/propose), Env-Konfig (NEXUS_ENABLED/INTERVAL/USE_LLM), der
Startup-Spawn, das Dashboard-Panel + `nexusPropose`-JS + toter `_nx*`-State +
Nexus-CSS, und der .env.example-Block. Verifiziert: Bot startet sauber ohne
Nexus, alle Nexus-Routen sind 404, AZRAEL Sentinel (Shield, Timeouts,
Chat-Antworten) unberührt.

# NIGHTCRAWLER v37 — AI Operating System

bot_v36 + Brain-Layer (Module M1–M8). **Alle v36-Features bleiben vollständig
erhalten** — jeder Brain-Baustein ist additiv, fail-open und einzeln
abschaltbar. Ohne `brain/`-Verzeichnis startet bot.py exakt wie v36.

## Architektur

```
                    ┌──────────── bot.py (dein v36 + 3 Patches) ───────────┐
Telegram ⇄ Bot ⇄ Recorder/Restream/Loops ⇄ SQLite (bot-DB)   Flask-Dashboard   │
                    └───────────────┬──────────────────────────────┬───────────┘
                              (nur lesen)                    (Routen additiv)
                                    │                               │
                          brain_bridge.py  ──────────────►  /brain + /api/brain/*
                                    │
        ┌─────────── brain/ (eigene brain.db, isoliert) ────────────┐
        │ state.py      StateMachine — Systemspiegel, Transitions   │
        │ rules.py      Rules Engine — Tier 1, LLM-frei, Warum-Log  │
        │ router.py     Task-Router — rules→db→knowledge→llm        │
        │ memory.py     M3 Langzeitgedächtnis (Sessions/Metriken)   │
        │ knowledge.py  M4 Wissensgraph (Triple-Store, erklärbar)   │
        │ scheduler.py  M5 Prognosen + Poll-Hints                   │
        │ llm.py        M6 LLM-Runtime (llama.cpp → Ollama)         │
        │ agents.py     M7 AZRAEL-Flotte (health/recovery/scout/    │
        │               analytics/learning), einzeln schaltbar      │
        └───────────────────────────────────────────────────────────┘
```

## Scharf geschaltet (11.07.2026)
`.env` steht jetzt auf: `AI_PROVIDER=brain` + `REACTION_AI_PROVIDER=brain`
(Chat UND Live-React über llama.cpp:8080, Ollama nur noch Fallback),
Scheduler-Hints, Recovery-/DB-/Restream-Restart-Gates an, SENTINEL_SHIELD an.
**Serverseitig nötig:** `llama-server.service` installieren (liegt bei) und
Modell laden — sonst greift automatisch der Ollama-Fallback.

## Fehlerbehebungen aus dem Log vom 11.07.
| Fix | Symptom im Log | Lösung |
|---|---|---|
| B90 | Discord-Uploads ≤25 MB scheitern | Discord-Free-Limit ist seit 2023 **10 MB**; Default korrigiert, echtes `guild.filesize_limit` zur Laufzeit, 413→Not-Schrumpfen+Retry |
| B91 | 404-Serien (`stream_dead`, 27–60s ffmpeg-Burn alle 2 min) | Preflight-GET vor dem Spawn; `_hd/_uhd/_sd`-Suffix-Fallback (CDN-Quirk); alles 404 → kein Spawn |
| B92 | `WATCHDOG: live-react seit 422s ohne Lebenszeichen` | Reaction-KI-Calls hart auf `REACTION_AI_TIMEOUT` (75s) begrenzt + `provider=brain` (llama.cpp statt langsamem Ollama) |
| B93 | dito (Fehlalarme bei ruhigen Streams) | Heartbeat jetzt pro Loop-Iteration, nicht nur nach Reaktionen |

## Neue Schutzschicht: SENTINEL-SHIELD
Deterministische Anti-**Doxxing**- (Telefonnummern, IBAN, Wohnadressen,
Koordinaten, Klarnamen-Ansagen, E-Mail) und Anti-**Hate/Drohungs**-Erkennung
(Volksverhetzung inkl. Code-Zahlen mit Kaufkontext-Guard, Suizid-Aufforderung,
Gewaltandrohung) mit Leetspeak-/Tarnungs-Normalisierung — läuft VOR Banned-
Words und KI auf **Kick UND Discord**, kostet kein KI-Budget, erzwingt
Delete+Timeout unabhängig vom Automod-Modus. `SENTINEL_SHIELD=0` schaltet ab.

## Discord = Telegram (W-PAR)
15 neue Slash-Kommandos (`/sys_pause`, `/sys_resume`, `/sys_stoprec`,
`/sys_cleanup`, `/sys_quota`, `/sys_res`, `/sys_topusers`, `/sys_summary`,
`/sys_logs`, `/sys_diag`, `/sys_aireset`, `/sys_teststream`, `/sys_bulkadd`,
`/sys_live`, `/sys_cookies`) führen die **Original-Telegram-Handler** über
einen Update/Context-Shim aus — null Duplikate, TG-Fixes wirken automatisch
auch in Discord. Admin-Rolle erforderlich.

## Multi-Plattform-Restream: der ECHTE Fix + Mobile-Dashboard

**Warum es vorher nicht klappte (zwei Ursachen):**
1. **tee ohne onfail=ignore** — ein zickendes Zusatzziel riss den ganzen
   Fan-out ab (Kick ging mit offline). Behoben in nc/restream_targets.py.
2. **copy-Modus inkompatibel mit Multi-Target** — im Default (RESTREAM_
   TRANSCODE=0) teilt der tee denselben H.264-Bitstream an alle Ziele, aber
   Kick/Twitch/YouTube haben verschiedene Keyframe-/GOP-Anforderungen; mind.
   ein Ziel lehnt den Stream dann ab oder ruckelt. **Fix:** sobald ein
   Zusatzziel aktiv ist, wird transcode automatisch erzwungen — ffmpeg
   erzeugt ein plattformkonformes GOP (feste 2s-Keyframes via -g/-keyint_min/
   -sc_threshold 0), das Kick, Twitch UND YouTube gleichzeitig akzeptieren.

Damit läuft auf allen konfigurierten Plattformen gleichzeitig dasselbe Signal.
Kosten: transcode braucht CPU (kein GPU auf dem OVH-Server) — bei Bedarf
RESTREAM_BITRATE_K / RESTREAM_FPS senken.

**Scharf schalten:** in .env `TWITCH_ENABLED=1` + `TWITCH_STREAM_KEY=...`
(YouTube analog). Kick bleibt Primär, die anderen kommen als robuste tee-Ziele
dazu, transcode schaltet sich selbst ein.

## V37 Wellen 4-6: Fremdwerbung, Gehirn-Kurve, Llama-Budget

**Welle 4 — Fremdwerbung unterbunden.** `_detect_foreign_ad` erkennt fremden
Link/Invite/Eigenwerbung ("folgt mir", "check meinen Kanal", fremder discord.gg).
Die EIGENEN Kanäle/Discord sind per Allowlist frei — kritischer Fix: der eigene
Invite wird auf den VOLLEN Pfad geprüft (discord.gg/meinserver), nicht nur die
Domain, sonst gälte jeder discord.gg-Invite als eigen. Verdrahtet in `_spam_check`
(am `block_ads`-Schalter, `MOD_BLOCK_ADS`, Default an). Getestet: 6/6 Werbung
geblockt, 0 False Positives.

**Welle 5 — Gehirn-Dashboard mit echter Lernkurve.** Vorher zeigte `/api/brain`
nur Momentan-Status (aktiv/idle) — keine Entwicklung. Neu: Tabelle `brain_growth`
mit stündlichen Snapshots (Wissen/Vektoren/Nutzer/Sessions), Route
`/api/brain/growth?days=30`, und eine Multi-Linien-Wachstumskurve im
Brain-Dashboard. Zeigt endlich, wie das Gehirn über Zeit lernt und wächst.
Snapshots lesen die echten `knowledge.stats()`/`semantic.stats()`.

**Welle 6 — Llama.cpp-Budget erhöht.** Symptom: Antworten abgeschnitten UND
Timeouts — beides zusammen, weil bei CPU-Inferenz ohne GPU mehr Tokens mehr Zeit
brauchen. `BRAIN_LLM_TIMEOUT_S` 60→300s, `BRAIN_LLM_MAX_TOKENS` 512→1024,
Kontextfenster `-c` 4096→8192 in SETUP_LLAMACPP.md. Bewusst NICHT angefasst:
`REACTION_AI_TIMEOUT` (75s) bleibt kurz — die Live-Reaktion muss snappy sein,
sonst kehrt der Watchdog-Blockade-Bug zurück. Die Ressourcen-Abwägung (RAM,
ffmpeg-Vorrang, 4-Core-Grenze) ist im Setup dokumentiert statt blind
hochgedreht.

## V37-SHIELD-HARDEN (Welle 3): Sentinel gegen Umgehung gehärtet

Menschen umgehen Filter — der Shield normalisiert jetzt VOR der Prüfung deutlich
mehr Tricks weg. Neu in `_shield_normalize`:

1. **Unicode-Homoglyphen** — kyrillische/griechische Zeichen, die lateinisch
   AUSSEHEN (`ѕіеg hеіl` → `sieg heil`), werden zurückgebildet.
2. **Zero-Width- und unsichtbare Zeichen** — zwischen Buchstaben gestreut
   (`s\u200bieg`) werden entfernt.
3. **Akzent-/Diakritika-Tarnung** — NFKD-Zerlegung + Kombizeichen droppen
   (`síég héíl` → `sieg heil`).
4. **Trennzeichen-Tarnung erweitert** — auch `h-e-i-l` und vereinzelte
   Leerzeichen-Ketten (`s c h e i ß e`), aber NUR bei langen Einzelbuchstaben-
   Sequenzen, damit normale Sätze unangetastet bleiben.

Mindestlänge von 4 auf 3 gesenkt (fängt kurze Angriffe wie `kys`).

**Der kritische Teil — keine False Positives.** Bei Moderation ist ein zu Unrecht
bestrafter Zuschauer schlimmer als ein durchgerutschter Troll. Getestet: 0 False
Positives über harmlose Nachrichten inkl. Grenzfälle (`Sieglinde`, `1488 euro`,
`heiliger`, `e-mail`, `3.5 sterne`, echtes Kyrillisch). Normale Wortgrenzen
bleiben erhalten — `gut gemacht leute` verschmilzt NICHT.

Bewusste Grenze: vollständig vereinzeltes `s i e g h e i l` ohne Rest-Anker
wird nach dem Zusammenziehen von den `\b`-Wortgrenzen der Hate-Muster nicht
erfasst. Die Wortgrenzen bleiben streng, weil ihre Lockerung das
False-Positive-Risiko (jedes Wort mit „heil"/„sieg" darin) zu stark erhöht —
die richtige Abwägung bei Moderation.

## V37-CLEANUP + SENTINEL-REACH (Wellen 1-2)

**Welle 1 — Obsidian vollständig entfernt.** „Wir haben ein Gehirn, das reicht":
Obsidian-Integration (Definitionsblock, `_obsidian_append`-Aufrufe, zwei Routen,
Dashboard-Panel, .env-Block) restlos raus. Die umgebende Logik (Schimpfwort-Lernen,
Nexus-Vorschläge) bleibt — nur der Obsidian-Notiz-Nebeneffekt ist weg. Der
Nexus-Vorschlagsgenerator bleibt als reines Brain-Feature im Dashboard.

**Welle 2 — Sentinel-Chat-Reichweite komplett.** Fund: AZRAEL antwortete auf
@Azrael nur auf Twitch/YouTube — **Kick fehlte**, obwohl Hauptplattform (dort lief
nur die alte Frage-auto_reply, keine namentliche Ansprache). Jetzt antwortet
AZRAEL auf @Azrael in ALLEN Chats außer TikTok (Kick/Twitch/YouTube), über die
gemeinsame `_azrael_chat_should_reply`/`_azrael_chat_reply`-Logik mit
Shield-Screen. TikTok bleibt bewusst außen vor.

## V37-LOYALTY: Belohnungssystem (Punkte + Ränge)

Verwandelt die Wiedererkennung in echte Bindung. `nc/loyalty.py` — Stammzuschauer
sammeln Punkte fuer Stream-Treue und steigen in Raengen auf.

**Bewusst getrennt vom Discord-XP:** Das vorhandene `discord_xp` belohnt
Discord-CHAT. Loyalty belohnt Stream-TREUE — wer regelmaessig zuschaut und im
Live-Chat mitredet, sammelt Punkte, auch ohne je etwas im Discord zu schreiben.

- **Persistenz (kritisch):** Punkte liegen in der DB-Tabelle `loyalty_points`,
  NICHT im RAM. Ein Belohnungssystem, das beim Neustart vergisst, ist wertlos —
  ein Vertrag beweist, dass Punkte den Neustart ueberleben.
- **Punktequellen:** Live-Chat-Nachricht (mit Cooldown gegen Farming),
  Wiederkehr-Bonus (die Wiedererkennung feuert ihn).
- **Raenge:** Neuling (0) → Stammgast (100) → Bekanntes Gesicht (500) →
  Veteran (1500) → Legende (5000). Rangaufstiege werden im Sendebild + Discord
  gefeiert.
- Route `/api/loyalty/leaderboard`, Top-Liste im Community-Panel. Schalter
  `LOYALTY_ENABLED` + `LOYALTY_CHAT_POINTS`/`_COOLDOWN_S`/`_RETURN_POINTS`.

Die DB-Anbindung ist per configure() injiziert — das Modul kennt keine
DB-Details und bleibt testbar ohne Netzwerk/DB.

## V37-COMMUNITY: Discovery-Loop (Community-Ausbau)

Drei zusammenspielende Bausteine in `nc/community.py`, jeder einzeln schaltbar.
Antwort auf den genannten Engpass (Reichweite) + gewünschtes Feature
(Wiedererkennung):

1. **Stammzuschauer-Wiedererkennung** — merkt sich, wer schon im Chat war, und
   begrüßt Wiederkehrer im Sendebild + Discord. Bewusst konservativ: NIE
   Erstbesucher, erst nach echter Pause, ab N Besuchen, mit Cooldown. Verdrahtet
   im zentralen Chat-Choke-Point `_restream_chat_push` (alle Plattformen).
2. **Live-Ping** — beim frischen Restream-Start eine „ist LIVE"-Ankündigung nach
   Discord, mit optionalem Rollen-Ping. Entprellt über `_COMMUNITY_PINGED` gegen
   Reconnect-Spam (nur `_attempts == 0`, Reset beim Stop).
3. **Highlight-Share** — reißt ein Clip die Highlight-Schwelle, kommt zusätzlich
   zum bestehenden Telegram-Push ein teilbarer Discord-Beitrag mit Teilen-Aufruf.
   Der eigentliche Reichweiten-Motor.

Dashboard-Panel „Community" (bekannte Zuschauer, Stammgäste, welche Loop-Teile
aktiv). Route `/api/community/stats`. Schalter in `.env`
(`COMMUNITY_*_ENABLED`), alle brauchen `DISCORD_WEBHOOK_URL`.

**Ehrlich zur Reichweite:** Der stärkste Discovery-Hebel bei TikTok-Live ist die
Plattform selbst (Algorithmus, Hashtags, Zeiten) — das kann kein Bot direkt
beeinflussen. Was der Bot beiträgt: vorhandenen Content maximal teilbar machen
und die bestehende Community aktivieren. Das ist realistisch der technische
Anteil.

## V37-TWINGEST: tee-Restream-Bug war die veraltete Twitch-Ingest-URL

**Gelöst — und ehrlich zum Weg dahin.** Restreams brachen im tee-Modus mit rc=8
ab. Ich hatte ZWEI Fehldiagnosen: erst ein vermeintliches tee-Escaping-Problem
(gegen echtes ffmpeg widerlegt — der tee-Muxer parst rtmps://host:443 im
exec-Kontext korrekt), dann eine vermutete Codec-Fehlklassifikation (im Log
nicht bestätigt). Die echte Ursache fand sich durch Nachschlagen der aktuellen
Twitch-Ingest-Server: die .env nutzte `rtmp://live.twitch.tv/app` — eine
veraltete generische URL, die Twitch nicht mehr sauber annimmt. Weil der Primär
(Kick) im tee kein onfail trägt, riss das den ganzen Fan-out ab.

Fix: Default auf `rtmp://ingest.global-contribute.live-video.net/app` (globaler
Ingest, Twitch leitet an einen nahen Server weiter). In der Praxis bestätigt —
der Wechsel behob es. Der alte Wert ist raus, ein Vertrag verhindert seine
Rückkehr.

**Lehre (zum wiederholten Mal bei Twitch):** erst die aktuellen Fremdsystem-Fakten
nachschlagen, dann diagnostizieren — nicht am Code raten, während die Ursache
eine veraltete URL in der Config ist.

## V37-TWFIX: Kanal-Status hing noch am alten Token

Der Screenshot zeigte im Twitch-Panel „TWITCH_CLIENT_ID + TWITCH_EVENTSUB_TOKEN
nötig", obwohl der OAuth-Flow verbunden war. **Mein Fehler beim OAuth-Umbau:**
ich hatte den EventSub-Loop UND den Chat-Loop auf OAuth umgestellt, aber die
Kanal-Status-Route (`_twitch_channel_status`, liefert Live/Zuschauer/Follower
fürs Dashboard-Panel) übersehen — die las weiter nur den alten
`TWITCH_EVENTSUB_TOKEN` aus der .env.

Behoben: dieselbe Token-Quelle wie die anderen Loops (OAuth bevorzugt,
.env-Token als Fallback). Die Fehlermeldung verweist jetzt auf „Twitch
verbinden" statt auf den manuellen Token. Zwei Verträge sichern das ab.

## V37-TWMOD: SENTINEL timeoutet auf Twitch + Token-Speicherung

**Zum Token in der .env:** Auf den Wunsch, `TWITCH_EVENTSUB_TOKEN` automatisch in
die .env zu schreiben, rate ich bewusst ab — das wäre der falsche Weg:
- Es wäre der kurzlebige **Access**-Token (~1h), beim nächsten Start längst tot.
  Der Bot speichert stattdessen den **Refresh**-Token (in
  `recordings/twitch_oauth.json`) und erneuert daraus selbst.
- `load_dotenv()` würde beim Start einen festen .env-Wert laden und den frischen
  aus dem Refresh **überschreiben** — genau der Fehlertyp aus V37-TWOAUTH-FIX.
  Das 60-Tage-Ablaufproblem käme zurück.
- Ein Bot, der die .env (mit allen anderen Secrets) zur Laufzeit schreibt, ist
  ein Risiko.

Der Token wird also bereits automatisch gespeichert — am richtigen Ort, im
richtigen Format, selbst-erneuernd. Der EventSub-Loop bevorzugt ihn und nutzt
`TWITCH_EVENTSUB_TOKEN` nur noch als Fallback (mit Log-Hinweis, welcher aktiv
ist).

**SENTINEL auf Twitch:** Der OAuth-Flow holt jetzt zusätzlich
`moderator:manage:banned_users`. Damit kann SENTINEL harte Verstöße
(Doxxing/Hate, via `_sentinel_screen`) auf Twitch **timeouten** — über die
Helix-API (`/moderation/bans`), am **selben Auto-Moderate-Schalter** wie Kick.
Sentinel an/aus im Dashboard gilt jetzt für beide Plattformen.

Damit deckt EINE Twitch-Autorisierung alles ab: Follower-Zähler, AZRAEL-Chat
(lesen/schreiben) und SENTINEL-Timeouts. Nach dem Deploy einmal neu autorisieren
(die neuen Scopes brauchen frische Zustimmung).

## V37-TWCHAT: EIN Twitch-OAuth für Follower UND Chat, AZRAEL antwortet

**Henrys Idee, direkt umgesetzt:** Der „Twitch verbinden"-Flow beschafft den
Chat-Token gleich mit. Der OAuth-Flow fragt jetzt drei Scopes an —
`moderator:read:followers` (Follower-Zähler) plus `chat:read` + `chat:edit`
(AZRAEL liest und schreibt im Twitch-Chat). **Eine Autorisierung deckt beides**,
selbst-erneuernd, kein separater Token mehr.

- Der Twitch-Chat-Loop nutzt den OAuth-Token (mit manuellem `TWITCH_CHAT_TOKEN`
  als Fallback). Der IRC-NICK kommt aus `login_name()` — Twitch verlangt, dass
  NICK = der autorisierte Account ist.
- **AZRAEL antwortet jetzt auf Twitch- UND YouTube-Chat** (vorher nur Kick).
  Bewusst konservativ: nur wenn `AZRAEL_CHAT_REPLY=1`, nur bei direkter Ansprache
  (`@azrael`/`azrael`), mit globalem Cooldown (`AZRAEL_CHAT_REPLY_COOLDOWN_S=20`),
  und der SENTINEL-SHIELD screent VOR der Antwort — auf toxische Nachrichten
  antwortet AZRAEL nicht (die moderiert der Bot separat).
- YouTube braucht zum Senden weiter das `YOUTUBE_REFRESH_TOKEN` (Google-OAuth,
  getrennt von Twitch) — das kann Twitch-OAuth nicht mitliefern, das ist ein
  anderer Anbieter. Ist es gesetzt, antwortet AZRAEL auch dort.

**Ehrlich zur Reichweite:** „Sentinel im Control-Tab nutzt den Token ebenfalls"
— die Moderation (`_sentinel_screen`) ist plattformneutral und screent jeden
Text; die AZRAEL-Antwort im Chat läuft jetzt über denselben OAuth-Token. Der
Timeout-Vollzug bei Twitch (User sperren) wäre noch ein eigener Schritt über die
Twitch-API — der Chat-Token allein sendet Nachrichten, für Moderations-Aktionen
bräuchte es zusätzlich den Scope `moderator:manage:banned_users`. Sag Bescheid,
wenn AZRAEL auf Twitch auch timeouten soll, dann ergänze ich den Scope.

## V37-AZHIDE: AZRAEL aus dem Sendebild, Chat bleibt

**Wichtige Architektur-Klarstellung.** AZRAEL hat zwei getrennte Verhalten, die
oft verwechselt werden:
1. **Overlay-Reaktion** — reagiert auf den TikTok-Live-TON (Whisper-Transkript)
   und wird ins Sendebild gebrannt (die sichtbare Sprechblase).
2. **Chat-Antworten** — beantwortet/moderiert Chat (`_KICK_MOD._handle` →
   `send_message`). Getrennter Pfad.

**Neu:** `AZRAEL_OVERLAY_REACT=0` macht AZRAEL im Stream unsichtbar (die
react-Zeile bleibt leer), ohne die Chat-Antworten zu berühren. `LIVE_REACT_ENABLED=0`
stoppt zusätzlich die Reaktion auf den TikTok-Ton an der Quelle.

**Ehrliche Einschränkung — Cross-Platform-Chat-Antworten:** AZRAEL *beantwortet*
heute nur **Kick**-Chat. Twitch- und YouTube-Chat werden im Overlay nur
*angezeigt* (`_restream_chat_push`), lösen aber keine AZRAEL-Antwort aus. „AZRAEL
soll auf Twitch/YouTube-Chat antworten" ist deshalb **neue Arbeit**, kein
Schalter — der Antwortpfad existiert für diese Plattformen noch nicht. Das wäre
ein eigener Baustein (Chat-Nachricht → `_KICK_MOD.react()` → zurück in den
jeweiligen Chat), den ich bei Bedarf sauber baue.

## V37-DON-FIX: TikTok aus dem Donation-Panel

Auf Wunsch zeigt das Panel nur noch Kick/Twitch/YouTube. Die TikTok-Donations
werden weiter erfasst (in overlay_events), nur nicht mehr angezeigt — weder in
den Zählern noch in der Verlaufsliste (`platform != 'tiktok'`).

## V37-DON: Donations-Panel + alle vier Plattformen

**Klarstellung vorweg:** YouTube und Twitch werden für Donations bereits
unterstützt — sie nutzen denselben Pfad wie Kick/TikTok
(`_overlay_push("donation", …, platform=…)` → `overlay_events`). Twitch bucht
Bits und Subs über den Twitch-Chat-Listener, YouTube die Superchats über die
YouTube-Chat-Anbindung. Was fehlte, war die **Sichtbarkeit**: kein Panel zeigte,
was reinkommt.

**Neu:** `/api/donations/summary?days=30` aggregiert `overlay_events` nach
Plattform (alle vier, auch mit 0), plus die letzten 15 Einzeldonations. Panel im
System-Tab mit vier Zählern und Verlaufsliste. Zeigt eine Plattform 0, ist ihre
Quelle (noch) nicht verbunden — bei Twitch/YouTube hängt das an Chat- bzw.
OAuth-Anbindung, nicht am fehlenden Code.

Zwei Testverträge belegen, dass alle vier Plattformen in der Aggregation
auftauchen und dass Twitch- wie YouTube-Donation-Pushes existieren.

## V37-SEC: .env nicht mehr im Deploy-Paket

Das Zip enthielt bisher die echte `.env` mit Twitch-Credentials. Ab jetzt kommt
nur noch `.env.example` mit — die echte `.env` wird beim Paketbau ausgeschlossen.

## V37-TWOAUTH: Twitch-OAuth statt manuellem Token

**Motiv aus der Praxis.** Der Follower-Zähler brauchte einen von Hand erzeugten
`TWITCH_EVENTSUB_TOKEN` — mit drei Dauerproblemen, die alle in einer
Support-Session aufschlugen:
1. Der Token muss an die richtige Client-ID gebunden sein. Ein Token vom
   Generator gehört zu DESSEN öffentlicher Client-ID, nicht zur eigenen — passt
   dann nicht zur `.env` und liefert 401.
2. Er braucht Scope `moderator:read:followers`. Fehlt der, bleibt der Zähler leer.
3. Er läuft nach ~60 Tagen ab und friert den Zähler still ein.

**Der Flow ersetzt das:** Nutzer trägt nur `TWITCH_CLIENT_ID` +
`TWITCH_CLIENT_SECRET` ein und klickt im Dashboard **Twitch verbinden**. Der Bot
holt über den OAuth-Code-Flow einen Refresh-Token und erneuert den Access-Token
danach selbst — dauerhaft. Die Client-ID-Bindung ist automatisch korrekt, weil
die Autorisierung gegen genau diese App läuft.

- `nc/twitchoauth.py`: `authorize_url()` / `exchange_code()` für den einmaligen
  Browser-Flow, `access_token()` als selbst-erneuerndes Gegenstück zu
  `_yt_access_token()`. Refresh-Token wird unter `RECORDINGS_DIR` mit **0600**
  persistiert (nie der kurzlebige Access-Token).
- Drei Routen: `/api/twitch/oauth/status`, `/start` (→ Twitch-Dialog),
  `/callback` (Code-Tausch, mit CSRF-`state`-Prüfung).
- Dashboard-Panel im System-Tab: zeigt fehlende `.env`-Werte an oder den
  Verbinden-Knopf, pollt nach Rückkehr den Status.
- Der EventSub-Loop bevorzugt den OAuth-Token, hält aber den manuellen
  `TWITCH_EVENTSUB_TOKEN` als Fallback für Bestands-Setups. Token wird pro
  Reconnect erneuert (ein langer Lauf überdauert die ~1h Access-Token-Lebensdauer).

Anleitung: `SETUP_TWITCH_OAUTH.md`. Scope bleibt minimal (nur
`moderator:read:followers`, kein Overreach).

**Zwei eigene Fehler beim Bauen gefangen:** (1) eine lokale Variable `html`
verdeckte das `html`-Modul, sodass `html.escape` eine Zeile darüber scheiterte —
umbenannt zu `page`. (2) Der EventSub-Loop baute die Auth-Header einmal VOR der
`while`-Schleife; bei OAuth wäre der Token nach einer Stunde abgelaufen und jeder
Reconnect hätte den alten weiterverwendet — Refresh in die Schleife gezogen.



### V37-TWOAUTH-FIX2: Twitch will HTTPS — IP geht nicht

Zweiter Praxistest: `https://217.182.138.35:8050/...` scheiterte. Recherche
bestätigt: Twitch verlangt bei Redirect-URLs HTTPS, mit genau einer Ausnahme —
`http://localhost:PORT`. Eine nackte IP mit HTTPS ist unmöglich (kein Zertifikat
für IPs). Mein request-basierter Ansatz aus FIX war also selbst falsch: er
erzeugte genau die abgelehnte `https://IP`-Form.

Fix: Default zurück auf `http://localhost:3000/api/twitch/oauth/callback` (Twitchs
einzige HTTP-Ausnahme), das der Nutzer per SSH-Tunnel (`ssh -L 3000:localhost:8050`)
auf den Bot legt. Der Flow läuft dann komplett über localhost:3000. Das
Dashboard-Panel zeigt den fertigen Tunnel-Befehl und die einzutragende URL.
`TWITCH_REDIRECT_URI` überschreibt für Nutzer mit echter Domain + HTTPS.

Lehre: erst die Fremdsystem-Regeln prüfen (hier: was Twitch bei Redirects
akzeptiert), dann die Lösung bauen — nicht umgekehrt.

### V37-TWOAUTH-FIX: localhost:3000 → Dashboard-Adresse

Erster Praxistest scheiterte: Twitch autorisierte korrekt, aber der Redirect auf
`http://localhost:3000` lief auf dem Handy ins Leere (ERR_CONNECTION_REFUSED) —
`localhost` ist das Gerät mit dem Browser, nicht der Server mit dem Bot.

Fix: Die Redirect-URI wird aus `request.host_url` abgeleitet — der Callback
landet automatisch wieder am Dashboard, unter genau der Adresse, über die der
Nutzer es erreicht. `TWITCH_REDIRECT_URI` ist jetzt standardmäßig **leer**;
gesetzt überschreibt es (für Server hinter Proxy mit anderer externer URL).

**Eigener Fehler dabei:** meine zuvor ergänzte `.env`-Zeile
`TWITCH_REDIRECT_URI=http://localhost:3000` hätte den Fix ausgehebelt —
`load_dotenv()` hätte den festen Wert erzwungen. Genau der Config-Drift-Fehlertyp,
gegen den ich das confdrift-Modul gebaut hatte. In allen .env geleert.

Das Dashboard-Panel zeigt die exakte URL an, die in der Twitch-App unter OAuth
Redirect URLs stehen muss — Twitch prüft sie strikt.

## V37-OVFIX: AZRAEL-Reaktion im Sendebild abgeschnitten

**Aus zwei echten Screenshots diagnostiziert.** Die AZRAEL-Reaktion im
gebrannten Restream-Overlay (`RESTREAM_OVERLAY_MODE=html` → drawtext) wurde
mitten im Satz abgeschnitten, mit hängendem Komma und ohne jeden Hinweis, dass
da noch etwas fehlte.

**Ursache, per Playwright-Render und Geometrie-Rechnung bestätigt:**
`_ov_wrap(f"AZRAEL ▸ {txt}", 38, 2)` brach auf **2 Zeilen à 38 Zeichen** um und
warf den Rest **still weg**. AZRAELs Antworten sind bis zu 140 Zeichen lang —
es wurden also ~76 gezeigt, der Rest verschwand. Die Breite 38 ist korrekt (sie
passt zum engeren Portrait-Panel, das sich mit Landscape dieselbe drawtext-Datei
teilt), aber 2 Zeilen sind zu wenig.

**Fix:**
- `_ov_wrap` bekommt `ellipsis=True`: passt der Text nicht, endet die letzte
  Zeile mit »…« statt den Rest wegzuwerfen. Der Zuschauer sieht jetzt, dass es
  weitergeht.
- 3 statt 2 Zeilen (`AZRAEL_OVERLAY_WRAP_LINES`), Breite per
  `AZRAEL_OVERLAY_WRAP_W` steuerbar. ~114 statt ~76 Zeichen.
- Über-lange Einzelwörter (URL, langer Name) werden hart umgebrochen, damit
  nichts über den Bildrand läuft — vorbestehende Schwäche, gleich mitbehoben.
- Portrait-react von der Marken-Zeile nach OBEN verankert (`y=H-th-58` statt fix
  `H-132`), damit die 3. Zeile nicht in den Marken-Schriftzug läuft. Landscape
  war mit `y=h-th-30` schon th-basiert.

**"Der Verwendungszweck fehlt":** Der Zuschauer sah `AZRAEL ▸ ...` ohne zu
wissen, was AZRAEL ist. Das Präfix ist jetzt `AZRAEL_OVERLAY_PREFIX`, Default
`AZRAEL · KI-COHOST ▸` — es erklärt sich im Sendebild selbst und ist per Env
frei änderbar (z.B. `AZRAEL · KI-MOD ▸`).

Fünf Testverträge (`test_overlay_react_wrap`): Ellipse nur beim echten
Abschnitt, kurzer Text unverändert, keine Zeile über der Breite (auch nicht bei
Extremwort), bestehende Aufrufer unberührt.

**Selbst gefangen:** beim Umbau von `_ov_wrap` blieb ein `enumerate` ohne
genutzten Index stehen (B007). Die Testsuite lief grün, aber ruff fand es —
entfernt.

## V37-UI: Design-Durchgang am Dashboard

**Die Diagnose war nicht die erwartete.** Das Dashboard wirkte nicht
selbstgebaut, weil Blur-Effekte oder Gradients fehlten, sondern wegen dieser
Zahlen:

| | vorher | jetzt |
|---|---|---|
| Schriftgroessen | **26** (7, 7.5, 8, 8.5, 9, 9.5, 10, 10.5, 11, 11.5, 12 …) | **8 Tokens** |
| Radien | 9 | **3 Tokens** |
| Ladezustaende | 33 Panels zeigten »…« | Skeleton-Shimmer |
| Zahlen | sprangen | zaehlen (Count-Up) |
| Font-Requests | Orbitron 2x geladen | 1x |

Premium-Software sieht nicht teuer aus, weil sie *mehr* Effekte hat, sondern
weil sie **weniger Entscheidungen** hat, konsequent durchgezogen. 26
Schriftgroessen sind keine Gestaltung, das ist Rauschen.

Die Umstellung lief per Nearest-Neighbor, damit sich optisch wenig verschiebt:
174 font-size- und 53 border-radius-Ersetzungen.

**Die 26 @media-Bloecke blieben unberuehrt** (11.410 Zeichen). Dort steht
bewusste Mobile-Abstimmung: `.cmdbar input{font-size:16px}` verhindert, dass
iOS beim Fokussieren zoomt; die 44px-Touch-Targets sind Absicht. Ein
mechanischer Durchlauf haette beides zerstoert.

### Der Fund: 83 tote Style-Deklarationen

`--green` (39x) und `--mag` (44x) wurden benutzt, waren aber **nirgends
definiert** — Altlast-Namen fuer `--neon` und `--magenta`. CSS verwirft
ungueltige Werte still, also fiel es nie auf:
- `.azr-budget>i{background:linear-gradient(90deg,var(--green),var(--amber))}` → **kein Gradient**
- `.notif-badge{background:var(--mag)}` → **kein Hintergrund**

Kein Linter sieht das. Erst der Abgleich »benutzte Tokens gegen definierte«
bringt es hoch. 83 Stellen repariert.

### Was NICHT gemacht wurde — und warum

Die Vorlage forderte React-Hooks, Memoization, Code-Splitting, Bundle-Size und
ein GPU-Widget. Nichts davon passt: das Dashboard ist **eine HTML-Datei mit
Vanilla-JS** (229 Funktionen, kein Bundler, direkt von Flask ausgeliefert), und
der Server hat **keine GPU**. Widgets fuer Revenue/Subscriber/Goals waeren
Attrappen — die Daten existieren nicht.

Ebenso wurde die CSS **nicht weggeworfen**. Sie hatte bereits ein Token-System,
`:focus-visible`, `prefers-reduced-motion` und durchdachte Mobile-Arbeit. Das
STUDIO-Theme (Default) hatte die Farbdisziplin schon: neutraler Text statt
gruenem, gedaempfte Akzente, Glows durch Schatten ersetzt. Ein Neubau waere
Vandalismus an funktionierender Arbeit gewesen.

### Skeleton + Count-Up ohne Eingriff in die Render-Funktionen

Beides haette naiv bedeutet, ~229 Funktionen anzufassen — viel Aenderungsflaeche
fuer wenig Effekt, jede vergessene Stelle ein Bruch.

- **Skeleton**: der Shimmer haengt an den `<i>`-Kindern. Sobald eine
  Render-Funktion `innerHTML` setzt, verschwinden sie und `.skel` ist inert.
- **Count-Up**: ein MutationObserver sieht jede Textaenderung an `.metric .v`,
  egal welche Funktion sie ausgeloest hat. Neue Panels bekommen das Verhalten
  automatisch. Bewusst zurueckhaltend: nur reine Zahlen (Einheiten, Zeiten und
  »—« werden ignoriert, 10/10 Testfaelle), max. 420ms, und bei
  `prefers-reduced-motion` gar nicht — eine Animation, die den Blick auf den
  Wert verzoegert, waere in einem Kontrollraum ein Fehler.

## V37-DRIFT: .env gegen Code-Default

**Warum das existiert — drei echte Faelle, alle in EINER Session:**

| Schluessel | was passierte | Kosten |
|---|---|---|
| `RESTREAM_OVERLAY_HTML_SIZE` | .env feste Groesse, Default `auto` | Overlay verzerrt, mehrere Runden Fehlersuche |
| `RESTREAM_MULTI_MODE` | .env `independent`, Default `tee` | doppeltes Encoding, halbe Encoder-CPU verschenkt |
| `LIVE_REACT_ENABLED` | Default 0, .env 1 | zwei Falschaussagen ueber den Systemzustand |

Dreimal dieselbe Ursache ist kein Zufall. Das Muster: `os.getenv("X", "default")`
kollabiert zur Laufzeit. Steht in der .env etwas anderes, ist der Default
unsichtbar — und niemand merkt, dass eine Einstellung die Absicht des Codes
aushebelt.

**`nc/confdrift.py`** liest die Quelldatei zur Laufzeit selbst und gewinnt die
Defaults per AST zurueck (`os.getenv`, `_env_int`, `_env_int_range`). Damit gibt
es **keine zweite Liste**, die man pflegen und vergessen koennte — die Pruefung
bleibt automatisch aktuell. Defaults, die keine Konstanten sind, werden als
`<dynamisch>` markiert statt falsch geraten.

Gefiltert wird zweifach: Secrets/Pfade (`IGNORE`) sind erwartbar gesetzt und
keine Drift. Und gezeigt wird per Default nur die `WATCHLIST` — Schluessel, bei
denen eine Abweichung Verhalten oder Last spuerbar aendert. Gegen die echte .env:
**5 relevante von 45** Abweichungen. Eine Wand aus 45 liest niemand, und was
niemand liest, warnt nicht.

- Beim Start: einmal `log_watchlist_drift()` in `main()`
- Route: `/api/system/config_drift` (`?all=1` fuer alle)
- Panel im System-Tab

**Abweichung ist nicht automatisch falsch** — `RESTREAM_BITRATE_K=4500` statt
6000 ist eine bewusste, richtige Entscheidung. Der Punkt ist Sichtbarkeit, nicht
Bevormundung.

## V37-DISC: Disconnects der getrackten Streams

**Erst messen, dann fixen.** Die Tabelle `recording_attempts` protokolliert seit
jeher JEDEN Aufnahmeversuch mit Dauer, Returncode, Outcome und den letzten 1500
Zeichen ffmpeg-stderr — ausgewertet hat das nie jemand. Es wurde also über
Disconnect-Ursachen geraten, statt sie abzulesen.

**Neu: `nc/recdiag.py` + `/api/recordings/disconnects?days=7[&user=x]`** +
Panel im System-Tab. Es beantwortet:
- Welche Abbruchgründe dominieren, und bei welchem User?
- Was sagt das ffmpeg-stderr **wirklich** — 403 (Datacenter-IP-Block), 404
  (URL abgelaufen), Timeout (Tunnel instabil), kaputter Bitstream?
- Wie viele "Aufnahmen" endeten unter 60s (= keine Streams, sondern Fehlschläge)?

Die stderr-Klassifikation ist der ehrlichste Teil: sie liest, was ffmpeg gesehen
hat, statt unsere eigene Outcome-Kategorie zu wiederholen.

### Der Fund: 20 Sekunden fehlende Aufnahme, alle 28 Minuten

TikToks Stream-URL trägt ein `expire=`-Token (~30min TTL). Der
`_url_refresh_watchdog` beendet ffmpeg absichtlich 120s vorher (SIGTERM →
MP4 wird sauber finalisiert) und lässt neu starten — soweit richtig.

**Aber:** danach fiel der Code in den Normalpfad und wartete das reguläre
Live-Intervall ab (`ADAPTIVE_INTERVALS["live"] = 20`). Der User ist dabei
nachweislich noch live — das Warten ist grundlos. Bei einem 3h-Stream sind das
6 Schnitte × 20s = **2 Minuten fehlende Aufnahme ohne jeden Grund**.

Fix: nach einem `url_refreshed`-Schnitt wird `_NEXT_CHECK_AT[tid] = 0` gesetzt
(sofort fällig). AST-geprüft, dass kein späteres `_schedule_next_check` — weder
in `handle_recording_finished()` noch beim Aufrufer — die 0 wieder überschreibt.

### Chat-Guardian: bis zu 30s toter Chat pro Abbruch

`_restream_chat_guardian` pollte stur `await asyncio.sleep(30)`. Ein Listener,
den TikTok nach 5 Minuten normal getrennt hatte (die WS-Verbindungen rotieren),
blieb dadurch bis zu **30 Sekunden** tot, bevor der nächste Tick es überhaupt
bemerkte. Kein Backoff: bei Dauerfehlern hämmerte er im 30s-Takt und verbrannte
Sign-Quota.

Jetzt wird auf den Task **gewartet** — bricht die Verbindung, steht der
Reconnect sofort. Gegenstück: hält eine Session länger als `CHAT_FLAP_S` (10s),
gilt sie als gesund → sofortiger Reconnect, Backoff zurück auf 0. Fällt sie
früher, wächst der Backoff exponentiell (5→10→20→40→80→160→300s Deckel), denn
jeder `connect()` kostet Sign-Quota.

### Chat-Telemetrie pro User

`_CHAT_DIAG` war EIN globales Dict für alle User — mehrere Listener
überschrieben sich gegenseitig, und es gab keine Historie. Neu: `_CHAT_STATS`
pro User mit Connects, Failed, Disconnects, Flaps, Session-Dauern (Median/
kürzeste/längste), Abbruchgründen und **Uptime-Quote** — der ehrlichste
Einzelwert.

Fünf Testverträge halten das fest (`test_url_refresh_no_wait`,
`test_chat_guardian_reconnect`), inklusive der AST-Prüfung gegen das
Überschreiben.

## V37-PERF: der zweite Durchgang (Load 113 → 7.15 → ?)

Nach dem Thread-Deckel: Load **113 → 7.15**, Threads **812 → 325**, Swap sauber.
Aber 7.15 auf 8 Kernen ist "busy", nicht entspannt — und die Messung lief bei
3:49 Uptime mit *steigender* Load (7.15/3.72/1.5 = 1m/5m/15m), also im Hochlauf.

### Der grosse Fund: doppeltes Encoding

`RESTREAM_MULTI_MODE` steht im Code auf **`tee`**, in der Produktions-.env aber
auf **`independent`**. Mit `TWITCH_ENABLED=1` bedeutet das:

| Modus | Encodes | TikTok-Pulls | Encoder-Threads |
|---|---|---|---|
| `independent` (.env) | **2** | **2** | **5** |
| `tee` (Code-Default) | **1** | **1** | **3** |

Der unabhängige Relay zieht die TikTok-Quelle **ein zweites Mal** und encodiert
sie **komplett neu** für Twitch. Dasselbe Bild, doppelt gerechnet.

Der `tee`-Muxer macht EINEN Encode und fächert auf alle Ziele auf — mit
`onfail=ignore` pro Ziel, d.h. **Kick bleibt live, wenn Twitch klemmt**. Genau
die Absicherung, für die `independent` vermutlich gesetzt wurde, gibt es dort
also auch. Am geladenen Bot verifiziert, nicht behauptet.

Derselbe Fallentyp wie B102 (`RESTREAM_OVERLAY_HTML_SIZE`): die .env hebelt den
Code-Default aus, und niemand merkt es.

`RESTREAM_MULTI_ALLOW_COPY=0` bleibt dagegen **richtig** — Kick/Twitch/YT
brauchen ein plattformkonformes GOP; ein reiner Copy-Fanout lässt mindestens
eine Plattform ruckeln.

### Was schon optimal war
`faster-whisper` mit `compute_type=int8` und gedeckelten `cpu_threads` — die
schnellste CPU-Variante, da ist nichts zu holen.

### uvloop + orjson (optional)
- **uvloop**: libuv statt Python-Event-Loop. Wird in `_install_fast_eventloop()`
  VOR `asyncio.run(main())` gesetzt (danach wäre es wirkungslos), ist per
  `USE_UVLOOP=0` abschaltbar und fällt bei fehlendem Paket sauber zurück.
- **orjson**: als Flask-JSON-Provider. **Gemessen: 14.6x schneller** bei einer
  255-KB-Archiv-Antwort (2.84 ms → 0.19 ms).

**EHRLICHE EINORDNUNG:** beide beschleunigen die **Python-Seite**. orjson spart
~0.12 s CPU pro Minute; ein x264-Encoder verbraucht in derselben Minute ~180 s.
Das Dashboard wird spürbar flotter, die Encoder-Last bleibt gleich. Der
`tee`-Wechsel spart eine ganze Encoder-Instanz — das ist die Größenordnung, die
zählt.

**Beim Bauen selbst gefangen:** der erste orjson-Provider hatte `default=str`.
Damit wird eine nicht serialisierbare `sqlite3.Row` still zu
`"<sqlite3.Row object at 0x...>"` — der Fehler landet in der API-Antwort statt
im Log; Standard-json wirft dort einen TypeError. Ein schnellerer Serializer,
der Fehler verschluckt, ist schlechter als ein langsamer, der sie zeigt. Der
Provider konvertiert jetzt bekannte Typen (sqlite3.Row, nc.dbwrap-Row-Proxies,
set, bytes, Decimal) und wirft sonst TypeError. Gegen alle echten Bot-Typen
getestet, dazu 140 Routen im Smoke-Test mit aktivem orjson.

Vier Testverträge halten das fest: `test_fast_json_safety` (kein `default=str`,
lautes Scheitern, sauberer Fallback) und `test_uvloop_optional` (Policy vor
`asyncio.run`, per Env abschaltbar).

## V37-CPU: Thread-Budget für ffmpeg (Load 113 → geplant)

**Befund aus dem Produktions-htop:** Load **113** auf 8 Kernen, **812 Threads**,
alle Kerne auf 100%, Swap 961M/1024M voll (bei 10.9G/31G RAM — der Swap ist
also NICHT aus Speichermangel voll, sondern aus einer früheren Spitze).

**Ursache, per grep gefunden:** `-threads` kam im gesamten Bot **kein einziges
Mal** vor. Ohne die Option nimmt ffmpeg `-threads 0` = auto = **alle Kerne** —
pro Prozess. Und es können **vier libx264-Encoder gleichzeitig** laufen:

| Pfad | Wo | Was |
|---|---|---|
| Restream-Transcode | `_build_restream_cmd` | veryfast 4500k + Overlay |
| Relay | derselbe Builder (`relay_profile`) | ultrafast 3500k |
| Discord-Shrink | `_shrink_for_discord`, Re-Encode-Split | veryfast |
| Clip-Extraktion | `clip_moment` | veryfast |

x264 startet ~1.5× Kerne an Threads. Vier Encoder × ~12 = **48 rechnende
Threads auf 8 Kernen** — dazu Whisper (3×2) und llama.cpp (4). Der Killer:
eine Aufnahme endet → die Nachbearbeitung startet einen vollen x264 **gegen das
laufende Sendebild**.

**Der Fix — `_ff_cmd(cmd, threads=…, nice=…)`.** Ein Helfer, durch den jeder
rechnende ffmpeg-Pfad läuft. `-threads` steht direkt hinter `"ffmpeg"` (globale
Codec-Option, gilt für De- und Encoder — nachgemessen: `-threads 2` ergibt 4
OS-Threads statt ~1.5× Kerne). `nice` als Prefix statt `preexec_fn`: das
funktioniert auch über `asyncio.create_subprocess_exec` und ist im `ps` sichtbar.

Die Aufteilung folgt der Wichtigkeit — **das Sendebild hat Vorrang**:

| Env | Default | Pfad | nice |
|---|---|---|---|
| `FFMPEG_THREADS_LIVE` | 3 | Restream-Transcode | **kein** (Vorrang) |
| `FFMPEG_THREADS_RELAY` | 2 | Relay | **kein** |
| `FFMPEG_THREADS_RECORD` | 1 | Aufnahme (`-c copy`, I/O-gebunden) | 5 |
| `FFMPEG_THREADS_BG` | 1 | Shrink/Clip/Split/Waveform | 12 |

Der Whisper-Audio-Tap bekommt 1 Thread und **kein** nice — er füttert die
Live-Reaktion und darf nicht ins Stocken geraten. `ffmpeg -version` bleibt
ungedeckelt (rechnet nichts).

**Rechnung für 8 Kerne:** Sendebild 3 + Relay 2 + Aufnahme 1 + llama.cpp 4 = 10.
**Ehrlich: das ist immer noch leicht überbucht.** Real gleichzeitig sind es ~9 —
die Aufnahme ist I/O-gebunden und verbraucht ihren Thread kaum, Whisper wird bei
Live auf 1× gedrosselt (B98), llama.cpp läuft nur, wenn AZRAEL reagiert. Ruckelt
es weiter, ist `llama-server.service -t 4` → 3 der nächste Hebel, danach
`RESTREAM_RELAY_BITRATE_K` runter.

**Sichtbarkeit statt Raten.** `/api/system/resilience` liefert jetzt einen
`load`-Block direkt aus `/proc` (kein psutil): Load 1m/5m/15m + pro Kern +
Zustand (ok/busy/overloaded), RAM, **Swap-Prozent**, die Top-CPU-Verbraucher mit
Thread- und RSS-Zahl, sowie `ffmpeg_procs`/`ffmpeg_threads_total`. Das
Resilienz-Panel zeigt die Load-Zeile immer, die Top-Verbraucher und das
Thread-Budget nur, wenn es eng wird (sonst Rauschen).

**Zur Deutung der Load:** sie zählt auch Prozesse im I/O-Wait (D-State). Ein
vollgelaufener Swap treibt sie hoch, **ohne dass eine CPU rechnet** — deshalb
steht der Swap-Wert direkt daneben.

Zwei Testverträge halten das fest: `test_ffmpeg_thread_budget` prüft per AST,
dass **jede** rechnende ffmpeg-Befehlsliste durch `_ff_cmd` läuft (Ausnahme:
`-version`), dass das Sendebild mehr Threads bekommt als der Hintergrund, und
dass der Restream-Pfad **nicht** genice't ist.

Ehrliche Grenze: der Test-Container hat 1 Kern — die Thread-Steuerung ist
nachgewiesen (`-threads 2` → 4 OS-Threads), das 8-Kern-Verhalten unter echter
Last kann nur der Server zeigen.

## V37-B104: AI-Aufrufe ohne Deckel

`AI_FLASK_TIMEOUT` (300s) existierte als Deckel, wurde aber **nur** bei
`_run_async_from_flask` angewandt. Drei Flask-Routen (`api_ai_conversation_send`,
`api_ai_diagnose`, `api_ai_ask`) riefen `llm_chat_sync()` **direkt** — und erbten
damit `AI_TIMEOUT`. In der .env steht `AI_TIMEOUT=0`, was der Code zu **3600s**
übersetzt: ein Flask-Worker konnte **eine Stunde** blockieren. Dazu konnte
`_selfcheck()` den Start aufhalten. Alle vier sind jetzt gedeckelt
(`timeout=AI_FLASK_TIMEOUT` bzw. `asyncio.wait_for(…, 30)`).
`test_ai_timeout_capped` prüft per AST, dass kein AI-Aufruf ohne
timeout/wait_for zurückkommt.

## Testsuite: die Lücke, die alle anderen offenließen

Alle bisherigen Suiten lesen `bot.py` nur als **Text** (Regex/AST). Ob die
Datei überhaupt **importierbar** ist, ob die Modul-Ebene ohne NameError
durchläuft, ob die Routen registriert werden und beim Aufruf keinen 500er
werfen — das prüfte **nichts**. Genau solche Fehler sind statisch unsichtbar:
der `jsonify(ok=…, **rep)`-Bug (doppeltes Keyword-Argument → TypeError) fiel
erst beim echten Aufruf auf.

`test_smoke.py` schließt das: es stubbt TikTokLive + python-telegram-bot (mit
`_AnyMeta`-Metaklasse, weil `ContextTypes.DEFAULT_TYPE` ein Klassen-Attribut
ist), lädt bot.py, ruft `init_db()` und dann **jede parameterlose
GET-Route** auf. Ergebnis: **268 Routen registriert, 140 aufgerufen, 138
sauber, 2 erwartete 503er** (`/api/channels/status`, `/api/kick/channel` —
brauchen einen Event-Loop und liefern planmäßig `transient: true`; der Test
hält genau das fest).

## DB als SQL exportieren / importieren (V37-DBX)
Neu: `nc/dbexport.py` + drei Routen + ein Panel im System-Tab. Zweck ist der
Umstieg **SQLite -> MariaDB** ohne Handarbeit.

**Warum kein `sqlite3 .dump` / `mysqldump`?** Beide erzeugen dialekt-spezifische
DDL. `.dump` schreibt `INTEGER PRIMARY KEY AUTOINCREMENT` und
`BEGIN TRANSACTION` — MariaDB frisst das nicht. mysqldump schreibt Backticks und
`ENGINE=InnoDB` — SQLite frisst das nicht. Ein DDL-Uebersetzer waere eine eigene
Baustelle voller Sonderfaelle.

**Der Weg hier: nur DATEN exportieren, das Schema baut das Ziel selbst.**
`_init_db()` legt alle 42 Tabellen bereits in beiden Dialekten korrekt an
(`_schema_pk()`, txt_idx/txt_big/tbl_opts). Damit bleibt die Schema-Wahrheit an
genau EINER Stelle.

**Umstieg in vier Schritten:**
1. System-Tab -> "Datenbank — SQL-Export / Import" -> Ziel-Dialekt `mariadb` -> exportieren
2. `.env`: `DB_BACKEND=mariadb` + `MARIADB_*` setzen
3. Bot einmal starten & stoppen (legt das Schema an)
4. Datei im Dashboard importieren — erst "Pruefen" (dry-run), dann "Importieren"

**Der Backslash-Fallstrick (echt, nicht theoretisch):** MySQL/MariaDB behandeln
`\` in String-Literalen als Escape, SQLite NICHT. `'C:\rec\x.mp4'` bleibt in
SQLite unveraendert, wird in MariaDB aber zu `C:recx.mp4` — Dateipfade und Regexe
waeren **still** zerstoert, ohne jede Fehlermeldung. Deshalb kennt der Export
seinen Ziel-Dialekt, der Header haelt ihn fest, und der Import **bricht ab**,
wenn er nicht zum laufenden Backend passt. Ein Test weist beides nach.

Weiteres: Statement-Splitter parst String-Zustaende (ein naives `split(";")`
zerreisst jeden Wert mit Semikolon — Chat-Nachrichten, HTML, Regexe), BLOBs als
`X'hex'` (in beiden Dialekten gueltig), Export streamt zeilenweise (kein
RAM-Berg), `DELETE FROM` je Tabelle vor dem Insert-Block (Wiedereinspielen ohne
Dubletten), `?dry_run=1` prueft ohne zu schreiben, `DB_IMPORT_MAX_MB=200`
begrenzt den Upload.

**Beim Bauen selbst gefangen:** die Import-Route hatte
`jsonify(ok=rep.get("ok"), **rep)` — `rep` enthaelt `ok` bereits, das ist ein
doppeltes Keyword-Argument und wirft TypeError. Kein statischer Check sieht das;
erst der Test gegen den echten Flask-Stack (`app.test_client()`) hat es
gezeigt. Die drei bestehenden `jsonify(ok=True, **x)`-Stellen im Projekt wurden
geprueft — deren Dicts enthalten kein `ok`, sind also sicher.

## Modularisierung: der db_conn-Durchbruch (V37-MOD2)
Die Klassen-Extraktion war zu Recht gestoppt (RestreamManager/KickModerator
brauchen 22 bzw. 26 Bot-Funktionen). Ein AST-Scan der **441 freien Funktionen**
(17.077 Z.) zeigte den eigentlichen Hebel:

| Gruppe | Funktionen | Zeilen |
|---|---|---|
| 0 Bot-Abhaengigkeiten | 40 | 533 |
| **1–3 Abhaengigkeiten** | **297** | **6.439** |
| >3 Abhaengigkeiten | 104 | 10.105 |

Und in der 1–3-Gruppe hingen **106 Funktionen an genau EINEM Symbol: `db_conn`**.

**Schritt 1 — db_conn nach nc/dbwrap.py.** Die Wrapper lagen dort schon, die
Fabrik selbst noch in bot.py. Sie braucht nur env-abgeleitete Konstanten →
per `configure_db(db_path=…, backend=…, mariadb={…})` injiziert; das Modul liest
selbst KEINE Env und bleibt testbar. `_mariadb_connect`, `_WAL_INIT` und der
Pool-Lock sind mitgewandert. Reihenfolge AST-geprueft: alle 309 `db_conn()`-
Aufrufe liegen in Funktionen, `configure_db()` laeuft auf Modul-Ebene davor.

**Effekt: 40 → 109 abhaengigkeitsfreie Funktionen (533 → 1.652 Z.).**

**Schritt 2 — drei Domaenen-Module** aus dem freigewordenen Bestand:
- `nc/stats.py` — Auswertungen/Kennzahlen (get_per_user_stats, get_activity_pulse,
  get_lives_heatmap, get_recordings_heatmap, _collect_session_stats,
  _streamer_health, _dir_stats)
- `nc/archive.py` — Archiv-Regeln, Retention, Duplikat-Scan (run_archive_file_check,
  evaluate_archive_rule, get_archive_entries_paged, _retention_match,
  _scan_for_duplicates, compute_recording_fingerprint)
- `nc/notes.py` — Notizen/Lesezeichen/Annotationen (set_recording_note,
  toggle_bookmark, add_annotation, delete_annotation, _conv_list,
  set_tracking_notes)

**Stand: 25 nc-Module, bot.py 28.589 → 27.984 Z.** (seit Projektstart
29.449 → 27.984, −1.465 Z.).

**Neue Testsuite `test_nc_modules.py` (14 Vertraege).** Sie zieht das Schema
zur Laufzeit AUS bot.py (Klammer-Zaehlung statt Regex) und loest die
f-String-Platzhalter mit den SQLite-Werten auf — der Test kann also nicht gegen
ein ausgedachtes Schema gruen werden. Genau dieser Fehler ist beim Bauen
mehrfach passiert: erst wurde eine `recordings.filename`-Spalte angenommen (es
ist `filepath`), dann `get_lives_heatmap()` ohne das noetige `username`-Argument
aufgerufen. Beide Male war der Code richtig und der Test falsch — deshalb liest
er jetzt Signaturen und Schema aus der Quelle.

Ehrliche Grenze: der AST-Scanner hatte eine zu grosszuegige STD-Whitelist und
liess echte Bot-Helfer (`_parse_iso`, `_md5`, `_archive_where_clause`) als
"bekannt" durchgehen. pyflakes hat es gefangen, die Imports wurden nachgezogen.
Ein Scanner ersetzt die statische Pruefung nicht.

## Overlay-Feinschliff aus dem Handy-Screenshot (V37-B103)
Nach B100 füllt die Bühne das Bild — der Screenshot zeigte drei Restfehler:

- **Avatar außermittig**: `#az-panel` war im Leerlauf `opacity:0` — unsichtbar,
  belegte aber weiter Platz im Flex-Layout und drückte den Avatar aus der
  Mitte. Jetzt `#azrael:not(.active) #az-panel{display:none}`. Der Verlust der
  Fade-Transition ist egal: das Overlay wird mit 1 fps abfotografiert, CSS-
  Transitions sind im Sendebild ohnehin nie sichtbar.
- **Titel überlappte die Subtitle**: `.tname` hatte `line-height:1` — bei 40px
  liefen die Unterlängen von „g"/„P" in die 5px-Lücke. Jetzt `1.14`, und im
  Portrait `white-space:nowrap` + Ellipsis, damit lange Kanalnamen nicht
  umbrechen.
- **Donations-Text zu blass**: Zweckzeile, „noch keine Donations" und die
  Seit-Zeile im Portrait größer und kontrastreicher.

**`RESTREAM_OVERLAY_MODE=html` ist jetzt Default** (Code + .env). Das ist
sicher: der HTML-Pfad hat **vier Fallbacks auf drawtext** (Chromium fehlt,
Render-Fehler, FIFO-Fehler, Feeder-Abbruch) — er kann den Stream nicht kaputt
machen. `text` bleibt als Notausgang. Ein Test hält beides fest.

## Overlay-Ausrichtung & Größe — die eigentliche Ursache (V37-B100…B102)
Der erste B94-Fix (Rendern in Quellauflösung) war richtig, aber unvollständig.
Der Screenshot aus dem laufenden Kick-Stream hat den echten Fehler gezeigt:

**B100 — die Bühne war hart auf 1920×1080 verdrahtet.** overlay.html hat ein
`#stage` mit fixen 1920×1080, das per JS eingepasst wurde:
`s = Math.min(vw/1920, vh/1080)`. Bei einer 9:16-Quelle (1080×1920) ergibt das
**s = 0,5625** → die komplette Bühne schrumpft auf ein **1080×608-Band in der
Bildmitte**, 32% der Höhe bespielt, der Rest leer. Und die erste
Portrait-Fassung rechnete in `vw/vh` — die zählen gegen den **Viewport**, nicht
gegen die skalierte Bühne, also doppelt daneben.
**Neu:** `fit()` wählt die Bühnen-Referenz nach Seitenverhältnis (portrait →
1080×1920, sonst 1920×1080), setzt `stage.style.width/height` und die Klasse
`html.portrait`. Die Portrait-Regeln hängen daran und rechnen in **echten
Bühnen-Pixeln** (0 vw/vh, per Test erzwungen). Ergebnis: die Bühne füllt jetzt
in JEDER Auflösung 100% des Bildes.
Vertikale Aufteilung (1920px): Titel 36–126 · Follower 150–260 ·
*[Kameramitte 260–600 frei]* · AZRAEL 620–900 · Moderator 980–1180 ·
Donations bottom 48.

**B101 — AZRAELs Textwand.** Der drawtext-Pfad kappt seit je auf 2×38 Zeichen,
der HTML-Pfad reichte den **vollen** Reaktionstext durch → im Sendebild eine
unlesbare Textwand. Neu: `AZRAEL_OVERLAY_MAXLEN=240` + `_ov_clip_text()`
(kappt an der Satzgrenze, kein Wort-Abriss); die API liefert `text` gekappt
und `text_full` daneben. CSS-Deckelung als zweite Sicherung: `.aztext` 21px mit
`-webkit-line-clamp:4` / `max-height:130px` (Portrait 27px, 5 Zeilen, 200px).

**B102 — der auto-Default greift nicht bei bestehender .env.**
`os.getenv("RESTREAM_OVERLAY_HTML_SIZE", "auto")` liest die Server-.env
**zuerst** — steht dort noch `1080,1920`, war der ganze B94-Fix wirkungslos.
Neu prüft `_overlay_render_size()` eine fest konfigurierte Größe trotzdem
gegen die geprobte Quelle: weicht das Seitenverhältnis um >0,05 ab, **gewinnt
die Quelle** (mit deutlicher Warnung im Log). Passt der Aspekt und nur die
Auflösung unterscheidet sich, bleibt die Vorgabe — dann skaliert scale2ref
sauber und proportional.

| .env-Wert | Quelle | gerendert | warum |
|---|---|---|---|
| `auto` | 1080×1920 | 1080×1920 | Quellauflösung |
| `1080,1920` | 1920×1080 | **1920×1080** | korrigiert, Aspekt passte nicht |
| `1080,1920` | 720×1280 | 1080×1920 | Aspekt passt, scale2ref skaliert |
| `auto` | unbekannt | Fallback | Probe fehlgeschlagen |

## AZRAELs Antworten im Sendebild (V37-B99)
**Echter Bug, warum AZRAEL im Restream stumm blieb:** die drawtext-Kette las
ausschließlich `_KICK_MOD.last_spoken` — das wird aber NUR gesetzt, wenn der
Bot eine Nachricht in den **Kick-Chat** schickt. Die Live-Reaction-Engine ruft
`_KICK_MOD.react()` auf und schreibt nichts in den Chat; AZRAELs eigentliche
Antworten (die in `_AZRAEL_REACTION` landen) tauchten im Sendebild deshalb nie
auf. Jetzt ist `_AZRAEL_REACTION` die Primärquelle, `last_spoken` bleibt
Fallback für echte Chat-Nachrichten des Bots.

**Das wirkt SOFORT im aktiven text-Modus** — kein Chromium nötig. Der
HTML-Modus (overlay.html, `#az_text`) las die richtige Quelle schon immer.
Haltezeiten passen zusammen: `RESTREAM_REACT_HOLD=20` (drawtext) vs.
`AZRAEL_REACTION_HOLD_S=18` (HTML-API).

**Portrait-Layout nachgezogen**: in der ersten 9:16-Fassung fehlte `#azrael`
komplett — das Panel wäre bei `bottom:40px` unter dem Donations-Block
verschwunden. Jetzt sitzen Avatar + Sprechpanel mittig auf 34vh, Text mit
2.6vw (handylesbar), darunter Moderator (58–70vh) und Donations (75–97vh) —
kollisionsfrei. Zwei neue Testverträge sichern beides ab (jetzt 17).

## CPU-Vorrang fürs Sendebild (V37-B98)
Der B96-Befund hatte eine tiefere Ursache: **dein Server ist ohne GPU massiv
überbucht.** Rechnung für 8 Kerne bei laufendem Multi-Restream:

| Verbraucher | Kerne |
|---|---|
| ffmpeg Kick (x264 veryfast, 4500k, 1080x1920@30) | 2–4 |
| ffmpeg Relay Twitch (ultrafast, 3500k) | 1–2 |
| Chromium Overlay-Screenshot (1/s) | ~0.5 |
| Whisper base × 3 gleichzeitig (WHISPER_CPU_THREADS=2 je Instanz) | bis 6 |
| llama.cpp (AI_PROVIDER=brain) | 2–8 |

Summe im Spitzenfall: **weit über 8**. Alles kämpft, nichts gewinnt — das
Encoding fällt zurück (ENCODE-RÜCKSTAND) und Whisper staut sich.

**Neu: `WHISPER_THROTTLE_LIVE=1` (Default).** Solange ein Restream läuft, wird
Whisper auf EINE Transkription gleichzeitig serialisiert; im Leerlauf sofort
wieder voller Speed. Begründung: das Sendebild ist das Produkt, Transkription
ist Beiwerk. Das Umschalten wird einmal pro Wechsel geloggt.

**Sichtbar gemacht**: `/api/system/resilience` liefert jetzt einen `cpu`-Block
(Kerne, laufende Restreams, Whisper-Drosselstatus, verworfene Segmente,
Encoder-Presets, llama.cpp aktiv), und das Resilienz-Panel im Control-Tab
zeigt eine CPU-Zeile — inkl. Warnung, wenn Segmente verworfen wurden.

**Wenn es weiter klemmt** (ehrliche Reihenfolge): `RESTREAM_RELAY_BITRATE_K`
senken → `LIVE_REACT_SPEECH=0` (Whisper ganz aus, Chat-Reaktion bleibt) →
`AI_PROVIDER` weg von `brain` auf freeai (llama.cpp frisst dann keine Kerne
mehr). Eine GPU löst es endgültig, aber das ist keine Softwarefrage.

## Modularisierung: bewusster Stopp
RestreamManager (645 Z.) und KickModerator (613 Z.) bleiben in bot.py. Der
AST-Scan zeigt **22 bzw. 26 harte Bot-Funktions-Abhängigkeiten** — eine
Extraktion bräuchte 48 injizierte Callbacks. Das wäre kein Modul, sondern
verschobener Code mit riesiger Injektionsfläche: schlechter als der
Ist-Zustand. Diese Kopplung ist semantisch — die beiden Klassen SIND die
Orchestrierung. Endstand: **22 nc-Module**, bot.py 29.449 → ~28.600 Z.

## Fehlerbehebung aus dem Produktions-Log (V37-B94…B97)
Vier Befunde aus error.log, alle mit Regressionsvertrag in test_restream:

**B94 — Overlay-Auflösung (der Kern des "passt nicht"):** das HTML-Overlay
wurde in FESTER Größe (1080x1920) gerendert und per `scale2ref=w=iw:h=ih` auf
die Videogröße gezogen — ohne Seitenverhältnis. Bei einer 16:9-Quelle wurde
das 9:16-Overlay breitgequetscht, auf dem PC unbrauchbar. Jetzt:
`RESTREAM_OVERLAY_HTML_SIZE=auto` (neuer Default) probet per ffprobe die
**echte Quellauflösung** (mit denselben Headern/Proxy wie der Recorder, sonst
403) und rendert das Overlay 1:1 in dieser Größe → scale2ref wird zum No-Op,
pixelgenau, für JEDE Quelle. Als Sicherheitsnetz skaliert der Filter jetzt mit
`force_original_aspect_ratio=decrease` und zentriert — verzerrt also selbst bei
erzwungener Festgröße nie mehr.

**B95 — /api/channels/status warf HTTP 500** ("too many values to unpack"):
`_run_async_from_flask` gibt das Coroutine-Ergebnis DIREKT zurück; das
`info, err = ...`-Muster aus api_kick_channel funktioniert dort nur, weil
`channel_info()` selbst ein 2-Tupel liefert. Mein `_all()` liefert ein
3-Key-Dict. Behoben, Vertrag im Test.

**B96 — "live-react seit 434s ohne Lebenszeichen" (der TikTok-Chat):** zwei
echte Ursachen. (1) Der Heartbeat schlug erst NACH der Whisper-Transkription —
ein Worker, der ordnungsgemäß in einer langen CPU-Operation steckt, sah für
den Watchdog tot aus. Neu: `_hb_while()` hält den Beat WÄHREND langer Awaits.
(2) `for w in wavs[:-1]` arbeitete einen ganzen Segment-Rückstau in EINER
Iteration ab. Whisper ohne GPU kommt bei ausgelasteten Kernen nicht nach
(Restream-Encoding teilt sich die 8 Cores), der Stau wuchs, die Schleife lief
minutenlang. Neu: `LIVE_REACT_MAX_BACKLOG=4` — ältere Segmente werden
verworfen (minutenalte Sprache in eine LIVE-Reaktion zu füttern ist ohnehin
wertlos) und einmal pro Schwung als Warnung geloggt.

**B97 — 176× "Chat-ID ungültig: Chat not found" in einer Nacht:**
`_mark_dead()` setzte längst eine Sperre, aber nur `_safe_send()` (Text) hat
sie je gelesen — der Video-Upload rannte für jeden Part jeder Aufnahme erneut
hinein und schickte die Fehlermeldung auch noch an genau den Chat, den es
nicht gibt. Jetzt prüft `_send_one()` die Sperre und die Part-Schleife bricht
nach dem ersten Treffer ab.

**Offen (kein Softwarefehler):** die 403er bei @helge_72-Aufnahmen sind der
bekannte Datacenter-IP-Block von TikTok. Der adaptive Schutz schaltet nach 2
Treffern auf yt-dlp; hilft auch das nicht, ist die Egress-IP verbrannt und es
braucht einen Residential-Proxy.

## STUDIO-Theme: heller, professioneller Default
Das Dashboard startet jetzt im neuen **studio**-Theme — helle Broadcast-
Konsole statt Cyberpunk. Der Switcher im Footer zykelt weiter durch
`studio → matrix → ember → ice → blood`, die alten Themes bleiben also
vollständig erhalten (localStorage merkt sich die Wahl).

**Wie es sauber umgesetzt wurde**: ein naives Light-Theme wäre gebrochen —
34 Flächen hatten `rgba(0,0,0,x)` hart im CSS. Die wurden zuerst auf
Surface-Variablen gehoben (`--sunken` / `--sunken-2` / `--sunken-3`), die das
Theme kippen kann. Danach neutralisiert ein Override-Block die Cyberpunk-
Effekte: Scanlines aus, Raster fast unsichtbar, Neon-Glows → echte Schatten,
Orbitron → Inter, Panels → Karten mit Elevation, Buttons → solide Flächen,
Tabs → Segmented Control, Inputs mit Focus-Ring.

**Bewusst dunkel geblieben**: Video-Monitore (`.studio-monitor`, `.mon`),
Log-Konsolen (`.logbox`), der Proxy-Globus und der Boot-Splash. Genau so
machen es professionelle Studio-Tools (YouTube Studio, VS Code) — ein weißer
Video-Bereich wäre ein Fehler, kein Feature. Die pulsierende ON-AIR-Lampe
bleibt ebenfalls: Live-Semantik schlägt Zurückhaltung. Kontrast geprüft —
YouTube-Rot auf Weiß hatte nur ~3.3:1 und wurde für kleine Schrift
nachgedunkelt.

## Control-Tab: vollständig Multi-Plattform (V37-MP)
Audit ergab: Deck-Chips und Chat-Senden konnten längst alle drei Plattformen
(das Backend liefert `platforms` + `restream` je kick/twitch/youtube), aber
drei Dinge waren noch Kick-only:
- **Kanal-Status** war eine Kick-Kachel → jetzt Panel "Kanal-Status — alle
  Plattformen" mit einer Karte je Plattform (live/Zuschauer/Follower/Titel,
  Markenfarbe als Akzent) plus **Zuschauer gesamt** über alle Kanäle. Neue
  Route `/api/channels/status`: Kick über die keylose Channel-API, Twitch über
  Helix (`/streams` + `/users` + `/channels/followers`), YouTube über einen
  leichten `/live`-Scrape (Data-API würde OAuth+Quota kosten). 20s-Cache, weil
  der Tab pollt; `?refresh=1` erzwingt.
- **"Restream → Kick"** hieß so, sendete aber längst an alle → jetzt
  "Restream → Multi-Plattform", Beschreibung entsprechend ehrlich.
- **Ziel-Anzeige** zeigte pauschal "Kick" → nennt jetzt die tatsächlich
  laufenden Ziele (z.B. "KICK + TWITCH").

Ehrliche Grenze: Twitch-Zuschauer/Follower brauchen `TWITCH_CLIENT_ID` +
`TWITCH_EVENTSUB_TOKEN` (dieselben Credentials wie die Follows). Fehlen sie,
zeigt die Karte einen Hinweis statt Zahlen — Kick und YouTube laufen keylos.

## Overlay: 9:16-Modus für den Relay
Der Screenshot aus dem laufenden Kick-Stream zeigte es: die Panels waren für
16:9/OBS gebaut und wirkten in der hochkant gerenderten TikTok-Quelle
verloren, die Schrift war auf dem Handy unlesbar. Eine Portrait-Media-Query
(`max-aspect-ratio: 1/1`) skaliert jetzt alles mit vw/vh: Titel und Donations
über die volle Breite, Follower unter den Titel, Moderator mittig über die
Donations, Alert 84vw. Landscape/OBS bleibt **exakt** wie vorher — reine
Ergänzung, keine Änderung am bestehenden Layout.

## Overlay: Multi-Plattform (Kick/Twitch/YouTube) + Session-Reset-FIX
**Echter Bug gefunden und behoben**: `_overlay_session_reset()` setzte beim
Sende-Start brav den Nullpunkt, und die drawtext-Kette filterte auch danach —
aber `/api/overlay/state` (= die HTML-Overlay-Anzeige, die jetzt auch im Relay
läuft) tat das NICHT. Die Donation-Summe zählte deshalb ALLE Spenden seit
Installation und sprang nie auf 0 zurück. Die Route filtert jetzt nach
`_OVERLAY_SESSION["start"]` und liefert `session_start` mit; das Overlay zeigt
"seit Sende-Start HH:MM".

**Plattform-Herkunft durchgängig**: neue Spalte `overlay_events.platform`
(Migration; Bestandszeilen → 'kick'), `_overlay_push(..., platform=)` und alle
8 Event-Quellen getaggt. `/api/overlay/state` liefert jetzt `by_platform`
(Donations/Summe/Follows je Plattform), `followers` (Ticker aller Plattformen)
und `platform` an jedem Event. `/api/overlay/event` akzeptiert `platform` im
Body (für externe Webhooks).

**Abdeckung je Plattform:**
- **Kick**: Follows + Donations (bestand)
- **Twitch**: Bits + Subs (bestand) · **Follows NEU** über EventSub-WebSocket
  — Twitch-IRC liefert keine Follow-Events, das geht nur über EventSub.
  Braucht andere Credentials als der Chat-Token: `TWITCH_CLIENT_ID` +
  `TWITCH_EVENTSUB_TOKEN` (User-Token mit Scope `moderator:read:followers`).
  Fehlt eins, wird der Listener sauber übersprungen (einmalige Log-Info),
  Bits/Subs laufen unabhängig weiter. Inkl. session_reconnect/revocation-
  Handling und Backoff.
- **YouTube**: Superchat (bestand) · **NEU** Super-Sticker + Mitgliedschaften
  (inkl. geschenkter). Ehrliche Grenze: neue YouTube-*Abonnenten* liefert die
  Live-Chat-API nicht — Mitgliedschaften sind das nächstliegende Signal.
- **TikTok**: Gifts + Follows (bestand, jetzt getaggt)

**Overlay-UI**: Plattform-Badges in Markenfarben (Kick-Grün, Twitch-Lila,
YouTube-Rot, TikTok-Cyan) an jeder Donation, am letzten Follower und im neuen
Follower-Ticker; Bilanzleiste je Plattform unter dem Zielbalken; Alerts nennen
die Plattform. Zwei neue Testverträge in test_restream (jetzt 9).

## V37-Ausbau: Tests, HTML-Overlay im Relay, Pulse, Latenz-Ranking, Wartung
**test_restream.py** (neu, 9. Suite): sichert die Restream-Kernlogik ab —
Failover-Streak, Round-Robin, tee/independent-Kommandobau (Kick hart, Zusätze
weich), Transcode-Matrix, Reentrance-/Cleanup-Verträge, relay_profile-
Vererbung, 403-Lebenszyklus. Ab jetzt Teil jeder Validierung.

**HTML-Overlay im Relay** (`RESTREAM_OVERLAY_MODE=html`): die /overlay-
Browser-Source (Donations, letzter Follower, virtueller Moderator) wird
server-seitig per headless Chromium zu transparenten PNGs gerendert und über
eine image2pipe-FIFO ins Video gemischt (scale2ref passt sie jeder Videogröße
an). Der Feeder pusht mit FESTEM Takt und wiederholt notfalls das letzte Bild
— ein stallender Overlay-Input kann den Restream also nie mitreißen; 
eof_action=repeat + shortest=0 sichern die ffmpeg-Seite. Vier Fallback-Pfade
(kein html-Modus / kein Chromium / Preflight-Screenshot scheitert / FIFO-
Fehler) landen automatisch beim bewährten drawtext. Voraussetzung auf dem
Server: `apt install chromium-browser`. CPU: ~1 Screenshot/s, auf die Relays
wird das Overlay bewusst NICHT dupliziert.

**/api/pulse**: bündelt die vier 5-Sekunden-Poller (stats, bandwidth,
health-score, restream/deck) in EINEN Request — ruft die bestehenden View-
Funktionen intern auf, Datenformat bleibt 1:1. Der 700ms-Avatar-Poller läuft
nur noch im Control-Tab bei sichtbarer Seite. Spürbar weniger Server-Last +
Mobil-Akku.

**freeai-Latenz-Ranking**: EMA-Latenz pro Base; die schnellste Base sortiert
sich automatisch nach vorn, ungemessene werden früh probiert (sonst käme eine
zweite Base nie dran), 429-Sperren haben Vorrang. `bases_status()` liefert
avg_ms fürs Dashboard.

**Wartung + Kontext**: wöchentlicher VACUUM+ANALYZE-Loop (ergänzt die
bestehende F82-6h-WAL-Pflege — Namenskollision beim Einbau entdeckt und
aufgelöst, F82 blieb intakt). Kick-Zuschauer-Sampler (keyless public API,
60s, nur bei laufendem Restream) → die Sende-Timeline liefert jetzt
now/peak/avg + Verlaufspunkte (`viewers` im /api/stream/timeline).

## freeai-Rotation aktiv + Dashboard-GLOW-UP
**Basen-Rotation scharf**: `FREEAI_BASES` enthält jetzt Pollinations (primär)
+ llm7.io (sekundär) — beide keyless. Fällt eine aus oder läuft ins 429,
übernimmt die nächste automatisch. Ehrlicher Hinweis: die Verfügbarkeit
kostenloser Endpunkte schwankt naturgemäß — genau dafür existieren Rotation
und Backoff. Neue Route `/api/freeai/status` zeigt Basen + Cooldowns; die
Brain-Zustandszeile im Dashboard zeigt "☁ frei/gesamt Basen" live an.

**GLOW-UP** (CSS-only, alle 4 Farb-Themes profitieren automatisch):
animiertes Grid-Raster + Vignette im Hintergrund, subtile CRT-Scanlines,
Orbitron-Display-Font für Tabs/Header/Metriken, Neon-Glow auf Hover (Panels,
Buttons, Tabs, Metriken), pulsierende Live-Lampen, Gradient-Linien an Panel-
Köpfen, Neon-Scrollbars, Focus-Glow auf Formularfeldern, Row-Hover in
Tabellen, Sparkline-Drop-Shadows. `prefers-reduced-motion` stoppt alle
Animationen; auf Mobil sind Grid-Animation + Scanlines deaktiviert (Akku).

## V37: Ollama KOMPLETT entfernt — nc.freeai ist der einzige Cloud-Pfad
Ollama ist aus Bot, Dashboard, Brain-Runtime und Bridge restlos raus (Kern-
Funktionen, Konstanten, Health-Checks, Fehlertexte, UI-Strings, Embeddings).
Die AI-Kette ist jetzt: **AI_PROVIDER=brain** → lokales llama.cpp (Port 8080),
bei Ausfall/anders konfiguriert → **nc.freeai** (keyless Cloud).

**`nc/freeai.py`** (neu, ausgebaut):
- Kostenlose OpenAI-kompatible Endpunkte OHNE API-Key (Default: Pollinations).
- **Basen-Rotation**: `FREEAI_BASES` = Komma-Liste `url` oder `url|key` — fällt
  eine Base aus (Netz/HTTP/429), übernimmt die nächste automatisch.
- **429-Backoff pro Base** (`FREEAI_429_COOLDOWN_S`, Default 90s): eine rate-
  limitierte Base wird gesperrt statt weiter gehämmert.
- **sync + async + SSE-Streaming** mit dem unveränderten (text, error_kind)-
  Vertrag; der <think>-Filter für Reasoning-Modelle blieb 1:1 erhalten.
- **Vision-Konvertierung**: alte Ollama-Style `images`-Felder (base64) werden
  automatisch ins OpenAI-Vision-Format übersetzt — alle Bild-Callsites
  funktionieren unverändert weiter.
- Telemetrie-/Warn-Hooks per Injection (bot-frei, isoliert testbar).

Migration: `OLLAMA_URL`/`OLLAMA_MODEL`/`REACTION_AI_FALLBACK_OLLAMA` aus .env
entfernt; `AI_MODEL` (Default `openai` = Pollinations-Alias) ersetzt das
Modell; `REACTION_AI_PROVIDER=ollama` wird sanft auf pollinations migriert.
Brain: `BRAIN_LLM_BACKEND` = auto|llamacpp|off; Embeddings nur noch llama.cpp
(`BRAIN_EMBED_URL`, llama-server --embedding).

## Dashboard: AZRAEL + Brain vereint, Control-Tab voll mobil (Welle 1+2)
**Welle 1 — AZRAEL-Tab in den Brain-Tab gemerged**: der eigene AZRAEL-Tab
entfällt; der Brain-Tab heißt jetzt „AZRAEL BRAIN" und zeigt drei Sektionen:
(1) eine neue Brain-Zustandszeile (Tick/LLM/aktive Regeln/Entscheidungen 24h +
Warnungen der letzten 6h — dieselbe Quelle wie /brain in Telegram), (2) die
komplette AZRAEL-Kommandozentrale (nativ, unverändert), (3) die Brain-Analytik
(iframe, lazy geladen + einklappbar). Tab-Nummern nachgezogen, railViews +
Deep-Links bereinigt.

**Welle 2 — Control-Tab 100% mobil**: die fixierte Sendeleiste überlappte den
Content und lief rechts raus; jetzt kompakt + horizontal scrollbar, body mit
Platz darüber. ON-AIR-Deck-Signalnodes untereinander (Pfeil rotiert), Restream-
Karten volle Breite, Deck-Tabellen scrollbar, Chat-Panel full-width, Button-
Reihen umbrechend, Formfelder full-width. Breakpoints ≤760px + ≤420px.
CSS-Klammern 861/861, 12 JS-Blöcke OK.

## Modularisierung Runde 3 — Klassen (8 Klassen, 4 neue Module)
AST-Scan über alle Top-Level-Klassen mit echter Abhängigkeitsanalyse:
- **`nc/dbwrap.py`** — _SQLiteConnWrap + MariaDB-Shim (Row-Proxy/Cursor/Conn).
  Der Pool lebt jetzt im Modul (get_pool/set_pool), der Bot initialisiert ihn
  lazy — kein Import-Zyklus, keine Reihenfolge-Falle.
- **`nc/logfilters.py`** — _WerkzeugScannerFilter + _DiscordErrorHandler
  (Fehler-Queue per configure injiziert).
- **`nc/scraper.py`** — TikTokScraper (Header per configure, Proxy aus
  nc.proxyutil).
- **`nc/proxyutil.py`** — _ProxyRouter dazu (Pool/Lock als Referenzen,
  configure_router VOR der Instanziierung — AST-verifiziert).
Ergebnis: **22 nc-Module**, bot.py von 29.449 auf **28.186 Zeilen**.
Bewusst NICHT extrahiert: RestreamManager (645 Z.) und KickModerator (613 Z.)
— beide mit 6+ harten Bot-Abhängigkeiten; das wäre eine eigene Welle mit
Callback-Injection und braucht mehr Testabdeckung als die Verträge in
test_restream heute leisten.

## Modularisierung Runde 2 — massiver Batch (23 Funktionen, 6 neue Module)
AST-Vollscan über alle 700+ Top-Level-Funktionen fand 37 mit null Bot-
Abhängigkeiten. In zwei verifizierten Batches extrahiert:
- **`nc/ffdiag.py`** — ffmpeg-stderr-Diagnostik (Banner-Skip, Tail),
  Kommando-Redaktion (Cookies raus), Codec-Erkennung, Qualitätsstufe.
- **`nc/cookies.py`** — Cookie-Eingabe→Netscape, Dedupe, Alarm-Stufen.
- **`nc/textmore.py`** — Telegram-Splitting, ISO-Parse, Archiv-Dateinamen,
  Video-Captions, Overlay-Umbruch, Text-Kompaktierung.
- **`nc/scoring.py`** — Aufnahme-Qualitäts-Score + Telegram-Analyse-Report.
- **`nc/sqlutil.py`** — NL→SQL-Übersetzung, regelbasierter SQL-Bau,
  Whitelist-ORDER-BY.
- **`nc/persona.py`** — AZRAEL-Intensitäts-Hinweis, Emotions-Klassifikation,
  Lernparameter.
Jeder Batch: py_compile + pyflakes 0 + AST-Nahtcheck (47 Symbole, Import vor
Nutzung, keine Doppel-Defs) + Funktionstests gegen die ECHTEN Signaturen
(mehrere Testannahmen waren falsch — der Code war jeweils korrekt; exakte
Original-Semantik wie Tupel-Rückgaben und Komma-Listen-Matching erhalten).
Der Bughunt fand und behob einen echten Reihenfolge-Bug (_parse_iso wurde
Z.930 genutzt, Import stand bei Z.1210 → Batch-Importe in den frühen Block).
_env_int blieb bewusst im Bot (Z.599, fundamental für alle Konstanten).

## ENDGÜLTIGER Multi-Plattform-Fix: Kick raus aus dem tee
Befund über mehrere Runden: Kick lief IMMER stabil, solange es der einzige
Restream war (direkter -f flv-Pfad an den rtmps/IVS-Ingest). Kick brach erst,
als es in den ffmpeg-tee gesteckt wurde — und zwar OHNE Fehlermeldung: ffmpeg
pusht scheinbar erfolgreich, aber Kick nimmt den Stream nicht an. Der tee-Muxer
und Kicks rtmps/IVS-Ingest vertragen sich still nicht. Twitch (rtmp/plain)
verträgt den tee problemlos — daher "nur Twitch läuft".

Konsequenz — Default jetzt `RESTREAM_MULTI_MODE=independent`:
- **Kick** läuft als Hauptprozess über EXAKT den bewährten direkten Pfad
  (kein tee, -f flv an rtmps), volles Profil (veryfast, RESTREAM_BITRATE_K).
- **Twitch/YT** laufen als eigene Relay-Prozesse mit eigenem Reconnect-Loop
  und LEICHTEM Encode-Profil (`RESTREAM_RELAY_PRESET=ultrafast`,
  `RESTREAM_RELAY_BITRATE_K=3500`) — das hält die Gesamt-CPU unter dem Niveau,
  das früher die Disconnects erzeugte (2× veryfast@6000k).
- Jeder Prozess ist unabhängig: fällt Twitch, läuft Kick ungestört — und
  umgekehrt.

## Adaptiver 403-Schutz (Recorder)
TikTok blockt Live-CDN-Pulls von Datacenter/VPS-IPs mit `403 Forbidden` — auch
mit gültigen Cookies und über RECORD_PROXY. Der Resolve klappt (Bot weiß, User
ist live), aber der ffmpeg-Pull der signierten CDN-URL wird abgelehnt. Neu:
bekommt ein User `RECORD_403_YTDLP_HITS` (Default 2) mal in Folge 403 mit dem
nativen ffmpeg-Recorder, wird er für `RECORD_403_YTDLP_COOLDOWN_S` (Default
30min) auf **yt-dlp** umgestellt — das signiert die TikTok-Requests selbst und
umgeht das CDN-403 meist. Nach dem Cooldown wird der native (schnellere) Pfad
wieder probiert; eine erfolgreiche Aufnahme setzt den Zähler sofort zurück.

Hilft yt-dlp auch nicht, ist es fast sicher die Server-Egress-IP: dann einen
Residential-/Mobile-Proxy in RECORD_PROXY setzen (Datacenter-IPs sind geflaggt).

## Fix: "nur Twitch streamt, Kick fehlt"
Ursache: mein onfail=ignore lag an ALLEN tee-Zielen — also auch am Kick-Primär.
Scheiterte Kick (typisch: rtmps-TLS-Handshake zum IVS-Ingest), wurde es STILL
übersprungen, und nur Twitch (rtmp/plain) blieb übrig. Fixes:
- **Primär (Kick) ohne onfail**: ein Kick-Fehler ist jetzt SICHTBAR → der
  Monitor greift und verbindet neu, statt Kick lautlos fallenzulassen. Nur die
  Zusatz-Ziele (Twitch/YT) tragen onfail=ignore.
- **Ziel-Diagnose im Log**: bei Multi-Target-Abbruch wird erkannt, ob ein
  rtmps/TLS-Ziel (Kick) oder ein rtmp-Ziel (Twitch) die Ursache war — kein
  Raten mehr.

Hinweis: der tee mischt rtmps(Kick) + rtmp(Twitch). Klappt das bei dir nicht
zuverlässig, ist `RESTREAM_MULTI_MODE=independent` die Alternative (getrennte
Protokoll-Kontexte), aber mit 2 Encodes — dann `RESTREAM_X264_PRESET=ultrafast`
+ niedrigere Bitrate, damit die CPU reicht.

## Restream-Stabilität: Disconnects durch Encode-Rückstand
Häufigste Disconnect-Ursache auf GPU-losem Server: ffmpeg fällt beim Encoden
hinter Echtzeit zurück (speed < 1.0x) → RTMP-Puffer laufen leer → Verbindung
bricht. Besonders im independent-Modus (mehrere parallele Encodes) + hoher
Bitrate. Gegenmaßnahmen:
- **Encode-Rückstand-Erkennung**: fällt speed anhaltend unter 0.95x, kommt eine
  klare Log-Warnung mit der Ursache + Abhilfe (statt stiller Disconnects).
- **`RESTREAM_X264_PRESET`** (Default veryfast): auf `superfast`/`ultrafast`
  senken spart CPU → stabilerer Stream.
- **`-max_muxing_queue_size 1024`**: kurzer Rückstand staut den Muxer nicht mehr
  bis zum Abbruch.
- **Sichere Default-Konfig**: `RESTREAM_MULTI_MODE=tee` (EIN Encode an alle Ziele
  dupliziert) statt independent (N parallele Encodes), Bitrate 4500k. Der
  independent-Modus bleibt für Server mit genug CPU verfügbar.

## Quellen-Failover (channel-surfing) + Chat folgt der Quelle
Nach dem **Autostart** verbindet sich der Restream mit einer live TikTok-Quelle.
Danach läuft ein leichter Watcher pro Restream, der **nur den Online-Status**
der aktuellen Quelle pollt (Intervall `RESTREAM_SRC_POLL_S`, Default 30s). Geht
die Quelle offline, schaltet er **aktiv** (ohne auf den ffmpeg-Tod zu warten)
zur nächsten live Quelle aus der auto_restream-Liste um — Round-Robin ab der
aktuellen, damit nicht immer dieselbe oben drankommt.

Stabilisierung gegen Flackern:
- Aufwärmphase vor dem ersten Check (frischer Stream/Quelle bekommt Zeit).
- Umschalten erst nach `RESTREAM_SRC_OFFLINE_HITS` echten Offline-Treffern in
  Folge (Default 2).
- `unknown` (Proxy/Rate-Limit/403) zählt NICHT als offline — nur echtes
  Offline. Ein zwischenzeitliches „live" setzt den Zähler zurück.
- Watcher nur nach Autostart (manueller Start/Reconnect bleibt unberührt).

Der **Studio-Chat** zeigt automatisch den TikTok-Chat der gerade gerestreamten
Quelle: der Chat-Feed routet gegen die aktive Restream-Registry, und beim
Failover-Switch wird der Chat-Guardian für die neue Quelle neu gestartet.

## Multi-Plattform: tee- vs. independent-Modus (echte Unabhängigkeit)
Zwei Modi via `RESTREAM_MULTI_MODE`:
- **`tee`** (Default): EIN ffmpeg-Prozess dupliziert einen Encode an alle Ziele.
  Wenig CPU. `onfail=ignore` macht die Ziele ausfall-unabhängig (totes Ziel
  reißt andere nicht mit) — aber alle hängen am selben Prozess.
- **`independent`**: ein EIGENER ffmpeg-Relay-Prozess pro Plattform. Echte
  Unabhängigkeit — Twitch kann ausfallen/neustarten (eigener Reconnect-Loop),
  ohne Kick oder YouTube zu stören. Kostet mehr CPU (ein Encode je Ziel).
  Kick bleibt der Hauptprozess (unveränderte Logik), Twitch/YouTube laufen als
  separate Zusatz-Relays.

**Encode-Modus** gilt für beide: `transcode` (festes 2s-GOP, plattformkonform,
Default bei Multi-Target) oder `copy` (kein Re-Encode). Der copy-Modus bei
Multi-Target ist standardmäßig gesperrt (erzwingt transcode für saubere
Keyframes); zum Testen `RESTREAM_MULTI_ALLOW_COPY=1` — funktioniert aber nur,
wenn die TikTok-Quelle bereits ~2s-Keyframes liefert.

4-Felder-Matrix (tee/independent × copy/transcode) logisch verifiziert.

## Mobile-Dashboard
Die Chip-Reihen (Plattformen, AZRAEL-Kanäle) liefen auf dem Handy rechts aus
dem Bild. Jetzt: horizontal scrollbar mit Snap, Header/Sendeleiste brechen um,
Tabs scrollbar, Überschriften umbrechend, kompaktere Paddings. Zwei Breakpoints
(≤760px, ≤420px).

## Control-Tab: Restream-Ziel-Status
**Bugfix**: Gingen Kick und Twitch gleichzeitig live, blieb Kick offline. Ursache:
der ffmpeg-tee-Muxer hatte kein `onfail=ignore` — ein zickendes Zusatzziel
(Twitch beim Connect) riss den gesamten Fan-out ab, Kick ging mit. Jetzt trägt
JEDES tee-Ziel `onfail=ignore`: Kick (Primär) läuft weiter, egal ob Twitch/
YouTube klemmen. Logik nach **`nc/restream_targets.py`** extrahiert (multistream_
targets + robuster tee-Bau), gegen alle Kombinationen E2E-getestet.

**Control-Tab**: Die Plattform-Chips zeigen jetzt Chat- UND Restream-Status
getrennt (📡 SENDET/bereit/konfig. + 💬 liest/live). Deck-API um `restream`-Feld
erweitert (is_target/live/primary je Plattform).

## /start + /about aktualisiert
Beide Telegram-Infotexte auf NIGHTCRAWLER v37 gebracht (vorher „TKT-OPS v2"):
Brain-Kommandos, Multi-Restream, SENTINEL-SHIELD, korrekter Stack (llama.cpp/
Whisper/Piper). Neu: **Entwickler-Angabe** mit TikTok-Profil
[@archangele.azrael](https://www.tiktok.com/@archangele.azrael) in `/about`.

## Modularisierung (nc/-Paket) — Start
Erste Runde der schrittweisen Entflechtung des ~29k-Zeilen-Monolithen. In sich
geschlossene, abhängigkeitsarme Einheiten wandern nach `nc/`; bot.py
re-importiert sie, sodass sich am Laufzeitverhalten **nichts** ändert:
- **`nc/shield.py`** — SENTINEL-SHIELD (reine Regex-Logik, nur re+os).
- **`nc/preflight.py`** — Stream-URL-Preflight; `log`/`RECORD_PROXY` werden per
  `configure()` injiziert (keine Rückabhängigkeit auf den Monolithen).
- **`nc/channels.py`** — geteilter Status-Container der Chat-Listener
  (WCHAT_STATUS/TWITCH_SEND/YT_SEND); Deck-API, Chat-Send und Loops nutzen
  dieselbe Quelle.
- **`nc/textutil.py`** — reine Text-/Format-Helfer (clean_username mit
  TikTok-URL-Härtung, fmt_number, safe, short); nur re+html.
- **`nc/proxyutil.py`** — Proxy-URL-Helfer (_normalize_proxy_url, _proxy_key);
  reine String-Logik.
- **`nc/fmt.py`** — Format-/Stream-Helfer (_sse, _partial_tag_hold,
  _fmt_offset, fmt_duration, fmt_size_mb, utc_clock, pre_table).
- **`nc/util.py`** — kleine Logik-Helfer (_ai_err_msg, _looks_like_vision_model,
  _safe_callback_data, _topic_key).
- **`nc/story.py`** — StoryMemory (erste extrahierte Klasse): Erzähl-Gedächtnis
  pro Live-Session, STORY_MAX_BEATS per configure() injiziert.
- **`nc/director.py`** — LiveDirector: Regie-Instanz pro Live-User (Momentum-
  Messung, Reaktions-Timing); DIRECTOR_*-Schwellen per configure() injiziert.
- `nc/proxyutil.py` zusätzlich um _proxy_scheme, _tunnel_mask und die
  ProxyHealth-Klasse (EWMA-Latenz + Erfolgsrate je Proxy) erweitert.

Nahtprüfung inzwischen AST-basiert (zuverlässig gegen Docstring-Fehlalarme):
alle 23 importierten nc-Symbole stehen nachweislich vor ihrer ersten Nutzung.

Alle nc-Importe stehen im frühen Konstantenblock (vor jeder Nutzung) — der
Bughunt fand dabei zwei echte Reihenfolge-Bugs (proxyutil in get_random_proxy,
shield im KickModerator wurden vor ihrem späten Import aufgerufen) und behob
sie. 5 Module, keine Zirkularität, alle isoliert importierbar.

Nach der Extraktion ein 5-Runden-Bughunt: Naht-Reihenfolge (Alias vor Nutzung),
configure-Timing, Shared-State-Identität unter Nebenläufigkeit, AST-
Vollständigkeit aller Symbole, Modul-E2E. Alle 8 Testsuiten grün, pyflakes 0.

## Auto-Reaktivierung + /brain unpause
- **Zweite Chance nach Karenz**: eine per Stufe 3 auto-pausierte Quelle wird
  nach `BRAIN_DEAD_RETRY_HOURS` (Default 12h) automatisch reaktiviert — kommt
  der Account zurück, läuft er weiter; bleibt er tot, greift Stufe 3 beim
  nächsten Preflight erneut. Selbstregulierend, kein manueller Eingriff nötig.
- **`/brain unpause <user>`** (Telegram) und **`/sys_unpause`** (Discord):
  auto-pausierte Quelle sofort wieder scharf schalten, löscht auch den
  Karenz-Marker.

## RecoveryAgent Stufe 3 + Warnungen in Telegram
- **Auto-Pause chronisch toter Quellen** (`BRAIN_ACT_PAUSE_DEAD_SOURCE=1`,
  Default 0): war eine Quelle 1,5× über der Alarmschwelle in Folge tot, pausiert
  der RecoveryAgent sie über einen Bot-Hook — einmalig pro Quelle (persistiert
  in `paused_sources`), damit manuelles Reaktivieren respektiert wird. Spart
  dauerhaft Poll-Ressourcen für offline/gelöschte Accounts. Restream-Quellen
  ausgenommen.
- **`/brain` zeigt Warnungen**: der Telegram-Zustand listet jetzt die aktuellen
  Warnungen der letzten 6h (Quelle tot, Watchdog, Ressourcen/Disk) — die Dinge,
  die man ohne Dashboard sehen will, direkt unter dem Kompakt-Status.

## Chronisch-tote-Quelle-Regel + Preflight-Kachel
- **Brain-Regel `source_chronically_dead`**: war eine Quelle X-mal in Folge
  beim Preflight komplett tot (alle URL-Varianten 404), meldet das Brain sie
  als Untrack-Kandidat (`💀 Quelle chronisch tot — @user: 8× in Folge tot`).
  Schwelle `BRAIN_DEAD_STREAK_ALERT` (Default 8), langer Cooldown. Der
  Streak-Zähler resettet bei jedem erfolgreichen Preflight.
- **Preflight-Kachel im System-Tab**: direkt/gerettet/tot als 24h-Zähler mit
  Klartext-Hinweis — der CDN-404-Schutz ist jetzt auch im Cockpit sichtbar,
  nicht nur im Wochenreport.

## Preflight-Telemetrie + Aufräumen
- **Preflight-Zähler als Metrik**: `preflight_ok/fallback/dead` zeigen im
  Wochenreport, wie oft der CDN-404-Quirk zuschlug — „**N×** tote HD-URL
  erkannt und umgeschwenkt (spart je ~30–60s)" plus tote Quellen ohne Spawn.
  Macht den Nutzen der B91-Absicherung schwarz auf weiß messbar.
- **Aufgeräumt**: die verwaiste Recorder-Preflight-Closure (60 Zeilen toter
  Code seit der Extraktion in `_preflight_url`) entfernt.

## Robustheit: Restream-Preflight + Twitch-Send-Härtung
- **B91-Preflight jetzt auch beim Restream-Start**: Die aufgelöste Quell-URL
  wird vor dem ffmpeg-Restream auf 404 geprüft (dieselbe `_hd`→Basis-Fallback-
  Logik wie beim Recorder, in eine wiederverwendbare Modulfunktion extrahiert).
  Tote/Battle-Stage-URLs → Status `unknown` statt 27–60s ffmpeg-Reconnect-Burn.
- **Twitch-Send abgesichert**: Schreibt der Sender in einen toten Socket, wird
  der Send-Hook invalidiert (nächster Aufruf → sauberes 503) statt still zu
  scheitern; der Loop reconnectet und registriert den Hook neu.

## YouTube-Senden (OAuth) + Reconnect-Metrik
- **AZRAEL antwortet jetzt auch auf YouTube**: mit einmalig eingerichtetem
  OAuth-Refresh-Token (SETUP_YT_OAUTH.md) sendet der Bot über die Data-API v3
  in den eigenen Live-Chat — Superchat-Dank automatisch, plus Dashboard-Chat-
  Send (Plattform YouTube) und Broadcast (▶ Alle). Access-Token wird zur
  Laufzeit selbst erneuert, liveChatId aus dem aktiven Broadcast aufgelöst.
  Ohne Token bleibt YouTube wie bisher lesend.
- **Reconnects als Metrik**: `listener_reconnects` (Summe über alle Kanäle)
  wandert als Zeitreihe in brain.db; der Wochenreport zeigt das Delta über den
  Zeitraum und markiert >20 Reconnects als „⚠ instabil".

## Listener-Stabilität + SHIELD-Zeitreihe
- **Reconnect-Zähler**: Das Chat-Listener-Panel zeigt pro Kanal Reconnects seit Bot-Start (↻N, gelb) und Uptime der aktuellen Verbindung — instabile Kanäle (häufige Reconnects) fallen sofort auf.
- **SHIELD als Metrik**: Die Bridge spiegelt jeden SENTINEL-SHIELD-Block cursor-basiert als Brain-Metrik (`shield_blocks` + `shield_doxxing/hate/drohung`). Damit erscheint der Schutz als **7-Tage-Sparkline** im SHIELD-Panel und als eigene Sektion im **Wochenreport** — nicht mehr nur im 24h-Fenster.

## System-Tab: Listener-Health + LLM-Latenz
Zwei neue Panels im System-Tab (05): **Chat-Listener** zeigt Kick/Twitch/
YouTube mit Verbindungsstatus, Modus (liest/sendet) und Zeit seit letzter
Nachricht (aus `/api/restream/deck`). **LLM-Latenz** zeigt das aktive Backend
(llama.cpp/Ollama) mit Ø-Antwortzeit und einer 6h-Sparkline aus der Metrik
`llm_avg_ms` — grün <1.5s, gelb <3s, rot darüber. Damit ist der Ollama→
llama.cpp-Umstieg direkt am Verlauf ablesbar.

## Control-Tab: 3-Plattform-Ausbau (W-CTRL)
Das ON-AIR-Deck zeigt jetzt **Kick, Twitch und YouTube** als Live-Status-Chips
(verbunden/getrennt/Fehler, Modus lesend/sendend, Zeit seit letzter Nachricht,
Klick öffnet den Kanal). Neue Bausteine:
- **Chat-Send aus dem Dashboard** (`POST /api/chat/send`): Nachricht direkt in
  den eigenen Kick- oder Twitch-Chat schreiben, ohne die Plattform-App zu
  öffnen. Dropdown **▶ Alle** sendet an alle sendefähigen Kanäle gleichzeitig
  ("gleich geht's los"). YouTube ist lesend (Senden bräuchte OAuth).
- **Chat-Feed** kennt jetzt Twitch- (lila) und YouTube-Badges (rot); die drei
  Plattform-Listener aus W-CHAT sind damit auch im Sendebild-Feed sichtbar.
- **SHIELD-Zähler** in der Sendeleiste (`GET /api/shield/stats`): abgewehrte
  Doxxing/Hate/Drohungs-Versuche der letzten 24h, rot wenn >0, Tooltip mit
  Aufschlüsselung nach Kategorie.

## Sofort-Verbesserungen (11.07., Runde 2)
- **`!mem <frage>`** im Kick-Chat (auch `!erinnerung`, `!damals`): AZRAEL durchsucht das semantische Gedächtnis aller Streams und antwortet mit Fundstelle+Datum. Läuft über die Oracle-Cooldowns.
- **`/brain <frage>`** in Telegram: Router-Kaskade direkt befragen; ohne Frage kompakter Systemzustand (Tick, LLM-Backend+Latenz, Regeln). **`/report`**: Wochenreport in Telegram.
- **`/healthz`**: Monitoring-Endpoint ohne Auth (nur ok/degraded) für UptimeRobot/Kuma — 200 wenn Eventloop-Heartbeats frisch und DB antwortet, sonst 503; Brain-Status informativ.
- **Tagesbriefing**: erster Brain-Tick nach Mitternacht (UTC) schreibt eine Lagemeldung ins Warum-Log — 24h-Sessions, Entscheidungen, Restream-Zustände, Go-Live-Prognose. 1×/Tag, getestet idempotent.

## Neue Fähigkeiten (W-PLUS)
- **Wochenreport**: Button `REPORT 7T` im Brain-Dashboard oder `GET /api/brain/report/weekly` (Markdown).
- **Semantik-Suche**: Suchfeld im Brain-Dashboard; Bridge indiziert `stream_memories` alle 5 min automatisch. Voraussetzung: `ollama pull nomic-embed-text` (oder llama.cpp mit `--embeddings`).
- **Selbstheilung Stufe 2**: `BRAIN_ACT_RESTREAM_RESTART=1` — RecoveryAgent startet tote Restreams über die Bot-Eventloop neu (2 Versuche/h, dann Krit-Finding im Warum-Log).
- **Sendeleiste**: Go-Live-Countdown (Brain-Prognose) + bei Multi-Restream klickbare Quellen-Pills (Stop pro rid).
- **brain.db im 04:00-Backup** als konsistenter SQL-Dump (`db/brain_<stamp>.sql`).
- **llama.cpp**: fertige Unit in `llama-server.service` (Port 8089, `--embeddings` gleich aktiv → ein Backend für Chat UND Semantik: `BRAIN_EMBED_BACKEND=llamacpp`, `BRAIN_EMBED_URL=http://127.0.0.1:8080`).

## Deploy (auf ns3068954)

```bash
cd /pfad/zum/projekt
# 0. Backup des aktuellen Dashboards
cp templates/dashboard.html templates/dashboard_v36.bak.html
# 1. Entpacken — legt bot.py, brain/, brain_bridge.py und
#    templates/dashboard.html (mit Tab 06 AI BRAIN) + templates/brain.html ab
unzip -o NIGHTCRAWLER_v37_complete.zip
# 2. Selbsttests auf dem Server (keine Abhängigkeit außer Flask für M2-Test)
python3 -m brain.test_m1 && python3 -m brain.test_m3 && \
python3 -m brain.test_m4 && python3 -m brain.test_m5 && \
python3 -m brain.test_m6 && python3 -m brain.test_m7 && \
python3 test_m2_bridge.py
# 3. systemd auf bot.py umstellen
sed -i 's/bot_v36.py/bot.py/' /etc/systemd/system/nightcrawler.service
systemctl daemon-reload && systemctl restart nightcrawler
# 4. Prüfen
curl -s localhost:8050/api/brain/overview | head -c 400
# Browser: Dashboard → Tab 06 AI BRAIN (oder Taste 6, oder direkt /brain)
```

Rollback = systemd zurück auf bot_v36.py. brain.db ist isoliert — die
bot-DB wird vom Brain nie geschrieben (einzige Ausnahme: RecoveryAgent
mit explizitem `BRAIN_ACT_RECOVERY=1`).

## Die 3 Patches in bot.py (Suchmarke `V37-P`)

| Patch | Ort | Verhalten |
|---|---|---|
| V37-P1 | `main()` nach `init_db()` | startet die Bridge; try/except → ohne brain/ läuft v36-Verhalten |
| V37-P2 | `ollama_chat()` | `AI_PROVIDER=brain` routet Text über die Brain-Runtime (llama.cpp→Ollama), fail-open auf den alten Pfad; Vision bleibt immer Ollama |
| V37-P4 | Regie + Kick-Listener | Gifts: eigener Kanal wird bedankt, getrackte Streams nur kommentiert |
| V37-P5 | Restream-Manager | Multi-Restream-Registry, Chat-Routing für parallele Quellen, Deck-API-Feld `all` |
| V37-P6 | Overlay/Studio/ffmpeg | **W-MULTI**: pro Restream eigene Overlay-Dateien (`rid_<n>/`), Studio-Chat-Panel pro Quelle gefiltert, rid durch die komplette ffmpeg-Kette gefädelt, F97-Purge multi-fest, Sendeleiste zeigt alle aktiven Quellen |
| V37-P3 | `_schedule_next_check()` | `BRAIN_HINTS_POLL=1` lässt M5-Hints das Poll-Intervall **nur verkürzen** (wie X3), 60s-Cache, fail-open |

## Env-Schalter (Auszug — vollständig in .env dokumentiert)

| Schalter | Default | Wirkung |
|---|---|---|
| `AI_PROVIDER` | *(leer)* | `brain` = LLM-Anfragen über llama.cpp-Runtime |
| `BRAIN_HINTS_POLL` | 0 | Scheduler-Hints fürs adaptive Polling nutzen |
| `BRAIN_ACT_RECOVERY` | 0 | RecoveryAgent darf stale recording-Flags räumen |
| `BRAIN_ACT_BRAIN_DB_BIG` | 0 | Selbstwartung brain.db (GC+VACUUM) |
| `BRAIN_LLM_BACKEND` | auto | llamacpp / ollama / auto / off |
| `BRAIN_LLM_MAX_CALLS_H` | 30 | hartes Tier-4-Stundenbudget |
| `BRAIN_AGENT_<NAME>` | 1 | Agent-Default (Laufzeit-Toggle überstimmt) |
| `AZRAEL_THANK_OWN_GIFTS` | 1 | Dank für Subs/Gifts im eigenen Kick-Chat (P4b) |
| `AZRAEL_THANK_TRACKED_GIFTS` | 0 | Altverhalten: Dank für fremde TikTok-Gifts (P4a) |
| `TWITCH_CHANNEL` / `TWITCH_CHAT_TOKEN` | – | Twitch-Chat lesen; mit Token auch Sub/Bits-Dank (W-CHAT) |
| `YOUTUBE_CHANNEL` | – | YouTube-Live-Chat lesen, Superchats aufs Overlay (W-CHAT) |
| `AZRAEL_VOICE_PER_STREAM` | 0 | TTS-Stimme pro Restream-Quelle statt nur primär (P7b) |
| `BRAIN_ACT_RESTREAM_RESTART` | 0 | Selbstheilung Stufe 2: tote Restreams neu starten, max 2/h (W-PLUS) |
| `BRAIN_EMBED_BACKEND/URL/MODEL` | ollama | Semantisches Gedächtnis; `ollama pull nomic-embed-text` (W-PLUS) |

**Multi-Restream (W-MULTI):** Parallel laufende Restreams haben jetzt je
eigenes Studio-Panel mit NUR dem Chat ihrer Quelle (Kick läuft überall mit),
eigene source.txt, gespiegelte Kanal-Overlays. Der PRIMÄRE (zuletzt
gestartete) Restream nutzt weiterhin exakt die v36-Pfade — bestehende
OBS-/ffmpeg-Setups bleiben unberührt. Grenze: TTS-Stimme und Avatar hängen
weiterhin am primären Stream (eine AZRAEL-Stimme, bewusst).

Empfohlene Reihenfolge: 1–2 Wochen reine Beobachtung (alle Gates aus,
`/brain` → "Entscheidungen · Warum?" lesen), dann Gates einzeln öffnen.

## LLM-Runtime (Ollama-Ablösung)

Siehe `SETUP_LLAMACPP.md` — llama-server + Qwen2.5-1.5B-Instruct GGUF Q4_K_M,
4 dedizierte Kerne, systemd-Unit. Danach `BRAIN_LLM_BACKEND=llamacpp`
setzen und Ollama abschalten.

## Test-Matrix (alle grün bei Auslieferung)

| Suite | Deckt ab |
|---|---|
| brain.test_m1 | State/Rules/Router/Persistenz/Tick |
| test_m2_bridge | DB-Sync, 10 Regeln, Cooldowns, Flask-Routen, Cleanup |
| brain.test_m3 | Sessions, recorded-Flag, Flap, Profile, Metriken, Crash-Recovery |
| brain.test_m4 | Graph-Ableitung, Idempotenz, Prune, erklärbare Empfehlung |
| brain.test_m5 | Go-Live-Prognose, Flap-Schutz, Hints, CPU-Forecast, Aktions-Gate |
| brain.test_m6 | LLM-Backends, Fallback, Budget, Concurrency-Slot, Tier 4 |
| brain.test_m7 | Agenten-Registry, Toggle-Persistenz, Isolation, Recovery, Brier |

Statik: py_compile OK · pyflakes 0 (v36-Baseline 0 → v37 0) ·
ruff F/E9/B: keine neuen Findings · Dashboard-JS node-geprüft ·
E2E: 12 API-Endpunkte gegen Flask-Testclient.

## Website (separat deploybar)

`website/lafap_index.html` → als `index.html` auf lafap.de (NICHT in templates/ — gehört nicht zum Bot).
Platzhalter ersetzen: `DEIN-KANAL` (Kick/YouTube/Twitch),
`DEIN-INVITE` (Discord). `/impressum.html` und `/datenschutz.html`
sind verlinkt und müssen angelegt werden (DE-Pflicht).
