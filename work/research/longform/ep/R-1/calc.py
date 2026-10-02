# R-1 사실표 계산 — 원자료 raw/collect_20261003.json만 쓴다. 이자 = 1억 × 연금리(1년 만기 일시지급 단리), 세금 = 이자 × 14% + 그 10%(지방소득세) = 15.4%
import json, sys, os, math
sys.stdout.reconfigure(encoding='utf-8')
D = os.path.dirname(os.path.abspath(__file__))
d = json.load(open(os.path.join(D, 'raw', 'collect_20261003.json'), encoding='utf-8'))
P = 100_000_000
def net(rate):
    gross = round(P * rate / 100); it = math.floor(gross * 0.14 / 10) * 10; lt = math.floor(it * 0.1 / 10) * 10
    return gross, it + lt, gross - it - lt
dep = {t: float(v) for t, v in d['정기예금1년_신규_M']}
print('[A] 은행 신규 정기예금(1년) 가중평균 %: 2025-08', dep['202508'], '2026-08', dep['202608'], '최고(2020~)', max(dep.items(), key=lambda x: x[1]), '최저', min(dep.items(), key=lambda x: x[1]))
for y in ['2020', '2021', '2022', '2023', '2024', '2025', '2026']:
    v = [dep[k] for k in dep if k.startswith(y)]; print('   ', y, '평균', round(sum(v) / len(v), 2), '개월', len(v))
def uniq(rows):
    s = {}
    for x in rows:
        k = (x['은행'], (x['상품'] or '').replace('\n', ' '))
        if x['금리'] is not None: s[k] = max(s.get(k, 0), x['금리'])
    return s
for g in ['은행', '저축은행']:
    s = uniq(d[f'finlife_예금12개월_{g}']); v = sorted(s.values()); n = len(v)
    print(f'[B-{g}] 12개월 정기예금 상품 {n}개(회사·상품명 기준, 기본금리 높은 쪽) 공시월 202609 · 최저 {v[0]} · 중앙 {v[n//2]} · 최고 {v[-1]} · 회사 수 {len({k[0] for k in s})}')
    top = sorted(s.items(), key=lambda x: -x[1])[:3]; print('    상위3', top)
c = {t: float(v) for t, v in d['CPI_M']}; inf = round((c['202608'] / c['202508'] - 1) * 100, 2)
print('[C] 소비자물가 2026-08', c['202608'], '2025-08', c['202508'], '1년 상승률 %', inf)
br = d['기준금리_D']
print('[D] 기준금리(일별 자료 끝)', br[-1])
print('\n[계산] 1억 · 1년 만기 일시지급(단리) · 세금 15.4%')
cases = [('1년 전 은행 평균(2025-08)', dep['202508']), ('지금 은행 평균(2026-08)', dep['202608']), ('은행 공시 최고(2026-09)', max(uniq(d['finlife_예금12개월_은행']).values())),
         ('저축은행 공시 최고(2026-09)', max(uniq(d['finlife_예금12개월_저축은행']).values())), ('2022-11 고점', dep['202211'])]
for name, r in cases:
    g, t, n = net(r); print(f'  {name} {r}% → 세전 {g:,} · 세금 {t:,} · 세후 {n:,} · 한 달로 나누면 {n//12:,} · 실질(세후 - 물가 {inf}%) {n - round(P*inf/100):,}')
print('  물가만큼 지키려면 필요한 이자(세후)', f'{round(P*inf/100):,}', '→ 세전 금리', round(inf / 0.846, 2), '%')
for r in [dep['202608'], 4.10]:
    print(f'  [경계] {r}%일 때 금융소득(이자) 1천만원 = 원금 {math.ceil(1e7/(r/100)):,} · 2천만원 = {math.ceil(2e7/(r/100)):,}')
g, t, n = net(dep['202608']); print('  [예금자보호] 1억 넣으면 만기 채권 합계', f'{P+g:,}', '→ 한도 1억 넘는 몫', f'{g:,}')
