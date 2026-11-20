# S&P500 보유 기간별 손해 본 적 — 야후 ^SP500TR(배당 재투자, 1988~)·^GSPC(가격, 1928~), 원화는 FRED DEXKOUS (2026-11-21 firemap-write)
import json, datetime, sys, statistics as st, bisect
sys.stdout.reconfigure(encoding='utf-8')
def y(n):
    q = json.load(open(f'raw/{n}_20261121.json'))['chart']['result'][0]
    return [((datetime.date(1970,1,1)+datetime.timedelta(seconds=a)).date() if False else (datetime.datetime(1970,1,1)+datetime.timedelta(seconds=a)).date(), b) for a, b in zip(q['timestamp'], q['indicators']['quote'][0]['close']) if b]
tr = y('sp500tr'); px = y('gspc')
print('TR', tr[0], tr[-1], len(tr)); print('PX', px[0], px[-1], len(px))
fx = sorted((datetime.date.fromisoformat(a), float(b)) for a, b in json.load(open('raw/fred_DEXKOUS_20261121.json')))
print('FX', fx[0], fx[-1], len(fx))
def roll(r, yrs, step_month=False):
    ds = [a for a, _ in r]; out = []
    for i, (d, v) in enumerate(r):
        try: t = d.replace(year=d.year + yrs)
        except ValueError: t = d.replace(year=d.year + yrs, day=28)
        j = bisect.bisect_left(ds, t)
        if j >= len(r): break
        out.append((d, r[j][0], r[j][1] / v - 1))
    return out
def summ(name, r, yrs):
    o = roll(r, yrs)
    if not o: return
    rets = [x[2] for x in o]; loss = [x for x in o if x[2] < 0]
    ann = [((1 + x) ** (1 / yrs) - 1) * 100 for x in rets]
    w = min(o, key=lambda x: x[2]); b = max(o, key=lambda x: x[2])
    lastloss = max(loss, key=lambda x: x[0]) if loss else None
    print(f'{name} {yrs}년: 구간 {len(o)} · 손해 {len(loss)} ({len(loss)/len(o)*100:.1f}%) · 연 중간 {st.median(ann):.1f}% · 최악 {w[0]}~{w[1]} {w[2]*100:.1f}% · 최고 {b[0]}~{b[1]} {b[2]*100:.1f}% · 마지막 손해 시작 {lastloss[0] if lastloss else None}')
for yrs in [1, 3, 5, 10, 15, 20]: summ('TR(달러)', tr, yrs)
for yrs in [1, 5, 10, 15, 20]: summ('가격만(1928~)', px, yrs)
# 원화: TR × 원/달러
fd = [a for a, _ in fx]
def fxat(d):
    j = bisect.bisect_right(fd, d) - 1
    return fx[j][1] if j >= 0 else None
trk = [(d, v * fxat(d)) for d, v in tr if fxat(d)]
print('TRK', trk[0], trk[-1])
for yrs in [1, 3, 5, 10, 15, 20]: summ('TR(원화)', trk, yrs)
# 10년 손해 구간 묶음(시작일 범위)
o = roll(tr, 10); L = [x for x in o if x[2] < 0]
if L: print('TR 10년 손해 시작일', L[0][0], '~', L[-1][0], '건', len(L))
o = roll(px, 10); L = [x for x in o if x[2] < 0]
yrs_ = sorted({x[0].year for x in L}); print('가격 10년 손해 시작 연도', yrs_)
# 지금 위치
pk = max(tr, key=lambda x: x[1]); print('TR 최고', pk, '마지막', tr[-1], round((tr[-1][1]/pk[1]-1)*100, 1))
pkp = max(px, key=lambda x: x[1]); print('PX 최고', pkp, '마지막', px[-1], round((px[-1][1]/pkp[1]-1)*100, 1))
# 1억 예시: 10년 중간·최악 (달러 TR)
o10 = roll(tr, 10); m = st.median([x[2] for x in o10]); print('1억 10년 중간', round(1e8*(1+m)), '최악', round(1e8*(1+min(x[2] for x in o10))))
o = roll(trk, 10); L = [x for x in o if x[2] < 0]
print('원화 10년 손해 시작일', L[0][0], '~', L[-1][0], '건', len(L), '시작 연도', sorted({x[0].year for x in L}))
for d in ['1999-03-08', '2009-03-09', '2000-03-23', '2026-11-13']: print('달러값', d, fxat(datetime.date.fromisoformat(d)))
# 1년 손해 확률 vs 10년, 1억 예시(달러 TR 10년 중간·최악)
for yrs in [1, 10]:
    o = roll(tr, yrs); print(yrs, '년 1억 →', '중간', round(1e8*(1+st.median([x[2] for x in o]))/1e4), '만원 · 최악', round(1e8*(1+min(x[2] for x in o))/1e4), '만원')
for yrs in [15, 20]:
    L = [x for x in roll(px, yrs) if x[2] < 0]; print('가격', yrs, '년 손해 시작', L[0][0], '~', L[-1][0], len(L))
print('달러값 1997-12-23', fxat(datetime.date(1997,12,23)), '1997-11-03', fxat(datetime.date(1997,11,3)))
print('TR 10년 구간 시작 범위', roll(tr,10)[0][0], '~', roll(tr,10)[-1][0], ' 20년', roll(tr,20)[-1][0])
# SPY 기간(1993-01-29~)으로 자른 배당 재투자 지수 10년 손해 — SPY 8.0%와 기간 차이 가르기
sub = [x for x in tr if x[0] >= datetime.date(1993, 1, 29)]
o = roll(sub, 10); print('TR 1993-01-29~ 10년 구간', len(o), '손해', sum(x[2] < 0 for x in o), round(sum(x[2] < 0 for x in o)/len(o)*100, 1))
o = roll(tr, 20); print('1억 20년 중간', round(1e8*(1+st.median([x[2] for x in o]))/1e4), '만원')
