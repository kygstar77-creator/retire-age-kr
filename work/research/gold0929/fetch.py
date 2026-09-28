import json, urllib.request, datetime, sys
sys.stdout.reconfigure(encoding='utf-8')
UA={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 Safari/537.36'}
out={'fetched':datetime.datetime.now().strftime('%Y-%m-%d %H:%M'),'yahoo':{}}
for s,rng in [('GC=F','5y'),('KRW=X','2y'),('132030.KS','2y'),('411060.KS','2y')]:
    u=f'https://query1.finance.yahoo.com/v8/finance/chart/{s.replace("=","%3D")}?range={rng}&interval=1d'
    try:
        j=json.load(urllib.request.urlopen(urllib.request.Request(u,headers=UA),timeout=30))
        r=j['chart']['result'][0]; m=r['meta']; ts=r['timestamp']; c=r['indicators']['quote'][0]['close']
        off=m.get('gmtoffset',0)
        rows=[[datetime.datetime.utcfromtimestamp(t+off).strftime('%Y-%m-%d %H:%M'),v] for t,v in zip(ts,c) if v is not None]
        out['yahoo'][s]={'url':u,'meta':{k:m.get(k) for k in ['currency','symbol','longName','shortName','regularMarketPrice','regularMarketTime','fiftyTwoWeekHigh','fiftyTwoWeekLow','chartPreviousClose','exchangeTimezoneName']},'rows':rows}
        print(s,len(rows),rows[-1],m.get('longName'),m.get('fiftyTwoWeekHigh'),m.get('regularMarketPrice'),datetime.datetime.utcfromtimestamp(m.get('regularMarketTime',0)+off))
    except Exception as e: print(s,'ERR',e)
json.dump(out,open('data.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
