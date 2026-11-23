import json,datetime as D
def load(t):
    r=json.load(open(f'raw/{t}.json'))['chart']['result'][0]
    ts=[D.datetime.utcfromtimestamp(x).date() for x in r['timestamp']]
    c=r['indicators']['quote'][0]['close']; ac=r['indicators']['adjclose'][0]['adjclose']
    dv=sorted((D.datetime.utcfromtimestamp(int(k)).date(),v['amount']) for k,v in r['events']['dividends'].items())
    return ts,c,ac,dv
ts,c,ac,dv=load('DGRO')
print('DGRO last',ts[-1],c[-1])
by={}
for a,v in dv: by.setdefault(a.year,[]).append((a,v))
for y in range(2015,2027):
    L=by.get(y,[]); tot=sum(v for a,v in L)
    dec=[v for a,v in L if a.month==12]
    big=max(L,key=lambda x:x[1]) if L else None
    print(y, ' '.join(f"{a.month:02d}/{a.day:02d}:{v:.3f}" for a,v in L), f"sum {tot:.3f}", f"dec share {dec[0]/tot*100:.0f}%" if dec else '', 'biggest', big[0].month if big else '')
for t in ['DGRO','SCHD','VIG','SPY']:
    ts,c,ac,dv=load(t); last=ts[-1]
    ann={}
    for a,v in dv: ann[a.year]=ann.get(a.year,0)+v
    ttm=sum(v for a,v in dv if a>last-D.timedelta(days=365))
    def at(y):
        for a,b,x in zip(ts,c,ac):
            if a>=y: return a,b,x
    s=at(D.date(2015,11,20))
    # cuts: years where annual < previous
    cuts=[y for y in range(2016,2026) if ann.get(y,0)<ann.get(y-1,0)]
    print(f"\n{t} {last} close {c[-1]:.2f} ttm {ttm:.4f} yield {ttm/c[-1]*100:.2f}%  2015 {ann[2015]:.3f} 2025 {ann[2025]:.3f} x{ann[2025]/ann[2015]:.2f} cagr {((ann[2025]/ann[2015])**0.1-1)*100:.1f}% cut-years {cuts}")
    print(f"  10y from {s[0]} {s[1]:.2f}: total {(ac[-1]/s[2]-1)*100:.1f}% price {(c[-1]/s[1]-1)*100:.1f}% YOC {ttm/s[1]*100:.2f}% 10k->{10000*ac[-1]/s[2]:,.0f}")
    pk=0;mdd=0
    for a,x in zip(ts,ac):
        if a.year<2021: continue
        pk=max(pk,x); mdd=min(mdd,x/pk-1)
    print(f'  MDD since 2021 {mdd*100:.1f}%')

print('\n--- 2017->2025 annual, 1y total')
for t in ['DGRO','SCHD','VIG']:
    ts,c,ac,dv=load(t); ann={}
    for a,v in dv: ann[a.year]=ann.get(a.year,0)+v
    s1=[(a,x) for a,x in zip(ts,ac) if a>=D.date(2025,11,20)][0]
    print(t, f"2017 {ann[2017]:.3f} 2025 {ann[2025]:.3f} x{ann[2025]/ann[2017]:.2f} cagr {((ann[2025]/ann[2017])**(1/8)-1)*100:.1f}%  1y total {(ac[-1]/s1[1]-1)*100:.1f}% counts", sum(1 for a,v in dv if a.year==2017), sum(1 for a,v in dv if a.year==2025))
