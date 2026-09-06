#!/usr/bin/env python3
"""
Applies patches to Jellyfin's index.html. Safe to re-run.
  1. Live TV tab between Home and Favorites
  2. Now-line v7: uses grid.scrollLeft (exact now position) once programCell-active confirms load
"""
import os, sys, re
import hashlib as _h   # used by sf-ls-external (line ~17013) and the build stamp

PATH = sys.argv[1] if len(sys.argv) > 1 else '/tmp/jf_index.html'
# --- payload constants (203 of them, ~1.1MB of JS/CSS) live in jfblocks/.
# What remains here is the orchestration: read index.html, strip and
# re-inject each marker-guarded block, write it back.
from jfblocks import *  # noqa: F401,F403



with open(PATH) as f:
    html = f.read()

changed = False
# sf-config: optional, install-specific values. Everything here is OPTIONAL and
# defaults to empty -- each consumer guards for that, because a blank id fed to
# indexOf() returns 0 and would match every element on the page. Read at BUILD
# time and inlined, so the browser needs no extra request.
import json as _json
_cfg_path = os.environ.get('SF_CONFIG_FILE') or os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.json')
try:
    with open(_cfg_path, encoding='utf-8') as _cf:
        _cfg = _json.load(_cf)
except (OSError, ValueError):
    _cfg = {}
_cfg_js = '<script>window.SF_CONFIG=' + _json.dumps(_cfg, separators=(',', ':')) + ';</script>'
html = re.sub(r'<script>window\.SF_CONFIG=.*?</script>', '', html, flags=re.S)
html = html.replace('<head>', '<head>' + _cfg_js, 1)
print('patched: sf-config (%d key%s)' % (len(_cfg), '' if len(_cfg) == 1 else 's'))
changed = True

for v in ['v1','v2','v3','v4','v5','v6','v7']:
    marker = f'jf-now-line-{v}'
    if marker in html:
        html = re.sub(
            r'<script>\(function\(\)\{.*?' + re.escape(marker) + r'.*?\}\)\(\);</script>',
            '', html
        )
        print(f'removed: {marker}')
        changed = True

# Strip any prior copy, then always re-inject -- see unfreeze note. This was
# `if HOME_MARKER not in html: ... else: skip`, i.e. write-once, so every later
# edit to HOME_SCRIPT was silently discarded on an already-patched file.
if re.search(r'<script>\(function\(\)\{function addHomeTab', html):
    html = re.sub(r'<script>\(function\(\)\{function addHomeTab.*?\}\)\(\);</script>', '', html, flags=re.S)
    print('removed old home')
    html = html.replace('</body>', HOME_SCRIPT + '</body>')
    print('patched: home tab on live tv')
    changed = True

# Strip any prior copy, then always re-inject -- see unfreeze note. This was
# `if ENDSAT_MARKER not in html: ... else: skip`, i.e. write-once, so every later
# edit to ENDSAT_SCRIPT was silently discarded on an already-patched file.
# The re-inject must sit OUTSIDE the guard. It was indented INTO it, which means
# "re-inject only if already present" -- so once the block was missing (a Jellyfin
# image update resets index.html) it could never come back, and jf-endsat-12h is in
# apply_jf_patch.sh's early-exit chain. Net effect: the chain never matched, so the
# 10-minute cron re-patched index.html forever. Verified the strip regex round-trips
# ENDSAT_SCRIPT exactly, so strip-then-always-inject is idempotent.
if re.search(r'<script>\(function\(\)\{ /\* jf-endsat-12h \*/', html):
    html = re.sub(r'<script>\(function\(\)\{ /\* jf-endsat-12h \*/.*?\}\)\(\);</script>', '', html, flags=re.S)
    print('removed old endsat')
html = html.replace('</body>', ENDSAT_SCRIPT + '</body>')
print('patched: ends-at 12h')
changed = True

# custom Live Sports browse page (streamfree.top-style cards, hooked into the
# guide filter's "Live Sports" pill): strip any prior version, then (re)inject
if LIVESPORTS_MARKER in html:
    html = re.sub(r'<script>\(function\(\)\{\s*/\* sf-livesports \*/.*?\}\)\(\);</script>', '', html, flags=re.S)
    html = re.sub(r'<script src="sf-livesports\.js[^"]*"></script>', '', html)
    print('removed old live sports page')
# sf-ls-external: this closure is 593KB -- 58% of index.html -- and index.html is
# served no-cache, so every page load re-downloaded and re-parsed all of it even
# though most sessions never open Live Sports. Ship it as a separate file: the
# <script src> sits exactly where the inline block sat and, with no defer/async,
# executes in the same document order, so semantics are unchanged. The browser
# then caches it by ETag across loads. The ?v= hash busts that cache on edit.
_ls_body = LIVESPORTS_SCRIPT
if _ls_body.startswith('<script>'):
    _ls_body = _ls_body[len('<script>'):]
if _ls_body.endswith('</script>'):
    _ls_body = _ls_body[:-len('</script>')]
_ls_hash = _h.sha1(_ls_body.encode('utf-8')).hexdigest()[:10]
_ls_file = os.environ.get('SF_JS_OUT') or os.path.join(os.path.dirname(PATH), 'sf-livesports.js')
try:
    _ls_cur = open(_ls_file, encoding='utf-8').read()
