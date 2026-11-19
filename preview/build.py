"""Generate the six static NECA preview pages. Python standard library only."""
from pathlib import Path
from html import escape
import hashlib, json, re
from xml.etree import ElementTree as ET
ET.register_namespace("", "http://www.w3.org/2000/svg")
P=Path(__file__).resolve().parent
def x(t): return escape(str(t or ''),quote=True)
def pair(ko,en): return '<span class="ko" lang="ko">'+x(ko)+'</span><span class="en" lang="en">'+x(en)+'</span>'
def diagram(r):return '<img src="'+x(r['image'])+'?v='+hashlib.sha256((P/r['image']).read_bytes()).hexdigest()[:9]+'" loading="lazy" decoding="async" width="800" height="400" alt="'+x(r['altKo'])+'" data-alt-ko="'+x(r['altKo'])+'" data-alt-en="'+x(r['alt'])+'">'
def tag(t):return '<span class="eyebrow">'+x(t)+'</span>'
def img(src,description='',cls='',lazy=True):return '<img class="'+x(cls)+'" src="'+x(src)+'" alt="'+x(description)+'" decoding="async" '+('loading="lazy"' if lazy else 'fetchpriority="high"')+'>'
def button(href,ko,en,cls=''):return '<a class="btn '+x(cls)+'" href="'+x(href)+'">'+pair(ko,en)+'</a>'
def txtlink(href,ko,en):return '<a class="text-link" href="'+x(href)+'">'+pair(ko,en)+'</a>'
def transl(obj,key,default=''):return obj.get(key+'Ko') or obj.get(key+'_ko') or default
D=json.loads((P/'data/catalog.json').read_text())
pubs=D['publications']; people=D['people']; research=D['research']; news=D['news']
legacy='https://sites.google.com/view/necalab'
piemail='ohseongwoog@uos.ac.kr'
def render_name(s):return '<strong><u>'+x(s)+'</u></strong>' if re.fullmatch(r'(Seongwoog Oh|Oh S\.?|S\.? Oh|Oh,? S\.?)',s,re.I) else x(s)
def plink(a):return a.get('url') or (('https://doi.org/'+a['doi']) if a.get('doi') else '')
def paper(a,compact=False):
 kind=a['type'];url=plink(a);au=', '.join(render_name(n) for n in a['authors']);title=x(a['title']);meta='<span class="kind">'+pair(('저널' if kind=='journal' else '국제학회'),('Journal' if kind=='journal' else 'International conference'))+'</span>'
 content=('<a href="'+x(url)+'">'+title+'</a>') if url else title
 venue='<i>'+x(a['venue'])+'</i>'
 detail=''
 if not compact:
  citation=str(a.get('citation') or '').strip().rstrip('.')
  v=a.get('venue') or ''
  tail=citation[len(v):].lstrip(' ,.;:') if citation.lower().startswith(v.lower()) else citation
  if tail: detail+='<p class="paper-extra" lang="en">'+x(tail)+'</p>'
  role=a.get('role') or a.get('authorRole')
  if role:detail+='<p class="paper-extra">'+x(role)+'</p>'
  if a.get('doi'):detail+='<a class="doi" href="https://doi.org/'+x(a['doi'])+'">DOI: '+x(a['doi'])+'</a>'
 return '<article class="paper'+(' compact' if compact else '')+'" id="'+('featured-' if compact else '')+x(a['id'])+'" data-kind="'+x(kind)+'" data-year="'+x(a['year'])+'"><div class="paper-tag">'+meta+'<span class="mono">'+x(a['year'])+'</span></div><div><h3 lang="en">'+content+'</h3><p class="venue">'+venue+'</p>'+('' if compact else '<p class="authors" lang="en">'+au+'</p>'+detail)+'</div></article>'
