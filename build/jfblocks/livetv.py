"""jfblocks/livetv.py -- payload constants lifted out of jf_patch.py.

Each constant's source text (and its comments) is byte-identical to the
monolith; only its location changed. 20 constants.
"""
__all__ = [
    'LIVETV_MARKER',
    'LIVETV_SCRIPT',
    'SPORTSTAB_MARKER',
    'SPORTSTAB_SCRIPT',
    'NOWLINE_MARKER',
    'NOWLINE_SCRIPT',
    'LIVETVRESUME_MARKER',
    'LIVETVRESUME_SCRIPT',
    'LIVECTRL_MARKER',
    'LIVECTRL_SCRIPT',
    'GUIDEFILTER_MARKER',
    'GUIDEFILTER_SCRIPT',
    'CHANNELCARDS_MARKER',
    'CHANNELCARDS_SCRIPT',
    'GUIDEFIX_MARKER',
    'GUIDEFIX_STYLE',
    'LIVETVPANE_MARKER',
    'LIVETVPANE_SCRIPT',
    'SPORTSPAGE_MARKER',
    'SPORTSPAGE_SCRIPT',
]


LIVETV_MARKER = 'jf-livetv-tab'
LIVETV_SCRIPT = (
    '<script>(function(){ /* jf-livetv-tab */'
    'function addLiveTvTab(){'
    'var page=document.querySelector("#indexPage:not(.hide)");'
    'if(!page)return;'
    'var slider=document.querySelector(".headerTabs.sectionTabs .emby-tabs-slider");'
    'if(!slider){slider=document.querySelector(".headerTabs.sectionTabs");}'
    '/* GLOBAL guard, matching jf-home-tab: a per-slider check adds a second'
    ' copy whenever two tab strips exist at once (see jellyfin-main-nav-pills). */'
    'if(!slider||document.querySelector(".jf-livetv-tab"))return;'
    'var btns=slider.querySelectorAll(".emby-tab-button");'
    'if(btns.length<2)return;'
    'var btn=document.createElement("button");'
    'btn.type="button";'
    'btn.className="emby-button emby-tab-button jf-livetv-tab";'
    'btn.setAttribute("data-sf-nav","Live TV");'
    'btn.textContent="Live TV";'
    # jf-tabdelegation: Jellyfin's emby-tabs delegation matches the clicked element
    # by its .emby-tab-button class and then resolves a tab controller by INDEX.
    # Our pill has no index in that view, so its bundle threw "Cannot find module
    # './'" on every Live TV switch. We navigate ourselves, so the class is dropped
    # for the duration of the click and restored on the next tick -- the styling it
    # feeds (the sf-pill-tight padding tiers) is unaffected in steady state.
    'btn.addEventListener("click",function(e){'
    'try{localStorage.setItem("sfProgramsFilter","all");}catch(err){}'
    # sf-tab-nojitter: the event, not the class -- see the note in jf-sports-tab
    'e.preventDefault();e.stopPropagation();'
    'if(e.stopImmediatePropagation)e.stopImmediatePropagation();'
    # sf-tab-pushstate: pushState, not location.hash. Assigning the hash fires a
    # hashchange, and Jellyfin answers that by REPLACING the whole
    # .emby-tabs-slider inside .headerTabs -- even though #/home?livetv=1 is the
    # same route it is already on. Traced: t=172 slider swapped (+1/-1) and four
    # buttons re-added, t=177 sfPillDedupe prunes the duplicates. While that runs
    # the strip is short, so the pill row dropped 31px and sprang back.
    # pushState fires no hashchange, so the strip is never touched; the pane's own
    # wrapper picks the change up, and the history entry keeps Back working.
    'try{history.pushState(null,"","#/home?livetv=1");}'
    'catch(e2){window.location.hash="#/home?livetv=1";}'
    '},true);'   # jf-livetv-pane: the home pane, not the route
    'slider.insertBefore(btn,btns[1]);'
    '}'
    'var obs=new MutationObserver(addLiveTvTab);'
    '/* jf-observer-scope: was document.body with subtree+attributes, so every class change anywhere re-ran this. A pane swap emits ~544 mutations, and with 4 such observers that is thousands of needless callbacks -- measured as a fixed ~1.4s tab switch. The tab slider lives inside .skinHeader, so that is the smallest correct scope. Page .hide state is still evaluated on each run, and the existing setInterval covers anything the narrower scope misses. Falls back to body if the header never appears. */'
    '(function _at(){var _t=document.querySelector(".skinHeader");'
    'if(!_t){return setTimeout(_at,300);}'
    'obs.observe(_t,{childList:true,subtree:true,attributes:true,attributeFilter:["class"]});})();'
    '})();</script>'
)

# --- Sports tab (2026-08-02). A third pill on the home header, right after
# Live TV, jumping straight to the live sports card browse.
# TARGET IS tab=0 (Programs), NOT tab=1. Measured on the live page: the tab
# strip reads Home / Programs / Guide / Channels / Recordings / Schedule /
# Series, but "Home" is our own injected jf-home-tab and does not count toward
# the index, so tab=0 -> Programs and tab=1 -> Guide. The Programs tab is where
# sf-livesports renders its card grid (verified: .sf-livesports-root present,
# .sf-ls-show set, 46 cards). tab=1 would have been the Guide, which is already
# exactly where the existing jf-livetv-tab pill points, so a Sports pill aimed
# there would have been a duplicate of Live TV.
# Mirrors jf-livetv-tab: same gating on #indexPage:not(.hide) so the pill only
# exists on home, same emby classes so it inherits the native pill styling, and
# the same MutationObserver approach since Jellyfin re-renders the header.
# Anchored to .jf-livetv-tab rather than a fixed index -- it returns early until
# that button exists, so the two always sit together regardless of insert order.
SPORTSTAB_MARKER = 'jf-sports-tab'
SPORTSTAB_SCRIPT = r'''<script>(function(){ /* jf-sports-tab */
function addSportsTab(){
var page=document.querySelector("#indexPage:not(.hide)");
if(!page)return;
var slider=document.querySelector(".headerTabs.sectionTabs .emby-tabs-slider")||document.querySelector(".headerTabs.sectionTabs");
/* GLOBAL guard, matching jf-home-tab -- see the note on jf-livetv-tab. */
if(!slider||document.querySelector(".jf-sports-tab"))return;
/* Anchor to the ONE Live TV pill wherever it ended up, and insert beside it
   rather than into `slider`, so the pair cannot be split across strips. */
var live=document.querySelector(".jf-livetv-tab");
if(!live||!live.parentNode)return;
var btn=document.createElement("button");
btn.type="button";
btn.className="emby-button emby-tab-button jf-sports-tab";
btn.setAttribute("data-sf-nav","Sports");
btn.textContent="Sports";
/* The overlay keys on localStorage.sfProgramsFilter==='sports'; navigating
   alone left it on whatever the TV|Sports pill was last set to, which is why
   this tab "did not always work". Set the destination explicitly. */
btn.addEventListener("click",function(e){try{localStorage.setItem("sfProgramsFilter","sports");}catch(err){}
/* sf-tab-nojitter (2026-08-29): stop Jellyfin's delegation with the EVENT,
   never by removing .emby-tab-button. That class carries the pill metrics, so
   dropping it for the duration of the click shrank the button and the row
   visibly twitched -- measured Live TV@30 and Sports@30 against Home@35 and
   My Stuff@35 for one frame, i.e. the pills split by 5px and snapped back.
   Capture + stopImmediatePropagation is exactly what the .jf-mu-mainbar pills
   already do, and it changes no geometry at all. */
e.preventDefault();e.stopPropagation();
if(e.stopImmediatePropagation)e.stopImmediatePropagation();
window.location.hash="#/home?sports=1";},true);
live.parentNode.insertBefore(btn,live.nextSibling);
}
var obs=new MutationObserver(addSportsTab);
/* jf-observer-scope: was document.body with subtree+attributes, so every class change anywhere re-ran this. A pane swap emits ~544 mutations, and with 4 such observers that is thousands of needless callbacks -- measured as a fixed ~1.4s tab switch. The tab slider lives inside .skinHeader, so that is the smallest correct scope. Page .hide state is still evaluated on each run, and the existing setInterval covers anything the narrower scope misses. Falls back to body if the header never appears. */
(function _at(){var _t=document.querySelector('.skinHeader');
if(!_t){return setTimeout(_at,300);}
obs.observe(_t,{childList:true,subtree:true,attributes:true,attributeFilter:['class']});})();
addSportsTab();
})();</script>'''

NOWLINE_MARKER = 'jf-now-line-v8'
NOWLINE_SCRIPT = (
    '<script>(function(){'
    'if(!document.getElementById("jf-now-css")){'
    'var s=document.createElement("style");'
    's.id="jf-now-css";'
    's.textContent='
    '"#jf-now-line{'
        'position:absolute!important;top:0!important;bottom:0!important;'
        'width:3px!important;background:#ff4444!important;'
        'z-index:9999!important;pointer-events:none!important;'
        'box-shadow:0 0 10px rgba(255,68,68,0.9)!important;'
    '}'
    '#jf-now-label{'
        'position:absolute!important;bottom:0!important;'
        'background:#ff4444!important;color:#fff!important;'
        'font-size:0.6em!important;padding:1px 5px!important;line-height:1.1!important;'
        'border-radius:4px 4px 0 0!important;white-space:nowrap!important;'
        'z-index:9999!important;pointer-events:none!important;'
        'transform:translateX(-50%)!important;font-weight:bold!important;'
    '}";'
    'document.head.appendChild(s);'
    '}'
    'function parseStart(){'
    'var h=document.querySelector(".timeslotHeader");'
    'if(!h)return null;'
    'var m=h.textContent.trim().match(/(\d{1,2}):(\d{2})\s*(am|pm)?/i);'
    'if(!m)return null;'
    'var hh=parseInt(m[1],10),mm=parseInt(m[2],10);'
    'if(m[3]){var ap=m[3].toLowerCase();'
    'if(ap==="pm"&&hh!==12)hh+=12;'
    'if(ap==="am"&&hh===12)hh=0;}'
    'var d=new Date();d.setHours(hh,mm,0,0);'
    'if(d.getTime()>Date.now()+300000)d.setTime(d.getTime()-86400000);'
    'return d.getTime();'
    '}'
    'function isToday(){'
    'var tabs=document.querySelectorAll(".emby-tab-button-active");'
    'for(var i=0;i<tabs.length;i++){'
    'var m=tabs[i].textContent.trim().match(/^[A-Za-z]{3}\s*(\d{1,2})$/);'
    'if(m)return parseInt(m[1],10)===new Date().getDate();'
    '}'
    'return true;'
    '}'
    'function clear(){'
    'var ln=document.getElementById("jf-now-line");if(ln)ln.remove();'
    'var lb=document.getElementById("jf-now-label");if(lb)lb.remove();'
    '}'
    'function draw(){'
    'var grid=document.querySelector(".programGrid");'
    'var headers=document.querySelectorAll(".timeslotHeader");'
    'if(!grid||!headers.length||!isToday()){clear();return;}'
    'var start=parseStart();'
    'if(start===null){clear();return;}'
    'var slotW=grid.scrollWidth/headers.length;'
    'var x=((Date.now()-start)/1800000)*slotW;'
    'if(x<0||x>grid.scrollWidth){clear();return;}'
    'grid.style.position="relative";'
    'var ln=document.getElementById("jf-now-line");'
    'if(!ln||ln.parentElement!==grid){if(ln)ln.remove();ln=document.createElement("div");ln.id="jf-now-line";grid.appendChild(ln);}'
    'var _l=Math.round(x)+"px";if(ln.style.left!==_l)ln.style.left=_l;'
    'var inner=document.querySelector(".timeslotHeadersInner");'
    'if(inner){'
    'var lb=document.getElementById("jf-now-label");'
    'if(!lb||lb.parentElement!==inner){if(lb)lb.remove();lb=document.createElement("div");lb.id="jf-now-label";inner.appendChild(lb);}'
    'var _l2=Math.round(x)+"px";if(lb.style.left!==_l2)lb.style.left=_l2;'
    'lb.textContent=new Date().toLocaleTimeString([],{hour:"numeric",minute:"2-digit"});'
    '}'
    '}'
    'setInterval(draw,2000);draw();'
    '/* jf-now-line-v8 */'
    '})();</script>'
)

