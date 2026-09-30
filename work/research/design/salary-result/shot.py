from playwright.sync_api import sync_playwright
import pathlib
p = pathlib.Path('preview.html').resolve().as_uri()
with sync_playwright() as pw:
    b = pw.chromium.launch()
    pg = b.new_page(viewport={'width': 880, 'height': 900}, device_scale_factor=1)
    pg.goto(p); pg.wait_for_timeout(600)
    pg.screenshot(path='code-preview.png', full_page=True)
    for i in ('A','B'):
        print(i, pg.eval_on_selector('#'+i, 'e=>[e.scrollWidth,e.clientWidth,e.scrollHeight]'))
    print('font', pg.evaluate("document.fonts.check('16px \"Pretendard Variable\"')"))
    b.close()
