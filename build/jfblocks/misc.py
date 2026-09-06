"""jfblocks/misc.py -- payload constants lifted out of jf_patch.py.

Each constant's source text (and its comments) is byte-identical to the
monolith; only its location changed. 96 constants.
"""

__all__ = [
    'ENDSAT_MARKER',
    'ENDSAT_SCRIPT',
    'SUBLIFT_MARKER',
    'SUBLIFT_STYLE',
    'SUBABYSS_MARKER',
    'SUBABYSS_STYLE',
    'SEAMLESS_MARKER',
    'SEAMLESS_SCRIPT',
    'JEOFF_MARKER',
    'JEOFF_SCRIPT',
    'ONEREND_MARKER',
    'ONEREND_SCRIPT',
    'SFUICONS_MARKER',
    'SFUICONS_STYLE',
    'ICONGUARD_MARKER',
    'ICONGUARD_STYLE',
    'NOLAZY_MARKER',
    'NOLAZY_SCRIPT',
    'NOLAZY_TOUCHSCROLL_MARKER',
    'TOUCHSCROLL_SCRIPT',
    'ATVBOOT_MARKER',
    'ATVBOOT_STYLE',
    'SLIDESEMPTY_MARKER',
    'SLIDESEMPTY_STYLE',
    'HDRSCRIM_MARKER',
    'HDRSCRIM_STYLE',
    'PAUSEREP_MARKER',
    'PAUSEREP_SCRIPT',
    'VOLPOP_MARKER',
    'VOLPOP_STYLE',
    'JEHELP_MARKER',
    'JEHELP_SCRIPT',
    'BTNSETTLE_MARKER',
    'BTNSETTLE_SCRIPT',
    'PAGESDEDUPE_MARKER',
    'PAGESDEDUPE_SCRIPT',
    'BMITEMID_MARKER',
    'BMITEMID_SCRIPT',
    'MYSTUFF_MARKER',
    'MYSTUFF_SCRIPT',
    'ABCUT_MARKER',
    'ABCUT_STYLE',
    'AVPICKER_MARKER',
    'AVPICKER_STYLE',
    'AVPICKER_SCRIPT',
    'MOBILEPLAYER_MARKER',
    'MOBILEPLAYER_STYLE',
    'NOCOLLAPSE_MARKER',
    'NOCOLLAPSE_SCRIPT',
    'SCROLLFIX_MARKER',
    'SCROLLFIX_SCRIPT',
    'DEDUPEPAGING_MARKER',
    'DEDUPEPAGING_SCRIPT',
    'CRASHRECOVERY_MARKER',
    'CRASHRECOVERY_SCRIPT',
    'MBCSS_MARKER',
    'MBCSS_LINK',
    'ITEMCACHE_MARKER',
    'ITEMCACHE_SCRIPT',
    'BMFIX_MARKER',
    'BMFIX_STYLE',
    'TYPINGGUARD_MARKER',
    'TYPINGGUARD_SCRIPT',
    'BRAND',
    'ABSTAGE_MARKER',
    'ABSTAGE_STYLE',
    'SHELF_MARKER',
    'SHELF_STYLE',
    'TAPFEEL_MARKER',
    'TAPFEEL_STYLE',
    'DISCBADGE_MARKER',
    'DISCBADGE_STYLE',
    'SRCCAP_MARKER',
    'SRCCAP_SCRIPT',
    'COALESCE_MARKER',
    'COALESCE_SCRIPT',
    'SF_BUILD',
    'FRESH_MARKER',
    'FRESH_SCRIPT',
    'FRESH_CHECK',
    'SWIPEGUARD_SCRIPT',
    'ABCARD_MARKER',
    'ABCARD_SCRIPT',
    'RETIRED',
    'DIAG_MARKER',
    'DIAG_SCRIPT',
    'HDRSOLID_MARKER',
    'HDRSOLID_SCRIPT',
    'VIEWSCOPE_MARKER',
    'VIEWSCOPE_SCRIPT',
    'MEDIASESSION_MARKER',
    'MEDIASESSION_SCRIPT',
]


ENDSAT_MARKER = 'jf-endsat-12h'
ENDSAT_SCRIPT = (
    '<script>(function(){ /* jf-endsat-12h */'
    'function fix(){'
    'document.querySelectorAll(".runTime").forEach(function(el){'
    'var t=el.innerText;'
    'if(/AM|PM/i.test(t))return;'
    'var m=t.match(/^(.*?)(\\d{1,2}):(\\d{2})\\s*$/);'
    'if(!m)return;'
    'var h=parseInt(m[2],10);'
    'if(isNaN(h)||h>23)return;'
    'var ap=h>=12?" PM":" AM";'
    'var h12=h%12;if(h12===0)h12=12;'
    'el.innerText=m[1]+h12+":"+m[3]+ap;'
    '});'
    '}'
    'var mo=new MutationObserver(fix);'
    'mo.observe(document.body,{childList:true,subtree:true});'
    'setInterval(fix,2000);fix();'
    '})();</script>'
)

# --- Subtitle lift: the video control bar (.videoOsdBottom, ~14vh tall) pops up over
# the subtitles when the mouse moves, hiding them. Jellyfin drops body.mouseIdle when
# the controls are visible; ASS/SSA subs render on canvas.libassjs-canvas (JASSUB). So
# while the OSD is showing, shift that canvas up ~14vh (the control-bar height) so the
# subtitles sit just above the bar; they drop back when the controls hide.
SUBLIFT_MARKER = 'sf-sub-lift'
SUBLIFT_STYLE = ('<style id="sf-sub-lift">'
                 # sf-sub-lift-measured (2026-08-28). The lift used to be a fixed
                 # 17vh (text) / 14vh (ASS). vh is the wrong unit for it: the
                 # control bar is roughly constant in PIXELS, so as a share of the
                 # viewport it shrinks as the screen grows. Measured with the real
                 # CSS in Playwright, the controls occupy 13.4vh at 720p but only
                 # 8.9vh at 1080p -- so one vh number cannot fit both, and at 1080p
                 # 17vh cleared the bar by 114px when ~20px is what looks right.
                 # That overshoot is the "jumps too high" complaint.
                 # sfSubLift() now measures the gap at runtime and publishes it as
                 # --sf-sub-lift in px; this is the fallback for the first frame.
                 'canvas.libassjs-canvas{transition:transform .2s ease;}'
                 'body:not(.mouseIdle) canvas.libassjs-canvas'
                 '{transform:translateY(calc(-1 * var(--sf-sub-lift,9vh)))!important;}'
                 # Primary keeps its baseline pinned to the container's bottom.
                 '.videoSubtitlesInner{margin-bottom:0!important;}'
                 # SECONDARY (dual subtitles). jellyfin-web appendChild()s the
                 # secondary track whenever verticalPosition >= 0 (ours is 85), so
                 # it became the LAST flex child -- and with justify-content:flex-end
                 # that handed the translation the prime bottom slot and shoved the
                 # PRIMARY up by its height. Turning on a second track visibly moved
                 # the main subtitle. order:-1 puts the translation ABOVE instead, so
                 # the primary's baseline is now identical whether or not a secondary
                 # is on (measured: primary bottom 1053 rest / 962 lifted, both cases).
                 # Slightly smaller and slightly dimmer marks it as subordinate,
                 # which is the usual treatment for a translation track.
                 # Selector is two classes deep so it outranks the one-class
                 # font-size rule in sf-sub-abyss regardless of block order.
                 '.videoSubtitles .videoSecondarySubtitlesInner{order:-1!important;'
                 'margin-top:0!important;margin-bottom:.45em!important;'
                 'font-size:.82em!important;opacity:.92!important;}'
                 '.videoSubtitlesInner,.videoSecondarySubtitlesInner'
                 '{transition:transform .2s ease;}'
                 'body:not(.mouseIdle) .videoSubtitlesInner,'
                 'body:not(.mouseIdle) .videoSecondarySubtitlesInner'
                 '{transform:translateY(calc(-1 * var(--sf-sub-lift,9vh)))!important;}'
                 '</style>')

SUBABYSS_MARKER = 'sf-sub-abyss'
# Uniform Abyss subtitle appearance (2026-08-26).
# Measured across the library: SRT/text 74%, PGS+DVD image 18%, ASS/SSA 8%.
# Only ONE of the four render paths draws a background --
#   .videoSubtitlesInner  -> jellyfin-web ships background-color:rgba(0,0,0,.8)  <-- the black box
#   ::cue (native)        -> background-color:transparent
#   ASS via libass canvas -> sampled 8/8 files BorderStyle=1 (outline+shadow, no box)
#   PGS/DVD               -> bitmap, appearance baked into the pixels
# CSS cannot reach the libass canvas or the bitmaps, so a tinted panel could only ever
# cover 74% and would leave the other 26% mismatched. Going boxless matches what the
# other three paths ALREADY do, which is the only way to be uniform across everything.
# JE writes font-size (Inner) and position (.videoSubtitles) inline !important but never
# background/color/text-shadow, so these rules land without disabling JE -- the size
# tuning that matches ASS is preserved.
SUBABYSS_STYLE = ('<style id="sf-sub-abyss">'
                  # /* sf-sub-abyss-pos */ JE positioned the OUTER element as well as
                  # styling it (position:absolute, top:<subtitleVerticalPosition>%,
                  # left:50%, translate(-50%,-50%)). Gating JE off therefore dropped subs
                  # back to jellyfin-web's own `.videoSubtitles{position:fixed;bottom:0}`,
                  # which puts them UNDER the control bar -- verified by screenshot.
                  # Reproduce JE's geometry exactly (85% was the live value) so the
                  # resting position is unchanged for everyone.
                  # NB the transform goes on the OUTER here, matching JE; sf-sub-lift
                  # deliberately transforms the INNER, so the two still compose.
                  '.videoSubtitles{position:absolute!important;top:85%!important;'
                  'bottom:auto!important;left:50%!important;right:auto!important;'
                  'transform:translate(-50%,-50%)!important;text-align:center!important;'
                  # /* sf-sub-wrap 2026-08-27 */ WIDTH. jellyfin-web ships
                  # `.videoSubtitles{left:0;right:0}` (full width) but sf-sub-abyss-pos
                  # replaced that with `left:50%;right:auto` to reproduce JE's centring.
                  # An absolutely-positioned box with left:50%/right:auto/width:auto is
                  # SHRINK-TO-FIT against the space that remains -- i.e. 50% of the frame
                  # -- and jellyfin-web's own `.videoSubtitlesInner{max-width:70%}` then
                  # applies to THAT, so text wrapped at ~35% of frame width (~23 chars a
                  # line at 3vw). Give the outer an explicit width so left:50% stops
                  # capping it; the real wrap limit now lives on the inner, in ch.
                  'width:92vw!important;max-width:92vw!important;'
                  # /* sf-sub-wrap */ HEIGHT + flex-end. sf-sub-abyss-pos CENTRE-anchors
                  # (top:85% with translateY(-50%)), so the box grows in BOTH directions
                  # and a cue that wraps to 2 lines drops ~half a line lower than a
                  # 1-liner -- the text visibly moves as the wrap changes. A fixed-height
                  # box with its content bottom-aligned pins the last line to one
                  # baseline no matter how many lines there are, WITHOUT changing the
                  # anchor model (so this still composes with JE's inline transform if
                  # sf-sub-je-off ever fails to land). Bottom edge = 85% + 25vh/2 = 97.5vh.
                  'height:25vh!important;justify-content:flex-end!important;'
                  # The box is now large and sits over the video. It has never been
                  # interactive, and at this size it would start swallowing taps meant
                  # for play/pause.
                  'pointer-events:none!important;}'
                  '.videoSubtitlesInner,.videoSecondarySubtitlesInner{'
                  'background-color:transparent!important;'
                  'background:none!important;'
                  'color:rgb(245,245,247)!important;'
                  'font-weight:600!important;'
                  # JE supplied the size (3vw 'Gigantic', tuned to match ASS). With JE's
                  # styling gated off we must supply it, or Jellyfin's own 170% rule
                  # renders SRT at ~25px against ASS's ~58px.
                  'font-size:clamp(16px,2.2vw,46px)!important;'
                  # /* sf-sub-wrap */ Wrap width in ch, not %, so characters-per-line
                  # stays constant if the size is ever retuned. 38ch is ~42 rendered
                  # characters. Measured at 1920x1080: 38ch still broke a typical 52-char cue
                  # onto two lines; 44ch+ keeps it on one, which is the change that is
                  # actually visible. Genuinely long cues (80c+) still wrap, as they
                  # should. The 90% cap keeps it
                  # inside the frame on narrow viewports.
                  'max-width:min(48ch,90%)!important;'
                  'line-height:1.3!important;'
                  'padding:0!important;'
                  'text-shadow:0 0 .12em rgba(4,7,16,.95),0 0 .30em rgba(4,7,16,.78),.05em .05em .08em rgba(0,0,0,.95)!important;'
                  '}'
                  # native TextTrack path (subtitleStyling: Auto, per-device) -- same look
                  '::cue{'
                  'background-color:transparent!important;'
                  'color:rgb(245,245,247)!important;'
                  'font-weight:600;'
                  'text-shadow:0 0 .12em rgba(4,7,16,.95),0 0 .30em rgba(4,7,16,.78),.05em .05em .08em rgba(0,0,0,.95);'
                  '}'
                  '</style>')

SEAMLESS_MARKER = 'sf-sub-seamless'
# Seamless subtitle switching (2026-08-27).
# the admin: "it pisses me off when i click subtitles and it makes the entire media
# have to reload".
#
# It is not inherent. playbackManager.setSubtitleStreamIndex only restarts the
# stream (changeStream, i.e. a new PlaySession = the reload) when the TARGET
# subtitle's DeliveryMethod is not External:
#     External, or Embed on a non-transcoding session -> set in place, no reload
#     Encode (burn-in) / Embed while transcoding      -> changeStream
# The server picks that method from the SubtitleProfiles the client declares.
# jellyfin-web builds them like this:
#     var je = appSettings.get('subtitleburnin');
#     var Te = 'true' === appSettings.get('subtitlerenderpgs');
#     'all' !== je && ( push vtt External,
#                       (je === 'allcomplexformats') || push ass + ssa External,
#                       ... Te && je not in (allcomplexformats, onlyimageformats)
#                           && push pgssub External )
# so PGS is only ever offered as External when subtitlerenderpgs is on -- and it
# is compared with "true" ===, i.e. OFF by default. libpgs ships in this build
# (node_modules.libpgs.*.chunk.js, referenced by htmlVideoPlayer-plugin), so the
# client can render PGS itself; nothing but the flag was stopping it.
#
# Proven against the real server with /Items/{id}/PlaybackInfo on 17 Again
# (PGSSUB + SUBRIP), same item, only SubtitleProfiles differing:
#     web default            PGSSUB -> Encode    (no DeliveryUrl)
#     + pgssub External      PGSSUB -> External  (DeliveryUrl present)
# subrip was already External in both, which is why SRT titles never reloaded and
# Blu-ray remuxes always did. Burn-in also forces a VIDEO transcode, so this is a
# CPU saving on the N100 as well as a UX fix.
#
# Library split (MediaStreamInfos, StreamType=2): subrip 19564, PGSSUB 2280,
# ass 1860, DVDSUB 835. This fixes PGS. DVDSUB still burns in -- libpgs decodes
# PGS only, and declaring dvdsub External would hand the client a URL it cannot
# render, which is worse than a reload. That 3% is a known remaining case.
#
# appSettings keys are the BARE names here: getKey is
# `function f(e,t){return t&&(e=t+"-"+e),e}` and the subtitle settings page calls
# set('subtitlerenderpgs', v) with no userId. Verified, not assumed.
#
# These are per-DEVICE localStorage values with a real UI at
# Settings -> Subtitles ("Render PGS subtitles" / "Burn subtitles"), so asserting
# them here is what makes the fix reach every device and every family member
# instead of one browser. Same approach as sf-sub-je-off. Anyone who genuinely
# wants burn-in can have this block dropped.
SEAMLESS_SCRIPT = ('<script>(function(){/* sf-sub-seamless */'
                   'try{'
                   "if(localStorage.getItem('subtitlerenderpgs')!=='true')"
                   "localStorage.setItem('subtitlerenderpgs','true');"
                   # 'all' kills External for EVERY format, including srt.
                   "var b=localStorage.getItem('subtitleburnin');"
                   "if(b==='all'||b==='allcomplexformats'||b==='onlyimageformats')"
                   "localStorage.setItem('subtitleburnin','');"
                   "if(localStorage.getItem('alwaysBurnInSubtitleWhenTranscoding')==='true')"
                   "localStorage.setItem('alwaysBurnInSubtitleWhenTranscoding','false');"
                   '}catch(e){}'
                   '})();</script>')


JEOFF_MARKER = 'sf-sub-je-off'
# Jellyfin Enhanced writes subtitle appearance as INLINE !important styles, which
# outrank any stylesheet -- so sf-sub-abyss is inert while JE styling is live.
# JE ships style PRESETS whose bgColor differs (transparent / #000000FF / #000000B2 ...)
# and the choice is PER USER, which is why some people saw a black box and others none.
# The server-side plugin flag DisableCustomSubtitleStyles did NOT stop it (verified live:
# the inline style was still written with the flag set true). The real gate is the
# CLIENT value JE.currentSettings.disableCustomSubtitleStyles, checked at subtitles.js
# lines 135/213/242 -- when true JE returns early and removeProperty()s what it set.
# Assert it on every page load: it need not persist, because this re-applies each time.
# Bounded to 60s of 100ms ticks (never an unbounded timer -- see the tick-isolation rule)
# and fully try/caught so a JE change can never take the page down with it.
JEOFF_SCRIPT = ('<script>(function(){/* sf-sub-je-off */'
                'var n=0;var t=setInterval(function(){n++;'
                'try{if(window.JE&&JE.currentSettings){'
                'JE.currentSettings.disableCustomSubtitleStyles=true;}}catch(e){}'
                'if(n>600){clearInterval(t);}'
                '},100);})();</script>')

ONEREND_MARKER = 'sf-sub-one-renderer'
# jellyfin-web has TWO text-subtitle renderers and the choice is stored PER DEVICE in
# localStorage (<userId>-localplayersubtitleappearance3 .subtitleStyling):
#   Auto/Native -> browser TextTracks, styled only via ::cue, browser-sized
#   Custom      -> jellyfin parses the cues into .videoSubtitles > .videoSubtitlesInner
# Both are themed by sf-sub-abyss, but they do not render at the SAME SIZE (measured:
# Custom 57.6px vs native materially smaller), so two people could still differ.
# Pin every web client to the DOM renderer so one code path -- and one look -- applies.
# Other fields in the blob are preserved; only subtitleStyling is touched.
# NOTE: this reaches Jellyfin WEB only. The Android TV / iOS / Android apps do their own
# subtitle rendering and are not affected by any of this CSS.
ONEREND_SCRIPT = ('<script>(function(){/* sf-sub-one-renderer */'
                  'var n=0;var t=setInterval(function(){n++;try{'
                  'var u=(window.ApiClient&&ApiClient._currentUser)?ApiClient._currentUser.Id:null;'
                  'if(u){var k=u+"-localplayersubtitleappearance3";var o={};'
                  'try{o=JSON.parse(localStorage.getItem(k)||"{}")||{};}catch(e){o={};}'
                  'if(o.subtitleStyling!=="Custom"){o.subtitleStyling="Custom";'
                  'localStorage.setItem(k,JSON.stringify(o));}'
                  'clearInterval(t);}}catch(e){}'
                  'if(n>600){clearInterval(t);}},100);})();</script>')

