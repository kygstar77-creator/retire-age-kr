# R-1 r2h(2026-10-05 visual 24차) — r2e에서 머리 두 줄 '1억 예금'·'세후 1년'을 88→124px(168px 목록에서 주제가 바로 읽히게, Claude 24차 지적)
# '세후'를 줄이지 않는다(r2f 레드팀 반려). 오른쪽 아래(x>960·y>576)·아래 5% 그대로 비움.
import os, sys, pathlib
sys.stdout.reconfigure(encoding='utf-8')
from playwright.sync_api import sync_playwright
from PIL import Image
H = os.path.dirname(os.path.abspath(__file__)); EP = os.path.join(H, '..', '..', 'longform', 'ep', 'R-1')
s = open(os.path.join(H, 'r2e.html'), encoding='utf-8').read()
R = [("left:50px;top:76px;font-size:88px", "left:44px;top:58px;font-size:124px"),
     ("left:50px;top:192px;font-size:88px", "left:44px;top:206px;font-size:124px"),
     ("data-fit='490' style='left:40px;top:380px", "data-fit='490' style='left:40px;top:392px")]
for a, b in R: assert a in s, a; s = s.replace(a, b)
p = os.path.join(H, 'r2h.html'); open(p, 'w', encoding='utf-8').write(s)
with sync_playwright() as pw:
    br = pw.chromium.launch(); pg = br.new_page(viewport={'width': 1280, 'height': 720}); pg.goto(pathlib.Path(p).as_uri())
    pg.wait_for_selector('body[data-ready]', timeout=15000)
    print(pg.evaluate("()=>[...document.querySelectorAll('.lab,.t,.fine')].slice(0,4).map(e=>{const r=e.getBoundingClientRect();return [e.textContent,Math.round(r.left),Math.round(r.top),Math.round(r.right),Math.round(r.bottom),getComputedStyle(e).fontSize]})"))
    out = os.path.join(EP, 'thumb_r2h.png'); pg.screenshot(path=out); br.close()
im = Image.open(out).convert('RGB')
for w in (168, 320): im.resize((w, round(w * 9 / 16)), Image.LANCZOS).save(os.path.join(H, f'r2h_{w}.png'))
