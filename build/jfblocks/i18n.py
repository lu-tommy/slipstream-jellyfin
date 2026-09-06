"""jfblocks/i18n.py -- payload constants lifted out of jf_patch.py.

Each constant's source text (and its comments) is byte-identical to the
monolith; only its location changed. 11 constants.
"""

__all__ = [
    'ONELANG_MARKER',
    'ONELANG_SCRIPT',
    'PLOTI18N_SCRIPT',
    'LANGTOGGLE_MARKER',
    'LANGTOGGLE_SCRIPT',
    'SUBLANG_MARKER',
    'SUBLANG_SCRIPT',
    'I18N_MARKER',
    'I18N_SCRIPT',
    'TITLEI18N_MARKER',
    'TITLEI18N_SCRIPT',
]



ONELANG_MARKER = 'sf-sub-onelang'
# Collapse duplicate English subtitle tracks in the picker (2026-08-27).
# the admin: "for a lot of my shows i have like multiple english subs ... we dont
# need multiple english subs."
#
# Measured: 3048 items carry 2+ English subtitle tracks (one Better Call Saul
# episode has EIGHT: English, English SDH, English FORCED, the same three again
# as PGSSUB, and two commentary tracks). Almost all of them are EMBEDDED, so
# removing them would mean remuxing thousands of files -- not worth it. Only 195
# external sidecars were genuinely redundant. So this hides, it does not delete;
# drop the block and every track is back.
#
# Keep rule: EXACTLY ONE entry PER LANGUAGE, labelled with just the language name
# ("English", "German", "Chinese") -- the admin: "can we have it simply just say
# english, german, chinese. instead of hearing impared or whatever that is
# nonsense". Originally English-only; widened to every language 2026-08-28.
# the admin first asked for plain + Forced, then
# looked at Better Call Saul and said "there are still 2 english sub tracks... we
# only want 1", so Forced is hidden too. A file whose ONLY English track is a
# forced one still keeps it -- the fallback below never lets English reach zero.
#
# TWO things this must not do, both of which the data forced:
#  1. IsForced / IsHearingImpaired are FALSE on this library even for a track
#     literally named "English FORCED" -- the flags are unset and the truth is
#     only in Title. So classify on Title first, flags second. Title is the raw
#     track name from the file, which (unlike DisplayTitle) is NOT localized, so
#     this keeps working in de/zh.
#  2. Never hide every English option. If nothing classifies as "plain" the best
#     English track of any kind is kept instead.
#
# Bonus: ranking text above image formats means the kept track is also the one
# that does NOT reload (DVDSUB is the only remaining Encode case -- see
# sf-sub-seamless), so on any item that has both, the reload becomes unreachable.
#
# Hiding is keyed on the stream INDEX via the actionsheet's data-id, never on the
# button text. An audio-track index can never collide with a subtitle index
# within one media source, so the audio menu is untouched by construction.
ONELANG_SCRIPT = ('<script>(function(){/* sf-sub-onelang */'
 'var plans={},curId=null,busy=false,last=0;'
 "function isText(c){c=String(c||'').toLowerCase();"
 "return c==='subrip'||c==='ass'||c==='ssa'||c==='mov_text'||c==='vtt'||c==='webvtt';}"
 "function ttl(s){return String(s.Title||s.DisplayTitle||'');}"
 'function isComment(s){return /commentary|director/i.test(ttl(s));}'
 'function isSDH(s){return s.IsHearingImpaired===true||/\\bsdh\\b|hearing|\\(hi\\)/i.test(ttl(s));}'
 'function isForced(s){return s.IsForced===true||/\\bforced\\b/i.test(ttl(s));}'
 "function rank(s){var c=String(s.Codec||'').toLowerCase();"
 'if(isText(c))return s.IsExternal?1:0;'
 "if(c==='pgssub')return 2;return 3;}"
 # /* sf-sub-onlylang */ the admin: "i want only german, english, and chinese subs
 # and have them named simply chinese, english, and german ... im looking at
 # movies like avatar aang and obsessions and its so many english subs".
 # The rule above was ONE PER LANGUAGE, for EVERY language -- so Obsession (19
 # subtitle tracks across 14 languages) still listed Danish, Finnish, Hindi,
 # Dutch, Norwegian, Polish, Portuguese... Restrict the list to the three that
 # are actually wanted; the one-per-language + plain-name rules then apply
 # within those.
 # Matched on the CODE, not the resolved name: the name is localized (German ->
 # "Deutsch" on a German profile), so a name test would break in exactly the
 # language it is meant to keep. Both ISO 639-2/B and /T spellings are listed
 # because this library carries both (ger AND deu, chi AND zho).
 'function wantedLang(code){'
 "var c=String(code||'').toLowerCase();"
 "if(c.indexOf('-')>0)c=c.split('-')[0];"
 "return c==='eng'||c==='en'||c==='deu'||c==='ger'||c==='de'"
 "||c==='zho'||c==='chi'||c==='zh'||c==='cmn'||c==='yue';}"
 # /* sf-sub-langname */ Intl.DisplayNames resolves EVERY code in this library,
 # including the ISO 639-2/B forms -- verified against all 51: ger AND deu both
 # give "German", chi AND zho both give "Chinese". Grouping on the resolved NAME
 # therefore merges those duplicate codes with no hand-written table, and it
 # localizes itself (Deutsch / de, German / en) so it tracks the UI language.
 # Returns '' when a code cannot be named; such tracks are left completely alone.
 'function langName(code){'
 "code=String(code||'').trim();if(!code)return '';"
 'try{'
 "var loc=document.documentElement.getAttribute('lang')||navigator.language||'en';"
 "var n=new Intl.DisplayNames([loc],{type:'language'}).of(code);"
 'if(n&&String(n).toLowerCase()!==code.toLowerCase())return n;'
 '}catch(e){}'
 "return '';}"
 'function plan(streams){'
 'var subs=[],i;for(i=0;i<(streams||[]).length;i++)'
 "if(streams[i].Type==='Subtitle')subs.push(streams[i]);"
 'var groups={},hide={},label={},nm,g,j,s2;'
 'for(i=0;i<subs.length;i++){'
 'nm=langName(subs[i].Language);'
 # no resolvable language (2614 streams have none) -- never hidden, never renamed
 'if(!nm)continue;'
 '(groups[nm]=groups[nm]||[]).push(subs[i]);}'
 # Safety: if a file has NONE of the three, leave every track exactly as it is.
 # Hiding them all would leave no subtitles to choose at all, which is worse
 # than an untidy list.
 'var anyWanted=false;'
 'for(i=0;i<subs.length;i++)if(wantedLang(subs[i].Language)){anyWanted=true;break;}'
 'for(nm in groups){'
 'if(!Object.prototype.hasOwnProperty.call(groups,nm))continue;'
 'g=groups[nm];var plain=[];'
 'if(anyWanted&&!wantedLang(g[0].Language)){'
 'for(j=0;j<g.length;j++)hide[g[j].Index]=1;continue;}'
 'for(j=0;j<g.length;j++){s2=g[j];'
 'if(isComment(s2)||isForced(s2)||isSDH(s2))continue;plain.push(s2);}'
 'var pick;'
 'if(plain.length){plain.sort(function(a,b){return rank(a)-rank(b);});pick=plain[0];}'
 'else{var any=g.slice().sort(function(a,b){return rank(a)-rank(b);});pick=any[0];}'
 'label[pick.Index]=nm;'
 'for(j=0;j<g.length;j++)if(g[j].Index!==pick.Index)hide[g[j].Index]=1;}'
 'return {hide:hide,label:label};}'
 'function learn(){'
 "if(!document.querySelector('video'))return;"
 'var A=window.ApiClient;if(!A||!A.getJSON||!A.getUrl)return;'
 'if(busy||Date.now()-last<3000)return;last=Date.now();busy=true;'
 "var dev='';try{dev=A.deviceId&&A.deviceId();}catch(e){}"
 "A.getJSON(A.getUrl('Sessions',dev?{deviceId:dev}:{})).then(function(list){"
 'busy=false;var np=null,i;'
 'for(i=0;i<(list||[]).length;i++)if(list[i].NowPlayingItem){np=list[i].NowPlayingItem;break;}'
 'if(!np||!np.Id)return;curId=np.Id;'
 'if(plans[curId])return;'
 'if(np.MediaStreams&&np.MediaStreams.length){plans[curId]=plan(np.MediaStreams);return;}'
 "var uid='';try{uid=A.getCurrentUserId();}catch(e){}"
 "A.getJSON(A.getUrl('Items/'+curId,{userId:uid})).then(function(it){"
 'plans[curId]=plan((it&&it.MediaStreams)||[]);}).catch(function(){});'
 '}).catch(function(){busy=false;});}'
 # /* sf-sub-onelang-pos */ Hiding or renaming rows AFTER the sheet is positioned
 # strands it. actionsheet centres itself on the button using its size at open
 # time -- `s=n.offsetHeight||300; r.top-=s/2` -- and writes the result as inline
 # position:fixed/top/left on the DIALOG element. That runs synchronously off
 # dialogHelper.open(), so a MutationObserver (a microtask) can never win the race
 # and pre-edit. Instead, undo the error exactly: top was anchorCentre - h0/2 and
 # should be anchorCentre - h1/2, so shifting by (h0-h1)/2 re-anchors it without
 # our ever needing to know which button opened it. Same for left, which moves
 # too -- both hiding rows and shortening labels narrow the sheet.
 # Only touches a sheet that carries an inline top -- a mobile/fullscreen sheet is
 # centred BY DESIGN and must be left alone.
 'function host(el){var n=el;while(n){'
 "if(n.style&&n.style.position==='fixed'&&n.style.top)return n;"
 'n=n.parentElement;}return null;}'
 'function apply(){'
 'var P=curId&&plans[curId];if(!P)return;'
 'var h=P.hide||{},lb=P.label||{};'
 "var sheets=document.querySelectorAll('.actionSheet'),k;"
 'for(k=0;k<sheets.length;k++){'
 'var sh=sheets[k];'
 "if(sh.getAttribute('data-sf-1lang-done')==='1')continue;"
 'var hst=host(sh),h0=hst?hst.offsetHeight:0,w0=hst?hst.offsetWidth:0;'
 "var btns=sh.querySelectorAll('.actionSheetMenuItem'),j,n=0;"
 'for(j=0;j<btns.length;j++){'
 "var id=btns[j].getAttribute('data-id');"
 'if(id===null||id==="")continue;'
 'if(h[id]){'
 "if(btns[j].getAttribute('data-sf-1lang')!=='1'){"
 "btns[j].setAttribute('data-sf-1lang','1');"
 "btns[j].style.setProperty('display','none','important');n++;}}"
 # rename the survivor to just the language. The label lives in its own node,
 # a SIBLING of the check icon, so setting it cannot disturb the tick mark.
 'else if(lb[id]){'
 "var tx=btns[j].querySelector('.actionSheetItemText');"
 'if(tx&&tx.textContent!==lb[id]){tx.textContent=lb[id];n++;}}}'
 'if(!n)continue;'
 "sh.setAttribute('data-sf-1lang-done','1');"
 'if(!hst)continue;'
 'var h1=hst.offsetHeight,w1=hst.offsetWidth;'
 'var t=parseFloat(hst.style.top)||0,l=parseFloat(hst.style.left)||0;'
 't+=(h0-h1)/2;l+=(w0-w1)/2;'
 't=Math.max(10,Math.min(t,window.innerHeight-h1-10));'
 'l=Math.max(10,Math.min(l,window.innerWidth-w1-10));'
 "hst.style.top=t+'px';hst.style.left=l+'px';}}"
 'try{setInterval(function(){try{learn();apply();}catch(e){}},900);}catch(e){}'
 'try{new MutationObserver(function(){try{apply();}catch(e){}})'
 '.observe(document.body,{childList:true,subtree:true});}catch(e){}'
 '})();</script>')


