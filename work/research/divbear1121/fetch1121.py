# divbear1121 발행 날(11/21) 다시 받기 — SPY·SCHD 사상 최고 대비 마지막 거래일
import json, urllib.request, time, datetime
for t in ['SPY','SCHD']:
    u = f'https://query1.finance.yahoo.com/v8/finance/chart/{t}?period1=1546300800&period2={int(time.time())}&interval=1d&events=div'
    d = urllib.request.urlopen(urllib.request.Request(u, headers={'User-Agent':'Mozilla/5.0'}), timeout=30).read()
    open(f'raw/{t}_chart_20261121.json','wb').write(d)
    r = json.loads(d)['chart']['result'][0]
    ts = r['timestamp']; adj = r['indicators']['adjclose'][0]['adjclose']; cl = r['indicators']['quote'][0]['close']
    pts = [(datetime.datetime.utcfromtimestamp(a).date(), b, c) for a, b, c in zip(ts, adj, cl) if b is not None]
    hi = max(pts, key=lambda p: p[1]); last = pts[-1]
    print(t, 'max', hi[0], round(hi[1],2), 'last', last[0], 'close', round(last[2],2), 'dd', round((last[1]/hi[1]-1)*100,1))
    time.sleep(1)