except OSError:
    _ls_cur = None
if _ls_cur != _ls_body:
    with open(_ls_file, 'w', encoding='utf-8') as _f:
        _f.write(_ls_body)
    print('wrote sf-livesports.js (%d bytes)' % len(_ls_body))
html = html.replace('</body>', '<script src="sf-livesports.js?v=' + _ls_hash + '"></script></body>')
print('patched: core runtime (motion, navigation lifecycle, detail pages, music)')
changed = True

if TYPINGGUARD_MARKER in html:
    html = re.sub(r'<script>\(function\(\)\{\s*/\* jf-typing-guard \*/.*?\}\)\(\);</script>', '', html, flags=re.S)
    print('removed old typing guard')
html = html.replace('</body>', TYPINGGUARD_SCRIPT + '</body>')
print('patched: typing guard (Jellyfin Enhanced shortcuts ignored inside text fields)')
changed = True

# header fix: strip any prior version, then (re)inject the current one
if HEADERFIX_MARKER in html:
    html = re.sub(r'<style id="sf-header-fix">.*?</style>', '', html, flags=re.S)
    print('removed old header fix')
html = html.replace('</body>', HEADERFIX_STYLE + '</body>')
print('patched: header fix (back/home nav on library pages)')
changed = True

# subtitle lift: strip any prior version, then (re)inject the current one
if SUBLIFT_MARKER in html:
    html = re.sub(r'<style id="sf-sub-lift">.*?</style>', '', html, flags=re.S)
    print('removed old subtitle lift')
html = html.replace('</body>', SUBLIFT_STYLE + '</body>')
print('patched: subtitle lift (keep subs above the control bar)')
changed = True

# subtitle abyss theme: strip any prior version, then (re)inject the current one
if SUBABYSS_MARKER in html:
    html = re.sub(r'<style id="sf-sub-abyss">.*?</style>', '', html, flags=re.S)
    print('removed old subtitle abyss theme')
html = html.replace('</body>', SUBABYSS_STYLE + '</body>')
print('patched: subtitle abyss theme (uniform boxless subs)')
changed = True

# ui consistency: strip any prior version, then (re)inject the current one
if SFUICONS_MARKER in html:
    html = re.sub(r'<style id="sf-ui-consistency">.*?</style>', '', html, flags=re.S)
    print('removed old ui consistency')
html = html.replace('</body>', SFUICONS_STYLE + '</body>')
print('patched: ui consistency (row spacing, trackpad row scrolling)')
changed = True

# row arrows: strip any prior version, then (re)inject the current one
if ROWARROWFIX_MARKER in html:
    html = re.sub(r'<script>\(function\(\)\{/\* sf-row-arrowfix \*/.*?\}\)\(\);</script>', '', html, flags=re.S)
    print('removed old row arrows')
html = html.replace('</body>', ROWARROWFIX_SCRIPT + '</body>')
print('patched: row arrows (scroll buttons work with native scrolling)')
changed = True

# music cover pin: REMOVED. Inline setProperty(...,'important') is the top of the CSS
# cascade, yet the width/height it wrote were GONE moments later while the data attribute
# set on the same line survived -- something rewrites these posters' style attribute. A pin
# that gets wiped is just a timer doing nothing, so it is gone.
if 'sf-music-pin' in html:
    html = re.sub(r'<script>\(function\(\)\{/\* sf-music-pin \*/.*?\}\)\(\);</script>', '', html, flags=re.S)
    print('removed old music pin script')
    changed = True

# hero gap: REMOVED. It sized the rows' top padding to the hero button, but the button
# sits at 430 on continue slides and 388 on play slides, so the whole row shifted on every
# carousel rotation -- reported as the Continue Watching row jumping up and down. A static
# padding (sf-ui-consistency) cannot move, so it cannot jump.
if 'sf-hero-gap' in html:
    html = re.sub(r'<script>\(function\(\)\{/\* sf-hero-gap \*/.*?\}\)\(\);</script>', '', html, flags=re.S)
    print('removed old hero gap script')
    changed = True

# hero button: the JS version is GONE -- see sf-hero-rhythm in the style block. Three
# JS attempts all jittered (46px / 98px / 89px measured) because the carousel re-lays out
# the slide underneath them. Static CSS cannot fight back.
if 'sf-hero-btn' in html:
    html = re.sub(r'<script>\(function\(\)\{/\* sf-hero-btn \*/.*?\}\)\(\);</script>', '', html, flags=re.S)
    print('removed old hero button script')
    changed = True

# icon guard: strip any prior version, then (re)inject the current one
if ICONGUARD_MARKER in html:
    html = re.sub(r'<style id="sf-icon-guard">.*?</script>', '', html, flags=re.S)
    print('removed old icon guard')
html = html.replace('</body>', ICONGUARD_STYLE + '</body>')
print('patched: icon guard (no ligature text flash)')
changed = True

# JE subtitle-style gate: strip any prior version, then (re)inject the current one
if JEOFF_MARKER in html:
    html = re.sub(r'<script>\(function\(\)\{/\* sf-sub-je-off \*/.*?\}\)\(\);</script>', '', html, flags=re.S)
    print('removed old JE subtitle gate')
