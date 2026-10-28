# 주택연금 부부 모두 사망 시 정산 — 자녀(상속인)에게 남는 돈
# 원문: HF 월지급금 예시(종신지급·정액형, 2026.3.1 기준) 70세 4억 = 1,231천원 / 초기보증료 주택가격 1.0% (최초 지급일) /
#       연보증료 보증잔액 연 0.95% (매월) / 대출금리 91일물 CD + 1.1%p (CD 2026-10-28 3.27%, ECOS 817Y002) — 금리는 이 값으로 고정 가정
#       정산: 주택처분금액 > 연금지급총액 → 남는 부분 상속인, 부족하면 청구 없음 · 상속인이 직접 갚으면 집값과 잔액 중 적은 금액
CD=0.0327; RATE=CD+0.011; FEE=0.0095; INIT=0.01
def bal_after(years, house=400_000_000, pay=1_231_000):
    bal=house*INIT; paid=0
    for m in range(int(years*12)):
        bal+=pay; paid+=pay
        bal+=bal*(FEE+RATE)/12
    return bal, paid
house=400_000_000
print("70세 가입·4억 집·월 123만1천원, 금리 %.2f%%(CD %.2f%%+1.1%%p) 고정" % (RATE*100, CD*100))
for age in (75,80,85,90,95):
    y=age-70; b,p=bal_after(y)
    left=max(0,house-b); keep=min(house,b)
    print(f"{age}세 ({y}년): 받은 돈 {p/1e4:,.0f}만 · 대출잔액 {b/1e4:,.0f}만 · 집값 그대로면 남는 돈 {left/1e4:,.0f}만 · 집 지키려면 갚을 돈 {keep/1e4:,.0f}만")
# 잔액이 집값(4억)을 넘는 달
m=0; bal=house*INIT
while bal<house:
    bal+=1_231_000; bal+=bal*(FEE+RATE)/12; m+=1
print(f"잔액이 4억을 넘는 때: {m}개월 = {m//12}년 {m%12}개월 뒤 (약 {70+m/12:.1f}세)")
# 집값이 연 1%·2% 오르면 같아지는 나이
for g in (0.01,0.02):
    m=0; bal=house*INIT; h=house
    while bal<h and m<12*40:
        bal+=1_231_000; bal+=bal*(FEE+RATE)/12; m+=1; h*=(1+g)**(1/12)
    print(f"집값 연 {g*100:.0f}% 오르면 같아지는 때: {m//12}년 {m%12}개월 (약 {70+m/12:.1f}세), 그때 집값 {h/1e4:,.0f}만")
