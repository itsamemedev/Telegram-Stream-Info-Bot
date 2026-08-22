"""nc.restrend — v4.0-W40: reine Trend-Erkennung für Langzeit-Ressourcen.

Die W38-Schwellenwarnung schlägt erst an, wenn fds/RSS einen ABSOLUTEN Wert
reißen. Ein LANGSAMES Leck (z. B. +2 fds/Stunde) bleibt monatelang darunter,
wächst aber trotzdem unaufhaltsam. Diese Funktion erkennt den Trend: steigt der
Median der jüngeren Hälfte deutlich und anhaltend über den der älteren, ist das
ein schleichendes Leck — sichtbar lange bevor es kracht.

Rein: Liste von Zahlen rein, Urteil raus. Bitgenau testbar, keine Kopplung.
"""


def _median(xs):
    s = sorted(xs)
    n = len(s)
    if n == 0:
        return 0.0
    mid = n // 2
    return float(s[mid]) if n % 2 else (s[mid - 1] + s[mid]) / 2.0


def rising_trend(samples, min_points=12, min_rel_growth=0.25, min_abs_growth=0.0):
    """Erkennt einen anhaltenden Aufwärtstrend in einer Zahlenreihe (ältester
       zuerst). Vergleicht den Median der ersten Hälfte mit dem der zweiten.

       Rückgabe: dict {trend, first, last, rel_growth, points}.
       trend=True nur wenn genug Punkte da sind UND das Wachstum sowohl relativ
       (min_rel_growth, z. B. +25 %) als auch absolut (min_abs_growth) über der
       Schwelle liegt — so schlägt es nicht bei harmlosem Rauschen an, aber bei
       einem echten schleichenden Anstieg.
    """
    pts = [x for x in samples if x is not None]
    n = len(pts)
    if n < min_points:
        return {"trend": False, "reason": "zu wenige Datenpunkte",
                "points": n, "first": None, "last": None, "rel_growth": 0.0}
    half = n // 2
    old = _median(pts[:half])
    new = _median(pts[half:])
    abs_growth = new - old
    rel_growth = (abs_growth / old) if old > 0 else (1.0 if abs_growth > 0 else 0.0)
    trend = (abs_growth >= min_abs_growth and rel_growth >= min_rel_growth
             and new > old)
    return {"trend": bool(trend), "points": n,
            "first_median": round(old, 1), "second_median": round(new, 1),
            "rel_growth": round(rel_growth, 3), "abs_growth": round(abs_growth, 1)}
