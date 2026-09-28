# 한 번 쓰고 끝난 조사 스크립트(2026-09-28 큰 카페 가입 유도 실측, 결과는 research/_dossier/dossier.json).
# 정기 회차가 부르는 도구가 아니라서 work/ 에서 oneoff/ 로 옮겼다(health.py '안 부르는 도구' 집계 제외).
"""빨리 큰 카페가 모르는 사람을 어떻게 가입시키는지 한 곳씩 뜯어본다(2026-09-28 사장님 "모르는 사람이 가입할 수 있게 로직을").
대문·공지·운영자 공개글 끝 문구·외부 링크·가입 화면(질문·안내). 가입 버튼은 누르지 않는다 — 보기만."""
import sys, os, json, re, time, html, urllib.request, collections
sys.stdout.reconfigure(encoding='utf-8')
from playwright.sync_api import sync_playwright
HERE=os.path.dirname(os.path.dirname(os.path.abspath(__file__))); OUT=os.path.join(HERE,'research','_dossier'); os.makedirs(OUT,exist_ok=True)
STATE=r'C:\Users\강영준\Documents\naver_profile\storage_state.json'
H={'User-Agent':'Mozilla/5.0','Referer':'https://cafe.naver.com/'}
def get(u): return json.load(urllib.request.urlopen(urllib.request.Request(u,headers=H),timeout=20))
def txt(h): return re.sub(r'\n{2,}','\n',html.unescape(re.sub(r'<[^>]+>','\n',h or ''))).strip()
KEY=re.compile(r'가입|멤버|구독|알림|등업|등급|출석|이벤트|오픈채팅|open\.kakao|유튜브|youtube|youtu\.be|블로그|인스타|텔레그램|t\.me|링크')
def articles(cid, pages=3):
    out=[]
    for pg in range(1,pages+1):
        try: out+=get(f'https://apis.naver.com/cafe-web/cafe2/ArticleListV2dot1.json?search.clubid={cid}&search.queryType=lastArticle&search.page={pg}&search.perPage=20')['message']['result']['articleList']
        except Exception: break
        time.sleep(0.3)
    return out
def body(cid, aid):
    try: a=get(f'https://apis.naver.com/cafe-web/cafe-articleapi/v2.1/cafes/{cid}/articles/{aid}?useCafeId=true')['result']['article']; return a.get('contentHtml','')
    except Exception: return None
def dossier(c, ctx_guest, ctx_login):
    cid, club = c['cafeId'], c['cluburl']; d={'club':club,'name':c['name'],'members':c.get('memberCount'),'perday':c.get('perday')}
    L=articles(cid); d['n']=len(L)
    d['open_ratio']=round(sum(1 for a in L if a.get('openArticle'))/max(1,len(L)),2)
    mgr=collections.Counter(a.get('writerNickname') for a in L).most_common(1)
    d['top_writer']=mgr[0] if mgr else None
    d['menus']=collections.Counter(html.unescape(a.get('menuName','')) for a in L).most_common(8)
    d['avg_comments']=round(sum(a.get('commentCount',0) for a in L)/max(1,len(L)),1)
    # 공지·운영자 공개글
    notes, ctas, links = [], [], collections.Counter()
    for a in [a for a in L if a.get('openArticle')][:25]:
        h=body(cid,a['articleId']); time.sleep(0.3)
        if h is None: continue
        for u in re.findall(r'href="(https?://[^"]+)"',h):
            host=re.sub(r'^https?://(www\.|m\.)?','',u).split('/')[0]
            if 'naver.com' in host and 'blog' not in host: continue
            links[host]+=1
        t=txt(h); tail=t[-400:]
        isnote='공지' in (a.get('menuName') or '') 
        if isnote and len(notes)<3: notes.append({'title':html.unescape(a['subject']),'text':t[:1500]})
        hits=[ln for ln in tail.splitlines() if KEY.search(ln)]
        if hits and a.get('writerNickname')==(mgr[0][0] if mgr else None): ctas.append({'title':html.unescape(a['subject'])[:40],'tail':hits[-3:]})
    d['notices']=notes; d['cta_manager']=ctas[:6]; d['ext_links']=links.most_common(8)
    # PC 대문
    pg=ctx_guest.new_page()
    try:
        pg.goto(f'https://cafe.naver.com/{club}',wait_until='domcontentloaded',timeout=40000); pg.wait_for_timeout(5000)
        fr=pg.frame(name='cafe_main'); t=fr.inner_text('body') if fr else ''
        i=t.find('카페 대문'); d['gate']=t[i:i+900] if i>=0 else t[:600]
        d['side']=pg.inner_text('body')[:900]
    except Exception as e: d['gate_err']=str(e)[:80]
    pg.close()
    # 가입 화면(로그인·비멤버) — 보기만
    pg=ctx_login.new_page()
    try:
        pg.goto(f'https://m.cafe.naver.com/ca-fe/web/cafes/{cid}/join',wait_until='domcontentloaded',timeout=40000); pg.wait_for_timeout(5000)
        d['join']=pg.inner_text('body')[:1500]; pg.screenshot(path=os.path.join(OUT,f'{club}_join.png'),full_page=True)
    except Exception as e: d['join_err']=str(e)[:80]
    pg.close()
    return d
if __name__=='__main__':
    T=json.load(open(os.path.join(OUT,'targets.json'),encoding='utf-8'))
    res=[]
    with sync_playwright() as p:
        b=p.chromium.launch(headless=True)
        g=b.new_context(viewport={'width':1400,'height':1100},locale='ko-KR')
        l=b.new_context(**p.devices['iPhone 13'],locale='ko-KR',storage_state=STATE)
        for c in T:
            try: res.append(dossier(c,g,l)); print(c['cluburl'],'완료',flush=True)
            except Exception as e: print(c['cluburl'],'실패',e,flush=True)
            json.dump(res,open(os.path.join(OUT,'dossier.json'),'w',encoding='utf-8'),ensure_ascii=False,indent=1)
        b.close()
