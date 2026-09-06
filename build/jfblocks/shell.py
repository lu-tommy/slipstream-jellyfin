"""jfblocks/shell.py -- payload constants lifted out of jf_patch.py.

Each constant's source text (and its comments) is byte-identical to the
monolith; only its location changed. 14 constants.
"""

__all__ = [
    'HEADERFIX_MARKER',
    'HEADERFIX_STYLE',
    'SPLASHMARK_MARKER',
    'SPLASHMARK_STYLE',
    'MOTION_MARKER',
    'MOTION_STYLE',
    'RSKEL_MARKER',
    'RSKEL_STYLE',
    'BGHOLD_MARKER',
    'BGHOLD_STYLE',
    'FLATBG_MARKER',
    'FLATBG_STYLE',
    'HOMESETTLE_MARKER',
    'HOMESETTLE_STYLE',
    'NOSPINNER_MARKER',
    'NOSPINNER_STYLE',
    'PANEGUARD_MARKER',
    'PANEGUARD_SCRIPT',
    'SHEETCLOSE_MARKER',
    'SHEETCLOSE_SCRIPT',
    'DRAWERTIDY_MARKER',
    'DRAWERTIDY_SCRIPT',
    'USERRAIL_MARKER',
    'USERRAIL_SCRIPT',
]


# --- Header fix: on library pages (Movies/Shows/etc.) the .skinHeader collapses to
# ~29px and its `contain:paint` clips the back/home/menu buttons out of view, leaving
# no way to navigate back or home. Force the header to size to its content (and drop
# paint containment) so the nav bar is always visible. Scoped :not(.osdHeader) so the
# video-player overlay header is untouched.
HEADERFIX_MARKER = 'sf-header-fix'
# The header also FLASHES DARK on every reload. The transparency is not ours and
# not the theme's -- it comes from Media Bar's stylesheet, which is loaded
# cross-origin from jsDelivr by the plugin's own JS. Jellyfin's dark theme paints
# .skinHeader-withBackground rgb(32,32,32) immediately (that class is present on
# every route, verified), and the header only goes transparent once that CDN
# request lands. The visible flash is exactly that round trip.
# Fixed by stating the final value here instead of waiting for the network: this
# <style> is static in the HTML, so it applies on first parse. !important because
# the theme's rule is not, which makes cascade order irrelevant -- we win whether
# theme.css is injected before or after us.
# background-COLOR only: Media Bar layers a gradient on the header and setting
# background wholesale would wipe it.
# Steady state is unchanged -- the header already computes transparent on home,
# movies and every other route measured, so this only removes the transient.
HEADERFIX_STYLE = ('<style id="sf-header-fix">'
                   '.skinHeader:not(.osdHeader){height:auto!important;min-height:3.3em!important;'
                   'contain:layout style!important;'
                   'background-color:transparent!important;}'
                   '</style>')

