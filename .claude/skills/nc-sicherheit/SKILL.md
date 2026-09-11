---
name: nc-sicherheit
description: Sicherheit in NIGHTCRAWLER — was nie nach aussen darf (.env mit 519 Variablen, Cookies, OAuth-Tokens, Stream-Keys), die vorhandenen Riegel und wie man sie NICHT umgeht: Redact-Pfad beim ffmpeg-Logging, nc.sicherpfad gegen Pfad-Ausbruch, _fehler_text fuer API-Antworten, dashauth fuer das offene Deck, die CodeQL-Barriere, die Hash-Kette des Ledgers. Nutze dies bei jeder Aenderung an Kommandozeilen, Datei-Pfaden aus Nutzereingabe, API-Fehlerantworten, Dashboard-Zugang, Cookie-Handling oder vor einem Release. Trigger: Sicherheit, Secret, Token, Key, Cookie, Redact, Pfad-Ausbruch, path traversal, CodeQL, Leak, .env, Ledger, Audit, Exposition, sanitize.
---

# NIGHTCRAWLER — Sicherheit

## Die Lage, aus der alles folgt

Diese Box nimmt fremde Livestreams auf, hält Sendeschlüssel für vier
Plattformen und ein Dashboard mit 361 Routen — darunter Konfigurations-
Wiederherstellung, Log-Auszug und Dateidownload. Ein Leck ist hier nicht „eine
Zeile im Log zu viel", sondern der Übernahme-Schlüssel für fremde Kanäle.

Die `.env` trägt **521 Variablen**: Cookies, OAuth-Tokens, Stream-Keys,
API-Schlüssel. Sie liegt **nie** im Auslieferungsarchiv, wird **nie** ausgegeben
und **nie** in eine Fehlermeldung geschrieben. `.env.example` fährt mit — andere
Datei, nur Namen, keine Werte.

## Die Riegel sind gebaut. Der Fehler ist, sie zu umgehen

Für jedes wiederkehrende Problem existiert genau eine Stelle. Eine zweite
Lösung danebenzustellen ist der eigentliche Fehler — dann sind es zwei
Wahrheiten, und eine davon veraltet.

| Gefahr | Der eine Riegel |
|---|---|
| Stream-Keys/Cookies im Log | `nc/logsafe.py::redact_stream_urls`, `nc/ffdiag.py::redact_cmd_for_log` |
| Pfad-Ausbruch aus Nutzereingabe | `nc/sicherpfad.py` — `sicherer_name`, `unter`, `sicher_join`, `pruefe_unter` |
| Roher Ausnahmetext in einer API-Antwort | `_fehler_text(e, wo)` in `bot.py` |
| Offenes Dashboard ohne Token und PIN | `nc/dashauth.py::lage()` |
| Nachträglich geänderte Auszahlung | Hash-Kette in `nc/ledger.py` |

### ffmpeg- und streamlink-Kommandos

Beim Logging werden Cookie-Header und Stream-URLs redacted (F4). **Wer die
Kommandozeile ändert, prüft, ob sein neues Argument noch durch den Redact-Pfad
läuft.** Ein Key landet sonst im Klartext in `error.log` — und das Log geht bei
jeder Störungsmeldung mit.

### Pfade aus Nutzereingabe

`nc/sicherpfad.py` entstand, weil die Riegel schon überall **da** waren — jeder
in einer anderen Form (`startswith`, `basename`, Regex, Erlaubnisliste, festes
Dict). CodeQL meldete 241 Befunde, und keiner ließ sich billig prüfen. Ein
neuer Pfad-Riegel gehört deshalb nicht neu geschrieben, sondern importiert.

### Fehlermeldungen nach außen

`_fehler_text(e, wo)` gibt dem Aufrufer eine Klasse, nicht den Wortlaut. Der
volle Text bleibt im Log, wo er für den Betreiber steht. Ein nacktes
`str(e)` in einer `jsonify(...)`-Antwort trägt Dateipfade, SQL und manchmal
Zugangsdaten nach außen — 22 solcher Stellen sind in v4.2 W3 nachträglich
geschlossen worden, nachdem die erste Runde sie durchgelassen hatte.

