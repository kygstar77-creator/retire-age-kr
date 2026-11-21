# tigerdj1122 — 야후 일별 종가·분배 events(458730.KS·SCHD·KRW=X) + FRED DEXKOUS, 2026-11-21
import json, urllib.request, time, sys
sys.path.insert(0, r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work')
T = ['458730.KS', 'SCHD', 'KRW=X']
for t in T:
    u = f'https://query1.finance.yahoo.com/v8/finance/chart/{t}?period1=1685577600&period2={int(time.time())}&interval=1d&events=div'
    req = urllib.request.Request(u, headers={'User-Agent': 'Mozilla/5.0'})
    d = urllib.request.urlopen(req, timeout=30).read()
    open(f'raw/{t}_chart_20261121.json', 'wb').write(d); print(t, len(d)); time.sleep(1)
u = 'https://fred.stlouisfed.org/graph/fredgraph.csv?id=DEXKOUS&cosd=2023-06-01'
req = urllib.request.Request(u, headers={'User-Agent': 'Mozilla/5.0'})
d = urllib.request.urlopen(req, timeout=30).read(); open('raw/fred_DEXKOUS_20261121.csv', 'wb').write(d); print('DEXKOUS', len(d))
