"""nc.tiktokheaders — v4.1-W23: die Kopfzeilen fuer TikTok-Abrufe.

Ein Browser-Fingerabdruck, kein Geheimnis: TikTok liefert ohne plausible
Kopfzeilen eine andere Seite aus (oder gar keine), und der Aufloeser findet
dann keine Stream-URL. Deshalb stehen sie vollstaendig da statt "irgendein
User-Agent" — jede einzelne Zeile hat schon einmal den Unterschied zwischen
"live gefunden" und "offline" gemacht.

Sie lagen als Modul-Global in bot.py. Hierher geloest, damit
nc/routes/beobachtung.py sie ohne Kontext-Eintrag erreicht; die
Accept-Encoding-Zeile kommt per configure(), weil sie davon abhaengt, ob
Brotli installiert ist (siehe die Warnung beim Bot-Start).
"""

_ACCEPT_ENCODING = "gzip, deflate"


def configure(*, accept_encoding=None):
    """Der Bot reicht sein tatsaechliches Accept-Encoding herein — ohne
       Brotli darf hier kein 'br' stehen, sonst kommt eine Antwort zurueck,
       die niemand auspacken kann."""
    global _ACCEPT_ENCODING
    if accept_encoding:
        _ACCEPT_ENCODING = accept_encoding
        HEADERS["Accept-Encoding"] = accept_encoding


HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/131.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,"
              "image/avif,image/webp,image/apng,*/*;q=0.8",
    "Accept-Language": "de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7",
    "Accept-Encoding": _ACCEPT_ENCODING,
    "Referer": "https://www.tiktok.com/",
    "sec-ch-ua": '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "same-origin",
    "sec-fetch-user": "?1",
    "upgrade-insecure-requests": "1",
    "Connection": "keep-alive",
}
