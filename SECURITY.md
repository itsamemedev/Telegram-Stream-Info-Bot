# Sicherheitsrichtlinie

## Unterstützte Versionen

| Version | Unterstützt |
|---|---|
| 4.0.x (`Restream Control Room`) | ✅ |
| 3.7.x (`Kontrollraum-Fundament`) | ⚠️ nur kritische Lücken |
| < 3.7 | ❌ |

## Eine Lücke melden

**Bitte kein öffentliches Issue.**

Melde Sicherheitslücken über **[GitHub Security Advisories](https://github.com/itsamemedev/Telegram-Stream-Info-Bot/security/advisories/new)**
(„Report a vulnerability") oder per E-Mail an den Repository-Inhaber.

Hilfreich in der Meldung:

- Betroffene Datei / Route / Modul und Version
- Wie sich das Problem reproduzieren lässt
- Wirkung: Was kann ein Angreifer damit erreichen?
- Falls vorhanden: ein Vorschlag zur Behebung

**Bitte redigiere Logausschnitte vor dem Versand** — sie enthalten
regelmäßig Cookies, OAuth-Tokens und Stream-Keys.

### Was du erwarten kannst

| Schritt | Rahmen |
|---|---|
| Empfangsbestätigung | innerhalb von 72 Stunden |
| Erste Einschätzung | innerhalb von 7 Tagen |
| Fix bzw. Zeitplan | nach Schweregrad, kritische Lücken zuerst |
| Nennung im Advisory | auf Wunsch, gerne |

Bitte gib uns Zeit für einen Fix, bevor du Details veröffentlichst.

---

## Betriebshinweise — die häufigsten Fußangeln

Die meisten realen Risiken in diesem Projekt entstehen beim Betrieb, nicht im
Code. Diese Punkte sind Pflicht:

### `.env` ist der Kronjuwelen-Speicher

Rund 470 Variablen, darunter Cookies, OAuth-Tokens, API-Schlüssel und
RTMP-Stream-Keys. Ein Stream-Key erlaubt jedem, auf deinem Kanal zu senden.

```bash
chmod 600 .env
```

Sie steht in `.gitignore` und liegt nie im Auslieferungsarchiv. **Ein einmal
committetes Geheimnis steht auch nach dem Löschen noch in der Historie** — dann
hilft nur: Schlüssel widerrufen und neu ausstellen.

### Das Dashboard gehört nicht ins offene Netz

Standard ist `127.0.0.1:8050`. Zugriff läuft über einen SSH-Tunnel:

```bash
ssh -L 3000:localhost:8050 ubuntu@<server-ip>
```

Wer das Dashboard öffentlich erreichbar macht, stellt einen vollständigen
Fernsteuerungs-Kontrollraum ins Netz — inklusive Aufnahme-Archiv,
Einnahmen-Journal und Restream-Steuerung. Wenn es sein muss: Reverse Proxy mit
TLS **und** Authentifizierung davor, `DASHBOARD_TOKEN` setzen, und die
CrowdSec-Anbindung aktivieren (siehe [`docs/CROWDSEC.md`](docs/CROWDSEC.md)).

### Log-Redaction nicht umgehen

Beim Loggen von `streamlink`- und `ffmpeg`-Kommandozeilen werden Cookie-Header
und Stream-Keys unkenntlich gemacht. Wer die Kommandozeilen-Erzeugung ändert,
muss sicherstellen, dass der Redact-Pfad weiterhin greift.

### Totmann-Meldung einrichten

Stirbt der Prozess ganz, sagt dir das sonst niemand — auch nicht, wenn der Grund
ein Angriff war:

```bash
chmod +x tools/notify_failure.sh
sudo systemctl edit nightcrawler   # → [Unit] OnFailure=nightcrawler-notify@%n.service
```

### Abhängigkeiten einfrieren

`requirements.txt` lässt Versionen bewusst offen. Friere auf dem Server den
laufenden Stand ein und halte ihn nach:

```bash
python3 -m pip freeze > requirements.lock.txt
```

---

## Was ausdrücklich **keine** Lücke ist

- Ein offenes Dashboard, das jemand selbst ins Netz gestellt hat.
- Eine `.env`, die jemand selbst committet hat.
- Rate-Limits oder Sperren der Fremdplattformen (TikTok, Kick, Twitch, YouTube).
- Fehlalarme der Moderations-Heuristik. Das ist ein normales Issue —
  der Shield ist bewusst auf null False Positives getrimmt, Meldungen dazu sind
  willkommen.
