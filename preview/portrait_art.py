"""Portrait editorial compositions of the original landscape research illustrations."""
from pathlib import Path
from html import escape
from hashlib import sha256
import xml.etree.ElementTree as ET

BASE = Path(__file__).resolve().parent
V = 'http://www.w3.org/2000/svg'
TAG = lambda n: n.tag.split('}')[-1]
ET.register_namespace('', V)

def flat(node):
    return ET.tostring(node, encoding='unicode').replace(f' xmlns="{V}"', '')

def g(transform, contents):
    return f'<g transform="{transform}">{contents}</g>'

def p(d, stroke, width=1.6, cls='', dash='', fill='none'):
    attributes = f' class="art-fx {cls}" pathLength="1"' if cls else ''
    if dash:
        attributes += f' stroke-dasharray="{dash}"'
    return (f'<path d="{d}" fill="{fill}" stroke="{stroke}" stroke-width="{width}"'
            f' stroke-linecap="round" stroke-linejoin="round"{attributes}/>')

def text(x, y, label, color='#d8edf3', size=15, anchor='start'):
    return f'<text x="{x}" y="{y}" fill="{color}" text-anchor="{anchor}" font-size="{size}" font-family="system-ui,sans-serif" font-weight="640">{escape(label)}</text>'

def rect(x,y,w,h,fill,stroke='none',rad=0):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rad}" fill="{fill}" stroke="{stroke}" stroke-width="1.3"/>'

def circle(x,y,r,fill,stroke='none'):
    return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fill}" stroke="{stroke}" stroke-width="1.35"/>'

def panel(y, v, h):
    return (rect(24,y,402,h,'#0d2838','#416878',9)+rect(31,y+7,388,h-14,'#071b2a','#244b5d',5)+
            p(''.join(f'M{x} {y+22}v{h-38}' for x in range(52,401,38))+
              ''.join(f'M43 {z}h363' for z in range(y+44,y+h-9,23)), '#244657', .8)+
            text(45,y+25,v)+text(405,y+h-14,'t','#9fbdcd',14,'end'))

def radar_plot():
    y=352
    tx='M53 440h37l8-5 8 6 7-15 7-28 7 66 7-47 8 30 6-12 7 5h53'
    rx='M229 440h19l9-4 8 6 7-15 8-11 6 43 8-33 8 20 7-9 8 3h81'
    return (panel(y,'A(t)',170)+text(403,379,'ECHO','#e0bd86',14,'end')+
            p('M51 395v91m0-46h345','#6b91a5',1)+
            p('M120 395v-14m0 7h160m0-7v20','#9bb6c4',1.15)+text(200,383,'Δt','#bbd6e1',13,'middle')+
            p(tx,'#77dfe3',2.5)+p(rx,'#e5bd82',2.5)+p(rx,'#fff1aa',3.4,'draw-end radar-read','1')+
            text(55,497,'Tx','#83e3e2',14)+text(94,497,'Rx','#e5bf84',14))

def rf_plot():
    curves = (
        'M53 458C108 458 130 452 150 428S192 399 216 405 255 427 278 449 330 458 399 458',
        'M53 458C104 458 135 450 158 417S201 381 230 389 263 416 284 447 337 458 399 458',
        'M53 458C107 458 142 451 161 414S207 369 234 382 267 412 288 444 339 458 399 458',
    )
    target='M53 455C105 455 140 449 162 411S209 367 236 380 272 413 289 442 339 455 399 455'
    tones=('#dbb888','#b8d4cb','#8ffbe6')
    return (panel(313,'|S|',206).replace('>t</text>','>f</text>')+
            p('M52 351v128h352','#7296a9',1.05)+p(target,'#f1d698',1.8,dash='5 5')+
            ''.join(p(curve,tone,1.5) for curve,tone in zip(curves,('#54737d','#719789','#7dbcae')))+
            ''.join(p(curve,tone,3,f'draw-{stage} rf-candidate-{i}','1')
                    for i,(curve,tone,stage) in enumerate(zip(curves,tones,('first','middle','end')),1))+
            p('M60 491h21','#f1d698',1.8,dash='4 4')+text(88,496,'Target','#dfcb9a',13)+
            p('M160 491h21','#8fd7bf',2.3)+text(188,496,'Candidate','#a2d5c6',13))

def chip_plot():
    a='M54 425H108Q122 425 133 412L155 386Q163 377 176 377H396'
    b='M54 463H110Q123 463 135 450T157 438Q165 438 178 449T207 463H396'
    return (panel(327,'V(t)',192)+
            p('M52 365v117h348M152 363v111','#6d93a7',1)+
            p(a,'#e3b884',2.6)+p(b,'#70caca',2.4)+
            p(a,'#ffdf98',3.4,'draw-middle chip-drive','1')+p(b,'#a1fff4',3.3,'draw-end chip-couple','1')+
            text(58,499,'A','#f0bc84',14)+p('M77 494h27','#e3b884',2.4)+
            text(130,499,'B','#a4e7e4',14)+p('M149 494h27','#70caca',2.4))

