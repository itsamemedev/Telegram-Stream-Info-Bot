# SETUP_LLAMACPP.md — lokales LLM: ik_llama.cpp mit Qwen3-14B-Uncensored

> 🌐 **Deutsch** · [English](en/SETUP_LLAMACPP.md)

Seit v5.1-W181 läuft das lokale LLM des Brains (Tier 4) auf
**[ik_llama.cpp](https://github.com/ikawrakow/ik_llama.cpp)** — einem Fork von
llama.cpp mit schnelleren CPU-Kernen — und dem Modell
**Qwen3-14B-Uncensored** (GGUF, Q4_K_M, rund 9 GB). Der Dateiname
`SETUP_LLAMACPP.md` bleibt, weil ihn Selbsttest, Installer und ältere Notizen
nennen.

## 1. Einrichten — ein Befehl

```bash
sudo bash tools/ikllama.sh            # gefuehrt
bash tools/ikllama.sh --dry-run       # zeigen, was liefe
bash tools/ikllama.sh --check         # nur pruefen (Exit 1, wenn etwas fehlt)
```

Dasselbe Werkzeug rufen der Installer (Frage „lokales LLM") und
`bash tools/update.sh --ik-llama`. Es tut, in dieser Reihenfolge:

1. **Vorprüfung** — Arbeitsspeicher, Platte, Bauwerkzeuge, Modellangaben bei
   Hugging Face. Fällt hier etwas, ist **nichts** verändert; ein vorhandenes
   llama.cpp läuft weiter.
2. **Altes llama.cpp entfernen** (Wunsch des Betreibers: erst deinstallieren):
   Dienste `llamacpp` und `llama-server` stoppen und abmelden, Unit-Dateien,
   `/opt/llamacpp`, `/opt/llama.cpp` und `/usr/local/bin/llama-server` weg.
   **Alte GGUF-Dateien bleiben** — sie laufen auch unter ik_llama.cpp und sind
   der Rückweg, falls 14B zu groß ist. Löschen: `--altes-modell-loeschen`.
   Ein llama-server an einem anderen Ort wird nur genannt, nicht gelöscht.
3. **ik_llama.cpp bauen** — `git clone` nach `/opt/ik_llama.cpp`, dann
   `cmake -DCMAKE_BUILD_TYPE=Release -DGGML_NATIVE=ON` und
   `cmake --build … --target llama-server` mit `nice -n 15` und halber
   Kernzahl (10–20 Minuten; die Box nimmt währenddessen auf).
4. **Modell laden** — nach `/opt/models/`, mit Wiederaufnahme nach Abbruch
   (`.teil`), Prüfung von Größe und SHA-256 gegen die Hugging-Face-API und der
   GGUF-Kennung. Erst danach entsteht der Prüfvermerk `….gguf.sha256`.
5. **Dienst** `llama-server.service` schreiben, starten und auf `/health`
   warten (503 = Modell lädt, mit `-rtr` einige Minuten), dann eine
   Chat-Probe.

Ein zweiter Lauf auf fertigem Bestand tut nichts. Neu bauen:
`sudo bash tools/ikllama.sh --neu-bauen`.

## 2. Modell und Werte

| Variable (Umgebung oder `.env`) | Vorgabe | Wofür |
|---|---|---|
| `LLM_MODELL_REPO` | `mradermacher/Qwen3-14B-Uncensored-GGUF` | Hugging-Face-Repo (statische Quants von `nicoboss/Qwen3-14B-Uncensored`) |
| `LLM_MODELL_DATEI` | `Qwen3-14B-Uncensored.Q4_K_M.gguf` | rund 9 GB |
| `LLM_MODELL_QUANT` | `Q4_K_M` | Rückfall, falls die Datei im Repo anders heißt — genau ein Treffer wird genommen |
| `LLM_MODELL_SHA256` | leer | leer = von Hugging Face; gesetzt = gegen diesen Wert |
| `LLM_MODELL_VERZ` | `/opt/models` | |
| `LLM_THREADS` | `4` | Aufnahmen haben Vorrang |
| `LLM_THREADS_BATCH` | leer (= `LLM_THREADS`) | Threads nur fürs **Einlesen** des Prompts (`-tb`, v5.5). Gemessen mit `-t 4`: 7,8 Token/s Einlesen, 3,4 Token/s Erzeugen. Nur setzen, wenn Aufnahme und Restream die Kerne nicht brauchen — und vorher/nachher messen (Abschnitt 5) |
| `LLM_WEBUI` | `llamacpp` | Chat-Oberfläche auf dem Port (`--webui`, v5.6): `llamacpp` ist die neue mit dem Reiter **„MCP“** in den Einstellungen, `auto` die alte von ik_llama.cpp ohne MCP, `none` keine. Gesetzt wird der Schalter nur, wenn das gebaute Programm ihn kennt |
| `LLM_WEBUI_MCP_PROXY` | `0` | `1` = CORS-Proxy für MCP-Server der Oberfläche (`--webui-mcp-proxy`). Der Server ruft dann fremde Adressen ab — laut Programm nicht in nicht vertrauten Umgebungen. Er lauscht nur auf 127.0.0.1 (SSH-Tunnel); trotzdem bewusst anschalten. Wirkt erst nach `sudo bash tools/ikllama.sh` und Neustart des Dienstes |
| `LLM_KV_CACHE` | `q8_0` | KV-Cache quantisiert (v5.3), `f16` = aus |
| `LLM_KONTEXT` | `8192` | |
| `IK_LLAMA_DIR` / `IK_LLAMA_REF` | `/opt/ik_llama.cpp` / `main` | |
| `BRAIN_LLAMACPP_URL` | `http://127.0.0.1:8080` | daraus der Port — derselbe wie vorher |

Kleinere Quantisierungen desselben Modells, wenn der RAM nicht reicht:
`Q3_K_M` (rund 7 GB), `Q2_K` (rund 6 GB) — `LLM_MODELL_DATEI` entsprechend
setzen. Der alte Qwen2.5-1.5B (rund 1 GB) läuft ebenfalls.

## 3. Die Unit — was die Schalter tun

```ini
ExecStart=/opt/ik_llama.cpp/build/bin/llama-server \
  -m /opt/models/Qwen3-14B-Uncensored.Q4_K_M.gguf -a qwen3-14b-uncensored.q4_k_m \
  --host 127.0.0.1 --port 8080 -t 4 -c 8192 -ngl 0 -rtr --jinja --no-warmup
Nice=10
CPUWeight=50
MemoryMax=13G        # Modellgroesse + 4 GB, vom Werkzeug berechnet
```

| Schalter | Warum |
|---|---|
| `-t 4` | 4 der 8 Kerne — ffmpeg-Aufnahmen und Restreams haben Vorrang |
| `-c 8192` | 4096 war zu klein für Verlauf + Frage + 1024-Token-Antwort |
| `-ngl 0` | reiner CPU-Betrieb; die Vorgabe von ik_llama.cpp ist 999 |
| `-rtr` | Gewichte beim Laden in die verschränkte Form umpacken („may improve performance"); legt das Modell ganz in den RAM, daher `MemoryMax` |
| `--jinja` | Chat-Vorlage aus dem Modell — nur damit wirkt `enable_thinking=false` |
| `-a` | Name, unter dem `/v1/models` das Modell meldet (Deck, Selbsttest) |
| kein `-fa` | Flash-Attention ist bei ik_llama.cpp ab Werk an |
| kein `-fmoe` | betrifft nur MoE-Modelle; Qwen3-14B ist dicht |

**ABWÄGUNG** (kein GPU, 8 Kerne, ffmpeg hat Vorrang):

- 14B auf der CPU ist **langsam** — grob einige Token je Sekunde. Das
  Stundenbudget (`BRAIN_LLM_MAX_CALLS_H`) und der Timeout
  (`BRAIN_LLM_TIMEOUT_S=300`) bleiben deshalb, wie sie sind.
- Reicht der RAM knapp? Kleinere Quantisierung (siehe oben) oder `-c 6144`
  über `LLM_KONTEXT`.
- Recordings stottern während KI-Last? **Nicht** auf `-t 6` erhöhen — die
  4-Kern-Grenze schützt die Aufnahmen bewusst.

**Nicht mit `--embeddings` starten.** Der Schalter beschränkt den Server auf
Embeddings (laut Server-Doku von ik_llama.cpp wie bei llama.cpp) — `/health`
wäre grün, der Chat nicht. Embeddings für das Brain kommen von einem eigenen
Server (`BRAIN_EMBED_URL`, Vorgabe Port 8089).

## 4. Qwen3 denkt — und der Bot lässt es nicht

Qwen3 schreibt ab Werk erst einen `<think>…</think>`-Block, dann die Antwort.
Auf der CPU kostet das hunderte Token vor dem ersten Wort, und bei
`max_tokens` 1024 blieb für die Antwort oft nichts. `brain/llm.py` schickt
deshalb (Vorgabe `BRAIN_LLM_DENKEN=0`):

- `chat_template_kwargs: {"enable_thinking": false}` — wirkt mit `--jinja`,
- `/no_think` an der letzten Nutzernachricht — Qwen3s eigener Schalter, wirkt
  auch ohne Vorlage,

und entfernt **jeden** Denkblock aus der Antwort (`ohne_denkblock`). Bleibt
danach nichts übrig (Denken von `max_tokens` abgeschnitten), ist das ein
Fehler für die Kette, kein leerer Erfolg — die Anfrage geht an die Cloud.

## 5. Was der Bot vom Server erwartet

| Erwartung | Warum |
|---|---|
| `--host 127.0.0.1 --port 8080` (oder `BRAIN_LLAMACPP_URL` passend) | nur lokal erreichbar — der Server hat keine Anmeldung |
| `GET /health` antwortet 200 | daran entscheidet der Bot „lokal oder Cloud" (15-s-Cache, 3 s Timeout) |
| `POST /v1/chat/completions` (OpenAI-kompatibel) | der eigentliche Chat |
| `GET /v1/models` | Modellname im Deck und im Selbsttest |
| `-t 4`, `Nice=10`, `CPUWeight=50` | Sendebild und Aufnahmen haben Vorrang |

Prüfen:

```bash
bash tools/ikllama.sh --check
systemctl status llama-server
curl -s localhost:8080/health
curl -s localhost:8080/v1/chat/completions -H 'Content-Type: application/json' \
  -d '{"messages":[{"role":"user","content":"Sag nur: ok /no_think"}],"max_tokens":16,
       "chat_template_kwargs":{"enable_thinking":false}}'
python3 bot.py --selfcheck      # Zeile „Lokales LLM: llama-server antwortet (…)"
```

## 6. NIGHTCRAWLER (.env) — nichts nötig

Das lokale LLM wird **von selbst bevorzugt**, sobald `/health` antwortet
(seit v4.2-W110). Kein Neustart des Bots nötig.

```bash
# alles Vorgaben — nur setzen, wer abweichen will
AI_PROVIDER=auto                # auto = lokal wenn erreichbar | lokal = immer zuerst | cloud = nie lokal
REACTION_AI_PROVIDER=auto
BRAIN_LLM_BACKEND=auto          # in brain/: lokal zuerst, keyless Cloud als Reserve
BRAIN_LLAMACPP_URL=http://127.0.0.1:8080
BRAIN_LLM_MAX_CALLS_H=30        # hartes Stundenbudget (danach Cloud)
BRAIN_LLM_TIMEOUT_S=300         # CPU-Inferenz braucht Zeit
BRAIN_LLM_DENKEN=0              # Qwen3-Denkmodus aus (siehe 4.)
```

Reihenfolge jeder Anfrage: **Claude** (nur mit Anthropic-Key) → **lokales
ik_llama.cpp** → **keyless Cloud** (`nc/freeai`). **Bilder (Vision) gehen
weiter in die Cloud.**

Im Brain-Panel steht in der Pille `IK_LLAMA.CPP` (lokal) bzw.
`CLOUD (RESERVE)`, in der Tabelle der Modellname.

## 7. Ollama ist entfernt

Seit V37 spricht der Bot kein Ollama mehr. Läuft der Dienst noch:
`systemctl disable --now ollama`.

## 5. AZRAEL an das lokale Modell binden (v5.5)

AZRAEL spricht seit v5.5 per Vorgabe **nur** über das lokale Modell, sobald
ein lokaler Server eingerichtet ist — ohne Claude und ohne stillen Wechsel in
die Cloud. Antwortet Qwen nicht, schweigt AZRAEL, und das Log sagt gedrosselt
warum (`AZRAEL schweigt (…)`).

| Variable | Vorgabe | Wofür |
|---|---|---|
| `AZRAEL_LLM` | `lokal` mit Server, sonst `auto` | `lokal` / `auto` (Claude → lokal → Cloud) / `cloud` |
| `AZRAEL_LOKAL_ZEIT_GESPRAECH` | `180` | Sekunden für Telegram, Discord, `!ask`, Kick-Antwort — davon die Hälfte Warten auf den Platz |
| `AZRAEL_LOKAL_ZEIT_REAKTION` | `90` | Live-Reaktion — ein Drittel Warten |
| `AZRAEL_LOKAL_ZEIT_NEBENBEI` | `60` | Eigeninitiative (Dead-Air, Hype) — wartet nie, fällt bei Stau weg |
| `BRAIN_LLM_RESERVE` | `8` | so viele Aufrufe je Stunde bleiben Gesprächen vorbehalten |

Der Bot schickt `cache_prompt` mit, und alle drei Wege beginnen mit derselben
Persona: llama-server liest sie einmal und danach aus dem Cache. Nachsehen, ob
das wirkt — `/healthz` (lokal abfragen) trägt unter `sparen`:

    curl -s http://127.0.0.1:8050/healthz | python3 -c 'import json,sys; s=json.load(sys.stdin)["sparen"]; print(json.dumps({k: s[k] for k in ("azrael_ki","lokales_llm")}, indent=1, ensure_ascii=False))'

`azrael_ki.lokal_anteil` sagt, wie oft wirklich Qwen geantwortet hat,
`lokales_llm.letzte` die Zeiten der letzten Antwort (Einlesen/Erzeugen, Token
je Sekunde, `gecacht` = Prompt-Token aus dem Cache), `cache_anteil` den Anteil
über alle Antworten.
