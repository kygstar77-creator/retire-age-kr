import json,datetime
d=json.load(open("ks11.json"))["chart"]["result"][0]
rows=[(datetime.datetime.fromtimestamp(t+9*3600,datetime.UTC).date().isoformat(),x) for t,x in zip(d["timestamp"],d["indicators"]["quote"][0]["close"]) if x]
out=[]
for i in range(1,len(rows)):
    ch=rows[i][1]/rows[i-1][1]-1
    if ch<=-0.07:
        def f(k): return None if i+k>=len(rows) else round((rows[i+k][1]/rows[i][1]-1)*100,2)
        out.append((rows[i][0],round(ch*100,2),round(rows[i][1],2),f(5),f(21),f(250),rows[i+250][0] if i+250<len(rows) else None))
for o in out: print(o)
print(len(out))
