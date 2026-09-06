"""jfblocks/audiobook.py -- payload constants lifted out of jf_patch.py.

Each constant's source text (and its comments) is byte-identical to the
monolith; only its location changed. 8 constants.
"""

__all__ = [
    'NOCHAPTERS_MARKER',
    'NOCHAPTERS_STYLE',
    'CHAPTERS_MARKER',
    'CHAPTERS_SCRIPT',
    'ABPLAYER_MARKER',
    'ABPLAYER_SCRIPT',
    'READALONG_MARKER',
    'READALONG_SCRIPT',
]


NOCHAPTERS_MARKER = 'jf-no-chapters'
NOCHAPTERS_STYLE = ('<style id="jf-no-chapters">'
                    # detail page: the "Scenes" card row
                    '#scenesCollapsible{display:none!important;}'
                    # video player: the chapter tick marks on the seek bar.
                    # These are built from chapter markerInfo -- one
                    # <span class="sliderMarker"> per chapter inside
                    # .sliderMarkerContainer. Hiding the container leaves the
                    # seek bar itself untouched.
                    '.sliderMarkerContainer{display:none!important;}'
                    # seek-bar HOVER bubble. Structure is:
                    #   .chapterThumbContainer > img.chapterThumb
                    #                          + .chapterThumbTextContainer >
                    #                              .chapterThumbText-dim  (chapter NAME)
                    #                              h2.chapterThumbText    (TIMESTAMP)
                    # Drop the thumbnail and the chapter name, keep the timestamp so
                    # scrubbing still tells you where you are.
                    '.chapterThumb{display:none!important;}'
                    # sf-thumb-wrapper (2026-08-28): ...and the WRAPPER around
                    # it. The JS gives that div an INLINE width/height of the
                    # trickplay tile (e.g. 320x180), so hiding only the image
                    # left a ~320x180 INVISIBLE box inside the bubble.
                    # .sliderBubble is centred on the pointer via
                    # translate3d(-50%,-120%,0), so the BOX centred correctly
                    # while the timestamp -- pushed to its left edge and below
                    # the dead wrapper -- drew ~128-160px LEFT of the cursor and
                    # far too high. Reported as a Brave/Safari bug; it was not.
                    # It only ever hit items WITH trickplay data: without it,
                    # Jellyfin falls back to <h1 class=sliderBubbleText>, which
                    # this markup never touches -- which is why a movie with no
                    # trickplay looked fine in Chrome and an episode with it did
                    # not. Measured in Chromium AND WebKit via Playwright:
                    # glyph offset -128px before, 0px after, identical in both.
                    '.chapterThumbWrapper{display:none!important;}'
                    '.chapterThumbText-dim{display:none!important;}'
                    '.chapterThumbContainer{box-shadow:none!important;flex-grow:0!important;}'
                    '.chapterThumbTextContainer{position:static!important;}'
                    # player transport: skip-to-chapter buttons either side of
                    # play/pause. Verified live in the OSD -- they stay
                    # inline-flex even with every other chapter surface hidden.
                    # (An existing html.sf-live rule hides these for Live TV only,
                    # so this general rule is still needed.)
                    '.btnPreviousChapter,.btnNextChapter{display:none!important;}'
                    '</style>')


CHAPTERS_MARKER = 'sf-audiobook-chapters'
CHAPTERS_SCRIPT = """<script>(function(){ /* sf-audiobook-chapters */
var sfChCache={},sfChFor='';
/* sf-ch-sameorigin (2026-08-21): the chapter index, served from Jellyfin's own
   web root. It used to come only from requestbridge on :8099, which the admin's
   phones cannot reach -- so the chapter list vanished and chapter-skip did
   nothing, while the buttons themselves stayed on screen because they are built
   blind. One 56KB file covers every book; fetched once, then cached. */
var SF_CH_ALL=null,SF_CH_BUSY=false,SF_CH_WAIT=[];
function sfChSameOrigin(id,cb){
var key=String(id||'').replace(/-/g,'').toLowerCase();
function give(){
if(!SF_CH_ALL){cb(null);return;}
var hit=SF_CH_ALL[key];
cb(hit&&hit.c&&hit.c.length?hit.c:null);
}
if(SF_CH_ALL!==null){give();return;}
SF_CH_WAIT.push(give);
if(SF_CH_BUSY)return;
SF_CH_BUSY=true;
fetch('readalong/chapters.json',{credentials:'same-origin'})
.then(function(r){return r.ok?r.json():null;})
.then(function(d){
var out={},items=(d&&d.items)||{},k;
for(k in items){if(items.hasOwnProperty(k))out[String(k).replace(/-/g,'').toLowerCase()]=items[k];}
SF_CH_ALL=out;
}).catch(function(){SF_CH_ALL=false;})
.then(function(){
SF_CH_BUSY=false;
var w=SF_CH_WAIT;SF_CH_WAIT=[];
for(var i=0;i<w.length;i++){try{w[i]();}catch(e){}}
});
}
function sfChBase(){
/* Same rule as the request UI: on :8096 the browser is on the LAN talking to
   Jellyfin directly, where nginx's /requestbridge/ path does not exist. */
return (location.port==='8096')
?(location.protocol+'//'+location.hostname+':8099')
:(location.origin+'/requestbridge');
}
function sfChToken(){
try{if(window.ApiClient&&ApiClient.accessToken)return ApiClient.accessToken();}catch(e){}
try{var c=JSON.parse(localStorage.getItem('jellyfin_credentials')||'{}');
return (c.Servers&&c.Servers[0]&&c.Servers[0].AccessToken)||'';}catch(e){return '';}
}
function sfChUser(){
try{if(window.ApiClient&&ApiClient.getCurrentUserId)return ApiClient.getCurrentUserId();}catch(e){}
try{var c=JSON.parse(localStorage.getItem('jellyfin_credentials')||'{}');
return (c.Servers&&c.Servers[0]&&c.Servers[0].UserId)||'';}catch(e){return '';}
}
function sfChHashId(){
var h=location.hash||'';
if(h.indexOf('details')<0)return '';
var i=h.indexOf('id=');
if(i<0)return '';
var v=h.substr(i+3),j=v.indexOf('&');
if(j>=0)v=v.substr(0,j);
return v;
}
function sfChTime(sec){
sec=Math.max(0,Math.floor(sec));
var h=Math.floor(sec/3600),m=Math.floor((sec%3600)/60),s2=sec%60;
function p(n){return n<10?'0'+n:''+n;}
return h?(h+':'+p(m)+':'+p(s2)):(m+':'+p(s2));
}
/* The book currently loaded in the audio element, if it is this one. */
function sfChLiveAudio(id){
var a=document.querySelector('audio');
if(!a||!a.currentSrc)return null;
var bar=document.querySelector('.nowPlayingBar');
if(!bar)return null;
var link=bar.querySelector('a[href*="id="]');
if(link&&link.getAttribute('href').indexOf(id)>=0)return a;
return null;
}
function sfChSetResume(id,sec,done){
try{
var url=location.origin+'/UserItems/'+id+'/UserData?userId='+sfChUser();
fetch(url,{method:'POST',headers:{'Content-Type':'application/json','X-Emby-Token':sfChToken()},
body:JSON.stringify({PlaybackPositionTicks:Math.round(sec*10000000)})}).then(done,done);
}catch(e){done();}
}
function sfChJump(id,sec,row){
var a=sfChLiveAudio(id);
if(a){
try{
a.currentTime=sec;
if(a.paused&&a.play)a.play();
sfChMark(sec);
return;
}catch(e){}
}
if(row){row.classList.add('sf-ch-loading');setTimeout(function(){row.classList.remove('sf-ch-loading');},4000);}
sfChSetResume(id,sec,function(){
try{
if(typeof sfPlayItemViaProxy==='function')
sfPlayItemViaProxy(id,'AudioBook','Audio',false,'resume');
}catch(e){}
});
}
/* Highlight whichever chapter contains the given second. */
function sfChMark(sec){
var wrap=document.querySelector('.sf-chapters');
if(!wrap)return;
var rows=wrap.querySelectorAll('.sf-ch-row'),i,best=-1;
for(i=0;i<rows.length;i++){
if(parseFloat(rows[i].getAttribute('data-t'))<=sec+0.25)best=i;
}
for(i=0;i<rows.length;i++)rows[i].classList.toggle('sf-ch-now',i===best);
}
function sfChBuild(id,list,dur){
var page=(window.__jfView&&window.__jfView.itemPage&&window.__jfView.itemPage())||
document.querySelector('.itemDetailPage:not(.hide)');
if(!page)return false;
var host=page.querySelector('.detailPageContent')||page.querySelector('.detailPageWrapperContainer');
if(!host)return false;
var old=page.querySelector('.sf-chapters');
if(old)old.parentNode.removeChild(old);
var sec=document.createElement('div');
sec.className='verticalSection sf-chapters';
sec.setAttribute('data-sf-id',id);
var head=document.createElement('div');
head.className='sectionTitleContainer';
head.innerHTML='<h2 class="sectionTitle">Chapters</h2>';
var count=document.createElement('span');
count.className='sf-ch-count';
count.textContent=list.length+' chapters';
head.appendChild(count);
sec.appendChild(head);
var box=document.createElement('div');
box.className='sf-ch-list';
var i;
for(i=0;i<list.length;i++){
(function(ch,idx){
var row=document.createElement('button');
row.type='button';
row.className='sf-ch-row';
row.setAttribute('data-t',String(ch.t));
var next=(idx+1<list.length)?list[idx+1].t:(dur||0);
var len=next>ch.t?sfChTime(next-ch.t):'';
row.innerHTML='<span class="sf-ch-num">'+(idx+1)+'</span>'
+'<span class="sf-ch-name"></span>'
+'<span class="sf-ch-len"></span>'
+'<span class="sf-ch-at"></span>';
row.querySelector('.sf-ch-name').textContent=ch.n||('Chapter '+(idx+1));
row.querySelector('.sf-ch-len').textContent=len;
row.querySelector('.sf-ch-at').textContent=sfChTime(ch.t);
row.addEventListener('click',function(e){
e.preventDefault();e.stopPropagation();
sfChJump(id,ch.t,row);
});
box.appendChild(row);
})(list[i],i);
}
sec.appendChild(box);
host.insertBefore(sec,host.firstChild);
/* sf-synopsis (2026-08-21). All 36 books now carry a real Audible synopsis, but
   none of it was reaching the screen: our own Apple-TV detail styling sets
   #itemDetailPage.sf-atv .detailSectionContent{display:none}, so Jellyfin's
   .overview node sits in the page with its full text (measured 1,419 chars on
   Dungeon Crawler Carl) and zero height.

   Rather than fight that rule -- or move a node Jellyfin owns, which broke the
   video player once before -- read the text out of the hidden node and render
   our own block above the chapter list. No extra request; the text is already
   in the DOM. Scoped to the audiobook path, so film and TV pages keep the clean
   poster-and-Play layout deliberately chosen for them. */
(function(){
var src=page.querySelector('.overview');
var txt=src?(src.textContent||'').trim():'';
var prev=page.querySelector('.sf-synopsis');
if(!txt){if(prev&&prev.parentNode)prev.parentNode.removeChild(prev);return;}
if(prev&&prev.parentNode)prev.parentNode.removeChild(prev);
var sy=document.createElement('div');
sy.className='verticalSection sf-synopsis';
sy.setAttribute('data-sf-id',id);
var body=document.createElement('div');
body.className='sf-syn-text';
body.textContent=txt;
sy.appendChild(body);
/* Long blurbs are clamped with a real control rather than cut off silently. */
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
}else{
sy.classList.add('sf-syn-open');
}
host.insertBefore(sy,host.firstChild);
})();
return true;
}
function sfChTick(){
try{
var id=sfChHashId();
if(!id){sfChFor='';return;}
var page=document.querySelector('.itemDetailPage:not(.hide)');
if(!page||page.offsetParent===null)return;
var have=page.querySelector('.sf-chapters');
if(have){
if(have.getAttribute('data-sf-id')===id){
/* already rendered for this item: just keep the highlight current */
var a=sfChLiveAudio(id);
if(a)sfChMark(a.currentTime||0);
return;
}
/* belongs to a previously viewed item -- the page instance is reused, so it
   would otherwise sit there under the wrong book (or a movie). */
have.parentNode.removeChild(have);
}
if(sfChFor===id&&sfChCache[id]===undefined)return;   /* fetch in flight */
if(sfChCache[id]!==undefined){
if(sfChCache[id]&&sfChCache[id].length)sfChBuild(id,sfChCache[id],sfChCache[id+':d']||0);
return;
}
sfChFor=id;
sfChSameOrigin(id,function(hit){
if(hit){sfChCache[id]=hit;sfChBuild(id,hit,0);return;}
fetch(sfChBase()+'/api/chapters?id='+encodeURIComponent(id),
{headers:{'x-jellyfin-token':sfChToken()}})
.then(function(r){return r.json();})
.then(function(d){
var list=(d&&d.chapters)||[];
sfChCache[id]=list;
if(list.length){sfChBuild(id,list,0);}
else{
var stale=document.querySelector('.sf-chapters');
if(stale&&stale.getAttribute('data-sf-id')!==id&&stale.parentNode)
stale.parentNode.removeChild(stale);
}
})
.catch(function(){sfChCache[id]=[];});
});
}catch(e){}
}
setInterval(sfChTick,600);
})();</script>"""


