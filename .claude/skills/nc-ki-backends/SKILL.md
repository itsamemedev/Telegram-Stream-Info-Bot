---
name: nc-ki-backends
description: KI-Pfade in NIGHTCRAWLER ändern oder debuggen — die Tier-Kaskade des Routers, das Stundenbudget von brain/llm.py (llama.cpp), die Basen-Rotation in nc/freeai.py mit Pro-Base-Modellen, AZRAEL-Persona und Reaction-Engine. Nutze dies bei Arbeiten an nc/freeai.py, brain/llm.py, brain/router.py, brain_bridge.py oder wenn "die KI antwortet nicht". Trigger: AZRAEL, KI, LLM, freeai, Pollinations, llama.cpp, llama-server, Tier, Router, Budget, Prompt, Modell, TTS, Reaction-Engine.
---

# KI-Backends

## Zwei getrennte Wege — nicht verwechseln

**`brain/`** ist die Entscheidungs-Maschine des Bots. Ihr LLM-Tier ist
**lokal**: `llama-server` auf `127.0.0.1:8080` — seit v5.1-W181
**ik_llama.cpp** mit **Qwen3-14B-Uncensored** (GGUF Q4_K_M, rund 9 GB),
eingerichtet von `tools/ikllama.sh` (Installer und `update.sh --ik-llama`
rufen es; ein altes llama.cpp wird zuerst entfernt). Der Bot spricht nur HTTP
mit dem Server — `/health`, `/v1/chat/completions`, `/v1/models` —, also
aendert der Umstieg an `brain/llm.py` nur eines:

**Qwen3 denkt.** Ab Werk steht vor jeder Antwort ein `<think>…</think>`-Block,
auf der CPU hunderte Token. `brain/llm.py` schickt deshalb
`chat_template_kwargs={"enable_thinking": false}` (wirkt mit `--jinja` in der
Unit) **und** `/no_think` an der letzten Nutzernachricht (auf einer Kopie —
der Verlauf des Aufrufers bleibt sauber), und `ohne_denkblock()` nimmt jeden
Denkblock aus der Antwort. Bleibt nur Denken uebrig, ist das ein Fehler fuer
die Kette, kein leerer Erfolg. Schalter: `BRAIN_LLM_DENKEN` (Vorgabe 0). Wer
einen neuen lokalen Aufrufer baut, geht durch `LLMRuntime.chat()` — sonst
landet der Denkblock im Chat, im Overlay und in der Sprachausgabe.
Thread-basiert, stdlib-`urllib`, kein `aiohttp`. Kein Cloud-Zugriff.

**`nc/freeai.py`** ist der **einzige** Cloud-Pfad des Bots — OpenAI-kompatible
Endpunkte, bevorzugt keyless.

**`nc/kiwahl.py`** entscheidet seit v4.2-W110, ob lokal oder Cloud: Chat
(`/ai`), AZRAEL und Reaction-Engine fragen `lokal_zuerst()`. Vorgabe `auto` =
lokales llama.cpp, sobald `/health` antwortet. **Nie wieder
`os.getenv("AI_PROVIDER")` selbst lesen** — das stand siebenmal verstreut, und
jede Anzeige rechnete anders. Reihenfolge: Claude (mit Key) → lokal → Cloud.
„Ist lokal installiert?" beantwortet `lokal_installiert()` (Units und
`/opt/ik_llama.cpp`), nicht `shutil.which("llama-server")` — ik_llama.cpp liegt
nicht im PATH.

Ollama existiert nicht mehr. Neue Cloud-Aufrufe gehören nach `nc.freeai`, nicht
direkt in Aufrufercode — sonst gibt es Rotation und Fehlerklassifikation nicht.

## Die Tier-Kaskade — warum das LLM zuletzt kommt

    RULES      deterministisch, µs
    DB         Faktenabfrage, ms
    KNOWLEDGE  Graph-Inferenz, ms
    LLM        nur wenn nichts anderes konnte

`router.route(topic, payload)` geht die Tiers in dieser Reihenfolge durch und
protokolliert pro Tier, **warum** weitergereicht wurde — dieser `trace` ist die
Erklärbarkeit im Dashboard und darf nicht wegoptimiert werden. Ein Tier-Fehler
reicht weiter statt abzubrechen; `Unhandled` (bewusst Exception, nicht `None`)
heißt: kein Tier konnte, und das wird dem Nutzer ehrlich so gesagt.

