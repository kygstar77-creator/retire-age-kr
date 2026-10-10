# 계약갱신청구권 사례 계산 (법: 주임법 제6조의3·제7조·제7조의2, 시행령 제9조, 한은 기준금리 2026-09 3.0%)
base=3.0; rate=min(10.0, base+2.0)/100
dep=10000; rent=80   # 만원
conv=rent+dep*rate/12
print('전환율',rate,'환산월차임',round(conv,2),'3개월분',round(conv*3,1))
new=150; diff=new-conv
print('새 임차인 환산월차임',new,'차액',round(diff,2),'2년분',round(diff*24,1),'큰 금액',round(max(conv*3,diff*24),1))
print('보증금 3억 5% 상한',30000*0.05,'보증금3억 월세0 -> 증액상한',30000*0.05)
print('보증금 2억+월세50 -> 보증금 상한',20000*.05,'월세 상한',50*.05)