SFUICONS_MARKER = 'sf-ui-consistency'
# Measured on the live page before changing anything:
#   hero button bottom 496 vs Continue Watching top 500  -> a 4px gap at 1280x800
#   section <h2> margin-bottom 4.46px                    -> title sits 4px off its cards
#   .emby-scroller overflow-x: hidden                    -> scrollWidth 1859 > clientWidth
#     1586, i.e. 273px of the row unreachable by trackpad/wheel; only the arrows moved it.
# The hero lives ABOVE .sections.homeSectionsContainer and that container's first child is a
# zero-height placeholder, so :first-child cannot be targeted -- pad the container instead.
# overflow-y stays hidden so rows never grow a vertical scrollbar, and the scrollbar itself is
# hidden so the look is unchanged; the arrows keep working because they set scrollLeft.
SFUICONS_STYLE = ('<style id="sf-ui-consistency">'
                  '.sections.homeSectionsContainer{padding-top:34px;}'
                  # /* sf-ml-hover */ Hover was inconsistent row to row: the NATIVE rows
                  # carry .card-hoverable and fade in Jellyfin's .cardOverlayContainer,
                  # while our own rows (.sf-ml-card -- Watchlist, Live TV, Audiobooks,
                  # Music) build .sf-ml-ov instead, which sfAddCardOverlay deliberately
                  # leaves background:transparent (the artwork itself is the play target;
                  # the centre FAB was removed on purpose). So five rows reacted to the
                  # pointer and four did nothing.
                  # Give ours a hover-only scrim so every row responds, rather than
                  # stripping the native overlay and taking away its buttons. Hover-only
                  # matters: a PERMANENT scrim is what once made these rows look darkened.
                  # !important because .sf-ml-ov's transparent background is set inline.
                  # .sf-ml-ov is the WRONG target: measured opacity 0, and it is an empty layer --
                  # the round dot-menu is a sibling (.sf-ml-br), not a child -- so anything
                  # painted on it is invisible. Dim the poster instead, which is the element
                  # that actually carries the artwork.
                  # /* sf-hero-rhythm */ Hero spacing, done statically because every JS attempt jittered.
                  # Measured gaps on a continue slide: 12 / 9 / 10 / **44** / 15 -- the
                  # description sat 44px below the progress bar and the button 59px below the
                  # description, where a Play slide has 15.
                  # The description is clamped to a FIXED height first: without that the
                  # button's gap would still vary with the line count (2 lines vs 3), which is
                  # what made a single static offset impossible before.
                  # Continue slides are selected by :has(.sf-hero-ep) -- that episode line is
                  # exactly what pushes their stack down; Play slides are already correct
                  # (measured 15/15) and are deliberately left alone.
                  # The offsets are POSITIVE: clamping .plot to a fixed height already
                  # pulls the stack up past the target, so these push it back down to a
                  # 12px gap under the progress bar and 15px under the description.
                  # The button needs NO offset of its own: it shares the plot's containing
                  # block, so the +12 on .plot-container already carries it along. Measured
                  # 474 with +44 and 430 (correct) with 0.
                  # sf-hero-plot4 (2026-08-30): 4 lines, not 3. The server-side
                  # MediaBar WebConfig was also cutting the text to 200 characters
                  # before it ever reached the page (raised to 400), so the two limits
                  # had to move together -- more text with a 3-line box shows nothing
                  # new, and a 4-line box with a 200-char cut has nothing to put in it.
                  '#slides-container .slide .plot{display:-webkit-box;-webkit-line-clamp:4;'
                  '-webkit-box-orient:vertical;overflow:hidden;height:80px!important;}'
                  '#slides-container .slide:has(.sf-hero-ep) .plot-container'
                  '{margin-top:15px!important;}'
                  # The button takes NO offset: measured, it DOES follow .plot-container, so a
                  # matching +3 overshot and gave 18px where Play slides have 15.
                  '#slides-container .slide:has(.sf-hero-ep) .button-container'
                  '{margin-top:0!important;}'
                  # /* sf-cardmenu-dup */ On a HOVER layout the card ends up with TWO menu buttons.
                  # Jellyfin's own overlay already carries one -- measured on a Continue
                  # Watching card: cardOverlayButton[data-action=menu], more_vert, 39x39 at
                  # right 1 / bottom 31 -- and sf-cardmenu adds another, more_vert, 32x32 at
                  # right 6 / bottom 26. Same icon, same action, offset 5px in both axes and a
                  # different size, so on hover they read as one control drawn twice slightly
                  # out of line.
                  # sf-cardmenu must STAY for touch (jellyfin renders no overlay buttons there
                  # at all -- that is why it exists), and it must stay at REST on desktop so
                  # cards keep their dot. So hand over only while hovering, and only on cards
                  # that actually have a native menu button to hand over TO -- some rows
                  # (Discover) carry just a play button, and blanking ours there would leave no
                  # menu at all.
                  # No :hover in the selector: jellyfin's overlay menu button measured
                  # opacity 1 at REST as well as on hover, so the two dots are doubled the
                  # whole time, not just while pointing at the card. (:has() + :hover also did
                  # not apply here even though :has() alone matched.)
                  '@media (hover:hover){'
                  '.card:has(.cardOverlayButton[data-action="menu"]) .sf-cardmenu'
                  '{display:none!important;}'
                  # Jellyfin's own overlay dot is a bare white glyph with no backdrop -- on
                  # bright artwork it is nearly invisible (measured colour
                  # rgba(255,255,255,.76) straight over the poster). Ours carried a dark
                  # circular scrim, so handing over to Jellyfin's would have LOST that.
                  # Give it the same treatment the injected dots use, so one control looks
                  # the same wherever it appears. Native size (39px) is kept -- it sits in a
                  # row with the played/favourite buttons and must line up with them.
                  '.card .cardOverlayButton[data-action="menu"]{'
                  'background:rgba(12,12,14,.72)!important;border-radius:50%!important;'
                  '-webkit-backdrop-filter:blur(6px);backdrop-filter:blur(6px);}'
                  '}'
                  # NO hover effect on .sf-ml-card. A brightness(.72) dim was added here to make the
                    # custom rows 'respond' like the native ones -- that was wrong. Jellyfin's
                    # native rows do NOT animate on hover at all: their overlay buttons measure
                    # opacity 1 permanently, so nothing fades in or moves. The dim therefore made
                    # Watchlist / Live TV / Music / Audiobooks the only rows that animated -- the
                    # exact inconsistency it was meant to remove.
                    ''
                  '@media (hover:hover){'
                  ''
                  '}'
                  # /* sf-ml-nohover */ Our own rows (Watchlist / Live TV / Music / Audiobooks) were the
                    # ONLY ones that animated on hover: the poster lifted and its controls faded
                    # in. Jellyfin's native rows do neither -- their overlay buttons measure
                    # opacity 1 permanently, so nothing moves or appears.
                    # The lift was removed from branding.xml; this kills the remaining fade by
                    # making the controls permanently visible, which is what the native rows do.
                    # !important because branding.xml's CustomCss loads AFTER these inline styles.
                    '@media (hover:hover){'
                    '.sf-ml-card .sf-ml-ov{opacity:1!important;transition:none!important;}'
                    '.sf-ml-card .sf-ml-poster{transition:none!important;transform:none!important;'
                    'box-shadow:none!important;}'
                    '}'
                    '.verticalSection h2.sectionTitle{margin-bottom:14px!important;}'
                  '.verticalSection .emby-scroller{overflow-x:auto!important;'
                  'overflow-y:hidden!important;scrollbar-width:none;-ms-overflow-style:none;}'
                  '.verticalSection .emby-scroller::-webkit-scrollbar{height:0;display:none;}'
                  '</style>')

ICONGUARD_MARKER = 'sf-icon-guard'
# Icon-font FOUT. jellyfin-web's own icons set the glyph via a CLASS and use
# font-display:block, so they are invisible until the font arrives. Several of OUR
# buttons/drawer links put the ligature in TEXT, and the family they resolve to
# ("Material Icons Round") is font-display:swap -- which paints the literal word.
# Measured 79 visible elements reading 'more_vert' at t=2.5s.
ICONGUARD_STYLE = ('<style id="sf-icon-guard">'
                   'html:not(.sf-icons-ready) .material-icons{visibility:hidden!important;}'
                   # sf-icon-guard2 (2026-08-29): the action sheet's icons are NOT
                   # .material-icons. Measured on Jellyfin Enhanced's Remove row:
                   # span.actionsheetMenuItemIcon.listItemIcon, font-family
                   # "Material Icons Round", textContent "visibility_off" -- so the
                   # rule above never matched it and the row read
                   # "visibility_off Remove" until the font landed. The admin read that
                   # as Remove being broken. Same family, same swap, same guard.
                   'html:not(.sf-icons-ready) .actionsheetMenuItemIcon,'
                   'html:not(.sf-icons-ready) .listItemIcon{visibility:hidden!important;}'
                   '</style>'
                   '<script>(function(){/* sf-icon-guard */'
                   'function go(){try{document.documentElement.classList.add("sf-icons-ready");}catch(e){}}'
                   'try{if(document.fonts&&document.fonts.ready){document.fonts.ready.then(go).catch(go);}else{go();}}'
                   'catch(e){go();}'
                   'setTimeout(go,4000);'
                   '})();</script>')

# --- Remove ALL lazy loading (2026-07-31, user request: "mobile and desktop, all").
# jellyfin-web lazy-loads images through THREE independent systems:
#   1. its own LazyLoader  -- stashes the url in data-src, adds .lazy-hidden, and
#      only swaps data-src -> src (or -> style.backgroundImage) on intersection;
#   2. react-lazy-load-image-component -- used by the React-migrated pages;
#   3. swiper's loading="lazy" -- the Media Bar carousel.
# All three drive off IntersectionObserver, so rather than chase each one we shim
# IntersectionObserver itself: when something observes an element that looks like a
# lazy image target, we promote it and fire the callback immediately as fully
# visible. Anything else observed (scroll spies, sticky headers, infinite-scroll
# triggers) is forwarded to the REAL observer untouched -- a blanket
# "everything is always intersecting" shim would have broken those too.
# The shim must exist before the bundles run: every jellyfin-web script tag is
# defer, and this inline script sits before </body>, so it executes during parsing
# and therefore ahead of all of them. The intersection-observer POLYFILL bundle
# no-ops because it early-returns when window.IntersectionObserver already exists.
# MutationObserver (childList + data-src attribute) catches nodes added later;
# the interval is a cheap backstop for anything both miss.
# NOTE: this makes big library pages request every poster at once -- that is the
# explicit intent here, but it is why Jellyfin ships lazy loading by default.
NOLAZY_MARKER = 'jf-no-lazy'
NOLAZY_SCRIPT = ('<script>(function(){ /* jf-no-lazy */'
                 'var SEL=\'img[data-src],[data-src],.lazy-image,.lazy-hidden,.swiper-lazy,[class*="lazy-load-image"]\';'
                 # Routes where eager loading is a liability rather than a win. /search was
                 # first (100+ posters per query); the library grids joined it once
                 # libraryPageSize=0 made a single page the WHOLE library -- 589 movies at
                 # ~215KB a poster is ~125MB fired at once on a cold cache. On these routes
                 # the element is handed back to the real IntersectionObserver so Jellyfin's
                 # own lazy loading resumes and art loads as you scroll. Everywhere else
                 # (home, detail pages, Live TV) still loads eagerly as requested.
                 'var LAZYOK=/^#\\/(search|movies|tv|list|music|homevideos)\\b/;'
                 'function onSearch(){try{return LAZYOK.test(location.hash||"");}catch(e){return false;}}'
                 'var gateOpen=false;'
                 'function openGate(){if(gateOpen)return;gateOpen=true;try{sweep(document);}catch(e){}}'
                 'try{document.addEventListener("sf-hero-painted",openGate);}catch(e){}'
                 # Independent of the hero script on purpose: if that fails to install,
                 # __sfHeroPainted never becomes true and a gate keyed only on it would
                 # hold the rows for ever. This timer opens it regardless.
                 'try{setTimeout(openGate,3000);}catch(e){}'
                 'function gated(el){try{'
                 'if(gateOpen)return false;'
                 'if((location.hash||"").indexOf("#/home")!==0)return false;'
                 'if(window.__sfHeroPainted){openGate();return false;}'
                 # sf-cw-visible: the three things on screen at load are the header, the hero
                 # and Continue Watching. The hero was already exempt from this gate; CW was
                 # not, so its posters were held back and then released in the SAME flood as
                 # every below-fold row -- which is exactly why CW felt like it arrived with
                 # the rows instead of with the hero. Exempt it for the same reason the hero
                 # is exempt: you can see it.
                 'if(el&&el.closest&&el.closest("#slides-container,.ContinueWatching"))return false;'
                 'return true;'
                 '}catch(e){return false;}}'
                 # sf-near-fold: eager loading on home fetched art for EVERY card in every
                 # row. Measured at 1440x900: 170 cards, only 5 within one viewport and 99
                 # scrolled off to the RIGHT inside their row carousels (136 of 170 on a
                 # phone). The waste is horizontal far more than vertical, so proximity is
                 # tested on BOTH axes. Anything far away is handed back to the real
                 # IntersectionObserver, and the scroll sweep below catches it if Jellyfin
                 # never observed it. An element with no box yet is treated as far: it has
                 # not been laid out, so its position is unknown and the observer is the
                 # right owner.
                 'function isHome(){try{return (location.hash||"").indexOf("#/home")===0;}catch(e){return false;}}'
                 'function nearby(el){try{'
                 'var r=el.getBoundingClientRect();'
                 'if(!r.width&&!r.height)return false;'
                 'var vh=window.innerHeight||800, vw=window.innerWidth||1200;'
                 'if(r.top>vh*1.5||r.bottom<-vh*0.5)return false;'
                 'if(r.left>vw*1.5||r.right<-vw*0.5)return false;'
                 'return true;}catch(e){return true;}}'
                 'function deferrable(el){return isHome()&&gateOpen&&!nearby(el);}'
                 'function lazyish(el){try{if(onSearch())return false;if(gated(el))return false;if(deferrable(el))return false;return el&&el.nodeType===1&&(el.matches(SEL)||!!el.querySelector(SEL));}catch(e){return false;}}'
                 'function promote(el){try{'
                 'if(!el||el.nodeType!==1||!el.getAttribute)return;'
                 'if(gated(el))return;'
                 'if(deferrable(el))return;'
                 'var ds=el.getAttribute("data-src");'
                 'if(ds){if(el.tagName==="IMG"){if(!el.getAttribute("src"))el.setAttribute("src",ds);}'
                 'else{try{el.style.backgroundImage="url(\'"+ds+"\')";}catch(e){}}el.removeAttribute("data-src");}'
                 'if(el.getAttribute("loading")==="lazy")el.setAttribute("loading","eager");'
                 'if(el.classList){el.classList.remove("lazy-hidden");el.classList.remove("lazy-hidden-children");}'
                 '}catch(e){}}'
                 'function sweep(root){try{if(onSearch())return;var r=(root&&root.querySelectorAll)?root:document;'
                 'var n=r.querySelectorAll(\'[data-src],img[loading="lazy"],.lazy-hidden,.lazy-hidden-children\');'
                 'for(var i=0;i<n.length;i++)promote(n[i]);}catch(e){}}'
                 'function install(){var N=window.IntersectionObserver;if(!N||N.__jfNoLazy)return;'
                 'function S(cb,opts){var self=this;try{this._n=new N(cb,opts);}catch(e){this._n=null;}'
                 'this.observe=function(el){if(lazyish(el)){promote(el);sweep(el);'
                 'var b={};try{b=el.getBoundingClientRect();}catch(e){}'
                 'try{cb([{target:el,isIntersecting:true,intersectionRatio:1,boundingClientRect:b,'
                 'intersectionRect:b,rootBounds:null,time:Date.now()}],self);}catch(e){}}'
                 'else if(self._n){try{self._n.observe(el);}catch(e){}}};'
                 'this.unobserve=function(el){if(self._n){try{self._n.unobserve(el);}catch(e){}}};'
                 'this.disconnect=function(){if(self._n){try{self._n.disconnect();}catch(e){}}};'
                 'this.takeRecords=function(){if(!self._n)return[];try{return self._n.takeRecords();}catch(e){return[];}};}'
                 'S.__jfNoLazy=true;try{S.prototype=N.prototype;}catch(e){}'
                 'try{window.IntersectionObserver=S;}catch(e){}}'
                 'install();'
                 'document.addEventListener("DOMContentLoaded",function(){install();sweep(document);});'
                 # sf-near-fold sweep: rows scroll horizontally inside their own scrollers,
                 # so listen in CAPTURE for scroll anywhere, not just on window. rAF-throttled
                 # so a fast drag costs one pass per frame at most.
                 'var swTick=0;'
                 'function nearSweep(){if(swTick)return;swTick=1;'
                 'try{requestAnimationFrame(function(){swTick=0;try{'
                 'if(!isHome())return;'
                 'var n=document.querySelectorAll(\'[data-src],.lazy-hidden,.lazy-hidden-children\');'
                 'for(var i=0;i<n.length;i++){if(nearby(n[i]))promote(n[i]);}'
                 '}catch(e){}});}catch(e){swTick=0;}}'
                 'try{document.addEventListener("scroll",nearSweep,true);'
                 'window.addEventListener("resize",nearSweep);'
                 'window.addEventListener("hashchange",function(){setTimeout(nearSweep,120);});}catch(e){}'
                 'try{new MutationObserver(function(ms){for(var i=0;i<ms.length;i++){var m=ms[i];'
                 'if(m.type==="attributes"){promote(m.target);continue;}'
                 'var a=m.addedNodes;for(var j=0;j<a.length;j++){if(a[j].nodeType===1){promote(a[j]);sweep(a[j]);}}}})'
                 '.observe(document.documentElement,{childList:true,subtree:true,attributes:true,attributeFilter:["data-src"]});}catch(e){}'
                 'setInterval(function(){sweep(document);},3000);'
                 '})();</script>')

# --- Touch row scrolling (2026-08-01). Companion to the jf-mobile-scroll branding
# CSS, which sets .emby-scroller{overflow-x:auto} on touch so a real scroll
# container exists. That alone was NOT enough: jellyfin-web's scroller is a
# sly-style widget whose touchstart handler (element-level, BUBBLE phase,
# {passive:true}) starts a JS drag that animates transform:translateX on
# .scrollSlider, with releaseSwing + elasticBounds -- so a swipe that fails to
# clear its dragThreshold springs straight back. That spring-back is the bug.
# Reading the minified scroller: options default to touchDragging:1, and for
# touch it deliberately does NOT preventDefault (`e || t.preventDefault()`),
# so native scrolling and the JS drag both run and the transform wins visually.
# touchDragging lives in a closure we cannot reach, so instead we stop the event
# ever reaching sly: a window-level CAPTURE listener registered from index.html
# (which parses before every deferred bundle, so ours is the first capture
# listener on window and fires first) calls stopPropagation for touchstarts
# inside a scroller. passive:true -- we must NEVER preventDefault here, that
# would kill the native scrolling we are trying to enable.
# Guarded three ways: touch-pointer devices only, only when the CSS actually
# made the element scrollable (overflow-x != visible), and only when there is
# something to scroll -- so pointer devices and the desktop arrow buttons
# (jf-scroller-fix) are untouched.
NOLAZY_TOUCHSCROLL_MARKER = 'jf-touch-scroll'
TOUCHSCROLL_SCRIPT = ('<script>(function(){ /* jf-touch-scroll */'
                      'try{if(!window.matchMedia)return;'
                      'if(!matchMedia("(hover: none), (pointer: coarse)").matches)return;'
                      'function isRow(sc){try{'
                      'if(!sc||!sc.getAttribute)return false;'
                      # The guard this replaces tested data-horizontal="true". No scroller in
                      # jellyfin-web carries that attribute -- inspected live, a real row is
                      # <div is="emby-scroller" data-scroll-mode-x="custom" data-centerfocus="true">
                      # -- so enable() returned on its FIRST line every time and this entire
                      # touch fix has been dead code. That is the row snap-back on iOS: sly's
                      # drag was never stopped, so a swipe short of its dragThreshold springs
                      # back. data-scroll-mode-x is the honest signal: it exists only on
                      # scrollers whose X axis sly manages.
                      'if(sc.getAttribute("is")!=="emby-scroller"&&'
                      '!(sc.classList&&sc.classList.contains("emby-scroller")))return false;'
                      'return sc.getAttribute("data-scroll-mode-x")!==null;'
                      '}catch(e){return false;}}'
                      'function enable(sc){try{'
                      'if(!isRow(sc))return;'
                      'var ox=getComputedStyle(sc).overflowX;'
                      'if(ox!=="auto"&&ox!=="scroll"){'
                      'sc.style.setProperty("overflow-x","auto","important");'
                      'sc.style.setProperty("overflow-y","hidden","important");'
                      'try{window.__jfTouchScroll.enabled++;}catch(e){}}'
                      '}catch(e){}}'
                      'function sweep(root){try{'
                      'try{window.__jfTouchScroll.sweeps++;}catch(e){}'
                      'var r=(root&&root.querySelectorAll)?root:document;'
                      'if(r.matches&&r.matches(".emby-scroller,[is=emby-scroller]"))enable(r);'
                      'var n=r.querySelectorAll(".emby-scroller,[is=emby-scroller]");'
                      'for(var i=0;i<n.length;i++)enable(n[i]);'
                      '}catch(e){}}'
                      'window.addEventListener("touchstart",function(e){try{'
                      'var t=e.target;if(!t||!t.closest)return;'
                      'var sc=t.closest(".emby-scroller,[is=emby-scroller],.sf-ml-row");if(!sc)return;'
                      # OUR rows (.sf-ml-row) are plain overflow-x containers, not
                      # emby-scrollers, so they never reached the stopPropagation below and
                      # a horizontal drag on them travelled up to emby-tabs' swipe handler.
                      # Captured on an emulated iPhone 17: swiping My List removed is-active
                      # from the home pane at t=19981, the pane went display:none, the
                      # sections container collapsed 2390px -> 0, the document shrank to
                      # exactly one viewport, the browser CLAMPED scrollY 830 -> 0, and
                      # is-active came back 130ms later -- leaving the user at the top of the
                      # page. That is the "crash and jump" on the music and My List rows.
                      # A control run with no interaction showed 0 collapses in 280 samples,
                      # so the gesture is the trigger, not a timer.
                      # They need the shield, not the overflow fix-up, so they take it and stop.
                      'if(sc.classList&&sc.classList.contains("sf-ml-row")){'
                      'if(sc.scrollWidth>sc.clientWidth)e.stopPropagation();'
                      'return;}'
                      'if(!isRow(sc))return;'
                      'enable(sc);'
                      'var ox=getComputedStyle(sc).overflowX;'
                      'if(ox!=="auto"&&ox!=="scroll")return;'
                      'if(sc.scrollWidth<=sc.clientWidth)return;'
                      'e.stopPropagation();'
                      '}catch(err){}},{capture:true,passive:true});'
                      'window.__jfTouchScroll={sweeps:0,enabled:0};'
                      'sweep(document);'
                      'document.addEventListener("DOMContentLoaded",function(){sweep(document);});'
                      # Verified on an emulated iPhone 17 (402x874, DPR3, pointer:coarse):
                      # all six row scrollers passed the guard, yet every one still had
                      # overflow-x:hidden and no inline style -- enable() had never run on
                      # any of them. emby-scroller is a CUSTOM BUILT-IN element, so
                      # is=/data-scroll-mode-x land when the element upgrades, which can be
                      # after the MutationObserver has already seen the node and skipped it.
                      # A node only gets one chance from that observer and there was nothing
                      # to revisit it. This re-sweep is that second chance; it is idempotent
                      # (enable() no-ops once overflow-x is auto) and matches the interval
                      # jf-no-lazy already uses for the same class of race.
                      'setInterval(function(){sweep(document);},1500);'
                      'try{new MutationObserver(function(ms){for(var i=0;i<ms.length;i++){'
                      'var a=ms[i].addedNodes;for(var j=0;j<a.length;j++){'
                      'if(a[j].nodeType===1)sweep(a[j]);}}})'
                      '.observe(document.documentElement,{childList:true,subtree:true});}catch(e){}'
                      '}catch(err){}})();</script>')

