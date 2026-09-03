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
    var roh = text.trim();
    if (!roh) return null;
    var treffer = KAT[roh];
    if (!treffer) return null;
    // Rand-Leerzeichen erhalten: viele Knoten sind " Text " mit Einrueckung,
    // und ein Trim wuerde das Layout veraendern.
    return text.replace(roh, treffer);
  }

  function knoten(n){
    if (n.nodeType === 3){                       // Textknoten
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
