"""Image-first English research gallery shared by Home and Research."""
from hashlib import sha256
from html import escape
from pathlib import Path
import xml.etree.ElementTree as ET

BASE = Path(__file__).resolve().parent
SVG_NS = 'http://www.w3.org/2000/svg'
ET.register_namespace('', SVG_NS)

CONTENT = {
    'radar': ('Radar & Physical AI', 'A later echo stands out on the time trace.',
              'A radar pulse reflects off the buried object. The delay between sending and receiving it helps locate the object.'),
    'rf-design': ('AI for RF Design', 'A candidate response approaches the target.',
                  'An AI design loop proposes coupler geometries and checks their frequency responses in simulation.'),
    'interconnects': ('3D Chip Interconnects', 'A smaller ripple appears on the neighboring via.',
                      'A signal step travels down one vertical chip interconnect and couples into an adjacent one.'),
    'plasma': ('RF for Fusion Plasmas', 'Wavefronts spread into the plasma edge.',
               'A waveguide feeds the launcher, which transfers RF power to the plasma.'),
    'grounded-ai': ('Evidence-Grounded AI', 'The same citation appears beside the answer.',
                    'The system selects a relevant source passage so a reader can verify what supports the answer.'),
}

def x(value):
    return escape(str(value), quote=True)

def overlay(src):
    tag = ET.parse(BASE/src).getroot()
    parts = []
    for node in tag.iter():
        if 'art-fx' in node.get('class', '').split():
            encoded = ET.tostring(node, encoding='unicode').replace(f' xmlns="{SVG_NS}"', '')
            parts.append(encoded)
    return '<svg class="vd-overlay" viewBox="'+x(tag.get('viewBox', '0 0 800 400'))+'" preserveAspectRatio="xMidYMin meet" aria-hidden="true" focusable="false">'+''.join(parts)+'</svg>'

def deck(fields, rich=False):
    key = 'fields' if rich else 'focus'
    track = 'visual-'+key+'-track'
    cards, panels, fallback = [], [], []
    for n, r in enumerate(fields):
        field = r['id']
        title, result, _ = CONTENT[field]
        copy = r['summary']
        panel = f'visual-{key}-{field}-detail'
        src = r['image']
        art_url = src + '?v=' + sha256((BASE/src).read_bytes()).hexdigest()[:9]
        cards.append(f'''<article class="vd-card" data-deck-card id="{x(field)}" data-field="{x(field)}"><button type="button" class="vd-card-button" data-vd-open aria-expanded="false" aria-controls="{x(panel)}" aria-label="{x(title)}: show explanation"><span class="vd-art"><img src="{x(art_url)}" alt="" width="800" height="400" decoding="async" {"fetchpriority='high'" if rich and n == 0 else "loading='lazy'"}>{overlay(src)}</span><span class="vd-heading">{x(title)}</span></button></article>''')
        example = r.get('example')
        link = ''
        if not rich:
            link = f'<a class="vd-reference" href="research.html#{x(field)}">Explore this research field</a>'
        elif example and example.get('href') and not example['href'].startswith(('/', 'javascript:')):
            name = 'Related publication' if example['href'].startswith('publications.html#') else 'Lab announcement'
            link = f'<a class="vd-reference" href="{x(example["href"])}">{name}</a>'
        fallback.append(f'<details class="vd-static"><summary>{x(title)}</summary><p>{x(copy)}</p>{link}</details>')
        panels.append(f'''<section class="vd-panel" id="{x(panel)}" data-vd-panel hidden tabindex="-1" aria-labelledby="{x(panel)}-title"><h3 id="{x(panel)}-title" data-vd-result>{x(result)}</h3><p>{x(copy)}</p>{link}<button type="button" class="vd-close" data-vd-close>Close explanation</button></section>''')
    return f'''<div class="visual-deck" data-deck data-visual-deck lang="en" role="region" aria-label="Research gallery"><div class="vd-controls" hidden><button type="button" data-deck-prev aria-controls="{track}" aria-label="Previous research field">Previous</button><span class="vd-index" data-deck-index aria-live="polite" aria-atomic="true"></span><button type="button" data-deck-next aria-controls="{track}" aria-label="Next research field">Next</button><button type="button" data-vd-motion aria-pressed="false">Pause motion</button></div><div class="vd-track" data-deck-track id="{track}" tabindex="0" aria-label="Research fields. Swipe or use the arrow keys to browse.">{''.join(cards)}</div>{''.join(panels)}<noscript>{''.join(fallback)}</noscript></div>'''
