# jepipair1103 그림 3장 — 숫자는 raw/JEPI_chart_1103.json(야후 파이낸스 일별 종가·분배, 2026-11-03 받음) · 계산은 calc.py와 같음
import os, json, datetime as D
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib import font_manager as fm
F = r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work\video\public\fonts'
fm.fontManager.addfont(F + r'\pd500.ttf'); fm.fontManager.addfont(F + r'\pd700.ttf')
plt.rcParams['font.family'] = fm.FontProperties(fname=F + r'\pd500.ttf').get_name()
def Bf(s): return fm.FontProperties(fname=F + r'\pd700.ttf', size=s)
ORG, NAVY, GRAY = '#EA580C', '#1E3A8A', '#9CA3AF'
d = json.load(open('raw/JEPI_chart_1103.json'))['chart']['result'][0]
day = lambda t: D.datetime.fromtimestamp(t, D.UTC).date()
px = {day(t): c for t, c in zip(d['timestamp'], d['indicators']['quote'][0]['close']) if c}
dv = sorted((day(int(k)), v['amount']) for k, v in d['events']['dividends'].items())
days = sorted(px); s0 = min(x for x in days if x >= D.date(2021, 11, 1)); end = days[-1]
sh = 1000 / px[s0]          # 1,000만원어치(만원 단위, 환율 변화 뺌)
xs = [x for x in days if s0 <= x <= end]
val = [sh * px[x] for x in xs]
cum, c = [], 0.0; it = iter([t for t in dv if s0 < t[0] <= end]); nxt = next(it, None)
for x in xs:
    while nxt and nxt[0] <= x: c += sh * nxt[1]; nxt = next(it, None)
    cum.append(c)
re_sh, rv, it = sh, [], iter([t for t in dv if s0 < t[0] <= end]); nxt = next(it, None)
for x in xs:
    while nxt and nxt[0] <= x: re_sh += re_sh * nxt[1] / px[x]; nxt = next(it, None)
    rv.append(re_sh * px[x])
SRC = '야후 파이낸스 JEPI 일별 종가·분배(2021.11.1~2026.11.2) · 달러 기준 비율을 1,000만원으로 바꿈(환율 변화 뺌) · 세금 떼기 전 · 파이어맵 계산'

# 00 표지(차트 카드): 큰 글 + 주식 평가액 선 + 받은 돈 누적
fig = plt.figure(figsize=(9, 9), dpi=100); fig.patch.set_facecolor('white')
fig.text(0.05, 0.86, 'JEPI 분배금 꺼내 쓰면', fontproperties=Bf(64), color='#111827')
fig.text(0.05, 0.76, '5년 뒤 원금은?', fontproperties=Bf(64), color='#111827')
fig.text(0.05, 0.655, f'주식 {val[-1]:.0f}만원', fontproperties=Bf(52), color=NAVY)
fig.text(0.53, 0.655, f'+ 받은 돈 {cum[-1]:.0f}만원', fontproperties=Bf(36), color=ORG)
fig.text(0.06, 0.6, '1,000만원어치 사서 분배금을 다 꺼내 썼다면(세금 떼기 전)', fontsize=19, color='#374151')
ax = fig.add_axes([0.1, 0.15, 0.84, 0.40])
ax.axhline(1000, color=GRAY, lw=1.5, ls='--'); ax.text(D.date(2023, 3, 1), 1030, '처음 넣은 1,000만원', fontsize=14, color='#6B7280')
ax.plot(xs, val, color=NAVY, lw=3); ax.fill_between(xs, 0, cum, color=ORG, alpha=0.35, lw=0)
ax.text(xs[-1], val[-1] + 25, f'{val[-1]:.0f}', ha='right', fontproperties=Bf(18), color=NAVY)
ax.text(xs[-1], cum[-1] - 70, f'{cum[-1]:.0f}', ha='right', fontproperties=Bf(18), color=ORG)
ax.set_ylim(0, 1150); ax.set_yticks([0, 500, 1000]); ax.set_yticklabels(['0', '500만', '1,000만'], fontsize=13)
ax.xaxis.set_major_locator(mdates.YearLocator()); ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y')); ax.tick_params(axis='x', labelsize=13)
for s in ('top', 'right'): ax.spines[s].set_visible(False)
fig.text(0.1, 0.07, '파랑 = 가진 주식 값 · 주황 = 그동안 받은 분배금을 쌓은 것', fontsize=13, color='#4B5563')
fig.text(0.06, 0.03, SRC, fontsize=8.5, color='#6B7280')
fig.savefig('pkg/img/00.png', dpi=100); plt.close(fig)

