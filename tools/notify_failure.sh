#!/usr/bin/env bash
#
# Totmann-Meldung: systemd ruft das auf, wenn der Dienst scheitert.
#
# WARUM ES DAS GIBT
# Der eingebaute Watchdog erkennt Stillstand — aber nur, solange der Prozess
# lebt. Stirbt bot_v37 ganz (OOM-Killer, Absturz beim Start, kaputter Build),
# meldet sich NIEMAND. Bei einem unbeaufsichtigten Dienst ist genau das die
# Ausfallart, die einen kalt erwischt: der Bot ist weg, und man merkt es
# Stunden spaeter am fehlenden Stream.
#
# EINRICHTEN (einmalig, auf dem Server)
#   1) Skript ablegen und ausfuehrbar machen:
#        chmod +x ~/tiktok-bot/tools/notify_failure.sh
#   2) In der Unit verdrahten:
#        sudo systemctl edit tiktok-bot
#      und dort eintragen:
#        [Unit]
#        OnFailure=nightcrawler-notify@%n.service
#   3) Die Melder-Unit anlegen:
#        sudo tee /etc/systemd/system/nightcrawler-notify@.service <<'EOF'
#        [Unit]
#        Description=NIGHTCRAWLER Totmann-Meldung fuer %i
#        [Service]
#        Type=oneshot
#        User=ubuntu
#        EnvironmentFile=/home/ubuntu/tiktok-bot/.env
#        ExecStart=/home/ubuntu/tiktok-bot/tools/notify_failure.sh %i
#        EOF
#        sudo systemctl daemon-reload
#   4) Testen — MUSS eine Nachricht ausloesen:
#        systemctl start nightcrawler-notify@tiktok-bot.service
#
# Nutzt TELEGRAM_TOKEN/TELEGRAM_CHAT_ID bzw. DISCORD_WEBHOOK aus der .env.
# Faellt ein Kanal aus, wird der andere trotzdem versucht.

set -uo pipefail   # bewusst KEIN -e: eine gescheiterte Meldung darf die
                   # zweite nicht verhindern.

EINHEIT="${1:-tiktok-bot.service}"
WANN="$(date '+%F %H:%M:%S %Z')"
RECHNER="$(hostname)"

# Die letzten Zeilen sind das Wertvollste an der Meldung — ohne sie weiss man
# nur DASS etwas kaputt ist, nicht WAS.
LOG="$(journalctl -u "$EINHEIT" -n 25 --no-pager 2>/dev/null | tail -c 1200)"
STATUS="$(systemctl show -p Result --value "$EINHEIT" 2>/dev/null || echo '?')"

TEXT="🔴 NIGHTCRAWLER AUSGEFALLEN
Dienst:  ${EINHEIT}
Rechner: ${RECHNER}
Zeit:    ${WANN}
Grund:   ${STATUS}

Letzte Logzeilen:
${LOG}

Neustart:  sudo systemctl start ${EINHEIT}
Ansehen:   journalctl -u ${EINHEIT} -n 100 --no-pager"

gesendet=0

# ── Telegram ─────────────────────────────────────────────────────────────
if [ -n "${TELEGRAM_TOKEN:-}" ] && [ -n "${TELEGRAM_CHAT_ID:-}" ]; then
  if curl -fsS -m 15 -o /dev/null \
      --data-urlencode "chat_id=${TELEGRAM_CHAT_ID}" \
      --data-urlencode "text=${TEXT}" \
      "https://api.telegram.org/bot${TELEGRAM_TOKEN}/sendMessage"; then
    echo "Telegram-Meldung gesendet."
    gesendet=1
  else
    echo "Telegram-Meldung fehlgeschlagen." >&2
  fi
fi

# ── Discord ──────────────────────────────────────────────────────────────
if [ -n "${DISCORD_WEBHOOK:-}" ]; then
  # Discord deckelt bei 2000 Zeichen; wir kuerzen defensiv auf 1900.
  KURZ="$(printf '%s' "$TEXT" | head -c 1900)"
  if printf '%s' "$KURZ" | python3 -c '
import json,sys
print(json.dumps({"content": "```\n" + sys.stdin.read() + "\n```"}))' \
      | curl -fsS -m 15 -o /dev/null -H "Content-Type: application/json" \
             -d @- "$DISCORD_WEBHOOK"; then
    echo "Discord-Meldung gesendet."
    gesendet=1
  else
    echo "Discord-Meldung fehlgeschlagen." >&2
  fi
fi

if [ "$gesendet" = "0" ]; then
  echo "KEIN Meldeweg konfiguriert oder alle fehlgeschlagen — " \
       "TELEGRAM_TOKEN/TELEGRAM_CHAT_ID oder DISCORD_WEBHOOK in der .env pruefen." >&2
  exit 1
fi