# sf-plot-i18n: the plot on a detail page, in the user's language.
# build_titles.py gave this server localized TITLES and plots were deliberately
# skipped as "a much bigger DOM surface". Measured, that turned out to be wrong:
# the detail page renders the synopsis into a single .overview node, so the
# client half is one text swap. The data half is build_plots.py -> /api/plots.
PLOTI18N_SCRIPT = r"""<script>(function(){ /* sf-plot-i18n */
/* Plots in the reader's own language, and never a frame of English first.

   sf-plot-i18n-nopaint: the swap runs inside a MutationObserver callback, which
   is delivered as a MICROTASK -- before the browser paints. Rewriting there means
   the English text exists in the DOM for less than one frame and is never drawn.
   A 600ms poll cannot do that: it is a whole visible beat late, which is exactly
   what "it flashes English then switches" was.

   When the translation is not in hand yet the text is HELD instead: hidden, the
   lookup fires, and it is revealed as German. If the lookup fails or the item has
   no translation, it is revealed as English after a short deadline, so a bridge
   outage can only ever cost a brief blank -- never a permanently empty plot.

   Everything here is inert unless the profile language is German or Chinese. */
function uid(){
try{if(window.ApiClient&&ApiClient.getCurrentUserId)return ApiClient.getCurrentUserId();}catch(e){}
try{var c=JSON.parse(localStorage.getItem('jellyfin_credentials')||'{}');
return (c.Servers&&c.Servers[0]&&c.Servers[0].UserId)||'';}catch(e){return '';}
}
function lang(){
var u=uid();
if(!u)return '';
var v='';
try{v=localStorage.getItem(u+'-language')||'';}catch(e){}
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
function norm(id){return String(id||'').split('-').join('').toLowerCase();}
function squash(x){return String(x||'').split(/\s+/).join(' ').trim();}
function same(a,b){return squash(a)===squash(b);}
/* Replace only text we can PROVE is this item's English plot. A Continue Watching
   hero shows the EPISODE synopsis while the slide still carries the SERIES id;
   without this the series plot landed on it and the hero's own enforcement loop
   fought back twice a second, forever. */
function replaceable(cur,rec){
if(!cur)return true;
if(same(cur,rec.t))return false;
if(same(cur,rec.e))return true;
/* sf-plot-i18n-clip: the hero TRUNCATES a long plot, so an exact match rejected
   every film on it -- The Princess Diaries showed 203 of its 357 characters and
   was therefore never translated. A prefix still identifies the text uniquely;
   40 characters is far past coincidence. */
var a=squash(cur).replace(/[\s.…]+$/,'');
return a.length>=40 && squash(rec.e).indexOf(a)===0;
}
var HOLD_MS=2500;
function hold(n){
if(n.getAttribute('data-sf-held'))return;
n.setAttribute('data-sf-held','1');
n.style.visibility='hidden';
setTimeout(function(){release(n);},HOLD_MS);
}
function release(n){
if(!n.getAttribute('data-sf-held'))return;
n.removeAttribute('data-sf-held');
n.style.visibility='';
}
function put(n,text){n.textContent=text;release(n);}

/* ---- maps ------------------------------------------------------------- */
var TEXT={},BUSY={},EPT={},EPBUSY={};
/* sf-plot-i18n-cachever: the cache MUST be versioned.
   Episode entries were first cached as {t,e} (plot only). When the title fields
   {n,ne} were added, every browser that had already cached the old shape kept
   serving it: the entry existed, so nothing re-fetched it, and `!rec.n` meant the
   title silently stayed English -- permanently, and only on machines that had
   used the feature before. A fresh profile worked, which is exactly why this
   survived several rounds of testing. Bump V whenever the cached shape changes. */
var CVER=2,CKEY='sf-plot-i18n-v'+CVER,LOADED='';
try{
var _k,_old=[];
for(_k in localStorage){
if(_k.indexOf('sf-plot-i18n')===0&&_k.indexOf('-v'+CVER)<0)_old.push(_k);
}
for(_k=0;_k<_old.length;_k++)localStorage.removeItem(_old[_k]);
}catch(e){}
function cacheLoad(L){
try{
var raw=localStorage.getItem(CKEY+'-'+L);
if(raw){var m=JSON.parse(raw),k;for(k in m){if(m.hasOwnProperty(k)&&TEXT[k]===undefined)TEXT[k]=m[k];}}
raw=localStorage.getItem(CKEY+'-ep-'+L);
if(raw){var e=JSON.parse(raw),j;for(j in e){if(e.hasOwnProperty(j)&&EPT[j]===undefined)EPT[j]=e[j];}}
}catch(x){}
}
function cacheSave(L){
try{
var m={},n=0,k;
for(k in TEXT){if(TEXT.hasOwnProperty(k)&&TEXT[k]){m[k]=TEXT[k];if(++n>200)break;}}
localStorage.setItem(CKEY+'-'+L,JSON.stringify(m));
var e={},j=0,q;
for(q in EPT){if(EPT.hasOwnProperty(q)&&EPT[q]){e[q]=EPT[q];if(++j>400)break;}}
localStorage.setItem(CKEY+'-ep-'+L,JSON.stringify(e));
}catch(x){}
}
function fetchInto(L,path,ids,store,busy){
var i,want=[];
for(i=0;i<ids.length;i++){
if(!ids[i]||store[ids[i]]!==undefined||busy[ids[i]])continue;
want.push(ids[i]);
}
if(!want.length)return;
want=want.slice(0,60);
for(i=0;i<want.length;i++)busy[want[i]]=1;
fetch(bridge()+path+'?lang='+encodeURIComponent(L)+'&ids='+encodeURIComponent(want.join(',')),
{headers:{'x-jellyfin-token':token()}})
.then(function(r){return r.json();})
.then(function(d){
var m=(d&&d.items)||{},j,v;
for(j=0;j<want.length;j++){v=m[want[j]];store[want[j]]=(v&&(v.t||v.n))?v:null;busy[want[j]]=0;}
cacheSave(L);
sweep();
})
.catch(function(){var j;for(j=0;j<want.length;j++){store[want[j]]=null;busy[want[j]]=0;}sweep();});
}

/* ---- the three surfaces ------------------------------------------------ */
function routeId(){
var h=location.hash||'';
if(h.indexOf('#/details')!==0)return '';
var q=h.indexOf('?');
if(q<0)return '';
var parts=h.slice(q+1).split('&'),i,kv;
for(i=0;i<parts.length;i++){kv=parts[i].split('=');if(kv[0]==='id')return decodeURIComponent(kv[1]||'');}
return '';
}
function one(n,k,store,need){
var rec=store[k],cur=(n.textContent||'').trim();
if(rec===undefined){if(cur)hold(n);need.push(k);return;}
if(!rec||!rec.t){release(n);return;}
if(!replaceable(cur,rec)){release(n);return;}
if(same(cur,rec.t)){release(n);return;}
put(n,rec.t);
}
function sweep(){
var L=lang();
if(!L)return;                       /* English profile: never touched */
if(LOADED!==L){LOADED=L;cacheLoad(L);}
var need=[],epneed=[],i,k,n,list;

var id=routeId();
if(id){
k=norm(id);
list=document.querySelectorAll('#itemDetailPage .overview');
for(i=0;i<list.length;i++)one(list[i],k,TEXT,need);
}
list=document.querySelectorAll('.slide[data-item-id]');
for(i=0;i<list.length;i++){
n=list[i].querySelector('.plot');
if(!n)continue;
/* A resumed show's hero shows the EPISODE synopsis under the SERIES id, so the
   episode id is what must be looked up -- the series plot would be both wrong
   and the old flicker. */
var ep=norm(list[i].getAttribute('data-sf-epid')||'');
if(ep){one(n,ep,EPT,epneed);continue;}
k=norm(list[i].getAttribute('data-item-id')||'');
if(!k)continue;
one(n,k,TEXT,need);
/* the hero rewrites .plot from data-sf-plot on a timer -- Media Bar owns that
   row, so the attribute has to carry the translation too or it is undone */
if(TEXT[k]&&TEXT[k].t&&(n.textContent||'').trim()===TEXT[k].t
   &&list[i].getAttribute('data-sf-plot')!==TEXT[k].t)
list[i].setAttribute('data-sf-plot',TEXT[k].t);
}
list=document.querySelectorAll('.sf-ml-card[data-id]');
for(i=0;i<list.length;i++){
k=norm(list[i].getAttribute('data-id')||'');
if(!k)continue;
n=list[i].querySelector('.sf-ep-ov');
if(n)one(n,k,EPT,epneed);
/* sf-plot-i18n-eptitle: the episode NAME on a show page. The translation was
   already in the episode index -- sf-t18n-ep only ever swept the "S1:E1 - name"
   card, and this row renders the name into its own .sf-ep-title, which nothing
   visited. The string was never missing; the selector list was. */
var tn=list[i].querySelector('.sf-ep-title');
if(tn){
var rec=EPT[k],cur=(tn.textContent||'').trim();
if(rec===undefined){if(cur)hold(tn);if(epneed.indexOf(k)<0)epneed.push(k);}
else if(!rec||!rec.n)release(tn);
else if(same(cur,rec.n))release(tn);
else if(!cur||same(cur,rec.ne))put(tn,rec.n);
else release(tn);
}
}
if(need.length)fetchInto(L,'/api/plots',need,TEXT,BUSY);
if(epneed.length)fetchInto(L,'/api/epplots',epneed,EPT,EPBUSY);
}

/* Microtask-timed: this is what keeps English off the screen. The 600ms timer
   stays only as a safety net for anything the observer cannot see. */
var pending=false;
function schedule(){
if(pending)return;
pending=true;
Promise.resolve().then(function(){pending=false;try{sweep();}catch(e){}});
}
/* sf-plot-i18n-lazyobs: a whole-document observer is not free -- one of those
   cost 1.5s of scripting on this client before. It is therefore installed ONLY
   for a German or Chinese profile, and only once, so an English profile carries
   no observer and no sweeps at all. */
var OBS=null;
function arm(){
if(OBS||!lang())return;
try{
OBS=new MutationObserver(schedule);
OBS.observe(document.documentElement,{childList:true,subtree:true,characterData:true});
}catch(e){}
}
setInterval(function(){try{arm();sweep();}catch(e){}},600);
arm();
schedule();
})();</script>"""


