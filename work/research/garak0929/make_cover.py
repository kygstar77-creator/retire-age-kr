# garak0929 대표사진 1080x1080 — b10danji1003 2차(남색 카드, 평균 8) 틀 그대로. firemap-write 2026-10-02 18:3x
import os, sys
sys.stdout.reconfigure(encoding='utf-8')
V = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'visual', 'cafe-covers-1002'); sys.path.insert(0, V)
import make_covers as MC
from playwright.sync_api import sync_playwright
MC.HTML = (MC.HTML.replace('background:#F7F8FA', 'background:#0F1B3D').replace('.stamp{', '.stamp{display:none;')
           .replace('color:#6B7280', 'color:#A5B4D4').replace('top:196px', 'top:96px'))
Y, Wt = '#FFD43B', '#FFFFFF'
MC.COV['garak0929'] = dict(stamp='',
    rows=[('헬리오시티 84㎡', 120, Wt, 't'), ('1년 새', 130, Y, 't'), ('3.9|%', 380, Y, 'num'), ('가락1차쌍용 84㎡ 22.5%', 104, Wt, 't')],
    src='국토부 실거래 · 송파구 가락동 2025·2026년 7~9월 매매 가운데 값', keep_orig=False,
    check=['3.9%', '22.5%', '가락1차쌍용', '헬리오시티', '7~9월'])
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1080, 'height': 1080}); MC.make('garak0929', pg); b.close()
