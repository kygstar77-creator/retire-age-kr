# TIGER 미국S&P500 상품 페이지 분배금 지급현황 — 더보기를 눌러 전체 기록을 글자로 저장, 응답 주소도 남김
import sys
from playwright.sync_api import sync_playwright
sys.stdout.reconfigure(encoding='utf-8')
seen=[]
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page()
    pg.on('response', lambda r: seen.append(r.url) if ('.ajax' in r.url or '/api/' in r.url or 'distrib' in r.url.lower() or 'divid' in r.url.lower()) else None)
    pg.goto('https://investments.miraeasset.com/tigeretf/ko/product/search/detail/index.do?ksdFund=KR7360750004', wait_until='networkidle', timeout=60000)
    pg.wait_for_timeout(2000)
    for i in range(8):
        btns=pg.locator('text=더보기')
        n=btns.count(); clicked=False
        for j in range(n):
            el=btns.nth(j)
            try:
                box=el.evaluate("e=>{let s=e.closest('section,div');return s?s.innerText.slice(0,0):''}")
                par=el.evaluate("e=>{let x=e;for(let k=0;k<6&&x;k++){x=x.parentElement;if(x&&x.innerText.includes('분배금 지급현황'))return 1}return 0}")
                if par and el.is_visible():
                    el.click(); pg.wait_for_timeout(1500); clicked=True; break
            except Exception as ex: pass
        if not clicked: break
    open('raw/tiger_detail_full.txt','w',encoding='utf-8').write(pg.inner_text('body'))
    b.close()
print('\n'.join(sorted(set(seen))))
