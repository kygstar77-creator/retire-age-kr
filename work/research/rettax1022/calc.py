# 소득세법 48조·55조②·시행령105조 그대로. 지방소득세는 소득세의 10%(지방세법 103조의13 확인 후)
def C(n):
    if n<=5: return 100e4*n
    if n<=10: return 500e4+200e4*(n-5)
    if n<=20: return 1500e4+250e4*(n-10)
    return 4000e4+300e4*(n-20)
def D(s):
    if s<=800e4: return s
    if s<=7000e4: return 800e4+(s-800e4)*.6
    if s<=1e8: return 4520e4+(s-7000e4)*.55
    if s<=3e8: return 6170e4+(s-1e8)*.45
    return 15170e4+(s-3e8)*.35
B=[(1400e4,.06,0),(5000e4,.15,84e4),(8800e4,.24,624e4),(15000e4,.35,1536e4),(3e8,.38,3706e4),(5e8,.40,9406e4),(10e8,.42,17406e4),(1e20,.45,38406e4)]
def tax(t):
    lo=0
    for hi,r,base in B:
        if t<=hi: return base+(t-lo)*r
        lo=hi
def ret(P,n):
    c=min(C(n),P); s=(P-c)*12/n; d=D(s); t=max(s-d,0)
    it=int(tax(t)/12*n)
    return dict(P=P,n=n,C=c,S=s,D=d,T=t,tax=it,local=int(it*0.1),total=int(it*1.1),eff=it*1.1/P*100)
if __name__=='__main__':
    import json
    for P in (3e7,5e7,1e8,2e8,3e8):
        for n in (5,10,15,20,25,30):
            r=ret(P,n); print(f"{P/1e4:>6.0f}만 {n:>2}년 세금 {r['tax']:>11,} 지방 {r['local']:>9,} 합 {r['total']:>11,} {r['eff']:.2f}% 과표 {r['T']:,.0f}")