LIVETVRESUME_MARKER = 'sf-livetv-resume'
LIVETVRESUME_SCRIPT = r'''<script>(function(){
/* sf-livetv-resume */
/* The auto-heal reload (sf-livetv-control) used to bounce to the home
   screen instead of back into the channel -- confirmed live: Jellyfin's
   own #/video route carries NO item-identifying info in the URL at all
   (hash is the literal string "#/video", zero query params, for both live
   and on-demand playback), so a plain location.reload() has nothing to
   resume from and boots fresh to home. This stashes the currently-playing
   channel's id in sessionStorage right before the stall-recovery script
   reloads; on the next fresh page load, if that stash is present and
   recent, this automatically navigates back to the exact same channel's
   details page and presses Play again.

   BUG FIXED (2026-07-25, "played UFC... but it loaded up baseball"): this
   used to track "the currently playing channel" by polling location.hash
   for the #/details?id=... pattern and remembering the last match --  but
   that stops updating the instant playback starts (hash becomes the
   content-free "#/video"), so it only ever reflected the last channel
   whose DETAILS PAGE was visited, not what's actually playing now. Confirmed
   the exact failure: a channel switch that doesn't revisit #/details (e.g.
   Jellyfin's own in-player channel switcher) leaves that stale, and an
   unstable stream (this UFC channel was stalling every 8-30s per the bridge
   logs) then triggers OUR auto-reload frequently enough to resume the WRONG,
   stale channel instead of the one actually playing.
   FIX: ask Jellyfin's own server directly, via ApiClient.getSessions() for
   THIS device, which item this session's NowPlayingItem actually is right
   now -- server-authoritative, unaffected by however the user navigated
   here. Verified live: getSessions({deviceId}) correctly returned the
   actually-playing item's id even when this browser tab's own hash history
   didn't reflect it. */
window.__sfLiveTvStashResume=function(){
try{
var api=window.ApiClient;
if(!api)return Promise.resolve(false);
var creds=JSON.parse(localStorage.getItem('jellyfin_credentials'));
var serverId=creds.Servers[0].Id;
return api.getSessions({deviceId:api.deviceId()}).then(function(sessions){
var item=sessions&&sessions[0]&&sessions[0].NowPlayingItem;
if(!item)return false;
try{sessionStorage.setItem('sfResumeChannel',JSON.stringify({id:item.Id,serverId:serverId,at:Date.now()}));return true;}catch(e){return false;}
},function(){return false;});
}catch(e){return Promise.resolve(false);}
};

/* Boot-time resume: if the previous page reloaded specifically to recover
   from a stall, jump back into that channel and press Play automatically. */
(function(){
var raw;try{raw=sessionStorage.getItem('sfResumeChannel');}catch(e){}
if(!raw)return;
try{sessionStorage.removeItem('sfResumeChannel');}catch(e){}
var info;try{info=JSON.parse(raw);}catch(e){return;}
if(!info||Date.now()-info.at>30000)return;
setTimeout(function(){
location.hash='#/details?id='+info.id+'&serverId='+info.serverId;
var tries=0;
var iv=setInterval(function(){
tries++;
var btn=document.querySelector('button.button-flat.btnPlay.detailButton.emby-button:not(.hide)');
if(btn){clearInterval(iv);btn.click();}
else if(tries>50){clearInterval(iv);}
},400);
},2000);
})();
})();</script>'''

