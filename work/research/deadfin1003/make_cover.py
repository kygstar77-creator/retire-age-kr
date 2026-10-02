# deadfin1003 대표사진 1080x1080 — offimkt_ic0929(남색 카드) 틀 그대로. firemap-write 2026-10-02 23:3x
import os, sys
sys.stdout.reconfigure(encoding='utf-8')
V = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'visual', 'cafe-covers-1002'); sys.path.insert(0, V)
import make_covers as MC
from playwright.sync_api import sync_playwright
MC.HTML = (MC.HTML.replace('background:#F7F8FA', 'background:#0F1B3D').replace('.stamp{', '.stamp{display:none;')
           .replace('color:#6B7280', 'color:#A5B4D4').replace('top:196px', 'top:96px'))
Y, Wt = '#FFD43B', '#FFFFFF'
MC.COV['deadfin1003'] = dict(stamp='',
    rows=[('사망자 계좌 정지', 92, Wt, 't'), ('장례비는', 136, Y, 't'), ('장례식장', 250, Y, 'num'), ('으로 바로 가요', 112, Wt, 't')],
    src='금융위원회·행정안전부 보도자료 2026.9.7 · 9월 11일부터 전 금융권', keep_orig=False,
    check=['사망자 계좌 정지', '장례식장'])
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1080, 'height': 1080}); MC.make('deadfin1003', pg); b.close()
