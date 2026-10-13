import json,urllib.request,datetime
def get(t,rng='14mo'):
    u=f'https://query1.finance.yahoo.com/v8/finance/chart/{t}?range=2y&interval=1d&events=div%7Csplit'
    r=urllib.request.Request(u,headers={'User-Agent':'Mozilla/5.0'})
    return json.load(urllib.request.urlopen(r,timeout=30))
for t in ['QQQ','QQQM','KRW=X']:
    d=get(t); json.dump(d,open(f'y_{t.replace("=","")}.json','w'))
    res=d['result'][0] if 'result' in d else d['chart']['result'][0]
    ts=res['timestamp']; c=res['indicators']['quote'][0]['close']
    print(t,len(ts),datetime.date.fromtimestamp(ts[-1]),c[-1], res['meta'].get('regularMarketPrice'))
    print(res.get('events',{}).get('dividends') and [(datetime.date.fromtimestamp(v['date']).isoformat(),v['amount']) for v in sorted(res['events']['dividends'].values(),key=lambda x:x['date'])][-8:])
