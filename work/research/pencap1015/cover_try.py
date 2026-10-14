# pencap1015 표지 (c1cafe1011 틀) — netpay1011 cover_try 틀(남색 카드)
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
SRC = '소득세법(2026.1.1 시행) 계산 · 1인 가구 · 다른 공제 없음'
V_ = {
 'K1': [('연금저축·IRP', 120, Wt, 't'), ('연봉 3천만원은', 135, Wt, 't'), ('321만원까지만 공제', 105, Y, 't')],
 'K2': [('900만원 다 채워도', 120, Wt, 't'), ('연봉 3천만원이면', 130, Wt, 't'), ('579만원은 환급 0원', 105, Y, 't')],
 'K4': [('900만원 다 채워도', 120, Wt, 't'), ('연봉 3천만원이면', 130, Wt, 't'), ('579만원은 세금 그대로', 98, Y, 't')],
 'K5': [('연금저축·IRP 공제', 115, Wt, 't'), ('연봉 3천만원은', 135, Wt, 't'), ('321만원 넘게 넣어도 그대로', 80, Y, 't')],
 'K3': [('연금저축 세액공제', 120, Wt, 't'), ('연봉별 상한', 150, Wt, 't'), ('3천만원 321만 · 4천 900만', 85, Y, 't')],
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
