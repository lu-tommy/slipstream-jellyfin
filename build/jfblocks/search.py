"""jfblocks/search.py -- payload constants lifted out of jf_patch.py.

Each constant's source text (and its comments) is byte-identical to the
monolith; only its location changed. 16 constants.
"""

__all__ = [
    'WATCHLISTBTN_MARKER',
    'WATCHLISTBTN_SCRIPT',
    'FAVWL_MARKER',
    'FAVWL_SCRIPT',
    'NOSEARCHSUGG_MARKER',
    'NOSEARCHSUGG_STYLE',
    'SEERRFALLBACK_MARKER',
    'SEERRFALLBACK_SCRIPT',
    'WATCHLIST_MARKER',
    'WATCHLIST_SCRIPT',
    'REQSEARCH_MARKER',
    'REQSEARCH_SCRIPT',
    'SEARCHSKEL_MARKER',
    'SEARCHSKEL_SCRIPT',
    'SEARCHRANK_MARKER',
    'SEARCHRANK_SCRIPT',
    'SEERRCLIP_MARKER',
    'SEERRCLIP_STYLE',
    'SEARCHI18N_MARKER',
    'SEARCHI18N_SCRIPT',
]


# --- Watchlist button (2026-08-02). The admin wanted the eye button beside
# Favorite -- Jellyfin Enhanced's `.je-detail-hide-btn` ("Hide") -- to add to
# the Watchlist instead, keeping the same icon.
# The drawer Watchlist (jf-watchlist-link) is backed by Jellyfin's own **Likes**
# user-data flag: it lists `/Users/<uid>/Items?Filters=Likes`, fed by Swiparr
# swipe-hearts. So "add to watchlist" == set Likes. Verified against the API:
#   POST   /Users/<uid>/Items/<id>/Rating?Likes=true  -> 200, Likes=true
#   DELETE /Users/<uid>/Items/<id>/Rating             -> 200, Likes cleared
# and the item duly appears in / disappears from the Filters=Likes query.
# NOTE JE's own `JE.bookmarks` is NOT this -- its add() takes (timestamp, label),
# i.e. in-video chapter bookmarks, not an item watchlist. Do not wire to that.
# JE owns the button element and re-creates it, so rather than replace the node
# (which would lose JE's re-render) we intercept the click in the CAPTURE phase
# and stopImmediatePropagation, leaving JE's hide handler unfired -- the same
# technique jf-scroller-fix uses on the row arrows.
WATCHLISTBTN_MARKER = 'jf-watchlist-btn'
WATCHLISTBTN_SCRIPT = r'''<script>(function(){ /* jf-watchlist-btn */
function creds(){try{var c=JSON.parse(localStorage.getItem('jellyfin_credentials'));var sv=c.Servers[0];
return {base:sv.ManualAddress||sv.LocalAddress,uid:sv.UserId,tok:sv.AccessToken};}catch(e){return null;}}
function itemId(){var m=(location.hash||'').match(/[?&]id=([a-zA-Z0-9]+)/);return m?m[1]:null;}
function paint(btn,on){
btn.classList.toggle('jf-wl-on',!!on);
btn.setAttribute('title',on?'Remove from Watchlist':'Add to Watchlist');
var ic=btn.querySelector('.material-icons');
if(ic)ic.style.color=on?'#4ac694':'';
}
function refresh(btn){
var c=creds(),id=itemId();if(!c||!id)return;
fetch(c.base+'/Users/'+c.uid+'/Items/'+id,{headers:{'X-Emby-Token':c.tok}})
.then(function(r){return r.json();})
.then(function(d){paint(btn,!!(d&&d.UserData&&d.UserData.Likes));}).catch(function(){});
}
function toggle(btn){
var c=creds(),id=itemId();if(!c||!id)return;
var on=btn.classList.contains('jf-wl-on');
paint(btn,!on);
fetch(c.base+'/Users/'+c.uid+'/Items/'+id+'/Rating'+(on?'':'?Likes=true'),
{method:on?'DELETE':'POST',headers:{'X-Emby-Token':c.tok}})
.then(function(r){if(!r.ok)paint(btn,on);}).catch(function(){paint(btn,on);});
}
document.addEventListener('click',function(e){
var btn=e.target&&e.target.closest?e.target.closest('.je-detail-hide-btn'):null;
if(!btn)return;
e.stopImmediatePropagation();e.preventDefault();
toggle(btn);
},true);
function scan(){
var b=document.querySelectorAll('.je-detail-hide-btn:not([data-jf-wl])');
for(var i=0;i<b.length;i++){b[i].setAttribute('data-jf-wl','1');paint(b[i],b[i].classList.contains('jf-wl-on'));refresh(b[i]);}
}
try{new MutationObserver(scan).observe(document.body,{childList:true,subtree:true});}catch(e){}
window.addEventListener('hashchange',function(){
var b=document.querySelectorAll('.je-detail-hide-btn');
for(var i=0;i<b.length;i++)refresh(b[i]);
});
setInterval(scan,1500);scan();
})();</script>'''

