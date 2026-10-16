# 떨어지기 전날 종가까지 되찾았나 (1천만원을 전날 종가에 갖고 있었다면)
import json,datetime as D,bisect
r=[(D.date(int(a[:4]),int(a[4:6]),int(a[6:])),float(b)) for a,b,_ in json.load(open("ecos_kospi.json",encoding="utf-8")) if b]
ds=[x[0] for x in r]
def after(i,days):
    j=bisect.bisect_left(ds,r[i][0]+D.timedelta(days=days)); return None if j>=len(r) else r[j]
for k,n in ((7,"1w"),(30,"1m"),(365,"1y")):
    v=[]
    for i in range(1,len(r)):
        if r[i][1]/r[i-1][1]-1<=-0.07:
            a=after(i,k)
            if a: v.append((r[i][0].isoformat(),round(1000*a[1]/r[i-1][1])))
    print(n,"n",len(v),"전날값 되찾음",sum(x[1]>=1000 for x in v),v)
