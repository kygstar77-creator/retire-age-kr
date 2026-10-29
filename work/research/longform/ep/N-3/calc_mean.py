# N-3 7장 '평균이 가운데보다 높은 이유' — 위쪽 몇 %를 빼면 평균이 얼마로 내려오나 (motion 10/29 18:58 요청, youtube-loop)
import json
d = json.load(open('../N-1/nts_pct.json', encoding='utf-8'))
N, G = d['N'], d['G_eok']
rows = d['rows']
mean = G / N * 1e4  # 만원
mid = next(r['avg_man'] for r in rows if r['k'] == '상위 50%')
print(f'전체 평균 {mean:,.0f}만 · 상위 50% 구간 평균(가운데) {mid:,}만 · 차이 {mean-mid:,.0f}만')
def cut(prefix_keys):
    n = sum(r['n'] for r in rows if r['k'] in prefix_keys)
    g = sum(r['pay_eok'] for r in rows if r['k'] in prefix_keys)
    return n, g
top1 = [r['k'] for r in rows[:10]]           # 천분위 0.1~1.0%
top10 = top1 + [r['k'] for r in rows[10:19]]  # 백분위 2~10%
for name, keys in (('상위 1%', top1), ('상위 10%', top10)):
    n, g = cut(keys)
    rest = (G - g) / (N - n) * 1e4
    share = (mean - rest) / (mean - mid) * 100
    print(f'{name}: {n:,}명 · 총급여 {g:,}억 · 평균 {g/n*1e4:,.0f}만 · 빼면 평균 {rest:,.0f}만 · 차이 중 {share:.0f}% 설명')
