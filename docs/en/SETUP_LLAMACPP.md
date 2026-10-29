# SETUP_LLAMACPP.md — M6: llama-server on ns3068954 (replacing Ollama)

> 🌐 **English** · [Deutsch](../SETUP_LLAMACPP.md)

## 1. Get the binary (static, no build needed)

```bash
mkdir -p /opt/llamacpp && cd /opt/llamacpp
# Current release, Linux x64 (AVX2 — the OVH Xeon/EPYC can do that):
curl -sL https://github.com/ggml-org/llama.cpp/releases/latest/download/llama-b*-bin-ubuntu-x64.zip -o llama.zip \
  || echo "check the release asset names on github.com/ggml-org/llama.cpp/releases"
unzip llama.zip && chmod +x build/bin/llama-server
```

## 2. Model (GGUF, INT4) — recommendation for 8 cores / no GPU

| Model | Size Q4_K_M | RAM | Suitability |
|---|---|---|---|
| Qwen2.5-0.5B-Instruct | ~0.4 GB | <1 GB | fastest answers, enough for explain/ask |
| Qwen2.5-1.5B-Instruct | ~1.0 GB | ~2 GB | noticeably better German, recommended |
| Llama-3.2-1B-Instruct | ~0.8 GB | ~1.5 GB | alternative |

```bash
cd /opt/llamacpp
curl -sL -o model.gguf \
  "https://huggingface.co/Qwen/Qwen2.5-1.5B-Instruct-GGUF/resolve/main/qwen2.5-1.5b-instruct-q4_k_m.gguf"
```

## 3. systemd unit

```ini
# /etc/systemd/system/llamacpp.service
[Unit]
Description=llama.cpp Server (NIGHTCRAWLER Brain Tier 4)
After=network.target

[Service]
ExecStart=/opt/llamacpp/build/bin/llama-server \
  -m /opt/llamacpp/model.gguf \
  --host 127.0.0.1 --port 8080 \
  -t 4 -c 8192 --no-warmup
# -t 4: ONLY 4 of the 8 cores — ffmpeg recordings take precedence.
# -c 8192: V37-LLMBUDGET raised to 8192 (was 4096). 4096 was too small as soon
#   as chat history + question + a 1024-token answer came together — the server
#   then truncated or refused. 8192 gives room. RAM cost: the KV cache grows
#   roughly linearly with the context, so about twice as much as at 4096.
#   IMPORTANT TRADE-OFF (no GPU, 8 cores, ffmpeg has priority):
#     - RAM barely sufficient? Then stay at -c 6144.
#     - Recordings stutter under AI load? Then do NOT raise -t to 6 —
#       the 4-core limit protects the recordings on purpose.
#     - Answers still too short? Raise BRAIN_LLM_MAX_TOKENS in the .env,
#       but together with -c (the context has to hold prompt + answer).
Restart=always
RestartSec=5
Nice=10
CPUWeight=50

[Install]
WantedBy=multi-user.target
```

```bash
systemctl daemon-reload && systemctl enable --now llamacpp
curl -s localhost:8080/health
```

## 4. What the bot expects from the server

| Expectation | Why |
|---|---|
| `--host 127.0.0.1 --port 8080` (or set `BRAIN_LLAMACPP_URL`) | local only — the server has no authentication |
| `GET /health` returns 200 | this decides "local or cloud" (15 s cache, 3 s timeout) |
| `POST /v1/chat/completions` (OpenAI-compatible) | the actual chat |
| `GET /v1/models` | model list in the dashboard and the self-check |
| `-t 4`, `Nice=10`, `CPUWeight=50` | broadcast and recordings come first |

**Do not start it with `--embeddings`.** According to the llama.cpp server docs
that switch restricts the server to embeddings — `/health` stays green, chat
fails, and every request would go to the cloud. The bundled
`llama-server.service` had it until v4.2-W110. Brain embeddings come from a
separate server (`BRAIN_EMBED_URL`, default port 8089).

## 5. NIGHTCRAWLER (.env) — nothing needed since v4.2-W110

Since v4.2-W110 the local llama.cpp is **preferred automatically** as soon as
`/health` answers. Before, the bot only asked it with `AI_PROVIDER=brain`.

```bash
# all defaults — only set what you want to change
AI_PROVIDER=auto                # auto = local if reachable | lokal = always first | cloud = never local
REACTION_AI_PROVIDER=auto       # same rule for AZRAEL's live reactions
BRAIN_LLM_BACKEND=auto          # in brain/: llama.cpp first, keyless cloud as reserve
BRAIN_LLAMACPP_URL=http://127.0.0.1:8080
BRAIN_LLM_MAX_CALLS_H=30
BRAIN_LLM_TIMEOUT_S=300
```

Order of every request: **Claude** (only with an Anthropic key) → **local
llama.cpp** → **keyless cloud**. Images (vision) still go to the cloud.

## 6. Ollama is gone

```bash
systemctl disable --now ollama
```

`OLLAMA_URL`, `OLLAMA_MODEL` and friends are no longer read.