html = html.replace('</body>', JEOFF_SCRIPT + '</body>')
print('patched: JE subtitle-style gate (lets sf-sub-abyss own appearance)')
changed = True

# one subtitle renderer: strip any prior version, then (re)inject the current one
if ONEREND_MARKER in html:
    html = re.sub(r'<script>\(function\(\)\{/\* sf-sub-one-renderer \*/.*?\}\)\(\);</script>', '', html, flags=re.S)
    print('removed old one-renderer pin')
html = html.replace('</body>', ONEREND_SCRIPT + '</body>')

# seamless subtitle switching: strip any prior version, then (re)inject
if SEAMLESS_MARKER in html:
    html = re.sub(r'<script>\(function\(\)\{/\* sf-sub-seamless \*/.*?\}\)\(\);</script>', '', html, flags=re.S)
    print('removed old seamless-subtitle defaults')
html = html.replace('</body>', SEAMLESS_SCRIPT + '</body>')

# no home spinner: strip any prior version, then (re)inject the current one
if NOSPINNER_MARKER in html:
    html = re.sub(r'<style id="jf-no-home-spinner">.*?</style>', '', html, flags=re.S)
    print('removed old no-home-spinner')
html = html.replace('</body>', NOSPINNER_STYLE + '</body>')
print('patched: no home spinner (hides the HSS loading circle on home)')
changed = True

# scroller fix: strip any prior version, then (re)inject the current one
if SCROLLFIX_MARKER in html:
    html = re.sub(r'<script>\(function\(\)\{\s*/\* jf-scroller-fix \*/.*?\}\)\(\);</script>', '', html, flags=re.S)
    print('removed old scroller fix')
html = html.replace('</body>', SCROLLFIX_SCRIPT + '</body>')
print('patched: scroller fix (row next/prev arrows no longer crash blank)')
changed = True

# dedupe paging: strip any prior version, then (re)inject the current one
if DEDUPEPAGING_MARKER in html:
    html = re.sub(r'<script>\(function\(\)\{\s*/\* jf-dedupe-paging \*/.*?\}\)\(\);</script>', '', html, flags=re.S)
    print('removed old dedupe paging')
html = html.replace('</body>', DEDUPEPAGING_SCRIPT + '</body>')
print('patched: dedupe paging (hide duplicate X-Y of Z footer)')
changed = True

# crash recovery: strip any prior version, then (re)inject the current one
if CRASHRECOVERY_MARKER in html:
    html = re.sub(r'<script>\(function\(\)\{\s*/\* jf-crash-recovery \*/.*?\}\)\(\);</script>', '', html, flags=re.S)
    print('removed old crash recovery')
html = html.replace('</body>', CRASHRECOVERY_SCRIPT + '</body>')
print('patched: crash recovery (malformed #/list deep links bounce home instead of crashing blank)')
changed = True

# trailer exit button: removed 2026-07-25 -- the native Jellyfin Mobile app
# already shows its own back button/header chrome around the WebView during
# trailer playback, so this floating one was overlapping a real back button
# rather than filling a gap. Strip it from any already-patched install.
if 'jf-trailer-exit' in html:
    html = re.sub(r'<script>\(function\(\)\{\s*/\* jf-trailer-exit \*/.*?\}\)\(\);</script>', '', html, flags=re.S)
    print('removed trailer exit button (overlapped the native app\'s own back button)')
    changed = True

# play-loading overlay: removed 2026-07-25 at user's request (the full-screen
# black spinner + title shown on play tap). Strip it from any already-patched
# install.
if 'jf-play-loading' in html:
    html = re.sub(r'<script>\(function\(\)\{\s*/\* jf-play-loading \*/.*?\}\)\(\);</script>', '', html, flags=re.S)
    print('removed play-loading overlay (user requested removal)')
    changed = True

# media bar stylesheet: local copy, injected before anything else in <head>
if MBCSS_MARKER not in html:
    html = html.replace('<head>', '<head>' + MBCSS_LINK, 1)
    print('patched: local Media Bar stylesheet')
    changed = True

# item cache: strip any prior version, then (re)inject
if ITEMCACHE_MARKER in html:
    html = re.sub(r'<script>\(function\(\)\{ /\* sf-item-cache \*/.*?\}\)\(\);</script>', '', html, flags=re.S)
    print('removed old item cache')
# sf-cw-boot was reverted 2026-09-01 (it ran a 16ms interval through boot and
# held rows from first paint, which slowed the header and made the page look
# unfinished). jf_patch patches index.html IN PLACE, so this strip has to stay:
# without it the old block would live on in index.html forever.
html = re.sub(r'<script>\(function\(\)\{ /\* sf-cw-boot \*/.*?\}\)\(\);</script>', '', html, flags=re.S)
html = html.replace('</head>', ITEMCACHE_SCRIPT + '</head>', 1)
print('patched: short-TTL item cache')
changed = True


# bookmarks Movies/Series tab header-overlap fix: strip any prior version, then (re)inject
if BMFIX_MARKER in html:
    html = re.sub(r'<style id="jf-bm-tabs-fix">.*?</style>', '', html, flags=re.S)
    print('removed old bookmarks tab fix')
html = html.replace('</body>', BMFIX_STYLE + '</body>')
print('patched: bookmarks Movies/Series tab header-overlap fix')
changed = True