# --- sf-motion: ONE set of motion tokens for the whole app -------------------
# Audited state: durations and curves were chosen per feature and disagree --
# .2s ease on the header, .7s cubic-bezier(.22,.61,.36,1) on the home rows,
# .7s cubic-bezier(.16,1,.3,1) on sfFinA/sfFinB in branding.xml, 320ms on the
# nav swap. Nothing is wrong with any one of them; together they are why the
# app reads as several pages rather than one product.
# These are tokens only -- declaring them changes nothing on its own. Rules opt
# in by name, so there is no `transition: all` anywhere and no element animates
# because a token exists.
MOTION_MARKER = 'sf-motion'
MOTION_STYLE = (
    '<style id="sf-motion">'
    ':root{'
    # 160 / 220 / 280: the range the admin asked for. `fast` is for things that must
    # feel instant (a pill lighting up), `base` for content arriving, `slow` for
    # a full-bleed surface like the backdrop where a quick fade reads as a blink.
    '--sf-dur-fast:160ms;'
    '--sf-dur:220ms;'
    '--sf-dur-slow:280ms;'
    # the curve already measured good on the home rows (sf-ease): it spreads the
    # motion instead of front-loading it, so it does not read as a snap
    '--sf-ease:cubic-bezier(.22,.61,.36,1);'
    # for something leaving: start fast, settle out
    '--sf-ease-out:cubic-bezier(.33,1,.68,1);'
    # --- entrance scale. Extracted from the Home page, which is the source of
    # truth -- and which disagreed with itself: its first-load entrance
    # (sfHomeInV2) travelled 36px while its navigation entrance (sfFinA/sfFinB)
    # travelled 20px, so the same rows arrived differently depending on how you
    # got there. 20px is the one seen far more often and is now the standard.
    # `dense` is a DESIGNED exception, not drift: the existing note on the grid
    # rules says a full-height grid sliding as far as a single row reads as the
    # whole page lurching, so a surface made of many small items travels less
    # and arrives quicker. Two distances, two entrance durations, no more.
    '--sf-dur-enter:700ms;'
    '--sf-dur-enter-dense:550ms;'
    '--sf-lift:20px;'
    '--sf-lift-sm:10px;'
    # already used at this value by every staggered surface; now it is named
    '--sf-stagger:50ms;'
    '}'
    # honour the OS setting once, centrally. Zeroing the DISTANCE tokens means
    # no rule needs its own reduced-motion variant to stop travelling.
    '@media (prefers-reduced-motion:reduce){:root{'
    '--sf-dur-fast:1ms;--sf-dur:1ms;--sf-dur-slow:1ms;'
    '--sf-dur-enter:1ms;--sf-dur-enter-dense:1ms;'
    '--sf-lift:0px;--sf-lift-sm:0px;--sf-stagger:0ms;}}'
    # --- sf-xfade: the page-transition lifecycle. See sfXfade for the measured
    # architecture. The outgoing page is held ON TOP and dissolved; the incoming
    # one is never seen part-built. z-index 1 puts it above its sibling pages and
    # still far below .skinHeader (999) and .mainDrawer (1099), both measured.
    # display is overridden because Jellyfin's .hide is display:none -- we never
    # touch that class, only what it paints, and only on a page we tagged.
    # --- sf-xf-stack. The admin, three times: "the rows are still invading the info
    # page". They were, and it is a stacking-context bug, not a timing one.
    # Measured on a live detail page:
    #     #itemDetailPage   position:relative  z-index:auto   <- NO stacking context
    #     .detailLogo       position:absolute  z-index:3
    #     .detailRibbon     position:relative  z-index:2
    # Because the page itself establishes no stacking context, those children are
    # painted in the ROOT context -- so at z-index 3 and 2 they sit ABOVE the held
    # page at z-index 1. The incoming logo and ribbon drew over the outgoing page
    # while Home's Continue Watching row (plain z-index auto, inside the held page)
    # still showed underneath them. That is the "invasion": one screen's hero on
    # top of another screen's rows.
    # `isolation:isolate` makes the incoming page its own stacking context, so its
    # internal z-indexes stay internal and it composites as a single layer beneath
    # the held one. Applied ONLY while a transition is in flight, so normal
    # rendering is untouched. Raising the held page's z-index instead would only
    # work until some child outranked the new number.
    'html.sf-xf-active .mainAnimatedPages > .page:not(.sf-xf-hold){isolation:isolate;}'
    # sf-xf-under. Isolation fixes the ORDER but not the VISIBILITY: measured with
    # isolation in place, the incoming page reached opacity 0.807 while the hold was
    # still up, fading in underneath a held page that is itself transparent across
    # its hero region -- so it showed straight through while Home's rows painted
    # below it. While something is held, the page behind it is not ready to be seen.
    #
    # This was FIRST written as `html.sf-xf-active ... {opacity:0!important}` and
    # that was a bad idea: one root class that fails to clear blanks every page in
    # the app, and it did -- 4976ms on Movie -> TV Show, 3363ms going Home.
    # Now it is a class on the page itself, and it carries its own way out: the
    # animation holds opacity 0 with steps(1,end) and then jumps to 1 at 2.5s, so a
    # stranded class costs a bounded pause instead of a dead client. !important
    # because it has to beat jfAtvIn, which is an ID-specificity animation.
    'html .mainAnimatedPages > .page.sf-xf-under:not(.sf-xf-instant){'
    'animation:sfXfUnder 2.5s steps(1,end) both!important;}'
    '@keyframes sfXfUnder{0%{opacity:0;}99.9%{opacity:0;}100%{opacity:1;}}'
    'html .mainAnimatedPages > .page.sf-xf-hold{'
    'display:block!important;z-index:1;pointer-events:none;opacity:1;'
    # Front-loaded on purpose. NEITHER page is opaque -- both are transparent
    # over the shared ambient wash -- so for the length of the dissolve the two
    # screens composite. Measured at the midpoint it reads as a fault, not as a
    # cross-fade: home's Continue Watching row sat across the movie's Play
    # button at roughly equal weight. A curve that spends most of its travel in
    # the first few frames keeps the ambiguous middle to ~2 frames, so it reads
    # as the old screen leaving. Shorter and subtler beats bigger here.
    'transition:opacity var(--sf-dur-fast) cubic-bezier(.2,0,.3,1);}'
    # A departing page also RECEDES, very slightly. Neither page is opaque, so for
    # the 1-4 frames they overlap the eye has to decide which screen it is looking
    # at; a layer that is moving away is read as depth rather than as two screens
    # at once. 1.5% is below the threshold where it registers as a zoom -- the cue
    # is doing the work, not the size of it. transform-origin sits above centre so
    # the movement is felt where the content is, not at the bottom of the page.
    # scale (not `transform`) so it composes with the inline `translate` that
    # holds the outgoing scroll position. Compositor-only, no layout.
    'html .mainAnimatedPages > .page.sf-xf-hold{'
    'transition:opacity var(--sf-dur-fast) cubic-bezier(.2,0,.3,1),'
    'scale var(--sf-dur-fast) cubic-bezier(.2,0,.3,1);'
    'transform-origin:50% 42%;}'
    'html .mainAnimatedPages > .page.sf-xf-hold.sf-xf-out{opacity:0;scale:.985;}'
    # The page being revealed under a leaving one must not run its own entrance as
    # well. Opacity is forced ONLY where the page is genuinely ready: a detail page
    # that has lost .sf-atv is mid-rebuild and must stay invisible, and forcing it
    # visible here is what briefly exposed half-built detail pages.
    'html .mainAnimatedPages > .page.sf-xf-instant{animation:none!important;}'
    'html .mainAnimatedPages > .page.sf-xf-instant:not(#itemDetailPage){opacity:1!important;}'
    'html #itemDetailPage.sf-atv.sf-xf-instant{opacity:1!important;}'
    # --- sf-hero-fold: the first viewport is artwork, title, metadata, actions.
    # The overview begins after it. --sf-ribbon-bottom is the hero's bottom edge in
    # document coordinates, published by the same ResizeObserver that owns
    # --sf-ribbon-h, so it is correct in the frame the hero changes rather than a
    # tick later. 100vh stays live in CSS, so a window resize needs no JS at all.
    # max() clamps it: if the hero is already taller than the viewport the plot
    # simply follows it, and the fallback makes the margin 0 before the value
    # exists rather than a full screen of empty space.
    'html #itemDetailPage .sf-dfacts{'
    'margin-top:max(0px,calc(100vh - var(--sf-ribbon-bottom,100vh)));}'
    # the reuse-path copy: inert, and never part of the accessibility tree
    'html .mainAnimatedPages > .page[data-sf-clone]{'
    'pointer-events:none!important;user-select:none!important;}'
    '@media (prefers-reduced-motion:reduce){'
    'html .mainAnimatedPages > .page.sf-xf-hold.sf-xf-out{scale:1;}}'
    # reduced motion still needs the HOLD (it is what removes the black gap);
    # only the dissolve goes away
    '@media (prefers-reduced-motion:reduce){'
    'html .mainAnimatedPages > .page.sf-xf-hold{transition:none;}}'
    # --- the one interaction that must feel immediate: a nav pill lighting up.
    # Measured as instant already (it is a class swap), but it changed with no
    # transition at all, which reads as a jump rather than a response.
    '.emby-tab-button,.jf-mu-mainbar button,[data-sf-nav]{'
    'transition:color var(--sf-dur-fast) var(--sf-ease),'
    'background-color var(--sf-dur-fast) var(--sf-ease);}'
    # The last split in the system: the entrance that plays on every
    # NAVIGATION (sfFinA/sfFinB, defined in branding.xml) still carries
    # cubic-bezier(.16,1,.3,1) -- the curve this codebase already measured
    # and rejected for the first-load entrance, because it reaches 90% in
    # 231ms of a 700ms run and reads as a snap with half a second of
    # invisible drift after it. sfHomeInV2 was given .22,.61,.36,1 for
    # exactly that reason. So load-in and navigate-in were two different
    # motions for the same event. Same curve for both, from the token.
    # branding.xml is FETCHED and injected at runtime, so it lands after
    # this block and would win on order at equal specificity -- the `html `
    # prefix takes specificity instead, the same trick sf-ease already uses.
    # --- sf-motion-one-owner (2026-09-05, Phase 5). The Abyss theme ships its OWN
    # complete section-entrance system, on the same elements as ours:
    #     .verticalSection:nth-child(1..9+)
    #       animation: abyss-section-fade-up .7s var(--abyss-ease) both .05s*N
    #     @keyframes abyss-section-fade-up { opacity 0->1; translateY(20px)->0 }
    # The SHAPE is byte-identical to sfFinA/sfHomeIn, so this was invisible as a
    # look -- but the values are not ours: --abyss-ease is
    # cubic-bezier(.16,1,.3,1), the exact curve this codebase measured and rejected
    # for reaching 90% of its travel in 231ms of a 700ms run.
    # Found by animation-name inventory across the app: abyss-section-fade-up was
    # the entrance actually running on My Stuff, Watchlist, Bookmarks, Movies,
    # Shows, Music and all three Live TV tabs. Our rules only beat it where we had
    # already added a class and an !important (branding.xml even says so), so most
    # of the app was animating on the theme's system, not ours.
    # Re-point it rather than switch it off: the keyframes are equivalent, so
    # taking over duration, curve and delay keeps every section's entrance while
    # making the values shared. It also drops the nth-child stagger, which is a
    # hazard in its own right -- the delay is keyed to sibling position, so
    # inserting or removing one row re-times every row after it.
    # (0,2,1) to beat the theme's (0,2,0); abyss.css is @imported by branding.xml
    # and therefore lands after this block, so specificity is the only lever.
    'html .verticalSection:nth-child(n){'
    'animation-duration:var(--sf-dur-enter);'
    'animation-timing-function:var(--sf-ease);'
    'animation-delay:calc(var(--sf-row-i, 0) * var(--sf-stagger));}'
    'html .verticalSection.sf-fin-a,html .verticalSection.sf-fin-b{'
    'animation-timing-function:var(--sf-ease)!important;}'
    # sf-det-nobdfade (2026-09-04). The admin: the info page still feels choppy --
    # "a section of the screen is black ... or it's slow".
    # Jellyfin's stock rule runs `backdrop-fadein .8s ease-in` on #itemBackdrop.
    # ease-in starts nearly flat, so measured against the page's own 280ms
    # entrance: at 265ms the PAGE was at opacity 0.94 while the backdrop behind
    # it was still at 0.11. The content arrives over a black rectangle and the
    # artwork only catches up half a second later -- two entrances, different
    # lengths, different curves, on the same screen.
    # We now decode the backdrop BEFORE revealing (sf-det-decoded), so the image
    # is ready at the first frame and this second fade buys nothing but lag. Let
    # the page's single jfAtvIn carry the whole thing, which is the stated goal
    # for this page: one complete layout, arriving once.
    # Scoped to .sf-atv so the stock behaviour is untouched anywhere our reveal
    # has not run -- if the failsafe cap fires, that path is unchanged.
    'html #itemDetailPage.sf-atv #itemBackdrop{'
    'animation:none!important;opacity:1!important;}'
    # sf-det-latefade (2026-09-04). The rule above is right when the artwork
    # won the race, and wrong when it did not: revealing on the cap put a
    # fully opaque backdrop on screen in one frame, a few hundred ms after the
    # page had settled. sfDetailHero marks only that case with .sf-bd-late and
    # flips .sf-bd-in once the image has decoded, so the artwork fades in
    # behind text that is already correct. Specificity, not order: the rule
    # above is (1,2,0) with !important, so these carry an extra class each.
    'html #itemDetailPage.sf-atv.sf-bd-late #itemBackdrop{'
    'opacity:0!important;transition:opacity 340ms var(--sf-ease,ease)!important;}'
    'html #itemDetailPage.sf-atv.sf-bd-late.sf-bd-in #itemBackdrop{'
    'opacity:1!important;}'
    '@media (prefers-reduced-motion:reduce){'
    'html #itemDetailPage.sf-atv.sf-bd-late #itemBackdrop{transition:none!important;}}'
    '</style>')

