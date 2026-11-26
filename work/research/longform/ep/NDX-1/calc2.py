# NDX-1 4장·5장 셈 (youtube-loop 2026-11-27) — FRED NASDAQ100(가격지수, 배당 빠짐) 일별 종가 · FRED DEXKOUS(원/달러, 연준 H.10 정오 매입률)
import csv, sys, statistics as st, datetime as dt
sys.stdout.reconfigure(encoding='utf-8')
def load(p): return [(dt.date.fromisoformat(a), float(b)) for a, b in csv.reader(open(p)) if a[:1].isdigit() and b not in ('', '.')]
r = load('fred_NASDAQ100_1127.csv'); fx = dict(load('fred_DEXKOUS_1127.csv'))
print('기간', r[0][0], '~', r[-1][0], len(r), '일 · 환율', min(fx), '~', max(fx))
eps = []; peak = r[0]; tr = r[0]; ind = False
for d, v in r:
    if v >= peak[1]:
        if ind and (peak[1]-tr[1])/peak[1] >= .10: eps.append((peak, tr, (d, v)))
        peak = (d, v); tr = (d, v); ind = False
    else:
        ind = True
        if v < tr[1]: tr = (d, v)
cur = (peak, tr, None) if ind else None
done = eps
def dd(e): return (e[1][1]/e[0][1]-1)*100
def days(e): return (e[2][0]-e[0][0]).days
print('\n끝난 구간', len(done))
# 4장: 같은 깊이(바닥 -15~-25%)
same = [e for e in done if -25 < dd(e) <= -15]
print('\n[4장] 바닥이 -15%~-25% 사이에서 멈춘 구간', len(same))
for e in same: print(f"  {e[0][0]} → 바닥 {e[1][0]} ({dd(e):.1f}%, 고점에서 {(e[1][0]-e[0][0]).days}일째 바닥) → 회복 {e[2][0]} · {days(e)}일 · 바닥에서 회복까지 {(e[2][0]-e[1][0]).days}일")
ds = sorted(days(e) for e in same); print('  회복 날수 가장 짧음', ds[0], '가장 김', ds[-1], '가운데', st.median(ds))
bt = sorted((e[1][0]-e[0][0]).days for e in same); print('  고점→바닥 날수 가운데', st.median(bt), '범위', bt[0], '~', bt[-1])
# 더 깊어진 구간: -20%를 처음 넘은 날
print('\n[4장] -20%보다 깊어진 구간에서 -20%를 처음 넘은 날')
for e in done + ([cur] if cur else []):
    if dd(e) <= -20:
        pk = e[0]
        x = next((d for d, v in r if d > pk[0] and v <= pk[1]*.8), None)
        print(f"  {pk[0]} 고점 · -20% 첫날 {x} (고점에서 {(x-pk[0]).days}일째) · 바닥 {e[1][0]} {dd(e):.1f}% (−20% 뒤 {(e[1][0]-x).days}일 더) · 회복 {e[2][0] if e[2] else '아직'}")
# 지금
last = r[-1]; pk = cur[0] if cur else None
if cur:
    print(f"\n[지금] 고점 {pk[0]} {pk[1]:,.2f} · 바닥 지금까지 {cur[1][0]} {cur[1][1]:,.2f} ({dd(cur):.1f}%) · 마지막 {last[0]} {last[1]:,.2f} ({(last[1]/pk[1]-1)*100:.1f}%) · 고점에서 {(last[0]-pk[0]).days}일째 · 고점까지 +{(pk[1]/last[1]-1)*100:.1f}% 필요")
# 5장: 2021-11-19 고점부터 매달 같은 날(그날 없으면 다음 거래일) 1씩
start = dt.date(2021, 11, 19)
def nxt(d):
    for dd_, v in r:
        if dd_ >= d: return dd_, v
buys = []; y, m = 2021, 11
while True:
    d = dt.date(y, m, 19)
    if d > dt.date(2023, 12, 31): break
    buys.append(nxt(d)); m += 1
    if m == 13: y, m = y+1, 1
# 본전 = 가장 깊은 평가 손실 날(2021-11-19~2023-12-31 안) 뒤 처음 평가액 >= 넣은 돈인 날 (11/27 고침 — 처음 판은 12월 초 짧은 반등을 본전으로 셌다)
END = dt.date(2023, 12, 31)
def path(dca, use_fx):
    units = 0; paid = 0; bi = 0; out = []; p0 = None
    for d, v in r:
        if d < start: continue
        if use_fx and d not in fx: continue
        px = v*fx[d] if use_fx else v
        if dca:
            while bi < len(buys) and buys[bi][0] <= d:
                bd, bv = buys[bi]; k = bd if bd in fx else max(k for k in fx if k <= bd)
                units += 1/(bv*fx[k] if use_fx else bv); paid += 1; bi += 1
        elif p0 is None: p0 = px; units = 1/px; paid = 1
        out.append((d, units*px/paid-1, paid))
    return out
for dca in (False, True):
    for f in (False, True):
        p = path(dca, f); win = [x for x in p if x[0] <= END]
        low = min(win, key=lambda x: x[1])
        ev = next((x for x in p if x[0] > low[0] and x[1] >= 0), None)
        nm = ('매달 19일 같은 돈' if dca else '고점 하루 한 번에') + (' · 원화(지수×원/달러)' if f else ' · 달러(지수 그대로)')
        print(f"[5장] {nm} → 가장 깊은 평가 손실 {low[0]} {low[1]*100:.1f}%({low[2]}번 넣은 때) → 본전 {ev[0]} (고점에서 {(ev[0]-start).days}일 · 바닥에서 {(ev[0]-low[0]).days}일 · {ev[2]}번 넣음)")
print('\n환율', start, fx[start], '·', dt.date(2023, 12, 15), fx.get(dt.date(2023, 12, 15)))
# 지금 구간 원화로(댓글 물음 TT46dYq2-SI lc=Ugwjg2x4 '원화로는 30%') — 지수×원/달러, 환율 있는 날만
kr = [(d, v*fx[d]) for d, v in r if d in fx]
pk = max((x for x in kr if x[0] <= dt.date(2026, 11, 20)), key=lambda x: x[1]); lastk = kr[-1]
pk_since = max((x for x in kr if x[0] >= dt.date(2026, 10, 6)), key=lambda x: x[1])
lowk = min((x for x in kr if x[0] >= pk[0]), key=lambda x: x[1])
print(f"\n[원화 지금] 원화 최고 {pk[0]} {pk[1]:,.0f} · 그 뒤 가장 낮음 {lowk[0]} {lowk[1]:,.0f} ({(lowk[1]/pk[1]-1)*100:.1f}%) · 환율 마지막 날 {lastk[0]} ({(lastk[1]/pk[1]-1)*100:.1f}%) · 10/6 달러 고점 날 환율 {fx.get(dt.date(2026,10,6))} · 11/20 {fx[dt.date(2026,11,20)]}")
