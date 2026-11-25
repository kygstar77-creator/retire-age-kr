import urllib.request, urllib.parse
for t in ['JEPI','^VIX','SPY','JEPQ']:
    u='https://query1.finance.yahoo.com/v8/finance/chart/'+urllib.parse.quote(t)+'?period1=1588291200&period2=1800000000&interval=1d&events=div'
    d=urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'Mozilla/5.0'}),timeout=30).read()
    open('raw/'+t.replace('^','')+'.json','wb').write(d); print(t,len(d))