# --- sf-route-skel: contextual loading for every route that currently goes
# black. Measured before this, with the outgoing page already gone:
#     #/livetv?tab=1 (Guide)  black + a small spinner, ~400-800ms
#     #/details               ~670ms with nothing on screen at all
#     #/music                 1127ms of global spinner, 791ms with no content
#     #/movies                254ms of global spinner
#     #/home?tab=1 (My Stuff) ~1100ms with only the blurred backdrop showing
# Home already has skeleton machinery; the rest of the app had none. (The home
# one, .sf-skel, is currently inert -- `display:none!important` -- so these use
# their own .sf-rskel namespace rather than reviving a rule someone deliberately
# switched off.)
# Shape matches the real layout so nothing jumps when the content lands, and the
# shimmer is the app's existing .sf-skel-sh so this reads as the same product.
# --- sf-bg-hold: never let the backdrop go dark just because an image is still
# loading. Measured on #/details: the outgoing page's artwork disappears, the
# page paints its dark scrim, and the incoming backdrop only resolves a few
# hundred ms later -- which is the "heavily blurred screen with no content"
# stage of the complaint.
# This never writes to .backdropContainer. It parks a COPY of the outgoing image
# on its own layer directly above it, then fades that away once the incoming
# image has actually decoded. Jellyfin keeps full control of its own element, so
# there is nothing to fight and nothing to loop on.
# --- sf-flat-pagebg: the ambient wash needs a hero above it, and three of the
# four top-level surfaces do not have one.
# body::before is a blurred copy of the HOME hero's artwork at opacity .62 with
# saturate(170%) brightness(1.15), and body::after is a scrim that is deliberately
# TRANSPARENT AT THE TOP so the hero is untouched. That is right for #/home. But
# `onHome` in sfPageBg is `hash.indexOf('#/home')===0`, which is also true for
# ?tab=1 (My Stuff), ?sports=1 and ?livetv=1 -- and on those the hero is not
# painted at all. Measured: heroPainted=true on /home, false on all three, while
# ::before stayed at opacity .62 on every one of them. So the brightest, most
# saturated part of the wash sits at the top of a page with nothing over it, the
# scrim leaves that exact band undarkened, and the surface reads bright, low
# contrast and washed out -- worst on My Stuff, where the content is sparse.
# This is not a new judgement call: sf-mus-pagebg already exists and says
# "Home earns .62 because a full-bleed hero still fills the top third ... Music
# has no such image -- the wash IS the top of the page -- so at .62 the entire
# screen went orange and read as a coloured page rather than as light coming off
# the record." Identical situation, never generalised past music. Same numbers,
# so the app has ONE treatment for "wash with no hero above it" rather than two.
# `html body` for specificity: branding.xml owns the base rules and is fetched
# and injected at runtime, so it lands later and wins on order at equal weight.
FLATBG_MARKER = 'sf-flat-pagebg'
FLATBG_STYLE = (
    '<style id="sf-flat-pagebg">'
    'html body.sf-flat-pagebg::before{'
    'opacity:.26!important;'
    'filter:blur(72px) saturate(125%) brightness(1.02)!important;'
    # the base rule animates opacity to .62 with fill `both`, and an animation
    # beats a declared value -- so the fade-in has to be cancelled, not just
    # out-specified
    'animation:none!important;}'
    # a scrim that starts with weight instead of starting transparent: here the
    # top is exactly what needs holding down
    'html body.sf-flat-pagebg::after{'
    'background:linear-gradient(180deg,'
    'rgba(12,12,14,.30) 0%,rgba(12,12,14,.46) 38%,'
    'rgba(12,12,14,.74) 74%,rgba(12,12,14,.88) 100%)!important;}'
    '</style>')


BGHOLD_MARKER = 'sf-bg-hold'
BGHOLD_STYLE = (
    '<style id="sf-bg-hold">'
    '.sf-bgprev{position:fixed;left:0;right:0;top:0;bottom:0;pointer-events:none;'
    'background-repeat:no-repeat;background-size:cover;background-position:center;'
    'opacity:1;transition:opacity var(--sf-dur-slow,280ms) var(--sf-ease-out,ease);}'
    '.sf-bgprev.sf-bgprev-out{opacity:0;}'
    '@media (prefers-reduced-motion:reduce){.sf-bgprev{transition:none;}}'
    '</style>')


RSKEL_MARKER = 'sf-route-skel'
RSKEL_STYLE = (
    '<style id="sf-route-skel">'
    # Fixed under the header, exactly like the album skeleton (.sf-dskel) already
    # does -- the route's own page element frequently does not exist yet at the
    # moment the gap starts, so anything parented to it can only cover the tail.
    '.sf-rskel{position:fixed;left:0;right:0;top:var(--sf-hdr,7rem);bottom:0;'
    'z-index:1;pointer-events:none;-webkit-user-select:none;user-select:none;'
    'overflow:hidden;padding:0 3vw;'
    'animation:sfRsIn var(--sf-dur,220ms) var(--sf-ease,ease) both;}'
    '@keyframes sfRsIn{from{opacity:0;}to{opacity:1;}}'
    # leaving: quicker than arriving, so the real content is never waiting on it
    '.sf-rskel.sf-rskel-out{animation:sfRsOut var(--sf-dur-fast,160ms) var(--sf-ease-out,ease) both;}'
    '@keyframes sfRsOut{from{opacity:1;}to{opacity:0;}}'
    '@media (prefers-reduced-motion:reduce){.sf-rskel{animation:none;}}'
    '.sf-rskel-hd{height:22px;width:34%;max-width:260px;border-radius:7px;margin:6px 0 20px;}'
    # --- grid: library routes (Movies / Shows / Music / Folders / Channels).
    # auto-fill at the real card width so the column count matches what lands.
    '.sf-rskel-grid{display:grid;gap:1.4rem 1.2rem;'
    'grid-template-columns:repeat(auto-fill,minmax(148px,1fr));}'
    '.sf-rskel-card .sf-rskel-img{width:100%;aspect-ratio:2/3;border-radius:12px;}'
    '.sf-rskel-card .sf-rskel-tx{height:10px;width:72%;border-radius:5px;margin-top:9px;}'
    '.sf-rskel-card .sf-rskel-tx2{height:9px;width:44%;border-radius:5px;margin-top:6px;opacity:.6;}'
    # --- rows: My Stuff, and anything else that is a strip of 16:9 cards
    '.sf-rskel-row{margin-bottom:26px;}'
    '.sf-rskel-strip{display:flex;gap:1.1rem;overflow:hidden;}'
    '.sf-rskel-wide .sf-rskel-img{width:min(19vw,300px);aspect-ratio:16/9;border-radius:12px;flex:0 0 auto;}'
    # My Stuff's rows are posters, so its skeleton has to be too
    '.sf-rskel-poster .sf-rskel-img{width:min(11.5vw,165px);aspect-ratio:2/3;'
    'border-radius:12px;flex:0 0 auto;}'
    '.sf-rskel-strip .sf-rskel-tx{height:10px;width:70%;border-radius:5px;margin-top:8px;}'
    # --- guide: the Live TV grid. A time ruler, then channel rows of programmes
    # at deliberately uneven widths so it reads as a schedule, not a table.
    '.sf-rskel-ruler{display:flex;gap:.9rem;margin-bottom:14px;}'
    '.sf-rskel-ruler i{height:11px;flex:1 1 0;border-radius:5px;display:block;}'
    '.sf-rskel-grow{display:flex;align-items:center;gap:.9rem;margin-bottom:.7rem;}'
    '.sf-rskel-chan{flex:0 0 auto;width:104px;height:46px;border-radius:9px;}'
    '.sf-rskel-prog{height:46px;border-radius:8px;}'
    # --- detail: the shape of the item page's first screen
    '.sf-rskel-detail{padding-top:8vh;max-width:720px;}'
    '.sf-rskel-detail .sf-rskel-logo{height:52px;width:min(46%,320px);border-radius:10px;margin-bottom:18px;}'
    '.sf-rskel-detail .sf-rskel-meta{height:13px;width:38%;max-width:230px;border-radius:6px;margin-bottom:14px;}'
    '.sf-rskel-detail .sf-rskel-plot{height:11px;border-radius:5px;margin-bottom:8px;}'
    '.sf-rskel-detail .sf-rskel-btns{display:flex;gap:.8rem;margin-top:22px;}'
    '.sf-rskel-detail .sf-rskel-btn{height:42px;width:150px;border-radius:21px;}'
    '.sf-rskel-detail .sf-rskel-btn2{width:44px;}'
    '@media (max-width:640px){'
    '.sf-rskel-grid{grid-template-columns:repeat(auto-fill,minmax(104px,1fr));gap:1rem .8rem;}'
    '.sf-rskel-wide .sf-rskel-img{width:62vw;}'
    '.sf-rskel-poster .sf-rskel-img{width:31vw;}'
    '.sf-rskel-detail .sf-rskel-logo{height:38px;}'
    '.sf-rskel-chan{width:74px;}}'
    # --- the point of all of the above: while a skeleton is up the route already
    # has contextual feedback, so the app's full-screen spinner is pure noise on
    # top of it. Scoped to the flag, so every route without a skeleton keeps its
    # spinner and nothing loses its loading feedback.
    'html[data-sf-rskel] > body > .docspinner,'
    'html[data-sf-rskel] .docspinner{display:none!important;}'
    '</style>')

