/* NECA mini challenges: deterministic teaching scenarios, entirely in the browser. */
(() => {
'use strict';
const words=(ko,en)=>({ko,en});
const cards=(...entries)=>entries.map(([id,ko,en])=>({id,label:words(ko,en)}));
const ai=[
 {
  title:words('빗속의 시연','The rainy-day demo'),
  prompt:words('오늘 오후 2시 야외 시연은 어디에서 열릴까요? 방문객에게 근거 있는 안내를 보내세요.','Where will today’s 2 p.m. outdoor demo take place? Send visitors an answer you can support.'),
  clues:cards(['a','오늘 13:45 기상 알림: 시연 장소에 호우주의보 발효.','Today, 1:45 p.m. weather alert: heavy-rain advisory in effect at the demo site.'],['b','지난주 사진: 맑은 날 야외에서 시연을 진행했다.','Photo from last week: the demo was outdoors on a clear day.'],['c','현행 운영 안내: 호우주의보가 발효되면 야외 시연을 1층 로비로 옮긴다.','Current event rule: when a heavy-rain advisory is in effect, move outdoor demos to the ground-floor lobby.'],['d','오늘 이동 안내: 북문 쪽 자전거 거치대를 이용할 수 있다.','Today’s travel notice: bike racks near the north gate are available.']),
  answers:cards(['a','예정대로 야외에서 열린다.','It will go ahead outdoors.'],['b','1층 로비에서 열린다.','It will take place in the ground-floor lobby.'],['c','시연이 취소된다.','The demo will be canceled.']),
  key:['a','c'],answer:'b',
  hint:words('오늘 실제로 발효된 알림과 그 알림에 대응하는 규칙을 한 장씩 찾으세요.','Find one clue about today’s alert and one about what to do when that alert is active.'),
  why:words('A는 오늘 호우주의보가 발효됐다는 사실을, C는 그때 로비로 옮긴다는 규칙을 보여줍니다. 취소한다는 근거는 없습니다.','A establishes that today’s advisory is active. C says an active advisory moves the demo indoors; it does not cancel the event.')
 },
 {
  title:words('돌아온 계측기?','The missing return'),
  prompt:words('오늘 17:30 기준, 계측기 Q-7이 반납됐다고 확인할 수 있을까요? 예정과 기록을 구분하세요.','As of 5:30 p.m. today, can you verify that meter Q-7 has been returned? Separate the plan from what was recorded.'),
  clues:cards(['a','어제 완료 기록: 계측기 Q-9을 반납했다.','Yesterday’s completed log: meter Q-9 was returned.'],['b','오늘 Q-7 대여대장: 반납 예정 시각 17:00.','Today’s Q-7 checkout log: return due at 5 p.m.'],['c','공용 안내: 계측기는 지정 보관함에 반납한다.','General notice: return meters to the designated cabinet.'],['d','오늘 17:30 Q-7 기록: 실제 반납 확인란이 비어 있고 보관함 점검은 아직 하지 않았다.','Today, 5:30 p.m. Q-7 record: the confirmed-return field is blank, and the cabinet has not yet been checked.']),
  answers:cards(['a','17시까지 반납된 것이 확인됐다.','It was confirmed returned by 5 p.m.'],['b','아직 반납하지 않았다는 것이 확인됐다.','It is confirmed not yet returned.'],['c','현재 기록만으로는 확인할 수 없다.','The current records do not confirm either way.']),
  key:['b','d'],answer:'c',
  hint:words('Q-7의 오늘 기록 두 장을 찾으세요. 예정 시각과 실제 반납 확인은 같은 정보가 아닙니다.','Find the two clues about today’s Q-7 records. A due time is not a verified return time.'),
  why:words('B의 17:00은 예정입니다. D의 빈 확인란은 반납과 미반납 어느 쪽도 입증하지 못합니다.','B gives a deadline, not a confirmed return. D’s blank field proves neither a return nor a non-return.')
 },
 {
  title:words('초록불을 기다려요','Wait for green'),
  prompt:words('지금 14:10, 안내원은 실험실 앞 방문객에게 뭐라고 해야 할까요?','It’s 2:10 p.m. What should the guide tell visitors waiting outside the test room?'),
  clues:cards(['a','현행 방문 안내: 시험이 진행 중이면 입구 표시등이 녹색으로 바뀔 때까지 기다린다.','Current visitor rule: during a test, wait until the entrance light turns green.'],['b','어제 14:10 점검표: 입구 표시등 녹색.','Yesterday’s 2:10 p.m. log: the entrance light was green.'],['c','다음 주 안내표: 정기 설명회는 14:00 시작.','Next week’s timetable: the regular talk begins at 2 p.m.'],['d','오늘 14:10 시험 기록: 시험 진행 중, 입구 표시등 주황색.','Today’s 2:10 p.m. test log: test in progress, entrance light amber.']),
  answers:cards(['a','지금은 기다리고, 녹색으로 바뀌면 들어간다.','Wait now; enter once the light turns green.'],['b','어제 녹색이었으니 지금 들어간다.','Enter now because the light was green yesterday.'],['c','현재 표시등 상태를 알 수 없다.','The current light status is unknown.']),
  key:['a','d'],answer:'a',
  hint:words('어제 표시는 오늘 상태가 아닙니다. 오늘 기록을 현행 안내와 맞춰 보세요.','Yesterday’s light is not today’s status. Compare the current rule with today’s log.'),
  why:words('D의 현재 상태는 시험 중이고, A는 녹색으로 바뀔 때 입장해도 된다고 안내합니다.','D shows the test is currently running. A tells visitors to wait for the green light.')
 }
];

const rf=[
 {
  title:words('센서 신호를 공중으로','Send a sensor signal'),mode:'path',
  prompt:words('칩에서 이미 만들어진 작은 RF 신호를 안테나로 내보내세요. 소자를 누른 순서대로 연결됩니다.','Your chip has already generated a weak RF signal. Send it out over the air. Tap the three blocks in signal-flow order.'),
  start:words('칩의 RF 출력','Chip RF output'),end:words('공중으로','Out over the air'),
  parts:cards(['match','출력 정합 회로','Output matching network'],['lna','저잡음 증폭기(LNA)','Low-noise amplifier (LNA)'],['antenna','송신 안테나','Transmit antenna'],['pa','전력 증폭기(PA)','Power amplifier (PA)']),
  key:['pa','match','antenna'],
  hint:words('작은 신호의 전력을 먼저 키웁니다. 정합 회로는 전력 증폭기 출력과 안테나 사이에서 임피던스를 맞춥니다.','Boost the weak signal’s power first. The matching network transforms the load seen at the PA output before the antenna radiates.'),
  why:words('PA가 RF 전력을 키우고 출력 정합 회로가 증폭기에 적절한 부하 임피던스를 만들어 줍니다. 마지막 안테나가 전파를 내보냅니다.','The PA boosts RF power. The output matching network presents an appropriate load to the PA. The antenna converts the guided signal into radiated waves.')
 },
 {
  title:words('작은 수신 신호 살리기','Recover a faint signal'),mode:'path',
  prompt:words('공중에서 온 약한 전파를 칩이 처리할 낮은 중간주파수(IF) 신호로 바꿔 보세요. 이 예에서는 필터와 정합 회로가 이미 준비돼 있습니다.','Turn a faint radio wave into a lower intermediate-frequency (IF) signal for the chip. Assume the required filters and matching are already in place.'),
  start:words('공중 전파','Incoming radio wave'),end:words('낮은 IF 출력','Lower IF output'),
  parts:cards(['mixer','하향변환 믹서','Downconversion mixer'],['antenna','수신 안테나','Receive antenna'],['pa','송신 전력 증폭기(PA)','Transmit power amplifier (PA)'],['lna','저잡음 증폭기(LNA)','Low-noise amplifier (LNA)']),
  key:['antenna','lna','mixer'],
  hint:words('먼저 전파를 받습니다. 그다음 잡음을 적게 보태며 신호를 키운 뒤 주파수를 내립니다.','Capture the wave first. Then amplify the weak signal with little added noise before shifting it to a lower frequency.'),
  why:words('안테나가 전파를 받아 RF 신호를 만들고, LNA가 잡음을 적게 더하며 증폭합니다. 믹서가 국부 발진기 신호를 이용해 더 낮은 IF로 변환합니다.','The antenna captures the wave. The LNA amplifies the signal while adding little noise. The mixer uses a local oscillator to convert it to a lower IF.')
 },
 {
  title:words('반사를 줄이는 부품 하나','One component to stop the reflection'),mode:'match',
  prompt:words('한 주파수에서 50 Ω 선로가 50 − j25 Ω 안테나에 연결돼 있습니다. 이상적인 소자 하나를 직렬로 넣어 반사를 없애세요.','At one frequency, a 50 Ω line feeds an antenna with impedance 50 − j25 Ω. Add one ideal series component to eliminate the reflection.'),
  answers:cards(['a','커패시터: −j25 Ω','Capacitor: −j25 Ω'],['b','인덕터: +j25 Ω','Inductor: +j25 Ω'],['c','저항: +25 Ω','Resistor: +25 Ω']),
  answer:'b',
  hint:words('50 Ω인 실수부는 그대로 두고, −j25 Ω과 더해서 0이 되는 허수부를 찾으세요.','Keep the 50 Ω real part. Find the imaginary part that adds to −j25 Ω to give zero.'),
  why:words('직렬 임피던스는 더해집니다. (50 − j25) Ω + j25 Ω = 50 Ω이므로 이 주파수에서 이상적인 반사계수는 0입니다. 광대역 정합이나 방사 효율까지 보장하지는 않습니다.','Series impedances add: (50 − j25) Ω + j25 Ω = 50 Ω, so the ideal reflection coefficient is zero at this frequency. This does not guarantee a broadband match or radiation efficiency.')
 }
];

const labels={
 progress:words('문제','Round'),
 clues:words('1. 근거 두 장 고르기','1. Pick two pieces of evidence'),
 answersAI:words('2. 결론 고르기','2. Choose a conclusion'),
 parts:words('회로 소자','Circuit blocks'),
 answersRF:words('직렬 소자 하나 고르기','Choose one series component'),
 slots:words('현재 연결 순서','Current signal path'),
 slot:words('빈 슬롯','Empty slot'),
 check:words('정답 확인','Check answer'),
 hint:words('힌트','Hint'),
 reset:words('다시 풀기','Reset round'),
 next:words('다음 문제','Next round'),
 replay:words('첫 문제로','Back to round one'),
 undo:words('마지막 연결 취소','Undo last connection'),
 ready:words('선택한 내용을 확인해 보세요.','Ready to check your choices.'),
 none:words('선택한 내용을 여기에서 확인할 수 있습니다.','Feedback appears here when you check your answer.'),
 max:words('근거는 두 장까지 선택할 수 있어요. 바꾸려면 선택한 카드를 다시 누르세요.','You can choose two clues. To swap one, press a selected card to deselect it.'),
 full:words('슬롯이 찼습니다. 순서를 바꾸려면 마지막 연결을 취소하세요.','The slots are full. Undo the last connection to change the order.'),
 chooseAI:words('정답을 확인하려면 서로 다른 근거 두 장과 결론 하나를 골라 주세요.','Pick two different clues and a conclusion before checking.'),
 choosePath:words('정답을 확인하려면 소자 세 개를 원하는 순서로 채워 주세요.','Fill all three slots in signal-flow order before checking.'),
 chooseMatch:words('소자를 하나 골라 주세요.','Choose one component before checking.'),
 wrongAI:words('근거를 다시 살펴보세요. 질문의 대상과 현재 조건을 함께 뒷받침하는 자료여야 합니다.','Look again at the evidence. Together the two clues should address the right subject and the current situation.'),
 wrongConclusion:words('근거는 맞았어요. 두 근거를 함께 읽고, 그 이상을 단정하지 않는 결론을 찾아보세요.','You found the two clues. Now choose the conclusion that follows without assuming more than they say.'),
 wrongPath:words('아직 신호가 목적지에 닿지 않았어요. 출발 신호와 각 소자의 역할을 다시 확인해 보세요.','The signal has not made it through yet. Reconsider the starting signal and what each block does.'),
 wrongMatch:words('아직 반사가 남습니다. 고른 소자의 임피던스를 안테나 임피던스에 더해 보세요.','There would still be a reflection. Try adding your chosen component’s impedance to the antenna impedance.'),
 correct:words('정답!','Correct!'),
 resetMessage:words('이 문제를 처음 상태로 되돌렸습니다.','This round has been reset.')
};

const doc=document,language=()=>doc.documentElement.lang.startsWith('en')?'en':'ko';
const tr=value=>value[language()];
const make=(name,cls,content)=>{const node=doc.createElement(name);if(cls)node.className=cls;if(content!==undefined)node.textContent=content;return node};
const button=(txt,attrs,cls='game-choice')=>{const node=make('button',cls,txt);node.type='button';for(const [name,value] of Object.entries(attrs))node.setAttribute(name,value);return node};
const same=(a,b)=>a.length===b.length&&a.every((v,i)=>v===b[i]);

function makeGame(root,kind){
 const rounds=kind==='ai'?ai:rf;
 let current=0,clues=[],parts=[],answer='',hintOpen=false,phase='ready',feedbackKey='none';
 const key=kind+'-game';
 const selectFocus=()=>{const el=doc.activeElement;if(!root.contains(el))return null;return ['data-clue','data-answer','data-part','data-action','data-heading'].map(n=>[n,el.getAttribute(n)]).find(v=>v[1]!==null)||null};
 const restoreFocus=old=>{if(!old)return;const el=root.querySelector('['+old[0]+'="'+old[1]+'"]');if(el&&!el.hidden)el.focus({preventScroll:true})};
 let ui;
 function render(focus=null){
  const c=rounds[current];
  root.classList.add('game');
  root.dataset.round=String(current+1);
  root.dataset.mode=c.mode||'evidence';
  root.dataset.state=phase;
  const top=make('div','game-top');
  const h=make('h3','game-title',tr(c.title));
  h.setAttribute('data-heading','true');h.tabIndex=-1;h.id=key+'-question';
  const progress=make('span','game-progress',tr(labels.progress)+' '+(current+1)+' / '+rounds.length);
  top.append(h,progress);
  const p=make('p','game-prompt',tr(c.prompt));p.id=key+'-prompt';
  root.setAttribute('role','group');root.setAttribute('aria-labelledby',h.id);root.setAttribute('aria-describedby',p.id);
  const flow=make('div','game-fields');
  const control=(entries,attr,label,tokens=false)=>{
   const field=make('fieldset','game-field');
   field.append(make('legend',null,tr(label)));
   const box=make('div','game-choices game-choices-'+attr);field.append(box);
   for(const {id,label:text} of entries){
    const el=button(undefined,{['data-'+attr]:id,'aria-pressed':'false'});
    if(tokens)el.append(make('span','game-token',id.toUpperCase()));
    el.append(make('span','game-choice-text',tr(text)));
    box.append(el);
   }
   flow.append(field);
  };
  let slots=null;
  if(kind==='ai'){
   control(c.clues,'clue',labels.clues,true);
   control(c.answers,'answer',labels.answersAI);
  }else if(c.mode==='path'){
   const path=make('div','game-path');
   path.append(make('p','game-path-start',tr(c.start)));
   slots=make('ol','game-slots');
   slots.setAttribute('aria-label',tr(labels.slots));
   for(let i=0;i<3;i++){const li=make('li','game-slot');li.dataset.slot=String(i+1);slots.append(li)}
   path.append(slots,make('p','game-path-end',tr(c.end)));flow.append(path);
   control(c.parts,'part',labels.parts);
  }else control(c.answers,'answer',labels.answersRF);

  const actions=make('div','game-actions');
  const action=(id,li)=>button(tr(li),{'data-action':id},'game-button'+(id==='check'?' game-primary':''));
  const check=action('check',labels.check),hint=action('hint',labels.hint),reset=action('reset',labels.reset),next=action('next',current===rounds.length-1?labels.replay:labels.next);
  hint.setAttribute('aria-controls',key+'-hint');
  actions.append(check,hint);
  if(slots)actions.append(action('undo',labels.undo));
  actions.append(reset,next);
  const tips=make('p','game-hint');tips.id=key+'-hint';tips.setAttribute('role','status');
  const feedback=make('p','game-feedback');feedback.setAttribute('role','status');feedback.setAttribute('aria-atomic','true');
  root.replaceChildren(top,p,flow,actions,tips,feedback);
  ui={slots,hint,next,tips,feedback};
  sync();
  restoreFocus(focus);
 }
 function sync(){
  const c=rounds[current],solved=phase==='correct';
  root.dataset.state=phase;
  for(const el of root.querySelectorAll('[data-clue],[data-answer],[data-part]')){
   const chosen=el.hasAttribute('data-clue')?clues.includes(el.dataset.clue):el.hasAttribute('data-answer')?answer===el.dataset.answer:parts.includes(el.dataset.part);
   el.setAttribute('aria-pressed',String(chosen));
   if(solved)el.setAttribute('aria-disabled','true');else el.removeAttribute('aria-disabled');
  }
  if(ui.slots){
   Array.from(ui.slots.children).forEach((el,i)=>{
    const part=c.parts.find(obj=>obj.id===parts[i]);el.dataset.filled=String(Boolean(part));
    el.replaceChildren(make('span','game-slot-number',String(i+1)),make('span','game-slot-label',part?tr(part.label):tr(labels.slot)));
   });
   const undo=root.querySelector('[data-action="undo"]');
   undo.setAttribute('aria-disabled',String(solved||!parts.length));
  }
  ui.tips.hidden=!hintOpen;
  const tipText=hintOpen?tr(c.hint):'';
  if(ui.tips.textContent!==tipText)ui.tips.textContent=tipText;
  ui.hint.setAttribute('aria-expanded',String(hintOpen));
  ui.next.hidden=!solved;
  root.querySelector('[data-action="check"]').setAttribute('aria-disabled',String(solved));
  let response=solved?tr(labels.correct)+' '+tr(c.why):feedbackKey==='none'?'':tr(labels[feedbackKey]);
  if(!solved&&feedbackKey==='ready'){
   const ko=language()==='ko';
   if(kind==='ai'&&(clues.length!==2||!answer))response=ko?'근거 '+clues.length+'/2 · 결론 '+(answer?'선택함':'선택 전'):'Clues '+clues.length+'/2 · conclusion '+(answer?'selected':'not selected');
   if(c.mode==='path'&&parts.length<3)response=ko?'연결한 소자 '+parts.length+'/3':'Connected blocks: '+parts.length+'/3';
  }
  // Keep the live region in the document and touch it only when its message changes.
  if(ui.feedback.textContent!==response)ui.feedback.textContent=response;
 }
 function fresh(fromNext){
  clues=[];parts=[];answer='';hintOpen=false;phase='ready';feedbackKey=fromNext?'none':'resetMessage';
 }
 function mark(key,status='ready'){feedbackKey=key;phase=status}
 root.addEventListener('click',event=>{
  const el=event.target.closest('button');if(!el||!root.contains(el))return;
  const c=rounds[current],action=el.dataset.action;
  if(action==='hint'){hintOpen=!hintOpen;sync();return}
  if(action==='reset'){fresh(false);sync();return}
  if(action==='next'&&phase==='correct'){
   current=(current+1)%rounds.length;fresh(true);render();
   root.querySelector('[data-heading]').focus();return;
  }
  if(phase==='correct')return;
  if(el.hasAttribute('data-clue')){
   const id=el.dataset.clue;
   if(clues.includes(id)){clues=clues.filter(v=>v!==id);mark('ready')}
   else if(clues.length<2){clues.push(id);mark('ready')}
   else mark('max');
  }else if(el.hasAttribute('data-answer')){
   answer=el.dataset.answer;mark('ready');
  }else if(el.hasAttribute('data-part')){
   const id=el.dataset.part;
   if(parts.includes(id))return;
   if(parts.length===3)mark('full');else{parts.push(id);mark('ready')}
  }else if(action==='undo'){
   if(parts.length){parts.pop();mark('ready')}
  }else if(action==='check'){
   if(kind==='ai'){
    if(clues.length!==2||!answer)mark('chooseAI');
    else if(!same(clues.slice().sort(),c.key))mark('wrongAI','wrong');
    else if(answer!==c.answer)mark('wrongConclusion','wrong');
    else mark('correct','correct');
   }else if(c.mode==='path'){
    if(parts.length!==3)mark('choosePath');
    else if(!same(parts,c.key))mark('wrongPath','wrong');
    else mark('correct','correct');
   }else{
    if(!answer)mark('chooseMatch');
    else if(answer!==c.answer)mark('wrongMatch','wrong');
    else mark('correct','correct');
   }
  }
  sync();
 });
 render();
 return ()=>render(selectFocus());
}

const games=Array.from(doc.querySelectorAll('[data-game]')).filter(el=>['ai','rf'].includes(el.dataset.game)).map(el=>makeGame(el,el.dataset.game));
if(!games.length)return;
function openLinkedGame(){
 const id=location.hash.slice(1);
 if(id!=='puzzle-ai'&&id!=='puzzle-rf')return;
 const item=doc.getElementById(id);
 if(item&&item.tagName==='DETAILS')item.open=true;
}
openLinkedGame();
window.addEventListener('hashchange',openLinkedGame);
doc.addEventListener('click',event=>{
 // A hero link to the current hash still opens a panel the visitor closed.
 const anchor=event.target.closest('a[href="#puzzle-ai"],a[href="#puzzle-rf"]');
 if(!anchor)return;
 const item=doc.getElementById(anchor.hash.slice(1));
 if(item&&item.tagName==='DETAILS')item.open=true;
});
let lastLanguage=language();
function relabel(){
 const next=language();if(next===lastLanguage)return;
 lastLanguage=next;games.forEach(redraw=>redraw());
}
doc.addEventListener('neca:lang',relabel);
new MutationObserver(relabel).observe(doc.documentElement,{attributes:true,attributeFilter:['lang']});
})();
