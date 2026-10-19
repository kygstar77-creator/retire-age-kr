import json,datetime
T={'114260.KS':'KODEX 국고채3년','148070.KS':'국고채10년(148070)','114820.KS':'TIGER 국채3년','157450.KS':'TIGER 단기통안채(157450)'}
def load(t):
    d=json.load(open(f'raw/{t}.json',encoding='utf-8'))['chart']['result'][0]
    ts=[datetime.date.fromtimestamp(x) for x in d['timestamp']];c=d['indicators']['quote'][0]['close']
    dv={datetime.date.fromtimestamp(v['date']):v['amount'] for v in (d.get('events',{}).get('dividends',{}) or {}).values()}
    return ts,c,dv
for t,n in T.items():
    ts,c,dv=load(t)
    print('==',t,n,ts[0],ts[-1],c[-1])
    for lab,start in [('1y',datetime.date(2025,10,17)),('2y',datetime.date(2024,10,17)),('3y',datetime.date(2023,10,19))]:
        i=next(k for k,x in enumerate(ts) if x>=start)
        p0=c[i];p1=c[-1]
        d=sum(a for k,a in dv.items() if k>ts[i])
        # reinvest-free simple
        print(lab,ts[i],p0,p1,'price%.2f%%'%((p1/p0-1)*100),'div',round(d),'divpct%.2f%%'%(d/p0*100),'total%.2f%%'%(((p1+d)/p0-1)*100))
    # max drawdown last 3y
    pk=0;mdd=0;pd=None
    for x,y in zip(ts,c):
        if y is None: continue
        if y>pk: pk=y;pkd=x
        dd=y/pk-1
        if dd<mdd: mdd=dd;mdate=(pkd,x)
    print('mdd%.2f%%'%(mdd*100),mdate)
    print('divs',[(str(k),v) for k,v in sorted(dv.items())][-6:])
