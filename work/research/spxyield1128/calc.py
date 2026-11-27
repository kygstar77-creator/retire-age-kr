# S&P500(SPY·VOO) 배당수익률 30년 직접 계산. 입력 raw/SPY.json·raw/VOO.json(야후 chart, fetch.py)
import json, sys, datetime as dt
sys.stdout.reconfigure(encoding='utf-8')
def load(t):
    j=json.load(open(f'raw/{t}.json',encoding='utf-8'))['chart']['result'][0]
    ts=j['timestamp']; c=j['indicators']['quote'][0]['close']
    px=[(dt.datetime.utcfromtimestamp(a).date(),b) for a,b in zip(ts,c) if b]
    dv=sorted((dt.datetime.utcfromtimestamp(int(v['date'])).date(),v['amount']) for v in j['events']['dividends'].values())
    return px,dv
def ttm(dv,d):
    lo=d-dt.timedelta(days=365)
    return sum(a for x,a in dv if lo<x<=d)
for T in ['SPY','VOO']:
    px,dv=load(T)
    print(f'== {T} 종가 {px[0][0]}~{px[-1][0]} · 배당 {len(dv)}회 {dv[0][0]}~{dv[-1][0]}')
    print('최근 배당 4회:',[(str(d),round(a,4)) for d,a in dv[-4:]])
    # 월말
    me={}
    for d,c in px: me[(d.year,d.month)]=(d,c)
    rows=[]
    for k in sorted(me):
        d,c=me[k]
        if d < px[0][0]+dt.timedelta(days=366): continue
        rows.append((d,c,ttm(dv,d),ttm(dv,d)/c*100))
    last=(px[-1][0],px[-1][1],ttm(dv,px[-1][0]),ttm(dv,px[-1][0])/px[-1][1]*100)
    if rows[-1][0].month==last[0].month: rows[-1]=last
    y=[r[3] for r in rows]
    cur=last[3]
    lower=sum(1 for v in y if v<cur-1e-9); 
    print(f'지금 {last[0]} 종가 {last[1]:.2f} · 1년 배당 {last[2]:.4f} · 배당수익률 {cur:.2f}%')
    print(f'월말 {len(rows)}개({rows[0][0]}~{rows[-1][0]}) 중 지금보다 낮았던 달 {lower}개 · 지금 이하 비율 {(lower+1)/len(rows)*100:.1f}%')
    mn=min(rows,key=lambda r:r[3]); mx=max(rows,key=lambda r:r[3])
    print(f'가장 낮은 달 {mn[0]} {mn[3]:.2f}% · 가장 높은 달 {mx[0]} {mx[3]:.2f}%')
    s=sorted(rows,key=lambda r:r[3])[:8]; print('낮은 8달:',[(str(r[0]),round(r[3],2)) for r in s])
    # 연말 표
    if T=='SPY':
        print('연말(12월) 배당수익률:')
        for r in rows:
            if r[0].month==12 and r[0].year in (1999,2000,2002,2007,2008,2009,2012,2015,2019,2020,2021,2022,2024,2025): print(f'  {r[0]} 종가 {r[1]:.2f} 1년배당 {r[2]:.3f} {r[3]:.2f}%')
        # 10·20년 전 대비 배당금·주가
        for yrs in (10,20,30):
            dd=last[0]-dt.timedelta(days=round(365.25*yrs))
            old=[r for r in px if r[0]<=dd][-1]
            od=ttm(dv,old[0])
            print(f'{yrs}년 전 {old[0]} 종가 {old[1]:.2f} 1년배당 {od:.3f} 수익률 {od/old[1]*100:.2f}% → 주가 {last[1]/old[1]:.2f}배 · 배당금 {last[2]/od:.2f}배')
        # 25년 평균·중앙
        import statistics as st
        print(f'전체 평균 {st.mean(y):.2f}% 중앙 {st.median(y):.2f}%')
        for a,b in ((1994,1999),(2000,2009),(2010,2019),(2020,2026)):
            v=[r[3] for r in rows if a<=r[0].year<=b]; print(f'  {a}~{b} 평균 {st.mean(v):.2f}% 최저 {min(v):.2f} 최고 {max(v):.2f}')
    if T=='VOO':
        amt=1e8*cur/100
        print(f'1억(원) × {cur:.2f}% = 1년 세전 {amt:,.0f}원 · 미국 15% 뗀 뒤 {amt*0.85:,.0f}원 · 한 분기 약 {amt*0.85/4:,.0f}원')
        need=12e6/0.85/(cur/100)
        print(f'세후 1년 1,200만원(월 100만) 받으려면 {need:,.0f}원')
# 해마다 배당 합(SPY, 달력 연도·배당락일 기준)과 늘어난 %
px,dv=load('SPY')
ys={}
for d,a in dv: ys[d.year]=ys.get(d.year,0)+a
print('== SPY 해마다 배당 합(배당락일 기준)')
prev=None; down=[]
for y in sorted(ys):
    g='' if prev is None else f'{(ys[y]/prev-1)*100:+.1f}%'
    if prev and ys[y]<prev: down.append((y,round((ys[y]/prev-1)*100,1)))
    print(f'  {y} {ys[y]:.4f} {g}')
    prev=ys[y]
print('줄어든 해(1994~2025, 2026은 3회만):',[x for x in down if 1994<=x[0]<=2025])
print('2026년 들어 배당 3회 합',round(ys[2026],4),'· 2025년 같은 3회(3·6·9월) 합',round(sum(a for d,a in dv if d.year==2025 and d.month in (3,6,9)),4))
# 지금보다 낮았던 달이 언제였나
px,dv=load('SPY')
me={}
for d,c in px: me[(d.year,d.month)]=(d,c)
rows=[(d,ttm(dv,d)/c*100) for k,(d,c) in sorted(me.items()) if d>=px[0][0]+dt.timedelta(days=366)]
cur=ttm(dv,px[-1][0])/px[-1][1]*100
lo=[(str(d)[:7],round(y,2)) for d,y in rows if y<cur-1e-9]
print('== 지금(%.2f%%)보다 낮았던 달 %d개:'%(cur,len(lo)),lo)
print('1.2% 밑이었던 달 수:',sum(1 for d,y in rows if y<1.2),'· 그 가운데 2021년 뒤:',sum(1 for d,y in rows if y<1.2 and d.year>=2021))
