# bot.py
import logging
import sqlite3
import time
import httpx
import os
import traceback
import numpy as np
from datetime import datetime, time as dt_time
from openai import OpenAI
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
    MessageHandler,
    filters,
    AIORateLimiter
)
from dotenv import load_dotenv

# Konfiguration
load_dotenv()
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TWITCH_CLIENT_ID = os.getenv("TWITCH_CLIENT_ID")
TWITCH_CLIENT_SECRET = os.getenv("TWITCH_CLIENT_SECRET")
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
DB_FILE = os.getenv("DB_FILE", "streams.db")
ADMIN_CHAT_ID = os.getenv("ADMIN_CHAT_ID")

# Logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
    handlers=[logging.FileHandler("bot.log"), logging.StreamHandler()],
)
logger = logging.getLogger(__name__)

# Datenbank-Initialisierung
def init_db():
    try:
        with sqlite3.connect(DB_FILE) as conn:
            conn.executescript("""
            CREATE TABLE IF NOT EXISTS tracked_streams (
                chat_id TEXT,
                streamer TEXT,
                user_id TEXT,
                platform TEXT DEFAULT 'twitch',
                last_status BOOLEAN,
                added_at TEXT,
                last_stream_start TEXT,
                last_stream_end TEXT,
                peak_viewers INTEGER DEFAULT 0,
                total_stream_time INTEGER DEFAULT 0,
                PRIMARY KEY (chat_id, streamer, platform)
            );
            
            CREATE TABLE IF NOT EXISTS rate_limits (
                chat_id TEXT,
                command TEXT,
                count INTEGER,
                reset_ts REAL,
                PRIMARY KEY (chat_id, command)
            );
            
            CREATE TABLE IF NOT EXISTS api_usage (
                date TEXT PRIMARY KEY,
                youtube_units INTEGER DEFAULT 0
            );
            
            CREATE TABLE IF NOT EXISTS user_settings (
                user_id TEXT PRIMARY KEY,
                theme TEXT DEFAULT 'dark'
            );
            
            CREATE TABLE IF NOT EXISTS stream_stats (
                streamer TEXT,
                start_time TEXT,
                end_time TEXT,
                duration INTEGER
            );
            """)
            logger.info("Datenbank initialisiert")
    except Exception as e:
        logger.critical(f"DB init error: {e}")
        raise

# Error-Handler
async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    logger.error("Fehler:", exc_info=context.error)
    if ADMIN_CHAT_ID:
        error_msg = f"⚠️ **Bot-Fehler**\n```\n{traceback.format_exc()}\n```"
        await context.bot.send_message(
            chat_id=int(ADMIN_CHAT_ID),
            text=error_msg[:4096],  # Telegram Nachrichtenlimit
            parse_mode="Markdown"
        )

# Twitch-API
CACHED_TWITCH_TOKEN = None
TWITCH_TOKEN_EXPIRY = 0

async def get_twitch_token():
    global CACHED_TWITCH_TOKEN, TWITCH_TOKEN_EXPIRY
    if time.time() < TWITCH_TOKEN_EXPIRY and CACHED_TWITCH_TOKEN:
        return CACHED_TWITCH_TOKEN
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://id.twitch.tv/oauth2/token",
                params={
                    "client_id": TWITCH_CLIENT_ID,
                    "client_secret": TWITCH_CLIENT_SECRET,
                    "grant_type": "client_credentials",
                },
            )
            data = response.json()
            CACHED_TWITCH_TOKEN = data["access_token"]
            TWITCH_TOKEN_EXPIRY = time.time() + data["expires_in"] - 60
            return CACHED_TWITCH_TOKEN
    except Exception as e:
        logger.error(f"Twitch-Token-Fehler: {e}")
        return None

async def get_twitch_user_id(name: str):
    token = await get_twitch_token()
    if not token:
        return None
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                "https://api.twitch.tv/helix/users",
                headers={"Client-ID": TWITCH_CLIENT_ID, "Authorization": f"Bearer {token}"},
                params={"login": name},
            )
            return response.json()["data"][0]["id"] if response.json().get("data") else None
    except Exception as e:
        logger.error(f"Twitch-User-ID-Fehler: {e}")
        return None

