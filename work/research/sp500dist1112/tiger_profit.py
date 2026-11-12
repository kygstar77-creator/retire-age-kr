# TIGER 상품 페이지가 부르는 수익률(profit.ajax) 응답 원문 저장
import sys
from playwright.sync_api import sync_playwright
sys.stdout.reconfigure(encoding='utf-8')
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(); got = {}
    def on(r):
        if 'detail/profit.ajax' in r.url:
            try: got['t'] = r.text()
            except Exception: pass
    pg.on('response', on)
    pg.goto('https://investments.miraeasset.com/tigeretf/ko/product/search/detail/index.do?ksdFund=KR7360750004', wait_until='networkidle', timeout=60000)
    pg.wait_for_timeout(1500)
    open('raw/tiger_profit.html', 'w', encoding='utf-8').write(got.get('t', ''))
    b.close()
