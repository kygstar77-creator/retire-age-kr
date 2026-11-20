# guri1121 — 구리시 41310(규제 밖) vs 하남시 41450(2025-10-20 토지거래허가) 아파트 매매 실거래(S1 raw) · firemap-write-b 2026-11-20 (hanam1120/calc.py 틀)
# 같은 집 = 같은 단지(aptSeq)·같은 전용면적(1㎡ 반올림). 해제(cdealType) 뺌.
import json, os, glob, statistics as st, sys, collections as C
sys.stdout.reconfigure(encoding='utf-8')
H = os.path.dirname(os.path.abspath(__file__))
num = lambda s: float(str(s or '0').replace(',', '') or 0)
def load(code):
    out = []
    for p in sorted(glob.glob(os.path.join(H, 'raw', f'{code}_*_trade.json'))):
        for r in json.load(open(p, encoding='utf-8')):
            r['_ym'] = int(r['dealYear']) * 100 + int(r['dealMonth']); r['_d'] = r['_ym'] * 100 + int(r['dealDay'])
            r['_a'] = round(num(r['excluUseAr'])); r['_k'] = (r.get('aptSeq') or r['aptNm'], r['_a']); r['_p'] = num(r['dealAmount'])
            out.append(r)
    return out
D = {}
for code, nm in (('41310', '구리'), ('41450', '하남')):
    A = load(code); T = [r for r in A if not r.get('cdealType')]; D[nm] = T
    print(f'{nm} 매매(해제 뺌) {len(T)}건 · 해제 {len(A)-len(T)}건 · 단지 {len({r["_k"][0] for r in T})} · 기간 {min(r["_ym"] for r in T)}~{max(r["_ym"] for r in T)}')
G = D['구리']
print('구리 동별 건수:', C.Counter(r['umdNm'] for r in G).most_common())
print('\n# 월별 매매 건수(해제 뺌) 구리 / 하남')
for ym in sorted({r['_ym'] for r in G}):
    if ym >= 202501: print(ym, sum(1 for r in G if r['_ym'] == ym), '/', sum(1 for r in D['하남'] if r['_ym'] == ym))
PER = {'규제전5': (202505, 202509), '규제후5': (202511, 202603), '최근5': (202606, 202610), '1년전5': (202506, 202510), '전년같은때': (202406, 202410)}
def inper(r, k): lo, hi = PER[k]; return lo <= r['_ym'] <= hi
print('\n# 5개월 묶음 건수·월평균')
for k in PER:
    for nm in ('구리', '하남'):
        v = [r for r in D[nm] if inper(r, k)]; print(f'{nm} {k} {PER[k]}: {len(v)}건 · 월평균 {len(v)/5:.0f}')
for nm in ('구리', '하남'):
    a = sum(1 for r in D[nm] if inper(r, '규제전5')); b = sum(1 for r in D[nm] if inper(r, '규제후5')); c = sum(1 for r in D[nm] if inper(r, '최근5'))
    print(f'{nm} 규제후/규제전 {b/a:.3f} · 최근/규제전 {c/a:.3f}')
print('\n# 10월 15일 앞뒤 2주(계약일)')
for nm in ('구리', '하남'):
    a = sum(1 for r in D[nm] if 20251001 <= r['_d'] <= 20251014); b = sum(1 for r in D[nm] if 20251020 <= r['_d'] <= 20251102)
    print(f'{nm} 10/1~10/14 {a}건 · 10/20~11/2 {b}건')
def pairs(rows, a, b):
    d = C.defaultdict(lambda: C.defaultdict(list)); nm = {}
    for r in rows:
        nm[r['_k']] = (r['aptNm'], r['umdNm'])
        for k in (a, b):
            if inper(r, k): d[r['_k']][k].append(r['_p'])
    return [(st.median(v[b]) / st.median(v[a]) - 1, st.median(v[b]) - st.median(v[a]), nm[k], k[1], st.median(v[a]), st.median(v[b]), len(v[a]), len(v[b])) for k, v in d.items() if v[a] and v[b]]
def show(lbl, ps):
    if not ps: print(lbl, '0쌍'); return
    rs = [x[0] for x in ps]; ds = [x[1] for x in ps]
    print(f"{lbl}: {len(ps)}쌍 · 가운데 {st.median(rs)*100:+.1f}% · 가운데 금액 {st.median(ds)/10000:+.2f}억 · 오른 쌍 {sum(1 for x in rs if x>0)}개({sum(1 for x in rs if x>0)/len(rs)*100:.0f}%)")
