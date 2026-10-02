# F3 실업급여 3번 타일 3상태 × 320·375 캡처 + 타일 끝 여백 측정 (product-dev 10/2)
from playwright.sync_api import sync_playwright
import pathlib, sys
out = pathlib.Path(__file__).parent
URL = sys.argv[1] if len(sys.argv) > 1 else 'http://localhost:5181/calc/unemployment-benefit'
STATES = {'floor': 3000000, 'cap': 6000000, 'sixty': 3400000}
SET = '''(v)=>{const el=document.querySelector('input[type=range][aria-label="월평균 임금"]');
const s=Object.getOwnPropertyDescriptor(HTMLInputElement.prototype,'value').set;s.call(el,String(v));
el.dispatchEvent(new Event('input',{bubbles:true}));}'''
MEASURE = '''()=>[...document.querySelector('.ds-hero__tiles').children].map(t=>{
const r=t.getBoundingClientRect();const kids=[...t.children];
return {label:kids[0].innerText,value:kids[kids.length-1].innerText,right:+(r.right).toFixed(1),
margin:+Math.min(...kids.map(k=>{const rg=document.createRange();rg.selectNodeContents(k);return r.right-rg.getBoundingClientRect().right})).toFixed(1)}})'''
with sync_playwright() as pw:
    b = pw.chromium.launch()
    for w in (320, 375):
        pg = b.new_page(viewport={'width': w, 'height': 800}, device_scale_factor=2)
        pg.goto(URL, wait_until='domcontentloaded'); pg.wait_for_selector('.ds-hero--compact-tiles'); pg.wait_for_timeout(500)
        for name, v in STATES.items():
            pg.evaluate(SET, v); pg.wait_for_timeout(250)
            hero = pg.query_selector('.ds-hero--compact-tiles')
            hero.screenshot(path=str(out / f'unemployment-f3-{name}-{w}.png'))
            print(w, name, pg.evaluate(MEASURE))
        pg.close()
    b.close()
