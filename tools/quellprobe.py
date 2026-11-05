#!/usr/bin/env python3
"""tools/quellprobe.py — Aufruf von der Kommandozeile (v4.2-W141).

Der Kern liegt seit v4.2-W142 in nc/quellprobe.py, damit der Bot ihn auch
per Telegram/Discord (`/quelle name`) fahren kann. Auf dem Server:

    venv/bin/python tools/quellprobe.py nutzername
    venv/bin/python tools/quellprobe.py nutzername --ohne-proxy
    venv/bin/python tools/quellprobe.py nutzername --json
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from nc.quellprobe import main  # noqa: E402

if __name__ == "__main__":
    sys.exit(main())
