# Setting up CrowdSec for Azrael Sentinel

> 🌐 **English** · [Deutsch](../CROWDSEC.md)

As of v4.0-W23

> **The most important rule first:** do **not assume** the LAPI port —
> **determine** it (step 2). “8083” is the value from one particular setup, not
> the default. CrowdSec starts on **8080** by default. A wrongly assumed port is
> the most common cause of “it will not connect”.

---

## What the bot does with CrowdSec

The bot **blocks nothing itself**. It *reads* the decisions (bans) CrowdSec has
made and shows them in the dashboard (panel **Abwehr · CrowdSec** + world map).
The actual blocking is done by a **bouncer** (step 4c).

Two routes; the bot automatically takes the first one when a key is set:

* **Route A — bouncer key (recommended, no root).** The bot queries the LAPI
  over HTTP with an API key. **No sudo rule needed**, revocable at any time.
* **Route B — `cscli`** (fallback). Needs root → a sudoers rule (3b).

**New in W23:** the dashboard panel **Abwehr · CrowdSec** has a
**“Verbindung testen”** (test connection) button. It takes **exactly the route
the bot takes** and shows the mode, the exact URL queried, whether a key is set,
plus the concrete failure reason and the command that fixes it. After every step
here: press that button — it is the most honest feedback, more so than a `curl`
you built yourself.

---

## 1. Is CrowdSec installed?

```bash
sudo systemctl status crowdsec        # has to be "active (running)"
cscli version
```

If it is missing:

```bash
curl -s https://install.crowdsec.net | sudo sh
sudo apt install crowdsec
```

---

## 2. Determine the REAL LAPI address (do not guess)

CrowdSec tells you itself where its LAPI listens:

```bash
sudo cscli lapi status
```

The line **“Trying to authenticate … on http://HOST:PORT/”** is the address you
need — host **and** port. To cross-check, the configuration:

```bash
grep -A2 'server:' /etc/crowdsec/config.yaml     # listen_uri: 127.0.0.1:PORT
```

> **Note down HOST and PORT from that output.** Everything below uses exactly
> those values. This guide writes `PORT` — substitute your real port (e.g. 8080
> or, if you changed it, 8083).

**Only if you deliberately want to change the port**, in
`/etc/crowdsec/config.yaml`:

```yaml
api:
  server:
    listen_uri: 127.0.0.1:PORT
```

Then `sudo systemctl restart crowdsec` and `sudo cscli lapi status` again — it
has to report “successfully interact with LAPI”.

> Is the LAPI running with **TLS** (a `tls:` section under `api.server` in the
> config.yaml, URL starting with `https://`)? Then the bot cannot query it at
> the moment — run the LAPI for 127.0.0.1 over `http` (locally that is safe) or
> use route B (cscli).

---

## 3. Route A — create a bouncer key (recommended)

```bash
sudo cscli bouncers add azrael-dashboard
```

CrowdSec prints an API key **once**. Put it in the bot's **`.env`** (not in the
shell):

```bash
CROWDSEC_BOUNCER_KEY=<the printed key>
CROWDSEC_LAPI_HOST=127.0.0.1
CROWDSEC_LAPI_PORT=PORT           # the REAL port from step 2
# Alternatively the complete address instead of host/port:
# CROWDSEC_LAPI_URL=http://127.0.0.1:PORT
```

Restart the bot so the `.env` is read:

```bash
sudo systemctl restart tiktok-bot
```

Then in the dashboard **Abwehr · CrowdSec → “Verbindung testen”**. Expected:
“verbunden · LAPI · Schlüssel gesetzt”. If an error shows there, the button
gives the reason and the command.

### 3a. Cross-checking by hand — the key trap

The key sits in the **`.env`**, **not** in your shell. A blind

```bash
curl -H "X-Api-Key: $CROWDSEC_BOUNCER_KEY" http://127.0.0.1:PORT/v1/decisions
```

sends an **empty** key → **403** → and you wrongly conclude it is broken. One of
these two is right:

```bash
# a) load the variables from the .env into the current shell:
set -a; . /path/to/.env; set +a
curl -s -H "X-Api-Key: $CROWDSEC_BOUNCER_KEY" \
     "http://127.0.0.1:$CROWDSEC_LAPI_PORT/v1/decisions" ; echo

# b) or paste the key literally (not as a variable):
curl -s -H "X-Api-Key: THE_REAL_KEY" \
     http://127.0.0.1:PORT/v1/decisions ; echo
```

