"""nc.kick_oauth — B169: Kick User-OAuth 2.1 (Authorization-Code + PKCE), bot-frei.

Warum: Kick-Titel/Kategorie setzen (PATCH api.kick.com/public/v1/channels) verlangt
einen USER-Access-Token mit Scope `channel:write`. Der bisherige App-Token
(client_credentials) darf das NICHT → HTTP 401 (siehe B164). Dieses Modul liefert
die REINEN, testbaren Bausteine des offiziellen Kick-OAuth-Flows (id.kick.com):
PKCE-Erzeugung, Authorize-URL, Token-/Refresh-Payloads, Antwort-Parsing, Ablauf-/
Scope-Prüfung. Der Bot macht die HTTP-Aufrufe + Token-Speicherung (app_config).

Spec: https://github.com/KickEngineering/KickDevDocs (OAuth 2.1 Flow).
"""

import base64
import hashlib
import secrets
from urllib.parse import urlencode

AUTHORIZE_URL = "https://id.kick.com/oauth/authorize"
TOKEN_URL = "https://id.kick.com/oauth/token"
REVOKE_URL = "https://id.kick.com/oauth/revoke"
# channel:write = Titel/Kategorie setzen; chat:write = als Nutzer schreiben.
# W17: chat:write = im Chat schreiben (App-Token darf das NICHT -> HTTP 401);
# moderation:ban = Timeouts/Banns; moderation:chat_message:manage = Nachrichten
# loeschen. Ohne diese Scopes antwortet Kick auf Chat/Moderation mit 401.
DEFAULT_SCOPES = ("user:read", "channel:read", "channel:write", "chat:write",
                  "moderation:ban", "moderation:chat_message:manage")


def gen_pkce():
    """(code_verifier, code_challenge) nach RFC 7636, Methode S256."""
    verifier = secrets.token_urlsafe(64)
    challenge = base64.urlsafe_b64encode(
        hashlib.sha256(verifier.encode("ascii")).digest()).decode("ascii").rstrip("=")
    return verifier, challenge


def gen_state():
    return secrets.token_urlsafe(24)


def build_authorize_url(client_id, redirect_uri, scopes, state, challenge):
    """Vollständige Authorize-URL. Bei 127.0.0.1-Redirect wird der von Kick
       dokumentierte Sacrificial-`redirect`-Parameter vorangestellt (NextJS-Bug)."""
    params = {
        "response_type": "code",
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        "scope": " ".join(scopes),
        "code_challenge": challenge,
        "code_challenge_method": "S256",
        "state": state,
    }
    if "127.0.0.1" in (redirect_uri or ""):
        return AUTHORIZE_URL + "?redirect=127.0.0.1&" + urlencode(params)
    return AUTHORIZE_URL + "?" + urlencode(params)


def token_exchange_payload(client_id, client_secret, redirect_uri, code, verifier):
    """Form-Body für den Authorization-Code-Tausch (POST /oauth/token)."""
    return {
        "grant_type": "authorization_code",
        "client_id": client_id,
        "client_secret": client_secret,
        "redirect_uri": redirect_uri,
        "code_verifier": verifier,
        "code": code,
    }


def token_refresh_payload(client_id, client_secret, refresh_token):
    return {
        "grant_type": "refresh_token",
        "client_id": client_id,
        "client_secret": client_secret,
        "refresh_token": refresh_token,
    }


def parse_token_response(data, now_ts):
    """Token-Antwort → (token_dict, None) oder (None, fehler). token_dict enthält
       expires_at (absolut) für die Ablaufprüfung."""
    if not isinstance(data, dict) or not data.get("access_token"):
        err = data.get("error") if isinstance(data, dict) else "keine Token-Antwort"
        return None, (err or "kein access_token in Antwort")
    try:
        expires_in = int(data.get("expires_in") or 0)
    except (TypeError, ValueError):
        expires_in = 0
    return {
        "access_token": data["access_token"],
        "refresh_token": data.get("refresh_token", ""),
        "token_type": data.get("token_type", "bearer"),
        "scope": data.get("scope", ""),
        "obtained_at": now_ts,
        "expires_at": (now_ts + expires_in) if expires_in else 0,
    }, None


def is_expired(token, now_ts, skew=60):
    """True, wenn der Token abgelaufen ist (mit Sicherheits-Skew). expires_at=0
       (unbekannt) gilt als NICHT abgelaufen — dann entscheidet erst ein 401."""
    ea = (token or {}).get("expires_at") or 0
    return bool(ea) and now_ts >= (ea - skew)


def has_scope(token, scope):
    return scope in ((token or {}).get("scope", "") or "").split()
