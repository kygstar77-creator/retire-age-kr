# wolsegong1027 그림 3장 — 숫자는 calc.py (조세특례제한법 제95조의2, 현행 한도 1,000만원 / 정부안 1,200만원)
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import font_manager as fm
F = r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work\video\public\fonts'
fm.fontManager.addfont(F + r'\pd500.ttf'); fm.fontManager.addfont(F + r'\pd700.ttf')
plt.rcParams['font.family'] = fm.FontProperties(fname=F + r'\pd500.ttf').get_name()
def Bs(n): return fm.FontProperties(fname=F + r'\pd700.ttf', size=n)
ORG, INK, SUB, GR = '#EA580C', '#111827', '#4B5563', '#94A3B8'
BG, WH, LG = '#0F3B44', '#FFFFFF', '#CFE6EA'
def credit(m, cap, rate): return min(m * 12, cap) * rate
# 00 표지 — 월 100만원 세 경우 공제액 지금 vs 정부안
fig = plt.figure(figsize=(10.8, 10.8), dpi=100); fig.patch.set_facecolor(BG)
fig.text(0.06, 0.865, '월세 세액공제', fontproperties=Bs(76), color=WH)
fig.text(0.06, 0.765, '월 100만원이면 +30만원', fontproperties=Bs(54), color='#FB923C')
fig.text(0.06, 0.695, '한도 1,000 → 1,200만원 · 정부안(국회 확정 전)', fontsize=28, color=LG)
ax = fig.add_axes([0.06, 0.13, 0.88, 0.5]); ax.set_facecolor(BG)
bars = [('지금\n(한도 1,000)', credit(100, 1000, .15), LG), ('정부안\n(한도 1,200)', credit(100, 1200, .15), '#FB923C')]
for i, (lab, v, c) in enumerate(bars):
    ax.bar(i, v, color=c, width=0.5)
    ax.text(i, v + 6, f'{v:.0f}만원', ha='center', fontproperties=Bs(32), color=c)
    ax.text(i, -8, lab, ha='center', va='top', fontsize=24, color=WH, linespacing=1.4)
ax.set_ylim(-48, 215); ax.set_xlim(-0.7, 1.7); ax.axis('off')
fig.text(0.06, 0.035, '월세 월 100만원 · 공제율 15% · 조세특례제한법 제95조의2', fontsize=24, color=WH)
fig.savefig('pkg/img/00.png', dpi=100, facecolor=BG); fig.savefig('pkg/cover_100.png', dpi=100 * 100 / 1080, facecolor=BG); plt.close(fig)
# 01 월세별 공제액 선 — 지금 vs 정부안 (15%)
fig, ax = plt.subplots(figsize=(9, 6.6), dpi=100)
ms = np.arange(60, 111, 1)
ax.plot(ms, [credit(m, 1000, .15) for m in ms], color=GR, lw=3.5, label='지금 (한도 1,000만원)')
ax.plot(ms, [credit(m, 1200, .15) for m in ms], color=ORG, lw=3.5, label='정부안 (한도 1,200만원)')
for m in (70, 90, 100):
    ax.text(m, credit(m, 1200, .15) + 6, f'{credit(m,1200,.15):.0f}', ha='center', fontsize=13, color=INK)
ax.axvline(1000 / 12, color=GR, ls=':', lw=1.5); ax.text(1000 / 12 + 0.5, 112, '월 83.3만원', fontsize=13, color=SUB)
ax.set_xlabel('월세 (만원/월)', fontsize=14); ax.set_yticks([]); ax.set_ylim(90, 200)
for s in ('top', 'right', 'left'): ax.spines[s].set_visible(False)
ax.legend(frameon=False, fontsize=14, loc='upper left')
fig.text(0.05, 0.92, '월세별 세액공제액 (만원)', fontproperties=Bs(22), color=INK)
fig.text(0.05, 0.02, '공제율 15% · 조세특례제한법 제95조의2', fontsize=12, color='#6B7280')
fig.subplots_adjust(top=0.84, bottom=0.14, left=0.05, right=0.97)
fig.savefig('pkg/img/01.png', dpi=100); plt.close(fig)
# 02 월 100만원일 때 세 경우 지금→정부안
fig, ax = plt.subplots(figsize=(9, 6.6), dpi=100)
cases = [('일반\n(총급여 8,000 이하)', credit(100, 1000, .15), credit(100, 1200, .15)),
         ('총급여 5,500\n이하', credit(100, 1000, .17), credit(100, 1200, .17)),
         ('청년 15~34세\n(총급여 5,500 초과)', credit(100, 1000, .15), credit(100, 1200, .17))]
x = np.arange(len(cases)); w = 0.32
for k, (col, nm) in enumerate([(GR, '지금'), (ORG, '정부안')]):
    vals = [c[1 + k] for c in cases]
    ax.bar(x + (k - .5) * w, vals, w, color=col, label=nm)
    for xi, v in zip(x + (k - .5) * w, vals): ax.text(xi, v + 4, f'{v:.0f}', ha='center', fontsize=14, color=INK)
for i, c in enumerate(cases): ax.text(i, c[2] + 24, f'+{c[2]-c[1]:.0f}만원', ha='center', fontproperties=Bs(18), color=ORG)
ax.set_xticks(x); ax.set_xticklabels([c[0] for c in cases], fontsize=14); ax.set_yticks([]); ax.set_ylim(0, 260)
for s in ('top', 'right', 'left'): ax.spines[s].set_visible(False)
ax.legend(frameon=False, fontsize=14, loc='upper left')
fig.text(0.05, 0.92, '월세 월 100만원일 때 공제액 (만원)', fontproperties=Bs(22), color=INK)
fig.text(0.05, 0.02, '정부안은 국회 확정 전 · 청년 특례는 2029년까지로 보도', fontsize=12, color='#6B7280')
fig.subplots_adjust(top=0.84, bottom=0.14, left=0.05, right=0.97)
fig.savefig('pkg/img/02.png', dpi=100); plt.close(fig)
print('ok')