LIVECTRL_MARKER = 'sf-livetv-control'
LIVECTRL_SCRIPT = r'''<script>(function(){
/* sf-livetv-control */
var css="html.sf-live .videoOsdBottom .sliderContainer:not(.osdVolumeSliderContainer){visibility:hidden!important;}html.sf-live .videoOsdBottom .btnPause,html.sf-live .videoOsdBottom .btnRewind,html.sf-live .videoOsdBottom .btnFastForward,html.sf-live .videoOsdBottom .btnPreviousChapter,html.sf-live .videoOsdBottom .btnNextChapter,html.sf-live .videoOsdBottom .btnPreviousTrack,html.sf-live .videoOsdBottom .btnNextTrack{display:none!important;}"
/* Root cause of the volume slider being invisible found 2026-07-25: this
   rule's original .sliderContainer selector is a GENERIC class shared by
   BOTH the seek/position slider (which we correctly want hidden -- no
   seeking on live) and the volume slider (.sliderContainer
   osdVolumeSliderContainer, which we want visible, matching on-demand).
   Confirmed live: the volume slider had display:flex (correct, from the
   earlier fix reverting its OWN display:none) but visibility:hidden --
   inherited from this broader, earlier rule that was never actually the
   one removing it. :not(.osdVolumeSliderContainer) scopes this back to
   only the seek slider, its original intent. */
/* Record button removed for live (not a supported workflow here), and
   Bookmark Current Time removed too -- it marks a position on the
   timeline to jump back to later, which doesn't mean anything on a
   continuously-moving live feed. Confirmed live: .osdTimeText (the
   now-playing-position text, blank during live playback) carries
   margin-right:auto in the stock layout -- normally that pushes the seek
   slider into the middle for on-demand video, but since the slider is
   already hidden for live (rule above), that auto-margin just shoves every
   remaining control (favorite/mute/settings/pip/fullscreen) to the far
   right edge instead, leaving a large dead gap in between. Zeroing it lets
   the row flow together compactly. */
+"html.sf-live .videoOsdBottom .btnRecord{display:none!important;}"
+"html.sf-live .videoOsdBottom button[title=\"Bookmark Current Time\"]{display:none!important;}"
/* The rule above is an ENGLISH-only match: the title is translated, so in zh
   the same button reads "\u4e3a\u76ee\u524d\u65f6\u95f4\u5efa\u7acb\u4e66\u7b7e" and stayed VISIBLE during live TV
   (measured: en 4 OSD buttons, zh 5). sfHideLiveBookmark stamps it by its
   material-icons ligature, which is not translated. */
+"html.sf-live .videoOsdBottom button[data-sf-bmk]{display:none!important;}"
+"html.sf-live .videoOsdBottom .osdTimeText{margin-right:0!important;}"
/* The seek-slider row itself (the direct-child wrapper in .osdControls
   containing the position slider + start/end time text) was still
   reserving ~30px of vertical space above the controls row even though
   the slider inside it is already hidden via visibility:hidden -- that
   property hides the slider visually but keeps its layout space reserved.
   display:none on the whole wrapper actually removes it, closing the
   dead gap above the row. Scoped to a direct-child selector under
   .osdControls, confirmed to match exactly this one element. */
+"html.sf-live .videoOsdBottom .osdControls > .flex.flex-direction-row.align-items-center{display:none!important;}"
/* .osdControls itself has padding:12px on all sides (24px combined top+
   bottom) -- trimmed to 4px top/bottom for a tighter bar now that it's
   down to a single row. Left/right untouched (no complaint there), and
   button padding itself is left alone too so tap targets don't shrink. */
+"html.sf-live .videoOsdBottom .osdControls{padding-top:4px!important;padding-bottom:4px!important;}"
+"html.sf-live .videoOsdBottom .btnUserRating{display:none!important;}"
+"html.sf-live .videoOsdBottom .volumeButtons{margin-left:auto!important;}"
/* Program title moved down (see moveTitleIfNeeded below) out of the top
   header into this same row as the controls -- per feedback, having it
   isolated at the very top with nothing else nearby just left a large
   dead gap between it and the actual controls at the bottom. Style it to
   sit naturally among the icon buttons: same rough text size as the
   channel-info line above it, truncated rather than wrapping/overflowing
   into the icon cluster on a narrow screen. */
+"html.sf-live .videoOsdBottom .pageTitle{font-size:1em;font-weight:400;color:#fff;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;max-width:55%;margin-right:.5em;order:-1;}"
/* Channel info (CH 558 SKY SPORTS F1) moved down alongside it -- same
   treatment, positioned first via flex order so it lands at the far left
   ahead of the title, per feedback. */
+"html.sf-live .videoOsdBottom .osdSecondaryMediaInfo{display:flex!important;font-size:.9em;color:#ccc;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;max-width:30%;margin-right:.75em;order:-2;}";
/* Correction: a previous version of this patch also hid
   .osdVolumeSliderContainer, thinking its reserved width was dead space
   left over from the button removals above. It wasn't -- on-demand
   playback shows this exact same horizontal slider right next to the
   mute icon, always visible and fully functional (confirmed by comparing
   directly against an on-demand title), and hiding it for live removed a
   real, working volume control, not empty space. Reverted; the slider now
   shows for live exactly as it already does for on-demand. */
var st=document.createElement("style");st.textContent=css;document.head.appendChild(st);
/* Rewritten 2026-07-25 after a confirmed real F1-channel stall: server logs
   showed ffmpeg's output frame count completely frozen (same frame number
   for 50+ consecutive log lines, fps/speed decaying toward zero) while the
   process itself never crashed or errored -- so Jellyfin's own restart-on-
   failure logic never triggered, and the user had to manually reload every
   time ("never self-heals"). Traced the ORIGINAL version of this script to
   the exact reason it didn't catch that: liveV() returned null (resetting
   every counter to zero) whenever v.readyState===0, and the stall counter
   only ever incremented inside `if(v.seekable.length)` -- but a stall
   severe enough to starve the input is exactly when the browser's buffer
   can run dry enough to drop readyState to 0 and/or empty the seekable
   range. The one safety net meant to catch a dead stream was disabling
   itself in precisely the scenario it existed for. Fixed by tracking
   staleness with wall-clock time instead of tick counts (immune to a
   single check's applicability that tick) and treating a degraded/empty
   readyState or seekable range as "still stalled", never as "stop
   watching, reset to zero". */
/* NOTE: deliberately does NOT check !isFinite(v.duration). duration is NaN
   for EVERY video (live or a regular movie/show) for a moment right after
   the element is created, before metadata loads -- it's not a live-specific
   signal, just "not loaded yet". The old code included that check, which the
   1s-polling detection rarely observed in practice (duration usually
   resolved before the next tick). Once detection became instant (the
   MutationObserver added for the "flash of old layout" fix), it reliably
   caught this transient NaN window on EVERY regular video too, incorrectly
   flagging it as live for a moment -- long enough for moveTitleIfNeeded()
   below to physically relocate the title/info nodes into the live-only
   bottom-row layout, with no reverse operation, leaving a regular movie/show
   with a permanently oversized OSD bar (reported: it grew large enough to
   cover subtitles again despite the sub-lift fix). duration>86400 and the
   Record button are both unambiguous real-live signals that don't have this
   loading-phase false positive. */
/* sf-live-ersatz: ErsatzTV channels do not LOOK live in the DOM. Measured while
   "LU TV" played: video.duration went 20 -> 40 -> 48s and kept growing (a
   sliding HLS window, so never > 86400), durInfinite false, and .btnRecord was
   present but carried .hide -- so neither check below ever fired and the
   one-line OSD never engaged on the admin's own channels.
   Duration GROWTH is deliberately not used as a signal: a Jellyfin HLS transcode
   of ordinary VOD also reports a growing duration, so it would flag films as
   live. The authoritative answer is what the SERVER says is playing -- a channel
   item is Type=TvChannel with RunTimeTicks=null -- so ask it once per playback
   and cache the answer. */
var SF_LIVE_SESS=null,SF_LIVE_BUSY=false,SF_LIVE_LAST=0;
function sfLiveSession(){
if(SF_LIVE_SESS!==null||SF_LIVE_BUSY)return;
/* Retry until the server actually reports something playing. The first attempt
   fires the moment <video> appears, which is BEFORE the session has a
   NowPlayingItem -- caching that empty answer pinned "not live" for the whole
   playback (measured: resolved with type=null, sf-live never engaged). */
if(Date.now()-SF_LIVE_LAST<2000)return;
SF_LIVE_LAST=Date.now();
var ac=window.ApiClient;
if(!ac||!ac.ajax||!ac.getUrl||!ac.deviceId)return;
SF_LIVE_BUSY=true;
try{
ac.ajax({type:"GET",url:ac.getUrl("Sessions",{deviceId:ac.deviceId()}),dataType:"json"})
.then(function(list){
var n=list&&list[0]&&list[0].NowPlayingItem;
/* Only a definitive answer is cached; "nothing playing yet" stays unknown so the
   next tick asks again. */
if(n)SF_LIVE_SESS=!!(n.Type==="TvChannel"||n.Type==="Program"||n.IsLiveStream===true);
SF_LIVE_BUSY=false;
/* flip the class immediately rather than waiting for the next DOM change */
try{fastLiveCheck();}catch(e){}
},function(){SF_LIVE_BUSY=false;});
}catch(e){SF_LIVE_BUSY=false;}
}
function sfLiveReset(){SF_LIVE_SESS=null;SF_LIVE_BUSY=false;SF_LIVE_LAST=0;}
function isLiveCandidate(v){
if(!v)return false;
if(v.duration===Infinity||v.duration>86400)return true;
if(document.querySelector(".btnRecord:not(.hide)"))return true;
sfLiveSession();
return SF_LIVE_SESS===true;
}
var lc=-1,lastProgressAt=0,seekFails=0;
function reloadedRecently(){try{return Date.now()-(+sessionStorage.getItem("sfReloadAt")||0)<90000;}catch(e){return false;}}
/* Physically relocates Jellyfin's own .pageTitle node AND the channel-info
   node (.osdSecondaryMediaInfo, "CH 558 SKY SPORTS F1") -- not text copies --
   into the bottom control row, so everything (channel info, program title,
   volume/settings/pip/fullscreen) ends up on ONE line instead of three
   separate rows each reserving their own vertical space. Moving the real
   nodes rather than cloning text means Jellyfin's own logic for updating
   them (e.g. channel or program changes) keeps working with zero extra
   code here. Order: channel info first (far left, per feedback), then
   title, then whatever was already first in the row (nothing, now that
   record's been removed) -- insertBefore each at firstChild in reverse
   order of desired appearance achieves that. Idempotent: checks each
   node's current parent before doing anything, safe to call every tick. */
/* Remember where each node actually came from. Assuming a fixed home was the
   bug below: these two nodes do NOT share one. */
var SF_HOME_TITLE=null,SF_HOME_INFO=null;
/* Stamp Jellyfin Enhanced's "bookmark current time" button so the CSS above can
   hide it on live streams in EVERY language. Matching on the icon ligature
   rather than the title, because the title is localized. */
function sfHideLiveBookmark(){
try{
var b=document.querySelectorAll('.videoOsdBottom button'),i,ic;
for(i=0;i<b.length;i++){
if(b[i].getAttribute('data-sf-bmk'))continue;
ic=b[i].querySelector('.material-icons');
if(!ic)continue;
if(!/bookmark/i.test(ic.textContent||''))continue;
b[i].setAttribute('data-sf-bmk','1');
}
}catch(e){}
}
function moveTitleIfNeeded(){
if(window.__sfNoMove)return;
var slot=document.querySelector(".videoOsdBottom .buttons.focuscontainer-x");
if(!slot)return;
var title=document.querySelector(".osdHeader .pageTitle");
if(title&&title.parentElement!==slot){
SF_HOME_TITLE=title.parentElement;
title.setAttribute("data-sf-osdmoved","1");
slot.insertBefore(title,slot.firstChild);
}
var info=document.querySelector(".osdTextContainer.osdSecondaryMediaInfo");
if(info&&info.parentElement!==slot){
SF_HOME_INFO=info.parentElement;
info.setAttribute("data-sf-osdmoved","1");
slot.insertBefore(info,slot.firstChild);
}
}
/* Reverse of the above -- moves the title/info nodes back out of the bottom
   row and into the header where Jellyfin's stock layout expects them for
   regular (non-live) playback. Needed as a safety net: if isLiveCandidate()
   ever flags something as live only briefly (a transient false positive, a
   race at video start, etc.), moveTitleIfNeeded() has already relocated
   these nodes with no way back on its own, permanently oversizing the OSD
   bar for the rest of that playback session otherwise. Idempotent, like its
   counterpart -- once a node's already back in the header, the querySelector
   below simply won't find it in the bottom row and this no-ops. */
/* Only ever move back what WE moved, and only to the parent it actually came
   from. The first version moved any .videoOsdBottom .osdSecondaryMediaInfo into
   .osdHeader -- but on ordinary (non-live) playback Jellyfin creates that node
   inside the video page (.osdControls) and never puts it in the header at all.
   So this relocated a node we had not touched, out of #videoOsdPage entirely,
   and Jellyfin's own OSD code then did
       var c = e.querySelector('.osdSecondaryMediaInfo'); c.innerHTML = ...
   scoped to the video page -- c was null and its bundle threw
   "Cannot set properties of null (setting 'innerHTML')" on EVERY video start.
   Measured: relocation on -> 1 error, node under .skinHeader; relocation off ->
   0 errors, node under .osdControls. */
function moveTitleBack(){
if(window.__sfNoMove)return;
var title=document.querySelector(".videoOsdBottom .pageTitle[data-sf-osdmoved]");
if(title&&SF_HOME_TITLE&&title.parentElement!==SF_HOME_TITLE){
SF_HOME_TITLE.appendChild(title);
title.removeAttribute("data-sf-osdmoved");
}
var info=document.querySelector(".videoOsdBottom .osdSecondaryMediaInfo[data-sf-osdmoved]");
if(info&&SF_HOME_INFO&&info.parentElement!==SF_HOME_INFO){
SF_HOME_INFO.appendChild(info);
info.removeAttribute("data-sf-osdmoved");
}
}
/* The sf-live class + title/info relocation above used to only run on the
   1-second setInterval below, so the stock Jellyfin layout (title up top,
   record button, dead gaps, etc.) was visible for up to a full second
   before flipping to ours -- a visible flash on every load. A
   MutationObserver reacts the instant Jellyfin actually creates these
   elements instead of waiting for the next poll tick, closing that gap to
   effectively zero. Kept separate from the interval below, which still
   owns the heavier stall-detection/recovery work that doesn't need to be
   instant. */
var sfBoundVideo=null;
function fastLiveCheck(){
var v=document.querySelector("video");
if(!v)sfLiveReset();                     /* nothing playing: forget the answer */
if(v&&v!==sfBoundVideo){
sfLiveReset();                           /* a different item is starting */
/* isLiveCandidate() leans on v.duration, which the DOM doesn't know
   about the instant <video> is inserted -- it only becomes accurate
   once the browser has loaded stream metadata, an async media event
   with no corresponding DOM mutation. Without this, the class flip
   was stuck waiting for the next unrelated DOM change (or the 1s
   interval fallback) to re-check, which is exactly the split-second
   flash of stock controls the observer alone didn't close. */
sfBoundVideo=v;
v.addEventListener("loadedmetadata",fastLiveCheck);
v.addEventListener("durationchange",fastLiveCheck);
}
var live=isLiveCandidate(v);
document.documentElement.classList.toggle("sf-live",live);
if(live){sfHideLiveBookmark();moveTitleIfNeeded();}else moveTitleBack();
}
new MutationObserver(fastLiveCheck).observe(document.body,{childList:true,subtree:true});
fastLiveCheck();
setInterval(function(){
var v=document.querySelector("video");
var live=isLiveCandidate(v);
document.documentElement.classList.toggle("sf-live",live);
if(live)moveTitleIfNeeded();else moveTitleBack();
if(!v||!live){lc=-1;lastProgressAt=0;seekFails=0;return;}
if(v.paused&&!v.ended){try{v.play();}catch(e){}}
var hasEdge=v.seekable&&v.seekable.length>0;
if(hasEdge){
var edge=v.seekable.end(v.seekable.length-1);var behind=edge-v.currentTime;
if(behind>24){if(v.playbackRate!==1.08)v.playbackRate=1.08;}else if(behind<10){if(v.playbackRate!==0.99)v.playbackRate=0.99;}else if(v.playbackRate!==1){v.playbackRate=1.0;}
}
var ct=v.currentTime;
if(lc<0){lc=ct;lastProgressAt=Date.now();return;}
if(Math.abs(ct-lc)>=0.05){
/* genuine forward progress -- all clear, reset the staleness clock */
lc=ct;lastProgressAt=Date.now();seekFails=0;
return;
}
lc=ct;
var stalledMs=Date.now()-lastProgressAt;
if(stalledMs<10000)return;
/* stale for 10s+: try to recover. Prefer seeking near the live edge if we
   have one; if the buffer is too degraded to even offer a seekable range
   (readyState/seekable both empty -- the actual failure mode confirmed via
   the F1 stall), fall back to v.load() to force the element to re-fetch
   its source, which doesn't depend on any existing buffered range at all. */
if(hasEdge){try{v.currentTime=Math.max(0,v.seekable.end(v.seekable.length-1)-12);v.play();}catch(e){}}
else{try{v.load();v.play();}catch(e){}}
seekFails++;
lastProgressAt=Date.now()-7000;
/* recovery attempts didn't help after ~3 tries (~30s wedged): the upstream
   feed itself is stuck, which only a fresh bridge connection fixes.
   Auto-reload ONCE (what the user used to do by hand), guarded so we never
   reload-loop. */
if(seekFails>=3&&!reloadedRecently()){
try{sessionStorage.setItem("sfReloadAt",""+Date.now());}catch(e){}
var doReload=function(){location.reload();};
if(window.__sfLiveTvStashResume){
/* __sfLiveTvStashResume is now async (queries Jellyfin's own /Sessions API
   for the truly-current item -- see sf-livetv-resume) -- must wait for it
   to finish writing sessionStorage before reloading, or the reload can win
   the race and the stash never lands. Reload happens either way; a failed
   stash just means boot-time resume finds nothing and falls back to the
   pre-existing "bounces to home" behavior, never worse than that. */
var p=window.__sfLiveTvStashResume();
if(p&&typeof p.then==="function")p.then(doReload,doReload);else doReload();
}else{
doReload();
}
}
},1000);
})();</script>'''

