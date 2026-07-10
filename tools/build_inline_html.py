#!/usr/bin/env python3
"""Build a single self-contained "inline" hub HTML file.

Consolidates the individual page HTML files of this repo into ONE file
(`howto290626.html`) so it can be uploaded to a static host as a single
document. Every local JavaScript asset is inlined and every image is
re-encoded to WebP and embedded as a base64 data URI, which keeps the
output small enough to clear typical upload size limits.

Run locally:
    pip install Pillow
    python3 tools/build_inline_html.py

Or trigger the "Build inline HTML" GitHub Action and download the
resulting file from the workflow run's artifacts.

Tunables (env vars, also exposed as workflow inputs):
    WEBP_QUALITY    WebP quality 1-100        (default 80)
    WEBP_MAX_WIDTH  max image width in px,    (default 1280; 0 = keep size)
    OUTPUT_FILE     output filename           (default howto290626.html)
"""

import base64
import io
import os
import re
import sys
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent

# Pages included in the hub, in navigation order.
# The first entry is the default view shown when no #hash is present.
PAGES = [
    "index.html",
    "playbook.html",
    "agent-principles.html",
    "our-agents.html",
    "token-economics.html",
    "api-key.html",
    "web-app-guide.html",
    "local-app-guide.html",
    "CYBAIMakerUpdateSlides.html",
]

WEBP_QUALITY = int(os.environ.get("WEBP_QUALITY", "80"))
WEBP_MAX_WIDTH = int(os.environ.get("WEBP_MAX_WIDTH", "1280"))
OUTPUT_FILE = os.environ.get("OUTPUT_FILE", "howto290626.html")

# Sentinel used to escape literal </script> inside the embedded page text,
# because each page lives inside a <script type="text/html"> block. The
# router script (below) reverses this when injecting the page into the iframe.
SENTINEL = "__WS_CLOSE_SCRIPT__"

RASTER_EXT = {".png", ".jpg", ".jpeg", ".gif", ".bmp", ".webp"}

SHELL_HEAD = """<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Wavestone CYB AI Maker Initiative — Hub</title>
<style>
  html,body{margin:0;padding:0;height:100%;background:#fff}
  body{overflow:hidden}
  #ws-view{display:block;border:0;width:100%;height:100vh;height:100dvh}
  #ws-noscript{font-family:system-ui,sans-serif;padding:40px;text-align:center;color:#3A3550}
</style>
</head>
<body>
<iframe id="ws-view" title="Wavestone CYB AI Maker" referrerpolicy="no-referrer"></iframe>
<noscript><div id="ws-noscript">Ce portail consolid&eacute; n&eacute;cessite JavaScript pour afficher les pages.</div></noscript>
"""

# Injected into every page (before </body>): rewrites internal .html links
# into a postMessage to the parent shell, and restores the de-duplicated
# zoom-anchor hrefs from their inlined <img> source at runtime.
NAV_SCRIPT = """<script>
/* consolidated-hub: intercept internal .html navigation -> tell parent shell */
(function(){
  if (window === window.parent) return;
  document.addEventListener('click', function(e){
    var a = e.target.closest && e.target.closest('a[href]');
    if (!a) return;
    if (a.target && a.target === '_blank') return;
    var h = a.getAttribute('href') || '';
    var m = h.match(/^([A-Za-z0-9_\\-]+\\.html)(#.*)?$/);
    if (m){ e.preventDefault(); parent.postMessage({wsNav: m[1], hash: m[2]||''}, '*'); }
  }, true);
  // Re-point de-duplicated zoom anchors to their (inlined) image source.
  function wireZoom(){
    var zs = document.querySelectorAll('a.zoom');
    for (var i=0;i<zs.length;i++){
      var img = zs[i].querySelector('img');
      if (img && !zs[i].getAttribute('href')) zs[i].setAttribute('href', img.src);
    }
  }
  if (document.readyState === 'loading'){
    document.addEventListener('DOMContentLoaded', wireZoom);
  } else { wireZoom(); }
})();
</script>"""

# Top-level router: reads every page block, restores the sentinel, and swaps
# the iframe's srcdoc based on the URL hash / postMessage navigation.
ROUTER_SCRIPT = """<script>
(function(){
  var PAGES = {};
  var SENT = '__WS_CLOSE_SCRIPT__';
  var CLOSE = '<' + '/script>';
  var holders = document.querySelectorAll('script[type="text/html"][data-page]');
  for (var i=0;i<holders.length;i++){
    var n = holders[i].getAttribute('data-page');
    PAGES[n] = holders[i].textContent.split(SENT).join(CLOSE);
  }
  var view = document.getElementById('ws-view');
  var current = '';
  function norm(n){ if(!n || !PAGES.hasOwnProperty(n)) n='index.html'; return n; }
  function show(name){
    name = norm(name);
    if (name !== current){ current = name; view.srcdoc = PAGES[name]; }
    if (location.hash.slice(1) !== name){
      history.replaceState(null, '', '#' + name);
    }
  }
  window.addEventListener('message', function(e){
    var d = e.data || {};
    if (d && d.wsNav) show(d.wsNav);
  });
  window.addEventListener('hashchange', function(){
    show(location.hash.slice(1));
  });
  show(location.hash.slice(1) || 'index.html');
})();
</script>"""

