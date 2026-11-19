# hanam1120 — 경기 하남시 41450 아파트 매매·전세 실거래(S1·S2 raw)로 하남 안 네 동네(미사·위례·감일·구도심) 같은 집 1년·2021년 고점 대비 · firemap-write-b 2026-11-19 (songdo1119/calc.py 틀)
# 같은 집 = 같은 단지(aptSeq)·같은 전용면적(1㎡ 반올림). 매매는 해제(cdealType) 뺌. 전세 = monthlyRent 0.
import json, os, glob, statistics as st, sys, collections as C
sys.stdout.reconfigure(encoding='utf-8')
H = os.path.dirname(os.path.abspath(__file__))
num = lambda s: float(str(s or '0').replace(',', '') or 0)
G = {'망월동': '미사', '풍산동': '미사', '선동': '미사', '학암동': '위례', '감이동': '감일', '감일동': '감일', '신장동': '구도심', '덕풍동': '구도심', '창우동': '구도심'}
def load(kind):
    out = []
    for p in sorted(glob.glob(os.path.join(H, 'raw', f'41450_*_{kind}.json'))):
        for r in json.load(open(p, encoding='utf-8')):
            r['_g'] = G.get(r['umdNm'], '기타')
            r['_ym'] = int(r['dealYear']) * 100 + int(r['dealMonth']); r['_a'] = round(num(r['excluUseAr']))
            r['_k'] = (r.get('aptSeq') or r['aptNm'], r['_a']); out.append(r)
    return out
TA = load('trade'); T = [r for r in TA if not r.get('cdealType')]
for r in T: r['_p'] = num(r['dealAmount'])
R = load('rent'); J = [r for r in R if num(r['monthlyRent']) == 0]
for r in J: r['_p'] = num(r['deposit'])
print('하남시 매매(해제 뺌)', len(T), '건 · 해제', len(TA) - len(T), '건 · 단지', len({r['_k'][0] for r in T}), '· 전세', len(J), '건')
print('동네별 매매 건수:', C.Counter(r['_g'] for r in T).most_common())
print('기간 처음·끝:', min(r['_ym'] for r in T), max(r['_ym'] for r in T))
PER = {'1년전': (202506, 202510), '최근': (202606, 202610), '고점21': (202107, 202112), '바닥23': (202301, 202306)}
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
GS = ['미사', '위례', '감일', '구도심']
print('\n# 같은 집 매매 1년(2025.6~10 → 2026.6~10)')
show('하남 전체', pairs(T, '1년전', '최근'))
for g in GS: show(g, pairs([r for r in T if r['_g'] == g], '1년전', '최근'))
print('\n# 같은 집 매매 2021년 7~12월 → 2026.6~10 (고점 대비)')
show('하남 전체', pairs(T, '고점21', '최근'))
for g in GS: show(g, pairs([r for r in T if r['_g'] == g], '고점21', '최근'))
print('\n# 같은 집 매매 2023년 1~6월(바닥) → 2026.6~10')
show('하남 전체', pairs(T, '바닥23', '최근'))
for g in GS: show(g, pairs([r for r in T if r['_g'] == g], '바닥23', '최근'))
print('\n# 같은 집 전세 1년')
show('하남 전체', pairs(J, '1년전', '최근'))
for g in GS: show(g, pairs([r for r in J if r['_g'] == g], '1년전', '최근'))
print('\n# 84㎡ 안팎(83~86㎡) 매매 가운데 값')
for g in GS:
    for per in ('고점21', '1년전', '최근'):
        v = [r['_p'] for r in T if r['_g'] == g and inper(r, per) and 83 <= r['_a'] <= 86]
        print(f'{g} {per}: {len(v)}건 {st.median(v)/10000:.2f}억' if v else f'{g} {per}: 0건')
print('\n# 동네별 1년 같은 집 매매 — 가장 많이 오른·덜 오른 예(84㎡ 안팎, 양쪽 2건 이상)')
for g in GS:
    ps = sorted([x for x in pairs([r for r in T if r['_g'] == g and 83 <= r['_a'] <= 86], '1년전', '최근') if x[6] >= 2 and x[7] >= 2], reverse=True)
    for x in ps[:2] + ps[-1:]: print('  ', g, f'{x[0]*100:+.1f}%', x[2][0], x[2][1], f'{x[3]}㎡', f'{x[4]/10000:.2f}억→{x[5]/10000:.2f}억', f'({x[6]}건/{x[7]}건)')
print('\n# 월별 매매 건수(해제 뺌)')
m = C.Counter(r['_ym'] for r in T)
for ym in sorted(m):
    if ym >= 202501: print(ym, m[ym], ' '.join(f"{g}{sum(1 for r in T if r['_ym']==ym and r['_g']==g)}" for g in GS))
for lab, lo, hi in (('2024년 6~10월', 202406, 202410), ('2025년 6~10월', 202506, 202510), ('2025년 11월~2026년 3월', 202511, 202603), ('2026년 6~10월', 202606, 202610)):
    v = [r for r in T if lo <= r['_ym'] <= hi]; print(f'{lab}: {len(v)}건 · 월평균 {len(v)/5:.0f}')
print('\n# 2026년 11월 계약(최근에서 뺌):', sum(1 for r in T if r['_ym'] == 202611), '건')
print('\n# 동네별 단지·건수(최근 6~10월)')
for g in GS:
    v = [r for r in T if r['_g'] == g and inper(r, '최근')]; print(g, len(v), '건 · 단지', len({r['_k'][0] for r in v}))
print('\n# 직거래 몫(최근)', C.Counter(r.get('dealingGbn') for r in T if inper(r, '최근')).most_common())
print('\n# 확인: 1년 같은 집 매매 내린·그대로 쌍')
for x in pairs(T, '1년전', '최근'):
    if x[0] <= 0: print('  ', f'{x[0]*100:+.1f}%', x[2], f'{x[3]}㎡', x[4], x[5])
print('\n# 확인: 위례 84㎡ 안팎 최근 거래 단지')
print(C.Counter(r['aptNm'] for r in T if r['_g'] == '위례' and inper(r, '최근') and 83 <= r['_a'] <= 86))
print('\n# 확인: 미사 84㎡ 안팎 최근 단지별 가운데(3건 이상)')
d = C.defaultdict(list)
for r in T:
    if r['_g'] == '미사' and inper(r, '최근') and 83 <= r['_a'] <= 86: d[r['aptNm']].append(r['_p'])
v = sorted((st.median(x), k, len(x)) for k, x in d.items() if len(x) >= 3)
for m, k, n in v[:2] + v[-2:]: print('  ', k, n, '건', m / 10000, '억')
print('\n# 표지용: 신도시 셋(미사·위례·감일) 묶음 같은 집 매매 1년')
show('신도시 셋', pairs([r for r in T if r['_g'] in ('미사', '위례', '감일')], '1년전', '최근'))
show('구도심', pairs([r for r in T if r['_g'] == '구도심'], '1년전', '최근'))
