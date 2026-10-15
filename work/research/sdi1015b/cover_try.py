# sdi1015b 표지 (c1cafe1011 틀) — netpay1011 cover_try 틀(남색 카드)
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
SRC = '한국거래소 종가 2026.10.15 · DART 배당 공시 · 전망 아님'
V_ = {
 'K1': [('코스피 엿새 -14%', 115, Wt, 't'), ('삼성SDI는 +11.7%', 125, Y, 't'), ('1년 고점보다 17% 아래', 85, Wt, 't')],
 'K2': [('삼성SDI 1년 고점 대비', 100, Wt, 't'), ('-17.0%', 330, Y, 't'), ('1년 전보다는 2.7배', 95, Wt, 't')],
 'K3': [('삼성SDI 1년 전 22만원', 100, Wt, 't'), ('지금 59만 1천원', 125, Y, 't'), ('배당은 3년 쉬는 중', 105, Wt, 't')],
 'M1': [('삼성SDI 올해 고점보다', 105, Wt, 't'), ('24% 아래', 230, Y, 't'), ('배당은 3년 쉬기로', 100, Wt, 't')],
 'M2': [('삼성SDI 1년 전 22만원', 100, Wt, 't'), ('지금 59만 1천원', 125, Y, 't'), ('올해 고점보다 17% 아래', 88, Wt, 't')],
 'M3': [('삼성SDI 1년 새 2.7배', 115, Wt, 't'), ('올해 고점보다 -17%', 118, Y, 't'), ('배당은 3년 쉬는 중', 100, Wt, 't')],
 'K4': [('코스피 엿새 -14%', 110, Wt, 't'), ('삼성SDI +11.7%', 130, Y, 't'), ('1년 범위 속 75% 자리', 90, Wt, 't')],
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
