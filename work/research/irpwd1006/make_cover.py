# irpwd1006 대표사진 1080x1080 — offimkt_ic0929(남색 카드) 틀 그대로. firemap-write 2026-10-02 23:3x
import os, sys
sys.stdout.reconfigure(encoding='utf-8')
V = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'visual', 'cafe-covers-1002'); sys.path.insert(0, V)
import make_covers as MC
from playwright.sync_api import sync_playwright
MC.HTML = (MC.HTML.replace('background:#F7F8FA', 'background:#0F1B3D').replace('.stamp{', '.stamp{display:none;')
           .replace('color:#6B7280', 'color:#A5B4D4').replace('top:196px', 'top:96px'))
Y, Wt = '#FFD43B', '#FFFFFF'
MC.COV['irpwd1006'] = dict(stamp='',
    rows=[('IRP 퇴직금 아파서 꺼내면', 100, Y, 't'), ('집 살 때보다 세금', 128, Wt, 't'), ('30|% 덜', 300, Y, 'num'), ('IRP 중도인출 세금 비교', 84, Wt, 't')],
    src='퇴직금 2억·근속 15년 계산 · 소득세법 제129조·시행령 제20조의2', keep_orig=False,
    check=['30', '아파서'])
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1080, 'height': 1080}); MC.make('irpwd1006', pg); b.close()
