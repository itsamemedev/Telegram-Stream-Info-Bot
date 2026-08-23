---
name: nc-betrieb
description: NIGHTCRAWLER ausliefern und betreiben — ZIP über den Bestand legen, systemd-Dienst tiktok-bot, Log richtig lesen, Rollback, Dashboard-Tunnel, CrowdSec-/Kick-/YouTube-Störungsbilder. Nutze dies bei Deploy, Neustart, "läuft nicht", Log-Analyse, journalctl, Rollback, Backup, Port/Tunnel-Fragen. Trigger: deploy, ausliefern, Build, systemctl, journalctl, Dienst, Neustart, Rollback, Backup, CrowdSec, cscli, Tunnel, Port 8050, llama-server.
---

# NIGHTCRAWLER — Betrieb

## Die Lage, aus der alles folgt

Es gibt **kein Git und keine Staging-Umgebung**. Ausgeliefert wird ein ZIP, das
über den laufenden Bestand gelegt wird — auf derselben Box, die gerade
aufnimmt und restreamt. Deshalb gilt: jede Änderung einzeln verifizierbar, jede
Auslieferung mit Rettungsanker davor, Beobachtung im Log danach.

    Dienst      tiktok-bot            (systemd, Restart=always)
    Pfad        ~/tiktok-bot          (prüfen: systemctl list-units | grep -i tiktok)
    Dashboard   127.0.0.1:8050        (nie öffentlich binden)
    Brain-LLM   127.0.0.1:8080        (eigener Dienst llama-server, Nice=10)

**Nicht im Archiv und niemals überschreiben:** `.env`, `tiktok_cookies.txt`,
`recordings/`, die Datenbank. `.env.example` ist nur Vorlage.

## Auslieferung — in dieser Reihenfolge

    # 1 SICHERN — nicht überspringen
    cd ~/tiktok-bot && tar czf ../nightcrawler_backup_$(date +%F_%H%M).tgz .

    # 2 EINSPIELEN
    sudo systemctl stop tiktok-bot
    unzip -o ~/NIGHTCRAWLER_v37_<build>.zip -d ~/tiktok-bot
    sudo systemctl start tiktok-bot

    # 3 MITLESEN
    journalctl -u tiktok-bot -f

Erwartete Startzeilen: `Discord verbunden als <bot> — N Slash-Commands aktiv.` /
`Brain-LLM: llama.cpp OK` (oder `KEIN Backend erreichbar`) / `Dashboard läuft`.

Beim Rausgeben eines Builds gehört in die Begleitnotiz **welche Dateien geändert
wurden** — der Betreiber legt das Archiv über den Bestand und muss wissen, was
er zurückrollen müsste.

## Log lesen — der Teil, der zählt

`Strg+C` beendet nur das Mitlesen, nicht den Bot.

Gezielt statt alles:

    journalctl -u tiktok-bot -f | grep -Ei 'discord|brain|freeai|restream'
    journalctl -u tiktok-bot --since "10 min ago" -p warning

**Der wichtigste Reflex:** ein Fehler, der nicht im ERROR-Log steht, ist nicht
abwesend — er ist als `warning`/`debug` geloggt. Der Bot fängt großflächig ab.
Bei „Funktion X geht nicht mehr" **erst** auf `warning`-Level suchen, dann das
`except` finden, das den Grund frisst. Ein leerer Fehlerlog ist kein Beweis für
einen gesunden Dienst.

## Rollback

    sudo systemctl stop tiktok-bot
    cd ~/tiktok-bot && tar xzf ../nightcrawler_backup_<datum>.tgz
    sudo systemctl start tiktok-bot

Für einzelne Dateien reicht das `.bak`, das `ncpatch apply` anlegt.

## Dashboard ansehen

    ssh -L 3000:localhost:8050 ubuntu@<server-ip>
    # dann lokal:  http://localhost:3000

Der Port bleibt auf Loopback. Wer das Dashboard „einfach erreichbar" macht,
öffnet 283 Routen mit Config-Restore, Log-Tail und Datei-Download ins Netz —
`DASHBOARD_TOKEN` ist optional und deshalb kein Verlass.

## Prüfschritte nach dem Start

    # KI-Basen: pro Base frei/gesperrt, Latenz, keyless/KEY, letzter Fehler
    cd ~/tiktok-bot && python3 -c "import nc.freeai as f; print(f.diagnose())"

    Telegram:  /brain        Statuszeile mit aktivem Backend
               /brain teste  echte Antwort statt "keine Antwort"
               /ai hallo  ·  /einnahmen
    Discord:   /status  ·  /ai  ·  /tracklist

## Störungsbilder, die keine Code-Fehler sind

**CrowdSec-/Abwehr-Panel bleibt leer.** Ein Server-Rechte-Thema: `cscli` liest
root-only Zugangsdaten. Erst den echten Pfad feststellen (`which cscli`), dann
**denselben** Pfad passwortlos in die sudoers:

    echo 'ubuntu ALL=(root) NOPASSWD: /usr/local/bin/cscli' | sudo tee /etc/sudoers.d/nightcrawler
    sudo chmod 440 /etc/sudoers.d/nightcrawler
    sudo -n cscli decisions list -o json      # muss sauberes JSON liefern

Für die Angriffs-Liste braucht der Bot-User zusätzlich Leserechte auf die
Auth-Logs: `sudo usermod -aG adm ubuntu`, danach Dienst einmal neu starten.

**Nur Kick sendet nicht, Twitch/YouTube laufen.** `Input/output error` auf die
Kick-Ingest-URL heißt: Kick nimmt die Verbindung nicht an. Kick-seitig prüfen —
Stream-Key aktuell? Läuft schon woanders ein Stream auf denselben Key (nur einer
erlaubt)? Server-IP regional geblockt (Test von anderer IP)? Der `tee` führt Kick
mit `onfail=ignore`, ein Kick-Blip nimmt TikTok deshalb nicht mit runter. Altes
hartes Verhalten: `RESTREAM_KICK_HARD=1`.

**YouTube-Restream nicht aktiv.** Der RTMP-Key kommt automatisch über die
YouTube-Data-API. Voraussetzung: `YOUTUBE_ENABLED=1`, YouTube im Dashboard
verbunden, **und** ein Live-Stream in YouTube Studio angelegt. Grund steht im Log
(`YouTube-Restream bereit/NICHT aktiv: …`) und im Dashboard-Kanalstatus (`reason`).

**Restream-Latenz.** `RESTREAM_LOW_LATENCY=1` (Standard) fährt `-tune
zerolatency`, halben VBV-Puffer, `muxdelay=0`. Auf `0` zurückdrehen bringt mehr
Puffer und damit Robustheit bei Netz-Jitter. Die inhärente TikTok-Quell-Latenz
(HLS-Segmente) kürzt kein Re-Encode — das nie versprechen.

**Brain-LLM tot.** Eigener Dienst: `systemctl status llama-server`. Läuft mit
`-t 4` auf 4 von 8 Kernen und `Nice=10`, weil Restream-ffmpeg Vorrang hat. Wer
dort mehr Threads gibt, nimmt sie den Aufnahmen weg.

## Was beim Deploy nicht passiert

Keine Migration wird manuell gefahren — `init_db()` legt fehlende Tabellen und
Spalten beim Start selbst an (`_migrate_columns`). Schlägt eine Migration fehl,
steht das als `warning` im Log und der Dienst läuft mit fehlender Spalte weiter,
bis eine Query auf `no such column` läuft. Nach Schema-Änderungen deshalb
gezielt nach `DB-Migration` im Log greifen.