Wer eine neue Fähigkeit baut, prüft erst, ob sie in RULES oder DB gehört. Ein
Handler im LLM-Tier für etwas, das eine Query beantwortet, verbrennt Budget und
macht die Antwort nichtdeterministisch.

**Payload-Verträge sind die Bruchstelle.** Bei Änderung eines Handler-Keys alle
Callsites prüfen: `grep -n 'router.route('`. Ein Drift `prompt` vs. `question`
fiel monatelang nur im Telegram-Pfad aus, weil die Flask-Route den richtigen Key
benutzte — und niemand testet den Pfad, der noch geht.

## Plätze und Deckel im lokalen LLM

Seit v5.9-W202 **mehrere Inferenz-Plätze** und **kein Stundendeckel per
Vorgabe**. Die Kerne schützt `-t 4` mit `Nice=10`/`CPUWeight=50` — mehrere
Plätze rechnen in denselben vier Threads (llama-server bündelt sie zu einem
Schritt), sie nehmen ffmpeg keine Kerne weg. Die Zahl der Plätze steht genau
einmal: `LLM_PLAETZE` in `tools/ikllama.sh` (`-np`); `brain/llm.py` liest sie
beim Server (`/props` → `total_slots`), `BRAIN_LLM_PLAETZE` erzwingt eine Zahl.
Der Platz gilt **nur** dem lokalen Modell — die Cloud wartet nie dahinter.
Eigeninitiative bekommt nie den letzten freien Platz, und die Warteschlange ist
begrenzt (drei je Platz): jeder Wartende hält einen Thread fest.
`BRAIN_LLM_MAX_CALLS_H` > 0 setzt wieder einen Stundendeckel (mit
`BRAIN_LLM_RESERVE` für Gespräche). Mit 14B ist eine Antwort langsam (grob
einige Token je Sekunde) — das ist der Preis, nicht ein Grund, `-t` zu heben.

`BudgetExhausted` ist kein Fehler, sondern ein Ergebnis: der Router reicht es als
`Unhandled` weiter. Es wird nie stumm geschluckt und nie in eine Wiederholung
umgebaut.

Zwei Werte sind bewusst eingestellt und nicht „zu großzügig": Timeout **nicht**
60s (CPU-Inferenz ohne GPU braucht länger) und `max_tokens` **1024**, weil 512
längere Antworten abschnitt.

Konfiguration wird zur **Laufzeit** gelesen, nicht als Modul-Konstante — `.env`
ist beim Import teils noch nicht geladen. Dieses Muster bei Erweiterungen
beibehalten.

## Basen-Rotation in `nc/freeai.py`

Vertrag: `(text, error_kind)` mit
`error_kind ∈ {None, 'auth', 'rate_limit', 'http', 'timeout', 'net', 'empty'}`.
Dieser Vertrag ist stabil zu halten — das Dashboard und die Fehleranzeige hängen
daran.

**Die Falle, die die Rotation schon einmal komplett tot gemacht hat:** ein
*globaler* Modellname für alle Basen. Nur Pollinations kennt den Alias `openai`;
jede Rotation auf eine zweite Base lief sofort in HTTP 400/404 „unknown model".
Fiel Base 1 aus, fiel alles aus — die Rotation war eine Attrappe. Seit B120 hat
**jede Base im `_CATALOG` ihre eigene Modell-Liste**; der Modellname des
Aufrufers ist nur ein *Wunsch* und geht ausschließlich an Basen, die ihn kennen.
Wer eine Base hinzufügt, trägt deren echte Modellnamen ein — kein Copy-Paste der
Liste von oben.

Weitere Eigenheiten, die man nicht raten kann:

- **Referrer-Auth.** Pollinations identifiziert keylose Aufrufer über
  `Referer`/`referrer`. Ohne den Header landet ein Server-Request im striktesten
  Anonym-Bucket. `FREEAI_REFERRER` setzt ihn (Default `nightcrawler`).
- **HTTP 402 zählt als `auth`**, nicht als generisches `http` — sonst zeigt das
  Dashboard „HTTP-Fehler", wo „Base verlangt jetzt einen Key" die eigentliche
  Aussage ist.
- **Reihenfolge im Katalog** ist nur die Startreihenfolge; danach sortiert die
  gemessene Latenz. Gesperrte Basen (`_base_block`) fallen bis Ablauf raus.
- `text.pollinations.ai/openai` ist der keylose Altpfad, `gen.pollinations.ai`
  der aktuelle Gateway (Key empfohlen: `POLLINATIONS_API_KEY` von
  enter.pollinations.ai). `LLM7_TOKEN` von token.llm7.io hebt 30 auf 120
  Anfragen/min.

