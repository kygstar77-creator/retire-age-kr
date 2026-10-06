# 가정 사례: 근속 25년 차에 임금피크 시작, 월급 600만원, 이후 5년 80·70·60·60·60%, 퇴직(근속 30년)
# 퇴직금 = 30일분 평균임금 x 근속연수. 평균임금 ≈ 월급(3개월 총일수 차이는 무시한 근사)
base=600; years_before=25; peak=[0.8,0.7,0.6,0.6,0.6]
last=base*peak[-1]
a=last*(years_before+len(peak))
b_mid=base*years_before; b_after=last*len(peak); b=b_mid+b_after
c_db=base*years_before; c_dc=sum(base*p*12/12 for p in peak); c=c_db+c_dc
print(f"A 그대로(퇴직 직전 월급 {last:.0f}만 x 30년) = {a:,.0f}만원")
print(f"B 피크 직전 중간정산 {b_mid:,.0f} + 피크 5년 {b_after:,.0f} = {b:,.0f}만원 (A보다 {b-a:,.0f}만원)")
print(f"C 피크 직전 DC 전환 {c_db:,.0f} + 매년 연봉 1/12 {c_dc:,.0f} = {c:,.0f}만원 (A보다 {c-a:,.0f}, B보다 {c-b:,.0f}) — 운용수익 0% 가정")
