/* v4.0-W114 · DER RAUM — die ganze Seite steht in 3D.

   Vorher hatte die Seite drei raeumliche Widgets (Sentinel-Kern,
   Verbrauchsbalken, Spendenmuenze) auf einer flachen Flaeche. Dieses
   Skript macht die SEITE raeumlich: ein perspektivischer Korridor hinter
   dem Inhalt, jede Sektion auf einer eigenen Z-Ebene, jede Kachel als
   Koerper, der sich unter dem Zeiger neigt.

   Wie die uebrigen 3D-Teile dieser Seite: Vanilla-Canvas, kein Fremd-Code,
   kein externer Request. Alles haengt an html.d3 — ohne JS, bei
   prefers-reduced-motion oder nach einem Klick auf "Flach" faellt die
   Klasse weg und die Seite ist exakt die alte.

   Drei Dinge, die hier bewusst so und nicht anders stehen:

   * EINE Schleife fuer alles. Korridor, Sektionstiefe und Kachelneigung
     laufen in demselben requestAnimationFrame. Drei eigene Schleifen
     haetten sich gegenseitig Frames weggenommen und auf dem Handy
     sichtbar geruckelt.
   * getBoundingClientRect() nur bei BEWEGUNG. Der Aufruf erzwingt ein
     Layout; ihn pro Frame fuer jede Sektion zu fahren kostet mehr als das
     Zeichnen. Er laeuft nur, wenn sich Scrollstand oder Fenstermass
     geaendert haben.
   * Flach ist der ehrliche Rueckfallpfad. Kein Canvas, kein 2D-Kontext,
     zu wenig Kerne, schmaler Schirm — jeder dieser Faelle fuehrt zu
     weniger Punkten oder zu gar keinem Raum, nie zu einer ruckelnden
     Seite. */