# --- Favorites sub-tabs (2026-08-02). The home Favorites tab (#favoritesTab)
# holds a single `.sections` div with one `.verticalSection` per item type
# (Movies/Shows/Seasons/.../Artists), most of them `.hide` when empty. This adds
# a pill bar above it to switch between Favorites and the Watchlist.
# The Watchlist is Jellyfin's **Likes** flag -- the same source the drawer's
# jf-watchlist-link uses (`/Users/<uid>/Items?Filters=Likes`) and the same flag
# the repurposed detail-page eye button sets (see jf-watchlist-btn). Nothing new
# is stored; this is just a second view over that data.
# Pill styling mirrors jf-seerr-fallback's `.jf-search-tab` so the two tab bars
# in the app look like one design.
FAVWL_MARKER = 'jf-fav-watchlist'
FAVWL_SCRIPT = r'''<script>(function(){ /* jf-fav-watchlist */
/* Mirrors the Abyss theme's own header tab bar so this reads as a deliberate
   second level rather than a bolted-on control. Measured from the live theme:
     capsule  background rgba(42,42,42,.69), border-radius 50px, padding 5px 2.5px
     active   #f5f5f7 on #121212, radius 50px, weight 600
     inactive transparent on #999
   Same shape, ~0.8x the scale, centred under the main tabs. */
var css='.jf-fav-tabs{display:flex;justify-content:center;align-items:center;gap:2px;'
+'margin:1.15em auto .95em;padding:5px 2.5px;width:max-content;max-width:calc(100% - 2em);'
+'background:rgba(42,42,42,.69);border-radius:50px;flex-wrap:wrap;box-sizing:border-box;}'
+'.jf-fav-tab{background:transparent;color:#999;border:none;border-radius:50px;'
+'padding:.42em 1.4em;font-size:.95em;font-weight:600;cursor:pointer;font-family:inherit;'
+'line-height:1.45;white-space:nowrap;transition:background .15s ease,color .15s ease;}'
+'.jf-fav-tab:hover{background:rgba(255,255,255,.07);color:#e8e8e8;}'
+'.jf-fav-tab-active{background:#f5f5f7;color:#121212;}'
+'.jf-fav-tab-active:hover{background:#f5f5f7;color:#121212;}'
+'.jf-fwl-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(150px,1fr));gap:1.1em;padding:.4em 0 2em;}'
+'.jf-fwl-item{cursor:pointer;}'
+'.jf-fwl-poster{width:100%;aspect-ratio:2/3;background-size:cover;background-position:center;background-color:#222;border-radius:10px;}'
/* jf-fwl-font: match the Favorites card title exactly. Measured live on the
   Favorites pill 2026-08-27: .cardText-first is 17.856px (= 1.2rem) / 600 /
   line-height 1.35 / rgba(255,255,255,.8), Google Sans. This grid was
   .86em / 400 / #e8e8e8 -- same family, but visibly smaller and lighter, so
   flipping between the pills read as two different designs. The Bookmarks
   pill shares this class and comes along for free. */
+'.jf-fwl-title{margin-top:.45em;font-size:1.2rem;font-weight:600;line-height:1.35;'
+'color:rgba(255,255,255,.8);overflow:hidden;text-overflow:ellipsis;white-space:nowrap;}'
+'.jf-fwl-msg{padding:2em 0;color:#9a9a9a;}'
/* jf-rq-tab: the Requests pill. Rows, not posters -- the useful thing here is the
   STATUS, and a poster grid buries it. Badge colours are semantic: green=ready,
   blue=on its way, grey=still looking, amber=needs the admin, red=went wrong. */
+'.jf-rq-list{padding:.4em 0 2em;}'
+'.jf-rq-row{display:flex;align-items:center;gap:.9em;padding:.7em .9em;margin-bottom:.55em;'
+'background:rgba(255,255,255,.045);border-radius:12px;}'
+'.jf-rq-poster{flex:none;width:46px;aspect-ratio:2/3;border-radius:6px;background:#222;'
+'background-size:cover;background-position:center;}'
+'.jf-rq-meta{font-size:.82rem;color:#8d8d8d;margin-top:.15em;'
+'overflow:hidden;text-overflow:ellipsis;white-space:nowrap;}'
+'.jf-rq-main{flex:1;min-width:0;}'
+'.jf-rq-title{font-size:1.05rem;font-weight:600;color:rgba(255,255,255,.9);'
+'overflow:hidden;text-overflow:ellipsis;white-space:nowrap;}'
+'.jf-rq-hint{font-size:.85rem;color:#9a9a9a;margin-top:.2em;white-space:normal;}'
+'.jf-rq-badge{flex:none;padding:.32em .95em;border-radius:50px;font-size:.8rem;'
+'font-weight:600;white-space:nowrap;}'
+'.jf-rq-b-available{background:#1e7a45;color:#eafdf1;}'
+'.jf-rq-b-partial{background:#1e6a7a;color:#eaf9fd;}'
+'.jf-rq-b-downloading{background:#1f5c9e;color:#eaf2fd;}'
+'.jf-rq-b-searching{background:#4a4a4a;color:#e8e8e8;}'
+'.jf-rq-b-pending{background:#8a6a1f;color:#fdf6ea;}'
+'.jf-rq-b-failed{background:#8a2f2f;color:#fdeaea;}'
+'.jf-rq-b-declined{background:#5a3a3a;color:#f2dede;}';
var st=document.createElement('style');st.id='jf-fav-watchlist-style';st.textContent=css;document.head.appendChild(st);

function creds(){try{var c=JSON.parse(localStorage.getItem('jellyfin_credentials'));var sv=c.Servers[0];
return {base:sv.ManualAddress||sv.LocalAddress,uid:sv.UserId,tok:sv.AccessToken};}catch(e){return null;}}

function render(grid,items,c){
grid.innerHTML='';
if(!items.length){var m=document.createElement('div');m.className='jf-fwl-msg';
m.textContent='Nothing on your watchlist yet. Use the eye button on a movie or show to add it.';
grid.appendChild(m);return;}
items.forEach(function(it){
var w=document.createElement('div');w.className='jf-fwl-item';
var p=document.createElement('div');p.className='jf-fwl-poster';
var tag=it.ImageTags&&it.ImageTags.Primary;
if(tag)p.style.backgroundImage='url("'+c.base+'/Items/'+it.Id+'/Images/Primary?maxWidth=300&tag='+tag+'&api_key='+c.tok+'")';
var t=document.createElement('div');t.className='jf-fwl-title';t.textContent=it.Name||'';
w.appendChild(p);w.appendChild(t);
w.addEventListener('click',function(){location.hash='#/details?id='+it.Id;});
grid.appendChild(w);});
}

function load(grid){
var c=creds();if(!c){grid.innerHTML='<div class="jf-fwl-msg">Not signed in.</div>';return;}
grid.innerHTML='<div class="jf-fwl-msg">Loading\u2026</div>';
fetch(c.base+'/Users/'+c.uid+'/Items?Recursive=true&Filters=Likes&IncludeItemTypes=Movie,Series&SortBy=SortName&Fields=PrimaryImageAspectRatio',
{headers:{'X-Emby-Token':c.tok}}).then(function(r){return r.json();})
.then(function(d){render(grid,(d&&d.Items)||[],c);})
.catch(function(){grid.innerHTML='<div class="jf-fwl-msg">Could not load watchlist.</div>';});
}

function fmtTs(t){
t=Number(t)||0;
/* JE may store seconds or .NET ticks (1e7 per second) - normalise */
if(t>100000000)t=t/10000000;
t=Math.max(0,Math.floor(t));
var h=Math.floor(t/3600),m=Math.floor((t%3600)/60),sec=t%60;
var mm=(h?('0'+m).slice(-2):String(m));
return (h?h+':':'')+mm+':'+('0'+sec).slice(-2);
}

function loadBookmarks(grid){
var c=creds();if(!c){grid.innerHTML='<div class="jf-fwl-msg">Not signed in.</div>';return;}
grid.innerHTML='<div class="jf-fwl-msg">Loading\u2026</div>';
fetch(c.base+'/JellyfinEnhanced/user-settings/'+c.uid+'/bookmark.json',{headers:{'X-Emby-Token':c.tok}})
.then(function(r){return r.ok?r.json():null;})
.then(function(d){
var list=(d&&(d.bookmarks||d.Bookmarks))||(Array.isArray(d)?d:[]);
if(!list.length){grid.innerHTML='<div class="jf-fwl-msg">No bookmarks yet. Press B, or the bookmark button in the player, while watching.</div>';return;}
grid.innerHTML='';
list.forEach(function(bm){
var id=bm.itemId||bm.ItemId;
var w=document.createElement('div');w.className='jf-fwl-item';
var p=document.createElement('div');p.className='jf-fwl-poster';
if(id)p.style.backgroundImage='url("'+c.base+'/Items/'+id+'/Images/Primary?maxWidth=300&api_key='+c.tok+'")';
var t=document.createElement('div');t.className='jf-fwl-title';
t.textContent=(bm.label||bm.Label||'Bookmark')+' \u00b7 '+fmtTs(bm.timestamp||bm.Timestamp);
w.appendChild(p);w.appendChild(t);
if(id)w.addEventListener('click',function(){location.hash='#/details?id='+id;});
grid.appendChild(w);});
})
.catch(function(){grid.innerHTML='<div class="jf-fwl-msg">Could not load bookmarks.</div>';});
}

/* jf-rq-tab: a user's own Jellyseerr requests. The Jellyseerr API key is NOT in
   the browser -- requestbridge identifies the caller from their Jellyfin token
   and returns only that person's requests. Same-origin bridge path as the other
   callers (sf-bridge-path), so this works off-site too. */
function loadRequests(grid){
var c=creds();if(!c){grid.innerHTML='<div class="jf-fwl-msg">Not signed in.</div>';return;}
grid.innerHTML='<div class="jf-fwl-msg">Loading\u2026</div>';
var base=(location.port==='8096')?(location.protocol+'//'+location.hostname+':8099')
:(location.origin+'/requestbridge');
fetch(base+'/api/myrequests',{headers:{'X-Jellyfin-Token':c.tok}})
.then(function(r){return r.json();})
.then(function(d){
var list=(d&&d.requests)||[];
grid.innerHTML='';
if(!list.length){grid.innerHTML='<div class="jf-fwl-msg">You have not requested anything yet. '
+'Use Search to ask for a movie or show.</div>';return;}
var wrap=document.createElement('div');wrap.className='jf-rq-list';
list.forEach(function(q){
var row=document.createElement('div');row.className='jf-rq-row';
var ph=document.createElement('div');ph.className='jf-rq-poster';
if(q.image)ph.style.backgroundImage='url("'+q.image+'")';
row.appendChild(ph);
var main=document.createElement('div');main.className='jf-rq-main';
var t=document.createElement('div');t.className='jf-rq-title';
var seas=(q.seasons&&q.seasons.length)
?(q.seasons.length>1?('Seasons '+q.seasons.join(', ')):('Season '+q.seasons[0])):'';
t.textContent=q.title||'';
main.appendChild(t);
var bits=[];
if(q.year)bits.push(q.year);
bits.push(q.type==='tv'?'Series':'Movie');
if(seas)bits.push(seas);
var meta=document.createElement('div');meta.className='jf-rq-meta';
meta.textContent=bits.join('  \u2022  ');
main.appendChild(meta);
if(q.hint){var h=document.createElement('div');h.className='jf-rq-hint';h.textContent=q.hint;main.appendChild(h);}
var b=document.createElement('div');
b.className='jf-rq-badge jf-rq-b-'+(q.state||'searching');
b.textContent=q.label||'';
row.appendChild(main);row.appendChild(b);wrap.appendChild(row);});
grid.appendChild(wrap);
})
.catch(function(){grid.innerHTML='<div class="jf-fwl-msg">Could not load your requests.</div>';});
}

function build(){
/* jf-view-scope: resolve #favoritesTab INSIDE the home instance that is
   actually on screen. Several #indexPage copies -- each with its own
   #favoritesTab -- legitimately coexist because Jellyfin caches a view per
   URL, and a bare querySelector('#favoritesTab') returns whichever is first
   in the DOM. Measured: after one Sports click the VISIBLE #favoritesTab was
   instance 1 while instance 0 (hidden) held our pills, so My Stuff opened an
   empty, undecorated pane.
   Scoping also repairs the early-return below. It used to find the STALE
   instance's .jf-fav-tabs, conclude there was nothing to do, and return -- so
   the newly created instance was never decorated at all. Per-instance now, it
   re-arms automatically: the existing observer/interval that already call
   build() pick the new instance up without a new observer. */
var ft=(window.__jfView&&window.__jfView.favTab())||null;
if(!ft||ft.querySelector('.jf-fav-tabs'))return;
var sections=ft.querySelector('.sections');
if(!sections)return;
var bar=document.createElement('div');bar.className='jf-fav-tabs';
var grid=document.createElement('div');grid.className='jf-fwl-grid padded-left padded-right';
grid.style.display='none';
function mk(label){var b=document.createElement('button');b.type='button';
b.className='jf-fav-tab';b.textContent=label;return b;}
var bFav=mk('Favorites'),bWl=mk('Watchlist'),bBm=mk('Bookmarks'),bRq=mk('Requests');
/* jf-default-subtab: no pill is pre-marked here. show() below sets the
   active class, content visibility and the URL together, so the default
   lives in exactly one place instead of being half-applied at build time. */
/* jf-subpill-url: mirror the chosen sub-pill into the address bar so a reload
   comes back to the same view. replaceState, not a hash assignment - assigning
   would re-enter Jellyfin's router and re-render the whole page. */
function syncUrl(which){
try{
var base='#/home?tab=1';
history.replaceState(null,'',which==='fav'?base:base+'&sub='+which);
}catch(e){}
}
/* jf-default-subtab: `quiet` applies the view without touching the URL.
   build() runs whenever #favoritesTab exists in the DOM -- which is true on the
   home page even when My Stuff is NOT the active tab -- so an unconditional
   syncUrl() there rewrote #/home into #/home?tab=1&sub=wl and effectively
   hijacked Home. Only real user clicks may change the address bar. */
function show(which,quiet){
var isFav=which==='fav';
bFav.classList.toggle('jf-fav-tab-active',isFav);
bWl.classList.toggle('jf-fav-tab-active',which==='wl');
bBm.classList.toggle('jf-fav-tab-active',which==='bm');
bRq.classList.toggle('jf-fav-tab-active',which==='rq');
sections.style.display=isFav?'':'none';
/* jf-rq-tab: the shared pane is a poster GRID; requests are rows. */
grid.style.display=isFav?'none':(which==='rq'?'block':'');
if(which==='wl')load(grid);
if(which==='bm')loadBookmarks(grid);
if(which==='rq')loadRequests(grid);
if(!quiet)syncUrl(which);
}
bFav.addEventListener('click',function(){show('fav');});
bWl.addEventListener('click',function(){show('wl');});
bBm.addEventListener('click',function(){show('bm');});
bRq.addEventListener('click',function(){show('rq');});
bar.appendChild(bFav);bar.appendChild(bWl);bar.appendChild(bBm);bar.appendChild(bRq);
ft.insertBefore(bar,sections);
sections.parentNode.insertBefore(grid,sections.nextSibling);
/* jf-default-subtab: FAVORITES is the default view for My Stuff (changed from
   Watchlist 2026-08-09 at the admin's request). An explicit ?sub= in the URL still
   wins, so a reload or a shared link returns to whatever was actually being
   viewed -- only the no-preference case changes.
   Note syncUrl() maps 'fav' to a bare #/home?tab=1 with no &sub=, so the default
   and "explicitly chose Favorites" are the same URL, which is what we want. */
var initial=(/[?&]sub=([a-z]+)/.exec(location.hash||'')||[])[1];
if(initial!=='fav'&&initial!=='wl'&&initial!=='bm'&&initial!=='rq')initial='fav';
show(initial,true);   /* quiet: never rewrite the URL from a passive build */
}
/* The vertical gap under the main tab bar is NOT constant: Jellyfin re-flows
   the header responsively, so .headerTabs.sectionTabs sits at a different
   bottom edge per viewport while #indexPage's padding-top barely moves.
   Measured: 1000px wide -> main bar bottom 125, gap 4px
             1600px wide -> main bar bottom  78, gap 39px
   A fixed margin therefore cannot hold the spacing. Instead measure the real
   distance each time and set margin-top so the gap is always GAP px. */
var GAP=12;
function align(){
/* jf-view-scope: this must be the pill bar in the home instance that is ON
   SCREEN. A bare querySelector('.jf-fav-tabs') returns the first in the DOM,
   and once a second #indexPage is cached that is usually the HIDDEN copy --
   whereupon the offsetParent check below returned early and the VISIBLE bar
   was never aligned at all. That is why the My Stuff pills sat lower than the
   pills on every other page: they kept a stale margin instead of the measured
   one. Scoping inside #favoritesTab also excludes the .jf-ltv-sub bar for
   free. */
var ft=window.__jfView&&window.__jfView.favTab();
var bar=ft?ft.querySelector('.jf-fav-tabs'):null;
var main=document.querySelector('.headerTabs.sectionTabs');
if(!bar||!main)return;
if(bar.offsetParent===null)return;                 /* not visible - nothing to measure */
/* ONLY MEASURE AT REST. This lines the bar up against the main bar in VIEWPORT
   coordinates -- but the main bar lives in a position:fixed header while this one
   scrolls with the page. Once scrolled, the header's bottom stays put while this
   bar's top climbs, so every pass added the difference back as margin and the
   next pass saw a bigger difference: a runaway that only stopped at the 240 clamp
   below, then unwound on the way back up.
   Measured on the Watchlist tab: document height oscillating 1050 to 1312 while
   scrolling, three layout shifts, CLS 0.3416 (Google rates anything above 0.25
   as poor). That is what "scrolling feels bad" was.
   At rest the geometry is exactly what this was written to solve, and while
   scrolling the bar is pinned by position:sticky (sf-subnav-glass) instead, which
   costs no layout at all. */
if((window.pageYOffset||document.documentElement.scrollTop||0)>4)return;
var mb=main.getBoundingClientRect().bottom;
if(!mb)return;
var cur=parseFloat(getComputedStyle(bar).marginTop)||0;
var next=cur+((mb+GAP)-bar.getBoundingClientRect().top);
if(!isFinite(next))return;
/* must allow NEGATIVE margins: at wide viewports #indexPage's padding-top
   already leaves ~22px under the main bar, so margin-top:0 is still too far
   and the bar has to be pulled up to reach GAP. Clamped both ways so a bad
   measurement can never strand it off-screen. */
if(next<-160)next=-160; if(next>240)next=240;
if(Math.abs(next-cur)>0.5)bar.style.marginTop=next+'px';
}
/* sf-align-coalesce: this observer watches the WHOLE body subtree and ran
   build()+align() once per mutation batch. align() performs four forced layout
   reads (offsetParent, getComputedStyle, and two getBoundingClientRect), so on a
   home load -- which appends 188 cards and 165 images -- it re-flowed the page
   over and over.
   Profiled at 4x CPU throttle over the LOAD window: align() was 1573ms, the
   largest single JS cost on the page and roughly a quarter of all main-thread
   blocking. (An earlier 30s profile blamed onScreen/querySelectorAll; that was
   the steady-state TICK cost, not the load, which is why fixing it alone moved
   nothing.)
   Coalesced to at most one run per animation frame. The DOM is only read once
   the frame's mutations have all landed, which is also when the measurement is
   correct -- measuring mid-batch was never useful. */
var _alRaf=0;
function alignSoon(){
if(_alRaf)return;
_alRaf=1;
var run=function(){_alRaf=0;try{build();align();}catch(e){}};
if(window.requestAnimationFrame)requestAnimationFrame(run);else setTimeout(run,16);
}
try{new MutationObserver(alignSoon).observe(document.body,{childList:true,subtree:true});}catch(e){}
window.addEventListener('resize',align);
setInterval(function(){build();align();},1000);build();align();
})();</script>'''

