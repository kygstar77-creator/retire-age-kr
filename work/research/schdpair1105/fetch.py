# schdpair1105 — Yahoo chart API(무키) 배당 이벤트 12년. raw/yh_<티커>_<날짜>.json
import sys, json, time, urllib.request, pathlib, datetime
RAW = pathlib.Path(__file__).resolve().parent / 'raw'; D = datetime.date.today().strftime('%Y%m%d')
for t in sys.argv[1:] or ['SCHD','VIG','DGRO','HDV','VYM','NOBL','DVY','SDY']:
    u = f'https://query1.finance.yahoo.com/v8/finance/chart/{t}?range=12y&interval=1d&events=div%7Csplit&includeAdjustedClose=true'
    try:
        b = urllib.request.urlopen(urllib.request.Request(u, headers={'User-Agent': 'Mozilla/5.0'}), timeout=40).read()
        r = json.loads(b)['chart']['result'][0]
        (RAW / f'yh_{t}_{D}.json').write_bytes(b)
        dv = r.get('events', {}).get('dividends', {})
        last = max(dv.values(), key=lambda x: x['date'])
        print(t, 'div', len(dv), 'last', datetime.datetime.utcfromtimestamp(last['date']).date(), last['amount'], 'close', r['meta'].get('regularMarketPrice'))
    except Exception as e:
        print(t, 'ERR', str(e)[:100])
    time.sleep(0.5)