SPLASHMARK_MARKER = 'jf-splash-mark'

# sf-home-head (2026-09-01). The admin: "our hero elements do it perfectly everytime
# but our CW row just flashes in on a fresh page load."
# Cause, measured: the hold rule that sf-home-settle depends on lives in
# Jellyfin's Custom CSS (branding.xml). index.html does NOT <link> that -- the
# app FETCHES /Branding/Css (326KB) and injects it at runtime, after boot. So on
# a fresh load the rows could paint before the hold rule existed at all, then
# snap to opacity 0 once it arrived: the flash. The hero never does this because
# sf-mediabar.css is a real <link> in <head>, render-blocking, present from the
# first byte. This puts the same rules in <head> so the hold is live from the
# first frame, exactly like the hero. branding.xml keeps its copy; the rules are
# identical, so the later duplicate is a no-op.
HOMESETTLE_MARKER = 'sf-home-head'
HOMESETTLE_STYLE = (
    '<style id="sf-home-head">'
    # sf-prehold: measured -- the row painted at opacity 1 for ~105ms before
    # sfHomeSettle added [data-sf-settle], because the rule below waits on an
    # attribute that JS must set. Hold from the very first frame instead, and
    # stop as soon as JS has taken over (either attribute present). Same 6s
    # failsafe, so a route sfHomeSettle deliberately ignores (My Stuff, Sports)
    # still reveals, and sfFloatPass animates those rows anyway.
    '.homeSectionsContainer:not([data-sf-settle]):not([data-sf-settled]) > .verticalSection{'
    'opacity:0;animation:sfHomeFailsafe 6s steps(1,end) forwards;}'
    '.homeSectionsContainer[data-sf-settle] > .verticalSection{'
    'opacity:0;animation:sfHomeFailsafe 6s steps(1,end) forwards;}'
    '@keyframes sfHomeFailsafe{0%,99%{opacity:0;}100%{opacity:1;}}'
    # sf-composite: 2070ms of main-thread blocking measured across 15 long tasks
    # on a cold load, including a 311ms task at the exact moment the entrance
    # began. opacity/transform is only immune to that when the element is on its
    # own compositor layer; it was not, so the animation ran on the blocked main
    # thread, froze at opacity 0 for 3.3s and snapped to 1 -- the flash. Promote
    # the entering rows so the animation runs off the main thread.
    '.homeSectionsContainer[data-sf-settle] > .verticalSection,'
    '.homeSectionsContainer[data-sf-settled] > .verticalSection{'
    'will-change:opacity,transform;}'
    # sf-ease (2026-09-01). The admin: it still just pops in. Measured the curve:
    # cubic-bezier(.16,1,.3,1) reaches 49% at 70ms, 75% at 140ms and 90% at
    # 231ms of a 700ms animation -- the remaining 469ms covers only the last
    # 10%, which is invisible. So it is a 231ms snap plus half a second of
    # imperceptible drift: a pop. Favorites gets away with it because many rows
    # stagger 50ms apart and you read the wave; a single first-view row has
    # nothing to hide behind. cubic-bezier(.22,.61,.36,1) spreads the motion
    # (27/50/67/79/87% at 70/140/210/280/350ms) and the travel goes 20px -> 36px
    # so it visibly rises. Own keyframe name + `html ` prefix so branding.xml's
    # copy of sfHomeIn -- injected at runtime, therefore later -- cannot win.
    'html .homeSectionsContainer[data-sf-settled] > .verticalSection,'
    'html .homeSectionsContainer[data-sf-settle] > .verticalSection.sf-first{'
    'animation:sfHomeInV2 var(--sf-dur-enter) var(--sf-ease) both;'
    'animation-delay:calc(var(--sf-row-i, 0) * var(--sf-stagger));}'
    '@keyframes sfHomeInV2{from{opacity:0;transform:translateY(var(--sf-lift));}'
    'to{opacity:1;transform:translateY(0);}}'
    '@media (prefers-reduced-motion: reduce){'
    '.homeSectionsContainer[data-sf-settled] > .verticalSection,'
    '.homeSectionsContainer[data-sf-settle] > .verticalSection.sf-first{'
    'animation:none;opacity:1;}}'
    # sf-ls-in (2026-09-04). The admin: the tab switches should load in smoothly too.
    # The Sports page appeared in ONE frame, fully opaque -- captured on three
    # switches, a single-frame luma step of +39 with no intermediate frame at all.
    # Cause: every entrance in this build is selected on `.verticalSection`
    # (sfHomeInV2 here, and sfFinA/sfFinB in branding.xml, which is written
    # `.verticalSection.sf-fin-a`). The sports page does not build those -- its
    # rows are `.sf-ls-section`, so no rule ever matched them and they had
    # animation:none. sfFloatPass now includes them; these are the rules it needs.
    # Own keyframe names, defined HERE rather than reusing branding.xml's sfFinA:
    # branding.xml is fetched and injected at runtime, so on a cold load straight
    # to #/home?sports=1 its keyframes may not exist yet, and an animation naming
    # a missing keyframe simply does not run. Same alternating-name trick as
    # sf-floatin-altname, because a CSS animation only restarts when its NAME
    # changes and these rows are re-used across navigations.
    '.sf-ls-section.sf-fin-a{animation:sfLsInA var(--sf-dur-enter) var(--sf-ease) both;'
    'animation-delay:calc(var(--sf-row-i, 0) * var(--sf-stagger));}'
    '.sf-ls-section.sf-fin-b{animation:sfLsInB var(--sf-dur-enter) var(--sf-ease) both;'
    'animation-delay:calc(var(--sf-row-i, 0) * var(--sf-stagger));}'
    # sf-lib-in: library grids (Movies / Shows / Music / Folders) get the
    # same entrance. No stagger delay -- a grid is one surface, and there is
    # no row index for it to stagger against. A shorter travel than a row's
    # 20px too: a full-height grid sliding as far as a single row reads as
    # the whole page lurching.
    '.itemsContainer.sf-fin-a,.jf-fwl-grid.sf-fin-a,.guideVerticalScroller.sf-fin-a,.sf-lvp-grid.sf-fin-a{'
    'animation:sfGridInA var(--sf-dur-enter-dense) var(--sf-ease) both;}'
    '.itemsContainer.sf-fin-b,.jf-fwl-grid.sf-fin-b,.guideVerticalScroller.sf-fin-b,.sf-lvp-grid.sf-fin-b{'
    'animation:sfGridInB var(--sf-dur-enter-dense) var(--sf-ease) both;}'
    '@keyframes sfGridInA{from{opacity:0;transform:translateY(var(--sf-lift-sm));}'
    'to{opacity:1;transform:translateY(0);}}'
    '@keyframes sfGridInB{from{opacity:0;transform:translateY(var(--sf-lift-sm));}'
    'to{opacity:1;transform:translateY(0);}}'
    '@media (prefers-reduced-motion:reduce){'
    '.itemsContainer.sf-fin-a,.itemsContainer.sf-fin-b,'
    '.jf-fwl-grid.sf-fin-a,.jf-fwl-grid.sf-fin-b,'
    '.guideVerticalScroller.sf-fin-a,.guideVerticalScroller.sf-fin-b,'
    '.sf-lvp-grid.sf-fin-a,.sf-lvp-grid.sf-fin-b{animation:none;opacity:1;}}'
    '@keyframes sfLsInA{from{opacity:0;transform:translateY(var(--sf-lift));}'
    'to{opacity:1;transform:translateY(0);}}'
    '@keyframes sfLsInB{from{opacity:0;transform:translateY(var(--sf-lift));}'
    'to{opacity:1;transform:translateY(0);}}'
    '@media (prefers-reduced-motion: reduce){'
    '.sf-ls-section.sf-fin-a,.sf-ls-section.sf-fin-b{animation:none;opacity:1;}}'
    '</style>')
