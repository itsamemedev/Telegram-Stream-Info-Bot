# Connecting YouTube (B121)

> 🌐 **English** · [Deutsch](../SETUP_YT_OAUTH.md)

Since build B121 there is a button for this in the dashboard — exactly like for
Twitch. The route through the Google OAuth Playground that used to be necessary
is gone.

## Once in the Google Cloud Console

1. console.cloud.google.com → create a project (or pick an existing one)
2. “APIs & Services” → Library → enable **YouTube Data API v3**
3. “APIs & Services” → OAuth consent screen
   - User type: External
   - Add your Google account as a test user
   - **Important:** while the app is in “Testing”, refresh tokens expire after
     7 days and the chat goes silent without a word. Publish it to
     “In production” as soon as it works.
4. “Credentials” → OAuth client ID → type: **Web application**
   - Authorised redirect URI:
     `http://localhost:3000/api/youtube/oauth/callback`
   - Copy the client ID and client secret

## Into the .env

    YOUTUBE_CLIENT_ID=...
    YOUTUBE_CLIENT_SECRET=...
    YOUTUBE_CHANNEL=@yourchannel

`YOUTUBE_REFRESH_TOKEN` is **no longer needed**. An existing value keeps
working, but the flow supersedes it as soon as you connect once.

Restart the bot.

## Connecting

Google only allows HTTPS or `localhost` as a redirect URI — a bare server IP
does not work. So tunnel once:

    ssh -L 3000:localhost:8050 your-user@<server>

Then open `http://localhost:3000` in the browser (not the IP), scroll to the
**“YouTube verbinden”** panel and click. Be logged in with the channel account.

After you approve, the bot stores the refresh token in
`recordings/youtube_oauth.json` (mode 0600) and renews the access itself. The
tunnel is not needed afterwards.

Alternative without a tunnel: your own domain with HTTPS, then set
`YOUTUBE_REDIRECT_URI=https://your-domain/api/youtube/oauth/callback` and enter
the same value in the Google app.

## What works afterwards

| Function | Requires |
|---|---|
| Viewer count (exact, not rounded) | youtube.readonly |
| Subscriber count | youtube.readonly |
| Reading the live chat | keyless (scrape), worked before already |
| The AI moderator writing in chat | youtube.force-ssl |
| Counting Super Chats as donations | youtube.force-ssl |

The flow fetches both scopes in one go.

## Checking

    curl -s localhost:8050/api/youtube/oauth/status | jq
    curl -s localhost:8050/api/channels/status | jq .youtube

`"source":"api"` = connected, exact numbers.
`"source":"scrape"` = not connected, keyless fallback (rounded subscriber count).

## When it jams

**“Google gave no refresh token”** — the app was already authorised once. Revoke
the access under myaccount.google.com/permissions, then connect again.

**Dead after ~7 days (`invalid_grant` in the log)** — the app is still in
“Testing”. Set the consent screen to “In production” and connect once more.

**`redirect_uri_mismatch`** — the URI in the Google app has to match the one
shown in the panel character for character, including the path and without a
trailing slash.
