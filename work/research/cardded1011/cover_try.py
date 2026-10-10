# cardded1011 표지 — netpay1011 cover_try 틀(남색 카드)
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
SRC = '조세특례제한법 제126조의2 · 1~9월 신용카드 기준'
V_ = {
 'P1': [('신용카드 소득공제', 140, Wt, 't'), ('10월에 체크카드로 바꿔도', 105, Wt, 't'), ('0원인 사람이 있어요', 115, Y, 't')],
 'P2': [('신용카드 소득공제', 140, Wt, 't'), ('체크카드로 바꾸면', 115, Wt, 't'), ('+67만원? 0원?', 135, Y, 't')],
 'P3': [('신용카드 소득공제', 140, Wt, 't'), ('한도 찼으면', 125, Wt, 't'), ('체크카드도 0원', 130, Y, 't')],
 'P4': [('신용카드 소득공제', 140, Wt, 't'), ('체크카드로 바꿔도', 135, Wt, 't'), ('공제 +0원인 사람', 140, Y, 't')],
 'P5': [('신용카드 소득공제', 140, Wt, 't'), ('체크카드로 바꿔도', 135, Wt, 't'), ('공제 그대로인 사람', 130, Y, 't')],
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