def plasma_feed():
    feed='M379 402V365Q379 351 378 339L372 258 357 215 350 183'
    return (
        p('M350 167L361 159 382 208 394 255 397 340V404H361V340L358 265 346 218 337 190Z',
          '#adc5cd',1.4,fill='#214553')+
        p('M350 167L361 159 382 208 394 255 397 340V404L382 412 380 344 377 258 361 210 345 179Z',
          '#7d9dab',1.1,fill='#386174')+
        p('M352 180L368 217 383 256 387 341v63','#c4dce3',1.2)+
        p('M358 238l24-7m-17 36 23-4m-26 68 31-2m-31 24 31-2','#a0b8c2',1.3)+
        p('M338 184L350 198 365 193 356 178Z','#c4d6df',1,fill='#3a6775')+
        p(feed,'#d9b97d',2.5)+p(feed,'#ffe69c',5,'flow-first plasma-feed','.07 .93')+
        p('M313 341h34l21 18','#a0b9c5',1.35)+text(270,346,'P',size=18)+text(282,351,'RF',size=11)+
        rect(300,392,112,89,'#183b4f','#789aa7',7)+rect(310,402,92,49,'#081e2d','#335a6a',4)+
        text(356,434,'RF','#b4ebdf',25,'middle')+circle(317,465,3.5,'#85cf9e')+
        p('M332 460v9m8-9v9m8-9v9m8-9v9m8-9v9m8-9v9m8-9v9m8-9v9','#698d9c',1.25))

def ai_network():
    layers=[[(270,128),(268,171),(274,209)],[(317,121),(312,160),(317,203),(319,246)],[(371,139),(367,186),(371,232)]]
    net=''
    for left, right in zip(layers,layers[1:]):
        for x,y in left:
            for u,v in right:
                if abs(y-v)<75:
                    net+=p(f'M{x} {y}L{u} {v}','#4f8497',1.1)
    for layer in layers:
        for x,y in layer:
            net+=circle(x,y,5.5,'#183149','#7eb5c4')
    route='M242 173L268 171 312 160 367 186Q391 209 357 241L322 271 298 304'
    query='M350 95L345 107 317 121 312 160'
    return (rect(282,53,107,42,'#1b4353','#7ba4af',6)+
            circle(301,72,6,'none','#9bd0d7')+p('M306 77l6 6','#a9dbe2',1.4)+text(333,80,'Q','#c7e9ed',17)+net+
            p(query,'#8bbbc8',1.4)+p(query,'#9aebed',3.4,'flow-first ai-query','.07 .93')+
            p(route,'#9bad91',1.65)+p(route,'#cdeaa5',3.8,'flow-middle ai-route','.095 .905'))

def transform_nodes(tag, indexes, transform):
    nodes=list(tag)
    return g(transform,''.join(flat(nodes[i]) for i in indexes))

def field_content(svg, key):
    # Each source originally contains a contiguous landscape scene followed by its instrumentation.
    if key=='radar':
        return transform_nodes(svg,[*range(8,87),102,103],'translate(-3 4) scale(.90)')+radar_plot()
    if key=='rf-design':
        return transform_nodes(svg,range(8,170),'translate(-10 -37) scale(.94)')+p('M217 279v21','#527689',1.4,dash='2 6')+rf_plot()
    if key=='interconnects':
        return transform_nodes(svg,range(8,264),'translate(-24 -31) scale(1.015)')+chip_plot()
    if key=='plasma':
        return (transform_nodes(svg,[*range(8,46)],'translate(-52 41) scale(.86)')+
                g('translate(0 45)',plasma_feed())+
                transform_nodes(svg,range(63,71),'translate(-52 41) scale(.86)'))
    if key=='grounded-ai':
        return (transform_nodes(svg,[9,*range(11,50)],'translate(-22 7) scale(.90)')+ai_network()+
                transform_nodes(svg,range(82,98),'translate(-442 205) scale(1.14)'))
    raise ValueError(key)

def portrait(src, key):
    tree=ET.parse(BASE/src).getroot()
    bg=(
        '<defs><radialGradient id="portrait-glow" cx=".53" cy=".32" r=".76">'
        '<stop stop-color="#1b4456"/><stop offset=".69" stop-color="#0b2a3b"/><stop offset="1" stop-color="#071d2d"/>'
        '</radialGradient><pattern id="portrait-grid" width="25" height="25" patternUnits="userSpaceOnUse">'
        '<path d="M25 0H0V25" fill="none" stroke="#54798b" stroke-opacity=".21" stroke-width=".9"/>'
        '<circle cx="0" cy="0" r="1.35" fill="#83b0bc" opacity=".33"/></pattern></defs>'
        '<rect width="450" height="600" fill="url(#portrait-glow)"/><rect width="450" height="539" fill="url(#portrait-grid)"/>'
        '<path d="M14 35V15H36m378 0h22v20" fill="none" stroke="#7396a6" stroke-opacity=".6" stroke-width="1.4"/>'
    )
    title=next(n.text or '' for n in tree if TAG(n)=='title')
    desc=next(n.text or '' for n in tree if TAG(n)=='desc')
    originals=''.join(flat(n) for n in list(tree) if TAG(n)=='defs')
    content=field_content(tree,key)
    complete=(
        f'<svg xmlns="{V}" width="450" height="600" viewBox="0 0 450 600" role="img">'
        f'<title>{escape(title)}</title><desc>{escape(desc)}</desc>{originals}'
        f'<style>.art-fx{{opacity:0}}</style>{bg}{content}</svg>\n'
    )
    path=Path('assets')/f'portrait-{key}.svg'
    out=BASE/path
    data=complete.encode('utf-8')
    if not out.exists() or out.read_bytes()!=data:
        out.write_bytes(data)
    # Preserve all geometric ancestor transforms when lifting the active overlay paths.
    content_tree=ET.fromstring(f'<g xmlns="{V}">'+content+'</g>')
    def extract(node):
        if 'art-fx' in node.get('class','').split():
            return flat(node)
        keep=''.join(extract(child) for child in node)
        if not keep:
            return ''
        transform=node.get('transform')
        return g(transform,keep) if transform else keep
    extracted=extract(content_tree)
    overlay=(f'<svg class="vd-overlay" viewBox="0 0 450 600" preserveAspectRatio="xMidYMin meet" aria-hidden="true" focusable="false">{extracted}</svg>')
    return path.as_posix()+'?v='+sha256(data).hexdigest()[:9],overlay
