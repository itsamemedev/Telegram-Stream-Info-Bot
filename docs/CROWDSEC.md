# CrowdSec für Azrael Sentinel einrichten

Stand: v4.0-W23

> **Wichtigste Regel zuerst:** Nimm den LAPI-Port **nicht an** — **ermittle** ihn
> (Schritt 2). „8083“ ist der Wert aus einem konkreten Setup, nicht der Standard.
> CrowdSec startet standardmäßig auf **8080**. Ein falsch angenommener Port ist
> die häufigste Ursache für „verbindet nicht“.

---

## Was der Bot mit CrowdSec macht

Der Bot **sperrt nichts selbst**. Er *liest* die Entscheidungen (Bans), die
CrowdSec getroffen hat, und zeigt sie im Dashboard (Panel **Abwehr · CrowdSec**
+ Weltkarte). Das eigentliche Blockieren macht ein **Bouncer** (Schritt 4c).

Zwei Wege, der Bot nimmt automatisch den ersten, wenn ein Schlüssel gesetzt ist:

* **Weg A — Bouncer-Schlüssel (empfohlen, ohne Root).** Der Bot fragt die LAPI
  über HTTP mit einem API-Schlüssel ab. **Keine sudo-Regel nötig**, jederzeit
  widerrufbar.
* **Weg B — `cscli`** (Rückfallebene). Braucht Root → sudoers-Regel (3b).

**Neu ab W23:** Im Dashboard-Panel **Abwehr · CrowdSec** gibt es den Knopf
**„Verbindung testen“**. Er geht **genau den Weg, den der Bot geht**, und zeigt
Modus, die exakt abgefragte URL, ob ein Schlüssel gesetzt ist, sowie den
konkreten Fehlergrund + Behebungsbefehl. Nach jedem Schritt hier: diesen Knopf
drücken — er ist die ehrlichste Rückmeldung, nicht ein selbst gebautes `curl`.

---

## 1. Ist CrowdSec installiert?

```bash
sudo systemctl status crowdsec        # muss "active (running)" sein
cscli version
```

Fehlt es:

```bash
curl -s https://install.crowdsec.net | sudo sh
sudo apt install crowdsec
```

---

## 2. Die ECHTE LAPI-Adresse ermitteln (nicht raten)

CrowdSec sagt dir selbst, wo seine LAPI hört:

```bash
sudo cscli lapi status
```

Die Zeile **„Trying to authenticate … on http://HOST:PORT/“** ist die Adresse,
die du brauchst — Host **und** Port. Zur Gegenprobe die Konfiguration:

```bash
grep -A2 'server:' /etc/crowdsec/config.yaml     # listen_uri: 127.0.0.1:PORT
```

> **Merke dir HOST und PORT aus dieser Ausgabe.** Alles Weitere benutzt genau
> diese Werte. In dieser Anleitung steht `PORT` — setze deinen echten Port ein
> (z. B. 8080 oder, falls du ihn umgestellt hast, 8083).

**Nur wenn du den Port bewusst ändern willst**, in `/etc/crowdsec/config.yaml`:

```yaml
api:
  server:
    listen_uri: 127.0.0.1:PORT
```

Danach `sudo systemctl restart crowdsec` und `sudo cscli lapi status` erneut —
muss „successfully interact with LAPI“ melden.

> Läuft die LAPI mit **TLS** (Abschnitt `tls:` unter `api.server` in der
> config.yaml, URL beginnt mit `https://`)? Dann kann der Bot sie derzeit nicht
> abfragen — LAPI für 127.0.0.1 auf `http` betreiben (lokal ist das sicher) oder
> Weg B (cscli) nutzen.

---

## 3. Weg A — Bouncer-Schlüssel anlegen (empfohlen)

```bash
sudo cscli bouncers add azrael-dashboard
```

CrowdSec gibt **einmalig** einen API-Schlüssel aus. Diesen in die **`.env`** des
Bots (nicht in die Shell):

```bash
CROWDSEC_BOUNCER_KEY=<der ausgegebene Schlüssel>
CROWDSEC_LAPI_HOST=127.0.0.1
CROWDSEC_LAPI_PORT=PORT           # der ECHTE Port aus Schritt 2
# Alternativ statt Host/Port die komplette Adresse:
# CROWDSEC_LAPI_URL=http://127.0.0.1:PORT
```

Bot neu starten, damit die `.env` gelesen wird:

```bash
sudo systemctl restart tiktok-bot
```

Dann im Dashboard **Abwehr · CrowdSec → „Verbindung testen“**. Erwartet:
„verbunden · LAPI · Schlüssel gesetzt“. Steht dort ein Fehler, zeigt der Knopf
Grund + Befehl.

### 3a. Von Hand gegenprüfen — die Schlüssel-Falle

Der Schlüssel steht in der **`.env`**, **nicht** in deiner Shell. Ein blindes

```bash
curl -H "X-Api-Key: $CROWDSEC_BOUNCER_KEY" http://127.0.0.1:PORT/v1/decisions
```

sendet einen **leeren** Schlüssel → **403** → du hältst es fälschlich für kaputt.
Richtig ist eines von beiden:

