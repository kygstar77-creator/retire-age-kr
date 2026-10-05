# hfguar1006 표지 B안 — 통과한 남색 카드 틀(imuigye1005 7.5·irpwd1006 7.33) 그대로, 숫자 1개(533만)+짧은 말. firemap-write 2026-10-06 03:2x
# 결과는 covers_try/00_<안>.png 로만 낸다(pkg/img/00.png는 통과 전 안 바꿈).
import os, sys, shutil
sys.stdout.reconfigure(encoding='utf-8')
D = os.path.dirname(os.path.abspath(__file__))
V = os.path.join(D, '..', 'visual', 'cafe-covers-1002'); sys.path.insert(0, V)
import make_covers as MC
from playwright.sync_api import sync_playwright
MC.HTML = (MC.HTML.replace('background:#F7F8FA', 'background:#0F1B3D').replace('.stamp{', '.stamp{display:none;')
           .replace('color:#6B7280', 'color:#A5B4D4').replace('top:196px', 'top:96px')
           .replace('let s=parseFloat(n.style.fontSize);while(', 'let s=n?parseFloat(n.style.fontSize):0;while(n&&'))
Y, Wt = '#FFD43B', '#FFFFFF'
SRC = '65세·4억 집·월 101만원 가정 · 2026.3.1 개편 초기 1.5→1.0%·연 0.75→0.95%'
CHK = ['533만원', '65세', '4억']
V_ = {
 'B1': [('주택연금 보증료 개편 뒤', 80, Wt, 't'), ('65세·4억 집, 20년 받으면', 74, Wt, 't'), ('보증료 533만원 더', 100, Y, 't'), ('개편 전보다 · 대출잔액에 더해져요', 56, Wt, 't')],
 'B3': [('주택연금 보증료 개편', 100, Y, 't'), ('20년 받으면 보증료', 128, Wt, 't'), ('533|만 더', 260, Y, 'num'), ('현금 아닌 대출잔액에 더해져요', 76, Wt, 't')],
 'B4': [('주택연금 20년 받으면', 100, Y, 't'), ('개편 전보다 보증료', 128, Wt, 't'), ('533|만 더', 260, Y, 'num'), ('현금 아닌 대출잔액에 더해져요', 76, Wt, 't')],
 'B5': [('주택연금 20년 받으면', 100, Y, 't'), ('개편 전보다 보증료', 128, Wt, 't'), ('533|만 더 내요', 230, Y, 'num'), ('현금 아닌 대출잔액에 더해져요', 76, Wt, 't')],
 'B6': [('주택연금 20년 받으면', 100, Y, 't'), ('개편 전보다 보증료', 128, Wt, 't'), ('533|만 더 내요', 230, Y, 'num'), ('3월 신규 가입부터 · 11년까진 덜 내요', 70, Wt, 't')],
 'B2': [('주택연금 20년 받으면', 100, Y, 't'), ('개편 전보다 보증료', 128, Wt, 't'), ('533|만 더', 260, Y, 'num'), ('주택연금 보증료 개편 비교', 84, Wt, 't')],
}
names = sys.argv[1:] or list(V_)
img = os.path.join(D, 'pkg', 'img'); cur = os.path.join(img, '00.png'); bak = cur + '.bak'
shutil.copy(cur, bak)
try:
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1080, 'height': 1080})
        for n in names:
            MC.COV['hfguar1006'] = dict(stamp='', rows=V_[n], src=SRC, keep_orig=False, check=CHK)
            MC.make('hfguar1006', pg)
            shutil.copy(cur, os.path.join(D, 'covers_try', f'00_{n}.png'))
        b.close()
finally:
    shutil.move(bak, cur)
