# Installation von Hand

> 🌐 **Deutsch** · [English](en/INSTALL.md)

Der schnelle Weg steht im README: **[📦 Installation](../README.md#-installation)**
— `tools/installer.sh` richtet alles ein und fragt vor jedem Eingriff. Diese
Anleitung ist für alle, die jeden Schritt selbst gehen wollen.

> **Python 3.12 ist harte Mindestversion.** `bot.py` nutzt f-strings mit
> Backslash (PEP 701) — unter 3.11 scheitert schon das Parsen der Datei.
> Debian 12 und Raspberry Pi OS bookworm liefern 3.11.

---

## Schritt 1 — Systempakete

Diese vier kommen **nicht** über `pip`, sondern über den Paketmanager:

```bash
sudo apt update
sudo apt install -y python3 python3-venv python3-pip ffmpeg streamlink yt-dlp
```

| Paket | Wofür |
|---|---|
| `ffmpeg` | Aufnahme, Restream, Overlay-Einblendung |
| `streamlink` | Quellenauflösung |
| `yt-dlp` | Rückfall-Auflösung (403-Lebenszyklus) |
| `crowdsec` | *optional* — Abwehr-Panel im Dashboard (`cscli`), siehe [`CROWDSEC.md`](CROWDSEC.md) |

---

## Schritt 2 — Projekt und virtuelle Umgebung

```bash
git clone https://github.com/itsamemedev/Telegram-Stream-Info-Bot.git ~/nightcrawler
cd ~/nightcrawler

python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

`requirements.txt` lässt die Versionen bewusst offen. Sobald der Bot bei dir
läuft, friere den **nachweislich funktionierenden** Stand ein:

```bash
python3 -m pip freeze > requirements.lock.txt
```

Das ist besonders für `TikTokLive` wichtig — die Bibliothek hängt an einer
undokumentierten API und kann von einem Tag auf den anderen brechen.

---

## Schritt 3 — Konfiguration anlegen

```bash
cp .env.example .env
chmod 600 .env
nano .env
```

Pflicht sind nur zwei Werte:

```ini
BOT_TOKEN=123456:ABC-DEF…            # Telegram-Bot von @BotFather
ADMIN_CHAT_ID=123456789              # deine Telegram-ID (Alarme, Admin-Befehle)
```

Die Vorlage ist **auto-generiert** aus dem Quellcode und listet alle
Konfigurationsvariablen mit ihren Defaults. Auskommentierte Zeilen = Default
aktiv. Neu erzeugen nach Code-Änderungen:

```bash
python3 tools/gen_env_example.py
```

> **`.env` gehört niemals ins Repository.** Sie enthält Cookies, OAuth-Tokens
> und Stream-Keys. Die `.gitignore` sperrt sie bereits — ein einmal committetes
> Geheimnis steht auch nach dem Löschen noch in der Historie.

---

## Schritt 4 — Datenbank

Die Datenbank legt sich beim ersten Start **selbst** an — nichts zu tun.
Standard ist SQLite; für MariaDB in der `.env`:

```ini
DB_BACKEND=mariadb
DB_HOST=127.0.0.1
DB_NAME=nightcrawler
DB_USER=nightcrawler
DB_PASS=…
```

---

## Schritt 5 — Erster Start

```bash
python3 bot.py
```

Erwartete Zeilen im Log:

```
Recorder-Inventur:  ffmpeg : /usr/bin/ffmpeg   yt-dlp : /usr/bin/yt-dlp
Discord verbunden als <bot> — 45 Slash-Commands aktiv.
Brain-LLM: llama.cpp OK   (oder: KEIN Backend erreichbar → Fallback)
Dashboard läuft auf 127.0.0.1:8050
```

Läuft alles, richte den systemd-Dienst ein: **[`DEPLOY.md`](DEPLOY.md)**.

---

## Optional — lokales LLM (llama.cpp)

Für KI-Antworten ohne Cloud und ohne Kosten: siehe
**[`SETUP_LLAMACPP.md`](SETUP_LLAMACPP.md)** und die mitgelieferte Unit
**[`llama-server.service`](../llama-server.service)**.

Ist kein llama.cpp erreichbar, fällt der Bot automatisch auf Ollama und danach
auf die keylosen freien Backends zurück — er startet **nie** deswegen nicht.

---

## Optional — OAuth für Titel und Kategorie

| Plattform | Anleitung |
|---|---|
| Twitch | **[`SETUP_TWITCH_OAUTH.md`](SETUP_TWITCH_OAUTH.md)** |
| YouTube | **[`SETUP_YT_OAUTH.md`](SETUP_YT_OAUTH.md)** |
| Kick | User-OAuth direkt im Dashboard-Panel |

---

Läuft es nicht wie erwartet? → **[`TROUBLESHOOTING.md`](TROUBLESHOOTING.md)**
