# costchk1016 표지 — pencap1015 cover_try 틀(남색 카드)
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
SRC = '도시정비법 제29조의2 · 한국은행 생산자물가지수 · 공사비 산정 기준일 2023년 8월 예시'
V_ = {
 'K1': [('재건축 공사비 15% 올라도', 92, Wt, 't'), ('물가 몫 빼면', 140, Wt, 't'), ('3.75%만 남는 계약', 110, Y, 't')],
 'K2': [('공사비 검증 의무', 120, Wt, 't'), ('15% 증액도 물가 빼면', 100, Wt, 't'), ('3.75%라 대상 아님', 105, Y, 't')],
 'K4': [('재건축 공사비 15% 증액', 95, Wt, 't'), ('검증 의무 따질 땐', 125, Wt, 't'), ('물가 빼고 3.75%', 125, Y, 't')],
 'K5': [('2023년 8월 정한 공사비', 95, Wt, 't'), ('15% 올라도 물가 빼면', 105, Wt, 't'), ('검증 의무 기준 미달', 110, Y, 't')],
 'K6': [('2023년 8월 계약 15% 증액', 88, Wt, 't'), ('물가 빼면 3.75%', 135, Y, 't'), ('기준 5·10% 미달 의무 아님', 80, Wt, 't')],
 'K7': [('공사비 15% 올라도', 110, Wt, 't'), ('2023년 8월 계약은 물가 빼면', 75, Wt, 't'), ('3.75%라 검증 의무 없음', 95, Y, 't')],
 'K8': [('공사비 15% 올라도', 110, Wt, 't'), ('2023년 8월 기준 계약은 물가 빼면', 66, Wt, 't'), ('3.75%라 검증 의무 없음', 95, Y, 't')],
 'K3': [('재건축 공사비 검증', 115, Wt, 't'), ('15% 올라도', 160, Wt, 't'), ('의무 아닐 수 있다', 110, Y, 't')],
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