# 01 꺼내 씀 vs 다시 넣음 (5년 뒤, 1,000만원 기준)
fig, ax = plt.subplots(figsize=(9, 7), dpi=100); fig.patch.set_facecolor('white')
ax.bar(0, val[-1], width=0.55, color=NAVY); ax.bar(0, cum[-1], bottom=val[-1], width=0.55, color=ORG)
ax.bar(1, rv[-1], width=0.55, color=NAVY)
ax.text(0, val[-1] / 2, f'주식\n{val[-1]:.0f}만', ha='center', va='center', fontproperties=Bf(20), color='white')
ax.text(0, val[-1] + cum[-1] / 2, f'받은 돈\n{cum[-1]:.0f}만', ha='center', va='center', fontproperties=Bf(20), color='white')
ax.text(0, val[-1] + cum[-1] + 25, f'합 {val[-1] + cum[-1]:,.0f}만원', ha='center', fontproperties=Bf(20), color='#111827')
ax.text(1, rv[-1] / 2, f'주식\n{rv[-1]:,.0f}만', ha='center', va='center', fontproperties=Bf(20), color='white')
ax.text(1, rv[-1] + 25, f'합 {rv[-1]:,.0f}만원', ha='center', fontproperties=Bf(20), color='#111827')
ax.axhline(1000, color=GRAY, lw=1.5, ls='--')
ax.set_xticks([0, 1]); ax.set_xticklabels(['분배금 꺼내 씀', '분배금 다시 넣음'], fontproperties=Bf(19))
ax.set_ylim(0, 1600); ax.set_yticks([0, 500, 1000, 1500]); ax.set_yticklabels(['0', '500만', '1,000만', '1,500만'], fontsize=13)
for s in ('top', 'right'): ax.spines[s].set_visible(False)
fig.text(0.06, 0.93, 'JEPI 1,000만원, 5년 뒤 (2021.11 → 2026.11)', fontproperties=Bf(24), color='#111827')
fig.text(0.06, 0.885, '점선 = 처음 넣은 1,000만원 · 세금 떼기 전', fontsize=14, color='#4B5563')
fig.text(0.06, 0.025, SRC, fontsize=8.5, color='#6B7280')
plt.subplots_adjust(left=0.12, right=0.95, top=0.83, bottom=0.12)
fig.savefig('pkg/img/01.png', dpi=100); plt.close(fig)

# 02 해마다 받은 분배금(1,000만원 기준, 다 채운 해만)
yrs = [2022, 2023, 2024, 2025]
amt = [sum(sh * a for t, a in dv if t.year == y) for y in yrs]
fig, ax = plt.subplots(figsize=(9, 7), dpi=100); fig.patch.set_facecolor('white')
ax.bar(range(4), amt, width=0.6, color=ORG)
for i, v in enumerate(amt): ax.text(i, v + 2, f'{v:.1f}만원', ha='center', fontproperties=Bf(20), color='#111827')
ax.set_xticks(range(4)); ax.set_xticklabels([f'{y}년' for y in yrs], fontproperties=Bf(18))
ax.set_ylim(0, 125); ax.set_yticks([])
for s in ('top', 'right', 'left'): ax.spines[s].set_visible(False)
fig.text(0.06, 0.93, '1,000만원어치가 한 해 동안 받은 분배금', fontproperties=Bf(24), color='#111827')
fig.text(0.06, 0.885, '같은 주식 수인데 해마다 달랐어요 · 세금 떼기 전', fontsize=14, color='#4B5563')
fig.text(0.06, 0.025, SRC, fontsize=8.5, color='#6B7280')
plt.subplots_adjust(left=0.08, right=0.95, top=0.83, bottom=0.1)
fig.savefig('pkg/img/02.png', dpi=100); plt.close(fig)
print(round(val[-1]), round(cum[-1]), round(rv[-1]), [round(a, 1) for a in amt], round(min(val)), xs[val.index(min(val))])
