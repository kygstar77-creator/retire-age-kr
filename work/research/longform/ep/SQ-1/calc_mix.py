"""SQ-1 비율별 과거값: SCHD·QQQ 섞기 (달러, 분배 재투자, 세금·환율·수수료 밖 보수는 이미 가격에 반영)
자료: raw/yh_SCHD_1112.json, raw/yh_QQQ_1112.json (Yahoo 월봉 adjclose = 분배 재투자 반영 2차)
대조: raw/schd_distributions_schwab_1112.csv(운용사), raw/nasdaq_QQQ_div_1112.json(Nasdaq)
구간: 2011-10 말 → 2026-10 말 (15년). 리밸런싱: 매년 10월 말 목표 비율로.
"""
import json, datetime as dt, statistics as st
def load(s):
    r=json.load(open(f'raw/yh_{s}_1112.json',encoding='utf-8'))['chart']['result'][0]
    out={}
    for t,a in zip(r['timestamp'], r['indicators']['adjclose'][0]['adjclose']):
        d=dt.datetime.fromtimestamp(t, dt.UTC); out[(d.year,d.month)]=a
    return out
S,Q=load('SCHD'),load('QQQ')
months=[k for k in sorted(S) if k in Q and (2011,10)<=k<=(2026,10)]
assert months[0]==(2011,10) and months[-1]==(2026,10), (months[0],months[-1])
def run(w, start=(2011,10), end=(2026,10)):
    ms=[m for m in months if start<=m<=end]
    v=1.0; a=w; b=1-w; peak=1.0; mdd=0.0; yearly={}; yv=1.0
    for p,m in zip(ms,ms[1:]):
        rs=S[m]/S[p]; rq=Q[m]/Q[p]
        a*=rs; b*=rq; v=a+b
        peak=max(peak,v); mdd=min(mdd,v/peak-1)
        if m[1]==12: yearly[m[0]]=v/yv-1; yv=v
        if m[1]==10: a=v*w; b=v*(1-w)
    yrs=(len(ms)-1)/12
    return v, v**(1/yrs)-1, mdd, yearly
print('구간 2011-10말 → 2026-10말, 1억(달러 기준 같은 비율) 분배 재투자, 매년 10월 말 비율 맞춤')
print('SCHD비율  끝값(1억→)  연평균  최대낙폭  2022년  2020년  최악연도')
res={}
for w in [1.0,0.7,0.5,0.3,0.0]:
    v,c,m,y=run(w); res[w]=(v,c,m,y)
    worst=min(y.items(), key=lambda kv:kv[1])
    print(f'{int(w*100):>3}%   {v:6.2f}억   {c*100:5.2f}%  {m*100:6.1f}%  {y[2022]*100:6.1f}%  {y[2020]*100:6.1f}%  {worst[0]} {worst[1]*100:.1f}%')
# 최근 5년·10년
for lbl,st_ in [('최근 10년',(2016,10)),('최근 5년',(2021,10))]:
    print(lbl)
    for w in [1.0,0.5,0.0]:
        v,c,m,y=run(w,start=st_); print(f'  SCHD {int(w*100)}%: 1억→{v:.2f}억 연 {c*100:.2f}% 최대낙폭 {m*100:.1f}%')
# 분배금: 최근 4회 합(주당) ÷ 10월 말 종가 (참고용 분배 수익률)
def close(s,k):
    r=json.load(open(f'raw/yh_{s}_1112.json',encoding='utf-8'))['chart']['result'][0]
    for t,c in zip(r['timestamp'], r['indicators']['quote'][0]['close']):
        d=dt.datetime.fromtimestamp(t, dt.UTC)
        if (d.year,d.month)==k: return c
schd4=0.2782+0.2569+0.2525+0.2665  # 운용사 CSV 12/2025~9/2026
nq=json.load(open('raw/nasdaq_QQQ_div_1112.json'))['data']['dividends']['rows'][:4]
qqq4=sum(float(r['amount'].strip('$')) for r in nq)
cs,cq=close('SCHD',(2026,10)),close('QQQ',(2026,10))
print(f'최근 4회 분배 합 SCHD {schd4:.4f}$ / 10월말 {cs:.2f}$ = {schd4/cs*100:.2f}%  · QQQ {qqq4:.4f}$ / {cq:.2f}$ = {qqq4/cq*100:.2f}%')
print('1억(가정: 달러로 바꿔 같은 비율) 연 분배 어림: SCHD 100% %.0f만원 · 50%% %.0f만원 · QQQ 100%% %.0f만원 (세전, 환율 고정 가정)'.replace('%.0f','{:.0f}').replace('%%','%').format(1e8*schd4/cs/1e4, 1e8*(0.5*schd4/cs+0.5*qqq4/cq)/1e4, 1e8*qqq4/cq/1e4))
