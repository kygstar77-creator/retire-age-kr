# 맥쿼리인프라(088980) 배당락 기록 — Yahoo 일별 시세(raw/yahoo.json) + MKIF 공식 분배금
import json, datetime as dt, statistics as st, sys
sys.stdout.reconfigure(encoding='utf-8')
d = json.load(open('raw/yahoo.json'))['chart']['result'][0]
ts = d['timestamp']; q = d['indicators']['quote'][0]
KST = dt.timezone(dt.timedelta(hours=9))
days = [dt.datetime.fromtimestamp(t, KST).date() for t in ts]
rows = [(days[i], q['open'][i], q['close'][i], q['low'][i]) for i in range(len(ts)) if q['close'][i]]
official = {'2022-06-30':380,'2022-12-31':390,'2023-06-30':385,'2023-12-31':390,'2024-06-30':380,
            '2024-12-31':380,'2025-06-30':380,'2025-12-31':380,'2026-06-30':350}
divs = sorted(d['events']['dividends'].values(), key=lambda x: x['date'])
out = []
for (rec, amt), ev in zip(official.items(), divs):
    exd = dt.datetime.fromtimestamp(ev['date'], KST).date()
    i = next(k for k, r in enumerate(rows) if r[0] >= exd)
    prev = rows[i-1]; ex = rows[i]
    drop_open = prev[2] - ex[1]; drop_close = prev[2] - ex[2]
    rec_i = next((k for k in range(i, len(rows)) if rows[k][2] >= prev[2]), None)
    rec_days = (rec_i - i) if rec_i is not None else None
    rec_date = rows[rec_i][0] if rec_i is not None else None
    m1 = rows[min(i+20, len(rows)-1)][2]
    y = amt / prev[2] * 100
    out.append((rec, amt, ev['amount'], prev[0], prev[2], ex[0], ex[1], ex[2], drop_open, drop_close, rec_days, rec_date, m1, y))
    print(f"기준일 {rec} 분배 {amt}원(야후 {ev['amount']:.0f}) | 마지막 받는 날 {prev[0]} 종가 {prev[2]:,.0f} | 배당락 {ex[0]} 시가 {ex[1]:,.0f} 종가 {ex[2]:,.0f} | "
          f"시가 하락 {drop_open:,.0f} 종가 하락 {drop_close:,.0f} ({drop_close/amt*100:.0f}% of 분배) | 회복 {rec_days}거래일 {rec_date} | 20거래일 뒤 {m1:,.0f} | 반기 분배율 {y:.2f}%")
dc = [o[9] for o in out]; ratio = [o[9]/o[1]*100 for o in out]
print('종가 하락 중앙', st.median(dc), '분배 대비 중앙 %', round(st.median(ratio)))
rd = [o[10] for o in out if o[10] is not None]
print('회복 거래일', [o[10] for o in out], '중앙', st.median(rd))
print('최근 종가', rows[-1])
# 예시: 1,000만원 어치(마지막 받는 날 종가로) 샀다면 받은 분배금(세전) vs 배당락 종가 하락 손
for o in out:
    n = int(10_000_000 // o[4]); print(o[0], '1천만원→', n, '주, 분배', f"{n*o[1]:,}", '원, 배당락 종가 평가 변화', f"{-n*o[9]:,.0f}")
# 52주
last = rows[-1][0]; yr = [r for r in rows if (last - r[0]).days <= 365]
print('52주 최고', max(yr, key=lambda r: r[2])[:3:2], '최저', min(yr, key=lambda r: r[2])[:3:2])
print('최근 1년 분배 730원 기준 분배율', round(730/rows[-1][2]*100, 2))
