from playwright.sync_api import sync_playwright
import pathlib
p = pathlib.Path(__file__).with_name('preview.html').resolve().as_uri()
out = pathlib.Path(__file__).parent
with sync_playwright() as pw:
    b = pw.chromium.launch()
    pg = b.new_page(viewport={'width': 1700, 'height': 900}, device_scale_factor=1)
    pg.goto(p); pg.wait_for_timeout(600)
    pg.screenshot(path=str(out / 'preview.png'), full_page=True)
    for i in 'ABCD':
        pg.query_selector('#' + i).screenshot(path=str(out / f'{i}-375.png'))
        btn = pg.eval_on_selector(f'#{i} .ds-btn', 'e=>{const r=e.getBoundingClientRect(),p=e.closest(".ph").getBoundingClientRect();return [Math.round(r.bottom-p.top), Math.round(r.height)]}')
        over = pg.eval_on_selector(f'#{i} .body', 'e=>e.scrollWidth-e.clientWidth')
        print(i, 'button bottom/height', btn, 'overflow', over)
    b.close()
