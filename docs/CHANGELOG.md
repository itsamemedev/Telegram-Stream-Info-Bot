# Changelog

Alle nennenswerten Änderungen an NIGHTCRAWLER. Format angelehnt an
[Keep a Changelog](https://keepachangelog.com/de/1.1.0/).

Die maßgebliche Quelle ist [`nc/version.py`](../nc/version.py) — Dashboard-Footer,
`/api/version` und das „Was ist neu"-Panel lesen von dort. Die ausführliche
Historie aller Entwicklungswellen steht in [`README_V37.md`](README_V37.md).

---

## [Unveröffentlicht]

### Geändert — die Cookie-Gesundheit wird jetzt in `nc/cookies.py` bewertet (v4.2 W21)

147 Zeilen aus `bot.py` (→ **22.580 Zeilen**), die **nie ausgeführt worden
waren** — obwohl sie die Leiter sind, an der der Betreiber ablesen soll, warum
ein Pull 403 bekommt.

Sie liegen jetzt neben den beiden Funktionen, die zu derselben Frage gehören:
`lade_jar()` liest die Datei, `gesundheit()` bewertet sie, `_cookie_alarm_level()`
liest das Ergebnis. Kein neues Modul — drei Teile einer Frage, eine Datei.

**Sieben Zusicherungen, die vorher nicht formulierbar waren.** Die wichtigste
betrifft den Fall, der am meisten Zeit gekostet hat:

* **„403 trotz aktuellem Cookie laut Dashboard".** Ursache ist ein kritischer
  Cookie, der unter *mehreren Domains* in der Datei steht — der Browser wählt
  je Subdomain situativ, der Bot statisch und kann den falschen erwischen. Der
  Vertrag schreibt genau diese Datei und prüft, dass die Warnung kommt **und
  dass sie sagt, was zu tun ist** („bereinigen, frisch exportieren"). Ohne
  diese Meldung sieht das Deck grün aus.
* **Die Reihenfolge der Leiter hält**: kritisch vor abgelaufen vor Dubletten.
  Kippte sie, verdeckte eine Warnung einen kritischen Zustand.
* **Session-Cookies ohne Ablaufzeit gelten nicht als abgelaufen** — sonst
  meldete jede normale Datei Alarm.
* **Die Reparatur hängt an der `mtime`, nicht am Aufruf.** Das Deck pollt im
  Sekundentakt; hinge sie am Aufruf, stünde bei einer nur lesbaren Datei jede
  Sekunde ein `log.error` im Journal — und der eine echte Grund ginge darin
  unter. Der Vertrag ruft dreimal und zählt einen Reparaturversuch.
* Fehlende Datei meldet `missing` statt zu krachen; eine 45 Tage alte Datei
  ist eine Warnung; bald ablaufende Cookies melden sich vorher.

Sechs Mutationen geprüft, alle sechs schlagen an.

**Ein Anker war zu weit gefasst.** Die W10-Prüfung „lädt nicht direkt über
`MozillaCookieJar`" suchte in der ganzen Datei — und `lade_jar(` steht dort
auch in `load_dict()` und in der Definition selbst. Sie wäre grün geblieben,
während `gesundheit()` längst wieder direkt parst. Sie sucht jetzt nur noch im
Rumpf von `gesundheit()`; die Mutation bestätigt es.

### Behoben — die Pause-Grace war ab dem zweiten Aussetzer einer Sitzung wirkungslos (v4.2 W20)

**Der Fund.** In `_handle_single_tracking` stand für den Fall „Streamer ist
wieder da":

```python
if _PENDING_OFFLINE_COUNT.pop(tid, None) or _PENDING_OFFLINE_SINCE.pop(tid, None):
```

Ein `or` mit Kurzschluss. Sobald der Zähler gesetzt war — also immer, wenn
überhaupt ein Aussetzer beobachtet worden war — wurde der **zweite `pop` nie
ausgeführt**: der Startzeitpunkt der Offline-Phase blieb stehen.

Beim nächsten Aussetzer misst die Pause-Grace dann ab dem *ersten* Aussetzer
der Sitzung statt ab jetzt. `offline_for` ist sofort riesig, die
Grace-Schwelle fällt augenblicklich, und es entscheidet allein der
Debounce-Zähler. Damit war genau der Schutz weg, für den es die Grace gibt:
„Live pausiert" wird als Stream-Ende gelesen — OFFLINE-Meldung, Aufnahme
beendet, neue LIVE-Meldung beim Zurückkommen.

Die vier anderen Reset-Stellen im Monolithen räumen beide Register in zwei
getrennten Zeilen. Nur diese eine nicht.

Gefunden hat es der Vertrag, der beim Herauslösen entstand — beim allerersten
Lauf. Der Code war seit W20-Vorgeschichte unverändert; ohne die Zerlegung
hätte ihn nichts angefasst.

### Geändert — die Entscheidungen aus dem Live-Signal stehen jetzt in `nc/livefolge.py` (v4.2 W20)

Drei Rechnungen aus `_handle_single_tracking` (`bot.py`: 22.734 → **22.718**),
die reine Arithmetik sind und trotzdem in einer 380-Zeilen-Funktion steckten,
die eine Datenbank, einen Scraper und einen Recorder braucht — also hier nie
ausgeführt wurde:

* **Ist „offline" wirklich offline?** Zwei Schwellen müssen **beide** fallen:
  genug aufeinanderfolgende Beobachtungen (Debounce) *und* lange genug offline
  (Pause-Grace). Ein `or` hätte die häufigste Störung durchgelassen — zwei
  schnelle Ticks hintereinander erfüllen den Debounce, aber nicht die Grace,
  und das ist das Bild eines TikTok-Aussetzers, nicht eines beendeten Streams.
* **Ist gerade Ruhezeit?** Ein Fenster über Mitternacht (22-7) ist die
  Standardfalle: `start <= h < ende` trifft dort *nie*. Der Vertrag zählt
  jetzt alle 24 Stunden durch, für beide Fensterformen, plus `start == ende`
  (schaltet ab) und die Grenzen (Beginn zählt, Ende nicht).
* **Wann wird das nächste Mal geschaut?** Und: **„unbekannt" ist nicht
  „offline"** — die Abfrage kam nicht durch, der Streamer kann laufen. Mit
  dem Offline-Intervall behandelt hieße das, einen laufenden Stream fünf
  Minuten lang nicht anzusehen.

Dazu zwei Zusicherungen an den Aufrufstellen in `bot.py`: die Pause-Grace
rechnet in **monotoner** Zeit (mit der Wanduhr hätte ein NTP-Sprung mitten im
Stream entweder sofort „offline" gemeldet oder eine Stunde lang gar nicht),
und Priorität wie Brain-Hinweise dürfen das Poll-Intervall nur **verkürzen** —
ein Hinweis, der verlängern darf, kann ein Tracking still einschlafen lassen.

Neun Mutationen geprüft, alle neun schlagen an — die erste davon ist der oben
beschriebene Kurzschluss.

### Geändert — der Versandweg der Aufnahmen steht jetzt in `telegramversand.py` (v4.2 W19)

381 Zeilen, die eine fertige Aufnahme nach Telegram bringen: teilen, hochladen,
auf Sperren und Fehler reagieren, das Forum-Thema treffen, tote Chats merken.
`bot.py` fällt auf **22.734 Zeilen**. Zusammen mit `nc/videoteil.py` (W11, das
ffmpeg-Teilen) ist damit der komplette Weg von der Datei zum Abonnenten aus dem
Monolithen heraus.

**Bot-seitig, nicht unter `nc/`** — dieselbe Grenze wie bei `discordbot.py`
(W15): die Datei fängt `telegram.error`-Ausnahmen ab und braucht die echten
Klassen zur Laufzeit. Unter `nc/` wäre der Vertrags-Job an einem nackten
`ImportError` gestorben; dort sind nur `orjson` und `flask` installiert. Die
Grenze in die andere Richtung gilt auch hier: **kein `from bot import`.**

**Das ist der Pfad, der im Betrieb schon wehgetan hat.** Eine Chat-ID, die
Telegram mit `chat not found` beantwortet, ließ den Bot für *jede* Aufnahme
durch die komplette Teil- und Retry-Kette laufen — 176 identische Fehlerzeilen
in einer Nacht (B97). Die Sperre dagegen war Text-, aber nie verhaltensgeprüft.
Jetzt baut der Vertrag den Upload mit einer Attrappe und zählt nach:

* **Eine gesperrte Chat-ID kostet null `send_video`-Aufrufe** — und der
  Betreiber bekommt eine Meldung, die `TELEGRAM_CHAT_ID` beim Namen nennt.
* **`RetryAfter` wartet einmal und spult die Datei zurück.** Ohne `seek(0)`
  lädt der zweite Versuch **null Bytes** hoch; Telegram nimmt das an, und im
  Chat liegt eine leere Datei. Das fällt sonst nirgends auf.
* **Rate-Limit als `BadRequest`** (B46): PTB wickelt manche 429-Antworten so
  ein, der `RetryAfter`-Pfad wird dann nie erreicht.
* **Gelöschtes Forum-Thema** → Mapping verworfen und der Zweitversuch geht
  ohne `message_thread_id` in den Haupt-Chat, statt den Upload zu verlieren.
* `Forbidden` und `chat not found` sperren die Chat-ID; ein Formatfehler
  (`VIDEO_FILE_INVALID`) tut das **nicht** und erreicht stattdessen den
  Betreiber.

Sechs Mutationen geprüft, alle sechs schlagen an.

Der Rumpf ist bitgenau übernommen (gegen `git show HEAD:bot.py` verglichen).
`konfiguriere()` lehnt unbekannte und fehlende Helfer ab: ein stilles `None`
hieße hier, dass eine fertige Aufnahme beim Versand mit
`NoneType is not callable` verschwindet — also genau dann, wenn die Daten schon
da sind und nur noch rausgehen müssen.

**Anker nachgezogen, Verträge unverändert:** B97 (toter Chat) und die
W11-Prüfung, dass die vier ffmpeg-Hüllen nicht in den Monolithen
zurückkommen — letztere prüft jetzt zusätzlich, dass `bot.py` nur noch die
dünne Hülle hält. `tools/ncpatch.py` (Karte, Funktionszahl) und
`tools/i18n_extract.py` kennen die dritte bot-seitige Datei; ohne den
Extraktor-Eintrag hätte der nächste Aufräumlauf die Upload-Fehlermeldungen als
verwaist gelöscht.

### Geändert — die Eskalationsrechnung des Recorders steht jetzt in `nc/aufnahmefolge.py` (v4.2 W18)

Diesmal geht es nicht um Zeilen (`bot.py`: 23.111 → **23.103**), sondern um
**einen Zustandsautomaten, der an drei Stellen lag**: gesetzt beim
Aufnahme-Ende, zurückgesetzt beim Offline-Übergang, durchgesetzt vor dem
nächsten Spawn. Vier exponentielle Kurven mit Schwellen-Offset — und keine
davon war je ausgeführt worden, weil sie in einer 669-Zeilen-Funktion steckt,
die einen laufenden ffmpeg-Prozess braucht.

Acht Zusicherungen, die vorher nicht formulierbar waren:

* **Die 403-Kurve.** `2 ** (n - hits)`: beim *ersten* erzwungenen Wechsel muss
  die Basis stehen, nicht Basis × 2^hits. Mit den Standardwerten wäre der
  Unterschied Faktor 4 — vier Minuten statt einer.
* **Die Stream-Tod-Kurve** (300/600/1200/1800) **und dass beide Zweige den
  Worker-Tick mitverschieben.** Ohne das bremst die Sperre nur den Spawn,
  während der Live-Check weiter im 20-Sekunden-Takt läuft — die Last bleibt.
* **Was als „keine Daten" zählt.** Der gefährliche Fall ist die *große* Datei
  mit `stall_killed`: das ist ein echter, abgeschnittener Mitschnitt. Als tot
  gezählt, schickt er einen Streamer in den Backoff, der gerade sendet.
* **Der Früh-Trennungs-Zähler fällt nach Max-Retries weg**, statt oben stehen
  zu bleiben — sonst bekäme die nächste frühe Trennung sofort den längsten
  Backoff (F50-Bug B12).
* **Restzeiten runden auf.** `int(0.4)` wäre 0 gewesen: die Meldung hätte
  „frei" gesagt, während die Sperre den Spawn weiter verhindert.
* **Zwei Uhren, und der Bot benutzt an jeder Stelle die richtige.** Der
  403-Zweig rechnet in `time.time()`, der Stream-Tod-Zweig in
  `time.monotonic()` — weil er den Worker-Tick fällig stellt, und der ist
  monoton. Ein vertauschtes Paar setzt eine Sperre, die entweder sofort
  abgelaufen oder Jahrzehnte gültig ist; im Betrieb sieht beides aus wie „der
  Bot nimmt nicht auf" bzw. „der Bot hämmert". Der Vertrag liest die
  Aufrufstellen in `bot.py` und prüft die Uhr je Stelle.
* **Erfolg räumt alle sechs Register, das Sitzungsende nur fünf.** Die
  Asymmetrie ist Absicht: der Früh-Trennungs-Zähler hängt an der Netzqualität
  zur Verbindung, nicht an der Sitzung. Sie wird über die Signaturen und über
  die Aufrufstelle in `bot.py` festgehalten. Die Reset-Menge stand vorher
  dreimal verteilt im Monolithen — und zweimal fehlte einer der Zähler.

Acht Mutationen geprüft, alle acht schlagen an.

**Ein Vertrag hat sich selbst blind gemacht.** `test_v40_w55_record_fail_backoff`
prüfte die Backoff-Kurve, indem er sie **selbst nachbaute** — eine Kopie der
Formel, die mit dem Original nie verglichen wurde. Er wäre grün geblieben, auch
wenn die echte Rechnung falsch wird. Er ruft jetzt die echte Funktion; eine
Mutation an der Formel bringt ihn zu Fall.

### Geändert — die Recorder-Kommandozeilen stehen jetzt in `nc/reccmd.py` (v4.2 W17)

400 Zeilen, die entscheiden **womit** aufgenommen wird (nativer ffmpeg-Pull
oder yt-dlp) und mit welchen Argumenten. `bot.py` fällt auf **23.111 Zeilen**.
Wie bei W16 ist der Gewinn nicht die Zeilenzahl, sondern dass dieser Pfad
erstmals geprüft wird — und er ist der, an dem der Betrieb hängt: fällt er
aus, gibt es keine Aufnahme.

Neun Zusicherungen, die vorher nicht formulierbar waren:

* **F4, zwei Formen.** Der native Befehl trägt die TikTok-Session in einem
  `-headers`-Blob, yt-dlp als `--cookies <Datei>`. Zwei Formen, ein
  Redaktionspfad — und genau deshalb kann eine davon unbemerkt durchrutschen.
  Der Vertrag baut beide und prüft, dass `redact_cmd_for_log` beide leert.
* **Der 403-Umschalter.** Blockt TikTok die CDN-URL für unsere Egress-IP,
  wird der User zeitweise auf yt-dlp gezwungen. Drei Dinge werden festgehalten:
  der Zwang greift, ein **expliziter Force des Operators hat Vorrang** (sonst
  ließe sich der native Pfad nach der Behebung nicht mehr testen), und ein
  abgelaufener Cooldown wird **entfernt**, nicht nur ignoriert — sonst wächst
  das Dict mit jedem je geblockten User weiter.
* **B58.** Eine von der Detection mitgelieferte Stream-URL mit fast
  abgelaufenem `expire`-Token wird verworfen und frisch aufgelöst. Genau die
  „Sofort-404"-Aufnahmen waren das Fehlerbild. Umgekehrt wird eine frische URL
  **nicht** unnötig neu aufgelöst — der Vertrag zählt die Resolver-Aufrufe.
* **Proxy-Rotation.** Zuletzt geblockte Proxys werden ausgeschlossen, und der
  tatsächlich benutzte wird gemerkt — ohne das kann
  `handle_recording_finished` ihn hinterher weder belohnen noch rauswerfen.
* **F44:** reine FLV-Rooms werden aufgenommen (vorher galten sie als „kein
  Recorder verfügbar"). **F42:** `native_api` fällt auf yt-dlp zurück statt
  hart zu scheitern. Ohne brauchbaren Recorder kommt `(None, None)` zurück.
* **Die Aufnahme läuft `nice`-t und gedeckelt** — anders als das Relay, das
  nie genice't wird (W16). Der Gegensatz ist Absicht und steht jetzt fest.

Acht Mutationen geprüft, alle acht schlagen an.

**Ein Anker war still schwächer geworden — schon seit W16.** Die Prüfung „jede
rechnende ffmpeg-Befehlsliste läuft durch `_ff_cmd`" las **nur `bot.py`**. Seit
die beiden großen Kommandobauer nach `nc/` gewandert sind, lagen die größten
ffmpeg-Pfade des Projekts außerhalb der Suche, ohne dass irgendetwas rot wurde.
Gesucht wird jetzt in allen 173 Dateien, die ffmpeg aufrufen können; die
Mutation bestätigt, dass die Suche in `nc/` wirklich greift.

Dabei ist **eine echte Lücke** aufgefallen und bewusst nicht in dieser Welle
geschlossen worden: `nc/restream_testpush.build_cmd` baut einen synthetischen
Testbild-Push ohne `-threads`. Er ist im Bauer auf 30 Sekunden hart gedeckelt,
aber während eines laufenden Streams nimmt sich dieser x264 für die Dauer alle
Kerne. Die Ausnahme steht **benannt und begründet** im Vertrag, nicht in einer
still wachsenden Liste.

Der Rumpf ist bitgenau übernommen (gegen `git show HEAD:bot.py` verglichen,
alle fünf Funktionen). `configure()` lehnt unbekannte und fehlende Schlüssel
ab — ein stiller Default hieße hier: falscher Recorder, fehlende Cookies, kein
Thread-Deckel.

### Geändert — die ffmpeg-Zeile des Relays steht jetzt in `nc/restreamcmd.py` (v4.2 W16)

188 Zeilen, die nichts tun außer eine Argumentliste bauen: Input-Härtung,
Filtergraph, Encoder-Profil, tee-Ausgänge. `bot.py` fällt auf **23.494 Zeilen**.

**Der Gewinn ist nicht die Zeilenzahl, sondern dass dieser Teil erstmals
geprüft wird.** Im Monolithen hing er an zwanzig Bot-Globals, und in der
Entwicklungsumgebung gibt es kein ffmpeg — der Bauer war damit faktisch
ungetestet. Herausgelöst ist er importierbar und mit Attrappen aufrufbar.
Geprüft wird, **was aufgerufen wird**, nicht was ffmpeg daraus macht. Zehn
neue Zusicherungen, die vorher nicht formulierbar waren:

* **Der Cookie (F4).** Der gebaute Befehl trägt in `-headers` die komplette
  TikTok-Session. Der Vertrag baut ihn, schickt ihn durch
  `redact_cmd_for_log` und prüft, dass die Session verschwindet — **und** dass
  der `Referer` stehen bleibt. Eine Redaktion, die zu viel wegnimmt, macht das
  Log für die Fehlersuche wertlos; das fiel bisher niemandem auf.
* **B124.** `-reconnect_on_http_error` darf 403 und 404 nicht enthalten. Auf
  `4xx,5xx` hämmerte ffmpeg 30 Sekunden lang die tote Quell-URL, bis der ganze
  tee kollabierte („All tee outputs failed") — die Ursache der
  Restream-Abbrüche alle paar Minuten.
* **HLS bekommt `+genpts+igndts`, FLV nicht.** TikTok liefert HLS-Pakete ohne
  PTS und mit nicht-monotonem DTS; ohne das bricht der FLV-Muxer mit rc=187 ab.
* **Die Eingangs-Reihenfolge bestimmt die Filter-Indizes.** TTS ist Eingang 1,
  Avatar Eingang 2. Ein vertauschter Index legt nichts lahm, das man *sieht* —
  ffmpeg mischt dann einfach den falschen Stream.
* Thread-Deckel je Profil (Relay 2, Transcode 3) und **nie** `nice`;
  copy bleibt copy; `only_target` sendet ohne tee; `-http_proxy` nur mit Proxy;
  leere Zielliste fällt auf den Notausgang zurück statt ohne Ausgang zu senden.

Sechs Mutationen geprüft, alle sechs schlagen an.

**`configure()` lehnt ab, statt zu schlucken.** `nc/restream_targets` ignoriert
unbekannte Schlüssel bewusst; hier wäre das falsch. Ein Tippfehler liefe sonst
mit dem Default weiter — andere Bitrate, anderes Preset, kein Overlay — und
nichts würde rot. Sichtbar erst auf dem Sendebild. Fehlende Schlüssel ebenso.

Der Rumpf ist **bitgenau** übernommen (gegen `git show HEAD:bot.py` verglichen);
die Werte, die vorher Modul-Globale von `bot.py` waren, sind jetzt
Modul-Globale, die `configure()` belegt. Die beiden Ketten-Hüllen
`_drawtext_chain`/`_studio_chain` hatten nur diesen einen Nutzer und sind
mitgegangen.

**Anker nachgezogen, Verträge unverändert:** Overlay-Seitenverhältnis (B94),
Thread-Budget, die drei Duck-Mix-Stellen (v4.0-W11/W12) und die
Ketten-Delegation (v4.0-W27). Die verbietenden Zusicherungen lesen weiterhin
*beide* Dateien — ein nackter Stretch oder ein nachgebauter Filtergraph darf
nirgends zurückkommen.

### Geändert — der Discord-Teil ist aus dem Monolithen heraus (v4.2 W15)

`bot.py` fällt von **25.650 auf 23.661 Zeilen**. Der gesamte Discord-Teil —
Supervisor, Session, alle 45 Slash-Commands, Automod, Fehler-Kanal,
Community-Loops — steht jetzt in `discordbot.py`.

**Warum bot-seitig und nicht unter `nc/`:** die Datei importiert `discord.py`
und macht ein Gateway auf. `nc/*` ist bewusst bot-frei und bibliotheksartig;
ein Modul, das eine Verbindung hält, gehört dort nicht hin. Die Grenze, die
gilt, ist die andere Richtung: **kein einziges `from bot import`.** Alles
kommt durch genau einen Kanal, `starte(ctx)` mit einem `nc.botctx.BotKontext`.

**Der Entwurf lag falsch, und die Messung hat ihn umgeworfen.** Er zählte
13 Funktionen als „Discord-eigen" und wollte sie mitnehmen. Gezählt hatte er
*Aufrufe*. Es sind aber **Telegram-Handler, die Discord mitbenutzt**: `/sys_diag`
in Discord ruft denselben `diag`, den `/diag` in Telegram ruft — registriert
als Paar-Liste, referenziert statt aufgerufen. Nach Referenzen gemessen bleiben
**vier** Funktionen, die wirklich nur Discord gehören. Die geteilte
Befehlsschicht durfte nicht mitwandern; sie kommt als `befehle`-Tabelle herein.

**Der Kontext hat 21 Felder, nicht 57.** Aufrufbares und lebender Zustand sind
Felder — sie haben eine Signatur bzw. eine Identität, deren Änderung im Diff
auffallen muss. Konfiguration ist *ein* Wörterbuch mit fester Schlüsselmenge.
`.env` wird weiter an genau einer Stelle gelesen, in `bot.py`; zwei Dateien mit
eigenem `os.getenv("DISCORD_…")` wären zwei Orte, an denen ein Default
auseinanderläuft — und `tools/gen_env_example.py` müsste beide kennen.

**Der eine Fall, den bloßes Verschieben kaputtgemacht hätte:**
`_ensure_discord_invite` schrieb per `global` nach `DISCORD_INVITE_URL`. In der
neuen Datei hätte das nur die dortige Kopie gesetzt, während der Announcer in
`bot.py` weiter die leere URL verschickt hätte — still, ohne Fehlermeldung.
Der Invite geht deshalb durch einen Setzer im Kontext.

**Was hier nicht geprüft werden kann:** ob ein Slash-Command antwortet. Es gibt
in der Entwicklungsumgebung kein Discord-Gateway. Geprüft wird die Form — und
genau die trägt das Risiko: 1.900 Zeilen wechseln den Namensraum, in dem
51 Namen implizite Globals waren. Fällt einer durch, ist er still `None`. Die
beiden harten Zusicherungen schließen das: jeder Platzhalter wird von
`_uebernehmen()` belegt (und ist dort `global` erklärt — ohne das schriebe die
Zuweisung nur eine lokale Variable und der Vertrag liefe grün durch), und jeder
Schlüssel, den der Kontext verlangt, existiert in `bot.py`. Dazu ein echter
Import unter CI-Bedingungen, ohne `discord.py`.

Sechs Mutationen geprüft, alle sechs schlagen an. Verträge: 131 in
`test_nc_modules`, 379 in `test_restream`.

**Anker nachgezogen, Verträge unverändert:** die Ratsche aus W29
(blockierende `db_conn`-Blöcke, Grenze 52) zählt jetzt über **beide**
bot-seitigen Dateien — nur `bot.py` zu zählen hätte sie auf 28 fallen lassen,
ohne dass eine einzige Blockade beseitigt ist. Ebenso der Marken-Sweep aus
v4.0-W7, der Invite-Vertrag aus v4.0-W35, das Client-Register aus v4.1-W16,
der Sprach-Haken aus v4.1-W7 und die drei Flood-Historien aus v4.0-W14.
`tools/ncpatch.py` (Karte, `docs`, Befehlsliste) und `tools/i18n_extract.py`
kennen die zweite Datei jetzt — ohne den Extraktor-Eintrag hätte der nächste
Aufräumlauf 61 Slash-Command-Beschreibungen als verwaist gelöscht.

### Hinzugefügt — die MOTD spricht Englisch (v4.2 W14)

`tools/motd.sh` band `lib/i18n.sh` seit v4.1-W17 ein und rief `t()` **kein
einziges Mal** auf. Jede Zeile war ein `printf` mit deutschem Literal. Und
`tools/i18n_tools.py` sammelte nur aus den Senken von `installer.sh` — die es
in `motd.sh` gar nicht gibt. Ergebnis: **nichts** eingesammelt, und trotzdem
„100 % Abdeckung" gemeldet für eine Datei, die zu 0 % übersetzt war.

Eine Zahl, die nur zählt, was sie ohnehin kennt, verdeckt genau das, was sie
sichtbar machen soll. Das war schon die Lehre aus W28 (Dashboard) und W8
(`install.bat`) — hier zum dritten Mal, in derselben Datei, die die beiden
anderen prüft.

Der Katalog steht jetzt bei **373 Einträgen** statt 280, drei Werkzeuge,
0 fehlend, 0 verwaist. Die MOTD läuft vollständig auf Englisch.

**Neu ist ein ehrlicher Melder.** Die Quote sagt, wie viel von dem übersetzt
ist, was der Sammler *findet*. Der Melder sagt, was er **gar nicht erst
findet**: deutscher Ausgabetext, der an keiner Senke hängt. Hartes Tor bei
**null** — eine Ausnahmeliste „vier bekannte Fälle" verrottet, nach dem fünften
liest niemand mehr hin.

Der Melder hat sich dabei dreimal selbst korrigiert, und jedes Mal aus einem
echten Fehlschlag:

* Er zog die inneren Zeichenketten **aus** `$(t "…")` heraus und meldete
  ausgerechnet die als unumschlossen. Ein Melder mit Fehlalarm wird nicht
  gelesen — dann fällt der echte Befund mit durch.
* Er sah nur `printf`/`echo`-Zeilen. `lage_setz "…"` und Zuweisungen wie
  `EQ="  ${FNT}Kerne  ${R}"` fielen durch — und der englische Lauf zeigte
  prompt „Kerne". Jetzt gilt: **ein Literal mit Farbcode ist Anzeige**, egal
  wohin es geht.
* Seine Wortliste kannte „Kerne", „Netz", „Werkzeuge" nicht. Ein Marker-Satz,
  den man nicht nachzieht, wird blind.

Nach jeder Korrektur fand er weitere Stellen — insgesamt acht, die vorher
unsichtbar waren, plus zwei echte Lücken in `installer.sh` (deutscher Text in
einem `printf` **innerhalb** einer Ersetzung: der äußere Text läuft durch
`t()`, trägt aber einen Laufzeitwert und trifft nie einen Schlüssel).

**Der deutsche Text ändert sich an fünf Stellen leicht** — dort, wo ein Wert
mitten im Satz stand und der feste Teil zum Schlüssel werden musste: „Platte zu
92 % voll" wird „Platte fast voll (92 %)", „BOT_DIR in /etc/… setzen" wird
„BOT_DIR in der Konfiguration setzen (/etc/…)". Dieselbe Aussage, andere
Satzstellung.

Der Vertrag lässt die MOTD **zweimal laufen** und vergleicht — ohne diesen Lauf
wäre alles andere nur die Behauptung, die Verdrahtung stimme, und genau die
stimmte seit v4.1-W17 nicht. Dazu: ohne Katalog bleibt alles deutsch (nie ein
nackter Schlüssel, nie eine leere Zeile), und die drei Senken werden
ausnahmsweise am Wortlaut geprüft — `gauge` trägt CPU, RAM, Swap und Disk, die
in beiden Sprachen gleich lauten, und ein Verhaltenstest kann den Ausfall dort
nicht sehen.

### Geändert — was nur rechnet, rechnet jetzt außerhalb (v4.2 W13)

Angefragt war „alles in einer großen Welle": die vier verbliebenen Brocken
`_discord_run_once` (1730), `RestreamManager` (1418), `handle_recording_finished`
(669) und der Rest von `KickModerator` (585).

**Das geht so nicht, und das ist ein Befund, keine Ausrede.** Diese Blöcke lesen
56 bis 88 Bot-Namen. Ein `nc/`-Modul mit 88 eingespritzten Abhängigkeiten wäre
kein Modul, sondern derselbe Monolith in zwei Dateien — mit einer Schnittstelle
obendrauf, die niemand überblickt. Die Messung „wenige Außenbezüge" trügt dabei
zusätzlich: `_award_xp` hat sechs, bekommt aber ein Discord-`message`;
`_clip_week_leader` liest `client.guilds`; die beiden Aufnahme-Wächter sind
Closures über einen laufenden Prozess. Wenige Namen heißt nicht wenig Bindung.

Herausgelöst wurde deshalb aus **allen vier** Blöcken das, was wirklich nur
rechnet — 52 Zeilen weniger im Monolithen, aber zwei Module, die man ohne
laufenden Stream und ohne Sprachmodell nachprüfen kann.

**`nc/restreamgesundheit.py`** — Fortschrittsmarke, Blind-Markierung, Verfall
der tee-Ziel-Fehler. Diese drei beantworten dieselbe Frage: misst eine Anzeige
noch etwas, oder zeigt sie nur noch etwas? Das ist die gefährlichere Hälfte
jedes Befunds — ein leeres Feld fällt auf, eine eingefrorene Bitrate nicht. In
der Vorgeschichte stecken drei Fehler genau dieser Form (W113, W116, v4.1-W10),
und alle drei waren Rechenfehler, keine ffmpeg-Fehler. Der Vertrag rechnet sie
jetzt nach, statt ihre Quelltextzeilen wiederzuerkennen.

**`nc/modki.py`** — die zwei KI-Fragen der Chat-Moderation: Aufforderung und
Auswertung. Der Aufruf bleibt im Bot, weil `ai_chat` am Router, am Budget und
an der Basen-Rotation hängt. Die Auswertung ist der Teil, der schiefgeht: ein
Modell antwortet mal mit ```json, mal nackt, mal mit einem Satz davor. **Und
`None` ist nicht `unauffällig`** — sonst gilt ein ausgefallenes Modell als
Freispruch. Beim Lernen gilt das Gegenteil: ein unlesbares Ergebnis darf keine
Sperrliste erweitern, im Zweifel wird nicht gelernt.

**Der Vertrag hat dabei einen Fehler gefunden, den ich selbst eingebaut habe.**
`blind_markieren` prüfte `if not info` — ein **leeres** Wörterbuch gilt damit
als „kein Eintrag". Im Monolithen fiel das nie auf, weil `_eintrag()` dort
immer ein gefülltes liefert; als allgemeine Funktion wäre es ein stiller
Ausfall genau in dem Fall, für den die Markierung gedacht ist. Jetzt
`is None`.

Ein Anker in `test_restream.py` ist gewandert — und dabei **besser geworden**:
er prüfte, dass die Zeile `w = eintrag.setdefault("watch"` im Monolithen steht.
Jetzt prüft er, dass Stillstand nicht als Fortschritt zählt. Das war die ganze
Zeit die eigentliche Zusage.

### Geändert — die Kick-REST-Aufrufe raus (v4.2 W12)

`nc/kickapi.py` gab es schon — mit `slug()`, `broadcaster_id()` und dem
gemeinsamen `SEND_LAST`. Die fünf Aufrufe, die es eigentlich beherbergen
sollte, standen weiter in `KickModerator`: Chat senden, Timeout setzen,
Kanalzustand lesen, Titel/Kategorie ändern, Kategorie suchen. Dazu die
Tokenbeschaffung. **196 Zeilen raus**, 25.898 → 25.702.

In `bot.py` bleiben Durchreicher — und der **Bot-Zustand**: der
Moderations-Logeintrag und `last_spoken` gehören nicht nach `nc/`. Der
Vertrag prüft beides, und zwar am geparsten Quelltext ohne Kommentare: der
Modulkopf von `nc/kickapi.py` *nennt* `_modlog`, um zu erklären, dass es dort
nicht hingehört — ein Textvergleich über die rohe Datei schlägt auf genau
dieser Erklärung an. Derselbe Fehler wie in W32, W33 und v4.2-W3, diesmal
gleich beim ersten Lauf gefangen.

**Die Zwei-Token-Regel steht jetzt an einer Stelle statt an dreien.** Kick
kennt einen App-Token (`client_credentials`) und einen User-Token. Der
App-Token darf lesen, aber weder chatten noch moderieren noch den Kanal
ändern — dort antwortet Kick mit einem nackten 401, das nach einem kaputten
Schlüssel aussieht und in Wahrheit „falsche Token-Art" heißt. Das war v4.0-W17
und hat Wochen gekostet. `_schreib_token()` bedient jetzt Chat, Timeout und
Kanaländerung gemeinsam; die Mutationsprobe stellt den alten Fehler wieder her
und der Vertrag fängt ihn.

Auch der App-Token-Cache ist gewandert: er lag am `KickModerator`-Objekt, hängt
aber an genau einem Kick-Zugang. Bei jedem Neustart der Chat-Schleife holte das
einen frischen Token.

**Vier Anker in `test_restream.py` sind gewandert, keiner gelöscht.** Die
Verträge B169, v4.0-W9, v4.0-W10 und v4.0-W17 verankern sich an wörtlichem
`bot.py`-Quelltext; der Code hat sich nicht geändert, nur sein Ort. Jeder Anker
trägt jetzt die Notiz, was gewandert ist und warum die Zusage dieselbe blieb —
und wo es enger geht als vorher: der Sendepfad muss auf **jedem** Fehlerweg
eine Spur in `SEND_LAST` hinterlassen, nicht nur an der Stelle, die der alte
Anker traf.

**Die CI hat einen Fehler gefunden, den der lokale Lauf nicht finden konnte.**
Der Vertrags-Job zieht nur `orjson` und `flask` — eine Regel seit W23. Der neue
Vertrag ruft `send_message()` wirklich auf, und dort steht ein `import aiohttp`.
Lokal ist `aiohttp` vorhanden (es steckt in `requirements-smoke.txt`), also lief
er grün; in der CI starb er mit `ModuleNotFoundError`. `aiohttp` wird jetzt
gestubbt statt installiert, wie `test_smoke.py` es mit TikTokLive und
python-telegram-bot tut — der Vertrag prüft NC-Code, nicht aiohttp. Nachgestellt
wird die CI-Lage seitdem lokal über einen Importblocker.

Aus dem Behelf ist eine **zusätzliche Zusage** geworden: der Stub zählt mit,
mit welchem Zeitdeckel gerufen wird. Jede Kick-Anfrage muss einen tragen — ein
stiller Kick-Endpunkt ohne Deckel hängt den Event-Loop auf, und mit ihm jede
Aufnahme, den Restream und das Dashboard.

Die erste Fassung dieser Zusage war wertlos: sie prüfte „es gab Zeitdeckel, und
alle waren 15 Sekunden". Beim Mutationstest blieb ein Aufruf **ohne** Deckel
unentdeckt, weil die anderen vier weiterhin einen setzten. Gezählt wird jetzt
Deckel gegen Anfrage. Eine Zusage, die man mit vier richtigen Aufrufen
erschleichen kann, ist keine.

### Geändert — das ffmpeg-Handwerk der Upload-Zerlegung raus (v4.2 W11)

Parallel zur Cookie-Welle oben, und unabhängig davon. Nach fünf Wellen Routenabbau sind die Routen nicht mehr das Problem: die 34
verbliebenen in `bot.py` sind zusammen **554 Zeilen**, zwei Prozent der Datei.
Die Masse liegt in wenigen sehr großen Funktionen — sechs Definitionen tragen
5.698 Zeilen.

Gewählt wurde nicht die größte, sondern die **lösbarste**: `split_and_send_video`
(614 Zeilen) hängt an nur **23** Bot-Namen. Zum Vergleich: `RestreamManager` 69,
`KickModerator` 67, `_discord_run_once` 88. Und es gab eine saubere Naht — der
ffmpeg-Teil kennt Telegram nicht, und der Telegram-Teil kennt ffmpeg nicht.

`nc/videoteil.py` (neu) übernimmt: messen, teilen, notfalls neu kodieren,
kaputte Container reparieren, Zeitstempel geradeziehen. `bot.py` behält
`_send_one` und die gesamte Ablaufsteuerung samt aller Meldungen an den Nutzer.
**226 Zeilen raus**, 25.949 → 25.723.

**Eine verschattete Zweitkopie ist dabei aufgeflogen.** `bot.py` importiert
`nc.ffdiag.ffprobe_duration` als `_ffprobe_duration` — und
`split_and_send_video` definierte eine verschachtelte Funktion **desselben
Namens**, die den Import verschattete. Die beiden sind nicht austauschbar: die
im Modul ist **synchron** (`subprocess.run`), die verschachtelte **asynchron**
mit Zombie-Schutz. Sie zusammenzulegen sieht nach Aufräumen aus und ist ein
Ausfall — ein `subprocess.run` mit 15 s Timeout auf dem Event-Loop friert jede
andere Aufnahme, den Restream und das Dashboard für 15 Sekunden ein. Beide
bleiben, jetzt mit verschiedenen Namen und einem Vertrag, der ihre Rollen
festhält.

Der Vertrag prüft die Zerlegung über ihr **Verhalten**, ohne ffmpeg: der
Subprozess wird abgefangen und die **Kommandozeile** geprüft. 300 MB über 600 s
müssen `segment_time=81` ergeben; ohne ffprobe-Dauer greift der konservative
Rückfall auf 180. Das ist genau die Rechnung, deren Vorfassung
`CHUNK_SIZE_MB*60` benutzte — 45 Minuten je Segment, 300–700 MB je Teil, also
immer ein 413. Die Mutationsprobe reproduziert sie: `segment_time=2700`.

Dazu: ein hängendes ffprobe wird getötet **und** abgewartet (ohne `wait()`
bleibt ein Zombie, und nach ein paar hundert Aufnahmen ist die Prozesstabelle
voll), eine gescheiterte Platzprobe blockiert **keinen** Upload, der
funktioniert hätte, und der Repair springt nur bei einem wirklich kaputten
Container an — wer dort zu breit erkennt, startet nach jedem beliebigen
ffmpeg-Fehler einen Reparaturlauf über die volle Dateigröße.

### Behoben — der Cookie-Parse-Fehler, und Cookies holt sich der Bot jetzt selbst (v4.2 W10)

Gemeldet als „Cookie parse error". Die Reparatur, die es dafür seit B63 gab,
hat den Text nur **durchgereicht**. Genau die drei Dinge, an denen
`MozillaCookieJar` tatsächlich stirbt, hat sie nie angefasst:

* **Feld 2 passt nicht zur Domain.** Der Parser prüft
  `assert domain_specified == initial_dot`. Ein `.tiktok.com` mit `FALSE`
  (oder `www.tiktok.com` mit `TRUE`) ist ein harter Abbruch — nicht der
  Zeile, sondern der **ganzen Datei**.
* **Nicht genau sieben Felder.** Ein Tab zu viel im Wert: `ValueError`.
  Ein Editor, der das leere letzte Feld wegtrimmt: derselbe Fehler von der
  anderen Seite — und der Cookie verschwand vorher still.
* **Eine Ablaufzeit, die keine Zahl ist.** `Session` statt `0` reicht.

Dazu ein Kopf, der nicht in **Zeile 1** steht (eine Leerzeile davor genügt,
denn der Parser liest genau eine Zeile weit), und ein BOM aus einem
Windows-Editor. Acht Fehlerbilder, jedes einzeln reproduziert, jedes jetzt
repariert — festgehalten in `test_nc_modules.py`.

Die Folgen waren überall dieselbe stille Fehlanzeige: das Deck meldete
`parse_error`, yt-dlp brach mit `rc=1` ab („early_disconnect" nach zwei
Sekunden), und `_load_cookies_dict()` lieferte ein **leeres dict** — der
Recorder fuhr ohne Cookies los und bekam von TikTok 403. Drei verschiedene
Symptome, eine Ursache.

Drei weitere Löcher im selben Pfad sind mit zu:

* **`lade_jar()` liest jetzt auch eine krumme Datei** (normalisiert, ohne sie
  anzufassen). Vorher war ein Formatfehler gleichbedeutend mit „keine Cookies".
* **Die Reparatur prüft, bevor sie tauscht.** Sie schrieb bisher erst und
  sah nie nach, ob das Ergebnis ladbar ist. Blieb es kaputt, lief die nächste
  Aufnahme wieder ins Leere.
* **`LoadError` erbt von `OSError`** — ein `except OSError` an der falschen
  Stelle hätte den ganzen neuen Weg wieder ausgehebelt. Steht als Vertrag drin.

**Und der Bot holt sich Cookies jetzt selbst** (`nc/cookieholen.py`, neu).
Der Gast-Abruf holt die rotierenden Anti-Bot-Tokens (`ttwid`, `msToken`,
`tt_chain_token`, …) mit einem HTTPS-Aufruf bei TikTok — ohne Login, ohne
Extension, über denselben Proxy wie Resolve und Pull. Das ist der Teil, der
zuerst abläuft. Der Cookie-Alarm versucht das **bevor** er jemanden weckt:
lässt sich der Zustand selbst reparieren, kommt keine Meldung mehr. Höchstens
alle `COOKIE_AUTO_FETCH_INTERVAL_H` Stunden (Vorgabe 6).

Auth-Cookies fasst der Gast-Weg **grundsätzlich nicht an**. Ein Gast-`odin_tt`
neben einem echten Login ist genau die Mischung, die 403 erzeugt — ein stiller
Logout wäre die schlechtere Version des Fehlers, den wir gerade beheben. Einen
`sessionid` kann nur ein Browser liefern: dafür gibt es den Browser-Import
(`browser_cookie3`, sonst `yt-dlp --cookies-from-browser`), der **nach Domain
filtert** — ein Browser-Profil trägt die Cookies aller Seiten, und
`tiktok_cookies.txt` liegt in jedem Backup.

Erreichbar über `POST /api/cookies/fetch`, zwei Knöpfe im Cookie-Panel des
Decks und `/cookies holen [browser]` in Telegram.

### Behoben — der gespeicherte OAuth-Zustand hat gelogen (v4.2 W9)

Gemeldet als „YouTube-OAuth speichert Daten nicht, ständige Neuverbindung
nötig". Es waren vier Fehler, und die beiden Hälften des Paares waren
spiegelbildlich falsch.

**YouTube: der tote Token überlebte den Neustart.** Lehnte Google den
Refresh-Token ab (`invalid_grant`), leerte `access_token()` ihn **nur im
Speicher**. Auf der Platte blieb er liegen. Beim nächsten Start las `_load()`
ihn zurück, `status()` meldete `ready`, das Panel zeigte „verbunden" — und kein
einziger Aufruf ging durch. Genau das Bild „muss ständig neu verbinden": der
gespeicherte Zustand log über die Wirklichkeit. Jetzt räumt `forget()` beides
ab; Platte und Speicher sagen dasselbe.

**Twitch: eine Störung kostete die Verbindung.** Umgekehrter Fehler. Der
Refresh-Token flog bei **jedem** ausbleibenden Access-Token raus — also auch
bei einem 500er, einem Wartungsfenster oder einer Antwort, die sich nicht als
JSON lesen ließ. Ein Schluckauf auf Twitchs Seite kostete die gespeicherte
Verbindung, und der Betreiber autorisierte neu, obwohl an seinem Token nie
etwas falsch war. Gelöscht wird jetzt nur noch bei einer ausdrücklichen
Ablehnung (400/401 mit `invalid`/`expired`).

**Ein Kanalname konnte die Verbindung löschen.** `set_channel()` rief `_save()`,
und `_save()` schrieb, was gerade im Speicher stand. War der Refresh-Token dort
schon geleert, überschrieb ein **Kanalname** den Store mit einem leeren Token.
Neue Regel, in beiden Modulen: `_save()` schreibt nur eine **Verbindung**, nie
ihre Abwesenheit. Gelöscht wird ausschließlich über `forget()` — das entfernt
die Datei. `nc/twitchoauth.py` hatte gar kein `forget()` und bekommt eins, sonst
hätte es den YouTube-Fehler geerbt.

**Der Store-Pfad war relativ.** `bot.py` reicht `recordings/…` herein, also
relativ zum Arbeitsverzeichnis. Ein Start aus einem anderen Verzeichnis
(Handstart, cron) hätte den Store woanders gesucht und den Token
stillschweigend verloren. `configure()` löst ihn jetzt einmal beim Start auf.

**Und es war unsichtbar.** Ein nicht schreibbarer Store meldete `log.warning` —
ein ERROR-Log zeigt `warning` nie (CLAUDE.md). Genau so blieb „der Token wird
gar nicht gespeichert" verborgen: der Flow meldete Erfolg, und nach dem
nächsten Neustart war die Verbindung weg. Beide Module melden das jetzt auf
`error`, mit dem Pfad.

Das Panel sagt außerdem, **warum** es nicht geht: „abgelaufen" und „nie
verbunden" sahen bisher gleich aus — beides nur ein graues Feld. `status()`
trägt jetzt `expired`, `last_error` und `last_error_ts`, und das Dashboard nennt
den Grund samt Hinweis auf den häufigsten Fall: eine Google-App im Status
„Testing" lässt Refresh-Tokens nach 7 Tagen ablaufen. **Das** ist die Ursache
einer wöchentlichen Neuverbindung, und sie steht in der Google Cloud Console,
nicht im Code.

### Hinzugefügt — der Windows-Installer spricht Englisch (v4.2 W8)

`tools/install.bat` hatte **gar keine Sprachschicht**: 610 Zeilen, jede Ausgabe
ein deutsches `echo`. Und `tools/i18n_tools.py` kannte die Datei nicht einmal —
sie stand nicht in seiner Quellenliste. Der Prüfer meldete deshalb **100 %
Abdeckung** für ein Werkzeug, das er nie angesehen hat. Genau die unehrliche
Zahl, die W28 fürs Dashboard beseitigt hat, nur eine Etage tiefer.

Der Installer benutzt jetzt denselben Katalog wie `installer.sh` und `motd.sh`
— **eine** Datei `locales/tools.en.tsv` für beide Installer. 18 der 157
Schlüssel standen bereits darin und werden mitbenutzt; genau dafür ist es eine
gemeinsame Datei. 139 kamen dazu, der Katalog steht bei 280 Einträgen,
0 fehlend, 0 verwaist.

Übersetzt wird **an der Senke**, wie überall sonst im Projekt: `:kopf`, `:info`,
`:gut`, `:warn`, `:fehler`, `:erklaere`, `:merken` und die drei Frage-Routinen
laufen durch ein neues `:t`. Für Meldungen mit einem Wert darin gibt es
`*_wert`-Varianten — „Quelltext liegt in C:\..." kann kein Katalogschlüssel
sein, der Pfad steht erst zur Laufzeit fest. Für die freien Ausgabezeilen
(Begrüßung, Schrittliste, „Was unter Windows anders ist") gibt es `:zeile`,
`:zeile2` und `:punkt`.

**Der deutsche Pfad ist nachweisbar unverändert.** Dieser Installer lässt sich
auf einem Linux-Rechner nicht ausführen — es gibt kein `cmd.exe`. Was man nicht
ausprobieren kann, muss so gebaut sein, dass sein Fehlschlag folgenlos bleibt:
`NC_KATALOG` wird nur gesetzt, wenn ausdrücklich Englisch gewünscht **und** die
Datei da ist; sonst kehrt `:t` nach zwei Zeilen zurück. Der Rückfallwert steht
in Zeile eins, **bevor** irgendetwas nachgeschlagen wird. Findet `findstr`
nichts, läuft der Schleifenrumpf nie; schlägt `findstr` selbst fehl, schluckt
`2>nul` die Meldung — mit demselben Ergebnis. Es gibt in `:t` keinen Weg, der
etwas anderes tut als übersetzen oder nichts.

Der Vertrag ersetzt den Lauf, den es hier nicht gibt: `findstr /b /l /c:` wird
nachgebildet und **jeder** der 280 Schlüssel dagegen geprüft — ein Schlüssel,
den `findstr` nicht fände, wäre eine Zeile, die für immer deutsch bleibt. Dazu:
die Datei bleibt reines ASCII (cmd.exe rendert sonst je nach Codepage
Buchstabensalat), der Tabulator in `delims=` und im Suchmuster ist ein echter
Tabulator, kein Schlüssel trägt einen Laufzeitwert, und keine Ausgabezeile läuft
an einer Senke vorbei.

Der letzte Punkt hat sich beim Mutationstest selbst korrigiert: die erste
Fassung des Prüfers sah nur Zeilen, die mit `echo` **beginnen**, und ließ
`if exist ... echo Merkzettel` durch — genau die Form, die diese Datei benutzt.
Der Fehlschlag steht als Begründung im Test.

### Hinzugefügt — vier neue Anzeigen in der MOTD (v4.2 W7)

`tools/motd.sh` steht jetzt auf **v2.1**. Vier Anzeigen, jede aus einer Frage,
die die alte Fassung nicht beantwortet hat:

**Gesamtampel im Kopf.** Die MOTD hat acht Blöcke; wer per Handy-SSH einloggt,
sieht davon drei, ohne zu scrollen. Der schlimmste Befund steht deshalb jetzt
in Zeile zwei — `● alles im Griff`, `▲ Dashboard antwortet nicht sauber` oder
`✘ Bot läuft nicht`. Rot schlägt Gelb, und innerhalb einer Stufe gewinnt der
**erste** Befund: „Bot läuft nicht" ist die Ursache, „Dashboard nicht
erreichbar" meist nur die Folge — stünde dort die Folge, suchte der Betreiber
am falschen Ende.

Dafür laufen die Proben für Dienst und Dashboard **vor** dem Kopf statt mitten
in der Ausgabe. Es sind dieselben zwei Aufrufe mit denselben Zeitdeckeln, nur
früher; die Anzeige kostet keine Millisekunde mehr.

**Netzdurchsatz.** „Bot läuft" und „es geht wirklich etwas raus" sind zwei
verschiedene Fragen — für eine Restream-Box ist die zweite die wichtigere, und
sie blieb bisher offen. Gemessen wird im **selben** Fenster wie die CPU: ein
Durchsatz braucht zwei Proben mit Abstand, und ein eigener `sleep` wäre der
teuerste Posten der ganzen MOTD geworden.

**Fehlerverlauf über sieben Tage.** Eine nackte 4 sagt nichts. Vier Fehler
hinter sechs stillen Tagen sind ein Ausbruch, vier hinter sechs Tagen mit je
dreißig sind eine Verbesserung. Ein `awk`-Durchgang über das Ende der Datei
statt sieben `grep`-Läufen.

**Verlaufsbalken in Truecolor.** Jede Zelle trägt die Farbe ihrer Position, der
Balken liest sich als Thermometer: 85 % sind sichtbar heiß, bevor die
90er-Schwelle reißt. In 256 und 16 Farben gäbe das Bandenbildung statt Verlauf
— dort bleibt es bei der einen Farbe. Der Balken **verschwindet nie**: eine
Statusanzeige ist kein Plakat, „schön oder gar nicht" wäre hier der falsche
Handel.

Der Vertrag prüft das **Verhalten**, nicht den Wortlaut: die MOTD wird mit
vorgetäuschtem `systemctl` und `curl` in den grünen und den roten Zustand
gefahren, der Miniverlauf gegen bekannte Zahlen gerechnet und der Balken in
allen vier Farbmodi nachgewiesen. Dazu die Grundregel, die diese Datei trägt:
kein `set -e`, und jedes neue Kommando, das hängen kann, hinter `tmo()` — ein
blockierter Login auf einem Server ohne Konsole ist ein Ausfall, der sich nicht
mehr aus der Ferne beheben lässt.

### Hinzugefügt — Sätze, die ein Inline-Tag zerschneidet (v4.2 W6)

Der Übersetzer im Browser vergleicht ganze Textknoten. Ein Satz wie

    Gebucht wird der <b>Zufluss</b> — der Tag der Gutschrift auf dem Konto …

ist im DOM aber drei Knoten, und **keiner davon ist ein Satz**: „Gebucht wird
der" endet auf einem Artikel, „— der Tag …" beginnt mit einem Gedankenstrich.
Beide flogen zu Recht als Bruchstück aus dem Katalog — und damit blieb der
ganze Absatz deutsch, ohne dass die Abdeckungszahl es zeigte. Das war die
letzte bekannte Lücke der Mehrsprachigkeit aus v4.1-W6.

Neu ist ein **Platzhalter-Schlüssel**: jedes Inline-Kind wird zu `{0}`, `{1}`, …
Der Schlüssel trägt den vollständigen Satz und trotzdem kein Markup. Der
Browser setzt beim Übersetzen die **vorhandenen** Kind-Elemente wieder ein, er
baut keine neuen — es gibt in diesem Weg keine Stelle, an der HTML geparst
wird, also auch keine, an der eine Übersetzung ein Tag einschleusen könnte.

Dass die Kinder in der Reihenfolge der **Zielsprache** eingesetzt werden, ist
kein Beiwerk: Englisch stellt um, und ein Verfahren, das die Elemente an ihrem
deutschen Platz ließe, wäre für die Hälfte der Sätze unbrauchbar.

Angefasst wird nur, wo es klemmt: trägt jedes Textstück des Elements für sich
schon als Knoten, bleibt es beim normalen Weg. Sonst hätte ein längerer
Schlüssel 39 funktionierende Übersetzungen entwertet. Ergebnis: **15 neue
Sätze** (2 im Dashboard, 8 auf der Website, 5 in Impressum/Datenschutz),
7 tote Bruchstück-Einträge ersetzt, Katalog **1390 Einträge, 0 fehlend,
0 verwaist**.

Der Extraktor liest dafür zum ersten Mal die **Struktur** statt nur die
Zeichen (`html.parser` statt Regex) — die Frage „welche Kinder hat dieses
Element?" ist genau die, an der ein Regex über HTML scheitert.

Der Vertrag koppelt beide Seiten über ihr **Verhalten**, nicht über ihren
Wortlaut: Inline-Tag-Liste und Platzhalter-Obergrenze werden aus dem
ausgelieferten JavaScript geparst und mit den Python-Konstanten verglichen.
Wer in einer Sprache ein Tag ergänzt und in der anderen nicht, baut sonst eine
Lücke, die kein Textvergleich sieht — der Extraktor sammelte einen Schlüssel
ein, den der Browser nie erzeugt. Dazu ein Katalog-Prüfer: fehlt in einer
Übersetzung ein `{n}`, verschwände das Kind-Element beim Umbau. Ein fehlender
Link ist schlimmer als ein deutscher Satz, deshalb lässt der Browser so einen
Eintrag liegen — und der Vertrag meldet ihn, statt ihn still wirken zu lassen.

### Geändert — der Selbsttest raus, Vorschlag 2 ist fertig (v4.2 W5)

`/api/selftest` (226 Zeilen) liegt jetzt in `nc/routes/selbsttest.py`. Damit
steht **keine der acht System-Routen** mehr im Monolithen — der Rest von
Vorschlag 2 ist abgearbeitet. Der Kontext bleibt bei **24 von 25 Slots**;
fünf Wellen Routenabbau, null neue Einträge.

Der Selbsttest kam zuletzt, weil er als einziger quer durch alle Domänen
liest — Dauerläufer, Restream-Ziele, Moderation, Abwehr. Erst musste der
Zustand, den er abfragt, überall sonst aufgelöst sein.

**Er kostet keinen neuen Eintrag**, weil alles schon da war:

- Der Restream-Manager kommt aus dem Register `nc/restreamstate.py` (W18).
- Sperrliste und Angriffe kommen über die **Haken**, die
  `nc/routes/abwehr.py` seit W25 ohnehin hält — dieselben zwei Funktionen,
  die das Abwehr-Panel benutzt. Ein zweiter Weg zu denselben Daten wäre eine
  zweite Wahrheit, und die beiden Panels könnten Widersprüchliches melden.
- `_st_befund` ist mitgewandert: 23 Aufrufe, alle in dieser einen Funktion.

**„Gar nicht nachgesehen" bleibt von „nichts gefunden" getrennt.** Fehlt ein
Haken (Bot läuft nicht), liefert `_haken()` ein leeres Dict — nicht
`{"total_banned": 0}`. Bei einer Sicherheitsanzeige ist „alles ruhig" die
gefährlichste aller Antworten, wenn niemand nachgesehen hat. Dieselbe
Überlegung wie in `abwehr._nicht_bereit()`.

**Wache am Manager.** Vor dem Start ist er `None`; ein nacktes `_mgr()._procs`
hätte die **ganze** Antwort gekippt — also auch die zwanzig Befunde, die mit
Restream nichts zu tun haben. Alle Zugriffe laufen über `getattr` mit Vorgabe,
ein Vertrag prüft jede Stelle.

Nachgemessen an einer bewusst falsch gesetzten `TWITCH_INGEST_URL`: der Befund
kommt als `rot` mit der richtigen Adresse im Fix-Hinweis. Der YouTube-Schlüssel
erscheint weder in der Antwort noch im Kontext — geprüft wird nur, **ob** einer
gesetzt ist.

Fünf Negativtests, alle feuern. Zwei davon musste ich nachschärfen: die
Haken-Prüfung lief zuerst über Text und konnte das `return {}` im
`except`-Zweig nicht vom richtigen unterscheiden — jetzt läuft sie über das
Verhalten. Und der Teilcheck mit dem werfenden Haken braucht einen gefüllten
Kontext (er loggt); ohne Absicherung wäre er ein Fehlalarm über etwas, das im
Betrieb nie vorkommt.

`bot.py` 26.160 → **25.949 Zeilen**, eigene Routen 35 → **34**,
`nc/routes/` 35 → **36 Blueprints**.


### Geändert — Preflight und Resilienz raus, Sondenschicht vollständig (v4.2 W4)

Dritte Teillieferung von Vorschlag 2. `/api/system/preflight` (123 Zeilen) und
`/api/system/resilience` (50 Zeilen) liegen jetzt in
`nc/routes/systemlage.py` — **ohne einen einzigen neuen `nc.ctx`-Slot**,
weiterhin 24 von 25. Von den ursprünglich acht System-Routen bleibt nur noch
`selftest`.

Drei Sonden sind nach `nc/systemprobe.py` gewandert, dem Modul aus W32:

- **`cpu_load_snapshot`** — Load, Speicher/Swap und die größten CPU-Fresser
  direkt aus `/proc`. Das *Parsen* lag seit v4.0-W30 ohnehin in
  `nc/sysload.py`; im Bot stand nur noch das Einsammeln.
- **`disk_pct`** — reine stdlib, hing nur an `RECORDINGS_DIR`.
- **`ai_alive`** — beide Wege (`brain`, `nc.freeai`) liegen außerhalb des
  Bots; er war reine Durchreiche.

Vier weitere Helfer brauchten gar nichts: `_multistream_targets`,
`_tunnel_effective`, `_faster_whisper_available` und `_piper_available` waren
längst Aliase auf `nc/`-Funktionen.

**Wieder eine stille Fehlanzeige verhindert.** Die Preflight-Karte maß den
Plattenplatz mit

```python
_sh.disk_usage(RECORDINGS_DIR if "RECORDINGS_DIR" in globals() else "/")
```

Im Blueprint ist `globals()` der Namensraum **dieser** Datei — der Test wäre
dauerhaft `False` gewesen und gemessen worden wäre die **Systemplatte** statt
des Aufnahme-Verzeichnisses. Eine Zahl, die richtig aussieht und falsch ist.
Dritter Fund dieser Art nach W32 (`__file__`) und W33 (`/api/version`).

**Keine zweite Wahrheit.** `recordings_dir`, `ffmpeg_threads_bg` und
`ffmpeg_nice_bg` liegen seit W110/W116 als **Slot** im Kontext. Sie zusätzlich
nach `cfg` zu legen wären zwei Werte für dieselbe Sache; der Blueprint liest
jetzt den Slot. Ein Vertrag hält das fest.

**Geheimnisse bleiben draußen.** Alle sechs im Spiel (`DASHBOARD_TOKEN`,
`DISCORD_BOT_TOKEN`, `KICK_CLIENT_SECRET`, `KICK_STREAM_KEY_BACKUP`,
`TWITCH_STREAM_KEY`, `YOUTUBE_STREAM_KEY`) werden ausschließlich als Boolean
geprüft — es gehen `HAT_…`-Werte in den Kontext. Nachgemessen mit sechs
unterscheidbaren Testgeheimnissen: keines erscheint in der Antwort, keines im
Kontext.

**Ein Fehler, den erst der Aufruf zeigte:** `c["FFMPEG_THREADS_BG"]` gab es in
`cfg` nicht — der Wert liegt als Slot vor. Statisch unsichtbar, im Betrieb ein
`KeyError` beim ersten Klick. Der Vertrag vergleicht jetzt **jeden** gelesenen
`cfg`-Schlüssel gegen das, was der Bot wirklich liefert.

Sechs Negativtests, alle feuern. Der Test für „misst das konfigurierte
Verzeichnis" ist dabei zweimal geschrieben worden: die erste Fassung verglich
Prozentzahlen und feuerte nicht, weil Temp- und Arbeitsverzeichnis auf
derselben Platte liegen. Jetzt wird der Aufruf abgefangen und der übergebene
Pfad geprüft.

**Drei Anker gewandert, keiner gelöscht:** die Whisper-Drossel-Diagnose (B98),
der sysload-Delegationsnachweis (W30) und das Gesamturteil der
Übersichtskachel (W68) zeigten alle auf `bot.py`.

`bot.py` 26.346 → **26.160 Zeilen**, eigene Routen 37 → **35**.


### Geändert — CodeQL bekommt eine Barriere statt 208 unlesbarer Meldungen (v4.2 W3, Teil 2)

Der Wechsel auf **Advanced Setup**. `py/stack-trace-exposure` meldete 208
Stellen, von denen 193 durch `nc.fehlertext.nach_aussen` laufen und dort
nachweislich gesäubert werden. Die Datenflussanalyse sieht die Säuberung
nicht — sie verfolgt `str(e)` durch die Funktion hindurch bis in die Antwort.

**208 Meldungen, die niemand mehr einzeln liest, sind schlimmer als keine.**
Genau das ist passiert: der Befund in `nc/routes/brain.py` — `str(ex)`, roh,
nur mit einem anderen Variablennamen als die W30-Prüfung suchte — stand
wochenlang unbemerkt in der Liste. Gefunden hat ihn erst das lokal
installierte CodeQL. Behoben.

**Die Regel wird ersetzt, nicht abgeschaltet.** `.github/codeql/` enthält
dieselbe Abfrage mit einer Barriere für `nach_aussen`/`_fehler_text`
(`nc/stack-trace-exposure`), die Konfiguration schließt nur die Standardfassung
aus. Ein blosses `exclude` hätte auch jeden neuen echten Befund verschluckt.

Vorher lokal geprüft, nicht gehofft:

| | Standard | mit Barriere |
|---|---:|---:|
| Testfall `str(e)` roh | gemeldet | **gemeldet** |
| Testfall über `nach_aussen` | gemeldet | unterdrückt |
| echte Codebasis | 208 | **14** |

Ein `# codeql[py/stack-trace-exposure]`-Kommentar unterdrückt übrigens
**nichts** — auch das wurde gemessen, bevor der aufwendigere Weg gewählt wurde.

**Gesamtbilanz über beide Teile von W3:**

| Regel | vorher | nachher |
|---|---:|---:|
| `py/stack-trace-exposure` → `nc/stack-trace-exposure` | 208 | **14** |
| `py/path-injection` | 17 | 17 |
| `py/incomplete-url-substring-sanitization` | 6 | 6 |
| `py/bad-tag-filter` | 4 | **0** |
| `py/url-redirection` | 2 | 2 |
| `py/sql-injection` | 2 | 2 |
| `py/weak-sensitive-data-hashing` | 1 | 1 |
| `py/insecure-temporary-file` | 1 | **0** |
| `py/cookie-injection` | 1 | 1 |
| **gesamt** | **242** | **43** |

Ein Vertrag hält die Namen zusammen: die Barriere greift über
`"nach_aussen"` und `"_fehler_text"`. Wird der Helfer im Python-Code
umbenannt und die Abfrage nicht, fiele die Barriere still weg und 193
Meldungen kämen ohne Vorwarnung zurück. Vier Negativtests, alle feuern.

> **Eine Handarbeit bleibt.** Solange in den Repo-Einstellungen das
> Default-Setup aktiv ist, bricht der neue Workflow beim Hochladen ab
> („default setup is enabled"). Einmalig abschalten unter
> **Settings → Code security → Code scanning → CodeQL analysis →
> Default setup → Disable**. Der Hinweis steht auch im Workflow-Kopf, damit
> niemand den Fehler im Workflow sucht.


### Behoben — 22 rohe Ausnahmetexte, die W30 durchgelassen hat (v4.2 W3)

**CodeQL läuft jetzt lokal** (Bundle 2.26.4, dieselbe Suite wie GitHubs
Default-Setup: `python-code-scanning.qls`). Damit lässt sich vor jedem Push
nachrechnen, was eine Änderung wirklich schließt — statt „sagt erst der
nächste Lauf".

Notwendig wurde das, weil die Alarme aus dieser Umgebung nicht abrufbar sind:
`api.github.com/rate_limit` antwortet 200, **jeder** `/repos/…`-Pfad 403;
Repo-Zugriff läuft nur über den GitHub-MCP, und der hat kein
Code-Scanning-Werkzeug. Der Umweg über CI-Artefakte fiel ebenfalls aus — das
CodeQL läuft über Default-Setup, also ohne Workflow-Datei im Repo, und erzeugt
keine Artefakte.

**Der erste Lauf hat das Bild korrigiert.** 242 Alarme, aber nicht die
Verteilung, die die Oberfläche nahelegt:

| Regel | Alarme | Urteil |
|---|---:|---|
| `py/stack-trace-exposure` | 208 | **22 echt**, 166 bereits gesäubert, 20 zu prüfen |
| `py/path-injection` | 17 | überwiegend bereits geriegelt (W2) |
| `py/incomplete-url-substring-sanitization` | 6 | 3 in Testdateien |
| `py/bad-tag-filter` | 4 | präzisiert |
| `py/sql-injection` | 2 | `dbwrap` mit gebundenen Parametern — Fehlalarm |
| `py/url-redirection` | 2 | **Fehlalarm, verifiziert** |
| `py/insecure-temporary-file` | 1 | behoben |
| `py/weak-sensitive-data-hashing` | 1 | bewusst so (Dedup-Id, siehe W2) |
| `py/cookie-injection` | 1 | **Fehlalarm, verifiziert** |

Die beiden „high"-Befunde sind nachweislich falsch: `_sicheres_ziel()` weist
alles ab, was nicht mit `/` beginnt — inklusive `//` und `/\`; und
`normalisieren()` kann nur `de`, `en` oder `None` liefern (gegen `'../etc'`,
`'<script>'`, `'fr'` durchgemessen).

**Die 22 echten sind eine Lücke in meinem eigenen W30-Vertrag.** Er verbot
`error=str(e)` — aber `error=f"JSON nicht lesbar: {e}"` ist derselbe
Leck-Weg, nur anders geschrieben, und stand danach noch an 22 Stellen. Sie
gaben genau das preis, wogegen W30 gebaut wurde: Dateipfade, den Wortlaut
fremder API-Antworten, bei `nc/routes/settings.py` potenziell Cookie-Inhalte.

Alle 22 laufen jetzt durch `_fehler_text`. `nc/routes/marketing.py` und
`nc/routes/news.py` hatten den Helfer noch nicht — nachgezogen.

**Der Vertrag prüft jetzt die FORM, nicht die Zeichenkette:** in einem
`except … as e` darf `{e}` in keinem f-string stehen, der an `jsonify`,
`Response`, `make_response`, `abort` oder `_oauth_page` geht. Nach AST, weil
ein f-string beliebig verschachtelt sein kann. **Log-Zeilen bleiben
ausdrücklich unangetastet** — dort ist der volle Wortlaut richtig, `nach_aussen()`
schreibt ihn selbst dorthin; ein Vertrag, der `log.warning(f"… {e}")` meldet,
wäre ein Dauer-Fehlalarm und flöge nach der dritten Welle raus.

**Zwei billige Präzisierungen mitgenommen:** die Tag-Muster akzeptieren jetzt
auch Attribute im schließenden Tag (`</script foo>`, was Browser durchgehen
lassen), und `tempfile.mktemp()` in `test_restream.py` ist `mkstemp()` gewichen —
`mktemp` vergibt nur einen Namen, zwischen Vergabe und Anlegen kann ein anderer
Prozess dort einen Symlink hinlegen.

#### Nachgemessen — und das Ergebnis widerspricht der Erwartung

Zweiter CodeQL-Lauf über denselben Baum:

| Regel | vorher | nachher | Delta |
|---|---:|---:|---:|
| `py/stack-trace-exposure` | 208 | 208 | **±0** |
| `py/bad-tag-filter` | 4 | 0 | −4 |
| `py/insecure-temporary-file` | 1 | 0 | −1 |
| **gesamt** | **242** | **237** | **−5** |

**Die 22 Fixes senken die Zahl nicht.** `_fehler_text` liest intern `str(e)`
und gibt das gesäuberte Ergebnis zurück — für die Datenflussanalyse fließt der
Ausnahmetext damit weiterhin bis in die Antwort. Sie sieht die Säuberung
dazwischen nicht.

Das Leck ist trotzdem zu. Nachgemessen am Säuberer selbst:

```
roh    : [Errno 2] No such file or directory: '/home/ubuntu/tiktok-bot/recordings/x.mp4'
aussen : FileNotFoundError: [Errno 2] No such file or directory: '<x.mp4>'

roh    : HTTP 401 von kick.com: token=abc123def456ghi789
aussen : RuntimeError: HTTP 401 von kick.com: token=<geschwärzt>

roh    : rtmp://ingest/app/46zAbCdEfGhIjKlMnOpQrStUvWxYz012345 refused
aussen : ValueError: rtmp://ingest/app/<geschwärzt> refused
```

Vorher gingen genau diese Zeichenketten unverändert nach draußen. Die
Alarmzahl misst hier also nicht die Sicherheit — sie misst, was die Analyse
erkennt.

Um die 208 wirklich zu schließen, gäbe es zwei Wege, beide eine
Betreiber-Entscheidung: ein **CodeQL-Model-Pack**, das `nach_aussen` als
Sanitizer deklariert (setzt Advanced Setup voraus und ersetzt damit das
Default-Setup), oder ein gesammeltes Abweisen der Meldungen mit Begründung.
Den Grund aus der Meldung zu entfernen, ist keine Option — das hat W30 aus
gutem Grund abgelehnt.


### Behoben — `main` war rot, und zwei automatische Sicherheits-Fixes waren der Grund (v4.2 W2)

Am 04.09. wurden sechs von GitHub erzeugte CodeQL-Auto-Fixes (#43–#48) direkt
nach `main` gemergt. **Zwei davon haben Schaden angerichtet, einer hat den
Testlauf zerstört.** Die CI von PR #42 lief noch gegen den Stand davor und war
grün — der Bruch fiel erst beim nächsten `fetch` auf.

| PR | Datei | Urteil |
|---|---|---|
| #44 | `nc/news.py` | **Regression** — sha1 → sha256 |
| #46 | `test_restream.py` | **kaputt** — die neue Zusicherung kann nicht greifen |
| #48 | `nc/oauthpage.py` | **Verbesserung** — behalten |
| #43, #45, #47 | Extraktor, Verträge | Umformulierungen, gleichwertig |

**#44 ist der schwerwiegendste.** `item_id()` trug seit v4.1-W10 genau den
richtigen Fix — `hashlib.new("sha1", …, usedforsecurity=False)` — mit dieser
Begründung darüber:

> *„Der WERT bleibt derselbe; ein Wechsel auf sha256 würde jede bereits
> veröffentlichte Meldung einmalig zur Neu-Meldung machen, weil ihre Id sich
> ändert."*

Der Auto-Fix hat diesen Kommentar **gelöscht** und genau die Änderung gemacht,
vor der er warnt. Der CodeQL-Befund ist damit formal erledigt und der Dedup
kaputt: jede bereits veröffentlichte News-Meldung wäre einmal neu erschienen.
Zurückgesetzt.

**#46 hat eine funktionierende Zusicherung durch eine unmögliche ersetzt.**
Aus `assert "ingest.global-contribute.live-video.net" in cfg` wurde ein
Regex-Muster `ingest\s*\([^)]*\)\s*:…`, das auf die Signatur
`def ingest(name) -> str:` **nicht passen kann** — zwischen `)` und `:` steht
ein Rückgabetyp. Damit schlug `test_restream.py` fehl, und der Ingest-Default
wäre nie wieder geprüft worden. Ersetzt durch einen Verhaltenstest.

**#48 wird behalten und der Vertrag angehoben.** `nc.oauthpage.kick()` ersetzte
manuell nur `&<>` und ließ Anführungszeichen stehen — „bewusst so", weil
bitgenau aus dem Monolithen übernommen. `html.escape(…, quote=True)` ist die
stärkere Zusicherung. Hier wurde der Vertrag korrigiert, nicht der Code
zurückgedreht.

**Drei weitere Anker gewandert, keiner gelöscht** — Muster, deren Absicht hielt,
deren Schreibweise die Auto-Fixes aber änderten. Die betroffenen Ausdrücke in
`tools/i18n_extract.py` und `tools/ncpatch.py` liegen jetzt als benannte
Konstanten an **einer** Stelle (`RE_BLOECKE_WEG`, `RE_JS_INHALT`,
`RE_SCRIPT_WEG`, `RE_SCRIPT_BLOCK`) und werden über ihr **Verhalten** geprüft,
nicht über ihre Schreibweise: `</script>`, `</script >` und `</SCRIPT\n>`
müssen alle drei als Ende gelten.

### Geändert — ein Riegel gegen Pfad-Ausbruch, überall derselbe (v4.2 W2)

`nc/sicherpfad.py` (neu): `sicherer_name`, `unter`, `sicher_join`,
`pruefe_unter`.

Die 241 offenen CodeQL-Befunde sind zum weit überwiegenden Teil **„Uncontrolled
data used in path expression"** — und nachgesehen trug fast jede betroffene
Stelle bereits eine Prüfung, nur jede in einer anderen Form: `abspath` +
`startswith` + `raise` (updater), `basename` + Zeichensatz-Regex (Archiv),
`basename` + Präfix-Erlaubnisliste (rollback), Mitgliedschaft in einem Tupel
(i18n), Nachschlagen in einem Dict (ops). Fünf Formen für eine Frage. Folge:
die statische Analyse erkennt keine davon, und eine neue Route erbt keinen
Riegel.

**Ein echtes Loch war trotzdem dabei.** `nc/updater._abs` prüfte mit
`os.path.abspath` — das löst **keine Symlinks** auf. Steht in der Wurzel ein
Link `raus -> /etc`, dann ist `abspath(root/raus/passwd)` genau
`root/raus/passwd`, die `startswith`-Prüfung sagt „drin", und geschrieben wird
nach `/etc/passwd`. Genau der Fall, den der Kommentar darüber ausschließen
wollte („Ein Zip-Slip schreibt sonst nach /etc"). Nachgemessen:
`abspath+startswith = True`, `realpath+commonpath = False`.

Ebenso `commonpath` statt `startswith`: `/daten/archiv2` beginnt mit
`/daten/archiv`, liegt aber nicht darin.

Angewendet in `nc/updater.py` (`_abs`, `rollback`), `nc/routes/archive.py`
(beide Zielpfade beim Umbenennen). `nc/i18n.py` schlägt die Katalogdatei jetzt
in `KATALOGDATEI` nach, statt `"%s.json" % sprache` zu bauen — die
Erlaubnisliste steht damit dort, wo sie wirkt.

Sieben Negativtests, alle feuern.

**Was das an den 241 Befunden ändert, ist offen.** Die Alarme lassen sich aus
dieser Sitzung heraus weder auflisten (API gesperrt) noch nachrechnen (kein
CodeQL lokal). Ob die statische Analyse den neuen Riegel als solchen erkennt,
sagt erst der nächste Lauf auf `main`.


### Geändert — Schnappschuss und Messwerte raus, ohne Geheimnisse (v4.2 W1)

Zweite Teillieferung von Vorschlag 2. `/api/system/config_snapshot` und
`/api/system/check_timing` liegen jetzt in `nc/routes/systemlage.py` —
**ohne einen einzigen neuen `nc.ctx`-Slot**, weiterhin 24 von 25.

Aufgelöst wurden vier Helfer:

- **`nc/discordlimits.py`** beantwortet das Upload-Limit jetzt selbst
  (`aktuell_mb`, `aktuell_label`, `guild_filesize_bytes`). Bisher war das
  Modul reine Rechnung — Bytes rein, MB raus — und wer das Ergebnis wollte,
  musste im Bot fragen. Der verbundene Client liegt seit W16 ohnehin als
  Register in `nc/discordstate.py`.
- **`_faster_whisper_available`** war eine **zweite, schwächere Kopie** von
  `nc.whispercfg.verfuegbar()`: dieselben drei Zeilen, aber ohne das `try`.
  Ein kaputter Paket-Baum hätte dort eine Ausnahme geworfen, statt „nein" zu
  sagen. Der Bot benutzt jetzt die vorhandene Fassung.
- **`_piper_available`** war bereits ein Alias auf `nc.piper_voices`.
- Der **Restream-Manager** kommt aus dem Register `nc/restreamstate.py` — mit
  Wache gegen `None`: vor dem Start stirbt sonst die ganze Antwort an einem
  `AttributeError`, statt eine leere Zielliste zu melden.

**Ein Geheimnis weniger im Umlauf.** Der Schnappschuss beantwortet nur, **ob**
etwas gesetzt ist. Die Werte dafür durch den Kontext zu reichen, damit ein
Blueprint sie zu `True` verrechnet, wäre größere Angriffsfläche für null
Gewinn — dieselbe Überlegung wie bei `s3_zugang()` in W24. Es gehen daher
`HAT_DASHBOARD_TOKEN`, `HAT_DISCORD_BOT_TOKEN`, `HAT_KICK_CREDS` und so
weiter, keine Klartextwerte.

**Der Vertrag fand dabei einen Altbestand:** `KICK_CLIENT_SECRET` lag seit W9
im Kontext und war damit für **jedes der 35 Blueprints** erreichbar — benutzt
wurde es an genau drei Stellen in `nc/routes/kick.py`, und zwar ausschließlich
für `bool(id and secret)`. Der Token-Tausch läuft im Bot, nicht in einer
Route. Ersetzt durch `HAT_KICK_CREDS`, der Eintrag ist raus. Nachgemessen: von
zwei gesetzten Testgeheimnissen erscheint keines in der Antwort **und** keines
im Kontext.

**Das Panel war nie übersetzbar.** Fünf Urteilstexte und der Transcode-Hinweis
erreichen das DOM in einem JSON-Feld — der Browser-Übersetzer sieht ganze
Textknoten, ein Wert in einer JSON-Antwort ist keiner. Im Monolithen blieb das
Panel deshalb dauerhaft deutsch, auch im englischen Deck. Jetzt an der Quelle
übersetzt; Katalog 1376 → **1382**.

Sechs Negativtests, alle feuern: Geheimnis wieder im Kontext, Zustand als
Kopie statt Referenz, `globals()` im Blueprint, fehlende `None`-Wache,
durchbrochene Qualitäts-Untergrenze beim Upload-Limit, eigene
Whisper-Prüfung im Bot.

**Ein eigener Irrtum, den der Vertrag korrigiert hat:** ich hatte erwartet,
dass ein Betreiber-Deckel von 5 MB auf 5 MB führt. Er führt auf 8 —
`FLOOR_MB` ist eine bewusste Qualitäts-Untergrenze. Der Vertrag prüft jetzt
genau das, statt meine falsche Annahme.

Es bleiben drei System-Routen im Monolithen: `preflight`, `resilience` und
`selftest`.

---

## [4.2] — 2026-09 · „Zerlegter Kern"

### Neu — Vorschläge gesammelt entscheiden (v4.2)

Der Evolutions-Kern legt Vorschläge an; abgearbeitet wurde bisher **einzeln**.
Bei zwanzig offenen Einträgen heißt das vierzig Klicks — die Liste wurde
dadurch nicht gelesen, sondern ignoriert.

Zwei Knöpfe über der Liste: **„✓ alles übernehmen"** und **„alles verwerfen"**.
Dazu eine eigene Route `POST /api/evolution/proposals/bulk`.

**Warum eine Route und keine Schleife im Browser:** zwanzig POSTs wären zwanzig
Transaktionen und zwanzig Audit-Einträge — und bricht einer davon ab, bleibt
die Liste halb bearbeitet zurück, ohne dass jemand sagen kann, welche Hälfte.
Eine Anweisung, ein Ergebnis, eine Zahl.

**Die Aktion fasst nur `status='proposed'` an.** Ein bereits übernommener
Vorschlag darf durch einen späteren Klick auf „alles verwerfen" nicht
rückwirkend zu „verworfen" werden — das wäre eine Umschreibung der
Entscheidungshistorie, nicht eine Massenaktion.

Die Rückfrage vor dem Verwerfen nennt die **Zahl**: eine Frage ohne Zahl
beantwortet man anders als eine, die 17 nennt. Die Knöpfe sind ausgeblendet,
solange nichts offen ist — ein Knopf, der auf eine leere Liste wirkt, tut
nichts und sieht wie ein Fehler aus.

### Behoben — der Build-Stempel stand vier Mal im Code und wanderte nie mit (v4.2)

Gemeldet als „Build steht immer noch auf 08.2026". Der Befund war schlimmer
als die Meldung:

1. **Der Footer war statisches HTML.** `<b>v4.1</b>` und `<b>2026.08</b>`
   standen wörtlich in `dashboard.html`. Wer `nc/version.py` hochzählte,
   bewegte den Footer nicht mit.
2. **`/api/version` lieferte `build: ""`.** Die Route las
   `globals().get("BUILD_STAMP", "")` — seit W26 liegt sie in einem Blueprint,
   und dort ist `globals()` der Namensraum **dieser** Datei, in dem
   `BUILD_STAMP` nie stand. Der Bot reicht ihn seit W116 über `ctx.cfg`
   herein; die Route benutzte ihn nur nie. Eine stille Fehlanzeige, die
   niemand sah, weil der Footer ohnehin fest verdrahtet war.
3. **Vier Kopien derselben Zeichenkette:** `nc/version.py`, `bot.py`,
   `nc/routes/brain.py` und der Footer. Ein Modul, das sich „eine einzige
   Wahrheit" nennt, darf keine Kopien haben.

Jetzt: `nc.version.build_stamp()` ist die einzige Vorgabe, `bot.py` und
`nc/routes/brain.py` leiten davon ab, `/api/version` liest aus `ctx.cfg`, und
der Footer **holt** die Version, statt sie zu behaupten. Der Wert im Markup ist
nur noch der Auslieferungsstand.

Nachgemessen nach dem Fix: `/api/version` meldet `build='2026.09 · v4.2'`,
`/api/brain/health` dasselbe.

### Version 4.2 — „Zerlegter Kern"

Der September in einer Zahl. Zehn Wellen (W22–W33): sieben Routengruppen aus
dem Monolithen, Dashboard-Übersetzung von 18 % auf 89 %, kein blockierter
Ereignis-Loop mehr, gesäuberte Fehlertexte, Dauerwarnung beim offenen Deck,
Rauchtest in der CI. Die Wellenzählung beginnt mit 4.2 neu — wie beim Übergang
von v4.0-W126 auf v4.1-W2. Die Wellen W22 bis W32 tragen deshalb noch die
Marke `v4.1-Wxx` — sie sind unter dieser Nummer entstanden und werden nicht
rückwirkend umbenannt; die Verträge und Commits verweisen darauf.


### Geändert — die Sondenschicht raus, drei System-Routen hinterher (v4.1 W32)

Erste Teillieferung von Vorschlag 2, dem harten Rest des Monolithen. Die acht
System-Routen greifen zusammen auf **112 verschiedene Namen** aus `bot.py` zu —
mehr als jede Gruppe, die bisher gewandert ist. Deshalb kommen sie zuletzt, und
deshalb geht es nach der W117-Regel: **erst die Zustandsschicht auflösen, dann
kosten die Routen nichts.**

Aufgelöst wurde die Sondenschicht:

- **`nc/systemprobe.py` (neu)** — `redis_alive`, `redis_version`,
  `ai_calls_total`, `active_recorder` und der 5-Sekunden-Deckel (F24), der sie
  zusammenhält. Reine stdlib; im Monolithen hingen sie nur an den Konstanten
  `REDIS_URL` und `RECORDER_PREF` fest. Die Redis-Sonden sprechen weiterhin
  RESP direkt über einen Socket statt über das `redis`-Paket — Absicht: die
  Sonde muss auch antworten, wenn das Paket fehlt, sonst meldet das Deck
  „Redis tot", weil eine Bibliothek nicht installiert ist.
- **`nc/cookies.load_dict`** — der Leser von `cookies.txt`, wörtlich übernommen.
  Er lag als einziger Cookie-Teil noch im Bot, während die übrige
  Format-Verarbeitung längst in diesem Modul steht. 16 Aufrufstellen, alle über
  einen Alias unverändert.
- **`nc/logsafe.url_ohne_zugang`** — der Maskierer für Zugangsdaten in URLs
  (W118). Dieselbe Aufgabe wie `redact_stream_urls`, jetzt dieselbe Datei.

Danach ließen sich drei Routen ohne **einen einzigen neuen `nc.ctx`-Slot**
herauslösen — `nc/routes/systemlage.py`: `/api/system`,
`/api/system/preflight_history`, `/api/system/config_drift`.
Slots weiterhin **24 von 25**.

**Eine stille Fehlanzeige dabei verhindert:** `api_config_drift` übergab
`__file__` an `nc/confdrift`, das den Quelltext nach `os.getenv`-Vorgaben
durchsucht. In einem Blueprint zeigt `__file__` auf **dessen** Datei — dort
steht keine einzige Vorgabe, und die Antwort wäre ein leerer Bericht mit
`ok: true` gewesen. Der Pfad kommt jetzt aus `cfg["BOT_DATEI"]`; ein Vertrag
hält es fest.

**Konfiguration als Injektion, nicht als Modul-Konstante.** Beide neuen Module
lesen kein `os.getenv` auf der Modul-Ebene — CLAUDE.md: „.env wird teils erst
nach den ersten Imports geladen". Ein Vertrag prüft das per AST für
`nc/systemprobe.py` und `nc/cookies.py`.

**Ein Cookie-Cache, nicht zwei.** Der Bot leert ihn nach einer
Cookie-Reparatur, das Deck liest ihn über `ctx.cfg` — eine Kopie wäre ein totes
Panel und ein Cache, den niemand mehr invalidiert. `nc.cookies.CACHE` ist
dasselbe Objekt, der Vertrag prüft die Identität.

Vertrag `_test_w32_sondenschicht_und_systemlage`, sechs Negativtests, alle
feuern: `__file__` im Blueprint, `os.getenv` auf Modul-Ebene, `pref=ytdlp`
fällt still auf native zurück, der Deckel hält kein negatives Ergebnis fest,
der Cookie-Cache als Kopie, die Domain-Kollision nur nach Expiry aufgelöst.

**Zwei Anker gewandert, keiner gelöscht:** die Cookie-Log-Drossel
(`test_deepbughunt_fixes`) und der Maskierer-Vertrag aus W118
(`test_v40_w118_sicherheitsaudit`) zeigten auf `bot.py`. Beide prüfen jetzt die
neue Stelle **und** zusätzlich, dass `bot.py` sich keine zweite Wahrheit
zurückholt.

Doku-Zahlen nachgezogen: `bot.py` 26.585 → **26.392 Zeilen**, `nc/` 118 → **119
Module**, `nc/routes/` 34 → **35 Blueprints** mit 317 → **320 Routen**, eigene
Routen in `bot.py` 42 → **39**. `README.en.md` stand noch bei 92 Modulen und
27.218 Zeilen — `ncpatch docs` prüft die englische Fassung nicht, deshalb war
die Drift dort unbemerkt gewachsen.

Es bleiben fünf System-Routen im Monolithen: `preflight`, `resilience`,
`check_timing`, `config_snapshot` und `selftest`. Sie hängen noch am
Discord-Client, am Restream-Manager und am Watchdog-Zustand und folgen, wenn
der aufgelöst ist — nicht vorher.


### Behoben — der Rauchtest lief nirgends automatisch (v4.1 W31)

`test_smoke.py` steht seit v37 in der Pflicht-Prüfkette. Ausgeführt hat ihn
trotzdem **keine Maschine regelmäßig**: auf der Autorenmaschine fehlte der
Laufzeitstack, die CI schloss ihn ausdrücklich aus, und auf dem Server lief er
nur, wenn jemand daran dachte. Ein Test in der Pflichtkette, den niemand
ausführt, ist eine Zeile Dokumentation, keine Prüfung.

Er ist zugleich der einzige, der `bot.py` **wirklich ausführt** — und damit der
einzige, der `NameError` auf der Modul-Ebene, eine Route mit 500er beim ersten
Aufruf oder einen nie verdrahteten Rückruf überhaupt sehen kann. Genau solche
Fehler haben in W26 (`_claude_chat_sync_metered`, 9× in Produktion) und W29 in
Produktion zugeschlagen.

**Die Begründung für den Ausschluss war falsch.** Nachgemessen braucht der Test
*nicht* den Serverbestand:

- TikTokLive und python-telegram-bot **stubbt er selbst**.
- requests, httpx, boto3, redis, PyMySQL, PySocks und faster-whisper werden
  erst **innerhalb** von Funktionen importiert.
- ffmpeg, streamlink und yt-dlp fasst er **gar nicht** an.
- Ein `.env` braucht er nicht — er setzt sich die nötigen Variablen selbst.

Übrig bleiben **fünf** Pakete. Sie stehen jetzt in `requirements-smoke.txt`
(nicht in `requirements.txt`: die zieht faster-whisper, boto3 und uvloop mit,
und genau deren Installationsdauer war die Begründung, warum der Job fehlte).
Installation rund 20 Sekunden.

**Neu:** CI-Job `Rauchtest (bot.py laeuft wirklich)` — Python 3.13,
`PYTHONUTF8=1`, Installation aus `requirements-smoke.txt`, dann
`python test_smoke.py`. Ergebnis auf dieser Codebasis: **10 Verträge grün**,
360 Routen registriert, 203 GET-Routen aufgerufen, 0 unerwartete 5xx.

**Damit er lauffähig bleibt** — der eigentliche Punkt der Welle: der Vertrag
`_test_w31_rauchtest_laeuft_in_der_ci` vergleicht die Modul-Ebene von `bot.py`,
`nc/` (178 Dateien) und `brain/` gegen `requirements-smoke.txt`. Ein neuer
Import ohne Eintrag würde den CI-Job an einem nackten `ImportError` töten,
mitten in der Liste, ohne Hinweis worauf — der Vertrag meldet ihn stattdessen
mit Datei, Import- und Paketnamen. Umgekehrt meldet er tote Einträge: eine
Liste, die still wächst, macht den Job wieder teuer. Importe in einem `try`
mit `except ImportError` zählen als optional und dürfen fehlen.

**Ein Loch im Rauchtest selbst mitgeschlossen:** `discord` ist im Code optional
(`except Exception: discord = None`). Ohne das Paket lief der Test bis zum Ende
grün — und hatte dabei die gesamte Slash-Command-Registrierung nie angefasst.
Dort saß B79: discord.py löst Annotationen wie `member: discord.Member` über
`callback.__globals__` auf, ein fehlender Modul-Import ließ den ganzen
Discord-Bot beim Registrieren crashen. `test_smoke.py` prüft jetzt
`m.discord is not None` und sagt, warum.

Vier Negativtests, alle feuern: neuer Modul-Import ohne Eintrag, entfernter
Eintrag, toter Eintrag, entkernter CI-Job.

Doku nachgezogen: `CLAUDE.md`, `CLAUDE.en.md`, `docs/CONTRIBUTING.md`,
`docs/en/CONTRIBUTING.md`, `README.md`, `README.en.md`, der Kopfkommentar von
`ci.yml` und die PR-Vorlage behaupteten alle das Gegenteil.


### Behoben — die Warnung vor dem offenen Dashboard war unsichtbar (v4.1 W30)

Die Schranke des Dashboards (`_auth_guard`) macht **gar nichts**, wenn weder
`DASHBOARD_TOKEN` noch `DASHBOARD_PIN` gesetzt ist:

```python
if not DASHBOARD_TOKEN and not DASHBOARD_PIN:
    return None          # jede Adresse, jeder Pfad, frei
```

Solange `WEB_HOST` auf dem Loopback steht, ist das gewollt — dann kommt nur
der SSH-Tunnel durch. Steht dort etwas anderes, ist das Deck offen im Netz:
Aufnahmen löschen, Konfiguration zurückspielen, Log mitlesen.

Eine Warnung dafür gab es. Sie hatte **drei Mängel**, zwei davon sind die
Fallen, die CLAUDE.md selbst benennt:

1. **Sie lief auf `log.warning`.** „Ein `log.warning` erscheint in einem
   ERROR-Log **nie**" — so blieb der Discord-Gateway-Tod monatelang
   unsichtbar. Für einen Sicherheitszustand ist das die falsche Stufe.
2. **Sie kam nur beim Start.** Der Betreiber liest das Log, wenn etwas kaputt
   ist, nicht beim Hochfahren. Der gefährliche Zustand ist aber ein
   **Dauerzustand** — er verschwindet nicht, bis jemand die `.env` anfasst.
3. **Sie fragte nur nach dem Token, nicht nach dem PIN.** Ein PIN-geschütztes
   Deck löste sie fälschlich aus. Ein Fehlalarm erzieht dazu, die Meldung zu
   überlesen — und dann auch die im echten Fall.

`nc/dashauth.py` beantwortet die Frage jetzt an einer Stelle, mit **derselben
Bedingung, die die Schranke selbst benutzt**. Die Meldung läuft auf `error`
und wiederholt sich alle sechs Stunden, solange der Zustand anhält — und
schweigt vollständig, sobald ein Token oder ein PIN gesetzt ist.

### Behoben — roher Ausnahmetext in API-Antworten (v4.1 W30)

**161 Stellen** antworteten mit `jsonify(ok=False, error=str(e))`, weitere 15
reichten den Wortlaut über ein Dict nach draussen. CodeQL meldete das als
`py/stack-trace-exposure` und bei jeder Verschiebung in einen Blueprint
erneut als „neu" — fünfmal habe ich in einer PR vorgerechnet, dass die Bilanz
stimmt. Das war die Antwort auf die Meldung, nicht auf die Sache.

Ob es ein echtes Problem ist, hängt am Betrieb — und nach dem Befund oben ist
es eines: bei offener Schranke geht jede dieser Meldungen an jeden, der den
Port erreicht, mitsamt Dateipfaden, Datenbank-Interna und gelegentlich dem
Wortlaut einer Antwort einer fremden API.

**Kein Entweder-Oder.** „Interner Fehler" wäre in einem Ein-Personen-Betrieb
keine Sicherheit, sondern eine Sackgasse — der Betreiber ist der einzige
gewollte Leser. `nc/fehlertext.py` löst es anders:

* **Der Wortlaut geht ins Log**, vollständig, mit Ausnahmetyp.
* **Nach aussen geht eine gesäuberte Fassung**: absolute Pfade auf den
  Dateinamen gekürzt, alles nach `token=`/`key=`/`secret=` geschwärzt, lange
  Zufallsketten (Stream-Keys) geschwärzt, auf 200 Zeichen begrenzt.
* **Der Ausnahmetyp bleibt.** „OperationalError" sagt Datenbank,
  „TimeoutError" sagt Netz — das ist die halbe Diagnose und verrät nichts
  über den Bestand.

Umgeschrieben wurde über den AST mit **Byte-Offsets**, nicht über Zeichen:
`col_offset` ist ein UTF-8-Byte-Offset, und in diesen Dateien stehen Umlaute
(die Falle aus W20, dort schrieb ein Zeichen-Slice prompt `), )400`).

`str(e)` in **allen** Blueprints: **0**. In `bot.py` bleiben 45 — Logzeilen
und interne Rückgabewerte, wo der Wortlaut hingehört.

### Behoben — das Ereignisprotokoll blockierte den Event-Loop (v4.1 W29)

Fortsetzung des Befunds aus W26. `log_event` schrieb **synchron** in die
Datenbank, aus jedem Pfad — auch aus async-Funktionen. Unter Plattenlast
blockiert SQLite, und dann steht nicht die Abfrage, sondern der ganze Bot.
Einer der Stack-Abzüge vom 2026-09-03 zeigte genau diese Kette
(`on_comment` → `log_event`).

Die Funktion hat über dreissig Aufrufer, synchrone wie asynchrone. Sie alle
auf `await` umzustellen hätte dreissig Stellen angefasst und die Zusicherung
gebrochen, die in ihrem eigenen Docstring steht: „Caller darf das aus jedem
Pfad aufrufen ohne Risiko".

Deshalb der andere Weg: **`nc/eventlog.py` — eine Warteschlange und EIN
Schreiber-Thread.** Der Aufrufer legt ab und geht weiter. **Keine einzige
Aufrufstelle musste geändert werden**, und die Zusicherung gilt jetzt sogar
stärker: der Aufruf wartet nie mehr. Gemessen: 500 Einträge in 1 ms
(0,002 ms je Aufruf), Reihenfolge exakt erhalten.

Drei Entscheidungen, die im Modul begründet stehen:

* **Die Schlange ist begrenzt** (2000). Ein unbegrenzter Puffer vor einer
  hängenden Platte ist ein Speicherleck mit Anlauf — dieselbe Sorte wie der
  Adress-Cache in W25. Läuft sie voll, werden neue Einträge verworfen **und
  gezählt**: ein Prüfprotokoll, das still Einträge verliert, ist schlimmer
  als keines, denn die Lücke sieht aus wie Ruhe.
* **Ein Schreiber.** Das Protokoll ist eine Chronik; zwei Threads würden die
  Reihenfolge zerwürfeln.
* **Gebündelt** (bis 50 pro Transaktion). Bei einem Chat-Ansturm ist das der
  Unterschied zwischen zweihundert Schreibvorgängen und zweien — und die
  Platte war das Problem.

**Ein Fehler in meinem eigenen Entwurf, gefunden im Überlast-Test:** die
Fehler-Drosselung lief über `_ZÄHLER["fehler"] % 100 == 1`. Der Zähler wächst
aber in Bündeln von bis zu 50 — 50 und 100 treffen die 1 nie. Der
Schreibfehler wäre **still** geblieben, ausgerechnet der, der die Chronik
löchert. Jetzt zeitgedrosselt.

`reaper_loop` läuft ebenfalls neben dem Loop. Er räumt im Minutentakt tote
Recorder-Prozesse ab und las dabei synchron aus der Datenbank.

### Geändert — der Sendebild-Chat läuft neben dem Loop, mit EINEM Arbeiter (v4.1 W29)

`_restream_chat_push` wird aus **dreizehn** Stellen gerufen, alle in
async-Funktionen: TikTok-Kommentare, Geschenke und Follows, der
Kick-Websocket, Twitch-Chat und -EventSub, der YouTube-Chat. Also bei **jeder
Chat-Nachricht jeder Plattform**. Dabei schreibt die Funktion Treuepunkte in
die Datenbank — synchron, auf dem Loop.

In W29 hatte ich sie zurückgestellt, weil in einem gewöhnlichen Thread-Pool
die **Reihenfolge des Chats** an der Scheduling-Reihenfolge der Threads hinge.
Diese Sorge war berechtigt, nicht bloß vorsichtig — nachgemessen:

| | 200 Nachrichten in Einreichungsreihenfolge? |
|---|---|
| ein Arbeiter | **ja** |
| acht Arbeiter | **nein** |

Deshalb genau **ein** Arbeiter. Damit bleibt die Reihenfolge exakt die der
Einreichung, und der Loop ist trotzdem frei (nachgemessen: 51 ms Taktlücke bei
einem 400-ms-Push, also der normale Takt).

Der Aufrufer **wartet** (`await`). Das ist Absicht: hängt die Platte, bremst
der Rückstau die Chat-Schleife, statt eine unbegrenzte Schlange aufzubauen —
dieselbe Überlegung wie bei der begrenzten Warteschlange des
Ereignisprotokolls, nur mit Gegendruck statt Verwerfen.

Ein Vertrag hält beides fest: genau ein Arbeiter, und **kein** Aufrufer, der
an der nebenläufigen Hülle vorbeigeht.

### Geändert — der Pfad der manuellen Aufnahme (v4.1 W29)

Fünf blockierende Blöcke in `trigger_manual_recording`, **vier davon
wortgleich** — dieselbe `UPDATE manual_recordings SET status=…`-Anweisung,
jedes Mal in einem eigenen `try: … except Exception: pass`. Ein Helfer löst
beides: die Blockade und die Wiederholung.

Stand: **71 → 52** blockierende Stellen.

### Geändert — die ereignisgetriebenen Pfade laufen neben dem Loop (v4.1 W29)

Nach den Dauerläufern die Stellen, die pro **Ereignis** laufen statt pro
Befehl:

* **`_award_xp`** — bei jeder Discord-Nachricht. Zwei Blöcke: die
  Live-Prüfung (30 s gecacht, der Cache dämpfte die Zahl der Abfragen, nicht
  ihre Blockade) und die XP-Buchung. Lesen und Schreiben bleiben in **einer**
  Transaktion: sonst könnten zwei Nachrichten desselben Nutzers denselben
  Stand lesen und ein XP-Gewinn ginge verloren. Der 60-s-Cooldown macht das
  unwahrscheinlich, nicht unmöglich.
* **`on_raw_reaction_add`** — bei jeder Discord-Reaktion, drei Blöcke.
* **`handle_recording_finished`** und **`_wait_and_finish`** — nach jeder
  Aufnahme, drei Blöcke. Die Absicherung gegen das Wettrennen beim
  Auto-Abschalten steckt im `WHERE` der Anweisung, nicht darin, dass der
  Aufruf auf dem Loop läuft.

Stand: **71 → 57** blockierende Stellen.

### Behoben — offene Transaktion über ein `await` hinweg (v4.1 W29)

Beim Umstellen der Dauerläufer kam ein zweiter, andersartiger Befund zutage:
in `_community_events_loop` und `/daily` stand ein `await` **innerhalb** eines
offenen `db_conn()`-Blocks — einmal ein Discord-Versand, einmal eine Antwort
an den Nutzer.

Das blockiert den Event-Loop **nicht** (das `await` gibt ihn frei) und ist
deshalb in keinem Stack-Abzug aufgetaucht. Es hält aber die Verbindung und
damit den Schreib-Lock offen, während auf das Netz gewartet wird. Bei einem
langsamen Discord bekommt in dieser Zeit **jeder andere Schreiber**
„database is locked" — und die Ursache steht in einer Schleife, die nur jede
Minute läuft.

Beide Stellen lesen jetzt zuerst, senden dann, und schreiben zum Schluss. Ein
Vertrag lässt kein `await` mehr in einem offenen `db_conn()`-Block zu.

Nebenbei gefunden: `_nc_i18n.t(f"@here 🔴 **{r['title']}** geht JETZT los!")`
— ein `t()` um einen **f-String**. Der Katalogschlüssel hätte den Titel des
Events enthalten und nie getroffen. Jetzt läuft nur der feste Teil durch die
Übersetzung.

### Geändert — kein Dauerläufer blockiert mehr (v4.1 W29)

`_restream_verify_loop`, `_intel_index_loop` (zwei Stellen) und
`_community_events_loop` laufen neben dem Loop. Dauerläufer sind die
schlimmsten Blocker: sie wiederholen sich für immer, also trifft ihre Blockade
früher oder später jeden Betriebszustand. Ein Vertrag hält fest, dass keiner
zurückfällt.

Stand: **71 → 65** blockierende Stellen.

### Hinzugefügt — `db_async` (v4.1 W29)

`nc/dbwrap.db_async(fn)` führt `fn(conn)` mitsamt Verbindungsauf- und -abbau
in einem Thread aus. Die Verbindung entsteht **im** Thread: eine
sqlite3-Verbindung gehört dem Thread, der sie geöffnet hat, und eine über die
Thread-Grenze gereichte wirft zur Laufzeit.

Nachgemessen: derselbe blockierende Zugriff kostet den Takt **411 ms**
synchron und **50 ms** (also nichts) über `db_async`.

### Ein Vertrag als Ratsche

70 blockierende Stellen sind noch im Bestand. Eine harte Null wäre heute
unerreichbar und deshalb wertlos — sie würde sofort abgeschaltet. Der Vertrag
setzt stattdessen eine **Obergrenze, die bei jeder Welle sinkt**: die Zahl
darf fallen, nie steigen. Gegenprobe gemacht — eine neu eingefügte
blockierende Stelle meldet er namentlich.

**Korrektur an meiner eigenen Meldung:** ich hatte 115 solcher Stellen
gemeldet. Die richtige Zahl ist **71** (jetzt 70). Die erste Zählung ordnete
`db_conn()`-Blöcke der lexikalisch umschliessenden async-Funktion zu, statt
der unmittelbar umschliessenden — Blöcke in verschachtelten **synchronen**
Helfern laufen längst über `asyncio.to_thread` und blockieren nichts.
`_discord_run_once` mit angeblich 31 Stellen fällt damit ganz aus der Liste.

### Behoben — die Abdeckungszahl maß den kleineren Teil (v4.1 W28)

Gemeldet wurden **970 Einträge, 0 fehlend**. Gemessen am Dashboard waren davon
**18 % der Textknoten** erfasst. Die Zahl war nicht falsch gerechnet — sie
zählte nur, was der Extraktor eingesammelt hatte, und das war der kleinere
Teil.

**Ursache:** Für Texte zwischen zwei Tags verlangte der Extraktor einen
deutschen Marker (Umlaut oder Funktionswort). „Aufnahmen", „Analysieren",
„BEFUNDE", „7-TAGE-TREND" haben weder das eine noch das andere und sahen
deshalb aus wie Bezeichner. Die Ausnahme, die W18 für `<th>Datei</th>`
beschrieben hatte, stand im Kommentar der Funktion — angewandt wurde sie an
dieser Aufrufstelle nie.

Dieselbe Krankheit wie die toten Einträge aus W21/W23/W27, nur umgekehrt:
dort zählte Erfasstes mit, das nie griff; hier fehlte das meiste und wurde
nie gezählt.

**Vier Befunde beim Aufräumen, alle behoben:**

1. **Die Bezeichner-Prüfung hing an der Deutsch-Heuristik.** Wer die eine
   abschaltete, verlor die andere. Das sind zwei getrennte Fragen: „ist das
   überhaupt Text?" und „ist das *deutscher* Text?". Jetzt entkoppelt.
2. **22 Katalogschlüssel trugen HTML-Entities.** Der Browser sieht den
   dekodierten Text — aus `BACKUP &amp; EXPORT` wird im DOM
   „BACKUP & EXPORT". Diese Einträge waren tot. Extraktor und Katalog lösen
   Entities jetzt auf.
3. **Mehrzeilige Hilfetexte waren ganz ausgeschlossen** — die längsten und
   nützlichsten Texte im Deck. Extraktor **und** Browser normalisieren innere
   Umbrüche jetzt gleich; hinge der Schlüssel an der Einrückung im HTML,
   würde jede Umformatierung ihn stillschweigend töten.
4. **Ein Regressions-Fehler meiner eigenen Entkopplung** — „Restream-Status"
   ist die Beschreibung eines Slash-Befehls und sieht bloß aus wie ein
   Bezeichner. Der Verwaisten-Melder hat ihn gemeldet.

**Was bewusst NICHT übersetzt wird**, steht jetzt als namentliche Liste im
Extraktor (`_KEIN_TEXT`), nicht als Heuristik: Produkt- und Markennamen
(„Kick" heißt auf Englisch „Kick"), technische Bezeichner, bewusst englische
Gestaltung und Fälle, in denen Deutsch und Englisch wortgleich sind. Ein
Identitäts-Eintrag wäre Rauschen — und genau den verbietet der Vertrag aus W6.

Katalog: 970 → **1367** Einträge. Dashboard-Abdeckung **18 % → 89 %**,
brain.html 85 %, Website 79 %. Der Rest sind von Inline-Tags zerschnittene
Sätze: die lassen sich nicht knotenweise übersetzen, ohne das HTML umzubauen.

Ein Vertrag misst die Abdeckung jetzt selbst und fällt unter 85 %.

### Behoben — verkettete Textzuweisungen blieben deutsch (v4.1 W27)

Die dritte Stelle derselben stillen Buchhaltung, nach den nativen Dialogen
(W21) und den verketteten Toasts (W23). Der DOM-Übersetzer trifft **ganze**
Textknoten. Bei

```js
el.textContent = 'Quelle: ' + name
```

heißt der Knoten „Quelle: kick"; ein Katalogeintrag für `Quelle: ` trifft dort
nie. **Zehn solcher Einträge standen bereits im Katalog** und zählten als
übersetzt, ohne je zu greifen.

84 Literale in verketteten `textContent`/`innerText`/`innerHTML`-Zuweisungen
laufen jetzt durch `T()`. Unberührt bleiben ganze Literale (die sind schon
vollständige Knoten) und Markup — Tags, Attribute und CSS-Variablen sind kein
Benutzertext.

**Ein Fall musste aufgetrennt werden.** In

```js
o.innerHTML='<span …>✓ veröffentlicht</span> …'+n+' News auf der Website ('+m+' neu)</span>'
```

klebte Prosa am Markup und war deshalb nicht umschließbar — die Meldung wäre
zur Hälfte übersetzt gewesen, englischer und deutscher Text im selben Satz.
Markup und Text stehen jetzt getrennt. Ein Vertrag lässt genau das nicht mehr
zu.

`MODULES ONLINE` war englischer **Quelltext** in einer deutschen Oberfläche.
Nach der Regel aus W19 ist der deutsche String der Schlüssel: die Anzeige
heißt jetzt `MODULE ONLINE`, der Katalog trägt das Englische. Ein bestehender
Vertrag hat das gemeldet — er verbietet Einträge, deren „Übersetzung" mit der
Quelle identisch ist, weil die als erledigt zählen, ohne etwas zu tun.

Der neue Vertrag prüft drei Dinge: keine verkettete Zuweisung ohne `T()`,
keine Prosa am Markup, und dass **Nachschlag und Extraktor beide trimmen** —
fiele eines von beiden weg, wären alle Fragment-Einträge (`Quelle: `,
` aktiv`) auf einen Schlag tot und die Abdeckungszahl löge wieder.

Katalog: 906 → **970** Einträge, 0 fehlend, 0 verwaist. Vier Vertrags-Anker
sind mitgewandert, keiner gelöscht.

### Behoben — `_living_title_loop` starb bei jedem Lauf (v4.1 W26)

Aus dem Betriebslog vom 2026-09-03, neunmal:

```
TypeError: _claude_chat_sync_metered() got an unexpected keyword argument 'on_error'
```

Der Monolith **ersetzt** `nc.claude.chat_sync` durch eine Hülle, die die Token
zählt. Diese Hülle zählte ihre Parameter einzeln auf. Als v4.1-W13 `on_error`
zu `chat_sync` hinzufügte, wurde sie nicht mitgezogen — und weil sie die
Funktion im Modul ersetzt, brach jeder Aufruf mit dem neuen Parameter. Im Log
stand nur „Schleife gestört"; der Grund kam erst aus dem Traceback.

Beide Zähl-Hüllen (Claude und freeai) reichen jetzt mit `**weitere` alles
durch, was sie nicht selbst brauchen. Die ersten Parameter bleiben ausdrücklich
einzeln stehen: drei Aufrufstellen übergeben `model` und `timeout`
**positionell**, und ein Zusammenfassen hätte das Modell in den falschen
Parameter geschoben — ein stiller Fehler statt eines lauten.

Ein Vertrag vergleicht die Hüllen jetzt gegen die echte Signatur der Module
(`inspect.signature`) und prüft zusätzlich die Reihenfolge der
Positions-Parameter. Gegenprobe gemacht: mit zurückgebauter Hülle meldet er
genau den Fehler, der neunmal im Log stand.

### Behoben — der Event-Loop stand bis zu 68 Sekunden (v4.1 W26)

Aus demselben Log. Der Wächter meldete Blockaden von 30 bis 68 Sekunden; in
dieser Zeit stand der ganze Bot: keine Live-Prüfungen, kein Telegram, und
Discord trennte mit „heartbeat blocked".

`_write_restream_overlay()` schreibt bis zu **vierzehn** Textdateien, jede mit
`open` + `write` + `os.replace`. Das lief **synchron auf dem Event-Loop**, rund
einmal pro Sekunde, aus dem `-progress`-Strom von ffmpeg heraus. Im
Normalbetrieb kostet das Bruchteile einer Millisekunde. Lief daneben aber ein
685-MB-Upload nach Telegram, schrieb ffmpeg Aufnahmen und lief der Restream,
blockierte `os.replace` zehnfach Sekunden. **Neunzehn von fünfundzwanzig
Stack-Abzügen des Wächters zeigten genau diesen Aufruf.**

Der Sekundentakt läuft jetzt über `asyncio.to_thread`, mit einem
**modul-globalen** Wächter (nicht als Objekt-Attribut, CLAUDE.md): dauert ein
Schreibvorgang länger als der Takt, wird der nächste übersprungen statt
aufgestaut. Der Anlauf-Aufruf bleibt synchron — die Dateien müssen existieren,
bevor `drawtext` sie öffnet.

Zwei weitere Abzüge zeigten `try_acquire_recording_lock` → `db_conn().__exit__`
→ `close()`. Auch der läuft jetzt neben dem Loop. Der Anspruch bleibt atomar:
er steckt im einen `UPDATE … WHERE recording=0`, nicht darin, dass der Aufruf
auf dem Loop läuft.

### Geändert — die lesenden Auskunfts-Routen als Blueprint (v4.1 W26)

Fünfundzwanzig kleine Routen, die einzeln keinen eigenen Blueprint
rechtfertigen: `/api/top`, `/api/pulse`, `/api/search`, `/api/version`,
`/api/heatmap/*`, `/api/shield/stats`, `/api/loyalty/leaderboard` und weitere.

Die Klammer ist streng und wird **geprüft**: sie antworten nur. Keine Route
dort startet, stoppt, löscht oder speichert etwas. `/api/annotations` (DELETE)
und `/api/highlights/config` (POST) liegen benachbart und sind deshalb
ausdrücklich **nicht** mitgewandert — ein Vertrag lässt keinen schreibenden
Pfad in diesen Blueprint. Ohne ihn wäre die Klammer eine Behauptung im
Docstring statt einer Regel.

Vier Funktionen sind nach `nc/` gelöst statt kopiert: `nc/suche.py`,
`nc/outcomes.py` (mitsamt der Zuordnung Ausgang → Klartext), `nc/bandbreite.py`
und die Speicher-Vorhersage in `nc/storage.py` — „wann ist die Platte voll"
steht jetzt neben „wie viel Platz ist da". `get_all_checks` ging nach
`nc/recdb.py`.

Die Schalter `LOYALTY_ENABLED` und die drei `COMMUNITY_*` liegen jetzt bei
ihren Fachmodulen statt im Monolithen — als Funktionen, nicht als Konstanten.

Der Radar-Zustand der Highlights ist ein **Register** in `nc/highlights.py`
geworden, kein Haken: das ist geteilter Zustand, keine Fähigkeit. Und Register
statt Alias, weil `bot.py` den Namen mit `new_state()` neu bindet — ein Alias
zeigte für immer auf das leere Anfangs-Dict, und das Panel meldete dauerhaft
null Treffer, ohne Fehler und ohne Logzeile.

`bot.py` fällt von 26.805 auf **26.425 Zeilen**, die eigenen Routen von 67 auf
**42**. Katalog: 901 → **906** Einträge. Weiterhin **null neue
Kontext-Einträge** — 24 von vertraglich 25 Plätzen.

### Behoben — der Adress-Cache wuchs bei Angriffswellen unbegrenzt (v4.1 W25)

Für die Geodaten der Abwehr-Karte gab es eine Obergrenze von 5000 Einträgen
und einen Helfer, der sie durchsetzt. Zwei Aufrufer benutzten ihn — **einer
nicht**: die Geo-Auflösung der Abwehr schrieb

```python
with _PROXY_GEO_LOCK:
    _PROXY_GEO_CACHE[ip] = g
```

direkt unter der Sperre und ging damit an der Verdrängung vorbei. Bei einer
Angriffswelle mit vielen verschiedenen Adressen wuchs der Cache unbegrenzt.
Kein Fehler, keine Logzeile — nur Speicher, der nicht mehr zurückkommt. Der
Befund kam beim Verschieben zutage, nicht beim Suchen.

Behoben wird er **strukturell**: `nc/geocache.py` hat genau einen Schreibweg
(`put()`), und der setzt die Grenze durch. Es gibt keinen zweiten Weg mehr, an
dem man vorbeikommen könnte; der Cache selbst ist nicht Teil der öffentlichen
Fläche. Ein Vertrag prüft beides.

### Geändert — Abwehr-Routen als Blueprint (v4.1 W25)

`/api/defense/overview`, `/crowdsec`, `/fail2ban` und `/attacks` liegen in
`nc/routes/abwehr.py`. Sie zeigen nur; keine davon sperrt oder entsperrt.

`nc/defensecfg.py` trägt den Serverstandort und die vier LAPI-Angaben.
**Der Bouncer-Schlüssel kommt nur aus `bouncer_key()`**, das ausschliesslich
der LAPI-Aufruf benutzt; für Anzeige und Diagnose gibt es `bouncer_gesetzt()`
— ein bool. Dieselbe Trennung wie bei den Stream-Keys (W22) und den
S3-Zugangsdaten (W24). Dass *kein* Schlüssel gesetzt ist, darf die Anzeige
sehr wohl sagen: es erklärt dem Betreiber, warum der sudo-Weg über `cscli`
genommen wird.

Der letzte Fehlgrund der Geo-Auflösung ist ein **Register**, kein Alias: eine
Zeichenkette ist unteilbar, und der Monolith band den Namen früher mit
`global` neu — ein Alias hätte danach für immer auf den alten leeren Wert
gezeigt.

**Fehlt der Haken in den Monolithen, antworten alle vier Routen 503** statt
0 Sperren und 0 Angriffe zu melden. Bei einer Sicherheitsanzeige ist „alles
ruhig" die gefährlichste aller falschen Antworten — sie sieht aus wie ein
gutes Ergebnis.

Ein Vertrag aus W23 (`test_v40_w23_crowdsec_panel`) ist **mitgewandert, nicht
gelöscht**: was er zusichert, gilt unverändert, nur seine Fundstelle hat sich
geändert. Er prüft jetzt zusätzlich, dass die Diagnose den Schlüssel nicht
herausgibt.

**Null neue Kontext-Einträge**, weiterhin 24 von vertraglich 25 Plätzen.

### Geändert — Wartungs-Routen als Blueprint, Löschpfade gehärtet (v4.1 W24)

Zehn Routen mit einer Klammer: `/api/storage`, `/api/retention`, `/api/backup`
und `/api/auto-archive-rules` halten den Bestand in Ordnung. Drei von ihnen
**löschen oder kopieren** — die gefährlichste Gruppe dieser Zerlegung, und
deshalb die, bei der eine Kopie am teuersten gewesen wäre.

`_retention_scan`, `cleanup_old_recordings`, `get_storage_stats` und die vier
Archivregel-Funktionen hatten im Monolithen je zwei Aufrufer: eine Dauerschleife
und eine Route. Beim Herauslösen der Routen wären daraus Kopien geworden. Eine
Kopie einer löschenden Funktion läuft irgendwann auseinander, und man merkt es
an der falschen Stelle. Stattdessen sind sie nach `nc/` gewandert
(`nc/retention.py`, `nc/storage.py`, `nc/archiverules.py`); der Monolith ruft
jetzt dieselbe Funktion auf wie der Blueprint.

Die Härtung von `retention.scan()` — gelöscht wird ausschliesslich, was per
`os.path.abspath` nachweislich **innerhalb** des Aufnahme-Verzeichnisses liegt
— ist mitgewandert und hat jetzt einen eigenen Vertrag. Ohne sie wäre aus einer
Aufräumfunktion ein Löschwerkzeug für das ganze Dateisystem geworden, sobald
ein `filepath` in der Datenbank mit `../` beginnt.

`nc/backupcfg.py` trägt die fünfzehn .env-Werte, jeden Namen wörtlich in einem
`os.getenv(...)`. **Die S3-Zugangsdaten gibt nur `s3_zugang()` heraus**, das
ausschliesslich der boto3-Client aufruft; für Anzeige und Diagnose gibt es
`s3_konfiguriert()` — ein bool. Dieselbe Trennung wie bei den Stream-Keys in
W22, und aus demselben Grund: wer einen Bucket-Schlüssel in eine API-Antwort
schreibt, verschenkt den Bucket.

**Null neue Kontext-Einträge**, weiterhin 24 von vertraglich 25 Plätzen.

### Behoben — „Sicherung gestartet", während nichts sicherte (v4.1 W24)

`threading.Thread(target=None)` startet klaglos und tut nichts.
`/api/backup/system` hätte damit `started: true` gemeldet, ohne dass eine
Sicherung läuft — genau die stille Sorte Fehler, die CLAUDE.md als Hauptfeind
benennt. Fehlt der Haken in den Monolithen, antwortet die Route jetzt 503 und
sagt warum. Ein Vertrag prüft beide Backup-Routen darauf.

Acht Benutzertexte des neuen Blueprints laufen an der Quelle durch `t(...)`;
drei englische Quelltexte (`insert failed`, `name, condition, action required`,
`days >= 1`) sind deutsch formuliert statt als Identitäts-Übersetzung in den
Katalog geschoben — der deutsche String ist der Schlüssel. Katalog: 891 →
**899**.

### Behoben — verkettete Toast-Meldungen blieben deutsch (v4.1 W23)

`toast()` erzeugt einen DOM-Knoten, den der Übersetzer sieht — **aber nur, wenn
der ganze Text ein Katalogschlüssel ist.** Bei

```js
toast('Aufnahme @'+u+' gestartet')
```

heißt der Knoten „Aufnahme @helge_72 gestartet"; ein Eintrag für `Aufnahme @`
trifft dort nie. **28 solcher Einträge standen bereits im Katalog** und zählten
als übersetzt, ohne je zu greifen — dieselbe stille Buchhaltung wie bei den
nativen Dialogen in W21, nur an anderer Stelle.

89 Literale in verketteten Aufrufen laufen jetzt durch `T()`. Ternäre Zweige
(`d.ok?'Gespeichert':'Fehler'`) sind unberührt geblieben: sie sind bereits
vollständige Knoten.

**Ein Fehler im ersten Anlauf, festgehalten weil er teuer gewesen wäre:** das
Skript umschloss auch das *zweite* Argument — `toast(msg, 'err')`. Das ist die
CSS-Klasse, kein Text; ein Katalogeintrag dafür hätte die Fehlerfarbe zerstört.
Jetzt wird nur das erste Argument angefasst, und ein Vertrag prüft, dass
`T('err')` nirgends steht.

Fünf englische Bruchstücke in deutschen Meldungen (`done`, `matched`,
`MOVED TO TRASH //`, `QUALITY //`, `dupes)`) sind deutsch formuliert statt mit
Identitäts-Übersetzungen in den Katalog geschoben. Katalog: 829 → **891**.

### Geändert — die Beobachtungs-Routen als Blueprint (v4.1 W23)

Vier kleine Gruppen in **einem** Blueprint: `/metrics`, `/api/backoff-watch`,
`/api/stream` und `/api/profile` — acht Routen, **null neue
`nc.ctx`-Einträge**. Einzeln rechtfertigt keine davon eine eigene Datei;
zusammen haben sie eine klare Klammer: **sie beobachten, sie steuern nichts.**
Ein Vertrag prüft das per AST — keine schreibende Methode, kein `DELETE`.

Gelöst wurde dafür:

* Die drei Wächter-Zähler liegen jetzt beieinander in `nc/brainstate.py`. Sie
  beantworten dieselbe Frage („warum startet der nicht neu?") und wurden
  vorher an drei Stellen im Monolithen gepflegt.
* Die Zuschauer-Stichproben in `nc/channels.py`, mit `maxlen` — ohne die wäre
  das ein Leck, das erst nach Tagen auffällt.
* **`nc/tiktokheaders.py`** trägt den Browser-Fingerabdruck für TikTok-Abrufe.
  Kein Geheimnis, aber auch keine Kosmetik: ohne plausible Kopfzeilen liefert
  TikTok eine andere Seite aus, und der Auflöser findet keine Stream-URL. Das
  `Accept-Encoding` kommt weiterhin vom Bot, weil es davon abhängt, ob Brotli
  installiert ist.

`/metrics` liegt bewusst **nicht** unter `/api/` — ein Prometheus-Scraper sucht
es genau dort. Der generische Blueprint-Vertrag hat das prompt gemeldet; er
führt die Ausnahme jetzt ausdrücklich, damit ein versehentlich gesetzter
`url_prefix` trotzdem auffliegt.

`.env.example` 499 → **500** (`RECORDINGS_DIR` wurde durch den Umzug erstmals
sichtbar).

`bot.py` 27.624 → **27.218** Zeilen, Blueprints 30 → 31, eigene Routen im
Monolithen 89 → **81**.

### Geändert — `/api/restream` als Blueprint, Sendeziele mit einer Parse-Regel (v4.1 W22)

Die letzte große Gruppe im Monolithen: **16 Routen**, und **null neue
`nc.ctx`-Einträge**. Roh wären es **38** gewesen. Zwei neue Module:

* **`nc/restreamcfg.py`** trägt die drei Sendeziele, die Parameter der
  Sendeprüfung, den Stall-Zeitgeber und die beiden öffentlichen Links. Es liest
  bei **jedem Aufruf**, nicht als Modul-Konstante. Die 16 Konstanten in `bot.py`
  kommen jetzt aus demselben Modul — es gibt genau **eine** Parse-Regel für
  Vorgaben, Leerzeichen und Wahrheitswerte statt zweier, die auseinanderlaufen
  können.
* **`nc/restreamstate.py`** trägt die sieben Zustands-Container als Aliase,
  dazu **Manager und Wächter als Register**: beide entstehen im Monolithen
  erst weit unten in der Datei, ein Alias wäre für immer `None` und jede
  Steuerroute meldete „kein Manager", während er läuft.

**Stream-Keys sind Geheimnisse.** Für Anzeige und Diagnose gibt es
`key_gesetzt(name)` — ein bool, kein Wert. Nur `ziel(name)` gibt einen Key
heraus, und die Funktion heißt deshalb bewusst nicht wie ein Getter. Ein
Vertrag verbietet jeden Key in einer API-Antwort.

**Zwei Fehler, die das eigene Werkzeug gefangen hat** — beide wären still
durchgegangen:

1. Die `.env`-Namen waren zuerst **dynamisch** gebaut
   (`"%s_INGEST_URL" % ziel.upper()`). `tools/gen_env_example.py` findet solche
   Namen nicht: **vierzehn Variablen** fielen aus der Vorlage. Jetzt steht jeder
   Name wörtlich in einem `os.getenv(...)` — auch damit ein `grep` ihn trifft,
   was in diesem Bestand die halbe Arbeitsgrundlage ist.
2. Danach fehlte noch `TWITCH_INGEST_URL`: der Aufruf war **umbrochen**, und
   der Erzeuger suchte zeilenweise. Er setzt die kommentarfreien Zeilen jetzt
   zusammen, bevor er sucht. Dabei kamen **zwei Variablen zum Vorschein**, die
   schon vorher still gefehlt hatten (`AI_SYSTEM_PROMPT`,
   `RESTREAM_OVERLAY_HTML_FALLBACK_SIZE`). Vorlage: 497 → **499**.

Die 525 Zeilen sind **mechanisch** übertragen worden, token-basiert statt per
`str.replace`: die Konstantennamen stehen auch in deutschen Fehlertexten
(`"YOUTUBE_ENABLED=0 (in .env aktivieren)"`), und blindes Ersetzen zerlegte
die. Der `ast.parse()`-Schutz vor dem Schreiben fing genau das beim ersten
Lauf.

Sechs Vertrags-Anker sind mitgewandert, keiner gelöscht. Der
Übersetzungs-Vertrag aus W20 griff beim neuen Blueprint sofort und meldete zehn
nicht umschlossene Texte — genau wofür er gebaut wurde.

`bot.py` 28.133 → **27.624** Zeilen (erstmals unter 28.000), Blueprints 29 →
30, eigene Routen im Monolithen 105 → **89**.

### Behoben — die 35 nativen Dialoge waren dauerhaft deutsch (v4.1 W21)

`confirm()` und `prompt()` öffnet der **Browser selbst**. Der
MutationObserver in `/api/i18n/uebersetzer.js` beobachtet `document.body` —
ein natives Dialogfenster ist kein DOM-Knoten und taucht dort nie auf. Alle 35
Rückfragen des Dashboards blieben deshalb Deutsch, egal welche Sprache
eingestellt war.

Schlimmer als die fehlende Übersetzung war die **stille Buchhaltung**: 26 der
Texte hatten längst einen Katalogeintrag. Der zählte als übersetzt und traf
nie — genau die tote Zeile, die die Abdeckungszahl zur Lüge macht.

Übersetzt werden kann so ein Text nur **vor** dem Aufruf, mit dem ohnehin
exportierten `window.T()`. Alle 35 Stellen laufen jetzt darüber. Sätze, die
aus Bruchstücken zusammengeklebt waren, sind dabei umgebaut worden — statt
`'Restream #'+rid+' (@'+user+') stoppen?'` steht dort jetzt ein **ganzer**
übersetzbarer Satz und die Details darunter. Elf Bruchstück-Einträge sind
damit aus dem Katalog verschwunden, 38 vollständige Sätze dazugekommen.

Der Extraktor sammelt `T("...")` jetzt **ausdrücklich** ein, wie schon `t(...)`
in den Blueprints. Ohne das fiele ein einzelnes Wort wie `T('Tage')` durch die
Bruchstück-Regel — obwohl es ein vollständiger Baustein ist, den der Aufrufer
selbst zusammensetzt. Katalog: 805 → **825 Einträge**, 0 fehlend, 0 verwaist.

### Geändert — `/api/brain` als Blueprint, zwei Register (v4.1 W21)

Sechs Routen aus dem Monolithen, **null neue `nc.ctx`-Einträge**. Roh wären es
siebzehn gewesen. **`nc/brainstate.py`** trägt jetzt die Ringpuffer der
Knoten-Historie, das Übergangs-Gedächtnis, den Brücken-Zustand, die
Sende-Bremse des Dashboard-Chats und den Wächter-Zustand des Check-Loops.

Zwei davon **müssen** Register sein und können keine Aliase werden:

* **`STALLS`** war eine ganze Zahl (`_LOOP_STALL_COUNT += 1` unter `global`).
  Eine Zahl lässt sich nicht teilen — ein Alias wäre eine Kopie, die für immer
  auf 0 steht, und `/api/brain/health` meldete „keine Stalls", während der Loop
  klemmt. Genau die stille Fehlanzeige, gegen die es die Zahl überhaupt gibt.
* **`PROXY`** entsteht im Monolithen erst weit unten in der Datei. Dort stand
  dafür `globals().get("PROXY_ROUTER")` — im Blueprint wäre `globals()` dessen
  eigener Namensraum, und das Panel meldete den Proxy für immer als „idle".

Die 210 Zeilen von `api_brain` sind **mechanisch** übertragen worden, nicht
abgetippt: das Skript ersetzt nur Namen und meldet, was danach noch nach
Monolith aussieht. Es fand prompt zwei Reste (`_AI_DASHBOARD_LOCK`,
`_AI_DASHBOARD_RATE`), die beim Abtippen niemandem aufgefallen wären.

Zwei Vertrags-Anker sind mitgewandert, keiner gelöscht. Ein neuer Vertrag
verbietet `globals()` im Blueprint — geprüft per AST, weil die *Erklärung*
dazu völlig zu Recht im Docstring steht und kein Verstoß ist.

`bot.py` 28.467 → **28.133** Zeilen, Blueprints 28 → 29, eigene Routen im
Monolithen 111 → **105**.

### Geändert — jede Route übersetzt an der Quelle (v4.1 W20)

W19 hat den Extraktor bis in `nc/routes/` gebracht, aber nur zwei Blueprints
umgestellt. Die übrigen **21 antworteten weiter deutsch** — 136 Stellen. Von
Hand wären das über hundert Einzeländerungen gewesen, und die *eine*
vergessene fällt niemandem auf: eine deutsch gebliebene Zeile sieht aus wie
eine, die es noch nicht gibt.

Deshalb **`tools/i18n_wrap.py`**: es findet die Benutzertexte per AST und
schreibt `t(...)` textuell an die Stelle — nicht per `ast.unparse`, das die
ganze Datei umformatiert hätte. `--check` ist der Vertrag, `--write` die
Arbeit. f-Strings bleiben draußen (ihr Wert steht erst zur Laufzeit fest und
wäre als Schlüssel wertlos), mehrzeilige Literale werden gemeldet statt
geraten — die 14 sind von Hand umschlossen.

Eine Falle, die das Werkzeug beim ersten Lauf sofort aufdeckte: **`col_offset`
im AST ist ein UTF-8-Byte-Offset, kein Zeichen-Offset.** In einer Zeile mit
Umlaut vor dem Literal verrutscht ein Zeichen-Slice um genau die Zahl der
Mehrbytes und schreibt kaputten Code. Dass es auffiel, lag nur am `ast.parse()`
vor dem Schreiben; ohne das wären still defekte Blueprints entstanden. Ein
Vertrag hält jetzt beides fest.

**Vierzehn Fehlertexte waren bereits englisch** (`file not found`,
`recording not found`, …) — in einer deutschen API. Die sind jetzt deutsch
formuliert, statt den Katalog mit Identitäts-Übersetzungen aufzuweichen: sein
Vertrag lautet, dass der Schlüssel deutsch ist (`nc/i18n.py`), und
`"file not found" → "file not found"` sähe in der Abdeckungszahl aus wie
geleistete Arbeit, wo keine war. Vorher geprüft, dass die Oberfläche keine
dieser Zeichenketten vergleicht.

Katalog: 692 → **805 Einträge über 36 Dateien**, 0 fehlend, 0 verwaist. Die
drei i18n-Prüfungen laufen jetzt auch in CI — bis hierher waren sie nur über
die Verträge gedeckt, was „ein Vertrag ist rot" meldet statt „dieser Text
fehlt".

### Geändert — `/api/overlay` und `/api/audio` als Blueprint, ein Einnahmen-Gate (v4.1 W20)

Fünf Routen aus dem Monolithen, **null neue `nc.ctx`-Einträge**. Gelöst wurde:

* **`nc/revenue.py`** trägt das Einnahmen-Gate (B120) und die
  Overlay-Plattformen. Es stand als Konstantenpaar im Monolithen, und
  `nc/routes/money.py` spiegelte es zusätzlich über einen `ctx.cfg`-Eintrag —
  **zwei Orte für eine Wahrheit, aus der ein Drift wird.** Jetzt eine Quelle,
  und der `cfg`-Eintrag ist weg. TikTok gehört nicht zu den Einnahmequellen
  (Gifts gehen an den getrackten Streamer), wohl aber zu den
  Overlay-Plattformen: Follows von dort sind Reichweite, kein Geld.
* **`nc/audiocue.py`** trägt Signalton- und Ducking-Konfiguration; die
  `.env`-Vorgaben reicht der Bot hinein, statt sie im Modul einzufrieren.
* **`nc/channels.RESTREAM_TTS`** und **`nc/azraelstate.OVERLAY_SESSION`** sind
  Aliase. Beim Testton ist das der ganze Punkt: er muss in den **Live-Mix**.
  Eine Kopie hieße „0 Warteschlangen" bei laufendem Restream — eine
  Fehlanzeige, die wie ein kaputter Ton aussieht.

`_overlay_push` bleibt im Bot (zwölf weitere Aufrufer dort) und kommt als
Haken, wie in W19.

**Vier Vertrags-Anker sind mitgewandert, keiner gelöscht** — die Zusicherungen
gelten unverändert, nur stehen sie jetzt in `nc/`: der Session-Filter des
Overlays, die Einnahmen-Positivliste, die Audio-Laufzeitkonfig und der
`normalize_audio`-Delegationsanker.

`bot.py` 28.640 → **28.467** Zeilen, Blueprints 26 → 28, eigene Routen im
Monolithen 116 → **111**.

**Offen, nicht angefasst:** `nc/ledger.PLATFORMS` behauptet im Kommentar,
deckungsgleich mit den Einnahmequellen zu sein — ist es nicht (`sonstige`
gegen `manuell`). Das sind Buchungskategorien für die Steuer gegen
Einnahmequellen; sie *sollen* sich unterscheiden, nur der Kommentar ist
falsch. Geldcode wird nicht nebenbei angefasst (CLAUDE.md).

### Geändert — `/api/azrael` als Blueprint, drei Schichten gelöst (v4.1 W19)

Die größte Routengruppe, die noch im Monolithen stand: **18 Routen**, und
**null neue `nc.ctx`-Einträge**. Roh hätte sie 35 gekostet — bei 24 von
vertraglich 25 belegten Plätzen war das kein knapper Fall, sondern ein
unmöglicher. Also wieder erst die Schichten, dann die Routen (W117):

* **`nc/azraelstate.py`** trägt die acht Zustands-Container:
  Overlay-Konfiguration, Stream-Kontext, letzte Reaktion, KI-Aufruf-Budget,
  Pause-Schalter der Reaction-Engine, Live-Transkript, laufende Worker und die
  Agenten-Rollen — dazu die Personas auf Platte. Alles **Aliase**: `bot.py`
  bindet keinen dieser Namen je neu, es verändert sie nur an Ort und Stelle.
  Ein Vertrag prüft per AST, dass das so bleibt: bei nur einer Neubindung
  zeigte der Alias danach auf eine tote Kopie, und das Dashboard meldete einen
  eingefrorenen Stand — ohne Fehler, ohne Logzeile.
* **`nc/piper_voices.py`** bekam Suchorte, Scannen samt Cache und
  Verfügbarkeitsprüfung dazu. Der Cache wird beim Wechsel der Suchorte
  verworfen; sonst zeigte `/api/azrael/voices` die Stimmen des alten
  Verzeichnisses und der Betreiber suchte am falschen Ort.
* **`nc/whispercfg.py`** hält Modellname **und** geladenes Modell in *einem*
  Register. Der Laufzeit-Umschalter tat das im Monolithen mit `global`; in
  einem Blueprint wäre das dessen eigener Namensraum gewesen — die Route hätte
  Erfolg gemeldet und der nächste Transkript-Lauf das alte Modell benutzt. Und
  beides gehört zusammen: wer nur den Namen ändert und das geladene Objekt
  stehen lässt, transkribiert weiter mit dem alten Modell und sieht den neuen
  Namen im Dashboard. Das wäre schlimmer als gar kein Umschalten.

Drei Dinge kann nur der Bot — sprechen (`_piper_say`), den zentralen KI-Aufruf
fahren (`azrael_chat`) und sagen, was NIGHTCRAWLER gerade tut
(`_azrael_live_state`). Sie kommen als **Haken** aus den Registern, nach dem
Muster von `TWITCH_SEND`/`YT_SEND`. Das ist Kopplung; sie steht sichtbar in
`nc/azraelstate.py` statt versteckt im Kontext, dessen 25 Plätze eine andere
Frage beantworten.

`bot.py` 28.935 → **28.640** Zeilen, Blueprints 25 → 26, eigene Routen im
Monolithen 134 → **116**.

### Geändert — der Übersetzungskatalog reicht in die Blueprints (v4.1 W19)

Der Extraktor kannte nur `bot.py`. Bei 243 Routen in `nc/routes/` hieß das:
**die Fehlertexte der halben API waren außer Reichweite** — und die
Abdeckungszahl zeigte es nicht, weil sie nur zählt, was sie sieht. Jede
Blueprint-Welle hat diese Lücke bisher stillschweigend vergrößert.

Eingesammelt wird aus `nc/routes/*.py` **nur, was ausdrücklich in `t(...)`
steht**. Das ist der Unterschied zur Heuristik in den HTML-Dateien und der
Grund, warum es hier keine toten Einträge geben kann: ein API-Fehlertext
erreicht das DOM meist verkettet (`"Fehler: " + error`), ein Katalogeintrag
für den bloßen Text träfe dort nie. Er trifft, weil im Blueprint schon
übersetzt wurde — an der Quelle, nicht im Browser. Dieselbe Überlegung wie bei
`_safe_send()` (W7) und der Shell-Übersetzung (W17).

`nc/routes/azrael.py` und `nc/routes/kickmod.py` sind entsprechend umgestellt;
16 Einträge kamen dazu. Katalog: 676 → **692 Einträge über 34 Dateien**, 0
fehlend, 0 verwaist.

### Behoben — TikTok löst keine Toxizitäts-Warnung mehr aus (v4.1 W18)

Der Betreiber bekam Meldungen der Form „Chat-Toxizität steigt: N
Moderations-Aktionen letzte Stunde" für einen Chat, den der Bot **gar nicht
moderiert**. Ursache: der Schnappschuss für den `ToxicityAgent` zählte jede
Zeile aus `kick_mod_log` — dort liegt aber deutlich mehr als Moderation.
AZRAELs Live-Reaktion auf einen TikTok-Stream (`kind="reaction"`, im
Sekundentakt), der Highlight-Radar, die eigenen Chat-Nachrichten des Bots und
gelernte Schimpfwort-Kandidaten zählten alle mit. Ein einziger aktiver
Live-React-Worker schrieb mühelos die sechs Zeilen, ab denen `spike_min` greift.

Die Regel steht jetzt in **`nc/modstats.py`** und beantwortet zwei Fragen
getrennt: Ist die Zeile ein Durchgreifen gegen einen Nutzer? Und auf welcher
Plattform? Gezählt wird nur, was beides beantwortet und in der Auswahl des
Betreibers liegt — standardmäßig Kick, Twitch und YouTube. Alle elf
Moderations-Aufrufe tragen ihre Plattform jetzt im `meta`; `sentinel-shield`
schreibt aus dem Kick-Moderator **und** aus dem Discord-Automod und war über
den Aktor allein nicht unterscheidbar. TikTok steht nicht in `PLATTFORMEN` und
lässt sich damit auch per `MOD_TREND_PLATTFORMEN` nicht zuschalten — dieselbe
Trennlinie wie bei `REVENUE_PLATFORMS`.

Wichtig für den Trend: die **Vorstunde läuft durch dieselbe Regel**. Wäre nur
die aktuelle Stunde gefiltert, wäre jede TikTok-Sitzung in der Vorstunde eine
gemeldete „Beruhigung" und jedes Sitzungsende eine gemeldete „Welle". Und die
Meldung nennt die Plattformen jetzt mit (`[kick 7, twitch 2]`) — vorher wusste
der Betreiber zwar, *dass* es kracht, aber nicht *wo*.

### Geändert — `/api/kickmod` als Blueprint, zwei Schichten gelöst (v4.1 W18)

Neun Routen aus dem Monolithen, **null neue `nc.ctx`-Einträge** (der Kontext
steht bei 24 von vertraglich 25). Möglich durch dieselbe Reihenfolge wie
W117 — erst die Datenschicht lösen, dann sind die Routen umsonst:

* **`nc/badwords.py`** trägt Bannwortliste, Lern-Warteschlange und die
  LDNOOBW-Basisliste. Geschrieben wird über eine Zwischendatei und
  `os.replace`: ein Absturz mitten im Schreiben darf die Bannwortliste nicht
  halbieren, danach moderierte der Bot still schwächer. Ein Netzfehler beim
  Holen der Basisliste fällt auf die eingebaute Liste zurück, nie auf leer.
* **`nc/channels.RESTREAM_ACTIVE`** ist ein Register für den primären Restream.
  Im Monolithen stand dafür `globals()["_RESTREAM_ACTIVE"] = {…}` — in einem
  Blueprint wäre `globals()` der Namensraum des Blueprints, und das
  SENTINEL-Panel meldete TikTok für immer als „nicht verbunden", während der
  Listener läuft. Genau die stille Fehlanzeige aus W116.

Die sieben `.env`-Werte liest der Blueprint bei **jedem Aufruf** statt sie als
Modul-Konstante einzufrieren — die Regel aus `CLAUDE.md`, weil `.env` teils
erst nach den ersten Imports geladen wird.

`bot.py` 29.112 → 28.935 Zeilen, Blueprints 24 → 25, eigene Routen im
Monolithen 143 → 134.

### Geändert — der Übersetzungskatalog reicht bis zum Tabellenkopf (v4.1 W18)

`<th>Datei</th>` ist im DOM ein vollständiger Textknoten, fiel aber aus dem
Katalog, weil er „weniger als zwei Wörter" hat. Diese Regel gibt es gegen
Bruchstücke um Platzhalter herum (`Für @${user}` steht im DOM nie für sich) —
sie traf aber auch die Tabellenköpfe. Ergebnis: der Kopf einer Tabelle blieb
deutsch, während ihr Inhalt übersetzt war.

`tools/i18n_extract.py` unterscheidet jetzt **Tag-Grenzen von
Platzhalter-Grenzen**: an einem Tag endet ein Textknoten, an einem Platzhalter
verschmilzt er mit dem eingesetzten Wert. Belegt sein muss es — ein blankes
Literal wie `'läuft'` kann genauso gut ein Vergleichswert oder ein
Objektschlüssel sein, und ein Eintrag dafür wäre **tot**: er zählte als
übersetzt, während die Stelle deutsch bleibt, und verdeckte damit genau das,
was die Abdeckungszahl sichtbar machen soll. 41 solcher Kandidaten wurden
deshalb abgelehnt; **29** echte Tabellenköpfe und Knopfbeschriftungen sind
dazugekommen (`Datei`, `Datum`, `Grund`, `Größe`, `Quelle`, `Zeit`, `Gebühr`,
`Priorität`, `Lautstärke`, `Tonhöhe` …). Katalog: 647 → **676 Einträge, 0
fehlend, 0 verwaist**.

Offen bleibt bewusst: Sätze, die per String-Verkettung um einen Platzhalter
gebaut werden (`'GESTÖRT · ' + phase`). Die brauchen ein `T()` an der Quelle
und kommen in einer eigenen Welle — ein Katalogeintrag dafür wäre tot.

### Geändert — Werkzeuge, Installer, MOTD, Doku und Website (v4.1 W17)

Fünf Befunde des Betreibers, in einer Welle.

**Die Werkzeuge sprechen jetzt Englisch — an der Senke übersetzt.**
`tools/lib/i18n.sh` bringt dieselbe Regel wie `nc/i18n.py`: der deutsche Text
ist der Schlüssel, eine fehlende Zeile bleibt Deutsch. Entscheidend ist, **wo**
übersetzt wird: `info`/`gut`/`warn`/`fehler`/`erklaere`/`frage_ja`/`frage_text`
laufen durch `t()`, damit sind alle **141** Ausgabestellen von `installer.sh`
und `motd.sh` erfasst, ohne eine einzige davon anzufassen. Jede einzeln zu
umschliessen wäre ein Diff von 250 Zeilen gewesen, bei dem die vergessene
Stelle unsichtbar bleibt — dieselbe Überlegung wie bei `_safe_send()` in W7.
Der Katalog `locales/tools.en.tsv` ist zu **100 %** gefüllt;
`tools/i18n_tools.py --check en` misst das und meldet **verwaiste** Einträge
als Fehler (ein Eintrag ohne Quelle heisst: der deutsche Text wurde geändert
und der Katalog nicht nachgezogen — ab da bliebe die Zeile für immer deutsch).

**Installer: Reverse-Proxy mit HTTPS.** Bisher endete er beim Dashboard auf
`127.0.0.1` und überliess den Rest der Anleitung — genau dort brach der
häufigste Weg ab: wer die Oberfläche von aussen wollte, öffnete den Port,
statt einen Proxy davorzusetzen. Neu: `nginx` + `certbot` +
`python3-certbot-nginx`, eine vollständige Server-Vorlage und das Zertifikat
per Let's Encrypt. Die drei `X-Forwarded-*`-Kopfzeilen sind dabei nicht Deko:
ohne `X-Forwarded-Proto` baut `nc/oauthredirect.py` ein `http://` und Google
lehnt den OAuth-Rückruf ab, **bevor** die Kontoauswahl erscheint (W121).
`PUBLIC_BASE_URL` und `TRUSTED_PROXIES` werden gleich mitgesetzt.

**MOTD: räumt jetzt wirklich auf.** `silence_defaults` kannte eine **feste
Liste** von Ubuntu-Stücken — aber nicht das, was Hoster, Images und
Distributionen sonst einhängen. Nach `--install` stand das alles weiter da.
Jetzt wird **alles** in `/etc/update-motd.d/` ausser dem eigenen Stück
gedämpft, jede Datei namentlich vermerkt, und `--uninstall` holt exakt sie
zurück. Dazu die **statische** `/etc/motd`, die gar nicht über `run-parts`
läuft und deshalb bisher unberührt stehen blieb: sie wird beiseitegelegt und
kommt zurück — ausser jemand hat seither neu hineingeschrieben, dann bleibt
die Sicherung liegen statt fremden Inhalt zu überbügeln. Ausserdem gehört die
MOTD jetzt zur Standard-Einrichtung: im Express- und im unbeaufsichtigten Lauf
kommentarlos an, statt ganz auszufallen.

**MOTD-Farbe: `always` statt `auto`.** `auto` wählte ohne `COLORTERM` die
256-Farben-Palette — viele Handy-SSH-Apps melden aber nur `TERM=xterm` und
stellen 256er-Codes teils gar nicht dar. Der Betreiber sah dann eine graue
Wand statt der Ampel, für die die MOTD gebaut ist. `always` fällt bis auf die
**16 Basisfarben** durch, die wirklich jedes Terminal kann — nie auf farblos.

**Doku: der Versionsdrift ist jetzt maschinell gefangen.** Im deutschen README
stand `4.0 — „Restream Control Room"`, während `nc/version.py` und das
englische README längst bei `4.1 — „Öffentliche Stimme"` waren. Die
Zahlenprüfung in `ncpatch docs` konnte das nicht sehen: `4.0` ist keine
Einheit. Sie vergleicht jetzt Version und Codename gegen `nc/version.py`.
Dazu nachgezogen: `89 Fachmodule` → 95 im Verzeichnisbaum, `283 Routen` → 359
im Installer-Text.

**Website: Material statt flacher Kästen.** Drei Befunde, in dieser Reihenfolge
behoben: (1) **alles** leuchtete — der eigene Grundsatz lautet „Leuchten ist
Signal, nicht Deko", tatsächlich hatten Überschriften, Zahlen, Knöpfe und
Kanten denselben Schimmer, womit er nichts mehr trug; (2) keine Tiefe — eine
Fläche, ein Rahmen, fertig; (3) kein Rhythmus — 76 px zwischen allen
Abschnitten und 15 px Schrift auf jedem Schirm. Jetzt: vier Ebenen, die
Bezel-Oberkante als das eine wiedererkennbare Detail (dasselbe Motiv wie im
Dashboard, in Phosphor statt Messing), eine fliessende Typo-Skala, ein
Farbverlauf im Logo statt des Glows (auf OLED war der ein Fleck), 56-px-Ziele
für Finger, ein ehrliches `prefers-reduced-motion` und ein Druck-Stylesheet.
Als **Schicht** am Ende des Stylesheets, an bestehenden Klassennamen — damit
ist der Diff lesbar und die Änderung in einem Zug rückrollbar.

Drei Verträge sind neu (373).

### Geändert — Discord als Blueprint (v4.1 W16)

`bot.py`: 29.306 → **29.112 Zeilen**. `nc/routes/` trägt jetzt 24 Blueprints
mit 216 Routen, der Monolith noch 143. `nc.ctx` bleibt bei **24 von 25**.

`/api/discord` kostete acht Kontext-Einträge. Neu `nc/discordstate.py` löst
Wochenstand (`state_get`), Invite (`invite`) und den Verbindungszustand heraus;
die drei `.env`-Werte gehen über `ctx.cfg`, das ein Dict ist und keinen Slot
kostet. Übrig bleibt `run_async` — das gab es schon. **Null neue Einträge.**

**Warum ein Modul für zwei so verschiedene Dinge** — das eine aus der
Datenbank, das andere aus dem Arbeitsspeicher: sie beantworten dieselbe Frage,
„wie steht es gerade um Discord?". Das Panel liest in einem Aufruf den
gespeicherten Wochenstand *und* den laufenden Verbindungszustand. Zwei Module
für eine Ansicht wären die schlechtere Grenze.

**Register für den Client, Alias für die Session — und das ist kein Zufall.**
`_DISCORD_CLIENT` wird vom Bot **neu gebunden** (bei jedem Reconnect und beim
Aufräumen); ein Alias zeigte danach auf den alten, geschlossenen Client, und
das Panel meldete „online", während nichts mehr durchging. Deshalb ein
Register, wie bei `KICK_MOD` in W9. `_DISCORD_SESSION` dagegen wird nur *in
place* verändert, nie neu gebunden — dort ist der Alias richtig und genügt.
Damit ist auch der letzte `globals()`-Zugriff aus dem Discord-Pfad
verschwunden.

`DISCORD_INVITE_URL` liest die Schicht jetzt bei jedem Aufruf statt als
Modul-Konstante — die Regel aus `CLAUDE.md`. Am Ergebnis ändert das nichts,
sobald der Flow einmal lief (der gespeicherte Wert schlägt die Variable
ohnehin); es hilft nur dem Fall „Betreiber trägt die Variable nach".

**`ruff` hat eine Dublette gefangen:** zwei der drei `.env`-Werte
(`DISCORD_GUILD_ID`, `DISCORD_WEBHOOK_URL`) standen bereits in `ctx.cfg`. Neu
ist nur `CLIP_HIGHLIGHT_STARS`.

Ein Vertrag ist neu, ein Anker gewandert (W35) — keiner gelöscht.

### Geändert — Chat und Co-Host als Blueprint (v4.1 W15)

`bot.py`: 29.442 → **29.306 Zeilen**. `nc/routes/` trägt jetzt 23 Blueprints
mit 210 Routen, der Monolith noch 149. `nc.ctx` bleibt bei **24 von 25**.

Beide Gruppen hängen an **geteiltem Zustand**, und genau daran entschied sich,
ob der Umzug richtig ist. Das ist hier besonders heikel, weil beide Routen
**Diagnose** sind: eine Kopie hätte sie „nicht verbunden" bzw. eine Bremse
melden lassen, die nie zieht — während beides läuft.

* `/api/chat` (2 Routen) liest die drei Sendewege aus `nc/channels.py`:
  `KICK_MOD` (seit W9 im Register), `TWITCH_SEND` und `YT_SEND`. Die vier
  `_KICK_MOD`-Zugriffe der Chat-Routen gehen jetzt über das Register — dieselbe
  Umstellung wie bei den Kick-Routen in W9.
* `/api/cohost` (2 Routen): Bremse (`STATE`) und Konfigurations-Leser
  (`config()`) sind nach `nc/cohost.py` gewandert, dorthin, wo `decide`,
  `snapshot` und `default_config` schon lagen. Ohne Injektion — `nc.cfgnorm`
  und `nc.cfgstore` sind ebenfalls bot-frei. Das Ergebnis ist das **zweite
  Blueprint überhaupt ohne jeden `nc.ctx`-Zugriff** (nach `evolution` in W3).

**Ein Vertrag hat sich selbst als zu grob erwiesen.** Die Prüfung „jeder
`cfg`-Schlüssel, den ein Blueprint liest, wird auch geliefert" suchte nach
jedem `cfg["x"]` — und traf damit auch ein **lokales** Dict, das die Route
selbst gebaut hat (`cfg = _cohost_cfg()`, dann `cfg["enabled"]`). Sie hätte
vier Schlüssel vom Bot verlangt, die es dort nie gab. Blueprints lesen den
Kontext ausnahmslos als `_c().cfg[...]`; der Ausdruck verlangt jetzt genau
diese Form.

Ein Vertrag ist neu, vier Anker sind gewandert (W24, W33, W41, W15) — keiner
gelöscht.

**Was liegen bleibt und warum.** `/api/audio` (2 Routen) sieht mit zwei
Einträgen gleich billig aus, ist es aber nicht: `_restream_tts` ist die
Laufzeit-Buchführung des TTS-Feeders (Threads, FIFOs, Queues, 26 Lesestellen),
und `_audio_cfg` hat keine natürliche Heimat in `nc/` — `nc/audio_cue.py` ist
bewusst reines DSP (nur `math`/`struct`). Dort etwas hineinzulegen wäre
Verschieben ohne Gewinn. Die Gruppe wartet auf die TTS-Schicht, nicht auf einen
Slot — derselbe Fall wie `/api/profile`.

### Behoben — totes Modell kostete jeden Umlauf, Watchdog zeigte falsch (v4.1 W14)

**Ein totes Modell wurde 26 Mal neu entdeckt.** Im `debug.log` steht 26 Mal
derselbe Satz: `Model 'gpt-4.1-nano-2025-04-14' is currently unavailable.`
B140 hatte schon dafür gesorgt, dass ein solcher 400 die Base nicht verbrennt —
die übrigen Modelle werden danach probiert. Was fehlte: sich das zu **merken**.
Jeder folgende Aufruf begann wieder mit dem toten Namen, verbrannte einen
Umlauf und schrieb eine Warnung. Auf dem Live-React-Pfad, dessen ganzes
Zeitbudget Sekunden beträgt, ist das kein Schönheitsfehler.

`nc/freeai.py` merkt sich jetzt pro **(Base, Modell)**, dass der Anbieter es
abgelehnt hat, und sortiert es für 15 Minuten ans Ende — nicht heraus. Sind
alle Modelle einer Base gesperrt, wird trotzdem probiert; dieselbe Haltung wie
bei `_eligible_bases`: lieber ein Versuch als sicheres Scheitern. Die Sperre
gilt pro Base, damit ein anderswo gesundes Modell nicht mitgesperrt wird.

**Der Watchdog schickte zum Audio-Tap, während die KI ausfiel.** 19 Mal stand
`Live-React @… seit Ns ohne einzige Reaktion — prüfe Audio-Tap/Chat` im Log,
alle 45 Sekunden neu. In Wahrheit scheiterte **jeder** Reaktionsversuch am
Backend (Claude `bad_request` → pollinations `auth` → llm7 400). Dieselbe Sorte
Fehler wie die Kick-Diagnose aus W10: eine Meldung, die auf eine Stelle zeigt,
die das Log gar nicht belastet.

Der Bot weiss es besser — `_react_warn` hinterlegt den Zeitpunkt der letzten
Backend-Klage. Liegt der frisch vor, nennt die Meldung das KI-Backend als
Ursache und sagt ausdrücklich, dass Audio-Tap und Chat es **nicht** sind;
schweigt das Backend, bleibt der alte Hinweis richtig und stehen. Ausserdem ist
der Zweig jetzt flankengesteuert wie der Loop-Wächter darüber: eine Meldung je
Stillstand, und eine Entwarnung, wenn wieder reagiert wird.

Drei Verträge sind neu.

### Behoben — AZRAELs Claude-Pfad sagte nicht, warum er scheitert (v4.1 W13)

Im `debug.log` vom 30.08. steht **26 Mal** „Reaction-AI Claude fehlgeschlagen
(bad_request) → Kette" — und kein einziges Mal, *was* am Request schlecht war.
Die API schickt diese Begründung bei jedem 400 mit; `chat_sync` las den Body
gar nicht erst:

```python
except urllib.error.HTTPError as e:
    return (None, _error_kind(e.code))     # der Grund ist hier weg
```

Bemerkenswert: `probe()` — der Dashboard-Test — liest denselben Body seit W70
vollständig aus. Der Weg, den der Betreiber im Alltag nutzt, war der stumme.
Genau der Fall aus CLAUDE.md: erst das `except` suchen, das den Grund frisst.

`fehlertext(e)` liegt jetzt einmal da und wird von **beiden** Wegen benutzt.
`chat_sync` meldet über einen `on_error(kind, detail, model)`-Rückruf; der
**Rückgabewert bleibt `(text, kind)`**, weil ein Dutzend Aufrufstellen
`err == "auth"` vergleicht und ein dritter Rückgabewert sie alle angefasst
hätte. Die Warnung nennt jetzt Modell und API-Text.

**Zwei deterministische 400er gleich mit erledigt.** `_split_messages` warf
leere **system**-Inhalte weg, liess leere **user/assistant**-Inhalte aber
durch — und die Messages-API weist einen leeren Textblock mit 400 ab, und zwar
den ganzen Request. Und bestand die Anfrage nur aus System-Text, ging sie mit
`messages: []` hinaus, was ebenfalls nur 400 werden kann; dieser Fall wird
jetzt gar nicht mehr gesendet, sondern heisst `kein_verlauf` statt sich als
`bad_request` zu tarnen.

Der Rückruf läuft im Thread von `chat_sync` — er schreibt nur, er loggt nicht;
ein Vertrag hält das fest.

Vier Verträge sind neu.

### Behoben — zwei Restreams auf einem Kick-Key (v4.1 W12)

Der Befund aus dem `debug.log` vom 30.08., und die Ursache der Abbruch-Serie
aus dem `error.log` desselben Tages. Sekunde für Sekunde:

```
09:23:42  #60 stirbt (rc=255). _monitor plant reconnect in 20s und nimmt #60
          dabei aus _procs — der Einzel-Slot sieht frei aus.
09:23:46  auto_start_due findet _procs leer, Single-Modus sagt „frei", → #6.
09:24:02  Der geplante Reconnect von #60 feuert — ohne noch einmal zu fragen.
```

Ab hier senden zwei Restreams auf **denselben Kick-Key**. Ein RTMP-Key nimmt
einen Publisher; jeder neue Verbindungsaufbau wirft den anderen raus. Beide
sterben abwechselnd, der Wiederanlauf baut beide neu auf. Das lief über
Stunden — im `error.log` als `Broken pipe`, `Input/output error` und sechs
Stillstands-Abschüsse für ein Ziel.

**Die Prüfung sass nur im Scheduler, nicht im Start.** `auto_start_due`
respektierte den Einzel-Modus vorbildlich; der Reconnect-Pfad in `_monitor`
kannte ihn gar nicht. Zwischen „reconnect in 20s" und dem Start liegt aber
genug Zeit, dass sich die Lage ändert — genau diese Lücke wurde benutzt. Die
Prüfung sitzt jetzt in `start()`, dem einen Punkt, durch den Scheduler,
Verify-Loop, Reconnect und Handstart gleichermassen gehen.

**Die dafür gebaute Warnung schwieg.** B141 meldet seit Langem „Restream #X
teilt sich den Kick-Key mit #Y" — unter der Bedingung `_dup and not
RESTREAM_SINGLE`. Sie war also ausgerechnet in dem Modus stumm, in dem der
Fehler überhaupt entstehen kann. In dreieinhalb Stunden Log steht sie kein
einziges Mal. Ein geteilter Key ist immer falsch; die Warnung gilt jetzt immer.

**Nebenbefund im selben Log:** `Abwehr: CrowdSec-LAPI HTTP 403` stand 109 Mal
da — der Dashboard-Takt ruft den Weg alle zwei Minuten auf, und ein 403 ist ein
Dauerzustand (Bouncer-Schlüssel nicht registriert), kein Ereignis. Was dabei
fehlte, war das Wichtigste: `hint` und `fix` gingen nur an die API zurück, nie
ins Log. Wer den Log las, sah 109 Mal eine Zahl und nie, was zu tun ist. Jetzt
beim ersten Mal und danach höchstens alle 15 Minuten — dafür mit Grund und
Abhilfe.

Zwei Verträge sind neu.

### Behoben — Fehlerbilder aus dem Betrieb und fünf CodeQL-Klassen (v4.1 W10)

**Die Abbruch-Diagnose zeigte auf die falsche Plattform.** Bei jedem
`Input/output error` und jedem `End of file` schrieb der Bot kategorisch
„Kick-Ingest nimmt die Verbindung nicht an (rtmps)" — im `error.log` vom
30.08. sechsmal, während im selben Auszug auch der **Twitch**-Slave scheiterte.
Wer danach handelt, prüft Kick-Key, Kick-App und IP-Block bei Kick, während
Twitch das Problem ist. Eine Diagnose, die auf die falsche Plattform zeigt,
ist schlimmer als gar keine. Sie nennt jetzt die Ziele, deren **Ingest-Host**
wirklich im Auszug steht (`nc/restream_util.betroffene_ziele`) — verglichen
wird auf den vollen Host, nie auf den Plattformnamen: Kick und Twitch liegen
beide auf `live-video.net`, und „twitch" kommt in Twitchs eigener URL nicht vor.

**Eingefrorene Health-Werte sahen aus wie ein gesunder Stream.** Endet der
`-progress`-Leser regulär (ffmpeg schliesst den Strom, EOF — keine Exception,
also auch keine Meldung), blieben Bitrate und FPS im Dashboard auf dem letzten
Wert stehen. Der Stillstands-Wächter meldete einmal „keine Fortschrittsdaten
mehr" und lief danach blind weiter. Das ist die gefährlichere Hälfte: nicht
dass die Messung aufhört, sondern dass ihr letzter Wert weiter als Messung
gilt. Der Leser markiert seinen Eintrag jetzt als `blind` samt Grund, der
Wächter nennt diesen Grund, und das Dashboard zeigt „⚠ blind" statt einer
Zahl, die nichts mehr misst. Der saubere Stopp (`CancelledError`) markiert
ausdrücklich **nicht** — sonst trüge jeder normale Stopp eine Warnung.

**CodeQL, fünf Klassen:**

* *Uncontrolled command line* (Critical). `--window-size` und die Overlay-URL
  gehen aus der `.env` auf Chromiums Kommandozeile. Die Übergabe ist eine
  Liste, es gibt also keine Shell — ein Wert wie `800,600 --dump-dom` wäre
  trotzdem ein zweites Argument, und `file:///…` eine gültige Seite. Beide
  werden jetzt am **einen** Übergabepunkt geprüft; fällt etwas durch, greift
  der Fallback statt eines Fehlers.
* *Uncontrolled data in path expression*. Die Ausliefer-Routen (`/api/clip/<fn>`,
  `/api/tts/<fn>`) prüften auf verbotene Zeichen. Das war dicht, aber es ist
  eine Aussage über Zeichen statt über das Ziel. Jetzt zwei Schranken mit je
  eigener Aufgabe: `werkzeug.utils.safe_join` ist der von Flask mitgelieferte,
  dafür gebaute Schutz und kennt die Sonderfälle je Plattform;
  `nc.util.datei_in()` löst zusätzlich **Symlinks** auf, erzwingt die Endung
  und schliesst den Präfix-Nachbarn aus (`/daten/clips2` fängt mit
  `/daten/clips` an, liegt aber nicht darin) — beides tut `safe_join` nicht,
  ein Symlink im Clip-Ordner zeigte damit weiterhin nach draussen.
  `nc/routes/ops.py` baut den Log-Pfad aus einer Tabelle.
* *Path injection über einen Sprachnamen*. `nc.i18n.katalog()` ist über
  `/api/i18n/katalog?lang=…` erreichbar und legte den Namen in einen Dateipfad.
  Jetzt nur noch Sprachen aus `SPRACHEN`; Unbekanntes fällt auf den leeren
  Katalog, also auf Deutsch.
* *Weak hashing*. Die Item-Id in `nc/news.py` ist ein Inhalts-Hash für den
  Dedup, kein Schutz — `usedforsecurity=False` sagt das. **Der Wert bleibt
  gleich**: ein Wechsel auf sha256 hätte jede bereits veröffentlichte Meldung
  einmalig zur Neu-Meldung gemacht.
* *Bad HTML filtering regex*. `tools/i18n_extract.py` erkannte nur `</script>`.
  Bei `</script >` hätte es den Rest der Datei als Skript verschluckt — alle
  folgenden Textknoten wären lautlos aus dem Katalog gefallen.

Sechs Verträge sind neu (vier in `test_nc_modules.py`, zwei in
`test_restream.py`).

### Geändert — Kick als Blueprint, Kick-Schicht nach `nc/` (v4.1 W9)

`bot.py`: 29.437 → **29.254 Zeilen**. `nc/routes/` trägt jetzt 21 Blueprints
mit 206 Routen, der Monolith noch 153. Damit sind **alle drei** OAuth-Flows
(Kick, Twitch, YouTube) aus dem Monolithen heraus.

`/api/kick` war mit **elf** `nc.ctx`-Einträgen die teuerste offene Gruppe
überhaupt. Neu `nc/kickapi.py` löst Slug, Broadcaster-ID, Sende-Gedächtnis und
Token-Tausch heraus; die Rückruf-Adressen lagen seit W8 in
`nc/oauthredirect.py`. Übrig bleiben `run_async` und `log` — beide gab es
schon. **Null neue Einträge.**

**Geteilter Zustand, nicht kopierter.** `SEND_LAST` schreibt der Kick-Sendepfad
im Bot, gelesen wird es von `/api/kick/sendcheck`. Zwei Kopien, und die
Diagnose meldete ewig „noch kein Sendeversuch", während Kick in Wahrheit jede
Zeile mit 401 abweist — genau die stille Fehlanzeige, gegen die diese Route in
W10 gebaut wurde. Dasselbe für `BID_CACHE`: zwei Caches wären zwei
Fremdabrufe pro Stunde statt einem.

**`globals()` ist raus.** Der laufende Moderator kam an neun Stellen über
`globals().get("_KICK_MOD")`. Im Monolithen liefert das die Instanz; in einem
Blueprint ist `globals()` **dessen** Namensraum — der Wert wäre für immer
`None`, und `/api/kick/sendcheck` meldete „Kick-Moderator läuft nicht",
während er läuft. Er steht jetzt im Register `nc.channels.KICK_MOD`, neben
`TWITCH_SEND`/`YT_SEND`. Das ist zugleich die Vorarbeit für `/api/kickmod`
und `/api/chat`.

Die Zugangsdaten (`KICK_CLIENT_ID`, `KICK_CLIENT_SECRET`,
`KICK_BROADCASTER_ID`) kommen über `ctx.cfg` statt über eine zweite
`os.getenv`-Stelle — der Bot friert sie beim Import ein, ein zweiter Lesepfad
könnte abweichen.

**Werkzeugfehler behoben, und dieser hätte Produktion getroffen:**
`bp_analyse` und `bp_extract` durchsuchten für „wer benutzt diesen Helfer
sonst noch?" nur Top-Level-Funktionen — **keine Klassenkörper**.
`_kick_broadcaster_id` wird ausschliesslich von `KickModerator` und den
`/api/kick`-Routen benutzt; der Extraktor hielt ihn deshalb für „gehört nur
den Routen", hätte ihn ins Blueprint verschoben und aus `bot.py` entfernt —
der Kick-Chat wäre beim nächsten Sendeversuch mit `NameError` gestorben,
mitten in einem `except`-Block. Beide Werkzeuge sehen jetzt Klassenkörper,
und jede **lesende** Erwähnung zählt, nicht nur `ast.Call`.

Drei Verträge sind neu, sieben Anker gewandert (B169, W9, W10, W17, W23, W49,
W8) — keiner gelöscht.

### Geändert — OAuth-Rückruf-Schicht nach `nc/`, Twitch und YouTube als Blueprint (v4.1 W8)

`bot.py`: 29.714 → **29.437 Zeilen**. `nc/routes/` trägt jetzt 20 Blueprints
mit 198 Routen, der Monolith noch 161.

**Reihenfolge wie in W117: erst die Schicht, dann die Routen.** `/api/twitch`
hätte vorher drei `nc.ctx`-Slots gekostet, `/api/youtube` acht — bei 24 von
vertraglich 25 belegten Slots war das der Grund, warum beide Gruppen liegen
blieben. Nach dem Umzug der Schicht kosten sie **null**.

Neu `nc/oauthredirect.py`: `public_base_url()`, `redirect_env()`,
`redirect_uri()`, `redirect_source()`, `redirect_public()`. Die Reihenfolge
app_config → `.env` → öffentliche Basis-URL steht damit an **einer** Stelle für
Kick, Twitch und YouTube. Fällt sie auseinander, kommt genau der Fehler zurück,
den W121 behoben hat: `redirect_uri_mismatch`, ausgelöst **vor** der
Kontoauswahl — also ohne jede Meldung im Bot.

`TRUSTED_PROXIES` und `DASHBOARD_PORT` kommen per `configure()` aus dem Bot,
nicht aus einer zweiten `os.getenv`-Stelle im Modul: zwei Lesestellen mit
unterschiedlichen Werten wären genau der unauffindbare Fall.
`PUBLIC_BASE_URL` und die `*_REDIRECT_URI` liest die Schicht weiterhin bei
jedem Aufruf — sie sind zur Laufzeit änderbar.

`nc/channels.py` bekam `YT_API_CACHE`, `YT_SENDRATE` und `yt_sendrate_cfg()`
dazu — sie standen als Modul-Globals im Monolithen, neben `YT_SEND`, das
längst dort liegt. Der direkte Import trifft **dasselbe** Objekt: eine zweite
Kopie wäre ein Zustandsriss, bei dem der Trennen-Knopf den Token-Cache des
Sendepfads nicht mehr leert und der Bot nach dem Abmelden weitersendet. Ein
Vertrag prüft das.

**Werkzeug korrigiert:** `tools/bp_analyse.py` hielt `_YT_SEND =
_nc_channels.YT_SEND` für einen Monolith-Global und meldete drei
`nc.ctx`-Einträge, die es gar nicht gibt — dieselbe Fehlanzeige, die es bei
reinen Delegations-Funktionen schon kannte. Aliase auf `nc`-Modul-Attribute
zählen jetzt als direkt importierbar, aber nur bei **eindeutiger** Bindung: wer
auf Modulebene ein zweites Mal zugewiesen wird, ist kein Alias, sondern Zustand
mit Geschichte.

Vier Verträge sind neu, sieben Anker gewandert (Aufteilung, Bremse,
`cfgnorm`, OAuth-Seite, W121, W122, W23) — keiner gelöscht.

### Geändert — Sprache je Benutzer statt je Server (v4.1 W7)

Bis W6 entschied `UI_LANG` für alle. Ein deutschsprachiger und ein
englischsprachiger Zuschauer im selben Discord bekamen dieselbe Sprache — und
zwar die des Betreibers. Jetzt entscheidet Telegrams `language_code` bzw.
discord.pys `interaction.locale` **je Anfrage**.

**Die Sprache hängt an der Anfrage, nicht am Modul.** `nc.i18n` führt sie in
einer `ContextVar`. Ein Modul-Global wäre geteilter Zustand zwischen
gleichzeitigen Tasks — der Deutsche bekäme Englisch, weil eine Millisekunde
vorher ein Engländer gefragt hat. Ein Vertrag beweist das mit zwei parallel
laufenden Tasks.

Gesetzt wird **vor** dem Handler, an genau einer Stelle je Plattform: Telegram
über `TypeHandler(Update, …)` in Gruppe −1, Discord über
`tree.interaction_check`. Damit sind alle 46 Slash-Befehle und alle
Telegram-Handler erfasst, ohne einen einzigen davon anzufassen.

Beide Haken sind **fail-open**. `interaction_check` ist eigentlich eine
Berechtigungsprüfung: gäbe die Spracherkennung dort `False` oder würfe sie, wäre
jeder Slash-Befehl im Discord tot — die Übersetzung hätte den Bot abgeschaltet.
Sie fängt deshalb alles und liefert immer `True`.

212 Sendestellen sind mechanisch mit `_nc_i18n.t(…)` umschlossen, über
Byte-Offsets (die Em-Dash-Falle aus W6c). `t()` reicht Nicht-Text unverändert
durch — manche Sendestellen bekommen kein Wort, sondern `None` oder ein Embed,
und ein `TypeError` dort wäre eine Antwort, die gar nicht erst rausgeht.

**Ein Fehler dabei gefunden und behoben:** der Wrapper entschied nach dem
*Methodennamen*, wo der Text steht. Bei `telegram.Bot.send_message(chat_id,
text)` stimmt Position 2 — bei `KickModerator.send_message(text, session)` steht
dort die **Session**. Drei Stellen übersetzten die HTTP-Session und ließen den
Text deutsch. Der Empfänger entscheidet, nicht der Name; ein Vertrag hält fest,
dass `t()` auf keiner Session mehr sitzt.

Zwei Vertragsanker sind mitgewandert (Kick-only-Fallback, Announce) — beide
Verträge gelten unverändert, nur ihr wörtlicher Anker hat sich um das `t(…)`
erweitert.

### Hinzugefügt — die restliche Dokumentation auf Englisch (v4.1 W7)

`docs/en/` trägt jetzt auch CrowdSec, die drei SETUP-Anleitungen und die
Fremdcode-Lizenzen: **30 Dokumente zweisprachig**, jedes mit beidseitigem
Sprachumschalter. Der Link-Vertrag deckt sie alle ab.

Deutsch bleiben weiterhin `CHANGELOG.md`, `README_V37.md` und
`MODULARISIERUNG.md` (Historie und interne Analyse, ~3.700 Zeilen) sowie
`START_HIER.txt` — eine `.txt`, keine Markdown-Datei.


### Hinzugefügt — Mehrsprachigkeit, Englisch als zweite Sprache (v4.1 W6)

Oberfläche, Bot und Doku sprechen jetzt Deutsch **und** Englisch. Neu:
`nc/i18n.py` (Katalog, Spracherkennung, Rückfall), `nc/routes/i18n.py`
(Katalog-, Sprachlisten- und Wahl-Endpunkt plus der ausgelieferte Übersetzer),
`locales/de.json` und `locales/en.json`, `tools/i18n_extract.py` und die
Variable `UI_LANG` (Default `de`).

**Der Ansatz ist ungewöhnlich und deshalb begründet: die deutsche Zeichenkette
IST der Schlüssel.** Der Bestand hatte 1.803 übersetzbare Zeichenketten in
sieben Dateien. Jede davon gegen einen künstlichen Schlüssel zu tauschen wäre
ein Umbau an 1.803 Stellen gewesen: nicht rückrollbar, nicht einzeln prüfbar
und mit sicherem Verlust einzelner Strings. So bleibt der Bestand unverändert
lesbar, und ein fehlender Eintrag fällt auf Deutsch zurück statt auf einen
nackten Schlüsselnamen. Der Preis — ein geänderter deutscher Text verliert
still seine Übersetzung — ist bekannt; genau dagegen steht
`tools/i18n_extract.py --check`, das fehlende **und** verwaiste Einträge meldet.

**Übersetzt wird im Browser, nicht auf dem Server.** Das Dashboard erzeugt den
größten Teil seiner Texte selbst; serverseitiges Rendern hätte nur das feste
Gerüst getroffen und den Rest deutsch gelassen — sichtbar halb übersetzt, also
schlechter als gar nicht. Ein `MutationObserver` fängt nachgeladene Inhalte;
`<code>`, `<pre>`, `<textarea>` und alles unter `[data-i18n-skip]` bleiben tabu,
dort stehen Befehle und Logzeilen. Dashboard, brain und overlay binden denselben
Übersetzer unter `/api/i18n/uebersetzer.js` ein.

Sprachwahl in dieser Reihenfolge: `?lang=` schlägt Cookie schlägt
`Accept-Language` schlägt `UI_LANG`. Eine gesetzte Wahl darf der Browser nie
überstimmen, sonst springt die Oberfläche auf dem nächsten Gerät zurück.

Der Bot übersetzt am **Sendeweg**: `_safe_send` ist der einzige Weg nach
Telegram, deshalb steht die Übersetzung dort und nicht an 90 Aufrufstellen. Die
46 Discord-Slash-Beschreibungen sind einzeln umschlossen, weil sie zur
Definitionszeit ausgewertet werden.

Der Katalog umfasst **647 Einträge, alle übersetzt**. Logzeilen sind bewusst
nicht dabei: sie erreichen nie einen Benutzer, `CLAUDE.md` sagt ausdrücklich,
dass sie deutsch bleiben, und im Katalog hätten sie als „noch zu übersetzen"
gezählt und verdeckt, was wirklich fehlt.

Vier Fallen unterwegs, jede davon still:

* **Der Extraktor sammelte rohe JS-Literale.** Der Übersetzer vergleicht aber
  Textknoten — `'<div class="empty">Noch keine Aufnahmen.</div>'` hätte als
  Schlüssel NIE getroffen. Jetzt zieht er Markup und `${…}` ab und verwirft
  Bruchstücke, die im DOM nie allein stehen. Ein Eintrag, der nie trifft, wäre
  schlimmer als keiner: er zählte als erledigt, während die Stelle deutsch
  bleibt.
* **Pythons AST liefert Byte-Offsets, keine Zeichen.** Beim Umschließen der
  `description=`-Literale landete der Schnitt hinter jedem Em-Dash zu weit
  rechts und fraß die schließende Klammer. `py_compile` fing es sofort.
* **22 Befehlsbeschreibungen fielen durch den Deutsch-Filter** („Status",
  „Tracklist", „Ban") und eine durch den Bezeichner-Filter („Restream-Status").
  Beide Heuristiken sind an `description=` falsch — dort steht per Definition
  Text für Menschen. Ohne die Ausnahme wäre die Befehlsliste im Discord halb
  deutsch geblieben.
* **Der Blueprint-Vertrag verlangt `/api/` für jede Route.** Der erste Entwurf
  lieferte den Übersetzer unter `/i18n.js` aus — ein Sonderweg neben der API.
  Der Pfad heißt jetzt `/api/i18n/uebersetzer.js`.

Neuer Vertrag: die 100-Zeichen-Grenze der Slash-Beschreibungen wird gegen
**beide** Sprachen geprüft. Ausgeliefert wird ab jetzt die übersetzte — eine zu
lange englische Beschreibung ließe die Registrierung scheitern, und der Befehl
wäre im Discord schlicht weg, ohne dass irgendetwas rot würde.

### Hinzugefügt — englische Dokumentation neben der deutschen (v4.1 W6)

`README.en.md`, `CLAUDE.en.md` und `docs/en/` mit Index, Roadmap, Installation,
Deploy, Fehlersuche, Mitwirken, Sicherheit und Verhaltenskodex. Jede deutsche
Datei mit englischer Entsprechung trägt oben einen Sprachumschalter, und beide
Seiten zeigen aufeinander.

**Die deutsche Fassung bleibt die Quelle.** Bei `CLAUDE.md` steht das
ausdrücklich in der englischen Datei: Claude Code lädt die deutsche, und wenn
beide auseinandergehen, gilt die deutsche.

Nicht übersetzt und in `docs/en/README.md` begründet: `CHANGELOG.md`,
`README_V37.md` und `MODULARISIERUNG.md` — rund 3.700 Zeilen Historie und
interne Analyse, die mit jeder Welle wachsen. Zwei Fassungen davon zu pflegen
hieße, sie bei jeder Welle doppelt fortzuschreiben.

Ein Vertrag hält beides fest: jede englische Datei existiert, beide Seiten
verweisen aufeinander, und kein relativer Link in den zwanzig Dokumenten zeigt
ins Leere.


### Behoben — neun weitere Dauerläufer-Stellen melden ihre Ausfälle (v4.1 W5)

W2 hat sieben Stellen versorgt und im Changelog gestanden, damit sei die Regel
durchgesetzt. Ein Scan über **alle** Dauerschleifen fand zwölf, die weiter an
`_loop_fehler` vorbei meldeten — sieben davon still auf `log.warning`, was in
einem ERROR-Log nicht erscheint:

* **`reaper_loop`** — die EINZIGE Instanz, die tote Recorder-Prozesse abräumt.
  Fällt sie aus, bleiben Zombies in den Slots und keine Aufnahme startet mehr.
* **`_storage_cleanup_loop`** — ohne ihn läuft die Platte voll.
* **`_proxy_pool_refresh_loop`** — ohne Refresh altert der Pool, und die
  Aufnahmen laufen nach und nach auf tote Proxies.
* **`_evolution_loop`** — in W2 übersehen, obwohl dort genau diese Regel
  aufgestellt wurde.
* **`_live_react_loop`** — fällt sie aus, reagiert AZRAEL im Live-Chat auf
  nichts mehr; das sieht aus wie „die KI antwortet nicht", nicht wie ein Ausfall.
* **`_db_maintenance_loop`** — Datenbank wächst unbegrenzt, der Planer arbeitet
  mit alter Statistik.
* **`_system_backup_loop`** — war sichtbar, aber ohne Traceback und ungedrosselt.

Dazu zwei Stellen eine Ebene tiefer: `_disk_alarm_loop` und `_cookie_alarm_loop`
melden ihren eigenen Absturz längst auf `log.error` mit Traceback, aber ihre
**Prüfung** scheiterte still. Scheitert die dauerhaft, feuert der Alarm nie und
die Schleife läuft weiter — von aussen nicht von „alles in Ordnung" zu
unterscheiden.

Nicht angefasst: `_daily_summary_loop`, `_disk_alarm_loop`, `_cookie_alarm_loop`,
`_restream_verify_loop` und `_auto_restream_loop` melden ihren Schleifenfehler
bereits auf `log.error` mit Traceback (die beiden Restream-Wächter seit B138).
Sie sind sichtbar; ihnen fehlt nur die Drosselung, und sie ticken minütlich bis
stündlich.

Der Vertrag prüft ab jetzt **generisch**: kein Dauerläufer ohne sichtbare
Fehlermeldung. Vorher war das eine Liste, die jede neue Schleife wieder
unterlaufen konnte.

### Geändert — Monolith zerlegt: die Streamer-Ansicht (v4.1 W5)

`bot.py` schrumpft von 29.942 auf **29.646 Zeilen**. Von den 355 Flask-Routen
liegen jetzt **183 ausserhalb** (vorher 173), in **17 Blueprints**. Die
Routentabelle ist vor und nach der Welle bitgleich.

`/api/streamer` kostete nach `bp_analyse` **elf** Kontext-Einträge; nach dem
Lösen der Helfer fünf, und alle fünf gab es bereits. **Vierte Welle in Folge
ohne einen neuen `nc.ctx`-Slot.** Gelöst wurden `_ci_key` und
`_resolve_tracked_user` nach `nc/trackingdb.py` (beide drehen sich um die
gespeicherte Schreibweise eines Handles), `_tiktok_account_exists` in das neue
`nc/tiktokcheck.py`, und `remove_tracking` ebenfalls nach `nc/trackingdb.py` —
letzteres mit einem `on_remove`-Rückruf, weil die sieben per-tracking-Dicts dem
Live-Worker gehören und nicht der Datenbank (derselbe Weg wie `on_resume` in
W117; ohne den Rückruf wächst der Orphan-State still weiter, F51/B6).

**Der Befund dieser Welle ist ein Werkzeugfehler, kein Codefehler.**
`api_streamer_compare` enthält eine verschachtelte Hilfsfunktion `def stats(u)`.
`bp_extract` sammelte die Aufrufe einer Route und verglich die Namen mit den
Top-Level-Definitionen, **ohne zu prüfen, was die Route selbst bindet** — der
gleichnamige **Telegram-Befehl `stats`** galt damit als Helfer dieser Route,
wäre ins Flask-Blueprint gewandert und aus `bot.py` verschwunden. Bemerkenswert
ist, was das nicht gefangen hätte: die Routentabelle bleibt identisch, weil sie
nur Flask-Regeln zählt; ein Slash-Befehl weniger ist dort unsichtbar. Der
Extraktor schliesst lokal gebundene Namen jetzt aus, und ein Vertrag hält beide
Hälften fest.

**Liegen bleibt `/api/profile`** (3 Routen, 184 Zeilen). Es hängt an
`_get_live_info` — einer Funktion mit acht weiteren Aufrufern im Recorder-Kern.
Sie ist echter Bot-Laufzeitcode und liesse sich nur über einen neuen
Kontext-Slot erreichen, den genau *ein* Blueprint benutzt; genau den Fall
schliesst `nc/ctx.py` im Kopf aus. Die Gruppe wartet auf das Lösen der
Live-Auflösungs-Schicht, nicht auf einen Slot.


### Behoben — `bot_app` war nie gebunden, zwei Melder liefen ins Leere (v4.1 W4)

`bot_app` kam in `bot.py` ausschliesslich als **Parametername** vor, nie als
Modul-Global. Die beiden Stellen, die ihn per `globals().get("bot_app")` lesen,
bekamen deshalb immer `None`:

* **`_brain_notify`** meldete „BRAIN-ALARM (Loop/Bot nicht bereit)" auf
  `log.warning` und kehrte um. In einem ERROR-Log erscheint davon nichts — kein
  einziger Brain-Alarm hat je Telegram erreicht.
* **`_marketing_post_telegram`** antwortete dauerhaft
  `{"ok": false, "error": "Bot nicht bereit"}`. Der Telegram-Zweig des
  Marketings war tot; im Dashboard sah es nach einem Konfigurationsfehler aus.

Genau das Fehlerbild aus `CLAUDE.md`: etwas „geht nicht" und der Grund steht in
einem `warning`, das niemand sieht. Gefunden beim Vermessen der Abhängigkeiten
für den News-/Marketing-Umzug — `globals()`-Zugriffe sind dort seit W116
Handprüfung. Der Name wird jetzt dort gebunden, wo die Application zum ersten
Mal feststeht: in `run_bot`, zwei Zeilen über `_GLOBAL_SCRAPER`, das an
derselben Stelle nach demselben Muster gesetzt wird. Vertrag:
`test_v41_w4_bot_app_gebunden`.

### Geändert — Monolith zerlegt: News- und Marketing-Kern plus 13 Routen (v4.1 W4)

`bot.py` schrumpft von 30.451 auf **29.942 Zeilen** — zum ersten Mal unter
30.000. Von den 355 Flask-Routen liegen jetzt **173 ausserhalb** (vorher 160),
in **16 Blueprints**. Die Routentabelle ist vor und nach der Welle bitgleich.

Dieselbe Reihenfolge wie in W117 und W3, diesmal für zwei Module gleichzeitig:
**erst der Kern, dann die Routen.** 404 Zeilen — Faktenerhebung, Config, Zustand,
`news.json`-Schreiber, KI-Pfad, Creator-Dossier, das Marketing-Senden — sind
wörtlich nach `nc/news.py` und `nc/marketing.py` gewandert, wo bisher nur die
bot-freie Text- und Anti-Spam-Logik lag. `/api/news` kostete davor **zwölf**
Kontext-Einträge, `/api/marketing` **sieben**; danach zwei und drei, und alle
fünf gab es schon (`run_async`, `get_main_loop`, zwei `cfg`-Schlüssel).
**`nc.ctx` ist um null Einträge gewachsen** und steht weiter bei 24 Slots.

Drei Fallen, jede davon still:

* **`__file__` wiederholt sich pro Welle.** `_news_output_path` legt `news.json`
  neben den Bot. Im Fachmodul wäre daraus `nc/website/news.json` geworden — die
  öffentliche Seite hätte eine Datei gelesen, die niemand mehr schreibt, und der
  News-Agent hätte in ein totes Verzeichnis geschrieben. Kommt jetzt als
  `bot_file` aus dem Bot; im Testharnisch gegengeprüft.
* **Die `.env.example`-Falle aus W117, anders herum.** Nicht der Suchpfad des
  Scanners, sondern die Schreibweise der Aufrufstelle: aus
  `_env_int("NEWS_MAX_ITEMS", 20)` wurde durch die Injektion
  `_conf["env_int"](...)`, worauf das Muster des Generators nicht mehr passt.
  **Acht Variablen** wären lautlos aus der Vorlage gefallen. Gefunden hat es der
  Vertrag. `_env_int` ist ohnehin nur eine Weiterleitung auf `nc.envnum` — jetzt
  direkt importiert statt injiziert, damit die Aufrufstelle wörtlich bleibt.
* **Verschattung beim Umbenennen.** Wie `llm_note` in W3: `publish()` hat ein
  lokales `flavor`, `generate()` ein lokales `facts`, `phrase_impl()` einen
  Parameter dieses Namens. Die Funktionen heissen deshalb `ai_flavor` und
  `collect_facts`; `pyflakes` (F823) hat beides vor dem ersten Lauf gefunden.

Ausserdem ist `_loop_not_ready` nach `nc/util.py` gewandert — ein reines
Prädikat mit siebzehn Lesern im Monolithen und ab jetzt in jedem Blueprint. Als
Kontext-Slot wäre es Verschwendung gewesen.

Fünf Vertragsanker sind mitgewandert (Fakten-Sammlung, Aufnahme-Verbot im
Prompt, Creator-Dossier, Invite-Auflösung, Absatz-Normalisierung) — **kein
einziger gelöscht**. Neu: `test_v41_w4_news_marketing_kern_raus`.


### Geändert — Monolith zerlegt: der Evolution-Core und seine acht Routen (v4.1 W3)

`bot.py` schrumpft von 30.944 auf **30.451 Zeilen**; von den 355 Flask-Routen
liegen jetzt **160 ausserhalb** des Monolithen (vorher 152). Die Routentabelle
ist vor und nach der Welle bitgleich — Pfad **und** `methods`, geprüft mit
`tools/route_inventory.py`.

`nc.ctx` stand bei 24 von 25 erlaubten Slots, und `/api/evolution` hätte nach
der Kostenrechnung fünf Funktionen und fünf Globals gebraucht. Statt die Grenze
zu verschieben, ist wie in W117 erst der Kern gelöst worden — diesmal
vollständig: Versionszähler, LLM-Notiz, der `build/`-Schreiber und der Zyklus
selbst (zusammen 352 Zeilen) sind wörtlich nach `nc/evolution.py` gewandert, wo
seit B167 nur `analyze()` lag. Danach kostet das Blueprint **null**
Kontext-Einträge: `nc/routes/evolution.py` importiert `nc.evolution` direkt und
kennt `nc.ctx` überhaupt nicht. Der Kontext steht weiterhin bei 24 Slots.

Im Bot bleibt genau das, was dorthin gehört: die `EVOLUTION_*`-Startwerte, der
Supervisor `_evolution_loop` und ein `nc.evolution.configure(...)` in der
Kompositionswurzel.

Drei Befunde, die die Welle fast still kaputtgemacht hätten:

* **`__file__` ist beim Umzug dieselbe Falle wie `globals()` in W116.** Der
  Self-Reproduction-Pfad schreibt einen versionierten Schnappschuss der eigenen
  Quelle mit `open(__file__)`. Im Monolithen ist das `bot.py`; im Fachmodul wäre
  es ab dem Umzug das 25 KB grosse `nc/evolution.py` gewesen — `build/bot_v{N}.py`
  hätte still das falsche File enthalten, und **gemerkt hätte es niemand**, weil
  der ganze Pfad in einem `except: pass` hängt. Die Quelle kommt jetzt als
  `bot_file` aus dem Bot; ein Vertrag hält fest, dass `nc/evolution.py` `__file__`
  nicht mehr liest. Gegenprobe im Testharnisch: der geschriebene Schnappschuss
  ist 1,5 MB gross, nicht 25 KB.
* **Ein Funktionsname, der eine lokale Variable beschattet.** Der Zyklus enthält
  `llm_note = _evolution_llm_note(...)`. Hiesse die Funktion nach dem Umzug
  `llm_note`, bände Python den Namen für die ganze Funktion lokal und der Aufruf
  stürbe mit `UnboundLocalError` — erst zur Laufzeit, mitten im Zyklus.
  `pyflakes` hat es als F823 gefunden, bevor es je lief; sie heisst jetzt
  `engineering_note`.
* **Der Extraktor benennt auch Schlüsselwort-Argumente um.** `analyze(...)` wird
  mit genau den Namen gerufen, die umzubenennen waren; `rewrite_names` sieht bei
  `f(x=x)` keinen Unterschied zwischen links und rechts. Die Signatur von
  `analyze()` ist der Vertrag aus B167 und bleibt unangetastet.

Der Vertragsanker aus B167 (`_nc_evolution.analyze(` in `bot.py`) ist gebrochen,
weil der Bot `analyze()` gar nicht mehr selbst ruft — der **Vertrag** gilt
weiter, nur sein **Anker** ist gewandert. Er wurde migriert, nicht gelöscht.
Neu dazu: `test_v41_w3_evolution_core_raus` hält die fünf gewanderten Funktionen,
die `bot_file`-Durchreichung, das laute Werfen ohne `configure()` und die
Kontextfreiheit des Blueprints fest. `test_smoke.py` ruft den Zyklus einmal
vollständig durch — 6 geschriebene Dateien, Schnappschuss in voller Grösse.


### Behoben — Dauerläufer, die ihre Ausfälle verschluckt haben (v4.1 W2)

Die Regel steht in `CLAUDE.md`: jeder Dauerläufer gehört auf `_loop_fehler`
(erste Meldung sofort mit Traceback, danach höchstens alle 15 Minuten eine) —
nie auf `log.debug` und nie auf `pass`. Ein `log.warning` erscheint in einem
ERROR-Log ebenfalls **nie**; genau so blieb der Discord-Gateway-Tod
monatelang unsichtbar. Sieben Stellen hielten sich nicht daran, und bei jeder
nimmt ein stiller Ausfall ein ganzes Stück Funktion mit:

* **Beide YouTube-Chat-Schleifen.** W116 hatte für Dauerverbindungen
  `_verbindung_verloren()` eingeführt und Kick-WebSocket, Twitch-EventSub und
  Twitch-Chat umgestellt — die zwei YouTube-Schleifen blieben liegen. Eine
  dauerhaft abreißende YouTube-Verbindung stand damit nur auf `log.debug`.
  Jetzt derselbe Weg wie bei Twitch, inklusive Flatter-Bewertung über
  `nc/flapguard.py` (Gateway-Rotation ist kein Vorfall, dauerndes Flattern
  schon).
* **`_stats_loop` → `_nc_usage.flush()`** im stillen `except: pass`. Schlägt
  das Sichern dauerhaft fehl, zählt der Bot ins Nichts.
* **`_scheduler_loop`** gab bei einem Query-Fehler stumm `[]` zurück — das
  heißt: keine fällige Aufgabe gefunden, der Zeitplan läuft nie, und das Log
  sagt nichts.
* **`_db_vacuum_loop`** ließ `ANALYZE` und `VACUUM` still scheitern. Die
  Datenbank wächst dann unbegrenzt weiter, der Planer arbeitet mit veralteter
  Statistik — beides sieht man erst viel später.
* **`_viewer_sample_loop`** hatte ein stilles `continue`: fällt die Stichprobe
  aus, bleibt die Zuschauerkurve leer, ohne Grund im Log.
* **`_upload_window_loop`** meldete auf `log.warning`. Dieser Läufer hält die
  aufgeschobenen Uploads — fällt er aus, bleiben Aufnahmen für immer in der
  Warteschlange.

Nicht angefasst und bewusst still bleiben die 19 Stellen, die `CLAUDE.md`
ausdrücklich ausnimmt: der Fehlerkanal selbst (dort erzeugt Loggen Rekursion),
Aufräumpfade, deren Fehlschlag bedeutungslos ist (`proc.terminate()` auf einen
toten Prozess), Zeilen-/Zeilenweise-Parser und ein `raise`, das ohnehin
weiterwirft.

### Behoben — `/healthz` war ein Präfix, kein Pfad (v4.1 W2)

`_AUTH_EXEMPT_PREFIXES` enthielt `/healthz`, geprüft mit `startswith`. Damit
hätte auch `/healthzirgendwas` den Login übersprungen. Es ist genau **eine**
Route — steht jetzt bei den exakten Pfaden. `/api/public/` bleibt Präfix, dort
liegen mehrere Routen.

### Behoben — `gen_env_example.py` hätte Variablen still verlieren können (v4.1 W2)

Der Scanner schnitt Kommentare mit `zeile.split("#", 1)[0]` ab. Ein Default,
der selbst ein `#` enthält — eine Farbe wie `os.getenv("UI_ACCENT", "#e8c86a")` —
hätte die Zeile mittendrin zerschnitten, das Muster nicht mehr gepasst, und
die Variable wäre lautlos aus `.env.example` gefallen. Genau die Lücke, gegen
die das Skript geschrieben wurde; `--check` hätte es nicht gefangen, weil
beide Seiten vom selben Scanner kommen. Heute trifft es keine einzige
Lesestelle (nachgezählt: null) — es war eine Falle für die nächste. Der
Schnitt ist jetzt quote-bewusst.

Der Vertrag `test_v41_w2_dauerlaeufer_melden_sich` hält alle sieben Stellen
fest; jede Zusicherung wurde per Sabotage gegengeprüft.


### Geändert — Monolith zerlegt: fünf Blueprints, 62 Routen, 1.762 Zeilen (W116, W117)

`bot.py` schrumpft von 32.596 auf **30.834 Zeilen**; von den 355 Flask-Routen
liegen jetzt **152 ausserhalb** des Monolithen (vorher 90). Verhalten
unverändert — die Routentabelle ist vor und nach beiden Wellen bitgleich,
Pfad **und** `methods`.

Neu in `nc/routes/`: `settings` (Konfiguration, Zeitplan, DB-Im/Export,
Cookies), `ops` (Betrieb, Tunnel, Selbst-Update), `money` (Spenden,
Finanzamt), `trackings`, `stats` (Auswertung, KI-Log, Moderations-Feed). Neu
in `nc/`: `donationsdb`; erweitert: `trackingdb` (+11 Zugriffe), `stats`
(+`get_stats`, +Status-Verteilung), `proxyutil` (Tunnel-Zustand lesen).

Vier Dinge, die für den Betrieb zählen:

- **`nc.ctx.configure(...)` steht jetzt am Dateiende.** Vorher mitten in der
  Datei — und sah damit nur Namen, die bis dorthin definiert waren.
- **`globals().get("BOT_VERSION")` wäre beim Umzug still gebrochen.** In einem
  Blueprint ist `globals()` das Modul; vier Routen hätten dauerhaft ihren
  Default geliefert („Version 3.7", „event_loop: false").
- **Geteilter Laufzeitzustand wandert als Referenz, nie als Kopie** — Cookie-
  Cache, Ressourcen-Ring, Tunnel-Dict und die neun Zähler des Live-Workers.
  Eine Kopie wäre ein Panel, das einfriert, oder ein Schalter ohne Wirkung.
- **`tools/gen_env_example.py` scannte `nc/routes/` nicht.** Mit der letzten
  Lesestelle von `DASHBOARD_TRACK_GROUP_ID` im Blueprint wäre die Variable
  lautlos aus `.env.example` gefallen.

Neue Werkzeuge: `tools/route_inventory.py` (Routentabelle vor/nach
vergleichen), `bp_extract --mit` (Cache zieht mit seinem Eigentümer um) plus
Warnung vor Namenskollisionen mit dem Kontextzugriff.

### Behoben — neun Panels aus dem Reorg wieder verdrahtet (W126)

Der Reorg löste die Ansichten **VAULT**, **INTEL**, **BRAIN+** und **LAB** auf
und ließ ihre Loader mit einem Wächter (`if(!$('#x')) return;`) stehen. Die
Funktionen laufen seither, greifen ins Leere und melden nichts. Alle
betroffenen Endpunkte antworteten die ganze Zeit weiter — es fehlte nur die
Oberfläche. Jetzt hängen sie da, wo sie hingehören:

**Betrieb → Automatisierung** (neues Panel): Auto-Archiv-Regeln
(`/api/auto-archive-rules`), Webhooks (`/api/webhooks`), Sammlungen
(`/api/collections`), Ruhezeiten (`/api/notifications/quiet-hours`). Für alle
vier gab es nur Lese-, Test- und Löschwege — das **Anlegen** fehlte, und eine
Liste, die nur leer sein kann, ist keine Bedienung. Das Regel-Formular bietet
genau die vier Bedingungen, die `evaluate_archive_rule` wirklich kennt, und
benennt die eine Aktion, die die Regel-Maschine beherrscht.

**Betrieb → Aufnahmefenster planen**: das Anlegen lief seit je, die geplanten
Fenster **anzusehen** oder zu entfernen nicht (`/api/schedule/list|remove`).

**AZRAEL Brain → Evolutions-Kern** (neues Panel): Stand, Wissensbalken,
gelernte Werte und offene Vorschläge (`/api/evolution/status|learned|
proposals`). Verlauf und Changelog hatten anderswo überlebt — deshalb fiel
nicht auf, dass der Rest unsichtbar war.

**AZRAEL Brain → KI-Chat** (neues Panel): hier fehlte mehr als Markup. Da
waren nur Lesewege ohne Eingang — Konversationen laden, öffnen, löschen.
Modell-Liste, neue Konversation und **Senden** gab es nicht, `_aiModels` wurde
nie gefüllt. Neu geschrieben; die vollständige Stilvorlage (`.ai-wrap` bis
`.ai-send`) stand die ganze Zeit im Stylesheet.

**Streams → Aufnahmen** (neues Panel): die Aufnahmen aus der Datenbank samt
Aufnahme-Fenster (Manifest, Qualität, Wellenform, Notizen, Marken). Ohne
Liste war das Fenster über keinen Weg mehr erreichbar.

**Control → Highlight-Clips** (neues Panel): `loadClips()` lief seit je im
700-ms-Takt über `avatarPoll` und schrieb in ein Raster, das es nicht gab.
Die Clips entstanden also durchgehend, sehen konnte sie niemand.

Zwei Altlasten ersatzlos entfernt statt Markup zu erfinden: `km_conn`
(denselben Zustand zeigen `kms_conn` und die Kanal-Chips) und `cc_tag` (der
zweite Einbau der Kommandozentrale, den W71 entfernt hat — `ov_cc_tag` lebt).

**Drei Fehler, die erst der Browser gezeigt hat:**

* `loadAutomation()` gab es **zweimal** — der Autopilot-Lader und, im ersten
  Anlauf dieser Welle, das Automatisierungs-Panel. Die spätere Deklaration
  gewinnt; das Panel blieb stumm, ohne dass irgendwo ein Fehler stand. Meines
  heißt jetzt `loadAutomatisierung()`.
* `loadClips is not defined`: Funktions-Deklarationen gelten nur im eigenen
  `<script>`-Block. Ein Ansichts-Loader in einem früheren Block sieht spätere
  Deklarationen nicht — und die Restream-Ansicht wird schon während des
  Parsens aufgebaut. Dafür gibt es jetzt `nachAufbau(name)`.
* `d.items.map` im Autopilot-Lader war ungeprüft: antwortet die Route ok, aber
  ohne `items`, warf es und das Panel blieb stumm zurück. Gehärtet.

Beim Wiederbeleben zwei Escaping-Altlasten mitgenommen: der Clip-Name ging über
`esc()` plus String-Konkatenation in einen `onclick` — das Muster, das W118 mit
`escJs()` geschlossen hat. Und die englischen Beschriftungen der wiederbelebten
Renderer (`no rules defined`, `KEINE COLLECTIONS`, `RUN`, `test/off/on`,
`URL/Events/Fails`, `4 msg`) sind jetzt deutsch.

Ergebnis messbar: **0 tote IDs** (vorher 28), **0 unerreichbare Funktionen**
(vorher 27) im Dashboard. Der Vertrag
`test_v40_w126_reorg_reste_verdrahtet` prüft nicht Einzel-IDs, sondern die
Eigenschaft, die verloren ging — *jede ID, die das JavaScript nachschlägt,
muss es im Markup geben* — plus doppelte Funktionsnamen. Diese eine Zeile
hätte W122, W125 und W126 verhindert. Jede Zusicherung wurde durch Sabotage
gegengeprüft.

Geprüft im echten Browser (Chromium gegen eine gestubbte API): 36 Schritte
über alle vier Ansichten, plus die 15 aus W125 — Kennzahlen, Listen, Anlegen,
Ablehnen falscher Eingaben, Senden im Chat, Apostroph im Datei- und
Clip-Namen, keine Konsolenfehler.

### Behoben — Papierkorb, Dubletten und Umbenennen waren unerreichbar (W125)

Der Reorg löste die Ansichten **VAULT** und die Aufnahme-Liste auf und ließ
ihre Loader mit einem Wächter (`if(!$('#…')) return;`) stehen. Was dabei
unterging: drei Endpunkte verloren ihre einzige Oberfläche, während sie im
Backend die ganze Zeit weiterliefen.

* **Papierkorb** — das gefährlichste der drei. Eine Aufnahme wegzuwerfen ging
  weiter (`trashRec` im Aufnahme-Fenster), sie anzusehen oder zurückzuholen
  nicht: `/api/recordings/trash` und `/api/recordings/<id>/restore` hatten
  keinen einzigen Aufrufer mehr. Wegwerfen ohne Zurückholen ist die
  gefährlichere Hälfte. Liegt jetzt als vierte Kachel in den
  Speicher-Werkzeugen, mit Bestand und Größe direkt auf der Kachel.
* **Dubletten im Archiv** — `rtDedup()` zählt sie nur; die Oberfläche zum
  Ansehen und Löschen (`/api/archive/duplicates`, `…/delete`) war weg. Hängt
  jetzt am Archiv-Panel, Knopf „⊟ Dubletten".
* **Umbenennen** — `/api/archive/<id>/rename` benennt die echte Datei um und
  hatte gar keinen Aufrufer. Jetzt ein ✎ je Archiv-Zeile.

Beim Wiederbeleben gleich zwei Altlasten mitgenommen: der Dateipfad ging über
`esc()` plus naives Quote-Ersetzen in einen `onclick` — genau das Muster, das
W118 mit `escJs()` geschlossen hat; ein Apostroph im Dateinamen hätte den
String beendet. Und „3072.0 MB verschwendet" heißt jetzt „3.0 GB doppelt
belegt".

Ersatzlos entfallen, weil das Archiv-Panel und die Aufnahme-Werkzeuge dasselbe
können: `loadVault`, `vaultDelete`, `loadManual`, `stopManual`.

Geprüft im echten Browser (Chromium, Template gegen eine gestubbte API):
15 Schritte grün — Kachel, Fenster, Wiederherstellen, Umbenennen mit
Apostroph im Namen, Dubletten löschen, keine Konsolenfehler. Der Vertrag
`test_v40_w125_papierkorb_und_archiv_werkzeuge` hält Markup **und**
Verdrahtung fest.

Was der Reorg sonst noch abgehängt hat, ist damit nicht erledigt — ohne
Oberfläche laufen weiter: Auto-Archiv-Regeln, Webhooks, Sammlungen,
KI-Konversationen, Evolutions-Status/-Vorschläge und geplante Aufnahmen.

### Behoben — Offline-Meldungen landeten weiter im Hauptchat (W124)

Das Melde-Thema aus W121 wirkte nur halb: LIVE ging hinein, OFFLINE weiter
in den Hauptchannel. Grund war nicht der Sendeweg, sondern dass es **zwei**
Sender für die Offline-Meldung gibt, beide über
`claim_live_transition(going_live=False)` serialisiert:

* der Live-Check-Worker in `_handle_single_tracking` — der war in W121
  umgestellt und wurde auch als einziger geprüft,
* der Fan-Out am **Ende der Aufnahme** in `handle_recording_finished` — der
  war es nicht.

Der zweite gewinnt den Anspruch praktisch immer: die Aufnahme endet in
derselben Sekunde, in der der Stream stirbt, während der Live-Check erst
~30 s später pollt. Damit ging real jede Offline-Meldung über den einfachen
Sendeweg ohne `message_thread_id` — also in den Hauptchat. Jetzt nutzen
beide Sender `_send_live_notice`.

Am selben Ort lag ein zweiter Fehler derselben Ursache: **F63 (Quiet Hours)**
prüfte nur der Live-Check-Worker. Weil der andere Sender feuerte, kam nachts
genau der Fall, den F63 verhindern soll — OFFLINE ohne vorheriges LIVE. Der
Anspruch wird weiterhin geltend gemacht (er setzt `last_live`), nur die
Meldung entfällt.

Neuer Vertrag `test_v40_w124_offline_meldung_ins_thema` hält **beide** Sender
fest, statt wie W121 nur einen.

### Behoben — zwei Dauerläufer verschluckten ihre Fehler (W124)

Verstoß gegen die eigene Regel „jeder Dauerläufer gehört auf `_loop_fehler`,
nie auf `log.debug` und nie auf `pass`":

* `_intel_index_loop` (Archiv-Indexer/Transkription) meldete auf `log.debug`.
  Fällt Whisper aus, ist die DB gesperrt oder die Platte voll, transkribiert
  er nie wieder — und in einem ERROR-Log steht dazu keine Zeile.
* `_scheduler_loop` schrieb `last_run_date` in einem stillen `except: pass`.
  Schlägt das UPDATE fehl, gilt die Aufgabe als nie gelaufen und feuert alle
  30 s den ganzen Tag erneut, lautlos.

### Entfernt — Rest der 2D-Angriffskarte (W124)

`ncGratG()` (das Gradnetz) und die Regel `.wm-grat` blieben stehen, als W71
`ncDefenseMap` entfernte. Die Funktion hatte danach keinen einzigen Aufrufer
mehr — sie war die einzige nie aufgerufene der 488 Dashboard-Funktionen.

### Behoben — README rendert nicht mehr, Kennzahlen waren veraltet (W123)

GitHub meldete am Lebenszyklus-Diagramm „Unable to render rich display /
Cannot read properties of undefined (reading 'render')". Es war der einzige
Block, der kein `flowchart` war: `stateDiagram-v2` wird von GitHubs Renderer
als eigener Chunk nachgeladen. Jetzt ein `flowchart TD` mit identischem
Inhalt; zusätzlich raus, was in älteren Renderern stolpert — `<b>`-Tags in
Labels und die Klasse `in`. Alle vier Blöcke gegen mermaid 9.4.3, 10.9.3 und
11 in echtem Chromium gerendert.

Dazu die Zahlen, die still auseinandergelaufen waren: **355 Routen** (265 in
`bot.py`, 90 in `nc/routes/`) statt 345, **32.569 Zeilen** statt 34.487,
**89** `nc`-Module statt 84, **10** `brain`-Module statt 11, **13**
Sentinel-Agenten statt 12 — `swap` und `proxy` fehlten in der Tabelle ganz —,
**~495** `.env`-Variablen statt ~470, **29** Telegram-Befehle statt 28
(`/update` war nirgends dokumentiert). `CLAUDE.md` trug dieselbe Drift, teils
noch älter, und behauptete „Kein Git-Repo".

Zwei Badges zeigten ins Leere: der Discord-Badge auf eine Überschrift in
`<summary><h3>`, für die GitHub keine ID vergibt, der Telegram-Badge auf einen
Anker ohne den Variation Selector, der im Emoji der Überschrift steckt.

### Hinzugefügt — `ncpatch docs`, der Zahlenwächter (W123)

    python3 tools/ncpatch.py docs

Vergleicht die Kennzahlen in `README.md`, `CLAUDE.md` und den ausgelagerten
Doku-Dateien mit dem Quelltext: Routen, Slash-Commands, Top-Level-Funktionen,
Zeilen in `bot.py`, Module, Blueprints, Sentinel-Agenten, Telegram-Befehle,
`.env`-Variablen. Prüft zusätzlich jeden internen Anker gegen GitHubs
Slug-Regel und die Befehlslisten **namentlich** — wer einen 46. Slash-Command
hinzufügt und brav „46" schreibt, ohne den Namen einzutragen, käme durch eine
reine Zählprüfung.

Bewusst **nicht** Teil von `ncpatch check`: `check` läuft in `deploy.sh` vor
dem Umschwenken auf Produktion, und eine veraltete Zahl im README darf keinen
Deploy aufhalten. Stattdessen neuer CI-Job `doku`.

### Geändert — README von 1.116 auf 946 Zeilen (W123)

Referenzmaterial raus aus dem Einstiegsdokument, Verweise rein:
[`INSTALL.md`](INSTALL.md) (Installation von Hand, fünf Schritte),
[`TROUBLESHOOTING.md`](TROUBLESHOOTING.md) (Störungsbilder und ihre echten
Ursachen) und [`ROADMAP.md`](ROADMAP.md) (die sechs Wellen der Zerlegung).
Im README bleibt, was die Entscheidung trägt: Schnellstart, Voraussetzungen,
der `selftest`-Aufruf und die Messlatte der Zerlegung. Das
Inhaltsverzeichnis war unvollständig und listet jetzt alle Abschnitte.

### Behoben — Im Dashboard hinzugefügte Streamer zählten nirgends (W120)

Ein im Dashboard angelegter Streamer tauchte weder als live noch als Creator
noch sonstwo auf. Drei getrennte Ursachen, die zusammen dasselbe Bild ergaben.

- **Die Zielgruppe.** Der einzige Weg war der Bulk-Add tief in der
  Trackings-Verwaltung, mit Pflichtfeld `group_id`. Leer gelassen brach die
  Route mit „group_id fehlt" ab — das Tracking entstand nie. Geraten landete
  es in einem Chat, den es nicht gibt: kein Live-Ping, kein Discord-Post.
  Beides sah für den Betreiber gleich aus. `group_id` ist jetzt optional;
  `_dashboard_track_group()` löst sie auf (`DASHBOARD_TRACK_GROUP_ID`,
  `DAILY_SUMMARY_CHAT_ID`, meistgenutzte Gruppe aus `trackings`,
  `DISCORD_TRACK_GROUP_ID`, `DISCORD_GUILD_ID`, einzelner
  `ALLOWED_CHAT_IDS`-Eintrag). Ist keine auflösbar, nennt die Antwort die zu
  setzende Variable im Klartext.
- **Neu:** `GET /api/trackings/groups` (bekannte Gruppen samt Belegung) und
  ein Feld **„+ TRACKEN"** direkt an der Monitor-Wand — Name rein, fertig.
- **Die Kachel „Creator"** zeigte `unique_users`, also `DISTINCT
  telegram_user_id` aus `tiktok_checks`: die Konten, die je `/check` getippt
  haben. Ein neu getrackter Streamer konnte diese Zahl nie bewegen.
  `/api/stats` liefert jetzt `creators` (`DISTINCT username` aus `trackings`).
- **Groß-/Kleinschreibung.** `clean_username` schreibt nicht klein, die
  `trackings` speichern den Handle also wie getippt. `/api/streamer/detail`,
  `/api/stream/timeline` und `/api/restream/report` schrieben ihn stur klein —
  bei jedem Handle mit Großbuchstaben traf keine Abfrage: OFFLINE, 0
  Aufnahmen, leere Timeline, während gesendet wurde. Jetzt löst
  `_resolve_tracked_user()` die gespeicherte Schreibweise auf, die Abfragen
  laufen über `LOWER(...)` (SQLite wie MariaDB), Laufzeit-Dicts über
  `_ci_key()`.

### Behoben — OAuth hinter dem Proxy, Google-Abmeldung, Melde-Thema (W121)

- **YouTube-OAuth lief nicht über den Reverse-Proxy.** Kick konnte seine
  Rückruf-Adresse im Dashboard setzen; Twitch und YouTube hatten nur `.env`
  und sonst fest `http://localhost:3000` — eine Adresse, die von außen niemand
  sieht. Google bricht damit mit `redirect_uri_mismatch` ab, **bevor** die
  Kontoauswahl erscheint; weil der Flow nie durchlief, erschien auch nie der
  Trennen-Knopf. Eine falsche Adresse, drei Symptome.
  Neu `_public_base_url()` (Vorrang `PUBLIC_BASE_URL`, sonst Proxy-Header —
  aber nur von einem vertrauten Absender, sonst wäre die Rückruf-Adresse per
  Header fälschbar; fehlt der Port im Host, ergänzt `X-Forwarded-Port` ihn)
  und `_oauth_redirect_uri()` für alle drei Plattformen: app_config, dann
  `.env`, dann diese Adresse. Dazu `POST /api/youtube/oauth/redirect` und
  `POST /api/twitch/oauth/redirect` zum Live-Setzen samt Feld im Panel.
- **Google-Abmeldung.** `forget()` löschte nur lokal — die Freigabe im
  Google-Konto blieb, ein Kontowechsel war nur über `myaccount.google.com`
  möglich. `nc/ytoauth.py` bekommt `revoke()` (Widerruf beim Google-Endpunkt,
  lokaler Zustand **immer** geleert, auch bei Netzfehler) und
  `POST /api/youtube/oauth/logout`. Im Panel „Von Google abmelden" und „Konto
  wechseln", auch sichtbar, wenn noch nie verbunden wurde. Der Start-Aufruf
  gibt `prompt=select_account consent` jetzt ausdrücklich mit.
- **Der Befund „Kick-Key-Kollision" war nicht mehr wahr.** Seit der
  symmetrischen Zielauflösung (W77) ist die Zielliste global; das verglichene
  Feld `kick_url` ist nur noch „die erste konfigurierte Plattform" und bei
  jedem Restream gleich. Wer eine Quelle auf drei Plattformen ausspielt, bekam
  den Befund im Zwei-Minuten-Takt — ohne Plattform, ohne Quelle, mit einem
  Rat, der zur `.env`-Konfiguration nicht mehr passt. Jetzt werden alle Ziele
  je Prozess verglichen, nur lebende Prozesse gezählt, `RESTREAM_SINGLE`
  berücksichtigt, und der Befund nennt Plattform, Restream-Nummern und
  Quellen — zwei Zeilen derselben Quelle sind ein anderer Fall als zwei
  Quellen auf einem Key.
- **Live-/Offline-Meldungen gingen in den Hauptchannel.** Ist die Gruppe ein
  Forum, legt der Bot jetzt ein eigenes Thema an
  (`TELEGRAM_NOTIFY_TOPIC_NAME`, Standard „📡 Live & Offline") und meldet nur
  dorthin. Wird das Thema gelöscht, antwortet Telegram mit „message thread not
  found" — dann Zuordnung verwerfen, Thema neu anlegen, einmal wiederholen.
  Der Hauptchannel ist bewusst kein Rückfall; scheitert auch das, sagt eine
  Fehlerzeile warum. Ohne Forum gibt es keine Themen — dort bleibt es beim
  Chat.

### Behoben — Trackings-Ansicht hatte kein Markup mehr (W122)

Die Logik lief die ganze Zeit weiter (`loadSurveil`, `renderTargetGrid`,
`renderBandwidth`, `loadHeatmap`), nur ihr HTML war verschwunden: alle elf IDs
kamen im Template **null** mal vor, die Funktionen brachen an ihrem eigenen
Wächter ab. Damit waren **Tags, Notizen, Priorität, Schnell-Neustart und
Jetzt-Prüfen** aus dem Dashboard nicht mehr erreichbar — ein getrackter
Streamer war nur noch eine Kachel.

- Panel wieder im Streams-Tab unter der Monitor-Wand: vier Kennzahlen, Filter
  über Name und Notiz, Sortierung nach Status/Name/VIP, Tabelle mit
  Status/Tags/Notiz, laufende Aufnahmen mit Rate, 30-Tage-Karte. Keine Zeile
  Logik geändert, nur das fehlende Markup und die Verdrahtung im Loader.
- Die Heatmap bekommt eine Drossel (5 Minuten) — sie deckt 30 Tage ab und wäre
  sonst im 8-Sekunden-Takt der Tabelle mitgelaufen.
- Texte der Ansicht auf Deutsch (war `TARGET`/`SCAN`/`CTL`/`NO TARGETS`).

#### Entfernt
- **Radar-Anzeige.** Sie hing an einem Canvas, das es im Template nicht mehr
  gibt: `_radarRAF`/`_radarAngle` wurden nie wieder gelesen,
  `radarUpdateStats()` schrieb in fünf IDs, die nirgends existierten.
- Die feste Server-IP aus den Tunnel-Kästen des Dashboards.

### Geändert — `bot_v37.py` heißt jetzt `bot.py` (W119)

Die Versionsnummer im Dateinamen war seit v4.0 falsch und stiftete bei jedem
Blick in die Ablage Zweifel, ob die Datei noch die aktuelle ist. Der Name sagt
jetzt nur noch, was die Datei ist.

- Alle 448 Verweise nachgezogen: Tests, `tools/`, CI, Patch-Dateien,
  `.gitattributes`, Skills und Dokumentation.
- Der Architektur-Wächter in `test_nc_modules.py` prüft den Rückimport aus dem
  Monolithen jetzt auf `bot` **exakt oder als Paket-Präfix** `bot.`. Ein
  `startswith("bot")` hätte künftig jedes Modul getroffen, dessen Name so
  beginnt.
- Der Vertrag für `nc.updater` prüft denselben Rückimport über den AST statt
  über eine Textsuche — „bot" steckt seit der Umbenennung in jedem zweiten
  Wort des Moduls („bot-frei") und wäre ein Dauer-Fehlalarm.

### Geändert — Wurzelverzeichnis aufgeräumt (W119)

Elf Textdateien lagen in der Wurzel und verdeckten, was dort tatsächlich zum
Betrieb gehört. Sie liegen jetzt unter [`docs/`](.), mit
[`docs/README.md`](README.md) als Wegweiser.

- Verschoben: `CHANGELOG.md`, `CODE_OF_CONDUCT.md`, `CONTRIBUTING.md`,
  `DEPLOY.md`, `README_V37.md`, `SECURITY.md`, die drei `SETUP_*`-Anleitungen,
  `START_HIER.txt`, `THIRD_PARTY_LICENSES.md`. GitHub erkennt
  Verhaltenskodex, Beitragsleitfaden und Sicherheitshinweis auch unter `docs/`.
- In der Wurzel geblieben, weil dort gebraucht: `README.md` (Einstieg),
  `LICENSE` (Lizenzerkennung von GitHub), `requirements.txt`
  (`pip install -r`), `.env.example` (schreibt `tools/gen_env_example.py`
  dorthin), `llama-server.service` (systemd-Einheit) und `CLAUDE.md` —
  **letztere zwingend**, sonst findet Claude Code die Arbeitsgrundlage nicht.
- Alle Querverweise nachgezogen: relative Links aus `docs/` nach oben
  (`../nc/version.py`), die Hinweise in den Fehlermeldungen des Bots
  (`docs/SETUP_YT_OAUTH.md`), GitHub-Vorlagen, CI und der Website-Text.
- `tools/build_release.py` zählt die Anleitungen nicht mehr einzeln auf — sie
  kommen über den `docs`-Ordner mit. Sonst wären sie doppelt im Archiv
  gelandet und jede Umbenennung hätte ein `FEHLT:` ins Protokoll geschrieben.

### Hinzugefügt — Selbst-Update aus dem Repo (W115)

Der Bestand lässt sich jetzt aus dem GitHub-Repo aktualisieren, ohne den Umweg
über ein ZIP von Hand. Die Entscheidungslogik liegt bot-frei und geprüft in
[`nc/updater.py`](../nc/updater.py).

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
geprüft in [`nc/restream_stability.py`](../nc/restream_stability.py).

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
  von [`tools/stempel_assets.py`](../tools/stempel_assets.py), geprüft im
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
  [`nc/flapguard.py`](../nc/flapguard.py) meldet erst, wenn vier Trennungen in eine
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
Datenschutz) aus einer Quelle: [`website/raum.css`](../website/raum.css) und
[`website/raum.js`](../website/raum.js). Dependency-frei wie der Rest der
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

## [4.1] — 2026-08 · „Öffentliche Stimme"

### Geändert — Website-News sind Meldungen, keine Statuszeilen (Welle 1)

Bis v4.0 war eine News auf lafap.de **ein Satz**. Für einen Erstbesucher stand
dort nichts, was ihn bleiben ließ, und für eine Suchmaschine waren es rund 30
Wörter pro Eintrag. Ein Item trägt jetzt fünf Felder statt einem:

| Feld | Inhalt |
|---|---|
| `lead` | Anreißer-Satz, der auch allein steht |
| `body` | Fließtext in **mehreren Absätzen** (durch Leerzeile getrennt) |
| `metrics` | `[{label, value}]` — die harten Zahlen als Kennzahlen-Leiste |
| `bullets` | Detailpunkte, die im Fließtext nur bremsen würden |
| `tags` | Themen-Chips |

Alle neuen Felder sind **optional**: eine bestehende `news.json` mit alten
Einträgen rendert unverändert weiter, statt leere Kästen zu hinterlassen.

Damit es überhaupt etwas zu erzählen gibt, sammelt `_news_facts()` ein
Wochenbild ein — Sendungen, verschiedene Creator und aktive Tage der letzten
sieben Tage, eingerichtete Sende-Ziele, Moderations-Eingriffe, Chat-Antworten
und der Zuwachs des Wissensspeichers. Die Zeitfenster werden in Python
berechnet und als Parameter gebunden; `datetime('now', …)` gibt es auf MariaDB
nicht.

Drei Dinge, die für den Betrieb zählen:

- **Die KI formuliert nur den Fließtext.** `lead`, `metrics`, `bullets` und
  `tags` entstehen ausschließlich aus echten Fakten — eine halluzinierte Zahl
  kann so gar nicht erst in eine Kennzahl geraten. Der Prompt fordert jetzt
  drei Absätze statt „1-2 Sätze"; `_news_absaetze()` normalisiert die Antwort,
  weil der Renderer an Leerzeilen trennt.
- **Fehlende Fakten verschwinden, sie werden nie zur 0.** Beim Praxislauf
  zerbrachen zwei Sätze, sobald eine Zahl fehlte („Jeder von **ihnen**" ohne
  Bezug, ein Absatz der klein anfing). Die Texte werden jetzt satzweise
  zusammengesetzt, und ein Vertrag spielt Teilmengen der Fakten durch.
- **Öffentliche Texte in korrektem Deutsch.** Die News gingen bisher mit
  `ae/oe/ue`-Umschrift auf eine deutsche Seite („Waechter", „Kanaele").

Dazu: die Kennzahlen-Leiste liegt auf Flex statt Grid — bei fünf Zahlen auf
drei Spalten blieb auf dem Handy eine leere Geisterkachel stehen. Und die
Dashboard-Vorschau zeigt vor dem Veröffentlichen, welche Zahlen nach außen
gehen; vorher stand dort nur der Body.

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
