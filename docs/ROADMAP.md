# Roadmap

> 🌐 **Deutsch** · [English](en/ROADMAP.md)

Der nächste grosse Schritt ist kein Feature, sondern Aufräumen: **`bot.py` hat
29.714 Zeilen**. Die Datei ist der Engpass des Projekts — sie lässt sich nicht
überblicken und nur mit Werkzeug bearbeiten.

Der vollständige, gemessene Plan steht in
**[`MODULARISIERUNG.md`](MODULARISIERUNG.md)**. Hier die Kurzfassung.

---

## Die sechs Wellen

| Welle | Inhalt | Zeilen |
|---|---|---:|
| **0** | Fundament — `nc/ctx.py` für die 13 echten Querschnittshelfer | ±0 |
| **1** | Die 173 global-freien Funktionen bündeln | −2.200 |
| **2** | Blueprint-Pilot `/api/recordings` — beweist das Verfahren | −470 |
| **3** | Blueprints in Serie — **der grosse Hebel** | −7.600 |
| **4** | `RestreamManager` und `KickModerator` herauslösen | −1.700 |
| **5** | Discord-Schicht nach `discord_ext/` | −2.100 |
| **6** | Kern aufräumen, `bot.py` wird Kompositionswurzel | Rest |

Welle 2 ist erledigt, Welle 3 läuft: `nc/routes/` trägt heute 18 Blueprints mit
187 API-Routen, die nicht mehr im Monolithen stehen.

---

## Warum das machbar ist

Zwei Messungen, keine Schätzungen:

1. **Die Kopplung ist flach.** Median 2 Fremdbezüge je Route, nur 13 echte
   Querschnittshelfer. Eine Route herauszulösen zieht selten mehr als eine
   Handvoll Namen mit.
2. **Es gibt kein einziges `url_for` im Projekt.** Flask-Blueprints sind hier
   deshalb verhaltensneutral — der Umzug einer Route ändert keine URL und
   bricht kein Template.

---

## Die Messlatte

Nicht die Zeilenzahl entscheidet, ob das Ziel erreicht ist, sondern:

> **Eine neue API-Route anlegen, ohne `bot.py` zu öffnen.**

---

Weiter: **[`MODULARISIERUNG.md`](MODULARISIERUNG.md)** (der volle Plan) ·
**[`CHANGELOG.md`](CHANGELOG.md)** (was schon drin ist)
