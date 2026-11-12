# 운용사 페이지가 부르는 분배금 API 주소를 찾는다
import sys
from playwright.sync_api import sync_playwright
sys.stdout.reconfigure(encoding='utf-8')
url = sys.argv[1]
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(); seen = []
    pg.on('response', lambda r: seen.append(r.url) if r.request.resource_type in ('xhr', 'fetch') else None)
    pg.goto(url, wait_until='networkidle', timeout=60000); pg.wait_for_timeout(2000)
    for u in seen: print(u)
    b.close()
