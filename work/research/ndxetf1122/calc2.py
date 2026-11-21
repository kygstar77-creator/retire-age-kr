# 대조·세후·연도별 — calc.py 같은 원자료(raw/*.json, 야후 11/21 받음)
import json, sys, datetime as D
sys.stdout.reconfigure(encoding='utf-8')
N={'133690':'TIGER','379810':'KODEX','367380':'ACE','368590':'RISE'}
def load(t):
    j=json.load(open(f'raw/{t}.json'))['chart']['result'][0]
    ts=[D.date.fromtimestamp(x) for x in j['timestamp']]; c=j['indicators']['quote'][0]['close']
    px={d:v for d,v in zip(ts,c) if v}
    dv={D.date.fromtimestamp(int(k)):v['amount'] for k,v in j.get('events',{}).get('dividends',{}).items()}
    return px,dv
data={t:load(t) for t in N}
def tr(t,s,e,tax=0.0):
    px,dv=data[t]; ds=sorted(d for d in px if s<=d<=e)
    sh=1/px[ds[0]]
    for d in ds[1:]:
        if d in dv: sh+=sh*dv[d]*(1-tax)/px[d]
    return sh*px[ds[-1]], ds[0], ds[-1]
E=D.date(2026,11,19)
for lab,s,yrs in [('Y1',D.date(2025,11,19),1),('Y3',D.date(2023,11,20),3),('Y5',D.date(2021,11,19),5)]:
    print(lab, {N[t]:(round((tr(t,s,E)[0]**(1/yrs)-1)*100,2)) for t in N})
S=D.date(2021,4,9); E2=D.date(2026,11,20)
for tax in [0,0.154]:
    print('2021-04-09~11-20 tax',tax, {N[t]:round(tr(t,S,E2,tax)[0],4) for t in N})
for y in range(2021,2027):
    s=D.date(y,1,1) if y>2021 else S; e=D.date(y,12,31) if y<2026 else E2
    # 연도 수익: 전년 마지막 종가 기준
    r={}
    for t in N:
        px,dv=data[t]; prev=[d for d in px if d<s]
        s0=max(prev) if y>2021 else S
        v,_,_=tr(t,s0,e); r[N[t]]=round((v-1)*100,1)
    print(y,r)
for t in N:
    px,_=data[t]; print(N[t], 'first',min(px), [ (str(d),px[d]) for d in sorted(px) if d in (D.date(2021,4,9),D.date(2025,11,19),D.date(2025,11,20),D.date(2026,11,19),D.date(2026,11,20))])
