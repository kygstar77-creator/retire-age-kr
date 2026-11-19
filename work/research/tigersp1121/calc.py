# TIGER 미국S&P500(360750) 매달 50만원 5년 vs 같은 돈 한 번에 — 종가는 야후 일별 원래 종가(네이버 siseJson은 분배금 수정주가라 대조만), 분배금은 야후 events + 2022-07 40원(미래에셋 연간 합 160원에서 채움)
import json, datetime, sys
sys.stdout.reconfigure(encoding='utf-8')
rows=json.loads(open('raw/nv_360750.txt',encoding='utf-8').read().replace("'",'"'))[1:]
px={r[0]:r[4] for r in rows}; days=sorted(px)
y=json.load(open('raw/y_360750.KS.json'))['chart']['result'][0]
ydiv={datetime.date.fromtimestamp(int(k)).strftime('%Y%m%d'):v['amount'] for k,v in y['events']['dividends'].items()}
ydiv['20220728']=40.0
# 야후 종가 대조
yc={datetime.date.fromtimestamp(t).strftime('%Y%m%d'):c for t,c in zip(y['timestamp'],y['indicators']['quote'][0]['close']) if c}
nv=px; px=yc; days=sorted(px)
print('네이버(수정주가)와 같은 마지막 날', [(d,nv.get(d),px[d]) for d in days[-3:]])
END=days[-1]; START='20211201'
months=[]
for d in days:
    if d>=START and (not months or d[:6]!=months[-1][:6]): months.append(d)
months=[m for m in months if m<=END][:60]
print('매수 첫날', months[0], '마지막', months[-1], '횟수', len(months), '마지막 종가일', END, px[END])
SER={}
def run(plan):
    sh=0; cash=0; paid=0; dist=0; worst=(0,None); lossm=0; hist=[]; ser=[]
    buy=dict(plan)
    for d in days:
        if d<START or d>END: continue
        if d in ydiv: dist+=sh*ydiv[d]
        if d in buy:
            cash+=buy[d]; paid+=buy[d]; n=int(cash//px[d]); sh+=n; cash-=n*px[d]
        if d in buy or d==END:
            v=sh*px[d]+cash; r=(v+dist)/paid-1 if paid else 0
            hist.append((d,paid,v,dist,r))
        v=sh*px[d]+cash; r=(v+dist)/paid-1
        if d=='20260702': print(f'  ({plan[0][1]:,}) 고점 2026-07-02 넣은 {paid:,} 평가+분배 {v+dist:,.0f} {r:+.2%}')
        if r<worst[0]: worst=(r,d,paid,v+dist)
        ser.append((d,paid,round(v+dist)))
    SER[plan[0][1]]=ser
    return sh,cash,paid,dist,worst,hist
for name,plan in (('매달 50만원',[(m,500000) for m in months]),('한 번에 3천만원',[(months[0],30000000)])):
    sh,cash,paid,dist,worst,hist=run(plan)
    v=sh*px[END]+cash
    print(f'\n[{name}] 넣은 돈 {paid:,} · 주수 {sh:,} · 남은 현금 {cash:,.0f} · 평가 {v:,.0f} · 분배금 {dist:,.0f} · 합 {v+dist:,.0f} · 수익률 {(v+dist)/paid-1:+.2%} · 주가만 {v/paid-1:+.2%}')
    print(f'  가장 깊은 손실 {worst[0]:+.2%} 날 {worst[1]} 그때 넣은 돈 {worst[2]:,} 그때 가치 {worst[3]:,.0f}')
    if name.startswith('매달'):
        loss=[h for h in hist if h[4]<0]; print('  매수일 기준 손실이던 달', len(loss), '/', len(hist), [h[0] for h in loss][:30])
        for h in hist:
            if h[0][4:6] in ('12',) or h[0]==END: print('   ',h[0],f'넣은 {h[1]:,} 평가+분배 {h[2]+h[3]:,.0f} {h[4]:+.2%}')
print('\n매수 첫날 종가', px[months[0]], '최저 종가', min((px[d],d) for d in days if START<=d<=END), '최고', max((px[d],d) for d in days if START<=d<=END))
yr={}
for d,a in ydiv.items():
    if d>=START: yr[d[:4]]=yr.get(d[:4],0)+a
print('연도별 주당 분배금', yr, '합', sum(yr.values()), '횟수', len([d for d in ydiv if d>=START]))

json.dump(SER,open('series.json','w'),ensure_ascii=False)
sh=1738;print('매달 평균 단가', round((30000000-6370)/sh), '· 한 번에 2,189주 차이', 2189-1738, '· 7/2 대비 지금', round(24400/28875-1,4), '· 2026-11-02 종가', px['20261102'])
