# NIGHTCRAWLER v37 — Arbeitsgrundlage

> 🌐 **Deutsch** (maßgeblich) · [English](CLAUDE.en.md)

TikTok-Live-Überwachung, Aufnahme, Multi-Ziel-Restream und KI-Moderation
(AZRAEL). Ein Python-Monolith plus zwei bot-freie Bibliotheken, betrieben als
systemd-Dienst auf einer 8-Kern-Ubuntu-Box. Auslieferung läuft per ZIP über den
Bestand, nicht per `git pull`, siehe `.claude/skills/nc-betrieb`. Das
GitHub-Repo trägt Historie, CI und Issues — es ist nicht der Deploy-Weg.

## Die eine Regel

`bot.py` hat **22.609 Zeilen / 1,2 MB ≈ 293.000 Token**. Diese Datei wird
**nie** ganz gelesen und **nie** blind durchsucht. Erst fragen wo etwas steht,
dann den Ausschnitt holen:

    python tools/ncpatch.py find "donations"               # wo ist X? (~100 Token)
    python tools/ncpatch.py sym  bot.py api_brain      # Zeilenbereich eines Symbols
    python tools/ncpatch.py show bot.py 24750 24810    # nur diesen Ausschnitt
    python tools/ncpatch.py grep "tree.command" bot.py -C 3
    python tools/ncpatch.py map                            # Karte neu bauen
    python tools/ncpatch.py verify patches/x.json          # Trockenlauf
    python tools/ncpatch.py apply  patches/x.json          # alles-oder-nichts, legt .bak an
    python tools/ncpatch.py check                          # Templates: doppelte IDs, CSS-Bilanz
    python tools/ncpatch.py docs                           # Doku-Zahlen gegen den Quelltext

`find` antwortet aus `.claude/INDEX.md` — 361 Routen (34 in `bot.py`, 327 in
`nc/routes/`), 45 Slash-Commands, 474 Funktionen mit Zeilennummern. Nach Änderungen an Routen, Commands oder
Top-Level-Funktionen `map` neu laufen lassen. Details: Skill `nc-navigation`.

Für „wer ruft das auf?" und „was ist der Typ?" ist der Sprachserver billiger als
jede Suche: `findReferences`, `incomingCalls`, `goToDefinition`, `hover`.

Auf diesem Windows-Rechner heißt der Interpreter **`python`** (3.13.12);
`python3` existiert nicht. Auf dem Server ist es `python3`.

## Aufbau

    bot.py               Monolith: Telegram, Flask-Dashboard (34 eigene
                         Routen), Scraper, Recorder, Restream, Schema (init_db).
                         Hiess bis v4.0-W119 bot_v37.py — beim Suchen in
                         alten Notizen und Patch-Dateien daran denken.
    discordbot.py        Der Discord-Teil (45 Slash-Commands), seit v4.2-W15
                         heraus. Bot-seitig, weil er discord.py importiert und
                         ein Gateway aufmacht — nicht nach nc/, das bot-frei
                         bleibt. Bekommt alles per starte(ctx), importiert
                         NIE aus bot.py.
    nc/botctx.py         Der eine Kanal dorthin: BotKontext (eingefroren).
    telegramversand.py   Der Versandweg der Aufnahmen (split_and_send_video),
                         seit v4.2-W19 heraus. Ebenfalls bot-seitig: er braucht
                         telegram.error zur Laufzeit. Bekommt fuenf Helfer per
                         konfiguriere(), importiert NIE aus bot.py.
    brain_bridge.py      Adapter Bot ↔ brain/ (M2)
    brain/               KI-Kern: state, rules, router, agents, memory,
                         semantic, knowledge, scheduler, llm, report
    nc/                  132 Fachmodule: db, scraping, restream, oauth, ledger,
                         i18n, …
    nc/routes/           36 Flask-Blueprints mit 327 weiteren API-Routen
    locales/             de.json, en.json — der Übersetzungskatalog
    templates/           dashboard.html, brain.html, overlay.html, PWA
    website/             lafap_index.html (öffentliche Seite)
    tools/ncpatch.py     Patch- und Prüfwerkzeug
    docs/                Sämtliche Anleitungen und Historie — DEPLOY,
                         START_HIER, CONTRIBUTING, SECURITY, CHANGELOG,
                         README_V37, die SETUP_*-Anleitungen. In der Wurzel
                         liegt an Text nur noch README.md (Einstieg),
                         CLAUDE.md (diese Datei, muss dort liegen, sonst
                         findet Claude Code sie nicht) und LICENSE.
    .claude/skills/      Arbeitsanweisungen — hier und nur hier findet Claude
                         Code sie. Gehören mit ins Auslieferungs-Archiv
                         (früher lagen sie unter skills/, dort wurden sie nie
                         geladen).

