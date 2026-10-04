# bubyang1005 대표사진 1080x1080 — offimkt_ic0929(남색 카드) 틀 그대로. firemap-write 2026-10-02 23:3x
import os, sys
sys.stdout.reconfigure(encoding='utf-8')
V = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'visual', 'cafe-covers-1002'); sys.path.insert(0, V)
import make_covers as MC
from playwright.sync_api import sync_playwright
MC.HTML = (MC.HTML.replace('background:#F7F8FA', 'background:#0F1B3D').replace('.stamp{', '.stamp{display:none;')
           .replace('color:#6B7280', 'color:#A5B4D4').replace('top:196px', 'top:96px'))
Y, Wt = '#FFD43B', '#FFFFFF'
MC.COV['bubyang1005'] = dict(stamp='',
    rows=[('연금 5년 늦추면 기본 연금 +36%', 72, Wt, 't'), ('부양가족연금 가산은', 110, Y, 't'), ('+0|%', 330, Y, 'num'), ('늦춘 5년간은 아예 못 받아요', 80, Wt, 't')],
    src='국민연금법 제62조·제63조 · 공단 2026 연금액 공지', keep_orig=False,
    check=['부양가족', '36%'])
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1080, 'height': 1080}); MC.make('bubyang1005', pg); b.close()
