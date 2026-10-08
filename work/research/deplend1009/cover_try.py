# deplend1009 표지 (parking1007 틀) — yangdo1006 cover_try 틀 — 남색 카드 틀(hfguar1006 mc_h.py와 같은 방식). 결과 covers_try/00_<안>.png, 비교판 board_<안>.png
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
SRC = '우리은행 · 5천만원 1년 예금 · 만기 세후'
V_ = {
 'F1': [('예금 2천만원이 급할 때', 100, Wt, 't'), ('세후 이자 70→106|만원', 170, Y, 'num'), ('통째로 깨면 → 예금담보대출이면', 76, Wt, 't')],
 'F2': [('예금담보대출', 130, Y, 't'), ('이자 내고 써도', 100, Wt, 't'), ('통째 해지보다|+37만원', 190, Y, 'num'), ('우리은행 5천만원 예금 · 만기 세후', 76, Wt, 't')],
 'F3': [('정기예금 통째로 깨면', 110, Wt, 't'), ('698,230|원', 190, Y, 'num'), ('예금담보대출로 2천만원 쓰면', 86, Wt, 't'), ('1,064,061원', 110, Y, 't')],
 'F4': [('예금 안 깨고 쓰면', 120, Y, 't'), ('2천만원', 120, Wt, 't'), ('+37만|원', 190, Y, 'num'), ('통째로 깰 때보다 만기에 더 남아요', 76, Wt, 't')],
 'F5': [('예금 2천만원이 급할 때', 100, Wt, 't'), ('예금담보대출이 통째 해지보다', 86, Wt, 't'), ('+37만|원', 190, Y, 'num'), ('만기에 더 남아요', 96, Wt, 't')],
 'F6': [('예금담보대출', 130, Y, 't'), ('통째로 깨는 것과', 92, Wt, 't'), ('37만|원 차이', 190, Y, 'num'), ('예금 2천만원 쓸 때 · 우리은행', 80, Wt, 't')],
 'F8': [('예금 2천만원이 급할 때', 100, Wt, 't'), ('받는 이자 70→106|만원', 170, Y, 'num'), ('통째로 깰 때 → 담보대출 쓸 때', 96, Wt, 't')],
 'F9': [('예금 2천만원 급할 때', 110, Wt, 't'), ('받는 이자 70→106|만원', 170, Y, 'num'), ('깰 때 → 담보대출', 130, Wt, 't')],
 'F7': [('예금 2천만원이 급할 때', 100, Wt, 't'), ('통째로 깨면 70만원', 110, Wt, 't'), ('예금담보대출 106|만원', 150, Y, 'num'), ('만기에 남는 세후 이자', 86, Wt, 't')],
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
