# 나스닥100(^NDX) vs S&P500(^GSPC) 하락장 비교 — Yahoo chart API 일별 종가(가격 지수, 배당 뺌)
# 원자료: raw/%5ENDX.json, raw/%5EGSPC.json (2026-11-19 22:43 다시 받음, 마지막 거래일 2026-11-18 — 11/18 받은 것은 raw/1118/)
import json, datetime as dt

def load(t):
    r = json.load(open(f'raw/{t}.json'))['chart']['result'][0]
    out = []
    for ts, c in zip(r['timestamp'], r['indicators']['quote'][0]['close']):
        if c is None: continue
        out.append((dt.datetime.fromtimestamp(ts, dt.UTC).date(), c))
    return out

N = load('%5ENDX'); S = load('%5EGSPC')
S = [x for x in S if x[0] >= N[0][0]]   # 같은 시작일(1985-10-01)

def episode(series, a, b, pk0=dt.date(1900,1,1)):
    """a~b 사이 바닥, 그 바닥 앞 최고점(전체 과거 기준), 그 최고점 회복일"""
    seg = [x for x in series if a <= x[0] <= b]
    trough = min(seg, key=lambda x: x[1])
    before = [x for x in series if pk0 <= x[0] <= trough[0]]
    peak = max(before, key=lambda x: x[1])
    rec = next((x for x in series if x[0] > trough[0] and x[1] >= peak[1]), None)
    dd = trough[1] / peak[1] - 1
    yrs = (rec[0] - peak[0]).days / 365.25 if rec else None
    return peak, trough, dd, rec, yrs

# (이름, 바닥 찾는 구간 시작·끝, 고점 찾기 시작) — 고점은 그 하락이 시작된 해 안에서 찾는다(금융위기를 2000년 고점으로 재지 않게)
EP = [('닷컴 버블', dt.date(2000,1,1), dt.date(2003,12,31), dt.date(1999,1,1)),
      ('금융위기', dt.date(2007,6,1), dt.date(2009,12,31), dt.date(2007,1,1)),
      ('코로나', dt.date(2020,1,1), dt.date(2020,6,30), dt.date(2020,1,1)),
      ('2022 금리 인상', dt.date(2022,1,1), dt.date(2022,12,31), dt.date(2021,6,1)),
      ('2025 관세 충격', dt.date(2025,1,1), dt.date(2025,6,30), dt.date(2024,12,1))]

for name, a, b, k in EP:
    for lab, s in (('NDX', N), ('SPX', S)):
        p, t, dd, rec, yrs = episode(s, a, b, k)
        print(f'{name} {lab}: 고점 {p[0]} {p[1]:,.0f} → 바닥 {t[0]} {t[1]:,.0f} = {dd*100:.1f}% · 회복 {rec[0] if rec else "아직"} ({yrs:.1f}년)' if rec else
              f'{name} {lab}: 고점 {p[0]} {p[1]:,.0f} → 바닥 {t[0]} {t[1]:,.0f} = {dd*100:.1f}% · 회복 아직')

# 지금 위치
for lab, s in (('NDX', N), ('SPX', S)):
    p = max(s, key=lambda x: x[1]); last = s[-1]
    print(f'지금 {lab}: 사상 최고 {p[0]} {p[1]:,.0f} · {last[0]} {last[1]:,.0f} = 최고 대비 {(last[1]/p[1]-1)*100:.1f}%')

# 기간 수익(가격): 10년·20년·1985-10 이후
def at(s, d):
    return next(x for x in reversed(s) if x[0] <= d)
for yrs in (5, 10, 20):
    d0 = N[-1][0].replace(year=N[-1][0].year - yrs)
    for lab, s in (('NDX', N), ('SPX', S)):
        a = at(s, d0); z = s[-1]
        tot = z[1]/a[1]; cagr = tot ** (1/yrs) - 1
        print(f'{yrs}년({a[0]}~{z[0]}) {lab}: {tot:.2f}배 · 연 {cagr*100:.1f}%')
for lab, s in (('NDX', N), ('SPX', S)):
    a = s[0]; z = s[-1]; y = (z[0]-a[0]).days/365.25
    print(f'전체({a[0]}~{z[0]}, {y:.1f}년) {lab}: {z[1]/a[1]:.1f}배 · 연 {((z[1]/a[1])**(1/y)-1)*100:.1f}%')

# 1천만원을 고점에 넣었다면(닷컴) 바닥에서 얼마
for lab, s in (('NDX', N), ('SPX', S)):
    p, t, dd, rec, yrs = episode(s, dt.date(2000,1,1), dt.date(2003,12,31))
    print(f'닷컴 고점 1천만원 {lab}: 바닥 {1000*(1+dd):,.0f}만원')

# 닷컴 고점 달(2000-03)부터 매달 첫 거래일 같은 돈을 넣었다면 — 넣은 돈 합계를 처음 다시 넘은 달(바닥 뒤)
def dca(s, start):
    months = {}
    for d, c in s:
        if d >= start: months.setdefault((d.year, d.month), (d, c))
    units = inv = 0; rows = []
    for (y, m), (d, c) in sorted(months.items()):
        units += 1 / c; inv += 1
        rows.append((d, units * c / inv - 1))
    wi = min(range(len(rows)), key=lambda i: rows[i][1])   # 가장 나빴던 달
    out = next((d for d, r in rows[wi:] if r >= 0), None)  # 그 뒤 처음 본전
    return out, rows[wi][1], rows[wi][0]
for lab, s in (('NDX', N), ('SPX', S)):
    out, worst, wd = dca(s, dt.date(2000, 3, 1))
    print(f'닷컴 고점 달부터 매달 적립 {lab}: 가장 나빴을 때 {wd} {worst*100:.1f}% · 그 뒤 본전 회복 {out}')

# 나스닥100 매달 적립(2000-03~): 첫 본전 회복 뒤 다시 밑으로 갔는지, 그 뒤 마지막으로 본전을 넘은 달
months = {}
for d, c in N:
    if d >= dt.date(2000, 3, 1): months.setdefault((d.year, d.month), (d, c))
units = inv = 0; rows = []
for k in sorted(months):
    d, c = months[k]; units += 1 / c; inv += 1; rows.append((d, units * c / inv - 1))
first = next(d for d, r in rows if d > dt.date(2001, 10, 1) and r >= 0)
after = [(d, r) for d, r in rows if d > first]
w2 = min(after, key=lambda x: x[1])
back = next(d for d, r in after if d > w2[0] and r >= 0)
print(f'NDX 적립: 첫 본전 {first} → 다시 최저 {w2[0]} {w2[1]*100:.1f}% → 다시 본전 {back}')
