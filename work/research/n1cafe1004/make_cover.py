# n1cafe1004 대표사진 1080x1080 — schd1003 남색 카드 틀 그대로. firemap-write 2026-10-03
import os, sys
sys.stdout.reconfigure(encoding='utf-8')
V = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'visual', 'cafe-covers-1002'); sys.path.insert(0, V)
import make_covers as MC
from playwright.sync_api import sync_playwright
MC.HTML = (MC.HTML.replace('background:#F7F8FA', 'background:#0F1B3D').replace('.stamp{', '.stamp{display:none;')
           .replace('color:#6B7280', 'color:#A5B4D4').replace('top:196px', 'top:96px').replace('s>120){s-=6', 's>9999){s-=6'))
Y, Wt = '#FFD43B', '#FFFFFF'
MC.COV['n1cafe1004'] = dict(stamp='',
    rows=[('연봉 순위 100칸 중', 96, Wt, 't'), ('1억원 → 2억원', 110, Wt, 't'), ('올라가는 자리', 110, Y, 't'), ('6|칸뿐', 300, Y, 'num')],
    src='국세청 근로소득 백분위 2024년 귀속 · 100칸 중 7~8% → 1% 칸', keep_orig=False,
    check=['1억', '6', '자리'])
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1080, 'height': 1080}); MC.make('n1cafe1004', pg); b.close()
