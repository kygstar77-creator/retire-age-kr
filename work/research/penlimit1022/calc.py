# 연금수령한도 = 평가액/(11-연차)*1.2 (소득세법 시행령 40조의2 ③3·④), 수익률 0% 가정
X=300_000_000
def path(start_year, X=X):
    R=X; rows=[]
    for k in range(start_year, 11):
        lim=R/(11-k)*1.2
        take=min(lim,R); rows.append((k,lim,take,R)); R-=take
    return rows,R
print("== A. 1년차부터 매년 한도만큼 꺼냄 (3억, 수익 0%)")
rows,R=path(1)
for k,lim,take,r in rows: print(f"연차{k:2d} 연초잔액 {r/1e4:,.0f}만 한도 {lim/1e4:,.0f}만 ({lim/X*100:.1f}% of 3억)")
print(f"11년차 남은 돈 {R/1e4:,.0f}만 ({R/X*100:.1f}%) — 한도 없음")
print("== B. 6년차부터 (2013.3.1 전 가입 또는 5년 늦게 개시)")
rows,R=path(6)
for k,lim,take,r in rows: print(f"연차{k:2d} 연초잔액 {r/1e4:,.0f}만 한도 {lim/1e4:,.0f}만")
print(f"11년차 남은 돈 {R/1e4:,.0f}만 ({R/X*100:.1f}%)")
print("== C. 첫해 한도 연차별 (3억)")
for k in range(1,11): print(k, f"{X/(11-k)*1.2/1e4:,.0f}만")
print("== D. 한도 안 1500만원 맞추려면: 연차1 한도가 1500만원이 되는 평가액", f"{1500e4*10/1.2/1e4:,.0f}만")
