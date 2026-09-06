"""jfblocks/home.py -- payload constants lifted out of jf_patch.py.

Each constant's source text (and its comments) is byte-identical to the
monolith; only its location changed. 12 constants.
"""

__all__ = [
    'MOBCARD_MARKER',
    'MOBCARD_SCRIPT',
    'NOCOUNT_MARKER',
    'NOCOUNT_SCRIPT',
    'HOME_MARKER',
    'HOME_SCRIPT',
    'ROWARROWFIX_MARKER',
    'ROWARROWFIX_SCRIPT',
    'HEROLAYOUT_MARKER',
    'HEROLAYOUT_SCRIPT',
    'HOLDROWS_MARKER',
    'HOLDROWS_STYLE',
    'HEROEDGE_MARKER',
    'HEROEDGE_SCRIPT',
    'FASTFOLD_MARKER',
    'FASTFOLD_SCRIPT',
]


HOME_MARKER = 'jf-home-tab'
HOME_SCRIPT = (
    '<script>(function(){'
    'function addHomeTab(){'
    'var page=document.querySelector("#liveTvSuggestedPage:not(.hide)");'
    'var ex=document.querySelector(".jf-home-tab");'
    'if(!page){if(ex)ex.remove();return;}'
    'if(ex)return;'
    'var slider=document.querySelector(".headerTabs.sectionTabs .emby-tabs-slider");'
    'if(!slider)return;'
    'var btn=document.createElement("button");'
    'btn.type="button";'
    'btn.className="jf-home-tab";'
    'btn.textContent="Home";'
    'btn.addEventListener("click",function(e){e.preventDefault();e.stopPropagation();var hb=document.querySelector(".headerHomeButton");if(hb){hb.click();}else{window.location.hash="#/home";}},true);'
    'slider.insertBefore(btn,slider.firstChild);'
    '}'
    'var obs=new MutationObserver(addHomeTab);'
    '/* jf-observer-scope: was document.body with subtree+attributes, so every class change anywhere re-ran this. A pane swap emits ~544 mutations, and with 4 such observers that is thousands of needless callbacks -- measured as a fixed ~1.4s tab switch. The tab slider lives inside .skinHeader, so that is the smallest correct scope. Page .hide state is still evaluated on each run, and the existing setInterval covers anything the narrower scope misses. Falls back to body if the header never appears. */'
    '(function _at(){var _t=document.querySelector(".skinHeader");'
    'if(!_t){return setTimeout(_at,300);}'
    'obs.observe(_t,{childList:true,subtree:true,attributes:true,attributeFilter:["class"]});})();'
    '})();</script>'
)

ROWARROWFIX_MARKER = 'sf-row-arrowfix'
# The row scrollers run data-scroll-mode-x="custom": jellyfin drives them itself rather
# than through native scrollLeft. Giving them overflow-x:auto (so a trackpad can scroll a
# row at all) made native scrolling work but left jellyfin's own arrows dead -- verified
# with a REAL click: scrollLeft 0 before and after. So we drive them natively instead.
# NB the name: 'sf-row-arrows' is ALREADY taken by the arrows on our injected rows.
#
# The LEFT arrow then still did nothing, and the reason was not the click handler: jellyfin
# disables the left button (the real HTML `disabled` attribute, opacity .3) while its own
# scroller thinks it is at position 0, and our native scrollBy never updates that internal
# state. Measured: scrollLeft 958 with the left button still disabled, so it fired no click
# at all. Keep the two buttons' disabled state in sync with the ACTUAL scroll position.
# Scroll events do not bubble, hence the capture-phase document listener -- that catches
# every row, including ones added long after load, with no per-row wiring.
ROWARROWFIX_SCRIPT = ('<script>(function(){/* sf-row-arrowfix */'
                      # sf-arrow-realscroller (2026-09-04). The admin: "the arrows for rows
                      # in favorites tab do not work." They were DISABLED, so they fired
                      # no click at all -- neither this handler's nor any other.
                      # sync() measured whatever it was handed, and the interval below
                      # always hands it `.emby-scroller`. On home that is the element
                      # that scrolls, but on My Stuff the overflow sits one level in:
                      #     home      .emby-scroller  sw 8010 cw 1426   <- scrolls
                      #     My Stuff  .emby-scroller  sw 1440 cw 1440   <- no overflow
                      #               .itemsContainer.scrollSlider sw 2681 cw 1365
                      # so max came out 0, `max<=2` disabled BOTH buttons, and a
                      # disabled button is inert. The click walk below already resolves
                      # the real scroller correctly; sync has to use the same rule or it
                      # switches off the very control that walk exists to serve.
                      'function realsc(sec,fb){try{'
                      'var c=sec.querySelectorAll(".emby-scroller,.itemsContainer"),k;'
                      'for(k=0;k<c.length;k++){if(c[k].scrollWidth>c[k].clientWidth+4)return c[k];}'
                      '}catch(e){}return fb;}'
                      'function sync(sc){try{'
                      'var sec=sc.closest&&sc.closest(".verticalSection");if(!sec)return;'
                      'var btns=sec.querySelectorAll(".emby-scrollbuttons button");'
                      'if(!btns.length)return;'
                      'sc=realsc(sec,sc);'
                      'var max=sc.scrollWidth-sc.clientWidth;'
                      'for(var i=0;i<btns.length;i++){var b=btns[i];'
                      'var isRight=!!b.querySelector(".chevron_right");'
                      'var off=isRight?(sc.scrollLeft>=max-2):(sc.scrollLeft<=2);'
                      'if(max<=2)off=true;'
                      'if(off){b.setAttribute("disabled","");}else{b.removeAttribute("disabled");}'
                      '}}catch(e){}}'
                      'document.addEventListener("scroll",function(e){'
                      'var t=e.target;'
                      'if(t&&t.classList&&t.classList.contains("emby-scroller"))sync(t);'
                      '},true);'
                      'document.addEventListener("click",function(e){try{'
                      'var t=e.target;if(!t||!t.closest)return;'
                      'var btn=t.closest(".emby-scrollbuttons button");if(!btn)return;'
                      # sf-arrow-oneowner (2026-08-30). Two guards, both about
                      # ownership. Our injected rows (Watchlist / Live TV / Music /
                      # Audiobooks) reuse Jellyfin's button CLASSES so they inherit the
                      # native look -- which means this delegated handler matched them
                      # too. They have no .emby-scroller of their own, so the walk below
                      # climbed out of the row and took the first scrollable box it
                      # found in the sections container: Continue Watching's. One press
                      # on Watchlist scrolled Watchlist AND Continue Watching, exactly
                      # as reported. Those rows already have their own handler, so skip
                      # them outright.
                      'if(btn.closest(".sf-row-arrows"))return;'
                      # sf-arrow-walk (2026-08-28): this used to be
                      #   sec = btn.closest('.verticalSection'); sc = sec.querySelector('.emby-scroller')
                      # Home keeps a cached copy of the view per URL, so #homeTab and its
                      # sections legitimately exist more than once -- that lookup could resolve
                      # against the wrong copy. Measured on Continue Watching: the handler saw
                      # scFound=false while the visible row plainly had a scroller, so it hit
                      # `if(!sc)return` and the arrow was a no-op.
                      # Walk up from the BUTTON and take the first ancestor that actually
                      # contains a scrollable box: that is the row the user clicked, whichever
                      # copy of the view it belongs to.
                      'var own=btn.closest(".verticalSection");'
                      'var sc=null,p=btn.parentElement,g,k,i=0,cand;'
                      # bound the climb to the row the button lives in. Walking up from
                      # the BUTTON is still right (it survives the cached duplicate views
                      # described above), but leaving the row never is -- that is how a
                      # neighbour's scroller got picked.
                      'while(p&&!sc&&i<12){i++;'
                      'if(own&&!own.contains(p))break;'
                      'cand=p.querySelectorAll(".emby-scroller,.itemsContainer");'
                      'for(k=0;k<cand.length;k++){g=cand[k];'
                      'if(g.scrollWidth>g.clientWidth+4){sc=g;break;}}'
                      'p=p.parentElement;}'
                      'if(!sc)return;'
                      'var right=!!btn.querySelector(".chevron_right");'
                      'var d=Math.max(220,Math.round(sc.clientWidth*0.85));'
                      'var before=sc.scrollLeft;'
                      'sc.scrollBy({left:right?d:-d,behavior:"smooth"});'
                      # these scrollers run data-scroll-mode-x="custom", so a smooth scrollBy
                      # is not always honoured. If nothing actually moved, set the position
                      # outright -- pressing the arrow must never be a no-op.
                      'setTimeout(function(){try{'
                      'if(Math.abs(sc.scrollLeft-before)<2)sc.scrollLeft=before+(right?d:-d);'
                      'sync(sc);}catch(e2){}},380);'
                      'setTimeout(function(){sync(sc);},900);'
                      '}catch(err){}},true);'
                      'setInterval(function(){try{'
                      # sweep the SECTIONS: a row whose scroller is the inner
                      # .itemsContainer has no .emby-scroller to be found by, so it
                      # was never swept and its arrows kept whatever state they were
                      # last left in.
                      'var all=document.querySelectorAll(".verticalSection");'
                      'for(var i=0;i<all.length;i++){var s0=realsc(all[i],null);if(s0)sync(s0);}'
                      '}catch(e){}},1500);'
                      '})();</script>')