# --- Hide the empty-query "Suggestions" list on the search page (2026-08-04).
# Opening search with no query renders Jellyfin's own
# div.verticalSection.searchSuggestions > div.searchSuggestionsList inside
# #searchPage -- a random list of library titles. There is no server-side or
# user setting to turn it off, so hide it with CSS.
# NOTE: this hides it, it does not prevent the /Items fetch that populates it
# (one request). Blocking that fetch would mean pattern-matching a generic
# /Items query, which risks breaking real search results -- not worth it.
NOSEARCHSUGG_MARKER = 'jf-no-search-suggestions'
NOSEARCHSUGG_STYLE = ('<style id="jf-no-search-suggestions">'
                      '#searchPage .searchSuggestions{display:none!important;}'
                      # The spinner is a body-level .docspinner (NOT inside #searchPage),
                      # so it has to be reached with body:has(...) -- same shape as
                      # jf-no-home-spinner. Gate on :placeholder-shown so it only hides
                      # while the query box is EMPTY: once the user types, the placeholder
                      # is gone, the selector stops matching, and real searches keep their
                      # loading feedback. Verified both states before shipping.
                      'body:has(#searchPage:not(.hide) input:placeholder-shown)'
                      ' > .docspinner{display:none!important;}'
                      '</style>')

# --- Seerr search tabs: "Discover on Seerr" fires its own Jellyseerr query on
# every search and always rendered mixed in with local library results, even
# when you already own the title — confusing, and doubles as extra exposure
# to the scroller crash fixed above. An earlier version of this patch tried
# to auto-hide Seerr only when local results existed, but that was a fuzzy
# heuristic; this replaces it with two explicit tabs ("My Library" / "Discover
# on Seerr") so which one you're looking at is never ambiguous. My Library is
# the default on every fresh search. Deliberately independent of Jellyfin
# Enhanced's own isJellyseerrOnlyMode toggle (the small icon in the search
# box) rather than driving it — that toggle's default state is "show both
# mixed together", not "local only", so it doesn't match what's wanted here;
# simpler and more predictable to control the two section groups' visibility
# directly than to interoperate with JE's internal state machine.
SEERRFALLBACK_MARKER = 'jf-seerr-fallback'
SEERRFALLBACK_SCRIPT = r'''<script>(function(){
/* jf-seerr-fallback */
var css='.jf-search-tabs{display:flex;gap:.5em;padding:.75em 0 .25em;flex-wrap:wrap;box-sizing:border-box;}'
+'.jf-search-tab{background:rgba(255,255,255,.09);color:#cfcfcf;border:none;border-radius:20px;padding:.4em 1.1em;font-size:.85em;font-weight:600;cursor:pointer;font-family:inherit;line-height:1.3;}'
+'.jf-search-tab:hover{background:rgba(255,255,255,.18);}'
+'.jf-search-tab-active{background:#fff;color:#111;}'
+'.searchFields .jellyseerr-icon{display:none!important;}';
var st=document.createElement('style');st.textContent=css;document.head.appendChild(st);

function getMode(){try{return localStorage.getItem('jfSearchTab')||'library';}catch(e){return 'library';}}
function setMode(v){try{localStorage.setItem('jfSearchTab',v);}catch(e){}}

function updateActive(bar){
var mode=getMode();
if(bar.children.length<2)return;
bar.children[0].classList.toggle('jf-search-tab-active',mode==='library');
bar.children[1].classList.toggle('jf-search-tab-active',mode==='seerr');
}

function ensureTabs(searchPage){
var host=searchPage.querySelector('.searchFields')||searchPage.querySelector('.searchFieldsInner');
if(!host||!host.parentElement)return null;
var bar=searchPage.querySelector('.jf-search-tabs');
if(bar){updateActive(bar);return bar;}
bar=document.createElement('div');
bar.className='jf-search-tabs padded-left padded-right';
var libBtn=document.createElement('button');
libBtn.type='button';libBtn.className='jf-search-tab';libBtn.textContent='My Library';
libBtn.addEventListener('click',function(){setMode('library');apply();});
var seerrBtn=document.createElement('button');
seerrBtn.type='button';seerrBtn.className='jf-search-tab';seerrBtn.textContent='Add to your library';
seerrBtn.addEventListener('click',function(){setMode('seerr');apply();});
bar.appendChild(libBtn);bar.appendChild(seerrBtn);
host.parentElement.insertBefore(bar,host.nextSibling);
updateActive(bar);
return bar;
}

function apply(){
var searchPage=document.querySelector('#searchPage:not(.hide)');
if(!searchPage)return;
/* sf-search-merge: the tabs only toggled display on sections that were both
   already rendered, so they never saved a request -- and the slow part is
   Jellyfin's own 864ms library query, not the 110-227ms bridge call. One list
   instead: everything visible, no tab bar. */
var bar=searchPage.querySelector('.jf-search-tabs');
if(bar&&bar.parentNode)bar.parentNode.removeChild(bar);
/* sf-no-blanket-unhide: this used to be
     searchPage.querySelectorAll('.verticalSection').forEach(s=>{
       if(s.style.display==='none') s.style.display='';   });
   -- it force-revealed EVERY section anyone had hidden inline. That was
   written for the old My Library / Add-to-library tab bar, which hid sections
   to switch tabs; sf-search-merge deleted those tabs, so nothing of ours hides
   a section any more and the loop had no job left. What it still did was
   overrule Jellyfin and Jellyseerr: Jellyseerr's search integration leaves
   sections in the DOM with display:none when it has nothing to show for them
   (the same habit documented in sf-empty-hidden-cards, where it left 19 hidden
   cards on a music-only query), and this loop resurrected them -- an empty
   duplicate row appearing under the real one. Only unhide OUR own thing, and
   only when we can see it is ours. */
var seerr=searchPage.querySelector('.jellyseerr-section');
if(seerr){
/* sf-search-order: the heading still carried the Seerr brand. Rewrite only
   the text node -- the h2 also holds the refresh button. */
var st=seerr.querySelector('.sectionTitle');
if(st){
for(var ni=0;ni<st.childNodes.length;ni++){
var nd=st.childNodes[ni];
if(nd.nodeType===3&&nd.nodeValue&&nd.nodeValue.indexOf('Seerr')>=0)nd.nodeValue='Add to your library';
}
}
/* sf-rank-nomove: this used to appendChild(seerr) to push it last whenever it
   was not already the last child. sf-search-rank now places it with flex
   order, so the move is redundant -- and it was actively harmful: the move is
   a childList mutation on a subtree this same MutationObserver watches, and
   Jellyseerr's own renderer re-appends its cards, so the two could trade
   mutations and peg the page. Ranking never touches the DOM tree. */
}
}
var obs=new MutationObserver(apply);
obs.observe(document.body,{childList:true,subtree:true});
setInterval(apply,1000);
})();</script>'''

WATCHLIST_MARKER = 'jf-watchlist-link'
WATCHLIST_SCRIPT = r'''<script>(function(){
/* jf-watchlist-link */
/* "Watchlist" hamburger-drawer entry. This Jellyfin build has no "Liked"
   library filter and playlists only render as track LISTS, so we render the
   user's Liked items (fed by Swiparr swipe-hearts via the swiparr-watchlist
   sync -> UserData.Likes) as our own LIBRARY-STYLE POSTER GRID.
   Per-user, client-side, modeled on the sf-livesports overlay pattern.
   Sits BELOW Jellyfin's real .skinHeader (z-index 998 < the header's 999) so
   the STANDARD header (home/back/hamburger/search) stays visible + usable, for
   consistency with the home/bookmarks pages (the admin 2026-07-27: "keep the top
   the same ... for consistency"). Any header click, or any navigation, hides it. */
var CSS='.jf-wl-root{position:fixed;inset:0;background:#0d0d11;z-index:998;overflow-y:auto;padding:1.5rem 2rem 3rem;display:none;}'
+'.jf-wl-root.jf-wl-show{display:block;}'
  /* matched to the Favorites section heading, measured live: 22.32px / 600 /
     rgba(255,255,255,.8) / Google Sans / line-height 30.132px, margins 4.464px.
     Size, weight, family and line-height already agreed; the page heading was pure
     #fff and carried a much bigger bottom margin, which is what read as 'different'.
     These four lines used to start with '#' -- Python comment syntax, but this is a
     raw string holding JAVASCRIPT, so they shipped verbatim into index.html and threw
     'Invalid or unexpected token'. That killed the whole jf-watchlist-link IIFE, so
     the drawer entry and its grid did not exist at all. Verified dead 2026-08-27. */
  +'.jf-wl-title{font-size:1.5rem;font-weight:600;color:rgba(255,255,255,.8);'
  +'margin:4.464px 0;}'
+'.jf-wl-grid{display:grid;grid-template-columns:repeat(auto-fill,192px);gap:0;justify-content:start;}'
+'@media (max-width:640px){.jf-wl-grid{grid-template-columns:repeat(auto-fill,minmax(105px,1fr));gap:.7rem;}'
  +'.jf-wl-poster{width:100%;max-width:100%;margin:0;}'
  +'.jf-wl-name,.jf-wl-year{margin-left:0;margin-right:0;}}'
+'.jf-wl-card{cursor:pointer;}'
+'.jf-wl-poster{width:165px;max-width:calc(100% - 18px);aspect-ratio:2/3;border-radius:12px;'
  +'margin:0 9px;background:#222 center/cover no-repeat;box-shadow:0 3px 10px rgba(0,0,0,.5);}'
+'.jf-wl-card:hover .jf-wl-poster{transform:none;}'
+'.jf-wl-name{color:rgba(255,255,255,.8);font-size:1.2rem;font-weight:600;margin:.45rem 9px 0;'
  +'text-align:left;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;}'
  +'.jf-wl-year{color:rgba(255,255,255,.5);font-size:16px;font-weight:200;margin:0 9px;'
  +'text-align:left;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;}'
+'.jf-wl-empty{color:#8a8a90;text-align:center;padding:3.5rem 1rem;font-size:1rem;}';
if(!document.getElementById('jf-wl-css')){var s=document.createElement('style');s.id='jf-wl-css';s.textContent=CSS;document.head.appendChild(s);}
function creds(){var c=JSON.parse(localStorage.getItem('jellyfin_credentials'));var sv=c.Servers[0];return {base:sv.ManualAddress||sv.LocalAddress,uid:sv.UserId,tok:sv.AccessToken};}
function closeDrawer(){var d=document.querySelector('.mainDrawer');if(d&&d.classList.contains('drawer-open')){var b=document.querySelector('.mainDrawerButton');if(b)b.click();}}
function shown(){var r=document.querySelector('.jf-wl-root');return r&&r.classList.contains('jf-wl-show');}
function hide(){var r=document.querySelector('.jf-wl-root');if(r)r.classList.remove('jf-wl-show');}
function ensureRoot(){
var r=document.querySelector('.jf-wl-root');
if(r)return r;
r=document.createElement('div');r.className='jf-wl-root';
r.innerHTML='<h2 class="jf-wl-title">Watchlist</h2><div class="jf-wl-grid"></div>';
document.body.appendChild(r);
return r;
}
async function openWatchlist(){
var c=creds();
var r=ensureRoot();
var hdr=document.querySelector('.skinHeader');
r.style.paddingTop=((hdr?hdr.offsetHeight:64)+12)+'px';
var grid=r.querySelector('.jf-wl-grid');
grid.innerHTML='<div class="jf-wl-empty">Loading…</div>';
r.classList.add('jf-wl-show');
var data;
try{data=await fetch(c.base+'/Users/'+c.uid+'/Items?Recursive=true&Filters=Likes&IncludeItemTypes=Movie,Series&SortBy=SortName',{headers:{'X-Emby-Token':c.tok}}).then(function(x){return x.json();});}
catch(e){grid.innerHTML='<div class="jf-wl-empty">Could not load your watchlist.</div>';return;}
var items=data.Items||[];
if(!items.length){grid.innerHTML='<div class="jf-wl-empty">Your watchlist is empty. Open “What to Watch” and swipe some movies.</div>';return;}
grid.innerHTML='';
items.forEach(function(it){
var card=document.createElement('div');card.className='jf-wl-card';
var p=document.createElement('div');p.className='jf-wl-poster';
var tag=it.ImageTags&&it.ImageTags.Primary;
if(tag)p.style.backgroundImage='url("'+c.base+'/Items/'+it.Id+'/Images/Primary?maxWidth=300&tag='+tag+'&api_key='+c.tok+'")';
var n=document.createElement('div');n.className='jf-wl-name';n.textContent=it.Name;
var yr=document.createElement('div');yr.className='jf-wl-year';
yr.textContent=it.ProductionYear?String(it.ProductionYear):'';
card.appendChild(p);card.appendChild(n);if(yr.textContent)card.appendChild(yr);
card.addEventListener('click',function(){hide();location.hash='#/details?id='+it.Id;});
grid.appendChild(card);
});
}
/* Any real-header interaction (home/back/hamburger/search/pill) or any route
   change dismisses the grid -- so the standard header nav works as the way out,
   no custom close button needed. Capture phase so we hide before the header's
   own handler runs; we never preventDefault, so the header still does its job. */
document.addEventListener('click',function(e){if(shown()&&e.target.closest&&e.target.closest('.skinHeader'))hide();},true);
window.addEventListener('hashchange',hide);
function add(){
var cont=document.querySelector('.customMenuOptions')||document.querySelector('.mainDrawer-scrollContainer');
if(!cont||cont.querySelector('.jf-watchlist-link'))return;
var a=document.createElement('a');
a.className='navMenuOption emby-button jf-watchlist-link';
a.href='#';
a.innerHTML='<span class="material-icons navMenuOptionIcon" aria-hidden="true">bookmark</span><span class="navMenuOptionText">Watchlist</span>';
a.addEventListener('click',function(e){e.preventDefault();e.stopPropagation();closeDrawer();openWatchlist();});
cont.appendChild(a);
}
new MutationObserver(add).observe(document.body,{childList:true,subtree:true});
setInterval(add,1500);add();
})();</script>'''

