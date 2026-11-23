import json,urllib.request
for t in ['VIG','VYM','DGRO','SCHD','SPY']:
    u=f'https://query1.finance.yahoo.com/v8/finance/chart/{t}?period1=1262304000&period2=1800000000&interval=1d&events=div'
    d=urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'Mozilla/5.0'}),timeout=30).read()
    open(f'raw/{t}.json','wb').write(d); print(t,len(d))
