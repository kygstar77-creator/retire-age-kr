# wolsegong1027 계산 — 조세특례제한법 제95조의2 (현행 한도 1,000만원, 정부안 1,200만원). 단위 만원
def credit(monthly, cap, rate):
    return min(monthly*12, cap)*rate
print("월세(월) 연월세 | 15% 현행 정부안 차 | 17% 현행 정부안 차 | 청년 15%→17% 차")
for m in (70, 83, 84, 90, 100):
    a15, b15 = credit(m,1000,.15), credit(m,1200,.15)
    a17, b17 = credit(m,1000,.17), credit(m,1200,.17)
    print(m, m*12, '|', round(a15,1), round(b15,1), round(b15-a15,1), '|', round(a17,1), round(b17,1), round(b17-a17,1), '|', round(b17-a15,1))
print('한도 도달 월세(월)=', 1000/12, ' 정부안=', 1200/12)
