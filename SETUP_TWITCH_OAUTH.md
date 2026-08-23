# Twitch verbinden (Follower-Zähler)

Der Follower-Zähler nutzt Twitch EventSub. Du gibst Client-ID + Secret an und
klickst einmal verbinden — danach erneuert der Bot den Zugang selbst.

## Warum ein SSH-Tunnel nötig ist

Twitch verlangt bei OAuth-Redirect-URLs **HTTPS** — mit genau einer Ausnahme:
`http://localhost:PORT` ist erlaubt. Eine nackte Server-IP mit HTTPS geht NICHT,
weil es dafür kein gültiges TLS-Zertifikat gibt (`https://217.x.x.x:8050` wird
abgelehnt).

Lösung: Du leitest `localhost:3000` per SSH auf den Bot-Port. Damit *ist*
localhost:3000 auf deinem Gerät der Bot — nur für den einmaligen Verbinden-Klick.

(Wer eine echte Domain + HTTPS hat, kann stattdessen `TWITCH_REDIRECT_URI` auf
`https://domain.de/api/twitch/oauth/callback` setzen und braucht keinen Tunnel.)

## 1. App auf Twitch anlegen

https://dev.twitch.tv/console/apps → **Register Your Application**
- **OAuth Redirect URLs**: `http://localhost:3000/api/twitch/oauth/callback`
- Danach zeigt die App **Client ID** und (per Knopf) **Client Secret**.

## 2. In die .env eintragen

```
TWITCH_CLIENT_ID=<deine Client ID>
TWITCH_CLIENT_SECRET=<dein Client Secret>
TWITCH_CHANNEL=logikabsolutfehlamplatz
```

`TWITCH_REDIRECT_URI` **leer lassen** (Default localhost:3000). Bot neu starten.

## 3. Tunnel öffnen

Auf deinem PC oder Handy (Termius) — nicht auf dem Server:

```
ssh -L 3000:localhost:8050 dein-user@217.182.138.35
```

Das leitet localhost:3000 (dein Gerät) auf Port 8050 (Bot am Server). Fenster
offen lassen, solange du verbindest.

## 4. Verbinden

Im **selben** Gerät, wo der Tunnel läuft, den Browser öffnen:

```
http://localhost:3000
```

**Nicht** die Server-IP — der ganze Flow muss über localhost:3000 laufen, sonst
passt der Redirect nicht. Dann System-Tab → **Twitch verbinden** → zustimmen.

Danach ist der Refresh-Token gespeichert. Der Zähler läuft und erneuert sich
selbst. Den Tunnel kannst du schließen.

## Der alte manuelle Token

`TWITCH_EVENTSUB_TOKEN` funktioniert weiter als Fallback, falls gesetzt — läuft
aber nach ~60 Tagen ab. Der OAuth-Weg ist der empfohlene Ersatz.
