"""nc.livefolge — was aus einem Live-Signal folgt (v4.2-W20).

Drei Entscheidungen aus `_handle_single_tracking`, die reine Rechnung sind und
trotzdem in einer 380-Zeilen-Funktion steckten, die eine Datenbank, einen
Scraper und einen Recorder braucht — also hier nie ausgefuehrt wurde:

1. **Ist "offline" wirklich offline?** TikTok liefert Aussetzer. Ein einzelner
   verpasster Live-Ping darf keine OFFLINE-Meldung ausloesen und keine
   laufende Aufnahme beenden. Zwei Schwellen muessen BEIDE fallen: genug
   aufeinanderfolgende Beobachtungen (Debounce) UND lange genug offline
   (Pause-Grace). Faellt nur eine, ist es eine Pause — der Streamer kommt
   zurueck, und die Aufnahme laeuft ohne neue LIVE-Meldung weiter.
2. **Ist gerade Ruhezeit?** Ein Fenster ueber Mitternacht (22-7) ist die
   Standardfalle: `start <= h < ende` ist dort immer falsch.
3. **Wann wird das naechste Mal geschaut?** Der Grundabstand nach Status.

Keine Uhr aus dem Modul: die Zeit kommt als Parameter. Die Register kommen
als Woerterbuecher und werden in place fortgeschrieben — dieselben Objekte,
die der Bot und das Brain-Panel lesen.

**Die Uhr ist MONOTON.** Die Pause-Grace misst eine Dauer, keinen Zeitpunkt.
Mit der Wanduhr haette eine Zeitumstellung oder ein NTP-Sprung mitten in
einem Stream entweder sofort "offline" gemeldet oder eine Stunde lang gar
nicht — dieselbe Falle wie beim Stream-Tod-Backoff (W18).
"""


def live_gesehen(zaehler, seit, tid):
    """Der Streamer ist (wieder) da: beide Offline-Register fuer ihn raeumen.

    Rueckgabe True, wenn ueberhaupt etwas anhaengig war — der Bot loggt nur
    dann. Ohne das Zuruecksetzen zaehlte ein Aussetzer von vor Stunden noch
    auf die Debounce-Schwelle von heute Abend.

    **VERHALTENSKORREKTUR (v4.2-W20).** Im Monolithen stand hier

        if _PENDING_OFFLINE_COUNT.pop(tid, None) or _PENDING_OFFLINE_SINCE.pop(tid, None):

    — ein `or` mit Kurzschluss. War ein Zaehler gesetzt (der Normalfall,
    sobald ueberhaupt ein Aussetzer beobachtet wurde), wurde der ZWEITE pop
    nie ausgefuehrt: der Startzeitpunkt der Offline-Phase blieb stehen.

    Folge: beim naechsten Aussetzer misst die Pause-Grace ab dem ERSTEN
    Aussetzer der Sitzung, nicht ab jetzt. `offline_for` ist dann sofort
    riesig, die Grace-Schwelle faellt augenblicklich, und es entscheidet
    allein der Debounce-Zaehler. Genau der Schutz, fuer den es die Grace
    gibt — "Live pausiert" nicht als Stream-Ende zu lesen — war ab dem
    zweiten Aussetzer einer Sitzung wirkungslos.

    Die vier anderen Reset-Stellen im Monolithen raeumen beide Register in
    zwei getrennten Zeilen; nur diese eine nicht. Hier wird es getrennt
    ausgewertet, damit der Kurzschluss nicht wiederkommen kann.
    """
    war_zaehler = zaehler.pop(tid, None)
    war_seit = seit.pop(tid, None)
    return bool(war_zaehler or war_seit)


def offline_bestaetigt(zaehler, seit, tid, jetzt_mono, *, debounce, grace_s):
    """Eine Offline-Beobachtung. Zaehlt und entscheidet, ob es eine echte
    Transition ist.

    `jetzt_mono` ist MONOTONE Zeit (siehe Modul-Text). Rueckgabe:
        {"pending": n, "offline_for": sekunden, "bestaetigt": bool}

    Bei `bestaetigt` sind beide Register geraeumt: der naechste Offline-Lauf
    beginnt sauber bei 1. Bleiben sie stehen, waere die naechste Sitzung
    sofort "bestaetigt offline", noch bevor sie richtig begonnen hat.
    """
    n = zaehler.get(tid, 0) + 1
    zaehler[tid] = n
    beginn = seit.get(tid)
    if beginn is None:
        beginn = jetzt_mono
        seit[tid] = beginn
    dauer = jetzt_mono - beginn
    # BEIDE Schwellen. Ein `or` haette gereicht, um die haeufigste Stoerung
    # durchzulassen: zwei schnelle Ticks hintereinander (Debounce erfuellt,
    # Grace nicht) sind genau das Bild eines TikTok-Aussetzers.
    if n < debounce or dauer < grace_s:
        return {"pending": n, "offline_for": dauer, "bestaetigt": False}
    zaehler.pop(tid, None)
    seit.pop(tid, None)
    return {"pending": n, "offline_for": dauer, "bestaetigt": True}


def ruhezeit(stunde, start, ende):
    """True, wenn `stunde` im Ruhefenster liegt.

    `start == ende` schaltet das Fenster AB — sonst waere "0 bis 0" entweder
    keine oder eine volle Ruhe, und beide Lesarten hat schon jemand gemeint.
    Ist `ende` kleiner als `start`, laeuft das Fenster ueber Mitternacht
    (22-7): der naive Vergleich `start <= h < ende` ist dort IMMER falsch,
    und die Ruhezeit haette schlicht nicht existiert.
    """
    if start == ende:
        return False
    if start < ende:
        return start <= stunde < ende
    return stunde >= start or stunde < ende


def poll_abstand(status, war_live, intervalle):
    """Der Grund-Abstand bis zur naechsten Pruefung, in Sekunden.

    Der Sonderfall ist `just_went_offline`: direkt nach einem Live-Ende wird
    kuerzer nachgeschaut, weil genau dann die Unterscheidung zwischen Pause
    und echtem Ende faellt. Ein unbekannter Status ist NICHT offline — er
    bedeutet, dass die Abfrage selbst nicht durchkam, und bekommt sein
    eigenes Intervall.

    Was hier herauskommt, darf von Prioritaet und Brain-Hinweisen nur noch
    VERKUERZT werden, nie verlaengert (X3/M5). Diese Richtung ist die
    eigentliche Zusicherung: ein Hinweis, der verlaengern darf, kann ein
    Tracking still einschlafen lassen.
    """
    if status == "live":
        return intervalle["live"]
    if status == "offline":
        return intervalle["just_went_offline"] if war_live else intervalle["offline"]
    return intervalle["unknown"]
