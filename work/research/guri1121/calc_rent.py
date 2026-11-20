# guri1121 — 구리시 41310 아파트 전월세 실거래(S2 raw): 2026-07 지정(투기과열·조정 7/1, 토지거래허가 7/5) 앞뒤 전세 · firemap-write-b 2026-11-20
# 같은 집 = 같은 단지(aptSeq)·같은 전용면적(1㎡ 반올림). 전세 = monthlyRent 0. 신규/갱신 = contractType.
import json, os, glob, statistics as st, sys, collections as C
sys.stdout.reconfigure(encoding='utf-8')
H = os.path.dirname(os.path.abspath(__file__))
num = lambda s: float(str(s or '0').replace(',', '') or 0)
R = []
for p in sorted(glob.glob(os.path.join(H, 'raw', '41310_*_rent.json'))):
    for r in json.load(open(p, encoding='utf-8')):
        r['_ym'] = int(r['dealYear']) * 100 + int(r['dealMonth']); r['_a'] = round(num(r['excluUseAr']))
        r['_k'] = (r.get('aptSeq') or r['aptNm'], r['_a']); r['_dep'] = num(r['deposit']); r['_mr'] = num(r['monthlyRent']); R.append(r)
print('칸', sorted(R[-1].keys()))
print('구리 전월세', len(R), '건 · 기간', min(r['_ym'] for r in R), max(r['_ym'] for r in R))
print('contractType', C.Counter(r.get('contractType') for r in R).most_common())
J = [r for r in R if r['_mr'] == 0]
PER = {'전년같은때': (202507, 202510), '상반기26': (202601, 202606), '지정후': (202607, 202610), '1년전5': (202506, 202510), '최근5': (202606, 202610)}
def inper(r, k): lo, hi = PER[k]; return lo <= r['_ym'] <= hi
print('\n# 월별 전세 / 월세 건수(전체) · 월세 몫 · 신규 전세')
for ym in sorted({r['_ym'] for r in R}):
    if ym >= 202501:
        a = [r for r in R if r['_ym'] == ym]; j = [r for r in a if r['_mr'] == 0]
        print(ym, len(j), '/', len(a) - len(j), f'월세몫 {(len(a)-len(j))/len(a)*100:.0f}%', '신규전세', sum(1 for r in j if r.get('contractType') == '신규'))
for k in PER:
    a = [r for r in R if inper(r, k)]; j = [r for r in a if r['_mr'] == 0]; n = (PER[k][1] % 100 - PER[k][0] % 100 + 1)
    print(f'{k} {PER[k]}: 전세 {len(j)}건(월 {len(j)/n:.0f}) · 월세 {len(a)-len(j)}건 · 월세 몫 {(len(a)-len(j))/len(a)*100:.1f}% · 신규 전세 {sum(1 for r in j if r.get("contractType")=="신규")}건')
def pairs(rows, a, b):
    d = C.defaultdict(lambda: C.defaultdict(list)); nm = {}
    for r in rows:
        nm[r['_k']] = (r['aptNm'], r['umdNm'])
        for k in (a, b):
            if inper(r, k): d[r['_k']][k].append(r['_dep'])
    return [(st.median(v[b]) / st.median(v[a]) - 1, st.median(v[b]) - st.median(v[a]), nm[k], k[1], st.median(v[a]), st.median(v[b]), len(v[a]), len(v[b])) for k, v in d.items() if v[a] and v[b]]
def show(lbl, ps):
    if not ps: print(lbl, '0쌍'); return
    rs = [x[0] for x in ps]; ds = [x[1] for x in ps]
    print(f"{lbl}: {len(ps)}쌍 · 가운데 {st.median(rs)*100:+.1f}% · 가운데 금액 {st.median(ds):+,.0f}만원 · 오른 쌍 {sum(1 for x in rs if x>0)}개({sum(1 for x in rs if x>0)/len(rs)*100:.0f}%)")
NJ = [r for r in J if r.get('contractType') == '신규']
print('\n# 같은 집 전세(모든 계약)')
show('2026.1~6 → 2026.7~10', pairs(J, '상반기26', '지정후'))
show('1년 2025.6~10 → 2026.6~10', pairs(J, '1년전5', '최근5'))
show('그 전 같은 길이 2025.7~10 → 2026.1~6 아님(참고 2025.7~10 → 2026.7~10)', pairs(J, '전년같은때', '지정후'))
print('\n# 같은 집 전세(신규 계약만)')
show('2026.1~6 → 2026.7~10', pairs(NJ, '상반기26', '지정후'))
show('1년 2025.6~10 → 2026.6~10', pairs(NJ, '1년전5', '최근5'))
show('2025.7~10 → 2026.7~10', pairs(NJ, '전년같은때', '지정후'))
print('\n# 84㎡ 안팎 전세 가운데(신규)')
for k in ('전년같은때', '상반기26', '지정후'):
    v = [r['_dep'] for r in NJ if inper(r, k) and 83 <= r['_a'] <= 86]; print(f'{k}: {len(v)}건 {st.median(v):,.0f}만원' if v else f'{k} 0건')
print('\n# 동별 같은 집 신규 전세 2025.7~10 → 2026.7~10')
for u, _ in C.Counter(r['umdNm'] for r in NJ).most_common():
    show('  ' + u, pairs([r for r in NJ if r['umdNm'] == u], '전년같은때', '지정후'))
print('\n# 갱신 계약 인상률(종전 보증금 칸 preDeposit 있으면)')
G2 = [r for r in J if r.get('contractType') == '갱신' and num(r.get('preDeposit')) > 0]
for k in ('상반기26', '지정후'):
    v = [r['_dep'] / num(r['preDeposit']) - 1 for r in G2 if inper(r, k)]
    if v: print(f'{k}: {len(v)}건 · 가운데 {st.median(v)*100:+.1f}% · 5% 넘은 몫 {sum(1 for x in v if x > 0.0501)/len(v)*100:.0f}%')
print('\n# 갱신요구권 사용 칸', C.Counter(r.get('useRRRight') for r in J if inper(r, '지정후')).most_common())
