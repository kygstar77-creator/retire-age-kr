# nhisrent1005 대표사진 1080x1080 — offimkt_ic0929(남색 카드) 틀 그대로. firemap-write 2026-10-02 23:3x
import os, sys
sys.stdout.reconfigure(encoding='utf-8')
V = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'visual', 'cafe-covers-1002'); sys.path.insert(0, V)
import make_covers as MC
from playwright.sync_api import sync_playwright
MC.HTML = (MC.HTML.replace('background:#F7F8FA', 'background:#0F1B3D').replace('.stamp{', '.stamp{display:none;')
           .replace('color:#6B7280', 'color:#A5B4D4').replace('top:196px', 'top:96px')
           .replace('let s=parseFloat(n.style.fontSize);while(', 'let s=n?parseFloat(n.style.fontSize):0;while(n&&'))
Y, Wt = '#FFD43B', '#FFFFFF'
MC.COV['nhisrent1005'] = dict(stamp='',
    rows=[('집 있는 퇴직자 건강보험료', 84, Wt, 't'), ('집 없을 때 월 2만 2,800원', 76, Wt, 't'), ('과세표준 3억이면 월 16만 3,020원', 70, Y, 't'), ('소득 없을 때 · 장기요양 포함', 60, Wt, 't')],
    src='국민건강보험법 시행령 별표 4 대입 계산 · 2026년 기준', keep_orig=False,
    check=['건강보험료', '3억', '16만']
)
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1080, 'height': 1080}); MC.make('nhisrent1005', pg); b.close()
