# 현대차 2026년 배당 · 건보료(1천만원)·종합과세(2천만원) 문턱 주식 수 — 원문 raw/*.txt, 주가 raw/yahoo_*.json
import math,json,sys
sys.stdout.reconfigure(encoding='utf-8')
com=[2500,2500,2500,2500]   # 결산(기준 2/28, 주총 3/26 결의)·1분기(5/31)·2분기(8/31)·3분기(11/30)
pref=[2600,2500,2500,2500]  # 종류주식 결산 2,600
P=json.load(open('raw/yahoo_005380.KS.json'))['chart']['result'][0]['indicators']['quote'][0]['close'][-1]
Q=json.load(open('raw/yahoo_005387.KS.json'))['chart']['result'][0]['indicators']['quote'][0]['close'][-1]
c,p=sum(com),sum(pref); print('1주당 2026 합계 보통',c,'우선',p)
tax=0.14+0.014
print('3분기 100주 세전',2500*100,'세후',round(2500*100*(1-tax)))
for lim in (10_000_000,20_000_000):
    n=lim//c+1; m=lim//p+1
    print(f'{lim:,} 넘는 첫 주식 수 보통 {n}주(배당 {n*c:,}) 가격 {n*P:,.0f} | 2우B {m}주(배당 {m*p:,}) 가격 {m*Q:,.0f}')
print('주가 보통',P,'2우B',Q,'시가배당률(연) 보통',round(c/P*100,2),'2우B',round(p/Q*100,2))
# 예금 이자 500만원 있으면
n=(10_000_000-5_000_000)//c+1; print('이자 500만원 있으면 1천만원 넘는 첫 주식 수',n,'합계',5_000_000+n*c)
# 3분기 하나만 받는다면(11/26 매수) 1천만원
print('3분기 하나로 1천만원 넘으려면',10_000_000//2500+1,'주')
