# renew1011 계산 2 — 전세·월세 사례 (주택임대차보호법 제6조의3 ⑥, 제7조의2, 시행령 제9조)
import sys; sys.stdout.reconfigure(encoding='utf-8')
base=3.0; r=min(0.10,(base+2)/100)   # 기준금리 3.0%(ECOS 2026-09) → 5%
def hw(dep,rent): return dep*r/12+rent   # 만원
print('전환율',r)
# 전세 3억
h=hw(30000,0); print('전세3억 환산',round(h,2),'3개월분',round(h*3,1),'증액상한',30000*0.05)
for nd in (32000,33000,33750,34000,36000):
    d=hw(nd,0)-h; print(' 새 전세',nd,'차액',round(d,2),'2년분',round(d*24,1),'큰금액',round(max(h*3,d*24),1))
# 월세 1억/80
h2=hw(10000,80); print('1억/80 환산',round(h2,2),'3개월분',round(h2*3,1),'경계 차액',round(h2/8,2))
for nr in (90,95,110):
    d=hw(10000,nr)-h2; print(' 새 월세',nr,'차액',round(d,2),'2년분',round(d*24,1),'큰',round(max(h2*3,d*24),1))
# 기준금리 2.5%(2026-06까지) 이면
r2=min(0.10,(2.5+2)/100); print('2.5%일때 전환율',r2,'전세3억 3개월분',round(30000*r2/12*3,1))