REQSEARCH_MARKER = 'sf-request-search'
REQSEARCH_SCRIPT = r'''<script>(function(){
/* sf-request-search */
/* Adds "not in your library" MUSIC / AUDIOBOOKS sections under Jellyfin's own
   search results, each card carrying a single Request button.

   Design rules this follows deliberately:
   - Jellyfin's OWN card classes are reused (.card .cardBox .cardScalable
     .cardPadder .cardImageContainer .cardText) so artwork proportions, radius,
     typography, spacing and hover come from the active theme. No parallel
     design system, and it keeps matching if the theme changes.
   - Jellyfin's native results are never touched, only appended after.
   - The button NEVER shows "Requested" until the bridge confirms the backend
     accepted it. An optimistic flip would tell the user something is coming
     when it may not be.
   - No hover-dependent behaviour: everything is tap-driven for touch. */

/* sf-bridge-origin: this was always location.hostname + ':8099', which only
   ever worked on the LAN. Off-site the page is served from
   https://your-jellyfin-host.example, so the same expression asked for
   that host on port 8099 -- a port that is not open. The fetch did not merely
   fail auth, it failed to CONNECT (measured: curl exit with status 000), and
   because render()'s .catch() is deliberately silent so a bridge outage cannot
   disturb Jellyfin's own results, the Music row just never appeared and
   nothing was logged. Library music still worked throughout, because that row
   comes from Jellyfin's API rather than the bridge -- which is exactly why it
   looked like "music search is broken" rather than "the bridge is unreachable".
   Reaching it on the same origin needs no open port: nginx proxies
   /requestbridge/ to :8099 (see sf-bridge-path in the proxy host config).
   Port 8096 means the browser is talking to Jellyfin directly on the LAN,
   where that path does not exist and the port does work. */
var BRIDGE = (location.port === '8096')
  ? location.protocol + '//' + location.hostname + ':8099'
  : location.origin + '/requestbridge';

var css =
  '.sfrq-sec{margin:2em 0 0;}'
+ '.sfrq-head{display:flex;align-items:baseline;gap:.6em;margin:0 0 .15em;padding-left:3.3%;}'
+ '.sfrq-head h2{margin:0;}'
+ '.sfrq-sub{color:rgba(255,255,255,.5);font-weight:300;font-size:.82em;padding-left:3.3%;margin:0 0 .8em;}'
/* 2 columns on phones is the floor; wider screens fill naturally to 4-6+.
   Explicit column counts are avoided so Jellyfin's own responsive rhythm
   still drives the layout. */
+ '.sfrq-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:1.1em .8em;padding:0 3.3%;box-sizing:border-box;}'
+ '@media (min-width:500px){.sfrq-grid{grid-template-columns:repeat(auto-fill,minmax(200px,1fr));}}'
+ '.sfrq-card{position:relative;min-width:0;}'
+ '.sfrq-box{display:flex;flex-direction:column;min-width:0;}'
+ '.sfrq-art{position:relative;width:100%;aspect-ratio:1/1;border-radius:12px;overflow:hidden;'
+ 'background-color:#1c1c1c;background-size:cover;background-position:center;}'
+ '.sfrq-art-fallback{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;font-size:2.4em;opacity:.3;background:linear-gradient(145deg,#232323,#161616);}'
+ '.sfrq-t{margin-top:.5em;color:rgba(255,255,255,.85);font-weight:600;font-size:.92em;'
+ 'white-space:nowrap;overflow:hidden;text-overflow:ellipsis;}'
+ '.sfrq-s{color:rgba(255,255,255,.45);font-weight:300;font-size:.8em;'
+ 'white-space:nowrap;overflow:hidden;text-overflow:ellipsis;}'
/* 46px tall: comfortably inside the 44-48px touch target range. */
+ '.sfrq-btn{margin-top:.5em;width:100%;min-height:46px;border:0;border-radius:8px;cursor:pointer;'
+ 'font-family:inherit;font-size:.88em;font-weight:600;letter-spacing:.01em;'
+ 'display:flex;align-items:center;justify-content:center;gap:.4em;'
+ 'background:rgba(255,255,255,.13);color:#fff;transition:background .15s ease;}'
+ '.sfrq-btn:active{transform:scale(.98);}'
+ '.sfrq-btn[data-s="none"]{background:#fff;color:#101010;}'
+ '.sfrq-btn[data-s="busy"]{background:rgba(255,255,255,.13);color:rgba(255,255,255,.75);cursor:default;}'
+ '.sfrq-btn[data-s="requested"]{background:rgba(255,255,255,.1);color:rgba(255,255,255,.65);cursor:default;}'
+ '.sfrq-btn[data-s="downloading"]{background:rgba(90,160,255,.22);color:#cfe2ff;cursor:default;}'
+ '.sfrq-btn[data-s="available"]{background:rgba(80,200,120,.2);color:#bdf0cd;}'
+ '.sfrq-btn[data-s="error"]{background:rgba(224,38,63,.9);color:#fff;}'
+ '.sfrq-spin{width:15px;height:15px;border:2px solid rgba(255,255,255,.28);border-top-color:#fff;'
+ 'border-radius:50%;animation:sfrqspin .7s linear infinite;}'
+ '@keyframes sfrqspin{to{transform:rotate(360deg);}}';
var st = document.createElement('style'); st.textContent = css; document.head.appendChild(st);

function esc(s){ return String(s == null ? '' : s); }
function token(){
  try { return JSON.parse(localStorage.getItem('jellyfin_credentials')).Servers[0].AccessToken; }
  catch(e){ return ''; }
}

/* Her four states. Anything the backend has not actually confirmed as moving
   stays at "Requested" -- we do not invent "Coming soon" from a timer. */
var LABEL = {
  none:        '＋ Request',
  busy:        '',
  requested:   '✓ Requested',
  /* sf-req-states: queued and processing used to be MISSING here, so they fell
     through to '＋ Request' and the album looked like it had never been asked
     for. Queued is where a request spends most of its life. */
  queued:      '✓ Requested',
  downloading: '⬇ Coming soon',
  processing:  '⬇ Almost ready',
  available:   '▶ Play',
  failed:      '↻ Try again',
  error:       'Couldn’t submit — Try Again'
};

function paint(btn, state){
  btn.dataset.s = state;
  btn.textContent = '';
  if (state === 'busy') {
    var sp = document.createElement('span'); sp.className = 'sfrq-spin'; btn.appendChild(sp);
  } else {
    btn.textContent = LABEL[state] || LABEL.none;
  }
  /* anything already in flight must not be re-submittable; 'failed' stays
     enabled deliberately so a retry is one tap. */
  btn.disabled = (state === 'busy' || state === 'requested' || state === 'queued'
                  || state === 'downloading' || state === 'processing');
}

function submit(btn, item){
  paint(btn, 'busy');
  fetch(BRIDGE + '/api/request', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', 'X-Jellyfin-Token': token() },
    body: JSON.stringify({
      kind: item.kind, ref: item.ref, title: item.title,
      artist: item.artist, album: item.album, mkind: item.mkind
    })
  }).then(function(r){
    /* Only a real backend confirmation earns "Requested". */
    if (r.ok) return r.json().then(function(){ paint(btn, 'requested'); });
    paint(btn, 'error');
  }).catch(function(){ paint(btn, 'error'); });
}

/* Insert an artist's real albums straight after their card, as ordinary album
   cards -- so every existing state, label and submit path applies unchanged.
   Inserted into the same grid rather than a new container: the grid already
   flows, so this needs no new CSS and cannot disturb the section's rhythm. */
function expandArtist(btn, item, card){
  if (btn.dataset.done === '1') return;
  btn.disabled = true;
  btn.textContent = '';
  var sp = document.createElement('span'); sp.className = 'sfrq-spin'; btn.appendChild(sp);
  fetch(BRIDGE + '/api/artist?mbid=' + encodeURIComponent(item.ref), {
    headers: { 'X-Jellyfin-Token': token() }
  }).then(function(r){ return r.json(); }).then(function(j){
    var list = (j && j.albums) || [];
    if (!list.length) { btn.textContent = 'No albums found'; return; }
    var grid = card.parentNode;
    if (!grid) { btn.textContent = 'No albums found'; return; }
    var next = card.nextSibling;
    list.forEach(function(a){
      /* /api/artist carries no artist NAME (it is keyed by mbid), and keyOf()
         on the bridge includes the artist -- so pass the one from this card,
         otherwise the request would be filed against an empty artist. */
      grid.insertBefore(buildCard({
        kind: 'music', mkind: 'album', ref: a.ref,
        title: a.title, artist: item.artist, album: a.title || a.album,
        subtitle: [item.artist, a.year].filter(Boolean).join(' · '),
        image: '', state: a.state || 'none', done: a.done, total: a.total
      }), next);
    });
    btn.dataset.done = '1';
    btn.textContent = '✓ ' + list.length + ' albums';
  }).catch(function(){
    btn.textContent = 'Couldn’t load albums';
    btn.disabled = false;
  });
}

function buildCard(item){
  /* Deliberately NOT Jellyfin's .card/.cardBox: those classes carry their own
     width and flex rules and collapse to slivers inside a CSS grid. We match
     the theme's measured values (12px radius, same type scale) instead. */
  var wrap = document.createElement('div');
  wrap.className = 'sfrq-card';

  var box = document.createElement('div'); box.className = 'sfrq-box';
  var art = document.createElement('div'); art.className = 'sfrq-art';
  if (item.image) art.style.backgroundImage = 'url(' + JSON.stringify(item.image) + ')';
  else {
    var fb = document.createElement('div'); fb.className = 'sfrq-art-fallback';
    fb.textContent = item.kind === 'audiobook' ? '🎧' : '🎵';
    art.appendChild(fb);
  }
  box.appendChild(art);

  var t = document.createElement('div'); t.className = 'sfrq-t'; t.textContent = esc(item.title);
  box.appendChild(t);
  var s = document.createElement('div'); s.className = 'sfrq-s'; s.textContent = esc(item.subtitle || '');
  box.appendChild(s);

  var btn = document.createElement('button');
  btn.className = 'sfrq-btn';
  /* sf-artist-albums: an ARTIST card must never submit. The bridge now refuses
     it (400 artist_not_requestable) because an artist has no single album to
     fetch -- requesting "Adele" used to search Soulseek for "Adele Adele" and
     fail 5 times in silence. Refusing alone would be a dead end though: a bare
     artist search returns almost no albums BY that artist (MusicBrainz matches
     on title, so "adele" returns albums *called* Adele by other acts), so the
     artist card is the only route to her real records. Expand it instead --
     /api/artist?mbid= already returned Adele's 30/25/21/19 in 474ms and was
     never called by any UI until now. */
  if (item.mkind === 'artist') {
    paint(btn, 'none');
    btn.textContent = '♫ Albums';
    btn.disabled = false;
    btn.addEventListener('click', function(){ expandArtist(btn, item, wrap); });
    /* sf-artist-getall: the bridge can now take an artist wholesale -- every
       release it does not already have, plus a standing subscription to what
       they release next. Browsing stays first because wanting one album is the
       commoner case. */
    var all = document.createElement('button');
    all.className = 'sfrq-btn';
    all.textContent = '\u002B Get all';
    all.addEventListener('click', function(){
      all.disabled = true;
      all.textContent = 'Working...';
      fetch(BRIDGE + '/api/request', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'X-Jellyfin-Token': token() },
        body: JSON.stringify({
          kind: item.kind, ref: item.ref, title: item.title,
          artist: item.artist, album: item.album, mkind: item.mkind
        })
      }).then(function(r){
        if (!r.ok) throw new Error('http ' + r.status);
        return r.json();
      }).then(function(j){
        all.textContent = (j && j.requested)
          ? ('Getting ' + j.requested + ' albums')
          : 'Tracking this artist';
      }).catch(function(){
        all.disabled = false;
        all.textContent = 'Try again';
      });
    });
    box.appendChild(all);
  } else {
    paint(btn, item.state === 'none' ? 'none' : item.state);
    btn.addEventListener('click', function(){
      var s = btn.dataset.s;
      if (s === 'none' || s === 'error') submit(btn, item);
    });
  }
  box.appendChild(btn);

  wrap.appendChild(box);
  return wrap;
}

function buildSection(title, sub, items){
  var sec = document.createElement('div');
  sec.className = 'verticalSection sfrq-sec';
  var head = document.createElement('div'); head.className = 'sfrq-head';
  var h = document.createElement('h2'); h.className = 'sectionTitle sectionTitle-cards';
  h.textContent = title; head.appendChild(h);
  sec.appendChild(head);
  var sb = document.createElement('div'); sb.className = 'sfrq-sub'; sb.textContent = sub;
  sec.appendChild(sb);
  var grid = document.createElement('div'); grid.className = 'sfrq-grid';
  items.forEach(function(i){ grid.appendChild(buildCard(i)); });
  sec.appendChild(grid);
  return sec;
}


/* Jellyfin's own empty-state. Located by class first, then by text as a
   fallback so a theme or version change does not silently break it. */
function nativeEmptyEls(page){
  var out = [], i;
  var byClass = page.querySelectorAll('.noItemsMessage, .centerMessage');
  for (i = 0; i < byClass.length; i++) out.push(byClass[i]);
  if (!out.length) {
    /* sf-empty-shallow: this fallback used to be
         page.querySelectorAll('div,p,h1,h2,h3')
       and then, PER ELEMENT, a .querySelector('.sfrq-sec') subtree search plus
       a .textContent that concatenates that element's whole subtree. Measured
       on a real query ("love"): 6346 elements scanned, 6.7ms per call on a
       desktop -- and this runs from tick(), which fires every 400ms AND on
       every DOM mutation with no debounce. While Jellyfin paints 568 cards and
       Jellyseerr appends its own, that is hundreds of calls back to back; the
       main thread stalls, and a stalled main thread never runs Jellyfin's
       loading.hide(), which is what leaves the spinner turning forever. A
       phone is several times slower again.
       The expensive path also ran in the COMMON case, not the rare one: it is
       entered precisely when there is no empty-state element, i.e. whenever
       the search actually found something.
       An empty-state banner is a direct child of the page or of its results
       wrapper -- it is never buried inside a card -- so scan two levels, not
       the whole subtree. ~10 elements instead of 6346. */
    var shallow = [], k, kid;
    for (k = 0; k < page.children.length; k++) {
      kid = page.children[k];
      shallow.push(kid);
      for (i = 0; i < kid.children.length; i++) shallow.push(kid.children[i]);
    }
    for (i = 0; i < shallow.length; i++) {
      if (shallow[i].querySelector('.sfrq-sec')) continue;      // never our own
      if (/no results found/i.test(shallow[i].textContent || '') &&
          shallow[i].querySelectorAll('div,p,h1,h2,h3').length <= 2) { out.push(shallow[i]); break; }
    }
  }
  return out;
}

/* Does Jellyfin itself have anything? Its cards carry .card; ours never do. */
function jellyfinHasResults(page){
  var cards = page.querySelectorAll('.card'), i, c;
  for (i = 0; i < cards.length; i++) {
    c = cards[i];
    if (c.closest('.sfrq-sec')) continue;              /* never our own */
    /* sf-empty-hidden-cards: the Jellyseerr search integration leaves its movie
       cards in the DOM with display:none even when it has nothing to show.
       Measured on a music-only query ("Fleetwood Mac"): 19 .card elements in
       #searchPage, 0 of them visible, all inside .jellyseerr-* sections.
       Counting those made this function report "Jellyfin has results", so
       syncNativeEmpty() never suppressed the empty-state -- and the result was
       "Sorry! No results found" displayed directly above 18 albums she could
       have tapped to request. That is the exact failure this feature exists to
       avoid. Only a card that actually renders counts as a real result.
       getClientRects() is used rather than offsetParent because it is not
       fooled by positioned ancestors. */
    if (!c.getClientRects().length) continue;
    return true;
  }
  return false;
}

/* Three states, per spec:
     Jellyfin has results                      -> leave Jellyfin entirely alone
     Jellyfin empty BUT we have requestables    -> hide the empty-state
     Jellyfin empty AND we have nothing         -> leave the empty-state showing
   Telling her "No results found" directly above an album she can request makes
   the feature look broken, so only that middle case is suppressed. */
function syncNativeEmpty(page){
  var weHaveResults = !!page.querySelector('.sfrq-sec .sfrq-card');
  var hide = weHaveResults && !jellyfinHasResults(page);
  nativeEmptyEls(page).forEach(function(el){
    if (hide) {
      if (!el.dataset.sfrqHid) { el.dataset.sfrqHid = '1'; el.style.display = 'none'; }
    } else if (el.dataset.sfrqHid) {
      el.style.display = '';
      delete el.dataset.sfrqHid;
    }
  });
}

var lastQuery = '', inFlight = null, timer = null;

function currentQuery(){
  var inp = document.querySelector('.searchFields input, input[type="search"], .searchfields-txtSearch');
  if (inp && inp.value != null && inp.value.trim()) return inp.value.trim();
  var m = String(location.hash || '').match(/[?&]query=([^&]*)/);
  return m ? decodeURIComponent(m[1].replace(/\+/g, ' ')) : '';
}

function searchPage(){
  var pages = document.querySelectorAll('#searchPage, .searchPage, [data-type="search"]');
  for (var i = 0; i < pages.length; i++) if (pages[i].offsetParent !== null) return pages[i];
  return null;
}

function clearOurs(){
  document.querySelectorAll('.sfrq-sec').forEach(function(e){ e.remove(); });
  /* Put Jellyfin's empty-state back the moment we stop covering for it. */
  document.querySelectorAll('[data-sfrq-hid]').forEach(function(el){
    el.style.display = '';
    delete el.dataset.sfrqHid;
  });
}

function render(q){
  var page = searchPage();
  if (!page) return;
  fetch(BRIDGE + '/api/search?kind=all&q=' + encodeURIComponent(q), {
    headers: { 'X-Jellyfin-Token': token() }
  }).then(function(r){ return r.ok ? r.json() : { results: [] }; })
    .then(function(d){
      if (currentQuery() !== q) return;           // user typed on; drop stale answer
      clearOurs();
      var res = d.results || [];
      var music = res.filter(function(x){ return x.kind === 'music'; });
      var books = res.filter(function(x){ return x.kind === 'audiobook'; });
      /* A section with nothing missing is not shown at all -- an empty
         "Not in your library" heading reads like a failure. */
      if (music.length) page.appendChild(buildSection('Music', 'Not in your library', music));
      if (books.length) page.appendChild(buildSection('Audiobooks', 'Not in your library', books));
      syncNativeEmpty(page);
    }).catch(function(){ /* stay silent; Jellyfin's own results are unaffected */ });
}

function tick(){
  var page = searchPage();
  if (!page) { if (lastQuery) { lastQuery = ''; clearOurs(); } return; }
  var q = currentQuery();
  syncNativeEmpty(page);   // Jellyfin can paint its empty-state after we render
  if (q === lastQuery) return;
  lastQuery = q;
  clearOurs();
  if (q.length < 2) return;
  clearTimeout(timer);
  timer = setTimeout(function(){ render(q); }, 450);   // debounce typing
}

setInterval(tick, 400);
/* sf-tick-debounce: this was `new MutationObserver(tick)` -- tick() ran once
   per mutation batch, synchronously, with no coalescing. Jellyfin and
   Jellyseerr both append cards in many small batches, so a single search fired
   tick() hundreds of times in a row, each doing a full-page scan. Coalescing
   to one run per frame-ish window collapses that to a handful of calls without
   changing what tick() does or when the user sees the result. */
var moTimer = null;
new MutationObserver(function(){
  if (moTimer) return;
  moTimer = setTimeout(function(){ moTimer = null; tick(); }, 80);
}).observe(document.body, { childList: true, subtree: true });
})();</script>'''

