"""nc.aufnahmekategorie — warum eine Aufnahme so geendet hat (v4.2-W23).

EIN Blick auf `stderr`, Returncode, Dateigröße und Dauer entscheidet, in
welche von zehn Kategorien eine beendete Aufnahme fällt — und genau dieser
Blick stand als 87-Zeilen-`if`/`elif`-Kette mitten in `handle_recording_finished`
(658 Zeilen), einer Funktion, die einen laufenden ffmpeg-Prozess braucht. Die
Kette war damit NIE einzeln aufrufbar, obwohl sie die Grundlage jeder
Fehlerstatistik im Dashboard ist.

**Die Reihenfolge ist der eigentliche Vertrag, nicht die einzelnen Muster.**
Mehrere Kategorien konkurrieren um dieselbe stderr-Zeile:

* `hevc_unsupported` steht ZUERST, weil es sonst mal als `stall_killed`, mal
  als frühzeitiger Fehlschlag durchgeht — je nachdem, wie ffmpeg abbricht.
* `stream_dead` (HTTP 404 — die Quell-URL ist abgelaufen) steht VOR
  `codec_header_fail`, weil das nachgelagerte "could not write header" nur
  eine FOLGE des toten Streams ist, kein Codec-Problem. Vertauscht, würde ein
  toter Stream fälschlich als Codec-Fehler gezählt — und der Backoff, der
  genau für tote Streams existiert, griffe nicht.
* `codec_header_fail` sitzt selbst wieder INNERHALB von `stall_killed`: nur
  ein Stall MIT dieser Signatur ist ein Input-Codec-Problem, ein Stall ohne
  sie ist ein generischer Abbruch.

Der Sonderfall `early_disconnect` ist keine Zeile in der Kette, sondern eine
NACHTRÄGLICHE Umwidmung: eine sehr kurze Aufnahme (<30s) mit Fehler, die
sonst als das nichtssagende `fail` verbucht würde, wird darauf umgeschrieben
— sonst sieht der Betreiber nur "fail" und nicht "TikTok hat uns rausgekickt".

Rein rechnend: kein Logging, keine Registerpflege. Beides bleibt in `bot.py`,
weil die Log-Zeilen `username` und `RECORD_PROXY` brauchen und die
Eskalation (403-Streak, Early-Disconnect-Retry) an geteiltem Zustand hängt,
den `nc.aufnahmefolge` (W18) schon rechnet.
"""


def kategorisiere(stderr_text, stall_killed, returncode, file_exists, duration):
    """Die Fehlerkategorie einer beendeten Aufnahme, priorisiert.

    `stderr_text` ist bereits aufbereitet (leer → "empty stderr", sonst
    gekürzt) — das bleibt Sache des Aufrufers, hier zählt nur der Text.
    `"403"` wird bewusst gegen den ROHEN Text geprüft, nicht gegen die
    kleingeschriebene Fassung: ein numerischer Code hat keine Groß-/
    Kleinschreibung, und `stderr_lc` existiert nur fürs Wortmaterial.
    """
    stderr_lc = stderr_text.lower()

    # B64: HEVC-in-FLV (codec-id 12 / bytevc1) — ffmpeg < 7.x kann das im
    # FLV-Container nicht demuxen. Zuerst geprüft: tritt sonst mal als
    # stall_killed, mal als früher Fehlschlag auf.
    hevc_sig = ("is not implemented" in stderr_lc
                or "update your ffmpeg" in stderr_lc
                or "0x000c" in stderr_lc
                or "[12][0][0][0]" in stderr_lc
                or ("unknown codec" in stderr_lc and "video" in stderr_lc))

    if hevc_sig:
        category = "hevc_unsupported"
    elif ("http error 404" in stderr_lc or "404 not found" in stderr_lc
          or "server returned 404" in stderr_lc):
        # B68: tote/abgelaufene Stream-URL. Vor codec_header_fail geprüft —
        # sonst landet ein toter Stream fälschlich als Codec-Fehler.
        category = "stream_dead"
    elif stall_killed:
        # B59: ein Stall MIT dieser Signatur ist ein Input-Codec-Problem,
        # kein generischer Abbruch.
        if ("could not write header" in stderr_lc
                or "incorrect codec parameters" in stderr_lc
                or "error opening output file" in stderr_lc):
            category = "codec_header_fail"
        else:
            category = "stall_killed"
    elif "no playable streams" in stderr_lc or "this user is offline" in stderr_lc:
        category = "offline_or_protected"
    elif "403" in stderr_text or "forbidden" in stderr_lc:
        category = "forbidden_403"
    elif "timeout" in stderr_lc:
        category = "timeout"
    elif "no plugin" in stderr_lc:
        category = "no_plugin"
    elif returncode == 0 and not file_exists:
        category = "empty_output"
    else:
        category = "fail"

    # F45: eine sehr kurze Aufnahme (<30s) mit Fehler ist fast immer ein
    # TikTok-CDN-Disconnect, kein ffmpeg-Konfigfehler. Nur "fail" wird
    # umgewidmet — jede spezifischere Kategorie (403, tot, Codec, …) sagt
    # bereits mehr, als "gekickt" sagen würde, und bleibt stehen.
    if duration < 30 and returncode != 0 and category == "fail" and not stall_killed:
        category = "early_disconnect"

    return category