# no lazy loading: strip any prior version, then (re)inject the current one
if NOLAZY_MARKER in html:
    html = re.sub(r'<script>\(function\(\)\{\s*/\* jf-no-lazy \*/.*?\}\)\(\);</script>', '', html, flags=re.S)
    print('removed old no-lazy shim')
html = html.replace('</body>', NOLAZY_SCRIPT + '</body>')
print('patched: no lazy loading (images load eagerly, all three lazy systems)')
changed = True
# touch scroll: strip any prior version, then (re)inject the current one
if NOLAZY_TOUCHSCROLL_MARKER in html:
    html = re.sub(r'<script>\(function\(\)\{\s*/\* jf-touch-scroll \*/.*?\}\)\(\);</script>', '', html, flags=re.S)
    print('removed old touch scroll shim')
html = html.replace('</body>', TOUCHSCROLL_SCRIPT + '</body>')
print('patched: touch scroll (native row scrolling on touch, no sly spring-back)')
changed = True
if '<title>Jellyfin</title>' in html:
    html = html.replace('<title>Jellyfin</title>', '<title>' + BRAND + '</title>')
    print('patched: <title> -> ' + BRAND)
    changed = True
if '<meta name="application-name" content="Jellyfin">' in html:
    html = html.replace('<meta name="application-name" content="Jellyfin">',
                        '<meta name="application-name" content="' + BRAND + '">')
    print('patched: application-name -> ' + BRAND)
    changed = True

# item-page boot style: must be in index.html, not the branding sheet, because
# the branding sheet is injected from JS into a body DIV after first paint
if ATVBOOT_MARKER in html:
    html = re.sub(r'<style id="jf-atv-boot">.*?</style>', '', html, flags=re.S)
    print('removed old atv boot style')
html = html.replace('</head>', ATVBOOT_STYLE + '</head>')
print('patched: item page boot style (no flash of the stock layout)')
changed = True

# empty hero overlay: strip any prior version, then (re)inject
if SLIDESEMPTY_MARKER in html:
    html = re.sub(r'<style id="sf-slides-empty">.*?</style>', '', html, flags=re.S)
    print('removed old slides-empty guard')
html = html.replace('</head>', SLIDESEMPTY_STYLE + '</head>')
print('patched: empty #slides-container no longer swallows clicks')
changed = True

# header scrim: strip any prior version, then (re)inject
if HDRSCRIM_MARKER in html:
    html = re.sub(r'<style id="sf-hdr-scrim">.*?</style>', '', html, flags=re.S)
    print('removed old header scrim')
html = html.replace('</head>', HDRSCRIM_STYLE + '</head>')
print('patched: header scrim (icons no longer sit on bare artwork)')
changed = True

# paused-session clobber guard: strip any prior version, then (re)inject
if PAUSEREP_MARKER in html:
    html = re.sub(r'<script>\(function\(\)\{\s*/\* sf-pause-report \*/.*?\}\)\(\);</script>',
                  '', html, flags=re.S)
    print('removed old pause-report guard')
html = html.replace('</body>', PAUSEREP_SCRIPT + '</body>')
print('patched: a paused tab can no longer rewind your saved position')
changed = True

# volume popover: strip any prior version, then (re)inject
if VOLPOP_MARKER in html:
    html = re.sub(r'<style id="sf-vol-pop">.*?</style>', '', html, flags=re.S)
    print('removed old volume popover')
html = html.replace('</head>', VOLPOP_STYLE + '</head>')
print('patched: volume slider opens from the speaker button')
changed = True

# JellyfinEnhanced helpers shim: strip any prior version, then (re)inject
if JEHELP_MARKER in html:
    html = re.sub(r'<script id="sf-je-helpers">.*?</script>', '', html, flags=re.S)
    print('removed old JE helpers shim')
html = html.replace('</head>', JEHELP_SCRIPT + '</head>')
print('patched: JellyfinEnhanced helpers shim (features.js no longer aborts)')
changed = True

# splash mark: strip any prior version, then (re)inject the current one
if SPLASHMARK_MARKER in html:
    html = re.sub(r'<style id="jf-splash-mark">.*?</style>', '', html, flags=re.S)
    print('removed old splash mark')
# jf-splash-head (2026-09-01). The admin: "we are getting flashed the old jellyfin
# logo on page refresh with the word jellyfin". <div class="splashLogo"> is the
# FIRST element in <body> (byte ~32315) but this style was injected at </body>
# (byte ~159087) -- 127KB later in the parse -- so the splash painted with stock
# styling long before the override existed. Put it in <head> so it applies from
# the first frame; the splash can then never render un-overridden.
html = html.replace('</head>', SPLASHMARK_STYLE + '</head>', 1)
# sf-home-head: the settle/entrance rules must be in <head>; see shell.py.
html = re.sub(r'<style id="sf-home-head">.*?</style>', '', html, flags=re.S)
html = html.replace('</head>', HOMESETTLE_STYLE + '</head>', 1)
# sf-motion / sf-route-skel: both must be in <head>. The skeleton has to be
# styled on the frame it is inserted, and the motion tokens are read by rules
# that already live up here -- a runtime-injected copy would apply too late.
html = re.sub(r'<style id="sf-motion">.*?</style>', '', html, flags=re.S)
html = re.sub(r'<style id="sf-route-skel">.*?</style>', '', html, flags=re.S)
html = re.sub(r'<style id="sf-bg-hold">.*?</style>', '', html, flags=re.S)
html = re.sub(r'<style id="sf-flat-pagebg">.*?</style>', '', html, flags=re.S)
html = html.replace('</head>', MOTION_STYLE + RSKEL_STYLE + BGHOLD_STYLE + FLATBG_STYLE + '</head>', 1)

