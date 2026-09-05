# NIGHTCRAWLER v37 — working brief

> 🌐 **English** · [Deutsch](CLAUDE.md)
>
> **The German [`CLAUDE.md`](CLAUDE.md) is the authoritative version** — that is
> the file Claude Code actually loads. This translation exists so English-
> speaking contributors can read the rules; when the two disagree, the German
> one wins.

TikTok live monitoring, recording, multi-target restream and AI moderation
(AZRAEL). A Python monolith plus two bot-free libraries, operated as a systemd
service on an 8-core Ubuntu box. Delivery happens as a ZIP laid over the
existing installation, not through `git pull` — see `.claude/skills/nc-betrieb`.
The GitHub repository carries history, CI and issues; it is not the deployment
route.

## The one rule

`bot.py` has **22,609 lines / 1.2 MB ≈ 293,000 tokens**. That file is **never**
read in full and **never** searched blindly. First ask where something is, then
fetch the excerpt:

    python tools/ncpatch.py find "donations"           # where is X? (~100 tokens)
    python tools/ncpatch.py sym  bot.py api_brain      # line range of a symbol
    python tools/ncpatch.py show bot.py 24750 24810    # only this excerpt
    python tools/ncpatch.py grep "tree.command" bot.py -C 3
    python tools/ncpatch.py map                        # rebuild the map
    python tools/ncpatch.py verify patches/x.json      # dry run
    python tools/ncpatch.py apply  patches/x.json      # all-or-nothing, writes a .bak
    python tools/ncpatch.py check                      # templates: duplicate IDs, CSS balance
    python tools/ncpatch.py docs                       # documentation numbers vs. the source

`find` answers from `.claude/INDEX.md` — 361 routes (34 in `bot.py`, 327 in
`nc/routes/`), 45 slash commands, 474 functions with line numbers. After changes
to routes, commands or top-level functions, run `map` again. Details: skill
`nc-navigation`.

For “who calls this?” and “what is the type?” the language server is cheaper
than any search: `findReferences`, `incomingCalls`, `goToDefinition`, `hover`.

On the author's Windows machine the interpreter is called **`python`**
(3.13.12); `python3` does not exist there. On the server it is `python3`.

## Layout

    bot.py               monolith: Telegram, Flask dashboard (34 own
                         routes), scraper, recorder, restream, schema (init_db).
                         Was called bot_v37.py until v4.0-W119 — keep that in
                         mind when searching old notes and patch files.
    discordbot.py        the Discord part (45 slash commands), lifted out in
                         v4.2-W15. It lives bot-side because it imports
                         discord.py and opens a gateway — not under nc/, which
                         stays bot-free. Everything reaches it via starte(ctx);
                         it NEVER imports from bot.py.
    nc/botctx.py         the one channel there: BotKontext (frozen).
    telegramversand.py   the delivery path for recordings (split_and_send_video),
                         lifted out in v4.2-W19. Bot-side as well: it needs
                         telegram.error at runtime. Gets five helpers via
                         konfiguriere(); never imports from bot.py.
    brain_bridge.py      adapter bot ↔ brain/ (M2)
    brain/               AI core: state, rules, router, agents, memory,
                         semantic, knowledge, scheduler, llm, report
    nc/                  132 domain modules: db, scraping, restream, oauth, ledger, i18n, …
    nc/routes/           36 Flask blueprints with 327 further API routes
    locales/             de.json, en.json — the translation catalogue
    templates/           dashboard.html, brain.html, overlay.html, PWA
    website/             lafap_index.html (the public site)
    tools/ncpatch.py     patch and verification tool
    docs/                every guide and the history — DEPLOY, START_HIER,
                         CONTRIBUTING, SECURITY, CHANGELOG, README_V37, the
                         SETUP_* guides, plus docs/en/ with the English
                         versions. In the root the only text files left are
                         README.md / README.en.md (entry point), CLAUDE.md
                         (the German working brief, which has to sit there or
                         Claude Code will not find it), this file and LICENSE.
    .claude/skills/      working instructions — here and only here does Claude
                         Code find them. They belong in the release archive
                         (they used to live under skills/, where they were
                         never loaded).

**The architectural boundary that holds:** `nc/*`, `brain/*` and
`discordbot.py` **never** import
from `bot.py`. Configuration comes through `configure(...)` injection. That
keeps both testable in isolation and prevents circular imports. `brain/` is
thread-based and stdlib-only (`urllib`, no `aiohttp`).

## The mandatory verification chain — before EVERY release

    python -m py_compile <changed .py>
    python -m pyflakes   <changed .py>        # 0 findings
    python -m ruff check --select F,E9,B --ignore B905 <changed .py>
    python tools/ncpatch.py check
    python tools/ncpatch.py docs
    python tools/i18n_extract.py --check en
    python test_smoke.py ; python test_nc_modules.py ; python test_restream.py

**On the author's Windows machine, set `$env:PYTHONUTF8="1"` first.** The tests
open `bot.py` without `encoding=`; without UTF-8 mode cp1252 kicks in and they
die with a `UnicodeDecodeError` instead of checking anything. On the server
UTF-8 is the default and nothing needs setting.

