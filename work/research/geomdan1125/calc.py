# geomdan1125 — 인천 28290(검단: 당하·원당·마전·불로·왕길동 등) 아파트 매매 실거래(S1 raw)로 같은 집 고점 무렵 대비 지금 · firemap-write-b 2026-11-24 (sejong1124/calc.py 틀) · 묶음 = 준공 2019년 이후(새 단지)·그 전(옛 단지)
# 같은 집 = 같은 단지(aptSeq)·같은 전용면적(1㎡ 반올림). 매매는 해제(cdealType) 뺌. 묶음은 법정동 이름 그대로(생활권 번호는 안 씀).
import json, os, glob, statistics as st, sys, collections as C
sys.stdout.reconfigure(encoding='utf-8')
H = os.path.dirname(os.path.abspath(__file__))
num = lambda s: float(str(s or '0').replace(',', '') or 0)
def load(kind):
    out = []
    for p in sorted(glob.glob(os.path.join(H, 'raw', f'28290_*_{kind}.json'))):
        for r in json.load(open(p, encoding='utf-8')):
            r['_town'] = '새단지' if int(r.get('buildYear') or 0) >= 2019 else '옛단지'
            r['_ym'] = int(r['dealYear']) * 100 + int(r['dealMonth']); r['_a'] = round(num(r['excluUseAr']))
            r['_k'] = (r.get('aptSeq') or r['aptNm'], r['_a']); out.append(r)
    return out
TA = load('trade'); T = [r for r in TA if not r.get('cdealType')]
for r in T: r['_p'] = num(r['dealAmount'])
print('검단 매매(해제 뺌)', len(T), '건 · 해제', len(TA) - len(T), '건 · 단지', len({r['_k'][0] for r in T}))
print('기간 처음·끝:', min(r['_ym'] for r in T), max(r['_ym'] for r in T))
print('동/읍면 건수:', C.Counter(r['_town'] for r in T).most_common())
HS = [(f'{y}{h}', (y*100+lo, y*100+hi)) for y in range(2020, 2027) for h, lo, hi in (('상', 1, 6), ('하', 7, 12))]
PER = dict(HS)
PER.update({'1년전': (202506, 202510), '최근': (202606, 202610)})
def inper(r, k): lo, hi = PER[k]; return lo <= r['_ym'] <= hi
def pairs(rows, a, b):
    d = C.defaultdict(lambda: C.defaultdict(list)); nm = {}
    for r in rows:
        nm[r['_k']] = (r['aptNm'], r['umdNm'])
        for k in (a, b):
            if inper(r, k): d[r['_k']][k].append(r['_p'])
    return [(st.median(v[b]) / st.median(v[a]) - 1, st.median(v[b]) - st.median(v[a]), nm[k], k[1], st.median(v[a]), st.median(v[b]), len(v[a]), len(v[b])) for k, v in d.items() if v[a] and v[b]]
def show(lbl, ps, back=False):
    if not ps: print(lbl, '0쌍'); return None
    rs = [x[0] for x in ps]; ds = [x[1] for x in ps]; m = st.median(rs)
    extra = f' · 되찾으려면 {(1/(1+m)-1)*100:+.1f}%' if back and m < 0 else ''
    print(f"{lbl}: {len(ps)}쌍 · 가운데 {m*100:+.1f}% · 가운데 금액 {st.median(ds)/10000:+.2f}억 · 넘은 쌍(>=0) {sum(1 for x in rs if x>=0)}개({sum(1 for x in rs if x>=0)/len(rs)*100:.0f}%){extra}")
    return m
print('\n# 반기별 매매 건수(해제 뺌)·84㎡ 안팎(83~86㎡) 가운데 값')
for lab, (lo, hi) in HS:
    v = [r for r in T if lo <= r['_ym'] <= hi]; x = [r['_p'] for r in v if 83 <= r['_a'] <= 86]
    if v: print(lab, len(v), '건 · 동 지역 84㎡', len(x), '건', f'{st.median(x)/10000:.2f}억' if x else '')
print('\n# 같은 집 반기 사슬(앞 반기 → 다음 반기 가운데 변화) — 고점 반기 찾기')
for (la, _), (lb, _) in zip(HS, HS[1:]):
    ps = pairs(T, la, lb)
    if ps: print(f'{la}→{lb}: {len(ps)}쌍 가운데 {st.median([x[0] for x in ps])*100:+.1f}%')
