# tdf1115: 국내 상장 TDF ETF 9개 — 야후 일별 종가+분배금 재투자로 1년·3개월 총수익과 최근 고점 대비 하락폭을 직접 계산,
# 네이버페이 증권 ETF 지표(총보수·1년 수익률·순자산)와 맞대 본다
import json, sys, datetime as dt
sys.stdout.reconfigure(encoding='utf-8')
codes = '433970 442550 433980 442560 0025N0 434060 442570 0082V0 433880'.split()
END = dt.date(2026, 11, 13)
def series(c):
    r = json.load(open(f'raw/yahoo_{c}.json', encoding='utf-8'))['chart']['result'][0]
    rows = [(dt.datetime.fromtimestamp(t + 9*3600, dt.UTC).date(), v) for t, v in zip(r['timestamp'], r['indicators']['quote'][0]['close']) if v]
    divs = {dt.datetime.fromtimestamp(int(k) + 9*3600, dt.UTC).date(): v['amount'] for k, v in r.get('events', {}).get('dividends', {}).items()}
    return rows, divs
def tr(c, start):
    rows, divs = series(c)
    rows = [x for x in rows if start <= x[0] <= END]
    sh = 1.0; p0 = rows[0][1]; peak = 0; mdd = 0
    for day, px in rows[1:]:
        if day in divs: sh += sh * divs[day] / px
    return (sh * rows[-1][1] / p0 - 1) * 100, rows[0][0], rows[-1][0]
def drawdown(c, start):
    rows, divs = series(c); rows = [x for x in rows if start <= x[0] <= END]
    sh = 1.0; peak = 0; pk_day = None; v = 0
    for day, px in rows:
        if day in divs: sh += sh * divs[day] / px
        v = sh * px
        if v > peak: peak, pk_day = v, day
    return (v / peak - 1) * 100, pk_day
for c in codes:
    n = json.load(open(f'raw/naver_{c}.json', encoding='utf-8')); k = n['etfKeyIndicator']
    one = tr(c, dt.date(2025, 11, 13)) if c not in ('0082V0',) else (None, None, None)
    th = tr(c, dt.date(2026, 8, 13))
    dd = drawdown(c, dt.date(2025, 11, 13))
    o = f"{one[0]:.2f}% ({one[1]}~{one[2]})" if one[0] is not None else '1년 안 됨'
    print(f"{n['stockName']} | 총보수 {k['totalFee']}% | 순자산 {k['totalNav']} | 직접 1년 {o} | 네이버 1년 {k['returnRate1y']}% | 직접 3개월 {th[0]:.2f}% | 네이버 3개월 {k.get('returnRate3m')}% | 1년 안 고점 대비 {dd[0]:.2f}% (고점 {dd[1]})")
