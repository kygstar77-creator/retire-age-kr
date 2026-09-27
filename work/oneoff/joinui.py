# 한 번 쓰고 끝난 조사 스크립트(2026-09-27 카페 가입 화면 실측, 결과는 research/cafe-features.md 11절).
# 정기 회차가 부르는 도구가 아니라서 work/ 에서 oneoff/ 로 옮겼다(health.py '안 부르는 도구' 집계 제외).
"""다른 카페가 휴대폰 글 화면에서 가입을 어떻게 받는지 잰다(비로그인 / 로그인·비멤버)."""
import sys, os, json, urllib.request, time
sys.stdout.reconfigure(encoding='utf-8')
from playwright.sync_api import sync_playwright
HERE=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # oneoff/ 한 칸 위 = work/
OUT=os.path.join(HERE,'research','_joinui'); os.makedirs(OUT,exist_ok=True)
STATE=r'C:\Users\강영준\Documents\naver_profile\storage_state.json'
H={'User-Agent':'Mozilla/5.0','Referer':'https://cafe.naver.com/'}
def pick(cid):
    u=f'https://apis.naver.com/cafe-web/cafe2/ArticleListV2dot1.json?search.clubid={cid}&search.queryType=lastArticle&search.page=1&search.perPage=20'
    r=json.load(urllib.request.urlopen(urllib.request.Request(u,headers=H),timeout=20))
    out={}
    for a in r['message']['result']['articleList']:
        if a.get('menuName','').startswith('공지'): continue
        k='open' if a.get('openArticle') else 'member'
        out.setdefault(k,a['articleId'])
    return out
JS=r'''()=>{const out=[];const seen=new Set();
document.querySelectorAll('body *').forEach(e=>{const t=(e.innerText||'').trim();if(!t||t.length>90||!/가입/.test(t))return;
 if([...e.children].some(c=>/가입/.test(c.innerText||'')))return; if(e.offsetParent===null&&getComputedStyle(e).position!=='fixed')return;
 let p=e,f='';while(p&&p!==document.body){const s=getComputedStyle(p).position;if(s==='fixed'||s==='sticky'){f=s;break}p=p.parentElement}
 const r=e.getBoundingClientRect(); if(r.width<5||r.height<5)return; const k=t.replace(/\s+/g,' ');if(seen.has(k))return;seen.add(k);
 out.push({t:k,y:Math.round(r.top),h:Math.round(r.height),w:Math.round(r.width),pos:f})});
const dlg=[...document.querySelectorAll('[role=dialog],[class*=layer i],[class*=popup i],[class*=sheet i],[class*=modal i]')].filter(d=>d.offsetParent!==null||getComputedStyle(d).position==='fixed').map(d=>(d.innerText||'').trim().replace(/\s+/g,' ').slice(0,120)).filter(Boolean);
return {out,dlg,vh:innerHeight}}'''
def probe(ctx, tag, club, aid, cid):
    pg=ctx.new_page(); res={}
    try:
        pg.goto(f'https://cafe.naver.com/{club}/{aid}', wait_until='domcontentloaded', timeout=45000)
        pg.wait_for_timeout(4000); res['load']=pg.evaluate(JS); pg.screenshot(path=os.path.join(OUT,f'{club}_{tag}_a.png'))
        pg.mouse.wheel(0,1200); pg.wait_for_timeout(3000); res['scroll']=pg.evaluate(JS); pg.screenshot(path=os.path.join(OUT,f'{club}_{tag}_b.png'))
        pg.mouse.wheel(0,20000); pg.wait_for_timeout(3000); res['end']=pg.evaluate(JS); pg.screenshot(path=os.path.join(OUT,f'{club}_{tag}_c.png'))
        res['url']=pg.url
    except Exception as e: res['err']=str(e)[:120]
    pg.close(); return res
if __name__=='__main__':
    cafes=json.load(open(os.path.join(OUT,'targets.json'),encoding='utf-8'))
    modes=sys.argv[1].split(',') if len(sys.argv)>1 else ['guest','login']
    results=[]
    with sync_playwright() as p:
        b=p.chromium.launch(headless=True)
        ctxs={}
        if 'guest' in modes: ctxs['guest']=b.new_context(**p.devices['iPhone 13'],locale='ko-KR')
        if 'login' in modes: ctxs['login']=b.new_context(**p.devices['iPhone 13'],locale='ko-KR',storage_state=STATE)
        for c in cafes:
            try: aids=pick(c['cafeId'])
            except Exception as e: print(c['cluburl'],'목록 실패',e); continue
            row={**c,'aids':aids}
            for kind,aid in aids.items():
                for m,ctx in ctxs.items(): row[f'{m}_{kind}']=probe(ctx,f'{m}_{kind}',c['cluburl'],aid,c['cafeId'])
            results.append(row); print(c['cluburl'],'완료',flush=True)
            json.dump(results,open(os.path.join(OUT,'joinui.json'),'w',encoding='utf-8'),ensure_ascii=False,indent=1)
        b.close()
