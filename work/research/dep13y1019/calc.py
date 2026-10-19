# 1억, 세율 15.4%, 단리 만기일시(이자 만기 수령) 가정
P=100_000_000; T=0.154
def after(p,r,y): return p*r*y*(1-T)
three=after(P,0.027,3)   # 우리 WON플러스 3년 2.7%(기본=최고)
print('3년 고정 2.7% 세후 이자', round(three))
y1=after(P,0.036,1); print('1년 3.6% 1년차 세후', round(y1))
# 2·3년차 같은 금리 x로 다시 넣을 때(원금+세후이자 재예치) 3년 고정과 같아지는 x
def roll(x):
    p=P+y1; i2=after(p,x,1); p+=i2; i3=after(p,x,1); return y1+i2+i3
lo,hi=0,0.05
for _ in range(60):
    m=(lo+hi)/2
    (lo,hi)=(m,hi) if roll(m)<three else (lo,m)
print('같아지는 금리', round(lo*100,3))
print('1년 3.6% 3번 그대로', round(roll(0.036)), '차이', round(roll(0.036)-three))
print('2년 차부터 3.0%', round(roll(0.030)), round(roll(0.030)-three))
print('2년 차부터 2.5%', round(roll(0.025)), round(roll(0.025)-three))
# 중도해지: 1년 뒤 돈 필요 — 3년짜리 중도해지이율은 상품마다 다름(확인 안 함) → 글에선 '약관 확인'