HEROLAYOUT_MARKER = 'jf-hero-layout'
HEROLAYOUT_SCRIPT = r'''<script>(function(){ /* jf-hero-layout */
var MINW=768;
function num(v){return parseFloat(v)||0;}
function slide(){return document.querySelector('#slides-container .slide.active')||document.querySelector('#slides-container .slide');}
/* jf-view-scope: #homeTab is duplicated once Jellyfin caches a second home
   view, so scope to the instance on screen rather than the first in the DOM. */
/* sf-sections-visible: resolve the container that is ON SCREEN, not the one a
   cached view hands back. Jellyfin keeps one view per URL, so returning to home
   from Live TV can leave TWO #indexPage instances in the DOM, and
   __jfView.homeTab() kept answering with the stale hidden one. The fitter then
   dutifully positioned a container nobody could see while the visible one was
   never given a `top` at all -- so the rows sat directly under the header, on
   top of the hero. Reproduced 3/3 going Live TV -> hamburger -> Home:
       scTop stayed 489px          (the hidden instance, being fitted)
       rowT  118, once -277        (the visible instance, unpositioned)
       rows overlapped the hero buttons by up to 752px
   Derive it from the row we are actually fitting: whatever holds the visible
   first row IS the container that has to move. Falls back to a visibility scan,
   then to the old lookup, so a home page with no rows yet still resolves.
   See [[jellyfin-duplicate-page-instances]] -- querySelector lies here. */
function sections(){
var row=firstRow();
if(row&&row.closest){var rc=row.closest('.sections.homeSectionsContainer');if(rc)return rc;}
var all=document.querySelectorAll('.sections.homeSectionsContainer'),i,e,pgw;
for(i=0;i<all.length;i++){e=all[i];
if(e.offsetParent===null)continue;
pgw=e.closest?e.closest('.page'):null;
if(pgw&&pgw.classList.contains('hide'))continue;
return e;}
var h=window.__jfView&&window.__jfView.homeTab();
return h?h.querySelector('.sections.homeSectionsContainer'):null;}
function firstRow(){
var secs=document.querySelectorAll('#indexPage:not(.hide) .verticalSection');
for(var i=0;i<secs.length;i++){
if(secs[i].querySelector('.card')&&secs[i].getBoundingClientRect().height>0)return secs[i];}
return null;}
function clearAll(){
var s=slide();if(s){
['.logo-container','.info-container','.genre','.plot-container','.button-container'].forEach(function(sel){
var e=s.querySelector(sel);if(!e)return;
e.style.removeProperty('top');e.style.removeProperty('transform');
e.style.removeProperty('left');e.style.removeProperty('height');e.style.removeProperty('max-height');});}
/* the band is written to every slide now, so it has to be cleared from every
   slide too -- otherwise a narrow viewport keeps a stale fixed height */
var lcs=document.querySelectorAll('.slide .logo-container'),li;
for(li=0;li<lcs.length;li++){lcs[li].style.removeProperty('height');lcs[li].style.removeProperty('max-height');}
}
function dropRowTop(){var sc=sections();if(sc)sc.style.removeProperty('top');}
/* Media Bar leaves .button-container at height 0 on a phone, with its children
   centred on that zero-height line, so offsetHeight is 0 and the container's own
   bottom sits ~22px ABOVE the buttons you can actually see. Take the furthest
   child instead, or the floor below is measured against the wrong edge. */
function btnBottom(btns,slideEl){
var y=btns.offsetTop+btns.offsetHeight,kids=btns.children,i,kb,cr;
for(i=0;i<kids.length;i++){
kb=btns.offsetTop+kids[i].offsetTop+kids[i].offsetHeight;
if(kb>y)y=kb;}
if(slideEl)return slideEl.getBoundingClientRect().top+y;
var rb=btns.getBoundingClientRect().bottom;
for(i=0;i<kids.length;i++){cr=kids[i].getBoundingClientRect();if(cr.bottom>rb)rb=cr.bottom;}
return rb;}
/* sf-phone-btnfloor: below MINW the HERO is Media Bar's, but the ROW POSITION
   still has to respect it. sf-fold-short pulls the rows up by
   `min(52vh, max(100vh - 420px, 30vh))` so the first card clears the fold, and
   that formula knows nothing about where the Play button ended up. On a real
   iPhone -- 390x664 once Safari's toolbars are showing, not the 390x844 the CSS
   was tuned against -- it resolves to 244px and puts the rows, which carry
   z-index 6, straight over the buttons: measured Play/Info at y=383-427 with
   'Continue Watching' starting at y=411. They were painted over, so the primary
   action of the whole app was invisible on a phone.
   fitRow already carries exactly the right rule -- the row title must clear the
   button row -- so run that part here. layoutSlide stays OFF below MINW: Media
   Bar owns the phone hero and fighting it put the Play button at left:-29px. */
/* sf-phone-btngap: close the hole the hidden synopsis leaves.
   Media Bar drops .plot-container in portrait, but nothing reclaims the space
   it was occupying, so the phone stack read (measured 390x664):
       chips bottom 294 -> bar 309   15px
       bar bottom 312   -> buttons 383   71px
   against 10/15/15 on desktop, where the synopsis fills that band. The admin: 'the
   spacing between the progress bar and buttons could be better'.
   Anchored off the CHIPS, not off the bar: the bar only exists on a resume
   slide, so anchoring to it would move the buttons whenever the carousel
   rotated onto a Next Up card. The bar's own band (3px rule + its 15px gap) is
   reserved unconditionally instead, which keeps the buttons at one height on
   every slide -- the same reason layout() lays out all slides rather than the
   active one.
   Only `top` is written. Media Bar centres this row with
   `left:50%; transform:translateX(-50%) scale(.95)`, and that must survive --
   the desktop path's `transform:none` is what once put Play at left:-29px. */
var BAR_BAND=18;
/* OFFSETS, NEVER RECTS -- the same trap layoutSlide documents above, and the
   first version of this function walked straight into it. sf-hero-motion
   animates `translate` on the chips and the button row, and a rect INCLUDES
   that translate, so anchoring off `info.getBoundingClientRect().bottom` made
   the buttons chase the entrance animation frame by frame. Measured on an
   iPhone 13: the row stepped 405 -> 378 -> 352 -> 349 -> 347 -> 340 over half a
   second while the chips' LAYOUT position never moved at all. That is the
   'button jumps up slightly after it loads'. offsetTop/offsetHeight are layout
   values and are blind to transforms, so the placement is settled from the
   first pass and the animation plays over it. */
function offTopIn(el,root){var y=0,n=el;while(n&&n!==root){y+=n.offsetTop;n=n.offsetParent;}return y;}
function phoneBtns(s){
if(!s)return;
var btns=s.querySelector('.button-container');if(!btns)return;
var info=s.querySelector('.info-container');if(!info||info.offsetHeight<1)return;
var H=window.innerHeight;
var G=Math.max(18,Math.min(40,Math.round(H*0.042)));
/* Reserve the bar's band ONLY on a slide that actually has a bar. The admin: 'on
   heros with no progress bar it can be moved up a little more.' Every slide
   owns its own .button-container and slides cross-fade rather than sliding, so
   a per-slide difference is never seen as movement. */
var bar=s.querySelector('.sf-cw-prog');
var band=(bar&&bar.offsetHeight>0)?BAR_BAND:0;
/* the container is height 0 with its buttons centred on that line, so each
   child carries a NEGATIVE offsetTop -- exactly how far the visible row starts
   above the container's own top. Add it back or the row lands half a button
   too high. */
var kids=btns.children,lift=0,i;
for(i=0;i<kids.length;i++){if(kids[i].offsetHeight>1&&-kids[i].offsetTop>lift)lift=-kids[i].offsetTop;}
var want=Math.round(offTopIn(info,s)+info.offsetHeight+band+G+lift);
var w=want+'px';
if(btns.style.top!==w){
btns.style.setProperty('top',w,'important');
btns.style.setProperty('bottom','auto','important');
/* Re-arm the row fitter ONLY for the slide it actually measures against.
   This runs over every slide so a card is never laid out for the first time at
   the moment it becomes active, but an inactive slide repainting is not a
   reason to restart the fit -- and refit() clears the settle counter, so an
   unconditional call here meant the counter was reset on almost every pass and
   the row was never placed at all. It survived on the CSS fallback alone. */
if(s===slide())refit();}}
function phoneFit(){
var s=slide();
var btns=s?s.querySelector('.button-container'):null;
if(!s||!btns){dropRowTop();return;}
var all=document.querySelectorAll('.slide'),k;
for(k=0;k<all.length;k++)phoneBtns(all[k]);
var H=window.innerHeight;
var gap=Math.max(10,Math.min(24,Math.round(H*0.017)));
fitRow(btns,gap,s);}
/* Lay out EVERY slide, not just the active one.
   Media Bar keeps its slides in the DOM at opacity 0 (display is block and they
   measure normally -- verified: an inactive slide reports the full 727px height
   and a real logo band), so a slide that had never been on screen had no inline
   geometry at all and sat at its static position. Measured on slide 4 of a
   rotation: the chip row at 193px against the 210px every laid-out slide uses.
   It was corrected the instant the slide went active, which is precisely the
   "everything shuffles for a moment" the hero was doing.
   Laying all of them out up front means becoming active changes opacity and
   nothing else. Cost is a handful of extra measurements on a 1s tick. */
/* sf-paint-first: paint the active slide, THEN measure it.
   sf-hero-nojitter already made the layout decision synchronous inside
   sfHeroResume -- the .sf-cw class, the episode band and the progress bar are
   all decided from sfCwMap without waiting on getItem. But sfHeroResume runs on
   the 400ms tick, and this layout runs on its own schedule, so the two could
   still land in either order. When layout won the race it measured a slide that
   had no progress bar yet, reserved no band for one, and then had to move the
   button row down 18px once the bar appeared. Measured on an iPhone 13:
       t=1223  buttons placed at 322   (no bar yet, band 0)
       t=1438  bar appears, band 18    buttons re-placed at 340  <-- the hop
   the admin: 'when the button loads in, it jumps up slightly after it loads'.
   One synchronous call makes the order explicit instead of lucky. It is cheap:
   sfHeroResume returns immediately once it has processed the active slide. */
function layout(){
try{if(window.__sfHeroResume)window.__sfHeroResume();}catch(e){}
if(window.innerWidth<MINW){clearAll();phoneFit();return;}
var all=document.querySelectorAll('.slide'),k;
for(k=0;k<all.length;k++)layoutSlide(all[k]);}
function layoutSlide(s){
if(!s)return;
var logo=s.querySelector('.logo-container'),info=s.querySelector('.info-container'),
genre=s.querySelector('.genre'),plotC=s.querySelector('.plot-container'),
plot=s.querySelector('.plot'),btns=s.querySelector('.button-container');
if(!info||!plotC||!btns)return;
var H=window.innerHeight;
var gap=Math.max(10,Math.min(24,Math.round(H*0.017)));
var small=Math.max(7,Math.round(gap*0.75));
/* Measure with offsetTop/offsetHeight, NEVER getBoundingClientRect.
   sf-hero-motion animates `translate` on these very rows, and a rect INCLUDES
   that translate -- so every row was positioned from where its neighbour was
   momentarily drawn rather than from where it sits. Because the rows are chained
   (chips off the logo, synopsis off the chips, buttons off the synopsis) and each
   carries a different animation delay, the error compounded down the card:
   measured chips -14px, synopsis -28px, buttons -39px, arriving at 361ms when the
   card is already half faded in. That was the "layout shifts up after a second".
   offsetTop/offsetHeight are layout values and translate is invisible to them, so
   the layout pass and the entrance animation can no longer interact at all.
   Slide-relative, walking the offsetParent chain: every row's offsetParent is the
   slide except .plot, which nests inside .plot-container. */
function offTop(el){var y=0,n=el;while(n&&n!==s){y+=n.offsetTop;n=n.offsetParent;}return y;}
function bottomOf(el){return offTop(el)+el.offsetHeight;}
function place(el,y){el.style.setProperty('transform','none','important');
el.style.setProperty('top',Math.round(y)+'px','important');}
/* The logo band is a fixed height rather than the image's own: the stylesheet
   default is 124px and the viewport-derived value here is 113px, so a band left
   unsized snapped by 11px the moment its slide went active, carrying the chip
   row, the progress bar and the description with it. Every slide gets it now
   (see layout()), so the band never changes height. */
if(logo){var lh=Math.max(72,Math.min(190,Math.round(H*0.155)));
logo.style.setProperty('height',lh+'px','important');
logo.style.setProperty('max-height',lh+'px','important');}
/* alignment: whatever x the synopsis actually sits at, the buttons match */
btns.style.setProperty('transform','none','important');
btns.style.setProperty('left',plotC.offsetLeft+'px','important');
var y=logo?bottomOf(logo):Math.round(H*0.25);
place(info,y+gap);
y=bottomOf(info);
if(genre&&genre.offsetHeight>0){place(genre,y+small);y=bottomOf(genre);}
place(plotC,y+gap);
var tb=(plot&&plot.offsetHeight>0)?bottomOf(plot):bottomOf(plotC);
place(btns,tb+gap);
fitRow(btns,gap,s);}
/* Published for the slide-change observer in the home script: a new hero should
   be positioned when it arrives, not up to a tick later. */
window.__jfHeroLayout=layout;
/* The hero extras must use the SAME threshold as the layout that makes room for
   them -- below MINW this whole layout bails, so anything that assumes it ran
   has to stand down too. Published rather than duplicated so the two can never
   drift apart. */
window.__jfHeroWide=function(){
if(window.innerWidth>=MINW)return true;
/* Phones get the progress bar back. It was dropped here because Media Bar's
   hero rows are absolutely positioned 9-12px apart, leaving no band to put it
   in -- an early version drew straight over the genre line. That is no longer
   true: sf-hero-tighten re-anchors the logo and badges upward from the
   buttons, which opens roughly 30px of clean space above them, and the CSS
   places the bar in it.
   Phones only, not everything below MINW. The awkward middle -- a narrow
   desktop window between 520 and MINW -- is the case the original guard was
   really protecting, and it is not re-anchored, so it still has no room. */
return window.innerWidth<=520;
};
function scrollNow(){return window.pageYOffset||document.documentElement.scrollTop||0;}
var fitted=false,fittedEl=null,stable=0,armedAt=Date.now(),lastCb=-1,lastTop='';
/* sf-rowtop-remember: this fitter derives the rows' top from where the HERO's
   buttons end, so it cannot settle until the hero's content has loaded -- and
   until it does, the rows sit at the stylesheet default and then move. Measured
   on a cold load: css top 567px at t=1.9s, then an inline 607.8px at t=9.8s, so
   the first row jumped 41px nine seconds in. That is the "the hero loading
   shifts the rows" report, and no amount of reserving the hero's HEIGHT fixes it
   because the input is the hero's CONTENT.
   The settled value only depends on the viewport, so remember it per size and
   apply it on the next visit before the hero has loaded anything. The fitter
   still runs and still owns the property; it now converges on the value already
   applied, so there is nothing to see. First ever visit at a given size is
   unchanged. */
var ROWKEY='sf-rowtop';
function rowKey(){return ROWKEY+':'+Math.round(innerWidth)+'x'+Math.round(innerHeight);}
try{var _seed=localStorage.getItem(rowKey());if(_seed)lastTop=_seed;}catch(e){}
var lastHeroH=0,lastParTop=-1;
function refit(){fitted=false;stable=0;armedAt=Date.now();lastCb=-1;}
function fitRow(btns,gap,slideEl){
var sc=sections();if(!sc)return;
/* Re-arm when the hero changes height. The latch below stops adjusting after two
   stable readings, and it was locking against Media Bar's own 90vh -- the
   branding stylesheet is injected into a body div AFTER boot, so the phone
   height override lands later and the row was already fitted and never looked
   again. Symptom: shrinking the hero moved nothing at all, and the first
   Continue Watching card stayed 85px below the fold with its title off screen.
   Cheap to check and it only fires when the height genuinely differs. */
var heroEl=document.getElementById('slides-container');
var heroH=heroEl?Math.round(heroEl.getBoundingClientRect().height):0;
if(heroH&&heroH!==lastHeroH){lastHeroH=heroH;refit();}
/* sf-hdr-rearm: the header is the OTHER thing that moves everything below it.
   Around 1200px wide its pill bar wraps to a second line and .skinHeader goes
   77px -> 125px, which eventually pushes the hero and the rows down 48px.
   Watch the ORDER -- measured at frame resolution shrinking 1200 -> 1180:
       t=44ms   header is already 125   content top still 101
       t=117ms  fitRow runs, reads the STALE 101, writes top=522.77
       t=239ms  content top finally becomes 149; nothing re-runs
   The header's own height changes synchronously with the media query, but the
   offset it pushes onto everything below lands ~195ms later. So keying this
   re-arm on header HEIGHT does not work: it has already settled before fitRow
   is first called, and the one call that matters measures pre-shift geometry,
   sees two stable readings and latches. The first row then sat 48px past the
   fold for good -- at 1180x900, cardBottom 948 against a 900 fold with 220px of
   clearance to the hero buttons, i.e. plenty of room, the fitter had simply
   stopped looking. Key on the container's own offset instead: that is the thing
   that actually moves the rows, whatever caused it.
   Same shape as the heroH check above and just as cheap. */
var scPar=sc.parentElement;
var parTop=scPar?Math.round(scPar.getBoundingClientRect().top+scrollNow()):0;
if(parTop!==lastParTop){lastParTop=parTop;refit();}
if(sc!==fittedEl){fittedEl=sc;
/* sf-rowtop-seedfirst: apply the remembered position BEFORE the first refit,
   not after it. refit() writes an inline top of its own, so the provisional
   apply below (`!sc.style.top`) could never fire on a fresh container -- the
   rows drew at the fitter's early guess and then moved when the hero's content
   finally landed. Seeding first means the container starts at the value this
   viewport settled on last time, and the fitter converges on the same number
   with nothing visible in between. */
if(lastTop&&!sc.style.top)sc.style.setProperty('top',lastTop,'important');
refit();
/* sf-row-provisional: a brand new container starts with NO inline top, so for
   the frames between the rows rendering and this fitter converging they draw at
   the CSS default -- directly under the header, on top of the hero. That is the
   'rows load overlaid the hero' when returning from Live TV: measured rowT=118
   against hero buttons ending at 476, a 358px overlap lasting ~250ms.
   The viewport has not changed, so the value we last settled on is right; apply
   it at once and let the normal fit refine it. Only when the element has no top
   of its own, so this can never fight a real measurement. */
if(lastTop&&!sc.style.top)sc.style.setProperty('top',lastTop,'important');}
/* sf-fit-sanity: never stay latched in a state where the rows cover the hero.
   fitted is a one-way latch and its only re-arms are a hero height change, the
   container moving, or the container being swapped. Coming back to home from
   Live TV, Jellyfin builds a SECOND #indexPage; this fitter measured across the
   swap, wrote a value from geometry that belonged to the outgoing page, and
   latched on it. Measured 3/3: the visible container held top:17.19px with its
   first row at y=118 while the hidden one held a healthy 403.9px -- rows drawn
   straight over the hero, and it never recovered. want computed to 489 the
   whole time; calling __jfHeroLayout() by hand three times changed nothing,
   because the latch short-circuits before the write.
   So verify the latch instead of trusting it: if the first row's title is above
   the hero buttons, the fit is wrong no matter what the latch says. Re-arming
   cannot loop -- the correction moves the title below the buttons (that is what
   the floor further down guarantees), after which this stops firing. */
if(fitted&&btns){
var rw0=firstRow();
var ti0=rw0?rw0.querySelector('.sectionTitle'):null;
if(ti0&&ti0.getBoundingClientRect().top<btnBottom(btns,slideEl))refit();}
if(fitted)return;
if(scrollNow()>4)return;
/* sf-fit-wait-anim (2026-08-29). This fitter pins the first row's card bottoms
   to the fold using getBoundingClientRect, and rect INCLUDES transforms. The
   home rows now flow in with sfHomeIn (translateY(20px) -> 0, `both` fill), so
   while that animation is delayed or running every card reads 20px low. The
   sf-row-settle repeat-guard below does not save us: during the delay phase the
   row is held at a CONSTANT +20px, so two consecutive samples agree and the
   fitter happily latches on a position the rows are only passing through -- it
   put the settled first row at 570 instead of 590, every run.
   Measure only once the rows have stopped moving. */
try{
/* sf-fit-wait-anynames (2026-08-29). This guard named `sfHomeIn` literally, so
   renaming the entrance to the alternating sfFinA/sfFinB pair (needed to make
   the animation actually restart) silently switched the guard OFF: the fitter
   went back to measuring rows that were still 20px low and latching a position
   they were only passing through, then correcting -- "the first row floats in
   and then jumps back down". Measured 20-42px of resting-position travel per
   Live TV -> Home, against 0px before the rename.
   Match the whole family by prefix so adding another entrance name cannot
   quietly disarm it again. */
if(sc.getAnimations&&sc.getAnimations({subtree:true}).some(function(a){
return a.playState==='running'&&/^(sfHomeIn|sfFin)/.test(a.animationName||'');}))return;
}catch(e){}
var row=firstRow();if(!row)return;
var cards=row.querySelectorAll('.card');if(!cards.length)return;
var cb=0;for(var i=0;i<cards.length;i++){var b=cards[i].getBoundingClientRect().bottom;if(b>cb)cb=b;}
/* sf-row-settle: place the row ONCE, against cards that have stopped growing.
   This fitter pins the first row's card bottom to the fold, so while the
   artwork is still loading its target keeps moving and every pass wrote a new
   position. Measured on an iPhone 13 after the hero was already settled:
       t=1569  row 373
       t=2074  row 391
       t=2471  row 401
   Three placements over 900ms -- the admin: 'it also makes my first row continue
   watching shift as well, which shouldnt be'. Requiring the measurement to
   REPEAT before acting costs one extra pass and turns that into a single write.
   Rounded, because the raw rect is fractional and would never repeat exactly.
   refit() clears this, so a resize still re-fits immediately. */
var cbR=Math.round(cb);
if(cbR!==lastCb){lastCb=cbR;return;}
var cur=num(getComputedStyle(sc).top);
var want=cur+(window.innerHeight-(cb+scrollNow()));
var title=row.querySelector('.sectionTitle');
/* Same trap as layout(): the button row's own rect carries the entrance
   animation's translate, so this floor -- which drives the whole sections
   container, i.e. everything below the hero -- would be set from a position the
   row is only passing through. offsetTop is relative to the slide, and the slide
   itself is never translated, so slideRect.top + offsetTop is the settled
   position in viewport coordinates. */
if(title&&btns){
var bb=slideEl?(btnBottom(btns,slideEl))
              :btnBottom(btns,null);
var floor=cur+(bb+gap-title.getBoundingClientRect().top);
if(want<floor)want=floor;}
if(Math.abs(want-cur)<0.5){if(++stable>=2||Date.now()-armedAt>6000)fitted=true;return;}
stable=0;
lastTop=want+'px';
try{localStorage.setItem(rowKey(),lastTop);}catch(e){}
sc.style.setProperty('top',lastTop,'important');}
var t=null;
/* Two passes: 60ms keeps the drag responsive, and a second one after the 400ms
   tick has had its say catches any header/hero height change that lands later.
   Without it the re-arm above would wait on setInterval(layout,2000). */
var t2=null,raf=0;
/* Three passes, cheapest first. The rAF one is what removes the VISIBLE jump:
   it runs before the next paint, so a header wrap and the row correction that
   answers it land in the same frame instead of a frame or two apart. The two
   timers stay because rAF is suspended in a background tab -- this is an extra
   pass, never the gate. 60ms rides out a fast drag (each resize restarts it),
   520ms is the backstop for anything that settles late. */
function schedule(){clearTimeout(t);t=setTimeout(layout,60);
clearTimeout(t2);t2=setTimeout(layout,520);
try{if(raf)cancelAnimationFrame(raf);raf=requestAnimationFrame(function(){raf=0;layout();});}catch(e){}}
/* sf-hdr-var-first: update --sf-hdr-h BEFORE scheduling the fit. Both run off
   the same resize event, and the header variable drives .page padding-top, i.e.
   the position of everything this fitter is about to measure. Left to two
   independent listeners the order is registration order and the 60ms pass below
   still raced it -- measured the variable landing at 68ms, the fit at 60ms, so
   the first row kept jumping 48px on a fast drag across the 1200px wrap. Calling
   it inline makes the ordering explicit rather than lucky. */
window.addEventListener('resize',function(){
try{if(window.__sfHdrVar)window.__sfHdrVar();}catch(e){}
refit();schedule();});
window.addEventListener('hashchange',schedule);
/* childList only -- observing attributes would re-fire on our own style writes */
try{new MutationObserver(schedule).observe(document.body,{childList:true,subtree:true});}catch(e){}
setInterval(layout,2000);
schedule();
})();</script>'''

