import os, sys, shutil
sys.stdout.reconfigure(encoding='utf-8')
V = os.path.join(r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work\research\visual\cafe-covers-1002'); sys.path.insert(0, V)
import make_covers as MC
from playwright.sync_api import sync_playwright
MC.HTML = (MC.HTML.replace('background:#F7F8FA', 'background:#0F1B3D').replace('.stamp{', '.stamp{display:none;')
           .replace('color:#6B7280', 'color:#A5B4D4').replace('top:196px', 'top:96px').replace('justify-content:space-between','justify-content:center;gap:44px'))
Y, Wt = '#FFD43B', '#FFFFFF'
VAR = {
 'A': [('육아휴직 급여 12개월', 92, Wt, 't'), ('2,310|만원', 250, Y, 'num'), ('월급이 300만원이든 400만원이든 같아요', 56, Wt, 't')],
 'C': [('육아휴직 12개월', 124, Wt, 't'), ('2,310|만원', 250, Y, 'num'), ('통상임금 250만원부터 다 같아요', 70, Wt, 't')],
 'D': [('육아휴직 12개월', 124, Wt, 't'), ('2,310|만원', 250, Y, 'num'), ('상한에 걸리면 똑같아요', 92, Wt, 't')],
 'E': [('육아휴직 12개월', 124, '#1F2937', 't'), ('2,310|만원', 250, '#E8590C', 'num'), ('상한에 걸리면 똑같아요', 92, '#1F2937', 't')],
 'F': [('육아휴직 12개월 급여', 104, Wt, 't'), ('150|만원', 280, Y, 'num'), ('통상임금 2배 차이인데 이만큼', 80, Wt, 't')],
 'B': [('육아휴직 급여', 100, Wt, 't'), ('150|만원', 280, Y, 'num'), ('월급은 2배 차이인데 급여 차이는 이만큼', 56, Wt, 't')],
}
v = sys.argv[1]
if v=='E': MC.HTML = MC.HTML.replace('background:#0F1B3D','background:#FFF1D6').replace('color:#A5B4D4','color:#6B7280')
MC.R = os.path.abspath('..')
MC.COV['childleave1010'] = dict(stamp='', rows=VAR[v], src='', keep_orig=False, check=['2,310', '150'] if v in 'BF' else ['2,310'])
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1080, 'height': 1080}); MC.make('childleave1010', pg); b.close()
shutil.copy('pkg/img/00.png', f'covers_try/00_{v}.png')
