import sys
from playwright.sync_api import sync_playwright
sys.stdout.reconfigure(encoding='utf-8')
url, out = sys.argv[1], sys.argv[2]
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page()
    pg.goto(url, timeout=45000); pg.wait_for_timeout(5000)
    t = pg.inner_text('body')
    for f in pg.frames:
        try: t += '\n=====FRAME ' + f.url + '\n' + f.inner_text('body')
        except Exception: pass
    open(out, 'w', encoding='utf-8').write(t); print(len(t))
    b.close()