ABPLAYER_MARKER = 'sf-audiobook-player'
ABPLAYER_SCRIPT = """<script>(function(){ /* sf-audiobook-player */
var RATE_KEY='sf-ab-rate';
var RATES=[0.75,1,1.1,1.25,1.5,1.75,2,2.5,3];
var abType={},abChaps={},sleepAt=0,sleepChapter=false,fading=0,volSaved=-1;
var lastSeen={};

function el(){return document.querySelector('audio');}
function rate(){
var v=parseFloat(localStorage.getItem(RATE_KEY)||'1');
return (v>=0.5&&v<=3.5)?v:1;
}
function setRate(v){
try{localStorage.setItem(RATE_KEY,String(v));}catch(e){}
var a=el();
if(a)try{a.playbackRate=v;}catch(e){}
paint();
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
function userId(){
try{if(window.ApiClient&&ApiClient.getCurrentUserId)return ApiClient.getCurrentUserId();}catch(e){}
try{var c=JSON.parse(localStorage.getItem('jellyfin_credentials')||'{}');
return (c.Servers&&c.Servers[0]&&c.Servers[0].UserId)||'';}catch(e){return '';}
}
/* item id of whatever the bar is showing */
function nowNode(){
var bars=document.querySelectorAll('.nowPlayingBar'),i,n;
for(i=0;i<bars.length;i++){
if(!bars[i].getClientRects().length)continue;
n=bars[i].querySelector('[data-id]');
if(n)return n;
}
return null;
}
/* sf-ab-switchguard: the capsule's data-id LAGS the <audio> element by ~2s when
   you tap a second book while the first is playing (measured: at +1s the audio
   src was already book B while the bar still reported book A).
   Everything in tick() is keyed on that id, and rewindCheck() is the dangerous
   one -- it seeks el() (the NEW book) using the OLD book's last-seen stamp, so
   the book you just opened jumps backwards up to 30 seconds for no reason.
   That is the "clicking another audiobook feels buggy" report.
   The <audio> element is the only thing that cannot be stale, so read the id
   from its own URL and simply SIT OUT any tick where the two disagree. */
function audioId(){
var a=el();
if(!a)return '';
var src=a.currentSrc||a.src||'';
var m=/\/Audio\/([0-9a-fA-F-]{32,36})\//.exec(src);
return m?m[1].toLowerCase().replace(/-/g,''):'';
}
function nowId(){
var n=nowNode();
return n?(n.getAttribute('data-id')||''):'';
}
/* sf-np-typeflash (2026-08-24): the bar publishes the type itself, but LATE.
   Measured on a 390px phone: data-itemtype appeared 640ms after the now-playing bar
   became visible on one run, and on another it was still absent 4s in. Until it
   lands isBook() answers null, which is why the full-screen player could not know
   what it was opening.

   So: remember every audiobook id the bar ever confirms, and once per half day take
   one cheap id-only sweep of the audiobook shelf (36 items here). With that list
   present the answer is a synchronous map lookup keyed by the id in the <audio>
   element's own stream URL -- which cannot be stale -- so the player knows what it
   is before it paints. A live data-itemtype still always wins, so this can never
   make the answer staler than it already was. */
var TKEY='sf-ab-types';
var TMAP={},TBUSY=false;
try{TMAP=JSON.parse(localStorage.getItem(TKEY)||'{}')||{};}catch(e){TMAP={};}
function tnorm(x){return String(x||'').toLowerCase().replace(/-/g,'');}
function tFresh(){
var at=0;
try{at=parseInt(localStorage.getItem(TKEY+'-at')||'0',10);}catch(e){}
return (Date.now()-at)<43200000;
}
function tRemember(id){
var k=tnorm(id);
if(!k||TMAP[k])return;
TMAP[k]=1;
try{localStorage.setItem(TKEY,JSON.stringify(TMAP));}catch(e){}
}
/* Only AudioBook ids are stored, so the map stays the size of the shelf rather than
   growing by one entry per song ever played. Anything absent from a FRESH map is
   therefore known not to be a book. */
function tPrewarm(){
if(TBUSY||tFresh())return;
var ac=window.ApiClient;
if(!ac||!ac.getCurrentUserId||!ac.getUrl||!ac.getJSON)return;
TBUSY=true;
try{
ac.getJSON(ac.getUrl('Items',{UserId:ac.getCurrentUserId(),IncludeItemTypes:'AudioBook',
Recursive:true,Limit:2000,EnableImages:false,EnableUserData:false,EnableTotalRecordCount:false}))
.then(function(d){
var it=(d&&d.Items)||[],i,m={};
for(i=0;i<it.length;i++)m[tnorm(it[i].Id)]=1;
TMAP=m;TBUSY=false;
try{localStorage.setItem(TKEY,JSON.stringify(TMAP));
localStorage.setItem(TKEY+'-at',String(Date.now()));}catch(e){}
}).catch(function(){TBUSY=false;});
}catch(e){TBUSY=false;}
}
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
try{if(window.requestIdleCallback)requestIdleCallback(function(){tPrewarm();},{timeout:8000});else{tPrewarm();}}catch(e){try{tPrewarm();}catch(e2){}}
},20000);
function isBook(id){
var n=nowNode(),t='';
if(n)t=n.getAttribute('data-itemtype')||'';
if(t){
if(t==='AudioBook'){tRemember(n.getAttribute('data-id'));return true;}
return false;
}
var k=tnorm(id||nowId()||audioId());
if(!k)return null;
if(TMAP[k])return true;
if(tFresh())return false;
tPrewarm();
return null;
}
/* sf-ch-sameorigin (2026-08-21): the chapter index, served from Jellyfin's own
   web root. It used to come only from requestbridge on :8099, which the admin's
   phones cannot reach -- so the chapter list vanished and chapter-skip did
   nothing, while the buttons themselves stayed on screen because they are built
   blind. One 56KB file covers every book; fetched once, then cached. */
var SF_CH_ALL=null,SF_CH_BUSY=false,SF_CH_WAIT=[];
function sfChSameOrigin(id,cb){
var key=String(id||'').replace(/-/g,'').toLowerCase();
function give(){
if(!SF_CH_ALL){cb(null);return;}
var hit=SF_CH_ALL[key];
cb(hit&&hit.c&&hit.c.length?hit.c:null);
}
if(SF_CH_ALL!==null){give();return;}
SF_CH_WAIT.push(give);
if(SF_CH_BUSY)return;
SF_CH_BUSY=true;
fetch('readalong/chapters.json',{credentials:'same-origin'})
.then(function(r){return r.ok?r.json():null;})
.then(function(d){
var out={},items=(d&&d.items)||{},k;
for(k in items){if(items.hasOwnProperty(k))out[String(k).replace(/-/g,'').toLowerCase()]=items[k];}
SF_CH_ALL=out;
}).catch(function(){SF_CH_ALL=false;})
.then(function(){
SF_CH_BUSY=false;
var w=SF_CH_WAIT;SF_CH_WAIT=[];
for(var i=0;i<w.length;i++){try{w[i]();}catch(e){}}
});
}
function chapters(id,cb){
if(abChaps[id]!==undefined){cb(abChaps[id]);return;}
abChaps[id]=null;
sfChSameOrigin(id,function(hit){
if(hit){abChaps[id]=hit;cb(hit);return;}
fetch(bridge()+'/api/chapters?id='+encodeURIComponent(id),
{headers:{'x-jellyfin-token':token()}})
.then(function(r){return r.json();})
.then(function(d){abChaps[id]=(d&&d.chapters)||[];cb(abChaps[id]);})
.catch(function(){abChaps[id]=[];cb([]);});
});
}
function fmt(sec){
sec=Math.max(0,Math.round(sec));
var m=Math.floor(sec/60),s2=sec%60;
return m+':'+(s2<10?'0':'')+s2;
}
function seekBy(d){
var a=el();
if(!a)return;
try{a.currentTime=Math.max(0,a.currentTime+d);}catch(e){}
}
function jumpChapter(dir){
var a=el(),id=nowId();
if(!a||!id)return;
chapters(id,function(list){
if(!list||!list.length)return;
var t=a.currentTime,i,target=null;
if(dir<0){
/* like every audiobook player: within the first 2s, go to the previous
   chapter; otherwise restart the current one */
for(i=list.length-1;i>=0;i--){if(list[i].t<=t-2){target=list[i].t;break;}}
if(target===null)target=0;
}else{
for(i=0;i<list.length;i++){if(list[i].t>t+0.5){target=list[i].t;break;}}
if(target===null)return;
}
try{a.currentTime=target;}catch(e){}
});
}
/* ---- sleep timer ---------------------------------------------------- */
function sleepStop(){
var a=el();
if(a){
try{
if(volSaved<0)volSaved=a.volume;
var v=a.volume,step=v/20;
clearInterval(fading);
fading=setInterval(function(){
if(!a||a.volume<=step){
clearInterval(fading);fading=0;
try{if(a){a.pause();a.volume=(volSaved<0?1:volSaved);}}catch(e){}
volSaved=-1;
return;
}
try{a.volume=Math.max(0,a.volume-step);}catch(e){}
},500);
}catch(e){try{a.pause();}catch(e2){}}
}
sleepAt=0;sleepChapter=false;
paint();
}
function sleepSet(mins){
if(!mins){sleepAt=0;sleepChapter=false;paint();return;}
if(mins==='chapter'){sleepChapter=true;sleepAt=0;}
else{sleepAt=Date.now()+mins*60000;sleepChapter=false;}
paint();
}
function sleepLeft(){
if(sleepChapter)return 'chapter';
if(!sleepAt)return '';
return fmt((sleepAt-Date.now())/1000);
}
function sleepTick(){
var a=el();
if(!a)return;
if(sleepAt&&Date.now()>=sleepAt){sleepStop();return;}
if(sleepChapter){
var id=nowId();
if(!id)return;
var list=abChaps[id];
if(!list||!list.length)return;
var t=a.currentTime,i,end=null;
for(i=0;i<list.length;i++){if(list[i].t>t+0.4){end=list[i].t;break;}}
if(end!==null&&t>=end-0.4)sleepStop();
}
}
/* ---- auto-rewind ----------------------------------------------------- */
/* Rewind proportional to time away, the behaviour Smart Audiobook Player and
   Prologue are liked for: a short pause needs no rewind, overnight needs a run-up. */
function rewindFor(gapMs){
if(gapMs<45000)return 0;
if(gapMs<3600000)return 5;
if(gapMs<86400000)return 15;
return 30;
}
function rewindCheck(id){
var a=el();
if(!a||a.paused)return;
var k='sf-ab-last-'+id,now=Date.now();
var prev=0;
try{prev=parseInt(localStorage.getItem(k)||'0',10);}catch(e){}
if(!lastSeen[id]){
lastSeen[id]=now;
if(prev){
var back=rewindFor(now-prev);
if(back>0&&a.currentTime>back+1){
try{a.currentTime=a.currentTime-back;}catch(e){}
}
}
}
try{localStorage.setItem(k,String(now));}catch(e){}
}
/* ---- UI -------------------------------------------------------------- */
function btn(cls,label,title,fn){
var b=document.createElement('button');
b.type='button';
b.className='sf-ab-btn '+cls;
b.title=title;
b.innerHTML=label;
b.addEventListener('click',function(e){e.preventDefault();e.stopPropagation();fn(e);});
return b;
}
function closeMenus(){
var m=document.querySelectorAll('.sf-ab-menu');
for(var i=0;i<m.length;i++)if(m[i].parentNode)m[i].parentNode.removeChild(m[i]);
}
/* ---- sf-ab-bm: bookmarks -------------------------------------------------
   The one Audible feature with no Jellyfin equivalent: mark a moment and come
   back to it. Stored SERVER side through requestbridge (/api/bookmarks, keyed
   by userId|itemId) rather than in localStorage, precisely so a mark made on
   the phone is there on the desktop -- a per-device bookmark would miss the
   point of the feature.
   The default label is the chapter you are in, because "1:23:45" alone tells
   you nothing weeks later. */
var bmCache={},bmBusy={};
function bmFmt(t){
t=Math.max(0,Math.floor(t||0));
var h=Math.floor(t/3600),m=Math.floor((t%3600)/60),sec=t%60;
function p2(n){return (n<10?'0':'')+n;}
return h?(h+':'+p2(m)+':'+p2(sec)):(m+':'+p2(sec));
}
function bmLoad(id,cb){
if(bmCache[id]){cb(bmCache[id]);return;}
if(bmBusy[id]){cb(null);return;}
bmBusy[id]=1;
fetch(bridge()+'/api/bookmarks?id='+encodeURIComponent(id),
{headers:{'x-jellyfin-token':token()}})
.then(function(r){return r.ok?r.json():null;})
.then(function(d){bmBusy[id]=0;bmCache[id]=(d&&d.bookmarks)||[];cb(bmCache[id]);})
.catch(function(){bmBusy[id]=0;bmCache[id]=[];cb([]);});
}
function bmSave(id,body,cb){
fetch(bridge()+'/api/bookmarks?id='+encodeURIComponent(id),
{method:'POST',headers:{'x-jellyfin-token':token(),'Content-Type':'application/json'},
body:JSON.stringify(body)})
.then(function(r){return r.ok?r.json():null;})
.then(function(d){bmCache[id]=(d&&d.bookmarks)||[];if(cb)cb(bmCache[id]);})
.catch(function(){if(cb)cb(null);});
}
/* the chapter you are in, used as the default label */
function bmChapterAt(id,t,cb){
try{
chapters(id,function(list){
var name='',i;
for(i=0;i<(list||[]).length;i++){
var st=(list[i].t!==undefined)?list[i].t:(list[i].s||list[i].start||0);
if(st<=t+0.5)name=list[i].n||list[i].name||'';
}
cb(name||'');
});
}catch(e){cb('');}
}
function bmMenu(anchorEl){
var id=nowId(),a=el();
if(!id||!a)return;
var now=a.currentTime||0;
bmLoad(id,function(list){
list=list||[];
var rows=[{label:'\u2795  '+(window.sfTr?window.sfTr('Bookmark this moment'):'Bookmark this moment'),fn:function(){
bmChapterAt(id,now,function(ch){
bmSave(id,{t:now,label:ch},null);
});
}}];
for(var i=0;i<list.length;i++){
(function(b){
rows.push({
label:bmFmt(b.t)+(b.label?('  ·  '+b.label):''),
fn:function(){var au=el();if(au)try{au.currentTime=b.t;}catch(e){}},
del:function(){bmSave(id,{action:'remove',t:b.t},null);}
});
})(list[i]);
}
if(list.length<1)rows.push({label:(window.sfTr?window.sfTr('No bookmarks yet'):'No bookmarks yet'),on:false,fn:function(){}});
openMenu(anchorEl,rows);
});
}
function openMenu(anchor,rows){
closeMenus();
var m=document.createElement('div');
m.className='sf-ab-menu';
for(var i=0;i<rows.length;i++){
(function(r){
var b=document.createElement('button');
b.type='button';
b.className='sf-ab-mi'+(r.on?' sf-ab-on':'');
b.textContent=r.label;
b.addEventListener('click',function(e){
e.preventDefault();e.stopPropagation();
closeMenus();r.fn();
});
/* sf-ab-bm: a row can carry its own delete, so a bookmark is removable from the
   same list it is used in -- without it the only way out would be "remove all". */
if(r.del){
var x=document.createElement('span');
x.className='sf-ab-mi-x';
x.textContent='\u00d7';
x.setAttribute('role','button');
x.setAttribute('aria-label','Remove');
x.addEventListener('click',function(e){
e.preventDefault();e.stopPropagation();
closeMenus();r.del();
});
b.appendChild(x);
b.classList.add('sf-ab-mi-hasx');
}
m.appendChild(b);
})(rows[i]);
}
document.body.appendChild(m);
var r=anchor.getBoundingClientRect();
m.style.left=Math.max(8,Math.min(window.innerWidth-m.offsetWidth-8,r.left+r.width/2-m.offsetWidth/2))+'px';
m.style.top=Math.max(8,r.top-m.offsetHeight-10)+'px';
setTimeout(function(){
document.addEventListener('click',function once(){closeMenus();document.removeEventListener('click',once,true);},true);
},0);
}
function paint(){
var wraps=document.querySelectorAll('.sf-ab-wrap'),i;
for(i=0;i<wraps.length;i++){
var sp=wraps[i].querySelector('.sf-ab-rate');
/* sf-np-flicker: same rule -- innerHTML rebuilds two nodes every tick. */
if(sp&&sp.getAttribute('data-r')!==String(rate())){
sp.setAttribute('data-r',String(rate()));
sp.innerHTML='<span class="sf-ab-rate-n">'+rate()+'</span>&times;';
}
var sl=wraps[i].querySelector('.sf-ab-sleep');
if(sl){
var left=sleepLeft();
sl.classList.toggle('sf-ab-armed',!!left);
sl.title=left?('Sleep timer: '+left):'Sleep timer';
var lab=sl.querySelector('.sf-ab-sleep-lab');
if(lab)lab.textContent=left&&left!=='chapter'?left:'';
}
}
}
function build(bar){
if(bar.querySelector('.sf-ab-wrap'))return;
/* Anchor on the CLASS, never on title=. The title attribute is localized, so
   `button[title="Pause"]` only ever matched in English -- measured: en abWrap
   true, zh abWrap FALSE with the same button carrying title="\u6682\u505c". That
   silently removed every audiobook control (chapter skip, +/-30s, speed, sleep
   timer) for anyone not using English. .playPauseButton is what Jellyfin
   actually puts on it; the old selectors stay as a fallback. */
var anchor=bar.querySelector('.playPauseButton,.btnPause,.btnPlayPause,button[title="Pause"],button[title="Play"]');
if(!anchor||!anchor.parentNode)return;
var wrap=document.createElement('div');
wrap.className='sf-ab-wrap';
/* sf-ab-declutter (2026-08-28). The admin: the audiobook controls are "too much and
   cluttery". Measured on the live bar: 13 controls, NINE of them between the play
   button and the book's own title, all the same weight -- and the two skips were
   identical circles both reading "30", so back and forward were indistinguishable.
   Every audiobook player surveyed (Audible, Libby, Apple Books, Spotify) leads
   with one transport group and demotes the rest.
   PRIMARY here = the two skips flanking Jellyfin's own play/pause. Everything
   else moves into .sf-ab-sec, smaller and dimmer behind a hairline divider, so
   the eye lands on transport first. Nothing is removed -- the complaint is
   weight and legibility, not function. */
var sec=document.createElement('div');
sec.className='sf-ab-sec';
var pchB=btn('sf-ab-pch','&laquo;','Previous chapter',function(){jumpChapter(-1);});
/* sf-ab-center (2026-08-28). Back-30 goes BEFORE the play button, not after it.
   Every player surveyed -- Scribd, Libby, Apple Books, Audiobookshelf, and the
   physical players the convention came from -- centres play/pause with the skips
   flanking it: [-30] [play] [+30]. Ours read [play] [-30] [+30], which puts the
   primary action at the edge of its own group and makes the pair look like two
   forward controls. Jellyfin owns the play button, so we insert either side of it
   rather than rebuilding it. */
var pre=bar.querySelector('.sf-ab-pre');
if(pre&&pre.parentNode)pre.parentNode.removeChild(pre);
pre=document.createElement('div');
pre.className='sf-ab-pre';
pre.appendChild(btn('sf-ab-b30','<span class="material-icons sf-ab-i">replay_30</span>','Back 30 seconds',function(){seekBy(-30);}));
anchor.parentNode.insertBefore(pre,anchor);
var rb=btn('sf-ab-rate','1&times;','Playback speed',function(e){
var rows=[],i;
for(i=0;i<RATES.length;i++){
(function(v){rows.push({label:v+'\u00d7',on:Math.abs(rate()-v)<0.001,fn:function(){setRate(v);}});})(RATES[i]);
}
openMenu(e.currentTarget,rows);
});
wrap.appendChild(btn('sf-ab-f30','<span class="material-icons sf-ab-i">forward_30</span>','Forward 30 seconds',function(){seekBy(30);}));
sec.appendChild(rb);
sec.appendChild(pchB);
sec.appendChild(btn('sf-ab-nch','&raquo;','Next chapter',function(){jumpChapter(1);}));
/* sf-ab-readalong (2026-08-21). The read-along entry belongs HERE, in the
   audiobook cluster, not on the collapsed now-playing bar. The admin could not find
   it for days and described exactly this row -- chapter skip, 30s, speed, sleep
   -- because this is the control surface he actually uses. The bar button stays
   for the collapsed view; this is the one that matters.
   Shown only when a read-along map exists for the book, so books without one are
   unchanged. */
var raBtn=btn('sf-ab-ra','<span class="sf-ab-book"></span>','Read along',function(){
try{if(window.__sfRaOpen)window.__sfRaOpen(nowId());}catch(e){}
});
raBtn.style.display='none';
sec.appendChild(raBtn);
(function(){
var id=nowId();
if(!id)return;
fetch('readalong/'+encodeURIComponent(id)+'.json',{credentials:'same-origin'})
.then(function(r){return r.ok?r.json():null;})
.then(function(d){if(d&&d.b&&d.b.length)raBtn.style.display='';})
.catch(function(){});
})();
sec.appendChild(btn('sf-ab-bm','<span class="sf-ab-bmk"></span>','Bookmarks',function(e){
bmMenu(e.currentTarget);
}));
sec.appendChild(btn('sf-ab-sleep','<span class="sf-ab-moon"></span><span class="sf-ab-sleep-lab"></span>','Sleep timer',function(e){
openMenu(e.currentTarget,[
{label:'Off',on:!sleepAt&&!sleepChapter,fn:function(){sleepSet(0);}},
{label:'5 minutes',fn:function(){sleepSet(5);}},
{label:'10 minutes',fn:function(){sleepSet(10);}},
{label:'15 minutes',fn:function(){sleepSet(15);}},
{label:'30 minutes',fn:function(){sleepSet(30);}},
{label:'45 minutes',fn:function(){sleepSet(45);}},
{label:'1 hour',fn:function(){sleepSet(60);}},
{label:'End of chapter',on:sleepChapter,fn:function(){sleepSet('chapter');}}
]);
}));
wrap.appendChild(sec);
anchor.parentNode.insertBefore(wrap,anchor.nextSibling);
paint();
}
/* sf-ab-striplag: REVERTED. Between Jellyfin swapping the bar to a song and our
   next tick there is a sub-second window where a book's controls sit on a track.
   A MutationObserver that stripped the moment data-itemtype stopped being
   AudioBook fixed that -- and broke read-along: it picked the FIRST
   [data-itemtype] node in the bar rather than the now-playing one, stripped
   during playback, the tick rebuilt, and the churn left the reader stuck on
   sentence 0 (measured 0->0 where it should advance ~3 sentences in 11s).
   A cosmetic sub-second artifact is not worth breaking a feature for. If this is
   attempted again, resolve the now-playing node the way isBook() does and prove
   read-along still tracks. */
function strip(){
var w=document.querySelectorAll('.sf-ab-wrap'),i;
for(i=0;i<w.length;i++)if(w[i].parentNode)w[i].parentNode.removeChild(w[i]);
closeMenus();
stripStage();
}
/* ---- sf-ab-stage: the FULL-SCREEN book player -------------------------
   the admin's call, and the right one: the capsule stays minimal and the full
   player carries chapters, speed and the sleep timer. The chapter arrows had
   been deleted outright on phones ("the bar is tight, so drop chapter arrows")
   -- the bar was simply the wrong home for them, and losing them cost the one
   control an audiobook listener needs most.

   Built HERE, inside the audiobook IIFE, rather than in the sf-np stage code,
   for one concrete reason: openMenu() positions its popup against the button
   that was clicked. Proxying a stage button through to the capsule's hidden
   copy anchored the speed menu to a display:none node and parked it in the
   top-left corner. Owning the buttons keeps the menus where the finger is.

   Targets are 44px here, not the capsule's 29px, which was under the
   accessibility floor. */
function hms(sec){
sec=Math.max(0,Math.round(sec));
var h=Math.floor(sec/3600),m=Math.floor((sec%3600)/60),s2=sec%60;
return (h?(h+':'+(m<10?'0':'')):'')+m+':'+(s2<10?'0':'')+s2;
}
function stageEl(){return document.querySelector('.sf-np-stage');}
function buildStage(id){
var stage=stageEl();
if(!stage)return;
var root=document.querySelector('.sf-np');
/* sf-np-flicker: buildStage runs on EVERY tick, and classList.add rewrites the
   class attribute even when the token is already present -- which re-triggers
   the overlay's CSS transitions ~1.4 times a second. Measured 14 rewrites in
   10s of an otherwise idle player. Only write on a real change. */
if(root&&!root.classList.contains('sf-np-book'))root.classList.add('sf-np-book');
var ctr=stage.querySelector('.sf-np-controls');
if(ctr&&!ctr.querySelector('.sf-ab-s-b30')){
var play=ctr.querySelector('.sf-np-play');
if(play){
var pch=btn('sf-ab-s-pch','&laquo;','Previous chapter',function(){jumpChapter(-1);});
var b30=btn('sf-ab-s-b30','<span class="sf-ab-n">30</span>','Back 30 seconds',function(){seekBy(-30);});
var f30=btn('sf-ab-s-f30','<span class="sf-ab-n">30</span>','Forward 30 seconds',function(){seekBy(30);});
var nch=btn('sf-ab-s-nch','&raquo;','Next chapter',function(){jumpChapter(1);});
ctr.insertBefore(pch,play);
ctr.insertBefore(b30,play);
ctr.insertBefore(f30,play.nextSibling);
ctr.insertBefore(nch,f30.nextSibling);
}
}
if(ctr&&!stage.querySelector('.sf-ab-s-row2')){
var r2=document.createElement('div');
r2.className='sf-ab-s-row2';
r2.appendChild(btn('sf-ab-s-rate','1&times;','Playback speed',function(e){
var rows=[],i;
for(i=0;i<RATES.length;i++){
(function(v){rows.push({label:v+'×',on:Math.abs(rate()-v)<0.001,fn:function(){setRate(v);}});})(RATES[i]);
}
openMenu(e.currentTarget,rows);
}));
r2.appendChild(btn('sf-ab-s-sleep','<span class="sf-ab-moon"></span><span class="sf-ab-s-sleep-lab"></span>','Sleep timer',function(e){
openMenu(e.currentTarget,[
{label:'Off',on:!sleepAt&&!sleepChapter,fn:function(){sleepSet(0);}},
{label:'5 minutes',fn:function(){sleepSet(5);}},
{label:'10 minutes',fn:function(){sleepSet(10);}},
{label:'15 minutes',fn:function(){sleepSet(15);}},
{label:'30 minutes',fn:function(){sleepSet(30);}},
{label:'45 minutes',fn:function(){sleepSet(45);}},
{label:'1 hour',fn:function(){sleepSet(60);}},
{label:'End of chapter',on:sleepChapter,fn:function(){sleepSet('chapter');}}
]);
}));
/* sf-ab-s-ra (2026-08-21). The admin: "our read along feature on mobile only shows
   when the controls are minimized. when full screen we don't see it that
   feature." Correct -- the button existed only on the minimised cluster
   (.sf-ab-ra), and the full-screen stage never got one, so the moment you
   expanded the player the feature vanished. Everything else on this row was
   already here; this was simply missing.

   Opening the reader closes the player first: stacking a full-screen reader on
   top of a full-screen player left two scroll containers fighting for the same
   drag. */
r2.appendChild(btn('sf-ab-s-bm','<span class="sf-ab-bmk"></span>','Bookmarks',function(e){
bmMenu(e.currentTarget);
}));
r2.appendChild(btn('sf-ab-s-ra','<span class="sf-ab-book"></span>','Read along',function(){
try{
var np=document.querySelector('.sf-np');
if(np){np.classList.remove('sf-np-show');document.documentElement.classList.remove('sf-np-lock');}
}catch(e){}
try{if(window.__sfRaOpen)window.__sfRaOpen(nowId());}catch(e){}
}));
ctr.parentNode.insertBefore(r2,ctr.nextSibling);
}
/* Offered only for a book that actually HAS a map, so it is never a dead end.
   Re-checked whenever the book changes -- row2 itself is built once and kept. */
(function(){
var rb=stage.querySelector('.sf-ab-s-ra');
if(!rb||rb.getAttribute('data-for')===id)return;
rb.setAttribute('data-for',id);
rb.style.display='none';
fetch('readalong/'+encodeURIComponent(id)+'.json',{credentials:'same-origin'})
.then(function(r){return r.ok?r.json():null;})
.then(function(m){
if(m&&m.b&&m.b.length&&rb.getAttribute('data-for')===id)rb.style.display='';
}).catch(function(){});
})();
buildChapterList(stage,id);
}
function buildChapterList(stage,id){
var list=abChaps[id];
if(!list||!list.length)return;
var box=stage.querySelector('.sf-ab-s-chl');
if(box&&box.getAttribute('data-id')===id)return;
if(box&&box.parentNode)box.parentNode.removeChild(box);
box=document.createElement('div');
box.className='sf-ab-s-chl';
box.setAttribute('data-id',id);
var h=document.createElement('div');
h.className='sf-ab-s-chh sf-ab-mi-h';
h.textContent='Chapters';
box.appendChild(h);
var i;
for(i=0;i<list.length;i++){
(function(ch,idx){
var row=document.createElement('button');
row.type='button';
row.className='sf-ab-s-chrow';
row.innerHTML='<span class="sf-ab-s-chn"></span>'
+'<span class="sf-ab-s-chname"></span>'
+'<span class="sf-ab-s-chat"></span>';
row.querySelector('.sf-ab-s-chn').textContent=String(idx+1);
row.querySelector('.sf-ab-s-chname').textContent=ch.n||('Chapter '+(idx+1));
row.querySelector('.sf-ab-s-chat').textContent=hms(ch.t);
/* sf-ab-chtap: a 38-row list inside a 34vh scroller means most taps arrive at
   the end of a drag, and a plain click handler fires on those too -- so
   scrolling the chapter list jumped the book. Only count it as a tap if the
   finger stayed put. */
row.addEventListener('touchstart',function(e){
var t=e.touches&&e.touches[0];
row.__sx=t?t.clientX:0;row.__sy=t?t.clientY:0;row.__moved=false;
},{passive:true});
row.addEventListener('touchmove',function(e){
var t=e.touches&&e.touches[0];
if(!t)return;
if(Math.abs(t.clientX-row.__sx)>8||Math.abs(t.clientY-row.__sy)>8)row.__moved=true;
},{passive:true});
row.addEventListener('click',function(e){
e.preventDefault();e.stopPropagation();
if(row.__moved){row.__moved=false;return;}
var a=el();
if(a){try{a.currentTime=ch.t;}catch(x){}}
});
box.appendChild(row);
})(list[i],i);
}
stage.appendChild(box);
}
function paintStage(id){
var stage=stageEl();
if(!stage)return;
var rl=stage.querySelector('.sf-ab-s-rate');
if(rl&&rl.getAttribute('data-r')!==String(rate())){
rl.setAttribute('data-r',String(rate()));
rl.innerHTML='<span class="sf-ab-rate-n">'+rate()+'</span>&times;';
}
var sl=stage.querySelector('.sf-ab-s-sleep');
if(sl){
var left=sleepLeft();
sl.classList.toggle('sf-ab-armed',!!left);
var lab=sl.querySelector('.sf-ab-s-sleep-lab');
if(lab)lab.textContent=left&&left!=='chapter'?left:'';
}
var a=el(),list=abChaps[id];
if(a&&list&&list.length){
var cur=0,i;
for(i=0;i<list.length;i++)if(a.currentTime>=list[i].t)cur=i;
var rows=stage.querySelectorAll('.sf-ab-s-chrow');
for(i=0;i<rows.length;i++)rows[i].classList.toggle('sf-ab-s-now',i===cur);
}
}
function stripStage(){
var root=document.querySelector('.sf-np');
if(root&&root.classList.contains('sf-np-book'))root.classList.remove('sf-np-book');
var junk=document.querySelectorAll('.sf-ab-s-pch,.sf-ab-s-b30,.sf-ab-s-f30,.sf-ab-s-nch,.sf-ab-s-row2,.sf-ab-s-chl'),i;
for(i=0;i<junk.length;i++)if(junk[i].parentNode)junk[i].parentNode.removeChild(junk[i]);
}
function tick(){
try{
if(!nowId()){try{document.documentElement.classList.remove('sf-book-now');}catch(e){}}
/* sf-rate-confirm: normalise the playback rate BEFORE any of the early returns
   below. Every one of them (no bar id yet, mid-switch id disagreement, not a
   book) used to leave a stale 1.5x sitting on the shared <audio> element, and
   Jellyfin reuses that element for the next thing you play. Deciding the rate
   first means there is no path out of this function that can leave music
   running fast. */
try{
var _a0=el();
if(_a0){
var _aid0=audioId(),_nid0=String(nowId()||'').toLowerCase().replace(/-/g,'');
var _want0=(_aid0&&_nid0&&_aid0===_nid0&&isBook(_nid0)===true)?rate():1;
if(Math.abs(_a0.playbackRate-_want0)>0.001)_a0.playbackRate=_want0;
}
}catch(e){}
/* sf-np-typeflash: the bar's [data-id] node can be missing for seconds after
   playback starts (one run: still absent 4s in), and this early return then
   stripped the book controls on every tick for as long as that lasted. The audio
   element's own stream URL carries the same id and cannot be stale, so use it when
   the bar has nothing. */
var id=nowId()||audioId();
if(!id){strip();return;}
var aid=audioId();
if(aid&&aid!==String(id).toLowerCase().replace(/-/g,''))return;   /* mid-switch: state disagrees */
var book=isBook(id);
/* sf-book-now (2026-08-21): a document-level flag for "an audiobook is playing".
   The full-screen player already had .sf-np-book; the now-playing BAR had no
   equivalent, so it kept showing music-only controls during a book -- Lyrics on
   an audiobook, plus shuffle and repeat, which is also what pushed the row wide
   enough to clip Shuffle off the left edge. */
try{document.documentElement.classList.toggle('sf-book-now',book===true);}catch(e){}
/* sf-book-declutter (2026-08-21). The admin, twice: "why do we have lyrics button
   available when we are listening to an audiobook" and "shits overflowing, the
   play pause button is being cut off".

   Both are the same cause: the now-playing bar carries 17 controls during a
   book, several of which are meaningless for one -- Lyrics, Shuffle, Repeat, and
   previous/next TRACK (an audiobook is a single file; the queue length is 1).
   Measured with all 17 present: Shuffle rendered at x=395 inside a bar starting
   at x=403, i.e. clipped off the left edge.

   Done in JS with setProperty(...,'important') rather than a stylesheet rule.
   A CSS attempt matched the element and still lost -- .paper-icon-button-light
   sets display from inside a media query, and fighting that on specificity has
   already cost three rounds. An inline important declaration is not negotiable.
   Every element is restored the moment a book is not what is playing, so music
   is untouched. */
try{
var BOOKHIDE='.sf-lyr-btn,.btnToggleLyrics,.btnShuffleQueue,.toggleRepeatButton,'
+'.previousTrackButton,.nextTrackButton,.sf-ra-btn';
var bars2=document.querySelectorAll('.nowPlayingBar'),bi,bn,bl,bx;
for(bi=0;bi<bars2.length;bi++){
bl=bars2[bi].querySelectorAll(BOOKHIDE);
for(bx=0;bx<bl.length;bx++){
bn=bl[bx];
if(book===true){
if(bn.getAttribute('data-sf-bookhid')!=='1'){
bn.setAttribute('data-sf-bookhid','1');
bn.style.setProperty('display','none','important');
}
}else if(bn.getAttribute('data-sf-bookhid')==='1'){
bn.removeAttribute('data-sf-bookhid');
bn.style.removeProperty('display');
}
}
}
}catch(e){}
if(book!==true){
if(book===false){
strip();
/* sf-rate-leak (2026-08-20). The audiobook speed control writes
   audio.playbackRate, and NOTHING ever put it back. Jellyfin reuses the same
   <audio> element for the next thing you play, so a book left at 1.5x made
   every SONG afterwards play 1.5x fast and a semitone-and-a-half sharp -- the
   "voice gets higher and speeds up" report. Reproduced: set the book speed to
   1.5, play a book, then play an album -> the album's audio element is still at
   1.5 and stays there.
   The rate belongs to audiobooks only, so anything that is NOT a book is
   restored to 1. Deliberately only touches the AUDIO element: Live TV's
   catch-up nudges a VIDEO element's rate and must not be disturbed. */
var na=el();
if(na&&Math.abs(na.playbackRate-1)>0.001){try{na.playbackRate=1;}catch(e){}}
}
return;
}
var bars=document.querySelectorAll('.nowPlayingBar'),i;
for(i=0;i<bars.length;i++)if(bars[i].getClientRects().length)build(bars[i]);
/* Jellyfin builds a new audio element per stream; without this the rate
   silently returns to 1x when a book starts or the stream is rebuilt. */
/* sf-rate-confirm (2026-08-20). The speed control must only ever touch audio we
   have POSITIVELY confirmed is the audiobook. Previously this applied the saved
   rate whenever isBook() said true -- and isBook() reads data-itemtype off the
   now-playing BAR, which lags the <audio> element by seconds on every switch.
   Whenever audioId() could not parse the stream URL, the mid-switch guard above
   was skipped too, so a stale "AudioBook" reading applied 1.5x to whatever was
   really playing. That is the intermittent "the song speeds up and goes higher
   for a few seconds" report -- it lasts exactly as long as the bar stays stale.
   Now the rate is applied ONLY when the audio element's own id matches the bar's
   id AND that item is a book; anything else is forced back to 1x. */
/* sf-np-typeflash: id may now come from the AUDIO element when the bar has not
   published one yet, which would make this comparison trivially true and apply the
   saved speed while sf-rate-guard (which requires the BAR to agree) forces it back
   to 1x every 30ms -- a tug of war, not a fix. The rate stays gated on the bar
   exactly as sf-rate-confirm left it; only the UI uses the fallback id. */
var a=el(),wantRate=1;
if(a){
var _aid=audioId(),_nid=String(nowId()||'').toLowerCase().replace(/-/g,'');
if(_aid&&_nid&&_aid===_nid)wantRate=rate();
if(Math.abs(a.playbackRate-wantRate)>0.001){try{a.playbackRate=wantRate;}catch(e){}}
}
chapters(id,function(){});
rewindCheck(id);
sleepTick();
paint();
buildStage(id);
paintStage(id);
}catch(e){}
}
/* sf-np-typeflash: the synchronous entry point the full-screen player calls in its
   own tap handler. Returns true (book: stage built NOW, before the overlay paints),
   false (not a book: any leftover book chrome removed) or null (not knowable yet --
   the caller suppresses the ambiguous controls rather than guessing). */
window.__sfAbSync=function(){
var id=nowId()||audioId();
if(!id)return null;
var book=isBook(id);
if(book===true){
try{document.documentElement.classList.add('sf-book-now');}catch(e){}
/* the chapter list is the one part that needs a fetch; ask for it now so it
   lands with the rest instead of shifting the stage a second time */
try{chapters(id,function(){var s2=stageEl();if(s2)buildChapterList(s2,id);});}catch(e){}
buildStage(id);
paintStage(id);
return true;
}
if(book===false){stripStage();return false;}
return null;
};
/* sf-ab-msapi: publish the controls the lock-screen block needs. It lives in a
   separate IIFE (tick isolation), so without this it would have to duplicate
   seekBy/jumpChapter/isBook and drift out of step with them. */
try{window.__sfAbApi={el:el,rate:rate,seekBy:seekBy,jumpChapter:jumpChapter,
nowId:nowId,isBook:isBook,audioId:audioId};}catch(e){}
setInterval(tick,700);
})();</script>"""

