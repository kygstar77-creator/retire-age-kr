# NDX-1 원화 셈을 ECOS(한국은행 731Y001 원/달러 매매기준율)로 다시 — calc2(FRED DEXKOUS)와 대조 (youtube-loop 2026-11-27 13시)
# 같은 날짜끼리 곱함: 나스닥 종가(미국 날짜) × 그날 서울 매매기준율. 서울 날이 없으면 그 전 가장 가까운 서울 날.
import csv, json, sys, datetime as dt
sys.stdout.reconfigure(encoding='utf-8')
def load(p): return [(dt.date.fromisoformat(a), float(b)) for a, b in csv.reader(open(p)) if a[:1].isdigit() and b not in ('', '.')]
r = load('fred_NASDAQ100_1127.csv'); fred = dict(load('fred_DEXKOUS_1127.csv'))
ec = {dt.date(int(x['TIME'][:4]), int(x['TIME'][4:6]), int(x['TIME'][6:])): float(x['DATA_VALUE']) for x in json.load(open('raw/ecos_731Y001_usd_1127.json', encoding='utf-8'))}
eks = sorted(ec)
import bisect
def e_on(d):
    i = bisect.bisect_right(eks, d) - 1
    return eks[i], ec[eks[i]]
print('ECOS', eks[0], '~', eks[-1], len(eks), '일 · 마지막', ec[eks[-1]])
# 1) 같은 날 두 출처 차이
diffs = [(d, fred[d], ec[d], (fred[d]/ec[d]-1)*100) for d in fred if d in ec and d >= dt.date(2021, 1, 1)]
ad = sorted(abs(x[3]) for x in diffs)
print(f'같은 날 {len(diffs)}일 · FRED/ECOS 차이 절댓값 가운데 {ad[len(ad)//2]:.2f}% · 90% {ad[int(len(ad)*.9)]:.2f}% · 가장 큼 {ad[-1]:.2f}%')
for d in (dt.date(2021,11,19), dt.date(2022,12,28), dt.date(2023,3,16), dt.date(2023,6,29), dt.date(2023,12,15), dt.date(2026,6,30), dt.date(2026,10,6), dt.date(2026,11,20), dt.date(2026,11,25)):
    print(f'  {d} FRED {fred.get(d)} · ECOS {e_on(d)}')
# 2) 원화 지금(ECOS)
kr = [(d, v*e_on(d)[1]) for d, v in r if d >= dt.date(2000, 1, 4)]
pk = max((x for x in kr if x[0] <= dt.date(2026, 11, 25)), key=lambda x: x[1])
low = min((x for x in kr if x[0] >= pk[0]), key=lambda x: x[1]); last = kr[-1]
print(f'\n[원화 지금 ECOS] 원화 최고 {pk[0]} {pk[1]:,.0f}(환율 {e_on(pk[0])}) · 그 뒤 가장 낮음 {low[0]} {low[1]:,.0f} ({(low[1]/pk[1]-1)*100:.1f}%) · 마지막 {last[0]} ({(last[1]/pk[1]-1)*100:.1f}%)')
# 달러 고점 10/6 대비 원화
d106 = next(x for x in kr if x[0] == dt.date(2026, 10, 6))
print(f'  달러 고점 날 2026-10-06 원화 값 {d106[1]:,.0f} → {low[0]} {(low[1]/d106[1]-1)*100:.1f}% · 원화 최고 대비 10/6은 {(d106[1]/pk[1]-1)*100:.1f}%')
# 3) 5장 원화(ECOS)
start = dt.date(2021, 11, 19); END = dt.date(2023, 12, 31)
def nxt(d): return next((a, v) for a, v in r if a >= d)
buys = []; y, m = 2021, 11
while dt.date(y, m, 19) <= END:
    buys.append(nxt(dt.date(y, m, 19))); m += 1
    if m == 13: y, m = y+1, 1
def path(dca):
    units = paid = bi = 0; out = []; p0 = None
    for d, v in r:
        if d < start: continue
        px = v*e_on(d)[1]
        if dca:
            while bi < len(buys) and buys[bi][0] <= d:
                bd, bv = buys[bi]; units += 1/(bv*e_on(bd)[1]); paid += 1; bi += 1
        elif p0 is None: p0 = px; units = 1/px; paid = 1
        out.append((d, units*px/paid-1, paid))
    return out
for dca in (False, True):
    p = path(dca); win = [x for x in p if x[0] <= END]; lo = min(win, key=lambda x: x[1])
    ev = next((x for x in p if x[0] > lo[0] and x[1] >= 0), None)
    print(f"[5장 ECOS] {'매달 19일 같은 돈' if dca else '고점 하루 한 번에'} · 원화 → 가장 깊은 손실 {lo[0]} {lo[1]*100:.1f}%({lo[2]}번) → 본전 {ev[0]} (고점에서 {(ev[0]-start).days}일 · {ev[2]}번 넣음)")
