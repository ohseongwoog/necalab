"""Two localized, directly manipulable teaching puzzles for the bottom of Home."""
from html import escape

def x(value):
    return escape(str(value), quote=True)

def pair(ko, en):
    return f'<span class="ko" lang="ko">{x(ko)}</span><span class="en" lang="en">{x(en)}</span>'

def knob(puzzle, key, ko, en, minimum, maximum, step, initial, low, high):
    id=f'lab-{puzzle}-{key}'
    return f'''<div class="puzzle-knob"><div class="puzzle-knob-line"><label for="{id}">{pair(ko,en)}</label><output data-knob-value="{key}" for="{id}" aria-hidden="true"></output></div><input id="{id}" data-knob="{key}" type="range" min="{minimum}" max="{maximum}" step="{step}" value="{initial}" aria-describedby="lab-{puzzle}-help" disabled><div class="puzzle-knob-scale"><span>{pair(*low)}</span><span data-knob-hint="{key}"></span><span>{pair(*high)}</span></div></div>'''

def track(key):
    return f'<div class="puzzle-track" aria-hidden="true" data-track="{key}"><span data-target="{key}"></span><i data-marker="{key}"></i></div>'

def ai_plot():
    nodes=[18,44,70]
    colors=['#7fe2db','#ffc788','#c3b2ff']
    paths=''.join(f'<path data-channel="{i}" data-main="{int(i==j)}" d="M36 {y}C104 {y} 183 {z} 246 {z}" stroke="{colors[i]}" stroke-linecap="round" fill="none"/>' for i,y in enumerate(nodes) for j,z in enumerate(nodes))
    ends=''.join(f'<g stroke="{colors[i]}" stroke-width="1.6" fill="#123149"><circle cx="26" cy="{y}" r="7"/><circle cx="256" cy="{y}" r="7"/><path d="M10 {y}h9m244 0h9"/></g>' for i,y in enumerate(nodes))
    return f'<svg class="puzzle-diagram puzzle-ai-plot" viewBox="0 0 282 88" aria-hidden="true">{paths}{ends}</svg>'

def rf_plot():
    return '''<svg class="puzzle-diagram puzzle-rf-plot" viewBox="0 0 420 88" aria-hidden="true"><g stroke="#a2c9df" stroke-width="1.55" fill="none" stroke-linecap="round" stroke-linejoin="round"><rect x="9" y="33" width="20" height="20" rx="3"/><path d="M12 29v4m7-4v4m7-4v4m-14 20v4m7-4v4m7-4v4m-21-21h4m-4 7h4m-4 7h4m20-7h23m0 0V24m0 5-9-9m9 9 9-9m-14 32h10"/></g><path d="M52 43H380" stroke="#47657b" stroke-dasharray="3 5"/><path data-wave fill="none" d="" stroke="#91f0c1" stroke-width="2.15" stroke-linejoin="round" stroke-linecap="round"/><g data-receiver transform="translate(365,0)"><path d="M0 66V44" stroke="#96c6dc" fill="none" stroke-width="1.7"/><g data-rf-axis><path d="M0 45V25m0 4-9-9m9 9 9-9" stroke="#b4e1f3" stroke-width="1.8" fill="none" stroke-linecap="round"/></g><circle data-rf-light cx="13" cy="59" r="3.7" fill="#b4e1f3"/><text x="-8" y="79" fill="#c6e4f4" font-size="10" font-family="monospace">RX</text></g><text x="45" y="72" fill="#c6e4f4" font-size="10" font-family="monospace">TX</text></svg>'''

def ai_results():
    outputs=[('text','연결 끊김','Wi-Fi fault'),('sensor','과열','Overheating'),('log','재부팅','Reboot fault')]
    return '<div class="puzzle-score-grid">'+''.join(f'''<div class="puzzle-score"><span>{pair(ko,en)}</span><strong data-score="{key}">—</strong>{track(key)}<span class="puzzle-target-label" data-band="{key}">—</span></div>''' for key,ko,en in outputs)+'</div>'

