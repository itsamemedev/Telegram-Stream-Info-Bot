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
import glob
import logging
import os
import re

from telegram.constants import ParseMode
from telegram.error import (
    BadRequest, Forbidden, NetworkError, RetryAfter, TelegramError,
)

from nc import videoteil as _nc_videoteil
from nc.textmore import _video_caption
from nc.textutil import safe

log = logging.getLogger("TikTokBot")

# ══════════════════════════════════════════════════════════════════════════
# Vom Bot belegt — siehe konfiguriere(). Vorher None: ein Zugriff davor soll
# krachen und nicht still eine Aufnahme verschlucken.
# ══════════════════════════════════════════════════════════════════════════
_ensure_topic = None    # legt das Forum-Thema des Users an bzw. findet es
_is_dead = None         # ist dieser Chat als unerreichbar gemerkt?
_mark_dead = None       # Chat als unerreichbar merken
_safe_send = None       # Textversand mit denselben Sperr-/Fehlerregeln
_topic_forget = None    # gemerktes Thema verwerfen (Forum geloescht/umgebaut)

_PFLICHT = ("ensure_topic", "is_dead", "mark_dead", "safe_send", "topic_forget")


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
                               started_at=None, ended_at=None):
    """F28: Upload mit großzügigen Timeouts + Telegram-spezifischer Error-Behandlung.
       PTB v21 default write_timeout=20s ist zu kurz für 50 MB Files auf
       normalen DSL-Uplinks (würde TimedOut werfen). Wir setzen ausreichend
       Reserve und melden Probleme zurück damit der User nicht stillschweigend
       auf Uploads wartet die nie kommen."""
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

    async def _send_one(fh_or_path, caption):
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
        except TelegramError as e:
            return False, f"Telegram: {e}"

    # v4.2-W11: das ffmpeg-Handwerk liegt in nc/videoteil.py — messen,
    # teilen, notfalls neu kodieren, kaputte Container reparieren. Hier bleibt
    # nur, was Telegram kennt: Versand, Bildunterschrift, Fehlermeldung.

    # BUG-FIX: B47-Repair erzeugt eine .repaired.mp4 (~Originalgröße) und macht
    # sie zur neuen Split-Quelle. Vorher wurde sie nach erfolgreichem Repair NIE
    # gelöscht → bei jedem moov-Repair blieb eine vollgroße Dublette liegen (bis
    # der Retention-Cleanup nach RECORDINGS_RETAIN_DAYS Tagen griff). Wir tracken
    # sie und räumen im finally auf — das Original bleibt als reguläre Aufnahme.
    _b47_repaired = None
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
                        f"<code>{safe(err)[:200]}</code>",
                        parse_mode=ParseMode.HTML, disable_notification=True)
                except Exception: pass
            return

        # Multi-Part-Pfad: bitrate-basiert splitten
        prefix = f"{filepath}_part"
        # B53: Pre-flight Disk-Check — sonst crasht ffmpeg mitten im Split mit
        # "No space left on device" und wir haben verstreute Half-Parts.
        disk_ok, disk_info = _nc_videoteil.platz_reicht(filepath)
        if not disk_ok:
            log.error(f"split @{username} abgebrochen: {disk_info}")
            try:
                await _safe_send(
                    bot_app.bot, chat_id,
                    f"⚠ <b>SPLIT ABGEBROCHEN · @{safe(username)}</b>\n"
                    f"<i>Nicht genug Disk-Space: {disk_info}.</i>\n"
                    f"<i>Originaldatei bleibt auf Server.</i>",
                    parse_mode=ParseMode.HTML, disable_notification=True)
            except Exception: pass
            return
        part_files, split_err = await _nc_videoteil.kopier_teilen(
            filepath, prefix, _nc_videoteil.ZIEL_TEIL_MB)
        if part_files is None:
            # B47: "moov atom not found" / "Invalid data found when processing input"
            # → die Quelle-Datei ist korrupt (ffmpeg wurde mit SIGKILL beendet
            # bevor er das moov-atom schreiben konnte, z.B. durch unseren Stall-
            # Watchdog). Repair-Versuch: ffmpeg mit -err_detect ignore_err lesen
            # und neu muxen. Wenn das klappt, retry mit der reparierten Datei.
            is_moov_err = _nc_videoteil.ist_kaputter_container(split_err)
            if is_moov_err:
                log.warning(f"split @{username}: moov-atom-Fehler erkannt — versuche MP4-Repair")
                repaired = filepath + ".repaired.mp4"
                rep_ok, rep_err = await _nc_videoteil.reparieren(filepath, repaired)
                if rep_ok:
                    rep_size_mb = os.path.getsize(repaired) / 1024 / 1024
                    log.warning(f"B47 Repair OK: {rep_size_mb:.1f} MB nach Repair "
                                f"(Original war {size_mb:.1f} MB) — retry split")
                    # Temp im finally aufraeumen; die reparierte Datei wird zur
                    # neuen Split-Quelle.
                    _b47_repaired = repaired
                    filepath = repaired
                    part_files, split_err = await _nc_videoteil.kopier_teilen(
                        filepath, prefix, _nc_videoteil.ZIEL_TEIL_MB)
                else:
                    log.error("B47 Repair fehlgeschlagen für @%s: %s",
                              username, rep_err or "?")
        if part_files is None:
            log.error(f"ffmpeg split failed: {split_err}")
            for orphan in glob.glob(f"{prefix}_*.mp4"):
                try: os.remove(orphan)
                except OSError: pass
            try:
                await _safe_send(
                    bot_app.bot, chat_id,
                    f"⚠ <b>SPLIT FEHLGESCHLAGEN · @{safe(username)}</b>\n"
                    f"<i>ffmpeg-Split crashte — Datei liegt komplett auf Server.</i>",
                    parse_mode=ParseMode.HTML, disable_notification=True)
            except Exception: pass
            return

        # Falls trotz Bitrate-Rechnung ein Part > Hard-Limit → einmal re-splitten
        # mit halbierter Target-Größe.
        # F28-Bug-Fix B42: VBR-Streams haben Burst-Sections (z.B. Action-Szene
        # in der Aufnahme) mit deutlich höherer Bitrate als der Durchschnitt.
        # Die avg_mb_per_sec-Rechnung produziert dann für genau diese Sections
        # einen Part der weit über target_mb liegt. Vorher: einmal halbieren,
        # wenn DAS auch noch zu groß war → skip mit Notif. Im Live-Log
        # gesehen: part 7/7 blieb 362.6 MB > 50 MB Hard-Limit nach einem
        # Re-Split. Jetzt: iterativ halbieren bis alle Parts unter Limit ODER
        # bis target_mb < 5 (dann gibt's keine sinnvolle weitere Halbierung).
        max_resplits = 4   # max 4 Halbierungen: 22, 11, 5, 2 MB
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
            # Reste löschen + neuer Versuch
            _nc_videoteil.wegwerfen(part_files)
            part_files, split_err = await _nc_videoteil.kopier_teilen(
                filepath, prefix, cur_target)
            if part_files is None:
                log.error(f"re-split #{attempt} failed: {split_err}")
                # F42-Bug-Hunt-Fix B3: User-Notif beim Re-Split-Fail. Vorher
                # silent return — der User sah die OFFLINE-Notif "Upload läuft"
                # aber kein Upload kam. Jetzt klare Fehlermeldung.
                try:
                    await _safe_send(
                        bot_app.bot, chat_id,
                        f"⚠ <b>RE-SPLIT FEHLGESCHLAGEN · @{safe(username)}</b>\n"
                        f"<i>ffmpeg-Re-Split (#{attempt}) crashte — "
                        f"Datei liegt komplett auf Server ({size_mb:.0f} MB).</i>",
                        parse_mode=ParseMode.HTML, disable_notification=True)
                except Exception: pass
                return

        # B70-Fix: Wenn Copy-Split die Parts NICHT klein genug bekommt (zu wenige
        # Keyframes → Segment-Muxer kann nicht zwischen ihnen schneiden, Symptom:
        # "part 1/1 bleibt 68 MB"), greift jetzt ein Re-Encode-Fallback mit
        # erzwungenen Keyframes. Vorher wurde der Part einfach übersprungen.
        still_oversized = _nc_videoteil.zu_gross(part_files)
        if still_oversized:
            log.warning(f"split: {len(still_oversized)} part(s) weiterhin > "
                        f"{_nc_videoteil.TELEGRAM_HARD_MB} MB nach Copy-Re-Splits — "
                        f"Re-Encode-Fallback (erzwungene Keyframes)")
            _nc_videoteil.wegwerfen(part_files)

            # BUG-FIX (B70+): Vor dem Re-Encode erst einen sauberen Re-Mux-Schritt
            # durchführen. Streams mit "pts has no value" / "Non-monotonic DTS"
            # (wie bei @xxxderspender88xxx im Log) bringen den Segment-Muxer in
            # _reencode_segment zum Absturz weil ffmpeg mit -f segment keine
            # kaputten Timestamps toleriert. Ein vorheriger Re-Mux mit
            # -fflags +genpts erzeugt saubere Timestamps → Re-Encode klappt dann.
            remux_path = filepath + ".remux.mp4"
            _remux_ok, _rm_err = await _nc_videoteil.zeitstempel_richten(
                filepath, remux_path)
            if _remux_ok:
                log.info("split: Re-Mux (genpts) OK → Re-Encode auf remuxed file")
            else:
                log.warning("split: Re-Mux fehlgeschlagen (%s) — Re-Encode direkt "
                            "auf Original", _rm_err or "?")

            _encode_src = remux_path if _remux_ok else filepath
            re_parts, re_err = await _nc_videoteil.neu_kodieren(
                _encode_src, prefix, _nc_videoteil.ZIEL_TEIL_MB)
            if _remux_ok:
                try: os.remove(remux_path)
                except OSError: pass

            if re_parts:
                part_files = re_parts
                log.info(f"split: Re-Encode-Fallback erzeugte {len(re_parts)} Parts")
            else:
                log.error(f"split: Re-Encode-Fallback fehlgeschlagen: {re_err} — "
                          f"Datei bleibt komplett auf Server")
                # BUG-FIX: part_files ist hier leer (alle Parts wurden oben gelöscht,
                # Globs finden nichts mehr). Vorher lief die for-Schleife mit [] durch
                # und das Video ging lautlos verloren. Jetzt: explizite Notif + return.
                try:
                    await _safe_send(
                        bot_app.bot, chat_id,
                        f"⚠ <b>UPLOAD NICHT MÖGLICH · @{safe(username)}</b>\n"
                        f"<i>Copy-Split und Re-Encode-Fallback beide fehlgeschlagen.\n"
                        f"Datei ({size_mb:.0f} MB) liegt komplett auf dem Server.</i>\n"
                        f"<code>{safe((re_err or '')[:200])}</code>",
                        parse_mode=ParseMode.HTML, disable_notification=True)
                except Exception:
                    pass
                return

        total = len(part_files)
        sent_count = 0
        for i, part in enumerate(part_files, 1):
            part_size_mb = 0
            try:
                part_size_mb = os.path.getsize(part) / 1024 / 1024
                # Letzter Safety-Check vor Upload: wenn Part immer noch > Hard-Limit,
                # gar nicht erst versuchen (würde 413 zurückkommen)
                if part_size_mb > _nc_videoteil.TELEGRAM_HARD_MB:
                    log.error(f"part {i}/{total} bleibt {part_size_mb:.1f} MB > "
                              f"{_nc_videoteil.TELEGRAM_HARD_MB} MB hard limit — skip")
                    try:
                        await _safe_send(
                            bot_app.bot, chat_id,
                            f"⚠ <b>PART {i}/{total} ÜBERSPRUNGEN · @{safe(username)}</b>\n"
                            f"<i>Part wäre {part_size_mb:.0f} MB — überschreitet Telegram-Bot-Limit (50 MB)</i>",
                            parse_mode=ParseMode.HTML, disable_notification=True)
                    except Exception: pass
                    continue

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
                            f"<code>{safe(err)[:200]}</code>",
                            parse_mode=ParseMode.HTML, disable_notification=True)
                    except Exception: pass
            finally:
                try: os.remove(part)
                except OSError: pass

            # F34: 5s Pause zwischen Parts. Schützt vor Telegram-Rate-Limiting
            # (FloodWait) bei großen Aufnahmen mit vielen Parts, und gibt der
            # Verbindung Zeit zum Reset.
            if i < total:
                await asyncio.sleep(5)

        log.info(f"Upload @{username}: {sent_count}/{total} parts erfolgreich")
    except Exception as e:
        # Letzter Auffang — z.B. wenn os.path.getsize crasht
        log.error(f"Video-Splitting/-Upload crash: {e}", exc_info=True)
    finally:
        # BUG-FIX: B47-Repair-Temp aufräumen (vollgroße Dublette der ohnehin
        # retainten Original-Aufnahme). Läuft auf JEDEM Pfad inkl. Early-Returns.
        if _b47_repaired:
            try: os.remove(_b47_repaired)
            except OSError: pass
