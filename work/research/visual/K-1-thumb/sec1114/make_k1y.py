# K-1 썸네일 박힌 해 판(copywriter 11/14, benchmark-loop 지시 '작년·올해'→연도). make_k1n.py의 함수만 빌려 씀(그 파일 맨 아래 make 호출은 실행 안 함).
import os, sys
sys.stdout.reconfigure(encoding='utf-8')
O = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
src = open(os.path.join(O, 'make_k1n.py'), encoding='utf-8').read().split('\n')
keep = [l for i, l in enumerate(src) if not (l.startswith('make(') or l.startswith('BIG[1]') or l.startswith('if __name__') or l.startswith('    make_h('))]
g = {'__file__': os.path.join(O, 'make_k1n.py'), '__name__': 'k1y'}
exec('\n'.join(keep), g)
from PIL import Image
TOP = '1년 정기예금 · 세금 뗀 이자|2025년 9월 vs 2026년 9월'
V = {'y1': '2025년보다 87만원 더', 'y2': '1년 새 87만원 더'}
for k, big2 in V.items():
    g['BIG'][:] = ['정기예금 1억 이자', big2]
    out = f'k1y_{k}.png'
    g['make_h'](out, 'bank_counter_hands_money_1_18804128.jpg', 0.0, TOP)
    im = Image.open(os.path.join(O, out))
    for w in (412, 168):
        im.resize((w, round(w * 720 / 1280)), Image.LANCZOS).save(os.path.join(O, 'sec1114', f'k1y_{k}_{w}.png'))
    os.replace(os.path.join(O, out), os.path.join(O, 'sec1114', out))
