# KODEX 441640(fId 2ETFH4) 상품 화면의 API 응답 전부 저장 — 분배금 이력·기간 수익률 찾기 (youtube-loop 2026-11-22)
import json
from playwright.sync_api import sync_playwright
hits = []
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page()
    def on_resp(r):
        if '/api/' in r.url:
            try: hits.append({'url': r.url, 'body': r.text()[:300000]})
            except Exception: pass
    pg.on('response', on_resp)
    pg.goto('https://m.samsungfund.com/etf/product/view.do?id=2ETFH4', timeout=60000)
    pg.wait_for_load_state('networkidle', timeout=60000); pg.wait_for_timeout(3000)
    for _ in range(12):
        pg.mouse.wheel(0, 2500); pg.wait_for_timeout(700)
    open('raw/kodex_view_1122.txt', 'w', encoding='utf-8').write(pg.inner_text('body'))
    open('raw/kodex_view_api_1122.json', 'w', encoding='utf-8').write(json.dumps(hits, ensure_ascii=False))
    for h in hits: print(h['url'][:150], len(h['body']))
    b.close()
