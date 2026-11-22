# divoone1122 — 야후 chart API 배당 이력·종가 받기 (write-b 2026-11-21)
import urllib.request, time, sys
T = sys.argv[1:] or ['DIVO','JEPI','JEPQ','QYLD','XYLD','SCHD','SPYD','VYM','HDV','DGRO']
for t in T:
    u = f'https://query1.finance.yahoo.com/v8/finance/chart/{t}?range=2y&interval=1d&events=div'
    d = urllib.request.urlopen(urllib.request.Request(u, headers={'User-Agent':'Mozilla/5.0'}), timeout=30).read()
    open(f'raw/{t}_chart_20261122.json','wb').write(d); print(t, len(d)); time.sleep(1)
