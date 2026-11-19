/* Local teaching puzzles. Targets are sampled once per page load. */
(() => {
'use strict';
const AKEY=['text','sensor','log'], RKEY=['distance','angle','match'];
const AI_START=Object.freeze([12,12,12]), RF_START=Object.freeze([14,75,19]);
const clamp=(x,lo,hi)=>Math.max(lo,Math.min(hi,x));
const pick=(rng,lo,hi)=>lo+Math.floor(clamp(rng(),0,1-Number.EPSILON)*(hi-lo+1));
const one=x=>Math.round(x*10)/10;
const aiScores=values=>values.map((v,i)=>one(.76*v+.12*values[(i+1)%3]+.12*values[(i+2)%3]));
function aiChallenge(rng=Math.random){
 const solution=AKEY.map(()=>pick(rng,45,87));
 return {solution,bands:aiScores(solution).map(center=>({lo:one(center-2.5),hi:one(center+2.5)}))};
}
function receive([d,a,p]){
 const fspl=20*Math.log10(4*Math.PI*d*2.45e9/299792458);
 return -5-fspl+20*Math.log10(Math.cos(a*Math.PI/180))+10*Math.log10(p/100);
}
function rfChallenge(rng=Math.random){
 const center=pick(rng,-554,-525)/10;
 return {lo:one(center-.6),hi:one(center+.6)};
}
const includes=(value,{lo,hi})=>value>=lo&&value<=hi;
const aiSolved=(values,c)=>aiScores(values).every((v,i)=>includes(v,c.bands[i]));
const rfSolved=(values,c)=>includes(one(receive(values)),c);
if(typeof module==='object'&&module.exports)module.exports={aiScores,aiChallenge,aiSolved,receive,rfChallenge,rfSolved,AI_START,RF_START};
if(typeof document==='undefined')return;

const ui={
 target:['목표','Target'], goal:['성공! 세 점수가 모두 목표에 들어왔어요.','Solved! All three scores are in range.'],
 count:['목표에 맞춘 점수','Scores in range'], up:['올리기 ↑','Raise ↑'], down:['낮추기 ↓','Lower ↓'],
 hold:['이대로','Hold here'], aligned:['편파 맞추기 ↓','Align ↓'], misaligned:['덜 정렬 ↑','Tilt ↑'],
 closer:['가까이 ↓','Closer ↓'], farther:['멀리 ↑','Farther ↑'], tune:['정합 개선 ↑','Match better ↑'], detune:['정합 낮추기 ↓','Match less ↓'],
 weak:['너무 약함','Too weak'], strong:['너무 강함','Too strong'], linked:['성공! 수신 전력이 목표에 들어왔어요.','Solved! Receive power is on target.'],
}
const T=k=>ui[k][document.documentElement.lang==='en'?1:0];
const val=(n,precision=1)=>n.toFixed(precision).replace('-','−');
const bandText=(b,unit='')=>T('target')+' '+val(b.lo)+' – '+val(b.hi)+unit;
const set=(node,value)=>{if(node.textContent!==value)node.textContent=value};
function meter(card,key,v,b,min,max){
 const q=s=>card.querySelector(s), span=max-min, frac=n=>(clamp((n-min)/span,0,1)*100)+'%';
 const t=q('[data-target="'+key+'"]'),m=q('[data-marker="'+key+'"]');
 t.style.left=frac(b.lo);t.style.width=100*(b.hi-b.lo)/span+'%';
 m.style.left=frac(v);m.dataset.pass=String(includes(v,b));
}
function init(card){
 const ai=card.dataset.lab==='ai',keys=ai?AKEY:RKEY;
 const challenge=ai?aiChallenge():rfChallenge();
 const q=s=>card.querySelector(s);
 const outcome=q('[data-outcome]');
 const knobs=keys.map(k=>q('[data-knob="'+k+'"]'));
 card.dataset.challenge=JSON.stringify(ai?challenge.bands:challenge);
 const fmtKnob=(key,v)=>key==='distance'?val(v)+' m':key==='angle'?val(v,0)+'°':val(v,0)+'%';
 function knob(key,i,value,hint){
  const s=knobs[i],display=fmtKnob(key,value);
  s.style.setProperty('--fill',100*(value-Number(s.min))/(Number(s.max)-Number(s.min))+'%');
  s.setAttribute('aria-valuetext',display+', '+T(hint).replace(/[↑↓]/g,'').trim());
  set(q('[data-knob-value="'+key+'"]'),display);set(q('[data-knob-hint="'+key+'"]'),T(hint));
 }
 function updateAI(values){
  const s=aiScores(values), hit=s.filter((v,i)=>includes(v,challenge.bands[i])).length;
  card.dataset.state=hit===3?'goal':'progress';
  keys.forEach((key,i)=>{
   const b=challenge.bands[i],v=values[i];
   set(q('[data-score="'+key+'"]'),val(s[i]));
   set(q('[data-band="'+key+'"]'),bandText(b));
   meter(card,key,s[i],b,0,100);
   knob(key,i,v,hit===3||Math.abs(v-challenge.solution[i])<=1?'hold':v<challenge.solution[i]?'up':'down');
  });
  card.querySelectorAll('[data-channel]').forEach(p=>{
   const weight=values[Number(p.dataset.channel)]/100,main=p.dataset.main==='1';
   p.setAttribute('opacity',(.18+(main?.72:.33)*weight).toFixed(2));
   p.setAttribute('stroke-width',(.72+(main?2.55:1.16)*weight).toFixed(2));
  });
  set(outcome,hit===3?T('goal'):T('count')+' '+hit+' / 3');
 }
 function updateRF(values){
  const [d,a,p]=values, power=one(receive(values)),b=challenge,goal=includes(power,b),weak=power<b.lo;
  card.dataset.state=goal?'goal':weak?'weak':'strong';
  set(q('[data-score="power"]'),val(power)+' dBm');set(q('[data-band="power"]'),bandText(b,' dBm'));
  meter(card,'power',power,b,-90,-49);
  const hints=goal?['hold','hold','hold']:weak?
    [d>2?'closer':'hold',a>0?'aligned':'hold',p<100?'tune':'hold']:
    [d<14?'farther':'hold',a<75?'misaligned':'hold',p>19?'detune':'hold'];
  keys.forEach((key,i)=>knob(key,i,values[i],hints[i]));
  const end=118+(d-2)*21.2, line=q('[data-wave]'),amp=8.2*Math.sqrt(p/100);
  let path='M52 43';
  for(let i=1;i<=118;i++){
   const t=i/118,x=52+(end-52)*t,fade=Math.min(1,(x-52)/4,(end-x)/4);
   const y=43-amp*2/(2+(d-2)*t)*Math.sin(2*Math.PI*(x-52)/22)*fade;
   path+='L'+x.toFixed(2)+' '+y.toFixed(2);
  }
  line.setAttribute('d',path);
  q('[data-receiver]').setAttribute('transform','translate('+end.toFixed(2)+',0)');
  q('[data-rf-axis]').setAttribute('transform','rotate('+a+' 0 43)');
  q('[data-rf-light]').setAttribute('fill',goal?'#80efb4':weak?'#9cb7c9':'#ffc992');
  set(outcome,T(goal?'linked':weak?'weak':'strong'));
 }
 const refresh=()=>{const values=knobs.map(s=>Number(s.value));ai?updateAI(values):updateRF(values)};
 knobs.forEach(s=>{s.disabled=false;s.addEventListener('input',refresh)});
 document.addEventListener('neca:lang',refresh);
 refresh();
}
document.querySelectorAll('.micro-card[data-lab]').forEach(init);
const anchors=new Set(['#hands-on','#lab-ai','#lab-rf','#puzzle-ai','#puzzle-rf']);
function settlePuzzleAnchor(){
 if(!anchors.has(location.hash))return;
 document.getElementById(location.hash.slice(1))?.scrollIntoView({behavior:'instant',block:'start',inline:'nearest'});
}
if(document.readyState==='complete')settlePuzzleAnchor();
else window.addEventListener('load',settlePuzzleAnchor,{once:true});
window.addEventListener('hashchange',settlePuzzleAnchor);

})();
