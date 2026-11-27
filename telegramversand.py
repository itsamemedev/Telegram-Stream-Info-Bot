"""telegramversand.py — der Versandweg der Aufnahmen (v4.2-W19).

381 Zeilen, die eine fertige Aufnahme nach Telegram bringen: teilen, hochladen,
auf Sperren und Fehler reagieren, das Thema im Forum treffen, tote Chats
merken. Zusammen mit nc/videoteil.py (W11, das ffmpeg-Teilen) ist das der
komplette Weg von der Datei zum Abonnenten.

**Warum bot-seitig und nicht unter nc/** — dieselbe Grenze wie bei
discordbot.py (W15): die Datei faengt `telegram.error`-Ausnahmen ab und
braucht die echten Klassen zur Laufzeit. `nc/*` bleibt bot-frei, und der
Vertrags-Job der CI installiert dort nur orjson und flask; ein
`from telegram.error import …` unter nc/ haette ihn an einem nackten
ImportError sterben lassen, ohne dass ein einziger Vertrag laeuft.
Die Grenze in die andere Richtung gilt auch hier: **kein `from bot import`.**

Der Rumpf ist ZEICHENGLEICH aus bot.py uebernommen; die fuenf Helfer, die
dort bleiben, werden als Modul-Globale belegt. Begruendung wie in W15/W16/W17:
ein Umschreiben auf Attributzugriffe haette jede Zeile zu einer moeglichen
Regression gemacht, fuer einen Pfad, den hier nichts wirklich ausfuehren kann
— es gibt weder ffmpeg noch einen Telegram-Server.

**Was dieser Pfad im Betrieb schon gekostet hat:** eine Chat-ID, die Telegram
mit `chat not found` beantwortet, laesst jeden Upload scheitern. Ohne die
Tot-Markierung unten laeuft der Bot dann fuer JEDE Aufnahme durch die
komplette Teil- und Retry-Kette, bevor er aufgibt.
"""

import asyncio
import logging
import os
import re

from telegram.constants import ParseMode
from telegram.error import (
    BadRequest, ChatMigrated, Forbidden, NetworkError, RetryAfter, TelegramError,
)

from nc import videoteil as _nc_videoteil
from nc.textmore import _video_caption
from nc.textutil import safe

log = logging.getLogger("TikTokBot")

# ══════════════════════════════════════════════════════════════════════════
# Vom Bot belegt — siehe konfiguriere(). Vorher None: ein Zugriff davor soll
# krachen und nicht still eine Aufnahme verschlucken.
# ══════════════════════════════════════════════════════════════════════════
_chat_migriert = None   # v4.2-W175: Gruppe wurde Supergruppe -> Trackings umschreiben
_ensure_topic = None    # legt das Forum-Thema des Users an bzw. findet es
_is_dead = None         # ist dieser Chat als unerreichbar gemerkt?
_mark_dead = None       # Chat als unerreichbar merken
_safe_send = None       # Textversand mit denselben Sperr-/Fehlerregeln
_topic_forget = None    # gemerktes Thema verwerfen (Forum geloescht/umgebaut)

_PFLICHT = ("chat_migriert", "ensure_topic", "is_dead", "mark_dead", "safe_send",
            "topic_forget")


def konfiguriere(**kw):
    """Der Bot reicht seine fuenf Helfer einmal beim Start herein.

    Unbekannte UND fehlende Schluessel sind ein Fehler: ein stiller None
    hiesse hier, dass eine fertige Aufnahme beim Versand mit
    `NoneType is not callable` verschwindet — nach der Aufnahme, also genau
    dann, wenn die Daten schon da sind und nur noch rausgehen muessen.
    """
    unbekannt = sorted(set(kw) - set(_PFLICHT))
    fehlt = sorted(set(_PFLICHT) - set(kw))
    if unbekannt or fehlt:
        raise ValueError(
            "telegramversand.konfiguriere: unbekannt=%s fehlt=%s" % (unbekannt, fehlt))
    g = globals()
    for k, v in kw.items():
        g["_" + k] = v


