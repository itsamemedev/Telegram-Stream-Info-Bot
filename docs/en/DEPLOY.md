# NIGHTCRAWLER v37 — Build B120

> 🌐 **English** · [Deutsch](../DEPLOY.md)

This archive is the **complete project state**, laid out identically to the
original. Unpack it, put it over the existing directory, restart.

## 1. Back up (do not skip)

    cd ~/tiktok-bot
    tar czf ../nightcrawler_backup_$(date +%F_%H%M).tgz .

## 2. Install

    sudo systemctl stop tiktok-bot
    unzip -o NIGHTCRAWLER_v37_B120.zip -d ~/tiktok-bot
    sudo systemctl start tiktok-bot

`.env`, `tiktok_cookies.txt`, `recordings/` and the database are NOT in the
archive and stay untouched. `.env.example` is only the template.

## 3. What is newly added

    nc/ledger.py              revenue journal (tax office)
    nc/ytoauth.py             YouTube OAuth flow (counterpart to nc/twitchoauth.py)
    tools/ncpatch.py          patch and validation tool
    skills/nightcrawler/      working brief for future sessions
    DEPLOY.md                 this file

Changed: bot.py, brain_bridge.py, nc/freeai.py, nc/logfilters.py, brain/llm.py.
Everything else is unchanged from the original.

## 4. Watch the start

    journalctl -u tiktok-bot -f | grep -Ei 'discord|brain|freeai|Normalisierung'

Expected:
  Discord verbunden als <bot> — 60 Slash-Commands aktiv.
  Brain-LLM: llama.cpp OK   OR   KEIN Backend erreichbar
  possibly Startup-Cleanup: N Usernames normalisiert

(Log output is German — it is written for the operator. `UI_LANG` only changes
the user-facing language of the bot and dashboard.)

If Discord stays silent, the reason is now an ERROR with a traceback in the log —
previously it was a WARNING and therefore invisible in an error log.

## 5. Verification steps

**AI backends**

    cd ~/tiktok-bot && python3 -c "import nc.freeai as f; print(f.diagnose())"

Shows per base: free/blocked, latency, keyless/KEY, last error. If every
Pollinations base reports "auth", you need a key from enter.pollinations.ai →
`POLLINATIONS_API_KEY` in the `.env`. Optionally `LLM7_TOKEN` from token.llm7.io
(raises 30 to 120 requests/min).

**Commands**

    Telegram:  /brain          status line with the active backend
               /brain teste    a real answer instead of "no answer"
               /ai hallo
               /einnahmen
    Discord:   /status  /ai  /tracklist

**YouTube**

    curl -s localhost:8050/api/channels/status | jq .youtube

`"source":"api"` = Data API active, exact viewers + subscribers.
`"source":"scrape"` = not connected, the keyless fallback is running.

Connecting now works in the dashboard: the **“Connect YouTube”** panel sits
directly below the Twitch panel. It only needs YOUTUBE_CLIENT_ID +
YOUTUBE_CLIENT_SECRET in the `.env`; the flow fetches the refresh token itself
(SETUP_YT_OAUTH.md). As with Twitch, tunnel once with
`ssh -L 3000:localhost:8050 ...` and open the page through
http://localhost:3000 — Google does not allow bare IPs.

**Discord state**

    curl -s localhost:8050/api/discord/overview | jq .session

Contains attempts, reconnects, the last reason and its timestamp.

**Tax office**

    /einnahmen buchen 2026-02-15 twitch 412.50 0 TW-2026-01
    /einnahmen 2026
    curl -s "localhost:8050/api/finanzamt/entries?year=2026" | jq .summary
    Browser: localhost:8050/api/finanzamt/export.csv?year=2026

The date is the day the money was **credited to the account**, not the day of
the stream. Bookings are append-only; a correction is a counter-entry
(`kind=correction` + `storno_of`), not an overwrite.

## 6. Restream supervision (B123)

Two separate problems, two mechanisms.

