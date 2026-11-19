(() => {
  'use strict';
  const lang = () => document.documentElement.lang === 'en' ? 'en' : 'ko';
  const init = box => {
    const track=box.querySelector('[data-deck-track]'),cards=Array.from(track.querySelectorAll('[data-deck-card]'));
    const controls=box.querySelector('.deck-tools'),prev=box.querySelector('[data-deck-prev]'),next=box.querySelector('[data-deck-next]'),index=box.querySelector('[data-deck-index]');
    if (!cards.length) return;
    controls.hidden=false;
    const pos=card=>card.getBoundingClientRect().left-track.getBoundingClientRect().left+track.scrollLeft;
    const metrics=()=>{
      const gap=parseFloat(getComputedStyle(track).columnGap)||0,unit=cards[0].getBoundingClientRect().width+gap;
      const visible=Math.max(1,Math.min(cards.length,Math.floor((track.clientWidth+gap+2)/unit)));
      return {visible,last:cards.length-visible,max:Math.max(0,track.scrollWidth-track.clientWidth)};
    };
    const current=({last,max})=>{
      if(!max||last<1)return 0;
      if(track.scrollLeft>=max-2)return last;
      let best=0,dist=Infinity;
      for(let i=0;i<=last;i++){const d=Math.abs(pos(cards[i])-track.scrollLeft);if(d<dist){best=i;dist=d}}
      return best;
    };
    const sync=()=>{
      const m=metrics(),start=current(m),end=Math.min(cards.length,start+m.visible);
      const nums=m.visible>1?(start+1)+'–'+end:String(start+1),en=lang()==='en';
      const note=en?'Research cards '+nums+' of '+cards.length:'연구 카드 '+nums+' / '+cards.length;
      box.setAttribute('aria-label',en?'Research fields':'연구 분야');box.setAttribute('aria-roledescription',en?'carousel':'카드 모음');
      track.setAttribute('aria-label',en?'Research cards; use left and right arrow keys to navigate':'연구 카드: 좌우 방향키로 탐색');
      const str=nums+' / '+cards.length;
      if(index.textContent!==str)index.textContent=str;
      index.setAttribute('aria-label',note);box.dataset.deckFirst=String(start+1);box.dataset.deckCount=String(m.visible);
      prev.setAttribute('aria-disabled',String(start===0));next.setAttribute('aria-disabled',String(start>=m.last));
      return {m,start};
    };
    function go(i){
      const m=metrics();i=Math.max(0,Math.min(m.last,i));
      // Programmatic navigation is immediate: keyboard users never wait for an animation.
      // Finger-based scrolling retains the browser's native inertia and snap behaviour.
      const left=i===m.last?m.max:Math.max(0,pos(cards[i]));
      track.scrollTo({left,top:0,behavior:'instant'});sync();
    }
    function step(delta){const {start}=sync();go(start+delta)}
    prev.addEventListener('click',()=>{if(prev.getAttribute('aria-disabled')!=='true')step(-1)});
    next.addEventListener('click',()=>{if(next.getAttribute('aria-disabled')!=='true')step(1)});
    track.addEventListener('keydown',e=>{
      if(e.target!==track||e.ctrlKey||e.altKey||e.metaKey)return;
      const {m,start}=sync();const value={ArrowLeft:start-1,ArrowRight:start+1,Home:0,End:m.last}[e.key];
      if(value===undefined)return;e.preventDefault();go(value);
    });
    track.addEventListener('scroll',sync,{passive:true});
    track.addEventListener('scrollend',sync);
    function revealHash(){
      if(!location.hash)return;let name;try{name=decodeURIComponent(location.hash.slice(1))}catch{return}
      const i=cards.findIndex(c=>c.id===name);if(i<0)return;
      go(i);
    }
    window.addEventListener('hashchange',revealHash);
    document.addEventListener('click',e=>{const a=e.target.closest('a[href^="#"]');if(a&&a.hash===location.hash&&a.hash)requestAnimationFrame(revealHash)});
    if('ResizeObserver'in window){new ResizeObserver(()=>{sync();if(location.hash&&!track.dataset.touched)revealHash()}).observe(track)}
    else window.addEventListener('resize',sync);
    for(const ev of ['keydown','pointerdown','wheel'])box.addEventListener(ev,()=>{track.dataset.touched='true'},{passive:true});
    document.addEventListener('neca:lang',sync);
    sync();if(location.hash){requestAnimationFrame(revealHash);window.addEventListener('load',revealHash,{once:true})}
  };
  document.querySelectorAll('[data-deck]').forEach(init);
})();