# sf-nocdn-css (2026-09-01). Media Bar injects a <link> to its slideshowpure.css
# on jsdelivr. We already serve sf-mediabar.css from <head> and it is BYTE
# IDENTICAL (both 15357 bytes, md5 37eda222ea689ecfdab1bfb76113ade8), so the CDN
# copy is a pure duplicate -- a render-blocking request to the public internet
# for a file we already have locally, measured at 1.74s on a cold fetch. It has
# been an outage source before (a blocked jsdelivr stylesheet once made the home
# rows overlap the hero). The plugin re-injects it, and jf_patch runs every 10
# minutes, so this strip re-applies itself. The local copy loads FIRST and is
# identical, so nothing changes visually.
_cdn_before = html.count('cdn.jsdelivr.net')
html = re.sub(r'<link[^>]+href="https://cdn\.jsdelivr\.net/gh/IAmParadox27/jellyfin-plugin-media-bar[^"]*"[^>]*/?>', '', html)
if html.count('cdn.jsdelivr.net') < _cdn_before:
    print('patched: sf-nocdn-css (removed Media Bar jsdelivr stylesheet)')
    changed = True

print('patched: splash mark (icon-only jellyfish, no wordmark)')
changed = True

# --- Tab icon (2026-08-02). Stock index.html ships
# <link rel="shortcut icon" href="favicon.<hash>.ico">. That .ico is a separate,
# content-hashed asset from the mark now used for the header and splash, so the
# tab could drift from the rest of the UI. Point it at the same
# favicons/touchicon512.png -- one asset for tab, splash and header, and that
# path is NOT content-hashed so it survives image updates.
# Matched by REGEX, not a literal: the .ico filename hash changes every release,
# so a fixed string would silently stop matching after an upgrade.
if 'favicons/touchicon512.png" id="jf-favicon"' not in html:
    html_new = re.sub(r'<link rel="shortcut icon" href="favicon[^"]*\.ico">',
                      '<link rel="icon" type="image/png" '
                      'href="favicons/touchicon512.png" id="jf-favicon">',
                      html, count=1)
    if html_new != html:
        html = html_new
        print('patched: tab icon -> favicons/touchicon512.png')
        changed = True

# detail action row settle: strip any prior version, then (re)inject
if BTNSETTLE_MARKER in html:
    html = re.sub(r'<script>\(function\(\)\{\s*/\* jf-btn-settle \*/.*?\}\)\(\);</script>', '', html, flags=re.S)
    print('removed old button settle')
html = html.replace('</body>', BTNSETTLE_SCRIPT + '</body>')
print('patched: detail action row reveals as one')
changed = True

# hero layout: strip any prior version, then (re)inject
if HEROLAYOUT_MARKER in html:
    html = re.sub(r'<script>\(function\(\)\{\s*/\* jf-hero-layout \*/.*?\}\)\(\);</script>', '', html, flags=re.S)
    print('removed old hero layout')
html = html.replace('</body>', HEROLAYOUT_SCRIPT + '</body>')
print('patched: hero layout (measure-based, any viewport)')
changed = True

# plugin pages dedupe: strip any prior version, then (re)inject
if PAGESDEDUPE_MARKER in html:
    html = re.sub(r'<script>\(function\(\)\{\s*/\* jf-pluginpages-dedupe \*/.*?\}\)\(\);</script>', '', html, flags=re.S)
    print('removed old plugin-pages dedupe')
html = html.replace('</body>', PAGESDEDUPE_SCRIPT + '</body>')
print('patched: plugin pages dedupe (1 request instead of ~8)')
changed = True

# bookmark item-id shim: strip any prior version, then (re)inject
if BMITEMID_MARKER in html:
    html = re.sub(r'<script>\(function\(\)\{\s*/\* jf-bookmark-itemid \*/.*?\}\)\(\);</script>', '', html, flags=re.S)
    print('removed old bookmark item-id shim')
html = html.replace('</body>', BMITEMID_SCRIPT + '</body>')
print('patched: bookmark item-id shim')
changed = True


# rename home Favorites pill -> My Stuff: strip any prior version, then (re)inject
if MYSTUFF_MARKER in html:
    html = re.sub(r'<script>\(function\(\)\{ /\* jf-mystuff-tab \*/.*?\}\)\(\);</script>', '', html, flags=re.S)
    print('removed old My Stuff rename')
html = html.replace('</body>', MYSTUFF_SCRIPT + '</body>')
print('patched: home Favorites pill -> My Stuff')
changed = True


# hide the chapters/scenes row: strip any prior version, then (re)inject
if HOLDROWS_MARKER in html:
    html = re.sub(r'<style id="sf-holdrows">.*?</style>', '', html, flags=re.S)
    print('removed old home row hold css')
