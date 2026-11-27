# KODEX 494300 공식 상품 페이지(id 2ETFO6 — 투자설명서 PDF 이름) 글자·분배금 지급현황. 11/27 write.
import sys, re
sys.stdout.reconfigure(encoding='utf-8')
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.chromium.launch(headless=True)
    pg=b.new_page(user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/124')
    pg.goto('https://www.samsungfund.com/etf/product/view.do?id=2ETFO6',timeout=60000,wait_until='domcontentloaded'); pg.wait_for_timeout(8000)
    t=re.sub(r'\s+',' ',pg.inner_text('body')); open('raw/kodex_494300_pw_1127.txt','w',encoding='utf-8').write(pg.url+'\n'+t)
    print(pg.url,len(t))
    try:
        pg.get_by_text('분배금 지급현황').first.click(); pg.wait_for_timeout(5000)
        for _ in range(4):
            loc=pg.locator('button:has-text("더보기"), a:has-text("더보기")')
            if not loc.count(): break
            loc.first.click(force=True); pg.wait_for_timeout(2000)
    except Exception as e: print('click',repr(e)[:90])
    t=re.sub(r'\s+',' ',pg.inner_text('body')); open('raw/kodex_494300_div_1127.txt','w',encoding='utf-8').write(pg.url+'\n'+t)
    print('rows',re.findall(r'2025[.\-]0[234][.\-]\d\d.{0,60}',t)[:6])
    b.close()
