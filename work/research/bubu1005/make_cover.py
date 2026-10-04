import os, sys
sys.stdout.reconfigure(encoding='utf-8')
V = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'visual', 'cafe-covers-1002'); sys.path.insert(0, V)
import make_covers as MC
from playwright.sync_api import sync_playwright
MC.HTML = (MC.HTML.replace('background:#F7F8FA', 'background:#0F1B3D').replace('.stamp{', '.stamp{display:none;')
           .replace('color:#6B7280', 'color:#A5B4D4').replace('top:196px', 'top:96px')
           .replace('let s=parseFloat(n.style.fontSize);while(', 'let s=n?parseFloat(n.style.fontSize):0;while(n&&'))
Y, Wt = '#FFD43B', '#FFFFFF'
MC.COV['bubu1005'] = dict(stamp='',
    rows=[('기초연금 부부감액', 84, Wt, 't'), ('부부 소득인정액이', 70, Wt, 't'), ('약 339만원 넘으면', 96, Y, 't'), ('20%에 더해 또 줄어요', 64, Wt, 't')],
    src='기초연금법 제8조 · 시행령 제11조 · 2026년 기준', keep_orig=False,
    check=['부부감액', '339만', '20%']
)
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1080, 'height': 1080}); MC.make('bubu1005', pg); b.close()
