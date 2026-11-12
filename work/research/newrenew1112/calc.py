# newrenew1112 '우리만' 계산 — 전세 새 계약(신규) vs 재계약(갱신) 보증금 차이
# 재료 A: raw/ (국토교통부 아파트 매매·전월세 실거래, 강남·송파·양천 계약 2025-11~2026-11, 2026-11-12 16:5x 받음, fetch.py)
# 재료 B: ../convrate1112/raw (서울 25개 구 아파트 전월세 실거래 계약 2026-08~10, 2026-11-12 받음)
# 순수 전세 = 월세 0. 계약구분(contractType) 신규/갱신, 갱신요구권 사용(useRRRight '사용'), 종전 보증금(preDeposit).
import json, os, sys, glob, statistics as st, collections
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
def num(s): return float(str(s or '0').replace(',', '') or 0)
def eok(m): return f'{m/10000:.2f}억'
def med(v): return st.median(v) if v else 0
def load(d, pat):
    out = []
    for p in sorted(glob.glob(os.path.join(d, pat))): out += [r for r in json.load(open(p, encoding='utf-8')) if isinstance(r, dict) and 'aptNm' in r]
    return out
def ar(r): return num(r['excluUseAr'])
def ymk(r): return int(r['dealYear']) * 100 + int(r['dealMonth'])
def ok(r): return not r.get('cdealType') and r.get('buyerGbn') != '공공기관'
RAW = os.path.join(HERE, 'raw')
DONG = [('11680', '압구정동'), ('11710', '신천동'), ('11470', '목동'), ('11470', '신정동')]
PICK = [('신천동', '파크리오', 84, 85.5), ('신천동', '장미2', 81, 83), ('목동', '목동신시가지7', 66, 68), ('목동', '목동신시가지3', 64, 66),
        ('신정동', '목동신시가지11', 65, 67), ('압구정동', '한양1차(영동한양)', 49, 51), ('압구정동', '신현대12차', 107, 113)]
for lo_ym, hi_ym, lab in [(202511, 202610, '계약 2025.11~2026.10(쇼츠와 같은 기간, 11/12 다시 받은 자료)'), (202605, 202611, '최근 계약 2026.05~11.11')]:
    print(f'## A. 7곳 같은 집 순수 전세 — {lab}')
    for umd, nm, lo, hi in PICK:
        lawd = [l for l, u in DONG if u == umd][0]
        R = [r for r in load(RAW, f'{lawd}_*_rent.json') if r['umdNm'] == umd and r['aptNm'] == nm and lo <= ar(r) < hi and num(r['monthlyRent']) == 0 and lo_ym <= ymk(r) <= hi_ym]
        T = [r for r in load(RAW, f'{lawd}_*_trade.json') if r['umdNm'] == umd and r['aptNm'] == nm and lo <= ar(r) < hi and ok(r) and lo_ym <= ymk(r) <= hi_ym]
        new = [num(r['deposit']) for r in R if r.get('contractType') == '신규']; ren = [num(r['deposit']) for r in R if r.get('contractType') == '갱신']
        rr = [num(r['deposit']) for r in R if r.get('contractType') == '갱신' and r.get('useRRRight') == '사용']
        ra = [num(r['deposit']) for r in R if r.get('contractType') == '갱신' and r.get('useRRRight') != '사용']
        ss = [num(r['dealAmount']) for r in T]
        gap = med(new) - med(ren) if new and ren else 0
        print(f'- {umd} {nm} {lo}~{hi}㎡: 신규 {len(new)}건 {eok(med(new))} · 갱신 {len(ren)}건 {eok(med(ren))} (요구권 사용 {len(rr)}건 {eok(med(rr))} · 그 밖 {len(ra)}건 {eok(med(ra))}) · 차이 {eok(gap)} ({gap/med(ren)*100 if ren else 0:.1f}%) · 매매 {len(ss)}건 {eok(med(ss))} → 신규÷매매 {med(new)/med(ss)*100 if ss else 0:.0f}% · 갱신÷매매 {med(ren)/med(ss)*100 if ss else 0:.0f}%')
    print()

