"""nc.logfilters — Logging-Filter/-Handler ohne Bot-Abhängigkeiten.

_WerkzeugScannerFilter: dämpft Portscanner-Noise im Flask-Access-Log.
_DiscordErrorHandler: throttled Fehler-Spiegelung (Callback-injiziert)."""

import logging
import time as _time_mod

_DC_ERR_QUEUE = None     # vom Bot via configure_logfilters gesetzt (deque)


def configure_logfilters(dc_err_queue=None):
    global _DC_ERR_QUEUE
    if dc_err_queue is not None:
        _DC_ERR_QUEUE = dc_err_queue


class _WerkzeugScannerFilter(logging.Filter):
    """Klassifiziert Port-Scanner-Hits als WARNING statt ERROR. Echte 400er
       von legitimem Traffic (z.B. malformed JSON von eigenem Frontend) bleiben
       ERROR. Heuristik: 400-Antworten auf TLS-/Binary-/Protokoll-Probe-Bytes
       sind keine echten Probleme."""
    # Patterns die typisch für Port-Scanner sind (in lowercase verglichen)
    _SCANNER_HINTS = (
        "bad request version",        # TLS ClientHello bytes
        "bad http/0.9 request type",  # malformed HTTP-Versions
        "bad request syntax",         # binary payloads
        "jdwp-handshake",             # Java Debug Wire Protocol scanner
        "jrmi",                       # Java RMI scanner
        "rtsp/1.0", "sip/2.0",        # streaming protocols
        "giop", "amqp", "mssqlserver",
        "tnmp", "dmdt",
    )
    # B120: Abgebrochene Verbindungen sind KEIN Serverfehler.
    # Das Dashboard haelt SSE-/Streaming-Antworten offen. Schliesst der
    # Browser den Tab, wechselt das Handy von WLAN auf Mobilfunk oder
    # laeuft ein Fetch in seinen Timeout, bricht werkzeug mitten im
    # chunked write ab und loggt einen zweistufigen ERROR-Traceback
    # (BrokenPipeError -> SSLError UNEXPECTED_EOF_WHILE_READING).
    # Im Produktionslog waren das 11 Tracebacks a ~35 Zeilen fuer reine
    # Client-Abbrueche — Rauschen, das echte Fehler zudeckt.
    _CLIENT_ABORT_HINTS = (
        "brokenpipeerror",
        "connectionreseterror",
        "unexpected_eof_while_reading",
        "connectionabortederror",
        "[errno 32] broken pipe",
        "[errno 104] connection reset",
        "ssl: application_data_after_close_notify",
    )

    def filter(self, record):
        if record.levelno != logging.ERROR:
            return True
        msg = record.getMessage().lower()
        # Traceback-Text mitpruefen: bei "Error on request:" steht der
        # eigentliche Fehler im exc_info, nicht in der Message.
        if record.exc_info:
            try:
                import traceback as _tb
                msg += " " + "".join(
                    _tb.format_exception(*record.exc_info)).lower()
            except Exception:
                pass
        if any(hint in msg for hint in self._CLIENT_ABORT_HINTS):
            record.levelno = logging.DEBUG
            record.levelname = "DEBUG"
            record.exc_info = None          # Traceback komplett unterdruecken
            return True
        if any(hint in msg for hint in self._SCANNER_HINTS):
            # Demote to DEBUG — bleibt im Log wenn man's wirklich braucht,
            # aber spammt nicht mehr das ERROR-Level.
            record.levelno = logging.DEBUG
            record.levelname = "DEBUG"
        return True


class _DiscordErrorHandler(logging.Handler):
    def emit(self, record):
        try:
            if record.levelno < logging.ERROR:
                return
            if record.name.startswith(("discord", "websockets")):
                return          # keine Rekursion über Fehler des Discord-Stacks selbst
            _msg = self.format(record)[:900]
            _DC_ERR_QUEUE.append({"ts": _time_mod.time(), "msg": _msg})
            _bp = globals().get("_browser_push")
            if _bp:
                _bp("log.error", "error", record.getMessage()[:120], "")   # F98
        except Exception:
            pass
