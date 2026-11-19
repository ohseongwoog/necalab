from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
import urllib.parse,re, json, hashlib
P=Path(__file__).resolve().parent;pages=['index','research','people','publications','news','join']; d=json.loads((P/'data/catalog.json').read_text())
assert sorted([k for k in d])==sorted(['publications','research','news','people'])
assert sum(n['type']=='journal' for n in d['publications'])==23 and len([n for n in d['publications'] if n.get('international')])==9
assert len(d['people'])==7 and all((P/p['image']).is_file() for p in d['people'])
assert len({x['title'].casefold() for x in d['publications']})==32
assert hashlib.sha256((P/'assets/neca-logo.png').read_bytes()).hexdigest()=='407b8241e7e28f8a449700ae4a8138b619a564742a648ec43f31092598fc48e5'
class Parse(HTMLParser):
 def __init__(self):super().__init__();self.ids=set();self.links=[];self.robots=None;self.h1=0
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if 'id'in a:assert a['id'] not in self.ids,a['id'];self.ids.add(a['id'])
  if tag=='h1':self.h1+=1
  if tag=='meta'and a.get('name')=='robots':self.robots=a['content']
  if tag in ['img','script','a','link']:
   if a.get('src') or a.get('href'):self.links.append(a.get('src') or a.get('href'))
parsed={}
for page in pages:
 f=P/(page+'.html');a=Parse();a.feed(f.read_text());parsed[page]=a
 assert a.h1==1 and 'noindex' in a.robots
for page,a in parsed.items():
 for link in a.links:
  assert not link.startswith(('http:','javascript:','/','//')),link
  url=urlsplit(link)
  if url.scheme:continue
  if url.path: assert (P/url.path).is_file(),(page,link)
  if url.fragment:
   target=parsed[Path(url.path).stem] if url.path else a
   assert unquote(url.fragment) in target.ids,(page,link)
for p in d['publications']:
 if p['doi']:assert re.match(r'^10\.\d{4,9}/\S+$',p['doi'])
print('PASS six noindex pages, 32 distinct records, 7 portraits, logo provenance, '+str(sum(len(x.links) for x in parsed.values()))+' resource/anchor references.')


# Guards for the bilingual editorial pages; no third-party modules or network access.
from xml.etree import ElementTree as ET
from build import home, research_page, recent_outputs
fields=d['research']
assert len(fields)==len({r['id'] for r in fields})==5
for r in fields:
 assert r['image'].startswith('assets/field-') and r['image'].endswith('.svg')
 root=ET.parse(P/r['image']).getroot()
 assert root.tag=='{http://www.w3.org/2000/svg}svg' and root.attrib.get('viewBox')=='0 0 560 280'
 assert not root.findall('.//{http://www.w3.org/2000/svg}image') and not root.findall('.//{http://www.w3.org/2000/svg}script')
 for k in ['summary','summaryKo']:
  assert 0<len(re.findall(r'[.!?](?:\s|$)',r[k]))<=2,r['id']
 for k in ['short','shortKo','caption','captionKo','alt','altKo']:assert r[k].strip(),r['id']
h=home(); order=['class="hero"','id="lab-news"','id="research-areas"','id="recent-outputs"'];assert [h.index(m) for m in order]==sorted(h.index(m) for m in order)
j,c=recent_outputs(d['publications']);assert len(j)==len(c)==2
assert all(r['type']=='journal' and r['peerReviewed'] is True for r in j)
assert all(r['type']=='conference' and r['international'] is True and r['presentationDate'] for r in c)
assert recent_outputs([{'type':'news'},{'type':'journal','peerReviewed':False},{'type':'conference','international':True}])==([],[])
for r in j+c:assert f'publications.html#{r["id"]}' in h
for r in fields:
 assert f'research.html#{r["id"]}' in h and r['altKo'] in research_page()
print('PASS homepage section order, strict academic output selection, five bilingual areas and five original vector diagrams.')
