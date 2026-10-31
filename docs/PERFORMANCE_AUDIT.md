# Performance-Audit

> Alle Zahlen stammen aus Produktions-Logs des Betreibers
> (`_leistung_erheben` alle 15 Minuten, `_loop_stockung_melden`,
> `_verbindung_verloren`). Keine geschätzten Werte. Wo die Messdauer zu kurz
> für ein Urteil ist, steht das dabei.

## Messreihen

| Lauf | Stand | Dauer | Quelle |
|---|---|---|---|
| A | v4.4 (W132) | 00:44–04:19, 3 h 35 min | debug.log vom 31.10. früh |
| B | v4.4.1 (W133) + Paket-Upgrade W135 | 06:01–06:48, **46 min** | debug.log vom 31.10. morgens |

## 1. Speicher (RSS)

| Zeitpunkt nach Start | A | B |
|---|---|---|
| ~10 s | 232 MB | 708 MB |
| ~15 min | 817 MB | 749 MB |
| ~30 min | 852 MB | 750 MB |
| ~45 min | 821 MB | 751 MB |
| ~1 h 30 | 1078 MB | — |
| ~3 h 30 | 1459 MB | — |

**Lesart.** Nach der Anlaufphase stieg Lauf B in 30 Minuten um 2 MB; Lauf A
im selben Abschnitt um rund 50 MB und danach stufenweise um 130–230 MB je
Viertelstunde, auch ohne laufende Aufnahme. Der Unterschied fällt mit W133
zusammen (der Kick-Chat verband sich bis dahin knapp jede Sekunde neu).

**Nicht belegt** ist, dass W133 die Ursache war: 46 Minuten reichen nicht, und
Lauf A wuchs vor allem nach der ersten Stunde. Die Anlaufwerte (232 gegen 708
MB nach zehn Sekunden) unterscheiden sich, weil in B das Whisper-Modell früher
geladen wurde — kein Leck. **Urteil erst mit einem Lauf von mindestens vier
Stunden.**

## 2. Event-Loop-Stockungen

| | A (3 h 35) | B (46 min) |
|---|---|---|
| `_loop_stockung_melden` | 8 Warnungen + 9 Fehler | 2 |
| Loop p99 nach dem Anlauf | 17–60 ms | 44–51 ms |

Die schwersten Einzelstellen aus A sind seit W133 aus dem Loop genommen
(Piper-Stimmensuche 4,3 s, Token-Zähler 1,7 s, Upload-Warteschlange). Übrig
bleiben einzelne synchrone Datenbankzugriffe (`get_tracking_priority`,
`_live_users`, `cfgstore.get`, `_set_status`); sie zu verlegen ist riskant,
weil die Reihenfolge der Schreibvorgänge daran hängt (Begründung in W132).

## 3. Verbindungen und Meldungen

| | A | B |
|---|---|---|
| Kick-Chat „verbunden" | 11 975 in 3 h 35 (≈ 1/s) | 251 in 46 min (≈ alle 11 s) |
| CrowdSec-Warnungen | 106 | 3 |
| live-react ohne Ausgabe | 65 | 34 |

Ab W136 versucht der Kick-Chat bei einem Pusher-Code 4000–4099 nur noch alle
15 Minuten (Pusher-Protokoll: „nicht unverändert neu verbinden").

## Offen

- Langlauf (≥ 4 h) nach W136 für das Speicherurteil.
- Ein tracemalloc-Schnappschuss im Betrieb wäre die direkte Antwort auf die
  Frage *was* wächst; das braucht einen Schalter im Bot und kommt nur, falls
  der Langlauf weiter wächst.
