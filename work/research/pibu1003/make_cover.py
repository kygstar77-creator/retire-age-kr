# pibu1003 대표사진 1080x1080 — offimkt_ic0929(남색 카드) 틀 그대로. firemap-write 2026-10-02 23:3x
import os, sys
sys.stdout.reconfigure(encoding='utf-8')
V = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'visual', 'cafe-covers-1002'); sys.path.insert(0, V)
import make_covers as MC
from playwright.sync_api import sync_playwright
MC.HTML = (MC.HTML.replace('background:#F7F8FA', 'background:#0F1B3D').replace('.stamp{', '.stamp{display:none;')
           .replace('color:#6B7280', 'color:#A5B4D4').replace('top:196px', 'top:96px'))
Y, Wt = '#FFD43B', '#FFFFFF'
MC.COV['pibu1003'] = dict(stamp='',
    rows=[('국민연금 피부양자 소득 기준', 92, Wt, 't'), ('재산 많으면', 136, Y, 't'), ('1천만|원', 330, Y, 'num'), ('보통은 2천만원', 112, Wt, 't')],
    src='국민건강보험법 시행규칙 별표 1의2(2025.4.23 개정) · 공적연금은 받은 돈 전부', keep_orig=False,
    check=['피부양자', '2천만원', '1천만원', '5억 4천만원'])
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1080, 'height': 1080}); MC.make('pibu1003', pg); b.close()
