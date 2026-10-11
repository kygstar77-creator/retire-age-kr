# c1cafe1011 표지 — netpay1011 cover_try 틀(남색 카드)
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
SRC = '미국 세금 + 지역가입자 건보료, 첫해 기준'
V_ = {
 'K1': [('S&P500 3억에서', 140, Wt, 't'), ('매달 200만원 꺼내면', 125, Wt, 't'), ('배당 쪽 9년째 바닥', 125, Y, 't')],
 'K2': [('배당으로 받을까', 140, Wt, 't'), ('팔아서 쓸까', 150, Wt, 't'), ('3억 월 200만원 37년 돌려 봄', 95, Y, 't')],
 'K4': [('S&P500 3억 월 200만원', 112, Wt, 't'), ('2000년에 시작했다면', 125, Wt, 't'), ('배당 쪽 9년째 바닥', 125, Y, 't')],
 'K5': [('같은 3억 월 200만원', 125, Wt, 't'), ('배당이 팔기보다', 140, Wt, 't'), ('첫해 722만원 더 나감', 120, Y, 't')],
 'K3': [('같은 3억 월 200만원', 125, Wt, 't'), ('배당 쪽만', 150, Wt, 't'), ('첫해 722만원 더 나감', 120, Y, 't')],
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
