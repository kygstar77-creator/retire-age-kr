import json, datetime, sys
sys.stdout.reconfigure(encoding='utf-8')
def load(fn):
    d=json.load(open(fn))['chart']['result'][0]
    ts=d['timestamp']; q=d['indicators']['quote'][0]
    rows=[]
    for t,c,h,l in zip(ts,q['close'],q['high'],q['low']):
        if c is None: continue
        dt=(datetime.datetime.fromtimestamp(t,datetime.UTC)+datetime.timedelta(hours=9)).date()
        rows.append((dt,c,h,l))
    return rows
for fn in ['y_SDI.json','y_KOSPI.json']:
    r=load(fn); last=r[-1]
    for yrs in (1,3,5,10):
        since=last[0].replace(year=last[0].year-yrs)
        w=[x for x in r if x[0]>since]
        hi=max(w,key=lambda x:x[1]); lo=min(w,key=lambda x:x[1])
        hh=max(w,key=lambda x:x[2]); ll=min(w,key=lambda x:x[3])
        print(fn,yrs,'close hi',hi[0],hi[1],'lo',lo[0],lo[1],'| intraday hi',hh[0],hh[2],'lo',ll[0],ll[3],'| start',w[0][0],w[0][1])
    # monthly sample last year
    for x in r[-260::20]: print(' ',x[0],round(x[1]))
