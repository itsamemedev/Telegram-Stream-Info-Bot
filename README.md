# Stream Monitor Bot

Telegram-Bot zur Überwachung von Twitch- und YouTube-Livestreams mit Live-Benachrichtigungen und Statistiken.

## 📥 Installation (Debian/Ubuntu)

### Voraussetzungen
```bash
sudo apt update && sudo apt install -y python3 python3-pip sqlite3

Schritt-für-Schritt Einrichtung

    Repository klonen:

bash

git clone https://github.com/itsamemedev/Telegram-Stream-Info-Bot
cd Telegram-Stream-Info-Bot

    Abhängigkeiten installieren:

bash

pip3 install -r requirements.txt

    Umgebungsvariablen konfigurieren:

bash

cp .env.example .env
nano .env  # Trage deine API-Keys ein

    Datenbank initialisieren:

bash

python3 bot.py --init-db

🚀 Nutzung
Befehlsreferenz
Befehl	Aktion	Beispiel
/track <pl> <name>	Streamer hinzufügen	/track youtube MrBeast
/untrack <pl> <name>	Streamer entfernen	/untrack twitch shroud
/list	Alle Streamer anzeigen	/list
/help	Hilfemenü öffnen	/help
Funktionsweise

    🔄 Automatische Überprüfung alle 60 Sekunden

    📸 Twitch-Benachrichtigungen mit Thumbnail + Clip-Button

    📊 Statistik-Tracking (Stream-Dauer, Peak-Zuschauer)

    ⚠️ Rate-Limiting: 5 Anfragen/30 Sekunden pro Chat

📜 Lizenz

MIT-Lizenz – Details siehe LICENSE.

Hinweis:

    Erforderliche API-Keys: Telegram, Twitch, YouTube

    Starten des Bots: python3 bot.py
 
Hinweise zur Beschaffung der Keys:

    Telegram Token: Erstelle einen Bot über @BotFather

    Twitch Keys: Registriere eine App unter Twitch Dev Console

    YouTube API Key: Erstelle ein Projekt in der Google Cloud Console

    Admin Chat ID: Sende /start an @userinfobot um deine Chat-ID zu erhalten