# --- Boot splash mark (2026-08-02). index.html renders
# <div class="splashLogo"></div> during startup, and the bundle CSS points it at
# `banner-light.<hash>.png` -- a WORDMARK LOCKUP (jellyfish + the word
# "Jellyfin" in one image). That is why the reload flash still read "Jellyfin"
# after the rest of the rebrand: you cannot keep that artwork without the name.
# Jellyfin also ships the mark on its own at favicons/touchicon512.png, which
# (unlike the banner) is NOT content-hashed, so the path stays valid across
# image updates. Injected as a <style> in index.html rather than branding Custom
# CSS because the splash paints before the branding stylesheet is fetched.
# background-size/position are restated since the stock rule is shaped for a
# wide banner and would otherwise stretch a square icon.
# sf-atv-failsafe-12s (2026-08-29). The failsafe delay was 4s, and its job is
# to reveal the page if sfDetailHero never fires. But sf-atv is gated on
# ApiClient.getItem, and that endpoint measured 2.3-5.1s on the PUBLIC h2 origin
# (1.5-4.2s on :8096) -- so on the warm in-app path 4/8 sampled movies overran
# the failsafe and it revealed the STOCK layout at ~4.1s, which then snapped to
# ours at 5.5-6.7s. The admin: "i dont want to see the old layout as we load, i only
# want to see the complete new layout." Firing the failsafe IS showing the old
# layout, so it must only ever fire on genuine failure: 12s clears the measured
# max (6.58s warm / 9.43s cold) with headroom. The page is not blank meanwhile --
# it shows the blurred backdrop and the header. The real fix is the slow item
# endpoint; this stops it being visible.
ATVBOOT_MARKER = 'jf-atv-boot'
ATVBOOT_STYLE = ('<style id="jf-atv-boot">'
                 # sf-hold-off: with no snapshot covering the screen, a page that
                 # hides itself until we have finished styling it IS the blank gap.
                 # Jellyfin paints this page at ~240ms; that is what the user should
                 # see. .sf-atv still arrives and restyles it in place.
                 # sf-motion: a PAGE-level fade, deliberately not the 700ms content
                 # entrance -- the detail page arrives as one composed unit after a
                 # wait, and a long fade on top of that wait reads as more waiting.
                 # This used to disagree with a second copy in branding.xml
                 # (.34s cubic-bezier) which won on source order; that copy is gone.
                 # ...and it must not fade in either: the page is already on screen by
                 # then, so replaying an entrance would darken it back to nothing and
                 # bring it up again -- a flash caused entirely by the animation.
                 # sf-atv-shortgate (2026-09-05). The page is composed at ~230ms now
                 # that the item is warmed and nothing waits on a tick -- it used to
                 # be 900-1700ms, which is why showing it half-built ever seemed
                 # worth it. At 230ms it is not: revealing Jellyfin's stock layout
                 # first and restyling it in place moved the action buttons 241px in
                 # full view, and reserving the hero's space up front over-corrected
                 # the other way (274px). Both were measured.
                 # So wait the 230ms and arrive complete. This is NOT the old hold:
                 # nothing of the previous screen is kept, no page is cloned, and the
                 # failsafe is 2s rather than 12s so a stalled item can never leave a
                 # page invisible for long.
                 '#itemDetailPage:not(.sf-atv):not(.sf-alb-on){'
                 'animation:jfAtvFailsafe .2s ease 2s both;}'
                 '#itemDetailPage.sf-atv{animation:none;}'
                 '@keyframes jfAtvIn{from{opacity:0}to{opacity:1}}'
                 '@keyframes jfAtvFailsafe{from{opacity:0}to{opacity:1}}'
                 '</style>')

# --- Empty hero overlay (2026-08-23). The Media Bar plugin creates
# #slides-container for the home hero and gives it a full 1440x810 box BEFORE
# its slides arrive. In that window the element has ZERO element children, is
# still display:block with pointer-events:auto, and hit-tests to ITSELF -- so
# every click landing in the top ~810px of the page goes into an invisible,
# empty box. Reproduced on a cold #/home load: {kids:0, rect:[0,0,1440,810],
# blocks:true}; once the slides land (kids:8) it behaves. Three independent QA
# passes hit this on desktop AND Android, on home and on album/artist/audiobook
# detail pages, where it reads as "the top of the page is dead".
#
# `:has(> *)` rather than `:empty` on purpose -- the container carries whitespace
# text nodes, which defeat :empty while leaving it visually and behaviourally
# empty. The rule is live, so the instant Media Bar appends a slide the override
# stops applying on its own; no observer, no timer, no teardown to get wrong.
SLIDESEMPTY_MARKER = 'sf-slides-empty'
# sf-hero-reserve (2026-08-29). Collapsing the empty container to height:0
# fixed the dead clicks and created a worse problem: the page then has TWO
# different layouts. Measured over repeated cold loads --
#   hero 945px, 8 slides -> Continue Watching row lands at y=643
#   hero   0px, 0 slides -> the same row lands at y=0
# Media Bar does not always deliver its slides (1 of 3 loads on a loaded
# box), so the rows moved 643px between one visit and the next. That is the
# "why is it never in the same place" complaint, and it is caused here.
#
# Hold the hero's real footprint instead of collapsing it. Measured exactly
# 90vh desktop and 92vh at <=45em, so the reservation is the true size at
# every viewport rather than a guessed pixel value. pointer-events:none is
# what actually fixed the dead clicks -- the element hit-tested to ITSELF --
# and it is kept; visibility:hidden means an empty box is never seen.
# The rule is live, so the instant Media Bar appends a slide it stops
# applying and the real hero occupies exactly the space already held.
SLIDESEMPTY_STYLE = ('<style id="sf-slides-empty">'
                     '/* sf-hero-reserve */'
                     '#slides-container:not(:has(> *)){'
                     'pointer-events:none!important;visibility:hidden!important;'
                     'min-height:90vh!important;}'
                     '@media (max-width:45em){'
                     '#slides-container:not(:has(> *)){min-height:92vh!important;}}'
                     '</style>')

# --- Header scrim (2026-08-23). .skinHeader ships the classes
# `skinHeader-withBackground skinHeader-blurred semiTransparent`, but the
# computed style is background rgba(0,0,0,0) with backdrop-filter:none -- BOTH
# at scrollTop 0 and scrolled 900px. So the back/hamburger and
# cast/language/search/account icons sit directly on whatever poster or episode
# still happens to be underneath, and legibility is pure luck. Most obvious on
# the Steam Deck at 1280x800, but it is every viewport.
#
# A top-down gradient rather than a flat fill, and no scroll listener: the class
# list never changes on scroll here, so a JS toggle would mean a scroll handler
# on a 4-core N100 for something CSS does for free. The gradient reads as
# deliberate over a hero AND keeps the icons legible over content.
HDRSCRIM_MARKER = 'sf-hdr-scrim'
HDRSCRIM_STYLE = ('<style id="sf-hdr-scrim">'
                  '.skinHeader{'
                  'background:transparent!important;background-color:transparent!important;'
                  ''
                  '-webkit-backdrop-filter:none!important;'
                  'backdrop-filter:none!important;}'
                  '</style>')

# --- Paused-session clobber (2026-08-23). A PAUSED tab rewinds your bookmark.
#
# jellyfin-web POSTs /Sessions/Playing/Progress every 10 seconds and KEEPS DOING
# IT AFTER YOU PAUSE, carrying the position it is parked at. The server takes the
# last writer, so an idle paused tab overwrites a newer position saved by another
# device -- and then does it again every 10s, pinning it there.
#
# Measured: paused a book at 67.3s, then advanced the server to 1800s as another
# device would. Within 10s the paused tab clawed it back to 67.3s and held it
# there for the whole 80s observation. That is 29 minutes of listening silently
# destroyed by a tab nobody was looking at.
#
# This is almost certainly what an audit reported as "resume uses a stale cached
# position" -- its log shows the server holding 110.2s while playback began at
# 67.6s, the same shape and very nearly the same number. Resume itself is fine:
# three separate reproductions showed playback correctly using the server's
# value. The position was being CORRUPTED before the tap, not misread during it.
#
# Fix: while the audio is paused, allow ONE progress report (so remote-control
# UIs still see "paused at X") and drop the repeats that carry no new
# information. A paused player has nothing to report -- its position is not
# moving. Playing reports and the final Stopped report are untouched, so the
# position is still saved normally when you actually stop.
PAUSEREP_MARKER = 'sf-pause-report'
PAUSEREP_SCRIPT = r"""<script>(function(){ /* sf-pause-report */
var lastPaused=null;
function audio(){return document.querySelector('audio')||document.querySelector('video');}
function suppress(url){
  if(!url||String(url).indexOf('/Sessions/Playing/Progress')<0)return false;
  var a=audio();
  if(!a||!a.paused){lastPaused=null;return false;}   /* playing: always report */
  var pos=Math.round(a.currentTime||0);
  if(lastPaused!==null&&Math.abs(pos-lastPaused)<2)return true;  /* nothing new */
  lastPaused=pos;
  return false;
}
var of=window.fetch;
if(of){
  window.fetch=function(input,init){
    try{
      var u=(typeof input==='string')?input:(input&&input.url);
      if(suppress(u))return Promise.resolve(new Response(null,{status:204,statusText:'No Content'}));
    }catch(e){}
    return of.apply(this,arguments);
  };
}
var ox=XMLHttpRequest.prototype.open, os=XMLHttpRequest.prototype.send;
XMLHttpRequest.prototype.open=function(m,u){this.__sfUrl=u;return ox.apply(this,arguments);};
XMLHttpRequest.prototype.send=function(){
  try{if(suppress(this.__sfUrl))return;}catch(e){}
  return os.apply(this,arguments);
};
})();</script>"""

# --- Volume popover (2026-08-23). The speaker button toggles `sf-vol-open` on
# <body> and always has -- but NO CSS anywhere ever implemented that class, so
# clicking it did nothing at all and the slider stayed collapsed. Measured on the
# capsule during playback: .nowPlayingBarVolumeSlider [988,836,0,36] and its
# .nowPlayingBarVolumeSliderContainer both computing to width:0px, so there was
# no volume control on desktop at all -- an audit filed it as "renders 0px wide
# and cannot be hit", which was the symptom of a half-built feature rather than a
# layout bug.
#
# This supplies the missing half, matching the intent recorded at the toggle:
# "Apple's speaker is the last control and opens the slider on CLICK" -- click,
# not hover, because hover-to-expand grew the slider under the pointer whenever
# you reached for the heart or the overflow menu.
VOLPOP_MARKER = 'sf-vol-pop'
VOLPOP_STYLE = ('<style id="sf-vol-pop">'
                '.nowPlayingBar .nowPlayingBarVolumeSliderContainer{'
                'width:0!important;min-width:0!important;opacity:0!important;'
                'overflow:hidden!important;flex:0 0 auto!important;'
                'transition:width .18s ease,opacity .18s ease,margin .18s ease!important;}'
                'body.sf-vol-open .nowPlayingBar .nowPlayingBarVolumeSliderContainer{'
                'width:104px!important;opacity:1!important;margin:0 6px 0 2px!important;}'
                'body.sf-vol-open .nowPlayingBar .nowPlayingBarVolumeSlider{'
                'width:104px!important;min-width:104px!important;}'
                # the speaker reads as "on" while its slider is out
                'body.sf-vol-open .nowPlayingBar .muteButton{color:#fff!important;}'
                '@media (prefers-reduced-motion: reduce){'
                '.nowPlayingBar .nowPlayingBarVolumeSliderContainer{transition:none!important;}}'
                '</style>')

# --- JellyfinEnhanced helpers shim (2026-08-23). The plugin's own features.js
# runs `const handleItemDetails = JE.helpers.debounce(...)` at module top level,
# and `window.JellyfinEnhanced.helpers` is sometimes undefined at that moment --
# its script files load out of order. Measured: 3 of 20 cold loads (15%) threw
# `Cannot read properties of undefined (reading 'debounce')` at features.js:940,
# and because the throw is inside the file's top-level IIFE, EVERYTHING after
# line 940 never runs for that page load. So 15% of the time a chunk of the
# plugin silently does not exist.
#
# We cannot edit the plugin, but we can make the namespace exist before it looks.
# Defined in <head>, so it is in place before any plugin script executes. Only
# fills in what is MISSING -- if the real helpers load afterwards they overwrite
# this, and if they never do, features.js still gets a working debounce.
JEHELP_MARKER = 'sf-je-helpers'
JEHELP_SCRIPT = ("""<script id="sf-je-helpers">(function(){
try{
/* A plain assignment is not enough: measured 5/20 loads still throwing with the
   shim demonstrably in place at load time, because the plugin REPLACES the whole
   namespace (window.JellyfinEnhanced = {...}), discarding whatever was there.
   So intercept the assignment instead -- accept whatever the plugin sets, then
   re-attach any helper it has not defined yet. Their real helpers always win;
   we only ever fill a hole. */
function mkdeb(){return function(fn,wait){
var t=null,w=(typeof wait==='number'?wait:250);
return function(){var self=this,args=arguments;
if(t)clearTimeout(t);
t=setTimeout(function(){t=null;fn.apply(self,args);},w);};};}
function mkthr(){return function(fn,wait){
var last=0,w=(typeof wait==='number'?wait:250);
return function(){var now=Date.now();
if(now-last>=w){last=now;fn.apply(this,arguments);}};};}
/* Fixing debounce revealed createObserver -- the earlier throw was ABORTING the
   file before it ever reached that call, so one bug was hiding the next. A stub
   is strictly better than a throw: the caller gets a live MutationObserver
   wrapper instead of dying and taking the rest of the module with it. If the
   plugin's real helpers arrive later the setter below keeps theirs. */
function mkobs(){return function(cb,opts){
try{
var mo=new MutationObserver(function(recs){try{if(cb)cb(recs);}catch(e){}});
return {observe:function(t,o){try{mo.observe(t||document.body,o||opts||{childList:true,subtree:true});}catch(e){}},
        disconnect:function(){try{mo.disconnect();}catch(e){}},
        takeRecords:function(){try{return mo.takeRecords();}catch(e){return [];}}};
}catch(e){return {observe:function(){},disconnect:function(){},takeRecords:function(){return [];}};}
};}
function ensure(o){
if(!o||typeof o!=='object')return o;
var h=o.helpers;
if(!h||typeof h!=='object'){h={};
try{Object.defineProperty(o,'helpers',{configurable:true,enumerable:true,
get:function(){return h;},
set:function(v){ if(v&&typeof v==='object'){
  if(typeof v.debounce!=='function')v.debounce=mkdeb();
  if(typeof v.throttle!=='function')v.throttle=mkthr();
  if(typeof v.createObserver!=='function')v.createObserver=mkobs();
  h=v; } }});}catch(e){o.helpers=h;}
}
if(typeof h.debounce!=='function')h.debounce=mkdeb();
if(typeof h.throttle!=='function')h.throttle=mkthr();
if(typeof h.createObserver!=='function')h.createObserver=mkobs();
return o;
}
var cur=ensure(window.JellyfinEnhanced||{});
Object.defineProperty(window,'JellyfinEnhanced',{configurable:true,enumerable:true,
get:function(){return cur;},
set:function(v){cur=ensure(v||{});}});
}catch(e){}
})();</script>""")

# --- Detail action row settle (2026-08-02). Opening a detail page showed the
# buttons arriving in FOUR visible stages -- measured on a never-watched movie:
#   149ms  a lone "Resume" button   <- STALE: Jellyfin paints from default/last
#                                      user-data before the real data arrives,
#                                      so an unwatched film offers "Resume"
#   936ms  flips to Play + Trailer, Mark played, Favorites, More
#   1446ms "Hide" appears           <- Jellyfin Enhanced injecting its button
#   1753ms "Hide" renames to "Add to Watchlist"  <- our own jf-watchlist-btn
# All 13 buttons are in the DOM from the first paint; Jellyfin ships the full
# set in the template and toggles a `.hide` class per item as data resolves.
# So nothing is "loading" -- it is a visibility cascade, which is why it reads
# as flicker. The Play/Resume flip is the same cascade hitting the `title`
# attribute, which our jf-action-row CSS renders via `content: attr(title)`.
#
# Fix: hold `.mainDetailButtons` at opacity 0 from the moment it appears, watch
# it, and reveal once it has been QUIET for 180ms (or at the CAP, whichever is
# first). Opacity -- not display -- so the row keeps its space and nothing
# reflows. Result is one clean fade instead of four pops, and the bogus
# "Resume" is never seen because it is gone long before the row settles.
#
# FAILS OPEN BY DESIGN: the hiding is done from JS, never from CSS, so if this
# script does not run the buttons are simply normal. The cap timer is armed
# before the observer and reveals unconditionally, and any MutationObserver
# failure reveals immediately -- there is no path that leaves the row invisible.
BTNSETTLE_MARKER = 'jf-btn-settle'
BTNSETTLE_SCRIPT = r'''<script>(function(){ /* jf-btn-settle */
var QUIET=250, MIN=650, CAP=2600;
/* v1 set opacity from JS once the body observer noticed a new row, which was
   1-2 frames too late: the row painted its stale "Resume" first and was then
   hidden, so a ~120ms flash of exactly the wrong content remained. The hide has
   to be in effect BEFORE the row's first paint, which only CSS can do. The rule
   is injected BY THIS SCRIPT, so it cannot exist unless the script ran -- if the
   patch is ever absent the buttons are simply normal. */
var st=document.createElement('style');
st.textContent='.mainDetailButtons{transition:opacity .15s ease;}'
+'.mainDetailButtons:not([data-jf-settled]){opacity:0;}';
(document.head||document.documentElement).appendChild(st);
function settle(row){row.setAttribute('data-jf-settled','1');}
function arm(row){
if(!row||row.getAttribute('data-jf-armed'))return;
row.setAttribute('data-jf-armed',Date.now());
var timer=null,cap=null,obs=null,armedAt=Date.now();
function reveal(){
if(obs){try{obs.disconnect();}catch(e){}}
clearTimeout(timer);clearTimeout(cap);
settle(row);
}
function tryReveal(){
var left=MIN-(Date.now()-armedAt);
if(left>0){clearTimeout(timer);timer=setTimeout(tryReveal,left);return;}
reveal();
}
cap=setTimeout(reveal,CAP);
function bump(){clearTimeout(timer);timer=setTimeout(tryReveal,QUIET);}
try{obs=new MutationObserver(bump);
obs.observe(row,{childList:true,subtree:true,attributes:true,attributeFilter:['class','style','title']});
}catch(e){reveal();return;}
bump();
}
function sweep(){arm(document.querySelector('.page:not(.hide) .mainDetailButtons'));}
window.addEventListener('hashchange',function(){setTimeout(sweep,0);});
try{new MutationObserver(sweep).observe(document.body,{childList:true,subtree:true});}catch(e){}
/* Watchdog. The CSS hides every row by default, so a row that somehow never got
   armed (observer missed it, script threw) would stay invisible forever. Anything
   unsettled for longer than CAP is force-revealed, including never-armed rows,
   which are stamped on first sight so they get a full CAP of grace rather than
   being settled mid-render. */
setInterval(function(){
var rs=document.querySelectorAll('.mainDetailButtons:not([data-jf-settled])');
for(var i=0;i<rs.length;i++){
var a=rs[i].getAttribute('data-jf-armed');
if(!a){var s=rs[i].getAttribute('data-jf-seen');
if(!s)rs[i].setAttribute('data-jf-seen',Date.now());
else if(Date.now()-parseInt(s,10)>CAP)settle(rs[i]);
continue;}
if(Date.now()-parseInt(a,10)>CAP)settle(rs[i]);
}
},1000);
sweep();
})();</script>'''

# --- Scroller pagination fix: clicking a row's next/prev arrow (data-direction
# left/right on .emby-scrollbuttons-button) throws "t.scrollHandler is not a
# function" in Jellyfin's own bundled scroller code and crashes before applying
# the transform that would advance the row — the row's items are still in the
# DOM (confirmed via devtools), the row just visually goes blank because the
# translateX never updates. Reproduces on any row with more than one page
# (search results, Discover on Seerr, likely others — they share the component).
# Not fixable by patching the minified bundle directly, so we intercept the
# arrow click in the CAPTURE phase (before Jellyfin's broken handler runs),
# stop it, and drive the same transform:translateX(...) mechanism ourselves by
# reading the track's current matrix and computing a new page offset. Content
# extent is measured via first/last child offsetLeft+offsetWidth rather than
# track.scrollWidth: scrollWidth only tracks "scrollable overflow", which the
# browser never establishes on elements styled overflow-x:visible (true of
# rows like Discover on Seerr) — there scrollWidth just equals clientWidth,
# under-reporting real content width and letting a "next" click translate the
# whole track past its actual content, landing on empty page background. Child
# offsetLeft/offsetWidth reflect real layout regardless of overflow or any
# transform we've applied (transforms are paint-only, not layout).
# --- Plugin Pages duplicate-request dedupe (2026-08-04).
# The Plugin Pages plugin's inject.js registers a MutationObserver on <body>
# with subtree+attributes, and its mutationHandler checks `PluginPages.initialized`
# ONCE at the top of the observer callback -- but then loops over every
# mutationRecord (and every addedNode within each) calling populateSidebar()
# without ever re-checking the flag. One burst of DOM changes therefore fires
# GET /PluginPages/User ~8 times, all within 1ms of each other. Measured: 8
# calls, 778ms cumulative, 183ms wall-clock, durations climbing 24->182ms as
# they queue behind each other. The response is a static 2-item menu list.
# inject.js is an embedded resource inside Jellyfin.Plugin.PluginPages.dll, so
# there is no file on disk to patch -- dedupe at the network layer instead.
# All 8 go through window.fetch (verified via PerformanceResourceTiming
# initiatorType), so wrapping fetch catches every one.
PAGESDEDUPE_MARKER = 'jf-pluginpages-dedupe'
PAGESDEDUPE_SCRIPT = (
    '<script>(function(){ /* jf-pluginpages-dedupe */'
    # Wrapping window.fetch does NOT work: something later in the load
    # (abortcontroller-polyfill / JE) reassigns window.fetch having captured the
    # native one, orphaning any earlier wrapper -- verified live, 3 calls still
    # produced 3 requests. Hook what inject.js actually calls: ApiClient.getJSON.
    # It resolves to parsed JSON (not a Response), so one promise can be shared
    # with every caller, no clone() needed. Assigning on the instance shadows the
    # prototype method.
    # MEASURING NOTE: performance.getEntriesByType("resource") caps at 250 entries
    # and silently drops the rest -- a saturated buffer makes a broken dedupe look
    # like it works. clearResourceTimings() first, or read from devtools/network.
    'var cache=null;'
    'var iv=setInterval(function(){'
    'try{'
    'if(!window.ApiClient||!ApiClient.getJSON||ApiClient.__ppDedupe){return;}'
    'ApiClient.__ppDedupe=1;'
    'var orig=ApiClient.getJSON;'
    'ApiClient.getJSON=function(url){'
    'if(String(url).indexOf("PluginPages/User")!==-1){'
    'if(!cache){cache=orig.apply(this,arguments)["catch"](function(e){cache=null;throw e;});}'
    'return cache;'
    '}'
    'return orig.apply(this,arguments);'
    '};'
    'clearInterval(iv);'
    '}catch(e){clearInterval(iv);}'
    '},50);'
    'setTimeout(function(){clearInterval(iv);},30000);'
    '})();</script>'
)


