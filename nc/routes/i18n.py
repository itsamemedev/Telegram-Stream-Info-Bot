"""nc.routes.i18n — Sprachkatalog und Sprachwahl als Flask-Blueprint.

v4.1-W6. Ohne nc.ctx: der Katalog liegt in nc/i18n.py, die Sprachwahl steckt in
Request und Cookie — der Monolith muss dafuer nichts stellen.

Die Oberflaeche uebersetzt im Browser, nicht auf dem Server. Warum: das
Dashboard ist eine JS-Oberflaeche, die den grossen Teil ihrer Texte selbst
erzeugt (Tabellenzeilen, Meldungen, Panels). Serverseitiges Rendern haette nur
das feste Geruest getroffen und den Rest auf Deutsch stehen lassen — sichtbar
zweisprachig, also schlimmer als gar nicht.
"""

from flask import Blueprint, Response, jsonify, make_response, request

from nc import i18n as _nc_i18n

bp = Blueprint("i18n", __name__)

def _t(s):
    """v4.1-W20: an der Quelle uebersetzen. Diese Texte erreichen das DOM
       meist verkettet ("Fehler: " + error) — ein Katalogeintrag fuer den
       blossen Text traefe dort nie."""
    return _nc_i18n.t(s)


# Ein Jahr. Die Sprachwahl ist eine Vorliebe, keine Sitzung — sie soll einen
# Neustart des Browsers ueberleben.
_COOKIE = "nc_lang"
_COOKIE_MAX_AGE = 365 * 24 * 3600


def aktive_sprache():
    """Die Sprache dieses Requests.

    Reihenfolge, absichtlich in dieser: ausdrueckliche Wahl (?lang=) schlaegt
    gespeicherte Wahl (Cookie) schlaegt Browser-Wunsch (Accept-Language)
    schlaegt Standard. Eine gesetzte Wahl darf der Browser nie ueberstimmen —
    sonst springt die Oberflaeche beim naechsten Geraet wieder zurueck.
    """
    aus_query = _nc_i18n.normalisieren(request.args.get("lang"))
    if aus_query:
        return aus_query
    aus_cookie = _nc_i18n.normalisieren(request.cookies.get(_COOKIE))
    if aus_cookie:
        return aus_cookie
    aus_browser = _nc_i18n.aus_accept_language(request.headers.get("Accept-Language"))
    if aus_browser:
        return aus_browser
    return _nc_i18n.standard()


@bp.route("/api/i18n/sprachen")
def api_i18n_sprachen():
    """Welche Sprachen es gibt und welche gerade gilt — fuer den Umschalter."""
    return jsonify(ok=True,
                   aktiv=aktive_sprache(),
                   standard=_nc_i18n.standard(),
                   quelle=_nc_i18n.QUELLSPRACHE,
                   sprachen=[{"code": c, "name": _nc_i18n.SPRACHNAMEN.get(c, c)}
                             for c in _nc_i18n.SPRACHEN])


@bp.route("/api/i18n/katalog")
def api_i18n_katalog():
    """Der Katalog der aktiven (oder per ?lang= gewuenschten) Sprache.

    Fuer Deutsch ist er leer — die Quellsprache braucht keine Uebersetzung, und
    ein leerer Katalog laesst den Uebersetzer im Browser sofort aufhoeren.
    """
    sprache = aktive_sprache()
    return jsonify(ok=True, sprache=sprache,
                   quelle=_nc_i18n.QUELLSPRACHE,
                   strings=_nc_i18n.katalog(sprache))


@bp.route("/api/i18n/waehlen", methods=["POST"])
def api_i18n_waehlen():
    """Sprache setzen und im Cookie merken.

    Bewusst ein POST mit Cookie und nicht nur localStorage: die Wahl muss auch
    dort gelten, wo der Server die Seite ausliefert — sonst blitzt beim Laden
    erst Deutsch auf und springt dann um.
    """
    daten = request.get_json(silent=True) or {}
    gewuenscht = _nc_i18n.normalisieren(daten.get("sprache") or request.args.get("lang"))
    if not gewuenscht:
        return jsonify(ok=False, error=_t("unbekannte Sprache"),
                       sprachen=list(_nc_i18n.SPRACHEN)), 400
    antwort = make_response(jsonify(ok=True, sprache=gewuenscht))
    antwort.set_cookie(_COOKIE, gewuenscht, max_age=_COOKIE_MAX_AGE,
                       samesite="Lax", httponly=False)
    return antwort