HOLDROWS_MARKER = 'sf-holdrows'
# sf-holdrows (2026-08-28). Home sections are placed by CSS `order` but render
# whenever their own query returns, so a high-order row paints into a low-order
# row's slot and is shoved down when the real one lands (measured: Recently Added
# Movies first at y=568, then -630px in two jumps as Next Up and Continue Watching
# arrived). Reserving the slots was tried and reverted -- the reservation itself
# landed after the first row had painted, and removing it was not atomic with the
# row's arrival, which put Continue Watching at y=-115 mid-transition.
#
# So gate the REVEAL instead of reserving space. Rows stay in flow and keep
# `visibility:hidden` -- NOT display:none, which would stop their card artwork
# being fetched and trade the jump for a flash of empty cards. They therefore
# take their real space and settle into final position while invisible; the
# skeleton is lifted out of flow to overlay the fold so the user sees it rather
# than a blank. When the hold releases, rows simply become visible where they
# already are and the skeleton goes: nothing moves.
HOLDROWS_STYLE = ('<style id="sf-holdrows">'
                  '.sf-hold{position:relative!important;}'
                  '.sf-hold .verticalSection{visibility:hidden!important;}'
                  '.sf-hold .sf-skel{position:absolute!important;left:0;right:0;top:0;z-index:2;}'
                  '</style>')


