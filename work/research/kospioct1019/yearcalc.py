# kospioct1019 해마다 흔들림 — 야후 ^KS11 월봉(월간 등락)·일봉(한 해 안 고점 대비 최대 하락) 직접 계산
import json,datetime as D,statistics as S,os,sys
sys.stdout.reconfigure(encoding='utf-8'); os.chdir(os.path.dirname(os.path.abspath(__file__)))
def kst(t): return D.datetime.fromtimestamp(t,D.UTC)+D.timedelta(hours=9)
d=json.load(open('raw/ks11_1mo.json'))['chart']['result'][0]; q=d['indicators']['quote'][0]; mon=[]
for i,t in enumerate(d['timestamp']):
    if q['close'][i] is None: continue
    k=(kst(t).year,kst(t).month)
    if mon and mon[-1][0]==k: mon[-1]=(k,q['close'][i]); continue
    mon.append((k,q['close'][i]))
# 10월은 16일 종가로 고정
mon=[(k,c) if k!=(2026,10) else (k,5668.0498046875) for k,c in mon]
rets={}
for i in range(1,len(mon)): rets[mon[i][0]]=mon[i][1]/mon[i-1][1]-1
dd=json.load(open('raw/ks11_1d_max.json'))['chart']['result'][0]
days=[(kst(t).date(),c) for t,c in zip(dd['timestamp'],dd['indicators']['quote'][0]['close']) if c]
days=[x for x in days if x[0]<=D.date(2026,10,16)]
out=[]
for y in range(1997,2027):
    r=[v for (yy,m),v in rets.items() if yy==y]
    if not r: continue
    ds=[c for dt,c in days if dt.year==y]
    peak=None; mdd=0; 
    for c in ds:
        peak=c if peak is None or c>peak else peak; mdd=min(mdd,c/peak-1)
    out.append(dict(y=y,n=len(r),m15=sum(v<=-0.15 for v in r),m10=sum(v<=-0.10 for v in r),best=round(max(r)*100,1),worst=round(min(r)*100,1),rng=round((max(r)-min(r))*100,1),sd=round(S.pstdev(r)*100,1),mdd=round(mdd*100,1),ndays=len(ds)))
for o in out: print(o)
for key,rev in (('m15',True),('m10',True),('rng',True),('sd',True),('mdd',False)):
    s=sorted(out,key=lambda o:o[key],reverse=rev); rank=[o['y'] for o in s].index(2026)+1
    print(key,'2026 순위',rank,'/',len(out),'top3',[(o['y'],o[key]) for o in s[:4]])
json.dump(out,open('year_out.json','w'),indent=1)
