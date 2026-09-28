# 미국 시총 상위 100 — 1년 최고 종가 대비 지금 몇 % 아래인지, 1년 배당 합계
import requests, json, time, statistics, sys
sys.stdout.reconfigure(encoding='utf-8')
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
        j=requests.get(f"https://query1.finance.yahoo.com/v8/finance/chart/{s}?range=1y&interval=1d&events=div",headers=H,timeout=30).json()
        res=j["chart"]["result"][0]; ts=res["timestamp"]; c=res["indicators"]["quote"][0]["close"]
        pts=[(time.strftime("%Y-%m-%d",time.gmtime(t)),v) for t,v in zip(ts,c) if v]
        pts=[p for p in pts if p[0]<"2026-09-28"]  # 9/28(월) 장중 값 제외, 9/25(금) 종가까지
        hi=max(pts,key=lambda p:p[1]); last=pts[-1]
        divs={k:v for k,v in res.get("events",{}).get("dividends",{}).items() if time.strftime("%Y-%m-%d",time.gmtime(v["date"]))<"2026-09-28"}
        dsum=sum(d["amount"] for d in divs.values())
        out.append(dict(sym=s,name=x["name"],sector=x.get("sector"),cap=cap(x),hi=hi,last=last,dd=round((last[1]/hi[1]-1)*100,2),div12=round(dsum,4),yld=round(dsum/last[1]*100,2),first=pts[0][0]))
    except Exception as e: print("fail",s,e)
    time.sleep(0.15)
json.dump(out,open("hi.json","w",encoding="utf-8"),ensure_ascii=False,indent=1)
print("조회",time.strftime("%Y-%m-%d %H:%M"),"상위100 1위",top[0]["symbol"],round(cap(top[0])/1e9),"100위",top[-1]["symbol"],round(cap(top[-1])/1e9))
dd=[o["dd"] for o in out]
print("받음",len(out),"중앙값",statistics.median(dd),"-20%이하",sum(d<=-20 for d in dd),"-30%이하",sum(d<=-30 for d in dd),"고점 0%",sum(d==0 for d in dd))
for o in sorted(out,key=lambda o:o["dd"])[:15]: print(o["sym"],o["name"][:38],o["dd"],o["hi"],o["last"],round(o["cap"]/1e9),o["sector"],"div",o["div12"],o["yld"])