LANGTOGGLE_MARKER = 'sf-lang-toggle'
LANGTOGGLE_SCRIPT = """<script>(function(){ /* sf-lang-toggle */
var LANGS=[['en-US','English','EN'],['de','Deutsch','DE'],['zh-CN','\u4e2d\u6587','\u4e2d']];
/* sf-lang-badge: the corner badge was fed label(), i.e. the FULL display name
   -- 'English' rendered at 9px in a 2px-inset corner of a 36px button, which
   measured 31.8px wide and ran straight across the globe glyph. The MENU still
   shows full names; only the badge uses the short code. */
function shortlbl(code){
for(var i=0;i<LANGS.length;i++)if(LANGS[i][0]===code)return LANGS[i][2]||LANGS[i][1];
return 'EN';
}
function uid(){
try{if(window.ApiClient&&ApiClient.getCurrentUserId)return ApiClient.getCurrentUserId();}catch(e){}
try{var c=JSON.parse(localStorage.getItem('jellyfin_credentials')||'{}');
return (c.Servers&&c.Servers[0]&&c.Servers[0].UserId)||'';}catch(e){return '';}
}
function key(){var u=uid();return u?(u+'-language'):'';}
function cur(){
try{var v=localStorage.getItem(key());return v||'en-US';}catch(e){return 'en-US';}
}
function label(code){
for(var i=0;i<LANGS.length;i++)if(LANGS[i][0]===code)return LANGS[i][1];
return 'English';
}
function apply(code){
var k=key();
if(!k)return;
try{
if(code==='en-US')localStorage.setItem(k,'en-US');
else localStorage.setItem(k,code);
}catch(e){}
/* Jellyfin reads the language once at boot, so a reload is how its own
   settings page applies the change too. */
location.reload();
}
function closeMenu(){
var m=document.querySelectorAll('.sf-lang-menu'),i;
for(i=0;i<m.length;i++)if(m[i].parentNode)m[i].parentNode.removeChild(m[i]);
}
function openMenu(anchor){
closeMenu();
var m=document.createElement('div');
m.className='sf-lang-menu';
var now=cur(),i;
for(i=0;i<LANGS.length;i++){
(function(code,name){
var b=document.createElement('button');
b.type='button';
b.className='sf-lang-item'+(code===now?' sf-lang-on':'');
b.textContent=name;
b.addEventListener('click',function(e){
e.preventDefault();e.stopPropagation();
closeMenu();
if(code!==now)apply(code);
});
m.appendChild(b);
})(LANGS[i][0],LANGS[i][1]);
}
document.body.appendChild(m);
var r=anchor.getBoundingClientRect();
var left=r.left+r.width/2-m.offsetWidth/2;
if(left<8)left=8;
if(left+m.offsetWidth>window.innerWidth-8)left=window.innerWidth-m.offsetWidth-8;
m.style.left=left+'px';
m.style.top=(r.bottom+8)+'px';
setTimeout(function(){
document.addEventListener('click',function once(){closeMenu();document.removeEventListener('click',once,true);},true);
},0);
}
function build(){
var bars=document.querySelectorAll('.skinHeader .headerRight'),i;
for(i=0;i<bars.length;i++){
if(bars[i].querySelector('.sf-lang-btn'))continue;
var b=document.createElement('button');
b.type='button';
b.className='headerButton headerButtonRight paper-icon-button-light sf-lang-btn';
b.title='Language';
b.innerHTML='<span class="material-icons">language</span><span class="sf-lang-code"></span>';
b.addEventListener('click',function(e){
e.preventDefault();e.stopPropagation();
openMenu(e.currentTarget);
});
bars[i].insertBefore(b,bars[i].firstChild);
}
var tags=document.querySelectorAll('.sf-lang-code');
for(i=0;i<tags.length;i++)tags[i].textContent=shortlbl(cur());
}
setInterval(function(){try{build();}catch(e){}},800);
})();</script>"""

# --- sf-sub-lang (2026-08-29) ------------------------------------------------
# the admin: "german users default to german subtitles and chinese users default to
# chinese subs. english users default to english subs. and we can tell based on
# which language a user has selected from the header".
#
# The header toggle stores the choice in localStorage as `<uid>-language`
# ('en-US' | 'de' | 'zh-CN'), so it is a BROWSER preference -- the server cannot
# read it and this can NOT be backfilled by a script on the NAS. Mirror it onto
# the Jellyfin USER instead (SubtitleLanguagePreference), which is the field that
# actually picks a subtitle track, and which then applies on every client the
# account touches -- phone and TV as well as this browser.
#
# Codes are ISO 639-2/T exactly as the library tags the streams: sampled 80 films
# and the subtitle languages are eng / zho / deu -- NOT ger or chi. (Joey's
# account was already on 'zho', which confirms the shape.) Getting this wrong is
# silent: a preference that matches no stream simply never applies.
#
# sf-lang-toggle's apply() ends in location.reload(), so syncing once per load
# also covers the moment of switching -- no need to hook the menu itself.
#
# NO stored language = do nothing. Returning 'eng' as a default would overwrite
# an account that was set deliberately on the server (Joey, 'zho') the first time
# that user opened a browser that had never touched the toggle.
#
# SubtitleMode is deliberately left alone: 7 of the 9 accounts are already
# 'Always', and "should subtitles appear at all" is a different decision from
# "which language", one a user on 'None' has already made.
SUBLANG_MARKER = 'sf-sublang'
SUBLANG_SCRIPT = """<script>(function(){ /* sf-sublang */
function uid(){
try{if(window.ApiClient&&ApiClient.getCurrentUserId)return ApiClient.getCurrentUserId();}catch(e){}
try{var c=JSON.parse(localStorage.getItem('jellyfin_credentials')||'{}');
return (c.Servers&&c.Servers[0]&&c.Servers[0].UserId)||'';}catch(e){return '';}
}
function want(){
var u=uid();
if(!u)return '';
var v='';
try{v=localStorage.getItem(u+'-language')||'';}catch(e){}
if(!v)return '';
if(v.indexOf('zh')===0)return 'zho';
if(v.indexOf('de')===0)return 'deu';
return 'eng';
}
/* sublang-retrycap (2026-08-29): a FAILED write used to be retried on every
   800ms tick for the whole 40-tick window, i.e. up to 40 POSTs to
   /Users/{id}/Configuration per page load. Jellyfin's DB is SQLite, and under
   IO pressure that write contends: the log showed 40 'database table is
   locked: Users' errors, all inside one hour, all from this loop retrying
   during testing. Two attempts is plenty -- the next page load tries again
   anyway, and the preference only ever needs writing when it changes. */
var inflight=false,ok=false,fails=0;
function sync(){
if(ok||inflight||fails>=2)return;
var u=uid(),w=want();
if(!u||!w)return;
var ac=window.ApiClient;
if(!ac||!ac.getUser||!ac.ajax||!ac.getUrl)return;
inflight=true;
ac.getUser(u).then(function(usr){
var cfg=(usr&&usr.Configuration)||null;
if(!cfg){inflight=false;return;}
if(cfg.SubtitleLanguagePreference===w){ok=true;inflight=false;return;}
cfg.SubtitleLanguagePreference=w;
return ac.ajax({type:'POST',url:ac.getUrl('Users/'+u+'/Configuration'),
data:JSON.stringify(cfg),contentType:'application/json'})
.then(function(){ok=true;inflight=false;});
}).catch(function(){inflight=false;fails++;});
}
var tries=0;
var t=setInterval(function(){tries++;sync();if(ok||fails>=2||tries>25)clearInterval(t);},800);
sync();
})();</script>"""


