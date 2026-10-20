# yen1021 계산 — 한국은행 ECOS 731Y001(원/100엔 매매기준율 일별) · 하나은행 10/20 고시(raw/hana_1020.html·t_wpfxd653_01i.do.html)
import json, os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
r = sorted((d, float(v)) for d, v, _ in json.load(open('raw/ecos_jpy_daily.json', encoding='utf-8')) if v and v != '-')
print('일수', len(r), r[0][0], '~', r[-1][0])
last = r[-1]; print('최근', last)
below = [x for x in r if x[0] < last[0] and x[1] <= last[1]]; print('이 값 이하 마지막', below[-1])
y26 = [x for x in r if x[0] >= '20260101']; hi = max(y26, key=lambda x: x[1]); print('2026 최고', hi, '차', round(hi[1] - last[1], 2), '비율', round((hi[1] - last[1]) / hi[1] * 100, 1))
print('1만엔 원화: 최고일', round(hi[1] * 100), '오늘', round(last[1] * 100), '차', round(hi[1] * 100) - round(last[1] * 100))
since08 = [x for x in r if x[0] >= '20080101']; mx = max(since08, key=lambda x: x[1]); print('2008~ 최고', mx)
ye = {}
for d, v in r: ye[d[:4]] = (d, v)
for y in ('2007', '2011', '2015', '2020', '2025'): print('연말', y, ye[y])
# 하나은행 10/20 21:00 580회차
base, buy, sell, abuy, asell = 840.91, 855.62, 826.20, 876.00, 780.00
n = 1000  # 10만엔 = 100엔 x 1000
print('10만엔 기준', round(base * n), '영업점 살 때', round(buy * n), '+', round((buy - base) * n), '공항 살 때', round(abuy * n), '+', round((abuy - base) * n), '공항-영업점', round((abuy - buy) * n))
print('영업점 사고 바로 팔면', round((buy - sell) * n), '비율', round((buy - sell) / buy * 100, 2))
print('살 때 기준율 대비', round((buy / base - 1) * 100, 2), '%')
print('ECOS vs 하나 기준율 차', round(base - last[1], 2))
u = sorted((d, float(v)) for d, v, _ in json.load(open('raw/ecos_usd_2026.json', encoding='utf-8')))
print('원달러 2026 최저', min(u, key=lambda x: x[1]), '최고', max(u, key=lambda x: x[1]))
