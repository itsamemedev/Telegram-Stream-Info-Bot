"""nc.version — zentrale Versions- und Changelog-Quelle (bot-frei).

Eine einzige Wahrheit für die Versionsanzeige (Dashboard-Footer, /api/version,
„Was ist neu"-Panel). Reine Daten + kleine Helfer, voll testbar.
"""

VERSION = "5.8.0"
CODENAME = "Nachlese"
RELEASE = "2026.11"


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
        "version": "5.8.0",
        "date": "2026-11",
        "title": "Nachlese",
        # Nebenversion: Bughunt + Security, Aufraeumen, Monolith-Abtrag (W199).
        "highlights": [
            "Zeitplaene und Konfiguration im Deck gehen bei gesperrter Datenbank nicht mehr verloren: sieben Routen lasen nachsichtig und schrieben zurueck — jetzt streng gelesen, unter Sperre geschrieben, sonst 503",
            "build/ waechst nicht mehr ohne Ende: jeder Lernzyklus legte eine volle Kopie des Monolithen ab (rund 2 GB im Jahr, in jeder Systemsicherung) — jetzt hoechstens 20",
            "Caches nehmen die Uhr nach der Sonde; die GeoIP-Ruhezeit gilt auch nach einem Fehlschlag",
            "Link-Video sendet nur Dateien aus seinem eigenen Arbeitsordner",
            "Der Highlights-&-Memes-Zusammenschnitt geht nur noch nach Discord — in die Telegram-Gruppen nur mit MEME_REEL_TELEGRAM=1 (war ungefragt an)",
            "Aufgeraeumt: 27 tote Weiterleitungen, ein totes Modul und leere Abschnitte im Monolithen; neun Dokumente im Doku-Index nachgetragen",
            "Monolith: Sperrliste und SSH-Angriffe nach nc/abwehrlage.py, die Proxy-GeoIP nach nc/geocache.py — bot.py 27.956 → 27.312 Zeilen",
        ],
    },
    {
        "version": "5.7.0",
        "date": "2026-11",
        "title": "Werkzeugkasten",
        # Nebenversion: MCP-Server im Deck verwalten (W198).
        "highlights": [
            "Neuer Reiter „09 MCP“: MCP-Server anlegen, bearbeiten, aktiv schalten und loeschen — der Token verlaesst den Server nie, nicht in Antworten, nicht im Log",
            "Verbindungstest mit echtem MCP-Handshake (Streamable HTTP, JSON und SSE): Protokoll, Servername und Werkzeugliste — oder der Grund mit Abhilfe (401, falsche Adresse, Umleitung, Zeitueberschreitung)",
            "Export als mcp_server.json, mit Token nur nach Rueckfrage; die llama-Oberflaeche fuehrt ihre eigene Liste im Browser",
            "Lage der llama-Oberflaeche im Reiter: ob --webui llamacpp und der MCP-Proxy laufen, mit Abhilfe und Tunnel-Hinweis",
            "Einstellungen bleiben nach dem Neuladen nicht mehr leer, wenn sie der zuletzt offene Reiter waren",
        ],
    },
    {
        "version": "5.6.0",
        "date": "2026-11",
        "title": "Kehraus",
        # Nebenversion: Bughunt, Aufraeumen, Monolith-Abtrag, Cookie-Knopf (W197).
        "highlights": [
            "KI-Abfrage im Deck: Frist von 15 s unter SQLite und MariaDB, Zeilendeckel auch bei innerem LIMIT, und unter MariaDB ueberhaupt lauffaehig — vier von sechs Regel-Abfragen sprachen SQLite",
            "yt-dlp- und Piper-Arbeiter starten nach einem Fehlstart nicht mehr bei jedem Aufruf neu (die Ersparnis kostete sonst doppelt); ein yt-dlp-Update hebt die Ruhezeit sofort auf",
            "Cookie-Pruefung im System-Tab: Knopf „Bereinigen“ entfernt abgelaufene Cookies und die Domain-Varianten, die der Bot nicht sendet — mit Vorschau, Backup und ohne je die Anmeldung zu verlieren",
            "--selfcheck stirbt nicht mehr an der Diagnose einer unlesbaren Datenbank (KeyError im Bericht); der Selbsttest ist in benannte Abschnitte zerlegt",
            "Monolith: stats.json-Erzeuger und Tagesbericht nach nc/, tote Huellen und veraltete Patches entfernt, bot.py 28.831 → 27.954 Zeilen",
            "llama-server zeigt wieder die Oberflaeche mit dem Reiter „MCP“ (--webui llamacpp, LLM_WEBUI); der CORS-Proxy fuer MCP-Server nur mit LLM_WEBUI_MCP_PROXY=1",
        ],
    },
    {
        "version": "5.5.0",
        "date": "2026-11",
        "title": "Stimme",
        # Nebenversion: AZRAEL an das lokale Qwen gebunden (W196).
        "highlights": [
            "AZRAEL spricht mit Persona ueber das lokale Qwen3-14B — ohne Claude davor und ohne stillen Wechsel in die Cloud (AZRAEL_LLM, Vorgabe lokal mit Server)",
            "Telegram, Discord und !ask bekamen die Persona gar nicht: jetzt beginnen alle Wege mit derselben, im Deck gesetzten Persona",
            "Prompt-Cache: die Persona steht vorn und wird einmal eingelesen statt bei jeder Nachricht — bei 7,8 Token/s Einlesen der groesste Teil der Wartezeit",
            "Ein Platz mit Vorrang statt Sofort-Abbruch: Gespraeche warten und ueberholen Reaktionen, Eigeninitiative faellt bei Stau weg und laesst Gespraechen eine Reserve im Stundenbudget",
            "Sichtbar statt still: /healthz nennt, wer AZRAEL antwortet, die Zeiten der letzten Antwort und den Cache-Anteil; jeder Rueckfall in die Cloud steht im Log",
        ],
    },
    {
        "version": "5.4.0",
        "date": "2026-11",
        "title": "Schlüsselbund",
        # Nebenversion: Cookies vom Telefon, 18+-Erkennung, frisches yt-dlp (W195).
        "highlights": [
            "Cookies vom Telefon: Header-String aus Cookie-Editor, Datei waehlen im Deck oder als Telegram-Dokument mit /cookies — ein gemeinsamer Weg, unter der Schreibsperre, mit 0600",
            "18+-Lives beim Namen: TikTok-Code 4003110 wird erkannt und mit Abhilfe gemeldet, statt „Abo oder Sitzung/IP“ zu raten",
            "Die Cookie-Anzeige sagt, wenn nur Gast-Tokens hinterlegt sind — dann bleiben 18+- und Abo-Lives zu",
            "Der Bot benutzt das yt-dlp und streamlink seiner venv (wie immer sie heisst) und meldet Alter und fehlendes curl_cffi; update.sh haelt beide frisch",
            "Reconnects loesen „live ohne Adresse“ nicht mehr mehrmals je Sekunde neu auf, und die Zeile dazu ist gedrosselt",
            "17 als Benutzertext markierte Telegram- und Discord-Texte fehlten im Uebersetzungskatalog und erschienen auf Englisch und Spanisch deutsch — jetzt erfasst und uebersetzt",
        ],
    },
    {
        "version": "5.3.1",
        "date": "2026-11",
        "title": "Leichtgewicht",
        # Patch-Fassung: MariaDB als Installer-Vorgabe (W194).
        "highlights": [
            "MariaDB ist die Vorgabe fuer neue Installationen: der Installer richtet Server, Datenbank, Nutzer, C-Treiber und Einstellungen von sich aus ein",
            "SQLite bleibt, wo MariaDB nicht sicher einzurichten ist: schon Daten in SQLite, kein Paketmanager, unter 1 GB RAM — oder SQLite steht ausdruecklich in der .env",
            "Laesst sich der Server nicht einrichten, faellt die neue Installation auf SQLite zurueck und sagt es — statt den Bot gegen einen fehlenden Server starten zu lassen",
            "Bestehende SQLite-Installationen werden nie still umgestellt: update.sh empfiehlt den Umzug (Vorgabe Ja) und macht ihn nur auf Nachfrage oder mit --mariadb",
            "Die Anleitung nannte fuer MariaDB DB_HOST/DB_NAME/DB_USER/DB_PASS — Variablen, die der Bot nie gelesen hat; jetzt die echten MARIADB_*",
        ],
    },
    {
        "version": "5.3.0",
        "date": "2026-11",
        "title": "Leichtgewicht",
        # Nebenversion: zehn Bausteine getauscht oder geteilt (W193).
        "highlights": [
            "Ein Chromium fuer alle Restream-Overlays statt einer je Restream: drei Restreams 1076 -> 530 MB, jeder weitere kostet rund 25 statt 300 MB",
            "yt-dlp und Piper laufen als dauerhafte Arbeiter: ein yt-dlp-Nachschlag 0,83 -> 0,067 CPU-Sekunden, Piper laedt die Stimme einmal statt je Satz — abschiessbar bei Haengern wie vorher",
            "MariaDB mit dem C-Treiber mysqlclient (3-7x weniger CPU je Abfrage, PyMySQL bleibt Rueckweg) und eigenen Server-Einstellungen: kein DNS je Verbindung, Commit 329 -> 177 us",
            "Whisper wird nach 15 Minuten ohne Sprache entladen und der Speicher zurueckgegeben; Discord laedt keine komplette Mitgliederliste mehr",
            "ik_llama.cpp mit quantisiertem KV-Cache (rechnerisch 0,6 GB weniger), nur wenn das Programm die Schalter kennt — sonst automatisch ohne",
            "Kick-API ueber eine geteilte Verbindung; ein Chat, der still am Tunnel vorbei liefe, meldet sich jetzt laut",
        ],
    },
    {
        "version": "5.2.1",
        "date": "2026-11",
        "title": "Sparflamme",
        # Patch-Fassung: der MariaDB-Pfad (W192) — der Betrieb laeuft auf MariaDB.
        "highlights": [
            "MariaDB-Zugriff fast doppelt so schnell: 233 statt rund 130 Mikrosekunden je db_conn(), gemessen gegen MariaDB 10.11 — der Verbindungsvorrat aus 5.2.0 galt nur fuer SQLite",
            "Kein ping mehr bei jedem Ausleihen (nur nach 30 s Leerlauf, MARIADB_PRUEFEN_NACH_S) und kein ueberfluessiges rollback nach einem erfolgreichen commit",
            "Server-Neustart ohne gescheiterten Aufruf: die erste Anweisung auf einer abgerissenen Verbindung laeuft einmal neu an, tote Verbindungen fliegen aus dem Pool",
            "Ein gescheiterter commit (Deadlock) rollt zurueck, bevor die Verbindung zurueck in den Pool geht; ein Abriss gibt seinen Slot frei",
            "/healthz zeigt den MariaDB-Pool: offen, belegt, frei, gespart, gewartet, erschoepft, verloren — die Poolgroesse laesst sich jetzt an Zahlen beurteilen",
        ],
    },
    {
        "version": "5.2.0",
        "date": "2026-11",
        "title": "Sparflamme",
        # Nebenversion: Stabilitaet und Ressourcen (W191), Konzept in
        # docs/KONZEPT_SPARFLAMME.md.
        "highlights": [
            "SQLite-Verbindungen werden wiederverwendet: 2 statt 180 Mikrosekunden je Datenbankzugriff, und der 8-MB-Seiten-Cache wird endlich warm (DB_VORRAT, Vorgabe 4, 0 = aus)",
            "Der Vorrat gibt nie eine Verbindung auf eine getauschte Datei, einen alten Pfad oder mit offener Transaktion heraus; die Wiederherstellung leert ihn vor dem Tausch",
            "Speicher geht an das System zurueck: zwei glibc-Arenen statt bis zu 64 und alle zehn Minuten malloc_trim — gemessen 861 MB Rest-RSS nach einer Lastspitze statt rund 105 MB",
            "/healthz zeigt beides: Vorrat (neu/wiederverwendet/verworfen) und Heap (zurueckgegebene MB)",
            "Abschaltbar ohne Codeaenderung: DB_VORRAT=0, SPEICHER_ARENEN=0, SPEICHER_TRIM_MIN=0",
        ],
    },
    {
        "version": "5.1.1",
        "date": "2026-11",
        "title": "Hausrecht",
        # Patch-Fassung: Sicherheits-Durchgang (W190).
        "highlights": [
            "DNS-Rebinding geschlossen: eine fremde Seite im Browser konnte ihren Namen auf 127.0.0.1 umbiegen und das Deck ueber den SSH-Tunnel ohne Anmeldung bedienen — der Tunnel gilt jetzt nur noch mit lokalem Host-Kopf (DASHBOARD_HOSTNAMEN fuer eigene Namen)",
            "PIN-Cookie mit Serverschluessel: ein abgegriffenes Cookie verriet die PIN per Offline-Probe in Sekunden, danach liessen sich Sitzungen ohne Ablauf faelschen",
            "Offener Telegram-Modus: ohne ALLOWED_USER_IDS konnte jeder Fremde /logs lesen, /diag abrufen, Cookies beziehen und /update ausloesen — diese vier brauchen jetzt eine Freischaltliste",
            "/healthz zeigt Fremden von aussen nur noch ok/degradiert statt Commit-Stand, Tunnel-Lage und Prozesszahlen",
            "PIN-Sperre zusaetzlich global (wechselnde IPv6-Adressen umgingen die Sperre je Adresse); Kick-OAuth-State zeitkonstant und mit Frist",
            "Deck: Restream-Quellnamen werden escaped; ikllama.sh nimmt SHA-256 auch gross geschrieben und prueft vor dem 9-GB-Download auf Hex",
        ],
    },
    {
        "version": "5.1.0",
        "date": "2026-11",
        "title": "Hellhörig",
        # Nebenversion: lokales LLM auf ik_llama.cpp (W181), Befunde aus dem
        # Produktionslog vom 11.11. (W180, W182–W187).
        "highlights": [
            "Lokales LLM jetzt ik_llama.cpp mit Qwen3-14B-Uncensored: tools/ikllama.sh entfernt ein vorhandenes llama.cpp zuerst, baut, laedt mit Pruefsumme und richtet den Dienst ein — Installer und update.sh (--ik-llama) rufen dasselbe Werkzeug",
            "Qwen3 denkt nicht laut: Denkmodus aus, <think>-Bloecke werden entfernt, eine reine Denk-Antwort geht an die Cloud statt leer in den Chat",
            "Live-Pruefung staut nicht mehr: jedes Tracking hoechstens einmal in der Schlange, jede Pruefung mit Frist, Prozessstart hat Vorrang vor Whisper",
            "Whisper-Modellwechsel prueft den freien Speicher — der Sprung auf 4,5 GB RSS kam vom Umschalten auf medium, nicht von einem Leck",
            "Cookie-Bezug ohne Desktop sagt den Grund statt HTTP 502; keine Telegram-Aufrufe mehr fuer Discord-Server-IDs; leere TikTok-Room-ID wird erklaert statt int('')",
            "Lagebild im Deck zeigt Encode- und Upload-Schlange, Discord-Aufnahme, Overlay-Browser, Tunnelwache, Kick-Chat und Spendenziel",
        ],
    },
    {
        "version": "5.0.0",
        "date": "2026-11",
        "title": "Gleichtakt",
        # Hauptversion: Tiefengrund-Bughunt ueber alle Bereiche (W174–W179).
        "highlights": [
            "Restream bricht nicht mehr auf allen Zielen zugleich weg: der Waechter hielt bei Plattenlast den gesunden Sender fuer tot, weil das Text-Overlay den Fortschrittsleser blockierte",
            "Zeitstempel-Glaettung in Aufnahme und Restream: Spruenge und Ruecklaeufe der TikTok-Quelle zerlegen keine Aufnahme mehr (Standbild, Ton weg) und trennen kein Ziel mehr",
            "Encode-Warteschlange: Clips, Memes, Chat-Einbrennen und Verkleinern laufen nacheinander und nur, wenn die Maschine Luft hat — Aufnahme und Restream haben Vorrang",
            "Telegram: wieder ein Thema je Nutzer; Gruppenwechsel zur Supergruppe wird erkannt und nachgezogen; Uploads gehen bei Neustart nicht mehr verloren und werden wiederholt",
            "Discord bekommt die ganze Aufnahme in hochladbaren Teilen (DISCORD_AUFNAHME_UPLOAD), nicht nur Highlights und Memes",
            "AZRAEL ist mit dem Brain verbunden: Antworten im Kick-Chat kennen Sendezeiten, Gewohnheiten und die letzte Sendung des Streamers; das Brain lernt keine Schein-Sitzungen mehr",
            "Kick-Chat ueber Centrifugo, /spenden in Telegram und Discord, ein Spendenziel fuer Website, Overlay, Sendebild und Chat — mit Bits, Superchats und Subs in Euro",
            "Sicherheit: Deck lehnt Schreibanfragen fremder Seiten ab (CSRF), LD_PRELOAD/PATH & Co. sind nicht mehr aus dem Deck setzbar",
            "Platz-Waechter loescht nur noch Gesichertes und Unmarkiertes; keine doppelten Live-Meldungen, keine doppelte Aufnahme, Pruefschleife mit Lebenszeichen",
        ],
    },
    {
        "version": "4.6.23",
        "date": "2026-11",
        "title": "Leitstand",
        # Patch-Fassung von 4.6: ein Spendenziel (W173).
        "highlights": [
            "Ein Spendenziel für Website, Stream-Overlay, Sendebild und /spenden — dasselbe Ziel, derselbe Stand, derselbe Zeitraum",
            "Der Stand zählt jede Spende auf eigenen Kanälen (Kick, Twitch, YouTube, im Deck erfasst) im laufenden Monat; TikTok-Gifts nie",
            "Vorher zählte die Website nur manuell erfasste Spenden, das Overlay nur ab Stream-Start und gegen ein eigenes Ziel (Vorgabe: aus)",
            "/spenden zeigt jetzt auch den Stand: „120 € von 500 € (24 %) · monatlich\"",
            "Das Ziel im Overlay-Formular gilt überall und überlebt einen Neustart; leere Felder lassen es unverändert",
        ],
    },
    {
        "version": "4.6.22",
        "date": "2026-11",
        "title": "Leitstand",
        # Patch-Fassung von 4.6: /spenden (W172).
        "highlights": [
            "Neuer Befehl /spenden auf Telegram und Discord: PayPal mit Spenden-Link, alle eingetragenen Krypto-Adressen und das Spendenziel",
            "Für jeden: Zuschauer stehen in keiner Freischaltliste, die Antwort enthält nur, was auch die Website zeigt",
            "Eine Quelle für Website, Deck und Chat — eine im Deck geänderte Adresse gilt sofort, ohne Neustart",
            "Ist nichts eingetragen, sagt der Bot das mit den Variablennamen, statt still zu schweigen",
            "Neu: DONATION_LINK für einen zusätzlichen Link (z. B. die Spendenseite); README mit Abschnitt „Unterstützen\"",
        ],
    },
    {
        "version": "4.6.21",
        "date": "2026-11",
        "title": "Leitstand",
        # Patch-Fassung von 4.6: Kick-Chat ueber Centrifugo (W171).
        "highlights": [
            "Kick-Chat läuft wieder: Kick hat den Chat im Oktober von Pusher auf Centrifugo umgestellt, jeder Pusher-Key wurde mit 4001 abgewiesen",
            "Neuer Weg wie im Web-Client von kick.com: Gast-Token ohne Login, Websocket-Adresse von Kick erfragt statt fest verdrahtet, Token wird vor Ablauf erneuert",
            "Moderation, AZRAEL, Overlay und Sub-/Gift-Dank laufen unverändert — Kick liefert in beide Wege dieselben Ereignisse",
            "Prüfen auf dem Server: venv/bin/python tools/kickchat.py zeigt Anmeldung, Abo und eingehende Nachrichten",
            "Schalter KICK_CHAT_WEG (centrifugo, Vorgabe; pusher als Rückweg, falls Kick zurückwechselt)",
        ],
    },
    {
        "version": "4.6.20",
        "date": "2026-11",
        "title": "Leitstand",
        # Patch-Fassung von 4.6: ein Chromium je Restream statt je Bild (W170).
        "highlights": [
            "HTML-Overlay: ein dauerhaft laufender Chromium je Restream statt eines Kaltstarts für jedes Overlay-Bild — gemessen 0,08 statt 0,86 CPU-Sekunden je Bild",
            "Der Overlay-Browser läuft mit nice (FFMPEG_NICE_BG) und tritt hinter den Transcode zurück; ein verspätetes Overlay-Bild wiederholt nur das letzte",
            "Sprechblasen und Alerts im Overlay laufen jetzt wirklich: die Seite bleibt offen, statt für jedes Bild neu geladen zu werden",
            "Stirbt oder hängt der Browser, wird er beendet und nach 30 s neu gestartet; startet er gar nicht, bleibt der alte Einzelschuss und das Log sagt es auf error",
        ],
    },
    {
        "version": "4.6.19",
        "date": "2026-11",
        "title": "Leitstand",
        # Patch-Fassung von 4.6: Link gepostet, Video als Antwort (W169).
        "highlights": [
            "YouTube- oder TikTok-Link in Telegram oder Discord gepostet: der Bot lädt das Video und antwortet direkt darauf mit der Datei",
            "Passt das Video nicht ins Upload-Limit (Telegram 48 MB, Discord je nach Boost-Stufe), wird erst eine kleinere Fassung gewählt und sonst neu kodiert",
            "Scheitert der Download, antwortet der Bot mit dem Grund — privat, zu lang, YouTube-Anmeldesperre, 403 — statt still nichts zu tun",
            "Live-Links bleiben außen vor; höchstens drei Links je Nachricht, Abklingzeit je Absender, ein Download zur Zeit (LINK_VIDEO_PARALLEL)",
            "Schalter: LINK_VIDEO (an), LINK_VIDEO_MAX_MIN (20), LINK_VIDEO_COOLDOWN_S (15), LINK_VIDEO_YT_COOKIES_PATH für YouTube-Cookies",
        ],
    },
    {
        "version": "4.6.18",
        "date": "2026-11",
        "title": "Leitstand",
        # Patch-Fassung von 4.6: ein Thema, ein Kanal (W168).
        "highlights": [
            "Telegram: EIN Upload-Thema je Gruppe („🎬 Aufnahmen“, TELEGRAM_UPLOAD_TOPIC_NAME) statt eines @name-Themas je getracktem Nutzer",
            "Die alten @name-Themen werden umgezogen: jede noch vorhandene Aufnahme wird ins Upload-Thema nachgeladen, erst danach wird das alte Thema gelöscht — mit gemerktem Fortschritt, ohne Doppel nach einem Neustart",
            "Discord: EIN Clip-Kanal (#clips, DISCORD_CLIP_CHANNEL) statt einer Kategorie mit drei Kanälen je Nutzer; die alten 🎯-Bereiche werden umkopiert und gelöscht, von Hand angelegte bleiben tabu",
            "Per Discord-/track angelegte Nutzer sind nur Discord — ihre Aufnahmen gehen nicht mehr ersatzweise nach Telegram",
            "Dashboard: neue Trackings landen in der Telegram-Gruppe statt in der Discord-Guild; bestehende Dashboard-Trackings an der Guild werden beim Start umgezogen (Dubletten entfernt)",
            "Offline-Meldung: die Zuordnung Tracking ↔ Chat konnte bei zwei Trackings in derselben Gruppe verrutschen",
        ],
    },
    {
        "version": "4.6.17",
        "date": "2026-11",
        "title": "Leitstand",
        # Patch-Fassung von 4.6: Befunde aus den Logs vom 06./07.11. (W167).
        "highlights": [
            "Telegram-Uploads: Aufnahmen von Nutzern, die per Discord-/track angelegt wurden, gingen an die Discord-Guild und wurden verworfen — jetzt an DISCORD_TRACK_GROUP_ID, sonst an die erste freigeschaltete Telegram-Gruppe",
            "Der Upload wartet nicht mehr auf das Einbrennen des Chats (bis zu viermal die Aufnahmedauer) — der Chat kommt danach im Hintergrund in die gespeicherte Aufnahme",
            "Restream-Durchreicher: scheitert yt-dlp mit „not currently live\", wird jetzt auch streamlink versucht",
            "Kick-Chat: lehnt jeder Cluster den eingestellten Pusher-Key ab, probiert der Bot die bekannten Keys und sagt, welcher in die .env gehört — und meldet das einmal statt die ganze Nacht alle 15 Minuten",
            "Cookie-Datei wird nicht mehr auf dem Event-Loop geparst (gemessen: 1,8 s Stillstand)",
        ],
    },
    {
        "version": "4.6.16",
        "date": "2026-11",
        "title": "Leitstand",
        # Patch-Fassung von 4.6: der Grund steht im Panel (W166).
        "highlights": [
            "Restream-Ziel „keine spielbare Quell-URL\": das Deck sagt jetzt auch, warum der Durchreicher ebenfalls nichts brachte",
            "Bisher stand dieser Grund nur gedrosselt im Log — im Panel blieb die halbe Auskunft",
            "Mögliche Gründe mit Abhilfe: Ruhezeit nach gescheiterten Aufnahmen, kein yt-dlp/streamlink, Sendebrücke aus, Multi-Modus independent",
            "Die Fehlermeldung eines Ziels wird bis 600 statt 300 Zeichen gespeichert, damit die Abhilfe nicht abgeschnitten wird",
            "Die Einordnung des Wächters bleibt dieselbe: „live, aber ohne Adresse\" wird weiter von „offline\" unterschieden",
        ],
    },
    {
        "version": "4.6.15",
        "date": "2026-11",
        "title": "Leitstand",
        # Patch-Fassung von 4.6: alte Beilagen einsammeln, manuelle Spenden (W164),
        # Durchreicher nach der Ruhezeit (W165).
        "highlights": [
            "Alte .ass-Beilagen neben Aufnahmen sammelt der Bot beim Start selbst ein: der Chat darin wird in die Aufnahme eingearbeitet, die Datei verschwindet",
            "Eine Beilage ohne zugehörige Aufnahme wird entfernt; fremde Untertiteldateien bleiben unangetastet",
            "Im Deck eingetragene Spenden (PayPal, Krypto) zählen jetzt im Spendenziel des Overlays, in den Spendenlisten und in der Gegenprobe des Steuer-Journals",
            "Ursache: die Einnahmenliste nannte „manuell\", gespeichert wurde „manual\" — der Eintrag traf nie eine Zeile",
            "Die Website-Summe rechnet manuelle Spenden weiterhin getrennt — nichts wird doppelt gezählt; im Overlay tragen sie das Abzeichen DIREKT",
            "Restream ohne Bild bei laufendem TikTok-Live: nach drei gescheiterten Aufnahmeversuchen blieb der Durchreicher für das ganze Live gesperrt — jetzt nur für die Ruhezeit von 2 bis 10 Minuten",
        ],
    },
    {
        "version": "4.6.14",
        "date": "2026-11",
        "title": "Leitstand",
        # Patch-Fassung von 4.6: Chat-Nachtrag statt Beilage (W163).
        "highlights": [
            "Eine beim Stopp gesicherte Aufnahme bekommt ihren Chat jetzt wie jede andere: eingebrannt oder als Untertitelspur, beim nächsten Start nachgetragen",
            "Bisher lag er als .ass-Datei daneben — Telegram und das Deck sahen ihn nie, kein Löschweg kannte die Datei, und das Archiv ließ sie zurück",
            "Beim Stopp kostet das einen Datenbankeintrag statt Minuten Einbrennen — das Herunterfahren bleibt schnell",
            "Die Größe im Deck folgt der Datei nach dem Einarbeiten; ein Eintrag, der dreimal scheitert, wird aufgegeben statt jeden Start zu belasten",
            "Die neue Tabelle steht im Schema und zieht beim Umzug nach MariaDB mit",
        ],
    },
    {
        "version": "4.6.13",
        "date": "2026-11",
        "title": "Leitstand",
        # Patch-Fassung von 4.6: zweiter Bughunt-Durchgang (W162).
        "highlights": [
            "Der Highlights-&-Memes-Zusammenschnitt ging sofort an Telegram, auch außerhalb des Upload-Fensters — oft mitten in der Nacht und vor der Aufnahme selbst",
            "Außerhalb des Fensters wandert er jetzt in dieselbe Warteschlange wie die Aufnahmen",
            "Steuer-Journal: ein unlesbarer Kurs oder Originalbetrag brach die Buchung mit HTTP 500 ab statt mit einer Meldung",
            "„nan\" und „inf\" als Kurs oder Originalbetrag wurden gebucht und standen so in der CSV fürs Steuerbüro — jetzt abgelehnt",
            "Ein Kurs von 0 bleibt „kein Kurs\", wie bisher",
        ],
    },
    {
        "version": "4.6.12",
        "date": "2026-11",
        "title": "Leitstand",
        # Patch-Fassung von 4.6: Tiefengrund-Bughunt ueber W150-W160 (W161).
        "highlights": [
            "Kick-Chat: zog Kick den Key nach einem gefundenen Cluster erneut um, blieb die Suche am nächsten unerreichbaren Kandidaten hängen — „bestätigt\" gilt jetzt je Cluster",
            "Ein verschlossener Raum (live ohne Stream-Adresse) blieb über das Ende des Lives hinaus markiert und sperrte beim nächsten, öffentlichen Live den Durchreicher des Restreams",
            "Der Chat-Empfang einer Aufnahme lief nach deren Ende bis zum Ende des Lives weiter und verbrauchte Sign-Quota — jetzt endet er mit der Aufnahme, ein Segmentwechsel bleibt überbrückt",
            "Ein Clip kurz vor dem Aufnahmeende konnte aus der Fassung mit eingebranntem Chat schneiden und einen zweiten Chat darüberlegen — das Einarbeiten wartet jetzt auf offene Clips",
            "Discord: der automatische Abgleich löscht eine 🎯-Kategorie nur noch, wenn sie ausschließlich die Kanäle trägt, die der Bot selbst anlegt — eine von Hand angelegte bleibt samt Verlauf stehen",
        ],
    },
    {
        "version": "4.6.11",
        "date": "2026-11",
        "title": "Leitstand",
        # Patch-Fassung von 4.6: HTML-Modus traegt die Quelle (W160).
        "highlights": [
            "Restream im HTML-Modus: Quellbild und Quellton kamen nicht an, gesendet wurden nur Overlay, Chat und AZRAEL — gemessen und behoben",
            "Ursache: der Sender tastete beim Start die Overlay-FIFO sekundenlang ab, die Sendebrücke hielt den Rückstau für eine stumme Quelle und schoss den gesunden Zubringer ab; danach stand das Quellbild eingefroren",
            "Die Sendebrücke unterscheidet jetzt Rückstau beim Sender von einer stummen Quelle",
            "Die Overlay-FIFO öffnet ohne Abtastpause — jede der beiden Korrekturen behebt den Fehler für sich",
            "Neuer Vertrag: ein echter Lauf im HTML-Modus mit Overlay, Stimme und Avatar misst Quellbild, Bewegung und Quellton im Ausgang",
        ],
    },
    {
        "version": "4.6.10",
        "date": "2026-11",
        "title": "Leitstand",
        # Patch-Fassung von 4.6: Restream weicht aus, Memes, Chat im Clip (W159).
        "highlights": [
            "Restream ohne Quellbild: liefert die Quelle drei Minuten lang kein Bild, wechselt der Restream auf ein Ziel der Auto-Liste, das eine echte Stream-Adresse hat — bisher gab es den Wechsel nur bei „offline\"",
            "Gibt es kein solches Ziel, bleibt der Restream mit AZRAEL und Chat stehen und sagt das im Log, statt stumm Pausenbild zu senden",
            "Der Hype-Director schneidet die Clips einer Aufnahme nach dem Ende zu einem Highlights-&-Memes-Video zusammen und schickt es an Discord und die Telegram-Gruppen",
            "Jeder Highlight-Clip trägt jetzt den Chat seines Zeitfensters, eingebrannt wie in der Aufnahme",
            "Neue Stellschrauben: RESTREAM_OHNE_BILD_S, MEME_REEL, MEME_REEL_MIN, MEME_REEL_MAX, MEME_REEL_TELEGRAM",
        ],
    },
    {
        "version": "4.6.9",
        "date": "2026-11",
        "title": "Leitstand",
        # Patch-Fassung von 4.6: der Chat kommt in die Aufnahme (W158).
        "highlights": [
            "Aufnahmen tragen jetzt den TikTok-Chat — eingebrannt unten links wie im Restream, sichtbar auch im Telegram-Player",
            "Für jede laufende Aufnahme läuft ein Chat-Empfang; bisher gab es ihn nur für Restreams und Live-React-Nutzer, und viele Aufnahmen hatten gar keinen Chat",
            "AUFNAHME_CHAT=einbrennen|untertitel|aus — „untertitel\" legt den Chat als abschaltbare Spur ab, ohne neu zu kodieren",
            "Das Einbrennen läuft mit niedrigster Priorität nach der Aufnahme; scheitert es, bleibt die Aufnahme ohne Chat erhalten statt verloren",
            "Chattext kann keine Untertitel-Formatierung einschleusen, und doppelte Nachrichten zweier Empfänger erscheinen nur einmal",
        ],
    },
    {
        "version": "4.6.8",
        "date": "2026-11",
        "title": "Leitstand",
        # Patch-Fassung von 4.6: Befunde aus dem Log vom 06.11. mittags (W157).
        "highlights": [
            "Kick-Chat: die Cluster-Suche probierte „us1\", das es bei Pusher nicht gibt, und blieb dort am DNS-Fehler hängen — jetzt nur echte Cluster, und ein unerreichbarer Kandidat wird verlassen",
            "Restream-Statuswechsel schreiben neben dem Event-Loop: ein MariaDB-Commit hielt den Loop eine Sekunde an",
            "Die Warnung „Stream-Auflösung ergebnislos\" flutete das Log (290 Zeilen in 36 Minuten): jeder gesunde Nutzer leerte die Drossel für die kranken",
            "Räume ohne Stream-Adresse: die Meldung behauptet nicht mehr „Abo/18+\", sondern nennt beide möglichen Ursachen und was die Abo-Erkennung sagt",
            "Kürzere Ruhezeit für solche Räume (2 bis 10 statt 5 bis 30 Minuten) — ein wieder offener Raum wird schneller aufgenommen",
        ],
    },
    {
        "version": "4.6.7",
        "date": "2026-11",
        "title": "Leitstand",
        # Patch-Fassung von 4.6: das Lagebild als Radarschirm (W156).
        "highlights": [
            "Das Lagebild der Übersicht ist ein Radarschirm: Entfernungsringe, Gradskala, Plotterraster und ein Strahl, der die Live-Ziele beim Überstreichen aufleuchten lässt",
            "Stationen als Glasmodule mit Blendenkante und Schatten, der Kern als Metallscheibe mit drehender Skala und Statusring",
            "Auf Leitungen mit Restream laufen Datenpakete — schnell, wenn gesund, zäh, wenn langsam, keine, wenn gestört",
            "Live-Ziele als Radarkontakte mit Welle und Hof, Aufnahme mit blinkendem REC-Punkt, Namen auf Schildern mit Führungslinie",
            "Bei reduzierter Bewegung und im Kontrast-Thema steht alles still und leuchtet nichts — auf dem Handy skaliert das Bild mit",
        ],
    },
    {
        "version": "4.6.6",
        "date": "2026-11",
        "title": "Leitstand",
        # Patch-Fassung von 4.6: Restream zeigte dauerhaft das Pausenbild (W155).
        "highlights": [
            "Restream ohne Bild: lieferte der Zubringer Daten, an denen die Weiche nicht umschalten konnte, blieb das Pausenbild für immer stehen — ohne eine einzige Logzeile",
            "Die Sendebrücke erkennt diese Lage jetzt nach der Anlaufzeit, nennt den Grund (keine PMT, kein Bildstrom, kein Keyframe-Merker) und startet den Zubringer neu kodierend",
            "Bleibt das Bild auch neu kodiert aus, endet die Brücke nach der Grenze mit einer ERROR-Zeile statt still weiterzusenden",
            "Der Vertrag speist dafür einen echten ffmpeg-Strom ein — einmal gesund, einmal ohne Keyframe-Merker",
            "Vertrag geschärft: eine Zusicherung prüfte nur ein Wort, das auch der falsche Satz enthielt — die Mutationsprobe hat es gefangen",
        ],
    },
    {
        "version": "4.6.5",
        "date": "2026-11",
        "title": "Leitstand",
        # Patch-Fassung von 4.6: Befunde aus dem Log des Betreibers (W154).
        "highlights": [
            "Abo- und 18+-Lives werden erkannt: statt alle 20 Sekunden einen sterbenden yt-dlp zu starten, ruht der Bot und sagt einmal laut, dass Cookies eines berechtigten Kontos fehlen — nicht der Proxy",
            "Ein Restream, dessen Quelle nie ein Bild liefert, stand bisher stumm auf dem Pausenbild; jetzt meldet die Sendebrücke den Grund und beendet nach der Grenze, statt ewig dunkel zu senden",
            "Kick-Chat: lehnt Pusher den Key mit 4001 ab, probiert der Bot die Cluster selbst durch, statt 15 Minuten zu warten — und sagt, welcher Wert in die .env gehört",
            "MariaDB: Summen und Mittelwerte kommen als Zahl wie unter SQLite — „Object of type Decimal is not JSON serializable\" brach das Lernen der Evolution ab",
            "tools/kickpusher.py und der Bot probieren dieselbe Cluster-Liste",
        ],
    },
    {
        "version": "4.6.4",
        "date": "2026-11",
        "title": "Leitstand",
        # Patch-Fassung von 4.6: zweite Runde des Bughunts (W152).
        "highlights": [
            "PIN- und Token-Cookie tragen hinter dem HTTPS-Proxy des Installers jetzt Secure — vorher reichte ein Aufruf über http://, und sie gingen im Klartext über die Leitung",
            "Ein Umlaut im PIN-Feld brachte den Login mit HTTP 500 zum Absturz und zählte nicht als Fehlversuch",
            "Ein Rollback kann nicht mehr neben einem laufenden Update schreiben — beide zusammen hinterließen einen Stand, der weder alt noch neu war",
            "Die Spendenliste im Deck las nach einem Fehler das Ergebnis der vorigen Abfrage",
            "Discord: jeder getrackte User bekommt seinen Bereich von selbst, und der eines nicht mehr getrackten wird gelöscht — alle zehn Minuten, ohne /setup_targets",
        ],
    },
    {
        "version": "4.6.3",
        "date": "2026-11",
        "title": "Leitstand",
        # Patch-Fassung von 4.6: MariaDB vergleicht bytegenau wie SQLite (W151).
        "highlights": [
            "Der Umzug nach MariaDB brach an doppelten Treuepunkte-Schlüsseln ab: MariaDB hielt Nora und nora, ängie und angie oder ｊａｎａ und jana für denselben Zuschauer — SQLite nicht",
            "Alle Tabellen vergleichen jetzt bytegenau wie SQLite (utf8mb4_nopad_bin); auch Leerzeichen am Ende zählen, wie in SQLite",
            "Schon angelegte Tabellen — etwa aus dem abgebrochenen Umzug — werden beim Umzug und beim Start angeglichen",
            "Im laufenden Betrieb auf MariaDB hätte dieselbe Regel die Punkte zweier Zuschauer still zusammengelegt",
            "Die Suche bleibt unverändert: sie vergleicht ohnehin in Kleinbuchstaben",
        ],
    },
    {
        "version": "4.6.2",
        "date": "2026-11",
        "title": "Leitstand",
        # Patch-Fassung von 4.6: der Umzug nach MariaDB (W150), gegen eine
        # echte MariaDB 10.11 nachgefahren.
        "highlights": [
            "Der Umzug nach MariaDB brach an „unbekannten Tabellen“ ab: Steuer-Journal und Stream-Archiv stehen jetzt im Schema und ziehen mit — die Hash-Kette bleibt intakt",
            "Das Steuer-Journal ließ sich unter MariaDB gar nicht anlegen; es hat jetzt eine eigene MariaDB-Fassung",
            "Ein Prozentzeichen in einem Datensatz ließ den MariaDB-Import scheitern, und das Stream-Archiv schickte unter MariaDB keine gültige Abfrage — beides behoben",
            "Reste einer Rettung mit sqlite3 .recover blockieren den Umzug nicht mehr: sie bleiben mit Hinweis in der SQLite-Datei",
            "Gegen eine echte MariaDB 10.11 nachgefahren: Umzug, Buchen, Storno, Kettenprüfung und Archivsuche",
        ],
    },
    {
        "version": "4.6.1",
        "date": "2026-11",
        "title": "Leitstand",
        # Patch-Fassung von 4.6: Tiefengrund-Bughunt (W149), elf Befunde,
        # drei davon Sicherheit.
        "highlights": [
            "Hinter dem nginx des Installers war das Deck ohne Anmeldung offen: jede Anfrage kam als 127.0.0.1 an und galt als SSH-Tunnel — jetzt zählt nur Loopback ohne Weiterleitungskopf, und X-Forwarded-For wird von rechts gelesen",
            "Der OAuth-Rückruf von Twitch und YouTube tauschte ohne laufende Anmeldung jeden Code — ein Fremder konnte sein Konto an den Bot binden; der state ist jetzt Pflicht und gilt einmal",
            "Steuer-Journal: jede Storno-Buchung aus dem Deck meldete die Hash-Kette als gebrochen; nan, inf, ungültige Daten und Storno auf fehlende Buchungen werden abgelehnt",
            "Retention und stündliches Aufräumen lassen markierte Aufnahmen stehen, days=0 löscht nicht mehr mit 30 Tagen, und kein Löschweg greift mehr außerhalb seines Ordners",
            "Die .env wird so geschrieben, wie dotenv sie liest, und das Update spielt genau den Commit ein, den es meldet",
        ],
    },
    {
        "version": "4.6",
        "date": "2026-11",
        "title": "Leitstand",
        # v4.6 traegt W144 bis W148: alles im Deck einstellbar, alles
        # beobachtet — Einstellungen in der Datenbank, Prometheus/Grafana
        # vollstaendig und bewacht, der Datenbank-Waechter, das neue
        # Lagebild, der Durchreicher und das Ausfuehrungsrecht beim Update.
        "highlights": [
            "Einstellungen im Deck: alle rund 571 Variablen durchsuchbar, gespeichert in der Datenbank und vor der .env geladen — Zugang, Befehle, Pfade und die Datenbank-Verbindung bleiben geschützt in der .env",
            "Prometheus und Grafana vollständig: jeder Messwert hat ein Panel, 16 Alarmregeln mit Tests, die .env trägt PROMETHEUS_URL und GRAFANA_*, und Grafana bekommt ein erzeugtes Passwort statt admin/admin",
            "Der vierzehnte Wächter beobachtet die Datenbank — Antwortzeit, Zuwachs, Journal, Schema und ob die Einstellungen geladen wurden",
            "Das Lagebild der Übersicht neu gezeichnet: Kern, sieben Stationen mit Status-LED, Wächter an festen Plätzen — in jedem Thema lesbar und ab dem ersten Laden sichtbar",
            "Log-Verluste sind für /healthz und Prometheus sichtbar; vorher stand der Zähler Millisekunden nach dem Verlust wieder auf 0",
            "Zwei neue Wächter für Prometheus und Grafana: sie melden feuernde Alarme, gescheiterte Regeln und eine leere Datenquelle, starten einen hängenden Dienst neu, und das Deck steuert beide über drei feste Befehle",
            "Restream ohne ziehbare Adresse: gibt TikTok weder FLV noch HLS heraus, holt yt-dlp den Stream selbst und reicht ihn an die Sendebrücke durch",
            "sudo ./update.sh scheiterte mit „Permission denied“: die Update-Funktion übernimmt jetzt das Ausführungsrecht aus dem Archiv und setzt es auch für unveränderte Dateien",
        ],
    },
    {
        "version": "4.5.3",
        "date": "2026-11",
        "title": "Vielstimmig",
        # Dritte Patch-Fassung von 4.5: update.sh fragt nach, was fehlt, und
        # zieht die Datenbank auf Wunsch nach MariaDB um (W143).
        "highlights": [
            "bash tools/update.sh fragt im geführten Modus nach allem, was fehlt: Prometheus, Grafana, optionale Pakete und den Umzug nach MariaDB — ein Zeitplan löst davon nie etwas aus",
            "SQLite → MariaDB in einem Schritt: Server, Datenbank und Nutzer anlegen, Bot kurz stoppen, jede Tabelle umziehen, nachzählen und erst dann DB_BACKEND=mariadb in die .env schreiben — die SQLite-Datei bleibt als Rückweg liegen",
            "Das MariaDB-Schema war nie lauffähig: zwei reservierte Spaltennamen (lines, trigger) und neun indizierte TEXT-Spalten brachen jeden Start; gegen einen echten MariaDB-Server gemessen und behoben",
            "Treuepunkte und der Discord-Tagesbonus buchten auf MariaDB still nie — ON CONFLICT ist SQLite; beide Upserts sprechen jetzt beide Dialekte",
            "Der Installer schaltete auf eine leere MariaDB um, obwohl die Daten in SQLite lagen; jetzt bleibt er auf SQLite und verweist auf den Umzug",
        ],
    },
    {
        "version": "4.5.2",
        "date": "2026-11",
        "title": "Vielstimmig",
        # Zweite Patch-Fassung von 4.5: zehn Verbesserungen quer durch das
        # Projekt (W142).
        "highlights": [
            "/quelle ‹name› in Telegram und Discord: die Quellprobe misst vom Handy aus jeden Weg zu einem Live-Stream und nennt die Abhilfe — ohne SSH",
            "/tracklist zeigt wie das Deck „unbekannt“, „ausstehend“ und „überfällig“ statt eines alten LIVE, und /healthz zählt dasselbe ohne Nutzernamen",
            "Fällt ein Tracking aus der Abfrage, meldet der Bot das selbst als Fehler mit den Namen — vorher sah man es nur, wenn man im Deck hinsah",
            "Die Systemsicherung wird beim Sichern geprüft: ohne mysqldump meldete sie bisher Erfolg mit einer Platzhalterzeile statt der Datenbank",
            "Releases tragen SHA256SUMS, das Deck zeigt die Herkunft der Stream-Adressen, und Profil-Schnappschüsse wachsen nicht mehr mit jedem Klick",
        ],
    },
    {
        "version": "4.5.1",
        "date": "2026-11",
        "title": "Vielstimmig",
        # Erste Patch-Fassung von 4.5: der Befund vom 05.11. — sieben Nutzer
        # live, kein Restream, „weder FLV noch HLS" (W141).
        "highlights": [
            "Sieben Nutzer live und kein Restream, weil „weder FLV noch HLS“: die Kette kannte genau diese zwei Formen und verwarf alles andere. TikToks stream_data wird jetzt auch auf CMAF und DASH gelesen, und yt-dlp-Formate als DASH-Manifest oder MP4 werden nicht mehr weggeworfen — als letzte Quelle für Restream und Aufnahme",
            "tools/quellprobe.py misst auf dem Server für einen Live-Nutzer jeden Weg: alle yt-dlp-Formate, die Adressen der Live-Seite, ffprobe auf jede Adresse und yt-dlp als Durchreicher — und nennt die Abhilfe",
            "Lief nur die FLV-Adresse bald ab, verwarf der yt-dlp-Weg auch eine HLS-Adresse mit einer Stunde Laufzeit; jetzt wird einzeln gestrichen",
            "Warum ein Restream nicht startet, steht jetzt im Deck unter dem Ziel, und /healthz zählt je Weg, woher die Adressen der letzten Stunde kamen und wie oft keine kam",
            "Zwei verschluckte Fehler im Restream-Pfad werden gemeldet, und das Schreiben des Panel-Status läuft neben dem Event-Loop",
        ],
    },
    {
        "version": "4.5",
        "date": "2026-11",
        "title": "Vielstimmig",
        # v4.5 traegt W134 bis W140: das Technologie-Audit (Lieferkette,
        # Lockfile, Python 3.14 in der CI), den Kick-Chat, der nie lief, und
        # die Oberflaeche — drei Sprachen, vier Themen, Profile, die etwas
        # sagen, und ein Deck, das „unbekannt" nicht mehr als „live" zeigt.
        "highlights": [
            "Spanisch als dritte Sprache: alle 1557 Texte in Deck, Brain-Seite, Overlay, Telegram und Discord; ein Browser mit es-* bekommt sie von selbst, und ein Vertrag hält Platzhalter und Nähte auf dem Stand des Englischen",
            "Zwei neue Deck-Themen: „Kontrast“ erreicht für jede Farbe WCAG AAA und wählt sich bei „mehr Kontrast“ im System von selbst, „Phosphor“ ist grüner Bildschirmphosphor für den Leitstand bei Nacht — beide aus den Farbwerten nachgerechnet",
            "Das TikTok-Profil im Deck lud nie: die Route rief die Profilabfrage auf der HTTP-Session statt auf dem Scraper auf. Jetzt lädt es, und Deck, Telegram und Discord zeigen Verhältnisse, Follower-Verlauf über 24 h und 7 Tage, Kontoart, Sprache und Bio-Link — oder, wenn TikTok ablehnt, den Grund mit Abhilfe",
            "Online/Offline ehrlich: wer seit über zehn Minuten nur „unbekannt“ liefert, steht als „? unbekannt“ da statt mit seinem alten Wert; nie geprüfte und überfällige Trackings sind sichtbar, jede Zeile nennt „geprüft vor …“",
            "Discord zeigt die Telegram-Auswertungen lesbar: Tabellen als Codeblöcke statt Fettdruck, Links und Zitate übersetzt, geschnitten an Absatzgrenzen",
            "Der Kick-Chat lief nie — Pusher lehnte den App-Key ab und der Bot versuchte es alle zehn Sekunden wieder. Schließcodes 4000–4099 warten jetzt 15 Minuten, und tools/kickpusher.py klärt Key und Cluster am Server",
            "Lieferkette: Untergrenzen, die 69 bekannte Schwachstellen erlaubten, sind angehoben; der Produktionsstand liegt als requirements.lock.txt im Repo und wird in jedem CI-Lauf mit pip-audit geprüft, Python 3.14 läuft in der CI mit, Dependabot ist eingerichtet",
        ],
    },
    {
        "version": "4.4.1",
        "date": "2026-10",
        "title": "Wachsam",
        # Erste Patch-Fassung von 4.4: die Befunde aus dem Log vom 31.10.,
        # dem ersten Lauf auf 4.4. Eigener Tag statt Ueberschreiben — der
        # Release-Workflow verschiebt beim zweiten Lauf den Tag nicht.
        "highlights": [
            "Der Kick-Chat baute knapp jede Sekunde neu auf — 11975-mal in dreieinhalb Stunden: schloss Pusher die Verbindung ordentlich, endete die Leseschleife ohne Ausnahme, und der Bot verband sofort wieder, am Flatter-Wächter vorbei. Jetzt ist auch das ordentliche Ende eine Trennung mit Backoff, und eine pusher:error-Meldung steht im Log",
            "Ein Neustart hing neun Minuten: nach dem Aufräumen wartete das Beenden auf einen Arbeiter-Thread in einem KI-Aufruf, der mit AI_TIMEOUT=0 bis zu einer Stunde dauern darf. Eine Abschiedswache beendet den Prozess jetzt nach 20 Sekunden (ABSCHIED_FRIST_S) mit dem vorgesehenen Exitcode und nennt die hängenden Threads; der Loop-Wächter meldet das Ende nicht mehr als eingefrorenen Loop",
            "Eine beschädigte brain.db stand nur als Warnung im Log, und die Sicherung enthielt sie stillschweigend nicht — jetzt ein Fehler mit dem Rettungsweg über sqlite3 .recover",
            "Die CrowdSec-Meldung ist gedrosselt (106 gleiche Zeilen in 3,5 Stunden) und nennt die Abhilfe; ein HTTP/2-Scanner steht nicht mehr im Fehlerlog",
            "Drei Plattenzugriffe laufen neben dem Event-Loop statt darauf: die Piper-Stimmensuche (4,3 s gemessen), der Token-Zähler und die Upload-Warteschlange",
        ],
    },
    {
        "version": "4.4",
        "date": "2026-10",
        "title": "Wachsam",
        # v4.4 traegt die Wellen W81 bis W132. Das gemeinsame Thema ist nicht
        # eine Funktion, sondern eine Eigenschaft: was schiefgeht, sagt es.
        # Stille Rueckgaben, stille except-Bloecke, ein Log, das den Loop
        # anhielt, Sperren, die selbst blind waren — und am Ende ein Bot, der
        # beim Neustart, beim Update und beim Tunnel meldet, woran er ist.
        "highlights": [
            "Der Event-Loop steht nicht mehr an der Logdatei: bis zu 176 Sekunden eingefrorener Bot kamen nicht aus dem Netz, sondern aus den Log-Handlern unter Plattenlast. Seit W97 schreibt ein eigener Thread, die Schlange ist begrenzt, und jeder Verlust wird gemeldet. Die Stellen, an denen der Loop sonst noch steht, nennt der Bot jetzt selbst mit Datei und Zeile",
            "Der Restream reißt beim Quellwechsel nicht mehr ab: die Sendebrücke hält die Verbindung zu Kick, Twitch und YouTube über jeden Wechsel der TikTok-Adresse und füllt die Lücke mit einem Pausenbild, statt die Plattform-Sitzung neu aufzubauen",
            "Aufnahmen verlieren beim Schnitt und beim Hänger weniger Minuten: die Sperre wird frei, sobald ffmpeg endet, nicht erst nach dem Telegram-Upload, und ein Hänger fällt nach 25 statt bis zu 105 Sekunden auf",
            "„Reste aufräumen“ konnte alle Aufnahmen löschen — ein gesperrtes SQLite genügte, und jede Datei galt als verwaist. Jetzt bricht die Funktion ab, wenn sie den Bestand nicht kennt, und die laufende Aufnahme zählt nie als Rest",
            "Ein Stream ohne Tonspur stirbt nicht mehr in einer Reconnect-Schleife: jeder ffmpeg-Bauer mappt ausdrücklich, der Restream sendet bei tonloser Quelle mit Stille, und Preflight wie Selbsttest prüfen die Ton-Garantie",
            "yt-dlp hatte die Stream-Adresse und wir lasen sie als Ja/Nein: 71 % der Auflösungen meldeten „live“ ohne Adresse. Die Adresse wird jetzt gelesen, in allen drei Formen, in denen TikTok sie liefert, und ein Wörterbuch gilt nicht mehr als URL",
            "Eine beschädigte Datenbank wird erklärt statt mit einem Einzeiler quittiert: Pfad, Größe, Kopf als Hex, Deutung und Abhilfe — und der Start legt keine leere Datenbank an. Wiederherstellung geht im Deck und ohne Bot, das WAL wird dabei mitgetauscht",
            "Das Deck bindet nicht mehr offen, wenn weder Token noch PIN gesetzt sind, läuft auf waitress statt auf dem Entwicklungsserver, und der Token verschwindet nach dem Login aus der Adresszeile",
            "Ein Update über das Deck meldet, dass es erst nach dem Neustart wirkt — in /healthz und gedrosselt im Fehlerlog, bis der Prozess wirklich neu gestartet ist",
            "Das Lagebild der Übersicht zeigt in Echtzeit, was die dreizehn Wächter gerade tun; Prometheus und Grafana sind angebunden, und der Polen-Tunnel wird alle zehn Minuten geprüft statt nur auf Knopfdruck",
            "Telegram und Discord teilen ein Befehlsverzeichnis, das lokale llama.cpp wird bevorzugt, und der Installer fragt erst, bevor er handelt — mit sechs Paketmanagern, Nutzungsprofilen und Windows-Dienst",
            "Die Prüfwerkzeuge sind selbst gegen Blindheit gesichert: stille except-Blöcke, stille Rückgaben, Riesenfunktionen, Event-Loop-Blocker, Importzeit-Lesungen der .env und Testmüll werden gezählt und dürfen nicht wachsen; die Überdeckung ist gemessen und jede neue Aussage per Mutationsprobe gegengeprüft",
            "Der Telegram-Bot-Token steht nicht mehr im Log: httpx schrieb ihn auf INFO mit jeder Anfrage in debug.log. Er wird jetzt in jeder Zeile und im Discord-Fehlerspiegel geschwärzt, ebenso ein Redis-Passwort in der Form redis://:pw@",
            "Aufnahmen gingen an eine Discord-Guild statt an Telegram, und jede wurde vorher bis 1,5 GB zerlegt, um dann an „chat not found“ zu scheitern. Nicht-Telegram-IDs werden jetzt erkannt, und ein gesperrter Chat kostet kein Zerlegen mehr",
            "Ein Restream startete zweimal gleichzeitig auf denselben Key und warf sich selbst von Kick und Twitch: jetzt läuft je Ziel nur ein Start, und der Einzel-Slot sieht auch Starts, die gerade laufen",
        ],
    },
    {
        "version": "4.3.1",
        "date": "2026-09",
        "title": "Freie Sicht",
        # Erste Patch-Fassung. 4.3 stand keinen halben Tag, dann kamen drei
        # Befunde dazu, die jeder fuer sich das Archiv erneuern rechtfertigen:
        # AZRAELs taubes Ohr, eine Funktion ohne Knopf und eine Plattform, die
        # haerter bestraft als die anderen. Eigener Tag statt Ueberschreiben —
        # der Release-Workflow verschiebt beim zweiten Lauf den Tag NICHT, das
        # Archiv haette sonst nicht mehr zu seiner Marke gepasst.
        "highlights": [
            "Der Aufnahmeschluss ist von 616 auf 455 Zeilen und von 141 auf 113 Verzweigungen — vier Blöcke in vier getrennten Wellen heraus, jeder einzeln geprüft. Der letzte war der heikelste: er wartet und schreibt in die Datenbank, und ein vergessenes await hätte die Notbremse still abgeschaltet",
            "Der Aufnahmeschluss ist von 616 auf 503 Zeilen und von 141 auf 119 Verzweigungen — drei Blöcke heraus, jeder einzeln daraufhin gemessen, dass er ohne Wirkung auf den Aufrufer ist. Die Freigabe des einen galt dabei nicht für den nächsten: derselbe Kurzname sah erst nach dem vorigen Schnitt folgenlos aus",
            "Erster Schnitt an der heikelsten Funktion des Bestands: der Aufnahmeschluss (616 Zeilen) ist auf 537 herunter. Bewusst nicht der größte Block zuerst, sondern der folgenloseste — beide herausgelösten Stücke haben nachgemessen keine Wirkung auf den Aufrufer. Der Auto-Abschalt-Block blieb ausdrücklich drin: er wartet auf Netz und schreibt in die Datenbank",
            "Die Discord-Dauerläufer sprachen nach einem Reconnect einen toten Client an: Liveboard, Wochen-Digest und Clip der Woche starten laut B120 einmalig über alle Sitzungen hinweg, hielten dabei aber die Client-Referenz der ERSTEN Sitzung fest — deren HTTP-Verbindung ist längst geschlossen. Es ist derselbe Fehler, den B120 für den Guard behoben und für die Referenz stehen gelassen hat. Sie holen ihn jetzt aus dem Register, das genau dafür da ist",
            "main() war zur Hälfte Brain-Bridge-Verdrahtung: ein einziger try-Block machte 245 der 504 Zeilen aus. Zehn Rückrufe brauchten von main keine einzige Variable und stehen jetzt auf Modulebene — 504/135 Verzweigungen wurden 293/59. Die Schattenprüfung war dabei zuerst ein Fehlalarm und hätte den Umzug verboten: das Messskript zählte Variablen innerer Funktionen der äußeren zu",
            "Das Maß für „zu große Funktion“ zeigte aufs falsche Ziel: ganz oben stand die Schema-Erzeugung mit 718 Zeilen — ausgerechnet die einfachste Funktion des Bestands, eine Liste aus 42 CREATE TABLE mit einer Verzweigung je 40 Zeilen, während jede andere Riesenfunktion eine je drei bis fünf hat. Gemessen wird jetzt beides, und die Rangliste führt die Verzweigungen an. Die Schema-Funktion bleibt bewusst ganz",
            "15 Slash-Commands waren unsichtbar: der Bot bietet 60 an, gezählt und dokumentiert waren 45. Die sys_*-Befehle entstehen in einer Schleife statt über einen Dekorator, und das Prüfwerkzeug sah nur Dekoratoren — im README standen sie in keiner Liste, obwohl eine Fußnote sie erwähnte. Wäre die Schleife weggefallen, hätte das kein Werkzeug bemerkt",
            "Die 45 Discord-Befehle haben eine Registrierung bekommen: elf kleine Funktionen statt einer Closure mit allem drin. _discord_run_once ist damit von 1730 auf 716 Zeilen (−59 %). Zwei Werkzeuge haben den Umbau unterwegs korrigiert — pyflakes stoppte ihn mit 25 Meldungen, weil app_commands entgegen der Messung gar kein Modul-Name war, und die Riesen-Sperre aus W70 meldete zwei zu groß geratene Sammelfunktionen. Beide wurden geteilt statt die Grundlinie hochzusetzen",
            "Die größte Funktion des Bestands ist zum ersten Mal kleiner geworden: _discord_run_once von 1730 auf 1560 Zeilen. Heraus gingen die Rang-Rechnung (Stufen, XP-Kurve, Kanal-Slug — jetzt bot- und discord-frei in nc/discordrang.py, die XP-Kurve stand vorher dreimal im Code) und neun Helfer, die keine einzige Closure-Variable brauchten. Dass der Umzug nichts verändert hat, ist bewiesen und nicht gehofft: die Rümpfe sind vor und nach dem Heben strukturell identisch",
            "Der Plan wollte den Monolithen zerlegen und zeigte damit auf die falsche Arbeit: in den drei genannten Riesen ist fast nichts mehr zu holen (bot.py ruft schon 674-mal in nc/ hinein), und die größte Funktion des Bestands steht gar nicht in bot.py, sondern mit 1730 Zeilen in discordbot.py — der Datei, die genau gegen dieses Problem aus bot.py herausgelöst wurde. Die Masse ist umgezogen, nicht geschrumpft. Gemessen wird jetzt der ganze Produktionscode, und keine neue Riesenfunktion kommt mehr dazu",
            "Das Diagnose-Kommando für die KI-Kette log über die Schlüssel: es stand an acht Stellen ohne load_dotenv() und zeigte deshalb IMMER „keyless“, auch bei sauber gesetzten Schlüsseln — nc/freeai ist bot-frei und lädt die .env nie selbst. Ausgerechnet die Frage, für die man es aufruft, hat es falsch beantwortet",
            "Keines der 17 Fremdpakete hatte eine Untergrenze — pip durfte auf einer älteren Maschine irgendeine Fassung auflösen, und der Fehler kam dann nicht als klare Ansage, sondern als AttributeError tief im Code an. Jede Grenze ist jetzt nachgesehen statt geschätzt: für die sechs mit API-Zwang wurde das Paket der Fassung darunter geladen und geprüft, dass die benutzte Schnittstelle dort fehlt. Dazu ein Prüfer, der Importe auch in FUNKTIONEN sieht — dort stecken boto3, redis, pymysql und httpx, und für die gab es bisher gar keine Prüfung",
            "Die API-Schlüssel aus der .env haben nie einen Request gesehen: nc/freeai.py baute seine Basen-Liste beim Import, und weil drei nc-Module das Modul in die Import-Reihe ziehen, geschah das vor load_dotenv(). Dazu strich bot.py den Katalog bedingungslos auf eine einzige Base zusammen — die Rotation gab es also gar nicht, und als Pollinations „budget exceeded“ meldete, war deshalb kein Ausweichziel da. Statt einer keylosen Base laufen jetzt vier mit ihren Schlüsseln",
            "Elf Verträge standen kurz vorm Kippen, ohne dass jemand davon wusste: sie prüfen ein Fenster fester Länge im Quelltext, und das war randvoll — der nächste Zuwachs hätte sie fallen lassen, obwohl der Code stimmt. Gemessen wurde das, indem jedes Fenster einzeln verkleinert und die Suite gefahren wurde; die elf engen laufen jetzt auf einem mitwachsenden Anker",
            "Der „Hauptfeind“ ist zum ersten Mal gezählt: 1746 except-Blöcke, davon 1086 ohne jede Meldung — jede Welle von W51 bis W64 kam aus genau dieser Klasse. Ein Werkzeug sortiert sie jetzt (Aufräumpfade und Abbruch-Signale sind legitim still) und die CI verhindert, dass die Zahl wächst",
            "AZRAEL sagte die Rechnung des KI-Anbieters im Chat auf: Pollinations meldet ein erschöpftes Budget nicht als Fehlercode, sondern als HTTP 200 mit dem Fehlertext als Antwort — samt der URL, die die Kennung des Keys trägt. Der Bot hielt das für eine Antwort, schaltete deshalb nie auf eine freie Base um und schickte den Text in den öffentlichen Chat. Jetzt wird die Meldung erkannt, die Base gesperrt und rotiert",
            "Eine manuelle Aufnahme war nach dem Start unsichtbar und nicht abbrechbar: sie liegt in einer eigenen Tabelle, das Panel AKTIVE AUFNAHMEN liest aber eine andere — das Deck antwortete auf einen erfolgreichen Start mit „Keine laufende Aufnahme.“. Jetzt gibt es eine Liste mit Zustand, Größe und Stop-Knopf",
            "AZRAEL hat eine dritte Haltung: bleibt der Chat anderthalb Minuten still, senkt er Kinn und Klingenspitze, dimmt die Glut und blinzelt alle drei Sekunden. Vorher kannte er genau zwei Bilder von sich — reden oder dieselben drei Sekunden, stundenlang, und das sieht im Sendebild aus wie ein abgestürzter Restream",
            "Muss die Notbremse doch etwas aus dem Bild nehmen, dann den Avatar — nie das Panel: der Chat läuft weiter, AZRAELs Antwort steht weiter im Wortlaut da und seine Stimme bleibt hörbar. Weg ist nur das Gesicht dazu. Gemessen bringt der Schritt 14 Prozentpunkte, die Leinwandverkleinerung davor null — deshalb steht der Avatar jetzt vor ihr",
            "Aus dem Sendebild fällt nichts mehr heraus: die Notbremse gegen Encode-Rückstand warf ab ihrer dritten Stufe das komplette Panel weg — Chat, Titel, Quelle — und behielt ausgerechnet den Avatar, der gemessen mehr kostet als sämtliche Texte zusammen. Sie regelt jetzt nur noch Preset, Bitrate, Bildrate und Leinwandgröße",
            "AZRAEL antwortet wieder auf jeder Plattform: alle drei Chats teilten sich EINEN Antwort-Cooldown, eine Frage auf Kick verschluckte damit die Fragen auf Twitch und YouTube für zwanzig Sekunden — stumm, ohne Log",
            "AZRAELs Ohr war aus demselben Grund taub wie der Recorder blind: ohne Stream-URL kein Audio-Abgriff, ohne Abgriff kein Transkript — gemeldet hat das Log davon nur „audio=False“, ein Wort für drei mögliche Ursachen. Jetzt nennt es die Ursache und meldet sie als Warnung statt als Beiwerk",
            "Aufnahme-Sitzungen haben endlich eine Oberfläche: die Funktion, die einen zerstückelten Stream auf Knopfdruck zu einer Datei zusammenfügt, gab es seit W44 nur als Schnittstelle — der versprochene Knopf fehlte. Jetzt zeigt die Betrieb-Ansicht je Sitzung Segmente, Nahtlücken und Abdeckung, und fügt auf Klick zusammen",
            "Auf YouTube gab es für denselben Verstoß sofort eine Auszeit, während Kick und Twitch erst verwarnen — die Moderation läuft auf allen drei Plattformen, nur dieser eine Schritt fehlte dort",
        ],
    },
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
            "Der Zweitversuch der Live-Abfrage nahm nicht, wie der Code behauptete, einen frischen Proxy, sondern bei fester Proxy-Einstellung immer denselben — jede Live-Prüfung war damit zwei gleiche Anfragen mit einer halben Sekunde Pause dazwischen, gegen einen Endpunkt, der ohnehin schon mit 502 ablehnte",
            "Wenn die Stream-Adresse nicht aufzulösen ist, steht jetzt im Log, WARUM: die Auflösung hatte elf Wege, ergebnislos zu enden, acht davon nur auf der Entwickler-Stufe und drei ganz wortlos — der Chat verband sich, der Recorder fand nichts, und die Ursache (meist eine geblockte Server-IP) war nicht zu ermitteln. Dasselbe für das leere Transkript: auch Whisper verschluckte jeden Fehler. Beides meldet sich jetzt im Klartext samt Abhilfe, aber gedrosselt — sonst wäre das Log nach einer Stunde unlesbar",
            "Der Chat steht im Sendebild wieder vorn: der Avatar lag über der halben rechten Spalte, und die Zeilen liefen zusätzlich rechts aus dem Bild, weil die Umbruchbreite eine feste Zahl für eine Schrift mit fester Zeichenbreite war — die Schrift ist aber proportional. Beides rechnet jetzt aus der Panel-Geometrie",
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