async def split_and_send_video(chat_id, filepath, bot_app, username,
                               started_at=None, ended_at=None, ergebnis=None):
    """F28: Upload mit großzügigen Timeouts + Telegram-spezifischer Error-Behandlung.
       PTB v21 default write_timeout=20s ist zu kurz für 50 MB Files auf
       normalen DSL-Uplinks (würde TimedOut werfen). Wir setzen ausreichend
       Reserve und melden Probleme zurück damit der User nicht stillschweigend
       auf Uploads wartet die nie kommen."""
    # v4.2-W132: die Sperre VOR dem Zerlegen fragen. Bisher las erst
    # _send_one() sie — nach einem vollstaendigen ffmpeg-Durchgang ueber die
    # Aufnahme. Am 30.10. zerlegte die Box so Aufnahmen bis 1,5 GB, nur um
    # beim ersten Teil "abgebrochen" zu melden, und das bei Load 7,9 neben
    # einem laufenden Restream. Die Datei bleibt liegen; nichts geht verloren.
    if _is_dead(chat_id):
        _grund = ("Chat-ID gesperrt (zuvor 'chat not found' oder keine "
                  "Telegram-ID) — Upload übersprungen. TELEGRAM_CHAT_ID bzw. "
                  "das Tracking prüfen.")
        log.error("Upload @%s fehlgeschlagen: %s Die Aufnahme bleibt auf dem "
                  "Server: %s", username, _grund, filepath)
        # Derselbe Meldeweg wie bisher nach dem Zerlegen: _safe_send kennt
        # die Sperre selbst und verwirft die Zeile, wenn der Chat tot ist —
        # und wirft nie (Vertrag von bot._safe_send).
        await _safe_send(
            bot_app.bot, chat_id,
            f"⚠ <b>UPLOAD FEHLGESCHLAGEN · @{safe(username)}</b>\n"
            f"<code>{safe(_grund)}</code>",
            parse_mode=ParseMode.HTML, disable_notification=True)
        return
    # Timeouts: writes können bei 50 MB auf 8 Mbit/s = ~50s dauern. Mit Reserve.
    UPLOAD_TIMEOUTS = dict(
        read_timeout=120,       # Antwort von Telegram
        write_timeout=600,      # File-Upload selbst (10 min für lahmen Upload OK)
        connect_timeout=30,
        pool_timeout=10,
    )
    # Forum-Topic (Sub-Channel) pro User: Uploads in ein nach @username benanntes
    # Topic legen → je User sortiert. Kein Forum / keine Rechte → None, dann ganz
    # normal in den Chat. message_thread_id steckt mit in UPLOAD_TIMEOUTS und wird
    # so in JEDEN send_video-Aufruf (inkl. aller Retry-Pfade) gespreadet.
    _topic_tid = await _ensure_topic(chat_id, username, bot_app.bot)
    if _topic_tid:
        UPLOAD_TIMEOUTS["message_thread_id"] = _topic_tid

    # v4.2-W168: `ergebnis` (dict) zaehlt gesendete und gescheiterte Teile.
    # Der Topic-Umzug loescht ein altes Topic nur, wenn das Neu-Hochladen
    # nachweislich durchging — und diese Funktion sagte das bisher niemandem.
    # Gezaehlt wird an der EINEN Stelle, durch die jeder Teil geht.
    if ergebnis is not None:
        ergebnis.setdefault("gesendet", 0)
        ergebnis.setdefault("fehler", 0)

    async def _send_one(fh_or_path, caption):
        ok, err = await _send_one_roh(fh_or_path, caption)
        if ergebnis is not None:
            ergebnis["gesendet" if ok else "fehler"] += 1
            if not ok:
                ergebnis["grund"] = err
        return ok, err

    def _fehlschlag(grund):
        # v4.2-W175: Fehler, die nicht durch _send_one gehen (Teil zu gross,
        # Split gescheitert, Absturz), zaehlten nicht. Ein uebersprungener
        # Teil neben gesendeten sah damit aus wie ein voller Erfolg, und die
        # Warteschlange (nc/uploadschlange) haette den Eintrag entfernt.
        if ergebnis is not None:
            ergebnis["fehler"] += 1
            ergebnis["grund"] = grund

    async def _send_one_roh(fh_or_path, caption):
        # v4.2-W175: wird die Gruppe zur Supergruppe, gilt ab dem naechsten
        # Teil die neue ID — fuer den Versand UND die Fehlermeldungen unten.
        nonlocal chat_id
        # V37-B97: _mark_dead() setzt bei 'chat not found' längst eine Sperre,
        # aber nur _safe_send() (Textnachrichten) hat sie je gelesen. Der
        # Video-Upload rannte für JEDEN Part jeder Aufnahme erneut hinein —
        # im Log: 176× dieselbe Fehlermeldung in einer Nacht.
        if _is_dead(chat_id):
            return False, ("Chat-ID gesperrt (zuvor 'chat not found') — "
                           "Upload übersprungen. TELEGRAM_CHAT_ID prüfen: der Bot "
                           "muss Mitglied des Chats sein und ihn einmal gesehen haben.")
        """Wrapper mit Telegram-spezifischer Error-Behandlung."""
        try:
            await bot_app.bot.send_video(
                chat_id, fh_or_path,
                caption=caption,
                parse_mode=ParseMode.HTML,
                supports_streaming=True,
                **UPLOAD_TIMEOUTS)
            return True, None
        except RetryAfter as e:
            wait = getattr(e, 'retry_after', 30)
            log.warning(f"Telegram RetryAfter {wait}s — warte und versuche erneut")
            await asyncio.sleep(min(wait + 1, 120))
            # einmaliger Retry
            try:
                if hasattr(fh_or_path, 'seek'):
                    fh_or_path.seek(0)
                await bot_app.bot.send_video(
                    chat_id, fh_or_path,
                    caption=caption,
                    parse_mode=ParseMode.HTML,
                    supports_streaming=True,
                    **UPLOAD_TIMEOUTS)
                return True, None
            except Exception as e2:
                return False, f"nach RetryAfter erneut gescheitert: {e2}"
        except Forbidden as e:
            # User hat den Bot blockiert oder Chat ist nicht erreichbar
            _mark_dead(chat_id)
            return False, f"Chat verloren (Forbidden): {e}"
        except BadRequest as e:
            msg = str(e).lower()
            # B46: Aus dem Live-Log: "BadRequest: Too many requests: retry after 8"
            # PTB wickelt manche 429-Antworten als BadRequest statt RetryAfter →
            # wir kriegen den RetryAfter-Pfad nie zu sehen. Hier explizit
            # erkennen + wie RetryAfter behandeln (sleep + einmaliger Retry).
            if 'too many requests' in msg or 'retry after' in msg:
                # Versuch retry-after-Wert zu extrahieren
                m = re.search(r'retry after (\d+)', msg)
                wait = int(m.group(1)) if m else 15
                log.warning(f"Telegram Rate-Limit als BadRequest gemeldet — "
                            f"warte {wait}s und versuche erneut")
                await asyncio.sleep(min(wait + 1, 120))
                try:
                    if hasattr(fh_or_path, 'seek'):
                        fh_or_path.seek(0)
                    await bot_app.bot.send_video(
                        chat_id, fh_or_path,
                        caption=caption,
                        parse_mode=ParseMode.HTML,
                        supports_streaming=True,
                        **UPLOAD_TIMEOUTS)
                    return True, None
                except Exception as e2:
                    return False, f"nach Rate-Limit-Wait erneut gescheitert: {e2}"
            if 'file is too big' in msg or 'too large' in msg or 'request entity too large' in msg:
                return False, f"Datei zu groß für Telegram (limit 50 MB für Bots): {e}"
            if 'chat not found' in msg or 'peer_id_invalid' in msg:
                _mark_dead(chat_id)
                return False, f"Chat-ID ungültig: {e}"
            if (UPLOAD_TIMEOUTS.get("message_thread_id") and
                ('thread not found' in msg or 'message thread' in msg or
                 'topic_deleted' in msg or 'topic was deleted' in msg or
                 'topic_closed' in msg or 'topic is closed' in msg)):
                # Topic wurde gelöscht/geschlossen → Mapping verwerfen und OHNE
                # Thread in den Haupt-Chat senden, statt den Upload zu verlieren.
                _topic_forget(chat_id, username)
                UPLOAD_TIMEOUTS.pop("message_thread_id", None)
                log.info(f"Topic für @{username} weg → Upload geht in den Haupt-Chat")
                try:
                    if hasattr(fh_or_path, 'seek'): fh_or_path.seek(0)
                    await bot_app.bot.send_video(
                        chat_id, fh_or_path, caption=caption,
                        parse_mode=ParseMode.HTML, supports_streaming=True,
                        **UPLOAD_TIMEOUTS)
                    return True, None
                except Exception as e2:
                    return False, f"Topic weg, Fallback-Send fehlgeschlagen: {e2}"
            return False, f"BadRequest: {e}"
        except (NetworkError, asyncio.TimeoutError) as e:
            msg = str(e).lower()
            if 'too large' in msg or 'entity too large' in msg or '413' in msg:
                return False, f"Datei zu groß für Telegram (limit 50 MB für Bots): {e}"
            # VERBESSERUNG: Transiente Netzwerkfehler (httpx.ReadError) einmal
            # automatisch retried statt sofort aufgeben.
            log.warning(f"Upload Netzwerk/Timeout ({e}) — Retry in 8s")
            await asyncio.sleep(8)
            try:
                if hasattr(fh_or_path, 'seek'):
                    fh_or_path.seek(0)
                await bot_app.bot.send_video(
                    chat_id, fh_or_path,
                    caption=caption,
                    parse_mode=ParseMode.HTML,
                    supports_streaming=True,
                    **UPLOAD_TIMEOUTS)
                return True, None
            except Exception as e2:
                return False, f"Netzwerk/Timeout (auch nach Retry): {e2}"
        except ChatMigrated as e:
            # v4.2-W175: bisher „Telegram: …" je Teil, und das fuer jede
            # Aufnahme — die alte Gruppen-ID nimmt nie wieder etwas an.
            alt, neu = chat_id, getattr(e, "new_chat_id", None)
            if not neu:
                return False, f"Chat migriert, neue ID unbekannt: {e}"
            await _chat_migriert(alt, neu)
            chat_id = neu
            UPLOAD_TIMEOUTS.pop("message_thread_id", None)   # Thema der alten Gruppe
            try:
                if hasattr(fh_or_path, 'seek'):
                    fh_or_path.seek(0)
                await bot_app.bot.send_video(
                    chat_id, fh_or_path, caption=caption,
                    parse_mode=ParseMode.HTML, supports_streaming=True,
                    **UPLOAD_TIMEOUTS)
                return True, None
            except Exception as e2:
                log.error("Upload @%s: Versand nach Umwandlung %s → %s gescheitert: %s",
                          username, alt, neu, e2)
                return False, f"Chat migriert ({alt} → {neu}), erneuter Versand gescheitert: {e2}"
        except TelegramError as e:
            return False, f"Telegram: {e}"

    # v4.2-W11: das ffmpeg-Handwerk liegt in nc/videoteil.py — messen,
    # teilen, notfalls neu kodieren, kaputte Container reparieren. Hier bleibt
    # nur, was Telegram kennt: Versand, Bildunterschrift, Fehlermeldung.
    # v5.12: das Teilen selbst steht in _teile_bereiten (unten) und laeuft je
    # Aufnahme EINMAL, auch wenn mehrere Chats gleichzeitig hochladen.
    _geholt = False
    try:
        size_mb = os.path.getsize(filepath) / 1024 / 1024
        log.info(f"Upload @{username}: {filepath} ({size_mb:.1f} MB) → chat {chat_id}")

        # Single-File-Pfad nur wenn die Datei selbst unter Telegram-Hard-Limit liegt
        if size_mb <= _nc_videoteil.ZIEL_TEIL_MB:
            with open(filepath, "rb") as fh:                          # C5
                ok, err = await _send_one(
                    fh, _video_caption(username, started_at, ended_at, size_mb))
            if ok:
                log.info(f"Upload @{username} OK ({size_mb:.1f} MB)")
            else:
                log.error(f"Upload @{username} fehlgeschlagen: {err}")
                try:
                    await _safe_send(
                        bot_app.bot, chat_id,
                        f"⚠ <b>UPLOAD FEHLGESCHLAGEN · @{safe(username)}</b>\n"
                        f"<i>Aufnahme liegt auf Server ({size_mb:.0f} MB)</i>\n"
                        f"<code>{safe((err or '')[:200])}</code>",
                        parse_mode=ParseMode.HTML, disable_notification=True)
                except Exception: pass
            return

        # Multi-Part-Pfad: die Teile kommen aus der gemeinsamen Vorbereitung.
        _geholt = True
        vorbereitet = await _teile_holen(filepath, username)
        if vorbereitet.get("fehler"):
            _fehlschlag(vorbereitet["fehler"])
            try:
                await _safe_send(bot_app.bot, chat_id, vorbereitet["meldung"],
                                 parse_mode=ParseMode.HTML, disable_notification=True)
            except Exception: pass
            return
        part_files = vorbereitet["teile"]

        total = len(part_files)
        sent_count = 0
        pause = teil_pause_s()
        for i, part in enumerate(part_files, 1):
            part_size_mb = os.path.getsize(part) / 1024 / 1024
            # Letzter Safety-Check vor Upload: wenn Part immer noch > Hard-Limit,
            # gar nicht erst versuchen (würde 413 zurückkommen)
            if part_size_mb > _nc_videoteil.TELEGRAM_HARD_MB:
                log.error(f"part {i}/{total} bleibt {part_size_mb:.1f} MB > "
                          f"{_nc_videoteil.TELEGRAM_HARD_MB} MB hard limit — skip")
                _fehlschlag(f"Teil {i}/{total} bleibt {part_size_mb:.0f} MB")
                try:
                    await _safe_send(
                        bot_app.bot, chat_id,
                        f"⚠ <b>PART {i}/{total} ÜBERSPRUNGEN · @{safe(username)}</b>\n"
                        f"<i>Part wäre {part_size_mb:.0f} MB — überschreitet Telegram-Bot-Limit (50 MB)</i>",
                        parse_mode=ParseMode.HTML, disable_notification=True)
                except Exception: pass
                continue

            # v5.12: kein os.remove je Teil mehr — andere Chats lesen dieselben
            # Teile gleichzeitig. Weg kommen sie, wenn der LETZTE fertig ist
            # (_teile_freigeben im finally unten).
            with open(part, "rb") as fh:                          # C5
                ok, err = await _send_one(
                    fh, _video_caption(username, started_at, ended_at,
                                       part_size_mb, part=i, total_parts=total))
            if ok:
                sent_count += 1
            else:
                # V37-B97: tote Chat-ID → EINMAL melden und abbrechen. Vorher
                # scheiterte jeder Part einzeln und schickte die Fehlermeldung
                # auch noch an genau den Chat, den es nicht gibt.
                if _is_dead(chat_id):
                    log.error("Upload @%s abgebrochen: Chat-ID %s ungültig "
                              "('chat not found'). Kein Retry für die restlichen "
                              "%d Parts. TELEGRAM_CHAT_ID prüfen.",
                              username, chat_id, total - i + 1)
                    break
                log.error(f"Upload part {i}/{total} fehlgeschlagen: {err}")
                try:
                    await _safe_send(
                        bot_app.bot, chat_id,
                        f"⚠ <b>PART {i}/{total} FEHLGESCHLAGEN · @{safe(username)}</b>\n"
                        f"<code>{safe((err or '')[:200])}</code>",
                        parse_mode=ParseMode.HTML, disable_notification=True)
                except Exception: pass

            # F34: Pause zwischen Parts. Schützt vor Telegram-Rate-Limiting
            # (FloodWait) bei großen Aufnahmen mit vielen Parts. v5.12: 3 statt
            # 5 s, einstellbar (teil_pause_s) — sie gilt je Chat; verschiedene
            # Chats laden gleichzeitig.
            if i < total:
                await asyncio.sleep(pause)

        log.info(f"Upload @{username} → {chat_id}: {sent_count}/{total} parts erfolgreich")
    except Exception as e:
        # Letzter Auffang — z.B. wenn os.path.getsize crasht
        log.error(f"Video-Splitting/-Upload crash: {e}", exc_info=True)
        _fehlschlag(f"Absturz: {e}")
    finally:
        # AUF-5: die Teile gehen auf JEDEM Ausstieg weg — seit v5.12, sobald der
        # letzte Chat dieser Aufnahme fertig (oder abgebrochen) ist.
        if _geholt:
            _teile_freigeben(filepath)


