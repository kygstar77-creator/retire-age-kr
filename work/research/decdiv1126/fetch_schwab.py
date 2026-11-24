# 슈왑 SCHD 문서 화면에서 '2026 주식 ETF 배당 일정표' PDF를 받아 raw/에 둔다
import sys, os
from playwright.sync_api import sync_playwright
here = os.path.dirname(os.path.abspath(__file__))
with sync_playwright() as p:
    b = p.chromium.launch(headless=True)
    ctx = b.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36", accept_downloads=True)
    pg = ctx.new_page()
    pg.goto("https://www.schwabassetmanagement.com/products/schd/documents", wait_until="domcontentloaded", timeout=60000)
    pg.wait_for_timeout(6000)
    links = pg.eval_on_selector_all("a", "els => els.map(e => [e.innerText.trim(), e.href])")
    print(pg.title(), len(links)); print([l for l in links if ".pdf" in l[1].lower()][:30])
    hit = [l for l in links if 'Distribution' in l[0] or 'distribution' in l[1].lower()]
    for l in hit: print(l)
    target = [l for l in hit if 'Equity' in l[0] and '2026' in l[0]]
    if target:
        url = target[0][1]
        r = ctx.request.get(url, timeout=60000)
        open(os.path.join(here, 'raw', 'schwab_equity_sched2026.pdf'), 'wb').write(r.body())
        print('saved', url, r.status, len(r.body()))
    b.close()
