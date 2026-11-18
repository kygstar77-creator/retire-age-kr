# pyeongchon1120 — 안양 동안구 41173 중 평촌동(1990년대 신도시 핵심)과 호계동 아파트 매매 실거래(S1 raw) 직접 계산 · firemap-write 2026-11-18 (cheongna1117/calc.py 틀)
# 같은 집 = 같은 단지(aptSeq)·같은 전용면적(1㎡ 반올림). 해제(cdealType) 뺌. 직거래 포함(몫 따로 셈).
import json, os, glob, statistics as st, sys, collections as C
sys.stdout.reconfigure(encoding='utf-8')
H = os.path.dirname(os.path.abspath(__file__))
num = lambda s: float(str(s or '0').replace(',', '') or 0)
rows = []; agent = C.Counter()
for p in sorted(glob.glob(os.path.join(H, 'raw', '*_trade.json'))):
    code = os.path.basename(p)[:5]
    for r in json.load(open(p, encoding='utf-8')):
        if r.get('cdealType'): continue
        if r['umdNm'] == '평촌동': g = '평촌동'
        elif r['umdNm'] == '호계동': g = '호계동'
        else: continue
        agent[(g, r.get('estateAgentSggNm'))] += 1
        r['_g'] = g; r['_ym'] = int(r['dealYear']) * 100 + int(r['dealMonth']); r['_p'] = num(r['dealAmount']); r['_a'] = round(num(r['excluUseAr']))
        r['_k'] = (r.get('aptSeq') or r['aptNm'], r['_a']); rows.append(r)
G = ('평촌동', '호계동')
print('중개사 시군구 칸(상위):', agent.most_common(6))
print('전체(해제 뺌)', len(rows), '건 · 계약', min(r['_ym'] for r in rows), '~', max(r['_ym'] for r in rows))
for g in G:
    v = [r for r in rows if r['_g'] == g]
    print(' ', g, len(v), '건 · 직거래 몫', f"{sum(1 for r in v if r.get('dealingGbn')=='직거래')/len(v)*100:.1f}%", '· 단지 수', len({r['aptSeq'] for r in v}))
PER = {'고점21': (202107, 202112), '바닥23': (202301, 202306), '1년전': (202506, 202510), '최근': (202606, 202610)}
def inper(r, k): lo, hi = PER[k]; return lo <= r['_ym'] <= hi
def pairs(g, a, b, minn=1):
    d = C.defaultdict(lambda: C.defaultdict(list))
    for r in rows:
        if r['_g'] != g: continue
        for k in (a, b):
            if inper(r, k): d[r['_k']][k].append(r['_p'])
    rs = [st.median(v[b]) / st.median(v[a]) - 1 for v in d.values() if len(v[a]) >= minn and len(v[b]) >= minn]
    return len(rs), (st.median(rs) if rs else None), (sum(1 for x in rs if x > 0) / len(rs) if rs else None)
print('\n# 같은 집 값 변화(가운데) — 최근 = 2026년 6~10월 계약')
for g in G:
    for a in ('고점21', '바닥23', '1년전'):
        for mn in (1, 2):
            n, m, up = pairs(g, a, '최근', mn)
            print(f'{g} {a}→최근 (각 {mn}건↑): {n}쌍 · 가운데 {m*100:+.1f}% · 오른 쌍 {up*100:.0f}%')
print('\n# 같은 집 반기별(2021H2 대비)')
HALF = [(f'{y}H{h}', (y*100+1+6*(h-1), y*100+6*h)) for y in range(2022, 2027) for h in (1, 2)]
for g in G:
    out = []
    for lab, (lo, hi) in HALF:
        if lo > 202610: continue
        hi = min(hi, 202610)
        d = C.defaultdict(lambda: C.defaultdict(list))
        for r in rows:
            if r['_g'] != g: continue
            if 202107 <= r['_ym'] <= 202112: d[r['_k']]['a'].append(r['_p'])
            if lo <= r['_ym'] <= hi: d[r['_k']]['b'].append(r['_p'])
        rs = [st.median(v['b']) / st.median(v['a']) - 1 for v in d.values() if v['a'] and v['b']]
        out.append(f'{lab} {len(rs)}쌍 {st.median(rs)*100:+.1f}%')
    print(g, ' | '.join(out))
