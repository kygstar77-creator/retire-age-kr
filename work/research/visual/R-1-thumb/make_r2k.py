# R-1 r2k·r2l(2026-10-05 visual 27차) = r2i 그대로 + 오른쪽 칸 아래 빈 띠 중 왼쪽(x570~950·y592~668)만 채움
# 24~26차 새 심사관 공통 '오른쪽 아래 20% 빈 띠' 지적. 재생시간 자리(x>960·y>576)·아래 5%(y>684)는 그대로 비움.
# r2k = 비교 조건 '같은 1억 · 같은 1년'(사실표 [계산]·[영수증] 조건 그대로) · r2l = 질문 '예금은 몇 등?'(값·순위는 안 줌)
import os, sys, pathlib
sys.stdout.reconfigure(encoding='utf-8')
from playwright.sync_api import sync_playwright
from PIL import Image
H = os.path.dirname(os.path.abspath(__file__)); EP = os.path.join(H, '..', '..', 'longform', 'ep', 'R-1')
base = open(os.path.join(H, 'r2i.html'), encoding='utf-8').read()
BAND = ("<div style='position:absolute;left:570px;top:592px;width:380px;height:76px;background:{bg};border-radius:14px'></div>"
        "<div class='lab' style='left:570px;top:592px;width:380px;height:76px;display:flex;align-items:center;justify-content:center;font-size:{fs}px;line-height:1;color:{fg}'>{t}</div>")
V = {'r2k': BAND.format(bg='#22262E', fg='#FFFFFF', fs=44, t='같은 1억 · 같은 1년'),
     'r2l': BAND.format(bg='#FFD43B', fg='#0F1720', fs=50, t='예금은 몇 등?')}
with sync_playwright() as pw:
    br = pw.chromium.launch(); pg = br.new_page(viewport={'width': 1280, 'height': 720})
    for k, band in V.items():
        s = base.replace('\n<script>', band + '\n<script>', 1); p = os.path.join(H, k + '.html'); open(p, 'w', encoding='utf-8').write(s)
        pg.goto(pathlib.Path(p).as_uri()); pg.wait_for_selector('body[data-ready]', timeout=15000)
        r = pg.evaluate("""()=>{const E=[...document.querySelectorAll('.lab,.t,.fine')].map(e=>({t:e.textContent,b:e.getBoundingClientRect()}));
          const hit=(a,c)=>a.right>c.left&&a.left<c.right&&a.bottom>c.top&&a.top<c.bottom;let o=[];
          for(let i=0;i<E.length;i++)for(let j=i+1;j<E.length;j++)if(hit(E[i].b,E[j].b))o.push(E[i].t+'×'+E[j].t);
          const z=E.filter(x=>(x.b.right>960&&x.b.bottom>576)||x.b.bottom>684).map(x=>x.t);
          return {overlap:o,zone:z}}""")
        print(k, r); assert not r['overlap'] and not r['zone']
        out = os.path.join(EP, f'thumb_{k}.png'); pg.screenshot(path=out)
        im = Image.open(out).convert('RGB')
        for w in (168, 320): im.resize((w, round(w * 9 / 16)), Image.LANCZOS).save(os.path.join(H, f'{k}_{w}.png'))
    br.close()
