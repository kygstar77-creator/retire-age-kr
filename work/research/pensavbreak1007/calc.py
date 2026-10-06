# 사례 가정: 연금저축에 5년간 해마다 600만원(세액공제 한도 소득세법 59조의3) 납입, 운용수익 400만원
pay_year, years, gain = 600, 5, 400
principal = pay_year*years
val = principal + gain
for label, rate in (("총급여 5,500만원 이하(15%+지방 1.5%)", 0.165), ("총급여 5,500만원 초과(12%+지방 1.2%)", 0.132)):
    refund = principal*rate
    tax = val*0.165
    print(f"{label}: 5년간 돌려받은 세액 {refund:.0f}만원 / 해지 때 떼는 세금 {tax:.1f}만원 / 차이 {tax-refund:.1f}만원 / 손에 쥐는 돈 {val-tax:.1f}만원")
print(f"55세 이후 연금수령 70세 미만 5.5%: {val*0.055:.1f}만원")
print(f"원금만 해지(수익 0): 16.5%자 {principal*0.165-principal*0.165:.0f}만원 차이, 13.2%자 {principal*0.165-principal*0.132:.0f}만원 더 냄")
# 공제 한도 넘겨 넣은 돈: 연 900만원씩 넣었다면 300만원×5=1,500만원은 세금 없이 먼저 빠짐(시행령 40조의3②3)
print("연 900만원 납입 시 공제 밖 1,500만원은 과세제외금액으로 먼저 인출")
