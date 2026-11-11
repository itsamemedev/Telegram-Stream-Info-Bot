# SETUP_LLAMACPP.md — local LLM: ik_llama.cpp with Qwen3-14B-Uncensored

> 🌐 **English** · [Deutsch](../SETUP_LLAMACPP.md)

Since v5.1-W181 the brain's local LLM (tier 4) runs on
**[ik_llama.cpp](https://github.com/ikawrakow/ik_llama.cpp)** — a llama.cpp
fork with faster CPU kernels — and the model **Qwen3-14B-Uncensored** (GGUF,
Q4_K_M, about 9 GB). The file name `SETUP_LLAMACPP.md` stays because the
self-check, the installer and older notes refer to it.

## 1. Setup — one command

```bash
sudo bash tools/ikllama.sh            # guided
bash tools/ikllama.sh --dry-run       # show what would run
bash tools/ikllama.sh --check         # check only (exit 1 if something is missing)
```

The installer (question "local LLM") and `bash tools/update.sh --ik-llama`
call the same tool. In this order it:

1. **Pre-checks** memory, disk, build tools and the model details on Hugging
   Face. If anything fails here, **nothing** has changed; an existing llama.cpp
   keeps running.
2. **Removes the old llama.cpp** (operator's request: uninstall first): stops
   and disables the `llamacpp` and `llama-server` services, removes the unit
   files, `/opt/llamacpp`, `/opt/llama.cpp` and `/usr/local/bin/llama-server`.
   **Old GGUF files are kept** — they also run under ik_llama.cpp and are the
   way back if 14B is too large. Delete them with `--altes-modell-loeschen`.
   A llama-server in any other place is only reported, never deleted.
3. **Builds ik_llama.cpp** — `git clone` to `/opt/ik_llama.cpp`, then
   `cmake -DCMAKE_BUILD_TYPE=Release -DGGML_NATIVE=ON` and
   `cmake --build … --target llama-server` with `nice -n 15` and half the
   cores (10–20 minutes; the box keeps recording meanwhile).
4. **Downloads the model** to `/opt/models/`, resuming after an interruption
   (`.teil`), checking size and SHA-256 against the Hugging Face API and the
   GGUF magic. Only then the marker `….gguf.sha256` is written.
5. **Writes the service** `llama-server.service`, starts it, waits for
   `/health` (503 = model loading, a few minutes with `-rtr`) and sends one
   chat probe.

A second run on a finished setup does nothing. Rebuild:
`sudo bash tools/ikllama.sh --neu-bauen`.

## 2. Model and values

| Variable (environment or `.env`) | Default | Purpose |
|---|---|---|
| `LLM_MODELL_REPO` | `mradermacher/Qwen3-14B-Uncensored-GGUF` | Hugging Face repo (static quants of `nicoboss/Qwen3-14B-Uncensored`) |
| `LLM_MODELL_DATEI` | `Qwen3-14B-Uncensored.Q4_K_M.gguf` | about 9 GB |
| `LLM_MODELL_QUANT` | `Q4_K_M` | fallback if the file is named differently — exactly one match is taken |
| `LLM_MODELL_SHA256` | empty | empty = from Hugging Face; set = checked against this value |
| `LLM_MODELL_VERZ` | `/opt/models` | |
| `LLM_THREADS` | `4` | recordings have priority |
| `LLM_KONTEXT` | `8192` | |
| `IK_LLAMA_DIR` / `IK_LLAMA_REF` | `/opt/ik_llama.cpp` / `main` | |
| `BRAIN_LLAMACPP_URL` | `http://127.0.0.1:8080` | the port comes from here — same as before |

Smaller quantisations of the same model if memory is short: `Q3_K_M` (about
7 GB), `Q2_K` (about 6 GB) — set `LLM_MODELL_DATEI` accordingly. The old
Qwen2.5-1.5B (about 1 GB) runs as well.

## 3. The unit — what the switches do

```ini
ExecStart=/opt/ik_llama.cpp/build/bin/llama-server \
  -m /opt/models/Qwen3-14B-Uncensored.Q4_K_M.gguf -a qwen3-14b-uncensored.q4_k_m \
  --host 127.0.0.1 --port 8080 -t 4 -c 8192 -ngl 0 -rtr --jinja --no-warmup
Nice=10
CPUWeight=50
MemoryMax=13G        # model size + 4 GB, computed by the tool
```

| Switch | Why |
|---|---|
| `-t 4` | 4 of 8 cores — ffmpeg recordings and restreams have priority |
| `-c 8192` | 4096 was too small for history + question + a 1024-token answer |
| `-ngl 0` | CPU only; the ik_llama.cpp default is 999 |
| `-rtr` | repack weights to the interleaved form while loading ("may improve performance"); keeps the whole model in RAM, hence `MemoryMax` |
| `--jinja` | chat template from the model — only then `enable_thinking=false` works |
| `-a` | name `/v1/models` reports (deck, self-check) |
| no `-fa` | flash attention is on by default in ik_llama.cpp |
| no `-fmoe` | only affects MoE models; Qwen3-14B is dense |

**TRADE-OFF** (no GPU, 8 cores, ffmpeg has priority):

- 14B on the CPU is **slow** — roughly a few tokens per second. The hourly
  budget (`BRAIN_LLM_MAX_CALLS_H`) and the timeout (`BRAIN_LLM_TIMEOUT_S=300`)
  therefore stay as they are.
- Memory tight? A smaller quantisation (see above) or `-c 6144` via
  `LLM_KONTEXT`.
- Recordings stutter under AI load? Do **not** raise to `-t 6` — the 4-core
  limit protects the recordings on purpose.

**Do not start with `--embeddings`.** It restricts the server to embeddings —
`/health` would be green, chat would not. Embeddings for the brain come from a
separate server (`BRAIN_EMBED_URL`, default port 8089).

## 4. Qwen3 thinks — and the bot does not let it

Qwen3 first writes a `<think>…</think>` block, then the answer. On the CPU that
costs hundreds of tokens before the first word, and with `max_tokens` 1024
often nothing was left for the answer. So `brain/llm.py` sends (default
`BRAIN_LLM_DENKEN=0`):

- `chat_template_kwargs: {"enable_thinking": false}` — works with `--jinja`,
- `/no_think` on the last user message — Qwen3's own switch, works without the
  template too,

and strips **every** thinking block from the answer (`ohne_denkblock`). If
nothing is left (thinking cut off by `max_tokens`), that is an error for the
chain, not an empty success — the request goes to the cloud.

## 5. What the bot expects from the server

| Expectation | Why |
|---|---|
| `--host 127.0.0.1 --port 8080` (or matching `BRAIN_LLAMACPP_URL`) | local only — the server has no login |
| `GET /health` answers 200 | the bot decides "local or cloud" on it (15 s cache, 3 s timeout) |
| `POST /v1/chat/completions` (OpenAI-compatible) | the actual chat |
| `GET /v1/models` | model name in the deck and the self-check |
| `-t 4`, `Nice=10`, `CPUWeight=50` | output picture and recordings have priority |

Check:

```bash
bash tools/ikllama.sh --check
systemctl status llama-server
curl -s localhost:8080/health
python3 bot.py --selfcheck
```

## 6. NIGHTCRAWLER (.env) — nothing needed

The local LLM is **preferred automatically** as soon as `/health` answers
(since v4.2-W110). No bot restart needed. `BRAIN_LLM_DENKEN=0` (default) keeps
Qwen3's thinking mode off. Order of every request: **Claude** (only with an
Anthropic key) → **local ik_llama.cpp** → **keyless cloud** (`nc/freeai`).
**Images (vision) still go to the cloud.**

## 7. Ollama is gone

Since V37 the bot no longer speaks Ollama. If the service still runs:
`systemctl disable --now ollama`.