HEROEDGE_MARKER = 'sf-hero-edge'
HEROEDGE_SCRIPT = r'''<style id="sf-hero-edge">
/* sf-hero-edge: the hero's chevrons are hidden and the outer thirds of the hero
   become the control instead. opacity+pointer-events only -- `display` is left to
   Media Bar, which toggles it on hover, and a click still needs to reach the real
   element so its own handler runs. */
#slides-container .arrow,
#slides-container .left-arrow,
#slides-container .right-arrow{
  opacity:0!important;pointer-events:none!important;
}
/* sf-hero-nodots: the slide-position dots are unused here and they FLASH during
   load -- Media Bar mounts them before it has slides, so they appear as a row of
   pips over the top of the hero and then vanish. display:none, not opacity, so
   they never occupy space or take a tap. */
#slides-container .dots-container,
#slides-container .dots,
#slides-container .dot-container{display:none!important;}
/* sf-no-livetv-row: the admin -- "remove the live tv row from my and all my users
   homepage". Hidden rather than un-built: the row is created by the shared home
   tick, and hiding it here removes it for every user without touching that
   builder's other work. Its query is ranked LAST in sf-fastfold so it no longer
   competes with rows people can actually see. */
#indexPage .verticalSection.sf-livetvrow{display:none!important;}
/* sf-gutter: <html> is the scrolling element here (scrollH 3825 vs 900 viewport)
   and its scrollbar-gutter was `auto`, so the bar only appears once the rows have
   made the page taller than one screen -- taking ~15px of width with it and
   shifting every centred element sideways mid-load. Reserving the gutter from the
   first paint keeps the layout still. overflow-y:scroll is the same trick for
   engines without scrollbar-gutter. */
html{scrollbar-gutter:stable;}
@supports not (scrollbar-gutter: stable){ html{overflow-y:scroll;} }
/* a click target that reads as one: the edges take a directional cursor on
   pointer devices, and nothing changes on touch */
@media (hover:hover){
  #slides-container.sf-he-l{cursor:w-resize;}
  #slides-container.sf-he-r{cursor:e-resize;}
}
</style>
<script>(function(){ /* sf-hero-edge */
if(window.__sfHeroEdge)return; window.__sfHeroEdge=1;
var EDGE=0.18, MINEDGE=90;
function sc(){try{return document.getElementById('slides-container');}catch(e){return null;}}
/* Never hijack a real control. The hero carries Play/Resume, Info, the dots and
   (on our build) a progress bar -- a click on any of those must reach it. */
function isControl(t){
 /* Only things you can actually operate. .info-container was in this list and it
    spans the hero's whole left side (logo, plot, metadata), so the left zone
    bailed out on every click while the right zone -- which it does not cover --
    worked. Text is not a control. */
 /* .sf-cw-prog is deliberately NOT here: it is a display-only progress bar that
    spans much of the hero's left side, and listing it made every left-edge click
    bail out. Only genuinely operable things belong in this list. */
 try{return !!(t&&t.closest&&t.closest('button,a,input,select,textarea,[role=button],.button-container,.dots-container'));}
 catch(e){return false;}
}
function zone(e,c){
 var r=c.getBoundingClientRect();
 if(r.width<2)return 0;
 /* The home rows overlay the bottom of the hero box, so a click down there is
    not the hero at all -- act only in its upper band. */
 var y=e.clientY-r.top;
 if(y<0||y>r.height*0.72)return 0;
 var x=e.clientX-r.left, edge=Math.max(MINEDGE,r.width*EDGE);
 if(x<=edge)return -1;
 if(x>=r.width-edge)return 1;
 return 0;
}
document.addEventListener('click',function(e){
 /* Only real user clicks. The proxy below dispatches .click() on the arrow, and
    a programmatic click carries clientX=0 -- which lands inside the LEFT zone and
    re-entered this handler on its own synthetic event, so the slide never moved. */
 if(!e.isTrusted)return;
 var c=sc(); if(!c)return;
 if(!e.target||!e.target.closest||!e.target.closest('#slides-container'))return;
 if(isControl(e.target))return;
 var z=zone(e,c); if(!z)return;
 var a=c.querySelector(z<0?'.arrow.left-arrow, .left-arrow':'.arrow.right-arrow, .right-arrow');
 if(!a)return;
 e.preventDefault(); e.stopPropagation();
 /* React binds at the root and listens for click, but the arrow may also be
    driven by pointer events -- send the whole sequence so either wiring fires. */
 try{
  var r=a.getBoundingClientRect(), px=Math.round(r.left+r.width/2)||1, py=Math.round(r.top+r.height/2)||1;
  ['pointerdown','mousedown','pointerup','mouseup','click'].forEach(function(t){
   var Ev=(t.indexOf('pointer')===0&&window.PointerEvent)?PointerEvent:MouseEvent;
   a.dispatchEvent(new Ev(t,{bubbles:true,cancelable:true,composed:true,clientX:px,clientY:py}));
  });
 }catch(err){try{a.click();}catch(e2){}}
},true);
/* cursor affordance follows the pointer; class on the container so it costs one
   class toggle rather than a style write per move */
var last=0;
document.addEventListener('mousemove',function(e){
 var c=sc(); if(!c)return;
 if(!e.target||!e.target.closest||!e.target.closest('#slides-container')){
  if(last){c.classList.remove('sf-he-l','sf-he-r');last=0;} return; }
 var z=isControl(e.target)?0:zone(e,c);
 if(z===last)return;
 last=z;
 c.classList.toggle('sf-he-l',z<0);
 c.classList.toggle('sf-he-r',z>0);
},true);
})();</script>'''


