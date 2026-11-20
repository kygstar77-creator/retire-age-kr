# divbear1121 — 야후 일별 가격(배당 재투자 adjclose) 받기, 2026-11-20
import json, urllib.request, time, datetime
T = ['SPY','SCHD','JEPI','HDV','SPYD','VYM','DGRO','VIG']
for t in T:
    u = f'https://query1.finance.yahoo.com/v8/finance/chart/{t}?period1=1546300800&period2={int(time.time())}&interval=1d&events=div'
    req = urllib.request.Request(u, headers={'User-Agent':'Mozilla/5.0'})
    d = urllib.request.urlopen(req, timeout=30).read()
    open(f'raw/{t}_chart_20261120.json','wb').write(d)
    print(t, len(d))
    time.sleep(1)
