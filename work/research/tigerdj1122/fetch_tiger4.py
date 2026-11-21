# 미래에셋 TIGER 상품 상세(458730) 렌더 뒤 총보수·분배 이력 받기 — audit 11/21 21:14 요청(네이버 대신 운용사 원문), 2026-11-21 23시
import re
from playwright.sync_api import sync_playwright
U = 'https://investments.miraeasset.com/tigeretf/ko/product/search/detail/index.do?ksdFund=KR7458730008'
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page()
    pg.goto(U, timeout=60000); pg.wait_for_load_state('networkidle', timeout=60000); pg.wait_for_timeout(5000)
    t = pg.inner_text('body')
    open('raw/tiger_page_1121d.txt', 'w', encoding='utf-8').write(t)
    for k in ['총보수', '보수', '분배금', '기준일']:
        for m in re.finditer(k, t):
            print(k, '|', t[max(0, m.start()-60):m.start()+120].replace('\n', ' / ')); break
    b.close()
