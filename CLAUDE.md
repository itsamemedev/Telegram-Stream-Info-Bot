# NIGHTCRAWLER v37 — Arbeitsgrundlage

> 🌐 **Deutsch** (maßgeblich) · [English](CLAUDE.en.md)

TikTok-Live-Überwachung, Aufnahme, Multi-Ziel-Restream und KI-Moderation
(AZRAEL). Ein Python-Monolith plus zwei bot-freie Bibliotheken, betrieben als
systemd-Dienst auf einer 8-Kern-Ubuntu-Box. Auslieferung läuft per ZIP über den
Bestand, nicht per `git pull`, siehe `.claude/skills/nc-betrieb`. Das
GitHub-Repo trägt Historie, CI und Issues — es ist nicht der Deploy-Weg.

## Die eine Regel

`bot.py` hat **24.798 Zeilen / 1,2 MB ≈ 295.000 Token**. Diese Datei wird
**nie** ganz gelesen und **nie** blind durchsucht. Erst fragen wo etwas steht,
dann den Ausschnitt holen:

    python tools/ncpatch.py find "donations"               # wo ist X? (~100 Token)
    python tools/ncpatch.py sym  bot.py api_brain      # Zeilenbereich eines Symbols
    python tools/ncpatch.py show bot.py 24750 24810    # nur diesen Ausschnitt
    python tools/ncpatch.py grep "tree.command" bot.py -C 3
    python tools/ncpatch.py map                            # Karte neu bauen
    python tools/ncpatch.py map --check                    # ist die Karte aktuell?
    python tools/ncpatch.py verify patches/x.json          # Trockenlauf
    python tools/ncpatch.py apply  patches/x.json          # alles-oder-nichts, legt .bak an
    python tools/ncpatch.py check                          # Templates: doppelte IDs, CSS-Bilanz
    python tools/ncpatch.py docs                           # Doku-Zahlen gegen den Quelltext

`find` antwortet aus `.claude/INDEX.md` — 369 Routen (34 in `bot.py`, 333 in
`nc/routes/`), 60 Slash-Commands, 553 Funktionen mit Zeilennummern. Nach Änderungen an Routen, Commands oder
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
    discordbot.py        Der Discord-Teil (60 Slash-Commands, davon 15 in
                         einer Schleife statt per Dekorator), seit v4.2-W15
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
    nc/                  147 Fachmodule: db, scraping, restream, oauth, ledger,
                         i18n, …
    nc/routes/           36 Flask-Blueprints mit 335 weiteren API-Routen
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
    python tools/ncpatch.py map --check
    python tools/stillecheck.py --sperre
    python tools/vertragscheck.py --sperre
    python tools/importzeit.py    --sperre   # braucht requirements-smoke.txt
    python tools/abhaengigkeiten.py --sperre
    python tools/monolith.py      --sperre
    python tools/blindstellen.py  --sperre
    python tools/testmuell.py     --sperre   # die Suiten lassen nichts liegen
    python tools/ueberdeckung.py  --sperre   # braucht coverage + die Suiten
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

**Die Suiten sind seit v4.2-W86 auch einzeln fahrbar.** Bis dahin gab es genau
einen Weg hinein — `python test_nc_modules.py`, alles oder nichts, rund eine
Minute je Lauf. Der Grund war kein Vorsatz: der Aufbau der Testdatenbank stand
mitten in `main()`, also bekam ein einzeln aufgerufener Vertrag keine
konfigurierte Datenbank, `db_conn()` fiel auf den Vorgabepfad zurück und legte
ein `tiktok_bot.db` **im Arbeitsverzeichnis** an. Beim zweiten Lauf starb
`_test_dbexport` an „table dbx_t already exists".

    python -m pytest                                    alle 344 einzeln (~47 s)
    python -m pytest -k w83                             nur eine Welle
    python -m pytest "test_nc_modules.py::_test_dbexport"   genau einer (0,06 s)

`conftest.py` ruft denselben `richte_testdatenbank_ein()` auf wie `main()`.
**Beide Wege bleiben** — `python test_nc_modules.py` ist und bleibt das, was
die Prüfkette fährt und was die Sperre ist; pytest kommt daneben, für die
Arbeit am einzelnen Befund.

**Die Überdeckung ist seit v4.2-W86 gemessen: 52,4 %** von `nc/` und `brain/`
(20.231 Anweisungen, 9.631 davon ungeprüft). Das ist die Zahl, die den 546
Verträgen erst ihren Maßstab gibt — „alles grün" sagt sonst nichts darüber,
wie viel Bestand dabei angefasst wurde. Gesperrt wird wie bei W65/W66 nur der
Zuwachs, und zwar die **Anzahl** ungeprüfter Anweisungen, nicht der
Prozentsatz: ein Prozentsatz springt auch dann, wenn nichts schlechter wurde.