SEARCHSKEL_MARKER = 'sf-search-skel'
# sf-search-skel (2026-09-01). The admin: "my jellyfin search doesnt work".
# It worked -- it just showed NOTHING while it did. Measured on a phone
# viewport: after the last keystroke the page stayed completely blank for
# 3.66s before the first result painted, with no spinner, no placeholder and
# no message. There is nothing on screen to distinguish "searching" from
# "broken", so a person types, waits, sees an empty page and concludes the
# feature is dead. (sf-srchcount and sf-exact-first took that first paint to
# ~1.2s, which is better but still far past the ~100ms at which a delay stops
# feeling instant, so the blank window still needs filling.)
# Deliberately a skeleton and not a spinner: it occupies the shape the results
# will take, so the arrival of real cards is a fill rather than a jump -- this
# page has a history of layout shift eating taps.
SEARCHSKEL_SCRIPT = r"""<script>(function(){
/* sf-search-skel */
/* sf-qskel, not sf-skel: sf-livesports.js already ships
   '.sf-skel{display:none!important;}' -- a different, deliberately parked
   skeleton system (.sf-skel-off/.sf-skel-row/.sf-skel-card). Reusing that class
   meant this element was created, inserted and correctly torn down while being
   display:none the whole time: every DOM assertion passed and nothing was ever
   drawn. Caught only by measuring the rendered box (0x0) rather than trusting
   querySelector. */
if (window.__sfSearchSkel) return;
window.__sfSearchSkel = 1;

var css =
  '.sf-qskel{padding:0 3.3%;margin:1.1em 0 0;order:5;}'
+ '.sf-qskel-h{height:1.05em;width:7.5em;border-radius:6px;margin:0 0 .9em;}'
+ '.sf-qskel-g{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:1.1em .8em;}'
+ '@media (min-width:500px){.sf-qskel-g{grid-template-columns:repeat(auto-fill,minmax(150px,1fr));}}'
+ '.sf-qskel-c{aspect-ratio:2/3;border-radius:12px;}'
/* the same glass tokens the rest of Abyss uses, so this reads as part of the
   theme rather than a generic grey placeholder */
+ '.sf-qskel-h,.sf-qskel-c{background-color:rgba(255,255,255,.05);'
+ 'background-image:linear-gradient(100deg,rgba(255,255,255,0) 30%,rgba(255,255,255,.075) 50%,rgba(255,255,255,0) 70%);'
+ 'background-size:200% 100%;background-repeat:no-repeat;'
+ 'animation:sfskel 1.25s ease-in-out infinite;}'
+ '@keyframes sfskel{from{background-position:190% 0;}to{background-position:-30% 0;}}'
+ '@media (prefers-reduced-motion:reduce){.sf-qskel-h,.sf-qskel-c{animation:none;}}';
var st = document.createElement('style');
st.textContent = css;
document.head.appendChild(st);

function visiblePage(){
  var all = document.querySelectorAll('#searchPage'), i;
  for (i = 0; i < all.length; i++) {
    if (!all[i].classList.contains('hide') && all[i].offsetParent !== null) return all[i];
  }
  return null;
}
function currentQuery(){
  var ins = document.querySelectorAll('input.searchfields-txtSearch'), i;
  for (i = 0; i < ins.length; i++) {
    if (ins[i].getClientRects().length) return String(ins[i].value || '').trim();
  }
  return '';
}
/* A section only counts as "results are here" once it has a card that is
   actually laid out. Jellyfin and Jellyseerr both leave display:none sections
   in the DOM, and counting those would tear the skeleton down over a blank
   page -- the exact failure this exists to prevent. */
function hasVisibleResults(p){
  var secs = p.querySelectorAll('.verticalSection,.sfrq-sec'), i, s;
  for (i = 0; i < secs.length; i++) {
    s = secs[i];
    if (!s.getClientRects().length) continue;
    if (s.classList.contains('sf-qskel')) continue;
    if (s.querySelector('.card,.sfrq-card')) return true;
  }
  return false;
}
/* Jellyfin's own "nothing found" element. Without this the skeleton would
   shimmer over a genuine no-match until the safety timeout. */
function saysEmpty(p){
  var n = p.querySelectorAll('.noItemsMessage,.centerMessage,[class*="noResults"]'), i;
  for (i = 0; i < n.length; i++) if (n[i].getClientRects().length) return true;
  return false;
}

function build(){
  var d = document.createElement('div');
  d.className = 'sf-qskel';
  d.setAttribute('aria-hidden', 'true');
  var h = document.createElement('div'); h.className = 'sf-qskel-h'; d.appendChild(h);
  var g = document.createElement('div'); g.className = 'sf-qskel-g';
  for (var i = 0; i < 6; i++) {
    var c = document.createElement('div'); c.className = 'sf-qskel-c'; g.appendChild(c);
  }
  d.appendChild(g);
  return d;
}

var lastQ = null, since = 0;
/* 250ms grace so a fast (cached) answer never flashes a skeleton, and a 7s
   cap so a hung query cannot shimmer forever. */
var GRACE_MS = 250, MAX_MS = 7000;

function tick(){
  try {
    var p = visiblePage();
    var q = p ? currentQuery() : '';
    if (q !== lastQ) { lastQ = q; since = Date.now(); }
    var cur = p ? p.querySelector(':scope > .sf-qskel') : null;
    /* the skeleton lives on whichever host the sections do, so flex order
       applies to it as well -- see sf-rank-onehost */
    var host = p ? (p.querySelector('.searchResults') || p) : null;
    if (!cur && host) cur = host.querySelector(':scope > .sf-qskel');

    var want = !!p && q.length >= 1
            && (Date.now() - since) > GRACE_MS
            && (Date.now() - since) < MAX_MS
            && !hasVisibleResults(p)
            && !saysEmpty(p);

    if (want && !cur) host.appendChild(build());
    else if (!want && cur && cur.parentNode) cur.parentNode.removeChild(cur);
  } catch (e) {}
}
setInterval(tick, 160);
})();</script>"""

