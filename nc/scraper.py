"""nc.scraper — TikTok-Profil/Live-HTML-Scraper.

Extrahiert aus bot_v37.py. Proxy-Auswahl kommt aus nc.proxyutil (dort per
configure injiziert), aiohttp wird lazy im Call importiert."""

import asyncio
import json
import re
import html
import logging

import aiohttp

log = logging.getLogger("TikTokBot")

_LIVE_RESOLVER_HEADERS = {}     # vom Bot via configure_scraper injiziert


def configure_scraper(live_resolver_headers=None):
    global _LIVE_RESOLVER_HEADERS
    if live_resolver_headers is not None:
        _LIVE_RESOLVER_HEADERS = live_resolver_headers

from nc.proxyutil import get_random_proxy


class TikTokScraper:
    BASE = "https://www.tiktok.com"

    def __init__(self):
        # VERBESSERUNG: TCPConnector mit Connection-Pooling — verhindert
        # TCP-Handshake-Overhead bei jedem Check, reduziert Latenz um 50-200ms.
        # limit=20 erlaubt parallele Auflösungen, ttl_dns_cache=300s reduziert
        # DNS-Lookups. keepalive_timeout=60s hält Connections zu TikTok-CDN warm.
        connector = aiohttp.TCPConnector(
            limit=20,
            limit_per_host=8,
            ttl_dns_cache=300,
            keepalive_timeout=60,
            enable_cleanup_closed=True,
        )
        self.session = aiohttp.ClientSession(
            connector=connector,
            headers={
                "User-Agent": _LIVE_RESOLVER_HEADERS["User-Agent"],
                "Accept": _LIVE_RESOLVER_HEADERS["Accept"],
                "Accept-Language": _LIVE_RESOLVER_HEADERS["Accept-Language"],
                "Accept-Encoding": _LIVE_RESOLVER_HEADERS["Accept-Encoding"],
                "sec-ch-ua": _LIVE_RESOLVER_HEADERS["sec-ch-ua"],
                "sec-ch-ua-mobile": _LIVE_RESOLVER_HEADERS["sec-ch-ua-mobile"],
                "sec-ch-ua-platform": _LIVE_RESOLVER_HEADERS["sec-ch-ua-platform"],
                "Referer": "https://www.tiktok.com/",
                "Connection": "keep-alive",
            },
            timeout=aiohttp.ClientTimeout(total=20, connect=8, sock_read=15),
        )

    async def close(self):
        await self.session.close()

    async def _request(self, url, **kwargs):
        proxy = get_random_proxy()                                      # C18
        if proxy and "proxy" not in kwargs:
            kwargs["proxy"] = proxy
        for attempt in range(3):
            try:
                resp = await self.session.get(url, **kwargs)
                if resp.status in (429, 500, 502, 503, 504) and attempt < 2:
                    # BUG-FIX: Connection zurück in den Pool geben — eine ungelesene
                    # aiohttp-Response hält ihre Connection bis Body gelesen/released.
                    # Vorher leakte jeder Retry eine Connection; bei limit_per_host=8
                    # blockiert der nächste GET genau im 429-Sturm (Pool-Starve).
                    resp.release()
                    await asyncio.sleep(2 ** attempt)
                    continue
                return resp
            except Exception:
                if attempt == 2:
                    raise
                await asyncio.sleep(2 ** attempt)
        raise RuntimeError("Request wiederholt gescheitert")

    # C1+C2: html.unescape now refers to the imported module again, and we
    # parse TikTok's current rehydration script as well as the legacy SIGI_STATE.
    def _extract_json(self, html_text: str):
        m = re.search(
            r'<script id="__UNIVERSAL_DATA_FOR_REHYDRATION__"[^>]*>(.*?)</script>',
            html_text, re.DOTALL)
        if m:
            try:
                payload = json.loads(html.unescape(m.group(1)))
                return ("universal", payload.get("__DEFAULT_SCOPE__") or payload)
            except Exception as e:
                log.debug(f"UNIVERSAL_DATA parse failed: {e}")
        m = re.search(
            r'<script id="SIGI_STATE" type="application/json">(.*?)</script>',
            html_text, re.DOTALL)
        if m:
            try:
                return ("sigi", json.loads(html.unescape(m.group(1))))
            except Exception as e:
                log.debug(f"SIGI_STATE parse failed: {e}")
        return (None, None)

    def _user_from_universal(self, scope: dict):
        info = (scope or {}).get("webapp.user-detail", {}).get("userInfo")
        if not info:
            return None
        return {"user": info.get("user") or {}, "stats": info.get("stats") or {}}

    def _user_from_sigi(self, data: dict, username: str):
        ul = username.lower()
        um = data.get("UserModule", {})
        users = um.get("users", {}) or {}
        for u in users.values():
            if str(u.get("uniqueId", "")).lower() == ul:
                stats = um.get("stats", {}).get(u.get("id"), {}) or {}
                return {"user": u, "stats": stats}
        return None

    def _recent_videos_sigi(self, data: dict, limit=3):
        videos = []
        try:
            for vid, info in list((data.get("ItemModule") or {}).items())[:limit]:
                videos.append({
                    "id": vid,
                    "desc": info.get("desc", ""),
                    "url": f"{self.BASE}/@{info.get('author',{}).get('uniqueId','')}/video/{vid}",
                })
        except Exception:
            pass
        return videos

    async def fetch_profile(self, username: str) -> dict:
        url = f"{self.BASE}/@{username}"
        result = {"ok": False, "username": username, "profile_url": url,
                  "http_status": None, "error": None, "recent_videos": []}
        try:
            resp = await self._request(url, allow_redirects=True)
            result["http_status"] = resp.status
            if resp.status != 200:
                result["error"] = f"HTTP {resp.status}"
                resp.release()   # BUG-FIX: Body nie gelesen → Connection würde leaken
                return result
            text = await resp.text()
        except Exception as e:
            result["error"] = f"Request: {e}"
            return result

        kind, parsed = self._extract_json(text)
        if not parsed:
            result["error"] = "JSON nicht gefunden (TikTok-HTML hat sich evtl. geändert)"
            return result

        if kind == "universal":
            found = self._user_from_universal(parsed)
        else:
            found = self._user_from_sigi(parsed, username)
            result["recent_videos"] = self._recent_videos_sigi(parsed)

        if not found:
            result["error"] = "Benutzerdaten nicht gefunden"
            return result

        user, stats = found["user"], found["stats"]
        result.update({
            "ok": True,
            "user_id":         user.get("id"),
            "sec_uid":         user.get("secUid"),
            "unique_id":       user.get("uniqueId", username),
            "nickname":        user.get("nickname"),
            "signature":       user.get("signature"),
            "avatar":          user.get("avatarLarger") or user.get("avatarMedium") or user.get("avatarThumb"),
            "private":         user.get("privateAccount"),
            "verified":        user.get("verified"),
            "follower_count":  stats.get("followerCount"),
            "following_count": stats.get("followingCount"),
            "heart_count":     stats.get("heartCount") or stats.get("heart"),
            "video_count":     stats.get("videoCount"),
            "friend_count":    stats.get("friendCount"),
            "digg_count":      stats.get("diggCount"),
            "create_time":     user.get("createTime"),
            "modify_time":     user.get("modifyTime"),
        })
        return result
