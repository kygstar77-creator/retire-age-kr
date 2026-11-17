# divsep1117 그림 2장 — 숫자는 calc.py(조특법 104조의27·소득세법 55·56·62조 직접 계산)
import os, sys
os.chdir(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, '.')
from calc import row
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
F = r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work\video\public\fonts'
fm.fontManager.addfont(F + r'\pd500.ttf'); fm.fontManager.addfont(F + r'\pd700.ttf')
plt.rcParams['font.family'] = fm.FontProperties(fname=F + r'\pd500.ttf').get_name()
def Bs(n): return fm.FontProperties(fname=F + r'\pd700.ttf', size=n)
ORG, INK, SUB, BLU, GRN, LG, RED = '#EA580C', '#111827', '#4B5563', '#2563EB', '#059669', '#CBD5E1', '#DC2626'
# 01: 다른 소득별, 분리과세 신청하면 더 내는(+)·덜 내는(−) 돈 — 배당 3천만원·1억원
os_ = [0, 2000, 4000, 6000, 8000, 10000, 12000, 15000]
fig, ax = plt.subplots(figsize=(9, 5.6), dpi=100)
for d, c, n in [(3000, ORG, '배당 3천만원'), (10000, BLU, '배당 1억원')]:
    v = [1.1 * (row(o, d)[1] - row(o, d)[0]) for o in os_]
    ax.plot(range(len(os_)), v, color=c, lw=3.2, marker='o', ms=6)
    ax.text(len(os_) - 0.8, v[-1], n, va='center', fontproperties=Bs(14), color=c)
    ax.text(-0.15, v[0] + (25 if d == 3000 else 0), f'+{v[0]:.0f}만원', ha='right', va='center', fontproperties=Bs(13), color=c)
ax.axhline(0, color=SUB, lw=1.2)
ax.text(0.0, -450, '0 아래 = 분리과세가 이득', fontproperties=Bs(13), color=GRN)
ax.text(0.2, 560, '0 위 = 신청하면 더 냄', fontproperties=Bs(13), color=RED)
ax.set_xticks(range(len(os_))); ax.set_xticklabels(['0' if o == 0 else (f'{o//10000}억' if o % 10000 == 0 else (f'{o/10000:.1f}억' if o > 10000 else f'{o//1000}천')) for o in os_], fontproperties=Bs(13), color=SUB)
ax.set_xlabel('다른 소득 과세표준(만원)', fontproperties=Bs(12), color=SUB)
ax.set_xlim(-1.6, 9.3); ax.set_yticks([])
for s in ['top', 'right', 'left']: ax.spines[s].set_visible(False)
ax.spines['bottom'].set_color(LG)
fig.suptitle('분리과세 신청하면 세금이 얼마나 달라질까', fontproperties=Bs(23), color=INK, x=0.04, ha='left', y=0.96)
fig.text(0.04, 0.015, '고배당기업 배당만 있다고 가정 · 지방소득세 포함 · 조특법 104조의27·소득세법 62조 직접 계산', fontproperties=Bs(11), color=SUB)
plt.subplots_adjust(left=0.13, right=0.97, top=0.86, bottom=0.17)
fig.savefig('pkg/img/01.png'); plt.close(fig)
# 02: 분리과세가 싸지기 시작하는 다른 소득 과세표준
rows = [('배당 3천만원', 8028, '약 8천만원'), ('배당 5천만원', 6482, '약 6,500만원'), ('배당 1억원', 3691, '약 3,700만원')]
fig, ax = plt.subplots(figsize=(9, 5.6), dpi=100)
for i, (n, y, t) in enumerate(rows):
    ax.barh(2 - i, y, color=[ORG, '#F59E0B', BLU][i], height=0.55)
    ax.text(y + 150, 2 - i, t, va='center', fontproperties=Bs(19), color=INK)
ax.set_yticks(range(3)); ax.set_yticklabels([r[0] for r in rows][::-1], fontproperties=Bs(17), color=INK)
ax.set_xlim(0, 11000); ax.set_xticks([])
for s in ['top', 'right', 'bottom']: ax.spines[s].set_visible(False)
ax.spines['left'].set_color(LG)
fig.suptitle('다른 소득이 이만큼 넘어야 분리과세가 싸요', fontproperties=Bs(23), color=INK, x=0.04, ha='left', y=0.96)
fig.text(0.04, 0.10, '다른 소득이 없으면 배당 약 1억 9천만원부터', fontproperties=Bs(15), color=RED)
fig.text(0.04, 0.03, '다른 소득 = 근로·사업·연금소득 과세표준 · 다른 금융소득·공제 없다고 가정 · 직접 계산', fontproperties=Bs(11), color=SUB)
plt.subplots_adjust(left=0.2, right=0.97, top=0.86, bottom=0.2)
fig.savefig('pkg/img/02.png'); plt.close(fig)
