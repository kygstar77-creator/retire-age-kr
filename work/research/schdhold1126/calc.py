# SCHD 보유 기간별 손해 본 적 — 야후 adjclose(배당 재투자·분할 반영), 원화는 FRED DEXKOUS (2026-11-24 firemap-write)
import json, datetime, sys, statistics as st, bisect
sys.stdout.reconfigure(encoding='utf-8')
def load(n):
    q = json.load(open(f'raw/{n}_20261124.json'))['chart']['result'][0]
    ts = q['timestamp']; adj = q['indicators']['adjclose'][0]['adjclose']; cl = q['indicators']['quote'][0]['close']
    d = lambda a: (datetime.datetime(1970,1,1)+datetime.timedelta(seconds=a+9*3600)).date()
    tr = [(d(a), b) for a, b in zip(ts, adj) if b]; px = [(d(a), b) for a, b in zip(ts, cl) if b]
    ev = q.get('events', {})
    return tr, px, ev
tr, px, ev = load('schd'); str_, spx, _ = load('spy')
print('SCHD', tr[0], tr[-1], len(tr)); print('SPY', str_[0], str_[-1])
print('split', [( (datetime.datetime(1970,1,1)+datetime.timedelta(seconds=int(k))).date(), v.get('splitRatio')) for k, v in ev.get('splits', {}).items()])
divs = sorted(((datetime.datetime(1970,1,1)+datetime.timedelta(seconds=int(k))).date(), v['amount']) for k, v in ev.get('dividends', {}).items())
print('배당 횟수', len(divs), '첫', divs[0], '마지막', divs[-4:])
spy0 = tr[0][0]; str_ = [x for x in str_ if x[0] >= spy0]; spx = [x for x in spx if x[0] >= spy0]
fx = sorted((datetime.date.fromisoformat(a), float(b)) for a, b in json.load(open('raw/fred_DEXKOUS_20261124.json')) if b not in ('.', None, ''))
fd = [a for a, _ in fx]
def fxat(d):
    j = bisect.bisect_right(fd, d) - 1
    return fx[j][1] if j >= 0 else None
print('FX 마지막', fx[-1])
def roll(r, yrs):
    ds = [a for a, _ in r]; out = []
    for d, v in r:
        try: t = d.replace(year=d.year + yrs)
        except ValueError: t = d.replace(year=d.year + yrs, day=28)
        j = bisect.bisect_left(ds, t)
        if j >= len(r): break
        out.append((d, r[j][0], r[j][1] / v - 1))
    return out
def summ(name, r, yrs):
    o = roll(r, yrs)
    if not o: print(name, yrs, '구간 없음'); return
    rets = [x[2] for x in o]; loss = [x for x in o if x[2] < 0]
    ann = [((1 + x) ** (1 / yrs) - 1) * 100 for x in rets]
    w = min(o, key=lambda x: x[2]); b = max(o, key=lambda x: x[2])
    ls = (loss[0][0], max(loss, key=lambda x: x[0])[0]) if loss else None
    print(f'{name} {yrs}년: 구간 {len(o)} · 시작 {o[0][0]}~{o[-1][0]} · 손해 {len(loss)} ({len(loss)/len(o)*100:.1f}%) · 연 중간 {st.median(ann):.1f}% · 누적 중간 {st.median(rets)*100:.1f}% · 최악 {w[0]}~{w[1]} {w[2]*100:.1f}% · 최고 {b[0]}~{b[1]} {b[2]*100:.1f}% · 손해 시작 범위 {ls}')
for yrs in [1, 2, 3, 4, 5, 7, 10]: summ('SCHD 배당재투자(달러)', tr, yrs)
for yrs in [1, 3, 5, 10]: summ('SCHD 가격만(달러)', px, yrs)
for yrs in [1, 3, 5, 10]: summ('SPY 배당재투자(같은 기간)', str_, yrs)
trk = [(d, v * fxat(d)) for d, v in tr if fxat(d)]
for yrs in [1, 2, 3, 4, 5, 7, 10]: summ('SCHD 배당재투자(원화)', trk, yrs)
pk = max(tr, key=lambda x: x[1]); print('SCHD TR 최고', pk, '마지막', tr[-1], round((tr[-1][1]/pk[1]-1)*100, 1))
pkp = max(px, key=lambda x: x[1]); print('SCHD 가격 최고', pkp, '마지막', px[-1], round((px[-1][1]/pkp[1]-1)*100, 1))
# 가장 긴 물림: 배당재투자 기준 전 고점 회복까지 걸린 날
best = None; peak = tr[0]; 
for d, v in tr:
    if v >= peak[1]:
        if best is None or (d - peak[0]).days > best[2]: best = (peak[0], d, (d - peak[0]).days)
        peak = (d, v)
print('가장 긴 고점 회복(TR)', best, '지금 고점 뒤', (tr[-1][0]-peak[0]).days, '일', peak)
mdd = 0; pk_ = tr[0]
for d, v in tr:
    if v > pk_[1]: pk_ = (d, v)
    dd = v / pk_[1] - 1
    if dd < mdd: mdd, at = dd, (pk_[0], d)
print('최대 낙폭 TR', round(mdd*100, 1), at)
for yrs in [1, 5]:
    o = roll(tr, yrs); print(yrs, '년 1억 → 중간', round(1e8*(1+st.median([x[2] for x in o]))/1e4), '만원 · 최악', round(1e8*(1+min(x[2] for x in o))/1e4), '만원')
# 최근 1년 배당 합
last = tr[-1][0]; s = sum(a for d, a in divs if d > last - datetime.timedelta(days=365)); print('최근 1년 배당 합', round(s, 4), '종가', px[-1], '배당률', round(s/px[-1][1]*100, 2))
print('5년 전 같은 때', [x for x in px if x[0] >= last.replace(year=last.year-5)][0])
for d in ['2019-03-21', '2020-03-23', '2017-03-20', '2022-01-11', '2023-12-28', '2026-11-20']: print('달러값', d, fxat(datetime.date.fromisoformat(d)))
o = roll(trk, 2); L = [x for x in o if x[2] < 0]; print('원화 2년 손해', [(a, b, round(c*100, 1)) for a, b, c in L])
o = roll(tr, 3); L = [x for x in o if x[2] < 0]; print('달러 3년 손해', [(a, b, round(c*100, 1)) for a, b, c in L])
o = roll(trk, 1); L = [x for x in o if x[2] < 0]; print('원화 1년 손해 시작 연도', sorted({x[0].year for x in L}), len(L))
o = roll(tr, 1); L = [x for x in o if x[2] < 0]; import collections; print('달러 1년 손해 시작 연도별', sorted(collections.Counter(x[0].year for x in L).items()))
