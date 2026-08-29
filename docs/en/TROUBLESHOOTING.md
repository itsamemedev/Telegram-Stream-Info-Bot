# Troubleshooting

> 🌐 **English** · [Deutsch](../TROUBLESHOOTING.md)

The common failure patterns and where their cause really sits. Entry point in
the README: **[🩺 Troubleshooting](../../README.en.md#-troubleshooting)**.

---

## First: ask the bot itself

```bash
curl -s localhost:8050/api/selftest | python3 -m json.tool
```

It summarises what would otherwise be five separate log greps: dead broadcast
targets, the YouTube reason, defence permissions, disturbed background loops,
silent core loops, disk fill level — **every finding with the command that fixes
it**.

---

## “It stopped working” — silent `except` blocks are the main enemy

The bot catches broadly and logs at `warning`/`debug`. A `log.warning` **never**
shows up in an ERROR log — that is how a dead Discord gateway stayed invisible
for months. When something “stopped working”, look for the `except` that is
eating the reason first.

For periodic loops there is `_loop_fehler(name, exc)`: the first report goes out
immediately at `error` level with a traceback, after that at most one every 15
minutes — carrying the number of suppressed cases. Every long-running watchdog
belongs there, never on `log.debug` and never on `pass`.

The only paths that may legitimately stay silent are cleanup paths whose failure
is meaningless (`proc.terminate()` on a dead process, `os.remove()` on an
already-deleted file) and the error channel itself — logging there creates
recursion.

---

## Recordings fail

```
KEIN Recorder installiert — Aufnahmen werden FEHLSCHLAGEN.
```

```bash
sudo apt install ffmpeg        # recommended, for the native path
pip install -U yt-dlp          # fallback recorder
```

The recorder falls back in three stages: native (ffmpeg) → streamlink → yt-dlp.
Before every spawn a preflight GET runs, so no ffmpeg spends minutes running
against a 404.

---

## The AI does not answer / answers are cut off

```bash
python3 -c "import nc.freeai as f; print(f.diagnose())"
```

Shows per backend: free/blocked, latency, keyless/KEY, last error. For truncated
answers raise `BRAIN_LLM_MAX_TOKENS`, for timeouts `BRAIN_LLM_TIMEOUT_S` — with
CPU inference the two hang together.

`REACTION_AI_TIMEOUT` deliberately stays **short**: the live reaction has to be
snappy, otherwise the watchdog raises an alarm.

---

## Configuration is not picked up

**Module constants freeze the `.env`.** The `.env` is partly loaded only after
the first imports. Always read configuration through a function
(`_backend_conf()`), never as a module constant.

---

## “Online” does not mean “the process is running”

Twitch and YouTube carry `onfail=ignore` in the `tee` muxer — so that a stuck
Twitch does not drag Kick down with it. That is exactly why ffmpeg keeps running
when they drop out: the panel showed three green targets while nothing arrived
on two platforms.

`_restream_verify_loop` therefore polls **the platforms themselves**
periodically (Kick keyless, Twitch Helix, YouTube Data API). The four rules in
`nc/restream_guard.py` against restart loops are in the README under
**[📡 Restream](../../README.en.md#-restream)**.

---

## When a contract in `test_restream.py` breaks

The static contracts anchor themselves to the **literal source text** of
`bot.py`. If a signature changes, the contract breaks even though the code is
right. The same goes for windows of the form `src[i:i + 3000]`: if a function
grows past them, the test reports something as missing that sits two lines
further down.

**Before fixing the code, check whether the contract or only its anchor is
broken.**

---

Next: **[`DEPLOY.md`](DEPLOY.md)** (rolling out and rolling back) ·
**[`CROWDSEC.md`](../CROWDSEC.md)** (defence panel, German) ·
**[`START_HIER.txt`](../START_HIER.txt)** (first aid in one command, German)
