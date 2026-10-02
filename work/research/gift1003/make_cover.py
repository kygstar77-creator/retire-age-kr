# gift1003 대표사진 1080x1080 — deadfin1003 남색 틀 그대로. firemap-write 2026-10-03 04:2x
import os, sys
sys.stdout.reconfigure(encoding='utf-8')
V = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'visual', 'cafe-covers-1002'); sys.path.insert(0, V)
import make_covers as MC
from playwright.sync_api import sync_playwright
MC.HTML = (MC.HTML.replace('background:#F7F8FA', 'background:#0F1B3D').replace('.stamp{', '.stamp{display:none;')
           .replace('color:#6B7280', 'color:#A5B4D4').replace('top:196px', 'top:96px'))
Y, Wt = '#FFD43B', '#FFFFFF'
MC.COV['gift1003'] = dict(stamp='',
    rows=[('증여세 면제한도', 100, Wt, 't'), ('엄마·아빠·할머니', 112, Wt, 't'), ('합쳐서', 136, Y, 't'), ('5천만원', 230, Y, 'num')],
    src='상속세 및 증여세법 제53조 · 성인 10년 기준 · 2025.10.1 시행본', keep_orig=False,
    check=['증여세 면제한도', '5천만원'])
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1080, 'height': 1080}); MC.make('gift1003', pg); b.close()
