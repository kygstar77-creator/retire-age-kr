# 삼성자산운용 KODEX 441640(미국배당커버드콜액티브) 상품 화면 렌더 뒤 분배금 이력 받기 — youtube-loop 2026-11-22 (CC-1 원문 대조, audit 11/21 1차 출처 규칙)
import re, json
from playwright.sync_api import sync_playwright
hits = []
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page()
    def on_resp(r):
        u = r.url
        if 'samsungfund' in u and ('json' in (r.headers.get('content-type') or '') or 'api' in u):
            try: hits.append({'url': u, 'body': r.text()[:200000]})
            except Exception: pass
    pg.on('response', on_resp)
    pg.goto('https://www.samsungfund.com/etf/product/list.do', timeout=60000)
    pg.wait_for_load_state('networkidle', timeout=60000)
    links = pg.eval_on_selector_all('a', 'as => as.map(a => [a.innerText.trim(), a.href]).filter(x => x[0].includes("커버드콜"))')
    print(json.dumps(links[:20], ensure_ascii=False))
    open('raw/kodex_list_1122.json', 'w', encoding='utf-8').write(json.dumps(hits, ensure_ascii=False))
    print(len(hits), [h['url'][:120] for h in hits][:30])
    b.close()