html = html.replace('</body>', HOLDROWS_STYLE + '</body>')
print('patched: home rows reveal together (no first-row displacement)')
changed = True

if ABCUT_MARKER in html:
    html = re.sub(r'<style id="sf-ab-cut">.*?</style>', '', html, flags=re.S)
    print('removed old audiobook control css')
html = html.replace('</body>', ABCUT_STYLE + '</body>')
print('patched: audiobook control hierarchy (+ heart/cast hidden on books)')
changed = True

# avatar picker: strip any prior version, then (re)inject
if AVPICKER_MARKER in html:
    html = re.sub(r'<style id="sf-avatar-picker-css">.*?</style>', '', html, flags=re.S)
    html = re.sub(r'<script>\(function\(\)\{\s*/\* sf-avatar-picker \*/.*?\}\)\(\);</script>', '', html, flags=re.S)
    print('removed old avatar picker')
html = html.replace('</body>', AVPICKER_STYLE + AVPICKER_SCRIPT + '</body>')
print('patched: avatar picker')
changed = True

# mobile now-playing bar: strip any prior version, then (re)inject
if MOBILEPLAYER_MARKER in html:
    html = re.sub(r'<style id="jf-mobile-player">.*?</style>', '', html, flags=re.S)
    print('removed old mobile player css')
html = html.replace('</body>', MOBILEPLAYER_STYLE + '</body>')
print('patched: mobile now-playing bar (110px -> 84px, play/pause restored)')
changed = True

# music playlists filter: strip any prior version, then (re)inject
if NOCOLLAPSE_MARKER in html:
    html = re.sub(r'<script>\(function\(\)\{ /\* jf-no-collapse \*/.*?\}\)\(\);</script>', '', html, flags=re.S)
    print('removed old no-collapse shim')
html = html.replace('</body>', NOCOLLAPSE_SCRIPT + '</body>')

if MUSICPL_MARKER in html:
    html = re.sub(r'<script>\(function\(\)\{\s*/\* jf-music-playlists \*/.*?\}\)\(\);</script>', '', html, flags=re.S)
    print('removed old music playlists filter')
html = html.replace('</body>', MUSICPL_SCRIPT + '</body>')
print('patched: Music > Playlists filtered to audio')
changed = True

# music tab trim: strip any prior version, then (re)inject
if MUSICTABS_MARKER in html:
    html = re.sub(r'<style id="jf-music-tabs">.*?</style>', '', html, flags=re.S)
    print('removed old music tab trim')
html = html.replace('</body>', MUSICTABS_STYLE + '</body>')
print('patched: music tab trim (Artists, Genres hidden)')
changed = True

# music artist tab label: strip any prior version, then (re)inject
if MUSICARTISTLBL_MARKER in html:
    html = re.sub(r'<script>\(function\(\)\{\s*/\* jf-music-artist-label \*/.*?\}\)\(\);</script>', '', html, flags=re.S)
    print('removed old music artist label')
html = html.replace('</body>', MUSICARTISTLBL_SCRIPT + '</body>')
print('patched: Album artists -> Artists')
changed = True

if ABSTAGE_MARKER in html:
    html = re.sub(r'<style id="sf-ab-stage-css">.*?</style>', '', html, flags=re.S)
    print('removed old audiobook stage css')
html = html.replace('</body>', ABSTAGE_STYLE + '</body>')
print('patched: full-screen audiobook player')
changed = True

if SHELF_MARKER in html:
    html = re.sub(r'<style id="sf-music-shelves">.*?</style>', '', html, flags=re.S)
    print('removed old music shelf css')
html = html.replace('</body>', SHELF_STYLE + '</body>')
print('patched: music suggestion shelves scroll instead of wrapping')
changed = True

if TAPFEEL_MARKER in html:
    html = re.sub(r'<style id="sf-tap-feel">.*?</style>', '', html, flags=re.S)
    print('removed old tap feel')
html = html.replace('</body>', TAPFEEL_STYLE + '</body>')
print('patched: touch feedback matches the theme')
changed = True

if DISCBADGE_MARKER in html:
    html = re.sub(r'<style id="sf-disc-badge-i18n">.*?</style>', '', html, flags=re.S)
    print('removed old discover badge i18n')
html = html.replace('</body>', DISCBADGE_STYLE + '</body>')
print('patched: discover MOVIE/SERIES badges translated')
changed = True

# Hero artwork sizing. Must be in <head>: it has to be installed before Media
# Bar's first preload, which happens well before any tick of ours could run.
if SRCCAP_MARKER in html:
    html = re.sub(r'<script>\(function\(\)\{\s*/\* sf-hero-srccap \*/.*?\}\)\(\);</script>',
                  '', html, flags=re.S)
    print('removed old hero src cap')
html = html.replace('</head>', SRCCAP_SCRIPT + '</head>')

if COALESCE_MARKER in html:
    html = re.sub(r'<script>\(function\(\)\{\s*/\* sf-coalesce \*/.*?\}\)\(\);</script>', '', html, flags=re.S)
