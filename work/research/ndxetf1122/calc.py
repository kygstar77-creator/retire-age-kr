# 국내 나스닥100 ETF 4종 같은 날 1억 — 야후 종가·분배금(raw/*.json, 2026-11-21 받음). 세전, 분배금은 받은 날 종가로 다시 삼.
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
def run(start,end=None):
    out=[]
    for t,(px,dv) in data.items():
        ds=sorted(d for d in px if d>=start and (end is None or d<=end))
        if not ds or ds[0]-start>D.timedelta(days=7): continue
        sh=1e8/px[ds[0]]; cash=0; sh_nr=sh
        for d in ds[1:]:
            if d in dv: sh+=sh*dv[d]/px[d]; cash+=sh_nr*dv[d]
        last=px[ds[-1]]
        out.append((N[t],ds[0],ds[-1],sh*last/1e8,(sh_nr*last+cash)/1e8,len([d for d in dv if ds[0]<d<=ds[-1]]),sum(v for d,v in dv.items() if ds[0]<d<=ds[-1])))
    for r in out: print(f'  {r[0]:5} {r[1]}~{r[2]} 재투자 {r[3]:.4f}억 · 분배 따로 {r[4]:.4f}억 · 분배 {r[5]}번 {r[6]:.0f}원')
for s in [D.date(2021,4,9),D.date(2023,1,2),D.date(2025,11,20)]:
    print('#',s); run(s)
for t,(px,dv) in data.items():
    print(N[t],'분배', [(str(d),v) for d,v in sorted(dv.items())][-6:])
