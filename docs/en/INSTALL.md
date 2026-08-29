# Manual installation

> 🌐 **English** · [Deutsch](../INSTALL.md)

The quick route is in the README: **[📦 Installation](../../README.en.md#-installation)**
— `tools/installer.sh` sets everything up and asks before every intervention.
This guide is for anyone who wants to walk each step themselves.

> **Python 3.12 is a hard minimum.** `bot.py` uses f-strings containing
> backslashes (PEP 701) — on 3.11 even parsing the file fails. Debian 12 and
> Raspberry Pi OS bookworm ship 3.11.

---

## Step 1 — system packages

These four do **not** come through `pip` but through the package manager:

```bash
sudo apt update
sudo apt install -y python3 python3-venv python3-pip ffmpeg streamlink yt-dlp
```

| Package | What for |
|---|---|
| `ffmpeg` | recording, restream, overlay compositing |
| `streamlink` | source resolution |
| `yt-dlp` | fallback resolution (403 life cycle) |
| `crowdsec` | *optional* — defence panel in the dashboard (`cscli`), see [`CROWDSEC.md`](../CROWDSEC.md) (German) |

---

## Step 2 — project and virtual environment

```bash
git clone https://github.com/itsamemedev/Telegram-Stream-Info-Bot.git ~/nightcrawler
cd ~/nightcrawler

python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

`requirements.txt` deliberately leaves versions open. Once the bot runs for you,
freeze the **demonstrably working** state:

```bash
python3 -m pip freeze > requirements.lock.txt
```

That matters especially for `TikTokLive` — the library hangs off an
undocumented API and can break from one day to the next.

---

## Step 3 — create the configuration

```bash
cp .env.example .env
chmod 600 .env
nano .env
```

Only two values are mandatory:

```ini
BOT_TOKEN=123456:ABC-DEF…            # Telegram bot from @BotFather
ADMIN_CHAT_ID=123456789              # your Telegram ID (alarms, admin commands)
```

The template is **auto-generated** from the source and lists every
configuration variable with its default. A commented-out line means the default
is active. Regenerate it after code changes:

```bash
python3 tools/gen_env_example.py
```

> **The `.env` never belongs in the repository.** It contains cookies, OAuth
> tokens and stream keys. `.gitignore` already blocks it — a secret that has
> been committed once is still in the history after you delete it.

---

## Step 4 — database

The database creates **itself** on first start — nothing to do. The default is
SQLite; for MariaDB, in the `.env`:

```ini
DB_BACKEND=mariadb
DB_HOST=127.0.0.1
DB_NAME=nightcrawler
DB_USER=nightcrawler
DB_PASS=…
```

---

## Step 5 — first start

```bash
python3 bot.py
```

Expected lines in the log:

```
Recorder-Inventur:  ffmpeg : /usr/bin/ffmpeg   yt-dlp : /usr/bin/yt-dlp
Discord verbunden als <bot> — 45 Slash-Commands aktiv.
Brain-LLM: llama.cpp OK   (oder: KEIN Backend erreichbar → Fallback)
Dashboard läuft auf 127.0.0.1:8050
```

(Log output is German by default; set `UI_LANG=en` to switch the bot's
user-facing language — log lines stay German on purpose, they are for the
operator.)

If everything runs, set up the systemd service: **[`DEPLOY.md`](DEPLOY.md)**.

---

## Optional — local LLM (llama.cpp)

For AI answers without cloud and without cost: see
**[`SETUP_LLAMACPP.md`](../SETUP_LLAMACPP.md)** (German) and the bundled unit
**[`llama-server.service`](../../llama-server.service)**.

If no llama.cpp is reachable, the bot automatically falls back to Ollama and
then to the keyless free backends — it **never** refuses to start because of
this.

---

## Optional — OAuth for title and category

| Platform | Guide |
|---|---|
| Twitch | **[`SETUP_TWITCH_OAUTH.md`](../SETUP_TWITCH_OAUTH.md)** (German) |
| YouTube | **[`SETUP_YT_OAUTH.md`](../SETUP_YT_OAUTH.md)** (German) |
| Kick | user OAuth directly in the dashboard panel |

---

Not running as expected? → **[`TROUBLESHOOTING.md`](TROUBLESHOOTING.md)**
