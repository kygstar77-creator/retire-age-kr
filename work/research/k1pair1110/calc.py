# k1pair1110 계산 — 금감원 금융상품한눈에 주담대(아파트·분할상환) 공시 '전월 취급 평균금리' + K-1 calc5 가정
import json, statistics as st, sys
sys.stdout.reconfigure(encoding='utf-8')
r = json.load(open('raw/finlife_mortgage_20261109.json', encoding='utf-8'))
rows = [x for x in r if x['담보'] == '아파트' and '분할' in (x['상환방식'] or '') and x['대출평균'] is not None]
def pmt(P, rate, n): i = rate/100/12; return P*i/(1-(1+i)**-n)
out = {}
for t in ('고정금리', '변동금리'):
    v = sorted(x['대출평균'] for x in rows if x['금리유형'] == t)
    out[t] = v
    print(f"{t}: 상품 {len(v)}개 · 공시월 {set(x['공시월'] for x in rows)} · 평균금리 최저 {v[0]} · 중앙 {st.median(v)} · 최고 {v[-1]}")
P0 = 300_000_000; first = pmt(P0, 2.98, 360)
# 5년(60회) 뒤 남은 원금
i = 2.98/100/12; bal = P0*(1+i)**60 - first*((1+i)**60-1)/i
print(f"2021.08 3억·30년 2.98% 월 {first:,.0f} · 5년 뒤 남은 원금 {bal:,.0f}")
for t in ('고정금리', '변동금리'):
    v = out[t]
    for name, rt in (('최저', v[0]), ('중앙', st.median(v)), ('최고', v[-1])):
        m = pmt(bal, rt, 300)
        print(f"  {t} {name} {rt}% → 25년 월 {m:,.0f} (2021보다 +{m-first:,.0f})")
