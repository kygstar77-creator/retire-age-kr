import json, datetime as D, statistics as S, warnings
warnings.filterwarnings('ignore')
CUT=D.date(2026,11,24)  # 기준일: 마지막 미국 종가(11/25 장중 값 뺌)
def load(t):
    r=json.load(open(f'raw/{t}.json'))['chart']['result'][0]
    ts=[D.datetime.utcfromtimestamp(x).date() for x in r['timestamp']]
    q=r['indicators']['quote'][0]['close']; ac=r['indicators'].get('adjclose',[{}])[0].get('adjclose',q)
    dv=sorted((D.datetime.utcfromtimestamp(int(k)).date(),v['amount']) for k,v in r.get('events',{}).get('dividends',{}).items())
    n=sum(1 for a in ts if a<=CUT); return ts[:n],q[:n],ac[:n],[x for x in dv if x[0]<=CUT]
ts,c,ac,dv=load('JEPI'); vt,vc,_,_=load('VIX')
px=dict(zip(ts,c)); vix=dict((a,b) for a,b in zip(vt,vc) if b)
print('JEPI last',ts[-1],round(c[-1],2),'first',ts[0],round(c[0],2), 'n div',len(dv), 'first div',dv[0])
# monthly VIX avg
mv={}
for a,b in vix.items(): mv.setdefault((a.year,a.month),[]).append(b)
mv={k:S.mean(v) for k,v in mv.items()}
rows=[]
for a,v in dv:
    # price on ex-date (close previous trading day)
    prev=max(d for d in ts if d<a); p=px[prev]
    # VIX avg of the month before ex-date (option premium collected during prior month)
    pm=(a.year,a.month-1) if a.month>1 else (a.year-1,12)
    rows.append((a,v,p,v*12/p*100,mv.get(pm),mv.get((a.year,a.month))))
for r in rows: print(r[0],f'{r[1]:.4f}',f'{r[2]:.2f}',f'ann {r[3]:.2f}%',f'vixprev {r[4]:.1f}' if r[4] else '')
# annual sums
ann={}
for a,v in dv: ann[a.year]=ann.get(a.year,0)+v
print('annual',{k:round(v,3) for k,v in ann.items()})
# yearly avg VIX
yv={}
for a,b in vix.items(): yv.setdefault(a.year,[]).append(b)
print('VIX year avg',{k:round(S.mean(v),1) for k,v in yv.items()})
# yearly distribution yield: annual sum / avg price that year
yp={}
for a,b in zip(ts,c):
    if b: yp.setdefault(a.year,[]).append(b)
print('yield on avg price',{k:round(ann[k]/S.mean(yp[k])*100,2) for k in ann if k in yp})
# correlation
xs=[r[4] for r in rows if r[4]]; ys=[r[3] for r in rows if r[4]]
mx,my=S.mean(xs),S.mean(ys); cov=sum((a-mx)*(b-my) for a,b in zip(xs,ys)); 
print('corr vixprev vs annualized',round(cov/(sum((a-mx)**2 for a in xs)*sum((b-my)**2 for b in ys))**.5,2), 'n',len(xs))
# group by vix level
lo=[r[3] for r in rows if r[4] and r[4]<15]; mid=[r[3] for r in rows if r[4] and 15<=r[4]<20]; hi=[r[3] for r in rows if r[4] and r[4]>=20]
print('VIX<15',len(lo),round(S.median(lo),2) if lo else None,'15-20',len(mid),round(S.median(mid),2) if mid else None,'>=20',len(hi),round(S.median(hi),2) if hi else None)
# top/bottom months
s=sorted(rows,key=lambda r:r[3]); print('lowest',[(str(r[0]),round(r[1],3),round(r[3],2),round(r[4] or 0,1)) for r in s[:4]]); print('highest',[(str(r[0]),round(r[1],3),round(r[3],2),round(r[4] or 0,1)) for r in s[-4:]])
# ttm
last=ts[-1]; ttm=sum(v for a,v in dv if a>last-D.timedelta(days=365)); print('ttm',round(ttm,4),'yield',round(ttm/c[-1]*100,2))
# total return since first and 1y, vs SPY
st,sc,sac,_=load('SPY')
def tr(ts,ac,d0):
    i=next(i for i,a in enumerate(ts) if a>=d0); return (ac[-1]/ac[i]-1)*100, ts[i]
for d0 in [D.date(2020,5,21),D.date(2022,1,3),D.date(2025,11,24)]:
    print('TR from',d0,'JEPI',[round(x,1) if isinstance(x,float) else str(x) for x in tr(ts,ac,d0)],'SPY',[round(x,1) if isinstance(x,float) else str(x) for x in tr(st,sac,d0)])
# 2022 price return
def pr(ts,c,a,b):
    i=next(i for i,x in enumerate(ts) if x>=a); j=max(i for i,x in enumerate(ts) if x<=b); return round((c[j]/c[i]-1)*100,1)
print('2022 price JEPI',pr(ts,c,D.date(2022,1,1),D.date(2022,12,31)),'SPY',pr(st,sc,D.date(2022,1,1),D.date(2022,12,31)))
print('price since start JEPI',round((c[-1]/c[0]-1)*100,1))
print('last VIX',vt[-1],vc[-1],'Nov26 avg',round(mv.get((2026,11),0),1),'Oct',round(mv.get((2026,10),0),1))

print('VIX last5',[(str(a),round(b,2)) for a,b in list(zip(vt,vc))[-5:]])
print('VIX >=20 months since 2020-06:',sum(1 for k,v in mv.items() if v>=20 and k>=(2020,6)))
# same-month JEPQ? skip
# monthly div per share by VIX group (amount, not rate)
print('amt median <15',round(S.median([r[1] for r in rows if r[4] and r[4]<15]),3),'>=20',round(S.median([r[1] for r in rows if r[4] and r[4]>=20]),3))
# 1만 달러 2020-05-21 start: 받은 분배금 and value (no reinvest)
sh=10000/c[0]; print('10k shares',round(sh,1),'divs',round(sh*sum(v for a,v in dv),0),'value',round(sh*c[-1],0))
med=S.median([r[3] for r in rows])
hi_rows=[r for r in rows if r[4] and r[4]>=20]
print('overall median ann',round(med,2),'>=20 below overall median',[(str(r[0]),round(r[3],2),round(r[4],1)) for r in hi_rows if r[3]<med])
lo_rows=[r for r in rows if r[4] and r[4]<15]
print('<15 list',[(str(r[0]),round(r[1],3),round(r[3],2),round(r[4],1)) for r in lo_rows])
xs=[r[5] for r in rows if r[5]]; ys=[r[3] for r in rows if r[5]]
mx,my=S.mean(xs),S.mean(ys); cov=sum((a-mx)*(b-my) for a,b in zip(xs,ys))
print('corr same-month',round(cov/(sum((a-mx)**2 for a in xs)*sum((b-my)**2 for b in ys))**.5,2))
print('2026 monthly VIX',{k[1]:round(v,1) for k,v in mv.items() if k[0]==2026})
print('max monthly VIX since 2025-05',max((v,k) for k,v in mv.items() if k>=(2025,5) and k!=(2026,11)))
print('1y div per share by group: <15 amt*12', round(S.median([r[1] for r in lo_rows])*12,2),'>=20',round(S.median([r[1] for r in hi_rows])*12,2))
# per 1억원 at 1400? skip FX
print('Nov 2026 div',[(str(a),v) for a,v in dv if a.year==2026 and a.month>=10])