**a) Resuming after a restart or crash**
New columns `restreams.desired` + `desired_since`: the intended state. `start()`
sets it, only an explicit `stop()` clears it — a crash does not touch it. On
startup `_restream_resume_after_restart` picks up everything that should be
running. Previously this hung on `auto_restream=1` alone; restreams started by
hand were gone after a restart.

**b) “online” only meant “the process exists”**
With multistreaming, Twitch and YouTube carry `onfail=ignore` in the tee muxer
(so that a stuck Twitch does not drag Kick down). That is exactly why ffmpeg
keeps running when they drop out — the panel showed three green targets while
nothing arrived on two platforms.

`_restream_verify_loop` now polls the PLATFORMS themselves every
RESTREAM_VERIFY_S (Kick keyless, Twitch Helix, YouTube Data API) and rebuilds
the restream when a target is demonstrably dead. With tee you cannot reconnect a
single target, hence the whole process.

Four rules against restart loops (in nc/restream_guard.py, tested in isolation):
  1. 90s startup grace — RTMP can take up to a minute before the platform
     reports live. YouTube is the slowest.
  2. Hysteresis: three consecutive negatives, not one.
  3. UNKNOWN != OFFLINE. An API timeout or quota error is NO proof of a dead
     stream and does not count.
  4. Backoff 60s, doubling up to 15 min.
  In addition: if the SOURCE is offline, empty targets are the normal case.

Check it:

    curl -s localhost:8050/api/restream/verify | jq

Shows per target the last platform response, consecutive negatives and whether
the target has ever been confirmed since the start. `targets_dead` is the answer
to “is it really running?” — `live` stays the pure process state.

Switch it off: RESTREAM_VERIFY=0.

## 7. Performance (B122)

Measured against a realistically filled tiktok_checks table:

| tiktok_checks | get_stats() total |
|---|---|
| 50,000 rows | 10 ms |
| 250,000 | 54 ms |
| 1,000,000 | 241 ms |
| 3,000,000 | 635 ms |

These three full scans hung off api_stats() on the dashboard's 5-second pulse —
17,280 calls per day per open tab. The header shows none of it; it only reads
live_now and active_trackings.

    /api/pulse   1164 ms  ->  0.2 ms
    CPU/day       335 min ->  0.1 min

Three changes:
  * /api/pulse calls api_stats(lean=True) — only the three cheap, indexed
    counters on small tables.
  * get_stats() gets a TTL cache (STATS_CACHE_TTL, default 120s) for the
    statistics view.
  * tiktok_checks was the only log table WITHOUT any cleanup. Now capped by
    CHECKS_RETENTION_DAYS (30) and the hard ceiling CHECKS_MAX_ROWS (200,000),
    plus an index on created_at.
    Effect: 403 MB -> 27 MB, statistics view 1164 ms -> 42 ms.

On the FIRST start after the update, retention does one large cleanup. Compact
once afterwards so the disk space actually comes back:

    sqlite3 <your>.db "VACUUM;"

You can switch it off through the .env (CHECKS_RETENTION_DAYS=0,
CHECKS_MAX_ROWS=0).

## 7b. What was NOT changed, and why

Connection pooling for SQLite was evaluated and rejected: `db_conn()` does open
a new connection on every call, but the measured overhead is 0.095 ms and a warm
page cache would only bring 14 %. Against the risk of thread-shared SQLite
connections in a process with recording, restream and Flask threads, that is a
bad trade.

The ffmpeg paths (x264 presets, thread ceiling, Whisper throttle) were already
bounded in earlier builds and were not touched.

## 8. Deep search B124 — bugs found and fixed

**1. Shutdown deleted the intended state (severe, introduced in B123)**
`_shutdown` calls `stop_all()`, and every `stop()` set `desired=0`. After an
orderly `systemctl restart`, NO restream came back — the B123 function would
only have worked after a hard crash.
Fix: `stop_all(_keep_desired=True)` on the shutdown path.