**Sieben Module standen auf null bis 16 %** und sind seit v4.2-W87 bei 92 bis
100 %: `director`, `scraper`, `scoring`, `preflight`, `tiktokcheck`,
`archiverules`, `storage`. In `director.py` lag dabei eine Geldregel aus
diesem Dokument ungesichert — TikTok-Gifts gehen an den **getrackten
Streamer**, nicht an eigene Kanäle; AZRAEL hat sich dafür einmal bedankt
(V37-P4a, „peinlich und irreführend"), der Vorgabewert wurde umgedreht, und
seither hielt ihn nichts. In `scraper.py` waren es die beiden
`resp.release()`, ohne die jeder Wiederholungsversuch eine Verbindung leckt.

**Die 14 Verdachtsstellen aus W87 sind seit v4.2-W89 behoben.** Acht
Korrekturen, jede mit Vertrag und Mutationsprobe. Drei davon sind die Klasse
Fehler, die dieses Dokument meint:

`nc/preflight.py` hatte `except Exception: return u` **in** der
Kandidatenschleife. Ein Timeout auf der zweiten URL-Variante beendete die
Suche und gab das Original zurück, das zwei Zeilen vorher schon 404 war.
Schlimmer war die Gegenrichtung: `None` heißt „tot", „tot" füttert
`_PREFLIGHT_DEAD_STREAK`, und daran hängt die Brain-Regel
`source_chronically_dead` mit „Untracken erwägen". Ein Netzhänger auf dem
eigenen Server durfte damit einen **lebenden Account zum Entfernen
vorschlagen**. Der Störfall zählt jetzt auf `_PREFLIGHT_STATS["gestoert"]` und
lässt die Tot-Strähne unberührt.

`nc/storage.py` teilte die Bytes der letzten sieben Tage durch die Zahl der
Tage **mit** Aufnahmen — `GROUP BY` liefert nur solche. Im Vertrag gemessen:
aus „Platte voll in 10 Tagen" wird 35. Stumpf durch sieben zu teilen wäre die
gefährlichere Hälfte desselben Fehlers (ein junger Bestand hat strukturell
leere Tage, und dann ist die Prognose zu optimistisch). Entschieden wird an
einer Ja/Nein-Frage: gibt es Aufnahmen vor dem Fenster?

`nc/archiverules.py` ließ eine Kopie ohne Datenbankzeile liegen, wenn der
INSERT fiel — und `os.path.exists` sperrte die Aufnahme danach **für immer**
vom Archiv aus. Es fiel nichts, es wurde nur nichts mehr.

**Jede gesicherte Aussage ist per Mutationsprobe gegengeprüft** — die Stelle
im Produktionscode gezielt brechen und nachsehen, ob der Vertrag fällt. Ein
Vertrag, der auf gesundem Code grün ist, aber die Regression nicht fängt, ist
wertlos. In W89 entwischten beim ersten Durchgang zwei von 17: der
Erfolgspfad, der die Meldedrossel zurücksetzt, war von keinem Vertrag gedeckt,
und eine Pfad-Riegel-Probe lief ins Leere, weil die Attrappen-Quelldatei unter
dem bösen Namen gar nicht existierte und `copy2` schon vorher scheiterte.
**Eine Probe, die entwischt, ist ein Befund am Vertrag, nicht am Code.**

Dasselbe gilt für die Überdeckungssperre. W89 hat 49 Anweisungen hinzugefügt
und fünf davon zunächst ungeprüft gelassen — alle fünf waren die neuen
Fehlerpfade. Die Sperre lässt sich mit `--neu-grundlinie` heben; richtig war,
nachzusehen, welche fünf es sind, und sie zu decken. Die Grundlinie steht
deshalb unverändert bei **9695**, obwohl der Bestand gewachsen ist. Eine
Grundlinie, die bei jeder Welle mitwächst, ist keine.

**Dabei die Falle, die diese Proben selbst wertlos macht:** Python prüft den
Bytecode-Cache über **(mtime, Größe)**. Eine Mutation wie `404` → `410` ist
größengleich; wird sie innerhalb derselben mtime-Sekunde zurückgeschrieben,
hält Python die `.pyc` für gültig und führt **weiter den mutierten Code aus**.
Genau so ist hier ein grüner Vertrag nachträglich „gefallen", obwohl `git
status` sauber war. Vor jeder Mutationsreihe deshalb
`find . -name __pycache__ -exec rm -rf {} +` und mit
`PYTHONDONTWRITEBYTECODE=1` fahren.

Die statischen Verträge in `test_restream.py` verankern sich an **wörtlichem
Quelltext** von `bot.py`. Ändert sich eine Signatur, kippt der Vertrag,
obwohl der Code stimmt — dreimal passiert (`stop(self, rid)` wurde
`stop(self, rid, _keep_desired=False)`). Ebenso die Fenster der Form
`src[i:i + 3000]`: wächst die Funktion darüber hinaus, meldet der Test etwas
als fehlend, das zwei Zeilen weiter unten steht.

Seit v4.2-W66 ist auch das gemessen: **34 solche Fenster** im Code der beiden
Suiten (`tools/vertragscheck.py`). Die elf, die randvoll waren, laufen jetzt
über `rumpf_ab(quelle, ab)` — von der Fundstelle bis zur nächsten
Top-Level-Definition, also mitwachsend. Die übrigen haben gemessen Luft
(`--spielraum` verkleinert jedes Fenster einzeln und fährt die Suite); sie
anzufassen wäre Risiko ohne Nutzen gewesen. `--sperre` verhindert neue. **Vor jedem Fix am Code erst
prüfen, ob der Vertrag oder nur sein Anker gebrochen ist.**

Bei JS in `templates/*.html` zusätzlich Script-Blöcke extrahieren und
`node --check` fahren (JSON-LD als JSON prüfen, nicht als JS).

Zusätzlich immer: keine doppelten Top-Level-Defs (`ast.parse` → `module.body`),
keine doppelten Flask-Routen **inklusive `methods=`** (gleicher Pfad mit
GET und POST ist kein Duplikat — ein naiver Regex meldet Fehlalarm).

## Fallstricke, die schon zugeschlagen haben

**Stille `except`-Blöcke sind der Hauptfeind.** Seit v4.2-W65 ist das keine
Behauptung mehr, sondern gemessen: **1746 `except`-Blöcke, davon 1085 ohne
jede Meldung** (`python tools/stillecheck.py`). Jede Welle der Reihe W51–W64
kam aus dieser Klasse. Der Bestand darf bleiben, er darf nur nicht *wachsen* —
`stillecheck.py --sperre` fällt in der CI, sobald irgendwo ein stiller Block
dazukommt. Legitim still sind Aufräumpfade, der Fehlerkanal und
Abbruch-Signale (`CancelledError`); die erkennt der Klassierer selbst.

Der Bot fängt großflächig ab und
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

**Stille `except`-Blöcke sind nur die halbe Blindheit.** Die andere Hälfte
hat der Betreiber am 13.09. gemeldet: „whisper/transkript funktioniert immer
noch nicht" und „Chats können von online tiktok Usern geladen werden aber
keine gültigen streams". Beide Wege scheitern **ohne Absturz** — sie kehren
ordentlich zurück, nur mit leerem Ergebnis. `stillecheck` fällt dort nicht:
es gibt keinen stillen `except`, sondern ein **stilles `return`**.

`_resolve_via_webcast_api_v2` hatte elf solche Ausgänge, acht auf `log.debug`
und drei ganz ohne Zeile; `_whisper_transcribe` verschluckte jeden Fehler auf
`debug`. Ein `log.debug` erscheint in einem INFO- oder ERROR-Log **nie** —
für den Betreiber ist ein Fehlerpfad auf `debug` dasselbe wie `pass`.
`tools/blindstellen.py` misst diese Klasse, Bestand **464**, und wie bei
W65/W66 wird nur das Wachstum gesperrt.

Auf `warning` heben allein genügt aber nicht: der Resolver läuft pro Poll und
pro verfolgtem Nutzer, ungedrosselt wäre das Log nach einer Stunde unlesbar —
und eine unlesbare Warnung ist so gut wie keine. Deshalb geht jede dieser
Meldungen durch **`nc/meldetakt.py`**: erste Meldung sofort, ein *Wechsel des
Grundes* sofort (dass aus einem Timeout ein 403 geworden ist, ist die
eigentliche Nachricht), sonst höchstens alle 15 Minuten mit der Zahl der
unterdrückten Fälle. Der Schlüssel ist der **Kanal**, nicht der Nutzer — bei
200 Trackings drosselt ein Schlüssel je Nutzer gar nichts. Und der Erfolgspfad
setzt die Drossel zurück, sonst bleibt ein wiederkehrender Ausfall bis zu 15
Minuten unsichtbar. Die Klartexte stehen in `nc/resolvergrund.py`, jeder **mit
Abhilfe**: „HTTP 403" allein hat schon einmal wochenlang niemandem geholfen.

**Ein stiller `except` machte aus „räum die Reste weg" ein „lösche alle
Aufnahmen".** `_find_orphans()` in `nc/routes/recordings.py` liest die Liste
der bekannten Dateien aus der Datenbank und meldet jede Datei im
Aufnahmeverzeichnis, die nicht darin steht. Um die Abfrage stand bis v4.2-W91:

    except Exception:
        known = set()

Mit leerem `known` ist `full not in known` für **jede** Datei wahr — jede
`.mp4` bekommt den Grund „kein-db-eintrag", und `/api/rec/orphans/clean`
löscht alles, was die Funktion liefert. Ein gesperrtes SQLite genügte, und
das ist bei laufendem Recorder Alltag.

Der gefährliche Ablauf brauchte nicht einmal Pech: das Deck lädt erst
`/api/rec/orphans` (Datenbank in Ordnung, drei Reste) und schickt dann den
Knopf mit `confirm=true`. Fällt die Datenbank zwischen diesen beiden
Aufrufen, hat der Betreiber das Löschen von drei Dateien bestätigt und alle
verloren. **Es gibt hier keine sichere Annahme:** „ich weiß nicht, was in der
Datenbank steht" heißt „ich kann nicht entscheiden, was verwaist ist" — also
abbrechen (`BestandUnbekannt`, HTTP 503), nicht raten.

Dieselbe Welle: `/api/rec/retention/apply` löschte den Datenbank-Eintrag auch
dann, wenn `os.remove` scheiterte. Die Aufnahme belegte weiter Platz, tauchte
in keiner Liste mehr auf, und das Deck meldete den Platz als frei — die
Umkehrung des W89-Befunds in `archiverules.py`. **Wer die Datei nicht löschen
kann, darf auch ihre Spur nicht löschen.**

**Die Meldung selbst hielt den Event-Loop an.** Der Voll-Stack-Dump vom
18.09. 22:15 endet nicht in einer Netzoperation, sondern hier:

    File "httpx/_client.py", line 1740, in _send_single_request
        logger.info(
    File "logging/__init__.py", line 1026, in handle
        with self.lock:                     <<< hier stand der Event-Loop

Drei synchrone Handler am Wurzel-Logger — Konsole (unter systemd eine Pipe
nach journald) und zwei `RotatingFileHandler` — teilen ihre Sperren mit 21
Threads. Auf einer Platte unter Volllast dauert ein Schreibvorgang Sekunden,
und **jeder** `log.info` im Loop wartet mit. Gemessen: bis 176,5 s
eingefrorener Loop, Bridge-Tick 182 s tot, Restream 225 s ohne Bild,
`disk-guard` 444 s ohne Lebenszeichen, Discord-Heartbeat blockiert, am Ende
`database is locked`. Nichts stürzt ab, nichts meldet sich — dieselbe Klasse
wie die stillen `return`s aus W81, nur ist die Ursache diesmal das Logging.

Seit v4.2-W97 hängt am Wurzel-Logger nur noch ein `QueueHandler`
(`nc/logschleuse.py`), die echten Handler bedient ein Thread. Gemessen an
einem Handler mit 20 ms je Logzeile: 1,006 s → 0,001 s für zwanzig
Ausgaben. Die
Schlange ist **begrenzt** — eine unbegrenzte tauscht den eingefrorenen Loop
gegen einen OOM-Kill —, sie wartet nie, und jeder Verlust wird gemeldet.
`/healthz` trägt `log_wartend` und `log_verloren`; ohne Schleuse ist
`log_wartend` **−1**, nicht 0: eine 0 liest sich wie Normalbetrieb.
**Wer eine Logzeile schreibt, darf dafür nie auf die Platte warten.**

**Eine Drossel, die jeden Grundwechsel sofort durchlässt, drosselt nichts.**
`nc/meldetakt.py` meldete bis W97 jeden Grund sofort, der sich vom *vorigen*
unterschied. Das setzt voraus, dass ein Kanal zu einer Zeit EINEN
vorherrschenden Grund hat. Der Resolver-Kanal tut das nicht — er läuft pro
Poll über 40 verfolgte Nutzer, und jeder erzeugt der Reihe nach
`status_code`, dann `html_kein_tag`. Damit war jeder Aufruf ein Wechsel:
**13675 Warnungen in 22 Stunden**, 5315 davon mit Unterdrückt-Zähler.

Die Ruhezeit hängt seither am Paar (Kanal, Grund). Ein wirklich neuer Grund
meldet weiter sofort, ein zurückkehrender erst nach 15 Minuten; aus 200
abwechselnden Aufrufen werden zwei laute Zeilen. Es ist derselbe Fehler, vor
dem der Docstring des Moduls seit W81 warnt (Schlüssel = Kanal, nicht
Nutzer), nur eine Ebene tiefer.

**Ein Kommentar über die Eingabe ist kein Beweis über die Eingabe.**
`concat_cmd` begründet sein `-safe 0` seit W44 damit, dass „die Liste
absolute Pfade trägt". Die Liste trug relative — `RECORDINGS_DIR` ist ein
relativer Name, also steht `recordings/xyz.mp4` in der Datenbank. Der
concat-Demuxer löst einen relativen Eintrag gegen das Verzeichnis der
**Listendatei** auf, und die liegt in `recordings/`:

    Impossible to open 'recordings/recordings/tiktok_live_….mp4'

Damit scheiterte **jedes** Zusammenfügen einer Sitzung, dreimal am 19.09.
gemessen. Grün geblieben ist der W44-Vertrag, weil er ausschliesslich Pfade
ab `/rec/…` hereinreichte — die Eingabe der Produktion hat er nie gesehen.
Ein Vertrag, der nur die bequeme Eingabe prüft, prüft nichts.

**Ein Bestand hat zwei Richtungen, und das Archiv kannte nur eine.**
`/api/archive/check` prüft die Datenbank gegen die Platte (Einträge ohne
Datei). Die Gegenrichtung — Dateien ohne Eintrag — gab es bis v4.2-W98
nicht, und damit war eine von Hand hineinkopierte Aufnahme im Deck schlicht
nicht vorhanden. Nach einem Neuaufbau der Datenbank betrifft das den
kompletten Bestand. Seither: `/api/archive/scan` (lesend) und
`/api/archive/scan/adopt` (trägt ein, verschiebt und löscht nichts), im Deck
der Knopf „Ordner prüfen". **Bei jedem Abgleich zwischen Datenbank und
Dateisystem beide Richtungen prüfen — eine davon fehlt sonst jahrelang
unbemerkt.**

Dabei zweimal dieselben Lehren wie eine Welle vorher. Die Pfade werden auf
**beiden** Seiten mit `abspath` verglichen: in der Datenbank kann ein
relativer stehen (`ARCHIVE_DIR` darf relativ sein, die Vorgabe ist
`"archive"`), im Scan entsteht ein absoluter — ohne Normalisierung sieht
jeder bestehende Eintrag wie ein neuer aus und der Knopf bietet an, das
Archiv doppelt aufzunehmen. Und fällt die Datenbankabfrage aus, bricht der
Scan ab (`BestandUnbekannt`, HTTP 503) statt zu raten, genau wie
`_find_orphans` seit W91 — hier mit umgekehrtem Vorzeichen: dort hätte
Raten alles gelöscht, hier würde es alles doppelt eintragen.

**Ein nachweislich dichter Riegel ist für CodeQL kein Riegel.** Der
Ordner-Scan aus W98 nahm zuerst die Pfade aus der Anfrage und prüfte sie mit
`nc.sicherpfad.unter()`. Dicht — der Vertrag fing den `../`-Ausbruch — und
trotzdem zwei High-Severity-Befunde „Uncontrolled data used in path
expression" auf `os.path.isfile` und `os.path.getsize`: die
Datenflussanalyse sieht die Barriere nicht. Dasselbe war bei
`api_recording_session_join` schon einmal der Fall.

Die Antwort ist beide Male dieselbe und steht schon dort: die Abfrage blind
zu entschärfen hieße, eine Prüfung abzuschalten, die sich nicht nachprüfen
lässt — **den Pfad gar nicht erst aus Fremdeingabe bauen.** `uebernehmen`
scannt deshalb selbst und nimmt nur Pfade aus `os.walk` über den
serverseitigen Ordner; aus der Anfrage kommt eine Liste relativer Namen, die
als Filter per Zeichenketten-Vergleich wirkt. Der `sicherpfad`-Import ist
dabei entfallen: ein Riegel gegen Fremdeingabe, wo keine mehr ankommt, ist
toter Code, der Sicherheit suggeriert. Der Vertrag prüft seither die
stärkere Aussage — kein Name bringt eine Datei von außerhalb ins Archiv.

**Eine Sperre, die fällt, will nicht immer eine neue Grundlinie.** In W98
fiel der Vertrag, der die rohen Env-Lesepfade in `nc/routes/archive.py`
zählt, weil die neue Scan-Route die Ordner-Auflösung aus
`api_archive_duplicates` kopiert hatte. Richtig war nicht, von eins auf zwei
zu gehen, sondern die Dublette aufzulösen: beide Ordner-Knöpfe rufen jetzt
dieselbe Funktion und sehen damit nachweislich denselben Ordner — was der
Kommentar ohnehin behauptete.

**Ein Datenbank-Tausch ohne das WAL ist lautlos wertlos.** SQLite laeuft hier
im WAL-Modus. Wer nur `tiktok_bot.db` ersetzt und `-wal` liegen laesst,
bekommt nach dem Neustart den **alten** Stand zurueck — mit sauberem
`integrity_check`, also ohne einen einzigen Hinweis. Gemessen in v4.2-W96,
bevor `nc/dbrestore.einsetzen()` existierte. Hauptdatei **und** `-wal`/`-shm`
gehoeren zur Seite, sonst spielt SQLite das alte Journal auf die neue Datei.
Und der laufende Prozess haelt die alte Datei am **inode** fest: was er bis
zum Neustart schreibt, ist danach weg. Das laesst sich nicht wegprogrammieren,
nur sagen.

**Backup und Import passten nicht zueinander.** Der Betreiber am 18.09.:
„Über die Backup Funktion im dashboard lassen sich keine SQL Dateien
importieren da sämtliche Tabellen schon existieren." Zwei Formate:
`nc/dbexport.py` schreibt **nur Daten** (Kopf `-- NIGHTCRAWLER-DB-EXPORT`,
gebaut für den Umzug SQLite ↔ MariaDB), `_system_backup()` schreibt
`sqlite3 .iterdump()` — **Schema und Daten**. Die Sicherung erzeugt also
genau das, was der Importer nicht lesen kann.

Schlimmer: er lehnte nicht ab, sondern lief **halb** durch. Die `CREATE TABLE`
fielen, die `INSERT` liefen, und `db_conn` committet beim *sauberen*
Verlassen — ein abgefangener Fehler ist für den Kontextmanager sauber.
Gemessen: `angewandt: 7` von 9. Seit v4.2-W95 greift der Riegel **vor** dem
ersten Schreibzugriff, und ein Teilfehler rollt zurück. Wiederhergestellt wird
mit `tools/dbwiederher.py`, und zwar **ohne Bot**: ist die Datenbank unlesbar,
gibt es kein Dashboard (W92, Exitcode 3) — ein Rettungsweg, der den laufenden
Bot voraussetzt, fehlt genau dann, wenn man ihn braucht.

**Und die Diagnose aus W92 riet dann falsch.** Am 18.09. brach der Start
korrekt ab, nannte Datei, Größe und Hex und warnte vor dem Löschen — und
endete mit „STRUKTURIERTE Daten. Diese Datei aufzugeben wäre verfrüht",
**ohne einen Weg zu nennen**. Dieselbe Art Meldung wie ein blankes „HTTP 403",
eine Ebene tiefer.

Die Antwort stand im Log: **401408 = 4096 × 98**, exakt 98 SQLite-Seiten. Der
TLS-Record ist 5 + 0x2d = 50 Bytes. Zerstört war der 100-Byte-**Kopf**, nicht
die Datenbank — die Datei wurde angeschrieben, nicht ersetzt.

Schlimmer war der aktive Fehlrat: die Diagnose fand `CREATE TABLE`, hielt die
Datei für einen SQL-Dump und empfahl `sqlite3 neu.db < datei`. Das **kann**
nicht laufen. `CREATE TABLE` steht in **jeder** SQLite-Datei, weil das Schema
wörtlich in `sqlite_master` liegt; gemessen an einer echten Datei: `CREATE
TABLE` 1 Treffer, `INSERT INTO` **0**. Der Dump-Verdacht hängt seit v4.2-W94
an `INSERT INTO`/`BEGIN TRANSACTION`, und `tools/dbkopf.py` setzt den Kopf neu
— Seitengröße durchprobiert, **`PRAGMA integrity_check` entscheidet**, wörtlich
`ok` und nichts sonst. „Keine Ausnahme" als Kriterium hätte eine zu 85 % leere
Datenbank als Rettung ausgegeben (gemessen: 308 von 2000 Datensätzen bei falscher
Seitengröße). Die Eingabedatei wird nur mit `"rb"` geöffnet.

**Der Bot schreibt das nicht.** Nachgesehen wurde vor dem Bauen: alle
`DB_PATH`-Stellen, Restore-Routen, der Backup-Pfad, rohe
Netz-nach-Datei-Schreibvorgänge, `close_fds`/`pass_fds`, jedes Öffnen ohne
Truncate. Außer `sqlite3.connect` fasst nichts den Pfad an.

**Ein zwölfzeiliger Traceback sagte so wenig wie ein blankes „HTTP 403".**
Das Log vom 18.09. trägt sechsmal denselben Block aus elf fremden
Bibliotheksrahmen und endet jedes Mal auf `telegram.error.Conflict:
terminated by other getUpdates request`. Kein Rahmen davon liegt in unserem
Code — es gibt darin nichts nachzusehen. Das ist die **Umkehrung von W92**:
dort war die Meldung zu kurz, hier ist sie zu lang, und beide sagen dem
Betreiber nichts.

Der Laut war aber nicht der eigentliche Befund. Ein `Conflict` hat zwei
Bedeutungen, und im Log sehen sie **wortgleich** aus: beim Neustart hält die
alte Instanz ihren Long-Poll noch (am 18.09. 57 Sekunden lang, dann wieder
HTTP 200) — völlig harmlos. Läuft dagegen wirklich eine zweite Instanz mit
demselben `BOT_TOKEN`, hört es nie auf, und dann gehen die Updates **dorthin**:
dieser Bot nimmt weiter auf, sendet weiter und moderiert weiter, er bekommt
nur keinen Telegram-Befehl mehr. Nichts stürzt ab, nichts meldet sich — es
geht bloß nichts. Dieselbe Klasse wie die stillen `return`s aus W81, nur
eine Schicht höher.

Unterscheidbar sind die beiden allein an der **Dauer**. Die misst seit
v4.2-W93 `nc/telegramfehler.py`, und `start_polling(error_callback=…)` hängt
den eigenen Kanal ein — `add_error_handler` taugt dafür **nicht**, der fängt
Fehler beim *Verarbeiten* eines Updates, nicht beim Abholen. Innerhalb der
Gnadenfrist eine Warnzeile mit dem Hinweis, dass ein Neustart genau so
aussieht; darüber hinaus ein ERROR mit Dauer, Folge und Abhilfe. Weil dabei
der Grund-Schlüssel wechselt, lässt `nc/meldetakt.py` die Eskalation sofort
durch statt sie in die 15-Minuten-Drossel zu stecken.

**Das Log nannte die Adresse des Decks mit dem falschen Schema.** Zwei Zeilen
im Abstand von 19 Millisekunden, dasselbe Log: `Dashboard-TLS aktiv:
https://<host>:8050` und `Dashboard: http://0.0.0.0:8050`. Die zweite ist die
mit der vollständigen Adresse, also die, die man kopiert — und sie war falsch.
Es ist derselbe Befund wie bei der Bindung in W84 („die WIRKLICHE Adresse
nennen, nicht die gewünschte"), eine Zeile weiter: dort war es der Host, hier
das Schema. Die Ursache war beide Male dieselbe — die Antwort stand nur in
`run_flask()`, und `main()` riet. Seit v4.2-W93 beantwortet
`nc/webserver.tls_lage()` die Frage einmal für beide, und `_dashboard_adresse()`
baut die Zeile als **ein** benannter Schritt.

Dabei fiel die Sperre aus W74 zu Recht: `main()` stand genau auf der
300er-Stufe, und fünf zusätzliche Zeilen hätten sie darüber gehoben. Die Zeile
herauszulösen war deshalb nicht Kosmetik, sondern die Arbeit.

**Ein Release-Build machte die Suite rot.** `tools/build_release.py` schreibt
`AUSLIEFERUNG.json` in den Arbeitsbaum, damit der Stempel ins Archiv wandert —
und räumte ihn dort nie weg. Die Datei steht in `.gitignore`, fällt bei `git
status` also nicht auf; `nc/auslieferung.py` bevorzugt sie aber vor `git`.
Nach einem einzigen Build meldeten `/healthz` und `/api/version` auf dem
Entwicklungsrechner dauerhaft den eingefrorenen Stand, und der W85-Vertrag
fiel mit „aus einem git-Arbeitsbaum heraus darf die Herkunft nicht unbekannt
sein" — eine rote Suite ohne Codefehler, deren Meldung auf die Herkunft zeigt
statt auf den liegengebliebenen Stempel. Seit v4.2-W91 entfernt der Bauer ihn
wieder, aber nur, wenn er ihn selbst angelegt hat: in einem entpackten Archiv
gehört er dorthin.

**Die teuerste Fehlermeldung des Bestands war die kuerzeste.** Am 17.09. lag
statt der Datenbank ein 108-MB-Blob im Arbeitsverzeichnis, und der Start endete
so:

    File "nc/dbwrap.py", line 370, in db_conn
      conn.execute("PRAGMA synchronous=NORMAL")
    sqlite3.DatabaseError: file is not a database

Drei Dateien Traceback, und keine Angabe, die weiterhilft: welche Datei, wie
gross, was steht stattdessen drin, was ist zu tun. In der gefaehrlichsten Lage
des Systems ist das dieselbe Art Meldung wie ein blankes „HTTP 403" — richtig
und nutzlos. Die naheliegende Reaktion, die Datei zu loeschen, damit es wieder
laeuft, kostet Trackings, Aufnahme-Eintraege und den Ledger; SQLite legt bei
**fehlender** Datei eine neue an, und der Verlust waere still.

Seit v4.2-W92 nennt `nc/dbwrap.datei_diagnose()` Pfad, Groesse, die ersten
Bytes als Hex, eine Deutung und die Abhilfe. `DatenbankUnlesbar` erbt von
`sqlite3.DatabaseError`, damit die rund 208 Aufrufstellen von `db_conn()`
unveraendert weiter fangen; der Start bricht mit Exitcode 3 ab, statt eine
leere Datenbank anzulegen.

**Und die erste Fassung dieser Diagnose beriet falsch.** Sie sah nur die
ersten 16 Bytes, erkannte dort einen TLS-Record und riet „aus ihr ist nichts
zu holen". Beim Betreiber steckten dahinter **33.444 Treffer** mit
CREATE-TABLE- und INSERT-Vokabular, 10 MB komprimierten auf 2 MB — ein
SQL-Dump, also seine vollstaendigen Daten. Der Kopf allein entscheidet nichts;
`_inhalt_befund()` probt deshalb Anfang, **Mitte und Ende** und prueft drei
Dinge: liegt irgendwo ein SQLite-Header (dann `dd skip=`), gibt es
Dump-Vokabular (dann `sqlite3 neu.db < datei`), und laesst sich der Inhalt
komprimieren — verschluesselte Daten tun das nicht. **Ein falscher Rat ist in
dieser Lage teurer als gar keiner.**

**Die Sperren waren selbst blind.** Vier der Zählwerkzeuge — `monolith`,
`stillecheck`, `blindstellen`, `importzeit` — hatten dieselbe Schleife, und
jede endete mit `except (OSError, SyntaxError): continue`. Das ist der stille
`except`-Block, gegen den sie gebaut wurden, an der Stelle, an der er am
teuersten ist: `bot.py` ist rund die Hälfte des Produktionscodes. Fällt die
Datei aus der Messung, meldet die Sperre nicht „ich konnte nicht nachsehen",
sondern einen **Fortschritt** — auf Python 3.11 gemessen `stillecheck: OK —
733 stille Blöcke, –352 seit der Grundlinie` bei tatsächlich 1085, und
`monolith:` meldete auf der 100er-Stufe 22 statt 63. Beides mit Exitcode 0.

Seit v4.2-W83 parst alles über **`tools/quelle.py`**, und eine unlesbare Datei
bricht ab: Exitcode **2**, getrennt von der 1, die „der Bestand ist gewachsen"
bedeutet. Dazu `pflicht_erfuellt` gegen den Fall, den keine Ausnahme meldet —
ein Glob, der ins Leere zeigt, nimmt `bot.py` genauso lautlos aus der Zählung.
`vertragscheck` hatte den Fehler nie; es liest ungefangen.

**Die Suiten füllten die Platte des Entwicklers.** 35 `tempfile.mkdtemp()`,
drei `shutil.rmtree` — der Rest blieb liegen, pro Lauf. Auf der Maschine, auf
der W89 entstand, waren nach einem Tag Arbeit **5093 Verzeichnisse mit rund
30 GB** aufgelaufen, und die Prüfkette brach mitten im Lauf ab: `df` meldete
1,1 MB frei bei 38 GB belegt, `OSError: [Errno 28] No space left on device`.
Kein Vertrag war rot, keine Sperre fiel — es ging nur nichts mehr. In der CI
fällt das nie auf: ein Lauf, frischer Container, danach ist die Maschine weg.
Genau deshalb konnte es wachsen, und genau deshalb prüft die CI es seit
v4.2-W90 **für** die Entwicklungsrechner mit (`tools/testmuell.py`, Grenze
null).

Der Kostentreiber war dabei nicht die Zahl der Verzeichnisse, sondern **eine
Zeile**:

    f.write(b"\0" * (300 * 1024 * 1024))    # 300 MB (sparse)

Der Kommentar sagt „sparse", der Code ist das Gegenteil — erst ein 300-MB-
Objekt im RAM, dann 300 MB echte Nullen auf die Platte, je Lauf, für eine
Zahl, die `os.path.getsize()` auch von einer Datei mit bloß gesetzter Größe
liefert. `pruefhilfen.attrappe()` nutzt `truncate()`: gemessen 0,000 s statt
0,31 s und 0 statt 614.400 belegten Blöcken. Das ist erlaubt, **solange** der
geprüfte Code die Größe aus den Metadaten liest; ein Vertrag hält
`nc/videoteil`, `nc/storage` und `nc/archiverules` darauf fest und fällt,
sobald dort `st_blocks` auftaucht.

**Dasselbe Muster zweimal an einem Tag:** auch die neue Sperre trug im ersten
Entwurf einen Kommentar über die Falle („`300 * 1024 * 1024` steht als
verschachtelter BinOp im Baum") und benutzte dann `ast.literal_eval`, das
Multiplikation ablehnt — sie hätte genau die 300-MB-Zeile nicht gefunden, für
die sie gebaut wurde. Gefangen hat das die Mutationsprobe, nicht das
Nachdenken. **Ein Kommentar, der die Absicht beschreibt, ist kein Beweis, dass
der Code sie erfüllt.**

**Die Navigationskarte wurde von nichts geprüft.** `.claude/INDEX.md` trägt die
„eine Regel" dieses Projekts und war am 13.09. in **483 Einträgen** veraltet —
`/healthz` stand auf 17805 und lag auf 17839. Ein Index, dessen
Zeilennummern um 34 danebenliegen, ist schlimmer als keiner: er schickt jedes
`ncpatch show` an die falsche Stelle. `ncpatch map --check` steht seit v4.2-W83 in der Prüfkette und
in der CI.

**Vorwärts-Migration beantwortet die Rollback-Frage nicht.** Das Schema wird
bei jedem Start idempotent nachgezogen — das ist richtig und bleibt. Es sagt
nur nichts über den einzigen wirklich gefährlichen Fall: Ausgeliefert wird per
ZIP direkt gegen Produktion, der Rollback ist „die vorige ZIP wieder
drüberlegen", und die **Datenbank rollt nicht mit zurück**. Neue Spalten und
Tabellen stören alten Code nicht; gefährlich ist eine Spalte, deren
*Bedeutung* sich geändert hat, und die sieht man erst an falschen Zahlen.

Seit v4.2-W85 trägt die Datenbank einen Zähler (`nc/schemastand.py`,
`ERWARTET`). Gleichstand ist **still**, ein niedrigerer Stand eine INFO-Zeile,
ein **höherer** ein ERROR mit beiden Zahlen — und er wird *nicht*
heruntergeschrieben, sonst wäre die Spur nach einem Start weg. Hochzählen nur,
wenn sich die Bedeutung bestehender Daten ändert; für eine neue Tabelle oder
eine neue Spalte mit Vorgabewert **nicht** — ein Zähler, der bei jeder
Kleinigkeit springt, meldet nur Rauschen.

**Der laufende Bestand ließ sich keinem Commit zuordnen.** `tools/deploy.sh`
liefert sauber aus, aber nichts prüfte hinterher die Herkunft: ein Handgriff
direkt auf dem Server war unsichtbar und wurde beim nächsten Deploy wortlos
überschrieben. Seit v4.2-W85 schreibt `build_release.py` eine
`AUSLIEFERUNG.json` ins Archiv, und `nc/auslieferung.py` meldet sie beim Start,
in `/healthz` und in `/api/version` — aus dem Archiv, ersatzweise aus `git`,
sonst ehrlich „unbekannt".

**Die Vorlage kannte sechs Variablen selbst nicht.** `.env.example` wird als
Vorlage **aller** Variablen geführt — und enthielt keine der sechs
`DONATION_<COIN>_ADDRESS`. `tools/gen_env_example.py` sucht wörtliches
`os.getenv("NAME")`; `nc/crypto.py` liest `os.getenv(env)` mit `env` aus einer
Schleife über `_COINS`. Wer seine `.env` aus der Vorlage neu aufbaute, verlor
damit sämtliche Spendenadressen, und die öffentliche Seite versteckte den Block
still. Gemeldet am 30.09.: „es fehlen sämtliche krypto wallet Adressen".

Seit v4.2-W99 löst `dynamische_namen()` den Namen aus der Liste auf, und eine
Lesestelle, die **kein** Weg erreicht, bricht den Generator ab (Exitcode 2).
Gezählt beim Trennen: 21 dynamische Lesestellen, **15 davon Durchleitung** —
dort steht das Literal beim Aufrufer, und sie als Lücke zu melden hätte 15
Fehlalarme ergeben. Es ist der dritte Fall dieser Klasse in derselben Datei;
die beiden Vorgänger (`_BERECHNET`, `_ohne_kommentar`) haben je den Einzelfall
behoben. **Beim dritten Mal gehört die Klasse gesperrt, nicht der Fall
behoben.**

**Ein leerer Block ist keine Auskunft.** Dieselbe Welle, drei stille Schichten
übereinander: `except Exception: stats["crypto"] = {"addresses": []}` im
Server, `catch(e){}` in der Seite, und ein `hidden`-Block, der nur bei Treffern
sichtbar wird. „Nichts konfiguriert" und „Ausfall" sahen identisch aus.
`snapshot()` nennt jetzt einen Grund **und die gesuchten env-Namen**, der Bot
meldet den leeren Fall gedrosselt mit diesen Namen, und die Seite sagt bei
einem Ausfall einen Satz statt zu verschwinden. Bei jeder Anzeige, die etwas
weglässt: **unterscheiden, ob nichts da ist oder nichts geladen wurde.**

**`stats.json` darf nie ins Archiv.** Sie entsteht zur Laufzeit im Ordner der
Seite und fuhr bis v4.2-W99 mit. Ein Deploy hätte damit das Live-Lagebild des
Servers mit dem Stand des Entwicklungsrechners überschrieben — eingefrorene
Zahlen, und `git status` fällt dabei nicht auf. Dieselbe Falle wie
`AUSLIEFERUNG.json` in W91. `news.json` fährt weiter mit: Inhalt, keine Messung.

**Exitcode 0 nach einem fatalen Fehler macht die Totmann-Meldung wertlos.**
Stirbt `run_bot`, gilt der Task für `asyncio.wait(..., FIRST_COMPLETED)` als
„completed"; `main()` fuhr ordentlich herunter und der Prozess endete mit
**0**. Der Installer verdrahtet `OnFailure=nightcrawler-notify@%n.service`,
und `tools/notify_failure.sh` ist genau dafür gebaut, dass ein ganz
gestorbener Bot nicht stundenlang unbemerkt bleibt — bei 0 feuert sie nicht.
Mit `Restart=always` lief der Dienst alle zehn Sekunden im Kreis, ohne dass
jemand etwas erfuhr. Reproduziert mit dem Zustand, in dem **jede frische
Installation steht**: `BOT_TOKEN` ist leer, weil der Installer ihn nicht
erfinden kann.

Seit v4.2-W100 bleiben Signal und Abbruch 0; ein gestorbener Telegram-Teil
endet mit **4** (1 und 2 belegt der Selbsttest, 3 die unlesbare Datenbank).
Die Abschiedszeile sagt dazu, warum. **Ein Prozess, der seine Arbeit nicht
tun kann, muss das dem Dienstverwalter sagen — sonst ist jede Alarmierung
daran wirkungslos.**

**Ein Selbsttest, der die Startbedingung nicht kennt, sagt „STARTKLAR" und
liegt falsch.** `_selfcheck` hatte 21 Prüfungen, den
`DISCORD_BOT_TOKEN` darunter — `BOT_TOKEN` nicht. Gemessen an einer frischen
Installation: „STARTKLAR · 13 ok · 7 Warnungen · 0 Fehler", und eine Sekunde
später starb der Start. Seit v4.2-W100 geprüft, und als **Fehler**: eine
Warnung meldet weiter STARTKLAR, und genau diese Auskunft war falsch.

**Zwei Listen für denselben Zweck, zum dritten Mal.** Der Installer kopierte
den Quelltext mit einer eigenen Ausschlussliste — zweimal hingeschrieben
(rsync und tar) und abweichend von der des Auslieferungsarchivs. Mitgewandert
sind `.coverage`, `.pytest_cache/`, `.ruff_cache/` und ein 4-MB-Release-ZIP
(gemessen: 21 MB statt 14 MB). Jetzt eine Liste für beide Wege. Dazu lag eine
Streudatei `-- No entries --` im Git, die der Installer in jede Installation
kopierte.

**Und der Bericht druckte einen Befehl, der nicht laufen kann:**
`…/.venv/bin/python/bot.py --selfcheck` — ein Schrägstrich statt eines
Leerzeichens, in genau der Zeile, die man kopiert. Dieselbe Klasse wie die
Dashboard-Adresse in W93.

**Eine Konfigurationsdatei, die die Umgebung überstimmt.** `tools/motd.sh`
sagt im Kopf „per `/etc/nightcrawler/motd.conf` **oder** Umgebung
überschreibbar" und lud die Datei **nach** den Vorgaben — sie gewann damit
immer. Aufgefallen ist es daran, dass zwei MOTD-Verträge rot wurden, sobald
auf derselben Maschine eine Installation gelaufen war: **eine Suite, die vom
Systemzustand abhängt, prüft nicht mehr nur den Code.** In der CI fällt das
nie auf — frischer Container, kein `/etc`-Zustand. Beide fahren jetzt mit
`CONF=/dev/null`, und die Reihenfolge ist Umgebung > Datei > Vorgabe.

Der erste Entwurf dieser Reparatur war wirkungslos und entwertete die Datei
vollständig: die Momentaufnahme der gesetzten Variablen stand **hinter** dem
Vorgabenblock, und `WIDTH="${WIDTH:-54}"` *setzt* WIDTH — eine Prüfung auf
„ist gesetzt" ist danach für jede Variable wahr. Gefangen hat das der eigene
Vertrag, nicht das Nachdenken. **Wer in einer Shell die Umgebung von den
Vorgaben unterscheiden will, muss das vor der ersten Zuweisung tun.**

**Der Chat braucht keine Stream-Adresse, der Restream schon.** Der Betreiber
am 01.10.: „wird selten ein live restreamt, aber dennoch läuft der Chat von
getrackten usern durchs transkript". Beide Hälften gehören zusammen:
TikTokLive signiert seine Webcast-Anfragen selbst, der Raum lebt, das
Transkript füllt sich — für den Restream muss aber eine pullbare URL vorliegen.
Gemessen (W51, steht seit damals im Quelltext): **71 % der Auflösungen melden
„live" ohne Adresse.** Gast-Cookies ändern daran nichts, sie erneuern nur die
Anti-Bot-Tokens.

Der Weg, der in dieser Lage noch durchkommt, lief nie: die yt-dlp-Stufe hing an
`status == "unknown"`, und der Status ist hier „live". Und als sie lief, warf
sie die Adresse weg — `_resolve_via_ytdlp` las `manifest_url`, `url` und
`formats` als **Ja/Nein-Frage** und gab `info=None` zurück. Dazu stand an zwei
Stellen als Tatsache „Nur der HTML-Weg trägt eine URL": eine Aussage über die
eigene Hülle, nicht über yt-dlp, und **selbsterfüllend**. Seit v4.2-W102 liest
`nc/ytdlpurl.py` die Adresse aus demselben JSON, frischegeprüft, und der
yt-dlp-Weg läuft als zweiter Nachschlag. **Ein Kommentar über die Eingabe ist
kein Beweis über die Eingabe — und ein Kommentar über die eigene Funktion ist
kein Beweis über das Werkzeug, das sie aufruft.**

Die Zuordnung ist gegen `yt_dlp/extractor/tiktok.py` geprüft, nicht gegen eine
bequeme Eingabe: HLS trägt `ext=mp4` mit `protocol=m3u8_native`, `rtmp_pull_url`
trägt `ext=flv` mit `protocol=https`, und `flv_pull_url` trägt **gar kein**
`protocol`. Eine Erkennung allein am `protocol` hätte beide FLV-Formen
verworfen; ein `endswith(".flv")` jede signierte Adresse, denn die Endung steht
vor dem Query-Teil.

**`src_live = not _err` machte aus fünf Lagen zwei.** „offline" (sendet nicht)
und „keine spielbare Quell-URL" (sendet, wir kommen nicht ran) sind
verschiedene Nachrichten mit verschiedener Abhilfe. Der Wächter sah beide als
`source_live=False` und antwortete „Quelle nicht live — kein Start" — und das
ist `ACT_NONE`, das die Schleife **nie** loggt. Ein Restream, der nie anlief,
erzeugte keine einzige Zeile. `nc/resolvergrund.quelle_lage` trennt sie jetzt,
`quelle_laut` hält „offline" still (Alltag, sonst Log-Flut), und die Meldung
nennt die Abhilfe. Drei Texte behaupteten dabei eine Aussage über TikTok
(„aktuell keine weitere Live-Quelle verfügbar") — der dritte, „offline → still
überspringen", war wörtlich wahr und genau das Problem.

Dabei die Warnung aus W51 eingelöst, nicht gelöscht: ein yt-dlp-Subprozess im
häufigsten Pfad kostet bis 20 s je Poll und Nutzer, und
`_get_resolve_semaphore()` lässt nur zwei Auflösungen gleichzeitig. Deshalb
`YTDLP_NACHSCHLAG_RUHE_S` (60 s je Nutzer), und der Zeitstempel steht **vor**
dem Aufruf — ein yt-dlp im Timeout hätte die Ruhezeit sonst nie gesetzt.
**Ein Vertrag, der eine Welle vorhersieht, hinterlässt auch deren Kosten; wer
die Zusicherung anpasst, muss die Warnung daneben mitlesen.**

**Ein Meldeweg, den man sehen muss, meldet nachts nichts.** Das Deck hatte
drei — Toast (nur sichtbar, wenn man hinsieht), Benachrichtigungs-Center (nur
aufgeklappt), Browser-Push (nur bei verstecktem Tab) — und keinen hörbaren.
Seit v4.2-W101 gibt es den Signalton, und er **muss** per Knopf eingeschaltet
werden: Browser blockieren WebAudio ohne Nutzergeste. Ein automatisch
bewaffneter Ton wäre das Schlimmste von beidem — das Deck hielte sich für
alarmierend, und es käme nichts heraus. Deshalb prüft `ncTonUmschalten()` den
`ctx.state` **nach** dem `resume()`, und der Probe-Piep ist die Bestätigung.
**Wer eine Wirkung zusagt, muss sie nachsehen, nicht nur auslösen.**

Dabei zwei Lehren aus früheren Wellen, eine Schicht weiter: die Ruhezeit hängt
am Paar (Schwere, Zeit), nicht am Kanal — eine Drossel für alles verschluckt
bei einem Ereignissturm genau den Fehler-Piep, auf den es ankommt (W97). Und
die Zustandsprüfung steht **vor** dem Stempeln der Drossel: ein Piep, den
niemand gehört hat, darf die nächste echte Meldung nicht stumm machen.

**Eine Anzeige, die ganz verschwindet, ist keine Auskunft.** W99 hat den
*Ausfall* des Krypto-Spendenblocks sichtbar gemacht und den leeren Fall weiter
still versteckt — für den Betreiber sah eine zugeklappte Seite damit immer noch
aus wie ein Fehler, und der Unterschied liegt in einer Zeile `.env`. Seit
v4.2-W101 steht der Block in jedem Zustand und sagt in drei verschiedenen
Sätzen, welcher es ist; der Vertrag prüft die stärkere Aussage, dass im ganzen
Abschnitt kein `hidden=true` mehr vorkommt. Eine einzelne fehlende Adresse
kostete immer nur ihre Zeile — `nc.crypto.addresses()` nimmt die gesetzten.

Dazu der dritte Zustand, der bis dahin gar keinen hatte: `gesucht` war bei
einem Treffer leer („bei Treffern braucht niemand die Namen"). Eine
**Teilkonfiguration** ist aber der Normalfall — wer nur Bitcoin annimmt, hat
fünf leere Namen —, und eine von sechs Adressen sah damit genauso aus wie alle
sechs. `fehlend` nennt sie jetzt, und der Bot meldet das einmal gedrosselt.

**Benutzertext, der nie im Katalog landet, bleibt still deutsch.** Drei neue
Texte aus W101 wären so durchgefallen, und keiner davon hätte sich gemeldet:
eine über zwei Zeilen zusammengesetzte Toast-Meldung (zwei Bruchstücke im
Quelltext, ein ganzer Satz zur Laufzeit), ein vollständiger Satz, der auf „zu"
endet und deshalb `_BRUCHSTUECK_ENDE` traf, und ein JS-Literal mit
`\uXXXX`-Escapes — `tools/i18n_extract.py` sammelt nur Literale **ohne**
Backslash ein. Ebenso Markup im selben Literal (`'<p class="note">…'`). Nach
Änderungen an Benutzertext deshalb nicht nur auf „fehlend: 0" sehen, sondern
nachzählen, ob der neue Text überhaupt **gefunden** wurde. **Ein Schalter, der
in der englischen Oberfläche halb deutsch ist, ist eine Fehlanzeige, kein
Schönheitsfehler.**

**Modul-Konstanten frieren `.env` ein.** `.env` wird teils erst nach den ersten
Imports geladen. Konfiguration als Funktion lesen (`_backend_conf()`), nie als
Modul-Konstante.

Dieser Satz stand hier jahrelang ungeprüft, und der Bestand hat ihn an der
teuersten Stelle gebrochen: `nc/freeai.py` baute seine Basen-Liste beim Import,
und weil `nc/news.py`, `nc/marketing.py` und `nc/routes/ai.py` das Modul in die
Import-Reihe ziehen, geschah das **vor** `load_dotenv()` (bot.py:696).
`POLLINATIONS_API_KEY` und `LLM7_TOKEN` standen in der `.env` und haben nie
einen Request erreicht. Seit v4.2-W67 misst das `tools/importzeit.py`, und die
Grenze ist **null** — anders als bei den Ratschen aus W65/W66 gibt es hier
keinen Bestand zu dulden.

Der Prüfer **startet den Bot**, statt den Quelltext zu lesen: ein AST-Lauf
findet nur das wörtliche `os.getenv` auf Modul-Ebene und fand damit einen von
fünf Fällen — die anderen vier standen in einer Funktion, die auf Modul-Ebene
*aufgerufen* wird. Die 178 Lesungen in `bot.py` sind in Ordnung; sie stehen
alle nach `load_dotenv()`. Es zählt die Reihenfolge, nicht die Menge.

**Riesenfunktionen — und wo sie wirklich stehen.** Der Plan wollte lange
`RestreamManager`, `handle_recording_finished` und `KickModerator` nach `nc/`
holen. v4.2-W70 hat nachgemessen: **das ist die falsche Arbeit.** Was sich
sauber herauslösen ließ, ist heraus (`bot.py` ruft 674-mal in `nc/`); übrig
blieb Orchestrierung mit Zustand — 58 bis 77 fremde Globals je Kandidat, und
zusammen kaum reine Logik (47 + 6 + 0). Ein Umzug hieße, bis zu 77 Namen per
`configure()` hineinzureichen: kein Zerlegen, sondern ein Parameterobjekt, an
der heikelsten Stelle des Bestands. **Bitte nicht neu aufrollen.**

**Lang ist nicht gleich schwer.** Seit v4.2-W74 misst `tools/monolith.py`
beide Achsen, und die Verzweigungen sind die Liste, an der man arbeitet:

    Zeilen  Zweige  Z/Zw   Funktion
       718      18  40.0   nc/schema.py:create_schema
       716     204   3.5   discordbot.py:_discord_run_once
       616     141   4.4   bot.py:handle_recording_finished

`create_schema` ist die längste Funktion des Bestands und die mit Abstand
einfachste: eine Liste aus 42 `CREATE TABLE`, 82 der 88 Anweisungen sind ein
schlichtes `conn.execute(...)`. **Sie wird nicht zerlegt** — das wäre Kosmetik
an Code, der gegen die Produktionsdatenbank läuft, und es bräche die Regel,
die sich das Modul selbst gegeben hat: beim Umzug aus `bot.py` wurde keine
Schema-Zeile geändert, und Platzhalter wie `{txt_idx}` stehen genau deshalb
unverändert in jeder Anweisung. Bitte nicht neu aufrollen.

Die größte Funktion steht ohnehin nicht in `bot.py`:

     718 Z  nc/schema.py   create_schema      (bewusst ganz, s.o.)
     482 Z  discordbot.py  _discord_run_once  (1730 vor W71)
     455 Z  bot.py         handle_recording_finished  (616 vor W78)

`discordbot.py` wurde in v4.2-W15 aus `bot.py` herausgelöst, genau gegen dieses
Problem. Die Masse zog um, statt zu schrumpfen. `tools/monolith.py` misst deshalb den **ganzen**
Produktionscode und zählt, wie viele Funktionen über einer Stufe liegen —
seit v4.2-W80 sind das 63 über 100, 16 über 200, 8 über 300 und 1 über 500
Zeilen, dazu 21 über 50, 2 über 100 und keine über 150 Verzweigungen. Gezählt
wird die Anzahl, nicht die Länge: eine Sperre, die jede zusätzliche
Zeile meldet, fällt bei jeder Fehlerbehebung und ist in einer Woche
abgeschaltet.

Die Zahlen stehen so auch in `.claude/monolith_grundlinie.json`, und ein
Vertrag hält beide gegeneinander — hier stand nach W75 kurz die alte Grundlinie
(9 und 4), weil das Senken der Datei den Fließtext nicht mitnimmt und
`ncpatch docs` diese Zahlen nicht kennt. Eine Riesenfunktion bloß in eine andere Datei zu verschieben
besteht die Sperre nicht.

**Fremdpakete ohne Untergrenze.** Bis v4.2-W68 trug keiner der 17 Einträge in
`requirements.txt` ein `>=`. Jede Grenze dort ist jetzt **nachgesehen**, nicht
geschätzt — für die sechs mit API-Zwang wurde das Paket der Fassung darunter
geladen und geprüft, dass die benutzte Schnittstelle fehlt. Wer eine Grenze
ändert, prüft sie genauso, statt sie zu erben.

Der zweite Teil ist die wichtigere Lücke: der Vertrag aus v4.1-W31 prüft nur
die **Modul-Ebene** und nur gegen `requirements-smoke.txt`. Die teuren Pakete
werden erst **in Funktionen** importiert (`boto3`, `redis`, `pymysql`,
`httpx`, `faster_whisper`) — dafür gab es keine Prüfung.
`tools/abhaengigkeiten.py` deckt beides ab, Grenze null. Drei Importe sind
ausgenommen und müssen es bleiben: `segno` (mitgeliefert unter `nc/_vendor/`),
`browser_cookie3` (optional mit `ImportError`-Auffang) und Pillow (nur
`tools/`, siehe W53).

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

`.env` hat rund 539 Variablen und enthält Cookies, OAuth-Tokens und Stream-Keys — sie
liegt nie im Archiv und wird nie ausgegeben. Beim Logging von
`streamlink`/`ffmpeg`-Kommandos werden Cookie-Header redacted (F4); dieser
Redact-Pfad darf bei Änderungen an der Kommandozeile nicht umgangen werden. Das
Dashboard bindet standardmäßig auf `127.0.0.1:8050`; Zugriff läuft über
SSH-Tunnel, nicht über Öffnen des Ports. Seit v4.2-W84 ist das **erzwungen**
statt empfohlen: ohne `DASHBOARD_TOKEN` und ohne `DASHBOARD_PIN` zieht
`nc/webserver.bindung()` die Adresse auf Loopback zurück, egal was in
`WEB_HOST` steht — `DASHBOARD_OFFEN_ERLAUBEN=1` ist der dokumentierte Ausweg.
Getragen wird das Deck von **waitress** (fester Thread-Pool); der
Werkzeug-Entwicklungsserver bleibt nur, wo TLS direkt am Dashboard hängt, und
sagt dann warum. Der Token in `?token=…` setzt das Cookie und verschwindet
danach per Umleitung aus der Adresszeile.

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
| `nc-sicherheit` | Secrets, Redact-Pfad, Pfad-Riegel, Dashboard-Zugang, CodeQL, Ledger |
