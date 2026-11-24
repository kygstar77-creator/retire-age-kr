# 운용사 상품 페이지 4곳 — 총보수 문구 확인(Playwright 화면 글자), 2026-11-24
import re, sys
sys.stdout.reconfigure(encoding='utf-8')
from playwright.sync_api import sync_playwright
U={'102110':'https://investments.miraeasset.com/tigeretf/ko/product/search/detail/index.do?ksdFund=KR7102110004',
   '069500':'https://www.samsungfund.com/etf/product/view.do?id=2ETF01',
   '148020':'https://www.riseetf.co.kr/prod/finderDetail/44C2',
   '105190':'https://www.aceetf.co.kr/fund/K55101B65619'}
with sync_playwright() as p:
    b=p.chromium.launch()
    for t,u in U.items():
        try:
            pg=b.new_page(); pg.goto(u,timeout=45000); pg.wait_for_timeout(5000)
            x=pg.inner_text('body'); open(f'raw/issuer_{t}_1124.txt','w',encoding='utf-8').write(x)
            hits=[m.start() for m in re.finditer('보수',x)][:4]
            print(t,pg.url,len(x)); [print('   ',x[max(0,h-60):h+80].replace('\n',' | ')) for h in hits]
            pg.close()
        except Exception as e: print(t,'실패',str(e)[:120])
    b.close()
