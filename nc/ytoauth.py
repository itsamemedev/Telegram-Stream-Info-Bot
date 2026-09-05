"""nc.ytoauth — YouTube/Google-OAuth ohne manuellen Token-Tanz.

WARUM DAS EXISTIERT (B121):
Twitch hatte mit nc.twitchoauth laengst einen Ein-Klick-Flow im Dashboard.
YouTube nicht: dort musste YOUTUBE_REFRESH_TOKEN von Hand ueber den Google
OAuth Playground erzeugt und in die .env geschrieben werden. Das ist die
gleiche Fehlerquelle, die der Twitch-Flow beseitigt hat:

  1. Der Token muss zur EIGENEN Client-ID gehoeren. Ein Token aus dem
     Playground gehoert zu DESSEN Client-ID, wenn man "Use your own
     credentials" vergisst — die API antwortet dann mit einem
     nichtssagenden 401.
  2. Er braucht die richtigen Scopes. youtube.readonly reicht fuer
     Zuschauer/Abonnenten, aber NICHT zum Schreiben im Live-Chat.
  3. Refresh-Tokens von Apps im Testing-Status laufen nach 7 Tagen ab.
     Danach friert der Chat-Versand still ein — kein Fehler im Log, der
     Bot antwortet einfach nicht mehr.

Dieser Flow ersetzt das durch: EINMAL im Browser autorisieren, danach hat
der Bot einen Refresh-Token und erneuert den Access-Token selbst.

Aufbau bewusst identisch zu nc.twitchoauth (configure/status/authorize_url/
exchange_code/access_token), damit beide Panels im Dashboard gleich
funktionieren und man nur an einer Stelle denken muss.

GOOGLE-BESONDERHEITEN gegenueber Twitch:
  * access_type=offline UND prompt=consent sind PFLICHT fuer einen
    Refresh-Token. Ohne prompt=consent liefert Google beim zweiten
    Autorisieren nur einen Access-Token — der Flow scheint zu klappen und
    der Bot faellt trotzdem nach einer Stunde aus.
  * Redirect-URI: http://localhost:PORT ist erlaubt (Loopback-Ausnahme),
    nackte IPs nicht. Gleiche Tunnel-Loesung wie bei Twitch.
  * Beim Refresh gibt Google KEINEN neuen refresh_token zurueck. Der alte
    bleibt gueltig und wird weiterverwendet.

Der Refresh-Token liegt in einer Datei unter RECORDINGS_DIR (die .env ist
zur Laufzeit nicht beschreibbar). Nur der Refresh-Token, keine
Access-Token — die sind kurzlebig und werden nie gespeichert.
"""

import json
import logging
import os
import time
import urllib.parse

log = logging.getLogger("TikTokBot")

# Scopes:
#   youtube.readonly  — Kanalstatus: Zuschauer, Abonnenten, laufender Stream
#   youtube.force-ssl — Live-Chat lesen UND schreiben (AZRAEL) sowie
#                       moderieren (Nachricht loeschen, User timeouten)
#   youtube.upload    — v4.2-W29: Auto-Clipper laedt Highlight-Clips hoch.
#                       Neu seit W29 — eine vor dieser Welle erteilte
#                       Autorisierung traegt ihn nicht, der Upload-Aufruf
#                       antwortet dann mit 401/403 bis neu verbunden wird.
# Ein Token traegt alle drei; damit deckt EINE Autorisierung Zahlen, Chat,
# Moderation und Upload ab — genau wie beim Twitch-Flow.
SCOPES = ["https://www.googleapis.com/auth/youtube.readonly",
          "https://www.googleapis.com/auth/youtube.force-ssl",
          "https://www.googleapis.com/auth/youtube.upload"]