# ══════════════════════════════════════════════════════════════════════════
# v5.12: EINE Vorbereitung je Aufnahme, egal wie viele Chats.
# ══════════════════════════════════════════════════════════════════════════
# bot._aufnahme_verteilen startet die Uploads an alle Chats gleichzeitig. Bis
# dahin teilte jeder Chat die Aufnahme neu, unter DEMSELBEN Praefix
# `<datei>_part` — nacheinander ging das, gleichzeitig haette der zweite
# Split die Teile des ersten ueberschrieben und dessen Aufraeumen sie mitten im
# Upload geloescht. Dazu waere jeder ffmpeg-Durchgang N-mal gelaufen, auf einer
# Box, die ihn schon einmal kaum vertrug (W132: Load 7,9 neben einem Restream).
# Wer zuerst kommt, bereitet vor; alle anderen warten auf dasselbe Ergebnis;
# der letzte raeumt auf.
_GEMEINSAM = {}          # Aufnahmepfad -> {"aufgabe": Task, "halter": int}


async def _teile_holen(filepath, username):
    """Die Teile dieser Aufnahme — gemeinsam fuer alle Chats.

    Der Aufrufer ruft danach IMMER _teile_freigeben (auch beim Abbruch); der
    Halter-Zaehler steigt deshalb vor dem Warten. asyncio.shield: bricht EIN
    Chat ab, laeuft die Vorbereitung fuer die anderen weiter."""
    eintrag = _GEMEINSAM.get(filepath)
    if eintrag is None:
        eintrag = {"aufgabe": asyncio.ensure_future(_teile_bereiten(filepath, username)),
                   "halter": 0}
        _GEMEINSAM[filepath] = eintrag
    eintrag["halter"] += 1
    return await asyncio.shield(eintrag["aufgabe"])


