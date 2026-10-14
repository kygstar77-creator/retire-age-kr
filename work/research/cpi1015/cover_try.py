# cpi1015 표지 — r1cafe_fx1014 cover_try 틀
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
SRC = '1년 전 대비 · 미국 노동통계국 CPI-U 2026년 9월'
V_ = {
 'C1': [('미국 CPI 9월 3.7%', 120, Wt, 't'), ('근원물가 2.6%', 95, Wt, 't'), ('에너지 20.4%', 95, Y, 't')],
 'C2': [('미국 CPI 3.7%', 125, Wt, 't'), ('식품·에너지 빼면 2.6%', 82, Wt, 't'), ('에너지만 보면 20.4%', 82, Y, 't')],
 'C4': [('미국 CPI 3.7%', 130, Wt, 't'), ('근원물가 2.6%', 100, Wt, 't'), ('에너지 1년 새 20.4%↑', 88, Y, 't')],
 'C5': [('미국 CPI 3.7%', 130, Wt, 't'), ('에너지 빼면 2.6%', 100, Wt, 't'), ('에너지는 20.4% 올라', 92, Y, 't')],
 'C3': [('미국 CPI 3.7%', 125, Wt, 't'), ('근원물가 2월 2.5% → 9월 2.6%', 66, Wt, 't'), ('에너지 2월 0.5% → 9월 20.4%', 66, Y, 't')],
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