# must run BEFORE Jellyfin's bundle so its ApiClient picks up the wrapper
html = html.replace('</head>', COALESCE_SCRIPT + '</head>')
# --- sf-fresh (2026-08-21) ---------------------------------------------------
# The single biggest source of "you said you fixed it and it is still broken"
# this whole session. The SPA fetches index.html ONLY at launch, so an app left
# open runs whatever JavaScript it started with -- and this session deployed
# dozens of times. Every round the admin tested a fix he had not been served.
#
# So the page learns to notice. A build stamp is written into the first bytes of
# <head>; a check fetches ONLY those bytes (a 2KB range request, not the 735KB
# document) and compares. When they differ the app refreshes ITSELF -- but only
# when that is safe:
#   * nothing is playing (never interrupt a book or a film),
#   * the tab is actually visible,
#   * no dialog, action sheet or drawer is open,
#   * and not within 60s of launch, so a reload can never become a loop.
# If it is not safe, a quiet pill offers the refresh instead of taking it.
# sf-fresh-contenthash (2026-08-29): SF_BUILD used to be int(time.time()), so
# EVERY run of this patcher produced a new stamp even when the output was
# byte-for-byte identical -- and sf-fresh reloads the app whenever the stamp it
# fetches differs from the one it booted with. Seven deploys in an afternoon
# therefore reloaded every open tab seven times, on focus, which is what the admin
# reported ("everytime i come back to the jellyfin page it reloads").
# The stamp is now a HASH OF THE OUTPUT, substituted just before the file is
# written: rebuilding unchanged content keeps the same stamp and nobody
# reloads; a real change still refreshes everyone exactly once.
# Kept DECIMAL on purpose -- the client matches /__SF_BUILD="(\d+)"/, so a hex
# digest would fail to parse in tabs still running the OLD script and they
# would silently never auto-refresh again.
import hashlib as _h

if FRESH_MARKER in html:
    html = re.sub(r'<script>window\.__SF_BUILD="\d+";</script>', '', html)
    html = re.sub(r'<script>\(function\(\)\{\s*/\* sf-fresh \*/.*?\}\)\(\);</script>', '', html, flags=re.S)
# the stamp goes in the FIRST bytes, so the check can read a 2KB range
html = html.replace('<head>', '<head>' + FRESH_SCRIPT, 1)
html = html.replace('</body>', FRESH_CHECK + '</body>')
if 'sf-swipe-guard' not in html:
    html = html.replace('</body>', SWIPEGUARD_SCRIPT + '</body>')

if ABCARD_MARKER in html:
    html = re.sub(r'<script>\(function\(\)\{\s*/\* sf-abcard \*/.*?\}\)\(\);</script>', '', html, flags=re.S)
html = html.replace('</body>', ABCARD_SCRIPT + '</body>')

if ALBUMBLURB_MARKER in html:
    html = re.sub(r'<script>\(function\(\)\{\s*/\* sf-alb-stage \*/.*?\}\)\(\);</script>', '', html, flags=re.S)
# retire the previous, narrower block so it cannot linger in an already-patched page
html = re.sub(r'<script>\(function\(\)\{\s*/\* sf-albumblurb \*/.*?\}\)\(\);</script>', '', html, flags=re.S)
html = html.replace('</body>', ALBUMBLURB_SCRIPT + '</body>')
for _marker in RETIRED:
    html = re.sub(r'<script>\(function\(\)\{\s*/\* ' + re.escape(_marker) + r' \*/.*?\}\)\(\);</script>',
                  '', html, flags=re.S)






print('patched: hero artwork src cap (preloads included)')
changed = True


# sf-pill-dedupe was REVERTED: it broke the Live TV header for everyone
# (visible tabs collapsed to just 'Home') while chasing a doubled pill bar
# only one client ever showed. Strip it from any index.html that still has
# it, and never inject it again.
if 'sf-pill-dedupe' in html:
    html = re.sub(r'<script>\(function\(\)\{\s*/\* sf-pill-dedupe \*/.*?\}\)\(\);</script>',
                  '', html, flags=re.S)
    print('removed sf-pill-dedupe (reverted)')
    changed = True

if DIAG_MARKER in html:
    html = re.sub(r'<script>\(function\(\)\{\s*/\* sf-diag-report \*/.*?\}\)\(\);</script>',
                  '', html, flags=re.S)
html = html.replace('</head>', DIAG_SCRIPT + '</head>')
print('patched: sf-diag-report (inert unless ?sfdiag=1)')
changed = True

if HDRSOLID_MARKER in html:
    html = re.sub(r'<script>\(function\(\)\{\s*/\* sf-hdr-solid \*/.*?\}\)\(\);</script>',
                  '', html, flags=re.S)
    print('removed old header-solid toggle')
# sf-hdr-solid is DELIBERATELY no longer injected. It faded a dark background
# into the header once the page scrolled past 60px, so the header visibly
# darkened on the way down -- the admin asked for that removed. The stripping block
# above is kept on purpose: it removes the script from an already-patched
# index.html, so existing installs lose the behaviour on the next run.
# (The .sf-hdr-solid CSS can stay: with the class never applied it does nothing.)
print('header solid-on-scroll toggle: intentionally NOT applied')
changed = True


# visible-view resolver: strip any prior version, then (re)inject. Goes in
# <head> so it is defined before the body patches that call it.
if VIEWSCOPE_MARKER in html:
    html = re.sub(r'<script>\(function\(\)\{\s*/\* jf-view-scope \*/.*?\}\)\(\);</script>',
                  '', html, flags=re.S)
    print('removed old view-scope resolver')
