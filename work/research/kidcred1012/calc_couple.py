# kidcred1012 맞벌이 부부 자녀 공제 누가 받나 — 소득세법(2026.1.1 시행본, 법령 API 2026-10-10 조회 law_sodeuk.xml)
# 제47조 근로소득공제 · 제50조 기본공제 150만원 · 제55조 세율 · 제59조 근로소득세액공제 · 제59조의2 자녀세액공제(8세 이상 1명 25만·2명 55만·3명 이상 55만+40만씩)
# 제61조③ 세액공제 합계가 산출세액을 넘으면 넘는 금액은 없는 것으로 본다(근로소득세액공제를 먼저 빼고 자녀세액공제가 남은 세액까지만)
# 가정: 연봉=총급여, 비과세 없음, 4대보험 근로자 몫만 소득공제(국민연금 4.75%·상한 월 659만원 / 건강 3.595% / 장기요양 건강×13.14% / 고용 0.9%),
#       다른 소득공제·세액공제 없음, 자녀는 모두 8세 이상, 지방소득세 10% 포함
import sys; sys.stdout.reconfigure(encoding='utf-8')
MAN = 10_000
def earn_ded(p):
    for top, base, lo, r in [(500e4, 0, 0, .7), (1500e4, 350e4, 500e4, .4), (4500e4, 750e4, 1500e4, .15), (1e8, 1200e4, 4500e4, .05)]:
        if p <= top: return min(base + (p - lo) * r, 2000e4)
    return min(1475e4 + (p - 1e8) * .02, 2000e4)
def calc_tax(base):
    for top, b, lo, r in [(1400e4, 0, 0, .06), (5000e4, 84e4, 1400e4, .15), (8800e4, 624e4, 5000e4, .24), (1.5e8, 1536e4, 8800e4, .35)]:
        if base <= top: return b + (base - lo) * r
def credit59(tax, pay):
    c = tax * .55 if tax <= 130e4 else 71.5e4 + (tax - 130e4) * .3
    if pay <= 3300e4: lim = 74e4
    elif pay <= 7000e4: lim = max(74e4 - (pay - 3300e4) * 8 / 1000, 66e4)
    elif pay <= 1.2e8: lim = max(66e4 - (pay - 7000e4) / 2, 50e4)
    else: lim = max(50e4 - (pay - 1.2e8) / 2, 20e4)
    return min(c, lim)
def kidcr(n):
    if n == 0: return 0
    if n == 1: return 25e4
    return 55e4 + (n - 2) * 40e4
def tax(pay, kids):
    m = pay / 12
    nps = min(int(m // 1000 * 1000), 659e4) * .0475 * 12
    hi = m * .03595 * 12; ltc = hi * .1314; emp = m * .009 * 12
    base = max(0, pay - earn_ded(pay) - 150e4 * (1 + kids) - nps - hi - ltc - emp)
    t = calc_tax(base); t = max(0, t - credit59(t, pay))
    used = min(t, kidcr(kids))
    return (t - used) * 1.1, base, used, kidcr(kids)
def won(x): return f'{round(x):,}원'
def show(a, b, n):
    print(f'\n== 남편 연봉 {a:,}만원 · 아내 연봉 {b:,}만원 · 8세 이상 자녀 {n}명')
    best = None
    for k in range(n + 1):
        ta = tax(a * MAN, k); tb = tax(b * MAN, n - k); tot = ta[0] + tb[0]
        print(f'  남편 {k}명·아내 {n-k}명: 남편 세금 {won(ta[0])}(과표 {won(ta[1])}, 자녀공제 {won(ta[2])}/{won(ta[3])}) + 아내 {won(tb[0])}(과표 {won(tb[1])}, 자녀공제 {won(tb[2])}/{won(tb[3])}) = {won(tot)}')
        if best is None or tot < best[1]: best = (k, tot)
    print(f'  가장 적음: 남편 {best[0]}명 · 합계 {won(best[1])}')
show(7000, 4000, 2)
show(7000, 4000, 3)
show(6000, 2600, 2)
show(5000, 5000, 2)
show(8000, 3000, 3)
