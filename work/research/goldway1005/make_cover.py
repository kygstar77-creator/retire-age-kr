# goldway1005 대표사진 1080x1080 — offimkt_ic0929(남색 카드) 틀 그대로. firemap-write 2026-10-02 23:3x
import os, sys
sys.stdout.reconfigure(encoding='utf-8')
V = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'visual', 'cafe-covers-1002'); sys.path.insert(0, V)
import make_covers as MC
from playwright.sync_api import sync_playwright
MC.HTML = (MC.HTML.replace('background:#F7F8FA', 'background:#0F1B3D').replace('.stamp{', '.stamp{display:none;')
           .replace('color:#6B7280', 'color:#A5B4D4').replace('top:196px', 'top:96px'))
Y, Wt = '#FFD43B', '#FFFFFF'
MC.COV['goldway1005'] = dict(stamp='',
    rows=[('국제 금값 +3%', 124, Wt, 't'), ('KRX 금시장은', 124, Y, 't'), ('-2.4|%', 380, Y, 'num'), ('1년 전 웃돈 7%가 1%로', 76, '#A5B4D4', 't')],
    src='KRX 금 일별 종가 · KB 골드뱅킹 고시', keep_orig=False,
    check=['KRX', '2.4%'])
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1080, 'height': 1080}); MC.make('goldway1005', pg); b.close()
