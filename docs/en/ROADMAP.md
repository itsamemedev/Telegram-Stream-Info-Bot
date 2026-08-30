# Roadmap

> 🌐 **English** · [Deutsch](../ROADMAP.md)

The next big step is not a feature, it is cleaning up: **`bot.py` has 29,356
lines**. That file is the project's bottleneck — it cannot be taken in at a
glance and can only be edited with tooling.

The complete, measured plan is in
**[`MODULARISIERUNG.md`](../MODULARISIERUNG.md)** (German). Here is the short
version.

---

## The six waves

| Wave | Content | Lines |
|---|---|---:|
| **0** | Foundation — `nc/ctx.py` for the 13 genuine cross-cutting helpers | ±0 |
| **1** | Bundle up the 173 global-free functions | −2,200 |
| **2** | Blueprint pilot `/api/recordings` — proves the method | −470 |
| **3** | Blueprints in series — **the big lever** | −7,600 |
| **4** | Extract `RestreamManager` and `KickModerator` | −1,700 |
| **5** | Move the Discord layer into `discord_ext/` | −2,100 |
| **6** | Clean up the core, `bot.py` becomes the composition root | the rest |

Wave 2 is done, wave 3 is running: `nc/routes/` carries 21 blueprints with 187
API routes today that no longer sit in the monolith.

---

## Why this is feasible

Two measurements, not estimates:

1. **The coupling is shallow.** A median of 2 foreign references per route, and
   only 13 genuine cross-cutting helpers. Extracting a route rarely drags more
   than a handful of names with it.
2. **There is not a single `url_for` in the project.** Flask blueprints are
   therefore behaviour-neutral here — moving a route changes no URL and breaks
   no template.

---

## The bar

Whether the goal is reached is not decided by a line count but by this:

> **Adding a new API route without opening `bot.py`.**

---

Next: **[`MODULARISIERUNG.md`](../MODULARISIERUNG.md)** (the full plan, German) ·
**[`CHANGELOG.md`](../CHANGELOG.md)** (what already landed, German)