def pagehead(k,ko,en,ks,es):return '<section class="intro"><div class="wrap">'+tag(k)+'<h1>'+pair(ko,en)+'</h1><p>'+pair(ks,es)+'</p></div></section>'
def sect(k,ko,en,href=None,cko='',cen=''):return '<div class="sect-head"><div>'+tag(k)+'<h2>'+pair(ko,en)+'</h2></div>'+(txtlink(href,cko,cen) if href else '')+'</div>'
def label(k,en):return pair(k,en)
pages=[('index','홈','Home'),('research','연구','Research'),('people','구성원','People'),('publications','논문·학회','Publications'),('news','소식','News'),('join','합류 안내','Join')]
logo_files=[f for f in (P/'assets').glob('neca-logo.*') if f.suffix.lower() in ('.jpg','.jpeg','.png','.webp','.svg','.gif')]; logo='assets/'+logo_files[0].name if logo_files else ''
def brand():
 if logo: return img(logo,'NECA Lab.','brand-mark',False)+'<span class="brand-word">NECA <span>Lab.</span></span>'
 return '<span class="brand-word">NECA <span>Lab.</span></span>'
def nav(pg):return ''.join('<a href="'+name+'.html"'+(' aria-current="page"' if pg==name else '')+'>'+pair(ko,en)+'</a>' for name,ko,en in pages)
def shell(pg,content,kt,et):
 title='NECA Lab. · '+kt+' / '+et
 extra=('<link href="assets/interact.css?v=2" rel="stylesheet"><link href="assets/field-motion.css?v=1" rel="stylesheet"><script defer src="assets/deck.js?v=1"></script><script defer src="assets/field-motion.js?v=1"></script>' if pg in ('index','research') else '')+('<link href="assets/lab-ai.css?v=1" rel="stylesheet"><link href="assets/lab-rf.css?v=1" rel="stylesheet"><script defer src="assets/lab-ai.js?v=1"></script><script defer src="assets/lab-rf.js?v=1"></script>' if pg=='index' else '')
 return f'''<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex,nofollow,noarchive"><meta name="referrer" content="strict-origin-when-cross-origin"><meta name="theme-color" content="#003987"><meta name="description" content="서울시립대학교 차세대 전자파 회로 및 응용 연구실 | NECA Lab., University of Seoul."><title>{x(title)}</title><link href="assets/site.css?v=3" rel="stylesheet"><script defer src="assets/site.js?v=3"></script>{extra}</head>
<body data-page="{pg}"><a class="skip" href="#main">{pair('본문 바로가기','Skip to content')}</a><header><div class="top"><div class="wrap"><span>{pair('서울시립대학교 · 전자전기컴퓨터공학부','University of Seoul · School of Electrical and Computer Engineering')}</span><span class="preview"><i></i>{pair('디자인 시안','Design preview')}</span></div></div><div class="bar wrap"><a class="brand" href="index.html" aria-label="NECA Lab. Home">{brand()}</a><nav id="navigation" aria-label="메인 메뉴 / Main menu">{nav(pg)}</nav><div class="nav-controls"><button type="button" id="language" hidden><span class="ko" lang="en">EN</span><span class="en" lang="ko">한국어</span></button><button type="button" class="hamb" id="menu-trigger" aria-expanded="false" aria-controls="navigation" aria-label="메뉴 / Menu" hidden><span></span><span></span></button></div></div></header><main id="main">{content}</main><footer><div class="foot-main wrap"><div><div class="foot-logo">NECA <span>Lab.</span></div><p>{pair('차세대 전자파 회로 및 응용 연구실','Next-gen. Electromagnetic Circuits and Application Lab.')}<br>{pair('서울시립대학교 전자전기컴퓨터공학부','School of Electrical and Computer Engineering, University of Seoul')}</p></div><div class="footer-links"><a href="mailto:{piemail}">{piemail}</a><a href="{legacy}/home">{pair('현행 연구실 홈페이지','Current lab website')}</a><a href="https://www.uos.ac.kr/">{pair('서울시립대학교','University of Seoul')}</a></div></div><div class="foot-base wrap"><span>NECA Lab. · University of Seoul</span><span>{pair('검토용 디자인 시안','Website design preview')}</span></div></footer></body></html>'''
def activity_icon(g):
 if g=='ai':
  v='<g fill="none" stroke="#80b7c8" stroke-width="1.3"><path d="m10 15 23-7-1 17-22-10 22 28L10 34l22-9 23-10-23-7 24 29-24-12m0 18 24-6"/></g><g fill="#a8d7df" stroke="#d7f2ed"><circle cx="10" cy="15" r="3.3"/><circle cx="10" cy="34" r="3.3"/><circle cx="32" cy="8" r="3.4"/><circle cx="32" cy="25" r="4"/><circle cx="32" cy="43" r="3.4"/></g><g fill="#d4ed8e"><circle cx="56" cy="15" r="4"/><circle cx="56" cy="37" r="4"/></g>'
 else:
  v='<g fill="none" stroke="#a5d4db" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 29h8m0-8v17l14-9-14-8zm15 8h7l2-4 3 8 3-8 2 4h4v-9m0 2-6-9m6 9 6-9"/><path d="M54 18q7 6 0 12m4-15q10 9 0 18" stroke="#cfeaa0"/></g>'
 return '<svg class="activity-icon" viewBox="0 0 66 52" aria-hidden="true" focusable="false">'+v+'</svg>'
