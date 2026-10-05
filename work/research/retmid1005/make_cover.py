# retmid1005 대표사진 1080x1080 — offimkt_ic0929(남색 카드) 틀 그대로. firemap-write 2026-10-02 23:3x
import os, sys
sys.stdout.reconfigure(encoding='utf-8')
V = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'visual', 'cafe-covers-1002'); sys.path.insert(0, V)
import make_covers as MC
from playwright.sync_api import sync_playwright
MC.HTML = (MC.HTML.replace('background:#F7F8FA', 'background:#0F1B3D').replace('.stamp{', '.stamp{display:none;')
           .replace('color:#6B7280', 'color:#A5B4D4').replace('top:196px', 'top:96px').replace('justify-content:space-between','justify-content:center;gap:44px'))
Y, Wt = '#FFD43B', '#FFFFFF'
MC.COV['retmid1005'] = dict(stamp='',
    rows=[('퇴직금 중간정산 하면', 96, Wt, 't'), ('퇴직소득세 25|% 더 내요', 150, Y, 'num'), ('1억 5천만원 퇴직금 예시', 80, Wt, 't')],
    src='', keep_orig=False,
    check=['198', '25%'])
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1080, 'height': 1080}); MC.make('retmid1005', pg); b.close()
