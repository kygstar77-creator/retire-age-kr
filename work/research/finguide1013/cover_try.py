# finfile1013·finguide1013 표지 — reitetf1013 cover_try 틀(남색 카드). 사용: py -3.12 cover_try.py <file|guide> [이름...]
import os, sys
sys.stdout.reconfigure(encoding='utf-8')
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
V = os.path.join(R, 'visual', 'cafe-covers-1002'); sys.path.insert(0, V)
import make_covers as MC
from pathlib import Path
from PIL import Image
from playwright.sync_api import sync_playwright
HT = (MC.HTML.replace('background:#F7F8FA', 'background:#0F1B3D').replace('.stamp{', '.stamp{display:none;')
      .replace('color:#6B7280', 'color:#A5B4D4').replace('top:196px', 'top:96px')
      .replace('let s=parseFloat(n.style.fontSize);while(', 'let s=n?parseFloat(n.style.fontSize):0;while(n&&'))
Y, Wt = '#FFD43B', '#FFFFFF'
SETS = {
 'file': ('finfile1013', '카페 회원 자료 · 엑셀 파일 · 2026년 기준값', {
   'F1': [('회원 자료', 120, Wt, 't'), ('금융소득·건보료', 125, Y, 't'), ('판정 엑셀', 150, Wt, 't')],
   'F3': [('금융소득 2천만원', 125, Wt, 't'), ('건보료 1천만원', 135, Y, 't'), ('넘는지 판정 엑셀', 120, Wt, 't')],
   'F4': [('피부양자 탈락', 135, Wt, 't'), ('건보료·소득세', 140, Y, 't'), ('엑셀로 판정', 140, Wt, 't')],
   'F2': [('이자·배당 넣으면', 110, Wt, 't'), ('건보료·소득세', 135, Y, 't'), ('엑셀이 계산', 135, Wt, 't')],
 }),
 'guide': ('finguide1013', '2026년 기준값 · 엑셀 파일은 카페 회원 자료', {
   'G1': [('금융소득 2,400만원', 115, Wt, 't'), ('건보료 월 343,594원', 115, Y, 't'), ('더 내는 소득세 0원', 115, Wt, 't')],
   'G3': [('금융소득 2천만원', 125, Wt, 't'), ('넘으면 세금·건보료', 115, Y, 't'), ('엑셀로 계산', 140, Wt, 't')],
   'G4': [('이자·배당 넣으면', 120, Wt, 't'), ('세금·건보료·피부양자', 110, Y, 't'), ('엑셀로 계산', 140, Wt, 't')],
   'G2': [('종합과세·건보료', 130, Wt, 't'), ('한 장에 계산', 140, Y, 't'), ('엑셀 파일', 130, Wt, 't')],
 }),
}
which = sys.argv[1]; item, SRC, V_ = SETS[which]
D = os.path.join(R, item); os.makedirs(os.path.join(D, 'covers_try'), exist_ok=True)
names = sys.argv[2:] or list(V_)
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1080, 'height': 1080})
    for n in names:
        html = os.path.join(D, 'covers_try', n + '.html')
        open(html, 'w', encoding='utf-8').write(HT % dict(stamp='', src=SRC, f=MC.M.FONTS, rows=MC.rows_html(V_[n])))
        pg.goto(Path(html).as_uri()); pg.wait_for_selector('body[data-ready]')
        box = pg.evaluate("[...document.querySelectorAll('.k,.src')].map(e=>{const r=e.getBoundingClientRect();return [e.className,Math.round(r.right),Math.round(r.bottom)]})")
        print(n, box)
        out = os.path.join(D, 'covers_try', f'00_{n}.png'); pg.screenshot(path=out)
        Image.open(out).resize((168, 168), Image.LANCZOS).save(os.path.join(D, 'covers_try', f'00_{n}_168.png'))
    b.close()