AUTHORIZE = "https://accounts.google.com/o/oauth2/v2/auth"
TOKEN = "https://oauth2.googleapis.com/token"
REVOKE = "https://oauth2.googleapis.com/revoke"
# v4.2-W29: resumable Upload — zwei Schritte, keine Datei im Request-Body
# des ersten Aufrufs (der legt nur die Session an, Location-Header traegt
# die Upload-URL fuer den zweiten, den eigentlichen PUT).
UPLOAD_INIT = ("https://www.googleapis.com/upload/youtube/v3/videos"
               "?uploadType=resumable&part=snippet,status")

_state = {
    "store_path": None,
    "redirect_uri": "http://localhost:3000/api/youtube/oauth/callback",
    "last_redirect": "",
    "access": "",
    "access_exp": 0.0,
    "refresh": "",
    "csrf": "",
    "channel": "",
    # v4.2-W9: warum die Verbindung weg ist und seit wann. Ohne das meldet
    # das Panel nach einem abgelaufenen Token weiter "verbunden" — und der
    # Betreiber sucht den Fehler im Chat-Code statt bei Google.
    "last_error": "",
    "last_error_ts": 0.0,
}


def configure(store_path, redirect_uri=None):
    """Beim Start aufrufen: wo der Refresh-Token liegt, welche Redirect-URI gilt.

    v4.2-W9: der Pfad wird ABSOLUT gemacht. bot.py reicht "recordings/..."
    herein, also relativ zum Arbeitsverzeichnis — ein spaeteres os.chdir oder
    ein Start aus einem anderen Verzeichnis (Handstart, cron) haette den Store
    woanders gesucht und den gespeicherten Token damit stillschweigend
    verloren. Einmal beim Start aufgeloest gilt er fuer die ganze Laufzeit.
    """
    _state["store_path"] = os.path.abspath(store_path) if store_path else store_path
    if redirect_uri:
        _state["redirect_uri"] = redirect_uri.strip()
    _load()


def _client():
    cid = (os.getenv("YOUTUBE_CLIENT_ID", "") or "").strip()
    csec = (os.getenv("YOUTUBE_CLIENT_SECRET", "") or "").strip()
    return cid, csec


def _load():
    """Refresh-Token laden. Reihenfolge: Store-Datei zuerst, .env als
    Rueckfall — so bleibt eine bestehende Handkonfiguration gueltig, wird
    aber vom Flow ueberschrieben, sobald einmal verbunden wurde."""
    p = _state.get("store_path")
    if p and os.path.exists(p):
        try:
            with open(p, encoding="utf-8") as f:
                d = json.load(f)
            _state["refresh"] = (d.get("refresh_token") or "").strip()
            _state["channel"] = (d.get("channel") or "").strip()
        except Exception as e:
            log.debug("ytoauth: Store nicht lesbar: %s", e)
    if not _state["refresh"]:
        _state["refresh"] = (os.getenv("YOUTUBE_REFRESH_TOKEN", "") or "").strip()


def _save():
    """Die Verbindung sichern.

    v4.2-W9: _save schreibt nur eine VERBINDUNG, nie ihre Abwesenheit.
    Vorher konnte set_channel() den Store mit einem leeren Refresh-Token
    ueberschreiben, sobald access_token() ihn im Speicher geleert hatte — ein
    Kanalname, der die gespeicherte Verbindung vernichtet. Geloescht wird
    ausschliesslich ueber forget(), und das entfernt die Datei.
    """
    p = _state.get("store_path")
    if not p:
        return
    if not (_state.get("refresh") or "").strip():
        log.debug("ytoauth: _save ohne Refresh-Token uebersprungen "
                  "(Loeschen laeuft ueber forget())")
        return
    try:
        os.makedirs(os.path.dirname(p), exist_ok=True)
        tmp = p + ".tmp"
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump({"refresh_token": _state["refresh"],
                       "channel": _state.get("channel", "")}, f)
        os.replace(tmp, p)
        try:
            os.chmod(p, 0o600)     # Refresh-Token ist ein Geheimnis
        except OSError:
            pass
    except Exception as e:
        # v4.2-W9 auf error, nicht warning: ein ERROR-Log zeigt warning NIE
        # (CLAUDE.md). Genau so blieb "der Token wird nicht gespeichert"
        # unsichtbar — der Flow meldete Erfolg, und nach dem naechsten
        # Neustart war die Verbindung weg.
        _merke_fehler("Store nicht schreibbar: %s" % e)
        log.error("ytoauth: Store nicht schreibbar (%s) — die Verbindung "
                  "ueberlebt den naechsten Neustart NICHT: %s", p, e)


