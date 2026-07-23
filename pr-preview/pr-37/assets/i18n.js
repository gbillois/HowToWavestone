/* ============================================================================
   Wavestone CYB AI Maker Initiative — shared i18n engine (FR / EN / DE)
   ----------------------------------------------------------------------------
   Same mechanism as web-app-guide.html, factored into one file so every page
   behaves identically:

     • French is the ORIGINAL text written directly in the HTML.
     • Each page declares only its EN + DE strings on window.WS_I18N:

         window.WS_I18N = {
           en: { "hero.title": "…", "__title": "Page title in English" },
           de: { "hero.title": "…", "__title": "Seitentitel auf Deutsch" }
         };

     • Tag translatable nodes with data-i18n="key" (innerHTML is swapped).
       Attributes are supported too: data-i18n-alt / -title / -aria-label /
       -content / -placeholder = "key".
     • The "__title" key (optional) translates the document <title>.

   On load the engine:
     1. injects the FR/EN/DE selector top-right of .bar-in (created if missing),
     2. picks the language: saved choice > browser language > English,
     3. swaps every tagged node, persists the choice under "ws_lang".

   The choice is shared across all pages (same storage key), so the language
   follows the visitor as they navigate the hub.
   ========================================================================== */
(function () {
  'use strict';

  var SUPPORTED = ['fr', 'en', 'de'];
  var DEFAULT = 'en';
  var KEY = 'ws_lang';
  var COPY = {
    fr: { copy: 'copier', copied: 'copié ✓' },
    en: { copy: 'copy', copied: 'copied ✓' },
    de: { copy: 'kopieren', copied: 'kopiert ✓' }
  };
  var ATTRS = [
    ['data-i18n-alt', 'alt'],
    ['data-i18n-title', 'title'],
    ['data-i18n-aria-label', 'aria-label'],
    ['data-i18n-content', 'content'],
    ['data-i18n-placeholder', 'placeholder']
  ];

  function detect() {
    try {
      var s = localStorage.getItem(KEY);
      if (s && SUPPORTED.indexOf(s) !== -1) return s;
    } catch (e) { /* storage blocked */ }
    var langs = navigator.languages || [navigator.language || navigator.userLanguage || ''];
    for (var i = 0; i < langs.length; i++) {
      var c = (langs[i] || '').slice(0, 2).toLowerCase();
      if (SUPPORTED.indexOf(c) !== -1) return c;
    }
    return DEFAULT;
  }

  function injectStyles() {
    if (document.getElementById('ws-langsel-css')) return;
    var css =
      '.langsel{display:flex;align-items:stretch;margin-left:auto;flex:0 0 auto;' +
      'border:1px solid var(--ws-ink-200,#CFCCDC);overflow:hidden;background:#fff}' +
      '.langsel.floating{position:fixed;top:12px;right:12px;z-index:1000;' +
      'box-shadow:0 4px 12px rgba(22,18,31,.14)}' +
      '.langsel button{font-family:var(--ws-font-mono,ui-monospace,monospace);font-size:12px;' +
      'padding:6px 11px;background:#fff;border:none;border-left:1px solid var(--ws-ink-100,#E6E4EE);' +
      'color:var(--ws-ink-500,#6B6580);cursor:pointer;line-height:1;transition:.15s ease}' +
      '.langsel button:first-child{border-left:none}' +
      '.langsel button.on{background:var(--ws-indigo-600,#451DC7);color:#fff;font-weight:600}' +
      '.langsel button:hover:not(.on){color:var(--ws-indigo-600,#451DC7)}' +
      '@media(prefers-reduced-motion:reduce){.langsel button{transition:none}}';
    var s = document.createElement('style');
    s.id = 'ws-langsel-css';
    s.textContent = css;
    document.head.appendChild(s);
  }

  function ensureSelector() {
    var sel = document.querySelector('.langsel');
    if (!sel) {
      sel = document.createElement('div');
      sel.className = 'langsel';
      sel.setAttribute('role', 'group');
      sel.setAttribute('aria-label', 'Language / Langue / Sprache');
      SUPPORTED.forEach(function (l) {
        var b = document.createElement('button');
        b.type = 'button';
        b.setAttribute('data-lang', l);
        b.setAttribute('aria-label', l.toUpperCase());
        b.textContent = l.toUpperCase();
        sel.appendChild(b);
      });
      var barIn = document.querySelector('.bar-in');
      if (barIn) {
        barIn.appendChild(sel);
      } else {
        sel.classList.add('floating');
        document.body.appendChild(sel);
      }
    }
    return sel;
  }

  function run() {
    injectStyles();

    var I18N = window.WS_I18N || {};
    var sel = ensureSelector();

    var nodes = Array.prototype.slice.call(document.querySelectorAll('[data-i18n]'));
    var ORIG = {};
    nodes.forEach(function (n) { ORIG[n.getAttribute('data-i18n')] = n.innerHTML; });

    // capture original (French) attribute values
    var attrNodes = [];
    ATTRS.forEach(function (pair) {
      var found = document.querySelectorAll('[' + pair[0] + ']');
      for (var i = 0; i < found.length; i++) {
        var el = found[i];
        attrNodes.push({ el: el, key: el.getAttribute(pair[0]), attr: pair[1], orig: el.getAttribute(pair[1]) });
      }
    });

    var ORIG_TITLE = document.title;

    function pick(lang, key, fallback) {
      if (lang === 'fr') return fallback;
      return (I18N[lang] && I18N[lang][key] != null) ? I18N[lang][key] : fallback;
    }

    function apply(lang) {
      if (SUPPORTED.indexOf(lang) === -1) lang = DEFAULT;
      if (lang !== 'fr' && !I18N[lang]) lang = 'fr';
      document.documentElement.lang = lang;

      nodes.forEach(function (n) {
        var v = pick(lang, n.getAttribute('data-i18n'), ORIG[n.getAttribute('data-i18n')]);
        if (v != null) n.innerHTML = v;
      });

      attrNodes.forEach(function (a) {
        var v = pick(lang, a.key, a.orig);
        if (v != null) a.el.setAttribute(a.attr, v);
      });

      document.title = pick(lang, '__title', ORIG_TITLE);

      var labels = COPY[lang] || COPY.fr;
      var copies = document.querySelectorAll('.copy');
      for (var i = 0; i < copies.length; i++) {
        if (!copies[i].classList.contains('ok')) copies[i].textContent = labels.copy;
      }

      var btns = sel.querySelectorAll('button');
      for (var j = 0; j < btns.length; j++) {
        btns[j].classList.toggle('on', btns[j].getAttribute('data-lang') === lang);
      }

      try { localStorage.setItem(KEY, lang); } catch (e) { /* ignore */ }
    }

    var btns = sel.querySelectorAll('button');
    for (var k = 0; k < btns.length; k++) {
      btns[k].addEventListener('click', function () { apply(this.getAttribute('data-lang')); });
    }

    apply(detect());

    // expose for pages that want to react to language changes
    window.WSI18N = { apply: apply, current: function () { return document.documentElement.lang; } };
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', run);
  } else {
    run();
  }
})();
