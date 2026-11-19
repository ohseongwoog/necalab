/* A transparent, fixed-weight teaching model. No training, network requests or persistence. */
(() => {
'use strict';
const mount=document.querySelector('[data-lab="ai"]');if(!mount)return;
const P=(ko,en)=>({ko,en});
const HELP=P('키워드 규칙과 고정 가중치로 계산하는 교육용 모형입니다. 학습된 AI나 LLM이 아니며 입력을 전송하거나 저장하지 않습니다.','This teaching model uses keyword rules and fixed weights. It is not a trained AI or an LLM. Inputs are never sent or stored.');
const kinds=[
 {id:'connection',color:'#155d98',name:P('연결','Connection'),cue:P('연결 불안정','Connection problems'),terms:[
  ['wifi','wi-fi','network','와이파이','무선','네트워크','인터넷'],
  ['disconnect','disconnects','disconnected','latency','timeout','timeouts','연결','끊김','끊어','끊겨','끊기','지연'],
  ['gateway','gateways','router','routers','ethernet','라우터','공유기','게이트웨이']
 ]},
 {id:'hardware',color:'#854624',name:P('장비','Hardware'),cue:P('장비 이상','Equipment problems'),terms:[
  ['power','battery','batteries','전원','배터리'],
  ['reboot','reboots','rebooting','restarted','restart','재부팅','재시작'],
  ['overheat','overheats','overheating','fan','fans','과열','팬','뜨거']
 ]},
 {id:'data',color:'#006849',name:P('데이터','Data'),cue:P('파일·데이터 오류','File or data errors'),terms:[
  ['file','files','data','csv','파일','데이터'],
  ['upload','uploads','uploaded','export','exports','업로드','내보내','내보낸'],
  ['missing','format','corrupt','corrupted','누락','형식','손상','없어']
 ]}
];
const samples={
 connection:{text:P('와이파이가 계속 끊기고 라우터를 다시 연결해도 나아지지 않아요.','The Wi-Fi disconnects repeatedly, even after reconnecting the router.'),cues:[1,4,0]},
 hardware:{text:P('전원은 들어오는데 장비가 과열되고 자꾸 재부팅돼요.','The power comes on, but the equipment keeps overheating and rebooting.'),cues:[0,3,1]},
 data:{text:P('업로드한 CSV 파일에 일부 행이 누락됐어요.','Rows are missing from the CSV file after upload.'),cues:[0,1,3]}
};
const L={
 intro:P('시작 예시에서 문장은 연결 문제를, 표는 하드웨어 문제를 가리킵니다. 텍스트 가중치를 낮춰 본 뒤 문장과 표를 직접 바꿔 보세요.','In the starting example, the message points to a connection issue while the observations favor hardware. Lower the text weight, then edit the inputs yourself.'),
 input:P('입력','Input'),features:P('특징','Features'),model:P('모형','Model'),output:P('출력','Output'),
 message:P('문의 내용','Support message'),placeholder:P('예: 와이파이가 자꾸 끊겨요.','Example: My Wi-Fi keeps disconnecting.'), sample:P('예시 불러오기','Load an example'),reset:P('초기화·입력 비우기','Reset and clear'),
 obs:P('현장 관측값 (0: 없음, 5: 강함)','Observations (0 = none, 5 = strong)'),signal:P('관측 신호','Observation'),value:P('강도','Strength'),
 rule:P('텍스트의 키워드 묶음은 분야별로 최대 3개가 반영됩니다. 0–5 관측값은 0–1로 바뀌며, 두 신호에 각각 가중치를 적용해 더합니다.','Up to three keyword groups count per topic. The model scales the 0–5 observations to 0–1, weights each input, and adds the two signals.'),
 matched:P('잡아낸 키워드','Recognized keywords'),group:P('분야','Topic'),wordMatches:P('텍스트 · /3','Text · /3'),table:P('관측 · /5','Table · /5'),fused:P('결합값','Combined'),
 controls:P('모형 조절','Model controls'),textWeight:P('텍스트 가중치','Text weight'),tableWeight:P('관측값 가중치','Table weight'),depth:P('은닉층 수','Hidden layers'),
 modelNotes:P('각 층은 자기 분야에 0.90, 다른 두 분야에 각각 0.15를 곱해 더한 뒤 tanh를 적용합니다. 연결선이 진할수록 다음 층에 전달되는 값이 큽니다.','Each layer weights its own topic by 0.90 and each other topic by 0.15, adds them, then applies tanh. Darker links carry larger values to the next layer.'),
 activations:P('층별 활성값','Activations by layer'),layer:P('은닉층','Layer'),inputShort:P('결합','Mix'),outputShort:P('점수','Score'),
 ops:P('모형 연산 수','Modeled operations'),latency:P('지연 모형','Latency model'),tick:P('틱','ticks'),
 countNotes:P('연산 수는 결합·은닉층·점수 계산의 스칼라 연산을 센 값입니다. 지연은 기본 3틱에 층당 2틱을 더한 모형이며 실제 실행 시간은 아닙니다.','The operation count covers scalar arithmetic for combining signals, hidden layers, and scoring. The latency model starts at three ticks and adds two per layer. It is not measured runtime.'),
 proposed:P('추천 담당','Suggested route'),routeNone:P('분류 보류','No route yet'),routeTie:P('여러 담당이 비슷함','Topics are tied'),noCues:P('키워드가 있는 문의나 관측값을 입력하고, 해당 가중치를 0보다 크게 설정하세요.','Enter a message with recognized clues or a nonzero observation, and give that source a weight above zero.'),
 scoreNotes:P('모형 안에서만 비교하는 점수입니다. 실제 신뢰도나 정답률이 아닙니다.','Scores compare topics within this model. They are not real-world confidence or accuracy.')
};
const initial=()=>({text:'',cues:[0,0,0],wt:1.2,wo:0.8,depth:2});
let state=initial(),lang=document.documentElement.lang.startsWith('en')?'en':'ko',ui={},queued;
let sourceSample='connection';
state.text=samples.connection.text[lang];state.cues=samples.connection.cues.slice();
const tr=p=>p[lang];
const E=(tag,cls='',content)=>{const node=document.createElement(tag);if(cls)node.className=cls;if(content!==undefined)node.textContent=String(content);return node;};
const S=(tag,attrs={})=>{const el=document.createElementNS('http://www.w3.org/2000/svg',tag);Object.entries(attrs).forEach(([k,v])=>el.setAttribute(k,v));return el;};
const button=(id,content,cls='ai-button')=>{const b=E('button',cls,content);b.type='button';b.dataset.aiAction=id;return b;};
const norm=x=>x.normalize('NFKC').toLowerCase().replace(/[‐‑‒–—−]/g,'-');
function matchesFor(msg,topic){
 return topic.terms.map(terms=>terms.find(term=>{
  if(/[가-힣]/.test(term))return msg.includes(term);
  const target=term.replace(/[.*+?^${}()|[\]\\]/g,'\\$&');
  return new RegExp('(^|[^a-z0-9])'+target+'($|[^a-z0-9])').test(msg);
 })).filter(Boolean);
}
function run(){
 const matches=kinds.map(topic=>matchesFor(norm(state.text),topic));
 const text=matches.map(terms=>terms.length);
 const combined=text.map((n,i)=>state.wt*(n/3)+state.wo*(state.cues[i]/5));
 const layers=[];
 let v=combined;
 for(let l=0;l<state.depth;l++){
  v=v.map((n,i)=>Math.tanh(0.90*n+0.15*v[(i+1)%3]+0.15*v[(i+2)%3]));
  layers.push(v);
 }
 const strength=v.map(n=>Math.exp(2.6*n));
 const total=strength[0]+strength[1]+strength[2];
 const scores=strength.map(n=>n/total);
 const high=Math.max(...scores);
 const best=scores.map((n,i)=>({n,i})).filter(x=>Math.abs(high-x.n)<1e-9);
 return {text,matches,combined,layers,scores,route:combined.every(x=>x===0)?'none':best.length!==1?'tie':kinds[best[0].i].id,ops:20+18*state.depth,ticks:3+2*state.depth};
}
function stage(parent,id,name){
 const section=E('section','ai-stage ai-stage-'+id);
 section.setAttribute('aria-labelledby','ai-stage-'+id);
 const title=E('h4','ai-stage-title',tr(name));title.id='ai-stage-'+id;section.append(title);parent.append(section);return section;
}
function th(txt,scope='col'){const el=E('th','',txt);el.scope=scope;return el}
function table(headers){
 const shell=E('div','ai-table-shell'),t=E('table','ai-table'),head=E('thead'),row=E('tr'),body=E('tbody');
 headers.forEach(h=>row.append(th(h)));head.append(row);t.append(head,body);shell.append(t);return [shell,body];
}
function render(){
 const active=document.activeElement;
 const focused=mount.contains(active)?active.id:null;
 const selection=active===ui.ta?[active.selectionStart,active.selectionEnd]:null;
 const intro=E('p','ai-intro',tr(L.intro)),wrap=E('div','ai-lab-grid');
 const input=stage(wrap,'input',L.input),features=stage(wrap,'features',L.features),model=stage(wrap,'model',L.model),output=stage(wrap,'output',L.output);
 const label=E('label','ai-label',tr(L.message));label.htmlFor='ai-message';
 const ta=E('textarea','ai-message');ta.id='ai-message';ta.dataset.aiText='';ta.value=state.text;ta.rows=3;ta.maxLength=320;ta.placeholder=tr(L.placeholder);ta.autocomplete='off';ta.spellcheck=false;
 const actions=E('div','ai-samples');actions.setAttribute('role','group');actions.setAttribute('aria-label',tr(L.sample));
 for(const kind of kinds){const b=button('sample-'+kind.id,tr(kind.name));b.id='ai-sample-'+kind.id;actions.append(b)}
 const reset=button('reset',tr(L.reset),'ai-button ai-reset');reset.id='ai-reset';
 const fieldTable=table([tr(L.signal),tr(L.value)]),caption=E('caption','ai-caption',tr(L.obs));fieldTable[0].firstElementChild.prepend(caption);
 const fields=[];
 kinds.forEach((kind,i)=>{
  const row=E('tr'),header=E('th'),lab=E('label','',tr(kind.cue));header.scope='row';header.append(lab);
  const td=E('td'),field=E('input','ai-number');field.type='number';field.min='0';field.max='5';field.step='1';field.id='ai-cue-'+kind.id;field.dataset.aiField=kind.id;field.value=String(state.cues[i]);lab.htmlFor=field.id;td.append(field);row.append(header,td);fieldTable[1].append(row);fields.push(field);
 });
 const sampleLabel=E('p','ai-caption',tr(L.sample));
 input.append(label,ta,sampleLabel,actions,fieldTable[0],reset);

 const transform=table([tr(L.group),tr(L.wordMatches),tr(L.table),tr(L.fused)]),featureRows=[];
 kinds.forEach(kind=>{
  const row=E('tr'),a=E('td'),b=E('td'),c=E('td');row.append(th(tr(kind.name),'row'),a,b,c);transform[1].append(row);featureRows.push([a,b,c]);
 });
 const featuresHint=E('p','ai-note',tr(L.rule));
 const keywords=E('div','ai-keywords'),keywordList=E('ul');keywords.append(E('p','ai-caption',tr(L.matched)),keywordList);
 features.append(transform[0],keywords,featuresHint);

 const control=E('div','ai-controls');control.setAttribute('role','group');control.setAttribute('aria-label',tr(L.controls));
 const sliders={};
 for(const [name,stateKey,description,min,max,step] of [['text','wt',L.textWeight,0,2,0.1],['table','wo',L.tableWeight,0,2,0.1],['depth','depth',L.depth,1,4,1]]){
  const block=E('div','ai-slider'),top=E('div','ai-slider-label'),label=E('label','',tr(description));
  const el=E('input','ai-range');el.type='range';el.id='ai-param-'+name;el.dataset.aiParameter=name;el.min=String(min);el.max=String(max);el.step=String(step);el.value=state[stateKey];label.htmlFor=el.id;
  const v=E('output','ai-number-readout');v.htmlFor=el.id;v.id=el.id+'-value';
  top.append(label,v);block.append(top,el);control.append(block);sliders[name]={el,v,stateKey};
 }
 const viz=E('div','ai-diagram');viz.setAttribute('aria-hidden','true');
 const layerList=table([tr(L.activations),...kinds.map(k=>tr(k.name))]);
 const metrics=E('dl','ai-metrics'),ops=E('dd'),latency=E('dd');ops.dataset.aiOps='';latency.dataset.aiLatency='';metrics.append(E('dt','',tr(L.ops)),ops,E('dt','',tr(L.latency)),latency);
 model.append(control,viz,E('p','ai-note',tr(L.modelNotes)),layerList[0],metrics,E('p','ai-note',tr(L.countNotes)));

 const route=E('p','ai-route'),scoreList=E('ul','ai-scores'),scores=[];
 route.dataset.aiRoute='none';
 const status=E('div','ai-sr');status.setAttribute('role','status');status.setAttribute('aria-atomic','true');
 for(const kind of kinds){
  const li=E('li','ai-score'),scoreRow=E('div','ai-score-line'),amount=E('span','ai-score-value','—'),track=E('div','ai-track'),bar=E('span','ai-bar');
  li.dataset.aiScore=kind.id;track.setAttribute('aria-hidden','true');bar.style.setProperty('--ai-color',kind.color);track.append(bar);scoreRow.append(E('span','',tr(kind.name)),amount);li.append(scoreRow,track);scoreList.append(li);scores.push({amount,bar});
 }
 const explain=E('p','ai-note ai-output-note');
 output.append(E('p','ai-output-label',tr(L.proposed)),route,scoreList,explain,status);
 mount.classList.add('ai-lab');mount.replaceChildren(intro,wrap,E('p','ai-disclaimer',tr(HELP)));
 ui={ta,fields,featureRows,keywords,keywordList,sliders,viz,layers:layerList[1],ops,latency,route,explain,scores,status};
 refresh(false);
 if(focused){
  const restored=document.getElementById(focused);
  if(restored&&mount.contains(restored)){restored.focus({preventScroll:true});if(selection&&restored===ta)ta.setSelectionRange(...selection)}
 }
}
function graph(result){
 const svg=S('svg',{viewBox:'0 0 440 124',role:'presentation',focusable:'false'});
 const columns=[result.combined,...result.layers,result.scores];
 const points=columns.map((v,i)=>({values:v,x:38+i*(364/(columns.length-1))}));
 const y=[34,64,94];
 points.slice(1).forEach(({x},i)=>{
  const prev=points[i];
  for(let to=0;to<3;to++){
   for(let from=0;from<3;from++){
    const readout=i===points.length-2;
    if(readout && to!==from)continue;
    const carry=readout?(result.route==='none'?0:result.scores[to]):Math.min(1,prev.values[from]*(to===from?0.90:0.15));
    svg.append(S('line',{x1:prev.x,y1:y[from],x2:x,y2:y[to],stroke:kinds[from].color,'stroke-opacity':0.12+0.75*carry,'stroke-width':0.75+4*carry}));
   }
  }
 });
 points.forEach(({values,x},i)=>{
  const name=S('text',{x,y:16,'text-anchor':'middle',fill:'#263d57','font-size':lang==='en'?11:12,'font-weight':700});
  name.textContent=i===0?tr(L.inputShort):i===points.length-1?tr(L.outputShort):'H'+i;svg.append(name);
  values.forEach((v,j)=>{
   const f=Math.max(0,Math.min(1,v)),pct=result.route==='none' && i===points.length-1 ? 0 : f;
   svg.append(S('circle',{cx:x,cy:y[j],r:4+4*pct,fill:pct>0.01?kinds[j].color:'#ffffff','fill-opacity':pct>0.01?0.25+0.75*pct:1,stroke:kinds[j].color,'stroke-width':1.5}));
  });
 });
 return svg;
}
function updateInputControls(){
 ui.ta.value=state.text;ui.fields.forEach((f,i)=>f.value=state.cues[i]);
 for(const {el,stateKey} of Object.values(ui.sliders))el.value=state[stateKey];
}
function refresh(announce=true){
 const result=run();
 ui.featureRows.forEach(([a,b,c],i)=>{a.textContent=result.text[i]+' / 3';b.textContent=state.cues[i]+' / 5';c.textContent=result.combined[i].toFixed(2)});
 ui.keywords.hidden=result.text.every(n=>n===0);
 ui.keywordList.replaceChildren(...result.matches.flatMap((terms,i)=>terms.length?[E('li','',tr(kinds[i].name)+': '+terms.join(' · '))]:[]));
 for(const {stateKey,v} of Object.values(ui.sliders))v.value=stateKey==='depth'?String(state.depth):state[stateKey].toFixed(1)+'×';
 ui.viz.replaceChildren(graph(result));
 ui.layers.replaceChildren(...result.layers.map((values,i)=>{
  const row=E('tr');row.dataset.aiLayer=String(i+1);row.append(th(tr(L.layer)+' '+(i+1),'row'),...values.map(n=>E('td','',n.toFixed(2))));return row;
 }));
 ui.ops.textContent=String(result.ops);ui.latency.textContent=result.ticks+' '+tr(L.tick);
 const previous=ui.route.dataset.aiRoute,match=kinds.find(k=>k.id===result.route);
 ui.route.dataset.aiRoute=result.route;
 ui.route.textContent=match?tr(match.name):tr(result.route==='none'?L.routeNone:L.routeTie);
 ui.explain.textContent=tr(result.route==='none'?L.noCues:L.scoreNotes);
 result.scores.forEach((n,i)=>{
  const hidden=result.route==='none';const pct=hidden?0:n*100;
  const {amount,bar}=ui.scores[i];amount.textContent=hidden?'—':pct.toFixed(1)+'%';bar.style.width=pct+'%';
 });
 if(announce && previous!==result.route){
  clearTimeout(queued);
  queued=setTimeout(()=>{ui.status.textContent=tr(L.proposed)+': '+ui.route.textContent},240);
 }
}
mount.addEventListener('input',event=>{
 const el=event.target;
 if(el.hasAttribute('data-ai-text')){sourceSample=null;state.text=el.value.slice(0,320)}
 else if(el.dataset.aiField){
  const i=kinds.findIndex(k=>k.id===el.dataset.aiField);
  const number=el.valueAsNumber;state.cues[i]=Number.isFinite(number)?Math.round(Math.max(0,Math.min(5,number))):0;
 }else if(el.dataset.aiParameter){
  const control=ui.sliders[el.dataset.aiParameter];state[control.stateKey]=Number(el.value);
 }else return;
 refresh();
});
mount.addEventListener('change',event=>{
 const i=kinds.findIndex(k=>k.id===event.target.dataset.aiField);if(i>=0)event.target.value=state.cues[i];
});
mount.addEventListener('click',event=>{
 const action=event.target.closest('[data-ai-action]');if(!action||!mount.contains(action))return;
 const id=action.dataset.aiAction;
 if(id==='reset'){state=initial();sourceSample=null}
 else if(id.startsWith('sample-') && samples[id.slice(7)]){
  sourceSample=id.slice(7);const scenario=samples[sourceSample];state.text=tr(scenario.text);state.cues=scenario.cues.slice();
 }else return;
 updateInputControls();refresh();
});
function localize(){
 const next=document.documentElement.lang.startsWith('en')?'en':'ko';if(next===lang)return;
 clearTimeout(queued);if(sourceSample)state.text=samples[sourceSample].text[next];lang=next;render();
}
document.addEventListener('neca:lang',localize);
new MutationObserver(localize).observe(document.documentElement,{attributes:true,attributeFilter:['lang']});
render();
})();
