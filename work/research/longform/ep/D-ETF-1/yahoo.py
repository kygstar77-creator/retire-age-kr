# D-ETF-1 가격·분배 이력 — Yahoo chart API(무키), 일별 10년 + 배당 이벤트. raw/yh_<티커>_<날짜>.json
import sys, json, time, urllib.request, pathlib, datetime
RAW = pathlib.Path(__file__).resolve().parent / 'raw'; D = datetime.date.today().strftime('%Y%m%d')
T = sys.argv[1:] or ['SCHD','VYM','VIG','DGRO','HDV','SPYD','JEPI','JEPQ','DIVO','SPY','NOBL','458730.KS','446720.KS','402970.KS','489250.KS','161510.KS','466940.KS','0105E0.KS','KRW=X']
for t in T:
    u = f'https://query1.finance.yahoo.com/v8/finance/chart/{t}?range=12y&interval=1d&events=div%7Csplit&includeAdjustedClose=true'
    try:
        b = urllib.request.urlopen(urllib.request.Request(u, headers={'User-Agent': 'Mozilla/5.0'}), timeout=40).read()
        d = json.loads(b); r = d['chart']['result'][0]
        (RAW / f'yh_{t.replace("=","_")}_{D}.json').write_bytes(b)
        ts = r['timestamp']; dv = r.get('events', {}).get('dividends', {})
        print(t, len(ts), datetime.datetime.utcfromtimestamp(ts[0]).date(), '→', datetime.datetime.utcfromtimestamp(ts[-1]).date(), 'div', len(dv))
    except Exception as e:
        print(t, 'ERR', str(e)[:100])
    time.sleep(0.5)
