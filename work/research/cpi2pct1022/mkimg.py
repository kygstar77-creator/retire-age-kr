# cpi2pct1022 그림 3장 — 숫자는 한국은행 ECOS 901Y009 소비자물가지수(raw/ecos_cpi_m.json)로 calc.py와 같은 식(전년동월비)
import os, json, datetime, sys
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt, matplotlib.dates as mdates
from matplotlib import font_manager as fm
F = r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work\video\public\fonts'
fm.fontManager.addfont(F + r'\pd500.ttf'); fm.fontManager.addfont(F + r'\pd700.ttf')
plt.rcParams['font.family'] = fm.FontProperties(fname=F + r'\pd500.ttf').get_name()
B = fm.FontProperties(fname=F + r'\pd700.ttf')
def Bs(n): return fm.FontProperties(fname=F + r'\pd700.ttf', size=n)
ORG, INK, SUB, GR, NAVY = '#EA580C', '#111827', '#4B5563', '#94A3B8', '#1E3A8A'
rows = json.load(open('raw/ecos_cpi_m.json', encoding='utf-8'))['StatisticSearch']['row']
idx = {r['TIME']: float(r['DATA_VALUE']) for r in rows}
def yoy(t): return round((idx[t] / idx[f'{int(t[:4])-1}{t[4:]}'] - 1) * 100, 1)
ms = sorted(t for t in idx if '201601' <= t <= '202609')
dt = lambda t: datetime.datetime(int(t[:4]), int(t[4:]), 15)
X = [dt(t) for t in ms]; Y = [yoy(t) for t in ms]
# 00 표지 — 짙은 초록 바탕, 큰 글 두 줄 + 2016~2026 물가상승률 선, 1.5~2.5% 띠
BG, WH, LG, BAND = '#12352E', '#FFFFFF', '#CDEBDD', '#2E6B5B'
fig = plt.figure(figsize=(10.8, 10.8), dpi=100); fig.patch.set_facecolor(BG)
fig.text(0.06, 0.875, '물가상승률 목표 2%', fontsize=70, fontproperties=B, color=WH)
fig.text(0.06, 0.765, '근처였던 달은 셋 중 하나', fontsize=56, fontproperties=B, color='#FDBA74')
ax = fig.add_axes([0.12, 0.14, 0.82, 0.52]); ax.set_facecolor(BG)
ax.axhspan(1.5, 2.5, color=BAND, zorder=0); ax.axhline(2, color=LG, lw=1.2, ls='--', zorder=1)
ax.plot(X, Y, color=LG, lw=3.2, zorder=2)
ax.plot([X[-1]], [Y[-1]], 'o', ms=16, color='#FDBA74', zorder=3)
ax.text(X[-1], Y[-1] + 0.6, '9월\n2.9%', ha='center', fontproperties=Bs(24), color='#FDBA74')
ax.text(dt('201604'), 2.65, '2% 근처(1.5~2.5%)', fontproperties=Bs(22), color=LG)
for v in (0, 2, 4, 6): ax.text(dt('201510'), v, f'{v}%', ha='right', va='center', fontproperties=Bs(20), color=LG)
ax.text(dt('202207'), 6.75, '6.3%', ha='center', fontproperties=Bs(20), color=LG)
ax.set_yticks([]); ax.set_ylim(-1, 7.2)
ax.set_xticks([dt('201601'), dt('201901'), dt('202201'), dt('202501')]); ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
ax.tick_params(colors=WH, labelsize=22, length=0)
for s_ in ('top', 'right', 'left'): ax.spines[s_].set_visible(False)
ax.spines['bottom'].set_color(LG)
fig.text(0.06, 0.03, '1년 전 같은 달보다 오른 비율 · 한국은행 경제통계시스템 소비자물가지수 2016.1~2026.9', fontsize=19, color=WH)
fig.savefig('pkg/img/00.png', dpi=100, facecolor=BG); fig.savefig('pkg/cover_100.png', dpi=100 * 100 / 1080, facecolor=BG); plt.close(fig)
# 01 해마다 — 근처·낮음·높음 달 수
yrs = list(range(2016, 2027))
lo = [sum(1 for t in ms if t.startswith(str(y)) and yoy(t) < 1.5) for y in yrs]
nr = [sum(1 for t in ms if t.startswith(str(y)) and 1.5 <= yoy(t) <= 2.5) for y in yrs]
hi = [sum(1 for t in ms if t.startswith(str(y)) and yoy(t) > 2.5) for y in yrs]
fig, ax = plt.subplots(figsize=(9, 7), dpi=100)
ax.bar(yrs, lo, color=GR, width=0.7, label='1.5% 밑')
ax.bar(yrs, nr, bottom=lo, color=NAVY, width=0.7, label='1.5~2.5%')
ax.bar(yrs, hi, bottom=[a + b for a, b in zip(lo, nr)], color=ORG, width=0.7, label='2.5% 넘음')
for y, a, b, c in zip(yrs, lo, nr, hi):
    if b: ax.text(y, a + b / 2, str(b), ha='center', va='center', fontproperties=Bs(13), color='white')
