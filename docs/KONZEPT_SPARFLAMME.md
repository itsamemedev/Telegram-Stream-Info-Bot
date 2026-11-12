# Konzept „Sparflamme" — Stabilität und Ressourcen (v5.2.0, W191)

> Stand 2026-11-12. Erst gemessen, dann gebaut. Jede Maßnahme hat einen
> Ausweg per `.env` und einen Vertrag mit Mutationsprobe.

## Ausgangslage

Die Box ist eine 8-Kern-Maschine, auf der gleichzeitig Aufnahmen (ffmpeg),
Restream-Transcodes, Whisper, ein 14B-LLM (ik_llama.cpp, ~9 GB) und der
Python-Monolith laufen. W170 und W183 haben gezeigt: Engpass ist CPU-Zeit und
Speicher, und jede Verzögerung im Python-Teil wird an Aufnahme und Restream
weitergereicht. Die großen Brocken (ffmpeg, Whisper, LLM) sind seit W108/W170/
W181 gedrosselt und gedeckelt. Übrig ist der Grundumsatz des Bots selbst.

## Messungen

| Messpunkt | Befund |
|---|---|
| `db_conn()` (SQLite) | **180 µs** je Aufruf: neue Verbindung, 5 PRAGMAs, Schema neu einlesen. Wiederverwendet: **2 µs**. Rund 210 Aufrufstellen, darunter Overlay (je Client alle 2,5 s, 5 Abfragen), Live-Prüfung je Tracking, `/healthz`, jede Deck-Kachel. Der 8-MB-Seiten-Cache (`cache_size=-8000`) wird mit jeder Verbindung verworfen — er wird **nie warm**. |
| glibc-Arenen | Der Bot hat 21+ Threads (Worker, waitress, Whisper, to_thread-Pool). glibc legt bis zu 8 × Kerne Arenen an (hier 64) und gibt freigegebenen Speicher aus ihnen kaum zurück. Das typische Bild: RSS steigt nach Spitzen (Whisper-Lauf, große JSON-Antworten, W180) und fällt nie wieder. |

## Maßnahmen

### A. SQLite-Verbindungsvorrat (`nc/dbwrap.py`)

Bis zu `DB_VORRAT` (Vorgabe 4) freie Verbindungen werden aufgehoben und beim
nächsten `db_conn()` wiederverwendet. Pragmas werden nur beim Öffnen gesetzt.

Sicherungen, jede aus einer Lehre dieses Bestands:

1. **Datei getauscht → Verbindung weg.** Jede Verbindung merkt sich
   `(st_dev, st_ino)` der Datei beim Öffnen. Passt das beim Herausgeben nicht
   mehr (Wiederherstellung, `dbkopf`, Handtausch), wird sie geschlossen und
   neu geöffnet. Ohne das hielte der Vorrat die alte Datei am Inode fest —
   genau die Falle aus W96, nur dauerhaft.
2. **Pfad gewechselt → Verbindung weg** (`configure_db`, Testsuiten).
3. **Nie mit offener Transaktion zurück.** Beim Zurücklegen `in_transaction`
   prüfen und zurückrollen; scheitert das, wird die Verbindung geschlossen.
4. **Nach dem `with` ist die Hülle tot.** Bisher schloss `__exit__` die
   Verbindung, ein späterer Zugriff warf `ProgrammingError`. Mit Vorrat würde
   derselbe Zugriff still auf einer Verbindung arbeiten, die schon ein anderer
   Thread benutzt. Die Hülle zeigt nach dem Verlassen auf einen Platzhalter,
   der genauso wirft wie vorher.
5. **Gedeckelt.** Mehr gleichzeitige Nutzer als `DB_VORRAT` bekommen eine
   eigene Verbindung, die beim Verlassen geschlossen wird. Kein Wachstum mit
   der Thread-Zahl, höchstens `DB_VORRAT` × 8 MB Cache.
6. **Verschachtelung bleibt getrennt.** Ein `with db_conn()` innerhalb eines
   anderen bekommt eine andere Verbindung — eine Thread-lokale Einzel-
   verbindung hätte die innere Transaktion die äußere committen lassen.
7. `DB_VORRAT=0` stellt das alte Verhalten wieder her. `DB_` ist geschützt —
   nicht aus dem Deck setzbar (Bootstrap der Datenbank).

MariaDB bleibt unverändert (eigener Verbindungsaufbau, eigene Lebensdauer).

