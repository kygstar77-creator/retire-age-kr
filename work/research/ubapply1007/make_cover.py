# ubapply1007 대표사진 1080x1080 — offimkt_ic0929(남색 카드) 틀 그대로. firemap-write 2026-10-02 23:3x
import os, sys
sys.stdout.reconfigure(encoding='utf-8')
V = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'visual', 'cafe-covers-1002'); sys.path.insert(0, V)
import make_covers as MC
from playwright.sync_api import sync_playwright
MC.HTML = (MC.HTML.replace('background:#F7F8FA', 'background:#0F1B3D').replace('.stamp{', '.stamp{display:none;')
           .replace('color:#6B7280', 'color:#A5B4D4').replace('top:196px', 'top:96px').replace('justify-content:space-between','justify-content:center;gap:44px'))
Y, Wt = '#FFD43B', '#FFFFFF'
MC.COV['ubapply1007'] = dict(stamp='',
    rows=[('실업급여 신청을 4개월 미루면', 80, Wt, 't'), ('35|일', 300, Y, 'num'), ('못 받아요 · 270일 받는 분 예시', 64, Wt, 't')],
    src='', keep_orig=False,
    check=['35'])
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1080, 'height': 1080}); MC.make('ubapply1007', pg); b.close()
