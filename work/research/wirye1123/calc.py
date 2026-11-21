# wirye1123 — 위례신도시 세 곳(서울 송파 11710 · 성남 수정 41131 · 하남 41450) 아파트 매매 실거래(S1 raw) 같은 집 비교 · firemap-write 2026-11-22 (bundang1122/calc.py 틀)
# 위례 단지 = 단지 이름에 '위례'가 들어간 곳(송파 장지·거여동, 성남 창곡동, 하남 학암동). 같은 집 = 같은 단지(aptSeq)·같은 전용면적(1㎡ 반올림). 해제 거래 뺌.
import json, os, glob, statistics as st, sys, collections as C
sys.stdout.reconfigure(encoding='utf-8')
H = os.path.dirname(os.path.abspath(__file__))
num = lambda s: float(str(s or '0').replace(',', '') or 0)
NM = {'11710': '송파', '41131': '성남', '41450': '하남'}
TA = []
for p in sorted(glob.glob(os.path.join(H, 'raw', '*_trade.json'))):
    lawd = os.path.basename(p)[:5]
    for r in json.load(open(p, encoding='utf-8')):
        r['_lawd'] = lawd; r['_ym'] = int(r['dealYear']) * 100 + int(r['dealMonth']); r['_a'] = round(num(r['excluUseAr']))
        r['_k'] = (r.get('aptSeq') or r['aptNm'], r['_a']); r['_p'] = num(r['dealAmount']); TA.append(r)
T = [r for r in TA if not r.get('cdealType')]
W = [r for r in T if '위례' in r['aptNm'] and r['umdNm'] in ('장지동', '거여동', '창곡동', '학암동')]
for r in W: r['_g'] = NM[r['_lawd']]
GS = ['송파', '성남', '하남']
print('세 곳 매매(해제 뺌)', len(T), '건 · 해제', len(TA) - len(T))
print('위례 단지 매매', len(W), '건 · 단지', len({r['_k'][0] for r in W}), '· 기간', min(r['_ym'] for r in W), max(r['_ym'] for r in W))
for g in GS:
    v = [r for r in W if r['_g'] == g]; print(f'  {g} 위례: {len(v)}건 · 단지 {len({r["_k"][0] for r in v})} ·', sorted({r["aptNm"] for r in v}))
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
    print(f"{lbl}: {len(ps)}쌍 · 가운데 {st.median(rs)*100:+.1f}% · 가운데 금액 {st.median(ds)/10000:+.2f}억 · 오른 쌍 {sum(1 for x in rs if x>0)/len(rs)*100:.0f}% · 고점 넘은(>=0) {sum(1 for x in rs if x>=0)}개({sum(1 for x in rs if x>=0)/len(rs)*100:.0f}%)")
for a, b, lab in (('1년전', '최근', '1년(2025.6~10 → 2026.6~10)'), ('고점21', '최근', '2021년 7~12월 → 2026.6~10'), ('바닥23', '최근', '2023년 1~6월 → 2026.6~10'), ('고점21', '바닥23', '2021년 7~12월 → 2023년 1~6월')):
    print(f'\n# 같은 집 매매 {lab}')
    show('위례 전체', pairs(W, a, b))
    for g in GS: show(g, pairs([r for r in W if r['_g'] == g], a, b))
print('\n# 비교: 같은 시·구의 위례 아닌 아파트 같은 집 1년')
for lawd, g in NM.items():
    v = [r for r in T if r['_lawd'] == lawd and r not in W]
    show(f'{g} 위례 뺀 나머지 1년', pairs(v, '1년전', '최근'))
print('\n# 84㎡ 안팎(83~86㎡) 매매 가운데 값')
for g in GS:
    row = []
    for per in ('고점21', '바닥23', '1년전', '최근'):
        v = [r['_p'] for r in W if r['_g'] == g and inper(r, per) and 83 <= r['_a'] <= 86]
        row.append(f'{per} {len(v)}건 {st.median(v)/10000:.2f}억' if v else f'{per} 0건')
    print(g, ' · '.join(row))
print('\n# 84㎡ 같은 단지 1년 — 양쪽 2건 이상, 단지별')
for g in GS:
    ps = sorted([x for x in pairs([r for r in W if r['_g'] == g and 83 <= r['_a'] <= 86], '1년전', '최근') if x[6] >= 2 and x[7] >= 2], reverse=True)
    for x in ps: print('  ', g, f'{x[0]*100:+.1f}%', x[2], f'{x[3]}㎡', f'{x[4]/10000:.2f}억→{x[5]/10000:.2f}억', f'({x[6]}건/{x[7]}건)')
print('\n# 반기별 매매 건수(위례)')
for y in range(2021, 2027):
    for h, (lo, hi) in (('상', (1, 6)), ('하', (7, 12))):
        v = [r for r in W if r['_ym'] // 100 == y and lo <= r['_ym'] % 100 <= hi]
        if v: print(f'{y}{h}', len(v), ' '.join(f"{g}{sum(1 for r in v if r['_g']==g)}" for g in GS))
print('\n# 10/15 대책(2025-10-20 토허) 앞뒤 월평균 계약: 2025.7~9 vs 2025.11~2026.1 vs 2026.6~10')
for g in GS:
    v = [r for r in W if r['_g'] == g]
    a = sum(1 for r in v if 202507 <= r['_ym'] <= 202509) / 3; b = sum(1 for r in v if 202511 <= r['_ym'] <= 202601) / 3; c = sum(1 for r in v if 202606 <= r['_ym'] <= 202610) / 5
    print(f'{g}: {a:.0f} → {b:.0f} → {c:.0f}')
print('\n# 2026년 11월 계약(최근에서 뺌):', sum(1 for r in W if r['_ym'] == 202611), '건')
print('\n# 84㎡ 최근 가장 비싼·싼 거래(위례)')
x = sorted([r for r in W if inper(r, '최근') and 83 <= r['_a'] <= 86], key=lambda r: r['_p'])
for r in x[:3] + x[-3:]: print('  ', r['_g'], r['aptNm'], r['_a'], r['_ym'], r['dealDay'], r['_p'], r.get('floor'))
print('\n# 직거래 몫(최근)', C.Counter(r.get('dealingGbn') for r in W if inper(r, '최근')).most_common())
print('\n# 84㎡ 최근(2026.6~10) 가격 구간(대출 한도 15억·25억 기준) 몫')
for g in GS + ['전체']:
    x = [r['_p'] for r in W if (g == '전체' or r['_g'] == g) and inper(r, '최근') and 83 <= r['_a'] <= 86]
    print(g, len(x), '건 · 15억 이하', sum(1 for p in x if p <= 150000), '· 15억 초과~25억', sum(1 for p in x if 150000 < p <= 250000), '· 25억 초과', sum(1 for p in x if p > 250000))
print('\n# 최근(2026.6~10) 위례 매매 전체 건수', sum(1 for r in W if inper(r, '최근')), '· 1년 전(2025.6~10)', sum(1 for r in W if inper(r, '1년전')))
