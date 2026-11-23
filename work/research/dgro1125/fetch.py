import urllib.request
H={'User-Agent':'Mozilla/5.0'}
for t in ['DGRO','SCHD','VIG','SPY']:
    u=f'https://query1.finance.yahoo.com/v8/finance/chart/{t}?period1=1262304000&period2=1800000000&interval=1d&events=div'
    d=urllib.request.urlopen(urllib.request.Request(u,headers=H),timeout=30).read()
    open(f'raw/{t}.json','wb').write(d); print(t,len(d))
for nm,u in [('ish_page','https://www.ishares.com/us/products/264623/ishares-core-dividend-growth-etf'),
             ('ish_hold','https://www.ishares.com/us/products/264623/ishares-core-dividend-growth-etf/1467271812596.ajax?fileType=csv&fileName=DGRO_holdings&dataType=fund')]:
    try:
        d=urllib.request.urlopen(urllib.request.Request(u,headers=H),timeout=40).read(); open(f'raw/{nm}','wb').write(d); print(nm,len(d))
    except Exception as e: print(nm,'ERR',e)
