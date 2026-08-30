# Third-party code and licences

> 🌐 **English** · [Deutsch](../THIRD_PARTY_LICENSES.md)

NIGHTCRAWLER is licensed under the **GNU GPL v3.0 or later**
([`LICENSE`](../../LICENSE)). This file lists third-party code that ships with
the project or is required at runtime, together with its licence.

---

## Bundled code (vendored)

This code sits **in the repository** and is shipped with it.

| Path | Project | Version | Licence | Copyright |
|---|---|---|---|---|
| `nc/_vendor/segno/` | [segno](https://github.com/heuer/segno) — QR code encoder | 1.6.6 | BSD-3-Clause | © 2016–2024 Lars Heuer |

> “QR Code” and “Micro QR Code” are registered trademarks of
> DENSO WAVE INCORPORATED.

**BSD-3-Clause is GPLv3-compatible** — the vendored code keeps its own licence,
and the copyright and licence notices in the source files stay untouched. Why it
is vendored: the QR encoder is needed for the dashboard login and should not add
another runtime dependency.

---

## Runtime dependencies (pip)

These packages are **not** shipped; they are installed through
[`requirements.txt`](../../requirements.txt).

| Package | Purpose | Licence |
|---|---|---|
| `python-telegram-bot` | Telegram bot | LGPL-3.0 |
| `discord.py` | Discord gateway and slash commands | MIT |
| `TikTokLive` | Live detection | MIT |
| `Flask` | Dashboard | BSD-3-Clause |
| `Werkzeug` | WSGI substrate | BSD-3-Clause |
| `aiohttp` | async HTTP | Apache-2.0 |
| `requests` | sync HTTP | Apache-2.0 |
| `httpx` | HTTP/2-capable client | BSD-3-Clause |
| `PySocks` | SOCKS proxy | BSD-3-Clause |
| `websockets_proxy` | WebSocket over a proxy | MIT |
| `python-dotenv` | loading the `.env` | BSD-3-Clause |
| `orjson` | fast JSON | Apache-2.0 / MIT |
| `PyMySQL` | MariaDB backend | MIT |
| `redis` | optional cache | MIT |
| `faster-whisper` | transcription | MIT |
| `boto3` | S3 backup (optional) | Apache-2.0 |
| `uvloop` | faster asyncio loop (optional) | MIT / Apache-2.0 |

All of the licences listed are compatible with the GPLv3.

---

## System tools

Installed through the package manager and invoked as **separate programs**
(subprocess), not linked:

| Tool | Purpose | Licence |
|---|---|---|
| `ffmpeg` | recording, restream, overlay | LGPL-2.1+ / GPL-2.0+ (build-dependent) |
| `streamlink` | source resolution | BSD-2-Clause |
| `yt-dlp` | fallback resolution | Unlicense |
| `crowdsec` (optional) | defence panel | MIT |
| `llama.cpp` (optional) | local LLM | MIT |
| `piper` (optional) | speech output | MIT |

---

## Notes

- The licence information given here is collected to the best of our knowledge.
  What is authoritative is always the licence file of the respective project in
  the version installed on your machine.
- Anyone adding third-party code enters it **here** and checks GPLv3
  compatibility — see [`CONTRIBUTING.md`](CONTRIBUTING.md).
- The web APIs used (TikTok, Kick, Twitch, YouTube, OpenAI, Anthropic,
  Pollinations, LLM7) are subject to the terms of the respective providers. They
  are not part of this software.
