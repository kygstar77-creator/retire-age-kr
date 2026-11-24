# gwanggyo1125 — 국토부 아파트 매매 실거래(S1 raw) 수원 영통구 41117·용인 수지구 41465로 광교신도시 수원 쪽 vs 용인 쪽 vs 영통·수지 옛 단지 같은 집 비교 · firemap-write 2026-11-25 (sanbon1123/calc.py 틀)
# 같은 집 = 같은 단지(aptSeq)·같은 전용면적(1㎡ 반올림). 매매는 해제(cdealType) 뺌.
# 광교 수원 쪽 = 이의동·하동 전부 + 원천동 이름에 '광교' 든 단지 · 광교 용인 쪽 = 상현동 2011년 이후 준공·이름에 '광교' 든 단지 (우리 정의, 한계에 적음)
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
print('영통구+수지구 매매(해제 뺌)', len(T), '· 해제', len(TA) - len(T), '· 기간', min(r['_ym'] for r in T), max(r['_ym'] for r in T))
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
gw_s = lambda r: r['sggCd'] == '41117' and (r['umdNm'] in ('이의동', '하동') or (r['umdNm'] == '원천동' and '광교' in r['aptNm']))
gw_y = lambda r: r['sggCd'] == '41465' and r['umdNm'] == '상현동' and r['_by'] >= 2011 and '광교' in r['aptNm']
GS = [r for r in T if gw_s(r)]; GY = [r for r in T if gw_y(r)]
YO = [r for r in T if r['umdNm'] in ('영통동', '매탄동') and r['_by'] <= 2005]
SO = [r for r in T if r['sggCd'] == '41465' and not gw_y(r) and r['_by'] <= 2005]
for lab, v in (('광교 수원 쪽', GS), ('광교 용인 쪽', GY)):
    print(lab, '단지', len({r['aptNm'] for r in v}), sorted({(r['umdNm'], r['aptNm'], r['_by']) for r in v}))
print('영통 옛 단지(영통·매탄동 2005년까지)', len({r['aptNm'] for r in YO}), '곳', len(YO), '건 · 수지 옛 단지(2005년까지, 광교 빼고)', len({r['aptNm'] for r in SO}), '곳', len(SO), '건')
G = GS + GY
for lab, v in (('광교 전체', G), ('광교 수원 쪽', GS), ('광교 용인 쪽', GY), ('영통 옛 단지', YO), ('수지 옛 단지', SO)):
    print(f'\n## {lab} · {len(v)}건 · 단지 {len({r["aptNm"] for r in v})}')
    for a, b in (('1년전', '최근'), ('고점21', '최근'), ('바닥23', '최근'), ('고점21', '바닥23')):
        show(f'{a}→{b}', pairs(v, a, b))
    for ar, lo, hi in (('59㎡안팎', 57, 60), ('84㎡안팎', 83, 86)):
        print('  ', ar, ' · '.join(f"{per} {len(x)}건 {st.median(x)/10000:.2f}억" if x else f'{per} 0건' for per in ('고점21', '바닥23', '1년전', '최근') for x in [[r['_p'] for r in v if inper(r, per) and lo <= r['_a'] <= hi]]))
print('\n# 광교 단지별 1년(같은 집, 양쪽 2건 이상)')
for x in sorted([x for x in pairs(G, '1년전', '최근') if x[6] >= 2 and x[7] >= 2], reverse=True): print('  ', f'{x[0]*100:+.1f}%', x[2], f'{x[3]}㎡', f'{x[4]/10000:.2f}→{x[5]/10000:.2f}억', f'({x[6]}/{x[7]}건)')
print('\n# 광교 2021하 대비 넘은 집')
for x in sorted([x for x in pairs(G, '고점21', '최근') if x[0] >= 0], reverse=True): print('  ', f'{x[0]*100:+.1f}%', x[2], f'{x[3]}㎡', f'{x[4]/10000:.2f}→{x[5]/10000:.2f}억', f'({x[6]}/{x[7]}건)')
print('\n# 광교 최근 84㎡안팎 단지별 가운데(2건 이상) 비싼 5·싼 5')
d = C.defaultdict(list)
for r in G:
    if inper(r, '최근') and 83 <= r['_a'] <= 86: d[(r['umdNm'], r['aptNm'])].append(r['_p'])
ls = sorted([(st.median(v), k, len(v)) for k, v in d.items() if len(v) >= 2], reverse=True)
for m, k, n in (ls[:5] + ls[-5:] if len(ls) > 10 else ls):
    print('  ', f'{m/10000:.2f}억 {k} {n}건')
print('  84㎡안팎 2건 이상 단지 수', len(ls))
print('\n# 반기별 건수 광교 수원/용인')
for y in range(2021, 2027):
    for h, (lo, hi) in (('상', (1, 6)), ('하', (7, 12))):
        a = [r for r in GS if r['_ym'] // 100 == y and lo <= r['_ym'] % 100 <= hi]; b = [r for r in GY if r['_ym'] // 100 == y and lo <= r['_ym'] % 100 <= hi]
        if a or b: print(f'{y}{h}', len(a), '/', len(b))
print('\n# 같은 집 반기 사슬(광교 전체)')
HS = [(f'{y}{h}', (y*100+lo, y*100+hi)) for y in range(2021, 2027) for h, lo, hi in (('상', 1, 6), ('하', 7, 12))]
for (la, pa), (lb, pb) in zip(HS, HS[1:]):
    PER['_a'], PER['_b'] = pa, pb; ps = pairs(G, '_a', '_b')
    if ps: print(f'{la}→{lb}: {len(ps)}쌍 {st.median([x[0] for x in ps])*100:+.1f}%')
print('\n# 직거래 몫(광교 최근)', C.Counter(r.get('dealingGbn') for r in G if inper(r, '최근')).most_common())
print('# 11월 계약(최근에서 뺌) 광교', sum(1 for r in G if r['_ym'] == 202611))
x = [r['_p'] for r in G if inper(r, '최근')]
print('# 최근 광교 매매', len(x), '건 가운데', st.median(x)/10000, '억 · 15억 넘는 집', sum(1 for p in x if p > 150000))
print('\n# 확인: 넓이 나눠 1년 — 광교 수원/용인/영통 옛/수지 옛')
for lab, f in (('85㎡ 초과', lambda r: r['_a'] > 85), ('60㎡ 이하', lambda r: r['_a'] <= 60), ('60~85㎡', lambda r: 60 < r['_a'] <= 85)):
    for nm, v in (('수원 쪽', GS), ('용인 쪽', GY), ('영통 옛', YO), ('수지 옛', SO)):
        show(f'  {lab} {nm}', pairs([r for r in v if f(r)], '1년전', '최근'))
