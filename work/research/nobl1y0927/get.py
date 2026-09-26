import json,urllib.request,time,datetime
T='BDX,TGT,EMR,NDSN,FDS,FAST,IBM,ADP,MDT,GPC,KO,ROP,JNJ,CVX,ERIE,EXPD,NUE,ECL,ABBV,XOM,WST,SHW,SJM,SWK,BEN'.split(',')
out=[]
for t in T:
    u=f'https://query1.finance.yahoo.com/v8/finance/chart/{t}?range=1y&interval=1d&events=div'
    d=json.load(urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'Mozilla/5.0'})))
    r=d['chart']['result'][0]; q=r['indicators']['quote'][0]; ts=r['timestamp']
    cl=[(a,c) for a,c in zip(ts,q['close']) if c]
    first=cl[0]; last=cl[-1]
    hi=max(c for a,c in cl); lo=min(c for a,c in cl)
    divs=r.get('events',{}).get('dividends',{})
    dv=sorted(divs.values(),key=lambda x:x['date'])
    s12=sum(x['amount'] for x in dv)
    out.append(dict(t=t,name=r['meta'].get('longName'),d0=datetime.date.fromtimestamp(first[0]).isoformat(),p0=round(first[1],2),
      d1=datetime.date.fromtimestamp(last[0]).isoformat(),p1=round(last[1],2),ret=round((last[1]/first[1]-1)*100,2),
      hi=round(hi,2),lo=round(lo,2),fromhi=round((last[1]/hi-1)*100,2),div12=round(s12,4),ndiv=len(dv),yld=round(s12/last[1]*100,2),
      divs=[(datetime.date.fromtimestamp(x['date']).isoformat(),x['amount']) for x in dv]))
    time.sleep(0.3)
json.dump(out,open('data.json','w'),ensure_ascii=False,indent=1)
for o in sorted(out,key=lambda x:x['ret']): print(o['t'],o['ret'],o['fromhi'],o['yld'],o['ndiv'],o['p1'],o['name'])
