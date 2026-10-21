# 대조: 네이버 fchart KOSPI 일별 종가(raw/naver_kospi.xml)로 같은 셈 — 야후 값과 같은지 본다
import re, sys, collections
sys.stdout.reconfigure(encoding='utf-8')
rows = [(m[0], float(m[1])) for m in re.findall(r'item data="(\d{8})\|[^|]*\|[^|]*\|[^|]*\|([\d.]+)', open('raw/naver_kospi.xml', encoding='utf-8', errors='ignore').read())]
rows = [r for r in rows if r[0] < '20261021']
print('기간', rows[0][0], rows[-1][0], len(rows))
up = collections.Counter(); dn = collections.Counter(); u5 = collections.Counter()
for a, b in zip(rows, rows[1:]):
    r = (b[1] / a[1] - 1) * 100
    y = b[0][:4]
    if r >= 4: up[y] += 1
    if r >= 5: u5[y] += 1
    if r <= -4: dn[y] += 1
for y in sorted(set(up) | set(dn)): print(y, '+4%↑', up[y], '+5%↑', u5[y], '-4%↓', dn[y])