# Chapters ("Scenes" on the detail page). Most rips strip the chapter NAMES and
# leave positional markers, so the row reads "Chapter 00..15" and tells you
# nothing. Chapter image extraction is also disabled on both libraries, so the
# cards would be blank anyway. The chapters still exist in the file -- this only
# hides the row.
# Jellyfin Enhanced's bookmark button resolves the playing item with
#     itemId = btnUserRating?.dataset?.id
# i.e. it reads data-id off the OSD's favourite/rating button. In Jellyfin
# 10.11.11 that button stays class="btnUserRating hide" with NO data-id during
# movie playback, because jellyfin-web only calls setItem() when canRate(item)
# is true and canRate requires item.UserData, which the OSD item lacks. Result:
# clicking bookmark says "cannot bookmark, no item found". Verified live.
# This shim supplies the attribute from our own session's NowPlayingItem.
BMITEMID_MARKER = 'jf-bookmark-itemid'
BMITEMID_SCRIPT = """<script>(function(){
  /* jf-bookmark-itemid */
  var done = false, busy = false;
  function onVideo(){ return /^#\\/video/.test(location.hash || ''); }
  function reset(){ done = false; }
  window.addEventListener('hashchange', function(){ if(!onVideo()) reset(); });
  setInterval(function(){
    if (!onVideo() || done || busy) return;
    var rb = document.querySelector('.videoOsdBottom .btnUserRating');
    if (!rb) return;
    if (rb.getAttribute('data-id')) { done = true; return; }   /* jellyfin set it itself */
    var ac = window.ApiClient;
    if (!ac || !ac.getUrl) return;
    busy = true;
    ac.getJSON(ac.getUrl('/Sessions', { DeviceId: ac.deviceId() })).then(function(list){
      var mine = (list || []).filter(function(x){ return x.NowPlayingItem; })[0];
      if (mine && mine.NowPlayingItem) {
        rb.setAttribute('data-id', mine.NowPlayingItem.Id);
        if (mine.NowPlayingItem.ServerId) rb.setAttribute('data-serverid', mine.NowPlayingItem.ServerId);
        done = true;
      }
    }).catch(function(){}).then(function(){ busy = false; });
  }, 2500);
})();</script>"""

# Rename the home page's "Favorites" pill to "My Stuff". The label comes from
# getTabs(){[{name:translate("Home")},{name:translate("Favorites")},...]} so it
# is a translated string, not markup -- renaming in the DOM is safer than
# patching the bundle. Scoped to #indexPage so the Movies/Shows pages keep their
# own "Favorites" tab untouched. Only the text changes; the tab keeps working.
MYSTUFF_MARKER = 'jf-mystuff-tab'
MYSTUFF_SCRIPT = r"""<script>(function(){ /* jf-mystuff-tab */
var LABEL="My Stuff", FROM="Favorites";
/* jf-mystuff-scope (2026-08-20). This ran on WHATEVER tab strip happened to be
   first in the document, because both lookups were unscoped:
     - the `page` guard is `#indexPage:not(.hide)`, and Jellyfin CACHES the home
       page, so a stale copy that has not been marked .hide keeps it truthy on
       every other route;
     - `slider` is a bare document.querySelector, and on #/music the first
       `.headerTabs.sectionTabs` in the DOM is the MUSIC page's tab strip.
   So on Music it renamed that page's own "Favorites" tab to "My Stuff" and wired
   it to replaceState("#/home?tab=1"). Reproduced: press the Music button from
   home and the strip reads "Albums | Suggestions | Artists | Playlists |
   My Stuff" with My Stuff lit, the URL silently becomes #/home?tab=1, and every
   music function bails on its `hash.indexOf('#/music')` guard -- no greeting, no
   featured hero with Play/Mix, no "Made for you", no Top Artists. The user gets
   a bare album grid and a Back button that goes somewhere else.
   replaceState fires no hashchange, which is why this never showed up in a
   navigation trace.
   The route is the unambiguous authority for "are we on home", so gate on it,
   and put every button back the way it was when we are not. */
function onHome(){
  var h=location.hash||"";
  return h===""||h==="#"||h==="#/"||h.indexOf("#/home")===0;
}
function restore(){
  var was=document.querySelectorAll("[data-jf-was]"),i,w;
  for(i=0;i<was.length;i++){
    w=was[i].getAttribute("data-jf-was");
    if(w&&(was[i].textContent||"").trim()===LABEL)was[i].textContent=w;
    was[i].removeAttribute("data-jf-was");
  }
}
function ren(){
  if(!onHome()){restore();return;}
  var pages=document.querySelectorAll("#indexPage"),page=null,pi;
  for(pi=0;pi<pages.length;pi++){
    if(pages[pi].offsetParent!==null&&pages[pi].getBoundingClientRect().height>0){page=pages[pi];break;}
  }
  if(!page)return;
  var slider=document.querySelector(".headerTabs.sectionTabs .emby-tabs-slider")||document.querySelector(".headerTabs.sectionTabs");
  if(!slider)return;
  var btns=slider.querySelectorAll(".emby-tab-button, button");
  for(var i=0;i<btns.length;i++){
    var b=btns[i];
    /* remember the ORIGINAL label -- it is a translated string, so restoring a
       hardcoded "Favorites" would put English into a German or Chinese UI. */
    if((b.textContent||"").trim()===FROM){ b.setAttribute("data-jf-was",FROM); b.textContent=LABEL; }
  }
  /* jf-mystuff-active: My Stuff now has a real URL (#/home?tab=1) so it survives
     a reload and no longer needs the navigate-then-poll-and-click dance that cost
     ~1.3s. But Jellyfin activates tabs by DOM INDEX, and the custom Live TV /
     Sports buttons sit between Home and My Stuff -- so ?tab=1 renders the
     Favorites CONTENT while highlighting whatever is at DOM index 1 (Live TV).
     Correct the highlight to match what is actually on screen. */
  /* jf-mystuff-highlight-fix: this correction MUST be symmetric. The original
     only ran for ?tab=1, so the active class was SET on My Stuff but never
     CLEARED -- pressing Home swapped the pane back to homeTab while My Stuff
     stayed lit (verified: visiblePane=homeTab, My Stuff still active).
     Jellyfin never fixes it itself because the Home pill clicks
     .headerHomeButton, not the tab, so its tab-activation never runs.
     Sports has its own bar and is deliberately excluded. */
  /* jf-tab-highlight: ren() is the SINGLE authority for which of the home
     page's four tabs is lit, because Jellyfin gets it wrong on its own.
     emby-tabs activates by DOM INDEX, and our Live TV / Sports buttons sit
     between Home and My Stuff -- so ?tab=1 renders Favorites CONTENT while
     Jellyfin lights index 1 (Live TV). Previously we lit My Stuff on top of
     that and skipped Live TV/Sports entirely, leaving TWO tabs lit.
     Now every one of the four is set from the URL, so exactly one can be lit.

     Deliberately inert when body.jf-ltv-nav is set: that is the Live TV /
     Sports pill bar (.jf-sp-tab), which buildMain owns. Touching those would
     mean two owners fighting over the same buttons. */
  if(!(document.body&&document.body.classList.contains("jf-ltv-nav"))){
    var _h=location.hash||"";
    /* sf-ren-livetv (2026-08-29): Live TV is a HOME url now (#/home?livetv=1),
       so "not tab=1" no longer means Home. This block is meant to be inert on
       Live TV via body.jf-ltv-nav, but that class is applied on a different
       schedule than the hash changes -- during the switch there is a window
       where the URL already says livetv=1 and the class has not landed, and in
       that window this lit HOME. sfHomeBarUnify then cleared it on its own tick
       and the two fought: measured My Stuff -> Live TV as
       My Stuff -> Home -> Live TV, with Home lit for ~68ms. Reading the hash
       directly removes the dependency on class timing. */
    var _want=/[?&]tab=1\b/.test(_h)?LABEL:(_h.indexOf("livetv=1")>=0?"Live TV":"Home");
    var _own={Home:1,"Live TV":1,Sports:1};_own[LABEL]=1;
    for(var j=0;j<btns.length;j++){
      if(btns[j].classList.contains("jf-sp-tab"))continue;  /* buildMain's, not ours */
      var t=(btns[j].textContent||"").trim();
      if(!_own[t])continue;                                  /* leave anything else alone */
      btns[j].classList.toggle("emby-tab-button-active", t===_want);
    }
  }
  /* jf-mystuff-urlsync: clicking Jellyfin's own home tabs switches content
     WITHOUT touching the URL, so a reload on My Stuff dropped you back on Home.
     Mirror the choice into the address bar with replaceState -- not a hash
     assignment, which would re-enter the router and re-render the page. */
  for(var k=0;k<btns.length;k++){
    if(btns[k].getAttribute("data-jf-urlsync"))continue;
    var lbl=(btns[k].textContent||"").trim();
    if(lbl!==LABEL&&lbl!=="Home")continue;
    btns[k].setAttribute("data-jf-urlsync","1");
    (function(el,label){
      el.addEventListener("click",function(){
        setTimeout(function(){
          /* jf-mystuff-scope: re-check the route AT CLICK TIME. A listener bound
             while this was mis-scoped outlives the fix, and rewriting the URL to
             #/home from a tab on another page is exactly the fault above. */
          if(!onHome())return;
          try{history.replaceState(null,"",label===LABEL?"#/home?tab=1":"#/home");}catch(e){}
        },30);
      });
    })(btns[k],lbl);
  }
}
/* jf-observer-scope: was document.body with subtree+attributes, so every class change anywhere re-ran this. A pane swap emits ~544 mutations, and with 4 such observers that is thousands of needless callbacks -- measured as a fixed ~1.4s tab switch. The tab slider lives inside .skinHeader, so that is the smallest correct scope. Page .hide state is still evaluated on each run, and the existing setInterval covers anything the narrower scope misses. Falls back to body if the header never appears. */
(function _at(){var _t=document.querySelector('.skinHeader');
if(!_t){return setTimeout(_at,300);}
new MutationObserver(ren).observe(_t,{childList:true,subtree:true,attributes:true,attributeFilter:['class']});})();
setInterval(ren,1500); ren();
})();</script>"""

ABCUT_MARKER = 'sf-ab-cut'
# sf-ab-cut (2026-08-28). Audiobook control-bar hierarchy + the two controls the admin
# asked to lose.
#
# THIS LIVES IN ITS OWN BLOCK ON PURPOSE. The first attempt appended these rules
# next to '.sf-ab-btn:active' in sf-tap-feel -- which sits inside
# `@media (hover:none)`, an :active treatment meant for touch. Everything landed
# inside that query: the rules were present in index.html (grep found them) and
# absent from document.styleSheets, so the secondary group was never dimmed on a
# desktop and the two buttons never went away. Measured: the selector matched
# (castMatches:1) and :has() was supported -- the rule simply was not live.
# Appending to an existing style block means inheriting whatever at-rule is open
# at that point; check the brace balance before trusting an anchor.
ABCUT_STYLE = ('<style id="sf-ab-cut">'
               # PRIMARY = the two skips beside play/pause. Everything else is
               # demoted behind a hairline so the eye lands on transport first.
               '.sf-ab-sec{display:flex;align-items:center;gap:1px;'
               'margin-left:9px;padding-left:9px;'
               'border-left:1px solid rgba(255,255,255,.13);}'
               '.sf-ab-sec .sf-ab-btn{opacity:.58;transform:scale(.86);}'
               '.sf-ab-sec .sf-ab-btn:hover{opacity:1;}'
               '.sf-ab-i{font-size:23px;line-height:1;}'
               '.sf-ab-pre{display:flex;align-items:center;}'
               # the narrow-screen trims target .sf-ab-wrap; the pre-wrap holds a
               # primary control and must shrink with it or the bar overflows.
               '@media (max-width:400px){.nowPlayingBar .sf-ab-pre .sf-ab-btn'
               '{min-width:30px;padding:0 3px;}}'
               '@media (max-width:400px){.sf-ab-sec{margin-left:5px;padding-left:5px;}}'
               # Drop the heart and the cast button while a BOOK is playing.
               # Favouriting is a library action and already lives on the book page;
               # casting a 13-hour m4b is not a mid-chapter reach.
               # Gated on :has(.sf-ab-wrap) rather than a class we add: the wrap is
               # built ONLY for AudioBook items, so music keeps both, and the rule
               # stops applying by itself when the bar swaps to a song.
               # The favourite button is matched by its ICON class -- its own classes
               # are shared with controls we are keeping. Both states covered.
               '.nowPlayingBar:has(.sf-ab-wrap) .sf-cast-btn,'
               # The favourite button is OURS -- .sf-np-fav -- so match that directly.
               # Two earlier attempts keyed off the icon
               # (`:has(> .material-icons.favorite_border)`) and both silently missed:
               # the icon carries the name as LIGATURE TEXT, not as a class --
               # `<span class="material-icons">favorite_border</span>` -- so there is
               # no .favorite_border class to select. Reading the element's real
               # outerHTML settled in one look what two guesses could not.
               # The heart carries NO distinguishing class of its own -- it is
               # `mediaButton paper-icon-button-light emby-button`, all shared with
               # controls we keep. Its CONTAINER is the handle:
               # .nowPlayingBarUserDataButtons. Three selectors were guessed before
               # this (.material-icons.favorite_border, .sf-np-fav,
               # .emby-ratingbutton) and each shipped, deployed and did nothing.
               # Dumping the untruncated className + parent of every visible control
               # answered it in one run -- do that FIRST next time.
               '.nowPlayingBar:has(.sf-ab-wrap) .nowPlayingBarUserDataButtons,'
               '.nowPlayingBar:has(.sf-ab-wrap) .sf-np-fav,'
               # ...and Jellyfin's OWN rating button. There are TWO hearts in this
               # bar: ours (.sf-np-fav) and the native .emby-ratingbutton. Hiding
               # only ours left the count at 12 with a heart still on screen, which
               # read exactly like "the rule does not work" -- it worked, on the
               # wrong one of two identical-looking controls.
               # Matched by class, never by title: title="Add to favorites" is
               # translated, and keying off an English string is what once removed
               # every audiobook control for the German and Chinese profiles.
               '.nowPlayingBar:has(.sf-ab-wrap) .emby-ratingbutton'
               '{display:none!important;}'
               '</style>')

AVPICKER_MARKER = 'sf-avatar-picker'
# Lets every user choose their own profile picture from the icon pack served at
# /web/avatars/<category>/<name>.png (manifest.json lists the categories).
#
# Two things it fixes at once:
#   * Jellyfin's header button renders a generic `person` glyph and never the
#     user's own picture, so a chosen avatar was invisible where people actually
#     look for it. The <img> is appended alongside that glyph and the glyph is
#     hidden only once the image has actually LOADED -- on error the glyph comes
#     back, so a user with no picture is unchanged rather than left with a gap.
#   * Jellyseerr needs nothing at all: it renders avatars through
#     /avatarproxy/<jellyfinUserId>, which proxies the Jellyfin image, so it
#     follows automatically (verified: identical bytes from both).
#
# The upload goes through a canvas rather than fetching raw bytes: it normalises
# whatever the source icon is to a 256x256 PNG and hands over the base64 body
# Jellyfin's image endpoint expects. Same origin, so the canvas is not tainted.
#
# An interval, not another whole-body MutationObserver -- the drawer and header
# are rebuilt on navigation, and this page already carries a lot of observers.
AVPICKER_STYLE = ('<style id="sf-avatar-picker-css">'
                  # Match the profile button to the OTHER boxes in the Abyss header.
                  # Measured siblings (sync / language / search) at 1440: 41x41,
                  # border-radius 12px, transparent background, 24.8px glyph. The user
                  # button was the odd one out -- 55x55 at radius 50px (a circle), and
                  # Jellyfin's inner .headerUserButtonRound carried a stray
                  # transform:scale(1.8) from elsewhere in the stack, which is why a
                  # 38px picture rendered 68px and overflowed its own button. That
                  # transform is cancelled rather than compensated for, so the size here
                  # is the size on screen.
                  # The picture fills the WHOLE box (cover + inherit the 12px radius)
                  # instead of sitting as a small circle inside it, which is what made it
                  # read as small next to the glyphs.
                  '.headerUserButton{width:41px!important;height:41px!important;'
                  'border-radius:12px!important;padding:0!important;overflow:hidden!important;'
                  'display:flex!important;align-items:center;justify-content:center;'
                  'transition:box-shadow .16s ease;}'
                  # The icons are circular BADGES -- measured, every corner pixel is
                  # alpha 0 and 21% of each image is transparent, which is 1-pi/4 exactly,
                  # a circle inscribed in a square. So at 100% the picture still read as a
                  # round blob inside a square box, unlike its glyph neighbours.
                  # Zooming it slightly past the edge fills the corners and makes it a
                  # box. The number is geometry, not taste: for a rounded square of side S
                  # with radius r, the farthest point of the corner arc from the centre is
                  # sqrt(2*(S/2-r)^2)+r, so at S=41 r=12 the circle has to be ~117% to
                  # reach it. 118% covers with almost nothing cropped off the character.
                  '.headerUserButton>.headerUserButtonRound{width:100%!important;'
                  'height:100%!important;border-radius:12px!important;'
                  'transform:none!important;margin:0!important;padding:0!important;'
                  'background-color:rgba(255,255,255,.08);'
                  'background-size:118%!important;background-position:center!important;'
                  'background-repeat:no-repeat!important;}'
                  '.headerUserButton:hover,.headerUserButton:focus-visible{'
                  'box-shadow:inset 0 0 0 2px rgba(255,255,255,.85);}'
                  # no picture yet: keep Jellyfin's glyph, sized like its neighbours
                  '.headerUserButton>.material-icons{font-size:24.8px!important;}'
                  # phones: siblings measure 37x37 but KEEP the 12px radius, so only the
                  # box size changes here -- an earlier 10px made it subtly rounder than
                  # every button beside it.
                  '@media (max-width:600px){.headerUserButton{width:37px!important;'
                  'height:37px!important;}}'
                  # fallback only, for the moment before Jellyfin has re-rendered the
                  # header for a user who had no picture at all
                  '.sf-hdr-av{width:100%;height:100%;border-radius:12px;'
                  'object-fit:cover;display:block;background:rgba(255,255,255,.08);'
                  'transform:scale(1.18);}'
                  '.sf-avp{position:fixed;inset:0;z-index:100000;background:rgba(0,0,0,.72);'
                  'backdrop-filter:blur(6px);display:flex;align-items:center;justify-content:center;}'
                  '.sf-avp-box{width:min(920px,92vw);height:min(78vh,720px);background:#141518;'
                  'border-radius:16px;display:flex;flex-direction:column;overflow:hidden;'
                  'box-shadow:0 24px 70px rgba(0,0,0,.6);}'
                  '.sf-avp-head{display:flex;align-items:center;justify-content:space-between;'
                  'padding:18px 22px 12px;}'
                  '.sf-avp-title{font-size:1.25em;font-weight:600;color:#fff;}'
                  '.sf-avp-x{background:none;border:0;color:#bbb;font-size:1.9em;line-height:1;'
                  'cursor:pointer;padding:0 6px;}'
                  '.sf-avp-x:hover{color:#fff;}'
                  '.sf-avp-tabs{display:flex;gap:8px;overflow-x:auto;padding:0 22px 12px;'
                  'scrollbar-width:none;}'
                  '.sf-avp-tabs::-webkit-scrollbar{display:none;}'
                  '.sf-avp-tab{flex:0 0 auto;background:rgba(255,255,255,.08);border:0;color:#ddd;'
                  'padding:7px 15px;border-radius:999px;cursor:pointer;font-size:.9em;white-space:nowrap;}'
                  '.sf-avp-tab.on{background:#fff;color:#111;font-weight:600;}'
                  '.sf-avp-grid{flex:1;overflow-y:auto;display:grid;padding:6px 22px 22px;gap:16px;'
                  'grid-template-columns:repeat(auto-fill,minmax(96px,1fr));align-content:start;}'
                  '.sf-avp-cell{border:0;background:none;padding:0;cursor:pointer;border-radius:50%;'
                  'position:relative;aspect-ratio:1;}'
                  '.sf-avp-cell img{width:100%;height:100%;border-radius:50%;display:block;'
                  'background:rgba(255,255,255,.06);transition:transform .15s ease,box-shadow .15s ease;}'
                  '.sf-avp-cell:hover img{transform:scale(1.07);box-shadow:0 0 0 3px #fff;}'
                  '.sf-avp-cell.sf-avp-busy img{opacity:.4;}'
                  '.sf-avp-cell.sf-avp-on img{box-shadow:0 0 0 3px #fff;}'
                  '.sf-avp-cell.sf-avp-fail img{box-shadow:0 0 0 3px #e05260;}'
                  '.sf-avp-empty{color:#999;padding:20px 22px;}'
                  # deliberately no layout of its own -- it must inherit whatever
                  # Jellyfin gives its neighbouring image buttons
                  '.sf-avp-pick{vertical-align:middle;}'
                  '@media (max-width:600px){.sf-avp-box{width:96vw;height:86vh;}'
                  '.sf-avp-grid{grid-template-columns:repeat(auto-fill,minmax(74px,1fr));gap:12px;}}'
                  '</style>')