def _teile_freigeben(filepath):
    """Ein Chat ist fertig. Der letzte raeumt die Teile weg (AUF-5)."""
    eintrag = _GEMEINSAM.get(filepath)
    if eintrag is None:
        return
    eintrag["halter"] -= 1
    if eintrag["halter"] > 0:
        return
    del _GEMEINSAM[filepath]
    aufgabe = eintrag["aufgabe"]
    if not aufgabe.done():
        # Alle Chats sind weg (Neustart) — die Vorbereitung raeumt im eigenen
        # finally auf, was sie schon angelegt hat.
        aufgabe.cancel()
        return
    if aufgabe.cancelled() or aufgabe.exception() is not None:
        return                          # ebenfalls dort schon geraeumt
    _nc_videoteil.teile_entfernen(aufgabe.result().get("praefix") or f"{filepath}_part")


def teil_pause_s(env=None) -> float:
    """Pause zwischen zwei Teilen an DENSELBEN Chat — UPLOAD_TEIL_PAUSE_S, Vorgabe 3.

    v5.12: 5 → 3 s auf Wunsch des Betreibers. Telegram nimmt in einer Gruppe
    rund 20 Nachrichten je Minute; mit 3 s Pause plus Uploadzeit bleibt jeder
    Chat darunter, und verschiedene Chats zaehlen getrennt. Unter 1 s nicht —
    dann kommt FloodWait, und das Warten darauf kostet mehr als es spart.
    Als Funktion gelesen: .env kommt teils erst nach dem Import (W67)."""
    roh = os.getenv("UPLOAD_TEIL_PAUSE_S", "3") if env is None else env
    try:
        wert = float(str(roh).strip() or "3")
    except ValueError:
        log.warning("UPLOAD_TEIL_PAUSE_S=%r ist keine Zahl — es gilt 3 s.", roh)
        return 3.0
    if wert < 1.0:
        log.warning("UPLOAD_TEIL_PAUSE_S=%s ist unter 1 s — es gilt 1 s (FloodWait).", roh)
        return 1.0
    return wert


