# 미국배당다우존스 ETF 4종 같은 날 1억 — 야후 종가·분배(raw/*.json, 2026-11-26 받음). 세전·세후(15.4%), 분배금은 받은 날 종가로 다시 삼.
# 끝 날짜: 오늘 16:00 전이면 전 거래일 종가(장중 값 안 씀). k200etf1126/calc.py 틀.
import json, sys, datetime as D
sys.stdout.reconfigure(encoding='utf-8')
N={'402970':'ACE','446720':'SOL','458730':'TIGER','489250':'KODEX'}
now=D.datetime.now(); END=D.date.today() if now.hour*60+now.minute>=16*60 else D.date.today()-D.timedelta(days=1)
if len(sys.argv)>1: END=D.date.fromisoformat(sys.argv[1])
def load(t):
    j=json.load(open(f'raw/{t}.json'))['chart']['result'][0]
    ts=[D.date.fromtimestamp(x) for x in j['timestamp']]; c=j['indicators']['quote'][0]['close']
    px={d:v for d,v in zip(ts,c) if v and d<=END}
    dv={D.date.fromtimestamp(int(k)):v['amount'] for k,v in j.get('events',{}).get('dividends',{}).items() if D.date.fromtimestamp(int(k))<=END}
    return px,dv
data={t:load(t) for t in N}
def run(start,tax=0.0,names=None):
    out=[]
    for t,(px,dv) in data.items():
        if names and N[t] not in names: continue
        ds=sorted(d for d in px if d>=start)
        if not ds or ds[0]-start>D.timedelta(days=7): continue
        sh=1e8/px[ds[0]]; cash=0; sh_nr=sh
        for d in ds[1:]:
            if d in dv: sh+=sh*dv[d]*(1-tax)/px[d]; cash+=sh_nr*dv[d]*(1-tax)
        last=px[ds[-1]]
        n=len([d for d in dv if ds[0]<d<=ds[-1]]); s=sum(v for d,v in dv.items() if ds[0]<d<=ds[-1])
        out.append((N[t],ds[0],ds[-1],sh*last/1e8,(sh_nr*last+cash)/1e8,n,s,px[ds[0]],last,cash))
    for r in out: print(f'  {r[0]:6} {r[1]}~{r[2]} 재투자 {r[3]:.4f}억 · 분배 현금 {r[4]:.4f}억(받은 현금 {r[9]/1e4:,.0f}만) · 분배 {r[5]}번 합 {r[6]:.0f}원 · 시작가 {r[7]:.0f} 끝 {r[8]:.0f}')
    v=[r[3] for r in out]; print(f'  차이(재투자) {(max(v)-min(v))*1e4:.0f}만원')
    return out
if __name__=='__main__':
    print('END',END)
    for t,(px,dv) in data.items(): print(N[t],'첫 종가일',min(px),'분배 첫',min(dv) if dv else None)
    for s in [D.date(2021,10,21),D.date(2022,11,15),D.date(2023,6,20),D.date(2024,8,13),D.date(2025,11,25),D.date(2026,1,2)]:
        print('# 세전',s); run(s)
    print('# 세후 15.4% 2024-08-13'); run(D.date(2024,8,13),tax=0.154)
    print('# 해마다(재투자, 전년 마지막 거래일 대비)')
    for y in range(2022,2027):
        row=[]
        for t,(px,dv) in data.items():
            pr=[d for d in px if d<D.date(y,1,1)]
            if not pr: continue
            prev=max(pr); ds=sorted(d for d in px if prev<=d<=D.date(y,12,31))
            sh=1.0/px[prev]
            for d in ds[1:]:
                if d in dv: sh+=sh*dv[d]/px[d]
            row.append((N[t],sh*px[ds[-1]]-1))
        print(y,' · '.join(f'{n} {r*100:.2f}%' for n,r in row), f'| 폭 {(max(r for _,r in row)-min(r for _,r in row))*100:.2f}%p')
    for t,(px,dv) in data.items():
        last=max(px); ttm=sum(v for d,v in dv.items() if d>last-D.timedelta(days=365))
        print(N[t],'끝',last,px[last],'1년 분배',ttm,f'{ttm/px[last]*100:.2f}%','최근',[(str(d),v) for d,v in sorted(dv.items())[-4:]])