(function(){
  'use strict';
  var root = document.documentElement;
  var cv   = document.getElementById('raum');
  var btn  = document.getElementById('d3-schalter');
  var mq   = window.matchMedia ? window.matchMedia('(prefers-reduced-motion: reduce)') : null;
  var reduce = !!(mq && mq.matches);
  var ctx  = (cv && cv.getContext) ? cv.getContext('2d') : null;
  var SCHLUESSEL = 'lafap.raum';

  function gelesen(){ try { return localStorage.getItem(SCHLUESSEL); } catch(e){ return null; } }
  function gemerkt(v){ try { localStorage.setItem(SCHLUESSEL, v); } catch(e){} }

  /* Vorgabe: an. Bei prefers-reduced-motion aus — aber umschaltbar: eine
     ausdrueckliche Wahl des Betrachters schlaegt die Systemvorgabe, nie
     umgekehrt. */
  var an = (function(){ var g = gelesen(); return g === null ? !reduce : g === '1'; })();

  function cssv(n, f){
    try { var v = getComputedStyle(root).getPropertyValue(n).trim(); return v || f; }
    catch(e){ return f; }
  }
  var PHOS = cssv('--phos', '#00ff9c'), CYAN = cssv('--cyan', '#00e5ff'),
      MAG  = cssv('--mag',  '#ff2e88');

  /* ── Der Korridor ──────────────────────────────────────────────────
     Kamera im Ursprung, Blick auf +Z. Der Raum ist endlos, die Punkte
     sind es nicht: sie laufen modulo FERN um, dadurch reichen ein paar
     hundert fuer einen Flug ohne Ende. */
  var W = 0, H = 0, dpr = 1, raf = null, t = 0;
  var FERN = 900, BRENN = 520, SCHRITT = 90, HALBB = 560, HALBH = 300;
  var kamZ = 0, gier = 0, nick = 0, zielGier = 0, zielNick = 0;
  var knoten = [];

  function sparsam(){
    /* Weniger Punkte auf schmalen Schirmen und schwachen Geraeten. Der
       Raum bleibt derselbe, nur duenner besetzt — das faellt weit weniger
       auf als ein Ruckeln. */
    var kerne = navigator.hardwareConcurrency || 4;
    return (window.innerWidth < 760 || kerne <= 2);
  }
  function feld(){
    var n = sparsam() ? 110 : 250, i;
    knoten = [];
    for (i = 0; i < n; i++){
      knoten.push({ x:(Math.random()*2-1)*HALBB, y:(Math.random()*2-1)*HALBH,
                    z: Math.random()*FERN,
                    c: (i % 11 === 0) ? MAG : ((i % 3 === 0) ? CYAN : PHOS),
                    r: 0.7 + Math.random()*1.6, ph: Math.random()*6.283 });
    }
  }
  function fit(){
    W = window.innerWidth; H = window.innerHeight;
    dpr = Math.min(2, window.devicePixelRatio || 1);
    if (!cv) return;
    cv.width = Math.max(1, Math.round(W*dpr));
    cv.height = Math.max(1, Math.round(H*dpr));
  }
  function proj(x, y, z){
    var s = Math.sin(gier), c = Math.cos(gier);
    var x1 = x*c - z*s, z1 = x*s + z*c;
    var sn = Math.sin(nick), cn = Math.cos(nick);
    var y1 = y*cn - z1*sn, z2 = y*sn + z1*cn;
    if (z2 < 14) return null;                 // hinter/auf der Bildebene
    var k = BRENN / z2;
    return { x: W/2 + x1*k, y: H*0.46 - y1*k, k: k, z: z2 };
  }
  function linie(a, b, farbe, alpha, breite){
    if (!a || !b) return;
    ctx.globalAlpha = alpha; ctx.strokeStyle = farbe; ctx.lineWidth = breite || 1;
    ctx.beginPath(); ctx.moveTo(a.x, a.y); ctx.lineTo(b.x, b.y); ctx.stroke();
  }
  function korridor(){
    var versatz = kamZ % SCHRITT, ringe = Math.floor(FERN / SCHRITT), i;
    for (i = 1; i <= ringe; i++){
      var z = i*SCHRITT - versatz;
      if (z < 20) continue;
      var a = proj(-HALBB, -HALBH, z), b = proj(HALBB, -HALBH, z),
          c = proj(HALBB, HALBH, z),  d = proj(-HALBB, HALBH, z);
      if (!a || !b || !c || !d) continue;
      /* Die Alpha-Rampe fiel frueher quadratisch mit der Entfernung ab —
         also genau dort am staerksten, wo ein Ring so gross projiziert wird,
         dass er komplett ausserhalb des Bildes liegt. Sichtbar war dadurch
         praktisch nichts. Jetzt blendet der nahe Rand ein (z/260) und erst
         der ferne wieder aus. */
      var f = 1 - z/FERN, al = 0.30*Math.min(1, z/260)*(0.15 + 0.85*f);
      if (al <= 0.004) continue;
      linie(a, b, PHOS, al); linie(b, c, PHOS, al*0.55);
      linie(c, d, PHOS, al*0.8); linie(d, a, PHOS, al*0.55);
    }
    /* Die vier Laengsschienen geben dem Raum seine Fluchtlinie — ohne sie
       liest sich das Ganze als flackernde Rechteckstapel statt als Gang. */
    var nah = 40, weit = FERN*0.95, e, g;
    var kanten = [[-HALBB,-HALBH],[HALBB,-HALBH],[HALBB,HALBH],[-HALBB,HALBH]];
    for (e = 0; e < 4; e++){
      linie(proj(kanten[e][0], kanten[e][1], nah),
            proj(kanten[e][0], kanten[e][1], weit), CYAN, 0.16);
    }
    /* Boden und Decke bekommen eigene Laengslinien. Ohne sie liest sich der
       Gang als Stapel schwebender Rahmen; mit ihnen als Raum, durch den man
       faehrt — und das ist der ganze Zweck. */
    for (g = -2; g <= 2; g++){
      var x = g*(HALBB/2.2);
      linie(proj(x, -HALBH, nah), proj(x, -HALBH, weit), PHOS, 0.085);
      linie(proj(x,  HALBH, nah), proj(x,  HALBH, weit), PHOS, 0.05);
    }
  }
  function punkte(){
    var i;
    for (i = 0; i < knoten.length; i++){
      var p = knoten[i];
      var z = (p.z - kamZ) % FERN; if (z < 0) z += FERN;
      var q = proj(p.x, p.y, z + 24); if (!q) continue;
      var f = 1 - z/FERN;
      var a = 0.85*f*f*(0.55 + 0.45*Math.sin(t*0.02 + p.ph));
      if (a <= 0.01) continue;
      ctx.globalAlpha = a; ctx.fillStyle = p.c;
      ctx.beginPath();
      ctx.arc(q.x, q.y, Math.max(0.4, Math.min(5, p.r*q.k)), 0, 6.2832);
      ctx.fill();
    }
  }
  function zeichnen(){
    if (!ctx) return;
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    ctx.clearRect(0, 0, W, H);
    korridor();
    punkte();
    ctx.globalAlpha = 1;
  }

  /* ── Tiefe der Sektionen ───────────────────────────────────────────
     REGEL: flach beim Lesen. Der Beitrag ist kubisch in der Abweichung
     von der Bildschirmmitte — nahe der Mitte praktisch null, erst an den
     Raendern voll. Dadurch steht jeder Textblock, den man gerade liest,
     pixelgenau plan; gekippter Fliesstext wird unscharf gerastert. */
  var sektionen = [].slice.call(document.querySelectorAll('main > section'));
  function tiefe(){
    var vh = window.innerHeight || 1, i;
    for (i = 0; i < sektionen.length; i++){
      var el = sektionen[i], r = el.getBoundingClientRect();
      /* Massstab ist NICHT die Sektionsmitte, sondern die naechste Kante zur
         Bildschirmmitte. Bei der Mitte kippt eine hohe Sektion noch spuerbar,
         waehrend man bereits mitten in ihrem Text liest — ihr Zentrum liegt
         dann laengst ausserhalb des Bildes. Deckt sie die Lesezone ab, ist
         die Tiefe exakt null; erst was ganz darueber oder darunter liegt,
         kippt weg. */
      var mY = vh*0.5, d;
      if (r.top <= mY && r.bottom >= mY) d = 0;
      else if (r.top > mY) d = Math.min(1, (r.top - mY)/(vh*0.6));
      else d = -Math.min(1, (mY - r.bottom)/(vh*0.6));
      var w = d*Math.abs(d);
      /* perspective() steht IM transform, nicht als CSS-Eigenschaft auf
         dem main-Element. Warum: main ist ueber zehntausend Pixel hoch,
         und eine perspective auf einem so hohen Element legt den Fluchtpunkt
         einmalig in dessen Mitte — alles weit darueber oder darunter
         kippt dann grotesk weg. Im transform-Funktionsaufruf gilt der
         Fluchtpunkt dagegen je Sektion und sitzt in ihrer eigenen Mitte. */
      el.style.transform = 'perspective(1600px) translate3d(0,0,' +
                           (-Math.abs(w)*230).toFixed(1) + 'px) rotateX(' +
                           (-w*7).toFixed(2) + 'deg)';
    }
  }
  function flachlegen(){
    var i;
    for (i = 0; i < sektionen.length; i++) sektionen[i].style.transform = '';
  }

  /* ── Neigung der Kacheln ───────────────────────────────────────────
     Delegiert statt vorab eingesammelt: die Nachrichten-Kacheln entstehen
     erst, wenn news.json geladen ist. Eine feste Liste haette sie nie
     erfasst. */
  var KACHEL = '.streams .btn,.res-card,.principle,.news-item,.metric,' +
               '.agent,.log,.chart-card,.stats';
  var letzte = null;
  function loslassen(){
    if (!letzte) return;
    letzte.style.transform = '';
    letzte.classList.remove('d3-hover');
    letzte = null;
  }
  function neigen(e){
    if (!an) return;
    var el = (e.target && e.target.closest) ? e.target.closest(KACHEL) : null;
    if (el !== letzte) loslassen();
    if (!el) return;
    letzte = el; el.classList.add('d3-hover');
    var r = el.getBoundingClientRect();
    if (!r.width || !r.height) return;
    var nx = (e.clientX - r.left)/r.width - 0.5;
    var ny = (e.clientY - r.top)/r.height - 0.5;
    el.style.transform = 'translateZ(26px) rotateY(' + (nx*9).toFixed(2) +
                         'deg) rotateX(' + (-ny*9).toFixed(2) + 'deg)';
  }

  /* ── Die eine Schleife ─────────────────────────────────────────────── */
  var letzterScroll = -1, letzteHoehe = -1, treibt = 0;
  function schleife(){
    raf = null;
    if (!an || document.hidden) return;
    var y = window.pageYOffset || root.scrollTop || 0;
    if (y !== letzterScroll || window.innerHeight !== letzteHoehe){
      letzterScroll = y; letzteHoehe = window.innerHeight;
      tiefe();
    }
    treibt += 0.35;                       // Eigenfahrt, damit der Raum lebt
    kamZ = treibt + y*0.55;
    gier += (zielGier - gier)*0.06;
    nick += (zielNick - nick)*0.06;
    t++;
    zeichnen();
    raf = window.requestAnimationFrame(schleife);
  }
  function anstossen(){
    if (!an || document.hidden) return;
    if (raf === null) raf = window.requestAnimationFrame(schleife);
  }

  /* ── Ein und aus ───────────────────────────────────────────────────── */
  function beschriften(){
    if (!btn) return;
    btn.hidden = false;
    btn.textContent = an ? 'Flach' : '3D';
    btn.setAttribute('title', an ? 'Raeumliche Darstellung abschalten'
                                 : 'Seite raeumlich darstellen');
  }
  function anwenden(){
    root.classList.toggle('d3', an);
    beschriften();
    if (an){
      fit(); feld(); letzterScroll = -1; tiefe(); anstossen();
    } else {
      if (raf !== null){ window.cancelAnimationFrame(raf); raf = null; }
      if (ctx){ ctx.setTransform(1,0,0,1,0,0); ctx.clearRect(0,0,cv.width,cv.height); }
      flachlegen(); loslassen();
    }
  }

  if (!ctx){
    /* Kein Canvas-Kontext: dann gibt es keinen Korridor, aber die
       CSS-Tiefe der Sektionen kostet nichts und bleibt. */
    root.classList.toggle('d3', an);
    beschriften();
    if (an){ letzterScroll = -1; tiefe(); }
  } else {
    anwenden();
  }

  if (btn){
    btn.addEventListener('click', function(){
      an = !an; gemerkt(an ? '1' : '0'); anwenden();
    });
  }
  window.addEventListener('resize', function(){
    if (!an) return;
    fit(); feld(); letzterScroll = -1;
    if (ctx) anstossen(); else tiefe();
  }, {passive:true});
  window.addEventListener('scroll', function(){
    if (an && !ctx) tiefe();              // ohne Canvas laeuft keine Schleife
    else anstossen();
  }, {passive:true});
  document.addEventListener('visibilitychange', function(){
    if (!document.hidden) anstossen();
  });
  /* Zeigerparallaxe nur, wo es einen echten Zeiger gibt. Auf dem Handy
     wuerde jeder Tipper den Raum verreissen. */
  if (window.matchMedia && window.matchMedia('(hover: hover) and (pointer: fine)').matches){
    window.addEventListener('pointermove', function(e){
      zielGier = ((e.clientX/(window.innerWidth||1)) - 0.5)*0.16;
      zielNick = ((e.clientY/(window.innerHeight||1)) - 0.5)*0.10;
      anstossen();
    }, {passive:true});
    document.addEventListener('pointermove', neigen, {passive:true});
    document.addEventListener('pointerleave', loslassen);
  }
  /* Aendert der Betrachter seine Systemvorgabe waehrend des Besuchs und
     hat hier noch nichts von Hand gewaehlt, folgt die Seite ihr. */
  if (mq && mq.addEventListener){
    mq.addEventListener('change', function(ev){
      if (gelesen() !== null) return;
      an = !ev.matches; anwenden();
    });
  }
})();