def _merke_fehler(text):
    _state["last_error"] = text
    _state["last_error_ts"] = time.time()


def status():
    """Fuers Dashboard: was ist konfiguriert, ist der Flow abgeschlossen?"""
    cid, csec = _client()
    from_env = bool((os.getenv("YOUTUBE_REFRESH_TOKEN", "") or "").strip())
    p = _state.get("store_path")
    return {
        "has_client_id": bool(cid),
        "has_secret": bool(csec),
        "has_refresh": bool(_state["refresh"]),
        "refresh_from": ("flow" if (p and os.path.exists(p))
                         else ("env" if from_env else "")),
        "ready": bool(cid and csec and _state["refresh"]),
        "redirect_uri": _state["redirect_uri"],
        "scopes": SCOPES,
        "channel": _state.get("channel", ""),
        # v4.2-W9: warum es nicht geht. "abgelaufen" und "nie verbunden"
        # sahen im Panel bisher gleich aus — beides nur ein graues Feld.
        # Der Betreiber musste raten, ob er neu verbinden oder erst die
        # Google-Konsole pruefen muss.
        "expired": bool(cid and csec and not _state["refresh"]
                        and _state.get("last_error")),
        "last_error": _state.get("last_error", ""),
        "last_error_ts": _state.get("last_error_ts", 0.0),
    }


def authorize_url(csrf, redirect_uri=None, prompt="select_account consent"):
    """Schritt 1: der Link, den der Nutzer im Browser oeffnet.

    prompt='select_account consent' zeigt IMMER die Google-Kontoauswahl (wichtig,
    wenn man mehrere Konten hat und das richtige/ein anderes verbinden will) UND
    erzwingt den Zustimmungsdialog — Letzteres liefert zuverlaessig einen
    Refresh-Token. Mit prompt='consent' (ohne select_account) nimmt Google still
    das zuletzt genutzte Konto.
    """
    cid, _ = _client()
    if not cid:
        return None
    _state["csrf"] = csrf
    ru = (redirect_uri or _state["redirect_uri"]).strip()
    _state["last_redirect"] = ru      # muss beim Tausch identisch sein
    q = urllib.parse.urlencode({
        "client_id": cid,
        "redirect_uri": ru,
        "response_type": "code",
        "scope": " ".join(SCOPES),
        "state": csrf,
        # access_type=offline + ein 'consent' im prompt sind PFLICHT fuer den
        # Refresh-Token (siehe Modul-Docstring); 'select_account' bringt die
        # Kontoauswahl.
        "access_type": "offline",
        "prompt": (prompt or "consent"),
        "include_granted_scopes": "true",
    })
    return AUTHORIZE + "?" + q


