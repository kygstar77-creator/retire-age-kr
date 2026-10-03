# deposit1004 대표사진 1080x1080 — offimkt_ic0929(남색 카드) 틀 그대로. firemap-write 2026-10-02 23:3x
import os, sys
sys.stdout.reconfigure(encoding='utf-8')
V = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'visual', 'cafe-covers-1002'); sys.path.insert(0, V)
import make_covers as MC
from playwright.sync_api import sync_playwright
MC.HTML = (MC.HTML.replace('background:#F7F8FA', 'background:#0F1B3D').replace('.stamp{', '.stamp{display:none;')
           .replace('color:#6B7280', 'color:#A5B4D4').replace('top:196px', 'top:96px'))
Y, Wt = '#FFD43B', '#FFFFFF'
MC.COV['deposit1004'] = dict(stamp='',
    rows=[('정기예금 1년 기본금리', 92, Wt, 't'), ('국민은행 우대 빼면', 120, Y, 't'), ('2.40|%', 300, Y, 'num'), ('우대 다 채우면 3.50%', 104, Wt, 't')],
    src='금융감독원 금융상품한눈에 공시 · 2026-10-03 조회 · KB Star 정기예금 12개월', keep_orig=False,
    check=['정기예금', '2.40', '3.50%'])
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1080, 'height': 1080}); MC.make('deposit1004', pg); b.close()
