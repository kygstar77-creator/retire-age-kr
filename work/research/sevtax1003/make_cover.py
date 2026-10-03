# sevtax1003 대표사진 1080x1080 — offimkt_ic0929(남색 카드) 틀 그대로. firemap-write 2026-10-02 23:3x
import os, sys
sys.stdout.reconfigure(encoding='utf-8')
V = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'visual', 'cafe-covers-1002'); sys.path.insert(0, V)
import make_covers as MC
from playwright.sync_api import sync_playwright
MC.HTML = (MC.HTML.replace('background:#F7F8FA', 'background:#0F1B3D').replace('.stamp{', '.stamp{display:none;')
           .replace('color:#6B7280', 'color:#A5B4D4').replace('top:196px', 'top:96px'))
Y, Wt = '#FFD43B', '#FFFFFF'
MC.COV['sevtax1003'] = dict(stamp='',
    rows=[('퇴직금 1억원 세금', 92, Wt, 't'), ('5년 다니면', 136, Y, 't'), ('1,036|만원', 300, Y, 'num'), ('30년이면 26만원', 112, Wt, 't')],
    src='소득세법 제48·55조로 계산 · 지방소득세 포함 · 일시금 기준', keep_orig=False,
    check=['퇴직금', '1,036', '26만원'])
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1080, 'height': 1080}); MC.make('sevtax1003', pg); b.close()