async def get_twitch_clip(user_id: str):
    token = await get_twitch_token()
    if not token:
        return None
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                "https://api.twitch.tv/helix/clips",
                headers={"Client-ID": TWITCH_CLIENT_ID, "Authorization": f"Bearer {token}"},
                params={"broadcaster_id": user_id, "first": 1},
            )
            return response.json()["data"][0]["url"] if response.json().get("data") else None
    except Exception as e:
        logger.error(f"Twitch-Clip-Fehler: {e}")
        return None

# YouTube-API
class YouTubeQuota:
    @staticmethod
    def _today():
        return datetime.utcnow().strftime("%Y-%m-%d")

    @classmethod
    def add_usage(cls, units: int):
        today = cls._today()
        with sqlite3.connect(DB_FILE) as conn:
            conn.execute(
                "INSERT INTO api_usage (date, youtube_units) VALUES (?, ?)"
                "ON CONFLICT(date) DO UPDATE SET youtube_units = youtube_units + ?",
                (today, units, units),
            )

    @classmethod
    def get_remaining(cls):
        today = cls._today()
        with sqlite3.connect(DB_FILE) as conn:
            row = conn.execute(
                "SELECT youtube_units FROM api_usage WHERE date = ?", (today,)
            ).fetchone()
            used = row[0] if row else 0
        return max(10000 - used, 0)

async def get_youtube_channel_id(name: str):
    if YouTubeQuota.get_remaining() < 100:
        logger.warning("YouTube-Kontingent erschöpft")
        return None
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                "https://www.googleapis.com/youtube/v3/search",
                params={
                    "part": "snippet",
                    "q": name,
                    "type": "channel",
                    "key": YOUTUBE_API_KEY,
                    "maxResults": 1,
                },
            )
            YouTubeQuota.add_usage(100)
            data = response.json()
            return data["items"][0]["id"]["channelId"] if data.get("items") else None
    except Exception as e:
        logger.error(f"YouTube-Kanal-Fehler: {e}")
        return None

async def check_youtube_live(channel_id: str):
    if YouTubeQuota.get_remaining() < 100:
        logger.warning("YouTube API Quota erschöpft - überspringe Check")
        return None
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                "https://www.googleapis.com/youtube/v3/search",
                params={
                    "part": "snippet",
                    "channelId": channel_id,
                    "eventType": "live",
                    "type": "video",
                    "key": YOUTUBE_API_KEY,
                },
            )
            YouTubeQuota.add_usage(100)
            return response.json().get("items", [])[0] if response.json().get("items") else None
    except Exception as e:
        logger.error(f"YouTube-Live-Check-Fehler: {e}")
        return None

# Rate-Limiting
def rate_limited(command: str, max_requests=5, period=30):
    def decorator(func):
        async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
            if not update.message:
                return
            chat_id = str(update.message.chat.id)
            now = time.time()
            with sqlite3.connect(DB_FILE) as conn:
                row = conn.execute(
                    "SELECT count, reset_ts FROM rate_limits WHERE chat_id = ? AND command = ?",
                    (chat_id, command),
                ).fetchone()
                if row:
                    count, reset_ts = row
                    if now > reset_ts:
                        count = 0
                        reset_ts = now + period
                    if count >= max_requests:
                        await update.message.reply_text("🚫 Zu viele Anfragen. Bitte warte 30 Sekunden.")
                        return
                    count += 1
                else:
                    count = 1
                    reset_ts = now + period
                conn.execute(
                    "INSERT OR REPLACE INTO rate_limits (chat_id, command, count, reset_ts) VALUES (?, ?, ?, ?)",
                    (chat_id, command, count, reset_ts),
                )
            return await func(update, context)
        return wrapper
    return decorator

