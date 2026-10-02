# offimkt_ic0929 대표사진 1080x1080 — garak0929(남색 카드, 평균 8) 틀 그대로. firemap-write 2026-10-02 22:5x
import os, sys
sys.stdout.reconfigure(encoding='utf-8')
V = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'visual', 'cafe-covers-1002'); sys.path.insert(0, V)
import make_covers as MC
from playwright.sync_api import sync_playwright
MC.HTML = (MC.HTML.replace('background:#F7F8FA', 'background:#0F1B3D').replace('.stamp{', '.stamp{display:none;')
           .replace('color:#6B7280', 'color:#A5B4D4').replace('top:196px', 'top:96px'))
Y, Wt = '#FFD43B', '#FFFFFF'
MC.COV['offimkt_ic0929'] = dict(stamp='',
    rows=[('인천 오피스텔 9월 신고 매매', 100, Wt, 't'), ('한 건물에서 하루에', 124, Y, 't'), ('59|채', 380, Y, 'num'), ('사는 쪽은 공공기관', 112, Wt, 't')],
    src='국토부 오피스텔 실거래 · 인천 2026년 9월 매매(9월 28일 계약분까지, 해제 제외)', keep_orig=True,
    check=['인천 오피스텔', '59채', '하루', '한 건물', '사는 쪽은 모두 공공기관'])
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1080, 'height': 1080}); MC.make('offimkt_ic0929', pg); b.close()
