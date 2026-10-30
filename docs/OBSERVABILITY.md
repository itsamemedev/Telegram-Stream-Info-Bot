# Beobachtung — Prometheus und Grafana

> Seit v4.2-W127. Werkzeug: `tools/observability.sh`, Vorlagen: `deploy/observability/`.

Der Bot liefert unter `/metrics` seit W122 alle Kennzahlen: Loop-Verzögerung,
Aufnahmen gegen Deckel, Dateideskriptoren, Kindprozesse, Log-Schleuse, Speicher,
Platte. Prometheus hält sie 30 Tage und prüft zehn Alarmregeln; Grafana zeigt
sie als Diagramme.

## Einrichten

    sudo bash tools/observability.sh                  # gefuehrt, fragt nach Grafana
    sudo bash tools/observability.sh --grafana-repo   # mit Grafana (traegt apt.grafana.com ein)
    bash tools/observability.sh --dry-run             # zeigen, nichts tun
    bash tools/observability.sh --check               # Exit 1, wenn etwas fehlt
    sudo bash tools/observability.sh --remove         # eigene Dienste und Dateien weg

Derselbe Weg steckt in `tools/update.sh --observability[=grafana]` und im
Installer (`--observability[=grafana]` oder die Frage „Beobachtung“).

Ein zweiter Lauf schreibt nur, was sich geändert hat: Ist nur die
Konfiguration anders, lädt Prometheus sie neu (ohne Lücke in den Daten);
ist die Unit anders, startet er neu; sonst passiert nichts.

## Zugang

Alles lauscht nur auf `127.0.0.1` — Prometheus auf 9099, Grafana auf 3000.
Von außen per SSH-Tunnel:

    ssh -L 3001:127.0.0.1:3000 -L 9099:127.0.0.1:9099 nutzer@server

Dann `http://localhost:3001` (Grafana, erste Anmeldung admin/admin) bzw.
`http://localhost:9099/alerts` (Prometheus). Lokal 3001, weil der Bericht des
Installers 3000 schon für den Tunnel zum Deck vorschlägt.

## Warum so

- **Ein eigener Dienst** (`nightcrawler-prometheus`) statt `prometheus.service`
  aus dem Paket: der lauscht ab Werk auf `*:9090` an allen Schnittstellen,
  ohne Anmeldung. Hat erst dieser Lauf das Paket gebracht, wird er wieder
  abgeschaltet; lief er schon vorher, bleibt er unangetastet.
- **Kein Token:** Prometheus fragt `127.0.0.1`, und das Deck lässt Loopback
  ohne Anmeldung durch. Kein Geheimnis wird kopiert. Bindet `WEB_HOST` an eine
  einzelne fremde Adresse, bricht das Werkzeug mit einer Erklärung ab.
- **promtool vor dem Start:** eine Konfiguration, die Prometheus ablehnt, ließe
  den Dienst sonst im Kreis neu starten.
- **Grafana auf Debian/Ubuntu** liegt nicht in den Paketquellen. Die offizielle
  Quelle wird nur mit `--grafana-repo` oder nach Rückfrage eingetragen.
- **Paketnamen** stehen nur für apt fest (nachgesehen). Auf anderen Systemen
  Prometheus selbst installieren, dann richtet das Werkzeug den Rest ein.

## Alarme

`deploy/observability/rules/nightcrawler.yml` — jede Schwelle aus dem Bot:

| Alarm | Wann | Schwelle aus |
|---|---|---|
| NightcrawlerNichtErreichbar | `/metrics` 2 min ohne Antwort | — |
| NightcrawlerNeustartSchleife | 3 Neustarts in 30 min | W100 (Exitcode 4) |
| NightcrawlerKennzahlenStehen | Schnappschuss > 60 s alt oder nie | W122 |
| NightcrawlerDatenbank | `db_ok` 3 min 0 | — |
| NightcrawlerPlatteVoll | > 90 % am Aufnahmepfad | `ALERT_DISK_PCT` |
| NightcrawlerLoopStockt | p99 über dem Budget | `nc/looplag.py` |
| NightcrawlerDateiDeskriptoren | ≥ 85 % | `FD_SPERRE_ANTEIL` |
| NightcrawlerAufnahmeDeckel | 15 min am Deckel | `nc/gegendruck.py` |
| NightcrawlerLogVerluste | verworfene Logzeilen | W97 |
| NightcrawlerKindprozesseGetoetet | ≥ 3 je Stunde | `nc/kindprozess.py` |

Jede Regel hat einen Test, der sie feuern lässt — und, wo die Bedingung eine
Falle hat, einen, der sie still lässt:

    promtool test rules deploy/observability/rules/nightcrawler.test.yml

Zugestellt werden die Alarme hier noch nicht (kein Alertmanager); sie stehen
unter `http://localhost:9099/alerts` und in Grafana.
