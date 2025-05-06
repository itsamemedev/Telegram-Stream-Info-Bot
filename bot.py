# bot.py
import logging
import sqlite3
import time
import httpx
import os
import traceback
import numpy as np
import asyncio
from datetime import datetime, time as dt_time
from typing import Optional, List, Dict
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
from cachetools import TTLCache
from openai import OpenAI

# Konfiguration
load_dotenv()
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TWITCH_CLIENT_ID = os.getenv("TWITCH_CLIENT_ID")
TWITCH_CLIENT_SECRET = os.getenv("TWITCH_CLIENT_SECRET")
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
DONATION_LINK = os.getenv("DONATION_LINK", "https://gofundme.com/your-project")
PAYPAL_ME = os.getenv("PAYPAL_ME", "https://paypal.me/your-account")
DB_FILE = os.getenv("DB_FILE", "streams.db")
ADMIN_CHAT_ID = os.getenv("ADMIN_CHAT_ID")

# Logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
    handlers=[
        logging.FileHandler("bot.log", mode="a", encoding="utf-8"),
        logging.StreamHandler()
    ],
)
logger = logging.getLogger(__name__)

# Error-Handler
async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    logger.error("Exception occurred:", exc_info=context.error)
    
    error_msg = (
        f"⚠️ **Unbehandelter Fehler**\n"
        f"Update: {update}\n"
        f"Context: {context}\n"
        f"Error: {context.error}"
    )
    
    if ADMIN_CHAT_ID:
        await context.bot.send_message(
            chat_id=ADMIN_CHAT_ID,
            text=error_msg[:4096],
            parse_mode="Markdown"
        )
    
    if update and hasattr(update, 'message'):
        await update.message.reply_text("❌ Ein unerwarteter Fehler ist aufgetreten")

