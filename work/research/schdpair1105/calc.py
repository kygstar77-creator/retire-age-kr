# schdpair1105 계산 — 1주당 최근 12개월 배당 합(오늘 기준 창)을 1·3·5·10년 전 같은 창과 비교한 연평균 성장률, 해마다 늘어난 폭
import json, glob, datetime, statistics
END = datetime.date(2026, 11, 4)
def divs(t):
    f = sorted(glob.glob(f'raw/yh_{t}_*.json'))[-1]
    r = json.load(open(f))['chart']['result'][0]
    return sorted((datetime.datetime.utcfromtimestamp(v['date']).date(), v['amount']) for v in r['events']['dividends'].values()), r['meta']['regularMarketPrice']
def ttm(dv, end):
    st = end.replace(year=end.year - 1)
    xs = [a for d, a in dv if st < d <= end]
    return sum(xs), len(xs)
out = []
for t in ['SCHD','VIG','DGRO','HDV','VYM','NOBL','DVY','SDY']:
    dv, px = divs(t)
    now, n = ttm(dv, END)
    g = {}
    for y in (1, 3, 5, 10):
        past, _ = ttm(dv, END.replace(year=END.year - y))
        g[y] = ((now / past) ** (1 / y) - 1) * 100 if past else None
    yy = []
    for k in range(10):
        a, _ = ttm(dv, END.replace(year=END.year - k)); b, _ = ttm(dv, END.replace(year=END.year - k - 1))
        yy.append((a / b - 1) * 100)
    yy = yy[::-1]
    down = sum(1 for v in yy if v < 0)
    out.append((t, px, now, n, now / px * 100, g, yy, down))
    print(f"{t}: 종가 {px} · 12개월 {now:.3f}({n}회) · 분배율 {now/px*100:.2f}% · 성장 1y {g[1]:.1f} / 3y {g[3]:.1f} / 5y {g[5]:.1f} / 10y {g[10]:.1f} · 해마다(오래된 순) {' '.join(f'{v:+.1f}' for v in yy)} · 줄어든 해 {down} · 해마다 폭 표준편차 {statistics.pstdev(yy):.1f}")
