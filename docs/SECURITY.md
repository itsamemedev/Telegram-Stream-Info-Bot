# Sicherheitsrichtlinie

> 🌐 **Deutsch** · [English](en/SECURITY.md)

## Unterstützte Versionen

| Version | Unterstützt |
|---|---|
| 4.3.x (`Freie Sicht`) | ✅ |
| 4.2.x (`Zerlegter Kern`) | ⚠️ nur kritische Lücken |
| < 4.2 | ❌ |

## Eine Lücke melden

**Bitte kein öffentliches Issue.**

Melde Sicherheitslücken über **[GitHub Security Advisories](https://github.com/itsamemedev/Telegram-Stream-Info-Bot/security/advisories/new)**
(„Report a vulnerability") oder per E-Mail an den Repository-Inhaber.

Hilfreich in der Meldung:

- Betroffene Datei / Route / Modul und Version
- Wie sich das Problem reproduzieren lässt
- Wirkung: Was kann ein Angreifer damit erreichen?
- Falls vorhanden: ein Vorschlag zur Behebung

**Bitte redigiere Logausschnitte vor dem Versand** — sie enthalten
regelmäßig Cookies, OAuth-Tokens und Stream-Keys.

### Was du erwarten kannst

| Schritt | Rahmen |
|---|---|
| Empfangsbestätigung | innerhalb von 72 Stunden |
| Erste Einschätzung | innerhalb von 7 Tagen |
| Fix bzw. Zeitplan | nach Schweregrad, kritische Lücken zuerst |
| Nennung im Advisory | auf Wunsch, gerne |

Bitte gib uns Zeit für einen Fix, bevor du Details veröffentlichst.

---

## Betriebshinweise — die häufigsten Fußangeln

Die meisten realen Risiken in diesem Projekt entstehen beim Betrieb, nicht im
Code. Diese Punkte sind Pflicht:

### `.env` ist der Kronjuwelen-Speicher

Rund 523 Variablen, darunter Cookies, OAuth-Tokens, API-Schlüssel und
RTMP-Stream-Keys. Ein Stream-Key erlaubt jedem, auf deinem Kanal zu senden.

```bash
chmod 600 .env
```

Sie steht in `.gitignore` und liegt nie im Auslieferungsarchiv. **Ein einmal
committetes Geheimnis steht auch nach dem Löschen noch in der Historie** — dann
hilft nur: Schlüssel widerrufen und neu ausstellen.

### Das Dashboard gehört nicht ins offene Netz

Standard ist `127.0.0.1:8050`. Zugriff läuft über einen SSH-Tunnel:

```bash
ssh -L 3000:localhost:8050 ubuntu@<server-ip>
```

Wer das Dashboard öffentlich erreichbar macht, stellt einen vollständigen
Fernsteuerungs-Kontrollraum ins Netz — inklusive Aufnahme-Archiv,
Einnahmen-Journal und Restream-Steuerung. Wenn es sein muss: Reverse Proxy mit
TLS **und** Authentifizierung davor, `DASHBOARD_TOKEN` setzen, und die
CrowdSec-Anbindung aktivieren (siehe [`docs/CROWDSEC.md`](CROWDSEC.md)).

### Log-Redaction nicht umgehen

Beim Loggen von `streamlink`- und `ffmpeg`-Kommandozeilen werden Cookie-Header
und Stream-Keys unkenntlich gemacht. Wer die Kommandozeilen-Erzeugung ändert,
muss sicherstellen, dass der Redact-Pfad weiterhin greift.

### Totmann-Meldung einrichten

Stirbt der Prozess ganz, sagt dir das sonst niemand — auch nicht, wenn der Grund
ein Angriff war:

```bash
chmod +x tools/notify_failure.sh
sudo systemctl edit nightcrawler   # → [Unit] OnFailure=nightcrawler-notify@%n.service
```

### Abhängigkeiten einfrieren

`requirements.txt` lässt Versionen bewusst offen. Friere auf dem Server den
laufenden Stand ein und halte ihn nach:

```bash
python3 -m pip freeze > requirements.lock.txt
```

## Auditstand

Letzter vollständiger Durchgang: **v4.3-W58** (der davor: v4.0-W118).
Abgedeckt wurden dieselben Klassen wie damals, gegen den heutigen Stand:

| Klasse | Ergebnis |
|---|---|
| Code-Ausführung (`eval`/`exec`/`pickle`/`yaml.load`) | kein Treffer |
| `shell=True` | ein Treffer — `SWAP_CLEAR_CMD`, die unten begründete Ausnahme |
| SQL-Injektion, inkl. der LLM-übersetzten Abfrage | kein Treffer |
| Pfad-Traversal in allen Datei-Routen | kein Treffer |
| Dashboard-Auth (Token, PIN, Rate-Limit, Zeitkonstanz) | kein Treffer |
| Geheimnisse in Logs und API-Antworten | kein Treffer |
| XSS in den drei Templates | **ein Befund, behoben (W58)** |
| SSRF | kein Treffer |
| OAuth-CSRF | ein Hinweis, siehe unten |
| Abhängigkeiten | unverändert offen, siehe unten |

**Was geprüft wurde, nicht nur behauptet:**

*SQL.* Sechs Stellen bauen ihr Statement mit einem f-String. Alle
interpolieren ausschließlich fest verdrahtete Spaltennamen (`"name=?"`) oder
eine im Quelltext stehende Tabellenliste; die Werte sind durchweg gebunden.
Der NL→SQL-Rückfall `_rule_based_sql` setzt den Fragetext **nie** ins
Statement — nur eine interne Zeitfenster-Konstante. Die LLM-Variante ist auf
`select`/`with` und ein einzelnes Statement begrenzt.

*Geheimnisse in Logs.* Der heikelste Pfad ist neu: seit v4.2-W46 wird der
`stderr` des Audio-Taps überhaupt erst gelesen, und darin steht die signierte
Quell-URL. Er geht durch `_log_sicher` (`nc/logsafe.redact_pull_urls`), mit
Begründung an der Zeile. Keine rohe Stream-URL im Log, keine in einer
API-Antwort.

*Pfad-Traversal.* Icons über eine Whitelist, Downloads über `realpath` +
`commonpath` gegen das erlaubte Verzeichnis, dreizehn weitere Stellen über
`nc.sicherpfad`.

*Dashboard-Auth.* Token und PIN werden mit `hmac.compare_digest` verglichen;
Fehlversuche zählen pro IP und sperren 60 Sekunden, die Tabelle ist gedeckelt.

Der XSS-Befund aus W58 hat einen Vertrag in `test_nc_modules.py`; ein Rückfall
fällt in der Prüfkette auf, nicht im Betrieb.

### Drei Dinge bleiben bewusst offen

Sie sind **keine** Nachlässigkeit, sondern Betreiber-Entscheidungen:

- **`SWAP_CLEAR_CMD` läuft mit `shell=True`.** Die Shell wird für `&&`
  gebraucht. Wer `.env` schreiben kann, kann ohnehin beliebigen Code
  ausführen — die Datei ist die Vertrauenswurzel, nicht diese Zeile.

- **Ungepinnte Abhängigkeiten** (siehe oben). Einfrieren ist Server-Arbeit;
  geratene Versionsnummern wären schlimmer als keine. Stand heute: null von 63
  Einträgen in `requirements.txt` sind gepinnt.

- **Der OAuth-`state` von Twitch und YouTube liegt nur im Speicher.** Beide
  prüfen ihn, wenn einer ausgegeben wurde — aber nicht, wenn gerade kein Flow
  läuft. Kick macht es strenger: es legt den `state` persistent ab und lehnt
  jeden Rückruf ab, der nicht dazu passt. Twitch und YouTube genauso streng zu
  machen hieße, den `state` ebenfalls zu persistieren, sonst bricht ein
  legitimer Flow über einen Neustart hinweg ab. Solange das Dashboard wie
  vorgesehen auf `127.0.0.1` hört, ist der Rückruf von außen nicht erreichbar;
  wer es öffentlich stellt, sollte diesen Punkt zuerst nachziehen.

## Was ausdrücklich **keine** Lücke ist

- Ein offenes Dashboard, das jemand selbst ins Netz gestellt hat.
- Eine `.env`, die jemand selbst committet hat.
- Rate-Limits oder Sperren der Fremdplattformen (TikTok, Kick, Twitch, YouTube).
- Fehlalarme der Moderations-Heuristik. Das ist ein normales Issue —
  der Shield ist bewusst auf null False Positives getrimmt, Meldungen dazu sind
  willkommen.