```bash
# a) Variablen aus der .env in die aktuelle Shell laden:
set -a; . /pfad/zur/.env; set +a
curl -s -H "X-Api-Key: $CROWDSEC_BOUNCER_KEY" \
     "http://127.0.0.1:$CROWDSEC_LAPI_PORT/v1/decisions" ; echo

# b) oder den Schlüssel wörtlich einsetzen (nicht als Variable):
curl -s -H "X-Api-Key: DER_ECHTE_SCHLUESSEL" \
     http://127.0.0.1:PORT/v1/decisions ; echo
```

* `null` oder `[]` → **verbunden, aktuell niemand gesperrt** (Erfolg, kein Fehler).
* `[{...}]` → verbunden, es gibt Bans.
* `access forbidden` / HTTP 403 → Schlüssel falsch oder widerrufen → neu anlegen.

Zeige die angelegten Zugänge / widerrufe einen:

```bash
sudo cscli bouncers list
sudo cscli bouncers delete azrael-dashboard
```

---

## 3b. Nur für Weg B: der Bot darf `cscli` als root aufrufen

`cscli` liest LAPI-Zugangsdaten, die **root** gehören. Ohne Rechte kommt
„permission denied“ oder ein Go-Panic. Passwortlose sudo-Regel **nur für dieses
eine Kommando** — Pfad exakt so, wie `command -v cscli` ihn ausgibt:

```bash
echo "$(whoami) ALL=(root) NOPASSWD: $(command -v cscli)" \
  | sudo tee /etc/sudoers.d/nightcrawler
sudo chmod 440 /etc/sudoers.d/nightcrawler
sudo systemctl restart tiktok-bot
sudo -n cscli decisions list -o json | head    # muss ohne Passwort laufen
```

Ist ein Bouncer-Schlüssel gesetzt (Weg A), wird 3b **nicht** gebraucht.

---

## 4. Was überwacht und gesperrt wird

### 4a. Sammler für deine Dienste

```bash
sudo cscli collections install crowdsecurity/sshd
sudo cscli collections install crowdsecurity/nginx          # falls nginx die Website liefert
sudo cscli collections install crowdsecurity/base-http-scenarios
sudo systemctl reload crowdsec
sudo cscli collections list
```

### 4b. Das Dashboard selbst überwachen

In `/etc/crowdsec/acquis.yaml` ergänzen (das Bot-Log über journald):

```yaml
---
source: journalctl
journalctl_filter:
  - "_SYSTEMD_UNIT=tiktok-bot.service"
labels:
  type: syslog
```

```bash
sudo systemctl reload crowdsec
sudo cscli metrics          # "Acquisition" muss Zeilen für die Quelle zeigen
```

### 4c. Bouncer — erst hier wird wirklich blockiert

```bash
sudo apt install crowdsec-firewall-bouncer-iptables
sudo systemctl status crowdsec-firewall-bouncer
```

Testsperre (erscheint binnen ~1 min im Dashboard, dann wieder entfernen):

```bash
sudo cscli decisions add --ip 203.0.113.10 --duration 5m --reason "Test"
sudo cscli decisions list
sudo cscli decisions delete --ip 203.0.113.10
```

---

## 5. Zusammenspiel mit dem Dashboard-Token

* **DASHBOARD_TOKEN** = wer darf ins Dashboard.
* **CrowdSec** = wer wird nach Fehlversuchen gar nicht erst durchgelassen.

Hängt ein Reverse-Proxy davor, in der `.env` setzen, sonst sieht der Bot nur die
Proxy-IP:

```bash
TRUSTED_PROXIES=<IP-des-Proxys>
```

---

## 6. Fehlersuche — was der „Verbindung testen“-Knopf anzeigt

| Anzeige / status | Bedeutung | Behebung |
|---|---|---|
| `verbunden`, 0 gesperrt | Alles läuft, nur noch nichts erkannt | Normal. Mit 4c testen |
| `kein_zugang` (401/403) | Bouncer-Schlüssel falsch oder widerrufen | `sudo cscli bouncers list`, ggf. neu anlegen (Schritt 3) |
| `lapi_pfad` (404) | LAPI erreichbar, aber falscher Port/Dienst | Port aus Schritt 2 mit `.env` vergleichen |
| `lapi_tot` | Dienst/LAPI antwortet nicht (falscher Port? TLS?) | Schritt 2, `sudo systemctl restart crowdsec` |
| `kein_sudo` (nur Weg B) | sudo-Regel fehlt/falscher Pfad | Schritt 3b (`command -v cscli`) |
| `fehlt` | CrowdSec nicht installiert | Schritt 1 |

Nützliche Befehle:

```bash
sudo cscli lapi status          # LAPI-Adresse + erreichbar?
sudo cscli decisions list       # was ist gesperrt
sudo cscli metrics              # kommen Logzeilen an
journalctl -u crowdsec -n 50    # Dienstprotokoll
```

---

## 7. Kurzfassung

1. `sudo cscli lapi status` → **echten HOST:PORT ablesen** (nicht raten).
2. `sudo cscli bouncers add azrael-dashboard` → Schlüssel in die `.env`
   (`CROWDSEC_BOUNCER_KEY` + `CROWDSEC_LAPI_PORT` mit dem echten Port).
3. `sudo systemctl restart tiktok-bot`.
4. Dashboard → **Abwehr · CrowdSec → „Verbindung testen“** → muss „verbunden“
   zeigen (oder Grund + Fix).
5. Sammler + `acquis.yaml` + Firewall-Bouncer, dann Testsperre.
