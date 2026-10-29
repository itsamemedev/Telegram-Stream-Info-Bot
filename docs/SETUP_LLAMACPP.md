# SETUP_LLAMACPP.md — M6: llama-server auf ns3068954 (lokales LLM, bevorzugt)

> 🌐 **Deutsch** · [English](en/SETUP_LLAMACPP.md)

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

## 4. Was der Bot vom Server erwartet

| Erwartung | Warum |
|---|---|
| `--host 127.0.0.1 --port 8080` (oder `BRAIN_LLAMACPP_URL` passend setzen) | nur lokal erreichbar — der Server hat keine Anmeldung |
| `GET /health` antwortet 200 | daran entscheidet der Bot „lokal oder Cloud" (15-s-Cache, 3 s Timeout) |
| `POST /v1/chat/completions` (OpenAI-kompatibel) | der eigentliche Chat; jeder andere OpenAI-kompatible Server geht genauso |
| `GET /v1/models` | Modellliste im Deck und im Selbsttest |
| `-t 4`, `Nice=10`, `CPUWeight=50` | Sendebild und Aufnahmen haben Vorrang. Seit v4.2-W108 zählt die Restream-Drossel die Load beim Start mit — ein lokales LLM unter Volllast senkt dort die Startstufe, statt Pixelsalat zu erzeugen |

Der Dienst darf `llamacpp.service` oder `llama-server.service` heißen — der Bot
spricht nur HTTP mit ihm.

**Nicht mit `--embeddings` starten.** Laut llama.cpp-Server-Doku beschränkt der
Schalter den Server auf Embeddings — `/health` ist dann grün, der Chat antwortet
mit einem Fehler, und jede Anfrage ginge in die Cloud. Die mitgelieferte
`llama-server.service` hatte ihn bis v4.2-W110. Embeddings für das Brain kommen
von einem eigenen Server (`BRAIN_EMBED_URL`, Vorgabe Port 8089). Prüfen:

```bash
curl -s localhost:8080/v1/chat/completions -H 'Content-Type: application/json' \
  -d '{"messages":[{"role":"user","content":"Sag nur: ok"}],"max_tokens":8}'
```

Antwortet das mit einem Fehler statt mit `choices`, steht seit W110 im Log
`LLM-Backend llamacpp scheitert: …`.

## 5. NIGHTCRAWLER (.env) — seit v4.2-W110 ist nichts mehr nötig

Ab v4.2-W110 wird das lokale llama.cpp **von selbst bevorzugt**, sobald
`/health` antwortet. Vorher fragte der Bot es nur bei `AI_PROVIDER=brain`,
ohne die Zeile ging jede Anfrage in die Cloud.

```bash
# alles Vorgaben — nur setzen, wer abweichen will
AI_PROVIDER=auto                # auto = lokal wenn erreichbar | lokal = immer zuerst | cloud = nie lokal
REACTION_AI_PROVIDER=auto       # dieselbe Regel fuer AZRAELs Live-Reaktionen
BRAIN_LLM_BACKEND=auto          # in brain/: llama.cpp zuerst, keyless Cloud als Reserve
BRAIN_LLAMACPP_URL=http://127.0.0.1:8080
BRAIN_LLM_MAX_CALLS_H=30        # hartes Stundenbudget (danach Cloud)
BRAIN_LLM_TIMEOUT_S=300         # CPU-Inferenz braucht Zeit
```

Reihenfolge jeder Anfrage: **Claude** (nur wenn ein Anthropic-Key gesetzt ist)
→ **lokales llama.cpp** → **keyless Cloud** (`nc/freeai`). Budget erschöpft
oder Inferenz-Slot belegt (Concurrency 1) heißt: diese eine Anfrage geht in die
Cloud, die nächste versucht wieder lokal.

**Bilder (Vision) gehen weiter in die Cloud.** llama-server kann das nur mit
einem multimodalen Modell plus `--mmproj`, und der Chat-Pfad reicht Bilder
nicht im OpenAI-Format durch.

Prüfen:

```bash
curl -s localhost:8080/health
curl -s localhost:8080/v1/models
python3 bot.py --selfcheck      # Zeile „Lokales LLM: llama-server antwortet (…) — bevorzugt"
```

Im Brain-Panel steht in der Pille `LLAMA.CPP` (lokal) bzw. `CLOUD (RESERVE)`.

## 6. Ollama ist entfernt

Seit V37 spricht der Bot kein Ollama mehr, seit v4.2-W110 nennt er es auch
nirgends mehr als Ratschlag. Läuft der Dienst noch:

```bash
systemctl disable --now ollama   # ~0.5–1 GB RAM frei
```

`OLLAMA_URL`, `OLLAMA_MODEL` und Verwandte liest der Bot nicht mehr; sie
können aus der `.env`.
