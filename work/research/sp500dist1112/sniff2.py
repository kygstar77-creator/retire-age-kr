# 페이지에서 글자를 눌러 뜨는 API 주소와 화면 글자를 함께 잡는다
import sys
from playwright.sync_api import sync_playwright
sys.stdout.reconfigure(encoding='utf-8')
url, txt, out = sys.argv[1], sys.argv[2], sys.argv[3]
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(); seen = []
    pg.on('response', lambda r: seen.append(r.url) if ('/api/' in r.url or '.ajax' in r.url) else None)
    pg.goto(url, wait_until='networkidle', timeout=60000); pg.wait_for_timeout(1500)
    els = pg.get_by_text(txt)
    for i in range(els.count()):
        try: els.nth(i).click(timeout=3000); pg.wait_for_timeout(2000)
        except Exception: pass
    for u in sorted(set(seen)): print(u)
    open(out, 'w', encoding='utf-8').write(pg.inner_text('body')); b.close()
