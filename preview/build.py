"""Generate the six static NECA preview pages. Python standard library only."""
from pathlib import Path
from html import escape
import json, re, math
P=Path(__file__).resolve().parent
def x(t): return escape(str(t or ''),quote=True)
def pair(ko,en): return '<span class="ko" lang="ko">'+x(ko)+'</span><span class="en" lang="en">'+x(en)+'</span>'
def diagram(r):return '<img src="'+x(r['image'])+'" loading="lazy" decoding="async" width="560" height="280" alt="'+x(r['altKo'])+'" data-alt-ko="'+x(r['altKo'])+'" data-alt-en="'+x(r['alt'])+'">'
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
 return f'''<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex,nofollow,noarchive"><meta name="referrer" content="strict-origin-when-cross-origin"><meta name="theme-color" content="#003987"><meta name="description" content="서울시립대학교 차세대 전자파 회로 및 응용 연구실 | NECA Lab., University of Seoul."><title>{x(title)}</title><link href="assets/site.css?v=2" rel="stylesheet"><script defer src="assets/site.js?v=2"></script></head>
<body data-page="{pg}"><a class="skip" href="#main">{pair('본문 바로가기','Skip to content')}</a><header><div class="top"><div class="wrap"><span>{pair('서울시립대학교 · 전자전기컴퓨터공학부','University of Seoul · School of Electrical and Computer Engineering')}</span><span class="preview"><i></i>{pair('디자인 시안','Design preview')}</span></div></div><div class="bar wrap"><a class="brand" href="index.html" aria-label="NECA Lab. Home">{brand()}</a><nav id="navigation" aria-label="메인 메뉴 / Main menu">{nav(pg)}</nav><div class="nav-controls"><button type="button" id="language" hidden><span class="ko" lang="en">EN</span><span class="en" lang="ko">한국어</span></button><button type="button" class="hamb" id="menu-trigger" aria-expanded="false" aria-controls="navigation" aria-label="메뉴 / Menu" hidden><span></span><span></span></button></div></div></header><main id="main">{content}</main><footer><div class="foot-main wrap"><div><div class="foot-logo">NECA <span>Lab.</span></div><p>{pair('차세대 전자파 회로 및 응용 연구실','Next-gen. Electromagnetic Circuits and Application Lab.')}<br>{pair('서울시립대학교 전자전기컴퓨터공학부','School of Electrical and Computer Engineering, University of Seoul')}</p></div><div class="footer-links"><a href="mailto:{piemail}">{piemail}</a><a href="{legacy}/home">{pair('현행 연구실 홈페이지','Current lab website')}</a><a href="https://www.uos.ac.kr/">{pair('서울시립대학교','University of Seoul')}</a></div></div><div class="foot-base wrap"><span>NECA Lab. · University of Seoul</span><span>{pair('검토용 디자인 시안','Website design preview')}</span></div></footer></body></html>'''
def num(x):return f'{x:.2f}'
def plot(deg):
 # The illustration computes the normalized principal-plane cut of an ideal uniform 8x8 planar aperture.  At phi=0 the second array-factor term equals 1.
 R=153; ox,oy=265,195; th0=math.radians(deg)
 def af(t):
  u=math.pi*(math.sin(t)-math.sin(th0))/2
  return abs(math.sin(8*u)/(8*math.sin(u))) if abs(math.sin(u))>1e-9 else 1
 def point(t,r):return (ox+r*math.sin(t),oy-r*math.cos(t))
 def path(points):return ' '.join(('M' if i==0 else 'L')+num(u)+' '+num(v) for i,(u,v) in enumerate(points))
 grid=''
 for rad in [R/3,2*R/3,R]:
  pts=[point(math.radians(a),rad) for a in range(-90,91,2)]
  grid+=f'<path d="{path(pts)}" class="polar-grid"/>'
 for a in range(-90,91,15):
  xx,yy=point(math.radians(a),R+5); grid+=f'<path d="M {ox} {oy} L {num(xx)} {num(yy)}" class="polar-grid"/>'
 for ang,txt,dx,dy in [(-60,'−60°',-20,2),(0,'0°',0,-1),(60,'+60°',19,2)]:
  xx,yy=point(math.radians(ang),R+12);grid+=f'<text class="axis-label" x="{num(xx+dx)}" y="{num(yy+dy)}" text-anchor="middle">{txt}</text>'
 pts=[point(math.radians(a/4),R*af(math.radians(a/4))) for a in range(-360,361)]
 spec=f'<path class="pattern-fill" d="M{ox} {oy} {path(pts).replace("M","L",1)} Z"/><path class="pattern-line" d="{path(pts)}"/>'
 xx,yy=point(th0,R); spec+=f'<circle cx="{num(xx)}" cy="{num(yy)}" r="4" fill="#e7fa9b"/>'
 # Show the planar patch aperture separately beneath the polar cut.
 aperture=''
 for row in range(8):
  for col in range(8):
   u=196+col*13+row*6.8;v=217+row*3.8-col*0.55
   aperture+=f'<path d="M{num(u)} {num(v)}l9.5 -.4 4.5 2.6 -9.5 .4z" fill="#6cade2" opacity="{num(.57+.34*(row%2==0))}"/>'
 return f'<g class="scan-pattern" data-scan="{deg}"'+('' if deg==0 else ' style="display:none"')+f'>{grid}{spec}{aperture}</g>'
