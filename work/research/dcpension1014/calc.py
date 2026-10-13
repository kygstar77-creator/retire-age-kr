# DB형 대 DC형 퇴직급여 비교 (예시: 첫해 연봉 5,000만원, 20년 근속, 부담금은 매년 말 연봉의 1/12 납입)
W0=5000; N=20
def wages(g,peak=None):
    w=[W0*(1+g)**k for k in range(N)]
    if peak:  # 마지막 peak년 동안 직전 연봉에서 피크 직전의 80%로 고정(임금피크 예시)
        base=w[N-peak-1]
        for i in range(N-peak,N): w[i]=base*0.8
    return w
def db(w): return w[-1]/12*N
def dc(w,r): return sum(w[k]/12*(1+r)**(N-1-k) for k in range(N))
out=[]
out.append("[1] 임금상승률 g · 운용수익률 r 별 20년 뒤 퇴직급여(만원)")
for g in (0.02,0.03,0.04):
    w=wages(g); line=f"g={g:.0%}: DB {db(w):,.0f} | "+" | ".join(f"DC r={r:.2%} {dc(w,r):,.0f}" for r in (0.02,0.0309,0.0353,0.05,0.0847))
    out.append(line)
out.append("[2] r=g면 같은지: g=3%% DB %.1f DC %.1f"%(db(wages(.03)),dc(wages(.03),.03)))
out.append("[3] 임금피크(마지막 5년 피크 직전의 80%) g=3%")
w=wages(.03,peak=5)
out.append(f"마지막 연봉 {w[-1]:,.0f} 피크 직전 연봉 {w[N-6]:,.0f} | DB {db(w):,.0f} | DC r=3.09% {dc(w,.0309):,.0f} | DC r=2% {dc(w,.02):,.0f}")
w2=wages(.03); out.append(f"피크 없을 때 DB {db(w2):,.0f} 마지막 연봉 {w2[-1]:,.0f}")
# 피크 직전 DC 전환 (15년 DB 정산 후 남은 5년 DC r=3.09%)
w=wages(.03,peak=5); db15=w[N-6]/12*15; rest=sum(w[k]/12*(1.0309)**(N-1-k) for k in range(15,N))
out.append(f"피크 직전 DC 전환: DB 15년분 {db15:,.0f}을 r=3.09%로 5년 굴림 {db15*1.0309**5:,.0f} + 남은 5년 DC {rest:,.0f} = {db15*1.0309**5+rest:,.0f}")
# 손익분기 r 찾기 g=3%
import math
for g in (0.02,0.03,0.04):
    w=wages(g); lo,hi=0,0.2
    for _ in range(60):
        m=(lo+hi)/2
        (lo,hi)=(m,hi) if dc(w,m)<db(w) else (lo,m)
    out.append(f"손익분기 r (g={g:.0%}) = {lo:.2%}")
open('calc_out.txt','w',encoding='utf-8').write("\n".join(out)); print("\n".join(out))
