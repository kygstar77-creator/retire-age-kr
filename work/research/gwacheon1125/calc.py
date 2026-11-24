# gwacheon1125 — 국토부 아파트 매매 실거래(S1 raw) 경기 과천시 41290으로 남은 주공 5개 단지 vs 재건축으로 새로 지은 단지 vs 지식정보타운(갈현동) 같은 집 비교 · firemap-write 2026-11-25 (gwanggyo1125/calc.py 틀)
# 같은 집 = 같은 단지(aptSeq)·같은 전용면적(1㎡ 반올림). 매매는 해제(cdealType) 뺌.
import json, os, glob, statistics as st, sys, collections as C
sys.stdout.reconfigure(encoding='utf-8')
H = os.path.dirname(os.path.abspath(__file__))
num = lambda s: float(str(s or '0').replace(',', '') or 0)
TA = []
for p in sorted(glob.glob(os.path.join(H, 'raw', '*_trade.json'))):
    for r in json.load(open(p, encoding='utf-8')):
        r['_ym'] = int(r['dealYear']) * 100 + int(r['dealMonth']); r['_a'] = round(num(r['excluUseAr']))
        r['_k'] = (r.get('aptSeq') or r['aptNm'], r['_a']); r['_by'] = int(r.get('buildYear') or 0); TA.append(r)
T = [r for r in TA if not r.get('cdealType')]
for r in T: r['_p'] = num(r['dealAmount'])
print('과천시 매매(해제 뺌)', len(T), '· 해제', len(TA) - len(T), '· 기간', min(r['_ym'] for r in T), max(r['_ym'] for r in T))
PER = {'1년전': (202506, 202510), '최근': (202606, 202610), '고점21': (202107, 202112), '바닥23': (202301, 202306)}
def inper(r, k): lo, hi = PER[k]; return lo <= r['_ym'] <= hi
def pairs(rows, a, b):
    d = C.defaultdict(lambda: C.defaultdict(list)); nm = {}
    for r in rows:
        nm[r['_k']] = r['aptNm']
        for k in (a, b):
            if inper(r, k): d[r['_k']][k].append(r['_p'])
    return [(st.median(v[b]) / st.median(v[a]) - 1, st.median(v[b]) - st.median(v[a]), nm[k], k[1], st.median(v[a]), st.median(v[b]), len(v[a]), len(v[b])) for k, v in d.items() if v[a] and v[b]]
def show(lbl, ps):
    if not ps: print(lbl, '0쌍'); return
    rs = [x[0] for x in ps]; ds = [x[1] for x in ps]
    print(f"{lbl}: {len(ps)}쌍 · 가운데 {st.median(rs)*100:+.1f}% · 가운데 금액 {st.median(ds)/10000:+.2f}억 · 오른 쌍 {sum(1 for x in rs if x>0)} · 넘은(>=0) {sum(1 for x in rs if x>=0)}개")
JG = [r for r in T if r['aptNm'].startswith('주공')]
NW = [r for r in T if r['umdNm'] != '갈현동' and 2018 <= r['_by'] <= 2022]
RM = [r for r in T if r['umdNm'] != '갈현동' and 2007 <= r['_by'] <= 2008]
GH = [r for r in T if r['umdNm'] == '갈현동']
for lab, v in (('남은 주공', JG), ('재건축 새 단지 2018~2022', NW), ('래미안 2007~2008', RM), ('지식정보타운 갈현동', GH)):
    print(lab, len(v), '건', sorted({(r['umdNm'], r['aptNm'], r['_by']) for r in v}))
