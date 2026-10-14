import json, urllib.request, sys
sys.stdout.reconfigure(encoding='utf-8')
UA={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/126'}
for sym,fn in [('006400.KS','y_SDI.json'),('%5EKS11','y_KOSPI.json')]:
    u=f'https://query1.finance.yahoo.com/v8/finance/chart/{sym}?range=10y&interval=1d&events=div'
    b=urllib.request.urlopen(urllib.request.Request(u,headers=UA),timeout=30).read()
    open(fn,'wb').write(b); print(fn,len(b))
