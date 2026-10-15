# toheo1016 표지 — didim1012 cover_try 틀(남색 카드)
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
SRC = ' '
V_ = {
 'K1': [('서울 토지거래허가 신청', 105, Wt, 't'), ('9월 다시 늘었는데', 115, Wt, 't'), ('같은 단지 실거래는 0.56%', 100, Y, 't')],
 'K2': [('토허 신청 24% 늘었다', 120, Wt, 't'), ('같은 단지 실제 계약값은', 100, Wt, 't'), ('8월보다 0.56%↑', 150, Y, 't')],
 'K4': [('서울 토지거래허가 신청가격', 92, Wt, 't'), ('8월 신청 +0.44%', 130, Wt, 't'), ('9월 실제 계약 +0.56%', 115, Y, 't')],
 'K5': [('토허 신청가격 vs 실제 계약값', 92, Wt, 't'), ('서남권만 거꾸로', 150, Y, 't'), ('신청 -0.46% · 계약 +0.40%', 95, Wt, 't')],
 'K6': [('서울 토허 신청가격 8월 +0.44%', 88, Wt, 't'), ('9월 실제 계약값은?', 135, Y, 't'), ('같은 단지·평형 463곳 맞대 보니', 84, Wt, 't')],
 'K7': [('서울 토지거래허가 신청가격 8월 +0.44%', 78, Wt, 't'), ('9월 실제 계약값은?', 135, Y, 't'), ('같은 단지·평형 463곳 맞대 보니', 84, Wt, 't')],
 'K3': [('서울 토지거래허가 신청가격', 92, Wt, 't'), ('9월 1.43%↑', 150, Y, 't'), ('같은 단지 실거래는 0.56%↑', 92, Wt, 't')],
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
