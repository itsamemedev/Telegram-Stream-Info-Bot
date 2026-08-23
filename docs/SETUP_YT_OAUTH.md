# YouTube verbinden (B121)

Seit Build B121 gibt es dafuer einen Knopf im Dashboard — genau wie bei Twitch.
Der frueher noetige Weg ueber den Google OAuth Playground entfaellt.

## Einmalig in der Google Cloud Console

1. console.cloud.google.com -> Projekt anlegen (oder vorhandenes waehlen)
2. "APIs & Dienste" -> Bibliothek -> **YouTube Data API v3** aktivieren
3. "APIs & Dienste" -> OAuth-Zustimmungsbildschirm
   - Nutzertyp: Extern
   - Dein Google-Konto als Testnutzer eintragen
   - **Wichtig:** Wenn die App auf "Testing" steht, laufen Refresh-Tokens
     nach 7 Tagen ab und der Chat verstummt still. Auf "In production"
     veroeffentlichen, sobald es laeuft.
4. "Anmeldedaten" -> OAuth-Client-ID -> Typ: **Webanwendung**
   - Autorisierte Redirect-URI:
     `http://localhost:3000/api/youtube/oauth/callback`
   - Client-ID und Client-Secret kopieren

## In die .env

    YOUTUBE_CLIENT_ID=...
    YOUTUBE_CLIENT_SECRET=...
    YOUTUBE_CHANNEL=@deinkanal

`YOUTUBE_REFRESH_TOKEN` wird **nicht** mehr gebraucht. Ein vorhandener Wert
funktioniert weiter, wird aber vom Flow abgeloest, sobald du einmal verbindest.

Bot neu starten.

## Verbinden

Google erlaubt als Redirect-URI nur HTTPS oder `localhost` — eine nackte
Server-IP geht nicht. Deshalb einmal tunneln:

    ssh -L 3000:localhost:8050 dein-user@<server>

Dann `http://localhost:3000` im Browser oeffnen (nicht die IP), zum Panel
**„YouTube verbinden"** scrollen und klicken. Als Kanal-Konto eingeloggt sein.

Nach dem Zustimmen speichert der Bot den Refresh-Token unter
`recordings/youtube_oauth.json` (Rechte 0600) und erneuert den Zugang selbst.
Der Tunnel wird danach nicht mehr gebraucht.

Alternative ohne Tunnel: eigene Domain mit HTTPS, dann
`YOUTUBE_REDIRECT_URI=https://deine-domain/api/youtube/oauth/callback` setzen
und denselben Wert in der Google-App eintragen.

## Was danach funktioniert

| Funktion | Braucht |
|---|---|
| Zuschauerzahl (exakt, nicht gerundet) | youtube.readonly |
| Abonnentenzahl | youtube.readonly |
| Live-Chat lesen | keyless (Scrape), lief schon vorher |
| KI-Moderator schreibt im Chat | youtube.force-ssl |
| Superchats als Spende zaehlen | youtube.force-ssl |

Beide Scopes holt der Flow in einem Rutsch.

## Pruefen

    curl -s localhost:8050/api/youtube/oauth/status | jq
    curl -s localhost:8050/api/channels/status | jq .youtube

`"source":"api"` = verbunden, exakte Zahlen.
`"source":"scrape"` = nicht verbunden, keyloser Rueckfall (gerundete Abos).

## Wenn es klemmt

**„Google gab keinen Refresh-Token"** — die App war schon einmal autorisiert.
Unter myaccount.google.com/permissions den Zugriff entziehen, dann neu
verbinden.

**Nach ~7 Tagen tot (`invalid_grant` im Log)** — die App steht noch auf
"Testing". Im Zustimmungsbildschirm auf "In production" setzen und einmal
neu verbinden.

**`redirect_uri_mismatch`** — die URI in der Google-App muss zeichengenau der
im Panel angezeigten entsprechen, inklusive Pfad und ohne Slash am Ende.
