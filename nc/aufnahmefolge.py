"""nc.aufnahmefolge — was aus einer beendeten Aufnahme folgt (v4.2-W18).

Die Eskalationsrechnung des Recorders lag an DREI Stellen in bot.py: gesetzt
beim Aufnahme-Ende, zurueckgesetzt beim Offline-Uebergang, durchgesetzt vor dem
naechsten Spawn. Drei Stellen fuer EINEN Zustandsautomaten — und keine davon
war je ausgefuehrt worden, weil sie tief in einer 669-Zeilen-Funktion steckte,
die einen laufenden ffmpeg-Prozess braucht.

Hier rechnet sie, und zwar nur. Kein Prozess, keine Datenbank, keine Uhr aus
dem Modul: die Zeit kommt als Parameter herein, die Register kommen als
Woerterbuecher herein und werden in place fortgeschrieben — dieselben Objekte,
die der Bot und das Brain-Panel lesen. Eine Kopie, und der Zaehler stuende in
einem Dict, waehrend die Durchsetzung das andere liest.

**Zwei Uhren, und das ist Absicht:**

* Der 403-Zweig rechnet in `time.time()` (Wanduhr). Sein Cooldown ueberlebt
  einen Neustart des Bots nicht, soll er auch nicht — nach einem Neustart ist
  ein frischer nativer Versuch richtig.
* Der Stream-Tod-Zweig rechnet in `time.monotonic()`. Er faellig-stellt den
  Worker-Tick (`_NEXT_CHECK_AT`), und der laeuft monoton. Wer hier die Uhren
  vertauscht, setzt eine Sperre, die entweder sofort abgelaufen oder 57 Jahre
  gueltig ist — je nach Richtung.

Die Funktionen bekommen die Uhr deshalb GETRENNT uebergeben und mischen sie
nie selbst.
"""

# Kategorien, bei denen eine kleine Datei bedeutet: es sind keine echten Daten
# geflossen. "stall_killed" ist dabei der haeufigste Fall — der Streamer hat
# "Live pausiert" gedrueckt, TikTok meldet weiter live, der HLS-Pull gibt 404.
TOTE_KATEGORIEN = ("stall_killed", "stream_dead", "codec_header_fail",
                   "hevc_unsupported")

# Backoff-Stufen bei Stream-Tod: 5min, 10min, 20min, 30min (Deckel).
TOT_BASIS_S = 300
TOT_MAX_S = 1800

# Frueher Abbruch: 10, 20, 40, 80, 160s. Der Deckel liegt bei 160 und nicht
# hoeher, weil danach ohnehin der regulaere Live-Check (30-60s) uebernimmt —
# ein groesserer Deckel wuerde die Aufnahme nur laenger verhindern.
FRUEH_BASIS_S = 10
FRUEH_MAX_S = 160

# Hoechstens eine "im Backoff"-Zeile alle fuenf Minuten. Ohne das schreibt der
# Poll-Zyklus sie alle ~20 Sekunden, und das Fehlerlog ist unlesbar.
MELDE_ABSTAND_S = 300


def daten_geflossen(kategorie, groesse, min_bytes):
    """False = die Aufnahme hat nichts Echtes geliefert.

    Beides muss zutreffen: eine Kategorie aus TOTE_KATEGORIEN UND eine Datei
    unter der Schwelle. Eine grosse Datei mit stall_killed ist ein echter,
    abgeschnittener Mitschnitt — den als "tot" zu zaehlen wuerde einen
    Streamer in den Backoff schicken, der gerade sendet.
    """
    return not (kategorie in TOTE_KATEGORIEN and groesse < min_bytes)


def nach_403(streak, sperre, backoff, user, jetzt, *, hits, cooldown_s,
             backoff_an, basis_s, max_s):
    """Ein 403 gezaehlt. Ab `hits` in Folge wird yt-dlp erzwungen.

    `jetzt` ist WANDUHR-Zeit. Rueckgabe:
        {"streak": n, "erzwingt_ytdlp": bool, "backoff_s": int|None}
    """
    n = streak.get(user, 0) + 1
    streak[user] = n
    if n < hits:
        return {"streak": n, "erzwingt_ytdlp": False, "backoff_s": None}
    sperre[user] = jetzt + cooldown_s
    bo = None
    if backoff_an:
        # Die Drosselung setzt bei der Schwelle mit der Basis ein und
        # verdoppelt je weiterem Treffer. n == hits ergibt 2**0 — ohne das
        # -hits waere der erste erzwungene Wechsel schon bei 2**hits, also
        # bei Standardwerten 4x zu lang.
        bo = min(max_s, basis_s * (2 ** (n - hits)))
        backoff[user] = jetzt + bo
    return {"streak": n, "erzwingt_ytdlp": True, "backoff_s": bo}


