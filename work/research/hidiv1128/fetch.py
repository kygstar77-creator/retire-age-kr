# 미국 고배당 ETF 3종(VYM·HDV·SPYD) — 야후 chart(일별 종가·배당 events). 2026-11-27 받음.
import json, urllib.request, sys
sys.stdout.reconfigure(encoding='utf-8')
T=['VYM','HDV','SPYD']
UA={'User-Agent':'Mozilla/5.0'}
for t in T:
    u=f'https://query1.finance.yahoo.com/v8/finance/chart/{t}?period1=946684800&period2=1800000000&interval=1d&events=div'
    d=urllib.request.urlopen(urllib.request.Request(u,headers=UA),timeout=30).read()
    open(f'raw/{t}.json','wb').write(d)
    j=json.loads(d)['chart']['result'][0]
    print(t,'첫',j['timestamp'][0],'수',len(j['timestamp']),'배당',len(j.get('events',{}).get('dividends',{})))
