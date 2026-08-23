# SETUP_LLAMACPP.md — M6: llama-server auf ns3068954 (Ollama-Ablösung)

## 1. Binary holen (statisch, kein Build nötig)

```bash
mkdir -p /opt/llamacpp && cd /opt/llamacpp
# Aktuelles Release, Linux x64 (AVX2 — OVH-Xeon/EPYC kann das):
curl -sL https://github.com/ggml-org/llama.cpp/releases/latest/download/llama-b*-bin-ubuntu-x64.zip -o llama.zip \
  || echo "Release-Asset-Namen auf github.com/ggml-org/llama.cpp/releases prüfen"
unzip llama.zip && chmod +x build/bin/llama-server
```

## 2. Modell (GGUF, INT4) — Empfehlung für 8 Cores / kein GPU

| Modell | Größe Q4_K_M | RAM | Eignung |
|---|---|---|---|
| Qwen2.5-0.5B-Instruct | ~0.4 GB | <1 GB | schnellste Antworten, reicht für explain/ask |
| Qwen2.5-1.5B-Instruct | ~1.0 GB | ~2 GB | deutlich besseres Deutsch, empfohlen |
| Llama-3.2-1B-Instruct | ~0.8 GB | ~1.5 GB | Alternative |

```bash
cd /opt/llamacpp
curl -sL -o model.gguf \
  "https://huggingface.co/Qwen/Qwen2.5-1.5B-Instruct-GGUF/resolve/main/qwen2.5-1.5b-instruct-q4_k_m.gguf"
```

## 3. systemd-Unit

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
# -t 4: NUR 4 der 8 Cores — ffmpeg-Recordings haben Vorrang.
# -c 8192: V37-LLMBUDGET auf 8192 erhöht (war 4096). 4096 war zu klein, sobald
#   Chat-Historie + Frage + eine 1024-Token-Antwort zusammenkamen — der Server
#   schnitt dann ab oder lehnte ab. 8192 gibt Luft. RAM-Kosten: der KV-Cache
#   wächst ~linear mit dem Kontext, also grob doppelt so viel wie bei 4096.
#   WICHTIGE ABWÄGUNG (kein GPU, 8 Cores, ffmpeg hat Vorrang):
#     - Reicht der RAM knapp? Dann bei -c 6144 bleiben.
#     - Recordings stottern während KI-Last? Dann NICHT auf -t 6 erhöhen —
#       die 4-Core-Grenze schützt die Aufnahmen bewusst.
#     - Antworten immer noch zu kurz? BRAIN_LLM_MAX_TOKENS in der .env heben,
#       aber gemeinsam mit -c (Kontext muss Prompt + Antwort fassen).
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

## 4. NIGHTCRAWLER umstellen (.env)

```bash
BRAIN_LLM_BACKEND=auto          # llamacpp zuerst, Ollama-Fallback
BRAIN_LLAMACPP_URL=http://127.0.0.1:8080
BRAIN_LLM_MAX_CALLS_H=30        # hartes Stundenbudget Tier 4
BRAIN_LLM_TIMEOUT_S=60
```

Test: `curl -s -X POST localhost:PORT/api/brain/llm/ask -H 'Content-Type: application/json' -d '{"prompt":"Status?"}'`
→ `"backend": "llamacpp"` in der Antwort.

## 5. Ollama abschalten (wenn stabil)

```bash
BRAIN_LLM_BACKEND=llamacpp      # Fallback-Kette deaktivieren
systemctl disable --now ollama  # Go-Daemon + Registry weg, ~0.5-1 GB RAM frei
```

Der bestehende Ollama-Pfad in bot_v36 (`ai_chat`) bleibt funktional —
die Umstellung von ai_chat auf die Brain-Runtime kommt im finalen
bot.py als env-Schalter `AI_PROVIDER=brain` (Default: unverändert).
