# -*- coding: utf-8 -*-
"""P-1 국민연금 받는 나이 — 같은 사람 세 길(조기·제때·연기) + 60대 초반 일하는 사람 감액 문턱.

실행: py -3.12 work/research/longform/ep/P-1/calc.py > work/research/longform/ep/P-1/calc_out.txt
근거는 전부 facts.txt 번호. 예시 월액 100만원은 '가정'(화면에 가정 표시).
단순화(말에 그대로 밝힌다): 물가 재평가는 세 길에 똑같이 붙으므로 비율·손익분기 나이는 실질 기준으로 같다.
세금·건보료·부양가족연금액은 넣지 않는다.
"""
A_2026 = 3_193_511            # [F3] 2026 적용 A값, 국민연금공단
BASE = 1_000_000              # 가정: 제때 받으면 월 100만원
EARLY = {1: 940, 2: 880, 3: 820, 4: 760, 5: 700}   # [F2] 제63조② 1천분의
DELAY_PER_MONTH = 6           # [F2] 제62조② 1천분의 6
LIFE65 = {'남': 19.5, '여': 23.7}  # [F5] 2024 생명표 65세 기대여명(보도, 원문 확인 필요)

# [F1] 부칙 제8541호 제8조 — 출생연도별 정상 수령 나이
def normal_age(y):
    if y <= 1956: return 61
    if y <= 1960: return 62
    if y <= 1964: return 63
    if y <= 1968: return 64
    return 65


def cum(monthly, start, t):
    """t세(만)까지 받은 누적 원금(원), start세부터."""
    return max(0.0, (t - start)) * 12 * monthly


def breakeven(m1, s1, m2, s2):
    """일찍 적게(m1, s1) vs 늦게 많이(m2, s2) 누적이 같아지는 나이."""
    # m1(t-s1) = m2(t-s2)  → t = (m2 s2 - m1 s1)/(m2-m1)
    return (m2 * s2 - m1 * s1) / (m2 - m1)


def cut(income_after_deduction):
    """[F4] 제63조의2(2025.12.16 개정, 2026-06-17 시행) 월 감액. 상한 노령연금액 1/2."""
    e = income_after_deduction - A_2026
    if e < 2_000_000: c = 0
    elif e < 3_000_000: c = 150_000 + (e - 2_000_000) * 0.15
    elif e < 4_000_000: c = 300_000 + (e - 3_000_000) * 0.20
    else: c = 500_000 + (e - 4_000_000) * 0.25
    return min(c, BASE / 2), e


def wage_deduction(total):
    """[F6] 소득세법 제47조① 근로소득공제(상한 2천만원)."""
    if total <= 5_000_000: d = total * 0.7
    elif total <= 15_000_000: d = 3_500_000 + (total - 5_000_000) * 0.4
    elif total <= 45_000_000: d = 7_500_000 + (total - 15_000_000) * 0.15
    elif total <= 100_000_000: d = 12_000_000 + (total - 45_000_000) * 0.05
    else: d = 14_750_000 + (total - 100_000_000) * 0.02
    return min(d, 20_000_000)


def pay_for_income(target_monthly_after):
    """공제 뒤 월 근로소득금액이 target이 되는 세전 연봉(이분법)."""
    lo, hi = 0.0, 1e9
    for _ in range(200):
        mid = (lo + hi) / 2
        if (mid - wage_deduction(mid)) / 12 < target_monthly_after: lo = mid
        else: hi = mid
    return hi


print('== 1. 출생연도별 세 길 (월 100만원 가정, 5년 당김/제때/5년 미룸) ==')
for y in range(1964, 1970):
    n = normal_age(y)
    early_m = BASE * EARLY[5] / 1000
    delay_m = BASE * (1 + DELAY_PER_MONTH * 60 / 1000)
    be1 = breakeven(early_m, n - 5, BASE, n)
    be2 = breakeven(BASE, n, delay_m, n + 5)
    print(f'{y}년생 제때 {n}세 | 조기 {n-5}세 월 {early_m:,.0f}원 | 연기 {n+5}세 월 {delay_m:,.0f}원 | '
          f'조기=제때 같아지는 나이 {be1:.2f}세 | 제때=연기 {be2:.2f}세')

print()
print('== 2. 1년씩 당기기/미루기 손익분기 (1969년생, 제때 65세) ==')
n = 65
for k in range(1, 6):
    em = BASE * EARLY[k] / 1000
    dm = BASE * (1 + DELAY_PER_MONTH * 12 * k / 1000)
    print(f'{k}년 당김 월 {em:,.0f}원 → 제때와 같아지는 나이 {breakeven(em, n-k, BASE, n):.2f}세 | '
          f'{k}년 미룸 월 {dm:,.0f}원 → 같아지는 나이 {breakeven(BASE, n, dm, n+k):.2f}세')

print()
print('== 3. 기대여명까지 누적(1969년생, 65세 생존 가정, 기대여명 [F5]) ==')
for sex, le in LIFE65.items():
    t = 65 + le
    a = cum(BASE * 0.7, 60, t); b = cum(BASE, 65, t); c = cum(BASE * 1.36, 70, t)
    print(f'{sex} {t:.1f}세까지: 조기 {a:,.0f}원 · 제때 {b:,.0f}원 · 연기 {c:,.0f}원 · '
          f'제때-조기 {b-a:+,.0f}원 · 연기-제때 {c-b:+,.0f}원')

print()
print('== 4. 제때 받으며 일할 때 감액(제63조의2, 월 100만원 가정) ==')
print(f'감액 시작 문턱: 공제 뒤 월 소득 A값 {A_2026:,}원 + 200만원 = {A_2026 + 2_000_000:,}원')
th = pay_for_income(A_2026 + 2_000_000)
print(f'근로소득만이면 세전 연봉 {th:,.0f}원(월 {th/12:,.0f}원)부터 감액 — 근로소득공제 [F6] 역산')
for after in (3_000_000, 4_000_000, 5_000_000, 5_193_511, 6_000_000, 7_000_000, 8_000_000):
    c, e = cut(after)
    pay = pay_for_income(after)
    print(f'공제 뒤 월 {after:,}원(세전 월 약 {pay/12:,.0f}원): 초과 {e:,.0f}원 → 월 감액 {c:,.0f}원')

print()
print('== 5. 옛 법(1·2호 살아 있을 때)과 차이 — 확인 안 함, 옛 조문 원문 받기 전 숫자 쓰지 않음 ==')
