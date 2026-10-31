# Dependency-Audit

> Stand: 31.10.2026, Ausgangscommit `4fa5426` (v4.4.1), Welle W134.
> Methode und Rohdaten am Ende. Alles hier ist gemessen oder nachgelesen —
> wo etwas nicht feststellbar war, steht das dabei.

## Das Wichtigste vorweg

1. **Die alten Untergrenzen erlaubten Pakete mit bekannten Schwachstellen.**
   `pip-audit` gegen genau die Fassungen, die `requirements.txt` als Minimum
   zuließ: 126 Einträge, 69 eindeutige Kennungen, in acht Paketen. Seit W134
   stehen die acht Grenzen auf der jeweils kleinsten befundfreien Fassung;
   die Gegenprobe gegen alle neuen Grenzen meldet nichts mehr.
2. **Die Produktionsfassungen waren unbekannt — seit W135 nicht mehr.**
   Der Betreiber hat am 31.10. auf dem Server eingefroren. `pip-audit` dort:
   **79 bekannte Schwachstellen in 11 Paketen** — zwei direkte (aiohttp
   3.14.1, Werkzeug 3.1.8) und neun mitgezogene, die in keiner
   Requirements-Datei stehen (multidict, anyio, h2, urllib3, brotli, certifi,
   filelock, Pillow, setuptools). Nach dem gezielten Upgrade: `pip check`
   ohne Konflikt, `pip-audit` ohne Befund. Dieser Stand ist jetzt
   `requirements.lock.txt`. Auf dem Server läuft **TikTokLive 6.6.5** (MIT)
   und **Python 3.14**; waitress fehlte dort trotz Pflicht (seit W136 installiert).
3. **TikTokLive hat mit 7.0 die Lizenz gewechselt** — von MIT (bis 6.6.5) zu
   „Modified AGPL-3.0". `docs/THIRD_PARTY_LICENSES.md` führte bis W134 „MIT".
   Bewertung unten; kurz: für NIGHTCRAWLER kein Hindernis, aber eine
   Pflicht zur richtigen Angabe.
4. **Die CI kannte die Produktions-Python-Fassung nicht.** Sie fuhr 3.12 und
   3.13, der Server läuft auf 3.14. Lokal auf 3.14.6 gefahren: alle drei
   Suiten grün. Seit W134 steht 3.14 in der Matrix.

## Inventar

Gezählt per Syntaxbaum über `bot.py`, `discordbot.py`, `brain_bridge.py`,
`telegramversand.py`, `nc/`, `brain/` und `tools/` — Importe auf
Modul-Ebene **und** in Funktionen. `nc/_vendor/` ausgenommen (mitgeliefert).

| Paket (Import) | Wo | Ebene |
|---|---|---|
| `flask` | bot.py, nc/ (40 Importstellen), brain_bridge.py | Modul |
| `werkzeug` | bot.py | Modul |
| `aiohttp` | bot.py (15 Importstellen), nc/ (24) | Modul + Funktion |
| `discord` | bot.py, discordbot.py | Funktion |
| `dotenv` | bot.py, tools/ | Modul |
| `telegram` | bot.py, telegramversand.py | Modul |
| `TikTokLive` | bot.py | Modul + Funktion |
| `orjson`, `waitress`, `httpx`, `socks`, `websockets_proxy`, `requests` | bot.py | Funktion |
| `pymysql` | bot.py, nc/ | Funktion |
| `redis`, `boto3`, `faster_whisper`, `uvloop` | bot.py | Funktion |
| `segno` | nc/ | Funktion (mitgeliefert unter `nc/_vendor/`) |
| `browser_cookie3` | nc/ | Funktion (optional, `ImportError`-Auffang) |
| `PIL`, `packaging`, `pip` | nur tools/ | Funktion |

`brain/` importiert außerhalb von `brain/test_bughunt.py` nichts Fremdes —
die Regel „stdlib-only" hält. Keine Rückimporte aus `bot.py` gefunden
(`tools/abhaengigkeiten.py --sperre`: OK, 18 Pakete).

Systemwerkzeuge (nicht per pip): `ffmpeg`, `streamlink`, `yt-dlp`, `cscli`.

## Bewertung je Bibliothek

Neueste Fassung und Datum: PyPI-JSON, abgefragt am 31.10.2026.

