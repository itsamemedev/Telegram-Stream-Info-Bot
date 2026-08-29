# Security policy

> 🌐 **English** · [Deutsch](../SECURITY.md)

## Supported versions

| Version | Supported |
|---|---|
| 4.0.x (`Restream Control Room`) | ✅ |
| 3.7.x (`control room foundation`) | ⚠️ critical holes only |
| < 3.7 | ❌ |

## Reporting a hole

**Please do not open a public issue.**

Report security holes through **[GitHub Security Advisories](https://github.com/itsamemedev/Telegram-Stream-Info-Bot/security/advisories/new)**
(“Report a vulnerability”) or by e-mail to the repository owner.

Helpful in the report:

- Affected file / route / module and version
- How to reproduce the problem
- Impact: what can an attacker achieve with it?
- If you have one: a suggested fix

**Please redact log excerpts before sending them** — they regularly contain
cookies, OAuth tokens and stream keys.

### What you can expect

| Step | Timeframe |
|---|---|
| Acknowledgement of receipt | within 72 hours |
| First assessment | within 7 days |
| Fix or schedule | by severity, critical holes first |
| Credit in the advisory | on request, gladly |

Please give us time for a fix before you publish details.

---

## Operational notes — the most common pitfalls

Most real risks in this project come from operating it, not from the code. These
points are mandatory:

### The `.env` is the crown-jewel store

Around 470 variables, among them cookies, OAuth tokens, API keys and RTMP stream
keys. A stream key lets anyone broadcast on your channel.

```bash
chmod 600 .env
```

It is listed in `.gitignore` and never ships in the release archive. **A secret
that has been committed once is still in the history after you delete it** —
then the only remedy is to revoke the key and issue a new one.

### The dashboard does not belong on the open internet

The default is `127.0.0.1:8050`. Access runs through an SSH tunnel:

```bash
ssh -L 3000:localhost:8050 ubuntu@<server-ip>
```

Anyone who makes the dashboard publicly reachable puts a complete remote-control
room on the internet — including the recording archive, the revenue journal and
restream control. If it has to be: a reverse proxy with TLS **and**
authentication in front of it, set `DASHBOARD_TOKEN`, and enable the CrowdSec
integration (see [`docs/CROWDSEC.md`](../CROWDSEC.md), German).

### Do not bypass log redaction

When `streamlink` and `ffmpeg` command lines are logged, cookie headers and
stream keys are masked. Anyone changing how the command lines are built must
make sure the redaction path still applies.

### Set up a dead-man's report

If the process dies completely, nobody else will tell you — not even when the
reason was an attack:

```bash
chmod +x tools/notify_failure.sh
sudo systemctl edit nightcrawler   # → [Unit] OnFailure=nightcrawler-notify@%n.service
```

### Freeze the dependencies

`requirements.txt` deliberately leaves versions open. Freeze the running state
on the server and keep it up to date:

```bash
python3 -m pip freeze > requirements.lock.txt
```

## Audit status

Last complete pass: **v4.0-W118**. Covered: code execution
(`eval`/`exec`/`pickle`/`yaml.load`), `shell=True`, SQL injection including the
LLM-translated query, path traversal in every file route, dashboard auth (token,
PIN, rate limit, constant time), XSS in all three templates, SSRF, OAuth CSRF,
open redirect, secrets in logs and API responses, file permissions of the token
stores, dependencies.

Seven findings fixed — details in the [CHANGELOG](../CHANGELOG.md) under W118
(German). Each one has a contract in `test_restream.py`
(`test_v40_w118_sicherheitsaudit`); a regression therefore shows up in the
verification chain, not in production.

Two things stay open deliberately and are **not** negligence but operator
decisions:

- **`SWAP_CLEAR_CMD` runs with `shell=True`.** The shell is needed for `&&`.
  Anyone who can write the `.env` can execute arbitrary code anyway — that file
  is the root of trust, not this line.
- **Unpinned dependencies** (see above). Freezing is server work; guessed
  version numbers would be worse than none.

---

## What is explicitly **not** a hole

- An open dashboard that someone put on the internet themselves.
- An `.env` that someone committed themselves.
- Rate limits or blocks by the third-party platforms (TikTok, Kick, Twitch,
  YouTube).
- False positives of the moderation heuristic. That is a normal issue — the
  shield is deliberately tuned to zero false positives, and reports are welcome.
