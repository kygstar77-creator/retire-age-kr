# QQQ·QLD·TQQQ 일별 종가(수정)·분배·분할 events 받기 — 야후 chart API (lev1125, write-b 11/23)
import json, urllib.request, urllib.parse, datetime
for t in ["QQQ","QLD","TQQQ","^NDX"]:
    u=f"https://query1.finance.yahoo.com/v8/finance/chart/{urllib.parse.quote(t)}?period1=946684800&period2=1830000000&interval=1d&events=div%2Csplit&includeAdjustedClose=true"
    r=urllib.request.Request(u,headers={"User-Agent":"Mozilla/5.0"})
    d=json.load(urllib.request.urlopen(r,timeout=30))
    json.dump(d,open(f"raw/{t.replace('^','')}.json","w"),ensure_ascii=False)
    res=d["chart"]["result"][0]; ts=res["timestamp"]
    print(t,len(ts),datetime.datetime.utcfromtimestamp(ts[0]).date(),datetime.datetime.utcfromtimestamp(ts[-1]).date(),res["meta"]["regularMarketPrice"])