**2. Source failover disabled restreams permanently (severe, B123)**
`_switch_to_next_live()` stopped without `_keep_desired`. Every time a TikTok
source went offline, the restream was permanently disabled.
Fix: the intended state stays; if it really switches to another target, it moves
along with it.

**3. The verify loop ignored RESTREAM_SINGLE (severe, B123)**
With several desired=1 targets it would have started each one. In single mode
there is exactly ONE Kick ingest, though — two ffmpeg encoders on the same
stream key, and the platform disconnects both. The watchdog would have created
the outage itself. Fix: slot lock.

**4. Five Discord loops without a task reference (severe, legacy)**
`client.loop.create_task(...)` without a reference. asyncio only holds a WEAK
reference — a task sitting in `await asyncio.sleep()` can be collected by the
GC. That is exactly what all five do (live board, weekly digest, clip of the
week, error feed, event countdown). If one disappears there is NO exception and
NO log line.
Fix: through `_spawn()` — it holds the reference and logs crashes.

**5. 32 unguarded DOM accesses to non-existent elements (legacy)**
8 JS functions (loadSurveil, loadCaptures, loadVault, aiShowEmpty, aiOpenConv,
loadEvolution, renderTargetGrid, renderCaptures) write to IDs that are in NO
template — leftovers of removed views. The dashboard has only 5 views left.
Every call threw “Cannot set properties of null” and aborted the function.
Fix: guards with an early `return` at the start of the function.

**6. Misleading dead code (cosmetic)**
`if False:` / `and False` in the Discord clip upload read like a bug. The real
compression runs further down, per guild. Branch removed.

CHECKED AND CLEAN: SQL injection (all f-string queries whitelisted), arity and
keywords across 69 cross-module calls, missing `await`, mutable default
arguments, dict mutation during iteration, name use before definition at module
level, 135 onclick targets, 116 API calls against 280 routes.

## 8b. Addendum B124 — analysis of the production log of 24 July

The log shrank from 4047 to 23 lines. Tooling noise, “channel is not currently
live” and the Telegram errors are gone. What remained was ONE event
(@tatjana335), logged twice. Two fixes came out of it:

**7. ffmpeg hammered a 404 for 60 seconds**
`-reconnect_on_http_error 4xx,5xx` included 404 and 403. Both are TERMINAL with
TikTok: the CDN pull URL carries an `expire=<ts>` — after expiry or an edge
switch it no longer exists, and requesting the same URL again can by definition
never succeed. Observed: five reconnects over 60s, then an abort without a
single second of material. The only rescue would have been to RESOLVE the stream
URL AGAIN — and that is exactly what the bot does on the next attempt, as soon
as ffmpeg gives up quickly.
The code's own diagnostic recommendation had said so all along (“on a 404 stop
quickly instead of hammering”), only the ffmpeg arguments did not follow it.
Now: only the genuinely transient codes 408, 429, 500, 502, 503, 504.

Verified against real ffmpeg 6.1.1: the code list is accepted.
`-reconnect_delay_total_max` was deliberately NOT added — the same probe
reported “Unrecognized option”, which would have broken EVERY recording.

**8. The same stderr was logged twice at full length**
handle_recording_finished and log_recording_failure both emitted the complete
block — twice ~800 characters for ONE event, half of the remaining log volume.
Now: a diagnostic line with a capped tail (600 characters) and a short form next
to it (400). In full, the stderr still sits in recording_attempts.stderr_tail.

In addition: 404/stream_dead now runs as WARNING instead of ERROR. The loss
stays visible, but a rotating CDN edge is not a bot defect and does not belong
in the error log.

## 8c. B125 — data destroyer in clean_username fixed

**9. “@www.tiktok.comrabi1978” is a REAL handle, not URL junk**

22 characters, only letters, digits and dots — TikTok allows dots in a handle,
so it is perfectly valid. The name is obviously chosen exactly that way to
outwit automatic URL detection. It succeeded:

  * `clean_username()` cut away everything before ANY occurrence of
    "tiktok.com" → the real handle became "rabi1978".
  * The startup migration added in B120 would have written that into the
    database and, if "rabi1978" is tracked as well, DELETED THE ORIGINAL AS A
    DUPLICATE.

