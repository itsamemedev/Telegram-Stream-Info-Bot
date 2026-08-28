"""nc.version — zentrale Versions- und Changelog-Quelle (bot-frei).

Eine einzige Wahrheit für die Versionsanzeige (Dashboard-Footer, /api/version,
„Was ist neu"-Panel). Reine Daten + kleine Helfer, voll testbar.
"""

VERSION = "4.1"
CODENAME = "Öffentliche Stimme"
RELEASE = "2026.08"

# Meilenstein-Changelog, neueste Version zuerst. highlights = kurze, ehrliche
# Stichpunkte dessen, was die Version bringt.
CHANGELOG = [
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
