import requests, json, time, statistics
H={"User-Agent":"Mozilla/5.0","Accept":"application/json"}
r=requests.get("https://api.nasdaq.com/api/screener/stocks?tableonly=true&limit=10000&download=true",headers=H,timeout=60).json()
rows=r["data"]["rows"]
def cap(x):
    try: return float(x["marketCap"] or 0)
    except: return 0
rows=[x for x in rows if "^" not in x["symbol"] and "/" not in x["symbol"] and x["symbol"] not in ("GOOG","GOOGM","GOOGN")]
rows.sort(key=cap,reverse=True)
top=rows[:100]
out=[]
for x in top:
    s=x["symbol"]
    try:
        j=requests.get(f"https://query1.finance.yahoo.com/v8/finance/chart/{s}?period1=1782345600&period2=1790553600&interval=1d",headers=H,timeout=30).json()
        res=j["chart"]["result"][0]; ts=res["timestamp"]; c=res["indicators"]["quote"][0]["close"]
        pts=[(time.strftime("%Y-%m-%d",time.gmtime(t)),v) for t,v in zip(ts,c) if v]
        base=[p for p in pts if p[0]<="2026-06-30"][-1]; last=pts[-1]
        out.append(dict(sym=s,name=x["name"],sector=x.get("sector"),cap=cap(x),base=base,last=last,chg=round((last[1]/base[1]-1)*100,2)))
    except Exception as e: print("fail",s,e)
    time.sleep(0.15)
json.dump(out,open("q3.json","w",encoding="utf-8"),ensure_ascii=False,indent=1)
print(len(rows),"종목; 상위100 1위",top[0]["symbol"],cap(top[0]),"100위",top[-1]["symbol"],cap(top[-1]))
print("받음",len(out),"중앙값",statistics.median([o["chg"] for o in out]),"마이너스",sum(o["chg"]<0 for o in out))
for o in sorted(out,key=lambda o:o["chg"])[:12]: print(o["sym"],o["name"][:40],o["chg"],o["base"],o["last"],round(o["cap"]/1e9),o["sector"])