def nach_totem_versuch(streak, sperre, faellig, tid, jetzt_mono, *,
                       schwelle, kurz_s):
    """Eine Aufnahme ohne echte Daten. Zaehlt und setzt die Sperre.

    `jetzt_mono` ist MONOTONE Zeit. Unterhalb der Schwelle wird nur ein kurzer
    Cooldown gesetzt (B62) — ohne ihn startet der Sofort-Retry nach ~50s ein
    ffmpeg, das dieselbe tote URL zieht. Rueckgabe:
        {"streak": n, "eskaliert": bool, "sekunden": int}
    """
    n = streak.get(tid, 0) + 1
    streak[tid] = n
    if n >= schwelle:
        sek = min(TOT_BASIS_S * (2 ** (n - schwelle)), TOT_MAX_S)
        eskaliert = True
    else:
        sek = kurz_s
        eskaliert = False
    if sek > 0:
        bis = jetzt_mono + sek
        sperre[tid] = bis
        # Auch den Worker-Tick verschieben: sonst prueft der Live-Check
        # weiter im 20s-Takt und die Sperre bremst nur den Spawn, nicht die
        # Last.
        faellig[tid] = bis
    return {"streak": n, "eskaliert": eskaliert, "sekunden": sek}


def nach_frueher_trennung(retry, tid, *, max_versuche):
    """Aufnahme brach in unter 30 Sekunden ab. Zaehlt und plant den Neuversuch.

    Rueckgabe {"anzahl": n, "wartet": sekunden|None}. `wartet is None` heisst:
    Hoechstzahl erreicht, der Zaehler ist zurueckgesetzt und der regulaere
    Poll uebernimmt wieder. Ohne dieses Zuruecksetzen bliebe der Zaehler oben
    und die naechste fruehe Trennung bekaeme sofort den laengsten Backoff.
    """
    n = retry.get(tid, 0) + 1
    retry[tid] = n
    if n > max_versuche:
        retry.pop(tid, None)
        return {"anzahl": n, "wartet": None}
    return {"anzahl": n, "wartet": min(FRUEH_BASIS_S * (2 ** (n - 1)), FRUEH_MAX_S)}


def sperre_rest(sperre, key, jetzt):
    """Restsekunden einer Sperre, 0 = frei. Rundet auf, nie auf 0 ab:

    ein `int()` haette 0.4 Restsekunden als "frei" gemeldet, obwohl die
    Sperre noch steht — die Meldung haette dann eine Sperre verschwiegen,
    die den Spawn trotzdem verhindert.
    """
    bis = sperre.get(key) or 0
    if not bis or jetzt >= bis:
        return 0
    return max(1, int(bis - jetzt + 0.999))


def melden_erlaubt(zuletzt, key, jetzt, abstand_s=MELDE_ABSTAND_S):
    """True und merkt sich den Zeitpunkt. Entspammt die Backoff-Meldung."""
    if jetzt - (zuletzt.get(key) or 0) <= abstand_s:
        return False
    zuletzt[key] = jetzt
    return True


def aufnahme_geglueckt(streak403, backoff, meldung, totstreak, totsperre,
                       frueh, user, tid):
    """Eine Aufnahme hat Daten geliefert — alle Fehlerzaehler dieses Users weg.

    Ein einziger Einstiegspunkt statt sechs pop()-Zeilen im Monolithen: die
    Reset-Menge stand dort dreimal, und zweimal fehlte einer der Zaehler.
    """
    for reg, k in ((streak403, user), (backoff, user), (meldung, user),
                   (totstreak, tid), (totsperre, tid), (frueh, tid)):
        reg.pop(k, None)


def sitzung_zuende(streak403, backoff, meldung, totstreak, totsperre,
                   user, tid):
    """TikTok meldet offline: Session-Ende, saubere Bilanz fuer die naechste.

    Bewusst OHNE den Frueh-Trennungs-Zaehler: der haengt an der Netzqualitaet
    zur Verbindung, nicht an der Sitzung. Rueckgabe True, wenn ueberhaupt ein
    Stream-Tod-Zaehler stand — der Bot loggt nur dann.
    """
    stand = bool(totstreak.get(tid) or totsperre.get(tid))
    for reg, k in ((streak403, user), (backoff, user), (meldung, user),
                   (totstreak, tid), (totsperre, tid)):
        reg.pop(k, None)
    return stand
