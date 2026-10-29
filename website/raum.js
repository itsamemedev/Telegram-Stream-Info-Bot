/* raum.js — v4.2-W113: ein leises Feld hinter der Seite, sonst nichts.

   Bis W112 stand hier der „Raum": Korridor, Sektionstiefe, Kachelneigung,
   ein Schalter „Flach". Er hat die Seite beim Scrollen kippen lassen — und
   gekippter Fliesstext wird vom Browser unscharf gerastert. Fuer eine Seite,
   die gelesen werden soll, ist das der falsche Effekt.

   Geblieben ist eine Andeutung: wenige Punkte, die sehr langsam treiben, und
   feine Linien zwischen nahen Nachbarn — das Netz, das der Name meint. Es
   liegt hinter dem Inhalt, faengt keine Klicks ab und kostet wenig:

   * prefers-reduced-motion: EIN Standbild, keine Schleife.
   * Versteckter Tab: die Schleife haelt an.
   * Wenige Kerne oder schmaler Schirm: weniger Punkte.
   * Kein Canvas, kein 2D-Kontext: es passiert nichts, und die Seite ist
     dieselbe — das Feld ist Zierde, keine Voraussetzung.
   Kein Fremd-Code, keine Anfrage nach aussen. */
(function(){
  'use strict';
  var cv = document.getElementById('raum');
  var ctx = (cv && cv.getContext) ? cv.getContext('2d') : null;
  if (!ctx) return;
  var mq = window.matchMedia ? window.matchMedia('(prefers-reduced-motion: reduce)') : null;
  var reduce = !!(mq && mq.matches);
  var W = 0, H = 0, dpr = 1, punkte = [], raf = null, zuletzt = 0;

  function anzahl(){
    var n = Math.round(W * H / 26000);
    if ((navigator.hardwareConcurrency || 4) <= 4) n = Math.round(n * 0.6);
    return Math.max(18, Math.min(70, n));
  }
  function saeen(){
    punkte = [];
    for (var i = 0, n = anzahl(); i < n; i++) {
      punkte.push({x: Math.random() * W, y: Math.random() * H,
                   vx: (Math.random() - 0.5) * 6, vy: (Math.random() - 0.5) * 6,
                   c: i % 7 === 0 ? 1 : 0});
    }
  }
  function fit(){
    dpr = Math.min(1.5, window.devicePixelRatio || 1);
    W = window.innerWidth; H = window.innerHeight;
    cv.width = Math.round(W * dpr); cv.height = Math.round(H * dpr);
    saeen();
  }
  function bild(){
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    ctx.clearRect(0, 0, W, H);
    var max = 130, i, j, a, b, dx, dy, d;
    ctx.lineWidth = 1;
    for (i = 0; i < punkte.length; i++) {
      a = punkte[i];
      for (j = i + 1; j < punkte.length; j++) {
        b = punkte[j]; dx = a.x - b.x; dy = a.y - b.y;
        if (dx > max || dx < -max || dy > max || dy < -max) continue;
        d = Math.sqrt(dx * dx + dy * dy);
        if (d < max) {
          ctx.strokeStyle = 'rgba(34,211,238,' + (0.07 * (1 - d / max)).toFixed(3) + ')';
          ctx.beginPath(); ctx.moveTo(a.x, a.y); ctx.lineTo(b.x, b.y); ctx.stroke();
        }
      }
    }
    for (i = 0; i < punkte.length; i++) {
      a = punkte[i];
      ctx.fillStyle = a.c ? 'rgba(0,255,156,.45)' : 'rgba(183,198,193,.22)';
      ctx.beginPath(); ctx.arc(a.x, a.y, a.c ? 1.6 : 1.1, 0, 6.2832); ctx.fill();
    }
  }
  function schritt(dt){
    for (var i = 0; i < punkte.length; i++) {
      var p = punkte[i];
      p.x += p.vx * dt; p.y += p.vy * dt;
      if (p.x < -10) p.x = W + 10; else if (p.x > W + 10) p.x = -10;
      if (p.y < -10) p.y = H + 10; else if (p.y > H + 10) p.y = -10;
    }
  }
  function takt(t){
    if (document.hidden || reduce) { raf = null; return; }
    var dt = zuletzt ? Math.min(0.05, (t - zuletzt) / 1000) : 0.016;
    zuletzt = t;
    schritt(dt); bild();
    raf = requestAnimationFrame(takt);
  }
  function los(){
    if (reduce) { bild(); return; }
    if (!raf) { zuletzt = 0; raf = requestAnimationFrame(takt); }
  }
  fit(); los();
  var warte = null;
  window.addEventListener('resize', function(){
    clearTimeout(warte); warte = setTimeout(function(){ fit(); los(); if (reduce) bild(); }, 150);
  });
  document.addEventListener('visibilitychange', function(){ if (!document.hidden) los(); });
  if (mq && mq.addEventListener) mq.addEventListener('change', function(e){ reduce = e.matches; los(); });
})();
