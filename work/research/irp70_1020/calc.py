# IRP 70% 한도 계산 — 2025-12-30 종가에 70:30으로 담았다면 2026-10-19 종가에 몇 %인가
import json
def close(f, day):
    import datetime
    d=json.load(open('raw/'+f))['chart']['result'][0]
    for t,x in zip(d['timestamp'], d['indicators']['quote'][0]['close']):
        if x and str(datetime.datetime.fromtimestamp(t+32400, datetime.UTC).date())==day: return x
for name,f in [('KODEX 200','y_069500.KS.json'),('TIGER 미국S&P500','y_360750.KS.json'),('코스피 지수','y_%5EKS11.json')]:
    a,b=close(f,'2025-12-30'),close(f,'2026-10-19')
    r=b/a
    risk=7000*r; safe=3000  # 만원, 예금 이자는 뺌(보수적)
    share=risk/(risk+safe)
    target=0.7*(risk+safe); sell=risk-target
    print(f'{name}: {a:,.2f} -> {b:,.2f} ({(r-1)*100:+.2f}%) | 1억(7천:3천) -> 위험 {risk:,.0f}만 + 안전 {safe:,}만 = {risk+safe:,.0f}만, 위험 비중 {share*100:.1f}% | 70%로 되돌리려면 {sell:,.0f}만원 옮김')
# 주가가 몇 % 오르면 70%를 넘나: 처음부터 70%면 1원만 올라도 넘는다. 60%로 담았다면?
for w in (0.6,0.65,0.7):
    # w*(1+g)/(w*(1+g)+(1-w)) = 0.7 -> 1+g = 0.7*(1-w)/(0.3*w)
    g=0.7*(1-w)/(0.3*w)-1
    print(f'처음 위험자산 {w*100:.0f}% → 주가 {g*100:.1f}% 오르면 70%')

print('--- 분배금 반영 가격(네이버 fchart 수정주가) ---')
import re
def fc(code, day):
    t=open('raw/fc_%s.xml'%code,encoding='utf-8',errors='ignore').read()
    m=re.search(r'data="%s\|[^|]*\|[^|]*\|[^|]*\|([^|]*)\|'%day,t); return float(m.group(1))
for name,code in [('KODEX 200','069500'),('TIGER 미국S&P500','360750')]:
    a,b=fc(code,'20251230'),fc(code,'20261019'); r=b/a
    risk=7000*r; tot=risk+3000; sell=risk-0.7*tot
    print(f'{name}: {a:,.0f} -> {b:,.0f} ({(r-1)*100:+.2f}%) | 위험 {risk:,.0f}만 / 합계 {tot:,.0f}만 = {risk/tot*100:.1f}% | 되돌리려면 {sell:,.0f}만원')
    # 5천만원 계좌
    risk=3500*r; tot=risk+1500; print(f'   5천만원(3,500:1,500): 위험 {risk:,.0f}만 / {tot:,.0f}만 = {risk/tot*100:.1f}%, 되돌리려면 {risk-0.7*tot:,.0f}만원')
