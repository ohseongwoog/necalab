/* NECA virtual RF bench: deterministic, single-frequency teaching model. */
(() => {
'use strict';
const root=document.querySelector('[data-lab="rf"]');
if(!root)return;
const labels={
 title:['RF 송수신 실험대','RF link bench'], intro:['회로를 바꾸거나 수신기를 움직여서 같은 신호가 어디까지 닿는지 실험해 보세요.','Rewire the circuit or move the receiver to see how far the same signal can travel.'],
 board:['송신 보드','Transmitter board'], boardhelp:['부품을 누른 뒤 슬롯을 누르면 옮기거나 서로 바꿉니다. 보드 위의 부품도 선택할 수 있습니다.','Select a part, then select a slot to place or swap it. You can also select parts already on the board.'],
 parts:['사용 가능한 부품','Available components'],slots:['왼쪽에서 오른쪽으로 연결된 네 슬롯','Four wired slots from left to right'],
 empty:['비어 있음','Empty'],source:['신호원','Source'],pa:['전력 증폭기','Power amp'],match:['직렬 정합','Series tuner'],antenna:['송신 안테나','TX antenna'],jumper:['연결선','Jumper'],
 remove:['선택 부품 빼기','Remove selected part'],clear:['보드 비우기','Clear board'],reset:['전체 초기화','Reset bench'],transmit:['신호 송신','Transmit'],
 gain:['증폭기 이득','Amplifier gain'],load:['안테나 임피던스','Antenna impedance'],reactance:['직렬 정합 소자','Series tuning element'],bypass:['우회선 · 0 Ω','Bypass · 0 Ω'],inductor:['인덕터','Inductor'],
 tuned:['공진','Resonant'], detuned:['이조','Detuned'], reactive:['저저항·이조','Low R, detuned'],
 map:['수신기 배치','Receiver placement'], maphelp:['지도에서 수신기를 끌거나 원하는 위치를 누르세요. 안테나의 손잡이 또는 회전 버튼으로 편파를 바꿀 수 있습니다.','Drag the receiver or tap a spot on the map. Rotate its polarization using the handle or the rotation buttons.'],
 keyhelp:['지도에서 방향키로 이동하고 [ 또는 ] 키로 돌립니다. 지도 바깥의 버튼으로도 조작할 수 있습니다.','On the map, use arrow keys to move and [ or ] to rotate. The buttons below do the same.'],
 left:['왼쪽으로','Left'],right:['오른쪽으로','Right'],up:['위로','Up'],down:['아래로','Down'], turnleft:['−15° 회전','Rotate −15°'],turnright:['+15° 회전','Rotate +15°'],
 rx:['수신기','Receiver'],tx:['송신기','Transmitter'],distance:['거리','Distance'],angle:['편파 차이','Polarization offset'],mismatch:['부정합 손실','Mismatch loss'],free:['자유공간 경로 손실','Free-space loss'],polar:['편파 손실','Polarization loss'],estimate:['예상 수신 전력','Estimated receive power'],threshold:['수신 기준','Receiver threshold'],
 ready:['배치에 따라 계산값이 바뀝니다. 신호 송신으로 이 배치의 결과를 확인하세요.','The estimate updates as you edit. Transmit to test this setup.'],
 invalid:['송신 경로가 열려 있거나 순서가 맞지 않습니다. 왼쪽 끝에 신호원, 오른쪽 끝에 안테나를 연결하세요. 가운데 슬롯은 증폭기 또는 연결선, 정합 소자 또는 연결선입니다.','The path is open or connected in the wrong order. Put the source first and the antenna last. The middle slots take an amplifier or jumper, then a tuner or jumper.'],
 connected:['수신 성공 · 수신 전력이 기준 이상입니다.','Link received · power meets the threshold.'],
 weak:['수신 실패 · 신호 전력이 수신 기준보다 낮습니다.','Signal too weak · receive power is below the threshold.'],
 null:['수신 실패 · 이상적인 선형 편파가 직교하여 수신 전력이 0입니다.','No signal · ideal perpendicular linear polarizations couple zero power.'],
 inactive:['경로 없음','No active path'],picked:['선택','Selected'],existing:['보드에 있음','On board'],drop:['부품을 먼저 선택하세요.','Choose a component first.'],
 assumptions:['계산 모델과 가정','Model and assumptions'],
 modelA:['2.45 GHz 단일 주파수에서 자유공간 원거리장 Friis 식을 사용합니다. 장애물, 반사, 잡음, 증폭기 포화는 모델링하지 않습니다. 작은 이상 안테나를 가정하고 최소 거리는 2 m입니다.','This uses the free-space far-field Friis equation at one frequency, 2.45 GHz. It omits obstructions, reflections, noise and amplifier saturation. The ideal antennas are assumed small; minimum distance is 2 m.'],
 modelB:['신호원은 −15 dBm, 두 안테나의 이득은 각각 2 dBi, 수신 기준은 −59 dBm입니다. 안테나에 직렬 소자를 더한 임피던스를 50 Ω 기준으로 보고, 반사되지 않은 전력 비율 1 − |Γ|²을 적용합니다.','Source power is −15 dBm, each antenna gain is 2 dBi, and the receiver threshold is −59 dBm. Series tuning adds to the antenna impedance; against a 50 Ω reference the delivered power fraction is 1 − |Γ|².'],
 modelC:['송·수신 선형 편파의 차이에 cos²(θ)를 적용합니다. 지도 안테나 표시는 전파 경로를 따라 본 편파 방향이며 빔의 방향이 아닙니다. 정확히 90°이면 이 이상 모델에서 수신 전력은 0(−∞ dBm)입니다. 실제 전파를 송신하지 않습니다.','Linear polarization contributes cos²(θ). The antenna symbols show polarization viewed along the radio path, not beam pointing. At exactly 90° the ideal receive power is zero (−∞ dBm). No real radio signal is transmitted.'],
};
const language=()=>document.documentElement.lang==='en'?1:0;
const T=k=>labels[k][language()];
const parts=['source','pa','match','antenna','jumper'], tx={x:3,y:8}, z0=50, f=2.45e9, wavelength=299792458/f, sensitivity=-59;
const loads={tuned:[50,0],detuned:[50,-75],reactive:[20,-85]};
const start=()=>({slots:['source','pa','match','antenna'],gain:18,load:'detuned',reactance:0,x:12,y:8,a:0,selected:null,transmitted:false});
let state=start(), dragging=null, animation=null, pulseTimer=0;
const Q=s=>root.querySelector(s),A=s=>Array.from(root.querySelectorAll(s));
const attr=(key,val)=>`data-rf-${key}="${val}"`;
const btn=(key,val,label,cls='')=>`<button type="button" class="${cls}" ${attr(key,val)}>${T(label)}</button>`;
const symbol={source:'<circle cx="16" cy="16" r="10"/><path d="M7 16h3q3-7 6 0t6 0h3"/>',pa:'<path d="M6 6l20 10L6 26Z"/><path d="M1 16h5m20 0h5"/>',match:'<path d="M1 17h3q3-11 6 0 3-11 6 0 3-11 6 0 3-11 6 0h3"/>',antenna:'<path d="M16 29V9m0 0L7 1m9 8 9-8M8 29h16"/>',jumper:'<path d="M2 16h28"/><circle cx="3" cy="16" r="2"/><circle cx="29" cy="16" r="2"/>'};
const icon=k=>`<svg viewBox="0 0 32 32" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.65" stroke-linejoin="round" stroke-linecap="round">${symbol[k]||'<path d="M10 16h12m-6-6v12"/>'}</svg>`;
function layout(){
 root.innerHTML=`
 <div class="rf-panel"><div class="rf-intro"><strong>${T('title')}</strong><p>${T('intro')}</p></div>
 <div class="rf-grid"><section class="rf-card"><h3>${T('board')}</h3><p class="rf-help">${T('boardhelp')}</p>
 <div class="rf-slots" aria-label="${T('slots')}" role="group">${[0,1,2,3].map(i=>`<button type="button" ${attr('slot',i)}></button>`).join('')}</div>
 <div class="rf-palette" role="group" aria-label="${T('parts')}">${parts.map(p=>`<button type="button" ${attr('part',p)}>${icon(p)}<span>${T(p)}</span></button>`).join('')}</div>
 <div class="rf-board-actions">${btn('action','remove','remove')}${btn('action','clear','clear')}</div><p class="rf-edit-note" data-rf-edit-note aria-live="polite"></p>
 <div class="rf-settings">
 <label>${T('gain')}<select ${attr('setting','gain')}><option value="8">+8 dB</option><option value="18">+18 dB</option><option value="24">+24 dB</option></select></label>
 <label>${T('load')}<select ${attr('setting','load')}>${Object.entries(loads).map(([k,v])=>`<option value="${k}">${T(k)} · ${v[0]}${v[1]? ' − j'+Math.abs(v[1]):''} Ω</option>`).join('')}</select></label>
 <label>${T('reactance')}<select ${attr('setting','reactance')}><option value="0">${T('bypass')}</option>${[25,75,85].map(v=>`<option value="${v}">${T('inductor')} · +j${v} Ω</option>`).join('')}</select></label>
 </div></section>
 <section class="rf-card"><h3>${T('map')}</h3><p class="rf-help">${T('maphelp')}</p>
 <svg data-rf-map tabindex="0" viewBox="0 0 580 330" role="group" aria-label="${T('map')}" aria-describedby="rf-map-keys">
  <defs><pattern id="rf-grid-pattern" width="20" height="20" patternUnits="userSpaceOnUse"><path d="M20 0H0V20" fill="none" stroke="#c4d7e3" stroke-width="1"/></pattern></defs>
  <rect width="580" height="330" rx="6" fill="#e9f2f6"/><rect width="580" height="330" rx="6" fill="url(#rf-grid-pattern)"/>
  <path data-rf-ray fill="none" stroke="#588397" stroke-width="1.5" stroke-dasharray="5 6"/>
  <circle data-rf-pulse r="7" fill="#00ac73" opacity="0"/>
  <g transform="translate(60 160)" class="rf-map-tx"><circle r="17" fill="#124a75"/><path d="M0-9V9M-5-7 0-11 5-7M-5 7 0 11 5 7" stroke="#fff" stroke-width="2" fill="none"/><text y="34" text-anchor="middle">${T('tx')}</text></g>
  <g data-rf-rx class="rf-map-rx"><circle data-rf-grip="move" r="23" fill="transparent"/><circle r="15" fill="#fff" stroke="#00765c" stroke-width="2.5"/>
   <g data-rf-axis><path d="M0-10V10M-5-8 0-12 5-8M-5 8 0 12 5 8" stroke="#00765c" stroke-width="2.5" fill="none"/><path d="M0-15V-24" stroke="#00765c" stroke-width="1.6"/><circle data-rf-grip="rotate" cx="0" cy="-27" r="9" fill="#e7b636" stroke="#513f13" stroke-width="1.4"/></g>
  </g>
 </svg>
 <p class="rf-keys" id="rf-map-keys">${T('keyhelp')}</p>
 <div class="rf-map-actions" role="group" aria-label="${T('map')}">${['left','right','up','down'].map(k=>btn('move',k,k)).join('')}${btn('rotate','left','turnleft')}${btn('rotate','right','turnright')}</div>
 <dl class="rf-map-stats"><div><dt>${T('rx')} (x, y)</dt><dd data-rf-stat="xy"></dd></div><div><dt>${T('distance')}</dt><dd data-rf-stat="distance"></dd></div><div><dt>${T('angle')}</dt><dd data-rf-stat="angle"></dd></div></dl></section></div>
 <div class="rf-console"><div class="rf-console-actions">${btn('action','transmit','transmit','rf-send')}${btn('action','reset','reset')}</div>
 <div data-rf-readout class="rf-readout"><div><span>${T('estimate')}</span><strong data-rf-power></strong></div>
 <div class="rf-losses"><span>${T('threshold')} ${sensitivity} dBm</span><span>${T('free')} <b data-rf-loss="free"></b></span><span>${T('mismatch')} <b data-rf-loss="mismatch"></b></span><span>${T('polar')} <b data-rf-loss="polar"></b></span></div>
 <p data-rf-status role="status" aria-atomic="true"></p></div></div>
 <details class="rf-model"><summary>${T('assumptions')}</summary><p>${T('modelA')}</p><p>${T('modelB')}</p><p>${T('modelC')}</p></details></div>`;
 for(const n of A('[data-rf-setting]'))n.value=String(state[n.dataset.rfSetting]);
 paint();
}
const dB=x=>10*Math.log10(x);
const fmt=(x,n=1)=>Number.isFinite(x)?x.toFixed(n):'−∞';
function result(){
 const d=Math.hypot(state.x-tx.x,state.y-tx.y);
 const fspl=20*Math.log10(4*Math.PI*d/wavelength);
 const [s,p,m,a]=state.slots;
 const valid=s==='source'&&(p==='pa'||p==='jumper')&&(m==='match'||m==='jumper')&&a==='antenna';
 if(!valid)return {d,fspl,valid};
 const [r,j]=loads[state.load],x=j+(m==='match'?state.reactance:0);
 const reflected=((r-z0)**2+x*x)/((r+z0)**2+x*x);
 const mismatch=dB(1-reflected);
 const pol=state.a===90?-Infinity:dB(Math.cos(state.a*Math.PI/180)**2);
 return {d,fspl,valid,mismatch,pol,power:-15+(p==='pa'?state.gain:0)+2+2-fspl+mismatch+pol};
}
function paint(){
 const r=result();
 A('[data-rf-slot]').forEach((el,i)=>{
  const part=state.slots[i],name=part?T(part):T('empty');
  if(el.dataset.filled!==(part||'')){
   el.dataset.filled=part||'';
   el.innerHTML=`<span class="rf-slot-num">${i+1}</span>${icon(part)}<span class="rf-slot-name">${name}</span>`;
  }
  el.setAttribute('aria-label',`${i+1}. ${name}`);
  el.setAttribute('aria-pressed',String(!!part&&part===state.selected));
 });
 A('[data-rf-part]').forEach(el=>{
  const p=el.dataset.rfPart,on=state.slots.includes(p);
  el.setAttribute('aria-pressed',String(p===state.selected));
  el.setAttribute('aria-label',T(p)+(on?' · '+T('existing'):''));
  el.dataset.onBoard=String(on);
 });
 Q('[data-rf-action="remove"]').disabled=!state.selected||!state.slots.includes(state.selected);
 const loc=(x,y)=>`${x*20} ${y*20}`;
 Q('[data-rf-rx]').setAttribute('transform',`translate(${loc(state.x,state.y)})`);
 Q('[data-rf-axis]').setAttribute('transform',`rotate(${state.a})`);
 Q('[data-rf-ray]').setAttribute('d',`M${loc(tx.x,tx.y)} L${loc(state.x,state.y)}`);
 Q('[data-rf-stat="xy"]').textContent=`${state.x.toFixed(1)}, ${state.y.toFixed(1)} m`;
 Q('[data-rf-stat="distance"]').textContent=r.d.toFixed(1)+' m';
 Q('[data-rf-stat="angle"]').textContent=state.a+'°';
 const output=Q('[data-rf-readout]');
 let status=state.transmitted?(!r.valid?'invalid':r.power===-Infinity?'null':r.power>=sensitivity?'linked':'weak'):'ready';
 output.dataset.state=status;output.dataset.predictedDbm=r.valid&&Number.isFinite(r.power)?r.power.toFixed(3):'';
 output.dataset.dbm=state.transmitted&&Number.isFinite(r.power)?r.power.toFixed(3):'';
 Q('[data-rf-power]').textContent=r.valid?fmt(r.power)+' dBm':T('inactive');
 const update=(k,v)=>Q('[data-rf-loss="'+k+'"]').textContent=v===undefined?'—':fmt(v)+' dB';
 update('free',r.fspl);update('mismatch',r.mismatch===undefined?undefined:-r.mismatch);update('polar',r.pol===-Infinity?Infinity:r.pol===undefined?undefined:-r.pol);
 if(r.pol===-Infinity)Q('[data-rf-loss="polar"]').textContent='∞ dB';
 const msg=T(status==='ready'?'ready':status==='linked'?'connected':status);
 const region=Q('[data-rf-status]');
 if(region.textContent!==msg)region.textContent=msg;
}
function stopPulse(){
 if(animation){animation.cancel();animation=null}if(pulseTimer){clearTimeout(pulseTimer);pulseTimer=0}
 root.classList.remove('rf-sending');
}
function change(){
 stopPulse();state.transmitted=false;Q('[data-rf-edit-note]').textContent='';paint();
}
function send(){
 stopPulse();state.transmitted=true;const r=result();paint();
 if(!r.valid||matchMedia('(prefers-reduced-motion: reduce)').matches)return;
 const pulse=Q('[data-rf-pulse]');
 root.classList.add('rf-sending');
 if(pulse.animate)animation=pulse.animate([
 {transform:`translate(${20*tx.x}px,${20*tx.y}px)`,opacity:1},
 {transform:`translate(${20*state.x}px,${20*state.y}px)`,opacity:0.9,offset:.92},
 {transform:`translate(${20*state.x}px,${20*state.y}px)`,opacity:0}
 ],{duration:740,easing:'linear'});
 pulseTimer=setTimeout(()=>{root.classList.remove('rf-sending');pulseTimer=0},780);
}
function place(i){
 const current=state.slots[i],selected=state.selected;
 if(!selected){if(current)select(current);else Q('[data-rf-edit-note]').textContent=T('drop');return}
 if(current===selected){select(selected);return}
 const from=state.slots.indexOf(selected);
 if(from>=0)state.slots[from]=current;
 state.slots[i]=selected;state.selected=null;change();
}
function select(p){
 state.selected=state.selected===p?null:p;
 Q('[data-rf-edit-note]').textContent=state.selected?`${T('picked')}: ${T(p)}`:'';
 paint();
}
const clamp=(v,a,b)=>Math.min(b,Math.max(a,v));
const half=v=>Math.round(v*2)/2;
function moveTo(x,y){
 x=half(clamp(x,5,27));y=half(clamp(y,2,14.5));
 if(x===state.x&&y===state.y)return;
 state.x=x;state.y=y;change();
}
function turnTo(a){
 a=((Math.round(a/15)*15%180)+180)%180;
 if(a!==state.a){state.a=a;change()}
}
function move(k){
 const d={left:[-1,0],right:[1,0],up:[0,-1],down:[0,1]}[k];
 if(d)moveTo(state.x+d[0],state.y+d[1]);
}
function mapPoint(event){
 const map=Q('[data-rf-map]'),pt=map.createSVGPoint();
 pt.x=event.clientX;pt.y=event.clientY;
 const mat=map.getScreenCTM();if(!mat)return null;
 const p=pt.matrixTransform(mat.inverse());return {x:p.x/20,y:p.y/20};
}
root.addEventListener('click',e=>{
 const b=e.target.closest('button');if(!b)return;
 const {rfAction:a,rfSlot:i,rfPart:p,rfMove:m,rfRotate:t}=b.dataset;
 if(p)select(p);else if(i!==undefined)place(Number(i));
 else if(m)move(m);else if(t)turnTo(state.a+(t==='right'?15:-15));
 else if(a==='transmit')send();
 else if(a==='clear'){state.slots=[null,null,null,null];state.selected=null;change()}
 else if(a==='remove'){
  const idx=state.slots.indexOf(state.selected);
  if(idx>=0){state.slots[idx]=null;state.selected=null;change();Q('[data-rf-slot="'+idx+'"]').focus()}
 }else if(a==='reset'){
  stopPulse();state=start();layout();Q('[data-rf-action="reset"]').focus();
 }
});
root.addEventListener('change',e=>{
 const k=e.target.dataset.rfSetting;if(!k)return;
 state[k]=k==='load'?e.target.value:Number(e.target.value);change();
});
root.addEventListener('keydown',e=>{
 if(!e.target.matches('[data-rf-map]')||e.altKey||e.ctrlKey||e.metaKey)return;
 const keys={ArrowLeft:'left',ArrowRight:'right',ArrowUp:'up',ArrowDown:'down'};
 if(keys[e.key]){e.preventDefault();move(keys[e.key])}
 else if(e.key==='['||e.key===']'){e.preventDefault();turnTo(state.a+(e.key===']'?15:-15))}
});
root.addEventListener('pointerdown',e=>{
 const map=e.target.closest('[data-rf-map]');if(!map||!e.isPrimary||e.button!==0)return;
 const mode=e.target.closest('[data-rf-grip="rotate"]')?'rotate':e.target.closest('[data-rf-rx]')?'drag':'tap';
 dragging={pointer:e.pointerId,mode,startX:e.clientX,startY:e.clientY,moved:false};
 if(mode!=='tap'){try{map.setPointerCapture?.(e.pointerId)}catch{/* An already-ended pointer cannot be captured. */}}
});
root.addEventListener('pointermove',e=>{
 if(!dragging||dragging.pointer!==e.pointerId)return;
 if(Math.hypot(e.clientX-dragging.startX,e.clientY-dragging.startY)>3)dragging.moved=true;
 if(!dragging.moved||dragging.mode==='tap')return;
 const p=mapPoint(e);if(!p)return;
 if(dragging.mode==='drag')moveTo(p.x,p.y);else turnTo(Math.atan2(p.y-state.y,p.x-state.x)*180/Math.PI+90);
});
root.addEventListener('pointerup',e=>{
 if(!dragging||dragging.pointer!==e.pointerId)return;
 if(dragging.mode==='tap'&&!dragging.moved){const p=mapPoint(e);if(p)moveTo(p.x,p.y)}
 dragging=null;
});
root.addEventListener('pointercancel',()=>dragging=null);
document.addEventListener('neca:lang',()=>{
 const old=document.activeElement;
 const k=root.contains(old)&&Object.keys(old.dataset).find(n=>/^rf(Action|Part|Slot|Move|Rotate|Setting|Map)$/.test(n));
 const value=k?old.dataset[k]:'';
 stopPulse();layout();
 if(k){const a=k.replace(/[A-Z]/g,s=>'-'+s.toLowerCase());const el=Q(value?`[data-${a}="${value}"]`:`[data-${a}]`);el?.focus({preventScroll:true})}
});
layout();
})();