# Der Uebersetzer fuer den Browser. Als ausgelieferte Datei und nicht dreimal
# inline in dashboard/brain/overlay: drei Kopien waeren drei Stellen, die
# auseinanderlaufen. Er steht hier als Zeichenkette statt in static/, weil das
# Projekt kein static/ hat und ein neuer Ordner im Auslieferungs-ZIP eine
# eigene Fehlerquelle waere.
_UEBERSETZER_JS = r"""(function(){
  'use strict';
  var KAT = null;            // deutsch -> zielsprache
  var SPRACHE = 'de';
  var ATTRS = ['placeholder','title','aria-label','alt'];

  // Elemente, deren Inhalt Daten ist und nie uebersetzt werden darf. <code>
  // und <pre> zeigen Befehle und Logzeilen — ein Treffer waere dort ein Fehler.
  var TABU = {SCRIPT:1, STYLE:1, CODE:1, PRE:1, TEXTAREA:1, KBD:1, SAMP:1};

  function uebersetze(text){
    if (!KAT || !text) return null;
    var teile = text.match(/^(\s*)([\s\S]*?)(\s*)$/);
    var vorn = teile[1], kern = teile[2], hinten = teile[3];
    if (!kern) return null;
    var treffer = KAT[kern];
    if (!treffer){
      // v4.1-W28: Mehrzeilige Knoten. Der Quelltext bricht Hilfetexte um und
      // rueckt sie ein — im DOM steht der Umbruch mit drin. Der Katalog haelt
      // sie mit einfachen Leerzeichen, sonst waere der Schluessel von der
      // Einrueckung im HTML abhaengig und jede Umformatierung wuerde ihn
      // stillschweigend toeten. Der Extraktor normalisiert genauso.
      treffer = KAT[kern.replace(/\s+/g, ' ')];
      if (!treffer) return null;
    }
    // Rand-Leerzeichen erhalten: viele Knoten sind " Text " mit Einrueckung,
    // und ein Trim wuerde das Layout veraendern.
    return vorn + treffer + hinten;
  }

  // ──────────────────────────────────────────────────────────────────
  // v4.2-W6: Saetze, die ein Inline-Tag zerschneidet.
  // ──────────────────────────────────────────────────────────────────
  // "Gebucht wird der <b>Zufluss</b> — der Tag der Gutschrift ..." ist im DOM
  // kein Textknoten, sondern drei — und keiner davon ist ein Satz. Der
  // Katalog haelt deshalb den GANZEN Satz mit {0}, {1}, … an den Stellen der
  // Inline-Kinder. Hier wird er wieder auseinandergenommen und um die
  // VORHANDENEN Kind-Elemente herum eingesetzt.
  //
  // Warum die vorhandenen Elemente und keine neuen: so kommt kein Markup aus
  // dem Katalog ins DOM. Eine Uebersetzung kann Text liefern, niemals ein
  // Tag, ein Attribut oder ein Ereignis — es gibt in diesem Weg keine Stelle,
  // an der HTML geparst wird.
  var INLINE = {B:1, STRONG:1, I:1, EM:1, U:1, CODE:1, KBD:1, SAMP:1, SPAN:1,
                A:1, SMALL:1, MARK:1, ABBR:1, BR:1, SUB:1, SUP:1, BIG:1,
                TT:1, VAR:1, Q:1, CITE:1};
  var MAX_PLATZ = 6;                 // ein Absatz mit zwoelf Tags ist Layout

  function musterSchluessel(el){
    var teile = [], zahl = 0, hatText = false, kinder = el.childNodes;
    for (var i = 0; i < kinder.length; i++){
      var k = kinder[i];
      if (k.nodeType === 3){
        if (k.nodeValue.replace(/\s/g, '')) hatText = true;
        teile.push(k.nodeValue.replace(/\s+/g, ' '));
      } else if (k.nodeType === 8){
        // Kommentar: der Extraktor entfernt Kommentare vor dem Parsen, hier
        // muss er deshalb genauso verschwinden — sonst waeren die Schluessel
        // beider Seiten verschieden und keiner traefe.
        continue;
      } else if (k.nodeType === 1){
        if (!INLINE[k.nodeName]) return null;
        if (++zahl > MAX_PLATZ) return null;
        teile.push('{' + (zahl - 1) + '}');
      } else {
        return null;
      }
    }
    if (!zahl || !hatText) return null;
    return teile.join('').replace(/^\s+|\s+$/g, '');
  }

  function musterEinsetzen(el){
    if (!KAT || el.__i18nMuster) return;
    var schluessel = musterSchluessel(el);
    if (!schluessel) return;
    var ziel = KAT[schluessel];
    if (!ziel) ziel = KAT[schluessel.replace(/\s+/g, ' ')];
    if (!ziel) return;
    var kinder = [], i;
    for (i = 0; i < el.childNodes.length; i++){
      if (el.childNodes[i].nodeType === 1) kinder.push(el.childNodes[i]);
    }
    var stuecke = ziel.split(/\{(\d+)\}/);   // gerade = Text, ungerade = Index
    // Jeder Platzhalter genau einmal, keiner erfunden, keiner vergessen.
    // Fehlt einer, wuerde das Kind-Element beim Umbau verschwinden — ein
    // fehlender Link ist schlimmer als ein deutscher Satz. Dann lieber gar
    // nicht uebersetzen.
    var benutzt = {};
    for (i = 1; i < stuecke.length; i += 2){
      var idx = +stuecke[i];
      if (!(idx >= 0 && idx < kinder.length) || benutzt[idx]) return;
      benutzt[idx] = 1;
    }
    for (i = 0; i < kinder.length; i++){ if (!benutzt[i]) return; }
    // Erst den Ersatz bauen: appendChild VERSCHIEBT die Kind-Elemente aus el
    // in das Fragment. Deshalb trifft das Leeren danach sie nicht mehr —
    // umgekehrte Reihenfolge wuerde sie loeschen, bevor sie gerettet sind.
    var frag = document.createDocumentFragment();
    for (i = 0; i < stuecke.length; i++){
      if (i % 2 === 0){
        if (!stuecke[i]) continue;
        var tn = document.createTextNode(stuecke[i]);
        tn.__fertig = 1;                 // nicht noch einmal nachschlagen
        frag.appendChild(tn);
      } else {
        frag.appendChild(kinder[+stuecke[i]]);
      }
    }
    el.__i18nMuster = 1;                 // der Beobachter sieht den Umbau
    while (el.firstChild) el.removeChild(el.firstChild);
    el.appendChild(frag);
  }

  function knoten(n){
    if (n.nodeType === 3){                       // Textknoten
      if (n.__fertig) return;                    // v4.2-W6: schon gesetzt
      if (n.parentNode && TABU[n.parentNode.nodeName]) return;
      if (n.parentNode && n.parentNode.closest && n.parentNode.closest('[data-i18n-skip]')) return;
      var neu = uebersetze(n.nodeValue);
      if (neu !== null && neu !== n.nodeValue){
        // Das Original merken, sonst laesst sich nicht zurueckschalten und ein
        // zweiter Durchlauf wuerde bereits Uebersetztes nicht mehr finden.
        if (n.__de === undefined) n.__de = n.nodeValue;
        n.nodeValue = neu;
      }
      return;
    }
    if (n.nodeType !== 1) return;
    if (TABU[n.nodeName] || n.hasAttribute('data-i18n-skip')) return;
    for (var i=0;i<ATTRS.length;i++){
      var a = ATTRS[i];
      if (!n.hasAttribute(a)) continue;
      var wert = n.getAttribute(a), neuA = uebersetze(wert);
      if (neuA !== null && neuA !== wert){
        if (!n.hasAttribute('data-de-'+a)) n.setAttribute('data-de-'+a, wert);
        n.setAttribute(a, neuA);
      }
    }
    // v4.2-W6 VOR dem Abstieg: danach sind die Textknoten andere.
    musterEinsetzen(n);
    for (var c = n.firstChild; c; c = c.nextSibling) knoten(c);
  }

  function alles(wurzel){
    if (!KAT || !Object.keys(KAT).length) return;
    knoten(wurzel || document.body);
  }

  // Nachgeladene Inhalte: das Dashboard baut Tabellen und Panels per JS. Ohne
  // Beobachter waere alles uebersetzt, was beim Laden schon dastand — und
  // alles danach wieder deutsch. Genau der halb uebersetzte Zustand, den der
  // Browser-Ansatz vermeiden soll.
  var beobachter = null;
  function beobachten(){
    if (beobachter || !window.MutationObserver) return;
    beobachter = new MutationObserver(function(liste){
      if (!KAT || !Object.keys(KAT).length) return;
      for (var i=0;i<liste.length;i++){
        var m = liste[i];
        for (var j=0;j<m.addedNodes.length;j++) knoten(m.addedNodes[j]);
        if (m.type === 'characterData' && m.target) knoten(m.target);
      }
    });
    beobachter.observe(document.body, {childList:true, subtree:true, characterData:true});
  }

  function umschalterBauen(sprachen, aktiv){
    var wo = document.querySelector('[data-i18n-switch]');
    if (!wo || sprachen.length < 2) return;
    var sel = document.createElement('select');
    sel.className = 'i18n-switch';
    sel.setAttribute('aria-label', 'Sprache / Language');
    sel.setAttribute('data-i18n-skip','');       // sich selbst nie uebersetzen
    sprachen.forEach(function(s){
      var o = document.createElement('option');
      o.value = s.code; o.textContent = s.name;
      if (s.code === aktiv) o.selected = true;
      sel.appendChild(o);
    });
    sel.addEventListener('change', function(){
      fetch('/api/i18n/waehlen', {method:'POST', headers:{'Content-Type':'application/json'},
                                 body: JSON.stringify({sprache: sel.value})})
        .then(function(){ location.reload(); })   // Neuladen ist ehrlicher als
        .catch(function(){ location.reload(); }); // ein halb zurueckgedrehtes DOM
    });
    wo.appendChild(sel);
  }

  fetch('/api/i18n/katalog').then(function(r){ return r.json(); }).then(function(d){
    if (!d || !d.ok) return;
    SPRACHE = d.sprache || 'de';
    KAT = d.strings || {};
    document.documentElement.setAttribute('lang', SPRACHE);
    alles(document.body);
    beobachten();
    return fetch('/api/i18n/sprachen').then(function(r){ return r.json(); });
  }).then(function(d){
    if (d && d.ok) umschalterBauen(d.sprachen || [], d.aktiv || SPRACHE);
  }).catch(function(){ /* ohne Katalog bleibt alles deutsch — das ist der Fallback */ });

  // Fuer Code, der selbst uebersetzen will (Meldungen vor dem Einfuegen).
  window.T = function(text){ var u = uebersetze(text); return u === null ? text : u; };
})();"""


@bp.route("/api/i18n/uebersetzer.js")
def api_i18n_js():
    """Der Uebersetzer, den die drei Oberflaechen einbinden.

    Eine Stunde Cache: der Code aendert sich selten, der KATALOG dagegen kommt
    aus /api/i18n/katalog und wird nicht mitgecacht — eine neue Uebersetzung
    ist damit sofort sichtbar, ohne dass jemand hart neu laden muss.
    """
    antwort = Response(_UEBERSETZER_JS, mimetype="application/javascript")
    antwort.headers["Cache-Control"] = "public, max-age=3600"
    return antwort
