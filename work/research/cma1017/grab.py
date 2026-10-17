import sys, re
sys.stdout.reconfigure(encoding='utf-8')
from playwright.sync_api import sync_playwright
U = {'kis': 'https://securities.koreainvestment.com/main/customer/cma/_static/TF04ca010000.jsp',
     'kis_m': 'https://securities.koreainvestment.com/mobile/asset/CmaInfo.jsp',
     'shinhan': 'https://m.shinhansec.com/mweb/fnin/fcma/ffcma0001?tab=0'}
with sync_playwright() as p:
    b = p.chromium.launch(headless=True)
    for k, u in U.items():
        try:
            pg = b.new_page(); pg.goto(u, timeout=40000); pg.wait_for_timeout(4000)
            t = pg.inner_text('body'); open(f'raw/{k}.txt', 'w', encoding='utf-8').write(t)
            hits = [l.strip() for l in t.splitlines() if '%' in l]
            print('==', k, len(t)); print('\n'.join(hits[:40]))
        except Exception as e: print(k, 'ERR', e)
    b.close()
