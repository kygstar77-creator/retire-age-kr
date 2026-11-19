# TIGER 연도별 분배금 목록에서 '미국S&P500' 검색 결과만 저장(2022~2026 연간 분배금 합)
import sys
from playwright.sync_api import sync_playwright
sys.stdout.reconfigure(encoding='utf-8')
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page()
    pg.goto('https://investments.miraeasset.com/tigeretf/ko/distribution/annual/list.do', wait_until='networkidle', timeout=60000)
    pg.wait_for_timeout(1500)
    inp=pg.locator('input[type=text]')
    for i in range(inp.count()):
        e=inp.nth(i)
        if e.is_visible():
            e.fill('미국S&P500'); e.press('Enter'); break
    pg.wait_for_timeout(3000)
    open('raw/tiger_annual_sp.txt','w',encoding='utf-8').write(pg.inner_text('body')); b.close()
