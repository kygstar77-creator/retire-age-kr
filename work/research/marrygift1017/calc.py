# 상증법 제26조 세율·제53조·제53조의2·제69조②(신고세액공제 3%)로 증여세 계산
import sys; sys.stdout.reconfigure(encoding='utf-8')
def rate(b):
    for lo,base,r in [(30e8,10.4e8,.5),(10e8,2.4e8,.4),(5e8,0.9e8,.3),(1e8,0.1e8,.2),(0,0,.1)]:
        if b>lo: return base+(b-lo)*r
    return 0
def tax(gift, prior=0, basic=5e7, marry=1e8):
    v=gift+prior                       # 47② 10년 합산
    base=max(0, v-basic-marry)          # 53·53의2
    if base<50e4: return 0,0,base
    s=rate(base); return s, s*0.97, base  # 69② 3%
for g,p,m in [(1.5e8,0,1e8),(2e8,0,1e8),(2e8,0,0),(3e8,0,1e8),(3e8,0,0),(1.5e8,5e7,1e8),(1e8,0,1e8)]:
    s,n,b=tax(g,p,marry=m)
    print(f"받는 돈 {g/1e4:,.0f}만 · 10년 안 받은 돈 {p/1e4:,.0f}만 · 혼인공제 {m/1e4:,.0f}만 → 과표 {b/1e4:,.0f}만 · 산출 {s/1e4:,.0f}만 · 신고 시 {n/1e4:,.1f}만")
# 시부모→며느리: 3촌 이내 인척 1천만원, 혼인공제 없음(직계존속 아님)
s,n,b=tax(1e8,basic=1e7,marry=0); print(f"시부모→며느리 1억 → 과표 {b/1e4:,.0f}만 · 신고 시 {n/1e4:,.1f}만")
s,n,b=tax(1.5e8,basic=1e7,marry=0); print(f"시부모→며느리 1.5억 → 과표 {b/1e4:,.0f}만 · 신고 시 {n/1e4:,.1f}만")
