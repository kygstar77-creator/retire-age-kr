# cma1017 표지 — sbdep1017 cover_try 틀(남색 카드)
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
SRC = '한국투자증권·신한투자증권 CMA 안내 · 예금자보호법 제2조·시행령 제3조 · 10월 17일 조회'
V_ = {
 'A1': [('증권사 CMA 통장', 100, Wt, 't'), ('예금자보호 안 됩니다', 124, Y, 't'), ('RP형 2.5% · 발행어음형 2.85%', 82, Wt, 't')],
 'A2': [('CMA에 퇴직금 넣으면', 100, Wt, 't'), ('예금자보호 0원', 130, Y, 't'), ('종금형 CMA만 예외', 92, Wt, 't')],
 'A4': [('CMA 예금자보호', 104, Wt, 't'), ('RP형도 발행어음형도 X', 112, Y, 't'), ('예수금·종금형 CMA는 O', 92, Wt, 't')],
 'A5': [('CMA 예금자보호', 104, Wt, 't'), ('RP형도 발행어음형도 X', 112, Y, 't'), ('주식 계좌 현금·종금형은 O', 86, Wt, 't')],
 'A3': [('CMA 예금자보호', 104, Wt, 't'), ('RP형도 발행어음형도 X', 112, Y, 't'), ('주식 계좌 예수금은 O', 96, Wt, 't')],
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
