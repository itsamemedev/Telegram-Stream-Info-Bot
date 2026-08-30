# Fremdcode und Lizenzen

> 🌐 **Deutsch** · [English](en/THIRD_PARTY_LICENSES.md)

NIGHTCRAWLER steht unter der **GNU GPL v3.0 oder später** ([`LICENSE`](../LICENSE)).
Diese Datei listet Fremdcode, der mitgeliefert oder zur Laufzeit benötigt wird,
samt seiner Lizenz.

---

## Mitgelieferter Code (vendored)

Dieser Code liegt **im Repository** und wird mit ausgeliefert.

| Pfad | Projekt | Version | Lizenz | Copyright |
|---|---|---|---|---|
| `nc/_vendor/segno/` | [segno](https://github.com/heuer/segno) — QR-Code-Encoder | 1.6.6 | BSD-3-Clause | © 2016–2024 Lars Heuer |

> „QR Code" und „Micro QR Code" sind eingetragene Marken von
> DENSO WAVE INCORPORATED.

**BSD-3-Clause ist GPLv3-kompatibel** — der vendored Code behält seine eigene
Lizenz, die Copyright- und Lizenzhinweise in den Quelldateien bleiben unangetastet.
Warum vendored: der QR-Encoder wird für das Dashboard-Login gebraucht und soll
keine zusätzliche Laufzeitabhängigkeit erzeugen.

---

## Laufzeitabhängigkeiten (pip)

Diese Pakete werden **nicht** mitgeliefert, sondern über
[`requirements.txt`](../requirements.txt) installiert.

| Paket | Zweck | Lizenz |
|---|---|---|
| `python-telegram-bot` | Telegram-Bot | LGPL-3.0 |
| `discord.py` | Discord-Gateway und Slash-Commands | MIT |
| `TikTokLive` | Live-Erkennung | MIT |
| `Flask` | Dashboard | BSD-3-Clause |
| `Werkzeug` | WSGI-Unterbau | BSD-3-Clause |
| `aiohttp` | async HTTP | Apache-2.0 |
| `requests` | sync HTTP | Apache-2.0 |
| `httpx` | HTTP/2-fähiger Client | BSD-3-Clause |
| `PySocks` | SOCKS-Proxy | BSD-3-Clause |
| `websockets_proxy` | WebSocket über Proxy | MIT |
| `python-dotenv` | `.env` laden | BSD-3-Clause |
| `orjson` | schnelles JSON | Apache-2.0 / MIT |
| `PyMySQL` | MariaDB-Backend | MIT |
| `redis` | optionaler Cache | MIT |
| `faster-whisper` | Transkription | MIT |
| `boto3` | S3-Backup (optional) | Apache-2.0 |
| `uvloop` | schnellere asyncio-Schleife (optional) | MIT / Apache-2.0 |

Alle genannten Lizenzen sind mit der GPLv3 vereinbar.

---

## Systemwerkzeuge

Werden über den Paketmanager installiert und als **separate Programme**
aufgerufen (Subprozess), nicht gelinkt:

| Werkzeug | Zweck | Lizenz |
|---|---|---|
| `ffmpeg` | Aufnahme, Restream, Overlay | LGPL-2.1+ / GPL-2.0+ (buildabhängig) |
| `streamlink` | Quellenauflösung | BSD-2-Clause |
| `yt-dlp` | Rückfall-Auflösung | Unlicense |
| `crowdsec` (optional) | Abwehr-Panel | MIT |
| `llama.cpp` (optional) | lokales LLM | MIT |
| `piper` (optional) | Sprachausgabe | MIT |

---

## Hinweise

- Die hier genannten Lizenzangaben sind nach bestem Wissen zusammengetragen.
  Maßgeblich ist immer die Lizenzdatei des jeweiligen Projekts in der bei dir
  installierten Version.
- Wer Fremdcode ergänzt, trägt ihn **hier ein** und prüft die
  GPLv3-Kompatibilität — siehe [`CONTRIBUTING.md`](CONTRIBUTING.md).
- Genutzte Web-APIs (TikTok, Kick, Twitch, YouTube, OpenAI, Anthropic,
  Pollinations, LLM7) unterliegen den Nutzungsbedingungen der jeweiligen
  Anbieter. Sie sind kein Bestandteil dieser Software.
