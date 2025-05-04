# Telegram Stream Monitor Bot 🤖

Ein leistungsstarker Telegram-Bot zur Überwachung von Twitch- und YouTube-Streams mit Live-Benachrichtigungen, Statistiken und KI-Integration.

[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Python 3.9+](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://www.python.org/)

![Bot Demo](https://via.placeholder.com/800x400.png?text=Bot+Demo+Preview)

## ✨ Funktionen

- 🔔 **Live-Benachrichtigungen** für Twitch & YouTube
- 📊 **Stream-Statistiken** (Dauer, Zuschauerrekorde)
- 🧠 **KI-Integration**: Streamer-Empfehlungen (GPT-4), Thumbnail-Generierung (DALL-E 3)
- 💸 **Spendenunterstützung** mit PayPal & GoFundMe
- ⚡ **Echtzeit-Checks** alle 60 Sekunden
- 🛡️ **Rate-Limiting** gegen Missbrauch
- 📈 **Datenbankunterstützung** (SQLite)
- 🔄 **Automatisches Error-Recovery**

## 🚀 Installation

### Voraussetzungen
- Python 3.9+
- Telegram-Bot-Token ([@BotFather](https://t.me/BotFather))
- API-Keys für [Twitch](https://dev.twitch.tv/) & [YouTube](https://console.cloud.google.com/)


# Repository klonen
git clone https://github.com/dein-benutzername/telegram-stream-bot.git
cd telegram-stream-bot

# Virtuelle Umgebung erstellen
python3 -m venv venv
source venv/bin/activate

# Abhängigkeiten installieren
pip install -r requirements.txt

## ⚙️ Konfiguration

    .env-Datei erstellen:

ini

TELEGRAM_TOKEN="dein_telegram_token"
TWITCH_CLIENT_ID="dein_twitch_client_id"
TWITCH_CLIENT_SECRET="dein_twitch_secret"
YOUTUBE_API_KEY="dein_youtube_key"
OPENAI_API_KEY="dein_openai_key"  # Optional für KI-Features
DONATION_LINK="https://gofundme.com/dein-projekt"
PAYPAL_ME="https://paypal.me/dein-account"

##     Datenbank initialisieren:

bash

python3 -c "from bot import init_db; init_db()"

## 🕹️ Nutzung
Befehl	Beschreibung	Beispiel
/track <pl> <name>	Streamer hinzufügen	/track youtube MrBeast
/untrack <pl> <name>	Streamer entfernen	/untrack twitch shroud
/list	Alle Streamer anzeigen	/list
/donate	Spendenmöglichkeiten anzeigen	/donate
/recommend	KI-Empfehlungen erhalten	/recommend
## ❤️ Unterstützung

Unterstütze dieses Projekt:

    PayPal

    GoFundMe

Jede Spende hilft bei der Weiterentwicklung!

## 🤝 Beitragen

 -   Fork das Repository

 -   Erstelle einen Feature-Branch: git checkout -b feature/mein-feature

 -   Commite deine Änderungen: git commit -m 'Add awesome feature'

 -   Pushe den Branch: git push origin feature/mein-feature

 -   Öffne einen Pull Request

## 📄 Lizenz

Dieses Projekt ist unter der MIT-Lizenz lizenziert.