def rig():
 groups=''.join(plot(d) for d in [-25,0,25])
 ctrls=''.join(f'<button class="angle" data-angle="{d}" aria-pressed="{str(d==0).lower()}" type="button">{s}</button>' for d,s in [(-25,'−25°'),(0,'0°'),(25,'+25°')])
 return '<figure class="rig"><div class="rig-head"><span>'+pair('빔 조향 실험','Beam steering study')+'</span><span class="mono">8 × 8&nbsp; / &nbsp;λ/2</span></div><svg class="polar" viewBox="0 0 530 264" aria-label="균일 배열의 정규화 주평면 배열인자 / Normalized principal-plane array factor" role="img">'+groups+'</svg><div class="rig-controls"><span>'+pair('조향각','Steering angle')+'</span><div class="angle-group">'+ctrls+'</div></div><figcaption>'+pair('균일 배열의 정규화 배열인자 · 계산 예시, 측정값 아님','Normalized array factor for a uniform array · calculated, not measured')+'</figcaption></figure>'
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
 h='<section class="wrap section focus-section" id="research-areas">'+sect('RESEARCH','연구 분야','Our research','research.html','연구 자세히 보기','Explore our research')+'<div class="focus-grid">'
 for r in research:
  h+='<a class="focus-card" href="research.html#'+x(r['id'])+'"><div class="focus-art">'+img(r['image'],'')+'</div><div class="focus-copy"><h3>'+r_name(r)+'</h3><p>'+pair(r['shortKo'],r['short'])+'</p></div></a>'
 return h+'</div></section>'
def home_outputs():
 journals,talks=recent_outputs(pubs)
 def column(rows,ko,en):
  return '<div class="output-group"><h3>'+pair(ko,en)+'</h3><ul>'+''.join('<li data-kind="'+x(r['type'])+'"><span class="output-meta"><i lang="en">'+x(r['venue'])+'</i> · '+x(r['year'])+'</span><h4 lang="en"><a href="publications.html#'+x(r['id'])+'">'+x(r['title'])+'</a></h4></li>' for r in rows)+'</ul></div>'
 return '<section class="tint" id="recent-outputs"><div class="wrap section">'+sect('PUBLICATIONS','최근 연구 성과','Recent research outputs','publications.html','성과 전체 보기','All publications')+'<div class="output-grid">'+column(journals,'저널 논문','Peer-reviewed journals')+column(talks,'국제학회 발표','International conference presentations')+'</div></div></section>'
def home():
 h='<section class="hero"><div class="hero-inner wrap"><div class="hero-copy">'+tag('NECA LAB.  /  UNIVERSITY OF SEOUL')+'<h1><span class="ko" lang="ko">차세대 전자파<br>회로 및 응용 연구실<span class="term">.</span></span><span class="en" lang="en">Electromagnetic<br>circuits and<br>applications<span class="term">.</span></span></h1><p>'+pair('전파로 땅속을 살피고, AI로 고주파 회로를 설계하고, 적층한 칩 사이를 지나는 신호를 측정합니다.','We use radar to see below ground, AI to design radio-frequency circuits, and measurements to trace signals between stacked chips.')+'</p><div class="actions">'+button('research.html','연구 분야 보기','Explore research','white')+button('join.html','연구실 합류 안내','Join the lab','transparent')+'</div></div>'+rig()+'</div></section>'
 h+=home_news()+home_areas()+home_outputs()
 return h+'<section class="section wrap"><div class="team-strip"><div>'+tag('PEOPLE')+'<h2>'+pair('연구실 구성원','Meet the team')+'</h2></div><div><p>'+pair('전자파와 회로를 함께 연구하는 사람들을 소개합니다.','Meet the people studying electromagnetic waves and circuits together.')+'</p>'+txtlink('people.html','구성원 소개','Browse people')+'</div></div></section>'
def concept():
 orig=(img(logo,'NECA Lab. original mark','logo-example')+'<span>'+pair('기존 로고','Original mark')+'</span>') if logo else ''
 return '<details class="concept"><summary>'+pair('연구실 로고 디자인 제안','Lab identity design study')+'</summary><div class="concept-grid">'+('<div class="mark-tile">'+orig+'</div>' if orig else '')+'<div class="mark-tile">'+img('assets/em-ai-study.svg','Proposed symbol: perpendicular fields and a circuit trace','logo-example')+'<span>'+pair('EM × AI · 제안안','EM × AI · concept only')+'</span></div><p>'+pair('전기장과 자기장의 직교 관계를 두 축으로, 전파 방향을 따라 이어지는 점을 회로·AI 연결선으로 표현했습니다. 기존 로고를 대체하지 않습니다.','Two axes represent orthogonal electric and magnetic fields. A line of circuit nodes suggests propagation and AI connections. This is a separate concept, not a replacement for the original.')+'</p></div></details>'
def research_page():
 h=pagehead('RESEARCH','연구 분야','Research','다섯 연구 분야에서 우리가 풀고 있는 문제를 소개합니다. 그림은 원리를 설명한 개념도이며 측정 결과가 아닙니다.','Explore the questions behind our five research fields. The diagrams illustrate principles, not measured results.')
 h+='<div class="wrap section areas"><div role="navigation" class="area-nav" aria-label="연구 분야 바로가기 / Research fields">'
 for r in research:h+='<a href="#'+x(r['id'])+'">'+r_name(r)+'</a>'
 h+='</div>'
 for r in research:
  h+='<article class="area pillar" id="'+x(r['id'])+'"><figure class="area-figure"><div class="area-image">'+diagram(r)+'</div><figcaption>'+pair(r['captionKo'],r['caption'])+'</figcaption></figure><div><h2>'+r_name(r)+'</h2><p>'+r_sum(r)+'</p>'
  if r.get('example'):
   ex=r['example'];h+='<div class="related"><span class="eyebrow">'+pair('공개 연구 사례','Explore an example')+'</span><a href="'+x(ex['href'])+'">'+pair(ex['labelKo'],ex['label'])+'</a></div>'
  h+='</div></article>'
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