SEARCHRANK_MARKER = 'sf-search-rank'
SEARCHRANK_SCRIPT = r'''<script>(function(){
/* sf-search-rank */
/* Gives every search section a rank, so the page reads the same on every load.
   The CSS half of this lives in the main style block (sf-rank-nesting).

   Why a script at all: the order a section deserves depends on WHAT IT IS, and
   the only thing that says so is its heading text ("Movies", "Songs"). CSS
   cannot select on text, so the classification happens here and is handed to
   CSS as a data attribute. CSS still does the moving -- no node is ever
   reparented for ordering, because an appendChild-based reorder driven off a
   MutationObserver froze this page once already.

   Ranks: 10 movies & TV | 20 people | 30 music you own | 40 artists
          | 50 Jellyseerr | 60 music to request. */

var RANK = [
  /* Checked in order; class beats heading text, because .jellyseerr-section
     and .sfrq-sec both also carry .verticalSection, and the Jellyseerr heading
     is rewritten to "Add to your library" by jf-seerr-fallback. */
  { cls: 'sfrq-sec',           rank: 60 },
  { cls: 'jellyseerr-section', rank: 50 },
  { cls: 'sf-lib-albums',      rank: 30 }
];

/* Jellyfin's own section headings on this build, lower-cased. Anything not
   listed falls through to 15 and stays with the library content. */
/* Observed on this server, not guessed: the sweep threw up "Audio Books" --
   with a space -- which fell through to 15 and sat above People. Any heading
   this build can produce should be placed on purpose, so the audio kinds are
   spelled out both ways and the video-ish extras are covered too. */
var TITLE_RANK = {
  'movies': 10, 'shows': 10, 'series': 10, 'episodes': 10, 'videos': 10,
  'collections': 10, 'movie collections': 10, 'box sets': 10, 'trailers': 10,
  'live tv': 10, 'programs': 10, 'channels': 10, 'recordings': 10,
  'people': 45, 'actors': 45,
  'albums': 30, 'songs': 30, 'music videos': 30, 'music albums': 30,
  'playlists': 30, 'books': 30, 'audiobooks': 30, 'audio books': 30,
  'photos': 30, 'photo albums': 30,
  'artists': 40, 'album artists': 40
};

/* The heading holds the Jellyseerr refresh BUTTON as well as the label, so
   .textContent would read "Add to your libraryrefresh". Only direct text
   nodes are the title. */
function headingText(sec){
  var h = sec.querySelector('.sectionTitle') || sec.querySelector('h2');
  if (!h) return '';
  var s = '', i;
  for (i = 0; i < h.childNodes.length; i++) {
    if (h.childNodes[i].nodeType === 3) s += h.childNodes[i].nodeValue;
  }
  /* fall back to the full text only when there are no direct text nodes */
  if (!s.trim()) s = h.textContent || '';
  return s.trim().toLowerCase();
}

/* sf-rank-bytype (2026-08-21). Two defects in ranking by heading text:

   1. PEOPLE OUTRANKED THE MUSIC. Searching "Adele" put 38 Person cards --
      "Adele Abinante", "Adele Baughn" and other film crew -- above the actual
      recording artist, which was the LAST section on the page. Person is the
      one result kind that is almost never what was meant, so it now sits below
      everything you own.
   2. IT ONLY WORKED IN ENGLISH. TITLE_RANK is keyed on lowercase English
      headings, so on a German or Chinese profile every section missed and fell
      to the default 15 -- the same class of bug that once left the music page
      empty in de/zh by matching an English tab name.

   Cards carry data-type, which is the same in every language, so rank on the
   dominant type of a section's cards and keep the heading only as a fallback
   for sections whose cards carry no type (the Jellyseerr row). */
var TYPE_RANK = {
  'Movie':10,'Series':10,'Episode':10,'Video':10,'BoxSet':10,'Trailer':10,
  'Program':10,'TvChannel':10,'Recording':10,'LiveTvProgram':10,'LiveTvChannel':10,
  'MusicAlbum':30,'Audio':30,'MusicVideo':30,'Playlist':30,'Book':30,
  'AudioBook':30,'Photo':30,'PhotoAlbum':30,
  'MusicArtist':40,'AlbumArtist':40,
  'Person':45
};
function typeRankOf(sec){
  var cards = sec.querySelectorAll('[data-type]'), i, t, tally = {}, best = null, n = 0;
  for (i = 0; i < cards.length; i++) {
    t = cards[i].getAttribute('data-type');
    if (!t || TYPE_RANK[t] == null) continue;
    tally[t] = (tally[t] || 0) + 1;
    if (tally[t] > n) { n = tally[t]; best = t; }
  }
  return best === null ? null : TYPE_RANK[best];
}
/* sf-exact-first (2026-09-01). Searching "psych" put the SHOW Psych third,
   under two American Psycho films. Not a bug in the ranking -- Movies and Shows
   both rank 10, so within that band the page fell back to DOM order, which is
   whichever section Jellyfin happened to append first. The thing a person
   typed the word for was never considered.
   So inside the video band only, a section that holds an EXACT title match
   moves to 8 and one that holds a PREFIX match to 9. Two deliberate limits:
   it can only reorder rank 10 against itself (music, people and the two
   request rows keep the places they were given for other reasons), and it can
   only ever promote -- nothing is pushed below where it already sat. */
function normTitle(s){
  return String(s == null ? '' : s).toLowerCase()
    .replace(/[\u2018\u2019\u02bc]/g, "'")
    .replace(/\s+/g, ' ').trim();
}
/* The hash is not reliable here: it carries the query only once Jellyfin has
   committed it, which is exactly the window this runs in. The visible input is
   the truth, with the hash as the fallback for a link opened cold. */
function searchQ(){
  var ins = document.querySelectorAll('input.searchfields-txtSearch'), i;
  for (i = 0; i < ins.length; i++) {
    if (ins[i].getClientRects().length && ins[i].value) return normTitle(ins[i].value);
  }
  return normTitle(queryOf());
}
function matchBoost(sec, band){
  if (band !== 10) return 0;
  var q = searchQ();
  if (!q || q.length < 2) return 0;
  var texts = sec.querySelectorAll('.cardText-first, .cardText'), i, t, best = 0;
  for (i = 0; i < texts.length && i < 60; i++) {
    t = normTitle(texts[i].textContent);
    if (!t) continue;
    if (t === q) return 2;
    /* prefix only at a word boundary, so "psych" promotes "Psych: The Movie"
       but not "Psychological Warfare" -- that one is merely a substring and
       already ranks where it should. */
    if (t.length > q.length) {
      var nx = t.charAt(q.length);
      if (t.indexOf(q) === 0 && (nx === ' ' || nx === ':' || nx === ',' || nx === '-')) best = 1;
    }
  }
  return best;
}
function rankOf(sec){
  var i, cl = ' ' + sec.className + ' ';
  for (i = 0; i < RANK.length; i++) {
    if (cl.indexOf(' ' + RANK[i].cls + ' ') >= 0) return RANK[i].rank;
  }
  var byType = typeRankOf(sec);
  if (byType != null) return byType - matchBoost(sec, byType);
  var t = headingText(sec);
  if (TITLE_RANK[t] != null) return TITLE_RANK[t];
  return 15;
}

function page(){
  var all = document.querySelectorAll('#searchPage'), i;
  for (i = 0; i < all.length; i++) {
    if (!all[i].classList.contains('hide') && all[i].offsetParent !== null) return all[i];
  }
  return null;
}

/* sf-own-first: the "Jellyseerr shows up first and everything else pops in
   above it" problem. It is not an ordering bug -- flex order is already
   correct -- it is a TIMING one. Measured on one load: the Jellyseerr search
   answers at ~3.5s while Jellyfin's own library query is still running, and
   the request bridge answers at ~1.5s, so for a second or more the only row
   on screen is one of the "you do not have this" rows. The page then reflows
   as the library rows land above it, which is what reads as broken.
   So hold the two not-in-your-library rows until Jellyfin's own search has
   actually FINISHED -- which is a signal, not a duration. Two things can mean
   finished: a library section is on screen, or Jellyfin has put up its own
   "no results" element (it renders that element only when the query really
   found nothing -- measured 0 of them whenever there were results). A first
   attempt used a flat 2500ms timer and failed in exactly the way timers do:
   under load this server took 8.4s to paint its library rows, the timer was
   long gone, and Jellyseerr appeared alone at 5.8s -- the original complaint,
   unchanged. The remaining timeout is only a dead-man's switch so a hung
   library query cannot hide Jellyseerr forever. */
var SAFETY_MS = 15000;
/* The empty-state has to STAY up to count. Jellyfin puts "no results found" on
   screen while its query is still in flight, so treating the first sighting as
   "finished" opened the gate mid-load -- observed letting the Jellyseerr row
   appear alone at 8.5s with nothing owned on screen yet, which is the exact
   thing the gate exists to prevent. A real empty result never takes it back
   down; a transient one does, well inside this dwell. */
var EMPTY_DWELL_MS = 1500;
var gateQuery = null, gateStart = 0, gateOpen = false, emptySince = 0;

function queryOf(){
  var h = String(location.hash || ''), i = h.indexOf('query=');
  if (i < 0) return '';
  var raw = h.substring(i + 6), amp = raw.indexOf('&');
  if (amp >= 0) raw = raw.substring(0, amp);
  try { return decodeURIComponent(raw.split('+').join(' ')).trim(); } catch (e) { return raw; }
}

/* Ranks 10-40 are the things you already own; 50 and 60 are the two we gate.
   Once open it stays open for this query, so a row can never flicker back out
   from under the pointer. */
function gate(p){
  var q = queryOf();
  if (q !== gateQuery) { gateQuery = q; gateStart = Date.now(); gateOpen = false; emptySince = 0; }
  if (gateOpen) return true;
  var owned = p.querySelectorAll('[data-sfrank="10"],[data-sfrank="15"],[data-sfrank="20"],[data-sfrank="30"],[data-sfrank="40"],[data-sfrank="45"]');
  for (var i = 0; i < owned.length; i++) {
    if (owned[i].getClientRects().length) { gateOpen = true; return true; }
  }
  /* Jellyfin searched and came back with nothing -- that is finished too, and
     it is the case where the request rows are the ONLY useful thing on the
     page, so they must not be held back. Test for existence, not visibility:
     sf-request-search hides this element (tracking it with data-sfrq-hid) when
     it has requestables to show in its place. */
  if (p.querySelector('.noItemsMessage, .centerMessage')) {
    if (!emptySince) emptySince = Date.now();
    if (Date.now() - emptySince > EMPTY_DWELL_MS) { gateOpen = true; return true; }
  } else {
    emptySince = 0;                      /* it went away: it was mid-load noise */
  }
  if (Date.now() - gateStart > SAFETY_MS) gateOpen = true;
  return gateOpen;
}

function apply(){
  var p = page();
  if (!p) return;

  /* sf-rank-onehost: flex `order` only sorts among SIBLINGS. The owned-albums
     row is built by sfOwnedAlbums() and lands wherever the DOM happened to be
     when its fetch answered -- inside .searchResults if Jellyfin had already
     rendered, directly on #searchPage if it won the race. In the second case
     it is a sibling of .searchResults rather than of the sections, so no rank
     can place it between Movies and People. Re-home it once, and only when it
     is actually in the wrong host, so this is not a per-tick mutation. */
  var results = p.querySelector('.searchResults');
  if (results) {
    /* sf-one-container: both custom rows are re-homed, and not only so that
       flex order can sort them against Jellyfin's sections (order only sorts
       SIBLINGS). It is also what makes the spacing uniform. .searchResults
       carries Jellyfin's padded-bottom-page, so a row left outside it sat
       BELOW that padding: the request row measured a 104px gap above it where
       every other row had 0-15px -- 74px of page padding plus its own 30px
       margin. Inside the container it takes part in the same rhythm as the
       native rows and the page padding stays where it belongs, under
       everything. Each move is guarded on the node actually being in the wrong
       place, so this is not a per-tick mutation. */
    var stray = p.querySelector(':scope > .sf-lib-albums');
    if (stray) results.appendChild(stray);
    var strayReq = p.querySelector(':scope > .sfrq-sec');
    if (strayReq) results.appendChild(strayReq);
  }

  var secs = p.querySelectorAll('.verticalSection, .sf-lib-albums, .sfrq-sec'), i, s, r;
  for (i = 0; i < secs.length; i++) {
    s = secs[i];
    r = String(rankOf(s));
    /* write only on change: this runs off a MutationObserver, and an
       unconditional setAttribute would retrigger it forever. */
    if (s.dataset.sfrank !== r) s.dataset.sfrank = r;
  }

  /* sf-seerr-once: Jellyseerr is allowed exactly one row. Its integration can
     leave extra .jellyseerr-section nodes in the page with nothing in them,
     and a second "Add to your library" heading under the real one just reads
     as the page being broken. Keep the first section that actually has a card
     and collapse the rest.
     Emptiness is judged on RENDERED cards (getClientRects), not on card count:
     the integration leaves its cards in the DOM with display:none rather than
     removing them, so counting nodes would call an empty row full -- the same
     trap sf-empty-hidden-cards documents. display is an attribute change, and
     the observers here watch childList only, so this cannot feed itself. */
  var open = gate(p);

  /* Keep the FULLEST row, not merely the first. Confirmed by reading both:
     same heading, same leading titles (Brüno, Bruno the Kid, Numero Bruno...)
     -- two renders of the same query, not movies-vs-TV -- but one had 59 cards
     and the other 34, and the shorter one carried a few titles the longer one
     had not paged in. Whichever is richer is the one to show; "first" would
     sometimes have picked the stub. */
  var seerrs = p.querySelectorAll('.jellyseerr-section'), j, sec, n, best = null, bestN = -1;
  for (j = 0; j < seerrs.length; j++) {
    n = realCardCount(seerrs[j]);
    if (n > bestN) { bestN = n; best = seerrs[j]; }
  }
  for (j = 0; j < seerrs.length; j++) {
    sec = seerrs[j];
    show(sec, open && sec === best && bestN > 0);
  }

  /* the music-request row rides the same gate */
  var reqs = p.querySelectorAll('.sfrq-sec');
  for (j = 0; j < reqs.length; j++) show(reqs[j], open);
}

/* write display only on change -- these run off a MutationObserver */
function show(el, on){
  if (on) { if (el.style.display === 'none') el.style.display = ''; }
  else if (el.style.display !== 'none') { el.style.display = 'none'; }
}

/* Does this Jellyseerr section have anything real in it?
   getClientRects() -- what the rest of this file uses to mean "visible" -- is
   NOT usable here: the gate above may already have hidden the section, and a
   hidden ancestor zeroes every descendant's rects, so a real row would report
   itself empty on the very next tick and could never be chosen again.
   A card's OWN computed display is unaffected by a hidden ancestor, so it
   still distinguishes the integration's deliberately hidden cards (measured:
   34 of them, all display:none, in the duplicate row) from real ones (74).
   Cached per query, and a negative is only cached once the row actually has
   card nodes -- otherwise a row inspected before it filled would be written
   off permanently. */
function realCardCount(sec){
  var cards = sec.querySelectorAll('.card'), k, n = 0;
  if (!cards.length) return 0;                     /* not filled yet: ask again */
  /* Cached on the node and keyed by query + card count, because this runs from
     apply() on every animation frame during a render storm and getComputedStyle
     forces style resolution. The key changes exactly when there is something
     new to count, so a growing row is still re-measured -- without that, a row
     measured at 34 cards would be frozen at 34 while it paged up to 59 and the
     wrong row could win. */
  var key = gateQuery + ':' + cards.length;
  if (sec.dataset.sfseerrKey === key) return +sec.dataset.sfseerrN;
  for (k = 0; k < cards.length; k++) {
    if (getComputedStyle(cards[k]).display !== 'none') n++;
  }
  sec.dataset.sfseerrKey = key;
  sec.dataset.sfseerrN = String(n);
  return n;
}

/* sf-rank-preframe: coalesce with requestAnimationFrame, not a timeout. A
   section is inserted with no rank, so it sits at the initial order:0 and
   paints at the TOP until the next pass ranks it. With a 60ms timeout that
   was visible as sections leaping to the top and snapping back -- recorded
   over one load as Music jumping first, then last, and Jellyseerr and the
   album row trading places twice between 6.6s and 7.5s. rAF runs after the
   mutation but BEFORE the browser paints, so a new section is ranked in the
   same frame it appears and never paints in the wrong place. Still one pass
   per frame however many mutations arrive, and this pass is cheap (a
   querySelectorAll plus attribute compares; the only costly read is cached).
   The interval stays as a backstop -- rAF does not run in a background tab. */
var raf = null;
function schedule(){
  if (raf) return;
  raf = requestAnimationFrame(function(){ raf = null; apply(); });
}
new MutationObserver(schedule).observe(document.body, { childList: true, subtree: true });
setInterval(apply, 1000);
apply();
})();</script>'''

