# 같은 날(2024-10-22, KODEX 상장일 — 셋 다 있는 첫 날) 1억씩. 종가: 야후 chart(수정 전 close). 분배: 운용사 원문(official_div.json — TIGER 표·삼성 divid-info),
# 배당락 = 지급기준일 바로 앞 거래일(야후 분배 날짜와 같은 규칙, 10/30 기준 → 10/29). 세금: 과세표준(taxDividA)×15.4%. 매매 수수료 뺌.
import json, sys, datetime as dt, statistics as st
sys.stdout.reconfigure(encoding='utf-8')
N={'441680':'TIGER 미국나스닥100커버드콜(합성)','486290':'TIGER 미국나스닥100타겟데일리커버드콜','494300':'KODEX 미국나스닥100데일리커버드콜OTM','133690':'TIGER 미국나스닥100'}
K=dt.timezone(dt.timedelta(hours=9)); OFF=json.load(open('official_div.json',encoding='utf-8'))
START=dt.date(2024,10,22); AMT=1e8; TAX=0.154
def prices(t):
    j=json.load(open(f'raw/{t}.json'))['chart']['result'][0]
    return [(dt.datetime.fromtimestamp(a,K).date(),b) for a,b in zip(j['timestamp'],j['indicators']['quote'][0]['close']) if b]
def divs(t,px):
    days=[d for d,_ in px]
    if t in OFF:
        out=[]
        for b,a,tx in OFF[t]:
            bd=dt.date.fromisoformat(b); ex=max((d for d in days if d<bd),default=None)
            # 11/30 기준 분배(KODEX 140·TIGER 94·110원 공지)는 셈에서 뺌
            if ex and ex>=START and bd<=dt.date(2026,10,31): out.append((ex,a,tx,bd))  # 11/30 기준은 TIGER 표에 아직 없음 → 셋 다 10월까지
        return sorted(out)
    j=json.load(open(f'raw/{t}.json'))['chart']['result'][0]
    return sorted((dt.datetime.fromtimestamp(int(k),K).date(),v['amount'],v['amount'],None) for k,v in j['events']['dividends'].items() if dt.datetime.fromtimestamp(int(k),K).date()>=START)
for t,nm in N.items():
    px=[p for p in prices(t) if p[0]>=START]; dv=divs(t,px); dd={}
    for ex,a,tx,bd in dv: dd.setdefault(ex,[0,0]); dd[ex][0]+=a; dd[ex][1]+=tx
    d0,p0=px[0]; sh=AMT/p0; shr=sh; cash=0; cashT=0; peak=0; mdd=0
    for d,p in px:
        if d in dd:
            a,tx=dd[d]; cash+=sh*a; cashT+=sh*(a-tx*TAX); shr+=shr*a/p
        peak=max(peak,sh*p); mdd=min(mdd,sh*p/peak-1)
    dl,pl=px[-1]; n=len(dv)
    print(f'{nm}({t}) {d0} {p0:,.0f}원 → {dl} {pl:,.0f}원 (주가 {pl/p0-1:+.1%}) · 주가 최대 낙폭 {mdd:.1%}')
    print(f'  분배 {n}번(락일 {dv[0][0]}~{dv[-1][0]}) 1주 합 {sum(x[1] for x in dv):,}원 · 과세표준 합 {sum(x[2] for x in dv):,}원({sum(x[2] for x in dv)/max(1,sum(x[1] for x in dv)):.0%})')
    print(f'  현금 받기 세전: 분배 {cash/1e4:,.0f}만 + 평가 {sh*pl/1e4:,.0f}만 = {(sh*pl+cash)/1e4:,.0f}만 · 세후 분배 {cashT/1e4:,.0f}만 → {(sh*pl+cashT)/1e4:,.0f}만 · 세금 {(cash-cashT)/1e4:,.0f}만')
    print(f'  다시 사기(세전): {shr*pl/1e4:,.0f}만 · 한 달 평균 분배(1억, 세전) {cash/n/1e4:,.1f}만')
    l12=dv[-12:] if t in OFF else dv[-4:]; print(f'  최근 12번 1주 {sum(x[1] for x in l12):,}원 ÷ {pl:,.0f} = {sum(x[1] for x in l12)/pl:.2%} · 최근 3번 '+', '.join(f'{x[3] or x[0]} {x[1]}({x[2]})' for x in dv[-3:]))