async def exchange_code(code, state, aiohttp):
    """Schritt 2: ?code gegen Access+Refresh tauschen. -> (ok, meldung)."""
    # v4.0-W118 (SEC): frueher `if state and _state["csrf"] and ...` — die
    # Pruefung fiel weg, sobald der Rueckruf GAR KEINEN state mitbrachte. Genau
    # das kann ein Angreifer: er baut den Callback-Aufruf selbst und laesst den
    # Parameter einfach weg. Damit war der CSRF-Schutz mit einem Handgriff
    # abschaltbar. Jetzt gilt: wurde ein state ausgegeben, MUSS er passen.
    if _state["csrf"] and state != _state["csrf"]:
        return False, "state fehlt oder stimmt nicht (CSRF) — Flow neu starten"
    cid, csec = _client()
    if not (cid and csec):
        return False, "YOUTUBE_CLIENT_ID + YOUTUBE_CLIENT_SECRET fehlen in der .env"
    try:
        async with aiohttp.ClientSession() as s:
            async with s.post(TOKEN, data={
                    "client_id": cid, "client_secret": csec,
                    "code": code, "grant_type": "authorization_code",
                    "redirect_uri": (_state.get("last_redirect")
                                     or _state["redirect_uri"])},
                    timeout=aiohttp.ClientTimeout(total=15)) as r:
                j = await r.json(content_type=None)
    except Exception as e:
        return False, f"Netzwerkfehler: {e}"
    rt = j.get("refresh_token")
    at = j.get("access_token")
    if not rt:
        # Haeufigster Fall: die App wurde schon einmal autorisiert und
        # prompt=consent fehlte. Das explizit sagen, statt den Google-
        # Fehlertext durchzureichen — der hilft hier niemandem.
        detail = j.get("error_description") or j.get("error") or "?"
        return False, ("Google gab keinen Refresh-Token (%s). Meist heisst das: "
                       "die App war schon autorisiert. Unter "
                       "myaccount.google.com/permissions den Zugriff entziehen "
                       "und erneut verbinden." % detail)
    _state["refresh"] = rt
    _state["access"] = at or ""
    _state["access_exp"] = time.time() + int(j.get("expires_in", 3600)) - 120
    _save()
    return True, ("YouTube verbunden — Refresh-Token gespeichert. "
                  "Zuschauer/Abonnenten und der KI-Moderator im Live-Chat "
                  "sind jetzt aktiv.")


async def access_token(aiohttp):
    """Laufzeit-Token. Erneuert sich selbst per Refresh-Token.

    Gegenstueck zu _twoauth.access_token(). Google liefert beim Refresh
    KEINEN neuen refresh_token — der alte bleibt in Kraft."""
    now = time.time()
    if _state["access"] and now < _state["access_exp"]:
        return _state["access"]
    cid, csec = _client()
    if not (cid and csec and _state["refresh"]):
        return None
    try:
        async with aiohttp.ClientSession() as s:
            async with s.post(TOKEN, data={
                    "client_id": cid, "client_secret": csec,
                    "refresh_token": _state["refresh"],
                    "grant_type": "refresh_token"},
                    timeout=aiohttp.ClientTimeout(total=15)) as r:
                j = await r.json(content_type=None)
    except Exception as e:
        log.debug("ytoauth: Refresh-Fehler: %s", e)
        return None
    at = j.get("access_token")
    if not at:
        err = j.get("error", "?")
        if err == "invalid_grant":
            # Der Refresh-Token ist tot: Zugriff entzogen, Passwort
            # geaendert, oder die App steht auf "Testing" (7-Tage-Ablauf).
            #
            # v4.2-W9: frueher wurde er NUR im Speicher geleert. Auf der
            # Platte blieb er stehen — und beim naechsten Neustart las _load()
            # den toten Token zurueck, status() meldete "ready", das Panel
            # zeigte "verbunden" und kein einziger Aufruf ging durch. Genau
            # das ist das Bild "muss staendig neu verbinden": der gespeicherte
            # Zustand log ueber die Wirklichkeit.
            #
            # Jetzt raeumt forget() beides ab. Platte und Speicher sagen
            # dasselbe, und status() traegt das WARUM.
            # Reihenfolge: erst raeumen, dann den Grund setzen — forget()
            # loescht ihn absichtlich mit, damit eine Handabmeldung keinen
            # alten Fehler stehen laesst.
            forget()
            _merke_fehler("Refresh-Token abgelehnt (invalid_grant)")
            log.error("ytoauth: Refresh-Token abgelehnt (invalid_grant) — "
                      "Verbindung geloest, im Dashboard neu verbinden. "
                      "Steht die Google-App noch auf 'Testing'? Dann laufen "
                      "Refresh-Tokens nach 7 Tagen ab; auf 'In production' "
                      "setzen, sonst wiederholt sich das jede Woche.")
        else:
            # KEIN Loeschen: eine Stoerung bei Google (5xx, Zeitablauf,
            # Netzwerk) ist kein toter Token. Wer hier aufraeumt, wirft eine
            # funktionierende Verbindung wegen eines Schluckaufs weg.
            log.debug("ytoauth: kein Access-Token (%s)", err)
        return None
    _state["access"] = at
    _state["access_exp"] = now + int(j.get("expires_in", 3600)) - 120
    return at