activities=[
 ('ai','AI 신경망 실험대','Neural network lab','문장과 표의 비중을 바꾸면 결과는?','What changes when text or table data gets more weight?','문장과 표를 편집하고 가중치와 층 수를 조절해 출력의 변화를 관찰하세요.','Edit text and table values, then change weights and depth to see the output shift.'),
 ('rf','RF 링크 실험대','Radio link lab','수신 안테나를 움직이면 신호는?','What happens when you move the receiving antenna?','회로를 조립하고 수신 안테나를 옮기거나 돌린 뒤 신호를 보내세요.','Assemble the circuit, move or rotate the receiving antenna, and transmit.')]
def gateway():
 h='<aside class="gateway" aria-label="가상 실험실 / Virtual labs"><div class="gateway-head"><span>'+pair('가상 실험실','Virtual labs')+'</span><small>'+pair('직접 조작','Hands-on')+'</small></div>'
 for g,ko,en,qk,qe,sk,se in activities:
  h+='<a class="gateway-link" href="#lab-'+g+'"><span class="gateway-icon">'+activity_icon(g)+'</span><span class="gateway-text"><strong>'+pair(ko,en)+'</strong><span>'+pair(qk,qe)+'</span></span><span class="gateway-play">'+pair('열기','Open')+'</span></a>'
 return h+'</aside>'
def bench():
 h='<section class="bench" id="hands-on"><div class="wrap section">'+sect('VIRTUAL LAB','직접 해보는 실험','Hands-on experiments')+'<div class="challenges">'
 for g,ko,en,qk,qe,sk,se in activities:
  h+='<details class="challenge" id="lab-'+g+'"><summary><span class="challenge-symbol">'+activity_icon(g)+'</span><span class="challenge-caption"><strong>'+pair(ko,en)+'</strong><span>'+pair(sk,se)+'</span></span><span class="challenge-open" aria-hidden="true"></span></summary><div data-lab="'+g+'"></div><noscript><p class="script-note">'+pair('실험을 조작하려면 브라우저의 자바스크립트를 켜 주세요.','Enable JavaScript in your browser to use the interactive controls.')+'</p></noscript></details>'
 return h+'</div></div></section>'
outcomes={
 'radar':('송신 펄스가 매설물에 닿은 뒤, 뒤늦게 도착한 반사파가 시간 기록에 나타납니다.','The pulse reaches the buried object; its returning echo appears later on the trace.'),
 'rf-design':('결합기에 신호를 흘려 여러 회로 후보의 주파수 응답을 목표 곡선과 비교합니다.','The coupler carries the signal; candidate responses are compared against the target curve.'),
 'interconnects':('A의 신호 변화가 수직 배선을 지나면 이웃 B에 더 작은 과도 응답이 나타납니다.','A step travels along A; coupling induces a smaller transient on B.'),
 'plasma':('전력이 도파관을 따라 안테나에 도달하고, 파면이 플라스마 가장자리로 진행합니다.','Power reaches the launcher through the waveguide. Wavefronts then enter the plasma edge.'),
 'grounded-ai':('선택한 근거 문장 S2를 검색 경로로 따라가면 같은 출처 표시가 답변에 붙습니다.','The selected passage follows the retrieval path and appears beside the answer with the same S2 citation.')}