print('\n# 같은 집 매매 1년(2025.6~10 → 2026.6~10)')
for nm in ('구리', '하남'): show(nm, pairs(D[nm], '1년전5', '최근5'))
print('\n# 같은 집 매매 그 전 1년(2024.6~10 → 2025.6~10)')
for nm in ('구리', '하남'): show(nm, pairs(D[nm], '전년같은때', '1년전5'))
print('\n# 같은 집 규제 전 5개월 → 규제 후 5개월')
for nm in ('구리', '하남'): show(nm, pairs(D[nm], '규제전5', '규제후5'))
print('\n# 84㎡ 안팎(83~86㎡) 매매 가운데 값')
for nm in ('구리', '하남'):
    for k in ('전년같은때', '1년전5', '최근5'):
        v = [r['_p'] for r in D[nm] if inper(r, k) and 83 <= r['_a'] <= 86]
        print(f'{nm} {k}: {len(v)}건 {st.median(v)/10000:.2f}억' if v else f'{nm} {k}: 0건')
print('\n# 구리 84㎡ 안팎 최근 단지별(3건 이상) 가운데')
d = C.defaultdict(list)
for r in G:
    if inper(r, '최근5') and 83 <= r['_a'] <= 86: d[(r['aptNm'], r['umdNm'])].append(r['_p'])
v = sorted((st.median(x), k, len(x)) for k, x in d.items() if len(x) >= 3)
for m, k, n in v: print('  ', k, n, '건', round(m / 10000, 2), '억')
print('\n# 구리 동별 같은 집 1년')
for u in [u for u, _ in C.Counter(r['umdNm'] for r in G).most_common()]:
    show('  ' + u, pairs([r for r in G if r['umdNm'] == u], '1년전5', '최근5'))
print('\n# 구리 1년 같은 집 많이 오른·덜 오른(양쪽 2건 이상)')
ps = sorted([x for x in pairs(G, '1년전5', '최근5') if x[6] >= 2 and x[7] >= 2], reverse=True)
for x in ps[:3] + ps[-3:]: print('  ', f'{x[0]*100:+.1f}%', x[2][0], x[2][1], f'{x[3]}㎡', f'{x[4]/10000:.2f}억→{x[5]/10000:.2f}억', f'({x[6]}건/{x[7]}건)')
print('\n# 구리 매수자 거주지(buyerGbn 등 칸 확인)', sorted(G[-1].keys()))
print('# 구리 최근5 거래유형', C.Counter(r.get('dealingGbn') for r in G if inper(r, '최근5')).most_common())
print('# 구리 2026-11 계약(뺌):', sum(1 for r in G if r['_ym'] == 202611))
print('\n# 추가: 구리 지정(7/1 투기과열·조정, 7/5 토지거래허가) 앞뒤')
PER['상반기26'] = (202601, 202606); PER['지정후'] = (202607, 202610)
show('구리 같은 집 2026.1~6 → 2026.7~10', pairs(G, '상반기26', '지정후'))
show('하남 같은 집 2026.1~6 → 2026.7~10', pairs(D['하남'], '상반기26', '지정후'))
for lo, hi, lab in ((20260601, 20260630, '6/1~6/30'), (20260630, 20260630, '6/30 하루'), (20260701, 20260704, '7/1~7/4'), (20260705, 20260731, '7/5~7/31'), (20260801, 20261031, '8/1~10/31')):
    print(f'구리 {lab}: {sum(1 for r in G if lo <= r["_d"] <= hi)}건')
for k in ('상반기26', '지정후'):
    v = [r['_p'] for r in G if inper(r, k) and 83 <= r['_a'] <= 86]; print(f'구리 84㎡ {k}: {len(v)}건 {st.median(v)/10000:.2f}억')
print('구리 2026.7~10 월평균', sum(1 for r in G if inper(r, '지정후')) / 4, '· 2026.1~6 월평균', sum(1 for r in G if inper(r, '상반기26')) / 6)
print('구리 2025.11~2026.6 8개월', sum(1 for r in G if 202511 <= r['_ym'] <= 202606), '건 · 2023.1~2025.10 34개월 월평균', round(sum(1 for r in G if 202301 <= r['_ym'] <= 202510) / 34))
