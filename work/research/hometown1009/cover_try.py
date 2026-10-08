# hometown1009 표지 (deplend1009 틀) — yangdo1006 cover_try 틀 — 남색 카드 틀(hfguar1006 mc_h.py와 같은 방식). 결과 covers_try/00_<안>.png, 비교판 board_<안>.png
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
SRC = '조세특례제한법 제58조 · 시행령 제5조'
V_ = {
 'H1': [('고향사랑기부제', 130, Wt, 't'), ('20만원 기부', 170, Y, 't'), ('세금 14만4천원', 150, Wt, 't')],
 'H2': [('고향사랑기부제', 130, Y, 't'), ('10만원 → 13만원', 150, Wt, 't'), ('20만원 → 20만4천원', 120, Wt, 't')],
 'H4': [('고향사랑기부제', 130, Wt, 't'), ('20만원 기부', 170, Y, 't'), ('세금 14만4천 공제', 130, Wt, 't')],
 'H3': [('고향사랑기부제', 140, Wt, 't'), ('기부액별', 130, Wt, 't'), ('돌려받는 돈', 200, Y, 't')],
}
names = sys.argv[1:] or list(V_)
S = 110; F = ImageFont.truetype(r'C:\Windows\Fonts\malgunbd.ttf', 12)
comp = json.load(open(os.path.join(D, 'covers_try', 'comp', 'comp.json'), encoding='utf-8'))['files'][:5]
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1080, 'height': 1080})
    for n in names:
        html = os.path.join(D, 'covers_try', n + '.html')
        HX = HT.replace('background:#0F1B3D', 'background:#FFD43B').replace('color:#A5B4D4','color:#0F1B3D') if n=='G12' else (HT.replace('background:#0F1B3D', 'background:#D7261E').replace('color:#A5B4D4','color:#FFE3E0') if n=='G16' else (HT.replace('background:#0F1B3D', 'background:#1F4FD8').replace('color:#A5B4D4','color:#DCE6FF') if n=='G17' else HT))
        open(html, 'w', encoding='utf-8').write(HX % dict(stamp='', src=SRC, f=MC.M.FONTS, rows=MC.rows_html(V_[n])))
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
