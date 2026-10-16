import json,urllib.request,datetime
u="https://query1.finance.yahoo.com/v8/finance/chart/%5EKS11?period1=0&period2=9999999999&interval=1d"
r=urllib.request.urlopen(urllib.request.Request(u,headers={"User-Agent":"Mozilla/5.0"}),timeout=30).read()
open("ks11.json","wb").write(r)
d=json.loads(r)["chart"]["result"][0]
ts=d["timestamp"];c=d["indicators"]["quote"][0]["close"]
rows=[(datetime.datetime.utcfromtimestamp(t+9*3600).date().isoformat(),x) for t,x in zip(ts,c) if x]
print(len(rows),rows[0],rows[-5:])
