import json
r=[(a,float(b)) for a,b,_ in json.load(open("ecos_kospi.json",encoding="utf-8")) if b]
out=[]
for i in range(1,len(r)):
    ch=r[i][1]/r[i-1][1]-1
    if ch<=-0.07:
        f=lambda k: None if i+k>=len(r) else round((r[i+k][1]/r[i][1]-1)*100,1)
        # 1천만원 넣었으면 1년 뒤
        y=None if i+250>=len(r) else round(1000*r[i+250][1]/r[i][1])
        out.append((r[i][0],round(ch*100,2),r[i][1],f(5),f(21),f(250),y))
for o in out: print(*o)
print(len(out))
up=[o for o in out if o[5] is not None]
print("1y n",len(up),"up",sum(o[5]>0 for o in up))
m=[o for o in out if o[4] is not None]; print("1m n",len(m),"up",sum(o[4]>0 for o in m))
w=[o for o in out if o[3] is not None]; print("1w n",len(w),"up",sum(o[3]>0 for o in w))