ALL = T
for lab, v in (('과천 전체', ALL), ('남은 주공', JG), ('재건축 새 단지', NW), ('래미안 2007~2008', RM), ('지식정보타운', GH)):
    print(f'\n## {lab} · {len(v)}건 · 단지 {len({r["aptNm"] for r in v})}')
    for a, b in (('1년전', '최근'), ('고점21', '최근'), ('바닥23', '최근'), ('고점21', '바닥23')):
        show(f'{a}→{b}', pairs(v, a, b))
    for ar, lo, hi in (('59㎡안팎', 57, 60), ('84㎡안팎', 83, 86)):
        print('  ', ar, ' · '.join(f"{per} {len(x)}건 {st.median(x)/10000:.2f}억" if x else f'{per} 0건' for per in ('고점21', '바닥23', '1년전', '최근') for x in [[r['_p'] for r in v if inper(r, per) and lo <= r['_a'] <= hi]]))
print('\n# 단지별 1년(같은 집, 양쪽 1건 이상)')
for x in sorted(pairs(ALL, '1년전', '최근'), reverse=True): print('  ', f'{x[0]*100:+.1f}%', x[2], f'{x[3]}㎡', f'{x[4]/10000:.2f}→{x[5]/10000:.2f}억', f'({x[6]}/{x[7]}건)')
print('\n# 2021하 대비(같은 집)')
for x in sorted(pairs(ALL, '고점21', '최근'), reverse=True): print('  ', f'{x[0]*100:+.1f}%', x[2], f'{x[3]}㎡', f'{x[4]/10000:.2f}→{x[5]/10000:.2f}억', f'({x[6]}/{x[7]}건)')
print('\n# 최근 84㎡안팎 단지별 가운데')
d = C.defaultdict(list)
for r in ALL:
    if inper(r, '최근') and 83 <= r['_a'] <= 86: d[(r['umdNm'], r['aptNm'], r['_by'])].append(r['_p'])
for m, k, n in sorted([(st.median(v), k, len(v)) for k, v in d.items()], reverse=True): print('  ', f'{m/10000:.2f}억 {k} {n}건')
print('\n# 반기별 건수 과천 / 주공')
for y in range(2021, 2027):
    for h, (lo, hi) in (('상', (1, 6)), ('하', (7, 12))):
        v = [r for r in ALL if r['_ym'] // 100 == y and lo <= r['_ym'] % 100 <= hi]
        if v: print(f'{y}{h}', len(v), '/', sum(1 for r in v if r['aptNm'].startswith('주공')))
print('\n# 같은 집 반기 사슬(과천 전체)')
HS = [(f'{y}{h}', (y*100+lo, y*100+hi)) for y in range(2021, 2027) for h, lo, hi in (('상', 1, 6), ('하', 7, 12))]
for (la, pa), (lb, pb) in zip(HS, HS[1:]):
    PER['_a'], PER['_b'] = pa, pb; ps = pairs(ALL, '_a', '_b')
    if ps: print(f'{la}→{lb}: {len(ps)}쌍 {st.median([x[0] for x in ps])*100:+.1f}%')
print('\n# 직거래 몫(최근)', C.Counter(r.get('dealingGbn') for r in ALL if inper(r, '최근')).most_common())
print('# 11월 계약(최근에서 뺌)', sum(1 for r in ALL if r['_ym'] == 202611))
x = [r['_p'] for r in ALL if inper(r, '최근')]
print('# 최근 과천 매매', len(x), '건 가운데', st.median(x)/10000, '억 · 20억 넘는 집', sum(1 for p in x if p > 200000))
print('\n# 월별 건수 2025-06~2026-11')
for ym in sorted({r['_ym'] for r in ALL if r['_ym'] >= 202506}): print(ym, sum(1 for r in ALL if r['_ym'] == ym))
print('\n# 확인: 넓이 나눠 1년')
for lab, f in (('60㎡ 이하', lambda r: r['_a'] <= 60), ('60~85㎡', lambda r: 60 < r['_a'] <= 85), ('85㎡ 초과', lambda r: r['_a'] > 85)):
    for nm, v in (('주공', JG), ('새 단지', NW), ('래미안', RM), ('갈현동', GH)):
        show(f'  {lab} {nm}', pairs([r for r in v if f(r)], '1년전', '최근'))
