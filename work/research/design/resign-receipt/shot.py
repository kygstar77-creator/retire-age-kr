from playwright.sync_api import sync_playwright
import pathlib
p = pathlib.Path(__file__).with_name('preview.html').resolve().as_uri()
out = pathlib.Path(__file__).parent
with sync_playwright() as pw:
    b = pw.chromium.launch()
    pg = b.new_page(viewport={'width': 1500, 'height': 1000}, device_scale_factor=1)
    pg.goto(p); pg.wait_for_timeout(600)
    pg.screenshot(path=str(out / 'preview.png'), full_page=True)
    pg.query_selector('.phone').screenshot(path=str(out / 'sheet-375.png'))
    r = pg.eval_on_selector('.phone', 'p=>{const a=p.getBoundingClientRect();const s=[...p.querySelectorAll("button")].map(e=>Math.round(e.getBoundingClientRect().bottom-a.top));return {btnBottoms:s, h:Math.round(a.height)}}')
    print('sheet', r)
    m = b.new_page(viewport={'width': 375, 'height': 812})
    m.goto(p); m.wait_for_timeout(400)
    print('mobile overflow', m.evaluate('document.documentElement.scrollWidth-375'))
    b.close()
