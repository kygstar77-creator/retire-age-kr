# SCHD·SPY 일별(배당 반영 adjclose·배당 이벤트) 야후, 원/달러 FRED DEXKOUS (2026-11-24 firemap-write)
import urllib.request, json, sys
sys.path.insert(0, '../../')
H = {'User-Agent': 'Mozilla/5.0'}
for n, t in [('schd', 'SCHD'), ('spy', 'SPY'), ('krw', 'KRW%3DX')]:
    u = f'https://query1.finance.yahoo.com/v8/finance/chart/{t}?period1=1300000000&period2=1800000000&interval=1d&events=div%2Csplit'
    d = urllib.request.urlopen(urllib.request.Request(u, headers=H), timeout=40).read()
    open(f'raw/{n}_20261124.json', 'wb').write(d); print(n, len(d))
import apis
r = apis.fred('DEXKOUS', 100000)
json.dump(r, open('raw/fred_DEXKOUS_20261124.json', 'w'), default=str); print('DEXKOUS', len(r), r[-1] if r else None)
