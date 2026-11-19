"""Two self-contained, one-gesture teaching models in the Home hero."""
from html import escape
from math import pi, sin

def pair(ko, en):
    return f'<span class="ko" lang="ko">{escape(ko)}</span><span class="en" lang="en">{escape(en)}</span>'

def svg(contents, box):
    return f'<svg viewBox="{box}" aria-hidden="true" focusable="false">{contents}</svg>'

def link_icon():
    path='<path class="first-state" d="m3.6 7.6 2.8 2.9 5.1-5.3"/><path class="second-state" d="m5 5 5 5m0-5-5 5"/>'
    return svg(f'<g fill="none" stroke="currentColor" stroke-width="1.65" stroke-linecap="round" stroke-linejoin="round">{path}</g>', '0 0 15 15')

def ai_plot():
    # The two rows are fixed conflicting observations, not editable user input.
    words = pair('“와이파이가 끊겨요”','“Wi-Fi drops”')
    pulse = svg('<path d="M1 8h3l2-5 2 10 2-6 2 1h2" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linejoin="round"/>','0 0 15 16')
    note = svg('<path d="M2 2.5h11v8H7.4l-3.3 2.8v-2.8H2zM4.7 5.1h5.6M4.7 7.5h3.8" fill="none" stroke="currentColor" stroke-width="1.2" stroke-linejoin="round"/>','0 0 15 16')
    network = svg('''<g fill="none" stroke-linecap="round">
<g data-net="text" stroke="#9ce4ff"><path d="M3 9h10C25 9 34 19 45 23M13 9c12 0 28-7 41 0M13 9c12 10 25 25 41 27"/></g>
<g data-net="sensor" stroke="#e6d691"><path d="M3 35h10c12 0 21-9 32-12M13 35c12-3 26-25 41-26M13 35c12 3 29 4 41 1"/></g>
<path d="M55 9c12 0 16 9 27 14M48 23h34M55 36c12 0 16-9 27-13m0 0h13" stroke="#a1bbd1" stroke-width="1.3"/></g>
<g fill="#0e3659" stroke="#cbe6f4" stroke-width="1.3"><circle cx="3.5" cy="9" r="2.7"/><circle cx="3.5" cy="35" r="2.7"/><circle cx="54" cy="9" r="3.1"/><circle cx="47" cy="23" r="3.5"/><circle cx="54" cy="36" r="3.1"/></g>
<path d="m92 20 4 3-4 3" fill="none" stroke="#cbe6f4" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round"/>''','0 0 100 44')
    return '<div class="micro-ai-plot"><div class="micro-inputs"><span>'+note+words+'</span><span>'+pulse+'82 °C</span></div><div class="micro-net">'+network+'</div><div class="micro-inference"><small>'+pair('AI 판단','Prediction')+'</small><span data-outcome>'+pair('연결 문제','Wi-Fi fault')+'</span></div></div>'

def rf_wave(distance):
    # Illustrative field amplitude decays between TX and RX; spatial scale is schematic.
    end=130+(distance-2)*7.2
    cycle=23
    def y(x):
        t=(x-68)/(end-68)
        return 23-(8.8*2/(2+(distance-2)*t))*sin(2*pi*(x-68)/cycle)*min(1,(x-68)/3,(end-x)/3)
    return 'M68 23 '+ ' '.join(f'L{x:.2f} {y(x):.2f}' for x in (68+(end-68)*i/112 for i in range(1,113)))

def rf_plot():
    # TX chip and feed, drawn RF waveform, and moving RX antenna in one coordinate system.
    layer=f'''<g fill="none" stroke-linejoin="round" stroke-linecap="round">
<g stroke="#a7c1cf" stroke-width="1.05"><path d="M6 17h4m-4 6h4m-4 6h4m3-19v5m6-5v5m6-5v5m-12 16v5m6-5v5m6-5v5m3-19h4m-4 12h4"/><rect x="10" y="15" width="18" height="16" rx="2.1"/><rect x="14" y="18.5" width="10" height="9" rx="1.2"/></g>
<g stroke="#d9e7b9" stroke-width="1.75"><path d="M29 23h8l3 8h10V16m0 0-7-10m7 10 7-10m-13 28h12"/></g>
<path d="M62 23h184" stroke="#8ba6b9" stroke-opacity=".33" stroke-dasharray="1.5 3.5"/>
<path data-wave d="{rf_wave(7.6)}" stroke="#a8ebd4" stroke-width="2.05"/>
<g data-receiver transform="translate(170.32,0)" stroke="#d5e8f0" stroke-width="1.75"><path d="M9 33V15m0 0-7-9m7 9 7-9M4 35h10m-7 3h4"/><path d="M15 23h8" stroke-width="1.05"/></g>
</g><g fill="#bfced9" font-family="ui-monospace,monospace" font-size="8" letter-spacing=".6"><text x="11" y="43">TX</text><text data-rx-label x="186" y="44">RX</text></g>'''
    return '<div class="micro-rf-plot">'+svg(layer,'0 0 250 46')+'</div>'

def one(g):
    ai = g == 'ai'
    title = pair('단서의 무게','Weigh the clues') if ai else pair('신호의 거리','Signal range')
    intro = pair('더 믿고 싶은 단서 쪽으로 밀어 보세요.','Slide toward the clue you trust more.') if ai else pair('안테나를 멀리 보내 연결 한계를 찾아보세요.','Move the antennas apart until the link drops.')
    lab = pair('교육용 모형','Toy model') if ai else pair('모의 무선 링크','Simulated link')
    low = pair('문장','Text') if ai else pair('가까이','Near')
    high = pair('센서','Sensor') if ai else pair('멀리','Far')
    label = pair('문장과 센서의 비중','Balance between text and sensor') if ai else pair('안테나 사이 거리','Distance between antennas')
    numbers = ('0','100','1','48') if ai else ('2','14','0.1','7.6')
    plot = ai_plot() if ai else rf_plot()
    status = '' if ai else '<span class="micro-link-state">'+link_icon()+'<span data-outcome role="status" aria-live="polite" aria-atomic="true">'+pair('연결됨','Connected')+'</span></span>'
    initial = pair('문장 52% · 센서 48%','52% text · 48% sensor') if ai else '7.6 m · −62.8 dBm'
    # Native, labelled range is kept disabled only for the no-script document.
    return f'''<article class="micro-card" id="lab-{g}" data-lab="{g}" data-state="{'connection' if ai else 'connected'}" aria-labelledby="lab-{g}-title"><span id="puzzle-{g}" class="micro-alias" aria-hidden="true"></span>
<div class="micro-head"><div class="micro-title"><span class="micro-tag">{g.upper()}</span><h2 id="lab-{g}-title">{title}</h2></div><span class="micro-kind">{lab}</span></div>
<p class="micro-help" id="lab-{g}-help">{intro}</p>
<div class="micro-display">{plot}{status}</div>
<label class="micro-sr" for="lab-{g}-range">{label}</label><input class="micro-range" id="lab-{g}-range" type="range" min="{numbers[0]}" max="{numbers[1]}" step="{numbers[2]}" value="{numbers[3]}" aria-describedby="lab-{g}-help" disabled>
<div class="micro-scale"><span>{low}</span><span data-meter>{initial}</span><span>{high}</span></div></article>'''

def hero_labs():
    return '<aside class="micro-labs" id="hands-on" aria-label="미니 실험 / Mini experiments">'+one('ai')+one('rf')+'<noscript><p class="micro-nojs">'+pair('슬라이더를 움직이려면 자바스크립트를 켜 주세요.','Enable JavaScript to move the sliders.')+'</p></noscript></aside>'