# --- Read-along (2026-08-21) -------------------------------------------------
# Audible-style immersion reading: the book's text on screen, the sentence being
# narrated highlighted, tap a sentence to jump the audio there.
#
# This was rejected once before as infeasible, on the assumption it needed
# TRANSCRIPTION of every book on a 4-core N100. It does not. We now have the
# EPUB, so this is FORCED ALIGNMENT -- aeneas synthesises the known text and
# DTW-matches it against the audio. Measured on Dungeon Crawler Carl book 1:
# 13.5 hours of audio aligned in 7.3 minutes of wall time (~112x real-time),
# 13,891 sentences, zero non-monotonic points, zero gaps over 3s, median
# speaking rate 2.76 words/sec. The whole 36-book shelf is a few hours overnight.
#
# The map is served per book by requestbridge at /api/readalong?id=<itemid>.
READALONG_MARKER = 'sf-readalong'
READALONG_SCRIPT = r"""<script>(function(){ /* sf-readalong */
if(window.__sfReadAlong)return;
window.__sfReadAlong=1;
var RA={el:null,id:null,map:null,idx:-1,busy:false,pending:{},winFrom:-1,winTo:-1,userScroll:0};

function bridge(){
return (location.port==='8096')
?(location.protocol+'//'+location.hostname+':8099')
:(location.origin+'/requestbridge');
}
function token(){
try{if(window.ApiClient&&ApiClient.accessToken)return ApiClient.accessToken();}catch(e){}
return '';
}
function audioEl(){return document.querySelector('audio');}

/* sf-ra-native (2026-08-21). The Android app (org.jellyfin.mobile) IS this web
   client in a WebView, but it hands playback to a NATIVE player -- so inside the
   page there is no <audio> element and no now-playing bar to read. Everything
   here used to hang off both, which is why read-along was invisible on the phone
   even though our code was running.

   So there are two clocks now. The local <audio> when the page owns playback
   (precise, free), and otherwise this device's own Jellyfin SESSION, polled once
   a second. Session position is reported in ticks and updates about every
   second, which is finer than a spoken sentence -- plenty to highlight by.
   iOS is a different story: Swiftfin is fully native and never loads this page
   at all, so nothing here can reach it. */
var sfRaSess={at:0,id:'',pos:0,busy:false};
function sfRaPollSession(){
var now=Date.now();
if(sfRaSess.busy||now-sfRaSess.at<900)return;
var ac=window.ApiClient;
if(!ac||!ac.getUrl||!ac.getJSON)return;
sfRaSess.busy=true;sfRaSess.at=now;
var dev='';
try{dev=ac.deviceId?ac.deviceId():'';}catch(e){}
ac.getJSON(ac.getUrl('Sessions',dev?{deviceId:dev}:{})).then(function(list){
sfRaSess.busy=false;
var i,s,ni;
for(i=0;i<(list||[]).length;i++){
s=list[i];ni=s&&s.NowPlayingItem;
if(!ni)continue;
sfRaSess.id=String(ni.Id||'').toLowerCase().replace(/-/g,'');
sfRaSess.pos=((s.PlayState||{}).PositionTicks||0)/10000000;
return;
}
sfRaSess.id='';sfRaSess.pos=0;
}).catch(function(){sfRaSess.busy=false;});
}
/* seconds into whatever is playing, from whichever clock exists */
function sfRaTime(){
var a=audioEl();
if(a&&isFinite(a.currentTime))return a.currentTime;
sfRaPollSession();
return sfRaSess.pos;
}
/* the <audio> URL is the only id that cannot be stale mid-switch; with native
   playback there is no URL, so fall back to the session's item */
function nowId(){
var a=audioEl();
if(a){
var m=/\/Audio\/([0-9a-fA-F-]{32,36})\//.exec(a.currentSrc||a.src||'');
if(m)return m[1].toLowerCase().replace(/-/g,'');
}
sfRaPollSession();
return sfRaSess.id||'';
}
function isBook(){
var bars=document.querySelectorAll('.nowPlayingBar'),i,n;
for(i=0;i<bars.length;i++){
if(!bars[i].getClientRects().length)continue;
n=bars[i].querySelector('[data-id]');
if(n)return (n.getAttribute('data-itemtype')||'')==='AudioBook';
}
return false;
}

/* ---- the map ---- */
var raCache={};
/* sf-ra-sameorigin (2026-08-21). The map used to come from requestbridge on port
   8099, and that is why the button never appeared on the admin's phones: the map has
   to load BEFORE the button is drawn, and :8099 is not reachable from every path
   the app is opened on (his iPhone reports from a different LAN subnet, a different subnet;
   remote access goes through nginx, which only proxies some prefixes). The
   audiobook chapter buttons were visible the whole time because those are built
   blind and only need the bridge when clicked -- which is exactly why this looked
   like "some controls work, read-along is missing".

   The maps are now static files under Jellyfin's own web root, so they are
   same-origin with index.html and reachable wherever Jellyfin itself is, with no
   second port, no second service and no separate token. The bridge is kept as a
   fallback for anything that has not been copied across yet. */
function loadMap(id,cb){
if(raCache[id]!==undefined){cb(raCache[id]);return;}
if(RA.pending[id]){RA.pending[id].push(cb);return;}
RA.pending[id]=[cb];
function settle(v){
raCache[id]=v;
var list=RA.pending[id]||[];delete RA.pending[id];
for(var i=0;i<list.length;i++){try{list[i](v);}catch(e){}}
}
function ok(d){return (d&&d.b&&d.b.length)?d:null;}
/* same origin first: no token, no CORS, works wherever the app does */
fetch('readalong/'+encodeURIComponent(id)+'.json',{credentials:'same-origin'})
.then(function(r){return r.ok?r.json():null;})
.then(function(d){
if(ok(d)){settle(d);return;}
throw 0;
})
.catch(function(){
/* fallback: the bridge, for maps not yet copied into the web root */
fetch(bridge()+'/api/readalong?id='+encodeURIComponent(id),
{headers:{'x-jellyfin-token':token()}})
.then(function(r){return r.ok?r.json():null;})
.then(function(d){settle(ok(d)||false);})
.catch(function(){settle(false);});
});
}

/* Binary search: 13,891 sentences is far too many to scan on every tick. */
function findIdx(map,t){
var lo=0,hi=map.b.length-1,best=-1;
while(lo<=hi){
var mid=(lo+hi)>>1;
if(map.b[mid]<=t){best=mid;lo=mid+1;}
else hi=mid-1;
}
return best;
}

/* ---- window rendering ----
   The whole book cannot live in the DOM -- 13,891 paragraphs is tens of
   megabytes of layout and it locks up a phone. Only a window around the current
   sentence is rendered, with spacer divs standing in for everything above and
   below so the scrollbar still feels like a book. */
var WIN=60;
function renderWindow(force){
var d=RA.el;if(!d||!RA.map)return;
var box=d.querySelector('.sf-ra-text');
var from=Math.max(0,RA.idx-WIN), to=Math.min(RA.map.b.length-1,RA.idx+WIN);
if(!force&&from===RA.winFrom&&to===RA.winTo)return;
RA.winFrom=from;RA.winTo=to;
/* Render REAL paragraphs with sentences as inline spans. One block per
   sentence looked shattered on dialogue -- "Yes," / Mordecai said. / He
   sighed. came out as three stacked blocks instead of one line of prose. The
   map carries the source paragraph index for exactly this. */
var html='',i,lastCh=-1,lastP=null,open=false;
function esc(x){return String(x).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');}
for(i=from;i<=to;i++){
var ch=RA.map.c[i];
var pa=RA.map.p?RA.map.p[i]:i;      /* older maps have no paragraph index */
if(ch!==lastCh){
if(open){html+='</p>';open=false;}
lastCh=ch;lastP=null;
html+='<h3 class="sf-ra-ch">'+(ch===999?'Epilogue':'Chapter '+ch)+'</h3>';
}
if(pa!==lastP){
if(open)html+='</p>';
html+='<p class="sf-ra-p">';open=true;lastP=pa;
}
html+='<span class="sf-ra-s" data-i="'+i+'">'+esc(RA.map.t[i])+'</span> ';
}
if(open)html+='</p>';
box.innerHTML=html;
paintActive(true);
}
function paintActive(scroll){
var d=RA.el;if(!d)return;
var rows=d.querySelectorAll('.sf-ra-s'),i,el,n;
for(i=0;i<rows.length;i++){
el=rows[i];n=parseInt(el.getAttribute('data-i'),10);
el.classList.toggle('sf-ra-on',n===RA.idx);
el.classList.toggle('sf-ra-done',n<RA.idx);
}
if(scroll){
var cur=d.querySelector('.sf-ra-s.sf-ra-on');
/* do not fight someone who is reading ahead */
if(cur&&Date.now()-RA.userScroll>6000){
try{cur.scrollIntoView({block:'center',behavior:'smooth'});}catch(e){}
}
}
}

function build(){
if(RA.el)return RA.el;
var d=document.createElement('div');
d.className='sf-ra';
d.innerHTML='<div class="sf-ra-top">'
+'<button class="sf-ra-x" title="Close"><span class="material-icons" aria-hidden="true">close</span></button>'
+'<div class="sf-ra-title"></div>'
+'<button class="sf-ra-sz" title="Text size"><span class="material-icons" aria-hidden="true">format_size</span></button>'
+'</div>'
+'<div class="sf-ra-text"></div>';
d.querySelector('.sf-ra-x').addEventListener('click',close);
d.querySelector('.sf-ra-sz').addEventListener('click',function(){
var cur=parseInt(localStorage.getItem('sf-ra-size')||'19',10);
var next=cur>=25?16:cur+3;
try{localStorage.setItem('sf-ra-size',String(next));}catch(e){}
d.style.setProperty('--sf-ra-fs',next+'px');
});
/* tap a sentence to jump there */
d.querySelector('.sf-ra-text').addEventListener('click',function(e){
var p=e.target&&e.target.closest?e.target.closest('.sf-ra-s'):null;
if(!p||!RA.map)return;
var i=parseInt(p.getAttribute('data-i'),10);
if(!isFinite(RA.map.b[i]))return;
var a=audioEl();
if(a){
try{a.currentTime=RA.map.b[i];if(a.paused)a.play();}catch(err){}
}else{
/* native player: ask the server to seek this session instead */
try{
var ac=window.ApiClient,dev='';
try{dev=ac.deviceId?ac.deviceId():'';}catch(e2){}
ac.getJSON(ac.getUrl('Sessions',dev?{deviceId:dev}:{})).then(function(list){
var s0=(list||[]).filter(function(x){return x.NowPlayingItem;})[0];
if(!s0)return;
ac.ajax({type:'POST',url:ac.getUrl('Sessions/'+s0.Id+'/Playing/Seek',
{seekPositionTicks:Math.round(RA.map.b[i]*10000000)})}).catch(function(){});
sfRaSess.pos=RA.map.b[i];sfRaSess.at=0;
}).catch(function(){});
}catch(err){}
}
RA.idx=i;RA.userScroll=0;renderWindow(true);
});
d.querySelector('.sf-ra-text').addEventListener('scroll',function(){
RA.userScroll=Date.now();
},{passive:true});
document.body.appendChild(d);
RA.el=d;
var sz=parseInt(localStorage.getItem('sf-ra-size')||'19',10);
d.style.setProperty('--sf-ra-fs',sz+'px');
return d;
}
function open_(explicitId){
var id=explicitId||nowId();
if(!id)return;
loadMap(id,function(map){
if(!map)return;
RA.map=map;RA.id=id;
var d=build();
d.querySelector('.sf-ra-title').textContent=map.n||'';
d.classList.add('sf-ra-open');
document.documentElement.classList.add('sf-ra-lock');
RA.idx=-1;RA.winFrom=-1;RA.winTo=-1;RA.userScroll=0;
tick(true);
});
}
function close(){
if(RA.el){RA.el.classList.remove('sf-ra-open');}
document.documentElement.classList.remove('sf-ra-lock');
}
function isOpen(){return !!(RA.el&&RA.el.classList.contains('sf-ra-open'));}

/* ---- entry points ----
   TWO of them on purpose. The now-playing bar is the natural place when the page
   owns playback, but the Android app plays natively and may never render that
   bar -- so the audiobook's own DETAIL page carries the button as well. The
   detail page is plain web UI and always renders, so this is the one that works
   everywhere the page loads at all. */
function detailEntry(){
var h=location.hash||'';
if(h.indexOf('#/details')!==0)return;
var m=/[?&]id=([0-9a-fA-F-]{32,36})/.exec(h);
if(!m)return;
var id=m[1].toLowerCase().replace(/-/g,'');
var pages=document.querySelectorAll('#itemDetailPage'),pg=null,i;
for(i=0;i<pages.length;i++){
if(pages[i].offsetParent!==null&&pages[i].getBoundingClientRect().height>0){pg=pages[i];break;}
}
if(!pg||pg.querySelector('.sf-ra-detail'))return;
var host=pg.querySelector('.mainDetailButtons')||pg.querySelector('.detailPagePrimaryContainer');
if(!host)return;
loadMap(id,function(map){
if(!map)return;
if(pg.querySelector('.sf-ra-detail'))return;
var b=document.createElement('button');
b.type='button';
/* Match sf-infobtn's shape exactly, NOT Jellyfin's own play/download buttons.
   Those carry `button-flat`, and the theme hides every .button-flat in this row
   by default (Jellyfin un-hides the ones an item supports) -- so a new
   button-flat renders display:none forever. Verified live: our button existed in
   the DOM with 0x0 while the identically-placed .sf-infobtn was 42x42. */
b.className='detailButton emby-button sf-ra-detail';
b.title='Read along';
b.innerHTML='<span class="material-icons detailButton-icon" aria-hidden="true">menu_book</span>';
b.addEventListener('click',function(e){
e.preventDefault();e.stopPropagation();
RA.pendingId=id;
open_(id);
});
host.appendChild(b);
});
}
function entry(){
/* detailEntry() is DELIBERATELY not called: in the simplified sf-atv action row
   it lands beside Play and was tapped by mistake when trying to start a book.
   Re-enable only with a label and clear separation from Play. */
if(!isBook())return;
var id=nowId();
if(!id)return;
loadMap(id,function(map){
if(!map)return;
var bars=document.querySelectorAll('.nowPlayingBar'),i,bar=null;
for(i=0;i<bars.length;i++)if(bars[i].getClientRects().length){bar=bars[i];break;}
if(!bar||bar.querySelector('.sf-ra-btn'))return;
var host=bar.querySelector('.nowPlayingBarRight')||bar.querySelector('.nowPlayingBarCenter')||bar;
var b=document.createElement('button');
b.type='button';
b.className='paper-icon-button-light sf-ra-btn';
b.title='Read along';
b.innerHTML='<span class="material-icons" aria-hidden="true">menu_book</span>';
b.addEventListener('click',function(e){e.preventDefault();e.stopPropagation();open_();});
host.insertBefore(b,host.firstChild);
});
}

/* ---- the tick ---- */
var lastPaint=0;
function tick(force){
try{
entry();
if(!isOpen())return;
var map=RA.map;
if(!map){close();return;}
/* the book changed underneath us */
var live=nowId();
/* Opened from the detail page, nothing playing yet: hold the page open at the
   top of the book rather than slamming it shut. Only a DIFFERENT book playing
   means this reader is stale. */
if(live&&live!==RA.id){close();return;}
if(!live){
/* sf-ra-blank-fix: this used to `return` here, which skipped renderWindow
   entirely -- so opening the reader before pressing play showed an empty page
   with only the toolbar. Make sure there is text on screen first. */
if(RA.idx<0)RA.idx=0;
if(RA.winFrom<0)renderWindow(true); else paintActive(false);
return;
}
var t=sfRaTime();
var i=findIdx(map,t);
if(i<0)i=0;
if(i!==RA.idx||force){
RA.idx=i;
if(i<RA.winFrom+10||i>RA.winTo-10)renderWindow(false);
else paintActive(true);
}
}catch(e){}
}
/* sf-ab-readalong: the audiobook control cluster lives in a different IIFE, so
   give it one explicit way in rather than duplicating the reader there. */
try{window.__sfRaOpen=function(id){open_(id);};}catch(e){}
setInterval(function(){tick(false);},250);
document.addEventListener('keydown',function(e){
if(e.key==='Escape'&&isOpen())close();
});
})();</script>"""
