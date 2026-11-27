# KODEX 분배금 지급현황 버튼이 부르는 JSON 찾기. 11/27 write.
import sys, re
sys.stdout.reconfigure(encoding='utf-8')
from playwright.sync_api import sync_playwright
hits=[]
with sync_playwright() as p:
    b=p.chromium.launch(headless=True)
    pg=b.new_page(user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/124')
    def on(r):
        if r.request.resource_type in ('xhr','fetch'):
            try: hits.append((r.url, r.text()[:300]))
            except Exception: hits.append((r.url,''))
    pg.on('response',on)
    pg.goto('https://www.samsungfund.com/etf/product/view.do?id=2ETFO6',timeout=60000,wait_until='domcontentloaded'); pg.wait_for_timeout(6000)
    n=len(hits)
    els=pg.get_by_text('분배금 지급현황')
    print('count',els.count())
    for i in range(els.count()):
        try: els.nth(i).click(timeout=3000); pg.wait_for_timeout(3000)
        except Exception as e: print(i,'x')
    for u,s in hits[n:]: print(u); print('  ',s[:300])
    b.close()