def scene(r):
 key=r['id'];root=ET.parse(P/r['image']).getroot();parts=[]
 for el in root.iter():
  if 'art-fx' in el.get('class','').split():
   part=ET.tostring(el,encoding='unicode').replace(' xmlns="http://www.w3.org/2000/svg"','')
   parts.append(part)
 assert len(parts)>=3
 over='<svg class="field-fx-layer" viewBox="0 0 800 400" preserveAspectRatio="xMidYMid meet" aria-hidden="true" focusable="false">'+''.join(parts)+'</svg>'
 alt_id='diagram-text-'+key;btn='<button type="button" class="field-art" data-art-play="'+x(key)+'" data-art-state="idle" aria-describedby="'+alt_id+'" aria-label="'+x(r['titleKo']+' 원리 재생')+'" data-name-ko="'+x(r['titleKo'])+'" data-name-en="'+x(r['title'])+'">'+diagram(r)+over+'<span class="art-control" aria-hidden="true"><span class="art-icon"></span><span class="art-play-word">'+pair('원리 재생','Play diagram')+'</span><span class="art-again-word">'+pair('다시 재생','Replay')+'</span><span class="art-still-word">'+pair('최종 상태 보기','Show final state')+'</span></span></button>'
 return '<figure class="deck-figure field-figure">'+btn+'<figcaption id="'+alt_id+'" class="art-caption" aria-live="polite" aria-atomic="true"><span data-art-original>'+pair(r['captionKo'],r['caption'])+'</span><span data-art-outcome hidden>'+pair(*outcomes[key])+'</span></figcaption><button class="art-expand" type="button" data-art-expand="'+x(key)+'">'+pair('크게 보기','Enlarge diagram')+'</button></figure>'
def deck(rich=False):
 key='fields' if rich else 'focus';track=key+'-track'
 h='<div class="research-deck '+('deck-rich' if rich else 'deck-brief')+'" data-deck role="region" aria-label="연구 분야 카드"><div class="deck-bar"><p class="deck-help">'+pair('옆으로 넘겨 탐색하고, 그림을 눌러 원리를 보세요.','Swipe to browse. Select a diagram to see how it works.')+'</p><div class="deck-tools" hidden><button type="button" data-deck-prev aria-controls="'+track+'">'+pair('이전','Previous')+'</button><span data-deck-index class="deck-index" role="status" aria-live="polite" aria-atomic="true"></span><button type="button" data-deck-next aria-controls="'+track+'">'+pair('다음','Next')+'</button></div></div><div id="'+track+'" class="deck-track" data-deck-track tabindex="0" aria-label="연구 분야 목록">'
 for r in research:
  if rich:
   h+='<article class="deck-card pillar" data-deck-card id="'+x(r['id'])+'" tabindex="-1" aria-labelledby="title-'+x(r['id'])+'">'+scene(r)+'<div class="deck-copy"><h2 id="title-'+x(r['id'])+'">'+r_name(r)+'</h2><p>'+r_sum(r)+'</p>'
   if r.get('example'):
    ex=r['example'];h+='<div class="related"><span class="eyebrow">'+pair('공개 연구 사례','Explore an example')+'</span><a href="'+x(ex['href'])+'">'+pair(ex['labelKo'],ex['label'])+'</a></div>'
   h+='</div></article>'
  else:
   h+='<article class="deck-card" data-deck-card>'+scene(r)+'<a class="deck-brief-link" href="research.html#'+x(r['id'])+'"><div class="deck-copy"><h3>'+r_name(r)+'</h3><span class="deck-blurb">'+pair(r['shortKo'],r['short'])+'</span></div></a></article>'
 return h+'</div></div>'
def r_name(r):return pair(r['titleKo'],r['title'])
def r_sum(r):return pair(r['summaryKo'],r['summary'])
def n_name(z):return pair(z['titleKo'],z['title'])
def n_sum(z):return pair(z['summaryKo'],z['summary'])
def recent_outputs(records):
 """Keep journals with a confirmed review venue and presentations at international conferences in separate lists."""
 journals=[r for r in records if r.get('type')=='journal' and r.get('peerReviewed') is True]
 talks=[r for r in records if r.get('type')=='conference' and r.get('international') is True and r.get('presentationDate')]
 # Source lists are newest first within a year, including year-only journal citations.
 return sorted(journals,key=lambda r:-r['year'])[:2],sorted(talks,key=lambda r:-r['year'])[:2]
