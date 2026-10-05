# goldway1005 계산 — 숫자는 facts.txt 원자료(krxgold.json, y_*.json, KB 고시)에서
M=10_000_000
krx0,krx1=187300,182770            # KRX 금 1kg 종가 원/g (네이버 M04020000) 2025-10-02 / 2026-10-02
etf0,etf1=26360,25515              # ACE KRX금현물 종가 2025-10-02 / 2026-10-02
gc0,fx0=3868.10009765625,1401.8199462890625   # GC=F, USD/KRW (야후) 2025-10-02 행
oz=31.1034768
kb_now_buy,kb_now_sell,kb_now_gold,kb_now_fx=182035.23,178430.59,4171.50,1343.85
kb_now_base=kb_now_gold*kb_now_fx/oz
print('KB 기준가 재계산',round(kb_now_base,2),'살때 +%.2f%%'%((kb_now_buy/kb_now_base-1)*100),'팔때 %.2f%%'%((kb_now_sell/kb_now_base-1)*100))
r_krx=krx1/krx0-1; print('KRX 1년 %.2f%%'%(r_krx*100), '1천만원→',round(M*(1+r_krx)), '차', round(M*r_krx))
r_etf=etf1/etf0-1; print('ETF 1년 %.2f%%'%(r_etf*100), round(M*(1+r_etf)), round(M*r_etf))
intl0=gc0*fx0/oz; intl1=kb_now_base
print('국제값 원/g 1년전 어림',round(intl0),'지금 KB기준',round(intl1),'%.2f%%'%((intl1/intl0-1)*100))
print('KRX 괴리 1년전 %.1f%%'%((krx0/intl0-1)*100))
# 골드뱅킹 어림: 1년 전 기준가×(살때 가산 비율 지금과 같다고 가정)
buy0=intl0*(kb_now_buy/kb_now_base)
g=M/buy0; val=g*kb_now_sell; gain=val-M; tax=max(0,gain)*0.154
print('골드뱅킹 어림 살때',round(buy0),'g',round(g,2),'팔면',round(val),'차익',round(gain),'세금',round(tax),'손에',round(val-tax))
# 실물: 부가세 10% 포함 1천만원
print('실물 금값 부분',round(M/1.1),'부가세',round(M-M/1.1))
# 10% 오른다고 할 때(가정)
up=0.10
print('가정+10%: KRX',round(M*up),'세금0 / ETF·골드뱅킹 세금',round(M*up*0.154),'/ 실물',round(M/1.1*1.1))
