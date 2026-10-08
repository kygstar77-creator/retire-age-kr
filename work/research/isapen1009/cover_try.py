# isapen1009 표지 (hometown1009 틀) (deplend1009 틀) — yangdo1006 cover_try 틀 — 남색 카드 틀(hfguar1006 mc_h.py와 같은 방식). 결과 covers_try/00_<안>.png, 비교판 board_<안>.png
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
SRC = '소득세법 제59조의3 · 시행령 제118조의2'
V_ = {
 'I1': [('ISA 만기 자금', 130, Wt, 't'), ('연금으로 옮기면', 130, Wt, 't'), ('최대 49만5천원', 150, Y, 't')],
 'I2': [('ISA 연금 이전', 130, Wt, 't'), ('두 해에 나눠도', 140, Y, 't'), ('공제 한도 300만원', 120, Wt, 't')],
 'I3': [('ISA 만기 3천만원', 120, Wt, 't'), ('연금계좌로 옮기면', 120, Wt, 't'), ('49만5천원 환급', 160, Y, 't')],
 'I4': [('ISA → 연금', 190, Wt, 't'), ('49만5천원', 230, Y, 't')],
 'I5': [('ISA 만기 → 연금', 150, Wt, 't'), ('환급 49만5천원', 175, Y, 't')],
 'I6': [('ISA 만기', 190, Wt, 't'), ('→ 연금계좌', 160, Wt, 't'), ('49만5천원 환급', 150, Y, 't')],
 'I7': [('ISA 연금 이전', 150, '#0F1B3D', 't'), ('두 해 나눠도', 170, '#0F1B3D', 't'), ('공제는 한 번', 190, '#D7261E', 't')],
 'I8': [('ISA → 연금', 190, '#0F1B3D', 't'), ('49만5천원', 230, '#D7261E', 't')],
 'I9': [('ISA 연금 이전', 150, '#0F1B3D', 't'), ('두 해 나눠도', 170, '#0F1B3D', 't'), ('한도는 한 번', 190, '#D7261E', 't')],
 'I10': [('ISA 연금 이전', 150, '#0F1B3D', 't'), ('소득 없는 해엔', 160, '#0F1B3D', 't'), ('환급 0원', 230, '#D7261E', 't')],
}
names = sys.argv[1:] or list(V_)
S = 110; F = ImageFont.truetype(r'C:\Windows\Fonts\malgunbd.ttf', 12)
comp = json.load(open(os.path.join(D, 'covers_try', 'comp', 'comp.json'), encoding='utf-8'))['files'][:5]
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1080, 'height': 1080})
    for n in names:
        html = os.path.join(D, 'covers_try', n + '.html')
        HX = HT.replace('background:#0F1B3D', 'background:#FFD43B').replace('color:#A5B4D4','color:#0F1B3D') if n in ('G12','I7','I8','I9','I10') else (HT.replace('background:#0F1B3D', 'background:#D7261E').replace('color:#A5B4D4','color:#FFE3E0') if n=='G16' else (HT.replace('background:#0F1B3D', 'background:#1F4FD8').replace('color:#A5B4D4','color:#DCE6FF') if n=='G17' else HT))
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