def home_news():
 lead,*others=news
 # Two more highlights from different categories; the complete announcements remain on the News page.
 highlights=[next((z for z in others if z.get('label')==category),None) for category in ('Research funding','Student award')]
 h='<section class="bulletin" id="lab-news"><div class="wrap section">'+sect('NEWS','연구실 소식','Lab news','news.html','소식 전체 보기','All lab news')+'<div class="bulletin-layout">'
 def news_entry(z,featured):
  k,e={'Industry collaboration':('산학협력','Industry collaboration'),'Research funding':('연구 선정','Research award'),'Student award':('학생 수상','Student award')}.get(z.get('label'),('연구실 소식','Lab news'))
  return '<article class="bulletin-item'+(' lead' if featured else '')+'"><span class="news-kicker">'+pair(k,e)+'</span><h3><a href="news.html#'+x(z['id'])+'">'+n_name(z)+'</a></h3>'+('<p>'+n_sum(z)+'</p>' if featured else '')+'</article>'
 h+=news_entry(lead,True)+'<div class="bulletin-more">'+''.join(news_entry(z,False) for z in highlights if z)+'</div></div></div></section>'
 return h
def home_areas():
 return '<section class="wrap section focus-section" id="research-areas">'+sect('RESEARCH','연구 분야','Our research','research.html','연구 자세히 보기','Explore our research')+deck()+'</section>'
def home_outputs():
 journals,talks=recent_outputs(pubs)
 def column(rows,ko,en):
  return '<div class="output-group"><h3>'+pair(ko,en)+'</h3><ul>'+''.join('<li data-kind="'+x(r['type'])+'"><span class="output-meta"><i lang="en">'+x(r['venue'])+'</i> · '+x(r['year'])+'</span><h4 lang="en"><a href="publications.html#'+x(r['id'])+'">'+x(r['title'])+'</a></h4></li>' for r in rows)+'</ul></div>'
 return '<section class="tint" id="recent-outputs"><div class="wrap section">'+sect('PUBLICATIONS','최근 연구 성과','Recent research outputs','publications.html','성과 전체 보기','All publications')+'<div class="output-grid">'+column(journals,'저널 논문','Peer-reviewed journals')+column(talks,'국제학회 발표','International conference presentations')+'</div></div></section>'
def home():
 h='<section class="hero"><div class="hero-inner wrap"><div class="hero-copy">'+tag('NECA LAB.  /  UNIVERSITY OF SEOUL')+'<h1><span class="ko" lang="ko">차세대 전자파<br>회로 및 응용 연구실<span class="term">.</span></span><span class="en" lang="en">Electromagnetic<br>circuits and<br>applications<span class="term">.</span></span></h1><p>'+pair('전파로 땅속을 살피고, AI로 고주파 회로를 설계하고, 적층한 칩 사이를 지나는 신호를 측정합니다.','We use radar to see below ground, AI to design radio-frequency circuits, and measurements to trace signals between stacked chips.')+'</p><div class="actions">'+button('research.html','연구 분야 보기','Explore research','white')+button('join.html','연구실 합류 안내','Join the lab','transparent')+'</div></div>'+gateway()+'</div></section>'
 h+=home_news()+bench()+home_areas()+home_outputs()
 return h+'<section class="section wrap"><div class="team-strip"><div>'+tag('PEOPLE')+'<h2>'+pair('연구실 구성원','Meet the team')+'</h2></div><div><p>'+pair('전자파와 회로를 함께 연구하는 사람들을 소개합니다.','Meet the people studying electromagnetic waves and circuits together.')+'</p>'+txtlink('people.html','구성원 소개','Browse people')+'</div></div></section>'
def concept():
 orig=(img(logo,'NECA Lab. original mark','logo-example')+'<span>'+pair('기존 로고','Original mark')+'</span>') if logo else ''
 return '<details class="concept"><summary>'+pair('연구실 로고 디자인 제안','Lab identity design study')+'</summary><div class="concept-grid">'+('<div class="mark-tile">'+orig+'</div>' if orig else '')+'<div class="mark-tile">'+img('assets/em-ai-study.svg','Proposed symbol: perpendicular fields and a circuit trace','logo-example')+'<span>'+pair('EM × AI · 제안안','EM × AI · concept only')+'</span></div><p>'+pair('전기장과 자기장의 직교 관계를 두 축으로, 전파 방향을 따라 이어지는 점을 회로·AI 연결선으로 표현했습니다. 기존 로고를 대체하지 않습니다.','Two axes represent orthogonal electric and magnetic fields. A line of circuit nodes suggests propagation and AI connections. This is a separate concept, not a replacement for the original.')+'</p></div></details>'
