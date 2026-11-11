"""nc.uploadschlange — wann ein aufgeschobener Upload fertig ist (rein, bot-frei).

v4.2-W175. Die Warteschlange `pending_uploads.json` (bot.py,
`_upload_window_loop`) hat bis hier jeden Eintrag nach EINEM Versuch
entfernt: `split_and_send_video` wirft nie — jeder Fehlschlag (Netz, toter
Chat, Split gescheitert) endet ordentlich mit `return`, und der Aufrufer
hielt das fuer Erfolg. Ein Upload, der nachts im Fenster an einem Timeout
scheiterte, war damit still verloren; der `except`-Zweig mit „NICHT
entfernen → nächster Durchlauf versucht erneut" lief nie.

Entschieden wird jetzt am Ergebnis, das `split_and_send_video` seit W168 in
ein mitgegebenes `ergebnis`-Woerterbuch zaehlt: mindestens ein Teil
gesendet und kein Fehler. Sonst bleibt der Eintrag mit wachsender Pause
liegen und wird nach `MAX_VERSUCHE` laut aufgegeben — ein Chat, den es
nicht mehr gibt, darf die Schlange nicht fuer immer belegen.
"""

MAX_VERSUCHE = 5
PAUSE_S = 600.0          # 10 min nach dem ersten Fehlschlag, dann verdoppelt
PAUSE_MAX_S = 6 * 3600.0


def angekommen(ergebnis) -> bool:
    """Hat der Versand die Datei vollstaendig gesendet?

    Mindestens ein Teil und kein Fehler. Ein leeres Ergebnis heisst, dass gar
    nichts gesendet wurde (toter Chat, Split gescheitert, Platte voll) — und
    das ist KEIN Erfolg, sonst verschwindet der Eintrag mit der einzigen
    Erinnerung daran, dass die Aufnahme noch raus muss."""
    return bool(ergebnis) and ergebnis.get("gesendet", 0) > 0 and not ergebnis.get("fehler", 0)


def faellig(eintrag, jetzt: float) -> bool:
    """Ist der Eintrag jetzt dran? Ohne Zeitstempel (Bestand vor W175): ja."""
    try:
        return float(eintrag.get("naechster_versuch") or 0) <= jetzt
    except (TypeError, ValueError):
        return True


def pause_s(versuche: int) -> float:
    """Pause nach dem n-ten Fehlschlag: 10, 20, 40 … Minuten, hoechstens 6 h."""
    return min(PAUSE_MAX_S, PAUSE_S * (2 ** max(0, int(versuche) - 1)))


def nach_versuch(eintrag, ergebnis, jetzt: float, max_versuche: int = MAX_VERSUCHE):
    """-> (lage, eintrag_neu) mit lage in "fertig", "wieder", "aufgeben".

    `eintrag_neu` ist eine Kopie mit hochgezaehltem `versuche`, dem Grund des
    letzten Fehlschlags und dem Zeitpunkt des naechsten Versuchs — der
    Aufrufer schreibt sie an die Stelle des alten Eintrags."""
    if angekommen(ergebnis):
        return "fertig", dict(eintrag)
    neu = dict(eintrag)
    neu["versuche"] = int(eintrag.get("versuche") or 0) + 1
    neu["letzter_fehler"] = str((ergebnis or {}).get("grund")
                                or ("nichts gesendet" if not (ergebnis or {}).get("gesendet")
                                    else "%s Teil(e) gescheitert" % (ergebnis or {}).get("fehler")))[:300]
    if neu["versuche"] >= max_versuche:
        return "aufgeben", neu
    neu["naechster_versuch"] = jetzt + pause_s(neu["versuche"])
    return "wieder", neu


def gleicher(a, b) -> bool:
    """Derselbe Eintrag? Datei, Ziel und Zeitpunkt des Einreihens — dieselben
    drei Felder, an denen `_upload_queue_remove` ihn seit jeher erkennt."""
    return (a.get("file") == b.get("file") and a.get("chat_id") == b.get("chat_id")
            and a.get("ziel") == b.get("ziel") and a.get("queued_at") == b.get("queued_at"))
