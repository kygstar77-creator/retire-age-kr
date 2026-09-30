# 연봉 실수령 손검산 — JS(src/utils/salaryNet.js)와 따로, 법령 API 별표 원문 글자를 직접 읽어 Fraction으로 계산한다.
# 실행: py -3.12 work/research/calc-salary/handcheck.py <별표2 원문 txt>
# 원문 txt는 법령 API(소득세법시행령) 별표단위 '근로소득 간이세액표' 별표내용을 CDATA 벗겨 저장한 것.
import sys, re
from fractions import Fraction as F

src = open(sys.argv[1], encoding='utf-8').read()
num = lambda s: 0 if s.strip() == '-' else int(s.replace(',', ''))
rows = []
for line in src.splitlines():
    c = [x.strip() for x in line.split('│')]
    if len(c) >= 14 and re.fullmatch(r'[\d,]+', c[1]) and re.fullmatch(r'[\d,]+', c[2]) and all(re.fullmatch(r'[\d,]+|-', v) for v in c[3:14]):
        rows.append((num(c[1]) * 1000, num(c[2]) * 1000, [num(v) for v in c[3:14]]))
top = next([num(v) for v in c[2:13]] for c in ([x.strip() for x in l.split('│')] for l in src.splitlines()) if len(c) >= 13 and c[1] == '10,000천원')

def table(m, fam):
    if m < rows[0][0]:
        return F(0)
    for lo, hi, v in rows:
        if lo <= m < hi:
            return F(v[fam - 1])
    b = F(top[fam - 1]); o = lambda L: F(m - L * 1000)
    if m == 10_000_000: return b
    if m <= 14_000_000: return b + o(10000) * F(98, 100) * F(35, 100) + 25000
    if m <= 28_000_000: return b + 1397000 + o(14000) * F(98, 100) * F(38, 100)
    raise ValueError('손검산 범위 밖')

f10 = lambda x: (int(x) // 10) * 10  # x >= 0
def kid(n): return 0 if n == 0 else 20830 if n == 1 else 45830 + (n - 2) * 33330

def calc(annual, nontax, fam, kids, ratio):
    monthly = annual // 12
    t = monthly - min(nontax, monthly)
    base = min(6_590_000, max(410_000, t // 1000 * 1000))
    pension = f10(F(base) * F(475, 10000))
    health = f10(F(t) * F(3595, 100000))
    ltc = f10(F(health) * F(1314, 10000))
    emp = f10(F(t) * F(9, 1000))
    it = f10(max(0, f10(table(t, fam)) - kid(kids)) * F(ratio, 100))
    lt = f10(F(it) / 10)
    ded = pension + health + ltc + emp + it + lt
    return dict(monthly=monthly, taxable=t, pension=pension, health=health, ltc=ltc, employment=emp, incomeTax=it, localTax=lt, net=monthly - ded)

# 장기요양 비율 확인: 0.9448% ÷ 7.19% 를 소수점 다섯째자리에서 반올림
r = F(9448, 1000000) / F(719, 10000)
print('장기요양 비율', float(r), '→', round(float(r), 4))

CASES = [
    ('A 연봉 4,000만 · 비과세 20만 · 본인 1 · 자녀 0 · 100%', (40_000_000, 200_000, 1, 0, 100)),
    ('B 연봉 3,000만 · 비과세 20만 · 1 · 0 · 100%', (30_000_000, 200_000, 1, 0, 100)),
    ('C 연봉 6,000만 · 비과세 20만 · 가족 4 · 자녀 2 · 100%', (60_000_000, 200_000, 4, 2, 100)),
    ('D 연봉 1억 · 비과세 20만 · 1 · 0 · 80% (국민연금 상한)', (100_000_000, 200_000, 1, 0, 80)),
    ('E 연봉 1억 5천 · 비과세 0 · 2 · 1 · 120% (월 1,000만 초과 식)', (150_000_000, 0, 2, 1, 120)),
    ('F 연봉 2,400만 · 비과세 20만 · 1 · 0 · 100% (세액 0 구간 경계 근처)', (24_000_000, 200_000, 1, 0, 100)),
]
for name, a in CASES:
    print(name, calc(*a))
