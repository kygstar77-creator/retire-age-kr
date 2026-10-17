import json,datetime as dt,sys,math
sys.stdout.reconfigure(encoding='utf-8')
def load(t):
    return [(dt.datetime.fromtimestamp(a,dt.timezone(dt.timedelta(hours=9))).date(),b) for a,b in json.load(open(f'raw/{t}.json')) if b]
def run(t,s,e=None):
    d=[x for x in load(t) if x[0]>=dt.date.fromisoformat(s) and (e is None or x[0]<=dt.date.fromisoformat(e))]
    p=1;l=1;worst=0;mn=1;
    for (_,a),(dd,b) in zip(d,d[1:]):
        r=b/a-1; p*=1+r; l*=1+2*r; worst=min(worst,r)
    return d[0][0],d[-1][0],len(d)-1,(p-1)*100,(l-1)*100,worst*100
for t in ['000660.KS','005930.KS']:
    for s,e in [('2026-05-27',None),('2026-01-02',None),('2025-10-17',None),('2026-07-16',None),('2026-08-14',None)]:
        print(t,run(t,s,e))
# simple hypotheticals
print('5% up/down x10d', (1.05*.95)**5, (1.1*.9)**5)
print('30up30down', 1.3*.7, 1.6*.4)
