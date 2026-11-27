# 매달 첫 거래일 종가에 100만원씩 적립(소수 주 허용), 분배금은 지급일(야후 events 날짜) 기준 받음.
# 재투자: 세후(15.4% 원천징수) 분배금을 그날 종가로 다시 삼 / 현금: 세후 분배금을 쌓아 둠(이자 0)
# 기준: 2026-11-27 종가(11/28 06:3x 다시 받음). 야후 chart API raw/*.json, 네이버 price API 종가와 대조
import json, datetime as D
END = D.date(2026, 11, 27)
def load(t):
    r = json.load(open(f'raw/{t}.json'))['chart']['result'][0]
    ts = [D.date.fromtimestamp(x) for x in r['timestamp']]
    cl = r['indicators']['quote'][0]['close']
    px = [(d, c) for d, c in zip(ts, cl) if c and d <= END]
    dv = {D.date.fromtimestamp(int(k)): v['amount'] for k, v in r.get('events', {}).get('dividends', {}).items()}
    # 11월 분배 103원(지급 기준일 11/30·배당락 11/27)은 야후에 아직 없음 → 한화자산운용 분배금 지급현황(11/28 받음 raw/plus_006273_1128.txt)으로 보탬
    if t == '161510.KS': dv.setdefault(D.date(2026, 11, 27), 103.0)
    return px, dv
def run(t, start, reinvest, tax=0.154):
    px, dv = load(t)
    px = [p for p in px if p[0] >= start]
    sh = cash = paid = 0; mon = None; peak = 0; mdd = 0; hist = []
    dd = {d: a for d, a in dv.items() if d >= start}
    for d, c in px:
        if (d.year, d.month) != mon:
            mon = (d.year, d.month); sh += 1_000_000 / c; paid += 1_000_000
        if d in dd:
            net = sh * dd[d] * (1 - tax)
            if reinvest: sh += net / c
            else: cash += net
        v = sh * c + cash
        hist.append((d, v, paid))
        r = v / paid
        peak = max(peak, r); mdd = min(mdd, r / peak - 1)
    v = sh * px[-1][1] + cash
    return dict(paid=paid, value=v, cash=cash, mult=v / paid, mdd=mdd, last=px[-1])
out = []
for yrs, start in [(10, D.date(2016, 12, 1)), (5, D.date(2021, 12, 1)), (3, D.date(2023, 12, 1))]:
    for t, name in [('161510.KS', 'PLUS 고배당주'), ('069500.KS', 'KODEX 200')]:
        for rv in (True, False):
            r = run(t, start, rv)
            out.append(f"{yrs}년 {name} {'재투자' if rv else '현금'}: 넣은 돈 {r['paid']/1e4:,.0f}만 · 끝값 {r['value']/1e4:,.0f}만(현금 {r['cash']/1e4:,.0f}만) · {r['mult']:.3f}배 · 수익률 기준 최대 낙폭 {r['mdd']*100:.1f}% · 마지막 {r['last']}")
# 분배금 연도별(1주당)
px, dv = load('161510.KS')
by = {}
for d, a in dv.items(): by[d.year] = by.get(d.year, 0) + a
out.append('PLUS 연도별 1주 분배금: ' + ', '.join(f'{y} {by[y]:.0f}원' for y in sorted(by)))
out.append('PLUS 분배 날짜 최근 8: ' + ', '.join(f'{d} {dv[d]:.0f}' for d in sorted(dv)[-8:]))
print('\n'.join(out)); open('calc_out.txt', 'w', encoding='utf-8').write('\n'.join(out) + '\n')
# 추가: 올해 가격 고점과 11/26 종가, 고점 날 적립 평가액(10년·재투자) → 지금
def peakinfo(t, start):
    px, dv = load(t)
    yr = [p for p in px if p[0].year == 2026]
    hi = max(yr, key=lambda p: p[1])
    return hi, px[-1]
ex = []
for t, name in [('161510.KS', 'PLUS 고배당주'), ('069500.KS', 'KODEX 200')]:
    hi, last = peakinfo(t, None)
    ex.append(f"{name} 2026 종가 고점 {hi[0]} {hi[1]:,.0f}원 → {last[0]} {last[1]:,.0f}원 ({(last[1]/hi[1]-1)*100:.1f}%)")
    # 10년 재투자 평가액: 고점 날 vs 끝
    px, dv = load(t); start = D.date(2016, 12, 1)
    sh = 0; mon = None; paid = 0; atpeak = None
    for d, c in [p for p in px if p[0] >= start]:
        if (d.year, d.month) != mon: mon = (d.year, d.month); sh += 1_000_000 / c; paid += 1_000_000
        if d in dv and d >= start: sh += sh * dv[d] * 0.846 / c
        if d == hi[0]: atpeak = (sh * c, paid)
    ex.append(f"  10년 재투자 적립 평가액: 고점 날 {atpeak[0]/1e4:,.0f}만(넣은 돈 {atpeak[1]/1e4:,.0f}만) → 끝 {sh*px[-1][1]/1e4:,.0f}만")
# 2026년 1주 분배금 ÷ 11/26 종가
px, dv = load('161510.KS')
last12 = sum(a for d, a in dv.items() if d > D.date(2025, 11, 27))
ex.append(f"PLUS 최근 12개월(2025-11-28~2026-11-27) 1주 분배금 {last12:.0f}원 ÷ 11/27 종가 {px[-1][1]:,.0f}원 = {last12/px[-1][1]*100:.2f}%")
print('\n'.join(ex)); open('calc_out.txt', 'a', encoding='utf-8').write('\n'.join(ex) + '\n')
# 추가 2: 코스피 쪽 고점 날(2026-06-22) 두 상품 10년 재투자 적립 평가액, 그 뒤 줄어든 비율
def val_on(t, start, day):
    px, dv = load(t); sh = 0; mon = None; paid = 0; v = None
    for d, c in [p for p in px if p[0] >= start]:
        if (d.year, d.month) != mon: mon = (d.year, d.month); sh += 1_000_000 / c; paid += 1_000_000
        if d in dv: sh += sh * dv[d] * 0.846 / c
        if d == day: v = (sh * c, paid)
    return v, sh * px[-1][1]
ex2 = []
for t, name in [('161510.KS', 'PLUS 고배당주'), ('069500.KS', 'KODEX 200')]:
    (vp, pp), ve = val_on(t, D.date(2016, 12, 1), D.date(2026, 6, 22))
    ex2.append(f"{name} 10년 재투자 적립: 2026-06-22 {vp/1e4:,.0f}만(넣은 돈 {pp/1e4:,.0f}만) → 11/27 {ve/1e4:,.0f}만 ({(ve/vp-1)*100:.1f}%, 그 사이 5번 500만 더 넣음 포함)")
print('\n'.join(ex2)); open('calc_out.txt', 'a', encoding='utf-8').write('\n'.join(ex2) + '\n')