print('\n# 같은 집: 각 반기 → 최근(2026.6~10)')
for la, _ in HS[:-2]:
    show(f'{la}→최근', pairs(T, la, '최근'), back=True)
show('1년(2025.6~10→2026.6~10)', pairs(T, '1년전', '최근'))
PK = sys.argv[1] if len(sys.argv) > 1 else '2021상'
print(f'\n# 고점 반기 {PK} 기준 — 동 지역 / 읍면 / 동별(양쪽 쌍 10개 이상)')
show('검단 전체', pairs(T, PK, '최근'), back=True)
for t in ('새단지', '옛단지'): show(t + ' 지역', pairs([r for r in T if r['_town'] == t], PK, '최근'), back=True)
rows = []
for u in sorted({r['umdNm'] for r in T}):
    ps = pairs([r for r in T if r['umdNm'] == u], PK, '최근')
    if len(ps) >= 10: rows.append((st.median([x[0] for x in ps]), u, len(ps)))
for m, u, n in sorted(rows, reverse=True): print(f'  {u}: {n}쌍 가운데 {m*100:+.1f}% · 되찾으려면 {(1/(1+m)-1)*100:+.1f}%')
print(f'\n# 1년 동별(양쪽 쌍 10개 이상)')
for u in sorted({r['umdNm'] for r in T}):
    ps = pairs([r for r in T if r['umdNm'] == u], '1년전', '최근')
    if len(ps) >= 10: print(f'  {u}: {len(ps)}쌍 가운데 {st.median([x[0] for x in ps])*100:+.1f}%')
print(f'\n# 84㎡ 안팎 같은 집 {PK}→최근, 양쪽 2건 이상 — 많이 빠진 셋·덜 빠진 셋')
ps = sorted([x for x in pairs([r for r in T if 83 <= r['_a'] <= 86], PK, '최근') if x[6] >= 2 and x[7] >= 2], reverse=True)
print('쌍', len(ps))
for x in ps[:3] + ps[-3:]: print('  ', f'{x[0]*100:+.1f}%', x[2][0], x[2][1], f'{x[3]}㎡', f'{x[4]/10000:.2f}억→{x[5]/10000:.2f}억', f'({x[6]}건/{x[7]}건)')
print('\n# 넓이별(같은 집) — 60㎡ 이하 / 60~85 / 85 초과')
for lab, f in (('60㎡ 이하', lambda a: a <= 60), ('60~85㎡', lambda a: 60 < a <= 85), ('85㎡ 초과', lambda a: a > 85)):
    show(lab, pairs([r for r in T if f(r['_a'])], PK, '최근'), back=True)
print('\n# 기간별 건수: 2020.6~10 / 2021.6~10 / 2025.6~10 / 2026.6~10 월평균')
for lab, lo, hi in (('2020년 6~10월', 202006, 202010), ('2021년 6~10월', 202106, 202110), ('2025년 6~10월', 202506, 202510), ('2026년 6~10월', 202606, 202610)):
    v = [r for r in T if lo <= r['_ym'] <= hi]; print(f'{lab}: {len(v)}건 · 월평균 {len(v)/5:.0f}')
print('# 2026년 11월 계약(최근에서 뺌):', sum(1 for r in T if r['_ym'] == 202611), '건')
print('# 직거래 몫(최근)', C.Counter(r.get('dealingGbn') for r in T if inper(r, '최근')).most_common())

print('\n# 가운데 값이 오른 까닭 — 84㎡ 안팎 거래 중 새 단지(2019년 이후 준공) 몫과 묶음별 가운데 값')
for lab, (lo, hi) in HS:
    v = [r for r in T if lo <= r['_ym'] <= hi and 83 <= r['_a'] <= 86]
    n = [r['_p'] for r in v if r['_town'] == '새단지']; o = [r['_p'] for r in v if r['_town'] == '옛단지']
    if v: print(lab, f"84㎡ {len(v)}건 · 새 단지 {len(n)}건({len(n)/len(v)*100:.0f}%)", f"새 {st.median(n)/10000:.2f}억" if n else '', f"옛 {st.median(o)/10000:.2f}억" if o else '')
