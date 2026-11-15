# c03 확인 — 22개 구 84㎡ 띠 한 채 중간값이 내린 까닭이 '구 섞임'인지: 구별 84㎡ 중간값이 1년 전보다 오른 구 수, 비싼 구 몫 변화, 구 몫을 1년 전으로 고정한 가중 중간값
import json, os, glob, statistics as st, sys, collections as C
sys.stdout.reconfigure(encoding='utf-8')
H = os.path.dirname(os.path.abspath(__file__)); W = os.path.abspath(os.path.join(H, '..', '..'))
SG = json.load(open(os.path.join(W, 'research', 'seoul_sgg.json'), encoding='utf-8'))
num = lambda s: float(str(s or '0').replace(',', '') or 0); ymi = lambda r: int(r['dealYear']) * 100 + int(r['dealMonth'])
rows = []
for p in sorted(glob.glob(os.path.join(H, 'raw', '*_trade.json'))):
    code = os.path.basename(p)[:5]
    for r in json.load(open(p, encoding='utf-8')):
        if not r.get('cdealType') and 80 <= num(r['excluUseAr']) < 90: r['_g'] = code; rows.append(r)
win = lambda r: 'now' if 202511 <= ymi(r) <= 202611 else ('pre' if 202411 <= ymi(r) <= 202510 else None)
NODO = ['11350', '11320', '11305']; G22 = [c for c in SG if c not in NODO]
d = C.defaultdict(lambda: {'pre': [], 'now': []})
for r in rows:
    w = win(r)
    if w and r['_g'] in G22: d[r['_g']][w].append(num(r['dealAmount']))
up = sum(1 for c in G22 if st.median(d[c]['now']) > st.median(d[c]['pre']))
print(f'- 22개 구 중 84㎡ 띠 한 채 중간값이 1년 전보다 오른 구: {up}개')
pre_med = {c: st.median(d[c]['pre']) for c in G22}; top = sorted(G22, key=lambda c: -pre_med[c])[:6]
for w in ('pre', 'now'):
    tot = sum(len(d[c][w]) for c in G22); t = sum(len(d[c][w]) for c in top)
    print(f'- {w}: 1년 전 중간값 위 6개 구({",".join(SG[c] for c in top)}) 몫 {t/tot*100:.1f}% ({t:,}/{tot:,})')
