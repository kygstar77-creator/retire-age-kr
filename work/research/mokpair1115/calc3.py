# 같은 크기 묶음(앞 1~7 vs 뒤 8~14) 최근 1년 vs 그 전 1년. 재료·제외 기준 calc.py와 같음
import json, os, glob, re, statistics as st, sys
sys.stdout.reconfigure(encoding='utf-8')
H = os.path.dirname(os.path.abspath(__file__)); PY = 3.305785
def num(s): return float(str(s or '0').replace(',', '') or 0)
rows = []
for p in sorted(glob.glob(os.path.join(H, 'raw', '11470_*_trade.json'))): rows += json.load(open(p, encoding='utf-8'))
ok = lambda r: not r.get('cdealType') and r.get('buyerGbn') != '공공기관'
pp = lambda r: num(r['dealAmount']) / num(r['excluUseAr']) * PY
ar = lambda r: num(r['excluUseAr']); ymi = lambda r: int(r['dealYear']) * 100 + int(r['dealMonth'])
med = lambda v: st.median(v) if v else 0
MS = [r for r in rows if ok(r) and '목동신시가지' in r['aptNm']]
dan = lambda r: int(re.search(r'\d+', r['aptNm'].replace('목동신시가지', '')).group())
P = {'최근 1년(25.11~26.11)': (202511, 202611), '그 전 1년(24.11~25.10)': (202411, 202510)}
for lo, hi in [(53, 56), (95, 109)]:
    print(f'\n## 전용 {lo}~{hi}㎡')
    for tag, (a, b) in P.items():
        rs = [r for r in MS if a <= ymi(r) <= b and lo <= ar(r) < hi]
        f = [r for r in rs if dan(r) <= 7]; k = [r for r in rs if dan(r) >= 8]
        pf, pk = med([pp(r) for r in f]), med([pp(r) for r in k]); af, ak = med([num(r['dealAmount']) for r in f]), med([num(r['dealAmount']) for r in k])
        print(f'- {tag}: 앞 {len(f)}건({sorted({dan(r) for r in f})}) 평당 {pf:,.0f} 한 채 {af/10000:.2f}억 / 뒤 {len(k)}건({sorted({dan(r) for r in k})}) 평당 {pk:,.0f} 한 채 {ak/10000:.2f}억 → 앞이 {pf/pk*100-100:+.1f}%, 한 채 {(af-ak)/10000:.2f}억')
        if lo == 53:
            for d in sorted({dan(r) for r in rs}):
                x = [r for r in rs if dan(r) == d]
                print(f'    {d}단지 {len(x)}건 한 채 {med([num(r["dealAmount"]) for r in x])/10000:.2f}억 평당 {med([pp(r) for r in x]):,.0f} 전용 {sorted({r["excluUseAr"] for r in x})}')
# 11월 최근 거래
print('\n## 2026.09~11 계약 전부')
for r in sorted([r for r in MS if ymi(r) >= 202609], key=lambda r: (ymi(r), int(r['dealDay']))):
    print(f"- {r['dealYear']}.{r['dealMonth']}.{r['dealDay']} {dan(r)}단지 {r['excluUseAr']}㎡ {num(r['dealAmount'])/10000:.2f}억 {r.get('dealingGbn')}")