FASTFOLD_MARKER = 'sf-fastfold'
FASTFOLD_SCRIPT = r'''<script>(function(){ /* sf-fastfold */
/* On a fresh home load the user sees exactly three things: the header, the hero,
   and Continue Watching. Everything else is below the fold or scrolled off to the
   right. Measured on a HARD RELOAD (1440x900, warm cache):

       367 requests, 6.8 MB   of which BitrateTest = 5.77 MB (85%)
       header 1028ms | hero 2611ms | continueWatching 2632ms
       ...while TEN other section queries fire together at ~2145ms and run to
       3261ms, competing for four cores with the three things you can see.

   Two changes below: stop paying 5.77MB on every open, and let the visible part
   win the race. */

/* ---- 1. sf-bitrate-cache -------------------------------------------------
   ApiClient.detectBitrate() downloads 0.5 + 1 + 3 MB of throwaway data and keeps
   the answer in MEMORY ONLY (verified: no localStorage key, lastDetectedBitrate
   is an instance field), so every app open re-runs it. The value is only ever
   used to pick a streaming quality, so persist it and let it go stale slowly. */
/* stamp the route on <html> immediately: CSS that needs to know "are we on
   home" cannot wait for #indexPage to exist, and the body-level loading spinner
   is on screen at ~604ms, well before it does. */
function stampHome(){try{
 var h=(location.hash||'').indexOf('#/home')===0;
 if(h)document.documentElement.setAttribute('data-sf-home','1');
 else document.documentElement.removeAttribute('data-sf-home');
}catch(e){}}
stampHome();
try{addEventListener('hashchange',stampHome);}catch(e){}

var BKEY='sf-bitrate', TTL=7*24*3600*1000;
function seed(){
 try{
  var ac=window.ApiClient; if(!ac||typeof ac.detectBitrate!=='function')return false;
  if(!ac.__sfBitrateWrapped){
   ac.__sfBitrateWrapped=1;
   var orig=ac.detectBitrate.bind(ac);
   ac.detectBitrate=function(force){
    /* Seeding lastDetectedBitrate is NOT enough -- traced the probe still firing
       on every reload with a fresh value each time, i.e. the caller passes
       force=true and bypasses jellyfin-apiclient's own cache check. So the
       short-circuit has to live here. Within the TTL we answer from storage and
       never touch the network; past it, one real probe refreshes the value. */
    var c=null; try{c=JSON.parse(localStorage.getItem(BKEY)||'null');}catch(e){}
    if(c&&c.v>0&&(Date.now()-c.t)<TTL)return Promise.resolve(c.v);
    return orig(force).then(function(v){
     try{if(v>0)localStorage.setItem(BKEY,JSON.stringify({v:v,t:Date.now()}));}catch(e){}
     return v;
    });
   };
  }
  var raw=null; try{raw=JSON.parse(localStorage.getItem(BKEY)||'null');}catch(e){}
  if(raw&&raw.v>0&&(Date.now()-raw.t)<TTL){
   /* jellyfin-apiclient short-circuits detectBitrate() when it already holds a
      recent reading, so handing it one skips the download entirely. */
   ac.lastDetectedBitrate=raw.v;
   ac.lastDetectedBitrateTime=Date.now();
   return true;
  }
 }catch(e){}
 return false;
}
if(!seed()){
 var tries=0,iv=setInterval(function(){ if(seed()||++tries>40)clearInterval(iv); },100);
}

/* ---- 1b. sf-cw-prefetch -------------------------------------------------
   Continue Watching is one of the three things visible on load, but it is fetched
   LAST of the visible set because the plugin must first fetch its section LIST:
       1302->1381ms  /HomeScreen/Sections
       1402->1842ms  /HomeScreen/Section/ContinueWatching
   The CW url needs nothing from that list -- it is just the user id, which we
   have by ~1000ms. So ask for it early through ApiClient (which owns the auth
   headers) and hand the answer to the plugin when it finally asks. */
var cwP=null;
function prefetchCW(){
 try{
  if(cwP)return true;
  var ac=window.ApiClient;
  if(!ac||!ac.getCurrentUserId||!ac.getUrl||!ac.ajax)return false;
  var uid=ac.getCurrentUserId(); if(!uid)return false;
  cwP=ac.ajax({type:'GET',dataType:'json',
    url:ac.getUrl('HomeScreen/Section/ContinueWatching',{UserId:uid})})
    .then(function(d){return d;},function(){return null;});
  /* Release the rest once CW's data is in hand -- not when a CW CARD renders,
     because a user with nothing in progress has no cards and the rows must not
     hang waiting for one. The 400ms beat gives CW's posters a clear run at the
     connection before ten more queries start. */
  cwP.then(function(){ setTimeout(function(){openGate('cw');},400); },
           function(){ openGate('cw-failed'); });
  return true;
 }catch(e){return false;}
}
if(!prefetchCW()){
 var ct=0,ci=setInterval(function(){ if(prefetchCW()||++ct>60)clearInterval(ci); },50);
}

/* ---- 2. sf-defer-belowfold ----------------------------------------------
   Hold the queries for rows nobody can see yet. Continue Watching is NOT held --
   it is on screen. The gate opens on whichever comes first: the hero and CW are
   both painted, the user scrolls, or 2.5s. The timeout is the safety net: if the
   hero never paints, the rows must still load. */
/* Rows must appear in DISPLAY order. Releasing every held query at once let them
   race: the row after Continue Watching was Next Up on two loads and Recently
   Added Movies on the next. Rows popping in out of order shift everything below
   them and read as jank. So the queue drains in rank order, ONE AT A TIME -- the
   next query starts only when the previous has settled, which also removes the
   ten-way contention that was making all of them slow. A per-item deadline stops
   one slow row holding the chain hostage. */
var ORDER=[
 /\/HomeScreen\/Section\/NextUp/,
 /Filters=Likes/,
 /cs-trending-movies/,
 /\/HomeScreen\/Section\/RecentlyAddedMovies/,
 /\/HomeScreen\/Section\/RecentlyAddedShows/,
 /\/HomeScreen\/Section\/Discover/,
 /IncludeItemTypes=AudioBook/,
 /IncludeItemTypes=Audio&/,
 /LiveTv\/Channels/
];
function rank(u){ for(var i=0;i<ORDER.length;i++){ if(ORDER[i].test(u))return i; } return ORDER.length; }
var open=false, queue=[], pumping=false;
function openGate(why){
 if(open)return; open=true;
 try{document.documentElement.setAttribute('data-sf-fastfold',why||'');}catch(e){}
 pump();
}
function pump(){
 /* Release the held batch in rank order but with a small STAGGER rather than
    waiting for each response: strict serialisation measured 19s. 120ms apart is
    enough to make them start in order without ten of them landing at once. */
 if(!open||pumping||!queue.length)return;
 pumping=true;
 queue.sort(function(a,b){return a.r-b.r;});
 var batch=queue.splice(0,queue.length);
 batch.forEach(function(item,i){
  setTimeout(function(){ try{item.go();}catch(e){} }, i*120);
 });
 pumping=false;
}
function whenOpen(u,go){ queue.push({r:rank(u),go:go}); if(open)pump(); }
/* The safety timeout used to be 2.5s. Traced under load: the gate opened on
   TIMEOUT at 2866ms and released all ten below-fold queries while Continue
   Watching had not even been fetched yet -- so CW then competed with ten other
   queries and landed at 7220ms, only 1.3s before the next row. That is exactly
   why CW "arrives with the rows". The gate now waits for CW's own data, and the
   timeout is only a genuine last resort. */
setTimeout(function(){openGate('timeout');},9000);
try{
 addEventListener('scroll',function(){openGate('scroll');},{capture:true,once:true});
 addEventListener('wheel',function(){openGate('wheel');},{passive:true,once:true});
 addEventListener('touchstart',function(){openGate('touch');},{passive:true,once:true});
}catch(e){}
/* poll cheaply for "the visible part is done" rather than depend on any one
   event firing -- the hero and CW are built by different owners */
var pt=0,pi=setInterval(function(){
 if(open||++pt>60){clearInterval(pi);return;}
 try{
  var hero=document.querySelector('#slides-container .slide');
  var cw=document.querySelector('.ContinueWatching .card,.ContinueWatching .sf-ml-card');
  if(hero&&hero.getBoundingClientRect().height>0&&cw){clearInterval(pi);openGate('painted');}
 }catch(e){}
},50);

/* Only home, and only the rows that are genuinely off-screen. ContinueWatching
   and the hero's own queries are deliberately absent from this list. */
var HOLD=/\/HomeScreen\/Section\/(?!ContinueWatching)|IncludeItemTypes=Audio(Book)?&|LiveTv\/Channels|Filters=Likes/;
function isHome(){try{return (location.hash||'').indexOf('#/home')===0;}catch(e){return false;}}
var of=window.fetch;
if(typeof of==='function'&&!window.__sfFastFold){
 window.__sfFastFold=1;
 window.fetch=function(input,init){
  var url='';
  try{url=(typeof input==='string')?input:((input&&input.url)||'');}catch(e){}
  var method='GET';
  try{method=String((init&&init.method)||(input&&input.method)||'GET').toUpperCase();}catch(e){}
  var self=this, args=arguments;
  /* hand the plugin the answer we already asked for */
  if(cwP&&method==='GET'&&url.indexOf('/HomeScreen/Section/ContinueWatching')>-1){
   return cwP.then(function(d){
    if(d==null)return of.apply(self,args);
    try{return new Response(JSON.stringify(d),{status:200,
      headers:{'Content-Type':'application/json'}});}
    catch(e){return of.apply(self,args);}
   });
  }
  /* REVERTED: an always-queue version (no `open` bypass) forced strict one-at-a-
     time ordering and measured CW at 19s with most rows never arriving -- each
     row waited for the previous, and under load that is ~3s each. Ordering is
     not worth a 20s page. Requests held before the gate are still released in
     rank order; anything issued after it goes straight through. */
  if(open||method!=='GET'||!url||!isHome()||!HOLD.test(url))return of.apply(this,arguments);
  return new Promise(function(res,rej){
   whenOpen(url,function(){
    var p;
    try{ p=of.apply(self,args); }catch(e){ rej(e); return null; }
    res(p);
    /* advance the pump when the RESPONSE lands, so the next row's query starts
       as this one finishes rather than alongside it */
    return (p&&p.then)?p.then(function(r){return r;},function(){return null;}):null;
   });
  });
 };
}
})();</script>'''