# Befehle
@rate_limited("track")
async def track(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not context.args or len(context.args) < 2:
        await update.message.reply_text("❌ Format: /track <twitch|youtube> <name>")
        return

    platform = context.args[0].lower()
    name = " ".join(context.args[1:]).lower()

    if platform not in ["twitch", "youtube"]:
        await update.message.reply_text("❌ Ungültige Plattform. Nur 'twitch' oder 'youtube'.")
        return

    if platform == "youtube" and YouTubeQuota.get_remaining() < 100:
        await update.message.reply_text("❌ YouTube-Kontingent erschöpft. Bitte später versuchen.")
        return

    user_id = await (get_twitch_user_id(name) if platform == "twitch" else get_youtube_channel_id(name))
    if not user_id:
        await update.message.reply_text("❌ Kanal nicht gefunden.")
        return

    with sqlite3.connect(DB_FILE) as conn:
        conn.execute(
            """
            INSERT OR IGNORE INTO tracked_streams 
            (chat_id, streamer, user_id, platform, last_status, added_at)
            VALUES (?, ?, ?, ?, 0, ?)
            """,
            (str(update.message.chat.id), name, user_id, platform, datetime.utcnow().isoformat()),
        )
    await update.message.reply_text(f"✅ {name} ({platform}) wird nun überwacht.")

@rate_limited("untrack")
async def untrack(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not context.args or len(context.args) < 2:
        await update.message.reply_text("❌ Format: /untrack <twitch|youtube> <name>")
        return

    platform = context.args[0].lower()
    name = " ".join(context.args[1:]).lower()

    with sqlite3.connect(DB_FILE) as conn:
        cur = conn.execute(
            "DELETE FROM tracked_streams WHERE chat_id = ? AND streamer = ? AND platform = ?",
            (str(update.message.chat.id), name, platform)
        )
    
    if cur.rowcount:
        await update.message.reply_text(f"🗑 {name} ({platform}) entfernt.")
    else:
        await update.message.reply_text(f"❌ {name} ({platform}) nicht gefunden.")

async def untrack_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    _, streamer, platform = query.data.split(":")
    chat_id = str(query.message.chat.id)
    with sqlite3.connect(DB_FILE) as conn:
        cur = conn.execute(
            "DELETE FROM tracked_streams WHERE chat_id = ? AND streamer = ? AND platform = ?",
            (chat_id, streamer, platform),
        )
    if cur.rowcount:
        await query.edit_message_text(f"✅ {streamer} ({platform}) entfernt.")
    else:
        await query.answer("❌ Konnte nicht entfernt werden.")
    await query.answer()

async def list_streams(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = str(update.message.chat.id)
    with sqlite3.connect(DB_FILE) as conn:
        streams = conn.execute(
            "SELECT streamer, platform, last_status, user_id FROM tracked_streams WHERE chat_id = ?",
            (chat_id,),
        ).fetchall()

    if not streams:
        await update.message.reply_text("🔍 Keine Streamer registriert.")
        return

    keyboard = []
    for streamer, platform, status, user_id in streams:
        if platform == "twitch":
            url = f"https://twitch.tv/{streamer}"
        else:
            url = f"https://youtube.com/channel/{user_id}"
            
        button = InlineKeyboardButton(
            text=f"{'🎮' if platform == 'twitch' else '📺'} {streamer} {'🟢' if status else '🔴'}",
            url=url
        )
        keyboard.append([button])

    await update.message.reply_text(
        "🎥 Registrierte Streamer (Tippe um zu öffnen):",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# KI-Funktionen
client = OpenAI(api_key=OPENAI_API_KEY)

async def recommend_streamers(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = str(update.message.chat.id)
    with sqlite3.connect(DB_FILE) as conn:
        tracked = conn.execute(
            "SELECT streamer FROM tracked_streams WHERE chat_id = ?",
            (chat_id,)
        ).fetchall()
    
    if not tracked:
        await update.message.reply_text("❌ Keine Streamer zum Analysieren vorhanden")
        return
    
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{
            "role": "system",
            "content": f"Empfehle 5 ähnliche Streamer wie {', '.join([t[0] for t in tracked])}. Antwortformat: '1. Name - Plattform - Beschreibung'"
        }]
    )
    await update.message.reply_text(f"🎮 KI-Empfehlungen:\n{response.choices[0].message.content}")

async def generate_thumbnail(title: str):
    response = client.images.generate(
        model="dall-e-3",
        prompt=f"Stream-Thumbnail im Gaming-Stil: {title}",
        size="1024x1024"
    )
    return response.data[0].url

# Zusätzliche Features
async def tutorial(update: Update, context: ContextTypes.DEFAULT_TYPE):
    steps = [
        ("tutorial1.jpg", "Schritt 1: Nutze /track <plattform> <name>"),
        ("tutorial2.jpg", "Schritt 2: Erhalte Live-Benachrichtigungen")
    ]
    
    media_group = [
        InputMediaPhoto(media=open(file, "rb"), caption=text)
        for file, text in steps
    ]
    
    await context.bot.send_media_group(
        chat_id=update.effective_chat.id,
        media=media_group
    )

def predict_next_live(streamer: str):
    with sqlite3.connect(DB_FILE) as conn:
        times = conn.execute(
            "SELECT strftime('%H:%M', last_stream_start) FROM tracked_streams WHERE streamer=?",
            (streamer,)
        ).fetchall()
    
    if not times:
        return "⚠️ Keine Stream-Daten vorhanden"
    
    avg_time = np.median([datetime.strptime(t[0], "%H:%M") for t in times])
    return f"⏱️ Voraussichtlich nächster Stream: {avg_time.strftime('%H:%M')}"

# Hauptlogik
async def check_streams(context: ContextTypes.DEFAULT_TYPE):
    logger.info("🚀 Starte Stream-Check...")
    try:
        with sqlite3.connect(DB_FILE) as conn:
            tracked = conn.execute(
                "SELECT chat_id, streamer, user_id, platform, last_status, last_stream_start FROM tracked_streams"
            ).fetchall()

        # Twitch-Check
        twitch_streams = [s for s in tracked if s[3] == "twitch"]
        if twitch_streams:
            user_ids = [s[2] for s in twitch_streams]
            token = await get_twitch_token()
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    "https://api.twitch.tv/helix/streams",
                    headers={"Client-ID": TWITCH_CLIENT_ID, "Authorization": f"Bearer {token}"},
                    params={"user_id": user_ids},
                )
                live_data = {stream["user_id"]: stream for stream in response.json().get("data", [])}

            updates_start = []
            updates_end = []
            for chat_id, streamer, user_id, platform, status, last_start in twitch_streams:
                stream_info = live_data.get(user_id)
                is_live = stream_info is not None
                if is_live and not status:
                    clip = await get_twitch_clip(user_id)
                    keyboard = [
                        [InlineKeyboardButton("🔴 LIVE", url=f"https://twitch.tv/{streamer}")],
                        [InlineKeyboardButton("📊 Stats", callback_data=f"stats_{streamer}")]
                    ]
                    if clip:
                        keyboard.append([InlineKeyboardButton("🎬 Clip", url=clip)])
                    await context.bot.send_photo(
                        chat_id=chat_id,
                        photo=stream_info["thumbnail_url"].replace("{width}", "640").replace("{height}", "360"),
                        caption=f"🎮 {streamer} ist LIVE auf Twitch!\n{stream_info.get('title', '')}",
                        reply_markup=InlineKeyboardMarkup(keyboard)
                    )
                    updates_start.append((1, datetime.utcnow().isoformat(), stream_info["viewer_count"], chat_id, streamer, platform))
                elif not is_live and status:
                    dur = (datetime.utcnow() - datetime.fromisoformat(last_start)).total_seconds() if last_start else 0
                    updates_end.append((0, datetime.utcnow().isoformat(), dur, chat_id, streamer, platform))
                    await context.bot.send_message(
                        chat_id=chat_id,
                        text=f"🌙 {streamer} (Twitch) offline. Dauer: {int(dur // 60)} Minuten"
                    )

            with sqlite3.connect(DB_FILE) as conn:
                conn.executemany(
                    "UPDATE tracked_streams SET last_status=?, last_stream_start=?, peak_viewers=? WHERE chat_id=? AND streamer=? AND platform=?",
                    updates_start
                )
                conn.executemany(
                    "UPDATE tracked_streams SET last_status=?, last_stream_end=?, total_stream_time=total_stream_time+? WHERE chat_id=? AND streamer=? AND platform=?",
                    [(u[0], u[1], u[2], u[3], u[4], u[5]) for u in updates_end]
                )

        # YouTube-Check
        youtube_streams = [s for s in tracked if s[3] == "youtube"]
        if youtube_streams and YouTubeQuota.get_remaining() >= 100 * len(youtube_streams):
            for chat_id, streamer, channel_id, platform, status, last_start in youtube_streams:
                live_info = await check_youtube_live(channel_id)
                is_live = live_info is not None
                if is_live and not status:
                    video_id = live_info["id"]["videoId"]
                    await context.bot.send_message(
                        chat_id=chat_id,
                        text=f"🎥 {streamer} ist LIVE auf YouTube!\n{live_info['snippet']['title']}\nhttps://youtu.be/{video_id}"
                    )
                    with sqlite3.connect(DB_FILE) as conn:
                        conn.execute(
                            "UPDATE tracked_streams SET last_status=1, last_stream_start=? WHERE chat_id=? AND streamer=? AND platform=?",
                            (datetime.utcnow().isoformat(), chat_id, streamer, platform)
                        )
                elif not is_live and status:
                    dur = (datetime.utcnow() - datetime.fromisoformat(last_start)).total_seconds() if last_start else 0
                    await context.bot.send_message(
                        chat_id=chat_id,
                        text=f"🌙 {streamer} (YouTube) offline. Dauer: {int(dur // 60)} Minuten"
                    )
                    with sqlite3.connect(DB_FILE) as conn:
                        conn.execute(
                            "UPDATE tracked_streams SET last_status=0, last_stream_end=?, total_stream_time=total_stream_time+? WHERE chat_id=? AND streamer=? AND platform=?",
                            (datetime.utcnow().isoformat(), dur, chat_id, streamer, platform)
                        )
        elif youtube_streams:
            logger.warning("YouTube API Quota reicht nicht für alle Checks")

        logger.info("✅ Stream-Check abgeschlossen")
    except Exception as e:
        logger.error(f"Stream-Check-Fehler: {e}")
        traceback.print_exc()

def schedule_report(app):
    async def daily_report(context: ContextTypes.DEFAULT_TYPE):
        if ADMIN_CHAT_ID:
            with sqlite3.connect(DB_FILE) as conn:
                rows = conn.execute(
                    "SELECT streamer, SUM(total_stream_time) FROM tracked_streams GROUP BY streamer ORDER BY SUM(total_stream_time) DESC LIMIT 5"
                ).fetchall()
            report = "📊 **Top 5 Streamer**\n" + "\n".join(
                f"• {streamer}: {int(total // 3600)}h {int((total % 3600) // 60)}m"
                for streamer, total in rows
            )
            await context.bot.send_message(chat_id=ADMIN_CHAT_ID, text=report, parse_mode="Markdown")
    app.job_queue.run_daily(daily_report, time=dt_time(hour=8, minute=0))

def main():
    init_db()
    application = ApplicationBuilder().token(TELEGRAM_TOKEN).rate_limiter(AIORateLimiter()).build()
    
    # Handler registrieren
    application.add_handler(CommandHandler("track", track))
    application.add_handler(CommandHandler("untrack", untrack))
    application.add_handler(CommandHandler("list", list_streams))
    application.add_handler(CommandHandler("recommend", recommend_streamers))
    application.add_handler(CommandHandler("tutorial", tutorial))
    application.add_handler(CallbackQueryHandler(untrack_callback, pattern="^untrack:"))
    application.add_error_handler(error_handler)
    
    application.job_queue.run_repeating(check_streams, interval=60, first=10)
    schedule_report(application)
    
    logger.info("🤖 Bot startet...")
    application.run_polling()

if __name__ == "__main__":
    main()