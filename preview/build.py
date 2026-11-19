"""Generate the six static NECA preview pages. Python standard library only."""
from pathlib import Path
from html import escape
from micro_labs import bottom_labs
from visual_deck import deck as visual_deck
import hashlib, json, re
P=Path(__file__).resolve().parent
def x(t): return escape(str(t or ''),quote=True)
def pair(ko,en): return '<span class="ko" lang="ko">'+x(ko)+'</span><span class="en" lang="en">'+x(en)+'</span>'
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
def asset(filename):
 path='assets/'+filename
 return path+'?v='+hashlib.sha256((P/path).read_bytes()).hexdigest()[:9]

def shell(pg,content,kt,et):
 title='NECA Lab. · '+kt+' / '+et
 extra=''
 if pg in ('index','research'):extra+='<link href="'+asset('visual-deck.css')+'" rel="stylesheet"><script defer src="'+asset('visual-deck.js')+'"></script>'
 if pg=='index':extra+='<link href="'+asset('home.css')+'" rel="stylesheet"><link href="'+asset('micro-labs.css')+'" rel="stylesheet"><script defer src="'+asset('micro-labs.js')+'"></script>'
 return f'''<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex,nofollow,noarchive"><meta name="referrer" content="strict-origin-when-cross-origin"><meta name="theme-color" content="#003987"><meta name="description" content="서울시립대학교 차세대 전자파 회로 및 응용 연구실 | NECA Lab., University of Seoul."><title>{x(title)}</title><link href="assets/site.css?v=3" rel="stylesheet"><script defer src="assets/site.js?v=3"></script>{extra}</head>
<body data-page="{pg}"><a class="skip" href="#main">{pair('본문 바로가기','Skip to content')}</a><header><div class="top"><div class="wrap"><span>{pair('서울시립대학교 · 전자전기컴퓨터공학부','University of Seoul · School of Electrical and Computer Engineering')}</span><span class="preview"><i></i>{pair('디자인 시안','Design preview')}</span></div></div><div class="bar wrap"><a class="brand" href="index.html" aria-label="NECA Lab. Home">{brand()}</a><nav id="navigation" aria-label="메인 메뉴 / Main menu">{nav(pg)}</nav><div class="nav-controls"><button type="button" id="language" hidden><span class="ko" lang="en">EN</span><span class="en" lang="ko">한국어</span></button><button type="button" class="hamb" id="menu-trigger" aria-expanded="false" aria-controls="navigation" aria-label="메뉴 / Menu" hidden><span></span><span></span></button></div></div></header><main id="main">{content}</main><footer><div class="foot-main wrap"><div><div class="foot-logo">NECA <span>Lab.</span></div><p>{pair('차세대 전자파 회로 및 응용 연구실','Next-gen. Electromagnetic Circuits and Application Lab.')}<br>{pair('서울시립대학교 전자전기컴퓨터공학부','School of Electrical and Computer Engineering, University of Seoul')}</p></div><div class="footer-links"><a href="mailto:{piemail}">{piemail}</a><a href="{legacy}/home">{pair('현행 연구실 홈페이지','Current lab website')}</a><a href="https://www.uos.ac.kr/">{pair('서울시립대학교','University of Seoul')}</a></div></div><div class="foot-base wrap"><span>NECA Lab. · University of Seoul</span><span>{pair('검토용 디자인 시안','Website design preview')}</span></div></footer></body></html>'''
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
def home_outputs():
 journals,talks=recent_outputs(pubs)
 def column(rows,ko,en):
  return '<div class="output-group"><h3>'+pair(ko,en)+'</h3><ul>'+''.join('<li data-kind="'+x(r['type'])+'"><span class="output-meta"><i lang="en">'+x(r['venue'])+'</i> · '+x(r['year'])+'</span><h4 lang="en"><a href="publications.html#'+x(r['id'])+'">'+x(r['title'])+'</a></h4></li>' for r in rows)+'</ul></div>'
 return '<section class="tint" id="recent-outputs"><div class="wrap section">'+sect('PUBLICATIONS','최근 연구 성과','Recent research outputs','publications.html','성과 전체 보기','All publications')+'<div class="output-grid">'+column(journals,'저널 논문','Peer-reviewed journals')+column(talks,'국제학회 발표','International conference presentations')+'</div></div></section>'
def home():
 h='<section class="hero"><div class="hero-inner wrap"><div class="hero-copy">'+tag('UNIVERSITY OF SEOUL')+'<h1 class="hero-wordmark" lang="en" aria-label="NECA Lab."><span class="word">NECA</span><span class="lab"> Lab<span class="term">.</span></span></h1><p class="hero-fullname">'+pair('차세대 전자파 회로 및 응용 연구실','Next-generation Electromagnetic Circuits and Applications Lab')+'</p><p class="hero-story">'+pair('전파로 땅속을 살피고, AI로 고주파 회로를 설계하고, 적층한 칩 사이를 지나는 신호를 측정합니다.','We use radar to see below ground, AI to design radio-frequency circuits, and measurements to trace signals between stacked chips.')+'</p><a class="hero-research-link" href="research.html">'+pair('연구 분야 전체 보기','Explore all research')+' <b aria-hidden="true">↗</b></a></div><div class="hero-gallery" id="research-areas" lang="en">'+visual_deck(research)+'</div></div></section>'
 h+=home_news()+home_outputs()
 h+='<section class="section wrap"><div class="team-strip"><div>'+tag('PEOPLE')+'<h2>'+pair('연구실 구성원','Meet the team')+'</h2></div><div><p>'+pair('전자파와 회로를 함께 연구하는 사람들을 소개합니다.','Meet the people studying electromagnetic waves and circuits together.')+'</p>'+txtlink('people.html','구성원 소개','Browse people')+'</div></div></section>'
 return h+bottom_labs()
def concept():
 orig=(img(logo,'NECA Lab. original mark','logo-example')+'<span>'+pair('기존 로고','Original mark')+'</span>') if logo else ''
 return '<details class="concept"><summary>'+pair('연구실 로고 디자인 제안','Lab identity design study')+'</summary><div class="concept-grid">'+('<div class="mark-tile">'+orig+'</div>' if orig else '')+'<div class="mark-tile">'+img('assets/em-ai-study.svg','Proposed symbol: perpendicular fields and a circuit trace','logo-example')+'<span>'+pair('EM × AI · 제안안','EM × AI · concept only')+'</span></div><p>'+pair('전기장과 자기장의 직교 관계를 두 축으로, 전파 방향을 따라 이어지는 점을 회로·AI 연결선으로 표현했습니다. 기존 로고를 대체하지 않습니다.','Two axes represent orthogonal electric and magnetic fields. A line of circuit nodes suggests propagation and AI connections. This is a separate concept, not a replacement for the original.')+'</p></div></details>'
def research_page():
 h='<section class="intro" lang="en"><div class="wrap">'+tag('NECA LAB. / RESEARCH')+'<h1>Research</h1></div></section>'
 return h+'<div class="wrap section areas">'+visual_deck(research, rich=True)+concept()+'</div>'
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

