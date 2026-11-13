# floor1114 그림 2장 — 01 층 띠별 6층 이상 대비 값(매매·전세, calc2_out.txt) 02 높은 층보다 싸게 거래된 1층 몫(calc2_out.txt)
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
BLUE, LBLUE, INK, GR, SUBC, ORG = '#1D4ED8', '#93C5FD', '#111827', '#CBD5E1', '#6B7280', '#EA580C'
# 01 — 6층 이상 중간값보다 몇 % 낮았나(가운데)
lab = ['1층', '2층', '3~5층']; tr = [7.2, 4.4, 1.5]; je = [4.5, 0.3, 0.0]
fig, ax = plt.subplots(figsize=(9, 6.2), dpi=100)
x = np.arange(len(lab)); w = 0.36
b1 = ax.bar(x - w/2, tr, w, color=ORG, label='매매'); b2 = ax.bar(x + w/2, je, w, color=BLUE, label='전세')
for bars, vals in ((b1, tr), (b2, je)):
    for b, v in zip(bars, vals): ax.text(b.get_x() + b.get_width()/2, v + 0.15, f'{v:g}%', ha='center', fontproperties=Bs(18), color=INK)
ax.set_xticks(x); ax.set_xticklabels(lab, fontproperties=Bs(18)); ax.set_ylim(0, 9); ax.set_yticks([])
for s in ('top', 'right', 'left'): ax.spines[s].set_visible(False)
ax.legend(frameon=False, prop=Bs(16), loc='upper right')
fig.text(0.04, 0.91, '같은 단지·같은 면적 높은 층(6층 이상)보다', fontproperties=Bs(21), color=INK)
fig.text(0.04, 0.84, '몇 % 낮게 거래됐나 · 서울 2026년 8~10월 계약', fontsize=16, color=SUBC)
fig.text(0.04, 0.03, '국토교통부 아파트 매매·전월세 실거래(서울 25개 구, 11/13 받음) · 해제 거래·월세 낀 계약 뺌 · 가운데 값', fontsize=10, color=SUBC)
fig.subplots_adjust(top=0.78, bottom=0.12, left=0.06, right=0.97)
fig.savefig('pkg/img/01.png', dpi=100); plt.close(fig)
# 02 — 1층 거래 가운데 높은 층 중간값보다 싸게 거래된 몫
rows = [('매매', 203, 215, ORG), ('전세 새 계약', 115, 181, BLUE), ('전세 갱신', 195, 314, LBLUE)]
fig, ax = plt.subplots(figsize=(9, 5.4), dpi=100)
ys = list(range(len(rows)))[::-1]
for y, (nm, a, n, c) in zip(ys, rows):
    ax.barh(y, 100, color=GR, height=0.55); ax.barh(y, a / n * 100, color=c, height=0.55)
    ax.text(a / n * 100 - 1.5, y, f'{a / n * 100:.0f}%', va='center', ha='right', fontproperties=Bs(20), color='white')
    ax.text(101.5, y, f'{n}건 중 {a}건', va='center', fontsize=14, color=SUBC)
ax.set_yticks(ys); ax.set_yticklabels([r[0] for r in rows], fontproperties=Bs(17)); ax.set_xlim(0, 125); ax.set_xticks([])
for s in ('top', 'right', 'bottom'): ax.spines[s].set_visible(False)
fig.text(0.04, 0.9, '1층 거래 중 높은 층보다 싸게 거래된 몫', fontproperties=Bs(21), color=INK)
fig.text(0.04, 0.82, '같은 단지·같은 면적 6층 이상 중간값과 비교', fontsize=16, color=SUBC)
fig.text(0.04, 0.03, '국토교통부 아파트 매매·전월세 실거래 서울 2026년 8~10월 · 전세는 새 계약끼리·갱신끼리 따로 비교', fontsize=10, color=SUBC)
fig.subplots_adjust(top=0.74, bottom=0.13, left=0.2, right=0.97)
fig.savefig('pkg/img/02.png', dpi=100); plt.close(fig)
print('ok')
