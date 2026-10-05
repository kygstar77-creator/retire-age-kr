# yangdo1006 대표사진 1080x1080 — irpwd1006(남색 카드) 틀 그대로. firemap-write 2026-10-06
import os, sys
sys.stdout.reconfigure(encoding='utf-8')
V = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'visual', 'cafe-covers-1002'); sys.path.insert(0, V)
import make_covers as MC
from playwright.sync_api import sync_playwright
MC.HTML = (MC.HTML.replace('background:#F7F8FA', 'background:#0F1B3D').replace('.stamp{', '.stamp{display:none;')
           .replace('color:#6B7280', 'color:#A5B4D4').replace('top:196px', 'top:96px'))
Y, Wt = '#FFD43B', '#FFFFFF'
MC.COV['yangdo1006'] = dict(stamp='',
    rows=[('12억 넘는 1주택 양도세', 100, Y, 't'), ('2년 살았는지로 공제가', 112, Wt, 't'), ('30|%→80%', 230, Y, 'num'), ('장기보유특별공제 비교', 84, Wt, 't')],
    src='소득세법 제95조② 표1·표2 · 시행령 제159조의4', keep_orig=False,
    check=['80', '12억'])
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1080, 'height': 1080}); MC.make('yangdo1006', pg); b.close()
