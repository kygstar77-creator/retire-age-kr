# TIGER 분배금 현황 페이지(자바스크립트 표)를 Playwright로 열어 글자만 저장
import sys
from playwright.sync_api import sync_playwright
sys.stdout.reconfigure(encoding='utf-8')
code, out = sys.argv[1], sys.argv[2]
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page()
    pg.goto(f'https://investments.miraeasset.com/tigeretf/ko/distribution/annual/list.do?ksdFund={code}', wait_until='networkidle', timeout=60000)
    pg.wait_for_timeout(2500)
    t = pg.inner_text('body'); open(out, 'w', encoding='utf-8').write(t); b.close()
