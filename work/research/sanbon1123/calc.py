# sanbon1123 — 경기 군포시 41410 아파트 매매 실거래(S1 raw)로 산본 재건축 선도지구 6개 단지 vs 나머지 산본동 옛 단지(1996년까지 준공) 같은 집 비교 · firemap-write-b 2026-11-23 (bundang1122/calc.py 틀)
# 같은 집 = 같은 단지(aptSeq)·같은 전용면적(1㎡ 반올림). 매매는 해제(cdealType) 뺌.
# 선도지구(2024-11-27 국토부·군포시 발표): 11구역 자이백합·삼성장미·산본주공11(2,758가구), 9-2구역 한양백두·동성백두·극동백두(1,862가구) — 단지 이름은 서울신문(2차). 실거래 자료 이름: 백합·삼성장미·주공11 / 한양백두·백두(동성)·백두(극동)
import json, os, glob, statistics as st, sys, collections as C
sys.stdout.reconfigure(encoding='utf-8')
H = os.path.dirname(os.path.abspath(__file__))
num = lambda s: float(str(s or '0').replace(',', '') or 0)
TA = []
for p in sorted(glob.glob(os.path.join(H, 'raw', '41410_*_trade.json'))):
    for r in json.load(open(p, encoding='utf-8')):
        r['_ym'] = int(r['dealYear']) * 100 + int(r['dealMonth']); r['_a'] = round(num(r['excluUseAr']))
        r['_k'] = (r.get('aptSeq') or r['aptNm'], r['_a']); TA.append(r)
T = [r for r in TA if not r.get('cdealType')]
for r in T: r['_p'] = num(r['dealAmount'])
S = [r for r in T if r['umdNm'] == '산본동']
print('군포시 매매(해제 뺌)', len(T), '· 해제', len(TA) - len(T), '· 산본동', len(S), '건 · 산본동 단지', len({r['_k'][0] for r in S}))
print('기간', min(r['_ym'] for r in T), max(r['_ym'] for r in T))
PER = {'1년전': (202506, 202510), '최근': (202606, 202610), '고점21': (202107, 202112), '바닥23': (202301, 202306), '발표전': (202406, 202410)}
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
    print(f"{lbl}: {len(ps)}쌍 · 가운데 {st.median(rs)*100:+.1f}% · 가운데 금액 {st.median(ds)/10000:+.2f}억 · 오른 쌍 {sum(1 for x in rs if x>0)/len(rs)*100:.0f}% · 고점 이상(>=0) {sum(1 for x in rs if x>=0)}개")
SD11 = {'백합', '삼성장미', '주공11'}; SD92 = {'한양백두', '백두(동성)', '백두(극동)'}; SD = SD11 | SD92
old = lambda r: int(r.get('buildYear') or 0) <= 1996
sd = [r for r in S if r['aptNm'] in SD]; ot = [r for r in S if r['aptNm'] not in SD and old(r)]; nw = [r for r in S if int(r.get('buildYear') or 0) >= 1997]
print('선도지구 단지', sorted({(r['aptNm'], r['buildYear']) for r in sd}), len(sd), '건 · 나머지 옛 단지', len({r['aptNm'] for r in ot}), '곳', len(ot), '건')
for lab, v in (('선도지구 6단지', sd), ('  11구역', [r for r in sd if r['aptNm'] in SD11]), ('  9-2구역', [r for r in sd if r['aptNm'] in SD92]), ('나머지 옛 단지(1996년까지)', ot), ('1997년 이후 준공', nw), ('산본동 전체', S)):
    print(f'\n## {lab}')
    for a, b in (('1년전', '최근'), ('발표전', '최근'), ('고점21', '최근'), ('바닥23', '최근'), ('고점21', '바닥23')):
        show(f'{a}→{b}', pairs(v, a, b))
    for ar, lo, hi in (('59㎡안팎', 57, 60), ('84㎡안팎', 83, 86)):
        print('  ', ar, ' · '.join(f"{per} {len(x)}건 {st.median(x)/10000:.2f}억" if x else f'{per} 0건' for per in ('고점21', '바닥23', '1년전', '최근') for x in [[r['_p'] for r in v if inper(r, per) and lo <= r['_a'] <= hi]]))
print('\n# 단지별 1년(같은 집, 양쪽 1건 이상) — 선도지구')
for x in sorted(pairs(sd, '1년전', '최근'), reverse=True): print('  ', f'{x[0]*100:+.1f}%', x[2], f'{x[3]}㎡', f'{x[4]/10000:.2f}→{x[5]/10000:.2f}억', f'({x[6]}/{x[7]}건)')
print('\n# 나머지 옛 단지 1년 높은 5·낮은 5(양쪽 2건 이상)')
ps = sorted([x for x in pairs(ot, '1년전', '최근') if x[6] >= 2 and x[7] >= 2], reverse=True)
for x in ps[:5] + ps[-5:]: print('  ', f'{x[0]*100:+.1f}%', x[2], f'{x[3]}㎡', f'{x[4]/10000:.2f}→{x[5]/10000:.2f}억', f'({x[6]}/{x[7]}건)')
print('\n# 반기별 건수 산본동 / 선도지구')
for y in range(2021, 2027):
    for h, (lo, hi) in (('상', (1, 6)), ('하', (7, 12))):
        v = [r for r in S if r['_ym'] // 100 == y and lo <= r['_ym'] % 100 <= hi]
        if v: print(f'{y}{h}', len(v), '/', sum(1 for r in v if r['aptNm'] in SD))
print('\n# 같은 집 반기 사슬(산본동 전체)')
HS = [(f'{y}{h}', (y*100+lo, y*100+hi)) for y in range(2021, 2027) for h, lo, hi in (('상', 1, 6), ('하', 7, 12))]
for (la, pa), (lb, pb) in zip(HS, HS[1:]):
    PER['_a'], PER['_b'] = pa, pb; ps = pairs(S, '_a', '_b')
    if ps: print(f'{la}→{lb}: {len(ps)}쌍 {st.median([x[0] for x in ps])*100:+.1f}%')
print('\n# 직거래 몫(최근)', C.Counter(r.get('dealingGbn') for r in S if inper(r, '최근')).most_common())
print('# 11월 계약(최근에서 뺌)', sum(1 for r in S if r['_ym'] == 202611))
x = [r['_p'] for r in S if inper(r, '최근')]
print('# 최근 산본동 매매 금액 구간: 15억 이하', sum(1 for p in x if p <= 150000), '/', len(x), '· 가운데', st.median(x)/10000)
print('\n# 확인: 넓이 섞임(선도지구는 90㎡ 넘는 집이 많다) — 85㎡ 넘는 집끼리·60㎡ 이하끼리 1년')
for lab, f in (('85㎡ 초과', lambda r: r['_a'] > 85), ('60㎡ 이하', lambda r: r['_a'] <= 60)):
    show(f'  선도지구 {lab}', pairs([r for r in sd if f(r)], '1년전', '최근')); show(f'  나머지 옛 단지 {lab}', pairs([r for r in ot if f(r)], '1년전', '최근'))
    show(f'  선도지구 {lab} 고점', pairs([r for r in sd if f(r)], '고점21', '최근')); show(f'  나머지 옛 단지 {lab} 고점', pairs([r for r in ot if f(r)], '고점21', '최근'))
print('# 나머지 옛 단지 85㎡ 초과 단지:', sorted({r['aptNm'] for r in ot if r['_a'] > 85}))