def research_page():
 h=pagehead('RESEARCH','연구 분야','Research','다섯 연구 분야에서 우리가 풀고 있는 문제를 소개합니다. 그림은 원리를 설명한 개념도이며 측정 결과가 아닙니다.','Explore the questions behind our five research fields. The diagrams illustrate principles, not measured results.')
 h+='<div class="wrap section areas"><details class="topic-index"><summary>'+pair('분야 바로가기','Jump to a field')+'</summary><div class="topic-links" role="navigation" aria-label="연구 분야 바로가기 / Research fields">'+''.join('<a href="#'+x(r['id'])+'">'+r_name(r)+'</a>' for r in research)+'</div></details>'+deck(True)
 return h+concept()+'</div>'
def people_page():
 h=pagehead('PEOPLE','구성원','People','연구책임자와 대학원 연구원들을 소개합니다.','Meet our principal investigator and graduate researchers.')
 a=people[0]; photo=img(a['image'],'Seongwoog Oh',lazy=False) if a.get('image') else '<span class="initials">SO</span>'
 h+='<section class="wrap section"><article class="pi"><div class="pi-pic">'+photo+'</div><div>'+tag('PRINCIPAL INVESTIGATOR')+'<h2>'+pair('오성욱','Seongwoog Oh')+'</h2><p class="person-en">'+pair('Seongwoog Oh','오성욱')+'</p><p>'+pair('서울시립대학교 전자전기컴퓨터공학부 조교수','Assistant Professor, School of Electrical and Computer Engineering, University of Seoul')+'</p><p class="contact-line"><a href="mailto:'+piemail+'">'+piemail+'</a><br>'+pair('정보기술관 511호','Information Technology Building, Room 511')+'</p>'+txtlink(legacy+'/professor','교수 프로필 원문','Full faculty profile')+'</div></article>'
 h+=sect('GRADUATE RESEARCHERS','대학원 연구원','Graduate researchers')+'<div class="people-grid">'
 focuses={'rf integrated circuits':'RF 집적회로','antenna':'안테나','antennas':'안테나','ai':'인공지능','artificial intelligence':'인공지능'}
 for a in people[1:]:
  ko=a.get('nameKo') or a['name'];en=a.get('nameEn') or a['name'];focus=a.get('focus') or ''
  mon=''.join(w[0] for w in (en if re.search('[a-zA-Z]',en) else ko).split()[:2]).upper() if re.search('[a-zA-Z]',en) else ko[-2:]
  pic=img(a['image'],ko) if a.get('image') else '<span class="initials">'+x(mon)+'</span>'
  h+='<article class="person"><div class="person-pic">'+pic+'</div><div><h3>'+pair(ko,en)+'</h3>'+('<p class="person-en">'+pair(en,ko)+'</p>' if ko!=en else '')+'<p class="focus">'+pair(a.get('focusKo') or focuses.get(focus.lower(),focus),a.get('focusEn') or focus)+'</p></div></article>'
 return h+'</div><p class="source-line">'+txtlink(legacy+'/members','현행 구성원 페이지','Current member directory')+'</p></section>'
