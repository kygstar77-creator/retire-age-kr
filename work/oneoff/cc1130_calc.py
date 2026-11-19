import urllib.request, json, datetime
def get(t):
    u=f'https://query1.finance.yahoo.com/v8/finance/chart/{t}?range=5y&interval=1d&events=div'
    r=json.load(urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'Mozilla/5.0'}),timeout=30))['chart']['result'][0]
    px={datetime.date.fromtimestamp(a):b for a,b in zip(r['timestamp'],r['indicators']['quote'][0]['close']) if b}
    dv={datetime.date.fromtimestamp(int(k)):v['amount'] for k,v in r.get('events',{}).get('dividends',{}).items()}
    return px,dv
def run(t,start,tax=0.154,reinv=False):
    px,dv=get(t); days=sorted(d for d in px if d>=start); p0=px[days[0]]; sh=1e8/p0; cash=0
    for d in sorted(dv):
        if d<days[0]: continue
        net=dv[d]*sh*(1-tax)
        if reinv:
            nd=[x for x in days if x>=d]; sh+=net/px[nd[0]]
        else: cash+=net
    v=sh*px[days[-1]]
    return days[0],days[-1],round(p0),round(px[days[-1]]),round(cash/1e4),round(v/1e4),round((v+cash)/1e4)
for t in ['441640.KS','458730.KS']:
  for s in [datetime.date(2022,9,27),datetime.date(2023,6,20),datetime.date(2025,11,19)]:
    for r in (False,True):
      try: print(t,s,'재투자' if r else '받아씀',run(t,s,reinv=r))
      except Exception as e: print(t,s,e)
