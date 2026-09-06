"""jfblocks/music.py -- payload constants lifted out of jf_patch.py.

Each constant's source text (and its comments) is byte-identical to the
monolith; only its location changed. 8 constants.
"""

__all__ = [
    'MUSICPL_MARKER',
    'MUSICPL_SCRIPT',
    'MUSICTABS_MARKER',
    'MUSICTABS_STYLE',
    'MUSICARTISTLBL_MARKER',
    'MUSICARTISTLBL_SCRIPT',
    'ALBUMBLURB_MARKER',
    'ALBUMBLURB_SCRIPT',
]


MUSICPL_MARKER = 'jf-music-playlists'
MUSICPL_SCRIPT = (
    '<script>(function(){ /* jf-music-playlists */'
    # /Artists and /Artists/AlbumArtists are ALSO sent with no ParentId, so they
    # return every artist on the server -- audiobook authors (Andy Weir,
    # J.K. Rowling, Matt Dinniman) showed up under Music. Scoped: 60 artists,
    # unscoped: 63 including those three. Same bug shape as the playlists one.
    # The library id is re-read from topParentId in the hash whenever Jellyfin
    # supplies it (drawer navigation does), so this self-heals if the Music
    # library is ever recreated; the literal is only the cold-start fallback.
    'var MUSICID=(window.SF_CONFIG&&window.SF_CONFIG.musicLibraryId)||"";'
    'function musicId(){'
    'try{var m=(location.hash||"").match(/topParentId=([0-9a-f]{32})/i);'
    'if(m)MUSICID=m[1];}catch(e){}'
    'return MUSICID;'
    '}'
    'function fix(u){'
    'try{'
    'var s=String(u),h=location.hash||"";'
    'if(h.indexOf("#/music")!==0)return u;'
    'if(s.indexOf("IncludeItemTypes=Playlist")!==-1&&s.indexOf("MediaTypes=")===-1){'
    'return s+(s.indexOf("?")===-1?"?":"&")+"MediaTypes=Audio";'
    '}'
    'if(s.indexOf("/Artists")!==-1&&s.indexOf("ParentId=")===-1&&musicId()){'
    'return s+(s.indexOf("?")===-1?"?":"&")+"ParentId="+musicId();'
    '}'
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

# --- Trim the Music library tab bar (2026-08-04).
# Measured contents of the Music library before deciding:
#   Albums 122 | Songs 1660 | Album artists 60 | Artists 169 | Genres 109 | audio playlists 0
# Hidden:
#  * Artists (index 3) - 169 vs 60 album artists; the extra ~109 are featured/guest
#    credits with a track or two each. "Album artists" is the browse that matches how
#    a personal collection is actually organised.
#  * Genres (index 6) - unusable, the tags are malformed. Real examples: one "genre" is
#    the whole semicolon-joined string "Alternative R&B; Baroque Pop; Contemporary R&B;
#    Dream Pop; Indie Pop; ... Trip Hop", plus near-duplicates ("Alternative Rock" vs
#    "Alternative-Rock") and stray non-English entries. 109 genres across 122 albums.
# KEPT Playlists (index 4) even though there are 0 audio playlists today - it is the
# only route to music playlists once any are created. Hiding it would strand them.
# Scoped with body:has(#musicRecommendedPage:not(.hide)) because .emby-tabs-slider is
# SHARED with the Movies/Shows pages, which use the same data-index values.
# Only the button is hidden - #/music?tab=3 still works if ever needed.
MUSICTABS_MARKER = 'jf-music-tabs'
MUSICTABS_STYLE = ('<style id="jf-music-tabs">'
                   'body:has(#musicRecommendedPage:not(.hide)) .emby-tabs-slider > [data-index="3"],'
                   'body:has(#musicRecommendedPage:not(.hide)) .emby-tabs-slider > [data-index="6"]'
                   '{display:none!important;}'
                   # sf-mtabs-gate (2026-08-28). The music page showed JELLYFIN'S OWN tab
                   # bar before ours replaced it. Measured cold on a phone:
                   #   t=1207ms  Albums* | Suggestions | Artists | Playlists | Songs   (stock)
                   #   t=1351ms  Library | Home* | New | Radio                          (ours)
                   # ~150ms of the stock five-tab bar, with the wrong tab lit, every load.
                   # Hold the strip until sfMusicTabs has claimed it. The gate keys off
                   # `data-sf-navinit`, the attribute that builder already stamps on the bar
                   # -- NOT the labels: those are translated, and matching English strings
                   # is what once removed every audiobook control for the de/zh profiles.
                   # Same 12s failsafe keyframes as the header gate, so a build that never
                   # runs still shows its tabs rather than hiding them for the session.
                   'body:has(#musicRecommendedPage:not(.hide)) .emby-tabs-slider:not([data-sf-navinit])'
                   '{opacity:0;animation:sf-hdr-failsafe .3s ease 12s both;}'
                   'body:has(#musicRecommendedPage:not(.hide)) .emby-tabs-slider'
                   '{transition:opacity .18s ease;}'
                   # sf-nav-swap (2026-08-28). .emby-tabs-slider is SHARED across pages,
                   # so during a route change it briefly carries the OLD page's buttons
                   # next to the new ones. Measured on a phone, settled app, real
                   # navigation:
                   #   home->music  t=185ms  Library* | Live TV | Sports | Home | New | Radio
                   #   music->home  t= 92ms  Library* | Live TV | Sports | Home* | New | My Stuff
                   # Six tabs, two of them lit. ~100-200ms every time you navigate --
                   # which is far more often than anyone reloads.
                   # Hide the strip across the swap rather than trying to sequence two
                   # pages' tab builders against each other.
                   # sf-navkeep (2026-08-29). The blanking above was written for the SHARED
                   # library strip, but .jf-mu-mainbar's inner element is an
                   # .emby-tabs-slider too, so the MAIN pill row was blanked on every
                   # navigation as well: measured 32 frames at opacity 0 (~500ms) then a
                   # 180ms fade back in, every single time you change page. That is the
                   # "nav bar disappears and reappears" report.
                   # A strip only needs hiding while it holds a MIX of two pages' tabs.
                   # Our pills all carry data-sf-nav (stamped on the native strip too, so
                   # this is locale-independent); a page's own tabs never do. So "every
                   # visible button carries data-sf-nav" == a clean main-pill row, which
                   # is true for our bar AND for the native strip once it has settled,
                   # and false for exactly the mixed state this rule exists to hide.
                   'html.sf-nav-swap .emby-tabs-slider:not([data-sf-navkeep]){opacity:0!important;}'
                   # sf-navswap-sub: same treatment for the Live TV sub-pills;
                   # sfNavSwap's mark() stamps them with the same keep decision.
                   'html.sf-nav-swap .jf-ltv-sub:not([data-sf-navkeep]){opacity:0!important;}'
                   '.emby-tabs-slider:not([data-sf-navkeep]){transition:opacity .15s ease;}'
                   # never animate the main row -- the admin asked for it to just stay put
                   '.emby-tabs-slider[data-sf-navkeep]{transition:none!important;opacity:1!important;}'
                   '</style>')

# --- Rename "Album artists" -> "Artists" in the Music tab bar (2026-08-04).
# jf-music-tabs hides the real Artists tab (169 entries, mostly featured credits),
# so "Album artists" is now the only artist browse and the qualifier is noise.
# Write to the inner .emby-button-foreground div, NOT the button: the button is
# <button><div class="emby-button-foreground">Album artists</div></button> and
# setting textContent on the button would destroy that wrapper and its styling.
# Scoped to the music page because .emby-tabs-slider is shared with Movies/Shows.
# The `!==` guard makes the MutationObserver self-terminating: our own write fires
# the observer once more, finds the text already correct, and stops.
MUSICARTISTLBL_MARKER = 'jf-music-artist-label'
MUSICARTISTLBL_SCRIPT = r'''<script>(function(){
/* jf-music-artist-label */
function ren(){
try{
if(!document.querySelector('#musicRecommendedPage:not(.hide)'))return;
var el=document.querySelector('.emby-tabs-slider > [data-index="2"] .emby-button-foreground');
if(el&&el.textContent!=='Artists'){el.textContent='Artists';}
}catch(e){}
}
new MutationObserver(ren).observe(document.body,{childList:true,subtree:true});
setInterval(ren,1500);ren();
})();</script>'''


# --- sf-alb: the album stage (2026-08-21) ------------------------------------
# The album page was the weakest surface in the whole app. Measured on a 412px
# phone: a 567px artist BACKDROP filling the screen, the album title rendered at
# 23px underneath it, and the album COVER not shown at all. Both reference apps
# lead an album with its square artwork -- it is how you recognise a record.
#
# So: cover as the hero, its own blur as the ambient ground behind it, a real
# title, the artist as a link, the metadata as quiet chips, and Play/Shuffle as
# the two things you actually came to do.
#
# Speed rules this file, so:
#   * NO new network requests -- the item is fetched once and cached, and the
#     cover URL resolves to the same image the grid already loaded, so it comes
#     from cache;
#   * the hero's height is reserved before the artwork decodes, because a late
#     hero is exactly what made taps miss earlier (see sf-heroslot);
#   * Play and Shuffle PROXY Jellyfin's own buttons rather than reimplementing
#     playback, so there is one code path and it is the tested one.
ALBUMBLURB_MARKER = 'sf-alb-stage'
ALBUMBLURB_SCRIPT = r"""<script>(function(){ /* sf-alb-stage */
if(window.__sfAlbStage)return;
window.__sfAlbStage=1;
var itemCache={};
function hashId(){
var m=/[#&?]id=([0-9a-fA-F-]{32,36})/.exec(location.hash||'');
return m?m[1].replace(/-/g,'').toLowerCase():'';
}
function pageEl(){
var p=document.querySelectorAll('.itemDetailPage'),i;
for(i=0;i<p.length;i++){if(!p[i].classList.contains('hide')&&p[i].offsetParent!==null)return p[i];}
return null;
}
function itemOf(id,cb){
if(itemCache[id]!==undefined){cb(itemCache[id]);return;}
var c=window.ApiClient;
if(!c||!c.getItem||!c.getCurrentUserId){cb(null);return;}
itemCache[id]=null;
c.getItem(c.getCurrentUserId(),id).then(function(it){
itemCache[id]=it||null;cb(itemCache[id]);
}).catch(function(){cb(null);});
}
function fmtRun(ticks){
if(!ticks)return '';
var s=Math.round(ticks/10000000),h=Math.floor(s/3600),m=Math.round((s%3600)/60);
return h?(h+'h '+m+'m'):(m+'m');
}
/* Click Jellyfin's own control: one playback path, and it is the tested one. */
function hit(p,sel){
var b=p.querySelectorAll(sel),i;
for(i=0;i<b.length;i++){if(b[i].getClientRects().length||b[i].offsetParent!==null){b[i].click();return true;}}
if(b.length){b[0].click();return true;}
return false;
}
function build(p,id,it){
var c=window.ApiClient;
var art='';
try{art=c.getImageUrl(id,{type:'Primary',maxWidth:640,tag:(it.ImageTags||{}).Primary});}catch(e){}
var stage=document.createElement('div');
stage.className='sf-alb-hero';
stage.setAttribute('data-sf-id',id);

var bg=document.createElement('div');
bg.className='sf-alb-bg';
if(art)bg.style.backgroundImage='url("'+art+'")';
stage.appendChild(bg);
var scrim=document.createElement('div');
scrim.className='sf-alb-scrim';
stage.appendChild(scrim);

var inner=document.createElement('div');
inner.className='sf-alb-in';

var cover=document.createElement('div');
cover.className='sf-alb-art';
if(art)cover.style.backgroundImage='url("'+art+'")';
inner.appendChild(cover);

var meta=document.createElement('div');
meta.className='sf-alb-meta';
var h1=document.createElement('div');
h1.className='sf-alb-title';
h1.textContent=it.Name||'';
meta.appendChild(h1);

var who=(it.AlbumArtists&&it.AlbumArtists[0])||null;
var artist=document.createElement('button');
artist.type='button';
artist.className='sf-alb-artist';
artist.textContent=(who&&who.Name)||it.AlbumArtist||'';
if(who&&who.Id){
artist.addEventListener('click',function(e){
e.preventDefault();e.stopPropagation();
location.hash='#/details?id='+who.Id;
});
}else{artist.disabled=true;}
if(artist.textContent&&!isArtist)meta.appendChild(artist);

var isBook=!!it&&it.Type==='AudioBook';
var isArtist=!!it&&it.Type==='MusicArtist';
var isList=!!it&&it.Type==='Playlist';
if(isBook)stage.classList.add('sf-alb-book');
if(isArtist)stage.classList.add('sf-alb-artistpg');
if(isList)stage.classList.add('sf-alb-listpg');
var chips=document.createElement('div');
chips.className='sf-alb-chips';
var bits=[];
if(isBook){
var nar=[],pp=it.People||[],pi;
for(pi=0;pi<pp.length;pi++)if(pp[pi].Role==='Narrator')nar.push(pp[pi].Name);
if(nar.length)artist.textContent=(artist.textContent||'')+'  \u00b7  '+nar[0];
if(it.CommunityRating)bits.push('\u2605 '+it.CommunityRating);
}
if(isArtist){
/* an artist has no track count worth showing; its genres say more.
   Deduped: Jellyfin returns Adele's genres as ["Soul","Soul"], which rendered
   the same chip twice. */
var gg=(it.Genres||[]),gi,seen={},got=0;
for(gi=0;gi<gg.length&&got<2;gi++){
var g=String(gg[gi]||'').trim();
if(!g||seen[g.toLowerCase()])continue;
seen[g.toLowerCase()]=1;bits.push(g);got++;
}
}else if(it.ChildCount&&!isBook){
bits.push(it.ChildCount+(it.ChildCount===1?' track':' tracks'));
}
var run=fmtRun(it.RunTimeTicks); if(run)bits.push(run);
if(it.ProductionYear)bits.push(String(it.ProductionYear));
/* A playlist's genre is just whatever its first track happened to be
   ("Experimental" on a 2000s mix), so it is noise rather than information. */
if(!isList&&!isArtist&&(it.Genres||[]).length)bits.push(it.Genres[0]);
for(var bi=0;bi<bits.length;bi++){
var ch=document.createElement('span');
ch.className='sf-alb-chip';
ch.textContent=bits[bi];
chips.appendChild(ch);
}
if(bits.length)meta.appendChild(chips);

var acts=document.createElement('div');
acts.className='sf-alb-acts';
var play=document.createElement('button');
play.type='button';
play.className='sf-alb-play';
play.innerHTML='<span class="material-icons" aria-hidden="true">play_arrow</span><span class="sf-alb-playlab">Play</span>';
/* Mirror Jellyfin's own label so a part-finished book reads "Resume" -- and read
   it from the DOM rather than hardcoding, so it stays translated. */
(function(){
try{
var nat=p.querySelector('.btnResume:not(.hide)')||p.querySelector('.btnPlay:not(.hide)');
var lab=nat&&(nat.querySelector('.button-text,span:not(.material-icons)')||{}).textContent;
lab=(lab||'').trim();
if(lab)play.querySelector('.sf-alb-playlab').textContent=lab;
}catch(e){}
})();
play.addEventListener('click',function(e){
e.preventDefault();e.stopPropagation();
if(!hit(p,'.btnResume:not(.hide)'))hit(p,'.btnPlay:not(.hide),.btnPlay');
});
acts.appendChild(play);
var shuf=document.createElement('button');
shuf.type='button';
shuf.className='sf-alb-shuffle';
shuf.innerHTML='<span class="material-icons" aria-hidden="true">shuffle</span><span class="sf-alb-shuflab">Shuffle</span>';
shuf.addEventListener('click',function(e){
e.preventDefault();e.stopPropagation();
if(!hit(p,'.btnShuffle,.btnInstantMix'))hit(p,'.btnPlay:not(.hide),.btnPlay');
});
/* Shuffle means nothing for a single 13-hour file; it means a lot for an
   artist's whole catalogue and for a 150-track playlist. */
if(!isBook)acts.appendChild(shuf);
meta.appendChild(acts);

/* sf-alb-bookmeta (2026-08-28). Two things an audiobook page has to answer that
   ours did not: how far in am I, and what is this book about.

   The synopsis was the bigger miss. sf-atv sets
   `#itemDetailPage.sf-atv .detailSectionContent{display:none}` across every
   detail page, so all 36 backfilled descriptions rendered at height 0 and the
   band under the hero was simply blank -- measured: .detailSectionContent
   display:none, h=0, while .sf-chapters sat 875px down, below the fold. Rather
   than fight that rule (see the album track list, where CSS lost to it twice and
   only JS won), render the overview INTO the stage, where the space beside the
   cover is already empty.

   Both come off the item we already fetched -- no extra request. */
if(isBook){
var ud=it.UserData||{};
var pos=ud.PlaybackPositionTicks||0,tot=it.RunTimeTicks||0;
if(tot>0&&pos>0&&pos<tot){
var pct=pos/tot*100;
if(pct<0)pct=0;if(pct>100)pct=100;
var prog=document.createElement('div');
prog.className='sf-alb-prog';
var bar=document.createElement('div');
bar.className='sf-alb-progbar';
var fill=document.createElement('span');
fill.style.width=pct.toFixed(1)+'%';
bar.appendChild(fill);
var plab=document.createElement('div');
plab.className='sf-alb-proglab';
/* "left" is what Audible puts here -- it is the number that decides whether you
   pick the book up tonight. Percentage rides along for orientation. */
plab.textContent=fmtRun(tot-pos)+' left  \u00b7  '+Math.round(pct)+'%';
prog.appendChild(bar);prog.appendChild(plab);
meta.appendChild(prog);
}
var ov=(it.Overview||'').trim();
if(ov){
var dsc=document.createElement('p');
dsc.className='sf-alb-desc';
dsc.textContent=ov;
/* clamped to 3 lines; tap to open. No chevron: the clamp itself reads as
   "there is more", and a control here would compete with Play. */
dsc.addEventListener('click',function(){this.classList.toggle('sf-alb-desc-open');});
meta.appendChild(dsc);
}
}

inner.appendChild(meta);
stage.appendChild(inner);

var host=p.querySelector('.detailPageWrapperContainer')||p;
host.insertBefore(stage,host.firstChild);
p.classList.add('sf-alb-on');
/* the page needs its own marker so CSS can lay an artist's ALBUMS out as a
   shelf rather than the one-per-row list Jellyfin gives that section */
p.classList.toggle('sf-alb-on-artist',isArtist);
showTracks(p);
}
/* THE TRACK LIST. sf-atv hides .detailSectionContent across every detail page,
   which on an album means its songs: 15 track rows in the DOM, none visible.
   An album page you cannot pick a song from is not an album page -- and this was
   true long before the restyle.

   Done in JS, not CSS. Two attempts at a stylesheet override lost on
   specificity: sf-atv's rule is `#itemDetailPage.sf-atv .detailPagePrimaryContent`
   at (1,2,0), and even an ID-matched override with !important did not take. An
   inline important declaration on the element ends the argument.

   Jellyfin's own rows are unhidden rather than reimplemented, so tapping a track
   still runs its real, tested playback path. */
/* sf-trace (2026-08-23, TEMPORARY): the playlist's 150 tracks intermittently
   stay hidden -- 4 of 9 stress runs, but 0 of 12 isolated reproductions, and NOT
   correlated with load (failed at 3.27, passed at 6.02). Instrument the unhide
   path so the next full suite captures the state at the moment it happens
   instead of guessing. Ring-buffered at 240 entries. */
function sfTrace(ev,d){
try{var T=window.__sfTrace||(window.__sfTrace=[]);
T.push({t:Date.now(),ev:ev,d:d});
if(T.length>240)T.shift();}catch(e){}
}
function showTracks(p){
try{
var pc=p.querySelector('.detailPagePrimaryContent');
if(!pc){sfTrace('showTracks:no-primary-content',{});return;}
/* Rows for an album or playlist; CARDS for an artist, whose content is its
   Albums shelf. Measured before this: an artist page hid a 2-album shelf, and a
   playlist hid all 150 of its tracks. */
var first=pc.querySelector('.listItem')||pc.querySelector('.card');
sfTrace('showTracks',{first:!!first,
  rows:pc.querySelectorAll('.listItem').length,
  cards:pc.querySelectorAll('.card').length,
  pageVisible:p.getClientRects().length>0,
  pcVisible:pc.getClientRects().length>0});
if(!first){
/* sf-pc-deadlock (2026-08-23). branding.xml hides .detailPagePrimaryContent with
   display:none, and this function was the only thing that ever unhid it -- but
   only once rows existed. Jellyfin populates that list LAZILY, and a display:none
   container is never measured and never intersects, so it is never populated.
   Rows never arrive -> we never unhide -> rows never arrive. A self-sustaining
   deadlock, which is why the playlist showed 0 of its 150 tracks in 4 of 9 stress
   runs while being unreproducible in 12 isolated attempts: it depends on whether
   Jellyfin got to render eagerly before our CSS applied.
   Captured live: {rows:0, cards:0, pcDisp:'none'} on the visible page, on EVERY
   tick, while an older cached instance of the same page sat at 'block'.
   Unhide the (empty) container so the lazy renderer can see it. An empty
   container shows nothing, so there is no visual cost. */
if(pc.getAttribute('data-sf-pcopen')!=='1'){
pc.setAttribute('data-sf-pcopen','1');
pc.style.setProperty('display','block','important');
sfTrace('showTracks:opened-empty-container',{});
}
return;
}
/* Unhide ONLY the ancestors of the real rows. A blanket pass over every
   .detailSection also revealed Jellyfin's empty "Schedule" and "Next Up"
   sections -- both carry its own `hide` class, and forcing display:block
   overrode that, putting a stray "Schedule" heading above the songs. */
var artistGrid=p.classList.contains('sf-alb-on-artist');
var node=first.parentElement,i;
while(node&&node!==pc.parentElement){
if(node.getAttribute('data-sf-alb')!=='1'){
node.setAttribute('data-sf-alb','1');
/* An artist's album shelf wants to be a GRID. This inline declaration was
   overriding the stylesheet's display:grid -- inline !important beats a rule
   !important, so the CSS silently lost to our own JS and the albums stayed
   stacked one per row. Set the right value here instead of fighting it. */
if(artistGrid&&node.classList.contains('itemsContainer'))
node.style.setProperty('display','grid','important');
else
node.style.setProperty('display','block','important');
}
node=node.parentElement;
}
/* Its own flag: the ancestor walk above already marks pc, so a shared guard
   silently skipped this and left a 110px hole between the artwork and track 1. */
if(pc.getAttribute('data-sf-albm')!=='1'){
pc.setAttribute('data-sf-albm','1');
pc.style.setProperty('display','block','important');
/* sf-atv reserves this margin to clear the backdrop the stage replaced */
pc.style.setProperty('margin-top','0','important');
}
var rows=pc.querySelectorAll('.listItem');
for(i=0;i<rows.length;i++){
if(rows[i].getAttribute('data-sf-alb')==='1')continue;
rows[i].setAttribute('data-sf-alb','1');
rows[i].style.setProperty('display','flex','important');
}
}catch(e){}
}
function tick(){
try{
if((location.hash||'').indexOf('#/details')!==0){
var stray=document.querySelectorAll('.sf-alb-hero'),k;
for(k=0;k<stray.length;k++)if(stray[k].parentNode)stray[k].parentNode.removeChild(stray[k]);
return;
}
var p=pageEl();if(!p)return;
var id=hashId();if(!id)return;
itemOf(id,function(it){
/* Jellyfin keeps one cached page instance per URL, so sweep every instance
   whose id is not the one on screen -- not just the visible page. */
var all=document.querySelectorAll('.sf-alb-hero'),si;
for(si=0;si<all.length;si++){
if(all[si].getAttribute('data-sf-id')!==id&&all[si].parentNode)
all[si].parentNode.removeChild(all[si]);
}
var isAlbum=!!it&&(it.Type==='MusicAlbum'||it.Type==='AudioBook'
||it.Type==='MusicArtist'||it.Type==='Playlist');
if(!isAlbum){
p.classList.remove('sf-alb-on');
var prevx=p.querySelector('.sf-alb-hero');
if(prevx&&prevx.parentNode)prevx.parentNode.removeChild(prevx);
sweepBlurb(p,id,null);
return;
}
var prev=p.querySelector('.sf-alb-hero');
sfTrace('tick',{id:id,type:it&&it.Type,hero:!!prev,
  pageVisible:p.getClientRects().length>0,
  pages:document.querySelectorAll('.itemDetailPage').length,
  rowsInPage:p.querySelectorAll('.listItem').length});
if(!prev)build(p,id,it);
else {p.classList.add('sf-alb-on');showTracks(p);}
sweepBlurb(p,id,it);
});
}catch(e){}
}
/* the description, read out of the node our own sf-atv styling hides */
function sweepBlurb(p,id,it){
var all=document.querySelectorAll('.sf-albumblurb'),si;
for(si=0;si<all.length;si++){
if(all[si].getAttribute('data-sf-id')!==id&&all[si].parentNode)
all[si].parentNode.removeChild(all[si]);
}
var prev=p.querySelector('.sf-albumblurb');
if(!it){if(prev&&prev.parentNode)prev.parentNode.removeChild(prev);return;}
if(p.querySelector('.sf-chapters'))return;
var src=p.querySelector('.overview');
var txt=src?(src.textContent||'').trim():'';
if(!txt){if(prev&&prev.parentNode)prev.parentNode.removeChild(prev);return;}
if(prev&&prev.getAttribute('data-sf-id')===id)return;
if(prev&&prev.parentNode)prev.parentNode.removeChild(prev);
var host=p.querySelector('.detailPageContent')||p.querySelector('.detailPageWrapperContainer');
if(!host)return;
var sy=document.createElement('div');
sy.className='verticalSection sf-synopsis sf-albumblurb';
sy.setAttribute('data-sf-id',id);
sy.style.order='-1';
var body=document.createElement('div');
body.className='sf-syn-text';
body.textContent=txt;
sy.appendChild(body);
if(txt.length>320){
var more=document.createElement('button');
more.type='button';
more.className='sf-syn-more';
more.textContent='More';
more.addEventListener('click',function(e){
e.preventDefault();e.stopPropagation();
var open=sy.classList.toggle('sf-syn-open');
more.textContent=open?'Less':'More';
});
sy.appendChild(more);
}else{sy.classList.add('sf-syn-open');}
var kids=host.children,i,ref=null;
for(i=0;i<kids.length;i++){if(kids[i].getClientRects().length){ref=kids[i];break;}}
if(ref)host.insertBefore(sy,ref); else host.appendChild(sy);
}
setInterval(tick,700);
window.addEventListener('hashchange',function(){setTimeout(tick,300);});
})();</script>"""
