# Security-Audit

> Stand: 31.10.2026, Ausgangscommit `4fa5426` (v4.4.1), Welle W134.
> Nur statische Prüfung und autorisierte lokale Läufe — kein Angriff auf
> fremde Systeme, kein Zugriff auf den Produktionsserver.

## Ergebnis in einem Satz

Keine ausnutzbare Lücke im eigenen Code gefunden; das echte Risiko lag in
den **erlaubten Fassungen** der Fremdpakete und in einem Geheimnis, das der
Bot selbst ins Log schrieb (behoben in W132).

## 1. Lieferkette (pip-audit)

| Liste | Befund |
|---|---|
| alte Untergrenzen aus `requirements.txt` | 126 Einträge, 69 eindeutige Kennungen in 8 Paketen |
| neue Untergrenzen (W134) | keine bekannten Schwachstellen |
| neueste Fassungen auf PyPI | keine bekannten Schwachstellen |

Betroffen waren Flask, Werkzeug (12 Kennungen), aiohttp (46), requests,
python-dotenv, orjson, PyMySQL und redis. Einzelheiten und die neuen Grenzen:
[`DEPENDENCY_AUDIT.md`](DEPENDENCY_AUDIT.md).

**Offen:** die Fassungen auf dem Server sind unbekannt (kein
`requirements.lock.txt`). Ob dort eine der befallenen Fassungen läuft, sagt
erst `pip-audit -r requirements.lock.txt` auf dem Server.

## 2. Statische Analyse (Bandit)

Lauf: `bandit -r bot.py discordbot.py brain_bridge.py telegramversand.py nc
brain -x nc/_vendor -ll -ii` (mittlere und hohe Schwere, mittlere und hohe
Sicherheit). 56 Befunde, alle von Hand nachgesehen.

| Prüfung | Anzahl | Bewertung |
|---|---|---|
| B608 SQL aus Zeichenketten | 37 | **kein Befund.** Tabellen- und Spaltennamen aus festen Listen, Werte über `?`-Platzhalter, Zahlen per `%d` erzwungen. Die vier Stellen mit Anfrageeingabe (`nc/routes/collections.py`, `restream.py`, `ops.py`, `money.py`) einzeln geprüft. |
| B310 `urlopen` mit variabler URL | 16 | **kein Befund.** URLs aus Konstanten oder `.env` des Betreibers; keine aus Anfrageeingabe. |
| B602 `shell=True` | 1 | **bewusst.** `brain/agents.py` führt `SWAP_CLEAR_CMD` aus der `.env` aus — Konfiguration des Betreibers, keine Fremdeingabe. |
| B324 SHA-1 | 1 | **kein Sicherheitszweck.** Fingerabdruck der Dopplungssperre (`nc/replygate.py`); seit W134 mit `usedforsecurity=False` ausgewiesen. |
| B108 `/tmp` | 1 | nur in einem Test. |

## 3. Geheimnisse

- **Telegram-Bot-Token im Log** (773-mal im debug.log vom 30.10.): behoben in
  W132, geschwärzt in der Log-Schleuse und im Discord-Fehlerspiegel. Der
  Betreiber sollte den Token rotiert haben.
- **Redis-Passwort** in `redis://:pw@host` wurde nicht maskiert: behoben in W132.
- `git grep` mit dem Muster der CI („Kein Geheimnis im Diff") über das ganze
  Repo: kein Treffer.

## 4. Bestehende Riegel — nachgesehen, nicht ersetzt

`nc/sicherpfad.py` (Pfadausbruch), Redact-Pfad für ffmpeg/streamlink
(F4), `nc/webserver.bindung()` (Deck nur auf Loopback ohne Token/PIN),
waitress statt Werkzeug-Server, CodeQL in der CI, Hash-Kette des Ledgers.
Sie bleiben, wie sie sind; jeder hat Verträge.

## 5. Offene Punkte

| Punkt | Risiko | Vorschlag |
|---|---|---|
| Serverfassungen unbekannt | mittel | Lockfile vom Server, dann `pip-audit` dort |
| PySocks ohne Pflege seit 2019 | niedrig | in einer späteren Welle durch `python-socks` ersetzen, falls der eine Aufruf es trägt |
| TikTokLive 7.x signiert über einen Drittanbieter | niedrig bis mittel | vor einem Wechsel den Datenfluss nachmessen |
| Dependabot | — | **behoben in W134**: die Datei war die leere Vorlage, Dependabot lief nie; jetzt pip und GitHub-Actions wöchentlich |
