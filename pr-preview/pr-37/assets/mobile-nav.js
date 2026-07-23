/* ============================================================================
   Wavestone CYB AI Maker Initiative — shared mobile navigation
   ----------------------------------------------------------------------------
   On small screens the top-bar links used to wrap into a tall vertical column
   that ate most of the viewport. This script turns them into a compact
   hamburger menu instead, on every page, without touching each page's markup.

   It works with both bar variants used across the hub:
     • <div class="nav-links"> … </div>   (index, playbook, principles, …)
     • <div class="nav"> … </div>         (web-app-guide, local-app-guide)

   The language selector (.langsel) — whether hard-coded in the page or injected
   by assets/i18n.js — is moved inside the nav container so it collapses into the
   same dropdown, keeping the bar itself clean: just the brand + the toggle.
   ========================================================================== */
(function () {
  'use strict';

  var BREAKPOINT = 820; // px — below this the links collapse into the menu

  function injectStyles() {
    if (document.getElementById('ws-mobilenav-css')) return;
    var css =
      '.ws-burger{display:none}' +
      '@media(max-width:' + BREAKPOINT + 'px){' +
        '.bar-in{flex-wrap:nowrap!important;gap:12px}' +
        '.brand{font-size:14px;min-width:0}' +
        '.ws-burger{display:flex;flex-direction:column;justify-content:center;' +
          'align-items:center;gap:5px;width:42px;height:42px;flex:0 0 auto;' +
          'margin-left:auto;background:#fff;cursor:pointer;padding:0;' +
          'border:1px solid var(--ws-ink-200,#CFCCDC);color:var(--ws-ink-700,#3A3550)}' +
        '.ws-burger span{display:block;width:20px;height:2px;background:currentColor;' +
          'transition:transform .22s ease,opacity .22s ease}' +
        '.nav-links,.nav{position:absolute;top:100%;left:0;right:0;margin:0;' +
          'flex-direction:column;align-items:stretch;gap:8px;padding:14px 20px 18px;' +
          'background:rgba(255,255,255,.98);-webkit-backdrop-filter:blur(10px);' +
          'backdrop-filter:blur(10px);border-bottom:1px solid var(--ws-ink-100,#E6E4EE);' +
          'box-shadow:0 14px 28px rgba(22,18,31,.14);flex-wrap:nowrap;' +
          'max-height:calc(100vh - 100%);overflow:auto;display:none}' +
        '.bar.nav-open .nav-links,.bar.nav-open .nav{display:flex}' +
        '.nav-links a.jump,.nav a.jump{width:100%;text-align:center;' +
          'padding:12px 14px;font-size:14px}' +
        '.nav-links .langsel,.nav .langsel{align-self:center;margin:6px auto 0}' +
        '.bar.nav-open .ws-burger span:nth-child(1){transform:translateY(7px) rotate(45deg)}' +
        '.bar.nav-open .ws-burger span:nth-child(2){opacity:0}' +
        '.bar.nav-open .ws-burger span:nth-child(3){transform:translateY(-7px) rotate(-45deg)}' +
      '}';
    var s = document.createElement('style');
    s.id = 'ws-mobilenav-css';
    s.textContent = css;
    document.head.appendChild(s);
  }

  function init() {
    var bar = document.querySelector('.bar');
    var barIn = document.querySelector('.bar-in');
    var nav = document.querySelector('.nav-links, .nav');
    if (!bar || !barIn || !nav) return;
    if (barIn.querySelector('.ws-burger')) return; // already initialised

    injectStyles();

    // Pull the language selector into the nav so it collapses with the menu.
    function relocateLang() {
      var ls = document.querySelector('.langsel');
      if (ls && ls.parentNode !== nav) nav.appendChild(ls);
    }
    relocateLang();
    // assets/i18n.js may inject .langsel after us — catch it, then stop watching.
    if (window.MutationObserver) {
      var mo = new MutationObserver(relocateLang);
      mo.observe(barIn, { childList: true });
      setTimeout(function () { mo.disconnect(); }, 4000);
    }

    var btn = document.createElement('button');
    btn.type = 'button';
    btn.className = 'ws-burger';
    btn.setAttribute('aria-label', 'Menu');
    btn.setAttribute('aria-expanded', 'false');
    btn.innerHTML = '<span></span><span></span><span></span>';
    barIn.appendChild(btn);

    function setOpen(open) {
      bar.classList.toggle('nav-open', open);
      btn.setAttribute('aria-expanded', open ? 'true' : 'false');
    }

    btn.addEventListener('click', function (e) {
      e.stopPropagation();
      setOpen(!bar.classList.contains('nav-open'));
    });
    nav.addEventListener('click', function (e) {
      if (e.target.closest('a')) setOpen(false); // close after picking a link
    });
    document.addEventListener('click', function (e) {
      if (bar.classList.contains('nav-open') && !bar.contains(e.target)) setOpen(false);
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' || e.keyCode === 27) setOpen(false);
    });
    window.addEventListener('resize', function () {
      if (window.innerWidth > BREAKPOINT) setOpen(false);
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
