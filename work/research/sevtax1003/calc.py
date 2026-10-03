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
for pay in (1e8,2e8,3e8):
  for y in (5,10,15,20,25,30):
    d1,conv,base,t,tot=tax(pay,y)
    print(f"퇴직금 {pay/1e8:.0f}억 근속 {y:2d}년: 근속공제 {d1/1e4:,.0f}만 환산급여 {conv/1e4:,.0f}만 과표 {base/1e4:,.0f}만 소득세 {t/1e4:,.1f}만 +지방 합계 {tot/1e4:,.1f}만 ({tot/pay*100:.2f}%) 손에 {(pay-tot)/1e4:,.0f}만")