# B. 서울 25개 구 2026-08~10: 같은 단지(aptSeq)·같은 면적(전용 소수점 버림) 순수 전세, 신규·갱신 각 3건 이상인 집
B = load(os.path.join(HERE, '..', 'convrate1112', 'raw'), '*.json')
B = [r for r in B if num(r['monthlyRent']) == 0 and r.get('contractType') in ('신규', '갱신')]
print(f'## B. 서울 25개 구 순수 전세 계약 2026.08~10: {len(B):,}건 (신규 {sum(r["contractType"]=="신규" for r in B):,} · 갱신 {sum(r["contractType"]=="갱신" for r in B):,})')
g = collections.defaultdict(lambda: {'n': [], 'r': [], 'nm': '', 'u': '', 'a': 0})
for r in B:
    k = (r['sggCd'], r['aptSeq'], int(ar(r)))
    g[k]['n' if r['contractType'] == '신규' else 'r'].append(num(r['deposit'])); g[k]['nm'] = r['aptNm']; g[k]['u'] = r['umdNm']; g[k]['a'] = int(ar(r))
pairs = [(k, v, med(v['n']) / med(v['r']) * 100 - 100, med(v['n']) - med(v['r'])) for k, v in g.items() if len(v['n']) >= 3 and len(v['r']) >= 3]
pct = [p[2] for p in pairs]; amt = [p[3] for p in pairs]
print(f'- 신규·갱신 각 3건 이상인 같은 단지·같은 면적: {len(pairs)}곳')
print(f'- 신규가 갱신보다 비싼 곳 {sum(x > 0 for x in pct)}곳 ({sum(x > 0 for x in pct)/len(pct)*100:.0f}%) · 같음 {sum(x == 0 for x in pct)} · 싼 곳 {sum(x < 0 for x in pct)}')
print(f'- 차이 중앙 {med(pct):.1f}% · 금액 중앙 {med(amt):,.0f}만원 · 사분위 {st.quantiles(pct, n=4)[0]:.1f}% ~ {st.quantiles(pct, n=4)[2]:.1f}%')
for lo, hi, lab in [(0, 30000, '갱신 중앙 3억 미만'), (30000, 60000, '3억~6억'), (60000, 10**9, '6억 이상')]:
    s = [p for p in pairs if lo <= med(p[1]['r']) < hi]
    if s: print(f'  · {lab}: {len(s)}곳 · 차이 중앙 {med([p[2] for p in s]):.1f}% · 금액 중앙 {med([p[3] for p in s]):,.0f}만원')
print('- 차이 % 큰 곳 5(참고):')
for k, v, p, a in sorted(pairs, key=lambda x: -x[2])[:5]: print(f'  {v["u"]} {v["nm"]} {v["a"]}㎡ 신규 {len(v["n"])}건 {eok(med(v["n"]))} · 갱신 {len(v["r"])}건 {eok(med(v["r"]))} → {p:+.1f}%')
# C. 갱신 계약의 종전 보증금 대비 인상률 — 요구권 사용 vs 그 밖
print('\n## C. 서울 갱신 순수 전세(종전도 월세 0) — 종전 보증금 대비 인상률')
for lab, f in [('갱신요구권 사용', lambda r: r.get('useRRRight') == '사용'), ('요구권 표시 없음(합의 갱신 등)', lambda r: r.get('useRRRight') != '사용')]:
    s = [num(r['deposit']) / num(r['preDeposit']) * 100 - 100 for r in B if r['contractType'] == '갱신' and f(r) and num(r.get('preDeposit')) > 0 and num(r.get('preMonthlyRent')) == 0]
    if s: print(f'- {lab}: {len(s):,}건 · 인상률 중앙 {med(s):.1f}% · 5% 넘게 올린 계약 {sum(x > 5.0001 for x in s)/len(s)*100:.0f}% · 동결·인하 {sum(x <= 0 for x in s)/len(s)*100:.0f}%')
# D. 계약구분 칸 비어 있는 순수 전세
A = [r for r in load(os.path.join(HERE, '..', 'convrate1112', 'raw'), '*.json') if num(r['monthlyRent']) == 0]
c = collections.Counter(r.get('contractType') or '빈칸' for r in A)
print(f'\n## D. 서울 순수 전세 2026.08~10 전체 {len(A):,}건 계약구분: ' + ' · '.join(f'{k} {v:,}({v/len(A)*100:.1f}%)' for k, v in c.most_common()))
