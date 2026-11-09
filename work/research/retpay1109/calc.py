# retpay1109 계산 — 소득세법 제48조(근속연수공제·환산급여공제)·제55조①②(기본세율, ÷12×근속)·제129조①5의3(70/60/50%)·지방세법 제103조의13(10%)·시행령 제40조의2③④(한도)
import sys; sys.stdout.reconfigure(encoding='utf-8')
def kunsok(n):
    if n<=5: return 100e4*n
    if n<=10: return 500e4+200e4*(n-5)
    if n<=20: return 1500e4+250e4*(n-10)
    return 4000e4+300e4*(n-20)
def hwan(h):
    if h<=800e4: return h
    if h<=7000e4: return 800e4+(h-800e4)*.6
    if h<=1e8: return 4520e4+(h-7000e4)*.55
    if h<=3e8: return 6170e4+(h-1e8)*.45
    return 15170e4+(h-3e8)*.35
def basic(t):
    B=[(1400e4,0,.06,0),(5000e4,84e4,.15,1400e4),(8800e4,624e4,.24,5000e4),(1.5e8,1536e4,.35,8800e4),(3e8,3706e4,.38,1.5e8),(5e8,9406e4,.40,3e8)]
    for top,base,r,lo in B:
        if t<=top: return base+(t-lo)*r
    return 17406e4+(t-5e8)*.42
def tax(pay,n):
    a=max(pay-kunsok(n),0); h=a/n*12; t=max(h-hwan(h),0); s=basic(t)/12*n
    return dict(kunsok=kunsok(n),hwan=h,hwanded=hwan(h),base=t,national=s,total=s*1.1)
for pay in (1e8,):
    for n in (10,20,30):
        r=tax(pay,n); T=r['total']
        print(f"퇴직금 {pay/1e4:,.0f}만 근속 {n}년: 근속공제 {r['kunsok']/1e4:,.0f}만 환산 {r['hwan']/1e4:,.0f}만 환산공제 {r['hwanded']/1e4:,.0f}만 과표 {r['base']/1e4:,.0f}만 국세 {r['national']:,.0f} 지방포함 {T:,.0f} ({T/pay*100:.2f}%) | 연금 1~10년차 70% {T*.7:,.0f} 11~20 60% {T*.6:,.0f} 21~ 50% {T*.5:,.0f} | 일시금-70% 차이 {T*.3:,.0f}")
print('한도 1억 첫해 보통(1년차): ', 1e8/(11-1)*1.2)
print('한도 1억 첫해 2013.3 전(6년차): ', 1e8/(11-6)*1.2)
