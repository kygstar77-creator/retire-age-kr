# cpi2pct1022 — ECOS 901Y009 소비자물가지수(총지수, 2020=100) 월별로 전년동월비를 직접 계산
import json, os, sys, statistics
sys.stdout.reconfigure(encoding='utf-8')
here = os.path.dirname(os.path.abspath(__file__))
rows = json.load(open(os.path.join(here, 'raw', 'ecos_cpi_m.json'), encoding='utf-8'))['StatisticSearch']['row']
idx = {r['TIME']: float(r['DATA_VALUE']) for r in rows}
def yoy(t):
    p = f'{int(t[:4])-1}{t[4:]}'
    return round((idx[t] / idx[p] - 1) * 100, 1) if p in idx else None
months = sorted(t for t in idx if '201601' <= t <= '202609')
ys = [(t, yoy(t)) for t in months]
n = len(ys)
print('기간', months[0], '~', months[-1], n, '달')
print('최근 12달', [(t, y) for t, y in ys[-12:]])
ge2 = [t for t, y in ys if y >= 2.0]; lt2 = [t for t, y in ys if y < 2.0]
print('2.0% 이상', len(ge2), ' 2.0% 미만', len(lt2))
near = [t for t, y in ys if 1.5 <= y <= 2.5]
print('1.5~2.5% (목표 ±0.5%p)', len(near), round(len(near)/n*100, 1), '%')
hi = [t for t, y in ys if y > 2.5]; lo = [t for t, y in ys if y < 1.5]
print('2.5% 넘음', len(hi), ' 1.5% 밑', len(lo))
eq = [t for t, y in ys if y == 2.0]; print('딱 2.0%', len(eq), eq)
# 해마다
for yr in range(2016, 2027):
    v = [y for t, y in ys if t.startswith(str(yr))]
    print(yr, '달', len(v), '평균', round(sum(v)/len(v), 2), '2.5%넘음', sum(1 for y in v if y > 2.5), '1.5밑', sum(1 for y in v if y < 1.5), '근처', sum(1 for y in v if 1.5 <= y <= 2.5))
# 2.5% 넘는 달이 이어진 구간
runs = []; cur = []
for t, y in ys:
    if y > 2.5: cur.append(t)
    else:
        if cur: runs.append(cur); cur = []
if cur: runs.append(cur)
print('2.5% 넘은 구간', [(r[0], r[-1], len(r)) for r in runs])
# 2% 이상 연속
runs2 = []; cur = []
for t, y in ys:
    if y >= 2.0: cur.append(t)
    else:
        if cur: runs2.append(cur); cur = []
if cur: runs2.append(cur)
print('2% 이상 구간', [(r[0], r[-1], len(r)) for r in runs2])
mx = max(ys, key=lambda x: x[1]); mn = min(ys, key=lambda x: x[1]); print('최고', mx, '최저', mn)
# 생활 단위: 같은 장바구니 값
for base in ('201601', '202001', '202109', '202509'):
    print(base, '→ 202609 지수', idx[base], idx['202609'], '배', round(idx['202609']/idx[base], 4), '100만원 →', round(1_000_000*idx['202609']/idx[base]))
# 2% 목표대로만 올랐다면(2016-01 기준, 월 복리 아니라 연 2%로 10년 8개월)
yrs = (2026 - 2016) + 8/12
print('연 2%로 10년 8개월', round(1.02**yrs, 4), '실제', round(idx['202609']/idx['201601'], 4))
# 2020년 평균 대비
a20 = statistics.mean(idx[f'2020{m:02d}'] for m in range(1, 13)); print('2020 평균', round(a20, 3))
# 연평균으로 바꾸면
r = (idx['202609']/idx['201601']) ** (1/yrs) - 1
print('2016.1~2026.9 연평균', round(r*100, 2), '%')
# 목표 ±0.5%p 밖 6달 이상 이어진 구간
out = []; cur = []
for t, y in ys:
    if y > 2.5 or y < 1.5: cur.append((t, y))
    else:
        if cur: out.append(cur); cur = []
if cur: out.append(cur)
print('밖 6달 이상', [(c[0][0], c[-1][0], len(c), '위' if c[0][1] > 2.5 else '아래') for c in out if len(c) >= 6])
# 9월은 상승률이 8월보다 낮지만 지수는 올랐다
print('지수 8월', idx['202608'], '9월', idx['202609'], '상승률 8월', yoy('202608'), '9월', yoy('202609'))
# 2025년 연평균 상승률(연간 지수 평균끼리) — 2026년 연금 인상률 2.1%와 대조
a24 = statistics.mean(idx[f'2024{m:02d}'] for m in range(1, 13)); a25 = statistics.mean(idx[f'2025{m:02d}'] for m in range(1, 13))
print('2025 연평균 상승률', round((a25/a24-1)*100, 2))
a26 = statistics.mean(idx[f'2026{m:02d}'] for m in range(1, 10)); a25_9 = statistics.mean(idx[f'2025{m:02d}'] for m in range(1, 10))
print('2026 1~9월 평균 지수 대비 작년 같은 기간', round((a26/a25_9-1)*100, 2))
# 예금 1천만원 1년, 기본금리 중앙 3.315%(finlife 2026-10-22, 은행 40상품)
p = 10_000_000; rate = 0.03315; it = round(p*rate); tax = int(it*0.14)//10*10 + int(int(it*0.14)//10*10*0.1)//10*10
print('이자', it, '세금(14%+지방1.4%, 10원 미만 버림)', tax, '세후', it - tax, '세후 금리', round((it-tax)/p*100, 2), '% · 9월 물가 2.9%만큼이면', round(p*0.029))