**Architektur-Grenze, die gilt:** `nc/*`, `brain/*` und `discordbot.py`
importieren **nie** aus `bot.py`. Konfiguration kommt per `configure(...)`-Injection. Das hält beides
isoliert testbar und verhindert Zirkularimporte. `brain/` ist thread-basiert und
stdlib-only (`urllib`, kein `aiohttp`).

## Pflicht-Prüfkette — vor JEDER Auslieferung

    python -m py_compile <geänderte .py>
    python -m pyflakes   <geänderte .py>        # 0 Befunde
    python -m ruff check --select F,E9,B --ignore B905 <geänderte .py>
    python tools/ncpatch.py check
    python tools/ncpatch.py docs
    python tools/i18n_extract.py --check en
    python test_smoke.py ; python test_nc_modules.py ; python test_restream.py

**Auf diesem Windows-Rechner gilt vorher `$env:PYTHONUTF8="1"`.** Die Tests
öffnen `bot.py` ohne `encoding=`; ohne UTF-8-Modus greift cp1252 und sie
sterben mit `UnicodeDecodeError` statt zu prüfen. Auf dem Server ist UTF-8
Default, dort ist nichts zu setzen.

**`test_smoke.py` läuft seit v4.1-W31 in der CI** — Job `Rauchtest (bot.py
laeuft wirklich)`. Die alte Begründung („braucht den vollen Serverbestand")
war falsch: TikTokLive und python-telegram-bot stubbt der Test selbst, alles
andere wird erst in Funktionen importiert. Übrig bleiben fünf Pakete in
`requirements-smoke.txt`, Installation rund 20 Sekunden. Lokal:

    python -m pip install -r requirements-smoke.txt
    python test_smoke.py

`requirements-smoke.txt` ist die **einzige** Stelle, an der ein neues
Fremdpaket für den Rauchtest einzutragen ist. Der Vertrag
`_test_w31_rauchtest_laeuft_in_der_ci` vergleicht die Modul-Ebene von
`bot.py`, `nc/` und `brain/` gegen diese Liste und meldet jedes fehlende
Paket mit Datei und Namen — statt den CI-Job an einem nackten `ImportError`
sterben zu lassen. Er meldet auch tote Einträge: eine Liste, die still
wächst, macht den Job wieder teuer.

Die statischen Verträge in `test_restream.py` verankern sich an **wörtlichem
Quelltext** von `bot.py`. Ändert sich eine Signatur, kippt der Vertrag,
obwohl der Code stimmt — dreimal passiert (`stop(self, rid)` wurde
`stop(self, rid, _keep_desired=False)`). Ebenso die Fenster der Form
`src[i:i + 3000]`: wächst die Funktion darüber hinaus, meldet der Test etwas
als fehlend, das zwei Zeilen weiter unten steht. **Vor jedem Fix am Code erst
prüfen, ob der Vertrag oder nur sein Anker gebrochen ist.**

Bei JS in `templates/*.html` zusätzlich Script-Blöcke extrahieren und
`node --check` fahren (JSON-LD als JSON prüfen, nicht als JS).

Zusätzlich immer: keine doppelten Top-Level-Defs (`ast.parse` → `module.body`),
keine doppelten Flask-Routen **inklusive `methods=`** (gleicher Pfad mit
GET und POST ist kein Duplikat — ein naiver Regex meldet Fehlalarm).

## Fallstricke, die schon zugeschlagen haben

**Stille `except`-Blöcke sind der Hauptfeind.** Der Bot fängt großflächig ab und
loggt auf `warning`/`debug`. Ein `log.warning` erscheint in einem ERROR-Log
**nie** — so blieb der Discord-Gateway-Tod monatelang unsichtbar. Wenn etwas
„nicht mehr geht", suche zuerst das `except`, das den Grund frisst.

Für periodische Schleifen gibt es dafür **`_loop_fehler(name, exc)`**: erste
Meldung sofort auf `error` mit Traceback, danach höchstens alle 15 Minuten eine
— mit der Zahl der unterdrückten Fälle. Jeder Dauerläufer-Wächter gehört
dorthin, nie auf `log.debug` und nie auf `pass`. Legitim still bleiben nur
Aufräumpfade, deren Fehlschlag bedeutungslos ist (`proc.terminate()` auf einen
toten Prozess, `os.remove()` auf eine bereits gelöschte Datei) und der
Fehlerkanal selbst — dort erzeugt Loggen eine Rekursion.

**Modul-Konstanten frieren `.env` ein.** `.env` wird teils erst nach den ersten
Imports geladen. Konfiguration als Funktion lesen (`_backend_conf()`), nie als
Modul-Konstante.

**Einmal-`await` ohne Supervisor.** Jeder Long-Running-Client braucht Reconnect
mit Backoff **und** ein Abbruchkriterium für deterministische Fehler.

**Guards als Objekt-Attribut.** `getattr(client, "_started", False)` bricht,
sobald das Objekt neu erzeugt wird → parallele Endlosschleifen. Modul-global
guarden.

**Vertragsbrüche zum `brain/`.** Bei Änderungen an `router.route(topic, payload)`
alle Callsites prüfen: `grep -n 'router.route('`. Ein Key-Drift (`prompt` vs.
`question`) fiel nur im Telegram-Pfad aus, weil die Flask-Route den richtigen
Key benutzte.

## Geld — nicht vermischen

`REVENUE_PLATFORMS = ("kick","twitch","youtube","manuell")`. **TikTok gehört nie
dazu**: TikTok-Gifts gehen an den getrackten Streamer, nicht an eigene Kanäle.
Sie werden als `kind="gift"` gespeichert, nie als `donation`, und laufen in keine
Geldsumme.

`/api/donations/summary` ist Live-Telemetrie aus **Schätzwerten**.
`nc/ledger.py` sind gebuchte **Auszahlungen** für die Steuer. Niemals das eine
aus dem anderen ableiten — Anzeigewert ≠ Auszahlung ≠ Zuflusszeitpunkt.
Ledger-Einträge sind append-only mit Hash-Kette; Korrektur = Gegenbuchung.

## Sicherheit

`.env` hat rund 508 Variablen und enthält Cookies, OAuth-Tokens und Stream-Keys — sie
liegt nie im Archiv und wird nie ausgegeben. Beim Logging von
`streamlink`/`ffmpeg`-Kommandos werden Cookie-Header redacted (F4); dieser
Redact-Pfad darf bei Änderungen an der Kommandozeile nicht umgangen werden. Das
Dashboard bindet standardmäßig auf `127.0.0.1:8050`; Zugriff läuft über
SSH-Tunnel, nicht über Öffnen des Ports.

## Sprache und Ton

Code-Kommentare und alle Ausgaben auf Deutsch. Kommentare erklären **warum**,
nicht was — bevorzugt mit dem konkreten Fehlerbild, das die Zeile verhindert.
Antworten an den Betreiber: knapp, entscheidungsfreudig, ohne Weichspüler.

**Benutzertexte sind seit v4.1-W6 mehrsprachig.** Der deutsche String ist der
Schlüssel, `locales/en.json` trägt das Englische. Ein fehlender Eintrag fällt
auf Deutsch zurück statt auf einen nackten Schlüsselnamen. Nach Änderungen an
Benutzertext `tools/i18n_extract.py --check en` laufen lassen — es meldet
fehlende **und** verwaiste Einträge. Logzeilen bleiben absichtlich deutsch: sie
sind für den Betreiber und laufen nie durch die Übersetzungsschicht.

## Arbeitsweise

In Wellen liefern, jede Welle validiert und abgeschlossen. Nach jeder Welle
Zwischenstand melden und auf „weiter" warten. Deploy läuft direkt gegen
Produktion mit anschließender Log- und Screenshot-Beobachtung — Änderungen
müssen deshalb einzeln verifizierbar und rückrollbar sein.

## Skills

| Skill | Wofür |
|---|---|
| `nc-navigation` | **Zuerst.** Etwas finden, ohne den Monolithen zu durchsuchen |
| `nightcrawler` | Änderungen an `bot.py`, `nc/`, `brain/` — Anker-Patching, Validierung |
| `html-templates` | `templates/*.html`, `website/*.html` — Themen Messing/Blaupause, Prüfkette |
| `nc-betrieb` | Deploy, systemd, Log-Lesen, Rollback, CrowdSec, Kick-Störungen |
| `nc-datenbank` | SQL und Schema unter SQLite **und** MariaDB |
| `nc-ki-backends` | `nc/freeai`, `brain/llm`, AZRAEL, Tier-Modell, Budget |
