# d1cafe1004 대표사진 1080x1080 — schd1003 남색 카드 틀 그대로. firemap-write 2026-10-03
import os, sys
sys.stdout.reconfigure(encoding='utf-8')
V = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'visual', 'cafe-covers-1002'); sys.path.insert(0, V)
import make_covers as MC
from playwright.sync_api import sync_playwright
MC.HTML = (MC.HTML.replace('background:#F7F8FA', 'background:#0F1B3D').replace('.stamp{', '.stamp{display:none;')
           .replace('color:#6B7280', 'color:#A5B4D4').replace('top:196px', 'top:96px').replace('s>120){s-=6', 's>9999){s-=6'))
Y, Wt = '#FFD43B', '#FFFFFF'
MC.COV['d1cafe1004'] = dict(stamp='',
    rows=[('퇴직 후 건강보험료', 96, Wt, 't'), ('배당·이자 1,000만원에서', 96, Wt, 't'), ('1만원만 넘어도', 110, Y, 't'), ('월 4.5|만원 더', 230, Y, 'num')],
    src='월 2만 2,800원 → 6만 7,850원 · 지역가입자 1인·재산 0·2026년', keep_orig=False,
    check=['4.5', '1만원', '건강보험료'])
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1080, 'height': 1080}); MC.make('d1cafe1004', pg); b.close()
