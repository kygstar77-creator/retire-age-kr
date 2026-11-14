# mokpair1115 계산 — 숫자는 전부 여기서. 재료 raw/11470_*_trade.json(국토부 매매 실거래, 2026-11-15 받음)
# 해제(cdealType)·공공기관 매수 제외. 평당 = 전용면적 3.305785㎡. 단위 만원.
import json, os, glob, re, statistics as st, collections, sys
sys.stdout.reconfigure(encoding='utf-8')
H = os.path.dirname(os.path.abspath(__file__)); PY = 3.305785
def num(s): return float(str(s or '0').replace(',', '') or 0)
rows = []
for p in sorted(glob.glob(os.path.join(H, 'raw', '11470_*_trade.json'))): rows += json.load(open(p, encoding='utf-8'))
def ok(r): return not r.get('cdealType') and r.get('buyerGbn') != '공공기관'
def pp(r): return num(r['dealAmount']) / num(r['excluUseAr']) * PY
def ar(r): return num(r['excluUseAr'])
def ymi(r): return int(r['dealYear']) * 100 + int(r['dealMonth'])
def med(v): return st.median(v) if v else 0
MS = [r for r in rows if ok(r) and '목동신시가지' in r['aptNm']]
cx = sum(1 for r in rows if r.get('cdealType') and '목동신시가지' in r['aptNm'])
def dan(r): return int(re.search(r'\d+', r['aptNm'].replace('목동신시가지', '')).group())
NOW = [r for r in MS if 202511 <= ymi(r) <= 202611]
OLD = [r for r in MS if 202411 <= ymi(r) <= 202510]
print(f'# 신시가지 거래 전체 {len(MS)}건(해제 {cx}건 뺌) · 최근 1년(2025.11~2026.11 계약) {len(NOW)}건 · 그 전 1년(2024.11~2025.10) {len(OLD)}건')
print(f'# 최근 계약일: {max((r["dealYear"], str(r["dealMonth"]).zfill(2), str(r["dealDay"]).zfill(2)) for r in MS)}')
BAND = (60, 70)
def band(rs): return [r for r in rs if BAND[0] <= ar(r) < BAND[1]]
print('\n## 1. 단지별 60~70㎡대(쇼츠와 같은 띠) 최근 1년 — 평당 중앙 높은 순')
res = []
for k in range(1, 15):
    b = band([r for r in NOW if dan(r) == k]); bo = band([r for r in OLD if dan(r) == k])
    allk = [r for r in NOW if dan(r) == k]
    umd = allk[0]['umdNm'] if allk else '-'
    if b:
        res.append((med([pp(r) for r in b]), k, umd, len(b), med([num(r['dealAmount']) for r in b]), med([ar(r) for r in b]),
                    med([pp(r) for r in bo]) if bo else 0, len(bo), len(allk)))
    else:
        print(f'- {k}단지 · {umd} · 60~70㎡대 거래 0건(전 면적 {len(allk)}건) · 면적 {sorted({round(ar(r)) for r in allk})}')
for p, k, umd, n, a, area, po, no, na in sorted(res, reverse=True):
    ch = f'{p/po*100-100:+.1f}%(전년 {no}건 평당 {po:,.0f})' if po and no >= 3 else f'전년 {no}건'
    print(f'- {k}단지 · {umd} · {n}건 · 평당 중앙 {p:,.0f} · 한 채 중앙 {a/10000:.2f}억 · 전용 중앙 {area:.1f}㎡ · 1년 전 대비 {ch} · 전 면적 {na}건')
print('\n## 2. 앞(1~7, 목동)·뒤(8~14, 신정동) 60~70㎡대 모아서')
for tag, rs in [('최근 1년', NOW), ('그 전 1년', OLD)]:
    f = band([r for r in rs if dan(r) <= 7]); b = band([r for r in rs if dan(r) >= 8])
    pf, pb = med([pp(r) for r in f]), med([pp(r) for r in b])
    af, ab = med([num(r['dealAmount']) for r in f]), med([num(r['dealAmount']) for r in b])
    print(f'- {tag}: 앞 {len(f)}건 평당 {pf:,.0f}·한 채 {af/10000:.2f}억 / 뒤 {len(b)}건 평당 {pb:,.0f}·한 채 {ab/10000:.2f}억 → 앞이 {pf/pb*100-100:+.1f}% · 한 채 차이 {(af-ab)/10000:.2f}억')
print('\n## 3. 반기별 앞·뒤 평당 중앙(60~70㎡대)')
for lo, hi, tag in [(202411, 202504, '24.11~25.04'), (202505, 202510, '25.05~25.10'), (202511, 202604, '25.11~26.04'), (202605, 202611, '26.05~26.11')]:
    rs = [r for r in MS if lo <= ymi(r) <= hi]
    f = band([r for r in rs if dan(r) <= 7]); b = band([r for r in rs if dan(r) >= 8])
    pf, pb = med([pp(r) for r in f]), med([pp(r) for r in b])
    print(f'- {tag}: 앞 {len(f)}건 {pf:,.0f} / 뒤 {len(b)}건 {pb:,.0f} → 앞이 {pf/pb*100-100:+.1f}%')
print('\n## 4. 월별 신시가지 거래 건수(전 면적)')
c = collections.Counter(ymi(r) for r in MS)
print(' · '.join(f'{k}:{c[k]}' for k in sorted(c)))
print('\n## 5. 단지 내 거래 건수 1년(전 면적) · 직거래')
for k in range(1, 15):
    rs = [r for r in NOW if dan(r) == k]
    print(f'- {k}단지 {len(rs)}건 · 직거래 {sum(1 for r in rs if r.get("dealingGbn")=="직거래")}')