# ---------------------------------------------------------------------------
# jellyseerr detail-page rows: clip sideways overflow the way native rows do.
#
# Jellyfin's own detail rows (#similarCollapsible, Cast & Crew) compute
# overflow:hidden, so when a row is scrolled sideways the cards that slide past
# its left edge are clipped away. The Jellyseerr plugin builds its "Recommended"
# and "Similar" sections without that clipping (computed overflow: visible), so
# their cards keep painting outside the section: they slide left underneath the
# position:fixed poster in .detailImageContainer and stay visible around it.
# Measured on a movie page -- section left edge x=467, first card left x=93.
#
# Native's hidden is applied imperatively by Jellyfin's scroller, not by any
# stylesheet rule (nothing in document.styleSheets matches #similarCollapsible,
# and the element carries no inline style), so there is no existing class to
# reuse -- adding .detailVerticalSection to a seerr section does NOT clip it.
# Hence an explicit rule.
#
# Both axes, to match what native computes (overflow-x and -y both hidden). The
# scroller keeps its padded-*-focusscale classes, which reserve the room the
# hover/focus card scale needs, so clipping here does not crop that animation.
SEERRCLIP_MARKER = 'jf-seerr-clip'
SEERRCLIP_STYLE = ('<style id="jf-seerr-clip">'
                   '.jellyseerr-details-section{overflow:hidden;}'
                   '</style>')


