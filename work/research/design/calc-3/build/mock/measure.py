from playwright.sync_api import sync_playwright
import pathlib,json
d=pathlib.Path(__file__).parent
with sync_playwright() as pw:
    b=pw.chromium.launch()
    for w in (320,375):
        pg=b.new_page(viewport={'width':w,'height':1400},device_scale_factor=2)
        pg.goto((d/'index.html').as_uri()); pg.wait_for_timeout(800)
        r=pg.evaluate('''()=>[...document.querySelectorAll('section')].map(s=>{const t=[...s.querySelectorAll('.ds-tile')];return [s.id, t.map(x=>{const v=x.querySelector('.ds-stat__value');const tr=x.getBoundingClientRect(),vr=v.getBoundingClientRect();const pr=parseFloat(getComputedStyle(x).paddingRight);return +(tr.right-pr-vr.right).toFixed(1)})]})''')
        print(w, json.dumps(r,ensure_ascii=False), pg.evaluate('document.fonts.check("15px \'Pretendard Variable\'")'))
        pg.screenshot(path=str(d/f'm{w}.png'),full_page=True)
    b.close()