SPLASHMARK_STYLE = ('<style id="jf-splash-mark">'
                    '.splashLogo{background-image:url(favicons/touchicon512.png)!important;'
                    'background-size:contain!important;background-position:center!important;'
                    'background-repeat:no-repeat!important;}'
                    '</style>')

# --- Home spinner: there are TWO separate .docspinner instances (Jellyfin's
# stock circular spinner, reused as a generic component) — one nested inside
# #hssLoadingIndicator (Home Screen Sections' own placeholder while rows
# load), and a SECOND one that's a direct child of <body>, which is
# Jellyfin's global page-transition spinner shown on ANY navigation, not
# specific to home. The first patch only caught the HSS one; this is the
# actual one visible when navigating to home. Scoped to only home via
# :has(#indexPage.homePage:not(.hide)) so it doesn't suppress loading
# feedback on other pages (library, search, etc.) that weren't complained
# about — only the direct-child-of-body spinner is scoped, not any spinner
# nested inside a specific component elsewhere on the page.
NOSPINNER_MARKER = 'jf-no-home-spinner'
NOSPINNER_STYLE = ('<style id="jf-no-home-spinner">'
                   '#hssLoadingIndicator .docspinner{display:none!important;}'
                   # jf-spinner-early: the body-level docspinner appears at ~604ms, long
                   # before #indexPage exists, so a :has(#indexPage...) scope never matches
                   # while it is on screen. sf-fastfold stamps data-sf-home on <html> as soon
                   # as the hash says home, which is available immediately.
                   'body:has(#indexPage.homePage:not(.hide)) > .docspinner{display:none!important;}'
                   'html[data-sf-home] > body > .docspinner{display:none!important;}'
                   'html[data-sf-home] > body > .mdl-spinner{display:none!important;}'
                   '</style>')


