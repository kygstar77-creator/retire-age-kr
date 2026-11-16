# bundil1117 — 분당구(41135)·일산동구(41285)·일산서구(41287) 아파트 매매 실거래(S1 raw) 직접 계산 · firemap-write-b 2026-11-17
# 같은 집 = 같은 단지(aptSeq)·같은 전용면적(1㎡ 반올림). 해제(cdealType) 뺌. 직거래 포함(몫 따로 셈).
import json, os, glob, statistics as st, sys, collections as C
sys.stdout.reconfigure(encoding='utf-8')
H = os.path.dirname(os.path.abspath(__file__))
num = lambda s: float(str(s or '0').replace(',', '') or 0)
NM = {'41135': '분당구', '41285': '일산동구', '41287': '일산서구'}
rows = []
for p in sorted(glob.glob(os.path.join(H, 'raw', '*_trade.json'))):
    code = os.path.basename(p)[:5]
    for r in json.load(open(p, encoding='utf-8')):
        if r.get('cdealType'): continue
        r['_g'] = NM[code]; r['_ym'] = int(r['dealYear']) * 100 + int(r['dealMonth']); r['_p'] = num(r['dealAmount']); r['_a'] = round(num(r['excluUseAr']))
        r['_k'] = (r.get('aptSeq') or r['aptNm'], r['_a']); rows.append(r)
print('전체(해제 뺌)', len(rows), '건 · 계약', min(r['_ym'] for r in rows), '~', max(r['_ym'] for r in rows))
for g in NM.values():
    print(' ', g, sum(1 for r in rows if r['_g'] == g), '건 · 직거래 몫', f"{sum(1 for r in rows if r['_g']==g and r.get('dealingGbn')=='직거래')/sum(1 for r in rows if r['_g']==g)*100:.1f}%")
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
for g in NM.values():
    for a in ('고점21', '바닥23', '1년전'):
        for mn in (1, 2):
            n, m, up = pairs(g, a, '최근', mn)
            print(f'{g} {a}→최근 (각 {mn}건↑): {n}쌍 · 가운데 {m*100:+.1f}% · 오른 쌍 {up*100:.0f}%')
# 84㎡형(전용 83~86㎡) 최근 가운데 값
print('\n# 전용 83~86㎡(국민평형) 가운데 매매가')
for g in NM.values():
    for k in ('고점21', '바닥23', '1년전', '최근'):
        v = [r['_p'] for r in rows if r['_g'] == g and inper(r, k) and 83 <= r['_a'] <= 86]
        print(f'{g} {k}: {len(v)}건 · 가운데 {st.median(v)/10000:.2f}억')
# 한 달 평균 거래 건수(2026년 11월은 신고 덜 들어와 뺌)
print('\n# 한 달 평균 매매 건수')
for g in NM.values():
    for lab, lo, hi in (('2021년', 202101, 202112), ('2022년', 202201, 202212), ('2023년', 202301, 202312), ('2024년', 202401, 202412), ('2025년', 202501, 202512), ('2026년 1~10월', 202601, 202610)):
        v = [r for r in rows if r['_g'] == g and lo <= r['_ym'] <= hi]; months = len({r['_ym'] for r in v})
        print(f'{g} {lab}: 월평균 {len(v)/months:,.0f}건')
# 일산 두 구 합친 같은 집
print('\n# 일산 두 구 합침')
for a in ('고점21', '바닥23', '1년전'):
    d = C.defaultdict(lambda: C.defaultdict(list))
    for r in rows:
        if r['_g'] == '분당구': continue
        for k in (a, '최근'):
            if inper(r, k): d[r['_k']][k].append(r['_p'])
    rs = [st.median(v['최근']) / st.median(v[a]) - 1 for v in d.values() if v[a] and v['최근']]
    print(f'일산 {a}→최근: {len(rs)}쌍 · 가운데 {st.median(rs)*100:+.1f}% · 오른 쌍 {sum(1 for x in rs if x>0)/len(rs)*100:.0f}%')
