import urllib.request,json,sys
sys.stdout.reconfigure(encoding='utf-8')
for t in sys.argv[1:]:
    try:
        u=f'https://query1.finance.yahoo.com/v8/finance/chart/{t}?range=1y&interval=1d'
        d=json.loads(urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'Mozilla/5.0'}),timeout=20).read())['chart']['result'][0]
        m=d['meta'];c=[x for x in d['indicators']['quote'][0]['close'] if x]
        print(t,m.get('longName'),m.get('currency'),m.get('exchangeName'),'last',m['regularMarketPrice'],'52wH',m.get('fiftyTwoWeekHigh'),'52wL',m.get('fiftyTwoWeekLow'),'t',m['regularMarketTime'])
    except Exception as e: print(t,'ERR',e)
