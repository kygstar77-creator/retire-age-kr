import json, sys; sys.stdout.reconfigure(encoding='utf-8')
d=json.load(open('raw_20261017.json',encoding='utf-8')); krx,gc,fx=d['KRX'],d['GC'],d['FX']; OZ=31.1034768
def on(s,day):
    ks=[k for k in s if k<=day]; return s[ks[-1]]
def bf(s,day):
    ks=[k for k in s if k<day]; return s[ks[-1]]
prem={}
for day,k in krx.items():
    if day<'2025-10-02': continue
    prem[day]=k/(bf(gc,day)*on(fx,day)/OZ)-1
mx=max(prem,key=prem.get); mn=min(prem,key=prem.get)
print('days',len(prem),'max',mx,round(prem[mx]*100,2),'min',mn,round(prem[mn]*100,2))
for day in ('2025-10-02','2025-10-15','2026-01-29','2026-09-15','2026-10-06','2026-10-13','2026-10-14','2026-10-15','2026-10-16'):
    print(day, krx.get(day), round(prem[day]*100,2) if day in prem else None)
pos=sum(1 for v in prem.values() if v>0); print('premium>0 days',pos,'of',len(prem))
import statistics; print('median',round(statistics.median(prem.values())*100,2))
# last 30 trading days range
last=sorted(prem)[-30:]; print('last30 range',last[0],round(min(prem[x] for x in last)*100,2),round(max(prem[x] for x in last)*100,2))
# since 2026-07-01 
sub=[x for x in sorted(prem) if x>='2026-07-01']; print('since 7/1', len(sub), round(min(prem[x] for x in sub)*100,2), round(max(prem[x] for x in sub)*100,2))
