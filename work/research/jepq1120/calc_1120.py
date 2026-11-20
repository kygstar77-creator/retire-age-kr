# jepq1120 발행 날(11/20) 다시 계산 — 11/19 종가·11/20 매매기준율
import json, datetime as dt
y = json.load(open('raw/yahoo_jepq_1120.json'))['chart']['result'][0]
px = {dt.datetime.fromtimestamp(t, dt.UTC).date(): c for t, c in zip(y['timestamp'], y['indicators']['quote'][0]['close'])}
px = {d: c for d, c in px.items() if c is not None}; px[dt.date(2026, 11, 19)] = y['meta']['regularMarketPrice']  # 11/19 종가(meta, 21:00 UTC)
fx = {dt.datetime.strptime(a, '%Y%m%d').date(): float(b) for a, b, _ in json.load(open('raw/ecos_usdkrw_1120.json', encoding='utf-8'))}
def fx_on(d):
    while d not in fx: d -= dt.timedelta(days=1)
    return d, fx[d]
rows = json.load(open('raw/nasdaq_div_1120.json', encoding='utf-8'))['data']['dividends']['rows']
md = lambda s: dt.datetime.strptime(s, '%m/%d/%Y').date()
buy = dt.date(2025, 11, 18); fxd, f0 = fx_on(buy); p0 = px[buy]
usd = 100_000_000 / f0; sh = int(usd // p0); cash = usd - sh * p0
print(f'매수 {buy} 종가 {p0:.2f} 환율 {fxd} {f0} → {usd:,.0f}달러 {sh}주 남은 달러 {cash:.2f}')
tot_g = tot_n = 0; out = []
for r in sorted(rows, key=lambda r: md(r['exOrEffDate'])):
    ex = md(r['exOrEffDate'])
    if not (buy < ex <= dt.date(2026, 11, 19)): continue
    a = float(r['amount'].strip('$')); pay = md(r['paymentDate']); fd, f = fx_on(pay)
    g = sh * a * f; n = g * 0.85; tot_g += g; tot_n += n
    out.append((ex, pay, a, f, g, n)); print(f'배당락 {ex} 지급 {pay} 주당 {a} 환율({fd}) {f} 세전 {g:,.0f} 세후 {n:,.0f}')
ns = [o[5] for o in out]
print(f'{len(out)}번 세전 합 {tot_g:,.0f} 세후 합 {tot_n:,.0f} 세후 월평균 {tot_n/len(out):,.0f}')
mn = min(out, key=lambda o: o[5]); mx = max(out, key=lambda o: o[5])
print(f'세후 최소 {mn[1]} {mn[5]:,.0f} 최대 {mx[1]} {mx[5]:,.0f} 차이 {mx[5]-mn[5]:,.0f} 배 {mx[5]/mn[5]:.2f}')
amin = min(out, key=lambda o: o[2]); amax = max(out, key=lambda o: o[2])
print(f'주당 최소 {amin[2]}({amin[0]}) 최대 {amax[2]}({amax[0]})')
last = max(px); p1 = px[last]; fd1, f1 = fx_on(dt.date(2026, 11, 20))
val = (sh * p1 + cash) * f1
print(f'지금 {last} 종가 {p1:.2f} 환율({fd1}) {f1} 평가 {val:,.0f} 주가 등락 {p1/p0-1:+.2%} 원화 평가 차 {val-1e8:+,.0f}')
print(f'평가+세후 분배금 {val+tot_n:,.0f} → {((val+tot_n)/1e8-1):+.2%}')
# 같은 기간 원화 환율 효과
print(f'환율 {f0}→{f1} {f1/f0-1:+.2%}')
# 52주
lo = min(v for d, v in px.items() if d > dt.date(2025, 11, 18)); hi = max(v for d, v in px.items() if d > dt.date(2025, 11, 18))
print(f'52주 종가 범위 {lo:.2f}~{hi:.2f}')
# 세전 분배율(최근 12번 주당 합 / 지금 종가)
s12 = sum(o[2] for o in out); print(f'주당 12번 합 {s12:.5f} / 종가 {p1:.2f} = {s12/p1:.2%}')
# 달러로만 셌다면
du = sum(o[2] for o in out) * sh * 0.85; vu = sh * p1 + cash
print(f'달러 기준: 처음 {usd:,.0f} 평가 {vu:,.0f} 세후 분배금 {du:,.0f} 합 {vu+du:,.0f} → {((vu+du)/usd-1):+.2%}')
print(f'세후 원화 분배금 / 1억 = {tot_n/1e8:.2%}')
for o in out: print(f'{o[1].month}월 {o[5]/1e4:.0f}만원')
