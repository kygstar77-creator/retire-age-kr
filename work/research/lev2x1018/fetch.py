import json,urllib.request,sys
sys.stdout.reconfigure(encoding='utf-8')
for t in ['000660.KS','005930.KS']:
    u=f'https://query1.finance.yahoo.com/v8/finance/chart/{t}?range=2y&interval=1d'
    d=json.load(urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'Mozilla/5.0'})))
    print(str(d)[:300]); r=d['chart']['result'][0]; ts=r['timestamp']; c=r['indicators']['quote'][0]['close']
    json.dump([(x,y) for x,y in zip(ts,c)],open(f'raw/{t}.json','w'))
    print(t,len(ts),r['meta'].get('regularMarketPrice'))
