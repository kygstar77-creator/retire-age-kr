# schd1003 대표사진 1080x1080 — offimkt_ic0929(남색 카드) 틀 그대로. firemap-write 2026-10-02 23:3x
import os, sys
sys.stdout.reconfigure(encoding='utf-8')
V = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'visual', 'cafe-covers-1002'); sys.path.insert(0, V)
import make_covers as MC
from playwright.sync_api import sync_playwright
MC.HTML = (MC.HTML.replace('background:#F7F8FA', 'background:#0F1B3D').replace('.stamp{', '.stamp{display:none;')
           .replace('color:#6B7280', 'color:#A5B4D4').replace('top:196px', 'top:96px').replace('s>120){s-=6', 's>9999){s-=6'))
Y, Wt = '#FFD43B', '#FFFFFF'
MC.COV['schd1003'] = dict(stamp='',
    rows=[('SCHD 1년 동안', 92, Wt, 't'), ('주가 +18.6%', 130, Wt, 't'), ('배당은', 110, Y, 't'), ('+2.0|%', 300, Y, 'num')],
    src='슈왑 자산운용 분배금 내역 · 최근 1년 배당 합계 · 10월 1일 종가 기준', keep_orig=False,
    check=['SCHD', '18.6', '배당'])
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1080, 'height': 1080}); MC.make('schd1003', pg); b.close()
