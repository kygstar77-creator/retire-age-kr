# 다우지수(^DJI)·DIA 보유 종목(SSGA)·SPY 보유 종목 받기
import json, urllib.request
H={"User-Agent":"Mozilla/5.0"}
def get(u,fn):
    d=urllib.request.urlopen(urllib.request.Request(u,headers=H),timeout=40).read()
    open(fn,"wb").write(d); print(fn,len(d))
get("https://www.ssga.com/us/en/intermediary/library-content/products/fund-data/etfs/us/holdings-daily-us-en-dia.xlsx","raw/dia_holdings.xlsx")
get("https://www.ssga.com/us/en/intermediary/library-content/products/fund-data/etfs/us/holdings-daily-us-en-spy.xlsx","raw/spy_holdings.xlsx")
for t in ["^DJI","DIA","^GSPC"]:
    u=f"https://query1.finance.yahoo.com/v8/finance/chart/{t}?range=2y&interval=1d"
    get(u,f"raw/{t.replace('^','')}.json")
