# 미국 고배당 ETF 3종 같은 날 1억(달러 기준 비율) — 야후 종가·배당(raw/*.json, 2026-11-27 받음). 세전·세후(미국 원천 15%), 배당은 받은 날 종가로 다시 삼.
# 끝 날짜: 미국 장 마감 뒤 받은 마지막 종가. divdj1127/calc.py 틀.
import json, sys, datetime as D
sys.stdout.reconfigure(encoding='utf-8')
N=['VYM','HDV','SPYD']
def load(t):
    j=json.load(open(f'raw/{t}.json'))['chart']['result'][0]
    ts=[D.datetime.fromtimestamp(x,D.UTC).date() for x in j['timestamp']]; c=j['indicators']['quote'][0]['close']
    px={d:v for d,v in zip(ts,c) if v}
    dv={D.datetime.fromtimestamp(int(k),D.UTC).date():v['amount'] for k,v in j.get('events',{}).get('dividends',{}).items()}
    return px,dv
data={t:load(t) for t in N}
END=min(max(px) for px,_ in data.values())
def run(start,tax=0.0):
    out=[]
    for t in N:
        px,dv=data[t]
        ds=sorted(d for d in px if start<=d<=END)
        sh=1/px[ds[0]]; cash=0; sh0=sh
        for d in ds[1:]:
            if d in dv: sh+=sh*dv[d]*(1-tax)/px[d]; cash+=sh0*dv[d]*(1-tax)
        last=px[ds[-1]]
        # 최대 낙폭(재투자 가치)
        s2=1/px[ds[0]]; peak=0; mdd=0; pk=None; tr=None
        for d in ds:
            if d in dv and d!=ds[0]: s2+=s2*dv[d]*(1-tax)/px[d]
            v=s2*px[d]
            if v>peak: peak=v; pkd=d
            if v/peak-1<mdd: mdd=v/peak-1; pk=pkd; tr=d
        out.append((t,ds[0],ds[-1],sh*last,sh0*last+cash,cash,sh0*last,mdd,pk,tr))
    for r in out: print(f'  {r[0]:5} {r[1]}~{r[2]} 재투자 {r[3]:.4f} · 현금으로 받기 {r[4]:.4f}(받은 배당 {r[5]:.4f}·주가만 {r[6]:.4f}) · 최대낙폭 {r[7]*100:.1f}% ({r[8]}→{r[9]})')
    return out
print('END',END)
for t in N:
    px,dv=data[t]; print(t,'첫 종가',min(px),'배당 첫',min(dv),'수',len(dv))
for s in [D.date(2015,10,22),D.date(2016,11,25),D.date(2021,11,26),D.date(2024,11,26),D.date(2025,11,26),D.date(2026,1,2)]:
    print('# 세전',s); run(s)
print('# 세후 15% 2016-11-25'); run(D.date(2016,11,25),tax=0.15)
print('# 해마다(재투자, 전년 마지막 거래일 대비)')
for y in range(2016,2027):
    row=[]
    for t in N:
        px,dv=data[t]
        prev=max(d for d in px if d<D.date(y,1,1)); ds=sorted(d for d in px if prev<=d<=min(D.date(y,12,31),END))
        sh=1.0/px[prev]
        for d in ds[1:]:
            if d in dv: sh+=sh*dv[d]/px[d]
        row.append((t,sh*px[ds[-1]]-1))
    print(y,' · '.join(f'{n} {r*100:.2f}%' for n,r in row),'| 1등',max(row,key=lambda x:x[1])[0])
print('# 1년 배당률·배당금 변화')
for t in N:
    px,dv=data[t]; last=END
    ttm=sum(v for d,v in dv.items() if last-D.timedelta(days=365)<d<=last)
    y10=sum(v for d,v in dv.items() if D.date(2016,1,1)<=d<=D.date(2016,12,31)); y25=sum(v for d,v in dv.items() if D.date(2025,1,1)<=d<=D.date(2025,12,31))
    print(t,'끝',last,round(px[last],2),'1년 배당',round(ttm,4),f'{ttm/px[last]*100:.2f}%','2016년 합',round(y10,4),'2025년 합',round(y25,4),f'늘어난 배 {y25/y10:.2f}','최근',[(str(d),v) for d,v in sorted(dv.items())[-4:]])
