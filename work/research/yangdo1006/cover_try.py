# yangdo1006 표지 1안 — 남색 카드 틀(hfguar1006 mc_h.py와 같은 방식). 결과 covers_try/00_<안>.png, 비교판 board_<안>.png
import os, sys, json
sys.stdout.reconfigure(encoding='utf-8')
D = os.path.dirname(os.path.abspath(__file__))
V = os.path.join(D, '..', 'visual', 'cafe-covers-1002'); sys.path.insert(0, V)
import make_covers as MC
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from playwright.sync_api import sync_playwright
HT = (MC.HTML.replace('background:#F7F8FA', 'background:#0F1B3D').replace('.stamp{', '.stamp{display:none;')
      .replace('color:#6B7280', 'color:#A5B4D4').replace('top:196px', 'top:96px')
      .replace('let s=parseFloat(n.style.fontSize);while(', 'let s=n?parseFloat(n.style.fontSize):0;while(n&&'))
Y, Wt = '#FFD43B', '#FFFFFF'
SRC = '소득세법 제95조② 표1·표2 · 시행령 제159조의4'
V_ = {
 'T2': [('12억 넘는 집 양도세', 120, Y, 't'), ('2년 살면 공제', 150, Wt, 't'), ('30→80|%', 300, Y, 'num')],
 'T3': [('2년 살았나요?', 150, Y, 't'), ('12억 넘는 집 양도세 공제', 96, Wt, 't'), ('30→80|%', 300, Y, 'num')],
 'T4': [('12억 넘는 집 양도세', 110, Y, 't'), ('직접 살면 공제 최대', 130, Wt, 't'), ('80|%', 380, Y, 'num'), ('안 살면 30%까지', 100, Wt, 't')],
 'T5': [('12억 넘는 집 양도세', 110, Y, 't'), ('직접 살면 공제 최대', 130, Wt, 't'), ('80|%', 420, Y, 'num')],
 'T6': [('12억 넘는 1주택 양도세', 104, Y, 't'), ('직접 살면 공제 최대', 130, Wt, 't'), ('80|%', 380, Y, 'num'), ('2년 못 살면 30%', 100, Wt, 't')],
 'T1': [('12억 넘는 1주택 양도세', 100, Y, 't'), ('2년 살았는지로 공제가', 112, Wt, 't'), ('30|%→80%', 230, Y, 'num'), ('장기보유특별공제 비교', 84, Wt, 't')],
}
names = sys.argv[1:] or list(V_)
S = 110; F = ImageFont.truetype(r'C:\Windows\Fonts\malgunbd.ttf', 12)
comp = json.load(open(os.path.join(D, 'covers_try', 'comp', 'comp.json'), encoding='utf-8'))['files'][:5]
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1080, 'height': 1080})
    for n in names:
        html = os.path.join(D, 'covers_try', n + '.html')
        open(html, 'w', encoding='utf-8').write(HT % dict(stamp='', src=SRC, f=MC.M.FONTS, rows=MC.rows_html(V_[n])))
        pg.goto(Path(html).as_uri()); pg.wait_for_selector('body[data-ready]')
        box = pg.evaluate("[...document.querySelectorAll('.k,.src')].map(e=>{const r=e.getBoundingClientRect();return [e.className,Math.round(r.right),Math.round(r.bottom)]})")
        print(n, box)
        out = os.path.join(D, 'covers_try', f'00_{n}.png'); pg.screenshot(path=out)
        Image.open(out).resize((168, 168), Image.LANCZOS).save(os.path.join(D, 'covers_try', f'00_{n}_168.png'))
        items = [('우리 새 표지', out)] + [(f'경쟁 {i+1}', os.path.join(D, 'covers_try', 'comp', c)) for i, c in enumerate(comp)]
        pad = 12; bd = Image.new('RGB', (len(items) * (S + pad) + pad, S + 2 * pad + 20), 'white'); d = ImageDraw.Draw(bd)
        for i, (lab, pp) in enumerate(items):
            im = Image.open(pp).convert('RGB'); w, h = im.size; m = min(w, h)
            im = im.crop(((w - m) // 2, (h - m) // 2, (w - m) // 2 + m, (h - m) // 2 + m)).resize((S, S), Image.LANCZOS)
            x = pad + i * (S + pad); bd.paste(im, (x, pad)); d.text((x, pad + S + 4), lab, fill='black', font=F)
        bd.save(os.path.join(D, 'covers_try', f'board_{n}.png'))
    b.close()
