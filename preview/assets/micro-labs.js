/* Fixed teaching examples, calculated on input. No animation loop, external model or radio hardware. */
(() => {
 'use strict';
 const cards=Array.from(document.querySelectorAll('.micro-card[data-lab]'));
 const say=(ko,en)=>document.documentElement.lang==='en'?en:ko;
 const set=(el,s)=>{if(el.textContent!==s)el.textContent=s};
 const label=(el,s)=>el.setAttribute('aria-valuetext',s);
 function renderAI(card,slider){
  const sensor=Number(slider.value),t=1-sensor/100,s=1-t;
  // Each fixed observation favors a different class; blend its two normalized support scores.
  const wifi=.90*t+.09*s,heat=.10*t+.91*s,hot=heat>wifi;
  const name=hot?say('기기 과열','Overheating'):say('연결 문제','Wi-Fi fault');
  card.dataset.state=hot?'hardware':'connection';
  set(card.querySelector('[data-outcome]'),name);
  const textPercent=Math.round(t*100);
  const weights=say('문장 '+textPercent+'% · 센서 '+sensor+'%',textPercent+'% text · '+sensor+'% sensor');
  set(card.querySelector('[data-meter]'),weights);
  for(const [group,w] of [['text',t],['sensor',s]]){
   const paths=card.querySelector('[data-net="'+group+'"]');
   paths.setAttribute('opacity',(.24+.76*w).toFixed(2));paths.setAttribute('stroke-width',(.7+2.6*w).toFixed(2));
  }
  slider.style.setProperty('--pos',sensor+'%');label(slider,weights+', '+name);
 }
 function wave(end,distance){
  const span=end-68,segments=112;let out='M68 23';
  for(let i=1;i<=segments;i++){const t=i/segments,x=68+span*t,edge=Math.min(1,(x-68)/3,(end-x)/3);
   const y=23-(8.8*2/(2+(distance-2)*t))*Math.sin(2*Math.PI*(x-68)/23)*edge;
   out+='L'+x.toFixed(2)+' '+y.toFixed(2);
  }return out;
 }
 function renderRF(card,slider){
  const m=Number(slider.value),rx=-5-20*Math.log10(4*Math.PI*m*2.45e9/299792458),up=rx>=-63;
  const name=up?say('연결됨','Connected'):say('연결 끊김','Disconnected');
  card.dataset.state=up?'connected':'disconnected';
  const end=130+(m-2)*7.2;
  card.querySelector('[data-wave]').setAttribute('d',wave(end,m));
  card.querySelector('[data-receiver]').setAttribute('transform','translate('+end.toFixed(2)+',0)');
  card.querySelector('[data-rx-label]').setAttribute('x',(end+13).toFixed(2));
  set(card.querySelector('[data-outcome]'),name);
  const pow=rx.toFixed(1).replace('-','−')+' dBm',distance=m.toFixed(1)+' m';
  set(card.querySelector('[data-meter]'),distance+' · '+pow);
  slider.style.setProperty('--pos',((m-2)/12*100)+'%');label(slider,distance+', '+pow+', '+name);
 }
 for(const card of cards){
  const slider=card.querySelector('input[type=range]'),outcome=card.querySelector('[data-outcome]');
  outcome.setAttribute('role','status');outcome.setAttribute('aria-live','polite');outcome.setAttribute('aria-atomic','true');
  const render=()=> (card.dataset.lab==='ai'?renderAI:renderRF)(card,slider);
  slider.disabled=false;slider.addEventListener('input',render);document.addEventListener('neca:lang',render);render();
 }
})();