## „Die KI antwortet nicht" — Diagnose in dieser Reihenfolge

    # 1 Cloud-Kette: pro Base frei/gesperrt, Latenz, keyless/KEY, letzter Fehler
    python3 -c "from dotenv import load_dotenv; load_dotenv(); import nc.freeai as f; print(f.diagnose())"

**`load_dotenv()` gehört zwingend davor.** `nc/freeai` ist bot-frei und lädt die
`.env` nie selbst — im Bot macht das `bot.py`. Ein nacktes
`python3 -c "import nc.freeai …"` zeigt deshalb **immer `keyless`**, auch wenn
`POLLINATIONS_API_KEY` und `LLM7_TOKEN` sauber gesetzt sind. Das Kommando stand
bis v4.2-W69 an acht Stellen ohne den Vorspann und hat damit genau die Frage
falsch beantwortet, für die man es aufruft. Wer „keyless" sieht, prüft zuerst,
ob er den Vorspann vergessen hat, und erst dann die `.env`.

    # 2 lokales LLM
    systemctl status llama-server
    journalctl -u tiktok-bot -f | grep -Ei 'brain|freeai|llm'

    # 3 Telegram /brain teste     — echte Antwort, nicht nur Statuszeile
    #   /brain allein zeigt nur, welches Backend gemeldet wird

Melden **alle** Pollinations-Basen `auth`, ist ein Key fällig — das ist kein
Code-Fehler. Melden alle `net`, prüfe zuerst den Proxy-Pfad, nicht den Client.

`last_errors()`/`diagnose()` merken pro Base den letzten echten Fehler
einschließlich Body-Anfang. Diese Speicherung nicht entfernen: ohne sie ist ein
Kettenausfall blind, weil jede Base einzeln nur „ging nicht" sagt.

## AZRAEL

**Seit v5.5-W196 an das lokale Modell gebunden** (`AZRAEL_LLM`, `nc/kiwahl.py`).
Jeder Persona-Aufruf geht durch `ai_chat(..., zweck=…)`. Der Zweck ergibt
einen Vorrang (`gespraech` > `reaktion` > `nebenbei`), und bei `lokal` geht der
Aufruf nur an Qwen (`_azrael_lokal`): kein Claude, kein stiller Rückfall in
die Cloud. Wer einen neuen AZRAEL-Weg baut, gibt `zweck=` mit. Ohne das landet
er in der allgemeinen Kette und spricht womöglich mit fremder Stimme. Zwei
Regeln, gemessen begründet (7,8 Token/s beim Einlesen auf der Box):

- **Persona zuerst, Wechselndes zuletzt.** llama-server nutzt aus dem Cache nur
  den gleichen *Anfang* (`cache_prompt`). Alle Wege beginnen mit
  `_azrael_persona_kern()`; Live-Zustand, Erinnerungen und Aufgabe stehen hinten.
- **Nicht warten lassen, was niemand angefordert hat.** Eigeninitiative wartet
  nie auf den Platz und bekommt die `BRAIN_LLM_RESERVE` nicht.

`/healthz` → `sparen.azrael_ki` (wer antwortet) und `sparen.lokales_llm`
(Zeiten, Cache-Anteil) beantworten „spricht AZRAEL wirklich mit Qwen?".

Persona, Stimme und Reaktionsverhalten sind **Konfiguration**, kein Code:
`.env`-Blöcke *AZRAEL: Persona*, *AZRAEL Stimme / TTS* und
*LIVE-REACTION-ENGINE*. Verhaltensänderungen gehören dorthin, nicht in
hartcodierte Prompts.

TTS läuft entweder browserseitig (Web-Speech im Overlay) oder serverseitig
(Piper). Der Server-Pfad kostet CPU auf derselben Box wie Aufnahme und Restream —
gilt dieselbe Vorrang-Regel wie beim LLM.

Overlay-Ausgabe geht über `127.0.0.1:8050/overlay` in den Restream. Änderungen
am Overlay sind damit **stream-sichtbar** — das ist Produktion, nicht Vorschau.

## Prüfung vor Auslieferung

    python -m py_compile nc/freeai.py brain/llm.py brain/router.py
    python -m pyflakes   nc/freeai.py brain/llm.py brain/router.py
    python test_m2_bridge.py
    python brain/test_m6.py            # LLM-Tier
    python brain/test_m7.py

`brain/` bleibt stdlib-only. Ein `aiohttp`- oder `requests`-Import dort ist ein
Architekturbruch, auch wenn er läuft.
