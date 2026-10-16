# kospidrop1017 표지
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
SRC = '한국은행 ECOS 코스피 일별 종가 · 1997.1~2026.10.15'
V_ = {
 'K1': [('코스피 하루 7% 넘게 빠진 날', 92, Wt, 't'), ('1년 뒤 16번 중', 120, Wt, 't'), ('11번은 올라 있었다', 120, Y, 't')],
 'K3': [('코스피 7% 넘게 빠진 날 샀다면', 92, Wt, 't'), ('1년 뒤 16번 중 11번', 120, Wt, 't'), ('산 값보다 올라 있었다', 120, Y, 't')],
 'K4': [('코스피 7% 넘게 빠진 날 산 뒤 1년', 84, Wt, 't'), ('오른 때 11번', 170, Y, 't'), ('손해 5번', 170, Wt, 't')],
 'K2': [('코스피 하루 7% 급락 24번', 92, Wt, 't'), ('한 달 뒤엔 반반', 130, Wt, 't'), ('1년 뒤엔 16번 중 11번 ↑', 100, Y, 't')],
}
names = sys.argv[1:] or list(V_)
S = 110; F = ImageFont.truetype(r'C:\Windows\Fonts\malgunbd.ttf', 12)
os.makedirs(os.path.join(D,'covers_try'),exist_ok=True)
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
    b.close()
