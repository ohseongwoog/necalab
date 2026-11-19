(() => {
'use strict';
const doc=document, root=doc.documentElement;root.classList.add('js');const $=s=>doc.querySelector(s),all=s=>Array.from(doc.querySelectorAll(s));
const language=$('#language'),hamb=$('#menu-trigger'),nav=$('#navigation'),getLang=()=>root.lang==='en'?'en':'ko';
let pref='ko';try{const saved=localStorage.getItem('neca-preview-lang');if(saved==='en')pref='en'}catch{}root.lang=pref;
function syncLabels(){const lang=getLang();for(const art of all('img[data-alt-ko]'))art.alt=art.getAttribute('data-alt-'+lang);language.setAttribute('aria-label',lang==='ko'?'Switch to English':'한국어로 전환');hamb.setAttribute('aria-label',lang==='ko'?'메뉴':'Menu');if($('#pub-list'))filter(false);doc.dispatchEvent(new CustomEvent('neca:lang',{detail:{lang}}))}
language.hidden=false;hamb.hidden=false;language.addEventListener('click',()=>{root.lang=getLang()==='ko'?'en':'ko';try{localStorage.setItem('neca-preview-lang',root.lang)}catch{}syncLabels()});
function menu(open){nav.classList.toggle('open',open);hamb.setAttribute('aria-expanded',String(open))}hamb.addEventListener('click',()=>menu(hamb.getAttribute('aria-expanded')!=='true'));doc.addEventListener('keydown',e=>{if(e.key==='Escape'&&nav.classList.contains('open')){menu(false);hamb.focus()}});
const q=$('#keywords'),y=$('#year'),list=$('#pub-list'),initial=new URLSearchParams(location.search);
let kind=['journal','conference'].includes(initial.get('type'))?initial.get('type'):'all';const norm=s=>(s||'').normalize('NFKC').toLowerCase().replace(/[\p{Pd}\s]+/gu,' ').trim();
function filter(save=true){if(!list)return;const query=norm(q.value),year=y.value,words=query.split(' ').filter(Boolean),items=all('#pub-list .paper');let n=0;
 for(const it of items){const target=norm(it.textContent),ok=(kind==='all'||it.dataset.kind===kind)&&(!year||it.dataset.year===year)&&words.every(w=>target.includes(w));it.hidden=!ok;if(ok)n++}
 for(const g of all('.yeargroup'))g.hidden=!Array.from(g.querySelectorAll('.paper')).some(a=>!a.hidden);
 for(const b of all('[data-type]'))b.setAttribute('aria-pressed',String(b.dataset.type===kind));$('#empty').hidden=n!==0;$('#result-count').textContent=getLang()==='ko'?n+'건 / 전체 '+items.length+'건':n+' of '+items.length+' publications';
 if(save){const u=new URL(location.href);for(const [k,v] of Object.entries({type:kind==='all'?'':kind,q:q.value.trim(),year})){if(v)u.searchParams.set(k,v);else u.searchParams.delete(k)}u.hash='';try{history.replaceState(null,'',u)}catch{}}}
if(list){for(const el of all('[data-js-only]'))el.hidden=false;q.value=initial.get('q')||'';if(Array.from(y.options).some(o=>o.value===initial.get('year')))y.value=initial.get('year');for(const b of all('[data-type]'))b.addEventListener('click',()=>{kind=b.dataset.type;filter()});q.addEventListener('input',()=>filter());y.addEventListener('change',()=>filter());$('#reset-filters').addEventListener('click',()=>{kind='all';q.value='';y.value='';filter();q.focus()})}
syncLabels();
})();
