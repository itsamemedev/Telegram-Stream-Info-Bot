"""nc.netstat — v4.0-W61b: Netzdurchsatz-Berechnung, aus bot.py gelöst.

Zwei reine Teile: sum_bytes parst den Inhalt von /proc/net/dev zur Summe aller
rx+tx-Bytes (ohne loopback), throughput_kbps macht aus zwei Messungen den
Durchsatz in kbps — mit Guards gegen den Erstaufruf und gegen Counter-Resets
(Reboot/Interface-Neustart). Datei-Lesen und der Sample-State bleiben beim
Aufrufer. sum_bytes wirft bei kaputten Zeilen bewusst (der Aufrufer fängt es zu
0.0 ab, wie im Original). Bitgenau geprüft.
"""


def sum_bytes(proc_net_dev):
    """Summe rx_bytes+tx_bytes über alle Interfaces außer 'lo', aus dem Inhalt
       von /proc/net/dev. Zeilen ohne ':' (Header) werden übersprungen."""
    total = 0
    for line in (proc_net_dev or "").splitlines():
        if ":" not in line:
            continue
        iface, rest = line.split(":", 1)
        iface = iface.strip()
        if not iface or iface == "lo":
            continue
        cols = rest.split()
        if len(cols) >= 9:
            total += int(cols[0]) + int(cols[8])   # rx_bytes + tx_bytes
    return total


def throughput_kbps(prev_ts, prev_bytes, now, total):
    """Durchsatz in kbps aus zwei Messungen. 0.0 beim Erstaufruf (prev_ts falsy),
       bei nicht-fortschreitender Zeit und bei Counter-Reset (total < prev_bytes)."""
    if prev_ts and now > prev_ts and total >= prev_bytes:
        return round((total - prev_bytes) * 8 / 1000.0 / (now - prev_ts), 1)
    return 0.0
