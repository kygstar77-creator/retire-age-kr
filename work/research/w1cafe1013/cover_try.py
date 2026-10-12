# w1cafe1013 표지 (c1cafe1011 틀) — netpay1011 cover_try 틀(남색 카드)
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
SRC = '삼성전자 100주 · 10월 2일→8일 · 세후 분기 배당 3만 1,640원 기준'
V_ = {
 'K1': [('삼성전자 100주', 140, Wt, 't'), ('사흘 평가액 -140만원', 120, Wt, 't'), ('분기 배당 44번치', 135, Y, 't')],
 'K4': [('삼성전자 100주', 140, Wt, 't'), ('사흘 평가액 -140만원', 120, Wt, 't'), ('배당금 44번치', 145, Y, 't')],
 'K2': [('실적 107조 나온 주', 125, Wt, 't'), ('삼성전자 100주는', 135, Wt, 't'), ('배당 44번치 빠짐', 130, Y, 't')],
 'K3': [('삼성전자 배당금', 140, Wt, 't'), ('100주 한 분기 3만원', 115, Wt, 't'), ('사흘에 44번치 빠짐', 120, Y, 't')],
}
V_OLD = {
 'K1': [('계약갱신 거절한 집에', 125, Wt, 't'), ('새 세입자가 들어왔다면', 115, Wt, 't'), ('배상금 최소 375만원', 125, Y, 't')],
 'K2': [('실거주라더니', 150, Wt, 't'), ('다른 세입자가?', 140, Wt, 't'), ('배상금 375만원부터', 120, Y, 't')],
 'K3': [('계약갱신청구권', 145, Wt, 't'), ('실거주 거절 뒤 재임대', 115, Wt, 't'), ('배상금 최소 375만원', 125, Y, 't')],
'K4': [('실거주라더니', 150, Wt, 't'), ('새 세입자가 들어왔다면', 115, Wt, 't'), ('전세 3억이면 375만원부터', 105, Y, 't')],
 'K5': [('계약갱신 거절한 집에', 125, Wt, 't'), ('새 세입자가 들어왔다면', 115, Wt, 't'), ('전세 3억이면 375만원부터', 105, Y, 't')],
'K6': [('실거주라더니', 150, Wt, 't'), ('다른 세입자가?', 140, Wt, 't'), ('전세 3억 배상금 375만원', 108, Y, 't')],
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
