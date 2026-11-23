# gmnew1125 — 경기 광명시 41210 아파트 매매 실거래(S1 raw)로 '2019년 이후 지은 단지(새 단지)' vs 그 전 단지 비교 · firemap-write-b 2026-11-23 (sanbon1123/calc.py 틀)
# h4s_new15 쇼츠(광명 15억 = 2019년 이후 새 단지 84㎡대 24건 가운데 값 14.71억) 짝 글 — 쇼츠에 없던 새 계산: 새 단지 웃돈 추이·같은 집 1년·2021년 하반기 대비·단지별
# 84㎡대 = 전용 80~85㎡(H-4와 같음). 매매는 해제(cdealType) 뺌. 같은 집 = 같은 단지(aptSeq)·같은 전용면적(1㎡ 반올림).
import json, os, glob, statistics as st, sys, collections as C
sys.stdout.reconfigure(encoding='utf-8')
H = os.path.dirname(os.path.abspath(__file__))
num = lambda s: float(str(s or '0').replace(',', '') or 0)
TA = []
for p in sorted(glob.glob(os.path.join(H, 'raw', '41210_*_trade.json'))):
    for r in json.load(open(p, encoding='utf-8')):
        r['_ym'] = int(r['dealYear']) * 100 + int(r['dealMonth']); r['_ar'] = num(r['excluUseAr']); r['_a'] = round(r['_ar'])
        r['_k'] = (r.get('aptSeq') or r['aptNm'], r['_a']); r['_by'] = int(r.get('buildYear') or 0); TA.append(r)
T = [r for r in TA if not r.get('cdealType')]
for r in T: r['_p'] = num(r['dealAmount'])
print('광명시 매매(해제 뺌)', len(T), '· 해제', len(TA) - len(T), '· 단지', len({r['_k'][0] for r in T}))
print('기간', min(r['_ym'] for r in T), max(r['_ym'] for r in T))
NEW = lambda r: r['_by'] >= 2019
OLD = lambda r: 0 < r['_by'] <= 2018
A84 = lambda r: 80 <= r['_ar'] <= 85
def med(v): return st.median(v) / 10000 if v else float('nan')
def inr(r, lo, hi): return lo <= r['_ym'] <= hi

print('\n# 1. 84㎡대 가운데 값(억) — 새 단지(2019년 이후 준공) / 그 전 / 전체')
for lab, lo, hi in (('쇼츠 기간 2026.07~09', 202607, 202609), ('최근 2026.07~10', 202607, 202610), ('1년 전 2025.07~10', 202507, 202510)):
    v = [r for r in T if inr(r, lo, hi) and A84(r)]
    n = [r['_p'] for r in v if NEW(r)]; o = [r['_p'] for r in v if OLD(r)]; a = [r['_p'] for r in v]
    print(f'{lab}: 새 {len(n)}건 {med(n):.2f} · 그 전 {len(o)}건 {med(o):.2f} · 전체 {len(a)}건 {med(a):.2f} · 새/그전 {med(n)/med(o):.2f}배 · 차이 {med(n)-med(o):.2f}억')