def _fehler_meldung(grund, titel, text, username):
    """Ergebnis einer gescheiterten Vorbereitung: der Grund fuer die Zaehlung
    (W175) und die Zeile, die JEDER wartende Chat bekommt."""
    return {"fehler": grund,
            "meldung": f"⚠ <b>{titel} · @{safe(username)}</b>\n{text}"}


async def _teile_bereiten(filepath, username):
    """Teilen, notfalls reparieren und neu kodieren. -> {"teile", "praefix"}
    oder {"fehler", "meldung"}. Laeuft je Aufnahme einmal (_teile_holen).

    Der Rumpf ist der bisherige Mittelteil von split_and_send_video, nur ohne
    Chat: die Fehlermeldung geht an jeden wartenden Chat. Die Teile bleiben
    liegen, bis _teile_freigeben sie wegraeumt; Zwischendateien (.repaired,
    .remux) und die Teile eines gescheiterten Laufs raeumt das finally hier."""
    zwischen = []          # .repaired / .remux — auf jedem Pfad weg (B47, B70+, AUF-5)
    prefix = f"{filepath}_part"
    gelungen = False
    try:
        size_mb = os.path.getsize(filepath) / 1024 / 1024
        # B53: Pre-flight Disk-Check — sonst crasht ffmpeg mitten im Split mit
        # "No space left on device" und wir haben verstreute Half-Parts.
        disk_ok, disk_info = _nc_videoteil.platz_reicht(filepath)
        if not disk_ok:
            log.error(f"split @{username} abgebrochen: {disk_info}")
            return _fehler_meldung(
                f"zu wenig Platz: {disk_info}", "SPLIT ABGEBROCHEN",
                f"<i>Nicht genug Disk-Space: {disk_info}.</i>\n"
                f"<i>Originaldatei bleibt auf Server.</i>", username)
        part_files, split_err, repariert = await _teilen_oder_reparieren(
            filepath, prefix, username, size_mb)
        if repariert:
            zwischen.append(repariert)
            filepath = repariert            # die reparierte Datei ist die Quelle
        if part_files is None:
            log.error(f"ffmpeg split failed: {split_err}")
            return _fehler_meldung(
                "Split gescheitert", "SPLIT FEHLGESCHLAGEN",
                "<i>ffmpeg-Split crashte — Datei liegt komplett auf Server.</i>", username)
        part_files, attempt = await _nachteilen(filepath, prefix, part_files)
        if part_files is None:
            # F42-Bug-Hunt-Fix B3: User-Notif beim Re-Split-Fail. Vorher
            # silent return — der User sah die OFFLINE-Notif "Upload läuft"
            # aber kein Upload kam. Jetzt klare Fehlermeldung.
            return _fehler_meldung(
                "Re-Split gescheitert", "RE-SPLIT FEHLGESCHLAGEN",
                f"<i>ffmpeg-Re-Split (#{attempt}) crashte — "
                f"Datei liegt komplett auf Server ({size_mb:.0f} MB).</i>", username)
        if _nc_videoteil.zu_gross(part_files):
            part_files, re_err = await _neu_kodiert(filepath, prefix, part_files, zwischen)
            if not part_files:
                # BUG-FIX: part_files ist hier leer (alle Parts wurden geloescht).
                # Vorher lief die Versand-Schleife mit [] durch und das Video ging
                # lautlos verloren. Jetzt: explizite Notif + return.
                return _fehler_meldung(
                    "Neu-Kodieren gescheitert", "UPLOAD NICHT MÖGLICH",
                    f"<i>Copy-Split und Re-Encode-Fallback beide fehlgeschlagen.\n"
                    f"Datei ({size_mb:.0f} MB) liegt komplett auf dem Server.</i>\n"
                    f"<code>{safe((re_err or '')[:200])}</code>", username)
        gelungen = True
        return {"teile": part_files, "praefix": prefix}
    finally:
        # Zwischendateien gehen auf JEDEM Pfad weg; die Teile nur, wenn die
        # Vorbereitung nicht gelang — sonst gehoeren sie den wartenden Chats,
        # bis _teile_freigeben sie raeumt. Seit v5.12 geht auch die B47-
        # Reparatur direkt nach dem Teilen weg: die Teile tragen den Inhalt.
        # v5.12.1: im Thread — .remux/.repaired sind so gross wie die
        # Aufnahme, und Loeschen auf voller Platte haelt sonst den Loop an.
        await asyncio.to_thread(_nc_videoteil.wegwerfen, zwischen)
        if not gelungen:
            await asyncio.to_thread(_nc_videoteil.teile_entfernen, prefix)


