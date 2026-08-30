# Connecting Twitch (follower counter)

> 🌐 **English** · [Deutsch](../SETUP_TWITCH_OAUTH.md)

The follower counter uses Twitch EventSub. You provide the client ID + secret and
click connect once — after that the bot renews the access itself.

## Why an SSH tunnel is needed

For OAuth redirect URLs Twitch demands **HTTPS** — with exactly one exception:
`http://localhost:PORT` is allowed. A bare server IP with HTTPS does NOT work,
because there is no valid TLS certificate for it (`https://217.x.x.x:8050` is
rejected).

The solution: you forward `localhost:3000` to the bot's port over SSH. That
makes localhost:3000 on your device *be* the bot — just for the one connect
click.

(Anyone with a real domain + HTTPS can instead point `TWITCH_REDIRECT_URI` at
`https://domain.tld/api/twitch/oauth/callback` and needs no tunnel.)

## 1. Create an app on Twitch

https://dev.twitch.tv/console/apps → **Register Your Application**
- **OAuth Redirect URLs**: `http://localhost:3000/api/twitch/oauth/callback`
- Afterwards the app shows the **Client ID** and (behind a button) the
  **Client Secret**.

## 2. Put it in the .env

```
TWITCH_CLIENT_ID=<your client ID>
TWITCH_CLIENT_SECRET=<your client secret>
TWITCH_CHANNEL=logikabsolutfehlamplatz
```

Leave `TWITCH_REDIRECT_URI` **empty** (it defaults to localhost:3000). Restart
the bot.

## 3. Open the tunnel

On your PC or phone (Termius) — not on the server:

```
ssh -L 3000:localhost:8050 your-user@217.182.138.35
```

That forwards localhost:3000 (your device) to port 8050 (the bot on the server).
Leave the window open while you connect.

## 4. Connect

On the **same** device where the tunnel runs, open the browser at:

```
http://localhost:3000
```

**Not** the server IP — the whole flow has to run through localhost:3000, or the
redirect will not match. Then go to the system tab → **Twitch verbinden** →
approve.

After that the refresh token is stored. The counter runs and renews itself. You
can close the tunnel.

## The old manual token

`TWITCH_EVENTSUB_TOKEN` keeps working as a fallback if it is set — but it
expires after ~60 days. The OAuth route is the recommended replacement.