async def upload_clip(aiohttp, dateipfad, titel, beschreibung=""):
    """v4.2-W29: einen lokalen Clip als YouTube-Video hochladen. -> (ok, url_oder_grund)

    ANDERS als Twitch: YouTube nimmt eine echte Datei entgegen (kein
    Live-Cut), dafuer in zwei Schritten — resumable Upload:
      1. POST an UPLOAD_INIT mit den Metadaten (JSON) legt die Session an
         und liefert die Upload-URL im Location-Header.
      2. PUT der Videodatei an genau diese URL.
    Ein Fehlschlag in Schritt 1 (401/403/Quota) darf keinen Schritt 2
    ausloesen — das waere ein Upload ohne gueltige Session.

    privacyStatus bewusst 'unlisted', nicht 'public': ein automatisch
    getriggerter Upload (Meme/Gift/Chat-Velocity) landet sonst ungefiltert
    im oeffentlichen Kanal-Feed und im Abo-Feed der Zuschauer. 'unlisted'
    bleibt ueber den Link teilbar (z.B. im selben Discord-Post wie der
    lokale Clip) ohne den Kanal zuzuspammen.
    """
    tok = await access_token(aiohttp)
    if not tok:
        return False, "kein Token"
    if not os.path.isfile(dateipfad):
        return False, "Datei fehlt"
    meta = {
        "snippet": {"title": (titel or "Clip")[:100],
                    "description": (beschreibung or "")[:4900],
                    "categoryId": "24"},          # 24 = Entertainment
        "status": {"privacyStatus": "unlisted", "selfDeclaredMadeForKids": False},
    }
    groesse = os.path.getsize(dateipfad)
    hdr = {"Authorization": f"Bearer {tok}",
           "Content-Type": "application/json; charset=UTF-8",
           "X-Upload-Content-Type": "video/mp4",
           "X-Upload-Content-Length": str(groesse)}
    try:
        async with aiohttp.ClientSession() as s:
            async with s.post(UPLOAD_INIT, headers=hdr, json=meta,
                              timeout=aiohttp.ClientTimeout(total=15)) as r:
                if r.status == 401:
                    return False, "401 — Scope youtube.upload fehlt, YouTube neu verbinden"
                if r.status == 403:
                    txt = (await r.text())[:200]
                    if "quota" in txt.lower():
                        return False, "403 — Tageskontingent aufgebraucht"
                    return False, f"403: {txt}"
                if r.status != 200:
                    return False, f"HTTP {r.status}: {(await r.text())[:200]}"
                ort = r.headers.get("Location")
            if not ort:
                return False, "keine Upload-Session-URL erhalten"
            with open(dateipfad, "rb") as f:
                daten = f.read()
            async with s.put(ort, data=daten, headers={"Content-Type": "video/mp4"},
                             timeout=aiohttp.ClientTimeout(total=120)) as r2:
                if r2.status not in (200, 201):
                    return False, f"Upload HTTP {r2.status}: {(await r2.text())[:200]}"
                j = await r2.json(content_type=None)
    except Exception as e:
        return False, str(e)
    vid = j.get("id")
    if not vid:
        return False, "YouTube meldet Erfolg ohne Video-ID"
    return True, f"https://youtu.be/{vid}"


