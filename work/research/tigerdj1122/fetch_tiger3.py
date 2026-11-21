# 미래에셋 TIGER 'ETF 분배금 현황' 페이지(연간 분배금 표) — 458730 줄과 부르는 ajax 저장, 2026-11-21
import json, re
from playwright.sync_api import sync_playwright
U = 'https://investments.miraeasset.com/tigeretf/ko/product/search/detail/index.do?ksdFund=KR7458730008'
got = []
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page()
    pg.on('response', lambda r: got.append(r.url) if 'ajax' in r.url else None)
    pg.goto(U, timeout=60000); pg.wait_for_timeout(3000)
    pg.get_by_text('ETF 분배금 현황').first.click(); pg.wait_for_timeout(6000)
    print('URL', pg.url)
    for _ in range(30):
        t = pg.inner_text('body')
        if '458730' in t: break
        more = pg.locator('text=더보기')
        if more.count() == 0: break
        try: more.first.click(timeout=5000); pg.wait_for_timeout(1500)
        except Exception: break
    t = pg.inner_text('body'); open('raw/tiger_dist_page_1121.txt', 'w', encoding='utf-8').write(t)
    i = t.find('458730'); print(t[max(0, i-200):i+300] if i >= 0 else 'NO 458730')
    b.close()
print('\n'.join(sorted(set(got))))
