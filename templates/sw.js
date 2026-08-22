/* NIGHTCRAWLER PWA Service Worker
 *
 * WICHTIG — Design-Entscheidung:
 * Dies ist ein LIVE-Kontrollpanel. API-Antworten (/api/...) dürfen NIEMALS
 * gecacht werden, sonst zeigt die App veralteten Bot-Status (z.B. "live"
 * obwohl offline). Nur die statische Shell (HTML/Icons) wird gecacht, damit
 * die App sofort startet und bei Verbindungsverlust eine saubere Meldung zeigt
 * statt des Browser-Dinos.
 *
 * Strategie:
 *   /api/*        → immer Netzwerk, nie Cache (network-only)
 *   Shell (/, /brain, Icons) → network-first mit Cache-Fallback
 */
const CACHE = "nightcrawler-shell-v3";
// v4.0-W53: /brain aus der Shell entfernt — es ist KEINE Route (404), sondern ein
// client-seitiger Tab (/#brain). Die Shell ist '/' (SPA mit allen Views) + Login + Icons.
const SHELL = ["/", "/login", "/pwa-icon-192.png", "/pwa-icon-512.png", "/pwa-icon-maskable-512.png"];

self.addEventListener("install", (e) => {
  // Shell vorab laden, aber Fehler einzelner Dateien nicht den ganzen
  // Install abbrechen lassen (z.B. wenn /brain gerade Auth verlangt).
  e.waitUntil(
    caches.open(CACHE).then((c) =>
      Promise.allSettled(SHELL.map((u) => c.add(u)))
    ).then(() => self.skipWaiting())
  );
});

self.addEventListener("activate", (e) => {
  // Alte Cache-Versionen aufräumen.
  e.waitUntil(
    caches.keys().then((keys) =>
      Promise.all(keys.filter((k) => k !== CACHE).map((k) => caches.delete(k)))
    ).then(() => self.clients.claim())
  );
});

self.addEventListener("fetch", (e) => {
  const url = new URL(e.request.url);

  // 1. API + alles Nicht-GET: NIE cachen. Immer live ans Netzwerk.
  if (url.pathname.startsWith("/api/") || e.request.method !== "GET") {
    return; // Standard-Browserverhalten (Netzwerk)
  }

  // 2. Shell: network-first (frisch bevorzugt), Cache nur als Offline-Fallback.
  e.respondWith(
    fetch(e.request)
      .then((resp) => {
        // Erfolgreiche Shell-Antwort in den Cache spiegeln (für offline).
        if (resp && resp.status === 200 && resp.type === "basic") {
          const copy = resp.clone();
          caches.open(CACHE).then((c) => c.put(e.request, copy));
        }
        return resp;
      })
      .catch(() =>
        // Offline → aus Cache liefern, sonst eine schlichte Offline-Seite.
        caches.match(e.request).then((cached) =>
          cached || new Response(
            "<!doctype html><meta charset=utf-8>" +
            "<meta name=viewport content='width=device-width,initial-scale=1'>" +
            "<body style='background:#020306;color:#39d98a;font-family:monospace;" +
            "display:flex;align-items:center;justify-content:center;height:100vh;" +
            "margin:0;text-align:center;padding:20px'>" +
            "<div><h2>▚ OFFLINE</h2><p>Keine Verbindung zum Bot.</p>" +
            "<p style='color:#5c6f68;font-size:13px'>Die App braucht Netzwerk-" +
            "zugriff auf den Server. Sobald er erreichbar ist, einfach neu laden.</p>" +
            "</div></body>",
            { headers: { "Content-Type": "text/html; charset=utf-8" } }
          )
        )
      )
  );
});
