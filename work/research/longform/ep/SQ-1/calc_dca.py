"""SQ-1 3장 끝 한 줄: 같은 비율로 '매달 100만원씩 나눠 넣은' 경우 (calc_mix.py와 같은 자료·같은 리밸런싱)
자료: raw/yh_SCHD_1112.json, raw/yh_QQQ_1112.json (Yahoo 월봉 adjclose, S7 검증 check_930_out.txt)
가정: 매달 말 종가에 100만원(달러로 바꿔 같은 환율로 셈 = 환율 고정), 매년 10월 말 목표 비율로 맞춤, 세금·매매비용 뺌.
넣는 달: 시작 달 말 ~ 끝 달 전 달 말(끝 달 말 값으로 평가). 15년 = 180번, 5년 = 60번.
"""
import json, datetime as dt
def load(s):
    r=json.load(open(f'raw/yh_{s}_1112.json',encoding='utf-8'))['chart']['result'][0]
    return {(d.year,d.month):a for t,a in zip(r['timestamp'], r['indicators']['adjclose'][0]['adjclose']) for d in [dt.datetime.fromtimestamp(t, dt.UTC)]}
S,Q=load('SCHD'),load('QQQ')
months=[k for k in sorted(S) if k in Q and (2011,10)<=k<=(2026,10)]
def dca(w,start,end=(2026,10),amt=1.0):
    ms=[m for m in months if start<=m<=end]
    a=b=0.0; paid=0.0; worst=0.0
    for i,m in enumerate(ms):
        if i>0:
            p=ms[i-1]; a*=S[m]/S[p]; b*=Q[m]/Q[p]
        v=a+b
        if paid>0: worst=min(worst, v/paid-1)
        if m[1]==10 and v>0: a,b=v*w,v*(1-w)
        if m!=ms[-1]: a+=amt*w; b+=amt*(1-w); paid+=amt
    return a+b, paid, worst
print('매달 100만원, 끝 2026-10말 평가 (단위 만원)')
for lbl,st in [('15년(2011-10~)',(2011,10)),('최근 10년(2016-10~)',(2016,10)),('최근 5년(2021-10~)',(2021,10))]:
    print(lbl)
    for w in [1.0,0.7,0.5,0.3,0.0]:
        v,p,wo=dca(w,st); print(f'  SCHD {int(w*100):>3}%: 넣은 돈 {p*100:,.0f} → {v*100:,.0f} (×{v/p:.2f}) · 넣은 돈보다 가장 낮았던 때 {wo*100:.1f}%')
