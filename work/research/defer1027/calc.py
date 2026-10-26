# 연기연금 계산 — 국민연금법 62조(매달 0.6%), 부칙 11143호 6조(1969년생 이후 70세까지),
# 건보 시행령 44조 7.19%, 시행규칙 44조 연금 50%, 법 71조 ÷12, 장기요양 시행령 4조 0.9448%·법 9조 비율(소수 다섯째 반올림)
def breakeven(start, months, ratio=1.0):
    # 제때(start세) 받기 vs months개월 미루기, 같아지는 나이(명목, 두 쪽 다 같은 물가 조정)
    up = 1 + 0.006*months
    d = months/12
    # P*(t-start) = P*(1-r)*(t-start) + P*r*up*(t-start-d)  ->  r*(t-start) = r*up*(t-start-d)
    return start + up*d/(up-1)
LINE = 20_000_000/12
def kunbo(annual):
    inc = int(annual*0.5/12)
    hi = int(inc*0.0719)//10*10
    ltc_ratio = round(0.009448/0.0719, 4)
    ltc = int(hi*ltc_ratio)//10*10
    return hi, ltc, ltc_ratio
out=[]
for y in range(1,6):
    m=12*y; up=1+0.006*m
    out.append(f"[계산] {y}년 미룸: 연금 {up*100-100:.1f}% 늘어남 · 같아지는 나이 {breakeven(65,m):.2f}세 · 피부양자 선 넘지 않는 65세 연금(월) {LINE/up:,.0f}원")
P=1_400_000
full=P*1.36; part=P*0.5+P*0.5*1.36
out.append(f"[계산] 65세 월 140만원 · 5년 다 미루면 월 {full:,.0f}원 연 {full*12:,.0f}원(선 2천만원 넘음) · 절반만 미루면 65세부터 월 {P*0.5:,.0f}원, 70세부터 월 {part:,.0f}원 연 {part*12:,.0f}원(선 아래)")
hi,ltc,r=kunbo(full*12)
out.append(f"[계산] 다 미룬 쪽 지역보험료(재산 0·혼자 세대): 소득월액 {int(full*12*0.5/12):,}원 · 건보료 {hi:,}원 + 장기요양(비율 {r}) {ltc:,}원 = 월 {hi+ltc:,}원")
net=full-(hi+ltc)
t=(net*70-P*65)/(net-P)
out.append(f"[계산] 건보료 빼고 받는 돈 월 {net:,.0f}원이면 같아지는 나이 {t:.2f}세(건보료 없으면 {breakeven(65,60):.2f}세)")
for age in (85,89):
    A=P*12*(age-65); B=net*12*(age-70); C=P*0.5*12*(age-65)+P*0.5*1.36*12*(age-70)
    out.append(f"[계산] {age}세까지 받은 돈 합계: 제때 {A:,.0f} · 다 미룸(건보료 뺀 뒤) {B:,.0f} · 절반 미룸 {C:,.0f}")
r_max=(LINE/P-1)/0.36
out.append(f"[계산] 월 140만원이 선을 안 넘는 최대 연기 비율 {r_max*100:.1f}% → 법에 있는 비율 중 50%만 됨(60%면 월 {P*0.4+P*0.6*1.36:,.0f}원)")
print("\n".join(out)); open("calc_out.txt","w",encoding="utf-8").write("\n".join(out)+"\n")
