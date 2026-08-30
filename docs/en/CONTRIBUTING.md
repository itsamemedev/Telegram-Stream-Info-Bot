# Contributing to NIGHTCRAWLER

> 🌐 **English** · [Deutsch](../CONTRIBUTING.md)

Thank you for wanting to contribute. This project runs in production around the
clock — a deployment goes straight against production. The rules here are
therefore not matters of style; they grew out of real outages.

---

## Contents

- [Development environment](#development-environment)
- [The mandatory verification chain](#the-mandatory-verification-chain)
- [Architecture rules](#architecture-rules)
- [Navigating the monolith](#navigating-the-monolith)
- [Code style](#code-style)
- [Pitfalls that have already bitten](#pitfalls-that-have-already-bitten)
- [Commits and pull requests](#commits-and-pull-requests)
- [Bug reports](#bug-reports)
- [Licence of your contributions](#licence-of-your-contributions)

---

## Development environment

```bash
git clone https://github.com/itsamemedev/Telegram-Stream-Info-Bot.git
cd Telegram-Stream-Info-Bot

python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
pip install pyflakes ruff            # checking tools

cp .env.example .env                 # adjust it
```

System packages (not through pip): `ffmpeg`, `streamlink`, `yt-dlp`.

**On Windows:** the interpreter is called `python` there, not `python3`. Set
`$env:PYTHONUTF8="1"` first — the tests open `bot.py` without `encoding=`, so
without UTF-8 mode cp1252 kicks in and they die with a `UnicodeDecodeError`
instead of checking anything.

---

## The mandatory verification chain

**It runs before every pull request. In full, not in part.**

```bash
python3 -m py_compile <changed .py>
python3 -m pyflakes   <changed .py>                        # 0 findings
python3 -m ruff check --select F,E9,B --ignore B905 <changed .py>
python3 tools/ncpatch.py check                             # check templates
python3 test_smoke.py
python3 test_nc_modules.py
python3 test_restream.py
```

Always in addition:

- No duplicate top-level defs (`ast.parse` → `module.body`).
- No duplicate Flask routes **including `methods=`** — the same path with `GET`
  and `POST` is **not** a duplicate. A naive regex raises a false alarm here.
- For JavaScript in `templates/*.html`: extract the script blocks and run
  `node --check`. Check JSON-LD as JSON, not as JS.

### `test_smoke.py` does not run everywhere

It **actually** executes `bot.py` and needs the whole runtime stack for that
(flask, telegram, discord, dotenv, streamlink, yt-dlp, psutil). On a development
machine without that stack it fails — there `py_compile` and `pyflakes` catch
most of it (NameError, ordering traps). This test belongs on the server.

### When a contract in `test_restream.py` breaks

The static contracts anchor themselves to the **literal source text** of
`bot.py`. If a signature changes, the contract breaks even though the code is
right — that has happened three times already (`stop(self, rid)` became
`stop(self, rid, _keep_desired=False)`). The same goes for windows of the form
`src[i:i + 3000]`: if the function grows past them, the test reports something
as missing that sits two lines further down.

> **Before fixing the code, check whether the contract or only its anchor is
> broken.**

---

## Architecture rules

### 1. No back-imports

`nc/*` and `brain/*` **never** import from `bot.py`. Configuration comes
exclusively through `configure(...)` injection.

```python
# ❌ wrong — couples the module to the monolith, creates circular imports
from bot.py import DB_PATH, log

# ✅ right — the caller injects what the module needs
def configure(*, db_conn, log, cfg):
    global _db_conn, _log, _cfg
    _db_conn, _log, _cfg = db_conn, log, cfg
```

That keeps both libraries testable in isolation — no network, no database, no
bot.

### 2. `brain/` is stdlib-only

Thread-based, `urllib` instead of `aiohttp`. Without the `brain/` directory the
bot has to start exactly as it does with it — every building block is additive,
fail-open, and individually switchable through an env flag.

### 3. Do not mix up money

`REVENUE_PLATFORMS = ("kick", "twitch", "youtube", "manuell")`. **TikTok never
belongs there** — TikTok gifts go to the tracked streamer, not to our own
channels. They are stored as `kind="gift"`, never as `donation`, and never enter
a monetary total.

`/api/donations/summary` is live telemetry built from **estimates**.
`nc/ledger.py` holds booked **payouts** for the tax office. Never derive one
from the other. Ledger entries are append-only with a hash chain; a correction
is a counter-entry, not an overwrite.

---

## Navigating the monolith

`bot.py` has almost 30,000 lines. That file is **never** read in full and
**never** searched blindly. First ask where something is, then fetch the
excerpt:

```bash
python3 tools/ncpatch.py find "donations"          # where is X?
python3 tools/ncpatch.py sym  bot.py api_brain     # line range of a symbol
python3 tools/ncpatch.py show bot.py 24750 24810   # only this excerpt
python3 tools/ncpatch.py grep "tree.command" bot.py -C 3
python3 tools/ncpatch.py verify patches/x.json     # dry run
python3 tools/ncpatch.py apply  patches/x.json     # all-or-nothing, writes a .bak
```

> **Working on taking the monolith apart?** Then read
> [`docs/MODULARISIERUNG.md`](../MODULARISIERUNG.md) (German) first — it holds
> the per-wave procedure, the rule about migrating contracts, and what is
> explicitly not done.

`find` answers from `.claude/INDEX.md`. **After every change to routes, slash
commands or top-level functions, rebuild the map** and commit it:

```bash
python3 tools/ncpatch.py map
```

The diff on `INDEX.md` immediately shows which routes and functions a change
touched.

After changes to configuration variables, additionally:

```bash
python3 tools/gen_env_example.py
```

---

## Code style

- **German.** Code comments and all user-facing output are written in German;
  the English strings live in `locales/en.json` (see
  [multilingual support](#multilingual-support) below).
- **Comments explain *why*, not *what*** — preferably with the concrete failure
  the line prevents:

  ```python
  # list() ist Pflicht: ein paralleler Restream-Stop ruft .pop() auf demselben
  # dict — ohne Kopie stirbt die Schleife mit "dict changed during iteration".
  for rid, proc in list(_RESTREAM_ACTIVE_ALL.items()):
  ```

- Line length up to 127 characters.
- New configuration gets a **default** that works without an entry in the
  `.env`. Empty values (`NAME=`) must never crash.
- New functionality is **switchable off** through an env flag.

### Multilingual support

The user-facing language is driven by `locales/<lang>.json`. **The German string
is the key** — so the source stays readable and a missing entry falls back to
German instead of a bare key name. After changing user-facing text:

```bash
python3 tools/i18n_extract.py --check en     # missing and orphaned entries
python3 tools/i18n_extract.py --write en     # add the missing keys (empty)
```

Log lines stay German on purpose: they are for the operator, not for users, and
they never pass through the translation layer.

---

## Pitfalls that have already bitten

### Silent `except` blocks are the main enemy

The bot catches broadly and logs at `warning`/`debug`. A `log.warning` **never**
shows up in an ERROR log — that is how a dead Discord gateway stayed invisible
for months.

For periodic loops there is **`_loop_fehler(name, exc)`**: the first report goes
out immediately at `error` level with a traceback, after that at most one every
15 minutes — carrying the number of suppressed cases. Every long-running
watchdog belongs there, never on `log.debug` and never on `pass`.

The only paths that may legitimately stay silent are cleanup paths whose failure
is meaningless (`proc.terminate()` on a dead process, `os.remove()` on an
already-deleted file) — and the error channel itself, where logging creates
recursion.

### Module constants freeze the `.env`

The `.env` is partly loaded only after the first imports. Read configuration as
a **function** (`_backend_conf()`), never as a module constant.

### A one-shot `await` without a supervisor

Every long-running client needs reconnect with backoff **and** an abort
criterion for deterministic errors.

### Guards as an object attribute

`getattr(client, "_started", False)` breaks as soon as the object is recreated →
parallel endless loops. Guard **module-globally**.

### Contract breaks against `brain/`

When changing `router.route(topic, payload)`, check every call site:
`grep -n 'router.route('`. A key drift (`prompt` vs. `question`) once failed
only on the Telegram path, because the Flask route used the right key.

### Iterating over mutable state

Every iteration over `_RESTREAM_ACTIVE_*` and related dicts needs `list()` —
parallel tasks `.pop()` on them.

### File handles

`/proc` files and everything else always with `with open(...)`. In the health
loop a bare `open()` adds up against the fd limit.

---

## Commits and pull requests

**Commit messages**: first line in the imperative, short, what changes. Then a
blank line and the *why* — preferably with the observed symptom.

```
Restream-Ziel-Verifikation gegen Plattform-APIs härten

Bei tee mit onfail=ignore läuft ffmpeg weiter, wenn Twitch wegbricht.
Das Panel zeigte drei grüne Ziele, während auf zwei Plattformen nichts
ankam. Der Verify-Loop fragt jetzt die Plattformen selbst.
```

**Pull requests**:

1. Branch from `main`: `git checkout -b feature/my-feature`
2. Keep the change small and **individually verifiable** — deployment goes
   against production, a rollback has to be possible.
3. Run the mandatory verification chain and state the result in the PR.
4. Regenerate `.claude/INDEX.md` and `.env.example` if needed and commit them.
5. Fill in the PR template.

**Do not commit:** `.env`, cookies, OAuth token files, databases, recordings,
logs, build archives. `.gitignore` already blocks that — still check
`git status` before you push. A secret that has been committed once is still in
the history after you delete it.

---

## Bug reports

Use the issue template. Always helpful:

```bash
journalctl -u nightcrawler -n 200 --no-pager     # log excerpt
curl -s localhost:8050/api/selftest | python3 -m json.tool
python3 -c "import nc.freeai as f; print(f.diagnose())"   # for AI problems
```

> **Redact before pasting:** logs can contain cookies, tokens and stream keys.

**Security holes do not belong in a public issue** — see
[`SECURITY.md`](SECURITY.md).

---

## Licence of your contributions

By opening a pull request you place your contribution under the
**GNU General Public License v3.0 or later** — the same licence as the project.
See [`LICENSE`](../../LICENSE).

If you bring third-party code with you, add it to
[`THIRD_PARTY_LICENSES.md`](../THIRD_PARTY_LICENSES.md) and check that its
licence is GPLv3-compatible.