async def _teilen_oder_reparieren(filepath, prefix, username, size_mb):
    """Erster Split; bei kaputtem Container reparieren und noch einmal.
    -> (teile oder None, fehlertext, reparierte Datei oder None)

    B47: "moov atom not found" / "Invalid data found when processing input"
    → die Quelle ist korrupt (ffmpeg wurde mit SIGKILL beendet, bevor er das
    moov-atom schreiben konnte, z.B. durch unseren Stall-Watchdog). Repair:
    mit -err_detect ignore_err lesen und neu muxen. Die reparierte Datei
    (~Originalgroesse) blieb frueher nach dem Upload liegen — sie wird jetzt
    vom Aufrufer im finally entfernt."""
    part_files, split_err = await _nc_videoteil.kopier_teilen(
        filepath, prefix, _nc_videoteil.ZIEL_TEIL_MB)
    if part_files is not None or not _nc_videoteil.ist_kaputter_container(split_err):
        return part_files, split_err, None
    log.warning(f"split @{username}: moov-atom-Fehler erkannt — versuche MP4-Repair")
    repaired = filepath + ".repaired.mp4"
    rep_ok, rep_err = await _nc_videoteil.reparieren(filepath, repaired)
    if not rep_ok:
        log.error("B47 Repair fehlgeschlagen für @%s: %s", username, rep_err or "?")
        return None, split_err, None
    rep_size_mb = os.path.getsize(repaired) / 1024 / 1024
    log.warning(f"B47 Repair OK: {rep_size_mb:.1f} MB nach Repair "
                f"(Original war {size_mb:.1f} MB) — retry split")
    part_files, split_err = await _nc_videoteil.kopier_teilen(
        repaired, prefix, _nc_videoteil.ZIEL_TEIL_MB)
    return part_files, split_err, repaired


