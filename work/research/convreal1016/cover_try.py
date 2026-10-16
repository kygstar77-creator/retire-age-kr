# convreal1016 표지 — pencap1015 cover_try 틀(남색 카드)
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
SRC = '국토교통부 실거래가 · 서울 아파트 2026년 7~8월 새 계약 · 직접 계산'
V_ = {
 'S5': [('줄인 전세 보증금 1억원당', 90, Wt, 't'), ('월세 약 40만원', 150, Y, 't'), ('7~8월 새 계약 1,641곳의 중간값', 72, Wt, 't')],
 'S1': [('서울 아파트 월세 전환율', 96, Wt, 't'), ('가운데 값 4.8%', 150, Wt, 't'), ('법 상한은 5%', 140, Y, 't')],
 'S2': [('보증금 1억 월세로 돌리면', 96, Wt, 't'), ('실제 계약 약 40만원', 120, Wt, 't'), ('법 상한 약 42만원', 120, Y, 't')],
 'S4': [('서울 아파트 보증금 1억 줄이면', 82, Wt, 't'), ('월세 실제 약 40만원', 120, Wt, 't'), ('법 상한 약 42만원', 120, Y, 't')],
 'S3': [('전월세 전환율', 130, Wt, 't'), ('서울 실제 4.8%', 140, Wt, 't'), ('법 상한 5%', 140, Y, 't')],
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
