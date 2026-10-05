# yujokstop1006 대표사진 1080x1080 — goldway1005/make_cover.py(남색 카드) 틀 그대로. firemap-write 2026-10-05 22:3x
import os, sys
sys.stdout.reconfigure(encoding='utf-8')
V = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'visual', 'cafe-covers-1002'); sys.path.insert(0, V)
import make_covers as MC
from playwright.sync_api import sync_playwright
MC.HTML = (MC.HTML.replace('background:#F7F8FA', 'background:#0F1B3D').replace('.stamp{', '.stamp{display:none;')
           .replace('color:#6B7280', 'color:#A5B4D4').replace('top:196px', 'top:96px'))
Y, Wt = '#FFD43B', '#FFFFFF'
ROWS = {
 'a': [('유족연금 3년 뒤', 124, Wt, 't'), ('다시 받는 나이', 124, Y, 't'), ('60|세', 380, Y, 'num'), ('1969년 이후 출생 배우자', 88, Wt, 't')],
}
v = sys.argv[1] if len(sys.argv) > 1 else 'a'
MC.COV['yujokstop1006'] = dict(stamp='', rows=ROWS[v], src='국민연금법 제76조 · 부칙 제8조', keep_orig=False, check=['60세', '1969년'])
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1080, 'height': 1080}); MC.make('yujokstop1006', pg); b.close()
