# R-1 B2안(2026-10-05 visual) — illustrator B안(r2e + 통장) 고칠 점 반영: 통장 1.3배(156→200px)·안쪽 회색 줄 2개 지움
# py -3.12 make_b2.py → ../../longform/ep/R-1/thumb_r2g.png + r2g_168/320.png, 겹침(글자↔통장·글자↔숫자) 검사
import os, re, sys, pathlib
sys.stdout.reconfigure(encoding='utf-8')
from playwright.sync_api import sync_playwright
from PIL import Image
H = os.path.dirname(os.path.abspath(__file__)); EP = os.path.join(H, '..', '..', 'longform', 'ep', 'R-1')
b = open(os.path.join(H, '..', 'objects', 'r1prop', 'b.html'), encoding='utf-8').read()
# 회색 줄 2개(흰 테두리 판 + 색 판 모두)
n0 = len(b)
b = re.sub(r'<rect x="190" y="(160|222)"[^>]*/>', '', b)
assert len(b) < n0 and 'y="160"' not in b and 'y="222"' not in b
X, Y, W = int(sys.argv[1]) if len(sys.argv) > 1 else 344, int(sys.argv[2]) if len(sys.argv) > 2 else 40, 200
b = b.replace("<div style='position:absolute;left:384px;top:60px;width:156px;height:156px'>", f"<div id='bk' style='position:absolute;left:{X}px;top:{Y}px;width:{W}px;height:{W}px'>")
b = b.replace('width="156" height="156" viewBox', f'width="{W}" height="{W}" viewBox')
assert "id='bk'" in b
p = os.path.join(H, 'r2g.html'); open(p, 'w', encoding='utf-8').write(b)
with sync_playwright() as pw:
    br = pw.chromium.launch(); pg = br.new_page(viewport={'width': 1280, 'height': 720}); pg.goto(pathlib.Path(p).as_uri())
    pg.wait_for_selector('body[data-ready]', timeout=15000)
    info = pg.evaluate("""()=>{const r=e=>e.getBoundingClientRect();const bk=document.querySelector('#bk svg');
      // 통장 실제 그림 영역(svg 안 그림은 70~442 / 512)
      const s=r(bk),k=s.width/512,bb={left:s.left+70*k,right:s.left+442*k,top:s.top+94*k,bottom:s.top+400*k};
      const T=[...document.querySelectorAll('.lab,.t,.fine')].map(e=>({t:e.textContent,b:r(e)}));
      const hit=(a,c)=>a.right>c.left&&a.left<c.right&&a.bottom>c.top&&a.top<c.bottom;
      return {bk:bb,over:T.filter(x=>hit(x.b,bb)).map(x=>x.t),labs:T.map(x=>[x.t,Math.round(x.b.left),Math.round(x.b.top),Math.round(x.b.right),Math.round(x.b.bottom)])}}""")
    print(info)
    out = os.path.join(EP, 'thumb_r2g.png'); pg.screenshot(path=out); br.close()
im = Image.open(out).convert('RGB')
for w in (168, 320): im.resize((w, round(w * 9 / 16)), Image.LANCZOS).save(os.path.join(H, f'r2g_{w}.png'))
print('ok', out)
