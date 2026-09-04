"""nc.version — zentrale Versions- und Changelog-Quelle (bot-frei).

Eine einzige Wahrheit für die Versionsanzeige (Dashboard-Footer, /api/version,
„Was ist neu"-Panel). Reine Daten + kleine Helfer, voll testbar.
"""

VERSION = "4.2"
CODENAME = "Zerlegter Kern"
RELEASE = "2026.09"


def build_stamp():
    """Die EINE Vorgabe für den Build-Stempel.

    v4.2: vorher stand die Zeichenkette "2026.08 · v4.1" wörtlich an vier
    Stellen — bot.py, nc/routes/brain.py und zweimal im Footer von
    dashboard.html. Genau deshalb zeigte das Deck im September noch August an:
    wer nc/version.py hochzählt, bewegt den Footer nicht mit. Ein Modul, das
    sich "eine einzige Wahrheit" nennt, darf keine Kopien haben.
    """
    return f"{RELEASE} · v{VERSION}"

# Meilenstein-Changelog, neueste Version zuerst. highlights = kurze, ehrliche
# Stichpunkte dessen, was die Version bringt.
CHANGELOG = [
    {
        "version": "4.2",
        "date": "2026-09",
        "title": "Zerlegter Kern",
        "highlights": [
            "Das Dashboard spricht wirklich Englisch: die Abdeckung stieg von 18 % auf 89 % — vorher meldete die Prüfung „0 fehlend“, weil sie nur zählte, was der Sammler überhaupt eingesammelt hatte",
            "Sieben weitere Routengruppen aus dem Monolithen gelöst — Wartung, Abwehr, Auskunft, Beobachtung, Systemlage — ohne einen einzigen neuen Kontext-Eintrag",
            "Kein Dauerläufer blockiert mehr die Ereignisschleife: die Stillstände von 30 bis 68 Sekunden sind weg, Datenbankzugriffe laufen neben der Schleife",
            "Fehlermeldungen nach außen tragen keine Dateipfade, Zugangsdaten oder Stream-Schlüssel mehr — der Wortlaut bleibt im Log",
            "Ein offenes Dashboard ohne Token und PIN meldet sich alle sechs Stunden auf Fehler-Ebene, nicht nur einmal beim Start",
            "Der Rauchtest führt bot.py in der CI wirklich aus — vorher stand er in der Pflichtliste, lief aber auf keiner Maschine automatisch",
            "Vorschläge des Evolutions-Kerns lassen sich gesammelt übernehmen oder verwerfen",
        ],
    },
    {
        "version": "4.1",
        "date": "2026-08",
        "title": "Öffentliche Stimme",
        "highlights": [
            "News auf der Website sind ausführliche Meldungen statt einer Statuszeile: Anreißer, Kennzahlen, Fließtext in Absätzen, Detailliste und Themen",
            "Der News-Agent liefert dafür ein Wochenbild — Sendungen und aktive Tage der letzten sieben Tage, eingerichtete Sende-Ziele, Moderations-Eingriffe, Chat-Antworten und Wissenszuwachs",
            "Kennzahlen und Detailpunkte stammen immer aus echten Fakten; die KI formuliert nur den Fließtext",
            "Website rendert die neuen Felder und bleibt für alte Einträge ohne sie fehlerfrei",
            "Dashboard-Vorschau zeigt vor dem Veröffentlichen, welche Zahlen nach außen gehen",
            "Öffentliche Texte in korrektem Deutsch statt in ae/oe/ue-Umschrift",
        ],
    },
    {
        "version": "4.0",
        "date": "2026-08",
        "title": "Multi-Plattform-Moderation & offener Kern",
        "highlights": [
            "Moderator überall: KI-Moderation auf Kick, Twitch und YouTube über eine geteilte Heuristik",
            "AZRAEL antwortet in alle drei Chats — adressiert an genau einen User im Restream",
            "Kick User-OAuth: Stream-Titel und Kategorie direkt aus dem Dashboard setzen",
            "News- & Marketing-Agent: eigene Kanäle und Website automatisch bewerben",
            "Sicherer Restream-Test-Push — Ziel prüfen ohne Broadcast-Risiko",
            "Modularer Kern: Schema, Moderations-Heuristik, Selbstanalyse und Stimmwahl in eigene Module gelöst",
            "Sentinel-Flotte: zwölf Wächter-Agenten mit Telegram-Alarmen",
        ],
    },
    {
        "version": "3.7",
        "date": "2026-07",
        "title": "Kontrollraum-Fundament",
        "highlights": [
            "Dreistufiger Recorder-Fallback, adaptives Polling, Anti-Flap",
            "Multi-Plattform-Restream (Kick / Twitch / YouTube)",
            "Wissensgraph-Gehirn mit Live-Visualisierung",
            "Abo-Stream-Erkennung mit eigenen Benachrichtigungen",
        ],
    },
]


def current():
    """Kompakter Versions-Datensatz."""
    return {"version": VERSION, "codename": CODENAME, "release": RELEASE}


def summary_line():
    return f"NIGHTCRAWLER v{VERSION} · {CODENAME}"


def latest():
    """Der neueste Changelog-Eintrag (die aktuelle Version)."""
    return CHANGELOG[0]


def changelog():
    return CHANGELOG
