# bpcut1016 표지
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
SRC = '2026년 기준 · 혼자 받는 경우 · A급여가 작으면 더 받음 · 기초연금 누리집 산식'
V_ = {
 'S1': [('국민연금 55만이든 65만이든', 88, Wt, 't'), ('혼자 받을 때 기초연금 더하면', 96, Wt, 't'), ('합계 87만 4천원부터', 132, Y, 't')],
 'S2': [('기초연금 국민연금 감액', 92, Wt, 't'), ('국민연금 60만원이면', 120, Wt, 't'), ('기초연금 27만 4천원', 140, Y, 't')],
 'S5': [('기초연금 국민연금 감액', 92, Wt, 't'), ('국민연금 60만원이면', 132, Wt, 't'), ('기초연금 27만 4천원쯤', 136, Y, 't')],
 'S6': [('국민연금 52만원 넘으면 감액', 88, Wt, 't'), ('60만원 받는 분 기초연금', 118, Wt, 't'), ('27만 4천원쯤', 160, Y, 't')],
 'S7': [('국민연금 60만원이면', 150, Wt, 't'), ('기초연금은', 150, Wt, 't'), ('얼마 깎일까?', 190, Y, 't')],
 'S8': [('국민연금 늘면', 160, Wt, 't'), ('기초연금 깎여서', 150, Wt, 't'), ('합계는 얼마?', 190, Y, 't')],
 'S3': [('국민연금 52만원 넘으면', 92, Wt, 't'), ('기초연금이 줄어든 만큼', 110, Wt, 't'), ('합계는 87만원 그대로', 130, Y, 't')],
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