html = html.replace('</head>', VIEWSCOPE_SCRIPT + '</head>')
print('patched: visible-view resolver (window.__jfView)')
changed = True


# pane guard: strip any prior version, then (re)inject
if PANEGUARD_MARKER in html:
    html = re.sub(r'<script>\(function\(\)\{\s*/\* jf-pane-guard \*/.*?\}\)\(\);</script>',
                  '', html, flags=re.S)
    print('removed old pane guard')
html = html.replace('</body>', PANEGUARD_SCRIPT + '</body>')
print('patched: pane guard (recovers a page with no active pane)')
changed = True


# card menu close: strip any prior version, then (re)inject
if SHEETCLOSE_MARKER in html:
    html = re.sub(r'<script>\(function\(\)\{\s*/\* sf-sheet-close \*/.*?\}\)\(\);</script>',
                  '', html, flags=re.S)
    print('removed old sheet-close')
html = html.replace('</body>', SHEETCLOSE_SCRIPT + '</body>')
print('patched: card menu closes after Remove')
changed = True


# audiobook lock-screen controls: must load AFTER the player block, because it
# reads window.__sfAbApi which that block publishes.
if MEDIASESSION_MARKER in html:
    html = re.sub(r'<script>\(function\(\)\{/\* sf-ab-mediasession \*/.*?\}\)\(\);</script>', '', html, flags=re.S)
    print('removed old audiobook mediaSession block')
html = html.replace('</body>', MEDIASESSION_SCRIPT + '</body>')
print('patched: audiobook lock-screen controls (position state + 30s seek)')

print('patched: audiobook player controls')
changed = True


# hero edge clicks: strip any prior version, then (re)inject
if HEROEDGE_MARKER in html:
    html = re.sub(r'<style id="sf-hero-edge">.*?/\* sf-hero-edge \*/.*?\}\)\(\);</script>',
                  '', html, flags=re.S)
    print('removed old hero edge')
html = html.replace('</body>', HEROEDGE_SCRIPT + '</body>')
print('patched: hero edge clicks (chevrons hidden, outer thirds scroll)')
changed = True


# above-the-fold priority: strip any prior version, then (re)inject
if FASTFOLD_MARKER in html:
    html = re.sub(r'<script>\(function\(\)\{\s*/\* sf-fastfold \*/.*?\}\)\(\);</script>',
                  '', html, flags=re.S)
    print('removed old fastfold')
html = html.replace('</body>', FASTFOLD_SCRIPT + '</body>')
print('patched: above-the-fold priority (persist bitrate, hold below-fold queries)')
changed = True


# drawer tidy: strip any prior version, then (re)inject
if DRAWERTIDY_MARKER in html:
    html = re.sub(r'<style id="sf-drawer-tidy">.*?/\* sf-drawer-tidy \*/.*?\}\)\(\);</script>',
                  '', html, flags=re.S)
    print('removed old drawer tidy')
html = html.replace('</body>', DRAWERTIDY_SCRIPT + '</body>')
print('patched: drawer tidy (drop unused entries, move Enhanced below Media)')
changed = True


# header user rail: strip any prior version, then (re)inject
if USERRAIL_MARKER in html:
    html = re.sub(r'<style id="sf-user-rail">.*?/\* sf-user-rail \*/.*?\}\)\(\);</script>',
                  '', html, flags=re.S)
    print('removed old user rail')
html = html.replace('</body>', USERRAIL_SCRIPT + '</body>')
print('patched: header user rail (collapse right-hand controls into the avatar)')
changed = True


# sf-nocount: strip the redundant TotalRecordCount COUNT from the two calls that
# gate the first paint (Shows/NextUp, Items/Resume). Injected last so its fetch
# wrapper sits outermost.
if NOCOUNT_MARKER in html:
    html = re.sub(r'<script>\(function\(\)\{\s*/\* sf-nocount \*/.*?\}\)\(\);</script>', '', html, flags=re.S)
    print('removed old nocount')
html = html.replace('</body>', NOCOUNT_SCRIPT + '</body>')
print('patched: sf-nocount (drop TotalRecordCount on NextUp/Resume)')
changed = True


# sf-mobcard: phone card controls -- drop the play disc, collapse the duplicate
# corner menu, and restyle the survivor with the Abyss glass tokens.
if MOBCARD_MARKER in html:
    html = re.sub(r'<script>\(function\(\)\{\s*/\* sf-mobcard \*/.*?\}\)\(\);</script>', '', html, flags=re.S)
    print('removed old mobcard')
html = html.replace('</body>', MOBCARD_SCRIPT + '</body>')
print('patched: sf-mobcard (phone card controls, Abyss-themed)')
changed = True


if changed:
    _tag = 'window.__SF_BUILD="' + SF_BUILD + '"'
    if _tag in html:
        _stamp = str(int(_h.sha1(html.encode('utf-8')).hexdigest()[:12], 16))
        html = html.replace(_tag, 'window.__SF_BUILD="' + _stamp + '"', 1)
        print('build stamp (content hash): ' + _stamp)
    with open(PATH, 'w') as f:
        f.write(html)
    print(f'wrote {len(html)} bytes')
else:
    print('nothing to do')

