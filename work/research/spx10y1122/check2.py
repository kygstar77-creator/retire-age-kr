# 2차 대조: 야후 SPY 수정종가(배당 재투자, 보수 뺀 값)로 같은 구간 다시 셈 (2026-11-21)
import urllib.request, json, datetime, sys, bisect
sys.stdout.reconfigure(encoding='utf-8')
u=None
d=open("raw/spy_20261121.json","rb").read()
q=json.loads(d)['chart']['result'][0]
r=[((datetime.datetime(1970,1,1)+datetime.timedelta(seconds=a)).date(),b) for a,b in zip(q['timestamp'],q['indicators']['adjclose'][0]['adjclose']) if b]
ds=[a for a,_ in r]
def at(s): return r[bisect.bisect_left(ds,datetime.date.fromisoformat(s))]
for a,b in [('1999-03-08','2009-03-09'),('2000-08-25','2015-08-25'),('2000-03-23','2020-03-23')]:
    x,y=at(a),at(b); print('SPY',x[0],y[0],round((y[1]/x[1]-1)*100,1))
o=[]
for i,(dd,v) in enumerate(r):
    j=bisect.bisect_left(ds,(dd.replace(day=28) if (dd.month,dd.day)==(2,29) else dd).replace(year=dd.year+10))
    if j>=len(r): break
    o.append(r[j][1]/v-1)
print('SPY 10년 구간',len(o),'손해',sum(x<0 for x in o),round(sum(x<0 for x in o)/len(o)*100,1))
o=[]
for i,(dd,v) in enumerate(r):
    j=bisect.bisect_left(ds,(dd.replace(day=28) if (dd.month,dd.day)==(2,29) else dd).replace(year=dd.year+15))
    if j>=len(r): break
    o.append(r[j][1]/v-1)
print('SPY 15년 구간',len(o),'손해',sum(x<0 for x in o))
tr=json.load(open('raw/gspc_20261121.json'))['chart']['result'][0]
m={(datetime.datetime(1970,1,1)+datetime.timedelta(seconds=a)).date().isoformat():b for a,b in zip(tr['timestamp'],tr['indicators']['quote'][0]['close']) if b}
print('야후 ^GSPC 11/19',m.get('2026-11-19'),'10/6',m.get('2026-10-06'))
