(() => {
 'use strict';
 const doc=document,reduce=matchMedia('(prefers-reduced-motion: reduce)');
 const timers=new WeakMap(),arts=new Set(),en=()=>doc.documentElement.lang==='en';
 function label(b){
  const name=b.getAttribute(en()?'data-name-en':'data-name-ko'),again=b.dataset.artState!=='idle';
  const action=reduce.matches?(en()?'Show final state':'최종 상태 보기'):(en()?(again?'Replay explanation':'Play explanation'):(again?'원리 다시 재생':'원리 재생'));
  b.setAttribute('aria-label',name+': '+action);
 }
 function finish(b){
  b.dataset.artState=reduce.matches?'reduced':'complete';const figure=b.closest('figure');
  figure.querySelector('[data-art-original]').hidden=true;figure.querySelector('[data-art-outcome]').hidden=false;label(b);
 }
 function initArt(b){arts.add(b);label(b);b.addEventListener('click',()=>{
  clearTimeout(timers.get(b));
  if(reduce.matches){finish(b);return}
  b.dataset.artState='idle';void b.offsetWidth;b.dataset.artState='playing';
  const f=b.closest('figure');f.querySelector('[data-art-original]').hidden=false;f.querySelector('[data-art-outcome]').hidden=true;
  label(b);timers.set(b,setTimeout(()=>finish(b),3100));
 })}
 doc.querySelectorAll('[data-art-play]').forEach(initArt);
 let dlg=null,title=null,closer=null,large=null,opener=null,active=null;
 function modalLanguage(){if(!dlg||!active)return;title.textContent=active.getAttribute(en()?'data-name-en':'data-name-ko');closer.textContent=en()?'Close':'닫기'}
 function openLarge(trigger){
  const source=trigger.closest('.field-figure'),button=source.querySelector('[data-art-play]');opener=trigger;active=button;
  if(!dlg){
   dlg=doc.createElement('dialog');dlg.className='field-view';dlg.setAttribute('aria-labelledby','field-view-heading');dlg.setAttribute('data-field-dialog','');
   const header=doc.createElement('div');header.className='field-view-head';title=doc.createElement('h2');title.id='field-view-heading';closer=doc.createElement('button');closer.type='button';closer.dataset.fieldClose='';header.append(title,closer);dlg.append(header);doc.body.append(dlg);
   closer.addEventListener('click',()=>dlg.close());dlg.addEventListener('close',()=>{if(large){const b=large.querySelector('[data-art-play]');clearTimeout(timers.get(b));arts.delete(b);large.remove();large=null}if(opener)opener.focus({preventScroll:true});active=null});
  }
  large=source.cloneNode(true);large.querySelector('[data-art-expand]').remove();
  const b=large.querySelector('[data-art-play]'),cap=large.querySelector('figcaption');b.dataset.artState='idle';cap.id='field-view-caption';b.setAttribute('aria-describedby',cap.id);
  large.querySelector('[data-art-original]').hidden=false;large.querySelector('[data-art-outcome]').hidden=true;
  dlg.append(large);initArt(b);modalLanguage();dlg.showModal();closer.focus({preventScroll:true});
 }
 doc.querySelectorAll('[data-art-expand]').forEach(b=>{b.addEventListener('click',()=>openLarge(b))});
 const sync=()=>{modalLanguage();for(const b of arts){if(reduce.matches&&b.dataset.artState==='playing'){clearTimeout(timers.get(b));finish(b)}label(b)}};
 doc.addEventListener('neca:lang',sync);if(reduce.addEventListener)reduce.addEventListener('change',sync);
 const aliases={'#puzzle-ai':'lab-ai','#puzzle-rf':'lab-rf','#lab-ai':'lab-ai','#lab-rf':'lab-rf'};
 function openLab(){const id=aliases[location.hash],item=id&&doc.getElementById(id);if(!item||item.tagName!=='DETAILS')return;
  item.open=true;if(location.hash!=='#'+id){try{const u=new URL(location.href);u.hash=id;history.replaceState(history.state,'',u)}catch{}item.scrollIntoView({behavior:'instant',block:'start'})}
 }
 openLab();window.addEventListener('hashchange',openLab);
 doc.addEventListener('click',e=>{const a=e.target.closest('a[href^="#lab-"]');if(!a)return;const d=doc.getElementById(aliases[a.hash]);if(d&&d.tagName==='DETAILS')d.open=true});
})();
