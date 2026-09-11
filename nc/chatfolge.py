"""nc.chatfolge — wie oft der TikTok-Chat neu aufgebaut werden darf (v4.2-W47).

Die Rechnung stand seit W37 im Restream-Chat-Waechter, und zwar nur dort. Der
Live-Reaction-Worker hat einen ZWEITEN Listener auf denselben TikTok-Chat —
und der hatte gar keine: er baute nicht neu auf, sondern beendete sich, worauf
die Engine ihn acht Sekunden spaeter neu startete. Ein Neuaufbau alle acht
Sekunden ist schneller als das Flattern, das W37 abgestellt hat.

Zwei Kopien derselben Regel waeren der naechste Fehler gewesen (eine wird
gepflegt, die andere nicht — dasselbe Bild wie beim Build-Stempel in v4.2).
Deshalb liegt sie jetzt hier und wird von BEIDEN benutzt.

Warum es die Regel ueberhaupt gibt, aus dem Log vom 10.09.: jede Chat-Sitzung
hielt 13-17 Sekunden, lag damit ueber der damaligen Gesundheits-Grenze von 10
Sekunden und galt als gesund — der Backoff wurde also jedes Mal auf null
zurueckgesetzt. 122 Listener-Starts in 85 Minuten, bis die Sign-API mit HTTP
500 dichtmachte. Der schnelle Reconnect war die URSACHE des Rate-Limits, nicht
die Reaktion darauf.

Rein rechnend: keine Uhr, kein Schlaf, kein Logging. Die Zeit kommt als
Parameter herein, damit sich ein Stunden-Verlauf in Millisekunden pruefen
laesst.
"""
from __future__ import annotations

# Kuerzer als das gilt als abgerissen, nicht als gesunde Rotation. TikTok
# dreht seine WebSocket-Verbindungen regelmaessig durch; 60 s trennt das von
# einem echten Abbruch. (W37: war 10 s und damit wirkungslos.)
FLAP_S = 60

# Mehr als so viele Neuaufbauten im Fenster sind Flattern — unabhaengig
# davon, wie lang die einzelne Sitzung hielt. Genau diese Unabhaengigkeit
# fehlte vor W37: wer die Gesundheits-Grenze knapp ueberbot, kam durch.
CHURN_MAX = 6
CHURN_WINDOW_S = 600

BACKOFF_MAX_S = 300


def entscheide(reconnects, jetzt, dauer, backoff, *,
               churn_max=None, fenster_s=None, flap_s=None, max_s=None):
    """Wie geht es nach einem getrennten Chat weiter?

    `reconnects` ist die Liste der bisherigen Neuaufbau-Zeitpunkte
    (monotonic). `dauer` ist die Laenge der gerade beendeten Sitzung,
    `backoff` der bisherige Wert.

    Rueckgabe: (reconnects_neu, backoff_neu, grund). `grund` ist
    "flattert", "gesund" oder "kurz" — der Aufrufer entscheidet daraus, auf
    welcher Ebene er loggt und ob er schlaeft.

    Die Liste wird NEU zurueckgegeben und nicht an Ort und Stelle geaendert:
    zwei Aufrufer teilen sich diese Funktion, und einer von beiden haelt seine
    Liste in einer Closure. Eine Funktion, die mal mutiert und mal nicht, ist
    genau die Sorte Falle, die man erst im Betrieb bemerkt.
    """
    g_max = CHURN_MAX if churn_max is None else churn_max
    g_fenster = CHURN_WINDOW_S if fenster_s is None else fenster_s
    g_flap = FLAP_S if flap_s is None else flap_s
    g_deckel = BACKOFF_MAX_S if max_s is None else max_s

    neu = [t for t in list(reconnects or []) if jetzt - t <= g_fenster]
    neu.append(jetzt)

    if len(neu) >= g_max:
        return neu, min(max(5, (backoff or 0) * 2), g_deckel), "flattert"
    if (dauer or 0) >= g_flap:
        # Gesunde Rotation: sofort wieder verbinden, Backoff zurueck auf null.
        return neu, 0, "gesund"
    return neu, min(max(5, (backoff or 0) * 2), g_deckel), "kurz"