print('\n# 전용 83~86㎡ 가운데 매매가')
for g in G:
    for k in PER:
        v = [r['_p'] for r in rows if r['_g'] == g and inper(r, k) and 83 <= r['_a'] <= 86]
        print(f'{g} {k}: {len(v)}건 · 가운데 {st.median(v)/10000:.2f}억')
print('\n# 한 달 평균 매매 건수')
for g in G:
    for lab, lo, hi in (('2021년', 202101, 202112), ('2022년', 202201, 202212), ('2023년', 202301, 202312), ('2024년', 202401, 202412), ('2025년', 202501, 202512), ('2026년 1~10월', 202601, 202610)):
        v = [r for r in rows if r['_g'] == g and lo <= r['_ym'] <= hi]; months = len({r['_ym'] for r in v})
        print(f'{g} {lab}: 월평균 {len(v)/months:,.0f}건')
print('\n# 2026년 11월 신고분(최근에서 뺌)')
for g in G: print(g, sum(1 for r in rows if r['_g'] == g and r['_ym'] == 202611), '건')
print('\n# 최근(2026.6~10) 같은 집 짝 중 2021H2보다 비싼 곳 예시(가운데 값 기준, 전용 84㎡ 안팎)')
for g in G:
    d = C.defaultdict(lambda: C.defaultdict(list)); nm = {}
    for r in rows:
        if r['_g'] != g or not (83 <= r['_a'] <= 86): continue
        nm[r['_k']] = r['aptNm']
        for k in ('고점21', '최근'):
            if inper(r, k): d[r['_k']][k].append(r['_p'])
    lst = sorted(((st.median(v['최근'])/st.median(v['고점21'])-1, nm[k], k[1], st.median(v['고점21']), st.median(v['최근']), len(v['고점21']), len(v['최근'])) for k, v in d.items() if v['고점21'] and v['최근']), reverse=True)
    print(g, '84㎡ 짝', len(lst))
    for x in lst[:3] + lst[-3:]: print('  ', f'{x[0]*100:+.1f}%', x[1], f'{x[2]}㎡', f'{x[3]/10000:.2f}억→{x[4]/10000:.2f}억', f'({x[5]}건/{x[6]}건)')
print('\n# 고점 값으로 돌아가려면(같은 집 짝마다 고점21 가운데 / 최근 가운데 - 1 의 가운데)')
for g in G:
    d = C.defaultdict(lambda: C.defaultdict(list))
    for r in rows:
        if r['_g'] != g: continue
        for k in ('고점21', '최근'):
            if inper(r, k): d[r['_k']][k].append(r['_p'])
    rs = [st.median(v['고점21']) / st.median(v['최근']) - 1 for v in d.values() if v['고점21'] and v['최근']]
    print(f'{g}: {len(rs)}쌍 · 가운데 {st.median(rs)*100:+.1f}%')
print('\n# 전용 83~86㎡ 거래 중 준공 2022년 이후 단지 몫·8억원 이상 건수')
for g in G:
    for k in ('고점21', '최근'):
        v = [r for r in rows if r['_g'] == g and inper(r, k) and 83 <= r['_a'] <= 86]
        new = sum(1 for r in v if int(r['buildYear'] or 0) >= 2022)
        hi8 = sum(1 for r in v if r['_p'] >= 80000)
        print(f'{g} {k}: {len(v)}건 · 2022년 이후 준공 {new}건({new/len(v)*100:.0f}%) · 8억원 이상 {hi8}건')
print('\n# 2021H2→최근 같은 집 중 오른 개수')
for g in G:
    d = C.defaultdict(lambda: C.defaultdict(list))
    for r in rows:
        if r['_g'] != g: continue
        for k in ('고점21', '최근'):
            if inper(r, k): d[r['_k']][k].append(r['_p'])
    rs = [st.median(v['최근']) / st.median(v['고점21']) - 1 for v in d.values() if v['고점21'] and v['최근']]
    print(f'{g}: {len(rs)}개 중 오른 {sum(1 for x in rs if x>0)}개')
