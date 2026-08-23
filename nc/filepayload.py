"""nc.filepayload — v4.0-W28: reine Datei-Klassifikation für den LLM-Upload.

Aus _extract_file_payload herausgelöst: der Telegram-DOWNLOAD (I/O) bleibt im
Bot, die reine Entscheidungs-/Decodier-Logik (Größen-Ablehnung, pdf/image/text/
binary, Encoding-Fallback utf-8→utf-8-sig→latin-1, Text-Cap) wandert hierher.
Bytes rein, dict raus — bitgenau gegen den Monolithen geprüft.
"""

import base64


def size_reject(declared_size, max_bytes):
    """Frühe Ablehnung anhand der vorab gemeldeten Größe (vor dem Download) —
       {kind:'too_big', error:…} oder None. Exakt wie im Bot."""
    if declared_size is None:
        return None
    if declared_size > max_bytes:
        return {"kind": "too_big",
                "error": f"Datei ist {declared_size / 1024 / 1024:.1f} MB, "
                         f"Limit {max_bytes / 1024 / 1024:.0f} MB."}
    return None


def classify_downloaded(raw, name="", mime="", max_chars=50000):
    """Post-Download: aus den Rohbytes + Name + (klein geschriebenem) Mime die
       Felder kind/content_b64/content_text/error ableiten. Rein.

    * PDF (per Mime oder .pdf)      → kind='pdf' + Hinweis (kein Parser).
    * Bild (Mime image/* oder Ext)  → kind='image' + content_b64.
    * Text (utf-8/utf-8-sig/latin-1)→ kind='text' + content_text (bei Überlänge
                                       auf max_chars gekürzt + Marker).
    * sonst                          → kind='binary' + Hinweis.
    """
    ext = name.rsplit(".", 1)[-1].lower() if "." in name else ""
    is_image = mime.startswith("image/") or ext in ("jpg", "jpeg", "png", "gif", "webp")
    is_pdf = mime == "application/pdf" or ext == "pdf"

    if is_pdf:
        return {"kind": "pdf",
                "error": "PDFs werden nicht unterstützt (kein Parser an Bord)."}

    if is_image:
        return {"kind": "image",
                "content_b64": base64.b64encode(raw).decode("ascii")}

    text = None
    for enc in ("utf-8", "utf-8-sig", "latin-1"):
        try:
            text = raw.decode(enc)
            break
        except UnicodeDecodeError:
            continue
    if text is None:
        return {"kind": "binary",
                "error": "Datei sieht binär aus, kein Text-Decode möglich."}

    if len(text) > max_chars:
        text = text[:max_chars] + f"\n\n[… {len(text) - max_chars} Zeichen abgeschnitten]"
    return {"kind": "text", "content_text": text}
