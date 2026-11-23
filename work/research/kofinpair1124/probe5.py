# RISE 상품 화면이 부르는 구성종목 API (firemap-write-b 2026-11-23)
import sys, json, pathlib
from playwright.sync_api import sync_playwright
sys.stdout.reconfigure(encoding='utf-8')
R = pathlib.Path(__file__).resolve().parent / 'raw'
with sync_playwright() as p:
    b = p.chromium.launch(); ctx = b.new_context(viewport={'width': 1400, 'height': 1000})
    got = {}
    ctx.on('response', lambda r: got.__setitem__(r.url, r) if 'kbam.co.kr/api' in r.url else None)
    q = ctx.new_page(); q.goto('https://kbam.co.kr/products/4494', timeout=60000); q.wait_for_timeout(7000)
    for t in ('구성종목', 'PDF', '포트폴리오'):
        try: q.get_by_text(t, exact=False).first.click(timeout=3000); q.wait_for_timeout(4000)
        except Exception: pass
    (R / 'pw' / 'rise_4494.txt').write_text(q.inner_text('body'), encoding='utf-8')
    for u in got: print(u[:200])
    b.close()