def ai():
    text=knob('ai','text','연결 끊김 문장 비중','Wi-Fi report weight',0,100,1,12,('낮게','Low'),('높게','High'))
    sensor=knob('ai','sensor','온도 센서 비중','Thermal sensor weight',0,100,1,12,('낮게','Low'),('높게','High'))
    log=knob('ai','log','재부팅 로그 비중','Reboot log weight',0,100,1,12,('낮게','Low'),('높게','High'))
    return f'''<article class="micro-card puzzle-card" data-lab="ai" id="lab-ai" aria-labelledby="lab-ai-title"><span id="puzzle-ai" class="micro-alias" aria-hidden="true"></span>
<header class="puzzle-card-head"><span class="puzzle-badge">AI</span><h3 id="lab-ai-title">{pair('세 가지 단서 맞추기','Balance three clues')}</h3></header>
<p class="puzzle-help" id="lab-ai-help">{pair('세 단서의 비중을 조절해 연결 끊김·과열·재부팅 점수를 각각 초록색 목표 구간에 넣어 보세요. 한 단서는 다른 진단에도 조금 영향을 줍니다.','Adjust the three clues until the Wi-Fi fault, overheating and reboot scores land in their green bands. Each clue also nudges the other two scores.')}</p>
<div class="puzzle-stage">{ai_plot()}{ai_results()}</div>
<p class="puzzle-outcome" data-outcome role="status" aria-live="polite" aria-atomic="true"></p><div class="puzzle-knobs">{text}{sensor}{log}</div>
<p class="puzzle-note">{pair('고정 가중치로 계산하는 교육용 모형입니다. 실제 AI 서비스에 연결되지 않습니다.','A fixed-weight teaching model. It does not connect to an AI service.')}</p></article>'''

def rf():
    distance=knob('rf','distance','안테나 거리','Antenna distance',2,14,.1,14,('가깝게','Near'),('멀리','Far'))
    angle=knob('rf','angle','편파 어긋남','Polarization mismatch',0,75,1,75,('정렬','Aligned'),('어긋남','Misaligned'))
    match=knob('rf','match','정합 전력 전달률','Matching efficiency',19,100,1,19,('반사 큼','More reflection'),('반사 없음','No reflection'))
    return f'''<article class="micro-card puzzle-card" data-lab="rf" id="lab-rf" aria-labelledby="lab-rf-title"><span id="puzzle-rf" class="micro-alias" aria-hidden="true"></span>
<header class="puzzle-card-head"><span class="puzzle-badge">RF</span><h3 id="lab-rf-title">{pair('수신 전력 맞추기','Tune the radio link')}</h3></header>
<p class="puzzle-help" id="lab-rf-help">{pair('거리·편파·정합을 바꿔 수신 전력을 초록색 목표 구간에 맞춰 보세요. 신호가 너무 강해도 목표를 벗어납니다.','Adjust distance, polarization and matching until the receive power lands in the green target band. A signal can also be too strong.')}</p>
<div class="puzzle-stage">{rf_plot()}<div class="puzzle-score puzzle-rf-score"><span>{pair('수신 전력','Receive power')}</span><strong data-score="power">—</strong>{track('power')}<span class="puzzle-target-label" data-band="power">—</span></div></div>
<p class="puzzle-outcome" data-outcome role="status" aria-live="polite" aria-atomic="true"></p><div class="puzzle-knobs">{distance}{angle}{match}</div>
<p class="puzzle-note">{pair('2.45 GHz 자유공간 모형입니다. 정합 전달률은 1 − |Γ|²이며 실제 전파를 송신하지 않습니다.','A 2.45 GHz free-space model. Matching efficiency is 1 − |Γ|². No radio waves are transmitted.')}</p></article>'''

def bottom_labs():
    return f'''<section class="micro-puzzles" id="hands-on" aria-labelledby="puzzles-title"><div class="wrap section"><header class="puzzles-heading"><p>PUZZLES</p><h2 id="puzzles-title">{pair('직접 풀어보는 퍼즐','Hands-on puzzles')}</h2></header><div class="puzzles-grid">{ai()}{rf()}</div><noscript><p>{pair('퍼즐을 풀려면 자바스크립트를 켜 주세요.','Enable JavaScript to play the puzzles.')}</p></noscript></div></section>'''
