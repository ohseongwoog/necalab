/* Only the current, on-screen research card animates. It never auto-advances. */
(() => {
'use strict';
const reduce=matchMedia('(prefers-reduced-motion: reduce)');
const galleries=[...document.querySelectorAll('[data-visual-deck]')];
for(const box of galleries){
 const q=s=>box.querySelector(s),portrait=box.classList.contains('vd-portrait');
 const track=q('[data-deck-track]'),controls=q('.vd-controls'),idx=q('[data-deck-index]');
 const motion=q('[data-vd-motion]'),cards=[...box.querySelectorAll('[data-deck-card]')];
 const actions=cards.map(card=>card.querySelector('[data-vd-open]'));
 const panels=[...box.querySelectorAll('[data-vd-panel]')];
 if(!cards.length)continue;
 let current=0,visible=false,opened=-1,firstHash=true,paused=false,effect=-1,effectTimer=0;
 let mouse=null,native=null,blockPointerClick=false;
 controls.hidden=false;
 const max=()=>Math.max(0,track.scrollWidth-track.clientWidth);
 const pos=card=>card.getBoundingClientRect().left-track.getBoundingClientRect().left+track.scrollLeft;
 function draw(){
  const enabled=visible&&!document.hidden&&!reduce.matches&&!paused;
  motion.disabled=reduce.matches;
  motion.textContent=reduce.matches?'Motion off':paused?'Resume motion':'Pause motion';
  motion.setAttribute('aria-pressed',String(paused));
  for(let i=0;i<cards.length;i++){
   cards[i].dataset.vdCurrent=String(i===current);
   cards[i].dataset.vdLoop=String(enabled&&i===current&&opened!==i);
   cards[i].dataset.vdPlay=String(enabled&&i===current&&effect===i);
   actions[i].tabIndex=i===current?0:-1;
  }
  const n=(current+1)+' / '+cards.length;if(idx.textContent!==n)idx.textContent=n;
  box.dataset.deckFirst=String(current+1);box.dataset.deckCount='1';
 }
 function close(restore=false){
  if(opened<0)return;
  const i=opened;opened=-1;effect=-1;clearTimeout(effectTimer);panels[i].hidden=true;cards[i].dataset.vdReveal='false';actions[i].setAttribute('aria-expanded','false');
  const title=actions[i].querySelector('.vd-heading').textContent;actions[i].setAttribute('aria-label',title+': show explanation');
  draw();
  if(restore){actions[i].focus({preventScroll:true});actions[i].scrollIntoView({block:'nearest',inline:'nearest',behavior:'instant'})}
 }
 function set(i){
  if(i!==current&&opened>=0&&opened!==i)close();
  current=i;draw();
 }
 function nearest(left=track.scrollLeft){
  const limit=max();if(limit>1&&left>=limit-2)return cards.length-1;
  let best=0,d=Infinity;
  cards.forEach((card,i)=>{const dx=Math.abs(left-pos(card));if(dx<d){d=dx;best=i}});
  return best;
 }
 function sync(){set(nearest())}
 function go(i,focus=false){
  i=Math.max(0,Math.min(cards.length-1,i));
  const left=i===cards.length-1?max():Math.max(0,pos(cards[i]));
  track.scrollTo({left,top:0,behavior:'instant'});set(i);
  if(focus)actions[i].focus({preventScroll:true});
 }
 function open(i,viaKeyboard=false){
  if(i===opened){close(true);return}
  close();opened=i;const a=actions[i],p=panels[i],title=a.querySelector('.vd-heading').textContent;
  a.setAttribute('aria-expanded','true');a.setAttribute('aria-label',title+': hide explanation');
  cards[i].dataset.vdReveal='true';p.hidden=false;p.focus({preventScroll:true});
  clearTimeout(effectTimer);effect=reduce.matches||paused?-1:i;draw();
  if(effect>=0)effectTimer=setTimeout(()=>{effect=-1;draw()},2670);
  // Keep the portrait image in view during a touch/pointer-triggered reveal.
  // Keyboard focus and reduced-motion users can still go straight to its explanation.
  if((!portrait||viaKeyboard||reduce.matches||paused)&&p.getBoundingClientRect().bottom>window.innerHeight)p.scrollIntoView({block:'nearest',behavior:'instant'});
 }
 motion.addEventListener('click',()=>{paused=!paused;if(paused){clearTimeout(effectTimer);effect=-1}draw()});
 track.addEventListener('keydown',e=>{
  if(e.ctrlKey||e.metaKey||e.altKey||(!actions.includes(e.target)&&e.target!==track))return;
  if(e.target===track&&(e.key==='Enter'||e.key===' ')){e.preventDefault();if(!e.repeat)open(current,true);return}
  const i={ArrowRight:current+1,ArrowLeft:current-1,Home:0,End:cards.length-1}[e.key];
  if(i===undefined)return;e.preventDefault();go(i,actions.includes(e.target));
 });
 box.addEventListener('keydown',e=>{if(e.key==='Escape'&&opened>=0){e.preventDefault();close(true)}});
 track.addEventListener('scroll',sync,{passive:true});track.addEventListener('scrollend',sync);
 // Touchscreens and trackpads retain the browser's two-axis scrolling and CSS snap.
 // Track a primary mouse gesture on the window only after a clear horizontal pull.
 // A small diagonal X delta otherwise latches certain trackpads to the nested rail
 // even on an almost vertical gesture. Route only that mixed, Y-dominant case to
 // the page; pure vertical, horizontal, shift-scroll and pinch-zoom stay native.
 track.addEventListener('wheel',e=>{
  const ax=Math.abs(e.deltaX),ay=Math.abs(e.deltaY);
  if(!e.cancelable||e.ctrlKey||e.metaKey||e.shiftKey||e.altKey||!ax||ay<=ax*1.5)return;
  const unit=e.deltaMode===1?(parseFloat(getComputedStyle(track).lineHeight)||16):e.deltaMode===2?window.innerHeight:1;
  const before=window.scrollY,cap=Math.max(0,document.documentElement.scrollHeight-window.innerHeight);
  if(e.deltaY<0?before<=0:before>=cap-1)return;
  e.preventDefault();window.scrollBy({top:e.deltaY*unit,left:0,behavior:'instant'});
 },{passive:false});
 track.addEventListener('pointerdown',e=>{
  if(!e.isPrimary||e.button!==0||!e.target.closest('[data-vd-open]'))return;
  blockPointerClick=false;
  const start={id:e.pointerId,x:e.clientX,y:e.clientY,left:track.scrollLeft};
  if(e.pointerType==='mouse'){
   if(e.ctrlKey||e.altKey||e.metaKey||e.shiftKey)return;
   native=null;mouse={...start,first:nearest(),drag:false,moved:false,vertical:false};
  }else{
   native={...start,moved:false};
  }
 },{passive:true});
 track.addEventListener('pointermove',e=>{
  if(native&&native.id===e.pointerId&&Math.hypot(e.clientX-native.x,e.clientY-native.y)>8)native.moved=true;
 },{passive:true});
 track.addEventListener('pointercancel',e=>{
  if(native&&native.id===e.pointerId){native.moved=true;blockPointerClick=true}
 },{passive:true});
 function finishMouse(toX,canceled=false){
  if(!mouse)return;
  const m=mouse;mouse=null;
  if(!m.drag){if(m.moved||m.vertical)blockPointerClick=true;return}
  if(!canceled&&Number.isFinite(toX))track.scrollLeft=m.left-(toX-m.x);
  const delta=track.scrollLeft-m.left;let dest=nearest();
  // A short, deliberate pull also turns a wide card; a long drag can cross several.
  const turn=Math.max(27,Math.min(65,cards[m.first].getBoundingClientRect().width*.13));
  if(!canceled&&dest===m.first&&Math.abs(delta)>=turn)dest=m.first+Math.sign(delta);
  blockPointerClick=true;delete track.dataset.vdDragging;
  go(dest);
 }
 window.addEventListener('pointermove',e=>{
  const m=mouse;if(!m||e.pointerId!==m.id||m.vertical)return;
  if(!(e.buttons&1)){finishMouse(e.clientX,true);return}
  const dx=e.clientX-m.x,dy=e.clientY-m.y,ax=Math.abs(dx),ay=Math.abs(dy);
  if(!m.drag){
   if(Math.hypot(dx,dy)>8)m.moved=true;
   if(ay>=9&&ay>ax*1.2){m.vertical=true;return}
   if(ax<8||ax<=ay*1.15)return;
   m.drag=true;track.dataset.vdDragging='true';
  }
  e.preventDefault();track.scrollLeft=m.left-dx;
 },{passive:false});
 window.addEventListener('pointerup',e=>{if(mouse?.id===e.pointerId)finishMouse(e.clientX)},{capture:true,passive:true});
 window.addEventListener('pointercancel',e=>{if(mouse?.id===e.pointerId)finishMouse(null,true)},{capture:true,passive:true});
 window.addEventListener('blur',()=>{if(mouse)finishMouse(null,true)});
 track.addEventListener('dragstart',e=>{if(e.target.closest('[data-vd-open]'))e.preventDefault()});
 // A pointer-up from a drag must not open a field. A fresh press or a keyboard
 // activation is independent, including a quick real click immediately afterward.
 track.addEventListener('click',e=>{
  const moved=blockPointerClick||(native&&(native.moved||Math.abs(native.left-track.scrollLeft)>7));
  native=null;blockPointerClick=false;
  if(e.detail>0&&moved){e.preventDefault();e.stopImmediatePropagation()}
 },true);
 actions.forEach((btn,i)=>btn.addEventListener('click',e=>{
  if(i!==current)go(i);open(i,e.detail===0);
 }));
 panels.forEach(panel=>panel.querySelector('[data-vd-close]').addEventListener('click',()=>close(true)));
 function revealHash(){
  let hash;try{hash=decodeURIComponent(location.hash.slice(1))}catch{return}
  const i=cards.findIndex(card=>card.id===hash);if(i<0)return false;
  go(i);firstHash=false;return true;
 }
 window.addEventListener('hashchange',revealHash);
 window.addEventListener('pageshow',()=>{if(firstHash)revealHash()});
 document.addEventListener('visibilitychange',draw);
 reduce.addEventListener?.('change',draw);
 if('IntersectionObserver'in window){
  const io=new IntersectionObserver(es=>{visible=es[0].isIntersecting&&es[0].intersectionRatio>=.12;draw()},{threshold:[0,.12]});
  io.observe(track);
 }else{
  const check=()=>{const r=track.getBoundingClientRect();visible=r.bottom>0&&r.top<innerHeight;draw()};
  window.addEventListener('scroll',check,{passive:true});window.addEventListener('resize',check,{passive:true});check();
 }
 if('ResizeObserver'in window)new ResizeObserver(()=>{if(!firstHash||!revealHash())sync()}).observe(track);
 else window.addEventListener('resize',sync);
 draw();if(location.hash)revealHash();
}
})();
