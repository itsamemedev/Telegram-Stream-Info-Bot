---
name: nc-ki-backends
description: KI-Pfade in NIGHTCRAWLER ändern oder debuggen — die Tier-Kaskade des Routers, das Stundenbudget von brain/llm.py (llama.cpp), die Basen-Rotation in nc/freeai.py mit Pro-Base-Modellen, AZRAEL-Persona und Reaction-Engine. Nutze dies bei Arbeiten an nc/freeai.py, brain/llm.py, brain/router.py, brain_bridge.py oder wenn "die KI antwortet nicht". Trigger: AZRAEL, KI, LLM, freeai, Pollinations, llama.cpp, llama-server, Tier, Router, Budget, Prompt, Modell, TTS, Reaction-Engine.
---

# KI-Backends

## Zwei getrennte Wege — nicht verwechseln

**`brain/`** ist die Entscheidungs-Maschine des Bots. Ihr LLM-Tier ist
**lokal**: `llama-server` (llama.cpp, GGUF INT4) auf `127.0.0.1:8080`.
Thread-basiert, stdlib-`urllib`, kein `aiohttp`. Kein Cloud-Zugriff.

**`nc/freeai.py`** ist der **einzige** Cloud-Pfad des Bots — OpenAI-kompatible
Endpunkte, bevorzugt keyless. Alles, was mit dem Betreiber oder dem Chat
spricht (`/ai`, AZRAEL, Reaction-Engine), läuft hierüber.

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

## Budget und Concurrency im lokalen LLM

Hartes **Stundenbudget** plus **Concurrency 1**. Der Grund ist die Hardware: die
Box hat 8 Kerne und nimmt gleichzeitig auf und restreamt. Zwei parallele
Inferenzen stehlen ffmpeg die Kerne — Aufnahmen brechen, damit die KI schneller
plaudert. Deshalb läuft `llama-server` mit `-t 4` und `Nice=10`.

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
    python3 -c "import nc.freeai as f; print(f.diagnose())"

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