print('\n# 2. 반기별 84㎡대 가운데 값(억) 새 단지 vs 그 전 — 차이·배수 (단지 섞임 주의)')
for y in range(2021, 2027):
    for h, lo, hi in (('상', 1, 6), ('하', 7, 12)):
        v = [r for r in T if r['_ym'] // 100 == y and lo <= r['_ym'] % 100 <= hi and A84(r) and r['_ym'] != 202611]
        n = [r['_p'] for r in v if NEW(r)]; o = [r['_p'] for r in v if OLD(r)]
        if n and o: print(f'{y}{h}: 새 {len(n)}건 {med(n):.2f} · 그 전 {len(o)}건 {med(o):.2f} · 차이 {med(n)-med(o):.2f}억 · {med(n)/med(o):.2f}배 · 새 단지 몫 {len(n)/len(v)*100:.0f}%')

PER = {'1년전': (202506, 202510), '최근': (202606, 202610), '고점21': (202107, 202112), '바닥23': (202301, 202306)}
def inper(r, k): lo, hi = PER[k]; return lo <= r['_ym'] <= hi
def pairs(rows, a, b):
    d = C.defaultdict(lambda: C.defaultdict(list)); nm = {}
    for r in rows:
        nm[r['_k']] = (r['aptNm'], r['umdNm'], r['_by'])
        for k in (a, b):
            if inper(r, k): d[r['_k']][k].append(r['_p'])
    return [(st.median(v[b]) / st.median(v[a]) - 1, st.median(v[b]) - st.median(v[a]), nm[k], k[1], st.median(v[a]), st.median(v[b]), len(v[a]), len(v[b])) for k, v in d.items() if v[a] and v[b]]
def show(lbl, ps):
    if not ps: print(lbl, '0쌍'); return
    rs = [x[0] for x in ps]; ds = [x[1] for x in ps]
    print(f"{lbl}: {len(ps)}쌍 · 가운데 {st.median(rs)*100:+.1f}% · 가운데 금액 {st.median(ds)/10000:+.2f}억 · 오른 쌍 {sum(1 for x in rs if x>0)}/{len(rs)} · >=0 {sum(1 for x in rs if x>=0)}개")
print('\n# 3. 같은 집 비교(같은 단지·같은 넓이, 모든 넓이)')
for lab, f in (('새 단지(2019~)', NEW), ('2010~2018', lambda r: 2010 <= r['_by'] <= 2018), ('2000~2009', lambda r: 2000 <= r['_by'] <= 2009), ('1999년까지', lambda r: 0 < r['_by'] <= 1999), ('그 전 전체(~2018)', OLD), ('광명 전체', lambda r: True)):
    v = [r for r in T if f(r)]
    print(f'## {lab}')
    for a, b in (('1년전', '최근'), ('고점21', '최근'), ('바닥23', '최근')):
        show(f'  {a}→{b}', pairs(v, a, b))

print('\n# 4. 새 단지 목록(2019년 이후 준공) — 1년(2025.11~2026.10) 84㎡대 건수·가운데 값, 전체 건수')
yr = [r for r in T if 202511 <= r['_ym'] <= 202610 and NEW(r)]
g = C.defaultdict(list); ga = C.Counter(); meta = {}
for r in yr:
    meta[r['aptNm']] = (r['umdNm'], r['_by']); ga[r['aptNm']] += 1
    if A84(r): g[r['aptNm']].append(r['_p'])
for nm, c in ga.most_common():
    v = g.get(nm, [])
    print(f'  {nm} ({meta[nm][0]}, {meta[nm][1]}) 전체 {c}건 · 84㎡대 {len(v)}건 {med(v):.2f}억' + (f' (최저 {min(v)/10000:.2f}~최고 {max(v)/10000:.2f})' if v else ''))
print('  새 단지 수', len(ga), '· 1년 거래', sum(ga.values()))
print('  새 단지 전체(1년, 해제 뺌) 준공 연도별 단지 수', sorted(C.Counter(meta[n][1] for n in ga).items()))

print('\n# 5. 쇼츠 기간 24건 다시 셈(2026.07~09, 84㎡대, 새 단지) 단지별')
v = [r for r in T if inr(r, 202607, 202609) and A84(r) and NEW(r)]
print('  ', C.Counter(r['aptNm'] for r in v).most_common(), len(v))

print('\n# 6. 최근 석 달 새 단지 84㎡대 15억 넘은 거래')
v = [r['_p'] for r in T if inr(r, 202608, 202610) and A84(r) and NEW(r)]
print('  ', len(v), '건 중 15억 이상', sum(1 for p in v if p >= 150000), '· 최고', max(v)/10000 if v else None)
print('\n# 직거래(최근 2026.06~10 새 단지)', C.Counter(r.get('dealingGbn') for r in T if inper(r, '최근') and NEW(r)).most_common())
print('# 11월 계약 건수(반기·같은 집 계산에서 뺌)', sum(1 for r in T if r['_ym'] == 202611))
print('# 월별 건수 2026', [(ym, sum(1 for r in T if r['_ym'] == ym)) for ym in range(202601, 202612)])

print('\n# 7. 같은 집 1년 — 84㎡대(80~85㎡)만으로 다시(넓이 섞임 확인)')
for lab, f in (('새 단지(2019~)', NEW), ('2010~2018', lambda r: 2010 <= r['_by'] <= 2018), ('2000~2009', lambda r: 2000 <= r['_by'] <= 2009), ('1999년까지', lambda r: 0 < r['_by'] <= 1999)):
    show(f'  {lab} 84㎡대 1년', pairs([r for r in T if f(r) and A84(r)], '1년전', '최근'))
print('\n# 8. 같은 집 1년 단지별(가운데) — 새 단지 / 1999년까지(쌍 많은 순)')
for lab, f in (('새 단지', NEW), ('1999년까지', lambda r: 0 < r['_by'] <= 1999)):
    g = C.defaultdict(list)
    for x in pairs([r for r in T if f(r)], '1년전', '최근'): g[(x[2][0], x[2][1], x[2][2])].append(x[0])
    print(' ##', lab)
    for k, v in sorted(g.items(), key=lambda kv: -len(kv[1]))[:12]: print(f'   {k[0]} ({k[1]}, {k[2]}) 평형 {len(v)}개 가운데 {st.median(v)*100:+.1f}%')
print('\n# 9. 1999년까지 단지 동별 구성(같은 집 1년 쌍)')
print('  ', C.Counter(x[2][1] for x in pairs([r for r in T if 0 < r['_by'] <= 1999], '1년전', '최근')).most_common())
print('\n# 10. 쇼츠 24건에서 유-플래닛태영데시앙 뺀 12건 가운데 값')
v = [r for r in T if inr(r, 202607, 202609) and A84(r) and NEW(r)]
w = [r['_p'] for r in v if r['aptNm'] != '유-플래닛태영데시앙']; u = [r['_p'] for r in v if r['aptNm'] == '유-플래닛태영데시앙']
print(f'   데시앙 {len(u)}건 {med(u):.2f}억 · 나머지 {len(w)}건 {med(w):.2f}억 · 전체 {med(u+w):.2f}억')
print('\n# 11. 2025하 vs 2026하 새 단지 84㎡대 거래 단지 구성(건수)')
for lo, hi in ((202507, 202510), (202607, 202610)):
    print('  ', lo, C.Counter(r['aptNm'] for r in T if inr(r, lo, hi) and A84(r) and NEW(r)).most_common())
