# 고배당 ETF 분배금(종합과세, 소득세법 제62조 비교과세) vs 고배당기업 직접 배당(조특법 104조의27 분리과세 신청) — 소득세만(지방소득세 10% 별도)
def base(x):  # 국세청 기본세율표(만원)
    t=[(1400,0,6),(5000,84,15),(8800,624,24),(15000,1536,35),(30000,3706,38),(50000,9406,40),(100000,17406,42),(10**9,38406,45)]
    lo=0
    for hi,b,r in t:
        if x<=hi: return b+(x-lo)*r/100
        lo=hi
def sep(d):  # 104조의27② 분리과세 세율
    t=[(2000,0,14),(30000,280,20),(500000,5880,25),(10**9,123880,30)]
    lo=0
    for hi,b,r in t:
        if d<=hi: return b+(d-lo)*r/100
        lo=hi
def etf(d,other):
    if d<=2000: return d*0.14+base(other)
    a=base(d-2000+other)+2000*0.14
    b=d*0.14+base(other)
    return max(a,b)
for d in (2000,3000):
  for other in (0,3000,6000,10000):
    e=etf(d,other); s=sep(d)+base(other)
    print(f"분배금 {d}만 다른과표 {other}만: ETF {e:.0f} 직접분리 {s:.0f} 차이(ETF-직접) {e-s:+.0f} 지방포함 {(e-s)*1.1:+.0f}")
print('check sep 3000',sep(3000),'base 2000',base(2000))
for other in (4000,4500,5000):
    e=etf(3000,other); s=sep(3000)+base(other); print(f"경계 확인 분배금 3000만 다른과표 {other}만: ETF {e:.0f} 직접 {s:.0f} 차이 {e-s:+.0f}")
