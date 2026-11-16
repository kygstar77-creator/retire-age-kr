# coinyu1116 직접 계산 — 업비트 KRW-BTC 일봉(raw/up_BTC_*.json, 2026-11-16 받음) · 소득세법 64조의3②(250만원·20%, 지방 10% 더해 22%)
import json,sys
sys.stdout.reconfigure(encoding='utf-8')
P={}
for y in range(2018,2027):
    d=json.load(open(f'raw/up_BTC_{y}0101.json'))[0]; P[y-1]=d['trade_price']   # y-1년 12/31 종가
now=json.load(open('raw/up_BTC_now.json'))[0]; P['now']=now['trade_price']
print('§1 해마다 연말 종가(원)', {k:int(v) for k,v in P.items()}, now['candle_date_time_kst'])
R={}
for y in range(2018,2026):
    R[y]=P[y]/P[y-1]-1
    print(f'  {y}년 한 해 {R[y]:+.1%}')
print(f'  2026년 1/1~11/16 {P["now"]/P[2025]-1:+.1%}')
loss=[y for y in R if R[y]<0]; print('  손해 본 해', loss, '8해 중', len(loss))
def tax(g): return max(0,g-250)*0.22   # 만원
def tax_cf(g,cf):  # 재경부 설명: 250만원 먼저 빼고 남은 데서 이월 손실
    base=max(0,g-250); use=min(base,cf); return (base-use)*0.22, cf-use
print('§2 해마다 1월 1일 1천만원어치 사서 12월 31일에 판다고 치면(만원)')
for a,b in [(2018,2019),(2022,2023),(2025,2026)]:
    la=1000*R[a]; gb=1000*(R[b] if b in R else P['now']/P[2025]-1)
    t0=tax(gb); t1,left=tax_cf(gb,-la) if la<0 else (t0,0)
    print(f'  {a}년 {la:+.0f} → {b}년 {gb:+.0f} · 지금 법 세금 {t0:.1f} · 이월공제 있으면 {t1:.1f} · 차이 {t0-t1:.1f} · 남은 손해 {left:.0f}')
print('§3 정부 예시: 1천만원 손해 다음 해 1천만원 이익', tax(1000), '→', tax_cf(1000,1000))
print('§4 1천만원 이익 세금', tax(1000), '· 3천만원', tax(3000), '· 300만원', tax(300))
print('§5 2025년 말 1천만원어치 산 경우 지금 값', round(1000*P['now']/P[2025]), '만원')
