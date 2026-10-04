# ltc1005 대표사진 1080x1080 — offimkt_ic0929(남색 카드) 틀 그대로. firemap-write 2026-10-02 23:3x
import os, sys
sys.stdout.reconfigure(encoding='utf-8')
V = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'visual', 'cafe-covers-1002'); sys.path.insert(0, V)
import make_covers as MC
from playwright.sync_api import sync_playwright
MC.HTML = (MC.HTML.replace('background:#F7F8FA', 'background:#0F1B3D').replace('.stamp{', '.stamp{display:none;')
           .replace('color:#6B7280', 'color:#A5B4D4').replace('top:196px', 'top:96px'))
Y, Wt = '#FFD43B', '#FFFFFF'
MC.COV['ltc1005'] = dict(stamp='',
    rows=[('장기요양보험료', 92, Wt, 't'), ('월급 300만원이면', 120, Wt, 't'), ('내 몫 월 1만|4,170원', 240, Y, 'num'), ('회사가 같은 금액 부담', 92, Wt, 't')],
    src='노인장기요양보험법 시행령 제4조·국민건강보험법 제76조 · 2026-10-05 조회', keep_orig=False,
    check=['장기요양', '4,170', '300만'])
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1080, 'height': 1080}); MC.make('ltc1005', pg); b.close()