# --- Pane guard (2026-08-08). ------------------------------------------------
# Jellyfin shows a tab pane by putting .is-active on one .pageTabContent inside
# the page (CSS then gives it display:block). emby-tabs activates BY DOM INDEX,
# and once several #indexPage copies exist -- normal, because the view manager
# caches one view per URL -- its controller can end up driving the copy that is
# not on screen. The visible page is then left with ZERO active panes: a blank
# screen. Worse, it never recovers on its own; every later navigation inherits
# it.
#
# Reproduced exactly (Home, Live TV, Sports, My Stuff, Home, Live TV, ...):
#   step 4  My Stuff (1st)   panes: homeTab favoritesTab:ACTIVE   activeCount 1  OK
#   step 6  Live TV  (2nd)   panes: all six inactive              activeCount 0  BLANK
#   step 7  Sports   (2nd)   activeCount 0   <- stuck
#   step 8  My Stuff (2nd)   activeCount 0   <- shows the page shell, not My Stuff
# At step 8 our decoration was verified present on the resolved instance, so the
# sub-tab work was never the problem -- only activation was.
#
# This ONLY acts on an already-broken state (visible page, panes present, none
# active), so it cannot fight Jellyfin during a healthy transition. If the id the
# URL implies is not in the visible page -- which is what happens mid-transition,
# when the hash has changed but the old page is still on screen -- it does
# nothing. Worst case it is a no-op.
PANEGUARD_MARKER = 'jf-pane-guard'
PANEGUARD_SCRIPT = r"""<script>(function(){ /* jf-pane-guard */
var LTV=['suggestionsTab','guideTab','channelsTab','recordingsTab','scheduleTab','seriesTab'];
function livePage(){
var all=document.querySelectorAll('#indexPage, .liveTvPage');
for(var i=0;i<all.length;i++){var p=all[i];
if(!p.classList.contains('hide')&&p.offsetParent!==null)return p;}
return null;}
function wantedId(){
var h=location.hash||'';
/* the aliased Live TV url starts #/home, so it MUST be tested first or the
   guard would expect homeTab while liveTvSuggestedPage is mounted and could
   force the user off the page. */
if(window.__sfLtv&&window.__sfLtv.is(h))return LTV[window.__sfLtv.tab(h)]||LTV[0];
if(/#\/livetv/.test(h)){var m=/[?&]tab=(\d+)/.exec(h);return LTV[m?+m[1]:0]||LTV[0];}
if(/#\/home/.test(h))return /[?&]tab=1\b/.test(h)?'favoritesTab':'homeTab';
return null;}
var pending=null;   /* jf-pane-guard-v2 */
function guard(){
var p=livePage();if(!p)return;
var panes=p.querySelectorAll('.pageTabContent');
if(!panes.length)return;
var id=wantedId();if(!id){pending=null;return;}
/* scoped to the visible page: ids are duplicated across cached views */
var t=p.querySelector('#'+id);
/* wanted pane is not in the page on screen -- the hash has changed but the old
   view is still up. Mid-transition: leave it entirely alone. */
if(!t){pending=null;return;}
/* jf-pane-guard-multi: this used to take the FIRST active pane and `break`, so
   the state "two panes active at once" was invisible to it -- if the correct one
   happened to come first it returned "already correct" and left the other one
   showing. Reproduced on Live TV: suggestionsTab AND guideTab both is-active,
   which paints the Guide grid on top of the Programs rows. Collect them all and
   insist on exactly one. */
var actives=[],i;
for(i=0;i<panes.length;i++){
if(panes[i].classList.contains('is-active'))actives.push(panes[i]);}
if(actives.length===1&&actives[0]===t){pending=null;return;}   /* already correct */
var active=actives.length?actives[0]:null;
/* Two distinct breakages are repaired here:
   (a) NO pane active -> blank screen. Unambiguous, so fix it at once.
   (b) the WRONG pane active -> #/home?tab=1 while homeTab is showing, which
       reads as "My Stuff shows the home screen". Reproduced from lap 2 of
       Home/LiveTV/Sports/MyStuff onward; the v1 guard missed it because one
       pane WAS active and it only checked for none.
   A mismatch can also just be a transition in flight, so (b) must PERSIST
   across two consecutive checks before we touch anything. (a) does not wait --
   a blank screen is never a legitimate intermediate state worth preserving. */
/* One wrong pane can be a transition in flight, so that still has to persist.
   TWO active panes cannot: nothing legitimate paints the Guide over Programs,
   so repair it on sight, same as the no-pane-active case. */
if(active&&actives.length===1){
var key=(p.id||'')+'|'+(location.hash||'')+'|'+active.id+'|'+id;
if(pending!==key){pending=key;return;}
}
pending=null;
for(var j=0;j<panes.length;j++){panes[j].classList.remove('is-active');}
t.classList.add('is-active');
/* let the existing listeners re-sync the sub-pills. Safe against recursion:
   the pane matches now, so a re-entrant guard() returns at the active===t
   check above. */
try{window.dispatchEvent(new Event('hashchange'));}catch(e){}
}
window.addEventListener('hashchange',function(){setTimeout(guard,60);setTimeout(guard,400);});
/* jf-pane-guard-click: history.replaceState does NOT fire hashchange, and our
   own header pills update the address bar with replaceState -- so on a tab
   click the hashchange listener above never ran and the ONLY thing that
   noticed the stale pane was the 500ms poll below.
   Measured on a Home <-> My Stuff cycle:
       12ms   replaceState #/home?tab=1     (the click)
      600ms   ...nothing...
      612ms   hashchange -> favoritesTab ACTIVE   (the poll, finally)
   That gap was the whole "My Stuff takes ages to load" complaint -- the data
   was never slow (favItems=18 the entire time), the pane switch was just
   waiting on a timer. It also widened the window in which the URL, the active
   pane and the lit pill disagree, which is the "both tabs lit" / "stuck on the
   home screen" state.
   Hooking the click in the CAPTURE phase runs the guard straight away instead.
   Several passes because Jellyfin swaps the pane asynchronously after its own
   handler; each is a cheap no-op once the pane already matches the URL. */
/* jf-pane-guard-atomic: the two home-route pills, and the pane each one means.
   Live TV and Sports are deliberately absent -- they change route / mount an
   overlay and are handled by their own code; this only covers the Home <-> My
   Stuff switch that shares one #indexPage. */
var HOMEDEST={'Home':{h:'#/home',p:'homeTab'},'My Stuff':{h:'#/home?tab=1',p:'favoritesTab'}};
document.addEventListener('click',function(e){
var t=(e.target&&e.target.closest)?e.target.closest('.headerTabs.sectionTabs .emby-tab-button'):null;
if(!t)return;
var d=HOMEDEST[(t.textContent||'').trim()];
if(d){
/* Apply what the USER clicked, immediately and atomically -- URL first, then
   the pane. guard() derives its target from location.hash, so running it right
   after a click (which is what jf-pane-guard-click did) let it fire while the
   URL still lagged the click, whereupon it "repaired" the pane straight back
   and the click was silently undone. Measured: clicking Home left
   hash=#/home?tab=1, pane=favoritesTab, lit=My Stuff -- i.e. nothing moved,
   which is the "stuck on the home screen" report.
   Setting both here in one synchronous step removes the race entirely: the
   later guard passes see agreement and no-op. */
var p=livePage();
if(p){
var want=p.querySelector('#'+d.p);
if(want){
try{history.replaceState(null,'',d.h);}catch(err){}
var panes=p.querySelectorAll('.pageTabContent');
for(var i=0;i<panes.length;i++){panes[i].classList.remove('is-active');}
want.classList.add('is-active');
/* let ren() re-light the pills against the now-correct URL */
try{window.dispatchEvent(new Event('hashchange'));}catch(err){}
}}}
/* no 0ms pass any more -- the click is already applied above. These remain as
   the safety net for whatever Jellyfin does asynchronously afterwards. */
setTimeout(guard,60);setTimeout(guard,180);setTimeout(guard,400);
},true);
/* jf-pane-guard-nopage: guard() above repairs the PANE inside a visible page --
   it opens with `var p=livePage(); if(!p)return;`, and livePage() requires
   offsetParent!==null. So the one state it cannot repair is the one where NO
   page is visible at all, which is exactly the Live TV back-button failure:
   Live TV -> programme page -> Back left #indexPage, #liveTvSuggestedPage and
   #itemDetailPage ALL carrying Jellyfin's own `hide` class. Measured: still
   blank 6s later, pills and sub-pills painted over an empty page.
   The router hid every page and never un-hid the destination, so recovery is
   simply to un-hide the page the URL asks for and let guard() sort the pane.
   Deliberately conservative: only when nothing at all is on screen (never a
   legitimate resting state), only after 1.2s so a page transition in flight is
   never interrupted, and only for routes we can name. */
var sfNoPageSince=0;
function sfPageForHash(){
var h=location.hash||'';
if(window.__sfLtv&&window.__sfLtv.is(h))return document.querySelector('.liveTvPage');
if(/#\/details/.test(h))return document.querySelector('#itemDetailPage');
if(/#\/home/.test(h))return document.querySelector('#indexPage');
return null;
}
function sfNoPageGuard(){
var pages=document.querySelectorAll('.mainAnimatedPages > .page'),i;
if(!pages.length){sfNoPageSince=0;return;}
for(i=0;i<pages.length;i++){if(pages[i].offsetParent!==null){sfNoPageSince=0;return;}}
if(!sfNoPageSince){sfNoPageSince=Date.now();return;}
if(Date.now()-sfNoPageSince<1200)return;
var t=sfPageForHash();
if(!t){sfNoPageSince=0;return;}
sfNoPageSince=0;
t.classList.remove('hide');
try{window.dispatchEvent(new Event('hashchange'));}catch(e){}
setTimeout(guard,80);setTimeout(guard,400);
}
setInterval(function(){guard();sfNoPageGuard();},500);
})();</script>"""


SHEETCLOSE_MARKER = 'sf-sheet-close'
SHEETCLOSE_SCRIPT = """<script>(function(){ /* sf-sheet-close */
/* The Jellyfin Enhanced plugin's "Remove" item in the card menu stops
   propagation (blocking Jellyfin's own close) and then tries to close the sheet
   with dialog[open].close() or an Escape keydown. This build has no native
   <dialog> elements and does not close on Escape, so the menu stayed on screen
   after choosing Remove. history.back() is what Jellyfin's dialogHelper uses for
   a history-enabled dialog, and is the only thing measured to close it here. */
function sfOpenSheet(){
var s=document.querySelector('.actionSheet[data-history],.dialog[data-history]');
return (s&&s.getBoundingClientRect().height>0)?s:null;
}
function sfHasDialogEntry(){
try{var st=history.state;
return !!(st&&st.usr&&st.usr.dialogs&&st.usr.dialogs.length);}catch(e){return false;}
}
/* Capture phase, so the plugin's stopPropagation cannot hide the click from us. */
document.addEventListener('click',function(e){
var t=e.target;
if(!t||!t.closest)return;
var btn=t.closest('.remove-continue-watching-button');
if(!btn)return;
var t0=Date.now();
function step(){
if(Date.now()-t0>6000)return;      /* give up; never close an unrelated sheet later */
if(btn.disabled){setTimeout(step,120);return;}   /* removal still in flight */
if(Date.now()-t0<400){setTimeout(step,120);return;}
if(!sfOpenSheet())return;          /* already closed -- nothing to do */
if(!sfHasDialogEntry())return;     /* no dialog entry to pop: do NOT navigate */
history.back();
}
setTimeout(step,150);
},true);
})();</script>"""