# --- Live TV guide: sub-filter pills (All / Live Sports / Movies & TV) injected
# below Jellyfin's top Home/Programs/Guide/Channels pills. Jellyfin can't group
# the guide natively, so we partition the rendered rows by channel number
# (sports live on 500+, ErsatzTV entertainment on 1-88) and show/hide the matched
# channel-header + program-row pairs so they stay aligned. Choice persists.
GUIDEFILTER_MARKER = 'sf-guide-filter'
GUIDEFILTER_SCRIPT = r'''<script>(function(){
/* sf-guide-filter */
var css='.sf-guidefilter{display:flex;gap:.5em;padding:.4em 1em;justify-content:center;align-items:center;background:rgba(0,0,0,.35);position:relative;z-index:2;flex-wrap:wrap;box-sizing:border-box;}'
+'.sf-gf-pill{background:rgba(255,255,255,.09);color:#cfcfcf;border:none;border-radius:20px;padding:.3em 1em;font-size:.8em;font-weight:600;cursor:pointer;line-height:1.3;font-family:inherit;white-space:nowrap;}'
+'.sf-gf-pill:hover{background:rgba(255,255,255,.18);}'
+'.sf-gf-active{background:#fff;color:#111;}';
var st=document.createElement('style');st.textContent=css;document.head.appendChild(st);
function getF(){try{return localStorage.getItem('sfGuideFilter')||'sports';}catch(e){return 'sports';}}
function setF(v){try{localStorage.setItem('sfGuideFilter',v);}catch(e){}}
function apply(){
var heads=document.querySelectorAll('.channelsContainer .guide-channelHeaderCell');
var grid=document.querySelector('.programGrid');if(!grid)return;
var rows=grid.querySelectorAll(':scope > .channelPrograms');
if(!heads.length||heads.length!==rows.length)return;
var f=getF();
for(var i=0;i<heads.length;i++){
var n=heads[i].querySelector('.guideChannelNumber');
var num=n?parseInt(n.textContent.trim(),10):NaN;
var sport=num>=500;
/* Restored native "Live Sports" grid-filter (2026-07-25): the card browse
   page (sf-livesports) moved to the Programs tab instead of living behind a
   Guide-tab pill, so the Guide's own 3 pills are back to purely filtering
   this native time-grid -- no 'cards' mode here anymore. */
var show=f==='all'||(f==='sports'&&sport)||(f==='tv'&&!sport);
heads[i].style.display=show?'':'none';rows[i].style.display=show?'':'none';
}
}
/* The guide (.tvguide) is absolutely positioned starting UNDER the fixed header,
   so a bar at its top collides with the Home/Programs/Guide/Channels pills. Push
   the bar down to clear the header's bottom edge; recomputed each tick so it
   adapts to any screen size / header height. */
function place(bar){
var tv=document.querySelector('.tvguide');if(!tv||!bar)return;
var hdr=document.querySelector('.skinHeader')||document.querySelector('.emby-tabs-slider');if(!hdr)return;
var need=Math.round(hdr.getBoundingClientRect().bottom-tv.getBoundingClientRect().top);
bar.style.marginTop=(need>0?need:0)+'px';
}
function ensure(){
var tv=document.querySelector('.tvguide');if(!tv)return null;
var bar=tv.querySelector('.sf-guidefilter');
if(bar)return bar;
bar=document.createElement('div');bar.className='sf-guidefilter';
/* "All" pill removed 2026-07-25 at user's request -- just Live Sports and
   Movies & TV now. getF() defaults to 'sports' rather than 'all' so a fresh
   install (no localStorage yet) lands on a pill that's actually in the bar;
   apply()'s f==='all' branch is left in place since it's harmless dead code
   for anyone whose localStorage still has 'all' saved from before. */
[['sports','Live Sports'],['tv','Movies & TV']].forEach(function(p){
var b=document.createElement('button');b.className='sf-gf-pill'+(p[0]===getF()?' sf-gf-active':'');b.textContent=p[1];
b.onclick=function(){setF(p[0]);[].forEach.call(bar.children,function(x){x.classList.remove('sf-gf-active');});b.classList.add('sf-gf-active');apply();};
bar.appendChild(b);
});
tv.insertBefore(bar,tv.firstChild);
return bar;
}
/* Mouse-wheel scrolling never moved the channel list (reported as "cannot
   scroll down on these guide tabs"). Root cause isn't anything in this
   patch -- confirmed live that even Jellyfin's own untouched Home page
   carousels don't respond to a real wheel event either (tested by
   dispatching a trusted WheelEvent directly), while setting .scrollTop by
   hand moves the view fine. So this Jellyfin build's own custom scroller
   just isn't wired up to wheel input in this browser context at all; we
   supply our own handler rather than relying on it. Guarded by a dataset
   flag so the listener is attached once per element, not once per 800ms
   tick. */
function ensureWheelScroll(){
var scroller=document.querySelector('.guideVerticalScroller');
if(!scroller||scroller.dataset.sfWheelFix)return;
scroller.dataset.sfWheelFix='1';
scroller.addEventListener('wheel',function(e){
var max=scroller.scrollHeight-scroller.clientHeight;
if(max<=0)return;
var next=Math.max(0,Math.min(max,scroller.scrollTop+e.deltaY));
if(next!==scroller.scrollTop){scroller.scrollTop=next;}
e.preventDefault();
},{passive:false});
}
setInterval(function(){var bar=ensure();place(bar);apply();ensureWheelScroll();},800);
})();</script>'''

CHANNELCARDS_MARKER = 'sf-channelcards'
CHANNELCARDS_SCRIPT = r'''<script>(function(){
/* sf-channelcards */
var css='.sf-cc-overlay{position:absolute;inset:0;z-index:3;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;padding:.5em;box-sizing:border-box;}'
+'.sf-cc-icon{font-size:2.6em;line-height:1;margin-bottom:.15em;filter:drop-shadow(0 2px 4px rgba(0,0,0,.35));}'
+'.sf-cc-label{color:rgba(255,255,255,.92);font-weight:700;font-size:.95em;line-height:1.25;}'
+'.sf-cc-sub{color:rgba(255,255,255,.6);font-size:.75em;margin-top:.25em;font-weight:600;letter-spacing:.02em;text-transform:uppercase;}'
+'.cardImageContainer.sf-cc-done{overflow:hidden;background-image:none!important;background:var(--sf-cc-bg)!important;}'
/* Channels with NO tvg-logo at all (the Upcoming-lane placeholders) don't
   get a background-image from Jellyfin -- instead it renders an actual
   visible DOM fallback (.cardDefaultText: big channel number + clock icon +
   title) as a sibling of .cardImageContainer's content, not a background,
   so background-image:none above doesn't touch it. Hide it directly. */
+'.cardImageContainer.sf-cc-done .cardDefaultText{display:none!important;}';
var st=document.createElement('style');st.textContent=css;document.head.appendChild(st);

/* ErsatzTV channels whose own logo is just auto-generated text-on-black
   (ErsatzTV's /logos/gen?text= placeholder -- confirmed via its M3U output;
   only channels 2 "Comfort Comedy" and 8 "Prestige Drama" have real uploaded
   artwork). Keyed by channel NUMBER, parsed from the Channels tab's card
   title ("1 LU TV" -> 1). Only affects the Channels tab -- the Programs tab
   already shows the real airing episode/movie's own poster for these, which
   is already correct. */
var ERSATZ_STYLE={
1:{icon:'📺',c1:'#7c3aed',c2:'#4c1d95'},
4:{icon:'🏰',c1:'#f59e0b',c2:'#b45309'},
5:{icon:'💥',c1:'#ef4444',c2:'#7f1d1d'},
6:{icon:'🕵️',c1:'#1e293b',c2:'#020617'},
7:{icon:'💕',c1:'#ec4899',c2:'#831843'},
9:{icon:'🚀',c1:'#06b6d4',c2:'#164e63'},
10:{icon:'🎬',c1:'#3730a3',c2:'#1e1b4b'},
12:{icon:'🎨',c1:'#f97316',c2:'#7c2d12'},
88:{icon:'💗',c1:'#f472b6',c2:'#9d174d'}
};
var SPORT_ICONS={'racing':'🏁','motorsport':'🏁','soccer':'⚽','basketball':'🏀','football':'🏈','american football':'🏈','combat sports':'🥊','fight':'🥊','baseball':'⚾'};
function sportIcon(s){return SPORT_ICONS[String(s||'').toLowerCase()]||'🏆';}

function buildOverlay(icon,label,sub){
var wrap=document.createElement('div');wrap.className='sf-cc-overlay';
var i=document.createElement('div');i.className='sf-cc-icon';i.textContent=icon;
wrap.appendChild(i);
if(label){var l=document.createElement('div');l.className='sf-cc-label';l.textContent=label;wrap.appendChild(l);}
if(sub){var s=document.createElement('div');s.className='sf-cc-sub';s.textContent=sub;wrap.appendChild(s);}
return wrap;
}

function enhance(card){
if(card.classList.contains('sf-cc-scanned'))return;
var titleEl=card.querySelector('.cardText,.cardTitle');
var title=titleEl?titleEl.textContent.trim():'';
if(!title)return;
var ic=card.querySelector('.cardImageContainer');
if(!ic)return;
card.classList.add('sf-cc-scanned');

var numMatch=title.match(/^(\d+)\s+(.+)$/);
if(numMatch&&ERSATZ_STYLE[+numMatch[1]]){
var st=ERSATZ_STYLE[+numMatch[1]];
/* Set via CSS custom property + a !important rule (above), not
   ic.style.background directly -- Jellyfin's own lazy-image loader can
   re-apply its background-image inline AFTER this runs (confirmed live:
   the real ErsatzTV auto-gen text logo re-appeared behind our overlay a
   moment after being overridden with a plain inline style). A custom
   property isn't touched by that, and !important beats Jellyfin's
   non-important inline background-image whenever it re-sets it. */
ic.style.setProperty('--sf-cc-bg','linear-gradient(160deg,'+st.c1+','+st.c2+')');
ic.classList.add('sf-cc-done');
ic.appendChild(buildOverlay(st.icon,numMatch[2]));
return;
}

/* Channels tab prefixes the visible channel number onto the title text
   ("590 🕐 Upcoming Football"), unlike Programs tab which doesn't -- the
   leading (?:\d+\s+)? handles both. */
var upcomingMatch=title.match(/^(?:\d+\s+)?🕐\s*Upcoming\s+(.+)$/i);
if(upcomingMatch){
ic.style.setProperty('--sf-cc-bg','linear-gradient(160deg,#1e1e2a,#0d0d13)');
ic.classList.add('sf-cc-done');
ic.appendChild(buildOverlay(sportIcon(upcomingMatch[1]),null,'Upcoming '+upcomingMatch[1]));
return;
}

if(/^(?:\d+\s+)?🔴\s*LIVE \(Streamed\)/i.test(title)){
ic.style.setProperty('--sf-cc-bg','linear-gradient(160deg,#1e1e2a,#0d0d13)');
ic.classList.add('sf-cc-done');
ic.appendChild(buildOverlay('🕒',null,'Not yet playable'));
return;
}
}

function scan(){
/* Live TV pages ONLY. enhance() identifies a channel by parsing a leading
   number off the card title (/^(\d+)\s+(.+)$/) and looking it up in
   ERSATZ_STYLE -- but scan() ran on every page via a body-wide
   MutationObserver plus a 1s interval, so any LIBRARY title beginning with a
   digit that collides with a channel number got replaced by a themed
   placeholder. "12 Angry Men" -> channel 12 -> the orange gradient with the
   palette icon, poster gone. Other collisions in ERSATZ_STYLE (1,4,5,6,7,9,
   10,12,88) would hit e.g. "10 Things I Hate About You". The header comment
   always claimed "only affects the Channels tab"; this makes that true. */
if(!/livetv/i.test(location.hash||''))return;
var cards=document.querySelectorAll('.card:not(.sf-cc-scanned)');
for(var i=0;i<cards.length;i++)enhance(cards[i]);
}
new MutationObserver(scan).observe(document.body,{childList:true,subtree:true});
scan();
setInterval(scan,1000);
})();</script>'''

