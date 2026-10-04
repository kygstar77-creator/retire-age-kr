# npsfee1005 대표사진 1080x1080 — offimkt_ic0929(남색 카드) 틀 그대로. firemap-write 2026-10-02 23:3x
import os, sys
sys.stdout.reconfigure(encoding='utf-8')
V = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'visual', 'cafe-covers-1002'); sys.path.insert(0, V)
import make_covers as MC
from playwright.sync_api import sync_playwright
MC.HTML = (MC.HTML.replace('background:#F7F8FA', 'background:#0F1B3D').replace('.stamp{', '.stamp{display:none;')
           .replace('color:#6B7280', 'color:#A5B4D4').replace('top:196px', 'top:96px'))
Y, Wt = '#FFD43B', '#FFFFFF'
MC.COV['npsfee1005'] = dict(stamp='',
    rows=[('월 소득 300만원 직장인', 96, Wt, 't'), ('국민연금 보험료 내 몫', 96, Wt, 't'), ('142,500|원', 250, Y, 'num'), ('회사와 절반씩 · 전체 285,000원', 76, Wt, 't')],
    src='2026년 9.5% · 국민연금법 부칙 제4조 · 2026-10-05 조회', keep_orig=False,
    check=['국민연금', '142,500', '285,000', '300만'])
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1080, 'height': 1080}); MC.make('npsfee1005', pg); b.close()
