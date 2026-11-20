# gimpo1121 — 경기 김포시 41570 아파트 매매 실거래(S1 raw)로 김포 네 동네(한강신도시·풍무·고촌·구도심) 같은 집 2021년 고점 무렵·1년 전 대비 · firemap-write-b 2026-11-20 (hanam1120/calc.py 틀)
# 같은 집 = 같은 단지(aptSeq)·같은 전용면적(1㎡ 반올림). 매매는 해제(cdealType) 뺌.
import json, os, glob, statistics as st, sys, collections as C
sys.stdout.reconfigure(encoding='utf-8')
H = os.path.dirname(os.path.abspath(__file__))
num = lambda s: float(str(s or '0').replace(',', '') or 0)
def grp(u):
    if u in ('장기동', '운양동', '구래동', '마산동'): return '한강신도시'
    if u == '풍무동': return '풍무'
    if u.startswith('고촌읍'): return '고촌'
    if u in ('사우동', '북변동', '감정동', '걸포동'): return '구도심'
    return '기타'
def load(kind):
    out = []
    for p in sorted(glob.glob(os.path.join(H, 'raw', f'41570_*_{kind}.json'))):
        for r in json.load(open(p, encoding='utf-8')):
            r['_g'] = grp(r['umdNm'])
            r['_ym'] = int(r['dealYear']) * 100 + int(r['dealMonth']); r['_a'] = round(num(r['excluUseAr']))
            r['_k'] = (r.get('aptSeq') or r['aptNm'], r['_a']); out.append(r)
    return out
TA = load('trade'); T = [r for r in TA if not r.get('cdealType')]
for r in T: r['_p'] = num(r['dealAmount'])
print('김포시 매매(해제 뺌)', len(T), '건 · 해제', len(TA) - len(T), '건 · 단지', len({r['_k'][0] for r in T}))
print('동네별 매매 건수:', C.Counter(r['_g'] for r in T).most_common())
print('기간 처음·끝:', min(r['_ym'] for r in T), max(r['_ym'] for r in T))
PER = {'1년전': (202506, 202510), '최근': (202606, 202610), '고점21': (202107, 202112), '바닥23': (202301, 202306), '상반21': (202101, 202106)}
def inper(r, k): lo, hi = PER[k]; return lo <= r['_ym'] <= hi
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
    print(f"{lbl}: {len(ps)}쌍 · 가운데 {st.median(rs)*100:+.1f}% · 가운데 금액 {st.median(ds)/10000:+.2f}억 · 오른 쌍 {sum(1 for x in rs if x>0)/len(rs)*100:.0f}% · 넘은 쌍(>=0) {sum(1 for x in rs if x>=0)}개({sum(1 for x in rs if x>=0)/len(rs)*100:.0f}%)")
GS = ['한강신도시', '풍무', '고촌', '구도심']
for a, b, lab in (('고점21', '최근', '2021년 7~12월 → 2026.6~10 (고점 무렵 대비)'), ('1년전', '최근', '1년(2025.6~10 → 2026.6~10)'), ('바닥23', '최근', '2023년 1~6월 → 2026.6~10'), ('상반21', '최근', '2021년 1~6월 → 2026.6~10'), ('고점21', '바닥23', '2021년 7~12월 → 2023년 1~6월 (얼마나 빠졌나)')):
    print(f'\n# 같은 집 매매 {lab}')
    show('김포 전체', pairs(T, a, b))
    for g in GS: show(g, pairs([r for r in T if r['_g'] == g], a, b))
print('\n# 84㎡ 안팎(83~86㎡) 매매 가운데 값')
for g in GS:
    for per in ('고점21', '바닥23', '1년전', '최근'):
        v = [r['_p'] for r in T if r['_g'] == g and inper(r, per) and 83 <= r['_a'] <= 86]
        print(f'{g} {per}: {len(v)}건 {st.median(v)/10000:.2f}억' if v else f'{g} {per}: 0건')
print('\n# 동네별 같은 집 고점 대비 — 84㎡ 안팎, 양쪽 2건 이상, 높은 둘·낮은 둘')
for g in GS:
    ps = sorted([x for x in pairs([r for r in T if r['_g'] == g and 83 <= r['_a'] <= 86], '고점21', '최근') if x[6] >= 2 and x[7] >= 2], reverse=True)
    for x in ps[:2] + ps[-2:]: print('  ', g, f'{x[0]*100:+.1f}%', x[2][0], x[2][1], f'{x[3]}㎡', f'{x[4]/10000:.2f}억→{x[5]/10000:.2f}억', f'({x[6]}건/{x[7]}건)')
print('\n# 반기별 매매 건수(해제 뺌)')
for y in range(2021, 2027):
    for h, (lo, hi) in (('상', (1, 6)), ('하', (7, 12))):
        v = [r for r in T if r['_ym'] // 100 == y and lo <= r['_ym'] % 100 <= hi]
        if v: print(f'{y}{h}', len(v), ' '.join(f"{g}{sum(1 for r in v if r['_g']==g)}" for g in GS))
for lab, lo, hi in (('2021년 6~10월', 202106, 202110), ('2024년 6~10월', 202406, 202410), ('2025년 6~10월', 202506, 202510), ('2026년 6~10월', 202606, 202610)):
    v = [r for r in T if lo <= r['_ym'] <= hi]; print(f'{lab}: {len(v)}건 · 월평균 {len(v)/5:.0f}')
print('\n# 2026년 11월 계약(최근에서 뺌):', sum(1 for r in T if r['_ym'] == 202611), '건')
print('\n# 동네별 단지·건수(최근 6~10월)')
for g in GS:
    v = [r for r in T if r['_g'] == g and inper(r, '최근')]; print(g, len(v), '건 · 단지', len({r['_k'][0] for r in v}))
print('\n# 확인: 고점 대비 넘은 쌍 목록(김포 전체)')
for x in sorted(pairs(T, '고점21', '최근'), reverse=True):
    if x[0] >= 0: print('  ', f'{x[0]*100:+.1f}%', x[2], f'{x[3]}㎡', x[4], x[5], x[6], x[7])
print('\n# 직거래 몫(최근)', C.Counter(r.get('dealingGbn') for r in T if inper(r, '최근')).most_common())
print('\n# 확인: 2021년 하반기가 고점 무렵인가 — 같은 집 반기 사슬(앞 반기 → 다음 반기 가운데 변화)')
HS = [(f'{y}{h}', (y*100+lo, y*100+hi)) for y in range(2021, 2027) for h, lo, hi in (('상', 1, 6), ('하', 7, 12))]
for (la, pa), (lb, pb) in zip(HS, HS[1:]):
    PER['_a'], PER['_b'] = pa, pb
    ps = pairs(T, '_a', '_b')
    if ps: print(f'{la}→{lb}: {len(ps)}쌍 가운데 {st.median([x[0] for x in ps])*100:+.1f}%')
print('\n# 확인: 구도심 84㎡ 가운데 값이 오른 것처럼 보이는 까닭 — 기간별 거래 많은 단지')
for per in ('고점21', '최근'):
    c = C.Counter(r['aptNm'] for r in T if r['_g'] == '구도심' and inper(r, per) and 83 <= r['_a'] <= 86)
    print(per, c.most_common(5))
