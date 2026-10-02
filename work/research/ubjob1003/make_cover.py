# ubjob1003 대표사진 1080x1080 — deadfin1003 남색 틀 그대로. firemap-write 2026-10-03 06:2x
import os, sys
sys.stdout.reconfigure(encoding='utf-8')
V = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'visual', 'cafe-covers-1002'); sys.path.insert(0, V)
import make_covers as MC
from playwright.sync_api import sync_playwright
MC.HTML = (MC.HTML.replace('background:#F7F8FA', 'background:#0F1B3D').replace('.stamp{', '.stamp{display:none;')
           .replace('color:#6B7280', 'color:#A5B4D4').replace('top:196px', 'top:96px'))
Y, Wt = '#FFD43B', '#FFFFFF'
MC.COV['ubjob1003'] = dict(stamp='',
    rows=[('실업급여 조건', 100, Wt, 't'), ('65세', 250, Y, 'num'), ('넘어 새로 입사하면', 104, Wt, 't'), ('그만둬도 못 받아요', 104, Y, 't')],
    src='고용보험법 제10조 · 65세 이후 새로 고용되면 실업급여 적용 제외', keep_orig=False,
    check=['실업급여 조건', '65세'])
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1080, 'height': 1080}); MC.make('ubjob1003', pg); b.close()
