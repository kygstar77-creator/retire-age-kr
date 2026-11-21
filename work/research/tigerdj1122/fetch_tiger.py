# 미래에셋 TIGER 상품 페이지 분배금 표 텍스트 받기(자바스크립트로 그려져 Playwright), 2026-11-21
import sys
from playwright.sync_api import sync_playwright
U = 'https://investments.miraeasset.com/tigeretf/ko/product/search/detail/index.do?ksdFund=KR7458730008'
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page()
    pg.goto(U, timeout=60000); pg.wait_for_timeout(6000)
    open('raw/tiger_page_1121.txt', 'w', encoding='utf-8').write(pg.inner_text('body'))
    for kw in ['분배금', '분배']:
        try:
            pg.get_by_text(kw, exact=False).first.click(timeout=5000); pg.wait_for_timeout(3000); break
        except Exception as e: print('click fail', kw, e)
    open('raw/tiger_page_1121b.txt', 'w', encoding='utf-8').write(pg.inner_text('body'))
    b.close()
