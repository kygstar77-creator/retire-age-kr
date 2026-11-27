# 야후에 2025-03 분배가 빠짐 → 운용사 '분배금 지급현황' 표 전부(더보기 반복). 11/27 write.
import sys, re
sys.stdout.reconfigure(encoding='utf-8')
from playwright.sync_api import sync_playwright
T={'441680':'KR7441680006','486290':'KR7486290000'}
with sync_playwright() as p:
    b=p.chromium.launch(headless=True)
    for c,i in T.items():
        pg=b.new_page(user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/124')
        pg.goto(f'https://investments.miraeasset.com/tigeretf/ko/product/search/detail/index.do?ksdFund={i}',timeout=40000,wait_until='domcontentloaded')
        pg.wait_for_timeout(4000)
        pg.get_by_text('분배금 지급 현황',exact=True).first.click(); pg.wait_for_timeout(3000)
        t0=re.sub(r'\s+',' ',pg.inner_text('body')); tot=re.search(r'분배금 지급현황 TIGER.*?총 (\d+)건',t0).group(1); print(' total',tot)
        for _ in range(6):
            try:
                loc=pg.locator('button:has-text("더보기"), a:has-text("더보기")').filter(has_text='/'+tot+')')
                print('  more',loc.count(), loc.first.inner_text()[:30] if loc.count() else '')
                loc.first.click(force=True); pg.wait_for_timeout(2000)
            except Exception as e: print('  stop',repr(e)[:80]); break
        t=re.sub(r'\s+',' ',pg.inner_text('body'))
        m=re.search(r'분배금 지급현황 TIGER.*?(?=확인 닫기|더보기\(\d+/\d+\) 확인)',t)
        seg=m.group(0) if m else ''
        open(f'raw/tiger_{c}_div_1127.txt','w',encoding='utf-8').write(pg.url+'\n'+seg)
        rows=re.findall(r'(\d{4}-\d\d-\d\d) (\d{4}-\d\d-\d\d) ([\d,]+) ([\d,]+)',seg)
        print(c,len(rows),rows[:2],[r for r in rows if r[0].startswith('2025-03')])
    pg=b.new_page(user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/124')
    pg.goto('https://www.samsungfund.com/etf/search.do?keyword=494300',timeout=60000,wait_until='domcontentloaded'); pg.wait_for_timeout(5000)
    print([x for x in pg.eval_on_selector_all('a[href*="product/view"]','e=>e.map(x=>x.href+" "+x.innerText.replace(/\s+/g," ").slice(0,50))') if '나스닥100' in x])
    b.close()
