# 야후 차트 API로 일별 종가를 받아 raw/px_<티커>.json 에 저장
import json, sys, urllib.request, datetime as dt
for t in sys.argv[1:]:
    u = f'https://query1.finance.yahoo.com/v8/finance/chart/{t}?period1=1730419200&period2=1794268800&interval=1d'
    r = urllib.request.Request(u, headers={'User-Agent': 'Mozilla/5.0'})
    d = json.load(urllib.request.urlopen(r, timeout=60))
    res = d['chart']['result'][0]
    ts = res['timestamp']; cl = res['indicators']['quote'][0]['close']
    rows = [[(dt.datetime.utcfromtimestamp(a) + dt.timedelta(hours=9)).strftime('%Y-%m-%d'), c] for a, c in zip(ts, cl) if c]
    json.dump({'ticker': t, 'got': dt.datetime.now().strftime('%Y-%m-%d %H:%M'), 'src': u, 'rows': rows}, open(f'raw/px_{t}.json', 'w'), ensure_ascii=False)
    print(t, len(rows), rows[0], rows[-1])
