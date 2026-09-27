import json,urllib.request,sys,datetime,time
H={'User-Agent':'Mozilla/5.0'}
out={}
for t in sys.argv[1:]:
    u=f'https://query1.finance.yahoo.com/v8/finance/chart/{t}?range=2y&interval=1d&events=div'
    d=json.load(urllib.request.urlopen(urllib.request.Request(u,headers=H),timeout=20))['chart']['result'][0]
    m=d['meta'];divs=sorted((v['date'],v['amount']) for v in d.get('events',{}).get('dividends',{}).values())
    cl=[c for c in d['indicators']['quote'][0]['close'] if c]
    out[t]={'price':m['regularMarketPrice'],'hi52':m.get('fiftyTwoWeekHigh'),'lo52':m.get('fiftyTwoWeekLow'),'name':m.get('longName'),
            'divs':[(datetime.datetime.utcfromtimestamp(a).strftime('%Y-%m-%d'),round(b,4)) for a,b in divs][-8:],
            'ts':datetime.datetime.utcfromtimestamp(m['regularMarketTime']).strftime('%Y-%m-%d')}
    o=out[t];print(t,o['name'],o['price'],o['lo52'],o['hi52'],o['ts']);print('  ',o['divs'][-5:])
    time.sleep(0.5)
json.dump(out,open('research/divup0927/yahoo.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
