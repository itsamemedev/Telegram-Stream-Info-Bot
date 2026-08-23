---
name: nightcrawler
description: Arbeiten am NIGHTCRAWLER-Bot (bot.py, nc/, brain/, brain_bridge.py, templates/dashboard.html) — TikTok-Live-Recording-, Restream- und KI-Moderations-Plattform. Nutze dies bei JEDER Änderung an diesen Dateien: Anker-Patching statt Volltext-Lesen, Pflicht-Validierung vor Auslieferung, bekannte Fallstricke. Trigger: bot.py, NIGHTCRAWLER, AZRAEL, Restream-Control-Room, nc/-Modul, brain/-Modul, Sendeleiste.
---

# NIGHTCRAWLER — Arbeitsanweisung

## Die eine Regel, die alles andere spart

`bot.py` hat ~29.000 Zeilen / 1,4 MB ≈ **400.000 Token pro Volltext-Lesung**.
Lies die Datei **nie** ganz. Nutze `ncpatch.py`:

```bash
python3 ncpatch.py sym  bot.py _discord_run_once   # Zeilenbereich eines Symbols
python3 ncpatch.py grep "tree.command" bot.py -C 3 # Anker finden
python3 ncpatch.py show bot.py 24750 24810         # nur diesen Ausschnitt
python3 ncpatch.py verify patches/x.json               # Trockenlauf
python3 ncpatch.py apply  patches/x.json               # Alles-oder-nichts + Validierung
```

Für Edits im Fluss reicht auch ein Python-Heredoc mit `assert src.count(old) == 1`
vor jedem `replace` — der Assert ist nicht optional. Ohne ihn ersetzt du still
mehrere Stellen oder keine.

## Pflicht-Validierung — vor JEDER Auslieferung, ohne Ausnahme

```bash
python3 -m py_compile <geänderte .py>
python3 -m pyflakes   <geänderte .py>          # 0 Befunde
python3 -m ruff check --select F,E9,B --ignore B905 <geänderte .py>
python3 ncpatch.py check                        # + Templates: doppelte IDs, CSS-Bilanz
```

Bei JS-Blöcken in `templates/*.html` zusätzlich extrahieren und `node --check`.

Zusätzlich immer prüfen:
- keine doppelten Top-Level-Defs (`ast.parse` → `module.body`)
- keine doppelten Flask-Routen **inklusive `methods=`** — gleicher Pfad mit
  GET/POST/DELETE ist *kein* Duplikat, ein naiver Regex meldet Fehlalarm
- Discord-Slash-Commands nach Änderungen gegen echte `discord.py` rekonstruieren
  (Namen `^[-_a-z0-9]{1,32}$`, Description ≤ 100 Zeichen, Signatur/`describe`-Match)

## Fallstricke, die schon zugeschlagen haben

**Stille `except`-Blöcke sind der Hauptfeind.** Der Bot fängt großflächig ab und
loggt auf `warning`/`debug`. Ein `log.warning` taucht in einem ERROR-Log **nie**
auf — genau so blieb der Discord-Gateway-Tod monatelang unsichtbar. Wenn eine
Funktion „nicht mehr geht", such zuerst nach dem `except`, das den Grund frisst,
nicht nach dem Fehler.

**Einmal-`await` ohne Supervisor.** Alles, was einen Long-Running-Client startet
(`client.start`, Websocket-Loops), braucht Reconnect mit Backoff **und** ein
Abbruchkriterium für deterministische Fehler.

**Guards als Objekt-Attribut.** `getattr(client, "_started", False)` bricht,
sobald das Objekt neu erzeugt wird → parallele Endlosschleifen. Modul-global
guarden.

**Vertragsbrüche zwischen Bot und `brain/`.** `router.route(topic, payload)` —
Handler-Erwartung und Aufrufer-Key liefen auseinander (`prompt` vs. `question`),
und weil die Flask-Route den richtigen Key nutzte, fiel nur der Telegram-Pfad
aus. Bei Payload-Änderungen **alle** Callsites prüfen: `grep -n 'router.route('`.

**Modul-Konstanten frieren `.env` ein.** `.env` wird teils nach den ersten
Imports geladen. Konfiguration als Funktion lesen (`_backend_conf()`), nicht als
Modul-Konstante.

**Ein globales Modell für mehrere API-Basen.** Jede Base kennt eigene
Modellnamen. Ein gemeinsamer Name macht jede Rotation zur Attrappe.

## Architektur-Grenzen, die einzuhalten sind

- `nc/*` und `brain/*` sind **bot-frei**: kein Import aus `bot.py`. Konfiguration
  kommt per `configure(...)`-Injection. Das hält beides isoliert testbar und
  verhindert Zirkularimporte im Monolithen.
- `brain/` ist thread-basiert und stdlib-only (urllib, kein aiohttp).
- Cloud-Zugriffe laufen ausschließlich über `nc.freeai`. Ollama existiert nicht mehr.

## Einnahmen & Geld — nicht vermischen

`REVENUE_PLATFORMS = ("kick","twitch","youtube","manuell")`. **TikTok gehört nie
dazu**: TikTok-Gifts gehen an den getrackten Streamer, nicht an eigene Kanäle.
Sie werden als `kind="gift"` gespeichert, nie als `donation`, und laufen in
keine Geldsumme.

`/api/donations/summary` = Live-Telemetrie aus **Schätzwerten**.
`nc/ledger.py` = gebuchte **Auszahlungen** für die Steuer. Niemals das eine aus
dem anderen ableiten — Anzeigewert ≠ Auszahlung ≠ Zuflusszeitpunkt.
Ledger-Einträge sind append-only mit Hash-Kette; Korrektur = Gegenbuchung.

## Sprache & Ton

Code-Kommentare und alle Ausgaben auf Deutsch. Kommentare erklären **warum**,
nicht was — bevorzugt mit dem konkreten Fehlerbild, das die Zeile verhindert.
Antworten an den Betreiber: knapp, entscheidungsfreudig, ohne Weichspüler.

## Arbeitsweise

In Wellen liefern, jede Welle validiert und abgeschlossen. Nach jeder Welle
Zwischenstand melden und auf „weiter" warten. Deploy läuft über Produktion mit
anschließender Log-/Screenshot-Beobachtung — Änderungen müssen deshalb einzeln
verifizierbar und rückrollbar sein (`ncpatch` legt `.bak` an).
