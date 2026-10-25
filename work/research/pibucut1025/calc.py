# 피부양자 탈락 전환자 감액(시행규칙 부칙 제907호 제3조) 계산 — 원문 raw/국민건강보험법시행규칙.xml
# 예: 공적연금만 연 2,400만원, 재산 몫 없음, 혼자 사는 세대(전환으로 인상된 분 = 소득 몫 보험료 전부)
RATE = 0.0719                     # 시행령 44조 ① 1만분의 719
pension = 24_000_000
inc_month = pension * 0.5 / 12    # 시행규칙 44조 ②2·③ 연금 50%, 법 71조 ② 12로 나눔
prem = inc_month * RATE
print(f"소득월액 {inc_month:,.0f}원 · 소득 몫 보험료 {prem:,.0f}원/월")
# 감액률(달력 구간)
periods = [("2022-09","2023-10",0.8),("2023-11","2024-10",0.6),("2024-11","2025-10",0.4),("2025-11","2026-08",0.2)]
def months(a,b):
    y1,m1=map(int,a.split('-')); y2,m2=map(int,b.split('-')); return (y2-y1)*12+m2-m1+1
for a,b,r in periods:
    print(f"{a}~{b} {months(a,b)}개월 감액 {r:.0%} → 냄 {prem*(1-r):,.0f}원 (감액 {prem*r:,.0f}원)")
print(f"2026-09~ 감액 0% → 냄 {prem:,.0f}원")
def total_cut(start):
    s=0;n=0
    for a,b,r in periods:
        for k in range(months(a,b)):
            y,m=map(int,a.split('-')); m+=k; y+=(m-1)//12; m=(m-1)%12+1
            if f"{y:04d}-{m:02d}">=start: s+=prem*r; n+=1
    return n,s
for st in ["2022-09","2023-12","2024-12","2025-12"]:
    n,s=total_cut(st); print(f"{st} 탈락(그달분부터 지역) → 감액 받은 달 {n}개월 · 감액 합계 {s:,.0f}원")
print("2026-12 탈락 → 감액 0개월 (부칙 구간 2026-08 끝)")
# 기준선: 공적연금 월 166만 6,667원 = 연 2,000만원(별표1의2 1호 가목 2천만원 이하)
print(f"연 2,000만원 = 월 {20_000_000/12:,.0f}원")