# --- Guide layout (2026-08-23). Three separate defects in the Live TV guide,
# all measured at 1440x900 and 1280x800:
#
# 1. CHANNEL NAMES CLIPPED TO ~40%. `.guideChannelName` is 69px wide inside a
#    173px cell (the logo and channel number take the first 88px), with
#    white-space:nowrap and overflow:hidden. Measured scrollWidth vs clientWidth:
#    "Upcoming Baseball" 152/69, "Upcoming Basketball" 164/69, "Upcoming Combat
#    Sports" 197/69. The cell is 74px TALL and the name uses only 25px of it, so
#    the room is vertical, not horizontal -- wrap to three lines instead of
#    widening the column, which would shift the whole grid. Four because
#    "Upcoming Combat Sports" breaks as clock/Upcoming/Combat/Sports and still
#    clipped at three; 4 lines x 15.1px = 60px inside a 74px cell.
#
# 2. THE "NOW" BADGE SITS ON THE TIME LABEL. #jf-now-label is bottom-anchored
#    inside .timeslotHeadersInner, which is precisely where .timeslotHeader
#    paints its text. Measured badge [474,252,63,24] against slot [424,238,243,38]
#    -- 100% of the badge's area covers the "2:30 pm" label. Hang it BELOW the
#    header instead, where it caps the red now-line and covers nothing.
#
# 3. EMPTY PROGRAMME LANES WITH NO EXPLANATION. 28 of 39 channels have no EPG at
#    all -- they are per-event sports channels ("Houston Astros vs Athletics",
#    "Upcoming Football") where the channel NAME is the event. Their
#    .channelPrograms lane is genuinely childless and collapses to 0x0, leaving a
#    silent void beside the channel. Say so, and keep the message pinned to the
#    left edge with position:sticky -- the lane is 11,664px wide, so text placed
#    at x=0 would only be visible at the extreme left of a horizontal scroll.
GUIDEFIX_MARKER = 'sf-guide-fix'
GUIDEFIX_STYLE = ('<style id="sf-guide-fix">'
                  '.guideChannelName{white-space:normal!important;overflow:hidden!important;'
                  'display:-webkit-box!important;-webkit-box-orient:vertical!important;'
                  '-webkit-line-clamp:4!important;line-clamp:4!important;'
                  'font-size:13px!important;line-height:1.16!important;'
                  'text-overflow:clip!important;word-break:break-word!important;}'
                  # top:100% pushed it OUT of .timeslotHeaders, which is
                  # overflow-y:hidden -- it vanished entirely, and an overlap
                  # check passed for the WRONG REASON (0% overlap because the
                  # element was invisible). Keep it inside the header, but lift
                  # the slot text to the top of its 38px box -- the text is only
                  # 17px tall, sitting at 248-265 -- so the bottom strip is free.
                  '.timeslotHeader{align-items:flex-start!important;}'
                  # size/padding live in the now-line script's own rule, which is
                  # injected at runtime and therefore wins any tie with this block.
                  '#jf-now-label{bottom:0!important;top:auto!important;}'
                  # The lane's flex origin is the START of an 11,664px timeline, which is scrolled
                  # out of view, so the message cannot be pinned beside its channel with CSS
                  # alone -- 100vw+sticky pushed it further right (955px), not left. It lands
                  # at a consistent x across every empty row, which reads deliberately enough;
                  # true left-pinning would need JS tracking scrollLeft, and is not worth a
                  # scroll handler on this box for a cosmetic gain.
                  '.channelPrograms:empty{display:flex!important;align-items:center!important;'
                  'min-height:74px!important;width:100%!important;}'
                  '.channelPrograms:empty::before{content:"No guide data";'
                  'padding-left:16px!important;'
                  'color:rgba(255,255,255,.34)!important;font-size:12.5px!important;'
                  'font-style:italic!important;white-space:nowrap!important;'
                  'pointer-events:none!important;}'
                  '</style>')

