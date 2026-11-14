# 자바스크립트로 그려지는 운용사 페이지를 열어 글자만 저장(필요하면 글자를 눌러 탭 전환)
import sys
from playwright.sync_api import sync_playwright
sys.stdout.reconfigure(encoding='utf-8')
url, out = sys.argv[1], sys.argv[2]; click = sys.argv[3] if len(sys.argv) > 3 else ''
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page()
    pg.goto(url, wait_until='networkidle', timeout=60000); pg.wait_for_timeout(2000)
    if click:
        try: pg.get_by_text(click, exact=True).first.click(); pg.wait_for_timeout(2500)
        except Exception as e: print('click fail', e)
    open(out, 'w', encoding='utf-8').write(pg.inner_text('body')); b.close()
