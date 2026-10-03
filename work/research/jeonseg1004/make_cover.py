# jeonseg1004 대표사진 1080x1080 — offimkt_ic0929(남색 카드) 틀 그대로. firemap-write 2026-10-02 23:3x
import os, sys
sys.stdout.reconfigure(encoding='utf-8')
V = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'visual', 'cafe-covers-1002'); sys.path.insert(0, V)
import make_covers as MC
from playwright.sync_api import sync_playwright
MC.HTML = (MC.HTML.replace('background:#F7F8FA', 'background:#0F1B3D').replace('.stamp{', '.stamp{display:none;')
           .replace('color:#6B7280', 'color:#A5B4D4').replace('top:196px', 'top:96px'))
Y, Wt = '#FFD43B', '#FFFFFF'
MC.COV['jeonseg1004'] = dict(stamp='',
    rows=[('전세보증보험 한도', 92, Wt, 't'), ('공시가격 2억 빌라', 120, Wt, 't'), ('2억5,200|만원', 240, Y, 'num'), ('공시가격의 126%까지', 104, Wt, 't')],
    src='주택도시보증공사 전세보증금반환보증 상품개요 · 2026-10-03 조회', keep_orig=False,
    check=['전세보증보험', '2억5,200', '126%'])
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1080, 'height': 1080}); MC.make('jeonseg1004', pg); b.close()
