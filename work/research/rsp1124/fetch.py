# RSP·SPY 일별 종가(수정)·분배 events 받기 — 야후 chart API
import json, urllib.request, sys
for t in ["RSP","SPY","488500.KS","360750.KS"]:
    u=f"https://query1.finance.yahoo.com/v8/finance/chart/{t}?period1=1041379200&period2=1830000000&interval=1d&events=div%2Csplit&includeAdjustedClose=true"
    r=urllib.request.Request(u,headers={"User-Agent":"Mozilla/5.0"})
    d=json.load(urllib.request.urlopen(r,timeout=30))
    json.dump(d,open(f"raw/{t}.json","w"),ensure_ascii=False)
    res=d["chart"]["result"][0]; ts=res["timestamp"]
    print(t,len(ts),res["meta"].get("firstTradeDate"),res["meta"]["regularMarketPrice"])