# --- Hero layout (2026-08-02). The CSS version of this used FIXED PIXEL
# constants -- a 433px row reserve, a 115px logo, and per-element translateY
# offsets tuned by hand at 1440x767. Every one of those breaks on a different
# screen, and the admin hit all three on an ultrawide: text squished, Play button
# misaligned, first row clipped.
#
# Why fixed px cannot work here: Jellyfin's card height scales with viewport
# WIDTH (posters are a fraction of the row), so a wider screen makes the first
# row TALLER. A reserve measured at 1440 under-reserves at 3440 and the row is
# cut off. Meanwhile Media Bar positions hero elements in vh, so the two scale
# on different axes and drift apart at any aspect ratio that is not the one they
# were tuned at.
#
# So this measures instead of assuming:
#   * ALIGNMENT  - reads the description's actual computed left edge and puts the
#                  button row on exactly that x. Works whatever Media Bar uses,
#                  at any width, without hardcoding 5%.
#   * SPACING    - walks the stack top-down (logo -> year -> genre -> synopsis ->
#                  buttons), placing each element a measured gap below the
#                  previous one's real rendered bottom. Gap scales with viewport
#                  height and is clamped to 10-24px so it never squishes on a
#                  short ultrawide nor sprawls on a tall 4K panel.
#   * ROW FIT    - self-correcting: want = currentTop + (viewportHeight -
#                  cardBottom). No constant at all. Converges in one pass and is
#                  a no-op once flush, so it cannot oscillate. Clamped so the row
#                  title always clears the Play button.
#
# Gaps are measured off `.plot` (the clamped TEXT), never `.plot-container`,
# which stays a fixed tall box regardless of how many lines actually render.
#
# Below 768px wide it REMOVES every inline override and hands the hero back to
# Media Bar, which centres it and hides the synopsis -- that layout is correct on
# phones and must not be fought (an earlier CSS attempt to force left:5% at all
# widths pushed the Play button to left:-29px, half off screen).
#
# The cut was 1000 until 2026-08-28. Between 768 and 999 Media Bar does NOT use
# the phone layout -- it uses the same left-aligned desktop SHAPE (logo, chips,
# progress bar, synopsis, buttons) with the static vh offsets of the
# sf-hero-midwidth CSS band, and those offsets are tuned at one aspect while the
# element heights they space are px/em based. So the gaps drifted apart, badly:
#
#     size        logo>chips  chips>synopsis  synopsis>buttons
#     1000x900 JS     45            30              15
#      990x900        32            61               6
#      900x900        32            61               6
#      768x1024       34            71              17
#      834x1112       35            78              25
#
# A 61-78px hole above the synopsis and 6px under it, plus a hard step at the
# 1000px boundary. This is exactly what measuring instead of assuming fixes, so
# the cut moved down to where Media Bar actually changes layout: 768, the top of
# its portrait band. Phones are untouched and still look right.
#
# The CSS blocks stay as a static baseline so a JS failure degrades to the
# current desktop look rather than to nothing; inline !important outranks
# stylesheet !important, so this refines them wherever it runs.
LIVETVPANE_MARKER = 'jf-livetv-pane'
# Live TV as a HOME PANE (#/home?livetv=1), 2026-08-29.
#
# the admin: "i feel like you should just rebuild live tv as a home pane".
#
# This is NOT the 2026-08-10 alias that was reverted. That one navigated to the
# real #/livetv, let Jellyfin mount liveTvSuggestedPage, and then rewrote the
# address bar -- which is why the true URL always painted first, why Back became
# a trap (history said /home while a Live TV page was mounted) and why Back out
# of a programme left every page hidden. See
# jellyfin-livetv-route-and-pane-guard.
#
# Here NOTHING is navigated. #/home?livetv=1 is a real home URL, home stays
# mounted, and this overlay renders the Live TV landing content itself -- the
# same shape sf-livesports already uses for #/home?sports=1, which is the
# working precedent in this file. So there is no second URL to rewrite, no
# history entry that disagrees with the mounted page, and the pill stops
# flickering because the header strip is never torn down at all.
#
# What the real page actually is, measured on liveTvSuggestedPage: not a guide
# grid, just card rows off two endpoints --
#     On Now                   LiveTv/Programs/Recommended?IsAiring=true
#     Movies/Shows/Kids/...    LiveTv/Programs?HasAired=false&IsMovie=...
# The Guide, Channels and Recordings GRIDS are separate tabs, so they keep their
# own real routes and are linked from the top of the pane rather than rebuilt.
LIVETVPANE_SCRIPT = r'''<script>(function(){ /* jf-livetv-pane */
/* Sub-views, addressed as #/home?livetv=1&sub=N so a reload lands where you were.
   0 Programs, 1 Guide, 2 Channels -- the same three the old page had, in the same
   order, so the existing .jf-ltv-sub capsule can drive them unchanged. */
var SUBS=['Programs','Guide','Channels'];
var root=null,timer=null,loading=false,lastAt=0,lastSub=-1;
function on(){return (location.hash||'').indexOf('livetv=1')>=0;}
function sub(){
var h=location.hash||'',i=h.indexOf('sub=');
if(i<0)return 0;
var n=parseInt(h.substr(i+4),10);
return (n>=0&&n<SUBS.length)?n:0;
}
function ac(){return window.ApiClient;}
function css(){
if(document.getElementById('sf-lvp-css'))return;
var s=document.createElement('style');s.id='sf-lvp-css';
s.textContent=
/* z-index 40, deliberately BELOW .jf-ltv-sub (41) and the header. At 50 the
   pane painted over the Programs/Guide/Channels capsule and swallowed its
   clicks -- the pills were still visible but completely inert, which is exactly
   the "sub tabs dont work properly" report. The pane's padding-top already
   clears both bars, so sitting under them is also the correct scroll behaviour. */
'.sf-lvp-root{position:fixed;left:0;right:0;top:0;bottom:0;z-index:40;overflow-y:auto;'
+'background:#0d0d12;display:none;}'
+'.sf-lvp-root.sf-lvp-show{display:block;}'
+'.sf-lvp-h{margin:0 0 .7em var(--sf-rail,4vw);font-size:1.5rem;font-weight:600;}'
+'.sf-lvp-grid{display:flex;flex-wrap:wrap;gap:1.4em 1.1em;'
+'padding:0 var(--sf-rail,4vw) 2em;}'
+'.sf-lvp-card{flex:0 0 auto;width:11.5em;text-decoration:none;color:inherit;}'
+'.sf-lvp-img{position:relative;width:100%;aspect-ratio:2/3;border-radius:10px;'
+'background:#1b1b22 center/cover no-repeat;overflow:hidden;}'
+'.sf-lvp-ch .sf-lvp-img{aspect-ratio:1/1;background-size:contain;background-color:#15151c;}'
+'.sf-lvp-bar2{position:absolute;left:8%;right:8%;bottom:7px;height:3px;border-radius:2px;'
+'background:rgba(255,255,255,.3);overflow:hidden;}'
+'.sf-lvp-bar2 i{display:block;height:100%;background:#fff;}'
+'.sf-lvp-t{margin-top:.5em;font-size:.95em;font-weight:500;line-height:1.25;'
+'display:-webkit-box;-webkit-line-clamp:1;-webkit-box-orient:vertical;overflow:hidden;}'
+'.sf-lvp-s{font-size:.85em;opacity:.6;margin-top:.15em;'
+'white-space:nowrap;overflow:hidden;text-overflow:ellipsis;}'
+'.sf-lvp-empty{padding:2em var(--sf-rail,4vw);opacity:.6;}'
+'.sf-lvp-gsec{margin-bottom:1.6em;}'
+'.sf-lvp-gch{display:flex;align-items:center;gap:.7em;margin:0 0 .5em var(--sf-rail,4vw);}'
+'.sf-lvp-glogo{width:2.1em;height:2.1em;border-radius:6px;background:#15151c center/contain no-repeat;flex:0 0 auto;}'
+'.sf-lvp-gname{font-size:1.02em;font-weight:600;}'
+'@media (max-width:520px){.sf-lvp-card{width:8.6em;}.sf-lvp-h{font-size:1.2rem;}}'
/* The home page keeps its own secondary pill rows mounted -- My Stuff leaves
   Favorites/Watchlist/Bookmarks behind, and they sat on top of this pane because
   the pane covers the CONTENT, not the header. Hide every sub-pill row except
   the Live TV one while the pane owns the screen. */
+'body.sf-lvp-on #favoritesTab .jf-fav-tabs,'
+'body.sf-lvp-on #indexPage .jf-fav-tabs,'
+'body.sf-lvp-on .sf-lib-pills{display:none!important;}';
document.head.appendChild(s);
}
function ensureRoot(){
if(root&&root.isConnected)return root;
css();
root=document.createElement('div');
root.className='sf-lvp-root';
document.body.appendChild(root);
return root;
}
function pad(n){return n<10?('0'+n):(''+n);}
function clock(d){
try{var t=new Date(d),h=t.getHours(),m=pad(t.getMinutes());
var ap=h<12?'AM':'PM',h12=h%12; if(!h12)h12=12;
return h12+':'+m+' '+ap;}catch(e){return '';}
}
function span(it){
if(!it.StartDate)return '';
var a=clock(it.StartDate);
return it.EndDate?(a+' - '+clock(it.EndDate)):a;
}
/* Season/episode come back as ParentIndexNumber/IndexNumber on a BaseItemDto --
   SeasonNumber/EpisodeNumber are not populated here, so keying only on those
   printed "Pulp Friction" where the old page showed "S5:E17 - Pulp Friction". */
function epLine(it){
var se=(it.SeasonNumber!=null)?it.SeasonNumber:it.ParentIndexNumber;
var ep=(it.EpisodeNumber!=null)?it.EpisodeNumber:it.IndexNumber;
var s='';
if(se!=null&&ep!=null)s='S'+se+':E'+ep;
if(it.EpisodeTitle)s=s?(s+' - '+it.EpisodeTitle):it.EpisodeTitle;
return s;
}
function pct(it){
try{
var s=new Date(it.StartDate).getTime(),e=new Date(it.EndDate).getTime(),n=Date.now();
if(!(e>s))return -1;
if(n<s||n>e)return -1;
return Math.max(0,Math.min(1,(n-s)/(e-s)));
}catch(err){return -1;}
}
function imgFor(it,id,tag){
var a=ac();if(!a)return '';
try{return a.getImageUrl(id,{type:'Primary',maxWidth:400,tag:tag});}catch(e){return '';}
}
function card(it){
var a=ac();
var el=document.createElement('a');
el.className='sf-lvp-card';
el.setAttribute('href','#/details?id='+it.Id+'&serverId='+(it.ServerId||(a&&a.serverId&&a.serverId())||''));
var im=document.createElement('div');im.className='sf-lvp-img';
var u='';
if(it.ImageTags&&it.ImageTags.Primary)u=imgFor(it,it.Id,it.ImageTags.Primary);
else if(it.ChannelPrimaryImageTag&&it.ChannelId)u=imgFor(it,it.ChannelId,it.ChannelPrimaryImageTag);
if(u)im.style.backgroundImage='url("'+u+'")';
var p=pct(it);
if(p>=0){
var bw=document.createElement('div');bw.className='sf-lvp-bar2';
var fi=document.createElement('i');fi.style.width=Math.round(p*100)+'%';
bw.appendChild(fi);im.appendChild(bw);
}
var t=document.createElement('div');t.className='sf-lvp-t';t.textContent=it.Name||'';
el.appendChild(im);el.appendChild(t);
var ep=epLine(it);
if(ep){var e1=document.createElement('div');e1.className='sf-lvp-s';e1.textContent=ep;el.appendChild(e1);}
var sp=span(it);
if(sp){var e2=document.createElement('div');e2.className='sf-lvp-s';e2.textContent=sp;el.appendChild(e2);}
return el;
}
function chanCard(ch){
var a=ac();
var el=document.createElement('a');
el.className='sf-lvp-card sf-lvp-ch';
el.setAttribute('href','#/details?id='+ch.Id+'&serverId='+(ch.ServerId||(a&&a.serverId&&a.serverId())||''));
var im=document.createElement('div');im.className='sf-lvp-img';
if(ch.ImageTags&&ch.ImageTags.Primary){
var u=imgFor(ch,ch.Id,ch.ImageTags.Primary);
if(u)im.style.backgroundImage='url("'+u+'")';
}
var t=document.createElement('div');t.className='sf-lvp-t';
t.textContent=(ch.ChannelNumber?(ch.ChannelNumber+'  '):'')+(ch.Name||'');
el.appendChild(im);el.appendChild(t);
var cur=ch.CurrentProgram;
if(cur){
var e1=document.createElement('div');e1.className='sf-lvp-s';e1.textContent=cur.Name||'';
el.appendChild(e1);
var e2=document.createElement('div');e2.className='sf-lvp-s';e2.textContent=span(cur);
el.appendChild(e2);
}
return el;
}
function getJSON(name,p){
var a=ac();if(!a)return Promise.resolve(null);
return a.getJSON(a.getUrl(name,p)).catch(function(){return null;});
}
function programs(extra){
var a=ac();if(!a)return Promise.resolve([]);
var p={userId:a.getCurrentUserId(),limit:60,ImageTypeLimit:1,
 EnableImageTypes:'Primary',EnableTotalRecordCount:false,Fields:'ChannelInfo'};
for(var k in extra)p[k]=extra[k];
return getJSON('LiveTv/Programs/Recommended',p).then(function(r){return (r&&r.Items)?r.Items:[];});
}
function channels(){
var a=ac();if(!a)return Promise.resolve([]);
return getJSON('LiveTv/Channels',{userId:a.getCurrentUserId(),limit:200,
 ImageTypeLimit:1,EnableImageTypes:'Primary',EnableTotalRecordCount:false,
 AddCurrentProgram:true}).then(function(r){return (r&&r.Items)?r.Items:[];});
}
function head(txt){var h=document.createElement('h2');h.className='sf-lvp-h';h.textContent=txt;return h;}
function grid(){var g=document.createElement('div');g.className='sf-lvp-grid';return g;}
function empty(r,txt){var e=document.createElement('div');e.className='sf-lvp-empty';e.textContent=txt;r.appendChild(e);}
function renderPrograms(r,items){
r.appendChild(head('On Now'));
if(!items.length){empty(r,'Nothing is airing right now.');return;}
var g=grid();
for(var i=0;i<items.length;i++)g.appendChild(card(items[i]));
r.appendChild(g);
}
function renderChannels(r,items){
r.appendChild(head('Channels'));
if(!items.length){empty(r,'No channels available.');return;}
var g=grid();
for(var i=0;i<items.length;i++)g.appendChild(chanCard(items[i]));
r.appendChild(g);
}
/* Guide: what is on each channel now, channel by channel. The real Guide tab is
   a scrolling EPG grid; this is the same information in the pane's idiom rather
   than a reimplementation of that grid, and it is built from the SAME
   AddCurrentProgram payload the Channels view already fetches. */
function renderGuide(r,items){
r.appendChild(head('Guide'));
var withProg=items.filter(function(c){return c.CurrentProgram;});
if(!withProg.length){empty(r,'No guide data available.');return;}
for(var i=0;i<withProg.length;i++){
var ch=withProg[i];
var sec=document.createElement('div');sec.className='sf-lvp-gsec';
var hd=document.createElement('div');hd.className='sf-lvp-gch';
var lg=document.createElement('div');lg.className='sf-lvp-glogo';
if(ch.ImageTags&&ch.ImageTags.Primary){
var u=imgFor(ch,ch.Id,ch.ImageTags.Primary);
if(u)lg.style.backgroundImage='url("'+u+'")';
}
var nm=document.createElement('div');nm.className='sf-lvp-gname';
nm.textContent=(ch.ChannelNumber?(ch.ChannelNumber+'  '):'')+(ch.Name||'');
hd.appendChild(lg);hd.appendChild(nm);
var g=grid();
g.appendChild(card(ch.CurrentProgram));
sec.appendChild(hd);sec.appendChild(g);
r.appendChild(sec);
}
}
function load(force){
var s=sub();
if(loading)return;
if(!force&&s===lastSub&&Date.now()-lastAt<60000&&root&&root.firstChild)return;
loading=true;lastAt=Date.now();lastSub=s;
var job=(s===0)?programs({IsAiring:true}):channels();
job.then(function(data){
loading=false;
var r=ensureRoot();
r.innerHTML='';
if(s===0)renderPrograms(r,data);
else if(s===1)renderGuide(r,data);
else renderChannels(r,data);
sizeRoot();
}).catch(function(){loading=false;});
}
function sizeRoot(){
if(!root)return;
var h=document.querySelector('.skinHeader');
var b=h?Math.round(h.getBoundingClientRect().bottom):64;
var s=document.querySelector('.jf-ltv-sub');
if(s&&s.getBoundingClientRect().height>2)b=Math.max(b,Math.round(s.getBoundingClientRect().bottom));
root.style.paddingTop=(b+16)+'px';
}
function markSub(){
var s=sub(),i;
var btns=document.querySelectorAll('.jf-ltv-sub .jf-fav-tab');
for(i=0;i<btns.length;i++){
var key=btns[i].getAttribute('data-sf-nav')||btns[i].textContent.trim();
btns[i].classList.toggle('jf-fav-tab-active',key===SUBS[s]);
}
}
function show(){
var r=ensureRoot();
sizeRoot();
if(!r.classList.contains('sf-lvp-show')){
r.classList.add('sf-lvp-show');
try{document.body.classList.add('sf-lvp-on');}catch(e){}
if(!timer)timer=setInterval(function(){if(on())load(true);},60000);
}
load(false);
markSub();
}
function hide(){
if(root&&root.classList.contains('sf-lvp-show'))root.classList.remove('sf-lvp-show');
try{document.body.classList.remove('sf-lvp-on');}catch(e){}
if(timer){clearInterval(timer);timer=null;}
}
function sync(){ if(on())show(); else hide(); }
/* Drive the EXISTING .jf-ltv-sub capsule rather than drawing our own row -- it is
   what the old page used, so the look is unchanged. Its own handler calls goTab()
   and then rewrites the URL to #/livetv?tab=N, which is meaningless while home is
   mounted; capture the click first and route it through the home URL instead. */
document.addEventListener('click',function(e){
try{
if(!on())return;
var t=e.target,b=(t&&t.closest)?t.closest('.jf-ltv-sub .jf-fav-tab'):null;
if(!b)return;
var key=b.getAttribute('data-sf-nav')||b.textContent.trim(),i=SUBS.indexOf(key);
if(i<0)return;
e.preventDefault();e.stopPropagation();
if(e.stopImmediatePropagation)e.stopImmediatePropagation();
var url='#/home?livetv=1'+(i?('&sub='+i):'');
try{history.pushState(null,'',url);}catch(err){location.hash=url;}
sync();
}catch(err2){}
},true);
window.addEventListener('hashchange',sync);
window.addEventListener('popstate',sync);
window.addEventListener('resize',sizeRoot);
(function(){
var wrap=function(n){
var o=history[n];
if(!o||o.__sfltv)return;
var f=function(){var v=o.apply(this,arguments);try{sync();}catch(e){}return v;};
f.__sfltv=true;history[n]=f;};
wrap('pushState');wrap('replaceState');
})();
setInterval(function(){ if(on()){sizeRoot();markSub();} },250);
setInterval(sync,60);
/* Build the (hidden) overlay and inject its CSS up front. Created lazily on the
   first click it cost 161ms before the pane covered home, against ~30ms on every
   later switch -- and for that window the home page is what you see, which is
   the flicker on the way in. Costs one empty div at startup. */
try{ensureRoot();}catch(e){}
/* Warm the Programs view once, well after boot. The overlay now covers home the
   instant you press Live TV, which is what stops the home page flashing -- but on
   the very first press it had nothing to draw yet and sat dark for ~230ms.
   Fetching in the background makes that first switch land populated. Deliberately
   late and once: it must not compete with the home page's own load. */
setTimeout(function(){
try{if(!on()&&ac()&&ac().getCurrentUserId())load(false);}catch(e){}
},6000);
sync();
})();</script>'''

