# 월급 실수령 2025년 12월 → 2026년 1월(요율) → 3월(간이세액표) → 7월(연금 상한) 비교
# 표: 별표2 원문(옛 2024.2.29 개정본 = 시행령 MST 282973, 새 2026.2.27 개정본 = calc-salary/byl2-2026-02-27.txt)
import re, sys
sys.stdout.reconfigure(encoding='utf-8')
def parse(path):
    rows = {}
    for line in open(path, encoding='utf-8'):
        cells = [c.strip() for c in line.split('│')]
        cells = [c for c in cells if c != '']
        if len(cells) >= 13 and re.fullmatch(r'[\d,]+', cells[0]) and re.fullmatch(r'[\d,]+', cells[1]):
            f = int(cells[0].replace(',', '')); vals = []
            for c in cells[2:13]:
                vals.append(0 if c in ('-', '') else int(c.replace(',', '')))
            rows[f] = (int(cells[1].replace(',', '')), vals)
    return rows
OLD = parse('byl2_old.txt'); NEW = parse('../calc-salary/byl2-2026-02-27.txt')
def tax(tbl, taxable, fam=1):
    k = taxable // 1000
    for f in sorted(tbl):
        to, v = tbl[f]
        if f <= k < to: return v[fam-1]
    raise ValueError(k)
f10 = lambda n: int(n // 10 * 10)
def net(annual, period, fam=1, meal=200000, kids=0):
    from fractions import Fraction as F
    if period == '2025-12': pr, cap, hr, ltc, tb, kc = F(45,1000), 6370000, F(3545,100000), F(1295,10000), OLD, (12500, 29160, 25000)
    elif period == '2026-01': pr, cap, hr, ltc, tb, kc = F(475,10000), 6370000, F(3595,100000), F(1314,10000), OLD, (12500, 29160, 25000)
    elif period == '2026-03': pr, cap, hr, ltc, tb, kc = F(475,10000), 6370000, F(3595,100000), F(1314,10000), NEW, (20830, 45830, 33330)
    else: pr, cap, hr, ltc, tb, kc = F(475,10000), 6590000, F(3595,100000), F(1314,10000), NEW, (20830, 45830, 33330)
    m = F(annual, 12); m = int(m); taxable = m - meal
    base = min(max(int(taxable // 1000 * 1000), 410000 if period >= '2026-07' else 400000), cap)
    nps = f10(base * pr); h = f10(taxable * hr); l = f10(h * ltc); e = f10(taxable * F(9,1000))
    it = tax(tb, taxable, fam)
    if kids: it = max(0, it - (kc[0] if kids == 1 else kc[1] + (kids-2)*kc[2]))
    lt = f10(it * 0.1)
    return dict(nps=nps, health=h, ltc=l, emp=e, tax=it, local=lt, net=int(m - nps - h - l - e - it - lt))
if __name__ == '__main__':
    print('표 행수', len(OLD), len(NEW))
    for a in (30_000_000, 40_000_000, 50_000_000, 60_000_000, 80_000_000, 100_000_000):
        for fam, kids in ((1,0), (3,1), (4,2)):
            r = {p: net(a, p, fam, kids=kids) for p in ('2025-12', '2026-01', '2026-03', '2026-07')}
            print(f'연봉 {a//10000}만 가족{fam} 자녀{kids}', ' | '.join(f"{p} 실{r[p]['net']:,} 연금{r[p]['nps']:,} 건{r[p]['health']:,} 요{r[p]['ltc']:,} 세{r[p]['tax']:,}" for p in r))
            print('    차이 12월→1월', r['2026-01']['net'] - r['2025-12']['net'], ' 1월→3월', r['2026-03']['net'] - r['2026-01']['net'], ' 3월→7월', r['2026-07']['net'] - r['2026-03']['net'], ' 12월→7월 합', r['2026-07']['net'] - r['2025-12']['net'])