### B. Speicher zurückgeben (neu: `nc/heapzaum.py`)

* Beim Start, **bevor** Threads entstehen: `mallopt(M_ARENA_MAX, 2)` über
  `ctypes` — nur glibc/Linux, sonst still übersprungen mit Grund in
  `/healthz`. Ausweg `SPEICHER_ARENEN=0` (glibc-Vorgabe), Wert einstellbar.
* Periodisch im Watchdog-Takt (`SPEICHER_TRIM_MIN`, Vorgabe 10) `malloc_trim(0)`: gibt freie Seiten ans System
  zurück. Gemessen wird RSS davor/danach; der Gewinn steht in `/healthz`
  (`heap`), große Gewinne als INFO.
* Läuft im Thread (`asyncio.to_thread`) — `malloc_trim` kann bei großem Heap
  einige Millisekunden dauern, der Event-Loop wartet darauf nicht (W97).

### C. Installer und `update.sh`

* Installer: `.nc_sitzung.key` nicht mitkopieren (erledigt in v5.1.1, W190).
* **Kein `MALLOC_ARENA_MAX` in der systemd-Unit** — nach der Messung
  verworfen. Der In-Prozess-Weg (B) wirkt für alle drei Auslieferungswege
  (Installer, ZIP, Update-Funktion), ohne dass jemand die Unit anfasst; eine
  Unit-Variable würde dagegen `SPEICHER_ARENEN` stumm überstimmen — zwei
  Schalter für eine Sache, und der Ausweg `SPEICHER_ARENEN=0` wirkte nicht.
  `update.sh` fasst Dienste nach seiner eigenen Regel nicht an; die neuen
  Variablen kommen über `.env.example`.

## Nicht gemacht (bewusst)

* **Overlay-Antwort zwischenspeichern:** bei 2,5 s Abfragetakt und wenigen
  Clients deckt sich der Nutzen mit A; ein Cache davor wäre eine zweite
  Wahrheit über Spendenstände.
* **OOMScoreAdjust/MemoryHigh für den Bot:** ohne Messung an der echten Box
  würde das raten, wen der Kernel opfert — Aufnahmen hängen am Bot.
* **`cache_size` erhöhen:** erst messen, wenn der Vorrat warm ist.

## Ergebnis der Umsetzung

* A: Vertrag `_test_v52_w191_db_vorrat` — 11 Aussagen, darunter Tausch,
  Pfadwechsel, offene Transaktion, Fehler, Deckel, 8 Threads × 150 Zugriffe,
  Ersparnis als Verhältnis (mindestens Faktor 3; gemessen rund 90).
* B: gemessen mit 8 Threads und fragmentierter Last: RSS nach dem Freigeben
  **861 MB** (glibc-Vorgabe) gegen **539 MB** (zwei Arenen); nach
  `malloc_trim` je rund **105 MB**. Der Vertrag misst die Rückgabe in einem
  eigenen Prozess.
* 19 Mutationsproben gefangen; eine entwischte zuerst (der Pfad-Riegel beim
  Zurücklegen war ungedeckt) und hat einen Vertragsfall bekommen.

## Abnahme

* Vertrag `_test_v52_w191_*` je Maßnahme, Mutationsproben je Sicherung.
* Gesamte Prüfkette grün, `ueberdeckung --sperre` ohne neue ungeprüfte
  Anweisungen.
* Gemessen: `db_conn()`-Kosten vorher/nachher im Vertrag (nicht als
  Zeitgrenze, sondern als Verhältnis — Zeitgrenzen sind in der CI flatterhaft).

## Nachtrag 5.2.1 — MariaDB

Maßnahme A galt nur für SQLite; der Betrieb läuft auf MariaDB. Dort nimmt
`db_conn()` einen eigenen Pool, und gemessen (MariaDB 10.11) kostete ein
Zugriff 233 µs, davon drei unnötige Rundreisen: `ping` bei jedem Ausleihen,
`commit`, und ein `rollback` nach erfolgreichem `commit`. 5.2.1 pingt nur nach
Leerlauf, lässt das `rollback` weg (rund 130 µs) und wiederholt die erste
Anweisung einmal, wenn die Verbindung abgerissen ist — ein Server-Neustart
kostet damit keinen Aufruf. Details: `docs/CHANGELOG.md`, Abschnitt 5.2.1.