AVPICKER_SCRIPT = r"""<script>(function(){
/* sf-avatar-picker */
var data=null,busy=false;
function tr(s){try{return (window.sfTr?window.sfTr(s):s)||s;}catch(e){return s;}}
function uid(){try{var a=window.ApiClient;return (a&&a.getCurrentUserId)?a.getCurrentUserId():'';}catch(e){return '';}}
/* Jellyfin draws the avatar itself once the user has one -- an inner
   .headerUserButtonRound div with the picture as its background. An <img> of our
   own next to it meant TWO avatars inside one 58px button. So: when that div is
   present it is the only thing we touch (just re-point its background after a
   pick, so the change shows without a reload); the <img> survives purely as the
   fallback for the seconds before Jellyfin re-renders for someone who had no
   picture at all. */
/* sf-avp-repaint: Jellyfin paints the avatar ONCE, from the user object it held
   when the view rendered, and never re-reads it. Measured after a successful
   pick: the server had the new PrimaryImageTag while the profile page's #image
   was still backgroundImage:none and the header had no avatar element at all --
   so nothing changed until a manual reload. Every surface is therefore repainted
   by us. The ?v= stamp matters as much as the repaint: the image URL is otherwise
   identical between two different pictures and the browser would serve the old
   bytes from cache. */
function avUrl(){
/* sf-avp-optimistic: prefer the icon the user just clicked. It is already
   decoded in the grid, so painting it is instant, where waiting for the round
   trip (fetch -> canvas -> POST -> Jellyfin writes the image) measured 6-9
   SECONDS before anything changed on screen and read as "nothing happened".
   Cleared again if the upload fails, so a picture is never left showing that
   the server did not accept. */
if(window.__sfAvLocal)return window.__sfAvLocal;
var ac=window.ApiClient;
return ac.getUrl('Users/'+uid()+'/Images/Primary')+'?v='+(window.__sfAvV||0);
}
function repaint(){
var ac=window.ApiClient;
if(!ac||!ac.getUrl||!uid())return;
if(!window.__sfAvV)return;   /* nothing picked this session -- leave Jellyfin's own render alone */
var url=avUrl(),els=document.querySelectorAll('#userProfilePage #image, .userProfileImage'),i,e;
for(i=0;i<els.length;i++){
e=els[i];
if(e.getAttribute('data-sfav')===url)continue;
e.setAttribute('data-sfav',url);
e.style.backgroundImage="url('"+url+"')";
e.style.backgroundSize='cover';
e.style.backgroundPosition='center';
}
}
function paintHeader(){
var b=document.querySelector('.headerUserButton');
if(!b)return;
var u=uid();if(!u)return;
var ac=window.ApiClient;if(!ac||!ac.getUrl)return;
var src=avUrl();
var own=b.querySelector('.headerUserButtonRound');
var img=b.querySelector('img.sf-hdr-av');
if(own){
if(img&&img.parentNode)img.parentNode.removeChild(img);
if(own.getAttribute('data-s')!==src){
own.setAttribute('data-s',src);
own.style.backgroundImage="url('"+src+"')";
}
return;
}
if(!img){
img=document.createElement('img');
img.className='sf-hdr-av';img.alt='';img.style.display='none';
img.addEventListener('load',function(){
img.style.display='';
var g=b.querySelector('.material-icons');if(g)g.style.display='none';});
img.addEventListener('error',function(){
img.style.display='none';
var g=b.querySelector('.material-icons');if(g)g.style.display='';});
b.appendChild(img);
}
if(img.getAttribute('data-s')!==src){img.setAttribute('data-s',src);img.src=src;}
}
function close(){var o=document.querySelector('.sf-avp');if(o&&o.parentNode)o.parentNode.removeChild(o);}
function apply(url,cell){
if(busy)return;busy=true;cell.classList.add('sf-avp-busy');
/* paint it NOW, then let the upload catch up */
var prevLocal=window.__sfAvLocal||null,prevV=window.__sfAvV||0;
window.__sfAvLocal=url;window.__sfAvV=Date.now();
var sel=document.querySelectorAll('.sf-avp-cell.sf-avp-on'),q;
for(q=0;q<sel.length;q++)sel[q].classList.remove('sf-avp-on');
cell.classList.add('sf-avp-on');
try{repaint();paintHeader();}catch(x){}
/* sf-avp-closefast: close NOW, not when the upload returns. The picture is
   already on screen (painted from the clicked icon), so waiting on
   fetch -> canvas -> POST kept the grid sitting there for seconds after the
   choice was made -- "it lingers". The upload carries on in the background and
   only reappears if it fails, by putting the previous picture back. */
close();
var im=new Image();
im.onload=function(){
try{
var c=document.createElement('canvas');c.width=256;c.height=256;
var g=c.getContext('2d');g.clearRect(0,0,256,256);g.drawImage(im,0,0,256,256);
var d=c.toDataURL('image/png');
var b64=d.substring(d.indexOf(',')+1);
var ac=window.ApiClient;
ac.ajax({type:'POST',url:ac.getUrl('Users/'+uid()+'/Images/Primary'),
data:b64,contentType:'image/png'}).then(function(){
try{localStorage.setItem('sf-avp-pick',url);}catch(x){}
busy=false;
cell.classList.remove('sf-avp-busy');
repaint();paintHeader();
},function(){
/* upload refused -- put back whatever was showing before */
window.__sfAvLocal=prevLocal;window.__sfAvV=prevV||Date.now();
busy=false;cell.classList.remove('sf-avp-busy','sf-avp-on');
cell.classList.add('sf-avp-fail');
try{repaint();paintHeader();}catch(x){}
setTimeout(function(){cell.classList.remove('sf-avp-fail');},1600);});
}catch(e){busy=false;cell.classList.remove('sf-avp-busy');}
};
im.onerror=function(){
window.__sfAvLocal=prevLocal;window.__sfAvV=prevV||Date.now();
busy=false;cell.classList.remove('sf-avp-busy','sf-avp-on');
try{repaint();paintHeader();}catch(x){}};
im.src=url;
}
function render(ov,cat){
var grid=ov.querySelector('.sf-avp-grid');
grid.innerHTML='';
var tabs=ov.querySelectorAll('.sf-avp-tab'),i;
for(i=0;i<tabs.length;i++)tabs[i].classList.toggle('on',tabs[i].getAttribute('data-c')===cat.id);
if(!cat.icons||!cat.icons.length){
var e=document.createElement('div');e.className='sf-avp-empty';e.textContent=tr('Nothing here yet');
grid.appendChild(e);return;
}
for(i=0;i<cat.icons.length;i++){
(function(name){
var url='avatars/'+cat.id+'/'+name+'.png';
var b=document.createElement('button');
b.type='button';b.className='sf-avp-cell';b.title=name.split('-').join(' ');
var cur='';try{cur=localStorage.getItem('sf-avp-pick')||'';}catch(x){}
if(cur===url)b.classList.add('sf-avp-on');
var im=document.createElement('img');
im.loading='lazy';im.alt=name;im.src=url;
b.appendChild(im);
b.addEventListener('click',function(){apply(url,b);});
grid.appendChild(b);
})(cat.icons[i]);
}
}
function build(ov){
var tabs=ov.querySelector('.sf-avp-tabs'),i;
tabs.innerHTML='';
for(i=0;i<data.categories.length;i++){
(function(cat){
var t=document.createElement('button');
t.type='button';t.className='sf-avp-tab';t.textContent=cat.label;
t.setAttribute('data-c',cat.id);
t.addEventListener('click',function(){render(ov,cat);});
tabs.appendChild(t);
})(data.categories[i]);
}
render(ov,data.categories[0]);
}
function open(){
if(document.querySelector('.sf-avp'))return;
var ov=document.createElement('div');
ov.className='sf-avp';
ov.innerHTML='<div class="sf-avp-box"><div class="sf-avp-head">'
+'<span class="sf-avp-title"></span>'
+'<button type="button" class="sf-avp-x" aria-label="Close">&#215;</button>'
+'</div><div class="sf-avp-tabs"></div><div class="sf-avp-grid"></div></div>';
ov.querySelector('.sf-avp-title').textContent=tr('Choose your picture');
document.body.appendChild(ov);
ov.addEventListener('click',function(e){if(e.target===ov)close();});
ov.querySelector('.sf-avp-x').addEventListener('click',close);
if(data){build(ov);return;}
var g=ov.querySelector('.sf-avp-grid');
g.innerHTML='<div class="sf-avp-empty">'+tr('Loading...')+'</div>';
fetch('avatars/manifest.json',{cache:'no-cache'}).then(function(r){return r.json();})
.then(function(j){data=j;build(ov);})
.catch(function(){g.innerHTML='<div class="sf-avp-empty">'+tr('Could not load the picture pack')+'</div>';});
}
window.sfOpenAvatarPicker=open;
/* sf-avp-profilebtn: the picker sits on the Profile settings page -- Settings >
   Profile, which is exactly where the header button lands. Jellyfin's own
   .imagePlaceHolder there is an upload target with a full-size
   <input type="file"> laid over it, so this is a SEPARATE button underneath
   rather than a hijack of that click: "upload your own picture" keeps working.
   Swept over every #userProfilePage and skipped unless it is actually on screen,
   because this build keeps a cached copy of each visited view in the DOM. */
function addProfileBtn(){
var pages=document.querySelectorAll('#userProfilePage'),i,p,host;
for(i=0;i<pages.length;i++){
p=pages[i];
if(!p.getClientRects().length)continue;
if(p.querySelector('.sf-avp-pick'))continue;
host=p.querySelector('.imagePlaceHolder');
if(!host||!host.parentNode)continue;
/* sf-avp-align: a plain sibling BUTTON, no wrapper. Jellyfin's own image
   buttons ("Add Image" / "Delete Image" -- two buttons that swap, one always
   carrying `hide`) are direct children of the username block with their own
   0.3em margin. Wrapping ours in a div made it a block-level element on its own
   line with different margins, which is why it did not line up with Delete
   Image. Same element type, same classes, same parent, no extra styling: it
   inherits their layout instead of competing with it.
   Text-only for the same reason -- its neighbours carry no icon.
   .readOnlyContent itself is a flex ROW (avatar | name block), so this must go
   in the username block, never after .imagePlaceHolder, or it becomes a third
   column wedged between the avatar and the name. */
var btn=document.createElement('button');
btn.type='button';
btn.className='emby-button raised sf-avp-pick';
btn.textContent=tr('Choose from icons');
btn.addEventListener('click',function(e){e.preventDefault();open();});
var nm=p.querySelector('h2.username');
var box=nm?nm.parentElement:null;
if(box)box.appendChild(btn);
else host.parentNode.insertBefore(btn,host.nextSibling);
}
}
/* The header button deliberately keeps Jellyfin's own behaviour -- it opens
   Settings, and the picker lives one step further in, on the Profile page. An
   earlier build claimed this click in the capture phase; that is gone. */
function tick(){try{addProfileBtn();paintHeader();repaint();}catch(e){}}
setInterval(tick,1500);tick();
})();</script>"""

MOBILEPLAYER_MARKER = 'jf-mobile-player'
MOBILEPLAYER_STYLE = ('<style id="jf-mobile-player">'
                      # ---- structural, ALL widths -------------------------------
                      # .appfooter ships margin:24px + radius:24px = floating pill
                      # sitting 24px off the bottom with content visible underneath.
                      '.appfooter{margin:0!important;border-radius:14px 14px 0 0!important;}'
                      '.nowPlayingBar{padding:6px 0!important;position:relative!important;}'
                      # margin-top:24px was dead space left from when the slider was a row
                      '.nowPlayingBarTop{margin:0!important;padding:6px 14px 0!important;}'
                      '.nowPlayingBarPositionContainer{position:absolute!important;'
                      'top:0;left:0;right:0;height:4px!important;padding:0!important;'
                      'margin:0!important;z-index:2;}'
                      '.nowPlayingBarPositionSlider{height:4px!important;}'
                      # The visible track is NOT the <input>: it is
                      # .mdl-slider-background-flex-container > .mdl-slider-background-flex
                      # (grey rgb(77,77,77)). Sizing only the wrapper left that painting
                      # element at ~1.5px, so the bar looked absent. Size it explicitly.
                      # MDL CENTRES the track rather than filling: the flex-container is
                      # position:absolute;top:50%;padding:0 .54em and the flex itself is
                      # height:.2em;margin-top:-.1em;top:50%. Setting height:100% while
                      # leaving top:50% pushed the track BELOW the 3px box -- it happened
                      # to look right at desktop em sizes but landed outside the box on
                      # iOS, hence "no progress bar". Neutralise the centring too, and
                      # drop the .54em inset so the hairline runs edge to edge.
                      '.nowPlayingBarPositionContainer .mdl-slider-background-flex-container'
                      '{top:0!important;height:100%!important;padding:0!important;}'
                      '.nowPlayingBarPositionContainer .mdl-slider-background-flex'
                      '{top:0!important;margin-top:0!important;height:100%!important;}'
                      '.nowPlayingBarPositionContainer .mdl-slider-background-flex-inner'
                      '{height:100%!important;}'
                      # keep the hairline when the header unpins on scroll
                      '.headroom--unpinned .nowPlayingBarPositionContainer'
                      '{display:flex!important;}'
                      # thumb hidden until hover: clean hairline, still scrubbable by mouse
                      '.nowPlayingBarPositionSlider::-webkit-slider-thumb'
                      '{opacity:0;transition:opacity .15s;}'
                      '.appfooter:hover .nowPlayingBarPositionSlider::-webkit-slider-thumb'
                      '{opacity:1;}'
                      # stop is redundant next to pause - back / pause / next only
                      '.nowPlayingBarCenter .stopButton{display:none!important;}'
                      # sf-lyr-dupe: sfCapsuleButtons() adds .sf-lyr-btn on the premise that
                      # Jellyfin's .openLyricsButton is .hide on this build. That stopped
                      # being true -- 10.11.11 shows it, so the capsule carried TWO identical
                      # Lyrics buttons (measured: title="Lyrics" x2). Ours opens the panel;
                      # Jellyfin's routes to a whole page. Keep ours.
                      '.nowPlayingBar .openLyricsButton{display:none!important;}'
                      # Jellyfin picks layout by DEVICE, not width: a real iPhone gets
                      # .layout-mobile even though a 414px desktop window does NOT. On
                      # layout-mobile Jellyfin renders its OWN play/pause inside
                      # .nowPlayingBarRight and hides .nowPlayingBarCenter. We unhide
                      # centre (prev/next live there - nextTrackButton is NOT in the
                      # right cluster on this build), so BOTH play/pause rendered:
                      # "back, play, play, next". Drop the right-cluster duplicate.
                      # NOT related to hiding stopButton - verified that computes
                      # display:none at 0x0 with no reserved space.
                      'html.layout-mobile .nowPlayingBarRight .playPauseButton'
                      '{display:none!important;}'
                      # Jellyfin also hides the overflow menu on layout-mobile; keep it
                      'html.layout-mobile .nowPlayingBarRight .btnToggleContextMenu'
                      '{display:flex!important;}'
                      # ---- 56em: match Jellyfin's OWN hide breakpoint ------------
                      # Jellyfin hides .nowPlayingBarCenter at max-width:56em. Unhiding
                      # only at 45em left 45-56em (720-896px) with NO transport controls
                      # at all. Must mirror 56em exactly.
                      # It is also position:absolute (centred OVER the bar), so the title
                      # ran underneath the buttons; static returns it to flex flow.
                      '@media (max-width:56em){'
                      '.nowPlayingBarCenter{display:flex!important;position:static!important;'
                      'flex:0 0 auto;align-items:center;}'
                      # min-width:auto on a flex item blocks shrinking below content size
                      # sf-cap-title: min-width:0 let the title shrink below its content -- and
                      # because .nowPlayingBarCenter/.nowPlayingBarRight are flex:0 0 auto and
                      # refuse to shrink, the info container absorbed ALL of the overflow and
                      # collapsed to nothing. Measured on a 412px phone: music title 20px wide
                      # ("Rewrite" rendered as "R..."), audiobook title 0px -- the book's name
                      # and author were simply not on screen, and the page showed through the
                      # gap. A FLOOR is what was missing, not the ability to shrink.
                      '.nowPlayingBarInfoContainer{min-width:96px!important;flex:1 1 auto!important;}'
                      '.nowPlayingBarText{min-width:0!important;overflow:hidden!important;}'
                      # An audiobook is ONE file: NowPlayingQueue length is 1 (measured), so
                      # prev/next track are dead controls, and a book has no lyrics. Dropping
                      # the three of them is what buys the title its room -- 129px of buttons
                      # that could never do anything.
                      '.nowPlayingBar:has(.sf-ab-wrap) .previousTrackButton,'
                      '.nowPlayingBar:has(.sf-ab-wrap) .nextTrackButton,'
                      '.nowPlayingBar:has(.sf-ab-wrap) .sf-lyr-btn{display:none!important;}'
                      '.nowPlayingBarText>*{overflow:hidden!important;'
                      'text-overflow:ellipsis!important;white-space:nowrap!important;'
                      'display:block!important;}'
                      '}'
                      # ---- 45em: phone-only trimming ----------------------------
                      '@media (max-width:45em){'
                      '.nowPlayingBar{padding:2px 0!important;}'
                      # padding-top keeps the button hover circles off the hairline
                      '.nowPlayingBarTop{height:auto!important;padding:9px 10px 0!important;}'
                      '.nowPlayingBarPositionContainer{height:3px!important;}'
                      '.nowPlayingBarPositionSlider{height:3px!important;}'
                      '.nowPlayingBarCenter .nowPlayingBarCurrentTime{display:none!important;}'
                      # volume is a hardware button on a phone
                      '.nowPlayingBar .muteButton,'
                      '.nowPlayingBarVolumeSliderContainer{display:none!important;}'
                      '.nowPlayingBarCenter .mediaButton,'
                      '.nowPlayingBarRight .mediaButton{width:2.4em!important;height:2.4em!important;}'
                      # .nowPlayingImage ships height:70% -- a PERCENTAGE. The phone rule
                      # sets .nowPlayingBarTop{height:auto}, and a % height against an
                      # auto-height parent resolves to ZERO, so the art vanished
                      # (measured: computed height 0px). Use a fixed em instead.
                      '.nowPlayingBar .nowPlayingImage{height:2.4em!important;'
                      'width:2.4em!important;}'
                      '}'
                      '</style>')

# --- Music > Playlists showed VIDEO playlists (2026-08-04).
# The tab requests /Users/{id}/Items?IncludeItemTypes=Playlist&Recursive=true with
# **no MediaTypes filter and no ParentId**, so it returns every playlist on the
# server. Verified: all 3 of the admin's playlists are MediaType=Video (Seasonal Picks,
# Trending Movies, Watchlist) and all 3 showed under Music. Server-side filtering
# works correctly -- &MediaTypes=Audio returns 0, &MediaTypes=Video returns 3 --
# so the fix is simply to add the filter when the request is made from the music
# route. Stock Jellyfin behaviour, not a plugin.
# Interception point: NOT ApiClient.getJSON/ajax/getItems and NOT window.fetch --
# all three were instrumented and saw nothing. jellyfin-web's newer pages go through
# the @jellyfin/sdk + axios stack, so XMLHttpRequest.prototype.open is the reliable
# hook; fetch is wrapped too as a belt-and-braces fallback.
# --- Ungrouped library listings (2026-08-10). Movies showed 227 of 587 titles and
# Shows 63 of 87, because Jellyfin COLLAPSES items into BoxSet entries held in a
# library's cached child listing -- and those BoxSets are ghosts:
# /Items?IncludeItemTypes=BoxSet&Recursive=true returns 0, yet the listing still
# groups by them. Proof, measured on both libraries: the identical query with
# CollapseBoxSetItems=false returns the full count (587 / 87).
#
# A restart clears the cache (it did on 2026-08-01) but the ghosts came back
# twice, because the Collection Sections plugin recreates the collections on its
# startup task. Its Collection-type sections have been stripped again, but this
# makes the view correct REGARDLESS of whether any collection ever exists --
# which is what was asked for: all movies in the Movies tab, never grouped into
# Action/Drama tiles.
#
# Interception point matters and is not obvious: jellyfin-web's newer pages go
# through @jellyfin/sdk + axios, so XMLHttpRequest.prototype.open is the hook
# that works; fetch is wrapped too as a fallback. Same finding as
# jf-music-playlists.
#
# Deliberately narrow: only /Items requests that already carry ParentId (i.e. a
# library/folder listing) and do not already specify the flag.
NOCOLLAPSE_MARKER = 'jf-no-collapse'
NOCOLLAPSE_SCRIPT = (
    '<script>(function(){ /* jf-no-collapse */'
    'function fix(u){'
    'try{'
    'var s=String(u);'
    'if(s.indexOf("/Items")===-1)return u;'
    # The real library grid query carries NO ParentId -- captured from the wire
    # it is /Users/<id>/Items?SortBy=SortName,ProductionYear&IncludeItemTypes=
    # Movie&Recursive=true&...&Limit=100. Matching on ParentId (the first
    # attempt) therefore never fired. Match on IncludeItemTypes instead, which
    # every library grid sends.
    'if(s.indexOf("IncludeItemTypes=")===-1)return u;'
    'if(s.indexOf("CollapseBoxSetItems")!==-1)return u;'
    'return s+(s.indexOf("?")===-1?"?":"&")+"CollapseBoxSetItems=false";'
    '}catch(e){}'
    'return u;'
    '}'
    'try{'
    'var O=XMLHttpRequest.prototype.open;'
    'XMLHttpRequest.prototype.open=function(m,u){'
    'arguments[1]=fix(u);'
    'return O.apply(this,arguments);'
    '};'
    '}catch(e){}'
    'try{'
    'var F=window.fetch;'
    'if(F){'
    'window.fetch=function(i,init){'
    'try{'
    'if(typeof i==="string"){arguments[0]=fix(i);}'
    'else if(i&&i.url&&fix(i.url)!==i.url){arguments[0]=new Request(fix(i.url),i);}'
    '}catch(e){}'
    'return F.apply(this,arguments);'
    '};'
    '}'
    '}catch(e){}'
    '})();</script>'
)

