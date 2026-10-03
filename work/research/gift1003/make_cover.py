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
    rows=[('증여세 면제한도', 100, Wt, 't'), ('엄마가 먼저 쓰면', 112, Wt, 't'), ('할머니 1억', 136, Y, 't'), ('세금 두 배', 230, Y, 'num')],
    src='630만 5천원 → 1,261만원 · 상속세 및 증여세법 · 성인 손주 기준', keep_orig=False,
    check=['증여세 면제한도', '두 배'])
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1080, 'height': 1080}); MC.make('gift1003', pg); b.close()
