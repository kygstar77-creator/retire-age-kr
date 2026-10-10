import os, sys, shutil
sys.stdout.reconfigure(encoding='utf-8')
V = os.path.join(r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work\research\visual\cafe-covers-1002'); sys.path.insert(0, V)
import make_covers as MC
from playwright.sync_api import sync_playwright
MC.HTML = (MC.HTML.replace('background:#F7F8FA', 'background:#0F1B3D').replace('.stamp{', '.stamp{display:none;')
           .replace('color:#6B7280', 'color:#A5B4D4').replace('top:196px', 'top:96px').replace('justify-content:space-between','justify-content:center;gap:44px'))
Y, Wt = '#FFD43B', '#FFFFFF'
VAR = {
 'A': [('같은 집 10억원 상속세', 92, Wt, 't'), ('6.5|배', 280, Y, 'num'), ('두 번째 상속에서 이만큼 뛰어요', 72, Wt, 't')],
 'B': [('상속세 면제한도', 110, Wt, 't'), ('10억→5억', 200, Y, 'num'), ('남은 부모님 상속 땐 배우자공제가 없어요', 54, Wt, 't')],
 'D': [('상속세 면제한도', 130, Wt, 't'), ('6.5|배', 300, Y, 'num'), ('두 번째 상속에서 뛰는 세금', 84, Wt, 't')],
 'E': [('상속세 면제한도', 130, Wt, 't'), ('10억→5억', 240, Y, 'num'), ('두 번째 상속 땐 반으로', 96, Wt, 't')],
 'F': [('상속세 면제한도', 150, Wt, 't'), ('6|배↑', 380, Y, 'num'), ('두 번째 상속 세금', 120, Wt, 't')],
 'G': [('상속세 면제한도', 150, Y, 't'), ('10억→5억', 270, Wt, 'num'), ('두 번째 상속 땐', 130, Y, 't')],
 'H': [('상속세 면제한도', 150, Wt, 't'), ('6|배 넘게', 330, Y, 'num'), ('2,037만→1억3,240만', 112, Wt, 't')],
 'I': [('상속세 면제한도', 150, Wt, 't'), ('6.5|배', 430, Y, 'num'), ('두 번째 상속 세금', 130, Wt, 't')],
 'J': [('상속세 면제한도', 150, Wt, 't'), ('6|배 뛰어요', 300, Y, 'num'), ('두 번째 상속 세금', 130, Wt, 't')],
 'C': [('부모님 두 번째 상속', 104, Wt, 't'), ('1억3,240|만원', 190, Y, 'num'), ('첫 상속 땐 2,037만원이었는데', 72, Wt, 't')],
}
v = sys.argv[1]
if v=='Z': MC.HTML = MC.HTML.replace('background:#0F1B3D','background:#FFF1D6').replace('color:#A5B4D4','color:#6B7280')
MC.R = os.path.abspath('..')
MC.COV['inhded1011'] = dict(stamp='', rows=VAR[v], src='', keep_orig=False, check=[])
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1080, 'height': 1080}); MC.make('inhded1011', pg); b.close()
shutil.copy('pkg/img/00.png', f'covers_try/00_{v}.png')
