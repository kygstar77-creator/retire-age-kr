import sys,json,datetime as dt
sys.path.insert(0,'work');import apis
R='work/research/usrate1104/raw/'
o=json.load(open(R+'rates_1103.json',encoding='utf-8'))
kd=apis.ecos(cycle='D',start='19990506',end='20261103',n=100000)
json.dump(kd,open(R+'ecos_daily_1103.json','w',encoding='utf-8'),ensure_ascii=False)
D=lambda s:dt.date.fromisoformat(s)
us={}
for d,v in o['DFEDTAR']: us[D(d)]=float(v)
for d,v in o['DFEDTARU']: us[D(d)]=float(v)
kr={dt.date(int(t[:4]),int(t[4:6]),int(t[6:])):float(v) for t,v,_ in kd}
days=sorted(set(us)&set(kr))
print('기간',days[0],days[-1],len(days))
gap=[(d,us[d]-kr[d]) for d in days]
def changes(m):
  ks=sorted(m);out=[]
  for a,b in zip(ks,ks[1:]):
    if m[a]!=m[b]: out.append((b,m[a],m[b]))
  return out
print('미국 최근 변경',changes(us)[-6:])
print('한국 최근 변경',changes(kr)[-6:])
cur=gap[-1];print('지금',cur)
# 미국이 더 높은(역전) 구간
runs=[];st=None
for d,g in gap:
  if g>0 and st is None: st=d
  if g<=0 and st is not None: runs.append((st,prev));st=None
  prev=d
if st: runs.append((st,prev))
for a,b in runs: print('역전',a,b,(b-a).days,'최대',max(g for d,g in gap if a<=d<=b))
n=len(gap); ge=sum(1 for d,g in gap if g>=cur[1]); print('지금 차이 이상 날 비율',ge,n,round(ge/n*100,1))
mx=max(gap,key=lambda x:x[1]);print('최대차',mx)
# 1억 예금 단순 이자 차이(연, 세전) — 기준금리 차만큼
print('1억×1%p=',1e8*cur[1]/100)
# 추가: 하단 기준·7월부터 세기·11/4 기준 일수
lo={}
for d,v in apis.fred('DFEDTARL',n=100000): lo[D(d)]=float(v)
print('하단 지금',lo[max(lo)],'차',lo[max(lo)]-kr[days[-1]])
print('2022-09-22→2026-11-04',(dt.date(2026,11,4)-dt.date(2022,9,22)).days)
print('2022-07-28→2026-11-04',(dt.date(2026,11,4)-dt.date(2022,7,28)).days)
eq=[d for d,g in gap if dt.date(2022,8,24)<d<dt.date(2022,9,22)];print('같은 날',eq[0],eq[-1],len(eq),set(round(g,2) for d,g in gap if d in eq))
print('2%p 이상 기간',[d for d,g in gap if g>=2][0],[d for d,g in gap if g>=2][-1])
print('2022-09-22→2026-11-03',(dt.date(2026,11,3)-dt.date(2022,9,22)).days)