def invalidate_access():
    """Access-Token verwerfen, Refresh-Token behalten.

    Warum: bot.py setzte bei 401/403 nur _YT_SEND["token_exp"]=0 — das ist
    aber nur der Cache des Bots. access_token() hier gab danach denselben
    zwischengespeicherten Token bis zu 50 Minuten weiter zurueck, weil
    _state["access_exp"] unberuehrt blieb. Die Invalidierung war damit
    wirkungslos und der Bot lief in genau dieselbe 401 zurueck.
    """
    _state["access"] = ""
    _state["access_exp"] = 0.0


async def revoke(aiohttp):
    """Google-Abmeldung: den Zugriff BEI GOOGLE zurueckziehen, nicht nur lokal
    vergessen. -> (ok, meldung)

    WARUM das noetig ist: forget() loescht nur unseren Refresh-Token. Die
    Freigabe im Google-Konto bleibt bestehen — der naechste Verbindungsversuch
    laeuft dann still durch dieselbe Zustimmung, und wer das Konto WECHSELN
    will, kommt nicht heran, ohne von Hand auf myaccount.google.com den
    Zugriff zu entziehen. Genau dieser Schritt fehlte im Dashboard.

    Nach dem Widerruf ist der Refresh-Token tot; die Zustimmung wird beim
    naechsten Verbinden neu abgefragt, samt Kontoauswahl.

    Der lokale Zustand wird IMMER geleert — auch wenn Google nicht erreichbar
    war. Sonst haette der Betreiber einen Knopf, der bei Netzfehlern gar
    nichts tut, und der Zustand im Dashboard bliebe auf 'verbunden'.
    """
    tok = (_state.get("refresh") or "").strip() or (_state.get("access") or "").strip()
    if not tok:
        forget()
        return True, "Es war keine Verbindung gespeichert — Zustand ist jetzt leer."
    ok, meldung = True, ("Google-Zugriff widerrufen. Beim naechsten Verbinden "
                         "fragt Google wieder nach Konto und Zustimmung.")
    try:
        async with aiohttp.ClientSession() as s:
            async with s.post(REVOKE, data={"token": tok},
                              timeout=aiohttp.ClientTimeout(total=15)) as r:
                if r.status not in (200, 204):
                    body = (await r.text())[:200]
                    # 400 heisst bei Google meist "Token war ohnehin schon
                    # ungueltig" — kein Grund zur Panik, aber sagen muss man es.
                    ok = (r.status == 400)
                    meldung = (f"Google antwortete mit {r.status}: {body}. "
                               f"Lokal ist die Verbindung trotzdem geloest; "
                               f"zur Sicherheit unter myaccount.google.com/permissions "
                               f"nachsehen.")
    except Exception as e:
        ok = False
        meldung = (f"Google nicht erreichbar ({e}). Lokal ist die Verbindung "
                   f"geloest — die Freigabe im Google-Konto besteht evtl. weiter.")
    finally:
        forget()
    return ok, meldung


def forget():
    """Verbindung loesen: Refresh-Token verwerfen und Store loeschen.

    Der EINZIGE Weg, eine gespeicherte Verbindung loszuwerden. _save()
    schreibt seit v4.2-W9 nur noch Verbindungen, nie ihre Abwesenheit —
    sonst konnte ein Kanalname den Store leeren.
    """
    _state.update(refresh="", access="", access_exp=0.0, channel="",
                  last_error="", last_error_ts=0.0)
    p = _state.get("store_path")
    if p and os.path.exists(p):
        try:
            os.remove(p)
        except OSError as e:
            log.warning("ytoauth: Store nicht loeschbar: %s", e)
    return True


def set_channel(name):
    """Kanalname aus der API merken (nur Anzeige im Dashboard)."""
    n = (name or "").strip()
    if n and n != _state.get("channel"):
        _state["channel"] = n
        _save()