I18N_MARKER = 'sf-ui-i18n'
I18N_SCRIPT = """<script>(function(){ /* sf-ui-i18n */
var MAP={
'de':{
'User':'Benutzer',
'Quick Connect':'Schnellverbindung',
'Choose from icons':'Symbol ausw\u00e4hlen','Profile':'Profil','Display':'Anzeige','Playback':'Wiedergabe','Subtitles':'Untertitel','Controls':'Steuerung','Sign Out':'Abmelden','Theme':'Design','Google Cast Version':'Google Cast-Version','Advanced Settings (Jellyfin Enhanced)':'Erweiterte Einstellungen (Jellyfin Enhanced)',

'Album':'Album',
/* sf-ab-i18n: the audiobook controls and the whole sleep-timer MENU were
   hardcoded English in every language -- measured in de AND zh-CN. The sweep
   already translates [title] globally, so these only ever needed keys. */
'Artists you have not heard':'Noch nicht geh\u00f6rt',
'Back 30 seconds':'30 Sekunden zur\u00fcck','Forward 30 seconds':'30 Sekunden vor',
'Playback speed':'Wiedergabegeschwindigkeit','Sleep timer':'Einschlaftimer',
'Cast':'\u00dcbertragen','Close':'Schlie\u00dfen',
'Off':'Aus','5 minutes':'5 Minuten','10 minutes':'10 Minuten','15 minutes':'15 Minuten',
'30 minutes':'30 Minuten','45 minutes':'45 Minuten','1 hour':'1 Stunde',
'End of chapter':'Kapitelende',
'Add to your library':'Zu deiner Bibliothek hinzuf\u00fcgen',
'Continue Watching':'Weiterschauen','Next Up':'Als N\u00e4chstes','My List':'Meine Liste',
'Watchlist':'Merkliste','Bookmarks':'Lesezeichen','Favorites':'Favoriten',
'Play':'Abspielen','Resume':'Fortsetzen','Shuffle':'Zufall','More Info':'Mehr Infos',
'Lyrics':'Liedtext','Up Next':'Als N\u00e4chstes','Made for you':'F\u00fcr dich','Read along':'Mitlesen','Sleep timer':'Sleep-Timer','Playback speed':'Wiedergabegeschwindigkeit','Next chapter':'N\u00e4chstes Kapitel','Previous chapter':'Vorheriges Kapitel',
'Live Sports':'Live-Sport','Movies & TV':'Filme & Serien','More':'Mehr','Audiobook':'H\u00f6rbuch','Continue listening':'Weiterh\u00f6ren','Recently added':'K\u00fcrzlich hinzugef\u00fcgt','Leaving Soon':'Bald nicht mehr verf\u00fcgbar','__leavedays':' Tage','today':'heute','Favorite it to keep':'Favorisieren zum Behalten','__tokeep':'zum Behalten','Mix':'Mix','Bookmark this moment':'Diesen Moment merken','No bookmarks yet':'Noch keine Lesezeichen','__tracks':' Titel','Deep Cuts':'Verborgene Perlen','Songs':'Titel','Artists':'K\u00fcnstler','Playlists':'Playlisten',
'Trending Movies':'Angesagte Filme','Recently Added Movies':'K\u00fcrzlich hinzugef\u00fcgte Filme',
'Recently Added Shows':'K\u00fcrzlich hinzugef\u00fcgte Serien','Discover':'Entdecken',
'Recently Added Books':'K\u00fcrzlich hinzugef\u00fcgte H\u00f6rb\u00fccher','Jump Back In':'Weiterh\u00f6ren',
'Home':'Startseite','Remove':'Entfernen','Remove from Continue Watching':'Aus \u201eWeiter ansehen\u201c entfernen','Audiobooks':'H\u00f6rb\u00fccher','w:Action':'Action','w:Heroes':'Helden','w:Comedy':'Comedy','w:Comfort':'Wohlf\u00fchl','w:Crime':'Krimi','w:Thriller':'Thriller','w:Drama':'Drama','w:Romance':'Romantik','w:Family':'Familie','w:Disney':'Disney','w:Animation':'Animation','w:Station':'Kanal','w:Movie':'Film','w:Night':'abend','w:Prestige':'Prestige','w:Kids':'Kinder','w:Sports':'Sport','w:Music':'Musik','w:Documentary':'Dokumentation','w:Horror':'Horror','w:Fantasy':'Fantasy','w:Adventure':'Abenteuer','w:Classics':'Klassiker','w:Holiday':'Feiertage','w:Anime':'Anime','w:Mystery':'Mystery','w:War':'Krieg','w:Western':'Western','w:Musical':'Musical','w:Teen':'Teen','LIVE':'LIVE','Action & Heroes':'Action & Helden','Animation Station':'Animation','Comfort Comedy':'Wohlf\u00fchl-Comedy','Crime & Thriller':'Krimi & Thriller','Disney & Family':'Disney & Familie','Movie Night':'Filmabend','Prestige Drama':'Prestige-Drama','Romance & Drama':'Romantik & Drama','Sci-Fi & Mind-Bend':'Sci-Fi & Mindbender','Pick up where you left off':'Weiter, wo du aufgehört hast','Enhanced Panel':'Erweitertes Panel','Plugin Settings':'Plugin-Einstellungen','Good morning':'Guten Morgen','Good afternoon':'Guten Tag','Good evening':'Guten Abend','Rating':'Altersfreigabe','Programs':'Programme','Guide':'Fernsehprogramm','Channels':'Kan\u00e4le','Live TV':'Live-TV','Play':'Abspielen','Menu':'Men\u00fc','Music':'Musik','Language':'Sprache','Search':'Suche','Back':'Zur\u00fcck','What to Watch':'Was ansehen','Folders':'Ordner','Audio Books':'H\u00f6rb\u00fccher','Books':'B\u00fccher','Recordings':'Aufnahmen','Modular Home':'Modulare Startseite','Hidden Content':'Versteckte Inhalte','Favorite Albums':'Lieblingsalben','Favorite Albums':'Lieblingsalben','Your Top Artists':'Deine Top-K\u00fcnstler','Resume':'Fortsetzen','Shuffle':'Zufallswiedergabe','Play All':'Alle abspielen','__mix':'-Mix','Sports':'Sport','My Stuff':'Meine Sachen','Chapters':'Kapitel',
/* sf-i18n-gaps (2026-08-20): found by sweeping every visible heading, button
   and [title] on home/music/movies in each language and flagging anything still
   in English. These were the real misses. */
'Last played':'Zuletzt gespielt','Cast to Device':'Auf Ger\u00e4t \u00fcbertragen',
'Your Playlists':'Deine Playlisten','Cancel':'Abbrechen','Create':'Erstellen',
'Start a mix':'Mix starten','__inlib':' in deiner Bibliothek',
'Continue':'Weiter','Recently Added':'K\u00fcrzlich hinzugef\u00fcgt','Suggestions':'Vorschl\u00e4ge',
/* sf-mus-listennow: 'Suggestions' stays -- Jellyfin uses it elsewhere. This is
   the new music landing tab. Apple Music's own German wording. */
'Listen Now':'Jetzt h\u00f6ren',
/* sf-mus-nav: the four-tab music navigation. Apple Music's own German wording
   for the tabs themselves, so it reads as the app it is modelled on. */
'New':'Neu','Radio':'Radio','Library':'Mediathek','Albums':'Alben',
'Your mixes':'Deine Mixe','Artist stations':'K\u00fcnstler-Sender','New Playlist':'Neue Playlist',
'Song radio':'Song-Radio','Because you listen to':'Weil du h\u00f6rst','Radio':'Radio',
/* sf-mood-mixes: the five mood mixes are real Jellyfin playlists, so their
   names arrive in English from build_mixes.py and are translated on the way
   out like any other label. */
'Discover more from':'Mehr entdecken von','If you like':'Wenn du magst','Liked Songs':'Lieblingssongs',
'Moods':'Stimmungen','Chill':'Chill','Energy':'Energie','Feel Good':'Gute Laune',
'Focus':'Fokus','Late Night':'Sp\u00e4tabends',
'Top Artists':'Top-K\u00fcnstler','Albums':'Alben','Movies':'Filme','Shows':'Serien','Music':'Musik'
},
'zh-CN':{
'User':'\u7528\u6237',
'Quick Connect':'\u5feb\u901f\u8fde\u63a5',
'Choose from icons':'\u9009\u62e9\u5934\u50cf','Profile':'\u4e2a\u4eba\u8d44\u6599','Display':'\u663e\u793a','Playback':'\u64ad\u653e','Subtitles':'\u5b57\u5e55','Controls':'\u63a7\u5236','Sign Out':'\u9000\u51fa\u767b\u5f55','Theme':'\u4e3b\u9898','Google Cast Version':'Google Cast \u7248\u672c','Advanced Settings (Jellyfin Enhanced)':'\u9ad8\u7ea7\u8bbe\u7f6e (Jellyfin Enhanced)',
'Live Sports':'\u4f53\u80b2\u76f4\u64ad','Movies & TV':'\u5f71\u89c6','More':'\u66f4\u591a','Audiobook':'\u6709\u58f0\u4e66','Continue listening':'\u7ee7\u7eed\u6536\u542c','Recently added':'\u6700\u8fd1\u6dfb\u52a0','Leaving Soon':'\u5373\u5c06\u4e0b\u67b6','__leavedays':'\u5929','today':'\u4eca\u5929','Favorite it to keep':'\u6536\u85cf\u5373\u53ef\u4fdd\u7559','__tokeep':'\u5373\u53ef\u4fdd\u7559','Mix':'\u6df7\u97f3','Bookmark this moment':'\u6807\u8bb0\u6b64\u523b','No bookmarks yet':'\u6682\u65e0\u4e66\u7b7e','__tracks':'\u9996',
'Album':'\u4e13\u8f91',
'Artists you have not heard':'\u5c1a\u672a\u542c\u8fc7\u7684\u827a\u4eba',
'Back 30 seconds':'\u540e\u9000 30 \u79d2','Forward 30 seconds':'\u5feb\u8fdb 30 \u79d2',
'Playback speed':'\u64ad\u653e\u901f\u5ea6','Sleep timer':'\u7761\u7720\u5b9a\u65f6\u5668',
'Cast':'\u6295\u5c4f','Close':'\u5173\u95ed',
'Off':'\u5173','5 minutes':'5 \u5206\u949f','10 minutes':'10 \u5206\u949f','15 minutes':'15 \u5206\u949f',
'30 minutes':'30 \u5206\u949f','45 minutes':'45 \u5206\u949f','1 hour':'1 \u5c0f\u65f6',
'End of chapter':'\u672c\u7ae0\u7ed3\u675f',
'Add to your library':'\u6dfb\u52a0\u5230\u60a8\u7684\u5a92\u4f53\u5e93',
'Continue Watching':'\u7ee7\u7eed\u89c2\u770b','Next Up':'\u63a5\u4e0b\u6765','My List':'\u6211\u7684\u7247\u5355',
'Watchlist':'\u60f3\u770b','Bookmarks':'\u4e66\u7b7e','Favorites':'\u6536\u85cf',
'Play':'\u64ad\u653e','Resume':'\u7ee7\u7eed\u64ad\u653e','Shuffle':'\u968f\u673a\u64ad\u653e','More Info':'\u8be6\u7ec6\u4fe1\u606f',
'Lyrics':'\u6b4c\u8bcd','Up Next':'\u63a5\u4e0b\u6765','Made for you':'\u4e3a\u4f60\u63a8\u8350','Read along':'\u8fb9\u542c\u8fb9\u8bfb','Sleep timer':'\u5b9a\u65f6\u5173\u95ed','Playback speed':'\u64ad\u653e\u901f\u5ea6','Next chapter':'\u4e0b\u4e00\u7ae0','Previous chapter':'\u4e0a\u4e00\u7ae0',
'Deep Cuts':'\u6c27\u6c14\u6b4c\u5355','Songs':'\u6b4c\u66f2','Artists':'\u827a\u4eba','Playlists':'\u64ad\u653e\u5217\u8868',
'Trending Movies':'\u70ed\u95e8\u7535\u5f71','Recently Added Movies':'\u6700\u8fd1\u6dfb\u52a0\u7684\u7535\u5f71',
'Recently Added Shows':'\u6700\u8fd1\u6dfb\u52a0\u7684\u5267\u96c6','Discover':'\u53d1\u73b0',
'Recently Added Books':'\u6700\u8fd1\u6dfb\u52a0\u7684\u6709\u58f0\u4e66','Jump Back In':'\u7ee7\u7eed\u6536\u542c',
'Home':'\u9996\u9875','Remove':'\u79fb\u9664','Remove from Continue Watching':'\u4ece\u7ee7\u7eed\u89c2\u770b\u4e2d\u79fb\u9664','Audiobooks':'\u6709\u58f0\u4e66','__amp':'\u4e0e','w:Action':'\u52a8\u4f5c','w:Heroes':'\u82f1\u96c4','w:Comedy':'\u559c\u5267','w:Comfort':'\u8f7b\u677e','w:Crime':'\u72af\u7f6a','w:Thriller':'\u60ca\u609a','w:Drama':'\u5267\u60c5','w:Romance':'\u7231\u60c5','w:Family':'\u5bb6\u5ead','w:Disney':'\u8fea\u58eb\u5c3c','w:Animation':'\u52a8\u753b','w:Station':'\u9891\u9053','w:Movie':'\u7535\u5f71','w:Night':'\u4e4b\u591c','w:Prestige':'\u7ecf\u5178','w:Kids':'\u513f\u7ae5','w:Sports':'\u4f53\u80b2','w:Music':'\u97f3\u4e50','w:Documentary':'\u7eaa\u5f55\u7247','w:Horror':'\u6050\u6016','w:Fantasy':'\u5947\u5e7b','w:Adventure':'\u5192\u9669','w:Classics':'\u7ecf\u5178','w:Holiday':'\u8282\u65e5','w:Anime':'\u52a8\u6f2b','w:Mystery':'\u60ac\u7591','w:War':'\u6218\u4e89','w:Western':'\u897f\u90e8','w:Musical':'\u97f3\u4e50\u5267','w:Teen':'\u9752\u6625','LIVE':'\u76f4\u64ad','Action & Heroes':'\u52a8\u4f5c\u4e0e\u82f1\u96c4','Animation Station':'\u52a8\u753b\u9891\u9053','Comfort Comedy':'\u8f7b\u677e\u559c\u5267','Crime & Thriller':'\u72af\u7f6a\u4e0e\u60ca\u609a','Disney & Family':'\u8fea\u58eb\u5c3c\u4e0e\u5bb6\u5ead','Movie Night':'\u7535\u5f71\u4e4b\u591c','Prestige Drama':'\u7ecf\u5178\u5267\u96c6','Romance & Drama':'\u7231\u60c5\u4e0e\u5267\u60c5','Sci-Fi & Mind-Bend':'\u79d1\u5e7b\u4e0e\u70e7\u8111','Movie Night ':'\u7535\u5f71\u4e4b\u591c','Pick up where you left off':'\u7ee7\u7eed\u4e0a\u6b21\u7684\u6536\u542c','Enhanced Panel':'\u589e\u5f3a\u9762\u677f','Plugin Settings':'\u63d2\u4ef6\u8bbe\u7f6e','Good morning':'\u65e9\u4e0a\u597d','Good afternoon':'\u4e0b\u5348\u597d','Good evening':'\u665a\u4e0a\u597d','Rating':'\u5206\u7ea7','Programs':'\u8282\u76ee','Guide':'\u6307\u5357','Channels':'\u9891\u9053','Live TV':'\u76f4\u64ad\u7535\u89c6','Play':'\u64ad\u653e','Menu':'\u83dc\u5355','Music':'\u97f3\u4e50','Language':'\u8bed\u8a00','Search':'\u641c\u7d22','Back':'\u8fd4\u56de','What to Watch':'\u770b\u4ec0\u4e48','Folders':'\u6587\u4ef6\u5939','Audio Books':'\u6709\u58f0\u4e66','Books':'\u4e66\u7c4d','Recordings':'\u5f55\u5236','Modular Home':'\u6a21\u5757\u5316\u4e3b\u9875','Hidden Content':'\u9690\u85cf\u5185\u5bb9','Favorite Albums':'\u6536\u85cf\u7684\u4e13\u8f91','Favorite Albums':'\u6536\u85cf\u7684\u4e13\u8f91','Your Top Artists':'\u4f60\u6700\u5e38\u542c\u7684\u827a\u4eba','Resume':'\u7ee7\u7eed\u64ad\u653e','Shuffle':'\u968f\u673a\u64ad\u653e','Play All':'\u64ad\u653e\u5168\u90e8','__mix':'\u7cbe\u9009','Sports':'\u4f53\u80b2','My Stuff':'\u6211\u7684\u5185\u5bb9','Chapters':'\u7ae0\u8282',
'Last played':'\u6700\u8fd1\u64ad\u653e','Cast to Device':'\u6295\u5c4f\u5230\u8bbe\u5907',
'Your Playlists':'\u4f60\u7684\u64ad\u653e\u5217\u8868','Cancel':'\u53d6\u6d88','Create':'\u521b\u5efa',
'Start a mix':'\u5f00\u59cb\u5408\u8f91','__inlib':'\uff08\u5728\u4f60\u7684\u5a92\u4f53\u5e93\uff09',
'Continue':'\u7ee7\u7eed','Recently Added':'\u6700\u8fd1\u6dfb\u52a0','Suggestions':'\u63a8\u8350',
/* sf-mus-listennow: Apple Music's own zh-CN wording for Listen Now. */
'Listen Now':'\u7acb\u5373\u8046\u542c',
/* sf-mus-nav: Apple Music's own zh-CN wording for the tabs. */
'New':'\u6700\u65b0','Radio':'\u5e7f\u64ad','Library':'\u8d44\u6599\u5e93','Albums':'\u4e13\u8f91',
'Home':'\u4e3b\u9875','Artists':'\u827a\u4eba','Songs':'\u6b4c\u66f2','Playlists':'\u64ad\u653e\u5217\u8868',
'Your mixes':'\u4f60\u7684\u6df7\u97f3','Artist stations':'\u827a\u4eba\u7535\u53f0','New Playlist':'\u65b0\u5efa\u64ad\u653e\u5217\u8868',
'Song radio':'\u6b4c\u66f2\u7535\u53f0','Because you listen to':'\u56e0\u4e3a\u4f60\u5728\u542c',
'Discover more from':'\u53d1\u73b0\u66f4\u591a','If you like':'\u5982\u679c\u4f60\u559c\u6b22','Liked Songs':'\u5df2\u559c\u6b22\u7684\u6b4c\u66f2',
'Moods':'\u5fc3\u60c5','Chill':'\u653e\u677e','Energy':'\u6d3b\u529b','Feel Good':'\u597d\u5fc3\u60c5',
'Focus':'\u4e13\u6ce8','Late Night':'\u6df1\u591c',
'Top Artists':'\u70ed\u95e8\u827a\u4eba','Albums':'\u4e13\u8f91','Movies':'\u7535\u5f71','Shows':'\u5267\u96c6','Music':'\u97f3\u4e50'
}};
function uid(){
try{if(window.ApiClient&&ApiClient.getCurrentUserId)return ApiClient.getCurrentUserId();}catch(e){}
try{var c=JSON.parse(localStorage.getItem('jellyfin_credentials')||'{}');
return (c.Servers&&c.Servers[0]&&c.Servers[0].UserId)||'';}catch(e){return '';}
}
function lang(){
var u=uid();
if(!u)return '';
var v='';
try{v=localStorage.getItem(u+'-language')||'';}catch(e){}
if(v==='zh-TW'||v==='zh-HK')v='zh-CN';
return v;
}
/* One translator for BOTH text nodes and attributes. The generated strings --
   "Continue S1 E14", "Rating: TV-14", "Good morning, the admin", "Pop Mix" -- can
   never be exact keys, and the attribute pass previously did exact lookups only,
   so a hero tooltip stayed English even when its label did not. */
function sfT(t,tbl){
if(!t)return null;
if(tbl[t])return tbl[t];
var m;
if(tbl['Continue']&&(m=/^Continue(\s+.*)$/.exec(t)))return tbl['Continue']+m[1];
if(tbl['Rating']&&(m=/^Rating:\s*(.+)$/.exec(t)))return tbl['Rating']+': '+m[1];
if((m=/^(Good (?:morning|afternoon|evening))(,.*)?$/.exec(t))&&tbl[m[1]])
return tbl[m[1]]+(m[2]||'');
if(tbl['__mix']&&/ Mix$/.test(t))return t.replace(/ Mix$/,tbl['__mix']);
/* sf-i18n-gaps: two more generated shapes that could never be exact keys.
   "Play Deep Cuts" (a mix tile's tooltip) and "<Artist> in your library" (the
   search page's owned-albums heading) both stayed English in de AND zh-CN.
   The tail is run back through the table so a known mix name translates too. */
if(tbl['Play']&&(m=/^Play\s+(.+)$/.exec(t)))return tbl['Play']+' '+(tbl[m[1]]||m[1]);
if(tbl['__inlib']&&(m=/^(.+)\s+in your library$/.exec(t)))return m[1]+tbl['__inlib'];
/* Compositional fallback, so a channel added LATER translates with nothing to
   edit. ErsatzTV channel names are built from a small genre vocabulary
   ("Crime & Thriller", "Disney & Family"), and each word is stored under a
   'w:' prefix. Only used when EVERY word is known -- a partial translation
   reads worse than leaving it alone. */
var parts=String(t).split(/(\s*&\s*|\s+)/),outp=[],any=false,okAll=true,pi;
if(parts.length>1&&parts.length<=9){
for(pi=0;pi<parts.length;pi++){
var seg=parts[pi];
if(/^(\s*&\s*|\s+)$/.test(seg)){
/* Chinese does not put '&' between words -- '\u6050\u6016 & \u60ac\u7591' reads wrong */
outp.push((/&/.test(seg)&&tbl['__amp'])?tbl['__amp']:seg);continue;}
var w=tbl['w:'+seg];
if(w){outp.push(w);any=true;}
else{okAll=false;break;}
}
if(any&&okAll)return outp.join('');
}
return null;
}
/* Jellyfin's OWN zh-CN string for "1-100 of 616" has its two placeholders
   swapped, so every library page (Movies, Shows, Music...) reads
   "616 \u7684 1-100" -- literally "of 616, 1-100". Verified side by side:
   en "1-100 of 616", de "1-100 von 616", zh "616 \u7684 1-100".
   Rewritten in place from the rendered numbers, so it holds for any page size.
   Self-guarding: once rewritten the text no longer matches the pattern. */
function sfFixPaging(L){
if(String(L||'').toLowerCase().indexOf('zh')!==0)return;
var nodes=document.querySelectorAll('.listPaging span'),i,n,t,m;
for(i=0;i<nodes.length;i++){
n=nodes[i];
if(n.children.length)continue;
t=(n.textContent||'').trim();
m=/^(\d+)\s*\u7684\s*(\d+)\s*[-\u2013]\s*(\d+)$/.exec(t);
if(!m)continue;
n.textContent='\u7b2c '+m[2]+'-'+m[3]+' \u9879\uff0c\u5171 '+m[1]+' \u9879';
}
}
function sweep(){
var L=lang();
try{sfFixPaging(L);}catch(e){}
if(!L||L==='en-US'||!MAP[L])return;
var tbl=MAP[L];
/* .navMenuOptionText covers the drawer, where our own entries (Watchlist,
   Bookmarks, Swiparr, LUSERTUBE) are plain English -- Jellyfin's own entries are
   already translated by then, so they simply do not match a key here.
   .play-text is the hero's Play / Resume label, which is Media Bar's markup and
   therefore never saw Jellyfin's translation layer either. */
/* Tooltips: the header icons (Menu, Music, Language, Search, Back, Home) carry
   their label in a title ATTRIBUTE, which this sweep never looked at -- so every
   icon in the app announced itself in English in every language, including to a
   screen reader. Same table, applied to the attribute. */
var tt=document.querySelectorAll('[title]'),ti,tn,tv,tr;
for(ti=0;ti<tt.length;ti++){
tn=tt[ti];tv=(tn.getAttribute('title')||'').trim();
tr=sfT(tv,tbl);
if(tr){tn.setAttribute('title',tr);
if(tn.getAttribute('aria-label')===tv)tn.setAttribute('aria-label',tr);}
}
var nodes=document.querySelectorAll(
'#myPreferencesMenuPage .listItemBodyText, #myPreferencesMenuPage .listItemBodyText h3, .userPreferencesPage h2, .userPreferencesPage .sectionTitle, .userPreferencesPage .selectLabel, .userPreferencesPage .inputLabel, .userPreferencesPage .checkboxLabel, .sf-mus-greet-title, .sf-mus-greet-sub, .sf-mus-hero-kicker, .sidebarHeader, .jf-fav-tab, .verticalSection .sectionTitle, .verticalSection h2, .verticalSection h3, .headerTabs button, .sf-ch-list ~ *, .sf-chapters .sectionTitle, .navMenuOptionText, .play-text, .sf-np-tab, .sf-np-album, .sf-mix-label, .sf-ab-mi, .sf-plnew-cancel, .sf-plnew-save, .sf-alb-playlab, .sf-alb-shuflab, .sf-gf-pill, .sf-syn-more, .sf-ov-more, .sf-alb-chip, .sf-mus-hero-play, .sf-mus-hero-mix, .sf-ablib-shelf .sectionTitle');
var i,n,t;
for(i=0;i<nodes.length;i++){
n=nodes[i];
/* Some headings carry a CONTROL beside their text -- Jellyseerr's "Add to your
   library" is <h2>Add to your library<button class="jellyseerr-refresh"></h2>.
   Two consequences, both handled here:
     1. textContent reads "Add to your libraryrefresh" (the icon ligature), so an
        exact-match lookup could never hit;
     2. writing textContent would DELETE the button.
   So when the label is a leading text node with element siblings, read and write
   that node alone and leave the control in place. */
var tnode=(n.firstChild&&n.firstChild.nodeType===3&&n.children&&n.children.length)?n.firstChild:null;
t=(tnode?tnode.nodeValue:(n.textContent||'')).trim();
/* No permanent stamp: Media Bar rewrites .play-text as the hero rotates between
   slides (Play vs Resume), so a card marked done once would keep the previous
   slide's label. Re-testing is cheap because a translated string is no longer a
   key in the table, so it can never be translated twice. */
var _tr=sfT(t,tbl);
if(_tr){
if(tnode)tnode.nodeValue=_tr; else n.textContent=_tr;
n.setAttribute('data-sf-i18n','1');
}else if(false&&t&&tbl['Continue']&&/^Continue\s/.test(t)){
/* Media Bar's resume label for a series is "Continue S2 E8" -- the episode
   marker is generated, so exact match can never catch it. Translate the leading
   word and leave the SxEy exactly as it is. */
var mm=/^Continue(\s+.*)$/.exec(t);
if(mm){n.textContent=tbl['Continue']+mm[1];n.setAttribute('data-sf-i18n','1');}
}else if(t&&tbl['Audiobook']&&/^Audiobook(,|$)/.test(t)){
/* composite chip -- translate the item TYPE and leave the genres alone */
n.textContent=t.replace(/^Audiobook/,tbl['Audiobook']);
n.setAttribute('data-sf-i18n','1');
}else if(t&&tbl['__tracks']&&/^\d+ tracks?$/.test(t)){
/* generated count, so never an exact key: keep the number, translate the noun */
n.textContent=t.replace(/ tracks?$/,tbl['__tracks']);
n.setAttribute('data-sf-i18n','1');
}else if(t&&tbl['__mix']&&/ Mix$/.test(t)){
/* build_mixes.py names these from a genre or a decade, so the full string is
   never a key -- translate the generated " Mix" suffix and keep the genre. */
n.textContent=t.replace(/ Mix$/,tbl['__mix']);
n.setAttribute('data-sf-i18n','1');
}
}
}
/* sf-ui-i18n-flash: every navigation REBUILDS the header pill bar with English
   labels, and a 700ms poll meant the user watched it sit in English first --
   measured "首页|Live TV|Sports|我的最爱" for 600ms on Live TV -> home, and a full
   "Home|Live TV|Sports|My Stuff" on home -> music. That is the reported "after
   every switch I see the main pill tab flash something".
   sweep() is idempotent by design (a translated string is no longer a key), so
   it is safe to run it on DOM insertion and on hashchange as well as on the
   poll. childList only, collapsed into one rAF, for the same reason as the title
   sweep: an attributes observer would re-run on every class change. */
var SFHOT='.play-text,.sectionTitle,.emby-tab-button,.navMenuOptionText,.jf-fav-tab,.sf-mus-greet-title,.sf-mus-greet-sub,.sf-np-tab,.sf-mix-label,.sidebarHeader,.sf-ab-mi,.sf-alb-playlab,.sf-alb-shuflab,.sf-gf-pill,.sf-syn-more,.sf-alb-chip';
var UIQ=false;
function sweepSoonUI(){
if(UIQ)return;
UIQ=true;
requestAnimationFrame(function(){UIQ=false;try{sweep();}catch(e){}});
}
function observeUI(){
if(!document.body){setTimeout(observeUI,50);return;}
try{
/* A rAF-debounced sweep still lets the English text PAINT once -- measured one
   frame of "Play" per ~5900 on the hero, which is the "sometimes it doesn't
   translate" report. A MutationObserver callback runs as a microtask BEFORE the
   next paint, so translating right there means the English string is never
   shown. Guarded against re-entry: our own write re-triggers the observer, but a
   translated string is no longer a key so the second pass is a no-op. */
new MutationObserver(function(m){
var txt=false,add=false,i;
for(i=0;i<m.length;i++){
if(m[i].type==='characterData')txt=true;
else if(m[i].addedNodes&&m[i].addedNodes.length)add=true;
}
/* A slide rotation REPLACES the label node rather than editing its text, so it
   arrives as an add and the debounced path let one English frame paint
   ("Continue S1 E2", measured at a rotation 14s in). Sweep synchronously for
   adds too -- but only when the added subtree actually contains something we
   translate, so the common case (cards, images) still costs nothing. */
var hot=false,j,nd;
if(add){
for(i=0;i<m.length&&!hot;i++){
for(j=0;j<m[i].addedNodes.length;j++){
nd=m[i].addedNodes[j];
if(!nd||nd.nodeType!==1)continue;
if((nd.matches&&nd.matches(SFHOT))||(nd.querySelector&&nd.querySelector(SFHOT))){hot=true;break;}
}
}
}
if(txt||hot){
if(!window.__sfSweeping){
window.__sfSweeping=true;
try{sweep();}catch(e){}
window.__sfSweeping=false;
}
return;
}
if(add)sweepSoonUI();
}).observe(document.body,{childList:true,subtree:true,characterData:true});
}catch(e){}
}
/* sf-tr-export: generated labels ("Continue S1 E2") were written in ENGLISH and
   left for the sweep to correct, which is a repaint later by construction. Expose
   the translator so the producing code can emit the final string directly -- the
   English form then never exists in the DOM at all. */
window.sfTr=function(t){
try{
var L=lang();
if(!L||L==='en-US')return t;
var tbl=MAP[L];
if(!tbl)return t;
return sfT(t,tbl)||t;
}catch(e){return t;}
};
observeUI();
window.addEventListener('hashchange',sweepSoonUI);
try{sweep();}catch(e){}
setInterval(function(){try{sweep();}catch(e){}},700);
})();</script>"""