SCROLLFIX_MARKER = 'jf-scroller-fix'
SCROLLFIX_SCRIPT = r'''<script>(function(){
/* jf-scroller-fix */
function getTrack(scroller){return scroller.querySelector('.itemsContainer, .scrollSlider')||scroller;}
/* Some rows (e.g. Discover on Seerr) render their track with overflow-x:hidden
   set directly on the element we transform. Since a CSS transform repositions
   an element's already-clipped paint output rather than changing what its own
   overflow clips, translating that element only slides its fixed first-page
   clip window off-screen — it never reveals the rest of the row, leaving blank
   space where later cards should be. The fix is the standard viewport/track
   split: the clip must live on an untransformed ancestor (the scroller) while
   the transformed element itself stays overflow:visible so content can slide
   underneath the fixed clip. Applied once per scroller, inline, so rows that
   are already built this way (overflow:visible track) are left untouched. */
function ensureClipModel(scroller,track){
if(track.getAttribute('data-jf-clipfixed'))return;
var ov=getComputedStyle(track).overflowX;
if(ov==='hidden'||ov==='scroll'||ov==='clip'){
scroller.style.setProperty('overflow','hidden','important');
track.style.setProperty('overflow','visible','important');
}
track.setAttribute('data-jf-clipfixed','1');
}
function contentWidth(track){
var kids=track.children;
if(!kids.length)return track.scrollWidth;
var first=kids[0],last=kids[kids.length-1];
return (last.offsetLeft+last.offsetWidth)-first.offsetLeft;
}
function currentOffset(track){
var m=getComputedStyle(track).transform;
if(!m||m==='none')return 0;
var mm=m.match(/matrix\(([^)]+)\)/);
if(!mm)return 0;
var parts=mm[1].split(',').map(function(s){return parseFloat(s);});
return -parts[4]||0;
}
/* maxScroll has to come from RENDERED geometry, not
   contentWidth(track)-scroller.clientWidth. clientWidth INCLUDES the row's
   horizontal padding (Jellyfin rows carry padded-left/padded-right -- ~47.5px a
   side at 1440px wide) while contentWidth is measured in the TRACK's own
   coordinates, which already begin inside that padding. The old formula
   therefore stopped ~95px short and clipped the final card: measured on a
   search row, maxScroll came out 476 when it needed to be 570, leaving the last
   card's right edge 94px past the visible edge. Comparing the last child's
   rendered right edge against the scroller's padding edge is self-correcting --
   it accounts for padding, margins and the current transform without assuming
   any of them, and lands the last card flush with the right padding, mirroring
   the left. */
function maxScrollFor(scroller,track){
var kids=track.children;
if(!kids.length)return 0;
var cs=getComputedStyle(scroller);
var sr=scroller.getBoundingClientRect();
var lr=kids[kids.length-1].getBoundingClientRect();
var visibleRight=sr.right-(parseFloat(cs.paddingRight)||0);
return Math.max(0,currentOffset(track)+(lr.right-visibleRight));
}
function findScroller(btn){
var s=btn.closest('.emby-scroller');
if(s)return s;
var p=btn.parentElement;
for(var i=0;i<5&&p;i++){
var found=p.querySelector('.emby-scroller');
if(found)return found;
p=p.parentElement;
}
return null;
}
/* Jellyfin's own lazy-image loader is normally kicked off by the same
   scroll-handler call we bypass below, so cards scrolled into view for the
   first time are left blank (position correct, no artwork). Force-load any
   .lazy[data-src] card still pending — cheap since a row is at most a
   couple dozen items and they're already in the DOM either way. Each card
   also carries a canvas.blurhash-canvas placeholder layered on top that's
   normally faded out once the real image loads (same broken trigger), so
   without hiding it too the real image stays covered by the blurred canvas. */
function revealLazy(track){
track.querySelectorAll('.lazy[data-src]').forEach(function(el){
var src=el.getAttribute('data-src');
if(!src)return;
el.style.backgroundImage='url("'+src+'")';
el.classList.remove('lazy');
var card=el.closest('.card');
if(card){
card.querySelectorAll('canvas.blurhash-canvas').forEach(function(c){
c.style.transition='opacity .2s';
c.style.opacity='0';
});
}
});
}
/* Jellyfin derives the arrows' disabled state from scrollLeft, which NEVER
   changes here because this fix positions the row with transform instead. The
   result: once you page right, Jellyfin leaves the LEFT arrow disabled=true
   (opacity .3) forever, and a disabled button fires no click at all -- so the
   click never even reaches our handler and the row is stuck at the right-hand
   end, only recoverable with a mouse wheel. Since we own the position, we own
   the button state too. */
function syncArrows(btn,offset,maxScroll){
try{
var box=btn.parentElement;
if(!box)return;
var l=box.querySelector('.emby-scrollbuttons-button[data-direction="left"]');
var r=box.querySelector('.emby-scrollbuttons-button[data-direction="right"]');
if(l)l.disabled=offset<=1;
if(r)r.disabled=offset>=maxScroll-1;
}catch(e){}
}
function onClick(e){
var btn=e.target.closest('.emby-scrollbuttons-button');
if(!btn)return;
var dir=btn.getAttribute('data-direction');
if(dir!=='left'&&dir!=='right')return;
var scroller=findScroller(btn);
if(!scroller)return;
var track=getTrack(scroller);
if(!track)return;
e.stopImmediatePropagation();
e.preventDefault();
/* sf-arrow-native-first (2026-08-30). These rows are given overflow-x:auto
   elsewhere in this patch, so most of them can scroll for real, and a second
   handler already drives them that way off their true scrollLeft. Moving them
   with a transform on top of that pinned scrollLeft at 0, which is what left the
   arrows describing a row that was not on screen. Where native scrolling is
   available it wins, and this fix stays for the surfaces that genuinely cannot
   scroll (Discover on Seerr, search results). */
try{if(getComputedStyle(scroller).overflowX==='auto'&&scroller.scrollWidth>scroller.clientWidth+4)return;}catch(nf){}
ensureClipModel(scroller,track);
var viewport=scroller.clientWidth||600;
var maxScroll=maxScrollFor(scroller,track);
var cur=currentOffset(track);
var step=Math.round(viewport*0.9);
var next=dir==='right'?Math.min(maxScroll,cur+step):Math.max(0,cur-step);
track.style.transition='transform .3s ease';
track.style.transform='translateX('+(-next)+'px)';
revealLazy(track);
syncArrows(btn,next,maxScroll);
/* Jellyfin may re-evaluate the buttons after its own (bypassed) handler would
   have run, so re-assert once the transition has settled. */
setTimeout(function(){syncArrows(btn,next,maxScroll);},350);
}
document.addEventListener('click',onClick,true);

/* Touch/swipe support: mobile has no hover state, so the arrow buttons above
   are typically not the primary interaction — a swipe is expected. But the
   scroller isn't a native overflow-scroll container (overflow-x:visible; the
   track is positioned purely via the transform we manage above), so without
   this a touch drag does nothing and mobile users get stuck on page one with
   no way to reach the rest of a row. */
var touchAttached=(typeof WeakSet!=='undefined')?new WeakSet():null;
function attachTouch(scroller){
if(touchAttached){if(touchAttached.has(scroller))return;touchAttached.add(scroller);}
else{if(scroller.getAttribute('data-jf-touch'))return;scroller.setAttribute('data-jf-touch','1');}
var track=getTrack(scroller);
ensureClipModel(scroller,track);
var startX=0,startY=0,startOffset=0,dragging=false,moved=false;
scroller.addEventListener('touchstart',function(e){
if(e.touches.length!==1)return;
startX=e.touches[0].clientX;startY=e.touches[0].clientY;
startOffset=currentOffset(track);
dragging=true;moved=false;
track.style.transition='none';
},{passive:true});
scroller.addEventListener('touchmove',function(e){
if(!dragging)return;
var dx=e.touches[0].clientX-startX;
var dy=e.touches[0].clientY-startY;
if(!moved){
if(Math.abs(dx)<10&&Math.abs(dy)<10)return;
if(Math.abs(dy)>Math.abs(dx)){dragging=false;return;}
moved=true;
}
e.preventDefault();
var viewport=scroller.clientWidth||600;
var maxScroll=maxScrollFor(scroller,track);
var next=Math.min(maxScroll,Math.max(0,startOffset-dx));
track.style.transform='translateX('+(-next)+'px)';
},{passive:false});
scroller.addEventListener('touchend',function(){
if(!dragging)return;
dragging=false;
track.style.transition='transform .2s ease';
if(!moved)return;
var viewport=scroller.clientWidth||600;
var step=Math.round(viewport*0.9)||1;
var maxScroll=maxScrollFor(scroller,track);
var cur=currentOffset(track);
var page=Math.round(cur/step);
var next=Math.min(maxScroll,Math.max(0,page*step));
track.style.transform='translateX('+(-next)+'px)';
revealLazy(track);
});
}
function scanTouch(){document.querySelectorAll('.emby-scroller').forEach(attachTouch);}
var touchObs=new MutationObserver(scanTouch);
touchObs.observe(document.body,{childList:true,subtree:true});
scanTouch();
})();</script>'''

# --- Play-loading overlay: pressing play (from a card's overlay button, or the
# detail page's Play/Resume button) gives NO reliable visual feedback while the
# server negotiates playback -- on a slow connection this can take several
# seconds to over a minute, during which the browsing UI stays fully visible
# and interactive, so it feels like nothing happened. Root-caused two things:
# (1) the existing jf-no-home-spinner fix (below) hides Jellyfin's own
# body-direct-child .docspinner on the home page to kill an unrelated
# annoyance (a spinner flashing on every home page load) -- but Jellyfin
# reuses that exact same spinner instance for "starting playback from a home
# row card", so that earlier fix was inadvertently also silencing the ONLY
# feedback this scenario had. (2) On the detail page the spinner does appear,
# but it's tiny (74x74), positioned wherever Jellyfin happens to place it, and
# the page underneath stays fully visible/scrollable -- and Jellyfin's own
# spinner has been observed to disappear without the video ever loading
# (likely a client-side timeout unrelated to whether playback actually
# started), silently reverting to "looks like nothing happened" with no error.
# Fix: don't rely on detecting Jellyfin's spinner at all. Hook the actual
# button click directly (capture phase, so it fires before Jellyfin's own
# handler) and drive our own full-screen overlay independently -- shown the
# instant the click happens, removed only once we've actually reached the
# video page, with a stall message if that takes unusually long rather than
# silently vanishing.
DEDUPEPAGING_MARKER = 'jf-dedupe-paging'
DEDUPEPAGING_SCRIPT = r'''<script>(function(){
/* jf-dedupe-paging */
/* Every list-type page (Playlists, Collections, Movies, etc.) renders the
   same "X-Y of Z" item-count widget TWICE with the identical .listPaging
   class -- once in the top toolbar, once again as a bottom footer -- with
   nothing to functionally distinguish them (confirmed live: neither ever
   contains actual prev/next buttons, checked on both a 2-item and a
   259-item list). Hiding .listPaging outright via CSS removes BOTH
   (they share one class), so this instead keeps the first (top) one and
   hides only text-identical later ones, run on an interval since this is
   an SPA and the list re-renders on every navigation. */
function dedupe(){
var all=document.querySelectorAll('.listPaging');
if(all.length<2)return;
var first=all[0],firstText=first.textContent.trim();
for(var i=1;i<all.length;i++){
if(all[i].textContent.trim()===firstText)all[i].style.display='none';
}
}
setInterval(dedupe,500);
})();</script>'''

CRASHRECOVERY_MARKER = 'jf-crash-recovery'
CRASHRECOVERY_SCRIPT = r'''<script>(function(){
/* jf-crash-recovery */
/* A malformed/incomplete deep link -- e.g. #/list?type=favorites without
   the parentId a real click into that page would always include -- throws
   an uncaught "item or serverId cannot be null" from Jellyfin's own list
   page chunk and leaves a blank, unrecoverable page with no error message.
   Confirmed live on multiple #/list?type=X variants; the crash is in
   stock/minified Jellyfin code we can't safely patch at the source, so
   this catches that specific failure globally and bounces to home instead
   of leaving a dead page. Scoped to this one known message so it can't
   mask or redirect on unrelated errors. */
window.addEventListener('error',function(e){
if(e&&e.message&&e.message.indexOf('item or serverId cannot be null')>-1){
location.hash='#/home';
}
});
})();</script>'''

MBCSS_MARKER = 'sf-mediabar-css'
MBCSS_LINK = ('<link rel="stylesheet" href="sf-mediabar.css" id="sf-mediabar-css">'
              '<!-- sf-mediabar-css: a LOCAL copy of Media Bar\'s slideshowpure.css.\n'
              '     The plugin injects a <link> to that file on cdn.jsdelivr.net at request\n'
              '     time (File Transformation, so it is not in index.html on disk and cannot\n'
              '     be rewritten here). Two of its declarations lay out the ENTIRE home page:\n'
              '       .homeSectionsContainer { position: relative; top: 65vh; z-index: 6 }\n'
              '       #slides-container      { height: 90% }\n'
              '     Every `top` override we ship is !important, but top does nothing on a\n'
              '     static element -- so a slow or blocked CDN dropped every row to the top of\n'
              '     the page and the hero sprawled behind them. Reproduced by aborting\n'
              '     jsdelivr: first row y=101 instead of 590.\n'
              '     Loading our own copy first means a CDN failure costs nothing; when the CDN\n'
              '     does answer it simply restates the same rules. Refresh this file if the\n'
              '     plugin is ever upgraded. -->')

ITEMCACHE_MARKER = 'sf-item-cache'

ITEMCACHE_SCRIPT = r'''<script>(function(){ /* sf-item-cache */
/* Tap -> audible on the featured hero measured 5,463ms against Spotify Web's
   1.42s. Tracing it request by request showed the cost is not bandwidth and not
   the server being slow -- it is the SAME lookups repeated:

       37ms   GET /Users/{u}/Items/{album}      -> 921ms   (884ms)
       922ms  GET /Users/{u}/Items?ParentId=..  -> 5091ms  (4169ms!)
       2237ms GET /Users/{u}/Items/{album}      -> 3894ms  (1657ms)  <- 2nd
       3895ms GET /Users/{u}/Items?ParentId=..  -> 3969ms  (74ms)    <- 2nd
       4125ms GET /Users/{u}/Items/{track}      -> 4410ms
       4411ms GET /Users/{u}/Items/{album}      -> 4982ms  (571ms)   <- 3rd
       -> audible 5463ms

   The album is fetched THREE times and its track list twice, by Jellyfin's own
   card handler and playback manager. They are SEQUENTIAL, so coalescing
   in-flight duplicates does nothing -- each starts after the last finished.
   That 4,169ms children request is the other half: :8096 is HTTP/1.1, six
   connections, and a music page is saturating them with artwork, so a request
   can sit in the queue for seconds (the identical retry took 74ms).

   So: a very short TTL cache over item lookups. Anything asked for twice inside
   a few seconds cannot meaningfully have changed, and one play action is over
   in well under that.

   Deliberately narrow:
     - GET only
     - only /Users/{uid}/Items... -- item and child lookups
     - NEVER /Images, /universal, /PlaybackInfo, /Sessions, or anything with a
       body, so playback state, streams and writes are untouched
     - 8s TTL, and the whole map is dropped on any POST/DELETE to /Users or
       /Items so a favourite, a played-state change or a playlist edit is never
       served from a stale entry
   Every caller gets response.clone(); the stored response is never read. */
if(window.__sfItemCache)return; window.__sfItemCache=1;
var of=window.fetch;
if(typeof of!=='function')return;
var TTL=8000, map={};
function cacheable(url,method){
if(method!=='GET')return false;
if(url.indexOf('/Items')===-1)return false;
if(/\/Images|\/universal|PlaybackInfo|\/Sessions|\/InstantMix|\/Similar/.test(url))return false;
return true;
}
window.fetch=function(input,init){
var url='',method='GET';
try{
url=(typeof input==='string')?input:((input&&input.url)||'');
method=String((init&&init.method)||(input&&input.method)||'GET').toUpperCase();
}catch(e){return of.apply(this,arguments);}
/* any write invalidates everything -- cheap, and correctness beats a few
   saved milliseconds after a favourite or a playlist edit */
if(method!=='GET'&&/\/(Users|Items|Playlists)/.test(url)){map={};return of.apply(this,arguments);}
if(!cacheable(url,method))return of.apply(this,arguments);
var now=Date.now(),hit=map[url];
if(hit&&(now-hit.t)<TTL){
return hit.p.then(function(r){return r.clone();});
}
var p=of.apply(this,arguments);
map[url]={t:now,p:p};
p.then(function(r){
/* only keep a response worth reusing; an error must not be cached */
if(!r||!r.ok)delete map[url];
},function(){delete map[url];});
return p.then(function(r){return r.clone();});
};
})();</script>'''


BMFIX_MARKER = 'jf-bm-tabs-fix'
# JE's standalone Bookmarks page (#/bookmarks, .sections.bookmarks) renders its
# Movies/Series tabs at y=0 -- underneath Jellyfin's fixed .skinHeader (z-index
# 999, ~101px tall), whose .headerLeft region then intercepts all clicks on
# those tabs (confirmed live: elementFromPoint over the tabs returned .headerLeft,
# not the tab button). Push the whole JE page down so its tabs clear the header
# and become clickable. Scoped to .sections.bookmarks so nothing else is touched;
# padding (not display:none) so it can't trip the Abyss-theme header-collapse gotcha.
BMFIX_STYLE = ('<style id="jf-bm-tabs-fix">'
               '.sections.bookmarks{padding-top:7rem!important;}'
               '</style>')

TYPINGGUARD_MARKER = 'jf-typing-guard'
TYPINGGUARD_SCRIPT = r'''<script>(function(){
/* jf-typing-guard */
/* Jellyfin Enhanced binds single-letter GLOBAL shortcuts (D, Q, R, A, I, S, C,
   V, B, +, -, /). Its handler does not check whether focus sits in a text-entry
   control, so typing into the search box fires them: "q" jumped to Quick
   Connect mid-word, "r" and friends navigated away.

   The shortcuts are useful outside text fields, so this does NOT disable them.
   It swallows the event ONLY while a text-entry control has focus.

   Deliberately narrow:
   - capture phase on window, so it runs before the plugin's own document-level
     listener gets the event;
   - stopPropagation only, never preventDefault, so the character still reaches
     the field and types normally;
   - only plain single-character keys with no ctrl/meta/alt. Enter, Escape, Tab,
     Backspace and the arrows still propagate, so Jellyfin's own field
     behaviour (submit, clear, autocomplete navigation) is untouched. */
function isTextEntry(el){
  if (!el) return false;
  if (el.isContentEditable) return true;
  var tag = (el.tagName || '').toLowerCase();
  if (tag === 'textarea' || tag === 'select') return true;
  if (tag === 'input') {
    var t = (el.type || 'text').toLowerCase();
    /* Only non-text input types are safe to let shortcuts through on. */
    return ['button','checkbox','radio','submit','reset','file','image','range','color']
      .indexOf(t) === -1;
  }
  if (el.closest && el.closest('[contenteditable=""],[contenteditable="true"]')) return true;
  return false;
}

['keydown','keypress','keyup'].forEach(function(evt){
  window.addEventListener(evt, function(e){
    if (e.ctrlKey || e.metaKey || e.altKey) return;   // real chords still work
    if (!e.key || e.key.length !== 1) return;         // Enter/Esc/Tab/arrows pass
    if (!isTextEntry(e.target)) return;               // outside fields: unchanged
    e.stopPropagation();
    if (e.stopImmediatePropagation) e.stopImmediatePropagation();
  }, true);
});
})();</script>'''
# --- Rebrand pre-boot / PWA surfaces (2026-08-02). Once the app boots it
# already shows the server name (LUSERVERSE), but index.html ships a hardcoded
# "Jellyfin" in <title> and application-name. Those are exactly what the browser
# tab shows BEFORE the app loads and what "Add to Home Screen" picks up, which
# is why it still felt like someone else's product.
# Deliberately TARGETED replaces, never a blanket s/Jellyfin/LUSERVERSE/:
# index.html also contains /jellyfin/jellyfin-web asset paths and the comments
# in our own injected patches, and rewriting those would break the page.
# Artwork (logo, favicon, touchicons) is intentionally left stock — the admin likes
# the jellyfish mark; only the name is his.
BRAND = 'LUSERVERSE'


# --- Discover badges (2026-08-19). ------------------------------------------
# The MOVIE / SERIES pills on the Discover row are NOT text in the DOM -- they are
# CSS generated content from the Jellyfin Enhanced plugin
# (.discoverCard-movie::before {content:"Movie"}), which is why every text sweep
# missed them and they sat in English on an otherwise Chinese page. Verified with
# getComputedStyle(el,'::before').content.
# Overridden per language off <html lang>, which Jellyfin sets to "zh-cn" / "de"
# (verified). !important + the extra .discover-card ancestor to beat the plugin.
# --- Touch feedback (2026-08-20). -------------------------------------------
# Jellyfin ships -webkit-tap-highlight-color: rgba(51,181,229,.4) -- a CYAN
# flash -- and it is inherited by every card. Two problems on this build:
#   1. Abyss is monochrome near-white (--abyss-accent: 245,245,247), so a
#      saturated blue flash is the one colour on screen that belongs to nothing;
#   2. the native highlight paints a hard RECTANGLE that ignores border-radius,
#      so tapping a 10px-rounded poster flashed square corners outside the art.
# That is the "highlight doesn't match or fit" report, and it fires on EVERY tap.
# Replaced with a pressed state the theme owns: a small scale-down plus a
# brightness dip, both GPU-cheap transforms/filters rather than a repaint, and
# both inherit the element's own radius because they act on the element itself.
# Scoped to (hover:none) so a mouse keeps Jellyfin's hover behaviour untouched.
# --- Full-screen audiobook player (2026-08-20). -----------------------------
# The capsule was carrying 10 controls on a 412px bar; chapters had already been
# deleted on phones to make room and the title had collapsed to 0px. Splitting
# it is the only shape where chapters, a readable title AND 44px targets all fit:
# the capsule keeps art/title/play/+30, the full player takes the rest.
ABSTAGE_MARKER = 'sf-ab-stage-css'
ABSTAGE_STYLE = ('<style id="sf-ab-stage-css">'
                 # a book has one file: shuffle/prev/next/repeat are dead here,
                 # and there is no album page and no queue to show.
                 '.sf-np-book .sf-np-shuffle,.sf-np-book .sf-np-prev,'
                 '.sf-np-book .sf-np-next,.sf-np-book .sf-np-repeat,'
                 '.sf-np-book .sf-np-tabs,.sf-np-book .sf-np-panel,'
                 '.sf-np-book .sf-np-album{display:none!important;}'
                 # sf-np-typeflash: the type is not knowable yet. Show only what is
                 # correct for BOTH kinds (art, title, scrubber, play/pause) and hide
                 # everything that belongs to one of them, so no wrong control is ever
                 # painted. Resolves on the next 400ms sweep at the latest.
                 '.sf-np-typing .sf-np-tabs,.sf-np-typing .sf-np-album,'
                 '.sf-np-typing .sf-np-shuffle,.sf-np-typing .sf-np-repeat,'
                 '.sf-np-typing .sf-np-prev,.sf-np-typing .sf-np-next{display:none!important;}'
                 '.sf-np-book .sf-np-controls{gap:.45em;flex-wrap:nowrap;}'
                 '.sf-np-book .sf-np-controls .sf-ab-btn{min-width:44px;height:44px;}'
                 '.sf-ab-s-row2{display:flex;gap:1.6em;justify-content:center;'
                 'align-items:center;margin:.35em 0 .1em;}'
                 '.sf-ab-s-row2 .sf-ab-btn{min-width:44px;height:44px;}'
                 '.sf-ab-s-chl{width:100%;max-width:560px;margin:.7em auto 0;'
                 'max-height:34vh;overflow-y:auto;-webkit-overflow-scrolling:touch;}'
                 '.sf-ab-s-chh{font-size:.78em;letter-spacing:.09em;'
                 'text-transform:uppercase;opacity:.55;margin:.1em .3em .45em;}'
                 '.sf-ab-s-chrow{display:flex;align-items:center;gap:.85em;width:100%;'
                 'min-height:52px;background:transparent;border:0;color:inherit;'
                 'padding:.6em .55em;border-radius:10px;text-align:left;cursor:pointer;font:inherit;}'
                 '.sf-ab-s-chrow:active{background:rgba(var(--abyss-accent),.10);}'
                 '.sf-ab-s-now{background:rgba(var(--abyss-accent),.14);}'
                 '.sf-ab-s-chn{opacity:.45;min-width:1.7em;font-variant-numeric:tabular-nums;}'
                 '.sf-ab-s-chname{flex:1 1 auto;overflow:hidden;'
                 'text-overflow:ellipsis;white-space:nowrap;}'
                 '.sf-ab-s-chat{opacity:.5;font-variant-numeric:tabular-nums;font-size:.92em;}'
                 # capsule goes minimal on phones -- these now live in the full player
                 '@media (max-width:700px){'
                 # back-30 STAYS: a mini player with only forward-30 cannot undo a
                 # missed line, which is the single most common thing a listener
                 # reaches for. Speed and the sleep timer are one tap away in the
                 # full player; skipping back is not something to make you open it.
                 '.nowPlayingBar .sf-ab-wrap .sf-ab-rate,'
                 '.nowPlayingBar .sf-ab-wrap .sf-ab-sleep{display:none!important;}'
                 # sf-ab-narrow (2026-08-21): adding the Bookmarks button pushed
                 # the bar 3px past the edge on a 390px iPhone -- "More" measured
                 # right edge 393 against a 390 bar, i.e. the overflow the admin
                 # reported once already. The cluster is 4 buttons at 35.9px
                 # min-width with a 2.2px gap, so trimming both reclaims ~31px:
                 # enough to clear it now and to absorb one more control later.
                 # Height is untouched, and both of these controls also exist at
                 # full size in the expanded player.
                 '@media (max-width:400px){'
                 '.nowPlayingBar .sf-ab-wrap{gap:0;}'
                 '.nowPlayingBar .sf-ab-wrap .sf-ab-btn{min-width:30px;padding:0 3px;}'
                 '}'
                 '}'
                 '</style>')


