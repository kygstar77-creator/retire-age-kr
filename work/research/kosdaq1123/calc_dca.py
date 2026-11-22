# 매달 첫 거래일 같은 돈(100만원)을 지수에 넣었다면 — 세전·지수 값만(배당·보수 없음), 2006-01 / 2016-01 시작, 기준일 2026-11-20 종가
import json, sys
sys.stdout.reconfigure(encoding='utf-8')
d = json.load(open('raw_ecos.json', encoding='utf-8'))
def dca(rows, start):
    last = rows[-1][1]; months = {}; 
    for t, v in rows:
        if t >= start and t[:6] not in months: months[t[:6]] = v
    units = sum(1_000_000 / v for v in months.values()); paid = 1_000_000 * len(months)
    return len(months), paid, units * last, (units * last / paid - 1) * 100
for start in ['20060101', '20160101', '20210101']:
    for nm in ['kosdaq', 'kospi']:
        n, paid, val, r = dca(d[nm], start)
        print(start, nm, f'{n}달 넣은 돈 {paid/1e4:,.0f}만원 → {val/1e4:,.0f}만원 ({r:+.1f}%)')
