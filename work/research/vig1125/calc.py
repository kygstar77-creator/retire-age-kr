import json,datetime as D
def load(t):
    r=json.load(open(f'raw/{t}.json'))['chart']['result'][0]
    ts=[D.datetime.utcfromtimestamp(x).date() for x in r['timestamp']]
    c=r['indicators']['quote'][0]['close']; ac=r['indicators']['adjclose'][0]['adjclose']
    dv=sorted((D.datetime.utcfromtimestamp(int(k)).date(),v['amount']) for k,v in r['events']['dividends'].items())
    return ts,c,ac,dv,r['meta']
for t in ['VIG','VYM','DGRO','SCHD','SPY']:
    ts,c,ac,dv,m=load(t)
    last=ts[-1]; 
    def at(y):  # first close on/after date
        for a,b,x in zip(ts,c,ac):
            if a>=y: return a,b,x
    ann={}
    for a,v in dv: ann[a.year]=ann.get(a.year,0)+v
    s=at(D.date(2015,11,20)); s5=at(D.date(2020,11,20)); s1=at(D.date(2025,11,20))
    ttm=sum(v for a,v in dv if a>last-D.timedelta(days=365))
    print(f"\n{t} last {last} close {c[-1]:.2f} ttm div {ttm:.4f} yield {ttm/c[-1]*100:.2f}% expense? ")
    print(' annual div:', {y:round(v,3) for y,v in ann.items() if 2015<=y<=2026})
    print(f' 2015 div {ann.get(2015,0):.3f} -> 2025 {ann.get(2025,0):.3f}  x{ann.get(2025,0)/ann.get(2015,1):.2f}  CAGR {((ann.get(2025,0)/ann.get(2015,1))**0.1-1)*100:.1f}%')
    for nm,st in [('10y',s),('5y',s5),('1y',s1)]:
        tr=(ac[-1]/st[2]-1)*100; pr=(c[-1]/st[1]-1)*100
        divs=sum(v for a,v in dv if a>st[0])
        print(f' {nm} from {st[0]} price {st[1]:.2f}: price {pr:.1f}% total {tr:.1f}%  divs/share {divs:.2f} ({divs/st[1]*100:.1f}% of cost)  YOC now {ttm/st[1]*100:.2f}%')
    # max drawdown 2022
    pk=0;mdd=0
    for a,x in zip(ts,ac):
        if a.year<2021: continue
        pk=max(pk,x); mdd=min(mdd,x/pk-1)
    print(f' MDD since 2021 {mdd*100:.1f}%')