TITLEI18N_MARKER = 'sf-title-i18n'
TITLEI18N_SCRIPT = """<script>(function(){ /* sf-title-i18n */
var MAP=null,PENDING=false;
function uid(){
try{if(window.ApiClient&&ApiClient.getCurrentUserId)return ApiClient.getCurrentUserId();}catch(e){}
try{var c=JSON.parse(localStorage.getItem('jellyfin_credentials')||'{}');
return (c.Servers&&c.Servers[0]&&c.Servers[0].UserId)||'';}catch(e){return '';}
}
function lang(){
var u=uid();
if(!u)return '';
var v='';
try{v=localStorage.getItem(u+'-language')||'';}catch(e){}
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
/* sf-t18n-cache: cards render at ~2.2s but the title map only lands after its
   own round trip, so the FIRST paint is unavoidably English. Persist the map and
   a repeat visit -- which is every visit after the first -- has it synchronously
   at t=0 and never shows an English title at all. The network copy still refreshes
   in the background, so a newly-translated title appears on the next load. */
var MAPKEY='sf-t18n-map';
function cacheGet(L){
try{
var raw=localStorage.getItem(MAPKEY+'-'+L);
if(!raw)return null;
var o=JSON.parse(raw);
if(!o||!o.items)return null;
if((Date.now()-(o.at||0))>604800000)return null;   /* a week */
return o.items;
}catch(e){return null;}
}
function cachePut(L,items){
try{
var body=JSON.stringify({at:Date.now(),items:items});
if(body.length>3000000)return;      /* never risk blowing the quota */
localStorage.setItem(MAPKEY+'-'+L,body);
}catch(e){}                          /* quota/private mode: caching is optional */
}
function load(){
if(MAP!==null||PENDING)return;
var L=lang();
var hit=L?cacheGet(L):null;
if(hit){MAP=hit;try{sweepSoon();}catch(e){}}   /* paint translated immediately */
PENDING=true;
fetch(bridge()+'/api/titles',{headers:{'x-jellyfin-token':token()}})
.then(function(r){return r.json();})
.then(function(d){MAP=(d&&d.items)||{};PENDING=false;
if(L)cachePut(L,MAP);
try{sweepSoon();}catch(e){}})
.catch(function(){if(!MAP)MAP={};PENDING=false;});
}
function norm(id){return String(id||'').split('-').join('').toLowerCase();}
/* The element that actually shows this card's title. */
function titleNode(card){
var n=card.querySelector('.cardText-first .textActionButton');
if(n)return n;
/* sf-t18n-keeplink (2026-08-29): a card title is
     <div class="cardText-first"><bdi><a href="#/details?...">Name</a></bdi></div>
   and NOT every one of those anchors carries .textActionButton. For those the
   old fallback returned the .cardText-first CONTAINER, so writing textContent
   deleted the <bdi> and the <a> with it -- the title kept its translation but
   stopped being a link: no hover underline, not clickable.
   Only ever visible in a translated language, because nothing rewrites these
   nodes in English. Measured on the Shows grid: EN 45/57 titles linked, DE
   40/72, and every unlinked German one was a title we had translated.
   The admin: "when im in german, some shows i cant click the show title".
   Write into the anchor instead -- same text, and the link survives.
   Same rule the Discover/jellyseerr path already follows for the same reason. */
n=card.querySelector('.cardText-first a');
if(n)return n;
n=card.querySelector('.cardText-first');
return n||null;
}
/* sf-t18n-episodes: an Episode/Season card's cardText-first is the SERIES name
   (verified live: first="Dragon Ball Z Kai", secondary="S1:E1 - Prologue..."),
   and the whole of Continue Watching plus Next Up is made of these -- measured
   0/36 translated on the Chinese home page while the map already held every one
   of those series. They were skipped because the card carries only data-id (the
   EPISODE id) and no data-seriesid, so the series could not be reached.

   Resolved with ONE batched lookup per group of unknown ids rather than a call
   per card, cached for the session. Each entry keeps the series' ENGLISH name as
   well, because cardText-first is only the series name in SOME layouts -- on a
   season page it is the episode title. Rewriting only when the node's current
   text is exactly that English series name means a layout where it means
   something else is left untouched instead of mislabelled. */
/* sf-t18n-ep: EPISODE names. cardText-secondary reads "S1:E1 - <episode name>",
   and only the name is translatable -- the season/episode prefix is Jellyfin's.
   So the bridge returns the English name alongside the translation and we swap
   that exact substring; if the English name is not present (a different layout,
   an already-translated node) nothing is touched.

   Source is /api/eptitles, which serves only the ids asked for: the full map is
   7425 episodes / ~930KB and must never be shipped wholesale. */
var EPT={},EPNEED={},EPBUSY=false;
/* sf-t18n-discover: the Discover row is Jellyseerr content, not library items, so
   the id-keyed title map cannot reach it. Its cards do carry data-tmdb-id +
   data-media-type, and /api/tmdbtitles turns those into localized titles via
   Jellyseerr's TMDb proxy (the HomeScreenSections plugin accepts a Language
   parameter and ignores it -- en and zh-CN return byte-identical titles). */
var TMT={},TMNEED={},TMBUSY=false;
var SER={},NEED={},SERBUSY=false,PREWARMED=false;
/* Pre-warm the episode->series map from the two queries whose rows are made
   almost entirely of episode cards (Continue Watching and Next Up), at load time
   rather than after the cards appear.

   Without this the sequence is: cards render -> tick notices them -> batch
   request -> next tick rewrites, and on this server that measured **cards at 19s,
   Chinese titles at 28s** -- nine seconds of visibly English titles on a page the
   user is already looking at. The lookup itself is fast (0.1-0.7s); the delay is
   the 700ms tick competing with the eager render of ~84 cards for the main
   thread. Starting the fetch before the cards exist takes that whole window off
   the critical path. The reactive batch below still handles every other page. */
function prewarm(){
if(PREWARMED)return;
var ac=window.ApiClient;
if(!ac||!ac.getJSON||!ac.getCurrentUserId)return;
var u=ac.getCurrentUserId();
if(!u)return;
PREWARMED=true;
function soak(r){
var L=(r&&r.Items)||[],i,it;
for(i=0;i<L.length;i++){
it=L[i];
if(it.Type==='Episode'||it.Type==='Season')
SER[norm(it.Id)]={sid:norm(it.SeriesId||''),en:(it.SeriesName||'')};
}
}
try{
ac.getJSON(ac.getUrl('Users/'+u+'/Items/Resume',
{MediaTypes:'Video',Limit:24,Fields:'SeriesId'})).then(soak).catch(function(){});
ac.getJSON(ac.getUrl('Shows/NextUp',
{userId:u,Limit:24,Fields:'SeriesId'})).then(soak).catch(function(){});
}catch(e){}
}
function resolveSeries(){
if(SERBUSY)return;
var ids=[],k;
for(k in NEED){if(NEED.hasOwnProperty(k)&&!SER[k])ids.push(k);}
if(!ids.length)return;
var ac=window.ApiClient;
if(!ac||!ac.getJSON||!ac.getCurrentUserId)return;
var u=ac.getCurrentUserId();
if(!u)return;
ids=ids.slice(0,50);                 /* keep the query string sane */
SERBUSY=true;
/* Ids alone -- adding Recursive/IncludeItemTypes only widens the query plan
   for what is a direct id lookup, and SeriesId/SeriesName come back either way. */
ac.getJSON(ac.getUrl('Users/'+u+'/Items',{Ids:ids.join(','),Fields:'SeriesId'}))
.then(function(r){
var L=(r&&r.Items)||[],i,it;
for(i=0;i<L.length;i++){
it=L[i];
SER[norm(it.Id)]={sid:norm(it.SeriesId||''),en:(it.SeriesName||'')};
}
/* anything the server did not return is unresolvable -- record it so the
   card is marked skip instead of being queued forever */
for(i=0;i<ids.length;i++)if(!SER[ids[i]])SER[ids[i]]={sid:'',en:''};
SERBUSY=false;})
.catch(function(){
var i;for(i=0;i<ids.length;i++)SER[ids[i]]={sid:'',en:''};
SERBUSY=false;});
}
function bfetch(path){
return fetch(bridge()+path,{headers:{'x-jellyfin-token':token()}}).then(function(r){return r.json();});
}
function resolveEpTitles(L){
if(EPBUSY)return;
var ids=[],k;
for(k in EPNEED){if(EPNEED.hasOwnProperty(k)&&EPT[k]===undefined)ids.push(k);}
if(!ids.length)return;
ids=ids.slice(0,120);
EPBUSY=true;
bfetch('/api/eptitles?lang='+encodeURIComponent(L)+'&ids='+ids.join(','))
.then(function(d){
var m=(d&&d.items)||{},i;
for(i=0;i<ids.length;i++)EPT[ids[i]]=m[ids[i]]||null;   /* null = known-absent */
EPBUSY=false;})
.catch(function(){var i;for(i=0;i<ids.length;i++)EPT[ids[i]]=null;EPBUSY=false;});
}
function resolveTmdbTitles(L){
if(TMBUSY)return;
var keys=[],k;
for(k in TMNEED){if(TMNEED.hasOwnProperty(k)&&TMT[k]===undefined)keys.push(k);}
if(!keys.length)return;
keys=keys.slice(0,50);
TMBUSY=true;
bfetch('/api/tmdbtitles?lang='+encodeURIComponent(L)+'&ids='+encodeURIComponent(keys.join(',')))
.then(function(d){
var m=(d&&d.items)||{},i;
for(i=0;i<keys.length;i++)TMT[keys[i]]=m[keys[i]]||null;
TMBUSY=false;})
.catch(function(){var i;for(i=0;i<keys.length;i++)TMT[keys[i]]=null;TMBUSY=false;});
}
/* Discover cards are keyed on TMDb, not on a Jellyfin item id. */
/* The title node for a TMDb-keyed card. NOT titleNode(): a jellyseerr card wraps
   its title in an <a href="#/search?query=..."> and writing textContent on the
   .cardText-first container would delete that anchor, so the card would lose its
   tap target. Write into the anchor when there is one. */
function discTitleNode(host){
return host.querySelector('.cardText-first .textActionButton')
    || host.querySelector('.cardText-first a')
    || host.querySelector('.cardText-first');
}
function sweepDiscover(L){
/* Was '.discover-card[data-tmdb-id]'. The Jellyseerr rows on a detail page
   ("\u63a8\u8350" / "\u76f8\u4f3c\u9879\u76ee") are the same kind of content and carry the same
   data-tmdb-id + data-media-type, but the class is .jellyseerr-card AND the
   attributes sit on a CHILD of .card -- so this sweep matched none of them and
   two whole rows of a Chinese detail page stayed English ("Secret Sunshine",
   "Payback"). Selecting on the attributes rather than the class covers both, and
   the title is resolved from the enclosing card. */
var els=document.querySelectorAll('[data-tmdb-id][data-media-type]'),i,c,host,kind,key,node,name;
for(i=0;i<els.length;i++){
c=els[i];
if(c.getAttribute('data-sf-t18n-d'))continue;
kind=(c.getAttribute('data-media-type')||'').toLowerCase();
if(kind!=='movie'&&kind!=='tv'){c.setAttribute('data-sf-t18n-d','skip');continue;}
key=kind+':'+c.getAttribute('data-tmdb-id');
name=TMT[key];
if(name===undefined){TMNEED[key]=1;continue;}      /* queued -- retry next tick */
if(!name){c.setAttribute('data-sf-t18n-d','skip');continue;}
host=(c.closest&&c.closest('.card,.discover-card'))||c;
node=discTitleNode(host)||discTitleNode(c);
if(!node)continue;
if((node.textContent||'').trim()!==name)node.textContent=name;
c.setAttribute('data-sf-t18n-d','1');
}
resolveTmdbTitles(L);
}
function sweepCards(L){
/* OUR rows (Watchlist, the music/audiobook rows) build .sf-ml-card and never
   carry Jellyfin's .card class, so a '.card[data-id]' sweep matched ZERO of them
   -- the Watchlist heading translated while every title under it stayed English.
   They do contain a .cardText-first, so once they are selected the rest of this
   function already handles them. */
var cards=document.querySelectorAll('.card[data-id],.sf-ml-card[data-id]'),i,c,id,e,node;
for(i=0;i<cards.length;i++){
c=cards[i];
/* Two INDEPENDENT jobs live on an episode card: the series name in
   cardText-first and the episode name in cardText-secondary. This used to
   `continue` on data-sf-t18n before looking at either -- so the moment the
   series name resolved, the card was skipped forever and the episode name was
   never translated. It only appeared to work because Jellyfin re-renders those
   rows after ~35s, wiping the attribute with both caches warm by then. That is
   exactly the reported "episode names load in English but flash into Chinese
   after some time". Each pass now carries its own mark. */
var doneSeries=!!c.getAttribute('data-sf-t18n');
var t=c.getAttribute('data-type')||'';
id=norm(c.getAttribute('data-id'));
if(t==='Episode'||t==='Season'){
/* Independent of the series-name pass below: the two live in different nodes
   and either can be translatable without the other. */
if(t==='Episode'&&!c.getAttribute('data-sf-t18n-ep')){
var ep=EPT[id];
if(ep===undefined){EPNEED[id]=1;}
else if(!ep||!ep.t||!ep.en){c.setAttribute('data-sf-t18n-ep','skip');}
else{
var sn=c.querySelector('.cardText-secondary'),stx=sn?(sn.textContent||''):'';
/* the node reads "S1:E1 - <name>"; swap only the name */
if(sn&&stx.indexOf(ep.en)>=0){
sn.textContent=stx.split(ep.en).join(ep.t);
c.setAttribute('data-sf-t18n-ep','1');
}else if(sn){c.setAttribute('data-sf-t18n-ep','skip');}
}
}
if(doneSeries)continue;                /* series half already handled */
var s=SER[id];
if(!s){NEED[id]=1;continue;}           /* queued -- retry on a later tick */
if(!s.sid||!s.en){c.setAttribute('data-sf-t18n','skip');continue;}
e=MAP[s.sid];
if(!e||!e[L]){c.setAttribute('data-sf-t18n','skip');continue;}
node=titleNode(c);
if(!node)continue;
/* only when this really is the series name in this layout */
if((node.textContent||'').trim()!==s.en.trim()){c.setAttribute('data-sf-t18n','skip');continue;}
node.textContent=e[L];
c.setAttribute('data-sf-t18n','1');
continue;
}
if(doneSeries)continue;
if(t&&t!=='Movie'&&t!=='Series')continue;      /* audio keeps its own labels */
e=MAP[id];
if(!e||!e[L]){c.setAttribute('data-sf-t18n','skip');continue;}
node=titleNode(c);
if(!node)continue;
node.textContent=e[L];
c.setAttribute('data-sf-t18n','1');
}
resolveSeries();
resolveEpTitles(L);
}
function hashId(){
var h=location.hash||'';
if(h.indexOf('details')<0)return '';
var i=h.indexOf('id=');
if(i<0)return '';
var v=h.substr(i+3),j=v.indexOf('&');
if(j>=0)v=v.substr(0,j);
return norm(v);
}
function sweepDetail(L){
var id=hashId();
if(!id)return;
var e=MAP[id];
if(!e||!e[L])return;
var pages=document.querySelectorAll('.itemDetailPage'),i,p,n;
for(i=0;i<pages.length;i++){
p=pages[i];
if(p.offsetParent===null)continue;
n=p.querySelector('.itemName.infoText, h1.itemName, .itemName');
if(!n)continue;
if(n.getAttribute('data-sf-t18n')===id)continue;
n.textContent=e[L];
n.setAttribute('data-sf-t18n',id);
}
}
/* sf-t18n-programs: the Live TV PAGE's own cards.
   These are Program items -- their ids are guide ids, not library ids, so they
   are not in the id-keyed MAP and sweepCards never touched them. The result was
   a straight contradiction on screen: our home Live TV row showed 四眼天鸡 while
   the Live TV page showed "Chicken Little", for the same programme, with the
   translation sitting in the name index the whole time (verified for all six
   programmes on screen).
   Translated by NAME, the same source the home row uses. Guard on CONTENT, never
   a stamp: Jellyfin re-renders these cards on every guide refresh, and
   sfTrName() is a no-op on an already-translated string (the normalised Chinese
   key is not in the index), so re-running is free and self-correcting. */
/* sf-t18n-osdtitle: the video player's own title.
   Jellyfin builds it from the item as "Series - S1:E2 - Episode", so it read
   "Friends - S1:E2 - ..." in Chinese even though the card that started playback
   said 老友记. The series part is translatable straight from the NAME index with
   no extra request; the SxEy marker and the episode name are left as broadcast.
   Content-guarded: an already-translated name is not a key in the index, so
   re-running is a no-op and a Jellyfin re-render is simply re-translated. */
function sweepOsdTitle(L){
try{
var els=document.querySelectorAll('.osdHeader .pageTitle,.videoOsdBottom .pageTitle'),i,n,t,parts,tr;
var k,ep;
for(i=0;i<els.length;i++){
n=els[i];
t=(n.textContent||'').trim();
if(!t||t.indexOf(' - ')<0)continue;
parts=t.split(' - ');
tr=window.sfTrName?window.sfTrName(parts[0]):parts[0];
if(tr&&tr!==parts[0])parts[0]=tr;
t=parts.join(' - ');
/* The EPISODE name as well, when it is already cached. EPT is keyed by item id
   and the OSD gives us no id, but the card that started playback resolved this
   very episode a moment ago -- so match on the English name we stored with it.
   Costs nothing extra and keeps the player consistent with the detail page,
   which shows 超声波检查 for the same episode. */
for(k in EPT){
if(!EPT.hasOwnProperty(k))continue;
ep=EPT[k];
if(ep&&ep.en&&ep.t&&ep.en!==ep.t&&t.indexOf(ep.en)>-1){t=t.split(ep.en).join(ep.t);break;}
}
if(t!==(n.textContent||'').trim())n.textContent=t;
}
}catch(e){}
}
function sweepPrograms(L){
try{
var cards=document.querySelectorAll('.card[data-type="Program"]'),i,c,n,t,tr;
for(i=0;i<cards.length;i++){
c=cards[i];
n=c.querySelector('.cardText-first');
if(!n)continue;
t=(n.textContent||'').trim();
if(!t)continue;
tr=window.sfTrName?window.sfTrName(t):t;
if(tr&&tr!==t)n.textContent=tr;
}
}catch(e){}
}
function tick(){
try{
var L=lang();
if(!L)return;                 /* English: leave everything alone */
load();
prewarm();                    /* starts before any card exists */
sweepDiscover(L);             /* independent of MAP -- Discover is not library content */
sweepPrograms(L);             /* guide data: keyed on NAME, not on the item map */
sweepOsdTitle(L);             /* the player's own title bar */
if(!MAP)return;
sweepCards(L);
sweepDetail(L);
}catch(e){}
}

/* sf-t18n-fouc: the 700ms poll IS the "starts English then flashes to Chinese"
   complaint. Two delays stacked:
     1. load() only ran from the first tick, so the fetch began at t=700ms.
     2. a card inserted just after a tick kept its English title for the rest of
        the interval -- and the home page inserts cards in bursts.
   So: start the fetch immediately, sweep the moment the map lands, and sweep on
   DOM INSERTION instead of waiting for the next poll. childList only -- never
   attributes, which is what made an earlier observer re-run on every class
   change -- and a burst of inserts collapses into a single rAF sweep. */
var SWEEPQ=false;
function sweepSoon(){
if(SWEEPQ)return;
SWEEPQ=true;
requestAnimationFrame(function(){
SWEEPQ=false;
try{
var L=lang();
if(!L)return;
sweepDiscover(L);
sweepPrograms(L);
sweepOsdTitle(L);
if(!MAP)return;
sweepCards(L);sweepDetail(L);
}catch(e){}
});
}
function observeInserts(){
if(!document.body){setTimeout(observeInserts,50);return;}
try{
new MutationObserver(function(m){
for(var i=0;i<m.length;i++){
if(m[i].type==='characterData'||(m[i].addedNodes&&m[i].addedNodes.length)){sweepSoon();return;}
}
}).observe(document.body,{childList:true,subtree:true,characterData:true});
}catch(e){}
}
/* sf-name-i18n: a NAME -> translated-title index, for anything that knows only a
   title. The Live TV row is the case that needed it: an EPG programme is not a
   library item and carries no id, so its name could never be looked up and the
   row read as English under a translated heading. Measured 11 of 11 airing
   programmes resolvable, so this covers essentially all of them.
   Cached in localStorage exactly like the title map, so a repeat visit has it at
   t=0 and the row is never built with an English title first. */
var NMAP=null,NPEND=false,NKEY='sf-t18n-names';
function nameNorm(s){
return String(s||'').toLowerCase().replace(/[^a-z0-9]+/g,'');
}
function nameLoad(){
if(NMAP!==null||NPEND)return;
var L=lang();
if(!L)return;
try{
var raw=localStorage.getItem(NKEY+'-'+L);
if(raw){
var o=JSON.parse(raw);
if(o&&o.names&&(Date.now()-(o.at||0))<604800000)NMAP=o.names;
}
}catch(e){}
NPEND=true;
fetch(bridge()+'/api/nametitles?lang='+encodeURIComponent(L),
      {headers:{'x-jellyfin-token':token()}})
.then(function(r){return r.json();})
.then(function(d){
NMAP=(d&&d.names)||{};
NPEND=false;
try{localStorage.setItem(NKEY+'-'+L,JSON.stringify({at:Date.now(),names:NMAP}));}catch(e){}
})
.catch(function(){if(!NMAP)NMAP={};NPEND=false;});
}
/* Episode NAME by item id, for callers that compose their own line (the detail
   page's "S1 E1 . <name>"). Returns the English name until the batch resolves,
   and queues the fetch, so the caller can simply ask again next tick. */
window.sfTrEp=function(id,en){
try{
var L=lang();if(!L)return en;
var k=norm(id),e=EPT[k];
if(e===undefined){EPNEED[k]=1;resolveEpTitles(L);return en;}
if(e&&e.t)return e.t;
return en;
}catch(x){return en;}
};
window.sfTrName=function(n){
try{
if(!n)return n;
if(!lang())return n;
nameLoad();
if(!NMAP)return n;
return NMAP[nameNorm(n)]||n;
}catch(e){return n;}
};
try{nameLoad();}catch(e){}
observeInserts();
try{if(lang()){load();prewarm();}}catch(e){}
setInterval(tick,700);
})();</script>"""
