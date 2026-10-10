# eitclate1009 표지 (deplend1009 틀) — yangdo1006 cover_try 틀 — 남색 카드 틀(hfguar1006 mc_h.py와 같은 방식). 결과 covers_try/00_<안>.png, 비교판 board_<안>.png
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
SRC = '조세특례제한법 · 늦어도 받는 날(법정 기한)'
V_ = {
 'I4': [('근로장려금', 170, Wt, 't'), ('하루 차이', 250, Wt, 't'), ('= 한 달', 330, Y, 't')],
 'I3': [('근로장려금 늦은 신청', 150, Wt, 't'), ('한 달 밀림', 320, Y, 't'), ('하루 차이로 지급 기한', 120, Wt, 't')],
 'I1': [('근로장려금 늦은 신청', 150, Wt, 't'), ('한|달', 430, Y, 'num'), ('하루 차이로 밀리는 지급 기한', 104, Wt, 't')],
 'I2': [('근로장려금 늦은 신청', 150, Wt, 't'), ('+1|달', 430, Y, 'num'), ('12월 1일에 내면 지급 기한', 110, Wt, 't')],
 'G1': [('근로장려금 기한 후 신청', 100, Wt, 't'), ('하루 늦으면 한|달', 170, Y, 'num'), ('늦어도 받는 날이 밀려요', 90, Wt, 't')],
 'G2': [('근로장려금 기한 후 신청', 100, Wt, 't'), ('11월 안에 내면|3월', 170, Y, 'num'), ('12월 1일에 내면 4월', 110, Wt, 't')],
 'G4': [('근로장려금 기한 후 신청', 100, Wt, 't'), ('11월에 내면 3월', 150, Y, 't'), ('12월 1일이면 4월', 140, Wt, 't'), ('늦어도 받는 날', 90, Y, 't')],
 'G5': [('근로장려금', 150, Y, 't'), ('11월 신청 → 3월', 160, Wt, 't'), ('12월 1일 → 4월', 160, Wt, 't')],
 'G6': [('근로장려금 늦은 신청', 110, Wt, 't'), ('11월 → 3월', 210, Y, 't'), ('12월 1일 → 4월', 150, Wt, 't')],
 'G7': [('근로장려금', 120, Wt, 't'), ('11월 신청 → 3월', 175, Y, 't'), ('12월 1일 → 4월', 150, '#7F8DB0', 't'), ('하루 차이로 한 달', 110, Wt, 't')],
 'G8': [('근로장려금 기한 후', 120, Y, 't'), ('11월에 내야', 220, Wt, 't'), ('12월 1일이면 한 달 밀림', 100, Y, 't')],
 'G9': [('근로장려금', 150, Y, 't'), ('11월 30일 vs', 150, Wt, 't'), ('12월 1일', 150, Wt, 't'), ('받는 기한 한 달 차이', 100, Y, 't')],
 'G10': [('근로장려금 늦은 신청', 110, Wt, 't'), ('11월 → 3월까지', 190, Y, 't'), ('12월 1일 → 4월까지', 130, Wt, 't')],
 'G11': [('근로장려금', 190, Y, 't'), ('11월 → 3월', 200, Wt, 't'), ('12월 1일 → 4월', 150, Wt, 't')],
 'G12': [('근로장려금', 190, '#0F1B3D', 't'), ('11월 → 3월', 200, '#0F1B3D', 't'), ('12월 1일 → 4월', 150, '#7A1F1F', 't')],
 'G13': [('근로장려금', 170, Y, 't'), ('하루 늦게 내면', 160, Wt, 't'), ('기한 한 달 뒤로', 160, Y, 't')],
 'G14': [('근로장려금', 150, Y, 't'), ('11월 30일 → 3월 30일', 100, Wt, 't'), ('12월 1일 → 4월 30일', 100, Wt, 't'), ('하루 차이, 기한은 한 달', 100, Y, 't')],
 'G15': [('근로장려금 기한 후 신청', 100, Wt, 't'), ('하루 차이', 220, Y, 't'), ('지급 기한은 한 달', 120, Wt, 't')],
 'G16': [('근로장려금', 190, Wt, 't'), ('11월 → 3월', 200, Y, 't'), ('12월 1일 → 4월', 150, Wt, 't')],
 'G17': [('근로장려금', 190, Y, 't'), ('11월 → 3월', 200, Wt, 't'), ('12월 1일 → 4월', 150, Wt, 't')],
 'G3': [('근로장려금', 140, Y, 't'), ('11월 30일 → 3월 30일', 120, Wt, 't'), ('12월 1일 → 4월 30일', 120, Y, 't'), ('늦어도 받는 날', 90, Wt, 't')],
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