# Caching
cache = TTLCache(maxsize=1000, ttl=300)

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
            
            CREATE TABLE IF NOT EXISTS donations (
                donor_id TEXT PRIMARY KEY,
                amount REAL,
                donation_date TEXT
            );
            
            CREATE TABLE IF NOT EXISTS user_settings (
                user_id TEXT PRIMARY KEY,
                theme TEXT DEFAULT 'dark'
            );""")
            logger.info("Datenbank initialisiert")
    except Exception as e:
        logger.critical(f"DB init error: {e}")
        raise

# Twitch-Service
class TwitchService:
    _token = None
    _token_expiry = 0
    _cache = TTLCache(maxsize=500, ttl=3600)

    @classmethod
    async def get_user_id(cls, name: str) -> Optional[str]:
        cache_key = f"twitch_user_{name}"
        if cached := cls._cache.get(cache_key):
            return cached
            
        token = await cls._get_token()
        if not token:
            return None

        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    "https://api.twitch.tv/helix/users",
                    headers={
                        "Client-ID": TWITCH_CLIENT_ID,
                        "Authorization": f"Bearer {token}"
                    },
                    params={"login": name},
                    timeout=10
                )
                response.raise_for_status()
                if data := response.json().get("data"):
                    cls._cache[cache_key] = data[0]["id"]
                    return data[0]["id"]
        except Exception as e:
            logger.error(f"Twitch API Error: {e}")
        return None

    @classmethod
    async def _get_token(cls):
        if time.time() < cls._token_expiry and cls._token:
            return cls._token
            
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    "https://id.twitch.tv/oauth2/token",
                    params={
                        "client_id": TWITCH_CLIENT_ID,
                        "client_secret": TWITCH_CLIENT_SECRET,
                        "grant_type": "client_credentials",
                    },
                    timeout=5
                )
                data = response.json()
                cls._token = data["access_token"]
                cls._token_expiry = time.time() + data["expires_in"] - 60
                return cls._token
        except Exception as e:
            logger.critical(f"Twitch Token Error: {e}")
            return None

# YouTube-Service
class YouTubeService:
    _quota_cache = TTLCache(maxsize=1, ttl=60)
    _last_quota_check = datetime.utcnow().date()

    @classmethod
    async def get_channel_id(cls, name: str) -> Optional[str]:
        cache_key = f"youtube_channel_{name}"
        if cached := cache.get(cache_key):
            return cached

        if await cls._check_quota() < 100:
            logger.warning("Kontingent erschöpft für Channel ID Abfrage")
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
                    timeout=15
                )
                response.raise_for_status()
                
                if items := response.json().get("items"):
                    channel_id = items[0]["id"]["channelId"]
                    await cls._update_quota(100)
                    cache[cache_key] = channel_id
                    return channel_id
        except Exception as e:
            logger.error(f"YouTube Channel ID Error: {e}")
        return None

    @classmethod
    async def check_live(cls, channel_id: str) -> Optional[dict]:
        if await cls._check_quota() < 100:
            logger.warning("Kontingent erschöpft für Live-Check")
            return None

        for attempt in range(3):
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
                        timeout=15
                    )
                    response.raise_for_status()
                    
                    if items := response.json().get("items"):
                        await cls._update_quota(100)
                        return items[0]
                    return None
            except httpx.HTTPStatusError as e:
                if e.response.status_code == 403:
                    await cls._update_quota(5)
                    return await cls._fallback_check(channel_id)
                logger.error(f"YouTube API Error: {e}")
                await asyncio.sleep(2 ** attempt)
            except Exception as e:
                logger.error(f"YouTube Check Error: {e}")
                return None
        return None

    @classmethod
    async def _fallback_check(cls, channel_id: str) -> bool:
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"https://www.youtube.com/channel/{channel_id}/live",
                    headers={"User-Agent": "Mozilla/5.0"},
                    follow_redirects=True,
                    timeout=10
                )
                return "isLiveBroadcast" in response.text
        except Exception as e:
            logger.error(f"YouTube Fallback Error: {e}")
            return False

    @classmethod
    async def _check_quota(cls) -> int:
        today = datetime.utcnow().date()
        if today != cls._last_quota_check:
            cls._quota_cache.clear()
            cls._last_quota_check = today

        with sqlite3.connect(DB_FILE) as conn:
            row = conn.execute(
                "SELECT youtube_units FROM api_usage WHERE date = ?", 
                (today.isoformat(),)
            ).fetchone()
            used = row[0] if row else 0
            return max(10000 - used, 0)

    @classmethod
    async def _update_quota(cls, units: int):
        today = datetime.utcnow().isoformat()[:10]
        with sqlite3.connect(DB_FILE) as conn:
            conn.execute("BEGIN TRANSACTION")
            try:
                conn.execute(
                    """INSERT INTO api_usage (date, youtube_units)
                    VALUES (?, ?)
                    ON CONFLICT(date) DO UPDATE SET
                    youtube_units = youtube_units + ?""",
                    (today, units, units)
                )
                conn.commit()
            except Exception as e:
                conn.rollback()
                logger.error(f"Quota update failed: {e}")

# Rate-Limiting Decorator
def rate_limited(command: str, max_requests: int = 5, period: int = 30):
    def decorator(func):
        async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
            if not update.message:
                return

            chat_id = str(update.message.chat.id)
            now = time.time()
            
            with sqlite3.connect(DB_FILE) as conn:
                cursor = conn.execute(
                    "SELECT count, reset_ts FROM rate_limits WHERE chat_id = ? AND command = ?",
                    (chat_id, command)
                )
                result = cursor.fetchone()

                if result:
                    count, reset_ts = result
                    if now > reset_ts:
                        count = 0
                        reset_ts = now + period
                    if count >= max_requests:
                        await update.message.reply_text(
                            f"🚫 Zu viele Anfragen. Bitte warte {int(reset_ts - now)} Sekunden."
                        )
                        return
                    count += 1
                else:
                    count = 1
                    reset_ts = now + period

                conn.execute(
                    """INSERT INTO rate_limits (chat_id, command, count, reset_ts)
                    VALUES (?, ?, ?, ?)
                    ON CONFLICT(chat_id, command) DO UPDATE SET
                    count = excluded.count,
                    reset_ts = excluded.reset_ts""",
                    (chat_id, command, count, reset_ts)
                )

            return await func(update, context)
        return wrapper
    return decorator
    
# KI-Service
class AIService:
    client = OpenAI(api_key=OPENAI_API_KEY) if OPENAI_API_KEY else None

    @classmethod
    async def generate_recommendations(cls, tracked: list) -> str:
        if not cls.client:
            return "❌ KI-Dienste aktuell nicht verfügbar"
            
        try:
            response = cls.client.chat.completions.create(
                model="gpt-4-1106-preview",
                messages=[{
                    "role": "system",
                    "content": f"Empfehle 5 ähnliche Streamer wie {', '.join(tracked)}. Format: 1. Name - Plattform - Kurzbeschreibung"
                }],
                temperature=0.7,
                max_tokens=500
            )
            return f"🎮 KI-Empfehlungen:\n{response.choices[0].message.content}"
        except Exception as e:
            logger.error(f"AI Error: {e}")
            return "⚠️ KI-Service temporär nicht verfügbar"

    @classmethod
    async def generate_thumbnail(cls, title: str) -> Optional[str]:
        if not cls.client:
            return None
            
        try:
            response = cls.client.images.generate(
                model="dall-e-3",
                prompt=f"Professional Gaming Stream Thumbnail: {title}",
                size="1024x1024",
                quality="hd"
            )
            return response.data[0].url
        except Exception as e:
            logger.error(f"Thumbnail Generation Error: {e}")
            return None

# Spenden-Service
class DonationService:
    @staticmethod
    async def handle_donation(update: Update, context: ContextTypes.DEFAULT_TYPE):
        keyboard = [
            [InlineKeyboardButton("💳 PayPal", url=PAYPAL_ME)],
            [InlineKeyboardButton("🎗️ GoFundMe", url=DONATION_LINK)]
        ]
        await update.message.reply_text(
            "❤️ Unterstütze dieses Projekt:\n"
            "Deine Spende hilft bei der Weiterentwicklung!",
            reply_markup=InlineKeyboardMarkup(keyboard)
            )
        user_id = str(update.effective_user.id)
        with sqlite3.connect(DB_FILE) as conn:
            conn.execute(
                "INSERT INTO donations (donor_id, donation_date) VALUES (?, ?)",
                (user_id, datetime.utcnow().isoformat())
            )

# Hauptfunktionen
@rate_limited("track", max_requests=5, period=30)
async def track(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args or len(context.args) < 2:
        await update.message.reply_text("❌ Format: /track <twitch|youtube> <name>")
        return

    platform = context.args[0].lower()
    name = " ".join(context.args[1:]).lower()

    if platform not in ["twitch", "youtube"]:
        await update.message.reply_text("❌ Ungültige Plattform")
        return

    user_id = None
    try:
        if platform == "twitch":
            user_id = await TwitchService.get_user_id(name)
        else:
            if await YouTubeService._check_quota() < 100:
                await update.message.reply_text("❌ Tägliches YouTube-Kontingent erschöpft")
                return
            user_id = await YouTubeService.get_channel_id(name)

        if not user_id:
            await update.message.reply_text("❌ Kanal nicht gefunden")
            return

        chat_id = str(update.message.chat.id)
        with sqlite3.connect(DB_FILE) as conn:
            conn.execute(
                """INSERT INTO tracked_streams 
                (chat_id, streamer, user_id, platform, last_status, added_at)
                VALUES (?, ?, ?, ?, 0, ?)
                ON CONFLICT DO NOTHING""",
                (chat_id, name, user_id, platform, datetime.utcnow().isoformat())
            )
        await update.message.reply_text(f"✅ {name} ({platform}) wird überwacht")

    except Exception as e:
        logger.error(f"Track Error: {e}")
        await update.message.reply_text("⚠️ Fehler beim Hinzufügen")

@rate_limited("untrack", max_requests=5, period=30)
async def untrack(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args or len(context.args) < 2:
        await update.message.reply_text("❌ Format: /untrack <twitch|youtube> <name>")
        return

    platform = context.args[0].lower()
    name = " ".join(context.args[1:]).lower()
    chat_id = str(update.message.chat.id)

    with sqlite3.connect(DB_FILE) as conn:
        cur = conn.execute(
            "DELETE FROM tracked_streams WHERE chat_id = ? AND streamer = ? AND platform = ?",
            (chat_id, name, platform)
        )

    if cur.rowcount > 0:
        await update.message.reply_text(f"🗑 {name} ({platform}) entfernt")
    else:
        await update.message.reply_text("❌ Eintrag nicht gefunden")

async def list_streams(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = str(update.message.chat.id)
    with sqlite3.connect(DB_FILE) as conn:
        streams = conn.execute(
            "SELECT streamer, platform, last_status, user_id FROM tracked_streams WHERE chat_id = ?",
            (chat_id,)
        ).fetchall()

    if not streams:
        await update.message.reply_text("🔍 Keine Streamer registriert")
        return

    keyboard = []
    for streamer, platform, status, user_id in streams:
        url = (f"https://twitch.tv/{streamer}" if platform == "twitch" 
               else f"https://youtube.com/channel/{user_id}")
        
        button = InlineKeyboardButton(
            text=f"{'🎮' if platform == 'twitch' else '📺'} {streamer} {'🟢' if status else '🔴'}",
            url=url
        )
        keyboard.append([button])

    await update.message.reply_text(
        "🎥 Registrierte Streamer:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

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
            token = await TwitchService._get_token()
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    "https://api.twitch.tv/helix/streams",
                    headers={
                        "Client-ID": TWITCH_CLIENT_ID,
                        "Authorization": f"Bearer {token}"
                    },
                    params={"user_id": user_ids},
                )
                live_data = {stream["user_id"]: stream for stream in response.json().get("data", [])}

            updates_start = []
            updates_end = []
            for stream in twitch_streams:
                chat_id, streamer, user_id, platform, status, last_start = stream
                stream_info = live_data.get(user_id)
                is_live = stream_info is not None
                
                if is_live and not status:
                    thumbnail_url = stream_info["thumbnail_url"].replace("{width}", "640").replace("{height}", "360")
                    caption = f"🎮 {streamer} ist LIVE auf Twitch!\n{stream_info.get('title', '')}"
                    
                    if OPENAI_API_KEY:
                        ai_thumbnail = await AIService.generate_thumbnail(stream_info.get('title', 'Live Stream'))
                        if ai_thumbnail:
                            thumbnail_url = ai_thumbnail
                    
                    await context.bot.send_photo(
                        chat_id=chat_id,
                        photo=thumbnail_url,
                        caption=caption,
                        reply_markup=InlineKeyboardMarkup([
                            [InlineKeyboardButton("🔴 LIVE", url=f"https://twitch.tv/{streamer}")]
                        ])
                    )
                    updates_start.append((
                        1, 
                        datetime.utcnow().isoformat(), 
                        stream_info["viewer_count"], 
                        chat_id, 
                        streamer, 
                        platform
                    ))
                
                elif not is_live and status:
                    duration = (datetime.utcnow() - datetime.fromisoformat(last_start)).total_seconds()
                    await context.bot.send_message(
                        chat_id=chat_id,
                        text=f"🌙 {streamer} (Twitch) offline. Dauer: {int(duration // 60)} Minuten"
                    )
                    updates_end.append((
                        0,
                        datetime.utcnow().isoformat(),
                        duration,
                        chat_id,
                        streamer,
                        platform
                    ))

            with sqlite3.connect(DB_FILE) as conn:
                if updates_start:
                    conn.executemany(
                        """UPDATE tracked_streams 
                        SET last_status = ?, last_stream_start = ?, peak_viewers = ?
                        WHERE chat_id = ? AND streamer = ? AND platform = ?""",
                        updates_start
                    )
                if updates_end:
                    conn.executemany(
                        """UPDATE tracked_streams 
                        SET last_status = ?, last_stream_end = ?, total_stream_time = total_stream_time + ?
                        WHERE chat_id = ? AND streamer = ? AND platform = ?""",
                        updates_end
                    )

        # YouTube-Check
        youtube_streams = [s for s in tracked if s[3] == "youtube"]
        for stream in youtube_streams:
            chat_id, streamer, channel_id, platform, status, last_start = stream
            live_info = await YouTubeService.check_live(channel_id)
            is_live = live_info if isinstance(live_info, dict) else {"snippet": {"title": "Live Stream"}} if live_info else None
            
            if is_live and not status:
                video_id = live_info["id"]["videoId"]
                await context.bot.send_message(
                    chat_id=chat_id,
                    text=f"🎥 {streamer} ist LIVE auf YouTube!\n{live_info['snippet']['title']}\nhttps://youtu.be/{video_id}"
                )
                with sqlite3.connect(DB_FILE) as conn:
                    conn.execute(
                        """UPDATE tracked_streams 
                        SET last_status = 1, last_stream_start = ?
                        WHERE chat_id = ? AND streamer = ? AND platform = ?""",
                        (datetime.utcnow().isoformat(), chat_id, streamer, platform)
                    )

            elif not is_live and status:
                duration = (datetime.utcnow() - datetime.fromisoformat(last_start)).total_seconds()
                await context.bot.send_message(
                    chat_id=chat_id,
                    text=f"🌙 {streamer} (YouTube) offline. Dauer: {int(duration // 60)} Minuten"
                )
                with sqlite3.connect(DB_FILE) as conn:
                    conn.execute(
                        """UPDATE tracked_streams 
                        SET last_status = 0, last_stream_end = ?, total_stream_time = total_stream_time + ?
                        WHERE chat_id = ? AND streamer = ? AND platform = ?""",
                        (datetime.utcnow().isoformat(), duration, chat_id, streamer, platform)
                    )

        logger.info("✅ Stream-Check abgeschlossen")

    except Exception as e:
        logger.error(f"Stream-Check Fehler: {e}")
        traceback.print_exc()
        if ADMIN_CHAT_ID:
            await context.bot.send_message(
                chat_id=ADMIN_CHAT_ID,
                text=f"🚨 Kritischer Fehler: {str(e)[:3000]}"
            )

# Setup
def main():
    init_db()
    application = ApplicationBuilder() \
        .token(TELEGRAM_TOKEN) \
        .rate_limiter(AIORateLimiter()) \
        .build()

    # Handler
    application.add_handler(CommandHandler("start", lambda u,c: u.message.reply_text("Willkommen beim Stream Monitor!")))
    application.add_handler(CommandHandler("track", track))
    application.add_handler(CommandHandler("untrack", untrack))
    application.add_handler(CommandHandler("list", list_streams))
    application.add_handler(CommandHandler("donate", DonationService.handle_donation))
    application.add_handler(CommandHandler("recommend", 
        lambda u,c: asyncio.create_task(AIService.generate_recommendations(u,c))))
    
    application.add_error_handler(error_handler)
    application.job_queue.run_repeating(check_streams, interval=60, first=10)

    # Start
    logger.info("🤖 Bot startet...")
    application.run_polling()

if __name__ == "__main__":
    try:
        import uvloop
        uvloop.install()
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("🛑 Bot gestoppt")