import json,datetime as D,bisect
r=[(D.date(int(a[:4]),int(a[4:6]),int(a[6:])),float(b)) for a,b,_ in json.load(open("ecos_kospi.json",encoding="utf-8")) if b]
ds=[x[0] for x in r]
def after(i,days):
    t=r[i][0]+D.timedelta(days=days); j=bisect.bisect_left(ds,t)
    return None if j>=len(r) else r[j]
out=[]
for i in range(1,len(r)):
    ch=r[i][1]/r[i-1][1]-1
    if ch<=-0.07:
        row=[r[i][0].isoformat(),round(ch*100,2),r[i][1]]
        for k in (7,30,365):
            a=after(i,k); row.append(None if a is None else (a[0].isoformat(),a[1],round((a[1]/r[i][1]-1)*100,1),round(1000*a[1]/r[i][1])))
        out.append(row)
for o in out: print(o)
for k,n in ((3,"1w"),(4,"1m"),(5,"1y")):
    v=[o[k] for o in out if o[k]]; print(n,"n",len(v),"up",sum(x[2]>0 for x in v),"min",min(x[2] for x in v),"max",max(x[2] for x in v))
json.dump(out,open("calc3.json","w"),ensure_ascii=False)