# --- sf-search-i18n (2026-09-04): search in the language the titles are shown in.
# German users see translated titles everywhere (sf-title-i18n rewrites every card
# from the /api/titles map) but that map is a DISPLAY layer -- Jellyfin's search
# index only ever held the original name. Measured on the live server:
#     searchTerm=wimpy -> 3 results     searchTerm=gregs -> 0 results
# for a film whose German card reads "Gregs Tagebuch - Von Idioten umzingelt!".
# Server-side routes were tested and rejected: Tags are NOT searched (a tag on the
# item returns 0), and OriginalTitle -- which IS searched -- is global rather than
# per-user, so filling it with German would print German under the title for the
# English half of the house. So this stays a display-layer fix like the rest of the
# i18n work, and MERGES matches into the search response rather than injecting DOM:
# Jellyfin then renders them as its own results (correct cards, sections, images)
# and sf-title-i18n paints the German title on them as usual.
SEARCHI18N_MARKER = 'sf-search-i18n'
SEARCHI18N_SCRIPT = r'''<script>(function(){ /* sf-search-i18n */
var MAPKEY='sf-t18n-map';
function uid(){
try{if(window.ApiClient&&ApiClient.getCurrentUserId)return ApiClient.getCurrentUserId();}catch(e){}
try{var c=JSON.parse(localStorage.getItem('jellyfin_credentials')||'{}');
return (c.Servers&&c.Servers[0]&&c.Servers[0].UserId)||'';}catch(e){return '';}
}
function lang(){
var u=uid();if(!u)return '';
var v='';try{v=localStorage.getItem(u+'-language')||'';}catch(e){}
if(v.indexOf('zh')===0)return 'zh';
if(v.indexOf('de')===0)return 'de';
return '';
}
function bridge(){
return (location.port==='8096')
?(location.protocol+'//'+location.hostname+':8099')
:(location.origin+'/requestbridge');
}
function token(){
try{if(window.ApiClient&&ApiClient.accessToken)return ApiClient.accessToken();}catch(e){}
try{var c=JSON.parse(localStorage.getItem('jellyfin_credentials')||'{}');
return (c.Servers&&c.Servers[0]&&c.Servers[0].AccessToken)||'';}catch(e){return '';}
}
var MAP=null,PENDING=false;
/* Read sf-title-i18n's own cache rather than keeping a second copy of a ~1800
   entry map: it is written on every load, so it is warm before a keystroke. */
function ensureMap(L){
if(MAP)return MAP;
try{
var raw=localStorage.getItem(MAPKEY+'-'+L);
if(raw){var o=JSON.parse(raw);if(o&&o.items){MAP=o.items;return MAP;}}
}catch(e){}
if(!PENDING){
PENDING=true;
fetch(bridge()+'/api/titles',{headers:{'x-jellyfin-token':token()}})
.then(function(r){return r.json();})
.then(function(d){MAP=(d&&d.items)||{};PENDING=false;})
.catch(function(){PENDING=false;});
}
return null;
}
/* Fold accents and punctuation away, so "Gregs Tagebuch - Von Idioten umzingelt!"
   is reachable by "gregs tage" and "Boese Falle" by "bose". */
function fold(s){
s=String(s||'').toLowerCase();
try{s=s.normalize('NFD').replace(/[̀-ͯ]/g,'');}catch(e){}
return s.replace(/[^a-z0-9一-鿿]+/g,' ').replace(/^ +| +$/g,'');
}
function matchIds(q,L){
var m=ensureMap(L);if(!m)return [];
var needle=fold(q);
if(needle.length<2)return [];
var out=[],id,t;
for(id in m){
t=m[id]&&m[id][L];
if(!t)continue;
if(fold(t).indexOf(needle)>=0){out.push(id);if(out.length>=40)break;}
}
return out;
}
/* sf-search-hints: the search PAGE does not call /Items -- it calls
   /Search/Hints, whose payload is {SearchHints:[...]} with its own row shape,
   not {Items:[...]}. The first cut of this patch only knew about Items, so it
   bailed out on every real search and changed nothing (verified 2026-09-04:
   "gregs tage" still returned "Keine Ergebnisse"). Handle both shapes, and
   build a hint row for the hints endpoint. */
function toHint(it){
var tags=it.ImageTags||{};
var bd=(it.BackdropImageTags&&it.BackdropImageTags[0])||null;
return {ItemId:it.Id,Id:it.Id,Name:it.Name,
ProductionYear:it.ProductionYear,
PrimaryImageTag:tags.Primary||null,
ThumbImageTag:tags.Thumb||null,
ThumbImageItemId:tags.Thumb?it.Id:null,
BackdropImageTag:bd,
BackdropImageItemId:bd?it.Id:null,
Type:it.Type,MediaType:it.MediaType,
RunTimeTicks:it.RunTimeTicks||null,
IsFolder:!!it.IsFolder,
Artists:it.Artists||[],
ChannelId:it.ChannelId||null};
}
/* sf-search-xhr: the search page talks over XMLHttpRequest, not fetch.

   Two earlier attempts hooked window.fetch and a third hooked ApiClient.fetch;
   all three were correct code that never ran. Driving a real browser and
   counting requests by transport is what settled it -- for one search:

       xhr: 5   <- /Persons, /Artists and the three /Items that ARE the results
       windowFetch: 1, apiClientFetch: 1   <- one unrelated MusicArtist lookup

   So the results never pass through any fetch path. (A plugin tracking
   /Sessions/Playing also reassigns window.fetch wholesale after index.html
   parses, which was un-installing the first attempt on top of that.)

   XHR makes this harder in one specific way: `responseText` is a read-only
   getter and the load event is synchronous, so the merge cannot await anything.
   Hence the cache. The map lookup IS synchronous, so at send() time we already
   know which item ids a query should add; we start fetching their metadata then,
   in parallel with the search itself, and merge on a later response once it has
   landed. Jellyfin re-queries on each keystroke, so in normal typing the cache is
   warm well before the user stops. For the one-shot case -- a pasted URL, or a
   restored tab -- the fill nudges the page to re-run its own search exactly once
   per query, which is what makes a direct link to /web/#/search?query=... work.

   An own property defined on the instance shadows the prototype's getter; that
   is what lets a native XHR hand back an edited body. */
var ITEMS={};        /* id -> item metadata, once fetched */
var FETCHING={};     /* query -> true, so a burst of keystrokes fetches once */
var NUDGED={};       /* query -> true, so the re-run can never loop */

function cachedFor(ids){
var out=[],i;
for(i=0;i<ids.length;i++)if(ITEMS[ids[i]])out.push(ITEMS[ids[i]]);
return out;
}
function warm(q,ids){
if(FETCHING[q])return;
FETCHING[q]=true;
var need=[],i;
for(i=0;i<ids.length;i++)if(!ITEMS[ids[i]])need.push(ids[i]);
if(!need.length)return;
if(!window.ApiClient||!window.ApiClient.getItems)return;
window.ApiClient.getItems(uid(),{Ids:need.join(','),Recursive:true,Limit:40,
Fields:'PrimaryImageAspectRatio,ProductionYear'})
.then(function(d){
var add=(d&&d.Items)||[],k;
for(k=0;k<add.length;k++)ITEMS[add[k].Id]=add[k];
if(add.length)nudge(q);
}).catch(function(){});
}
/* Re-run the page's own search once the metadata is in, so a cold first query
   still ends up showing results instead of "no results". */
function nudge(q){
if(NUDGED[q])return;
NUDGED[q]=true;
try{
var inp=document.querySelector('.searchfields input, input[type=search], .searchFields input');
if(!inp||inp.value!==q)return;
setTimeout(function(){
try{
inp.dispatchEvent(new Event('input',{bubbles:true}));
}catch(e){}
},30);
}catch(e){}
}
function mergeBody(text,url,ids){
var d;
try{d=JSON.parse(text);}catch(e){return null;}
if(!d)return null;
var key=(d.SearchHints instanceof Array)?'SearchHints'
       :((d.Items instanceof Array)?'Items':'');
if(!key)return null;
var have={},i,list=d[key];
for(i=0;i<list.length;i++)have[String(list[i].Id||list[i].ItemId||'').toLowerCase()]=1;
var add=[],cache=cachedFor(ids);
for(i=0;i<cache.length;i++)if(!have[String(cache[i].Id).toLowerCase()])add.push(cache[i]);
if(!add.length)return null;
/* Only offer a film to the request that asked for films: a search fires one
   call per section, and /Persons and /Artists must be left alone. */
/* sf-types-repeated: Jellyfin REPEATS this parameter rather than comma-joining
   it -- includeItemTypes=Movie&includeItemTypes=Series&... -- exactly as it does
   with `fields`. Reading only the first match (which is what an .exec() without
   /g gives you) collapsed the whole request to "Movie", so series were filtered
   out of the one request that actually feeds the "Serien" section and only ever
   surfaced through the untyped sweep, i.e. under a "Videos" heading. Collect
   every occurrence, and split on commas too in case a caller joins them. */
var types=[];
try{
var _re=/[?&]includeItemTypes=([^&]*)/gi,_m;
while((_m=_re.exec(url))!==null){
types=types.concat(decodeURIComponent(_m[1].replace(/\+/g,' ')).toLowerCase().split(','));
}
types=types.map(function(x){return x.replace(/^ +| +$/g,'');}).filter(Boolean);
}catch(e){types=[];}
if(/\/Persons|\/Artists/i.test(url))return null;
/* sf-merge-typed-only: merge ONLY into a request that names the types it
   wants. A search also fires an untyped sweep (isMissing=false&limit=800),
   and adding films to THAT grew a second "Videos" shelf repeating everything
   already under "Filme" -- a section the same search in English does not
   produce. If a request did not ask for a type, this is not its section. */
if(types.length){
add=add.filter(function(x){return types.indexOf(String(x.Type||'').toLowerCase())>=0;});
}else{
/* sf-untyped-nonmovie: the search fires ONE untyped /Items sweep plus a typed
   includeItemTypes=Movie one. Films therefore have a request of their own, and
   adding them to the untyped sweep as well made the page grow a second "Videos"
   shelf duplicating "Filme".

   Series have no typed request at all -- "Serien" is filled from that same
   untyped sweep -- so refusing every untyped request (the first cut of the
   duplicate fix) silently un-translated search for every TV show while movies
   went on working. The stress test caught it: 30/30 movie queries passed and
   almost every series query failed.

   So: untyped requests take everything EXCEPT films, which are already covered
   by their own typed request. */
/* Now that the typed request is parsed correctly it covers films AND series,
   so the untyped sweep is pure duplication -- merging into it is what produced
   the phantom "Videos" shelf. Leave it alone. */
return null;
}
if(!add.length)return null;
var rows=(key==='SearchHints')?add.map(toHint):add;
d[key]=rows.concat(list);
if(typeof d.TotalRecordCount==='number')d.TotalRecordCount+=rows.length;
try{return JSON.stringify(d);}catch(e){return null;}
}
function install(){
var XP=window.XMLHttpRequest&&window.XMLHttpRequest.prototype;
if(!XP||XP.__sfSearchI18n)return;
var oOpen=XP.open,oSend=XP.send;
XP.open=function(m,u){try{this.__sfUrl=String(u||'');}catch(e){}
return oOpen.apply(this,arguments);};
XP.send=function(){
var self=this,url=self.__sfUrl||'';
if(/[?&]searchTerm=/i.test(url)){
var L=lang();
if(L){
var q='';
try{q=decodeURIComponent(((/[?&]searchTerm=([^&]*)/i.exec(url)||[])[1]||'').replace(/\+/g,' '));}catch(e){}
var ids=q?matchIds(q,L):[];
if(ids.length){
self.__sfIds=ids;
warm(q,ids);            /* runs alongside the search, not after it */
self.addEventListener('readystatechange',function(){
if(self.readyState!==4||self.status<200||self.status>=300)return;
try{
var body=mergeBody(self.responseText,url,ids);
if(!body)return;
Object.defineProperty(self,'responseText',{configurable:true,get:function(){return body;}});
Object.defineProperty(self,'response',{configurable:true,get:function(){return body;}});
}catch(e){}
});
}
}
}
return oSend.apply(this,arguments);
};
XP.__sfSearchI18n=1;
}
install();
setInterval(install,1000);
})();</script>'''
