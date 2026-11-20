# 야후 ^SP500TR(배당 재투자)·^GSPC(가격)·KRW=X, FRED DEXKOUS·SP500 받기 (2026-11-21 firemap-write)
import urllib.request, json, sys
sys.path.insert(0, '../../')
H = {'User-Agent': 'Mozilla/5.0'}
for n, t in [] and [('sp500tr', '%5ESP500TR'), ('gspc', '%5EGSPC')]:
    u = f'https://query1.finance.yahoo.com/v8/finance/chart/{t}?period1=-1400000000&period2=1800000000&interval=1d'
    d = urllib.request.urlopen(urllib.request.Request(u, headers=H), timeout=40).read()
    open(f'raw/{n}_20261121.json', 'wb').write(d); print(n, len(d))
import apis
for s in ['DEXKOUS', 'SP500']:
    r = apis.fred(s, 100000)
    json.dump(r, open(f'raw/fred_{s}_20261121.json', 'w'), default=str); print(s, type(r), (len(r) if hasattr(r, '__len__') else r))
