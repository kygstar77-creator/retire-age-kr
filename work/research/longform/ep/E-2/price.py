"""테슬라 주가 5년 — 나스닥 공식 과거 시세(api.nasdaq.com) 1차, 야후 차트로 대조 → price.json (2026-10-01, E-1 방식 그대로)."""
import json, os, sys, urllib.request, datetime
sys.stdout.reconfigure(encoding='utf-8')
H = os.path.dirname(os.path.abspath(__file__)); R = os.path.join(H, 'raw')
UA = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/130 Safari/537.36', 'Accept': 'application/json'}

def get(u, p):
    if not os.path.exists(p):
        open(p, 'wb').write(urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=60).read())
    return json.load(open(p, encoding='utf-8'))

today = datetime.date(2026, 10, 1)
n = get(f'https://api.nasdaq.com/api/quote/TSLA/historical?assetclass=stocks&fromdate=2021-09-29&todate={today}&limit=2000',
        os.path.join(R, 'nasdaq_TSLA.json'))
rows = n['data']['tradesTable']['rows']
nas = {datetime.datetime.strptime(r['date'], '%m/%d/%Y').strftime('%Y%m%d'): float(r['close'].replace('$', '').replace(',', '')) for r in rows}
y = get('https://query1.finance.yahoo.com/v8/finance/chart/TSLA?range=5y&interval=1d', os.path.join(R, 'TSLA_5y.json'))['chart']['result'][0]
yah = {datetime.datetime.utcfromtimestamp(t).strftime('%Y%m%d'): c for t, c in zip(y['timestamp'], y['indicators']['quote'][0]['close']) if c}
both = sorted(set(nas) & set(yah)); diff = [d for d in both if abs(nas[d] / yah[d] - 1) > 0.005]
s = sorted(nas.items())
def at(d):  # d 이전 마지막 거래일
    return max((k for k in nas if k <= d)), nas[max((k for k in nas if k <= d))]
peak = max(s, key=lambda x: x[1]); last = s[-1]
# 최대 낙폭(고점 → 이후 저점)
hi = s[0]; mdd = (0, None, None)
for d, c in s:
    if c > hi[1]: hi = (d, c)
    dd = c / hi[1] - 1
    if dd < mdd[0]: mdd = (dd, hi[0], d)
out = {'source': 'api.nasdaq.com historical (나스닥 공식), 야후 대조', 'days': len(s), 'first': s[0], 'last': last,
       'y1': at('20250929'), 'y3': at('20230929'), 'y5': at('20210929') if s[0][0] <= '20210929' else s[0],
       'peak': peak, 'mdd': {'pct': round(mdd[0] * 100, 1), 'from': mdd[1], 'to': mdd[2]},
       'yahoo_compare': {'days': len(both), 'over_0.5pct': len(diff), 'sample': diff[:5]}}
for k in ('y1', 'y3', 'y5'):
    out[k + '_x'] = round(last[1] / out[k][1], 2)
json.dump(out, open(os.path.join(H, 'price.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(json.dumps(out, ensure_ascii=False, indent=1))