# --- Music suggestion shelves scroll, not wrap (2026-08-20). ----------------
# Measured on a 412px phone: Jellyfin's music suggestion "rows" are not rows at
# all -- flex-wrap:wrap, so "Recently Added Music" laid 12 cards over SIX lines
# and stood 1454px tall; Recently Played and Frequently Played 970px each. The
# Suggestions tab was ~4400px of scrolling for five shelves, none of which could
# be skimmed. Our own rows next to them are 183-250px single-line scrollers,
# which is why the page reads as two different apps stitched together.
#
# Scoped to .pageTabContent[data-index="1"] -- the Suggestions pane. data-index
# is Jellyfin's own and is identical in every language (the same hook that fixed
# sfMusicLanding). Albums/Artists/Songs are SEPARATE panes and keep their
# wrapping grids, which is correct for a full A-Z library view.
SHELF_MARKER = 'sf-music-shelves'
SHELF_STYLE = ('<style id="sf-music-shelves">'
               '.pageTabContent[data-index="1"] .verticalSection .itemsContainer{'
               'flex-wrap:nowrap!important;overflow-x:auto!important;'
               'overflow-y:hidden!important;-webkit-overflow-scrolling:touch;'
               'scrollbar-width:none;}'
               '.pageTabContent[data-index="1"] .verticalSection .itemsContainer'
               '::-webkit-scrollbar{display:none;}'
               # without a fixed basis a nowrap flex line squashes every card to
               # fit, which is worse than wrapping
               '.pageTabContent[data-index="1"] .verticalSection .itemsContainer>.card{'
               'flex:0 0 auto!important;}'
               '</style>')


TAPFEEL_MARKER = 'sf-tap-feel'
TAPFEEL_STYLE = ('<style id="sf-tap-feel">'
                 'html,body,.card,.cardBox,.cardContent,.cardImageContainer,'
                 '.sf-ml-card,.sf-ml-poster,.emby-button,.paper-icon-button-light,'
                 '.listItem,.itemAction'
                 '{-webkit-tap-highlight-color:transparent!important;}'
                 '@media (hover:none){'
                 '.sf-ml-poster,.cardImageContainer,.cardBox'
                 '{transition:transform .14s ease-out,filter .14s ease-out;}'
                 '.sf-ml-card:active .sf-ml-poster,'
                 '.card:active .cardImageContainer'
                 '{transform:scale(.955);filter:brightness(.82);}'
                 '.sf-mix-card:active,.sf-mus-artist:active'
                 '{transform:scale(.955);filter:brightness(.82);}'
                 '.emby-button:active,.paper-icon-button-light:active,'
                 '.sf-ab-btn:active,.sf-np-b:active{opacity:.55;}'
                 '}'
                 '</style>')


DISCBADGE_MARKER = 'sf-disc-badge-i18n'
DISCBADGE_STYLE = ('<style id="sf-disc-badge-i18n">'
                   'html[lang^="zh"] .discover-card .discoverCard-movie::before'
                   '{content:"\u7535\u5f71"!important;}'      # 电影
                   'html[lang^="zh"] .discover-card .discoverCard-tv::before'
                   '{content:"\u5267\u96c6"!important;}'      # 剧集
                   'html[lang^="de"] .discover-card .discoverCard-movie::before'
                   '{content:"Film"!important;}'
                   'html[lang^="de"] .discover-card .discoverCard-tv::before'
                   '{content:"Serie"!important;}'
                   # sf-disc-abyss: the plugin ships Tailwind colours -- a #FFD700 gold
                   # star (an INLINE style on a .material-icons span, which is why no
                   # stylesheet rule touched it) and rgba(37,99,235,.9) / purple pills.
                   # Abyss is monochrome near-white (--abyss-accent: 245,245,247), so
                   # saturated blue/purple/gold read as foreign chips pasted on top.
                   # Recoloured to the theme's own accent. No backdrop-filter: this row
                   # renders 25 cards on a phone and blur is the expensive part.
                   '.discover-card .cardText-secondary .material-icons'
                   '{color:rgba(var(--abyss-accent),.72)!important;}'
                   '.discover-card [class*="discoverCard-"]::before{'
                   'background:rgba(16,16,16,.66)!important;'
                   'color:rgba(var(--abyss-accent),.94)!important;'
                   'border:1px solid rgba(var(--abyss-accent),.20)!important;'
                   'font-weight:600!important;letter-spacing:.05em!important;}'
                   '</style>')


# --- Visible-view resolver (2026-08-08). ------------------------------------
# Jellyfin's view manager caches ONE VIEW PER URL. Home, Sports and My Stuff are
# three URLs on the same route (#/home, #/home?sports=1, #/home?tab=1), so up to
# three #indexPage elements -- each with its own #homeTab and #favoritesTab --
# legitimately coexist. Duplicate ids are expected; document.getElementById then
# returns whichever copy is first in the DOM, which is frequently the stale one.
#
# Measured with two instances live:
#   instance 0  .hide=true   display:none   decorated=true    <- ours, stale
#   instance 1  .hide=false  display:block  decorated=false   <- on screen
# so the user saw an empty, undecorated My Stuff pane.
#
# Jellyfin marks inactive copies with .hide; '#indexPage:not(.hide)' matched
# exactly one. offsetParent is checked too, so a copy hidden by any other means
# is still rejected.
#
# Injected into <head> so it is defined before every body patch that uses it,
# independent of the order the apply blocks run in. It only defines functions --
# no DOM access at load time -- so running before <body> exists is safe.
SRCCAP_MARKER = 'sf-hero-srccap'
SRCCAP_SCRIPT = r"""<script>(function(){ /* sf-hero-srccap */
if(window.__sfSrcCap)return;
window.__sfSrcCap=1;
/* Media Bar preloads its next slides with detached `new Image()` objects that
   never enter the DOM, so a MutationObserver cannot see them -- measured on a
   cold load: 8 full-size originals fetched here, then the SAME artwork fetched
   again at the capped size once the slide markup was built. Two downloads of
   every backdrop. Capping the URL at the setter catches the preloads and the
   DOM images with one rule, so both ask for the identical URL and the second
   one is a cache hit.

   Deliberately narrow: hero Backdrop/Logo endpoints only, and only when no size
   is already requested -- every other caller in Jellyfin passes fillWidth or
   maxWidth and is left untouched. If the pattern ever fails to match, the URL
   passes through unchanged and the worst case is today's behaviour. */
var d=Object.getOwnPropertyDescriptor(HTMLImageElement.prototype,'src');
if(!d||!d.set)return;
var RX=/\/Items\/[^/]+\/Images\/(Backdrop|Logo)\b/;
function cap(u){
try{
if(typeof u!=='string')return u;
var m=RX.exec(u);
if(!m)return u;
if(u.indexOf('maxWidth=')>-1||u.indexOf('fillWidth=')>-1||u.indexOf('maxHeight=')>-1)return u;
/* the backdrop sits behind a scrim at ~1540 CSS px; 2560 is already a
   downscale from the 3840 originals and is indistinguishable at DPR 2 */
var hi=(window.devicePixelRatio||1)>1;
/* Phones take a smaller backdrop. Measured on an iPhone 17: the hero box is
   422x845 CSS, so 1267x2534 device pixels, and a 16:9 backdrop cropped to that
   tall a slice is ALREADY being upscaled 1.76x at maxWidth=2560 -- the source
   simply has no more vertical resolution to give. Since the picture is soft
   either way, the extra bytes buy almost nothing:

       2560 -> 503KB, 1.76x upscale
       1920 -> 304KB, 2.35x upscale

   40% off the largest asset on the page, which on a 2 Mbps link is the
   difference between roughly 2.0s and 1.2s before the hero appears. The lower
   half of the image is under a scrim and the fade anyway.
   Desktop keeps 2560, where the crop is gentle and the detail is visible. */
var phone=false;
try{phone=window.innerWidth<=520;}catch(e){}
/* PHONES GET THE POSTER, NOT THE BACKDROP.
   The hero box on a phone is 422x845 CSS -- an aspect of 0.50 -- and a 16:9
   backdrop covering that discards 72% of itself. Measured against the item's
   Primary image at the same byte cost:

       backdrop 1920 : 304KB, 28% of pixels survive the crop, 1.76x upscale
       poster   1080 : 315KB, 75% survive,                    1.56x upscale

   So the poster is sharper for the same bytes, and it is composed for a portrait
   frame in the first place rather than being a landscape still cropped to a
   sliver. Matches how Netflix and Disney+ treat a phone hero.

   The backdrop's tag is dropped deliberately: it identifies THAT image, and
   carrying it onto a Primary request would key the cache to the wrong artwork.
   Everything else in the query (quality) is preserved. If an item has no poster
   the request 404s and sfHeroPosterFallback puts the backdrop back. */
if(phone&&m[1]==='Backdrop'){
var idm=u.match(/\/Items\/([^/]+)\/Images\//);
if(idm){
var q=(u.match(/[?&]quality=(\d+)/)||[])[1]||'80';
try{
var base=u.split('/Items/')[0];
/* Art, not Primary. Most TMDB posters carry the title printed on them, and the
   hero already draws the show's Logo over the top, so the title was appearing
   twice. textless.py parks a TMDB "no language" poster in the otherwise unused
   Art slot; this asks for that first and falls back through Primary to Backdrop
   for anything not yet processed. */
/* 900/q55, measured against the alternatives on this server:
       1080 q80 231KB | 1080 q60 140KB | 900 q55 96KB | 720 q50 64KB
   The poster is upscaled to fill the hero either way (1.56x at 1080, 1.87x at
   900) and its lower half sits under the scrim and the fade, so the detail lost
   between those two is not detail anyone sees. 31% fewer bytes, and a smaller
   resize for a NAS that is already CPU-bound. */
return base+'/Items/'+idm[1]+'/Images/Art?quality=55&maxWidth=900';
}catch(e){}
}
}
var w=m[1]==='Logo'?(hi?900:600):(phone?1920:(hi?2560:1920));
return u+(u.indexOf('?')>-1?'&':'?')+'maxWidth='+w;
}catch(e){return u;}
}
Object.defineProperty(HTMLImageElement.prototype,'src',{
configurable:true,
enumerable:d.enumerable,
get:d.get,
set:function(v){try{var c=cap(v);prio(this,c);d.set.call(this,c);}catch(e){d.set.call(this,v);}}
});
/* Media Bar's preloader uses setAttribute, which does NOT go through the
   property setter above -- measured: propSetterCaps true, attrSetterCaps false,
   and the originals kept being fetched. Shadowing setAttribute on the IMAGE
   prototype rather than patching Element.prototype means no other element type
   ever enters this code path. */
var sa=Element.prototype.setAttribute;
Object.defineProperty(HTMLImageElement.prototype,'setAttribute',{
configurable:true,writable:true,enumerable:false,
value:function(n,v){
try{if(n==='src'){var c=cap(v);prio(this,c);return sa.call(this,n,c);}}catch(e){}
return sa.call(this,n,v);
}
});
/* PRIORITY. Media Bar loads the visible slide and its 3 preloads as one
   undifferentiated burst, so the artwork actually on screen queues behind
   artwork nobody can see yet. The first backdrop and logo are marked high, the
   preloads low -- the browser then spends the connection on the slide the user
   is looking at. Nothing is delayed or withheld: only the ORDER changes, so
   there is no way for a preload to be starved or for Media Bar to wait on a
   load that never happens.

   The first backdrop finishing is also the signal the rest of the page waits
   on (see jf-no-lazy), broadcast as an event. */
/* home makes ~380 image requests and the resource-timing buffer defaults to 250,
   so the hero's own entries were being dropped before they could be read -- every
   attempt to time the hero from the page came back empty. Raised here, at the
   only point early enough to matter. */
try{performance.setResourceTimingBufferSize(3000);}catch(e){}
var nB=0,nL=0;
window.__sfHeroPainted=false;
window.__sfHeroPaintedAt=0;
function heroPainted(){
if(window.__sfHeroPainted)return;
window.__sfHeroPainted=true;
try{window.__sfHeroPaintedAt=Math.round(performance.now());}catch(e){}
try{document.dispatchEvent(new Event('sf-hero-painted'));}catch(e){}
}
/* the page must never depend on an image that fails or hangs */
try{setTimeout(heroPainted,2500);}catch(e){}
/* sf-art-cached (2026-09-04): a picture that is already decoded must not be
   faded in again. Keyed by URL because the ELEMENT does not survive: measured
   going Back to Home, Media Bar builds a fresh <img> for the slide, so it
   arrived carrying .sf-art but no .sf-art-in and replayed the full .45s fade
   from black -- the top 60% of the screen went dark for 471ms on every return
   to a page that was already rendered. */
var SF_ART_SEEN=Object.create(null);
function prio(img,u){
try{
/* Fade the artwork in once it has DECODED. Media Bar drops a fresh src on the
   element and the browser paints the JPEG progressively as bytes arrive, which
   is the "flashes in / staggers in" look -- bands of a half-drawn picture, then
   a snap to the finished one. Holding the element transparent until the decode
   completes means one clean transition instead. The container behind it is
   opaque (sf-hero-opaque), so nothing shows through while it waits and the old
   red-flash cannot come back. */
if(!img.__sfFade){
img.__sfFade=1;
img.classList.add('sf-art');
var reveal=function(){
try{if(img.__sfUrl)SF_ART_SEEN[img.__sfUrl]=1;}catch(e){}
img.classList.add('sf-art-in');};
img.addEventListener('load',function(){
if(img.decode)img.decode().then(reveal).catch(reveal);else reveal();});
/* an item with no poster: put the backdrop back rather than show nothing */
/* Art -> Primary -> Backdrop. Art only exists where textless.py has run, and an
   item with no textless variant on TMDB will never have one, so the chain has to
   degrade rather than show an empty hero. Each step is taken at most once. */
img.addEventListener('error',function(){
try{
var cur=img.getAttribute('src')||'';
var idm=cur.match(/\/Items\/([^/]+)\/Images\//);
if(!idm)return;
var base=cur.split('/Items/')[0],id=idm[1];
if(cur.indexOf('/Images/Art')>-1&&!img.__sfArtFell){
img.__sfArtFell=1;
img.setAttribute('src',base+'/Items/'+id+'/Images/Primary?quality=55&maxWidth=900');
return;}
if(cur.indexOf('/Images/Primary')>-1&&!img.__sfFellBack){
img.__sfFellBack=1;
img.setAttribute('src',base+'/Items/'+id+'/Images/Backdrop/0?quality=60&maxWidth=1920');
}
}catch(e){}});
}
img.__sfUrl=u;
/* Two independent signals, because either can be true first: the element is
   already complete (naturalWidth guards the no-src case, where complete is
   also true), or this exact URL was revealed earlier in the session. */
if((img.complete&&img.naturalWidth)||(u&&SF_ART_SEEN[u])){
img.classList.add('sf-art-now');
img.classList.add('sf-art-in');
}
var isB=/\/Images\/(Backdrop|Primary)/.test(u),isL=/\/Images\/Logo/.test(u);
if(!isB&&!isL)return;
var first=isB?(++nB===1):(++nL===1);
img.fetchPriority=first?'high':'low';
if(isB&&first){
img.addEventListener('load',heroPainted);
img.addEventListener('error',heroPainted);
}
}catch(e){}
}
})();</script>"""

# --- sf-coalesce (2026-08-21) -------------------------------------------------
# Tap -> audible on a phone traced request by request: 2,325ms, and the SINGLE
# biggest line in it is Jellyfin fetching the SAME album item TWICE.
#
#     +46ms   GET /Users/<u>/Items/<album>          -> 200 at  +659ms   (613ms)
#     +660ms  GET /Users/<u>/Items?ParentId=<album> -> 200 at  +992ms   (332ms)
#     +1126ms GET /Users/<u>/Items/<track>          -> 200 at +1128ms   (  2ms)
#     +1139ms GET /Users/<u>/Items/<album>  AGAIN   -> 200 at +1723ms  (584ms)
#     +1730ms /Audio/<track>/universal              -> 206 at +1883ms
#     AUDIBLE +2325ms
#
# The repeat is byte-identical to the first and starts 480ms after it finished,
# so it is pure waste -- 584ms, a quarter of the entire wait. It is not cached
# because Jellyfin sends no cache headers on its API at all (verified: no
# Cache-Control, no ETag, no Expires).
#
# So coalesce it in the client: identical GETs for a single item inside a short
# window share one response. Deliberately narrow --
#   * ONLY /Users/<32hex>/Items/<32hex>, the single-item lookup;
#   * ONLY GET;
#   * 2s TTL, so nothing can go stale in a way a person would notice (a
#     favourite toggle or a resume-position write is well outside that window);
#   * every caller gets a clone(), so no one consumes another's body.
# Anything else falls straight through to the original fetch untouched.
COALESCE_MARKER = 'sf-coalesce'
COALESCE_SCRIPT = r"""<script>(function(){ /* sf-coalesce */
if(window.__sfCoalesce)return;
window.__sfCoalesce=1;
var TTL=2000, RX=/\/Users\/[0-9a-f]{32}\/Items\/[0-9a-f]{32}(?:$|\?)/i;
var cache=Object.create(null), orig=window.fetch;
if(typeof orig!=='function')return;
window.fetch=function(input,init){
try{
var url=(typeof input==='string')?input:(input&&input.url)||'';
var m=((init&&init.method)||(input&&input.method)||'GET').toUpperCase();
if(m==='GET'&&RX.test(url)){
var now=Date.now(), hit=cache[url], k;
for(k in cache){if(now-cache[k].t>TTL*3)delete cache[k];}
if(hit&&now-hit.t<TTL){
window.__sfCoalesceHits=(window.__sfCoalesceHits||0)+1;
return hit.p.then(function(r){return r.clone();});
}
var p=orig.apply(this,arguments);
cache[url]={t:now,p:p};
/* Drop a failed request from the cache so an error is never replayed. */
p.then(function(r){if(!r||!r.ok)delete cache[url];},function(){delete cache[url];});
return p.then(function(r){return r.clone();});
}
}catch(e){}
return orig.apply(this,arguments);
};
})();</script>"""
SF_BUILD = '1000000000000001'   # placeholder, replaced with the content hash below
FRESH_MARKER = 'sf-fresh'
FRESH_SCRIPT = ('<script>window.__SF_BUILD="' + SF_BUILD + '";</script>')
FRESH_CHECK = r"""<script>(function(){ /* sf-fresh */
if(window.__sfFresh)return;
window.__sfFresh=1;
var BOOT=Date.now(),NAG=null;
function playing(){
var m=document.querySelectorAll('audio,video'),i;
for(i=0;i<m.length;i++){if(!m[i].paused&&m[i].currentTime>0)return true;}
return false;
}
function busy(){
if(document.hidden)return true;
if(playing())return true;
if(document.querySelector('.dialogContainer,.actionSheet,.sf-ab-menu'))return true;
var d=document.querySelector('.mainDrawer');
if(d&&d.classList.contains('drawer-open'))return true;
return false;
}
function pill(){
if(NAG||document.querySelector('.sf-fresh-pill'))return;
NAG=document.createElement('button');
NAG.type='button';
NAG.className='sf-fresh-pill';
NAG.textContent='Update ready — tap to refresh';
NAG.addEventListener('click',function(){location.reload();});
document.body.appendChild(NAG);
}
function check(){
try{
var url=location.origin+location.pathname+'?sfb='+Date.now();
fetch(url,{cache:'no-store',headers:{Range:'bytes=0-2047'},credentials:'same-origin'})
.then(function(r){return r.text();})
.then(function(txt){
var m=/__SF_BUILD="(\d+)"/.exec(txt||'');
if(!m)return;
if(m[1]===window.__SF_BUILD)return;
if(Date.now()-BOOT<60000)return;      /* never loop straight after a launch */
if(busy()){pill();return;}
location.reload();
}).catch(function(){});
}catch(e){}
}
setInterval(check,180000);
window.addEventListener('focus',function(){setTimeout(check,1200);});
document.addEventListener('visibilitychange',function(){
if(!document.hidden)setTimeout(check,1200);
});
})();</script>"""

