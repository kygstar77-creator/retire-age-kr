# 고배당·월배당 ETF 12종 — 최근 12개월 분배금 합계, 현재가, 최근 배당락일, 1년 주가·총수익
# 자료: Yahoo Finance chart API(무키). 배당률은 여기서 계산한다([계산] 표시 대상).
import json, sys, datetime, urllib.request, time
sys.stdout.reconfigure(encoding='utf-8')
UA = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
SYMS = ['SCHD', 'VYM', 'HDV', 'DVY', 'SPYD', 'DGRO', 'VIG', 'NOBL', 'SDY', 'JEPI', 'JEPQ', 'QYLD']

def get(u, t=30, tries=3):
    for i in range(tries):
        try:
            return json.load(urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=t))
        except Exception as e:
            if i == tries - 1: raise
            time.sleep(1.5 * (i + 1))

def day(ts): return datetime.datetime.fromtimestamp(int(ts), datetime.UTC).strftime('%Y-%m-%d')

out = {}
for s in SYMS:
    d = get(f'https://query1.finance.yahoo.com/v8/finance/chart/{s}?range=2y&interval=1d&events=div')
    r = d['chart']['result'][0]
    m = r['meta']
    price = m.get('regularMarketPrice')
    ts = r['timestamp']; close = r['indicators']['quote'][0]['close']
    adj = r['indicators'].get('adjclose', [{}])[0].get('adjclose')
    divs = [(day(k), v['amount']) for k, v in sorted(r.get('events', {}).get('dividends', {}).items(), key=lambda kv: int(kv[0]))]
    today = datetime.date.today()
    y1 = today - datetime.timedelta(days=365)
    last12 = [(dt, a) for dt, a in divs if datetime.date.fromisoformat(dt) > y1]
    # 1년 전 가장 가까운 거래일 종가/수정종가
    i0 = None
    for i, t in enumerate(ts):
        if datetime.date.fromtimestamp(t) >= y1: i0 = i; break
    px0 = close[i0] if i0 is not None else None
    adj0 = adj[i0] if (adj and i0 is not None) else None
    adjN = adj[-1] if adj else None
    out[s] = {
        'price': price, 'asof_price_date': day(ts[-1]),
        'divs_12m': last12, 'sum_12m': round(sum(a for _, a in last12), 6),
        'n_12m': len(last12), 'last_ex': divs[-1][0] if divs else None, 'last_amt': divs[-1][1] if divs else None,
        'px_1y_ago': px0, 'px_1y_ago_date': day(ts[i0]) if i0 is not None else None,
        'adj_1y_ago': adj0, 'adj_now': adjN,
        'exchange': m.get('fullExchangeName') or m.get('exchangeName'), 'currency': m.get('currency'),
    }
    y = (out[s]['sum_12m'] / price * 100) if price else None
    pxret = ((price / px0 - 1) * 100) if px0 else None
    totret = ((adjN / adj0 - 1) * 100) if (adj0 and adjN) else None
    out[s]['yield_calc_pct'] = round(y, 2) if y else None
    out[s]['price_ret_1y_pct'] = round(pxret, 2) if pxret is not None else None
    out[s]['total_ret_1y_pct'] = round(totret, 2) if totret is not None else None
    print(f"{s:5s} {price:8.2f} 12M분배 {out[s]['sum_12m']:7.4f} ({out[s]['n_12m']}회) 배당률 {out[s]['yield_calc_pct']:5.2f}%  주가1년 {pxret:+6.2f}%  총수익1년 {totret:+6.2f}%  최근배당락 {out[s]['last_ex']}")
json.dump(out, open('work/research/hidiv12/raw.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('저장 work/research/hidiv12/raw.json')