**`test_smoke.py` has run in CI since v4.1-W31** — job `Rauchtest (bot.py
laeuft wirklich)`. The old reasoning ("needs the full server stack") was wrong:
the test stubs TikTokLive and python-telegram-bot itself, everything else is
imported inside functions. What remains is five packages in
`requirements-smoke.txt`, about 20 seconds to install. Locally:

    python -m pip install -r requirements-smoke.txt
    python test_smoke.py

`requirements-smoke.txt` is the **only** place a new third-party package for
the smoke test gets entered. The contract
`_test_w31_rauchtest_laeuft_in_der_ci` compares the module level of `bot.py`,
`nc/` and `brain/` against that list and reports every missing package with
file and name — instead of letting the CI job die on a bare `ImportError`. It
reports dead entries too: a list that quietly grows makes the job expensive
again.

The static contracts in `test_restream.py` anchor themselves to the **literal
source text** of `bot.py`. If a signature changes, the contract breaks even
though the code is right — it has happened three times (`stop(self, rid)` became
`stop(self, rid, _keep_desired=False)`). The same goes for windows of the form
`src[i:i + 3000]`: if the function grows past them, the test reports something
as missing that sits two lines further down. **Before fixing the code, check
whether the contract or only its anchor is broken.**

For JS in `templates/*.html`, additionally extract the script blocks and run
`node --check` (check JSON-LD as JSON, not as JS).

Always in addition: no duplicate top-level defs (`ast.parse` → `module.body`),
no duplicate Flask routes **including `methods=`** (the same path with GET and
POST is not a duplicate — a naive regex raises a false alarm).

## Pitfalls that have already bitten

**Silent `except` blocks are the main enemy.** The bot catches broadly and logs
at `warning`/`debug`. A `log.warning` **never** shows up in an ERROR log — that
is how the death of the Discord gateway stayed invisible for months. When
something “stopped working”, look for the `except` eating the reason first.

For periodic loops there is **`_loop_fehler(name, exc)`**: the first report goes
out immediately at `error` level with a traceback, after that at most one every
15 minutes — carrying the number of suppressed cases. Every long-running
watchdog belongs there, never on `log.debug` and never on `pass`. The only paths
that may legitimately stay silent are cleanup paths whose failure is meaningless
(`proc.terminate()` on a dead process, `os.remove()` on an already-deleted file)
and the error channel itself — logging there creates recursion.

**Module constants freeze the `.env`.** The `.env` is partly loaded only after
the first imports. Read configuration through a function (`_backend_conf()`),
never as a module constant.

**A one-shot `await` without a supervisor.** Every long-running client needs
reconnect with backoff **and** an abort criterion for deterministic errors.

**Guards as an object attribute.** `getattr(client, "_started", False)` breaks as
soon as the object is recreated → parallel endless loops. Guard module-globally.

**Contract breaks against `brain/`.** When changing
`router.route(topic, payload)`, check every call site:
`grep -n 'router.route('`. A key drift (`prompt` vs. `question`) once failed
only on the Telegram path, because the Flask route used the right key.

## Money — do not mix it up

`REVENUE_PLATFORMS = ("kick","twitch","youtube","manuell")`. **TikTok never
belongs there**: TikTok gifts go to the tracked streamer, not to our own
channels. They are stored as `kind="gift"`, never as `donation`, and never enter
a monetary total.

`/api/donations/summary` is live telemetry built from **estimates**.
`nc/ledger.py` holds booked **payouts** for the tax office. Never derive one
from the other — displayed value ≠ payout ≠ time of receipt. Ledger entries are
append-only with a hash chain; a correction is a counter-entry.

## Security

The `.env` has around 503 variables and contains cookies, OAuth tokens and
stream keys — it is never in the archive and is never printed. When logging
`streamlink`/`ffmpeg` commands, cookie headers are redacted (F4); that redaction
path must not be bypassed when the command line changes. The dashboard binds to
`127.0.0.1:8050` by default; access runs through an SSH tunnel, not by opening
the port.

## Language and tone

Code comments and all source strings are written in German. Comments explain
**why**, not what — preferably with the concrete failure the line prevents.
Replies to the operator: short, decisive, without hedging.

**User-facing text is multilingual since v4.1-W6.** The German string is the
key; `locales/en.json` holds the English. A missing entry falls back to German
rather than to a bare key name. After changing user-facing text, run
`tools/i18n_extract.py --check en` — it reports missing *and* orphaned entries.
Log lines stay German on purpose: they are for the operator and never pass
through the translation layer.

## Way of working

Deliver in waves, each wave validated and closed. After every wave report the
state and wait for “weiter”. Deployment goes straight against production with
log and screenshot observation afterwards — changes therefore have to be
individually verifiable and roll-back-able.

## Skills

| Skill | What for |
|---|---|
| `nc-navigation` | **First.** Find something without searching the monolith |
| `nightcrawler` | Changes to `bot.py`, `nc/`, `brain/` — anchor patching, validation |
| `html-templates` | `templates/*.html`, `website/*.html` — the Messing/Blaupause themes, verification chain |
| `nc-betrieb` | Deployment, systemd, reading logs, rollback, CrowdSec, Kick outages |
| `nc-datenbank` | SQL and schema under SQLite **and** MariaDB |
| `nc-ki-backends` | `nc/freeai`, `brain/llm`, AZRAEL, the tier model, budget |
