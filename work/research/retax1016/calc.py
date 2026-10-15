# 퇴직소득세 계산 — 소득세법 제48조(퇴직소득공제)·제55조(세율·②퇴직소득 산출세액)·제129조①5의3(연금수령 70/60/50%)
def basic(t):  # 제55조① 기본세율, 만원
    B=[(1400,0,.06),(5000,84,.15),(8800,624,.24),(15000,1536,.35),(30000,3706,.38),(50000,9406,.40),(100000,17406,.42),(1e12,38406,.45)]
    lo=0
    for hi,base,r in B:
        if t<=hi: return base+(t-lo)*r
        lo=hi
def ys_ded(n):
    if n<=5: return 100*n
    if n<=10: return 500+200*(n-5)
    if n<=20: return 1500+250*(n-10)
    return 4000+300*(n-20)
def conv_ded(c):
    if c<=800: return c
    if c<=7000: return 800+(c-800)*.6
    if c<=10000: return 4520+(c-7000)*.55
    if c<=30000: return 6170+(c-10000)*.45
    return 15170+(c-30000)*.35
def tax(pay,n):
    d=min(ys_ded(n),pay); conv=(pay-d)/n*12; base=conv-conv_ded(conv)
    return dict(근속공제=d,환산급여=conv,환산공제=conv_ded(conv),과표=base,산출세액=basic(base)/12*n)
for pay,n in [(20000,25),(20000,10),(10000,25),(10000,10),(30000,30)]:
    r=tax(pay,n); t=r['산출세액']
    print(f"퇴직금 {pay}만원 근속 {n}년:",{k:round(v,1) for k,v in r.items()}, f"| 지방세 포함 {t*1.1:.1f} | 연금 70% {t*.7:.1f} 60% {t*.6:.1f} 50% {t*.5:.1f} | 실효 {t/pay*100:.2f}%")