## Das Dashboard

Bindung ist `127.0.0.1:8050`. Zugriff läuft über SSH-Tunnel:

    ssh -L 3000:localhost:8050 ubuntu@<server-ip>

**Den Port „für den einfachen Zugriff" zu öffnen ist kein Komfort, sondern
eine Übernahme.** 361 Routen, darunter Konfigurations-Wiederherstellung,
Log-Auszug und Dateidownload.

`DASHBOARD_TOKEN` **oder** `DASHBOARD_PIN` reicht als Schutz. Fehlen beide,
meldet `dashauth.lage()` das alle sechs Stunden auf Fehler-Ebene — nicht nur
einmal beim Start, weil eine Startmeldung niemand liest, der das Bootlog nicht
aufhebt.

**Warum nicht schärfer:** die Warnung fragte früher nur nach dem Token. Ein
PIN-geschütztes Deck löste sie fälschlich aus — und ein Fehlalarm erzieht dazu,
die Meldung zu überlesen. Das ist schlimmer als keine Meldung. Dieselbe
Überlegung gilt für jede neue Warnung, die hier eingebaut wird.

## Geld — die Hash-Kette ist kein Schmuck

`nc/ledger.py` sind gebuchte **Auszahlungen** für die Steuer, append-only mit
`prev_hash`/`row_hash`. Eine Korrektur ist eine **Gegenbuchung**, nie ein
`UPDATE`. Wer einen Ledger-Eintrag nachträglich ändert, bricht die Kette und
macht die gesamte Historie unbeweisbar.

Nicht vermischen: `/api/donations/summary` ist Live-Telemetrie aus
**Schätzwerten**. Anzeigewert ≠ Auszahlung ≠ Zuflusszeitpunkt.

## CodeQL

Der Lauf ist scharf und die Zahl wird per Vertrag festgehalten
(`test_v41_w10_codeql_befunde`). Sanitizer-Funktionen sind über
`.github/codeql/NcSanitizer.qll` als **Barriere** deklariert — deshalb zählt
CodeQL 43 statt 242 Befunde, ohne dass eine Prüfung entfernt wurde.

**Wer eine Barriere-Funktion umbenennt oder ihre Rückgabe ändert, hebt die
Barriere auf** — der nächste Lauf meldet dann hunderte Befunde, die vorher
begründet stumm waren. Bei Änderungen an `nc/cookieholen.py`, `nc/sicherpfad.py`
oder `nc/logsafe.py` also zuerst in `.github/codeql/` nachsehen.

Neue Befunde werden **behoben oder begründet** — nie durch Anheben der
Vertragszahl weggedrückt.

## Vor dem Ausliefern

Das Bau-Skript prüft selbst (seit v4.2-W36):

1. **Nichts Geheimes** — kein Treffer auf `.env`, `.sqlite`, `.pem`, `.key`.
2. **Kein Import ins Leere** — jeder importierte Wurzel-Modulname muss im
   Archiv sein, sonst stirbt er zur Laufzeit in einem breiten `except`.
3. **Compiliert wirklich** — jede `.py` aus dem *entpackten* Archiv.

Dazu der CI-Job `Kein Geheimnis im Diff` bei jedem Push.

## Wenn doch etwas abgeflossen ist

Reihenfolge, nicht Reihenfolge egal:

1. **Schlüssel drehen**, bevor irgendetwas anderes passiert — Stream-Keys in
   den Kanal-Dashboards, OAuth-Tokens widerrufen, Cookies neu holen.
2. Erst danach aufräumen: `.env` korrigieren, Dienst neu starten.
3. Logs prüfen, wie lange der Wert dort stand, und ob das Log geteilt wurde.

Ein rotierter Schlüssel ist sofort wertlos. Ein Log zu löschen, ohne den
Schlüssel zu drehen, ist Kosmetik.