_datauri_cache = {}


def asset_data_uri(rel_path):
    """Return a base64 data URI for a local asset, re-encoding raster
    images to WebP. SVGs are embedded as-is. Results are cached per path."""
    if rel_path in _datauri_cache:
        return _datauri_cache[rel_path]

    path = (ROOT / rel_path).resolve()
    if not path.is_file():
        print(f"  ! missing asset, left untouched: {rel_path}", file=sys.stderr)
        _datauri_cache[rel_path] = None
        return None

    ext = path.suffix.lower()
    if ext == ".svg":
        raw = path.read_bytes()
        uri = "data:image/svg+xml;base64," + base64.b64encode(raw).decode()
    elif ext in RASTER_EXT:
        im = Image.open(path)
        im = im.convert("RGBA") if im.mode in ("RGBA", "LA", "P") else im.convert("RGB")
        if WEBP_MAX_WIDTH and im.width > WEBP_MAX_WIDTH:
            new_h = round(im.height * WEBP_MAX_WIDTH / im.width)
            im = im.resize((WEBP_MAX_WIDTH, new_h), Image.LANCZOS)
        buf = io.BytesIO()
        im.save(buf, "WEBP", quality=WEBP_QUALITY, method=6)
        uri = "data:image/webp;base64," + base64.b64encode(buf.getvalue()).decode()
    else:
        raw = path.read_bytes()
        uri = "data:application/octet-stream;base64," + base64.b64encode(raw).decode()

    _datauri_cache[rel_path] = uri
    return uri


def strip_zoom_href(html):
    """Remove href from <a class="zoom"> anchors so each screenshot is only
    embedded once (via its <img>). NAV_SCRIPT rewires the href at runtime."""
    def repl(m):
        tag = m.group(0)
        if 'class="zoom"' in tag:
            tag = re.sub(r'\s+href="[^"]*"', "", tag, count=1)
        return tag
    return re.sub(r"<a\b[^>]*>", repl, html)


def inline_js_assets(html):
    """Replace <script src="assets/foo.js"></script> with the file inlined."""
    def repl(m):
        rel = m.group(1)
        path = (ROOT / "assets" / rel).resolve()
        if not path.is_file():
            print(f"  ! missing JS asset, left untouched: assets/{rel}", file=sys.stderr)
            return m.group(0)
        return "<script>\n" + path.read_text(encoding="utf-8") + "\n</script>"
    return re.sub(
        r'<script\b[^>]*\bsrc="assets/([^"]+\.js)"[^>]*>\s*</script>',
        repl,
        html,
    )


def inline_images(html):
    """Replace src=/href= references to local image assets with data URIs."""
    def repl(m):
        attr, rel = m.group(1), m.group(2)
        uri = asset_data_uri(rel)
        return f'{attr}="{uri}"' if uri else m.group(0)
    return re.sub(
        r'(src|href)="(assets/[^"]+\.(?:png|jpe?g|gif|bmp|webp|svg))"',
        repl,
        html,
    )


def build_page_block(name):
    src = ROOT / name
    html = src.read_text(encoding="utf-8")

    html = inline_js_assets(html)
    html = strip_zoom_href(html)
    html = inline_images(html)

    # Inject the navigation/zoom helper just before the page's closing body.
    if "</body>" in html:
        html = html.replace("</body>", NAV_SCRIPT + "\n</body>", 1)
    else:
        html += NAV_SCRIPT

    # Escape every closing script tag so it survives inside the wrapper block.
    escaped = re.sub(r"</script\s*>", SENTINEL, html, flags=re.IGNORECASE)

    return (
        f'<script type="text/html" data-page="{name}">'
        + escaped
        + "</script>"
    )


def main():
    print(
        f"Building {OUTPUT_FILE}  (webp q={WEBP_QUALITY}, "
        f"max width={WEBP_MAX_WIDTH or 'none'})"
    )
    blocks = []
    for name in PAGES:
        if not (ROOT / name).is_file():
            print(f"  ! skipping missing page: {name}", file=sys.stderr)
            continue
        print(f"  + {name}")
        blocks.append(build_page_block(name))

    out = SHELL_HEAD + "\n" + "\n".join(blocks) + "\n" + ROUTER_SCRIPT + "\n</body>\n</html>\n"

    out_path = ROOT / OUTPUT_FILE
    out_path.write_text(out, encoding="utf-8")

    size = out_path.stat().st_size
    print(f"\nWrote {out_path}  ({size/1024/1024:.2f} MB, {len(blocks)} pages)")


if __name__ == "__main__":
    main()
