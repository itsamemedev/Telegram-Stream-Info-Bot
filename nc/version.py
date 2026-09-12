"""nc.version — zentrale Versions- und Changelog-Quelle (bot-frei).

Eine einzige Wahrheit für die Versionsanzeige (Dashboard-Footer, /api/version,
„Was ist neu"-Panel). Reine Daten + kleine Helfer, voll testbar.
"""

VERSION = "4.3"
CODENAME = "Freie Sicht"
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
        "version": "4.3",
        "date": "2026-09",
        "title": "Freie Sicht",
        # v4.3 ist die Fassung, in der der Bot den Stream ueberhaupt erst
        # zuverlaessig FINDET und das Sendebild wieder LESBAR ist. 4.2 hatte
        # den Monolithen zerlegt — an der Oberflaeche sah der Betreiber davon
        # nichts. Hier sieht er es: zwei von drei Live-Erkennungen liefen ins
        # Leere, der Chat lag unter dem Avatar, die Notbremse trat aufs Gas.
        "highlights": [
            "Ein Stream ist wieder EIN Stream: die sechs bis zehn Dateien, in die ein dreistündiger Live-Auftritt zerfällt (Ablauf der signierten TikTok-URL alle ~30 Minuten, dazu je eine nach 403 oder Abriss), tragen jetzt eine gemeinsame Sitzungs-Kennung mit Start- und Endzeit — das Deck zeigt Abdeckung und die echten Nahtlücken, und auf Knopfdruck werden die Segmente ohne Neukodierung zu einer Datei zusammengefügt",
            "Die Live-Ankündigung nach Discord kommt wieder einmal pro Stream statt einmal pro Reparatur-Neustart — und sie trägt den Namen und die Rolle aus der Konfiguration, nicht mehr den danebenstehenden Kommentar",
            "Der Audio-Abgriff der Live-Reaktion sagt jetzt, warum er gestorben ist: er starb im Betrieb 57 Mal je eine Sekunde nach dem Start, warf den Grund aber jedes Mal weg — AZRAEL reagierte deshalb auf den gesendeten TikTok-Stream kein einziges Mal, sondern nur noch auf die Plattform-Chats",
            "AZRAELs Live-Reaktion bleibt am Stream: der Worker starb im Betrieb alle vier Sekunden, weil er seinen TikTok-Chat ohne laufenden Audio-Abgriff gar nicht neu verbinden konnte — und warf bei jedem Ende sein Gedächtnis über den Stream weg. Statt 328 Verbindungsversuchen pro Stunde sind es jetzt 17",
            "Kein Wiederholungs-Sturm mehr gegen Kanäle, die gar nicht senden: der Bot las yt-dlps „The channel is not currently live“ als frühen Abriss und versuchte es fünfmal erneut — und das Sendebild-Overlay fällt nicht mehr ganz aus, wenn die eingestellte Schrift fehlt, sondern nimmt eine Ersatzschrift",
            "Die Notbremse gegen Encode-Rückstand trat bisher aufs Gas: ihre erste Stufe schaltete auf ein LANGSAMERES x264-Preset, wodurch der Rückstand wuchs, bis auf der höchsten Stufe das ganze Sendebild fiel — Chat und Avatar gleich mit. Der Avatar hängt jetzt nicht mehr an der Schriftdatei, und ein leeres Anthropic-Guthaben wird als das gemeldet, was es ist, statt als Programmierfehler",
            "Der Avatar bleibt im Sendebild, auch wenn die Notbremse den eingebrannten Text abwirft — und eine Zeile im Log nennt bei jedem Start, ob Text und Avatar an sind und welche Bedingung sonst fehlt",
            "Zwei von drei Live-Erkennungen liefen bisher ohne Stream-URL weiter: die TikTok-API meldet einer Server-IP zwar „sendet“, rückt die Adresse aber nicht heraus — der Bot fragte den einzigen Weg, der sie noch liefert, ausgerechnet in diesem Fall nicht mehr ab und schickte den Recorder blind los",
            "Und der so gefundene Zugang wird nicht mehr verworfen, wenn er in der stabileren von zwei Formen kommt: die durchgehende Verbindung fiel durch die Prüfung, die nur die segmentierte kannte — dabei ist gerade die Kette signierter Segmente die, die im Betrieb abreißt",
            "AZRAEL steht nicht mehr da wie ein Standbild mit zuckendem Mund: Kopf, Hand und Schwert bewegen sich jetzt einzeln — die Klinge dreht um den Griff in der Faust statt um den Unterarm, und der Kopf neigt sich und hebt sich, ohne dass die Kapuze an der Schulter aufreißt",
            "Der Chat steht im Sendebild wieder vorn: der Avatar lag über der halben rechten Spalte, und die Zeilen liefen zusätzlich rechts aus dem Bild, weil die Umbruchbreite eine feste Zahl für eine Schrift mit fester Zeichenbreite war — die Schrift ist aber proportional. Beides rechnet jetzt aus der Panel-Geometrie",
            "AZRAELs Ohr war aus demselben Grund taub wie der Recorder blind: ohne Stream-URL kein Audio-Abgriff, ohne Abgriff kein Transkript — gemeldet hat das Log davon nur „audio=False“, ein Wort für drei mögliche Ursachen. Jetzt nennt es die Ursache und meldet sie als Warnung statt als Beiwerk",
            "Aufnahme-Sitzungen haben endlich eine Oberfläche: die Funktion, die einen zerstückelten Stream auf Knopfdruck zu einer Datei zusammenfügt, gab es seit W44 nur als Schnittstelle — der versprochene Knopf fehlte. Jetzt zeigt die Betrieb-Ansicht je Sitzung Segmente, Nahtlücken und Abdeckung, und fügt auf Klick zusammen",
            "Auf YouTube gab es für denselben Verstoß sofort eine Auszeit, während Kick und Twitch erst verwarnen — die Moderation läuft auf allen drei Plattformen, nur dieser eine Schritt fehlte dort",
        ],
    },
    {
        "version": "4.2",
        "date": "2026-09",
        "title": "Zerlegter Kern",
        # Die Liste wandert mit den Wellen mit. Sie stand bis v4.2-W38 auf dem
        # Stand von W13 — Footer und „Was ist neu"-Panel lesen von hier, also
        # zeigte das Deck einen Funktionsstand, den es seit zwanzig Wellen nicht
        # mehr gab. Verwandte Wellen stehen bewusst in EINEM Stichpunkt: eine
        # Liste mit dreissig Zeilen liest niemand mehr durch.
        "highlights": [
            "Der Monolith ist zerlegt: rund 2.900 Zeilen weniger in bot.py — der gesamte Discord-Teil mit seinen 45 Slash-Commands und der Versandweg der Aufnahmen nach Telegram stehen in eigenen Dateien, ohne einen einzigen Rückgriff auf bot.py",
            "Sieben weitere Routengruppen aus dem Monolithen gelöst — Wartung, Abwehr, Auskunft, Beobachtung, Systemlage — ohne einen einzigen neuen Kontext-Eintrag; mit Preflight, Resilienz und Selbsttest steht dort jetzt keine System-Route mehr",
            "Zehn Rechenkerne des Betriebs liegen in eigenen Modulen und werden damit erstmals einzeln geprüft: Recorder-Kommandozeilen, die ffmpeg-Zeile des Relays, der Eskalations-Backoff, die Entscheidungen aus dem Live-Signal, die Cookie-Bewertung, die Sendebild-Texte, die Fehlerkategorien der Aufnahme und die Kick-REST-Aufrufe",
            "„Live pausiert“ wird nicht mehr als Stream-Ende gelesen: die Pause-Grace war ab dem zweiten Aussetzer einer Sitzung wirkungslos — jede Pause kostete eine OFFLINE-Meldung, das Ende der Aufnahme und eine neue LIVE-Meldung",
            "Der TikTok-Chat baut die Verbindung nicht mehr im 15-Sekunden-Takt neu auf: 122 Listener-Starts in 85 Minuten hatten die Sign-Quota verbrannt, bis TikTok den Bot aussperrte — jetzt 14 statt 194 Neuaufbauten pro Stunde",
            "Acht Fehlerbilder, an denen die Cookie-Datei bisher komplett unlesbar wurde, sind repariert — und der Bot holt sich die rotierenden Gast-Tokens selbst, statt wegen 403 Alarm zu schlagen",
            "Der gespeicherte OAuth-Zustand lügt nicht mehr: ein von Google abgelehnter YouTube-Token überlebte den Neustart und meldete weiter „verbunden“, während Twitch die Verbindung schon bei einem 500er wegwarf — das Panel nennt jetzt auch den Grund",
            "Der Auto-Clipper erkennt meme-würdige Momente über eine kostenlose KI-Rotation (kein Claude-Budget), schneidet und postet sie nach Discord, legt zusätzlich einen echten Twitch-Clip an und lädt den Clip als ungelistetes YouTube-Video hoch — alles per Default an, YouTube gedeckelt auf vier Uploads am Tag",
            "AZRAEL steht als animierte Figur im Sendebild: unten rechts, schwebend, mit Mundbewegung im Silbentakt, Schwertarm und atmender Aura — und der Mund geht genau dann, wenn er wirklich redet, auch bei seinen Antworten im Chat",
            "Das Auslieferungsarchiv war seit der Discord-Herauslösung unvollständig — ohne discordbot.py, telegramversand.py, Übersetzungskatalog und Avatar-Dateien waren Discord und der Aufnahme-Versand auf dem Server still tot; der Bau prüft jetzt selbst, was importiert wird, und bricht ab, statt ein halbes Archiv zu liefern",
            "Die MOTD beim Einloggen nennt den schlimmsten Befund in Zeile zwei, misst den Netzdurchsatz, zeigt den Fehlerverlauf über sieben Tage, meldet ein Dashboard mit TLS nicht länger fälschlich als tot — und läuft wie der Windows-Installer jetzt vollständig auf Englisch",
            "Das Dashboard spricht wirklich Englisch: die Abdeckung stieg von 18 % auf 89 %, und Sätze, die ein Inline-Tag zerschneidet, verfallen nicht mehr als Bruchstücke — vorher meldete die Prüfung „0 fehlend“, weil sie nur zählte, was der Sammler überhaupt eingesammelt hatte",
            "Fehlermeldungen nach außen tragen keine Dateipfade, Zugangsdaten oder Stream-Schlüssel mehr — 22 Stellen, die die erste Runde durchgelassen hatte, sind zu, ein einheitlicher Riegel schließt ein echtes Symlink-Loch im Updater, und CodeQL meldet statt 242 nur noch 43 Befunde; ein offenes Dashboard ohne Token und PIN meldet sich zudem alle sechs Stunden auf Fehler-Ebene statt nur einmal beim Start",
            "Kein Dauerläufer blockiert mehr die Ereignisschleife: die Stillstände von 30 bis 68 Sekunden sind weg, Datenbankzugriffe laufen neben der Schleife",
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
