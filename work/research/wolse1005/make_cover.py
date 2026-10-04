# wolse1005 대표사진 1080x1080 — offimkt_ic0929(남색 카드) 틀 그대로. firemap-write 2026-10-02 23:3x
import os, sys
sys.stdout.reconfigure(encoding='utf-8')
V = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'visual', 'cafe-covers-1002'); sys.path.insert(0, V)
import make_covers as MC
from playwright.sync_api import sync_playwright
MC.HTML = (MC.HTML.replace('background:#F7F8FA', 'background:#0F1B3D').replace('.stamp{', '.stamp{display:none;')
           .replace('color:#6B7280', 'color:#A5B4D4').replace('top:196px', 'top:96px')
           .replace('let s=parseFloat(n.style.fontSize);while(', 'let s=n?parseFloat(n.style.fontSize):0;while(n&&'))
Y, Wt = '#FFD43B', '#FFFFFF'
MC.COV['wolse1005'] = dict(stamp='',
    rows=[('월세 세액공제 정부안', 96, Wt, 't'), ('월세 월 100만원 공제액', 80, Wt, 't'), ('170만원 → 204만원', 96, Y, 't'), ('5,500만원 이하 · 국회 심의 전', 72, Y, 't')],
    src='조세특례제한법 제95조의2 · 정책브리핑 2026-08-13', keep_orig=False,
    check=['월세', '204', '170'])
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1080, 'height': 1080}); MC.make('wolse1005', pg); b.close()