DRAWERTIDY_MARKER = 'sf-drawer-tidy'
DRAWERTIDY_SCRIPT = r'''<style id="sf-drawer-tidy">
.mainDrawer .sf-dt-hide{display:none!important;}
</style>
<script>(function(){ /* sf-drawer-tidy */
if(window.__sfDrawerTidy)return; window.__sfDrawerTidy=1;
function qa(s,r){try{return [].slice.call((r||document).querySelectorAll(s));}catch(e){return [];}}
function drawer(){try{return document.querySelector('.mainDrawer');}catch(e){return null;}}
/* Library ids are this server's own and do not change unless a library is
   recreated. Matched on href, never on the visible label -- the drawer renders
   in en/de/zh and a text match would silently stop working on a language switch. */
/* Library-scoped entries (Playlists, Recordings) are per-install, so their
   hrefs come from config rather than a hardcoded parentId. Empty strings are
   filtered out: indexOf('') is 0, which would hide every drawer entry. */
var CFG=(window.SF_CONFIG||{});
var DROP_HREF=[].concat(
 (CFG.drawerHideHrefs||[]).filter(function(s){return s&&s.length;}),
 [
 '#/livetv?tab=1',                                    /* Guide */
 'JellyfinEnhanced/bookmarksPage',                    /* Bookmarks (plugin settings) */
 /* Hidden Content is listed TWICE: once inside .jellyfinEnhancedSection and again
    under Plugin Settings. Keep the one in the Jellyfin Enhanced section, which is
    where the feature lives, and drop the plugin-settings duplicate. */
 'JellyfinEnhanced/hiddenContentPage'
]);
function tidy(){
 var dr=drawer(); if(!dr)return;
 /* 1. drop the entries the admin does not use */
 qa('a,button',dr).forEach(function(a){
  var h=a.getAttribute('href')||'';
  for(var i=0;i<DROP_HREF.length;i++){
   if(h.indexOf(DROP_HREF[i])>-1){a.classList.add('sf-dt-hide');return;}
  }
  /* the Jellyfin Enhanced "Bookmarks" entry has no distinguishing href, so it
     is matched on its icon ligature, which is language-independent */
  var ic=a.querySelector('.material-icons');
  if(ic&&(ic.textContent||'').trim()==='bookmarks'&&!/jf-watchlist-link/.test(a.className||''))
   a.classList.add('sf-dt-hide');
 });
 /* 2. a section header whose every entry is now hidden should go too */
 qa('.sidebarHeader',dr).forEach(function(h){
  var n=h.nextElementSibling,any=false;
  while(n&&!n.classList.contains('sidebarHeader')){
   if(!n.classList.contains('sf-dt-hide')&&n.getBoundingClientRect)any=true;
   n=n.nextElementSibling;
  }
  h.classList.toggle('sf-dt-hide',!any);
 });
 /* Step 3 used to MOVE the Jellyfin Enhanced section below Media by relocating
    its nodes. That is withdrawn: the drawer is built progressively and rebuilt
    wholesale by Jellyfin, and the DOM move landed the section at the very bottom
    (below Sign Out) and left a duplicate entry near the top. Reordering here
    needs a technique that cannot duplicate or misplace nodes. */
 /* 3. Media above Jellyfin Enhanced.
    Each section is ONE self-contained wrapper inside .mainDrawer-scrollContainer
    (.customMenuOptions, .jellyfinEnhancedSection, .libraryMenuOptions,
    .adminMenuOptions, .pluginMenuOptions, .userMenuOptions). So this is a single
    node moved against a NON-NULL reference -- it cannot append to the end or
    split a section, which is exactly how the earlier nextElementSibling version
    dumped JE below Sign Out and left a duplicate behind. Idempotent: once the
    library section precedes JE the condition is false. */
 /* 4. One plugins section. Modular Home was the only live entry left under
    "Plugin Settings", so it folds into the Jellyfin Enhanced wrapper and the
    heading becomes "Plugins"; the emptied wrapper is then hidden. Guarded on
    parentage so a redundant run is a no-op. */
 var jeBox=dr.querySelector('.jellyfinEnhancedSection');
 if(jeBox){
  var mh=dr.querySelector('a[href*="ModularHomeViews"],button[href*="ModularHomeViews"]');
  if(mh&&mh.parentElement!==jeBox)jeBox.appendChild(mh);
  var jh=jeBox.querySelector('.sidebarHeader');
  if(jh&&jh.textContent.trim()!=='Plugins')jh.textContent='Plugins';
 }
 var pmBox=dr.querySelector('.pluginMenuOptions');
 if(pmBox){
  var live=[].slice.call(pmBox.querySelectorAll('a,button')).filter(function(e){
   return !e.classList.contains('sf-dt-hide');});
  pmBox.classList.toggle('sf-dt-hide',live.length===0);
 }
 var lib=dr.querySelector('.libraryMenuOptions'), jeSec=dr.querySelector('.jellyfinEnhancedSection');
 if(lib&&jeSec&&lib.parentElement&&lib.parentElement===jeSec.parentElement){
  if(jeSec.compareDocumentPosition(lib)&Node.DOCUMENT_POSITION_FOLLOWING){
   jeSec.parentElement.insertBefore(lib,jeSec);
  }
 }
}
var t=0;
function schedule(){clearTimeout(t);t=setTimeout(tidy,60);}
function watch(){
 var dr=drawer(); if(!dr)return setTimeout(watch,400);
 try{new MutationObserver(schedule).observe(dr,{childList:true,subtree:true});}catch(e){}
 tidy();
}
watch();
document.addEventListener('click',function(e){
 if(e.target&&e.target.closest&&e.target.closest('.mainDrawerButton'))schedule();
},true);
})();</script>'''


