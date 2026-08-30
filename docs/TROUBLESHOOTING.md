# Fehlersuche

> 🌐 **Deutsch** · [English](en/TROUBLESHOOTING.md)

Die häufigen Störungsbilder und wo ihre Ursache wirklich liegt. Einstieg im
README: **[🩺 Fehlersuche](../README.md#-fehlersuche)**.

---

## Zuerst: den Bot selbst fragen

```bash
curl -s localhost:8050/api/selftest | python3 -m json.tool
```

Fasst zusammen, was sonst fünf verschiedene Log-Greps wären: tote Sendeziele,
YouTube-Grund, Abwehr-Rechte, gestörte Dauerschleifen, schweigende Kern-Loops,
Plattenfüllstand — **jeder Befund mit dem Befehl, der ihn behebt**.

---

## „Es geht nicht mehr" — stille `except`-Blöcke sind der Hauptfeind

Der Bot fängt großflächig ab und loggt auf `warning`/`debug`. Ein `log.warning`
erscheint in einem ERROR-Log **nie** — so blieb ein Discord-Gateway-Tod
monatelang unsichtbar. Wenn etwas „nicht mehr geht", suche zuerst das `except`,
das den Grund frisst.

Für periodische Schleifen gibt es `_loop_fehler(name, exc)`: erste Meldung
sofort auf `error` mit Traceback, danach höchstens alle 15 Minuten eine — mit
der Zahl der unterdrückten Fälle. Jeder Dauerläufer-Wächter gehört dorthin, nie
auf `log.debug` und nie auf `pass`.

Legitim still bleiben nur Aufräumpfade, deren Fehlschlag bedeutungslos ist
(`proc.terminate()` auf einen toten Prozess, `os.remove()` auf eine bereits
gelöschte Datei) und der Fehlerkanal selbst — dort erzeugt Loggen eine
Rekursion.

---

## Aufnahmen schlagen fehl

```
KEIN Recorder installiert — Aufnahmen werden FEHLSCHLAGEN.
```

```bash
sudo apt install ffmpeg        # empfohlen, für den nativen Pfad
pip install -U yt-dlp          # Fallback-Recorder
```

Der Recorder fällt in drei Stufen zurück: nativ (ffmpeg) → streamlink → yt-dlp.
Vor jedem Spawn läuft ein Preflight-GET, damit kein ffmpeg minutenlang gegen
eine 404 rennt.

---

## KI antwortet nicht / Antworten sind abgeschnitten

```bash
python3 -c "import nc.freeai as f; print(f.diagnose())"
```

Zeigt pro Backend: frei/gesperrt, Latenz, keyless/KEY, letzter Fehler. Bei
abgeschnittenen Antworten `BRAIN_LLM_MAX_TOKENS` erhöhen, bei Timeouts
`BRAIN_LLM_TIMEOUT_S` — beides hängt bei CPU-Inferenz zusammen.

`REACTION_AI_TIMEOUT` bleibt bewusst **kurz**: die Live-Reaktion muss snappy
sein, sonst schlägt der Watchdog Alarm.

---

## Konfiguration wird nicht übernommen

**Modul-Konstanten frieren `.env` ein.** Die `.env` wird teilweise erst nach den
ersten Imports geladen. Konfiguration deshalb immer als Funktion lesen
(`_backend_conf()`), nie als Modul-Konstante.

---

## „Online" heißt nicht „Prozess läuft"

Twitch und YouTube tragen im `tee`-Muxer `onfail=ignore` — damit ein klemmendes
Twitch nicht Kick mitreißt. Genau deshalb läuft ffmpeg weiter, wenn sie
wegbrechen: das Panel zeigte drei grüne Ziele, während auf zwei Plattformen
nichts ankam.

`_restream_verify_loop` fragt deshalb periodisch die **Plattformen selbst** ab
(Kick keyless, Twitch Helix, YouTube Data API). Die vier Regeln in
`nc/restream_guard.py` gegen Neustart-Schleifen stehen im README unter
**[📡 Restream](../README.md#-restream)**.

---

## Wenn ein Vertrag in `test_restream.py` kippt

Die statischen Verträge verankern sich an **wörtlichem Quelltext** von `bot.py`.
Ändert sich eine Signatur, kippt der Vertrag, obwohl der Code stimmt. Ebenso bei
Fenstern der Form `src[i:i + 3000]`: wächst eine Funktion darüber hinaus, meldet
der Test etwas als fehlend, das zwei Zeilen weiter unten steht.

**Vor jedem Fix am Code erst prüfen, ob der Vertrag oder nur sein Anker
gebrochen ist.**

---

Weiter: **[`DEPLOY.md`](DEPLOY.md)** (Ausrollen und Rollback) ·
**[`CROWDSEC.md`](CROWDSEC.md)** (Abwehr-Panel) ·
**[`START_HIER.txt`](START_HIER.txt)** (Erste Hilfe in einem Befehl)
