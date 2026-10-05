# R-1 r2j(2026-10-05 visual 26차) = r2h 왼쪽 그대로 + 오른쪽 세 줄 다시 짬
# 25차 Claude·레드팀 공통: S&P500(58px)이 168px에서 흐리고 '+'에 붙어 한 덩어리 → 금 줄을 낮추고(136) S&P500·SCHD 줄을 높여(184~194)
# 이름 72~76px을 줄 위쪽 왼편, 가린 숫자 112px을 아래 오른편에 엇갈려 둔다(가로로 붙지 않게). 오른쪽 아래(x>960·y>576) 그대로 비움.
import os, re, sys, pathlib
sys.stdout.reconfigure(encoding='utf-8')
from playwright.sync_api import sync_playwright
from PIL import Image
H = os.path.dirname(os.path.abspath(__file__)); EP = os.path.join(H, '..', '..', 'longform', 'ep', 'R-1')
s = open(os.path.join(H, 'r2h.html'), encoding='utf-8').read()
m = re.search(r"<div style='position:absolute;left:570px;top:40px.*?SCHD</div><div class='t'[^>]*>\+\?,\?\?\?만</div>", s)
assert m
BG = "<div style='position:absolute;left:570px;top:{t}px;width:690px;height:{h}px;background:#22262E;border-radius:16px'></div>"
NEW = (BG.format(t=40, h=136) + "<div class='lab' style='left:592px;top:68px;font-size:80px;line-height:1;color:#fff'>금</div>"
       "<div class='t' style='right:38px;top:52px;font-size:112px;color:#2BD98C'>+???만</div>"
       + BG.format(t=186, h=194) + "<div class='lab' style='left:592px;top:206px;font-size:72px;line-height:1;color:#fff'>S&P500</div>"
       "<div class='t' style='right:38px;top:262px;font-size:112px;color:#2BD98C'>+?,???만</div>"
       + BG.format(t=390, h=184) + "<div class='lab' style='left:592px;top:404px;font-size:76px;line-height:1;color:#fff'>SCHD</div>"
       "<div class='t' style='right:38px;top:452px;font-size:112px;color:#2BD98C'>+?,???만</div>")
s = s[:m.start()] + NEW + s[m.end():]
p = os.path.join(H, 'r2j.html'); open(p, 'w', encoding='utf-8').write(s)
with sync_playwright() as pw:
    br = pw.chromium.launch(); pg = br.new_page(viewport={'width': 1280, 'height': 720}); pg.goto(pathlib.Path(p).as_uri())
    pg.wait_for_selector('body[data-ready]', timeout=15000)
    r = pg.evaluate("""()=>{const E=[...document.querySelectorAll('.lab,.t,.fine')].map(e=>({t:e.textContent,b:e.getBoundingClientRect()}));
      const hit=(a,c)=>a.right>c.left&&a.left<c.right&&a.bottom>c.top&&a.top<c.bottom;let o=[];
      for(let i=0;i<E.length;i++)for(let j=i+1;j<E.length;j++)if(hit(E[i].b,E[j].b))o.push(E[i].t+'×'+E[j].t);
      const z=E.filter(x=>x.b.right>960&&x.b.bottom>576).map(x=>x.t);
      return {overlap:o,zone:z,box:E.map(x=>[x.t,Math.round(x.b.left),Math.round(x.b.top),Math.round(x.b.right),Math.round(x.b.bottom)])}}""")
    print(r); assert not r['overlap'] and not r['zone']
    out = os.path.join(EP, 'thumb_r2j.png'); pg.screenshot(path=out); br.close()
im = Image.open(out).convert('RGB')
for w in (168, 320): im.resize((w, round(w * 9 / 16)), Image.LANCZOS).save(os.path.join(H, f'r2j_{w}.png'))
