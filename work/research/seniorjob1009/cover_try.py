# hometown1009 표지 (deplend1009 틀) — yangdo1006 cover_try 틀 — 남색 카드 틀(hfguar1006 mc_h.py와 같은 방식). 결과 covers_try/00_<안>.png, 비교판 board_<안>.png
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
SRC = '생활법령정보 노인 일자리 지원 (2026.9.15 기준)'
V_ = {
 'N1': [('노인일자리 신청', 140, Wt, 't'), ('생계급여 받으면', 120, Wt, 't'), ('선발에서 빠져요', 140, Y, 't')],
 'N3': [('노인일자리 신청', 140, Wt, 't'), ('생계급여 받으면', 120, Wt, 't'), ('선발 제외 유형 있어요', 110, Y, 't')],
 'N4': [('노인일자리 신청', 140, Wt, 't'), ('생계급여·직장가입자는', 100, Wt, 't'), ('선발 제외 유형 있어요', 120, Y, 't')],
 'N5': [('노인일자리 신청', 140, Wt, 't'), ('생계급여 받으면', 120, Wt, 't'), ('취업지원 유형만 돼요', 115, Y, 't')],
 'N6': [('노인일자리', 150, Wt, 't'), ('생계급여·직장가입자', 100, Wt, 't'), ('취업지원 유형만 가능', 115, Y, 't')],
 'N7': [('노인일자리', 160, Wt, 't'), ('생계급여 받으면', 125, Wt, 't'), ('공익활동은 선발 제외', 115, Y, 't')],
 'N9': [('노인일자리', 160, Wt, 't'), ('생계급여 받는 분', 125, Wt, 't'), ('취업지원 빼고 선발 제외', 100, Y, 't')],
 'N10': [('노인일자리', 160, Wt, 't'), ('생계급여 받는 분', 125, Wt, 't'), ('취업지원만 선발 가능', 115, Y, 't')],
 'N2': [('노인일자리', 140, Wt, 't'), ('직장가입자면', 130, Wt, 't'), ('선발 제외', 170, Y, 't')],
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
