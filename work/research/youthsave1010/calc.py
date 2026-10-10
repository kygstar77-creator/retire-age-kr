# -*- coding: utf-8 -*-
"""청년도약계좌 유지 vs 청년미래적금 갈아타기 — 정부기여금만 비교 (이자 제외).
숫자 출처는 facts.txt 참고. 은행 금리는 확인 안 함 → 이자는 계산에 넣지 않는다.
실행: py -3.12 calc.py > calc_out.txt
"""
import sys
sys.stdout.reconfigure(encoding="utf-8")

M = 500_000  # 월 납입액 50만원 (미래적금 월 한도)

# ── 청년미래적금 (서민금융진흥원 fill4young, 금융위 2026-10-07 보도자료) ──
FUT_MONTHS = 36
FUT = {  # 이름: (비율, 월 지급한도)
    "일반형 6%": (0.06, 30_000),
    "우대형 12%": (0.12, 60_000),
    "기여금 미대상(총급여 6천만 초과~7,500만)": (0.0, 0),
}

def fut_monthly(rate, cap, m=M):
    return min(round(m * rate), cap)

# ── 청년도약계좌 ('25.1월 납입분부터, 서민금융진흥원 도약계좌 페이지·금융위 2024-12-26 보도자료) ──
# (구간Ⅰ 비율, 구간Ⅰ 상한 납입액, 구간Ⅱ 비율[상한~70만])
LEAP_MONTHS = 60
LEAP = {
    "총급여 2,400만 이하": (0.060, 400_000, 0.03),
    "총급여 3,600만 이하": (0.046, 500_000, 0.03),
    "총급여 4,800만 이하": (0.037, 600_000, 0.03),
    "총급여 6,000만 이하": (0.030, 700_000, 0.00),
    "총급여 6,000만 초과~7,500만": (0.0, 0, 0.0),
}

def leap_monthly(r1, lim, r2, m=M):
    a = min(m, lim) * r1
    b = max(0, min(m, 700_000) - lim) * r2
    return round(a + b)

def won(x):
    return f"{x:,.0f}원"

print("월 납입 50만원 가정 · 정부기여금만(이자·우대금리 제외, 금리 확인 안 함)")
print()
print("[검산] 도약계좌 월 70만 납입 시 월 기여금 → 공식표 33,000/29,000/25,200/21,000과 일치해야 함")
for k, v in LEAP.items():
    print(f"  {k}: {won(leap_monthly(*v, m=700_000))}")
print("[검산] 미래적금 3년 50만 꽉 채움 → 보도자료 일반형 108만·우대형 216만과 일치해야 함")
for k, (r, c) in FUT.items():
    print(f"  {k}: {won(fut_monthly(r, c) * FUT_MONTHS)}")
print()

print("A. 청년미래적금 36개월 (원금 1,800만원)")
for k, (r, c) in FUT.items():
    mm = fut_monthly(r, c)
    print(f"  {k}: 월 {won(mm)} × 36 = {won(mm * FUT_MONTHS)}")
print()

print("B. 청년도약계좌 60개월, 같은 50만원 (원금 3,000만원)")
for k, v in LEAP.items():
    mm = leap_monthly(*v)
    print(f"  {k}: 월 {won(mm)} × 60 = {won(mm * LEAP_MONTHS)}   (36개월분이면 {won(mm * 36)})")
print()

print("C. 같은 사람이 이미 도약계좌에 n개월 납입한 상태에서 비교 (기여금 합계)")
print("   유지 = 도약 60개월 전체 기여금(원금 3,000만)")
print("   갈아타기 = 도약 n개월분 기여금(특별중도해지로 지급) + 미래 36개월 기여금(원금 n×50만 + 1,800만)")
print("   ※ 가정: 특별중도해지 때 도약 n개월분 기여금 전액 지급(원문은 '정부기여금이 지급'까지만, 전액 명시 확인 안 함)")
print("   ※ 도약 기여금은 '25.1월 이후 기준표로 n개월 모두 계산(그 이전 납입분은 옛 기준이라 실제와 다를 수 있음)")
print("   ※ 소득구간·미래적금 유형 조합은 본인 자격에 따라 다름. 우대형은 중소기업 재직(총급여 3,600만 이하)·신규취업·연매출 1억 이하 소상공인")
pairs = [
    ("총급여 2,400만 이하", "일반형 6%"), ("총급여 2,400만 이하", "우대형 12%"),
    ("총급여 3,600만 이하", "일반형 6%"), ("총급여 3,600만 이하", "우대형 12%"),
    ("총급여 4,800만 이하", "일반형 6%"),
    ("총급여 6,000만 이하", "일반형 6%"),
    ("총급여 6,000만 초과~7,500만", "기여금 미대상(총급여 6천만 초과~7,500만)"),
]
for n in (12, 24, 36):
    print(f"  ── 도약 {n}개월 납입 후")
    for lk, fk in pairs:
        lm = leap_monthly(*LEAP[lk]); fm = fut_monthly(*FUT[fk])
        keep = lm * LEAP_MONTHS
        switch = lm * n + fm * FUT_MONTHS
        keep_months_left = LEAP_MONTHS - n
        print(f"    {lk} → 미래 {fk.split('(')[0]}: 유지 {won(keep)} (남은 {keep_months_left}개월) | "
              f"갈아타기 {won(switch)} (끝나는 시점 지금부터 36개월) | 차이 {won(switch - keep)}")
print()
print("D. 참고만(계산 근거로 쓰지 말 것): '27년 예산안 우대형 15%·25%(비수도권 중소기업 재직자)는 국회 확정 전.")
print("   확정 시 기존 가입자 소급 예정(보도자료). 월 지급한도는 확인 안 함 → 금액 계산 안 함.")
