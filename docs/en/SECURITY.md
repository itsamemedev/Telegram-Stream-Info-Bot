# Security policy

> 🌐 **English** · [Deutsch](../SECURITY.md)

## Supported versions

| Version | Supported |
|---|---|
| 4.3.x (`Clear View`) | ✅ |
| 4.2.x (`Decomposed Core`) | ⚠️ critical holes only |
| < 4.2 | ❌ |

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

Around 523 variables, among them cookies, OAuth tokens, API keys and RTMP stream
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

Last complete pass: **v4.3-W58** (the one before: v4.0-W118). The same classes
were covered as back then, against today's code:

| Class | Result |
|---|---|
| Code execution (`eval`/`exec`/`pickle`/`yaml.load`) | no hit |
| `shell=True` | one hit — `SWAP_CLEAR_CMD`, the exception explained below |
| SQL injection, incl. the LLM-translated query | no hit |
| Path traversal in every file route | no hit |
| Dashboard auth (token, PIN, rate limit, constant time) | no hit |
| Secrets in logs and API responses | no hit |
| XSS in the three templates | **one finding, fixed (W58)** |
| SSRF | no hit |
| OAuth CSRF | one note, see below |
| Dependencies | still open, see below |

**What was actually checked, not merely asserted:**

*SQL.* Six places build their statement with an f-string. All of them
interpolate hard-coded column names (`"name=?"`) or a table list written out in
the source; values are bound throughout. The NL→SQL fallback
`_rule_based_sql` **never** puts the question text into the statement — only an
internal time-window constant. The LLM variant is limited to `select`/`with`
and a single statement.

*Secrets in logs.* The riskiest path is new: since v4.2-W46 the audio tap's
`stderr` is read at all, and it contains the signed source URL. It goes through
`_log_sicher` (`nc/logsafe.redact_pull_urls`), with the reasoning at the line.
No raw stream URL in a log, none in an API response.

*Path traversal.* Icons via a whitelist, downloads via `realpath` +
`commonpath` against the permitted directory, thirteen further places via
`nc.sicherpfad`.

*Dashboard auth.* Token and PIN are compared with `hmac.compare_digest`; failed
attempts are counted per IP and lock for 60 seconds, and the table is bounded.

The XSS finding from W58 has a contract in `test_nc_modules.py`; a regression
shows up in the verification chain, not in production.

### Three things stay open deliberately

They are **not** negligence but operator decisions:

- **`SWAP_CLEAR_CMD` runs with `shell=True`.** The shell is needed for `&&`.
  Anyone who can write the `.env` can execute arbitrary code anyway — that file
  is the root of trust, not this line.

- **Unpinned dependencies** (see above). Freezing is server work; guessed
  version numbers would be worse than none. As of today: zero of 63 entries in
  `requirements.txt` are pinned.

- **The OAuth `state` for Twitch and YouTube lives in memory only.** Both check
  it when one was issued — but not when no flow is running. Kick is stricter: it
  persists the `state` and rejects any callback that does not match. Making
  Twitch and YouTube equally strict would mean persisting the `state` as well,
  otherwise a legitimate flow breaks across a restart. As long as the dashboard
  listens on `127.0.0.1` as intended, the callback is not reachable from
  outside; anyone exposing it publicly should close this first.

---

## What is explicitly **not** a hole

- An open dashboard that someone put on the internet themselves.
- An `.env` that someone committed themselves.
- Rate limits or blocks by the third-party platforms (TikTok, Kick, Twitch,
  YouTube).
- False positives of the moderation heuristic. That is a normal issue — the
  shield is deliberately tuned to zero false positives, and reports are welcome.
