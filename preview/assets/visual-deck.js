/* Only the current, on-screen research card animates. It never auto-advances. */
(() => {
'use strict';
const reduce=matchMedia('(prefers-reduced-motion: reduce)');
const galleries=[...document.querySelectorAll('[data-visual-deck]')];
for(const box of galleries){
 const q=s=>box.querySelector(s);
 const track=q('[data-deck-track]'),controls=q('.vd-controls'),idx=q('[data-deck-index]');
 const prev=q('[data-deck-prev]'),next=q('[data-deck-next]'),motion=q('[data-vd-motion]'),cards=[...box.querySelectorAll('[data-deck-card]')];
 const actions=cards.map(card=>card.querySelector('[data-vd-open]'));
 const panels=[...box.querySelectorAll('[data-vd-panel]')];
 if(!cards.length)continue;
 let current=0,visible=false,opened=-1,gesture=null,firstHash=true,paused=false,effect=-1,effectTimer=0;
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
  prev.setAttribute('aria-disabled',String(current===0));
  next.setAttribute('aria-disabled',String(current===cards.length-1));
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
 function sync(){
  const l=track.scrollLeft,limit=max();
  if(limit>1&&l>=limit-2){set(cards.length-1);return}
  let best=0,d=Infinity;
  cards.forEach((card,i)=>{const dx=Math.abs(l-pos(card));if(dx<d){d=dx;best=i}});
  set(best);
 }
 function go(i,focus=false){
  i=Math.max(0,Math.min(cards.length-1,i));
  const left=i===cards.length-1?max():Math.max(0,pos(cards[i]));
  track.scrollTo({left,top:0,behavior:'instant'});set(i);
  if(focus)actions[i].focus({preventScroll:true});
 }
 function open(i){
  if(i===opened){close(true);return}
  close();opened=i;const a=actions[i],p=panels[i],title=a.querySelector('.vd-heading').textContent;
  a.setAttribute('aria-expanded','true');a.setAttribute('aria-label',title+': hide explanation');
  cards[i].dataset.vdReveal='true';p.hidden=false;p.focus({preventScroll:true});
  clearTimeout(effectTimer);effect=reduce.matches||paused?-1:i;draw();
  if(effect>=0)effectTimer=setTimeout(()=>{effect=-1;draw()},2670);
  if(p.getBoundingClientRect().bottom>window.innerHeight)p.scrollIntoView({block:'nearest',behavior:'instant'});
 }
 motion.addEventListener('click',()=>{paused=!paused;if(paused){clearTimeout(effectTimer);effect=-1}draw()});
 prev.addEventListener('click',()=>{if(current>0)go(current-1)});
 next.addEventListener('click',()=>{if(current<cards.length-1)go(current+1)});
 track.addEventListener('keydown',e=>{
  if(e.ctrlKey||e.metaKey||e.altKey||(!actions.includes(e.target)&&e.target!==track))return;
  const i={ArrowRight:current+1,ArrowLeft:current-1,Home:0,End:cards.length-1}[e.key];
  if(i===undefined)return;e.preventDefault();go(i,actions.includes(e.target));
 });
 box.addEventListener('keydown',e=>{if(e.key==='Escape'&&opened>=0){e.preventDefault();close(true)}});
 track.addEventListener('scroll',sync,{passive:true});track.addEventListener('scrollend',sync);
 track.addEventListener('pointerdown',e=>{
  const b=e.target.closest('[data-vd-open]');if(!b)return;
  gesture={id:e.pointerId,x:e.clientX,y:e.clientY,left:track.scrollLeft,moved:false};
 },{passive:true});
 track.addEventListener('pointermove',e=>{
  if(gesture&&gesture.id===e.pointerId&&Math.hypot(e.clientX-gesture.x,e.clientY-gesture.y)>9)gesture.moved=true;
 },{passive:true});
 track.addEventListener('pointercancel',e=>{if(gesture&&gesture.id===e.pointerId)gesture.moved=true},{passive:true});
 actions.forEach((btn,i)=>btn.addEventListener('click',e=>{
  const swipe=e.detail>0&&gesture&&(gesture.moved||Math.abs(gesture.left-track.scrollLeft)>7);
  gesture=null;if(swipe)return;
  if(i!==current)go(i);open(i);
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
