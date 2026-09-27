# 한 번 쓰고 끝난 조사 스크립트(2026-09-27 카페 가입 화면 실측, 결과는 research/cafe-features.md 11절).
# 정기 회차가 부르는 도구가 아니라서 work/ 에서 oneoff/ 로 옮겼다(health.py '안 부르는 도구' 집계 제외).
"""다른 카페 글 본문에 가입 링크·가입 문구를 넣는지 센다(비로그인 공개글)."""
import sys, os, json, urllib.request, re, time, html
sys.stdout.reconfigure(encoding='utf-8')
OUT=os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),'research','_joinui')  # oneoff/ 한 칸 위 = work/
H={'User-Agent':'Mozilla/5.0','Referer':'https://cafe.naver.com/'}
def get(u): return json.load(urllib.request.urlopen(urllib.request.Request(u,headers=H),timeout=20))
res=[]
for c in json.load(open(os.path.join(OUT,'targets.json'),encoding='utf-8')):
    cid=c['cafeId']
    try: lst=get(f'https://apis.naver.com/cafe-web/cafe2/ArticleListV2dot1.json?search.clubid={cid}&search.queryType=lastArticle&search.page=1&search.perPage=20')['message']['result']['articleList']
    except Exception as e: print(c['cluburl'],'X',e); continue
    n=0; hits=[]
    for a in [a for a in lst if a.get('openArticle')][:12]:
        try: art=get(f'https://apis.naver.com/cafe-web/cafe-articleapi/v2.1/cafes/{cid}/articles/{a["articleId"]}?useCafeId=true')['result']
        except Exception: continue
        n+=1; h=art['article']['contentHtml']; txt=html.unescape(re.sub('<[^>]+>',' ',h))
        links=re.findall(r'href="([^"]*(?:join|Join)[^"]*)"',h)
        lines=[l.strip() for l in re.split(r'\s{2,}|\n',txt) if '가입' in l and len(l.strip())<120]
        wr=art['article']['writer'].get('memberLevelName','') if isinstance(art['article'].get('writer'),dict) else ''
        if links or lines: hits.append({'aid':a['articleId'],'menu':a.get('menuName'),'writer':a.get('writerNickname'),'links':links[:2],'lines':lines[:3]})
        time.sleep(0.3)
    res.append({'cluburl':c['cluburl'],'name':c['name'],'checked':n,'hits':hits})
    print(c['cluburl'],n,'편 중',len(hits),'편', flush=True)
json.dump(res,open(os.path.join(OUT,'joinbody.json'),'w',encoding='utf-8'),ensure_ascii=False,indent=1)
