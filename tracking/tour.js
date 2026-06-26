// Compliance Cove, self-contained guided tour engine.
// Usage: define window.COVE_TOUR_STEPS=[{target,title,text,placement}] BEFORE this script.
// Optional: an element with id 'coveTourTrigger' becomes the launch button; otherwise a floating pill is added.
(function(){
  if(!window.COVE_TOUR_STEPS||!window.COVE_TOUR_STEPS.length)return;
  var STEPS=window.COVE_TOUR_STEPS,idx=-1,spot,tip;
  var css='#cctSpot{position:absolute;border-radius:10px;box-shadow:0 0 0 9999px rgba(15,23,42,.55);z-index:99998;pointer-events:none;transition:all .25s;}'
  +'#cctTip{position:absolute;z-index:99999;max-width:330px;background:#fff;color:#0f172a;border:1px solid #e2e8f0;border-radius:14px;padding:16px 18px;box-shadow:0 18px 50px rgba(0,0,0,.22);font-family:Inter,system-ui,sans-serif;}'
  +'#cctTip .cct-num{font-size:11px;font-weight:700;color:#4f46e5;letter-spacing:.5px;text-transform:uppercase;}'
  +'#cctTip h4{font-size:15px;font-weight:800;margin:6px 0;}'
  +'#cctTip p{font-size:13px;line-height:1.55;color:#475569;margin:0;}'
  +'.cct-actions{display:flex;align-items:center;justify-content:space-between;margin-top:16px;gap:8px;}'
  +'.cct-dots{display:flex;gap:5px;}.cct-dot{width:7px;height:7px;border-radius:50%;background:#cbd5e1;transition:all .2s;}.cct-dot.on{background:#4f46e5;transform:scale(1.25);}'
  +'.cct-btns{display:flex;gap:6px;align-items:center;}'
  +'.cct-btn{font-size:12px;font-weight:600;padding:6px 12px;border-radius:8px;cursor:pointer;border:1px solid #e2e8f0;background:#fff;color:#0f172a;}.cct-btn:hover{border-color:#4f46e5;}'
  +'.cct-btn.pri{background:#4f46e5;color:#fff;border-color:#4f46e5;}'
  +'.cct-skip{font-size:11px;color:#64748b;cursor:pointer;background:none;border:none;text-decoration:underline;}'
  +'#cctLaunch{position:fixed;right:18px;bottom:18px;z-index:9990;display:inline-flex;align-items:center;gap:7px;padding:10px 15px;border-radius:999px;border:none;cursor:pointer;background:#4f46e5;color:#fff;font:600 13px Inter,system-ui,sans-serif;box-shadow:0 8px 24px rgba(79,70,229,.35);}';
  var st=document.createElement('style');st.textContent=css;document.head.appendChild(st);
  function build(){if(spot)return;spot=document.createElement('div');spot.id='cctSpot';spot.style.display='none';tip=document.createElement('div');tip.id='cctTip';tip.style.display='none';document.body.appendChild(spot);document.body.appendChild(tip);}
  function tgt(s){return s.target?document.querySelector(s.target):null;}
  function start(){build();idx=0;render();window.addEventListener('resize',pos);window.addEventListener('scroll',pos,true);if(typeof coveTrack==='function')coveTrack('tour_started',{});}
  function end(){if(idx>=0&&typeof coveTrack==='function')coveTrack('tour_ended',{screen:'step '+(idx+1)});idx=-1;if(spot){spot.style.display='none';tip.style.display='none';}window.removeEventListener('resize',pos);window.removeEventListener('scroll',pos,true);}
  function next(){if(idx<STEPS.length-1){idx++;render();}else end();}
  function prev(){if(idx>0){idx--;render();}}
  window.coveStartTour=start;window.coveTourNext=next;window.coveTourPrev=prev;window.coveTourEnd=end;
  function render(){build();var s=STEPS[idx],last=idx===STEPS.length-1;
    var dots=STEPS.map(function(_,i){return '<span class="cct-dot '+(i===idx?'on':'')+'"></span>';}).join('');
    tip.innerHTML='<div class="cct-num">Step '+(idx+1)+' of '+STEPS.length+'</div><h4>'+s.title+'</h4><p>'+s.text+'</p>'
      +'<div class="cct-actions"><div class="cct-dots">'+dots+'</div><div class="cct-btns">'
      +'<button class="cct-skip" onclick="coveTourEnd()">Skip</button>'
      +(idx>0?'<button class="cct-btn" onclick="coveTourPrev()">Back</button>':'')
      +'<button class="cct-btn pri" onclick="coveTourNext()">'+(last?'Finish':'Next')+'</button></div></div>';
    tip.style.display='';var el=tgt(s);if(el)el.scrollIntoView({behavior:'smooth',block:'center'});setTimeout(pos,el?320:0);}
  function pos(){if(idx<0)return;var s=STEPS[idx],el=tgt(s),pad=8,gap=14;
    if(!el){spot.style.display='none';tip.style.position='fixed';tip.style.top='50%';tip.style.left='50%';tip.style.transform='translate(-50%,-50%)';return;}
    tip.style.transform='';tip.style.position='absolute';var r=el.getBoundingClientRect();var top=r.top+window.scrollY,left=r.left+window.scrollX;
    spot.style.display='';spot.style.top=(top-pad)+'px';spot.style.left=(left-pad)+'px';spot.style.width=(r.width+pad*2)+'px';spot.style.height=(r.height+pad*2)+'px';
    var tw=tip.offsetWidth,th=tip.offsetHeight,place=s.placement||'bottom',tt,tl;
    if(place==='right'&&r.right+gap+tw<window.innerWidth){tt=top+r.height/2-th/2;tl=left+r.width+gap;}
    else if(place==='top'&&r.top-gap-th>0){tt=top-th-gap;tl=left+r.width/2-tw/2;}
    else if(place==='left'&&r.left-gap-tw>0){tt=top+r.height/2-th/2;tl=left-tw-gap;}
    else{tt=top+r.height+gap;tl=left+r.width/2-tw/2;}
    tl=Math.max(window.scrollX+12,Math.min(tl,window.scrollX+window.innerWidth-tw-12));tt=Math.max(window.scrollY+12,tt);
    tip.style.top=tt+'px';tip.style.left=tl+'px';}
  document.addEventListener('keydown',function(e){if(idx<0)return;if(e.key==='ArrowRight'){e.preventDefault();next();}else if(e.key==='ArrowLeft'){e.preventDefault();prev();}else if(e.key==='Escape'){e.preventDefault();end();}});
  function wire(){var t=document.getElementById('coveTourTrigger');
    if(t){t.addEventListener('click',start);}
    else{var b=document.createElement('button');b.id='cctLaunch';b.type='button';b.innerHTML='<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="2.2" stroke-linecap="round"><circle cx="12" cy="12" r="10"/><path d="M9.1 9a3 3 0 0 1 5.8 1c0 1.5-1.5 2-2.3 2.6-.5.4-.8.9-.8 1.4"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg> Guided tour';b.onclick=start;document.body.appendChild(b);}}
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',wire);else wire();
})();
