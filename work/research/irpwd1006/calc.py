# 소득세법 48조(퇴직소득공제)·55조①②(세율, 퇴직소득 산출세액) 그대로. 지방소득세 10% 별도.
import math
def yrded(y):
    if y<=5: return 100e4*y
    if y<=10: return 500e4+200e4*(y-5)
    if y<=20: return 1500e4+250e4*(y-10)
    return 4000e4+300e4*(y-20)
def convded(c):
    if c<=800e4: return c
    if c<=7000e4: return 800e4+(c-800e4)*0.6
    if c<=1e8: return 4520e4+(c-7000e4)*0.55
    if c<=3e8: return 6170e4+(c-1e8)*0.45
    return 15170e4+(c-3e8)*0.35
def rate(t):
    br=[(1400e4,0,.06,0),(5000e4,84e4,.15,1400e4),(8800e4,624e4,.24,5000e4),(15000e4,1536e4,.35,8800e4),(3e8,3706e4,.38,15000e4),(5e8,9406e4,.40,3e8),(1e9,17406e4,.42,5e8),(9e99,38406e4,.45,1e9)]
    for top,base,r,lo in br:
        if t<=top: return base+(t-lo)*r
def tax(pay,y):
    d1=min(yrded(y),pay); conv=(pay-d1)/y*12; base=max(conv-convded(conv),0)
    t=rate(base)/12*y; return d1,conv,base,t,t*1.1
    d1,conv,base,t,tot=tax(pay,y)
# irpwd1006: 퇴직금 2억·근속 15년 IRP 이체 후 중도인출. 시행령 202조의2② 비례, 소득세법 129조①5의3 70%, 시행규칙 11조의2 한도
pay,y=2e8,15
d1,conv,base,t,tot=tax(pay,y)
r=tot/pay
print(f"이연퇴직소득세(지방 포함) {tot/1e4:,.1f}만원 실효 {r*100:.3f}%")
lim=2000e4+6*150e4+200e4
print(f"요양 인출 한도(의료·간병 2,000만+휴직6개월×150만+200만) {lim/1e4:,.0f}만원")
for name,amt,k in [("요양 6개월(부득이·연금수령 70%)",lim,0.7),("주택구입(연금외수령 100%)",lim,1.0)]:
    print(f"{name}: {amt/1e4:,.0f}만원 인출 세금 {amt*r*k/1e4:,.1f}만원 손에 {(amt-amt*r*k)/1e4:,.1f}만원")
print(f"차이 {lim*r*0.3/1e4:,.1f}만원")
print(f"전액 해지(55세 전·사유 없음) 세금 {tot/1e4:,.1f}만원 손에 {(pay-tot)/1e4:,.0f}만원")
for age_lim in [1]:
    first=pay*1.2/10
    print(f"55세 뒤 연금 개시 첫해 한도 평가액×120%/(11-1) = {first/1e4:,.0f}만원, 세금 {first*r*0.7/1e4:,.1f}만원")