NOCOUNT_MARKER = 'sf-nocount'
# sf-nocount: Shows/NextUp and Items/Resume each run a SEPARATE COUNT query over
# the whole library (9,456 episodes) purely to fill TotalRecordCount -- which no
# home row reads. sf-hero-cap even overwrites it with Items.length. Measured on
# this box: NextUp 0.43-0.70s -> 0.22-0.26s once the count is off; those two calls
# gate the first thing a user sees. Only applied to short list requests
# (Limit<=24), so a paged view that genuinely needs a total keeps it.
NOCOUNT_SCRIPT = r"""<script>(function(){
/* sf-nocount */
var F=window.fetch;
if(!F||window.__sfNoCount)return;
window.__sfNoCount=1;
function trim(u){
 try{
  if(/[?&]EnableTotalRecordCount=/i.test(u))return u;
  /* sf-srchcount (2026-09-01): the search page runs the same redundant COUNT.
     Its results are grouped by Type out of .Items and no total is ever read.
     Measured on this box, 3 runs each: the big search query took 0.52/0.50/0.50s
     with the count and 0.32/0.31/0.28s without -- ~40% off the one request that
     gates the whole results page. StartIndex is the guard: a genuinely paged
     view (the library grids, which DO print "1-100 of N") always carries it,
     and the search page never does. */
  if(/[?&]searchTerm=/i.test(u) && /\/(Items|Artists|Persons)\?/i.test(u)
     && !/[?&]StartIndex=/i.test(u))
    return u+'&EnableTotalRecordCount=false';
  if(!/\/Shows\/NextUp|\/Items\/Resume/i.test(u))return u;
  var m=u.match(/[?&]Limit=(\d+)/i);
  if(!m||parseInt(m[1],10)>24)return u;
  return u+(u.indexOf('?')>-1?'&':'?')+'EnableTotalRecordCount=false';
 }catch(e){return u;}
}
window.fetch=function(input,init){
 var a=input;
 try{
  if(typeof input==='string'){var t=trim(input);if(t!==input)a=t;}
  else if(input&&input.url){var t2=trim(input.url);if(t2!==input.url)a=new Request(t2,input);}
 }catch(e){a=input;}
 return F.call(this,a,init);
};
})();</script>"""