Fixed:
  * `clean_username()` only interprets when it is ALLOWED to: a scheme or a "/"
    present → URL. Otherwise an "@" present → drop everything up to the last
    "@" (leading @ / swallowed slash). Otherwise LITERAL. A handle by definition
    contains neither "/" nor "@" — so "www.tiktok.comrabi1978" cannot be a URL
    at all and stays untouched. 12 cases tested, including "tiktok.company" and
    "www.tiktok.com.official".
  * The migration is replaced by a pure REPORT. It only reports what a handle
    can NEVER be (/ : ? space or @ inside the name). NOTHING is changed or
    deleted.
  * NEW `/track_exact <name>` — takes the name literally, entirely without URL
    detection, with a validity check against TikTok's rules.
  * `/track` now says WHEN it read the input as a URL and points at
    /track_exact. Previously you noticed the reinterpretation only when the
    capture failed to appear.
  * NEW `nc.textutil.is_valid_tiktok_username()` — 2-24 characters, only
    a-z A-Z 0-9 _ . , no dot at the end.

If the old migration has already run, check:

    sqlite3 <your>.db "SELECT id, username FROM trackings ORDER BY id;"

If the handle is missing, add it again:  /track_exact www.tiktok.comrabi1978

## 8d. B127 — performance, second round

**Point 1 (Chromium overlay) does not apply**: it already runs as
RESTREAM_OVERLAY_MODE=text on your box. The expensive html path is never
entered.

**10. Four more log tables without cleanup**
B122 only capped tiktok_checks. Also growing without bound were event_log,
ai_log, profile_snapshots and overlay_events.

Notably: AI_LOG_RETENTION_DAYS=30 was defined and documented but applied
NOWHERE — there was not a single DELETE FROM ai_log. A setting that suggested
cleanup and did nothing.

Treated per table, not uniformly:
  * event_log        -> delete older than 60 days
  * ai_log           -> delete older than AI_LOG_RETENTION_DAYS (now effective)
  * profile_snapshots-> THIN OUT instead of deleting: beyond 30 days, keep the
                        most recent snapshot per user and calendar day.
                        Measured against 2880 test rows: -65 %, curve shape
                        preserved (exactly 1 value per day), the last 30 days
                        untouched.
  * overlay_events   -> older than 180 days, BUT NEVER kind='donation'. Those
                        rows feed the donation goal and the cross-check of the
                        tax evaluation. In the test: 300 of 300 donations
                        untouched.

**11. Measurement instead of blind tuning for Whisper, polling and transcoding**
The numbers were missing for these three — on your machine, not in my sandbox.
Instead of guessing defaults, they are now measured:

  * Whisper: real-time factor (RTF = compute time / audio length) per run,
    moving average. RTF > 1 means transcription is slower than the audio plays
    → a backlog builds up. A warning after 5, 25 and 100 such runs with a
    concrete hint (WHISPER_MODEL=tiny).
  * Polling: the duration of each live check against ITS interval. If more than
    20 % of the checks exceed their interval (from 50 measurements on), there is
    a one-off warning. The reason: the comment on _INFLIGHT_GUARD_SECS allows a
    worst case of ~90s while the live interval is set to 20s.
  * Restream: transcode state per target plus speed/slow_ticks made visible.

All together:

    curl -s localhost:8050/api/system/check_timing | jq

Every block has a field "urteil" (verdict) — "unauffaellig" (nothing
conspicuous), "noch zu wenige Messungen" (not enough measurements yet) or a
concrete hint. Only when something other than "unauffaellig" stands there for
days is it worth turning the knobs.

## 8e. B128 — website and dashboard

### Website (website/lafap_index.html)

**12. Seven placeholder links were live**
DEIN-INVITE and DEIN-KANAL pointed nowhere. Now the real channels from your
.env (Kick, YouTube, Twitch, Discord).

