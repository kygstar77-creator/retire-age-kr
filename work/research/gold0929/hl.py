import json, urllib.request, datetime, sys
sys.stdout.reconfigure(encoding='utf-8')
UA={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/128.0 Safari/537.36'}
u='https://query1.finance.yahoo.com/v8/finance/chart/GC%3DF?range=1y&interval=1d'
r=json.load(urllib.request.urlopen(urllib.request.Request(u,headers=UA)))['chart']['result'][0]
q=r['indicators']['quote'][0]; off=r['meta']['gmtoffset']
rows=[(datetime.datetime.fromtimestamp(t+off,datetime.UTC).strftime('%Y-%m-%d'),h,l,c) for t,h,l,c in zip(r['timestamp'],q['high'],q['low'],q['close']) if c]
json.dump(rows,open('hl.json','w'),indent=0)
H=max(rows,key=lambda x:x[1]); print('intraday high',H)
after=[x for x in rows if x[0]>=H[0]]; L=min(after,key=lambda x:x[2]); print('lowest low after',L, L[2]/H[1]-1)
print('last',rows[-3:])
for x in rows:
  if '2026-01-26'<=x[0]<='2026-02-06' or '2026-07-10'<=x[0]<='2026-07-20': print(x)
# where would 28% from intraday high be
print('28% level', H[1]*0.72, '28% from close high', 5318.4*0.72)
