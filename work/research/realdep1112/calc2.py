# 같은 계산을 '만기 날 돈으로' 뺄셈(받은 이자 − 같은 물건 값이 오른 만큼)으로 — 독자용
import json, sys
sys.stdout.reconfigure(encoding='utf-8')
d = json.load(open('raw/ecos_1112.json', encoding='utf-8')); dep1, cpi = d['dep1'], d['cpi']
P, T = 1e8, .846
print('받은 시각', d['got'])
for y in range(2012, 2026):
    a, b = f'{y}09', f'{y+1}09'
    r = dep1[a]; pi = cpi[b]/cpi[a]-1; nom = P*r/100*T; up = P*pi
    print(f'{y}.09 금리 {r:.2f}% 세후이자 {nom:,.0f} · 물가 {pi*100:.2f}% 물건값 오름 {up:,.0f} · 남음 {nom-up:+,.0f} · CPI {cpi[a]}→{cpi[b]}')
pi = cpi['202610']/cpi['202510']-1; r = dep1['202609']
print(f"2026.09 {r}% 세후 {P*r/100*T:,.0f} · 10월 물가 {pi*100:.2f}% 오름 {P*pi:,.0f} · 남음 {P*r/100*T-P*pi:+,.0f} · CPI {cpi['202510']}→{cpi['202610']}")
pi9 = cpi['202609']/cpi['202509']-1
print(f"  (9월 물가 {pi9*100:.2f}%면 남음 {P*r/100*T-P*pi9:+,.0f})")
print('세후 금리=물가 되는 금리(10월 물가):', round(pi*100/T, 2), '%')
