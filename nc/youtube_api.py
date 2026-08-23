"""nc.youtube_api — v4.0: YouTube-Live-Chat über die offizielle Data API v3.

Warum bahnbrechend für NIGHTCRAWLER: der bisherige YouTube-Listener SCRAPTE die
Live-Seite (Regex im HTML) — fragil, und auf Server-/OVH-IPs oft von der
Consent-Wall blockiert (→ dauerhaft „getrennt"). Und moderieren konnte er gar
nicht. Dieses Modul liefert die REINEN Bausteine für den offiziellen Weg:
Live-Chat LESEN (liveChat/messages) und DURCHGREIFEN (liveChat/bans = Timeout,
liveChat/messages DELETE). Der Bot hat Token/liveChatId/Senden schon — hier
kommen Leser + Moderation dazu. Alles rein & testbar; die HTTP-Aufrufe macht
der Bot mit dem bestehenden OAuth-Token.
"""

BASE = "https://www.googleapis.com/youtube/v3"
MESSAGES_URL = BASE + "/liveChat/messages"
BANS_URL = BASE + "/liveChat/bans"
BROADCASTS_URL = BASE + "/liveBroadcasts"
VIDEOS_URL = BASE + "/videos"


def active_broadcast_params():
    """Query fuer liveBroadcasts.list — der EIGENE gerade aktive Broadcast."""
    return {"part": "id,snippet", "broadcastStatus": "active",
            "broadcastType": "all", "mine": "true", "maxResults": 1}


def parse_broadcast_id(data):
    """Video-/Broadcast-ID des aktiven Broadcasts (== Video-ID) oder ''."""
    if not isinstance(data, dict):
        return ""
    items = data.get("items") or []
    return (items[0].get("id") or "") if items else ""


def video_list_params(video_id):
    return {"part": "snippet", "id": video_id}


def parse_video_snippet(data):
    """Aktuelles snippet des Videos (Kopie) oder {}."""
    if not isinstance(data, dict):
        return {}
    items = data.get("items") or []
    return dict(items[0].get("snippet") or {}) if items else {}


def merge_video_snippet(current, title=None, category_id=None):
    """Aktualisiertes snippet fuer videos.update. Bei videos.update sind title UND
       categoryId PFLICHT — nicht geaenderte Felder behalten den aktuellen Wert,
       damit kein Pflichtfeld verloren geht. Titel auf 100 Zeichen (YT-Limit)."""
    snip = dict(current or {})
    if title:
        snip["title"] = title[:100]
    if category_id:
        snip["categoryId"] = str(category_id)
    return snip


def video_update_body(video_id, snippet):
    return {"id": video_id, "snippet": snippet}


def list_params(live_chat_id, page_token=""):
    """Query-Parameter für liveChat/messages.list (Lesen des Chats)."""
    p = {"liveChatId": live_chat_id, "part": "snippet,authorDetails", "maxResults": 200}
    if page_token:
        p["pageToken"] = page_token
    return p


def parse_messages(data):
    """(messages, next_page_token, polling_ms). messages = Liste normalisierter
       Dicts {id, author, channel_id, text, is_mod, is_owner, is_sponsor}.
       Robust gegen fehlende Felder (leere Antwort → [])."""
    if not isinstance(data, dict):
        return [], "", 5000
    out = []
    for it in (data.get("items") or []):
        sn = it.get("snippet") or {}
        ad = it.get("authorDetails") or {}
        text = sn.get("displayMessage") or (
            (sn.get("textMessageDetails") or {}).get("messageText") or "")
        out.append({
            "id": it.get("id") or "",
            "author": ad.get("displayName") or "",
            "channel_id": ad.get("channelId") or sn.get("authorChannelId") or "",
            "text": text,
            "is_mod": bool(ad.get("isChatModerator")),
            "is_owner": bool(ad.get("isChatOwner")),
            "is_sponsor": bool(ad.get("isChatSponsor")),
            "published_at": sn.get("publishedAt") or "",
        })
    try:
        poll = int(data.get("pollingIntervalMillis") or 0)
    except (TypeError, ValueError):
        poll = 0
    # YouTube empfiehlt pollingIntervalMillis; Untergrenze schützt das Kontingent.
    poll = max(poll, 3000)
    return out, (data.get("nextPageToken") or ""), poll


def ban_payload(live_chat_id, channel_id, seconds=0):
    """Body für liveChat/bans.insert. seconds>0 = temporärer Timeout, sonst
       permanenter Bann. So setzt der Moderator YouTube-Timeouts wie auf Kick."""
    snip = {"liveChatId": live_chat_id,
            "type": "temporary" if seconds and seconds > 0 else "permanent",
            "bannedUserDetails": {"channelId": channel_id}}
    if seconds and seconds > 0:
        snip["banDurationSeconds"] = int(seconds)
    return {"snippet": snip}


def parse_error(data):
    """Lesbarer Fehlergrund aus einer YouTube-API-Fehlerantwort (oder '')."""
    err = (data or {}).get("error") if isinstance(data, dict) else None
    if not err:
        return ""
    reason = ((err.get("errors") or [{}])[0].get("reason") or "").lower()
    if reason in ("quotaexceeded", "dailylimitexceeded", "ratelimitexceeded"):
        return f"Kontingent erschöpft ({reason}) — kein Rechteproblem, frei nach Mitternacht US-Pazifik"
    msg = (err.get("message") or "")[:120]
    return f"{reason or 'fehler'}: {msg}" if msg else (reason or "fehler")


def is_self(msg, own_channel_id):
    """True, wenn die Nachricht vom eigenen Kanal stammt (nicht moderieren/
       nicht beantworten — sonst Selbst-Loop)."""
    return bool(own_channel_id) and msg.get("channel_id") == own_channel_id
