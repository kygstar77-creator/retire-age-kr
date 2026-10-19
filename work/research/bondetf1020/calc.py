import json,datetime,sys
RAW=sys.argv[1] if len(sys.argv)>1 else 'raw'
T={'114260.KS':'KODEX 국고채3년','148070.KS':'국고채10년(148070)','114820.KS':'TIGER 국채3년','157450.KS':'TIGER 단기통안채(157450)'}
def load(t):
    d=json.load(open(f'{RAW}/{t}.json',encoding='utf-8'))['chart']['result'][0]
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
        if lab=='1y': print('  1억 넣었다면(분배금 재투자 안 함, 세전): %s원'%format(round(1e8*(p1+d)/p0),','))
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

# 듀레이션 x 금리 변화 (운용사 공시 듀레이션, ECOS 817Y002 1년 금리 변화)
for n,dur,dy in [('KIWOOM 국고채10년',7.694,4.205-2.885),('TIGER 국채3년',2.79,3.877-2.555),('TIGER 단기통안채',0.41,3.698-2.304)]:
    print(n,'듀레이션',dur,'금리변화 %+.3f%%p'%dy,'대략 값 변화 %.1f%%'%(-dur*dy))
