# deprise1010 이자 계산 — 1억 1년 단리, 이자소득세 15.4%(소득세 14%+지방소득세 1.4%)
import sys; sys.stdout.reconfigure(encoding="utf-8")
import json
E = json.load(open('ecos_1010.json', encoding='utf-8'))
dep = dict((t, float(v)) for t, v, _ in E['dep1y_M'])
P = 100_000_000
def net(r): g = round(P * r / 100); tax = int(g * 0.14 // 10 * 10) + int(g * 0.014 // 10 * 10); return g, g - tax
for lab, r in (('2025-08 신규 1년 평균', dep['202508']), ('2026-08 신규 1년 평균', dep['202608']), ('2026-07 신규 1년 평균', dep['202607']), ('5대은행 최고 3.5', 3.5), ('하나 최고 3.6', 3.6), ('하나 기본 2.3', 2.3), ('저축은행 최고 4.07', 4.07)):
    g, n = net(r); print(f'{lab} {r}% → 세전 {g:,} / 세후 {n:,}')
g1, n1 = net(dep['202508']); g2, n2 = net(dep['202608'])
print('1년 사이 세후 차이', f'{n2 - n1:,}', '금리차 %.2f%%p' % (dep['202608'] - dep['202508']))
s = dict((d, float(v)) for d, v, _ in E['kdb1y_D']); k = dict((d, float(v)) for d, v, _ in E['ktb1y_D']); c = dict((d, float(v)) for d, v, _ in E['cd91_D'])
for d in ('20250829', '20260716', '20260827', '20260901', '20260929', '20261008'):
    print(d, '산금채1년', s.get(d), '국고채1년', k.get(d), 'CD91', c.get(d))
print('산금채 최고', max(s.items(), key=lambda x: x[1]))
# 월평균(일별 단순평균) — 예금 신규취급 월평균과 견주려고
for m in ('202508', '202607', '202608', '202609'):
    for nm, ser in (('산금채1년', s), ('국고채1년', k)):
        v = [x for d, x in ser.items() if d.startswith(m)]
        print(m, nm, '월평균 %.3f' % (sum(v) / len(v)), f'({len(v)}일)')
