"""nc.memeklip — erkennt meme-würdige Chat-Momente, quellenübergreifend (v4.2-W24).

Erste Welle eines mehrteiligen Vorhabens: ein KI-Klassifikator liest ein
kurzes Fenster aus gemischtem Chat-Text (Kick, TikTok-Kommentare, später
Discord) und entscheidet, ob GERADE ein meme-würdiger Moment läuft — dann
klingelt `clip_moment()`, das schon existiert und bereits nach Discord
postet (`CLIP_DISCORD_UPLOAD`). Zwei weitere Plattform-Wege sind bewusst
NICHT Teil dieser Welle: Kick hat keine öffentliche Clip-Erstellungs-API
(die hiesige `nc/kickapi.py` deckt Chat/Bans/Channels/Kategorien ab — Clips
gibt es dort schlicht nicht), Twitch-Clips entstehen nur aus einer LAUFENDEN
Twitch-Übertragung (kein Datei-Upload, braucht zusätzlich den `clips:edit`-
Scope), und ein YouTube-Video-Upload braucht den `youtube.upload`-Scope
(Re-Autorisierung aller bestehenden Kanäle) sowie ein Quota-Budget (ein
Upload kostet 1600 von 10.000 Tages-Einheiten). Beides sind eigene, spätere
Wellen mit eigener OAuth-Erweiterung.

**Der Klassifikator läuft NICHT über `ai_chat`/`azrael_chat`.** Beide
bevorzugen Claude, sobald ein Anthropic-Key gesetzt ist (v4.0-W65) — genau
das würde bei einem Chat-Poll alle 20s laufend Claude-Budget verbrennen.
Dieser Pfad ruft `nc.freeai.chat()` DIREKT: keylose Basen-Rotation, nie
Claude. Der Bot reicht trotzdem denselben Budget-Deckel (`AZRAEL_MAX_CALLS_MIN`-
Stil) über eine eigene Zeitstempel-Liste durch, damit ein Chat-Sturm nicht
beide KI-Pfade (Moderation UND Meme-Erkennung) gleichzeitig flutet.

**Warum ein Fenster und keine Einzelnachricht:** ein Meme ist ein Chat-
MUSTER (mehrere Leute spammen dasselbe Wort/Emote, eine Reaktion eskaliert),
kein einzelner Satz. Das Fenster sammelt quellmarkierte Zeilen mit
Zeitstempel und liefert nur die noch nicht verfallenen als EIN Textblock —
dieselbe Rolle wie `chat_buf` beim TikTok-Comment-Handler, nur
quellenübergreifend und mit Verfallszeit statt fester Zeilenzahl.
"""

import json
import re

_ZAUN = re.compile(r"^```(?:json)?|```$", re.MULTILINE)

URTEIL_PROMPT = (
    "Du liest einen kurzen Ausschnitt aus einem Livestream-Chat (mehrere "
    "Quellen gemischt, mit [Quelle] markiert). Bewerte NUR: läuft GERADE ein "
    "meme-würdiger Moment — viele spammen dasselbe Wort/Emote, ein Insider-"
    "Witz eskaliert, eine ungewöhnlich starke gemeinsame Reaktion? Antworte "
    'NUR mit JSON: {"meme": <0.0-1.0>, "grund": "<kurz, max 60 Zeichen>"}. '
    "meme=Wahrscheinlichkeit, dass ein Clip JETZT lohnt. Normales Geplauder "
    "ohne Muster ist 0.0-0.2, nicht 0.5."
)

# Ab hier ist ein Fund "meme-wuerdig" — siehe soll_clippen(). Schwelle ist
# bewusst hoch: ein Fehlalarm postet automatisch (CLIP_DISCORD_UPLOAD) und
# ist damit oeffentlich sichtbar, nicht nur ein verschwendeter API-Call.
STANDARD_SCHWELLE = 0.72


def _entzaunen(text):
    return _ZAUN.sub("", (text or "").strip()).strip()


def frage(fenstertext, grenze=1200):
    """Die Nachrichtenliste fuer nc.freeai.chat(). Gekuerzt: ein Chat-Roman
    kostet nur Tokens, aendert am Urteil ueber den JUENGSTEN Moment nichts."""
    return [{"role": "system", "content": URTEIL_PROMPT},
            {"role": "user", "content": (fenstertext or "")[:grenze]}]


def lies_urteil(text):
    """-> {"meme": float, "grund": str} oder None.

    None heisst "keine lesbare Antwort", nicht "kein Meme" — der Aufrufer
    darf ein ausgefallenes Modell nicht als Nein werten, sonst probiert er
    es nie wieder, solange die Base laut freeai.diagnose() eigentlich lebt.
    """
    try:
        d = json.loads(_entzaunen(text))
        wert = float(d.get("meme", 0))
    except Exception:
        return None
    if wert != wert:   # NaN aus kaputtem JSON-Wert ("meme": NaN ist kein gueltiges JSON, aber float() liest "nan")
        return None
    grund = str(d.get("grund") or "").strip()[:60]
    return {"meme": max(0.0, min(1.0, wert)), "grund": grund}


def soll_clippen(urteil, schwelle=STANDARD_SCHWELLE):
    """True nur bei einer LESBAREN Antwort ueber der Schwelle. Ein None-Urteil
    (Modell ausgefallen, kaputtes JSON) ist IMMER False — nie ein Freispruch,
    aber eben auch nie ein Clip."""
    return bool(urteil) and urteil["meme"] >= schwelle


class Fenster:
    """Ring-Puffer quellmarkierter Chat-Zeilen mit Verfallszeit.

    Anders als `chat_buf` (feste Zeilenzahl, EINE Quelle) verfaellt hier nach
    ALTER: eine ruhige Minute soll nicht von einer heissen Sekunde vor zwei
    Minuten mitentschieden werden. `max_eintraege` ist nur ein Hart-Deckel
    gegen unbegrenztes Wachstum bei einem haengengebliebenen Aufrufer.
    """

    def __init__(self, max_eintraege=200):
        self._eintraege = []
        self._max = max_eintraege

    def merken(self, quelle, text, jetzt):
        text = (text or "").strip()
        if not text:
            return
        self._eintraege.append((quelle, text, jetzt))
        if len(self._eintraege) > self._max:
            del self._eintraege[:len(self._eintraege) - self._max]

    def text(self, jetzt, max_alter_s=90):
        """Die noch nicht verfallenen Zeilen, aeltestes zuerst, als EIN Block."""
        return "\n".join(f"[{q}] {t}" for (q, t, ts) in self._eintraege
                         if jetzt - ts <= max_alter_s)

    def leeren(self):
        """Nach einem ausgeloesten Clip: derselbe Hype darf nicht sofort
        einen zweiten Treffer geben, sobald der Cooldown von clip_moment()
        wieder offen ist."""
        self._eintraege.clear()