ax.set_xticks(yrs); ax.set_xticklabels([str(y)[2:] + '년' for y in yrs], fontsize=11); ax.set_yticks([0, 3, 6, 9, 12]); ax.tick_params(labelsize=12)
ax.set_ylabel('달 수', fontsize=12, color=SUB); ax.legend(loc='upper left', bbox_to_anchor=(0, 1.0), ncol=3, frameon=False, fontsize=13)
ax.set_ylim(0, 14)
for s in ('top', 'right'): ax.spines[s].set_visible(False)
fig.text(0.05, 0.93, '해마다 2% 근처에 든 달(남색 숫자)', fontsize=25, fontproperties=B, color=INK)
fig.text(0.05, 0.88, '129달 중 43달 · 낮은 해와 높은 해가 몇 해씩 이어짐', fontsize=16, color=SUB)
fig.text(0.05, 0.02, '한국은행 경제통계시스템 소비자물가지수 · 1년 전 같은 달 대비 · 2026년은 9월까지 · 직접 집계', fontsize=12, color='#6B7280')
fig.subplots_adjust(top=0.84, bottom=0.12)
fig.savefig('pkg/img/01.png', dpi=100); plt.close(fig)
# 02 2016년 1월 100만원어치 장바구니가 지금 얼마 — 실제 지수 대 해마다 2%
base = idx['201601']
V = [100 * idx[t] / base for t in ms]
T2 = [100 * 1.02 ** (((int(t[:4]) - 2016) * 12 + int(t[4:]) - 1) / 12) for t in ms]
fig, ax = plt.subplots(figsize=(9, 7), dpi=100)
ax.plot(X, T2, color=GR, lw=2.2, ls='--', label='해마다 딱 2%씩 올랐다면')
ax.plot(X, V, color=NAVY, lw=3, label='실제 소비자물가')
ax.plot([X[-1]], [V[-1]], 'o', ms=10, color=ORG); ax.text(X[-1], V[-1] + 1.2, '약 126만 5천원', ha='right', fontproperties=Bs(15), color=ORG)
ax.text(X[-1], T2[-1] - 4.2, '약 123만 5천원', ha='right', fontproperties=Bs(14), color=SUB)
ax.set_ylim(95, 132); ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f'{v:.0f}만원'))
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y')); ax.tick_params(labelsize=12)
ax.legend(loc='upper left', frameon=False, fontsize=13)
for s in ('top', 'right'): ax.spines[s].set_visible(False)
fig.text(0.05, 0.93, '2016년 1월 100만원어치, 지금은?', fontsize=25, fontproperties=B, color=INK)
fig.text(0.05, 0.88, '달마다 흔들렸지만 10년 8개월로 보면 한 해 2.2%쯤', fontsize=16, color=SUB)
fig.text(0.05, 0.02, '한국은행 경제통계시스템 소비자물가지수(2020=100) 2016.1 95.232 → 2026.9 120.43 · 직접 계산', fontsize=12, color='#6B7280')
fig.subplots_adjust(top=0.84, bottom=0.1)
fig.savefig('pkg/img/02.png', dpi=100); plt.close(fig)
print('ok', lo, nr, hi, round(V[-1], 2), round(T2[-1], 2))
