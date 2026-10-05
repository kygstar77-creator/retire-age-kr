# hfguar1006 대표사진 1080x1080 — offimkt_ic0929(남색 카드) 틀 그대로. firemap-write 2026-10-02 23:3x
import os, sys
sys.stdout.reconfigure(encoding='utf-8')
V = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'visual', 'cafe-covers-1002'); sys.path.insert(0, V)
import make_covers as MC
from playwright.sync_api import sync_playwright
MC.HTML = (MC.HTML.replace('background:#F7F8FA', 'background:#0F1B3D').replace('.stamp{', '.stamp{display:none;')
           .replace('color:#6B7280', 'color:#A5B4D4').replace('top:196px', 'top:96px').replace('justify-content:space-between','justify-content:center;gap:44px').replace('font:700 27px PD','font:700 56px PD')
           .replace('let s=parseFloat(n.style.fontSize);while(', 'let s=n?parseFloat(n.style.fontSize):0;while(n&&'))
Y, Wt = '#FFD43B', '#FFFFFF'
MC.COV['hfguar1006'] = dict(stamp='',
    rows=[('주택연금 보증료, 개편 뒤', 96, Wt, 't'), ('12년째부터', 170, Y, 't'), ('더 쌓여요', 170, Y, 't')],
    src='11년까진 덜 쌓임 · 65세·4억 집', keep_orig=False,
    check=['11년', '12년째']
)
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1080, 'height': 1080}); MC.make('hfguar1006', pg); b.close()
