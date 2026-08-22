"""nc.version — zentrale Versions- und Changelog-Quelle (bot-frei).

Eine einzige Wahrheit für die Versionsanzeige (Dashboard-Footer, /api/version,
„Was ist neu"-Panel). Reine Daten + kleine Helfer, voll testbar.
"""

VERSION = "4.0"
CODENAME = "Restream Control Room"
RELEASE = "2026.08"

# Meilenstein-Changelog, neueste Version zuerst. highlights = kurze, ehrliche
# Stichpunkte dessen, was die Version bringt.
CHANGELOG = [
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