def pubs_page():
 h=pagehead('PUBLICATIONS','논문과 국제학회','Publications','연구실의 저널 논문과 국제학회 발표를 연도·키워드로 찾아보세요.','Search the lab’s journal papers and international conference contributions by year or keyword.')
 h+='<section class="wrap section catalog"><div class="filter-box" data-js-only hidden><div class="filters" role="group" aria-label="자료 유형 / Publication type">'+''.join('<button data-type="'+t+'" aria-pressed="'+('true' if t=='all' else 'false')+'">'+pair(ko,en)+'</button>' for t,ko,en in [('all','전체','All'),('journal','저널','Journals'),('conference','국제학회','International conferences')])+'</div><div class="fields"><label>'+pair('키워드','Keyword')+'<input type="search" id="keywords" autocomplete="off" placeholder="제목·저자·학술지 / Title, author, venue"></label><label>'+pair('연도','Year')+'<select id="year"><option value="">'+x('전체 연도 / All years')+'</option>'+''.join('<option>'+x(y)+'</option>' for y in sorted({p['year'] for p in pubs},reverse=True))+'</select></label><button class="reset" id="reset-filters">'+pair('초기화','Reset')+'</button></div></div><p class="result" role="status" aria-live="polite" aria-atomic="true" id="result-count">'+pair(f'전체 {len(pubs)}건',f'{len(pubs)} publications')+'</p><p id="empty" hidden>'+pair('검색 결과가 없습니다. 검색어를 지우거나 연도를 바꿔보세요.','No matching publications. Clear the keyword or try another year.')+'</p><div class="papers" id="pub-list">'
 for y in sorted({p['year'] for p in pubs},reverse=True):
  h+='<section class="yeargroup" data-year="'+str(y)+'"><h2>'+str(y)+'</h2>'+''.join(paper(p) for p in pubs if p['year']==y)+'</section>'
 return h+'</div><p class="source-line">'+txtlink(legacy+'/Journal','현행 연구실 실적 페이지','Current lab publication list')+'</p></section>'
def news_page():
 h=pagehead('NEWS','연구실 소식','Lab news','연구실에서 공개한 연구 협력, 과제 선정, 교육 성과입니다.','Announcements from the lab about research collaborations, projects and student achievements.')
 h+='<div class="wrap section news-list">'
 for i,z in enumerate(news):
  h+='<article id="'+x(z['id'])+'">'+tag((z.get('label') or z.get('category') or 'LAB NEWS').upper())+'<h2>'+n_name(z)+'</h2><p>'+n_sum(z)+'</p></article>'
 return h+'<p class="source-line">'+txtlink(legacy+'/news','현행 연구실 소식','Current lab news page')+'</p></div>'
def join_page():
 h=pagehead('JOIN','연구실 합류 안내','Join the lab','학부연구생과 대학원 연구에 관심이 있다면 오성욱 교수에게 문의하세요.','Undergraduate and prospective graduate researchers are welcome to contact Prof. Seongwoog Oh.')
 return h+'<section class="section wrap join-layout"><div><div class="join-section">'+tag('UNDERGRADUATE RESEARCH')+'<h2>'+pair('학부연구생','Undergraduate research')+'</h2><p>'+pair('참여하고 싶은 연구 주제가 있다면 현재 전공과 관심 분야를 간단히 소개해 주세요.','If a research area interests you, introduce your academic background and the topic you would like to explore.')+'</p></div><div class="join-section">'+tag('GRADUATE RESEARCH')+'<h2>'+pair('대학원 과정','Graduate study')+'</h2><p>'+pair('관심 있는 문제와 함께 시작하고 싶은 시기를 알려주세요. 구체적인 참여 가능 여부와 일정은 연구실에 먼저 문의해 주세요.','Tell us about your research interests and when you hope to start. Contact the lab to discuss availability and timing.')+'</p>'+txtlink('research.html','연구 주제 살펴보기','Explore research topics')+'</div></div><aside class="contact-card">'+tag('CONTACT')+'<h2>'+pair('오성욱 교수','Prof. Seongwoog Oh')+'</h2><a class="email" href="mailto:'+piemail+'">'+piemail+'</a><dl><dt>'+pair('교수 연구실','Faculty office')+'</dt><dd>'+pair('서울시립대학교 정보기술관 511호','Information Technology Building, Room 511, University of Seoul')+'</dd><dt>'+pair('주소','Address')+'</dt><dd>'+pair('서울특별시 동대문구 서울시립대로 163','163 Seoulsiripdae-ro, Dongdaemun-gu, Seoul, Republic of Korea')+'</dd></dl>'+button('mailto:'+piemail,'이메일 작성','Compose email','white')+'</aside></section>'
if __name__=='__main__':
 content=[home(),research_page(),people_page(),pubs_page(),news_page(),join_page()]
 for (pg,ko,en),body in zip(pages,content):(P/(pg+'.html')).write_text(shell(pg,body,ko,en))

