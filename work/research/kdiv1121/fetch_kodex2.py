# KODEX 고배당주(2ETF96) 상품 페이지 분배금 — 11/20 12:3x 한 번만(Cloudflare 막히면 멈춤)
import sys, json
from playwright.sync_api import sync_playwright
sys.stdout.reconfigure(encoding='utf-8')
J = {}
with sync_playwright() as p:
    b = p.chromium.launch(headless=False, args=['--window-position=-2400,-2400']); pg = b.new_page()
    pg.on('response', lambda r: J.__setitem__(r.url, r.text()) if ('divid' in r.url.lower() and r.status == 200) else None)
    try:
        pg.goto('https://www.samsungfund.com/etf/product/view.do?id=2ETF96', wait_until='domcontentloaded', timeout=60000); pg.wait_for_timeout(12000)
        print(pg.title())
        for t in ('분배금', '분배'):
            try: pg.get_by_text(t, exact=True).first.click(timeout=4000); pg.wait_for_timeout(4000); break
            except Exception: pass
        t = pg.inner_text('body'); open('raw/kodex_2ETF96_1120.txt', 'w', encoding='utf-8').write(t); print(len(t), t.count('분배'))
    except Exception as e: print('ERR', e)
    json.dump(J, open('raw/kodex_2ETF96_api_1120.json', 'w', encoding='utf-8'), ensure_ascii=False); print(list(J)[:5])
    b.close()