# sf-swipe-guard: this shipped as a hand-injected <script> in the running
# container and was never added here, so it existed only in that one file --
# a Jellyfin image update or any rebuild from a pristine index.html would
# have dropped it silently. Body is verbatim from the live page.
SWIPEGUARD_SCRIPT = r'''<script id="sf-swipe-guard">(function(){var sx=0,sy=0,onTitle=false,lock=false;try{document.addEventListener("touchstart",function(e){lock=false;onTitle=false;var t=e.target;if(t&&t.closest&&t.closest(".sectionTitleContainer")){onTitle=true;if(e.touches&&e.touches[0]){sx=e.touches[0].clientX;sy=e.touches[0].clientY;}}},true);document.addEventListener("touchmove",function(e){if(!onTitle||!e.touches||!e.touches[0])return;var dx=Math.abs(e.touches[0].clientX-sx),dy=Math.abs(e.touches[0].clientY-sy);if(lock||(dx>6&&dx>dy)){lock=true;e.stopImmediatePropagation();}},true);document.addEventListener("touchend",function(e){if(lock)e.stopImmediatePropagation();lock=false;onTitle=false;},true);}catch(e){}})();</script>'''



# --- sf-abcard (2026-08-21) --------------------------------------------------
# Every audiobook card printed its title TWICE -- Jellyfin uses Album for the
# primary line and Name for the secondary, and for an audiobook those are the
# same string. Half of every card said nothing.
#
# That line now carries the AUTHOR, which is the thing you actually scan a
# bookshelf for, and series books get their number on the cover so Dungeon
# Crawler Carl 1-8 can be told apart at a glance.
#
# Author rather than narrator on purpose: it needs no translation, so it is
# correct on the German and Chinese profiles without a string table.
#
# One request for the whole shelf, cached in sessionStorage, and only when an
# audiobook card is actually on screen -- so browsing films costs nothing.
ABCARD_MARKER = 'sf-abcard'
ABCARD_SCRIPT = r"""<script>(function(){ /* sf-abcard */
if(window.__sfAbCard)return;
window.__sfAbCard=1;
/* sf-abcard-persist (2026-08-24): this shelf map was cached in sessionStorage,
   so it was rebuilt in every new TAB. Rebuilding is not cheap -- the request
   carries Fields=People, and People is the single most expensive field on this
   server: measured standalone, twice, on an idle box, AudioBook Limit=400 with
   Fields=People took 3.31s/3.21s versus 0.23s/0.22s for Tags or UserData alone.
   The People table holds 93,589 rows and PeopleBaseItemMap is joined per item.
   Under real home load it measured 8.9s and was the heaviest query competing
   with the home rows.
   localStorage makes it once per DAY per browser instead of once per tab.
   Staleness is handled two ways rather than by a short TTL: a 24h stamp, and a
   MISS check -- if a card asks for an id the map does not know (a newly added
   book), the cache is dropped and refetched once. Authors never change for a
   book that is already known, so nothing else can go stale. */
var MAP=null,BUSY=false,KEY='sf-abcard-v4',TTL=86400000,MISSED=false;
function store(o){
try{localStorage.setItem(KEY,JSON.stringify({at:Date.now(),m:o}));}catch(e){
try{sessionStorage.setItem(KEY,JSON.stringify({at:Date.now(),m:o}));}catch(e2){}}
}
function readCache(){
var raw=null;
try{raw=localStorage.getItem(KEY);}catch(e){}
if(!raw){try{raw=sessionStorage.getItem(KEY);}catch(e){}}
if(!raw)return null;
try{
var o=JSON.parse(raw);
if(!o||!o.m||typeof o.at!=='number')return null;
if(Date.now()-o.at>TTL)return null;
return o.m;
}catch(e){return null;}
}
/* a card whose id is not in the map means the shelf grew -- drop and rebuild */
window.__sfAbCardMiss=function(id){
if(MISSED||!MAP||!id)return;
if(MAP[String(id).replace(/-/g,'').toLowerCase()])return;
MISSED=true;MAP=null;
try{localStorage.removeItem(KEY);}catch(e){}
try{sessionStorage.removeItem(KEY);}catch(e){}
};
function load(cb){
if(MAP){cb(MAP);return;}
var hit=readCache();
if(hit){MAP=hit;cb(MAP);return;}
if(BUSY)return;
var c=window.ApiClient;
if(!c||!c.getJSON||!c.getCurrentUserId)return;
BUSY=true;
c.getJSON(c.getUrl('Users/'+c.getCurrentUserId()+'/Items',{
IncludeItemTypes:'AudioBook',Recursive:true,Limit:400,
Fields:'Tags,AlbumArtist'
})).then(function(d){
var out={},items=(d&&d.Items)||[],i,j;
for(i=0;i<items.length;i++){
var it=items[i],au='';
/* sf-abauthor (2026-09-01): the author now comes from AlbumArtist, not People.
   Fields=People was the single slowest request in the whole app -- measured on
   this box, twice, AudioBook Limit=400 with Fields=People took 12.24s/12.52s
   against 0.47s/0.44s for Tags,AlbumArtist. It is on the home critical path
   (the shelf map is built on first paint), and at 12s it also starved the row
   queries behind it on HTTP/1.1: RecentlyAddedMovies measured 8.5s in the
   browser against 0.064s standalone, purely from queueing behind this.
   AlbumArtist is not merely cheaper, it is BETTER DATA: measured over all 208
   books, People carried an Author for 64 of them, AlbumArtist for 190. There
   are exactly 3 books People covers that AlbumArtist does not, against 129 the
   other way. Where both exist they disagree only on spelling variants
   ("George R. R. Martin" vs "George R.R. Martin").
   Audible files the narrator into the same tag after a comma
   ("Sarah J. Maas, Amanda Leigh Cobb"), so only the first segment is the
   author -- which is the line we want, since the author is what you scan a
   shelf for and it needs no translation. */
var aa=String(it.AlbumArtist||'');
if(aa){au=aa.split(',')[0].trim();}
var ser='';
var tags=it.Tags||[];
for(j=0;j<tags.length;j++){if(String(tags[j]).indexOf('Series: ')===0){ser=String(tags[j]).slice(8);break;}}
var ud=it.UserData||{};
out[String(it.Id).replace(/-/g,'').toLowerCase()]={a:au,n:it.IndexNumber||0,s:ser,
rt:it.RunTimeTicks||0,pos:ud.PlaybackPositionTicks||0};
}
MAP=out;BUSY=false;
store(out);
cb(MAP);
}).catch(function(){BUSY=false;});
}
function paint(){
try{
/* sf-abtitle-any (2026-08-21). The admin: "pressing the audiobook title row doesn't
   do anything." It worked -- on the dedicated Audiobooks row, which is the only
   place I had wired it. The book in CONTINUE WATCHING had no title link at all,
   and that is the one he was pressing.
   So wire it by CARD, not by row: any audiobook card anywhere gets the same
   behaviour, including rows that do not exist yet. */
var SEL='.card[data-type="AudioBook"]:not([data-sf-abc]),'
+'.sf-ml-card[data-type="AudioBook"]:not([data-sf-abc]),'
+'[data-sf-abcard]:not([data-sf-abc]),'
+'[data-sf-cwbook]:not([data-sf-abc])';
var cards=document.querySelectorAll(SEL);
if(!cards.length)return;
load(function(map){
var cs=document.querySelectorAll(SEL),i;
for(i=0;i<cs.length;i++){
var card=cs[i];
var id=String(card.getAttribute('data-id')||'').replace(/-/g,'').toLowerCase();
var rec=map[id];
/* sf-abcard-persist: an unknown id means the shelf grew since the cache was
   written, so drop it and let the next pass rebuild -- once, not per card. */
if(!rec){try{window.__sfAbCardMiss&&window.__sfAbCardMiss(id);}catch(e){}continue;}
card.setAttribute('data-sf-abc','1');
/* the title is a way IN to the book; the artwork stays the way to PLAY it */
(function(){
var bid=card.getAttribute('data-id')||card.getAttribute('data-sf-cwbook')||'';
if(!bid)return;
var lines=card.querySelectorAll('.cardText'),li;
for(li=0;li<lines.length;li++){
if(lines[li].getAttribute('data-sf-ablink')==='1')continue;
lines[li].setAttribute('data-sf-ablink','1');
lines[li].classList.add('sf-ab-titlelink');
lines[li].addEventListener('click',function(e){
e.preventDefault();e.stopPropagation();
if(!bid)return;
try{if(window.__sfAbGo){window.__sfAbGo(bid);return;}}catch(err){}
location.hash='#/details?id='+bid;
});
}
})();
var texts=card.querySelectorAll('.cardText');
/* Second line: the AUTHOR on a book you have not started, and how much is LEFT
   once you have -- which is what Audible puts there, and the thing you actually
   want to know when deciding whether to pick it back up tonight. */
if(texts.length>1){
var second=texts[1],want=rec.a||'';
if(rec.rt&&rec.pos>0&&rec.pos<rec.rt){
var left=Math.max(0,Math.round((rec.rt-rec.pos)/10000000));
var lh=Math.floor(left/3600),lm=Math.round((left%3600)/60);
want=(lh?(lh+'h '+lm+'m'):(lm+'m'))+' left';
second.classList.add('sf-abc-left');
}else{
second.classList.remove('sf-abc-left');
second.classList.add('sf-abc-author');
}
if(want&&second.textContent.trim()!==want)second.textContent=want;
}
/* series position, on the artwork */
if(rec.s&&rec.n&&!card.querySelector('.sf-abc-num')){
var host=card.querySelector('.cardImageContainer')||card.querySelector('.cardScalable');
if(host){
var b=document.createElement('span');
b.className='sf-abc-num';
b.textContent=rec.n;
b.title=rec.s;
host.appendChild(b);
}
}
}
});
}catch(e){}
}
setInterval(paint,900);
window.addEventListener('hashchange',function(){setTimeout(paint,400);});
/* The shelves are built by the main tick; nudge them the moment the route
   changes so the page does not sit on the previous layout for a tick interval. */
window.addEventListener('hashchange',function(){
[0,60,200,500].forEach(function(d){setTimeout(function(){
try{if(window.__sfAbLibNudge)window.__sfAbLibNudge();}catch(e){}},d);});
});
})();</script>"""




# --- retired blocks ----------------------------------------------------------
# This patcher runs against the LIVE index.html, not a pristine copy, and each
# block is removed-then-re-added by its own marker. That means deleting a block
# from this file does NOT remove it from the server -- its cleanup regex goes
# with it, so the old script is orphaned in the page forever.
#
# Learned the hard way: sf-prenext (a next-track prefetch) was reverted after it
# measured no better than baseline, and it stayed live in the container because
# its own removal code had been deleted alongside it.
#
# So retired markers are listed here and stripped on every run.
RETIRED = ['sf-prenext']


DIAG_MARKER = 'sf-diag-report'
DIAG_SCRIPT = r"""<script>(function(){ /* sf-diag-report */
if(location.href.indexOf("sfdiag=1")<0)return;
function vis(e){if(!e)return false;var r=e.getBoundingClientRect();
if(!r.width||!r.height)return false;var s=getComputedStyle(e);
return s.display!=="none"&&s.visibility!=="hidden"&&parseFloat(s.opacity||"1")>0.05;}
function txt(e){return (e.textContent||"").trim().slice(0,18);}
function report(){
var L=[];
L.push("UA: "+navigator.userAgent.slice(0,110));
L.push("viewport: "+innerWidth+"x"+innerHeight+"  dpr="+devicePixelRatio
       +"  zoom~"+Math.round((outerWidth/innerWidth)*100)/100);
L.push("url: "+location.href.slice(0,90));
var bars=document.querySelectorAll(".headerTabs,.tabs-viewmenubar");
L.push("tab bars found: "+bars.length);
for(var i=0;i<bars.length;i++){
var b=bars[i],btns=b.querySelectorAll("button,a"),lab=[],j;
for(j=0;j<btns.length;j++){lab.push((vis(btns[j])?"":"~")+txt(btns[j]));}
L.push("  ["+i+"] vis="+vis(b)+" w="+Math.round(b.getBoundingClientRect().width)
       +" cls="+String(b.className).slice(0,42));
L.push("       "+lab.join(" | "));
}
var marks=["jf-home-tab","jf-livetv-tab","jf-sports-tab","jf-mystuff-tab",
           "sf-hdr-solid","jf-hero-layout","jf-pane-guard","sf-request-search"];
var got=[];
for(var m=0;m<marks.length;m++){
got.push(marks[m]+"="+(document.querySelector("."+marks[m])?"dom":
        (document.documentElement.innerHTML.indexOf(marks[m])>=0?"html":"NO")));
}
L.push("markers: "+got.join("  "));
var slides=document.querySelectorAll(".slide");
L.push("HERO slides: "+slides.length);
for(var k=0;k<slides.length&&k<4;k++){
var sl=slides[k],cs=getComputedStyle(sl);
L.push("  ["+k+"] "+String(sl.className).slice(0,26)
       +" vis="+vis(sl)+" h="+sl.offsetHeight
       +" op="+cs.opacity+" disp="+cs.display+" vy="+cs.visibility);
var ims=sl.querySelectorAll("img");
for(var z=0;z<ims.length&&z<3;z++){
L.push("       img nat="+ims[z].naturalWidth+"x"+ims[z].naturalHeight
       +" complete="+ims[z].complete
       +" "+String(ims[z].currentSrc||ims[z].src).slice(-42));
}
}
var bc=document.querySelector(".backgroundContainer");
if(bc)L.push("backdrop: vis="+vis(bc)+" h="+bc.offsetHeight
             +" bg="+String(getComputedStyle(bc).backgroundImage).slice(0,44));
var hero=document.querySelectorAll("[class*=mediaBar],[class*=media-bar],[class*=hero]");
L.push("hero-ish elements: "+hero.length);
L.push("plugins css/js blocked? scripts="+document.scripts.length
       +" stylesheets="+document.styleSheets.length);
var pre=document.getElementById("sf-diag-box");
if(!pre){pre=document.createElement("pre");pre.id="sf-diag-box";
pre.style.cssText="position:fixed;left:0;top:0;right:0;z-index:99999;margin:0;"
+"max-height:70vh;overflow:auto;background:#000;color:#0f0;font:11px/1.35 monospace;"
+"padding:10px;white-space:pre-wrap;border-bottom:2px solid #0f0;";
document.body.appendChild(pre);}
pre.textContent=L.join("\n");
}
setTimeout(report,6000);
setTimeout(report,12000);
})();</script>"""


HDRSOLID_MARKER = 'sf-hdr-solid'
HDRSOLID_SCRIPT = r"""<script>(function(){ /* sf-hdr-solid */
if(window.__sfHdrSolid)return;
window.__sfHdrSolid=1;
/* The header keeps jellyfin-web's own skinHeader-withBackground and
   skinHeader-blurred classes, but both are neutered further down the cascade --
   measured background rgba(0,0,0,0) and backdrop-filter none at every scroll
   position. Over the hero that is the intended look. Over scrolled content it
   leaves the icons sitting directly on card artwork, which on a phone is most of
   what you see.

   So the transparency is kept at the top and a background is faded in once the
   page has moved. Class toggle only -- the styling itself lives in CSS, and the
   at-top appearance is untouched.

   Listens in the CAPTURE phase because scroll does not bubble: home scrolls the
   document, but other views scroll an inner element, and a window-only listener
   silently misses those. */
var pending=false;
function apply(){
pending=false;
var h=document.querySelector('.skinHeader');
if(!h)return;
var y=window.pageYOffset||0;
if(!y){var se=document.scrollingElement;if(se)y=se.scrollTop||0;}
if(y>60)h.classList.add('sf-hdr-solid');
else h.classList.remove('sf-hdr-solid');
}
function onScroll(){if(pending)return;pending=true;requestAnimationFrame(apply);}
document.addEventListener('scroll',onScroll,{capture:true,passive:true});
window.addEventListener('resize',onScroll,{passive:true});
window.addEventListener('hashchange',function(){setTimeout(apply,60);});
document.addEventListener('DOMContentLoaded',apply);
apply();
})();</script>"""









VIEWSCOPE_MARKER = 'jf-view-scope'
VIEWSCOPE_SCRIPT = r"""<script>(function(){ /* jf-view-scope */
if(window.__jfView)return;
function onScreen(el){
return !!(el&&!el.classList.contains('hide')&&el.offsetParent!==null);}
/* sf-viewscope-cache: onScreen() reads offsetParent, which forces a SYNCHRONOUS
   LAYOUT, and homePage() called it once per #indexPage in the document. Several
   SF_TICK functions call homePage() (directly, or via favTab/homeTab), so every
   400ms tick paid several full layout flushes.
   Profiled on a 4x-throttled phone CPU, one home load: onScreen 1465ms +
   querySelectorAll 995ms -- the single largest JS cost on the page, out of
   6285ms of total main-thread blocking.
   Memoised for 250ms, which is shorter than the tick, so a tick does at most one
   scan instead of one per caller. Correctness held by dropping the cache on
   hashchange (a route change is when the visible page actually swaps) and by
   re-checking isConnected and .hide -- neither of which forces layout. */
var _hpEl=null,_hpAt=0;
try{window.addEventListener('hashchange',function(){_hpEl=null;_hpAt=0;},true);}catch(e){}
function homePage(){
var now=Date.now();
if(_hpEl&&(now-_hpAt)<250&&_hpEl.isConnected&&!_hpEl.classList.contains('hide'))return _hpEl;
var all=document.querySelectorAll('#indexPage'),found=null;
for(var i=0;i<all.length;i++){if(onScreen(all[i])){found=all[i];break;}}
_hpEl=found;_hpAt=now;
return found;}
function inHome(sel){
var p=homePage();
return p?p.querySelector(sel):null;}
window.__jfView={
homePage:homePage,
favTab:function(){return inHome('#favoritesTab');},
homeTab:function(){return inHome('#homeTab');},
onScreen:onScreen
};
})();</script>"""


MEDIASESSION_MARKER = 'sf-ab-mediasession'
# Audiobook lock-screen controls (2026-08-28).
#
# Measured in the deployed bundle, not assumed:
#   * setPositionState is called ZERO times by jellyfin-web, so the lock screen
#     and the car head unit show no scrubber, no elapsed and no remaining.
#   * playbackState is likewise never set (0 occurrences).
#   * bindNavigatorSession does:
#         n=["pause","play","previoustrack","nexttrack","stop","seekto"];
#         te.A.iOS||n.push("seekbackward","seekforward");
#     i.e. on iOS jellyfin-web DELIBERATELY registers no seek handlers at all.
#     So on the admin's iPhone a 13-hour audiobook offered prev/next TRACK -- which
#     do nothing on a single-file m4b -- and nothing else.
#
# Everything the audiobook cluster adds (speed, sleep timer, chapters, bookmarks,
# read-along) lives inside the page, so the moment the screen locks the listener
# had a play/pause button and no way to skip. That is most of audiobook listening.
#
# HOW IT AVOIDS BREAKING MUSIC AND VIDEO: it does not replace Jellyfin's handlers,
# it WRAPS setActionHandler. Jellyfin still registers whatever it wants; we keep a
# reference and install a gate that runs OUR action only while a confirmed
# audiobook is playing, and otherwise calls straight through to Jellyfin's. The
# wrapper is installed before Jellyfin's deferred bundles execute, so ordering is
# not a race. seekbackward/seekforward -- which Jellyfin never registers on iOS --
# are armed only while a book plays and restored to Jellyfin's own state (usually
# nothing) the moment one is not, so music keeps exactly the controls it had.
#
# The "is a book" test reuses sf-rate-confirm's rule: the now-playing bar's id must
# match the id parsed out of the AUDIO element's own src. The bar lags the element
# by seconds on a switch, and trusting it alone is what once applied 1.5x speed to
# music (see sf-rate-leak).
MEDIASESSION_SCRIPT = ('<script>(function(){/* sf-ab-mediasession */'
 "if(!('mediaSession' in navigator))return;"
 'var MS=navigator.mediaSession,SKIP=30,jf={},real;'
 'try{real=MS.setActionHandler.bind(MS);}catch(e){return;}'
 'function api(){return window.__sfAbApi||null;}'
 'function book(){'
 'var A=api();if(!A)return false;'
 'try{'
 'var id=A.nowId();if(!id)return false;'
 'if(A.isBook(id)!==true)return false;'
 "var aid=A.audioId(),nid=String(id).toLowerCase().replace(/-/g,'');"
 'return !!(aid&&nid&&aid===nid);'
 '}catch(e){return false;}}'
 'function ours(action,d){'
 'var A=api();if(!A)return false;'
 'var off=(d&&d.seekOffset)||SKIP;'
 'try{'
 "if(action==='seekbackward'){A.seekBy(-off);return true;}"
 "if(action==='seekforward'){A.seekBy(off);return true;}"
 "if(action==='previoustrack'){A.jumpChapter(-1);return true;}"
 "if(action==='nexttrack'){A.jumpChapter(1);return true;}"
 '}catch(e){}'
 'return false;}'
 'function gated(action){return function(d){'
 'if(book()&&ours(action,d))return;'
 'var f=jf[action];if(f)try{return f(d);}catch(e){}'
 '};}'
 'try{MS.setActionHandler=function(action,fn){'
 'jf[action]=fn||null;'
 'try{real(action,fn?gated(action):null);}catch(e){}'
 '};}catch(e){}'
 # iOS never registers these, so arm them ourselves -- but only during a book.
 'var armed=null;'
 'function arm(on){'
 'if(on===armed)return;armed=on;'
 "var acts=['seekbackward','seekforward'],i;"
 'for(i=0;i<acts.length;i++){(function(a){try{'
 'if(on)real(a,gated(a));'
 'else real(a,jf[a]?gated(a):null);'
 '}catch(e){}})(acts[i]);}}'
 # setPositionState throws TypeError on a non-finite duration, a position past
 # it, or a zero rate -- and Chromium's MSE blob reports duration Infinity for
 # the first moments of a transcoded stream. Guard every field.
 'function pos(){'
 'var A=api();if(!A)return;'
 'var a=A.el();if(!a)return;'
 'var isb=book();'
 'arm(isb);'
 'if(!isb)return;'
 'var d=a.duration,p=a.currentTime,r=a.playbackRate;'
 'if(!isFinite(d)||d<=0)return;'
 'if(!isFinite(p)||p<0)p=0;'
 'if(p>d)p=d;'
 'if(!isFinite(r)||r<=0)r=1;'
 'try{MS.setPositionState({duration:d,position:p,playbackRate:r});}catch(e){}'
 "try{MS.playbackState=a.paused?'paused':'playing';}catch(e){}"
 '}'
 'try{setInterval(function(){try{pos();}catch(e){}},1000);}catch(e){}'
 '})();</script>')