| Bibliothek | Grenze (vorher → jetzt) | Neueste | Zustand | Alternative | Empfehlung |
|---|---|---|---|---|---|
| python-telegram-bot | ≥ 20.0 | 22.8 (06/2026) | aktiv, LGPL-3.0 | aiogram | **BEHALTEN** — über 200 Sendestellen laufen über `_safe_send`; ein Wechsel wäre Neubau ohne Gewinn |
| discord.py | ≥ 2.0 | 2.7.1 (03/2026) | aktiv, MIT | pycord, nextcord, hikari | **BEHALTEN** — Forks ohne messbaren Vorteil |
| TikTokLive | ≥ 6.0 | 7.0.1 (09/2026) | aktiv, Lizenzwechsel in 7.0, Signatur über Euler Stream | keine gleichwertige Python-Bibliothek gefunden (Ports in Node, Go, Rust, Java, C#; gehostete Dienste mit API-Schlüssel) | **SERVERFASSUNG FESTNAGELN, 7.x EXPERIMENTELL TESTEN** — siehe unten |
| Flask | 2.2 → **3.1.3** | 3.1.3 | aktiv, BSD-3 | — | **AKTUALISIERT** (Sicherheit) |
| Werkzeug | 2.0 → **3.1.9** | 3.1.9 | aktiv, BSD-3 | — | **AKTUALISIERT** (Sicherheit, 12 Kennungen) |
| waitress | ≥ 3.0.1 | 3.0.2 (11/2024) | ruhig, aber gepflegt | gunicorn (kein Windows), granian | **BEHALTEN** |
| aiohttp | 3.9 → **3.14.4** | 3.14.5 | aktiv | httpx | **AKTUALISIERT** (Sicherheit, 46 Kennungen) |
| requests | 2.31 → **2.33.0** | 2.34.2 | aktiv | httpx / urllib | **AKTUALISIERT**; nur zwei Aufrufstellen — später durch `urllib` ersetzbar, kein Gewinn jetzt |
| httpx | ≥ 0.27 | 0.28.1 (12/2024) | kein Release seit 12/2024 | aiohttp | **BEHALTEN** — wird von python-telegram-bot und TikTokLive selbst gebraucht; die eine eigene Stelle bleibt |
| PySocks | ≥ 1.7.1 | 1.7.1 (09/2019) | **unbewegt seit 2019** | `aiohttp-socks`/`python-socks`, Proxy über HTTP-CONNECT | **SPÄTER ERNEUT PRÜFEN** — eine Aufrufstelle; funktioniert, aber ohne Pflege |
| websockets_proxy | ≥ 0.1.3 | 0.1.3 (11/2024) | klein, eine Fassung | `websockets` ≥ 15 kann Proxy selbst | **EXPERIMENTELL TESTEN** — hängt an der TikTokLive-Frage (B78) |
| python-dotenv | 1.0 → **1.2.2** | 1.2.4 | aktiv | — | **AKTUALISIERT** (Sicherheit) |
| orjson | 3.9 → **3.11.6** | 3.13.0 | aktiv | stdlib `json` | **AKTUALISIERT** (Sicherheit) |
| PyMySQL | 1.1 → **1.1.1** | 1.2.3 | aktiv, optional | mysqlclient | **AKTUALISIERT** (Sicherheit) |
| redis | 4.2 → **4.4.4** | 8.1.0 | aktiv, optional | valkey-py | **AKTUALISIERT** (Sicherheit); Betriebsbefund: Server verlangt Passwort |
| faster-whisper | ≥ 1.0 | 1.2.1 (10/2025) | gepflegt, optional | whisper.cpp, ONNX | **SPÄTER ERNEUT PRÜFEN** (Welle Performance/KI) |
| boto3 | ≥ 1.34 | 1.43.x | aktiv, optional | — | **BEHALTEN** |
| uvloop | ≥ 0.19 | 0.23.0 (10/2026) | aktiv | — | **BEHALTEN** |
| segno | mitgeliefert | 1.6.6 (03/2025) | gepflegt | — | **BEHALTEN** |
| browser-cookie3 | optional | 0.20.1 (12/2024) | ruhig, LGPL | yt-dlp `--cookies-from-browser` (wird schon benutzt) | **SPÄTER ERNEUT PRÜFEN** |

## TikTokLive im Einzelnen

**API.** Benutzt werden `TikTokLiveClient(..., web_proxy=, ws_proxy=)`,
`CommentEvent`, `GiftEvent` (bot.py, Chat-Listener). Der bekannte Bruch
(B78, ws-Proxy-Konvertierung) lag innerhalb der 6er-Reihe. Ein Wechsel auf
7.x ist **nicht** geprüft und wird es erst in einem isolierten Prototypen.

**Lizenz.** 6.6.5: MIT. 7.0.1: AGPL-3.0 mit Zusatzbedingungen nach
Abschnitt 7. Abschnitt 18 erlaubt die Einbindung in nachgelagerte Projekte
ohne AGPL-Pflicht und nennt ausdrücklich „TikTok LIVE Stream Bots and other
automated tools". Abschnitt 19 nimmt geschlossene oder gehostete
SaaS-/Relay-Dienste für Dritte davon aus. NIGHTCRAWLER ist quelloffen unter
GPL-3.0 und kein Dienst für Dritte — selbst die volle AGPL wäre erfüllbar.
**Das ist keine Rechtsberatung**; wer den Bot als Dienst für andere anbietet,
liest Abschnitt 19 selbst.

**Datenfluss.** 7.x signiert Anfragen standardmäßig über den Signaturserver
von Euler Stream; der Server ist austauschbar. Die Raum-ID und die Anfrage
gehen damit an einen Drittanbieter. Das ist in 6.x ähnlich — vor einem
Wechsel wird es nachgesehen, nicht angenommen.

**Alternativen.** Keine eigenständige, gleich gut gepflegte Python-
Bibliothek gefunden. Es gibt Ports in anderen Sprachen und gehostete
WebSocket-Dienste mit API-Schlüssel — beides tauscht eine Python-Abhängigkeit
gegen einen zweiten Laufzeitprozess oder einen Drittanbieter mit Konto. Die
offizielle TikTok-API ist laut Auftrag ausgeschlossen. **Ergebnis: BEHALTEN,
die laufende Fassung festnageln.**

## Das Lockfile

**Herkunft.** `requirements.lock.txt` ist `pip freeze --exclude-editable`
aus dem Server-venv vom 31.10., **nach** dem Sicherheits-Upgrade. Es ist von
Hand nicht verändert. Es enthält auch die Werkzeuge, die zum Prüfen
installiert wurden (pip-audit samt Abhängigkeiten) und solche, die der
Betreiber selbst nachinstalliert hat (ollama, piper-tts, py-spy, psutil) —
es beschreibt den Server, nicht `requirements.txt`.

**Was jetzt daran hängt:**

1. CI-Job **„Produktionsstand"**: installiert genau dieses Lockfile auf
   Python 3.14, fährt `pip-audit` darauf und alle drei Suiten. Lokal vorher:
   Installation auf frischem 3.14, Suiten grün.
2. `tools/abhaengigkeiten.py` vergleicht Lockfile und Untergrenzen und meldet
   als **Hinweis** (keine Sperre), was fehlt oder zu alt ist. Bis W136: waitress.
3. Dependabot liest `requirements*.txt` und meldet Sicherheitsfälle jetzt
   auch für die mitgezogenen Pakete — genau die neun aus dem Server-Befund
   waren bisher unsichtbar. Versions-Pull-Requests für pip sind bewusst aus:
   sie hoben Untergrenzen über den Serverstand und hätten das Lockfile vom
   Server gelöst.
4. `tools/build_release.py` packt die Datei ins Archiv.

**Pflege.** Nur auf dem Server erneuern, nie von Hand:

    cd ~/tiktok-bot
    venv/bin/python -m pip freeze --exclude-editable > requirements.lock.txt
    venv/bin/python -m pip_audit -r requirements.lock.txt

Danach die Datei ins Repo. Die Update-Funktion schreibt sie beim nächsten
Update aus dem Repo zurück auf den Server — wer dort neu einfriert und nicht
eincheckt, verliert den neuen Stand beim nächsten Update.

## Methode und Rohdaten

- Inventar: `ast.walk` über alle genannten Dateien, Standardbibliothek über
  `sys.stdlib_module_names` ausgeschlossen.
- Neueste Fassungen: `https://pypi.org/pypi/<paket>/json`.
- Schwachstellen: `pip-audit -r <datei> --no-deps --disable-pip` gegen drei
  Listen — alte Untergrenzen, neue Untergrenzen, neueste Fassungen. Neue
  Untergrenzen und neueste Fassungen: „No known vulnerabilities found".
- Python 3.14: Interpreter 3.14.6 über `uv`, venv mit `requirements-smoke.txt`
  plus `orjson waitress pytest coverage pyyaml`; `test_smoke.py`,
  `test_nc_modules.py`, `test_restream.py` grün.
- Lizenzen: METADATA und LICENSE aus den Rädern von PyPI.
