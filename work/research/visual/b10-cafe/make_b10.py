# B10 카페 첫 글 대표 이미지(00)·히트맵 기준일 도장(01) — visual 2026-10-02 09:5x
#   py -3.12 work/research/visual/b10-cafe/make_b10.py
# 왜: 기존 00(900x400)은 '60.9%'가 왼쪽 절반에 있어 목록 썸네일이 가운데 정사각형으로 잘리면 숫자가 잘린다(자르는 방식은 확인 안 함 → 정사각형으로 안전하게).
#     1초 시험: 168px에서 '무슨 숫자인지(서울 전세가율 1위 금천)'가 읽혀야 한다. 숫자 1개 크게, 기준일 도장.
# 숫자: b10cafe1002/undervalue_out.txt 금천구 60.9%·강남구 35.9%(2026년 7~9월, 같은 단지·같은 면적대 짝)
import os, re, sys, shutil
from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image, ImageDraw, ImageFont
sys.stdout.reconfigure(encoding='utf-8')
H = os.path.dirname(os.path.abspath(__file__)); R = os.path.join(H, '..', '..')
B10 = os.path.join(R, 'b10cafe1002'); IMG = os.path.join(B10, 'pkg', 'img')
rows = {m[1]: float(m[2]) for m in re.finditer(r'(\S+구) \| [\d,]+ \| [\d,]+ \| \d+ \| ([\d.]+)%', open(os.path.join(B10, 'undervalue_out.txt'), encoding='utf-8').read())}
assert rows['금천구'] == 60.9 and rows['강남구'] == 35.9 and max(rows, key=rows.get) == '금천구' and min(rows, key=rows.get) == '강남구'
FONTS = Path(r'C:/Windows/Fonts').as_uri()
VF = os.path.join(R, 'visual', 'E-1-thumb')
sys.path.insert(0, VF); import make_thumbs as M
HTML = """<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{font-family:BH;src:url('file:///%(f)s/BlackHanSans.ttf')}
@font-face{font-family:PD;src:url('file:///%(f)s/pd700.ttf');font-weight:700}
*{margin:0;padding:0;box-sizing:border-box}
body{width:1080px;height:1080px;background:#F7F8FA;font-family:PD;position:relative;overflow:hidden}
.stamp{position:absolute;left:80px;top:80px;border:6px solid #1F2937;color:#1F2937;font:700 44px PD;padding:10px 26px;border-radius:14px;transform:rotate(-3deg)}
.k{position:absolute;left:80px;font-family:BH;color:#111827;line-height:1.05}
.src{position:absolute;left:80px;bottom:70px;font:700 30px PD;color:#6B7280}
</style></head><body>
<div class='stamp'>2026년 7~9월 실거래</div>
<div class='k' style='top:230px;font-size:96px'>서울 아파트 전세가율</div>
<div class='k' style='top:350px;font-size:120px'>가장 높은 <span style='color:#1D4ED8'>금천</span></div>
<div class='k' style='top:480px;font-size:330px;color:#1D4ED8;letter-spacing:-8px'>60.9%%</div>
<div class='k' style='top:830px;font-size:72px;color:#6B7280'>가장 낮은 강남 35.9%%</div>
<div class='src'>국토교통부 실거래 · 같은 단지·같은 면적대 짝 · 25개 구</div>
<script>document.fonts.ready.then(()=>document.body.dataset.ready=1)</script></body></html>"""
html = os.path.join(H, '00.html'); open(html, 'w', encoding='utf-8').write(HTML % {'f': M.FONTS})
if not os.path.exists(os.path.join(IMG, '00_orig.png')): shutil.copy(os.path.join(IMG, '00.png'), os.path.join(IMG, '00_orig.png'))
if not os.path.exists(os.path.join(IMG, '01_orig.png')): shutil.copy(os.path.join(IMG, '01.png'), os.path.join(IMG, '01_orig.png'))
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1080, 'height': 1080})
    pg.goto(Path(html).as_uri()); pg.wait_for_selector('body[data-ready]')
    w = pg.evaluate("Math.max(...[...document.querySelectorAll('.k,.src,.stamp')].map(e=>e.getBoundingClientRect().right))")
    assert w <= 1040, f'넘침 {w}'
    pg.screenshot(path=os.path.join(IMG, '00.png')); b.close()
im = Image.open(os.path.join(IMG, '00.png')); im.resize((168, 168), Image.LANCZOS).save(os.path.join(H, '00_168.png'))
# 01 히트맵: 제목 줄 오른쪽 빈 자리에 기준일 도장
hm = Image.open(os.path.join(IMG, '01_orig.png')).convert('RGB'); d = ImageDraw.Draw(hm)
f = ImageFont.truetype(r'C:\Windows\Fonts\malgunbd.ttf', 26); t = '기준 2026.7~9월 · 10.1 수집'
tw = d.textlength(t, font=f); x1 = hm.width - 20; x0 = x1 - tw - 32
d.rounded_rectangle((x0, 14, x1, 60), radius=10, outline='#FFD60A', width=3); d.text((x0 + 16, 21), t, fill='#FFD60A', font=f)
hm.save(os.path.join(IMG, '01.png'))
print('00', Image.open(os.path.join(IMG, '00.png')).size, '01', hm.size)
