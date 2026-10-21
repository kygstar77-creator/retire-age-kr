# 중간정산 뒤 퇴직: 따로 계산 vs 합쳐서 정산(소득세법 제148조①·시행령 제203조①③) — calc.py의 ret()을 그대로 쓴다
# 합산: 퇴직소득누계액·합산 근속연수로 세액 계산 → 중간정산 때 낸 세금을 뺀 만큼 퇴직 때 뗌. 지방소득세는 각 소득세의 10%(지방세법 제103조의13①)
from calc import ret
CASES = [('10년째 중간정산 1억 + 10년 뒤 퇴직 1억', 1e8, 10, 1e8, 10),
         ('15년째 중간정산 7,500만 + 15년 뒤 퇴직 7,500만', 7.5e7, 15, 7.5e7, 15),
         ('20년째 중간정산 1.5억 + 3년 뒤 퇴직 2,000만', 1.5e8, 20, 2e7, 3)]
def tot(t): return t + int(t * 0.1)
for name, a, na, b, nb in CASES:
    ta, tb = ret(a, na)['tax'], ret(b, nb)['tax']
    sep = tot(ta) + tot(tb)
    comb = ret(a + b, na + nb)['tax']
    final = comb - ta
    combined_total = tot(ta) + tot(final)
    print(f"{name}: 중간정산 때 {tot(ta):,} · 따로 계산한 퇴직 때 {tot(tb):,} → 따로 합계 {sep:,}")
    print(f"   합쳐서: {(a+b)/1e4:,.0f}만원·{na+nb}년 소득세 {comb:,} − 이미 낸 {ta:,} = 퇴직 때 소득세 {final:,} (지방 포함 {tot(final):,}) → 합계 {combined_total:,} · 차이 {sep-combined_total:,}")
