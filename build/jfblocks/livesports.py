"""jfblocks/livesports.py -- payload constants lifted out of jf_patch.py.

Each constant's source text (and its comments) is byte-identical to the
monolith; only its location changed. 18 constants.
"""

__all__ = [
    'LIVESPORTS_MARKER',
    '_LS_01',
    '_LS_02',
    '_LS_03',
    '_LS_04',
    '_LS_05',
    '_LS_06',
    '_LS_07',
    '_LS_08',
    '_LS_09',
    '_LS_10',
    '_LS_11',
    '_LS_12',
    '_LS_13',
    '_LS_14',
    '_LS_15',
    '_LS_16',
    'LIVESPORTS_SCRIPT',
]


LIVESPORTS_MARKER = 'sf-livesports'
# ============================================================================
# sf-livesports -- ONE shared closure, deliberately.
#
# 11,591 lines in a single <script> because these features SHARE a runtime:
# 138 top-level functions and 47 vars are referenced across the whole block
# (sfNorm 44x, sfBeat 43x, sfCwMap 21x, sfPlayItemViaProxy 18x). Splitting it
# into separate <script> tags would give each its own scope and every one of
# those references would break at runtime.
#
# So the SOURCE is sliced for navigability and the slices are concatenated
# back into the identical original tag. These are NOT independent modules --
# they are contiguous slices of one closure, and a slice may begin mid-
# function. Do not reorder them. Verified byte-identical against a known-good
# build (see refactor/ harness: same input -> same md5).
#
# PART     START    LINES  FEATURES
#   _LS_01  L0       712    sf-livesports, jf-abyss-matched, sf-ls-jfoverlay, sf-ls-inplace, sf-ltv-nofiller
#   _LS_02  L712     704    sf-cwbook-art, sf-heroslot, sf-mus-heroh, sf-hero-oneshot, sf-mus-nobox
#   _LS_03  L1416    760    sf-ls-inplace, sf-ls-routesync, sf-ls-routesync2, sf-ltv-nofiller, sf-ltv-nofiller-all
#   _LS_04  L2176    713    sf-cwrm-reset, sf-cwrm-unplayed, sf-hidden-uid, sf-cw-rewatch, sf-music-pad
#   _LS_05  L2889    740    sf-ltv-backout, sf-ltv-pane-dest, sf-ltv-realurl, sf-ltv-alias, sf-tab-fouc
#   _LS_06  L3629    739    sf-hero-nextup, sf-hero-parallel, sf-cw-order, sf-hero-cap, sf-hero-parallel-resume
#   _LS_07  L4368    707    sf-music-tabs, sf-music-home, sf-music-row, sf-livetv-row, sf-audiobook-row
#   _LS_08  L5075    714    sf-play-confirm, sf-abgo, sf-ablib-nopeople, sf-prewarm-defer, sf-resume-pos
#   _LS_09  L5789    747    sf-mus-playlists, sf-mus-reveal, sf-hero-first, sf-hero-oneshot, sf-mus-pagebg
#   _LS_10  L6536    717    sf-music-ambient, sf-hero-oneshot, sf-mus-dedupe, sf-hide-internal-playlists, sf-nav-tuck
#   _LS_11  L7253    638    sf-np-flicker, sf-np-typeflash, sf-mixes, sf-mood-mixes, sf-tap-lost
#   _LS_12  L7891    805    sf-mood-mixes, sf-hero-epid2, sf-hero-nojitter, sf-hero-mobile, sf-hero-runtime
#   _LS_13  L8696    726    sf-info-panel, sf-episode-line, sf-dfacts, sf-dfacts-epdupe, sf-sub-lift-measured
#   _LS_14  L9422    720    sf-abrow-head, sf-hero-play, sf-drawer-scroll, sf-drawer-tapguard, sf-hero-resume-pos
#   _LS_15  L10142   762    sf-sports-exit, sf-pill-show, sf-home-bar-unify, sf-pill-dedupe, sf-ltv-subdupe
#   _LS_16  L10904   687    sf-one-spinner, sf-skel-max2, sf-dskel-scope, sf-dskel-exit, sf-dskel-atv
# ============================================================================

# _LS_01 (orig L0-712) -- sf-livesports, jf-abyss-matched, sf-ls-jfoverlay
_LS_01 = r'''<script>(function(){
/* sf-livesports */
/* jf-abyss-matched: every value below was measured off the live Abyss theme
   rather than eyeballed --
     page bg      rgb(16,16,16)          (html)
     card radius  12px                   (.cardImageContainer)
     section head rgba(255,255,255,.8) 22.32px w600
     card title   rgba(255,255,255,.8) 17.86px w600
     card sub     rgba(255,255,255,.5) 16px    w200
     tab capsule  rgba(42,42,42,.69) r50px, active #f5f5f7 on #121212 */
var css='.sf-livesports-root{display:none;position:fixed;left:0;right:0;bottom:0;background:#101010;z-index:40;overflow-y:auto;padding:1.5em 2em 3em;box-sizing:border-box;}'
+'.sf-livesports-root.sf-ls-show{display:block;}'
/* The pill bar lives inside the scrolling overlay, so it used to scroll away
   while the main tabs (in the fixed .skinHeader) stayed put - the two tab rows
   behaved differently, most obvious on mobile.
   top:0 is correct and deliberate. The sticky offset here resolves against the
   root's CONTENT edge, and the root already carries padding-top = headerBottom
   + 14 (92px). Setting top to that same value double-counted it and pinned the
   bar at 184px instead of 92px - measured. */
/* No full-width band: it read as a heavy horizontal bar across the page.
   The wrapper stays sticky but is invisible; the capsule itself carries the
   background and a blur so it stays legible floating over scrolling cards,
   matching how the main tab bar and the My Stuff sub-pills look. */
+'.sf-ls-pillwrap{position:sticky;top:0;z-index:3;margin:0 0 1.4em;padding:0;pointer-events:none;}'
+'.sf-ls-pillwrap > *{pointer-events:auto;}'
+'.sf-ls-pills{display:flex;justify-content:center;align-items:center;gap:2px;margin:0 auto;padding:5px 2.5px;width:max-content;max-width:100%;background:rgba(34,34,34,.92);-webkit-backdrop-filter:blur(14px);backdrop-filter:blur(14px);border-radius:50px;flex-wrap:wrap;box-sizing:border-box;}'
+'.sf-ls-pill{background:transparent;color:#999;border:none;border-radius:50px;padding:.42em 1.4em;font-size:.95em;font-weight:600;cursor:pointer;white-space:nowrap;font-family:inherit;line-height:1.45;transition:background .15s ease,color .15s ease;}'
+'.sf-ls-pill:hover{background:rgba(255,255,255,.07);color:#e8e8e8;}'
+'.sf-ls-pill-active,.sf-ls-pill-active:hover{background:#f5f5f7;color:#121212;}'
+'.sf-ls-section{margin-bottom:2.2em;}'
+'.sf-ls-sectionhead{color:rgba(255,255,255,.8);font-size:1.4em;font-weight:600;margin-bottom:.5em;letter-spacing:normal;}'
+'.sf-ls-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:1em;}'
+'.sf-ls-card{position:relative;aspect-ratio:16/9;border-radius:12px;overflow:hidden;background-color:#1c1c1c;background-size:cover;background-position:center;cursor:pointer;transition:transform .15s ease;}'
+'.sf-ls-card:hover{transform:none;}'
+'.sf-ls-card::after{content:"";position:absolute;left:0;right:0;bottom:0;height:65%;background:linear-gradient(to top, rgba(0,0,0,.88), rgba(0,0,0,0));pointer-events:none;}'
+'.sf-ls-badge{position:absolute;top:.6em;left:.6em;z-index:2;padding:.15em .6em;border-radius:5px;font-size:.7em;font-weight:800;letter-spacing:.03em;}'
+'.sf-ls-live{background:#e0263f;color:#fff;}'
+'.sf-ls-upcoming-badge{background:rgba(255,255,255,.15);color:#eee;}'
+'.sf-ls-cardinfo{position:absolute;left:.7em;right:.7em;bottom:.6em;z-index:2;}'
/* sf-ls-jfoverlay: reuse Jellyfin's real card overlay so Sports hover is the
   SAME element as Live TV, not a copy that can drift. Only stacking is ours:
   .sf-ls-card::after (the gradient) is generated last and would paint over
   the overlay, and the overlay must not intercept the card's click. */
+'.sf-ls-card .cardOverlayContainer{z-index:3;pointer-events:none;}'
/* sf-ls-inplace: live tune-in measured at 20-35s to first frame. Without
   feedback the card just sits there and reads as broken, so cover it while
   we wait and hide the hover play button (it already did its job). */
+'.sf-ls-card.sf-ls-tuning .cardOverlayContainer{display:none;}'
+'.sf-ls-tuningwrap{position:absolute;top:0;left:0;right:0;bottom:0;z-index:4;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:.55em;background:rgba(0,0,0,.72);}'
+'.sf-ls-spin{width:1.9em;height:1.9em;border-radius:50%;border:2px solid rgba(255,255,255,.25);border-top-color:#fff;animation:sf-ls-spin .9s linear infinite;}'
+'@keyframes sf-ls-spin{to{transform:rotate(360deg);}}'
+'.sf-ls-tuninglabel{font-size:.78em;color:#fff;opacity:.92;}'
/* sf-ltv-nofiller: placeholder lane cards inside Live TV's On Now row. */
+'.sf-ltv-filler{display:none!important;}'
/* sf-search-order2: owned results first, then movies/TV to add, then music
   to add. Done with flex order, NOT by moving nodes -- apply() runs off a
   MutationObserver, so an appendChild-based reorder retriggers itself and
   froze the renderer once already. order paints without mutating. */
+'#searchPage{display:flex;flex-direction:column;}'
+'#searchPage>.searchFields{order:-4;}'
/* sf-rank-nesting: EVERY '#searchPage>' order rule below this comment used to
   be a no-op. Jellyfin does not put its sections in #searchPage -- it puts
   them in a '.searchResults' wrapper, so the child combinator matched nothing
   and Movies/People/Artists/Jellyseerr all kept the initial order:0, leaving
   DOM order (i.e. whichever fetch answered first) to decide the page. Measured
   on two consecutive loads of the same query: once
   'searchFields > sf-lib-albums > sfrq-sec > searchResults' and once
   'searchFields > searchResults > sfrq-sec'. Same query, different page.
   Fix has two halves: make '.searchResults' a flex column too so it is a real
   ordering context, and rank by a data attribute set in JS (sf-search-rank),
   matched with a DESCENDANT selector so one rule covers a section whether it
   lands inside .searchResults or directly on the page. */
+'#searchPage>.searchResults{display:flex;flex-direction:column;order:0;}'
/* sf-row-rhythm: one spacing rule for every row instead of per-section
   margins. Jellyfin's own sections carry margin 0 and sit flush -- their
   breathing room is internal -- while the two custom rows each brought their
   own margins (7.44/14.88 on the album row, 30 top on the request row), so the
   gaps down the page measured 0, 7, 15 and 104px. Zero the custom margins and
   let the flex container own the spacing, so every gap is the same number by
   construction and adding a future row cannot reintroduce the problem. Kept at
   0 to match Jellyfin's existing rhythm exactly rather than restyle its
   sections. */
+'#searchPage>.searchResults{row-gap:0;}'
/* sf-static-order: our own two rows also get their rank statically, not only
   from the script. They are the only sections whose class already tells us
   what they are, and a section is inserted UNRANKED -- so for the one frame
   before apply() runs it sits at the initial order:0 and paints at the very
   top. Recorded as a 40ms flash of the request row above everything. These two
   rules agree with what the script would set, so nothing fights; they just
   remove the dependency on JS timing for the two rows we control. */
+'#searchPage .sf-lib-albums{margin:0;order:30;}'
+'#searchPage .sfrq-sec{margin:0;order:60;}'
/* the Jellyseerr row ships its own bottom margin, which showed up as the one
   15px gap in a column of 0s. */
+'#searchPage .jellyseerr-section{margin:0;}'
/* The scale, widely spaced so a rank can be inserted later without a reflow of
   every rule: 10 movies & TV | 20 people | 30 music you own | 40 artists
   | 50 Jellyseerr | 60 music to request. 15 is the fallback for any section
   this build does not name explicitly -- it keeps an unknown LIBRARY section
   with the rest of what you own rather than exiling it below the requests. */
/* sf-exact-first uses 8 and 9 for a video section holding an exact / prefix
   title match; everything else keeps the band it was given. */
+'#searchPage [data-sfrank="8"]{order:8;}'
+'#searchPage [data-sfrank="9"]{order:9;}'
+'#searchPage [data-sfrank="10"]{order:10;}'
+'#searchPage [data-sfrank="15"]{order:15;}'
+'#searchPage [data-sfrank="20"]{order:20;}'
+'#searchPage [data-sfrank="30"]{order:30;}'
+'#searchPage [data-sfrank="40"]{order:40;}'
+'#searchPage [data-sfrank="45"]{order:45;}'
+'#searchPage [data-sfrank="50"]{order:50;}'
+'#searchPage [data-sfrank="60"]{order:60;}'
/* sf-player-polish2: rows measured 68px even after the padding change --
   the thumbnail sets the height, not padding. Size that instead. */
+'.nowPlayingPage .listItem .listItemImage{width:46px!important;height:46px!important;background-size:cover;border-radius:4px;}'
+'.nowPlayingPage .listItem{min-height:0!important;}'
/* art was 215px tucked in a corner; give the current track presence. */
+'@media (min-width:700px){.nowPlayingPage .nowPlayingPageImage{width:280px!important;height:280px!important;}}'
/* sf-queue-fix: THE BROKEN QUEUE PAGE. The rule directly above grew the IMAGE
   to 280px but not the .nowPlayingPageImageContainer that holds it, which
   Jellyfin sizes to 215px. The container is a flex item, so the row after it
   still began at 215px while the artwork ran on to 280 -- measured art
   48->328, info column starting at 274, a 54px overlap. That is why the track
   title, the album, the artist AND the elapsed time were all painted
   underneath the cover art. Size the container, not just the picture. */
+'@media (min-width:700px){.nowPlayingPage .nowPlayingPageImageContainer{width:280px!important;flex:0 0 280px;margin-right:28px;}}'
/* sf-queue-polish: the header now reads like a player instead of a form.
   Measured before: the title box was pinned to 232px inside a 1119px column,
   so "State of Grace (Taylor's version)" truncated mid-word with 887px of
   empty space beside it. */
+'.nowPlayingPage .nowPlayingPageImage{border-radius:10px;box-shadow:0 10px 34px rgba(0,0,0,.5);}'
+'.nowPlayingPage .nowPlayingInfoContainerMedia{width:auto!important;flex:1 1 auto;min-width:0;}'
+'.nowPlayingPage .nowPlayingSongName{font-size:1.85em;font-weight:700;line-height:1.25;margin-bottom:.12em;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;}'
+'.nowPlayingPage .nowPlayingAlbum,.nowPlayingPage .nowPlayingArtist{white-space:nowrap;overflow:hidden;text-overflow:ellipsis;}'
+'.nowPlayingPage .nowPlayingArtist .emby-button{font-size:1.05em;color:rgba(255,255,255,.78);}'
+'.nowPlayingPage .nowPlayingAlbum .emby-button{color:rgba(255,255,255,.5);}'
/* the two times sat hard against the bar; tabular figures stop the elapsed
   time shivering as the digits change. */
+'.nowPlayingPage .positionTime,.nowPlayingPage .runtime{font-variant-numeric:tabular-nums;color:rgba(255,255,255,.6);font-size:.85em;}'
+'.nowPlayingPage .sliderContainer{gap:.85em;}'
/* sf-queue-list: Spotify/Apple show a titled queue with no rules between rows
   and the playing track called out. Jellyfin drew a divider under every row
   and left the current one indistinguishable from the rest. */
+'.nowPlayingPage .playlistSectionButton{margin-top:.4em;}'
+'.nowPlayingPage .nowPlayingPlaylist{margin-top:.2em;}'
+'.nowPlayingPage .nowPlayingPlaylist::before{content:"Up Next";display:block;font-size:1.15em;font-weight:600;color:rgba(255,255,255,.85);margin:0 0 .5em;}'
+'.nowPlayingPage .nowPlayingPlaylist .listItem{border:0!important;border-radius:8px;}'
+'.nowPlayingPage .nowPlayingPlaylist .listItem:hover{background:rgba(255,255,255,.06);}'
/* the playing row is the one carrying the equaliser thumbnail. Accent is the
   theme's own --abyss-accent (245,245,247), not a colour of our choosing. */
+'.nowPlayingPage .nowPlayingPlaylist .listItem:has(.playlistIndexIndicatorImage){background:rgba(255,255,255,.09);}'
+'.nowPlayingPage .nowPlayingPlaylist .listItem:has(.playlistIndexIndicatorImage) .listItemBodyText{color:rgb(245,245,247);font-weight:600;}'
/* drag handles on all 30 rows read as clutter. Kept operable -- opacity, never
   display:none, or the row stops being draggable. */
+'.nowPlayingPage .listViewDragHandle{opacity:0;transition:opacity .12s ease;}'
+'.nowPlayingPage .listItem:hover .listViewDragHandle,.nowPlayingPage .listItem:focus-within .listViewDragHandle{opacity:.5;}'
+'@media (hover:none){.nowPlayingPage .listViewDragHandle{opacity:.5;}}'
+'.nowPlayingPage .listItem .listItemMediaInfo{font-variant-numeric:tabular-nums;color:rgba(255,255,255,.5);}'
/* sf-queue-backdrop: with the overlap gone the real legibility problem showed
   up -- Jellyfin paints the artist backdrop full-bleed at opacity 1 with no
   filter, so the queue was white text over a lit photograph of a performer and
   the track rows were barely readable. Spotify and Apple both keep the artwork
   as AMBIENCE: heavily blurred and darkened so it reads as a colour wash. The
   scale hides the soft edges blur leaves at the viewport bounds, and the
   gradient guarantees contrast at the bottom where the queue rows are, whatever
   the image happens to be.
   Scoped with :has() because .backdropContainer is a FIXED element outside the
   page, so no descendant selector from .nowPlayingPage can reach it -- and
   scoped at all so backdrops everywhere else keep Jellyfin's own look. */
+'body:has(.nowPlayingPage:not(.hide)) .backdropImage{filter:blur(34px) saturate(1.25) brightness(.42);transform:scale(1.15);}'
+'body:has(.nowPlayingPage:not(.hide)) .backdropContainer::after{content:"";position:absolute;inset:0;background:linear-gradient(180deg,rgba(0,0,0,.45),rgba(0,0,0,.82));}'
/* sf-player-polish: music has no Stop -- that is a video control; pause is
   the music verb (Spotify/Apple both omit it). */
+'.nowPlayingPage .btnStop{display:none!important;}'
/* the Save/More row floated detached on the right; sit it with the queue it
   heads instead. */
+'.nowPlayingPage .playlistSectionButton{justify-content:flex-start!important;}'
/* 68px rows with four controls each read as a toolbar per line. Spotify runs
   ~56px and reveals actions on hover. */
+'.nowPlayingPage .listItem{padding-top:.25em!important;padding-bottom:.25em!important;}'
+'.nowPlayingPage .listItem .listItemButton{opacity:0;transition:opacity .12s ease;}'
+'.nowPlayingPage .listItem:hover .listItemButton,.nowPlayingPage .listItem:focus-within .listItemButton{opacity:1;}'
/* a phone has no hover: keep them visible there. */
+'@media (hover:none){.nowPlayingPage .listItem .listItemButton{opacity:1;}}'
/* sf-pill-fit: at 390px the four nav pills measured 402px inside a 369px
   track, clipping "My Stuff" by 28px. 157px of that was padding, so tighten
   padding rather than shrink the labels. Same for the Music main bar. */
+'@media (max-width:430px){'
+'.emby-tabs-slider .emby-tab-button{padding-left:.8em!important;padding-right:.8em!important;}'
+'}'
/* sf-music-nav: main pills above the library tab bar; the library's own tabs
   are restyled as secondary pills so the hierarchy reads main -> sub. */
/* sf-nav-uniform (2026-08-09): the bar used to carry a hand-copied version of
   Jellyfin's pill styling -- its own background, radius, padding:3.5px and a
   fixed 37px button height. Copied numbers drift, and these had: measured side
   by side against the real main bar on Live TV, ours came out 44px tall
   starting at y=34 where the native one is 49px starting at y=29, and the gap
   below it was 4px against Live TV's 10px. The bar now wears Jellyfin's OWN
   .emby-tabs-slider / .emby-tab-button classes (see sfMainNav), so background,
   radius, padding, font and height all come from the theme and cannot drift
   again. Only layout is ours: centred, and a 10px gap to the sub bar to match
   the Live TV / My Stuff rhythm exactly. */
/* sf-nav-gap-only-with-sub (2026-09-05). This 10px is the gap between our pill bar
   and the library tab strip UNDER it, and it was unconditional -- so it also
   applied on routes that have no strip. With the pills now on detail pages that
   made them 87px against Home's 77px: the same pills, ten pixels apart, for a gap
   to a row that is not there.
   sfMainNav already publishes exactly this condition -- it toggles html.sf-music-nav
   when a library strip exists -- so key the gap off that. Home and every detail
   page land on one height; library routes stay taller because they genuinely carry
   a second row. */
+'/* sf-music-track */.jf-mu-mainbar{margin:0;}'
+'html.sf-music-nav .jf-mu-mainbar{margin-bottom:10px;}'
/* sf-nav-hug: the capsule must be exactly as wide as its pills. Our wrapper is
   a flex item in .headerTabs and gets sized against the library strip beside
   it, so the slider inside -- display:block -- stretched to that width instead
   of its own content: measured 478.86px against the real bar's 443.59px. The
   slider is text-align:center, so the surplus split evenly and showed up as
   dead space at the two ENDS, 23.63px before "Home" and after "My Stuff" where
   the native bar has 6px. Hugging the content reproduces the native numbers
   exactly (443.59 / 6 / 6, verified against a live native bar). */
+'.jf-mu-mainbar .emby-tabs-slider{width:max-content;margin-left:auto;margin-right:auto;}'
/* Jellyfin parks every .emby-tab-button at position:absolute; left:-9999px;
   visibility:hidden and its emby-tabs component un-hides them when it lays the
   strip out. .jf-mu-mainbar is OUR container, not an emby-tabs component, so
   nothing ever un-hid them: measured left:-9999px, visibility:hidden on every
   pill on #/livetv, #/home?sports=1 and the library routes -- the bar was there
   in the DOM, 7px wide, with all four pills off-screen and unclickable. That is
   "the main pill tab is gone".
   NB a hidden element like this still returns getClientRects().length > 0, which
   is why earlier passes that only read textContent scored it as present. */
+'.headerTabs .emby-tabs-slider{display:flex;}'
/* sf-hdr-ready: the pill strip assembles in public -- measured the header
   growing 49 -> 57 -> 96 -> 119px and the labels passing through
   首页|Live TV|Sports|我的最爱 before settling on the final Chinese set ~30ms
   later. Hold the strip invisible (but still laid out, so nothing reflows) until
   it is final, then fade it in. */
+'html:not(.sf-hdr-ready) .headerTabs .emby-tabs-slider,'
/* sf-hdr-parts (2026-08-28): the BUTTONS assemble in public too, not just the
   pill strip. Measured cold on a 390px viewport:
       600-900ms  49px, empty bar
       1100ms     57px, THREE icons only -- language, EN, library_music
       1400ms     121px, the real header (menu/language/music/search/person + pills)
   That 1100ms frame is the admin's "header nav did not load in correctly yet": a
   half-built nav, on screen, for ~300ms. The pill strip was already gated; the
   button groups were not, so they leaked through the same window the strip was
   being protected from. Gate them on the same signal so the header goes from
   empty to FINAL in one step, never through a partial state. */
+'html:not(.sf-hdr-ready) .skinHeader .headerLeft,'
+'html:not(.sf-hdr-ready) .skinHeader .headerRight,'
+'html:not(.sf-hdr-ready) .jf-ltv-sub{opacity:0;'
/* failsafe: if the reveal JS never runs the bar appears by itself at 12s
   rather than staying invisible for the session */
+'animation:sf-hdr-failsafe .3s ease 12s both;}'
+'@keyframes sf-hdr-failsafe{from{opacity:0;}to{opacity:1;visibility:visible;}}'
+'.headerTabs .emby-tabs-slider,.jf-ltv-sub,.skinHeader .headerLeft,.skinHeader .headerRight{transition:opacity .2s ease;}'
/* sf-hdr-in (2026-09-04). The admin: make the header load in smoothly too.
   The .2s transition above never ran -- measured, the header went
   op=0.000 at 996ms to op=1.000 at 1012ms, one frame, on every load.
   Cause: the held rule carries `animation:sf-hdr-failsafe .3s ease 12s
   both`, and fill-mode `both` means that animation OWNS opacity for the
   whole 12s delay. A transition cannot interpolate a property an
   animation is controlling, so when .sf-hdr-ready lands the rule stops
   matching, the animation is removed, and opacity snaps from the
   animation's 0 to the base 1. Nothing to transition between.
   Answer it the way the home rows already do (see sf-floatin-altname):
   change the animation NAME, which restarts the animation, instead of
   hoping a transition can fight one. Same easing as the rows so the
   header reads as part of the same entrance.
   Opacity only, deliberately. .emby-tabs-slider is the element Jellyfin
   translateX-es to scroll the tab strip, and .skinHeader is fixed with a
   Media Bar gradient layered on it -- animating transform on either
   would fight machinery that already owns it.
   Scoped to a one-shot .sf-hdr-in rather than .sf-hdr-ready: the tab
   strip is rebuilt on route changes, and keying off the sticky class
   would re-fade the strip on every navigation, on top of sf-nav-swap's
   own 320ms blank. Only the first reveal animates. */
+'html.sf-hdr-in .headerTabs .emby-tabs-slider,'
+'html.sf-hdr-in .skinHeader .headerLeft,'
+'html.sf-hdr-in .skinHeader .headerRight,'
+'html.sf-hdr-in .jf-ltv-sub{animation:sfHdrIn var(--sf-dur-enter-dense) var(--sf-ease) both;}'
+'@keyframes sfHdrIn{from{opacity:0;}to{opacity:1;}}'
+'@media (prefers-reduced-motion: reduce){html.sf-hdr-in .headerTabs .emby-tabs-slider,'
+'html.sf-hdr-in .skinHeader .headerLeft,html.sf-hdr-in .skinHeader .headerRight,'
+'html.sf-hdr-in .jf-ltv-sub{animation:none;opacity:1;}}'
/* sf-pill-fit: German is simply longer -- Startseite(101) + Live-TV(84) +
   Sport(66) + Meine Sachen(137) = 411px of pills into 389px of bar, so the strip
   became a horizontal scroller on a phone. Shrinking the words would mean bad
   German; tightening the pills keeps every label intact and works for whatever
   language comes next. Two steps, applied only when it actually overflows. */
/* sf-rowplay: none of the music landing rows had ANY play control -- measured 0
   across Recently Played, Most Played and the album rows -- so tapping a card
   could only open the album page ("I press play on last played and it takes me
   to the music album page"). Always visible, because on a phone there is no
   hover to reveal it. */
+'.sf-rowplay{position:absolute;right:7px;bottom:7px;width:34px;height:34px;border-radius:50%;'
+'border:0;padding:0;display:flex;align-items:center;justify-content:center;cursor:pointer;'
+'background:rgba(12,12,14,.72);color:#fff;z-index:12;backdrop-filter:blur(6px);}'
+'.sf-rowplay .material-icons{font-size:21px;line-height:1;}'
+'.sf-rowplay:hover{background:rgba(12,12,14,.92);}'
+'.sf-rowplay-host{position:relative;}'
/* sf-cardmenu: Jellyfin does NOT render its card overlay buttons at all on a
   touch layout -- measured on a real Android UA, every one of its home rows had
   menuPresent:false, so there was no ⋮ to style. We inject our own, carrying
   data-action="menu" so Jellyfin's own delegation opens its real item menu
   (remove from Continue Watching, mark played, details). */
+'.sf-cardmenu{position:absolute;right:6px;bottom:6px;width:32px;height:32px;border:0;padding:0;'
+'border-radius:12px;display:flex;align-items:center;justify-content:center;cursor:pointer;'
+'background:transparent;color:#fff;z-index:12;}'
+'.sf-cardmenu .material-icons{font-size:20px;line-height:1;}'
/* one appearance for every ⋮ we draw: our own rows inherited Jellyfin's
   cardOverlayButton look (no backdrop) while the injected ones had a round
   scrim, so the same control looked like two different controls */
/* sf-mlcard-hover (2026-08-29). The admin: "fix watchlist row, it doesnt behave right
   like the hover icons dont show up there" and "live tv, music, audiobook are
   like the watchlist needs fixing". All four are OUR rows (.sf-ml-card), so they
   share one fix.
   Measured on a Watchlist card, hovered and not: the ⋮ was opacity 1 in BOTH
   states -- permanently on -- and 32px with an rgba(12,12,14,.72) circle, while
   a native card's controls are 39px, transparent, radius 12px, and fade 0 -> 1.
   Values below are copied from the native button as measured, not invented:
     rest  colour rgba(255,255,255,.76), background transparent
     hover colour rgb(245,245,247),      background rgba(0,0,0,.4)
     transition background .37s cubic-bezier(.16,1,.3,1), colour .37s */
+'.sf-ml-more{width:39px!important;height:39px!important;border-radius:12px!important;'
+'background:transparent!important;display:flex!important;align-items:center!important;'
+'justify-content:center!important;padding:0!important;'
+'color:rgba(255,255,255,.76)!important;backdrop-filter:none!important;'
+'transition:background .37s cubic-bezier(.16,1,.3,1),color .37s!important;}'
+'.sf-ml-more:hover,.sf-ml-more:focus-visible{'
+'background:rgba(0,0,0,.4)!important;color:#f5f5f7!important;}'
+'.sf-ml-more .material-icons{font-size:20px!important;line-height:1!important;}'
/* clear the progress bar on the rows that have one (Continue Watching) */
+'.card:has(.itemProgressBar) .sf-cardmenu{bottom:26px;}'
+'.sf-cardmenu-host{position:relative;}'
/* sf-card-details: a touch layout has no hover, so Jellyfin's own play button
   sits on every card at opacity 0 -- present, 56x56, and invisible. Revealing it
   is the whole feature on a phone: it already carries data-action resume/play
   and the card's resume position, so it needs no handler of ours. */
+'html.layout-mobile #indexPage .cardOverlayButton-hover{opacity:1;}'
+'html.layout-mobile #indexPage .cardOverlayContainer{background:rgba(0,0,0,.18);}'
/* sf-playspin: tapping a card starts a request that can take seconds (transcode
   negotiation, Soulseek-sourced audio, a cold NAS), and until now the UI did
   nothing at all so the tap read as ignored. Reuses Jellyfin's own .docspinner
   box so it sits exactly where its loading indicator does. */
+'.sf-playspin{position:fixed;left:0;top:0;right:0;bottom:0;z-index:9999998;'
+'display:flex;align-items:center;justify-content:center;background:rgba(0,0,0,.28);}'
+'.sf-playspin i{display:block;width:52px;height:52px;border-radius:50%;'
+'border:3px solid rgba(255,255,255,.25);border-top-color:#fff;'
+'animation:sf-playspin-rot .8s linear infinite;}'
+'@keyframes sf-playspin-rot{to{transform:rotate(360deg);}}'
/* sf-optibar (2026-08-20): OPTIMISTIC now-playing bar.
   Measured before this: tapping Play gave no feedback at all for 558ms, and the
   real now-playing bar did not appear until 2.2-2.3s -- AFTER the audio had
   already started. People notice delay from about 100ms, and Spotify's web
   player paints its bar instantly from data it already has, then lets audio
   catch up. We already know the title, artist and cover of the thing being
   tapped, so there is nothing to wait for.
   Sized and positioned to match Jellyfin's own bar so the handover is invisible;
   it removes itself the moment the real bar is up. */
/* sf-opti-match (2026-08-27): the placeholder was matched to JELLYFIN'S bar --
   flush, square, solid #101010 -- and then the real bar became the floating
   capsule and this was never updated. So the first play of a session showed a
   square dark slab that a moment later became a rounded translucent capsule,
   which reads exactly as "the old player bar, then the new one". The admin reported
   it as that.
   Caught by recording every animation frame: a 50ms poll missed it entirely.

       63ms   #sf-optibar   h=53  radius=0px   bg=rgb(16,16,16)
       3835ms .nowPlayingBar h=52 radius=26px  bg=rgba(44,44,46,.82)

   Values below are measured off the live .appfooter, not guessed:
     phone   full width, h=56, radius 14px 14px 0 0, rgba(42,42,42,.69) blur(15px)
     >=700   centred clamp(460px,44vw,720px), 20px up, radius 26px,
             rgba(44,44,46,.82) blur(26px) saturate(1.5) + the same shadow
   If the capsule is ever restyled, restyle this with it -- they are one object
   as far as the eye is concerned. */
+'.sf-optibar{position:fixed;left:0;right:0;bottom:0;z-index:9999997;'
+'display:flex;align-items:center;gap:10px;padding:8px 12px;'
+'height:56px;box-sizing:border-box;border-top:0;'
+'border-radius:14px 14px 0 0;background:rgba(42,42,42,.69);'
+'-webkit-backdrop-filter:blur(15px);backdrop-filter:blur(15px);'
+'transform:translateY(100%);animation:sf-optibar-in .18s ease-out forwards;}'
+'@keyframes sf-optibar-in{to{transform:translateY(0);}}'
/* the capsule only exists at >=700px; below that the real bar is deliberately a
   flush mini bar (see sf-music-capsule), which the base rule above already is */
+'@media (min-width:700px){.sf-optibar{left:50%;right:auto;'
+'width:clamp(460px,44vw,720px);margin:0 0 20px;height:52px;'
+'border-radius:26px;background:rgba(44,44,46,.82);'
+'-webkit-backdrop-filter:blur(26px) saturate(1.5);'
+'backdrop-filter:blur(26px) saturate(1.5);'
+'box-shadow:0 8px 32px rgba(0,0,0,.5),0 0 0 .5px rgba(255,255,255,.10);'
+'transform:translateX(-50%) translateY(140%);'
/* its own keyframe: the base one animates transform:translateY(0) and would
   drop the translateX(-50%) that centres it */
+'animation:sf-optibar-in-cap .18s ease-out forwards;}'
+'@keyframes sf-optibar-in-cap{to{transform:translateX(-50%) translateY(0);}}}'
+'.sf-optibar-art{width:36px;height:36px;flex:0 0 36px;border-radius:4px;'
+'background:#2a2a2a center/cover no-repeat;}'
+'.sf-optibar-txt{min-width:0;flex:1 1 auto;}'
+'.sf-optibar-t{font-size:14px;font-weight:600;color:#fff;'
+'white-space:nowrap;overflow:hidden;text-overflow:ellipsis;}'
+'.sf-optibar-a{font-size:12px;color:rgba(255,255,255,.6);'
+'white-space:nowrap;overflow:hidden;text-overflow:ellipsis;}'
+'.sf-optibar-s{flex:0 0 18px;width:18px;height:18px;border-radius:50%;'
+'border:2px solid rgba(255,255,255,.25);border-top-color:#fff;'
+'animation:sf-playspin-rot .8s linear infinite;}'
+'.sf-optibar-bar{position:absolute;left:0;right:0;top:0;height:2px;overflow:hidden;}'
+'.sf-optibar-bar i{display:block;height:100%;width:35%;background:#fff;opacity:.5;'
+'animation:sf-optibar-slide 1.1s ease-in-out infinite;}'
+'@keyframes sf-optibar-slide{0%{transform:translateX(-100%);}100%{transform:translateX(390%);}}'
/* sf-readalong: a reading surface, not a media overlay. Serif, a real measure
   (~62 characters), generous leading -- the point is that it is comfortable to
   READ while the narrator speaks, so it borrows from a book rather than from the
   player chrome around it. The active sentence is marked with a soft block
   highlight rather than a karaoke wipe: at a narrator's pace a per-word wipe is
   distracting, and Audible's own immersion reading highlights whole sentences. */
+'.sf-ra{position:fixed;inset:0;z-index:9999996;display:none;'
+'background:#faf7f0;color:#1c1a17;--sf-ra-fs:19px;}'
+'.sf-ra.sf-ra-open{display:flex;flex-direction:column;}'
+'html.sf-ra-lock,html.sf-ra-lock body{overflow:hidden;}'
+'.sf-ra-top{flex:0 0 auto;display:flex;align-items:center;gap:12px;'
+'padding:10px 14px;border-bottom:1px solid rgba(0,0,0,.12);background:#f3efe6;}'
+'.sf-ra-title{flex:1 1 auto;min-width:0;font-size:15px;font-weight:600;'
+'white-space:nowrap;overflow:hidden;text-overflow:ellipsis;}'
+'.sf-ra-x,.sf-ra-sz{flex:0 0 auto;background:none;border:0;color:#1c1a17;'
+'width:40px;height:40px;border-radius:50%;cursor:pointer;}'
+'.sf-ra-x:hover,.sf-ra-sz:hover{background:rgba(0,0,0,.07);}'
+'.sf-ra-text{flex:1 1 auto;overflow-y:auto;-webkit-overflow-scrolling:touch;'
+'padding:26px 20px 55vh;}'
+'.sf-ra-ch{max-width:34em;margin:34px auto 14px;font-size:13px;'
+'letter-spacing:.14em;text-transform:uppercase;color:#8a7f6d;font-weight:600;}'
+'.sf-ra-p{max-width:34em;margin:0 auto 1.05em;'
+'font-family:Georgia,"Iowan Old Style","Times New Roman",serif;'
+'font-size:var(--sf-ra-fs);line-height:1.72;color:#3b352c;}'
/* box-decoration-break keeps the highlight looking like one continuous mark
   when a sentence wraps across lines, instead of two detached rectangles */
+'.sf-ra-s{cursor:pointer;border-radius:5px;padding:1px 2px;'
+'-webkit-box-decoration-break:clone;box-decoration-break:clone;'
+'transition:background-color .18s ease,color .18s ease;}'
/* read text recedes; it should not compete with where the narrator actually is */
+'.sf-ra-s.sf-ra-done{color:#a9a094;}'
+'.sf-ra-p:has(.sf-ra-s.sf-ra-on){color:#3b352c;}'
+'.sf-ra-s.sf-ra-on{background:#ffe9a8;color:#1c1a17;}'
+'@media (prefers-color-scheme:dark){'
+'.sf-ra{background:#14120f;color:#eae4d8;}'
+'.sf-ra-top{background:#1b1815;border-bottom-color:rgba(255,255,255,.10);}'
+'.sf-ra-x,.sf-ra-sz{color:#eae4d8;}'
+'.sf-ra-x:hover,.sf-ra-sz:hover{background:rgba(255,255,255,.10);}'
+'.sf-ra-s{color:#c9c1b4;}'
+'.sf-ra-s.sf-ra-done{color:#6f675c;}'
+'.sf-ra-s.sf-ra-on{background:#4a3a12;color:#fff6de;}'
+'.sf-ra-ch{color:#9a8f7c;}'
+'}'
/* sf-ra-detail-visible: branding.xml simplifies the detail action row with
   `#itemDetailPage.sf-atv .mainDetailButtons > button:not(.btnPlay):not(.sf-infobtn)
    { display:none !important }`
   which swallowed our Read along button -- it existed in the DOM at 0x0 while
   the identically-placed .sf-infobtn rendered fine. Editing branding.xml does
   not help: Jellyfin caches that config in memory and only re-reads it on
   restart, so the fix belongs here where it ships with index.html. Both rules
   are !important, so this has to WIN ON SPECIFICITY. Theirs is (1,4,1) --
   #itemDetailPage + .sf-atv + .mainDetailButtons + :not(.btnPlay) +
   :not(.sf-infobtn) + button -- and :not() contributes its argument's weight.
   Repeating the class TWICE only tied it, and branding.css is linked after
   index.html so the tie went to them. Three times makes it (1,5,1). */
+'#itemDetailPage.sf-atv .mainDetailButtons > button.sf-ra-detail.sf-ra-detail.sf-ra-detail{'
+'display:inline-flex!important;align-items:center;justify-content:center;}'
/* sf-ab-bm: a ribbon, drawn rather than an icon font so it cannot arrive late. */
+'.sf-ab-bmk{display:inline-block;width:12px;height:16px;vertical-align:-3px;'
+'background:currentColor;'
+'-webkit-clip-path:polygon(0 0,100% 0,100% 100%,50% 72%,0 100%);'
+'clip-path:polygon(0 0,100% 0,100% 100%,50% 72%,0 100%);}'
+'.sf-ab-mi-hasx{display:flex;align-items:center;justify-content:space-between;gap:1em;}'
+'.sf-ab-mi-x{opacity:.45;font-size:1.15em;line-height:1;padding:0 .15em;cursor:pointer;}'
+'.sf-ab-mi-x:hover{opacity:1;}'
+'.sf-ab-book{display:inline-block;width:17px;height:14px;'
+'border:2px solid currentColor;border-radius:2px;position:relative;}'
+'.sf-ab-book:after{content:"";position:absolute;left:50%;top:-2px;bottom:-2px;'
+'width:2px;background:currentColor;transform:translateX(-50%);}'
+'.sf-ra-btn{width:40px;height:40px;border:0;background:none;cursor:pointer;'
+'color:inherit;flex:0 0 auto;}'
+'@media (max-width:45em){.sf-ra-text{padding:18px 16px 60vh;}}'
+'.sf-cardplay{position:absolute;left:0;top:0;width:1px;height:1px;opacity:0;'
+'pointer-events:none;border:0;padding:0;background:none;}'
+'.sf-ml-br{opacity:0;pointer-events:auto;transition:opacity .2s ease;}'
+'.sf-ml-card:hover .sf-ml-br,.sf-ml-card:focus-within .sf-ml-br{opacity:1;}'
+'@media (hover:none){.sf-ml-br{opacity:1;}}'
/* sf-cardmenu-hover (2026-08-29). The admin: "make the 3 dots abyss themed and like
   the other 2 icons show up on hover".
   Measured on a home card with NOTHING hovered: Mark played opacity 0, Add to
   favorites opacity 0, More opacity 1 -- the corner menu was the only control
   forced visible, by the opacity:1!important this rule replaces. It did not
   match them either: those two are transparent with a 12px radius, while the ⋮
   was a rgba(12,12,14,.72) circle with a blur behind it.
   So drop the force (it now fades in with its neighbours through Jellyfin's own
   .cardOverlayButton-hover) and give it their clothes. Touch keeps its own
   always-visible rule further down, because there is no hover there. */
+'#indexPage .card .cardOverlayButton[data-action="menu"]{'
+'background:transparent!important;border-radius:12px!important;'
+'backdrop-filter:none!important;pointer-events:auto!important;}'
/* sf-cardmenu-hoverbg (2026-08-29): the rule above neutralises the RESTING look,
   but `background:transparent!important` also beat the theme's :hover rule, so
   the ⋮ was the one control that stayed flat under the pointer. Measured with
   the pointer ON each button: Mark played goes to rgba(0,0,0,.4), the ⋮ stayed
   rgba(0,0,0,0) -- both did change colour, which is why it looked ALMOST right.
   Restate the hover fill at the same specificity, with the value measured off
   its neighbour rather than invented. */
+'#indexPage .card .cardOverlayButton[data-action="menu"]:hover,'
+'#indexPage .card .cardOverlayButton[data-action="menu"]:focus-visible{'
+'background:rgba(0,0,0,.4)!important;}'
+'#indexPage .card .cardOverlayContainer{opacity:1!important;background:none!important;}'
/* sf-home-tap: the same rule as our own rows, applied to Jellyfin's cards on the
   home page -- the ARTWORK plays, and the corner control is the ⋮ menu (remove
   from Continue Watching, mark played, details) rather than a second Play.
   Jellyfin's own overlay already carries a data-action="menu" button; the
   play/resume one is simply hidden, not removed, so its delegation stays intact. */
+'#indexPage .card .cardOverlayButton[data-action="play"],'
+'#indexPage .card .cardOverlayButton[data-action="resume"]'
+'{opacity:0!important;pointer-events:none!important;}'
/* the ⋮ has to be reachable on a phone, where there is no hover */
+'@media (hover:none){#indexPage .card .cardOverlayContainer{opacity:1!important;background:none!important;}'
+'#indexPage .card .cardOverlayButton[data-action="menu"]{opacity:1!important;pointer-events:auto!important;}}'
/* sf-detail-cardhover (2026-08-29). The admin: "when i hover over the cast or more
   like this, or any of the rows media boxes it shows up bad as in the overlay
   darkening doesnt look good. it looks jank."
   Measured on a movie detail page: .cardOverlayContainer is rgba(0,0,0,.7) and
   hover flips its opacity 0 -> 1. Two things make that read as broken:
     - it is a SQUARE box drawn over a ROUND person card, so hovering a cast
       portrait puts a black rectangle around the circle;
     - the element's transition lists `background`, NOT `opacity`, so the 70%
       black does not fade in at all, it snaps.
   #indexPage already neutralises exactly this (see the rules above) -- the
   detail page was simply never included in that scope, so it kept Jellyfin's
   stock scrim. Same treatment here, which also keeps the two surfaces
   consistent: no scrim, and the corner control is still the hover affordance.
   Deliberately NOT hiding the play/resume overlay button the way #indexPage
   does -- on home the artwork itself plays, which is not true of Cast & Crew or
   More Like This, so hiding it there would remove an action and not just a
   decoration. */
+'#itemDetailPage .card .cardOverlayContainer{background:none!important;}'
/* touch has no hover, so the corner control would otherwise never be reachable */
+'@media (hover:none){#itemDetailPage .card .cardOverlayContainer{opacity:1!important;background:none!important;}'
+'#itemDetailPage .card .cardOverlayButton[data-action="menu"]{opacity:1!important;pointer-events:auto!important;}}'
/* sf-cw-barclear: the progress bar runs along the bottom of the artwork and the
   corner button sits in the same strip, so they overlapped. Lift the button
   clear of the bar rather than moving the bar, which is a fixed part of the card. */
/* The corner is the corner: 30px of clearance is only needed on cards that
   actually carry a progress bar (Continue Watching). Applying it everywhere
   floated the ⋮ 31px up the artwork on every other row -- measured against our
   own rows, which sit at 5px from both edges. */
+'#indexPage .card .cardOverlayButton-br{bottom:5px!important;}'
+'#indexPage .card:has(.itemProgressBar) .cardOverlayButton-br{bottom:30px!important;}'
/* sf-lang-size: the language button measured 30x20 against its siblings, so its
   hover/pressed backdrop was a different shape. NOTE the sibling header icons
   are 41x41 as of 2026-08-23 (they were 36x36 when this was written), so a
   hardcoded 36 had drifted back into being the odd one out. If the header icon
   size changes again, this has to move with it. */
+'.sf-lang-btn{width:41px!important;height:41px!important;display:inline-flex!important;'
+'align-items:center!important;justify-content:center!important;padding:0!important;}'
+'.sf-lang-btn .sf-lang-code{position:absolute;bottom:2px;right:2px;font-size:9px;line-height:1;'
+'opacity:.85;pointer-events:none;}'
+'.sf-lang-btn{position:relative!important;}'
/* Jellyfin's own .cardOverlayContainer sits above our button in its own stacking
   context, so a finger tap landed on its hover-only play icon -- which is inert
   on touch, so the tap did nothing at all (verified: tap by coordinates produced
   no audio and no navigation, while calling our handler directly played fine).
   On a touch device that overlay has no purpose, so let taps pass through it.
   Scoped to cards we injected into, so nothing else changes. */
+'@media (hover:none){.sf-rowplay-host > .cardOverlayContainer{pointer-events:none;}}'
+'html.sf-pill-tight .headerTabs .emby-tab-button{padding-left:10px!important;padding-right:10px!important;}'
+'html.sf-pill-tighter .headerTabs .emby-tab-button{padding-left:6px!important;padding-right:6px!important;'
+'font-size:93%!important;}'
/* A third level, and a last-resort scroll. German clips at 360px on the main bar
   and at EVERY width on the sub-bars (Programme|Fernsehprogramm|Kanäle,
   Filme|Vorschläge|Favoriten|Sammlungen|Genres). Centred overflow clips on both
   sides, so when even the smallest size does not fit the bar left-aligns and
   scrolls instead -- swipeable, never cut off mid-word. */
+'html.sf-pill-tightest .headerTabs .emby-tab-button,'
+'html.sf-pill-tightest .jf-fav-tab{padding-left:4px!important;padding-right:4px!important;'
+'font-size:86%!important;}'
+'html.sf-pill-tight .jf-fav-tab{padding-left:10px!important;padding-right:10px!important;}'
+'html.sf-pill-tighter .jf-fav-tab{padding-left:6px!important;padding-right:6px!important;font-size:93%!important;}'
+'html.sf-pill-scroll .headerTabs .emby-tabs-slider,'
+'html.sf-pill-scroll .jf-fav-tabs{justify-content:flex-start!important;overflow-x:auto!important;'
+'scrollbar-width:none;}'
+'html.sf-pill-scroll .headerTabs .emby-tabs-slider::-webkit-scrollbar,'
+'html.sf-pill-scroll .jf-fav-tabs::-webkit-scrollbar{display:none;}'
+'.headerTabs .emby-tab-button{position:relative!important;left:auto!important;'
+'right:auto!important;visibility:visible!important;}'
/* sf-nav-unhide: Audio Books and Playlists have no tabs of their own, and
   Jellyfin marks the empty .headerTabs with .hide (display:none), so our bar
   was correctly inserted there and measured 0x0. Un-hide the container only
   while it actually holds our bar. Deliberately CSS rather than stripping the
   class in JS: Jellyfin re-adds .hide on navigation, so a JS fight would need
   state and could flicker -- this simply stops matching the moment the bar is
   removed, and Jellyfin keeps ownership of its own class. */
+'.headerTabs.hide:has(.jf-mu-mainbar){display:block!important;}'
/* sf-nav-abyss: earlier revisions hand-built this bar -- first with copied
   pill values, then with a bare .emby-tab-button class -- and it still did not
   look like the real pills, because the theme dresses the whole native
   STRUCTURE, not one class. Reading a live pill settled it: Jellyfin's own
   buttons carry `.emby-button` (which is what supplies border:0, inline-flex
   and the component metrics) alongside `.emby-tab-button`, and they sit in an
   .emby-tabs-slider inside a .tabs-viewmenubar. Our bar is now that exact
   structure -- the same shape jf-livetv-tab and jf-sports-tab already use --
   so Abyss and every future theme style it with no values copied here at all.
   Only the 10px gap above is ours.
   The rules below dress the library's own strip as the secondary row; our bar
   is not a .tabs-viewmenubar (see sf-nav-notabbar) so they cannot reach it. */
+'html.sf-music-nav .headerTabs .tabs-viewmenubar .emby-tabs-slider{padding:5px 2.5px;border:0;}'
+'html.sf-music-nav .tabs-viewmenubar .emby-tab-button{padding:5.93712px 19.7904px;margin:0;font-size:14.136px;min-width:0;height:32px;}'
+'html.sf-music-nav .tabs-viewmenubar .emby-tab-button-active{background:rgb(245,245,247);color:rgb(18,18,18);}'
/* sf-dice-swap: the random-item dice (Jellyfin Enhanced) is not something
   anyone here reaches for; Music takes its slot. Hidden, not removed, so the
   plugin keeps its own state. */
+'#randomItemButton{display:none!important;}'
/* sf-owned-albums: library albums for an artist-name search, shown first. */
+'.sf-lib-albums{margin:.5em 0 1em;}'
/* sf-lib-title-match: this row's heading used to be a bare <h2> with
   font-size:1.1em, which computed to 16.4px/400 next to Jellyfin's own
   22.3px/600 section titles -- measured side by side, and it read as a
   different, smaller kind of heading. The h2 now carries Jellyfin's own
   .sectionTitle .sectionTitle-cards classes (see sfOwnedAlbums), so size,
   weight and colour come from the theme and keep matching if the theme
   changes. Only the bottom margin is ours, to space the row's posters. */
+'.sf-lib-albums h2.sectionTitle{margin:0 0 .5em;}'
+'.sf-lib-row{display:flex;gap:.8em;overflow-x:auto;padding-bottom:.4em;}'
+'.sf-lib-alb{flex:0 0 auto;width:8.5em;text-decoration:none;color:inherit;}'
+'.sf-lib-alb-img{display:block;width:8.5em;height:8.5em;border-radius:8px;background-size:cover;background-position:center;background-color:#222;}'
+'.sf-lib-alb-t{display:block;margin-top:.35em;font-size:.85em;line-height:1.25;}'
+'.sf-lib-alb-y{display:block;font-size:.78em;opacity:.6;}'
/* sf-music-ux: empty Suggestions sections, and video-only controls that show
   up while playing a song (Jellyfin's own class for them is videoButton). */
+'.verticalSection[data-sf-empty]{display:none!important;}'
+'.nowPlayingPage.sf-audio-now .videoButton{display:none!important;}'
+'.nowPlayingPage.sf-audio-now .btnNowPlayingRewind{display:none!important;}'
+'.nowPlayingPage.sf-audio-now .btnNowPlayingFastForward{display:none!important;}'
+'@media (hover:none){.nowPlayingPage .nowPlayingVolumeSliderContainer{display:none!important;}}'
/* sf-album-clean: the album's own name is never rendered -- .itemName holds
   "folklore" but computes to display:none, and no readable rule sets it
   (checked every sheet, Branding CSS, and the media-bar plugin CSS directly).
   Force it back. .parentNameLast is the album/episode variant, so movie pages
   are untouched. */
+'.itemDetailPage .nameContainer .itemName.parentNameLast{display:block!important;}'
/* sf-title-dup: when the logo belongs to THIS item it already is the title,
   so the text form is a duplicate (movies/series). Higher specificity than the
   rule above so it wins. */
+'.itemDetailPage .nameContainer .itemName.parentNameLast.sf-title-dup{display:none!important;}'
+'@media (max-width:600px){'
/* 74px of MusicBrainz/TheAudioDb links sat above the track list; kept on
   desktop, dropped where space is scarce. */
+'.itemDetailPage .itemExternalLinks{display:none!important;}'
/* 16 genres = a 241px wall pushing the tracks off screen. */
/* sf-album-clean2: a raw max-height sliced the third line through the middle
   of the letters. Clamp the value element itself so it breaks between
   lines. */
+'.itemDetailPage .genresGroup{max-height:none;}'
+'.itemDetailPage .genres.content{display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden;}'
+'}'
/* sf-detail-mobile: at 390px the detail ribbon still reserved 126px of
   left padding for a poster that is stacked above on mobile, squeezing the
   action buttons into 111px and crushing the Play button to 59px -- its
   "Play" label (added by Branding custom CSS as ::after) had no room and sat
   on top of the icon. Reclaim the padding, stack the ribbon, and let the
   button size to its content. max-width:none is required because a
   CORS-blocked plugin stylesheet pins it to 58.5px. */
+'@media (max-width:600px){'
+'.detailRibbon.padded-left{padding-left:1.1em!important;}'
+'.detailRibbon.padded-right{padding-right:1.1em!important;}'
/* sf-detail-mobile2: the ribbon has a fixed height:107px, fine as one row but
   too short once stacked -- the buttons overlapped the Video/Audio rows
   below. Let it size to its content. */
+'.detailRibbon{flex-direction:column!important;align-items:flex-start!important;height:auto!important;min-height:0!important;}'
+'.mainDetailButtons{width:100%;gap:.5em;margin-top:.6em;justify-content:flex-start;}'
+'.mainDetailButtons .btnPlay{flex-direction:row!important;align-items:center;width:auto!important;max-width:none!important;min-width:0!important;flex:0 0 auto!important;padding:0 .95em 0 .7em!important;gap:.3em;}'
+'.mainDetailButtons .btnPlay .detailButton-content{flex-direction:row!important;}'
+'}'
+'.sf-ls-title{color:rgba(255,255,255,.92);font-weight:600;font-size:1em;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;}'
+'.sf-ls-sub{color:rgba(255,255,255,.55);font-weight:200;font-size:.85em;margin-top:.15em;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;}'
+'.sf-ls-card.sf-ls-upcoming{background-color:#181818;}'
+'.sf-ls-upcoming .sf-ls-icon{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;font-size:2.4em;opacity:.22;}'
+'.sf-ls-empty{color:rgba(255,255,255,.5);font-weight:200;font-size:.9em;padding:2em 0;text-align:center;}'
/* A card whose channel number has no match in /LiveTv/Channels cannot be
   played -- goToChannel() bails on !jfItem. It used to look identical to a
   working card and simply do NOTHING on click, with no explanation. Dim it and
   relabel the badge so the state is visible before you tap. */
+'.sf-ls-card.sf-ls-unavail{opacity:.4;cursor:default;}'
+'.sf-ls-card.sf-ls-unavail:hover{transform:none;}'
/* sf-ls-scrolllock: the overlay is position:fixed, so wheel input reaches
   the document behind it -- the scrollbar moves while the sports content
   stays put and ~497px of games cannot be reached. Freeze the page behind
   the overlay so it is the only scrollable surface. :has() keeps this in
   CSS: no JS bookkeeping, and it lifts automatically when .sf-ls-show goes
   away. */
+'html:has(.sf-livesports-root.sf-ls-show){overflow:hidden!important;}'
+'body:has(.sf-livesports-root.sf-ls-show){overflow:hidden!important;}'
/* sf-ls-nobounce: `contain` blocked the chaining but not the elastic bounce;
   at the end of the list the overlay still rubber-banded and the home page
   showed through. `none` disables the bounce itself. Also set on html/body
   because the rubber-band can originate on the document even with its
   overflow hidden. */
+'.sf-livesports-root.sf-ls-show{overscroll-behavior:none;}'
+'html:has(.sf-livesports-root.sf-ls-show){overscroll-behavior:none;}'
+'body:has(.sf-livesports-root.sf-ls-show){overscroll-behavior:none;}'
+'.sf-ls-badge.sf-ls-syncing{background:rgba(255,255,255,.22);color:#f0f0f0;}'
/* Count chip on each pill, so "how many games are in here" is answerable
   without opening the filter. */
+'.sf-ls-pillcount{opacity:.55;font-weight:600;margin-left:.35em;}'
/* Upcoming: compact time-first rows, deliberately unlike the live poster
   tiles. Narrower track, flat surface, no aspect-ratio box, no hover scale. */
+'.sf-ls-upgrid{grid-template-columns:repeat(auto-fill,minmax(310px,1fr));gap:.5em;}'
+'.sf-ls-uphead{font-size:1.15em;color:rgba(255,255,255,.62);}'
+'.sf-ls-card.sf-ls-upcoming{aspect-ratio:auto;display:flex;align-items:center;gap:.85em;padding:.62em .9em;background:rgba(255,255,255,.035);border:1px solid rgba(255,255,255,.06);border-radius:10px;}'
+'.sf-ls-card.sf-ls-upcoming:hover{transform:none;background:rgba(255,255,255,.07);}'
+'.sf-ls-card.sf-ls-upcoming::after{display:none;}'
+'.sf-ls-uptime{flex:0 0 auto;min-width:4.6em;font-size:.86em;font-weight:700;color:#e8e8e8;font-variant-numeric:tabular-nums;}'
+'.sf-ls-upinfo{min-width:0;}'
+'.sf-ls-uptitle{color:rgba(255,255,255,.82);font-weight:600;font-size:.94em;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;}'
+'.sf-ls-upsub{color:rgba(255,255,255,.42);font-weight:200;font-size:.8em;margin-top:.1em;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;}'
/* sf-ltv-settle: hold the tab strip invisible on a Live TV load until our pills
   are in, so Jellyfin's own Programs/Guide/Channels strip never flashes first.
   Deliberately emitted FROM THIS SCRIPT and not from branding.xml: if the patch
   ever fails to run, this rule does not exist and the stock bar shows normally
   (fail-open). visibility keeps the header's height so nothing below jumps. */
/* sf-tabs-noflash (2026-09-01). The admin: "i get flashed the old header".
   This rule hid the stock tab bar only ONCE JS had added .sf-tabs-unstyled,
   so the stock bar was visible from first paint until sfTabArm() ran -- the
   flash. The header block right above solves the same problem the other way
   round, with html:not(.sf-hdr-ready), and is hidden from the first frame.
   Use the same gate here: sfTabSettle already releases .sf-tabs-unstyled and
   .sf-hdr-ready together from one state machine, so the reveal moment is
   unchanged. Fail-open is preserved exactly: this CSS is emitted from THIS
   script (no script -> no rule -> stock bar shows), the 12s sf-tabs-failsafe
   still reveals it if the reveal JS never runs, and visibility:hidden keeps
   the header height so nothing below jumps. */
                +'html:not(.sf-hdr-ready) .headerTabs.sectionTabs .emby-tabs-slider{visibility:hidden;'
+'animation:sf-tabs-failsafe 0s linear 12s both;}'
+'@keyframes sf-tabs-failsafe{to{visibility:visible;opacity:1;}}'
/* sf-hide-bar: two places the now-playing bar appeared as the raw, unstyled
   stock bar.
   1. Over a film. The capsule is deliberately audio-only, so as soon as a video
      starts the capsule rules stop matching and Jellyfin's own 80px bar comes
      back -- on top of the movie, duplicating the video OSD.
   2. The ADMIN DASHBOARD. Jellyfin does not apply user Custom CSS to admin
      pages at all: verified on #/dashboard that not one branding rule was in
      document.styleSheets, so the bar rendered there at its stock 1424x80 with
      none of the capsule styling. That is why this rule must live HERE, in the
      script-injected stylesheet, which does survive on the dashboard -- putting
      it in branding.xml would have no effect on that page.
   body.dashboardDocument is Jellyfin's own marker for admin pages. */
+'html.sf-video-now .appfooter,body.dashboardDocument .appfooter{display:none!important;}'
/* sf-cw-hidden: cards Jellyfin Enhanced has marked hidden for Continue
   Watching but which its own filter fails to remove (see sfHideCW). */
+'.verticalSection.ContinueWatching .card.sf-cw-hidden,'
                +'.sf-cwscope .card.sf-cw-hidden,'
                +'.sf-cwscope .sf-ml-card.sf-cw-hidden{display:none!important;}'
/* sf-cw-first (2026-09-01): let the first view (Continue Watching and anything
   ordered above it) animate while the container is still held for the rows
   below, so the first view never waits on the slowest row. */
                +'.homeSectionsContainer[data-sf-settle] > .verticalSection.sf-first{animation:sfHomeIn var(--sf-dur-enter) var(--sf-ease) both;animation-delay:calc(var(--sf-row-i,0) * .05s);}'
                +'@media (prefers-reduced-motion: reduce){.homeSectionsContainer[data-sf-settle] > .verticalSection.sf-first{animation:none;opacity:1;}}'
/* sf-hide-internal-playlists: "__np_queue" is the now-playing queue stored as a
   real playlist; it must exist but must never be offered as something to play. */
+'.card.sf-pl-internal{display:none!important;}'
/* sf-music-pad: beats Jellyfin's .libraryPage{padding-top:7.5em!important} on
   specificity (id + two classes vs one class). Only on layout-mobile, which is
   the case that actually breaks -- desktop's 7.5em already clears both bars.
   Falls back to 188px if the variable is missing, and the whole rule cannot
   exist unless this script ran. */
+'html.layout-mobile #musicRecommendedPage.libraryPage{padding-top:var(--sf-music-pad,188px)!important;}'
'''

# _LS_02 (orig L712-1416) -- sf-cwbook-art, sf-heroslot, sf-mus-heroh
_LS_02 = r'''/* sf-cwbook-art: make an audiobook card in Continue Watching read as the same
   object as the film and episode cards beside it.

   Everything except the picture already matched exactly -- measured card 340x247,
   image 313x176, radius 12px, identical progress bar and both text styles. The
   only thing that looked wrong was the ARTWORK: a book cover is ~1:1 while the row
   is 16:9, and the card painted it with background-size:cover, so the cover was
   zoomed until the top and bottom (i.e. the title and the author) were cropped off.

   Fix is two layers in the same 16:9 box: a blurred, over-scaled copy fills the
   frame so there are no letterbox bars, and the real cover sits on top CONTAINED
   so none of it is lost. Card geometry is untouched, so the row stays uniform. */
/* no `position` here on purpose: .coveredImage sets its own, and overriding it
   is what broke the box. It is already a positioned ancestor, so the two
   inset:0 children resolve against it. */
+'.sf-cwbook-img{overflow:hidden;background:#101010;}'
+'.sf-cwbook-blur,.sf-cwbook-fit{position:absolute;inset:0;background-repeat:no-repeat;background-position:50% 50%;}'
/* scale() hides the soft edge blur leaves at the boundary */
+'.sf-cwbook-blur{background-size:cover;filter:blur(18px) saturate(1.35) brightness(.62);transform:scale(1.18);}'
+'.sf-cwbook-fit{background-size:contain;}'
/* the cover is the focal point, so give it the same lift a poster has */
+'.sf-cwbook-fit{filter:drop-shadow(0 2px 10px rgba(0,0,0,.55));}'

/* ---- sf-music-ambient ---- the page takes its colour from the artwork.
   Every rule is gated on .sf-mus-amb, which is only set once a colour has
   actually been extracted, so a failed readback leaves the old look intact. */
/* sf-heroslot: same footprint the hero will occupy, so its arrival moves nothing.
   Heights measured from the real hero: 194px at 412px wide, 225px on desktop. */
/* sf-mus-heroh (2026-08-24): these reservations were stale and the page shoved
   itself around on every music load -- the admin: "the last played box load in and
   then change a few seconds later". Re-measured on the SETTLED hero, twice per
   width: 227px at 390px wide (the slot said 194 -- 33px short) and 230px at
   1280px (the slot said 225). The old 194 came from a 412px-wide measurement
   before the hero gained its second line.
   The slot alone is not enough: the real hero mounts at 139px and only reaches
   227px once its art and second line land, so replacing a correct slot with a
   139px hero still yanked the page UP and then back down. Giving the hero the
   SAME min-height as its slot means the swap is a no-op and nothing below moves.
   Measured before: Recently Played walked y=632 -> 820 -> 1058 -> 1153. */
/* sf-hero-oneshot: re-measured 2026-08-27 with min-height lifted off, AFTER the
   ambient class stopped enlarging the panel. The old 230/227 was measured on the
   ambient hero, whose padding was 2em 1.9em and title 2.1em; the panel is
   smaller now, so those numbers were holding open a hole:

       viewport   natural   was forced to   dead space
       390px      155px     231px           76px
       768px      155px     234px           79px
       1280px     215px     234px           19px

   Now set to the natural height, and the breakpoint moved 700 -> 999px to match
   the one the hero's OWN geometry uses (.sf-mus-hero-art / -title in
   branding.xml) -- at 768px the panel had mobile content inside a desktop
   reservation, which is where the worst of the gap came from.
   The slot and the hero MUST hold the same number, and the same margin, or the
   swap moves the page. */
/* re-measured again after sf-mus-nobox took the card padding off: 187px
   desktop / 153px below 999px. Measure with style.minHeight='0px' and read the
   rect -- never trust the number already in the CSS, it is what went stale. */
+'.sf-mus-heroslot{min-height:187px;margin:0 0 1.6em 0;}'
+'.sf-mus-hero{min-height:187px;}'
+'@media (max-width:999px){.sf-mus-heroslot{min-height:153px;}'
+'.sf-mus-hero{min-height:153px;}}'
/* sf-mus-nobox (2026-08-27, the admin: "i still dont like the hero box, like the
   outline of the bottom and right and the top left corner"). All three were the
   same object: a rounded card with a 1px rgba(255,255,255,.06) border, an
   accent radial-gradient anchored at 12% 0% (hence the glow in the TOP-LEFT
   corner) and a 90deg scrim that ran light-to-dark left-to-right, so the panel
   faded out towards the RIGHT and its edge showed against a flat black page --
   the BOTTOM and right edges being the two the gradients did not disguise.
   A card only earns its outline if it sits on a different surface. Now that
   sf-mus-pagebg carries the artwork across the whole page, the panel IS the
   surface, so it gets no border, no radius, no scrim and no background of its
   own -- just the cover, the type and the buttons on the ambient page.
   See branding.xml for the rules this used to fight. */
/* sf-hero-oneshot (2026-08-27): these two rules USED to live here, and they
   were the whole "it loads in and then changes" complaint. .sf-mus-amb is added
   only after the cover has been downloaded and read back through a canvas, so
   for one 400ms tick the panel stood at its base geometry and then re-laid
   itself out in view. Measured on a 390px phone: title 20.088px -> 31.248px
   (the album name re-truncated from "EVOLution (10th Ann..." to "EVOLution..."),
   inner padding 16.4px -> 29.8px, the buttons reflowed from side-by-side to
   stacked, the cover shrank, hero height 227 -> 247px, and every row below
   shifted down 20px.
   GEOMETRY MUST NOT DEPEND ON THE COLOUR. The ambient class now carries colour
   and nothing else, so whenever the accent lands -- early, late or never -- the
   layout is identical. The base rules in branding.xml own the sizing. */
/* sf-mus-pagebg: the flat 52vh accent wash that used to live here is gone --
   it stopped dead half way down and left the rest of the page black, which is
   exactly the seam the admin was seeing. body.sf-has-pagebg (sf-page-bg) now paints
   the real blurred cover for the full height, the same layer home uses. */
/* accent the primary action, like the dominant-colour play button both of the
   big services use */
+'html.sf-mus-amb .sf-mus-hero-play{background:var(--sf-mus-accent);color:#0d0d0d;'
+'border:0;font-weight:700;}'
+'html.sf-mus-amb .sf-mus-hero-play .material-icons{color:#0d0d0d;}'

/* sf-mus-dedupe: a repeated album in Recently Played */
+'.card.sf-mus-dup{display:none!important;}'

/* sf-nav-tuck: slide the upper pill bar out of the way while scrolling a
   library page, and give back the vertical space it was holding. */
+'.jf-mu-mainbar{transition:max-height .22s ease,opacity .18s ease,margin .22s ease;'
+'max-height:60px;overflow:hidden;}'
+'html.sf-nav-tucked .jf-mu-mainbar{max-height:0;opacity:0;margin-bottom:0;}'
/* ---- sf-now-immersive ---- full-screen player.
   Colour comes from --sf-np-a, set per track from the artwork; every value below
   degrades to a neutral dark surface if extraction failed. */
+'.sf-np{position:fixed;inset:0;z-index:1200;opacity:0;pointer-events:none;'
+'transition:opacity .28s ease;overflow:hidden;background:#0b0b0b;}'
+'.sf-np.sf-np-show{opacity:1;pointer-events:auto;}'
+'html.sf-np-lock{overflow:hidden;}'
/* blurred cover fills the frame; the tint is the drifting colour field that
   stands in for Apple-style "album motion" and works on any artwork */
+'.sf-np-bg{position:absolute;inset:-12%;background-size:cover;background-position:50% 50%;'
+'filter:blur(70px) saturate(180%);opacity:.55;transform:scale(1.1);}'
+'.sf-np-tint{position:absolute;inset:-30%;pointer-events:none;opacity:.85;'
+'background:radial-gradient(45% 45% at 28% 26%, var(--sf-np-a60,rgba(90,90,90,.5)) 0%, rgba(0,0,0,0) 70%),'
+'radial-gradient(42% 42% at 74% 68%, var(--sf-np-a25,rgba(70,70,70,.3)) 0%, rgba(0,0,0,0) 72%);'
+'animation:sfNpDrift 26s ease-in-out infinite alternate;}'
+'@keyframes sfNpDrift{0%{transform:translate3d(-2%,-1%,0) scale(1);}100%{transform:translate3d(3%,2%,0) scale(1.12);}}'
+'.sf-np-scrim{position:absolute;inset:0;pointer-events:none;'
+'background:linear-gradient(180deg,rgba(0,0,0,.34) 0%,rgba(0,0,0,.10) 32%,rgba(0,0,0,.62) 100%);}'
+'.sf-np-body{position:relative;z-index:2;height:100%;display:flex;align-items:center;'
+'justify-content:center;gap:3.2vw;padding:2.2rem;box-sizing:border-box;}'
+'.sf-np-close{position:absolute;top:1.1rem;left:1.2rem;width:44px;height:44px;border:0;'
+'border-radius:50%;background:rgba(255,255,255,.10);color:#fff;cursor:pointer;'
+'display:flex;align-items:center;justify-content:center;backdrop-filter:blur(12px);}'
+'.sf-np-close:hover{background:rgba(255,255,255,.18);}'
+'.sf-np-stage{display:flex;flex-direction:column;align-items:center;'
+'width:min(440px,86vw);max-width:440px;}'
/* the cover floats gently -- motion without needing an animated asset */
+'.sf-np-artwrap{width:min(380px,64vh);aspect-ratio:1/1;margin-bottom:1.7rem;}'
+'.sf-np-art{width:100%;height:100%;border-radius:18px;background-size:cover;'
+'background-position:50% 50%;background-color:#1a1a1a;'
+'box-shadow:0 34px 90px rgba(0,0,0,.62), 0 0 0 1px rgba(255,255,255,.05);'
+'animation:sfNpFloat 7s ease-in-out infinite alternate;}'
+'@keyframes sfNpFloat{0%{transform:translateY(0) scale(1);}100%{transform:translateY(-10px) scale(1.012);}}'
/* sf-np-landscape (2026-08-24): the player stacked everything in one column, which
   simply does not fit a phone on its side. Measured at 844x390, the stage children
   summed to 456px of content in 390px of viewport:
     artwrap 250 (top already clipped at y=-67) | meta 74 | scrub 36 |
     controls 70 (bottom at 413, BELOW the fold) | tabs 26 (y=431, far off-screen)
   So in landscape the transport controls AND the Lyrics/Up Next tabs were
   unreachable -- which also made fullscreen lyrics unreachable, since its entry
   button lives in the lyrics pane.
   Landscape gets the layout it should have had: artwork on the left, everything
   else stacked beside it. Grid rather than flex because the five children are flat
   siblings with no wrapper to turn into a right-hand column.
   Gated on BOTH orientation and a short viewport so a landscape tablet or desktop
   window keeps the centred portrait composition. */
+'@media (orientation:landscape) and (max-height:560px){'
+'.sf-np-body{padding:.9rem 1.5rem;gap:1.4rem;}'
+'.sf-np-stage{display:grid;grid-template-columns:auto minmax(0,1fr);'
+'grid-template-areas:"art meta" "art scrub" "art ctrl" "art tabs";'
+'align-items:center;column-gap:1.5rem;row-gap:.35rem;width:auto;max-width:none;}'
+'.sf-np-artwrap{grid-area:art;width:min(70vh,230px);margin-bottom:0;align-self:center;}'
+'.sf-np-meta{grid-area:meta;margin-bottom:0;}'
+'.sf-np-scrub{grid-area:scrub;}'
+'.sf-np-controls{grid-area:ctrl;justify-content:flex-start;}'
+'.sf-np-tabs{grid-area:tabs;margin-top:.2rem;justify-content:flex-start;}'
/* the cover must not eat the row it shares -- keep the float subtle when short */
+'.sf-np-art{animation-name:none;}'
+'.sf-np-panel{max-height:82vh;}'
+'}'
+'.sf-np-meta{width:100%;text-align:left;margin-bottom:1.1rem;}'
+'.sf-np-title{font-size:1.62rem;font-weight:700;color:#fff;line-height:1.2;'
+'overflow:hidden;text-overflow:ellipsis;white-space:nowrap;}'
+'.sf-np-artist{font-size:1.02rem;color:rgba(255,255,255,.62);margin-top:.2rem;'
+'overflow:hidden;text-overflow:ellipsis;white-space:nowrap;}'
+'.sf-np-album{margin-top:.55rem;border:0;border-radius:50px;padding:.34rem .85rem;'
+'background:rgba(255,255,255,.10);color:rgba(255,255,255,.72);font-size:.76rem;'
+'font-weight:600;cursor:pointer;backdrop-filter:blur(10px);}'
+'.sf-np-album:hover{background:rgba(255,255,255,.18);color:#fff;}'
/* ---- sf-mixes ---- */
/* ---- sf-music-solo ---- */
+'html.sf-music-solo .jf-mu-mainbar{display:none!important;}'
/* the library strip is now the primary header, so give it the presence one */
+'html.sf-music-solo .headerTabs .emby-tabs-slider{margin-top:2px;}'
+'.sf-home-btn{display:none;}'
+'html.sf-music-solo .sf-home-btn{display:inline-flex;align-items:center;justify-content:center;}'
+'.sf-mixrow .sectionTitleContainer{padding-left:3.3%;padding-right:3.3%;}'
+'.sf-mix-row{display:flex;gap:1.05rem;overflow-x:auto;padding:.2rem 3.3% 1.1rem;'
+'scrollbar-width:none;-webkit-overflow-scrolling:touch;}'
+'.sf-mix-row::-webkit-scrollbar{display:none;}'
+'.sf-mix-card{flex:0 0 auto;width:172px;cursor:pointer;}'
+'.sf-mix-grid{position:relative;width:172px;height:172px;border-radius:14px;overflow:hidden;'
+'display:grid;grid-template-columns:1fr 1fr;grid-template-rows:1fr 1fr;background:#161616;'
+'box-shadow:0 10px 26px rgba(0,0,0,.42);}'
+'.sf-mix-cell{background-size:cover;background-position:50% 50%;background-color:#1e1e1e;}'
+'.sf-mix-play{position:absolute;right:9px;bottom:9px;width:42px;height:42px;border:0;'
+'border-radius:50%;background:rgba(245,245,247,.95);color:#101010;cursor:pointer;'
+'display:flex;align-items:center;justify-content:center;opacity:0;transform:translateY(6px);'
+'transition:opacity .16s ease,transform .16s ease;box-shadow:0 6px 18px rgba(0,0,0,.45);}'
+'.sf-mix-card:hover .sf-mix-play,.sf-mix-card:focus-within .sf-mix-play{opacity:1;transform:translateY(0);}'
+'.sf-mix-play .material-icons{font-size:25px;}'
+'.sf-mix-label{margin-top:.55rem;font-size:1.02rem;font-weight:600;color:rgba(255,255,255,.86);'
+'overflow:hidden;text-overflow:ellipsis;white-space:nowrap;}'
+'.sf-mix-sub{font-size:.86rem;font-weight:200;color:rgba(255,255,255,.5);}'
/* touch has no hover, so the play affordance is always visible there */
/* sf-touch-affordance: on a phone there is no hover, so the play / menu controls
   on our music, audiobook and watchlist cards were permanently invisible AND
   pointer-events:none -- a tap could only open the detail page, never play. The
   mix cards already handled this; these did not. Reveal the CONTROLS only, not
   the dark scrim, so the artwork is still the card. */
+'@media (hover:none){'
/* display:none is what actually hid it -- the overlay is switched off wholesale
   under (hover:none), so opacity alone changed nothing (measured 0x0 box). */
+'.sf-ml-ov{display:block!important;opacity:1!important;pointer-events:none!important;background:none!important;}'
/* sf-mlcard-hover: this rule is what pinned the control ON. Gate it on hover so
   our rows behave like Jellyfin's, and keep it unconditional where there is no
   hover to gate on -- a phone would otherwise have no way to reach the menu. */
+'.sf-ml-ov .sf-ml-play,.sf-ml-ov .sf-ml-more,.sf-ml-ov .sf-ml-br{'
+'opacity:0;pointer-events:auto!important;'
+'transition:opacity .2s ease;}'
+'.sf-ml-card:hover .sf-ml-ov .sf-ml-play,.sf-ml-card:hover .sf-ml-ov .sf-ml-more,'
+'.sf-ml-card:hover .sf-ml-ov .sf-ml-br,'
+'.sf-ml-card:focus-within .sf-ml-ov .sf-ml-play,'
+'.sf-ml-card:focus-within .sf-ml-ov .sf-ml-more,'
+'.sf-ml-card:focus-within .sf-ml-ov .sf-ml-br{opacity:1;}'
+'@media (hover:none){.sf-ml-ov .sf-ml-play,.sf-ml-ov .sf-ml-more,'
+'.sf-ml-ov .sf-ml-br{opacity:1;}}'
+'}'
+'@media (hover:none){.sf-mix-play{opacity:1;transform:none;}}'

/* sf-home-skeleton: placeholder rows for the blank stretch while home loads.
   Every dimension below is MEASURED from a settled home page on this server
   (phone 16:9 card image 271x204 / poster 103x206; desktop 313x229 / 169x306),
   so the real rows land in the same place the placeholders occupied instead of
   shoving the page around. Sized off .layout-mobile/.layout-desktop rather than
   a width media query because Jellyfin picks its layout by DEVICE, not viewport. */
/* sf-skel-off (2026-08-29). The row skeleton is OFF.

   Measured on a cold load it appeared at y=208 -- on top of the hero, because
   the sections container has not been positioned yet -- and then travelled
   4,154px down the page as the real rows landed above it. That is visible,
   it is jank, and it was the thing being described as "the skeleton loads in
   higher and then jumps down".

   It was there for anti-FOUC, to stop the fold being blank while rows loaded.
   That reason is gone: sf-hero-reserve now guarantees the hero holds 90vh from
   the first paint, so the fold is never blank -- the hero is what fills it. An
   earlier A/B already measured display:none at 0.238 median CLS against 0.222
   for the 2-row skeleton, i.e. no real cost, and that was BEFORE the hero was
   reserved.

   Kept as a display:none rule rather than deleting the builder: the element
   still exists for anything that references it, but it never participates in
   layout, so it cannot move anything. Flip this one line to bring it back. */
+'.sf-skel{display:none!important;}'
/* sf-season-arrow: keep the season dropdown's arrow planted.
   The arrow is not an icon -- it is two background gradients on the <select>.
   The theme's hover rule uses the `background` SHORTHAND, which resets
   background-image to none, so hovering ERASED the arrow, and `transition:
   background .2s` faded it out. Measured idle vs hover: identical rect, but
   bgImage went from the two gradients to `none`. Re-declare the arrow so the
   shorthand cannot win, and narrow the transition to background-COLOR so the
   hover tint still animates and the arrow never does. */
+'.sf-season-select{'
+'background-image:linear-gradient(45deg,rgba(0,0,0,0) 50%,rgba(235,235,240,.75) 50%),'
+'linear-gradient(135deg,rgba(235,235,240,.75) 50%,rgba(0,0,0,0) 50%)!important;'
+'background-position:calc(100% - 12px) 50%,calc(100% - 6px) 50%!important;'
+'background-size:6px 6px,6px 6px!important;'
+'background-repeat:no-repeat,no-repeat!important;'
+'transition:background-color .2s!important;}'
+'.sf-season-select:hover,.sf-season-select:focus{'
+'background-color:rgba(255,255,255,.1)!important;}'
/* sf-hdr-nocast: take the cast button out of the header.
   NOT display:none. The capsule's own cast control works by clicking this
   element (see sf-capsule-extras), and Jellyfin skips a click on a display:none
   control -- the same trap that made sf-cardplay a no-op. Zero-size it and drop
   its opacity instead: it takes no space and cannot be seen or tabbed to, but a
   programmatic .click() still reaches it, so casting from the now-playing bar
   keeps working. */
+'.headerCastButton{opacity:0!important;pointer-events:none!important;'
+'width:0!important;min-width:0!important;max-width:0!important;'
+'padding:0!important;margin:0!important;border:0!important;overflow:hidden!important;}'
+'.sf-skel-off{display:flex;flex-direction:column;order:9999;pointer-events:none;'
+'-webkit-user-select:none;user-select:none;}'
+'.sf-skel-row{padding:0 7px;}'
+'.sf-skel-hd{border-radius:6px;width:38%;max-width:240px;margin-left:3px;}'
+'.sf-skel-strip{display:flex;overflow:hidden;}'
+'.sf-skel-card{flex:0 0 auto;}'
+'.sf-skel-img{border-radius:12px;}'
+'.sf-skel-tx{height:9px;width:68%;border-radius:5px;margin-top:6px;}'
/* one shimmer definition, reused: a soft base tone so the shape reads even with
   animation suppressed, plus a highlight that sweeps across it */
/* sf-dskel: an album/playlist/book page shows a BARE SPINNER and nothing else
   for its first ~2s -- measured at 600ms and 1200ms into a cold playlist load:
   21 spinners, no title, no artwork, no play button -- and then the whole stage
   appears at once. (An audit reported ~25s here; that does not reproduce, median
   is 2.7s over repeated cold loads. The 25s was measured while the nightly
   backup, ugscan and a batch of ffprobes were saturating the box.) Give the page
   its shape immediately so nothing "spawns in". */
+'.sf-dskel{display:flex;gap:1.6rem;padding:2.2rem 3vw 1rem;pointer-events:none;'+'position:fixed;left:0;right:0;top:calc(var(--sf-hdr,7rem));z-index:1;}'
+'.sf-dskel-art{flex:0 0 auto;width:min(232px,26vw);aspect-ratio:1/1;border-radius:14px;}'
+'.sf-dskel-meta{flex:1 1 auto;display:flex;flex-direction:column;justify-content:flex-end;'
+'padding-bottom:.6rem;max-width:620px;}'
+'.sf-dskel-t{height:30px;width:46%;min-width:160px;border-radius:7px;}'
+'.sf-dskel-s{height:13px;width:28%;min-width:110px;border-radius:6px;margin-top:.85rem;}'
+'.sf-dskel-btns{display:flex;gap:.7rem;margin-top:1.5rem;}'
+'.sf-dskel-b{height:40px;width:116px;border-radius:50px;}'
+'.sf-dskel-b2{height:40px;width:116px;border-radius:50px;opacity:.6;}'
+'@media (max-width:820px){.sf-dskel{flex-direction:column;align-items:center;padding-top:3.4rem;}'
+'.sf-dskel-art{width:min(260px,58vw);} .sf-dskel-meta{align-items:center;max-width:none;}}'
/* sf-leaving: a title about to be rotated out gets a countdown, so a silent
   deletion becomes a choice -- favourite it or add it to your Watchlist and
   both rotation jobs keep it for good. Amber, not red: this is information,
   not an error. */
+'.sf-leave-badge{position:absolute;left:8px;bottom:8px;z-index:3;'
+'background:rgba(224,164,76,.92);color:#1a1206;font-size:11px;font-weight:700;'
+'letter-spacing:.02em;padding:3px 7px;border-radius:5px;pointer-events:none;'
+'box-shadow:0 2px 8px rgba(0,0,0,.45);font-variant-numeric:tabular-nums;}'
+'.sf-leavingrow .sf-ml-poster{position:relative;}'
/* sf-leave-fav: styled to match Jellyfin's OWN card overlay buttons, measured
   off a Trending Movies card rather than guessed:
       button  transparent, no radius, no shadow, rgba(255,255,255,.8)
       icon    21.86px, rgba(255,255,255,.76)
   The first version was a dark rounded chip, which read as a bolted-on control
   between two rows of native ones.

   One deliberate difference: Jellyfin's overlay buttons are hover-only
   (.cardOverlayButton-hover). This one is always visible, because it is the
   whole point of the row -- a save button you have to discover by hovering is
   no use on a phone, where most of these get seen. A drop shadow keeps a white
   glyph legible on a pale poster, which the native hover scrim would otherwise
   have handled. */
+'.sf-leave-fav{position:absolute;right:4px;bottom:4px;z-index:4;'
+'border:0;background:none;padding:6px;margin:0;cursor:pointer;'
+'display:flex;align-items:center;justify-content:center;'
+'color:rgba(255,255,255,.76);border-radius:12px;opacity:.92;'
+'transition:opacity .15s ease,transform .12s ease;}'
+'.sf-leave-fav:hover{opacity:1;transform:scale(1.12);}'
+'.sf-leave-fav .material-icons{font-size:21.862px;line-height:1;'
+'filter:drop-shadow(0 1px 3px rgba(0,0,0,.75));}'
+'.sf-leave-fav.sf-on{color:#fff;opacity:1;}'
+'.sf-ml-card.sf-leave-kept .sf-leave-badge{background:rgba(96,176,116,.94);}'
/* sf-leave-typography: match the card text to the rows either side of it.
   Measured against the Watchlist row, whose cards use Jellyfin's own
   .cardText treatment under Abyss:
       title  17.86px / 600 / rgba(255,255,255,.8)
       sub    16.00px / 200 / rgba(255,255,255,.5)
   this row was rendering both at 14.88px / 400, so it read as a foreign
   component sitting between two native ones. Expressed in em against the
   card's own 14.88px so it tracks Jellyfin's breakpoints instead of pinning
   pixel sizes that only happen to be right on a desktop. */
+'.sf-leavingrow .sf-ml-title{font-size:1.2em;font-weight:600;'
+'color:rgba(255,255,255,.8);letter-spacing:0;}'
+'.sf-leavingrow .sf-ml-sub{display:none;}'
/* Sits on the heading baseline, quieter than the title so it reads as a caption
   rather than a second heading. Hidden on a phone, where the row title already
   fills the width and the countdown badge carries the meaning. */
/* em here resolves against .sectionTitleContainer (~14.9px), NOT the h2, so
   .62em rendered at 9px -- unreadable. .92em puts it just under the card
   text, which is where a caption belongs. */
+'.sf-leave-hint{margin-left:.75em;font-size:.92em;font-weight:200;'
+'color:rgba(255,255,255,.5);letter-spacing:.01em;white-space:nowrap;'
+'display:inline-flex;align-items:center;gap:.35em;align-self:center;}'
+'.sf-leave-hint-i{font-size:1.15em;line-height:1;color:rgba(255,255,255,.76);}'
+'@media (max-width:640px){.sf-leave-hint{display:none;}}'
+'.sf-skel-sh{background-color:rgba(150,156,172,.30);'
+'background-image:linear-gradient(90deg,rgba(255,255,255,0) 0,rgba(255,255,255,.16) 50%,rgba(255,255,255,0) 100%);'
+'background-repeat:no-repeat;background-size:60% 100%;background-position:-150% 0;'
+'animation:sf-skel-wave 1.5s linear infinite;}'
+'@keyframes sf-skel-wave{to{background-position:250% 0;}}'
/* a shimmer is decorative -- never animate it for someone who asked for less motion */
+'@media (prefers-reduced-motion:reduce){.sf-skel-sh{animation:none;}}'
/* Sized by VIEWPORT WIDTH, not .layout-mobile/.layout-desktop. Measured: at the
   moment the skeleton paints the root is still 'preload layout-desktop' even on a
   412px phone, so keying off that class rendered 313x229 desktop cards on a phone.
   The layout class is not settled this early; the viewport always is. */
/* The hero band is the biggest empty area on a cold home page: it is reserved
   from the start (rows begin at y=621) but Media Bar does not paint into it for
   ~7s. Absolutely positioned so it occupies the band WITHOUT adding height --
   verified by checking the rows' y-offset is identical with and without it. */
+'.sf-skel-anchor{position:relative;}'
+'.sf-skel-hero{position:absolute;left:0;right:0;top:0;pointer-events:none;z-index:3;'
+'display:flex;flex-direction:column;justify-content:flex-end;padding:0 7px 26px;}'
+'.sf-skel-hero .sf-skel-htitle{width:58%;max-width:340px;height:30px;border-radius:8px;margin-bottom:14px;}'
+'.sf-skel-hero .sf-skel-hmeta{width:34%;max-width:190px;height:13px;border-radius:6px;margin-bottom:20px;}'
+'.sf-skel-hero .sf-skel-hbtns{display:flex;}'
+'.sf-skel-hero .sf-skel-hbtn{width:124px;height:40px;border-radius:20px;margin-right:12px;}'
+'.sf-skel-hero .sf-skel-hbtn.sf-skel-hbtn2{width:44px;}'
+'@media (max-width:820px){'
+'.sf-skel-hero{padding-bottom:18px;}'
+'.sf-skel-hero .sf-skel-htitle{height:24px;margin-bottom:11px;}'
+'.sf-skel-hero .sf-skel-hbtn{width:104px;height:36px;border-radius:18px;}'
+'}'
+'.sf-skel-hd{height:23px;margin-top:18px;margin-bottom:17px;}'
+'.sf-skel-card{margin-right:27px;}'
+'.sf-skel-wide .sf-skel-img{width:313px;height:229px;}'
+'.sf-skel-tall .sf-skel-img{width:169px;height:306px;}'
+'@media (max-width:820px){'
+'.sf-skel-hd{height:18px;margin-top:15px;margin-bottom:15px;}'
+'.sf-skel-card{margin-right:26px;}'
+'.sf-skel-wide .sf-skel-img{width:271px;height:204px;}'
+'.sf-skel-tall .sf-skel-img{width:103px;height:206px;}'
+'}'
+'@media (max-width:820px){.sf-mix-card{width:142px;}.sf-mix-grid{width:142px;height:142px;}}'
/* sf-synopsis: the book blurb on the detail page, clamped with a real control. */
/* ---- sf-alb: album stage ------------------------------------------------
   The cover is the subject; everything else defers to it. The ambient ground is
   the SAME image blurred, so the page takes its colour from the record without
   a second request or any colour-extraction work on the main thread. */
/* sf-abcard: the author line, and the series number on the cover */
/* a record with no artwork still deserves a tile, not a hole */
+'.sf-ml-poster.sf-ml-noart{position:relative;'
+'background-image:linear-gradient(145deg,rgba(255,255,255,.13),rgba(255,255,255,.04));}'
+'.sf-ml-poster.sf-ml-noart::after{content:"\\266a";position:absolute;inset:0;'
+'display:flex;align-items:center;justify-content:center;'
+'font-size:2.1rem;opacity:.30;color:#fff;}'
/* sf-abrow-title: the title is a way IN to the book, so it looks like one */
/* sf-abtitle-any: a bare 25px line of text is not a touch target. Padding gives
   the two lines together a comfortable area without changing how the card looks. */
+'.sf-ab-titlelink{cursor:pointer;padding:.22em .1em;margin:-.22em -.1em;'
+'border-radius:6px;}'
+'.sf-ab-titlelink:active{background:rgba(255,255,255,.10);}'
+'.sf-ab-titlelink:hover{text-decoration:underline;text-underline-offset:2px;}'
/* sf-ablib: shelves on the Audiobooks page */
+'.sf-ablib{margin:0 0 .6em;}'
+'.sf-ablib-shelf{margin-bottom:1.5em;}'
+'.sf-ablib-count{margin-left:.7em;font-size:.78rem;opacity:.45;font-weight:600;}'
+'.sf-ablib-allhead{margin:.4em 0 .2em;}'
/* On a bookshelf the TITLE is what you read, and a single clipped line
   ("Dungeon Cr...", "Harry Potter...") tells you nothing when eight books share
   a prefix. Two lines, then clamp. */
/* `.sf-ml-card .cardText{white-space:nowrap}` is (0,2,0) and so was
   `.sf-ablib .cardText-first` -- a TIE, decided by source order, which the other
   rule won. One more class makes it (0,3,0) and no !important is needed. */
+'.sf-ablib .sf-ml-card .cardText-first{white-space:normal;display:-webkit-box;'
+'-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden;'
+'line-height:1.25;max-height:2.5em;}'
+'.sf-ablib .sf-ml-card .cardText-secondary{white-space:nowrap;overflow:hidden;'
+'text-overflow:ellipsis;}'
/* sf-fresh: the refresh offer, when an automatic one would interrupt something */
+'.sf-fresh-pill{position:fixed;left:50%;transform:translateX(-50%);bottom:calc(env(safe-area-inset-bottom,0px) + 92px);'
+'z-index:100000;border:0;cursor:pointer;font:inherit;font-weight:650;font-size:.88rem;'
+'padding:.7em 1.2em;border-radius:50px;color:#111;background:#fff;'
+'box-shadow:0 8px 26px rgba(0,0,0,.45);}'
+'.sf-fresh-pill:active{transform:translateX(-50%) scale(.97);}'
+'.sf-abc-author{opacity:.62;font-weight:500;}'
+'.sf-abc-left{opacity:.82;font-weight:650;font-variant-numeric:tabular-nums;}'
+'.sf-abc-num{position:absolute;left:8px;top:8px;z-index:3;pointer-events:none;'
+'min-width:22px;height:22px;padding:0 6px;border-radius:11px;'
+'display:flex;align-items:center;justify-content:center;'
+'font-size:.74rem;font-weight:800;font-variant-numeric:tabular-nums;'
+'color:#0d0d0d;background:rgba(255,255,255,.92);'
+'box-shadow:0 2px 8px rgba(0,0,0,.45);}'
+'.sf-alb-hero{position:relative;isolation:isolate;overflow:hidden;'
+'margin:0 0 .4em;padding:clamp(1.4rem,5vw,2.6rem) clamp(1rem,4vw,2.6rem) clamp(1.2rem,3.5vw,2rem);'
/* reserved before the artwork decodes -- a hero that grows late is what makes
   taps land on the wrong row (see sf-heroslot) */
+'min-height:330px;}'
+'.sf-alb-bg{position:absolute;inset:-18%;z-index:0;background-size:cover;'
+'background-position:50% 50%;filter:blur(58px) saturate(165%);opacity:.62;'
+'transform:translateZ(0);}'
+'.sf-alb-scrim{position:absolute;inset:0;z-index:1;pointer-events:none;'
+'background:linear-gradient(180deg,rgba(10,10,12,.30) 0%,rgba(10,10,12,.62) 62%,rgba(10,10,12,.93) 100%);}'
+'.sf-alb-in{position:relative;z-index:2;display:flex;flex-direction:column;'
+'align-items:center;text-align:center;gap:1.15rem;}'
/* the artwork: square, lifted off the page */
/* Audiobook art is SQUARE -- it is embedded in the m4b. Forcing a 2/3 portrait
   box cropped the author's name off the top of every cover. */
+'.sf-alb-hero.sf-alb-book .sf-alb-art{border-radius:10px;}'
/* an artist is a portrait, so it gets the round frame the Top Artists row uses */
+'.sf-alb-hero.sf-alb-artistpg .sf-alb-art{border-radius:50%;width:min(190px,44vw);'
+'box-shadow:0 20px 44px rgba(0,0,0,.58);}'
+'.sf-alb-hero.sf-alb-artistpg{min-height:352px;}'
/* An artist's albums arrived stacked one per row, which turned a two-record
   discography into two screens of scrolling. A grid shows the shelf at a glance. */
+'#itemDetailPage.sf-alb-on-artist .detailPagePrimaryContent .itemsContainer{'
+'display:grid!important;grid-template-columns:repeat(auto-fill,minmax(132px,1fr));'
+'gap:1.1rem .9rem;}'
+'#itemDetailPage.sf-alb-on-artist .detailPagePrimaryContent .card{width:auto!important;'
+'margin:0!important;padding:0!important;}'
+'@media (min-width:900px){'
+'#itemDetailPage.sf-alb-on-artist .detailPagePrimaryContent .itemsContainer{'
+'grid-template-columns:repeat(auto-fill,minmax(168px,1fr));}'
+'}'
/* a playlist is a stack of records */
+'.sf-alb-hero.sf-alb-listpg .sf-alb-art{border-radius:12px;}'
+'.sf-alb-hero.sf-alb-book{min-height:376px;}'
+'.sf-alb-art{width:min(232px,52vw);aspect-ratio:1/1;border-radius:14px;'
+'background-size:cover;background-position:50% 50%;background-color:rgba(255,255,255,.05);'
+'box-shadow:0 26px 54px rgba(0,0,0,.62),0 3px 10px rgba(0,0,0,.45);'
+'flex:0 0 auto;}'
+'.sf-alb-meta{display:flex;flex-direction:column;align-items:center;gap:.5rem;width:100%;}'
+'.sf-alb-title{font-size:clamp(1.55rem,5.6vw,2.15rem);font-weight:800;line-height:1.12;'
+'letter-spacing:-.02em;color:#fff;text-wrap:balance;'
+'text-shadow:0 2px 14px rgba(0,0,0,.5);max-width:22ch;}'
+'.sf-alb-artist{border:0;background:transparent;padding:0;font:inherit;cursor:pointer;'
+'font-size:1.02rem;font-weight:600;color:rgba(255,255,255,.82);letter-spacing:.01em;}'
+'.sf-alb-artist:hover:not(:disabled){color:#fff;text-decoration:underline;}'
+'.sf-alb-artist:disabled{cursor:default;}'
+'.sf-alb-chips{display:flex;flex-wrap:wrap;justify-content:center;gap:.4rem;margin-top:.1rem;}'
+'.sf-alb-chip{font-size:.76rem;font-weight:600;letter-spacing:.02em;'
+'padding:.24em .66em;border-radius:50px;color:rgba(255,255,255,.78);'
+'background:rgba(255,255,255,.13);backdrop-filter:blur(6px);}'
+'.sf-alb-acts{display:flex;gap:.6rem;margin-top:.55rem;flex-wrap:wrap;justify-content:center;}'
+'.sf-alb-prog{width:100%;max-width:420px;margin-top:.75rem;}'
+'.sf-alb-progbar{height:4px;border-radius:2px;background:rgba(255,255,255,.20);overflow:hidden;}'
+'.sf-alb-progbar span{display:block;height:100%;border-radius:2px;background:rgba(255,255,255,.92);}'
+'.sf-alb-proglab{margin-top:.38rem;font-size:.78rem;font-weight:600;color:rgba(255,255,255,.62);}'
+'.sf-alb-desc{margin:.9rem 0 0;max-width:62ch;font-size:.95rem;line-height:1.55;'
+'color:rgba(255,255,255,.72);display:-webkit-box;-webkit-box-orient:vertical;'
+'-webkit-line-clamp:3;overflow:hidden;cursor:pointer;}'
+'.sf-alb-desc.sf-alb-desc-open{-webkit-line-clamp:unset;overflow:visible;}'
+'.sf-alb-hero.sf-alb-book .sf-alb-bg{filter:blur(58px) saturate(85%) brightness(.70);'
+'opacity:.5;}'
+'.sf-alb-play,.sf-alb-shuffle{display:inline-flex;align-items:center;gap:.4em;'
+'border:0;cursor:pointer;font:inherit;font-weight:700;font-size:.97rem;'
+'padding:.72em 1.5em;border-radius:50px;min-height:46px;}'
+'.sf-alb-play{background:#fff;color:#111;box-shadow:0 6px 18px rgba(0,0,0,.35);}'
+'.sf-alb-shuffle{background:rgba(255,255,255,.16);color:#fff;'
+'box-shadow:inset 0 0 0 1px rgba(255,255,255,.20);}'
+'.sf-alb-play .material-icons,.sf-alb-shuffle .material-icons{font-size:21px;}'
+'.sf-alb-play:active,.sf-alb-shuffle:active{transform:scale(.97);}'
/* the native artist backdrop and the duplicate title/chips/buttons are replaced
   by the stage, so hide them rather than stack two headers */
+'#itemDetailPage.sf-alb-on .itemBackdrop,'
+'#itemDetailPage.sf-alb-on .detailRibbon,'
+'#itemDetailPage.sf-alb-on .mainDetailButtons{display:none!important;}'
/* Selectors here are ID-based on purpose: sf-atv's own rules are
   `#itemDetailPage.sf-atv ...` at specificity (1,2,0), so a class-only override
   LOSES even with !important. */
+'#itemDetailPage.sf-alb-on .detailPagePrimaryContent{padding:0 clamp(.6rem,3vw,2rem);}'
/* and give the rows a rhythm worth reading */
+'#itemDetailPage.sf-alb-on .listItem{border-radius:11px;padding:.15em .3em;'
+'min-height:56px;transition:background .13s ease-out;}'
+'#itemDetailPage.sf-alb-on .listItem:hover{background:rgba(255,255,255,.07);}'
+'#itemDetailPage.sf-alb-on .listItem:active{background:rgba(255,255,255,.12);}'
+'#itemDetailPage.sf-alb-on .listItemBody{padding:.35em .5em;}'
+'#itemDetailPage.sf-alb-on .listItem .listItemIndexNumber{opacity:.42;min-width:1.9em;'
+'text-align:right;font-variant-numeric:tabular-nums;}'
+'#itemDetailPage.sf-alb-on .listItem .secondary{opacity:.55;}'
/* sf-atv reserves 357px of padding-top for the backdrop hero. With the backdrop
   replaced by the stage that padding is a 357px hole above the artwork -- give
   it back, or the cover starts halfway down the screen. */
+'#itemDetailPage.sf-alb-on .detailPageWrapperContainer{padding-top:0!important;}'
/* wider screens: cover beside the words, the way a record sleeve sits on a shelf */
/* Wide screens -- a Steam Deck is 1280x800, and so is a small laptop.
   Measured there before this: the hero content sat in the left 550px with ~700px
   of empty gradient beside it, and a track row stretched the full 1280 so the
   duration landed a thousand pixels from the title. Both reference apps hold
   their content to a readable column instead of filling the glass. */
+'@media (min-width:900px){'
+'.sf-alb-in{max-width:1080px;margin-left:auto;margin-right:auto;}'
+'#itemDetailPage.sf-alb-on .detailPagePrimaryContent{max-width:1080px;'
+'margin-left:auto!important;margin-right:auto!important;}'
+'#itemDetailPage.sf-alb-on .listItem{padding-left:.6em;padding-right:.6em;}'
+'}'
+'@media (min-width:900px){'
+'.sf-alb-in{flex-direction:row;align-items:flex-end;text-align:left;gap:2rem;}'
+'.sf-alb-art{width:248px;}'
+'.sf-alb-meta{align-items:flex-start;}'
+'.sf-alb-title{max-width:18ch;}'
+'.sf-alb-chips{justify-content:flex-start;}'
+'.sf-alb-acts{justify-content:flex-start;}'
+'.sf-alb-hero{min-height:360px;}'
+'}'
/* Short-and-wide screens: a Steam Deck is 800px tall, and the hero was taking
   425px of that -- over half the screen before a single track. Shrink it there
   so the content you came for is on screen without scrolling. Keyed on HEIGHT,
   so a tall desktop monitor keeps the full-size hero. */
+'@media (min-width:900px) and (max-height:860px){'
+'.sf-alb-hero{min-height:286px;padding-top:1.3rem;padding-bottom:1.1rem;}'
+'.sf-alb-art{width:184px;}'
+'.sf-alb-hero.sf-alb-artistpg .sf-alb-art{width:150px;}'
+'.sf-alb-hero.sf-alb-artistpg,.sf-alb-hero.sf-alb-book{min-height:286px;}'
+'}'
+'@media (prefers-reduced-motion:reduce){'
+'.sf-alb-play:active,.sf-alb-shuffle:active{transform:none;}'
+'}'
+'.sf-synopsis{margin:.2em 0 1.4em;max-width:60em;}'
+'.sf-syn-text{white-space:pre-wrap;line-height:1.62;opacity:.86;font-size:1.02em;'
+'display:-webkit-box;-webkit-line-clamp:4;-webkit-box-orient:vertical;overflow:hidden;}'
+'.sf-synopsis.sf-syn-open .sf-syn-text{-webkit-line-clamp:unset;overflow:visible;}'
+'.sf-syn-more{margin-top:.45em;border:0;background:transparent;padding:.2em 0;'
+'font:inherit;font-weight:650;font-size:.92em;cursor:pointer;'
+'color:rgba(var(--abyss-accent),1);opacity:.95;}'
+'.sf-syn-more:hover{text-decoration:underline;}'
+'@media (max-width:700px){.sf-syn-text{font-size:.97em;}}'
+'.sf-np-scrub{width:100%;}'
+'.sf-np-range{width:100%;-webkit-appearance:none;appearance:none;height:6px;border-radius:6px;'
+'background:rgba(255,255,255,.22);outline:0;cursor:pointer;}'
+'.sf-np-range::-webkit-slider-thumb{-webkit-appearance:none;width:14px;height:14px;'
+'border-radius:50%;background:#fff;box-shadow:0 2px 8px rgba(0,0,0,.5);}'
+'.sf-np-times{display:flex;justify-content:space-between;font-size:.78rem;'
+'color:rgba(255,255,255,.55);margin-top:.42rem;font-variant-numeric:tabular-nums;}'
+'.sf-np-controls{display:flex;align-items:center;justify-content:center;gap:.9rem;'
+'margin-top:1.1rem;}'
+'.sf-np-b{border:0;background:transparent;color:rgba(255,255,255,.82);cursor:pointer;'
+'width:52px;height:52px;border-radius:50%;display:flex;align-items:center;justify-content:center;}'
+'.sf-np-b:hover{background:rgba(255,255,255,.10);color:#fff;}'
+'.sf-np-b .material-icons{font-size:29px;}'
/* the one accented control, same idea as the dominant-colour play button */
+'.sf-np-play{width:70px;height:70px;background:#fff;color:#101010;}'
+'.sf-np-play:hover{background:#fff;color:#101010;transform:scale(1.04);}'
+'.sf-np-play .material-icons{font-size:37px;}'
+'.sf-np-tabs{display:flex;gap:.6rem;margin-top:1.4rem;}'
+'.sf-np-tab{border:0;border-radius:50px;padding:.5rem 1.15rem;cursor:pointer;'
+'font-size:.86rem;font-weight:600;background:rgba(255,255,255,.10);color:rgba(255,255,255,.75);'
+'backdrop-filter:blur(12px);}'
+'.sf-np-tab:hover{background:rgba(255,255,255,.17);color:#fff;}'
+'.sf-np-tab.sf-np-on{background:#f5f5f7;color:#121212;}'
+'.sf-np-panel{width:min(420px,42vw);max-height:78vh;overflow-y:auto;display:none;'
+'background:rgba(255,255,255,.07);border-radius:20px;padding:1.3rem;'
+'backdrop-filter:blur(22px);border:1px solid rgba(255,255,255,.08);}'
+'.sf-np.sf-np-haspanel .sf-np-panel{display:block;}'
/* ---- sf-np-panels ---- synced lyrics + real queue */
+'.sf-np-lyrpane{scroll-behavior:smooth;}'
+'.sf-np-lyrbox{padding:1.2rem .2rem 45vh;}'
/* sf-np-flyr (2026-08-24): fullscreen lyrics (sf-flyr) existed but was reachable
   ONLY from the desktop side panel's header button (.sf-lyrics-full inside
   .sf-lyrics-hd). On a phone the lyrics live in the now-playing overlay's Lyrics
   TAB instead -- a different surface entirely -- so the feature was invisible on
   mobile. This is the same affordance, placed where the mobile lyrics actually
   are. Pinned to the pane (not scrolled with the text) so it stays reachable
   while the lyrics move, and kept clear of the right edge where a thumb rests. */
+'.sf-np-lyrpane{position:relative;}'
+'.sf-np-flyr{position:sticky;top:.35rem;float:right;margin:0 .35rem 0 0;z-index:4;'
+'width:34px;height:34px;border:0;border-radius:50%;cursor:pointer;'
+'display:flex;align-items:center;justify-content:center;'
+'background:rgba(20,20,24,.62);backdrop-filter:blur(14px) saturate(160%);'
+'-webkit-backdrop-filter:blur(14px) saturate(160%);'
+'box-shadow:0 0 0 1px rgba(255,255,255,.10);}'
+'.sf-np-flyr .material-icons{font-size:19px;color:rgba(255,255,255,.92);}'
+'.sf-np-flyr:active{transform:scale(.93);}'
/* the lines start dim and only the current one is fully lit -- the falloff is
   what makes a lyric sheet readable while it moves */
+'.sf-np-lyr{font-size:1.12rem;line-height:1.62;font-weight:600;padding:.16rem 0;'
+'color:rgba(255,255,255,.34);transition:color .28s ease,opacity .28s ease,transform .28s ease;'
+'transform-origin:left center;}'
+'.sf-np-lyr-blank{height:.7rem;}'
+'.sf-np-on{color:#fff;transform:scale(1.03);}'
+'.sf-np-d1{color:rgba(255,255,255,.56);}'
+'.sf-np-d2{color:rgba(255,255,255,.28);}'
+'.sf-np-lyr-seek .sf-np-lyr{cursor:pointer;}'
+'.sf-np-lyr-seek .sf-np-lyr:hover{color:rgba(255,255,255,.85);}'
/* queue rows: art, title/artist, duration -- the shape every music app uses */
+'.sf-np-qrow{display:flex;align-items:center;gap:.7rem;padding:.42rem .5rem;'
+'border-radius:10px;cursor:pointer;transition:background .15s ease;}'
+'.sf-np-qrow:hover{background:rgba(255,255,255,.09);}'
+'.sf-np-qrow-on{background:rgba(255,255,255,.13);}'
+'.sf-np-qart{width:38px;height:38px;flex:0 0 auto;border-radius:6px;background:#222;'
+'background-size:cover;background-position:50% 50%;}'
+'.sf-np-qmeta{flex:1 1 auto;min-width:0;}'
+'.sf-np-qt{font-size:.92rem;color:rgba(255,255,255,.88);overflow:hidden;'
+'text-overflow:ellipsis;white-space:nowrap;}'
+'.sf-np-qrow-on .sf-np-qt{font-weight:700;color:#fff;}'
+'.sf-np-qa{font-size:.78rem;color:rgba(255,255,255,.5);overflow:hidden;'
+'text-overflow:ellipsis;white-space:nowrap;}'
+'.sf-np-qd{font-size:.78rem;color:rgba(255,255,255,.45);flex:0 0 auto;'
+'font-variant-numeric:tabular-nums;}'
+'.sf-np-empty{color:rgba(255,255,255,.5);font-size:.92rem;text-align:center;padding:1.6rem 0;}'
/* placeholder rows mirror .sf-np-qrow geometry exactly, so the real rows drop
   in without moving anything */
+'.sf-np-qskel{display:flex;align-items:center;gap:.7rem;padding:.42rem .5rem;}'
+'.sf-np-qskel i{display:block;background:rgba(255,255,255,.085);border-radius:5px;'
+'animation:sfNpSk 1.25s ease-in-out infinite;}'
+'.sf-np-qsa{width:38px;height:38px;flex:0 0 auto;border-radius:6px;}'
+'.sf-np-qsm{flex:1 1 auto;min-width:0;display:flex;flex-direction:column;gap:.34rem;}'
+'.sf-np-qs1{width:62%;height:11px;}.sf-np-qs2{width:38%;height:9px;opacity:.7;}'
+'@keyframes sfNpSk{0%,100%{opacity:.5;}50%{opacity:1;}}'
+'@media (prefers-reduced-motion: reduce){.sf-np-qskel i{animation:none;}}'
/* the capsule is redundant while the full player is open, and it floated ON TOP of it */
+'html.sf-np-lock .nowPlayingBar{opacity:0!important;pointer-events:none!important;}'
/* .appfooter paints its own frosted background behind the capsule, so hiding
   only the bar left an empty pill floating at the bottom of the player */
+'html.sf-np-lock .appfooter{opacity:0!important;pointer-events:none!important;}'
+'.sf-np-row{display:flex;align-items:center;gap:.8rem;padding:.5rem .6rem;border-radius:10px;'
+'color:rgba(255,255,255,.78);font-size:.92rem;}'
+'.sf-np-row-on{background:rgba(255,255,255,.12);color:#fff;font-weight:600;}'
+'.sf-np-n{width:1.5rem;text-align:right;opacity:.55;font-variant-numeric:tabular-nums;flex:0 0 auto;}'
+'.sf-np-t{flex:1 1 auto;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;}'
+'.sf-np-d{opacity:.5;font-variant-numeric:tabular-nums;flex:0 0 auto;}'
+'.sf-np-lyrics{color:rgba(255,255,255,.8);line-height:1.85;font-size:1rem;}'
/* phone: one column, artwork smaller, panel takes the full width under it */
+'@media (max-width:820px){'
+'.sf-np-body{flex-direction:column;justify-content:flex-start;gap:1.1rem;padding:3.6rem 1.15rem 1.4rem;overflow-y:auto;}'
+'.sf-np-artwrap{width:min(300px,58vw);margin-bottom:1.2rem;}'
+'.sf-np-stage{width:100%;max-width:none;}'
+'.sf-np-title{font-size:1.35rem;}'
+'.sf-np-panel{width:100%;max-height:none;}'
+'.sf-np-b{width:48px;height:48px;}.sf-np-play{width:64px;height:64px;}'
/* even with the tabs correctly outside it, audiobook mode injects 4 extra
   buttons here -- never let the row spill off the phone again */
+'.sf-np-controls{max-width:100%;flex-wrap:wrap;row-gap:.5rem;gap:.55rem;}'
+'}'
/* honour a reduced-motion preference: keep the colour, drop the drift */
+'@media (prefers-reduced-motion: reduce){'
+'.sf-np-tint,.sf-np-art{animation:none;}'
+'}';
var st=document.createElement('style');st.textContent=css;document.head.appendChild(st);

var CATEGORY_ICONS={'Motorsport':'🏁','Racing':'🏁','Soccer':'⚽','Basketball':'🏀','Football':'🏈','Combat Sports':'🥊','Baseball':'⚾'};
function iconFor(cat){return CATEGORY_ICONS[cat]||'🏆';}
function normName(n){return String(n||'').toLowerCase().replace(/[^a-z0-9]+/g,' ').trim();}
function esc(s){return String(s==null?'':s);}

function dedupe(list){
var seen={},out=[];
list.forEach(function(c){var key=normName(c.name);if(seen[key])return;seen[key]=true;out.push(c);});
return out;
}

function formatStart(ms){
if(!ms)return '';
var d=new Date(ms);
var h=d.getHours(),m=d.getMinutes();
var ap=h>=12?'PM':'AM';var h12=h%12||12;
return h12+':'+(m<10?'0':'')+m+' '+ap;
}

/* Jellyfin's LiveTvChannel API drops the M3U group-title entirely, so the
   bridge's own /channels.json (category, description, upcoming games) is
   joined here with Jellyfin's channel list (item id, for playback) by
   channel NUMBER -- both sides compute the same number from the same
   assignNumbers() logic, so they line up 1:1.
   The bridge is fetched via its HTTPS reverse-proxy hostname
   (your-jellyfin-host.example -> YOUR_SERVER_IP:8095 in Nginx Proxy
   Manager), NOT the raw LAN IP directly -- fetching a plain-http LAN address
   from this https:// page worked on desktop Chrome/Brave but was blocked as
   mixed content on mobile browsers, and wasn't reachable at all off the home
   network regardless. Routing through the same domain/TLS Jellyfin itself
   uses fixes both. */
async function fetchData(){
var creds=JSON.parse(localStorage.getItem('jellyfin_credentials'));
var server=creds.Servers[0];
var token=server.AccessToken,userId=server.UserId,base=server.ManualAddress||server.LocalAddress;
var _bu=(window.SF_CONFIG&&window.SF_CONFIG.sportsBridgeUrl)||'';
var bridgeP=_bu?fetch(_bu).then(function(r){return r.json();}):Promise.resolve({channels:[]});
var jfP=fetch(base+'/LiveTv/Channels?userId='+userId+'&EnableImages=true&AddCurrentProgram=true',{headers:{'X-Emby-Token':token}}).then(function(r){return r.json();});
var results=await Promise.all([bridgeP,jfP]);
var bridgeData=results[0],jfData=results[1];
var byNum={};
(jfData.Items||[]).forEach(function(c){byNum[String(c.Number)]=c;});
return {channels:bridgeData.channels||[],byNum:byNum,serverId:server.Id};
}

function goToChannel(jfItem,serverId){
if(!jfItem)return;
location.hash='#/details?id='+jfItem.Id+'&serverId='+serverId;
var tries=0;
var iv=setInterval(function(){
tries++;
var btn=document.querySelector('button.button-flat.btnPlay.detailButton.emby-button:not(.hide)');
if(btn){clearInterval(iv);btn.click();}
else if(tries>50){clearInterval(iv);}
},300);
}

'''

# _LS_03 (orig L1416-2176) -- sf-ls-inplace, sf-ls-routesync, sf-ls-routesync2
_LS_03 = r'''/* sf-ls-inplace: Jellyfin's click delegation is bound per container. Our own
   sports containers are NOT bound (verified: an itemAction card inside them is
   inert), but the home page's .itemsContainer IS -- and it is on this very page.
   So hand a real channel to a real bound container and let Jellyfin play it. */
function sfBoundContainer(){
var host=(window.__jfView&&window.__jfView.homePage&&window.__jfView.homePage())||document;
return host.querySelector('.itemsContainer');
}
function sfSetTuning(card,on){
if(!card)return;
var w=card.querySelector('.sf-ls-tuningwrap');
if(on){
card.classList.add('sf-ls-tuning');
if(!w){
w=document.createElement('div');w.className='sf-ls-tuningwrap';
var s=document.createElement('div');s.className='sf-ls-spin';
var l=document.createElement('div');l.className='sf-ls-tuninglabel';l.textContent='Tuning in...';
w.appendChild(s);w.appendChild(l);card.appendChild(w);
}
}else{
card.classList.remove('sf-ls-tuning');
if(w)w.remove();
}
}
/* Clear the spinner once Jellyfin's player has taken over. If no <video> shows
   up at all the click never landed, so fall back rather than spin forever. */
function sfWatchTuning(card,jfItem,serverId){
var t=0;
var iv=setInterval(function(){
t++;
var v=document.querySelector('video');
if(v){
if(t>4||!v.paused){clearInterval(iv);sfSetTuning(card,false);}
return;
}
if(t>=16){clearInterval(iv);sfSetTuning(card,false);goToChannel(jfItem,serverId);}
},500);
}
function playChannel(jfItem,serverId,card){
if(!jfItem)return;
var cont=sfBoundContainer();
if(!cont){goToChannel(jfItem,serverId);return;}
var proxy=document.createElement('div');
proxy.className='card sf-ls-proxy';
proxy.setAttribute('data-isfolder','false');
proxy.setAttribute('data-serverid',serverId);
proxy.setAttribute('data-id',jfItem.Id);
proxy.setAttribute('data-type',jfItem.Type||'TvChannel');
proxy.setAttribute('data-mediatype',jfItem.MediaType||'Video');
proxy.setAttribute('data-channelid',jfItem.Id);
proxy.innerHTML='<div class="cardBox"><div class="cardScalable">'
+'<div class="cardOverlayContainer itemAction" data-action="link">'
+'<button is="paper-icon-button-light" class="cardOverlayButton itemAction paper-icon-button-light" data-action="resume" title="Play">'
+'<span class="material-icons play_arrow"></span></button></div></div></div>';
proxy.style.cssText='position:fixed;left:-9999px;top:0;width:1px;height:1px;';
cont.appendChild(proxy);
var btn=proxy.querySelector('[data-action="resume"]');
if(!btn){proxy.remove();goToChannel(jfItem,serverId);return;}
sfSetTuning(card,true);
btn.click();
setTimeout(function(){proxy.remove();},3000);
sfWatchTuning(card,jfItem,serverId);
}
function buildCard(c,data){
var jfItem=data.byNum[String(c.num)];
var div=document.createElement('div');
div.className='sf-ls-card';
if(c.logo)div.style.backgroundImage='url('+JSON.stringify(c.logo)+')';
/* A bridge channel joins to a Jellyfin channel item BY NUMBER, and the bridge
   renumbers as events rotate while Jellyfin's guide refreshes far less often --
   so a card can be genuinely live yet have no jfItem to play. Show that
   plainly rather than rendering a normal-looking card that ignores clicks. */
var playable=!!jfItem;
/* No "LIVE" badge of our own: the bridge's poster art (cdn.highfly.dev)
   already has one burned into the top-left of the image, and ours landed
   almost exactly on top of it -- two overlapping labels, verified by hiding
   ours and seeing the artwork's remain. Only badge when we have something the
   picture does NOT say, i.e. that this card cannot be tuned yet. */
if(!playable){
div.classList.add('sf-ls-unavail');
var badge=document.createElement('div');badge.className='sf-ls-badge sf-ls-syncing';badge.textContent='SYNCING';
div.appendChild(badge);
}
var info=document.createElement('div');info.className='sf-ls-cardinfo';
var title=document.createElement('div');title.className='sf-ls-title';title.textContent=esc(c.name);
var sub=document.createElement('div');sub.className='sf-ls-sub';
sub.textContent=playable?esc(c.category):esc(c.category)+' · not in guide yet';
info.appendChild(title);info.appendChild(sub);
div.appendChild(info);
if(playable){
div.classList.add('card-hoverable');
var ov=document.createElement('div');ov.className='cardOverlayContainer';
var pb=document.createElement('button');pb.type='button';pb.tabIndex=-1;
pb.className='cardOverlayButton cardOverlayButton-hover paper-icon-button-light cardOverlayFab-primary';
var pi=document.createElement('span');
pi.className='material-icons cardOverlayButtonIcon cardOverlayButtonIcon-hover play_arrow';
pi.setAttribute('aria-hidden','true');
pb.appendChild(pi);ov.appendChild(pb);div.appendChild(ov);
div.onclick=function(){playChannel(jfItem,data.serverId,div);};
}
return div;
}

/* Upcoming games are a DIFFERENT KIND OF THING from live ones: there is no
   stream behind them, only a start time, and clicking one just parks you on a
   placeholder lane. They used to be rendered as the same 16:9 poster tile as a
   live game, so a scheduled game looked exactly as playable as one in progress.
   They are now a compact time-first row -- smaller, flatter, no poster, no
   hover-zoom -- so the two read as different at a glance. */
function buildUpcomingCard(game,lane,data){
var jfItem=data.byNum[String(lane.num)];
var div=document.createElement('div');
div.className='sf-ls-card sf-ls-upcoming';
var time=document.createElement('div');time.className='sf-ls-uptime';
time.textContent=formatStart(game.startMs)||'—';
div.appendChild(time);
var info=document.createElement('div');info.className='sf-ls-upinfo';
var title=document.createElement('div');title.className='sf-ls-uptitle';title.textContent=esc(game.name);
info.appendChild(title);
if(game.desc){var sub=document.createElement('div');sub.className='sf-ls-upsub';sub.textContent=esc(game.desc);info.appendChild(sub);}
div.appendChild(info);
if(jfItem)div.onclick=function(){goToChannel(jfItem,data.serverId);};
else div.classList.add('sf-ls-unavail');
return div;
}

function buildSection(title,cards,cat,upcoming){
var sec=document.createElement('div');sec.className='sf-ls-section';
if(cat)sec.dataset.cat=cat;
var h=document.createElement('div');h.className='sf-ls-sectionhead'+(upcoming?' sf-ls-uphead':'');h.textContent=title;
sec.appendChild(h);
if(!cards.length){
var empty=document.createElement('div');empty.className='sf-ls-empty';empty.textContent='Nothing here right now.';
sec.appendChild(empty);
return sec;
}
var grid=document.createElement('div');grid.className='sf-ls-grid'+(upcoming?' sf-ls-upgrid':'');
cards.forEach(function(c){grid.appendChild(c);});
sec.appendChild(grid);
return sec;
}

/* scrollToSection() removed 2026-08-07: the pills now filter the single Live
   Now grid rather than scroll between per-category sections, so there is
   nothing left to scroll to. */
function setActivePill(bar,btn){
[].forEach.call(bar.children,function(x){x.classList.remove('sf-ls-pill-active');});
btn.classList.add('sf-ls-pill-active');
}

function ensureRoot(){
var root=document.querySelector('.sf-livesports-root');
if(root)return root;
root=document.createElement('div');
root.className='sf-livesports-root';
document.body.appendChild(root);
return root;
}

async function loadAndRender(){
var root=ensureRoot();
var data;
/* A SINGLE transient fetch failure used to wipe the page to a dead-end
   message and leave it there for the full 60s refresh interval. Observed
   live: the page sat on "Could not load live sports right now" while the
   same URL answered in ~15ms from the console a second later. Two changes:
   retry a few times with backoff, and if it still fails, keep whatever is
   already rendered rather than clearing good cards off the screen. */
var err=null;
for(var attempt=0;attempt<3;attempt++){
try{ data=await fetchData(); err=null; break; }
catch(e){ err=e; if(attempt<2)await new Promise(function(r){setTimeout(r,600*(attempt+1));}); }
}
if(err){
if(!root.querySelector('.sf-ls-card'))root.innerHTML='<div class="sf-ls-empty">Could not load live sports right now.</div>';
return;
}
var live=dedupe((data.channels||[]).filter(function(c){return !c.isUpcomingLane;}));
var upcoming=(data.channels||[]).filter(function(c){return c.isUpcomingLane;});

var byCat={};
live.forEach(function(c){(byCat[c.category]=byCat[c.category]||[]).push(c);});
var cats=Object.keys(byCat).sort();

root.innerHTML='';

/* PAGE SHAPE (rewritten 2026-08-07). Previously: a "Live Now" row hard-capped
   at live.slice(0,10), then a section per category holding whatever that cap
   spilled. Two problems, both reported:
     1. With more than 10 games live, the rest were NOT in Live Now at all --
        "the live section does not show all live games".
     2. A sport appeared in two places (some games up top, the rest in their
        own section further down), so finding one game meant checking twice.
   Now: ONE Live Now grid holding every live game, and the pills FILTER that
   grid instead of scroll-jumping between duplicate-ish sections. One list, one
   control, nothing hidden below a cap. */
var pillWrap=document.createElement('div');pillWrap.className='sf-ls-pillwrap';
var pillBar=document.createElement('div');pillBar.className='sf-ls-pills';
pillWrap.appendChild(pillBar);
root.appendChild(pillWrap);

var body=document.createElement('div');
root.appendChild(body);

function pill(label,count,onPick,active){
var b=document.createElement('button');
b.className='sf-ls-pill'+(active?' sf-ls-pill-active':'');
b.textContent=label;
var n=document.createElement('span');n.className='sf-ls-pillcount';n.textContent=count;
b.appendChild(n);
b.onclick=function(){setActivePill(pillBar,b);onPick();};
return b;
}

function renderFor(cat){
body.innerHTML='';
var list=cat?(byCat[cat]||[]):live;
if(list.length){
body.appendChild(buildSection(cat?(iconFor(cat)+' '+cat):'🔴 Live Now',list.map(function(c){return buildCard(c,data);}),cat||null));
}else{
var e=document.createElement('div');e.className='sf-ls-empty';e.textContent='No live games right now.';
body.appendChild(e);
}
/* Upcoming follows the same filter, so picking a sport shows that sport's
   live games AND what's coming next in it -- not everything else's. */
upcoming.forEach(function(lane){
if(cat&&lane.category!==cat)return;
var games=(lane.games||[]).slice(0,12);
if(!games.length)return;
body.appendChild(buildSection('🕒 Upcoming '+lane.category,games.map(function(g){return buildUpcomingCard(g,lane,data);}),lane.category,true));
});
root.scrollTop=0;
}

pillBar.appendChild(pill('All',live.length,function(){renderFor(null);},true));
cats.forEach(function(cat){
pillBar.appendChild(pill(iconFor(cat)+' '+cat,byCat[cat].length,function(){renderFor(cat);},false));
});

renderFor(null);
}

var refreshTimer=null;

/* PROGRAMS TAB FIX (2026-07-25): the first cut of "move this to Programs"
   showed the overlay unconditionally whenever the Programs tab was active,
   which completely replaced Jellyfin's own native "On Now" list -- that list
   mixes regular movie/TV programs together with sports, so hiding it lost
   all the non-sports entries. Reported by the user as "movies and tv
   programs no show". Fixed by gating the overlay behind its own pill toggle
   (mirroring the Guide tab's filter pills, a separate localStorage key so
   the two tabs remember their choice independently) that defaults to
   Jellyfin's native content ('all') with an opt-in 'Sports' pill. */
function getProgF(){try{return localStorage.getItem('sfProgramsFilter')||'all';}catch(e){return 'all';}}
function setProgF(v){try{localStorage.setItem('sfProgramsFilter',v);}catch(e){}}

/* Deliberately NOT inserted into programsTab's own child list (a first cut
   did this via insertBefore(bar, programsTab.firstChild) and it blanked the
   whole tab -- reported as "all page is blank"). Root cause: Jellyfin ships
   its own native rule for this exact tab,
   "#liveTvSuggestedPage .pageTabContent[data-index="0"] .verticalSection:
   nth-child(n+2){display:none!important}", which hides every .verticalSection
   after the first (it's how Jellyfin suppresses its own duplicate/stale
   section instances in this tab). Prepending our bar as an extra sibling
   shifted the one real content section from position 1 into the "n+2" range,
   hiding it entirely. Rendering the pill bar as a fixed-position element
   appended to <body> (like ensureRoot() already does for the overlay root)
   keeps it completely outside that nth-child count. */
function ensureProgramsPillBar(){
var bar=document.querySelector('.sf-progfilter');
if(bar)return bar;
bar=document.createElement('div');bar.className='sf-guidefilter sf-progfilter';
/* z-index 1000 (not just "above the visible header") because
   .headerTop's real hit-box extends several px below where the header
   visually ends -- .skinHeader itself is fixed/z-index:999, so anything
   under that stacking context (our bar was z-index:30) loses the pointer-
   event tie in that overlap band even though it looks clearly separated
   on screen. Confirmed live via elementFromPoint() on the button's own
   center returning .headerTop, not the button -- root cause of "hard to
   press these buttons". */
bar.style.position='fixed';bar.style.left='0';bar.style.right='0';bar.style.zIndex='1000';bar.style.display='none';
/* Labeled "TV" rather than "All" -- Jellyfin's own native On Now list this
   pill shows is sourced purely from its own EPG "current program" data per
   channel, which often doesn't carry sports listings reliably, so in
   practice this pill is just the movie/TV programs, not literally
   everything. */
[['all','TV'],['sports','Sports']].forEach(function(p){
var b=document.createElement('button');b.className='sf-gf-pill'+(p[0]===getProgF()?' sf-gf-active':'');b.textContent=p[1];
b.onclick=function(){
setProgF(p[0]);
[].forEach.call(bar.children,function(x){x.classList.remove('sf-gf-active');});
b.classList.add('sf-gf-active');
};
bar.appendChild(b);
});
document.body.appendChild(bar);
return bar;
}

/* Whether to show the overlay is recomputed from live DOM state every tick,
   NOT toggled solely by a pill's click handler or a hashchange listener.
   Jellyfin's router uses history.pushState for its "#/..." routes, which
   does NOT fire a native hashchange event even though the visible URL
   changes -- confirmed by testing (navigating away left the overlay stuck on
   top with no event ever firing). Guide/Programs/Channels also all share the
   SAME "#/livetv" hash (only a ?tab= query differs), so a hash-prefix check
   alone can't tell them apart either. Polling a real content-visibility
   signal every tick means the overlay is always consistent with whatever's
   actually on screen, regardless of how the user got there (click,
   back/forward, programmatic navigation). Programs tab content lives in
   #suggestionsTab (Jellyfin's own id; like .tvguide it can have multiple
   stale instances mounted from earlier SPA navigation -- confirmed live even
   the Home page carries leftover copies -- so still filter to the one with
   offsetParent!==null). */
setInterval(function(){
var root=document.querySelector('.sf-livesports-root');
/* Jellyfin's MUSIC page reuses this very id for its Suggestions pane
   (#suggestionsTab inside #musicRecommendedPage), so an id-only check put the
   TV/Sports pill bar -- and the whole fixed-position Live Sports overlay when
   sfProgramsFilter=='sports' -- on top of Music > Suggestions. Verified live
   2026-08-04. Gate on the Live TV route as well; the existing else-branch
   already hides the bar and clears paddingTop when programsTab is null. */
var onLiveTv=window.__sfLtv?window.__sfLtv.is():((location.hash||'').indexOf('#/livetv')===0);
var candidates=onLiveTv?document.querySelectorAll('#suggestionsTab'):[];
var programsTab=null;
for(var i=0;i<candidates.length;i++){if(candidates[i].offsetParent!==null){programsTab=candidates[i];break;}}
var pillBar=ensureProgramsPillBar();
var hdr=document.querySelector('.skinHeader');
var hdrBottom=hdr?hdr.getBoundingClientRect().bottom:0;
if(false){
pillBar.style.display='flex';
var _pt=hdrBottom+'px';if(pillBar.style.top!==_pt)pillBar.style.top=_pt;
/* Reserve space via padding-top on the tab itself, not by inserting any
   new child -- inline styles on programsTab don't affect its children's
   nth-child positions, so the "hide everything but the first
   .verticalSection" native rule (see comment above ensureProgramsPillBar)
   stays keyed on the original untouched child order. */
programsTab.style.paddingTop=pillBar.getBoundingClientRect().height+'px';
}else{
pillBar.style.display='none';
for(var j=0;j<candidates.length;j++)candidates[j].style.paddingTop='';
}
/* Standalone sports page: #/home?sports=1. sf-livesports fetches ALL its own
   data (sportsbridge channels.json + /LiveTv/Channels), so it never needed the
   Live TV DOM -- tying it to #/livetv?tab=0 was what produced the occasional
   black page, because it depended on that route mounting #suggestionsTab first.
   On the dedicated route Home renders underneath (always reliable) and the
   overlay simply covers it. */
var dedicated=/[?&]sports=1/.test(location.hash||'');
/* Sports is now a separate destination (#/home?sports=1) and is deliberately NOT
   reachable from Live TV any more. Dropping the old
   "programsTab && filter==='sports'" branch is what finally removes every
   interaction between the two: no TV|Sports pill row, no writes to
   #suggestionsTab's padding, and therefore none of the bouncing that came from
   this script and jf-sports-page both driving that padding. */
var shouldShow=dedicated;
if(shouldShow){
if(!root)root=ensureRoot();
if(!root.classList.contains('sf-ls-show')){
root.classList.add('sf-ls-show');
loadAndRender();
if(!refreshTimer)refreshTimer=setInterval(loadAndRender,60000);
}
/* top:0 (not pillBar's bottom) plus padding-top to clear it, rather than
   starting the fixed overlay right at the pillBar -- otherwise the gap
   between viewport-top and the overlay's start left the OLD, still-scrolled
   native "On Now" list showing through the header's translucent backdrop
   (reported as "i can see the home page peeking from the back" after
   scrolling on TV then switching to Sports). Starting the overlay's own
   solid background at y:0 means whatever peeks through that translucency
   is this overlay, not a stale layer underneath. */
root.style.top='0';
/* dedicated mode has no pill bar to clear - measure the header instead */
root.style.paddingTop=(dedicated?(hdrBottom+14):pillBar.getBoundingClientRect().bottom)+'px';
}else if(root&&root.classList.contains('sf-ls-show')){
root.classList.remove('sf-ls-show');
}
},500);
/* sf-ls-routesync: the block above runs on a 500ms poll, so the overlay lagged
   every route change -- it lingered ~450ms into the video handoff (the flash as
   a stream opens) and came back ~500ms late on the way out (the flash of Home).
   Apply the same decision synchronously on the route event so visibility and
   route change in the same frame. The poll still owns first render, sizing and
   the 60s refresh; this only removes the lag. */
function sfRouteSync(){
var r=document.querySelector('.sf-livesports-root');
if(!r)return;
if(!/[?&]sports=1/.test(location.hash||'')){r.classList.remove('sf-ls-show');return;}
/* show only when there is something to show: a first visit has no cards yet and
   must wait for the poller's loadAndRender(), or we flash an empty overlay AND
   suppress the render branch that keys on the class being absent. */
if(r.querySelector('.sf-ls-card'))r.classList.add('sf-ls-show');
}
window.addEventListener('hashchange',sfRouteSync);
window.addEventListener('popstate',sfRouteSync);
/* sf-ls-routesync2: hashchange/popstate alone changed nothing (446ms -> 414ms)
   because Jellyfin navigates with history.pushState, which fires neither. Wrap
   the navigation itself so the overlay updates in the same tick as the route,
   and keep a cheap 60ms backstop for anything that bypasses both. */
(function(){
var wrap=function(n){
var o=history[n];
if(!o||o.__sfrs)return;
var f=function(){var r=o.apply(this,arguments);try{sfRouteSync();}catch(e){}return r;};
f.__sfrs=true;
history[n]=f;
};
wrap('pushState');wrap('replaceState');
})();
setInterval(sfRouteSync,60);
/* sf-ltv-nofiller: the sportsbridge parks future games on lane channels whose
   current program is titled "Upcoming games ahead". Jellyfin sees them as
   ordinary live programs, so they land in On Now and outnumber the real games
   (measured 6 of 9). Title is the only distinguishing feature -- no type, tag
   or genre separates them. Observer-driven, not polled, so they never paint. */
/* sf-ltv-nofiller-all: Live TV > Guide > Programs leaves TWO
   .activeProgramItems mounted -- [0] stale and empty, [1] live with the
   cards. querySelector picked the stale one, tagged nothing, and every
   placeholder reappeared. Sweep them all; the cached-view duplication is
   normal here, so 'first match' is never the right resolution. */
function sfSweepFiller(){
var conts=document.querySelectorAll('.activeProgramItems');
for(var n=0;n<conts.length;n++){
var cards=conts[n].querySelectorAll('.card:not(.sf-ltv-filler)');
for(var i=0;i<cards.length;i++){
var t=cards[i].querySelector('.cardText');
if(t&&/upcoming games ahead/i.test(t.textContent||''))cards[i].classList.add('sf-ltv-filler');
}
}
}
var sfFillerQueued=false;
function sfQueueFiller(){
if(sfFillerQueued)return;
sfFillerQueued=true;
/* sf-ltv-nofiller-tick: rAF is suspended in background/unfocused tabs, which
   left placeholders visible until something forced a paint. */
setTimeout(function(){sfFillerQueued=false;sfSweepFiller();},0);
}
try{new MutationObserver(sfQueueFiller).observe(document.documentElement,{childList:true,subtree:true});}catch(e){}
window.addEventListener('hashchange',sfQueueFiller);
sfQueueFiller();
/* sf-music-btn: Music sits 7th in the drawer behind Folders and Audio Books,
   and the main pills are absent on the music page, so there was no quick way
   in. Put it in the header next to the dice, where it is reachable from every
   page. Re-applied on a timer because Jellyfin rebuilds the header. */
function sfAddMusicButton(){
var right=document.querySelector('.headerRight');
if(!right||right.querySelector('.sf-music-btn'))return;
var btn=document.createElement('button');
btn.type='button';btn.title='Music';
btn.className='headerButton headerButtonRight paper-icon-button-light sf-music-btn';
btn.innerHTML='<span class="material-icons library_music" aria-hidden="true"></span>';
btn.addEventListener('click',function(){
var go=function(id){location.hash='#/music?topParentId='+id+'&collectionType=music';};
if(window.__sfMusicViewId){go(window.__sfMusicViewId);return;}
try{
var ac=window.ApiClient;
ac.getUserViews({UserId:ac.getCurrentUserId()}).then(function(r){
var items=r.Items||[];
for(var i=0;i<items.length;i++){
if(items[i].CollectionType==='music'){window.__sfMusicViewId=items[i].Id;go(items[i].Id);return;}
}
});
}catch(e){}
});
/* sf-dice-swap: sit at the front of the cluster, where the dice was */
right.insertBefore(btn,right.firstChild);
}
setInterval(sfAddMusicButton,900);
/* sf-music-ux: open Music on Suggestions (Recently Added / Recently Played /
   Frequently Played) instead of a paginated A-Z album grid. Jellyfin keeps no
   last-tab preference -- it resets to Albums every entry -- so this overrides
   no user choice. Keyed on the hash so it fires once per arrival: click Albums
   and it stays until you navigate away and return. */
var sfMusicNavDone='';
/* sf-music-landing-i18n: the tab was originally matched by the ENGLISH word
   "Suggestions", so every non-English client stayed on Jellyfin's default
   ALBUMS tab and the entire curated music landing page was invisible to the
   German and Chinese users it was built for. data-index is Jellyfin's own and
   is identical in every language (verified live: Suggestions / Vorschlaege /
   建议 are all data-index="1"). The sibling sf-music-btn already learned
   this lesson and matches on an icon class for the same reason. */
/* sf-music-landing-scope (2026-08-20). REPLACES the loop above, which took the
   first VISIBLE .emby-tabs-slider on the page. During the home -> music
   transition the HOME page's strip is still on screen, and its second button --
   Favorites / "My Stuff" -- also carries data-index="1". So this clicked My
   Stuff instead of Suggestions, which navigates to #/home?tab=1, and because
   sfMusicNavDone was latched BEFORE the click it never tried again.
   Measured: 5 of 6 home -> Music navigations ended on the bare Albums grid with
   the URL reading #/home?tab=1, no greeting, no featured hero with Play/Mix, no
   "Made for you", no Top Artists -- and a Back button that went to the wrong
   place. Direct loads of #/music were fine, which is why it hid for so long.
   Two changes make it safe:
     - pick the strip with the MOST data-index buttons. The music page has seven
       tabs, the home page exactly two, so this can never be home's again.
     - latch only once the tab is genuinely active, so a click that does not
       take is retried on the next tick instead of being given up on.
   Jellyfin marks an active tab with .emby-tab-button-active; .is-active is the
   PANE's class, so the old check never matched either. Both are accepted. */
function sfMusicLanding(){
var h=location.hash||'';
if(!/^#\/music/.test(h)){sfMusicNavDone='';return;}
if(sfMusicNavDone===h)return;
var pages=document.querySelectorAll('#musicRecommendedPage'),page=null,pi;
for(pi=0;pi<pages.length;pi++){if(pages[pi].offsetParent!==null){page=pages[pi];break;}}
if(!page)return;
var sliders=document.querySelectorAll('.emby-tabs-slider'),best=null,bestN=0,i,j,s,idx;
for(i=0;i<sliders.length;i++){
s=sliders[i];
if(!s.getClientRects().length)continue;
idx=s.querySelectorAll('button[data-index]');
if(idx.length>bestN){bestN=idx.length;best=s;}
}
/* home's strip is two buttons; the library strips are five or more */
if(!best||bestN<3)return;
/* sf-mus-nav: an EXPLICIT ?tab=N in the url wins. This function exists to stop
   Music opening on Jellyfin's default (Albums) when nothing was asked for, and
   it did that by forcing pane 1 on every #/music url whatever it said. That was
   harmless while the other panes were only reachable by clicking a tab -- but
   Library is a top-level destination now, so reloading on it, or opening a link
   to it, bounced you back to Home. Clicking still worked, which is exactly the
   kind of half-broken that goes unnoticed.
   Only ?tab=1 and a bare #/music are forced; anything else is deliberate. */
var tm=h.indexOf('tab=');
if(tm>-1){
var tv=h.slice(tm+4).split('&')[0];
if(tv&&tv!=='1'){sfMusicNavDone=h;return;}
}
var bb=best.querySelectorAll('button'),sug=null;
for(j=0;j<bb.length;j++){if(bb[j].getAttribute('data-index')==='1')sug=bb[j];}
if(!sug)return;
if(sug.classList.contains('emby-tab-button-active')||sug.classList.contains('is-active')){
sfMusicNavDone=h;
return;
}
sug.click();
}
/* toggled, not latched: a section that loads late must be able to come back */
function sfHideEmptySections(){
if(!/^#\/music/.test(location.hash||''))return;
var secs=document.querySelectorAll('.verticalSection');
for(var i=0;i<secs.length;i++){
/* only judge JELLYFIN's rows -- ours build their own card markup and would
   always look "empty" to a .card test */
/* The marker is a data attribute, NOT a class. As a class it started with
   "sf-", so the ownership regex above matched the marker this function had just
   written and un-hid the row on the next tick -- measured flipping
   display:block/none once per 400ms tick indefinitely on the Audio Books page. */
if(/(^| )sf-/.test(secs[i].className||''))
{secs[i].removeAttribute('data-sf-empty');continue;}
if(secs[i].querySelector('.card'))secs[i].removeAttribute('data-sf-empty');
else secs[i].setAttribute('data-sf-empty','1');
}
}
/* video-only controls are hidden only while the active player is audio */
/* sf-music-capsule: the same audio-vs-video test now also drives the floating
   player capsule, via body.sf-audio-playing. Video keeps the full-width flush
   bar -- that is the whole reason this is a class and not a blanket rule. */
/* ---- sf-np-fav (2026-08-27) ----------------------------------------------
   This library has 2,459 tracks and **zero** favourites, and the reason is not
   that nobody likes anything: the now-playing bar's buttons are Previous,
   Pause, Next, Lyrics, Cast, More. There is a heart on queue rows and on card
   overlays, but none at the one moment you actually want it -- while the song
   is playing. Both references put it right there on the bar.

   The id comes from the <audio> element's own src (/Audio/{id}/...), the same
   trick sf-ab-switchguard uses, because the bar's data-id lags the audio by up
   to ~2s when you skip tracks and a lagging id would favourite the WRONG song.
   Parsed with string ops rather than a regex literal containing '/', which has
   shipped broken from this file before. */
var sfFavState={}, sfFavBusy={};
function sfNpAudioId(){
var a=document.querySelector('audio');
if(!a)return '';
var src=a.currentSrc||a.src||'';
var i=src.indexOf('/Audio/');
if(i<0)return '';
var rest=src.slice(i+7),j=rest.indexOf('/');
if(j<0)return '';
var id=rest.slice(0,j).toLowerCase().split('-').join('');
return /^[0-9a-f]{32}$/.test(id)?id:'';
}
function sfNpFavPaint(btn,id){
var on=!!sfFavState[id];
var ic=btn.querySelector('.material-icons');
if(ic&&ic.textContent!==(on?'favorite':'favorite_border'))ic.textContent=on?'favorite':'favorite_border';
if(btn.classList.contains('sf-np-fav-on')!==on)btn.classList.toggle('sf-np-fav-on',on);
var t=on?'Remove from favorites':'Add to favorites';
try{t=window.sfTr?window.sfTr(t):t;}catch(e){}
if(btn.title!==t)btn.title=t;
}
function sfNpFav(){
/* audio only -- while a film is up the bar is hidden anyway (sf-hide-bar) */
if(document.querySelector('video'))return;
var right=document.querySelector('.nowPlayingBar .nowPlayingBarRight');
if(!right)return;
var btn=right.querySelector('.sf-np-fav');
/* sf-np-fav-dedupe: Jellyfin HAS its own favourite button in this bar --
   .nowPlayingBarUserDataButtons -- which it drops at max-width:66em and which
   sf-music-capsule then re-enables. So it is present on desktop and absent on a
   phone, and the first version of this function only ever ran against a 390px
   probe: on desktop it produced TWO "Add to favorites" buttons side by side.
   Where Jellyfin's own control exists, defer to it -- it already tracks state
   through the player and needs no help from us. */
var native=right.querySelector('.nowPlayingBarUserDataButtons button');
if(native&&native.offsetParent!==null){
if(btn&&btn.parentNode)btn.parentNode.removeChild(btn);
return;
}
var id=sfNpAudioId();
if(!id){if(btn&&btn.parentNode)btn.parentNode.removeChild(btn);return;}
if(!btn){
btn=document.createElement('button');
btn.type='button';
btn.className='sf-np-fav mediaButton paper-icon-button-light';
btn.innerHTML='<span class="material-icons" aria-hidden="true">favorite_border</span>';
btn.addEventListener('click',function(e){
e.preventDefault();e.stopPropagation();
var tid=btn.getAttribute('data-id');
if(!tid)return;
var on=!sfFavState[tid];
/* optimistic: a like has to feel instant, and the worst case is a heart that
   flips back if the write fails */
sfFavState[tid]=on;
sfNpFavPaint(btn,tid);
try{
var ac=window.ApiClient;
fetch(ac.getUrl('Users/'+ac.getCurrentUserId()+'/FavoriteItems/'+tid),
{method:on?'POST':'DELETE',headers:{'X-Emby-Token':ac.accessToken()}})
.then(function(r){if(!r||!r.ok){sfFavState[tid]=!on;sfNpFavPaint(btn,tid);}})
.catch(function(){sfFavState[tid]=!on;sfNpFavPaint(btn,tid);});
}catch(e){sfFavState[tid]=!on;sfNpFavPaint(btn,tid);}
});
/* left of Lyrics, so the cluster reads like/lyrics/cast/more */
var lyr=right.querySelector('.sf-lyr-btn');
if(lyr)right.insertBefore(btn,lyr); else right.insertBefore(btn,right.firstChild);
}
if(btn.getAttribute('data-id')!==id){
btn.setAttribute('data-id',id);
sfNpFavPaint(btn,id);
if(sfFavState[id]===undefined&&!sfFavBusy[id]){
sfFavBusy[id]=1;
try{
var ac2=window.ApiClient;
ac2.getJSON(ac2.getUrl('Users/'+ac2.getCurrentUserId()+'/Items/'+id))
.then(function(it){sfFavBusy[id]=0;
sfFavState[id]=!!(it&&it.UserData&&it.UserData.IsFavorite);
if(btn.getAttribute('data-id')===id)sfNpFavPaint(btn,id);})
.catch(function(){sfFavBusy[id]=0;});
}catch(e){sfFavBusy[id]=0;}
}
}
}
/* ---- sf-lyr-one (2026-08-27) ---------------------------------------------
   TWO lyrics surfaces could be on screen at once. Reported flow, reproduced
   exactly at 1440px:

     tap Lyrics on the now-playing bar -> .sf-lyrics side panel opens (x=1026,w=402)
     tap the artwork in the bar        -> the immersive player opens OVER it,
                                          side panel still open
     tap Lyrics in the player          -> .sf-np-panel-in renders lyrics too
                                          (x=753,w=420) and the side panel sits
                                          ON TOP of it

   Two identical lyric lists, one covering the other. They are independent
   surfaces -- .sf-lyrics is toggled by the bar's .sf-lyr-btn, the player's tab
   goes through sfNpPanel() -- and neither knew the other existed.

   Rule: while the immersive player is up it OWNS lyrics. The player is a
   full-screen takeover and its own tab is right there, so the side panel has
   nothing to add and only occludes it.

   The hand-over also carries the INTENT rather than just closing the panel: if
   lyrics were on screen when the player opened, the player opens on its Lyrics
   tab. Closing the panel alone would have punished the user for opening the
   player -- they asked to see lyrics and would have got none.
   Done once per opening (sfLyrHanded), so tapping the player's Lyrics tab to
   dismiss it -- sfNpPanel is a deliberate toggle -- is not fought on the next
   tick. */
var sfLyrHanded=0;
function sfLyrOne(){
var np=document.querySelector('.sf-np');
if(!np||!np.classList.contains('sf-np-show')){sfLyrHanded=0;return;}
if(!document.body.classList.contains('sf-lyrics-open'))return;
try{sfLyricsClose();}catch(e){}
if(!sfLyrHanded){
sfLyrHanded=1;
var t=np.querySelector('.sf-np-tab-lyr');
if(t&&!t.classList.contains('sf-np-on'))t.click();
}
}
function sfNowPlayingKind(){
var pages=document.querySelectorAll('.nowPlayingPage');
var isAudio=!!document.querySelector('audio')&&!document.querySelector('video');
for(var i=0;i<pages.length;i++)pages[i].classList.toggle('sf-audio-now',isAudio);
document.body.classList.toggle('sf-audio-playing',isAudio);
/* sf-hide-bar: while a VIDEO is up the now-playing bar is redundant (the video
   OSD is the control surface), and because the capsule is scoped to audio,
   leaving audio mode made the STOCK full-width bar reappear over the film --
   that is the "old music control bar" seen when a movie loads. */
document.documentElement.classList.toggle('sf-video-now',!!document.querySelector('video'));
/* nothing to show lyrics FOR once audio stops, and a panel left open over an
   idle app is just a dead sidebar */
if(!isAudio)sfLyricsClose();
}
/* sf-capsule-group: Apple keeps shuffle/prev/play/next/repeat as ONE cluster.
   Jellyfin puts prev/play/next in .nowPlayingBarCenter and leaves shuffle and
   repeat over in .nowPlayingBarRight, and CSS `order` only sorts among
   SIBLINGS -- it cannot move a node between two parents. So the two buttons are
   relocated here. Idempotent (the parentElement test), and re-run on the 400ms
   interval because Jellyfin rebuilds the bar when the player changes. */
function sfCapsuleGroup(){
var c=document.querySelector('.nowPlayingBarCenter');
if(!c)return;
var sh=document.querySelector('.nowPlayingBar .btnShuffleQueue');
var rp=document.querySelector('.nowPlayingBar .toggleRepeatButton');
var prev=c.querySelector('.previousTrackButton');
if(sh&&prev&&sh.parentElement!==c)c.insertBefore(sh,prev);
if(rp&&rp.parentElement!==c)c.appendChild(rp);
}
/* sf-playing-row: mark the album-page row for the track that is playing, so it
   can show an equaliser where its number was.
   The id comes from the now-playing bar's own rating button, which carries the
   CURRENT TRACK's data-id -- verified equal to the matching .listItem[data-id]
   on a live page. That is why this does no title-string matching, which would
   have broken on the duplicate titles an album can carry. */
function sfPlayingRow(){
var btn=document.querySelector('.nowPlayingBarUserDataButtons button');
var id=btn?btn.getAttribute('data-id'):null;
var rows=document.querySelectorAll('#childrenContent .listItem');
for(var i=0;i<rows.length;i++){
var r=rows[i];
var on=!!id&&r.getAttribute('data-id')===id;
if(on===r.classList.contains('sf-row-playing'))continue;
r.classList.toggle('sf-row-playing',on);
var cell=r.querySelector('.listItem-indexnumberleft');
if(!cell)continue;
var eq=cell.querySelector('.sf-eq');
if(on&&!eq){
var s=document.createElement('span');
s.className='sf-eq';
s.innerHTML='<i></i><i></i><i></i>';
cell.appendChild(s);
}else if(!on&&eq){eq.remove();}
}
}
/* sf-cw-hidden: "Remove" on a Continue Watching card did nothing lasting -- the
   item came straight back on reload. Measured: Jellyfin Enhanced DOES persist
   the hide (hidden-content.json gained an entry with HideScope
   "continuewatching"), and it does inspect the cards (each carries
   data-je-hidden-checked="1") -- it just fails to match them, so 6 items marked
   hidden were all still on the row after a reload.
   The likely reason is an id-format mismatch: JE stores DASHED guids
   ("00000000-1111-2222-3333-444444444444") while the card's data-id is undashed
   ("00000000111122223333444444444444"). This compares with the dashes stripped
   from both sides, so either format matches.
   Scoped to .verticalSection.ContinueWatching -- a stable class, unlike the
   localised section title -- so a hidden item still appears in Recently Added
   and everywhere else, which is what HideScope "continuewatching" means. */
var sfHidden=null,sfHiddenAt=0,sfHiddenBusy=false,sfHiddenRaw={},sfHiddenWhen={};
'''

# _LS_04 (orig L2176-2889) -- sf-cwrm-reset, sf-cwrm-unplayed, sf-hidden-uid
_LS_04 = r'''/* sf-cwrm-reset: the SERIES a hidden episode belongs to. A Next Up hide has to
   be able to expire when the SHOW is watched again, not only when that exact
   episode is -- otherwise removing an episode buries it for good. */
var sfHiddenSeries={};
/* sf-cwrm-unplayed: the series' UnplayedItemCount AT THE MOMENT it was parked.
   MEASURED, because the obvious signal does not exist: a Series carries NO
   LastPlayedDate at all -- its UserData is only
   {UnplayedItemCount, PlaybackPositionTicks, PlayCount, IsFavorite, Played, Key}
   -- so comparing the show's LastPlayedDate could never fire, which is exactly
   why a parked episode stayed parked after watching the show again. Verified:
   play one episode and the series' UnplayedItemCount goes 110 -> 109 while no
   date appears anywhere on the series. So THAT is the 'watched this show
   again' signal. */
var sfHiddenUnplayed={};
function sfNorm(id){return String(id||'').replace(/-/g,'').toLowerCase();}
function sfLoadHidden(force){
if(sfHiddenBusy)return;
if(!force&&sfHidden&&(Date.now()-sfHiddenAt)<20000)return;
var ac=window.ApiClient;
if(!ac)return;
/* sf-hidden-uid: ApiClient exists before it knows who is signed in, and the id
   was being concatenated straight into the path -- so every single page load
   fired GET .../user-settings/null/hidden-content.json and took a 400. Harmless
   to the user but it is one guaranteed failed request per load, and it fires on
   the busiest part of the timeline. Wait for a real id; the 400ms tick calls
   this again a moment later. */
var _hu='';
try{_hu=ac.getCurrentUserId&&ac.getCurrentUserId();}catch(e){_hu='';}
if(!_hu)return;
sfHiddenBusy=true;
ac.getJSON(ac.getUrl('JellyfinEnhanced/user-settings/'+_hu+'/hidden-content.json')).then(function(j){
var map={},items=(j&&j.Items)||{},k;
for(k in items){
if(!items.hasOwnProperty(k))continue;
if(items[k]&&items[k].HideScope==='continuewatching'){
var raw=items[k].ItemId||k;
map[sfNorm(raw)]=1;
/* keep the id in its ORIGINAL form too -- matching is done undashed, but the
   UserData write in sf-cw-purge should send back exactly what the server gave
   us rather than a reformatted guid. */
sfHiddenRaw[sfNorm(raw)]=raw;
/* sf-cw-rewatch: WHEN it was hidden. sf-cw-purge below compares this against
   the item's LastPlayedDate so that hiding something once cannot keep wiping
   its resume position for the rest of time. */
var _ha=Date.parse(items[k].HiddenAt||'');
sfHiddenWhen[sfNorm(raw)]=isFinite(_ha)?_ha:0;
sfHiddenSeries[sfNorm(raw)]=sfNorm(items[k].SeriesId||'');
var _su=items[k].SfUnplayed;
sfHiddenUnplayed[sfNorm(raw)]=(_su==null?-1:_su);
}
}
sfHidden=map;sfHiddenAt=Date.now();sfHiddenBusy=false;try{sfCwMark();}catch(e){}
}).catch(function(){sfHidden=sfHidden||{};sfHiddenAt=Date.now();sfHiddenBusy=false;});
}
/* sf-music-pad: on mobile the Music page's first heading rendered 66px UNDERNEATH
   the tab bars. Measured at a forced layout-mobile: .skinHeader is 174px tall
   because Music is the only page stacking TWO bars inside it (our main pills at
   75-122, then Jellyfin's Albums/Suggestions/... at 132-174), while
   #musicRecommendedPage only carries padding-top:108px -- so the content starts
   66px too high and the heading sits behind the sub-bar.
   The header's height is not a constant (it re-flows with viewport, and the same
   note in jf-fav-watchlist's align() applies), so this MEASURES it each tick
   rather than hardcoding a number. The >2px guard stops it writing style on
   every pass, which is what would otherwise fight Jellyfin's own layout. */
function sfMusicPad(){
var pages=document.querySelectorAll('#musicRecommendedPage'),page=null,i;
for(i=0;i<pages.length;i++)if(pages[i].offsetParent!==null)page=pages[i];
if(!page)return;
var hdr=document.querySelector('.skinHeader');
if(!hdr)return;
var hb=Math.round(hdr.getBoundingClientRect().bottom);
if(hb<=0)return;
var want=hb+14;
/* An inline style CANNOT win here: Jellyfin sets
   .libraryPage:not(.noSecondaryNavPage){padding-top:7.5em!important} -- 7.5em is
   exactly the 108px we measured, and it budgets for ONE secondary nav bar, not
   the extra main pill row we add. Verified by setting paddingTop inline and
   watching the computed value stay at 108px.
   So publish the measured height as a variable and let a higher-specificity
   !important rule (emitted with this script) consume it. */
var de=document.documentElement;
var cur=parseInt(de.style.getPropertyValue('--sf-music-pad'),10)||0;
if(Math.abs(cur-want)>2)de.style.setProperty('--sf-music-pad',want+'px');
if(page.style.paddingTop)page.style.paddingTop='';
}
/* sf-cw-purge: make a Continue Watching removal REAL.
   Hiding the card was only ever cosmetic -- measured, the server still returned
   all 42 resume items with the "removed" ones among them. That means the removal
   existed only in this browser: another device, or a lost/reset Jellyfin
   Enhanced settings file, and everything came straight back. That is the
   "it comes back after I reload" report.
   The durable fix is to clear the resume position server-side, which is exactly
   what "remove from Continue Watching" means: the item leaves /Items/Resume for
   every client, and returns only when it is watched again (which writes a new
   position). Verified endpoint: POST /UserItems/{id}/UserData?userId=...
   with {PlaybackPositionTicks:0, Played:false} -> 200, position 4270000000 -> 0.
   NOTE this discards the resume point by design. That is the requested
   behaviour; do not "improve" it by preserving progress, which would put the
   item straight back on the row.
   Runs once per id (sfCwPurged) so the 400ms tick cannot hammer the server. */
/* sf-cwrm-reset: retire a hide PERMANENTLY. The old code deleted it from the
   in-memory maps only, so sfLoadHidden read it straight back off the server on
   the next page load -- the item reappeared and then vanished again on reload,
   which is indistinguishable from 'it never came back'. */
/* sf-cwrm-moved (2026-08-29): has the viewer moved PAST a parked episode?
   Ask the one thing that actually knows -- Jellyfin's own Next Up for that
   series. If the episode it would show now is not the one we parked, the show
   has been watched on since, so the park has done its job and is retired. That
   is what makes this a 'remove', not a permanent hide: it never outlives the
   moment it was about.
   No stored baseline is involved, which is the point -- the hidden-content file
   cannot carry one. One small request per parked SERIES, and only on the 60s
   re-check, never per tick. */
var sfMovedBusy={};
function sfCwSeriesMoved(){
var ac=window.ApiClient;
if(!ac||!sfHidden)return;
var uid=ac.getCurrentUserId&&ac.getCurrentUserId();
if(!uid)return;
var bySeries={},k,sid;
for(k in sfHidden){
if(!sfHidden.hasOwnProperty(k))continue;
sid=sfHiddenSeries[k];
if(!sid||sfMovedBusy[sid])continue;
(bySeries[sid]=bySeries[sid]||[]).push(k);
}
for(sid in bySeries){
if(!bySeries.hasOwnProperty(sid))continue;
(function(series,ids){
sfMovedBusy[series]=1;
ac.getJSON(ac.getUrl('Shows/NextUp',{userId:uid,seriesId:series,Limit:1}))
.then(function(r){
sfMovedBusy[series]=0;
var cur=(((r&&r.Items)||[])[0]||{}).Id||'';
cur=sfNorm(cur);
var gone=[],i;
for(i=0;i<ids.length;i++){
/* still the very next episode -> the park still means something */
if(cur&&cur===ids[i])continue;
gone.push(sfHiddenRaw[ids[i]]||ids[i]);
if(sfHidden)delete sfHidden[ids[i]];
delete sfHiddenWhen[ids[i]];
delete sfCwPurged[ids[i]];
}
if(gone.length)sfDropHidden(gone);
}).catch(function(){sfMovedBusy[series]=0;});
})(sid,bySeries[sid]);
}
}
function sfDropHidden(ids){
var ac=window.ApiClient;
if(!ac||!ids||!ids.length)return;
var uid=ac.getCurrentUserId&&ac.getCurrentUserId();
if(!uid)return;
var path='JellyfinEnhanced/user-settings/'+uid+'/hidden-content.json';
ac.getJSON(ac.getUrl(path)).then(function(j){
if(!j||!j.Items)return;
var changed=false,k,n;
for(n=0;n<ids.length;n++){
for(k in j.Items){
if(!j.Items.hasOwnProperty(k))continue;
if(sfNorm(k)===sfNorm(ids[n])){delete j.Items[k];changed=true;}
}
}
if(!changed)return;
return ac.ajax({type:'POST',url:ac.getUrl(path),
contentType:'application/json',data:JSON.stringify(j)});
}).catch(function(){});
}
var sfCwPurged={};
function sfCwPurge(){
if(!sfHidden)return;
var ac=window.ApiClient;
if(!ac||!ac.getCurrentUserId)return;
/* sf-cwrm-recheck (2026-08-29): sfCwPurged used to claim an id FOREVER, so the
   'was it watched again?' test below ran exactly ONCE -- moments after the
   hide, when the answer is always no. A parked Next Up episode could therefore
   never retire itself, which is precisely the 'it can never come back' case
   the admin asked about. Verified: after removing an episode and then watching
   another episode of the same show, the entry was still parked.
   Claim with a TIMESTAMP and re-ask every 60s. Still one batched GET and never
   a per-tick request, but the expiry can actually fire. The UserData write does
   not repeat either: once a position has been zeroed the loop below skips it
   on `if(!ud.PlaybackPositionTicks)continue`. */
var pending=[],k;
for(k in sfHidden){if(sfHidden.hasOwnProperty(k)&&!sfCwPurged[k])pending.push(k);}
if(!pending.length)return;
for(k=0;k<pending.length;k++)sfCwPurged[pending[k]]=1;   /* claim before the async call */
var uid=ac.getCurrentUserId();
/* Reset the ids DIRECTLY rather than intersecting with /Items/Resume.
   The first version did that intersection and cleared almost nothing: the
   removed items were on the Continue Watching ROW but did not come back in the
   Resume query response, so the loop matched none of them and every position
   survived. We already hold the ids -- the round trip added nothing but a way
   to miss. Each id is attempted once (claimed above), so a POST for an item
   that is already at 0 is harmless and never repeats. */
var j,rawIds=[];
for(j=0;j<pending.length;j++)rawIds.push(sfHiddenRaw[pending[j]]||pending[j]);
/* sf-cwrm-reset: ask about each hidden item's SERIES in the same round trip,
   so 'watched the show again' can retire the hide, not just 'watched that
   exact episode again'. */
var _sid,_seen={};
for(j=0;j<pending.length;j++){
_sid=sfHiddenSeries[pending[j]];
if(_sid&&!_seen[_sid]){_seen[_sid]=1;rawIds.push(_sid);}
}
/* sf-cw-rewatch (2026-08-20). The version above fired the POSTs blindly, once
   per page load, forever -- and that is silent DATA LOSS. Measured: seed a
   40-minute position on a title that had ever been removed from Continue
   Watching, load #/home, and the position is back to 0. Remove something from
   the row once and you can never keep a resume point on it again, on any
   device. Ten of these went out at ~1.0s of EVERY home load, for every user
   with a hidden-content.json.
   So ask the server what the state actually is before writing:
     - played AFTER it was hidden  -> they came back to it. Drop the hide
       entirely and keep the position; the item belongs on the row again.
     - position already 0          -> nothing to purge. This is the steady
       state, so the write storm disappears once things settle.
     - otherwise                   -> the original purge, exactly once.
   One batched GET replaces up to N blind POSTs. */
if(!rawIds.length)return;
try{
ac.getJSON(ac.getUrl('Users/'+uid+'/Items',{Ids:rawIds.join(','),
Fields:'UserData',Limit:rawIds.length})).then(function(r){
var list=(r&&r.Items)||[],n,it,ud,nid,lp,hid,unhide=[],played={},unplayedNow={};
for(n=0;n<list.length;n++){
it=list[n];ud=it.UserData||{};
played[sfNorm(it.Id)]=ud.LastPlayedDate?Date.parse(ud.LastPlayedDate):0;
if(ud.UnplayedItemCount!=null)unplayedNow[sfNorm(it.Id)]=ud.UnplayedItemCount;
}
for(n=0;n<list.length;n++){
it=list[n];ud=it.UserData||{};nid=sfNorm(it.Id);
hid=sfHiddenWhen[nid]||0;
if(!hid)continue;                       /* a series we only asked about */
lp=played[nid]||0;
/* The SHOW being watched again is checked separately, against live Next Up --
   see sf-cwrm-moved. Two dead ends got us here, both measured, both worth not
   repeating: a Series carries NO LastPlayedDate (its UserData is only
   UnplayedItemCount/PlaybackPositionTicks/PlayCount/IsFavorite/Played/Key), and
   a baseline count cannot be stored alongside the hide because the plugin
   REWRITES the file through its own schema and silently drops any field it does
   not know -- verified by round-tripping SfUnplayed and CustomProbeField, both
   gone on read-back. So no custom state can live in that file. */
if(isFinite(lp)&&lp>hid){
/* watched again since the hide -- honour that, not the old removal, and
   take the entry off the SERVER so it cannot come back on the next load */
if(sfHidden)delete sfHidden[nid];
delete sfHiddenWhen[nid];
delete sfCwPurged[nid];
unhide.push(sfHiddenRaw[nid]||it.Id);
continue;
}
if(!ud.PlaybackPositionTicks)continue;
(function(iid){
try{
ac.ajax({type:'POST',
url:ac.getUrl('UserItems/'+iid+'/UserData',{userId:uid}),
contentType:'application/json',
data:JSON.stringify({PlaybackPositionTicks:0,Played:false})}).catch(function(){});
}catch(e){}
})(it.Id);
}
}).catch(function(){});
}catch(e){}
}
/* sf-cw-mark: marking is split OUT of sfHideCW on purpose.
   sfHideCW() also runs sfCwPurge(), which WRITES UserData (it zeroes
   PlaybackPositionTicks). That must stay event-driven -- looping it would
   re-purge continuously, and a purge running on every pass is exactly how
   resume positions were once wiped for every user. sfCwMark() only adds and
   removes a class, so it is safe to run on a timer.
   Needed because sfHideCW was only ever called from the action-sheet click
   handler: on a FRESH load of the Audiobooks page it never ran at all, and
   that page builds its 'Continue listening' shelf ~16s in -- long after any
   one-shot pass would have finished. Measured: the removed book still showed
   there with sf-cw-hidden absent. */
function sfCwMark(){
if(!sfHidden)return;
var rows=document.querySelectorAll('.verticalSection.ContinueWatching,.sf-cwscope');
for(var i=0;i<rows.length;i++){
var cards=rows[i].querySelectorAll('.card,.sf-ml-card');
for(var j=0;j<cards.length;j++){
var id=sfNorm(cards[j].getAttribute('data-id'));
if(id&&sfHidden[id])cards[j].classList.add('sf-cw-hidden');
else cards[j].classList.remove('sf-cw-hidden');
}
}
}
setInterval(function(){try{sfLoadHidden(false);sfCwMark();}catch(e){}},1000);
/* sf-cwrm (2026-08-29). The admin: "remove the 3 dots from the bottom right of each
   poster and card on my home, then make an on hover icon for remove from for
   next up and continue watching which would do the same thing as remove from
   continue watching."
   Writes the SAME store the old menu item wrote -- Jellyfin Enhanced's
   hidden-content.json (GET and POST both verified 200) -- so this is not a
   parallel mechanism: sfLoadHidden picks the entry up on its next pass and
   sf-cw-purge then clears the resume position server-side, which is what makes
   the removal real on every device rather than just in this browser.
   Entry shape copied from a real file: key AND ItemId are the DASHED guid,
   HideScope 'continuewatching', HiddenAt an ISO stamp (sf-cw-rewatch compares
   that against LastPlayedDate, so it must be honest).
   The card is hidden locally the moment it is clicked, because the round trip
   plus the next sfLoadHidden is far too slow to feel like a button. */
function sfDashId(u){
u=String(u||'').replace(/-/g,'');
if(u.length!==32)return u;
return u.substr(0,8)+'-'+u.substr(8,4)+'-'+u.substr(12,4)+'-'+u.substr(16,4)+'-'+u.substr(20);
}
/* sf-cwwl: Likes is the watchlist. Same endpoints jf-watchlist-btn verified. */
function sfWlToggle(btn,id){
var ac=window.ApiClient;
if(!ac||!ac.getCurrentUserId||!id)return;
var uid=ac.getCurrentUserId();
if(!uid)return;
/* called from the action sheet, where there is no button to paint */
var on=!!(btn&&btn.classList.contains('sf-wl-on'));
if(btn){btn.classList.toggle('sf-wl-on',!on);
btn.title=(!on)?'Remove from Watchlist':'Add to Watchlist';}
try{
ac.ajax({type:(on?'DELETE':'POST'),
url:ac.getUrl('Users/'+uid+'/Items/'+id+'/Rating'+(on?'':'?Likes=true'))})
.catch(function(){if(btn)btn.classList.toggle('sf-wl-on',on);});
}catch(e){if(btn)btn.classList.toggle('sf-wl-on',on);}
}
function sfCwRemove(card,id){
var ac=window.ApiClient;
if(!ac||!ac.getCurrentUserId||!id)return;
var uid=ac.getCurrentUserId();
if(!uid)return;
var key=sfDashId(id);
/* sf-cwrm-reset2 (2026-08-29). The admin: "be able to remove it so that it can come
   back instead of hiding it."
   So the two rows are treated as the different things they are:

   CONTINUE WATCHING -- there IS state behind the row (a resume position), so
   removal is a RESET of that state and nothing else. Clearing the position takes
   the item off the row for every client, and watching it again writes a new
   position and puts it straight back. No record is written anywhere, so there is
   nothing that can go stale or bury the item later. This is also the only form of
   removal that was ever durable; see sf-cw-purge.

   NEXT UP -- there is no state to reset. The episode is on the row purely because
   it is the next unwatched one, so the only way off is a hide. That hide carries
   the SeriesId and a real HiddenAt, and sf-cw-purge retires it (and deletes it
   from the server file) as soon as ANYTHING in that show is played afterwards --
   so removing an episode parks it, it does not bury it. */
try{card.classList.add('sf-cw-hidden');}catch(e){}
ac.getJSON(ac.getUrl('Users/'+uid+'/Items/'+id)).then(function(it){
var ud=(it&&it.UserData)||{};
if(ud.PlaybackPositionTicks){
/* Continue Watching: a reset, not a hide. */
return ac.ajax({type:'POST',
url:ac.getUrl('UserItems/'+id+'/UserData',{userId:uid}),
contentType:'application/json',
data:JSON.stringify({PlaybackPositionTicks:0,Played:false})});
}
/* Next Up: park it, and record what would bring it back. */
var sid=(it&&it.SeriesId)||'';
try{
sfHidden=sfHidden||{};
sfHidden[sfNorm(key)]=1;
sfHiddenRaw[sfNorm(key)]=key;
sfHiddenWhen[sfNorm(key)]=Date.now();
sfHiddenSeries[sfNorm(key)]=sfNorm(sid);
}catch(e){}
var path='JellyfinEnhanced/user-settings/'+uid+'/hidden-content.json';
/* take the show's unplayed count with us -- that is what will later say
   'they watched this show again' (see sf-cwrm-unplayed) */
return ac.getJSON(ac.getUrl('Users/'+uid+'/Items',{Ids:sid,Fields:'UserData'}))
.catch(function(){return null;})
.then(function(sr){
var sup=-1;
try{var s0=((sr&&sr.Items)||[])[0]||{};
if(s0.UserData&&s0.UserData.UnplayedItemCount!=null)sup=s0.UserData.UnplayedItemCount;}catch(e){}
try{sfHiddenUnplayed[sfNorm(key)]=sup;}catch(e){}
return ac.getJSON(ac.getUrl(path)).then(function(j){
j=j||{};
if(!j.Items)j.Items={};
if(j.Items[key])return;
j.Items[key]={ItemId:key,Name:(it&&it.Name)||'',Type:(it&&it.Type)||'',TmdbId:'',
HiddenAt:new Date().toISOString(),PosterPath:'',
SeriesId:sid,SeriesName:(it&&it.SeriesName)||'',
SeasonNumber:(it&&it.ParentIndexNumber)||null,
EpisodeNumber:(it&&it.IndexNumber)||null,
HideScope:'continuewatching'};
return ac.ajax({type:'POST',url:ac.getUrl(path),
contentType:'application/json',data:JSON.stringify(j)});
});
});
}).then(function(){try{sfLoadHidden(true);}catch(e){}})
.catch(function(){});
}
/* The button itself. Only on the two rows the admin named -- Continue Watching and
   Next Up -- because 'remove' means nothing on Recently Added. */
/* sf-emptyrow (2026-08-29). The admin: "next up row still shows up when empty on
   home." Removing every item from Next Up left the section behind -- a title,
   the scroll arrows and nothing under them. sfHideEmptySections already does
   this job but is gated to #/music, so home never had it.
   The test is deliberately NARROW: hide a row only when it HAS cards and every
   one of them is .sf-cw-hidden. A row with no cards at all is left alone,
   because that is also what a row looks like before it has loaded -- and hiding
   those would make rows disappear and pop back on every home load.
   Marked with a data ATTRIBUTE, not a class: a class starting with 'sf-' is what
   made the music version flip display on and off once per tick forever, because
   its own ownership test matched the marker it had just written. */
function sfEmptyRow(){
if((location.hash||'').indexOf('#/home')!==0)return;
var secs=document.querySelectorAll('#indexPage .verticalSection'),i,j;
for(i=0;i<secs.length;i++){
var sec=secs[i];
var cards=sec.querySelectorAll('.card[data-id],.sf-ml-card[data-id]');
if(!cards.length){sec.removeAttribute('data-sf-emptyrow');continue;}
var vis=0;
for(j=0;j<cards.length;j++)if(!cards[j].classList.contains('sf-cw-hidden'))vis++;
if(vis)sec.removeAttribute('data-sf-emptyrow');
else sec.setAttribute('data-sf-emptyrow','1');
}
}
function sfSheetWl(){
/* sf-sheet-wl (2026-08-29). The admin: "we want the 3 dots button to come back when
   you hover over it and users can add to watchlist in that menu and we already
   have a remove from option there that works."
   So a card gets NO extra icons at all -- the corner menu is the single place
   these actions live, and this adds one item to Jellyfin's own action sheet.
   The item is CLONED from a real .actionSheetMenuItem rather than built from
   scratch, which is what makes it match Abyss and the neighbouring rows exactly:
   it inherits the sheet's font, padding, height, hover and ripple, and cannot
   drift when the theme changes. (Building one by hand is how it ends up as a
   stray white bar -- the icon and the styling both live in the theme.)
   The sheet carries no item id of its own, so the id is captured from whichever
   card opened it, in the CAPTURE phase before Jellyfin handles the click.
   Watchlist is Jellyfin's Likes flag -- the endpoints jf-watchlist-btn verified:
     POST   /Users/{uid}/Items/{id}/Rating?Likes=true
     DELETE /Users/{uid}/Items/{id}/Rating */
if(!window.__sfSheetWl){
window.__sfSheetWl=1;
document.addEventListener('click',function(e){
try{
var t=e.target&&e.target.closest?e.target.closest('[data-action="menu"]'):null;
if(!t)return;
var card=t.closest('[data-id]');
window.__sfMenuId=card?(card.getAttribute('data-id')||''):'';
/* sf-menu-trim: remember WHICH row this came from. Continue Watching and Next
   Up already carry Jellyfin Enhanced's own Remove, and the admin does not want a
   watchlist entry competing with it there -- "for next up and continue watching
   row we dont need the add to watchlsit icon". */
window.__sfMenuCw=!!(card&&card.closest&&card.closest(
'.verticalSection.ContinueWatching,.verticalSection.NextUp,.sf-cwscope'));
}catch(x){}
},true);
}
var id=window.__sfMenuId||'';
if(!id)return;
/* sf-menu-trim: Continue Watching / Next Up keep their own Remove and nothing
   else of ours. Every other row still gets Add to Watchlist. */
if(window.__sfMenuCw)return;
var sheets=document.querySelectorAll('.actionSheet'),i;
for(i=0;i<sheets.length;i++){
var sh=sheets[i];
if(sh.getAttribute('data-sf-wl'))continue;
var proto=sh.querySelector('.actionSheetMenuItem');
if(!proto)continue;                    /* the sheet exists but is not filled yet */
sh.setAttribute('data-sf-wl','1');
var item=proto.cloneNode(true);
item.removeAttribute('data-id');
item.removeAttribute('data-action');
item.classList.add('sf-wl-item');
var tx=item.querySelector('.actionSheetItemText');
if(tx)tx.textContent='Add to Watchlist';
else item.textContent='Add to Watchlist';
/* sf-wl-item-fit: KEEP the cloned icon node, just blank it.
   Removing it made our row 40px tall against the sheet's 48px -- the icon is
   what holds that height. Blanking the ligature also avoids the font-display
   :swap flash that makes the neighbouring Remove row read 'visibility_off'
   until the icon font lands; ours gets its glyph from CSS instead. */
var ic=item.querySelector('.actionsheetMenuItemIcon,.material-icons');
if(ic){ic.textContent='';ic.classList.add('sf-wl-ico');}
(function(itemId){
item.addEventListener('click',function(e){
e.preventDefault();e.stopPropagation();
if(e.stopImmediatePropagation)e.stopImmediatePropagation();
sfWlToggle(null,itemId);
/* the sheet closes through history, never by removing the node -- sf-sheet-close */
try{history.back();}catch(x){}
},true);
})(id);
/* after the first action rather than above it: Play should stay the top row */
proto.parentNode.insertBefore(item,proto.nextSibling);
}
}
function sfHideCW(){
sfLoadHidden(false);
sfCwPurge();
if(!sfHidden)return;
var rows=document.querySelectorAll('.verticalSection.ContinueWatching,.sf-cwscope');
for(var i=0;i<rows.length;i++){
var cards=rows[i].querySelectorAll('.card,.sf-ml-card');
for(var j=0;j<cards.length;j++){
var id=sfNorm(cards[j].getAttribute('data-id'));
if(id&&sfHidden[id])cards[j].classList.add('sf-cw-hidden');
else cards[j].classList.remove('sf-cw-hidden');
}
}
}
/* sf-capsule-progress: the progress bar ran the full width of the capsule's TOP
   edge, where the 18px corner radius clipped both of its ends -- it read as a
   stray line rather than a control. Apple puts it UNDER the track text, spanning
   the text block. It is MOVED rather than restyled because it is a sibling of
   the info container, not a child, so no CSS could inset it to the text without
   hardcoding the transport and right-cluster widths -- and those change with
   which controls are shown. Moved back whenever the capsule is not in play, so
   the phone bar (which positions it at the top edge by design, see
   jf-mobile-player) is left exactly as it was. */
function sfCapsuleProgress(){
var top=document.querySelector('.nowPlayingBarTop');
var info=document.querySelector('.nowPlayingBarInfoContainer');
var pos=document.querySelector('.nowPlayingBarPositionContainer');
if(!top||!info||!pos)return;
var wide=window.innerWidth>=700&&document.body.classList.contains('sf-audio-playing');
if(wide){if(pos.parentElement!==info)info.appendChild(pos);}
else{if(pos.parentElement!==top)top.insertBefore(pos,top.firstChild);}
}
/* sf-progress-paint: the capsule's progress fill never moved, while the slider
   THUMB tracked correctly -- which is the clue to the cause. Jellyfin advances
   the bar by ASSIGNING input.value, and assigning .value fires no 'input'
   event, so MDL never runs the handler that resizes its own track: measured
   background-lower stuck at width 0 and background-upper frozen at 57px across
   a 6s sample while input.value went 22.29 -> 69.27. The native thumb is
   positioned by the browser straight from .value, so it alone kept up.
   Rather than synthesise events at MDL (which would also fight its drag
   handling), the MDL track is hidden and the fill is painted from input.value,
   which is a 0-100 PERCENT and is authoritative for remote/cast playback too --
   verified 11.1% against the audio element's own 11.3%. */
function sfProgressPaint(){
var pc=document.querySelector('.nowPlayingBarPositionContainer');
if(!pc)return;
var inp=pc.querySelector('input');
if(!inp)return;
var max=parseFloat(inp.max)||100;
var val=parseFloat(inp.value)||0;
var pct=val/max*100;
if(pct<0)pct=0;
if(pct>100)pct=100;
pc.style.setProperty('--sf-prog',pct.toFixed(2)+'%');
}
/* sf-lyrics: Apple's side panel. Jellyfin ships an .openLyricsButton but it is
   .hide on this build and routes to a whole page instead of a panel.
   Handles BOTH shapes the API returns -- plain {Text} lines, and synced lines
   carrying Start (in TICKS, 10,000,000 per second). Nothing here requires synced
   lyrics; the highlight simply lights up when they are present, which is what
   installing a provider such as LrcLib would add. Measured coverage on this
   library at the time of writing: 10/40 tracks, none synced. */
var sfLyrState={id:null,lines:[],synced:false,el:null};
function sfLyricsPanel(){
if(sfLyrState.el&&document.body.contains(sfLyrState.el))return sfLyrState.el;
var p=document.createElement('div');
p.className='sf-lyrics';
/* sf-flyr-entry: the expand button lives HERE, not on the capsule. The capsule
   already carries lyrics/cast/volume and is deliberately small; and reaching
   fullscreen lyrics via the lyrics panel is the same path Apple Music uses. */
p.innerHTML='<div class="sf-lyrics-hd"><h3></h3><button class="sf-lyrics-full" title="Fullscreen lyrics"><span class="material-icons" aria-hidden="true">open_in_full</span></button><button class="sf-lyrics-x" title="Close"><span class="material-icons" aria-hidden="true">close</span></button></div><div class="sf-lyrics-sub"></div><div class="sf-lyrics-body"></div>';
p.querySelector('.sf-lyrics-x').addEventListener('click',function(){sfLyricsClose();});
p.querySelector('.sf-lyrics-full').addEventListener('click',function(){
sfLyricsClose();      /* one lyrics surface at a time */
sfFlyrOpen();
});
/* sf-lyrpanel-seek: tap a line to jump there, same as fullscreen. Without it the
   two surfaces behave differently for the same gesture, which is worse than the
   feature being absent from both. */
p.addEventListener('click',function(e){
var line=e.target&&e.target.closest?e.target.closest('.sf-lyrics-body p'):null;
if(!line||line.classList.contains('sf-lyr-blank'))return;
var rows=[].slice.call(p.querySelectorAll('.sf-lyrics-body p'));
var i=rows.indexOf(line);
var au=document.querySelector('audio');
if(i>=0&&sfLyrState.lines[i]){
if(sfPlayerDead()){sfPlayFrom(sfCurrentTrackId(),sfLyrState.lines[i].Start);}
else if(au){try{au.currentTime=sfLyrState.lines[i].Start/10000000;if(au.paused)au.play();}catch(err){}}
}
});
document.body.appendChild(p);
sfLyrState.el=p;
return p;
}
function sfLyricsClose(){
var p=sfLyrState.el;
if(p)p.classList.remove('sf-open');
document.body.classList.remove('sf-lyrics-open');
var b=document.querySelector('.sf-lyr-btn');
if(b)b.classList.remove('sf-on');
}
/* the now-playing bar's rating button carries the CURRENT TRACK's id -- the same
   hook sfPlayingRow uses, verified equal to .listItem[data-id] on a live page. */
function sfCurrentTrackId(){
var ub=document.querySelector('.nowPlayingBarUserDataButtons button');
return ub?ub.getAttribute('data-id'):null;
}
function sfLoadLyrics(id){
var p=sfLyricsPanel();
var body=p.querySelector('.sf-lyrics-body');
var sub=p.querySelector('.sf-lyrics-sub');
var t=document.querySelector('.nowPlayingBarText');
p.querySelector('h3').textContent=(t&&t.children[0])?t.children[0].textContent:'Lyrics';
sfLyrState.id=id;sfLyrState.lines=[];sfLyrState.synced=false;
body.innerHTML='';sub.textContent='';
var ac=window.ApiClient;
if(!ac)return;
ac.getJSON(ac.getUrl('Audio/'+id+'/Lyrics')).then(function(j){
if(sfLyrState.id!==id)return;
var lines=(j&&j.Lyrics)||[];
if(!lines.length){body.innerHTML='<div class="sf-lyrics-empty">No lyrics available for this track.</div>';return;}
sfLyrState.lines=lines;
sfLyrState.synced=lines[0].Start!=null;
sub.textContent=sfLyrState.synced?'Synced':'';
for(var i=0;i<lines.length;i++){
var el=document.createElement('p');
var txt=lines[i].Text||'';
if(!txt.trim())el.className='sf-lyr-blank';else el.textContent=txt;
body.appendChild(el);
}
}).catch(function(){
if(sfLyrState.id!==id)return;
body.innerHTML='<div class="sf-lyrics-empty">No lyrics available for this track.</div>';
});
}
/* sf-fav-repair: Home -> Live TV -> Sports -> My Stuff left My Stuff PERMANENTLY
   EMPTY. Reproduced and measured: the visible #favoritesTab had .sections present
   but ZERO .verticalSection children, and its My Stuff button was already marked
   -active, so clicking it again did nothing (no change, no render). Bouncing to
   Home and back restored it instantly -- 16 sections, cards present -- which
   proves the content renders fine and the tab simply never received a CHANGE.
   Cause: "?tab=N is only honoured on a fresh page load". Arriving from
   #/home?sports=1, the hash goes to #/home?tab=1 but the route does not
   re-enter, so Jellyfin's tab controller never switches -- while our own code
   marks the pill active and reveals the pane. Shown but never rendered.
   This repairs the state generically, whatever path caused it, in the spirit of
   jf-pane-guard: if the tab is empty for >1.5s, drive Jellyfin's OWN buttons
   (Home, then My Stuff) so its controller emits a real change.
   Strictly one attempt per hash visit -- an account with genuinely zero
   favourites must not bounce forever. */
var sfFavHash='',sfFavSeen=0,sfFavFixed='';
function sfHomeTabRepair(){
var h=location.hash||'';
if(h.indexOf('/home')===-1||h.indexOf('tab=1')===-1){sfFavHash='';sfFavSeen=0;return;}
var all=document.querySelectorAll('#favoritesTab'),ft=null,i;
for(i=0;i<all.length;i++)if(all[i].offsetParent!==null)ft=all[i];
if(!ft)return;
if(ft.querySelectorAll('.verticalSection').length>0){sfFavSeen=0;return;}
if(h!==sfFavHash){sfFavHash=h;sfFavSeen=Date.now();sfFavFixed='';return;}
if(sfFavFixed===h)return;
/* sf-repair-dwell: was 1500ms, which fired on merely SLOW loads, not stuck ones.
   Measured on a healthy server, #favoritesTab fills in ~200ms; the 1.5s window
   was well inside the range a loaded NAS takes legitimately, so the repair ran
   during ordinary navigation. Because it is guarded by sfFavFixed (once per
   URL), that presented as "the page reloads the FIRST time I open My Stuff".
   4s is past any normal fill and still recovers a genuinely empty pane. */
if(Date.now()-sfFavSeen<4000)return;
sfFavFixed=h;
var bars=document.querySelectorAll('.headerTabs .emby-tabs-slider'),bar=null,j;
for(j=0;j<bars.length;j++)if(bars[j].offsetParent!==null)bar=bars[j];
if(!bar)return;
/* Jellyfin's own tab buttons are the ones we did not inject */
var natives=[],k,c;
for(k=0;k<bar.children.length;k++){
c=bar.children[k];
if(c.className.indexOf('jf-livetv-tab')===-1&&c.className.indexOf('jf-sports-tab')===-1&&c.className.indexOf('jf-sp-tab')===-1&&c.className.indexOf('jf-home-tab')===-1)natives.push(c);
}
if(natives.length<2)return;
/* sf-repair-silent: the recovery is a forced re-render, but it was performed in
   full view -- natives[0] is HOME, so the whole home screen (111 cards, measured)
   painted for ~230ms before the tab snapped back. That flash IS what users read
   as a reload. Hide the page for the hop; the pane is being rebuilt anyway, so
   there is nothing meaningful to look at. Restore is belt-and-braces: after the
   second click AND on an unconditional timer, so a failed click can never leave
   the page invisible. */
var pgs=document.querySelectorAll('.page'),pg=null,q;
for(q=0;q<pgs.length;q++)if(pgs[q].offsetParent!==null)pg=pgs[q];
var restore=function(){if(pg){pg.style.opacity='';pg.style.transition='';}};
if(pg){pg.style.transition='none';pg.style.opacity='0';}
natives[0].click();
setTimeout(function(){natives[natives.length-1].click();setTimeout(restore,140);},260);
setTimeout(restore,2500);
}
/* sf-ltv-settle: reloading on Live TV showed a different tab strip for a split
   second -- Jellyfin paints its own Programs/Guide/Channels/... strip, then our
   nav parks it off-screen and draws the four main pills.
   This inline script runs BEFORE jellyfin-web's deferred bundles, so the strip
   can be held invisible from the very first paint and revealed once our pills
   exist. Same approach as jf-btn-settle. visibility, not display, so the header
   keeps its height and nothing below it jumps. The 2.5s watchdog means a failure
   to draw pills can never leave the bar permanently hidden. */
/* sf-ltv-alias: Live TV was the only main pill whose URL was not #/home... --
   Home, Sports and My Stuff are all the SAME page (#indexPage) with a different
   query string, while Live TV is genuinely one of Jellyfin's own routes and
   mounts a different page (#liveTvSuggestedPage).
   Re-hosting it for real is not a copy-paste: that page is rendered by
   Jellyfin's route controller out of a code-split chunk, with its own lifecycle,
   data fetching and emby-tabs panes -- copied markup would be dead HTML and the
   guide/channels/recordings would stop working.
   So the PAGE is left exactly where it is and only the ADDRESS BAR is aliased.
   history.replaceState does not re-enter the router (the same property
   jf-mystuff-urlsync relies on), verified here: after the rewrite the page was
   still #liveTvSuggestedPage with all 126 cards and its sub-pills intact.
     real route  #/livetv?tab=N   <->   shown as  #/home?livetv=1[&sub=N]
   Cold entry on the aliased URL has to bounce through the real route once,
   because Jellyfin only honours ?tab=N on a fresh load. That settles in one
   pass: forward -> Jellyfin mounts -> rewrite -> the guard below sees the page
   already mounted and stops, so it cannot ping-pong. */
function sfLtvVisiblePage(){
var pages=document.querySelectorAll('.mainAnimatedPages > .page'),i;
for(i=pages.length-1;i>=0;i--)if(pages[i].offsetParent!==null)return pages[i].id||'';
return '';
}
'''

# _LS_05 (orig L2889-3629) -- sf-ltv-backout, sf-ltv-pane-dest, sf-ltv-realurl
_LS_05 = r'''/* sf-ltv-backout: the alias made the Back button a TRAP. Measured: from home ->
   Live TV, two consecutive history.back() calls both ended on
   #/home?livetv=1 / liveTvSuggestedPage -- you could never leave.
   Why: the address says /home while the mounted page is liveTvSuggestedPage, so
   when Back pops onto that entry the router honours the URL and mounts HOME;
   the guard below then sees "wrong page" and bounces forward to Live TV again.
   Every Back press re-entered Live TV.
   Back means two different things on this entry and the hash alone cannot tell
   them apart:
     video player -> Back  = "return TO Live TV"     (must bounce)
     Live TV      -> Back  = "leave Live TV"         (must NOT bounce)
   popstate fires BEFORE the router swaps pages, so whatever is on screen at that
   instant is the page being left -- which is exactly the missing signal. */
var sfLtvBackFrom='';
window.addEventListener('popstate',function(){
try{sfLtvBackFrom=sfLtvVisiblePage();}catch(e){sfLtvBackFrom='';}
});
function sfLtvAlias(){
var h=location.hash||'';
if(h.indexOf('#/home?livetv=1')===0){
/* already showing the real page -- nothing to do, just keep the alias */
if(sfLtvVisiblePage()==='liveTvSuggestedPage'){sfLtvBackFrom='';return;}
if(sfLtvBackFrom==='liveTvSuggestedPage'){
/* They pressed Back while ON Live TV: they want out. Let the home page the
   router already mounted stand, and drop the alias so the address is honest
   again -- otherwise the next tick would read it as Live TV and bounce back. */
sfLtvBackFrom='';
try{history.replaceState(null,'','#/home');}catch(e){}
return;
}
/* sf-ltv-pane-dest (2026-08-29): #/home?livetv=1 is now a REAL destination --
   the Live TV home pane renders there, so this legacy rescue must not bounce it
   to the route any more. It was kept in 2026-08-10 only so an old bookmark
   holding the retired alias reached SOMETHING instead of a blank page; landing
   on the pane is a better answer than the route it used to be sent to.
   Leaving it in place made the pill flash the pane and then jump straight to
   liveTvSuggestedPage -- measured hash #/livetv?tab=0 with the pane built but
   hidden. */
return;
}
/* sf-ltv-realurl (2026-08-10): the rewrite of #/livetv -> #/home?livetv=1 is
   GONE, on the admin's call. It bought a cosmetically consistent pill URL and cost
   more than it was worth:
     - the address bar visibly flickered on the way in, because the router MUST
       see the real #/livetv hash to navigate, so the true URL always painted
       for a frame before being rewritten;
     - it made Back a trap (measured: two consecutive back presses never left
       Live TV), because the entry said /home while liveTvSuggestedPage was
       mounted, so Back mounted home and the guard bounced forward again;
     - and it left every page hidden on the way back from a programme page.
   Live TV now simply keeps its own route. The reverse branch above is KEPT so
   any old bookmark or history entry still holding #/home?livetv=1 is carried to
   the real route instead of showing a blank page. */
}
/* sf-ltv-alias: ONE definition of "is this the Live TV route", exported the
   same way jf-view-scope exports __jfView, because aliasing the URL breaks every
   patch that recognised Live TV by its hash -- and they live in separate script
   blocks. Each caller keeps an inline fallback so load order cannot matter. */
window.__sfLtv={
is:function(h){h=h||location.hash||'';return h.indexOf('#/livetv')===0||h.indexOf('#/home?livetv=1')===0;},
tab:function(h){h=h||location.hash||'';
var m=(h.indexOf('#/home?livetv=1')===0)?/[?&]sub=(\d+)/.exec(h):/[?&]tab=(\d+)/.exec(h);
return m?parseInt(m[1],10):0;}
};
/* sf-tab-fouc: on reload the main pill bar painted as SQUARE unstyled buttons and
   then snapped into capsules. Not our pills' fault -- the capsule styling lives in
   Jellyfin's ROUTE-LEVEL code-split CSS (home.<hash>.css), which arrives after the
   header has painted. Verified by listing which sheets carry the
   .emby-tab-button radius/background: "home" and "livetv-livetvsuggested", i.e.
   per-route chunks, not the main bundle.
   The signal is therefore "has the capsule CSS arrived", which is measurable: a
   styled pill computes border-radius 50px, an unstyled one 0. Reveal at >=20px.
   visibility (not display) keeps the header's height so nothing below jumps, and
   a 3s watchdog means a square-pill theme, or any load failure, can never leave
   the bar hidden. Emitted from this script so it cannot exist if the patch does
   not run. */
var sfTabArmed=0;
function sfTabArm(){
if(document.documentElement.classList.contains('sf-tabs-unstyled'))return;
document.documentElement.classList.add('sf-tabs-unstyled');
sfTabArmed=Date.now();
}
/* sf-strip-state: ONE reader for "is the pill strip finished?", shared by the
   visibility guard (sf-tabs-unstyled) and the fade guard (sf-hdr-ready). Returns
   null until a strip is actually PAINTED with pills in it, so no caller can
   reason about a strip that does not exist yet. */
function sfStripState(){
var bars=document.querySelectorAll('.headerTabs .emby-tabs-slider'),bar=null,i,j;
for(i=0;i<bars.length;i++){
if(bars[i].getBoundingClientRect().width<20)continue;
bar=bars[i];break;
}
if(!bar)return null;
var pills=[],c;
for(j=0;j<bar.children.length;j++){c=bar.children[j];
if(getComputedStyle(c).display==='none')continue;
if(c.getBoundingClientRect().width<=0)continue;
pills.push(c);}
if(!pills.length)return null;
var styled=(parseFloat(getComputedStyle(pills[0]).borderRadius)||0)>=20;
var labelled=true,key;
for(j=0;j<pills.length;j++){
if(!(pills[j].textContent||'').trim()){labelled=false;break;}
key=pills[j].getAttribute('data-sf-nav');
/* still showing the English key in a translated UI means the i18n sweep has
   not run over this strip yet */
if(key&&sfHdrLang()&&(pills[j].textContent||'').trim()===key){labelled=false;break;}
}
return {bar:bar,pills:pills,styled:styled,labelled:labelled,n:pills.length};
}
/* sf-reveal: hold the strip until it is REAL -- painted, styled by the route CSS,
   and carrying final labels -- with the fail-open deadline armed from the moment
   the strip first APPEARS rather than from an early boot moment.

   Why this had to change. Measured on WebKit at 390px: sf-tabs-unstyled was armed
   at 4274ms and its 3000ms watchdog expired at 7280ms; sf-hdr-ready's 4000ms
   deadline expired at 8500ms; the pills did not render until 8749ms. BOTH
   deadlines therefore fired before the thing they were guarding existed, so every
   reveal took the fail-open path and the guards protected nothing. The user saw
   289ms of square (radius 0), 10.96px, 50px-wide pills snap to round 50 / 14.43px
   / 60px -- exactly "the nav pill tab starts small and then loads in the correct
   size". A deadline has to be the last resort, not the normal path.

   Fail-open is PRESERVED, with two deadlines that can both still fire:
     STRIP_CAP 1800ms after the strip is first seen -- a square-pill theme, or
               route CSS that never lands, still reveals promptly.
     BOOT_CAP  25s after this script runs -- if a strip never appears at all,
               nothing stays hidden forever.
   Reveal order is deliberate: visibility is dropped one frame BEFORE the opacity
   class lands, so the existing .2s opacity transition actually runs and the bar
   fades in instead of snapping. */
var SF_STRIP_SEEN=0,SF_BOOT_CAP=Date.now()+25000,SF_REVEALED=0;
function sfStripReveal(animate){
if(SF_REVEALED)return;
SF_REVEALED=1;
var de=document.documentElement;
/* Apply the overflow tiers while still hidden so the first VISIBLE frame is
   already final geometry. Without this the bar walks down tight/tighter/
   tightest in public: measured 50->40->39->38->37->36px wide and 11->9.4px font
   over 170ms, then a snap back to 60px/14.4px once the route CSS arrived. */
try{sfPillFit();}catch(e){}
de.classList.remove('sf-tabs-unstyled');
/* sf-hdr-behind-splash (2026-09-04). The admin: the header has to show up fast --
   it is what you navigate with.
   Measured boot: the pill strip is complete at 1844ms, but the splash does not
   lift until 2258ms, and the header then spent another ~280ms fading IN FRONT of
   the user -- fully visible only at 2574ms. The fade was costing time on the one
   control you need first.
   So when the splash is still up, reveal WITHOUT the entrance: the splash is an
   opaque full-screen cover, so there is nothing to see and nothing to hide, and
   the moment it lifts the header is simply already there -- which is how a native
   app boots. The fade is kept for the case the splash has already gone (a late
   strip rebuild), where it would genuinely be seen. */
var go=function(){
if(animate!==false)de.classList.add('sf-hdr-in');
de.classList.add('sf-hdr-ready');
/* one-shot: drop it once the entrance is over so a later strip rebuild
   does not re-fade the bar on every navigation */
try{setTimeout(function(){try{de.classList.remove('sf-hdr-in');}catch(e){}},700);}catch(e){}};
if(window.requestAnimationFrame)requestAnimationFrame(go);else go();
}
function sfTabSettle(){
if(SF_REVEALED)return;
var st=null;
try{st=sfStripState();}catch(e){st=null;}
if(st&&st.n>=2){
if(!SF_STRIP_SEEN)SF_STRIP_SEEN=Date.now();
/* sf-hdr-splashgate (2026-09-04). The rows got this guard and the header never
   did, so the header revealed while the splash was still covering the screen on
   5 of 7 measured loads -- its entrance spent behind the splash, exactly the
   fault sf-splash-gate was written for. Only the NORMAL path waits; the two
   deadlines below stay absolute so fail-open is unchanged and a splash that
   never clears can still never keep the header hidden. */
var _sp=document.querySelector('.splashLogo');
var _spUp=!!(_sp&&_sp.getClientRects().length);
/* The splash decides HOW to reveal, not WHETHER: holding the header back until
   the splash lifted is what made it arrive 316ms late. */
if(st.styled&&st.labelled){sfStripReveal(!_spUp);return;}
if(Date.now()-SF_STRIP_SEEN>1800)sfStripReveal(!_spUp);
return;
}
if(Date.now()>SF_BOOT_CAP)sfStripReveal(!_spUp);
}
/* sf-capsule-seek: clicking the bar landed nowhere near the pointer, and the
   error grew towards both ends. That is inherent to a native <input type=range>:
   the browser maps clientX across (width - thumbWidth) with the thumb CENTRED on
   the value, so the usable track is inset by half a thumb at each end and the
   two extremes are unreachable. Jellyfin ships a "slider-medium-thumb", which is
   a big thumb on a 234px bar.
   So the native mapping is switched off (pointer-events:none on the input, in
   CSS) and the position is computed straight from the container's own rect --
   an exact clientX -> percent, edge to edge. Verified that assigning value and
   dispatching 'change' really does seek: 20% -> 20.5%, 70% -> 70.5%.
   'input' fires continuously while dragging so the fill follows the pointer;
   'change' fires once on release so Jellyfin performs a single seek rather than
   one per pixel. */
function sfCapsuleSeek(){
var pc=document.querySelector('.nowPlayingBarPositionContainer');
if(!pc||pc.sfSeekBound)return;
var inp=pc.querySelector('input');
if(!inp)return;
pc.sfSeekBound=true;
function apply(clientX,commit){
var r=pc.getBoundingClientRect();
if(r.width<=0)return;
var pct=(clientX-r.left)/r.width*100;
if(pct<0)pct=0;
if(pct>100)pct=100;
inp.value=pct;
sfProgressPaint();
inp.dispatchEvent(new Event('input',{bubbles:true}));
if(commit)inp.dispatchEvent(new Event('change',{bubbles:true}));
}
pc.addEventListener('pointerdown',function(e){
if(window.innerWidth<700||!document.body.classList.contains('sf-audio-playing'))return;
e.preventDefault();
apply(e.clientX,false);
function mv(ev){apply(ev.clientX,false);}
function up(ev){
apply(ev.clientX,true);
document.removeEventListener('pointermove',mv);
document.removeEventListener('pointerup',up);
}
document.addEventListener('pointermove',mv);
document.addEventListener('pointerup',up);
});
}
/* sf-capsule-wire: document-level capture listeners, installed exactly once.
   Capture phase + stopImmediatePropagation is the same technique jf-watchlist-btn
   uses to take a control away from its original owner without replacing the node,
   so Jellyfin keeps rendering and re-rendering its own button. */
var sfWired=false;
function sfCapsuleWire(){
if(sfWired)return;
sfWired=true;
document.addEventListener('click',function(e){
if(!e.target||!e.target.closest)return;
var capsule=window.innerWidth>=700&&document.body.classList.contains('sf-audio-playing');
/* VOLUME: Apple's speaker is the last control and opens the slider on CLICK.
   Hover-to-expand meant the slider grew under the pointer whenever you reached
   for the heart or the overflow menu, so those became hard to hit. */
var mute=e.target.closest('.nowPlayingBar .muteButton');
if(mute){
if(!capsule)return;
e.preventDefault();
e.stopImmediatePropagation();
document.body.classList.toggle('sf-vol-open');
return;
}
/* a hide is applied through the card's action sheet; re-read JE's list shortly
   after so the card disappears without waiting for the 20s cache to lapse */
if(e.target.closest('.actionSheetMenuItem')||e.target.closest('.actionsheetMenuItem')){
setTimeout(function(){sfLoadHidden(true);setTimeout(sfHideCW,400);},1200);
}
var inBar=e.target.closest('.nowPlayingBar');
if(!inBar){
document.body.classList.remove('sf-vol-open');
return;
}
/* NO width gate here. `capsule` is innerWidth>=700, and gating the whole bar on
   it made the full-screen player DESKTOP ONLY: on a 412px phone this returned
   early, our opener never ran, and Jellyfin's stock "the whole bar is a link"
   took the tap to #/queue instead. Verified on a phone profile -- .sf-np was
   never even created. The volume popover below keeps its own `capsule` check,
   because that one really is a desktop affordance. */
/* dragging inside the volume slider must not be disturbed */
if(e.target.closest('.nowPlayingBarVolumeSliderContainer'))return;
/* the real controls (play, next, lyrics, cast, favourite, overflow) behave
   normally; they just dismiss the volume popover */
if(e.target.closest('button')){
document.body.classList.remove('sf-vol-open');
return;
}
/* THE WHOLE BAR IS A LINK IN STOCK JELLYFIN. Any click on it that is not a
   control navigates to #/queue -- so the capsule background, the padding around
   the artwork and even a released scrub all threw you onto another page. From
   here on nothing is allowed to reach that handler; only the artwork and the
   title/artist navigate, and they go to the ALBUM rather than the queue. */
e.preventDefault();
e.stopImmediatePropagation();
document.body.classList.remove('sf-vol-open');
/* the progress bar was already handled on pointerdown by sfCapsuleSeek */
if(e.target.closest('.nowPlayingBarPositionContainer'))return;
/* Tapping the artwork or the track text opens the FULL-SCREEN PLAYER
   (sf-now-immersive), which is what both Spotify and Apple Music do -- it used
   to jump to the album detail page, which took you away from listening. The
   album is still one tap away, from the player's own "Album" button.

   This has to live here rather than in sfNpWire: the handler below is
   registered on DOCUMENT in the capture phase and calls stopImmediatePropagation
   for any non-button click in the bar, so a listener bound to the bar itself can
   never run. Verified -- the bar showed data-sf-np="1" and still nothing fired. */
if(e.target.closest('.nowPlayingImage')||e.target.closest('.nowPlayingBarText')){
try{sfNpSetOpen(true);}catch(err){}
}
},true);
/* the progress fill is repainted off its own faster timer, and immediately on
   any slider input, so a seek SNAPS instead of sliding to the new position */
setInterval(sfProgressPaint,200);
document.addEventListener('input',function(e){
if(e.target&&e.target.classList&&e.target.classList.contains('nowPlayingBarPositionSlider'))sfProgressPaint();
},true);
}
/* sf-capsule-extras: lyrics + cast, the two controls Apple's capsule carries and
   ours did not. Cast FORWARDS to Jellyfin's own .headerCastButton rather than
   reimplementing device discovery -- clicking the real control keeps all of its
   state and its device list. */
function sfCapsuleButtons(){
var right=document.querySelector('.nowPlayingBarRight');
if(!right)return;
if(!right.querySelector('.sf-lyr-btn')){
var b=document.createElement('button');
b.className='sf-lyr-btn mediaButton paper-icon-button-light';
b.title='Lyrics';
b.innerHTML='<span class="material-icons" aria-hidden="true">lyrics</span>';
b.addEventListener('click',function(){
var p=sfLyricsPanel();
var open=!p.classList.contains('sf-open');
p.classList.toggle('sf-open',open);
document.body.classList.toggle('sf-lyrics-open',open);
b.classList.toggle('sf-on',open);
if(open){var id=sfCurrentTrackId();if(id)sfLoadLyrics(id);}
});
right.insertBefore(b,right.firstChild);
}
if(!right.querySelector('.sf-cast-btn')){
var c=document.createElement('button');
c.className='sf-cast-btn mediaButton paper-icon-button-light';
c.title='Cast';
c.innerHTML='<span class="material-icons" aria-hidden="true">cast</span>';
c.addEventListener('click',function(){
var h=document.querySelector('.headerCastButton');
if(h)h.click();
});
var lyr=right.querySelector('.sf-lyr-btn');
right.insertBefore(c,lyr?lyr.nextSibling:right.firstChild);
}
}
/* follows the track as it changes, and highlights the current line when the
   lyrics are synced. Start is in ticks: 10,000,000 per second. */
function sfLyricsTick(){
var p=sfLyrState.el;
if(!p||!p.classList.contains('sf-open'))return;
var id=sfCurrentTrackId();
if(id&&id!==sfLyrState.id){sfLoadLyrics(id);return;}
if(!sfLyrState.synced||!sfLyrState.lines.length)return;
var a=document.querySelector('audio');
if(!a)return;
var ticks=a.currentTime*10000000;
var idx=-1;
for(var i=0;i<sfLyrState.lines.length;i++){
if(sfLyrState.lines[i].Start<=ticks)idx=i;else break;
}
var rows=p.querySelectorAll('.sf-lyrics-body p');
if(idx<0||!rows.length)return;
if(rows[idx].classList.contains('sf-lyr-on'))return;
/* sf-lyrpanel-depth: the same distance falloff the fullscreen view uses, so the
   two surfaces read as one design instead of two. Kept lighter here (no blur on
   the near neighbours) because the panel is narrow and text is smaller -- blur
   at this size costs legibility for very little depth. */
var k,dist;
for(k=0;k<rows.length;k++){
dist=Math.abs(k-idx);
rows[k].className=rows[k].className.replace(/\s*sf-(lyr-on|p1|p2)\b/g,'');
if(dist===0)rows[k].className+=' sf-lyr-on';
else if(dist<=2)rows[k].className+=' sf-p1';
else rows[k].className+=' sf-p2';
}
/* The karaoke sweep is gone from BOTH surfaces -- our lyrics are line-level, so
   an interpolated wipe pointed at the wrong word on any line with a pause, and
   in this narrow column it also left the current line half-transparent. */
var lb=p.querySelector('.sf-lyrics-body');
/* 42%, matching the fullscreen view -- the current line holds a fixed spot just
   above centre so more of the song ahead stays visible than behind. */
var aimP=rows[idx].offsetTop-lb.clientHeight*0.42+rows[idx].offsetHeight/2;
try{lb.scrollTo({top:aimP,behavior:'smooth'});}
catch(e){lb.scrollTop=aimP;}
}
/* ------------------------------------------------------------------ sf-flyr
   Apple-Music-style FULLSCREEN lyrics: artwork on the left, synced lyrics on
   the right. Deliberately an ADDITIONAL mode -- the capsule player and the side
   lyrics panel are untouched, and this is entered from the panel's own expand
   button, so nothing changes for anyone who does not go looking for it.

   It reuses the existing engine rather than reimplementing it: the same
   Audio/{id}/Lyrics fetch, the same tick arithmetic (Start is in ticks,
   10,000,000 per second), and the same sfCurrentTrackId() hook. Only the
   presentation is new.

   Transport does NOT reimplement playback: it clicks Jellyfin's own now-playing
   buttons, the same trick sfCapsuleButtons uses for Cast -- so queue handling,
   reporting and device state all keep working. */
var sfFlyr={el:null,id:null,lines:[],synced:false,lastIdx:-1};
/* sf-flyr-revive: when a track finishes and nothing follows it, Jellyfin tears
   the player down -- measured after the last second: the <audio> element is left
   with readyState 0 and duration 0, and .nowPlayingBar goes display:none with
   its buttons at 0x0. So everything the fullscreen view drives was dead:
   clicking our transport hit hidden buttons with no player behind them, and
   tap-to-seek wrote currentTime to a torn-down element. Nothing responded, while
   the lyrics kept ticking.
   The cure is to start playback again rather than poke the corpse. Same route
   Media Bar uses for its hero Play button:
     POST /Sessions/{id}/Playing?playCommand=PlayNow&itemIds=...
   with startPositionTicks when we want to resume at a specific lyric. */
var sfSessId=null;
function sfSession(){
var ac=window.ApiClient;
if(sfSessId)return Promise.resolve(sfSessId);
if(!ac||!ac.getUrl)return Promise.resolve(null);
var dev='';
try{dev=ac.deviceId?ac.deviceId():'';}catch(e){}
return ac.getJSON(ac.getUrl('Sessions',dev?{deviceId:dev}:{})).then(function(list){
if(list&&list.length){sfSessId=list[0].Id;return sfSessId;}
return null;
}).catch(function(){return null;});
}
/* "dead" = the element exists but has no loaded media behind it any more. */
function sfPlayerDead(){
var a=document.querySelector('audio');
return !a||a.readyState===0||!a.duration;
}
function sfPlayFrom(itemId,ticks){
var ac=window.ApiClient;
if(!ac||!itemId)return false;
sfSession().then(function(sid){
if(!sid)return;
var q={playCommand:'PlayNow',itemIds:itemId};
if(ticks&&ticks>0)q.startPositionTicks=Math.round(ticks);
try{ac.ajax({type:'POST',url:ac.getUrl('Sessions/'+sid+'/Playing',q)}).catch(function(){});}catch(e){}
});
return true;
}
function sfFlyrClick(sel){
var i,b;
for(i=0;i<sel.length;i++){b=document.querySelector(sel[i]);if(b){b.click();return true;}}
return false;
}
function sfFlyrEl(){
if(sfFlyr.el&&document.body.contains(sfFlyr.el))return sfFlyr.el;
var d=document.createElement('div');
d.className='sf-flyr';
/* sf-flyr-ambient: Apple's fullscreen lyrics glow in the ARTWORK's own colours
   and drift. Rather than guess a palette, three copies of the cover art are
   blurred past recognition and animated on different periods -- the colour is
   therefore always exactly right for the track, with no canvas sampling, no
   palette extraction and nothing to get wrong on a cover we have never seen.
   A scrim sits over them so lyric contrast never depends on the artwork. */
d.innerHTML='<div class="sf-flyr-bg"><i></i><i></i><i></i><u></u></div>'
+'<button class="sf-flyr-x" title="Exit fullscreen"><span class="material-icons" aria-hidden="true">fullscreen_exit</span></button>'
+'<div class="sf-flyr-left">'
+'<div class="sf-flyr-art"><img alt=""></div>'
+'<div class="sf-flyr-meta"><h2></h2><p></p></div>'
+'<div class="sf-flyr-prog"><span></span></div>'
+'<div class="sf-flyr-ctl">'
+'<button data-a="prev" title="Previous"><span class="material-icons" aria-hidden="true">skip_previous</span></button>'
+'<button data-a="play" title="Play/Pause"><span class="material-icons" aria-hidden="true">play_arrow</span></button>'
+'<button data-a="next" title="Next"><span class="material-icons" aria-hidden="true">skip_next</span></button>'
+'</div></div>'
+'<div class="sf-flyr-right"><div class="sf-flyr-lines"></div></div>';
d.querySelector('.sf-flyr-x').addEventListener('click',function(){sfFlyrClose();});
/* sf-flyr-seek: tap a lyric to jump there. This is the feature that turns the
   screen from something you watch into something you use -- rewinding to the
   line you liked is otherwise a fiddle with the progress bar. Seeking the audio
   element directly is enough: Jellyfin's own progress reporting samples the
   element, so the server stays in step without us calling its player API. */
d.addEventListener('click',function(e){
var line=e.target&&e.target.closest?e.target.closest('.sf-flyr-lines p'):null;
if(line&&!line.classList.contains('sf-flyr-blank')){
var rows=[].slice.call(d.querySelectorAll('.sf-flyr-lines p'));
var i=rows.indexOf(line);
var au=document.querySelector('audio');
if(i>=0&&sfFlyr.lines[i]){
sfFlyr.lastIdx=-1;
if(sfPlayerDead()){sfPlayFrom(sfCurrentTrackId(),sfFlyr.lines[i].Start);}
else if(au){try{au.currentTime=sfFlyr.lines[i].Start/10000000;if(au.paused)au.play();}catch(err){}}
}
return;
}
var b=e.target&&e.target.closest?e.target.closest('.sf-flyr-ctl button'):null;
if(!b)return;
var a=b.getAttribute('data-a');
if(sfPlayerDead()){
/* nothing is loaded -- restart the track we are showing lyrics for */
if(a==='play'||a==='prev')sfPlayFrom(sfCurrentTrackId(),0);
else sfFlyrClick(['.nowPlayingBar .nextTrackButton','.nextTrackButton']);
return;
}
if(a==='play')sfFlyrClick(['.nowPlayingBar .playPauseButton','.playPauseButton']);
else if(a==='prev')sfFlyrClick(['.nowPlayingBar .previousTrackButton','.previousTrackButton']);
else if(a==='next')sfFlyrClick(['.nowPlayingBar .nextTrackButton','.nextTrackButton']);
});
document.body.appendChild(d);
sfFlyr.el=d;
return d;
}
/* ------------------------------------------------------- sf-flyr-beat
   Makes the ambient background breathe with the music.

   THE RISK, and why the order below is not negotiable:
   createMediaElementSource() permanently reroutes that <audio> element's output
   through the Web Audio graph. It cannot be undone for the life of the element,
   and if the graph does not reach a destination the track goes SILENT. Silent
   music is a far worse failure than a background that does not pulse, so:
     1. connect source -> destination FIRST, before anything else;
     2. only then tap the analyser off the source (the analyser is a dead end and
        is deliberately NOT connected onward -- doing so would double the signal);
     3. verify playback is still advancing, and if it is not, stop the VISUAL
        only. Never disconnect: at that point the graph is the audio path, and
        tearing it down is what would actually cause silence.
   Everything is wrapped so that any failure leaves plain playback untouched. */
var sfBeat={ctx:null,src:null,an:null,el:null,data:null,raf:0,ok:false,dead:false,level:0,err:''};
/* exposed for diagnosis: the catch below is deliberately silent so a Web Audio
   failure can never disturb playback, which also means a failure leaves no
   trace. This is the trace. */
try{window.__sfBeat=sfBeat;}catch(e){}
function sfBeatAttach(){
if(sfBeat.dead)return;
var el=document.querySelector('audio');
if(!el)return;
if(sfBeat.el===el)return;                 /* one source per element, ever */
try{
var AC=window.AudioContext||window.webkitAudioContext;
if(!AC){sfBeat.dead=true;return;}
if(!sfBeat.ctx)sfBeat.ctx=new AC();
var src=sfBeat.ctx.createMediaElementSource(el);
src.connect(sfBeat.ctx.destination);      /* (1) audio path, first and always */
var an=sfBeat.ctx.createAnalyser();
an.fftSize=256;an.smoothingTimeConstant=0.82;
src.connect(an);                          /* (2) analyser tap, goes nowhere else */
sfBeat.src=src;sfBeat.an=an;sfBeat.el=el;
sfBeat.data=new Uint8Array(an.frequencyBinCount);
if(sfBeat.ctx.state==='suspended'&&sfBeat.ctx.resume)sfBeat.ctx.resume();
sfBeatVerify(el);
}catch(e){sfBeat.dead=true;sfBeat.err=(e&&e.name?e.name:'')+': '+(e&&e.message?e.message:String(e));}
}
/* (3) the safety check: is sound still actually moving? */
function sfBeatVerify(el){
var t0=el.currentTime,wasPaused=el.paused;
setTimeout(function(){
if(wasPaused||el.paused){sfBeat.ok=true;return;}   /* cannot judge while paused */
if(el.currentTime>t0+0.05){sfBeat.ok=true;return;}
/* one retry: a context that never left 'suspended' is the common, harmless
   cause and resume() fixes it. */
try{if(sfBeat.ctx&&sfBeat.ctx.resume)sfBeat.ctx.resume();}catch(e){}
var t1=el.currentTime;
setTimeout(function(){
if(el.paused||el.currentTime>t1+0.05){sfBeat.ok=true;return;}
sfBeat.ok=false;sfBeat.dead=true;        /* visual off; graph stays connected */
var d=sfFlyr.el;if(d)d.style.setProperty('--sf-beat','0');
},900);
},1100);
}
function sfBeatLoop(){
var d=sfFlyr.el;
if(!d||!d.classList.contains('sf-open')){sfBeat.raf=0;return;}
if(sfBeat.ok&&sfBeat.an&&sfBeat.data){
try{
sfBeat.an.getByteFrequencyData(sfBeat.data);
var i,sum=0,n=10;                        /* low bins ~ the beat, not the vocal */
for(i=0;i<n;i++)sum+=sfBeat.data[i];
var lvl=sum/(n*255);
sfBeat.level=sfBeat.level*0.80+lvl*0.20; /* smooth, or it strobes */
d.style.setProperty('--sf-beat',sfBeat.level.toFixed(3));
}catch(e){}
}
sfBeat.raf=requestAnimationFrame(sfBeatLoop);
}
function sfFlyrOpen(){
var d=sfFlyrEl();
d.classList.add('sf-open');
document.body.classList.add('sf-flyr-open');
sfFlyr.id=null;sfFlyr.lastIdx=-1;          /* force a reload+repaint */
/* opening is a real user gesture, which is exactly when an AudioContext is
   allowed to start -- so attach here rather than at load. */
sfBeatAttach();
if(!sfBeat.raf)sfBeat.raf=requestAnimationFrame(sfBeatLoop);
sfFlyrTick();
}
/* sf-flyr-minimise: this button MINIMISES, it does not dismiss. Fullscreen is
   entered from the side lyrics panel, so leaving it must put you back where you
   came from -- closing outright left you with no lyrics at all, which is not
   what "collapse the fullscreen view" should do. The icon says so too
   (fullscreen_exit, not a close X). */
function sfFlyrClose(){
if(sfFlyr.el)sfFlyr.el.classList.remove('sf-open');
document.body.classList.remove('sf-flyr-open');
/* stop the render loop, but NEVER touch the audio graph -- see sf-flyr-beat */
if(sfBeat.raf){cancelAnimationFrame(sfBeat.raf);sfBeat.raf=0;}
/* restore the side panel we came from */
var p=sfLyricsPanel();
p.classList.add('sf-open');
document.body.classList.add('sf-lyrics-open');
var b=document.querySelector('.sf-lyr-btn');
if(b)b.classList.add('sf-on');
/* the track can change while fullscreen is up -- make sure the panel shows the
   one that is playing now, not the one we expanded from. */
var id=sfCurrentTrackId();
if(id&&id!==sfLyrState.id)sfLoadLyrics(id);
}
/* Escape is the one shortcut people try first in a fullscreen view. */
document.addEventListener('keydown',function(e){
if((e.key==='Escape'||e.keyCode===27)&&document.body.classList.contains('sf-flyr-open'))sfFlyrClose();
});
function sfFlyrLoad(id){
var d=sfFlyrEl(),box=d.querySelector('.sf-flyr-lines');
sfFlyr.id=id;sfFlyr.lines=[];sfFlyr.synced=false;sfFlyr.lastIdx=-1;
box.innerHTML='';
var ac=window.ApiClient;
if(!ac)return;
ac.getJSON(ac.getUrl('Audio/'+id+'/Lyrics')).then(function(j){
if(sfFlyr.id!==id)return;
var lines=(j&&j.Lyrics)||[];
if(!lines.length){box.innerHTML='<div class="sf-flyr-empty">No lyrics for this track.</div>';return;}
sfFlyr.lines=lines;
sfFlyr.synced=lines[0].Start!=null;
var i,p;
for(i=0;i<lines.length;i++){
p=document.createElement('p');
var t=lines[i].Text||'';
if(!t.trim())p.className='sf-flyr-blank';else p.textContent=t;
box.appendChild(p);
}
}).catch(function(){
if(sfFlyr.id!==id)return;
box.innerHTML='<div class="sf-flyr-empty">No lyrics for this track.</div>';
});
}
/* sf-flyr-art-hd: the now-playing bar asks for height=140 because its own
   element is 34x34. Reusing that URL put a 140px image behind artwork rendered
   at ~450px -- a 3x upscale, which is the pixelation. Same item, same tag, just
   asked for at a size that suits where it is being shown. */
function sfBigArt(u){
if(!u||u==='none')return u;
try{
var url=new URL(u,location.origin);
url.searchParams.delete('width');
url.searchParams.delete('maxWidth');
url.searchParams.delete('fillWidth');
url.searchParams.delete('fillHeight');
url.searchParams.set('height','900');
url.searchParams.set('quality','95');
return url.pathname+'?'+url.searchParams.toString();
}catch(e){return u;}
}
function sfFlyrTick(){
var d=sfFlyr.el;
if(!d||!d.classList.contains('sf-open'))return;
var id=sfCurrentTrackId();
if(id&&id!==sfFlyr.id){sfFlyrLoad(id);}
/* artwork + text mirror the now-playing bar, which already holds the resolved
   image URL -- no second lookup, and it stays correct across track changes. */
var img=d.querySelector('.sf-flyr-art img');
/* the artwork element is .nowPlayingImage (a DIV with a background-image), NOT
   .nowPlayingBarImage -- verified live; the latter does not exist. Both are
   tried so a Jellyfin rename cannot silently blank the art. */
var src=document.querySelector('.nowPlayingImage')||document.querySelector('.nowPlayingBarImage');
if(src){
var bg=(getComputedStyle(src).backgroundImage||'').replace(/^url\(["']?/,'').replace(/["']?\)$/,'');
var big=sfBigArt(bg);
if(big&&bg!=='none'&&img.getAttribute('src')!==big){
img.setAttribute('src',big);
/* drive the ambient layers off the same URL, so they change with the track */
var lay=d.querySelectorAll('.sf-flyr-bg i'),z;
for(z=0;z<lay.length;z++)lay[z].style.backgroundImage='url("'+big+'")';
}
}
var txt=document.querySelector('.nowPlayingBarText');
if(txt){
var h=d.querySelector('.sf-flyr-meta h2'),pp=d.querySelector('.sf-flyr-meta p');
var t0=txt.children[0]?txt.children[0].textContent:'';
var t1=txt.children[1]?txt.children[1].textContent:'';
if(h.textContent!==t0)h.textContent=t0;
if(pp.textContent!==t1)pp.textContent=t1;
}
var a=document.querySelector('audio');
if(!a)return;
/* Track finished: the element is torn down (readyState 0) but keeps its last
   currentTime semantics, so the highlight stayed pinned to the final line and
   the list stayed scrolled to the bottom -- it looked like the lyrics were
   still running. Reset to the top and clear the highlight so the view plainly
   reads as "finished", and leave it there; the transport can restart it. */
if(sfPlayerDead()){
if(sfFlyr.lastIdx!==-1){
var rz=d.querySelectorAll('.sf-flyr-lines p'),z;
for(z=0;z<rz.length;z++)rz[z].className=rz[z].className.replace(/\s*sf-(on|d1|d2|d3)\b/g,'');
sfFlyr.lastIdx=-1;
try{d.querySelector('.sf-flyr-lines').scrollTo({top:0,behavior:'smooth'});}catch(e){}
var pf=d.querySelector('.sf-flyr-prog span');if(pf)pf.style.width='0%';
var pb0=d.querySelector('.sf-flyr-ctl [data-a="play"] .material-icons');if(pb0)pb0.textContent='play_arrow';
}
return;
}
var pi=d.querySelector('.sf-flyr-prog span');
if(pi&&a.duration)pi.style.width=(Math.max(0,Math.min(1,a.currentTime/a.duration))*100)+'%';
var pb=d.querySelector('.sf-flyr-ctl [data-a="play"] .material-icons');
if(pb)pb.textContent=a.paused?'play_arrow':'pause';
if(!sfFlyr.synced||!sfFlyr.lines.length)return;
var ticks=a.currentTime*10000000,idx=-1,i;
for(i=0;i<sfFlyr.lines.length;i++){
if(sfFlyr.lines[i].Start<=ticks)idx=i;else break;
}
/* sf-flyr-nogap: the pulsing three-dot instrumental indicator is GONE. It was
   modelled on Apple's, but in practice it fired constantly during ordinary
   playback -- any line more than 4.5s from the next one lit it -- so it read as
   a loading spinner sitting on top of a working lyrics view. The lyrics
   themselves already show that playback is progressing. */
var nextAt=(idx+1<sfFlyr.lines.length)?sfFlyr.lines[idx+1].Start/10000000:null;
var nowS=a.currentTime;
if(idx<0||idx===sfFlyr.lastIdx)return;
var rows=d.querySelectorAll('.sf-flyr-lines p');
if(!rows.length||!rows[idx])return;
/* sf-flyr-depth: distance-based blur/dim, so the current line sits in focus and
   the rest fall away. Only runs when the line CHANGES, not every tick. */
var q,dist;
for(q=0;q<rows.length;q++){
dist=Math.abs(q-idx);
rows[q].className=rows[q].className.replace(/\s*sf-(on|d1|d2|d3)\b/g,'');
if(dist===0)rows[q].className+=' sf-on';
else if(dist===1)rows[q].className+=' sf-d1';
else if(dist===2)rows[q].className+=' sf-d2';
else rows[q].className+=' sf-d3';
}
/* sf-flyr-sweep: the karaoke wipe. Our lyrics are LINE-level (Jellyfin exposes a
   per-line Cues array for word timing, but lrclib fills none -- measured empty
   on every track), so the highlight is INTERPOLATED across the line over the
   time until the next one. Driven by a CSS animation rather than the 400ms tick
   so it runs at display refresh rate instead of stepping 2.5 times a second.
   A negative delay starts it at the right position when you join mid-line or
   seek. Capped at 9s so a long instrumental tail cannot crawl. */
var st=sfFlyr.lines[idx].Start/10000000;
var dur=Math.max(0.9,Math.min((nextAt!=null?nextAt:st+3.5)-st,9));
rows[idx].style.setProperty('--sf-dur',dur+'s');
rows[idx].style.setProperty('--sf-delay',(-(Math.max(0,nowS-st)))+'s');
sfFlyr.lastIdx=idx;
/* scrollTo with behavior:smooth rather than assigning scrollTop -- this is the
   one place the motion is the point, and it keeps the active line centred. */
var box=d.querySelector('.sf-flyr-lines');
/* 42%, not 50%: sitting the current line slightly ABOVE centre leaves more of
   the song ahead of it on screen, which is what you actually read. Dead centre
   splits the space evenly between lyrics already sung and lyrics still coming --
   half the view spent on the past. */
var aim=rows[idx].offsetTop-box.clientHeight*0.42+rows[idx].offsetHeight/2;
try{box.scrollTo({top:aim,behavior:'smooth'});}
catch(e){box.scrollTop=aim;}
}
/* sf-hero-cw-source: put Continue Watching INTO the hero rotation.
   Media Bar asks the server for
     /Items?IncludeItemTypes=Movie,Series&...&sortBy=Random&isPlayed=False&...
   i.e. random UNPLAYED movies and series -- so an item you are part-way through
   could only ever appear by luck, which is why the resume state never showed.
   Rather than fight its rotation we widen its INPUT: wrap fetch, spot that one
   request, and merge the user's resume items into the response before Media Bar
   parses it. It then builds, rotates and transitions those slides with its own
   code -- no DOM injection, nothing to keep in sync.

   Episodes are represented by their SERIES, not the episode: an episode has no
   logo and usually no backdrop of its own, so an episode slide renders bare.
   The series looks right, and sfCwMap remembers which episode it stands for so
   the hero can say "Continue S2 E4". */
var sfCwMap={};                 /* itemId(norm) -> {s,e,pct,epId,name} */
/* itemId(norm) -> RunTimeTicks, for FILMS. Media Bar's hero query already
   returns RunTimeTicks (it is the source of its own "Ends at 9:52 PM"), so
   skimming it off the response as it goes past means a film's length is in hand
   the instant its slide activates. Before this the chip was corrected only once
   ApiClient.getItem replied, which is why "Ends at" was visible for a moment on
   every film the first time it came round. */
'''

# _LS_06 (orig L3629-4368) -- sf-hero-nextup, sf-hero-parallel, sf-cw-order
_LS_06 = r'''/* sf-hero-nextup: seriesId(norm) -> the next unwatched episode of a show already
   under way. Same shape as an sfCwMap entry minus pct, so the paint can treat
   "resumed episode" and "next episode" as one thing. */
var sfNuMap={};
/* The raw endpoint is not what its name suggests, so this filters hard:
   - an episode WITH progress is a resume card, not a next-up one. Jellyfin
     returns the in-progress episode here too -- Euphoria S1E1 at 54% was in both
     lists -- so anything above 0% is dropped and left to the CW tier.
   - a series the CW tier already carries is dropped, or the same show turns up
     twice in one rotation. Measured 6 of 24 overlapping.
   - series never actually watched are dropped. PlayCount and Played are useless
     for this (0 and false on EVERY series record, verified across 14), so the
     real signal is RecursiveItemCount - UnplayedItemCount: Scrubs 14 watched and
     Reply 1988 14, against 0 for Yellowstone, South Park and Chuck -- which the
     endpoint offers only because their first episode is unwatched.
   - episodes with no season/episode number are dropped: Dragon Ball Z Kai
     returns ParentIndexNumber undefined and rendered as "SundefinedE99".
   Capped at 5, so the hero still recommends rather than becoming a chore list.
   Returns SERIES ids to inject: an episode has no logo and usually no backdrop,
   so an episode slide renders bare (same reason as sf-hero-cw-source). */
function sfNuCollect(ac,uid,pre){
try{
/* sf-hero-parallel (2026-08-24): `pre` is a Shows/NextUp request that was
   already started alongside Items/Resume. Measured before this change, the
   hero's data chain was FOUR round trips strictly in series --
   Items/Resume -> Shows/NextUp -> Items?Ids (inside here) -> Items?Ids (merge)
   -- and the trace showed Shows/NextUp not even being REQUESTED until
   Items/Resume had finished. Media Bar cannot paint a single slide until the
   whole chain resolves, which is why the hero sat empty for 7-13s.
   The serial order existed for a real reason: the filter below drops any
   series the Continue Watching tier already carries, and sfCwMap only exists
   once Resume has resolved. So the REQUEST is overlapped while the DEDUPE
   still happens afterwards -- the caller only invokes this from inside the
   Resume .then, so sfCwMap is populated by the time we filter. */
return (pre||ac.getJSON(ac.getUrl('Shows/NextUp',
{userId:uid,Limit:24,Fields:'Overview,SeriesId,UserData'})))
.then(function(nu){
var eps=(nu&&nu.Items)||[],ni,ep,key,keep=[];
for(ni=0;ni<eps.length;ni++){
ep=eps[ni];
if(!ep||!ep.SeriesId)continue;
if(ep.ParentIndexNumber==null||ep.IndexNumber==null)continue;
if(((ep.UserData&&ep.UserData.PlayedPercentage)||0)>0)continue;  /* a resume */
key=sfNorm(ep.SeriesId);
if(sfCwMap[key])continue;                                        /* CW has it */
keep.push(ep);
}
if(!keep.length)return [];
var ids=[],seen={};
for(ni=0;ni<keep.length;ni++)if(!seen[keep[ni].SeriesId]){
seen[keep[ni].SeriesId]=1;ids.push(keep[ni].SeriesId);}
return ac.getJSON(ac.getUrl('Users/'+uid+'/Items',
{Ids:ids.join(','),Fields:'UserData,RecursiveItemCount'}))
.then(function(sr){
var recs={},sl=(sr&&sr.Items)||[],k,rec,tot,unp,out=[];
for(k=0;k<sl.length;k++)recs[sl[k].Id]=sl[k];
for(k=0;k<keep.length&&out.length<5;k++){
ep=keep[k];
rec=recs[ep.SeriesId];
if(!rec)continue;
tot=rec.RecursiveItemCount||0;
unp=(rec.UserData&&rec.UserData.UnplayedItemCount);
if(unp==null||tot-unp<=0)continue;            /* never actually watched */
sfNuMap[sfNorm(ep.SeriesId)]={s:ep.ParentIndexNumber,e:ep.IndexNumber,
epId:ep.Id||'',name:ep.Name,rt:ep.RunTimeTicks||0,ov:ep.Overview||'',id:ep.Id};
out.push(ep.SeriesId);
}
return out;
});
}).catch(function(){return [];});
}catch(nerr){return Promise.resolve([]);}
}
var sfRtMap={};
function sfRtCache(items){
if(!items)return;
for(var ri=0;ri<items.length;ri++){
var rit=items[ri];
if(rit&&rit.Id&&rit.Type==='Movie'&&rit.RunTimeTicks)sfRtMap[sfNorm(rit.Id)]=rit.RunTimeTicks;
}
}
/* sf-cw-order: Media Bar does `itemIds = SlideUtils.shuffleArray(itemIds)` right
   after fetching, which threw away whatever order we merged in -- measured as CW
   filling 2 of 3 slides on one load and 0 of 4 on the next, i.e. the "progress
   bar is missing" report (the bar was fine; CW slides simply were not coming up).
   SlideUtils is a top-level `const` in a classic script: NOT on window, but its
   binding lives in the global lexical environment, so it resolves by bare name
   from this script. Verified live: typeof SlideUtils === "object".
   The shuffle is kept -- randomness within each group is good -- but Continue
   Watching is lifted back to the front afterwards, so the hero plays through
   what you are already watching and only then moves on to recommendations.
   Patched from inside the fetch interceptor, which is the one moment we KNOW
   Media Bar is loaded and has not shuffled yet. */
function sfCwOrder(){
try{
if(typeof SlideUtils==='undefined'||!SlideUtils||SlideUtils.__sfPatched)return;
var orig=SlideUtils.shuffleArray;
if(typeof orig!=='function')return;
SlideUtils.__sfPatched=1;
SlideUtils.shuffleArray=function(arr){
var out=orig.apply(SlideUtils,arguments);
try{
var cw=[],nu=[],rest=[],i;
for(i=0;i<out.length;i++){
if(sfCwMap[sfNorm(out[i])])cw.push(out[i]);
else if(sfNuMap[sfNorm(out[i])])nu.push(out[i]);
else rest.push(out[i]);
}
/* Continue Watching, then Next Up, then recommendations */
return cw.concat(nu,rest);
}catch(e){return out;}
};
}catch(e){}
}
/* sf-hero-cap (2026-08-24): Shows/NextUp is the slow half of the hero's data.
   Profiled repeatedly it takes 985-5720ms, and the merge cannot run until it
   answers -- so a slow Next Up holds the ENTIRE hero blank, including the
   Continue Watching slides that are already in hand. Next Up is a bonus tier;
   Continue Watching is the point. So its contribution is capped: if it has not
   answered in time the hero builds without it and simply shows no Next Up
   slides on that load. Resolves (never rejects) so a failure degrades a tier
   rather than losing the hero.
   NB an earlier attempt PREFETCHED Next Up at page load instead. That made it
   WORSE -- fired at ~800ms it lands amid the ~200 initial page requests and
   measured 4.6-26.4s instead of 1-5.7s, pushing the slides out to 12-17s and
   once never rendering. Do not reintroduce that. */
function sfHeroCap(p,ms,fb){
return new Promise(function(res){
var done=false;
var t=setTimeout(function(){if(!done){done=true;res(fb);}},ms);
try{
p.then(function(v){if(!done){done=true;clearTimeout(t);res(v);}},
function(){if(!done){done=true;clearTimeout(t);res(fb);}});
}catch(e){if(!done){done=true;clearTimeout(t);res(fb);}}
});
}
(function(){
var F=window.fetch;
if(!F||window.__sfCwWrapped)return;
window.__sfCwWrapped=1;
window.fetch=function(input,init){
var url='';
try{url=(typeof input==='string')?input:(input&&input.url)||'';}catch(e){}
var isHero=url.indexOf('/Items?')>-1&&url.indexOf('IncludeItemTypes=Movie,Series')>-1&&url.indexOf('sortBy=Random')>-1;
var p=F.apply(this,arguments);
if(!isHero)return p;
sfCwOrder();                 /* patch the shuffle BEFORE Media Bar uses it */
/* sf-hero-parallel-resume (2026-08-31): Items/Resume was fired only AFTER the
   hero list resolved -- traced starting 1ms after it ended on every run of 3,
   costing 766-1382ms of dead time while Media Bar cannot paint a single slide.
   Resume reads only `uid`, never the list body, so the serial order bought
   nothing. This starts it alongside the list, which is exactly the fix
   sf-hero-parallel already proved one level down (it overlapped Shows/NextUp
   with Resume via `pre`, keeping the dedupe afterwards).
   This is NOT the page-load prefetch that was tried and reverted: that fired at
   ~800ms into the initial ~200-request storm and measured 4.6-26.4s. This fires
   at the exact moment Media Bar asks, so it can never land earlier than the
   list request itself, and it inherits the same queue position.
   Falls back to the original in-chain request if ApiClient is not ready yet. */
var resumeP=null;
try{
var ac0=window.ApiClient,uid0=ac0&&ac0.getCurrentUserId&&ac0.getCurrentUserId();
if(ac0&&ac0.getJSON&&uid0){
resumeP=ac0.getJSON(ac0.getUrl('Users/'+uid0+'/Items/Resume',
{Limit:8,MediaTypes:'Video',Fields:'Overview,ImageTags,BackdropImageTags,UserData,SeriesId'}));
/* consumed below; this branch only silences a premature unhandled-rejection
   warning if it fails before the list resolves. The rejection still reaches the
   real consumer, which the existing outer .catch turns into "hero without CW". */
resumeP.catch(function(){});
}
}catch(e){resumeP=null;}
return p.then(function(res){
if(!res||!res.ok)return res;
return res.clone().json().then(function(data){
var ac=window.ApiClient;
if(!ac||!data||!data.Items)return res;
sfRtCache(data.Items);          /* runtimes, before anything else can need them */
var uid=ac.getCurrentUserId();
/* sf-hero-nonextup (2026-08-24): the Next Up tier is REMOVED from the hero at
   the admin's request -- the hero now carries Continue Watching plus Media Bar's own
   recommendations only. This deletes TWO requests from the hero's critical path:
   Shows/NextUp (measured 985-5720ms, the slow half) and the Items?Ids lookup that
   sfNuCollect made for the series it returned. sfNuCollect() and sfNuMap are left
   defined but uncalled, so restoring the tier is a one-line change.
   Superseded sf-hero-parallel (which overlapped Next Up with Resume) and
   sf-hero-cap (which time-boxed it) -- with no request at all, neither applies. */
return (resumeP||ac.getJSON(ac.getUrl('Users/'+uid+'/Items/Resume',
{Limit:8,MediaTypes:'Video',Fields:'Overview,ImageTags,BackdropImageTags,UserData,SeriesId'})))
.then(function(rz){
var list=(rz&&rz.Items)||[];
if(!list.length)return res;
/* an episode contributes its SERIES; remember the episode behind it */
var wanted=[],seen={},i,it;
for(i=0;i<list.length;i++){
it=list[i];
var ud=it.UserData||{};
if(it.Type==='Episode'&&it.SeriesId){
sfCwMap[sfNorm(it.SeriesId)]={s:it.ParentIndexNumber,e:it.IndexNumber,
pct:ud.PlayedPercentage||0,epId:it.Id,name:it.Name,rt:it.RunTimeTicks||0,
pt:ud.PlaybackPositionTicks||0,
ov:it.Overview||''};
if(!seen[it.SeriesId]){seen[it.SeriesId]=1;wanted.push(it.SeriesId);}
}else if(it.Type==='Movie'){
sfCwMap[sfNorm(it.Id)]={pct:ud.PlayedPercentage||0,epId:it.Id,pt:ud.PlaybackPositionTicks||0};
if(!seen[it.Id]){seen[it.Id]=1;wanted.push(it.Id);}
}
}
/* Next Up rides along here rather than in its own pass: both tiers need the
   same kind of series record, so they resolve into ONE Ids request. Note this is
   outside the `wanted.length` guard on purpose -- there can be Next Up with no
   Continue Watching at all. */
return Promise.resolve([]).then(function(nuIds){
var allIds=wanted.concat(nuIds);
if(!allIds.length)return res;
/* fetch the full records so the injected entries carry everything Media Bar
   reads (ImageTags for the logo/backdrop, Overview for the plot). */
return ac.getJSON(ac.getUrl('Users/'+uid+'/Items',
{Ids:allIds.join(','),Fields:'Overview,ImageTags,BackdropImageTags,UserData',
EnableImageTypes:'Logo,Backdrop,Primary'}))
.then(function(full){
var add=(full&&full.Items)||[];
if(!add.length)return res;
sfRtCache(add);                 /* the CW films we inject are not in data.Items */
var have={},j;
for(j=0;j<data.Items.length;j++)have[data.Items[j].Id]=1;
var merged=[];
for(j=0;j<add.length;j++)if(!have[add[j].Id])merged.push(add[j]);
/* CW, then Next Up, then Media Bar's own random picks. The Ids response comes
   back in its own order, so ours is restored explicitly.
   Ordering here is only half the job -- Media Bar shuffles the id list
   afterwards (see sfCwOrder), which is what threw the earlier attempts away. */
var rank={},r;
for(r=0;r<wanted.length;r++)rank[wanted[r]]=r;
for(r=0;r<nuIds.length;r++)rank[nuIds[r]]=1000+r;
merged.sort(function(a,b){
var ra=(rank[a.Id]==null)?9999:rank[a.Id],rb=(rank[b.Id]==null)?9999:rank[b.Id];
return ra-rb;});
data.Items=merged.concat(data.Items);
if(typeof data.TotalRecordCount==='number')data.TotalRecordCount=data.Items.length;
return new Response(JSON.stringify(data),
{status:res.status,statusText:res.statusText,headers:res.headers});
});
});
});
}).catch(function(){return res;});
}).catch(function(){return p;});
};
})();
/* sf-hero-resume: Continue Watching as a hero STATE, not a takeover.
   Media Bar owns which item is featured (its config exposes only MaxMovies /
   MaxTvShows / MaxItems -- there is no content-source option), and each slide
   carries data-item-id. So rather than fight its rotation, we read the featured
   item's own UserData: if it is part-watched, the hero gains a progress bar and
   Play becomes Resume. Anything not resumable keeps the existing Play/Info
   behaviour untouched.
   Cached per slide+item so this asks the server once per featured item, not
   every tick. */
/* sf-cw-barpos: the bar's top MUST be recomputed continuously, not once when the
   item changes. Media Bar lays the hero out asynchronously, so a single write at
   item-change time captured a pre-layout offset and stuck -- measured top 386px
   against a genre that had settled at 227. Writes only when the value actually
   moves, so it costs nothing on a steady slide. */
/* sf-hero-logo: some items have a PORTRAIT image in the Logo slot -- How I Met
   Your Mother's was 745x1051, a poster, which scaled to the hero band rendered
   59x83 (about 10% of the width). No scaling fixes that, so anything squarer
   than 1.2:1 is treated as bad logo data and the item's NAME is shown instead.
   1.2 and not 1.6: measured across 70 items, wordmarks like Cars (1.55) and
   Grease 2 (1.52) are legitimately chunky and were being thrown away.
   The name is already on the image as its alt text, so this costs no request. */
function sfHeroLogo(){
var imgs=document.querySelectorAll('.slide .logo, .slide .logo-container img'),i,img,box,name,el;
for(i=0;i<imgs.length;i++){
img=imgs[i];
if(img.getAttribute('data-sf-logo')==='1')continue;
if(!img.naturalWidth||!img.naturalHeight)continue;   /* not decoded yet */
img.setAttribute('data-sf-logo','1');
if(img.naturalWidth/img.naturalHeight>=1.2)continue;
box=img.parentElement;
if(!box)continue;
name=(img.getAttribute('alt')||'').trim();
if(!name)continue;
img.style.display='none';
if(!box.querySelector('.sf-hero-title')){
el=document.createElement('div');
el.className='sf-hero-title';
el.textContent=name;
box.appendChild(el);
}
}
}
function sfCwBarPos(){
/* Hero vertical rhythm. Everything is measured live and applied with MARGINS,
   never by writing `top`: Media Bar owns that property on this stack and
   rewrites it, which produced a visible ping-pong when we contested it.
   The genre line is gone (hidden for every slide), so nothing anchors to it any
   more -- the chain is logo -> episode -> chips -> progress -> description. */
var slides=document.querySelectorAll('.slide'),si,slide,lg,info,bar,plot,ep;
for(si=0;si<slides.length;si++){
slide=slides[si];
lg=slide.querySelector('.logo-container');
info=slide.querySelector('.info-container');
plot=slide.querySelector('.plot-container');
bar=slide.querySelector('.sf-cw-prog');
ep=slide.querySelector('.sf-hero-ep');
if(!lg||!info||!lg.offsetHeight)continue;
/* episode line rides under the logo -- the logo is the one element in this
   stack we never move, so anchoring here cannot feed back on itself */
if(ep){
/* Same gate as the progress bar: this carries no default top (the band depends
   on the logo, measured per slide), so before it is placed it would resolve to
   its static position and visibly jump into place as a new hero arrives. */
var epWant=(lg.offsetTop+lg.offsetHeight+12)+'px';
if(ep.style.top!==epWant)ep.style.top=epWant;
if(ep.getAttribute('data-pos')!=='1')ep.setAttribute('data-pos','1');
}
/* keep our runtime text in place -- Media Bar rewrites this row */
var rtq=slide.querySelector('.runTime'),rtWant=slide.getAttribute('data-sf-rt');
if(rtq&&rtWant&&rtq.textContent.trim()!==rtWant)rtq.textContent=rtWant;
/* same treatment for the episode synopsis -- see sf-hero-epplot */
var plq=slide.querySelector('.plot'),plWant=slide.getAttribute('data-sf-plot');
if(plq&&plWant&&plq.textContent!==plWant)plq.textContent=plWant;
/* progress sits under the chips */
if(bar){
/* sf-barpos-rendered (2026-08-28). This used to be
       info.offsetTop + info.offsetHeight + 10
   -- the chips' UNTRANSFORMED position. The chips carry a different transform in
   every hero band (translateY(-13.43vh) at 768-999, translateX(-50%) on phones,
   none under the JS layout), so the bar was placed where the chips WOULD be
   without their transform and rendered as a stray line: above the button at one
   size, through the chips at another, below the button at a third.
   Measure the chips as they are actually drawn and express that in the slide's
   own coordinates, so the bar sits 10px under them in every band with no
   per-band CSS at all. */
var _sr=slide.getBoundingClientRect(), _ir=info.getBoundingClientRect();
/* sf-barpos-adaptive (2026-08-29). A FIXED 10px gap is wrong: the room under the
   chips is not constant. Every part of this slide is position:absolute with its
   own top, so nothing displaces anything -- the bar was being dropped into a gap
   that is not guaranteed to exist. Measured over a width x height matrix, the
   space under the chips varies with the band (the phone band's button sits 15vh
   down, which collapses to 9px at a 700px-tall window), with the viewport height,
   AND with the slide itself (at 800x700 one item left 12px under its chips and
   the next left 27px). Centre the bar in whatever gap is actually there, capped
   at the 10px that looks right when there is room, so it degrades instead of
   drawing a line through the plot or the Play button. */
var _nx=(plot&&plot.getBoundingClientRect().height)?plot:slide.querySelector('.button-container');
var _bh=bar.offsetHeight||5;
var _av=_nx?(_nx.getBoundingClientRect().top-_ir.bottom):999;
var _gap=Math.max(1,Math.min(10,(_av-_bh)/2));
var barWant=Math.round(_ir.bottom-_sr.top+_gap)+'px';
if(bar.style.top!==barWant)bar.style.top=barWant;
if(bar.getAttribute('data-pos')!=='1')bar.setAttribute('data-pos','1');
}
/* Description keeps a constant gap below whatever precedes it. Solved by
   FEEDBACK rather than arithmetic: the margin we add changes plot.offsetTop, so
   computing it from that value directly would fold our own shift back in (the
   mistake that put the episode line on top of the chips). Nudge by the measured
   error instead, with a 2px dead-band so it settles rather than jitters. */
/* A plot that is not rendered cannot need a gap, and the arithmetic below is
   meaningless without one: Media Bar hides .plot-container on mobile, so
   offsetTop and offsetHeight are both 0, naturalTop goes negative, and the
   margin runs straight to its 160px ceiling every pass. That value is applied to
   .button-container as well, which is what pushed the mobile hero's Play button
   160px down and clean off the slide (measured: CSS top 508.9px, rendered at
   670, hero ending at 654 -- the button sat behind the Continue Watching row and
   could not be tapped; elementFromPoint returned a card, not the button).
   Clearing the property is what restores it, so this is an else, not a skip. */
if(plot&&plot.offsetHeight>0){
/* Solved DIRECTLY, in one pass -- not by nudging towards the target.
   The earlier version measured the error and stepped the margin toward it each
   tick, so a new hero slide visibly shuffled for several frames before settling.
   The natural position is recoverable (offsetTop minus the margin we ourselves
   added), so the correct margin can be computed outright and written once.
   All values are offsetTop-based, i.e. the slide's own coordinate space, so
   nothing here depends on where the slide happens to sit on screen.
   The property is used rather than an inline margin because something sets
   margin-top on .plot-container with !important -- an inline 45.99px was
   computing to 16px, which is why nudging never appeared to do anything. */
/* Converge IN THIS FRAME rather than across ticks. A single pass is not always
   right: on the pass that CREATES the progress bar the bar has not been placed
   yet, so the anchor it provides is its static position and the margin lands too
   low -- measured as 0 -> 32 -> 16px, a visible 16px step about 200ms in. Each
   iteration re-reads offsetTop, which forces layout, so the whole correction
   happens before the browser paints and only the final value is ever seen.
   Bounded at 4 passes; it settles in 2, and the dead-band guarantees it stops. */
var pass,curMt,naturalTop,nextMt,anchorBottom;
/* sf-plot-skip (perf): every pass reads offsetTop, forcing a synchronous
   layout, and this ran for each slide on each 400ms tick even when nothing had
   moved. Remember the geometry we settled at and skip while it is unchanged --
   measured 296 --sf-plot-mt writes per 15s idle before this guard. */
anchorBottom=bar?(bar.offsetTop+bar.offsetHeight):(info.offsetTop+info.offsetHeight);
curMt=parseFloat(slide.style.getPropertyValue('--sf-plot-mt')||'16')||16;
if(slide.__sfPlotKey!==anchorBottom+'|'+curMt){
for(pass=0;pass<4;pass++){
anchorBottom=bar?(bar.offsetTop+bar.offsetHeight):(info.offsetTop+info.offsetHeight);
curMt=parseFloat(slide.style.getPropertyValue('--sf-plot-mt')||'16')||16;
naturalTop=plot.offsetTop-curMt;
nextMt=Math.max(0,Math.min(160,(anchorBottom+14)-naturalTop));
if(Math.abs(nextMt-curMt)<=1)break;
slide.style.setProperty('--sf-plot-mt',nextMt+'px');
}
slide.__sfPlotKey=(bar?(bar.offsetTop+bar.offsetHeight):(info.offsetTop+info.offsetHeight))
  +'|'+(parseFloat(slide.style.getPropertyValue('--sf-plot-mt')||'16')||16);
}
}else if(slide.style.getPropertyValue('--sf-plot-mt')){
slide.style.removeProperty('--sf-plot-mt');
}
}
}
/* sfHeroPrefill: resolve every slide, not only the active one.
   sfHeroPaint runs for the active slide alone, so an inactive slide sat on Media
   Bar's "Ends at 9:52 PM" (and on the SERIES logline) until the moment it was
   activated. That was never actually on screen -- the paint lands in the same
   task as the .active class, before the browser paints -- but a DOM that is only
   correct because something else runs first is exactly what turns into a visible
   bug the day that ordering changes. Everything needed is already cached
   (sfCwMap from the resume query, sfRtMap from Media Bar's own response), so
   resolving all of them is a few attribute writes and no requests.
   Only ever SETS a value it can prove: a series with no resume entry and no film
   runtime is left alone, so "9 Seasons" and its layers glyph survive. Removal
   stays with sfHeroPaint, which is the one that knows the full item. */
/* A read-only window on the hero's three tiers. These maps live inside the
   IIFE, so without this there is no way to tell "Next Up produced nothing" from
   "Next Up produced items that never became slides" -- which is exactly the
   question that comes up when a tier does not appear. */
window.__sfHeroTiers=function(){
var k,nu=[];
for(k in sfNuMap)nu.push(k+' S'+sfNuMap[k].s+'E'+sfNuMap[k].e+' '+(sfNuMap[k].name||''));
return {cwCount:Object.keys(sfCwMap).length,
nuCount:Object.keys(sfNuMap).length,filmRuntimes:Object.keys(sfRtMap).length,
nextUp:nu,
slides:[].map.call(document.querySelectorAll('.slide'),function(s){
var id=s.getAttribute('data-item-id')||'',n=sfNorm(id);
return {id:id.slice(0,8),tier:sfCwMap[n]?'CW':(sfNuMap[n]?'NEXT-UP':'discover')};})};
};
/* sf-discover-links: the Discover row comes from Jellyfin Enhanced, and its
   cards link to JellyseerrUrls -- the LAN address http://YOUR_SERVER_IP:5055.
   Measured: ALL 84 anchors in that row. Off the home network that is a dead
   link on every card; on it, the tap throws the user out of Jellyfin into a
   separate app with a separate login.
   There is no public hostname for Jellyseerr (nginx proxies only jellyseerr.nas),
   and exposing it is not something to do silently, so the tap is sent instead to
   Jellyfin's OWN search for that title -- which already carries the Request
   buttons, works from anywhere, and keeps the user in one app.
   Each anchor is flagged once, so after the first pass the selector matches
   nothing and this costs a single failed query per tick. */
/* The sub-tab bar sticks directly beneath the header, whose height is not a
   constant: 78px here, but ~130px on library pages where our main pill bar is
   injected into it. Publishing the measured height as a custom property keeps
   the CSS honest without hard-coding a number that is wrong half the time. */
function sfHdrVar(){
var h=document.querySelector('.skinHeader');
if(!h)return;
var v=Math.round(h.getBoundingClientRect().height);
if(!v)return;
/* sf-hdr-resizeobs: react to the header CHANGING instead of noticing on the
   400ms tick. Navigation resizes the header (our pill bar is added on library
   routes and removed on home: 87 -> 77), and on the tick alone --sf-hdr-h was
   still the old value for up to 400ms after the header had already changed.
   A ResizeObserver fires before paint, so the variable is current in the same
   frame the header changes. Hooked from here rather than at startup because
   .skinHeader does not exist yet when this file runs. */
if(!window.__sfHdrObs&&window.ResizeObserver){
try{window.__sfHdrObs=new ResizeObserver(function(){try{sfHdrVar();}catch(e){}});
window.__sfHdrObs.observe(h);}catch(e){}
}
/* While a hold is active, let it GROW. The hold is pinned on the click, when
   the header still has the OUTGOING route's height -- 77 leaving home. The
   incoming route is taller (87 on Live TV), so the strip being torn down a
   second time dropped back to the pinned 77 and the header oscillated
   77 -> 87 -> 77 -> 87. Raising the pin as soon as the taller header appears
   turns that into a single 77 -> 87 step. Only ever upward, and the timeout
   releases it regardless. */
/* sf-hdr-growsettle (2026-09-05). This is the 49px library shift, and it was
   never the filter bar. Traced entering Movies:
       t 211  header 136px   page padding 160   (both bars briefly coexist)
       t 519  header  87px   page padding 160   <- header settles, padding does not
       t1006  header  87px   page padding 111   <- padding follows, 49px late
   .page carries `padding-top: calc(var(--sf-hdr-h) + 24px)`, so every header
   height change moves all page content. The pin below adopted the TRANSIENT 136
   peak, held it for the full 400ms window, and the release then dropped 49px --
   after the page was already on screen.
   Growth still publishes immediately (content needs the room); it is only the
   PIN that now requires the taller header to persist, using the same hysteresis
   the shrink path already uses. A peak that lasts two frames is a rebuild
   artefact, not a height, and pinning it guarantees a jump when it is released. */
if(_sfHdrHoldT&&v>(parseFloat(h.style.minHeight)||0)){
if(window.__sfHdrGrowV!==v){window.__sfHdrGrowV=v;window.__sfHdrGrowAt=Date.now();}
else if(Date.now()-window.__sfHdrGrowAt>=140){
try{h.style.setProperty('min-height',v+'px','important');}catch(e){}}
}else if(window.__sfHdrGrowV){window.__sfHdrGrowV=0;}
/* sf-hdr-xfade-settle (2026-09-05). ONE source of truth for when geometry may
   change: the transition lifecycle.
   .page carries `padding-top: calc(var(--sf-hdr-h) + 24px)`, so publishing this
   variable moves every page's content. During a route change the header is
   rebuilt and passes through heights that are not real -- entering Movies it hits
   136px while both bars briefly coexist -- and publishing those put the page's
   padding at 160 and then dropped it to 111 once things settled, 49px AFTER the
   page was on screen. That was the library shift.
   While a snapshot is held, the user is not looking at this page, so there is
   nothing to keep in the right place and nothing to gain by publishing a height
   that is still moving. Let the header settle behind the snapshot and publish
   once, at release -- xfDrop calls back into here -- so the incoming page is
   revealed with its final padding and never corrects itself afterwards.
   This replaces a timing guess with the lifecycle we already have; the 400ms
   sf-hdr-hold pin and the shrink hysteresis stay for navigations that arm no
   hold (a cached instant swap), where they are still the right tool. */
if(XF_HELD)return;
if(window.__sfHdrH===v){window.__sfHdrShrinkV=0;return;}
var prev=window.__sfHdrH;
/* sf-hdr-hysteresis (2026-08-29). Entering Live TV the header COLLAPSES for a
   few frames before settling taller -- measured 77 -> 49 or 63 -> 87 while the
   pill strip is momentarily incomplete (btns=[3,3] instead of [4,3]). Every
   consumer of --sf-hdr-h follows, so the Live TV sub-bar was yanked 24-38px and
   snapped back: the "nav bar flashes and is a little buggy" report.
   The ResizeObserver added earlier today is what exposed this -- on the old
   400ms tick a 60ms dip was usually missed entirely. Publish GROWTH at once
   (content needs the room now), but require a SHRINK to hold for ~180ms before
   believing it. The tick calls this again, so a real shrink is never lost, and
   sf-hdr-compensate still moves padding and the row container together when it
   does land -- a delayed publish costs a slightly late adjustment, never a jump. */
if(prev&&v<prev){
if(window.__sfHdrShrinkV!==v){window.__sfHdrShrinkV=v;window.__sfHdrShrinkAt=Date.now();return;}
if(Date.now()-window.__sfHdrShrinkAt<180)return;
}
window.__sfHdrShrinkV=0;
window.__sfHdrH=v;
if(!_sfHdrHoldT)_sfHdrLast=v;
document.documentElement.style.setProperty('--sf-hdr-h',v+'px');
/* sf-hdr-compensate (2026-08-29). The first home row jumped 10px whenever you
   came back from Live TV. TWO things position those rows against the same
   header height: `padding-top: calc(var(--sf-hdr-h) + 24px)` on .page, which
   moves the instant this variable changes, and the inline `top` the hero fitter
   writes on .sections.homeSectionsContainer, which is recomputed a frame or two
   later. Measured Live TV -> Home, 3/3 runs:
       t=167  --sf-hdr-h 87  padding 111  container top 479  row 590
       t=226  --sf-hdr-h 77  padding 101  container top 479  row 580  <- the jump
       t=242  --sf-hdr-h 77  padding 101  container top 489  row 590
   The fold does not move when the header does, so the compensation is exact
   arithmetic, not a re-measurement: padding changes by d, so `top` must change
   by -d for the row to stay put. Applying it in the same task as the variable
   means both land in one paint. The fitter's own passes still run afterwards
   and compute this same value, so this only removes the gap, it does not
   contest ownership of the property. */
if(prev&&prev!==v){
var d=v-prev,scs=document.querySelectorAll('.sections.homeSectionsContainer'),i,n;
for(i=0;i<scs.length;i++){
if(!scs[i].style.top)continue;
n=parseFloat(scs[i].style.top);
if(n===n)scs[i].style.setProperty('top',(n-d)+'px','important');
}
}
}
/* sf-hdr-var-sync: publish the header height on RESIZE as well as on the tick.
   --sf-hdr-h drives `padding-top: calc(var(--sf-hdr-h) + 24px)` on .page, so it
   is what actually pushes every page's content down when the header grows. On
   the 400ms tick alone that arrived late: shrinking 1200 -> 1180 (where the pill
   bar wraps and the header goes 77 -> 125) measured
       t=44ms   header already 125, page content still at 101
       t=259ms  padding finally 149, content jumps down 48px
   Everything that measures in between -- the hero row fitter above most of all
   -- reads a layout that is about to move, and the first home row ended up 48px
   past the fold. resize fires after layout, so calling it here updates the
   variable in the same frame and the shift is gone rather than merely corrected
   afterwards. sfHdrVar early-returns when the height is unchanged, so this is a
   couple of reads per resize event. */
window.__sfHdrVar=sfHdrVar;
try{window.addEventListener('resize',sfHdrVar);}catch(e){}
/* sf-hdr-hold: hold the header's height across a route change.
   Our pill bar lives inside Jellyfin's header strip, and Jellyfin re-renders
   that strip on navigation -- so for a frame or two there is no .jf-mu-mainbar
   in the document and the header collapses to its bare height. It does not
   happen once, it happens twice. Measured switching Home -> Live TV:
       t=134  bars=0  hdrH=49
       t=204  bars=1  hdrH=87
       t=258  bars=0  hdrH=49
       t=278  bars=1  hdrH=87
   Two 38px collapses in 150ms, and because --sf-hdr-h drives .page padding-top
   the whole page lurches up and back with each one. The admin: 'the live tv nav tab
   flickers and the page doesnt load in cleanly at all.'
   Pinning min-height for a short window means the bar can come and go without
   the layout below ever moving. 400ms comfortably covers both rebuilds; a route
   whose header really is shorter simply settles one tick later instead of
   flickering twice on the way. Inline, so it cannot outlive the timeout. */
var _sfHdrHoldT=null,_sfHdrLast=0;
function sfHdrHold(){
var h=document.querySelector('.skinHeader');
if(!h)return;
var v=Math.round(h.getBoundingClientRect().height);
if(!v)return;
/* Pin the last BELIEVED height, not the instantaneous one. By the time
   hashchange fires the strip is often already torn down, so reading the header
   here returned the bare 49px and pinning that achieved nothing -- measured the
   first dip still going to 49 with the naive version. _sfHdrLast is only ever
   written after sf-hdr-hysteresis has accepted a value, so it is a settled
   height by construction. */
var hold=Math.max(v,_sfHdrLast);
h.style.setProperty('min-height',hold+'px','important');
if(_sfHdrHoldT)clearTimeout(_sfHdrHoldT);
_sfHdrHoldT=setTimeout(function(){
_sfHdrHoldT=null;
var e2=document.querySelector('.skinHeader');
if(e2)e2.style.removeProperty('min-height');
try{sfHdrVar();}catch(e){}
},400);
}
try{window.addEventListener('hashchange',sfHdrHold,true);}catch(e){}
/* ...and pin it on the CLICK too, because hashchange is already too late.
   The pill handler assigns location.hash synchronously, Jellyfin tears the
   header strip down in the same task, and hashchange only fires afterwards --
   so by then the header measures its bare 49px and there is nothing good left
   to hold. Measured: with the hashchange hook alone the SECOND dip was caught
   (49 -> 77) but the first still collapsed to 49. Catching the click pins the
   height while the header is still intact. Any nav control counts; the timeout
   releases it either way, so a click that navigates nowhere costs one pinned
   min-height for 400ms and nothing else. */
try{document.addEventListener('click',function(e){
try{var t=e.target,n=(t&&t.closest)?t.closest('[data-sf-nav],.mainDrawer a,.navDrawer a,.emby-tab-button'):null;
if(n)sfHdrHold();}catch(err){}
},true);}catch(e){}
/* sf-mylist: the single strongest "come back tomorrow" row, and the one thing
   the home page was missing -- what the viewer themselves saved.

   NOT the Home Screen Sections plugin's built-in "MyList". That section exists
   and was enabled to test it: it returns 0 items because it reads JELLYSEERR's
   watchlist, not this server's. Measured on the admin: Likes = 22 items, IsFavorite
   = 1, plugin MyList = 0. The plugin then omits empty sections from
   /HomeScreen/Sections entirely, which is why enabling it changed nothing.

   The real watchlist is Jellyfin's own **Likes** flag -- what the detail-page
   eye button and Swiparr hearts write, and what My Stuff > Watchlist lists (see
   jf-watchlist-btn). Same source here, so the row always agrees with that tab.

   Fetched ONCE per user per page load and cached: the row is rebuilt from cache
   whenever Jellyfin re-renders the home view, without re-querying. Newly saved
   items appear on the next load, which is the right trade for a row that must
   not add a request to every tick.
   Renders nothing when the watchlist is empty -- an empty row is worse than no
   row, and a new user has nothing saved yet. */
var sfMlItems=null, sfMlBusy=false, sfMlUid=null;
/* sf-sec-find: locate one of Jellyfin's home rows WITHOUT relying on its heading
   text. Every custom row used to anchor on English strings ("next up",
   "continue watching", "discover", "recently added shows"), so on a German,
   Chinese or French UI the anchor never matched and the row was silently
   DROPPED -- verified: Watchlist and Live TV rendered on `en` and were entirely
   absent on de/zh-CN/fr, for the very users the translation work is for.

   Jellyfin puts a stable, untranslated class on each section
   (.ContinueWatching, .NextUp, .RecentlyAddedMovies, .RecentlyAddedShows,
   .Discover), so match on that first and keep the text test only as a fallback
   for builds that might not carry it. */
function sfFindSection(root,cls,rx){
var i,all=root.querySelectorAll('.verticalSection'),t;
for(i=0;i<all.length;i++)if(all[i].classList&&all[i].classList.contains(cls))return all[i];
if(rx)for(i=0;i<all.length;i++){
t=all[i].querySelector('.sectionTitle');
if(t&&rx.test((t.textContent||'')))return all[i];
}
return null;
}
function sfMyList(){
var page=document.querySelector('#indexPage:not(.hide)');
if(!page)return;
var secs=page.querySelector('.sections.homeSectionsContainer');
if(!secs)return;
var ac=window.ApiClient;
if(!ac||!ac.getCurrentUserId)return;
var uid=ac.getCurrentUserId();
if(!uid)return;
if(sfMlUid!==uid){sfMlUid=uid;sfMlItems=null;sfMlBusy=false;}
if(sfMlItems===null){
if(sfMlBusy)return;
sfMlBusy=true;
ac.getJSON(ac.getUrl('Users/'+uid+'/Items',{Filters:'Likes',Recursive:true,
IncludeItemTypes:'Movie,Series',Limit:30,SortBy:'DateCreated',SortOrder:'Descending',
Fields:'PrimaryImageAspectRatio'}))
.then(function(r){sfMlItems=(r&&r.Items)||[];sfMlBusy=false;})
.catch(function(){sfMlItems=[];sfMlBusy=false;});
return;
}
if(!sfMlItems.length)return;
/* Identity is .sf-mylistrow, NOT .sf-mylist: the music row reuses .sf-mylist for
   its card styling, and guarding on the shared class made this function believe
   the row already existed -- My List silently stopped rendering the moment the
   music row shipped. Styling class shared, identity class unique. */
if(secs.querySelector('.sf-mylistrow'))return;
var sec=document.createElement('div');
sec.className='verticalSection sf-mylist sf-mylistrow';
var head=document.createElement('div');
head.className='sectionTitleContainer sectionTitleContainer-cards';
var h2=document.createElement('h2');
/* native title classes so the heading matches every other row exactly */
h2.className='sectionTitle sectionTitle-cards';
/* Renamed from 'My List' 2026-08-17. The detail-page button and the drawer
   entry already said Watchlist, so the row was the odd one out. */
h2.textContent='Watchlist';
head.appendChild(h2);
sec.appendChild(head);
var row=document.createElement('div');
row.className='sf-ml-row';
var i,it,card,post,ttl,url;
for(i=0;i<sfMlItems.length;i++){
it=sfMlItems[i];
card=document.createElement('div');
card.className='sf-ml-card';
card.setAttribute('data-id',it.Id);
/* sf-resume-pos: this row asks sfAddCardOverlay for 'resume', which needs a
   position or Jellyfin restarts the item from 00:00 (the audiobook-row bug).
   Latent here only because nothing part-watched happened to be liked at the
   time -- like a half-finished film and it bites immediately. */
card.setAttribute('data-positionticks',
  ((it.UserData||{}).PlaybackPositionTicks)||'');
post=document.createElement('div');
post.className='sf-ml-poster';
try{url=ac.getImageUrl(it.Id,{type:'Primary',maxWidth:300,
tag:(it.ImageTags||{}).Primary});}catch(e){url='';}
if(url)post.style.backgroundImage='url("'+url+'")';
/* Use JELLYFIN'S OWN card text classes rather than restyling from scratch.
   Measured against a native poster card: title 17.86px / weight 600 /
   rgba(255,255,255,0.8), then a SECOND line for the year at 16px / weight 200 /
   rgba(255,255,255,0.5). Our single 12.8px grey line was visibly foreign -- and
   re-deriving those numbers is how it got foreign in the first place, so this
   inherits them instead and cannot drift when the theme changes. */
ttl=document.createElement('div');
ttl.className='cardText cardText-first';
ttl.textContent=it.Name||'';
var sub=document.createElement('div');
sub.className='cardText cardText-secondary';
/* native shows "2023" for a film and "1997 - Present" for a running series */
var yr=it.ProductionYear?String(it.ProductionYear):'';
if(yr&&it.Type==='Series'){
if(it.Status==='Continuing')yr=yr+' - Present';
else if(it.EndDate)yr=yr+' - '+String(it.EndDate).slice(0,4);
}
sub.textContent=yr;
card.appendChild(post);card.appendChild(ttl);
if(yr)card.appendChild(sub);
/* Same contract as every other home row: the ARTWORK plays, the ⋮ opens details.
   This row had no corner control at all. The card-level click below still runs
   for taps on the title/year strip, because the poster handler stops
   propagation before it. */
sfAddCardOverlay(card,it.Id,it.Type||'Movie',it.MediaType||'Video',!!it.IsFolder,'resume');
/* the app routes on the hash; this is the same target a native card uses */
card.addEventListener('click',function(){
location.hash='#/details?id='+this.getAttribute('data-id');});
row.appendChild(card);
}
sec.appendChild(row);
/* straight after Next Up -- Continue Watching and Next Up answer "carry on",
   this answers "I saved something for tonight", and everything below it is
   recommendation. Falls back to the top if Next Up is absent. */
var target=sfFindSection(secs,'NextUp',/next up/i);
if(!target)target=sfFindSection(secs,'ContinueWatching',/continue watching/i);
/* WAIT for an anchor rather than falling back to the top. The native rows are
   rendered asynchronously, so on the first ticks after a load this container is
   empty -- an earlier version prepended in that case, and because the "already
   built" guard above then short-circuits every later pass, the row stayed pinned
   at the very top for the rest of the session, above Continue Watching and
   overlapping the hero. There is no rush: returning here just tries again on the
   next tick, by which point the rows exist. */
if(!target||!target.parentNode)return;
/* DOM position is not enough. The sections container is display:flex /
   column, and Home Screen Sections writes an inline `order` on every row from
   its OrderIndex (Continue Watching 2, Next Up 3, Trending 6, ...). A row with
   no order defaults to 0, so ours sorted ABOVE everything regardless of where it
   was inserted -- it rendered at the very top, over the hero, while sitting
   correctly between Next Up and Trending in the DOM.
   Taking the anchor's order + 1 puts us in the gap after it (3 -> 4, and the
   next row is 6), and adapts if the sections are ever reordered. The DOM
   insertion still matters: equal orders fall back to document order. */
var aOrd=parseInt(getComputedStyle(target).order,10);
if(isFinite(aOrd))sec.style.order=(aOrd+1);
target.parentNode.insertBefore(sec,target.nextSibling);
}
'''

# _LS_07 (orig L4368-5075) -- sf-music-tabs, sf-music-home, sf-music-row
_LS_07 = r'''/* sf-music-tabs: order the music sub-tabs by how the library is actually used --
   Suggestions, Playlists, Albums, Artists, Songs -- instead of Jellyfin's
   Albums-first default. Suggestions is meant to be the landing page, so it leads.

   Done with flex `order` on the buttons, NOT by moving them in the DOM: Jellyfin
   maps a tab to its pane by the data-index attribute, and reordering nodes risks
   any index-by-position logic. Verified after: clicking Playlists (data-index 4,
   now second visually) still activates pane data-index 4, and the active marker
   follows correctly.

   The slider ships as display:block, so it has to become flex for order to mean
   anything; centring is restated because the block layout centred by other means.

   Route-scoped on purpose. `.tabs-viewmenubar` is every library's sub-tab strip
   and Movies/Shows use the same data-index numbering, so an unscoped rule would
   scramble their tabs. The music strip is the one holding data-index buttons on
   #/music. */
/* sf-music-home: make Suggestions a music home page rather than a leftovers pile.

   Jellyfin ships it as Recently Added, Recently Played, Frequently Played, then
   a favourites block whose heading is just "Albums" (the block is a wrapper
   section containing favourite artists/albums/songs, which is why "Albums"
   appeared twice in the DOM).

   Reordered by intent, the way a music app is actually used: what you were just
   listening to, then what you always listen to, then what is new, then what you
   have starred. Recently Added leading was the least useful of the four -- it is
   sorted by what the SERVER got, not by anything about the listener.

   Ordering uses flex `order` on the pane's direct children, so nothing moves in
   the DOM and Jellyfin's own rendering of each section is untouched; the pane
   ships as a block so it has to become a column flexbox for that to apply.

   The greeting is the "this is mine" moment -- time-aware and named. It is
   wrapped in Jellyfin's own .padded-left so it lines up with the section
   headings instead of sitting flush against the window edge. */
/* sf-music-row: Recently Added Music on the home page.

   Built client-side for the same reason My List is: the Home Screen Sections
   plugin HAS a RecentlyAddedAlbums section, it was enabled, and its endpoint
   returns 16 albums -- but the plugin's /HomeScreen/Sections still does not
   serve it. That list is a per-user selection which does not follow the global
   config (it serves cs-trending-movies, which is globally DISABLED, and omits
   sections that are globally enabled). Rather than fight an override I could not
   locate, this uses the same proven row-building path as sf-mylist.

   Square art, not 2:3: albums are square, and stretching them into poster cards
   is the tell that a music row was bolted onto a video UI. */
/* sf-livetv-row: the Live TV channel row, directly above Discover.

   Landscape cards, because a channel's Primary image is a wide logo card
   (measured aspect 1.76-2.0), not a poster -- and because that is the shape
   every streaming service uses for live content. Card widths are the native
   LANDSCAPE ladder: measured against Continue Watching's own cards, a native
   landscape card is 23.1vw where a portrait one is 13.3vw, so the portrait
   ladder in sf-mylist is scaled by that 1.737 ratio. The 13.3 -> 23.1 step is
   the one actually measured, and it lands exactly on the native value.

   Art is `contain`, not `cover`: these are logo cards, and cropping 11% off the
   sides of a 2:1 logo to fill a 16:9 box cuts into the channel name.

   The LIVE badge and the progress bar are what make this feel like live TV
   rather than another content row -- the bar is how far through the current
   programme you are, so a channel that has just started reads differently from
   one that is nearly over. AddCurrentProgram gives us that in the same request;
   no second round trip.

   Channels with no current programme (LU TV, the ErsatzTV filler) still appear
   -- it is a CHANNEL row, and a gap where channel 1 should be looks broken. */
var sfLtItems=null, sfLtBusy=false, sfLtUid=null, sfLtTick=0, sfLtBuilt=Date.now();
function sfLtPct(s,e){
var p=(Date.now()-s)/(e-s);
return p<0?0:(p>1?1:p);
}
/* The bars go stale on a page left open, so they are refreshed -- but only every
   20 seconds and only when the row exists. A programme is tens of minutes long,
   so anything faster is invisible work on every one of the 400ms ticks. */
function sfLtProg(){
var now=Date.now();
if(now-sfLtTick<20000)return;
sfLtTick=now;
/* A row headed "what is on now" cannot show a programme that finished half an
   hour ago, and the bar alone cannot fix that -- when a programme ends the whole
   card is wrong, art and title included. Every 5 minutes the cache is dropped
   and the row removed so the next tick rebuilds it from a fresh query. One
   request, one frame, and the row is usually off-screen when it happens. */
if(now-sfLtBuilt>300000){
sfLtBuilt=now;
sfLtItems=null;
var old=document.querySelector('.sf-livetvrow');
if(old&&old.parentNode)old.parentNode.removeChild(old);
return;
}
var cards=document.querySelectorAll('.sf-ltv-card[data-s]'),i,c,f,s,e;
for(i=0;i<cards.length;i++){
c=cards[i];
f=c.querySelector('.sf-ltv-prog i');
if(!f)continue;
s=+c.getAttribute('data-s');e=+c.getAttribute('data-e');
if(!isFinite(s)||!isFinite(e)||e<=s)continue;
var _f='scaleX('+sfLtPct(s,e).toFixed(4)+')';if(f.style.transform!==_f)f.style.transform=_f;
}
}
function sfLiveTvRow(){
/* Wait for the hero. Measured on a cold home load: this fired at ~1385ms and
   took 1380ms, landing on the exact instant Media Bar was querying its own
   items -- two heavy queries hitting a NAS that answers them serially, so the
   artwork filling the screen finished behind a row nobody had scrolled to yet.
   __sfHeroPainted is set by the first backdrop's load event and, failing that,
   by a 2.5s timer in sf-hero-srccap, so this can defer but never strand. */
if(!window.__sfHeroPainted&&(location.hash||'').indexOf('#/home')===0)return;
var page=document.querySelector('#indexPage:not(.hide)');
if(!page)return;
var secs=page.querySelector('.sections.homeSectionsContainer');
if(!secs)return;
var ac=window.ApiClient;
if(!ac||!ac.getCurrentUserId)return;
var uid=ac.getCurrentUserId();
if(!uid)return;
if(sfLtUid!==uid){sfLtUid=uid;sfLtItems=null;sfLtBusy=false;}
if(sfLtItems===null){
if(sfLtBusy)return;
sfLtBusy=true;
ac.getJSON(ac.getUrl('LiveTv/Channels',{userId:uid,Limit:24,
EnableImages:true,AddCurrentProgram:true,EnableUserData:false}))
.then(function(r){
/* Only channels ACTUALLY AIRING something with artwork. This row is "what is on
   now", so a channel with nothing on is not a smaller version of that -- it is a
   different thing, and it looked like filler.
   Drops three kinds of card in one rule: the ErsatzTV filler channel (LU TV,
   which never carries guide data), the "Upcoming ..." placeholder channels the
   sports sync creates, and any real channel whose guide has gone stale. Measured
   10 of 20 channels qualify at any moment, which is a full row. */
var all=(r&&r.Items)||[],keep=[],k;
for(k=0;k<all.length;k++){
var c=all[k];
if(c.CurrentProgram&&(c.CurrentProgram.ImageTags||{}).Primary)keep.push(c);
}
sfLtItems=keep;sfLtBusy=false;})
.catch(function(){sfLtItems=[];sfLtBusy=false;});
return;
}
/* nothing airing (or no tuner) -- render no row at all rather than an empty one */
if(!sfLtItems.length)return;
if(secs.querySelector('.sf-livetvrow')){sfLtProg();return;}
var sec=document.createElement('div');
sec.className='verticalSection sf-mylist sf-livetvrow';
var head=document.createElement('div');
head.className='sectionTitleContainer sectionTitleContainer-cards';
var h2=document.createElement('h2');
h2.className='sectionTitle sectionTitle-cards';
h2.textContent='Live TV';
head.appendChild(h2);
sec.appendChild(head);
var row=document.createElement('div');
row.className='sf-ml-row';
var i,it,card,art,ttl,sub,url,cp,st,en,badge,bar,fill,pArt;
for(i=0;i<sfLtItems.length;i++){
it=sfLtItems[i];
card=document.createElement('div');
card.className='sf-ml-card sf-ltv-card';
/* marked here, overlay added once the card is populated (see below) */
card.setAttribute('data-id',it.Id);
art=document.createElement('div');
art.className='sf-ml-poster sf-ltv-art';
cp=it.CurrentProgram;
/* Show WHAT IS ON, not which channel it is on -- the programme is the thing
   being chosen; the channel is only where it happens to live.
   Programme art is a 2:3 POSTER (measured 294x440 on every one), so the card is
   portrait like every other content row on this page and the art simply fills
   it. The earlier blurred-letterbox treatment existed only because the card was
   landscape; with the shapes agreeing it is dead weight and is gone.
   No channel-logo fallback either -- the row is filtered to channels that are
   airing something, so there is nothing left to fall back to. */
var pArt='';
try{pArt=ac.getImageUrl(cp.Id,{type:'Primary',maxWidth:400,
tag:cp.ImageTags.Primary});}catch(e){pArt='';}
if(pArt)art.style.backgroundImage='url("'+pArt+'")';
badge=document.createElement('span');
badge.className='sf-ltv-live';
/* the badge is OURS and was hardcoded English -- translate where it is set */
badge.textContent=(window.sfTr?window.sfTr('LIVE'):'LIVE');
art.appendChild(badge);
if(cp&&cp.StartDate&&cp.EndDate){
st=Date.parse(cp.StartDate);en=Date.parse(cp.EndDate);
if(isFinite(st)&&isFinite(en)&&en>st){
card.setAttribute('data-s',st);
card.setAttribute('data-e',en);
bar=document.createElement('div');
bar.className='sf-ltv-prog';
fill=document.createElement('i');
var _f2='scaleX('+sfLtPct(st,en).toFixed(4)+')';if(fill.style.transform!==_f2)fill.style.transform=_f2;
bar.appendChild(fill);
art.appendChild(bar);
}
}
ttl=document.createElement('div');
ttl.className='cardText cardText-first';
/* programme first, channel underneath -- and the episode title alongside the
   channel when there is one, which is what tells a rerun apart from a new one */
/* programme title: a library match gives us a real translation */
ttl.textContent=(window.sfTrName?window.sfTrName(cp.Name||it.Name||''):(cp.Name||it.Name||''));
sub=document.createElement('div');
sub.className='cardText cardText-secondary';
/* the CHANNEL name is ours (ErsatzTV naming: Comfort Comedy, Disney & Family);
   the episode title beside it is guide data and stays as broadcast. */
var chName=(window.sfTr?window.sfTr(it.Name||''):(it.Name||''));
sub.textContent=chName+(cp.EpisodeTitle?(' \u00b7 '+cp.EpisodeTitle):'');
card.appendChild(art);card.appendChild(ttl);card.appendChild(sub);
/* every other home row has a ⋮; this one had none */
sfAddCardOverlay(card,it.Id,it.Type||'TvChannel','Video',false,'play');
/* #/details on a TvChannel is a real page -- verified: channel art, a Play
   button and the rest of today's schedule. Playing straight from the card would
   be a bigger commitment than a click on a row usually implies. */
card.addEventListener('click',function(){
location.hash='#/details?id='+this.getAttribute('data-id');});
row.appendChild(card);
}
sec.appendChild(row);
/* Directly ABOVE Discover, by the admin's call. Anchoring on Discover rather than
   on a fixed number keeps the two adjacent if the sections are ever reordered:
   its order minus one lands in the gap left by moving music to the end. */
var target=sfFindSection(secs,'Discover',/^\s*discover/i);
if(target&&target.parentNode){
var dOrd=parseInt(getComputedStyle(target).order,10);
if(isFinite(dOrd))sec.style.order=(dOrd-1);
target.parentNode.insertBefore(sec,target);
return;
}
/* Discover comes from Jellyfin Enhanced and can be absent -- fall back to just
   after the last Recently Added row rather than dropping the row entirely. */
target=sfFindSection(secs,'RecentlyAddedShows',/recently added shows/i);
if(!target||!target.parentNode)return;
var aOrd=parseInt(getComputedStyle(target).order,10);
if(isFinite(aOrd))sec.style.order=(aOrd+1);
target.parentNode.insertBefore(sec,target.nextSibling);
}
var sfMrItems=null, sfMrBusy=false, sfMrUid=null, sfMrKind='new';
/* sf-audiobook-row: Audiobooks on the home page, directly below Music.
   See the notes in sf-music-row -- same proven path, cached the same way so the
   400ms tick does not refetch. Portrait cards: a book cover is ~2:3 and square
   crops its title away. */
var sfAbItems=null, sfAbBusy=false, sfAbUid=null, sfAbKind='new';
/* sf-cw-books: merge resumable audiobooks into the Continue Watching row.

   sf-cw-order: the books must land in DATE order among the video cards, not at
   the end. The original merge did a bare cont.appendChild(), so an audiobook
   played five minutes ago still rendered to the right of a film last touched in
   July -- the row looked sorted right up until you used it, which is exactly the
   reported symptom ("it pops up on the end even if it was the last thing").

   Interleaving is done with flex `order`, NOT by moving nodes. Two reasons:
   the container is `display:flex` (verified: .itemsContainer.scrollSlider,
   flex-direction row, every card computing order:0), and Jellyfin re-renders
   this row from its own data -- reordering its children would be undone on the
   next render and risks confusing its scroller bookkeeping. Writing `order` is
   idempotent, so the 400ms tick can re-assert it forever at no cost.

   Native card dates are NOT in the DOM, so they come from the same /Items/Resume
   query that built the row. Cached beside the books and refreshed on the same
   TTL. */
var sfCwBookItems=null, sfCwBookBusy=false, sfCwBookUid=null, sfCwBookAt=0;
var sfCwVidDates=null, sfCwVidBusy=false;
var SF_CW_TTL=60000;
function sfCwDate(v){var t=v?Date.parse(v):NaN;return isFinite(t)?t:0;}
function sfCwBooks(){
var ac=window.ApiClient;
if(!ac||!ac.getJSON||!ac.getCurrentUserId)return;
var uid=ac.getCurrentUserId();
if(!uid)return;
if(sfCwBookUid!==uid){sfCwBookUid=uid;sfCwBookItems=null;sfCwVidDates=null;sfCwBookBusy=false;sfCwVidBusy=false;sfCwBookAt=0;}
var now=Date.now();
/* Refresh on a TTL as well as on first run. Without this the list was fetched
   once per page load, so finishing or advancing a book left both its progress
   bar and its position in the row stale until a manual reload. */
if(sfCwBookItems===null||(now-sfCwBookAt)>SF_CW_TTL){
if(sfCwBookBusy)return;
sfCwBookBusy=true;sfCwBookAt=now;
ac.getJSON(ac.getUrl('Users/'+uid+'/Items',{IncludeItemTypes:'AudioBook',Recursive:true,
SortBy:'DatePlayed',SortOrder:'Descending',Limit:10,Filters:'IsResumable',
Fields:'UserData,PrimaryImageAspectRatio'}))
.then(function(r){sfCwBookItems=(r&&r.Items)||[];sfCwBookBusy=false;})
.catch(function(){if(sfCwBookItems===null)sfCwBookItems=[];sfCwBookBusy=false;});
/* First run only: block until the books land. On a refresh keep rendering the
   cards we already have rather than blanking the row for a network round trip. */
if(sfCwBookItems===null)return;
}
/* Dates for the NATIVE cards, from the query that produced them. */
if(sfCwVidDates===null){
if(!sfCwVidBusy){
sfCwVidBusy=true;
ac.getJSON(ac.getUrl('Users/'+uid+'/Items/Resume',{MediaTypes:'Video',Limit:24,
Fields:'UserData'}))
.then(function(r){
var m={},L=(r&&r.Items)||[],q;
for(q=0;q<L.length;q++)m[sfNorm(L[q].Id)]=sfCwDate((L[q].UserData||{}).LastPlayedDate);
sfCwVidDates=m;sfCwVidBusy=false;})
.catch(function(){sfCwVidDates={};sfCwVidBusy=false;});
}
/* fall through -- cards can still be created, ordering applies once dates land */
}
/* Find the Continue Watching row by its heading, and only inside the page that
   is actually on screen -- this build keeps a cached copy of every visited view
   in the DOM, so a document-wide lookup can land on a hidden one. */
var host=(window.__jfView&&window.__jfView.homePage&&window.__jfView.homePage())||document;
/* class first -- the heading is translated for de/zh users, which used to make
   the audiobooks vanish from Continue Watching on exactly those accounts */
var secs=host.querySelectorAll('.verticalSection'),sec=null,i,h;
for(i=0;i<secs.length;i++){
if(!secs[i].getClientRects().length)continue;
if(secs[i].classList&&secs[i].classList.contains('ContinueWatching')){sec=secs[i];break;}
h=secs[i].querySelector('h2,h3,.sectionTitle');
if(h&&/continue watching/i.test(h.textContent||'')){sec=secs[i];break;}
}
if(!sec)return;
var cont=sec.querySelector('.itemsContainer');
if(!cont)return;
var j,it,ud,pct,card,html;
/* Drop cards for books that have left the resumable set. Only matters now that
   the list is refreshed on a TTL -- before, the fetch happened once per load so
   a finished book could not go stale within the life of the page. Jellyfin
   never created these nodes, so removing them is ours to do. */
var live={};
for(j=0;j<sfCwBookItems.length;j++)live[sfCwBookItems[j].Id]=1;
var olds=cont.querySelectorAll('[data-sf-cwbook]');
for(j=0;j<olds.length;j++){
if(!live[olds[j].getAttribute('data-sf-cwbook')]&&olds[j].parentNode)
olds[j].parentNode.removeChild(olds[j]);
}
if(!sfCwBookItems.length){sfCwRowOrder(cont);return;}
for(j=0;j<sfCwBookItems.length;j++){
it=sfCwBookItems[j];
if(cont.querySelector('[data-sf-cwbook="'+it.Id+'"]'))continue;
ud=it.UserData||{};
pct=(ud.PlayedPercentage||0);
var url='';
try{url=ac.getImageUrl(it.Id,{type:'Primary',maxWidth:400,
tag:(it.ImageTags||{}).Primary});}catch(e){url='';}
card=document.createElement('div');
/* Same classes as the row's own cards, so sizing, hover and the overlay all
   come from Jellyfin rather than being re-styled here. */
card.className='card overflowBackdropCard card-hoverable card-withuserdata sf-cwbook';
card.setAttribute('data-sf-cwbook',it.Id);
card.setAttribute('data-isfolder','false');
card.setAttribute('data-serverid',ac.serverId());
card.setAttribute('data-id',it.Id);
card.setAttribute('data-type','AudioBook');
card.setAttribute('data-mediatype','Audio');
if(ud.PlaybackPositionTicks)card.setAttribute('data-positionticks',ud.PlaybackPositionTicks);
html='<div class="cardBox cardBox-bottompadded"><div class="cardScalable">'
+'<div class="cardPadder cardPadder-overflowBackdrop"></div>'
/* coveredImage KEPT. Dropping it collapsed the container to height 0 (measured)
   and both art layers vanished with it -- that class is what stretches
   .cardImageContainer to fill the card. Its background-size:cover is harmless
   now, because the element itself no longer carries a background-image; the art
   lives in the two children below. */
+'<div class="cardImageContainer coveredImage cardContent itemAction sf-cwbook-img" data-action="link">'
+'<div class="sf-cwbook-blur" style="background-image:url(\'' + url + '\');"></div>'
+'<div class="sf-cwbook-fit" style="background-image:url(\'' + url + '\');"></div>'
+'<div class="cardOverlayContainer itemAction" data-action="link">'
+'<button is="paper-icon-button-light" class="cardOverlayButton cardOverlayButton-hover itemAction paper-icon-button-light cardOverlayFab-primary" data-action="resume" title="Play">'
+'<span class="material-icons cardOverlayButtonIcon cardOverlayButtonIcon-hover play_arrow" aria-hidden="true"></span></button>'
/* sf-cwbook-btns (2026-08-27): these cards had ONLY the play button, so an
   audiobook in Continue Watching had no bottom-right cluster and nothing
   appeared on hover, while every video card beside it did. Measured: the
   episode card carries 6 buttons, ours carried 3, and .cardOverlayButton-br
   was display:none because it did not exist.
   Markup copied verbatim from a live native card so Jellyfin's own DELEGATED
   handlers pick it up -- the menu is plain data-action="menu" on .itemAction
   and reads the card's data-id / data-type / data-serverid, all of which this
   card already sets. */
+'<div class="cardOverlayButton-br flex">'
+'<button is="emby-playstatebutton" type="button" data-action="none" class="cardOverlayButton cardOverlayButton-hover itemAction paper-icon-button-light emby-button" '
+'data-id="'+it.Id+'" data-serverid="'+ac.serverId()+'" data-itemtype="AudioBook" data-played="'+(ud.Played?'true':'false')+'" title="Mark played">'
+'<span class="material-icons cardOverlayButtonIcon cardOverlayButtonIcon-hover check playstatebutton-icon-'+(ud.Played?'played':'unplayed')+'" aria-hidden="true"></span></button>'
+'<button is="emby-ratingbutton" type="button" data-action="none" class="cardOverlayButton cardOverlayButton-hover itemAction paper-icon-button-light emby-button" '
+'data-id="'+it.Id+'" data-serverid="'+ac.serverId()+'" data-itemtype="AudioBook" data-likes="" data-isfavorite="'+(ud.IsFavorite?'true':'false')+'" title="Add to favorites">'
+'<span class="material-icons cardOverlayButtonIcon cardOverlayButtonIcon-hover favorite" aria-hidden="true"></span></button>'
+'<button is="paper-icon-button-light" class="cardOverlayButton cardOverlayButton-hover itemAction paper-icon-button-light" data-action="menu" title="More">'
+'<span class="material-icons cardOverlayButtonIcon cardOverlayButtonIcon-hover more_vert" aria-hidden="true"></span></button>'
+'</div>'
+'</div></div>'
/* innerCardFooterClear matches the native cards -- without it the footer paints its
   own background behind the progress bar and the bar sits on a darker strip. */
+(pct>0?('<div class="innerCardFooter fullInnerCardFooter innerCardFooterClear"><div class="itemProgressBar">'
+'<div class="itemProgressBarForeground" style="width:'+Math.min(100,Math.round(pct))+'%;"></div>'
+'</div></div>'):'')
+'</div><div class="cardText cardTextCentered cardText-first">'+(it.Name||'').replace(/</g,'&lt;')+'</div>'
+'<div class="cardText cardTextCentered cardText-secondary">'
+((it.AlbumArtist||(it.Artists&&it.Artists[0])||'')+'').replace(/</g,'&lt;')+'</div></div>';
card.innerHTML=html;
card.setAttribute('data-sf-cwdate',sfCwDate(ud.LastPlayedDate));
cont.appendChild(card);
}
/* Keep an existing card's date fresh across a TTL refresh, otherwise a book
   that was just played keeps sorting on the timestamp it had at page load. */
for(j=0;j<sfCwBookItems.length;j++){
it=sfCwBookItems[j];
card=cont.querySelector('[data-sf-cwbook="'+it.Id+'"]');
if(card)card.setAttribute('data-sf-cwdate',sfCwDate((it.UserData||{}).LastPlayedDate));
}
sfCwRowOrder(cont);
}
/* sf-cw-roworder: interleave our audiobook cards with Jellyfin's video cards by
   last-played date, using flex `order` so no node is ever moved.

   Native cards keep their DOM sequence as the tiebreak: Jellyfin already sorted
   them, so where a date is missing (an id absent from the resume response, a
   card the row added itself) the card simply holds its current place instead of
   being flung to one end. Books are then slotted against those anchors. */
function sfCwRowOrder(cont){
if(!cont||!sfCwVidDates)return;
var kids=cont.children,n=kids.length,i,c,d,rows=[];
if(!n)return;
for(i=0;i<n;i++){
c=kids[i];
if(c.hasAttribute('data-sf-cwbook')){
d=parseInt(c.getAttribute('data-sf-cwdate'),10)||0;
rows.push({el:c,date:d,book:1,seq:i});
}else{
d=sfCwVidDates[sfNorm(c.getAttribute('data-id'))];
/* No date -> inherit the previous native card's, so it stays put rather than
   sorting to the far end of the row. */
if(!d)d=(rows.length?rows[rows.length-1].date:Number.MAX_SAFE_INTEGER);
rows.push({el:c,date:d,book:0,seq:i});
}
}
rows.sort(function(a,b){
if(b.date!==a.date)return b.date-a.date;   /* newest first */
if(a.book!==b.book)return a.book-b.book;   /* a tie keeps video ahead of book */
return a.seq-b.seq;                        /* otherwise DOM order, so it is stable */
});
for(i=0;i<rows.length;i++){
/* +1 so nothing is left on the flex default of 0, which would float ahead of
   an explicitly ordered sibling. */
var o=String(i+1);
if(rows[i].el.style.order!==o)rows[i].el.style.order=o;
}
}
/* sf-card-hover: give a custom row card the same hover affordances as a native
   one -- a primary Play, and a ⋮ in the bottom-right corner for the detail page.
   Jellyfin's class names are reused so the look and hover states come from its
   own stylesheet; the CLICKS are ours, because its delegation is not bound to
   our rows. */
/* sf-retap (2026-08-20). Tapping a card for the thing that is ALREADY playing
   used to start it over from 00:00. Reproduced on the audiobook row: play a
   book, let it run to 17s, tap the same cover -- back to 0.

   Two separate faults, both fixed here.

   1. The row writes `data-positionticks` once, when it is BUILT, and the row is
      built once per page load. A book you started in this session still carries
      the position it had at build time -- usually empty, because the row is
      "recently added" -- so the tap handler sends action 'play' instead of
      'resume' and Jellyfin honours that literally. sfCardPos() below keeps the
      attribute in step with the running <audio>, so the second tap has a real
      position to resume to.

   2. Even with a correct position, restarting the stream to seek back to where
      you already are is pointless work and a visible audio gap. Every mainstream
      player treats "tap what is already playing" as a no-op (or as unpause).
      sfIsNowPlaying() gives every card handler that check.

   The <audio> element's own URL is the only id that cannot be stale -- the
   now-playing bar lags it by ~2s on a switch, which is the same lag the
   audiobook player's switchguard works around. */
function sfAudioId(){
var a=document.querySelector('audio');
if(!a)return '';
var src=a.currentSrc||a.src||'';
var m=/\/(?:Audio|Videos)\/([0-9a-fA-F-]{32,36})\//.exec(src);
return m?sfNorm(m[1]):'';
}
function sfIsNowPlaying(id){
var n=sfNorm(id);
if(!n)return false;
if(sfAudioId()===n)return true;
/* sf-retap-robust (2026-08-20): do not depend on parsing the stream URL. It is
   the most reliable signal when it works, but the /Audio/<id>/ shape is not
   guaranteed (measured: one WebKit run fell through and the tap resumed to a
   stale position instead of being ignored, which is the original restart bug
   coming back intermittently). Two independent fallbacks:
     - the id we ourselves last started through the proxy, and
     - the now-playing bar's own data-id.
   Any of the three agreeing, with audio actually present, means "this is what is
   playing" and the tap must not restart it. */
var a=document.querySelector('audio');
if(!a)return false;
if(window.__sfLastPlayId&&sfNorm(window.__sfLastPlayId)===n)return true;
try{
var bars=document.querySelectorAll('.nowPlayingBar'),i,b;
for(i=0;i<bars.length;i++){
if(!bars[i].getClientRects().length)continue;
b=bars[i].querySelector('[data-id]');
if(b&&sfNorm(b.getAttribute('data-id'))===n)return true;
}
}catch(e){}
return false;
}
/* Tap on the item already loaded: unpause if they had paused it, otherwise
   leave it completely alone. Returns true when it handled the tap. */
function sfRetapGuard(id){
if(!sfIsNowPlaying(id))return false;
var a=document.querySelector('audio');
try{if(a&&a.paused)a.play();}catch(e){}
return true;
}
/* Keep the tapped-card position honest while it plays. Cheap: one attribute
   write per second at most, only on cards for the item actually playing. */
var sfCardPosAt=0;
function sfCardPos(){
var now=Date.now();
if(now-sfCardPosAt<1000)return;
sfCardPosAt=now;
var a=document.querySelector('audio'),aid=sfAudioId();
if(!a||!aid||!isFinite(a.currentTime)||a.currentTime<=0)return;
var ticks=String(Math.floor(a.currentTime*10000000));
var cards=document.querySelectorAll('.sf-ml-card[data-id]'),i,c;
for(i=0;i<cards.length;i++){
c=cards[i];
if(sfNorm(c.getAttribute('data-id'))===aid)c.setAttribute('data-positionticks',ticks);
}
}
function sfAddCardOverlay(card,id,type,mediaType,isFolder,action){
if(!card||card.querySelector('.sf-ml-ov'))return;
var ov=document.createElement('div');
ov.className='sf-ml-ov';
/* the scrim dimmed the poster for a centre Play button that is gone now, and it
   was making the music and audiobook rows look permanently darkened */
ov.style.background='transparent';
ov.style.pointerEvents='none';
/* sf-card-tap: the ARTWORK is the play button. There is no separate centre
   control any more -- it was a second target for the same intent and on a phone
   it simply covered the cover. The ⋮ keeps its own handler and stops
   propagation, so it is still reachable. */
/* sf-mlcard-wholecard (2026-08-29). The admin: "when i press a card near the edges
   and not in the center it still takes me to the info page".
   The listener was on .sf-ml-poster -- the artwork IMAGE -- so every tap that
   landed on the card's own padding missed it and fell through to the detail
   page. Same defect the native cards had (sf-tap-wholecard), and the earlier
   fix did not reach here because these rows are .sf-ml-card, not .card.
   Bind the whole CARD instead, and split inside the handler:
     the ⋮      -> its own handler
     the TITLE  -> the info page (these titles are plain divs with no link of
                   their own, so this is what makes them behave like a native
                   card's <a href="#/details">)
     anything else (the whole poster and its padding) -> play. */
var playHost=card;
if(!playHost.getAttribute('data-sf-tap')){
playHost.setAttribute('data-sf-tap','1');
playHost.style.cursor='pointer';
playHost.addEventListener('click',function(e){
if(e.target&&e.target.closest&&e.target.closest('.sf-ml-br'))return;   /* the ⋮ */
if(e.target&&e.target.closest&&e.target.closest('.cardText')){
e.preventDefault();e.stopPropagation();
location.hash='#/details?id='+id;return;}
e.preventDefault();e.stopPropagation();
/* sf-retap: never restart what is already playing */
if(sfRetapGuard(id))return;
/* sf-resume-pos: Jellyfin's 'resume' action needs a POSITION. Without
   data-positionticks it has nothing to resume to and silently restarts the item
   from 00:00 -- which is exactly what tapping a part-finished audiobook did:
   the row drew the progress bar from UserData and then threw that position
   away. Read from the CARD at click time, not captured when the row was built,
   because the row is built once while the position keeps moving as it plays.
   No position (never started) -> 'play', so 'resume' is never sent empty. */
var pt=(card&&card.getAttribute&&card.getAttribute('data-positionticks'))||'';
var act=pt?action:(action==='resume'?'play':action);
if(!sfPlayItemViaProxy(id,type,mediaType,isFolder,act,pt))location.hash='#/details?id='+id;
});
}
/* sf-cwrm: the corner menu is gone from the home rows -- the admin asked for the
   3 dots off every poster there. It is still built (hidden by CSS) rather than
   deleted, because the play handler above explicitly ignores taps inside
   .sf-ml-br and other code looks it up; removing the node would change those
   paths for no gain. Removal now lives on the hover button instead. */
var br=document.createElement('div');
br.className='cardOverlayButton-br flex sf-ml-br sf-menu-off';
var more=document.createElement('button');
more.type='button';
more.className='cardOverlayButton sf-ml-more';
more.title='Go to details';
more.innerHTML='<span class="material-icons cardOverlayButtonIcon more_vert" aria-hidden="true"></span>';
more.addEventListener('click',function(e){
e.preventDefault();e.stopPropagation();
location.hash='#/details?id='+id;
});
br.appendChild(more);
ov.appendChild(br);
/* Attach to the POSTER, not the card: anchored to the card the scrim ran on
   past the artwork and sat over the title and artist lines, which read as a
   dark box stuck on top rather than part of the cover. */
var host=card.querySelector('.sf-ml-poster')||card;
host.appendChild(ov);
}
function sfPlayItemViaProxy(id,type,mediaType,isFolder,action,positionTicks){
try{
var ac=window.ApiClient;if(!ac||!id)return false;
/* This whole function is wrapped in try/catch, so anything throwing here fails
   SILENTLY -- no error, no proxy, nothing plays. That is what happened on the
   music landing page: the host lookup is home-page specific and the container it
   found belonged to a HIDDEN page, so the proxy card was never usable.
   Resolve a VISIBLE container first and treat the home-page host as a fallback. */
var host=document;
try{
if(window.__jfView&&window.__jfView.homePage)host=window.__jfView.homePage()||document;
}catch(e){host=document;}
var cont=null,_all=document.querySelectorAll('.itemsContainer'),_ci;
for(_ci=0;_ci<_all.length;_ci++){
if(_all[_ci].getClientRects().length){cont=_all[_ci];break;}
}
if(!cont)cont=host.querySelector('.itemsContainer')||document.querySelector('.itemsContainer');
if(!cont)return false;
/* ONE PERSISTENT PROXY, never removed.

   The earlier version created a card, clicked it, and deleted it after 3s. That
   throws "Cannot set properties of null (setting 'innerHTML')" -- reproduced
   again on the hero play fix -- because Jellyfin ADOPTS whatever card started
   playback and keeps writing state into it (progress, played state). Deleting it
   leaves those writes on a detached node, and the half-finished handler can also
   navigate. Rewriting one node's attributes has none of that. */
var proxy=document.getElementById('sf-play-proxy');
if(!proxy){
proxy=document.createElement('div');
proxy.id='sf-play-proxy';
proxy.className='card sf-mu-proxy';
/* Parked INSIDE the viewport, not at left:-9999px. Jellyfin focuses whatever
   card started playback (its focus manager, chunk 4113), and the browser
   scrolls to bring a focused element into view -- with the proxy parked far
   off-screen that threw the page across the document, which is the "playing
   from the music row jumps me to the top" report (measured 3219 -> 328).
   One transparent pixel in the corner is focusable with nothing to scroll to. */
proxy.style.cssText='position:fixed;left:0;top:0;width:1px;height:1px;'
+'opacity:0;pointer-events:none;overflow:hidden;z-index:-1;';
/* The wrapper carries NEITHER itemAction NOR data-action="link": with them the
   click bubbles from the play button to the wrapper and navigates as well as
   plays. Only the button itself is actionable. */
proxy.innerHTML='<div class="cardBox"><div class="cardScalable">'
+'<div class="cardOverlayContainer">'
+'<button is="paper-icon-button-light" tabindex="-1" class="cardOverlayButton itemAction paper-icon-button-light" data-action="play" title="Play">'
+'<span class="material-icons play_arrow"></span></button></div></div></div>';
}
if(proxy.parentNode!==cont)cont.appendChild(proxy);
proxy.setAttribute('data-isfolder',isFolder?'true':'false');
proxy.setAttribute('data-serverid',ac.serverId());
proxy.setAttribute('data-id',id);
proxy.setAttribute('data-type',type||'MusicAlbum');
proxy.setAttribute('data-mediatype',mediaType||'Audio');
/* resume needs the position: without data-positionticks Jellyfin's resume action
   has nothing to resume TO and quietly does nothing -- which is exactly what a
   tap on a Continue Watching card did (proxy created, no playback). */
if(positionTicks)proxy.setAttribute('data-positionticks',positionTicks);
else proxy.removeAttribute('data-positionticks');
var btn=proxy.querySelector('button[data-action]');
if(!btn)return false;
btn.setAttribute('data-action',action||'play');
/* sf-retap-robust: remember what we asked for, so a second tap on the same thing
   is recognisable even if the stream URL cannot be parsed. */
try{window.__sfLastPlayId=id;}catch(e){}
/* Clicking the proxy moves focus to it, and the browser scrolls the focused
   element into view -- the proxy is parked off-screen, so the page jumped to the
   top. That is the "playing from the music row throws me back to the top of home"
   report (measured: scrollY 900 -> 234). Hold the scroll position across the
   click and for a few frames after, since focus settles asynchronously. */
try{sfSpinShow();}catch(e){}
var sx=window.pageXOffset,sy=window.pageYOffset;
var keep=0;
function hold(){
if(window.pageYOffset!==sy||window.pageXOffset!==sx)window.scrollTo(sx,sy);
if(++keep<90)requestAnimationFrame(hold);
}
/* The 90-frame hold above covers the focus jump, but NOT the second jump:
   starting playback makes Jellyfin refresh the home rows, and cards appearing or
   disappearing ABOVE the viewport shifts the page with no scroll call at all --
   measured 2482 -> 292 about 13s after the tap, with a scroll trap recording no
   scrollTo/scrollIntoView/scrollTop from anyone.
   So watch a while longer and put it back, but stop the moment the user scrolls
   deliberately -- otherwise this would fight them. */
var guardUntil=Date.now()+20000, cancelled=false;
function stopGuard(){cancelled=true;}
window.addEventListener('touchstart',stopGuard,{passive:true,once:true});
window.addEventListener('wheel',stopGuard,{passive:true,once:true});
window.addEventListener('keydown',stopGuard,{once:true});
/* sf-guard-route (2026-08-20). This guard exists to stop Jellyfin's post-play row
   refresh from jerking the CURRENT page around. It had no route scope, so it
   kept forcing the old scroll offset for a full 20s AFTER you navigated
   somewhere else -- start an audiobook, tap Music, and the music page is dragged
   back to the home page's offset with its hero (and the Play/Mix buttons)
   parked at y=-744, off the top of the screen. Reproduced twice on a phone
   viewport; nothing on the new page could be tapped until the guard expired.
   A route change means the page it was protecting is gone, so the guard is done. */
var guardHash=location.hash;
window.addEventListener('hashchange',stopGuard,{once:true});
window.addEventListener('popstate',stopGuard,{once:true});
(function watch(){
/* also stop the moment the route no longer matches the page we were guarding */
if(location.hash!==guardHash)cancelled=true;
if(cancelled||Date.now()>guardUntil){
window.removeEventListener('touchstart',stopGuard);
window.removeEventListener('wheel',stopGuard);
window.removeEventListener('keydown',stopGuard);
return;
}
if(Math.abs(window.pageYOffset-sy)>200)window.scrollTo(sx,sy);
setTimeout(watch,250);
})();
btn.click();
'''

# _LS_08 (orig L5075-5789) -- sf-play-confirm, sf-abgo, sf-ablib-nopeople
_LS_08 = r'''/* sf-play-confirm (2026-08-21). Clicking the proxy is not proof that anything
   played. Measured on a phone viewport: tapping a "Made for you" mix card
   started audio on 5 of 6 cold loads -- on the 6th the click dispatched, the
   proxy was adopted and __sfLastPlayId was set, but Jellyfin never created a
   media element at all. One tap in six doing nothing is exactly the
   unreliability that gets reported as "it just doesn't play sometimes".

   So confirm the intent actually took, and re-fire once if it did not. The
   retry is deliberately conservative: it needs BOTH no media element anywhere
   AND no visible now-playing bar, i.e. nothing whatsoever happened. A merely
   slow start always has an <audio> element by then, so this cannot double-start
   something that was only buffering. Also bails out if the route changed, so it
   never fires playback onto a page the user has already left. */
(function(){
var want=id, atHash=location.hash, tries=0;
function nothingHappened(){
if(document.querySelector('audio,video'))return false;
var bars=document.querySelectorAll('.nowPlayingBar'),i;
for(i=0;i<bars.length;i++){if(bars[i].getClientRects().length)return false;}
return true;
}
function confirm(){
if(location.hash!==atHash)return;                 /* user moved on */
if(window.__sfLastPlayId!==want)return;           /* something newer was started */
if(!nothingHappened())return;                     /* it did start -- leave it alone */
if(++tries>1)return;                              /* exactly one retry, never a loop */
try{if(btn&&btn.isConnected)btn.click();}catch(e){}
setTimeout(confirm,2200);
}
setTimeout(confirm,2200);
})();
requestAnimationFrame(hold);
setTimeout(function(){window.scrollTo(sx,sy);},120);
setTimeout(function(){window.scrollTo(sx,sy);},420);
setTimeout(function(){window.scrollTo(sx,sy);},1200);
return true;
}catch(e){return false;}
}
/* sf-abgo (2026-08-21). The admin reports the title tap "only takes us to the top of
   the home page" -- on his device. I could not reproduce it: real pointer taps
   open the book on Chromium-mobile, WebKit-iPhone and desktop, propagation is
   stopped so the card never plays, the scroll guard holds position, and Back
   keeps it too. So rather than keep guessing, make the navigation defensive and
   never silent:
     * refuse to navigate with an empty id (that would land on a broken route,
       which Jellyfin resolves by dropping you on home at the top -- exactly the
       symptom described);
     * confirm the route actually changed, and try once more if it did not;
     * show the spinner immediately, so a slow tap is never mistaken for a dead one. */
function sfAbGo(id){
try{window.__sfAbGo=sfAbGo;}catch(e){}
id=String(id||'').trim();
if(!id)return false;
try{sfSpinShow();}catch(e){}
var want='#/details?id='+id;
if(location.hash===want)return true;
location.hash=want;
setTimeout(function(){
if(location.hash.indexOf(id)<0){
try{location.hash=want;}catch(e){}
}
},450);
return true;
}
/* ---- sf-ablib: the Audiobooks library ----------------------------------
   the admin: "when I go to the hamburger menu and click audiobook it just takes me
   to a list of all audiobooks."

   Correct -- it was Jellyfin's flat A-Z grid of 36 covers with an alphabet
   scrollbar, which is a file listing, not a library. Every audiobook app worth
   copying opens on what you are IN THE MIDDLE OF, then the series you are
   collecting, then what is new. So the page now leads with shelves and keeps the
   full grid underneath, so nothing is lost.

   One request for the whole shelf, held for the session. Cards are the same
   .sf-ml-card the home rows use, tagged data-sf-abcard so sf-abcard enriches
   them with the author, the time left, the series number and the title link. */
var sfAbLib=null,sfAbLibBusy=false;
var SF_ABLIB_KEY='sf-ablib-v1';
/* Measured: opening Audiobooks painted Jellyfin's flat grid at 16ms and our
   shelves at 2235ms -- 2.2 seconds staring at the page you just left, which is
   exactly what reads as "buggy". Two fixes, both about having the data BEFORE
   the navigation rather than after it:
     * hold it in sessionStorage, so every later visit builds synchronously;
     * warm it once shortly after the app settles, so even the first visit is
       ready before you can reach the menu. */
function sfAbLibCached(){
if(sfAbLib!==null)return sfAbLib;
try{
var raw=sessionStorage.getItem(SF_ABLIB_KEY);
if(raw){sfAbLib=JSON.parse(raw);return sfAbLib;}
}catch(e){}
return null;
}
function sfAbLibFetch(cb){
if(sfAbLibCached()){if(cb)cb(sfAbLib);return;}
if(sfAbLibBusy)return;
var ac=window.ApiClient;
if(!ac||!ac.getJSON||!ac.getCurrentUserId)return;
var uid=ac.getCurrentUserId();
if(!uid)return;
sfAbLibBusy=true;
/* sf-ablib-nopeople (2026-08-24): People was requested here and NEVER READ.
   Grepped every `.People` consumer in this file -- 13903 (Author, from its own
   People,Tags fetch) and 14110 (Narrator, from a detail item). Nothing reads
   People off sfAbLib. It is not free: measured standalone against this server,
   twice, on an otherwise idle box --
     Fields=People,Tags,UserData,RunTimeTicks,DateCreated  3.15s / 3.22s
     Fields=People                                         3.31s / 3.21s
     Fields=Tags                                           0.23s / 0.22s
     Fields=UserData,RunTimeTicks,DateCreated              0.23s / 0.22s
   People alone is the entire cost: the BaseItems People table holds 93,589 rows
   and PeopleBaseItemMap has to be joined for every item. Under real home load
   this request measured 7.3-8.4s and was one of four heavy queries competing
   with the home rows. Limit is NOT the issue -- Limit:2000 without People is
   0.22s. Dropping the unused field takes this query from ~3.2s to ~0.22s. */
ac.getJSON(ac.getUrl('Users/'+uid+'/Items',{IncludeItemTypes:'AudioBook',Recursive:true,
Limit:400,Fields:'Tags,UserData,RunTimeTicks,DateCreated'}))
.then(function(r){
sfAbLib=(r&&r.Items)||[];sfAbLibBusy=false;
try{sessionStorage.setItem(SF_ABLIB_KEY,JSON.stringify(sfAbLib));}catch(e){}
if(cb)cb(sfAbLib);
}).catch(function(){sfAbLib=[];sfAbLibBusy=false;});
}
/* warm it once the app is idle, so the shelf is ready before the page is asked for */
function sfAbLibWarm(){
if(window.__sfAbLibWarmed)return;
window.__sfAbLibWarmed=1;
/* sf-prewarm-defer (2026-08-29). Profiled every home row and the bottleneck is
   not any single query -- it is CONCURRENCY. Fourteen heavy queries fire in one
   burst and Jellyfin serialises them, so each reports 7-12s of server time even
   though the same query standalone is a fifth of a second (this file already
   measured Limit:2000 without People at 0.22s).
   These two are PREWARMS on a 2.5s timer -- they were landing at 2.79s and 3.20s,
   squarely in the window the visible rows need, and measured 10.7s and 10.3s of
   server time there. Neither is needed to paint home: both are also called on
   demand by the code that actually uses them, so deferring costs only a first
   lookup, never correctness.
   Pushed past the row settle and then run at idle, so the shelf is still warm
   long before anyone opens an audiobook. */
setTimeout(function(){
try{if(window.requestIdleCallback)requestIdleCallback(function(){try{sfAbLibFetch(null);}catch(e){}},{timeout:8000});else{try{sfAbLibFetch(null);}catch(e){}}}catch(e){try{try{sfAbLibFetch(null);}catch(e){}}catch(e2){}}
},20000);
}
function sfAbLibIsPage(){
var h=location.hash||'';
var ab=(window.SF_CONFIG&&window.SF_CONFIG.audiobookLibraryId)||'';
if(!ab)return false;
return h.indexOf('#/list')===0&&h.indexOf(ab)>=0;
}
function sfAbLibCard(ac,it){
var card=document.createElement('div');
card.className='sf-ml-card';
card.setAttribute('data-id',it.Id);
card.setAttribute('data-sf-abcard','1');
var post=document.createElement('div');
post.className='sf-ml-poster sf-ml-square';
var url='';
if((it.ImageTags||{}).Primary){
try{url=ac.getImageUrl(it.Id,{type:'Primary',maxWidth:400,tag:it.ImageTags.Primary});}catch(e){}
}
if(url)post.style.backgroundImage='url("'+url+'")';
else post.classList.add('sf-ml-noart');
var ud=it.UserData||{};
card.setAttribute('data-positionticks',ud.PlaybackPositionTicks||'');
var pct=ud.PlayedPercentage||0;
if(pct>0&&pct<99){
var bar=document.createElement('div');bar.className='sf-ml-prog';
var fill=document.createElement('div');fill.className='sf-ml-progfill';
fill.style.width=Math.max(2,Math.min(100,pct))+'%';
bar.appendChild(fill);post.appendChild(bar);
}
var ttl=document.createElement('div');
ttl.className='cardText cardText-first';
ttl.textContent=it.Name||'';
var sub=document.createElement('div');
sub.className='cardText cardText-secondary';
sub.textContent='';
card.appendChild(post);card.appendChild(ttl);card.appendChild(sub);
/* resume, so a part-finished book carries on rather than restarting */
sfAddCardOverlay(card,it.Id,'AudioBook','Audio',false,
  (ud.PlaybackPositionTicks?'resume':'play'));
return card;
}
function sfAbLibShelf(title,items,ac){
var sec=document.createElement('div');
sec.className='verticalSection sf-mylist sf-ablib-shelf';
var head=document.createElement('div');
head.className='sectionTitleContainer sectionTitleContainer-cards';
var h2=document.createElement('h2');
h2.className='sectionTitle sectionTitle-cards';
h2.textContent=title;
head.appendChild(h2);
var count=document.createElement('span');
count.className='sf-ablib-count';
count.textContent=items.length+(items.length===1?' book':' books');
head.appendChild(count);
sec.appendChild(head);
var row=document.createElement('div');
row.className='sf-ml-row';
for(var i=0;i<items.length;i++)row.appendChild(sfAbLibCard(ac,items[i]));
sec.appendChild(row);
return sec;
}
function sfAbLibrary(){
try{window.__sfAbLibNudge=sfAbLibrary;}catch(e){}
sfAbLibWarm();
if(!sfAbLibIsPage())return;
var page=null,pages=document.querySelectorAll('.page.libraryPage'),i;
for(i=0;i<pages.length;i++){
if(!pages[i].classList.contains('hide')&&pages[i].offsetParent!==null){page=pages[i];break;}
}
if(!page)return;
var host=page.querySelector('.itemsContainer');
if(!host)return;
host=host.parentElement||host;
var ac=window.ApiClient;
if(!ac||!ac.getJSON||!ac.getCurrentUserId)return;
var uid=ac.getCurrentUserId();
if(!uid)return;
if(sfAbLibCached()===null){
sfAbLibFetch(function(){try{sfAbLibrary();}catch(e){}});
return;
}
if(!sfAbLib.length)return;
/* Jellyfin keeps ONE CACHED PAGE INSTANCE PER URL, so arriving here from the
   home row while an older instance is still in the DOM built the shelves twice
   -- measured 10 shelves and 147 grid cards where there should be 5 and 36.
   Sweep every instance that is not the one on screen. */
var others=document.querySelectorAll('.sf-ablib,.sf-ablib-allhead'),oi;
for(oi=0;oi<others.length;oi++){
if(!page.contains(others[oi])&&others[oi].parentNode)
others[oi].parentNode.removeChild(others[oi]);
}
if(page.querySelector('.sf-ablib'))return;
var wrap=document.createElement('div');
wrap.className='sf-ablib';

/* 1. what you are in the middle of -- the reason you opened the app */
/* Match what the HOME row means by "continue", or the same book is in progress
   on one page and not the other. Home queries Filters=IsResumable; this shelf
   filtered on "any position at all", so a book barely started still sat here
   after it had already dropped off home. Measured on this server:
     IsResumable audiobooks -> 1 (Dungeon Crawler Carl, 8.7%)
     position>0 && !Played  -> 2 (+ It Ends with Us, 1.4%)
   Jellyfin gates resume on MinResumePct/MaxResumePct (5 / 90 here), so apply
   the same window. Change these if those server settings change. */
var SF_AB_MINPCT=5, SF_AB_MAXPCT=90;
var going=sfAbLib.filter(function(x){
var u=x.UserData||{};
if(!u.PlaybackPositionTicks||u.Played)return false;
var pct=u.PlayedPercentage;
if(typeof pct!=='number')return true;
return pct>=SF_AB_MINPCT&&pct<=SF_AB_MAXPCT;});
going.sort(function(a,b){
return String((b.UserData||{}).LastPlayedDate||'').localeCompare(String((a.UserData||{}).LastPlayedDate||''));});
if(going.length){var sfCl=sfAbLibShelf((window.sfTr?window.sfTr('Continue listening'):'Continue listening'),going,ac);sfCl.classList.add('sf-cwscope');wrap.appendChild(sfCl);}

/* 2. a shelf per series, in reading order -- the thing a flat A-Z grid destroys */
var byser={},k;
for(i=0;i<sfAbLib.length;i++){
var tags=sfAbLib[i].Tags||[];
for(k=0;k<tags.length;k++){
if(String(tags[k]).indexOf('Series: ')!==0)continue;
var nm=String(tags[k]).slice(8);
(byser[nm]=byser[nm]||[]).push(sfAbLib[i]);
}
}
var names=Object.keys(byser).filter(function(n){return byser[n].length>1;});
names.sort(function(a,b){return byser[b].length-byser[a].length;});
for(i=0;i<names.length;i++){
byser[names[i]].sort(function(a,b){return (a.IndexNumber||0)-(b.IndexNumber||0);});
wrap.appendChild(sfAbLibShelf(names[i],byser[names[i]],ac));
}

/* 3. what arrived recently */
var recent=sfAbLib.slice().sort(function(a,b){
return String(b.DateCreated||'').localeCompare(String(a.DateCreated||''));}).slice(0,12);
if(recent.length)wrap.appendChild(sfAbLibShelf((window.sfTr?window.sfTr('Recently added'):'Recently added'),recent,ac));

host.parentNode.insertBefore(wrap,host);
/* the flat grid stays, under a heading, so nothing is taken away */
if(!page.querySelector('.sf-ablib-allhead')){
var ah=document.createElement('div');
ah.className='sectionTitleContainer sectionTitleContainer-cards sf-ablib-allhead';
var ah2=document.createElement('h2');
ah2.className='sectionTitle sectionTitle-cards';
ah2.textContent='All books';
ah.appendChild(ah2);
host.parentNode.insertBefore(ah,host);
}
}
var sfLeaveData=null,sfLeaveBusy=false,sfLeaveFav={},sfLeaveFavLoaded=false;
/* sf-leave-favstate: the heart used to start empty on every page load, because
   nothing ever asked the server what was already favourited. A title you had
   saved yesterday showed an outline heart today -- so it looked like the save
   had been lost, and tapping it again SILENTLY UNFAVOURITED it, removing the
   protection the user thought they were re-applying. Reported exactly that way.

   One query per load gets every favourite for this user; the hearts then paint
   from truth instead of from an empty in-memory guess. */
/* sf-leave-painone: paint a SINGLE button, by reference. The previous version
   only had a document-wide sweep, and the card builder called it before
   appendChild -- so at build time querySelectorAll could not see the button yet
   and its icon HTML was never written. The heart then appeared only if some
   later sweep happened to run, which is why it showed up sometimes and not
   others. Painting by reference works whether or not the node is in the DOM. */
function sfLeavePaintOne(b){
if(!b)return;
var on=!!sfLeaveFav[b.getAttribute('data-id')];
b.innerHTML='<span class="material-icons" aria-hidden="true">'
  +(on?'favorite':'favorite_border')+'</span>';
if(on)b.classList.add('sf-on'); else b.classList.remove('sf-on');
var card=b.closest?b.closest('.sf-ml-card'):null;
if(!card)return;
var badge=card.querySelector('.sf-leave-badge');
if(on){card.classList.add('sf-leave-kept');
       if(badge)badge.textContent=b.getAttribute('data-kept')||'Saved';}
else {card.classList.remove('sf-leave-kept');
      if(badge&&b.getAttribute('data-days'))badge.textContent=b.getAttribute('data-days');}
}
function sfLeavePaintAll(){
var list=document.querySelectorAll('.sf-leave-fav[data-id]'),i;
for(i=0;i<list.length;i++)sfLeavePaintOne(list[i]);
}
function sfLeaveLoadFav(){
if(sfLeaveFavLoaded)return;
var ac=window.ApiClient;
if(!ac||!ac.getCurrentUserId||!ac.getCurrentUserId())return;
sfLeaveFavLoaded=true;
try{
ac.getJSON(ac.getUrl('Users/'+ac.getCurrentUserId()+'/Items',
{Filters:'IsFavorite',Recursive:true,IncludeItemTypes:'Movie,Series',Limit:600}))
.then(function(d){
var it=(d&&d.Items)||[],i;
for(i=0;i<it.length;i++)sfLeaveFav[it[i].Id]=true;
sfLeavePaintAll();
/* drop any card that turns out to be favourited already */
var row=document.querySelector('.sf-leavingrow');
if(row){var c=row.querySelectorAll('.sf-ml-card'),z;
for(z=0;z<c.length;z++){
var b=c[z].querySelector('.sf-leave-fav');
if(b&&sfLeaveFav[b.getAttribute('data-id')]&&c[z].parentNode)
c[z].parentNode.removeChild(c[z]);}}
}).catch(function(){sfLeaveFavLoaded=false;});   /* allow a retry next tick */
}catch(e){sfLeaveFavLoaded=false;}
}
function sfPlaceLeaving(secs,sec){
/* Below the WATCHLIST row (the admin, 2026-09-04). Identity class is .sf-mylistrow,
   never .sf-mylist: the leaving row itself carries .sf-mylist for card styling,
   so anchoring on the shared class would match this very row. sfMyList's own
   comment records that exact trap silently killing My List once before.

   Falls back to the resume cluster when there is no watchlist row -- an empty
   watchlist is normal, and the row still has to land somewhere sane. */
var wl=secs.querySelector('.sf-mylistrow');
var anchor=wl
        ||secs.querySelector('.verticalSection.NextUp')
        ||secs.querySelector('.verticalSection.ContinueWatching');

/* sf-leave-flexorder: THE position on this home screen is CSS `order`, not DOM
   order. .sections.homeSectionsContainer is `display:flex; flex-direction:column`
   and every row carries an explicit order -- measured live:

       Continue Watching 2 | Next Up 3 | Watchlist 4 | Trending 6
       Recently Added Movies 8 | Shows 9 | Live TV 10 | Discover 11
       Recently Added Music 999 | Audiobooks 1000

   This row set none, so it kept the CSS default of 0 and sorted ahead of
   everything -- which is the whole "it spawns over the hero" bug. Inserting it
   at the right place in the DOM changed nothing and could never have: a DOM
   check said it sat after the watchlist while the screenshot showed it on top of
   the hero, which is exactly what flex order does.

   Take the watchlist row's own order + 1 rather than hard-coding 5, so it keeps
   following the watchlist if those numbers are ever re-tuned in the Home Screen
   Sections config. Ties break on DOM order, and the insert below puts this row
   after the watchlist anyway, so a collision still lands the right way round. */
var ord=5;
if(wl){
try{var o=parseInt(getComputedStyle(wl).order,10);if(!isNaN(o))ord=o+1;}catch(e){}
}
if(sec.style.order!==String(ord))sec.style.order=String(ord);

if(!anchor){
if(sec.parentNode!==secs)secs.appendChild(sec);
return;
}
if(anchor.nextElementSibling===sec)return;   /* already right: touch nothing */
var host=anchor.parentNode||secs;
if(anchor.nextSibling)host.insertBefore(sec,anchor.nextSibling);
else host.appendChild(sec);
}
function sfLeavingRow(){
if((location.hash||'').indexOf('#/home')!==0)return;
var page=null,pages=document.querySelectorAll('#indexPage'),i;
for(i=0;i<pages.length;i++){
if(pages[i].offsetParent!==null&&pages[i].getBoundingClientRect().height>0){page=pages[i];break;}
}
if(!page)return;
var secs=page.querySelector('.sections.homeSectionsContainer');
if(!secs)return;
var ac=window.ApiClient;if(!ac||!ac.getImageUrl)return;
if(sfLeaveData===null){
if(sfLeaveBusy)return;
sfLeaveBusy=true;
/* same-origin from Jellyfin's own web root, exactly like readalong/<id>.json --
   no bridge round-trip, and it is a static file so it costs the N100 nothing */
fetch('leaving/soon.json',{cache:'no-cache'}).then(function(r){return r.ok?r.json():{items:[]};})
.then(function(d){sfLeaveData=(d&&d.items)||[];sfLeaveBusy=false;})
.catch(function(){sfLeaveData=[];sfLeaveBusy=false;});
return;
}
sfLeaveLoadFav();
var old=secs.querySelector('.sf-leavingrow');
if(!sfLeaveData.length){if(old&&old.parentNode)old.parentNode.removeChild(old);return;}
/* sf-leave-reposition: the watchlist row renders from its own async fetch, so
   on any given tick it may not exist yet. Placing once and never looking again
   made the order a coin toss -- whichever row happened to render first won.
   Re-place every tick instead; sfPlaceLeaving is a no-op once it is right. */
if(old){sfPlaceLeaving(secs,old);return;}
var T=function(x){try{return window.sfTr?window.sfTr(x):x;}catch(e){return x;}};
var sec=document.createElement('div');
sec.className='verticalSection sf-mylist sf-leavingrow';
var head=document.createElement('div');
head.className='sectionTitleContainer sectionTitleContainer-cards';
var h2=document.createElement('h2');
h2.className='sectionTitle sectionTitle-cards';
h2.textContent=T('Leaving Soon');
head.appendChild(h2);
/* The instruction belongs to the ROW, not to each poster: repeating
   "Favorite it to keep" under all ten cards was ten copies of one sentence and
   it crowded the titles. Once, beside the heading, is enough. */
var hint=document.createElement('span');
hint.className='sf-leave-hint';
/* The same glyph as the button on every poster, so the sentence and the control
   are visibly the same thing. Material Icons, not a unicode emoji: an emoji
   renders in the platform's own colour and would be the one bit of the row that
   ignores the theme. */
hint.innerHTML='<span class="material-icons sf-leave-hint-i" aria-hidden="true">favorite</span>';
/* sfTr returns the KEY for en-US, so a '__' key leaks verbatim -- the same
   trap that once printed "26__leavedays" on the badge. Fall back explicitly. */
var tk=T('__tokeep'); if(tk==='__tokeep')tk='to keep';
hint.appendChild(document.createTextNode(tk));
head.appendChild(hint);
sec.appendChild(head);
var row=document.createElement('div');
row.className='sf-ml-row';
var j,it,card,post,ttl,sub,url,bdg;
for(j=0;j<sfLeaveData.length&&j<24;j++){
it=sfLeaveData[j];
/* Already favourited: it is safe, so drop it from the row entirely rather than
   leaving a card that says "Saved". The engine clears the mark on its next run
   and tops the list back up; until then the row is simply one shorter, which is
   honest -- it lists what is still at risk. */
if(sfLeaveFav[it.id])continue;
card=document.createElement('div');
card.className='sf-ml-card';
card.setAttribute('data-id',it.id);
post=document.createElement('div');
post.className='sf-ml-poster';
try{url=ac.getImageUrl(it.id,{type:'Primary',maxWidth:400});}catch(e){url='';}
if(url)post.style.backgroundImage='url("'+url+'")';
bdg=document.createElement('div');
bdg.className='sf-leave-badge';
/* sfTr returns the KEY unchanged for en-US, so a '__' suffix key leaks
   verbatim -- the badge read "26__leavedays". Fall back explicitly. */
var suf=T('__leavedays'); if(suf==='__leavedays')suf=' days';
var td=T('today'); if(td==='today')td='today';
bdg.textContent=(it.days<=0?td:(it.days+suf));
post.appendChild(bdg);
(function(item,cardEl,badgeEl){
var fav=document.createElement('button');
fav.type='button';
fav.className='sf-leave-fav';
fav.setAttribute('aria-label',T('Favorite it to keep'));
fav.setAttribute('title',T('Favorite it to keep'));
var kept=T('Kept'); if(kept==='Kept')kept='Saved';
fav.setAttribute('data-id',item.id);
fav.setAttribute('data-kept',kept);
fav.setAttribute('data-days',(item.days<=0?td:(item.days+suf)));
function paint(){sfLeavePaintOne(fav);}
fav.addEventListener('click',function(e){
/* the whole card navigates to the detail page, so this must not bubble */
e.preventDefault();e.stopPropagation();
var ac=window.ApiClient;
if(!ac||!ac.getCurrentUserId)return;
var on=!sfLeaveFav[item.id];
/* optimistic: saving something from deletion has to feel instant. If the
   write fails the heart flips back rather than lying about being safe. */
sfLeaveFav[item.id]=on; paint();
try{
fetch(ac.getUrl('Users/'+ac.getCurrentUserId()+'/FavoriteItems/'+item.id),
{method:on?'POST':'DELETE',headers:{'X-Emby-Token':ac.accessToken()}})
.then(function(r){if(!r||!r.ok){sfLeaveFav[item.id]=!on;paint();}})
.catch(function(){sfLeaveFav[item.id]=!on;paint();});
}catch(err){sfLeaveFav[item.id]=!on;paint();}
});
post.appendChild(fav);
paint();          /* in the DOM now, so the icon actually lands */
})(it,card,bdg);
card.appendChild(post);
ttl=document.createElement('div');
ttl.className='sf-ml-title';
ttl.textContent=it.name||'';
card.appendChild(ttl);
(function(id){card.addEventListener('click',function(e){
e.preventDefault();e.stopPropagation();
location.hash='#/details?id='+id;
});})(it.id);
row.appendChild(card);
}
sec.appendChild(row);
sfPlaceLeaving(secs,sec);
}
function sfAudiobookRow(){
if((location.hash||'').indexOf('#/home')!==0)return;
var page=null,pages=document.querySelectorAll('#indexPage'),i;
for(i=0;i<pages.length;i++){
if(pages[i].offsetParent!==null&&pages[i].getBoundingClientRect().height>0){page=pages[i];break;}
}
if(!page)return;
var secs=page.querySelector('.sections.homeSectionsContainer');
if(!secs)return;
var ac=window.ApiClient;
if(!ac||!ac.getJSON||!ac.getCurrentUserId)return;
var uid=ac.getCurrentUserId();
if(!uid)return;
if(sfAbUid!==uid){sfAbUid=uid;sfAbItems=null;sfAbBusy=false;}
if(sfAbItems===null){
if(sfAbBusy)return;
sfAbBusy=true;
/* RECENTLY ADDED books. Part-finished ones are no longer shown here -- they
   belong with the other things you are midway through, so they are merged into
   Continue Watching instead (see sf-cw-books). */
ac.getJSON(ac.getUrl('Users/'+uid+'/Items',{IncludeItemTypes:'AudioBook',
Recursive:true,Limit:20,SortBy:'DateCreated',SortOrder:'Descending'}))
.then(function(r){sfAbItems=(r&&r.Items)||[];sfAbKind='new';sfAbBusy=false;})
.catch(function(){sfAbItems=[];sfAbBusy=false;});
return;
}
if(!sfAbItems.length)return;
if(secs.querySelector('.sf-audiobookrow'))return;
var sec=document.createElement('div');
sec.className='verticalSection sf-mylist sf-audiobookrow';
var head=document.createElement('div');
head.className='sectionTitleContainer sectionTitleContainer-cards';
var h2=document.createElement('h2');
h2.className='sectionTitle sectionTitle-cards';
h2.textContent='Audiobooks';
head.appendChild(h2);
sec.appendChild(head);
var row=document.createElement('div');
row.className='sf-ml-row';
var j,it,card,post,ttl,sub,url,pct,bar,fill,ud;
for(j=0;j<sfAbItems.length;j++){
it=sfAbItems[j];
card=document.createElement('div');
card.className='sf-ml-card';
card.setAttribute('data-id',it.Id);
/* Marked for sf-abcard (time-left, series badge, title link). A private
   attribute rather than data-type="AudioBook": Jellyfin's click delegation keys
   off data-type, and these cards carry their own handler. */
card.setAttribute('data-sf-abcard','1');
post=document.createElement('div');
post.className='sf-ml-poster';
try{url=ac.getImageUrl(it.Id,{type:'Primary',maxWidth:400,
tag:(it.ImageTags||{}).Primary});}catch(e){url='';}
if(url)post.style.backgroundImage='url("'+url+'")';
/* how far in she is -- the reason this row exists */
ud=it.UserData||{};
/* sf-resume-pos: the row already reads UserData to draw the progress bar; carry
   the position onto the card so the tap handlers can resume to it. */
card.setAttribute('data-positionticks',ud.PlaybackPositionTicks||'');
pct=ud.PlayedPercentage||0;
if(pct>0&&pct<99){
bar=document.createElement('div');bar.className='sf-ml-prog';
fill=document.createElement('div');fill.className='sf-ml-progfill';
fill.style.width=Math.max(2,Math.min(100,pct))+'%';
bar.appendChild(fill);post.appendChild(bar);
}
ttl=document.createElement('div');
ttl.className='cardText cardText-first';
ttl.textContent=it.Name||'';
sub=document.createElement('div');
sub.className='cardText cardText-secondary';
sub.textContent=(it.AlbumArtist||it.Artists&&it.Artists[0]||'');
card.appendChild(post);card.appendChild(ttl);
if(sub.textContent)card.appendChild(sub);
/* sf-abrow-title (2026-08-21). The admin: "when we press the audiobook title for the
   audiobook row on home we should be taken to the audiobook page."
   So the row now reads the way a shelf should: the ARTWORK plays, the TITLE
   opens the book. Before this the whole card played, and there was no way to
   reach the page (with its chapters, synopsis and read-along) except the ⋮.
   stopPropagation, or the card's own play handler fires underneath. */
(function(bookId){
var openPage=function(e){
e.preventDefault();e.stopPropagation();
sfAbGo(bookId);
};
ttl.classList.add('sf-ab-titlelink');
ttl.addEventListener('click',openPage);
if(sub.textContent){
sub.classList.add('sf-ab-titlelink');
sub.addEventListener('click',openPage);
}
})(it.Id);
/* Same as the music row: the card plays. The ⋮ opens the book if that is what
   was wanted. resume, not play, so a part-finished book carries on. */
card.addEventListener('click',function(){
var id=this.getAttribute('data-id');
/* sf-retap: never restart what is already playing */
if(sfRetapGuard(id))return;
try{sfOptiFromCard(this);}catch(e){}
var pt=this.getAttribute('data-positionticks')||'';
if(sfPlayItemViaProxy(id,'AudioBook','Audio',false,pt?'resume':'play',pt))return;
location.hash='#/details?id='+id;});
sfAddCardOverlay(card,it.Id,it.Type||'AudioBook','Audio',false,'resume');
row.appendChild(card);
}
sec.appendChild(row);
/* 1000 = one above music's 999, so it is always the row directly below it.
   Absolute, for the same reason music's is (see sf-music-row). */
sec.style.order='1000';
secs.appendChild(sec);
}
function sfMusicRow(){
/* Wait for the hero. Measured on a cold home load: this fired at ~1385ms and
   took 1380ms, landing on the exact instant Media Bar was querying its own
   items -- two heavy queries hitting a NAS that answers them serially, so the
   artwork filling the screen finished behind a row nobody had scrolled to yet.
   __sfHeroPainted is set by the first backdrop's load event and, failing that,
   by a 2.5s timer in sf-hero-srccap, so this can defer but never strand. */
if(!window.__sfHeroPainted&&(location.hash||'').indexOf('#/home')===0)return;
var page=document.querySelector('#indexPage:not(.hide)');
if(!page)return;
var secs=page.querySelector('.sections.homeSectionsContainer');
if(!secs)return;
var ac=window.ApiClient;
if(!ac||!ac.getCurrentUserId)return;
var uid=ac.getCurrentUserId();
if(!uid)return;
if(sfMrUid!==uid){sfMrUid=uid;sfMrItems=null;sfMrBusy=false;}
if(sfMrItems===null){
if(sfMrBusy)return;
sfMrBusy=true;
/* "Jump Back In" -- the albums actually being listened to, most recent first,
   which is the Spotify/Apple row this was asked to become. Recently Added
   answers "what did the SERVER get", which is a librarian's question, not a
   listener's; on a library that rarely changes it is also a row that never
   moves.
   Jellyfin cannot filter ALBUMS by IsPlayed -- it only ever marks TRACKS played
   (see jellyfin-music-suggestions-home) -- so this reads recently played AUDIO
   and folds it up to distinct albums. Same source the Suggestions page's
   featured hero uses, so the two always agree.
   Everything the card needs is already on the audio item (AlbumId, Album,
   AlbumArtist), so folding up costs no second request. */
ac.getJSON(ac.getUrl('Users/'+uid+'/Items',{IncludeItemTypes:'Audio',Recursive:true,
SortBy:'DatePlayed',SortOrder:'Descending',Limit:100,Filters:'IsPlayed',Fields:'AlbumId'}))
.then(function(r){
var t=(r&&r.Items)||[],seen={},out=[],i,x;
for(i=0;i<t.length;i++){
x=t[i];
if(!x.AlbumId||seen[x.AlbumId])continue;
seen[x.AlbumId]=1;
out.push({Id:x.AlbumId,Name:x.Album||x.Name||'',AlbumArtist:x.AlbumArtist||''});
if(out.length>=20)break;
}
if(out.length>=4){sfMrItems=out;sfMrKind='played';sfMrBusy=false;return;}
/* A listener with no history yet -- a new user, or a fresh server -- would get
   an empty or near-empty row, which is worse than the row this replaced. Fall
   back to what is new in the library and say so in the heading. */
return ac.getJSON(ac.getUrl('Users/'+uid+'/Items',{IncludeItemTypes:'MusicAlbum',
Recursive:true,Limit:20,SortBy:'DateCreated',SortOrder:'Descending'}))
.then(function(r2){sfMrItems=(r2&&r2.Items)||[];sfMrKind='new';sfMrBusy=false;});
})
.catch(function(){sfMrItems=[];sfMrBusy=false;});
return;
}
if(!sfMrItems.length)return;
if(secs.querySelector('.sf-musicrow'))return;
var sec=document.createElement('div');
sec.className='verticalSection sf-mylist sf-musicrow';
var head=document.createElement('div');
head.className='sectionTitleContainer sectionTitleContainer-cards';
var h2=document.createElement('h2');
h2.className='sectionTitle sectionTitle-cards';
h2.textContent=(sfMrKind==='played')?'Music':'Recently Added Music';
head.appendChild(h2);
sec.appendChild(head);
var row=document.createElement('div');
row.className='sf-ml-row';
var i,it,card,post,ttl,sub,url;
for(i=0;i<sfMrItems.length;i++){
it=sfMrItems[i];
card=document.createElement('div');
card.className='sf-ml-card';
card.setAttribute('data-id',it.Id);
post=document.createElement('div');
/* sf-musicrow-play: play an album through Jellyfin's OWN handler.
   Jellyfin binds click delegation per container, so an itemAction element inside
   our row does nothing. Borrow a bound container (the home page's
   .itemsContainer), drop in a hidden proxy card wearing the delegated-action
   contract, click it, then remove it -- the same technique sf-ls-inplace uses
   for live channels. Returns false if it could not, so the caller can fall back
   to navigation rather than leaving a dead click. */
post.className='sf-ml-poster sf-ml-square';
try{url=ac.getImageUrl(it.Id,{type:'Primary',maxWidth:400,
tag:(it.ImageTags||{}).Primary});}catch(e){url='';}
if(url)post.style.backgroundImage='url("'+url+'")';
ttl=document.createElement('div');
ttl.className='cardText cardText-first';
ttl.textContent=it.Name||'';
sub=document.createElement('div');
sub.className='cardText cardText-secondary';
sub.textContent=it.AlbumArtist||it.ArtistItems&&it.ArtistItems[0]&&it.ArtistItems[0].Name||'';
card.appendChild(post);card.appendChild(ttl);
if(sub.textContent)card.appendChild(sub);
card.setAttribute('data-type',it.Type||'MusicAlbum');
/* "Jump Back In" means resume the album. Only fall back to the detail page if
   playback could not be started, so the click is never dead. */
card.addEventListener('click',function(){
var id=this.getAttribute('data-id');
if(sfPlayItemViaProxy(id,this.getAttribute('data-type'),'Audio',true,'play'))return;
location.hash='#/details?id='+id;});
sfAddCardOverlay(card,it.Id,it.Type||'MusicAlbum','Audio',true,'play');
row.appendChild(card);
}
sec.appendChild(row);
/* LAST on the page, by the admin's call. An absolute order rather than "one more
   than the row above": Home Screen Sections writes its own OrderIndex on every
   row and can add one at any index, so a relative value can be leapfrogged
   while 999 cannot. The appendChild matters too -- equal orders fall back to
   document position. */
sec.style.order='999';
secs.appendChild(sec);
}
/* sf-music-feature: the featured hero and the Your Top Artists row.

   BOTH are derived from one query -- the last 100 played tracks -- because the
   obvious endpoints do not work here:
     * albums filtered by IsPlayed return NOTHING; Jellyfin does not mark an
       album played, only its tracks.
     * /Artists sorted by PlayCount returns PlayCount 0 for every artist, and the
       list is full of credit permutations ("Taylor Swift featuring Keith Urban",
       "Tyler, The Creator feat. Alice Smith, Leon Ware and ...") with no images.
   Tallying AlbumArtist across real plays gives something true and personal
   instead: measured Ed Sheeran 24, Taylor Swift 18, Coldplay 7, BTS 5.
   Artist records (for ids and images) come from /Artists/AlbumArtists, matched
   by name -- that endpoint returns the clean canonical artists, not the credits.

   The hero's Play button carries Jellyfin's OWN delegated-action contract --
   class itemAction plus data-action / data-id / data-serverid, exactly what its
   card overlay buttons use -- so playback runs through Jellyfin's real handler.
   There is no AMD loader on this build (window.require is undefined), so calling
   playbackManager directly is not an option; wearing the attributes is. */
var sfNewAlb=null, sfNewAlbBusy=false;
var sfMfData=null, sfMfBusy=false, sfMfUid=null;
/* sf-hero-first: the featured panel reads exactly ONE row -- the most recently
   played track -- but it used to wait on the same Promise.all that feeds the
   artist tally and the unheard shelf. Timed on a phone 2026-08-27:
   Artists/AlbumArtists answered in 349ms, the 500-played-track query took
   2605ms, and Promise.all made the hero wait for both -- so it appeared at
   ~4.9s having been able to paint at ~2.6s. Its own Limit=1 query is cheap.
   sfHeroData: null = not asked yet, false = nothing played, else the track.
   sfHeroAmb: 0 until the accent has SETTLED (extracted, failed, or timed out).
   The pane reveal waits on that, which is what makes the panel arrive already
   coloured instead of recolouring in front of you. */
var sfHeroData=null, sfHeroBusy=false, sfHeroAmb=0;
/* sf-cap-reveal: don't show the player until its controls have finished
   assembling. Measured from a cold load: the bar becomes visible with 7 buttons,
   gains an 8th ~200ms later, and settles at 10 (lyrics, cast) at ~370ms as the
   capsule wiring runs on its tick. The container is right from the first frame --
   634px wide, 24px radius -- so what flashes is the CONTENTS rearranging in view.

   Held invisible for one tick's worth of time, then faded in, so the first thing
   seen is the finished capsule. The reveal is scheduled with a timeout the moment
   the bar is first seen, NOT gated on the wiring reporting done -- if any part of
   that wiring ever fails, a gated reveal would hide the player permanently, which
   is far worse than the flash it fixes. */
/* sf-playlist-new: let a listener actually make a playlist.

   Measured before building this: ZERO playlists on the server, and the Playlists
   tab renders zero cards and zero buttons -- a completely dead screen with no way
   in. The only route Jellyfin offers is a card's hover-only kebab menu, where
   "Add to playlist" sits SIXTH in a thirteen-item list, two rows above
   "Delete media". That is not a path anyone finds, and it is a dangerous
   neighbourhood for a casual listener.

   This puts a Create button on the empty tab and expands it into an inline
   composer -- name, Enter, done. Inline rather than a modal on purpose: it is one
   less layer, it cannot trap focus, and it matches the rest of the UI.

   POST /Playlists with MediaType Audio; the new playlist appears on the tab
   without a reload because Jellyfin re-renders the pane when it regains focus,
   and we nudge it by re-clicking the tab. */
/* sf-mix: start a Mix from any album or artist.

   Jellyfin calls this "Instant mix" and buries it 3rd in a card's hover-only
   kebab menu. It is the best thing in the music library -- an endless
   radio-style queue seeded from anything -- and nobody finds it. Verified: a mix
   seeded from Adele's "Hello" opened with Olly Murs, i.e. it genuinely branches
   out rather than replaying the same album.

   Triggering it needs Jellyfin's own menu, for the same reason the hero Play
   button does: the action handlers are bound to the item containers, so a
   synthetic control outside them is never heard. So this borrows a real card --
   clone one that is already inside an .itemsContainer, retarget the clone at our
   id/type, open its menu, click Instant mix, then remove the clone. Verified for
   MusicArtist as well as MusicAlbum (Ed Sheeran's menu opened correctly).

   Entirely driven by clicks on Jellyfin's own UI, so queue, reporting and device
   state all behave exactly as if the user had used the menu themselves. */
/* sf-visible-pane: `document.querySelector` returns the first match in DOCUMENT
   order, and Jellyfin keeps one cached view per URL -- a cached page holds on to
   its `.is-active` pane even while hidden. So on `#/music?tab=1` reached from
   home, the first `.pageTabContent.is-active` in the document is home's hidden
   `#homeTab` (data-index 0, height 0), NOT the music pane.

   Measured live on that exact route:
       #homeTab        data-index 0  visible false  height 0     <- what won
       #suggestionsTab data-index 1  visible true   height 1922  <- what we want

   Every music function guards on `data-index === '1'`, so all of them bailed and
   the entire Suggestions revamp silently failed to build -- no greeting, no
   featured hero, no Top Artists, and the duplicate "Albums" heading back. It
   looked like the page had reverted; nothing had, the guard was just reading the
   wrong element.

   offsetParent is null for anything inside a `display:none` ancestor, which is
   exactly how Jellyfin hides a cached view, so it is the cheap correct test.
   See jellyfin-duplicate-page-instances -- duplicate ids here are NORMAL and the
   rule is always to resolve the VISIBLE instance. */
function sfActivePane(){
var n=document.querySelectorAll('.tabContent.is-active, .pageTabContent.is-active'),i;
for(i=0;i<n.length;i++)if(n[i].offsetParent!==null)return n[i];
return null;
}
function sfMix(id,type){
/* sf-mix-direct (2026-08-20). REPLACES a hack that cloned a card, clicked its
   kebab menu, then POLLED the action sheet for up to 2.4s looking for the
   "Instant mix" row and clicked it.

   That approach failed in three different ways and was never going to be
   reliable: it matched the option by its ENGLISH label (dead in zh-CN, where the
   row reads "\u901f\u6210\u5408\u8f91"), it needed a real card on the page to clone as a
   model, and it depended on an action sheet rendering inside a fixed 2.4s budget
   on whatever device you happened to be holding.

   Jellyfin's own delegated card handler accepts data-action="instantmix"
   directly -- verified: setting it on a proxy card fires
   GET /Items/{id}/InstantMix with no menu involved at all. sfPlayItemViaProxy
   already builds exactly that proxy, sets the action on its button, and carries
   the scroll-position guards. So this is now one call on the same path the
   music and audiobook rows already use, with no DOM scraping, no polling and
   nothing language-dependent left in it. */
if(!id)return false;
if(sfPlayItemViaProxy(id,type||'MusicAlbum','Audio',true,'instantmix'))return true;
/* nothing we can do silently -- give them the page where Jellyfin's own
   Instant mix lives rather than appearing to ignore the tap */
location.hash='#/details?id='+id;
return false;
}
'''

# _LS_09 (orig L5789-6536) -- sf-mus-playlists, sf-mus-reveal, sf-hero-first
_LS_09 = r'''/* sf-mus-playlists: her own playlists, on the page she lands on.
   Hidden entirely when there are none -- an empty shelf is worse than no shelf,
   and a new listener has nothing here until they make something. */
var sfPlData=null, sfPlBusy=false, sfPlUid=null;
function sfPlaylistRow(){
if(location.hash.indexOf('#/music')!==0)return;
var pane=sfActivePane();
if(!pane||pane.getAttribute('data-index')!=='1')return;
var ac=window.ApiClient;
if(!ac||!ac.getCurrentUserId)return;
var uid=ac.getCurrentUserId();
if(!uid)return;
if(sfPlUid!==uid){sfPlUid=uid;sfPlData=null;sfPlBusy=false;}
if(sfPlData===null){
if(sfPlBusy)return;
sfPlBusy=true;
ac.getJSON(ac.getUrl('Users/'+uid+'/Items',{IncludeItemTypes:'Playlist',Recursive:true,
Limit:24,SortBy:'DateCreated',SortOrder:'Descending',Fields:'ChildCount'}))
.then(function(r){sfPlData=(r&&r.Items)||[];sfPlBusy=false;})
.catch(function(){sfPlData=[];sfPlBusy=false;});
return;
}
/* The generated mixes ARE real playlists, so they showed up here too and the
   page carried each of them twice -- "Made for you" and "Your Playlists" side by
   side. Wait for the mix list, then leave those out: this row is for playlists
   the household made, not ones we generated. */
sfMixLoad();
if(sfMixData===null)return;
var sfMixIds={},_mi;
for(_mi=0;_mi<sfMixData.length;_mi++){
if(sfMixData[_mi].playlistId)sfMixIds[String(sfMixData[_mi].playlistId)]=1;
}
var sfPlOwn=[],_pi;
for(_pi=0;_pi<sfPlData.length;_pi++){
/* '__' prefixes an internal playlist (the queue scratch pad) -- never a
   playlist a person made, so it must not appear in their list. */
if(!sfMixIds[String(sfPlData[_pi].Id)]&&String(sfPlData[_pi].Name||'').indexOf('__')!==0)
sfPlOwn.push(sfPlData[_pi]);
}
if(!sfPlOwn.length)return;
if(pane.querySelector('.sf-mus-playlists'))return;
var sec=document.createElement('div');
sec.className='verticalSection sf-mylist sf-mus-playlists';
sec.style.order='4';
var head=document.createElement('div');
head.className='sectionTitleContainer sectionTitleContainer-cards';
var h2=document.createElement('h2');
h2.className='sectionTitle sectionTitle-cards';
h2.textContent='Your Playlists';
head.appendChild(h2);
sec.appendChild(head);
var row=document.createElement('div');
row.className='sf-ml-row';
var i,p,c,art,t,s,u;
for(i=0;i<sfPlOwn.length;i++){
p=sfPlOwn[i];
c=document.createElement('div');
c.className='sf-ml-card sf-mus-playlist';
c.setAttribute('data-id',p.Id);
art=document.createElement('div');
art.className='sf-ml-poster sf-ml-square';
u='';
try{u=ac.getImageUrl(p.Id,{type:'Primary',maxWidth:400,tag:(p.ImageTags||{}).Primary});}catch(e){}
if(u&&(p.ImageTags||{}).Primary)art.style.backgroundImage='url("'+u+'")';
else art.className+=' sf-mus-playlist-empty';
t=document.createElement('div');
t.className='cardText cardText-first';
t.textContent=p.Name||'';
s=document.createElement('div');
s.className='cardText cardText-secondary';
s.textContent=(p.ChildCount||0)+((p.ChildCount===1)?' track':' tracks');
c.appendChild(art);c.appendChild(t);c.appendChild(s);
c.addEventListener('click',function(){
location.hash='#/details?id='+this.getAttribute('data-id');});
row.appendChild(c);
}
sec.appendChild(row);
pane.appendChild(sec);
}
function sfPlaylistNew(){
if(location.hash.indexOf('#/music')!==0)return;
var pane=sfActivePane();
if(!pane||pane.getAttribute('data-index')!=='4')return;
if(pane.querySelector('.sf-plnew'))return;
var ac=window.ApiClient;
if(!ac||!ac.getCurrentUserId)return;
var wrap=document.createElement('div');
wrap.className='sf-plnew';
var btn=document.createElement('button');
btn.className='sf-plnew-btn';
btn.innerHTML='<span class="material-icons" aria-hidden="true">add</span>';
btn.appendChild(document.createTextNode('New Playlist'));
var form=document.createElement('div');
form.className='sf-plnew-form';
var input=document.createElement('input');
input.className='sf-plnew-input';
input.type='text';
input.placeholder='Playlist name';
input.setAttribute('maxlength','80');
var save=document.createElement('button');
save.className='sf-plnew-save';
save.textContent='Create';
var cancel=document.createElement('button');
cancel.className='sf-plnew-cancel';
cancel.textContent='Cancel';
var msg=document.createElement('div');
msg.className='sf-plnew-msg';
form.appendChild(input);form.appendChild(save);form.appendChild(cancel);
wrap.appendChild(btn);wrap.appendChild(form);wrap.appendChild(msg);
pane.insertBefore(wrap,pane.firstChild);

function open(){wrap.classList.add('sf-plnew-open');input.value='';msg.textContent='';
setTimeout(function(){input.focus();},30);}
function close(){wrap.classList.remove('sf-plnew-open');msg.textContent='';}
btn.addEventListener('click',open);
cancel.addEventListener('click',close);
input.addEventListener('keydown',function(e){
if(e.key==='Enter'){e.preventDefault();create();}
else if(e.key==='Escape'){close();}});
save.addEventListener('click',create);

function create(){
var name=(input.value||'').trim();
if(!name){msg.textContent='Give it a name first.';return;}
save.disabled=true;msg.textContent='Creating...';
ac.ajax({type:'POST',
url:ac.getUrl('Playlists',{Name:name,UserId:ac.getCurrentUserId(),MediaType:'Audio'}),
dataType:'json'})
.then(function(){
msg.textContent='Created "'+name+'". Add songs from any track\u2019s menu.';
save.disabled=false;
input.value='';
/* Re-render the tab so the new playlist appears without a reload. Clicking the
   ALREADY-ACTIVE tab does nothing (verified: the list stayed empty until a full
   reload), so this leaves and returns -- Jellyfin re-queries on entering a tab. */
setTimeout(function(){
var away=document.querySelector('.tabs-viewmenubar .emby-tab-button[data-index="1"]');
var back=document.querySelector('.tabs-viewmenubar .emby-tab-button[data-index="4"]');
if(away&&back){away.click();setTimeout(function(){back.click();},450);}
},700);
})
.catch(function(){msg.textContent='Could not create it. Try a different name.';
save.disabled=false;});
}
}
function sfCapReveal(){
var bar=document.querySelector('.nowPlayingBar');
if(!bar||bar.classList.contains('sf-cap-ready'))return;
if(bar.getBoundingClientRect().height===0)return;
if(bar.getAttribute('data-sf-cap-seen'))return;
bar.setAttribute('data-sf-cap-seen','1');
setTimeout(function(){bar.classList.add('sf-cap-ready');},420);
}
/* sf-mus-reveal: hold the Suggestions pane until it is actually built.

   The CSS hides it by DEFAULT (see the sf-mus-reveal branding block) rather than
   having JS add a hiding class, because the 400ms tick cannot beat the pane
   painting -- measured, the pane is visible at 101ms. Hiding from first paint
   and revealing here is the only ordering that has no flash in it.

   Ready means the featured/artists fetch has SETTLED, not that it returned
   anything: a listener with no play history gets `{hero:null,artists:[]}` and
   must still see the page. The greeting is the marker that sfMusicHome has run
   and therefore that the section order has been applied.

   The CSS carries a 5s failsafe reveal, so a thrown error or a missing
   ApiClient can never leave a permanently blank page. */
function sfMusReveal(){
if(location.hash.indexOf('#/music')!==0)return;
var pane=sfActivePane();
if(!pane||pane.getAttribute('data-index')!=='1')return;
if(pane.getAttribute('data-sf-ready'))return;
/* sf-hero-first: gated on the HERO stage, not on the 2.6s row query. The rows
   below the fold (top artists, unheard, new albums) may still be in flight --
   they mount at orders 4-6, under the hero and the mixes row, so their arrival
   moves nothing that is on screen. */
if(sfHeroData===null)return;                    /* hero query still in flight */
if(!sfHeroAmb)return;                           /* accent not settled -- would recolour in view */
if(!pane.querySelector('.sf-mus-greet'))return; /* ordering not applied yet */
pane.setAttribute('data-sf-ready','1');
/* sf-hero-oneshot: only now is it safe to let the hero animate its colour --
   everything on screen is final, so any later change is a real retarget. */
setTimeout(function(){
var h=pane.querySelector('.sf-mus-hero');
if(h)h.classList.add('sf-hero-tx');
},600);
}
/* sf-hero-first: lifted out of sfMusicFeature verbatim so it can be called the
   moment the Limit=1 hero query returns, instead of only after the 2.6s
   artist/unheard query it never read from. */
function sfBuildMusHero(pane,ac,hv){
var art='';
try{art=ac.getImageUrl(hv.AlbumId,{type:'Primary',maxWidth:700});}catch(e){}
var _slot=pane.querySelector('.sf-mus-heroslot');
if(_slot&&_slot.parentNode)_slot.parentNode.removeChild(_slot);
var hero=document.createElement('div');
hero.className='sf-mus-hero';
hero.style.order='2';
/* sf-mus-pagebg: sfPageBg reads the featured cover from here. An attribute
   rather than the .sf-mus-hero-bg element's style, because that element is
   display:none now that the panel has no box of its own. */
if(art)hero.setAttribute('data-sf-art',art);
/* sf-hero-oneshot: .sf-hero-tx is armed by sfMusReveal, NOT here. A timer from
   mount was the first attempt and it was wrong: the accent read is a network
   fetch of the cover and can outlast any fixed delay, so at 700ms the fade was
   already armed when the colour finally landed, and the Play button was caught
   mid-way at rgb(250,234,228) on its way to rgb(214,78,21) -- a slower version
   of the exact flicker being fixed. Arming it after the pane has revealed is
   the only anchor that is guaranteed to be later than the colour, because the
   reveal itself waits on sfHeroAmb. */
var bg=document.createElement('div');
bg.className='sf-mus-hero-bg';
if(art)bg.style.backgroundImage='url("'+art+'")';
var inner=document.createElement('div');
inner.className='sf-mus-hero-inner';
var cover=document.createElement('div');
cover.className='sf-mus-hero-art';
if(art)cover.style.backgroundImage='url("'+art+'")';
var meta=document.createElement('div');
meta.className='sf-mus-hero-meta';
var kick=document.createElement('div');
kick.className='sf-mus-hero-kicker';
kick.textContent='Last played';
var ttl=document.createElement('h2');
ttl.className='sf-mus-hero-title';
ttl.textContent=hv.Album||hv.Name||'';
var who=document.createElement('div');
who.className='sf-mus-hero-artist';
who.textContent=hv.AlbumArtist||'';
/* Playback goes through one of Jellyfin's OWN card buttons.
   Wearing the delegated-action attributes is not enough -- tried both
   data-action on the button with data-id on it, and the real card's shape with
   the item data on an ancestor; neither played, because the handler is bound to
   the item containers rather than to the document, so an element outside them
   never receives the event. Clicking the album's actual card button DOES work
   (verified: audio element created, now-playing bar up, playing at 2s).
   So: find that card on the page and click its play control. If the album is not
   on screen -- it usually is, it was the last thing played -- fall back to its
   detail page, where Jellyfin's own Play button lives. */
var play=document.createElement('button');
play.className='sf-mus-hero-play';
play.setAttribute('data-album',hv.AlbumId);
/* sf-hero-play-direct (2026-08-20). This used to hunt for the album's OWN card
   somewhere on the page and click its play button, falling back to the detail
   page if it could not find one. The fallback was the normal case, not the
   exception: the featured album is the last thing you PLAYED, which is very
   often not in any of the shelves currently rendered -- measured live, 0 cards
   matched the featured album id while 125 other cards were on the page. So the
   big Play button quietly navigated to the album page instead of playing, which
   is exactly the "Play doesn't play, it takes me to the song page" report.
   sfPlayItemViaProxy needs nothing to be on screen. Detail page only if even
   that fails. */
play.addEventListener('click',function(){
var id=this.getAttribute('data-album');
if(!id)return;
/* sf-optibar: the featured card already holds all three fields */
try{sfOptiShow(hv.Album||hv.Name||'', hv.AlbumArtist||'', art||'');}catch(e){}
if(sfPlayItemViaProxy(id,'MusicAlbum','Audio',true,'play'))return;
location.hash='#/details?id='+id;
});
play.innerHTML='<span class="material-icons" aria-hidden="true">play_arrow</span>';
play.appendChild(document.createTextNode((window.sfTr?window.sfTr('Play'):'Play')));
/* "Mix", not "Instant mix" -- shorter reads cleaner next to Play, and the
   word does the same job. */
var mix=document.createElement('button');
mix.className='sf-mus-hero-mix';
mix.setAttribute('data-album',hv.AlbumId);
mix.innerHTML='<span class="material-icons" aria-hidden="true">shuffle</span>';
mix.appendChild(document.createTextNode((window.sfTr?window.sfTr('Mix'):'Mix')));
mix.addEventListener('click',function(){
try{sfOptiShow(hv.Album||hv.Name||'', 'Mix', art||'');}catch(e){}
sfMix(this.getAttribute('data-album'),'MusicAlbum');});
var acts=document.createElement('div');
acts.className='sf-mus-hero-actions';
acts.appendChild(play);acts.appendChild(mix);
meta.appendChild(kick);meta.appendChild(ttl);meta.appendChild(who);meta.appendChild(acts);
inner.appendChild(cover);inner.appendChild(meta);
hero.appendChild(bg);hero.appendChild(inner);
pane.appendChild(hero);
pane.appendChild(hero);
}

function sfMusicFeature(){
/* Wait for the hero. Measured on a cold home load: this fired at ~1385ms and
   took 1380ms, landing on the exact instant Media Bar was querying its own
   items -- two heavy queries hitting a NAS that answers them serially, so the
   artwork filling the screen finished behind a row nobody had scrolled to yet.
   __sfHeroPainted is set by the first backdrop's load event and, failing that,
   by a 2.5s timer in sf-hero-srccap, so this can defer but never strand. */
if(!window.__sfHeroPainted&&(location.hash||'').indexOf('#/home')===0)return;
if(location.hash.indexOf('#/music')!==0)return;
var pane=sfActivePane();
if(!pane||pane.getAttribute('data-index')!=='1')return;
var ac=window.ApiClient;
if(!ac||!ac.getCurrentUserId)return;
var uid=ac.getCurrentUserId();
if(!uid)return;
if(sfMfUid!==uid){sfMfUid=uid;sfMfData=null;sfMfBusy=false;sfHeroData=null;sfHeroBusy=false;sfHeroAmb=0;}
/* sf-heroslot (2026-08-21). The featured hero is built only once its query
   comes back -- measured at t=2814ms on a phone -- and it mounts at order 2,
   ABOVE the mixes row. So for the first ~2.8s every row below it sits 218px too
   high, and then jumps down.

   That is not cosmetic. Traced with a hit test at the moment of the tap: the
   mix card measured at y=249, the tap landed, and the card was at y=467 by the
   time it arrived -- elementFromPoint returned the bare page, not the card. Over
   10 cold loads, 5 taps were lost this way. It is also how a tap can land on the
   WRONG item, which is far worse than one that does nothing.

   Reserving the space up front costs nothing and removes the shift entirely.
   The slot carries the hero's own order so the sequence is right from frame one,
   and it is removed in the same statement that inserts the real hero. */
if(!pane.querySelector('.sf-mus-hero')&&!pane.querySelector('.sf-mus-heroslot')){
var slot=document.createElement('div');
slot.className='sf-mus-heroslot';
slot.style.order='2';
pane.appendChild(slot);
}
/* sf-hero-first: kicked off here rather than inside the Promise.all below, so
   the panel does not inherit the 2.6s the heavy query costs. */
if(sfHeroData===null&&!sfHeroBusy){
sfHeroBusy=true;
ac.getJSON(ac.getUrl('Users/'+uid+'/Items',{IncludeItemTypes:'Audio',Recursive:true,
SortBy:'DatePlayed',SortOrder:'Descending',Limit:1,Filters:'IsPlayed',Fields:'AlbumId'}))
.then(function(r){
sfHeroData=(((r&&r.Items)||[])[0])||false;
sfHeroBusy=false;
sfHeroPrime(ac);
try{sfMusicFeature();sfMusReveal();}catch(e){}})
.catch(function(){sfHeroData=false;sfHeroBusy=false;sfHeroAmb=1;
try{sfMusicFeature();sfMusReveal();}catch(e){}});
}
/* ---- featured hero (sf-hero-first: built off sfHeroData, so it no longer
   waits for the artist/unheard query below) ---- */
if(sfHeroData===false){
/* sf-heroslot: nothing to feature, so give the reserved space back rather than
   leaving a permanent hole. */
var _ns=pane.querySelector('.sf-mus-heroslot');
if(_ns&&_ns.parentNode)_ns.parentNode.removeChild(_ns);
}
if(sfHeroData&&sfHeroData.AlbumId&&!pane.querySelector('.sf-mus-hero')){
sfBuildMusHero(pane,ac,sfHeroData);
}
if(sfMfData===null){
if(sfMfBusy)return;
sfMfBusy=true;
/* Both at once. AlbumArtists is a plain lookup of every album artist -- it does
   not depend on the played-tracks result, it is only JOINED against it -- so
   chaining it put its 225ms on the critical path for nothing. */
Promise.all([
ac.getJSON(ac.getUrl('Users/'+uid+'/Items',{IncludeItemTypes:'Audio',Recursive:true,
SortBy:'DatePlayed',SortOrder:'Descending',Limit:500,Filters:'IsPlayed',Fields:'AlbumId'})),
ac.getJSON(ac.getUrl('Artists/AlbumArtists',{userId:uid,Recursive:true,Limit:500}))
])
.then(function(res){
var songs=res[0],ar=res[1];
var items=(songs&&songs.Items)||[],tally={},i,a;
for(i=0;i<items.length;i++){a=items[i].AlbumArtist;if(a)tally[a]=(tally[a]||0)+1;}
var names=Object.keys(tally).sort(function(x,y){return tally[y]-tally[x];}).slice(0,12);
var by={},list=(ar&&ar.Items)||[],j,out=[];
for(j=0;j<list.length;j++)by[list[j].Name]=list[j];
for(j=0;j<names.length;j++){
var rec=by[names[j]];
if(rec&&rec.Id)out.push({id:rec.Id,name:rec.Name,plays:tally[names[j]],
tag:(rec.ImageTags||{}).Primary});}
/* sf-mus-unheard: both halves of this already come back above -- the plays and
   the full album-artist list -- so the shelf costs NO extra request. An artist
   is "unheard" when no played track credits them.
   Limit was 100 and is now 500 for the same reason: this library has 134 played
   tracks in total, so 500 captures every one of them and makes both the tally
   and this set exact rather than "the last hundred plays".
   Measured 2026-08-20: 86 album artists, 33 with any play, 53 never played --
   and all 53 have artwork, which is what makes it a shelf worth looking at.
   This is the cold-start problem stated plainly: 5.5% of the library has ever
   been played, there are 0 favourites, and every album is under 30 days old, so
   nothing behavioural can rank it. */
var unheard=[],uj;
for(uj=0;uj<list.length;uj++){
var cand=list[uj];
if(!cand||!cand.Id)continue;
if(tally[cand.Name])continue;
if(!(cand.ImageTags||{}).Primary)continue;
unheard.push({id:cand.Id,name:cand.Name,tag:cand.ImageTags.Primary});
}
for(uj=unheard.length-1;uj>0;uj--){
var uk=Math.floor(Math.random()*(uj+1)),tmp=unheard[uj];
unheard[uj]=unheard[uk];unheard[uk]=tmp;
}
/* sf-song-radio: distinct recently played tracks, kept off the SAME response
   the tally above walks -- "start a station from this song" is the one radio
   affordance both Apple Music and Spotify put front and centre, and it needed
   no new call at all. Distinct by track id: playing an album straight through
   would otherwise fill the row with one record. */
var songs=[],sseen={},scap={},si2,sit,sart;
for(si2=0;si2<items.length&&songs.length<12;si2++){
sit=items[si2];
if(!sit||!sit.Id||sseen[sit.Id])continue;
/* Cap 2 per artist. Without it the row is just whatever album was played last:
   measured on the first build, 5 of 12 cards were Sabrina Carpenter because one
   record had been played straight through. build_mixes.py caps for the same
   reason (MAX_PER_ARTIST) -- one artist owning a shelf is what makes it feel
   broken rather than personal. */
sart=sit.AlbumArtist||'';
if(sart){if((scap[sart]||0)>=2)continue;scap[sart]=(scap[sart]||0)+1;}
sseen[sit.Id]=1;
songs.push({id:sit.Id,name:sit.Name||'',artist:sart,albumId:sit.AlbumId||''});
}
/* sf-mus-discover: measured on this library, 91 of 200 albums have never been
   played and 9 of the top 14 artists own at least one of them -- Drake 4 of 5,
   Gracie Abrams 4 of 6, Taylor Swift 4 of 16. That is the row a PERSONAL
   library can offer that a streaming service cannot, and unlike the old random
   "Artists you have not heard" it is anchored to someone you actually listen
   to. Anchor = the most played artist with at least 3 unplayed albums. */
/* sf-discover-unblock: the album list used to be the third leg of the
   Promise.all above. Measured on a busy night it answered in **13.1s** while
   the other two were done at 4s, and because Promise.all waits for the slowest,
   it gated Your Top Artists, New in your library and If you like as well --
   the page sat at 5 rows for half a minute. Exactly the fault sf-hero-first
   fixed for the hero, reintroduced by me when this row was added.
   It runs on its own now; `discover` starts null and the row appears when the
   list lands. sfDiscSeed holds the two things the join needs, both derived from
   the played-tracks response that has already arrived. */
var playedAlb={},pa;
for(pa=0;pa<items.length;pa++)if(items[pa].AlbumId)playedAlb[items[pa].AlbumId]=1;
sfDiscSeed={names:names,played:playedAlb};
sfMfData={hero:items[0]||null,artists:out.slice(0,10),unheard:unheard.slice(0,20),
songs:songs,discover:null};
sfDiscoverLoad(ac,uid);
sfMfBusy=false;
/* paint in THIS frame rather than waiting up to 400ms for the next tick --
   measured 1425ms data ready vs 1954ms painted, all of it dead time.
   Re-entrant by design: with sfMfData set these take the paint path. */
/* sf-mus-similar: fetched here rather than only when the Radio view opens,
   because Home wants it too. Seeded on the most played artist, so it cannot be
   fired until the tally above exists. One request. */
if(out.length&&sfSimData===null&&!sfSimBusy){
sfSimBusy=true;sfSimSeed=out[0].name||'';
ac.getJSON(ac.getUrl('Items/'+out[0].id+'/Similar',{userId:uid,Limit:12}))
.then(function(r2){sfSimData=(r2&&r2.Items)||[];sfSimBusy=false;
try{sfMusicFeature();}catch(e){}})
.catch(function(){sfSimData=[];sfSimBusy=false;});
}
try{sfMusicFeature();sfMusReveal();}catch(e){}
}).catch(function(){sfMfData={hero:null,artists:[]};sfMfBusy=false;
try{sfMusicFeature();sfMusReveal();}catch(e){}});
return;
}
var srv='';
try{srv=ac.serverId();}catch(e){}
/* ---- sf-mus-newalb: an ALBUM shelf --------------------------------------
   The music landing page had mixes and artists and no albums at all. On a
   library of 198 records that is the shelf a listener actually browses, and it
   is what makes the rebuilt album page reachable.

   Recently ADDED rather than recently played: the featured hero directly above
   is already "last played", so a played-albums row would just repeat it. One
   request, fired once, held for the session. */
if(!pane.querySelector('.sf-mus-newalb')){
if(sfNewAlb===null){
if(!sfNewAlbBusy){
sfNewAlbBusy=true;
ac.getJSON(ac.getUrl('Users/'+uid+'/Items',{IncludeItemTypes:'MusicAlbum',
Recursive:true,Limit:16,SortBy:'DateCreated',SortOrder:'Descending'}))
.then(function(r){sfNewAlb=(r&&r.Items)||[];sfNewAlbBusy=false;
try{sfMusicFeature();}catch(e){}})
.catch(function(){sfNewAlb=[];sfNewAlbBusy=false;});
}
}else if(sfNewAlb.length){
var nsec=document.createElement('div');
nsec.className='verticalSection sf-mylist sf-mus-newalb';
nsec.style.order='6';
var nhead=document.createElement('div');
nhead.className='sectionTitleContainer sectionTitleContainer-cards';
var nh2=document.createElement('h2');
nh2.className='sectionTitle sectionTitle-cards';
nh2.textContent='New in your library';
nhead.appendChild(nh2);
nsec.appendChild(nhead);
var nrow=document.createElement('div');
nrow.className='sf-ml-row';
var ni,nit,ncard,npost,ntt,nsub,nurl;
for(ni=0;ni<sfNewAlb.length;ni++){
nit=sfNewAlb[ni];
ncard=document.createElement('div');
ncard.className='sf-ml-card';
ncard.setAttribute('data-id',nit.Id);
ncard.setAttribute('data-type','MusicAlbum');
npost=document.createElement('div');
npost.className='sf-ml-poster sf-ml-square';
nurl='';
/* Only ask for art the item actually HAS. getImageUrl happily builds a URL for
   an album with no Primary image, and that 404s on every music page load --
   which is exactly what the suite kept reporting. */
if((nit.ImageTags||{}).Primary){
try{nurl=ac.getImageUrl(nit.Id,{type:'Primary',maxWidth:400,tag:nit.ImageTags.Primary});}catch(e){}
}
if(nurl)npost.style.backgroundImage='url("'+nurl+'")';
/* An album with no cover rendered as a blank tile, which reads as a broken
   card rather than a record without art. Mark it so CSS can put something
   deliberate there instead. */
else npost.classList.add('sf-ml-noart');
ntt=document.createElement('div');
ntt.className='cardText cardText-first';
ntt.textContent=nit.Name||'';
nsub=document.createElement('div');
nsub.className='cardText cardText-secondary';
nsub.textContent=nit.AlbumArtist||'';
ncard.appendChild(npost);ncard.appendChild(ntt);
if(nsub.textContent)ncard.appendChild(nsub);
/* the same overlay every other row uses, so tap-to-play behaves identically */
sfAddCardOverlay(ncard,nit.Id,'MusicAlbum','Audio',true,'play');
nrow.appendChild(ncard);
}
nsec.appendChild(nrow);
pane.appendChild(nsec);
}
}
/* ---- your top artists ---- */
if(sfMfData.artists.length&&!pane.querySelector('.sf-mus-artists')){
var sec=document.createElement('div');
sec.className='verticalSection sf-mylist sf-mus-artists';
sec.style.order='4';
var head=document.createElement('div');
head.className='sectionTitleContainer sectionTitleContainer-cards';
var h2=document.createElement('h2');
h2.className='sectionTitle sectionTitle-cards';
h2.textContent='Your Top Artists';
head.appendChild(h2);
sec.appendChild(head);
var row=document.createElement('div');
row.className='sf-ml-row';
var k,ar2,c2,p2,t2,s2,u2;
for(k=0;k<sfMfData.artists.length;k++){
ar2=sfMfData.artists[k];
c2=document.createElement('div');
c2.className='sf-ml-card sf-mus-artist';
c2.setAttribute('data-id',ar2.id);
p2=document.createElement('div');
p2.className='sf-ml-poster sf-mus-artist-art';
u2='';
try{u2=ac.getImageUrl(ar2.id,{type:'Primary',maxWidth:400,tag:ar2.tag});}catch(e){}
if(u2&&ar2.tag)p2.style.backgroundImage='url("'+u2+'")';
t2=document.createElement('div');
t2.className='cardText cardText-first';
t2.textContent=ar2.name;
s2=document.createElement('div');
s2.className='cardText cardText-secondary';
s2.textContent=ar2.plays+(ar2.plays===1?' play':' plays');
var mb=document.createElement('button');
mb.className='sf-mus-artist-mix';
mb.setAttribute('data-artist',ar2.id);
mb.setAttribute('title','Start a mix');
mb.innerHTML='<span class="material-icons" aria-hidden="true">shuffle</span>';
/* stopPropagation so the button does not also open the artist page underneath */
mb.addEventListener('click',function(e){
e.stopPropagation();e.preventDefault();
sfMix(this.getAttribute('data-artist'),'MusicArtist');});
p2.appendChild(mb);
c2.appendChild(p2);c2.appendChild(t2);c2.appendChild(s2);
c2.addEventListener('click',function(){
location.hash='#/details?id='+this.getAttribute('data-id');});
row.appendChild(c2);
}
sec.appendChild(row);
pane.appendChild(sec);
}
/* ---- sf-mus-discover: "Discover more from <artist>" ----------------------
   REPLACES "Artists you have not heard", which picked 20 unheard artists at
   random. Unanchored discovery is the weakest row a personal library can show:
   it answers "what haven't you played" with no reason for you to care about any
   particular answer. This anchors the same idea to someone you demonstrably
   listen to -- albums you OWN by your most played artist that you have never
   played. Measured on this library: 91 of 200 albums have never been played and
   9 of the top 14 artists own at least one, Drake 4 of 5 and Gracie Abrams 4 of
   6, so it is never empty in practice and it is always about someone real.
   Anchor and album list are computed in the fetch above; this only draws. */
if(sfMfData.discover&&sfMfData.discover.albums.length&&!pane.querySelector('.sf-mus-discover')){
var dsec=document.createElement('div');
dsec.className='verticalSection sf-mylist sf-mus-discover';
dsec.style.order='5';
var dhead=document.createElement('div');
dhead.className='sectionTitleContainer sectionTitleContainer-cards';
var dh2=document.createElement('h2');
dh2.className='sectionTitle sectionTitle-cards';
dh2.textContent=(window.sfTr?window.sfTr('Discover more from'):'Discover more from')+' '+sfMfData.discover.artist;
dhead.appendChild(dh2);
dsec.appendChild(dhead);
var drow=document.createElement('div');
drow.className='sf-ml-row';
var di,dit,dcard,dpost,dtt,dsub,durl;
for(di=0;di<sfMfData.discover.albums.length;di++){
dit=sfMfData.discover.albums[di];
dcard=document.createElement('div');
dcard.className='sf-ml-card';
dcard.setAttribute('data-id',dit.Id);
dcard.setAttribute('data-type','MusicAlbum');
dpost=document.createElement('div');
dpost.className='sf-ml-poster sf-ml-square';
durl='';
/* same rule as sf-mus-newalb: only ask for art the item actually HAS, or every
   coverless album 404s on each page load */
if((dit.ImageTags||{}).Primary){
try{durl=ac.getImageUrl(dit.Id,{type:'Primary',maxWidth:400,tag:dit.ImageTags.Primary});}catch(e){}
}
if(durl)dpost.style.backgroundImage='url("'+durl+'")';
else dpost.classList.add('sf-ml-noart');
dtt=document.createElement('div');
dtt.className='cardText cardText-first';
dtt.textContent=dit.Name||'';
dsub=document.createElement('div');
dsub.className='cardText cardText-secondary';
dsub.textContent=dit.ProductionYear?String(dit.ProductionYear):(dit.AlbumArtist||'');
dcard.appendChild(dpost);dcard.appendChild(dtt);
if(dsub.textContent)dcard.appendChild(dsub);
sfAddCardOverlay(dcard,dit.Id,'MusicAlbum','Audio',true,'play');
drow.appendChild(dcard);
}
dsec.appendChild(drow);
pane.appendChild(dsec);
}
/* ---- sf-liked-row: "Liked Songs" ----------------------------------------
   Pairs with sf-np-fav. Giving people a heart on the bar is only half of it --
   Spotify's Liked Songs is one of the most used surfaces in the app precisely
   because liking something has somewhere to GO. Hidden entirely at zero, so it
   appears the moment the first track is liked rather than sitting there empty
   (this library had 0 favourites for exactly as long as there was nowhere to
   see them). */
if(sfLikedData===null){
if(!sfLikedBusy){
sfLikedBusy=true;
ac.getJSON(ac.getUrl('Users/'+uid+'/Items',{IncludeItemTypes:'Audio',Recursive:true,
Limit:40,Filters:'IsFavorite',SortBy:'DatePlayed',SortOrder:'Descending',Fields:'AlbumId'}))
.then(function(r){sfLikedData=(r&&r.Items)||[];sfLikedBusy=false;try{sfMusicFeature();}catch(e){}})
.catch(function(){sfLikedData=[];sfLikedBusy=false;});
}
}else if(sfLikedData.length&&!pane.querySelector('.sf-mus-liked')){
var lsec=document.createElement('div');
lsec.className='verticalSection sf-mylist sf-mus-liked';
lsec.style.order='9';
var lhead=document.createElement('div');
lhead.className='sectionTitleContainer sectionTitleContainer-cards';
var lh2=document.createElement('h2');
lh2.className='sectionTitle sectionTitle-cards';
lh2.textContent=(window.sfTr?window.sfTr('Liked Songs'):'Liked Songs');
lhead.appendChild(lh2);
lsec.appendChild(lhead);
var lrow=document.createElement('div');
lrow.className='sf-ml-row';
var li2,lit,lcard,lpost,ltt,lsub,lurl;
for(li2=0;li2<sfLikedData.length;li2++){
lit=sfLikedData[li2];
lcard=document.createElement('div');
lcard.className='sf-ml-card';
lcard.setAttribute('data-id',lit.Id);
lcard.setAttribute('data-type','Audio');
lpost=document.createElement('div');
lpost.className='sf-ml-poster sf-ml-square';
lurl='';
/* art off the ALBUM: a track rarely has its own Primary, and the cover is what
   makes the card recognisable anyway (same rule as Song radio) */
try{if(lit.AlbumId)lurl=ac.getImageUrl(lit.AlbumId,{type:'Primary',maxWidth:400});}catch(e){}
if(lurl)lpost.style.backgroundImage='url("'+lurl+'")';
else lpost.classList.add('sf-ml-noart');
ltt=document.createElement('div');
ltt.className='cardText cardText-first';
ltt.textContent=lit.Name||'';
lsub=document.createElement('div');
lsub.className='cardText cardText-secondary';
lsub.textContent=lit.AlbumArtist||lit.Album||'';
lcard.appendChild(lpost);lcard.appendChild(ltt);
if(lsub.textContent)lcard.appendChild(lsub);
sfAddCardOverlay(lcard,lit.Id,'Audio','Audio',false,'play');
lrow.appendChild(lcard);
}
lsec.appendChild(lrow);
pane.appendChild(lsec);
}
/* ---- sf-mus-simrow: "If you like <artist>" ------------------------------
   Jellyfin's /Items/{id}/Similar over your OWN library, so everything it
   suggests is playable. Verified quality: Coldplay -> Keane, Snow Patrol, The
   Cranberries, The Script, OneRepublic. Deliberately different from the Radio
   tab's "Because you listen to" shelf, which is the same artists as STATIONS:
   here a tap browses the artist, there it starts playing. Dropped below 3
   results -- hip-hop returns 2, and a two-card row reads as a bug. */
var simFresh=0,sf2;
if(sfSimData&&sfMfData&&sfMfData.artists){
var topSeen={},t2;
for(t2=0;t2<sfMfData.artists.length;t2++)topSeen[sfMfData.artists[t2].id]=1;
for(sf2=0;sf2<sfSimData.length;sf2++)if(sfSimData[sf2]&&sfSimData[sf2].Id&&!topSeen[sfSimData[sf2].Id])simFresh++;
}
if(simFresh>=3&&!pane.querySelector('.sf-mus-simrow')){
var ssec=document.createElement('div');
ssec.className='verticalSection sf-mylist sf-mus-simrow';
ssec.style.order='10';
var shead=document.createElement('div');
shead.className='sectionTitleContainer sectionTitleContainer-cards';
var sh2=document.createElement('h2');
sh2.className='sectionTitle sectionTitle-cards';
sh2.textContent=(window.sfTr?window.sfTr('If you like'):'If you like')+' '+sfSimSeed;
shead.appendChild(sh2);
ssec.appendChild(shead);
var srow=document.createElement('div');
srow.className='sf-ml-row';
var zi,za,zc,zp,zt,zurl,zmb;
/* sf-mus-simrow: drop anyone already in Your Top Artists. Jellyfin's Similar
   is happy to return artists you play constantly -- the first build offered
   Sabrina Carpenter and Ed Sheeran, her #2 and #4 most played, directly under a
   row that already showed both. On a library this size that is not discovery,
   it is repetition. Filtered against the same tally the top-artists row uses. */
var topIds={},ti;
if(sfMfData&&sfMfData.artists)for(ti=0;ti<sfMfData.artists.length;ti++)topIds[sfMfData.artists[ti].id]=1;
for(zi=0;zi<sfSimData.length;zi++){
za=sfSimData[zi];
if(!za||!za.Id)continue;
if(topIds[za.Id])continue;
zc=document.createElement('div');
zc.className='sf-ml-card sf-mus-artist';
zc.setAttribute('data-id',za.Id);
zp=document.createElement('div');
zp.className='sf-ml-poster sf-mus-artist-art';
zurl='';
if((za.ImageTags||{}).Primary){
try{zurl=ac.getImageUrl(za.Id,{type:'Primary',maxWidth:400,tag:za.ImageTags.Primary});}catch(e){}
}
if(zurl)zp.style.backgroundImage='url("'+zurl+'")';
else zp.classList.add('sf-ml-noart');
zt=document.createElement('div');
zt.className='cardText cardText-first';
zt.textContent=za.Name||'';
zmb=document.createElement('button');
zmb.className='sf-mus-artist-mix';
zmb.setAttribute('data-artist',za.Id);
zmb.setAttribute('title',(window.sfTr?window.sfTr('Radio'):'Radio'));
zmb.innerHTML='<span class="material-icons" aria-hidden="true">shuffle</span>';
zmb.addEventListener('click',function(e){
e.stopPropagation();e.preventDefault();
sfMix(this.getAttribute('data-artist'),'MusicArtist');});
zp.appendChild(zmb);
zc.appendChild(zp);zc.appendChild(zt);
zc.addEventListener('click',function(){
location.hash='#/details?id='+this.getAttribute('data-id');});
srow.appendChild(zc);
}
ssec.appendChild(srow);
pane.appendChild(ssec);
}
}
'''

# _LS_10 (orig L6536-7253) -- sf-music-ambient, sf-hero-oneshot, sf-mus-dedupe
_LS_10 = r'''/* sf-music-ambient: colour the music page from the artwork it is showing.

   This is the single biggest reason the stock page reads flat. The hero already
   paints the album cover behind itself blurred, but that only works when the
   cover is colourful -- the featured album was "folklore", which is a grey
   black-and-white photograph, so the whole hero rendered as an empty dark box.
   Spotify and Apple Music both key the surface off a colour DERIVED from the art
   rather than off the art itself, which is what keeps a muted cover from
   producing a muted page.

   The colour is extracted in-browser: the artwork is same-origin (Jellyfin
   serves it), so a canvas readback is allowed and needs no server work. Pixels
   are bucketed coarsely and scored on saturation weighted by how common the
   bucket is, so a large flat background loses to a smaller vivid element -- and
   near-black/near-white are excluded outright, otherwise every dark cover
   returns "black" and nothing changes. If extraction fails for any reason the
   variables are simply never set and the existing styling stands. */
var SFAC={},SFACBUSY={};
/* clamp saturation into [smin,smax] and lightness into [lmin,lmax], hue kept */
function sfHslClamp(rgb,smin,smax,lmin,lmax){
var r=rgb[0]/255,g=rgb[1]/255,b=rgb[2]/255;
var mx=Math.max(r,g,b),mn=Math.min(r,g,b),h=0,sl=0,l=(mx+mn)/2,d=mx-mn;
if(d){
sl=l>0.5?d/(2-mx-mn):d/(mx+mn);
if(mx===r)h=((g-b)/d+(g<b?6:0));
else if(mx===g)h=((b-r)/d+2);
else h=((r-g)/d+4);
h/=6;
}
if(sl<smin)sl=smin; if(sl>smax)sl=smax;
if(l<lmin)l=lmin; if(l>lmax)l=lmax;
function hue2(p,q,t){
if(t<0)t+=1; if(t>1)t-=1;
if(t<1/6)return p+(q-p)*6*t;
if(t<1/2)return q;
if(t<2/3)return p+(q-p)*(2/3-t)*6;
return p;
}
var q2=l<0.5?l*(1+sl):l+sl-l*sl,p2=2*l-q2;
return [Math.round(hue2(p2,q2,h+1/3)*255),
        Math.round(hue2(p2,q2,h)*255),
        Math.round(hue2(p2,q2,h-1/3)*255)];
}
/* sf-hero-oneshot: extract the featured album's accent BEFORE the panel is
   mounted, so .sf-mus-amb is already on <html> the first time anyone sees it.
   sfMusAmbient still runs on the tick and is a cache hit (SFAC is keyed by url),
   so it stays the path for a hero that CHANGES -- playing something new makes it
   the new "last played" and retargets the panel.
   The 1200ms deadline exists because sfAccentFor's img.onerror never calls back
   and it drops a callback while another read of the same url is in flight; the
   pane must reveal regardless. Late colour is a far smaller sin than a page that
   never appears. */
function sfHeroPrime(ac){
if(sfHeroAmb)return;
function settle(){if(!sfHeroAmb){sfHeroAmb=1;try{sfMusReveal();}catch(e){}}}
if(!(sfHeroData&&sfHeroData.AlbumId)){settle();return;}
var art='';
try{art=ac.getImageUrl(sfHeroData.AlbumId,{type:'Primary',maxWidth:700});}catch(e){}
if(!art){settle();return;}
var timer=setTimeout(settle,1200);
sfAccentFor(art,function(rgb){
clearTimeout(timer);
if(rgb){
var st=document.documentElement.style;
st.setProperty('--sf-mus-accent','rgb('+rgb[0]+','+rgb[1]+','+rgb[2]+')');
st.setProperty('--sf-mus-accent-30','rgba('+rgb[0]+','+rgb[1]+','+rgb[2]+',.55)');
st.setProperty('--sf-mus-accent-14','rgba('+rgb[0]+','+rgb[1]+','+rgb[2]+',.22)');
document.documentElement.classList.add('sf-mus-amb');
}
settle();
});
}
function sfAccentFor(url,cb){
if(!url)return;
if(SFAC[url]!==undefined){cb(SFAC[url]);return;}
if(SFACBUSY[url])return;
SFACBUSY[url]=1;
var img=new Image();
img.crossOrigin='anonymous';
img.onload=function(){
try{
var N=36,cv=document.createElement('canvas');
cv.width=N;cv.height=N;
var cx=cv.getContext('2d');
cx.drawImage(img,0,0,N,N);
var d=cx.getImageData(0,0,N,N).data,bins={},i,best=null,bestScore=-1;
for(i=0;i<d.length;i+=4){
if(d[i+3]<128)continue;
var r=d[i],g=d[i+1],b=d[i+2];
var mx=Math.max(r,g,b),mn=Math.min(r,g,b);
if(mx<38||mn>226)continue;              /* nearly black / nearly white */
var key=(r>>4)+','+(g>>4)+','+(b>>4);
var e=bins[key]||(bins[key]={n:0,r:0,g:0,b:0});
e.n++;e.r+=r;e.g+=g;e.b+=b;
}
for(var k in bins){
if(!bins.hasOwnProperty(k))continue;
var q=bins[k],ar=q.r/q.n,ag=q.g/q.n,ab=q.b/q.n;
var M=Math.max(ar,ag,ab),m2=Math.min(ar,ag,ab);
var sat=M?(M-m2)/M:0;
/* frequency alone picks the background; saturation alone picks a stray
   pixel. sqrt(n) keeps big areas relevant without letting them dominate. */
var score=Math.sqrt(q.n)*(0.25+sat);
if(score>bestScore){bestScore=score;best=[Math.round(ar),Math.round(ag),Math.round(ab)];}
}
if(best){
/* Normalise in HSL rather than scaling RGB. The first version only lifted dark
   colours, so a greyscale cover (folklore is a black-and-white photograph) came
   back as mid-grey: the gradient was invisible and the accented Play button
   turned dark grey -- worse than the white one it replaced. Clamping saturation
   and lightness guarantees a usable accent from ANY artwork while keeping its
   hue, which is the part that carries the identity of the cover. */
best=sfHslClamp(best,0.45,0.92,0.46,0.68);
}
SFAC[url]=best;
}catch(e){SFAC[url]=null;}
SFACBUSY[url]=0;
try{cb(SFAC[url]);}catch(e){}
};
img.onerror=function(){SFAC[url]=null;SFACBUSY[url]=0;};
img.src=url;
}
function sfMusAmbient(){
if((location.hash||'').indexOf('#/music')!==0){
document.documentElement.classList.remove('sf-mus-amb');
return;
}
var hero=document.querySelector('.sf-mus-hero');
if(!hero)return;
var bg=hero.querySelector('.sf-mus-hero-bg');
if(!bg)return;
var m=/url\(["']?(.*?)["']?\)/.exec(bg.style.backgroundImage||'');
var url=m&&m[1];
if(!url)return;
if(hero.getAttribute('data-sf-amb')===url)return;
sfAccentFor(url,function(rgb){
if(!rgb)return;
hero.setAttribute('data-sf-amb',url);
var s=document.documentElement.style;
s.setProperty('--sf-mus-accent','rgb('+rgb[0]+','+rgb[1]+','+rgb[2]+')');
s.setProperty('--sf-mus-accent-30','rgba('+rgb[0]+','+rgb[1]+','+rgb[2]+',.55)');
s.setProperty('--sf-mus-accent-14','rgba('+rgb[0]+','+rgb[1]+','+rgb[2]+',.22)');
document.documentElement.classList.add('sf-mus-amb');
});
}
/* sf-mus-dedupe: Jellyfin's "Recently Played" row lists TRACKS, so playing one
   album puts the same cover on screen five times in a row (measured: 5 identical
   Chappell Roan covers on desktop). Collapse it to one card per album -- which is
   what every music app shows -- by hiding the later duplicates rather than
   removing them, since Jellyfin owns and re-renders those nodes. */
/* sf-hide-internal-playlists (2026-08-20). The now-playing queue is stored as a
   REAL Jellyfin playlist called "__np_queue", so it renders as a normal card on
   Music > Playlists -- a tile named "__np_queue" sitting between "2020s Mix" and
   "Alternative Rock Mix". sfPlaylistRow already skips names beginning "__" when
   it builds our own shelf, but Jellyfin's own grid knew nothing about the
   convention. Same rule, applied to any playlist card the app renders.
   Hidden, not deleted: the queue playlist is load-bearing for playback. */
function sfHideInternalPl(){
var cards=document.querySelectorAll('.card[data-type="Playlist"], .card[data-id]'),i,c,t,n;
for(i=0;i<cards.length;i++){
c=cards[i];
if(c.getAttribute('data-sf-plchk')==='1')continue;
t=c.querySelector('.cardText-first')||c.querySelector('.cardText');
n=t?(t.textContent||'').trim():'';
if(!n)continue;                       /* title not painted yet -- try again next tick */
c.setAttribute('data-sf-plchk','1');
if(n.indexOf('__')===0)c.classList.add('sf-pl-internal');
}
}
function sfMusDedupe(){
if((location.hash||'').indexOf('#/music')!==0)return;
var secs=document.querySelectorAll('.verticalSection'),i,j;
for(i=0;i<secs.length;i++){
var t=secs[i].querySelector('.sectionTitle');
if(!t||!/recently played|frequently played/i.test(t.textContent||''))continue;
var cont=secs[i].querySelector('.itemsContainer');
if(!cont)continue;
var cards=cont.children,seen={};
for(j=0;j<cards.length;j++){
var c=cards[j];
/* an Audio card carries its album in data-albumid on this build; fall back to
   the visible album/artist text so the row still collapses if that changes */
/* There is no data-albumid on this build (verified), and keying on the card's
   own text is useless here: cardText-first is the TRACK name, so five songs off
   one album produce five different keys and nothing collapses. The artwork URL
   is the album -- /Items/<albumId>/Images/Primary -- and it is identical for
   every track of that album. */
var img=c.querySelector('.cardImageContainer'),key='';
var bgi=img?(img.style.backgroundImage||''):'';
var mm=/\/Items\/([0-9a-f]{32})\/Images/i.exec(bgi);
if(mm)key=mm[1];
key=String(key).trim();
if(!key){c.classList.remove('sf-mus-dup');continue;}
if(seen[key]){c.classList.add('sf-mus-dup');}
else{seen[key]=1;c.classList.remove('sf-mus-dup');}
}
}
}
/* sf-nav-tuck: the music page stacks TWO pill bars (our main nav above
   Jellyfin's library tabs). Measured on a 412px phone that is a 171px header
   before a single card -- against 117px everywhere else -- and the library strip
   overflows, clipping "Songs". Rather than delete a bar, tuck the upper one away
   once the user starts scrolling and bring it back at the top, which is the
   shrinking-tab-bar behaviour Apple Music uses. Pure class toggle, no layout
   measurement, so it cannot fight sfMainNav. */
var sfTuckY=0;
function sfNavTuck(){
if(!sfLibraryRoute()){document.documentElement.classList.remove('sf-nav-tucked');return;}
var y=window.pageYOffset||document.documentElement.scrollTop||0;
var el=document.querySelector('.sf-mus-scroller');
if(el)y=el.scrollTop;
/* hysteresis: tuck past 90px, restore under 30px, so a rubber-band scroll does
   not flap the header open and shut */
var on=document.documentElement.classList.contains('sf-nav-tucked');
if(!on&&y>90)document.documentElement.classList.add('sf-nav-tucked');
else if(on&&y<30)document.documentElement.classList.remove('sf-nav-tucked');
sfTuckY=y;
}
/* sf-now-immersive: a real full-screen Now Playing.

   Jellyfin's own #/queue is a transport bar over remote-control accordions
   ("Navigation / Send Message / Enter Text") -- captured live, and it is the
   weakest surface in the app. This replaces the MOMENT of listening, which is
   the thing both Spotify and Apple Music compete on.

   Design notes, from looking at what each does well:
   * Apple's iOS 26 player expands the artwork full-screen and floats translucent
     controls ON the art. Album "motion" is the headline feature -- we cannot ship
     animated artwork, but a slow drifting colour field derived from the cover
     reads as the same idea and works for EVERY track, not the handful that ship
     motion assets.
   * Spotify's most-cited flaw in 2026 is clutter -- "unnecessary features that
     distract from the core experience of listening". So this surface holds
     artwork, the track, a scrubber, transport, and exactly two optional panels
     (Lyrics, Up Next). Nothing else.

   Playback is NEVER re-implemented: every control proxies a click to Jellyfin's
   own button in .nowPlayingBar (.playPauseButton, .nextTrackButton, ...). That is
   the same lesson as sfPlayItemViaProxy -- the handlers are bound to those nodes,
   so driving them is the only thing that reliably works. */
var sfNpEl=null,sfNpOpen=false,sfNpArt='',sfNpSeek=false;
function sfNpBar(){return document.querySelector('.nowPlayingBar');}
function sfNpAudio(){return document.querySelector('audio');}
function sfNpHit(sel){
var bar=sfNpBar();if(!bar)return false;
var b=bar.querySelector(sel);
if(!b||b.classList.contains('hide'))return false;
b.click();return true;
}
function sfNpFmt(s){
if(!isFinite(s)||s<0)s=0;
/* sf-np-hours: minutes-only overflowed the moment the player was reused for
   audiobooks -- an 11-hour book read "70:00 / 671:30" instead of
   "1:10:00 / 11:11:30". Songs are under an hour so their display is unchanged. */
var h=Math.floor(s/3600),m=Math.floor((s%3600)/60),x=Math.floor(s%60);
if(h)return h+':'+(m<10?'0':'')+m+':'+(x<10?'0':'')+x;
return m+':'+(x<10?'0':'')+x;
}
function sfNpBuild(){
if(sfNpEl&&sfNpEl.parentNode)return sfNpEl;
var d=document.createElement('div');
d.className='sf-np';
d.innerHTML=
 '<div class="sf-np-bg"></div>'
+'<div class="sf-np-tint"></div>'
+'<div class="sf-np-scrim"></div>'
+'<div class="sf-np-body">'
+'  <button type="button" class="sf-np-close" title="Close"><span class="material-icons" aria-hidden="true">expand_more</span></button>'
+'  <div class="sf-np-stage">'
+'    <div class="sf-np-artwrap"><div class="sf-np-art"></div></div>'
+'    <div class="sf-np-meta">'
+'      <div class="sf-np-title"></div>'
+'      <div class="sf-np-artist"></div>'
+'      <button type="button" class="sf-np-album">Album</button>'
+'    </div>'
+'    <div class="sf-np-scrub">'
+'      <input class="sf-np-range" type="range" min="0" max="1000" value="0" step="1" aria-label="Seek">'
+'      <div class="sf-np-times"><span class="sf-np-cur">0:00</span><span class="sf-np-dur">0:00</span></div>'
+'    </div>'
+'    <div class="sf-np-controls">'
+'      <button type="button" class="sf-np-b sf-np-shuffle" title="Shuffle"><span class="material-icons">shuffle</span></button>'
+'      <button type="button" class="sf-np-b sf-np-prev" title="Previous"><span class="material-icons">skip_previous</span></button>'
+'      <button type="button" class="sf-np-b sf-np-play" title="Play/Pause"><span class="material-icons">play_arrow</span></button>'
+'      <button type="button" class="sf-np-b sf-np-next" title="Next"><span class="material-icons">skip_next</span></button>'
+'      <button type="button" class="sf-np-b sf-np-repeat" title="Repeat"><span class="material-icons">repeat</span></button>'
/* sf-np-ctrlclose: .sf-np-controls was never closed, so the Lyrics/Up Next tab
   row became a CHILD of the transport flex row instead of a sibling. That is
   one bug producing two separate symptoms: the row measured 466px inside a
   390px iPhone (313.6px of buttons + 152.4px of tabs), pushing Shuffle to
   x=-38 and off-screen entirely; and 'Up Next' wrapped to two lines because
   its tab was being squeezed by the buttons beside it. In audiobook mode the
   stage injects four MORE buttons into this same row, which is what the
   .sf-np-book flex-wrap:nowrap workaround was papering over. */
+'    </div>'
+'    <div class="sf-np-tabs">'
+'      <button type="button" class="sf-np-tab sf-np-tab-lyr">Lyrics</button>'
+'      <button type="button" class="sf-np-tab sf-np-tab-q">Up Next</button>'
+'    </div>'
+'  </div>'
+'  <div class="sf-np-panel"><div class="sf-np-panel-in"></div></div>'
+'</div>';
document.body.appendChild(d);
sfNpEl=d;
function stop(e){e.preventDefault();e.stopPropagation();}
d.querySelector('.sf-np-close').addEventListener('click',function(e){stop(e);sfNpSetOpen(false);});
d.querySelector('.sf-np-album').addEventListener('click',function(e){
stop(e);
var id=sfCurrentTrackId(),ac=window.ApiClient;
if(!id||!ac)return;
ac.getItem(ac.getCurrentUserId(),id).then(function(it){
var t=it.AlbumId||it.ParentId;
if(t){sfNpSetOpen(false);window.location.hash='#/details?id='+t+'&serverId='+ac.serverId();}
}).catch(function(){});
});
d.querySelector('.sf-np-shuffle').addEventListener('click',function(e){stop(e);sfNpHit('.btnShuffleQueue');});
d.querySelector('.sf-np-prev').addEventListener('click',function(e){stop(e);sfNpHit('.previousTrackButton');});
d.querySelector('.sf-np-next').addEventListener('click',function(e){stop(e);sfNpHit('.nextTrackButton');});
d.querySelector('.sf-np-repeat').addEventListener('click',function(e){stop(e);sfNpHit('.toggleRepeatButton');});
d.querySelector('.sf-np-play').addEventListener('click',function(e){
stop(e);
/* the bar has more than one .playPauseButton (Jellyfin renders a second for
   narrow layouts); click the one that is actually visible */
var bar=sfNpBar();if(!bar)return;
var all=bar.querySelectorAll('.playPauseButton'),i;
for(i=0;i<all.length;i++){if(all[i].getClientRects().length){all[i].click();return;}}
if(all.length)all[0].click();
});
/* Seeking: drive Jellyfin's own range input where there is one so remote /
   cast targets stay in sync, and fall back to the audio element locally. */
var rng=d.querySelector('.sf-np-range');
rng.addEventListener('input',function(){sfNpSeek=true;});
rng.addEventListener('change',function(){
var a=sfNpAudio(),frac=(parseFloat(rng.value)||0)/1000;
var bar=sfNpBar(),jr=bar?bar.querySelector('input[type=range]'):null;
if(jr){
var mn=parseFloat(jr.min)||0,mx=parseFloat(jr.max)||100;
jr.value=String(mn+(mx-mn)*frac);
jr.dispatchEvent(new Event('input',{bubbles:true}));
jr.dispatchEvent(new Event('change',{bubbles:true}));
}else if(a&&isFinite(a.duration)){a.currentTime=a.duration*frac;}
sfNpSeek=false;
});
d.querySelector('.sf-np-tab-lyr').addEventListener('click',function(e){stop(e);sfNpPanel('lyrics');});
d.querySelector('.sf-np-tab-q').addEventListener('click',function(e){stop(e);sfNpPanel('queue');});
/* swipe down to dismiss, the gesture both apps use */
var y0=null;
d.addEventListener('touchstart',function(e){y0=e.touches&&e.touches[0]?e.touches[0].clientY:null;},{passive:true});
d.addEventListener('touchend',function(e){
if(y0==null)return;
var y1=(e.changedTouches&&e.changedTouches[0])?e.changedTouches[0].clientY:y0;
if(y1-y0>90)sfNpSetOpen(false);
y0=null;
},{passive:true});
document.addEventListener('keydown',function(e){
if(e.key==='Escape'&&sfNpOpen)sfNpSetOpen(false);
});
return d;
}
/* sf-np-typeflash (2026-08-24). The admin: opening an audiobook full screen "flickers
   and the controls don't load in right away -- I see music controls at first, like
   the lyrics and next up tab."

   Cause, measured: this overlay is BUILT with the music chrome (Lyrics / Up Next
   tabs, shuffle, prev, next, repeat, Album) and only becomes an audiobook player
   when the separate sf-audiobook-player tick -- a 700ms setInterval -- adds
   .sf-np-book and injects the book buttons. So the first open of a session always
   painted the music player first and swapped afterwards. Frame-by-frame at a 390px
   viewport: 168ms, 291ms and 440ms of wrong UI in three runs (uniform 0-700ms), the
   transport row jumping 27-30px when it settled, and one run where the bar never
   published data-itemtype at all so the music UI simply stayed.

   The type IS knowable synchronously at tap time -- from the bar's own
   data-itemtype, or from the id->type map the player remembers -- so ask for it
   HERE, in the same task that shows the overlay, and let the audiobook stage build
   before the first paint. Only when it is genuinely not knowable yet does
   .sf-np-typing suppress the chrome that is valid for just one of the two kinds.
   Suppress-until-known, never render-then-swap. */
function sfNpSetOpen(v){
sfNpOpen=!!v;
var d=sfNpBuild();
if(sfNpOpen){
var known=null;
try{if(window.__sfAbSync)known=window.__sfAbSync();}catch(e){}
d.classList.toggle('sf-np-typing',known===null);
}else if(d.classList.contains('sf-np-typing')){d.classList.remove('sf-np-typing');}
d.classList.toggle('sf-np-show',sfNpOpen);
document.documentElement.classList.toggle('sf-np-lock',sfNpOpen);
if(sfNpOpen)sfNpSync(true);
}
function sfNpPanel(kind){
var d=sfNpBuild();
var cur=d.getAttribute('data-panel')||'';
if(cur===kind){d.removeAttribute('data-panel');d.classList.remove('sf-np-haspanel');}
else{d.setAttribute('data-panel',kind);d.classList.add('sf-np-haspanel');}
sfNpFill();
}
/* sf-np-panels: real synced lyrics and the real queue.

   Both were stand-ins in the first cut -- the lyrics panel cloned a static block
   with no timing, and "Up Next" showed the current ALBUM because playbackManager
   is not on window in this build. Neither is necessary:

   * Lyrics ARE time-coded. /Audio/{id}/Lyrics returns
     {Text, Start, Cues} with **Start in ticks** (1723300000 = 172.33s), so
     line-level sync is exact. Cues is always empty, which is why there is no
     word-level wipe -- an interpolated sweep pointed at the wrong word on any
     line with a pause.
   * The queue is on the SESSION. /Sessions?deviceId=<ApiClient.deviceId()>
     returns this browser's own session with NowPlayingQueueFullItems -- verified
     150 items for a mix -- plus the session id, which is what lets a tap jump to
     a track without a player API. */
var sfNpLyr={id:null,lines:[],synced:false,idx:-1};
var sfNpQ={at:0,items:[],curId:null,session:null,busy:false};

function sfNpTicks(){
var a=sfNpAudio();
return a?(a.currentTime*10000000):0;
}
/* ---------------- lyrics ---------------- */
function sfNpLyrLoad(id,box){
sfNpLyr={id:id,lines:[],synced:false,idx:-1};
box.innerHTML='<div class="sf-np-empty">Loading lyrics…</div>';
var ac=window.ApiClient;
if(!ac){box.innerHTML='<div class="sf-np-empty">No lyrics</div>';return;}
ac.getJSON(ac.getUrl('Audio/'+id+'/Lyrics')).then(function(j){
if(sfNpLyr.id!==id)return;                 /* track changed while loading */
var lines=(j&&j.Lyrics)||[];
if(!lines.length){box.innerHTML='<div class="sf-np-empty">No lyrics for this track</div>';return;}
sfNpLyr.lines=lines;
sfNpLyr.synced=(lines[0].Start!=null);
var html='',i,t;
for(i=0;i<lines.length;i++){
t=(lines[i].Text||'').trim();
html+='<div class="sf-np-lyr'+(t?'':' sf-np-lyr-blank')+'" data-i="'+i+'">'
+String(t).replace(/</g,'&lt;')+'</div>';
}
box.innerHTML='<button type="button" class="sf-np-flyr" title="Fullscreen lyrics" aria-label="Fullscreen lyrics">'
+'<span class="material-icons" aria-hidden="true">open_in_full</span></button>'
+'<div class="sf-np-lyrbox">'+html+'</div>';
/* sf-np-flyr: hand off to the fullscreen surface. The overlay is closed first
   for the same reason the desktop path calls sfLyricsClose() -- one lyrics
   surface at a time, or two of them fight over the same audio clock. */
var _fb=box.querySelector('.sf-np-flyr');
if(_fb)_fb.addEventListener('click',function(e){
e.stopPropagation();e.preventDefault();
try{sfNpSetOpen(false);}catch(err){}
try{sfFlyrOpen();}catch(err){}
});
/* tap a line to jump there -- only meaningful when the lines are timed */
if(sfNpLyr.synced){
box.classList.add('sf-np-lyr-seek');
box.addEventListener('click',function(e){
var el=e.target&&e.target.closest?e.target.closest('.sf-np-lyr'):null;
if(!el)return;
var li=sfNpLyr.lines[parseInt(el.getAttribute('data-i'),10)];
if(!li||li.Start==null)return;
var a=sfNpAudio();
if(a&&isFinite(a.duration))a.currentTime=Math.max(0,li.Start/10000000);
});
}
sfNpLyr.idx=-1;
}).catch(function(){
if(sfNpLyr.id!==id)return;
box.innerHTML='<div class="sf-np-empty">No lyrics for this track</div>';
});
}
function sfNpLyrSync(box){
if(!sfNpLyr.synced||!sfNpLyr.lines.length)return;
var ticks=sfNpTicks(),idx=-1,i;
for(i=0;i<sfNpLyr.lines.length;i++){
if(sfNpLyr.lines[i].Start<=ticks)idx=i;else break;
}
if(idx<0||idx===sfNpLyr.idx)return;
sfNpLyr.idx=idx;
var rows=box.querySelectorAll('.sf-np-lyr'),k,d;
if(!rows.length)return;
/* same distance falloff the side panel uses, so the two surfaces read as one
   design rather than two */
for(k=0;k<rows.length;k++){
d=Math.abs(k-idx);
rows[k].className=rows[k].className.replace(/\s*sf-np-(on|d1|d2)\b/g,'');
if(d===0)rows[k].className+=' sf-np-on';
else if(d<=2)rows[k].className+=' sf-np-d1';
else rows[k].className+=' sf-np-d2';
}
var wrap=box.querySelector('.sf-np-lyrbox')||box;
var cur=rows[idx];
/* hold the current line just above centre so more of the song ahead is visible
   than behind -- 42%, matching the other lyric surfaces */
var aim=cur.offsetTop-box.clientHeight*0.42+cur.offsetHeight/2;
box.scrollTo({top:Math.max(0,aim),behavior:'smooth'});
}
/* ---------------- queue ---------------- */
function sfNpQueueLoad(box,force){
var ac=window.ApiClient;
if(!ac||!ac.getJSON){box.innerHTML='<div class="sf-np-empty">Queue unavailable</div>';return;}
var now=Date.now();
if(!force&&sfNpQ.busy)return;
if(!force&&(now-sfNpQ.at)<4000)return;
sfNpQ.busy=true;sfNpQ.at=now;
var dev='';
try{dev=ac.deviceId?ac.deviceId():'';}catch(e){dev='';}
/* only filter when we actually HAVE a device id -- Sessions?deviceId= matches
   nothing, which would strand the panel on the no-session path above */
ac.getJSON(dev?ac.getUrl('Sessions',{deviceId:dev}):ac.getUrl('Sessions')).then(function(list){
if(Array.isArray(list)&&list.length>1){var np=list.filter(function(x){return x.NowPlayingItem;});if(np.length)list=np;}
var s=(list&&list.length)?list[0]:null;
if(!s){sfNpQ.busy=false;sfNpQ.items=[];sfNpQueuePaint(box);return;}  /* was: return without painting, which left the panel permanently blank */
sfNpQ.session=s.Id;
sfNpQ.curId=(s.NowPlayingItem||{}).Id||null;
var full=s.NowPlayingQueueFullItems||[];
if(full.length){sfNpQ.busy=false;sfNpQ.items=full;sfNpQueuePaint(box);return;}
/* NowPlayingQueueFullItems lags badly: measured empty at 6s and 14s after
   playback started and only populated at ~26s, while NowPlayingQueue (ids only)
   was complete at 6s. Waiting on the full list left the panel blank for half a
   minute AND made a tap-to-jump impossible, because the item list it indexes
   into was empty. So drive off the ids and resolve them in one batch. */
var ids=(s.NowPlayingQueue||[]).map(function(x){return x.Id;}).filter(Boolean);
if(!ids.length){sfNpQ.busy=false;sfNpQ.items=[];sfNpQueuePaint(box);return;}
var uid=ac.getCurrentUserId();
ac.getJSON(ac.getUrl('Users/'+uid+'/Items',{Ids:ids.slice(0,300).join(','),
Fields:'RunTimeTicks'})).then(function(r){
sfNpQ.busy=false;
var got={},L=(r&&r.Items)||[],i;
for(i=0;i<L.length;i++)got[String(L[i].Id)]=L[i];
/* /Items does not preserve the order asked for, so rebuild it from the queue */
var out=[];
for(i=0;i<ids.length;i++)if(got[String(ids[i])])out.push(got[String(ids[i])]);
sfNpQ.items=out;
sfNpQueuePaint(box);
}).catch(function(){sfNpQ.busy=false;});
}).catch(function(){sfNpQ.busy=false;});
}
function sfNpQueuePaint(box){
var ac=window.ApiClient;
var L=sfNpQ.items||[];
if(!L.length){box.innerHTML='<div class="sf-np-empty">Nothing queued</div>';return;}
var cur=-1,i;
for(i=0;i<L.length;i++)if(String(L[i].Id)===String(sfNpQ.curId)){cur=i;break;}
var sig=String(sfNpQ.curId)+'|'+L.length;
if(box.getAttribute('data-sig')===sig)return;      /* nothing changed */
box.setAttribute('data-sig',sig);
/* show the current track plus what follows -- this is "Up Next", not a history */
var start=cur<0?0:cur;
var html='',n=0;
for(i=start;i<L.length&&n<60;i++,n++){
var it=L[i],art='';
try{art=ac.getImageUrl(it.AlbumId||it.Id,{type:'Primary',maxWidth:80,
tag:it.AlbumPrimaryImageTag});}catch(e){art='';}
var who=it.AlbumArtist||((it.Artists&&it.Artists[0])||'');
var secs=Math.round((it.RunTimeTicks||0)/10000000);
html+='<div class="sf-np-qrow'+(i===cur?' sf-np-qrow-on':'')+'" data-idx="'+i+'">'
+'<div class="sf-np-qart"'+(art?(' style="background-image:url(\''+art+'\')"'):'')+'></div>'
+'<div class="sf-np-qmeta"><div class="sf-np-qt">'+String(it.Name||'').replace(/</g,'&lt;')+'</div>'
+'<div class="sf-np-qa">'+String(who).replace(/</g,'&lt;')+'</div></div>'
+'<div class="sf-np-qd">'+sfNpFmt(secs)+'</div></div>';
}
box.innerHTML=html;
if(box.getAttribute('data-wired')!=='1'){
box.setAttribute('data-wired','1');
box.addEventListener('click',function(e){
var r=e.target&&e.target.closest?e.target.closest('.sf-np-qrow'):null;
if(!r)return;
sfNpJump(parseInt(r.getAttribute('data-idx'),10));
});
}
}
/* Jumping to a queued track, the only way that actually works here.

   Commanding our own session does NOT work: POST
   Sessions/{id}/Playing?playCommand=PlayNow returns **204** and jellyfin-web
   simply ignores a play command addressed to itself (verified -- request sent,
   correct session id, track unchanged). playbackManager is not on window either.

   What does work is the mechanism everything else here uses: play a real item
   through a card. So the remainder of the queue is written to one scratch
   playlist and that is played -- measured 512ms to create, and it jumped from
   "Hate You" to the track at index 5 with the rest queued behind it.

   The playlist is REUSED (deleted and rewritten each jump) rather than
   accumulating, and its name starts with "__" so sfPlaylistRow hides it. */
var sfNpScratch=null,sfNpJumping=false;
function sfNpJump(idx){
var ac=window.ApiClient,L=sfNpQ.items||[];
if(!ac||sfNpJumping||idx<0||idx>=L.length)return;
if(idx===0)return;                                  /* already the current track */
var ids=[],i;
for(i=idx;i<L.length&&ids.length<200;i++)ids.push(L[i].Id);
if(!ids.length)return;
sfNpJumping=true;
var uid=ac.getCurrentUserId();
function build(){
return ac.ajax({type:'POST',url:ac.getUrl('Playlists'),
data:JSON.stringify({Name:'__np_queue',Ids:ids,UserId:uid,MediaType:'Audio'}),
contentType:'application/json',dataType:'json'});
}
/* Remembering the id only covers THIS page load, so a second visit made a second
   __np_queue and they piled up (observed: two of them). On the first jump of a
   session, sweep every playlist with that name -- after which the remembered id
   is enough. Self-healing, and costs one extra request once per session. */
var pre;
if(sfNpScratch){
pre=ac.ajax({type:'DELETE',url:ac.getUrl('Items/'+sfNpScratch)}).catch(function(){});
}else{
pre=ac.getJSON(ac.getUrl('Users/'+uid+'/Items',{IncludeItemTypes:'Playlist',
Recursive:true,Limit:100})).then(function(r){
var L=(r&&r.Items)||[],dels=[],i;
for(i=0;i<L.length;i++){
if(String(L[i].Name||'')==='__np_queue')
dels.push(ac.ajax({type:'DELETE',url:ac.getUrl('Items/'+L[i].Id)}).catch(function(){}));
}
return Promise.all(dels);
}).catch(function(){});
}
pre.then(build).then(function(r){
sfNpScratch=(r&&r.Id)||null;
if(sfNpScratch)sfPlayItemViaProxy(sfNpScratch,'Playlist','Audio',true,'play');
sfNpJumping=false;
sfNpQ.at=0;                                        /* force a queue refresh */
}).catch(function(){sfNpJumping=false;});
}
function sfNpFill(){
var d=sfNpEl;if(!d)return;
var kind=d.getAttribute('data-panel')||'';
var box=d.querySelector('.sf-np-panel-in');
if(!box)return;
d.querySelector('.sf-np-tab-lyr').classList.toggle('sf-np-on',kind==='lyrics');
d.querySelector('.sf-np-tab-q').classList.toggle('sf-np-on',kind==='queue');
if(!kind){box.innerHTML='';box.removeAttribute('data-sig');return;}
var cur=sfCurrentTrackId();
if(kind==='lyrics'){
box.classList.add('sf-np-lyrpane');
/* sf-np-lyr-restore (2026-08-24): Lyrics and Up Next SHARE this one box
   (.sf-np-panel-in) -- the queue replaces its innerHTML. The reload below was
   guarded only on the TRACK changing, so returning to Lyrics on the same track
   was a no-op and the queue's markup just stayed on screen. Reproduced exactly:
     tap Lyrics  -> panel h=280 "Yeezy season approaching..."
     tap Up Next -> panel h=85  "On Sight  Ye  2:37"
     tap Lyrics  -> panel h=85  "On Sight  Ye  2:37"   <-- still the queue
   That is the admin's "click lyrics then next up then lyrics again and it breaks".
   Same track is therefore not sufficient: if the box no longer HOLDS lyrics
   (.sf-np-lyrbox, or .sf-np-empty for a track with none), the cached id is
   cleared so the existing load path rebuilds it. */
if(!box.querySelector('.sf-np-lyrbox,.sf-np-empty'))sfNpLyr.id=null;
if(cur&&cur!==sfNpLyr.id)sfNpLyrLoad(cur,box);
return;
}
box.classList.remove('sf-np-lyrpane');
/* sf-np-qskel: resolving the queue takes a round trip to /Sessions and then a
   batch /Items -- measured 1.96s from tap to the first row. The panel showed
   NOTHING for that whole time, which reads as broken (it is exactly what an
   audit flagged as an 'empty Up Next panel with 150 tracks loaded'). Paint
   placeholder rows at the real row height so there is no shift when the real
   ones land. */
if(!box.querySelector('.sf-np-qrow')&&!box.querySelector('.sf-np-qskel')){
var sk='',z;for(z=0;z<7;z++)sk+='<div class="sf-np-qskel"><i class="sf-np-qsa"></i>'
+'<div class="sf-np-qsm"><i class="sf-np-qs1"></i><i class="sf-np-qs2"></i></div></div>';
box.innerHTML=sk;
}
sfNpQueueLoad(box,true);
}
/* driven from the main tick so both panels stay live while open */
function sfNpPanelTick(){
var d=sfNpEl;
if(!d||!sfNpOpen)return;
var kind=d.getAttribute('data-panel')||'';
if(!kind)return;
var box=d.querySelector('.sf-np-panel-in');
if(!box)return;
if(kind==='lyrics'){
var cur=sfCurrentTrackId();
if(cur&&cur!==sfNpLyr.id){sfNpLyrLoad(cur,box);return;}
sfNpLyrSync(box);
return;
}
sfNpQueueLoad(box,false);
}
function sfNpSync(force){
var d=sfNpEl;
var bar=sfNpBar();
/* no bar means nothing is playing -- never leave the overlay stranded */
if(!bar){if(d&&sfNpOpen)sfNpSetOpen(false);return;}
if(!d)return;
if(!sfNpOpen&&!force)return;
var img=bar.querySelector('.nowPlayingImage,.nowPlayingBarImage,[class*=nowPlayingImage]');
var art='';
if(img){var m=/url\(["']?(.*?)["']?\)/.exec(img.style.backgroundImage||'');art=m?m[1]:'';}
if(!art){var im2=bar.querySelector('img');if(im2&&im2.src)art=im2.src;}
if(art&&art!==sfNpArt){
sfNpArt=art;
var a1=d.querySelector('.sf-np-art'),b1=d.querySelector('.sf-np-bg');
if(a1)a1.style.backgroundImage='url("'+art+'")';
if(b1)b1.style.backgroundImage='url("'+art+'")';
sfAccentFor(art,function(rgb){
if(!rgb)return;
d.style.setProperty('--sf-np-a','rgb('+rgb[0]+','+rgb[1]+','+rgb[2]+')');
d.style.setProperty('--sf-np-a60','rgba('+rgb[0]+','+rgb[1]+','+rgb[2]+',.6)');
d.style.setProperty('--sf-np-a25','rgba('+rgb[0]+','+rgb[1]+','+rgb[2]+',.25)');
});
}
/* Take the CHILD lines, never the container: .nowPlayingBarText's own
   textContent is both lines run together, which rendered the title as
   "Crave YouKayleigh Rose". */
var wrap=bar.querySelector('.nowPlayingBarText');
var texts=wrap?wrap.querySelectorAll(':scope > div'):[];
if(!texts.length&&wrap)texts=wrap.children;
var t1='',t2='';
if(texts&&texts.length){
t1=(texts[0].textContent||'').trim();
if(texts.length>1)t2=(texts[1].textContent||'').trim();
}
var tt=d.querySelector('.sf-np-title'),ta=d.querySelector('.sf-np-artist');
if(tt&&tt.textContent!==t1)tt.textContent=t1;
if(ta&&ta.textContent!==t2)ta.textContent=t2;
var au=sfNpAudio();
var pb=d.querySelector('.sf-np-play .material-icons');
var playing=!!(au&&!au.paused);
'''

# _LS_11 (orig L7253-7891) -- sf-np-flicker, sf-np-typeflash, sf-mixes
_LS_11 = r'''/* sf-np-flicker (2026-08-21). The admin: the full-screen audiobook player "keeps
   flickering". Every line below used to assign unconditionally on each tick,
   and assigning textContent REPLACES the text node even when the string is
   identical -- so the browser tore down and rebuilt these nodes several times a
   second for no change at all.

   Counted with a MutationObserver over 10s inside .sf-np, while nothing but the
   clock was moving:
     25x  the play/pause ICON node replaced
     25x  the elapsed-time node replaced
     25x  the DURATION node replaced -- a value that never changes
     14x  the speed button's contents replaced
     28x  the rate label's class rewritten
     14x  the root .sf-np class attribute rewritten
   Writing only on a real change takes all of these to zero while idle. */
if(pb&&pb.textContent!==(playing?'pause':'play_arrow'))pb.textContent=playing?'pause':'play_arrow';
if(au&&isFinite(au.duration)&&au.duration>0){
if(!sfNpSeek){
var r=d.querySelector('.sf-np-range');
var rv=String(Math.round((au.currentTime/au.duration)*1000));
if(r&&r.value!==rv)r.value=rv;
}
var cu=d.querySelector('.sf-np-cur'),du=d.querySelector('.sf-np-dur');
var cv=sfNpFmt(au.currentTime),dv=sfNpFmt(au.duration);
if(cu&&cu.textContent!==cv)cu.textContent=cv;
if(du&&du.textContent!==dv)du.textContent=dv;
}
if(d.classList.contains('sf-np-playing')!==playing)d.classList.toggle('sf-np-playing',playing);
}
/* the capsule itself is the way in -- tapping the artwork or the track text
   opens the full player, exactly like both reference apps */
function sfNpWire(){
var bar=sfNpBar();
if(!bar||bar.getAttribute('data-sf-np')==='1')return;
bar.setAttribute('data-sf-np','1');
bar.addEventListener('click',function(e){
var t=e.target;
if(!t||!t.closest)return;
if(t.closest('button')||t.closest('input')||t.closest('a'))return;   /* real controls win */
e.preventDefault();e.stopPropagation();
sfNpSetOpen(true);
},true);
}
/* sf-np-typeflash: while the player is open, re-ask on the 400ms sweep instead of
   waiting for the audiobook module's own 700ms tick. Only runs while open, so it
   costs nothing the rest of the time. */
function sfNpType(){
var d=sfNpEl;
if(!d||!sfNpOpen)return;
var known=null;
try{if(window.__sfAbSync)known=window.__sfAbSync();}catch(e){}
if(d.classList.contains('sf-np-typing')!==(known===null))d.classList.toggle('sf-np-typing',known===null);
}
function sfNpTick(){
try{sfNpWire();sfNpSync(false);sfNpPanelTick();sfNpType();}catch(e){}
}
/* sf-mixes: "Made for you" -- generated mixes built from THIS library.

   This is the one thing a self-hosted player can do that Spotify structurally
   cannot: the mixes are made of music the household actually owns, with no
   licensing gaps, no ads and nothing promoted into them.

   Definitions come from requestbridge /api/mixes (built nightly by
   build_mixes.py) because ranking genres by size from the browser would mean
   pulling every track -- 3.9MB / 6s on this NAS, measured. The payload here is
   ~3KB.

   Playback is a real Jellyfin MusicGenre item pushed through the existing card
   proxy, so it is genuine radio using the app's own player -- verified live:
   proxy-clicking the Pop genre started "24K Magic". No queue is re-implemented. */
var sfMixData=null,sfMixBusy=false;
function sfMixLoad(){
if(sfMixData!==null||sfMixBusy)return;
sfMixBusy=true;
fetch(bridgeUrl()+'/api/mixes',{headers:{'x-jellyfin-token':sfJfToken()}})
.then(function(r){return r.json();})
.then(function(d){sfMixData=(d&&d.mixes)||[];sfMixBusy=false;})
.catch(function(){sfMixData=[];sfMixBusy=false;});
}
/* the bridge helpers live in another script block, so keep local copies */
function bridgeUrl(){
return (location.port==='8096')
?(location.protocol+'//'+location.hostname+':8099')
:(location.origin+'/requestbridge');
}
function sfJfToken(){
try{if(window.ApiClient&&ApiClient.accessToken)return ApiClient.accessToken();}catch(e){}
try{var c=JSON.parse(localStorage.getItem('jellyfin_credentials')||'{}');
return (c.Servers&&c.Servers[0]&&c.Servers[0].AccessToken)||'';}catch(e){return '';}
}
function sfMixRow(){
if((location.hash||'').indexOf('#/music')!==0)return;
var pane=sfActivePane();
if(!pane||pane.getAttribute('data-index')!=='1')return;
sfMixLoad();
if(!sfMixData||!sfMixData.length)return;
if(pane.querySelector('.sf-mixrow'))return;
/* sf-mood-mixes: moods are a Radio shelf, not a Home row. "Made for you" is
   about genre and era; folding five mood mixes in would make it 15 cards of
   two different ideas. */
var sfMixHome=[],mh;
for(mh=0;mh<sfMixData.length;mh++)if((sfMixData[mh].kind||'')!=='mood')sfMixHome.push(sfMixData[mh]);
if(!sfMixHome.length)return;
var ac=window.ApiClient;
if(!ac||!ac.getCurrentUserId)return;
var sec=document.createElement('div');
sec.className='verticalSection sf-mixrow';
sec.style.order='3';                 /* directly under the hero */
var head=document.createElement('div');
head.className='sectionTitleContainer sectionTitleContainer-cards';
var h2=document.createElement('h2');
h2.className='sectionTitle sectionTitle-cards';
h2.textContent='Made for you';
head.appendChild(h2);
sec.appendChild(head);
var row=document.createElement('div');
row.className='sf-mix-row';
var i,j;
for(i=0;i<sfMixHome.length;i++){
(function(m){
var card=document.createElement('div');
card.className='sf-mix-card';
card.setAttribute('data-mix',m.key);
var grid=document.createElement('div');
grid.className='sf-mix-grid';
/* a 2x2 of real covers from the mix -- the same way both reference apps
   illustrate a generated playlist. One cover repeats if the genre is thin. */
var art=(m.art&&m.art.length)?m.art:[];
for(j=0;j<4;j++){
var cell=document.createElement('div');
cell.className='sf-mix-cell';
if(art.length){
var aid=art[j%art.length],url='';
try{url=ac.getImageUrl(aid,{type:'Primary',maxWidth:220});}catch(e){url='';}
if(url)cell.style.backgroundImage='url("'+url+'")';
}
grid.appendChild(cell);
}
var play=document.createElement('button');
play.type='button';
play.className='sf-mix-play';
play.title='Play '+m.label;
play.innerHTML='<span class="material-icons" aria-hidden="true">play_arrow</span>';
grid.appendChild(play);
var lab=document.createElement('div');
lab.className='sf-mix-label';
lab.textContent=m.label;
var sub=document.createElement('div');
sub.className='sf-mix-sub';
sub.textContent=m.sub||'';
card.appendChild(grid);card.appendChild(lab);card.appendChild(sub);
/* sf-tap-lost (2026-08-21). A plain click listener loses roughly one tap in
   six on a phone. Measured over 8 cold loads on a 412px viewport: 7 played,
   and on the 8th a capture-phase counter on the card recorded ZERO click
   events -- the handler never ran at all, so no amount of retrying inside the
   play path could have saved it.

   Cause is the row itself: .sf-mix-row is a horizontal scroller, and a touch
   the browser decides might become a drag is consumed as a scroll gesture, so
   no click is ever synthesised. The card looks unresponsive for no visible
   reason, which is exactly the "sometimes it just does nothing" complaint.

   Fix: treat a touch that did not travel as a tap, using touchend directly, and
   suppress the click that may still follow so a mix can never start twice. */
(function(){
var sx=0,sy=0,st=0,handled=0;
card.addEventListener('touchstart',function(e){
var t=e.touches&&e.touches[0];
sx=t?t.clientX:0; sy=t?t.clientY:0; st=Date.now();
},{passive:true});
card.addEventListener('touchend',function(e){
var t=e.changedTouches&&e.changedTouches[0];
if(!t)return;
/* a real tap: under 10px of travel and under 700ms on screen */
if(Math.abs(t.clientX-sx)>10||Math.abs(t.clientY-sy)>10)return;
if(Date.now()-st>700)return;
handled=Date.now();
e.preventDefault();
sfMixPlay(m);
});
card.addEventListener('click',function(e){
e.preventDefault();e.stopPropagation();
if(Date.now()-handled<1200)return;   /* touchend already started it */
sfMixPlay(m);
});
})();
row.appendChild(card);
})(sfMixHome[i]);
}
sec.appendChild(row);
pane.appendChild(sec);
}
function sfMixPlay(m){
if(!m)return;
/* Plays the CURATED playlist, not the genre item. A MusicGenre takes every
   tagged track, and the tags in this library are far too loose for that to be a
   mix: one Taylor Swift country song carries 17 genres including Trance and
   Ambient, which put 92 of her tracks into "Electronic". build_mixes.py filters
   on genre RANK and caps per artist, then writes the result as a real playlist --
   verified: Electronic went 282 -> 110 tracks with 0 Taylor Swift. */
var id=m.playlistId||m.id;
if(!id)return;
if(!sfPlayItemViaProxy(id,m.playlistId?'Playlist':'MusicGenre','Audio',true,'play')){
location.hash='#/music';
}
}
/* sf-music-solo: Music stops being "a library page with an extra bar on top".

   Every other library page stacks our main pills (Home / Live TV / Sports / My
   Stuff) ABOVE Jellyfin's own tab strip. On Music that meant a 171px header on a
   412px phone against 117px elsewhere, and the strip clipped "Songs". Tucking it
   on scroll helped, but the honest fix is that Music is a DESTINATION, not a
   sub-page: its own tabs are the header, the way Apple Music and Spotify present
   themselves.

   So on #/music the upper bar is hidden and a Home button appears next to the
   back arrow, which keeps a one-tap way out (Home is where every other section
   lives). Hidden with CSS rather than by removing the node, so sfMainNav keeps
   full ownership of the bar and the two cannot fight. */
/* sf-music-solo-sync: the class that hides the main pill bar on Music was only
   toggled from the 400ms tick, so the bar we deliberately remove was PAINTED for
   up to 400ms on every entry to Music -- the flash the admin kept seeing. The class
   test itself is pure and cheap, so it is split out and driven from hashchange
   (which fires before the new page paints) and from the 30ms strip as a backstop.
   sfMusicSolo still owns the Home button, which needs the DOM. */
function sfMusicSoloClass(){
document.documentElement.classList.toggle('sf-music-solo',
  (location.hash||'').indexOf('#/music')===0);
}
function sfMusicSolo(){
var on=(location.hash||'').indexOf('#/music')===0;
sfMusicSoloClass();
var head=document.querySelector('.skinHeader .headerLeft')||document.querySelector('.skinHeader');
if(!head)return;
var btn=head.querySelector('.sf-home-btn');
if(!on){if(btn&&btn.parentNode)btn.parentNode.removeChild(btn);return;}
if(btn)return;
btn=document.createElement('button');
btn.type='button';
btn.className='sf-home-btn headerButton headerButtonLeft paper-icon-button-light';
btn.title='Home';
btn.innerHTML='<span class="material-icons" aria-hidden="true">home</span>';
btn.addEventListener('click',function(e){
e.preventDefault();e.stopPropagation();
location.hash='#/home';
});
/* right after the back arrow, which is where a "leave this section" control is
   expected; falls back to the front of the header if that button is absent */
var back=head.querySelector('.headerBackButton');
if(back&&back.parentNode===head)head.insertBefore(btn,back.nextSibling);
else head.insertBefore(btn,head.firstChild);
}
function sfMusicHome(){
/* Wait for the hero. Measured on a cold home load: this fired at ~1385ms and
   took 1380ms, landing on the exact instant Media Bar was querying its own
   items -- two heavy queries hitting a NAS that answers them serially, so the
   artwork filling the screen finished behind a row nobody had scrolled to yet.
   __sfHeroPainted is set by the first backdrop's load event and, failing that,
   by a 2.5s timer in sf-hero-srccap, so this can defer but never strand. */
if(!window.__sfHeroPainted&&(location.hash||'').indexOf('#/home')===0)return;
if(location.hash.indexOf('#/music')!==0)return;
var pane=sfActivePane();
if(!pane||pane.getAttribute('data-index')!=='1')return;
var kids=[],i,c=pane.children;
for(i=0;i<c.length;i++)if(/verticalSection/.test(c[i].className||''))kids.push(c[i]);
if(!kids.length)return;
if(pane.style.display!=='flex'){pane.style.display='flex';pane.style.flexDirection='column';}
var s,t,tt,o,nat=0;
for(i=0;i<kids.length;i++){
s=kids[i];
/* our own sections set their own order in sfMusicFeature -- without this they
   fall through to the '9' default below and land at the bottom of the page */
if(/sf-mus-artists|sf-mus-discover|sf-mus-simrow|sf-mus-liked|sf-mus-hero|sf-mus-playlists|sf-mixrow|sf-mus-newalb/.test(s.className||''))continue;
t=s.querySelector('.sectionTitle');
tt=(t?t.textContent:'').toLowerCase();
o='11';
if(/favoriteSections/.test(s.className||''))o='11';
/* sf-mus-discover shifted these by one to open slot 5 for the discover row. */
else if(tt.indexOf('recently played')>-1)o='7';
else if(tt.indexOf('frequently played')>-1)o='8';
else if(tt.indexOf('recently added')>-1)o='9';
else{
/* sf-music-order-i18n: those three tests match ENGLISH titles, so every other
   language fell straight through to '9' and the shelves came out in raw DOM
   order -- which puts "Recently Added" FIRST. On this server that shelf is the
   entire library (196 of 196 albums are under 30 days old), so the least useful
   shelf led the page for exactly the users who already struggle with it.
   Measured: en ordered 5,6,7; de and zh-CN both ordered 9,9,9.
   Jellyfin renders these shelves in a fixed DOM sequence -- Recently Added,
   Recently Played, Frequently Played -- and that sequence is identical in every
   language, so fall back to position. favoriteSections is matched by CLASS
   above and deliberately does not consume a position. */
o=['9','7','8'][nat]||'11';
nat++;
}
if(s.style.order!==o)s.style.order=o;
/* sf-mus-dupadd (2026-08-27): slot 8 is Jellyfin's "Recently Added Music", and
   it is the SAME QUERY as our own "New in your library" shelf at slot 5 --
   MusicAlbum by DateCreated. Measured live: both rows led with Who Wants to
   Live Forever, EVOLution, Tastes Like Summer, The User's Guide, Damn the
   Torpedoes, Foreign Tongues, in that order. Two identical shelves, and the
   Jellyfin one renders worse (lazy art that was still blurred when the page
   had settled, no artist line). Hide it and keep ours.
   Keyed off the resolved slot, not the English title, so the positional
   fallback above covers de/zh too. */
if(o==='9')s.classList.add('sf-mus-dupadd');
else s.classList.remove('sf-mus-dupadd');
/* the favourites block's heading is bare "Albums", which reads as a second
   albums row next to the real one */
/* Key the rename off the CLASS, never the order number. This originally read
   o==='5' because favourites was 5 -- then the row order was renumbered twice to
   make room for the hero, artists and playlists, and '5' became Recently Played,
   so the code cheerfully retitled "Recently Played" as "Favorite Albums". The
   class is what actually identifies the section. */
if(/favoriteSections/.test(s.className||'')&&t&&!/favou?rite/i.test(t.textContent))
t.textContent='Favorite Albums';
}
if(!pane.querySelector('.sf-mus-greet')){
var h=new Date().getHours();
var greet=(h<12)?'Good morning':((h<18)?'Good afternoon':'Good evening');
var name='';
try{name=(window.ApiClient&&ApiClient._currentUser&&ApiClient._currentUser.Name)||'';}catch(e){}
var g=document.createElement('div');
g.className='sf-mus-greet padded-left';
g.style.order='1';
var h1=document.createElement('h1');
h1.className='sf-mus-greet-title';
h1.textContent=greet+(name?(', '+name):'');
var sub=document.createElement('div');
sub.className='sf-mus-greet-sub';
sub.textContent='Pick up where you left off';
g.appendChild(h1);g.appendChild(sub);
pane.insertBefore(g,pane.firstChild);
}
}
/* ---- sf-mus-nav (2026-08-27) ----------------------------------------------
   Home | New | Radio | Library, after the admin asked for the shape Apple Music and
   Spotify use.

   The thing their tab bars are actually doing is splitting a CATALOGUE you do
   not own from a LIBRARY you do: Home/New/Radio browse tens of millions of
   tracks, Library is your collection. This server has only the library half, so
   a literal copy would promote two tabs that repeat rows already on Home and
   bury the four axes that actually browse 200 albums. What carries over is the
   grouping: Albums/Artists/Songs/Playlists are ONE idea and were eating four of
   five slots, and collapsing them frees room for Radio, which is a destination
   we genuinely did not have.

   Jellyfin maps a tab to its pane by data-index and that mapping is load-bearing
   (see sf-music-ux), so nothing is renumbered and no node is moved:
     - data-index 1 keeps the landing pane, relabelled Home
     - data-index 0 keeps the Albums pane, relabelled Library, and carries a
       sub-pill row that clicks the now-hidden native buttons for 2/4/5
     - New and Radio are extra buttons that activate pane 1 and swap what it
       renders, the same mechanism as My Stuff's Favorites/Watchlist pills
   Everything is re-asserted on the 400ms tick, so a Jellyfin re-render of the
   strip repairs itself. */
var sfMusView='home', sfNewPg=null, sfNewPgBusy=false;
/* sf-sim-stations: Jellyfin's /Items/{id}/Similar works on MusicArtist and
   returns artists from THIS library, which is the whole point -- everything it
   suggests is playable. Verified quality: Coldplay -> Keane, Snow Patrol, The
   Cranberries, The Script, OneRepublic; Queen -> Fleetwood Mac, Foreigner, Tom
   Petty, Kings of Leon. Thin for hip-hop (Tyler and Post Malone return 2 each),
   so the row is dropped rather than shown nearly empty. One request, seeded
   from the most played artist. */
var sfSimData=null, sfSimBusy=false, sfSimSeed='';
var sfLikedData=null, sfLikedBusy=false;
var sfDiscSeed=null, sfDiscBusy=false;
/* sf-discover-unblock: off the critical path on purpose -- see the note in
   sfMusicFeature. Everything else on the page renders without it. */
function sfDiscoverLoad(ac,uid){
if(!sfDiscSeed||sfDiscBusy||(sfMfData&&sfMfData.discover))return;
sfDiscBusy=true;
ac.getJSON(ac.getUrl('Users/'+uid+'/Items',{IncludeItemTypes:'MusicAlbum',Recursive:true,
Limit:500,SortBy:'SortName',Fields:'AlbumArtist'}))
.then(function(r){
sfDiscBusy=false;
var albs=(r&&r.Items)||[],byArt={},ab;
for(ab=0;ab<albs.length;ab++){
var an=albs[ab].AlbumArtist||'';
if(!an)continue;
(byArt[an]=byArt[an]||[]).push(albs[ab]);
}
var names=sfDiscSeed.names,played=sfDiscSeed.played,disc=null,dn;
for(dn=0;dn<names.length&&!disc;dn++){
var owned=byArt[names[dn]]||[],fresh=[],ow;
for(ow=0;ow<owned.length;ow++)if(!played[owned[ow].Id])fresh.push(owned[ow]);
if(fresh.length>=3)disc={artist:names[dn],albums:fresh.slice(0,16)};
}
if(sfMfData)sfMfData.discover=disc;
try{sfMusicFeature();}catch(e){}
})
.catch(function(){sfDiscBusy=false;});
}
/* Declared HERE, not next to sfMusLibPills where it is mostly used: `var`
   hoists the binding but not the value, so sfMusicTabs -- which runs first on
   the tick -- would have read undefined and thrown on .length. */
var SFLIB=[['0','Albums'],['2','Artists'],['5','Songs'],['4','Playlists']];
function sfMusT(k){try{return window.sfTr?window.sfTr(k):k;}catch(e){return k;}}
function sfMusBar(){
var bars=document.querySelectorAll('.tabs-viewmenubar .emby-tabs-slider'),i;
for(i=0;i<bars.length;i++)if(bars[i].querySelector('.emby-tab-button[data-index]'))return bars[i];
return null;
}
function sfMusSetView(v,quiet){
sfMusView=v;
document.documentElement.setAttribute('data-sf-musview',v);
/* sf-subpill-url, same reasoning: replaceState, never a hash assignment --
   assigning would re-enter Jellyfin's router and re-render the whole page. */
if(!quiet){try{var b='#/music?tab=1';history.replaceState(null,'',v==='home'?b:b+'&view='+v);}catch(e){}}
try{sfMusicTabs();sfMusPages();}catch(e){}
}
function sfMusNavBtn(bar,view,en,order){
var b=bar.querySelector('.sf-mus-navbtn[data-sf-view="'+view+'"]');
if(!b){
b=document.createElement('button');
b.type='button';
b.setAttribute('is','emby-button');
b.className='emby-tab-button emby-button sf-mus-navbtn';
b.setAttribute('data-sf-view',view);
b.appendChild(document.createElement('div')).className='emby-button-foreground';
b.addEventListener('click',function(e){
e.preventDefault();e.stopPropagation();
/* activate the landing pane first if we are somewhere else, then swap the
   view. Clicking the native button is what makes Jellyfin do its own pane
   bookkeeping -- we never touch .is-active ourselves. */
var home=sfMusBar()&&sfMusBar().querySelector('.emby-tab-button[data-index="1"]');
if(home&&!home.classList.contains('emby-tab-button-active'))home.click();
sfMusSetView(view);
});
bar.appendChild(b);
}
if(b.style.order!==order)b.style.order=order;
var fg=b.querySelector('.emby-button-foreground'),want=sfMusT(en);
if(fg.textContent!==want)fg.textContent=want;
return b;
}
function sfMusicTabs(){
if(location.hash.indexOf('#/music')!==0)return;
var bar=sfMusBar();
if(!bar)return;
/* the slider ships display:block, so it has to become flex for order to mean
   anything; centring is restated because block layout centred by other means */
if(bar.style.display!=='flex'){
bar.style.display='flex';
bar.style.justifyContent='center';
bar.style.alignItems='center';}
/* pick the view up from the URL once, so a reload or a shared link comes back
   to the same place */
if(!bar.getAttribute('data-sf-navinit')){
bar.setAttribute('data-sf-navinit','1');
var h=location.hash||'';
if(h.indexOf('view=radio')>-1)sfMusSetView('radio',true);
else if(h.indexOf('view=new')>-1)sfMusSetView('new',true);
else sfMusSetView('home',true);
/* Pressing the native Home tab leaves whichever custom view is showing.
   e.isTrusted is load-bearing, not a nicety: clicking one of our buttons makes
   Jellyfin's own emby-tabs component RE-ASSERT the active tab by dispatching a
   click on a native button, and without this guard that synthetic click was
   read as "the user left" and snapped the view straight back to home. Traced
   with a MutationObserver on the attribute -- the sequence was
   attr=new -> attr=home inside a single user click, with no error to show for
   it. A real tap is trusted; a dispatched one never is.
   Leaving to any OTHER pane is handled declaratively below, off the active
   pane, so it cannot depend on catching a click at all. */
bar.addEventListener('click',function(e){
if(!e.isTrusted)return;
var t=e.target&&e.target.closest?e.target.closest('.emby-tab-button'):null;
if(!t||t.classList.contains('sf-mus-navbtn'))return;
if(t.getAttribute('data-index')!=='1')return;
if(sfMusView!=='home')sfMusSetView('home');
},true);
}
/* A custom view only exists on the landing pane. If anything has moved us off
   it -- the Library tab, a sub-pill, a deep link, Jellyfin restoring a
   remembered tab -- the view is home again by definition. Declarative, so it
   does not rely on observing the click that caused it. */
var actv=sfActivePane();
if(actv&&actv.getAttribute('data-index')!=='1'&&sfMusView!=='home')sfMusSetView('home',true);
var nat={'1':{o:'1',t:'Home'},'0':{o:'4',t:'Library'}};
var btns=bar.querySelectorAll('.emby-tab-button[data-index]'),i,b,idx,fg,want;
for(i=0;i<btns.length;i++){
b=btns[i];idx=b.getAttribute('data-index');
if(nat[idx]){
b.classList.remove('sf-mus-tabhide');
if(b.style.order!==nat[idx].o)b.style.order=nat[idx].o;
fg=b.querySelector('.emby-button-foreground')||b;
want=sfMusT(nat[idx].t);
if(fg.textContent!==want)fg.textContent=want;
}else{
/* Artists(2), the duplicate Artists(3), Playlists(4), Songs(5) and Genres(6)
   are reached from the Library sub-pills now. Hidden, never removed --
   Jellyfin clicks these very buttons to switch panes. */
b.classList.add('sf-mus-tabhide');
}
}
sfMusNavBtn(bar,'new','New','2');
sfMusNavBtn(bar,'radio','Radio','3');
/* Active pill. Jellyfin owns emby-tab-button-active and sets it on the native
   button it just activated; on a custom view that is Home, which would leave
   two tabs looking selected. Re-pointed here every tick, and synchronously
   inside our own click handler, so there is no frame where it is wrong. */
/* Library stays lit on Artists / Songs / Playlists. Those panes are reached
   through the sub-pills, and Jellyfin marks THEIR buttons active -- which are
   the ones we hide, so the top bar ended up with nothing selected at all.
   A class, not the active class, so Jellyfin's own state is left alone. */
var libB=bar.querySelector('.emby-tab-button[data-index="0"]');
if(libB){
var ai=actv?actv.getAttribute('data-index'):null,inLib=false,li;
for(li=0;li<SFLIB.length;li++)if(SFLIB[li][0]===ai)inLib=true;
if(libB.classList.contains('sf-mus-libsel')!==inLib)
libB.classList.toggle('sf-mus-libsel',inLib);
}
var homeB=bar.querySelector('.emby-tab-button[data-index="1"]');
var onLanding=!!(homeB&&homeB.classList.contains('emby-tab-button-active'));
var navs=bar.querySelectorAll('.sf-mus-navbtn'),k,want2;
for(k=0;k<navs.length;k++){
want2=onLanding&&sfMusView!=='home'&&navs[k].getAttribute('data-sf-view')===sfMusView;
if(navs[k].classList.contains('emby-tab-button-active')!==want2)
navs[k].classList.toggle('emby-tab-button-active',want2);
}
/* The native Home button KEEPS emby-tab-button-active while a custom view is
   showing, and is only made to LOOK unselected (see sf-mus-nav in branding).
   Stripping the class here was the first attempt and it broke the Library tab
   outright: Jellyfin's emby-tabs component reads its current tab back out of
   the DOM, so with no button marked active a click on Library did nothing at
   all -- the pane stayed on suggestionsTab and the press was simply swallowed.
   Never take away state a component owns to change how it looks. */
}
/* ---- Library sub-pills ----------------------------------------------------
   Albums | Artists | Songs | Playlists, plus the + that creates one. Rendered
   into each of those four panes and wired to click the hidden native buttons,
   so pane switching stays entirely Jellyfin's. Styling mirrors jf-fav-tabs so
   the two sub-navs in the app read as one control. */
function sfMusLibPills(){
if(location.hash.indexOf('#/music')!==0)return;
var pane=sfActivePane();
if(!pane)return;
var idx=pane.getAttribute('data-index');
var mine=false,i;
for(i=0;i<SFLIB.length;i++)if(SFLIB[i][0]===idx)mine=true;
if(!mine)return;
if(pane.querySelector('.sf-lib-pills'))
{sfMusLibMark(pane,idx);return;}
var bar=document.createElement('div');
bar.className='sf-lib-pills';
for(i=0;i<SFLIB.length;i++){
(function(rec){
var btn=document.createElement('button');
btn.type='button';
btn.className='sf-lib-pill';
btn.setAttribute('data-sf-lib',rec[0]);
btn.textContent=sfMusT(rec[1]);
btn.addEventListener('click',function(e){
e.preventDefault();e.stopPropagation();
var nb=sfMusBar()&&sfMusBar().querySelector('.emby-tab-button[data-index="'+rec[0]+'"]');
if(nb)nb.click();
});
bar.appendChild(btn);
})(SFLIB[i]);
}
/* + New Playlist. Jellyfin already ships this button on the playlists pane;
   surfacing it on every Library pane is what "Create" would have been as a
   tab, without spending a tab on one action. */
var add=document.createElement('button');
add.type='button';
add.className='sf-lib-pill sf-lib-add';
add.title=sfMusT('New Playlist');
add.innerHTML='<span class="material-icons" aria-hidden="true">add</span>';
add.addEventListener('click',function(e){
e.preventDefault();e.stopPropagation();
var nb=sfMusBar()&&sfMusBar().querySelector('.emby-tab-button[data-index="4"]');
if(nb)nb.click();
setTimeout(function(){
var p=sfActivePane();
var b=p&&(p.querySelector('.sf-plnew-btn')||p.querySelector('button.raised, .btnNewPlaylist'));
if(b)b.click();
},450);
});
bar.appendChild(add);
pane.insertBefore(bar,pane.firstChild);
sfMusLibMark(pane,idx);
}
function sfMusLibMark(pane,idx){
var ps=pane.querySelectorAll('.sf-lib-pill[data-sf-lib]'),i,on;
for(i=0;i<ps.length;i++){
on=ps[i].getAttribute('data-sf-lib')===idx;
if(ps[i].classList.contains('sf-lib-pill-active')!==on)
ps[i].classList.toggle('sf-lib-pill-active',on);
}
}
/* ---- sf-mus-pages: the New and Radio destinations -------------------------
   Both render INTO the landing pane as siblings of its shelves, with CSS
   swapping which of the three is visible off html[data-sf-musview]. That is the
   jf-fav-watchlist mechanism, already proven on My Stuff, and it means Jellyfin
   never has to know these views exist -- no new pane, no data-index to collide
   with, and the pane's own reveal/ordering logic is untouched. */
function sfMusCard(ac,id,title,sub,action,type){
var card=document.createElement('div');
card.className='sf-mus-gcard';
var art=document.createElement('div');
art.className='sf-mus-gart';
var url='';
try{url=ac.getImageUrl(id,{type:'Primary',maxWidth:320});}catch(e){}
if(url)art.style.backgroundImage='url("'+url+'")';
var play=document.createElement('button');
play.type='button';
play.className='sf-mus-gplay';
play.title=sfMusT(action==='play'?'Play':'Radio');
play.innerHTML='<span class="material-icons" aria-hidden="true">'+
(action==='play'?'play_arrow':'radio')+'</span>';
play.addEventListener('click',function(e){
e.preventDefault();e.stopPropagation();
if(action==='noop')return;                 /* the caller wires its own */
if(action==='instantmix')sfMix(id,type||'MusicArtist');
else sfPlayItemViaProxy(id,type||'MusicAlbum','Audio',true,'play');
});
art.appendChild(play);
var t=document.createElement('div');t.className='sf-mus-gname';t.textContent=title||'';
var s=document.createElement('div');s.className='sf-mus-gsub';s.textContent=sub||'';
card.appendChild(art);card.appendChild(t);if(sub)card.appendChild(s);
if(action==='instantmix'){
/* A station tile is ONE action. This used to fall through to the navigate
   branch below, so tapping anywhere on an "Artist stations" card opened the
   artist page and only the small radio button actually started anything --
   verified by intercepting /Items/{id}/InstantMix: a card-body click produced
   no request at all, the button produced the right one. Both references treat
   a station tile as a single target, and there is no useful detail page for a
   station anyway. */
card.addEventListener('click',function(e){
e.preventDefault();e.stopPropagation();
sfMix(id,type||'MusicArtist');
});
}else if(action!=='noop'){
card.addEventListener('click',function(){location.hash='#/details?id='+id;});
}
return card;
}
'''

# _LS_12 (orig L7891-8696) -- sf-mood-mixes, sf-hero-epid2, sf-hero-nojitter
_LS_12 = r'''/* sf-mood-mixes: the mix cards, built from a list rather than straight off
   sfMixData, so genre/decade mixes and mood mixes can be two shelves. They are
   the same object shape -- build_mixes.py writes both, tagged by `kind`. */
function sfMixGrid(ac,list){
var g=document.createElement('div');g.className='sf-mus-grid';
for(var j=0;j<list.length;j++){
(function(m){
var c=document.createElement('div');c.className='sf-mus-gcard';
var art=document.createElement('div');art.className='sf-mus-gart sf-mus-gart-mix';
var cov=(m.art&&m.art.length)?m.art:[];
for(var q=0;q<4;q++){
var cell=document.createElement('div');cell.className='sf-mix-cell';
if(cov.length){var u='';try{u=ac.getImageUrl(cov[q%cov.length],{type:'Primary',maxWidth:220});}catch(e){}
if(u)cell.style.backgroundImage='url("'+u+'")';}
art.appendChild(cell);
}
var pb=document.createElement('button');pb.type='button';pb.className='sf-mus-gplay';
pb.innerHTML='<span class="material-icons" aria-hidden="true">play_arrow</span>';
art.appendChild(pb);
var t=document.createElement('div');t.className='sf-mus-gname';t.textContent=m.label||'';
var sb=document.createElement('div');sb.className='sf-mus-gsub';sb.textContent=m.sub||'';
c.appendChild(art);c.appendChild(t);c.appendChild(sb);
c.addEventListener('click',function(e){e.preventDefault();e.stopPropagation();sfMixPlay(m);});
g.appendChild(c);
})(list[j]);
}
return g;
}
function sfMusSection(cls,title){
var sec=document.createElement('div');
sec.className='sf-mus-page '+cls;
var h=document.createElement('h2');
h.className='sectionTitle sectionTitle-cards sf-mus-pagetitle';
h.textContent=title;
sec.appendChild(h);
return sec;
}
function sfMusPages(){
if(location.hash.indexOf('#/music')!==0)return;
var pane=sfActivePane();
if(!pane||pane.getAttribute('data-index')!=='1')return;
var ac=window.ApiClient;
if(!ac||!ac.getCurrentUserId)return;
var uid=ac.getCurrentUserId();
if(!uid)return;

/* ---- New: every recently added album, as a grid rather than a row. The Home
   shelf shows 16 and scrolls; this is the whole thing. */
if(sfMusView==='new'&&!pane.querySelector('.sf-mus-page-new')){
if(sfNewPg===null){
if(!sfNewPgBusy){
sfNewPgBusy=true;
ac.getJSON(ac.getUrl('Users/'+uid+'/Items',{IncludeItemTypes:'MusicAlbum',Recursive:true,
Limit:120,SortBy:'DateCreated',SortOrder:'Descending',Fields:'DateCreated'}))
.then(function(r){sfNewPg=(r&&r.Items)||[];sfNewPgBusy=false;try{sfMusPages();}catch(e){}})
.catch(function(){sfNewPg=[];sfNewPgBusy=false;});
}
}else{
var ns=sfMusSection('sf-mus-page-new',sfMusT('Recently added'));
ns.style.order='2';
var ng=document.createElement('div');ng.className='sf-mus-grid';
for(var i=0;i<sfNewPg.length;i++){
var a=sfNewPg[i];
ng.appendChild(sfMusCard(ac,a.Id,a.Name||'',a.AlbumArtist||'','play','MusicAlbum'));
}
ns.appendChild(ng);
pane.appendChild(ns);
}
}

/* ---- Radio: the curated mixes as full cards, plus a station for each artist
   you actually listen to. Both already existed as machinery -- build_mixes.py's
   playlists and sfMix's instantmix proxy -- and neither had a home of its own. */
if(sfMusView==='radio'&&!pane.querySelector('.sf-mus-page-radio')){
try{sfMixLoad();}catch(e){}
/* Built in ONE pass once everything it needs has settled, rather than appended
   to as each source lands -- the page is above the fold and a shelf arriving
   late is the same flicker sf-hero-oneshot removed from the hero. */
if(sfMfData===null)return;
var seedArt=(sfMfData.artists&&sfMfData.artists[0])||null;
if(seedArt&&sfSimData===null){
if(!sfSimBusy){
sfSimBusy=true;sfSimSeed=seedArt.name||'';
ac.getJSON(ac.getUrl('Items/'+seedArt.id+'/Similar',{userId:uid,Limit:12}))
.then(function(r){sfSimData=(r&&r.Items)||[];sfSimBusy=false;try{sfMusPages();}catch(e){}})
.catch(function(){sfSimData=[];sfSimBusy=false;try{sfMusPages();}catch(e){}});
}
return;
}
/* split by kind: genre/decade/deep are "Your mixes", the ffmpeg-derived ones
   are "Moods" -- two different ideas and they read as noise in one shelf. */
var mixAll=sfMixData||[],mixPlain=[],mixMood=[],mi;
for(mi=0;mi<mixAll.length;mi++){
if((mixAll[mi].kind||'')==='mood')mixMood.push(mixAll[mi]);else mixPlain.push(mixAll[mi]);
}
var haveMix=mixPlain.length;
var haveMood=mixMood.length;
var haveArt=sfMfData&&sfMfData.artists&&sfMfData.artists.length;
var haveSong=sfMfData&&sfMfData.songs&&sfMfData.songs.length;
/* 3 is the floor for a shelf: two cards reads as a bug, not a row. */
var haveSim=sfSimData&&sfSimData.length>=3;
if(haveMix||haveMood||haveArt){
var rs=sfMusSection('sf-mus-page-radio',sfMusT('Your mixes'));
rs.style.order='2';
if(haveMix)rs.appendChild(sfMixGrid(ac,mixPlain));
if(haveMood){
var hm=document.createElement('h2');
hm.className='sectionTitle sectionTitle-cards sf-mus-pagetitle sf-mus-pagetitle2';
hm.textContent=sfMusT('Moods');
rs.appendChild(hm);
rs.appendChild(sfMixGrid(ac,mixMood));
}
if(haveArt){
var h3=document.createElement('h2');
h3.className='sectionTitle sectionTitle-cards sf-mus-pagetitle sf-mus-pagetitle2';
h3.textContent=sfMusT('Artist stations');
rs.appendChild(h3);
var ag=document.createElement('div');ag.className='sf-mus-grid sf-mus-grid-round';
for(var k=0;k<sfMfData.artists.length;k++){
var ar=sfMfData.artists[k];
ag.appendChild(sfMusCard(ac,ar.id,ar.name||'','','instantmix','MusicArtist'));
}
rs.appendChild(ag);
}
/* ---- Song radio ---- */
if(haveSong){
var h4=document.createElement('h2');
h4.className='sectionTitle sectionTitle-cards sf-mus-pagetitle sf-mus-pagetitle2';
h4.textContent=sfMusT('Song radio');
rs.appendChild(h4);
var sg=document.createElement('div');sg.className='sf-mus-grid';
for(var q2=0;q2<sfMfData.songs.length;q2++){
(function(sn){
/* art comes off the ALBUM: a track's own Primary is usually absent, and the
   cover is what makes the card recognisable anyway. */
var c=sfMusCard(ac,sn.albumId||sn.id,sn.name,sn.artist,'noop','Audio');
var pb=c.querySelector('.sf-mus-gplay');
if(pb)pb.title=sfMusT('Song radio');
/* isFolder FALSE here -- a track is not a container, and sfMix hardcodes
   true because everything else it is called with is. */
function go(e){if(e){e.preventDefault();e.stopPropagation();}
if(!sfPlayItemViaProxy(sn.id,'Audio','Audio',false,'instantmix'))
location.hash='#/details?id='+(sn.albumId||sn.id);}
c.addEventListener('click',go);
if(pb)pb.addEventListener('click',go);
sg.appendChild(c);
})(sfMfData.songs[q2]);
}
rs.appendChild(sg);
}
/* ---- Because you listen to <artist> ---- */
if(haveSim){
var h5=document.createElement('h2');
h5.className='sectionTitle sectionTitle-cards sf-mus-pagetitle sf-mus-pagetitle2';
h5.textContent=sfMusT('Because you listen to')+' '+sfSimSeed;
rs.appendChild(h5);
var mg=document.createElement('div');mg.className='sf-mus-grid sf-mus-grid-round';
for(var z=0;z<sfSimData.length;z++){
var sa=sfSimData[z];
if(!sa||!sa.Id)continue;
mg.appendChild(sfMusCard(ac,sa.Id,sa.Name||'','','instantmix','MusicArtist'));
}
rs.appendChild(mg);
}
pane.appendChild(rs);
}
}
}
function sfSeerrLinks(){
var as=document.querySelectorAll('a[href*=":5055"]:not([data-sf-seerr])'),i,a,card,t;
for(i=0;i<as.length;i++){
a=as[i];
a.setAttribute('data-sf-seerr','1');
card=a.closest?a.closest('.card'):null;
t=card?((card.querySelector('.cardText')||{}).textContent||''):'';
t=t.replace(/\s+/g,' ').trim();
if(!t)continue;
a.setAttribute('href','#/search?query='+encodeURIComponent(t));
a.removeAttribute('target');       /* it opened a new tab as an external link */
}
}
function sfHeroPrefill(){
var sl=document.querySelectorAll('.slide'),i,s,id,key,cw,epi,mins,ov;
for(i=0;i<sl.length;i++){
s=sl[i];
id=s.getAttribute('data-item-id');
if(!id)continue;
key=sfNorm(id);
cw=sfCwMap[key];
epi=(cw&&cw.s!=null)?cw:sfNuMap[key];            /* resumed, else queued next */
mins=0;
if(epi&&epi.rt)mins=Math.round(epi.rt/600000000);               /* the episode */
else if(sfRtMap[key])mins=Math.round(sfRtMap[key]/600000000);   /* the film */
if(mins>0&&s.getAttribute('data-sf-rt')!==mins+'m')s.setAttribute('data-sf-rt',mins+'m');
ov=(epi&&epi.ov)?epi.ov:'';
if(ov&&s.getAttribute('data-sf-plot')!==ov)s.setAttribute('data-sf-plot',ov);
/* sf-hero-epid2: the SECOND writer of data-sf-plot. Stamping the episode id at
   only the other one left every NEXT UP hero untranslatable -- the slide had an
   episode synopsis on it and no way to say which episode. Two writers, same
   attribute: sweep both, exactly like duplicate page instances. */
var eid=(epi&&epi.epId)?epi.epId:'';
if(eid){if(s.getAttribute('data-sf-epid')!==eid)s.setAttribute('data-sf-epid',eid);}
else if(s.getAttribute('data-sf-epid'))s.removeAttribute('data-sf-epid');
}
}
function sfHeroResume(){
var slide=document.querySelector('.slide.active');
if(!slide)return;
var id=slide.getAttribute('data-item-id');
if(!id)return;
if(slide.getAttribute('data-sf-cw')===id)return;
slide.setAttribute('data-sf-cw',id);
/* sf-hero-nojitter: the LAYOUT decision is made HERE, synchronously.
   Everything that changes the height of this card -- the .sf-cw class that
   opens the episode band, the episode line, the progress bar -- used to wait on
   ApiClient.getItem. Measured across two live rotations: the chip row settled
   17-30px late and the description and buttons cascaded 40-122px behind it, all
   over 2.4-3s. That is the "stuff moves around before it settles" -- not a
   positioning bug but a card being laid out twice, once before the reply and
   once after.
   None of it needed the round trip. sfCwMap is built from the resume query and
   already holds season, episode, percent and the episode's runtime -- and a
   Continue Watching slide cannot even EXIST before that map is filled, since
   our fetch wrapper is what merges those items into Media Bar's response. So
   the map is authoritative at the moment a slide activates. */
sfHeroPaint(slide,sfCwMap[sfNorm(id)],null);
/* The item is fetched anyway, for two things that cannot move the layout:
   a film's runtime (text inside a chip that is already placed), and as a
   fallback for a slide sfCwMap does not know about. It may UPGRADE such a slide
   to resumable but never downgrades one -- a late reply must not be able to
   undo a card that has already painted. */
var ac=window.ApiClient;
if(!ac||!ac.getItem)return;
ac.getItem(ac.getCurrentUserId(),id).then(function(it){
if(!it)return;
if(slide.getAttribute('data-sf-cw')!==id)return;   /* slide moved on */
sfHeroPaint(slide,sfCwMap[sfNorm(id)],it);
}).catch(function(){});
}
/* Published for the hero layout block, which lives in a different IIFE and so
   cannot see this name. It calls it BEFORE measuring -- see sf-paint-first. */
window.__sfHeroResume=sfHeroResume;
/* Paints a hero card from whatever is known so far: cw is its Continue Watching
   entry (undefined for a plain recommendation) and it is the full item (null on
   the synchronous first pass). Written to be safely re-runnable -- every write
   is guarded by a comparison, so the second pass with the item in hand is a
   no-op for anything already correct. */
function sfHeroPaint(slide,cw,it){
var ud=(it&&it.UserData)||{};
var pct=0,label='Resume',resumable=false;
var sid=slide.getAttribute('data-item-id');
/* A SERIES slide carries no progress of its own -- the progress belongs to the
   episode it stands for (see sf-hero-cw-source), so read it from sfCwMap. */
if(cw){
if(cw.s!=null&&cw.e!=null){
resumable=true;pct=cw.pct||0;
/* season 0 is Jellyfin's specials bucket -- "S0" is accurate and meaningless to
   a viewer, so name it. Verified present in this library: Attack on Titan S0E7. */
label=(cw.s===0)?('Continue Special '+cw.e):('Continue S'+cw.s+' E'+cw.e);
/* translate HERE, not after the fact -- see sf-tr-export */
try{if(window.sfTr)label=window.sfTr(label);}catch(e){}
}else if(cw.pct>0&&cw.pct<96){
resumable=true;pct=cw.pct;
}
}
/* Fallback for an item the resume query did not cover. >=96% is "basically
   finished" -- Jellyfin itself drops those from Continue Watching, and offering
   Resume 30 seconds from the credits is not useful. */
if(!resumable&&it){
var pos=ud.PlaybackPositionTicks||0,upct=ud.PlayedPercentage||0;
if(pos>0&&upct>0&&upct<96){resumable=true;pct=upct;}
}
/* Next Up applies only when there is nothing to resume -- Continue Watching
   always wins, so a series mid-episode appears once, as a resume card. */
var nu=resumable?null:(sid?sfNuMap[sfNorm(sid)]:null);
/* sf-hero-mobile: the episode line and the progress bar are DESKTOP-only.
   The hero layout bails below MINW (1000px) and clears its row positions, but
   these extras were still being created and positioned, so on a phone they were
   laid out against a hero that had never been arranged for them. Measured at
   414px in real layout-mobile CSS: the episode line overlapped the chip row by
   11px, the bar cut 3px into the episode line, and the whole stack pushed the
   Play button to 670-710px inside a hero that ends at 654 -- i.e. off the bottom
   of the slide and behind the Continue Watching row, leaving the mobile hero
   with NO usable button. Stripping these three things put the button back at
   510-550, inside the hero, with no overlap anywhere.
   Nothing important is lost: the button still says "Continue S2 E3", and the
   Continue Watching row directly below names the episode on every card.
   Defaults to wide when the predicate has not loaded yet, so desktop is never
   downgraded by a race. */
var wide=(typeof window.__jfHeroWide==='function')?window.__jfHeroWide():true;
slide.classList.toggle('sf-cw',!!resumable&&wide);
slide.classList.toggle('sf-nu',!!nu&&wide);
/* The episode this slide stands for, whether resumed or queued up next.
   Everything below reads from this one value so the two tiers cannot drift. */
var epi=(resumable&&cw&&cw.s!=null&&cw.e!=null)?cw:(nu||null);
var bar=slide.querySelector('.sf-cw-prog');
/* sf-hero-runtime: the chip said "Ends at 9:52 PM" on films and "9 Seasons" on
   shows. Neither answers "how long is this?" -- a clock time is only meaningful
   if you start right now, and a season count says nothing about the episode you
   are about to resume. Films get their length in minutes; a resumed show gets
   the length of THAT episode. The value is stashed on the slide and re-applied
   every tick, because Media Bar re-renders this row and would otherwise put its
   own text back. sf-hero-icons keys the chip's glyph off the same attribute:
   with a duration it shows a clock, without one it is still a season count. */
if(slide.querySelector('.runTime')){
var mins=0;
if(epi&&epi.rt)mins=Math.round(epi.rt/600000000);                     /* the episode */
else if(sid&&sfRtMap[sfNorm(sid)])mins=Math.round(sfRtMap[sfNorm(sid)]/600000000);
else if(it&&it.Type==='Movie'&&it.RunTimeTicks)mins=Math.round(it.RunTimeTicks/600000000);
if(mins>0)slide.setAttribute('data-sf-rt',mins+'m');
else if(!it)   {/* nothing known yet. Leave Media Bar's own text rather than
   blanking the chip -- the item reply below fills it in, and an empty chip that
   then pops back is worse than the wrong label for one round trip. */}
else slide.removeAttribute('data-sf-rt');
}
/* sf-hero-ep: on a Continue Watching SERIES slide, say which episode is being
   resumed -- "S1 E9 - La Chica o El Mundo" -- the way Abyss does. It replaces
   the genre line rather than adding a row: Media Bar's hero rows are 9-12px
   apart with nowhere to insert one, and "which episode am I on" beats "Comedy"
   for something you are half way through. */
var epEl=slide.querySelector('.sf-hero-ep');
if(epi&&wide){
if(!epEl){
epEl=document.createElement('div');
epEl.className='sf-hero-ep';
epEl.setAttribute('data-pos','0');   /* invisible until placed -- see below */
slide.appendChild(epEl);
}
/* Season 0 is Jellyfin's specials bucket. The BUTTON already says "Continue
   Special 7" rather than "S0 E7"; the line above it was still saying S0, so the
   two disagreed on the same card. Same rule in both places. */
/* sf-hero-eptitle (2026-08-29): the hero's episode line was the one place an
   episode NAME was never translated -- nothing outside this function even
   referenced .sf-hero-ep, so on a German profile the plot came through in
   German while the line above it stayed English.
   window.sfTrEp(id,en) already exists for exactly this (the detail page composes
   its own "S1 E1 . name" the same way): it returns the English name and queues
   the batch until /api/eptitles resolves, so calling it every tick is correct
   and costs one fetch.
   Translated AT THE SOURCE rather than by rewriting the node afterwards. A
   second writer would fight this one: the line below only writes when the text
   differs, so an outside translator would be undone 400ms later, forever --
   see [[jellyfin-episode-title-flicker]].
   NOTE some episodes legitimately have no translation: build_ep_titles.py's
   acceptable() drops a 'translation' equal to the English name, so e.g. HIMYM
   S2E8 "Atlantic City" is stored with no `de` because that IS the German
   title. Those correctly stay as they are. */
var _epn=epi.name;
try{if(window.sfTrEp)_epn=window.sfTrEp(epi.epId||epi.id||'',epi.name)||epi.name;}catch(e){}
var epTxt=sfEpName(epi)+(_epn?(' – '+_epn):'');
if(epEl.textContent!==epTxt)epEl.textContent=epTxt;
/* Describe the EPISODE being resumed, not the series. Media Bar fills .plot from
   the series record, so this is stashed on the slide and re-applied by the tick
   the same way the runtime is -- Media Bar re-renders that row and would
   otherwise put the show's logline back. */
if(epi.ov)slide.setAttribute('data-sf-plot',epi.ov);
else slide.removeAttribute('data-sf-plot');
/* sf-hero-epid: the slide carries the SERIES id, so nothing downstream could
   tell WHICH episode's synopsis is on it -- which is why a resumed show's hero
   could not be translated. Stamp the episode id here, where it is known. */
if(epi.epId)slide.setAttribute('data-sf-epid',epi.epId);
else slide.removeAttribute('data-sf-epid');
/* genre is hidden for every slide now (CSS), so nothing to toggle here */
}else{
if(epEl&&epEl.parentNode)epEl.parentNode.removeChild(epEl);
slide.removeAttribute('data-sf-plot');   /* films and unwatched shows keep their own */
}
/* sf-bar-allsizes (2026-08-28). The admin wants the progress bar at EVERY width.
   It used to be gated on `wide` as well as `resumable`, so on a narrow viewport
   it was never built at all -- not hidden, absent. The original reason was that
   the bar AND the episode line together pushed the Play button off the slide.
   Only the EPISODE LINE stays gated (see `if(epi&&wide)` above); the bar is 5px
   tall and costs almost nothing, and the phone band now hides the plot, which
   leaves a clear gap between the chips and the button for it to sit in. */
if(!resumable){
if(bar&&bar.parentNode)bar.parentNode.removeChild(bar);
/* "Play S8 E4" names the episode without implying progress that does not exist --
   "Continue" would be a lie here, nothing has been watched.
   On mobile the bar is gone but the LABEL stays: it is the one place the episode
   is still named, and text in an existing button cannot disturb the layout. */
sfHeroLabel(slide,resumable?label:(nu?('Play '+sfEpName(nu)):'Play'));
try{sfCwBarPos();}catch(e){}
return;
}
if(!bar){
bar=document.createElement('div');
bar.className='sf-cw-prog';
bar.innerHTML='<b><i></i></b>';
bar.setAttribute('data-pos','0');   /* hidden until placed -- see sf-cw-nojump */
/* Sits between the episode line and the description, in space we MAKE for it.
   Media Bar's hero rows are absolutely positioned with only 9-12px between them
   (measured: genre 227-247, plot 259-368), so there is no free band -- an
   earlier version floated here and was drawn straight over the genre line
   (-14px). The CSS shifts the description and buttons down on .sf-cw slides
   only, which opens a clean band; this positions the bar inside it, measured
   from the chip row's own box so it follows whatever layout the viewport gives. */
slide.appendChild(bar);
}
/* Fill from empty on each new slide -- the bar draws itself in as the hero
   arrives, which reads as deliberate rather than as a static graphic. The CSS
   transition does the work; the rAF is only so the browser has a 0 to move from. */
/* sf-hero-prog-smooth: this animates transform:scaleX, NOT width. Width is a
   LAYOUT property, so every frame of the .9s transition forced a layout + paint
   on the main thread -- and the 400ms tick, which re-measures and repositions
   this very bar in sfCwBarPos, lands inside that window. That is why the fill
   stepped instead of gliding. scaleX runs on the compositor and cannot be
   stuttered by main-thread work at all. The fill is width:100% and scaled from
   transform-origin:left, so the painted geometry is unchanged. */
var pc=Math.max(1,Math.min(100,pct));
var fill=bar.querySelector('i'),target='scaleX('+(pc/100).toFixed(4)+')';
if(fill&&fill.style.transform!==target){
fill.style.transform='scaleX(0)';
requestAnimationFrame(function(){requestAnimationFrame(function(){fill.style.transform=target;});});
}
/* No text beside the bar: the bar itself carries the meaning, and a label here
   competed with the episode line above and the plot below for the same space. */
sfHeroLabel(slide,label);
/* Place everything in THIS frame. Left to the 400ms tick, a card that is now
   decided synchronously would still spend up to 400ms at the wrong height. */
try{sfCwBarPos();}catch(e){}
}
/* Media Bar toggles .active on the slides themselves, so a class observer sees
   a hero change the moment it happens instead of up to 400ms later -- the last
   remaining source of visible settling once the data wait was removed.
   jf-observer-scope: the slideshow container only, attributes only, filtered to
   class. Our own writes here are to style properties and data- attributes, which
   this filter does not see, so painting cannot re-trigger the observer; the one
   class we do set (.sf-cw) re-enters sfHeroResume, which returns immediately on
   its data-sf-cw guard. */
var sfHeroObs=null;
/* sf-hero-wheel: the page would not scroll while the pointer was over the hero.
   Media Bar listens for wheel events on the slideshow to drive its own slide
   navigation and prevents the default, so the browser never scrolls -- the hero
   is a full viewport tall, so that is a dead zone across the entire first screen.

   Fixed by catching the wheel in the CAPTURE phase, before Media Bar's listener
   runs, and stopping propagation for VERTICAL wheels only. We deliberately do not
   preventDefault: letting the event through untouched is what allows the browser
   to scroll natively. Horizontal wheels still reach Media Bar, so trackpad
   swipe-to-change-slide keeps working. */
var sfWheelWired=false;
/* sf-hero-noport: nothing inside the hero may be a scroll container.

   #slides-container was the big one, but the dead zone survived over a band of
   the left column: `.plot` is line-clamped with overflow:hidden, and a clamped
   paragraph OVERFLOWS by definition (measured scrollHeight 80 vs clientHeight
   60). Any overflow:hidden box whose content overflows is a scrollport, and a
   hidden scrollport swallows the wheel without scrolling and without chaining to
   the page -- so hovering that 620px-wide strip killed scrolling.

   Converting hidden to `clip` fixes it: same clipping, but explicitly not a
   scroll container. Verified the line clamp is unaffected -- the element's height
   is identical either way.

   Done as a sweep rather than a list of selectors because the offender is
   whatever happens to overflow, which changes with the text: a long synopsis
   overflows where a short one does not. Each element is converted once and
   flagged, so this costs one attribute check per hero node per tick. */
/* sf-hero-img: the hero was decoding 27 megapixels of artwork on the main
   thread, synchronously, every time a slide came in -- long-animation-frame
   attribution put the two worst frames (110ms, 109ms) in rendering with no
   script time at all. Two causes, both fixed here.

   1. `decoding` was unset, which means SYNCHRONOUS decode during paint. async
      hands it to a decoder thread so a slow decode can no longer stall a frame.
   2. Nothing capped the request size. Media Bar asks for the original: a
      4320x898 logo to paint into a 391x113 box, a 3560x2003 backdrop for a
      1712x778 one. Measured against this server: maxWidth=600 turns that logo
      into 600x125 / 23KB (51x fewer pixels) and maxWidth=1920 turns the
      backdrop into 1920x1080 / 245KB. Wasted bytes, wasted decode, and wasted
      downscale-raster on every slide.

   The new URL is loaded into a detached Image FIRST and the visible src is only
   repointed once that has completed, so the artwork never blanks mid-swap. The
   cap is stored on the element so a Media Bar re-render (which rewrites src)
   is re-processed rather than skipped. */
/* sf-hero-img: ask the server for artwork the size we actually draw.

   Media Bar requests the ORIGINALS -- measured 3840x2160 backdrops and a
   4320x898 logo painted into a 391px box, 27 megapixels across the hero. That
   is what makes the hero slow. There is no size option in its config (checked:
   MaxItems, PreloadCount, intervals -- nothing about dimensions), so the URL has
   to be adjusted here.

   THE RULE THAT MATTERS: only ever rewrite an image that has NOT loaded yet.
   The earlier version preloaded a smaller copy and then re-pointed src once it
   arrived -- so the element briefly had a new source with nothing decoded, the
   ambient wash showed through, and that was the red flash. Rewriting before the
   first load means the browser aborts the original fetch mid-flight and only
   ever paints once. An image already showing is left alone, always: it costs
   nothing to leave (it is downloaded) and swapping it is exactly the bug.

   Driven by a MutationObserver rather than the 400ms tick, because the rewrite
   has to happen in the same task Media Bar sets src -- a tick landing later
   would find the image already loading or loaded. */
var sfHeroImgObs=null;
function sfHeroImgCap(im){
if(!im||im.tagName!=='IMG')return;
if(im.decoding!=='async')im.decoding='async';
var s=im.getAttribute('src')||'';
if(!s||s.indexOf('/Images/')<0||s.indexOf('maxWidth=')>-1)return;
if(im.complete&&im.naturalWidth>0)return;      /* painted already -- never touch */
var hi=(window.devicePixelRatio||1)>1;
var cap=/(^|\s)logo(\s|$)/.test(im.className)?(hi?900:600):(hi?2560:1920);
im.setAttribute('src',s+(s.indexOf('?')>-1?'&':'?')+'maxWidth='+cap);
}
function sfHeroImg(){
var host=document.getElementById('slides-container');
if(!host)return;
if(!sfHeroImgObs){
sfHeroImgObs=new MutationObserver(function(ms){
var i,j,k,m,n,q;
for(i=0;i<ms.length;i++){
m=ms[i];
if(m.type==='attributes'){sfHeroImgCap(m.target);continue;}
for(j=0;j<m.addedNodes.length;j++){
n=m.addedNodes[j];
if(!n||n.nodeType!==1)continue;
if(n.tagName==='IMG'){sfHeroImgCap(n);continue;}
if(n.querySelectorAll){q=n.querySelectorAll('img');for(k=0;k<q.length;k++)sfHeroImgCap(q[k]);}
}
}
});
/* the src filter is what makes re-entry safe: our own rewrite fires the
   observer again and falls straight out on the maxWidth test */
sfHeroImgObs.observe(host,{childList:true,subtree:true,attributes:true,attributeFilter:['src']});
}
var imgs=host.getElementsByTagName('img'),i;
for(i=0;i<imgs.length;i++)sfHeroImgCap(imgs[i]);
}
function sfHeroNoPort(){
var host=document.getElementById('slides-container');
if(!host)return;
var els=host.querySelectorAll('*:not([data-sf-clip])'),i,el,cs;
for(i=0;i<els.length;i++){
el=els[i];
cs=getComputedStyle(el);
if(cs.overflowY==='hidden'||cs.overflowX==='hidden'){
if(el.scrollHeight>el.clientHeight+1||el.scrollWidth>el.clientWidth+1){
el.style.overflow='clip';
el.setAttribute('data-sf-clip','1');
continue;
}
}
/* only flag boxes that can never become scrollports; a clamped paragraph can
   start overflowing later when the text changes, so leave those unflagged */
if(cs.overflowY!=='hidden'&&cs.overflowX!=='hidden')el.setAttribute('data-sf-clip','1');
}
}
function sfHeroWheel(){
if(sfWheelWired)return;
var slide=document.querySelector('.slide');
var host=slide&&slide.parentElement;
if(!host)return;
sfWheelWired=true;
/* Stop EVERY wheel event reaching Media Bar, not just vertical ones. The
   vertical-only test was too clever: a trackpad produces noisy diagonal deltas,
   so a gesture that is plainly a scroll can momentarily report deltaX > deltaY
   and slip through to Media Bar, which prevents the default and eats that part of
   the gesture. Losing wheel-driven slide changes costs nothing -- the slides
   rotate on their own and the arrows still work -- whereas losing scroll makes
   the whole first screen feel broken. */
host.addEventListener('wheel',function(e){
e.stopPropagation();
},{capture:true,passive:true});
}
/* sf-row-titles: make our injected rows behave like Jellyfin's own -- the
   heading is a link to the full list. Native rows already do this; ours were
   dead text, which reads as broken next to them. */
/* sf-music-btn: the header's music button opened the Music library on its
   DEFAULT tab, which is Albums -- so the Suggestions page built to be the music
   landing page was the one place the music button never went.
   `?tab=1` is Jellyfin's own tab selector and Suggestions is data-index 1
   (verified live: Albums 0, Suggestions 1, Artists 2, Playlists 4, Songs 5 --
   the visual order is flex `order`, the indices are unchanged).
   Capture phase + stopImmediatePropagation so Jellyfin's own handler never
   runs, the same technique jf-watchlist-btn uses on a button it does not own.
   Matched on the ICON class rather than the title, because the title is
   localised and a household user's client may not be in English. */
var sfMusBtnWired=false;
function sfMusicBtn(){
if(sfMusBtnWired)return;
if(!document.body)return;
sfMusBtnWired=true;
document.addEventListener('click',function(e){
var b=(e.target&&e.target.closest)?e.target.closest('.headerButton'):null;
if(!b||!b.querySelector('.library_music'))return;
e.preventDefault();
e.stopImmediatePropagation();
location.hash='#/music?tab=1';
},true);
}
/* sf-row-arrows: the prev/next controls on our injected rows.

   These were removed globally earlier on a misreading -- the arrows the admin wanted
   gone were the CHEVRONS BESIDE THE ROW TITLES, not the controls that scroll a
   row. The native ones are restored (see the sf-row-polish CSS) and our rows now
   get the same thing, which also removes the original objection to them: that
   they appeared on native rows but never on ours.

   Built from Jellyfin's own markup rather than styled from scratch --
   `.emby-scrollbuttons.padded-right` wrapping two
   `.emby-scrollbuttons-button.paper-icon-button-light` -- so size, icon, colour
   and hover state are inherited and cannot drift from the native rows. Measured
   after: top+0, right inset 0, 151x54, identical to a native row.

   Our rows are plain `overflow-x:auto` flex containers, not Jellyfin's sly-based
   scroller, so the buttons drive `scrollBy` directly. 85% of a screenful per
   press leaves the edge card visible as an anchor, which is what the native
   scroller does. */
/* sf-detail-appletv: the item page as a cinematic hero, the way Apple TV does it.

   Jellyfin ships `#itemBackdrop` as an EMPTY 225px spacer -- no image, no
   children (verified) -- and paints its artwork instead into `.backdropImage`,
   a full-viewport blur(23px) layer behind the whole app. That is why the stock
   page reads as "small blurred smudge behind a poster card": the art is never
   presented, only suggested.

   So the image is put where it belongs. The CSS turns #itemBackdrop into a
   full-bleed hero and hides the blurred layer on this route only.

   Guarded on the item id rather than a boolean, so moving from one title to the
   next repaints; and resolved against the VISIBLE #itemDetailPage, because
   Jellyfin keeps a cached hidden instance with the same id (measured: 2 of them,
   the hidden one first in document order). See jellyfin-duplicate-page-instances. */
/* sf-detail-badges: the small outlined capability badges Apple puts under the
   title -- 4K, Dolby Vision, Dolby Atmos, CC, SDH.

   This is the "delivers info without cluttering" part of the Apple layout: it
   answers "will this look and sound good, and can I put subtitles on" in one
   glance, without the codec table. Every value already exists in the item's
   MediaStreams, which until now were only readable by opening the Video/Audio
   selectors further down the page.

   Derived, not guessed:
     resolution  Height >= 2000 -> 4K, >= 1000 -> HD  (1920x1038 is HD; the
                 height is 1038 not 1080 because the film is letterboxed, which
                 is exactly why this keys off a threshold and not equality)
     range       VideoRangeType DOVI -> Dolby Vision, HDR* -> HDR
     audio       any stream whose profile or title says Atmos -> Dolby Atmos,
                 else the best channel layout present (7.1 / 5.1)
     subtitles   any subtitle track -> CC; one marked SDH/hearing -> SDH
   Nothing is invented: a badge appears only when the file actually has it. */
/* sf-series-episodes: a season picker and a row of episodes on the SERIES page,
   the way Apple TV does it.

   Stock Jellyfin shows none of this: measured on a live series page the only
   sections are Cast & Crew, More Like This, Recommended and Similar. To reach an
   episode you have to leave for a season page first. So this is not only a
   restyle -- it puts the thing the page exists for on the page.

   Cards carry what Apple's do: the still, "EPISODE n", the title, the synopsis,
   and the runtime. Watch progress is drawn on the still when there is any, so a
   half-finished episode is obvious without opening it.

   Rebuilt only when the series or the chosen season changes; the season <select>
   re-renders just the row, never the whole section. */
var sfEpBusy=false;
function sfEpCard(ac,ep){
var card=document.createElement('div');
card.className='sf-ml-card sf-ep-card';
card.setAttribute('data-id',ep.Id);
var art=document.createElement('div');
art.className='sf-ep-still';
var url='';
try{
if((ep.ImageTags||{}).Primary)url=ac.getImageUrl(ep.Id,{type:'Primary',maxWidth:500,tag:ep.ImageTags.Primary});
else if((ep.ParentBackdropImageTags||[]).length&&ep.ParentBackdropItemId)
url=ac.getImageUrl(ep.ParentBackdropItemId,{type:'Backdrop',index:0,maxWidth:500});
}catch(e){url='';}
if(url)art.style.backgroundImage='url("'+url+'")';
var pct=((ep.UserData||{}).PlayedPercentage)||0;
if(pct>0&&pct<99){
var bar=document.createElement('div');bar.className='sf-ep-prog';
var fill=document.createElement('i');
var _f3='scaleX('+(pct/100).toFixed(4)+')';if(fill.style.transform!==_f3)fill.style.transform=_f3;
bar.appendChild(fill);art.appendChild(bar);
}
card.appendChild(art);
var kicker=document.createElement('div');
kicker.className='sf-ep-kicker';
kicker.textContent='Episode '+(ep.IndexNumber!=null?ep.IndexNumber:'');
card.appendChild(kicker);
var ttl=document.createElement('div');
ttl.className='sf-ep-title';
ttl.textContent=ep.Name||'';
card.appendChild(ttl);
var ov=document.createElement('div');
ov.className='sf-ep-ov';
ov.textContent=ep.Overview||'';
card.appendChild(ov);
var foot=document.createElement('div');
foot.className='sf-ep-foot';
foot.textContent=ep.RunTimeTicks?(Math.round(ep.RunTimeTicks/600000000)+'m'):'';
card.appendChild(foot);
card.addEventListener('click',function(){
location.hash='#/details?id='+this.getAttribute('data-id');});
return card;
}
function sfSeriesEpisodes(){
if((location.hash||'').indexOf('#/details')!==0)return;
var pages=document.querySelectorAll('#itemDetailPage'),page=null,i;
for(i=0;i<pages.length;i++){
if(pages[i].offsetParent!==null&&pages[i].getBoundingClientRect().height>0){page=pages[i];break;}
}
if(!page)return;
var m=(location.hash||'').match(/[?&]id=([a-zA-Z0-9]+)/);
if(!m)return;
var id=m[1];
if(page.getAttribute('data-sf-eps')===id)return;
var host=page.querySelector('.detailPageContent');
if(!host)return;
var ac=window.ApiClient;
if(!ac||!ac.getJSON||!ac.getCurrentUserId)return;
if(sfEpBusy)return;
var uid=ac.getCurrentUserId();
if(!uid)return;
sfEpBusy=true;
page.setAttribute('data-sf-eps',id);
ac.getItem(uid,id).then(function(it){
if(!it){sfEpBusy=false;return null;}
/* Which series' seasons to list, which season to open on, and -- on an episode
   page -- which card to mark as the one you are looking at. */
var seriesId=null,wantSeason=null,curEp=null;
if(it.Type==='Series'){seriesId=id;}
else if(it.Type==='Season'){seriesId=it.SeriesId;wantSeason=id;}
else if(it.Type==='Episode'){seriesId=it.SeriesId;wantSeason=it.SeasonId;curEp=id;}
if(!seriesId){sfEpBusy=false;return null;}
return ac.getJSON(ac.getUrl('Shows/'+seriesId+'/Seasons',{userId:uid})).then(function(sr){
var seasons=(sr&&sr.Items)||[];
if(!seasons.length){sfEpBusy=false;return null;}
var old=page.querySelector('.sf-epsrow');
if(old&&old.parentNode)old.parentNode.removeChild(old);
var sec=document.createElement('div');
sec.className='verticalSection sf-mylist sf-epsrow';
var head=document.createElement('div');
head.className='sectionTitleContainer sectionTitleContainer-cards sf-eps-head';
var sel=document.createElement('select');
sel.className='sf-season-select';
for(var k=0;k<seasons.length;k++){
var o=document.createElement('option');
o.value=seasons[k].Id;
o.textContent=seasons[k].Name||('Season '+seasons[k].IndexNumber);
sel.appendChild(o);
}
head.appendChild(sel);
sec.appendChild(head);
var row=document.createElement('div');
row.className='sf-ml-row sf-eps-track';
sec.appendChild(row);
function load(seasonId){
row.setAttribute('data-loading','1');
ac.getJSON(ac.getUrl('Shows/'+seriesId+'/Episodes',{userId:uid,seasonId:seasonId,
Fields:'Overview',EnableUserData:true}))
.then(function(er){
row.innerHTML='';
row.removeAttribute('data-loading');
var eps=(er&&er.Items)||[],cur=null;
for(var j=0;j<eps.length;j++){
var c=sfEpCard(ac,eps[j]);
if(curEp&&eps[j].Id===curEp){c.classList.add('sf-ep-current');cur=c;}
row.appendChild(c);
}
/* open showing where you are, not at episode 1 -- but only scroll the ROW, so
   the page itself does not jump */
if(cur)try{row.scrollLeft=Math.max(0,cur.offsetLeft-row.clientWidth*0.28);}catch(e){}
}).catch(function(){row.removeAttribute('data-loading');});
}
sel.addEventListener('change',function(){load(this.value);});
var startId=seasons[0].Id,si;
if(wantSeason){
for(si=0;si<seasons.length;si++){
if(seasons[si].Id===wantSeason){startId=wantSeason;sel.selectedIndex=si;break;}
}
}
load(startId);
/* Above the synopsis, not merely above Cast & Crew: on a series page the
   episodes ARE the content and everything else is reference material. Inserted
   into the primary container straight after the hero ribbon, which puts it
   ahead of .detailPagePrimaryContent (synopsis, info, selectors). */
var pcont=page.querySelector('.detailPagePrimaryContainer');
var ribbon=pcont?pcont.querySelector('.detailRibbon'):null;
/* sf-plot-below-hero (2026-09-05): the overview now sits between the hero and
   this row, so anchor to the PLOT when it is there. Both insertions target
   ribbon.nextSibling otherwise, and whichever ran second won -- measured the row
   at y=789 with the plot pushed below it at y=1281, the wrong order for a series.
   Anchoring each to the element before it makes the result independent of which
   one is built first: ribbon -> plot -> episodes, always. */
var _anchor=(pcont?pcont.querySelector(':scope > .sf-dfacts'):null)||ribbon;
if(pcont&&ribbon)pcont.insertBefore(sec,_anchor.nextSibling);
else host.insertBefore(sec,host.firstChild);
sfEpBusy=false;
return null;
});
}).catch(function(){sfEpBusy=false;});
}
/* The 400ms tick is the backstop, not the mechanism: navigating from a card on
   home fires hashchange immediately, so the class lands within a frame or two
   instead of up to 400ms later. */
try{window.addEventListener('hashchange',function(){try{sfDetailHero();}catch(e){}});}catch(e){}
/* sf-overview-more: keep "Show more" honest after we tightened the clamp.

   Jellyfin clamps the synopsis at SIX lines and decides ONCE, at render, whether
   the expand control is needed -- adding its `hide` class when the text fits.
   Clamping to three in CSS (Apple shows two or three, not six) truncates text
   that Jellyfin had already judged short enough, so the control stayed hidden
   and the rest of the synopsis became unreachable.

   Overflow cannot be tested in CSS, so it is tested here: if the clamped element
   is taller than its box, the control is un-hidden. When Jellyfin expands, it
   removes `detail-clamp-text` -- the query then finds nothing and this leaves
   the "Show less" state entirely alone. */
'''

# _LS_13 (orig L8696-9422) -- sf-info-panel, sf-episode-line, sf-dfacts
_LS_13 = r'''/* sf-info-panel: the Info button, and the scroll hint that gets out of the way.

   Replaces Trailer and Shuffle in the hero row. Neither earned its place: a
   trailer is a detour on a server where you already own the film, and shuffle on
   a MOVIE is meaningless. Info answers the question people actually have.

   The panel is built by CLONING what is already on the page -- the synopsis, the
   Genres/Director/Writer/Studios rows, the capability badges -- rather than
   re-fetching. One source of truth, so it can never disagree with the page, and
   no extra request. The <select> controls are deliberately NOT cloned: a copy of
   a track picker would look operable and do nothing.

   Closes on the X, on the backdrop, and on Escape. Focus moves to the close
   button on open so a keyboard or remote is not stranded behind the overlay. */
function sfInfoClose(){
/* put the borrowed picker block back before the overlay is destroyed, or it
   would be removed along with it and the page would lose its only live control */
var t=window.__sfTs;
if(t&&t.node&&t.parent){
try{
t.node.classList.remove('sf-info-tracks');
t.parent.insertBefore(t.node,t.next&&t.next.parentNode===t.parent?t.next:null);
}catch(e){}
window.__sfTs=null;
}
var ov=document.querySelector('.sf-info-overlay');
if(ov&&ov.parentNode)ov.parentNode.removeChild(ov);
document.documentElement.style.removeProperty('overflow');
}
function sfInfoOpen(page){
if(document.querySelector('.sf-info-overlay'))return;
var ov=document.createElement('div');
ov.className='sf-info-overlay';
var panel=document.createElement('div');
panel.className='sf-info-panel';
var close=document.createElement('button');
close.className='sf-info-close';
close.setAttribute('title','Close');
close.innerHTML='<span class="material-icons close" aria-hidden="true"></span>';
close.addEventListener('click',sfInfoClose);
panel.appendChild(close);
var h=document.createElement('h2');
h.className='sf-info-title';
var logoName=page.querySelector('.itemName');
var nm=(logoName&&logoName.textContent.trim())||document.title||'';
h.textContent=nm;
panel.appendChild(h);
var body=document.createElement('div');
body.className='sf-info-body';
/* The status toggles the hero no longer shows. Proxied, not cloned: a clone
   would look identical and do nothing, because the handler belongs to the
   original node. The real buttons stay in the DOM, merely hidden. */
var acts=document.createElement('div');
acts.className='sf-info-actions';
[['.btnPlaystate','Mark played','check'],
 ['.btnUserRating','Favorite','favorite'],
 ['.je-detail-hide-btn','Watchlist','visibility'],
 ['.btnMoreCommands','More','more_horiz']].forEach(function(spec){
var real=page.querySelector(spec[0]);
if(!real)return;
var b=document.createElement('button');
b.type='button';
b.className='sf-info-action';
var ic=document.createElement('span');
ic.className='material-icons '+spec[2];
var tx=document.createElement('span');
/* Jellyfin keeps the CURRENT meaning in the title -- "Mark played" flips to
   "Mark unplayed" -- so reading it keeps this honest with no state of our own */
tx.textContent=(real.getAttribute('title')||spec[1]).trim();
b.appendChild(ic);b.appendChild(tx);
b.addEventListener('click',function(e){
e.preventDefault();e.stopPropagation();
/* close first, then act on the next tick: the overflow menu opens its own
   action sheet, and that must not appear underneath -- or inherit focus from --
   an overlay that is about to be destroyed. */
sfInfoClose();
setTimeout(function(){try{real.click();}catch(err){}},0);
});
acts.appendChild(b);
});
if(acts.children.length)body.appendChild(acts);
/* badges next -- they are the quickest read */
var badges=page.querySelector('.sf-badges');
if(badges)body.appendChild(badges.cloneNode(true));
/* The synopsis now lives ON THE PAGE (sf-dfacts), so the panel no longer
   carries it -- two copies of the same paragraph is how they drift. */
var grp=page.querySelector('.itemDetailsGroup');
if(grp){
var g=grp.cloneNode(true);
g.classList.add('sf-info-rows');
body.appendChild(g);
}
/* The REAL picker block is MOVED in, not copied. A cloned <select> looks
   operable and changes nothing, because the handler belongs to the original
   node -- so the node itself travels, and goes home again on close. Moving an
   element preserves its listeners; cloning does not. */
/* The Audio/Subtitle pickers now live ON THE PAGE (sf-dfacts). They are a
   single live node, so they can only be in one place -- borrowing them into
   the panel would take them off the page for as long as it was open.
   sfInfoClose's restore is left in place: it no-ops when __sfTs is null. */
panel.appendChild(body);
ov.appendChild(panel);
ov.addEventListener('click',function(e){if(e.target===ov)sfInfoClose();});
document.body.appendChild(ov);
document.documentElement.style.setProperty('overflow','hidden');
try{close.focus();}catch(e){}
}
try{document.addEventListener('keydown',function(e){
if(e.key==='Escape'&&document.querySelector('.sf-info-overlay'))sfInfoClose();});}catch(e){}
/* sf-episode-line: "Season 1 - 2. The Bicycle Thief" is how a database prints an
   episode, not how anyone says it. Rewritten to "S1 E2 . The Bicycle Thief",
   which is the form Apple and Netflix both use and reads at a glance.
   Keyed on the item id so a re-render restores it, and only ever applied to an
   Episode -- a movie's title is left exactly as it is. */
function sfEpisodeLine(){
if((location.hash||'').indexOf('#/details')!==0)return;
var pages=document.querySelectorAll('#itemDetailPage'),page=null,i;
for(i=0;i<pages.length;i++){
if(pages[i].offsetParent!==null&&pages[i].getBoundingClientRect().height>0){page=pages[i];break;}
}
if(!page)return;
var m=(location.hash||'').match(/[?&]id=([a-zA-Z0-9]+)/);
if(!m)return;
var id=m[1];
var el=page.querySelector('.itemName');
if(!el)return;
/* This is the ONLY writer of the episode line. It used to rebuild the line from
   the API's English name whenever the text was not what it last wrote -- so a
   translation applied by anything else was reverted, the translator re-applied
   it, and the title flickered between languages at tick speed (measured:
   Chinese at 3s, English at 8s, Chinese at 25s). Translating HERE keeps one
   writer and removes the fight; the separator stays Jellyfin's. */
var prefix=page.getAttribute('data-sf-epprefix');
var enName=page.getAttribute('data-sf-epname');
if(page.getAttribute('data-sf-epline-id')===id&&prefix!==null&&enName!==null){
var nm=(window.sfTrEp?window.sfTrEp(id,enName):enName)||enName;
var line2=prefix+nm;
if(el.textContent.trim()!==line2)el.textContent=line2;
return;
}
var ac=window.ApiClient;
if(!ac||!ac.getItem||!ac.getCurrentUserId)return;
if(page.getAttribute('data-sf-epline-id')===id)return;   /* fetch in flight */
page.setAttribute('data-sf-epline-id',id);
ac.getItem(ac.getCurrentUserId(),id).then(function(it){
if(!it||it.Type!=='Episode')return;
if(it.ParentIndexNumber==null||it.IndexNumber==null)return;
page.setAttribute('data-sf-epprefix','S'+it.ParentIndexNumber+' E'+it.IndexNumber+' · ');
page.setAttribute('data-sf-epname',it.Name||'');
}).catch(function(){});
}
/* sf-dfacts (2026-08-29). The admin: "for the movie info page and the tv info page,
   lets move the audio select and subtitle select and plot desctiption to the
   main movie or tv info page instead of in the info icon."
   Placed as the FIRST child of .detailPageContent, which already carries the
   page gutter -- measured 65px at 1440 and 12.5px at 390, the same padding that
   puts "Cast & Crew" where it is. Inheriting it means this block lines up with
   every row below it at any width, with no vw guess of our own. It also lands in
   the empty band between the hero buttons and the first row (measured 134px at
   1440, 62px at 390), which is exactly the space it should occupy.
   The pickers are MOVED, never cloned: a cloned <select> looks operable and does
   nothing, because the handler belongs to the original node.
   The plot is COPIED as text from the page's own .overview, which stays the one
   source of truth -- so the German/Chinese swap (the plot translator writes into
   #itemDetailPage .overview) reaches this copy on the next tick for free. */
function sfDetailFacts(){
if((location.hash||'').indexOf('#/details')!==0)return;
var pages=document.querySelectorAll('#itemDetailPage'),page=null,i;
for(i=0;i<pages.length;i++){
if(pages[i].offsetParent!==null&&pages[i].getBoundingClientRect().height>0){page=pages[i];break;}
}
if(!page)return;
/* sf-dfacts-preblock (2026-09-04). This used to wait for .sf-atv, which
   GUARANTEED a layout shift: the page was revealed first and the plot inserted
   afterwards, shoving everything below it down. Measured on a series --
   reveal at 792ms, plot inserted at 858ms, and the episodes row jumped
   806 -> 945 with the cast following 1249 -> 1391. A visible lurch on a page
   the user is already looking at.
   Building it earlier is safe: until .sf-atv lands the whole page is held at
   opacity 0 by the jf-atv-boot rule, so nothing here can be seen over the stock
   layout -- which is what that gate was protecting against. Wait for the item
   TYPE instead (stamped by sfDetailHero from its own getItem, ~440ms, well
   before the reveal), because the type is what decides where the block goes. */
if(!page.classList.contains('sf-atv')&&!page.getAttribute('data-sf-type'))return;
var content=page.querySelector('.detailPageContent');
if(!content)return;
var dm=(location.hash||'').match(/[?&]id=([a-zA-Z0-9]+)/);
var id=dm?dm[1]:'';
/* sf-plot-above-eps (2026-09-04). The admin: on a movie the summary reads fine, but
   on a series "the description for the plot loading below that seasons row ...
   doesn't look good". Measured: hero(centred) -> buttons 642 -> seasons row 789
   -> plot 853. The block is centre-aligned to sit under the centred hero, which
   is right on a movie; on a series the left-aligned episodes row lands between
   them and the paragraph is orphaned mid-page under a rule.
   It has to be placed HERE rather than moved afterwards: the lookup below is
   scoped to a direct child of .detailPageContent, so relocating the node from a
   tick just made this rebuild a second one (measured two painted copies at
   y=692 and y=1254). Choose the container instead, and re-seat an existing box
   if the episodes row only arrives later. */
var eps=page.querySelector('.sf-epsrow');
/* sf-plot-place-once (2026-09-04). The admin: "the plot loads in below the first
   view but when i scroll down and back up, the plot shifts up to be in the
   first view."
   That was this block re-seating itself: on a series the seasons row does not
   exist yet when the plot is first built, so it landed in .detailPageContent and
   was then moved above the row once it appeared -- a visible jump, and one you
   only noticed on the scroll back because that is when it repainted.
   Place it ONCE. On a series (#childrenContent is present on those pages and not
   on a movie) wait for the row, so the first position is the final one. The wait
   is capped: a series whose row never builds still gets its plot, just in the
   movie position. */
var ty=page.getAttribute('data-sf-type')||'';
/* sf-plot-one-place (2026-09-04). The admin: "The plot should have ONE intentional
   position in the final composition" and must never "appear in a location
   inherited from the wrong media type".
   It had two, chosen by type: Series/Season parked it in the ribbon (above the
   episodes row), everything else dropped it into .detailPageContent. That is
   what put an EPISODE's synopsis at y=1178, below a 371px row of its own
   siblings -- an episode inheriting the movie position. It also gave the two
   types different spacing for the same pair of elements: measured actions->plot
   at 42px on a series and 166px on a movie.
   A movie has no episodes row, so the ribbon is correct for it too, and the
   whole branch collapses. One position, chosen once, for all four types --
   fewer rules, not more. */
var isShow=true;
/* sf-plot-anchor (2026-09-04). The admin: "the plot loads in first, but once the
   season row loads in it loads in above the plot and pushes it down."
   Waiting for .sf-epsrow was the wrong mechanism. Measured here the row arrives
   at 1665ms and the plot at 1915ms, so the wait held and my tests passed -- but
   on a slower machine the row misses the cap, the plot is placed in the lower
   container, and the row then appears above it and shoves it down. A timeout
   cannot decide layout.
   Anchor to something that ALREADY EXISTS instead. .mainDetailButtons is present
   at 123ms, long before the type is even known, and it lives in .detailRibbon --
   which renders above .detailPagePrimaryContent, where the row is built. So on a
   show, park the plot at the end of the ribbon: it is above the row by
   construction, whenever the row turns up, with nothing to wait for and nothing
   to move afterwards. */
/* sf-plot-below-hero (2026-09-05). The admin revised the Phase 4 decision: the first
   viewport should carry artwork, title, metadata and the actions and nothing
   else, with the overview beginning below it.
   So the plot leaves the ribbon and becomes the ribbon's next SIBLING inside
   .detailPagePrimaryContainer. Measured, that container is exactly:
       .detailPagePrimaryContainer
         .detailRibbon      <- logo / metadata / actions   (the hero)
         [.sf-epsrow]       <- series only, appended later
   Inserting at ribbon.nextSibling therefore lands the plot after the hero and
   BEFORE the episodes row on a series -- which is the required order -- and
   after the hero and before the cast on a movie, with one rule and no type
   branch. It also cannot be pushed down when the row arrives later, because the
   row is appended after it.
   How far below is CSS's job, from --sf-ribbon-bottom; see sf-hero-fold. */
var rib=page.querySelector('.detailRibbon');
if(!rib||!rib.parentNode)return;               /* hero not built yet -- next tick */
var host=rib.parentNode,before=rib.nextSibling;
var box=page.querySelector('.sf-dfacts');
if(!box){
box=document.createElement('div');
box.className='sf-dfacts';
box.innerHTML='<p class="sf-dfacts-plot"></p>';
host.insertBefore(box,before);
}else if(box.parentNode!==host&&!page.classList.contains('sf-atv')){
/* re-seat ONLY while the page is still held invisible by the sf-atv gate --
   moving it after the page is on screen is the jump this file has fixed twice */
host.insertBefore(box,before);
}
/* deliberately no re-seat: moving it after the fact IS the shift above */
var ovw=page.querySelector('.overview');
var p=box.querySelector('.sf-dfacts-plot');
var txt=ovw?(ovw.textContent||'').trim():'';
/* sf-dfacts-epdupe: on an EPISODE page the season row directly above already
   prints this exact synopsis under the episode still, so repeating it here is
   the same paragraph twice on one screen -- the admin: "the plot feels redudant
   ... we see the plot in the season select and the plot again right below it".
   A SERIES page is different: the row carries per-episode text and this is the
   show's own logline, which appears nowhere else, so it stays.
   Detected from data-sf-epprefix, which sfEpisodeLine sets only for Episodes --
   no extra request, and it is already keyed to the current id. */
/* sf-dfacts-epdupe REVERSED (2026-09-04), deliberately, and here is why.
   It blanked an episode's synopsis because the episodes row directly BELOW
   printed the same paragraph -- correct while the plot sat under that row, where
   the two were adjacent. With sf-plot-one-place the plot is now in the first
   view, above the row, so the adjacency it was solving no longer exists; keeping
   the blank would instead leave an episode as the only media type whose first
   view says nothing about it. The row repeating it further down is the row doing
   its job -- it lists every episode, including this one. */
if(p){
if(txt&&p.textContent!==txt)p.textContent=txt;
if(p.style.display!==(txt?'':'none'))p.style.display=txt?'':'none';
}
/* Jellyfin rebuilds .trackSelections when the item changes, and the rebuilt one
   appears back in .detailSection -- so take whichever copy is NOT already ours
   and drop the stale one, rather than assuming there is only ever one. */
var all=page.querySelectorAll('.trackSelections'),k,live=null;
for(k=0;k<all.length;k++)if(!box.contains(all[k]))live=all[k];
if(live){
var old=box.querySelector('.trackSelections');
if(old&&old!==live&&old.parentNode)old.parentNode.removeChild(old);
live.classList.add('sf-dfacts-tracks');
box.appendChild(live);
}
}
function sfInfoBtn(){
if((location.hash||'').indexOf('#/details')!==0)return;
var pages=document.querySelectorAll('#itemDetailPage'),page=null,i;
for(i=0;i<pages.length;i++){
if(pages[i].offsetParent!==null&&pages[i].getBoundingClientRect().height>0){page=pages[i];break;}
}
if(!page)return;
var row=page.querySelector('.mainDetailButtons');
if(!row||row.querySelector('.sf-infobtn'))return;
var play=row.querySelector('.btnPlay');
var b=document.createElement('button');
b.type='button';
b.className='detailButton emby-button sf-infobtn';
b.setAttribute('title','Info');
b.innerHTML='<span class="material-icons detailButton-icon info_outline" aria-hidden="true"></span>';
b.addEventListener('click',function(e){e.preventDefault();e.stopPropagation();sfInfoOpen(page);});
if(play&&play.nextSibling)row.insertBefore(b,play.nextSibling);
else row.appendChild(b);
}
/* The hint is a page element so it scrolls away by itself, but it should also
   stop competing the moment someone starts moving. One passive listener, one
   attribute -- no work per frame. */
var sfHintWired=false;
function sfScrollHint(){
if(sfHintWired)return;
sfHintWired=true;
try{window.addEventListener('scroll',function(){
var on=window.pageYOffset>36;
var d=document.documentElement;
if((d.getAttribute('data-sf-scrolled')==='1')!==on)
d.setAttribute('data-sf-scrolled',on?'1':'0');
},{passive:true});}catch(e){}
}
function sfOverviewMore(){
if((location.hash||'').indexOf('#/details')!==0)return;
var pages=document.querySelectorAll('#itemDetailPage'),page=null,i;
for(i=0;i<pages.length;i++){
if(pages[i].offsetParent!==null&&pages[i].getBoundingClientRect().height>0){page=pages[i];break;}
}
if(!page)return;
var btn=page.querySelector('.overview-expand');
if(!btn)return;
var ov=page.querySelector('.overview.detail-clamp-text');
if(!ov)return;                                  /* expanded: Jellyfin owns it */
if(ov.scrollHeight>ov.clientHeight+2){
if(btn.classList.contains('hide'))btn.classList.remove('hide');
}
}
/* sf-meta-episodic (2026-09-04). The admin: the TV page "should clearly communicate
   that this is an ongoing/episodic piece of content" and must not read as the movie
   page with seasons bolted underneath.
   Audited side by side, the first view of a Series was indistinguishable from a
   Movie's: logo, one subtitle line, three pills (year / rating / score), Play. A
   Season's was worse -- it carried NO metadata pills at all, so nothing on screen
   said how many episodes it held or which season of how many it was.
   The fix is information, not decoration: the counts that only an episodic item has,
   in the pill row that already exists, using Jellyfin's own .mediaInfoItem so there
   is no second pill style to maintain.
   Reads the numbers sfDetailBadges stashed, so this makes no request of its own, and
   re-asserts if Jellyfin rebuilds .itemMiscInfo underneath it. */
function sfDetailMeta(){
try{
if((location.hash||'').indexOf('#/details')!==0)return;
var ps=document.querySelectorAll('#itemDetailPage'),page=null,i;
for(i=0;i<ps.length;i++){if(!ps[i].classList.contains('hide')&&ps[i].getClientRects().length){page=ps[i];break;}}
if(!page)return;
var dm=(location.hash||'').match(/[?&]id=([a-zA-Z0-9]+)/);
if(!dm)return;
var id=dm[1],raw=page.getAttribute('data-sf-meta');
if(!raw)return;
var info;try{info=JSON.parse(raw);}catch(e){return;}
if(!info||info.id!==id)return;                     /* stale: belongs to the last item */
var host=page.querySelector('.itemMiscInfo');
if(!host)return;
/* already correct for THIS item -- cheap check, and it is what makes the re-assert
   below free on every tick after the first */
var have=host.querySelector('.sf-meta-pill');
if(have&&have.getAttribute('data-sf-for')===id)return;
var old=host.querySelectorAll('.sf-meta-pill'),k;
for(k=0;k<old.length;k++)if(old[k].parentNode)old[k].parentNode.removeChild(old[k]);
var want=[];
if(info.t==='Series'){
if(info.sea>0)want.push(info.sea+(info.sea===1?' Season':' Seasons'));
if(info.epi>0)want.push(info.epi+(info.epi===1?' Episode':' Episodes'));
}else if(info.t==='Season'){
/* a Season's ChildCount is its episode count. This row was empty before. */
if(info.sea>0)want.push(info.sea+(info.sea===1?' Episode':' Episodes'));
}
if(!want.length)return;
for(k=0;k<want.length;k++){
var d=document.createElement('div');
d.className='mediaInfoItem sf-meta-pill';
d.setAttribute('data-sf-for',id);
try{d.textContent=(window.sfTr?window.sfTr(want[k]):want[k]);}catch(e){d.textContent=want[k];}
host.appendChild(d);
}
}catch(e){}
}
function sfDetailBadges(){
if((location.hash||'').indexOf('#/details')!==0)return;
var pages=document.querySelectorAll('#itemDetailPage'),page=null,i;
for(i=0;i<pages.length;i++){
if(pages[i].offsetParent!==null&&pages[i].getBoundingClientRect().height>0){page=pages[i];break;}
}
if(!page)return;
var m=(location.hash||'').match(/[?&]id=([a-zA-Z0-9]+)/);
if(!m)return;
var id=m[1];
if(page.getAttribute('data-sf-badges')===id)return;
var host=page.querySelector('.itemMiscInfo');
if(!host)return;
var ac=window.ApiClient;
if(!ac||!ac.getItem||!ac.getCurrentUserId)return;
page.setAttribute('data-sf-badges',id);
ac.getItem(ac.getCurrentUserId(),id).then(function(it){
if(!it||page.getAttribute('data-sf-badges')!==id)return;
/* sf-meta-episodic (2026-09-04): stash what sfDetailMeta needs, from the request
   this function already makes. Written to the element so the pills can be
   rebuilt with no further network if Jellyfin re-renders its own metadata row. */
try{
page.setAttribute('data-sf-meta',JSON.stringify({
id:id,t:it.Type||'',
sea:it.ChildCount||0,epi:it.RecursiveItemCount||0,st:it.Status||''}));
}catch(e){}
var src=(it.MediaSources&&it.MediaSources[0])||{};
var st=src.MediaStreams||[];
var out=[],j,s;
var vid=null,bestCh=0,atmos=false,anySub=false,sdh=false;
for(j=0;j<st.length;j++){
s=st[j];
if(s.Type==='Video'&&!vid)vid=s;
if(s.Type==='Audio'){
var tag=((s.Profile||'')+' '+(s.DisplayTitle||'')+' '+(s.Codec||'')).toLowerCase();
if(tag.indexOf('atmos')>-1)atmos=true;
var ch=(s.ChannelLayout||'').match(/(\d)\.(\d)/);
if(ch){var n=parseFloat(ch[1]+'.'+ch[2]);if(n>bestCh)bestCh=n;}
}
if(s.Type==='Subtitle'){
anySub=true;
if(/sdh|hearing/i.test((s.Title||'')+' '+(s.DisplayTitle||'')))sdh=true;
}
}
if(vid){
var h=vid.Height||0;
if(h>=2000)out.push('4K');else if(h>=1000)out.push('HD');
var rng=(vid.VideoRangeType||vid.VideoRange||'').toUpperCase();
if(rng.indexOf('DOVI')>-1||rng.indexOf('DOLBY')>-1)out.push('Dolby Vision');
else if(rng.indexOf('HDR')>-1)out.push('HDR');
}
if(atmos)out.push('Dolby Atmos');
else if(bestCh>=7)out.push('7.1');
else if(bestCh>=5)out.push('5.1');
if(anySub)out.push('CC');
if(sdh)out.push('SDH');
if(!out.length)return;
var old=page.querySelector('.sf-badges');
if(old&&old.parentNode)old.parentNode.removeChild(old);
var box=document.createElement('div');
box.className='sf-badges';
for(j=0;j<out.length;j++){
var b=document.createElement('span');
b.className='sf-badge';
b.textContent=out[j];
box.appendChild(b);
}
/* after the metadata line, before the buttons -- the same place Apple puts it */
if(host.parentNode)host.parentNode.insertBefore(box,host.nextSibling);
}).catch(function(){});
}
/* sf-plot-above-eps (2026-09-04). The admin: on a movie the summary reads fine, but
   on a series "the description for the plot loading below that seasons row ...
   doesn't look good".
   Measured on a series: hero(centred) -> buttons 642 -> seasons row 789 ->
   plot 853 -> cast 1390. The plot block (.sf-dfacts) is centre-aligned to sit
   under the centred hero, which is exactly right on a movie -- but on a series
   the left-aligned episodes row lands between the two, so the centred paragraph
   is orphaned mid-page under a rule, matching nothing above or below it.
   CSS order cannot fix it: .sf-dfacts is the first child of .detailPageContent
   while .sf-epsrow lives in .detailPagePrimaryContent, a different container
   entirely. So move the node -- once, and only when it is not already in place. */
function sfPlotOrder(){
try{
if((location.hash||'').indexOf('#/details')!==0)return;
var ps=document.querySelectorAll('#itemDetailPage'),pg=null,i;
for(i=0;i<ps.length;i++){if(!ps[i].classList.contains('hide')&&ps[i].getClientRects().length){pg=ps[i];break;}}
if(!pg)return;
/* MOVING THE NODE DOES NOT WORK, and this is the record of why: sfDetailFacts
   rebuilds .sf-dfacts in .detailPageContent whenever it is not there, so lifting
   it into .detailPagePrimaryContent next to the episodes row simply produced a
   SECOND one -- measured two painted blocks at y=692 and y=1254, the same
   paragraph twice. Reordering has to happen inside sfDetailFacts, not by moving
   its output from underneath it.
   What is kept here is the de-duplication, which is worth having on its own:
   if more than one ever exists, only the first survives. */
var all=pg.querySelectorAll('.sf-dfacts'),k;
for(k=1;k<all.length;k++){if(all[k].parentNode)all[k].parentNode.removeChild(all[k]);}
}catch(e){}
}
/* sf-det-kick (2026-09-05). The admin: "it feels like the home page reloads ... lets
   get us into the new page instead of reloading the old page again".
   He is right, and the hold was not the cause -- the wait was. Broken down, click
   to visible:
       ~250ms   the detail page exists and its buttons are already PAINTED
       ~870-1600ms  data-sf-type lands -- sfDetailHero's own getItem, which only
                    starts when the 400ms tick gets round to it
       ~1100-1700ms composed;  ~1200-1800ms visible
   So the page was ready at a quarter second and we sat on Home for another 1.3s
   waiting for ourselves. Holding the outgoing page is what stops a blank; it is
   not supposed to be somewhere you dwell.
   Run sfDetailHero as soon as the route changes instead of up to a tick later. A
   bounded 25ms kick rather than adding it to the 30ms strip: it does layout reads
   on every call (ribbon rect, logo style) and this codebase has already paid for
   putting those on a fast loop. It stops the instant data-sf-atv is stamped --
   which is the first thing sfDetailHero does once it starts -- and gives up after
   1s regardless. */
var _sfDetKickT=0;
/* sf-det-prewarm (2026-09-05). sfDetailHero cannot start its item fetch until the
   page element exists AND has layout, and by then Jellyfin's page build is running
   and starving our timers -- measured the page laid out at 286ms and the fetch
   still not starting until ~700ms, whether it was driven from the 30ms strip, a
   25ms kick, or the CREATE observer.
   So do not schedule it. The item id is in the URL the instant the route changes,
   long before any DOM work begins, and the request needs no DOM at all. Fire it
   then and throw the result away: sf-coalesce caches an identical single-item GET
   for 2s (measured 113ms, then 0ms, 0ms), so sfDetailHero's own call resolves
   instantly whenever it finally gets to run.
   Costs one request that was going to be made anyway, a few hundred ms earlier. */
window.__sfDetWarm=function(h){
try{
var m=(h||location.hash||'').match(/[?&]id=([a-zA-Z0-9]+)/);
if(!m)return;
if(window.__sfWarmId===m[1])return;          /* already warmed this one */
var ac=window.ApiClient;
if(!ac||!ac.getItem||!ac.getCurrentUserId)return;
var uid=ac.getCurrentUserId();
if(!uid)return;
window.__sfWarmId=m[1];
ac.getItem(uid,m[1]).then(function(){},function(){});
}catch(e){}
};
window.__sfDetKick=function(){
try{
if(_sfDetKickT)clearInterval(_sfDetKickT);
var n=0;
_sfDetKickT=setInterval(function(){
n++;
try{sfDetailHero();}catch(e){}
var pg=null,ps=document.querySelectorAll('#itemDetailPage'),i;
for(i=0;i<ps.length;i++){if(!ps[i].classList.contains('hide')&&!ps[i].getAttribute('data-sf-clone')){pg=ps[i];break;}}
if(n>40||(pg&&pg.getAttribute('data-sf-atv'))){clearInterval(_sfDetKickT);_sfDetKickT=0;}
},25);
}catch(e){}
};
/* sf-det-load (2026-09-04). The admin: "the header can go missing as it was not
   showing". Measured home -> a detail page, which is what the report was
   demonstrating:
       t=60ms     #itemDetailPage exists, held at opacity 0 by the sf-atv gate
       t=470ms    still opacity 0 -- and the ONLY thing painted is the outgoing
                  home ambient wash: body::before at opacity .62,
                  blur(58px) saturate(170%) brightness(1.15), with body::after
                  fully transparent at the top
       t=790-980  .sf-atv lands and the page finally appears
   So for most of a second the whole screen is the PREVIOUS page's wash at full
   strength, and the only things over it are the header icons that happen to
   have rendered. A back arrow and a hamburger floating on a bright coloured
   smear is not a header, which is exactly what was reported.
   The dimmer detail treatment for that layer already exists in branding.xml; it
   was gated on .sf-atv, i.e. on the END of the wait. This publishes the route
   itself so the surface can be settled BEFORE the page lands, and the header's
   home button can be shown from the first frame instead of ~200ms late.
   A pure hash test, so it is safe on the 30ms strip. hashchange as well, for
   the same reason sf-music-solo-sync has it: it fires before the new page
   paints, so the class is never a frame behind the route. */
/* ---- sf-xfade (2026-09-04) -------------------------------------------------
   the admin: "click -> black screen -> load -> suddenly appear ... feels cheap".

   AUDITED FIRST, and the architecture turned out to be on our side. Instrumented
   a real Home -> Movie -> Back round trip by watching .page nodes on
   .mainAnimatedPages:

       t   0  NAV      -> details
       t  49  CREATE   itemDetailPage      the new page is in the DOM at 49ms
       t  87  HIDE     indexPage           Jellyfin hides the old one
       t4078  SHOW     indexPage           Back is a class removal: instant
       t4078  HIDE     itemDetailPage

   So Jellyfin CACHES views -- it never destroyed #indexPage, it added .hide
   (display:none) -- there is no native transition of any kind, and for ~38ms both
   pages are in the document. Every .page is already position:absolute;top:0 in a
   static host, so two of them OVERLAP natively: a cross-fade needs no layout
   change and no wrapper.

   The black gap was therefore never Jellyfin's. It is ours: sfDetailHero holds
   the incoming page at opacity 0 until its backdrop decodes, and Jellyfin has
   already hidden the outgoing page 500-1400ms earlier, so the screen has nothing
   on it but the ambient wash for the whole wait.

   Fix the lifecycle rather than the symptom: keep the page the user is looking at
   ON SCREEN until the next one is actually composed, then dissolve it away.

   The held page goes ON TOP (z-index:1, still under .skinHeader at 999), not
   underneath. A detail page is transparent over the wash, so cross-fading two
   translucent layers would ghost; fading only the outgoing one means the incoming
   is complete before a single pixel of it is visible, which is the stated
   requirement -- never an intermediate DOM state.

   We never touch Jellyfin's own .hide class. We override what it PAINTS, for a
   bounded window, on one element we tagged ourselves.

   Held on CREATE, not on HIDE: at 49ms the outgoing page is still visible, so
   tagging it there means the display override is already in place when Jellyfin
   hides it at 87ms and there is no frame in between.

   RETURNING TO A CACHED PAGE IS NOT ANIMATED. Back fires no CREATE at all, so no
   hold is armed and the swap stays instant -- an entrance replayed from zero on a
   page that is already rendered is exactly the "page reload" feeling being
   removed here.
*/
var XF_HELD=null,XF_CAP=0,XF_Y0=0,XF_SCROLL=null,XF_SIG='',XF_STABLE=0,XF_CLONE=null,XF_LASTHASH=null,XF_ARMED_AT=0,XF_PREREVEALED=false;
/* sf-xfade-reuse (2026-09-04). The CREATE-based hold covers home -> item, but
   Jellyfin REUSES #itemDetailPage when you go from one detail page to another,
   so no page is created, no hold is armed -- and sfDetailHero then strips
   .sf-atv to stop the old title and artwork morphing into the new ones, which
   drops the only thing on screen to opacity 0. Measured on the series -> season
   -> episode chain, the worst case in the whole app:
       series -> season      287-668ms blank
       back to series        284ms blank
       movie -> series -> movie  512ms blank
   The element cannot be held here -- it is the same element the incoming page
   is about to render into. So hold a COPY of it instead, and let the real page
   blank and rebuild underneath.
   Ids are stripped from the copy on purpose: this codebase resolves the detail
   page as #itemDetailPage in a dozen places and every one of them would
   otherwise find the copy as well. */
/* sf-xfade-noplayer (2026-09-04). The admin, with a recording: starting playback put
   the HOME Continue Watching row on top of the video, and it stayed there for
   seconds.
   Two of my own mechanisms combined to do it. Pressing Play creates a new .page
   for the player, so the CREATE observer armed a hold on whatever was on screen;
   and the release test asks whether the INCOMING page has painted cards, which a
   video player never has -- so nothing ever satisfied it and the held page sat
   over the picture until the 2.5s cap, fading out on top of the film.
   A held page must never be able to cover playback, so this is a hard rule
   rather than a tuning of the release test: do not arm into the player, and drop
   an existing hold IMMEDIATELY (no fade -- a fade is still 160ms of something
   over the video) the moment the player is up. */
function xfIsPlayer(){
try{
if((location.hash||'').indexOf('#/video')===0)return true;
var v=document.querySelector('#videoOsdPage,.videoPlayerContainer,.videoOsd');
if(v&&!v.classList.contains('hide')&&v.getClientRects().length)return true;
}catch(e){}
return false;
}
function xfClone(src){
try{
var c=src.cloneNode(true);
c.removeAttribute('id');
var ids=c.querySelectorAll('[id]'),i;
for(i=0;i<ids.length;i++)ids[i].removeAttribute('id');
c.className=src.className;              /* look identical */
c.setAttribute('data-sf-clone','1');
return c;
}catch(e){return null;}
}
/* sf-xfade-settled (2026-09-04). "No elements appearing in the wrong location."
   Traced the plot block on a real open, sampling every frame:
       SERIES  t606 .sf-atv lands, .sf-dfacts at y=693
               t697 page becomes VISIBLE, still y=693
               t746 .sf-dfacts jumps to y=556   <- 137px, 50ms after it is seen
       MOVIE   t750 visible, .sf-dfacts y=787
               t903 .sf-dfacts moves to y=808   <- 21px, after it is seen
   The page was being revealed mid-composition and then correcting itself in
   front of the user. "Composed" therefore cannot mean "has painted nodes";
   it has to mean the above-the-fold geometry has stopped moving.
   Cheap on purpose: a handful of rects on the incoming page only, and only
   while a transition is actually in flight. Three consecutive identical
   samples on the 30ms strip is ~60-90ms of stillness -- enough to catch a
   correction, short enough that it is not a delay. The 2.5s cap still wins,
   so a page that never settles cannot hold the old one on screen. */
function xfSig(el){
try{
/* .itemMiscInfo is in here because sfDetailMeta appends the episodic pills to it:
   measured buttons moving 142-151px AFTER the page was visible when that pill
   row grew a line late. Anything that can change the composition has to be able
   to hold the transition. */
var sel=['.mainDetailButtons','.sf-dfacts','.detailLogo','.sf-badges','.itemMiscInfo','.verticalSection','.itemsContainer'];
var parts=[],i,n,r;
for(i=0;i<sel.length;i++){
n=el.querySelector(sel[i]);
if(!n)continue;
r=n.getBoundingClientRect();
if(r.height>1)parts.push(Math.round(r.top)+':'+Math.round(r.height));
}
return parts.join('|');
}catch(e){return '';}
}
function xfPainted(el){
try{
/* the same painted-node scan sfRouteSkel uses, and for the same reason: a page
   element exists long before it has anything in it, and querySelector alone
   returns the first match, which is routinely an unpainted node. Strided so the
   cost stays bounded on a page with hundreds of cards. */
var n=el.querySelectorAll('.cardBox,.card,.listItem,.programCell,.detailPagePrimaryContainer,.sf-alb-hero,.verticalSection,.sf-ls-section,.jf-fwl-msg,.noItemsMessage,.emptyMessage'),i;
var step=n.length>120?Math.ceil(n.length/120):1;
for(i=0;i<n.length;i+=step){if(n[i].getClientRects().length)return true;}
}catch(e){}
return false;
}
/* sf-xfade-freeze (2026-09-05). The admin: the Continue Watching row still pops up on
   the info page, and it "feels like the same symptom" as the video player. It is
   the same symptom -- we were holding a page that had stopped being a valid thing
   to show.
   Measured, logging Media Bar's slide count against the navigation:
       t   3.1  before-nav   slides=4
       t  52    after-nav    slides=4     <- the hold arms here, hero intact
       t 200.5  frame        slides=0     <- Media Bar destroys its own hero
   We hold the LIVE element, so ~150ms into the hold the hero is torn out from
   under us and the held screen becomes a 732px hole with the Continue Watching
   row sitting under it. Nothing 'appears' -- everything else disappears, which is
   what makes the row look like it popped up on the detail page.
   So hold a FROZEN COPY, never the live page. The copy is taken while the hero is
   still there, and Media Bar's teardown then only affects the real page, which is
   hidden anyway. This is what the reuse path already did; it just was not applied
   to the one case where the outgoing page is Home. */
function xfFreeze(cur,host){
try{
if(!SF_HOLD_ENABLED)return false;
if(!cur||!host)return false;
var c=xfClone(cur);
if(!c)return false;
host.appendChild(c);
XF_CLONE=c;
xfHold(c);
xfFreezeHero();
return true;
}catch(e){return false;}
}
/* sf-clone-hero (2026-09-05). Freezing the PAGE was not enough, because the home
   hero is not in the page. Measured: #slides-container is a direct child of
   <body> -- a sibling of .mainAnimatedPages, 732px tall at y=0 -- so it belongs to
   no page and no page clone can contain it.
   That is the whole complaint. Leaving home, Media Bar empties that container and
   it collapses to height 0, so the top 732px of the held screen goes empty while
   the rows below stay exactly where they were. Nothing appears; the artwork
   vanishes and leaves Continue Watching as the first thing on screen, which is
   what reads as the row popping up on the info page.
   So freeze the hero too, as a fixed copy pinned where it was, at z-index 0 --
   under the held page (z-index 1) and above the ambient wash (z-index -1). */
/* sf-hero-lastknown (2026-09-05). The admin, with a third recording: clicking a movie
   still flickers -- the hero's logo and plot blink out and back over 2-3 frames,
   then ~0.7s of bare ambient wash with the Continue Watching row stranded under
   it.
   Both freeze paths asked the LIVE #slides-container for its size and artwork at
   the moment of navigation, and Media Bar collapses that container faster than
   any of our arm points can reach it -- the CREATE observer at ~49ms, the 30ms
   poll, the 400ms tick. When it has already gone to height 0 both paths bail and
   nothing is held, which is exactly the wash the recording shows.
   Stop racing it. Home is on screen and stable for seconds before any click, so
   record the artwork and its box THEN, cheaply, and freeze from the record. The
   snapshot no longer depends on catching the component alive. */
var SF_HERO_LAST=null;
function sfHeroRemember(){
try{
if((location.hash||'').indexOf('#/home')!==0)return;
if(XF_HELD)return;                       /* mid-transition: not a truth to record */
var sc=document.getElementById('slides-container');
if(!sc)return;
var r=sc.getBoundingClientRect();
if(r.height<100)return;
var im=sc.querySelector('.slide.active img.backdrop')||sc.querySelector('img.backdrop')||sc.querySelector('img');
if(!im||!im.getClientRects().length)return;
var src=im.currentSrc||im.getAttribute('src')||'';
if(!src)return;
SF_HERO_LAST={src:src,top:Math.round(r.top),h:Math.round(r.height)};
}catch(e){}
}
function xfFreezeHero(){
try{
var sc=document.getElementById('slides-container');
var r=sc?sc.getBoundingClientRect():null;
var img=sc?sc.querySelector('img'):null;
var painted=!!(img&&img.getClientRects().length&&r&&r.height>=100);
/* the live container has already collapsed -- use what Home looked like before
   the click, which is the same picture the user was just looking at */
if(!painted&&!SF_HERO_LAST)return;
if(!r||r.height<100)r={top:SF_HERO_LAST.top,height:SF_HERO_LAST.h};
/* sf-clone-hero-paint (2026-09-05). Cloning the live Media Bar component works
   when its slides are still mounted, and silently does nothing when they are not
   -- which is what the admin's recording shows: the frozen Home holds the Continue
   Watching row correctly while the top 732px is bare ambient wash, a saturated
   blur with no artwork in it. The clone had bailed.
   Do not depend on the component. What has to survive the transition is the
   PICTURE, and its URL is knowable even when the slides are half torn down: the
   active backdrop's currentSrc, or failing that --sf-pagebg, which sfPageBg keeps
   pointed at the same artwork. One div with a background-image cannot be defeated
   by lazy loading, a rebuilt slide list, or a carousel mid-rotation. */
var h,i,ids;
if(painted){
h=sc.cloneNode(true);
h.removeAttribute('id');
ids=h.querySelectorAll('[id]');
for(i=0;i<ids.length;i++)ids[i].removeAttribute('id');
}else{
var src='';
try{
var a=sc?(sc.querySelector('.slide.active img.backdrop')||sc.querySelector('img.backdrop')||sc.querySelector('img')):null;
if(a)src=a.currentSrc||a.getAttribute('src')||'';
if(!src&&SF_HERO_LAST)src=SF_HERO_LAST.src;
if(!src){
var pb=getComputedStyle(document.body).getPropertyValue('--sf-pagebg')||'';
var m=/url\(["']?(.*?)["']?\)/.exec(pb);
if(m)src=m[1];
}
}catch(e){}
if(!src)return;                                /* genuinely nothing to hold */
h=document.createElement('div');
/* sf-hero-frozen-scrim: the picture alone is not what was on screen -- the real
   hero sits under a scrim that darkens toward the bottom so the rows below stay
   readable. Without it the frozen frame is markedly brighter than the Home it is
   standing in for, which reads as a flash of its own. Same gradient the page scrim
   already uses (body.sf-has-pagebg::after), so this borrows the existing treatment
   rather than inventing a second one. */
h.style.backgroundImage='linear-gradient(180deg,rgba(12,12,14,0) 0%,'+
'rgba(12,12,14,.20) 34%,rgba(12,12,14,.55) 70%,rgba(12,12,14,.72) 100%),'+
'url("'+src+'")';
h.style.backgroundSize='cover,cover';
h.style.backgroundPosition='center top,center top';
h.style.backgroundRepeat='no-repeat,no-repeat';
}
h.setAttribute('data-sf-clone-hero','1');
h.style.position='fixed';h.style.left='0';h.style.right='0';
h.style.top=Math.round(r.top)+'px';
h.style.height=Math.round(r.height)+'px';
h.style.zIndex='0';h.style.pointerEvents='none';
h.setAttribute('aria-hidden','true');
document.body.appendChild(h);
}catch(e){}
}
function xfDrop(animate){
var el=XF_HELD;XF_HELD=null;
/* Unconditional, and before any early return: whatever else happens, nothing may
   be left holding a page invisible. */
try{
document.documentElement.classList.remove('sf-xf-active');
var un=document.querySelectorAll('.page.sf-xf-under'),u2;
for(u2=0;u2<un.length;u2++)un[u2].classList.remove('sf-xf-under');
var hc=document.querySelectorAll('[data-sf-clone-hero]'),h2;
for(h2=0;h2<hc.length;h2++)if(hc[h2].parentNode)hc[h2].parentNode.removeChild(hc[h2]);
}catch(e){}
if(XF_SCROLL){try{window.removeEventListener('scroll',XF_SCROLL);}catch(e){}XF_SCROLL=null;}
if(!el)return;
var fin=function(){try{
try{document.documentElement.classList.remove('sf-xf-active');}catch(e){}
/* the header settled behind the snapshot; publish it now, in the same task the
   incoming page becomes visible, so it is revealed with final geometry */
try{if(window.__sfHdrVar)window.__sfHdrVar();}catch(e){}
/* let the next reveal animate normally */
var hp=el.parentNode,z;
if(hp)for(z=0;z<hp.children.length;z++){
if(hp.children[z].classList)hp.children[z].classList.remove('sf-xf-instant');
}
if(el===XF_CLONE){XF_CLONE=null;if(el.parentNode)el.parentNode.removeChild(el);return;}
el.classList.remove('sf-xf-hold');
el.classList.remove('sf-xf-out');
el.style.translate='';
el.removeAttribute('aria-hidden');
}catch(e){}};
/* One animated layer, not two. The incoming page is complete underneath, so the
   old screen dissolving away IS the reveal; letting jfAtvIn run at the same time
   means both layers are semi-transparent at once, which is what reads as two
   screens on top of each other. Snap the incoming page in (invisible -- it is
   still covered) and animate only the one that is leaving. */
try{
var host2=el.parentNode,i2,ch2=host2?host2.children:[];
for(i2=0;i2<ch2.length;i2++){
var q2=ch2[i2];
if(q2===el||!q2.classList||!q2.classList.contains('page'))continue;
if(q2.classList.contains('hide')||q2.getAttribute('data-sf-clone'))continue;
q2.classList.add('sf-xf-instant');
}
}catch(e){}
if(!animate){fin();return;}
try{el.classList.add('sf-xf-out');}catch(e){fin();return;}
/* comfortably past the transition; the class is what keeps it painted, so this
   must not fire early */
/* just past the 160ms dissolve: the class is what keeps the node painted, so
   this must not fire early, but there is no reason to keep an invisible page
   in the paint tree either */
setTimeout(fin,240);
}
/* sf-hold-off (2026-09-05). The admin: "lets stop holding pages please. its causing
   many bugs". He is right, and this is the honest reckoning.
   Holding the outgoing page removed the black gap, and every subsequent bug came
   from the same idea: Home's Continue Watching row painting over a detail page;
   the hero freezing as a bare rainbow wash because Media Bar tore its slides down
   first; the login form left on screen over a loaded Home; and the wait itself
   reading as Home re-rendering rather than as going into the title. Each fix was
   sound and each exposed the next one, which is the signal that the approach --
   not the implementation -- was wrong.
   A snapshot of the previous screen is a lie about what the app is doing. The
   destination page is painted by Jellyfin at ~240ms; showing THAT is both faster
   and truthful, and it needs no clones of pages, heroes or headers.
   Left as one switch rather than deleted: the measurements and the reasoning above
   are the most expensive thing learned tonight, and turning it back on is one
   word if a blank gap ever proves worse than what it cost. */
var SF_HOLD_ENABLED=false;
function xfHold(el){
if(!SF_HOLD_ENABLED)return;
if(xfIsPlayer())return;                 /* see sf-xfade-noplayer */
if(XF_HELD===el)return;
xfDrop(false);                       /* a second navigation retires the first hold */
XF_HELD=el;
XF_ARMED_AT=Date.now();
/* Was the destination ALREADY composed for this exact item when we armed? Opening
   an item you opened before finds its cached view still carrying .sf-atv and the
   right data-sf-atv, and sfDetailHero returns early rather than revealing it again
   -- so there is no fresh reveal to wait for, and requiring one held the outgoing
   page for the full 6s failsafe. Measured: 4878ms of Home sitting over the detail
   page on the second and third open of the same item.
   Nothing to rebuild means nothing to wait for. */
XF_PREREVEALED=false;
try{
var wm0=(location.hash||'').match(/[?&]id=([a-zA-Z0-9]+)/);
if(wm0){
var ps0=document.querySelectorAll('#itemDetailPage'),i0;
for(i0=0;i0<ps0.length;i0++){
if(ps0[i0]===el)continue;
if(ps0[i0].getAttribute('data-sf-clone'))continue;
if(ps0[i0].classList.contains('sf-atv')&&ps0[i0].getAttribute('data-sf-atv')===wm0[1])
XF_PREREVEALED=true;
}
}
}catch(e){}
XF_SIG='';XF_STABLE=0;
XF_CAP=Date.now()+2500;              /* a page that never composes cannot freeze the UI */
try{
/* Keep showing the PIXELS the user was looking at. The page is
   position:absolute;top:0 and the document scroller resets to 0 on navigation,
   so without this a held page that was scrolled down would jump to its own top --
   a worse artefact than the gap being removed. transform only: compositor work,
   no reflow, and the page is not re-laid-out to hold it. */
var se=document.scrollingElement||document.documentElement;
XF_Y0=se?(se.scrollTop||0):0;
var put=function(){try{
var s=document.scrollingElement||document.documentElement;
var d=(s?(s.scrollTop||0):0)-XF_Y0;
/* the INDIVIDUAL translate property, not `transform`: the departing page also
   carries a scale from CSS (see sf-xf-out), and one `transform` cannot hold
   both a value only JS knows and one only CSS knows. translate/scale compose. */
el.style.translate=d?('0 '+d+'px'):'';
}catch(e){}};
el.classList.add('sf-xf-hold');
try{document.documentElement.classList.add('sf-xf-active');}catch(e){}
/* every page that is NOT the held one is behind it and not ready to be seen */
try{
var hp2=el.parentNode,z2;
if(hp2)for(z2=0;z2<hp2.children.length;z2++){
var q3=hp2.children[z2];
if(q3===el||!q3.classList||!q3.classList.contains('page'))continue;
q3.classList.add('sf-xf-under');
}
}catch(e){}
el.setAttribute('aria-hidden','true');   /* one screen, one accessibility tree */
put();
XF_SCROLL=put;
window.addEventListener('scroll',put,{passive:true});
}catch(e){xfDrop(false);}
}
function sfXfade(){
/* sf-hold-sweep: clear anything an earlier build (or an interrupted transition)
   left in the document. A stranded .sf-xf-hold is display:block!important on a
   page Jellyfin has hidden -- which is exactly how the login form ended up sitting
   over a loaded Home -- and a stranded .sf-xf-under holds a page invisible. */
try{
var junk=document.querySelectorAll('.sf-xf-hold,.sf-xf-under,.sf-xf-out,[data-sf-clone],[data-sf-clone-hero],[data-sf-clone-hdr]'),j;
for(j=0;j<junk.length;j++){
var q=junk[j];
if(q.getAttribute('data-sf-clone')||q.getAttribute('data-sf-clone-hero')||q.getAttribute('data-sf-clone-hdr')){
if(q.parentNode)q.parentNode.removeChild(q);
continue;
}
q.classList.remove('sf-xf-hold');q.classList.remove('sf-xf-under');q.classList.remove('sf-xf-out');
q.style.translate='';q.removeAttribute('aria-hidden');
}
if(document.documentElement.classList.contains('sf-xf-active'))
document.documentElement.classList.remove('sf-xf-active');
}catch(e){}
var host=document.querySelector('.mainAnimatedPages');
if(!host)return;
if(!window.__sfXfade){
window.__sfXfade=1;
/* childList on the host ONLY -- pages are direct children and are created a
   handful of times per session. Watching class attributes across the subtree
   instead would mean a callback for every class Jellyfin toggles, which on a
   page swap is hundreds. */
try{
new MutationObserver(function(muts){
try{
var i,j,added=null;
for(i=0;i<muts.length;i++){
for(j=0;j<muts[i].addedNodes.length;j++){
var n=muts[i].addedNodes[j];
if(n.nodeType===1&&n.classList&&n.classList.contains('page'))added=n;
}
}
if(!added)return;
/* sf-xf-under-new (2026-09-05): a page CREATED after the freeze was armed never
   got the suppression class -- xfHold can only mark the siblings that exist at
   that moment -- so it faded in underneath the held copy and both were on screen
   together. Measured 1016ms of it on Home -> TV Show. The incoming page is
   created ~49ms after the freeze, i.e. essentially always. */
try{if(XF_HELD&&added!==XF_HELD)added.classList.add('sf-xf-under');}catch(e){}
/* sf-det-kick-oncreate (2026-09-05). Start the detail page's own work the instant
   the page element appears, which is the earliest moment it can possibly run.
   The 30ms strip is not that moment: measured, the route-change poll fired at
   646ms while the page had existed and been laid out since 286ms. Jellyfin's page
   build starves the interval, so a timer cannot be the thing that reacts to it.
   This observer is synchronous with the insertion, so it cannot be starved by the
   work that caused it. */
try{if(added.id==='itemDetailPage'&&window.__sfDetKick)window.__sfDetKick();}catch(e){}
/* the page the user is looking at right now: still un-hidden, not the new one */
var pages=host.children,k,out=null;
for(k=0;k<pages.length;k++){
var q=pages[k];
if(q===added||!q.classList||!q.classList.contains('page'))continue;
if(q.classList.contains('hide'))continue;
if(!q.getClientRects().length)continue;
out=q;
}
if(!out)return;
/* Nothing to cover: if the incoming page is somehow already composed, swapping
   straight to it is better than animating over it. */
if(xfPainted(added)&&(+getComputedStyle(added).opacity>0.01))return;
/* an earlier hook may already have frozen this navigation; that copy was taken
   sooner and is the better one */
if(XF_HELD)return;
xfFreeze(out,host);
}catch(e){}
}).observe(host,{childList:true});
}catch(e){}
/* hashchange fires while the outgoing page is still painted, which is the only
   moment a faithful copy can be taken. Scoped to detail -> detail: home -> item
   is already covered by CREATE, and cloning home (hundreds of cards) on every
   navigation would be real work to solve a problem that does not exist there. */
/* Named, because hashchange is NOT enough: Jellyfin navigates with
   history.pushState, which fires neither hashchange nor popstate -- the same
   fact sfNavSwap documents and wraps for. Wiring this to hashchange alone is
   why the first version of the reuse hold only fired occasionally: measured
   series -> season still blanking for 232ms with the copy never taken. */
function xfReuseArm(){
try{
if((location.hash||'').indexOf('#/details')!==0)return;
if(XF_HELD)return;
/* sf-xfade-nothing-to-cover (2026-09-05). A hold exists to cover a page that is
   not ready. If the destination is ALREADY composed -- which is the normal case
   going Back, where Jellyfin has a finished cached view per URL -- there is
   nothing to cover, and arming anyway did active harm: the clone put
   sf-xf-under on the finished page, and releasing it ran fin(), which strips
   sf-xf-instant, so jfAtvIn started over and faded a complete page up from zero.
   Measured Episode -> Back -> Season: hold armed t68, released t115, page still
   at opacity 0 and only reaching 0.16 at t137.
   Leave it alone. The poll has already marked it sf-xf-instant, so it appears
   at once -- which is what returning to a rendered page should do. */
try{
var _wm=(location.hash||'').match(/[?&]id=([a-zA-Z0-9]+)/);
if(_wm){
var _dd=document.querySelectorAll('#itemDetailPage'),_k;
for(_k=0;_k<_dd.length;_k++){
if(_dd[_k].getAttribute('data-sf-clone'))continue;
if(_dd[_k].classList.contains('hide'))continue;
if(_dd[_k].classList.contains('sf-atv')&&_dd[_k].getAttribute('data-sf-atv')===_wm[1])return;
}
}
}catch(e){}
var h2=document.querySelector('.mainAnimatedPages');
if(!h2)return;
var ch=h2.children,i,cur=null;
for(i=0;i<ch.length;i++){
var e2=ch[i];
if(!e2.classList||!e2.classList.contains('page'))continue;
if(e2.classList.contains('hide')||e2.classList.contains('sf-xf-hold'))continue;
if(!e2.getClientRects().length)continue;
cur=e2;
}
if(!cur)return;
if(+getComputedStyle(cur).opacity<=0.01)return;
if(!xfPainted(cur))return;
/* sf-xfade-cached (2026-09-04). Only a page that is about to be RE-RENDERED has
   to be copied. Coming from anywhere other than a detail page -- Home, a
   library, My Stuff -- the incoming detail page is a different element, so the
   outgoing one can simply be held, exactly as on the CREATE path, with no copy
   and no duplicated DOM.
   This is the case that was still slipping through: Jellyfin caches views, so
   opening an item you have opened before fires no CREATE at all and nothing was
   armed. Measured 34ms blank and a 24-30px settle on every repeat open. */
xfFreeze(cur,h2);
}catch(e){}
}
/* Capture phase: our listener is registered after Jellyfin's, and on Back its
   handler hides the outgoing page before ours runs -- there is then nothing left
   to copy and the screen blanks anyway (measured 173ms on Season -> back to
   Series). Capture listeners on window run before bubble listeners on window,
   which puts us ahead of it without touching its code. */
window.__sfXfArm=xfReuseArm;
/* sf-det-kick-onnav (2026-09-05). The CREATE observer is not enough: Jellyfin
   caches one view per URL, so re-opening an item fires no CREATE at all and the
   kick never started. Measured on exactly that path -- every guard sfDetailHero
   checks was satisfied at t=268 (route, page found and laid out, --sf-brand, api,
   ribbon) yet data-sf-atv was not stamped until t=616, because nothing CALLED it
   for 348ms. The 400ms tick was the only thing that ever did.
   Start the kick from the navigation itself, which happens whether or not a page
   is created. Its interval stops the moment data-sf-atv is stamped, so on a warm
   path it costs one or two extra calls. */
try{window.addEventListener('hashchange',function(){
try{window.__sfDetWarm();}catch(e){}
try{if((location.hash||'').indexOf('#/details')===0&&window.__sfDetKick)window.__sfDetKick();}catch(e){}
},true);}catch(e){}
try{window.addEventListener('hashchange',xfReuseArm,true);}catch(e){}
try{window.addEventListener('popstate',xfReuseArm,true);}catch(e){}
try{
['pushState','replaceState'].forEach(function(k){
var orig=history[k];
if(!orig||orig.__sfXf)return;
var w=function(){var r=orig.apply(this,arguments);
try{if(window.__sfDetWarm)window.__sfDetWarm();}catch(e){}
try{if((location.hash||'').indexOf('#/details')===0&&window.__sfDetKick)window.__sfDetKick();}catch(e){}
try{xfReuseArm();}catch(e){}return r;};
w.__sfXf=1;
history[k]=w;
});
}catch(e){}
}
/* sf-xfade-poll (2026-09-04). The event route is not reliable here. Traced a
   Season -> Back -> Series: clone=n held=n on every frame while the page blanked
   for 271ms and then faded itself back in -- neither popstate nor hashchange ever
   reached this code. Ours is registered after Jellyfin's own router and something
   ahead of us stops the event; capture phase does not help, because for an event
   dispatched AT window the capture and bubble lists collapse into registration
   order.
   So do not depend on being told. The route is readable, this runs every 30ms,
   and the outgoing page stays paintable for ~80ms after Back -- more than a tick.
   The listeners stay as the faster path when they do fire. */
/* Checked before anything else, and on every tick: playback can begin without a
   route change of its own, and nothing we own may be left on top of it. */
if(xfIsPlayer()){
if(XF_HELD)xfDrop(false);
XF_LASTHASH=location.hash||'';
return;
}
var _h=location.hash||'';
if(_h!==XF_LASTHASH){
var _first=(XF_LASTHASH===null);
XF_LASTHASH=_h;
/* sf-xfade-cachedin (2026-09-05). The deep-back "blank window" is not a blank at
   all -- it is an entrance replaying on a page that was already finished.
   Traced Episode -> Back -> Season, frame by frame:
       t 0   episode page visible, opacity 1
       t36   a DIFFERENT #itemDetailPage is visible (3 exist -- Jellyfin caches one
             view per URL), already .sf-atv, already painted, correct data-sf-atv
             ...and at opacity 0.00
       t53   opacity 0.16, climbing
   Nothing was missing: the season page was complete. Un-hiding an element
   restarts its CSS animations, so jfAtvIn ran again and faded a finished page up
   from nothing over ~280ms. No hold arms here either, because no page is created
   and sfDetailHero's item-changed branch never fires -- the incoming element
   already carries the right id.
   A page that is already composed for the route being entered must appear at
   once. sf-xf-instant already means exactly that, so reuse it rather than adding
   a second mechanism. Cleared on every route change so a genuine first reveal
   still animates. */
try{
var _pgs=document.querySelectorAll('.mainAnimatedPages > .page.sf-xf-instant'),_i;
for(_i=0;_i<_pgs.length;_i++)_pgs[_i].classList.remove('sf-xf-instant');
var _im=_h.match(/[?&]id=([a-zA-Z0-9]+)/);
if(_im){
var _ds=document.querySelectorAll('#itemDetailPage'),_j;
for(_j=0;_j<_ds.length;_j++){
if(_ds[_j].getAttribute('data-sf-clone'))continue;
if(_ds[_j].classList.contains('sf-atv')&&_ds[_j].getAttribute('data-sf-atv')===_im[1])
_ds[_j].classList.add('sf-xf-instant');
}
}
}catch(e){}
if(_h.indexOf('#/details')===0&&window.__sfDetWarm){try{window.__sfDetWarm(_h);}catch(e){}}
if(_h.indexOf('#/details')===0&&window.__sfDetKick){try{window.__sfDetKick();}catch(e){}}
if(!_first&&!XF_HELD&&_h.indexOf('#/details')===0&&window.__sfXfArm){
try{window.__sfXfArm();}catch(e){}
}
}
if(!XF_HELD)return;
/* Two ceilings. The soft one gives up on waiting for stillness but still
   requires the incoming page to be painted and visible -- dropping the hold
   before that is how the cap itself produced an 864ms blank on One Piece. The
   hard one is the real failsafe and releases no matter what, so a page that
   never arrives cannot strand the user on the previous screen. */
var _soft=Date.now()>XF_CAP, _hard=Date.now()>XF_CAP+3500;
if(_hard){xfDrop(true);return;}
/* release as soon as the incoming page is BOTH composed and actually visible.
   Opacity matters: a detail page is laid out (so it scores as painted) while
   sfDetailHero still holds it at opacity 0, and releasing on layout alone would
   put the gap straight back. */
var ch=host.children,c,inc=null;
for(c=0;c<ch.length;c++){
var e2=ch[c];
if(e2===XF_HELD||!e2.classList||!e2.classList.contains('page'))continue;
if(e2.classList.contains('hide'))continue;
if(e2.getAttribute('data-sf-clone'))continue;
inc=e2;
}
if(!inc)return;
/* sf-xfade-deadlock (2026-09-05). The admin: "it takes a long time from when i press
   and when the info page shows up". Measured, and the wait was entirely
   self-inflicted:
       page composed (.sf-atv)  ~1150-1420ms
       hold released            ~3070-3390ms      <- the 2500ms soft cap
       user sees the page       ~3100-3450ms
   Two seconds of holding a page that had been ready the whole time. This line was
   the cause: it required the incoming page to be visible before releasing, and
   sf-xf-under now deliberately forces that page to opacity 0 for the duration of
   the hold. The readiness test was waiting for the very thing the hold prevents,
   so every transition ran to the cap.
   Opacity is no longer evidence of anything here -- suppression guarantees it is
   0. Readiness is .sf-atv plus a fresh reveal for a detail page, and painted
   content for everything else, both of which are unaffected by opacity. */
if(!xfPainted(inc))return;
/* sf-xfade-newitem (2026-09-04). On the REUSE path the incoming page is the
   same element that is still showing the PREVIOUS item, so 'has painted nodes'
   and 'geometry is stable' are both trivially true the instant we start -- the
   hold was released immediately, sfDetailHero then stripped .sf-atv to swap the
   item, and the screen went blank anyway. Measured 304ms on Season -> back to
   Series with the copy correctly taken and correctly discarded, far too early.
   A detail page is only finished when sfDetailHero says so, and it already says
   so precisely: .sf-atv plus data-sf-atv stamped with THIS id. Use its signal
   rather than inferring one. */
try{
if((location.hash||'').indexOf('#/details')===0&&inc.id==='itemDetailPage'){
var wm=(location.hash||'').match(/[?&]id=([a-zA-Z0-9]+)/);
var wid=wm?wm[1]:'';
if(!inc.classList.contains('sf-atv'))return;
if(wid&&inc.getAttribute('data-sf-atv')!==wid)return;
/* sf-fresh-reveal (2026-09-05). Going Back to an item visited earlier, the page
   still carried .sf-atv and a matching data-sf-atv from that visit, so this gate
   passed on the very first tick -- we cut to it, and sfDetailHero then rebuilt it
   and blanked the screen for ~200ms. (The old dissolve had been hiding this: its
   160ms fade covered the gap the cut exposes.) Require a reveal that happened
   AFTER this transition was armed, which is the difference between 'composed'
   and 'composed for this navigation'. */
if(!XF_PREREVEALED&&+(inc.getAttribute('data-sf-atv-at')||0)<=XF_ARMED_AT)return;
}
}catch(e){}
/* ...and hold until it has stopped moving. See sf-xfade-settled above. */
/* sf-xfade-release (2026-09-05). The admin, with a recording: Home's Continue
   Watching row appeared layered into the detail page hero. Traced it -- the row
   is NOT a component on the detail page, it belongs to #indexPage, and #indexPage
   was the HELD page:
       t 67   hold armed, home opacity 1, detail 0
       t608   .sf-atv lands: the detail page is composed and starts revealing
       t763   detail opacity 0.16 while home is STILL at 1.00
       t1070  home finally released
   ~460ms of the incoming page fading in UNDERNEATH a fully opaque outgoing one.
   Home's hero region is empty by then (Media Bar is torn down), so the detail
   backdrop and logo showed through it while home's Continue Watching row kept
   painting on top -- exactly what the recording shows.
   The hold exists to cover the gap BEFORE the incoming page is ready. Once that
   page has revealed, holding is not caution, it is the bug. Release on the
   reveal signal itself.
   The three-frame stability wait that used to be here is gone deliberately: it
   was added BEFORE the --sf-ribbon-h ResizeObserver, it was measured NOT to fix
   the shift it was aimed at (time-to-visible went to 3.6s and the shift stayed),
   and the ResizeObserver is what actually fixed it. Keeping both meant paying
   for the same guarantee twice, in the one place where the cost is visible. */
/* sf-xfade-cut (2026-09-05). The admin, twice: Home's Continue Watching row is still
   visible over the detail page. It was, for 62-222ms -- and it is the DISSOLVE
   itself, not a timing bug. Neither page is opaque (both are transparent over the
   shared ambient wash), so for the whole length of any cross-fade both screens
   composite. Shortening it and front-loading the curve only made the window
   smaller; it cannot make it empty.
   The incoming page is COMPLETE at this point -- that is what we waited for -- so
   there is nothing to ease into. Replace it in one frame: complete screen to
   complete screen, which is a cut, and reads as decisive rather than abrupt
   because neither side is ever half-built. Fast, not theatrical.
   The dissolve survives on the CAP path below, where the incoming page may not
   be ready and a softer exit is the better failure mode. */
xfDrop(false);
}
function sfDetRoute(){
/* sf-xfade-bg (2026-09-04): NOT while a page is being held. The wash is a
   layer of the screen the user is still looking at -- switching it to the
   detail treatment the instant the hash changes visibly dimmed the outgoing
   page while it was still the only thing on screen. The surface now changes
   WITH the page it belongs to, which is what makes the two read as one
   transition rather than two events. */
/* The hold is armed by a MutationObserver when Jellyfin CREATES the incoming
   page (~49ms), but the 30ms strip runs before that, so for one tick XF_HELD
   was still null on a hash that already said #/details -- measured as the wash
   stepping .62 -> .34 -> .62 -> .34 under a page that had not moved.
   sfNavSwap already publishes html.sf-nav-swap synchronously on every
   navigation and clears it after 320ms, which is exactly 'a transition is
   starting, do not repaint the surface yet'. Use it rather than inventing a
   second flag. A COLD load straight to a detail URL has neither a swap nor a
   hold, so it still gets the treatment immediately, which is the case the
   dimming was written for. */
var _de=document.documentElement;
document.documentElement.classList.toggle('sf-det-load',
  (location.hash||'').indexOf('#/details')===0&&!XF_HELD&&!_de.classList.contains('sf-nav-swap'));
}
/* Deliberately NOT wired to hashchange. hashchange fires BEFORE Jellyfin
   creates the incoming page, so XF_HELD is still null at that instant and the
   wash switched to the detail treatment for one tick while the outgoing page
   was still the only thing on screen -- measured as .62 -> .34 -> .62 ->
   .34, a visible dim-and-recover under a page that had not moved. The 30ms
   strip owns it instead: by the time it runs, the hold is armed. */
function sfDetailHero(){
if((location.hash||'').indexOf('#/details')!==0)return;
var pages=document.querySelectorAll('#itemDetailPage'),page=null,i;
for(i=0;i<pages.length;i++){
if(pages[i].offsetParent!==null&&pages[i].getBoundingClientRect().height>0){page=pages[i];break;}
}
if(!page)return;
var m=(location.hash||'').match(/[?&]id=([a-zA-Z0-9]+)/);
if(!m)return;
var id=m[1];
/* sf-det-latefade failsafe. The normal release is bdLanded(), the moment the
   artwork decodes; this only covers an image that never arrives at all, so a
   page revealed on the cap can never be left with an invisible backdrop. */
try{
if(page.classList.contains('sf-bd-late')&&!page.classList.contains('sf-bd-in')){
var _bl=+(page.getAttribute('data-sf-bdlate')||0);
if(_bl&&Date.now()-_bl>2600)page.classList.add('sf-bd-in');
}
}catch(e){}
/* Re-checked every tick, not once: the logo arrives asynchronously, so a single
   check at paint time would usually run before it and latch the wrong answer. */
var lg=page.querySelector('.detailLogo');
var hasLogo=!!(lg&&getComputedStyle(lg).backgroundImage!=='none');
if(page.classList.contains('sf-haslogo')!==hasLogo)page.classList.toggle('sf-haslogo',hasLogo);
/* The page's own top padding clears the fixed header and is NOT constant --
   measured 125px on a movie and a season page but 81px on a series page. The
   hero offset has to subtract the real value or the ribbon rides up over the
   logo (measured 94px of overlap). Re-read each tick: the header grows as its
   tabs render. */
var pad=getComputedStyle(page).paddingTop;
if(page.style.getPropertyValue('--sf-pagepad')!==pad)page.style.setProperty('--sf-pagepad',pad);
/* The hero text block is anchored to the BOTTOM of the hero, not offset from its
   top, because its height is not constant: a movie carries an original-title
   line and capability badges that a series does not, so a fixed offset put the
   buttons in a different place on each. Publishing the measured height lets one
   rule land every page type at the same distance from the hero's lower edge.
   No feedback loop: moving the block does not change how tall it is. */
var rb=page.querySelector('.detailRibbon');
/* sf-ribbon-live (2026-09-04). This measurement drives the position of
   EVERYTHING below the ribbon, and it was taken on the 400ms tick -- so the
   published value was stale for up to a tick, and the page corrected itself
   in front of the user. Traced frame by frame:
     SERIES  t713 .sf-atv lands: real ribbon 122 -> 229px, --sf-ribbon-h still
                  122px, buttons at y=621
             t1023 the tick catches up, --sf-ribbon-h -> 229px, buttons snap
                  621 -> 514  (107px, 310ms AFTER the page was on screen)
     MOVIE   same shape, 21-31px, twice on the way in
   Adding .sf-atv is what resizes the ribbon (the logo grows 130 -> 172 and the
   stock title collapses), so the change is instantaneous and a poll can only
   ever be late. A ResizeObserver runs after layout and before paint, so the
   property is correct in the SAME frame and nothing below it ever moves.
   Safe against feedback, for the reason the original note gives: moving the
   block does not change how tall the ribbon is. The tick assignment below
   stays as a backstop and simply becomes a no-op. */
try{
if(rb&&window.ResizeObserver){
if(!page.__sfRibRO){
var _rp=page;
page.__sfRibRO=new ResizeObserver(function(){
try{
var r2=_rp.querySelector('.detailRibbon');
if(!r2)return;
var rr=r2.getBoundingClientRect();
var h2=Math.round(rr.height)+'px';
if(h2!=='0px'&&_rp.style.getPropertyValue('--sf-ribbon-h')!==h2)
_rp.style.setProperty('--sf-ribbon-h',h2);
/* sf-ribbon-bottom: where the hero block ENDS, in document coordinates. The plot
   sits immediately after the ribbon now, so this is the one number the CSS needs
   to push it past the first viewport -- and publishing it from the same callback
   means it is correct in the same frame the ribbon changes, never a tick late. */
var sc=document.scrollingElement||document.documentElement;
var bb=Math.round(rr.bottom+(sc?sc.scrollTop:0))+'px';
if(bb!=='0px'&&_rp.style.getPropertyValue('--sf-ribbon-bottom')!==bb)
_rp.style.setProperty('--sf-ribbon-bottom',bb);
}catch(e){}
});
}
if(page.__sfRibNode!==rb){
page.__sfRibRO.disconnect();
page.__sfRibRO.observe(rb);
page.__sfRibNode=rb;
}
}
}catch(e){}
if(rb){
var rbr=rb.getBoundingClientRect();
var rh=Math.round(rbr.height)+'px';
if(rh!=='0px'&&page.style.getPropertyValue('--sf-ribbon-h')!==rh)
page.style.setProperty('--sf-ribbon-h',rh);
var sc2=document.scrollingElement||document.documentElement;
var bb2=Math.round(rbr.bottom+(sc2?sc2.scrollTop:0))+'px';
if(bb2!=='0px'&&page.style.getPropertyValue('--sf-ribbon-bottom')!==bb2)
page.style.setProperty('--sf-ribbon-bottom',bb2);
}
if(page.getAttribute('data-sf-atv')===id)return;
var ac=window.ApiClient;
if(!ac||!ac.getItem||!ac.getCurrentUserId)return;
/* Do not reveal until the branding sheet is live -- see sf-brand-ready. Without
   this the class can land first and the page appears in the STOCK layout, which
   is the flash we are removing. */
if(!getComputedStyle(document.documentElement).getPropertyValue('--sf-brand'))return;
/* MOVING BETWEEN ITEMS. Jellyfin reuses this node, so without hiding it again
   the previous title and artwork stay on screen and morph into the new ones.
   Hide first, and drop everything derived from the old item so each piece is
   rebuilt rather than patched. */
var prev=page.getAttribute('data-sf-atv');
if(prev&&prev!==id){
/* sf-xfade-atsource (2026-09-04). Arm the transition HERE, at the exact
   instant we decide to blank the page, rather than racing to notice the route
   change from outside.
   Every other trigger was a guess about timing and each one lost: popstate and
   hashchange never arrive (Jellyfin's router stops them), pushState is not
   called on Back at all, and the 30ms poll is sometimes late -- traced Back with
   the page still painted at t=1ms and already blank at t=81ms, so a tick that
   lands in between finds nothing left to copy and the screen goes dark for
   ~270ms.
   The line below is what causes that blank, so this is the one place that
   cannot be late: the previous item is still fully on screen on the statement
   before it. The external triggers stay -- they arm earlier when they do fire,
   and xfReuseArm is a no-op once a hold exists. */
try{if(window.__sfXfArm)window.__sfXfArm();}catch(e){}
page.classList.remove('sf-atv');
page.classList.remove('sf-bd-late');
page.classList.remove('sf-bd-in');
page.removeAttribute('data-sf-bdlate');
page.removeAttribute('data-sf-plotwait');
page.removeAttribute('data-sf-type');
page.removeAttribute('data-sf-badges');
page.removeAttribute('data-sf-eps');
page.removeAttribute('data-sf-epline');
page.removeAttribute('data-sf-epline-id');
var oldEps=page.querySelector('.sf-epsrow');
if(oldEps&&oldEps.parentNode)oldEps.parentNode.removeChild(oldEps);
var oldBadges=page.querySelector('.sf-badges');
if(oldBadges&&oldBadges.parentNode)oldBadges.parentNode.removeChild(oldBadges);
}
page.setAttribute('data-sf-atv',id);
/* sf-det-capfrom (2026-09-04). The reveal cap below was armed INSIDE this
   .then(), so the real deadline was 'item fetch + 700ms', not 700ms. Measured
   over four opens with the page element present at 54-68ms, .sf-atv landed at
   793/882/939/977ms -- the cap firing late, every time, because the fetch was
   eating 100-280ms of it first. Anchor it to the moment this page's hero work
   starts, so the deadline means what it says whatever the API costs. */
var heroT0=Date.now();
ac.getItem(ac.getCurrentUserId(),id).then(function(it){
if(!it||page.getAttribute('data-sf-atv')!==id)return;   /* navigated on */
/* sf-item-type: published for sfDetailFacts, which has to know whether a
   seasons row is COMING before it decides where to put the plot. Guessing from
   markup does not work -- #childrenContent is present on a movie page too, and
   keying on it made every movie wait out the fallback. */
try{page.setAttribute('data-sf-type',it.Type||'');}catch(e){}
var bd=page.querySelector('#itemBackdrop');
if(!bd)return;
/* sf-det-progressive (2026-09-04). The admin: the info page "isn't smooth or fast".
   Measured on a real open: the title, logo and buttons are ready at 283ms, but
   the page stays HIDDEN until 1771ms -- because the reveal waits on a
   maxWidth:1920 backdrop and that image is 1.78MB / 634ms warm, so the 1500ms
   cap below was firing rather than the image. Nearly a second and a half of
   holding a page that was already built.
   Same trick every premium client uses: reveal on a light copy, then upgrade.
   960px is 540KB/306ms -- under a third of the bytes -- and it is a darkened
   full-bleed backdrop behind text, so the gap is invisible for the ~300ms before
   the full one swaps in. */
function mkUrl(w){
try{
if((it.BackdropImageTags||[]).length)
return ac.getImageUrl(id,{type:'Backdrop',index:0,maxWidth:w,tag:it.BackdropImageTags[0]});
/* an EPISODE carries no backdrop of its own -- use the series' */
if((it.ParentBackdropImageTags||[]).length&&it.ParentBackdropItemId)
return ac.getImageUrl(it.ParentBackdropItemId,{type:'Backdrop',index:0,maxWidth:w,
tag:it.ParentBackdropImageTags[0]});
return ac.getImageUrl(id,{type:'Primary',maxWidth:w});
}catch(e){return '';}
}
var url=mkUrl(1920), lowUrl=mkUrl(960);
/* Write the episode line HERE, from the item already in hand, rather than
   leaving it to sfEpisodeLine's own fetch -- otherwise the stock
   "Season 1 - 2. Title" is on screen at reveal and visibly rewrites itself. */
if(it.Type==='Episode'&&it.ParentIndexNumber!=null&&it.IndexNumber!=null){
var line='S'+it.ParentIndexNumber+' E'+it.IndexNumber+' · '+(it.Name||'');
page.setAttribute('data-sf-epline',line);
var nm=page.querySelector('.itemName');
if(nm&&nm.textContent.trim()!==line)nm.textContent=line;
}
var shown=false, curUrl='';
function reveal(){
if(shown||page.getAttribute('data-sf-atv')!==id)return;
shown=true;
if(curUrl)bd.style.backgroundImage='url("'+curUrl+'")';
/* sf-haslogo-presettle (2026-09-04): this class changes the ribbon's height, and
   it was being applied by the NEXT tick -- i.e. up to 400ms AFTER the page was
   already on screen, which moved the whole page up 153px in one jump (measured
   btns 642 -> 489, plot 684 -> 531). The logo has been decoded by this point, so
   settle it here and reveal the final geometry rather than correcting it. */
try{
var lg0=page.querySelector('.detailLogo');
var has0=!!(lg0&&getComputedStyle(lg0).backgroundImage!=='none');
page.classList.toggle('sf-haslogo',has0);
}catch(e){}
/* sf-det-latefade (2026-09-04): revealing on the cap means the backdrop is
   not decoded yet, and #itemBackdrop carries opacity:1 with no animation
   (sf-det-nobdfade) -- so it would appear in ONE frame on a page that has
   already settled. Mark that case so it fades in instead. Only that case:
   when the artwork won the race the page still arrives as one complete
   layout, which is the whole point of holding it. */
if(url&&!bdReady){
page.classList.add('sf-bd-late');
/* an image that never decodes must not leave the backdrop invisible.
   A STAMP read by the tick, not a setTimeout: measured one page in four
   still at .sf-bd-late with opacity 0 six seconds in, i.e. long past a
   2600ms timer, so the one-shot had been lost. A stamp cannot be lost and
   the check is idempotent. */
page.setAttribute('data-sf-bdlate',String(Date.now()));
}
/* sf-fresh-reveal: when this reveal happened. sf-xfade needs to distinguish
   'this page is composed' from 'this page is composed FOR THIS NAVIGATION' --
   returning to a cached item finds .sf-atv and a matching data-sf-atv already
   in place from the previous visit. */
try{page.setAttribute('data-sf-atv-at',String(Date.now()));}catch(e){}
page.classList.add('sf-atv');
}
/* paint + fade the backdrop that arrived after the reveal. Two rAFs so the
   opacity:0 start state is committed before .sf-bd-in flips it. */
function bdLanded(){
try{
if(!shown)return;                 /* normal path: reveal() paints it itself */
if(page.getAttribute('data-sf-atv')!==id)return;
if(curUrl)bd.style.backgroundImage='url("'+curUrl+'")';
requestAnimationFrame(function(){requestAnimationFrame(function(){
try{if(page.getAttribute('data-sf-atv')===id)page.classList.add('sf-bd-in');}catch(e){}});});
}catch(e){}
}
if(url){
/* Decode off-screen first, so the hero fades in WITH its artwork instead of
   fading in empty and filling a moment later -- but on the LIGHT copy, so that
   wait is ~300ms rather than ~1.5s. */
curUrl=lowUrl||url;
/* sf-det-decoded (2026-09-04). The admin: "half the icon loads in ... a section of
   the screen is black". Both, and for the same reason: `onload` only means the
   BYTES arrived, not that the image is decoded and paintable. Revealing on it
   put the page on screen a frame or two before the browser had anything to draw,
   so the first frames were a near-black backdrop with a half-rendered logo that
   then brightened over ~500ms. Captured at +277ms.
   Wait for decode(), not load -- and wait for the LOGO too, since it is the piece
   that visibly half-draws. The stated goal for this page has always been "I only
   want to see the complete new layout"; this is what makes the first frame
   complete. Every path sets its flag exactly once, and the cap below fires
   regardless, so a slow or broken image can never hold the page. */
var bdReady=false,lgReady=false,capHit=false;
function tryReveal(){ if((bdReady&&lgReady)||capHit)reveal(); }
function afterDecode(img,done){
try{ var d=img.decode?img.decode():null;
if(d&&d.then){d.then(done,done);return;} }catch(e){}
done();
}
var pre=new Image();
pre.decoding='async';
pre.onload=function(){afterDecode(pre,function(){bdReady=true;bdLanded();tryReveal();});};
pre.onerror=function(){bdReady=true;bdLanded();tryReveal();};
/* the logo is a background-image on .detailLogo and is already set by this point
   (measured present at 79ms, well before reveal) */
(function(){
try{
var lg=page.querySelector('.detailLogo');
var bi=lg?getComputedStyle(lg).backgroundImage:'';
var lm=/url\(["']?(.*?)["']?\)/.exec(bi||'');
if(!lm||!lm[1]){lgReady=true;return;}
var li=new Image();
li.decoding='async';
li.onload=function(){afterDecode(li,function(){lgReady=true;tryReveal();});};
li.onerror=function(){lgReady=true;tryReveal();};
li.src=lm[1];
}catch(e){lgReady=true;}
})();
/* The cap is a genuine failsafe rather than the normal path: at 1500ms it WAS
   the normal path, and firing it is what the user experienced as slow. */
/* sf-det-capfrom: 520ms from heroT0 (see above), not 700ms from here. Past
   that point the page is better ON SCREEN with its title, buttons and plot
   correct and the artwork arriving behind it than absent altogether -- and
   sf-det-latefade means the artwork fades rather than pops when it does. */
/* sf-det-kick: 260ms, not 520. With the fetch now starting immediately the page is
   composed far sooner, and waiting a further half second on a backdrop is the
   remaining reason the old screen is still up. sf-det-latefade already fades the
   artwork in when it loses the race, so the cost of revealing early is a picture
   that arrives softly rather than a page that arrives late. */
/* sf-det-cap-final (2026-09-05). 100ms. Everything before this point is Jellyfin's
   own page build, and it is not ours to reclaim: a 25ms interval started at the
   click does not fire until 597ms, so no hook of ours -- hashchange, pushState,
   the CREATE observer, the 30ms strip -- can run during it. Four were tried and
   none moved the number, which is the proof.
   What IS ours is the wait after the item arrives, and holding the previous screen
   through it is what makes the transition read as Home re-rendering rather than
   going into the title. sf-det-latefade already brings the artwork in softly when
   it loses the race, so spend as little as possible here. */
setTimeout(function(){capHit=true;tryReveal();},Math.max(40,100-(Date.now()-heroT0)));
pre.src=curUrl;
/* Swap the full-resolution copy in once it has decoded. Same element, same
   position, so there is nothing to see except it getting sharper -- and if the
   user has already navigated on, the id guard drops it. */
if(lowUrl&&url&&url!==lowUrl){
var hi=new Image();
hi.decoding='async';
hi.onload=function(){try{
if(page.getAttribute('data-sf-atv')!==id)return;
/* The two images race, and the full one sometimes wins. Applying it directly
   here let the light copy's own reveal() overwrite it a moment later -- measured
   the backdrop stuck at maxWidth=960 for the life of the page. Promote it to
   `curUrl` so whichever finishes first, the page ends up with the BEST image
   available, and only paint from here once the reveal has already happened. */
curUrl=url;
if(shown)bd.style.backgroundImage='url("'+url+'")';
/* sf-det-latefade: this copy can arrive first (or the light one can fail),
   and it is then the only thing that can lift .sf-bd-late. Without this the
   backdrop sat at opacity 0 until the 2.6s failsafe with the image already
   decoded and painted. */
bdLanded();
}catch(e){}};
hi.src=url;
}
}else{
reveal();
}
}).catch(function(){page.classList.add('sf-atv');});
}
/* sf-sub-lift-measured (2026-08-28). Publishes --sf-sub-lift: the exact
   distance the subtitles must rise to clear the transport controls.

   Measured, not guessed, because the control bar does not scale with the
   viewport the way vh does. Anchor is the SEEK BAR, never .videoOsdBottom
   itself: that element carries `padding-top:7.5em` of pure gradient, so its box
   top sits ~100px above anything you can actually see, and lifting by its height
   is most of the old overshoot.

   Reads the subtitle container's own bottom edge rather than assuming 97.5vh, and
   the container is never the element we transform (the two inners are), so
   measuring it cannot feed back into its own input. */
function sfSubLift(){
var root=document.documentElement,i;
var boxes=document.querySelectorAll('.videoSubtitles'),box=null;
for(i=0;i<boxes.length;i++){if(boxes[i].getBoundingClientRect().height){box=boxes[i];break;}}
var osds=document.querySelectorAll('.videoOsdBottom'),osd=null;
for(i=0;i<osds.length;i++){if(osds[i].getBoundingClientRect().height){osd=osds[i];break;}}
if(!box||!osd){
if(root.style.getPropertyValue('--sf-sub-lift'))root.style.removeProperty('--sf-sub-lift');
return;
}
var ctrl=osd.querySelector('.sliderContainer')||osd;
var cr=ctrl.getBoundingClientRect(),br=box.getBoundingClientRect();
/* the OSD wears `hide` (display:none) while idle, so its rect reads 0 -- hold the
   last good value instead of computing a bogus one */
if(!cr.height||!br.height)return;
var GAP=Math.round(window.innerHeight*0.02);
var want=Math.round(br.bottom-(cr.top-GAP));
if(want<0)want=0;
var cap=Math.round(window.innerHeight*0.25);
if(want>cap)want=cap;
var cur=parseInt(root.style.getPropertyValue('--sf-sub-lift'),10);
if(cur!==want)root.style.setProperty('--sf-sub-lift',want+'px');
}
/* sf-holdrows: hold the home rows invisible until the TOP ones are in place, then
   reveal them all at once. See the style block for why this beats reserving space.
   Released on whichever comes first: Continue Watching AND Next Up both laid out,
   or HOLD_MS. The cap matters -- a user with nothing in progress has no Continue
   Watching at all, and must not be held staring at a skeleton. */
var HOLD_MS=4500;
function sfHoldRows(){
try{
if((location.hash||'').indexOf('#/home')!==0)return;
var pages=document.querySelectorAll('#indexPage'),page=null,i;
for(i=0;i<pages.length;i++){if(pages[i].offsetParent){page=pages[i];break;}}
if(!page)return;
var host=page.querySelector('.homeSectionsContainer')||page.querySelector('.sections');
if(!host)return;
if(host.__sfHoldDone)return;
if(!host.__sfHoldT0){
host.__sfHoldT0=Date.now();
host.classList.add('sf-hold');
/* sf-hold-deadman (2026-09-04). The release below sits inside this function's
   try/catch on a polled tick, and the CSS failsafe only restores OPACITY --
   nothing undoes visibility:hidden. A deterministic throw above the release
   would therefore leave every home row permanently invisible. That was already
   true, but the entrance now waits on this hold, so make the release
   unconditional: one timer, armed with the hold itself. */
try{setTimeout(function(){try{if(!host.__sfHoldDone){host.classList.remove('sf-hold');host.__sfHoldDone=1;}}catch(e){}},HOLD_MS+600);}catch(e){}
}
var laid=function(sel){var e=host.querySelector('.verticalSection.'+sel);
return !!(e&&e.getBoundingClientRect().height>2);};
/* sf-holdstable: "both rows exist" is not the same as "the layout has stopped
   moving". With the fit applied at first-laid-out, 5 of 6 cold loads landed
   exactly on the fold and one still drifted 22px afterwards -- the hero is still
   settling at that moment. So also require the first row's bottom to be UNCHANGED
   since the previous tick before releasing. Costs at most one extra tick of
   skeleton; HOLD_MS still caps the whole thing. */
var cwNow=host.querySelector('.verticalSection.ContinueWatching');
var bNow=cwNow?Math.round(cwNow.getBoundingClientRect().bottom):-1;
var wasStable=(host.__sfPrevBottom===bNow&&bNow>0);
host.__sfPrevBottom=bNow;
if((laid('ContinueWatching')&&laid('NextUp')&&wasStable)||(Date.now()-host.__sfHoldT0)>HOLD_MS){
/* sf-foldfit: land Continue Watching exactly ON the fold, every time.
   The admin: "sometimes the continue watching row spawns in higher than normal, then
   I see a little of the next up row. It should always load in as THE row and we
   only see more when we scroll."
   Measured across four cold loads, the sections container settles at either
   y=590 (row bottom == 900 == viewport, nothing else showing) or y=505 (row
   bottom 815, leaving 85px of Next Up peeking). It is a race, not a constant
   offset: 590 happens while the hero SKELETON (.sf-skel-hero, 493px) is still the
   previous sibling, 505 once it has been removed and the real 810px hero is
   carrying the space. scrollY is 0 and margin-top is 0px in every case, so it is
   neither a restored scroll nor a stray margin.
   Rather than try to win that race, correct the result: nudge the container so
   the first row's bottom meets the viewport bottom. This happens while the rows
   are still HELD invisible, so the adjustment is never seen -- it is the whole
   reason the hold exists.
   Clamped to +/-200px: this is a race correction, not a licence to redesign the
   fold on an unusual viewport. */
try{
var cwEl=host.querySelector('.verticalSection.ContinueWatching');
var rr=cwEl&&cwEl.getBoundingClientRect();
if(rr&&rr.height>2){
/* sf-foldfit-removed (2026-08-28). This used to nudge the container's
   margin-top so the first row's bottom met the viewport bottom. It was a ONE-SHOT
   correction computed at reveal, and it never recomputed on resize -- so the
   moment the window changed size the offset was stale and yanked every row up
   over the hero. Caught live in Brave: margin-top -186px computed at a 596px-tall
   viewport, still applied at 733px tall, burying the hero logo behind Continue
   Watching. Actively hostile to anyone resizing a window, which is exactly how
   the admin uses it. The 22px it was chasing is not worth that. Clear anything a
   previous build left behind. */
host.style.removeProperty('margin-top');
}
/* Drop the skeleton HERE rather than letting it fall back into flow at
   order:9999 -- it is absolutely positioned during the hold, and releasing
   without removing it made it travel y=505 -> y=4096. Off-screen, so invisible,
   but the browser still counts that as layout shift. */
var sk=host.querySelector('.sf-skel');
if(sk&&sk.parentNode)sk.parentNode.removeChild(sk);
}catch(e){}
host.classList.remove('sf-hold');
host.__sfHoldDone=1;
}
}catch(e){}
}
/* sf-nav-swap: blank the shared tab strip for one navigation, so the mixed
   old+new tab set is never on screen. 320ms covers the measured 92-185ms window
   with margin; the class is always removed by a timer, so a navigation that never
   completes cannot leave the tabs hidden.
   hashchange alone is NOT enough -- Jellyfin navigates with history.pushState,
   which fires neither hashchange nor popstate, so both are wrapped. */
function sfNavSwap(){
if(window.__sfNavSwap)return;
window.__sfNavSwap=1;
var de=document.documentElement,t=null;
/* sf-navkeep: a strip is safe to leave on screen while it holds ONLY main
   pills. Every pill we own carries data-sf-nav -- on our .jf-mu-mainbar and on
   the native strip alike -- and a page's own tabs never do, so this needs no
   text matching and works in every language. Re-evaluated each frame because
   the strip mutates DURING the swap: it goes mixed, then clean. */
/* sf-nav-pinrow (2026-08-29). Live TV -> Home: the pill row dips 9px and then
   snaps back up ~450ms later. Measured cause, from the header's own children:
     t=0    .headerTabs h=67 (our .jf-mu-mainbar 49 + 10 margin), pill row top 29
     t=180  our bar removed -> .headerTabs h=57, but its margin-top is a FIXED
            -80.2032px, so the flex wrapper grew 101 -> 110 and the row fell to 38
     t=640  header finally re-sizes 87 -> 77 and the row returns to 29
   Nothing is wrong with the end state; the header is simply still sized for the
   page we left while its contents already belong to the page we are entering.
   The admin asked for this row to stay put, so hold it: measure where it sits before
   the teardown and keep it there with an inline margin-top on .headerTabs (the
   property that already positions it), releasing once the header height has been
   stable for 200ms -- by then the natural position matches and the release is
   invisible. Hard-capped so it can never stay pinned. */
var _pinEl=null,_pinBase=0,_pinTarget=0,_pinH=-1,_pinAt=0,_pinCap=0;
function mainStrip(){
var sl=document.querySelectorAll('.emby-tabs-slider'),i,j,btns,clean,any,b,found=null;
for(i=0;i<sl.length;i++){
if(!sl[i].getClientRects().length)continue;
btns=sl[i].querySelectorAll('button');clean=true;any=false;
for(j=0;j<btns.length;j++){
b=btns[j];
if(!b.getClientRects().length)continue;
any=true;
if(!b.getAttribute('data-sf-nav')){clean=false;break;}
}
if(any&&clean)found=sl[i];
}
return found;
}
function pinStart(){
try{
if(_pinEl)return;
var st=mainStrip();if(!st)return;
var ht=st.closest?st.closest('.headerTabs'):null;if(!ht)return;
_pinTarget=Math.round(st.getBoundingClientRect().top);
_pinBase=parseFloat(getComputedStyle(ht).marginTop)||0;
_pinEl=ht;_pinH=-1;_pinAt=Date.now();_pinCap=Date.now()+2500;
}catch(e){}
}
function pinEnd(){
try{if(_pinEl)_pinEl.style.marginTop='';}catch(e){}
_pinEl=null;
}
function pinStep(){
if(!_pinEl)return;
try{
if(Date.now()>_pinCap){pinEnd();return;}
var hdr=document.querySelector('.skinHeader');
var h=hdr?Math.round(hdr.getBoundingClientRect().height):0;
if(h!==_pinH){_pinH=h;_pinAt=Date.now();}
var st=mainStrip();
if(st){
var cur=Math.round(st.getBoundingClientRect().top),d=_pinTarget-cur;
if(d){
var m=parseFloat(_pinEl.style.marginTop||'');
if(m!==m)m=_pinBase;
_pinEl.style.marginTop=(m+d)+'px';
}
}
/* the header has held one height long enough to be its real one */
if(Date.now()-_pinAt>200)pinEnd();
}catch(e){}
}
function mark(){
try{
var sl=document.querySelectorAll('.emby-tabs-slider'),i,j,btns,clean,any,b,keep=[];
for(i=0;i<sl.length;i++){
btns=sl[i].querySelectorAll('button');clean=true;any=false;
for(j=0;j<btns.length;j++){
b=btns[j];
if(!b.getClientRects().length)continue;
any=true;
if(!b.getAttribute('data-sf-nav')){clean=false;break;}
}
if(any&&clean)keep.push(sl[i]);
else if(sl[i].hasAttribute('data-sf-navkeep'))sl[i].removeAttribute('data-sf-navkeep');
}
/* sf-navkeep-one: entering Live TV the header briefly holds TWO complete
   4-pill strips (measured strips=3, btns=[4,4,3], every one at opacity 1).
   Before sf-navkeep the swap blanked both, so the duplicate was never seen;
   exempting "clean" strips made it visible -- part of the Live TV nav "flash".
   Only the newest may stay: that is the one sfMainNav keeps, and blanking the
   older copy is exactly what the swap is for. */
for(i=0;i<keep.length;i++){
if(i===keep.length-1){if(!keep[i].hasAttribute('data-sf-navkeep'))keep[i].setAttribute('data-sf-navkeep','1');}
else if(keep[i].hasAttribute('data-sf-navkeep'))keep[i].removeAttribute('data-sf-navkeep');
}
/* sf-navswap-sub (2026-09-04). Going Home -> Live TV the header showed the
   Programs/Guide/Channels sub-pills with NO main nav above them for the length
   of the swap -- caught in a frame capture. The blanking rule only covers
   .emby-tabs-slider, and .jf-ltv-sub is not one, so it stayed lit on its own:
   exactly the half-built header sf-hdr-parts exists to prevent.
   Stamp it with the same keep decision the strip gets, so the two are blanked
   and revealed together. Done as an attribute here rather than as an
   `html.sf-nav-swap:not(:has(...))` rule on purpose -- a :has() anchored on the
   root re-evaluates against a page that builds hundreds of nodes during load.
   Keeping it tied to `keep` also means navigating WITHIN Live TV (Programs <->
   Guide <-> Channels), where the main strip stays clean and kept, never blinks
   the sub bar the user just clicked. */
/* sf-navsub-painted (2026-09-04): `keep.length` was the wrong test. During the
   swap a strip can be kept but not yet PAINTED, and the sub bar was then shown
   beside a main strip that was still blanked -- the half-built header again,
   caught entering Live TV. Follow the kept strip's actual on-screen state. */
var _kept=keep.length?keep[keep.length-1]:null;
var _keptOn=!!(_kept&&_kept.getClientRects().length);
var subs=document.querySelectorAll('.jf-ltv-sub'),k;
for(k=0;k<subs.length;k++){
if(_keptOn){if(!subs[k].hasAttribute('data-sf-navkeep'))subs[k].setAttribute('data-sf-navkeep','1');}
else if(subs[k].hasAttribute('data-sf-navkeep'))subs[k].removeAttribute('data-sf-navkeep');
}
}catch(e){}
}
function hide(){
try{
pinStart();
mark();
de.classList.add('sf-nav-swap');
if(t)clearTimeout(t);
/* keep the marker live for the whole window, otherwise a strip that is mixed
   at t=0 stays blanked after it settles (and one that is clean at t=0 stays
   visible after it goes mixed) */
(function loop(){
if(!de.classList.contains('sf-nav-swap')&&!_pinEl)return;
mark();pinStep();requestAnimationFrame(loop);
})();
t=setTimeout(function(){de.classList.remove('sf-nav-swap');mark();},320);
}catch(e){}
}
try{window.addEventListener('hashchange',hide);}catch(e){}
try{window.addEventListener('popstate',hide);}catch(e){}
try{
['pushState','replaceState'].forEach(function(k){
var orig=history[k];
if(!orig||orig.__sfWrapped)return;
var w=function(){var r=orig.apply(this,arguments);hide();return r;};
w.__sfWrapped=1;
history[k]=w;
});
}catch(e){}
}
/* sf-arrow-dim (2026-08-27). Jellyfin's native rows disable the arrow that
   cannot move and its stylesheet fades a :disabled scroll button to .3, so
   setting the property is all the dimming needs. Ours left BOTH arrows fully
   lit at position 0, so the left arrow on Watchlist / Live TV / Audiobooks /
   Music invited a click that could never do anything.
   Re-run on every tick, not once at build time: a row is created before its
   cards land, and at that moment scrollWidth==clientWidth would latch "next"
   disabled permanently. */
function sfArrowSync(r,box){
var b=box.getElementsByTagName('button');
if(b.length<2)return;
var max=r.scrollWidth-r.clientWidth;
var atStart=r.scrollLeft<=1,atEnd=max<=0||r.scrollLeft>=max-1;
if(b[0].disabled!==atStart)b[0].disabled=atStart;
if(b[1].disabled!==atEnd)b[1].disabled=atEnd;
}
function sfRowArrows(){
/* sf-leavingrow added 2026-09-04: it builds the same .sf-ml-row container as
   the watchlist, so it needed nothing but a place in this list -- it had
   simply never been added, which is why it was the one row you could not
   scroll with the chevrons. */
var sel=['.sf-mylistrow','.sf-leavingrow','.sf-livetvrow','.sf-musicrow','.sf-audiobookrow','.sf-epsrow'],i,j,list,sec,row,head,box,btns,ex;
for(i=0;i<sel.length;i++){
/* querySelectorAll, not querySelector: Jellyfin caches one view per URL, so a
   stale copy of a section can sit ahead of the visible one and swallow the
   build, leaving the row actually on screen with no arrows at all. */
list=document.querySelectorAll(sel[i]);
for(j=0;j<list.length;j++){
sec=list[j];
row=sec.querySelector('.sf-ml-row');
if(!row)continue;
ex=sec.querySelector('.emby-scrollbuttons');
if(ex){sfArrowSync(row,ex);continue;}   /* already built -- just refresh state */
head=sec.querySelector('.sectionTitleContainer');
if(!head)continue;
box=document.createElement('div');
box.className='emby-scrollbuttons padded-right sf-row-arrows';
box.innerHTML='<button type="button" class="emby-scrollbuttons-button paper-icon-button-light" title="Previous"><span class="material-icons chevron_left" aria-hidden="true"></span></button>'
+'<button type="button" class="emby-scrollbuttons-button paper-icon-button-light" title="Next"><span class="material-icons chevron_right" aria-hidden="true"></span></button>';
btns=box.getElementsByTagName('button');
(function(r,prev,next,bx){
function step(d){
r.scrollBy({left:d*Math.max(200,Math.round(r.clientWidth*0.85)),behavior:'smooth'});
}
/* stopPropagation so the click cannot reach the row heading's own link */
prev.addEventListener('click',function(e){e.preventDefault();e.stopPropagation();step(-1);});
next.addEventListener('click',function(e){e.preventDefault();e.stopPropagation();step(1);});
/* on scroll as well as on tick, so the dimming lands with the swipe rather
   than up to a tick later */
r.addEventListener('scroll',function(){sfArrowSync(r,bx);});
})(row,btns[0],btns[1],box);
head.parentNode.insertBefore(box,head.nextSibling);
sfArrowSync(row,box);
}
}
}
'''

# _LS_14 (orig L9422-10142) -- sf-abrow-head, sf-hero-play, sf-drawer-scroll
_LS_14 = r'''/* sf-abrow-head (2026-08-21). The "Audiobooks" row heading pointed at
   `#/list?type=AudioBook`, which is NOT a route Jellyfin can resolve -- a list
   page is addressed by parentId, not by type. An unresolvable hash lands you on
   home, at the top, which is precisely what the admin reported three times:
   "when I click that it takes me to the top of the home page".

   It now goes to the real Audio Books library -- the page with the Continue
   listening / series / Recently added shelves. The id is looked up from the
   user's own views rather than hardcoded, so it survives the library being
   recreated, with the known id as a fallback. */
var sfAbViewId=null;
function sfAbViewHash(){
var ac=window.ApiClient,srv='';
try{srv=ac?ac.serverId():'';}catch(e){}
var id=sfAbViewId||(window.SF_CONFIG&&window.SF_CONFIG.audiobookLibraryId)||'';
return '#/list?parentId='+id+(srv?('&serverId='+srv):'');
}
function sfAbViewResolve(){
if(sfAbViewId||window.__sfAbViewBusy)return;
var ac=window.ApiClient;
if(!ac||!ac.getJSON||!ac.getCurrentUserId)return;
var _uid=null;try{_uid=ac.getCurrentUserId();}catch(e){}
if(!_uid)return;
if((window.__sfAbViewFails|0)>=3)return;
window.__sfAbViewBusy=1;
ac.getJSON(ac.getUrl('UserViews',{userId:ac.getCurrentUserId()}))
.then(function(r){
var v=(r&&r.Items)||[],i;
for(i=0;i<v.length;i++){
if((v[i].CollectionType||'')==='books'){sfAbViewId=v[i].Id;break;}
}
window.__sfAbViewBusy=0;
}).catch(function(){window.__sfAbViewFails=(window.__sfAbViewFails|0)+1;window.__sfAbViewBusy=0;});
}
function sfRowTitles(){
sfAbViewResolve();
var map=[['.sf-mylistrow','#/home?tab=1&sub=wl'],
['.sf-livetvrow','#/livetv'],
['.sf-musicrow','#/music?tab=1'],
['.sf-audiobookrow',sfAbViewHash()],
['.sf-mus-artists','#/music?tab=1'],
['.sf-mus-playlists','#/music?tab=1']];
var i,sec,t;
for(i=0;i<map.length;i++){
sec=document.querySelector(map[i][0]);
if(!sec)continue;
t=sec.querySelector('.sectionTitle');
if(!t)continue;
/* rewrite when the target changes -- the audiobook id resolves asynchronously,
   and a link stamped once would keep the fallback forever */
if(t.getAttribute('data-sf-link')===map[i][1])continue;
t.setAttribute('data-sf-link',map[i][1]);
if(t.getAttribute('data-sf-linked')==='1'){continue;}
t.setAttribute('data-sf-linked','1');
t.classList.add('sf-title-link');
t.addEventListener('click',function(){
location.hash=this.getAttribute('data-sf-link');});
}
}
/* sf-hero-play: make the hero's Play button actually play.

   It never has. Media Bar's own handler (slideshowpure.js:1417) does:

       POST /Sessions/{sessionId}/Playing?playCommand=PlayNow&itemIds=...

   which is a REMOTE-CONTROL command addressed to the browser's OWN session --
   and jellyfin-web ignores those. The request returns 204, the plugin logs
   "Play command sent successfully", and nothing happens. Reproduced on desktop
   and phone: click lands, stopPropagation fires from the plugin, no media
   element is ever created and the route does not change.

   So the click is taken in the CAPTURE phase (which runs before the plugin's own
   onclick) and routed through sfPlayItemViaProxy -- the same card-proxy path every
   other row here uses, and the only mechanism that reliably starts playback.

   The id preferred is data-sf-cw, the resumable episode sf-hero-resume put on the
   slide, so "Continue S2 E8" continues that episode rather than restarting the
   series. */
/* sf-drawer-scroll: keep the side menu open while it is being scrolled.

   The drawer carries Jellyfin's own gesture library (class "touch-menu-la"),
   which watches touch drags to open/close it. Its content is taller than the
   screen on a phone (measured 1385px of menu in an 869px viewport), so the menu
   MUST be scrolled -- and a vertical drag inside it gets read as a close gesture,
   which is the "I scroll the hamburger menu and it keeps closing" report.

   The scroll container is not an emby-scroller, so jf-touch-scroll never touched
   it; this is the library's own behaviour. A predominantly VERTICAL drag that
   starts inside the scroller is stopped from reaching the gesture handler, while
   horizontal drags still close the drawer as they should. The scroller's own
   native scrolling is untouched -- propagation is stopped, not the default. */
function sfDrawerScroll(){
var sc=document.querySelector('.mainDrawer-scrollContainer');
if(!sc||sc.getAttribute('data-sf-dscroll')==='1')return;
sc.setAttribute('data-sf-dscroll','1');
var x0=0,y0=0,lock=null,moved=0,movedAt=0;
sc.addEventListener('touchstart',function(e){
var t=e.touches&&e.touches[0];
if(!t)return;
x0=t.clientX;y0=t.clientY;lock=null;moved=0;
/* A NEW touch is a NEW intention. Clearing the guard here is what makes this
   per-gesture instead of per-timer: the click that ends a scroll arrives with
   no touchstart of its own, so it is still swallowed, while a deliberate tap
   after a scroll always begins with this event and is therefore always let
   through -- even if it comes 50ms later. */
movedAt=0;
},{passive:true});
sc.addEventListener('touchmove',function(e){
var t=e.touches&&e.touches[0];
if(!t)return;
var dx=Math.abs(t.clientX-x0),dy=Math.abs(t.clientY-y0);
if(dx>moved)moved=dx;
if(dy>moved)moved=dy;
if(lock===null){
if(dx<4&&dy<4)return;                 /* not enough movement to judge yet */
lock=(dy>dx)?'v':'h';
}
/* vertical means "scroll the menu", never "close the menu" */
if(lock==='v')e.stopPropagation();
},{passive:true});
sc.addEventListener('touchend',function(){
/* sf-drawer-tapguard (2026-08-21). The admin: "when I try to scroll the hamburger
   menu it just exits when I'm done scrolling and not when I press what I want
   to press."
   Stopping touchmove was only half of it. A scroll still ends with a synthesised
   CLICK wherever the finger came to rest -- so lifting off after a scroll acted
   as a press: on nothing, which dismissed the drawer, or worse on whatever row
   happened to be under the finger. A gesture that MOVED is not a press, so the
   click that follows it is swallowed. Movement is the test, not time, so a slow
   deliberate tap still works.

   2026-08-23: the window was 700ms and was measured swallowing REAL taps. After
   a CDP touch scroll, tapping "Dashboard" did nothing at 0ms and merely closed
   the drawer at 300ms; only past ~500ms did it navigate -- which is exactly the
   original complaint, re-created by the fix for it. Nobody waits 700ms after
   scrolling before pressing. The window is now 350ms AND, more importantly,
   touchstart clears movedAt, so the guard only ever applies to the click that
   belongs to the same gesture. */
if(moved>10)movedAt=Date.now();
lock=null;moved=0;
},{passive:true});
sc.addEventListener('click',function(e){
if(movedAt&&Date.now()-movedAt<350){
e.preventDefault();
e.stopPropagation();
e.stopImmediatePropagation();
movedAt=0;
}
},true);
}
function sfHeroPlayFix(){
if(window.__sfHeroPlayWired)return;
window.__sfHeroPlayWired=1;
document.addEventListener('click',function(e){
var b=(e.target&&e.target.closest)?e.target.closest('.btnPlay.play-button'):null;
if(!b)return;
var slide=b.closest('.slide');
if(!slide)return;
var id=slide.getAttribute('data-sf-cw')||slide.getAttribute('data-item-id');
if(!id)return;
/* stop the plugin's broken handler from running at all */
e.preventDefault();
e.stopImmediatePropagation();
var ac=window.ApiClient;
if(!ac||!ac.getItem){location.hash='#/details?id='+id;return;}
/* sf-hero-resume-pos (2026-08-23). Pressing Play on a Continue Watching hero
   started the item from 00:00. Two faults, both here:
     1. the SERIES id was handed to playback, not the episode being resumed;
     2. no position was passed at all.
   Jellyfin's itemShortcuts reads data-positionticks off the element it acts on
   and calls play({startPositionTicks: that || 0}) -- for BOTH 'play' and
   'resume', so the action name is decoration and the attribute is the whole
   story. Measured before the fix on a hero labelled "Continue S1 E2" with the
   episode stored at 900s: proxy data-positionticks=null, data-type=Series, and
   the video element sat at currentTime 8.7s.
   sfCwMap already knows which episode a series slide stands for (epId), so the
   target costs no extra round trip; the getItem that was being made anyway is
   simply pointed at that episode, which is where the authoritative, current
   position comes from. */
var cw=sfCwMap[sfNorm(id)];
var playId=(cw&&cw.epId)?cw.epId:id;
ac.getItem(ac.getCurrentUserId(),playId).then(function(it){
if(!it){location.hash='#/details?id='+id;return;}
var ud=it.UserData||{};
/* The item's own stored position wins; sfCwMap.pt is the fallback for a reply
   that carries no UserData. >=96% is "basically finished" -- the same cut-off
   the hero LABEL uses to decide it is not resumable -- so a nearly-complete
   item starts over rather than resuming 30 seconds from the credits. */
var pt=ud.PlaybackPositionTicks||0;
if(!pt&&cw&&cw.pt)pt=cw.pt;
if(pt>0&&(ud.PlayedPercentage||0)>=96)pt=0;
var act=pt>0?'resume':'play';
/* The proxy needs a Jellyfin-bound .itemsContainer to exist. On a cold hero
   click the home rows may still be rendering, so give it one retry before
   falling back to the detail page rather than doing nothing. */
if(!sfPlayItemViaProxy(it.Id,it.Type||'Movie',it.MediaType||'Video',!!it.IsFolder,act,pt||'')){
setTimeout(function(){
if(!sfPlayItemViaProxy(it.Id,it.Type||'Movie',it.MediaType||'Video',!!it.IsFolder,act,pt||''))
location.hash='#/details?id='+it.Id;
},700);
}
}).catch(function(){location.hash='#/details?id='+id;});
},true);
}
function sfHeroWatch(){
if(sfHeroObs)return;
var s=document.querySelector('.slide');
if(!s||!s.parentNode)return;
sfHeroObs=new MutationObserver(function(){
/* first, before anything measures or paints: cap the artwork request. On the
   400ms tick alone this landed after the full-size original had already been
   downloaded and decoded. */
try{sfHeroImg();}catch(e){}
try{sfHeroPrefill();}catch(e){}
try{sfHeroResume();}catch(e){}
/* the hero layout lives in its own script block, so it is reached through the
   handle it publishes; ordering matters -- it sets the rows this then measures */
try{if(window.__jfHeroLayout)window.__jfHeroLayout();}catch(e){}
try{sfCwBarPos();}catch(e){}
});
sfHeroObs.observe(s.parentNode,{attributes:true,attributeFilter:['class'],subtree:true});
}
/* The label is a bare text node beside the icon, so it is set directly rather
   than via CSS content -- a ::after swap would leave the real label for screen
   readers saying "Play" while the button resumes. */
/* Season 0 is Jellyfin's specials bucket: "S0 E7" is accurate and meaningless to
   a viewer. One helper so the episode line and the button always agree. */
function sfEpName(x){
return (x.s===0)?('Special '+x.e):('S'+x.s+' E'+x.e);
}
function sfHeroLabel(slide,text){
var b=slide.querySelector('.btnPlay.play-button');
if(!b)return;
/* Media Bar wraps the label: <button><span class="play-text">Play</span></button>.
   Verified on the live markup -- a direct text-node walk finds only whitespace,
   which is why the first version silently left the button saying "Play". */
/* Translate at the CHOKE POINT, not at each caller. Every hero label reaches
   .play-text through here, so doing it once means no path can write an English
   string -- one caller was still emitting "Continue S6 E15" untranslated
   (measured 1 English frame in 5043 on German). The sweep would fix it a repaint
   later; this means the English form never exists. */
try{if(window.sfTr)text=window.sfTr(text);}catch(e){}
var sp=b.querySelector('.play-text');
if(sp){
if(sp.textContent.trim()!==text)sp.textContent=text;
b.setAttribute('title',text);
return;
}
var i,n,done=false;
for(i=0;i<b.childNodes.length;i++){
n=b.childNodes[i];
if(n.nodeType===3&&n.nodeValue&&n.nodeValue.trim()){
if(n.nodeValue.trim()!==text)n.nodeValue=n.nodeValue.replace(/\S.*\S|\S/,text);
done=true;break;
}
}
if(!done)b.setAttribute('title',text);
}
/* sf-page-bg: below the hero the page was flat rgb(16,16,16). Carry the hero's
   own artwork down the page instead, blurred and scrimmed.
   Painted from body::before rather than a new stacking element: a fixed div
   would have to out-stack Jellyfin's own positioned content and risks covering
   it, whereas ::before at z-index -1 sits above the html canvas colour and below
   every child of body, which is exactly the layer we want.
   The URL is published as a custom property so all the styling stays in CSS.
   Home only -- it follows Media Bar's slide, and there is no such artwork
   anywhere else. */
function sfPageBg(){
var h=location.hash||'';
var onHome=h.indexOf('#/home')===0;
var onDetail=h.indexOf('#/details')===0;
/* sf-mus-pagebg (2026-08-27, the admin: "have the background carry the ambient
   colour like we have at home"). Music used to get a single flat wash --
   html.sf-mus-amb #musicRecommendedPage::before, one accent colour over the top
   52vh and hard black below it. This is the real thing instead: the same
   blurred-artwork layer home has had since sf-page-bg, sourced from the
   featured album's cover, so the colour is the RECORD's rather than one
   averaged swatch of it, and it carries the full height of the page. */
var onMusic=h.indexOf('#/music')===0;
var b=document.body;
/* sf-flat-pagebg: #/home covers My Stuff, Sports and Live TV too, and none of
   those paint the hero the wash is designed to sit beside. Toggle here, ABOVE
   the early returns below -- the artwork itself does not change when you switch
   between these surfaces, so anything placed after `data-sf-bg === src` would
   never run on exactly the navigations that need it. */
b.classList.toggle('sf-flat-pagebg',!!(onHome&&/[?&](sports=1|livetv=1|tab=[1-9])/.test(h)));
if(!onHome&&!onDetail&&!onMusic){
if(b.getAttribute('data-sf-bg')){b.style.removeProperty('--sf-pagebg');b.removeAttribute('data-sf-bg');b.classList.remove('sf-has-pagebg');b.classList.remove('sf-mus-pagebg');b.classList.remove('sf-flat-pagebg');}
return;
}
/* Follows the hero slide by slide again. Locking this was my attempt at the red
   flash and it was the wrong culprit: the flash came from the hero stack being
   TRANSPARENT mid-crossfade, letting this layer show through (see
   sf-hero-opaque). With an opaque surface behind the slides it can change
   freely without ever being seen to. */
var src='';
if(onHome){
/* img.backdrop specifically, NOT the first image in the slide. A slide's DOM
   order is logo-container then backdrop-container, so the bare 'img' selector
   was picking up the LOGO -- verified live, the wash was being generated from
   the logo on both test devices. A logo is mostly transparent with a couple of
   brand colours, so blurring it produced a colour cast with no relationship to
   the still behind it (a red wash on Kim's Convenience, for instance). The wash
   is meant to be an out-of-focus continuation of the hero, the way Apple Music
   bleeds album art, so it has to come from the backdrop. */
var img=document.querySelector('.slide.active img.backdrop')||
document.querySelector('.slide img.backdrop')||
document.querySelector('.slide.active img')||document.querySelector('.slide img');
src=img?(img.currentSrc||img.getAttribute('src')||''):'';
}else if(onMusic){
/* Nothing to draw until the featured panel exists -- and it only exists once
   its cover has been read for the accent, so the wash and the panel arrive
   together the way sf-hero-oneshot intends. No hero (a listener with no play
   history) simply leaves the page its normal colour. */
var mhero=document.querySelector('.sf-mus-hero');
src=mhero?(mhero.getAttribute('data-sf-art')||''):'';
}else{
var pages=document.querySelectorAll('#itemDetailPage'),pg=null,i;
for(i=0;i<pages.length;i++){
if(pages[i].offsetParent!==null&&pages[i].getBoundingClientRect().height>0){pg=pages[i];break;}
}
var bd=pg?pg.querySelector('#itemBackdrop'):null;
var bg=bd?(bd.style.backgroundImage||''):'';
var m=bg.match(/url\(["']?([^"')]+)["']?\)/);
src=m?m[1]:'';
}
if(!src)return;
/* Do not paint the wash before the hero exists. The wash is a blurred copy of
   the hero still, and its own preload can finish before the hero image has
   decoded and been revealed -- which showed a big blurred smear above the first
   row with nothing above it, looking like a bug. Holding it until the hero has
   actually been revealed makes the two arrive together. Home only; the detail
   page has no equivalent reveal to wait on. */
if(onHome){
var hb=document.querySelector('#slides-container .slide.active img.backdrop')||
document.querySelector('#slides-container .slide img.backdrop');
if(!hb||!hb.classList.contains('sf-art-in'))return;
}
if(b.getAttribute('data-sf-bg')===src)return;
/* Apply only once the artwork is decoded. Setting the variable first makes the
   layer appear EMPTY for a frame and then pop when the image arrives -- the
   same one-frame gap, and the same flash. */
var pre=new Image();
pre.decoding='async';
pre.onload=function(){
b.setAttribute('data-sf-bg',src);
b.style.setProperty('--sf-pagebg','url("'+src+'")');
b.classList.add('sf-has-pagebg');
/* sf-mus-pagebg: music gets the same layer at a much lower strength. Home can
   carry opacity .62 because a full-bleed hero STILL occupies the top third and
   the wash is only ever seen beside and below it. The music page has no such
   image -- the wash IS the top of the page -- so at .62 the whole screen went
   orange and read as a coloured background rather than ambient light. */
b.classList.toggle('sf-mus-pagebg',!!onMusic);
};
pre.src=src;
}
/* sf-drawer-order: Sign Out was not the last entry -- Plugin Settings sat
   below it -- and Music was 7th of 9 in the library list, behind Folders and
   Audio Books. Both are whole-container moves, so no row-level shuffling. */
function sfDrawerOrder(){
var sc=document.querySelector('.mainDrawer-scrollContainer');
if(!sc)return;
var user=sc.querySelector('.userMenuOptions');
var plugin=sc.querySelector('.pluginMenuOptions');
/* only move while Plugin Settings still follows the user block, so this
   settles after one move instead of swapping every tick */
if(user&&plugin&&(user.compareDocumentPosition(plugin)&Node.DOCUMENT_POSITION_FOLLOWING)){
sc.appendChild(user);
}
var lib=sc.querySelector('.libraryMenuOptions');
if(lib&&lib.getAttribute('data-sf-music-first')!=='1'){
var links=lib.querySelectorAll('a.navMenuOption');
var music=null,first=null;
for(var i=0;i<links.length;i++){
if(!first)first=links[i];
var t=(links[i].textContent||'').replace(/\s+/g,' ').trim();
if(/(^|\s)Music$/.test(t))music=links[i];
}
if(music&&first&&music!==first){
lib.insertBefore(music,first);
lib.setAttribute('data-sf-music-first','1');
}
}
}
/* sf-title-dup: decide per item whether the visible logo already states the
   title. The logo's image URL names the item it belongs to -- equal to the page
   item means movie/series artwork (duplicate); different means it is the parent
   artist's logo on an album page, where the album name must still be shown. */
function sfTitleDup(){
var names=document.querySelectorAll('.itemName.parentNameLast');
if(!names.length)return;
var cur=(location.hash.match(/[?&]id=([0-9a-f]{32})/i)||[])[1];
var logo=null,logos=document.querySelectorAll('.detailLogo');
for(var i=0;i<logos.length;i++){if(logos[i].getClientRects().length){logo=logos[i];break;}}
var dup=false;
if(logo&&cur){
var bg=getComputedStyle(logo).backgroundImage||'';
/* no regex here on purpose: a slash inside a regex literal closes it, and the
   escaping needed to survive this file broke the whole script block once. */
var lowbg=bg.toLowerCase();
var k=lowbg.indexOf('/items/');
var logoId=(k>=0)?lowbg.substr(k+7,32):'';
dup=(logoId.length===32&&logoId===cur.toLowerCase());
}
for(var j=0;j<names.length;j++)names[j].classList.toggle('sf-title-dup',dup);
}
/* sf-owned-albums: Jellyfin matches albums by NAME only, so an artist-name
   search returns nothing from the library and the page fills with unavailable
   results instead. Resolve the query to an artist and list their albums first. */
var sfOwnedQ=null;
function sfSearchQuery(){
var h=location.hash||'';
var i=h.indexOf('query=');
if(i<0)return '';
var raw=h.substring(i+6);
var amp=raw.indexOf('&');
if(amp>=0)raw=raw.substring(0,amp);
try{return decodeURIComponent(raw.split('+').join(' ')).trim();}catch(e){return '';}
}
function sfOwnedAlbums(){
var fields=document.querySelectorAll('.searchFields');
var page=null;
for(var i=0;i<fields.length;i++){
if(!fields[i].getClientRects().length)continue;
var p=fields[i].parentElement;
while(p&&p.className.indexOf('page')<0)p=p.parentElement;
if(p){page=p;break;}
}
if(!page)return;
var q=sfSearchQuery();
var host=page.querySelector('.sf-lib-albums');
/* sf-no-churn: position used to be re-asserted here every tick with
   insertBefore. sf-search-order2 now places sections with flex `order`, so DOM
   position is irrelevant -- and a node move every 400ms kept waking the
   MutationObserver that drives apply(), which is how the page could lock up. */
if(!q){if(host)host.parentNode.removeChild(host);sfOwnedQ=null;return;}
if(q===sfOwnedQ)return;
sfOwnedQ=q;
if(host)host.parentNode.removeChild(host);
var ac=window.ApiClient,uid=ac.getCurrentUserId();
ac.getItems(uid,{SearchTerm:q,IncludeItemTypes:'MusicArtist',Recursive:true,Limit:1}).then(function(ar){
var art=(ar.Items||[])[0];
if(!art)return null;
return ac.getItems(uid,{AlbumArtistIds:art.Id,IncludeItemTypes:'MusicAlbum',Recursive:true,SortBy:'ProductionYear',SortOrder:'Descending',Limit:24}).then(function(al){
var items=al.Items||[];
if(!items.length)return null;
if(sfOwnedQ!==q)return null;
var box=document.createElement('div');
box.className='sf-lib-albums padded-left padded-right';
var hd=document.createElement('h2');
/* sf-lib-title-match: Jellyfin's own classes, so this heading is the same
   object as every other section title rather than a lookalike. */
hd.className='sectionTitle sectionTitle-cards';
hd.textContent=art.Name+' in your library';
box.appendChild(hd);
var row=document.createElement('div');row.className='sf-lib-row';
for(var j=0;j<items.length;j++){
var it=items[j];
var a=document.createElement('a');
a.className='sf-lib-alb';
a.setAttribute('href','#/details?id='+it.Id+'&serverId='+(it.ServerId||ac.serverId()));
var im=document.createElement('span');im.className='sf-lib-alb-img';
try{im.style.backgroundImage='url("'+ac.getImageUrl(it.Id,{type:'Primary',maxWidth:300})+'")';}catch(e){}
var t=document.createElement('span');t.className='sf-lib-alb-t';t.textContent=it.Name;
var y=document.createElement('span');y.className='sf-lib-alb-y';y.textContent=it.ProductionYear||'';
a.appendChild(im);a.appendChild(t);a.appendChild(y);row.appendChild(a);
}
box.appendChild(row);
var firstSec=page.querySelector('.verticalSection');
if(firstSec&&firstSec.parentNode)firstSec.parentNode.insertBefore(box,firstSec);
else page.appendChild(box);
return null;
});
}).catch(function(){});
}
/* sf-music-nav: the music tabs occupy .tabs-viewmenubar, the same bar the home
   page uses for the main pills -- which is why the pills disappear here. Add a
   main-pill bar above it instead of moving Jellyfin's own tab buttons, whose
   switching is bound to that slider by index. */
var SFMU=[['Home','#/home'],['Live TV','#/home?livetv=1'],['Sports','#/home?sports=1'],['My Stuff','#/home?tab=1']];
/* sf-drawer-home-route: send the drawer's Home through the SAME mechanism the
   main pill uses. Both target '#/home', but the pill assigns location.hash while
   the drawer anchor goes through Jellyfin's own link handling, which builds a
   SECOND #indexPage rather than reusing the cached one. With two home instances
   alive the row fitter measured across the swap and left the visible container
   at top:17px with its rows drawn over the hero. Measured going Live TV -> Home,
   three rounds each:
       pill     1 #indexPage,  0px overlap, clean every round
       drawer   2 #indexPage,  up to 358px of rows on top of the hero
   the admin's suggestion, and it is the better fix: it removes the duplicate view
   instead of correcting the layout afterwards. sf-fit-sanity stays as the net
   for any other route that can still produce one.
   Capture phase so it runs before Jellyfin's delegated handler; every other
   drawer entry falls through untouched. */
document.addEventListener('click',function(e){
try{
var t=e.target,a=(t&&t.closest)?t.closest('a'):null;
if(!a||a.getAttribute('href')!=='#/home')return;
if(!a.closest('.mainDrawer,.navDrawer'))return;
e.preventDefault();e.stopPropagation();
if(e.stopImmediatePropagation)e.stopImmediatePropagation();
var btn=document.querySelector('.mainDrawerButton');
if(btn)btn.click();
location.hash='#/home';
}catch(err){}
},true);
/* sf-nav-everywhere: this used to test the hash for the music route, so ONLY
   the music page got the main pills -- Movies, Shows, Audio Books and Playlists
   were left with just their own tab strip and no way back to Home / Live TV /
   Sports / My Stuff except the drawer. The test is now structural rather than a
   URL whitelist: any header tab strip that does NOT already carry the main
   pills is a library strip and gets them added above it. That covers every
   library page today and any added later with nothing to keep in sync, and
   Home / Live TV / My Stuff are skipped by the same test because they already
   hold the pills. */
/* Library routes only. Deliberately a route list and not "any page with a
   .headerTabs": that container exists on EVERY route -- it is simply left empty
   where there are no tabs -- so keying off its presence would have put the nav
   pills on the search page and on every item detail page too. These six are the
   places you browse a library from. */
function sfLibraryRoute(){
/* `home` deliberately NOT listed: the home header is Jellyfin's own strip
   with our pills injected into it. Treating home as a library route made
   sfMainNav build a second bar whenever the native strip had not laid out
   yet, and the pill injectors then filled that bar too -- the duplicated
   header. See jellyfin-main-nav-pills. */
/* sf-nav-ondetail (2026-09-05). `details` added deliberately, reversing the note
   above -- the admin's decision, and it is the fix for the header shell.
   Measured, the header is 101px on a detail route and 77px on Home. The cause is
   .headerTabs carrying margin-top:-80.2px: it only subtracts height when a pill
   row is present, so the header is 101 by default and the pills are what compress
   it. Detail pages were the one browsing surface without them, which is exactly
   why they were the odd height -- and .page carries
   `padding-top: calc(var(--sf-hdr-h) + 24px)`, so that 24px step moved every
   page's content on entry and exit.
   Adding them makes Home and every detail page one height, and removes the
   pills-vanishing flash on the way in. Library routes stay taller (87px) because
   they genuinely carry a second row -- their own tab strip under our pills --
   which is a real secondary-navigation region rather than drift.
   Three attempts to pin or freeze the height were reverted for making it worse;
   this removes the cause instead. Search stays excluded: it is not a browsing
   surface, which is what the original note was really protecting. */
return /^#\u002F(music|movies|tv|livetv|list|details)\b/.test(location.hash||'');
}

/* sf-nav-everywhere: this used to test the hash for the music route, so ONLY
   the music page got the main pills -- Movies, Shows, Audio Books and Playlists
   were left with just their own tab strip, or nothing at all, and no way back
   to Home / Live TV / Sports / My Stuff except the drawer. The strip that
   already carries the pills identifies itself by containing "My Stuff", so a
   page needs our bar exactly when no visible strip does. */
/* sf-hdrstate-cache: getClientRects() forces a synchronous layout, and this runs
   it for every header strip on every call -- from sfMainNav on the 400ms tick and
   again from the header observers. Profiled at 4x CPU throttle over the load
   window: 570ms, the largest remaining JS cost after align() was coalesced.
   Memoised for 250ms (shorter than the tick) and dropped on hashchange, which is
   when the header actually changes shape. sfMainNav still runs synchronously on
   hashchange for the no-flash behaviour -- it just no longer re-measures the same
   header dozens of times between route changes. */
var _hsVal=null,_hsAt=0;
try{window.addEventListener('hashchange',function(){_hsVal=null;_hsAt=0;},true);}catch(e){}
function sfHeaderState(){
var now=Date.now();
if(_hsVal&&(now-_hsAt)<250&&(!_hsVal.lib||_hsVal.lib.isConnected))return _hsVal;
var bars=document.querySelectorAll('.headerTabs .tabs-viewmenubar'),i,b;
var lib=null,hasMain=false;
for(i=0;i<bars.length;i++){
b=bars[i];
if(!b.getClientRects().length)continue;
if(/My Stuff/.test(b.textContent||'')){hasMain=true;continue;}
if(!lib)lib=b;
}
_hsVal={hasMain:hasMain,lib:lib};_hsAt=now;
return _hsVal;
}

function sfMainNav(){
var st=sfHeaderState();
/* ALL of them: a single querySelector left a second, stale bar behind, which
   is what put a full duplicate pill row on the Home header. */
var stale=document.querySelectorAll('.jf-mu-mainbar');
var bar=stale.length?stale[stale.length-1]:null;
/* sf-nav-staleMain (2026-08-29): the route decides, NOT hasMain.
   hasMain means 'some visible strip already carries the main pills', and on
   home that is correct -- the pills live in Jellyfin's own strip there, so ours
   must not be added. But during a transition INTO a library route the outgoing
   home strip is still in the document while location.hash already says
   #/livetv, so hasMain was momentarily true on a route that genuinely needs our
   bar -- and this branch deleted the pills we had just been asked to show.
   Measured Home -> Live TV, pill count over the switch:
       4 -> 1 -> 0 -> 4      the nav emptied for ~20-80ms
   while Live TV -> Home stayed at 4 throughout, which is why only the one
   direction flickered. .headerTabs itself SURVIVES navigation (verified by
   tagging the node and re-checking isConnected -- only .tabs-viewmenubar is
   replaced), so nothing external was ever removing the bar: we were.
   On a library route a strip advertising 'My Stuff' can only be the home strip
   on its way out, so it is not a reason to drop our pills. The dedupe below
   still guarantees exactly one bar. */
if(!sfLibraryRoute()){
/* sf-nav-noflash: the class and the bar are dropped the moment we are off a
   library page. Both used to be cleared only on the 400ms tick, so Home
   rendered with the shrunken sub-pill sizing still applied and then snapped
   back to full size -- the "home tab row resizes itself" report. hashchange
   now calls this synchronously. */
document.documentElement.classList.remove('sf-music-nav');
for(var _s=0;_s<stale.length;_s++){
if(stale[_s]&&stale[_s].parentNode)stale[_s].parentNode.removeChild(stale[_s]);
}
return;
}
/* Never keep more than one bar on a library route either -- drop every
   older copy and keep the newest, so a rebuild cannot leave a twin behind. */
for(var _d=0;_d<stale.length-1;_d++){
if(stale[_d]&&stale[_d].parentNode)stale[_d].parentNode.removeChild(stale[_d]);
}
/* only dress the library strip as a sub row when there IS one -- Audio Books
   and Playlists have no tabs of their own, just our pills. */
document.documentElement.classList.toggle('sf-music-nav',!!st.lib);
var host=st.lib?st.lib.parentNode:document.querySelector('.headerTabs');
if(!host)return;
/* in the right place already */
if(bar&&bar.parentNode===host&&bar.nextElementSibling===st.lib)return;
/* sf-nav-nogap: this used to remove the existing bar and only then build the
   replacement, so between the two the header had NO main pills at all --
   measured 30ms windows with 0 pills on every entry to Live TV, and longer on a
   slower device. That is the "main nav pill went away" report. Keep the old bar
   in place, build the new one, insert it, and remove the old one only after. */
var sfOldBar=bar;
bar=document.createElement('div');
/* sf-nav-notabbar: deliberately NOT '.tabs-viewmenubar'. The Abyss custom CSS
   hides library tab strips on Movies and Shows --
     body:has(#moviesPage:not(.hide)) .tabs-viewmenubar{opacity:0;height:0;...}
   -- and our bar wearing that class was swallowed by the same rule, which is
   why Movies showed no pills and both sliders stacked at the same y. That rule
   carries !important and an id inside :has(), so nothing we could write here
   outranks it. It turns out the class was never needed: stripped to
   .jf-mu-mainbar, with the styling left to .emby-tabs-slider and
   .emby-button.emby-tab-button, every computed value -- background, radius,
   padding, border, height, font, colour -- came out IDENTICAL (verified by
   toggling the classes on a live bar and diffing). */
bar.className='jf-mu-mainbar';
/* sfMainNav REMOVES the stale bar before drawing the new one, so on any
   navigation there is a frame or two with no .jf-mu-mainbar in the document.
   buildMain's guard below used to test for that element live and therefore
   fired inside that gap, appending its four pills into Live TV's own slider --
   the merged 7-tab bar that flashed on every switch to Live TV. Latch it. */
window.__sfMainNav=1;
var slider=document.createElement('div');
slider.className='emby-tabs-slider';
for(var j=0;j<SFMU.length;j++){
(function(m){
var b=document.createElement('button');
/* .emby-button is the one that matters: it is what supplies border:0 and the
   component metrics. .emby-tab-button alone left a 2px UA border, which made
   our pills 41px against the real 37px. Same shape jf-livetv-tab uses. */
b.type='button';b.className='emby-button emby-tab-button jf-mu-main';b.textContent=m[0];
b.setAttribute('data-sf-nav',m[0]);
/* Stop the event before Jellyfin's emby-tabs delegation sees it. Our pills
   carry .emby-tab-button (needed for the pill metrics) and live inside
   Jellyfin's own slider, but they have no tab index -- so its handler resolved
   a tab controller for nothing and its bundle threw "Cannot find module './'"
   on every Live TV switch. We do our own navigation, so its handler has no work
   to do here anyway. */
b.addEventListener('click',function(e){
e.preventDefault();e.stopPropagation();
if(e.stopImmediatePropagation)e.stopImmediatePropagation();
location.hash=m[1];},true);
slider.appendChild(b);
})(SFMU[j]);
}
bar.appendChild(slider);
if(st.lib)host.insertBefore(bar,st.lib); else host.appendChild(bar);
/* the replacement is live now -- only now is it safe to drop the old one */
if(sfOldBar&&sfOldBar!==bar&&sfOldBar.parentNode)sfOldBar.parentNode.removeChild(sfOldBar);
}

/* sf-nav-sync: the bar goes ABOVE the library tab strip and both live inside
   .skinHeader, so adding it grows the header -- measured 78px to 126px. Doing
   that from the 400ms poll meant the page painted at the old height and then
   everything below jumped down, which is the "sub pill tab has to move down"
   report. React to the strip appearing instead of polling for it: a
   MutationObserver coalesced with requestAnimationFrame runs before the browser
   paints, so the header is already its final height the first time it is drawn.
   hashchange covers leaving; the 400ms interval below stays as a backstop. */
var navRaf=null;
function sfNavSoon(){
if(navRaf)return;
navRaf=requestAnimationFrame(function(){navRaf=null;sfMainNav();});
}
new MutationObserver(sfNavSoon).observe(document.documentElement,{childList:true,subtree:true});
window.addEventListener('hashchange',sfMainNav);
/* sf-nav-observe: polling can only react a tick AFTER Jellyfin tears the header
   down, which still leaves one frame with no pills. Watching the header itself
   rebuilds it in the same task as the teardown, so there is no frame in between.
   childList only, and only on .skinHeader -- an attributes observer here would
   fire on every class change in the header. */
(function(){
function armHdrObserver(){
var hdr=document.querySelector('.skinHeader');
if(!hdr){setTimeout(armHdrObserver,60);return;}
if(hdr.__sfNavObs)return;
hdr.__sfNavObs=1;
var q=false;
try{
new MutationObserver(function(){
if(q)return;
q=true;
requestAnimationFrame(function(){q=false;try{sfMainNav();}catch(e){}});
}).observe(hdr,{childList:true,subtree:true});
}catch(e){}
}
armHdrObserver();
window.addEventListener('hashchange',armHdrObserver);
})();
/* armed as early as possible: this script runs before jellyfin-web's deferred
   bundles, so a reload straight onto Live TV never paints the native strip */
sfLtvAlias();
sfTabArm();
window.addEventListener('hashchange',sfLtvAlias);
window.addEventListener('hashchange',function(){try{sfMusicSoloClass();}catch(e){}});
try{sfMusicSoloClass();}catch(e){}
/* paint placeholders the instant home is entered, rather than up to a tick late */
window.addEventListener('hashchange',function(){try{sfHomeSkeleton();sfHeroSkeleton();}catch(e){}});
try{sfHomeSkeleton();}catch(e){}
window.addEventListener('scroll',sfNavTuck,{passive:true});
document.addEventListener('scroll',sfNavTuck,{passive:true,capture:true});
window.addEventListener('hashchange',function(){document.documentElement.classList.remove('sf-nav-tucked');});
/* Each of these ran in a BARE SEQUENCE, so the first one to throw silently
   killed every function after it for that tick -- and for a persistent DOM
   condition, forever. That presents as "the UI just bugs out": rows vanish,
   the nav stops updating, the capsule freezes, with nothing in the console.
   Isolate each call, and record the failure by NAME so it can be diagnosed
   (window.sfTickFails) instead of disappearing. */
/* sf-home-skeleton: measured on this server, home shows #indexPage at ~1.4s, its
   first cards at ~3.4s, and does not finish filling until ~6.7s -- so there is a
   ~2s dead blank and then a ragged fill. A spinner would show activity but hide
   the structure; placeholder rows show the shape of what is coming.

   The placeholders sit BELOW whatever has already loaded and shrink as real rows
   arrive, so the page never shows a skeleton above content that already exists.
   Two safeguards matter more than the look:
     * a hard deadline, so a skeleton can never outlive a failed load; and
     * the DOM is only rewritten when the NEEDED COUNT changes, otherwise this
       would rebuild 2.5x/second and re-trigger the title-i18n insert observer. */
'''

# _LS_15 (orig L10142-10904) -- sf-sports-exit, sf-pill-show, sf-home-bar-unify
_LS_15 = r'''/* sf-sports-exit: while #/home?sports=1 is up, Jellyfin's OWN Home / My Stuff
   pills are inert. Measured: clicking either left the hash at #/home?sports=1 and
   did nothing at all, while Live TV (which carries its own handler) still worked
   -- so the bar looked present but three quarters of it was dead, which reads as
   "the main pill tab is gone". The sports overlay owns the page, so the tab
   controller never sees a change to act on.
   Give those two an explicit destination that also clears sports=1. The overlay
   hides itself as soon as that flag leaves the hash. For My Stuff the route does
   not re-enter (a known trap here -- see sfHomeTabRepair), so drive the button
   once the overlay is gone rather than waiting out that 4s repair. */
function sfSportsExit(){
if(window.__sfSportsExit)return;
window.__sfSportsExit=1;
document.addEventListener('click',function(e){
if((location.hash||'').indexOf('#/home')!==0)return;
var btn=e.target&&e.target.closest?e.target.closest('.headerTabs .emby-tab-button'):null;
if(!btn||btn.closest('.jf-mu-mainbar'))return;
if(/jf-livetv-tab|jf-sports-tab|jf-sp-tab/.test(btn.className||''))return;
var bar=btn.parentNode,natives=[],i,c;
if(!bar)return;
for(i=0;i<bar.children.length;i++){
c=bar.children[i];
if((c.className||'').indexOf('jf-')===-1)natives.push(c);
}
var idx=natives.indexOf(btn);
if(idx<0)return;
var sports=/[?&]sports=1/.test(location.hash||'');
var dest=(idx===0?'#/home':'#/home?tab='+idx);
/* Off the sports overlay Jellyfin's own controller DOES switch the pane, so let
   it -- only correct the hash so it agrees. Swallowing the click here instead
   left My Stuff -> Home stuck on Favorites, because the pane never changed while
   sfHomeBarUnify kept pinning the highlight to the old hash. */
if(!sports){
if(location.hash!==dest)location.hash=dest;
return;
}
e.preventDefault();
e.stopPropagation();
location.hash=dest;
if(idx>0)setTimeout(function(){try{btn.click();}catch(x){}},280);
},true);
}
/* sf-pill-show: on #/livetv and #/home?sports=1 every header tab button computes
   position:absolute; left:-9999px; visibility:hidden -- Jellyfin's parked state,
   which its emby-tabs component clears when it lays a strip out and which never
   ran on those pages. The result is a header that looks empty: the bar is 7px
   wide with all four pills off-screen and unclickable ("the main pill tab is
   gone"). NB such a button still reports getClientRects().length > 0, which is
   why passes that only read textContent scored the bar as present.
   This is done inline rather than in CSS because a stylesheet rule did NOT win:
   enumerating every loaded sheet found no rule matching the button that sets
   left/position/visibility at all, yet the computed value persisted. Inline with
   'important' wins whatever the source is.
   Buttons Jellyfin genuinely hides use display:none (录制/日程/电视节目) -- that is
   a different mechanism and is deliberately left alone. */
/* sf-pill-batch (2026-09-01). CPU profile of a reload put this function at the
   top of our own costs. It ran on the 30ms tick and, per button, did a
   getComputedStyle READ immediately followed by setProperty WRITES -- so each
   write invalidated style for the next read and every button paid a fresh
   forced recalc, 33 times a second. Same logic, but all reads happen first and
   the writes are applied afterwards, so one recalc covers the whole pass. */
function sfPillShow(){
var btns=document.querySelectorAll('.headerTabs .emby-tab-button'),i,b,cs;
if(!btns.length)return;
var _fix=[];
for(i=0;i<btns.length;i++){
b=btns[i];
cs=getComputedStyle(b);
if(cs.display==='none')continue;
if(cs.position!=='absolute'&&cs.visibility!=='hidden'&&cs.pointerEvents!=='none')continue;
_fix.push(b);
}
if(!_fix.length)return;
for(i=0;i<_fix.length;i++){
b=_fix[i];
b.style.setProperty('position','relative','important');
b.style.setProperty('left','auto','important');
b.style.setProperty('right','auto','important');
b.style.setProperty('visibility','visible','important');
b.style.setProperty('pointer-events','auto','important');
}
}
function sfPillShowOld(){
var btns=document.querySelectorAll('.headerTabs .emby-tab-button'),i,b,cs;
for(i=0;i<btns.length;i++){
b=btns[i];
cs=getComputedStyle(b);
if(cs.display==='none')continue;              /* intentionally hidden tab */
/* pointer-events is the LAST piece of the parked state and outlives the rest:
   once position/visibility are repaired the pills are on-screen and still dead
   to a tap, so it has to be part of the same test. */
if(cs.position!=='absolute'&&cs.visibility!=='hidden'&&cs.pointerEvents!=='none')continue;
b.style.setProperty('position','relative','important');
b.style.setProperty('left','auto','important');
b.style.setProperty('right','auto','important');
b.style.setProperty('visibility','visible','important');
b.style.setProperty('pointer-events','auto','important');
}
}
/* sf-home-bar-unify: the main pill bar had TWO different identities. On #/home
   it is Jellyfin's own home strip with our Live TV / Sports injected, so the
   fourth pill is Jellyfin's FAVORITES tab (我的最爱 / Favoriten). Everywhere else
   it is .jf-mu-mainbar, whose fourth pill is MY STUFF (我的内容 / Meine Sachen).
   Same slot, same destination (#/home?tab=1), two different names -- which is
   exactly "I go to my stuff and it shows favorites".
   Second half: with ?sports=1 the route is still /home, so Jellyfin marks HOME
   active while the user is on Sports ("I switch to sports and the home pill tab
   is highlighted").
   Both are repaired here, on the fast strip so no wrong state is ever painted.
   The label is set to the ENGLISH key so the i18n sweep localises it -- setting a
   translated string directly would go stale on a language change. */
function sfHomeBarUnify(){
var h=location.hash||'';
/* The .jf-mu-mainbar shown on every non-home route had NO active state at all --
   measured "nothing highlighted" on #/livetv for every switch. Mark it from the
   route before doing the home-specific work below. */
var mb=document.querySelector('.jf-mu-mainbar');
if(mb){
var want=null;
if(/^#\/livetv/.test(h))want='Live TV';
else if(/[?&]sports=1/.test(h))want='Sports';
else if(h.indexOf('livetv=1')>=0)want='Live TV';
else if(/^#\/home/.test(h)&&/[?&]tab=1/.test(h))want='My Stuff';
else if(/^#\/home/.test(h))want='Home';
var mbtns=mb.querySelectorAll('.emby-tab-button'),k;
for(k=0;k<mbtns.length;k++){
var key=mbtns[k].getAttribute('data-sf-nav')||mbtns[k].textContent.trim();
mbtns[k].classList.toggle('emby-tab-button-active',!!want&&key===want);
}
}
if(h.indexOf('#/home')!==0)return;
var vis=function(e){if(!e)return false;var cs=getComputedStyle(e);
  return cs.display!=='none'&&e.getBoundingClientRect().width>3;};
var strips=document.querySelectorAll('.headerTabs .emby-tabs-slider'),sl=null,i;
for(i=0;i<strips.length;i++)if(vis(strips[i])&&!strips[i].closest('.jf-mu-mainbar'))sl=strips[i];
if(!sl)return;
var btns=[],c;
for(i=0;i<sl.children.length;i++){c=sl.children[i];if(vis(c))btns.push(c);}
if(btns.length<2)return;
/* ours carry a jf- marker; the rest are Jellyfin's [Home, Favorites] */
var natives=[];
for(i=0;i<btns.length;i++)if((btns[i].className||'').indexOf('jf-')===-1)natives.push(btns[i]);
if(natives.length>=2){
var fav=natives[natives.length-1];
var t=(fav.textContent||'').trim();
/* only rename the Favorites tab, and only once -- never touch Home */
if(fav.getAttribute('data-sf-mine')!=='1'&&t&&!/My Stuff/i.test(t)){
fav.textContent='My Stuff';
fav.setAttribute('data-sf-mine','1');
}
/* claim the two native destinations so buildMain does not add its own copies */
fav.setAttribute('data-sf-nav','My Stuff');
natives[0].setAttribute('data-sf-nav','Home');
}
/* active state must follow the ROUTE, not Jellyfin's idea of the tab index */
var sports=/[?&]sports=1/.test(h), tab1=/[?&]tab=1/.test(h);
/* Live TV is a home pane now (#/home?livetv=1), so on this strip it is just
   another home destination and has to claim the highlight the same way Sports
   does -- otherwise the route says Live TV while the bar says Home. */
var ltv=h.indexOf('livetv=1')>=0;
for(i=0;i<btns.length;i++){
c=btns[i];
var isSports=(c.className||'').indexOf('jf-sports-tab')>-1||(c.className||'').indexOf('jf-sp-tab')>-1;
var isLtv=(c.className||'').indexOf('jf-livetv-tab')>-1;
var want;
if(ltv)want=isLtv;
else if(sports)want=isSports;
else if(tab1)want=(natives.length>=2&&c===natives[natives.length-1]);
else want=(natives.length>=1&&c===natives[0]);
if(isSports&&!sports)want=false;
if(isLtv&&!ltv)want=false;
c.classList.toggle('emby-tab-button-active',!!want);
}
}
/* Measured against the widest strip in the header, and always re-tested from a
   clean state so a language change or a rotation can relax it again. */
function sfPillFit(){
var root=document.documentElement;
var strips=document.querySelectorAll('.headerTabs .emby-tabs-slider,.jf-ltv-sub .jf-fav-tabs'),i,s,over=false;
if(!strips.length)return;
/* Never measure a strip the route CSS has not styled yet. Before home.<hash>.css
   arrives the pills carry stock padding and no capsule geometry, so the fit test
   sees an overflow that is not real and adds tight, then tighter, then tightest,
   then scroll -- all four, in public, then drops them again when the real CSS
   lands. Measured on a cold mobile load: 50px -> 36px wide and 11px -> 9.4px font
   across 6 visible steps in 170ms, then a snap back to 60px/14.4px. */
var fst=null;try{fst=sfStripState();}catch(e){fst=null;}
if(fst&&!fst.styled)return;
var test=function(){
var vw=document.documentElement.clientWidth||window.innerWidth;
for(i=0;i<strips.length;i++){
s=strips[i];
var r=s.getBoundingClientRect();
if(r.width<4)continue;
if(s.scrollWidth>s.clientWidth+2)return true;
if(r.right>vw-4||r.left<-4)return true;
}
return false;
};
root.classList.remove('sf-pill-tight','sf-pill-tighter','sf-pill-tightest','sf-pill-scroll');
if(!test())return;
root.classList.add('sf-pill-tight');
if(!test())return;
root.classList.add('sf-pill-tighter');
if(!test())return;
root.classList.add('sf-pill-tightest');
if(!test())return;
root.classList.add('sf-pill-scroll');
}
function sfMusicRowPlay(){
if((location.hash||'').indexOf('#/music')!==0)return;
var cards=document.querySelectorAll('.verticalSection .card[data-id]'),i,c,id,type,host,btn;
for(i=0;i<cards.length;i++){
c=cards[i];
if(c.getAttribute('data-sf-rp'))continue;
id=c.getAttribute('data-id');
type=c.getAttribute('data-type')||'';
/* only things that can actually be played as audio */
if(!id||!/MusicAlbum|Audio|MusicArtist|Playlist|MusicGenre/.test(type)){
c.setAttribute('data-sf-rp','skip');continue;}
host=c.querySelector('.cardScalable')||c.querySelector('.cardBox')||c;
if(!host){c.setAttribute('data-sf-rp','skip');continue;}
host.classList.add('sf-rowplay-host');
btn=document.createElement('button');
btn.type='button';
btn.className='sf-rowplay';
btn.title='Play';
btn.innerHTML='<span class="material-icons" aria-hidden="true">play_arrow</span>';
(function(itemId,itemType){
btn.addEventListener('click',function(e){
/* the card itself navigates to the album -- this must never reach it */
e.preventDefault();e.stopPropagation();
if(e.stopImmediatePropagation)e.stopImmediatePropagation();
/* These cards already carry Jellyfin's OWN overlay play button, which is the
   path hover-play uses on desktop and is known to work. Drive that first and
   only fall back to the proxy -- re-implementing playback here was the mistake.
   isFolder must be REAL for the fallback: the proxy writes it to data-isfolder
   and a track sent as a folder makes Jellyfin look for children that do not
   exist, which fails silently inside its try/catch. */
var card=e.currentTarget&&e.currentTarget.closest?e.currentTarget.closest('.card[data-id]'):null;
var own=card?card.querySelector('[data-action="play"],[data-action="resume"]'):null;
if(own){own.click();return;}
sfPlayItemViaProxy(itemId,itemType,'Audio',
  /MusicAlbum|MusicArtist|Playlist|MusicGenre/.test(itemType),'play');
},true);
})(id,type);
host.appendChild(btn);
c.setAttribute('data-sf-rp','1');
}
}
/* "收藏的专辑" rendered twice on the music landing (measured: two visible
   sections with identical titles). Keep the first, hide the later duplicate. */
function sfDedupeRows(){
if((location.hash||'').indexOf('#/music')!==0)return;
var secs=document.querySelectorAll('.verticalSection'),seen={},i,s2,t;
for(i=0;i<secs.length;i++){
s2=secs[i];
if(!s2.getClientRects().length){continue;}
t=((s2.querySelector('.sectionTitle,h2')||{}).textContent||'').trim();
if(!t)continue;
if(seen[t]&&seen[t]!==s2){s2.style.display='none';s2.setAttribute('data-sf-dupe','1');continue;}
if(!seen[t])seen[t]=s2;
}
}
/* sf-pill-dedupe: measured on #/home?sports=1 -- ONE slider holding
   首页|直播电视|体育|我的内容|首页|直播电视|体育|我的内容, i.e. the whole main set
   twice, which then reads as an extra pill row on Live TV. Several paths can
   inject these pills (sfMainNav builds .jf-mu-mainbar, buildMain injects into
   Jellyfin's own slider) and any ordering where both run leaves a duplicate.
   Rather than chase every ordering, make a duplicate impossible to survive: a
   label may appear at most ONCE per strip, and two strips may not carry the same
   set. Keep the first occurrence, drop the later one. */
function sfPillDedupe(){
var strips=document.querySelectorAll('.emby-tabs-slider'),i,j,s,kids,seen,txt,k,sig,sigs={};
for(i=0;i<strips.length;i++){
s=strips[i];
kids=[];
for(j=0;j<s.children.length;j++){
k=s.children[j];
if(getComputedStyle(k).display==='none')continue;
kids.push(k);
}
if(kids.length<2)continue;
/* within a strip: a repeated label is always wrong */
seen={};
for(j=0;j<kids.length;j++){
/* Key on the stamped DESTINATION first: the same pill can appear once translated
   and once freshly added in English (measured 首页|直播电视|体育|我的内容|Live T|Sports),
   which a text comparison can never see as a duplicate. */
txt=kids[j].getAttribute('data-sf-nav')||(kids[j].textContent||'').trim();
if(!txt)continue;
if(seen[txt]){
/* drop OURS, not Jellyfin's: removing a native button only makes its controller
   put it back, which is how the dedupe and buildMain ended up fighting at 30Hz */
var dropA=kids[j],keepA=seen[txt];
if(!/jf-sp-tab|jf-mu-main/.test(dropA.className||'')&&/jf-sp-tab|jf-mu-main/.test(keepA.className||'')){
dropA=keepA;seen[txt]=kids[j];
}
if(dropA&&dropA.parentNode)dropA.parentNode.removeChild(dropA);
continue;
}
seen[txt]=kids[j];
}
}
/* across strips: an identical set means a whole duplicated bar */
strips=document.querySelectorAll('.emby-tabs-slider');
for(i=0;i<strips.length;i++){
s=strips[i];
if(s.getBoundingClientRect().width<4)continue;
sig=[];
for(j=0;j<s.children.length;j++){
if(getComputedStyle(s.children[j]).display==='none')continue;
sig.push((s.children[j].textContent||'').trim());
}
if(sig.length<2)continue;
sig=sig.join('|');
if(sigs[sig]){
var host=s.closest('.jf-mu-mainbar')||s;
if(host&&host.parentNode)host.parentNode.removeChild(host);
continue;
}
sigs[sig]=1;
}
}
/* sf-ltv-subdupe: THE third pill row on Live TV. subBar() builds .jf-ltv-sub
   (Programs|Guide|Channels) and appends it to document.body as a stand-in for
   Jellyfin's own sub-tab strip. Its labels are our own English strings, so on a
   Chinese UI the page showed 节目|指南|频道 AND Programs|Guide|Channels stacked --
   measured at y=127 and y=181. It exists because Jellyfin's strip used to be
   parked off-screen; sfPillShow now restores that strip, so this is pure
   duplication. Hide it whenever the real one is on screen, and leave it alone
   otherwise so it can still stand in if the native strip ever fails to lay out. */
function sfLtvSubDupe(){
var mine=document.querySelectorAll('.jf-ltv-sub'),i;
if(!mine.length)return;
var strips=document.querySelectorAll('.headerTabs .emby-tabs-slider'),n=0,j,r;
for(j=0;j<strips.length;j++){
r=strips[j].getBoundingClientRect();
if(r.width>20&&r.height>4&&r.left>-100&&getComputedStyle(strips[j]).display!=='none')n++;
}
/* CORRECTED: it is Jellyfin's own strip that is dead here -- its buttons do
   nothing when tapped and sit off-centre. It was parked off-screen for exactly
   that reason, and sfPillShow dragged it into view. .jf-ltv-sub is the one that
   actually navigates, so keep OURS and hide THEIRS. */
if(/^#\/livetv/.test(location.hash||'')){
var shown=false;
for(i=0;i<mine.length;i++){
if(getComputedStyle(mine[i]).display!=='none'&&mine[i].getBoundingClientRect().height>4)shown=true;
}
if(shown){
for(j=0;j<strips.length;j++){
if(strips[j].closest('.jf-mu-mainbar'))continue;
var host=strips[j].closest('.tabs-viewmenubar')||strips[j];
host.style.display='none';
}
}
}
}
var HDR_UNTIL=0;
/* Ready = every visible pill carries its destination stamp AND, in a translated
   UI, none of them still reads as the English key. A 4s deadline reveals it
   regardless, so a strip that never settles can never leave the header blank. */
/* Superseded by sfTabSettle/sfStripReveal above. This used to own its own
   4s deadline and its own copy of the readiness test, which is how the two
   guards ended up with different selectors, different mechanisms (visibility vs
   opacity) and different expiry times -- and holes between them. One state
   machine now decides, and both classes are released together. */
function sfHdrReady(){
if(document.documentElement.classList.contains('sf-hdr-ready'))return;
sfTabSettle();
}
function sfHdrLang(){
try{
var u=(window.ApiClient&&ApiClient.getCurrentUserId&&ApiClient.getCurrentUserId())||'';
var l=localStorage.getItem(u+'-language')||'';
return l&&l.indexOf('en')!==0;
}catch(e){return false;}
}
/* sf-hdr-order: the music (.sf-music-btn) and language (.sf-lang-btn) buttons are
   injected by two independent scripts, so whichever won the race ended up first
   -- measured alternating across page loads, which is why the two icons appear
   to swap places. Pin the order, immediately before the search button. Only
   touches the DOM when the order is actually wrong.

   sf-hdr-order-v2 (2026-08-27): LANGUAGE now sits left of MUSIC, giving
   SyncPlay . Cast . Language . Music . Search . <user> across the cluster.
   The rule is frequency rising towards the corner, with the account anchored in
   it: SyncPlay and Cast are rare session controls, and language is a set-once
   preference, so all three belong at the far end away from the corner. Before
   this, language sat BETWEEN the two most-used buttons (music and search) --
   a rarely-touched control occupying the prime corner-adjacent slot, which is
   the spot the serial-position effect says goes to the most-used item. */
function sfHdrOrder(){
var right=document.querySelector('.headerRight');
if(!right)return;
var music=right.querySelector('.sf-music-btn');
var lang=right.querySelector('.sf-lang-btn');
if(!music||!lang)return;
var search=right.querySelector('.headerSearchButton');
/* wanted: ... lang, music, search ... */
if(lang.nextElementSibling===music&&(!search||music.nextElementSibling===search))return;
if(search){
right.insertBefore(lang,search);
right.insertBefore(music,search);
}else{
right.insertBefore(lang,music);
}
}
/* One capture-phase handler for the whole home page rather than a listener per
   card: Jellyfin recycles these nodes constantly, so per-card wiring goes stale.
   A tap on the artwork drives the card's OWN resume/play button, which keeps
   Jellyfin's playback path (and its queue handling) rather than reimplementing it. */
function sfHomeTapPlay(){
if(window.__sfHomeTap)return;
window.__sfHomeTap=1;
document.addEventListener('click',function(e){
if((location.hash||'').indexOf('#/home')!==0)return;
/* Our own synthetic click on the card's play button bubbles straight back into
   this capture handler, which then intercepted it again -- so the action never
   reached Jellyfin and the tap appeared to do nothing at all. */
if(window.__sfTapFiring)return;
var t=e.target;
/* The play proxy is itself a .card[data-id] parked inside the home page, so this
   handler was hijacking the proxy's OWN click and breaking playback for our rows
   (which reach playback through it). Never touch it. */
if(t&&t.closest&&t.closest('#sf-play-proxy'))return;
if(!t||!t.closest)return;
if(t.closest('.cardOverlayButton-br')||t.closest('[data-action="menu"]'))return;  /* the ⋮ */
var page=t.closest('#indexPage');
if(!page)return;
/* sf-tap-wholecard (2026-08-29). The admin: "when i click like the edge of a
   poster it takes me to the info page but if i press it in the middle it plays
   the show... its not very clean".
   Requiring the tap to land inside .cardImageContainer/.cardPadder/.cardScalable
   made the play target SMALLER than the poster looks. Measured on a 390px
   layout: the card spans x 7-163 but that inner box only 16-145, so there were
   dead strips of 9px left, 18px right and 9px top where the tap fell through to
   Jellyfin's own link and opened the detail page instead. Two different results
   from one poster, decided by 9px.
   Invert the test: the whole card is the play target EXCEPT the title text,
   which keeps its own <a href="#/details"> (and the corner menu, handled
   above). One rule, no dead strips, and the title still opens the page. */
if(t.closest('.cardText'))return;
var card=t.closest('.card[data-id]');
if(!card)return;
/* sf-card-details: a native card already carries Jellyfin's own link to the
   detail page AND its own play button inside the overlay -- the same markup the
   Movies and Shows pages use. Taking the artwork click away from it meant the
   poster played instead of opening the page, and there was no route to the plot
   or the episode list at all. Leave both alone: artwork opens the page, the play
   button starts playback. This handler stays for the cards that have no such
   link -- our own rows reach playback through it. */
/* sf-tap-artwork-plays (2026-08-29). The admin: "when I'm on mobile and I click a
   show or movie title it should take me to the info page. if I just click the
   tv or movie picture it should play" -- and then: "right now when I press the
   picture it would take me to the info page. I only want it to take us to that
   page if we click the title."
   sf-card-details (above) deliberately handed the artwork BACK to Jellyfin's own
   link, because at the time the artwork was the only route to the plot and the
   episode list. The title is that route now, so on a TOUCH device the artwork
   can go back to meaning play.
   Safe because the handler has already required the tap to be inside
   .cardImageContainer/.cardPadder/.cardScalable, and Jellyfin's card builder
   appends .cardText AFTER those close -- the title is a SIBLING of .cardScalable,
   never a child, so a tap on it is not seen here at all and still follows its own
   <a href="#/details">.
   Two conditions, both required:
     * coarse pointer only. On desktop the overlay play button appears on hover,
       so artwork-opens-the-page stays the least surprising thing there.
     * the card must still HAVE a title link. Some cards render the title as
       plain text (an audiobook shows a bare "1984"), and taking the artwork away
       from them would leave no route to the detail page at all. */
/* sf-wholecard-plays (2026-08-30). The coarse-pointer condition that used to
   guard this meant the whole-card rule applied on TOUCH ONLY, and desktop kept
   Jellyfin's own behaviour. Measured on a 1440 layout, a click anywhere on a
   192x318 poster except the exact middle did NOTHING at all -- the card carries
   padding, so the perimeter lands on the bare .card element, which has no link
   of its own, and this handler returned before it could act. Only the centre
   was live, and it opened the detail page:

       top-left / top-mid / top-right      -> nothing
       left-mid / right-mid                -> nothing
       bot-left / bot-mid / bot-right      -> nothing
       CENTRE                              -> detail page

   the admin: "when i press poster and media cards around the broder now it takes us
   to the info page.. we prefer the entire card to play the media please."
   So the rule is now the same on every pointer: the whole card plays, with two
   exceptions kept deliberately -- the title, which keeps its own link to the
   detail page (asked for earlier: "I only want it to take us to that page if we
   click the title"), and the corner menu, handled further up.

   The one remaining guard is a card with NO title link -- an audiobook renders a
   bare "1984" as plain text -- because taking the artwork from those would leave
   no route to the detail page at all. */
var sfRoute=card.querySelector('.cardText-first a[href], .cardText-first .textActionButton');
if(!sfRoute&&card.querySelector('a.cardImageContainer[href], .cardOverlayContainer[data-action="link"]'))return;
e.preventDefault();
e.stopPropagation();
if(e.stopImmediatePropagation)e.stopImmediatePropagation();
/* Drive the proxy rather than the card's own hidden button: Jellyfin's
   delegation ignores a click on a display:none control, so tapping the artwork
   did nothing at all. The proxy is the path everything else here uses. */
var id=card.getAttribute('data-id');
var type=card.getAttribute('data-type')||'';
var folder=card.getAttribute('data-isfolder')==='true';
var mt=/Audio|MusicAlbum|MusicArtist|Playlist/.test(type)?'Audio':'Video';
/* Prefer the card's OWN control: it already carries the resume position and
   Jellyfin's own playback path. The proxy is the fallback for rows that have no
   such button (ours). */
var btn=card.querySelector('.sf-cardplay,[data-action="resume"],[data-action="play"]');
if(btn){
try{sfSpinShow();}catch(x){}
window.__sfTapFiring=1;
try{btn.click();}finally{setTimeout(function(){window.__sfTapFiring=0;},0);}
return;
}
var pos=card.getAttribute('data-positionticks')||'';
if(!sfPlayItemViaProxy(id,type,mt,folder,pos?'resume':'play',pos))
location.hash='#/details?id='+id;
},true);
}
function sfCardMenus(){
if((location.hash||'').indexOf('#/home')!==0)return;
var cards=document.querySelectorAll('#indexPage .card[data-id]'),i,c,host,btn;
for(i=0;i<cards.length;i++){
c=cards[i];
if(c.getAttribute('data-sf-menu'))continue;
c.setAttribute('data-sf-menu','1');
/* our own rows build their own ⋮ already */
if(c.classList.contains('sf-ml-card'))continue;
host=c.querySelector('.cardScalable')||c.querySelector('.cardBox')||c;
host.classList.add('sf-cardmenu-host');
btn=document.createElement('button');
btn.type='button';
btn.className='sf-cardmenu itemAction cardOverlayButton';
/* the attribute is the point: Jellyfin's delegated handler reads data-action
   from the closest element, so this opens ITS menu rather than a copy of it */
btn.setAttribute('data-action','menu');
btn.setAttribute('title','More');
/* `c` is a var in this loop, so a plain closure here captured the LAST card for
   every button -- every ⋮ reported the final card's id and ticks. Bind per card. */
(function(cardEl){
btn.addEventListener('click',function(){
/* the sheet is Jellyfin's, so the only way to add an item to it is to know
   which card opened it when it appears */
window.__sfMenuFor={id:cardEl.getAttribute('data-id'),
                    ticks:parseInt(cardEl.getAttribute('data-positionticks')||'0',10)||0};
/* Poll for the sheet rather than observing for it: it is not added as one node
   with a recognisable class -- the container is already in the DOM and its
   contents are filled in, so an addedNodes observer never matched. */
if(window.__sfInjectSoon)window.__sfInjectSoon();
},true);
})(c);
btn.innerHTML='<span class="material-icons cardOverlayButtonIcon more_vert" aria-hidden="true"></span>';
host.appendChild(btn);
/* Jellyfin renders no play/resume control on a touch layout either, so a tap on
   the artwork had nothing to drive (the proxy does not carry a video item's
   resume position). Inject a hidden one the same way: itemAction + data-action
   is what its delegation acts on. Hidden with opacity, never display:none --
   a display:none control is skipped by that delegation. */
var pos=c.getAttribute('data-positionticks');
var pb=document.createElement('button');
pb.type='button';
pb.className='sf-cardplay itemAction';
pb.setAttribute('data-action',pos&&pos!=='0'?'resume':'play');
pb.setAttribute('aria-hidden','true');
pb.tabIndex=-1;
host.appendChild(pb);
}
}
/* sf-cw-remove: Jellyfin's own action sheet has no "remove from Continue
   Watching" -- the row is driven by PlaybackPositionTicks, so removal means
   zeroing it (verified: POST /UserItems/{id}/UserData {PlaybackPositionTicks:0}
   drops the item from /Items/Resume, and writing the value back restores it).
   The sheet belongs to Jellyfin, so the entry is injected when it opens, and
   only for a card that actually has a resume position. */
/* sf-cw-remove REMOVED (2026-08-23). This injected a second "Remove" entry at
   the top of the card action sheet, and Jellyfin's own
   data-id="remove-continue-watching" entry renders IDENTICALLY -- same
   visibility_off icon, same short "Remove" label -- so the sheet showed the same
   option twice with no way to tell them apart.
   Verified before deleting ours: clicking the NATIVE entry cleared
   PlaybackPositionTicks to 0 and dropped the card out of the row, i.e. it does
   the server-side reset this custom version existed to provide. Jellyfin caught
   up; the custom one is now pure duplication and one less thing to maintain. */
var SF_SPIN_UNTIL=0,SF_SPIN_TIMER=0,SF_SPIN_AT=0;
/* "Playing" must mean THE PICTURE IS UP, nothing weaker. The first version
   accepted the #/video route or the mere existence of a <video> tag, and both
   happen long before anything is watchable -- measured on a phone profile, the
   route flipped and the element appeared at ~1.3s while the first frame arrived
   at 7.3s, so the spinner vanished and left six seconds of blank screen. That is
   the "it stops spinning before the video loads" half of the report.
   readyState>=2 is HAVE_CURRENT_DATA: there is a frame to show. */
function sfSpinPlaying(){
try{
var m=document.querySelectorAll('video,audio');
for(var i=0;i<m.length;i++){
var e=m[i];
if(!e.paused&&!e.ended&&e.currentTime>0&&e.readyState>=2)return true;
}
}catch(e){}
return false;
}
/* sf-optibar (2026-08-20). Instant feedback, built from what the tap already
   knows -- no network on the critical path.

   Measured before: 558ms before ANYTHING appeared, and Jellyfin's real bar only
   at 2.2-2.3s, i.e. after the music was already audible. That reads as a dead
   tap. Research target is feedback inside ~100ms; Spotify's web player paints
   its bar immediately from local data and lets the audio catch up.

   This paints the same shape as the real bar (art, title, artist, indeterminate
   progress) synchronously in the tap handler, then gets out of the way the
   instant Jellyfin's own bar is on screen. It is purely cosmetic -- it owns no
   playback state, so if anything goes wrong the worst case is a bar that
   removes itself. */
var SF_OPTI_UNTIL=0;
/* sf-rate-guard (2026-08-20). The admin: "randomly during the song it speeds up and
   sounds higher pitched for a few seconds", mostly on mobile.

   That is playbackRate, and the only thing in this app that writes it for AUDIO
   is the audiobook speed control. Its own guards were fixed (sf-rate-confirm),
   but those depend on the now-playing bar's data-itemtype being current, and
   that attribute demonstrably lags the <audio> element by seconds on a switch.
   Rather than keep auditing writers, this makes the invariant structural: on the
   30ms strip, any AUDIO that is not a positively-confirmed audiobook is pinned
   to 1x. Worst case a stray write is audible for one frame instead of seconds.

   Deliberately AUDIO only -- Live TV nudges a VIDEO element's rate to catch up
   and must be left alone. window.__sfRateFixes counts corrections so a real
   device can be asked what it actually caught. */
window.__sfRateFixes=0;
function sfRateGuard(){
var a=document.querySelector('audio');
if(!a)return;
if(Math.abs(a.playbackRate-1)<=0.001)return;      /* already fine, cheap path */
/* is the thing playing REALLY the audiobook the bar is describing? */
var ok=false;
try{
var aid=sfAudioId();
var bars=document.querySelectorAll('.nowPlayingBar'),i,n=null;
for(i=0;i<bars.length;i++){if(bars[i].getClientRects().length){n=bars[i].querySelector('[data-id]');break;}}
if(n&&aid){
var nid=sfNorm(n.getAttribute('data-id'));
if(nid===aid&&(n.getAttribute('data-itemtype')||'')==='AudioBook')ok=true;
}
}catch(e){}
if(!ok){
try{a.playbackRate=1;window.__sfRateFixes++;}catch(e){}
}
}
function sfOptiHide(){
SF_OPTI_UNTIL=0;
var el=document.getElementById('sf-optibar');
if(el&&el.parentNode)el.parentNode.removeChild(el);
}
function sfRealBarUp(){
var n=document.querySelectorAll('.nowPlayingBar'),i;
for(i=0;i<n.length;i++)if(n[i].getClientRects().length)return true;
return false;
}
function sfOptiShow(title,artist,art){
if(sfRealBarUp())return;                 /* the real thing is already there */
var el=document.getElementById('sf-optibar');
if(!el){
el=document.createElement('div');
el.id='sf-optibar';
el.className='sf-optibar';
el.setAttribute('aria-live','polite');
el.innerHTML='<div class="sf-optibar-bar"><i></i></div>'
+'<div class="sf-optibar-art"></div>'
+'<div class="sf-optibar-txt"><div class="sf-optibar-t"></div>'
+'<div class="sf-optibar-a"></div></div>'
+'<div class="sf-optibar-s"></div>';
document.body.appendChild(el);
}
var a=el.querySelector('.sf-optibar-art');
if(art)a.style.backgroundImage='url("'+art+'")';
else a.style.removeProperty('background-image');
el.querySelector('.sf-optibar-t').textContent=title||'';
el.querySelector('.sf-optibar-a').textContent=artist||'';
/* Same 45s ceiling as the spinner, and the same event-driven hides below take
   it down early. */
SF_OPTI_UNTIL=Date.now()+45000;
}
/* Read the three things we need straight off the card that was tapped. Works for
   every one of our rows (music, audiobooks, watchlist) because they all share
   the .sf-ml-card shape. */
function sfOptiFromCard(card){
if(!card)return;
try{
var t=card.querySelector('.cardText-first'),a=card.querySelector('.cardText-secondary');
var p=card.querySelector('.sf-ml-poster');
var art='';
if(p){
var bg=p.style.backgroundImage||'';
var m=/url\(["']?([^"')]+)["']?\)/.exec(bg);
if(m)art=m[1];
}
sfOptiShow(t?t.textContent:'', a?a.textContent:'', art);
}catch(e){}
}
function sfOptiTick(){
if(!SF_OPTI_UNTIL)return;
if(Date.now()>SF_OPTI_UNTIL){sfOptiHide();return;}
/* hand over the moment the real bar exists */
if(sfRealBarUp())sfOptiHide();
}
function sfSpinShow(){
if(sfSpinPlaying())return;                 /* already playing: nothing to wait for */
/* sf-one-spinner: if Jellyfin already has a spinner up, that IS the feedback --
   adding ours puts a second ring on top of it. Still arm the deadline so the
   event-driven hides below stay in charge of ending the wait. */
if(sfJfSpinner()){
SF_SPIN_AT=Date.now();
SF_SPIN_UNTIL=SF_SPIN_AT+45000;
if(SF_SPIN_TIMER)clearTimeout(SF_SPIN_TIMER);
SF_SPIN_TIMER=setTimeout(function(){sfSpinHide();},45000);
return;
}
var el=document.getElementById('sf-playspin');
if(!el){
el=document.createElement('div');
el.id='sf-playspin';
el.className='sf-playspin';
el.setAttribute('aria-busy','true');
el.innerHTML='<i></i>';
/* a tap anywhere dismisses it, so it can never trap the user */
el.addEventListener('click',function(){sfSpinHide();});
document.body.appendChild(el);
}
SF_SPIN_AT=Date.now();
/* 45s, not 25: a cold transcode measured 15s to first frame on this server, and
   the ceiling is no longer the thing that ends the wait -- leaving, playing,
   pausing and erroring all hide it on their own events now, so a generous
   ceiling can no longer strand anyone. */
SF_SPIN_UNTIL=SF_SPIN_AT+45000;
/* The ceiling must NOT depend on the shared 30ms tick. On iPhone the video goes
   into iOS's NATIVE fullscreen player, which hides this page -- and a hidden page
   has its timers suspended, so sfSpinTick never got to run the hide. Coming back
   to home then showed a spinner that nothing owned. This timeout belongs to the
   spinner itself, and the listeners below hide it on the events that actually
   mark the end of the wait, so removal never rides on a timer that may be
   frozen. */
if(SF_SPIN_TIMER)clearTimeout(SF_SPIN_TIMER);
SF_SPIN_TIMER=setTimeout(function(){sfSpinHide();},45000);
}
function sfSpinHide(){
SF_SPIN_UNTIL=0;
try{sfOptiHide();}catch(e){}
if(SF_SPIN_TIMER){clearTimeout(SF_SPIN_TIMER);SF_SPIN_TIMER=0;}
var el=document.getElementById('sf-playspin');
if(el&&el.parentNode)el.parentNode.removeChild(el);
/* belt and braces: any stray duplicate goes too */
var extra=document.querySelectorAll('.sf-playspin');
for(var i=0;i<extra.length;i++)if(extra[i].parentNode)extra[i].parentNode.removeChild(extra[i]);
}
/* Is the play actually going somewhere? A blind timer is not good enough: the
   first version bailed at 12s and was measured hiding the spinner 15s before a
   genuinely slow start produced its video element (server under load, 28s to
   first frame) -- which is the early-hide bug all over again.
   So the bail needs a real progress signal. A PerformanceObserver is the
   read-only way to get one: playback setup is a stream of requests (PlaybackInfo,
   then the segments themselves), and while those keep landing the play is alive
   however slow it is. Only when NOTHING has happened for a long stretch is the
   tap genuinely dead. Defaults to "in progress" on any error, so a browser
   without the observer never hides early. */
var SF_NET_LAST=0;
try{
new PerformanceObserver(function(list){
var es=list.getEntries();
for(var i=0;i<es.length;i++){
if(/PlaybackInfo|\/Videos\/|\/Audio\/|\/videos\/|\.m3u8|hls|Transcod/i.test(es[i].name||'')){
SF_NET_LAST=Date.now();break;
}}}).observe({type:'resource',buffered:true});
}catch(e){SF_NET_LAST=-1;}
function sfSpinProgress(){
try{
if(SF_NET_LAST===-1)return true;              /* no observer: never bail early */
if((location.hash||'').indexOf('#/video')===0)return true;
var m=document.querySelectorAll('video,audio');
for(var i=0;i<m.length;i++){
if(m[i].networkState===2||m[i].readyState>=1)return true;
}
if(SF_NET_LAST&&Date.now()-SF_NET_LAST<10000)return true;
}catch(e){return true;}
return false;
}
'''

# _LS_16 (orig L10904-11591) -- sf-one-spinner, sf-skel-max2, sf-dskel-scope
_LS_16 = r'''/* sf-one-spinner (2026-08-20): TWO loading circles at once.
   Ours (#sf-playspin, a full-screen scrim with a 52px ring) exists because
   Jellyfin does not always raise its own. But when Jellyfin DOES raise
   .docspinner it lands at z-index 9999999, one above ours, so both are painted
   -- measured on a phone: two concentric rings for the whole of a mix start.
   Jellyfin's is the better signal when it exists, so ours steps aside for it and
   stays purely as the fallback for the cases where nothing else appears. */
function sfJfSpinner(){
var n=document.querySelectorAll('.docspinner'),i;
for(i=0;i<n.length;i++)if(n[i].getClientRects().length)return true;
return false;
}
function sfSpinTick(){
if(!SF_SPIN_UNTIL)return;
if(sfSpinPlaying()||Date.now()>SF_SPIN_UNTIL){sfSpinHide();return;}
/* never two at once */
if(sfJfSpinner()){
var el=document.getElementById('sf-playspin');
if(el&&el.parentNode)el.parentNode.removeChild(el);
return;                       /* keep the deadline: if Jellyfin's goes away and
                                 we are still waiting, ours comes back */
}
if(Date.now()-SF_SPIN_AT>20000&&!sfSpinProgress())sfSpinHide();
}
/* Event-driven hides -- the part that actually fixes the stuck spinner.
   The original only ever hid from the 400ms/30ms sweep, so the spinner outlived
   anything that stopped the sweep from reaching a hide: on a phone, tapping a
   card and then leaving straight away meant nothing ever satisfied "is it
   playing", and the spinner sat on the home page until the ceiling expired.
   Each listener below marks the end of the wait on its own event, on the main
   thread, independent of any timer. */
(function sfSpinGuards(){
function bail(){if(SF_SPIN_UNTIL)sfSpinHide();}
/* coming back from the native fullscreen player or any background state */
document.addEventListener('visibilitychange',function(){
if(!document.hidden&&SF_SPIN_UNTIL&&!sfSpinPlaying())sfSpinHide();});
window.addEventListener('pageshow',bail);
window.addEventListener('focus',function(){
if(SF_SPIN_UNTIL&&!sfSpinPlaying())sfSpinHide();});
/* leaving the player, or landing anywhere that is not the play we asked for */
window.addEventListener('hashchange',function(){
if(!SF_SPIN_UNTIL)return;
if((location.hash||'').indexOf('#/video')===0)return;   /* the player: keep waiting for the picture */
if(Date.now()-SF_SPIN_AT>1200)sfSpinHide();});
window.addEventListener('popstate',function(){
if(SF_SPIN_UNTIL&&Date.now()-SF_SPIN_AT>1200)sfSpinHide();});
/* Real playback events. A capture listener on document sees non-bubbling events
   too -- which includes every <img> that fails to load, so the target MUST be
   checked or one broken poster kills the spinner. */
function media(e){
var t=e&&e.target,n=t&&t.tagName;
if(n!=='VIDEO'&&n!=='AUDIO')return;
bail();
}
['playing','loadeddata','pause','ended','error','abort'].forEach(function(ev){
document.addEventListener(ev,media,true);});
if(window.Events&&window.Events.on){
try{['playbackstart','playbackstop','playbackerror'].forEach(function(ev){
window.Events.on(window,ev,bail);});}catch(e){}
}
})();
/* sf-skel-max2: SKEL_MAX was 4. CLS is impact-AREA x distance, and this
   skeleton sits below the rows and gets shoved down as each real row lands --
   so the taller it is, the more every shove costs. Measured 2026-08-25 in
   interleaved A/B runs (the only way to compare on this box; CLS swings
   0.001-0.571 between identical loads, so before/after across different load
   conditions proves nothing):

     4 rows  median 0.264  mean 0.326
     2 rows  median 0.222  mean 0.227   -- won 4 of 6 paired runs

   Two rows still covers the fold on a phone, so the anti-FOUC job is done,
   while costing roughly a third less shift. Going to 1 row measured WORSE
   (0.261) -- less reservation starts costing more than the area saves.
   Note also: matching the skeleton's row heights to the real rows made CLS
   slightly WORSE (0.165 -> 0.191), because a more accurate skeleton is a
   TALLER one. Accuracy is not the goal here; area is. */
var SKEL_TARGET=10,SKEL_MAX=2,SKEL_CARDS=8,SKEL_UNTIL=0;
var HERO_UNTIL=0;
/* Placeholder for the Media Bar hero. Its height is MEASURED at runtime (the gap
   between the tab content and the first row) rather than hard-coded, because that
   band is not created by a margin or padding we could read -- and a wrong guess
   would either leave a strip of background or overlap the first row. */
function sfHeroSkeleton(){
var el=document.getElementById('sf-skel-hero');
var tc=document.querySelector('#indexPage:not(.hide) .tabContent.is-active');
function drop(){
if(el&&el.parentNode)el.parentNode.removeChild(el);
if(tc)tc.classList.remove('sf-skel-anchor');
}
/* sf-hero-skel-off (2026-09-04). The admin: "i see the hero skeleton load in in
   multiple places .. maybe we should remove it all together". It was scoped to
   #/home and tab=0, but that test passes for ?sports=1 and ?livetv=1 too (no
   `tab` param at all), so it could render on surfaces that have no hero.
   Switched off rather than re-scoped, as asked. The band it filled is RESERVED
   by layout either way -- the `band<160` test below only ever ran once the space
   existed -- so nothing shifts; that area is simply dark until the hero paints.
   The body of the function is kept so this is one line to reverse, and drop()
   still runs so any skeleton left over from a previous build is cleaned up. */
drop();HERO_UNTIL=0;return;
/* eslint-disable no-unreachable */
if(!/^#\/home/.test(location.hash||'')){drop();HERO_UNTIL=0;return;}
var m=/[?&]tab=(\d+)/.exec(location.hash||'');
if(m&&m[1]!=='0'){drop();return;}
if(!tc){drop();return;}
/* the hero has painted -- this is done */
if(document.querySelector('.slide')){drop();return;}
if(!HERO_UNTIL)HERO_UNTIL=Date.now()+15000;
if(Date.now()>HERO_UNTIL){drop();return;}
var hs=tc.querySelector('.homeSectionsContainer');
if(!hs)return;
var band=Math.round(hs.getBoundingClientRect().top-tc.getBoundingClientRect().top);
if(band<160)return;              /* band not reserved yet: adding one would shift the page */
if(!el){
el=document.createElement('div');
el.id='sf-skel-hero';
el.className='sf-skel-hero';
el.setAttribute('aria-hidden','true');
el.innerHTML='<div class="sf-skel-htitle sf-skel-sh"></div>'
+'<div class="sf-skel-hmeta sf-skel-sh"></div>'
+'<div class="sf-skel-hbtns"><div class="sf-skel-hbtn sf-skel-sh"></div>'
+'<div class="sf-skel-hbtn sf-skel-hbtn2 sf-skel-sh"></div></div>';
}
tc.classList.add('sf-skel-anchor');
if(el.style.height!==band+'px')el.style.height=band+'px';
if(el.parentNode!==tc)tc.insertBefore(el,tc.firstChild);
}

var DSKEL_UNTIL=0,DSKEL_SINCE=0,DSKEL_DONE=false;
/* sf-dskel-scope (2026-08-29): this shimmer is an ALBUM/BOOK shape -- square
   art, a title, two pills -- and it exists because those pages sit on a bare
   spinner for ~2s (see the .sf-dskel CSS comment). A Movie/Series/Season/
   Episode page does not have that problem: sfDetailHero keeps the page dark and
   fades it in COMPLETE once its backdrop has decoded, so the skeleton adds no
   information there and only paints a wrong-shaped box in the top-left corner,
   over a hero that has already finished. The admin: "when i go into a show or
   movies info page, i see like loading in the top left, i dont want to see this
   in these pages".
   So resolve the item's Type once per id and only stand in for the page kinds
   the shape was drawn for. Unknown or in-flight type = no skeleton: guessing
   wrong is the whole complaint, and being late costs nothing. */
var DSKEL_TYPE={},DSKEL_ID='';
var DSKEL_OK={MusicAlbum:1,Playlist:1,MusicArtist:1,AudioBook:1,Book:1};
function dskelAllowed(id){
if(!id)return false;
var t=DSKEL_TYPE[id];
if(t!==undefined)return !!DSKEL_OK[t];
var ac=window.ApiClient;
if(!ac||!ac.getItem||!ac.getCurrentUserId)return false;
DSKEL_TYPE[id]=null;
try{ac.getItem(ac.getCurrentUserId(),id).then(function(it){
DSKEL_TYPE[id]=(it&&it.Type)||'';},function(){DSKEL_TYPE[id]='';});}
catch(e){DSKEL_TYPE[id]='';}
return false;}
function sfDetailSkeleton(){
var el=document.getElementById('sf-dskel');
function drop(){if(el&&el.parentNode)el.parentNode.removeChild(el);}
if(!/^#\/details/.test(location.hash||'')){drop();DSKEL_UNTIL=0;DSKEL_SINCE=0;DSKEL_DONE=false;return;}
/* Reset per ITEM, not just on leaving details: Jellyfin reuses one view, so
   without this the deadline and the 'already finished' latch leak from the
   previous item into the next one. */
var dm=/[?&]id=([a-zA-Z0-9]+)/.exec(location.hash||'');
var did=dm?dm[1]:'';
if(did!==DSKEL_ID){DSKEL_ID=did;DSKEL_UNTIL=0;DSKEL_SINCE=0;DSKEL_DONE=false;drop();}
if(!dskelAllowed(did)){drop();return;}
/* Host on BODY, not on #itemDetailPage. Measured: that element does not exist
   until ~2200ms into a cold load, while the bare-spinner window starts at ~0 --
   so anything parented to it can only cover the last half second of the wait,
   which is the part that never needed covering. */
/* Jellyfin caches ONE VIEW PER URL and leaves it in the DOM, so a bare
   querySelector finds the .sf-alb-hero of a page visited earlier and concludes
   this page is already rendered. Measured: after visiting an album, opening a
   book reported hero@0.002s from the album's own hidden view, and the skeleton
   never appeared again for the rest of the session. Only a PAINTED node counts. */
function painted(sel){
var n=document.querySelectorAll(sel),i;
for(i=0;i<n.length;i++)if(n[i].getClientRects().length)return true;
return false;
}
/* sf-dskel-exit: the old test asked ONLY for our album hero. That element is
   built for MusicAlbum / AudioBook / MusicArtist / Playlist and for nothing else
   (see the isAlbum test in the album-stage block), so on a Movie, Series,
   Episode or Season page the condition could never become true and the only way
   out was the 12s DSKEL_UNTIL deadline -- a square, album-shaped shimmer sitting
   over a movie page that had already finished rendering. Same shape of bug as
   the pill guards: the exit signal never fires, so the deadline IS the normal
   path. Verified in the browser on #/details for a Movie, a Series and an
   Episode: .sf-alb-hero and .sf-alb-play both measure 0 painted nodes, while the
   stock .itemName is painted and filled.
   So: our hero when it is that kind of page, and the stock detail title
   otherwise. Both mean the same thing -- the real content is on screen. */
function detailReady(){
if(painted('.sf-alb-hero')||painted('.sf-alb-play'))return true;
/* sf-dskel-atv: sfDetailHero marks a finished page with .sf-atv on
   #itemDetailPage. Measured on a Series (Community) before this existed:
   .itemName painted at 1.65s so the skeleton dropped at 1.87s -- then the hero
   took the title over, .itemName stopped being painted, the exit test went
   FALSE again and the skeleton was RE-INSERTED at 2.73s on top of a fully
   rendered page, with only the 12s deadline to clear it (gone at 14.67s).
   A ready signal that can revert is not a ready signal. */
if(painted('#itemDetailPage.sf-atv'))return true;
var dn=document.querySelectorAll('.itemDetailPage:not(.hide) .itemName'),di;
for(di=0;di<dn.length;di++){
if(!dn[di].getClientRects().length)continue;
if((dn[di].textContent||'').trim())return true;
}
return false;
}
if(detailReady()){
drop();DSKEL_DONE=true;DSKEL_UNTIL=0;DSKEL_SINCE=0;return;}
/* Once this item has rendered it stays rendered -- never stand in front of it
   again, whatever any individual probe says a second later. */
if(DSKEL_DONE){drop();return;}
var page=document.body;
if(!page){drop();return;}
if(!DSKEL_UNTIL){DSKEL_UNTIL=Date.now()+12000;DSKEL_SINCE=Date.now();}
/* if the load has stalled, show the page as it really is rather than a lie */
if(Date.now()>DSKEL_UNTIL){drop();return;}
/* Grace period. Revisiting a page whose view is already cached renders almost
   immediately, and inserting straight away produced a 150ms flash of skeleton
   over content that was about to appear anyway. Only stand in for a wait that
   is actually happening. */
if(Date.now()-DSKEL_SINCE<320)return;
if(el&&el.parentNode===page)return;
if(!el){
el=document.createElement('div');
el.id='sf-dskel';el.className='sf-dskel';
el.innerHTML='<div class="sf-dskel-art sf-skel-sh"></div>'
+'<div class="sf-dskel-meta"><div class="sf-dskel-t sf-skel-sh"></div>'
+'<div class="sf-dskel-s sf-skel-sh"></div>'
+'<div class="sf-dskel-btns"><div class="sf-dskel-b sf-skel-sh"></div>'
+'<div class="sf-dskel-b2 sf-skel-sh"></div></div></div>';
}
page.insertBefore(el,page.firstChild);
}
/* ---- sf-home-settle (2026-08-28) -----------------------------------------
   the admin: "it doesn't feel premium -- sometimes rows load and overlap the hero,
   or it loads a different row like Watchlist first and then Continue Watching
   takes over as the first row."

   Both are the same thing: Jellyfin's home sections arrive one at a time and
   each is painted the moment it exists, so whichever lands first is briefly THE
   first row. Recorded on a 1440x900 load:

       6796ms  1 row   "Recently Added Movies"          <- top of the page
       7405ms  2 rows  "Continue Watching > Recently Added Movies"
       8867ms  9 rows
       firstY walked 505 -> 495 -> 486 -> 505 -> 490 -> 485

   The skeleton (sfHomeSkeleton) fills the empty space but never holds the real
   rows back, so it cannot stop the top row changing under you.

   So: keep the real sections invisible until the row that BELONGS at the top is
   there, then bring them in together. The skeleton stays visible underneath the
   whole time -- it is a sibling, not a .verticalSection, so the rule below does
   not touch it and the page never looks empty.

   Ready = Continue Watching is on screen, or 3s have passed since the first row
   appeared (a listener with nothing in progress has no Continue Watching at all
   and must not wait for one). Measured gap to close: ~600ms.
   The CSS carries its own 6s failsafe reveal, so a thrown error here can never
   leave the page permanently blank. */
var sfHomeFirstAt=0,sfHomeLastCount=-1,sfHomeLastChange=0;
var sfFirstN=-1,sfFirstAt=0;
/* sf-frame-ready (2026-09-01). The admin: "it works sometimes but not all the
   time". Measured across reloads: the entrance renders 14-22 frames over ~500ms
   with wildly uneven spacing -- the animation is correct, but during load the
   main thread is contended and the browser simply does not deliver frames to
   draw it, so it lands as a pop. Whether a given reload looked right was down to
   whether the thread happened to be free at that instant, which is exactly the
   "sometimes" behaviour.
   Track real frame delivery and only release the first view once frames are
   actually flowing. Three consecutive frames under 34ms (~30fps or better) is
   enough to know the thread is keeping up. The existing time caps still release
   regardless, so a permanently busy thread can never stall the page. */
var sfFrmLast=0,sfFrmGood=0;
function sfFrmTick(ts){
try{
if(sfFrmLast){var _d=ts-sfFrmLast;if(_d<34){sfFrmGood++;}else{sfFrmGood=0;}}
sfFrmLast=ts;
}catch(e){}
if(window.requestAnimationFrame)requestAnimationFrame(sfFrmTick);
}
try{if(window.requestAnimationFrame)requestAnimationFrame(sfFrmTick);}catch(e){}
function sfHomeSettle(){
if(!/^#\/home/.test(location.hash||'')){sfHomeFirstAt=0;return;}
/* My Stuff is a different surface with its own rows */
var m=/[?&]tab=(\d+)/.exec(location.hash||'');
if(m&&m[1]!=='0'){sfHomeFirstAt=0;return;}
var page=(window.__jfView&&window.__jfView.homePage&&window.__jfView.homePage())
  ||document.querySelector('#indexPage');
if(!page)return;
var host=page.querySelector('.homeSectionsContainer');
if(!host||host.getAttribute('data-sf-settled'))return;
/* sf-splash-gate (2026-09-01). Measured, and this was the real fault: the row
   entrance ran while the SPLASH was still covering the screen. Timed on a real
   reload -- fade began at 1748ms with the splash visible, reached opacity 0.903
   at 1947ms, and the splash only cleared at 2009ms with the row already at
   0.959. Ninety-six percent of the animation was spent where nobody could see
   it, so the row appeared to snap into place. That is why every timing fix
   measured correct and still looked like a flash.
   Hold the release until the splash is actually gone, so the entrance plays in
   view. Returning here leaves the rows held by the sf-prehold rule, and the 6s
   sfHomeFailsafe still guarantees they reveal if the splash never clears. */
var _sp=document.querySelector('.splashLogo');
if(_sp&&_sp.getClientRects().length)return;
/* sf-hold-gate (2026-09-04). THE cause of "the CW row just flashes in on a
   fresh page load", measured directly rather than inferred.
   sf-holdrows puts `visibility:hidden` on every row (via .sf-hold on this
   container) until the top rows have stopped moving, and sfHoldRows releases
   that on a completely separate condition from this function: it waits for
   ContinueWatching AND NextUp to be laid out and for the layout to be stable,
   on the 400ms tick. This function arms the entrance on ContinueWatching alone,
   on the 30ms tick. Two independent gates, and nothing coupled them.
   So the entrance was armed while the row was still visibility:hidden and ran
   to completion unseen. Instrumented over 11 consecutive reloads: sfHomeInV2
   started at ~1680ms with visibility:hidden, ticked through all 700ms hidden,
   reported finished@700 at ~2400ms -- and .sf-hold only came off at ~2930ms,
   ~550ms AFTER the animation had ended. 0 of 33 entrance frames were visible on
   every single run. The row therefore appeared in one frame, already at its
   final opacity and translate: the flash.
   This is also exactly why leaving home and coming back looks right. sfHoldRows
   stamps host.__sfHoldDone on the container element, and a soft navigation
   reuses that element -- so .sf-hold is never re-applied and sfFloatPass's
   entrance plays in full view (verified: sfFinA/sfFinB, vis=visible, every
   time). Only a document reload builds a fresh container and re-arms the hold.
   The fix is the same principle already applied to the splash above and to
   [data-sf-settle] in sfFloatPass below: no entrance may start before the user
   can actually see the element. Returning here leaves the rows held by
   sf-prehold, and sfHoldRows' own HOLD_MS cap plus its deadman timer guarantee
   the hold always lifts.
   This is a flag rather than an early return on purpose. Returning here also
   stopped this function's clocks -- sfHomeFirstAt is set further down -- so the
   900ms frame-ready wait restarted the instant the hold lifted and left the row
   blank for another ~780ms after the skeleton had already gone (measured: hold
   off at 2591ms, entrance armed at 3367ms). The timers must keep running
   through the hold; only the two arming actions below wait on it. */
var _held=host.classList.contains('sf-hold');
var secs=host.querySelectorAll('.verticalSection'),vis=0,i;
for(i=0;i<secs.length;i++)if(secs[i].getClientRects().length)vis++;
if(!vis){host.setAttribute('data-sf-settle','1');return;}
if(!sfHomeFirstAt)sfHomeFirstAt=Date.now();
var cw=host.querySelector('.ContinueWatching');
/* sf-cw-first (2026-09-01). The admin: continue watching, the hero and the header
   are the FIRST VIEW and should load in first. sf-home-settle holds every row
   until the whole set stops growing (up to 6s), so the first view was hostage
   to the slowest row below the fold. Release the above-the-fold rows -- the
   Continue Watching row and anything ordered above it -- as soon as CW is
   visible and its hidden set has been applied. The rest stay held and still
   arrive together behind them, so nothing pops in one at a time. */
/* sf-firstview (2026-09-01). The admin: the header, hero and CW row are the FIRST
   VIEW and must arrive first, smoothly; a user with no Continue Watching should
   get the next row instead. Measured before this: the batch released at 3175ms
   with 4 rows visible while CW was still at opacity 0, and CW only appeared at
   4009ms -- the first view was arriving LAST. Two changes: the anchor falls back
   to the first visible row when there is no CW (so new users get the same
   treatment), and sfHidden is only required when there IS a CW row to filter. */
if(!_held&&!host.getAttribute('data-sf-first')&&(!cw||sfHidden)&&/* sf-withhero (2026-09-01). The admin: he would rather the first row came in WITH
   the hero than with the rest of the rows. Measured: hero is fully up at 1702ms
   (it has no entrance animation of its own -- it simply appears), the CW row
   exists in the DOM at 3455ms, but my gates held its entrance until 4543ms. So
   ~1.1s of the 2.8s gap was self-inflicted. Keep the frame-ready check, since it
   is what made the entrance consistent, but cap its wait at 900ms instead of 3s
   and accept 2 good frames -- enough to know the thread is drawing, without
   parking the row long after it is ready. */
(sfFrmGood>=2||(Date.now()-sfHomeFirstAt)>900)){
var _cwsec=cw?((cw.closest&&cw.closest('.verticalSection'))||cw):null;
if(!_cwsec){for(var _q=0;_q<secs.length;_q++){if(secs[_q].getClientRects().length){_cwsec=secs[_q];break;}}}
if(_cwsec&&_cwsec.getClientRects().length){
var _f=[],_fi;
for(_fi=0;_fi<secs.length;_fi++)if(secs[_fi].getClientRects().length)_f.push(secs[_fi]);
_f.sort(function(a,b){
var oa=parseFloat(getComputedStyle(a).order)||0,ob=parseFloat(getComputedStyle(b).order)||0;
if(oa!==ob)return oa-ob;
return (a.compareDocumentPosition(b)&4)?-1:1;});
var _ci=-1;
for(_fi=0;_fi<_f.length;_fi++)if(_f[_fi]===_cwsec){_ci=_fi;break;}
if(_ci>=0){
/* sf-first-stable (2026-09-01). The admin: it "flashes in and then shifts down
   slightly". Releasing CW the instant IT was ready was not enough: the home
   rows are placed by CSS `order`, so a row ordered ABOVE Continue Watching that
   arrives later pushes CW down after you have already seen it -- a layout
   shift, not an opacity problem. Release the first view as a UNIT instead: hold
   until the above-the-fold count has been unchanged for 250ms, so nothing can
   still slot in above CW. Capped at 2.5s so a row that never comes cannot stall
   the first view. */
var _fn=_ci+1,_fnow=Date.now();
if(sfFirstN!==_fn){sfFirstN=_fn;sfFirstAt=_fnow;}
if(!sfFirstAt)sfFirstAt=_fnow;
/* sf-hold-handoff (2026-09-04). When sf-holdrows ran, this window is redundant
   work already done: sfHoldRows holds the reveal until Continue Watching AND
   Next Up are laid out AND the first row's bottom is unchanged since its
   previous tick -- a strictly stronger test than "the above-the-fold count has
   not changed for 80ms". Re-testing it cost one more 400ms tick with the
   skeleton already removed and the rows sitting at opacity 0, i.e. a blank fold.
   __sfHoldDone is only set once the hold has actually released. */
var _preStable=!!(host.__sfHoldDone);
if(_preStable||(_fnow-sfFirstAt)>=80||(_fnow-sfHomeFirstAt)>2500){
for(_fi=0;_fi<=_ci;_fi++){
_f[_fi].style.setProperty('--sf-row-i',_fi<8?_fi:8);
_f[_fi].classList.add('sf-first');
/* sf-first-nodouble (2026-09-01). Measured: the first-view rows animated in with
   sfHomeIn while the container was still [data-sf-settle], finished at ~1265ms,
   then at ~3045ms the container flipped to [data-sf-settled] -- so sfFloatPass
   stopped skipping them, found no float token, and ran the WHOLE entrance again
   as sfFinA. The row visibly faded out and back in ~1.8s after it had settled.
   Claim the current float token here: these rows have already had their
   entrance, so sfFloatPass must treat them as done. */
try{_f[_fi].setAttribute('data-sf-fin',String(_finTok));}catch(e){}
}
host.setAttribute('data-sf-first','1');
}
}
}
}
/* sf-settle-stable (2026-08-29). The admin: "ideally i want each row to have the
   same load in time and have it load in cleanly."
   The old gate released as soon as Continue Watching existed (or 3s), which is
   the moment the FIRST rows land -- everything slower then popped in one at a
   time behind it. Measured on a cold home: rows appeared at 14.49 / 14.74 /
   14.74 / 14.74 / 17.53 / 18.03 / 19.56 / 21.09 / 21.34s -- one clean batch of
   four, then five separate arrivals over the next seven seconds.
   Wait for the SET TO STOP GROWING instead: hold while the visible-row count is
   still changing, release once it has been steady for 700ms. Rows that arrive
   within the same burst therefore reveal together.
   Two caps stop this ever becoming a blank page: 6s from the first row when
   there is a Continue Watching row to wait for, 3s when there is not (a
   listener with nothing in progress must not be made to wait for a row that is
   never coming). The skeleton covers the hold, and anything landing after the
   release still fades in on its own via sf-floatin rather than popping. */
var _now=Date.now();
if(vis!==sfHomeLastCount){sfHomeLastCount=vis;sfHomeLastChange=_now;}
/* sf-settle-quick (2026-09-01). The admin: the CW row is missing while the scroll
   bar grows, then rows just show up. Measured: rows kept arriving until 4805ms,
   so the 700ms stability window kept resetting and the batch released at 5928ms
   -- 4.4s after the splash cleared, with every row invisible but still taking up
   layout, which is why the scrollbar moved with nothing on screen. Shorten the
   window; anything arriving after the release still flows in on its own via
   sfFloatPass, which is the progressive fill we actually want. */
var _stable=(_now-sfHomeLastChange)>300;
var _hasCw=!!(cw&&cw.getClientRects().length);
/* sf-cw-settle (2026-09-01). The Continue Watching row flashed in on a
   reload while every other row slid in. The stagger below was already
   right; the row was simply released BEFORE the hidden-content fetch had
   marked the removed cards, so it animated and then reflowed. Hold the
   release until sfHidden is populated when a Continue Watching row exists.
   The 6s/3s caps are untouched, and sfLoadHidden catch sets sfHidden to an
   empty object, so a failed request can never hold the page hostage. */
/* sf-firstview-order: the batch may not release before the first view has.
   Without this the timeout path fired first and the rest of the page overtook
   Continue Watching. The 4s hard cap still guarantees the page is never stuck. */
var _fvDone=!!host.getAttribute('data-sf-first');
var ready=((_hasCw&&_stable&&!!sfHidden)||(_now-sfHomeFirstAt>(_hasCw?2000:1500)));
if(ready&&!_fvDone&&(_now-sfHomeFirstAt)<4000)ready=false;
if(ready&&!_held){
/* sf-row-stagger (2026-08-29). The admin liked how the favorites rows "flow in" and
   asked for the same on home. That effect is Abyss's abyss-section-fade-up:
   0.7s, opacity 0 + translateY(20px), cubic-bezier(.16,1,.3,1), staggered 0.05s
   per row. Abyss keys the stagger off .verticalSection:nth-child(N) -- which is
   DOM order. That is fine on favorites but WRONG here: the home rows are placed
   with CSS `order` (the first row on screen carries order:2), so nth-child would
   fire the stagger in an order that has nothing to do with what you see, with
   rows lower down lighting up before the top one. Stamp the index in VISUAL
   order instead and let the CSS read it. Capped at 8 (0.4s) so a long home page
   does not keep animating well after it has settled -- the same idea as Abyss's
   own :nth-child(n+9) cap. */
var _ord=[],_k;
for(_k=0;_k<secs.length;_k++)if(secs[_k].getClientRects().length)_ord.push(secs[_k]);
_ord.sort(function(a,b){
var oa=parseFloat(getComputedStyle(a).order)||0,ob=parseFloat(getComputedStyle(b).order)||0;
if(oa!==ob)return oa-ob;
return (a.compareDocumentPosition(b)&4)?-1:1;});
/* before the attribute below: the animation starts when [data-sf-settled]
   appears, so the delay has to already be on the element */
for(_k=0;_k<_ord.length;_k++)_ord[_k].style.setProperty('--sf-row-i',_k<8?_k:8);
host.removeAttribute('data-sf-settle');
host.setAttribute('data-sf-settled','1');
}else{
host.setAttribute('data-sf-settle','1');
}
}
/* sf-floatin (2026-08-29). The admin: every page should flow in like favorites, and
   "sports then home doesn't do the float in".
   Cause: a CSS animation runs ONCE per element. Sports is not a separate page --
   it is #/home?sports=1, the same homeTab pane holding the same .verticalSection
   nodes (measured: 9 sections / 82 cards on Sports, 10 / 98 on Home, same
   container). Switching between them re-uses those elements, so nothing
   re-triggers. Live TV -> Home DOES animate only because that route tears the
   page down and rebuilds it.
   So restart the animation explicitly on each navigation. One token per
   navigation means every element animates at most once per nav, which also lets
   rows that arrive late flow in as they land instead of popping.
   Sections still inside a [data-sf-settle] container are skipped: they are held
   at opacity 0 on purpose until the top row is known (sf-home-settle), and
   animating them there would burn the entrance while they are invisible. */
var _finTok=0,_finUntil=0,_finRaf=0,_finCap=0,_finAny=0;
function sfFloatPass(){
_finRaf=0;
/* sf-float-splashgate (2026-09-01). Companion to sf-splash-gate. Gating only
   sfHomeSettle was not enough: it returns early while the splash is up, so it
   never sets [data-sf-settle], and sfFloatPass -- which deliberately skips rows
   inside a [data-sf-settle] container -- stopped skipping them and ran the
   entrance itself as sfFinA, still behind the splash. Measured: the gate moved
   the hidden portion from 96% to 52%, with sfFinA starting at 1757ms while the
   splash was still visible. No entrance of any kind should start before the
   user can see it. */
try{var _fsp=document.querySelector('.splashLogo');
if(_fsp&&_fsp.getClientRects().length)return;}catch(e){}
try{
/* sf-ls-in: the sports page's rows are .sf-ls-section, not .verticalSection,
   so this pass -- the one that animates every NAVIGATION -- never saw them
   and Sports arrived in a single fully-opaque frame. */
/* sf-lib-in (2026-09-04). The admin: every screen should load in like home does.
   Measured before this: only My Stuff animated. Movies, Shows, Music, Folders --
   every library page -- had ZERO frames mid-entrance, because their content is
   not built as rows at all. A library page is one .itemsContainer grid, so
   nothing here ever matched it and it simply appeared.
   The grid animates as ONE element rather than per card: a library can hold
   hundreds of cards, and staggering them would be both a lot of compositor work
   and far too busy to read as premium. One quiet rise for the grid matches what
   a single row does on home. */
/* .jf-fwl-grid  -- the My Stuff sub-views (Watchlist / Bookmarks / Requests)
   .guideVerticalScroller -- the Live TV guide's schedule body
   Neither is a row or an .itemsContainer, so neither was ever animated: measured
   0ms of entrance on all four while every other surface had one. */
/* .sf-lvp-grid -- the Live TV tab's own surface. The admin: "when I switch to live
   tv, the page doesn't smoothly load in like the rest". It didn't: measured
   animationName:none on it, so the tab hard-CUT from home to a page of empty
   card boxes while the artwork filled in behind. Every other surface fades. */
var all=document.querySelectorAll('.verticalSection,.sf-ls-section,.itemsContainer,.jf-fwl-grid,.guideVerticalScroller,.sf-lvp-grid'),vis=[],i;
for(i=0;i<all.length;i++){
if(!all[i].getClientRects().length)continue;
/* A library grid is a LEAF .itemsContainer. The same class is used both as the
   inner track of every ROW and, on the music page, as the tab-content WRAPPER
   that holds the rows -- and animating a wrapper as well as its rows runs the
   entrance twice over the same pixels (measured: 22 frames on Music, with
   .verticalSection rows animating inside an animating .pageTabContent).
   So skip it in both directions: not inside something this pass animates, and
   not containing something it animates either. Whatever is left is a real grid
   with no rows of its own -- Movies, Shows, Folders, Playlists. */
if(all[i].classList.contains('itemsContainer')&&
(all[i].closest('.verticalSection,.sf-ls-section')||all[i].querySelector('.verticalSection,.sf-ls-section')))continue;
/* sf-fin-defer (2026-09-04). If an ANCESTOR is already playing an entrance, let
   it carry this element -- two nested fades multiply, so the child starts dimmer
   and arrives on a different curve from everything else, which is precisely the
   compounding that reads as sloppy.
   The music page is the real case: it has owned its own reveal (sf-mus-in on
   .pageTabContent) since long before this pass covered anything, and its rows
   were fading inside that fade -- measured 26 frames of it. Written as a general
   rule rather than a music special case, because any page that brings in its own
   surface should win over a per-row pass. Bounded to 6 levels: an entrance
   wrapper is always close by, and this runs per candidate on a rAF loop. */
var _an=all[i].parentElement,_ad=0,_askip=false;
while(_an&&_ad<6){
if(_an.nodeType!==1)break;
var _ac=getComputedStyle(_an);
if(_ac.animationName&&_ac.animationName!=='none'&&_ac.animationPlayState!=='paused'){_askip=true;break;}
_an=_an.parentElement;_ad++;
}
if(_askip)continue;
/* sf-hold-gate: .sf-hold is the other way a row is held invisible (see
   sfHomeSettle). Without it here, gating sfHomeSettle alone would simply hand
   the burnt entrance to this pass instead -- the identical mistake the splash
   gate had to be extended to cover. */
if(all[i].closest&&all[i].closest('.homeSectionsContainer[data-sf-settle],.homeSectionsContainer.sf-hold'))continue;
/* sf-hold-prearm (2026-09-04). The mirror image of sf-hold-gate, and it bites on
   a cold load: this pass is driven by requestAnimationFrame, sfHoldRows by the
   400ms tick, so on a fresh document this pass can start the entrance BEFORE the
   hold has been armed at all -- and sfHoldRows then hides the row part-way
   through. Captured on a hard reload:
       t1650 op0.14 vis1 sfFinA [no hold]
       t1684 op0.38 vis1 sfFinA [no hold]
       t1705 op0.48 vis0 sfFinA [HOLD]   <- hold applied mid-animation
       t1800 op0.81 vis0 sfFinA [HOLD]
   The skip above cannot catch it, because at arm time there is no .sf-hold class
   and no [data-sf-settle] to see yet -- the container is simply untouched.
   The first-load entrance belongs to sfHomeSettle, which is properly gated; this
   pass exists for NAVIGATIONS. So wait for the container to have been through its
   hold at least once. __sfHoldDone is stamped by sfHoldRows when it releases, and
   its deadman timer guarantees that happens, so this can never wait forever. */
var _hsC=all[i].closest&&all[i].closest('.homeSectionsContainer');
if(_hsC&&!_hsC.__sfHoldDone)continue;
vis.push(all[i]);
}
/* visual order, not DOM order -- the home rows are placed with CSS `order` */
vis.sort(function(a,b){
var oa=parseFloat(getComputedStyle(a).order)||0,ob=parseFloat(getComputedStyle(b).order)||0;
if(oa!==ob)return oa-ob;
return (a.compareDocumentPosition(b)&4)?-1:1;});
var tok=String(_finTok),fresh=0;
for(i=0;i<vis.length;i++){
vis[i].style.setProperty('--sf-row-i',i<8?i:8);
if(vis[i].getAttribute('data-sf-fin')===tok)continue;
vis[i].setAttribute('data-sf-fin',tok);
/* sf-floatin-altname (2026-08-29). Removing a class, forcing a reflow and
   re-adding it does NOT restart this animation, and that is why Sports <-> Home
   animated only sometimes. A CSS animation restarts when its computed
   animation-NAME changes. Dropping .sf-fin left the element still matching
   .homeSectionsContainer[data-sf-settled] > .verticalSection, which names the
   very same `sfHomeIn` -- so the name never changed and the browser treated it
   as one continuous animation. Traced it directly: every section got stamped on
   each navigation and not one animationstart event fired.
   Alternate between two identical keyframes under DIFFERENT names instead. Both
   differ from `sfHomeIn`, so the first application also changes the name and
   restarts, whatever the element was doing before. No reflow hack needed. */
/* sf-floatin-flip: pick the name from what the element is wearing NOW, not from
   the token's parity. sfFloatArm can fire more than once for a single navigation
   (hashchange, pushState and the signature tick all arm it -- observed 15 then
   17), and two increments leave the parity unchanged, so the same class was
   re-applied, the animation-name never changed and nothing restarted. Measured:
   stamps=20, animationstart=0 on exactly those navigations. Flipping off the
   element's own class guarantees the name changes every time we decide to
   animate it, however many times we were armed. */
if(vis[i].classList.contains('sf-fin-a')){vis[i].classList.remove('sf-fin-a');vis[i].classList.add('sf-fin-b');}
else{vis[i].classList.remove('sf-fin-b');vis[i].classList.add('sf-fin-a');}
fresh++;
}
/* sf-floatin-adaptive: a fixed window was too short for the slow direction.
   Sports -> Home has to rebuild 10 sections / 98 cards and the rows landed
   AFTER the 2600ms window had closed, so that one transition -- the exact one
   the admin reported -- still did not animate, while the fast Home -> Sports did.
   Keep watching for 1.5s past the last row that actually arrived, with a hard
   cap so a page that never stops streaming cannot hold the loop open. */
if(fresh){_finAny=1;_finUntil=Math.min(_finCap,Date.now()+1500);}
}catch(e){}
/* sf-floatin-persist: the adaptive window only extended when it FOUND rows, so
   if a rebuild produced nothing for the first 2600ms the loop died before the
   rows ever arrived -- which is why Sports <-> Home animated on some passes of
   the audit and not others, purely on how fast that rebuild happened to be.
   Stay alive until we have actually animated something, then 1.5s past the last
   arrival, and let the 9s cap end it either way. */
var _alive=Date.now()<_finCap&&(!_finAny||Date.now()<_finUntil);
if(_alive&&!_finRaf)_finRaf=requestAnimationFrame(sfFloatPass);
}
/* sf-floatin-sig: events alone were not reliable. Wrapping pushState fixed the
   common case but Sports -> Home still animated only SOMETIMES -- the same
   transition passed on one pass of the audit and failed on a later one, i.e. a
   race over which navigation API fires and whether it lands before or after the
   rows are rebuilt. Stop guessing at the mechanism and watch the RESULT: poll a
   route signature on the existing tick, and arm whenever it changes. The events
   above stay, because they arm in the same frame and the tick is only a 400ms
   backstop. */
var _finSig='';
function sfFloatSig(){
try{
var p=document.querySelector('.pageTabContent.is-active');
return (location.hash||'')+'|'+(p&&p.id?p.id:'');
}catch(e){return '';}
}
function sfFloatTick(){
if(sfFloatSig()!==_finSig)sfFloatArm();
}
/* sf-floatin-routeguard (2026-08-29). The admin: "everytime i press the 3 dots on a
   media, it makes the rows move."
   sfFloatArm was called from the pushState/replaceState wrapper below on EVERY
   history write, with no check that the route had actually changed. Jellyfin
   10.11 routes through @remix-run/router -- the only bundle here that touches
   pushState -- and an action sheet opens by PUSHING A HISTORY ENTRY so that Back
   closes it (see [[jellyfin-actionsheet-close]]). So tapping the corner menu
   registered as a navigation and every visible row replayed its 20px fade-up,
   then did it again when the sheet closed.
   Arm on the ROUTE, not on the history write. The signature the tick already
   computed is the correct test; make it the single gate for every caller
   (hashchange, popstate, pushState, replaceState and the tick all land here).
   A dialog push leaves both the hash and the active pane untouched, so it no
   longer arms, while a real navigation still animates exactly once. */
function sfFloatArm(){
var _sig=sfFloatSig();
if(_sig===_finSig)return;
_finSig=_sig;
_finTok++;
/* rows stream in after the route changes, so keep watching briefly rather than
   taking a single snapshot the moment the hash changes */
_finUntil=Date.now()+2600;
_finCap=Date.now()+9000;
_finAny=0;
if(!_finRaf)_finRaf=requestAnimationFrame(sfFloatPass);
}
try{window.addEventListener('hashchange',sfFloatArm);}catch(e){}
try{window.addEventListener('popstate',sfFloatArm);}catch(e){}
/* sf-floatin-history: hashchange alone missed the one transition the admin actually
   reported. Home -> Sports fired it, Sports -> Home did not, and it was not a
   timing problem -- a 6.5s measurement window with an adaptive extension still
   showed maxRunning=0. Jellyfin returns to home through history.pushState /
   replaceState, which fire NEITHER hashchange NOR popstate; sfNavSwap wraps them
   for exactly this reason. Same treatment here. */
try{['pushState','replaceState'].forEach(function(k){
var orig=history[k];
if(!orig||orig.__sfFin)return;
var w=function(){var r=orig.apply(history,arguments);try{sfFloatArm();}catch(e){}return r;};
w.__sfFin=1;history[k]=w;
});}catch(e){}
/* sf-route-skel: give every route that currently goes black a contextual
   loading state instead. See the style block for the measured gaps this covers.
   Runs on the FAST tick: the gaps start at ~250ms, so a 400ms sweep would miss
   the front of the very windows this exists to cover. Cost is bounded -- it is a
   regex on the hash until a route is actually loading, one querySelector while
   it is, and a latch that stops all of it once content has landed. */
var RS_HASH='',RS_SINCE=0,RS_ARCH=null,RS_DONE=false;
function rsArch(h){
if(/^#\/details/.test(h))return 'detail';
if(/^#\/livetv/.test(h)){var m=/[?&]tab=(\d+)/.exec(h);return (m&&m[1]==='1')?'guide':'grid';}
if(/^#\/(movies|tv|music|list|videos|photos|livetvchannels)\b/.test(h))return 'grid';
/* home itself has its own machinery (sf-holdrows + sf-skel); only My Stuff,
   which sfHomeSettle deliberately ignores, needs covering here */
/* sf-noskel-mystuff (2026-09-04). The admin: remove "the skeleton that shows up on
   the watchlist page". My Stuff and its sub-views paint quickly enough that the
   placeholder was more noticeable than the wait it covered, so home and every
   one of its surfaces now opt out entirely. */
if(/^#\/home/.test(h))return null;
return null;
}
/* The VISIBLE page only. Jellyfin keeps one cached view per URL in the DOM, so a
   document-wide query happily finds the previous route's cards and concludes
   this route has already rendered -- the same trap sfDetailSkeleton documents. */
function rsVisiblePage(){
var p=document.querySelectorAll('.page'),i;
for(i=0;i<p.length;i++){if(!p[i].classList.contains('hide')&&p[i].getClientRects().length)return p[i];}
return null;
}
function rsHasContent(){
var pg=rsVisiblePage();
if(!pg)return false;                       /* nothing on screen at all */
/* querySelector alone was WRONG and left the skeleton covering live content for
   its full 12s deadline on the Guide, Music and My Stuff. It returns the FIRST
   match, which on those routes is a zero-size node -- measured 230+ matching
   descendants in the visible page, every one of them real, while the first was
   unpainted. Scan until something is actually painted. Capped so this stays
   cheap on the 30ms tick, and it only runs at all during the loading window --
   RS_DONE latches it off the moment content lands. */
/* An empty page is LOADED, not loading. Bookmarks with nothing in it renders
   .jf-fwl-msg ("No bookmarks yet...") and no cards at all, so the old list
   matched nothing and the skeleton sat on top of that message until its 12s
   deadline -- covering the one thing the user needed to read. */
var n=pg.querySelectorAll('.cardBox,.card,.listItem,.programCell,.detailPagePrimaryContainer,.sf-alb-hero,.verticalSection,.sf-ls-section,.jf-fwl-msg,.noItemsMessage,.emptyMessage'),i;
/* STRIDE, not "the first N". My Stuff shares #indexPage with the home tab, so
   the first ~60 matches in DOM order are home's own rows -- present but hidden
   while tab=1 is showing. Checking a prefix therefore found nothing painted and
   left the skeleton up for its full deadline over live content. Sampling the
   whole list at a stride costs the same bounded number of layout reads and
   cannot be defeated by where the hidden nodes happen to sit. */
var step=n.length>120?Math.ceil(n.length/120):1;
for(i=0;i<n.length;i+=step){if(n[i].getClientRects().length)return true;}
return false;
}
function rsCards(n,cls){
var h='',i;
for(i=0;i<n;i++)h+='<div class="sf-rskel-card"><div class="sf-rskel-img sf-skel-sh"></div>'
+'<div class="sf-rskel-tx sf-skel-sh"></div>'+(cls==='grid'?'<div class="sf-rskel-tx2 sf-skel-sh"></div>':'')+'</div>';
return h;
}
function rsHtml(a){
var W=window.innerWidth||1280,i,j,h='';
if(a==='grid'){
/* enough to fill the fold at this width and no more -- a skeleton taller than
   the viewport is invisible work */
var per=Math.max(2,Math.floor((W*0.94)/172)),rows=Math.ceil((window.innerHeight||800)/300)+1;
return '<div class="sf-rskel-hd sf-skel-sh"></div><div class="sf-rskel-grid">'+rsCards(per*rows,'grid')+'</div>';
}
if(a==='rows'){
/* My Stuff's rows are 2:3 posters (Movies / Shows / Albums), not the 16:9 cards
   Continue Watching uses -- the skeleton was the wrong shape for the only
   surface it appears on, so the layout still moved when the real row landed. */
var per=Math.max(2,Math.floor((W*0.94)/(Math.min(W*0.115,165)+18)));
for(i=0;i<2;i++)h+='<div class="sf-rskel-row sf-rskel-poster"><div class="sf-rskel-hd sf-skel-sh"></div>'
+'<div class="sf-rskel-strip">'+rsCards(per,'poster')+'</div></div>';
return h;
}
if(a==='guide'){
/* deliberately uneven programme widths -- an even grid reads as a table, and a
   schedule never is one */
var pat=[[3,2,4],[2,5,2],[4,3,2],[2,2,5],[5,2,2],[3,4,2],[2,3,4],[4,2,3]];
h='<div class="sf-rskel-ruler"><i class="sf-skel-sh"></i><i class="sf-skel-sh"></i>'
+'<i class="sf-skel-sh"></i><i class="sf-skel-sh"></i><i class="sf-skel-sh"></i><i class="sf-skel-sh"></i></div>';
var nrow=Math.max(4,Math.min(12,Math.floor((window.innerHeight||800)/58)));
for(i=0;i<nrow;i++){
h+='<div class="sf-rskel-grow"><div class="sf-rskel-chan sf-skel-sh"></div>';
for(j=0;j<3;j++)h+='<div class="sf-rskel-prog sf-skel-sh" style="flex:'+pat[i%pat.length][j]+' 1 0"></div>';
h+='</div>';
}
return h;
}
/* detail */
return '<div class="sf-rskel-detail"><div class="sf-rskel-logo sf-skel-sh"></div>'
+'<div class="sf-rskel-meta sf-skel-sh"></div>'
+'<div class="sf-rskel-plot sf-skel-sh" style="width:92%"></div>'
+'<div class="sf-rskel-plot sf-skel-sh" style="width:86%"></div>'
+'<div class="sf-rskel-plot sf-skel-sh" style="width:54%"></div>'
+'<div class="sf-rskel-btns"><div class="sf-rskel-btn sf-skel-sh"></div>'
+'<div class="sf-rskel-btn sf-rskel-btn2 sf-skel-sh"></div></div></div>';
}
/* sf-bg-hold: hold the outgoing backdrop until the incoming one has DECODED.
   See the style block for why. Reads .backdropContainer, writes only its own
   layer, so Jellyfin's element is untouched and this cannot fight it. */
var BG_LAST='';
function sfBgHold(){
try{
var bd=document.querySelector('.backdropContainer');
if(!bd)return;
var cs=getComputedStyle(bd),img=cs.backgroundImage||'none';
if(img===BG_LAST)return;
var prev=BG_LAST;BG_LAST=img;
if(!prev||prev==='none')return;                 /* nothing worth holding */
var L=document.getElementById('sf-bgprev');
if(!L){
L=document.createElement('div');
L.id='sf-bgprev';L.className='sf-bgprev';
L.setAttribute('aria-hidden','true');           /* decorative */
/* directly after the element it is standing in for: same stacking context, so
   it covers the backdrop and nothing else, whatever z-index the theme uses */
if(bd.parentNode)bd.parentNode.insertBefore(L,bd.nextSibling);
else return;
}
L.style.backgroundImage=prev;
L.style.backgroundSize=cs.backgroundSize;
L.style.backgroundPosition=cs.backgroundPosition;
L.style.filter=cs.filter;                       /* keep the theme's blur/scrim */
L.classList.remove('sf-bgprev-out');
var done=function(){try{L.classList.add('sf-bgprev-out');}catch(e){}};
var m=/url\(["']?(.*?)["']?\)/.exec(img);
/* No incoming image at all: this is the dark gap. HOLD the old one and return --
   the next real backdrop will release it. */
if(img==='none'||!m)return;
var im=new Image();
im.onload=function(){try{if(im.decode)im.decode().then(done,done);else done();}catch(e){done();}};
im.onerror=done;
im.src=m[1];
/* a backdrop that never loads must not park the previous one forever */
setTimeout(done,2500);
}catch(e){}
}
function sfRouteSkel(){
var h=location.hash||'',de=document.documentElement;
RS_ARCH=rsArch(h);
var el=document.getElementById('sf-rskel');
function clearFlag(){try{de.removeAttribute('data-sf-rskel');}catch(e){}}
function drop(){
if(!el)return;
if(el.classList.contains('sf-rskel-out'))return;   /* already leaving */
el.classList.add('sf-rskel-out');
/* Clear the flag when the skeleton is GONE, not when it starts leaving.
   Clearing it up-front un-suppressed the app spinner for the whole 220ms
   fade-out -- measured 235ms of spinner overlapping a skeleton that was still
   on screen, i.e. exactly the noise this is here to remove. */
var g=el;
setTimeout(function(){try{if(g.parentNode)g.parentNode.removeChild(g);}catch(e){}clearFlag();},220);
}
/* sf-rskel-surface (2026-09-04). The admin: "the watchlist page and bookmark and
   request page show a loading skeleton?" They did, and they should not.
   Keying the reset on the raw hash meant every My Stuff sub-tab -- Favorites ->
   Watchlist -> Bookmarks -> Requests, which only change `&sub=` -- counted as a
   brand new route, so the skeleton was re-armed and thrown over a surface that
   was already fully painted. Key on the SURFACE instead: the archetype plus the
   hash up to the first `&`. A cold load of My Stuff still gets its skeleton;
   moving between its sub-tabs no longer does. Detail pages keep a per-item key,
   since `#/details?id=...` differs before the first `&`. */
var _k=RS_ARCH?(RS_ARCH+'|'+h.split('&')[0]):h.split('&')[0];
if(_k!==RS_HASH){
RS_HASH=_k;RS_SINCE=Date.now();RS_ARCH=rsArch(h);RS_DONE=false;
/* a route change retires the previous skeleton immediately -- fading one route's
   placeholder out over another route's content is worse than no skeleton */
if(el&&el.parentNode){el.parentNode.removeChild(el);el=null;}
clearFlag();
}
if(!RS_ARCH||RS_DONE){if(el)drop();return;}
var age=Date.now()-RS_SINCE;
/* a route that is already warm paints well inside this, and must not be given a
   flash of skeleton it does not need */
if(age<90)return;
/* stalled or genuinely empty (an empty library): show the page, not a lie */
if(age>12000){RS_DONE=true;drop();return;}
if(rsHasContent()){RS_DONE=true;drop();return;}
if(el)return;
el=document.createElement('div');
el.id='sf-rskel';
el.className='sf-rskel';
el.setAttribute('aria-hidden','true');   /* decorative: keep it out of the a11y tree */
el.innerHTML=rsHtml(RS_ARCH);
document.body.appendChild(el);
try{de.setAttribute('data-sf-rskel','1');}catch(e){}
}
function sfHomeSkeleton(){
var el=document.getElementById('sf-skel');
function drop(){if(el&&el.parentNode)el.parentNode.removeChild(el);}
if(!/^#\/home/.test(location.hash||'')){drop();SKEL_UNTIL=0;return;}
/* My Stuff (tab=1) is a different surface with its own rows -- not this shape */
var m=/[?&]tab=(\d+)/.exec(location.hash||'');
if(m&&m[1]!=='0'){drop();return;}
var page=document.querySelector('#indexPage');
if(!page){drop();return;}
var host=page.querySelector('.homeSectionsContainer')||page;
var secs=page.querySelectorAll('.verticalSection'),real=0,i;
for(i=0;i<secs.length;i++)if(secs[i].getClientRects().length)real++;
if(!SKEL_UNTIL)SKEL_UNTIL=Date.now()+15000;
var want=SKEL_TARGET-real;
if(want>SKEL_MAX)want=SKEL_MAX;
if(want<0)want=0;
if(Date.now()>SKEL_UNTIL)want=0;      /* load stalled: show the page, not a lie */
if(!want){drop();return;}
if(el&&el.parentNode!==host)host.appendChild(el);
if(el&&+el.getAttribute('data-n')===want)return;
if(!el){
el=document.createElement('div');
el.id='sf-skel';el.className='sf-skel';
el.setAttribute('aria-hidden','true');   /* decorative: keep it out of the a11y tree */
}
var h='',j,wide;
for(i=0;i<want;i++){
/* the first two home rows are 16:9 (Continue Watching, Next Up); the rest are posters */
wide=(real+i)<2;
h+='<div class="sf-skel-row '+(wide?'sf-skel-wide':'sf-skel-tall')+'">'
+'<div class="sf-skel-hd sf-skel-sh"></div><div class="sf-skel-strip">';
for(j=0;j<SKEL_CARDS;j++)
h+='<div class="sf-skel-card"><div class="sf-skel-img sf-skel-sh"></div>'
+'<div class="sf-skel-tx sf-skel-sh"></div></div>';
h+='</div></div>';
}
el.innerHTML=h;
el.setAttribute('data-n',want);
if(el.parentNode!==host)host.appendChild(el);
}
/* sf-hero-bgrevive: the hero sometimes comes back BLACK after the app has been
   backgrounded on a phone for a while, and never recovers. iOS freezes and can
   discard a backgrounded page; Media Bar's slides come back without their
   images and nothing re-runs its init.

   I could NOT reproduce this in a headless browser -- simulated
   hidden->visible restored the hero fully (9 slides, 8 images) -- so this is a
   MITIGATION, not a verified fix, and it is gated accordingly. An earlier
   attempt used a bare 4-second timer and made things WORSE: the first slide
   does not appear until ~15s on a cold start, so it fired mid-startup and
   showed black on a FRESH open. Every gate below exists to stop that:

     * only after a real hidden -> visible transition (never on a cold start);
     * only if we were hidden at least 45s (a glance at the notification shade
       is not a discard);
     * only on #/home, where the hero lives;
     * only if the container has been around a while AND has no visible slide;
     * at most once every 10 minutes, so it can never loop.

   If any gate is wrong the worst case is that it does nothing, which is the
   behaviour today. */
(function(){
var HID=0,LAST=0,BOOT=Date.now();
function heroBroken(){
var c=document.getElementById('slides-container');
if(!c)return false;
var kids=c.children,i,r,st;
for(i=0;i<kids.length;i++){
r=kids[i].getBoundingClientRect();
st=window.getComputedStyle(kids[i]);
if(r.height>50&&st.display!=='none'&&st.opacity!=='0')return false;  /* something is showing */
}
return true;
}
document.addEventListener('visibilitychange',function(){
if(document.hidden){HID=Date.now();return;}
if(!HID)return;                                   /* never fired without a hide first */
var away=Date.now()-HID;HID=0;
if(away<45000)return;
if(Date.now()-BOOT<60000)return;                  /* not straight after launch */
if(Date.now()-LAST<600000)return;                 /* at most once per 10 min */
if(!/^#\/home/.test(location.hash||''))return;
setTimeout(function(){
if(document.hidden)return;
if(!/^#\/home/.test(location.hash||''))return;
if(!heroBroken())return;                          /* it came back fine -- leave it alone */
LAST=Date.now();
try{console.warn('[sf-hero-bgrevive] hero empty after '+Math.round(away/1000)+'s backgrounded; reloading');}catch(e){}
location.reload();
},4000);                                          /* give it 4s to restore on its own */
});
})();
window.sfTickFails={};
function sfRunGuarded(list){
for(var i=0;i<list.length;i++){
try{list[i]();}
catch(e){
var n=list[i].name||('fn'+i),r=window.sfTickFails[n];
if(!r){r=window.sfTickFails[n]={count:0,message:String((e&&e.message)||e),
stack:String((e&&e.stack)||'').slice(0,400)};
if(window.console&&console.warn)console.warn('[sf-tick] '+n+' threw: '+r.message);}
r.count++;
}
}
}
/* sf-track-endfix (2026-08-24). Seek near the end of a song and the queue stalls:
   measured on Maroon 5 "V", seeking to end-3s produced a SILENT GAP of 21.7s
   between the track ending and the next one starting, with ZERO network activity
   for 21 of those seconds -- then a Stopped report and the next track. Natural
   playback is fine (0.4-0.7s measured twice), so this is specific to seeking: the
   seek swaps the audio source, and the player's own end handling does not fire on
   the new element. The audio element itself sits at ended=true / paused=false the
   whole time, which is the tell -- the END happened, nothing acted on it.
   So: if the element really has ENDED and the player has not moved on after 2.5s,
   press its own next-track control. 2.5s is well past the 0.4-0.7s that a healthy
   advance takes, so a normal transition is never pre-empted.
   Guards, each for a reason:
     - audio only; video has its own next/ended handling
     - never for audiobooks (.sf-np-book): they are single long items and "next"
       would jump to a DIFFERENT BOOK
     - bails the moment currentSrc changes -- that means the player advanced itself
     - requires the real button to be visible, so on the last track of a queue
       (no next) this does nothing */
var SF_END_AT=0,SF_END_SRC='';
function sfTrackEndFix(){
try{
var a=document.querySelector('audio');
if(!a){SF_END_AT=0;return;}
if(document.querySelector('.sf-np-book')){SF_END_AT=0;return;}
var src=a.currentSrc||'';
if(!a.ended){SF_END_AT=0;SF_END_SRC=src;return;}
if(!SF_END_AT){SF_END_AT=Date.now();SF_END_SRC=src;return;}
if(src!==SF_END_SRC){SF_END_AT=0;SF_END_SRC=src;return;}
if(Date.now()-SF_END_AT<2500)return;
SF_END_AT=0;
var b=document.querySelector('.nextTrackButton');
if(b&&b.offsetParent!==null){
try{console.warn('sf-track-endfix: track ended but queue stalled; advancing');}catch(e){}
b.click();
}
}catch(e){}
}
/* sf-inline-lyr: make the TRACK PAGE's own lyrics follow the song.

   Jellyfin renders #lyricsSection as a flat TEXT BLOB -- measured on Grenade,
   49 bare text nodes separated by <br>, with no per-line element anywhere. So
   there was physically nothing to highlight and it sat completely static while
   the track played (verified: the same text, unchanged, across 30s of
   playback). This is the most discoverable lyrics surface -- it is on the page,
   no button to find -- so "the lyrics do not line up" is most likely THIS, not
   the overlay, whose sync measured exact (16/16 on CHIHIRO, 15/16 on Grenade).

   The rows are rebuilt from the LYRICS DATA, never from the DOM text. Grenade
   has 51 lyric lines but only 49 non-empty text nodes -- blank lines collapse --
   so wrapping what is on screen would shift every index after the first gap and
   highlight the wrong line. Building from the data keeps the mapping 1:1.

   Only takes over for SYNCED lyrics; a plain-text track (about 8% of this
   library, and lrclib genuinely has no timed version for them) is left exactly
   as Jellyfin drew it. The page is never auto-scrolled: you are reading it, and
   stealing the scroll position out from under a reader is worse than a line
   drifting off screen. */
var sfIL={id:null,lines:null,busy:false};
function sfILPlayingId(){
var a=document.querySelector('audio');if(!a)return null;
var m=(a.currentSrc||'').match(/\/Audio\/([0-9a-f]{32})\//i);return m?m[1]:null;
}
function sfILPageId(){
var m=(location.hash||'').match(/[?&]id=([0-9a-f]{32})/i);return m?m[1]:null;
}
/* Jellyfin caches ONE view per URL, so several #lyricsSection nodes coexist and
   document.querySelector() returns the first -- which is usually a HIDDEN page
   you navigated away from. Measured: after Grenade -> CHIHIRO, querySelector
   returned the hidden Grenade section (51 rebuilt rows) while the visible
   CHIHIRO one was never touched. Always resolve the VISIBLE instance. */
function sfILCont(){
var secs=document.querySelectorAll('#lyricsSection'),i,c;
for(i=0;i<secs.length;i++){
if(secs[i].offsetParent===null)continue;
c=secs[i].querySelector('.lyricsLineContainer');
if(c)return c;
}
return null;
}
function sfInlineLyr(){
var cont=sfILCont();
if(!cont)return;
var pid=sfILPageId(),tid=sfILPlayingId();
/* Follow only when the page being LOOKED at is the track being PLAYED, or the
   highlight would crawl down some other song's lyrics. */
if(!pid||!tid||pid!==tid){
var off=cont.querySelectorAll('p.sf-il.sf-il-on'),z;
for(z=0;z<off.length;z++)off[z].classList.remove('sf-il-on');
return;
}
if(sfIL.id!==tid){
if(sfIL.busy)return;
sfIL.busy=true;sfIL.id=tid;sfIL.lines=null;
var ac=window.ApiClient;if(!ac){sfIL.busy=false;sfIL.id=null;return;}
ac.getJSON(ac.getUrl('Audio/'+tid+'/Lyrics')).then(function(j){
sfIL.busy=false;
if(sfIL.id!==tid)return;
var L=(j&&j.Lyrics)||[];
sfIL.lines=(L.length&&L[0].Start!=null)?L:null;
}).catch(function(){sfIL.busy=false;sfIL.lines=null;});
return;
}
if(!sfIL.lines)return;
if(cont.getAttribute('data-sf-il')!==tid){
var frag=document.createDocumentFragment(),i,p,t;
for(i=0;i<sfIL.lines.length;i++){
p=document.createElement('p');
t=sfIL.lines[i].Text||'';
p.className=t.trim()?'sf-il':'sf-il sf-il-blank';
p.textContent=t;
frag.appendChild(p);
}
cont.innerHTML='';
cont.appendChild(frag);
cont.setAttribute('data-sf-il',tid);
}
var a=document.querySelector('audio');if(!a)return;
var ticks=a.currentTime*10000000,idx=-1,k;
for(k=0;k<sfIL.lines.length;k++){if(sfIL.lines[k].Start<=ticks)idx=k;else break;}
var rows=cont.querySelectorAll('p.sf-il');
if(idx<0||!rows.length||!rows[idx])return;
if(rows[idx].classList.contains('sf-il-on'))return;
for(k=0;k<rows.length;k++)rows[k].classList.remove('sf-il-on');
rows[idx].classList.add('sf-il-on');
}
var SF_TICK=[sfHeroRemember,sfTrackEndFix,sfDetailSkeleton,sfLeavingRow,sfCardPos,sfHideInternalPl,sfHomeTapPlay,sfCardMenus,sfHoldRows,sfHomeSettle,sfPlotOrder,sfHomeSkeleton,sfHeroSkeleton,sfSportsExit,sfPillShow,sfPillFit,sfMusicRowPlay,sfDedupeRows,sfNavTuck,sfMusicLanding,sfHideEmptySections,sfNowPlayingKind,sfNpFav,sfLyrOne,sfCapsuleGroup,sfCapsuleProgress,sfProgressPaint,sfCapsuleSeek,sfCapsuleWire,sfCapsuleButtons,sfPlayingRow,sfLyricsTick,sfFlyrTick,sfPageBg,sfHeroNoPort,sfHeroImg,sfHeroWheel,sfRowTitles,sfRowArrows,sfNavSwap,sfSubLift,sfDetailHero,sfDetailBadges,sfDetailFacts,sfSeriesEpisodes,sfOverviewMore,sfInfoBtn,sfEpisodeLine,sfScrollHint,sfMusicBtn,sfHdrVar,sfCapReveal,sfPlaylistNew,sfPlaylistRow,sfMusicTabs,sfMusLibPills,sfMusPages,sfMusicHome,sfMusicFeature,sfMusAmbient,sfMusDedupe,sfMixRow,sfMusicSolo,sfNpTick,sfMusReveal,sfMusicRow,sfAudiobookRow,sfAbLibrary,sfCwBooks,sfLiveTvRow,sfDrawerScroll,sfHeroPlayFix,sfHeroWatch,sfHeroPrefill,sfHeroResume,sfHeroLogo,sfSeerrLinks,sfMyList,sfCwBarPos,sfHideCW,sfSheetWl,sfMusicPad,sfHomeTabRepair,sfTabSettle,sfDrawerOrder,sfTitleDup,sfOwnedAlbums,sfInlineLyr];
setInterval(function(){sfRunGuarded(SF_TICK);},400);
/* the settle check also runs fast so the bar is revealed the moment it is ready
   rather than up to 400ms later */
/* alias on the fast timer as well as hashchange: our own sub-pill sync writes
   #/livetv?tab=N when Guide/Channels are clicked, and rewriting it on the 400ms
   sweep would show a visible flicker of the un-aliased URL. */
/* sf-home-fast (2026-09-01). The admin: the first view must load in smoothly and
   progressively. sfHomeSettle was ONLY on the 400ms SF_TICK, so Jellyfin could
   paint Continue Watching and the hold ([data-sf-settle] -> opacity:0) arrived
   up to 400ms later -- the row was visible, then snapped out, then animated.
   That snap is the flash. The header never did this because sfHdrReady and
   sfHdrOrder are on the 30ms SF_FAST tick, and sfTabSettle is deliberately on
   BOTH lists for exactly this reason. Give sfHomeSettle the same treatment.
   Cost is bounded: sfHomeSettle returns immediately when the route is not
   home, and again once data-sf-settled is set, so after the first view has
   landed it is a hash test plus one querySelector. */
var SF_FAST=[sfXfade,sfDetRoute,sfDetailMeta,sfRouteSkel,sfBgHold,sfFloatTick,sfRateGuard,sfSpinTick,sfOptiTick,sfMainNav,sfLtvAlias,sfTabSettle,sfHdrReady,sfHdrOrder,sfPillShow,sfMusicSoloClass,sfPillDedupe,sfLtvSubDupe,sfHomeBarUnify];
setInterval(function(){sfRunGuarded(SF_FAST);},30);
sfAddMusicButton();
})();</script>'''

LIVESPORTS_SCRIPT = _LS_01 + _LS_02 + _LS_03 + _LS_04 + _LS_05 + _LS_06 + _LS_07 + _LS_08 + _LS_09 + _LS_10 + _LS_11 + _LS_12 + _LS_13 + _LS_14 + _LS_15 + _LS_16
