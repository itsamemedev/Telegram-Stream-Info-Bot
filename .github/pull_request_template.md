<!--
Danke für den Beitrag. Bitte fülle die Abschnitte aus — vor allem die
Prüfkette. Sie ist keine Formalie: Deploy geht direkt gegen Produktion.
-->

## Was sich ändert

<!-- Knapp, im Imperativ. Eine Zeile reicht, wenn sie präzise ist. -->

## Warum

<!-- Bevorzugt mit dem beobachteten Symptom: was ging kaputt, was war unsichtbar,
     was war umständlich? -->

## Art der Änderung

- [ ] Fehlerbehebung
- [ ] Neue Funktion
- [ ] Umbau ohne Verhaltensänderung
- [ ] Dokumentation
- [ ] Betrieb / CI / Werkzeuge

## Prüfkette

<!-- Ergebnisse eintragen, nicht nur abhaken. -->

- [ ] `python3 -m py_compile <geänderte .py>`
- [ ] `python3 -m pyflakes <geänderte .py>` — 0 Befunde
- [ ] `python3 -m ruff check --select F,E9,B --ignore B905 <geänderte .py>`
- [ ] `python3 tools/ncpatch.py check`
- [ ] `python3 test_nc_modules.py`
- [ ] `python3 test_restream.py`
- [ ] `python3 test_smoke.py` <!-- braucht den vollen Laufzeitstack, sonst begründen -->

```
Ausgabe hier einfügen
```

## Regeln eingehalten

- [ ] `nc/*` und `brain/*` importieren **nicht** aus `bot_v37`
- [ ] Kein `except: pass` in Dauerläufern — `_loop_fehler(name, exc)` benutzt
- [ ] Konfiguration wird als **Funktion** gelesen, nicht als Modul-Konstante
- [ ] Neue Funktionalität ist per Env-Schalter abschaltbar, Default ist sinnvoll
- [ ] Kommentare und Ausgaben auf Deutsch, sie erklären **warum**

## Mitgeneriertes

- [ ] `.claude/INDEX.md` neu gebaut (`python3 tools/ncpatch.py map`) — falls Routen,
      Slash-Commands oder Top-Level-Funktionen betroffen sind
- [ ] `.env.example` neu erzeugt (`python3 tools/gen_env_example.py`) — falls neue
      Konfigurationsvariablen dazugekommen sind
- [ ] `CHANGELOG.md` ergänzt

## Rückrollbarkeit

<!-- Ist die Änderung einzeln verifizierbar und rückrollbar? Falls ein Schema-
     wechsel oder eine Migration dabei ist: wie kommt man zurück? -->

## Verwandte Issues

<!-- Fixes #123 -->

---

- [ ] Ich habe geprüft, dass **keine Geheimnisse** im Diff stehen (`git status`,
      `.env`, Cookies, Tokens, Stream-Keys)
- [ ] Ich stelle meinen Beitrag unter die **GPL-3.0-or-later**