USERRAIL_MARKER = 'sf-user-rail'
USERRAIL_SCRIPT = r'''<style id="sf-user-rail">
/* sf-user-rail: the header's right-hand controls collapse into the avatar and
   expand leftward out of it. Glass is lifted verbatim from .emby-tabs-slider
   (radius 50px, rgba(30,31,36,.66), blur(20px) saturate(1.8)) so the rail reads
   as the same component family as the nav pills. */
.headerRight{align-items:center;}
/* Sources are hidden WITHOUT touching `display`: Jellyfin sets display:none on
   Cast/Player when they are unavailable, and that is the only signal we have for
   whether to offer them. A display:none of our own would erase it and the rail
   would advertise dead buttons. */
/* Music is hidden outright, not folded into the rail: the admin does not use it and
   it is still reachable from the drawer under Media. */
.headerRight > button.sf-music-btn{display:none!important;}
.headerRight > button.sf-ur-src{
  position:absolute!important;width:0!important;height:0!important;
  padding:0!important;margin:0!important;border:0!important;
  opacity:0!important;pointer-events:none!important;overflow:hidden!important;
}
.sf-ur-rail{
  /* sf-ur-noshift: height is FIXED and padding is horizontal-only. Opening used
     to add 3px of vertical padding, taking the rail 38px -> 44px, which grew
     .headerRight, grew .skinHeader, and visibly nudged the nav pills and the
     hamburger down. Never let this box change height between states. */
  display:flex;align-items:center;gap:2px;box-sizing:border-box;
  height:38px;max-width:0;padding:0;margin:0;overflow:hidden;
  border-radius:50px;background:rgba(30,31,36,0);
  backdrop-filter:blur(20px) saturate(1.8);
  -webkit-backdrop-filter:blur(20px) saturate(1.8);
  transition:max-width .34s cubic-bezier(.22,1,.36,1),
             padding .34s cubic-bezier(.22,1,.36,1),
             margin .34s cubic-bezier(.22,1,.36,1),
             background-color .28s ease,box-shadow .28s ease;
  will-change:max-width;
}
.sf-ur-rail.sf-ur-open{
  max-width:420px;padding:0 4px;margin-right:5px;
  background:rgba(30,31,36,.66);
  box-shadow:0 6px 22px rgba(0,0,0,.34);
}
.sf-ur-btn{
  flex:0 0 auto;width:38px;height:38px;border:0;border-radius:50%;
  background:transparent;color:inherit;cursor:pointer;
  display:flex;align-items:center;justify-content:center;
  opacity:0;transform:translateX(16px) scale(.84);
  transition:opacity .19s ease,transform .3s cubic-bezier(.22,1,.36,1),background-color .15s ease;
}
.sf-ur-rail.sf-ur-open .sf-ur-btn{opacity:1;transform:none;}
/* stagger: nearest the avatar arrives first, so it reads as emerging from it */
.sf-ur-rail.sf-ur-open .sf-ur-btn:nth-last-child(1){transition-delay:.02s;}
.sf-ur-rail.sf-ur-open .sf-ur-btn:nth-last-child(2){transition-delay:.05s;}
.sf-ur-rail.sf-ur-open .sf-ur-btn:nth-last-child(3){transition-delay:.08s;}
.sf-ur-rail.sf-ur-open .sf-ur-btn:nth-last-child(4){transition-delay:.11s;}
.sf-ur-rail.sf-ur-open .sf-ur-btn:nth-last-child(5){transition-delay:.14s;}
.sf-ur-rail.sf-ur-open .sf-ur-btn:nth-last-child(6){transition-delay:.17s;}
.sf-ur-btn:hover{background:rgba(255,255,255,.13);}
.sf-ur-btn:focus-visible{outline:2px solid rgba(255,255,255,.72);outline-offset:2px;}
.sf-ur-btn .material-icons{font-size:1.4em;line-height:1;}
.sf-ur-sep{flex:0 0 auto;width:1px;height:20px;margin:0 3px;background:rgba(255,255,255,.22);}
.headerUserButton{transition:box-shadow .22s ease;}
.headerUserButton.sf-ur-active{box-shadow:0 0 0 2px rgba(255,255,255,.82);}
@media (prefers-reduced-motion:reduce){
  .sf-ur-rail,.sf-ur-btn,.headerUserButton{transition:none!important;}
  .sf-ur-btn{transform:none;}
}
</style>
<script>(function(){ /* sf-user-rail */
if(window.__sfUserRail)return; window.__sfUserRail=1;
function q(s,r){try{return (r||document).querySelector(s);}catch(e){return null;}}
function qa(s,r){try{return [].slice.call((r||document).querySelectorAll(s));}catch(e){return [];}}
function hdr(){return q('.skinHeader');}
function right(){var h=hdr();return h?q('.headerRight',h):null;}
function avatar(){var h=hdr();return h?q('.headerUserButton',h):null;}
/* Jellyfin hides an unavailable control with display:none. Our own hiding is
   position/size based precisely so this test still means something. */
function available(el){
 if(!el)return false;
 try{return getComputedStyle(el).display!=='none';}catch(e){return false;}
}
/* Language and Music carry no class of their own, so tag them by ICON, never by
   the visible label -- the UI runs in en/de/zh and a text match would silently
   stop working the moment someone switches language. */
function tagSources(){
 var r=right(); if(!r)return;
 qa('button.headerButtonRight',r).forEach(function(b){
  var c=(b.className||'').toString();
  /* Search and the avatar stay outside the rail; the audio Player button is
     excluded outright -- the admin: "it is not being used". */
  /* .sf-music-btn and .sf-lang-btn are tags our own patches already put on those
     two buttons, so this stays correct in de/zh where the labels change. */
  if(/headerSearchButton|headerUserButton|headerAudioPlayerButton|sf-music-btn/.test(c))return;
  if(!b.hasAttribute('data-sf-ur')){
   var ic=q('.material-icons',b), t=(ic&&ic.textContent||'').trim();
   b.setAttribute('data-sf-ur', t||'more_horiz');
  }
  b.classList.add('sf-ur-src');
 });
 qa('.headerCastButton,.headerSyncButton',r).forEach(function(b){
  if(!b.hasAttribute('data-sf-ur'))b.setAttribute('data-sf-ur','more_horiz');
  b.classList.add('sf-ur-src');
 });
}
function drawerItem(cls){return q('.mainDrawer .'+cls)||q('.'+cls);}
/* if an earlier build tagged the Player button, untag it so it renders normally
   again rather than staying invisible with no rail entry to reach it */
function releasePlayer(){
 var r=right(); if(!r)return;
 /* anything we no longer fold in must be untagged, or an earlier build leaves it
    invisible with no rail entry to reach it */
 qa('.headerAudioPlayerButton.sf-ur-src,.sf-music-btn.sf-ur-src',r)
  .forEach(function(b){b.classList.remove('sf-ur-src');});
}
function mkBtn(iconEl,iconName,label){
 var b=document.createElement('button');
 b.type='button'; b.className='sf-ur-btn'; b.setAttribute('role','menuitem');
 b.title=label||''; b.setAttribute('aria-label',label||'');
 if(iconEl){b.appendChild(iconEl.cloneNode(true));}
 else{var s=document.createElement('span');s.className='material-icons';
      s.setAttribute('aria-hidden','true');s.textContent=iconName||'more_horiz';
      b.appendChild(s);}
 return b;
}
var rail=null, open=false;
function close(){
 if(!open)return; open=false;
 if(rail)rail.classList.remove('sf-ur-open');
 var a=avatar(); if(a)a.classList.remove('sf-ur-active');
}
/* Reconcile, do not build-once. The header is assembled progressively and
   Cast/Player come and go with playback, so the rail is rebuilt from whatever is
   actually available each time the header changes. Signature-guarded so a
   no-change mutation costs one string compare. */
var lastSig='';
function sync(){
 var r=right(), a=avatar();
 if(!r||!a)return;
 tagSources(); releasePlayer();
 var srcs=qa('button.sf-ur-src',r).filter(available);
 var st=drawerItem('btnSettings'), lo=drawerItem('btnLogout');
 var sig=srcs.map(function(b){return b.getAttribute('data-sf-ur')+':'+(b.title||'');}).join('|')
       +'#'+(st?'s':'')+(lo?'l':'');
 if(rail&&r.contains(rail)&&sig===lastSig)return;
 lastSig=sig;
 if(!rail){rail=document.createElement('div');rail.className='sf-ur-rail';rail.setAttribute('role','menu');}
 rail.innerHTML='';
 srcs.forEach(function(srcEl){
  var b=mkBtn(q('.material-icons',srcEl),srcEl.getAttribute('data-sf-ur'),srcEl.title||'');
  b.addEventListener('click',function(e){e.preventDefault();e.stopPropagation();
    try{srcEl.click();}catch(err){} close();});
  rail.appendChild(b);
 });
 /* account actions last, nearest the avatar, behind a divider */
 if(srcs.length&&(st||lo))rail.appendChild(Object.assign(document.createElement('span'),{className:'sf-ur-sep'}));
 var bS=mkBtn(null,'settings',(st&&st.textContent.trim())||'Settings');
 bS.addEventListener('click',function(e){e.preventDefault();e.stopPropagation();
   var t=drawerItem('btnSettings');
   if(t){try{t.click();}catch(err){location.hash='#/mypreferencesmenu';}}
   else location.hash='#/mypreferencesmenu';
   close();});
 rail.appendChild(bS);
 var bL=mkBtn(null,'logout',(lo&&lo.textContent.trim())||'Sign Out');
 bL.addEventListener('click',function(e){e.preventDefault();e.stopPropagation();
   var t=drawerItem('btnLogout');
   if(t){try{t.click();}catch(err){}}
   else{try{window.ApiClient&&ApiClient.logout();}catch(err){}}
   close();});
 rail.appendChild(bL);
 if(!r.contains(rail)||rail.nextSibling!==a)r.insertBefore(rail,a);
 if(open)rail.classList.add('sf-ur-open');
}
document.addEventListener('click',function(e){
 var a=avatar();
 if(a&&e.target&&(e.target===a||(e.target.closest&&e.target.closest('.headerUserButton')===a))){
  e.preventDefault(); e.stopPropagation();
  sync();
  if(!rail)return;
  open=!open;
  rail.classList.toggle('sf-ur-open',open);
  a.classList.toggle('sf-ur-active',open);
  return;
 }
 if(open&&rail&&!rail.contains(e.target))close();
},true);
document.addEventListener('keydown',function(e){if(e.key==='Escape')close();},true);
window.addEventListener('hashchange',close);
/* Scoped to .skinHeader on purpose -- a document-wide subtree observer here
   measured 1.5s of scripting on mobile in the textless-poster round. */
var t=0;
function watch(){
 var h=hdr(); if(!h)return setTimeout(watch,400);
 try{new MutationObserver(function(){
   clearTimeout(t); t=setTimeout(sync,60);
 }).observe(h,{childList:true,subtree:true,attributes:true,attributeFilter:['style','class']});}catch(e){}
 sync();
}
watch();
})();</script>'''