print('\n# 새 단지 같은 집: 2023상·2024상 → 최근')
for la in ('2023상', '2024상', '2025상'):
    show(f'새단지 {la}→최근', pairs([r for r in T if r['_town'] == '새단지'], la, '최근'))
    show(f'옛단지 {la}→최근', pairs([r for r in T if r['_town'] == '옛단지'], la, '최근'))
print('\n# 최근(2026.6~10) 거래 새 단지 몫', f"{sum(1 for r in T if inper(r,'최근') and r['_town']=='새단지')/sum(1 for r in T if inper(r,'최근'))*100:.0f}%", '· 새 단지 수', len({r['_k'][0] for r in T if r['_town']=='새단지'}))
print('# 준공 연도별 최근 거래 건수', sorted(C.Counter(r['buildYear'] for r in T if inper(r,'최근')).items()))
print('\n# 1년(2025.6~10→2026.6~10) 같은 집 84㎡ 안팎, 양쪽 2건 이상 — 많이 오른 셋·많이 내린 셋')
ps = sorted([x for x in pairs([r for r in T if 83 <= r['_a'] <= 86], '1년전', '최근') if x[6] >= 2 and x[7] >= 2], reverse=True)
print('쌍', len(ps), '· 10% 넘게 오른 쌍', sum(1 for x in ps if x[0] > 0.10), '· 10% 넘게 내린 쌍', sum(1 for x in ps if x[0] < -0.10))
for x in ps[:3] + ps[-3:]: print('  ', f'{x[0]*100:+.1f}%', x[2][0], x[2][1], f'{x[3]}㎡', f'{x[4]/10000:.2f}억→{x[5]/10000:.2f}억', f'({x[6]}건/{x[7]}건)')
print('\n# 최근(2026.6~10) 84㎡ 안팎 거래 많은 단지 다섯(준공)')
cnt = C.Counter((r['aptNm'], r['umdNm'], r['buildYear']) for r in T if inper(r, '최근') and 83 <= r['_a'] <= 86)
for (a, u, y), n in cnt.most_common(5): print('  ', a, u, y, n, '건', f"{st.median([r['_p'] for r in T if inper(r,'최근') and r['aptNm']==a and 83<=r['_a']<=86])/10000:.2f}억")
print('\n# 1년 전(2025.6~10) 84㎡ 가운데 값 vs 최근 — 전체', f"{st.median([r['_p'] for r in T if inper(r,'1년전') and 83<=r['_a']<=86])/10000:.2f}억 → {st.median([r['_p'] for r in T if inper(r,'최근') and 83<=r['_a']<=86])/10000:.2f}억",
      '· 새 단지 몫', f"{sum(1 for r in T if inper(r,'1년전') and 83<=r['_a']<=86 and r['_town']=='새단지')/sum(1 for r in T if inper(r,'1년전') and 83<=r['_a']<=86)*100:.0f}% → {sum(1 for r in T if inper(r,'최근') and 83<=r['_a']<=86 and r['_town']=='새단지')/sum(1 for r in T if inper(r,'최근') and 83<=r['_a']<=86)*100:.0f}%")
for t in ('새단지', '옛단지'):
    a = [r['_p'] for r in T if inper(r,'1년전') and 83<=r['_a']<=86 and r['_town']==t]; b = [r['_p'] for r in T if inper(r,'최근') and 83<=r['_a']<=86 and r['_town']==t]
    print(f'  {t} 84㎡ 가운데 {st.median(a)/10000:.2f}억({len(a)}건) → {st.median(b)/10000:.2f}억({len(b)}건)')
print('\n# 1년 같은 집 새/옛 단지')
for t in ('새단지', '옛단지'): show(f'1년 {t}', pairs([r for r in T if r['_town'] == t], '1년전', '최근'))
print('# 새 단지 준공 연도(전 기간 거래)', sorted(C.Counter(r['buildYear'] for r in T if r['_town']=='새단지').items()))
for nm in ('힐스테이트신검단센트럴', '풍경채'):
    v = [r for r in T if nm in r['aptNm'].replace(' ', '') and 83 <= r['_a'] <= 86]
    print('#', nm, '84㎡ 1년전', sum(1 for r in v if inper(r,'1년전')), '건 · 최근', sum(1 for r in v if inper(r,'최근')), '건 · 단지', sorted({(r['aptNm'], r['buildYear']) for r in v}))
