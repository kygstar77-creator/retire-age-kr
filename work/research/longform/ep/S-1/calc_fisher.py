# 선반영(PRE4)·발표 날 방향별 한 달 뒤(A9) 차이가 우연으로 얼마나 나오나 — 피셔 정확 검정 양쪽(scipy 없이)
from math import comb
def fisher(a, b, c, d):
    r1, c1, n = a + b, a + c, a + b + c + d
    p = lambda x: comb(c1, x) * comb(n - c1, r1 - x) / comb(n, r1)
    p0 = p(a)
    return sum(p(x) for x in range(max(0, r1 - (n - c1)), min(r1, c1) + 1) if p(x) <= p0 * (1 + 1e-9))
print('PRE7 올라 있던 28번 중 내림 18 vs 안 올랐던 16번 중 내림 8: p =', round(fisher(18, 10, 8, 8), 3))
print('A10 발표 날 오른 17번 중 한 달 뒤 위 13 vs 내린 25번 중 위 12: p =', round(fisher(13, 4, 12, 13), 3))