* `null` or `[]` → **connected, nobody currently banned** (success, not an error).
* `[{...}]` → connected, there are bans.
* `access forbidden` / HTTP 403 → the key is wrong or revoked → create a new one.

Show the created accesses / revoke one:

```bash
sudo cscli bouncers list
sudo cscli bouncers delete azrael-dashboard
```

---

## 3b. Route B only: letting the bot call `cscli` as root

`cscli` reads LAPI credentials owned by **root**. Without permission you get
“permission denied” or a Go panic. A password-less sudo rule **for that one
command only** — with the path exactly as `command -v cscli` prints it:

```bash
echo "$(whoami) ALL=(root) NOPASSWD: $(command -v cscli)" \
  | sudo tee /etc/sudoers.d/nightcrawler
sudo chmod 440 /etc/sudoers.d/nightcrawler
sudo systemctl restart tiktok-bot
sudo -n cscli decisions list -o json | head    # has to run without a password
```

If a bouncer key is set (route A), 3b is **not** needed.

---

## 4. What is monitored and blocked

### 4a. Collections for your services

```bash
sudo cscli collections install crowdsecurity/sshd
sudo cscli collections install crowdsecurity/nginx          # if nginx serves the website
sudo cscli collections install crowdsecurity/base-http-scenarios
sudo systemctl reload crowdsec
sudo cscli collections list
```

### 4b. Monitoring the dashboard itself

Add to `/etc/crowdsec/acquis.yaml` (the bot log through journald):

```yaml
---
source: journalctl
journalctl_filter:
  - "_SYSTEMD_UNIT=tiktok-bot.service"
labels:
  type: syslog
```

```bash
sudo systemctl reload crowdsec
sudo cscli metrics          # "Acquisition" has to show lines for the source
```

### 4c. The bouncer — only here does anything actually get blocked

```bash
sudo apt install crowdsec-firewall-bouncer-iptables
sudo systemctl status crowdsec-firewall-bouncer
```

A test ban (appears in the dashboard within ~1 min, then remove it again):

```bash
sudo cscli decisions add --ip 203.0.113.10 --duration 5m --reason "Test"
sudo cscli decisions list
sudo cscli decisions delete --ip 203.0.113.10
```

---

## 5. Interplay with the dashboard token

* **DASHBOARD_TOKEN** = who may enter the dashboard.
* **CrowdSec** = who is not let through at all after failed attempts.

If a reverse proxy sits in front, set this in the `.env`, otherwise the bot only
sees the proxy's IP:

```bash
TRUSTED_PROXIES=<IP of the proxy>
```

---

## 6. Troubleshooting — what the “Verbindung testen” button shows

| Display / status | Meaning | Fix |
|---|---|---|
| `verbunden`, 0 banned | Everything runs, nothing detected yet | Normal. Test with 4c |
| `kein_zugang` (401/403) | Bouncer key wrong or revoked | `sudo cscli bouncers list`, create a new one if needed (step 3) |
| `lapi_pfad` (404) | LAPI reachable, but wrong port/service | Compare the port from step 2 with the `.env` |
| `lapi_tot` | Service/LAPI not answering (wrong port? TLS?) | Step 2, `sudo systemctl restart crowdsec` |
| `kein_sudo` (route B only) | sudo rule missing / wrong path | Step 3b (`command -v cscli`) |
| `fehlt` | CrowdSec not installed | Step 1 |

Useful commands:

```bash
sudo cscli lapi status          # LAPI address + reachable?
sudo cscli decisions list       # what is banned
sudo cscli metrics              # are log lines arriving
journalctl -u crowdsec -n 50    # service log
```

---

## 7. Short version

1. `sudo cscli lapi status` → **read the real HOST:PORT** (do not guess).
2. `sudo cscli bouncers add azrael-dashboard` → key into the `.env`
   (`CROWDSEC_BOUNCER_KEY` + `CROWDSEC_LAPI_PORT` with the real port).
3. `sudo systemctl restart tiktok-bot`.
4. Dashboard → **Abwehr · CrowdSec → “Verbindung testen”** → has to show
   “verbunden” (or the reason + fix).
5. Collections + `acquis.yaml` + firewall bouncer, then a test ban.
