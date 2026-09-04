# Mitwirken an NIGHTCRAWLER

> 🌐 **Deutsch** · [English](en/CONTRIBUTING.md)

Danke, dass du beitragen willst. Dieses Projekt läuft produktiv im Dauerbetrieb —
ein Deploy geht direkt gegen Produktion. Die Regeln hier sind deshalb keine
Stilfragen, sondern aus echten Ausfällen entstanden.

---

## Inhalt

- [Entwicklungsumgebung](#entwicklungsumgebung)
- [Die Pflicht-Prüfkette](#die-pflicht-prüfkette)
- [Architektur-Regeln](#architektur-regeln)
- [Navigation im Monolithen](#navigation-im-monolithen)
- [Code-Stil](#code-stil)
- [Fallstricke, die schon zugeschlagen haben](#fallstricke-die-schon-zugeschlagen-haben)
- [Commits und Pull Requests](#commits-und-pull-requests)
- [Bug-Reports](#bug-reports)
- [Lizenz deiner Beiträge](#lizenz-deiner-beiträge)

---

## Entwicklungsumgebung

```bash
git clone https://github.com/itsamemedev/Telegram-Stream-Info-Bot.git
cd Telegram-Stream-Info-Bot

python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
pip install pyflakes ruff            # Prüfwerkzeuge

cp .env.example .env                 # anpassen
```

Systempakete (nicht über pip): `ffmpeg`, `streamlink`, `yt-dlp`.

**Auf Windows:** Der Interpreter heißt dort `python`, nicht `python3`. Setze
vorher `$env:PYTHONUTF8="1"` — die Tests öffnen `bot.py` ohne `encoding=`,
ohne UTF-8-Modus greift cp1252 und sie sterben mit `UnicodeDecodeError`, statt
zu prüfen.

---

## Die Pflicht-Prüfkette

**Sie läuft vor jedem Pull Request. Vollständig, nicht auszugsweise.**

```bash
python3 -m py_compile <geänderte .py>
python3 -m pyflakes   <geänderte .py>                      # 0 Befunde
python3 -m ruff check --select F,E9,B --ignore B905 <geänderte .py>
python3 tools/ncpatch.py check                             # Templates prüfen
python3 test_smoke.py
python3 test_nc_modules.py
python3 test_restream.py
```

Zusätzlich immer:

- Keine doppelten Top-Level-Defs (`ast.parse` → `module.body`).
- Keine doppelten Flask-Routen **inklusive `methods=`** — derselbe Pfad mit `GET`
  und `POST` ist **kein** Duplikat. Ein naiver Regex meldet hier Fehlalarm.
- Bei JavaScript in `templates/*.html`: Script-Blöcke extrahieren und
  `node --check` fahren. JSON-LD als JSON prüfen, nicht als JS.

### `test_smoke.py` — fünf Pakete, keine Serverumgebung

Es führt `bot.py` **wirklich** aus, und genau das fängt, was keine statische
Prüfung sieht: `NameError` auf der Modul-Ebene, eine Route, die beim ersten
Aufruf in einen 500er läuft, ein Rückruf, der nie verdrahtet wurde.

Bis v4.1-W31 galt der Test als „nur auf dem Server lauffähig". Das stimmte
nicht: TikTokLive und python-telegram-bot stubbt er selbst,
requests/httpx/boto3/redis/PyMySQL/PySocks/faster-whisper werden erst **in**
Funktionen importiert, und ffmpeg/streamlink/yt-dlp fasst er gar nicht an.
Ein `.env` braucht er auch nicht — er setzt sich die nötigen Variablen selbst.
Übrig bleiben fünf Pakete:

```bash
python3 -m pip install -r requirements-smoke.txt
PYTHONUTF8=1 python3 test_smoke.py
```

Seitdem läuft er in der CI als Job `Rauchtest (bot.py laeuft wirklich)`.
Kommt ein neues Fremdpaket auf die Modul-Ebene, gehört es in
`requirements-smoke.txt` — der Vertrag
`_test_w31_rauchtest_laeuft_in_der_ci` in `test_nc_modules.py` meldet es
sonst mit Datei und Paketnamen.

### Wenn ein Vertrag in `test_restream.py` kippt

Die statischen Verträge verankern sich an **wörtlichem Quelltext** von
`bot.py`. Ändert sich eine Signatur, kippt der Vertrag, obwohl der Code
stimmt — das ist schon dreimal passiert (`stop(self, rid)` wurde
`stop(self, rid, _keep_desired=False)`). Ebenso die Fenster der Form
`src[i:i + 3000]`: wächst die Funktion darüber hinaus, meldet der Test etwas als
fehlend, das zwei Zeilen weiter unten steht.

> **Vor jedem Fix am Code erst prüfen, ob der Vertrag oder nur sein Anker
> gebrochen ist.**

---

## Architektur-Regeln

### 1. Keine Rückimporte

`nc/*` und `brain/*` importieren **niemals** aus `bot.py`. Konfiguration kommt
ausschließlich per `configure(...)`-Injection.

```python
# ❌ falsch — koppelt das Modul an den Monolithen, erzeugt Zirkularimporte
from bot.py import DB_PATH, log

# ✅ richtig — der Aufrufer injiziert, was das Modul braucht
def configure(*, db_conn, log, cfg):
    global _db_conn, _log, _cfg
    _db_conn, _log, _cfg = db_conn, log, cfg
```

Das hält beide Bibliotheken isoliert testbar — ohne Netz, ohne DB, ohne Bot.

### 2. `brain/` ist stdlib-only

Thread-basiert, `urllib` statt `aiohttp`. Ohne `brain/`-Verzeichnis muss der Bot
exakt so starten wie mit — jeder Baustein ist additiv, fail-open und einzeln per
Env-Schalter abschaltbar.

### 3. Geld nicht vermischen

`REVENUE_PLATFORMS = ("kick", "twitch", "youtube", "manuell")`. **TikTok gehört
nie dazu** — TikTok-Gifts gehen an den getrackten Streamer, nicht an eigene
Kanäle. Sie werden als `kind="gift"` gespeichert, nie als `donation`, und laufen
in keine Geldsumme.

`/api/donations/summary` ist Live-Telemetrie aus **Schätzwerten**.
`nc/ledger.py` sind gebuchte **Auszahlungen** für die Steuer. Niemals das eine
aus dem anderen ableiten. Ledger-Einträge sind append-only mit Hash-Kette;
eine Korrektur ist eine Gegenbuchung, kein Überschreiben.

---

## Navigation im Monolithen

`bot.py` hat über 30.000 Zeilen. Diese Datei wird **nie** ganz gelesen und
**nie** blind durchsucht. Erst fragen wo etwas steht, dann den Ausschnitt holen:

```bash
python3 tools/ncpatch.py find "donations"              # wo ist X?
python3 tools/ncpatch.py sym  bot.py api_brain     # Zeilenbereich eines Symbols
python3 tools/ncpatch.py show bot.py 24750 24810   # nur diesen Ausschnitt
python3 tools/ncpatch.py grep "tree.command" bot.py -C 3
python3 tools/ncpatch.py verify patches/x.json         # Trockenlauf
python3 tools/ncpatch.py apply  patches/x.json         # alles-oder-nichts, legt .bak an
```

> **Arbeitest du an der Zerlegung des Monolithen?** Dann lies zuerst
> [`docs/MODULARISIERUNG.md`](MODULARISIERUNG.md) — dort steht das Verfahren
> je Welle, die Regel zur Vertragswanderung und was ausdrücklich nicht gemacht wird.

`find` antwortet aus `.claude/INDEX.md`. **Nach jeder Änderung an Routen,
Slash-Commands oder Top-Level-Funktionen die Karte neu bauen** und mit
committen:

```bash
python3 tools/ncpatch.py map
```

Der Diff auf `INDEX.md` zeigt sofort, welche Routen und Funktionen eine Änderung
angefasst hat.

Nach Änderungen an Konfigurationsvariablen zusätzlich:

```bash
python3 tools/gen_env_example.py
```

---

## Code-Stil

- **Deutsch.** Code-Kommentare und alle Nutzerausgaben.
- **Kommentare erklären *warum*, nicht *was*** — bevorzugt mit dem konkreten
  Fehlerbild, das die Zeile verhindert:

  ```python
  # list() ist Pflicht: ein paralleler Restream-Stop ruft .pop() auf demselben
  # dict — ohne Kopie stirbt die Schleife mit "dict changed during iteration".
  for rid, proc in list(_RESTREAM_ACTIVE_ALL.items()):
  ```

- Zeilenlänge bis 127 Zeichen.
- Neue Konfiguration bekommt einen **Default**, der ohne Eintrag in der `.env`
  funktioniert. Leere Werte (`NAME=`) dürfen nie crashen.
- Neue Funktionalität ist per Env-Schalter **abschaltbar**.

---

## Fallstricke, die schon zugeschlagen haben

### Stille `except`-Blöcke sind der Hauptfeind

Der Bot fängt großflächig ab und loggt auf `warning`/`debug`. Ein `log.warning`
erscheint in einem ERROR-Log **nie** — so blieb ein Discord-Gateway-Tod
monatelang unsichtbar.

Für periodische Schleifen gibt es **`_loop_fehler(name, exc)`**: erste Meldung
sofort auf `error` mit Traceback, danach höchstens alle 15 Minuten eine — mit der
Zahl der unterdrückten Fälle. Jeder Dauerläufer-Wächter gehört dorthin, nie auf
`log.debug` und nie auf `pass`.

Legitim still bleiben nur Aufräumpfade, deren Fehlschlag bedeutungslos ist
(`proc.terminate()` auf einen toten Prozess, `os.remove()` auf eine bereits
gelöschte Datei) — und der Fehlerkanal selbst, dort erzeugt Loggen eine Rekursion.

### Modul-Konstanten frieren `.env` ein

`.env` wird teils erst nach den ersten Imports geladen. Konfiguration als
**Funktion** lesen (`_backend_conf()`), nie als Modul-Konstante.

### Einmal-`await` ohne Supervisor

Jeder Long-Running-Client braucht Reconnect mit Backoff **und** ein
Abbruchkriterium für deterministische Fehler.

### Guards als Objekt-Attribut

`getattr(client, "_started", False)` bricht, sobald das Objekt neu erzeugt wird
→ parallele Endlosschleifen. **Modul-global** guarden.

### Vertragsbrüche zum `brain/`

Bei Änderungen an `router.route(topic, payload)` alle Callsites prüfen:
`grep -n 'router.route('`. Ein Key-Drift (`prompt` vs. `question`) fiel einmal
nur im Telegram-Pfad aus, weil die Flask-Route den richtigen Key benutzte.

### Iteration über veränderliche Zustände

Alle Iterationen über `_RESTREAM_ACTIVE_*` und verwandte Dicts brauchen `list()`
— parallele Tasks `.pop()`en darauf.

### Dateihandles

`/proc`-Dateien und alles andere immer mit `with open(...)`. Im Health-Loop
summiert sich ein nacktes `open()` gegen das fd-Limit.

---

## Commits und Pull Requests

**Commit-Nachrichten**: erste Zeile im Imperativ, knapp, was sich ändert. Danach
eine Leerzeile und das *Warum* — bevorzugt mit dem beobachteten Symptom.

```
Restream-Ziel-Verifikation gegen Plattform-APIs härten

Bei tee mit onfail=ignore läuft ffmpeg weiter, wenn Twitch wegbricht.
Das Panel zeigte drei grüne Ziele, während auf zwei Plattformen nichts
ankam. Der Verify-Loop fragt jetzt die Plattformen selbst.
```

**Pull Requests**:

1. Branch von `main`: `git checkout -b feature/mein-feature`
2. Änderung klein und **einzeln verifizierbar** halten — Deploy geht gegen
   Produktion, Rollback muss möglich sein.
3. Die Pflicht-Prüfkette laufen lassen und das Ergebnis im PR nennen.
4. `.claude/INDEX.md` und `.env.example` bei Bedarf neu erzeugen und mit
   committen.
5. Die Vorlage im PR ausfüllen.

**Nicht committen:** `.env`, Cookies, OAuth-Token-Dateien, Datenbanken,
Aufnahmen, Logs, Build-Archive. Die `.gitignore` sperrt das bereits — prüfe
trotzdem `git status`, bevor du pushst. Ein einmal committetes Geheimnis steht
auch nach dem Löschen noch in der Historie.

---

## Bug-Reports

Nutze die Issue-Vorlage. Hilfreich ist immer:

```bash
journalctl -u nightcrawler -n 200 --no-pager     # Logausschnitt
curl -s localhost:8050/api/selftest | python3 -m json.tool
python3 -c "import nc.freeai as f; print(f.diagnose())"   # bei KI-Problemen
```

> **Vor dem Einfügen redigieren:** Logs können Cookies, Tokens und Stream-Keys
> enthalten.

**Sicherheitslücken gehören nicht in ein öffentliches Issue** — siehe
[`SECURITY.md`](SECURITY.md).

---

## Lizenz deiner Beiträge

Mit einem Pull Request stellst du deinen Beitrag unter die
**GNU General Public License v3.0 oder später** — dieselbe Lizenz wie das
Projekt. Siehe [`LICENSE`](../LICENSE).

Bringst du Fremdcode mit, trage ihn in
[`THIRD_PARTY_LICENSES.md`](THIRD_PARTY_LICENSES.md) ein und prüfe, dass seine
Lizenz GPLv3-kompatibel ist.