# Sports as a real destination, not a Live TV sub-view.
# Pressing the Sports pill goes to #/livetv?tab=0, where Jellyfin swaps the
# header for the LIVE TV tab set (Home/Programs/Guide/Channels/Recordings/
# Schedule/Series) and sf-guide-filter adds its own TV|Sports pill row. So the
# four main tabs vanished and the page read as "Live TV with sports on it".
# While the sf-livesports overlay is up we therefore:
#   - hide Jellyfin's Live TV tab buttons and draw Home / Live TV / Sports /
#     My Stuff instead, with Sports active
#   - hide the sf-guidefilter TV|Sports row, now redundant
# Everything is restored the moment the overlay goes away, and only elements we
# hid ourselves are unhidden (tracked with data-jf-sp-hid) so we never fight
# another patch that legitimately hid something.
SPORTSPAGE_MARKER = 'jf-sports-page'
SPORTSPAGE_SCRIPT = r"""<script>(function(){ /* jf-sports-page */
/* Live TV navigation, two modes on the same #/livetv route:
     SPORTS  = tab 0 + sfProgramsFilter 'sports'  -> only the sports overlay
     LIVE TV = anything else                      -> Programs/Guide/Channels sub-pills
   Why the Sports pill used to "not always work": jf-sports-tab only did
   location.hash='/livetv?tab=0'. The overlay actually keys on
   localStorage.sfProgramsFilter==='sports', so if the user had last clicked the
   TV pill the tab landed on ordinary Programs and looked broken. Every entry
   point below sets the filter explicitly, so the destination is never ambiguous.
   Inline styles are avoided throughout - sf-guide-filter re-asserts its own
   inline display on a timer, and only a stylesheet !important rule beats that. */
/* jf-no-tabflash: display:none removed these from layout entirely, and
   Jellyfin's emby-tabs cannot activate a tab it cannot measure -- which is why
   goTab() used to strip .jf-ltv-nav for the duration of a click. That unhid all
   SIX native tabs (Programs/Guide/Channels/Recordings/Schedule/Series) for
   60-400ms: the flash. Hiding them out of flow instead keeps them measurable
   and clickable while never painting them, so the class stays on permanently
   and there is no window in which they can appear. */
var css='body.jf-ltv-nav .headerTabs.sectionTabs .emby-tabs-slider > *:not(.jf-sp-tab)'
+'{position:absolute!important;left:-9999px!important;top:0!important;'
+'visibility:hidden!important;pointer-events:none!important;}'
+'body.jf-ltv-nav .sf-guidefilter.sf-progfilter{display:none!important;}'
+'body.jf-sports-mode .sf-livesports-root{padding-top:var(--jf-sp-top,90px)!important;}'
+'.jf-ltv-sub{position:fixed;left:0;right:0;z-index:41;display:flex;justify-content:center;pointer-events:none;}'
+'.jf-ltv-sub .jf-fav-tabs{pointer-events:auto;margin:0;}'
/* Clear the floating sub-pill bar. Done in CSS, not inline: sf-livesports
   writes #suggestionsTab.style.paddingTop on a 500ms timer (0px once its own
   pill bar is hidden), so an inline value here just alternated with theirs --
   the reported bouncing. A stylesheet !important rule wins outright and is
   written once. */
+'body.jf-ltv-nav:not(.jf-sports-mode) #suggestionsTab,'
+'body.jf-ltv-nav:not(.jf-sports-mode) #guideTab,'
+'body.jf-ltv-nav:not(.jf-sports-mode) #channelsTab{padding-top:var(--jf-ltv-pad,66px)!important;}';
var st=document.createElement('style');st.id='jf-sports-page-style';st.textContent=css;
(document.head||document.documentElement).appendChild(st);

function onLiveTv(){return window.__sfLtv?window.__sfLtv.is():((location.hash||'').indexOf('#/livetv')===0);}
function curTab(){if(window.__sfLtv)return window.__sfLtv.tab();var m=/[?&]tab=(\d+)/.exec(location.hash||'');return m?parseInt(m[1],10):0;}
function filt(){try{return localStorage.getItem('sfProgramsFilter')||'all';}catch(e){return 'all';}}
function setFilt(v){try{localStorage.setItem('sfProgramsFilter',v);}catch(e){}}
/* The ?tab= query is only honoured on a fresh page load. Once the Live TV page
   is mounted, rewriting location.hash from ?tab=1 to ?tab=0 changes the URL but
   does NOT switch the tab, so anything derived from the hash goes stale. Read
   the actually-visible pane instead, and drive navigation by clicking
   Jellyfin's own (CSS-hidden) tab buttons. */
function paneId(){
var p=[].slice.call(document.querySelectorAll('.pageTabContent')).filter(function(x){return x.offsetParent!==null;})[0];
return p?p.id:'';
}
function dedicatedSports(){return /[?&]sports=1/.test(location.hash||'');}
function sportsMode(){return dedicatedSports();}
function nativeTab(label){
var slider=document.querySelector('.headerTabs.sectionTabs .emby-tabs-slider');
if(!slider)return null;
return [].slice.call(slider.children).filter(function(c){
return !c.classList.contains('jf-sp-tab')&&c.textContent.trim()===label;})[0];
}
/* jf-url-shape: one canonical form for every Live TV URL we emit --
   #/livetv?tab=N. The pill and the sub-pill replaceState already used it; only
   this function's fallback emitted a bare #/livetv. Jellyfin honours ?tab= on a
   FRESH load (see the note above), which is precisely the case this fallback
   handles, so carrying the index also lands the correct pane immediately
   instead of relying solely on the poll-and-click below. */
var TABIDX={'Programs':0,'Guide':1,'Channels':2};

function goTab(label,f){
if(f)setFilt(f);
var b=nativeTab(label);
if(b){
/* Jellyfin's emby-tabs needs the button IN LAYOUT to switch (it measures /
   scrolls the target). Clicking one we had hidden with display:none left the
   page with NO visible pane at all - blank. So drop the hiding class for the
   duration of the click and let the next apply() put it back a tick later. */
/* jf-no-tabflash: the class is NOT removed any more -- see the stylesheet
   note. The native button is off-screen but still in layout, so emby-tabs can
   measure and activate it without it ever becoming visible. */
try{b.click();}catch(e){}
setTimeout(apply,60);
setTimeout(apply,400);
return;
}
var _idx=TABIDX[label];
location.hash=(_idx===undefined)?'#/livetv':('#/livetv?tab='+_idx);
var tries=0;
var iv=setInterval(function(){
tries++;
var t=nativeTab(label);
if(t){
/* Only click if Jellyfin has NOT already selected this tab. It honours ?tab=N on
   load, so by the time the button exists it is usually active already and the
   click is redundant -- and this poll fires ~200ms in, while the Live TV view is
   still initialising, which is when that click made Jellyfin's own bundle throw
   "Cannot find module './'" (it resolves a tab controller for a view that is not
   mounted yet). Clicking the same button once the page has settled is harmless,
   so the guard is on the active state, not on timing. */
if(!/emby-tab-button-active/.test(t.className||'')){try{t.click();}catch(e){}}
clearInterval(iv);
}
if(tries>30)clearInterval(iv);
},200);
}

function goHomeTab(label){
location.hash='#/home';
var tries=0;
var iv=setInterval(function(){
tries++;
var t=[].slice.call(document.querySelectorAll('.headerTabs.sectionTabs .emby-tab-button'))
.filter(function(x){return x.textContent.trim()===label;})[0];
if(t){t.click();clearInterval(iv);}
if(tries>25)clearInterval(iv);
},200);
}
function go(kind){
if(kind==='home')location.hash='#/home';
else if(kind==='mystuff')location.hash='#/home?tab=1';
else if(kind==='livetv')goTab('Programs','all');   /* jf-default-subtab: Programs, not Guide */
else if(kind==='sports'){setFilt('sports');location.hash='#/home?sports=1';}
}
var MAIN=[['Home','home'],['Live TV','livetv'],['Sports','sports'],['My Stuff','mystuff']];
var SUB=[['Programs',0],['Guide',1],['Channels',2]];

function buildMain(slider){
var want=sportsMode()?'Sports':'Live TV';
var have=slider.querySelector('.jf-sp-tab');
if(have){
[].slice.call(slider.querySelectorAll('.jf-sp-tab')).forEach(function(b){
b.classList.toggle('emby-tab-button-active',b.textContent.trim()===want);});
/* No early return. Bailing out as soon as ONE of its tabs existed meant a strip
   that Jellyfin had partially rebuilt was never repaired -- it kept whatever
   half-set was there and the append below added a second copy of the rest
   (measured 首页|直播电视|体育|我的内容|直播电视|体育). The per-destination skip
   below makes running this repeatedly idempotent, so it can just fall through. */
}
MAIN.forEach(function(m){
/* Do NOT re-add a destination the strip already has. buildMain appends the whole
   MAIN set, including Home and My Stuff, which Jellyfin's own home strip already
   provides -- measured 8 buttons in one slider on #/home?sports=1
   (首页|直播电视|体育|我的内容 twice). Matching on the visible label cannot work
   because it is translated, so the check is on a stamped English key. */
if(slider.querySelector('[data-sf-nav="'+m[0]+'"]'))return;
var b=document.createElement('button');
b.type='button';
b.className='emby-button emby-tab-button jf-sp-tab'+(m[0]===want?' emby-tab-button-active':'');
b.setAttribute('data-sf-nav',m[0]);
b.textContent=m[0];
/* Stop the event before Jellyfin's emby-tabs delegation sees it. Our pills
   carry .emby-tab-button (needed for the pill metrics) and live inside
   Jellyfin's own slider, but they have no tab index -- so its handler resolved
   a tab controller for nothing and its bundle threw "Cannot find module './'"
   on every Live TV switch. We do our own navigation, so its handler has no work
   to do here anyway. */
b.addEventListener('click',function(e){
e.preventDefault();e.stopPropagation();
if(e.stopImmediatePropagation)e.stopImmediatePropagation();
go(m[1]);},true);
slider.appendChild(b);
});
}
function subBar(){
var wrap=document.querySelector('.jf-ltv-sub');
if(!wrap){
wrap=document.createElement('div');wrap.className='jf-ltv-sub';
var inner=document.createElement('div');inner.className='jf-fav-tabs';
SUB.forEach(function(sp){
var b=document.createElement('button');b.type='button';b.className='jf-fav-tab';b.textContent=sp[0];
/* keep the ENGLISH name on the element: the visible label is translated by the
   i18n sweep, and the active-state lookup below is keyed on the English one */
b.setAttribute('data-sf-nav',sp[0]);
b.addEventListener('click',function(){goTab(sp[0],'all');
/* jf-subpill-url: Live TV honours ?tab=N on a fresh load, so keeping the URL in
   step makes reload land on the same sub-tab.
   With sf-ltv-realurl there is no longer a second writer racing this one -- the
   alias used to rewrite it ~70ms later (40ms here + up to 30ms of polling, since
   replaceState fires no hashchange), which was a visible address-bar flicker on
   every Programs/Guide/Channels click. The real URL is now the final one. */
setTimeout(function(){try{history.replaceState(null,'','#/livetv?tab='+sp[1]);}catch(e){}},40);});
inner.appendChild(b);
});
wrap.appendChild(inner);document.body.appendChild(wrap);
}
return wrap;
}
var _applying=false, _queued=false;
function apply(){
if(_applying){_queued=true;return;}
_applying=true;
try{_apply();}catch(e){}
_applying=false;
if(_queued){_queued=false;setTimeout(apply,50);}
}
function _apply(){
var sp=sportsMode(), live=onLiveTv()||sp;
if(document.body){
document.body.classList.toggle('jf-ltv-nav',live);
document.body.classList.toggle('jf-sports-mode',sp);
}
var wrap=document.querySelector('.jf-ltv-sub');
/* querySelector used to be enough, but sfMainNav now inserts .jf-mu-mainbar --
   which CONTAINS an .emby-tabs-slider -- ahead of the native strip. The first
   match became OUR bar, so buildMain appended its four pills into it and the
   cleanup only ever swept that one slider. Result on Live TV: the main nav drawn
   three times (8 buttons in our bar, 4 more inside Jellyfin's tab strip). */
var slider=null,_all=document.querySelectorAll('.headerTabs.sectionTabs .emby-tabs-slider'),_i;
for(_i=0;_i<_all.length;_i++){
if(!_all[_i].closest('.jf-mu-mainbar')){slider=_all[_i];break;}
}
/* always sweep EVERY slider, wherever a stale pill ended up */
function sfSpSweep(){
var q=document.querySelectorAll('.jf-sp-tab'),k;
for(k=0;k<q.length;k++)if(q[k].parentNode)q[k].parentNode.removeChild(q[k]);
}
if(!live){
sfSpSweep();
if(wrap)wrap.style.display='none';
return;
}
/* When sfMainNav has already drawn the main pills (any library route), a second
   set here is pure duplication -- so only draw them where that bar does NOT
   exist, which is the sports overlay on #/home. */
/* the latch, not a live lookup -- see sfMainNav: the bar is absent for a frame
   during every rebuild, and testing existence there merged the two bars */
if(window.__sfMainNav||document.querySelector('.jf-mu-mainbar')){sfSpSweep();}
else if(slider)buildMain(slider);
var hdr=document.querySelector('.skinHeader');
var hb=hdr?Math.round(hdr.getBoundingClientRect().bottom):78;
if(hb>0&&document.body)document.body.style.setProperty('--jf-sp-top',(hb+14)+'px');
if(sp){ if(wrap)wrap.style.display='none'; return; }
/* LIVE TV mode: show Programs/Guide/Channels under the main pills */
wrap=subBar();
wrap.style.display='flex';
var _wt=(hb+10)+'px';if(wrap.style.top!==_wt)wrap.style.top=_wt;
var pid=paneId();
var PANE={'Programs':'suggestionsTab','Guide':'guideTab','Channels':'channelsTab'};
/* sf-ltv-subactive-owner (2026-08-29): while the Live TV HOME PANE owns the
   screen it is the source of truth for which sub-pill is active, not this.
   This maps the pills to Jellyfin's Live TV pane ids, and none of
   suggestionsTab/guideTab/channelsTab exists while #indexPage is mounted, so
   paneId() matched nothing and every pill was cleared -- then the pane's own
   markSub() set it back 250ms later, and round it went. Measured sitting still
   on the pane: active toggled Programs -> (none) -> Programs every ~400ms,
   indefinitely. That is the flickering sub-tab.
   Off the pane this is unchanged and still owns the state. */
if(!(document.body&&document.body.classList.contains('sf-lvp-on'))){
[].slice.call(wrap.querySelectorAll('.jf-fav-tab')).forEach(function(b){
b.classList.toggle('jf-fav-tab-active',PANE[b.getAttribute('data-sf-nav')||b.textContent.trim()]===pid);});
}
/* push the visible pane clear of the floating bar */
/* Padding is applied by the stylesheet rule above; we only publish the size. */
var need=Math.round(wrap.getBoundingClientRect().height)+22;
if(need>0&&document.body)document.body.style.setProperty('--jf-ltv-pad',need+'px');
}
/* jf-sp-noloop: this observer MUST NOT watch class attributes. Our .jf-sp-tab
   buttons carry .emby-tab-button, so Jellyfin's own tab manager also toggles
   emby-tab-button-active on them. Watching class changes meant: we set active
   -> Jellyfin unsets it -> mutation -> we set it again ... a synchronous
   ping-pong that froze the renderer entirely (page stopped responding to even
   1+1). Watch childList only and let the 700ms interval correct the highlight. */
try{new MutationObserver(apply).observe(document.body,{childList:true,subtree:true});}catch(e){}
/* sf-ltv-subearly: the sub-bar arrived AFTER the page had already painted, and
   dropped the content 66px when it landed -- the "Live TV sub-tabs don't load in
   clean" jump. The bar itself is position:fixed and cannot push anything; what
   moves the content is `body.jf-ltv-nav`, which is what turns on the
   padding-top:66px on #suggestionsTab / #guideTab / #channelsTab.

   That class was only ever set by apply(), and apply() ran on a childList
   observer, a 700ms poll, or `hashchange` behind a setTimeout(0). Jellyfin
   navigates with history.pushState, which fires NEITHER hashchange nor popstate
   -- so on a pill click the class waited for the observer or the poll, measured
   at 200-400ms, by which time the panes had already been laid out without the
   padding. My Stuff never shows this because its content renders after its bar,
   so there is nothing on screen to shove.

   Wrapping pushState/replaceState is the same fix used elsewhere in this file for
   exactly this reason. Running apply() synchronously in the same task as the
   navigation puts the class on before the new panes are laid out, so they are
   padded on their FIRST paint and nothing jumps. */
(function(){
try{
var H=window.history;
['pushState','replaceState'].forEach(function(m){
var orig=H[m];
if(typeof orig!=='function')return;
H[m]=function(){
var r=orig.apply(this,arguments);
try{apply();}catch(e){}
return r;
};
});
}catch(e){}
})();
window.addEventListener('hashchange',apply);
window.addEventListener('resize',apply);
setInterval(apply,700);apply();
})();</script>"""
