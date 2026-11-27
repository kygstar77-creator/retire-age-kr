# NDX-1 대본 보조 셈 (youtube-loop 2026-11-27 13시) — calc_out_1125 35구간 재사용, FRED NASDAQ100 1127판
import csv, sys, datetime as dt, statistics as st
sys.stdout.reconfigure(encoding='utf-8')
r = [(dt.date.fromisoformat(a), float(b)) for a, b in csv.reader(open('fred_NASDAQ100_1127.csv')) if a[:1].isdigit() and b not in ('', '.')]
eps = []; peak = r[0]; tr = r[0]; ind = False
for d, v in r:
    if v >= peak[1]:
        if ind and (peak[1]-tr[1])/peak[1] >= .10: eps.append((peak, tr, (d, v)))
        peak = (d, v); tr = (d, v); ind = False
    else:
        ind = True
        if v < tr[1]: tr = (d, v)
days = [(e[2][0]-e[0][0]).days for e in eps]
print('끝난', len(eps), '· 1년(365일) 안 회복', sum(x <= 365 for x in days), '· 2년(730일) 안', sum(x <= 730 for x in days), '· 2년 넘음', [ (e[0][0].isoformat(), (e[2][0]-e[0][0]).days) for e in eps if (e[2][0]-e[0][0]).days > 730])
print('전체 가운데', st.median(days), '· 평균', round(st.mean(days), 1), '· 닷컴 뺀 평균', round(st.mean([x for x in days if x < 5000]), 1))
yrs = (r[-1][0]-r[0][0]).days/365.25; print(f'기간 {yrs:.1f}년 · 35번이면 {yrs/35:.2f}년에 한 번꼴')
# 하루 가장 크게 내린 날 5
ch = sorted(((r[i][0], (r[i][1]/r[i-1][1]-1)*100) for i in range(1, len(r))), key=lambda x: x[1])[:5]
print('하루 낙폭 상위', [(d.isoformat(), round(c, 1)) for d, c in ch])
# 닷컴: 바닥까지 날수, 바닥에서 회복까지
e = next(x for x in eps if x[0][0] == dt.date(2000, 3, 27))
print('닷컴 고점', e[0], '바닥', e[1], (e[1][0]-e[0][0]).days, '일 · 바닥→회복', (e[2][0]-e[1][0]).days, '일 · 바닥에서 고점까지 필요', round((e[0][1]/e[1][1]-1)*100), '%')
# 2007 고점(2000년 골짜기 안) → 2008 바닥: 2007-10-31 근처 최고
pk07 = max((x for x in r if dt.date(2007, 1, 1) <= x[0] <= dt.date(2008, 6, 30)), key=lambda x: x[1]); lo08 = min((x for x in r if pk07[0] <= x[0] <= dt.date(2009, 12, 31)), key=lambda x: x[1])
rec = next(x for x in r if x[0] > lo08[0] and x[1] >= pk07[1])
print('2007 고점', pk07, '→ 바닥', lo08, round((lo08[1]/pk07[1]-1)*100, 1), '% → 2007 고점 되찾음', rec[0], (rec[0]-pk07[0]).days, '일 · 이때도 2000 고점 4,705 아래:', rec[1] < 4704.73)
# 회복 산수
for x in (10, 16.6, 19.8, 20, 30, 50, 82.9): print(f'-{x}% → 되찾으려면 +{(1/(1-x/100)-1)*100:.1f}%')
