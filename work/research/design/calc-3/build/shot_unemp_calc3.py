# calc-3 실업급여 조각(숫자 줄·버튼) 320·375 캡처 + 첫 화면 안 버튼 위치 (product-dev 10/2)
from playwright.sync_api import sync_playwright
import pathlib, sys, json
out = pathlib.Path(__file__).parent
URL = sys.argv[1] if len(sys.argv) > 1 else 'http://localhost:5181/calc/unemployment-benefit'
INP = {'currentAge': 34, 'targetRetirementAge': 50, 'financialAsset': 150000000, 'monthlyInvestment': 1500000, 'monthlyLivingCost': 2500000}
with sync_playwright() as pw:
    b = pw.chromium.launch()
    for seeded in (True, False):
        for w in (320, 375):
            ctx = b.new_context(viewport={'width': w, 'height': 812}, device_scale_factor=2)
            init = "localStorage.setItem('fm_consent_v1','1');" + (f"localStorage.setItem('firemap-inputs-v3', {json.dumps(json.dumps(INP))});" if seeded else '')
            ctx.add_init_script(init)
            pg = ctx.new_page()
            pg.goto(URL, wait_until='commit', timeout=90000); pg.wait_for_selector('.ds-hero--compact-tiles', timeout=90000); pg.wait_for_timeout(800)
            name = f"unemployment-calc3-{'A' if seeded else 'B'}-{w}.png"
            pg.screenshot(path=str(out / name))
            info = pg.evaluate('''()=>{const btn=[...document.querySelectorAll('button')].find(x=>x.innerText.includes('몇 살에 은퇴'));
              const g=document.querySelector('.fm-gain');return {btnBottom: btn?Math.round(btn.getBoundingClientRect().bottom):null,
              gain: g?g.innerText.split(String.fromCharCode(10)).join(' / '):null, overflow: document.documentElement.scrollWidth-innerWidth,
              dark: document.querySelectorAll('.ds-card--dark').length}}''')
            print(name, info)
            ctx.close()
    b.close()