async def _nachteilen(filepath, prefix, part_files):
    """Zu grosse Teile mit halbiertem Ziel neu teilen. -> (teile oder None, versuch)

    F28-Bug-Fix B42: VBR-Streams haben Burst-Sections (z.B. Action-Szene in
    der Aufnahme) mit deutlich höherer Bitrate als der Durchschnitt; die
    avg_mb_per_sec-Rechnung produziert dann für genau diese Sections einen
    Part weit über target_mb. Im Live-Log gesehen: part 7/7 blieb 362.6 MB >
    50 MB nach einem Re-Split. Deshalb iterativ halbieren, bis alle Parts
    unter dem Limit sind oder target_mb < 5 (max 4 Halbierungen: 22, 11, 5, 2 MB)."""
    max_resplits = 4
    attempt = 0
    cur_target = _nc_videoteil.ZIEL_TEIL_MB
    while attempt < max_resplits:
        oversized = _nc_videoteil.zu_gross(part_files)
        if not oversized:
            break
        attempt += 1
        cur_target = max(5, cur_target // 2)
        log.warning(f"split: {len(oversized)} part(s) > "
                    f"{_nc_videoteil.TELEGRAM_HARD_MB} MB "
                    f"— re-split #{attempt} mit target={cur_target} MB")
        # Reste löschen + neuer Versuch (v5.12.1: im Thread, s. nc/videoteil)
        await asyncio.to_thread(_nc_videoteil.wegwerfen, part_files)
        part_files, split_err = await _nc_videoteil.kopier_teilen(
            filepath, prefix, cur_target)
        if part_files is None:
            log.error(f"re-split #{attempt} failed: {split_err}")
            return None, attempt
    return part_files, attempt


async def _neu_kodiert(filepath, prefix, part_files, zwischen):
    """B70: Copy-Split bekommt die Parts nicht klein genug (zu wenige Keyframes,
    Symptom "part 1/1 bleibt 68 MB") → Re-Encode mit erzwungenen Keyframes.
    -> (teile oder None, fehlertext). Die Re-Mux-Zwischendatei landet in
    `zwischen`, damit der Aufrufer sie auf jedem Pfad wegraeumt (AUF-5)."""
    log.warning(f"split: {len(_nc_videoteil.zu_gross(part_files))} part(s) weiterhin > "
                f"{_nc_videoteil.TELEGRAM_HARD_MB} MB nach Copy-Re-Splits — "
                f"Re-Encode-Fallback (erzwungene Keyframes)")
    await asyncio.to_thread(_nc_videoteil.wegwerfen, part_files)
    # BUG-FIX (B70+): Vor dem Re-Encode erst einen sauberen Re-Mux-Schritt
    # durchführen. Streams mit "pts has no value" / "Non-monotonic DTS"
    # (wie bei @xxxderspender88xxx im Log) bringen den Segment-Muxer in
    # _reencode_segment zum Absturz weil ffmpeg mit -f segment keine
    # kaputten Timestamps toleriert. Ein vorheriger Re-Mux mit
    # -fflags +genpts erzeugt saubere Timestamps → Re-Encode klappt dann.
    remux_path = filepath + ".remux.mp4"
    zwischen.append(remux_path)
    _remux_ok, _rm_err = await _nc_videoteil.zeitstempel_richten(filepath, remux_path)
    if _remux_ok:
        log.info("split: Re-Mux (genpts) OK → Re-Encode auf remuxed file")
    else:
        log.warning("split: Re-Mux fehlgeschlagen (%s) — Re-Encode direkt "
                    "auf Original", _rm_err or "?")
    re_parts, re_err = await _nc_videoteil.neu_kodieren(
        remux_path if _remux_ok else filepath, prefix, _nc_videoteil.ZIEL_TEIL_MB)
    if re_parts:
        log.info(f"split: Re-Encode-Fallback erzeugte {len(re_parts)} Parts")
        return re_parts, None
    log.error(f"split: Re-Encode-Fallback fehlgeschlagen: {re_err} — "
              f"Datei bleibt komplett auf Server")
    return None, re_err
