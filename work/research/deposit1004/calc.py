# deposit1004 — 금감원 금융상품한눈에(finlife) 정기예금 공시 집계. firemap-write 2026-10-03 16:3x
import sys, json, statistics as st, collections
sys.path.insert(0, r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work'); sys.stdout.reconfigure(encoding='utf-8')
import apis
def pull(g):
    rows, p = [], 1
    while True:
        r = apis.finlife('deposit', group=g, page=p)
        if not r: break
        rows += r; p += 1
        if len(r) < 100 or p > 40: break
    return rows
out = {}
for g, name in (('020000', '은행'), ('030300', '저축은행')):
    rows = pull(g)
    json.dump(rows, open(f'raw_{g}.json', 'w', encoding='utf-8'), ensure_ascii=False)
    print(f'== {name} 행 {len(rows)} 공시월 {sorted(set(x["공시월"] for x in rows))} 금융사 {len(set(x["은행"] for x in rows))}')
    for t in ('6', '12', '24', '36'):
        # 금융사별 그 기간 기본금리 최고 상품 하나씩(상품 수 많은 곳이 중간값을 끌지 않게)
        best = collections.defaultdict(float); bestmax = collections.defaultdict(float)
        for x in rows:
            if x['기간'] == t:
                best[x['은행']] = max(best[x['은행']], x['금리'] or 0)
                bestmax[x['은행']] = max(bestmax[x['은행']], x['최고금리'] or 0)
        if not best: continue
        b = list(best.values()); m = list(bestmax.values())
        print(f'  {t}개월: 금융사 {len(b)} · 기본 중간 {st.median(b):.2f} 최고 {max(b):.2f} 최저 {min(b):.2f} · 우대포함 중간 {st.median(m):.2f} 최고 {max(m):.2f} · 4%이상(우대포함) {sum(v>=4 for v in m)}곳')
    big = ['국민은행', '신한은행', '하나은행', '우리은행', '농협은행주식회사']
    if g == '020000':
        for bk in sorted(set(x['은행'] for x in rows)):
            v = [x for x in rows if x['은행'] == bk and x['기간'] == '12']
            if v:
                top = max(v, key=lambda x: (x['최고금리'] or 0))
                print(f'    {bk:14} 12개월 기본최고 {max(x["금리"] for x in v):.2f} 우대포함최고 {top["최고금리"]:.2f} ({top["상품"].replace(chr(10)," ")})')
# 1억 1년 단리 세후 이자(이자소득세 14% + 지방소득세 1.4% = 15.4%)
for r in (3.33, 3.5, 3.8, 4.05, 4.1, 2.6):
    i = 1e8 * r / 100; tax = int(i * 0.14 / 10) * 10; ltax = int(tax * 0.1 / 10) * 10
    print(f'1억 {r}% 1년 단리: 이자 {i/1e4:,.1f}만 세금 {(tax+ltax)/1e4:,.2f}만 세후 {(i-tax-ltax)/1e4:,.1f}만')
