# 미래에셋 TIGER 458730 상품 페이지가 부르는 JSON 응답을 그대로 저장, 2026-11-21
import json
from playwright.sync_api import sync_playwright
U = 'https://investments.miraeasset.com/tigeretf/ko/product/search/detail/index.do?ksdFund=KR7458730008'
got = []
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page()
    def on(r):
        try:
            ct = r.headers.get('content-type', '')
            if 'json' in ct or r.url.endswith('.ajax') or 'ajax' in r.url:
                got.append({'url': r.url, 'body': r.text()[:200000]})
        except Exception: pass
    pg.on('response', on)
    pg.goto(U, timeout=60000, wait_until='networkidle'); pg.wait_for_timeout(5000)
    open('raw/tiger_page_1121c.txt', 'w', encoding='utf-8').write(pg.inner_text('body'))
    b.close()
json.dump(got, open('raw/tiger_ajax_1121.json', 'w', encoding='utf-8'), ensure_ascii=False)
for g in got: print(g['url'][:160], len(g['body']))
