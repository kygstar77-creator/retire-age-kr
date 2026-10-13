# dcpension1014 표지 — cheongyak1012 cover_try 틀
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
SRC = '마지막 5년 연봉 80% 예시 · 첫해 연봉 5,000만원 · 20년 근속 · 원리금보장 3.09% 단순 계산'
V_ = {
 'K4': [('퇴직연금 DC형', 135, Wt, 't'), ('연봉 5천·임금피크 예시', 105, Wt, 't'), ('전환하면 +3,605만원', 115, Y, 't')],
 'K5': [('퇴직연금 DC형 전환', 120, Wt, 't'), ('임금피크 예시 계산', 115, Wt, 't'), ('DB형보다 3,605만원↑', 110, Y, 't')],
 'K1': [('퇴직연금 DB형 vs DC형', 105, Wt, 't'), ('누가 더 받나', 130, Wt, 't'), ('기준은 내 월급 인상률', 105, Y, 't')],
 'K2': [('퇴직연금 DC형', 135, Wt, 't'), ('수익률 < 월급 인상률이면', 95, Wt, 't'), ('DB형보다 적게 받는다', 110, Y, 't')],
 'K3': [('퇴직연금 DC형', 135, Wt, 't'), ('임금피크 앞두고 바꾸면', 105, Wt, 't'), ('+3,605만원', 140, Y, 't')],
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
