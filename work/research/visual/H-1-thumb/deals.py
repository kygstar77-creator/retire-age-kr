# H-1 썸네일용 84㎡대 거래별 평당(만원) — calc.py 3절 t84와 같은 원자료·같은 거르기. 중앙값을 calc_out 3절과 assert.
import json, os, sys, statistics as st
sys.stdout.reconfigure(encoding='utf-8')
H = os.path.dirname(os.path.abspath(__file__)); RT = os.path.join(H, '..', '..', 'rt')
PY = 3.305785
MS = ['202511', '202512', '202601', '202602', '202603', '202604', '202605', '202606', '202607', '202608', '202609', '202610']
num = lambda s: float(str(s or '0').replace(',', '') or 0)
def load(l):
    o = []
    for m in MS:
        p = os.path.join(RT, f'{l}_{m}_trade.json')
        if os.path.exists(p): o += json.load(open(p, encoding='utf-8'))
    return o
def t84(R, apt, umd):
    return [r for r in R if r['aptNm'].replace(' ', '') == apt and r['umdNm'] == umd and 80 <= num(r['excluUseAr']) < 85 and not r.get('cdealType') and r.get('buyerGbn') != '공공기관']
out = {}
for apt, umd, l in [('헬리오시티', '가락동', '11710'), ('올림픽파크포레온', '둔촌동', '11740')]:
    rows = t84(load(l), apt, umd)
    out[apt] = sorted(round(num(r['dealAmount']) / (num(r['excluUseAr']) / PY)) for r in rows)
    print(apt, len(out[apt]), min(out[apt]), max(out[apt]), round(st.median(out[apt])))
assert len(out['헬리오시티']) == 85 and len(out['올림픽파크포레온']) == 45
assert round(st.median(out['헬리오시티'])) == 11087 and round(st.median(out['올림픽파크포레온'])) == 10988
json.dump(out, open(os.path.join(H, 'deals.json'), 'w', encoding='utf-8'), ensure_ascii=False)
