# 운용사 상품 페이지(자바스크립트) Playwright로 글자만. 11/27 write. ISIN = KR7+코드+00+검사숫자.
import sys, re
sys.stdout.reconfigure(encoding='utf-8')
from playwright.sync_api import sync_playwright
def isin(code):
    s='KR7'+code+'00'; digs=''.join(str(int(c,36)) for c in s)
    tot=0
    for i,ch in enumerate(reversed(digs)):
        n=int(ch)
        if i%2==0: n*=2
        tot+=n//10+n%10
    return s+str((10-tot%10)%10)
P={}
for c in ['441680','486290']: P['tiger_'+c]=f'https://investments.miraeasset.com/tigeretf/ko/product/search/detail/index.do?ksdFund={isin(c)}'
P['kodex_494300']='https://www.samsungfund.com/etf/search.do?keyword=494300'
for c in ['441680','486290','494300']: P['funetf_'+c]=f'https://www.funetf.co.kr/product/etf/view/{isin(c)}'
with sync_playwright() as p:
    b=p.chromium.launch(headless=True)
    for k,u in P.items():
        pg=b.new_page(user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/124')
        try: pg.goto(u,timeout=40000,wait_until='networkidle')
        except Exception as e: print(k,'goto',repr(e)[:80])
        pg.wait_for_timeout(3000)
        t=re.sub(r'\s+',' ',pg.inner_text('body'))
        open(f'raw/{k}_pw_1127.txt','w',encoding='utf-8').write(pg.url+'\n'+t)
        print('==',k,pg.url,len(t))
        for w in ['총보수','기준일','분배','목표','프리미엄','순자산']:
            m=re.search(w,t)
            if m: print('  ',w,':',t[max(0,m.start()-30):m.start()+160])
    b.close()