**13. Google Fonts was loaded externally**
That transmits every visitor's IP to Google without consent — for a German site
with an imprint and a privacy notice, an avoidable risk (Munich Regional Court
I, 20 January 2022, 3 O 17493/20). Now a local @font-face embedding with
preload. External requests: 9 -> 7, and the remaining 7 are exclusively your own
social links. You have to place the font files once — instructions in
website/FONTS.md. Until then font-display:swap applies, the page stays usable,
it just looks less like a terminal.

**14. No `<h1>`** (4× h2, 0× h1). The acronym block is the main heading in
substance and is now marked up as one; role="img" stays so that the letter
graphic is read out as a unit.

**15. No `<main>` landmark** — added.

**16. No og:image** — when shared in Discord/WhatsApp/Telegram a grey card
appeared. og:image + twitter:card (1200x630) added; you still have to create the
file og-card.png (see FONTS.md).

### Dashboard (templates/dashboard.html)

**17. 27 icon buttons without a label** — a screen reader only read “button”,
voice control did not work. Now aria-label AND title (the latter also helps
sighted users as a tooltip). aria attributes in total: 37 -> 64.

**18. Touch targets under 44px** — Apple and Google both name 44px as the
minimum. Bound to @media(pointer:coarse) instead of a screen width: desktop
density stays, a touch laptop benefits anyway. On a dashboard that is operated
from a phone, a mis-tap can mean: stopped the wrong restream.

**19. No skip link, no visible focus ring, no main landmark**
Skip link “Zum Hauptinhalt springen” (visible only on keyboard focus),
:focus-visible outline and `<main id="hauptinhalt">` added.

**20. The only `<img>` without alt** — alt="" set (the avatar is decorative, the
name sits next to it; an empty alt lets screen readers skip it).

## 9. Rollback

    sudo systemctl stop tiktok-bot
    cd ~/tiktok-bot && tar xzf ../nightcrawler_backup_<stamp>.tgz
    sudo systemctl start tiktok-bot

## 10. What is in this build

| Area | Cause | Fixed |
|---|---|---|
| Discord dead | `client.start()` without a supervisor, exception swallowed as WARNING | reconnect 5s->300s, abort after 5 failed starts, config errors named clearly |
| Discord loops | guard hung off the client object | module-global guard |
| `/brain` | payload key `question` vs. handler `prompt` | both accepted, router trace instead of "no answer" |
| `/brain` | chain only `['llamacpp']` | `['llamacpp','freeai']`, cloud reserve |
| `/ai` | one global model for all bases -> rotation dead | model per base, 4 bases, key+referrer, 402 as `auth` |
| Log spam | offline channel as ERROR, client aborts as ERROR | both DEBUG, stdout capped |
| Phantom users | old rows from before the B76c fix | startup normalisation |
| Donations | TikTok hidden in only one view | `REVENUE_PLATFORMS` gate, TikTok runs as `gift` |
| YouTube | scraping, rounded subscribers | Data API v3, exact values, 60s quota cache |
| Connecting YouTube | missing — refresh token only by hand through the .env | dashboard panel like Twitch, one-click flow, self-renewing |
| Tax office | missing | `nc/ledger.py`, append-only, hash chain, CSV |
| Restream after restart | only auto_restream=1, otherwise gone | persisted intended state, resume on startup |
| Restream "online" despite offline | status() only reported "the process lives" | platform check every 120s + rebuild |
| CPU load | 3 full scans over an unbounded table every 5s | lean pulse + TTL cache + retention: 1164 ms -> 0.2 ms |

## 11. Limits

My test environment only reaches a domain allowlist — Pollinations, llm7.io, OVH
and the YouTube API were not reachable. The logic, the error classification and
the rotation paths are verified; the actual reachability of the services is not.
That is why step 5 comes first.

The revenue journal is structured groundwork for your tax adviser, not tax
advice. Check the figures against bank statements and platform settlements.
