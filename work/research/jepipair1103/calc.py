# jepipair1103 계산 — JEPI 1만 달러, 분배금을 꺼내 쓸 때 vs 다시 넣을 때 (야후 파이낸스 일별 종가·분배, raw/JEPI_chart_1103.json)
import json, datetime as D
d = json.load(open('raw/JEPI_chart_1103.json'))['chart']['result'][0]
day = lambda t: D.datetime.fromtimestamp(t, D.UTC).date()
px = {day(t): c for t, c in zip(d['timestamp'], d['indicators']['quote'][0]['close']) if c}
dv = sorted((day(int(k)), v['amount']) for k, v in d['events']['dividends'].items())
days = sorted(px)
start, end = D.date(2021, 11, 1), days[-1]
s0 = min(x for x in days if x >= start)
P0, P1 = px[s0], px[end]
sh = 10000 / P0
cash, re_sh, months = 0.0, sh, []
for t, a in dv:
    if s0 < t <= end:
        cash += sh * a; months.append((t, sh * a))
        re_sh += re_sh * a / px[min(x for x in days if x >= t)]
yrs = (end - s0).days / 365.25
out = {
 'start': str(s0), 'end': str(end), 'P0': round(P0, 2), 'P1': round(P1, 2), 'years': round(yrs, 2),
 'price_chg_pct': round((P1 / P0 - 1) * 100, 1),
 'withdraw_end_value': round(sh * P1), 'withdraw_cash_total': round(cash), 'withdraw_total': round(sh * P1 + cash),
 'n_payouts': len(months), 'avg_month': round(cash / len(months)),
 'min_month': min((round(v), str(t)) for t, v in months), 'max_month': max((round(v), str(t)) for t, v in months),
 'reinvest_end_value': round(re_sh * P1), 'reinvest_cagr_pct': round(((re_sh * P1 / 10000) ** (1 / yrs) - 1) * 100, 1),
 'withdraw_cagr_pct_simple': round(((sh * P1 + cash) / 10000 - 1) * 100, 1),
 'cash_after_tax15': round(cash * 0.85),
 'by_year': {y: round(sum(v for t, v in months if t.year == y)) for y in range(2021, 2027)},
 'per_share_by_year': {y: round(sum(a for t, a in dv if t.year == y), 3) for y in range(2021, 2027)},
}
# 가격이 가장 낮았던 날(꺼내 쓴 쪽 평가액)
lo = min((px[x], x) for x in days if s0 <= x <= end)
out['low'] = (round(lo[0], 2), str(lo[1]), round(sh * lo[0]))
print(json.dumps(out, ensure_ascii=False, indent=1, default=str))
