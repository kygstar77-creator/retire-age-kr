import requests, json, sys, time
sys.stdout.reconfigure(encoding='utf-8')
H={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/129.0 Safari/537.36"}
out={}
for t in ["360750.KS","379800.KS","^GSPC","KRW=X"]:
    u=f"https://query1.finance.yahoo.com/v8/finance/chart/{t}?range=5y&interval=1d&events=div"
    d=requests.get(u,headers=H,timeout=30).json()
    json.dump(d,open(f"raw/{t}.json","w"),ensure_ascii=False)
    r=d["chart"]["result"][0]; ts=r["timestamp"]; c=r["indicators"]["quote"][0]["close"]
    import datetime
    pts=[(datetime.datetime.fromtimestamp(a).strftime("%Y-%m-%d"),b) for a,b in zip(ts,c) if b]
    print(t,"last",pts[-1],"n",len(pts),"first",pts[0])
    # 1y ago
    last=pts[-1][0]; y=str(int(last[:4])-1)+last[4:]
    ago=[p for p in pts if p[0]<=y][-1]; print("  1y",ago, "chg %.2f%%"%((pts[-1][1]/ago[1]-1)*100))
    yr=[p for p in pts if p[0]>y]; print("  52w hi",max(yr,key=lambda p:p[1]),"lo",min(yr,key=lambda p:p[1]))
    dv=r.get("events",{}).get("dividends",{})
    for k,v in sorted(dv.items(),key=lambda kv:int(kv[0])):
        print("  div",datetime.datetime.fromtimestamp(int(k)).strftime("%Y-%m-%d"),v["amount"])