MOBCARD_MARKER = 'sf-mobcard'
# sf-mobcard (2026-08-31). The admin, on a phone: "i dont like the play button bottom
# left of each card. some 3 dots i see dont follow our abyss style and theme."
# Measured at 390x844, touch emulation, hover:none:
#   * TWO menu buttons sit on the same corner of every native card -- Jellyfin's
#     own .cardOverlayButton[data-action=menu] (40x40, icon 24x24) AND our
#     .sf-cardmenu (32x32, icon 26x29). elementsFromPoint at the corner returns
#     both. They are different sizes and slightly offset, which is exactly why
#     the corner control looked inconsistent from card to card.
#   * The grey discs are NOT the buttons -- the buttons are transparent. It is
#     .cardOverlayButtonIcon that carries background rgba(0,0,0,.35) with a 4px
#     blur and a 12px radius; at 24-30px a 12px radius IS a circle, so every
#     control renders as a flat grey blob that matches nothing else in Abyss
#     (the hero chips and the nav pill are wide, tinted, 15px-blur glass).
# So: one control per corner, no play button, and give the survivor the theme's
# own glass tokens instead of the stock disc.
MOBCARD_SCRIPT = r"""<script>(function(){
/* sf-mobcard */
var css=''
/* --- 1. touch: no play affordance on the artwork. The artwork itself already
       plays (sf-home-tap), so the disc was a second, smaller target for the
       same action -- and the one the thumb hits by accident while scrolling. */
+'@media (hover:none){'
+'#indexPage .card .cardOverlayButton[data-action="play"],'
+'#indexPage .card .cardOverlayButton[data-action="resume"],'
+'#indexPage .card .cardOverlayFab-primary,'
+'.sf-ml-card .sf-ml-play,.sf-cardplay{'
+'display:none!important;}'
/* Jellyfin also paints "mark played" and "favourite" discs on touch; they are
   duplicated inside the ⋮ menu, so the corner keeps exactly one control. */
+'#indexPage .card .cardOverlayButton[data-action="none"]{display:none!important;}'
/* --- 2. one ⋮, not two. Where our injected menu exists the native one is a
       duplicate; hide the native rather than ours, because ours is the one
       positioned against the progress bar (.card:has(.itemProgressBar)). */
+'#indexPage .sf-cardmenu-host .cardOverlayButton[data-action="menu"]:not(.sf-cardmenu){'
+'display:none!important;}'
/* --- 3. Abyss glass for the survivor, on both card systems. Values are the
       theme's own tokens, not invented: --abyss-glass-tint 42,42,42,
       --abyss-radius 12px, --abyss-accent 245,245,247, --abyss-glass-blur 15px. */
+'@media (hover:none){'
+'.sf-cardmenu,.sf-ml-more,'
+'#indexPage .card .cardOverlayButton[data-action="menu"]{'
+'width:34px!important;height:34px!important;border-radius:var(--abyss-radius,12px)!important;'
+'background:rgba(var(--abyss-glass-tint,42,42,42),.55)!important;'
+'-webkit-backdrop-filter:blur(var(--abyss-glass-blur,15px))!important;'
+'backdrop-filter:blur(var(--abyss-glass-blur,15px))!important;'
+'border:1px solid rgba(255,255,255,.10)!important;'
+'box-shadow:0 1px 3px rgba(0,0,0,.28)!important;'
+'color:rgb(var(--abyss-accent,245,245,247))!important;'
+'display:flex!important;align-items:center!important;justify-content:center!important;'
+'padding:0!important;opacity:1!important;}'
/* the disc lives on the ICON in this theme, so it has to be cleared there or it
   draws a second, smaller circle inside our new pill */
+'.sf-cardmenu .cardOverlayButtonIcon,.sf-ml-more .cardOverlayButtonIcon,'
+'#indexPage .card .cardOverlayButton[data-action="menu"] .cardOverlayButtonIcon{'
+'background:transparent!important;-webkit-backdrop-filter:none!important;'
+'backdrop-filter:none!important;border-radius:0!important;'
+'box-shadow:none!important;font-size:20px!important;line-height:1!important;'
+'color:inherit!important;width:auto!important;height:auto!important;}'
+'}';
var s=document.createElement('style');s.id='sf-mobcard-css';s.textContent=css;
(document.head||document.documentElement).appendChild(s);
})();</script>"""
