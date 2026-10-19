# directdeal1019 계산 2 — 개인이 개인에게 판 직거래만(가족 간 거래가 들어 있을 수 있는 묶음)
import sys, os, statistics as st, collections
sys.stdout.reconfigure(encoding='utf-8')
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'calc.py'), encoding='utf-8').read().split('# 월별')[0].replace("print(", "(lambda *a, **k: None)("))
P = [r for r in D if r.get('buyerGbn') == '개인' and r.get('slerGbn') == '개인']
print(f'개인→개인 직거래 {len(P):,} / 해제 뺀 전체 {len(V):,} = {100*len(P)/len(V):.1f}%')
bym = collections.defaultdict(lambda: [0, 0])
for r in V: k = r['_d'].strftime('%Y-%m'); bym[k][1] += 1
for r in P: bym[r['_d'].strftime('%Y-%m')][0] += 1
for k in sorted(bym): a, b = bym[k]; print(' ', k, f'{a}/{b} {100*a/b:.1f}%')
print('직거래 매도 법인→매수 누구', collections.Counter(r.get('buyerGbn') for r in D if r.get('slerGbn') == '법인'))
print('직거래 매수 공공기관 월별', sorted(collections.Counter(r['_d'].strftime('%Y-%m') for r in D if r.get('buyerGbn') == '공공기관').items()))
idx = collections.defaultdict(list)
for r in M: idx[r['_k']].append(r)
pairs = []
for r in P:
    c = [m['_p'] for m in idx[r['_k']] if abs((m['_d'] - r['_d']).days) <= 90]
    if len(c) >= 3: med = st.median(c); pairs.append((r, med, (r['_p'] / med - 1) * 100, len(c)))
g = [x[2] for x in pairs]
print(f'\n짝 지은 개인→개인 직거래 {len(pairs):,}건 · 차이 중앙 {st.median(g):+.1f}%')
for lab, f in (('30% 이상 쌈', lambda x: x <= -30), ('5% 이상 쌈', lambda x: x <= -5), ('±5% 안', lambda x: -5 < x < 5), ('5% 이상 비쌈', lambda x: x >= 5)):
    n = sum(map(f, g)); print(f'  {lab}: {n}건 {100*n/len(g):.1f}%')
d = [med - r['_p'] for r, med, _, _ in pairs]
print(f'  차액 중앙 {st.median(d):,.0f}만원 · 3억 이상 {sum(x >= 30000 for x in d)}건')
# 세법 선(시가 30%·3억 / 5%·3억) 기준 나누기 — 중개 중앙값을 '시가'로 볼 때(가정)
a = sum((med - r['_p']) >= min(med*0.3, 30000) for r, med, _, _ in pairs)
b = sum((med - r['_p']) >= min(med*0.05, 30000) for r, med, _, _ in pairs)
print(f'  중개 중앙값을 시가로 보면: 차액 ≥ min(30%,3억) {a}건 {100*a/len(pairs):.1f}% · 차액 ≥ min(5%,3억) {b}건 {100*b/len(pairs):.1f}%')
# 대표 예: 중앙 차이에 가까운 사례(84㎡ 근처)
ex = sorted([p for p in pairs if 80 <= float(p[0]['excluUseAr']) <= 86 and p[3] >= 8], key=lambda x: abs(x[2] - st.median(g)))[:5]
for r, med, gg, n in ex: print(f"  예: {SGG[r['sggCd']]} {r['umdNm']} {r['aptNm']} {r['excluUseAr']}㎡ {r['_d']} 직거래 {r['_p']:,}만 vs 중개 중앙 {med:,.0f}만({n}건) {gg:+.1f}%")
